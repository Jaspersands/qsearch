"""Bind the former qsearch.py globals that old-style code in the shim reads.

A global lookup inside a module never reaches that module's ``__getattr__``. So a
``command_*`` function or an add_parser line written into qsearch.py the old way would get
NameError for ``json``, ``Path``, ``validate_registry`` and every other name the monolith
imported. ``bind`` finds the names that code reads and binds exactly those, as the monolith
did at import. With no old-style code it binds nothing and imports nothing.
"""

from __future__ import annotations

import builtins
import types

# The shim's own functions; they import what they need themselves.
FRAMEWORK = frozenset({"__getattr__", "build_parser", "main"})
_LOADS = frozenset({"LOAD_GLOBAL", "LOAD_NAME", "LOAD_FROM_DICT_OR_GLOBALS"})


def _codes(namespace: dict) -> list[types.CodeType]:
    module = namespace.get("__name__")
    stack = [
        value.__code__
        for name, value in namespace.items()
        if name not in FRAMEWORK and isinstance(value, types.FunctionType) and value.__module__ == module
    ]
    codes = []
    while stack:
        code = stack.pop()
        codes.append(code)
        stack.extend(c for c in code.co_consts if isinstance(c, types.CodeType))
    return codes


def wanted(namespace: dict) -> set[str]:
    """Global names the shim's other functions read that the shim does not define."""
    codes = _codes(namespace)
    names = {n for code in codes for n in code.co_names} - set(namespace) - set(vars(builtins))
    if not names:
        return set()
    import dis  # co_names also holds attribute names; keep only global reads

    return {i.argval for code in codes for i in dis.get_instructions(code) if i.opname in _LOADS and i.argval in names}


def bind(namespace: dict) -> list[str]:
    names = wanted(namespace)
    if not names:
        return []
    from qsearch_cli.resolve import known, resolve

    bound = sorted(n for n in names if known(n))
    for name in bound:
        namespace[name] = resolve(name)
    return bound
