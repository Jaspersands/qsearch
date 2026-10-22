"""Build the agent brief: what changed in the last week, and what to run before choosing a direction.

    python tools/brief/build_brief.py                    # writes research/audits/AGENT_BRIEF.md and agent_brief.json
    python tools/brief/build_brief.py --since-days 14
    python tools/brief/build_brief.py --out DIR --json   # write into DIR; print the JSON

Seven sections: negative-registry ids added and removed since the cutoff (git history), open
arXiv flags and verdict actions, referee flags, preflight problems, cockpit inertia, near
duplicates of the new negatives, and the five commands to run. A section whose source is
missing or broken says "Not available" and why; it never reads as "nothing to report".

Git is used read-only. The brief's own git runs only the exact argument lists
`allowed_git_args` accepts, offline and with a timeout; the preflight section is the exception,
since tools/preflight/preflight.py runs its own local reads (rev-parse, ls-files, diff-files)
without that runner; none of them writes the index. Never imports core/ or theorems/.
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

from tools.cockpit.build_cockpit import US  # noqa: E402
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
# The cutoff is the start of a local day (window_start), given to git in UTC. git reads a bare
# date (--before=2026-10-13) as that day at the current time of day, so the same command would
# pick different commits morning and evening; and --before keeps a commit dated exactly at its
# limit. So the limit is the last second before the cutoff (commit dates are whole seconds, and
# time zones are whole minutes from UTC). [0-9], not \d: \d takes any Unicode digit.
BEFORE_ARG = re.compile(r"--before=[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:59Z")
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
    """The newest change to the registry before the cutoff (00:00 local time), as "<sha><US><unix time>".

    Path-limited and along the first parents only: the checked-out branch's own line, each
    merge commit compared with the branch's side of it. So a record merged in from another
    branch in the window by a merge commit counts as new, however old its commit there; and
    the other branch's commits, older or newer, never stand in for this branch's registry (a
    tool branch merged with --no-ff, or a branch that changed the registry too).

    A fast-forward is the limit: it leaves no merge commit, and git records nowhere when it
    happened. The other branch's commits become this branch's own first-parent line with their
    own dates, so a record that arrived by a fast-forward in the window counts from its
    commit's date (one committed before the window is not reported as added). Merge with --no-ff.
    """
    limit = window_start(cutoff).astimezone(dt.timezone.utc) - dt.timedelta(seconds=1)
    before = f"--before={limit:%Y-%m-%dT%H:%M:%S}Z"
    return ("log", "-1", "--first-parent", before, LOG_FORMAT, "--", REGISTRY)


def allowed_git_args(args: tuple[str, ...]) -> bool:
    """True only for the brief's own read-only git commands:

    ("log", "-1", "--first-parent", "--before=YYYY-MM-DDTHH:MM:59Z", "--format=%H<US>%ct", "--", REGISTRY),
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
    """A local calendar day: today when None; an aware datetime is cut to its local date, a naive one is taken as local.

    Local, not UTC: the arXiv watch (first_seen), the verdicts store and the referee
    (reviewed_on) stamp dt.date.today(), and the brief compares those stamps with its window.
    """
    if today is None:
        return dt.date.today()
    if isinstance(today, dt.datetime):
        return (today.astimezone() if today.tzinfo else today).date()
    return today if isinstance(today, dt.date) else dt.date.fromisoformat(today)


def window_start(cutoff: dt.date) -> dt.datetime:
    """00:00 local time on the cutoff day, with that day's offset from UTC (daylight saving may differ today)."""
    return dt.datetime.combine(cutoff, dt.time()).astimezone()


def _local_day(timestamp: str) -> str | None:
    """The local calendar date of a git %ct timestamp."""
    try:
        return dt.datetime.fromtimestamp(int(timestamp)).date().isoformat()
    except (ValueError, OverflowError, OSError):
        return None


def cutoff_day(since_days: int, today: dt.date | str | None = None) -> dt.date:
    """The first day of the window: the brief covers changes from its start (00:00 local time) on.

    Raises ValueError unless since_days is a whole number from 1 to MAX_SINCE_DAYS.
    """
    if isinstance(since_days, bool) or not isinstance(since_days, int) or not 1 <= since_days <= MAX_SINCE_DAYS:
        raise ValueError(f"since_days must be a whole number of days from 1 to {MAX_SINCE_DAYS}, not {since_days!r}")
    return _day(today) - dt.timedelta(days=since_days)


def since_commit(
    root: Path, since_days: int = 7, today: dt.date | str | None = None, git: GitRunner | None = None
) -> tuple[str, str] | None:
    """(sha, local commit date) of the registry's last change before the cutoff day (00:00
    local time) on the checked-out branch's first-parent line.

    The registry at that commit is the registry as this branch had it at the cutoff, except
    after a fast-forward in the window, which history cannot date (see _log_args: commits that
    arrived that way count from their own dates, so merge with --no-ff). None when git cannot
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
    day = _local_day(stamp)
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


def _records(data: Any) -> list:
    """Rows of a registry, without collapsing repeated ids."""
    if isinstance(data, dict) and isinstance(data.get("records"), list):
        data = data["records"]
    if not isinstance(data, list):
        raise ValueError(f"unexpected registry shape: {type(data).__name__}")
    return data


def _ids(data: Any) -> set[str]:
    """Record ids of a registry: a list of records, or an object with a "records" list."""
    return {record["id"] for record in _records(data)
            if isinstance(record, dict) and isinstance(record.get("id"), str)}


def _quarantined_ids(root: Path) -> set[str] | None:
    """Ids in the working copy's quarantine file; empty when it is absent, None when it cannot be
    read (a directory or a dangling link at its path is there, not absent)."""
    path = root / QUARANTINE
    if not os.path.lexists(path):
        return set()
    if not path.is_file():
        return None
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
    baseline_rows = _records(json.loads(committed))
    baseline = _ids(baseline_rows)
    # read_json retries a read that lands while an agent rewrites the file, and reads UTF-8
    # strictly, as core/research_registry.py and the corpus do.
    current_rows = _records(read_json(path))
    current = _ids(current_rows)
    seen, duplicate_ids = set(), set()
    for row in current_rows:
        rid = row.get("id") if isinstance(row, dict) else None
        if isinstance(rid, str):
            if rid in seen:
                duplicate_ids.add(rid)
            seen.add(rid)
    removed = baseline - current
    quarantined = _quarantined_ids(root)
    return {
        "available": True,
        "added": sorted(current - baseline),
        "removed": sorted(removed),
        "quarantined": sorted(removed & quarantined) if quarantined is not None else None,
        "since_sha": since_sha,
        "since_date": since_date,
        "baseline_count": len(baseline_rows),
        "current_count": len(current_rows),
        "duplicate_ids": sorted(duplicate_ids),
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


def _arxiv_state(path: Path) -> tuple[dict[str, Any] | None, str]:
    """The watch's state, or (None, why) when it cannot supply stored papers."""
    if not path.is_file():
        return None, f"no {ARXIV_STATE}" if not os.path.lexists(path) else f"{ARXIV_STATE} is not a file"
    try:
        state = read_json(path)
        papers = state.get("papers")
    except (OSError, ValueError, AttributeError) as error:
        return None, f"{ARXIV_STATE} cannot be read ({type(error).__name__}: {error})"
    if not isinstance(papers, dict):
        return None, f'{ARXIV_STATE} has no "papers" object'
    return state, ""


def _arxiv_coverage(state: dict[str, Any], since: str) -> dict[str, Any]:
    """Keep source checkpoints and missed windows beside the triage counts."""
    updated = state.get("updated")
    tracks = state.get("tracks_updated", {})
    gaps = state.get("gaps", [])
    warnings = []
    if not isinstance(tracks, dict):
        tracks = {}
        warnings.append("track checkpoints are unreadable")
    if not isinstance(gaps, list) or any(not isinstance(gap, dict) for gap in gaps):
        gaps = []
        warnings.append("coverage gaps are unreadable")
    if "tracks_updated" in state:
        from tools.arxiv_watch.tracks import TRACKS

        missing = sorted(set(TRACKS) - tracks.keys())
        if missing:
            warnings.append("no watch checkpoint for configured tracks: " + ", ".join(missing))
    dates = ([updated] if updated is not None else []) + list(tracks.values())
    valid_dates = []
    for value in dates:
        try:
            valid_dates.append(dt.date.fromisoformat(value).isoformat())
        except (TypeError, ValueError):
            warnings.append(f"invalid watch checkpoint: {value!r}")
    if not dates:
        warnings.append("watch checkpoint date is unknown")
    return {"updated": updated, "tracks_updated": tracks, "gaps": gaps,
            "stale": any(date < since for date in valid_dates), "warnings": warnings}


def arxiv_section(root: Path, since_date: dt.date | str) -> dict[str, Any]:
    """Flagged arXiv papers, verdicts recorded since `since_date`, and the actions still open.

    flagged: possible kills and scoops without a person's verdict (open, however old; as in the
    watch's digest, a judge's verdict alone leaves a flag open), then those first seen on or
    after `since_date` that have a person's verdict; None, with `flagged_reason`, when the
    collisions file is missing or unreadable (open flags live only there), while the verdicts
    and actions are still given. reviewed: verdicts recorded on or after `since_date`. actions:
    every person's verdict with an action whose `action_done` is not JSON true; judge actions
    remain proposed_actions awaiting a person. Verdicts come from the
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
    state, flagged_reason = _arxiv_state(state_path)
    papers = state["papers"] if state is not None else None
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
    all_actions = [
        {"id": arxiv_id, "action": str(entry["action"]).strip(), "by": entry.get("by"),
         **({"action_pending_clarification": entry["action_pending_clarification"]}
            if entry.get("action_pending_clarification") else {})}
        for arxiv_id, entry in sorted(verdicts.items())
        # Only a JSON true closes an action: action_done is written by hand, and "false" is truthy.
        if str(entry.get("action") or "").strip() and entry.get("action_done") is not True
    ]
    actions = [item for item in all_actions
               if not verdicts_module.by_judge(item) and not item.get("action_pending_clarification")]
    blocked_actions = [item for item in all_actions
                       if not verdicts_module.by_judge(item) and item.get("action_pending_clarification")]
    proposed_actions = [item for item in all_actions if verdicts_module.by_judge(item)]
    extra = {"proposed_actions": proposed_actions, "blocked_actions": blocked_actions,
             "coverage": _arxiv_coverage(state, since) if state is not None else None}
    if papers is None:
        return {"available": True, "flagged": None, "flagged_reason": flagged_reason, "reviewed": reviewed,
                "actions": actions, **extra}

    flagged = []
    for arxiv_id, record in papers.items():
        if not isinstance(record, dict) or record.get("label") not in FLAGGED_LABELS:
            continue
        entry = verdicts.get(arxiv_id)
        # As in the watch's digest: a judge's verdict is one model's reading, so only a
        # person's verdict closes a flag; one with only a judge's stays open, marked with it.
        is_open = entry is None or verdicts_module.by_judge(entry)
        first_seen = record.get("first_seen")
        if is_open or (isinstance(first_seen, str) and first_seen >= since):
            flagged.append({
                "id": arxiv_id,
                "title": record.get("title", ""),
                "label": record["label"],
                "first_seen": first_seen if isinstance(first_seen, str) else None,
                "verdict": entry.get("verdict") if entry else None,
                "by": entry.get("by") if entry else None,
                "open": is_open,
            })
    # Prioritize possible kills before scoops and the oldest open flag within each label.
    # Unknown dates come first so an undated kill cannot silently age out of the page.
    flagged.sort(key=lambda item: (not item["open"], item["label"] != "possible-kill",
                                   item["first_seen"] or "", item["id"]))
    return {"available": True, "flagged": flagged, "reviewed": reviewed, "actions": actions, **extra}


def referee_section(root: Path) -> dict[str, Any]:
    """`tools/referee/referee.py status`: flagged (unsound, needs-work) and stale reviews."""
    referee, reason = _import_tool("tools.referee.referee", "tools/referee")
    if referee is None:
        return {"available": False, "reason": reason}
    return referee.status(Path(root))


def preflight_section(root: Path) -> dict[str, Any]:
    """The static preflight checks (`tools/preflight/preflight.py`), problems grouped by check.

    Not available for a root without qsearch.py, which preflight.py's own command line refuses:
    every check would report a problem that only the wrong root causes.
    """
    preflight, reason = _import_tool("tools.preflight.preflight", "tools/preflight")
    if preflight is None:
        return {"available": False, "reason": reason}
    if not (Path(root) / "qsearch.py").is_file():
        return {"available": False, "reason": f"{root} is not a Q-Search checkout: it has no qsearch.py"}
    problems = preflight.run(Path(root))
    by_check: dict[str, list[dict[str, str]]] = {}
    for problem in problems:
        by_check.setdefault(problem.check, []).append({"path": problem.path, "message": problem.message})
    return {"available": True, "by_check": by_check, "total": len(problems)}


def _cockpit_warnings(value: Any) -> list[str]:
    """The cockpit's warnings: a list of strings; one string is one warning, not one per character."""
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if not isinstance(value, list):
        raise TypeError(f"{COCKPIT} warnings is a {type(value).__name__}, not a list")
    return [str(warning) for warning in value]


def _count(value: Any, what: str) -> int:
    """A whole number from the cockpit; anything else (NaN, a string, a bool) raises TypeError."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{COCKPIT} {what} is {value!r}, not a whole number")
    return value


def inertia_section(root: Path) -> dict[str, Any]:
    """Directions the cockpit flags as stuck: many sections since the registry last gained a record there.

    A malformed field (warnings not a list, a threshold or streak that is not a whole number)
    raises, so the section says not available rather than printing garbled values.
    """
    path = Path(root) / COCKPIT
    if not path.is_file():
        return {"available": False, "reason": f"no {COCKPIT} (python tools/cockpit/build_cockpit.py)"}
    cockpit = read_json(path)
    inertia = cockpit.get("inertia") or {}
    warnings = _cockpit_warnings(cockpit.get("warnings"))
    built = cockpit.get("generated_on")
    rebuild = "rebuild: python tools/cockpit/build_cockpit.py"
    if not isinstance(inertia, dict):
        raise TypeError(f"{COCKPIT} inertia is a {type(inertia).__name__}, not an object")
    if not inertia:
        return {"available": False, "reason": f"the cockpit of {built} has no inertia field ({rebuild})"}
    if "available" not in inertia:  # written before build_cockpit gave the measure that field
        return {"available": False, "reason": f"the cockpit of {built} is older than the brief: its inertia field has "
                                              f"no `available` ({rebuild})"}
    if not inertia["available"]:  # build_cockpit sets it false only without registry history
        why = "; ".join(warnings) or "no registry history"
        return {"available": False, "reason": f"the cockpit of {built} has no inertia measure: {why}"}
    flags = [
        {
            "direction": flag.get("direction"),
            "label": flag.get("label"),
            "streak": _count(flag.get("streak"), f"streak of {flag.get('direction')}"),
            "last_gain": (flag.get("last_gain") or {}).get("date"),
        }
        for flag in inertia.get("flags") or []
    ]
    return {
        "available": True,
        "generated_on": cockpit.get("generated_on"),
        "threshold": _count(inertia.get("threshold"), "inertia threshold"),
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
    registry delta was unavailable, so the section is too. `checked` counts the added records
    the index holds; `unchecked` names those it does not (it skips a record it cannot parse,
    and reads a registry that is not a list as raw text), and `index_issues` the problems it
    recorded for the negative registry files, any of which can hide a pair.
    """
    if added_ids is None:
        return {"available": False, "reason": "the registry delta is unavailable, so no new records are known"}
    added = set(added_ids)
    if not added:
        return {"available": True, "checked": 0, "unchecked": [], "index_issues": [], "threshold": DUPLICATE_THRESHOLD,
                "pairs": []}
    corpus = corpus if corpus is not None else _open_corpus(Path(root))
    unchecked = sorted(rid for rid in added if corpus.get(f"negative:{rid}") is None)
    index_issues = [f"{issue['path']}: {issue['message']}" for issue in corpus.issues()
                    if issue["path"] in (REGISTRY, QUARANTINE)]
    pairs = _near_duplicates(corpus, kind="negative", threshold=DUPLICATE_THRESHOLD, limit=sys.maxsize)
    kept = []
    for pair in pairs:
        new = sorted({_bare(pair.a), _bare(pair.b)} & added)
        if new:
            kept.append({**asdict(pair), "new": new})
    return {"available": True, "checked": len(added) - len(unchecked), "unchecked": unchecked,
            "index_issues": index_issues, "threshold": DUPLICATE_THRESHOLD, "pairs": kept}


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
        "when": "Before every commit: exit 1 lists JSON that does not parse under research/hypotheses/, "
                "research/registry/, research/audits/ and research/classical_baselines/, plus theorems/, core/ and "
                "qsearch_cli/ modules the CLI refers to that are missing or not tracked by git, and "
                "research/audits/cli_manifest.json subcommands missing from the CLI registry's ORDER or listed "
                "there under another module.",
    },
    {
        "name": "duplicates",
        "command": "python tools/corpus/cli.py check-new --file DRAFT_RECORD.json",
        "when": "Before filing a negative: exit 2 means a retained or quarantined record is close (TF-IDF cosine "
                "0.6 or above). A match is a record to read, not proof: extend it, say how the draft differs, or "
                "pass --allow ID for a sweep sibling you have read (MCP check_duplicate_negative).",
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
        "window_start": window_start(cutoff).isoformat(),
        "registry": registry,
        "arxiv": _section("arxiv", arxiv_section, root, cutoff),
        "referee": _section("referee", referee_section, root),
        "preflight": _section("preflight", preflight_section, root),
        "inertia": _section("inertia", inertia_section, root),
        "duplicates": _section("duplicates", duplicates_section, root, added),
        "commands": _section("commands", commands_section),
    }


LIST_CAP = 40  # ids or rows shown per list; agent_brief.json has them all
TITLE_CAP = 120  # characters of a title in the duplicates table; agent_brief.json has it whole


def _flat(text: Any) -> str:
    """Text on one line, otherwise verbatim: in a list item or a sentence a pipe is just a character."""
    return " ".join(str(text if text is not None else "").split())


def _clip(text: Any) -> str:
    """A title for the duplicates table: on one line, cut to TITLE_CAP characters and marked "..." when cut."""
    flat = _flat(text)
    return flat if len(flat) <= TITLE_CAP else flat[:TITLE_CAP].rstrip() + "..."


def _cell(text: Any) -> str:
    """Text for a table cell: one line, each pipe escaped as GFM reads it (\\|) so it cannot end the cell."""
    return _flat(text).replace("|", "\\|")


def _id_list(ids: list[str]) -> str:
    shown = ", ".join(f"`{rid}`" for rid in ids[:LIST_CAP])
    more = len(ids) - LIST_CAP
    return shown + (f", and {more} more (see agent_brief.json)" if more > 0 else "")


def _bullets(items: list[str], where: str = "agent_brief.json") -> list[str]:
    """List items, capped at LIST_CAP, then one item saying how many more and where they are."""
    more = len(items) - LIST_CAP
    return items[:LIST_CAP] + ([f"- And {more} more in {where}."] if more > 0 else [])


def _render_registry(section: dict[str, Any], since: str) -> list[str]:
    commit = section["since_sha"][:8] + (f" ({section['since_date']})" if section.get("since_date") else "")
    lines = [
        f"{section['current_count']} negative records in the working copy; {section['baseline_count']} at commit "
        f"{commit}, the registry's last change before {since}.",
        "",
    ]
    added, removed = section["added"], section["removed"]
    if section.get("duplicate_ids"):
        lines += [f"Duplicate ids in the working registry: {_id_list(section['duplicate_ids'])}. "
                  "The added/removed lists compare distinct ids; fix repeated ids before filing another record.", ""]
    lines.append(f"Added ({len(added)}): {_id_list(added) if added else 'none'}.")
    if not removed:
        lines.append("Removed (0): none.")
        return lines
    quarantined = section.get("quarantined")
    if quarantined is None:
        lines.append(f"Removed ({len(removed)}, the quarantine file could not be read): {_id_list(removed)}.")
    elif not quarantined or len(quarantined) == len(removed):
        note = "all now" if quarantined else "none now"
        lines.append(f"Removed ({len(removed)}, {note} in the quarantine file): {_id_list(removed)}.")
    else:  # say which ones moved to quarantine and which were dropped outright
        moved = set(quarantined)
        lost = [rid for rid in removed if rid not in moved]
        lines.append(f"Removed ({len(removed)}): {len(quarantined)} now in the quarantine file: "
                     f"{_id_list(quarantined)}; {len(lost)} not in it: {_id_list(lost)}.")
    return lines


def _by(item: dict[str, Any]) -> str:
    """Who recorded a verdict; an entry without `by` was written by hand (verdicts.by_judge counts it as a person's)."""
    return _flat(item.get("by")) or "by hand"


def _render_arxiv(section: dict[str, Any], since: str) -> list[str]:
    flagged, reviewed, actions = section["flagged"], section["reviewed"], section["actions"]
    counts: dict[str, int] = {}
    from tools.arxiv_watch.verdicts import by_judge

    human_reviews = [item for item in reviewed if not by_judge(item)]
    judge_reviews = [item for item in reviewed if by_judge(item)]
    for item in human_reviews:
        counts[_flat(item["verdict"])] = counts.get(_flat(item["verdict"]), 0) + 1
    tally = ", ".join(f"{verdict} {n}" for verdict, n in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])))
    if flagged is None:
        lines = [f"Possible kills and scoops: not available: {_flat(section.get('flagged_reason'))}. The verdicts "
                 "and actions below come from the verdicts file."]
    else:
        open_flags = sum(1 for item in flagged if item["open"])
        judged = sum(1 for item in flagged if item["open"] and item["verdict"] is not None)
        note = f" ({judged} of them with only a judge's verdict, which leaves a flag open)" if judged else ""
        lines = [f"Possible kills and scoops with no person's verdict yet: {open_flags}{note}. First seen since "
                 f"{since} and already reviewed: {len(flagged) - open_flags}. Labels are triage; verdicts are "
                 "judgement."]
    if flagged is not None:
        kills = sum(item["open"] and item["label"] == "possible-kill" for item in flagged)
        scoops = sum(item["open"] and item["label"] == "possible-scoop" for item in flagged)
        lines.append(f"Open backlog: {kills} possible kills; {scoops} possible scoops (oldest first within each label).")
    coverage = section.get("coverage")
    if coverage:
        lines.append(f"Watch last saved a run on {_flat(coverage.get('updated')) or 'an unknown date'}.")
        for track, date in sorted(coverage.get("tracks_updated", {}).items()):
            lines.append(f"- Track {_flat(track)} last covered through {_flat(date)}.")
        if coverage.get("stale"):
            lines.append("The watch has checkpoints older than this brief's window; refresh the watch before treating it as current.")
        for gap in coverage.get("gaps", []):
            lines.append(f"- Incomplete coverage: {_flat(gap.get('track'))}, {_flat(gap.get('since'))} to "
                         f"{_flat(gap.get('until'))}; flags may be missing in this window.")
        lines += [f"- Coverage warning: {_flat(warning)}." for warning in coverage.get("warnings", [])]
    lines += [f"Verdicts recorded since {since}: {len(human_reviews)}" + (f" ({tally})." if tally else "."), ""]
    if judge_reviews:
        judge_counts: dict[str, int] = {}
        for item in judge_reviews:
            verdict = _flat(item["verdict"])
            judge_counts[verdict] = judge_counts.get(verdict, 0) + 1
        judge_tally = ", ".join(f"{v} {n}" for v, n in sorted(judge_counts.items()))
        lines += [f"Judge-only verdicts since {since}: {len(judge_reviews)} ({judge_tally}); awaiting a person's review.", ""]
    # Every verdict of the window is named once: in a row the flagged table shows, or here.
    in_table = {item["id"] for item in (flagged or [])[:LIST_CAP]}
    others = [item for item in reviewed if item["id"] not in in_table]
    if others:
        where = " on papers not in the flagged table below" if flagged else ""
        lines += [f"Verdicts recorded since {since}{where} ({len(others)}):", ""]
        lines += _bullets([f"- `{item['id']}`: {_flat(item['verdict'])} ({_by(item)}, {item['reviewed_on']})."
                           for item in others])
        lines.append("")
    lines += [
        f"Open actions from verdicts ({len(actions)}; once one is done, run "
        "`python tools/arxiv_watch/watch.py --action-done ID`):",
        "",
    ]
    lines += _bullets([f"- `{item['id']}` ({_by(item)}): {_flat(item['action'])}" for item in actions]) or [
        "- None."]
    blocked = section.get("blocked_actions") or []
    if blocked:
        lines += ["", "Actions awaiting clarification (resolve the target before acting):", ""]
        lines += _bullets([f"- `{item['id']}`: {_flat(item['action'])} "
                           f"Pending: {_flat(item['action_pending_clarification'])}" for item in blocked])
    proposals = section.get("proposed_actions") or []
    if proposals:
        lines += ["", "Proposed by judges; awaiting a person (these are not adopted tasks):", ""]
        lines += _bullets([f"- `{item['id']}` ({_by(item)}): {_flat(item['action'])}" for item in proposals])
    if flagged:
        lines += ["", "| arXiv | Label | First seen | Verdict | Title |", "|---|---|---|---|---|"]
        for item in flagged[:LIST_CAP]:
            if not item["open"]:
                verdict = _cell(item["verdict"])
            elif item["verdict"] is not None:  # a judge's verdict only
                verdict = f"**open** (judge: {_cell(item['verdict'])}): read it"
            else:
                verdict = "**open**: read it"
            first_seen = item["first_seen"] or "-"
            lines.append(f"| {_cell(item['id'])} | {_cell(item['label'])} | {_cell(first_seen)} | {verdict} | "
                         f"{_cell(item['title'])} |")
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
    items = []
    for item in flagged:
        claim = item.get("worst_claim") or {}
        worst = ""
        if claim:  # the quote verbatim, pipes and all
            quote, finding = _flat(claim.get("quote")), _flat(claim.get("finding"))
            worst = f" Worst claim ({claim.get('verdict')}): \"{quote}\". {finding}"
        items.append(f"- `{item['stem']}` **{item['overall']}** (reviewed {item.get('reviewed_on')}).{worst}")
    lines += _bullets(items, "`research/audits/REFEREE_QUEUE.md` and agent_brief.json")
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
    lines += _bullets([f"- {check}: `{problem['path']}`: {_flat(problem['message'])}" for check, problem in rows],
                      "agent_brief.json, or run the command above")
    return lines


def _render_inertia(section: dict[str, Any], since: str) -> list[str]:
    lines = [
        f"From `{COCKPIT}`, built {section.get('generated_on')} (rebuild: `python tools/cockpit/build_cockpit.py`). "
        f"A direction is flagged after {section.get('threshold')} handoff sections with no registry gain in it.",
        "",
    ]
    flags = section["flags"]
    lines += _bullets([
        f"- {_flat(flag['label'])} (`{flag['direction']}`): {flag['streak']} sections since the registry last gained "
        f"a record here ({flag['last_gain'] or 'never'})."
        for flag in flags
    ]) or ["- No direction is flagged."]
    lines += _bullets([f"- Warning: {_flat(warning)}" for warning in section.get("warnings") or []])
    return lines


def _render_duplicates(section: dict[str, Any], since: str) -> list[str]:
    unchecked, issues = section.get("unchecked") or [], section.get("index_issues") or []
    if not section["checked"] and not unchecked:
        return ["No negative was added in the window, so there is nothing to compare."]
    pairs = section["pairs"]
    lines = []
    if section["checked"]:
        lines.append(f"{len(pairs)} pairs at TF-IDF cosine {section['threshold']} or above involve one of the "
                     f"{section['checked']} negatives added in the window.")
    if unchecked:
        lines.append(f"Not compared ({len(unchecked)}): {_id_list(unchecked)}: added in the window, but the corpus "
                     "index has no document for them, so no pair with them was looked for.")
    if issues:
        lines.append("The corpus index could not read all of the negative registry, so a pair may be missing: "
                     + "; ".join(_flat(issue) for issue in issues) + ".")
    if pairs:
        lines[0] += " Read both records before merging them; a sweep sibling is a separate result and stays."
        lines += ["", "| Cosine | Record | Title | Record | Title |", "|---|---|---|---|---|"]
        for pair in pairs[:LIST_CAP]:
            lines.append(f"| {pair['score']:.2f} | `{_cell(pair['a'])}` | {_cell(_clip(pair['title_a']))} | "
                         f"`{_cell(pair['b'])}` | {_cell(_clip(pair['title_b']))} |")
        if len(pairs) > LIST_CAP:
            lines += ["", f"And {len(pairs) - LIST_CAP} more in agent_brief.json."]
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


def _zone_label(start: Any) -> str:
    """ "00:00 local time, UTC+11:00" from the window start's ISO time; without it, "00:00 local time"."""
    try:
        offset = dt.datetime.fromisoformat(start).utcoffset()
    except (TypeError, ValueError):
        offset = None
    if offset is None:
        return "00:00 local time"
    sign, offset = ("-", -offset) if offset < dt.timedelta(0) else ("+", offset)
    hours, minutes = divmod(int(offset.total_seconds()) // 60, 60)
    return f"00:00 local time, UTC{sign}{hours:02d}:{minutes:02d}"


def render(brief: dict[str, Any]) -> str:
    """The brief as markdown: one fixed heading per section, "Not available: <reason>" when a source is missing."""
    since = cutoff_day(brief["since_days"], brief["generated_on"]).isoformat()
    lines = [
        "# Agent brief",
        "",
        f"Generated {brief['generated_on']} by `python tools/brief/build_brief.py`; covers the {brief['since_days']} "
        f"days since {since} ({_zone_label(brief.get('window_start'))}). Do not edit by hand.",
        "Read it before choosing a direction. \"Not available\" means the source could not be read, not that "
        "there is nothing to report.",
        "",
    ]
    for key, heading, render_section in SECTION_HEADINGS:
        section = brief.get(key) or {"available": False, "reason": "missing from the brief"}
        lines += [f"## {heading}", ""]
        if not section.get("available"):
            lines.append(f"Not available: {_flat(section.get('reason') or 'no reason given')}")
        else:
            lines += render_section(section, since)
        lines.append("")
    return "\n".join(lines)


def _output_dir(root: Path, out: Path | None) -> Path:
    return Path(out) if out is not None else Path(root) / Path(OUTPUT_MD).parent


def _replace(path: Path, text: str) -> None:
    """Write text beside path, then rename it over path: a reader sees the old file or the new one, never part of one."""
    tmp = path.with_name(f".{path.name}.{os.getpid()}.tmp")  # per process, so two runs never share one
    try:
        tmp.write_text(text, encoding="utf-8")
        os.replace(tmp, path)
    finally:
        tmp.unlink(missing_ok=True)


def write(root: Path, brief: dict[str, Any], out: Path | None = None) -> tuple[Path, Path]:
    """Write agent_brief.json, then AGENT_BRIEF.md, into `out` (default: root/research/audits).

    Each file is replaced whole (written beside it, then renamed), so an agent reading it while
    the brief is rebuilt never sees it empty or cut short; the two are replaced one after the other.
    """
    directory = _output_dir(root, out)
    directory.mkdir(parents=True, exist_ok=True)
    md, js = directory / Path(OUTPUT_MD).name, directory / Path(OUTPUT_JSON).name
    text = render(brief)
    _replace(js, json.dumps(brief, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
    _replace(md, text)
    return md, js


def _out_problem(directory: Path) -> str | None:
    """Why the output directory cannot take the two files, found before the build; None when it looks writable."""
    directory = Path(directory).absolute()
    if directory.exists() and not directory.is_dir():
        return f"{directory} is not a directory"
    existing = directory
    while not existing.exists():  # the directory, or the nearest parent mkdir would create it in
        existing = existing.parent
    if not existing.is_dir():
        return f"{directory} cannot be created: {existing} is not a directory"
    if not os.access(existing, os.W_OK | os.X_OK):
        return f"{existing} is not writable"
    return None


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
                        help="Window: changes since this many days ago, from 00:00 local time.")
    parser.add_argument("--out", type=Path,
                        help="Directory for AGENT_BRIEF.md and agent_brief.json (default: ROOT/research/audits).")
    parser.add_argument("--json", action="store_true", help="Print the brief as JSON instead of a summary.")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    if not root.is_dir():
        parser.error(f"--root {root} is not a directory")
    if not (root / "qsearch.py").is_file():
        parser.error(f"--root {root} is not a Q-Search checkout: it has no qsearch.py")
    problem = _out_problem(_output_dir(root, args.out))  # before the build, not after it
    if problem is not None:
        parser.error(f"--out: {problem}" if args.out is not None else f"cannot write the brief: {problem}")
    brief = build(root, since_days=args.since_days)
    try:
        md, js = write(root, brief, args.out)
    except OSError as error:  # what the check above cannot see (a full disk, a read-only mount)
        print(f"{parser.prog}: error: cannot write the brief: {error}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(brief, indent=2, sort_keys=True, ensure_ascii=False))
        return 0
    print(f"wrote {md} and {js}")
    for key, heading, _ in SECTION_HEADINGS:
        print(f"{heading}: {_summary(key, brief[key])}")
    return 0


def _summary(key: str, section: dict[str, Any]) -> str:
    """A section's console summary: ok, or not available and why; the open arXiv flags are reported apart."""
    if not section.get("available"):
        return f"not available ({section.get('reason')})"
    if key == "arxiv" and section.get("flagged") is None:
        return f"open flags not available ({section.get('flagged_reason')}); verdicts and actions ok"
    if key == "arxiv":
        coverage = section.get("coverage") or {}
        if coverage.get("gaps") or coverage.get("stale") or coverage.get("warnings"):
            return "coverage incomplete or stale; inspect watch checkpoints and gaps"
    if key == "duplicates" and (section.get("unchecked") or section.get("index_issues")):
        return (f"incomplete ({len(section.get('unchecked') or [])} added records not compared; "
                f"{len(section.get('index_issues') or [])} index issues)")
    if key == "registry" and section.get("duplicate_ids"):
        return f"{len(section['duplicate_ids'])} duplicate ids; inspect the registry"
    return "ok"


if __name__ == "__main__":
    raise SystemExit(main())
