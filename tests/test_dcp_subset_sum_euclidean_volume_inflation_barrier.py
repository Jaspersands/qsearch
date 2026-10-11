"""Unit test suite for Density-One Modular Subset-Sum Euclidean Volume Inflation & BDD Multiplicity Barrier."""

import json
import math
from pathlib import Path
import pytest

from theorems.dcp_subset_sum_euclidean_volume_inflation_barrier import (
    NEGATIVE_RESULT_ID,
    REPORT,
    REGISTRY,
    audit_finite_density_one_geometry,
    build_report,
    compute_ball_volume_log2,
    compute_expected_lattice_points_log2,
    evaluate_density_one_scaling,
)


def test_ball_volume_log2_and_stirling_convergence():
    """Verify that exact ball volume converges to Stirling asymptotic formula within O(1/n)."""
    for n in [10, 16, 20, 30, 50, 100]:
        radius = math.sqrt(n)
        exact_log2 = compute_ball_volume_log2(n, radius)
        asymptotic_log2 = 0.5 * n * math.log2(2.0 * math.pi * math.e) - 0.5 * math.log2(math.pi * n)
        diff = abs(exact_log2 - asymptotic_log2)
        assert diff < 0.2, f"Stirling discrepancy too large at n={n}: {diff}"


def test_expected_lattice_points_exponential_growth():
    """Verify that expected integer lattice points in ball B_n(sqrt(n)) grows as 2^{Omega(n)}."""
    sizes = [16, 20, 30, 40, 50]
    for n in sizes:
        log2_pts = compute_expected_lattice_points_log2(n, math.sqrt(n), float(n))
        assert log2_pts > 0
        rate = log2_pts / n
        assert rate > 0.8, f"Point multiplicity rate too low at n={n}: {rate}"

    # Specific reference values
    assert abs(compute_expected_lattice_points_log2(16, 4.0, 16.0) - 13.91) < 0.1
    assert abs(compute_expected_lattice_points_log2(30, math.sqrt(30), 30.0) - 28.13) < 0.1
    assert abs(compute_expected_lattice_points_log2(50, math.sqrt(50), 50.0) - 48.70) < 0.1


def test_finite_audit_16_geometry():
    """Verify that binary witness lies 4 times outside unique BDD decoding radius."""
    res = audit_finite_density_one_geometry(n=16)
    assert res["witness_outside_bdd_radius"] is True
    assert res["witness_norm_to_bdd_radius_ratio"] > 4.0
    assert abs(res["witness_norm_to_bdd_radius_ratio"] - math.sqrt(2 * math.pi * math.e)) < 1e-3


def test_scaling_profiles_exponential_undercoverage():
    """Verify that polynomial list decoders L = n^3 achieve only 2^{-Omega(n)} coverage for n >= 16."""
    sizes = [16, 24, 30, 40, 50, 64, 100]
    for n in sizes:
        res = evaluate_density_one_scaling(n)
        assert res["exponentially_undercovered"] is True
        assert res["log2_poly_list_coverage_n3"] < 0

        if n >= 30:
            assert res["log2_poly_list_coverage_n3"] < -10.0
        if n >= 50:
            assert res["log2_poly_list_coverage_n3"] < -30.0


def test_report_structure_and_claim_gate():
    """Verify that build_report disallows speedup claims and satisfies all obligations."""
    report = build_report()
    assert report["status"] == "DCP_SUBSET_SUM_EUCLIDEAN_VOLUME_INFLATION_BARRIER_PROVED"
    assert report["claim_gate"]["speedup_claim_allowed"] is False
    assert report["claim_gate"]["euclidean_ball_volume_inflation_proved"] is True
    assert report["claim_gate"]["expected_lattice_point_exponential_multiplicity_proved"] is True
    assert report["claim_gate"]["bdd_radius_collapse_proved"] is True
    assert report["claim_gate"]["polynomial_list_exponential_undercoverage_proved"] is True
    assert report["claim_gate"]["universal_subset_sum_lattice_trilemma_proved"] is True
    assert report["headline_metrics"]["speedup_claim_allowed"] is False


def test_negative_result_registered():
    """Verify that NEG-DCP-SUBSET-SUM-EUCLIDEAN-VOLUME-INFLATION-BARRIER is recorded in registry."""
    assert REGISTRY.exists()
    with open(REGISTRY, "r", encoding="utf-8") as f:
        registry = json.load(f)
    match = next((item for item in registry if item.get("id") == NEGATIVE_RESULT_ID), None)
    assert match is not None, f"Negative result {NEGATIVE_RESULT_ID} missing from registry"
    assert match["evidence"]["speedup_claim_allowed"] is False
    assert "DCP-DENSITY-ONE-SUBSET-SUM-PARTIAL-SOLVER" in match["applies_to"]
