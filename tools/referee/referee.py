"""Referee review-pending research notes with an independent judge.

    python tools/referee/referee.py select [--prefix PRIME] [--limit 30] [--json]
    python tools/referee/referee.py export --out-dir DIR [--limit 30] [--note STEM ...]
    python tools/referee/referee.py import DIR/out/*.jsonl --judge NAME
    python tools/referee/referee.py render
    python tools/referee/referee.py status [--json]

A judge (an in-session subagent) reads INSTRUCTIONS.md and one batch of note packets, and
writes one JSONL row per note: up to six claims, each quoted verbatim from the note, with a
verdict, the step at fault and what is missing. Import checks every quote against the note
text and records the note's content hash, so a review goes stale when the note changes.

Outputs: research/audits/reviews/reviews.json, reviews/<STEM>.md and REFEREE_QUEUE.md.
The referee never edits research/*.md.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.corpus.docs import read_json  # noqa: E402
from tools.corpus.sources.markdown import JOURNALS, note_status  # noqa: E402
from tools.referee.extract import DATE, _status_block  # noqa: E402

REVIEWS = "research/audits/reviews/reviews.json"


def load_reviews(root: Path) -> dict:
    path = root / REVIEWS
    return read_json(path) if path.exists() else {"notes": {}}


def note_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _note_date(lines: list[str]) -> str | None:
    match = DATE.search(" ".join(_status_block(lines)))
    return match.group(0) if match else None


def select_notes(
    root: Path,
    prefixes: tuple[str, ...] = (),
    limit: int | None = 30,
    exclude_reviewed: bool = True,
    reviews: dict | None = None,
    statuses: tuple[str, ...] = ("review-pending",),
) -> list[Path]:
    """Notes with one of `statuses`, newest status-block date first, then newest mtime."""
    notes = (reviews if reviews is not None else load_reviews(root)).get("notes", {})
    ranked = []
    for path in sorted((root / "research").glob("*.md")):
        if path.name in JOURNALS or (prefixes and not path.stem.startswith(tuple(prefixes))):
            continue
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        if note_status(lines) not in statuses:
            continue
        review = notes.get(path.stem)
        if exclude_reviewed and review and review.get("content_sha") == note_sha(path):
            continue
        ranked.append(((_note_date(lines) or "0000", path.stat().st_mtime), path))
    ranked.sort(key=lambda item: item[0], reverse=True)
    paths = [path for _, path in ranked]
    return paths[:limit] if limit else paths
