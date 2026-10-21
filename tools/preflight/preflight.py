"""Check a Q-Search checkout for the failures that have blocked a merge.

Research JSON files must parse: an invalid hypothesis contract broke the merge of 2026-10-19.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

JSON_DIRS = ("research/hypotheses", "research/registry", "research/audits", "research/classical_baselines")


@dataclass(frozen=True)
class Problem:
    check: str
    path: str  # relative to the checked root, posix
    message: str


def check_json(root: Path) -> list[Problem]:
    """Every .json file under JSON_DIRS that does not parse, with the parser's own message."""
    root = Path(root).resolve()
    problems = []
    for directory in JSON_DIRS:
        for path in sorted((root / directory).rglob("*.json")):
            if not path.is_file():
                continue
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError, OSError) as error:
                problems.append(Problem("json", path.relative_to(root).as_posix(), str(error)))
    return problems
