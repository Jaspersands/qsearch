import json

from self_dual_wreath_pair_sheaf_metric_incompatibility import (
    audit_pair_sheaf_metric,
    pair_sheaf_metric_scaling_record,
    run_pair_sheaf_metric_incompatibility,
    write_pair_sheaf_metric_incompatibility_report,
)


def test_noncommon_half_correlation_edge_rejects_unweighted_gluing() -> None:
    control = audit_pair_sheaf_metric(
        "S4-HALF",
        (2, 2),
        (((4,), (3, 1)), ((2, 2), (2, 1, 1))),
        0,
        3,
    )
    assert control.active_pair_channel_rank == 2
    assert control.common_pair_channel_rank == 0
    assert control.noncommon_pair_channel_rank == 2
    assert abs(control.minimum_active_principal_correlation - 0.5) < 1e-12
    assert abs(control.initial_final_projection_distance - 3**0.5 / 2) < 1e-12
    assert abs(control.endpoint_metric_difference_norm - 1.0) < 1e-12
    assert abs(control.canonical_section_residual - 2**0.5) < 1e-12
    assert control.noncommon_channel_incompatibility_verified


def test_inverse_carrier_dimension_controls_have_the_same_metric_obstruction() -> None:
    third = audit_pair_sheaf_metric(
        "S4-THIRD",
        (2, 1, 1),
        (((4,), (3, 1)), ((2, 2), (2, 1, 1))),
        1,
        2,
    )
    quarter = audit_pair_sheaf_metric(
        "S5-QUARTER",
        (2, 1, 1, 1),
        (((5,), (4, 1)), ((2, 1, 1, 1), (1, 1, 1, 1, 1))),
        0,
        3,
    )
    assert abs(third.maximum_active_principal_correlation - 1 / 3) < 1e-12
    assert abs(quarter.maximum_active_principal_correlation - 1 / 4) < 1e-12
    assert abs(third.endpoint_metric_difference_norm - 1.0) < 1e-12
    assert abs(quarter.endpoint_metric_difference_norm - 1.0) < 1e-12
    assert third.exact_metric_obstruction_verified
    assert quarter.exact_metric_obstruction_verified


def test_common_channel_is_the_exact_compatible_exception() -> None:
    control = audit_pair_sheaf_metric(
        "S4-COMMON",
        (1, 1, 1, 1),
        (((4,), (3, 1)), ((2, 1, 1), (1, 1, 1, 1))),
        1,
        2,
    )
    assert control.active_pair_channel_rank == 1
    assert control.common_pair_channel_rank == 1
    assert control.noncommon_pair_channel_rank == 0
    assert abs(control.minimum_active_principal_correlation - 1.0) < 1e-12
    assert control.initial_final_projection_distance < 1e-12
    assert control.endpoint_metric_difference_norm < 1e-12
    assert control.canonical_section_residual < 1e-12
    assert control.common_channel_compatibility_verified


def test_pulled_back_metric_identity_is_exact_on_all_controls() -> None:
    report = run_pair_sheaf_metric_incompatibility()
    assert all(
        row.endpoint_metric_identity_residual < 2e-15
        for row in report.finite_controls
    )
    assert report.headline_metrics["finite_control_failure_count"] == 0


def test_scaling_rejects_only_the_unweighted_noncommon_architecture() -> None:
    record = pair_sheaf_metric_scaling_record(16)
    assert record.pair_gpe_noncommon_transport_polynomial
    assert record.endpoint_metric_equality_necessary
    assert not record.vertex_local_gauge_can_repair_metric_mismatch
    assert not record.noncommon_pair_edges_compile_global_polar
    assert not record.common_edges_cover_complete_natural_frame_proved
    assert not record.operator_metric_or_higher_relation_compiler_proved
    assert not record.complete_orientation_polar_compiled


def test_report_keeps_weighted_higher_relation_and_speedup_gates_open_or_false() -> None:
    report = run_pair_sheaf_metric_incompatibility()
    assert report.theorem.theorem_verified
    assert report.headline_metrics["noncommon_pair_incompatibility_control_count"] == 3
    assert report.headline_metrics["common_pair_compatibility_control_count"] == 1
    assert report.claim_gate["pair_edge_endpoint_metric_equality_necessary"]
    assert report.claim_gate["endpoint_metric_obstruction_vertex_gauge_invariant"]
    assert not report.claim_gate["noncommon_pair_gpe_edges_unweighted_compatible"]
    assert not report.claim_gate[
        "unweighted_noncommon_pair_sheaf_compiles_global_polar"
    ]
    assert not report.claim_gate["all_partial_holonomy_architectures_rejected"]
    assert not report.claim_gate["operator_metric_or_higher_relation_compiler_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_report_writer_records_restricted_no_go(tmp_path) -> None:
    path = tmp_path / "pair_sheaf_metric.json"
    payload = write_pair_sheaf_metric_incompatibility_report(path)
    stored = json.loads(path.read_text())
    assert stored["status"] == payload["status"]
    assert stored["status"] == "noncommon-pair-polar-unweighted-sheaf-no-go"
    assert stored["headline_metrics"]["finite_control_count"] == 4
    assert stored["headline_metrics"]["pair_edge_metric_necessity_theorem_count"] == 1
    assert stored["headline_metrics"]["complete_orientation_polar_compiler_count"] == 0
    assert not stored["claim_gate"]["speedup_claim_allowed"]
