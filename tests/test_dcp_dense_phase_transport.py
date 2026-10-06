from fractions import Fraction

import pytest

from dcp_carry_packets import compile_packet
from dcp_physical_phase_noise import read
from dcp_dense_phase_transport import (
    _fault_amplification_controls, _lattice_parameter_controls,
    _physical_transport_controls, _residue_source_controls, correlated_basis_fault_reduction_bound,
    dense_source_certificate, group_index, group_vector, offset_collision_witness_certificate,
    reference_matching_permutation, sparse_sign_transport_certificate, verify_transport_witness,
)


def test_dense_chi_squared_identity_matches_every_higher_source_table():
    rows = _residue_source_controls()
    assert [row["all_higher_source_tables"] for row in rows] == [64, 256, 4096]
    assert [read(row["exact_mean_residue_chi_squared"]) for row in rows] == [Fraction(3, 4), Fraction(3, 8), Fraction(15, 2)]


def test_full_label_sparse_correction_bound_is_not_a_general_decoder_no_go():
    row = sparse_sign_transport_certificate(256, 256, 512, 256**2)
    assert read(row["supplied_attempt_success_upper_bound"]) < Fraction(1, 10**50)
    assert row["higher_label_dependent_corrections_and_full_image_parameterizations_allowed"]
    assert not row["retaining_signed_labels_or_decoding_them_ruled_out"]
    assert not sparse_sign_transport_certificate(64, 8, 128)["union_bound_nonvacuous"]


def test_dense_source_positive_bound_charges_states_and_unimplemented_transport():
    row = dense_source_certificate(256, 256, 16)
    assert row["original_phase_states_per_attempt"] == 2064
    assert read(row["rational_ideal_mean_residue_success_lower_bound"]) == Fraction(255, 256)**2
    assert read(row["exact_high_source_mean_residue_chi_squared_to_uniform"]) < Fraction(1, 65536)
    assert not row["efficient_canonical_transport_implemented"]


def test_all_secret_fourier_success_equals_independent_challenge_two_call_baseline():
    rows = _physical_transport_controls()
    assert len(rows) == 9
    for row in rows:
        assert row["mean_QFT_success"] == row["independent_challenge_witness_success"]
        assert read(row["public_monomial_phase_mean_success"]) <= read(row["mean_QFT_success"])
        assert row["two_call_certificate"]["forward_transport_evaluator_calls_per_classical_trial"] == 2
        assert not row["two_call_certificate"]["whole_DCP_input_experiment_classically_simulated"]


def test_reference_matching_is_a_true_permutation_and_never_an_efficient_claim():
    packet = compile_packet([[1, 3, 2, 7, 0]], 8)
    permutation, row = reference_matching_permutation(packet)
    assert sorted(permutation) == list(range(16))
    assert not row["efficient_decoder"]
    cert = offset_collision_witness_certificate(packet, permutation)
    assert not cert["classical_evaluator_provided_by_reference_enumeration_is_polynomial"]
    with pytest.raises(ValueError):
        reference_matching_permutation(compile_packet([[1] + [0] * 12], 8))


def test_independent_challenge_witness_is_explicitly_verified():
    packet = compile_packet([[1, 3, 2, 7, 0]], 8)
    permutation, _ = reference_matching_permutation(packet)
    for t in range(4):
        result = verify_transport_witness(packet, permutation, (t,), (0,), 0)
        if result is not None:
            assert sum(a * x for a, x in zip(packet.labels[0], result)) % 8 == 2 * t


def test_specific_prelabel_basis_fault_model_can_amplify_without_conditional_marginals():
    row = correlated_basis_fault_reduction_bound(256, 256)
    assert row["bounded_error_below_one_third_as_declared"]
    assert read(row["total_failure_probability_upper_bound"]) < Fraction(1, 3)
    assert row["arbitrary_classical_correlations_between_prelabel_fault_statuses_allowed"]
    assert not row["independent_fault_statuses_or_conditional_marginal_failure_bound_required"]
    assert not row["arbitrary_entangled_basis_corruption_or_joint_Z_error_laws_covered"]
    assert not row["efficient_canonical_transport_implemented"]
    assert row["total_original_states_charged"] == row["attempts"] * row["original_states_per_allocated_attempt_block"]


def test_insufficient_resources_are_retained_not_promoted_to_a_decoder():
    row = correlated_basis_fault_reduction_bound(64, 64, attempts=1)
    assert not row["bounded_error_below_one_third_as_declared"]
    assert not row["speedup_claim_allowed"]


def test_correlated_Z_marginals_cannot_replace_conditional_fair_gauge_coins():
    row = _fault_amplification_controls()
    assert row["conditional_clean_component_Jensen_controls"] == 625
    assert read(row["one_shared_fair_error_coin_no_clean_attempt_probability"]) > read(row["independent_fair_errors_no_clean_attempt_probability"])
    assert row["counterexample_is_about_clean_component_amplification_not_decoder_failure"]


def test_lattice_regime_is_exponential_modulus_but_polynomial_input_bits():
    rows = _lattice_parameter_controls()
    for row in rows:
        n = row["dimension"]
        assert row["coordinate_QFT_modulus_binary_exponent"] == 4 * n + 1
        assert row["residue_entropy_bits"] == 4 * n * n
        assert row["dense_packet_original_states"] == 4 * n * n + n + 16
        bound = row["conditional_full_decoder_bound"]
        assert bound["bounded_error_below_one_third_as_declared"]
        assert not row["actual_lattice_state_supply_and_total_precision_composition_verified"]
        assert not bound["candidate_record_accepted"]
        assert read(bound["remaining_total_probability_perturbation_margin_to_one_third"]) > 0


def test_parameter_and_domain_validation_rejects_invalid_reductions():
    for n, q in ((0, 8), (1, 7), (1, 4)):
        with pytest.raises(ValueError):
            dense_source_certificate(n, q)
    with pytest.raises(ValueError):
        dense_source_certificate(1, 8, 3)
    with pytest.raises(ValueError):
        correlated_basis_fault_reduction_bound(1, 8, markov_multiplier=1)
    with pytest.raises(ValueError):
        group_vector(16, 2, 4)
    with pytest.raises(ValueError):
        group_index((4,), 4)
    for index in range(16):
        assert group_index(group_vector(index, 2, 4), 4) == index
