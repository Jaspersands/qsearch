"""The uniform document record every source parser produces, plus small text helpers."""

from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Doc:
    doc_id: str
    kind: str
    path: str  # repo-relative source file
    line: int  # 1-based line of the record or heading in `path`, 0 when unknown
    title: str
    text: str
    meta: dict[str, Any] = field(default_factory=dict)


def read_json(path: Path, retries: int = 3, delay_seconds: float = 0.025) -> Any:
    """Read JSON, retrying briefly on a partial read while another agent rewrites the file.

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


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def flatten(value: Any, limit: int = 4000) -> str:
    """Join every string found in a JSON value, depth first, up to `limit` characters."""
    parts: list[str] = []
    size = 0

    def walk(item: Any) -> None:
        nonlocal size
        if size >= limit:
            return
        if isinstance(item, str):
            parts.append(item)
            size += len(item) + 1
        elif isinstance(item, dict):
            for key in sorted(item):
                walk(item[key])
        elif isinstance(item, (list, tuple)):
            for element in item:
                walk(element)

    walk(value)
    return " ".join(parts)[:limit]


def words(identifier: str) -> str:
    """Turn an id or snake_case name into words: NEG-DCP-X_Y -> 'neg dcp x y'."""
    return re.sub(r"[-_]+", " ", identifier).lower().strip()


def unique_ids(docs: list[Doc]) -> list[Doc]:
    """Suffix repeated doc_ids within one file with -2, -3, ... in order.

    A suffix never reuses an id that another document of the file already has, so a heading
    "Results 2" and a second "Results" heading cannot both end up as `results-2`.
    """
    taken = {doc.doc_id for doc in docs}
    seen: set[str] = set()
    result = []
    for doc in docs:
        if doc.doc_id in seen:
            count = 2
            while f"{doc.doc_id}-{count}" in taken:
                count += 1
            new_id = f"{doc.doc_id}-{count}"
            taken.add(new_id)
            doc = Doc(new_id, doc.kind, doc.path, doc.line, doc.title, doc.text, doc.meta)
        seen.add(doc.doc_id)
        result.append(doc)
    return result
