from self_dual_wreath_complete_s6_vertex_channel_audit import (
    low_dimension_s6_source_matchings,
    low_dimension_s6_source_partitions,
    run_complete_s6_vertex_channel_audit,
)


def test_low_dimension_s6_source_boundary_is_exact() -> None:
    partitions = low_dimension_s6_source_partitions()
    matchings = low_dimension_s6_source_matchings()
    assert len(partitions) == 8
    assert len(set(partitions)) == 8
    assert len(matchings) == 105
    assert all(
        len({partition for label in labels for partition in label}) == 8
        for labels in matchings
    )


def test_complete_s6_boundary_has_only_affine_triangle_channels() -> None:
    report = run_complete_s6_vertex_channel_audit()
    assert report.physical_portfolio_count == 1155
    assert report.degree_at_least_three_vertex_count == 64
    assert len(report.nonorthogonal_vertex_controls) == 16
    assert all(
        row.nontrivial_component_count == 1
        and row.every_component_is_three_edge_clique
        and row.every_component_closes_one_affine_plane
        and row.flat_groupoid_verified
        for row in report.nonorthogonal_vertex_controls
    )
    assert report.headline_metrics["nontrivial_component_count"] == 16
    assert report.headline_metrics["flat_groupoid_failure_count"] == 0


def test_complete_finite_audit_keeps_all_n_and_speedup_gates_closed() -> None:
    report = run_complete_s6_vertex_channel_audit()
    assert report.claim_gate["complete_stated_s6_portfolio_audited"]
    assert report.claim_gate[
        "every_observed_nonorthogonal_component_is_affine_triangle"
    ]
    assert not report.claim_gate["all_n_affine_triangle_channel_law_proved"]
    assert not report.claim_gate[
        "higher_multiplicity_channel_falsifiers_excluded"
    ]
    assert not report.claim_gate["collision_free_noncommon_frame_edge_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
