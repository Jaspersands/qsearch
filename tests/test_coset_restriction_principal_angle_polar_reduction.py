import math

import pytest

from coset_restriction_principal_angle_polar_reduction import (
    audit_restriction_principal_angle_control,
    bernstein_polar_degree_lower_bound,
    build_coset_restriction_principal_angle_polar_report,
    principal_angle_scaling_record,
    write_coset_restriction_principal_angle_polar_report,
)


def test_exact_restriction_principal_angle_controls_hold():
    standard = (2, 1)
    controls = (
        audit_restriction_principal_angle_control((standard,), standard),
        audit_restriction_principal_angle_control(
            (standard, standard), (3,)
        ),
        audit_restriction_principal_angle_control(
            (standard, standard), standard
        ),
    )
    for row in controls:
        assert row.exact_principal_angle_normal_form_verified
        assert row.invariant_projector_idempotence_residual < 1e-8
        assert row.involution_projector_idempotence_residual < 1e-8
        assert row.restriction_gram_residual < 1e-8
        assert row.product_projector_singular_value_residual < 1e-8
        assert row.polar_initial_support_residual < 1e-8


def test_multiplicity_greater_than_one_does_not_assume_scalar_gram():
    standard = (2, 1)
    row = audit_restriction_principal_angle_control(
        (standard, standard, standard), standard
    )
    assert row.hom_space_multiplicity == 3
    assert row.restriction_map_rank == 1
    assert row.exact_principal_angle_normal_form_verified


def test_bernstein_polar_degree_bound_tracks_small_singular_scale():
    coarse = bernstein_polar_degree_lower_bound(0.1)
    fine = bernstein_polar_degree_lower_bound(0.01)
    assert fine > 9 * coarse
    assert math.isfinite(fine)
    with pytest.raises(ValueError, match="singular bound"):
        bernstein_polar_degree_lower_bound(1.0)
    with pytest.raises(ValueError, match="approximation_error"):
        bernstein_polar_degree_lower_bound(0.1, 1.0)


def test_finite_scaling_rows_are_controls_not_asymptotic_evidence():
    row = principal_angle_scaling_record(32)
    assert row.windowed_pgm_success_lower_bound > 0.3
    assert not row.polynomial_normalization_one_generic_qsvt_possible_asymptotically
    assert row.asymptotic_principal_singular_order.startswith("exp(")
    assert row.asymptotic_generic_qsvt_degree_order.startswith("exp(")


def test_report_closes_access_but_leaves_structured_escape_routes_open(
    tmp_path,
):
    report = build_coset_restriction_principal_angle_polar_report()
    assert report.theorem.theorem_verified
    assert report.theorem.exact_restriction_principal_angle_normal_form_proved
    assert report.theorem.coherent_normalization_one_restriction_access_proved
    assert not report.theorem.dense_branching_table_required
    assert report.theorem.generic_qsvt_subexponential_obstruction_proved
    assert not report.theorem.representation_specific_rescaling_ruled_out
    assert not report.theorem.hyperoctahedral_branching_transform_constructed
    assert not report.theorem.polynomial_fused_polar_circuit_constructed
    assert not report.theorem.general_quantum_circuit_lower_bound_proved
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_coset_restriction_principal_angle_polar_report(
        tmp_path / "report.json"
    )
    assert payload["status"] == (
        "coherent-restriction-access-closed-generic-qsvt-subexponential-"
        "structured-rescaling-open"
    )
