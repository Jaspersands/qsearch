from __future__ import annotations

import numpy as np
import pytest

from self_dual_wreath_joint_character_analysis_map_normalization import (
    audit_joint_analysis_map,
    canonical_projector_erasure_map,
    generic_analysis_amplification_degree_lower_bound,
    joint_analysis_map_scaling_record,
    joint_character_analysis_maps,
    run_joint_analysis_map_normalization,
)
from self_dual_wreath_joint_character_multiplicity_gram import (
    predicted_joint_multiplicity_operator,
)


THRESHOLD_LABELS = (
    ((3,), (2, 1)),
    ((3,), (1, 1, 1)),
    ((2, 1), (1, 1, 1)),
)


def test_rectangular_analysis_factor_has_exact_joint_multiplicity_gram() -> None:
    multiplicity, target, canonical, circuit = joint_character_analysis_maps(
        (2, 1),
        THRESHOLD_LABELS,
    )
    assert target.shape == (32, 16)
    assert canonical.shape == target.shape
    assert circuit.shape == target.shape
    np.testing.assert_allclose(target.conj().T @ target, multiplicity, atol=1e-10)
    np.testing.assert_allclose(canonical, target / np.sqrt(2), atol=1e-10)
    np.testing.assert_allclose(circuit, canonical, atol=1e-10)
    np.testing.assert_allclose(
        canonical.conj().T @ canonical,
        multiplicity / 2,
        atol=1e-10,
    )


def test_canonical_projector_erasure_validates_dimensions() -> None:
    _, _, projectors = predicted_joint_multiplicity_operator(
        (2, 1),
        THRESHOLD_LABELS,
    )
    with pytest.raises(ValueError, match="power of two"):
        canonical_projector_erasure_map(projectors[:3], 2, 4)
    with pytest.raises(ValueError, match="dimension"):
        canonical_projector_erasure_map(projectors, 2, 3)


def test_finite_control_verifies_singular_scaling_and_polar_invariance() -> None:
    control = audit_joint_analysis_map(
        3,
        (2, 1),
        THRESHOLD_LABELS,
        control_id="threshold",
    )
    assert control.exact_analysis_normalization_theorem_verified
    assert control.irrep_dimension == 2
    assert control.multiplicity_operator_rank > 1
    assert control.target_gram_residual < 1e-9
    assert control.canonical_erasure_map_residual < 1e-9
    assert control.canonical_gram_residual < 1e-9
    assert control.singular_value_scaling_residual < 1e-9
    assert control.polar_scale_invariance_residual < 1e-9


def test_direct_analysis_generic_boundary_is_square_root_of_density_boundary() -> None:
    record = joint_analysis_map_scaling_record(64)
    assert record.canonical_direct_analysis_normalization == "sqrt(d_nu)"
    assert record.density_rescaling_degree_order == "Omega(d_nu)"
    assert record.direct_analysis_amplification_degree_order == "Omega(sqrt(d_nu))"
    assert 20 < record.generic_direct_analysis_degree_log2_lower_bound < 30
    assert record.balanced_two_row_dimension_exponential
    assert not record.witness_sector_natural_mass_proved
    assert not record.direct_polar_compiled
    assert not record.direct_structured_polar_ruled_out


def test_generic_analysis_amplification_bound_rejects_invalid_inputs() -> None:
    rows = [
        generic_analysis_amplification_degree_lower_bound(value)
        for value in (2, 16, 256, 65536)
    ]
    assert rows == [1, 3, 15, 250]
    with pytest.raises(ValueError, match="positive"):
        generic_analysis_amplification_degree_lower_bound(0)
    with pytest.raises(ValueError, match="error"):
        generic_analysis_amplification_degree_lower_bound(2, 0.5)


def test_report_keeps_direct_structured_polar_open() -> None:
    report = run_joint_analysis_map_normalization()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["joint_rectangular_analysis_factor_identified"]
    assert report.claim_gate["joint_rectangular_analysis_gram_equals_D_nu"]
    assert report.claim_gate["canonical_projector_erasure_access_constructed"]
    assert report.claim_gate["canonical_access_normalization_is_sqrt_d_nu"]
    assert report.claim_gate["canonical_access_gram_equals_D_nu_over_d_nu"]
    assert report.claim_gate[
        "generic_direct_analysis_amplification_costs_omega_sqrt_d_nu"
    ]
    assert not report.claim_gate["normalization_one_A_nu_access_constructed"]
    assert not report.claim_gate["large_row_sector_natural_information_mass_proved"]
    assert not report.claim_gate["direct_structured_polar_compiled"]
    assert not report.claim_gate["direct_structured_polar_ruled_out"]
    assert not report.claim_gate["speedup_claim_allowed"]
