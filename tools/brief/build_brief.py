"""Build the agent brief: what changed since the last sessions, and what to run before choosing.

Git is used read-only: only the exact argument lists `allowed_git_args` accepts are ever run.
Never imports core/ or theorems/.
"""

from __future__ import annotations

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
SHALLOW_ARGS = ("rev-parse", "--is-shallow-repository")
# The cutoff is the start of a UTC day. git reads a bare date (--before=2026-10-13) as that day
# at the current time of day, so the same command would pick different commits morning and
# evening; an explicit midnight UTC does not.
BEFORE_ARG = re.compile(r"--before=\d{4}-\d{2}-\d{2}T00:00:00Z")
SHOW_ARG = re.compile(r"[0-9a-f]{40}(?:[0-9a-f]{24})?:" + re.escape(REGISTRY))


def allowed_git_args(args: tuple[str, ...]) -> bool:
    """True only for the brief's own read-only git commands:

    ("log", "-1", "--before=YYYY-MM-DDT00:00:00Z", "--format=%H<US>%ct"),
    ("show", "<full sha>:" + REGISTRY) and ("rev-parse", "--is-shallow-repository").
    """
    args = tuple(args)
    if args == SHALLOW_ARGS:
        return True
    if len(args) == 4 and args[:2] == ("log", "-1") and args[3] == LOG_FORMAT:
        return bool(BEFORE_ARG.fullmatch(args[2]))
    if len(args) == 2 and args[0] == "show":
        return bool(SHOW_ARG.fullmatch(args[1]))
    return False


def git_runner(root: Path) -> GitRunner:
    """Run the brief's read-only git commands in root; return stdout, or None when git fails."""
    env = {**os.environ, "GIT_OPTIONAL_LOCKS": "0"}

    def run(*args: str) -> str | None:
        if not allowed_git_args(args):
            raise ValueError(f"the brief only runs its own read-only git commands, not {args!r}")
        try:
            result = subprocess.run(["git", "-C", str(root), *args], capture_output=True, env=env)
        except OSError:
            return None
        # A committed registry may hold bytes that are not UTF-8; replace them rather than fail.
        return result.stdout.decode("utf-8", errors="replace") if result.returncode == 0 else None

    return run


def _day(today: dt.date | str | None) -> dt.date:
    if today is None:
        return dt.datetime.now(dt.timezone.utc).date()
    return today if isinstance(today, dt.date) else dt.date.fromisoformat(today)


def cutoff_day(since_days: int, today: dt.date | str | None = None) -> dt.date:
    """The first day of the window: the brief covers changes from its start (00:00 UTC) on."""
    return _day(today) - dt.timedelta(days=since_days)


def since_commit(
    root: Path, since_days: int = 7, today: dt.date | str | None = None, git: GitRunner | None = None
) -> tuple[str, str] | None:
    """(sha, UTC commit date) of the newest commit before the cutoff day (00:00 UTC).

    None when git cannot answer, when the clone is shallow (its oldest commit is a cut, so the
    commit before the cutoff may be missing and an older one would be used silently), or when
    no commit is that old.
    """
    git = git or git_runner(root)
    if (git(*SHALLOW_ARGS) or "").strip() != "false":
        return None
    before = f"--before={cutoff_day(since_days, today).isoformat()}T00:00:00Z"
    sha, _, stamp = (git("log", "-1", before, LOG_FORMAT) or "").strip().partition(US)
    day = utc_day(stamp)
    return (sha, day) if sha and day else None


def _no_baseline_reason(git: GitRunner) -> str:
    answer = git(*SHALLOW_ARGS)
    if answer is None:
        return "no git history: not a git checkout, or git is not installed"
    if answer.strip() == "true":
        return "shallow clone: the registry at the cutoff is not in the history (git fetch --unshallow)"
    return "no commit before the cutoff: the history is younger than the window"


def _ids(data: Any) -> set[str]:
    """Record ids of a registry: a list of records, or an object with a "records" list."""
    if isinstance(data, dict) and isinstance(data.get("records"), list):
        data = data["records"]
    if not isinstance(data, list):
        raise ValueError(f"unexpected registry shape: {type(data).__name__}")
    return {record["id"] for record in data if isinstance(record, dict) and isinstance(record.get("id"), str)}


def _read_json(path: Path) -> Any:
    return json.loads(path.read_bytes().decode("utf-8", errors="replace"))


def _quarantined_ids(root: Path) -> set[str] | None:
    """Ids in the working copy's quarantine file; empty when it is absent, None when it cannot be read."""
    path = root / QUARANTINE
    if not path.is_file():
        return set()
    try:
        return _ids(_read_json(path))
    except (OSError, ValueError):
        return None


def registry_delta(
    root: Path, since_sha: str | None, git: GitRunner | None = None, since_date: str | None = None
) -> dict[str, Any]:
    """Negative-registry ids added and removed between the commit `since_sha` and the working copy.

    The working copy includes edits not committed yet. `quarantined` lists the removed ids
    that are now in the quarantine file (None when that file cannot be read). Unavailable
    (never "no change") when there is no baseline commit or the registry did not exist in it.
    """
    root = Path(root)
    git = git or git_runner(root)
    if not since_sha:
        return {"available": False, "reason": _no_baseline_reason(git)}
    committed = git("show", f"{since_sha}:{REGISTRY}")
    if committed is None:
        commit = f"commit {since_sha[:8]}" + (f" of {since_date}" if since_date else "")
        return {
            "available": False,
            "reason": f"{REGISTRY} did not exist at the cutoff ({commit})",
            "since_sha": since_sha,
            "since_date": since_date,
        }
    path = root / REGISTRY
    if not path.is_file():
        return {"available": False, "reason": f"{REGISTRY} is missing from the working copy"}
    baseline = _ids(json.loads(committed))
    current = _ids(_read_json(path))
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


def arxiv_section(root: Path, since_date: dt.date | str) -> dict[str, Any]:
    """Flagged arXiv papers, verdicts recorded since `since_date`, and the actions still open.

    flagged: possible kills and scoops without a verdict (open, however old), then those first
    seen on or after `since_date` that have one. reviewed: verdicts recorded on or after it.
    actions: every verdict whose action is not marked `action_done`. Verdicts come from the
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
    papers = read_json(state_path).get("papers", {}) if state_path.is_file() else {}
    verdicts = {
        arxiv_id: entry
        for arxiv_id, entry in verdicts_module.load_verdicts(root)["verdicts"].items()
        if isinstance(entry, dict)
    }

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

    reviewed = [
        {"id": arxiv_id, "verdict": entry.get("verdict"), "by": entry.get("by"), "reviewed_on": entry["reviewed_on"]}
        for arxiv_id, entry in sorted(verdicts.items())
        if isinstance(entry.get("reviewed_on"), str) and entry["reviewed_on"] >= since
    ]
    reviewed.sort(key=lambda item: item["reviewed_on"], reverse=True)
    actions = [
        {"id": arxiv_id, "action": str(entry["action"]).strip(), "by": entry.get("by")}
        for arxiv_id, entry in sorted(verdicts.items())
        if str(entry.get("action") or "").strip() and not entry.get("action_done")
    ]
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
        return {"available": False, "reason": f"the cockpit of {cockpit.get('generated_on')} has no inertia measure: {why}"}
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
    corpus.refresh()  # incremental: about 0.15 s when nothing changed; a first build takes minutes
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
