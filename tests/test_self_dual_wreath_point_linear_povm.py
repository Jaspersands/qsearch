from __future__ import annotations

import numpy as np
import pytest

from self_dual_wreath_point_linear_povm import (
    audit_linear_point_povm,
    linear_point_effects,
    linear_povm_scaling_record,
    run_point_linear_povm,
)
from self_dual_wreath_point_stabilizer_quotient import point_quotient_states


THRESHOLD_LABELS = (
    ((3,), (2, 1)),
    ((3,), (1, 1, 1)),
    ((2, 1), (1, 1, 1)),
)


def test_linear_effects_are_a_positive_complete_povm() -> None:
    states = point_quotient_states(THRESHOLD_LABELS)
    effects, beta, signal, effective_rank = linear_point_effects(states)
    assert beta > 0
    assert signal > 0
    assert effective_rank >= 1
    assert np.allclose(sum(effects), np.eye(len(states[0])), atol=1e-10)
    assert min(np.linalg.eigvalsh(effect).min() for effect in effects) >= -1e-10


def test_zero_signal_ensemble_is_rejected() -> None:
    state = np.eye(4) / 4
    with pytest.raises(ValueError, match="zero centered signal"):
        linear_point_effects((state, state, state))


def test_linear_success_formula_matches_direct_born_probabilities() -> None:
    for n, labels in (
        (3, (((3,), (2, 1)),)),
        (3, THRESHOLD_LABELS),
        (4, (((4,), (3, 1)), ((2, 2), (2, 1, 1)))),
    ):
        control = audit_linear_point_povm(n, labels, control_id=str(n))
        assert control.exact_linear_point_povm_verified
        assert control.minimum_effect_eigenvalue >= -1e-9
        assert control.povm_completeness_residual < 1e-9
        assert control.linear_success_formula_residual < 1e-9
        assert control.observed_linear_success > control.random_guess_success


def test_linear_measurement_can_beat_pgm_without_claiming_optimality() -> None:
    single = audit_linear_point_povm(
        3,
        (((3,), (2, 1)),),
        control_id="single",
    )
    w4 = audit_linear_point_povm(
        4,
        (((4,), (3, 1)), ((2, 2), (2, 1, 1))),
        control_id="w4",
    )
    assert single.linear_minus_pretty_good_success > 0
    assert w4.linear_minus_pretty_good_success > 0


def test_scaling_contract_exposes_physical_effect_access_gate() -> None:
    record = linear_povm_scaling_record(256)
    assert not record.pgm_average_inverse_required
    assert record.signed_centered_state_access_required
    assert record.operator_norm_estimation_required
    assert not record.coherent_affine_effect_compiler_proved
    assert not record.inverse_polynomial_natural_success_excess_proved


def test_report_records_inverse_free_criterion_without_speedup_claim() -> None:
    report = run_point_linear_povm()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.headline_metrics["linear_beats_pgm_control_count"] >= 2
    assert report.claim_gate["linear_covariant_point_povm_proved"]
    assert not report.claim_gate[
        "pgm_average_inverse_required_for_point_decoding"
    ]
    assert not report.claim_gate["natural_stable_rank_success_bound_proved"]
    assert not report.claim_gate[
        "signed_centered_state_block_encoding_proved"
    ]
    assert not report.claim_gate["coherent_linear_point_measurement_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]
