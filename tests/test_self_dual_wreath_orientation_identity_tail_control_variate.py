import math

import pytest

from self_dual_wreath_compressed_orientation_racah_cumulant_probe import (
    compile_orientation_racah_channel,
)
from self_dual_wreath_orientation_identity_tail_control_variate import (
    audit_orientation_identity_tail,
    coarse_sign_orbit_product_mass,
    raw_relative_variance_lower_bound,
    run_orientation_identity_tail_control_variate,
)


def test_identity_triple_mass_equals_coarse_product_null() -> None:
    group_order = math.factorial(7)
    dimension_product = 35**6
    identity_physical_mass = (
        8.0 * dimension_product**2 * (8.0 / group_order**3) / group_order**3
    )
    assert identity_physical_mass == pytest.approx(
        coarse_sign_orbit_product_mass(dimension_product, group_order)
    )


def test_s6_identity_residual_reconstructs_physical_likelihood_and_channel() -> None:
    control = compile_orientation_racah_channel(
        "S6-IDENTITY-TEST", ((3, 1, 1, 1),) * 6
    )
    row = audit_orientation_identity_tail(control)
    assert row.exact_identity_product_null_verified
    assert row.physical_to_product_likelihood_ratio == pytest.approx(0.23328)
    assert row.maximum_conditional_probability_residual < 1e-10
    assert row.negative_nonidentity_residual_count == 8


def test_raw_variance_warning_is_not_promoted_to_estimator_lower_bound() -> None:
    group_order = math.factorial(7)
    normalized_amplitude = group_order**-3
    bound = raw_relative_variance_lower_bound(normalized_amplitude, group_order)
    assert bound == pytest.approx(group_order**3 - 1.0)
    report = run_orientation_identity_tail_control_variate()
    assert report.claim_gate["identity_control_variate_available"] is True
    assert report.claim_gate["classical_lower_bound_proved"] is False


def test_s7_high_mass_repeated_sector_is_aggregate_product_like() -> None:
    control = compile_orientation_racah_channel(
        "S7-IDENTITY-TEST", ((3, 2, 1, 1),) * 6
    )
    row = audit_orientation_identity_tail(control)
    assert row.physical_orbit_mass > 0.01
    assert row.physical_to_product_likelihood_ratio == pytest.approx(
        0.9979348223954343
    )
    assert row.irreducible_racah_cmi_bits < 1e-4
    assert row.identity_subtracted_residual_efficiently_computable is False


def test_report_demotes_finite_signals_and_keeps_speedup_gate_closed() -> None:
    report = run_orientation_identity_tail_control_variate()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["S6_spike_survives_identity_audit_as_scalable_signal"] is False
    assert report.claim_gate["S7_high_mass_sector_has_large_aggregate_nonhaar_likelihood"] is False
    assert report.claim_gate["residual_positive_mass_scaling_proved"] is False
    assert report.claim_gate["speedup_claim_allowed"] is False
