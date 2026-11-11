"""Tests for the p = 5, d = 3 label-set SAT encoder, LRAT certification, and brute-force equivalence."""

from __future__ import annotations

import importlib.util
import os
import random
import shutil
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
LABELSAT_PATH = ROOT / "research" / "audits" / "reviews" / "2026-11-11-rees-sde-p5-d3" / "labelsat.py"


def _load_labelsat():
    spec = importlib.util.spec_from_file_location("labelsat", LABELSAT_PATH)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _has_cadical(mod) -> bool:
    return shutil.which(mod.CADICAL) is not None or (os.path.isfile(mod.CADICAL) and os.access(mod.CADICAL, os.X_OK))


def _full_gamma(gamma_reps: dict[tuple[int, ...], tuple[int, ...]], p: int) -> dict[tuple[int, ...], tuple[int, ...]]:
    full = dict(gamma_reps)
    for a, g in gamma_reps.items():
        full.setdefault(tuple((p - x) % p for x in a), tuple((p - x) % p for x in g))
    return full


def test_f5_d2_full_sat_and_f7_d2_unsat_verified(tmp_path: Path) -> None:
    mod = _load_labelsat()
    if not _has_cadical(mod):
        pytest.skip("cadical not available")
    lrat_bin = Path(mod.LRATCHECK)
    if not (lrat_bin.is_file() and os.access(lrat_bin, os.X_OK)):
        pytest.skip(f"fixed lrat-check not available at {lrat_bin}")

    L5 = mod.nonzero(5, 2)
    res_sat = mod.solve(L5, p=5, d=2, S=(0, 1, 4), workdir=str(tmp_path), tag="f5_d2_full")
    assert res_sat["status"] == "SAT"
    # solve(..., use_R=True) slices res["gamma"] to +-pair reps; check_model expects all alpha.
    gamma_full = _full_gamma(res_sat["gamma"], 5)
    ok, msg = mod.check_model(L5, res_sat["Phi"], gamma_full, 5, 2, (0, 1, 4))
    assert (ok, msg) == (True, "ok")

    L7 = mod.nonzero(7, 2)
    res_unsat = mod.solve(L7, p=7, d=2, S=(0, 1, 6), workdir=str(tmp_path), tag="f7_d2_full")
    assert res_unsat["status"] == "UNSAT_VERIFIED"
    assert "c VERIFIED" in res_unsat["lrat_out"]


def test_labelsat_solve_matches_brute_on_ten_random_small_cases(tmp_path: Path) -> None:
    mod = _load_labelsat()
    if not _has_cadical(mod):
        pytest.skip("cadical not available")
    lrat_bin = Path(mod.LRATCHECK)
    if not (lrat_bin.is_file() and os.access(lrat_bin, os.X_OK)):
        pytest.skip(f"fixed lrat-check not available at {lrat_bin}")

    rng = random.Random(20261111)
    specs = [
        (5, 2, (0, 1, 4), 3, True, True),
        (5, 2, (0, 1, 4), 4, True, False),
        (7, 1, (0, 1, 6), 4, True, True),
        (7, 1, (0, 1, 6), 6, True, True),
        (3, 2, (0, 1), 4, False, True),
        (3, 2, (0, 1), 5, False, False),
        (3, 2, (0, 1), 6, False, True),
        (5, 2, (0, 1), 4, False, False),
        (5, 2, (0, 1), 5, False, True),
        (7, 1, (0, 1), 5, False, True),
    ]

    sat_count = 0
    unsat_count = 0
    for idx, (p, d, S, k, use_R, use_N) in enumerate(specs):
        nz = mod.nonzero(p, d)
        while True:
            L = sorted(rng.sample(nz, k))
            if mod.rank(L, p, d) == d:
                break
        expected_sat = mod.brute(L, p, d, S)
        res = mod.solve(L, p=p, d=d, S=S, use_R=use_R, use_N=use_N, workdir=str(tmp_path), tag=f"rnd_{idx}")
        if expected_sat:
            sat_count += 1
            assert res["status"] == "SAT"
            gamma_full = _full_gamma(res["gamma"], p) if use_R else res["gamma"]
            ok, msg = mod.check_model(L, res["Phi"], gamma_full, p, d, S)
            assert (ok, msg) == (True, "ok")
        else:
            unsat_count += 1
            assert res["status"] == "UNSAT_VERIFIED"
            assert "c VERIFIED" in res["lrat_out"]

    assert sat_count >= 3 and unsat_count >= 3
