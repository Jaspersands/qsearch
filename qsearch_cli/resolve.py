"""Resolve a ``qsearch.<name>`` lookup: a command function or a formerly imported name."""

from __future__ import annotations

import importlib

from qsearch_cli.imports import IMPORTS
from qsearch_cli.registry import FUNCTIONS


def known(name: str) -> bool:
    """True for a command function or a name qsearch.py used to import."""
    return name in FUNCTIONS or name in IMPORTS


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
            pass
        if hasattr(loaded, "__path__"):  # ``from package import submodule``
            try:
                return importlib.import_module(f"{module}.{attr}")
            except ModuleNotFoundError as error:
                if error.name != f"{module}.{attr}":
                    raise
        path = getattr(loaded, "__file__", None)
        raise ImportError(f"cannot import name {attr!r} from {module!r} ({path})", name=module, path=path)
    raise AttributeError(f"module 'qsearch' has no attribute {name!r}")
