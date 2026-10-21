"""Build the agent brief: what changed since the last sessions, and what to run before choosing.

Git is used read-only: only the exact argument lists `allowed_git_args` accepts are ever run.
Never imports core/ or theorems/.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.cockpit.build_cockpit import US, utc_day  # noqa: E402

REGISTRY = "research/registry/negative_results.json"
QUARANTINE = "research/registry/quarantined_campaign_negatives.json"


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
