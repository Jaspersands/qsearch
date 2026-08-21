import os
import sys

_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
_THEOREMS_DIR = os.path.join(_ROOT_DIR, "theorems")

if _ROOT_DIR not in sys.path:
    sys.path.insert(0, _ROOT_DIR)
if _THEOREMS_DIR not in sys.path:
    sys.path.insert(0, _THEOREMS_DIR)
