"""The classical baselines a quantum proposal should be compared against.

    from tools.corpus.baselines import load_catalog, validate_catalog
    problems = validate_catalog(load_catalog())

The catalog (`baselines.json`, next to this module) lists named classical algorithms: the
problem each solves, three to six lowercase mechanism keywords, references (arXiv ids and
research notes by stem) and, when the repository has one, a command that runs it.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

CATALOG = Path(__file__).with_name("baselines.json")
FIELDS = ("id", "name", "aliases", "problem", "mechanisms", "summary", "references", "runnable")
_TEXT_FIELDS = ("id", "name", "problem", "summary")
_LIST_FIELDS = ("aliases", "mechanisms", "references")
_ARXIV = re.compile(r"\d{4}\.\d{4,5}")
_STEM = re.compile(r"[A-Z0-9_]+")


def load_catalog(path: Path = CATALOG) -> list[dict]:
    return json.loads(Path(path).read_text(encoding="utf-8"))["baselines"]


def _reference_ok(ref: object) -> bool:
    """{"arxiv": "2609.40036"} or {"note": "PRIME_CHARACTER_OPI"} (a research/<STEM>.md file)."""
    if not isinstance(ref, dict) or len(ref) != 1:
        return False
    (key, value), = ref.items()
    pattern = {"arxiv": _ARXIV, "note": _STEM}.get(key)
    return pattern is not None and isinstance(value, str) and pattern.fullmatch(value) is not None


def validate_catalog(entries: list[dict]) -> list[str]:
    """Problems with catalog entries, one line each; an empty list means the catalog is usable."""
    problems: list[str] = []
    seen: set[str] = set()
    for index, entry in enumerate(entries):
        label = str(entry.get("id") or f"entry {index + 1}")
        missing = [name for name in FIELDS if name not in entry]
        if missing:
            problems.append(f"{label}: missing field {', '.join(missing)}")
        for name in _TEXT_FIELDS:
            if name in entry and not (isinstance(entry[name], str) and entry[name].strip()):
                problems.append(f"{label}: {name} must be a non-empty string")
        for name in _LIST_FIELDS:
            if name in entry and not isinstance(entry[name], list):
                problems.append(f"{label}: {name} must be a list")
        if label in seen:
            problems.append(f"{label}: duplicate id")
        seen.add(label)
        mechanisms = entry.get("mechanisms")
        if isinstance(mechanisms, list) and not (
            3 <= len(mechanisms) <= 6 and all(isinstance(m, str) and m.strip() for m in mechanisms)
        ):
            problems.append(f"{label}: mechanisms must be 3 to 6 keywords, found {len(mechanisms)}")
        if isinstance(entry.get("aliases"), list) and not all(isinstance(a, str) and a.strip() for a in entry["aliases"]):
            problems.append(f"{label}: aliases must be non-empty strings")
        for ref in entry.get("references") if isinstance(entry.get("references"), list) else ():
            if not _reference_ok(ref):
                problems.append(f"{label}: malformed reference {json.dumps(ref)}")
        runnable = entry.get("runnable")
        if runnable is not None and not (
            isinstance(runnable, dict)
            and isinstance(runnable.get("command"), str)
            and set(runnable) <= {"command", "entry"}
        ):
            problems.append(f"{label}: runnable must be null or {{command, entry?}}")
    return problems
