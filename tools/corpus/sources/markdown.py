"""Chunk research notes and the agent handoff journals at `## ` headings."""

from __future__ import annotations

import re
from pathlib import Path

from tools.corpus.docs import Doc, slugify

MAX_WORDS = 400
JOURNALS = {"AGENT_HANDOFF.md", "MECHANICAL_FOLLOW_UP_PLAN.md"}

# First match wins, so the most decisive labels come first.
_STATUS_PATTERNS = [
    ("quarantined", re.compile(r"\bquarantin", re.I)),
    ("superseded", re.compile(r"\bsuperseded\b", re.I)),
    ("retracted", re.compile(r"\b(retracted|withdrawn)\b", re.I)),
    ("rejected", re.compile(r"\brejected\b", re.I)),
    ("review-pending", re.compile(r"\breview[ -]pending\b", re.I)),
    ("proved", re.compile(r"\bproved\b", re.I)),
    ("audited", re.compile(r"\baudit(ed)?\b", re.I)),
]


def note_status(lines: list[str]) -> str:
    head = " ".join(line for line in lines[:8] if not line.startswith("# "))
    for label, pattern in _STATUS_PATTERNS:
        if pattern.search(head):
            return label
    return "unlabelled"


def _sections(lines: list[str]) -> list[tuple[str, int, list[str]]]:
    """Return (heading, 1-based heading line, body lines); the preamble has heading ''."""
    sections: list[tuple[str, int, list[str]]] = [("", 1, [])]
    for number, line in enumerate(lines, start=1):
        if line.startswith("## "):
            sections.append((line[3:].strip(), number, []))
        else:
            sections[-1][2].append(line)
    return sections


def _split(body: list[str], first_line: int) -> list[tuple[int, str]]:
    """Group paragraphs into pieces of at most MAX_WORDS words; returns (line, text)."""
    paragraphs: list[tuple[int, list[str]]] = []
    for offset, line in enumerate(body, start=1):
        if not line.strip():
            if paragraphs and paragraphs[-1][1]:
                paragraphs.append((first_line + offset + 1, []))
            continue
        if not paragraphs:
            paragraphs.append((first_line + offset, []))
        paragraphs[-1][1].extend(line.split())
    pieces: list[tuple[int, list[str]]] = []
    for line, tokens in paragraphs:
        while tokens:
            if pieces and len(pieces[-1][1]) + len(tokens) <= MAX_WORDS:
                pieces[-1][1].extend(tokens)
                tokens = []
            elif len(tokens) <= MAX_WORDS:
                pieces.append((line, list(tokens)))
                tokens = []
            else:
                pieces.append((line, tokens[:MAX_WORDS]))
                tokens = tokens[MAX_WORDS:]
    return [(line, " ".join(tokens)) for line, tokens in pieces if tokens]


def parse(root: Path, rel: str) -> list[Doc]:
    path = root / rel
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    stem = path.stem
    title = next((line[2:].strip() for line in lines if line.startswith("# ")), stem)
    journal = path.name in JOURNALS
    status = note_status(lines)
    sections = _sections(lines)
    docs: list[Doc] = []

    if journal:
        # Number repeated headings from the bottom (oldest) so ids survive new sections on top.
        counts: dict[str, int] = {}
        suffixes: dict[int, str] = {}
        for index in range(len(sections) - 1, 0, -1):
            slug = slugify(sections[index][0]) or "section"
            counts[slug] = counts.get(slug, 0) + 1
            suffixes[index] = slug if counts[slug] == 1 else f"{slug}-{counts[slug]}"
        for index, (heading, line, body) in enumerate(sections):
            if index == 0:
                continue
            base = f"handoff:{stem}:{suffixes[index]}"
            for part, (part_line, text) in enumerate(_split(body, line)):
                doc_id = base if part == 0 else f"{base}~{part + 1}"
                meta = {"rank": index - 1, "file": path.name, "status": "journal"}
                docs.append(Doc(doc_id, "handoff", rel, line if part == 0 else part_line, heading, text, meta))
        return docs

    used: dict[str, int] = {}
    for heading, line, body in sections:
        slug = slugify(heading)
        used[slug] = used.get(slug, 0) + 1
        anchor = slug if used[slug] == 1 else f"{slug}-{used[slug]}"
        chunk_title = title if not heading else f"{title} › {heading}"
        if not heading:
            body = [b for b in body if not b.startswith("# ")]
        for part, (part_line, text) in enumerate(_split(body, line)):
            if len(text.split()) < 3:
                continue
            piece = anchor if part == 0 else f"{anchor}-{part + 1}"
            meta = {"status": status, "note": stem, "heading": heading}
            docs.append(Doc(f"note:{stem}#{piece}", "note", rel, line if part == 0 else part_line, chunk_title, text, meta))
    return docs
