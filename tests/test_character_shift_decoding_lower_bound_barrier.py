"""Tests for Uniform Character-Shift Decoding Lower Bound & Weil-Chernoff Query-Time Separation.

Verifies:
1. Exact Legendre autocorrelation identity sum == -1.
2. Closed-form pairwise agreement count N_agree == (p - 3) / 2.
3. Agreement fraction strictly below 0.5.
4. Chernoff-union bound logarithmic query ceilings k* = 2 ceil(log2 p).
5. Empirical random-sample identification success rates.
6. Cyclotomic equation degree obstruction d = (p - 1)/2.
7. Report generation, registry integration, and claim gating.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from theorems.character_shift_decoding_lower_bound_barrier import (
    legendre_symbol,
    verify_exact_autocorrelation_identity,
    verify_exact_pairwise_agreement_counts,
    evaluate_union_bound_query_ceilings,
    simulate_random_sample_shift_identification,
    evaluate_cyclotomic_degree_obstruction,
    evaluate_preprocessing_dichotomy,
    build_report,
    write_report,
    NEGATIVE_RESULT_ID,
    REPORT,
    REGISTRY,
)


def test_legendre_symbol_values():
    """Verify Legendre symbol values on known small residues."""
    assert legendre_symbol(0, 5) == 0
    assert legendre_symbol(1, 5) == 1
    assert legendre_symbol(2, 5) == -1
    assert legendre_symbol(3, 5) == -1
    assert legendre_symbol(4, 5) == 1

    assert legendre_symbol(1, 7) == 1
    assert legendre_symbol(2, 7) == 1
    assert legendre_symbol(3, 7) == -1
    assert legendre_symbol(4, 7) == 1
    assert legendre_symbol(5, 7) == -1
    assert legendre_symbol(6, 7) == -1


def test_autocorrelation_identity_all_primes():
    """Verify that sum chi(x) chi(x + delta) == -1 for all delta != 0 across test primes."""
    for p in (5, 7, 11, 13, 17, 19, 23, 29, 31):
        res = verify_exact_autocorrelation_identity(p)
        assert res["all_exact_neg_one"]
        assert res["max_residual"] == 0
        assert res["distinct_sum_values"] == [-1]


def test_closed_form_agreement_counts():
    """Verify N_agree == (p - 3) // 2 and N_disagree == (p - 1) // 2."""
    for p in (5, 7, 11, 13, 17, 19, 23, 29, 31):
        res = verify_exact_pairwise_agreement_counts(p)
        assert res["all_matched"]
        assert res["expected_agree"] == (p - 3) // 2
        assert res["expected_disagree"] == (p - 1) // 2
        assert res["fraction_strictly_sub_half"]


def test_agreement_fraction_sub_half():
    """Verify agreement fraction is strictly bounded away from 0.5 as required by Chernoff."""
    for p in (5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61):
        frac = (p - 3) / (2 * p)
        assert frac < 0.5
        assert abs(frac - (0.5 - (1.5 / p))) < 1e-14


def test_union_bound_query_ceilings():
    """Verify that k*(p) = 2 ceil(log2 p) queries guarantees failure bound <= 1/p."""
    rows = evaluate_union_bound_query_ceilings([5, 7, 11, 13, 17, 19, 23, 29, 31, 47, 61])
    for r in rows:
        assert r["failure_bound_below_one_over_p"]
        assert r["query_to_log2p_ratio"] <= 2.8


def test_simulation_shift_recovery():
    """Verify empirical random-sample shift recovery simulation."""
    for p in (11, 17, 23, 31):
        res = simulate_random_sample_shift_identification(p, true_shift=7, trials=30)
        assert res["unique_identification_rate"] >= 0.90


def test_cyclotomic_degree_obstruction():
    """Verify that equation degree d = (p - 1)/2 is exponential in bit-length."""
    rows = evaluate_cyclotomic_degree_obstruction([7, 11, 17, 31, 61])
    for r in rows:
        assert r["degree_exponential_in_n"]
        assert r["cyclotomic_equation_degree"] == (r["prime"] - 1) // 2


def test_preprocessing_dichotomy():
    """Verify non-uniform advice size vs uniform work requirements."""
    rows = evaluate_preprocessing_dichotomy([7, 11, 17, 31, 61])
    for r in rows:
        assert r["uniform_work_exponential"]
        assert r["non_uniform_advice_bits"] == r["prime"] * r["n_bits"]


def test_report_and_registry_integration(tmp_path, monkeypatch):
    """Verify report generation, claim gate, and negative results registry update."""
    # Write into a copy of the repo layout so the live report and registry stay untouched.
    import shutil
    import theorems.character_shift_decoding_lower_bound_barrier as module
    for name in ("DERIVATION", "REPORT", "REGISTRY"):
        live = getattr(module, name)
        copy = tmp_path / live.relative_to(module.ROOT)
        copy.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(live, copy)
        monkeypatch.setattr(module, name, copy)
    monkeypatch.setattr(module, "ROOT", tmp_path)
    registry_copy = module.REGISTRY
    out_path = write_report(write_registry=True)
    assert out_path.exists()

    report = json.loads(out_path.read_text())
    assert report["status"] == "CHARACTER_SHIFT_UNIFORM_DECODING_LOWER_BOUND_PROVED"
    assert report["claim_gate"]["speedup_claim_allowed"] is False
    assert report["claim_gate"]["classical_decoding_hardness_verified"] is True

    # Registry check
    registry = json.loads(registry_copy.read_text())
    entry = next((e for e in registry if e["id"] == NEGATIVE_RESULT_ID), None)
    assert entry is not None
    assert "CHARACTER-SHIFT-DECODING-LOWER-BOUND" in entry["applies_to"]
    assert "LEGENDRE-PRG-INVERSION" in entry["applies_to"]
    assert len(entry["lesson"]) > 20
    assert len(entry["reason_invalid"]) > 20
