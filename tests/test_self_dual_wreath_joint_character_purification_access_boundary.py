from __future__ import annotations

import math

import numpy as np
import pytest

from self_dual_wreath_joint_character_correlation_decoder import (
    joint_character_state,
)
from self_dual_wreath_joint_character_purification_access_boundary import (
    audit_joint_purification_access,
    balanced_two_row_irrep_dimension,
    generic_row_rescaling_degree_lower_bound,
    joint_character_purification,
    joint_purification_access_scaling_record,
    run_joint_purification_access_boundary,
    twirled_joint_character_purification,
)


THRESHOLD_LABELS = (
    ((3,), (2, 1)),
    ((3,), (1, 1, 1)),
    ((2, 1), (1, 1, 1)),
)


def test_native_operator_amplitudes_are_an_exact_joint_state_purification() -> None:
    identity = (0, 1, 2)
    purification = joint_character_purification(THRESHOLD_LABELS, identity)
    density = joint_character_state(THRESHOLD_LABELS, identity)
    assert purification.shape == (48, 16)
    np.testing.assert_allclose(
        purification @ purification.conj().T,
        density,
        atol=1e-10,
    )
    assert math.isclose(float(np.trace(density).real), 1.0, abs_tol=1e-10)


def test_coherent_covariant_twirl_purifies_the_exact_average_state() -> None:
    twirled, family = twirled_joint_character_purification(THRESHOLD_LABELS)
    observed = twirled @ twirled.conj().T
    expected = sum(state @ state.conj().T for state in family) / len(family)
    assert twirled.shape == (48, 96)
    np.testing.assert_allclose(observed, expected, atol=1e-10)


def test_schur_rows_expose_D_over_dimension_and_conditioning_does_not_fix_it() -> None:
    control = audit_joint_purification_access(
        3,
        THRESHOLD_LABELS,
        control_id="threshold",
    )
    assert control.exact_purification_schur_normalization_verified
    assert control.active_sector_count == 3
    assert control.maximum_active_irrep_dimension == 2
    assert control.maximum_fourier_row_block_residual < 1e-9
    assert control.maximum_fourier_cross_row_residual < 1e-9
    assert control.maximum_sector_conditioned_row_uniformity_residual < 1e-9
    assert control.minimum_unconditioned_row_probability > 0
    assert control.maximum_generic_row_rescaling_degree_lower_bound == 2


def test_balanced_two_row_irreps_give_an_exponential_generic_rescaling_witness() -> None:
    dimensions = []
    for n in (8, 16, 32, 64):
        partition, dimension = balanced_two_row_irrep_dimension(n)
        assert partition == (n // 2, n // 2)
        assert dimension == math.comb(n, n // 2) // (n // 2 + 1)
        dimensions.append(dimension)
    assert dimensions == [14, 1430, 35357670, 55534064877048198]

    record = joint_purification_access_scaling_record(64)
    assert record.exposed_multiplicity_block == "D_nu/d_nu"
    assert not record.sector_conditioning_removes_row_dilution
    assert int(record.generic_uniform_rescaling_degree_lower_bound_decimal) > 10**16
    assert record.balanced_two_row_dimension_exponential
    assert not record.witness_sector_natural_mass_proved
    assert not record.direct_structured_polar_ruled_out


def test_generic_rescaling_bound_is_linear_and_rejects_invalid_inputs() -> None:
    rows = [generic_row_rescaling_degree_lower_bound(value) for value in (2, 8, 32)]
    assert rows == [2, 7, 26]
    with pytest.raises(ValueError, match="positive"):
        generic_row_rescaling_degree_lower_bound(0)
    with pytest.raises(ValueError, match="error"):
        generic_row_rescaling_degree_lower_bound(2, 0.5)
    with pytest.raises(ValueError, match="even"):
        balanced_two_row_irrep_dimension(7)


def test_report_closes_only_global_density_access() -> None:
    report = run_joint_purification_access_boundary()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["native_joint_purification_proved"]
    assert report.claim_gate["global_average_density_block_encoding_proved"]
    assert report.claim_gate["global_average_block_encoding_has_normalization_one"]
    assert report.claim_gate["global_density_exposes_D_nu_over_d_nu"]
    assert not report.claim_gate["global_density_directly_exposes_D_nu"]
    assert not report.claim_gate["sector_conditioning_removes_schur_row_dilution"]
    assert report.claim_gate["generic_uniform_rescaling_costs_omega_d_nu"]
    assert not report.claim_gate["large_row_sector_natural_information_mass_proved"]
    assert not report.claim_gate["normalization_one_D_nu_block_encoding_proved"]
    assert not report.claim_gate["direct_structured_multiplicity_polar_ruled_out"]
    assert not report.claim_gate["speedup_claim_allowed"]
