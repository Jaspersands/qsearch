"""Per-day Codex token totals from local session logs, added to the spend ledger as token_day lines.

    python tools/spend/tokens.py              # import into research/audits/spend_ledger.jsonl
    python tools/spend/tokens.py --dry-run    # print the per-day totals, write nothing

Reads ~/.codex/sessions and ~/.codex/archived_sessions (*.jsonl and *.jsonl.zst; both
directories hold .zst files, which need the zstandard module). A session counts when its
starting working directory is this repo or a directory inside it (worktrees included). Codex
writes an event_msg of type token_count after each model call, carrying the session's
cumulative usage. Usage per day is the sum of the increases in that cumulative total; the
first counted event of a session, and any event where the total went down, count the event's
own usage instead.

Forks: a forked session's log starts with a copy of its parent's token_count history,
re-stamped at fork time. That replayed prefix is skipped, so the parent's usage is counted
once, on the parent's days, and the fork counts only what came after it. The prefix is the
leading run of events whose cumulative totals also occur in the parent's log (the session
named by session_meta.forked_from_id), or, when that log is not here, in an in-project
session that started earlier.

Bad records are skipped and counted (bad_lines), never fatal: a torn line from a session that
is still being written, a token_count without a timestamp, a non-numeric count.

The rewrite refuses (exit 3, nothing written) when .jsonl.zst logs had to be skipped because
zstandard is missing, or when it would drop more than 20% of the existing token_day lines
(pruned or missing logs). --force overrides; --dry-run never writes.

Privacy: only the working directory (to match the repo), session ids (to match a fork to its
parent, in memory only), timestamps and the numeric usage fields are read. Only per-day
aggregates are written: no text, paths or session ids.

Gemini: the Gemini CLI keeps chats under ~/.gemini/tmp/, which does not exist on this
machine. The Antigravity app under ~/.gemini/antigravity has no named token fields; see
tools/spend/README.md. Gemini tokens are therefore not imported.
"""

from __future__ import annotations

import argparse
import datetime as dt
import io
import json
import os
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Iterator

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.spend.common import LEDGER, MAX_DROP_SHARE, RebuildRefused, main_checkout, replace_kinds, to_utc_iso  # noqa: E402

FIELDS = ("input_tokens", "cached_input_tokens", "output_tokens", "reasoning_output_tokens", "total_tokens")
DEFAULT_DIRS = (Path.home() / ".codex" / "sessions", Path.home() / ".codex" / "archived_sessions")
AGENT = "codex"
REFUSED = 3

Usage = dict  # {field: int} for every field in FIELDS


def project_dir(root: Path) -> str:
    """The main checkout that `root` belongs to (worktrees share it), else `root` itself."""
    main = main_checkout(root)
    return str(main) if main is not None else str(root.resolve())


def zstd_available() -> bool:
    try:
        import zstandard  # noqa: F401
    except ImportError:
        return False
    return True


def _in_project(cwd: str, project: str) -> bool:
    cwd, project = os.path.normpath(cwd), os.path.normpath(project)
    return cwd == project or cwd.startswith(project + os.sep)


def _lines(path: Path) -> Iterator[bytes]:
    if path.name.endswith(".zst"):
        import zstandard  # optional; the caller skips .zst files when it is missing

        with path.open("rb") as handle:
            yield from io.BufferedReader(zstandard.ZstdDecompressor().stream_reader(handle))
    else:
        with path.open("rb") as handle:
            yield from handle


class _Reader:
    """Iterate a log's lines; a read error part-way (a truncated archive) ends the iteration and is kept."""

    def __init__(self, path: Path):
        self.path = path
        self.error: Exception | None = None

    def __iter__(self) -> Iterator[bytes]:
        try:
            yield from _lines(self.path)
        except Exception as exc:  # noqa: BLE001 - OSError, zstandard.ZstdError, EOFError, ...
            self.error = exc


def _usage(info: dict, key: str) -> Usage:
    usage = info.get(key) or {}
    return {name: int(usage.get(name) or 0) for name in FIELDS}


def _key(usage: Usage) -> tuple[int, ...]:
    return tuple(usage[name] for name in FIELDS)


def _json(raw: bytes) -> dict | None:
    try:
        row = json.loads(raw)
    except ValueError:
        return None
    return row if isinstance(row, dict) else None


def _moment(stamp) -> dt.datetime | None:
    try:
        text = str(stamp).strip()
        moment = dt.datetime.fromisoformat(text[:-1] + "+00:00" if text.endswith("Z") else text)
    except (TypeError, ValueError):
        return None
    return moment if moment.tzinfo else moment.replace(tzinfo=dt.timezone.utc)


@dataclass
class Session:
    in_project: bool | None = None  # None: no session_meta line
    session_id: str | None = None
    parent: str | None = None
    start: dt.datetime | None = None
    events: list[tuple[str, Usage, Usage]] = field(default_factory=list)  # (UTC day, cumulative, last)
    bad_lines: int = 0


def read_session(lines: Iterable[bytes], project: str) -> Session:
    """One session log. Stops reading at session_meta when the session is not in the project."""
    session = Session()
    for raw in lines:
        if session.in_project is None and b'"session_meta"' in raw[:300]:
            row = _json(raw)
            if row is None:
                session.bad_lines += 1
                continue
            payload = row.get("payload")
            if row.get("type") == "session_meta" and isinstance(payload, dict):
                session.in_project = _in_project(str(payload.get("cwd") or ""), project)
                if not session.in_project:
                    return session
                session.session_id = None if payload.get("id") is None else str(payload["id"])
                session.parent = None if payload.get("forked_from_id") is None else str(payload["forked_from_id"])
                session.start = _moment(row.get("timestamp"))
            continue
        if b'"token_count"' not in raw:
            continue
        row = _json(raw)
        if row is None:
            session.bad_lines += 1
            continue
        payload = row.get("payload")
        if row.get("type") != "event_msg" or not isinstance(payload, dict) or payload.get("type") != "token_count":
            continue
        info = payload.get("info")
        if not info:
            continue
        try:
            day = to_utc_iso(row["timestamp"])[:10]
            cumulative, last = _usage(info, "total_token_usage"), _usage(info, "last_token_usage")
        except (KeyError, TypeError, ValueError, AttributeError, OverflowError):
            session.bad_lines += 1
            continue
        session.events.append((day, cumulative, last))
    return session


def _replayed_prefixes(sessions: list[Session]) -> tuple[list[int], int]:
    """Per session, how many leading events replay another session's history; and how many forks lack their parent."""
    owners: dict[tuple[int, ...], set[int]] = defaultdict(set)
    for index, session in enumerate(sessions):
        for _, cumulative, _ in session.events:
            if cumulative["total_tokens"]:
                owners[_key(cumulative)].add(index)
    by_id: dict[str, set[int]] = defaultdict(set)
    for index, session in enumerate(sessions):
        if session.session_id is not None:
            by_id[session.session_id].add(index)
    prefixes, parent_missing = [], 0
    for index, session in enumerate(sessions):
        candidates = by_id.get(session.parent, set()) - {index} if session.parent else set()
        if session.parent and not candidates:
            parent_missing += 1
        if not candidates:
            candidates = {
                other for other, earlier in enumerate(sessions)
                if other != index and earlier.start and session.start and earlier.start < session.start
            }
        length = 0
        while length < len(session.events) and owners.get(_key(session.events[length][1]), set()) & candidates:
            length += 1
        prefixes.append(length)
    return prefixes, parent_missing


def session_days(events: list[tuple[str, Usage, Usage]], skip: int = 0) -> dict[str, Usage]:
    """Per-day usage of one session, not counting its first `skip` (replayed) events."""
    days: dict[str, Usage] = {}
    previous = events[skip - 1][1] if skip else None
    for day, cumulative, last in events[skip:]:
        if previous is None or cumulative["total_tokens"] < previous["total_tokens"]:
            step = last
        else:
            step = {name: max(cumulative[name] - previous[name], 0) for name in FIELDS}
        previous = cumulative
        usage = days.setdefault(day, dict.fromkeys(FIELDS, 0))
        for name in FIELDS:
            usage[name] += step[name]
    return days


def import_codex(dirs: Iterable[Path], project: str) -> tuple[dict[str, dict[str, int]], dict[str, int]]:
    has_zstd = zstd_available()
    stats = {"files": 0, "in_project": 0, "other_project": 0, "no_session_meta": 0, "skipped_zst": 0, "unreadable": 0,
             "truncated": 0, "bad_lines": 0, "replaying_sessions": 0, "replayed_events": 0, "replayed_tokens": 0,
             "fork_parent_missing": 0}
    sessions: list[Session] = []
    for base in dirs:
        if not base.exists():
            continue
        for path in sorted([*base.rglob("*.jsonl"), *base.rglob("*.jsonl.zst")]):
            stats["files"] += 1
            if path.name.endswith(".zst") and not has_zstd:
                stats["skipped_zst"] += 1
                continue
            reader = _Reader(path)
            session = read_session(reader, project)
            stats["bad_lines"] += session.bad_lines
            if reader.error is not None:
                if session.in_project is None and not session.events:
                    stats["unreadable"] += 1
                    continue
                stats["truncated"] += 1
            if session.in_project is None:
                stats["no_session_meta"] += 1
            elif not session.in_project:
                stats["other_project"] += 1
            else:
                stats["in_project"] += 1
                sessions.append(session)

    prefixes, stats["fork_parent_missing"] = _replayed_prefixes(sessions)
    totals: dict[str, dict[str, int]] = defaultdict(lambda: {"sessions": 0, **dict.fromkeys(FIELDS, 0)})
    for session, skip in zip(sessions, prefixes):
        if skip:
            stats["replaying_sessions"] += 1
            stats["replayed_events"] += skip
            stats["replayed_tokens"] += session.events[skip - 1][1]["total_tokens"]
        for date, usage in session_days(session.events, skip).items():
            day = totals[date]
            day["sessions"] += 1
            for name in FIELDS:
                day[name] += usage[name]
    return {date: totals[date] for date in sorted(totals)}, stats


def token_day_events(days: dict[str, dict[str, int]]) -> list[dict]:
    return [
        {
            "kind": "token_day",
            "timestamp": f"{date}T00:00:00+00:00",
            "date": date,
            "agent": AGENT,
            "sessions": usage["sessions"],
            **{name: usage[name] for name in FIELDS},
            "source": "codex session logs",
        }
        for date, usage in sorted(days.items())
    ]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--ledger", type=Path, help=f"Ledger path (default: ROOT/{LEDGER}).")
    parser.add_argument("--codex-dir", type=Path, action="append",
                        help="Codex session directory; repeatable (default: ~/.codex/sessions and archived_sessions).")
    parser.add_argument("--project-dir", help="Count sessions started in this directory (default: the repo's main checkout).")
    parser.add_argument("--dry-run", action="store_true", help="Print per-day totals; do not touch the ledger.")
    parser.add_argument("--force", action="store_true",
                        help="Write even when .zst logs were skipped or many existing token_day lines would be dropped.")
    args = parser.parse_args(argv)

    days, stats = import_codex(args.codex_dir or DEFAULT_DIRS, args.project_dir or project_dir(args.root))
    events = token_day_events(days)
    ledger = args.ledger or args.root / LEDGER
    written = False
    if stats["skipped_zst"] and not args.force:
        message = (f"{stats['skipped_zst']} .jsonl.zst session logs were skipped because the zstandard module is "
                   "not installed (pip install zstandard)")
        if not args.dry_run:
            print(f"tokens.py: refusing to rewrite the token_day lines of {ledger}: {message}. "
                  "Use --force to write anyway.", file=sys.stderr)
            return REFUSED
        print(f"tokens.py: warning: {message}; the totals below leave them out.", file=sys.stderr)
    if not args.dry_run:
        try:
            replace_kinds(ledger, {"token_day"}, events, max_drop_share=None if args.force else MAX_DROP_SHARE)
        except RebuildRefused as refused:
            print(f"tokens.py: refusing to rewrite {ledger}: {refused} Use --force to write anyway.", file=sys.stderr)
            return REFUSED
        written = True
    print(json.dumps({
        "sessions": stats,
        "days": len(events),
        "first_day": events[0]["date"] if events else None,
        "last_day": events[-1]["date"] if events else None,
        "total_tokens": sum(event["total_tokens"] for event in events),
        "written": written,
    }, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
