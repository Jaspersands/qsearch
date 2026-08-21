import os
import sys

_THEOREMS_DIR = os.path.dirname(os.path.abspath(__file__))
_ROOT_DIR = os.path.dirname(_THEOREMS_DIR)
_CORE_DIR = os.path.join(_ROOT_DIR, "core")

for _p in [_ROOT_DIR, _CORE_DIR, _THEOREMS_DIR]:
    if _p not in sys.path:
        sys.path.insert(0, _p)
