from self_dual_wreath_augmented_common_core_cech import (
    _controls,
    run_augmented_common_core_cech,
)


def test_distinct_w3_emergent_dependency_is_augmented_h0() -> None:
    control = _controls()[0]

    assert control.exact_augmented_cech_audit
    assert control.raw_leaf_dependency_dimension == 2
    assert control.pair_boundary_rank == 0
    assert control.emergent_leaf_dependency_homology_dimension == 2
    assert control.chain_groups[0].hodge_zero_eigenvalue_count == 2
    assert control.maximum_positive_degree_homology_dimension == 0
    assert not control.augmented_cech_exact


def test_repeated_w3_separates_pair_generated_and_emergent_h0() -> None:
    control = _controls()[1]

    assert control.raw_leaf_dependency_dimension == 4
    assert control.pair_boundary_rank == 3
    assert control.emergent_leaf_dependency_homology_dimension == 1
    assert control.chain_groups[0].hodge_zero_eigenvalue_count == 1
    assert control.maximum_boundary_composition_residual < 1e-10


def test_w5_pair_generated_control_is_augmented_exact() -> None:
    control = _controls()[2]

    assert control.raw_leaf_dependency_dimension == 5
    assert control.pair_boundary_rank == 5
    assert control.emergent_leaf_dependency_homology_dimension == 0
    assert control.augmented_cech_exact
    assert control.minimum_positive_hodge_eigenvalue > 0.59


def test_depth_three_cube_is_exact_but_explicitly_factorized() -> None:
    control = _controls()[3]

    assert len(control.chain_groups) == 8
    assert [record.nonzero_cell_count for record in control.chain_groups] == [
        8,
        28,
        56,
        70,
        56,
        28,
        8,
        1,
    ]
    assert all(record.homology_dimension == 0 for record in control.chain_groups)
    assert control.augmented_cech_exact
    assert control.minimum_positive_hodge_eigenvalue > 1.99
    assert control.maximum_positive_hodge_condition_number < 4.01


def test_report_blocks_pair_cycle_exactness_from_substituting_for_h0() -> None:
    report = run_augmented_common_core_cech()

    assert report.headline_metrics["finite_augmented_cech_audit_failure_count"] == 0
    assert report.headline_metrics["finite_emergent_h0_control_count"] == 2
    assert report.claim_gate["finite_augmented_cech_complex_verified"]
    assert not report.claim_gate[
        "pair_cycle_exactness_sufficient_for_full_exactness"
    ]
    assert report.claim_gate["emergent_leaf_dependency_homology_exists"]
    assert report.claim_gate["selected_n_at_least_five_augmented_controls_exact"]
    assert not report.claim_gate["all_n_augmented_cech_exactness_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
