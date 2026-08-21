from coset_hidden_involution_pair_gaudin_hierarchy import (
    _commutator,
    _element,
    audit_charge_hierarchy,
    audit_infinitesimal_braid_relations,
    audit_joint_spectra,
    build_pair_gaudin_hierarchy_report,
    pair_interaction,
    relative_charge_terms,
)


def test_pair_interaction_has_eight_three_cycle_terms():
    assert len(pair_interaction(6, 1, 5)) == 8
    assert len(set(pair_interaction(6, 1, 5))) == 8


def test_infinitesimal_braid_relations_are_exact():
    control = audit_infinitesimal_braid_relations()
    assert control.disjoint_support_relation_verified
    assert control.triangle_relation_verified
    assert control.all_rank_local_relations_proved


def test_relative_charges_commute_at_all_controlled_ranks():
    for half_degree in range(3, 9):
        charges = [
            _element(relative_charge_terms(rank, half_degree))
            for rank in range(2, half_degree + 1)
        ]
        assert all(
            not _commutator(charges[left], charges[right])
            for left in range(len(charges))
            for right in range(left + 1, len(charges))
        )


def test_cumulative_charge_is_global_orbit_but_relative_charges_break_K():
    for half_degree in (3, 4, 5, 6, 8):
        control = audit_charge_hierarchy(half_degree)
        assert control.charges_commute_pairwise
        assert control.cumulative_equals_global_orbit_sum
        assert control.cumulative_charge_commutes_with_final_K
        assert control.individual_charges_commuting_with_final_K_count == 0
        assert control.maximum_charge_term_count == 8 * (half_degree - 1)


def test_finite_joint_spectra_are_nontrivial_but_degenerate():
    for half_degree, repeated_count in ((4, 7), (5, 22)):
        control = audit_joint_spectra(half_degree)
        assert control.repeated_partition_count == repeated_count
        assert control.minimum_distinct_joint_eigenvalue_count > 1
        assert control.minimum_distinct_joint_eigenvalue_fraction > 0
        assert control.maximum_joint_eigenspace_multiplicity > 1
        assert control.simple_joint_spectrum_partition_count == 0
        assert control.maximum_pairwise_matrix_commutator_residual < 1e-9


def test_report_keeps_K_connection_and_speedup_gates_closed():
    report = build_pair_gaudin_hierarchy_report()
    assert report.theorem.exact_all_rank_commuting_hierarchy_proved
    assert report.theorem.polynomial_term_count_per_charge_proved
    assert report.theorem.cumulative_charge_has_natural_copy_variance_proved
    assert not report.theorem.joint_spectrum_simple_on_all_finite_controls
    assert not report.theorem.charges_preserve_final_K_labels
    assert not report.theorem.vertical_multiplicity_edges_factored
    assert not report.theorem.connection_to_K_adapted_basis_compiled
    assert not report.theorem.hidden_involution_detector_constructed
    assert not report.theorem.speedup_claim_allowed
