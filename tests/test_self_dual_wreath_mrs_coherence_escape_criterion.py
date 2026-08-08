import numpy as np
import pytest

from self_dual_wreath_mrs_coherence_escape_criterion import (
    audit_transcript_coherence,
    run_mrs_coherence_escape_criterion,
    transcript_classicalize,
    transcript_dephase,
)


def test_transcript_dephasing_removes_only_cross_blocks() -> None:
    matrix = np.arange(16, dtype=float).reshape(4, 4).astype(complex)
    dephased = transcript_dephase(matrix, (1, 2, 1))
    assert np.array_equal(dephased[1:3, 1:3], matrix[1:3, 1:3])
    assert dephased[0, 1] == 0
    assert dephased[2, 3] == 0
    assert dephased[3, 3] == matrix[3, 3]


def test_label_diagonal_effect_is_measured_transcript_simulable() -> None:
    plus = np.asarray([[1.0], [1.0]], dtype=complex) / np.sqrt(2)
    rho = plus @ plus.conj().T
    effect = np.diag([1.0, 0.0]).astype(complex)
    control = audit_transcript_coherence("diagonal", effect, rho, (1, 1))
    assert control.exact_dephasing_identity_verified
    assert control.transcript_measurement_preserves_statistics_for_all_inputs
    assert control.transcript_only_simulation_valid_for_all_inputs
    assert not control.transcript_measurement_changes_statistics
    assert control.decision_probability_difference == pytest.approx(0.0)


def test_hadamard_recombination_is_offdiagonal_witness() -> None:
    plus = np.asarray([[1.0], [1.0]], dtype=complex) / np.sqrt(2)
    rho = plus @ plus.conj().T
    effect = rho.copy()
    control = audit_transcript_coherence("coherent", effect, rho, (1, 1))
    assert control.exact_dephasing_identity_verified
    assert not control.transcript_measurement_preserves_statistics_for_all_inputs
    assert not control.transcript_only_simulation_valid_for_all_inputs
    assert control.transcript_measurement_changes_statistics
    assert control.coherent_decision_probability == pytest.approx(1.0)
    assert control.transcript_dephased_decision_probability == pytest.approx(0.5)


def test_within_block_effect_survives_dephasing_but_is_not_transcript_only() -> None:
    effect = np.diag([1.0, 0.0, 0.5, 0.5]).astype(complex)
    rho = np.diag([1.0, 0.0, 0.0, 0.0]).astype(complex)
    classicalized = transcript_classicalize(effect, (2, 2))
    control = audit_transcript_coherence("within-block", effect, rho, (2, 2))

    assert np.array_equal(classicalized, 0.5 * np.eye(4))
    assert control.decision_effect_dephasing_residual == pytest.approx(0.0)
    assert control.decision_effect_transcript_algebra_residual == pytest.approx(0.5)
    assert control.transcript_measurement_preserves_statistics_for_all_inputs
    assert not control.transcript_only_simulation_valid_for_all_inputs
    assert not control.transcript_measurement_changes_statistics
    assert control.transcript_only_probability_difference == pytest.approx(0.5)


def test_report_keeps_physical_mrs_escape_gate_closed() -> None:
    report = run_mrs_coherence_escape_criterion()
    assert report.headline_metrics[
        "transcript_dephasing_identity_theorem_count"
    ] == 1
    assert report.claim_gate[
        "exact_transcript_dephasing_criterion_proved"
    ]
    assert report.claim_gate[
        "exact_projective_transcript_only_criterion_proved"
    ]
    assert report.claim_gate[
        "offdiagonal_coherence_is_sufficient_not_necessary"
    ]
    assert report.claim_gate[
        "measured_projective_transcript_control_is_classical"
    ]
    assert not report.claim_gate["deferred_measurement_alone_escapes_mrs"]
    assert not report.claim_gate["pair_gpe_alone_proves_mrs_escape"]
    assert report.claim_gate[
        "noncommuting_recoupling_can_create_abstract_witness"
    ]
    assert not report.claim_gate[
        "current_physical_pgm_outside_mrs_transcript_postprocessing"
    ]
    assert not report.claim_gate[
        "complete_recursive_compiler_outside_mrs_class_proved"
    ]
    assert not report.claim_gate["mrs_lower_bound_avoided"]
    assert not report.claim_gate["speedup_claim_allowed"]
