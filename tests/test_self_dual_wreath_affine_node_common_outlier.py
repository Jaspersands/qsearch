import math

from self_dual_wreath_affine_node_common_outlier import (
    affine_generated_subgroup_order,
    audit_affine_subgroup,
    audit_physical_singleton_necessity,
    common_outlier_scaling_record,
    coordinate_incidence_rows,
    coordinate_membership_columns,
    run_affine_node_common_outlier,
)


def test_coordinate_affine_membership_geometry() -> None:
    for dimension in range(5):
        columns = coordinate_membership_columns(dimension)
        rows = coordinate_incidence_rows(dimension)
        assert len(columns) == 2 * dimension + 1
        assert len(set(columns)) == len(columns)
        assert len(rows) == 1 << dimension


def test_generated_subgroup_order_formula_matches_complete_s3_controls() -> None:
    for dimension in (0, 1, 2):
        record = audit_affine_subgroup(3, dimension)
        assert record.incidence_rank_over_f2 == dimension + 1
        assert record.predicted_generated_subgroup_order == (
            affine_generated_subgroup_order(math.factorial(3), dimension)
        )
        assert record.exact_generated_subgroup_order == (
            record.predicted_generated_subgroup_order
        )
        assert record.generated_subgroup_formula_verified


def test_physical_common_outlier_forces_singleton_one_dimensional_labels() -> None:
    for varying_pair in (0, 1):
        record = audit_physical_singleton_necessity(
            varying_pair_index=varying_pair
        )
        assert record.physical_block_count == 3**5
        assert record.common_outlier_block_count > 0
        assert record.singleton_one_dimensional_necessity_violation_count == 0
        assert record.exact_singleton_necessity_verified


def test_global_distinct_common_outlier_bound_is_factorially_small() -> None:
    records = [common_outlier_scaling_record(n) for n in (5, 8, 16, 32, 48)]
    for record in records:
        assert record.globally_distinct_event_numerator_upper_bound < (
            2 / math.factorial(record.n)
        )
        assert record.dimensions_at_least_two_impossible_under_global_distinctness
        assert record.exact_maximal_outlier_excluded_with_high_probability
        assert not record.near_maximal_outlier_excluded
        assert not record.natural_edge_proved
    assert all(
        right.globally_distinct_event_numerator_upper_bound_log2
        < left.globally_distinct_event_numerator_upper_bound_log2
        for left, right in zip(records, records[1:])
    )


def test_report_keeps_robust_edge_and_speedup_gates_closed() -> None:
    report = run_affine_node_common_outlier()
    assert report.headline_metrics["subgroup_control_failure_count"] == 0
    assert report.headline_metrics["physical_control_failure_count"] == 0
    assert report.claim_gate["exact_maximal_outlier_rare_over_natural_hierarchy"]
    assert not report.claim_gate["near_maximal_outliers_excluded"]
    assert not report.claim_gate["block_restricted_natural_edge_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
