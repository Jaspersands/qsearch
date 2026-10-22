"""Check a Q-Search checkout for the failures that have blocked a merge.

    python tools/preflight/preflight.py              # before every commit; static, a few seconds
    python tools/preflight/preflight.py --json
    python tools/preflight/preflight.py --imports    # also import every CLI name (slow)
    python tools/preflight/preflight.py --validate   # also run qsearch.py validate (slow)

JSON files under research/hypotheses, research/registry, research/audits and
research/classical_baselines must parse: an invalid hypothesis contract broke the merge of
2026-10-19. Other research/ directories are not read.
Every theorems/, core/ or qsearch_cli/ module the CLI refers to must exist and be tracked by
git: the same merge carried 24 imports of modules that were only in one working copy. Module
references are read statically, never imported: AST imports in qsearch.py,
qsearch_cli/imports.py and qsearch_cli/commands/*.py (theorems.x, qsearch_cli.x, from core
import y, and bare names that resolve to a file in theorems/ or core/), the IMPORTS table,
the module column of DISPATCH, and the module columns of ORDER and FUNCTIONS; then the
imports inside each module found, by a line scan, until no new module turns up. Every
subcommand in research/audits/cli_manifest.json must still be in the registry's ORDER, in
the same module.

Prints one line per problem and the count; exits 1 when there is any problem, else 0.
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import re
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

REPO = Path(__file__).resolve().parents[2]
JSON_DIRS = ("research/hypotheses", "research/registry", "research/audits", "research/classical_baselines")
JSON_RETRIES, JSON_RETRY_SECONDS = 3, 0.025  # as tools/corpus/docs.py:read_json
IMPORTS_FILE = "qsearch_cli/imports.py"
REGISTRY = "qsearch_cli/registry.py"
MANIFEST = "research/audits/cli_manifest.json"
IMPORT_SOURCES = ("qsearch.py", IMPORTS_FILE, "qsearch_cli/commands/*.py")
PACKAGES = ("theorems", "core")  # on the CLI's sys.path in this order
CLI_PACKAGE = "qsearch_cli"
MODULE_PREFIXES = ("theorems.", "core.", "qsearch_cli.")


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
        found: list[Problem] = []
        for path in _json_files(root, directory, found):
            rel = path.relative_to(root).as_posix()
            if path.is_symlink() and not path.exists():
                found.append(Problem("json", rel, "dangling symlink"))
            elif path.is_file():  # not a FIFO or socket, which would block or fail the read
                error = _json_error(path)
                if error is not None:
                    found.append(Problem("json", rel, error))
        problems += sorted(found, key=lambda problem: Path(problem.path))
    return problems


def _json_files(root: Path, directory: str, problems: list[Problem]) -> list[Path]:
    """Every *.json name under root/directory, sorted; a directory that cannot be listed is a problem.

    Path.rglob skips such a directory without a word, so this walks with os.walk instead.
    """
    base = root / directory
    if not base.is_dir():
        return []

    def unlistable(error: OSError) -> None:
        where = Path(error.filename).relative_to(root).as_posix() if error.filename else directory
        problems.append(Problem("json", where, f"cannot list: {error.strerror or error}"))

    paths = []
    for dirpath, dirnames, filenames in os.walk(base, onerror=unlistable):
        dirnames.sort()
        paths += [Path(dirpath) / name for name in filenames if name.endswith(".json")]
    return sorted(paths)


def _json_error(path: Path) -> str | None:
    """Why path is not JSON, in the parser's words; None when it parses.

    A failed parse is read again a few times, briefly, as the repository's own readers do: an
    agent rewriting the file in place can be caught half way. Integers are kept as text, so
    one past Python's 4300-digit int() limit still parses.
    """
    for attempt in range(JSON_RETRIES + 1):
        try:
            json.loads(path.read_text(encoding="utf-8"), parse_int=str)
            return None
        except ValueError as error:  # JSONDecodeError, or UnicodeDecodeError from a cut multi-byte character
            if attempt == JSON_RETRIES:
                return str(error)
            time.sleep(JSON_RETRY_SECONDS * (attempt + 1))
        except (RecursionError, OSError) as error:  # nested deeper than the parser follows; unreadable
            return str(error)
    raise AssertionError("unreachable")


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


# Each CLI table: (file, container, row width, shape). Width 0: a dict whose values are module names.
TABLES = {
    "IMPORTS": (IMPORTS_FILE, dict, 2, "a dict of name: (module, attribute or None)"),
    "DISPATCH": (REGISTRY, list, 3, "a list of (flag, module, function)"),
    "ORDER": (REGISTRY, list, 3, "a list of (subcommand, module, function)"),
    "FUNCTIONS": (REGISTRY, dict, 0, "a dict of function: module"),
}


def _table(root: Path, name: str):
    """The CLI table ``name``, read with _literal; None when absent, ValueError when it has another shape."""
    rel, container, width, shape = TABLES[name]
    value = _literal(root, rel, name)
    if value is None:
        return None

    def well_formed(row) -> bool:
        if width == 0:
            return isinstance(row, str)
        if not isinstance(row, (tuple, list)) or len(row) != width:
            return False
        last_ok = isinstance(row[-1], str) or (name == "IMPORTS" and row[-1] is None)
        return last_ok and all(isinstance(column, str) for column in row[:-1])

    if not isinstance(value, container):
        raise ValueError(f"{name} in {rel} is not {shape}")
    for key, row in value.items() if isinstance(value, dict) else enumerate(value):
        if not well_formed(row):
            raise ValueError(f"{name} in {rel} is not {shape}: {key!r}: {row!r}")
    return value


def _dotted_path(root: Path, name: str) -> str | None:
    """The file a dotted ``theorems.``, ``core.`` or ``qsearch_cli.`` name loads, present or not.

    A name that is a directory is a package: its __init__.py, or None when it has none.
    """
    rel = name.replace(".", "/")
    if (root / rel).is_dir():
        return f"{rel}/__init__.py" if (root / rel / "__init__.py").is_file() else None
    return rel + ".py"


def _module_path(root: Path, module: str) -> str | None:
    """The theorems/, core/ or qsearch_cli/ file a table entry loads; None for the standard library,
    other dotted names and the packages themselves.

    A bare name resolves as the CLI's sys.path does: theorems/ first, then core/.
    """
    if module.startswith(MODULE_PREFIXES):
        return _dotted_path(root, module)
    if "." in module or module in sys.stdlib_module_names or module in PACKAGES:
        return None
    return f"theorems/{module}.py" if (root / "theorems" / f"{module}.py").is_file() else f"core/{module}.py"


def _import_paths(root: Path, node: ast.AST) -> list[str]:
    """The theorems/, core/ or qsearch_cli/ files one import statement loads.

    ``theorems.x``, ``qsearch_cli.x`` and ``from core import y`` name their file, present or
    not. A bare name (``from x import f``) counts only when theorems/x.py or core/x.py exists,
    the order the CLI puts them on sys.path; a bare name with neither file is a third-party
    package.
    """
    if isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
        if node.module in PACKAGES:
            return [f"{node.module}/{alias.name}.py" for alias in node.names if alias.name != "*"]
        names = [node.module]
    elif isinstance(node, ast.Import):
        names = [alias.name for alias in node.names]
    else:
        return []
    paths = []
    for name in names:
        if name.startswith(MODULE_PREFIXES):
            path = _dotted_path(root, name)
            if path is not None:
                paths.append(path)
            continue
        top = name.split(".")[0]
        if top in sys.stdlib_module_names or top in PACKAGES:
            continue
        for directory in PACKAGES:
            if (root / directory / f"{top}.py").is_file():
                paths.append(f"{directory}/{top}.py")
                break
    return paths


# Strings and comments, blanked before the line scan below (a triple-quoted string keeps its newlines).
_STRING_OR_COMMENT = re.compile(
    r'"""(?:\\[\s\S]|[^\\])*?"""'
    r"|'''(?:\\[\s\S]|[^\\])*?'''"
    r'|"(?:\\.|[^"\\\n])*"'
    r"|'(?:\\.|[^'\\\n])*'"
    r"|#[^\n]*"
)
_IMPORT_LINE = re.compile(r"^[ \t]*(?:from[ \t]+[\w.]+[ \t]+import\b|import[ \t]+[\w.])", re.M)


def _scanned_imports(text: str) -> list[ast.stmt]:
    """The import statements in Python source, found by a line scan instead of a full parse.

    Parsing every module the CLI reaches through other modules adds about three seconds to a
    run; this scan adds a fraction of one. It sees an import that starts a line, outside
    strings and comments, with its parenthesised or backslash-continued names. It misses a
    one-line compound statement (``if x: import y``) and an import after a semicolon.
    """
    code = _STRING_OR_COMMENT.sub(lambda m: "\n" * m.group().count("\n"), text)
    nodes: list[ast.stmt] = []
    for match in _IMPORT_LINE.finditer(code):
        end = match.start()
        while True:
            newline = code.find("\n", end)
            end = len(code) if newline < 0 else newline
            statement = code[match.start() : end]
            if newline < 0 or (statement.count("(") <= statement.count(")") and not statement.endswith("\\")):
                break
            end += 1
        try:
            nodes.extend(ast.parse(statement.strip()).body)
        except SyntaxError:
            continue
    return nodes


def referenced_modules(root: Path) -> dict[str, set[str]]:
    """Every theorems/, core/ or qsearch_cli/ file the CLI refers to, mapped to the files that refer to it.

    Imports inside those files are followed too, since the CLI loads a module's imports with it.
    """
    root = Path(root).resolve()
    refs: dict[str, set[str]] = {}
    parsed: set[str] = set()

    def add(module_path: str | None, source: str) -> None:
        if module_path is not None:
            refs.setdefault(module_path, set()).add(source)

    for pattern in IMPORT_SOURCES:
        for path in sorted(root.glob(pattern)):
            rel = path.relative_to(root).as_posix()
            parsed.add(rel)
            for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"), filename=rel)):
                for module_path in _import_paths(root, node):
                    add(module_path, rel)
    for module, attribute in (_table(root, "IMPORTS") or {}).values():
        if module in PACKAGES and attribute:  # ("theorems", "x"): `from theorems import x`, as sweep writes it
            add(f"{module}/{attribute}.py", IMPORTS_FILE)
        else:
            add(_module_path(root, module), IMPORTS_FILE)
    for _flag, module, _function in _table(root, "DISPATCH") or []:
        add(_module_path(root, module), REGISTRY)
    # parser.py imports every ORDER module to build the parser; resolve.py imports FUNCTIONS' on use.
    for _name, module, _adder in _table(root, "ORDER") or []:
        add(_module_path(root, module), REGISTRY)
    for module in (_table(root, "FUNCTIONS") or {}).values():
        add(_module_path(root, module), REGISTRY)
    queue = sorted(refs)
    while queue:
        rel = queue.pop()
        if rel in parsed or not (root / rel).is_file():
            continue
        parsed.add(rel)
        try:
            text = (root / rel).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue  # its own path is still checked; only its imports go unfollowed
        for node in _scanned_imports(text):
            for module_path in _import_paths(root, node):
                if module_path not in refs:
                    queue.append(module_path)
                add(module_path, rel)
    return refs


def _git_output(root: Path, *args: str) -> str | None:
    """stdout of ``git -C root args``; None when git is missing or fails."""
    try:
        result = subprocess.run(["git", "-C", str(root), *args], capture_output=True)
    except OSError:
        return None
    return result.stdout.decode("utf-8", errors="replace") if result.returncode == 0 else None


def _git_index(root: Path) -> tuple[set[str], set[str]] | str:
    """(paths git tracks, paths only marked intent-to-add) under theorems/, core/ and qsearch_cli/,
    relative to root; when git cannot tell, why not.

    git can tell only when root is the top of its own work tree. A tree that sits inside some
    other repository (an export unpacked under a dotfiles repository) is not that repository's.
    A staged file is tracked: the commit will include it. One added with ``git add -N`` is
    listed by ls-files, but a plain commit leaves it out; ``git diff-files`` shows it as added.
    All three commands only read the index; none takes index.lock.
    """
    root = Path(root).resolve()
    prefix = _git_output(root, "rev-parse", "--show-prefix")
    if prefix is None:
        return "git unavailable"
    if prefix.strip():
        return f"git unavailable: the root is not the top of a git work tree (git sees it as {prefix.strip()})"
    pathspec = ("--", *PACKAGES, CLI_PACKAGE)
    listing = _git_output(root, "ls-files", "-z", *pathspec)
    if listing is None:
        return "git unavailable"
    # Plumbing diff-files, not `git diff`: porcelain diff refreshes stale stat data and writes
    # .git/index back under index.lock, even with GIT_OPTIONAL_LOCKS=0.
    added = _git_output(root, "diff-files", "--name-only", "-z", "--diff-filter=A", *pathspec)
    intent = {p for p in (added or "").split("\0") if p}
    return {p for p in listing.split("\0") if p} - intent, intent


def tracked_files(root: Path) -> set[str] | None:
    """Paths under theorems/, core/ and qsearch_cli/ that git tracks or has staged, relative to root;
    None when git cannot tell (see _git_index)."""
    index = _git_index(root)
    return None if isinstance(index, str) else index[0]


def _spelled_on_disk(root: Path, rel: str, listings: dict[Path, list[str]]) -> str | None:
    """rel as a file on disk spells it: rel itself, else a path differing only in case, else None.

    Python's import system matches case even where the file system does not (macOS), so a
    case mismatch is a missing module on every platform. ``listings`` caches os.listdir.
    """
    here, parts = root, []
    for name in rel.split("/"):
        if here not in listings:
            try:
                listings[here] = sorted(os.listdir(here))
            except OSError:
                listings[here] = []
        if name not in listings[here]:
            matches = [n for n in listings[here] if n.casefold() == name.casefold()]
            if not matches:
                return None
            name = matches[0]
        parts.append(name)
        here = here / name
    return "/".join(parts) if here.is_file() else None


def check_untracked_imports(root: Path) -> list[Problem]:
    """Modules the CLI refers to that are missing on disk or that git does not track."""
    root = Path(root).resolve()
    try:
        refs = referenced_modules(root)
    except (OSError, SyntaxError, ValueError, TypeError) as error:
        where = error.filename if isinstance(error, SyntaxError) and error.filename else "."
        return [Problem("imports", where, f"cannot read the CLI sources: {type(error).__name__}: {error}")]
    index = _git_index(root)
    tracked, intent = (None, set()) if isinstance(index, str) else index
    problems = []
    listings: dict[Path, list[str]] = {}
    for module_path in sorted(refs):
        on_disk = _spelled_on_disk(root, module_path, listings)
        if on_disk is None:
            problems.append(Problem("imports", module_path, "missing on disk"))
        elif on_disk != module_path:
            problems.append(Problem("imports", module_path, f"missing on disk (case differs: {on_disk})"))
        elif module_path in intent:
            problems.append(Problem("imports", module_path, "not tracked by git (intent-to-add only)"))
        elif tracked is not None and module_path not in tracked:
            problems.append(Problem("imports", module_path, "not tracked by git"))
    if isinstance(index, str):
        problems.append(Problem("imports", ".", index))
    return problems


def registry_order(root: Path) -> dict[str, str]:
    """Subcommand name -> module, from the ORDER literal in qsearch_cli/registry.py (read, never imported)."""
    order = _table(Path(root).resolve(), "ORDER")
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
    if not root.is_dir():
        parser.error(f"--root {root} is not a directory")  # exits 2: a typo, not a broken checkout
    if not (root / "qsearch.py").is_file():  # say a subdirectory of one: every check would mislead
        parser.error(f"--root {root} is not a Q-Search checkout: it has no qsearch.py")
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
