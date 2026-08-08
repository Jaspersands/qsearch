import math

from self_dual_wreath_subgroup_pair_angle_no_go import (
    audit_pair_angle_no_go,
    pair_angle_scaling_record,
    pair_generated_subgroup_order,
    run_subgroup_pair_angle_no_go,
)


def test_pair_generated_subgroup_has_three_pattern_order() -> None:
    for n in (2, 3, 5, 8):
        order = math.factorial(n)
        assert pair_generated_subgroup_order(order) == order**3 // 2


def test_complete_s2_two_cube_has_maximal_global_quotient_pair_angles() -> None:
    record = audit_pair_angle_no_go()
    assert record.ambient_dimension == 32
    assert record.full_generated_subgroup_order == 8
    assert record.pair_generated_subgroup_order == 4
    assert record.full_common_invariant_dimension == 4
    assert record.pair_common_invariant_dimension == 8
    assert record.tested_orientation_pair_count == 6
    assert record.minimum_globally_quotiented_pair_cosine > 1 - 1e-12
    assert record.maximum_globally_quotiented_pair_cosine_residual_from_one < 1e-12
    assert record.pairwise_cosine_matrix_spectral_radius == 3
    assert record.exact_pair_angle_no_go_verified


def test_pair_common_to_global_common_ratio_explodes_at_natural_depth() -> None:
    records = [
        pair_angle_scaling_record(n, math.ceil(math.lgamma(n + 1) / math.log(2)))
        for n in (8, 16, 32, 48)
    ]
    assert all(record.pair_to_full_common_dimension_ratio_log2 > 0 for record in records)
    assert all(
        right.pair_to_full_common_dimension_ratio_log2
        > left.pair_to_full_common_dimension_ratio_log2
        for left, right in zip(records, records[1:])
    )
    assert all(not record.unrefined_pairwise_angle_criterion_viable for record in records)
    assert all(not record.source_block_restricted_angle_theorem_proved for record in records)


def test_report_does_not_promote_regular_no_go_to_physical_no_go() -> None:
    report = run_subgroup_pair_angle_no_go()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["unrefined_regular_pairwise_angle_route_refuted"]
    assert not report.claim_gate["source_block_restricted_pair_angle_bound_proved"]
    assert not report.claim_gate["higher_order_center_valued_expansion_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
