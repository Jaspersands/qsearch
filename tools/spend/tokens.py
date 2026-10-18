"""Per-day Codex token totals from local session logs, added to the spend ledger as token_day lines.

    python tools/spend/tokens.py              # import into research/audits/spend_ledger.jsonl
    python tools/spend/tokens.py --dry-run    # print the per-day totals, write nothing

Reads ~/.codex/sessions and ~/.codex/archived_sessions (*.jsonl, and *.jsonl.zst when the
zstandard module is installed). A session counts when its starting working directory is
this repo or a directory inside it (worktrees included). Codex writes an event_msg of type
token_count after each model call, carrying the session's cumulative usage. Usage per day is
the sum of the increases in that cumulative total; the first event of a session, and any
event where the total went down, count the event's own usage instead, so a forked session
does not re-count its parent.

Privacy: only the working directory (to match the repo), timestamps and the numeric usage
fields are read. Only per-day aggregates are written: no text, paths or session ids.

Gemini: the Gemini CLI keeps chats under ~/.gemini/tmp/, which does not exist on this
machine. The Antigravity app under ~/.gemini/antigravity has no named token fields; see
tools/spend/README.md. Gemini tokens are therefore not imported.
"""

from __future__ import annotations

import argparse
import io
import json
import os
import sys
from collections import defaultdict
from pathlib import Path
from typing import Iterable, Iterator

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.spend.common import LEDGER, git, replace_kinds, to_utc_iso  # noqa: E402

FIELDS = ("input_tokens", "cached_input_tokens", "output_tokens", "reasoning_output_tokens", "total_tokens")
DEFAULT_DIRS = (Path.home() / ".codex" / "sessions", Path.home() / ".codex" / "archived_sessions")
AGENT = "codex"


def project_dir(root: Path) -> str:
    """The main checkout that `root` belongs to (worktrees share it), else `root` itself."""
    common_dir = git(root, "rev-parse", "--path-format=absolute", "--git-common-dir")
    if common_dir and common_dir.strip():
        return str(Path(common_dir.strip()).parent)
    return str(root.resolve())


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


def _usage(info: dict, key: str) -> dict[str, int]:
    usage = info.get(key) or {}
    return {field: int(usage.get(field) or 0) for field in FIELDS}


def session_usage(lines: Iterable[bytes], project: str) -> tuple[bool | None, dict[str, dict[str, int]]]:
    """(in project?, per-day usage) for one session. None when the session has no session_meta line."""
    in_project: bool | None = None
    days: dict[str, dict[str, int]] = {}
    previous: dict[str, int] | None = None
    for raw in lines:
        if in_project is None and b'"session_meta"' in raw[:300]:
            row = json.loads(raw)
            if row.get("type") == "session_meta":
                in_project = _in_project(str((row.get("payload") or {}).get("cwd") or ""), project)
                if not in_project:
                    return False, {}
            continue
        if b'"token_count"' not in raw:
            continue
        row = json.loads(raw)
        payload = row.get("payload") or {}
        if row.get("type") != "event_msg" or payload.get("type") != "token_count" or not payload.get("info"):
            continue
        cumulative = _usage(payload["info"], "total_token_usage")
        if previous is None or cumulative["total_tokens"] < previous["total_tokens"]:
            step = _usage(payload["info"], "last_token_usage")
        else:
            step = {field: max(cumulative[field] - previous[field], 0) for field in FIELDS}
        previous = cumulative
        day = days.setdefault(to_utc_iso(row["timestamp"])[:10], dict.fromkeys(FIELDS, 0))
        for field in FIELDS:
            day[field] += step[field]
    return in_project, days


def import_codex(dirs: Iterable[Path], project: str) -> tuple[dict[str, dict[str, int]], dict[str, int]]:
    try:
        import zstandard  # noqa: F401

        has_zstd = True
    except ImportError:
        has_zstd = False
    totals: dict[str, dict[str, int]] = defaultdict(lambda: {"sessions": 0, **dict.fromkeys(FIELDS, 0)})
    stats = {"files": 0, "in_project": 0, "other_project": 0, "no_session_meta": 0, "skipped_zst": 0, "unreadable": 0}
    for base in dirs:
        if not base.exists():
            continue
        for path in sorted([*base.rglob("*.jsonl"), *base.rglob("*.jsonl.zst")]):
            stats["files"] += 1
            if path.name.endswith(".zst") and not has_zstd:
                stats["skipped_zst"] += 1
                continue
            try:
                in_project, days = session_usage(_lines(path), project)
            except (OSError, ValueError):
                stats["unreadable"] += 1
                continue
            if in_project is None:
                stats["no_session_meta"] += 1
                continue
            if not in_project:
                stats["other_project"] += 1
                continue
            stats["in_project"] += 1
            for date, usage in days.items():
                day = totals[date]
                day["sessions"] += 1
                for field in FIELDS:
                    day[field] += usage[field]
    return {date: totals[date] for date in sorted(totals)}, stats


def token_day_events(days: dict[str, dict[str, int]]) -> list[dict]:
    return [
        {
            "kind": "token_day",
            "timestamp": f"{date}T00:00:00+00:00",
            "date": date,
            "agent": AGENT,
            "sessions": usage["sessions"],
            **{field: usage[field] for field in FIELDS},
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
    args = parser.parse_args(argv)

    days, stats = import_codex(args.codex_dir or DEFAULT_DIRS, args.project_dir or project_dir(args.root))
    events = token_day_events(days)
    if not args.dry_run:
        replace_kinds(args.ledger or args.root / LEDGER, {"token_day"}, events)
    print(json.dumps({
        "sessions": stats,
        "days": len(events),
        "first_day": events[0]["date"] if events else None,
        "last_day": events[-1]["date"] if events else None,
        "total_tokens": sum(event["total_tokens"] for event in events),
        "written": not args.dry_run,
    }, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
