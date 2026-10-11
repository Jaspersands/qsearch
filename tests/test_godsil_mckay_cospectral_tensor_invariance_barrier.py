"""Unit test suite for Godsil-McKay Switching Cospectrality & Rooted Tensor Contraction Invariance Barrier."""

import json
import math
from pathlib import Path
import pytest
import numpy as np

from theorems.godsil_mckay_cospectral_tensor_invariance_barrier import (
    NEGATIVE_RESULT_ID,
    REPORT,
    REGISTRY,
    audit_godsil_mckay_canonical_pair,
    build_godsil_mckay_q_matrix,
    build_report,
    evaluate_asymptotic_scaling,
    rook_graph,
    shrikhande_graph,
)


def test_godsil_mckay_q_matrix_properties():
    """Verify that Godsil-McKay matrix Q is symmetric, orthogonal, involutory, and preserves 1."""
    n = 16
    subset = (0, 5, 10, 15)
    q = build_godsil_mckay_q_matrix(n, subset)

    # 1. Symmetric
    assert np.allclose(q, q.T), "Q is not symmetric"

    # 2. Involutory: Q^2 = I
    assert np.allclose(q @ q, np.eye(n)), "Q^2 is not identity"

    # 3. Orthogonal: Q Q^T = I
    assert np.allclose(q @ q.T, np.eye(n)), "Q is not orthogonal"

    # 4. Preserves all-ones vector: Q 1 = 1
    ones = np.ones(n)
    assert np.allclose(q @ ones, ones), "Q does not preserve all-ones vector"


def test_godsil_mckay_orthogonal_similarity_and_spectrum():
    """Verify that A' = Q A Q identically and adjacency spectra are identical."""
    res = audit_godsil_mckay_canonical_pair()
    assert res["q_orthogonal_similarity_verified"] is True
    assert res["max_qaq_minus_switched_diff"] < 1e-12
    assert res["spectrum_identity_verified"] is True
    assert res["spectrum_max_diff"] < 1e-12


def test_walk_moment_invariance():
    """Verify that Tr((A')^k) == Tr(A^k) identically for all walk lengths k=1..8."""
    res = audit_godsil_mckay_canonical_pair()
    assert res["walk_moments_identical"] is True
    assert res["walk_moments_rook"] == res["walk_moments_switched"]


def test_ctqw_return_probability_identity():
    """Verify that continuous-time quantum walk return probabilities from uniform state match identically."""
    res = audit_godsil_mckay_canonical_pair()
    assert res["ctqw_return_prob_identical"] is True
    assert res["ctqw_max_return_prob_diff"] < 1e-12
    assert res["single_copy_quantum_mutual_information_bits"] == 0.0


def test_classical_neighborhood_topology_separation():
    """Verify that classical neighborhood inspection separates Rook from Shrikhande in O(n d^2) time."""
    res = audit_godsil_mckay_canonical_pair()
    assert res["rook_all_have_two_triangles"] is True
    assert res["switched_all_have_zero_triangles"] is True
    assert res["classically_separated_by_neighborhood_topology"] is True
    assert res["classical_operations_to_separate"] == 240


def test_asymptotic_scaling_metrics():
    """Verify polynomial classical time O(n d^2) vs exponential quantum commutant dimension (n!)^k."""
    sizes = [(16, 6), (36, 10), (64, 14), (100, 18), (256, 30)]
    for n, d in sizes:
        res = evaluate_asymptotic_scaling(n, d)
        expected_ops = n * d * (d - 1) // 2
        assert res["classical_operations"] == expected_ops
        assert res["quantum_strictly_harder_than_classical"] is True
        assert res["three_copy_quantum_commutant_dimension_log2"] > res["log2_classical_operations"]


def test_report_structure_and_claim_gate():
    """Verify that build_report disallows speedup claims and satisfies all obligations."""
    report = build_report()
    assert report["status"] == "GODSIL_MCKAY_COSPECTRAL_TENSOR_INVARIANCE_BARRIER_PROVED"
    assert report["claim_gate"]["speedup_claim_allowed"] is False
    assert report["claim_gate"]["q_orthogonal_similarity_proved"] is True
    assert report["claim_gate"]["spectrum_and_walk_moment_invariance_proved"] is True
    assert report["claim_gate"]["ctqw_return_amplitude_identity_proved"] is True
    assert report["claim_gate"]["classical_neighborhood_topology_subsumption_proved"] is True
    assert report["claim_gate"]["universal_godsil_mckay_trilemma_proved"] is True
    assert report["headline_metrics"]["speedup_claim_allowed"] is False


def test_negative_result_registered():
    """Verify that NEG-GODSIL-MCKAY-COSPECTRAL-TENSOR-INVARIANCE-BARRIER is recorded in registry."""
    assert REGISTRY.exists()
    with open(REGISTRY, "r", encoding="utf-8") as f:
        registry = json.load(f)
    match = next((item for item in registry if item.get("id") == NEGATIVE_RESULT_ID), None)
    assert match is not None, f"Negative result {NEGATIVE_RESULT_ID} missing from registry"
    assert match["evidence"]["speedup_claim_allowed"] is False
    assert "NONABELIAN-COSET-COLLECTIVE-OBSERVABLES" in match["applies_to"]
