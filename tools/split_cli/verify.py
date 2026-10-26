"""Check that the split CLI behaves like the monolith it was generated from.

The oracle is the legacy source itself. It is executed as a module, and both its ``main``
and the new one are run until the moment they call ``parse_args``, so the comparison sees
the complete parser each would use: every subcommand, alias, argument, default, help text
and certificate flag. Command bodies are compared as ASTs, and every lazily resolved name
must be the very object the legacy module held.
"""

from __future__ import annotations

import argparse
import ast
import builtins
import importlib
import sys
import types
import tempfile
from contextlib import contextmanager
from pathlib import Path

from tools.split_cli import extract as ex


class _Captured(Exception):
    pass


@contextmanager
def _source_imports():
    """Verification reads current source even after same-size, same-second edits.

    A fresh cache prefix prevents reads of timestamp-valid but stale .pyc files;
    disabling bytecode writes keeps verification read-only in the checkout.
    """
    prefix, no_write = sys.pycache_prefix, sys.dont_write_bytecode
    with tempfile.TemporaryDirectory(prefix="qsearch-verify-") as directory:
        sys.pycache_prefix, sys.dont_write_bytecode = directory, True
        try:
            yield
        finally:
            sys.pycache_prefix, sys.dont_write_bytecode = prefix, no_write


def capture_parser(main) -> argparse.ArgumentParser:
    """The parser ``main`` builds, taken at the moment it starts parsing."""
    original = argparse.ArgumentParser.parse_args
    held: dict[str, argparse.ArgumentParser] = {}

    def grab(self, *args, **kwargs):
        held.setdefault("parser", self)
        raise _Captured

    argparse.ArgumentParser.parse_args = grab
    try:
        main([])
    except _Captured:
        pass
    finally:
        argparse.ArgumentParser.parse_args = original
    return held["parser"]


def _value(value) -> str:
    if callable(value) and hasattr(value, "__name__"):
        return f"<callable {value.__name__}>"
    return repr(value)


def action_signature(action: argparse.Action) -> dict:
    sub = isinstance(action, argparse._SubParsersAction)
    sig = {
        "class": type(action).__name__,
        "options": list(action.option_strings),
        "dest": action.dest,
        "nargs": repr(action.nargs),
        "const": _value(action.const),
        "default": _value(action.default),
        "type": None if action.type is None else getattr(action.type, "__qualname__", repr(action.type)),
        "choices": None if sub or action.choices is None else repr(list(action.choices)),
        "required": action.required,
        "help": action.help,
        "metavar": repr(action.metavar),
    }
    if sub:
        sig["subparsers"] = {name: parser_signature(p) for name, p in action.choices.items()}
        sig["choice_help"] = [(c.dest, repr(c.metavar), c.help) for c in action._choices_actions]
    return sig


def parser_signature(parser: argparse.ArgumentParser) -> dict:
    return {
        "prog": parser.prog,
        "description": parser.description,
        "epilog": parser.epilog,
        "usage": parser.usage,
        "formatter": parser.formatter_class.__name__,
        "defaults": {k: _value(v) for k, v in parser._defaults.items()},
        "actions": [action_signature(a) for a in parser._actions],
        "help": parser.format_help(),
    }


def diff(old, new, where: str = "") -> list[str]:
    if isinstance(old, dict) and isinstance(new, dict):
        out = []
        for key in sorted(set(old) | set(new), key=str):
            if key not in new:
                out.append(f"{where}.{key}: missing in new")
            elif key not in old:
                out.append(f"{where}.{key}: not in legacy")
            else:
                out += diff(old[key], new[key], f"{where}.{key}")
        return out
    if isinstance(old, list) and isinstance(new, list):
        if len(old) != len(new):
            return [f"{where}: {len(old)} entries in legacy, {len(new)} in new"]
        return [p for i, (a, b) in enumerate(zip(old, new)) for p in diff(a, b, f"{where}[{i}]")]
    return [] if old == new else [f"{where}: {old!r} != {new!r}"[:400]]


def load_legacy(path: Path, root: Path) -> types.ModuleType:
    module = types.ModuleType("qsearch_legacy")
    module.__file__ = str(root / "qsearch.py")
    sys.modules["qsearch_legacy"] = module
    exec(compile(path.read_text(encoding="utf-8"), str(root / "qsearch.py"), "exec"), module.__dict__)
    return module


def _defs(source: str) -> dict[str, ast.FunctionDef]:
    return {n.name: n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef)}


def _without_lazy_import(node: ast.FunctionDef) -> ast.FunctionDef:
    body = list(node.body)
    first = body[0]
    index = 1 if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant) and isinstance(first.value.value, str) else 0
    if index < len(body) and isinstance(body[index], ast.ImportFrom) and body[index].module == "qsearch":
        body.pop(index)
    node.body = body
    return node


def function_problems(legacy_source: str, root: Path, functions: dict[str, str],
                      legacy_names: set[str] = frozenset()) -> tuple[list[str], list[str]]:
    """``legacy_names``: every global the executed legacy module held."""
    legacy = _defs(legacy_source)
    commands = {n: d for n, d in legacy.items() if n.startswith("command_")}
    problems = [f"function {n}: missing in new" for n in sorted(set(commands) - set(functions))]
    problems += [f"function {n}: not in legacy" for n in sorted(set(functions) - set(commands))]
    legacy_tree = ast.parse(legacy_source)
    imported = {b.name for b in ex.bindings_of(legacy_tree.body)}
    # Globals of the legacy module that are neither imports nor functions: __file__, _ROOT_DIR,
    # the loop variable, __name__ ... A moved function that reads one gets another value or none.
    module_only = ((set(legacy_names) | ex.module_globals(legacy_tree) | {"__file__", "__doc__"})
                   - set(legacy) - imported - {"__builtins__", "annotations"})
    legacy_top = set(legacy) | imported | set(dir(builtins)) | module_only
    legacy_globals = ex.function_globals(legacy_source)
    notes = []
    for path in sorted({root / (m.replace(".", "/") + ".py") for m in set(functions.values())}):
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)
        bound = set(dir(builtins)) | {n.name for n in tree.body if isinstance(n, ast.FunctionDef)}
        bound |= {b.name for b in ex.bindings_of(tree.body)}
        new_defs = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
        for name, used in ex.function_globals(source, str(path)).items():
            for name_read in sorted(used & module_only):
                problems.append(f"{path.name}: {name} reads legacy module global {name_read}, "
                                "which its new module does not provide")
            for missing in sorted(used - bound - module_only):
                if name in legacy_globals and missing in legacy_globals[name] and missing not in legacy_top:
                    notes.append(f"{name}: {missing} was already undefined in the legacy module")
                else:
                    problems.append(f"{path.name}: {name} reads undefined name {missing}")
        for name, node in new_defs.items():
            if name in commands and functions.get(name, "").replace(".", "/") + ".py" == path.relative_to(root).as_posix():
                if ast.dump(_without_lazy_import(node)) != ast.dump(commands[name]):
                    problems.append(f"function {name}: body differs from legacy")
    return problems, notes


def dispatch_problems(legacy_source: str, dispatch: list) -> list[str]:
    """DISPATCH must be the legacy main's flag if-chain: same flags, modules, functions, order."""
    node = _defs(legacy_source).get("main")
    if node is None:
        return ["DISPATCH: the legacy source has no main"]
    mono = ex.Monolith("", [], [])
    ex._parse_main(node, legacy_source, mono)
    old, new = [tuple(d) for d in mono.dispatch], [tuple(d) for d in dispatch]
    problems = [f"DISPATCH[{i}]: legacy {a} != new {b}" for i, (a, b) in enumerate(zip(old, new)) if a != b]
    if len(old) != len(new):
        problems.append(f"DISPATCH: {len(old)} flags in the legacy main, {len(new)} in the registry")
    return problems


def _use_root(root: Path) -> None:
    loaded = sys.modules.get("qsearch_cli")
    if loaded is not None:
        source = getattr(loaded, "__file__", None)
        if source is None or Path(source).resolve().parent != (root / "qsearch_cli").resolve():
            raise RuntimeError("qsearch_cli is already imported from another checkout")
    if str(root) not in sys.path[:1]:
        sys.path.insert(0, str(root))


@_source_imports()
def check_imports(root: Path) -> tuple[int, list[str]]:
    """Resolve every name in IMPORTS and every command function, as the monolith's start did.

    Returns how many names were checked and one line per failure.
    """
    root = root.resolve()
    _use_root(root)
    for extra in (root / "core", root / "theorems"):  # the order the shim sets up
        if str(extra) not in sys.path:
            sys.path.insert(0, str(extra))
    from qsearch_cli.imports import IMPORTS
    from qsearch_cli.registry import FUNCTIONS
    from qsearch_cli.resolve import resolve

    names = list(IMPORTS) + [f for f in FUNCTIONS if f not in IMPORTS]
    failures = []
    for name in names:
        try:
            resolve(name)
        except Exception as error:  # noqa: BLE001 - report every kind of import failure
            failures.append(f"{name}: {type(error).__name__}: {error}")
    return len(names), failures


@_source_imports()
def compare(root: Path, legacy_path: Path) -> tuple[list[str], list[str]]:
    root = root.resolve()
    _use_root(root)
    legacy_source = legacy_path.read_text(encoding="utf-8")
    legacy = load_legacy(legacy_path, root)
    from qsearch_cli import imports as new_imports
    from qsearch_cli import registry
    from qsearch_cli.main import run
    from qsearch_cli.parser import build_parser
    from qsearch_cli.resolve import resolve

    old_parser = capture_parser(legacy.main)
    new_parser = capture_parser(lambda argv: run(argv, build_parser(description=legacy.__doc__)))
    problems = diff(parser_signature(old_parser), parser_signature(new_parser), "parser")

    for name in new_imports.IMPORTS:
        if not hasattr(legacy, name):
            problems.append(f"import {name}: not bound in legacy")
        elif resolve(name) is not getattr(legacy, name):
            problems.append(f"import {name}: resolves to a different object than legacy")
    legacy_names = {b.name for b in ex.bindings_of(ast.parse(legacy_source).body)}
    problems += [f"import {n}: missing from IMPORTS" for n in sorted(legacy_names - set(new_imports.IMPORTS))]

    more, notes = function_problems(legacy_source, root, registry.FUNCTIONS, set(vars(legacy)))
    problems += more
    problems += dispatch_problems(legacy_source, registry.DISPATCH)

    shim = root / "qsearch.py"
    if "qsearch_cli" in shim.read_text(encoding="utf-8"):
        import qsearch

        sub = next(a for a in qsearch.build_parser()._actions if isinstance(a, argparse._SubParsersAction))
        for name, parser in sub.choices.items():
            func = parser._defaults.get("func")
            if func is not None and getattr(qsearch, func.__name__) is not func:
                problems.append(f"shim: qsearch.{func.__name__} is not the function {name} runs")
        notes.append(f"shim checked: {len(sub.choices)} subcommand names resolve to their functions")
    return problems, notes
