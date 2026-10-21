"""Check a Q-Search checkout for the failures that have blocked a merge.

    python tools/preflight/preflight.py              # before every commit; static, a few seconds
    python tools/preflight/preflight.py --json
    python tools/preflight/preflight.py --imports    # also import every CLI name (slow)
    python tools/preflight/preflight.py --validate   # also run qsearch.py validate (slow)

Research JSON files must parse: an invalid hypothesis contract broke the merge of 2026-10-19.
Every theorems/ or core/ module the CLI refers to must exist and be tracked by git: the same
merge carried 24 imports of modules that were only in one working copy. Module references
are read statically, never imported: AST imports in qsearch.py, qsearch_cli/imports.py and
qsearch_cli/commands/*.py (theorems.x, from core import y, and bare names that resolve to a
file in theorems/ or core/), the IMPORTS table, and the module column of DISPATCH. Every
subcommand in research/audits/cli_manifest.json must still be in the registry's ORDER, in
the same module.

Prints one line per problem and the count; exits 1 when there is any problem, else 0.
"""

from __future__ import annotations

import argparse
import ast
import json
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

REPO = Path(__file__).resolve().parents[2]
JSON_DIRS = ("research/hypotheses", "research/registry", "research/audits", "research/classical_baselines")
IMPORTS_FILE = "qsearch_cli/imports.py"
REGISTRY = "qsearch_cli/registry.py"
MANIFEST = "research/audits/cli_manifest.json"
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
        if isinstance(node, ast.Assign):
            targets = node.targets
        elif isinstance(node, ast.AnnAssign):
            targets = [node.target]
        else:
            continue
        if any(isinstance(t, ast.Name) and t.id == name for t in targets) and node.value is not None:
            try:
                return ast.literal_eval(node.value)
            except ValueError:
                raise ValueError(f"{name} in {rel} is not a literal") from None
    return None


def _module_path(root: Path, module: str) -> str | None:
    """The theorems/ or core/ file a table entry loads; None for the standard library and other dotted names.

    A bare name resolves as the CLI's sys.path does: theorems/ first, then core/.
    """
    if module.startswith(MODULE_PREFIXES):
        return module.replace(".", "/") + ".py"
    if "." in module or module in sys.stdlib_module_names:
        return None
    return f"theorems/{module}.py" if (root / "theorems" / f"{module}.py").is_file() else f"core/{module}.py"


def _import_paths(root: Path, node: ast.AST) -> list[str]:
    """The theorems/ or core/ files one import statement loads.

    ``theorems.x`` and ``from core import y`` name their file, present or not. A bare name
    (``from x import f``) counts only when theorems/x.py or core/x.py exists, the order the
    CLI puts them on sys.path; a bare name with neither file is a third-party package.
    """
    if isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
        if node.module in ("theorems", "core"):
            return [f"{node.module}/{alias.name}.py" for alias in node.names if alias.name != "*"]
        names = [node.module]
    elif isinstance(node, ast.Import):
        names = [alias.name for alias in node.names]
    else:
        return []
    paths = []
    for name in names:
        if name.startswith(MODULE_PREFIXES):
            paths.append(name.replace(".", "/") + ".py")
            continue
        top = name.split(".")[0]
        if top in sys.stdlib_module_names or top in ("theorems", "core"):
            continue
        for directory in ("theorems", "core"):
            if (root / directory / f"{top}.py").is_file():
                paths.append(f"{directory}/{top}.py")
                break
    return paths


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
                for module_path in _import_paths(root, node):
                    add(module_path, rel)
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
    except (OSError, SyntaxError, ValueError, TypeError) as error:
        where = error.filename if isinstance(error, SyntaxError) and error.filename else "."
        return [Problem("imports", where, f"cannot read the CLI sources: {type(error).__name__}: {error}")]
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


def registry_order(root: Path) -> dict[str, str]:
    """Subcommand name -> module, from the ORDER literal in qsearch_cli/registry.py (read, never imported)."""
    order = _literal(Path(root).resolve(), REGISTRY, "ORDER")
    if order is None:
        raise ValueError(f"{REGISTRY} has no ORDER")
    return {name: module for name, module, _add_parser in order}


def check_manifest(root: Path) -> list[Problem]:
    """Every subcommand the split manifest lists must still be in ORDER, in the same module."""
    root = Path(root).resolve()
    try:
        entries = json.loads((root / MANIFEST).read_text(encoding="utf-8"))["subcommands"]
        expected = {entry["name"]: entry["module"] for entry in entries}
    except FileNotFoundError:
        return [Problem("manifest", MANIFEST, "missing")]
    except (OSError, ValueError, KeyError, TypeError) as error:
        return [Problem("manifest", MANIFEST, f"invalid: {type(error).__name__}: {error}")]
    try:
        order = registry_order(root)
    except (OSError, SyntaxError, ValueError, TypeError) as error:
        return [Problem("manifest", REGISTRY, f"cannot read ORDER: {type(error).__name__}: {error}")]
    problems = []
    for name, module in expected.items():
        if name not in order:
            problems.append(Problem("manifest", REGISTRY, f"subcommand {name} missing from ORDER"))
        elif order[name] != module:
            problems.append(Problem("manifest", REGISTRY, f"{name}: manifest says {module}, ORDER says {order[name]}"))
    return problems


def _check_imports(root: Path) -> tuple[int, list[str]]:
    from tools.split_cli.verify import check_imports  # imports the CLI and every theorem module it names

    return check_imports(root)


def check_imports_resolve(root: Path) -> list[Problem]:
    """Resolve every IMPORTS name and command function in this process, as the CLI would (slow)."""
    root = Path(root).resolve()
    try:
        _checked, failures = _check_imports(root)
    except Exception as error:  # noqa: BLE001 - the verifier failing to start is itself the problem
        return [Problem("resolve", ".", f"{type(error).__name__}: {error}")]
    return [Problem("resolve", "qsearch_cli", failure) for failure in failures]


def check_validate(root: Path) -> list[Problem]:
    """Run ``qsearch.py validate`` as CI does (slow); a non-zero exit is one problem."""
    root = Path(root).resolve()
    result = subprocess.run(
        [sys.executable, "qsearch.py", "validate"], cwd=root, capture_output=True, text=True, errors="replace"
    )
    if result.returncode == 0:
        return []
    reason = _validate_reason(result.stdout, result.stderr)
    return [Problem("validate", "qsearch.py", f"exit {result.returncode}: {reason}")]


def _validate_reason(stdout: str, stderr: str) -> str:
    """Why validate failed: its first issue (it prints a JSON report on stdout), else the last line of output."""
    try:
        report = json.loads(stdout)
    except ValueError:
        report = None
    issues = report.get("issues") if isinstance(report, dict) else None
    if isinstance(issues, list) and issues:
        first = issues[0]
        if isinstance(first, dict) and "message" in first:
            first = f"{first.get('candidate_id', '?')}: {first['message']}"
        return f"{len(issues)} issues, first: {first}"
    for stream in (stderr, stdout):
        lines = [line.strip() for line in stream.splitlines() if line.strip()]
        if lines:
            return lines[-1]
    return "(no output)"


def run(root: Path, imports: bool = False, validate: bool = False) -> list[Problem]:
    """The static checks, then the slow ones that were asked for."""
    problems = check_json(root) + check_untracked_imports(root) + check_manifest(root)
    if imports:
        problems += check_imports_resolve(root)
    if validate:
        problems += check_validate(root)
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", default=str(REPO), help="Checkout to check (default: this repository).")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--imports", action="store_true", help="Also import every CLI name and command (slow).")
    parser.add_argument("--validate", action="store_true", help="Also run qsearch.py validate (slow).")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    problems = run(root, imports=args.imports, validate=args.validate)
    if args.json:
        print(json.dumps({"root": str(root), "problems": [asdict(p) for p in problems], "count": len(problems)}, indent=2))
    else:
        for problem in problems:
            print(f"{problem.check}: {problem.path}: {problem.message}")
        print(f"{len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
