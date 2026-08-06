from self_dual_wreath_recursive_pair_generation import (
    _controls,
    _s5_globally_distinct_portfolios,
    audit_s5_affine_pair_generation_boundary,
    run_recursive_pair_generation,
)


def test_recursive_h0_identity_localizes_w3_emergent_classes() -> None:
    distinct, repeated, _ = _controls()

    assert distinct.root_augmented_h0_dimension == 2
    assert distinct.maximum_cross_emergent_homology_dimension == 2
    assert repeated.root_augmented_h0_dimension == 1
    assert repeated.maximum_cross_emergent_homology_dimension == 1
    assert all(
        node.recursive_dimension_residual == 0
        and node.exact_recursive_h0_decomposition_verified
        for control in (distinct, repeated)
        for node in control.nodes
    )


def test_w5_recursive_pair_generation_has_no_emergent_cross_quotient() -> None:
    control = _controls()[2]

    assert control.globally_distinct_source_partitions
    assert control.root_augmented_h0_dimension == 0
    assert control.maximum_cross_emergent_homology_dimension == 0
    assert control.recursive_identity_failure_count == 0
    assert control.exact_recursive_pair_generation_audit


def test_s5_boundary_enumeration_has_105_distinct_portfolios() -> None:
    assert len(_s5_globally_distinct_portfolios()) == 105

    smoke = audit_s5_affine_pair_generation_boundary(maximum_portfolios=1)
    assert smoke.audited_affine_node_count == 105
    assert smoke.emergent_h0_node_count == 0
    assert smoke.maximum_pair_boundary_composition_residual < 1e-10
    assert not smoke.complete_s5_globally_distinct_affine_boundary_exhausted


def test_complete_s5_affine_boundary_is_pair_generated() -> None:
    report = run_recursive_pair_generation()
    boundary = report.s5_affine_boundary

    assert boundary.globally_distinct_portfolio_count == 105
    assert boundary.target_portfolio_count == 735
    assert boundary.affine_node_count_per_target_portfolio == 15
    assert boundary.audited_affine_node_count == 11_025
    assert boundary.emergent_h0_node_count == 0
    assert boundary.maximum_raw_leaf_dependency_dimension == 8
    assert boundary.maximum_pair_boundary_composition_residual < 1e-10
    assert boundary.complete_s5_globally_distinct_affine_boundary_exhausted
    assert report.claim_gate["recursive_augmented_h0_identity_verified"]
    assert not report.claim_gate["all_n_pair_generation_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
