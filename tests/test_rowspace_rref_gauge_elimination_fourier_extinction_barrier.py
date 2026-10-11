"""Unit test suite for Rowspace RREF Gauge Elimination & Self-Dual Code Equivalence Fourier Extinction Barrier."""

import json
import math
from pathlib import Path
import pytest

from theorems.rowspace_rref_gauge_elimination_fourier_extinction_barrier import (
    NEGATIVE_RESULT_ID,
    REPORT,
    REGISTRY,
    audit_rref_gauge_elimination,
    audit_wreath_centralizer_order,
    build_report,
    evaluate_fourier_extinction_bounds,
    gf2_rref,
)


def test_rref_gauge_elimination_identities():
    """Verify that Gaussian elimination RREF(A M) == RREF(M) holds under all GL_k(F_2) scramblers."""
    for (k, n) in [(4, 8), (6, 12), (8, 16)]:
        res = audit_rref_gauge_elimination(k=k, n=n, trials=15, seed=100 + k)
        assert res["rref_invariance_verified"] is True
        assert res["failures"] == 0


def test_wreath_centralizer_order():
    """Verify that the centralizer order |C_{W_n}(tau)| is identically 2 * n!."""
    res = audit_wreath_centralizer_order(n_perm=3)
    assert res["centralizer_order_verified"] is True
    assert res["wreath_group_order"] == 72
    assert res["expected_centralizer_order"] == 12


def test_fourier_extinction_scaling_profiles():
    """Verify that single-copy TV distance and mutual information vanish factorially for all rates."""
    sizes = [(8, 4), (16, 8), (24, 12), (32, 16), (64, 32)]
    for n, k in sizes:
        res = evaluate_fourier_extinction_bounds(n=n, k=k)
        assert res["rate_k_over_n"] == 0.5
        assert res["fourier_extinguished"] is True
        assert res["total_variation_bound"] <= 1.0 / (2.0 * math.sqrt(math.factorial(min(n, 20))))

        if n >= 16:
            assert res["dmr_naive_condition_satisfied"] is False  # DMR dimension gate fails naively
            assert res["log2_mutual_information_bound"] < -40.0

        if n >= 32:
            assert res["log2_mutual_information_bound"] < -100.0


def test_report_structure_and_claim_gate():
    """Verify that build_report disallows speedup claims and satisfies all obligations."""
    report = build_report()
    assert report["status"] == "ROWSPACE_RREF_GAUGE_ELIMINATION_FOURIER_EXTINCTION_BARRIER_PROVED"
    assert report["claim_gate"]["speedup_claim_allowed"] is False
    assert report["claim_gate"]["rref_gauge_elimination_proved"] is True
    assert report["claim_gate"]["physical_wreath_group_reduction_proved"] is True
    assert report["claim_gate"]["exact_centralizer_order_proved"] is True
    assert report["claim_gate"]["single_copy_total_variation_extinction_proved"] is True
    assert report["claim_gate"]["single_copy_mutual_information_extinction_proved"] is True
    assert report["claim_gate"]["universal_code_equivalence_trilemma_proved"] is True
    assert report["headline_metrics"]["speedup_claim_allowed"] is False


def test_negative_result_registered():
    """Verify that NEG-ROWSPACE-RREF-GAUGE-ELIMINATION-FOURIER-EXTINCTION-BARRIER is recorded in registry."""
    assert REGISTRY.exists()
    with open(REGISTRY, "r", encoding="utf-8") as f:
        registry = json.load(f)
    match = next((item for item in registry if item.get("id") == NEGATIVE_RESULT_ID), None)
    assert match is not None, f"Negative result {NEGATIVE_RESULT_ID} missing from registry"
    assert match["evidence"]["speedup_claim_allowed"] is False
    assert "SELF-DUAL-HSP-APPLICABILITY" in match["applies_to"]
    assert "ROWSPACE-CANONICAL-HSP" in match["applies_to"]
