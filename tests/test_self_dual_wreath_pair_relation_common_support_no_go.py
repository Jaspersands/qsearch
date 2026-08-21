import json

from self_dual_wreath_pair_relation_common_support_no_go import (
    audit_pair_relation_common_support,
    pair_relation_scaling_record,
    run_pair_relation_common_support_no_go,
    write_pair_relation_common_support_no_go_report,
)


def test_half_correlation_channels_have_no_exact_pair_relation_rank() -> None:
    control = audit_pair_relation_common_support(
        "S4-HALF",
        (2, 2),
        (((4,), (3, 1)), ((2, 2), (2, 1, 1))),
        0,
        3,
    )
    assert control.active_pair_principal_channel_rank == 2
    assert control.common_principal_channel_rank == 0
    assert control.noncommon_principal_channel_rank == 2
    assert control.coordinate_row_space_intersection_rank == 0
    assert control.maximum_exact_pair_relation_rank == 0
    assert control.noncommon_channel_rank_uncovered_by_pair_relations == 2
    assert control.exact_pair_relation_rank_theorem_verified


def test_inverse_dimension_noncommon_channels_remain_uncovered() -> None:
    third = audit_pair_relation_common_support(
        "S4-THIRD",
        (2, 1, 1),
        (((4,), (3, 1)), ((2, 2), (2, 1, 1))),
        1,
        2,
    )
    quarter = audit_pair_relation_common_support(
        "S5-QUARTER",
        (2, 1, 1, 1),
        (((5,), (4, 1)), ((2, 1, 1, 1), (1, 1, 1, 1, 1))),
        0,
        3,
    )
    assert third.noncommon_principal_channel_rank == 3
    assert quarter.noncommon_principal_channel_rank == 4
    assert third.maximum_exact_pair_relation_rank == 0
    assert quarter.maximum_exact_pair_relation_rank == 0
    assert third.exact_pair_relation_rank_theorem_verified
    assert quarter.exact_pair_relation_rank_theorem_verified


def test_common_channel_attains_the_exact_pair_relation_rank_bound() -> None:
    control = audit_pair_relation_common_support(
        "S4-COMMON",
        (1, 1, 1, 1),
        (((4,), (3, 1)), ((2, 1, 1), (1, 1, 1, 1))),
        1,
        2,
    )
    assert control.active_pair_principal_channel_rank == 1
    assert control.common_principal_channel_rank == 1
    assert control.noncommon_principal_channel_rank == 0
    assert control.coordinate_row_space_intersection_rank == 1
    assert control.maximum_exact_pair_relation_rank == 1
    assert control.constructed_maximal_relation_rank == 1
    assert control.constructed_maximal_relation_residual < 1e-12


def test_coordinate_intersection_rank_matches_literal_common_support() -> None:
    report = run_pair_relation_common_support_no_go()
    assert all(
        row.intersection_common_rank_residual == 0
        for row in report.finite_controls
    )
    assert report.headline_metrics["maximum_intersection_common_rank_residual"] == 0
    assert report.headline_metrics["maximum_constructed_relation_residual"] < 1e-12


def test_scaling_closes_pair_only_but_leaves_higher_arity_open() -> None:
    record = pair_relation_scaling_record(16)
    assert record.maximum_pair_relation_rank_equals_common_support
    assert not record.operator_endpoint_metrics_recover_noncommon_channels
    assert not record.pair_only_sheaf_compiles_complete_polar
    assert record.genuinely_higher_arity_relations_required
    assert not record.coherent_higher_arity_parity_check_compiled
    assert record.direct_rectangular_cs_transform_open


def test_report_records_pair_only_no_go_without_overclaiming() -> None:
    report = run_pair_relation_common_support_no_go()
    assert report.theorem.theorem_verified
    assert report.headline_metrics["finite_control_count"] == 4
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.headline_metrics["total_noncommon_channel_rank_uncovered"] == 9
    assert report.claim_gate[
        "maximum_exact_pair_relation_rank_equals_common_support"
    ]
    assert not report.claim_gate[
        "operator_weighted_pair_relations_recover_noncommon_channels"
    ]
    assert not report.claim_gate["pair_only_sheaf_compiles_complete_polar"]
    assert report.claim_gate[
        "higher_arity_relations_mathematically_required_for_noncommon_dependencies"
    ]
    assert not report.claim_gate["coherent_higher_arity_parity_check_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_report_writer_records_common_support_rank_theorem(tmp_path) -> None:
    path = tmp_path / "pair_relation_common_support.json"
    payload = write_pair_relation_common_support_no_go_report(path)
    stored = json.loads(path.read_text())
    assert stored["status"] == payload["status"]
    assert stored["status"] == (
        "pair-relations-exactly-common-support-higher-arity-required"
    )
    assert stored["headline_metrics"]["pair_relation_common_support_theorem_count"] == 1
    assert stored["headline_metrics"]["coherent_higher_arity_parity_check_compiler_count"] == 0
    assert stored["headline_metrics"]["new_quantum_algorithm_count"] == 0
    assert not stored["claim_gate"]["speedup_claim_allowed"]
