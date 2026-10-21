"""Reviewed verdicts for flagged arXiv papers, kept apart from the machine labels.

A label (possible-kill, possible-scoop, ...) comes from wording cues and is triage. A verdict is
judgement: a person, or a judge whose quote was checked, read the paper against the project and
decided what it means here. Verdicts live in research/audits/arxiv_verdicts.json, keyed by arXiv
id. That file is the source of truth: the watch copies each verdict onto its stored paper and
lists every verdict in the digest's Reviewed table.
"""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

from tools.corpus.docs import read_json

VERDICTS = ("kill", "scoop", "should-cite", "related-only", "false-alarm")
VERDICTS_FILE = "research/audits/arxiv_verdicts.json"


def load_verdicts(root: Path) -> dict:
    """The verdicts file as {"verdicts": {arxiv_id: entry}}; empty when the file is absent."""
    path = Path(root) / VERDICTS_FILE
    if not path.exists():
        return {"verdicts": {}}
    data = read_json(path)
    data.setdefault("verdicts", {})
    return data


def save_verdicts(root: Path, data: dict) -> None:
    path = Path(root) / VERDICTS_FILE
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def set_verdict(
    root: Path,
    arxiv_id: str,
    verdict: str,
    reason: str,
    by: str,
    action: str | None = None,
    today: str | None = None,
) -> dict:
    """Record (or replace) one paper's verdict and return the stored entry."""
    if verdict not in VERDICTS:
        raise ValueError(f"unknown verdict {verdict!r}; expected one of {', '.join(VERDICTS)}")
    if not arxiv_id:
        raise ValueError("an arXiv id is required")
    entry = {
        "verdict": verdict,
        "reason": reason,
        "action": action or None,
        "by": by,
        "reviewed_on": today or dt.date.today().isoformat(),
    }
    data = load_verdicts(root)
    data["verdicts"][arxiv_id] = entry
    save_verdicts(root, data)
    return entry
