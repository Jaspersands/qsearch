"""Find the corpus source files under a Q-Search checkout and parse each into documents."""

from __future__ import annotations

from pathlib import Path
from typing import Callable

from tools.corpus.docs import Doc
from tools.corpus.sources import literature, markdown, registry, theorems

# parser(root, rel, issues) -> docs; a parser appends one line to `issues` per record it had to skip.
Parser = Callable[[Path, str, list[str]], list[Doc]]

# Orientation pages rewritten every pass: they match most queries and record no result.
ORIENTATION_PAGES = {"STATE.md", "TRAPS.md", "TOOLBOX.md"}


def _parser_for(rel: str) -> Parser | None:
    parts = rel.split("/")
    name = parts[-1]
    if parts[:2] == ["research", "registry"] and name in registry.PARSERS:
        return registry.parse
    if len(parts) == 2 and parts[0] == "research" and name.endswith(".md") and name not in ORIENTATION_PAGES:
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


def parse_source(root: Path, rel: str) -> tuple[list[Doc], list[str]]:
    """Parse one source file into (docs, issues).

    A parser failure of any kind (bad JSON, an unexpected record shape, a bug) never escapes:
    the file becomes one raw-text document with status `unparseable` and the failure is
    returned as an issue, so callers can say the index is incomplete instead of empty.
    """
    parser = _parser_for(rel)
    if parser is None:
        return [], []
    issues: list[str] = []
    try:
        return parser(root, rel, issues), issues
    except Exception as error:  # noqa: BLE001 - one bad file must not take the index down
        message = f"unparseable, indexed as raw text ({type(error).__name__}: {error})"[:300]
        path = root / rel
        parts = rel.split("/")
        kind = _FALLBACK_KIND.get(parts[1] if len(parts) > 2 else "", "literature" if "literature" in rel else "note")
        try:
            raw = path.read_text(encoding="utf-8", errors="replace")[:4000]
        except OSError:
            return [], [message]
        meta = {"status": "unparseable", "error": message}
        return [Doc(f"{kind}:{path.stem}", kind, rel, 0, path.stem, raw, meta)], [message]


def parse_file(root: Path, rel: str) -> list[Doc]:
    """Parse one source file; a file that cannot be parsed becomes one raw-text document."""
    return parse_source(root, rel)[0]
