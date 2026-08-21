import os
import sys

# Ensure both project root and theorems directory are on sys.path
_THEOREMS_DIR = os.path.dirname(os.path.abspath(__file__))
_ROOT_DIR = os.path.dirname(_THEOREMS_DIR)

if _ROOT_DIR not in sys.path:
    sys.path.insert(0, _ROOT_DIR)
if _THEOREMS_DIR not in sys.path:
    sys.path.insert(0, _THEOREMS_DIR)
