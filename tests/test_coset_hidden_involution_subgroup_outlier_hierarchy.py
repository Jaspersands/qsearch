import pytest

from coset_hidden_involution_subgroup_outlier_hierarchy import (
    audit_subgroup_outlier,
    build_subgroup_outlier_report,
    centralizer_fixed_point_free_count,
    centralizer_fixed_point_free_count_recurrence,
    elementary_incident_lower_bound,
    subgroup_outlier_scaling_record,
    write_subgroup_outlier_report,
)


@pytest.mark.parametrize("half_degree", (2, 3, 4))
def test_exact_hyperoctahedral_incidence_count(half_degree):
    control = audit_subgroup_outlier(half_degree)
    assert control.exact_subgroup_incidence_verified
    assert control.centralizer_failure_count == 0
    assert control.direct_fixed_point_free_count == (
        control.formula_fixed_point_free_count
    )
    assert control.formula_fixed_point_free_count == (
        control.recurrence_fixed_point_free_count
    )
    assert control.noncommon_invariant_dimension == control.matching_index - 1
    assert control.all_incident_elements_fix_noncommon_sector


def test_incident_formula_recurrence_and_growth_bound():
    values = [centralizer_fixed_point_free_count(m) for m in range(1, 21)]
    assert values[:6] == [1, 3, 7, 25, 81, 331]
    assert all(
        value == centralizer_fixed_point_free_count_recurrence(m)
        for m, value in enumerate(values, start=1)
    )
    assert all(
        value >= elementary_incident_lower_bound(m)
        for m, value in enumerate(values, start=1)
    )
    with pytest.raises(ValueError, match="positive"):
        centralizer_fixed_point_free_count(0)
    with pytest.raises(ValueError, match="nonnegative"):
        centralizer_fixed_point_free_count_recurrence(-1)


def test_scaling_refutes_bounded_global_conditioning_only():
    rows = [subgroup_outlier_scaling_record(m) for m in (3, 4, 8, 16, 32, 64)]
    assert all(row.bounded_global_interval_conditioning_refuted for row in rows)
    assert all(
        int(row.trimmed_frame_norm_lower_bound_decimal)
        >= int(row.elementary_superpolynomial_lower_bound_decimal)
        for row in rows
    )
    assert rows[-1].global_polar_condition_proxy_lower_bound_log2 > 80
    assert all(not row.conjugate_sector_aggregate_mass_bounded for row in rows)
    assert all(not row.structured_subgroup_spectral_transform_compiled for row in rows)
    with pytest.raises(ValueError, match="at least three"):
        subgroup_outlier_scaling_record(2)


def test_report_keeps_structured_escape_and_speedup_gates_closed(tmp_path):
    report = build_subgroup_outlier_report(
        finite_half_degrees=(2, 3),
        scaling_half_degrees=(3, 4, 8, 16),
    )
    assert report.theorem.theorem_verified
    assert report.theorem.exact_incident_count_proved
    assert report.theorem.superpolynomial_incident_growth_proved
    assert report.theorem.all_copy_frame_norm_lower_bound_proved
    assert report.theorem.bounded_post_trim_global_conditioning_refuted
    assert not report.theorem.conjugate_sector_overlap_algebra_compiled
    assert not report.theorem.orbit_row_polar_compiled
    assert report.claim_gate["bounded_global_interval_polar_refuted"]
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_subgroup_outlier_report(
        tmp_path / "subgroup-outliers.json",
        finite_half_degrees=(2, 3),
        scaling_half_degrees=(3, 4, 8),
    )
    assert payload["status"] == (
        "post-trim-subgroup-outlier-no-go-structured-resolution-open"
    )
    assert payload["headline_metrics"]["new_quantum_algorithm_count"] == 0
