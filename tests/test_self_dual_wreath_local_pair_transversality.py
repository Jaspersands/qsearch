import math

from self_dual_wreath_local_pair_transversality import (
    _conjugate,
    audit_local_pair_formula,
    local_transversality_scaling_record,
    run_local_pair_transversality,
)


def test_partition_conjugation_is_an_involution() -> None:
    partitions = ((5,), (4, 1), (3, 2), (3, 1, 1), (2, 2, 1), (1, 1, 1, 1, 1))
    for partition in partitions:
        assert _conjugate(_conjugate(partition)) == partition


def test_complete_s4_radius_two_necessity_control() -> None:
    record = audit_local_pair_formula()
    assert record.globally_distinct_label_tuple_count == 15
    assert record.target_count == 5
    assert record.orientation_pair_count == 15 * 5 * 6
    assert record.hamming_one_pair_count == 15 * 5 * 4
    assert record.hamming_two_pair_count == 15 * 5 * 2
    assert record.common_hamming_one_pair_count == 0
    assert record.common_hamming_two_pair_count == 2
    assert record.hamming_one_necessity_violation_count == 0
    assert record.hamming_two_necessity_violation_count == 0
    assert record.exact_local_necessity_verified


def test_scaling_bounds_use_source_relations_not_orientation_pair_count() -> None:
    for n in (5, 8, 12, 16, 20):
        record = local_transversality_scaling_record(n)
        order = math.factorial(n)
        copies = record.information_threshold_copy_count
        assert math.isclose(
            record.hamming_one_any_coordinate_numerator_upper_bound,
            2 * copies / order**2,
        )
        assert math.isclose(
            record.hamming_two_any_coordinate_numerator_upper_bound,
            2
            * math.comb(copies, 2)
            * record.plancherel_collision_probability**2,
        )
        assert record.asymptotic_hamming_radius_two_transversality
        assert math.isclose(
            record.noncommon_pair_product_norm_upper_bound,
            1 / (n - 1),
        )
        assert not record.full_node_frame_edge_proved


def test_report_keeps_higher_order_and_speedup_gates_closed() -> None:
    report = run_local_pair_transversality()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["natural_global_distinct_radius_two_transversality_proved"]
    assert report.claim_gate["radius_two_noncommon_pair_norm_bound_proved"]
    assert not report.claim_gate["distant_pair_common_support_controlled"]
    assert not report.claim_gate["higher_order_incidence_expansion_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
