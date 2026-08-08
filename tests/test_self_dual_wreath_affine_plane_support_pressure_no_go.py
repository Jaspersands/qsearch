import math

from representation_obstruction import integer_partitions
from self_dual_wreath_affine_plane_support_pressure_no_go import (
    affine_plane_support_pressure_scaling_record,
    audit_rich_affine_plane_count,
    rich_plane_count_per_vertex,
    run_affine_plane_support_pressure_no_go,
    support_pressure_components,
)


def test_rich_affine_plane_count_matches_complete_enumeration() -> None:
    for copy_count in range(2, 9):
        record = audit_rich_affine_plane_count(copy_count)
        assert record.exact_rich_plane_count_verified
        assert record.predicted_rich_plane_count_per_vertex == (
            4**copy_count
            - 4 * 3**copy_count
            + 6 * 2**copy_count
            - 4
        ) // 6
        assert (
            record.predicted_rich_plane_count_per_vertex
            == rich_plane_count_per_vertex(copy_count)
        )


def test_exact_pressure_ratio_is_demand_over_worst_target_capacity() -> None:
    for n in (5, 7, 12, 20):
        demand, capacity, ratio, lower = support_pressure_components(n)
        record = affine_plane_support_pressure_scaling_record(n)
        assert ratio == demand / capacity
        assert math.isclose(record.exact_pressure_ratio, float(ratio))
        assert ratio >= lower > 1
        partition_count = len(tuple(integer_partitions(n)))
        assert record.elementary_pressure_ratio_lower_bound >= (
            (1 << record.selected_copy_count) / (20 * partition_count**2)
        )


def test_pressure_diverges_while_overlap_traffic_gate_stays_open() -> None:
    records = [
        affine_plane_support_pressure_scaling_record(n)
        for n in (8, 12, 16, 20, 24, 28, 32)
    ]
    assert all(record.pressure_exceeds_capacity for record in records)
    assert all(
        right.exact_pressure_ratio_log2 > left.exact_pressure_ratio_log2
        for left, right in zip(records, records[1:])
    )
    assert records[-1].exact_pressure_ratio_log2 > 90
    assert not records[-1].overlapping_plane_traffic_controlled


def test_report_falsifies_only_orthogonal_plane_atomization() -> None:
    report = run_affine_plane_support_pressure_no_go()
    assert report.headline_metrics["finite_plane_count_control_failure_count"] == 0
    assert report.headline_metrics["finite_pressure_capacity_failure_count"] == 0
    assert report.claim_gate["universal_orthogonal_plane_atomization_falsified"]
    assert report.claim_gate[
        "collision_free_orthogonal_plane_atomization_asymptotically_falsified"
    ]
    assert report.claim_gate[
        "local_scalar_affine_plane_holonomy_remains_positive"
    ]
    assert not report.claim_gate["overlapping_plane_matrix_traffic_controlled"]
    assert not report.claim_gate["global_carrier_groupoid_proved"]
    assert not report.claim_gate["collision_free_noncommon_frame_edge_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
