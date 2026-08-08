import math

import numpy as np
import pytest

from self_dual_wreath_mrs_transcript_povm_separation import (
    audit_transcript_povm_separation,
    compile_two_stage_adaptive_transcript_povm,
    run_mrs_transcript_povm_separation,
)


def test_block_scalar_effect_is_exact_transcript_postprocessing() -> None:
    first = np.diag([1.0, 1.0, 0.0, 0.0]).astype(complex)
    second = np.eye(4) - first
    candidate = 0.7 * first + 0.1 * second
    control = audit_transcript_povm_separation(
        "classical",
        (first, second),
        candidate,
    )
    assert control.exact_convex_separation_certificate_verified
    assert control.candidate_in_fixed_transcript_postprocessing_zonotope
    assert control.optimal_postprocessing_coefficients == pytest.approx((0.7, 0.1))
    assert control.hilbert_schmidt_separation_distance < 1e-12


def test_within_block_effect_has_positive_dual_separation_witness() -> None:
    first = np.diag([1.0, 1.0, 0.0, 0.0]).astype(complex)
    second = np.eye(4) - first
    candidate = np.diag([1.0, 0.0, 0.5, 0.5]).astype(complex)
    control = audit_transcript_povm_separation(
        "within",
        (first, second),
        candidate,
    )
    assert control.exact_convex_separation_certificate_verified
    assert not control.candidate_in_fixed_transcript_postprocessing_zonotope
    assert control.optimal_postprocessing_coefficients == pytest.approx((0.5, 0.5))
    assert control.hilbert_schmidt_separation_distance == pytest.approx(math.sqrt(0.5))
    assert control.operator_norm_separation_from_hs_projection == pytest.approx(0.5)
    assert control.dual_witness_support_gap == pytest.approx(math.sqrt(0.5))
    assert control.dual_witness_distance_identity_residual < 1e-12


def test_two_stage_adaptive_transcript_povm_compiles_exactly() -> None:
    kraus = (
        np.diag(np.sqrt([0.8, 0.2])).astype(complex),
        np.diag(np.sqrt([0.2, 0.8])).astype(complex),
    )
    plus = np.asarray([[1.0], [1.0]]) / math.sqrt(2.0)
    minus = np.asarray([[1.0], [-1.0]]) / math.sqrt(2.0)
    x_povm = (plus @ plus.T, minus @ minus.T)
    transcript, control = compile_two_stage_adaptive_transcript_povm(
        kraus,
        (x_povm, x_povm),
    )
    assert control.exact_adaptive_transcript_povm_compilation_verified
    assert len(transcript) == 4
    assert np.linalg.norm(sum(transcript) - np.eye(2), ord=2) < 1e-12


def test_adaptive_real_transcript_cannot_simulate_y_effect() -> None:
    report = run_mrs_transcript_povm_separation()
    adaptive = next(
        row
        for row in report.separation_controls
        if row.control_id == "ADAPTIVE-REAL-TRANSCRIPT-VERSUS-Y-EFFECT"
    )
    assert adaptive.exact_convex_separation_certificate_verified
    assert not adaptive.candidate_in_fixed_transcript_postprocessing_zonotope
    assert adaptive.hilbert_schmidt_separation_distance == pytest.approx(math.sqrt(0.5))
    assert adaptive.extremal_state_decision_probability_difference == pytest.approx(0.5)


def test_report_keeps_full_mrs_and_speedup_gates_closed() -> None:
    report = run_mrs_transcript_povm_separation()
    assert report.claim_gate[
        "exact_fixed_transcript_postprocessing_separation_test_proved"
    ]
    assert report.claim_gate["adaptive_transcript_povm_compilation_proved"]
    assert not report.claim_gate["offdiagonal_coherence_required_for_separation"]
    assert not report.claim_gate[
        "projective_dephasing_test_sufficient_for_general_adaptive_mrs"
    ]
    assert not report.claim_gate["current_physical_pgm_effect_constructed"]
    assert not report.claim_gate[
        "current_physical_pgm_outside_one_fixed_mrs_policy"
    ]
    assert not report.claim_gate[
        "current_physical_pgm_outside_full_mrs_algorithm_class"
    ]
    assert not report.claim_gate["mrs_lower_bound_avoided"]
    assert not report.claim_gate["speedup_claim_allowed"]
