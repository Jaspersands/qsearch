"""Summarize theorems/*.py modules from their docstrings without importing them."""

from __future__ import annotations

import ast
from pathlib import Path

from tools.corpus.docs import Doc, words


def parse(root: Path, rel: str, issues: list[str] | None = None) -> list[Doc]:
    path = root / rel
    source = path.read_text(encoding="utf-8", errors="replace")
    stem = path.stem
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return [Doc(f"theorem:{stem}", "theorem", rel, 1, stem, f"{words(stem)}. {source[:3000]}", {"functions": []})]

    module_doc = ast.get_docstring(tree) or ""
    functions: list[str] = []
    summaries: list[str] = []
    artifacts: list[str] = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if node.name.startswith("_"):
                continue
            functions.append(node.name)
            doc = ast.get_docstring(node)
            if doc:
                summaries.append(doc.strip().split("\n\n")[0])
        elif isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            value = node.value.value
            if value.endswith((".json", ".md")):
                artifacts.append(value)

    title = module_doc.strip().splitlines()[0] if module_doc.strip() else stem
    text = " ".join(
        [words(stem) + ".", module_doc, " ".join(words(name) for name in functions) + ".", " ".join(summaries)]
    )
    meta = {"functions": functions, "artifacts": artifacts, "status": "code"}
    return [Doc(f"theorem:{stem}", "theorem", rel, 1, title[:300], text[:6000], meta)]
