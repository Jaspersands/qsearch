"""Finite control for the exponent-p^e black-box route (research/audits/reviews/
2026-11-09-rees-exponent-pe-blackbox): chart acquisition, kernel readout and Algorithm RtF on
three exported GAP groups of exponent p^e > p (81_3, 243_24, 625_8).  For every exported
subgroup the recovered closure must equal H (ok == subs), and the number of field calls must
never exceed the cap b (calls_max <= cap).  The field solver in the control is the oracle-only
brute force, not Theorem thm:main; this finite check proves nothing for other groups.
"""
import importlib.util
import random
from pathlib import Path

import pytest

pytest.importorskip("sympy")

FOLDER = (Path(__file__).resolve().parents[1] / "research" / "audits" / "reviews"
          / "2026-11-09-rees-exponent-pe-blackbox")


def _load():
    spec = importlib.util.spec_from_file_location("exponent_pe_check", FOLDER / "exponent_pe_check.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def check():
    return _load()


@pytest.mark.parametrize("tag", ["81_3", "243_24", "625_8"])
def test_exponent_pe_group_recovers_every_subgroup(check, tag):
    groups = {g["tag"]: g for g in check.parse_groups(FOLDER / "groups.txt")}
    g = groups[tag]
    assert g["exp"] > g["p"] and g["cls"] < g["p"]
    res = check.run_group(g, random.Random(20261109), log=lambda s: None)
    assert res["subs"] > 0
    assert res["ok"] == res["subs"], res
    assert res["calls_max"] <= res["cap"], res
