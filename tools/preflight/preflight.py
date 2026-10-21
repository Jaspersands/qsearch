"""Check a Q-Search checkout for the failures that have blocked a merge.

Research JSON files must parse: an invalid hypothesis contract broke the merge of 2026-10-19.
Every theorems/ or core/ module the CLI refers to must exist and be tracked by git: the same
merge carried 24 imports of modules that were only in one working copy. Module references
are read statically, never imported: AST imports of theorems.* and core.* in qsearch.py,
qsearch_cli/imports.py and qsearch_cli/commands/*.py, the IMPORTS table, and the module
column of DISPATCH.
"""

from __future__ import annotations

import ast
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

JSON_DIRS = ("research/hypotheses", "research/registry", "research/audits", "research/classical_baselines")
IMPORTS_FILE = "qsearch_cli/imports.py"
REGISTRY = "qsearch_cli/registry.py"
IMPORT_SOURCES = ("qsearch.py", IMPORTS_FILE, "qsearch_cli/commands/*.py")
MODULE_PREFIXES = ("theorems.", "core.")


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


def _literal(root: Path, rel: str, name: str):
    """The literal assigned to ``name`` at the top level of root/rel; None when absent. Never imported."""
    path = root / rel
    if not path.is_file():
        return None
    for node in ast.parse(path.read_text(encoding="utf-8"), filename=rel).body:
        targets = node.targets if isinstance(node, ast.Assign) else [node.target] if isinstance(node, ast.AnnAssign) else []
        if any(isinstance(t, ast.Name) and t.id == name for t in targets) and node.value is not None:
            try:
                return ast.literal_eval(node.value)
            except ValueError as error:
                raise ValueError(f"{rel}: {name} is not a literal ({error})") from None
    return None


def _module_path(root: Path, module: str) -> str | None:
    """The theorems/ or core/ file a table entry loads; None for the standard library and other packages.

    A bare name resolves as the CLI's sys.path does: theorems/ first, then core/.
    """
    if module.startswith(MODULE_PREFIXES):
        return module.replace(".", "/") + ".py"
    if "." in module or module in sys.stdlib_module_names:
        return None
    return f"theorems/{module}.py" if (root / "theorems" / f"{module}.py").is_file() else f"core/{module}.py"


def referenced_modules(root: Path) -> dict[str, set[str]]:
    """Every theorems/ or core/ file the CLI refers to, mapped to the source files that refer to it."""
    root = Path(root).resolve()
    refs: dict[str, set[str]] = {}

    def add(module_path: str | None, source: str) -> None:
        if module_path is not None:
            refs.setdefault(module_path, set()).add(source)

    for pattern in IMPORT_SOURCES:
        for path in sorted(root.glob(pattern)):
            rel = path.relative_to(root).as_posix()
            for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"), filename=rel)):
                if isinstance(node, ast.ImportFrom) and node.level == 0:
                    names = [node.module or ""]
                elif isinstance(node, ast.Import):
                    names = [alias.name for alias in node.names]
                else:
                    continue
                for name in names:
                    if name.startswith(MODULE_PREFIXES):
                        add(name.replace(".", "/") + ".py", rel)
    for module, _attribute in (_literal(root, IMPORTS_FILE, "IMPORTS") or {}).values():
        add(_module_path(root, module), IMPORTS_FILE)
    for _flag, module, _function in _literal(root, REGISTRY, "DISPATCH") or []:
        add(_module_path(root, module), REGISTRY)
    return refs


def tracked_files(root: Path) -> set[str] | None:
    """Paths under theorems/ and core/ that git tracks, relative to root; None when git cannot tell."""
    try:
        result = subprocess.run(
            ["git", "-C", str(Path(root).resolve()), "ls-files", "-z", "--", "theorems", "core"], capture_output=True
        )
    except OSError:
        return None
    if result.returncode != 0:
        return None
    return {p for p in result.stdout.decode("utf-8", errors="replace").split("\0") if p}


def check_untracked_imports(root: Path) -> list[Problem]:
    """Modules the CLI refers to that are missing on disk or that git does not track."""
    root = Path(root).resolve()
    try:
        refs = referenced_modules(root)
    except (OSError, SyntaxError, ValueError) as error:
        return [Problem("imports", ".", f"cannot read the CLI sources: {type(error).__name__}: {error}")]
    tracked = tracked_files(root)
    problems = []
    for module_path in sorted(refs):
        if not (root / module_path).is_file():
            problems.append(Problem("imports", module_path, "missing on disk"))
        elif tracked is not None and module_path not in tracked:
            problems.append(Problem("imports", module_path, "not tracked by git"))
    if tracked is None:
        problems.append(Problem("imports", ".", "git unavailable"))
    return problems
