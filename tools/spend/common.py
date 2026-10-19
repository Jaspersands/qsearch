"""Shared helpers for the spend tools: timestamps, the JSONL ledger and registry counts.

The ledger is shared by several writers (timed.py appends, ledger.py and tokens.py rewrite
their own kinds), so every write holds an exclusive lock on the ledger file and re-checks
that the file it locked is still the one at the path. A rebuild that would drop a large share
of the existing lines of a kind is refused (see replace_kinds): it usually means a degraded
environment (shallow clone, missing logs), not less history.
"""

from __future__ import annotations

import datetime as dt
import fcntl
import json
import os
import subprocess
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Callable, Iterable, Iterator

LEDGER = Path("research/audits/spend_ledger.jsonl")
REGISTRY_DIR = Path("research/registry")
NEGATIVES = "negative_results.json"
# A rebuild may drop at most this share of the existing lines of a kind without --force.
MAX_DROP_SHARE = 0.2
# Kinds with fewer existing lines than this are not checked (registry_uncommitted is 0 or 1 line).
DROP_CHECK_MIN_LINES = 5


class RebuildRefused(RuntimeError):
    """A rebuild would drop too many existing ledger lines; nothing was written."""


def read_json(path: Path, retries: int = 3, delay_seconds: float = 0.025) -> Any:
    """Read JSON, retrying briefly on a partial read while an agent rewrites the file (tmp+rename).

    Mirrors core/research_registry.py:_read_json without importing core/.
    """
    for attempt in range(retries + 1):
        try:
            text = path.read_text(encoding="utf-8")
            if not text.strip():
                raise json.JSONDecodeError("empty file", text, 0)
            return json.loads(text)
        except json.JSONDecodeError:
            if attempt >= retries:
                raise
            time.sleep(delay_seconds * (attempt + 1))
    raise AssertionError("unreachable")


def git(root: Path, *args: str) -> str | None:
    """Run a read-only git command in `root`; None when `root` is not a checkout or git fails."""
    if not (root / ".git").exists():
        return None
    try:
        return subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, check=True).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def main_checkout(root: Path) -> Path | None:
    """The main checkout that `root` belongs to (a worktree shares it); None outside git."""
    common_dir = git(root, "rev-parse", "--path-format=absolute", "--git-common-dir")
    if not common_dir or not common_dir.strip():
        return None
    path = Path(common_dir.strip())
    return path.parent if path.name == ".git" else None


def repo_roots(root: Path) -> list[Path]:
    """`root` and, when it is a worktree, its main checkout: the directories whose files are repo files."""
    roots = [root.resolve()]
    main = main_checkout(root)
    if main is not None and main.resolve() not in roots:
        roots.append(main.resolve())
    return roots


def to_utc_iso(value: float | str | dt.datetime) -> str:
    """Normalise an epoch, ISO string or datetime to second-precision UTC ISO 8601."""
    if isinstance(value, (int, float)):
        moment = dt.datetime.fromtimestamp(value, tz=dt.timezone.utc)
    elif isinstance(value, dt.datetime):
        moment = value
    else:
        text = value.strip()
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        moment = dt.datetime.fromisoformat(text)
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=dt.timezone.utc)
    return moment.astimezone(dt.timezone.utc).replace(microsecond=0).isoformat()


def day_of(timestamp: str) -> str:
    """UTC calendar day of a normalised timestamp."""
    return timestamp[:10]


def _dump(event: dict) -> str:
    return json.dumps(event, sort_keys=True, ensure_ascii=False)


def _sort_key(event: dict) -> tuple[str, str, str]:
    return (str(event.get("timestamp", "")), str(event.get("kind", "")), _dump(event))


def _parse_lines(text: str) -> list[dict]:
    rows = []
    for line in text.splitlines():
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except ValueError:
            continue  # a torn line from an interrupted writer
        if isinstance(row, dict):
            rows.append(row)
    return rows


def read_ledger(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return _parse_lines(path.read_text(encoding="utf-8"))


@contextmanager
def _locked(path: Path) -> Iterator[Any]:
    """Open the ledger for append+read under an exclusive lock on the inode currently at `path`."""
    path.parent.mkdir(parents=True, exist_ok=True)
    while True:
        handle = open(path, "a+", encoding="utf-8")
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            same = os.fstat(handle.fileno()).st_ino == os.stat(path).st_ino
        except FileNotFoundError:
            same = False
        if same:
            break
        handle.close()  # another writer replaced the file while we waited; lock the new one
    try:
        yield handle
    finally:
        handle.close()


def append_event(path: Path, event: dict) -> None:
    with _locked(path) as handle:
        handle.write(_dump(event) + "\n")
        handle.flush()
        os.fsync(handle.fileno())


def _drop_problems(old: list[dict], new: list[dict], kinds: set[str], max_drop_share: float) -> list[str]:
    before = {kind: 0 for kind in kinds}
    after = dict(before)
    for row in old:
        if row.get("kind") in kinds:
            before[row["kind"]] += 1
    for row in new:
        if row.get("kind") in kinds:
            after[row["kind"]] += 1
    return [
        f"{kind}: {before[kind]:,} lines would become {after[kind]:,}"
        for kind in sorted(kinds)
        if before[kind] >= DROP_CHECK_MIN_LINES and before[kind] - after[kind] > max_drop_share * before[kind]
    ]


def replace_kinds(
    path: Path,
    kinds: Iterable[str],
    events: Iterable[dict],
    max_drop_share: float | None = None,
    transform: Callable[[dict], dict] | None = None,
) -> int:
    """Drop every line whose kind is in `kinds`, add `events`, keep everything else.

    With `max_drop_share`, raise RebuildRefused (and write nothing) when a kind in `kinds` with
    at least DROP_CHECK_MIN_LINES existing lines would lose more than that share of them.
    `transform` is applied to every kept line. Returns the number of kept lines. Writes a temp
    file and renames it while holding the lock.
    """
    kinds = set(kinds)
    events = list(events)
    with _locked(path) as handle:
        handle.seek(0)
        existing = _parse_lines(handle.read())
        if max_drop_share is not None:
            problems = _drop_problems(existing, events, kinds, max_drop_share)
            if problems:
                raise RebuildRefused(
                    f"the rebuild would drop more than {max_drop_share:.0%} of the existing lines of a kind ("
                    + "; ".join(problems) + "). That usually means missing data (a shallow clone, missing or "
                    "pruned logs, a missing module), not less history."
                )
        kept = [row for row in existing if row.get("kind") not in kinds]
        if transform is not None:
            kept = [transform(row) for row in kept]
        rows = sorted([*kept, *events], key=_sort_key)
        tmp = path.with_name(f".{path.name}.{os.getpid()}.tmp")
        tmp.write_text("".join(_dump(row) + "\n" for row in rows), encoding="utf-8")
        os.replace(tmp, path)
    return len(kept)


def count_records(data: Any) -> int:
    """A list counts its items; a dict counts the items of its top-level list values."""
    if isinstance(data, list):
        return len(data)
    if isinstance(data, dict):
        return sum(len(value) for value in data.values() if isinstance(value, list))
    return 0


def registry_counts(root: Path, retries: int = 3) -> dict[str, int | None]:
    """Record counts per research/registry/*.json file; None when a file cannot be parsed."""
    counts: dict[str, int | None] = {}
    for path in sorted((root / REGISTRY_DIR).glob("*.json")):
        try:
            counts[path.name] = count_records(read_json(path, retries=retries))
        except (OSError, ValueError):
            counts[path.name] = None
    return counts
