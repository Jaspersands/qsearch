import pytest

from coset_hidden_involution_imprimitive_plethysm_boundary import (
    audit_imprimitive_plethysm,
    bounded_partition_count,
    build_imprimitive_plethysm_report,
    fixed_point_free_involution_count_wreath,
    imprimitive_plethysm_scaling_record,
    incident_elementary_lower_bound,
    two_row_dimension,
    two_row_wreath_multiplicity,
    write_imprimitive_plethysm_report,
)


def test_exact_wreath_incidence_and_two_row_character_control():
    control = audit_imprimitive_plethysm(4, 3)
    assert control.generated_wreath_element_count == control.expected_wreath_order
    assert control.direct_fixed_point_free_count == 108
    assert control.direct_fixed_point_free_count == control.formula_fixed_point_free_count
    assert control.exact_incidence_formula_verified
    assert control.exact_two_row_multiplicity_formula_verified
    assert control.multiplicity_mismatch_count == 0
    assert control.odd_two_row_survivor_count > 0


def test_incident_formula_and_lower_term():
    for block_count, block_size in ((4, 3), (8, 3), (5, 4), (6, 5)):
        exact = fixed_point_free_involution_count_wreath(block_count, block_size)
        lower = incident_elementary_lower_bound(block_count, block_size)
        assert exact >= lower > 0
    with pytest.raises(ValueError, match="block_size"):
        fixed_point_free_involution_count_wreath(3, 1)


def test_subset_orbit_difference_exposes_odd_two_row_survivors():
    assert bounded_partition_count(3, 3, 4) == 3
    assert two_row_wreath_multiplicity(4, 3, 2) == 1
    assert two_row_wreath_multiplicity(4, 3, 3) == 1
    assert two_row_dimension(12, 3) == 154
    with pytest.raises(ValueError, match="subset_size"):
        two_row_wreath_multiplicity(4, 3, 7)


def test_high_index_survivors_are_two_row_deflatable_not_fully_resolved():
    rows = [
        imprimitive_plethysm_scaling_record(a, b)
        for a, b in ((8, 3), (16, 3), (16, 4), (16, 5))
    ]
    assert all(row.subgroup_index_log_group_order_ratio > 0.5 for row in rows)
    assert all(row.incident_candidate_count_log2 > 10 for row in rows)
    assert all(row.odd_two_row_survivor_sector_count > 0 for row in rows)
    assert all(row.odd_two_row_outliers_negligible_and_qft_deflatable for row in rows)
    assert all(not row.higher_row_plethysm_support_classified for row in rows)
    assert all(not row.residual_frame_norm_bounded for row in rows)
    with pytest.raises(ValueError, match="block_count,block_size"):
        imprimitive_plethysm_scaling_record(2, 3)


def test_report_isolates_higher_row_plethysm_barrier(tmp_path):
    report = build_imprimitive_plethysm_report(
        finite_specs=((4, 3),),
        scaling_specs=((8, 3), (16, 3), (16, 4)),
    )
    assert report.theorem.theorem_verified
    assert report.theorem.exact_incident_count_proved
    assert report.theorem.high_index_high_incidence_family_proved
    assert report.theorem.exact_two_row_plethysm_multiplicity_proved
    assert report.theorem.post_spherical_two_row_outliers_exhibited
    assert report.theorem.odd_two_row_outliers_deflated_at_vanishing_mass
    assert not report.theorem.higher_row_plethysm_support_classified
    assert not report.theorem.residual_frame_norm_bounded
    assert report.claim_gate["odd_two_row_survivors_exhibited_and_deflated"]
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_imprimitive_plethysm_report(
        tmp_path / "imprimitive-plethysm.json",
        finite_specs=((4, 3),),
        scaling_specs=((8, 3), (16, 3)),
    )
    assert payload["status"] == (
        "imprimitive-two-row-boundary-proved-higher-row-plethysm-open"
    )
    assert payload["headline_metrics"]["new_quantum_algorithm_count"] == 0
