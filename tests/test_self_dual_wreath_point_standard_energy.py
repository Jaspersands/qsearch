from __future__ import annotations

import numpy as np

from self_dual_wreath_joint_character_correlation_decoder import joint_character_state
from self_dual_wreath_point_stabilizer_quotient import point_quotient_states
from self_dual_wreath_point_standard_energy import (
    audit_point_standard_energy,
    point_stabilizer_twirl,
    run_point_standard_energy,
    standard_energy_scaling_record,
    standard_harmonic_projection,
    standard_kronecker_multiplicity,
    validate_standard_kronecker_rule,
)


THRESHOLD_LABELS = (
    ((3,), (2, 1)),
    ((3,), (1, 1, 1)),
    ((2, 1), (1, 1, 1)),
)


def test_standard_kronecker_multiplicity_is_exact_through_s8() -> None:
    for n in range(3, 9):
        control = validate_standard_kronecker_rule(n)
        assert control.mismatch_count == 0
        assert control.maximum_exact_multiplicity == control.maximum_formula_multiplicity
        assert control.exact_standard_kronecker_rule_verified
    assert standard_kronecker_multiplicity((3,), (2, 1)) == 1
    assert standard_kronecker_multiplicity((3,), (1, 1, 1)) == 0
    assert standard_kronecker_multiplicity((2, 1), (2, 1)) == 1


def test_standard_harmonic_projection_is_idempotent_and_stabilizer_selects_delta() -> None:
    state = joint_character_state(THRESHOLD_LABELS, (0, 1, 2))
    projected = standard_harmonic_projection(state, 3, 8)
    assert np.allclose(
        standard_harmonic_projection(projected, 3, 8),
        projected,
        atol=1e-10,
    )
    quotient = point_quotient_states(THRESHOLD_LABELS)
    delta = quotient[0] - sum(quotient) / 3
    assert np.allclose(point_stabilizer_twirl(projected, 3, 8), delta, atol=1e-10)
    np.testing.assert_allclose(
        np.linalg.norm(projected) ** 2,
        2 * np.linalg.norm(delta) ** 2,
        atol=1e-10,
    )


def test_finite_standard_energy_is_positive_young_edge_sum() -> None:
    control = audit_point_standard_energy(
        3,
        THRESHOLD_LABELS,
        control_id="threshold",
    )
    assert control.exact_positive_standard_energy_theorem_verified
    assert control.energy_identity_residual < 1e-10
    assert control.standard_projector_idempotence_residual < 1e-10
    assert control.stabilizer_projection_identity_residual < 1e-10
    assert control.fourier_block_energy_sum_residual < 1e-10
    assert control.maximum_zero_multiplicity_block_energy < 1e-10
    assert control.active_nonstandard_fourier_pair_count > 0
    assert control.offdiagonal_standard_energy > 0


def test_s4_energy_identity_survives_unrelated_collision_free_pair() -> None:
    control = audit_point_standard_energy(
        4,
        (((4,), (3, 1)), ((2, 2), (2, 1, 1))),
        control_id="w4",
    )
    assert control.exact_positive_standard_energy_theorem_verified
    assert control.standard_projection_energy > 0
    assert control.energy_identity_residual < 1e-10
    assert control.maximum_zero_multiplicity_block_energy < 1e-10


def test_scaling_records_do_not_turn_positivity_into_a_lower_bound() -> None:
    record = standard_energy_scaling_record(20)
    assert record.positive_standard_multiplicity_pair_count < record.ordered_irrep_pair_count
    assert record.positive_energy_sum_has_no_sign_cancellation
    assert not record.collision_free_expected_energy_lower_bound_proved
    assert not record.coherent_standard_block_projection_compiled


def test_report_keeps_signal_and_measurement_gates_closed() -> None:
    report = run_point_standard_energy()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["positive_standard_energy_identity_proved"]
    assert report.claim_gate["standard_kronecker_young_edge_rule_proved"]
    assert not report.claim_gate[
        "standard_energy_confined_to_literal_standard_fourier_sector"
    ]
    assert not report.claim_gate[
        "collision_free_standard_energy_lower_bound_proved"
    ]
    assert not report.claim_gate["coherent_standard_block_projection_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]
