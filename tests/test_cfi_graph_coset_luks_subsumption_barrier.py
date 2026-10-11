"""Unit test suite for Cai-Fürer-Immerman (CFI) Graph Coset Trilemma & Bounded-Valence Luks Classical Subsumption Barrier."""

import json
import math
from pathlib import Path
import pytest

from theorems.cfi_graph_coset_luks_subsumption_barrier import (
    NEGATIVE_RESULT_ID,
    REPORT,
    REGISTRY,
    audit_finite_cfi_base,
    build_report,
    evaluate_scaling_cfi_luks_barrier,
)


def test_finite_base_cfi_invariants():
    """Verify that finite 3-regular base graphs satisfy N_CFI == 7|V| and max degree <= 4."""
    cubic_bases = [
        "triangular-prism",
        "cube-q3",
        "mobius-ladder-8",
        "petersen",
        "heawood-like-14",
    ]
    for b_id in cubic_bases:
        res = audit_finite_cfi_base(b_id)
        assert res["is_3_regular"] is True
        assert res["vertex_count_identity_verified"] is True
        assert res["cfi_vertex_count"] == 7 * res["base_vertex_count"]
        assert res["cfi_edge_count"] == 12 * res["base_vertex_count"]
        assert res["cfi_max_degree"] <= 4
        assert res["degree_bounded_by_four"] is True
        assert res["classical_subsumption_status"] == "solvable_in_polynomial_time_by_luks_1982"


def test_cycle_space_automorphism_lower_bounds():
    """Verify cycle space dimension beta_1 = |V|/2 + 1 and normal 2-subgroup order."""
    cubic_bases = [
        "triangular-prism",
        "cube-q3",
        "mobius-ladder-8",
        "petersen",
        "heawood-like-14",
    ]
    for b_id in cubic_bases:
        res = audit_finite_cfi_base(b_id)
        n = res["base_vertex_count"]
        expected_beta_1 = (n // 2) + 1
        assert res["betti_number_beta_1"] == expected_beta_1
        assert res["cycle_space_automorphism_order_bound"] == (1 << expected_beta_1)


def test_scaling_cfi_luks_barrier():
    """Verify Luks polynomial time O(N^4) vs exponential quantum commutant scaling."""
    sizes = [6, 10, 20, 50, 100, 200]
    for v in sizes:
        res = evaluate_scaling_cfi_luks_barrier(v)
        n_cfi = 7 * v
        assert res["cfi_vertex_count"] == n_cfi
        assert res["max_degree"] == 4
        expected_luks_log2 = 4.0 * math.log2(n_cfi)
        assert abs(res["luks_classical_time_log2"] - expected_luks_log2) < 1e-3
        assert res["quantum_strictly_harder_than_classical"] is True
        assert res["three_copy_quantum_commutant_dimension_log2"] > res["luks_classical_time_log2"]


def test_report_structure_and_claim_gate():
    """Verify that build_report strictly disallows speedup claims."""
    report = build_report()
    assert report["status"] == "CFI_GRAPH_COSET_LUKS_SUBSUMPTION_BARRIER_PROVED"
    assert report["claim_gate"]["speedup_claim_allowed"] is False
    assert report["claim_gate"]["exact_7v_cfi_vertex_identity_proved"] is True
    assert report["claim_gate"]["max_degree_four_bounded_valence_proved"] is True
    assert report["claim_gate"]["luks_classical_polynomial_subsumption_certified"] is True
    assert report["claim_gate"]["universal_cfi_trilemma_barrier_proved"] is True
    assert report["headline_metrics"]["speedup_claim_allowed"] is False


def test_negative_result_registered():
    """Verify that NEG-CFI-GRAPH-COSET-LUKS-SUBSUMPTION-BARRIER is recorded in the registry."""
    assert REGISTRY.exists()
    with open(REGISTRY, "r", encoding="utf-8") as f:
        registry = json.load(f)
    match = next((item for item in registry if item.get("id") == NEGATIVE_RESULT_ID), None)
    assert match is not None, f"Negative result {NEGATIVE_RESULT_ID} missing from registry"
    assert match["evidence"]["speedup_claim_allowed"] is False
    assert "BOUNDED-VALENCE-LUKS-SUBSUMPTION" in match["applies_to"]
