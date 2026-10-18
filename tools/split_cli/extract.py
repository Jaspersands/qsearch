"""Read the monolithic qsearch.py into a model that the generator can split.

The extractor accepts only the shapes qsearch.py actually uses: top-level imports, the
sys.path block, ``command_*`` functions, a ``build_parser`` made of add_parser blocks, and a
``main`` that adds certificate flags and dispatches them. Anything else raises SplitError,
so a migration can never silently drop behaviour.
"""

from __future__ import annotations

import ast
import symtable
import sys
from dataclasses import dataclass, field

PATH_NAMES = {"_ROOT_DIR", "_CORE_DIR", "_THEOREMS_DIR"}
FRAMEWORK = {"build_parser", "main"}


class SplitError(Exception):
    """The source has a statement the split cannot move faithfully."""


@dataclass
class Binding:
    name: str
    module: str
    attr: str | None  # None for ``import module``
    stdlib: bool

    def statement(self) -> str:
        if self.attr is None:
            return f"import {self.module}" + (f" as {self.name}" if self.name != self.module else "")
        return f"from {self.module} import {self.attr}" + (f" as {self.name}" if self.name != self.attr else "")


@dataclass
class Command:
    name: str
    source: str           # the def with any comments directly above it
    lazy: list[str]       # names to import from qsearch when the command runs
    stdlib: list[str]     # standard-library names the module must import
    insert_at: int        # line index in ``source`` where the lazy import goes
    indent: str


@dataclass
class Block:
    subcommand: str
    aliases: list[str]
    function: str | None
    source: str           # statements, indented one level
    stdlib: list[str]


@dataclass
class Monolith:
    docstring: str
    bindings: list[Binding]
    commands: list[Command]
    docstring_source: str = ""
    prelude: str = ""             # build_parser statements before the first block
    parser_var: str = "parser"
    subparsers_var: str = "subparsers"
    blocks: list[Block] = field(default_factory=list)
    main_parser_var: str = "parser"
    flags_source: str = ""
    dispatch: list[tuple[str, str, str]] = field(default_factory=list)
    trailer: str = ""
    dropped: list[str] = field(default_factory=list)  # earlier copies of redefined commands


def _is_stdlib(module: str) -> bool:
    return module.split(".")[0] in sys.stdlib_module_names


def bindings_of(nodes: list[ast.stmt]) -> list[Binding]:
    out: dict[str, Binding] = {}
    for node in nodes:
        if isinstance(node, ast.ImportFrom):
            if node.level or node.module == "__future__":
                if node.level:
                    raise SplitError(f"line {node.lineno}: relative import")
                continue
            for alias in node.names:
                if alias.name == "*":
                    raise SplitError(f"line {node.lineno}: star import")
                name = alias.asname or alias.name
                out.pop(name, None)
                out[name] = Binding(name, node.module, alias.name, _is_stdlib(node.module))
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if "." in alias.name and not alias.asname:
                    raise SplitError(f"line {node.lineno}: dotted import {alias.name}")
                name = alias.asname or alias.name
                out.pop(name, None)
                out[name] = Binding(name, alias.name, None, _is_stdlib(alias.name))
    return list(out.values())


def _globals_of(table: symtable.SymbolTable) -> set[str]:
    names = {s.get_name() for s in table.get_symbols() if s.is_global() and s.is_referenced()}
    for child in table.get_children():
        names |= _globals_of(child)
    return names


def function_globals(source: str, filename: str = "qsearch.py") -> dict[str, set[str]]:
    """Module-level names each top-level function reads, nested scopes included."""
    top = symtable.symtable(source, filename, "exec")
    return {t.get_name(): _globals_of(t) for t in top.get_children() if t.get_type() == "function"}


def _lines(source: str, start: int, end: int) -> str:
    return "\n".join(source.splitlines()[start - 1:end])


def _call_on(node: ast.AST, var: str | None = None) -> str | None:
    """Method name if ``node`` is ``<var>.<method>(...)``."""
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
        if var is None or node.func.value.id == var:
            return node.func.attr
    return None


def _classify(names: set[str], bindings: dict[str, Binding], defs: set[str]) -> tuple[list[str], list[str]]:
    lazy = sorted(n for n in names if (n in bindings and not bindings[n].stdlib) or n in defs)
    std = sorted(n for n in names if n in bindings and bindings[n].stdlib)
    return lazy, std


def command_from(node: ast.FunctionDef, source: str, start: int, names: set[str],
                 bindings: dict[str, Binding], defs: set[str]) -> Command:
    if node.decorator_list:
        raise SplitError(f"line {node.lineno}: decorated function {node.name}")
    first = node.body[0]
    if first.lineno == node.lineno:
        raise SplitError(f"line {node.lineno}: one-line function {node.name}")
    has_doc = isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant) and isinstance(first.value.value, str)
    anchor = first.end_lineno + 1 if has_doc else first.lineno
    lines = source.splitlines()[start - 1:node.end_lineno]
    while lines and not lines[0].strip():
        lines.pop(0)
        start += 1
    lazy, std = _classify(names, bindings, defs)
    return Command(node.name, "\n".join(lines), lazy, std, anchor - start, " " * first.col_offset)


def _block_names(stmts: list[ast.stmt]) -> set[str]:
    return {n.id for s in stmts for n in ast.walk(s) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)}


def parse_blocks(stmts: list[ast.stmt], source: str, subparsers: str, bindings: dict[str, Binding],
                 where: str) -> list[Block]:
    blocks: list[Block] = []
    current: list[ast.stmt] = []
    owners: set[str] = set()

    def close() -> None:
        if not current:
            return
        head = current[0].value
        if not head.args or not isinstance(head.args[0], ast.Constant):
            raise SplitError(f"{where}: line {current[0].lineno}: add_parser without a literal name")
        kw = {k.arg: k.value for k in head.keywords}
        aliases = [a.value for a in kw["aliases"].elts] if "aliases" in kw else []
        func = None
        for st in current:
            if _call_on(st.value) == "set_defaults":
                for k in st.value.keywords:
                    if k.arg == "func":
                        if not isinstance(k.value, ast.Name):
                            raise SplitError(f"{where}: line {st.lineno}: func is not a plain name")
                        func = k.value.id
        used = _block_names(current) - owners - {subparsers}
        lazy = [n for n in used if n in bindings and not bindings[n].stdlib]
        if lazy:
            raise SplitError(f"{where}: line {current[0].lineno}: parser block reads imported names {sorted(lazy)}")
        std = sorted(n for n in used if n in bindings and bindings[n].stdlib)
        text = _lines(source, current[0].lineno, current[-1].end_lineno)
        blocks.append(Block(head.args[0].value, aliases, func, text, std))

    for st in stmts:
        if isinstance(st, ast.Assign) and len(st.targets) == 1 and isinstance(st.targets[0], ast.Name) \
                and _call_on(st.value, subparsers) == "add_parser":
            close()
            current = [st]
            owners = {st.targets[0].id}
            continue
        if current and isinstance(st, ast.Expr) and isinstance(st.value, ast.Call) \
                and isinstance(st.value.func, ast.Attribute) and isinstance(st.value.func.value, ast.Name) \
                and st.value.func.value.id in owners and st.value.func.attr in {"add_argument", "set_defaults"}:
            current.append(st)
            continue
        if current and isinstance(st, ast.Assign) and len(st.targets) == 1 and isinstance(st.targets[0], ast.Name) \
                and _call_on(st.value) in {"add_argument_group", "add_mutually_exclusive_group"} \
                and st.value.func.value.id in owners:
            current.append(st)
            owners.add(st.targets[0].id)
            continue
        raise SplitError(f"{where}: line {st.lineno}: unsupported statement {ast.unparse(st)[:80]!r}")
    close()
    return blocks


def _parse_build_parser(node: ast.FunctionDef, source: str, bindings: dict[str, Binding], mono: Monolith) -> None:
    body = node.body
    if not body or not isinstance(body[-1], ast.Return) or not isinstance(body[-1].value, ast.Name):
        raise SplitError("build_parser: must end with `return <parser>`")
    mono.parser_var = body[-1].value.id
    prelude: list[ast.stmt] = []
    index = 0
    for index, st in enumerate(body[:-1]):
        if isinstance(st, ast.Assign) and len(st.targets) == 1 and isinstance(st.targets[0], ast.Name):
            if _call_on(st.value, mono.parser_var) == "add_subparsers":
                mono.subparsers_var = st.targets[0].id
                prelude.append(st)
                continue
            if isinstance(st.value, ast.Call) and ast.unparse(st.value.func) == "argparse.ArgumentParser" \
                    and st.targets[0].id == mono.parser_var:
                prelude.append(st)
                continue
        if isinstance(st, ast.Expr) and _call_on(st.value, mono.parser_var) == "add_argument":
            prelude.append(st)
            continue
        break
    else:
        index = len(body) - 1
    if not prelude or _call_on(prelude[-1].value, mono.parser_var) != "add_subparsers":
        raise SplitError("build_parser: expected a prelude ending in add_subparsers")
    text = _lines(source, prelude[0].lineno, prelude[-1].end_lineno)
    if text.count("__doc__") > 1 or ("__doc__" in text and "description=__doc__" not in text):
        raise SplitError("build_parser: __doc__ used other than as description=__doc__")
    mono.prelude = text
    mono.blocks = parse_blocks(body[index:-1], source, mono.subparsers_var, bindings, "build_parser")


DISPATCH_TEMPLATE = "print(json.dumps({fn}(), indent=2, sort_keys=True))"


def _parse_main(node: ast.FunctionDef, source: str, mono: Monolith) -> None:
    body = list(node.body)

    def fail(st: ast.stmt) -> SplitError:
        return SplitError(f"main: line {st.lineno}: unsupported statement {ast.unparse(st)[:80]!r}")

    first = body.pop(0)
    if not (isinstance(first, ast.Assign) and isinstance(first.value, ast.Call)
            and ast.unparse(first.value) == "build_parser()" and isinstance(first.targets[0], ast.Name)):
        raise fail(first)
    var = first.targets[0].id
    mono.main_parser_var = var
    flags = []
    while body and isinstance(body[0], ast.Expr) and _call_on(body[0].value, var) == "add_argument":
        flags.append(body.pop(0))
    if flags:
        mono.flags_source = _lines(source, flags[0].lineno, flags[-1].end_lineno)
    if not body or ast.unparse(body[0]) != f"args = {var}.parse_args(argv)":
        raise fail(body[0] if body else node)
    body.pop(0)
    while body and isinstance(body[0], ast.If):
        st = body.pop(0)
        test = ast.unparse(st.test)
        ok = len(st.body) == 3 and not st.orelse and test.startswith("getattr(args, ") and test.endswith(", False)")
        if ok:
            imp, call, ret = st.body
            ok = (isinstance(imp, ast.ImportFrom) and len(imp.names) == 1 and not imp.names[0].asname
                  and ast.unparse(call) == DISPATCH_TEMPLATE.format(fn=imp.names[0].name)
                  and ast.unparse(ret) == "return 0" and isinstance(st.test.args[1], ast.Constant))
        if not ok:
            raise fail(st)
        mono.dispatch.append((st.test.args[1].value, imp.module, imp.names[0].name))
    if len(body) != 1 or ast.unparse(body[0]) != "return args.func(args)":
        raise fail(body[0] if body else node)


def extract(source: str) -> Monolith:
    tree = ast.parse(source)
    bindings = bindings_of(tree.body)
    by_name = {b.name: b for b in bindings}
    defs = {n.name for n in tree.body if isinstance(n, ast.FunctionDef)}
    names = function_globals(source)
    mono = Monolith(ast.get_docstring(tree, clean=False) or "", bindings, [])
    previous_end = 0
    for i, node in enumerate(tree.body):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            pass
        elif i == 0 and isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant):
            mono.docstring_source = ast.get_source_segment(source, node)
        elif isinstance(node, ast.Assign) and all(isinstance(t, ast.Name) and t.id in PATH_NAMES for t in node.targets):
            pass
        elif isinstance(node, ast.For) and ast.unparse(node.iter) == "[_ROOT_DIR, _CORE_DIR, _THEOREMS_DIR]":
            pass
        elif isinstance(node, ast.If) and ast.unparse(node.test) == "__name__ == '__main__'":
            mono.trailer = "\n".join(source.splitlines()[node.end_lineno:]).strip("\n")
        elif isinstance(node, ast.FunctionDef) and node.name == "build_parser":
            _parse_build_parser(node, source, by_name, mono)
        elif isinstance(node, ast.FunctionDef) and node.name == "main":
            _parse_main(node, source, mono)
        elif isinstance(node, ast.FunctionDef) and node.name.startswith("command_"):
            mono.commands.append(command_from(node, source, previous_end + 1, names.get(node.name, set()), by_name, defs))
        else:
            raise SplitError(f"line {node.lineno}: unsupported top-level statement {ast.unparse(node)[:80]!r}")
        previous_end = node.end_lineno
    last = {c.name: i for i, c in enumerate(mono.commands)}
    mono.dropped = [c.name for i, c in enumerate(mono.commands) if last[c.name] != i]
    mono.commands = [c for i, c in enumerate(mono.commands) if last[c.name] == i]
    known = set(last)
    for block in mono.blocks:
        if block.function is not None and block.function not in known and block.function not in by_name:
            raise SplitError(f"build_parser: {block.subcommand} points at undefined {block.function}")
    return mono
