"""Shared helpers for the spend tools: timestamps, the JSONL ledger and registry counts.

The ledger is shared by several writers (timed.py appends, ledger.py and tokens.py rewrite
their own kinds), so every write holds an exclusive lock on the ledger file and re-checks
that the file it locked is still the one at the path.
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
from typing import Any, Iterable, Iterator

LEDGER = Path("research/audits/spend_ledger.jsonl")
REGISTRY_DIR = Path("research/registry")
NEGATIVES = "negative_results.json"


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


def replace_kinds(path: Path, kinds: Iterable[str], events: Iterable[dict]) -> int:
    """Drop every line whose kind is in `kinds`, add `events`, keep everything else.

    Returns the number of kept lines. Writes a temp file and renames it while holding the lock.
    """
    kinds = set(kinds)
    with _locked(path) as handle:
        handle.seek(0)
        kept = [row for row in _parse_lines(handle.read()) if row.get("kind") not in kinds]
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
