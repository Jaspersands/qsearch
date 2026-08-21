from coset_hidden_involution_pair_matching_charge_hierarchy import (
    audit_branch_resolution,
    audit_higher_matching_boundary,
    audit_local_power_collapse,
    audit_matching_charge,
    audit_stable_branch_resolution,
    build_pair_matching_charge_report,
    central_pair_charge,
    disjoint_matching_charge,
)


def test_edge_power_sum_is_exactly_redundant_with_C_and_K_center():
    control = audit_local_power_collapse()
    assert control.square_relation_nonzero_count == 0
    assert control.local_center_term_count == 4
    assert control.local_center_is_subgroup_sum
    assert control.global_center_controls_verified
    assert not control.power_sum_adds_copy_labels_beyond_C_and_K_center


def test_matching_charge_has_exact_polynomial_term_counts():
    for half_degree in range(4, 8):
        control = audit_matching_charge(half_degree)
        assert len(central_pair_charge(half_degree)) == 8 * (
            half_degree * (half_degree - 1) // 2
        )
        assert len(disjoint_matching_charge(half_degree)) == 192 * (
            half_degree
            * (half_degree - 1)
            * (half_degree - 2)
            * (half_degree - 3)
            // 24
        )
        assert control.polynomial_sparse_K_adapted_commuting_pair_verified


def test_C_and_D_are_exactly_commuting_and_K_adapted():
    for half_degree in range(4, 8):
        control = audit_matching_charge(half_degree)
        assert control.C_pair_commutator_failure_count == 0
        assert control.C_D_commutator_nonzero_count == 0
        assert control.C_K_commutator_failure_count == 0
        assert control.D_K_commutator_failure_count == 0


def test_D_strictly_improves_a_repeated_rank_five_branch():
    control = audit_branch_resolution(5, (6, 3, 1))
    assert control.center_joint_eigenspace_count == control.K_branch_block_count
    assert control.center_plus_C_joint_eigenspace_count == 25
    assert control.center_plus_C_D_joint_eigenspace_count == 26
    assert control.target_copy_label_count == 26
    assert control.D_added_copy_label_count == 1
    assert control.C_D_resolves_all_copy_labels


def test_D_is_an_all_rank_inverse_polynomial_stable_branch_resolver():
    control = audit_stable_branch_resolution()
    assert control.maximum_interpolated_degree <= 4
    assert control.closed_formula_matches_interpolation
    assert control.all_holdouts_match
    assert control.action_preserves_top_harmonic_copy_space
    assert control.restricted_action_reconstruction_verified
    assert control.gap_squared_ratio_to_support_five_resolver == "16/25"
    assert control.all_rank_stable_branch_resolver_proved
    assert not control.natural_source_mass_nonnegligible


def test_matching_pair_leaves_a_large_controlled_residual_sector():
    control = audit_branch_resolution(5, (4, 3, 2, 1))
    assert control.center_plus_C_joint_eigenspace_count == 50
    assert control.center_plus_C_D_joint_eigenspace_count == 50
    assert control.target_copy_label_count == 62
    assert not control.C_D_resolves_all_copy_labels


def test_third_matching_charge_fails_to_extend_the_commuting_pair():
    control = audit_higher_matching_boundary()
    assert control.D_term_count == 2880
    assert control.M3_term_count == 7680
    assert control.commutator_witness_coefficient == -1
    assert not control.D_M3_commute
    assert not control.matching_charge_family_pairwise_commuting


def test_report_preserves_every_algorithmic_claim_gate():
    report = build_pair_matching_charge_report()
    assert report.theorem.exact_all_rank_K_adapted_commuting_pair_proved
    assert report.theorem.edge_power_sum_redundancy_proved
    assert report.theorem.stable_multiplicity_two_resolver_proved
    assert report.theorem.stable_inverse_polynomial_gap_proved
    assert report.theorem.finite_copy_resolution_strictly_improved
    assert not report.theorem.complete_finite_copy_resolution_on_every_control
    assert not report.theorem.asymptotic_natural_copy_resolution_proved
    assert not report.theorem.inverse_polynomial_conditional_gaps_proved
    assert not report.theorem.source_signal_correlation_proved
    assert not report.theorem.coherent_subduction_transform_compiled
    assert not report.theorem.hidden_involution_detector_constructed
    assert not report.theorem.speedup_claim_allowed
