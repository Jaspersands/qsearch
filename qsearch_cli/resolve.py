"""Resolve a ``qsearch.<name>`` lookup: a command function or a formerly imported name."""

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
