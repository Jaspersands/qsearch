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
import re
from pathlib import Path

from tools.corpus.docs import read_json

VERDICTS = ("kill", "scoop", "should-cite", "related-only", "false-alarm")
VERDICTS_FILE = "research/audits/arxiv_verdicts.json"

_ID_PREFIX = re.compile(r"^(?:https?://arxiv\.org/abs/|arxiv:)", re.I)
_ID = re.compile(r"^(?:\d{4}\.\d{4,5}|[a-z-]+(?:\.[A-Z]{2})?/\d{7})$")


def normalize_id(raw: str) -> str:
    """The bare arXiv id the watch stores papers under: "arXiv:2610.06753v2" or
    "https://arxiv.org/abs/2610.06753v2" -> "2610.06753". ValueError when it is not an arXiv id."""
    arxiv_id = re.sub(r"v\d+$", "", _ID_PREFIX.sub("", str(raw).strip()))
    if not _ID.match(arxiv_id):
        raise ValueError(f"not an arXiv id: {raw!r} (expected e.g. 2610.06753, arXiv:2610.06753v2 or quant-ph/0501044)")
    return arxiv_id


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
    """Record (or replace) one paper's verdict under its bare id (see normalize_id) and return the stored entry."""
    if verdict not in VERDICTS:
        raise ValueError(f"unknown verdict {verdict!r}; expected one of {', '.join(VERDICTS)}")
    arxiv_id = normalize_id(arxiv_id)
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
