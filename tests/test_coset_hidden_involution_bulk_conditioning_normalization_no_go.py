import math

import pytest

from coset_hidden_involution_bulk_conditioning_normalization_no_go import (
    alternative_outside_window_bound,
    audit_bulk_conditioning,
    build_bulk_conditioning_normalization_report,
    bulk_copy_count,
    bulk_normalization_scaling_record,
    write_bulk_conditioning_normalization_report,
)


@pytest.mark.parametrize("spec", ((3, 1, 2), (3, 1, 3), (4, 2, 2)))
def test_exact_size_biased_bulk_controls(spec):
    row = audit_bulk_conditioning(*spec)
    assert row.exact_moment_and_size_bias_control_verified
    assert math.isclose(row.source_mean_eigenvalue, 1.0, abs_tol=1e-8)
    assert math.isclose(
        row.source_centered_second_moment,
        row.predicted_source_centered_second_moment,
        abs_tol=1e-8,
    )
    assert row.size_biased_outside_window_mass <= (
        row.moment_outside_window_upper_bound + 1e-8
    )
    assert row.retained_bulk_condition_number <= math.sqrt(3) + 1e-8


def test_copy_and_tail_bounds_validate_inputs():
    copies = bulk_copy_count(1000, 1e-6)
    assert (999 / 2**copies) <= 1e-6
    assert alternative_outside_window_bound(1e-6, 0.5) == pytest.approx(6e-6)
    with pytest.raises(ValueError, match="candidate_count"):
        bulk_copy_count(1, 1e-6)
    with pytest.raises(ValueError, match="delta"):
        alternative_outside_window_bound(0.1, 1.0)


def test_scaling_separates_conditioning_from_normalization():
    rows = [bulk_normalization_scaling_record(m) for m in (3, 4, 8, 16, 32, 64)]
    assert all(row.retained_alternative_mass_lower_bound > 0.999 for row in rows)
    assert all(row.unnormalized_bulk_condition_number_upper_bound < 2 for row in rows)
    assert all(
        not row.subgroup_outlier_classification_required_for_bulk_conditioning
        for row in rows
    )
    assert all(not row.unitary_basis_changes_improve_inherited_normalization for row in rows)
    assert all(not row.constant_normalization_row_access_compiled for row in rows)
    assert rows[-1].bernstein_qsvt_degree_lower_bound_log2 > 100


def test_report_redirects_active_compiler_target(tmp_path):
    report = build_bulk_conditioning_normalization_report(
        finite_specs=((3, 1, 2), (3, 1, 3)),
        scaling_half_degrees=(3, 4, 8, 16),
    )
    assert report.theorem.theorem_verified
    assert report.theorem.exact_bulk_mass_bound_proved
    assert report.theorem.constant_unnormalized_bulk_conditioning_proved
    assert not report.theorem.subgroup_classification_needed_for_bulk_conditioning
    assert report.theorem.inherited_incidence_qsvt_sqrt_M_obstruction_proved
    assert not report.theorem.unitary_trims_change_inherited_singular_scale
    assert not report.theorem.structured_constant_normalization_access_compiled
    assert report.claim_gate["natural_alternative_bulk_constant_conditioned"]
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_bulk_conditioning_normalization_report(
        tmp_path / "bulk-normalization.json",
        finite_specs=((3, 1, 2),),
        scaling_half_degrees=(3, 4, 8),
    )
    assert payload["status"] == (
        "bulk-conditioning-resolved-access-normalization-is-active-obstruction"
    )
    assert payload["headline_metrics"]["new_quantum_algorithm_count"] == 0
