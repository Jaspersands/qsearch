"""Tests for General Quantum POVM Secret Variance Collapse & Inaccessible Environment Information Barrier.

Verifies:
1. Exact normalization of subset-sum phase states.
2. Parseval secret variance upper bound across finite dimensions.
3. Shallow-depth zero-information law on local circuits.
4. Total variation and mutual information exponential decay bounds.
5. Fano single-copy secret prediction upper bounds.
6. Report generation, registry integration, and claim gating.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from theorems.dcp_general_povm_secret_variance_collapse import (
    generate_subset_sum_phase_state,
    exact_secret_variance_for_effect,
    verify_parseval_variance_bound_instances,
    verify_shallow_depth_zero_information,
    evaluate_asymptotic_fano_collapse,
    build_report,
    write_report,
    NEGATIVE_RESULT_ID,
    REPORT,
    REGISTRY,
)


def test_phase_state_norm():
    """Verify statevector normalization for subset-sum phase states."""
    a = [3, 7, 5, 2]
    D = 16
    m = 4
    for s in range(D):
        psi = generate_subset_sum_phase_state(a, s, D, m)
        assert abs(np.linalg.norm(psi) - 1.0) < 1e-12


def test_parseval_variance_instances():
    """Verify Parseval secret variance bound across dimensions n in {2, 3, 4}."""
    results = verify_parseval_variance_bound_instances([2, 3, 4], trials_per_n=10)
    for r in results:
        assert r["mean_empirical_variance"] <= r["theoretical_bound"] + 1e-12
        assert abs(r["theoretical_bound"] - (2.0 ** (-2 * r["n_bits"]))) < 1e-12


def test_shallow_depth_zero_information():
    """Verify shallow-depth circuits produce zero transition elements for high-weight relations."""
    res = verify_shallow_depth_zero_information(n=4, depth_bound=1)
    assert res["shallow_depth_coherence_vanishes"]
    assert res["high_weight_vanishing_count"] == res["high_weight_deltas_tested"]


def test_asymptotic_total_variation_bound():
    """Verify total variation bound TV <= (1/2) M 2^{-n}."""
    rows = evaluate_asymptotic_fano_collapse([8, 16, 32, 64])
    for r in rows:
        assert r["total_variation_upper_bound"] <= 0.5 * r["outcome_count_m"] * (2.0 ** (-r["n_bits"])) + 1e-12
        if r["n_bits"] >= 16:
            assert r["total_variation_upper_bound"] < 0.05


def test_asymptotic_mutual_information_bound():
    """Verify mutual information bound I <= (M^2 / ln 2) 2^{-2n}."""
    rows = evaluate_asymptotic_fano_collapse([16, 32, 64])
    for r in rows:
        assert r["mutual_information_upper_bound_bits"] <= 0.001
        assert r["information_exponentially_extinguished"]


def test_fano_success_probability_bound():
    """Verify Fano single-copy success bound P_succ <= (I + 1)/n."""
    rows = evaluate_asymptotic_fano_collapse([8, 16, 32, 64])
    for r in rows:
        assert r["fano_success_probability_upper_bound"] <= (r["mutual_information_upper_bound_bits"] + 1.0) / r["n_bits"] + 1e-12
        assert r["fano_success_probability_upper_bound"] <= 0.2


def test_report_and_registry_integration():
    """Verify report generation, claim gate, and negative results registry update."""
    out_path = write_report(write_registry=True)
    assert out_path.exists()

    report = json.loads(out_path.read_text())
    assert report["status"] == "DCP_GENERAL_POVM_SECRET_VARIANCE_COLLAPSE_PROVED"
    assert report["claim_gate"]["speedup_claim_allowed"] is False
    assert report["claim_gate"]["non_erasure_inaccessible_environment_closed"] is True

    # Registry check
    registry = json.loads(REGISTRY.read_text())
    entry = next((e for e in registry if e["id"] == NEGATIVE_RESULT_ID), None)
    assert entry is not None
    assert "DCP-DENSITY-ONE-SUBSET-SUM-PARTIAL-SOLVER" in entry["applies_to"]
    assert "NON-ERASURE-POVM" in entry["applies_to"]
    assert "INACCESSIBLE-ENVIRONMENT" in entry["applies_to"]
    assert len(entry["lesson"]) > 20
    assert len(entry["reason_invalid"]) > 20
