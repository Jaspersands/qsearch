from coset_hidden_involution_source_local_likelihood_no_go import (
    audit_matching_charge_no_go,
    audit_proper_subset_factorization,
    audit_source_slice,
    audit_target_coupled_escape,
    build_source_local_likelihood_no_go_report,
    write_source_local_likelihood_no_go_report,
)


def test_exact_BAB_source_slice_for_two_nonisomorphic_controls():
    controls = [
        audit_source_slice(3, 1, 2)[0],
        audit_source_slice(4, 2, 2)[0],
    ]
    for control in controls:
        assert control.observed_target_identity_BAB_support_size == 4
        assert control.expected_target_identity_BAB_support_size == 4
        assert (
            control.observed_factorization_multiplicity_minimum
            == control.expected_factorization_multiplicity
        )
        assert (
            control.observed_factorization_multiplicity_maximum
            == control.expected_factorization_multiplicity
        )
        assert control.maximum_basis_trace_factorization_residual == 0.0
        assert control.target_identity_slice_equals_H_power
        assert control.exact_trace_factorization_verified


def test_matching_charges_are_inside_source_local_no_go_class():
    control = audit_matching_charge_no_go(5)
    assert control.pair_charge_term_count == 80
    assert control.matching_charge_term_count == 960
    assert control.pair_charge_identity_coefficient == 0
    assert control.pair_charge_hidden_coefficient == 0
    assert control.matching_charge_identity_coefficient == 0
    assert control.matching_charge_hidden_coefficient == 0
    assert control.pair_charge_K_commutator_failure_count == 0
    assert control.matching_charge_K_commutator_failure_count == 0
    assert control.pair_and_matching_charges_are_B_compatible
    assert control.joint_charge_spectral_measurement_is_source_local
    assert control.joint_charge_distribution_is_likelihood_independent
    assert not control.standalone_charge_detector_possible


def test_target_coupling_escapes_exact_source_slice_identity():
    control = audit_target_coupled_escape()
    assert control.baseline_normalized_trace == "0"
    assert control.likelihood_weighted_normalized_trace != "0"
    assert control.likelihood_weighted_trace_positive
    assert not control.source_local_factorization_extends_to_target_coupled_elements
    assert control.all_copy_target_coupling_escapes_proper_subset_no_go


def test_every_proper_source_target_subset_is_likelihood_blind():
    controls = [
        audit_proper_subset_factorization(3, 1, 2, 1),
        audit_proper_subset_factorization(3, 1, 3, 1),
        audit_proper_subset_factorization(3, 1, 3, 2),
        audit_proper_subset_factorization(4, 2, 2, 1),
    ]
    for control in controls:
        assert control.active_source_coordinate_count < control.copy_count
        assert control.untouched_source_coordinate_count >= 1
        assert (
            control.baseline_supported_basis_element_count
            == control.likelihood_supported_basis_element_count
        )
        assert control.non_H_target_likelihood_support_count == 0
        assert control.maximum_basis_trace_factorization_residual == 0.0
        assert control.proper_subset_trace_factorization_verified


def test_report_states_distribution_level_no_go_without_speedup_claim():
    report = build_source_local_likelihood_no_go_report()
    assert report.theorem.exact_all_finite_groups_trace_factorization_proved
    assert report.theorem.complete_source_local_measurement_independence_proved
    assert report.theorem.all_proper_source_target_marginals_likelihood_independent
    assert report.theorem.bounded_locality_low_degree_moment_no_go_proved
    assert report.theorem.matching_charge_standalone_detector_ruled_out
    assert report.theorem.finite_block_charge_correlation_globally_cancelled
    assert report.theorem.all_copy_target_coupled_observable_required_within_group_algebra_model
    assert not report.theorem.target_coupled_decoder_constructed
    assert not report.theorem.coherent_recoupling_transform_compiled
    assert not report.theorem.hidden_involution_detector_constructed
    assert not report.theorem.speedup_claim_allowed
    assert report.theorem.theorem_verified


def test_live_report_is_json_serializable(tmp_path):
    output_path = tmp_path / "source-local-likelihood-no-go.json"
    payload = write_source_local_likelihood_no_go_report(output_path)
    assert output_path.exists()
    assert payload["theorem"]["theorem_verified"]
    assert payload["claim_gate"][
        "complete_source_local_measurement_independence_proved"
    ]
