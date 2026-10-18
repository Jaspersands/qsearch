"""Write the qsearch_cli package, the qsearch.py shim and the manifest from a Monolith."""

from __future__ import annotations

import ast
import hashlib
import json
import re
from pathlib import Path

from tools.split_cli import extract as ex

PACKAGE = "qsearch_cli"
MANIFEST = "research/audits/cli_manifest.json"
DOMAINS = [
    ("self_dual_wreath_", "self_dual_wreath"),
    ("sdw_", "self_dual_wreath"),
    ("dcp_", "dcp"),
    ("code_", "code"),
    ("coset_", "coset"),
    ("native_", "native"),
]
TITLES = {
    "dcp": "Dihedral coset problem (DCP)",
    "code": "Code equivalence",
    "coset": "Nonabelian coset and hidden-subgroup",
    "self_dual_wreath": "Self-dual wreath product",
    "native": "Native higher-call",
    "general": "General and smaller-track",
}
LEGACY_SENTINEL = "    pass  # legacy-extensions"


def domain_of(function: str) -> str:
    stem = function.removeprefix("command_")
    for prefix, domain in DOMAINS:
        if stem.startswith(prefix):
            return domain
    return "general"


def adder_name(subcommand: str) -> str:
    return "add_" + re.sub(r"\W", "_", subcommand)


def module_of(domain: str) -> str:
    return f"{PACKAGE}.commands.{domain}"


def lazy_line(names: list[str], indent: str) -> str:
    line = f"{indent}from qsearch import {', '.join(names)}"
    if len(line) <= 100:
        return line
    inner = "".join(f"{indent}    {n},\n" for n in names)
    return f"{indent}from qsearch import (\n{inner}{indent})"


def render_command(cmd: ex.Command) -> str:
    lines = cmd.source.splitlines()
    if cmd.lazy:
        lines.insert(cmd.insert_at, lazy_line(cmd.lazy, cmd.indent))
    return "\n".join(lines)


def render_adder(block: ex.Block, subparsers: str, imports: list[str] = ()) -> str:
    head = f"def {adder_name(block.subcommand)}({subparsers}) -> None:"
    local = "".join(f"    {statement}\n" for statement in imports)
    return f"{head}\n{local}{block.source}"


def _header(domain: str, statements: list[str]) -> str:
    imports = "\n".join(["from __future__ import annotations", "", *statements])
    return (
        f'"""{TITLES.get(domain, domain)} subcommands, moved out of qsearch.py by tools/split_cli/migrate.py.\n\n'
        "Each ``add_*`` function registers one subcommand and each ``command_*`` function runs one.\n"
        "A command imports what it needs from ``qsearch`` when it runs, so loading this module stays\n"
        "cheap and ``monkeypatch.setattr(qsearch, name, ...)`` still reaches the command.\n"
        '"""\n\n'
        f"{imports}\n"
    )


def _std_statements(names: set[str], bindings: dict[str, ex.Binding]) -> list[str]:
    statements = {bindings[n].statement() for n in names if n in bindings}
    plain = sorted(s for s in statements if s.startswith("import "))
    froms = sorted(s for s in statements if s.startswith("from "))
    return plain + froms


def render_domain(domain: str, commands: list[ex.Command], blocks: list[ex.Block], bindings: list[ex.Binding],
                  subparsers: str = "subparsers") -> str:
    by_name = {b.name: b for b in bindings}
    std = {"argparse"} | {n for c in commands for n in c.stdlib} | {n for b in blocks for n in b.stdlib}
    parts = [_header(domain, _std_statements(std, by_name))]
    placed: set[int] = set()
    for cmd in commands:
        for i, block in enumerate(blocks):
            if block.function == cmd.name:
                parts.append(render_adder(block, subparsers))
                placed.add(i)
        parts.append(render_command(cmd))
    parts += [render_adder(b, subparsers) for i, b in enumerate(blocks) if i not in placed]
    return "\n\n\n".join(parts) + "\n"


def _block_domain(block: ex.Block, functions: dict[str, str]) -> str:
    if block.function and block.function in functions:
        return functions[block.function].rsplit(".", 1)[1]
    return domain_of("command_" + re.sub(r"\W", "_", block.subcommand))


def _q(value) -> str:
    return "None" if value is None else json.dumps(value)


def render_registry(order: list[tuple[str, str, str]], functions: dict[str, str],
                    dispatch: list[tuple[str, str, str]]) -> str:
    lines = [
        '"""Where every qsearch subcommand and command function lives.',
        "",
        "Maintained by tools/split_cli/migrate.py. To add a subcommand by hand, append it to ORDER",
        "and its function to FUNCTIONS; ORDER is also the order of ``qsearch.py --help``.",
        '"""',
        "",
        "# (subcommand, module, function that adds its parser), in --help order",
        "ORDER = [",
        *[f"    ({_q(n)}, {_q(m)}, {_q(a)})," for n, m, a in order],
        "]",
        "",
        "# command function -> module that defines it",
        "FUNCTIONS = {",
        *[f"    {_q(n)}: {_q(m)}," for n, m in functions.items()],
        "}",
        "",
        "# certificate flags: (args attribute, module, function), checked in this order before the subcommand",
        "DISPATCH = [",
        *[f"    ({_q(d)}, {_q(m)}, {_q(f)})," for d, m, f in dispatch],
        "]",
    ]
    return "\n".join(lines) + "\n"


def render_imports(table: dict[str, tuple[str, str | None]]) -> str:
    lines = [
        '"""Every name qsearch.py used to import at startup, resolved on first use instead."""',
        "",
        "IMPORTS = {",
        *[f"    {_q(n)}: ({_q(m)}, {_q(a)})," for n, (m, a) in table.items()],
        "}",
    ]
    return "\n".join(lines) + "\n"


def _stdlib_used(text: str, bindings: dict[str, ex.Binding]) -> set[str]:
    tree = ast.parse(text)
    return {n.id for n in ast.walk(tree) if isinstance(n, ast.Name) and n.id in bindings and bindings[n.id].stdlib}


def render_parser(mono: ex.Monolith) -> str:
    by_name = {b.name: b for b in mono.bindings}
    prelude = mono.prelude.replace("description=__doc__", "description=description")
    std = _stdlib_used(_dedent(prelude), by_name) - {"importlib"}
    statements = _std_statements(std | {"argparse"}, by_name) if "argparse" in by_name else ["import argparse"]
    return (
        '"""Build the qsearch argument parser from the registry. Generated by tools/split_cli/migrate.py."""\n\n'
        "from __future__ import annotations\n\n"
        "import importlib\n" + "\n".join(statements) + "\n\n"
        "from qsearch_cli.registry import ORDER\n\n\n"
        "def build_parser(description: str | None = None, extend=None) -> argparse.ArgumentParser:\n"
        f"{prelude}\n"
        "    for _name, module, adder in ORDER:\n"
        f"        getattr(importlib.import_module(module), adder)({mono.subparsers_var})\n"
        "    if extend is not None:\n"
        f"        extend({mono.subparsers_var})\n"
        f"    return {mono.parser_var}\n"
    )


def _dedent(text: str) -> str:
    return "\n".join(line[4:] if line.startswith("    ") else line for line in text.splitlines())


def render_main(mono: ex.Monolith) -> str:
    by_name = {b.name: b for b in mono.bindings}
    flags = mono.flags_source or "    pass"
    std = _stdlib_used(_dedent(flags), by_name) - {"json", "importlib"}
    extra = "".join(s + "\n" for s in _std_statements(std, by_name))
    var = mono.main_parser_var
    return (
        '"""Add the certificate flags, parse, and run. Generated by tools/split_cli/migrate.py."""\n\n'
        "from __future__ import annotations\n\n"
        "import importlib\nimport json\n" + extra + "\n"
        "from qsearch_cli.registry import DISPATCH\n\n\n"
        f"def add_flags({var}) -> None:\n{flags}\n\n\n"
        f"def run(argv, {var}) -> int:\n"
        f"    add_flags({var})\n"
        f"    args = {var}.parse_args(argv)\n"
        "    for dest, module, function in DISPATCH:\n"
        "        if getattr(args, dest, False):\n"
        "            print(json.dumps(getattr(importlib.import_module(module), function)(), indent=2, sort_keys=True))\n"
        "            return 0\n"
        "    return args.func(args)\n"
    )


INIT = '''"""The qsearch command-line interface, split out of the former 30,000-line qsearch.py.

``qsearch.py`` stays the entry point. It is now a short shim: ``build_parser`` and ``main``
come from here, and any name the old module defined or imported still resolves as
``qsearch.<name>`` the first time it is used.

- ``registry.py``: every subcommand (in --help order), every command function, every flag.
- ``commands/<domain>.py``: the subcommands themselves, one module per research domain.
- ``imports.py``: the names qsearch.py used to import eagerly, now imported on first use.

See tools/split_cli/README.md for how this was generated and how to add a command.
"""
'''

RESOLVE = '''"""Resolve a ``qsearch.<name>`` lookup: a command function or a formerly imported name."""

from __future__ import annotations

import importlib

from qsearch_cli.imports import IMPORTS
from qsearch_cli.registry import FUNCTIONS


def resolve(name: str):
    if name in FUNCTIONS:
        return getattr(importlib.import_module(FUNCTIONS[name]), name)
    if name in IMPORTS:
        module, attr = IMPORTS[name]
        loaded = importlib.import_module(module)
        if attr is None:
            return loaded
        try:
            return getattr(loaded, attr)
        except AttributeError:
            return importlib.import_module(f"{module}.{attr}")
    raise AttributeError(f"module 'qsearch' has no attribute {name!r}")
'''

COMMANDS_INIT = '"""qsearch subcommands, one module per research domain."""\n'

SHIM = '''{docstring}

from __future__ import annotations

import os
import sys

_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
_CORE_DIR = os.path.join(_ROOT_DIR, "core")
_THEOREMS_DIR = os.path.join(_ROOT_DIR, "theorems")

for _p in [_ROOT_DIR, _CORE_DIR, _THEOREMS_DIR]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

# The subcommands live in qsearch_cli/, one module per research domain. Every name this
# file used to import, and every command_* function, still resolves as qsearch.<name>: it
# is imported the first time it is used, so startup no longer loads every theorem module.


def __getattr__(name: str):
    from qsearch_cli.resolve import resolve

    value = resolve(name)
    globals()[name] = value
    return value


def build_parser():
    from qsearch_cli.parser import build_parser as _build_parser

    return _build_parser(description=__doc__, extend=_legacy_extensions)


def main(argv: list[str] | None = None) -> int:
    from qsearch_cli.main import run

    return run(argv, build_parser())


# -----------------------------------------------------------------------------------------
# Old-style additions still work. Put new imports and command_* functions above this
# block, and their add_parser lines inside _legacy_extensions. Running
#     python tools/split_cli/migrate.py sweep --root .
# later moves them into qsearch_cli/. Adding them to qsearch_cli/commands/ directly is
# preferred; see tools/split_cli/README.md.
# -----------------------------------------------------------------------------------------


def _legacy_extensions(subparsers) -> None:
{sentinel}


if __name__ == "__main__":
    sys.modules.setdefault("qsearch", sys.modules["__main__"])
    raise SystemExit(main())
'''


def render_shim(docstring_source: str, trailer: str) -> str:
    text = SHIM.format(docstring=docstring_source, sentinel=LEGACY_SENTINEL)
    return text + (f"\n{trailer}\n" if trailer else "")


def manifest(subcommands: list[dict], functions: dict[str, str], dispatch: list[tuple[str, str, str]],
             imports: int, source_sha: str, dropped: list[str] = ()) -> dict:
    return {
        "generated_by": "tools/split_cli/migrate.py",
        "source_sha256": source_sha,
        "subcommands": subcommands,
        "functions": len(functions),
        "orphan_functions": sorted(set(functions) - {s["function"] for s in subcommands}),
        "flags": [{"dest": d, "module": m, "function": f} for d, m, f in dispatch],
        "imports": imports,
        "dropped_duplicate_definitions": list(dropped),
    }


def plan(mono: ex.Monolith) -> tuple[dict[str, list], list[tuple[str, str, str]], dict[str, str], list[dict]]:
    functions = {c.name: module_of(domain_of(c.name)) for c in mono.commands}
    per_domain: dict[str, list] = {}
    for cmd in mono.commands:
        per_domain.setdefault(domain_of(cmd.name), [[], []])[0].append(cmd)
    order, subs = [], []
    for block in mono.blocks:
        domain = _block_domain(block, functions)
        per_domain.setdefault(domain, [[], []])[1].append(block)
        order.append((block.subcommand, module_of(domain), adder_name(block.subcommand)))
        subs.append({"name": block.subcommand, "aliases": block.aliases, "function": block.function,
                     "module": module_of(domain)})
    return per_domain, order, functions, subs


def write_package(mono: ex.Monolith, root: Path, source: str, shim: bool = False) -> list[Path]:
    per_domain, order, functions, subs = plan(mono)
    pkg = root / PACKAGE
    (pkg / "commands").mkdir(parents=True, exist_ok=True)
    written: dict[Path, str] = {
        pkg / "__init__.py": INIT,
        pkg / "resolve.py": RESOLVE,
        pkg / "commands" / "__init__.py": COMMANDS_INIT,
        pkg / "registry.py": render_registry(order, functions, mono.dispatch),
        pkg / "imports.py": render_imports({b.name: (b.module, b.attr) for b in mono.bindings}),
        pkg / "parser.py": render_parser(mono),
        pkg / "main.py": render_main(mono),
    }
    for domain, (commands, blocks) in sorted(per_domain.items()):
        written[pkg / "commands" / f"{domain}.py"] = render_domain(domain, commands, blocks, mono.bindings, mono.subparsers_var)
    for stale in (pkg / "commands").glob("*.py"):
        if stale not in written:
            stale.unlink()
    sha = hashlib.sha256(source.encode()).hexdigest()
    data = manifest(subs, functions, mono.dispatch, len(mono.bindings), sha, mono.dropped)
    written[root / MANIFEST] = json.dumps(data, indent=1) + "\n"
    if shim:
        written[root / "qsearch.py"] = render_shim(mono.docstring_source, mono.trailer)
    for path, text in written.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return sorted(written)


# ---- sweep: move old-style additions out of the shim -------------------------------------

SHIM_DEFS = {"__getattr__", "build_parser", "main", "_legacy_extensions"}


def _literal(path: Path, name: str):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets):
            return ast.literal_eval(node.value)
    raise ex.SplitError(f"{path}: no {name}")


def sweep(root: Path) -> dict:
    shim_path = root / "qsearch.py"
    source = shim_path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    pkg = root / PACKAGE
    imports = {k: tuple(v) for k, v in _literal(pkg / "imports.py", "IMPORTS").items()}
    order = [tuple(e) for e in _literal(pkg / "registry.py", "ORDER")]
    functions = dict(_literal(pkg / "registry.py", "FUNCTIONS"))
    dispatch = [tuple(e) for e in _literal(pkg / "registry.py", "DISPATCH")]
    new_bindings = ex.bindings_of([n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom))])
    new_bindings = [b for b in new_bindings if b.name not in {"os", "sys"}]
    known = {n: ex.Binding(n, m, a, ex._is_stdlib(m)) for n, (m, a) in imports.items()}
    known.update({b.name: b for b in new_bindings})
    defs = set(functions) | {"main", "build_parser"}
    commands, legacy, trailer, previous_end, docstring_source = [], None, "", 0, ""
    names = ex.function_globals(source)
    new_defs = {n.name for n in tree.body if isinstance(n, ast.FunctionDef) and n.name.startswith("command_")}
    for i, node in enumerate(tree.body):
        if i == 0 and isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant):
            docstring_source = ast.get_source_segment(source, node)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            pass
        elif isinstance(node, ast.Assign) and all(isinstance(t, ast.Name) and t.id in ex.PATH_NAMES for t in node.targets):
            pass
        elif isinstance(node, ast.For):
            pass
        elif isinstance(node, ast.If) and ast.unparse(node.test) == "__name__ == '__main__'":
            trailer = "\n".join(source.splitlines()[node.end_lineno:]).strip("\n")
        elif isinstance(node, ast.FunctionDef) and node.name == "_legacy_extensions":
            legacy = node
        elif isinstance(node, ast.FunctionDef) and node.name in SHIM_DEFS:
            pass
        elif isinstance(node, ast.FunctionDef) and node.name.startswith("command_"):
            cmd = ex.command_from(node, source, previous_end + 1, names.get(node.name, set()), known, defs | new_defs)
            cmd.lazy, cmd.stdlib = sorted(set(cmd.lazy) | set(cmd.stdlib)), []
            commands.append(cmd)
        else:
            raise ex.SplitError(f"qsearch.py line {node.lineno}: unsupported statement {ast.unparse(node)[:80]!r}")
        previous_end = node.end_lineno
    if legacy is None:
        raise ex.SplitError("qsearch.py has no _legacy_extensions; is it the shim?")
    param = legacy.args.args[0].arg
    body = [s for s in legacy.body if not isinstance(s, ast.Pass)]
    blocks = ex.parse_blocks(body, source, param, {}, "_legacy_extensions")
    for cmd in commands:
        functions[cmd.name] = module_of(domain_of(cmd.name))
    pieces: dict[str, list[str]] = {}
    subs = []
    for block in blocks:
        domain = _block_domain(block, functions)
        std = [known[n].statement() for n in sorted(_stdlib_used(_dedent(block.source), known))]
        pieces.setdefault(domain, []).append(render_adder(block, param, std))
        order.append((block.subcommand, module_of(domain), adder_name(block.subcommand)))
        subs.append({"name": block.subcommand, "aliases": block.aliases, "function": block.function,
                     "module": module_of(domain)})
    for cmd in commands:
        pieces.setdefault(domain_of(cmd.name), []).append(render_command(cmd))
    for domain, texts in pieces.items():
        path = pkg / "commands" / f"{domain}.py"
        head = path.read_text(encoding="utf-8").rstrip("\n") if path.exists() else _header(domain, ["import argparse"]).rstrip("\n")
        path.write_text(head + "\n\n\n" + "\n\n\n".join(texts) + "\n", encoding="utf-8")
    for b in new_bindings:
        imports[b.name] = (b.module, b.attr)
    (pkg / "imports.py").write_text(render_imports(imports), encoding="utf-8")
    (pkg / "registry.py").write_text(render_registry(order, functions, dispatch), encoding="utf-8")
    shim_path.write_text(render_shim(docstring_source, trailer), encoding="utf-8")
    manifest_path = root / MANIFEST
    if manifest_path.exists():
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        data["subcommands"] += subs
        data["functions"] = len(functions)
        data["orphan_functions"] = sorted(set(functions) - {s["function"] for s in data["subcommands"]})
        data["imports"] = len(imports)
        manifest_path.write_text(json.dumps(data, indent=1) + "\n", encoding="utf-8")
    return {"commands": [c.name for c in commands], "subcommands": [b.subcommand for b in blocks],
            "imports": [b.name for b in new_bindings]}
