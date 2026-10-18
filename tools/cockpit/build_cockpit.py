"""Build site/data/cockpit.json, the data behind the agent cockpit page.

    python tools/cockpit/build_cockpit.py                 # writes site/data/cockpit.json
    python tools/cockpit/build_cockpit.py --inertia 6     # raise the stuck flag after 6 sections
    python tools/cockpit/build_cockpit.py --no-history    # skip dating sections from git history

Reads research/AGENT_HANDOFF.md, the negative-results registry, the progress
snapshot's git history, .research_checkpoint.json and, when present,
research/audits/spend_summary.json. Git is used read-only (log, show, status).
Never imports core/ or theorems/.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable


HANDOFF = "research/AGENT_HANDOFF.md"
REGISTRY = "research/registry/negative_results.json"
QUARANTINE = "research/registry/quarantined_campaign_negatives.json"
SNAPSHOT = "research/progress_snapshot.json"
CHECKPOINT = ".research_checkpoint.json"
SPEND = "research/audits/spend_summary.json"


# ---------- Sections ----------


@dataclass(frozen=True)
class Section:
    index: int  # position in the file; 0 is the top (newest) section
    line: int  # 1-based line number of the "## " heading
    heading: str
    body: str


def split_sections(text: str) -> list[Section]:
    """Split the handoff into its "## " sections, ignoring headings inside code fences."""
    sections: list[Section] = []
    heading, line_no, body = None, 0, []
    in_fence = False

    def close() -> None:
        if heading is not None:
            sections.append(Section(len(sections), line_no, heading, "\n".join(body).strip("\n")))

    for number, line in enumerate(text.splitlines(), start=1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        if not in_fence and line.startswith("## "):
            close()
            heading, line_no, body = line[3:].strip(), number, []
            continue
        if heading is not None:
            body.append(line)
    close()
    return sections


HEADING_DATE = re.compile(r"(?<!\d)(20\d\d-[01]\d-[0-3]\d)(?!\d)")


def heading_date(heading: str) -> str | None:
    """A YYYY-MM-DD date written in the heading itself, if any. Most headings carry none."""
    match = HEADING_DATE.search(heading)
    return match.group(1) if match else None


# ---------- Directions ----------

# Letter boundaries, not word boundaries, so snake_case paths (dcp_native_tree.py) and
# hyphenated CLI names (dcp-native-tree) count, while HDQI never counts as DQI.
_L, _R, _S = r"(?<![a-z])", r"(?![a-z])", r"[-_ ]"


@dataclass(frozen=True)
class Direction:
    id: str
    label: str
    patterns: tuple[str, ...]
    compiled: tuple[re.Pattern, ...] = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "compiled", tuple(re.compile(p, re.I) for p in self.patterns))


# Order breaks ties: narrower directions first.
DIRECTIONS: tuple[Direction, ...] = (
    Direction("hdqi", "HDQI", (_L + "hdqi" + _R, "hamiltonian" + _S + "dqi")),
    Direction(
        "opi",
        "OPI / prime character",
        (
            _L + "opi" + _R, _L + "dqi" + _R, "prime" + _S + "character", _L + "morse" + _R, _L + "jacobi" + _R,
            "optimal polynomial intersection", "known" + _S + "norm", _L + "norm" + _S + "(solver|attack|witness)",
            "reed" + _S + "solomon", "semicircle",
        ),
    ),
    Direction(
        "bpqm",
        "BPQM / polar",
        (
            _L + "bpqm" + _R, _L + "polar" + _S + "(code|source|conditional|shaping|sampler)",
            "successive" + _S + "cancellation", "belief" + _S + "propagation", _L + "gibbs" + _R,
        ),
    ),
    Direction(
        "dcp",
        "DCP / dihedral coset",
        (
            _L + "e?dcp" + _R, "dihedral", _L + "dhsp?" + _R, "hidden" + _S + "shift", "subset" + _S + "sum",
            "kuperberg", _L + "regev" + _R, "sine" + _S + "window", "phase" + _S + "bank",
        ),
    ),
    Direction(
        "carrier_pgm",
        "Carrier / PGM",
        (
            _L + "carriers?" + _R, _L + "pgm" + _R, "pretty" + _S + "good measurement", _L + "racah" + _R,
            "plancherel", "recoupling", "involution", "hyperoctahedral", "tetrahedral", _L + "6j" + _R,
            "naimark", _L + "selectors?" + _R,
        ),
    ),
    Direction(
        "lattice",
        "Ternary / lattice",
        (
            "ternary", _L + "trits?" + _R, "lattices?" + _R, _L + "r?lwe" + _R, "ring" + _S + "lwe",
            _L + "cvp" + _R, _L + "u?svp" + _R, _L + "lll" + _R, _L + "babai" + _R, _L + "ntru" + _R,
            _L + "dgs" + _R, "cyclotomic", "q-?ary", _L + "sis" + _R, _L + "pip" + _R, "principal ideal",
        ),
    ),
    Direction(
        "code_equivalence",
        "Code equivalence",
        (
            "code" + _S + "equivalence", "self" + _S + "dual", _L + "goppa" + _R, "quasi" + _S + "cyclic",
            _L + "hull" + _R, "support" + _S + "splitting", "permutation code", _L + "wreath" + _R,
        ),
    ),
    Direction("other", "Other", ()),
)
OTHER = "other"
HEADING_WEIGHT = 3  # per distinct keyword in the heading
BODY_CAP = 12  # body mentions stop counting after this many
WEAK_BELOW = 3  # a winning score under this, or a tie, is a weak decision


@dataclass(frozen=True)
class DirectionResult:
    direction: str
    scores: dict[str, int]
    weak: bool


def classify_direction(heading: str, body: str) -> DirectionResult:
    """Score every direction: 3 per keyword in the heading plus body mentions (capped)."""
    scores: dict[str, int] = {}
    for direction in DIRECTIONS:
        if not direction.compiled:
            continue
        in_heading = sum(1 for pattern in direction.compiled if pattern.search(heading))
        in_body = sum(len(pattern.findall(body)) for pattern in direction.compiled)
        scores[direction.id] = HEADING_WEIGHT * in_heading + min(in_body, BODY_CAP)
    best = max(scores.values(), default=0)
    if best == 0:
        return DirectionResult(OTHER, scores, weak=False)
    winners = [d.id for d in DIRECTIONS if scores.get(d.id) == best]
    return DirectionResult(winners[0], scores, weak=best < WEAK_BELOW or len(winners) > 1)


# ---------- Agent attribution ----------

CODEX, GEMINI, UNKNOWN = "codex", "gemini", "unknown"


@dataclass(frozen=True)
class Cue:
    name: str
    agent: str
    where: str  # "heading" or "body"
    pattern: re.Pattern
    weight: int
    minimum: int = 1
    explicit: bool = False  # the agent names itself or the other agent, not just a style habit


CUES: tuple[Cue, ...] = (
    # Gemini: campaign-style headings, markdown-heavy bodies, unwrapped lines.
    Cue("investigation heading", GEMINI, "heading", re.compile(r"\bInvestigations? \d+ Proved\b"), 3, explicit=True),
    Cue("antigravity note heading", GEMINI, "heading", re.compile(r"\bAntigravity\b.*\bNote\b"), 3, explicit=True),
    Cue("em dash heading", GEMINI, "heading", re.compile(r" — "), 2),
    Cue("ampersand heading", GEMINI, "heading", re.compile(r" & "), 2),
    Cue("proved heading", GEMINI, "heading", re.compile(r"\bProved\b"), 1),
    Cue("bold spans", GEMINI, "body", re.compile(r"\*\*[^*\n]+\*\*"), 2, minimum=3),
    Cue("inline LaTeX", GEMINI, "body", re.compile(r"\$[^$\n]+\$"), 2, minimum=3),
    Cue(
        "stock phrases", GEMINI, "body",
        re.compile(r"strictly enforced|100% (COMPLETE|OK|intact)|fully (implemented|wired|verified)", re.I), 1,
    ),
    # Codex: talks about GPT and Gemini in the third person, hard-wraps, CAPS emphasis.
    Cue(
        "no GPT commit", CODEX, "body",
        re.compile(r"\bno (GPT|main-model) (commit|git)|\bGPT next\b|\bno GPT commits?\b", re.I), 3, explicit=True,
    ),
    Cue(
        "Gemini in third person", CODEX, "body",
        re.compile(
            r"\bGemini (can|owns|may|should|work|queue|integration|integrat|must)|remains? Gemini|"
            r"\b(to|for) Gemini\b|\bGemini:|\bGemini's\b",
            re.I,
        ),
        2,
        explicit=True,
    ),
    Cue("high-reasoning heading", CODEX, "heading", re.compile(r"High-Reasoning (Result|Frontier)"), 3),
    Cue("files template", CODEX, "body", re.compile(r"^Files and experiment IDs?:", re.M), 2),
    Cue("glued numerals", CODEX, "body", re.compile(r"\b(in|at|to|and|of|with|from|across|cover)\d"), 1, minimum=2),
    Cue("caps emphasis", CODEX, "body", re.compile(r"\b(NOT|ALL|ONLY|SAME|ACTUAL|EXACT|FULL|ALONE)\b"), 1, minimum=2),
)
PROSE_MIN_LINES = 6  # the line-layout cue needs this many prose lines
UNWRAPPED_SHARE = 0.25  # share of prose lines over 100 characters that reads as unwrapped
WRAP_WIDTH = 82
LAYOUT_WEIGHTS = {GEMINI: 2, CODEX: 1}
LAYOUT_CUE_NAMES = {GEMINI: "unwrapped lines", CODEX: "hard-wrapped lines"}
LABEL_MIN = 3  # an agent needs this score ...
LABEL_MARGIN = 2  # ... and this lead over the other agent; otherwise "unknown"


@dataclass(frozen=True)
class Attribution:
    agent: str
    scores: dict[str, int]
    cues: list[str]
    explicit: dict[str, int]  # score from explicit cues only, per agent


def _layout_cue(body: str) -> str | None:
    prose = [
        line for line in body.splitlines()
        if line.strip()
        and not line.startswith(("    ", "\t"))
        and not re.match(r"\s*([-*#>|`]|\d+\.)", line)
    ]
    if len(prose) < PROSE_MIN_LINES:
        return None
    long_share = sum(len(line) > 100 for line in prose) / len(prose)
    if long_share >= UNWRAPPED_SHARE:
        return GEMINI
    if all(len(line) <= WRAP_WIDTH for line in prose):
        return CODEX
    return None


def label_agent(scores: dict[str, int]) -> str:
    for agent, rival in ((GEMINI, CODEX), (CODEX, GEMINI)):
        if scores[agent] >= LABEL_MIN and scores[agent] - scores[rival] >= LABEL_MARGIN:
            return agent
    return UNKNOWN


def attribute_agent(heading: str, body: str) -> Attribution:
    """Label a section codex, gemini or unknown from wording conventions alone."""
    scores = {CODEX: 0, GEMINI: 0}
    explicit = {CODEX: 0, GEMINI: 0}
    cues = []
    for cue in CUES:
        text = heading if cue.where == "heading" else body
        if len(cue.pattern.findall(text)) >= cue.minimum:
            scores[cue.agent] += cue.weight
            if cue.explicit:
                explicit[cue.agent] += cue.weight
            cues.append(cue.name)
    layout = _layout_cue(body)
    if layout:
        scores[layout] += LAYOUT_WEIGHTS[layout]
        cues.append(LAYOUT_CUE_NAMES[layout])
    return Attribution(label_agent(scores), scores, cues, explicit)


def cue_table(counts: Counter) -> list[dict[str, Any]]:
    """Every cue with the agent it points to, its weight and how many sections it fired in."""
    rows = [(cue.name, cue.agent, cue.weight, cue.explicit) for cue in CUES]
    rows += [(name, agent, LAYOUT_WEIGHTS[agent], False) for agent, name in LAYOUT_CUE_NAMES.items()]
    return [
        {"name": name, "agent": agent, "weight": weight, "explicit": explicit, "sections": counts[name]}
        for name, agent, weight, explicit in rows
    ]


def attribution_check(results: list[Attribution]) -> dict[str, int]:
    """How the style cues alone do on sections whose explicit cues name one agent.

    Explicit cues (the agent naming itself or the other agent) are taken as the answer;
    the label is recomputed from the remaining style cues and compared with it.
    """
    check = {"explicit_sections": 0, "agree": 0, "disagree": 0, "abstain": 0}
    for result in results:
        named = [agent for agent, score in result.explicit.items() if score]
        if len(named) != 1:
            continue
        check["explicit_sections"] += 1
        style = {agent: result.scores[agent] - result.explicit[agent] for agent in result.scores}
        guess = label_agent(style)
        if guess == UNKNOWN:
            check["abstain"] += 1
        elif guess == named[0]:
            check["agree"] += 1
        else:
            check["disagree"] += 1
    return check


# ---------- Registry entries ----------

ID_TOKEN = re.compile(r"(?<![A-Za-z0-9_-])[A-Z][A-Z0-9_]*(?:-[A-Z0-9_]+)+(?![A-Za-z0-9_])")
WRAPPED_ID = re.compile(r"(?<=[A-Z0-9_])-\n[ \t]*(?=[A-Z0-9])")


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def registry_ids(root: Path) -> set[str]:
    """Ids of every negative result: the active registry plus quarantined records.

    Quarantined records were registry entries when they were written, so a section that
    added one still added a registry entry.
    """
    ids: set[str] = set()
    for rel in (REGISTRY, QUARANTINE):
        path = root / rel
        if not path.is_file():
            continue
        data = _read_json(path)
        for record in data if isinstance(data, list) else []:
            if isinstance(record, dict) and isinstance(record.get("id"), str):
                ids.add(record["id"])
    return ids


def mentioned_registry_ids(text: str, ids: set[str]) -> set[str]:
    """Registry ids that appear in the text, including ids hard-wrapped at a hyphen."""
    return set(ID_TOKEN.findall(WRAPPED_ID.sub("-", text))) & ids


def new_registry_ids(texts: list[str], ids: set[str]) -> list[list[str]]:
    """For texts in chronological order, the registry ids no earlier text mentioned."""
    seen: set[str] = set()
    result = []
    for text in texts:
        found = mentioned_registry_ids(text, ids)
        result.append(sorted(found - seen))
        seen |= found
    return result


# ---------- Chronology and inertia ----------

NOT_COMMITTED = "9999-12-31"  # sorts uncommitted sections after every committed one


def chronological_order(count: int, first_committed: dict[int, str | None]) -> list[int]:
    """Section indexes oldest first: by first commit date, then lower in the file is older."""
    return sorted(range(count), key=lambda i: (first_committed.get(i) or NOT_COMMITTED, -i))


def _label(direction_id: str) -> str:
    return next((d.label for d in DIRECTIONS if d.id == direction_id), direction_id)


def inertia(chronological: list[dict[str, Any]], threshold: int) -> dict[str, Any]:
    """Per direction, how many of its own sections have passed since one added a registry entry.

    Sections about other directions in between neither count nor reset the streak. The flag
    is raised when the streak reaches the threshold. "Other" is a catch-all and never flags.
    """
    rows: list[dict[str, Any]] = []
    runs: list[tuple[int, dict[str, Any]]] = []  # (chronological start, run)
    total = len(chronological)

    def close_run(direction_id: str, run: list[int], ongoing: bool) -> None:
        if len(run) >= threshold:
            first, last = chronological[run[0]], chronological[run[-1]]
            runs.append((run[0], {
                "direction": direction_id,
                "length": len(run),
                "from_index": first["index"],
                "to_index": last["index"],
                "from_date": first.get("first_committed"),
                "to_date": last.get("first_committed"),
                "ongoing": ongoing,
            }))

    for direction in DIRECTIONS:
        if direction.id == OTHER:
            continue
        positions = [pos for pos, row in enumerate(chronological) if row["direction"] == direction.id]
        if not positions:
            continue
        last_new, run = None, []
        for pos in positions:
            row = chronological[pos]
            if row["new_registry_ids"]:
                close_run(direction.id, run, False)
                run = []
                last_new = {
                    "index": row["index"],
                    "heading": row.get("heading", ""),
                    "ids": list(row["new_registry_ids"]),
                    "first_committed": row.get("first_committed"),
                }
            else:
                run.append(pos)
        close_run(direction.id, run, True)
        streak = len(run)
        rows.append({
            "direction": direction.id,
            "label": direction.label,
            "sections": len(positions),
            "streak": streak,
            "flag": streak >= threshold,
            "last_new": last_new,
            "latest_index": chronological[positions[-1]]["index"],
            "sections_ago": total - 1 - positions[-1],
        })
    return {
        "threshold": threshold,
        "directions": rows,
        "flags": [row for row in rows if row["flag"]],
        "runs": [run for _, run in sorted(runs, key=lambda item: item[0])],
    }


# ---------- Git (read-only) ----------

GitRunner = Callable[..., "str | None"]
READ_ONLY_GIT = frozenset({"log", "show", "status"})
RS, US = "\x1e", "\x1f"  # record and field separators in git log formats
COMMIT_LOG_ARGS = ("log", f"--format={RS}%H{US}%cs{US}%s", "--name-only")
SNAPSHOT_LOG_ARGS = ("log", f"--format=%H{US}%cs", "--", SNAPSHOT)
HANDOFF_LOG_ARGS = ("log", f"--format=%H{US}%cs", "--", HANDOFF)
CHECKPOINT_LOG_ARGS = ("log", "-1", f"--format=%H{US}%cs", "--", CHECKPOINT)
STATUS_ARGS = ("status", "--porcelain", "--untracked-files=all")


def git_runner(root: Path) -> GitRunner:
    """Run read-only git commands in root; return stdout, or None when git fails."""
    env = {**os.environ, "GIT_OPTIONAL_LOCKS": "0"}  # git status must not even refresh the index

    def run(*args: str) -> str | None:
        if not args or args[0] not in READ_ONLY_GIT:
            raise ValueError(f"the cockpit only runs read-only git commands, not {args[:1]!r}")
        try:
            result = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, env=env)
        except FileNotFoundError:
            return None
        return result.stdout if result.returncode == 0 else None

    return run


def parse_commit_log(text: str) -> list[dict[str, Any]]:
    """Commits from COMMIT_LOG_ARGS output, in log order (newest first)."""
    commits = []
    for record in text.split(RS):
        if not record.strip():
            continue
        header, _, rest = record.partition("\n")
        sha, day, subject = (header.split(US) + ["", ""])[:3]
        files = [line.strip() for line in rest.splitlines() if line.strip()]
        commits.append({"sha": sha, "date": day, "subject": subject, "files": files})
    return commits


def commit_topic(subject: str, files: list[str]) -> str:
    """The direction a commit is about.

    The subject decides when it names a direction. Otherwise the changed paths decide, but
    only when every path keyword points to one direction: big wiring commits touch many
    directions at once and stay "other".
    """
    by_subject = classify_direction(subject, "")
    if by_subject.direction != OTHER:
        return by_subject.direction
    scores = classify_direction("", "\n".join(files)).scores
    named = [direction for direction, score in scores.items() if score > 0 and direction != OTHER]
    return named[0] if len(named) == 1 else OTHER


def commits_per_day(commits: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Commits grouped by commit date, oldest day first, with a topic count per day."""
    days: dict[str, dict[str, Any]] = {}
    for commit in commits:
        day = days.setdefault(commit["date"], {"date": commit["date"], "count": 0, "topics": Counter(), "commits": []})
        topic = commit_topic(commit["subject"], commit["files"])
        day["count"] += 1
        day["topics"][topic] += 1
        day["commits"].append({"sha": commit["sha"][:8], "subject": commit["subject"][:140], "topic": topic})
    return [{**day, "topics": dict(day["topics"])} for _, day in sorted(days.items())]


def _numeric(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def metrics_series(versions: list[tuple[str, str, str]]) -> dict[str, Any]:
    """Snapshot metrics over time from (sha, commit date, file text), oldest first.

    A version is dated by its own updated_at when present; the latest version per date wins.
    """
    by_date: dict[str, dict[str, Any]] = {}
    for sha, commit_date, text in versions:
        try:
            snapshot = json.loads(text)
        except ValueError:
            continue
        if not isinstance(snapshot, dict):
            continue
        updated = snapshot.get("updated_at")
        day = updated[:10] if isinstance(updated, str) and len(updated) >= 10 else commit_date
        metrics = {k: v for k, v in (snapshot.get("metrics") or {}).items() if _numeric(v)}
        by_date[day] = {"date": day, "commit": sha[:8], "metrics": metrics}
    points = [by_date[day] for day in sorted(by_date)]
    keys = sorted({key for point in points for key in point["metrics"]})
    return {"keys": keys, "points": points}


STATUS_PREFIX = re.compile(
    r"^(latest|prior|previous|current|earlier|newest|completed|predecessor|new)\b[^:]{0,40}:\s*", re.I
)


def heading_key(heading: str) -> str:
    """A heading without the status prefix agents rewrite (Latest:, Prior:, Previous Pass:)."""
    stripped = STATUS_PREFIX.sub("", heading.strip())
    return " ".join(re.findall(r"[a-z0-9]+", stripped.lower()))


def _occurrence_keys(headings: list[str]) -> list[tuple[str, int]]:
    """(key, k) per heading, numbering repeats from the bottom of the file (the oldest first)."""
    seen: Counter = Counter()
    keys: list[tuple[str, int]] = []
    for heading in reversed(headings):
        key = heading_key(heading)
        seen[key] += 1
        keys.append((key, seen[key]))
    return list(reversed(keys))


def first_committed(sections: list[Section], versions: list[tuple[str, str]]) -> dict[int, str | None]:
    """Date each section by the first committed version of the handoff that contains it.

    versions are (commit date, file text), oldest first. Uncommitted sections get None.
    """
    first_seen: dict[tuple[str, int], str] = {}
    for day, text in versions:
        for key in _occurrence_keys([s.heading for s in split_sections(text)]):
            first_seen.setdefault(key, day)
    keys = _occurrence_keys([s.heading for s in sections])
    return {section.index: first_seen.get(key) for section, key in zip(sections, keys)}


def _porcelain_entries(porcelain: str) -> list[tuple[str, str]]:
    entries = []
    for line in porcelain.splitlines():
        if len(line) < 4 or line.startswith("!!"):
            continue
        status, path = line[:2], line[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        entries.append((status, path.strip().strip('"')))
    return entries


def dirty_paths(porcelain: str) -> set[str]:
    return {path for _, path in _porcelain_entries(porcelain)}


def dirty_summary(porcelain: str) -> dict[str, Any]:
    """Counts of modified and untracked files, by top-level folder. No file names leave here."""
    entries = _porcelain_entries(porcelain)
    untracked = sum(1 for status, _ in entries if status == "??")
    areas = Counter(path.split("/", 1)[0] if "/" in path else "(root)" for _, path in entries)
    return {
        "modified": len(entries) - untracked,
        "untracked": untracked,
        "total": len(entries),
        "by_area": dict(sorted(areas.items())),
    }


def checkpoint_status(
    root: Path,
    *,
    last_commit: tuple[str, str] | None,
    commit_shas: list[str],
    dirty: set[str],
    today: dt.date,
) -> dict[str, Any] | None:
    """Summary of .research_checkpoint.json, the agents' resumable session checkpoint."""
    path = root / CHECKPOINT
    if not path.is_file():
        return None
    data = _read_json(path)
    if not isinstance(data, dict):
        return None
    session = data.get("session_date")
    try:
        days_since = (today - dt.date.fromisoformat(str(session)[:10])).days
    except ValueError:
        days_since = None
    review = data.get("scientific_review_override") if isinstance(data.get("scientific_review_override"), dict) else {}
    completed = data.get("completed_subsystems")
    sha = last_commit[0] if last_commit else None
    return {
        "file": CHECKPOINT,
        "session_date": session,
        "days_since_session": days_since,
        "active_milestone": data.get("active_milestone"),
        "latest_verified_subsystem": data.get("latest_verified_subsystem"),
        "total_verified_subsystems": data.get("total_verified_subsystems"),
        "completed_subsystems": len(completed) if isinstance(completed, list) else None,
        "review": {key: review.get(key) for key in ("date", "status", "next_decision")} if review else None,
        "last_commit": {"sha": sha[:8], "date": last_commit[1]} if last_commit else None,
        "commits_since": commit_shas.index(sha) if sha in commit_shas else None,
        "uncommitted_changes": CHECKPOINT in dirty,
    }


SPEND_FIELDS = ("date", "runs", "wall_seconds", "cpu_seconds", "negatives_added", "tokens")


def spend_summary(root: Path) -> tuple[dict[str, Any] | None, str | None]:
    """The optional spend panel: (panel, warning). Missing file: (None, None)."""
    path = root / SPEND
    if not path.is_file():
        return None, None
    try:
        data = _read_json(path)
        days = data["days"]
        if not isinstance(days, list) or not all(isinstance(d, dict) and isinstance(d.get("date"), str) for d in days):
            raise ValueError("days must be a list of objects with a date")
    except (ValueError, KeyError, TypeError) as error:
        return None, f"{SPEND} was skipped: {error}"
    rows = sorted(({key: day.get(key) for key in SPEND_FIELDS} for day in days), key=lambda day: day["date"])
    return {"generated_on": data.get("generated_on"), "days": rows, "source": SPEND}, None


# ---------- Build ----------

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = "site/data/cockpit.json"
DEFAULT_INERTIA = 8


def _history(git: GitRunner, log_args: tuple[str, ...], rel: str) -> list[tuple[str, str, str]]:
    """Every committed version of rel as (sha, commit date, text), oldest first."""
    versions = []
    for line in reversed((git(*log_args) or "").splitlines()):
        sha, _, day = line.strip().partition(US)
        if not sha:
            continue
        text = git("show", f"{sha}:{rel}")
        if text is not None:
            versions.append((sha, day, text))
    return versions


def _section_rows(root: Path, git: GitRunner, history: bool) -> tuple[list[dict[str, Any]], list[Attribution]]:
    path = root / HANDOFF
    sections = split_sections(path.read_text(encoding="utf-8")) if path.is_file() else []
    versions = [(day, text) for _, day, text in _history(git, HANDOFF_LOG_ARGS, HANDOFF)] if history else []
    dates = first_committed(sections, versions)
    order = chronological_order(len(sections), dates)
    new_ids = new_registry_ids([sections[i].heading + "\n" + sections[i].body for i in order], registry_ids(root))
    position = {index: pos for pos, index in enumerate(order)}
    rows, attributions = [], []
    for section in sections:
        direction = classify_direction(section.heading, section.body)
        attribution = attribute_agent(section.heading, section.body)
        attributions.append(attribution)
        rows.append({
            "index": section.index,
            "line": section.line,
            "heading": section.heading,
            "heading_date": heading_date(section.heading),
            "first_committed": dates.get(section.index),
            "order": position[section.index],
            "direction": direction.direction,
            "direction_weak": direction.weak,
            "agent": attribution.agent,
            "cues": attribution.cues,
            "new_registry_ids": new_ids[position[section.index]],
        })
    return rows, attributions


def build(
    root: Path,
    *,
    git: GitRunner,
    inertia_threshold: int = DEFAULT_INERTIA,
    today: dt.date | None = None,
    history: bool = True,
) -> dict[str, Any]:
    """Everything the cockpit page shows, as one JSON-ready dict."""
    today = today or dt.date.today()
    warnings: list[str] = []
    porcelain = git(*STATUS_ARGS)  # read before anything is written
    rows, attributions = _section_rows(root, git, history)
    chronological = sorted(rows, key=lambda row: row["order"])
    commits = parse_commit_log(git(*COMMIT_LOG_ARGS) or "")
    checkpoint_log = (git(*CHECKPOINT_LOG_ARGS) or "").strip()
    last_commit = tuple(checkpoint_log.split(US)[:2]) if US in checkpoint_log else None
    by_direction = Counter(row["direction"] for row in rows)
    payload: dict[str, Any] = {
        "generated_by": "tools/cockpit/build_cockpit.py",
        "generated_on": today.isoformat(),
        "settings": {"history": history, "inertia_threshold": inertia_threshold},
        "head": {"sha": commits[0]["sha"][:8], "date": commits[0]["date"]} if commits else None,
        "directions": [{"id": d.id, "label": d.label} for d in DIRECTIONS],
        "sections": rows,
        "coverage": {
            "sections": len(rows),
            "by_direction": {d.id: by_direction[d.id] for d in DIRECTIONS},
            "other_share": round(by_direction[OTHER] / len(rows), 4) if rows else 0,
            "weak": sum(1 for row in rows if row["direction_weak"]),
        },
        "attribution": {
            "by_agent": {agent: sum(1 for row in rows if row["agent"] == agent) for agent in (CODEX, GEMINI, UNKNOWN)},
            "check": attribution_check(attributions),
            "cues": cue_table(Counter(cue for row in rows for cue in row["cues"])),
        },
        "inertia": inertia(chronological, inertia_threshold),
        "commits": {"total": len(commits), "days": commits_per_day(commits)},
        "metrics": metrics_series(_history(git, SNAPSHOT_LOG_ARGS, SNAPSHOT)),
        "dirty": dirty_summary(porcelain) if porcelain is not None else None,
        "checkpoint": checkpoint_status(
            root,
            last_commit=last_commit,
            commit_shas=[commit["sha"] for commit in commits],
            dirty=dirty_paths(porcelain or ""),
            today=today,
        ),
        "warnings": warnings,
    }
    spend, warning = spend_summary(root)
    if spend is not None:
        payload["spend"] = spend
    if warning:
        warnings.append(warning)
    return payload


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    path.write_text(text + "\n", encoding="utf-8")


def _positive(value: str) -> int:
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("must be at least 1")
    return number


def main(argv: list[str] | None = None, git: GitRunner | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=ROOT, help="Repository checkout to read.")
    parser.add_argument("--inertia", type=_positive, default=DEFAULT_INERTIA,
                        help="Sections of one direction without a new registry entry before it is flagged.")
    parser.add_argument("--no-history", action="store_true", help="Do not date sections from the handoff's git history.")
    parser.add_argument("--out", type=Path, help=f"Output file (default: ROOT/{OUTPUT}).")
    args = parser.parse_args(argv)
    payload = build(args.root, git=git or git_runner(args.root), inertia_threshold=args.inertia,
                    history=not args.no_history)
    out = args.out or args.root / OUTPUT
    write_json(out, payload)
    coverage, attribution = payload["coverage"], payload["attribution"]["by_agent"]
    print(f"wrote {out}: {coverage['sections']} sections, other share {coverage['other_share']:.1%}, "
          f"agents {attribution}, flags {[row['direction'] for row in payload['inertia']['flags']]}")
    for warning in payload["warnings"]:
        print(f"warning: {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
