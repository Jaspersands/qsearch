#!/opt/anaconda3/bin/python
"""Render the would-be numbers.tex from the regenerated JSON WITHOUT running make_numbers.py.

Imports make_numbers' load_map/compute_all/render read-only (as tests/tools/test_rees_paper_numbers.py
does) and writes only research/audits/reviews/2026-11-12-rees-headline-53/numbers.tex.new.
"""
import importlib.util
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PAPER = ROOT / "docs/papers/rees-hsp"
spec = importlib.util.spec_from_file_location("make_rees_numbers_readonly", PAPER / "make_numbers.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
m = mod.load_map()
text = mod.render(mod.compute_all(m, ROOT), m)
(HERE / "numbers.tex.new").write_text(text, encoding="utf-8")
print("wrote", HERE / "numbers.tex.new", len(text.splitlines()), "lines")
