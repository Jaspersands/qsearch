from __future__ import annotations

import math

import numpy as np
import pytest

from self_dual_wreath_point_effect_access_boundary import (
    audit_point_effect_access,
    audit_purification_block_encoding,
    bernstein_rescaling_degree_lower_bound,
    point_effect_access_scaling_record,
    purification_projected_unitary,
    run_point_effect_access_boundary,
)


def _cyclic_shift(dimension: int, amount: int) -> np.ndarray:
    matrix = np.zeros((dimension, dimension), dtype=complex)
    for index in range(dimension):
        matrix[(index + amount) % dimension, index] = 1
    return matrix


def test_purification_swap_dilation_has_density_as_exact_top_block() -> None:
    purification = np.asarray(
        [[math.sqrt(0.7), 0], [0, math.sqrt(0.3)]],
        dtype=complex,
    )
    dilation, block, residual = purification_projected_unitary(purification)
    density = purification @ purification.conj().T
    assert np.allclose(block, density, atol=1e-10)
    assert residual < 1e-10
    assert np.allclose(dilation.conj().T @ dilation, np.eye(len(dilation)), atol=1e-10)


def test_twirl_purifications_and_lcu_encode_centered_density() -> None:
    purification = np.asarray(
        [
            [math.sqrt(0.5), 0],
            [0, math.sqrt(0.3)],
            [0, math.sqrt(0.2)],
        ],
        dtype=complex,
    )
    group = tuple(_cyclic_shift(3, amount) for amount in range(3))
    control = audit_purification_block_encoding(
        purification,
        group,
        (0,),
        control_id="cyclic",
    )
    assert control.exact_purification_block_encoding_verified
    assert control.exact_twirl_and_lcu_block_encoding_verified
    assert control.lcu_normalization == 2
    assert control.lcu_centered_block_residual < 1e-10


def test_invalid_purification_and_rescaling_parameters_are_rejected() -> None:
    with pytest.raises(ValueError, match="normalized"):
        purification_projected_unitary(np.eye(2))
    with pytest.raises(ValueError, match="invalid beta"):
        bernstein_rescaling_degree_lower_bound(0, 0.01)
    with pytest.raises(ValueError, match="invalid beta"):
        bernstein_rescaling_degree_lower_bound(0.5, 0.5)


def test_bernstein_lower_bound_scales_inverse_beta() -> None:
    rows = [
        bernstein_rescaling_degree_lower_bound(beta, 0.01)
        for beta in (0.25, 0.125, 0.0625)
    ]
    assert rows[1] >= 2 * rows[0] - 1
    assert rows[2] >= 2 * rows[1] - 1


def test_finite_point_access_charges_beta_normalization() -> None:
    control = audit_point_effect_access(
        4,
        (((4,), (3, 1)), ((2, 2), (2, 1, 1))),
        control_id="w4",
    )
    assert control.centered_operator_norm_beta > 0
    assert control.bernstein_qsvt_degree_lower_bound > 50
    assert control.constant_normalization_centered_block_encoding_proved
    assert not control.inverse_polynomial_beta_proved_for_family
    assert not control.generic_rescaling_polynomial_for_family_proved
    assert not control.complete_n_outcome_naimark_compiler_proved


def test_scaling_contract_is_conditional_and_does_not_rule_out_direct_transform() -> None:
    record = point_effect_access_scaling_record(256)
    assert record.seed_joint_state_purification_schema_polynomial
    assert record.subgroup_and_group_uniform_prepare_polynomial
    assert record.controlled_left_action_polynomial
    assert record.centered_block_encoding_normalization == 2
    assert record.inverse_polynomial_beta_sufficient_for_polynomial_rescaling
    assert not record.inverse_polynomial_beta_proved
    assert not record.representation_specific_rescaling_bypass_ruled_out
    assert not record.end_to_end_point_measurement_compiled


def test_report_records_access_reduction_without_speedup_claim() -> None:
    report = run_point_effect_access_boundary()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["purification_density_block_encoding_proved"]
    assert report.claim_gate["centered_point_effect_block_encoding_proved"]
    assert report.claim_gate["centered_block_encoding_has_constant_normalization"]
    assert report.claim_gate["generic_rescaling_costs_inverse_beta"]
    assert not report.claim_gate["inverse_polynomial_collective_beta_proved"]
    assert not report.claim_gate[
        "complete_covariant_point_naimark_compiled"
    ]
    assert not report.claim_gate[
        "representation_specific_direct_point_transform_ruled_out"
    ]
    assert not report.claim_gate["speedup_claim_allowed"]
