from self_dual_wreath_affine_plane_support_pressure_no_go import (
    rich_plane_count_per_vertex,
)
from self_dual_wreath_interplane_gauge_homology import (
    audit_interplane_gauge_homology,
    audit_rich_point_degree,
    pattern_rich_steiner_lines,
    predicted_interplane_cycle_rank,
    run_interplane_gauge_homology,
)


def test_rich_line_and_point_degree_formulas_are_exact() -> None:
    for copy_count in range(4, 9):
        lines = pattern_rich_steiner_lines(copy_count)
        assert len(lines) == rich_plane_count_per_vertex(copy_count)
        for point in range(1, 1 << copy_count):
            record = audit_rich_point_degree(copy_count, point)
            assert record.exact_degree_verified
            assert (record.observed_rich_degree == 0) == (
                record.hamming_weight in {1, copy_count - 1, copy_count}
            )


def test_full_incidence_cycle_rank_is_exact_and_quadratic() -> None:
    for copy_count in range(3, 9):
        record = audit_interplane_gauge_homology(copy_count, "all")
        orientation_count = 1 << copy_count
        assert record.connected_component_count == 1
        assert record.isolated_point_count == 0
        assert record.cycle_rank == (
            (orientation_count - 2) * (orientation_count - 4) // 3
        )
        assert record.cycle_rank == predicted_interplane_cycle_rank(
            copy_count,
            "all",
        )
        assert record.exact_component_and_cycle_count_verified
        assert record.nontrivial_signed_cycle_class_verified


def test_rich_incidence_has_one_giant_component_and_quadratic_cycle_rank() -> None:
    for copy_count in range(4, 9):
        record = audit_interplane_gauge_homology(
            copy_count,
            "pattern-rich",
        )
        assert record.isolated_point_count == 2 * copy_count + 1
        assert record.connected_component_count == 2 * copy_count + 2
        assert record.cycle_rank == (
            2 * rich_plane_count_per_vertex(copy_count)
            - (1 << copy_count)
            + 2 * copy_count
            + 3
        )
        assert record.exact_component_and_cycle_count_verified
        assert record.negative_six_cycle_product == -1
        assert record.nontrivial_signed_cycle_class_verified


def test_report_exposes_natural_cycle_holonomy_as_the_open_boundary() -> None:
    report = run_interplane_gauge_homology()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["scalar_interplane_gauges_classified"]
    assert report.claim_gate["rich_cycle_rank_quadratic"]
    assert not report.claim_gate[
        "local_plane_holonomy_controls_global_gauge"
    ]
    assert not report.claim_gate["natural_cycle_holonomy_law_derived"]
    assert not report.claim_gate["natural_gauge_flat_or_concentrated"]
    assert not report.claim_gate["operator_valued_overlap_traffic_controlled"]
    assert not report.claim_gate["speedup_claim_allowed"]
