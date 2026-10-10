"""Tests for Native Phase Bank History Entanglement & Classical Dequantization Duality.

Verifies:
1. Finite coherence vanishing across multiple random seeds and parameter choices.
2. Exact classical BKW dequantization (trace distance 0.0).
3. Cauchy-Schwarz noise inflation lower bound ||c||_2 >= n.
4. Scaling trilemma profiles and ISIS exponential hardness.
5. Report generation and registry entry integrity.
"""
from pathlib import Path
import json

import pytest

from theorems.native_history_erasure_dequantization import (
    verify_finite_coherence_vanishing,
    evaluate_scaling_trilemma,
    build_report,
    write_report,
    NEGATIVE_RESULT_ID,
    REPORT,
    REGISTRY,
)


def test_finite_coherence_vanishing_n2():
    """Verify that off-diagonal density matrix elements vanish identically for n=2."""
    res1 = verify_finite_coherence_vanishing(n=2, q=9, M=4, W=4, seed=42)
    assert res1["coherence_vanishes_identically"]
    assert res1["max_off_diagonal_coherence"] == 0.0
    assert abs(res1["density_matrix_trace"] - 1.0) < 1e-12
    assert res1["dequantization_verified"]
    assert res1["trace_distance_to_classical_bkw"] == 0.0
    assert res1["all_paths_satisfy_cauchy_schwarz"]
    assert res1["noise_inflation_lower_bound_satisfied"]

    res2 = verify_finite_coherence_vanishing(n=2, q=9, M=4, W=4, seed=999)
    assert res2["coherence_vanishes_identically"]
    assert res2["max_off_diagonal_coherence"] == 0.0
    assert res2["dequantization_verified"]


def test_finite_coherence_vanishing_n3():
    """Verify that off-diagonal density matrix elements vanish identically for n=3."""
    res = verify_finite_coherence_vanishing(n=3, q=27, M=9, W=3, seed=123)
    assert res["coherence_vanishes_identically"]
    assert res["max_off_diagonal_coherence"] == 0.0
    assert abs(res["density_matrix_trace"] - 1.0) < 1e-12
    assert res["dequantization_verified"]
    assert res["trace_distance_to_classical_bkw"] == 0.0
    assert res["all_paths_satisfy_cauchy_schwarz"]
    assert res["noise_inflation_lower_bound_satisfied"]


def test_cauchy_schwarz_noise_inflation():
    """Verify Cauchy-Schwarz lower bound ||c||_2 >= ||c||_1 / sqrt(M) across instances."""
    for n, q, M, W in [(2, 9, 4, 4), (3, 27, 9, 3)]:
        res = verify_finite_coherence_vanishing(n=n, q=q, M=M, W=W, seed=77)
        assert res["noise_inflation_lower_bound_satisfied"]
        assert res["min_l2_norm_at_max_exposure"] >= res["cauchy_schwarz_l2_bound"] - 1e-12


def test_scaling_trilemma_profiles():
    """Verify asymptotic scaling profiles across all contract dimensions."""
    dims = [2, 3, 4, 8, 16, 32, 64]
    for n in dims:
        p = evaluate_scaling_trilemma(n)
        assert p["dimension"] == n
        assert p["bank_size_M"] == n * n
        assert p["exposure_W"] == n * n
        assert p["secret_trits"] == n * n
        assert p["min_noise_inflation_factor"] == n
        assert p["max_noise_inflation_factor"] == n * n
        assert p["un_erased_state_is_classically_dequantized"]

        if n >= 4:
            assert p["isis_hard_regime"]
            assert p["history_erasure_requires_gapsvp_oracle"]
            assert p["log2_isis_gap"] >= 2.0


def test_report_building_and_integrity():
    """Verify that the generated report meets all theorem requirements."""
    report = build_report()
    assert report["status"] == "NATIVE_HISTORY_ERASURE_DEQUANTIZATION_PROVED"
    assert report["speedup_claim_allowed"] is False
    assert report["accepted_speedup_candidate"] is False
    assert len(report["theorems_proved"]) == 4
    assert all(t["verified"] for t in report["theorems_proved"])
    assert len(report["finite_instance_verifications"]) >= 3
    assert len(report["scaling_profiles"]) == 7


def test_registry_integration():
    """Verify negative result registration in negative_results.json."""
    write_report(write_registry=True)
    assert REPORT.exists()
    assert REGISTRY.exists()

    data = json.loads(REGISTRY.read_text())
    entry = next((e for e in data if e.get("id") == NEGATIVE_RESULT_ID), None)
    assert entry is not None
    assert entry["id"] == NEGATIVE_RESULT_ID
    assert "CYCLOTOMIC-LWE" in entry["applies_to"]
    assert "NATIVE-PHASE-BANK" in entry["applies_to"]
    assert entry["source"] == "research/reductions/native_history_erasure_dequantization.json"
