"""Find the corpus source files under a Q-Search checkout and parse each into documents."""

from __future__ import annotations

from pathlib import Path
from typing import Callable

from tools.corpus.docs import Doc
from tools.corpus.sources import literature, markdown, registry, theorems

Parser = Callable[[Path, str], list[Doc]]


def _parser_for(rel: str) -> Parser | None:
    parts = rel.split("/")
    name = parts[-1]
    if parts[:2] == ["research", "registry"] and name in registry.PARSERS:
        return registry.parse
    if len(parts) == 2 and parts[0] == "research" and name.endswith(".md"):
        return markdown.parse
    if len(parts) == 2 and parts[0] == "theorems" and name.endswith(".py") and name != "__init__.py":
        return theorems.parse
    if rel == "research/literature_records.json":
        return literature.parse_records
    if parts[:2] == ["research", "literature_audits"] and name.endswith(".json"):
        return literature.parse_audit
    if parts[:2] == ["research", "hypotheses"] and name.endswith(".json"):
        return literature.parse_hypothesis
    return None


GLOBS = (
    "research/registry/*.json",
    "research/*.md",
    "theorems/*.py",
    "research/literature_records.json",
    "research/literature_audits/*.json",
    "research/hypotheses/*.json",
)


def discover(root: Path) -> list[str]:
    """Repo-relative paths of every file the corpus indexes, sorted."""
    found = set()
    for pattern in GLOBS:
        for path in root.glob(pattern):
            rel = path.relative_to(root).as_posix()
            if path.is_file() and _parser_for(rel) is not None:
                found.add(rel)
    return sorted(found)


_FALLBACK_KIND = {"hypotheses": "hypothesis", "literature_audits": "literature", "registry": "registry"}


def parse_file(root: Path, rel: str) -> list[Doc]:
    """Parse one source file; a file that cannot be parsed becomes one raw-text document."""
    parser = _parser_for(rel)
    if parser is None:
        return []
    try:
        return parser(root, rel)
    except (ValueError, UnicodeDecodeError) as error:
        path = root / rel
        parts = rel.split("/")
        kind = _FALLBACK_KIND.get(parts[1] if len(parts) > 2 else "", "literature" if "literature" in rel else "note")
        raw = path.read_text(encoding="utf-8", errors="replace")[:4000]
        meta = {"status": "unparseable", "error": f"{type(error).__name__}: {error}"[:300]}
        return [Doc(f"{kind}:{path.stem}", kind, rel, 0, path.stem, raw, meta)]
