from self_dual_wreath_pair_common_covering_transition import (
    _s7_covering_control_labels,
    audit_covering_common_range,
    run_pair_common_covering_transition,
)


def test_s7_covering_control_is_globally_distinct() -> None:
    labels, companions = _s7_covering_control_labels()
    source = tuple(partition for label in labels for partition in label)
    assert len(labels) == 6
    assert len(companions) == 3
    assert len(source) == 12
    assert len(set(source)) == 12


def test_disjoint_covering_clusters_force_common_range_for_every_s7_target() -> None:
    record = audit_covering_common_range()
    assert record.partition_count == 15
    assert record.hamming_distance == 3
    assert record.left_only_cluster_covers_all_irreps
    assert record.right_only_cluster_covers_all_irreps
    assert record.shared_source_cluster_covers_all_irreps
    assert record.target_with_common_range_count == 15
    assert record.target_with_trivial_contribution_count == 15
    assert record.target_with_sign_contribution_count == 15
    assert record.minimum_common_range_dimension > 0
    assert record.exact_covering_to_common_range_verified


def test_report_records_kronecker_positivity_boundary_without_claiming_it() -> None:
    report = run_pair_common_covering_transition()
    assert report.headline_metrics["finite_covering_control_failure_count"] == 0
    assert report.claim_gate["constant_hamming_pair_common_recurrence_proved"]
    assert report.claim_gate["hamming_three_reduced_to_typical_kronecker_positivity"]
    assert report.claim_gate[
        "independent_plancherel_hamming_three_common_range_proved"
    ]
    assert not report.claim_gate[
        "arbitrarily_coupled_hamming_three_common_range_proved"
    ]
    assert not report.claim_gate["pair_common_rank_distribution_proved"]
    assert not report.claim_gate["natural_all_depth_node_edge_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
