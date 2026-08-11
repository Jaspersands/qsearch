import math

import pytest

from coset_covariant_measurement_multiplicity_width_no_go import (
    audit_finite_covariant_measurement_width,
    build_coset_covariant_measurement_multiplicity_width_report,
    covariant_measurement_width_scaling_record,
    multiplicity_width_lower_bound,
    write_coset_covariant_measurement_multiplicity_width_report,
)


def test_multiplicity_width_formula_scales_with_success_and_orbit_size():
    assert multiplicity_width_lower_bound(105, 70, 2 / 3) == pytest.approx(1.0)
    assert multiplicity_width_lower_bound(105, 5, 1 / 7) == pytest.approx(3.0)


def test_exact_s3_pgm_support_has_valid_isotypic_mode_decomposition():
    for copy_count in (1, 2):
        row = audit_finite_covariant_measurement_width(3, copy_count)
        assert row.theorem_control_passed
        assert row.pgm_completeness_residual < 1e-8
        assert row.covariance_commutator_residual < 1e-8
        assert row.support_rank_decomposition_residual == 0
        assert row.multiplicity_divisibility_failure_count == 0
        assert row.support_dimension_bound_verified
        assert row.multiplicity_width_bound_verified


def test_inverse_polynomial_scaling_row_has_only_geometric_consequence():
    n = 32
    row = covariant_measurement_width_scaling_record(
        n,
        success_requirement_id="inverse-quadratic",
        target_success_probability=n**-2,
        polynomial_exponent=2,
    )
    assert row.target_success_polynomial_exponent == 2
    assert math.isfinite(row.log2_normalized_multiplicity_mode_lower_bound)
    assert not row.polynomial_explicit_mode_catalog_possible_asymptotically
    assert not row.polynomial_gate_lower_bound_proved
    assert not row.polynomial_qubit_lower_bound_proved


def test_invalid_width_parameters_are_rejected():
    with pytest.raises(ValueError, match="hidden_count"):
        multiplicity_width_lower_bound(1, 2, 0.5)
    with pytest.raises(ValueError, match="success_probability"):
        multiplicity_width_lower_bound(10, 2, 0.0)


def test_report_closes_sparse_catalogs_not_implicit_polar(tmp_path):
    report = build_coset_covariant_measurement_multiplicity_width_report()
    assert report.theorem.theorem_verified
    assert report.theorem.arbitrary_povm_support_rank_bound_proved
    assert report.theorem.covariant_symmetrization_preserves_success_proved
    assert report.theorem.exp_sqrt_multiplicity_width_for_inverse_polynomial_success_proved
    assert not report.theorem.polynomial_explicit_mode_catalog_possible
    assert not report.theorem.fused_polar_isometry_ruled_out
    assert not report.theorem.polynomial_gate_lower_bound_proved
    assert not report.theorem.polynomial_qubit_lower_bound_proved
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_coset_covariant_measurement_multiplicity_width_report(
        tmp_path / "report.json"
    )
    assert payload["status"] == (
        "sparse-multiplicity-measurements-closed-"
        "implicit-wide-polar-open"
    )
