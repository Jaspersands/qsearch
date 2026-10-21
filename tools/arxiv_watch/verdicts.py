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
JUDGE_PREFIX = "judge:"

_ID_PREFIX = re.compile(r"^(?:https?://arxiv\.org/abs/|arxiv:)", re.I)
_ID = re.compile(r"^(?:\d{4}\.\d{4,5}|[a-z-]+(?:\.[A-Z]{2})?/\d{7})$")


def normalize_id(raw: str) -> str:
    """The bare arXiv id the watch stores papers under: "arXiv:2610.06753v2" or
    "https://arxiv.org/abs/2610.06753v2" -> "2610.06753". ValueError when it is not an arXiv id."""
    arxiv_id = re.sub(r"v\d+$", "", _ID_PREFIX.sub("", str(raw).strip()))
    if not _ID.match(arxiv_id):
        raise ValueError(f"not an arXiv id: {raw!r} (expected e.g. 2610.06753, arXiv:2610.06753v2 or quant-ph/0501044)")
    return arxiv_id


def by_judge(entry) -> bool:
    """A stored verdict a judge may replace: one whose `by` names a judge. An entry without `by`
    (written by hand) counts as a human's."""
    return isinstance(entry, dict) and str(entry.get("by") or "").startswith(JUDGE_PREFIX)


def load_verdicts(root: Path) -> dict:
    """The verdicts file as {"verdicts": {arxiv_id: entry}}; empty when the file is absent.

    Keys are read as arXiv ids and returned bare (see normalize_id), so an entry written by hand
    under "arXiv:2610.06753v1" is the verdict for stored paper 2610.06753. When two keys name one
    paper, a person's entry outranks a judge's. ValueError, naming the file, when it is not JSON,
    is not {"verdicts": {...}}, an entry is not an object with a known verdict, a key is not an
    arXiv id, or two entries of the same kind name one paper.
    """
    path = Path(root) / VERDICTS_FILE
    if not path.exists():
        return {"verdicts": {}}
    try:
        data = read_json(path)
    except ValueError as error:
        raise ValueError(f"{VERDICTS_FILE}: not valid JSON ({error})") from error
    if not isinstance(data, dict) or not isinstance(data.setdefault("verdicts", {}), dict):
        raise ValueError(f'{VERDICTS_FILE}: expected an object {{"verdicts": {{arXiv id: entry, ...}}}}')
    verdicts: dict[str, dict] = {}
    keys: dict[str, str] = {}
    for key, entry in data["verdicts"].items():
        if not isinstance(entry, dict) or entry.get("verdict") not in VERDICTS:
            raise ValueError(f"{VERDICTS_FILE}: entry {key!r} must be an object whose verdict is one of {', '.join(VERDICTS)}")
        try:
            arxiv_id = normalize_id(key)
        except ValueError as error:
            raise ValueError(f"{VERDICTS_FILE}: {error}") from None
        if arxiv_id in verdicts:
            if by_judge(verdicts[arxiv_id]) == by_judge(entry):
                raise ValueError(f"{VERDICTS_FILE}: {keys[arxiv_id]!r} and {key!r} are both verdicts for {arxiv_id}; keep one")
            if by_judge(entry):
                continue  # a person's verdict outranks a judge's
        verdicts[arxiv_id], keys[arxiv_id] = entry, key
    data["verdicts"] = verdicts
    return data


def save_verdicts(root: Path, data: dict) -> None:
    path = Path(root) / VERDICTS_FILE
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def verdict_entry(verdict: str, reason: str, by: str, action: str | None = None, today: str | None = None) -> dict:
    """One verdicts-file entry; ValueError on an unknown verdict."""
    if verdict not in VERDICTS:
        raise ValueError(f"unknown verdict {verdict!r}; expected one of {', '.join(VERDICTS)}")
    return {"verdict": verdict, "reason": reason, "action": action or None, "by": by, "reviewed_on": today or dt.date.today().isoformat()}


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
    entry = verdict_entry(verdict, reason, by, action=action, today=today)
    arxiv_id = normalize_id(arxiv_id)
    data = load_verdicts(root)
    data["verdicts"][arxiv_id] = entry
    save_verdicts(root, data)
    return entry
