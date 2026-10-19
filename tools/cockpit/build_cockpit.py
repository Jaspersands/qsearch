"""Build site/data/cockpit.json, the data behind the agent cockpit page.

    python tools/cockpit/build_cockpit.py                 # writes site/data/cockpit.json
    python tools/cockpit/build_cockpit.py --inertia 6     # raise the stuck flag after 6 sections
    python tools/cockpit/build_cockpit.py --no-history    # skip dating sections from git history

Reads research/AGENT_HANDOFF.md and its git history, the negative-results registry and
its git history, the progress snapshot's git history, .research_checkpoint.json and, when
present, research/audits/spend_summary.json. Git is used read-only: only the exact log,
show, status and rev-parse argument lists defined below are ever run. Never imports core/
or theorems/.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
from bisect import bisect_right
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
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


def _line_starts(text: str, token: str) -> list[int]:
    """Offsets of the lines that start with token."""
    found = [0] if text.startswith(token) else []
    needle, at = "\n" + token, text.find("\n" + token)
    while at != -1:
        found.append(at + 1)
        at = text.find(needle, at + 1)
    return found


def _fence_lines(text: str) -> list[tuple[int, int, str, str]]:
    """(line start, line end, marker, info string) for every line that opens or closes a fence."""
    lines = []
    for token in ("```", "~~~"):
        at = text.find(token)
        while at != -1:
            start = text.rfind("\n", 0, at) + 1
            if text[start:at].strip(" \t"):  # the run is not at the start of its line
                at = text.find(token, at + 3)
                continue
            end = text.find("\n", at)
            end = len(text) if end == -1 else end
            run = at
            while run < end and text[run] == token[0]:
                run += 1
            marker, info = text[at:run], text[run:end].strip()
            if not (marker[0] == "`" and "`" in info):  # ```x``` is inline code, not a fence
                lines.append((start, end, marker, info))
            at = text.find(token, end)
    return sorted(lines)


def _fenced_spans(text: str, headings: list[int]) -> list[tuple[int, int]]:
    """(start, end) character spans of the ``` and ~~~ code fences, oldest first.

    A fence closes at the next line made only of at least as many of the same character.
    A fence with no such line, or whose would-be closer comes only after another opening
    fence with an info string (```text), is taken as unclosed: it ends at the next "## "
    heading, so one missing closer cannot hide every later section.
    """
    lines = _fence_lines(text)
    spans: list[tuple[int, int]] = []
    i = 0
    while i < len(lines):
        start, _, marker, _ = lines[i]
        end, resume = None, len(lines)
        for j in range(i + 1, len(lines)):
            _, line_end, other, info = lines[j]
            if other[0] != marker[0] or len(other) < len(marker):
                continue
            if not info:
                end, resume = line_end, j + 1
                break
            break  # a new fence with an info string opens: the first one was never closed
        if end is None:
            k = bisect_right(headings, start)
            end = headings[k] if k < len(headings) else len(text)
            resume = next((j for j in range(i + 1, len(lines)) if lines[j][0] >= end), len(lines))
        spans.append((start, end))
        i = resume
    return spans


def split_sections(text: str) -> list[Section]:
    """Split the handoff into its "## " sections, ignoring headings inside code fences.

    Lines end at "\\n" only, as GitHub counts them, so line numbers match its #L anchors.
    """
    text = text.replace("\r\n", "\n")
    candidates = _line_starts(text, "## ")
    spans = _fenced_spans(text, candidates)
    starts, k = [], 0
    for position in candidates:
        while k < len(spans) and spans[k][1] <= position:
            k += 1
        if not (k < len(spans) and spans[k][0] <= position < spans[k][1]):
            starts.append(position)
    sections: list[Section] = []
    line, counted = 1, 0
    for n, start in enumerate(starts):
        line += text.count("\n", counted, start)
        counted = start
        eol = text.find("\n", start)
        eol = len(text) if eol == -1 else eol
        stop = starts[n + 1] if n + 1 < len(starts) else len(text)
        body = text[eol + 1:stop] if eol < stop else ""
        sections.append(Section(n, line, text[start + 3:eol].strip(), body.strip("\n")))
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


# ---------- Registry ids quoted in the handoff ----------

# Any run of letters, digits and underscores joined by hyphens (double hyphens included). A
# token is matched against the real registry ids as a whole, so NEG-A-B-v2 never counts as
# NEG-A-B and NEG--HIDDEN-INVOLUTION-... is found.
ID_TOKEN = re.compile(r"[A-Za-z0-9_]+(?:-+[A-Za-z0-9_]+)+")
WRAPPED_ID = re.compile(r"(?<=[A-Z0-9_])-\n[ \t]*(?=[A-Z0-9])")


def _read_text(path: Path) -> str:
    """A text file, with any byte that is not UTF-8 replaced rather than failing the build."""
    return path.read_bytes().decode("utf-8", errors="replace")


def _read_json(path: Path) -> Any:
    return json.loads(_read_text(path))


def _records(data: Any) -> dict[str, dict[str, Any]] | None:
    """Registry records by id, or None when the data is not a list of records."""
    if not isinstance(data, list):
        return None
    return {record["id"]: record for record in data if isinstance(record, dict) and isinstance(record.get("id"), str)}


def registry_ids(root: Path) -> set[str]:
    """Ids of every negative result: the active registry plus quarantined records.

    Quarantined records were registry entries when they were written, so a section that
    quotes one still quotes a registry id.
    """
    ids: set[str] = set()
    for rel in (REGISTRY, QUARANTINE):
        path = root / rel
        if path.is_file():
            ids |= set(_records(_read_json(path)) or {})
    return ids


def mentioned_registry_ids(text: str, ids: set[str]) -> set[str]:
    """Registry ids that appear in the text, including ids hard-wrapped at a hyphen."""
    return set(ID_TOKEN.findall(WRAPPED_ID.sub("-", text))) & ids


def _scan_handoff(versions: list[tuple[str, str]], ids: set[str] | None = None) -> tuple[dict, dict[str, tuple[str, int]]]:
    """One pass over the committed handoff versions (day, text), oldest first.

    Returns the day each section key first appears, and, when ids are given, for each id the
    key of the section that quoted it in the first version quoting it. Within that version a
    section that is new in it wins over an older section edited in it; after that the lower
    one (the older by file order) wins.
    """
    first_seen: dict[tuple[str, int], str] = {}
    credit: dict[str, tuple[str, int]] = {}
    scanned: set[str] = set()  # section texts already searched: their ids are credited already
    for day, text in versions:
        sections = split_sections(text)
        keys = _occurrence_keys([s.heading for s in sections])
        if ids:
            for i in sorted(range(len(sections)), key=lambda i: (keys[i] in first_seen, -i)):
                blob = sections[i].heading + "\n" + sections[i].body
                if blob in scanned:
                    continue
                scanned.add(blob)
                for rid in mentioned_registry_ids(blob, ids):
                    credit.setdefault(rid, keys[i])
        for key in keys:
            first_seen.setdefault(key, day)
    return first_seen, credit


def _assign_quotes(
    sections: list[Section], credit: dict[str, tuple[str, int]], ids: set[str], order: list[int]
) -> tuple[dict[int, list[str]], dict[str, int]]:
    keys = _occurrence_keys([s.heading for s in sections])
    index_of = {key: s.index for s, key in zip(sections, keys)}
    quotes: dict[int, list[str]] = {s.index: [] for s in sections}
    stats = {"from_history": 0, "from_current_text": 0, "lost": 0}
    for rid, key in credit.items():
        if key in index_of:
            quotes[index_of[key]].append(rid)
            stats["from_history"] += 1
        else:
            stats["lost"] += 1  # the section that quoted it first is gone or renamed
    credited = set(credit)
    by_index = {s.index: s for s in sections}
    for index in order:  # ids no committed version quotes: the oldest current section quoting them
        section = by_index[index]
        found = mentioned_registry_ids(section.heading + "\n" + section.body, ids) - credited
        quotes[index].extend(found)
        credited |= found
        stats["from_current_text"] += len(found)
    return {index: sorted(found) for index, found in quotes.items()}, stats


def first_quoted(
    sections: list[Section], versions: list[tuple[str, str]], ids: set[str], order: list[int]
) -> tuple[dict[int, list[str]], dict[str, int]]:
    """Credit each registry id to the section that quoted it in the first committed handoff version quoting it.

    The credit follows history, not today's text: agents reword sections, so the section that
    first quoted an id often stops quoting it. Ids no committed version quotes go to the oldest
    current section quoting them (order is the current sections oldest first). Ids whose first
    quoting section no longer exists are counted as lost and credited to no one.
    """
    _, credit = _scan_handoff(versions, ids)
    return _assign_quotes(sections, credit, ids, order)


# ---------- Registry growth from the registry's own history ----------

UNCLASSIFIED = "unclassified"


def record_direction(record: dict[str, Any]) -> DirectionResult:
    """A registry record's direction: the keyword table on its id (as the heading), claim and tags.

    A record that matches no keyword is "unclassified" rather than "other".
    """
    tags = record.get("applies_to")
    tags = [tag for tag in tags if isinstance(tag, str)] if isinstance(tags, list) else []
    result = classify_direction(str(record.get("id") or ""), f"{record.get('claim') or ''}\n{' '.join(tags)}")
    if result.direction == OTHER:
        return DirectionResult(UNCLASSIFIED, result.scores, weak=False)
    return result


def _gain(rid: str, day: str | None, record: dict[str, Any]) -> dict[str, Any]:
    direction = record_direction(record)
    return {"id": rid, "date": day, "direction": direction.direction, "weak": direction.weak}


def registry_gains(versions: list[tuple[str, str, str]], current: Any) -> dict[str, Any] | None:
    """Records the registry gained, dated by the first committed version that contains them.

    versions are (sha, UTC commit date, file text), oldest first. The first version that
    parses is the baseline: its records were there before anything could be measured.
    current is the parsed working-tree registry; its records that no commit holds yet are
    gains dated None. A record removed later still counts as gained on its day.
    """
    baseline: dict[str, Any] | None = None
    known: set[str] = set()
    gains: list[dict[str, Any]] = []
    parsed = 0
    for _, day, text in versions:
        try:
            records = _records(json.loads(text))
        except ValueError:
            records = None
        if records is None:
            continue
        parsed += 1
        if baseline is None:
            baseline = {"date": day, "records": len(records)}
            known |= set(records)
            continue
        for rid, record in records.items():
            if rid not in known:
                known.add(rid)
                gains.append(_gain(rid, day, record))
    if baseline is None:
        return None
    for rid, record in (_records(current) or {}).items():
        if rid not in known:
            known.add(rid)
            gains.append(_gain(rid, None, record))
    return {"versions": parsed, "baseline": baseline, "gains": gains, "ids": known}


def registry_summary(gains: dict[str, Any]) -> dict[str, Any]:
    """What the registry gained after its baseline, by direction and by day (None: not committed)."""
    entries = gains["gains"]
    committed = [gain for gain in entries if gain["date"] is not None]
    by_direction = {d.id: 0 for d in DIRECTIONS if d.id != OTHER}
    by_direction[UNCLASSIFIED] = 0
    days: dict[str | None, dict[str, Any]] = {}
    for gain in entries:
        by_direction[gain["direction"]] += 1
        day = days.setdefault(gain["date"], {"date": gain["date"], "records": 0, "by_direction": Counter()})
        day["records"] += 1
        day["by_direction"][gain["direction"]] += 1
    ordered = sorted(days.values(), key=lambda day: day["date"] or NOT_COMMITTED)
    return {
        "source": REGISTRY,
        "versions": gains["versions"],
        "baseline": gains["baseline"],
        "added": len(committed),
        "uncommitted": len(entries) - len(committed),
        "by_direction": by_direction,
        "unclassified": by_direction[UNCLASSIFIED],
        "weak": sum(1 for gain in entries if gain["weak"]),
        "last_gain": max((gain["date"] for gain in committed), default=None),
        "days": [{**day, "by_direction": dict(day["by_direction"])} for day in ordered],
    }


# ---------- Chronology and inertia ----------

NOT_COMMITTED = "9999-12-31"  # sorts uncommitted sections (and registry records) after every committed one


def chronological_order(count: int, first_committed: dict[int, str | None]) -> list[int]:
    """Section indexes oldest first: by first commit date, then lower in the file is older."""
    return sorted(range(count), key=lambda i: (first_committed.get(i) or NOT_COMMITTED, -i))


def _public_day(day: str | None) -> str | None:
    return None if day in (None, NOT_COMMITTED) else day


def _gains_by_direction(gains: list[dict[str, Any]]) -> dict[str, dict[str, list[str]]]:
    """direction -> {gain day (NOT_COMMITTED when not committed yet) -> ids gained that day}."""
    by_direction: dict[str, dict[str, list[str]]] = {}
    for gain in gains:
        by_direction.setdefault(gain["direction"], {}).setdefault(gain["date"] or NOT_COMMITTED, []).append(gain["id"])
    return by_direction


def registry_days(rows: list[dict[str, Any]], gains: list[dict[str, Any]]) -> dict[int, bool]:
    """Per section: was it first committed on a day the registry gained a record in its direction?"""
    days = {(gain["direction"], gain["date"] or NOT_COMMITTED) for gain in gains}
    return {
        row["index"]: row["direction"] != OTHER and (row["direction"], row.get("first_committed") or NOT_COMMITTED) in days
        for row in rows
    }


def _direction_runs(
    chronological: list[dict[str, Any]], positions: list[int], days: list[str], threshold: int, direction: str
) -> tuple[int, list[tuple[int, dict[str, Any]]]]:
    """(current streak, runs at or over the threshold) for one direction's sections and gain days."""
    runs: list[tuple[int, dict[str, Any]]] = []

    def close(run: list[int], epoch: int, ongoing: bool) -> None:
        if len(run) < threshold:
            return
        first, last = chronological[run[0]], chronological[run[-1]]
        runs.append((run[0], {
            "direction": direction,
            "length": len(run),
            "from_index": first["index"],
            "to_index": last["index"],
            "from_date": first.get("first_committed"),
            "to_date": last.get("first_committed"),
            "after_gain": _public_day(days[epoch - 1]) if epoch else None,
            "ended_by_gain": None if ongoing else _public_day(days[epoch]),
            "ongoing": ongoing,
        }))

    run: list[int] = []
    epoch = 0  # how many gain days fall on or before the current run's sections
    for pos in positions:
        day = chronological[pos].get("first_committed") or NOT_COMMITTED
        current = bisect_right(days, day)
        on_gain_day = current > 0 and days[current - 1] == day
        if current != epoch or on_gain_day:
            close(run, epoch, False)
            run, epoch = [], current
        if not on_gain_day:
            run.append(pos)
    ongoing = epoch == len(days)  # no gain came after the latest run
    close(run, epoch, ongoing)
    return (len(run) if ongoing else 0), runs


def inertia(chronological: list[dict[str, Any]], threshold: int, gains: list[dict[str, Any]] | None) -> dict[str, Any]:
    """Per direction, how many of its own sections were first committed after the registry last
    gained a record in that direction.

    gains are the registry's gained records ({"id", "date", "direction"}, date None when not
    committed yet), read from the registry's own git history. Sections first committed on a day
    the registry gained a record in their direction are not counted, and that day ends a run,
    as does any such day between two sections. Sections about other directions neither count
    nor end a run. The flag is raised when the current streak reaches the threshold. "Other" is
    a catch-all and never flags; gained records that match no keyword ("unclassified") end no
    run. Without registry history (gains None) the measure is unavailable.
    """
    if gains is None:
        return {"available": False, "threshold": threshold, "directions": [], "flags": [], "runs": []}
    by_direction = _gains_by_direction(gains)
    rows: list[dict[str, Any]] = []
    runs: list[tuple[int, dict[str, Any]]] = []
    total = len(chronological)
    for direction in DIRECTIONS:
        if direction.id == OTHER:
            continue
        positions = [pos for pos, row in enumerate(chronological) if row["direction"] == direction.id]
        if not positions:
            continue
        gained = by_direction.get(direction.id, {})
        days = sorted(gained)
        streak, direction_runs = _direction_runs(chronological, positions, days, threshold, direction.id)
        runs += direction_runs
        last = days[-1] if days else None
        rows.append({
            "direction": direction.id,
            "label": direction.label,
            "sections": len(positions),
            "streak": streak,
            "flag": streak >= threshold,
            "last_gain": {"date": _public_day(last), "records": len(gained[last]), "ids": gained[last][:3]} if last else None,
            "gained": sum(len(ids) for ids in gained.values()),
            "latest_index": chronological[positions[-1]]["index"],
            "sections_ago": total - 1 - positions[-1],
        })
    return {
        "available": True,
        "threshold": threshold,
        "directions": rows,
        "flags": [row for row in rows if row["flag"]],
        "runs": [run for _, run in sorted(runs, key=lambda item: item[0])],
    }


# ---------- Git (read-only) ----------

GitRunner = Callable[..., "str | None"]
RS, US = "\x1e", "\x1f"  # record and field separators in git log formats
# %ct (commit time as a Unix timestamp) rather than %cs: %cs is the date in each committer's
# own time zone, while the spend summary uses UTC days. utc_day() turns %ct into a UTC date.
COMMIT_LOG_ARGS = ("log", f"--format={RS}%H{US}%ct{US}%s", "--name-only")
SNAPSHOT_LOG_ARGS = ("log", f"--format=%H{US}%ct", "--", SNAPSHOT)
HANDOFF_LOG_ARGS = ("log", f"--format=%H{US}%ct", "--", HANDOFF)
REGISTRY_LOG_ARGS = ("log", f"--format=%H{US}%ct", "--", REGISTRY)
CHECKPOINT_LOG_ARGS = ("log", "-1", f"--format=%H{US}%ct", "--", CHECKPOINT)
STATUS_ARGS = ("status", "--porcelain", "--untracked-files=all")
SHALLOW_ARGS = ("rev-parse", "--is-shallow-repository")
# Every git argument list the builder runs, exactly. Anything else is refused before git starts,
# so no option such as --output=FILE can ever reach git.
ALLOWED_GIT_ARGS = frozenset({
    COMMIT_LOG_ARGS, SNAPSHOT_LOG_ARGS, HANDOFF_LOG_ARGS, REGISTRY_LOG_ARGS, CHECKPOINT_LOG_ARGS, STATUS_ARGS, SHALLOW_ARGS,
})
SHOW_PATHS = frozenset({HANDOFF, SNAPSHOT, REGISTRY})  # plus "git show <full sha>:<one of these>"
SHOW_ARG = re.compile(r"[0-9a-f]{40}(?:[0-9a-f]{24})?:(.+)")


def allowed_git_args(args: tuple[str, ...]) -> bool:
    """True only for the builder's own read-only git commands."""
    args = tuple(args)
    if args in ALLOWED_GIT_ARGS:
        return True
    if len(args) == 2 and args[0] == "show":
        match = SHOW_ARG.fullmatch(args[1])
        return bool(match and match.group(1) in SHOW_PATHS)
    return False


def git_runner(root: Path) -> GitRunner:
    """Run the builder's read-only git commands in root; return stdout, or None when git fails."""
    env = {**os.environ, "GIT_OPTIONAL_LOCKS": "0"}  # git status must not even refresh the index

    def run(*args: str) -> str | None:
        if not allowed_git_args(args):
            raise ValueError(f"the cockpit only runs its own read-only git commands, not {args!r}")
        try:
            result = subprocess.run(["git", "-C", str(root), *args], capture_output=True, env=env)
        except FileNotFoundError:
            return None
        # A committed file may hold bytes that are not UTF-8; replace them rather than fail.
        return result.stdout.decode("utf-8", errors="replace") if result.returncode == 0 else None

    return run


def utc_day(timestamp: str) -> str | None:
    """The UTC calendar date of a git %ct timestamp."""
    try:
        return dt.datetime.fromtimestamp(int(timestamp), dt.timezone.utc).date().isoformat()
    except (ValueError, OverflowError, OSError):
        return None


def parse_commit_log(text: str) -> list[dict[str, Any]]:
    """Commits from COMMIT_LOG_ARGS output, in log order (newest first), dated in UTC."""
    commits = []
    for record in text.split(RS):
        if not record.strip():
            continue
        header, _, rest = record.partition("\n")
        sha, stamp, subject = (header.split(US) + ["", ""])[:3]
        files = [line.strip() for line in rest.splitlines() if line.strip()]
        commits.append({"sha": sha, "date": utc_day(stamp), "subject": subject, "files": files})
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
    """Commits grouped by UTC commit date, oldest day first, with a topic count per day."""
    days: dict[str, dict[str, Any]] = {}
    for commit in commits:
        if not commit["date"]:
            continue
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


def _dates(sections: list[Section], first_seen: dict[tuple[str, int], str]) -> dict[int, str | None]:
    keys = _occurrence_keys([s.heading for s in sections])
    return {section.index: first_seen.get(key) for section, key in zip(sections, keys)}


def first_committed(sections: list[Section], versions: list[tuple[str, str]]) -> dict[int, str | None]:
    """Date each section by the first committed version of the handoff that contains it.

    versions are (commit date, file text), oldest first. Uncommitted sections get None.
    """
    first_seen, _ = _scan_handoff(versions)
    return _dates(sections, first_seen)


def head_lines(sections: list[Section], head_text: str | None) -> dict[int, int | None]:
    """Each current section's line number in the head commit's handoff (None when not in it).

    Links pin that commit, so a line number from the working tree could point elsewhere.
    """
    if head_text is None:
        return {section.index: None for section in sections}
    head = split_sections(head_text)
    line_of = dict(zip(_occurrence_keys([s.heading for s in head]), (s.line for s in head)))
    keys = _occurrence_keys([s.heading for s in sections])
    return {section.index: line_of.get(key) for section, key in zip(sections, keys)}


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
    """Counts of changed tracked files and untracked files. No file or folder names leave here."""
    entries = _porcelain_entries(porcelain)
    untracked = sum(1 for status, _ in entries if status == "??")
    return {"modified": len(entries) - untracked, "untracked": untracked, "total": len(entries)}


def checkpoint_status(
    root: Path,
    *,
    last_commit: tuple[str, str] | None,
    commit_shas: list[str],
    dirty: set[str] | None,
    today: dt.date,
) -> dict[str, Any] | None:
    """Summary of .research_checkpoint.json, the agents' resumable session checkpoint.

    dirty is None when git status was not available: local edits are then unknown, not absent.
    """
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
        "uncommitted_changes": None if dirty is None else CHECKPOINT in dirty,
    }


SPEND_FIELDS = ("date", "runs", "wall_seconds", "cpu_seconds", "negatives_added", "tokens")
OPTIONAL_SPEND_FIELDS = ("tokens_uncached",)  # passed through when the spend summary has it


def _spend_row(day: dict[str, Any]) -> dict[str, Any]:
    row = {key: day.get(key) for key in SPEND_FIELDS}
    row.update({key: day[key] for key in OPTIONAL_SPEND_FIELDS if key in day})
    # The spend summary writes wall_seconds 0.0 and cpu_seconds null for a day with no timed
    # run. That is "not recorded", not zero seconds.
    if row["cpu_seconds"] is None and not row["wall_seconds"]:
        row["wall_seconds"] = None
    return row


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
    rows = sorted((_spend_row(day) for day in days), key=lambda day: day["date"])
    return {"generated_on": data.get("generated_on"), "days": rows, "source": SPEND}, None


# ---------- Build ----------

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = "site/data/cockpit.json"
DEFAULT_INERTIA = 8
SHOW_WORKERS = 6
NO_GIT_WARNING = (
    "git is not available here, or this is not a git checkout. Commits, section dates, registry growth, "
    "inertia, the working tree and the checkpoint's commit are unknown."
)
SHALLOW_WARNING = (
    "This checkout is a shallow clone, so its git history is cut off. Sections are left undated, registry "
    "growth and inertia are not computed, the checkpoint's last commit is unknown, and commit counts and research "
    "metrics cover only the commits that were fetched. Run git fetch --unshallow and rebuild."
)


def _log_entries(git: GitRunner, log_args: tuple[str, ...]) -> list[tuple[str, str]]:
    """(sha, UTC commit date) for every commit a log lists, oldest first."""
    entries = []
    for line in reversed((git(*log_args) or "").splitlines()):
        sha, _, stamp = line.strip().partition(US)
        day = utc_day(stamp)
        if sha and day:
            entries.append((sha, day))
    return entries


def _history(git: GitRunner, log_args: tuple[str, ...], rel: str) -> list[tuple[str, str, str]]:
    """Every committed version of rel as (sha, UTC commit date, text), oldest first.

    The git show calls run a few at a time: each is a separate read-only process.
    """
    entries = _log_entries(git, log_args)
    with ThreadPoolExecutor(max_workers=SHOW_WORKERS) as pool:
        texts = list(pool.map(lambda entry: git("show", f"{entry[0]}:{rel}"), entries))
    return [(sha, day, text) for (sha, day), text in zip(entries, texts) if text is not None]


def _section_rows(
    root: Path,
    git: GitRunner,
    *,
    history: bool,
    head_text: str | None,
    ids: set[str],
    gains: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[Attribution], dict[str, int], set[str]]:
    path = root / HANDOFF
    sections = split_sections(_read_text(path)) if path.is_file() else []
    versions = [(day, text) for _, day, text in _history(git, HANDOFF_LOG_ARGS, HANDOFF)] if history else []
    first_seen, credit = _scan_handoff(versions, ids)
    dates = _dates(sections, first_seen)
    order = chronological_order(len(sections), dates)
    quotes, quote_stats = _assign_quotes(sections, credit, ids, order)
    lines = head_lines(sections, head_text)
    position = {index: pos for pos, index in enumerate(order)}
    rows, attributions = [], []
    for section in sections:
        direction = classify_direction(section.heading, section.body)
        attribution = attribute_agent(section.heading, section.body)
        attributions.append(attribution)
        rows.append({
            "index": section.index,
            "line": section.line,
            "head_line": lines[section.index],
            "heading": section.heading,
            "heading_date": heading_date(section.heading),
            "first_committed": dates.get(section.index),
            "order": position[section.index],
            "direction": direction.direction,
            "direction_weak": direction.weak,
            "agent": attribution.agent,
            "cues": attribution.cues,
            "first_quoted_ids": quotes[section.index],
        })
    marks = registry_days(rows, gains)
    for row in rows:
        row["registry_day"] = marks[row["index"]]
    quoted = set(credit) | {rid for found in quotes.values() for rid in found}
    return rows, attributions, quote_stats, quoted


def build(
    root: Path,
    *,
    git: GitRunner,
    inertia_threshold: int = DEFAULT_INERTIA,
    today: dt.date | None = None,
    history: bool = True,
) -> dict[str, Any]:
    """Everything the cockpit page shows, as one JSON-ready dict."""
    today = today or dt.datetime.now(dt.timezone.utc).date()
    warnings: list[str] = []
    shallow_answer = git(*SHALLOW_ARGS)
    available = shallow_answer is not None
    shallow = shallow_answer.strip() == "true" if available else None
    if not available:
        warnings.append(NO_GIT_WARNING)
    elif shallow:
        warnings.append(SHALLOW_WARNING)
    complete = available and not shallow
    use_history = history and complete

    porcelain = git(*STATUS_ARGS) if available else None  # read before anything is written
    commits = parse_commit_log(git(*COMMIT_LOG_ARGS) or "") if available else []
    head = commits[0] if commits else None
    head_text = git("show", f"{head['sha']}:{HANDOFF}") if head else None
    registry_path = root / REGISTRY
    current_registry = _read_json(registry_path) if registry_path.is_file() else None
    gains = registry_gains(_history(git, REGISTRY_LOG_ARGS, REGISTRY), current_registry) if use_history else None
    ids = registry_ids(root) | (gains["ids"] if gains else set())
    rows, attributions, quote_stats, quoted = _section_rows(
        root, git, history=use_history, head_text=head_text, ids=ids, gains=gains["gains"] if gains else []
    )
    chronological = sorted(rows, key=lambda row: row["order"])
    checkpoint_log = (git(*CHECKPOINT_LOG_ARGS) or "").strip() if complete else ""
    stamp = checkpoint_log.split(US)[:2] if US in checkpoint_log else None
    last_commit = (stamp[0], utc_day(stamp[1])) if stamp and utc_day(stamp[1]) else None
    by_direction = Counter(row["direction"] for row in rows)
    registry = None
    if gains:
        registry = registry_summary(gains)
        registry["quoted"] = len({gain["id"] for gain in gains["gains"]} & quoted)
    payload: dict[str, Any] = {
        "generated_by": "tools/cockpit/build_cockpit.py",
        "generated_on": today.isoformat(),
        "settings": {"history": history, "inertia_threshold": inertia_threshold},
        "git": {"available": available, "shallow": shallow, "history": use_history},
        # The commit the build started from. The commit that carries this page comes after it.
        "head": {"sha": head["sha"][:8], "commit": head["sha"], "date": head["date"]} if head else None,
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
        "registry": registry,
        "quotes": quote_stats,
        "inertia": inertia(chronological, inertia_threshold, gains["gains"] if gains else None),
        "commits": {"total": len(commits), "days": commits_per_day(commits), "complete": complete},
        "metrics": metrics_series(_history(git, SNAPSHOT_LOG_ARGS, SNAPSHOT)) if available else {"keys": [], "points": []},
        "dirty": dirty_summary(porcelain) if porcelain is not None else None,
        "checkpoint": checkpoint_status(
            root,
            last_commit=last_commit,
            commit_shas=[commit["sha"] for commit in commits],
            dirty=dirty_paths(porcelain) if porcelain is not None else None,
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
                        help="Sections of one direction since its last registry gain before it is flagged.")
    parser.add_argument("--no-history", action="store_true",
                        help="Do not read git history: sections stay undated and inertia is not computed.")
    parser.add_argument("--out", type=Path, help=f"Output file (default: ROOT/{OUTPUT}).")
    args = parser.parse_args(argv)
    payload = build(args.root, git=git or git_runner(args.root), inertia_threshold=args.inertia,
                    history=not args.no_history)
    out = args.out or args.root / OUTPUT
    write_json(out, payload)
    coverage, attribution = payload["coverage"], payload["attribution"]["by_agent"]
    flags = [(row["direction"], row["streak"]) for row in payload["inertia"]["flags"]]
    print(f"wrote {out}: {coverage['sections']} sections, other share {coverage['other_share']:.1%}, "
          f"agents {attribution}, flags {flags}")
    for warning in payload["warnings"]:
        print(f"warning: {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
