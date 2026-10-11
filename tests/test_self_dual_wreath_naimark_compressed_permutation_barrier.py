"""Unit test suite for Uniform Harmonic Naimark Dilation & Compressed Permutation Multiplicity Obstruction."""

import json
import math
from pathlib import Path
import pytest

from theorems.self_dual_wreath_naimark_compressed_permutation_barrier import (
    NEGATIVE_RESULT_ID,
    REPORT,
    REGISTRY,
    build_report,
    evaluate_scaling_naimark_barrier,
    hook_length_dimension,
    integer_partitions,
    partition_children,
    partition_count_euler,
    verify_point_stabilizer_povm_finite,
    verify_young_branching_reciprocity,
)


def test_euler_partition_counting():
    """Verify Euler's pentagonal number theorem implementation."""
    known_values = {
        0: 1, 1: 1, 2: 2, 3: 3, 4: 5, 5: 7, 6: 11, 7: 15, 8: 22, 9: 30,
        10: 42, 11: 56, 12: 77, 13: 101, 14: 135, 15: 176, 16: 231,
        20: 627, 24: 1575, 32: 8349,
    }
    for n, expected in known_values.items():
        assert partition_count_euler(n) == expected, f"Failed at n={n}"


def test_young_branching_parent_decomposition():
    """Verify sum_{alpha in nu^-} d_alpha == d_nu for all parents in S_3, S_4, S_5, S_6."""
    for n in [3, 4, 5, 6]:
        parents = integer_partitions(n)
        for nu in parents:
            d_nu = hook_length_dimension(nu)
            children = partition_children(nu)
            sum_ch = sum(hook_length_dimension(c) for c in children)
            assert sum_ch == d_nu, f"Parent decomposition failed for n={n}, nu={nu}: {sum_ch} != {d_nu}"


def test_young_branching_child_reciprocity():
    """Verify sum_{nu : alpha in nu^-} d_nu == n * d_alpha for all children in S_3, S_4, S_5, S_6."""
    for n in [3, 4, 5, 6]:
        parents = integer_partitions(n)
        children_all = integer_partitions(n - 1)
        for alpha in children_all:
            d_alpha = hook_length_dimension(alpha)
            covering = [nu for nu in parents if alpha in partition_children(nu)]
            sum_covering = sum(hook_length_dimension(nu) for nu in covering)
            expected = n * d_alpha
            assert sum_covering == expected, f"Child reciprocity failed for n={n}, alpha={alpha}: {sum_covering} != {expected}"


def test_computational_basis_diagonal_invariance():
    """Verify [M_j]_{g, g} == 1/n! identically across all g in S_n and j in {0, ..., n-1}."""
    for n in [3, 4, 5]:
        rec = verify_point_stabilizer_povm_finite(n)
        assert rec["computational_basis_diagonal_exact_constant"] is True
        assert abs(rec["diagonal_matrix_element"] - 1.0 / math.factorial(n)) < 1e-15


def test_conclusive_probability_closed_identity():
    """Verify sum_{j=0}^{n-1} raw_overlap(j) == p(n) / n! identically."""
    for n in [3, 4, 5]:
        rec = verify_point_stabilizer_povm_finite(n)
        assert rec["conclusive_probability_identity_verified"] is True
        expected = partition_count_euler(n) / math.factorial(n)
        assert abs(rec["sum_raw_overlaps_conclusive_probability"] - expected) < 1e-7


def test_physical_bias_bound():
    """Verify that physical bias is bounded by conclusive probability."""
    for n in [3, 4, 5]:
        rec = verify_point_stabilizer_povm_finite(n)
        assert rec["physical_bias_bounded_by_conclusive_prob"] is True
        assert rec["physical_bias"] <= rec["expected_conclusive_probability"] + 1e-7


def test_asymptotic_scaling_profiles():
    """Verify factorial suppression and copy complexity growth for n up to 32."""
    dims = [3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32]
    prev_p = 1.0
    for n in dims:
        prof = evaluate_scaling_naimark_barrier(n)
        assert prof["conclusive_probability"] < prev_p
        prev_p = prof["conclusive_probability"]

    # Check n = 16
    prof16 = evaluate_scaling_naimark_barrier(16)
    assert prof16["conclusive_probability"] < 1.2e-11
    assert prof16["log2_conclusive_probability"] < -36.0
    assert prof16["log2_copies_needed_for_distinction"] > 70.0
    assert prof16["single_copy_mutual_information_upper_bound_bits"] < 1e-20

    # Check n = 32
    prof32 = evaluate_scaling_naimark_barrier(32)
    assert prof32["conclusive_probability"] < 1e-31
    assert prof32["log2_copies_needed_for_distinction"] > 200.0


def test_report_schema_and_claim_gate():
    """Verify that the generated report matches all claim gate requirements."""
    report = build_report()
    assert report["status"] == "SELF_DUAL_WREATH_NAIMARK_COMPRESSED_PERMUTATION_BARRIER_PROVED"
    assert report["claim_gate"]["speedup_claim_allowed"] is False
    assert report["claim_gate"]["young_branching_reciprocity_proved"] is True
    assert report["claim_gate"]["computational_basis_diagonal_invariance_proved"] is True
    assert report["claim_gate"]["conclusive_probability_identity_proved"] is True
    assert report["claim_gate"]["physical_bias_factorial_collapse_proved"] is True
    assert report["claim_gate"]["class_algebra_commutant_invariance_proved"] is True
    assert report["claim_gate"]["universal_trilemma_barrier_proved"] is True
    assert report["headline_metrics"]["speedup_claim_allowed"] is False
    assert report["headline_metrics"]["all_young_branching_dimensions_conserved"] is True


def test_negative_result_registry():
    """Verify that NEG-SELF-DUAL-WREATH-NAIMARK-COMPRESSED-PERMUTATION-BARRIER is properly registered."""
    assert REGISTRY.exists()
    with open(REGISTRY, "r", encoding="utf-8") as f:
        registry = json.load(f)

    entry = next((e for e in registry if e.get("id") == NEGATIVE_RESULT_ID), None)
    assert entry is not None, f"Negative result {NEGATIVE_RESULT_ID} not found in registry"
    assert "CODE-COSET-COLLECTIVE" in entry["applies_to"]
    assert "CODE-EQUIVALENCE-HARD-FAMILY-SEARCH" in entry["applies_to"]
    assert entry["evidence"]["speedup_claim_allowed"] is False
