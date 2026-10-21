"""Build the agent brief: what changed in the last week, and what to run before choosing a direction.

    python tools/brief/build_brief.py                    # writes research/audits/AGENT_BRIEF.md and agent_brief.json
    python tools/brief/build_brief.py --since-days 14
    python tools/brief/build_brief.py --out DIR --json   # write into DIR; print the JSON

Seven sections: negative-registry ids added and removed since the cutoff (git history), open
arXiv flags and verdict actions, referee flags, preflight problems, cockpit inertia, near
duplicates of the new negatives, and the five commands to run. A section whose source is
missing or broken says "Not available" and why; it never reads as "nothing to report".

Git is used read-only: only the exact argument lists `allowed_git_args` accepts are ever run.
Never imports core/ or theorems/.
"""

from __future__ import annotations

import argparse
import datetime as dt
import importlib
import json
import os
import re
import subprocess
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any, Callable

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.cockpit.build_cockpit import US, utc_day  # noqa: E402
from tools.corpus.docs import read_json  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUTPUT_MD = "research/audits/AGENT_BRIEF.md"
OUTPUT_JSON = "research/audits/agent_brief.json"
DEFAULT_SINCE_DAYS = 7
MAX_SINCE_DAYS = 3650  # ten years: longer than the repository's history, and far from date.min and 1970
REGISTRY = "research/registry/negative_results.json"
QUARANTINE = "research/registry/quarantined_campaign_negatives.json"
ARXIV_STATE = "research/audits/arxiv_collisions.json"
ARXIV_VERDICTS = "research/audits/arxiv_verdicts.json"
COCKPIT = "site/data/cockpit.json"
FLAGGED_LABELS = ("possible-kill", "possible-scoop")  # tools/arxiv_watch/watch.py FLAGGED
DUPLICATE_THRESHOLD = 0.8  # tools/corpus/README.md "Duplicates": a true restatement sits at 0.80


# ---------- Git (read-only) ----------

GitRunner = Callable[..., "str | None"]
LOG_FORMAT = f"--format=%H{US}%ct"
# Prints "true"/"false", then root's path below the top of its work tree ("" at the top).
HISTORY_ARGS = ("rev-parse", "--is-shallow-repository", "--show-prefix")
# The cutoff is the start of a UTC day. git reads a bare date (--before=2026-10-13) as that day
# at the current time of day, so the same command would pick different commits morning and
# evening; and --before keeps a commit dated exactly at its limit. So the limit is the last
# second before the cutoff (commit dates are whole seconds). [0-9], not \d: \d takes any
# Unicode digit.
BEFORE_ARG = re.compile(r"--before=[0-9]{4}-[0-9]{2}-[0-9]{2}T23:59:59Z")
FULL_SHA = re.compile(r"[0-9a-f]{40}(?:[0-9a-f]{24})?")
SHOW_ARG = re.compile(FULL_SHA.pattern + ":" + re.escape(REGISTRY))
GIT_TIMEOUT = 60  # seconds per git command; each takes well under one on this repository
# Variables that point git at a repository, its index, objects or refs, which git exports to
# hooks and a shell may export too: inherited, they would make git answer from that repository
# for any -C directory. git's own list (git rev-parse --local-env-vars; GIT_INTERNAL_SUPER_PREFIX
# from older versions), plus GIT_NAMESPACE.
REPOSITORY_ENV = (
    "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR", "GIT_CONFIG", "GIT_CONFIG_COUNT", "GIT_CONFIG_PARAMETERS",
    "GIT_DIR", "GIT_GRAFT_FILE", "GIT_IMPLICIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_INTERNAL_SUPER_PREFIX",
    "GIT_NAMESPACE", "GIT_NO_REPLACE_OBJECTS", "GIT_OBJECT_DIRECTORY", "GIT_PREFIX", "GIT_REPLACE_REF_BASE",
    "GIT_SHALLOW_FILE", "GIT_WORK_TREE",
)


def _log_args(cutoff: dt.date) -> tuple[str, ...]:
    """The newest change to the registry before the cutoff, as "<sha><US><unix time>".

    Path-limited and along the first parents only: the checked-out branch's own line, each
    merge compared with the branch's side of it. So the registry at the commit found is the
    registry this branch had at the cutoff. A record merged in from another branch in the
    window counts as new, however old its commit there; and the other branch's commits, older
    or newer, never stand in for this branch's registry (a tool branch merged with --no-ff, or
    a branch that changed the registry too).
    """
    before = f"--before={(cutoff - dt.timedelta(days=1)).isoformat()}T23:59:59Z"
    return ("log", "-1", "--first-parent", before, LOG_FORMAT, "--", REGISTRY)


def allowed_git_args(args: tuple[str, ...]) -> bool:
    """True only for the brief's own read-only git commands:

    ("log", "-1", "--first-parent", "--before=YYYY-MM-DDT23:59:59Z", "--format=%H<US>%ct", "--", REGISTRY),
    ("show", "<full sha>:" + REGISTRY), ("ls-tree", "--name-only", "<full sha>", "--", REGISTRY)
    and ("rev-parse", "--is-shallow-repository", "--show-prefix").
    """
    args = tuple(args)
    if args == HISTORY_ARGS:
        return True
    if len(args) == 7 and args[:3] == ("log", "-1", "--first-parent") and args[4:] == (LOG_FORMAT, "--", REGISTRY):
        return bool(BEFORE_ARG.fullmatch(args[3]))
    if len(args) == 2 and args[0] == "show":
        return bool(SHOW_ARG.fullmatch(args[1]))
    if len(args) == 5 and args[:2] == ("ls-tree", "--name-only") and args[3:] == ("--", REGISTRY):
        return bool(FULL_SHA.fullmatch(args[2]))
    return False


def git_runner(root: Path) -> GitRunner:
    """Run the brief's read-only git commands in root; return stdout, or None when git fails.

    Against root's own repository: the REPOSITORY_ENV variables are not passed on. Offline and
    non-interactive: a partial clone does not fetch a missing object from its promisor remote
    (GIT_NO_LAZY_FETCH, git 2.44 and later), git never prompts for credentials, and stdin is
    closed. Raises RuntimeError when a command runs longer than GIT_TIMEOUT.
    """
    env = {name: value for name, value in os.environ.items() if name not in REPOSITORY_ENV}
    env.update(GIT_OPTIONAL_LOCKS="0", GIT_NO_LAZY_FETCH="1", GIT_TERMINAL_PROMPT="0")

    def run(*args: str) -> str | None:
        if not allowed_git_args(args):
            raise ValueError(f"the brief only runs its own read-only git commands, not {args!r}")
        try:
            result = subprocess.run(["git", "-C", str(root), *args], capture_output=True, env=env,
                                    stdin=subprocess.DEVNULL, timeout=GIT_TIMEOUT)
        except subprocess.TimeoutExpired:
            raise RuntimeError(f"git {args[0]} did not finish within {GIT_TIMEOUT} s") from None
        except OSError:
            return None
        # A committed registry may hold bytes that are not UTF-8; replace them rather than fail.
        return result.stdout.decode("utf-8", errors="replace") if result.returncode == 0 else None

    return run


def _day(today: dt.date | str | None) -> dt.date:
    """A calendar day: today in UTC when None; a datetime is cut to its UTC date (a naive one is taken as UTC)."""
    if today is None:
        return dt.datetime.now(dt.timezone.utc).date()
    if isinstance(today, dt.datetime):
        return (today.astimezone(dt.timezone.utc) if today.tzinfo else today).date()
    return today if isinstance(today, dt.date) else dt.date.fromisoformat(today)


def cutoff_day(since_days: int, today: dt.date | str | None = None) -> dt.date:
    """The first day of the window: the brief covers changes from its start (00:00 UTC) on.

    Raises ValueError unless since_days is a whole number from 1 to MAX_SINCE_DAYS.
    """
    if isinstance(since_days, bool) or not isinstance(since_days, int) or not 1 <= since_days <= MAX_SINCE_DAYS:
        raise ValueError(f"since_days must be a whole number of days from 1 to {MAX_SINCE_DAYS}, not {since_days!r}")
    return _day(today) - dt.timedelta(days=since_days)


def since_commit(
    root: Path, since_days: int = 7, today: dt.date | str | None = None, git: GitRunner | None = None
) -> tuple[str, str] | None:
    """(sha, UTC commit date) of the registry's last change before the cutoff day (00:00 UTC)
    on the checked-out branch's first-parent line.

    The registry at that commit is the registry as this branch had it at the cutoff. None when git cannot
    answer; when the clone is shallow (its oldest commit is a cut, so the commit before the
    cutoff may be missing and an older one would be used silently); when root is not the top of
    its work tree (a copy inside another repository would be compared with that repository's
    history); or when no commit before the cutoff changed the registry.
    """
    return _baseline(since_days, today, git or git_runner(root))[0]


def _no_change_reason(cutoff: str) -> str:
    return f"no commit before {cutoff} changed {REGISTRY}: the registry, or the history, is younger than the window"


def _baseline(
    since_days: int, today: dt.date | str | None, git: GitRunner
) -> tuple[tuple[str, str] | None, str]:
    """since_commit's answer and, when it is None, why."""
    problem = _history_problem(git(*HISTORY_ARGS))
    if problem is not None:
        return None, problem
    cutoff = cutoff_day(since_days, today)
    answer = git(*_log_args(cutoff))
    if answer is None:
        return None, f"git log could not list the changes to {REGISTRY} before {cutoff.isoformat()}"
    sha, _, stamp = answer.strip().partition(US)
    day = utc_day(stamp)
    return ((sha, day), "") if sha and day else (None, _no_change_reason(cutoff.isoformat()))


def _history_problem(answer: str | None) -> str | None:
    """Why git history cannot give the registry at the cutoff, from the HISTORY_ARGS output; None if it can."""
    if answer is None:
        return "no git history: not a git checkout, or git is not installed"
    shallow, _, prefix = answer.partition("\n")
    if shallow.strip() == "true":
        return "shallow clone: the registry at the cutoff is not in the history (git fetch --unshallow)"
    if shallow.strip() != "false":
        return f"git did not say whether the clone is shallow ({answer.strip()!r})"
    if prefix.strip():
        return f"the root is not the top of its git work tree (it is {prefix.strip()} inside another repository)"
    return None


def _no_baseline_reason(git: GitRunner) -> str:
    return _history_problem(git(*HISTORY_ARGS)) or _no_change_reason("the cutoff")


def _unreadable_reason(git: GitRunner, sha: str, date: str | None) -> str:
    """Why `git show <sha>:REGISTRY` failed: absent from that commit only when git lists no such file there."""
    commit = f"commit {sha[:8]}" + (f" of {date}" if date else "")
    # ls-tree answers from the commit's trees alone, which even a blob-less partial clone holds,
    # and its answer does not depend on the language of git's messages.
    listed = git("ls-tree", "--name-only", sha, "--", REGISTRY)
    if listed is None:
        return f"git could not read {REGISTRY} at {commit}"
    if not listed.strip():
        return f"{REGISTRY} did not exist at the cutoff ({commit})"
    return (f"git could not read {REGISTRY} at {commit}: the file is in that commit, but its content is not in "
            "this clone (a partial clone?)")


def _ids(data: Any) -> set[str]:
    """Record ids of a registry: a list of records, or an object with a "records" list."""
    if isinstance(data, dict) and isinstance(data.get("records"), list):
        data = data["records"]
    if not isinstance(data, list):
        raise ValueError(f"unexpected registry shape: {type(data).__name__}")
    return {record["id"] for record in data if isinstance(record, dict) and isinstance(record.get("id"), str)}


def _quarantined_ids(root: Path) -> set[str] | None:
    """Ids in the working copy's quarantine file; empty when it is absent, None when it cannot be read."""
    path = root / QUARANTINE
    if not path.is_file():
        return set()
    try:
        return _ids(read_json(path))
    except (OSError, ValueError):
        return None


def registry_delta(
    root: Path, since_sha: str | None, git: GitRunner | None = None, since_date: str | None = None
) -> dict[str, Any]:
    """Negative-registry ids added and removed between the commit `since_sha` and the working copy.

    The working copy includes edits not committed yet. `quarantined` lists the removed ids
    that are now in the quarantine file (None when that file cannot be read). Unavailable
    (never "no change") when there is no baseline commit, the registry did not exist in it, or
    git cannot read it there.
    """
    root = Path(root)
    git = git or git_runner(root)
    if not since_sha:
        return {"available": False, "reason": _no_baseline_reason(git)}
    committed = git("show", f"{since_sha}:{REGISTRY}")
    if committed is None:
        return {
            "available": False,
            "reason": _unreadable_reason(git, since_sha, since_date),
            "since_sha": since_sha,
            "since_date": since_date,
        }
    path = root / REGISTRY
    if not path.is_file():
        return {"available": False, "reason": f"{REGISTRY} is missing from the working copy"}
    baseline = _ids(json.loads(committed))
    # read_json retries a read that lands while an agent rewrites the file, and reads UTF-8
    # strictly, as core/research_registry.py and the corpus do.
    current = _ids(read_json(path))
    removed = baseline - current
    quarantined = _quarantined_ids(root)
    return {
        "available": True,
        "added": sorted(current - baseline),
        "removed": sorted(removed),
        "quarantined": sorted(removed & quarantined) if quarantined is not None else None,
        "since_sha": since_sha,
        "since_date": since_date,
        "baseline_count": len(baseline),
        "current_count": len(current),
    }


# ---------- The other sections ----------


def _section(name: str, fn: Callable[..., dict[str, Any]], *args: Any) -> dict[str, Any]:
    """Run one section; any exception becomes {"available": False, "reason": "ExcType: msg"}."""
    try:
        result = fn(*args)
        if not isinstance(result, dict) or "available" not in result:
            raise TypeError(f"the {name} section returned {type(result).__name__}, not a dict with 'available'")
        return result
    except Exception as error:  # noqa: BLE001 - one broken source must not sink the whole brief
        return {"available": False, "reason": f"{type(error).__name__}: {error}"}


def _import_tool(module: str, label: str) -> tuple[Any, str | None]:
    """Another tool's module, imported only when its section runs: (module, None) or (None, reason)."""
    try:
        return importlib.import_module(module), None
    except ImportError as error:
        name = getattr(error, "name", None) or ""
        if isinstance(error, ModuleNotFoundError) and name and (module == name or module.startswith(name + ".")):
            return None, f"{label} not present"
        return None, f"{label} cannot be imported: {type(error).__name__}: {error}"


def _iso(day: dt.date | str) -> str:
    return day.isoformat() if isinstance(day, dt.date) else str(day)


def _arxiv_papers(path: Path) -> tuple[dict[str, Any] | None, str]:
    """The watch's stored papers, or (None, why) when the collisions file cannot give them."""
    if not path.is_file():
        return None, f"no {ARXIV_STATE}" if not os.path.lexists(path) else f"{ARXIV_STATE} is not a file"
    try:
        papers = read_json(path).get("papers")
    except (OSError, ValueError, AttributeError) as error:
        return None, f"{ARXIV_STATE} cannot be read ({type(error).__name__}: {error})"
    if not isinstance(papers, dict):
        return None, f'{ARXIV_STATE} has no "papers" object'
    return papers, ""


def arxiv_section(root: Path, since_date: dt.date | str) -> dict[str, Any]:
    """Flagged arXiv papers, verdicts recorded since `since_date`, and the actions still open.

    flagged: possible kills and scoops without a verdict (open, however old), then those first
    seen on or after `since_date` that have one; None, with `flagged_reason`, when the
    collisions file is missing or unreadable (open flags live only there), while the verdicts
    and actions are still given. reviewed: verdicts recorded on or after `since_date`. actions:
    every verdict with an action whose `action_done` is not JSON true. Verdicts come from the
    verdicts file, the source of truth, whether or not the watch has copied them onto its records.
    """
    root = Path(root)
    since = _iso(since_date)
    verdicts_module, reason = _import_tool("tools.arxiv_watch.verdicts", "tools/arxiv_watch")
    if verdicts_module is None:
        return {"available": False, "reason": reason}
    state_path = root / ARXIV_STATE
    if not state_path.is_file() and not (root / verdicts_module.VERDICTS_FILE).is_file():
        return {"available": False, "reason": f"no {ARXIV_STATE} and no {verdicts_module.VERDICTS_FILE} yet"}
    papers, flagged_reason = _arxiv_papers(state_path)
    verdicts = {
        arxiv_id: entry
        for arxiv_id, entry in verdicts_module.load_verdicts(root)["verdicts"].items()
        if isinstance(entry, dict)
    }

    reviewed = [
        {"id": arxiv_id, "verdict": entry.get("verdict"), "by": entry.get("by"), "reviewed_on": entry["reviewed_on"]}
        for arxiv_id, entry in sorted(verdicts.items())
        if isinstance(entry.get("reviewed_on"), str) and entry["reviewed_on"] >= since
    ]
    reviewed.sort(key=lambda item: item["reviewed_on"], reverse=True)
    actions = [
        {"id": arxiv_id, "action": str(entry["action"]).strip(), "by": entry.get("by")}
        for arxiv_id, entry in sorted(verdicts.items())
        # Only a JSON true closes an action: action_done is written by hand, and "false" is truthy.
        if str(entry.get("action") or "").strip() and entry.get("action_done") is not True
    ]
    if papers is None:
        return {"available": True, "flagged": None, "flagged_reason": flagged_reason, "reviewed": reviewed,
                "actions": actions}

    flagged = []
    for arxiv_id, record in papers.items():
        if not isinstance(record, dict) or record.get("label") not in FLAGGED_LABELS:
            continue
        entry = verdicts.get(arxiv_id)
        first_seen = record.get("first_seen")
        if entry is None or (isinstance(first_seen, str) and first_seen >= since):
            flagged.append({
                "id": arxiv_id,
                "title": record.get("title", ""),
                "label": record["label"],
                "first_seen": first_seen if isinstance(first_seen, str) else None,
                "verdict": entry.get("verdict") if entry else None,
            })
    # Open flags first, newest first within each group, undated last.
    flagged.sort(key=lambda item: item["id"])
    flagged.sort(key=lambda item: item["first_seen"] or "", reverse=True)
    flagged.sort(key=lambda item: item["verdict"] is not None)
    return {"available": True, "flagged": flagged, "reviewed": reviewed, "actions": actions}


def referee_section(root: Path) -> dict[str, Any]:
    """`tools/referee/referee.py status`: flagged (unsound, needs-work) and stale reviews."""
    referee, reason = _import_tool("tools.referee.referee", "tools/referee")
    if referee is None:
        return {"available": False, "reason": reason}
    return referee.status(Path(root))


def preflight_section(root: Path) -> dict[str, Any]:
    """The static preflight checks (`tools/preflight/preflight.py`), problems grouped by check."""
    preflight, reason = _import_tool("tools.preflight.preflight", "tools/preflight")
    if preflight is None:
        return {"available": False, "reason": reason}
    problems = preflight.run(Path(root))
    by_check: dict[str, list[dict[str, str]]] = {}
    for problem in problems:
        by_check.setdefault(problem.check, []).append({"path": problem.path, "message": problem.message})
    return {"available": True, "by_check": by_check, "total": len(problems)}


def inertia_section(root: Path) -> dict[str, Any]:
    """Directions the cockpit flags as stuck: many sections since the registry last gained a record there."""
    path = Path(root) / COCKPIT
    if not path.is_file():
        return {"available": False, "reason": f"no {COCKPIT} (python tools/cockpit/build_cockpit.py)"}
    cockpit = read_json(path)
    inertia = cockpit.get("inertia") or {}
    warnings = [str(warning) for warning in cockpit.get("warnings") or []]
    if not inertia.get("available"):
        why = "; ".join(warnings) or "no registry history"
        built = cockpit.get("generated_on")
        return {"available": False, "reason": f"the cockpit of {built} has no inertia measure: {why}"}
    flags = [
        {
            "direction": flag.get("direction"),
            "label": flag.get("label"),
            "streak": flag.get("streak"),
            "last_gain": (flag.get("last_gain") or {}).get("date"),
        }
        for flag in inertia.get("flags") or []
    ]
    return {
        "available": True,
        "generated_on": cockpit.get("generated_on"),
        "threshold": inertia.get("threshold"),
        "flags": flags,
        "warnings": warnings,
    }


def _open_corpus(root: Path) -> Any:
    from tools.corpus.api import Corpus

    corpus = Corpus(root)
    # Incremental. On 2026-10-21: a few seconds with nothing changed, about 26 s to build the
    # index from scratch in a fresh worktree (README.md, "Speed").
    corpus.refresh()
    return corpus


def _near_duplicates(corpus: Any, **kwargs: Any) -> list[Any]:
    from tools.corpus.duplicates import near_duplicates

    return near_duplicates(corpus, **kwargs)


def _bare(doc_id: str) -> str:
    return doc_id.rsplit(":", 1)[-1]


def duplicates_section(root: Path, added_ids: list[str] | None, corpus: Any = None) -> dict[str, Any]:
    """Near-duplicate pairs (TF-IDF cosine >= DUPLICATE_THRESHOLD) that involve a record added in the window.

    The corpus index is opened only when something was added. `added_ids` None means the
    registry delta was unavailable, so the section is too.
    """
    if added_ids is None:
        return {"available": False, "reason": "the registry delta is unavailable, so no new records are known"}
    added = set(added_ids)
    if not added:
        return {"available": True, "checked": 0, "threshold": DUPLICATE_THRESHOLD, "pairs": []}
    corpus = corpus if corpus is not None else _open_corpus(Path(root))
    pairs = _near_duplicates(corpus, kind="negative", threshold=DUPLICATE_THRESHOLD, limit=sys.maxsize)
    kept = []
    for pair in pairs:
        new = sorted({_bare(pair.a), _bare(pair.b)} & added)
        if new:
            kept.append({**asdict(pair), "new": new})
    return {"available": True, "checked": len(added), "threshold": DUPLICATE_THRESHOLD, "pairs": kept}


COMMANDS = (
    {
        "name": "oracle",
        "command": 'python tools/corpus/cli.py been-tried "<one paragraph describing the idea>"',
        "when": "Before proposing or extending a direction: read the nearest retained negatives and say how "
                "the idea escapes them (MCP been_tried).",
    },
    {
        "name": "screener",
        "command": "python tools/dqi_screen/screen.py --params CANDIDATE.json",
        "when": "Before any DQI claim: exit 1 means not viable under the Mazumder-Niroula soundness rules "
                "(MCP screen_dqi_candidate).",
    },
    {
        "name": "baselines",
        "command": 'python tools/corpus/cli.py baselines "<one line describing the idea>"',
        "when": "Before claiming an advantage: the classical algorithms the idea must be compared against "
                "(MCP classical_baselines).",
    },
    {
        "name": "preflight",
        "command": "python tools/preflight/preflight.py",
        "when": "Before every commit: exit 1 lists research JSON that does not parse and CLI references to "
                "untracked theorem modules.",
    },
    {
        "name": "duplicates",
        "command": "python tools/corpus/cli.py check-new --file DRAFT_RECORD.json",
        "when": "Before filing a negative: exit 2 means a retained or quarantined record already says it "
                "(MCP check_duplicate_negative).",
    },
)


def commands_section() -> dict[str, Any]:
    """The five checks an agent should run, with the moment to run each."""
    return {"available": True, "commands": [dict(command) for command in COMMANDS]}


# ---------- Build, render, write ----------


def _registry_section(root: Path, since_days: int, today: dt.date, git: GitRunner) -> dict[str, Any]:
    since, reason = _baseline(since_days, today, git)
    if since is None:
        return {"available": False, "reason": reason}
    return registry_delta(root, since[0], git, since[1])


def build(
    root: Path, since_days: int = DEFAULT_SINCE_DAYS, today: dt.date | str | None = None, git: GitRunner | None = None
) -> dict[str, Any]:
    """Every section of the brief, as one JSON-ready dict.

    Raises ValueError for a since_days outside 1 to MAX_SINCE_DAYS; never raises for a missing
    or broken source.
    """
    root = Path(root).resolve()
    day = _day(today)
    cutoff = cutoff_day(since_days, day)  # checks since_days before any section runs
    git = git or git_runner(root)
    registry = _section("registry", _registry_section, root, since_days, day, git)
    added = registry.get("added") if registry.get("available") else None
    return {
        "generated_on": day.isoformat(),
        "since_days": since_days,
        "registry": registry,
        "arxiv": _section("arxiv", arxiv_section, root, cutoff),
        "referee": _section("referee", referee_section, root),
        "preflight": _section("preflight", preflight_section, root),
        "inertia": _section("inertia", inertia_section, root),
        "duplicates": _section("duplicates", duplicates_section, root, added),
        "commands": _section("commands", commands_section),
    }


LIST_CAP = 40  # ids or rows shown per list; agent_brief.json has them all


def _cell(text: Any) -> str:
    return " ".join(str(text if text is not None else "").split()).replace("|", "/")


def _id_list(ids: list[str]) -> str:
    shown = ", ".join(f"`{rid}`" for rid in ids[:LIST_CAP])
    more = len(ids) - LIST_CAP
    return shown + (f", and {more} more (see agent_brief.json)" if more > 0 else "")


def _render_registry(section: dict[str, Any], since: str) -> list[str]:
    commit = section["since_sha"][:8] + (f" ({section['since_date']})" if section.get("since_date") else "")
    lines = [
        f"{section['current_count']} negative records in the working copy; {section['baseline_count']} at commit "
        f"{commit}, the registry's last change before {since}.",
        "",
    ]
    added, removed = section["added"], section["removed"]
    lines.append(f"Added ({len(added)}): {_id_list(added) if added else 'none'}.")
    if not removed:
        lines.append("Removed (0): none.")
        return lines
    quarantined = section.get("quarantined")
    if quarantined is None:
        note = "the quarantine file could not be read"
    elif len(quarantined) == len(removed):
        note = "all now in the quarantine file"
    else:
        note = f"{len(quarantined)} now in the quarantine file"
    lines.append(f"Removed ({len(removed)}, {note}): {_id_list(removed)}.")
    return lines


def _render_arxiv(section: dict[str, Any], since: str) -> list[str]:
    flagged, reviewed, actions = section["flagged"], section["reviewed"], section["actions"]
    counts: dict[str, int] = {}
    for item in reviewed:
        counts[str(item["verdict"])] = counts.get(str(item["verdict"]), 0) + 1
    tally = ", ".join(f"{verdict} {n}" for verdict, n in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])))
    if flagged is None:
        lines = [f"Possible kills and scoops: not available: {_cell(section.get('flagged_reason'))}. The verdicts "
                 "and actions below come from the verdicts file."]
    else:
        open_flags = sum(1 for item in flagged if item["verdict"] is None)
        lines = [f"Possible kills and scoops with no verdict yet: {open_flags}. First seen since {since} and already "
                 f"reviewed: {len(flagged) - open_flags}. Labels are triage; verdicts are judgement."]
    lines += [f"Verdicts recorded since {since}: {len(reviewed)}" + (f" ({tally})." if tally else "."), ""]
    # Every verdict of the window is named once: in the flagged table, or here.
    in_table = {item["id"] for item in flagged or []}
    others = [item for item in reviewed if item["id"] not in in_table]
    if others:
        where = "" if flagged is None else " on papers not in the flagged table below"
        lines += [f"Verdicts recorded since {since}{where} ({len(others)}):", ""]
        lines += [f"- `{item['id']}`: {_cell(item['verdict'])} ({_cell(item['by'])}, {item['reviewed_on']})."
                  for item in others[:LIST_CAP]]
        if len(others) > LIST_CAP:
            lines.append(f"- And {len(others) - LIST_CAP} more in agent_brief.json.")
        lines.append("")
    lines += [
        f"Open actions from verdicts ({len(actions)}; set `\"action_done\": true` in `{ARXIV_VERDICTS}` once done):",
        "",
    ]
    lines += [f"- `{item['id']}` ({item['by']}): {_cell(item['action'])}" for item in actions] or ["- None."]
    if flagged:
        lines += ["", "| arXiv | Label | First seen | Verdict | Title |", "|---|---|---|---|---|"]
        for item in flagged[:LIST_CAP]:
            verdict = item["verdict"] or "**open**: read it"
            first_seen = item["first_seen"] or "-"
            lines.append(f"| {item['id']} | {item['label']} | {first_seen} | {verdict} | {_cell(item['title'])} |")
        if len(flagged) > LIST_CAP:
            lines += ["", f"And {len(flagged) - LIST_CAP} more in agent_brief.json."]
    return lines


def _render_referee(section: dict[str, Any], since: str) -> list[str]:
    flagged, stale = section.get("flagged") or [], section.get("stale") or []
    lines = [
        f"{section.get('reviewed', 0)} notes reviewed; {len(flagged)} flagged unsound or needs-work; "
        f"{len(stale)} reviews stale (the note changed since). Queue: `research/audits/REFEREE_QUEUE.md`.",
        "",
    ]
    for item in flagged[:LIST_CAP]:
        claim = item.get("worst_claim") or {}
        worst = ""
        if claim:
            quote, finding = _cell(claim.get("quote")), _cell(claim.get("finding"))
            worst = f" Worst claim ({claim.get('verdict')}): \"{quote}\". {finding}"
        lines.append(f"- `{item['stem']}` **{item['overall']}** (reviewed {item.get('reviewed_on')}).{worst}")
    if stale:
        lines += ["", f"Stale: {_id_list(stale)}."]
    return lines


def _render_preflight(section: dict[str, Any], since: str) -> list[str]:
    total = section["total"]
    if not total:
        return ["No problems from the static checks of `python tools/preflight/preflight.py`."]
    noun = "problem" if total == 1 else "problems"
    lines = [f"{total} {noun} from the static checks of `python tools/preflight/preflight.py`:", ""]
    rows = [(check, problem) for check, problems in section["by_check"].items() for problem in problems]
    lines += [f"- {check}: `{problem['path']}`: {_cell(problem['message'])}" for check, problem in rows[:LIST_CAP]]
    if len(rows) > LIST_CAP:
        lines.append(f"- And {len(rows) - LIST_CAP} more: run the command above.")
    return lines


def _render_inertia(section: dict[str, Any], since: str) -> list[str]:
    lines = [
        f"From `{COCKPIT}`, built {section.get('generated_on')} (rebuild: `python tools/cockpit/build_cockpit.py`). "
        f"A direction is flagged after {section.get('threshold')} handoff sections with no registry gain in it.",
        "",
    ]
    flags = section["flags"]
    lines += [
        f"- {_cell(flag['label'])} (`{flag['direction']}`): {flag['streak']} sections since the registry last gained a "
        f"record here ({flag['last_gain'] or 'never'})."
        for flag in flags
    ] or ["- No direction is flagged."]
    lines += [f"- Warning: {_cell(warning)}" for warning in section.get("warnings") or []]
    return lines


def _render_duplicates(section: dict[str, Any], since: str) -> list[str]:
    if not section["checked"]:
        return ["No negative was added in the window, so there is nothing to compare."]
    pairs = section["pairs"]
    lines = [
        f"{len(pairs)} pairs at TF-IDF cosine {section['threshold']} or above involve one of the "
        f"{section['checked']} negatives added in the window."
    ]
    if pairs:
        lines[0] += " Read both records before merging them; a sweep sibling is a separate result and stays."
        lines += ["", "| Cosine | Record | Title | Record | Title |", "|---|---|---|---|---|"]
        for pair in pairs[:LIST_CAP]:
            lines.append(f"| {pair['score']:.2f} | `{pair['a']}` | {_cell(pair['title_a'])[:120]} | `{pair['b']}` | "
                         f"{_cell(pair['title_b'])[:120]} |")
    return lines


def _render_commands(section: dict[str, Any], since: str) -> list[str]:
    return [f"- **{item['name']}**: `{item['command']}`. {item['when']}" for item in section["commands"]]


SECTION_HEADINGS = (
    ("registry", "Registry", _render_registry),
    ("arxiv", "arXiv watch", _render_arxiv),
    ("referee", "Referee", _render_referee),
    ("preflight", "Preflight", _render_preflight),
    ("inertia", "Inertia", _render_inertia),
    ("duplicates", "Possible duplicates", _render_duplicates),
    ("commands", "Commands", _render_commands),
)


def render(brief: dict[str, Any]) -> str:
    """The brief as markdown: one fixed heading per section, "Not available: <reason>" when a source is missing."""
    since = cutoff_day(brief["since_days"], brief["generated_on"]).isoformat()
    lines = [
        "# Agent brief",
        "",
        f"Generated {brief['generated_on']} by `python tools/brief/build_brief.py`; covers the {brief['since_days']} "
        f"days since {since} (00:00 UTC). Do not edit by hand.",
        "Read it before choosing a direction. \"Not available\" means the source could not be read, not that "
        "there is nothing to report.",
        "",
    ]
    for key, heading, render_section in SECTION_HEADINGS:
        section = brief.get(key) or {"available": False, "reason": "missing from the brief"}
        lines += [f"## {heading}", ""]
        if not section.get("available"):
            lines.append(f"Not available: {_cell(section.get('reason') or 'no reason given')}")
        else:
            lines += render_section(section, since)
        lines.append("")
    return "\n".join(lines)


def write(root: Path, brief: dict[str, Any], out: Path | None = None) -> tuple[Path, Path]:
    """Write AGENT_BRIEF.md and agent_brief.json into `out` (default: root/research/audits)."""
    directory = Path(out) if out is not None else Path(root) / Path(OUTPUT_MD).parent
    directory.mkdir(parents=True, exist_ok=True)
    md, js = directory / Path(OUTPUT_MD).name, directory / Path(OUTPUT_JSON).name
    md.write_text(render(brief), encoding="utf-8")
    js.write_text(json.dumps(brief, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    return md, js


def _since_days_arg(value: str) -> int:
    try:
        number = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"not a whole number of days: {value!r}") from None
    if not 1 <= number <= MAX_SINCE_DAYS:
        raise argparse.ArgumentTypeError(f"must be from 1 to {MAX_SINCE_DAYS}")
    return number


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=ROOT, help="Checkout to read (default: this repository).")
    parser.add_argument("--since-days", type=_since_days_arg, default=DEFAULT_SINCE_DAYS,
                        help="Window: changes since this many days ago, from 00:00 UTC.")
    parser.add_argument("--out", type=Path,
                        help="Directory for AGENT_BRIEF.md and agent_brief.json (default: ROOT/research/audits).")
    parser.add_argument("--json", action="store_true", help="Print the brief as JSON instead of a summary.")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    if not root.is_dir():
        parser.error(f"--root {root} is not a directory")
    brief = build(root, since_days=args.since_days)
    md, js = write(root, brief, args.out)
    if args.json:
        print(json.dumps(brief, indent=2, sort_keys=True, ensure_ascii=False))
        return 0
    print(f"wrote {md} and {js}")
    for key, heading, _ in SECTION_HEADINGS:
        section = brief[key]
        print(f"{heading}: " + ("ok" if section.get("available") else f"not available ({section.get('reason')})"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
