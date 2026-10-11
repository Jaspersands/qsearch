"""Unit test suite for Dihedral Coset State Chirp Aliasing Barrier & Non-Linear Phase Spectral Flatness Law."""

import json
import math
from pathlib import Path
import pytest

from theorems.dihedral_coset_chirp_aliasing_spectral_flatness_barrier import (
    NEGATIVE_RESULT_ID,
    REPORT,
    REGISTRY,
    audit_cubic_phase_spectral_flatness,
    audit_higher_degree_anti_concentration,
    build_report,
    evaluate_quadratic_gauss_sum,
    evaluate_scaling_chirp_barrier,
)


def test_quadratic_gauss_sum_magnitude():
    """Verify that quadratic Gauss sum has absolute value sqrt(p) for non-zero leading coefficient."""
    for p in [7, 11, 13, 17, 19, 23]:
        for a in [1, 2, 3]:
            g = evaluate_quadratic_gauss_sum(a=a, b=0, c=0, p=p)
            mag = abs(g)
            expected = math.sqrt(p)
            assert abs(mag - expected) < 1e-12, f"Failed at p={p}, a={a}: {mag} != {expected}"


def test_cubic_phase_spectral_flatness():
    """Verify that cubic phase shift differences have identically flat Fourier spectrum |F(k)|^2 == 1/p."""
    for p in [7, 11, 13, 17, 19, 23, 31, 61, 127]:
        res = audit_cubic_phase_spectral_flatness(p=p, s=2)
        assert res["exact_spectral_flatness_verified"] is True
        assert res["maximum_probability_deviation"] < 1e-12
        assert res["single_copy_mutual_information_bits"] == 0.0


def test_dirac_needle_alignment_landscape():
    """Verify that candidate de-chirping alignment function is 1.0 at target and 1/p elsewhere."""
    for p in [7, 11, 13, 17, 19, 23]:
        res = audit_cubic_phase_spectral_flatness(p=p, s=3)
        assert abs(res["peak_at_correct_chirp_rate"] - 1.0) < 1e-12
        assert res["off_target_equals_uniform_floor"] is True
        assert abs(res["maximum_off_target_peak"] - res["expected_uniform_probability"]) < 1e-12


def test_bombieri_weil_higher_degree_anti_concentration():
    """Verify that degree d >= 4 polynomial phases satisfy Bombieri-Weil bound max P(k) <= (d-2)^2 / p."""
    for p in [17, 31, 61, 127]:
        for d in [4, 5]:
            res = audit_higher_degree_anti_concentration(p=p, d=d, s=2)
            assert res["obeys_bombieri_weil_bound"] is True
            assert res["max_probability"] <= res["bombieri_weil_bound"] + 1e-12
            assert res["total_variation_distance"] < 1.0


def test_asymptotic_scaling_profiles():
    """Verify BBBV query bound 2^{n/2} and classical search time 2^n."""
    for n in [8, 16, 32, 64, 128]:
        prof = evaluate_scaling_chirp_barrier(n)
        assert prof["bbbv_quantum_query_lower_bound_log2"] == n / 2.0
        assert prof["classical_search_time_log2"] == float(n)

    # At 64 bits
    prof64 = evaluate_scaling_chirp_barrier(64)
    assert prof64["quantum_query_barrier_exponential"] is True
    assert prof64["mutual_information_collapses_to_zero"] is True
    assert prof64["quartic_phase_single_copy_mi_bits"] < 1.3e-18


def test_report_schema_and_claim_gate():
    """Verify that the generated report passes all claim gates and disallows speedup claims."""
    report = build_report()
    assert report["status"] == "DIHEDRAL_COSET_CHIRP_ALIASING_SPECTRAL_FLATNESS_BARRIER_PROVED"
    assert report["claim_gate"]["speedup_claim_allowed"] is False
    assert report["claim_gate"]["cubic_gauss_spectral_flatness_proved"] is True
    assert report["claim_gate"]["dirac_needle_alignment_landscape_proved"] is True
    assert report["claim_gate"]["bombieri_weil_anti_concentration_proved"] is True
    assert report["claim_gate"]["multi_copy_sieve_decoherence_proved"] is True
    assert report["claim_gate"]["algebraic_phase_trilemma_proved"] is True
    assert report["headline_metrics"]["speedup_claim_allowed"] is False
    assert report["headline_metrics"]["all_cubic_phases_strictly_flat"] is True
    assert report["headline_metrics"]["all_cubic_needle_landscapes_verified"] is True
    assert report["headline_metrics"]["all_higher_degree_phases_obey_bombieri_weil"] is True


def test_negative_result_registry():
    """Verify that NEG-DIHEDRAL-COSET-CHIRP-ALIASING-SPECTRAL-FLATNESS-BARRIER is registered."""
    assert REGISTRY.exists()
    with open(REGISTRY, "r", encoding="utf-8") as f:
        registry = json.load(f)

    entry = next((e for e in registry if e.get("id") == NEGATIVE_RESULT_ID), None)
    assert entry is not None, f"Negative result {NEGATIVE_RESULT_ID} not found in registry"
    assert "HIDDEN-SHIFT-PHASE-FAMILY-GENERATION" in entry["applies_to"]
    assert "DIHEDRAL-COSET-PROBLEM" in entry["applies_to"]
    assert entry["evidence"]["speedup_claim_allowed"] is False
