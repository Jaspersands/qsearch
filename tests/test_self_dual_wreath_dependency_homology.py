from self_dual_wreath_dependency_homology import (
    _controls,
    run_dependency_homology,
)


def test_distinct_w3_dependencies_are_genuinely_emergent_and_neutral() -> None:
    distinct = _controls()[0]

    assert distinct.audited_fractional_merge_count == 9
    assert distinct.pair_generated_merge_count == 0
    assert distinct.emergent_merge_count == 9
    assert distinct.maximum_emergent_homology_dimension == 2
    assert distinct.nonneutral_merge_count == 0
    assert all(
        record.exact_pair_common_edge_count == 0
        and record.emergent_dependency_homology_dimension == 2
        and record.emergent_classes_totally_neutral
        for record in distinct.records
    )


def test_w5_and_w6_selected_common_channels_are_pair_generated() -> None:
    _, _, w5, w6, _ = _controls()

    assert w5.audited_fractional_merge_count == 11
    assert w5.pair_generated_merge_count == 11
    assert w5.emergent_merge_count == 0
    assert w5.nonneutral_merge_count == 0
    assert w6.audited_fractional_merge_count == 10
    assert w6.pair_generated_merge_count == 10
    assert w6.emergent_merge_count == 0
    assert w6.nonneutral_merge_count == 0


def test_collision_free_pair_generated_dependency_can_be_nonneutral() -> None:
    counterexample = _controls()[4]
    record = counterexample.records[0]

    assert counterexample.globally_distinct_source_partitions
    assert counterexample.pair_generated_merge_count == 1
    assert counterexample.emergent_merge_count == 0
    assert counterexample.nonneutral_merge_count == 1
    assert record.cross_dependency_dimension == 34
    assert record.pair_dependency_class_dimension == 34
    assert record.emergent_dependency_homology_dimension == 0
    assert abs(record.full_grading_neutrality_residual - 1 / 17) < 1e-10
    assert abs(min(record.fractional_eigenvalues) - 8 / 17) < 1e-10
    assert abs(max(record.fractional_eigenvalues) - 89 / 170) < 1e-10


def test_repeated_labels_show_pair_generation_and_neutrality_are_distinct() -> None:
    repeated = _controls()[1]

    assert repeated.nonneutral_merge_count == 9
    assert repeated.pair_generated_merge_count > 0
    assert repeated.emergent_merge_count > 0
    assert any(
        record.pair_dependency_class_dimension > 0
        and not record.pair_classes_totally_neutral
        for record in repeated.records
    )
    assert any(
        record.emergent_dependency_homology_dimension > 0
        and not record.emergent_classes_totally_neutral
        for record in repeated.records
    )


def test_report_keeps_all_n_chain_complex_and_coherent_quotient_open() -> None:
    report = run_dependency_homology()

    assert report.headline_metrics["finite_homology_audit_failure_count"] == 0
    assert report.headline_metrics[
        "w3_distinct_maximum_emergent_homology_dimension"
    ] == 2
    assert report.headline_metrics["w5_pair_generated_merge_count"] == 11
    assert report.headline_metrics["w6_pair_generated_merge_count"] == 10
    assert report.headline_metrics[
        "collision_free_nonneutral_pair_generated_merge_count"
    ] == 1
    assert report.claim_gate["finite_dependency_homology_quotient_verified"]
    assert report.claim_gate["w3_distinct_dependency_is_genuinely_emergent"]
    assert not report.claim_gate["universal_pair_generation_proved"]
    assert not report.claim_gate[
        "all_n_emergent_homology_neutrality_proved"
    ]
    assert report.claim_gate[
        "collision_free_pair_generated_half_balance_falsified"
    ]
    assert not report.claim_gate["coherent_pair_common_quotient_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]
