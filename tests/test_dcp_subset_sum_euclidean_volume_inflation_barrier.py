"""Unit test suite for Density-One Modular Subset-Sum Euclidean Volume Inflation & BDD Multiplicity Barrier."""

import json
import math
from pathlib import Path
import pytest

from theorems.dcp_subset_sum_euclidean_volume_inflation_barrier import (
    NEGATIVE_RESULT_ID,
    QUARANTINED_REGISTRY,
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
    """Verify that continuous heuristic volume/det ratio in ball B_n(sqrt(n)) grows as 2^{Omega(n)}."""
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
    """Verify uncentered heuristic radius ratio calculation at n=16."""
    res = audit_finite_density_one_geometry(n=16)
    assert res["witness_outside_bdd_radius"] is True
    assert res["witness_norm_to_bdd_radius_ratio"] > 4.0
    assert abs(res["witness_norm_to_bdd_radius_ratio"] - math.sqrt(2 * math.pi * math.e)) < 1e-3


def test_scaling_profiles_exponential_undercoverage():
    """Verify uncentered continuous volume ratio scaling profiles for n >= 16."""
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
    """Verify that build_report disallows speedup claims and records the 2026-11-06 retraction."""
    report = build_report()
    assert report["status"] == "UNIVERSAL_SUBSET_SUM_VOLUME_BARRIER_RETRACTED_BALL_VOLUME_FORMULA_ONLY"
    assert report["claim_gate"]["speedup_claim_allowed"] is False
    assert report["claim_gate"]["euclidean_ball_volume_inflation_proved"] is True
    assert report["claim_gate"]["expected_lattice_point_exponential_multiplicity_proved"] is False
    assert report["claim_gate"]["bdd_radius_collapse_proved"] is False
    assert report["claim_gate"]["polynomial_list_exponential_undercoverage_proved"] is False
    assert report["claim_gate"]["universal_subset_sum_lattice_trilemma_proved"] is False
    assert report["claim_gate"]["universal_exclusion_retracted_2026_11_06"] is True
    assert report["headline_metrics"]["speedup_claim_allowed"] is False


def test_negative_result_quarantined():
    """Verify that NEG-DCP-SUBSET-SUM-EUCLIDEAN-VOLUME-INFLATION-BARRIER is quarantined and not active."""
    assert REGISTRY.exists()
    with open(REGISTRY, "r", encoding="utf-8") as f:
        registry = json.load(f)
    assert all(item.get("id") != NEGATIVE_RESULT_ID for item in registry)

    assert QUARANTINED_REGISTRY.exists()
    with open(QUARANTINED_REGISTRY, "r", encoding="utf-8") as f:
        quarantined = json.load(f)
    match = next((item for item in quarantined if item.get("id") == NEGATIVE_RESULT_ID), None)
    assert match is not None, f"Negative result {NEGATIVE_RESULT_ID} missing from quarantined registry"
    assert match["status"] == "QUARANTINED_OVERBROAD_NO_GO"
    assert match["review"] == "research/DCP_HALF_CENTER_DGS_ADMISSION.md"
