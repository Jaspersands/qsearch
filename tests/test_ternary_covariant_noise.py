from fractions import Fraction
from itertools import product
import math
import random

import numpy as np
import pytest

from cyclotomic_fiber_receiver import inverse_frequency_coordinates, native_source
from ternary_covariant_noise import (
    CovariantRecord, TaggedEquation, apply_qutrit_tape, bkw_collision_ledger, chosen_radix_plan,
    collimate_tagged, compression_character, decode_chosen_radix,
    heldout_gate, heldout_score, noise_character, noise_probability, phase,
    native_identifiability_ledger,
    physical_readout_control, projected_noise_character, radix_access_ledger,
    qutrit_qft_recipe, receiver_recipe, scalar_projection_gate, simulated_record,
)


@pytest.mark.parametrize("q", [3, 9, 27])
def test_noise_law_fourier_support_and_collision_are_exactly_the_physical_receiver(q):
    probabilities = np.array([[noise_probability(q, a, b) for b in range(q)] for a in range(q)])
    assert abs(probabilities.sum()-1) < 1e-12
    assert abs(q*q*np.sum(probabilities**2)-5/3) < 1e-11
    characteristic = np.fft.ifftn(probabilities)*q*q
    for a, b in product(range(q), repeat=2):
        assert abs(characteristic[a, b]-float(noise_character(q, (a, b)))) < 1e-12
    marginal = probabilities.sum(axis=1)
    assert np.max(abs(marginal-np.array([(1+(2/3)*phase(a,q).real)/q for a in range(q)]))) < 1e-12
    assert np.max(abs(probabilities-marginal[:, None]*marginal[None, :])) > .01/(q*q)


@pytest.mark.parametrize("level", [2, 4, 6])
def test_actual_native_ring_state_matches_full_root_covariant_noise_law(level):
    q = 3**(level//2)
    source = native_source([[inverse_frequency_coordinates(1, q-2, level),
                             inverse_frequency_coordinates(q-1, 2, level)]], level)
    result = physical_readout_control(source, (q-1, q//3))
    assert result["modulus"] == q and result["outcome_probability_error"] < 1e-12
    assert result["all_outcomes_kept"] and not result["source_substituted_by_field_shadow"]
    assert result["gate_replay_amplitude_error"] < 1e-12


@pytest.mark.parametrize("digits", [1, 2, 3])
def test_inverse_root_QFT_recipe_on_every_basis_vector_not_only_native_phases(digits):
    q = 3**digits
    for x in range(q):
        state = np.zeros(q, dtype=complex); state[x] = 1
        actual = apply_qutrit_tape(state, digits, qutrit_qft_recipe(digits))
        expected = np.array([phase(-x*y, q)/math.sqrt(q) for y in range(q)])
        assert np.max(abs(actual-expected)) < 1e-12


def test_scalable_recipe_is_quadratic_size_with_no_unknown_state_inverse():
    for r in (1, 4, 32, 128):
        recipe = receiver_recipe(r)
        assert len(recipe["gates"]) == 1+2*(r+r*(r-1)//2+r//2)
        assert recipe["clean_qutrit_ancillas"] == 2*r-1
        assert not recipe["unknown_state_preparation_or_inverse_required"]


def test_final_field_covariant_readout_is_the_existing_MUB_incidence_channel():
    from ternary_incidence_decoder import measurement_probabilities
    first, second, secret = (1, 2), (2, 2), (1, 0)
    for y1, y2 in product(range(3), repeat=2):
        basis, outcome = (2*y1-y2) % 3, (y2-y1) % 3
        record = CovariantRecord(first, second, (y1, y2), 3)
        assert abs(record.probability(secret)-measurement_probabilities(first, second, secret, 3, basis)[outcome]/3) < 1e-12


@pytest.mark.parametrize("q", [9, 27])
def test_every_smaller_modulus_projection_of_paired_noise_is_uniform(q):
    d = q//3
    projected = np.zeros((d, d))
    for a, b in product(range(q), repeat=2):
        projected[a % d, b % d] += noise_probability(q, a, b)
    assert np.max(abs(projected-1/(d*d))) < 1e-12
    assert noise_character(q, (q//d, 0)) == 0


@pytest.mark.parametrize("q", [3, 9])
def test_complete_scalar_classification_for_every_one_qutrit_weight(q):
    for weights in product(range(q), repeat=2):
        gate = scalar_projection_gate(q, (weights,))
        chars = [projected_noise_character(q, (weights,), t) for t in range(q)]
        if gate["classification"] == "zero_statistic":
            assert chars == [Fraction(1)]*q
        elif gate["classification"] == "uniform_on_noise_image_subgroup":
            step = gate["noise_image_step"]
            assert chars == [Fraction(int(t*step % q == 0)) for t in range(q)]
        elif gate["classification"] == "exactly_uniform_full_modulus":
            assert chars == [Fraction(1)]+[Fraction(0)]*(q-1)
        else:
            support = gate["surviving_dual_frequencies"]
            assert chars == [Fraction(1) if t == 0 else Fraction(1, 3) if t in support else Fraction(0)
                             for t in range(q)]


def test_every_small_two_qutrit_scalar_projection_matches_character_classification():
    q = 9
    weight_pairs = [(a, b) for a, b in product(range(q), repeat=2)]
    for i, first in enumerate(weight_pairs):
        for second in weight_pairs[i::13]:
            gate = scalar_projection_gate(q, (first, second))
            chars = [projected_noise_character(q, (first, second), t) for t in range(q)]
            if gate["classification"] == "common_unit_scaled_root_directions":
                expected = Fraction(1, 3)**gate["active_original_qutrits"]
                assert all(chars[t] == expected for t in gate["surviving_dual_frequencies"])
                assert sum(bool(x) for x in chars) == 3
            elif gate["classification"] == "exactly_uniform_full_modulus":
                assert sum(bool(x) for x in chars) == 1
            else:
                step = gate["noise_image_step"]
                assert chars == [Fraction(int(t*step % q == 0)) for t in range(q)]


def test_nonunit_or_generic_gaussian_weights_destroy_scalar_signal_but_signed_sums_pay_bias():
    assert scalar_projection_gate(81, ((1, 0), (2, 0)))["classification"] == "exactly_uniform_full_modulus"
    assert scalar_projection_gate(81, ((1, 3),))["classification"] == "exactly_uniform_full_modulus"
    assert not scalar_projection_gate(81, ((3, 0),))["secret_information_in_this_scalar"]
    gate = scalar_projection_gate(81, ((1, 0), (80, 0), (1, 80)))
    assert gate["fourier_bias"] == "1/27" and gate["inverse_squared_bias_sampling_scale"] == "729"


def test_invertible_mixing_has_uniform_marginals_but_keeps_joint_information():
    q, rows = 9, ((1, 2), (1, 3))
    assert (rows[0][0]*rows[1][1]-rows[0][1]*rows[1][0]) % q == 1
    assert all(compression_character(q, rows, (t, 0)) == 0 for t in range(1, q))
    assert all(compression_character(q, rows, (0, t)) == 0 for t in range(1, q))
    assert compression_character(q, rows, (3, 7)) == Fraction(1, 3)
    assert sum(compression_character(q, rows, f)**2 for f in product(range(q), repeat=2)) == Fraction(5, 3)
    transformed = np.zeros((q, q))
    for a, b in product(range(q), repeat=2):
        transformed[(a+2*b) % q, (a+3*b) % q] += noise_probability(q, a, b)
    assert np.max(abs(transformed.sum(axis=0)-1/q)) < 1e-12
    assert np.max(abs(transformed-1/(q*q))) > .01/(q*q)


def test_label_error_independence_and_full_pair_likelihood_not_three_independent_equations():
    q, secret = 9, (7,)
    noise = {(a, b): noise_probability(q, a, b) for a, b in product(range(q), repeat=2)}
    for a, c in product(range(q), repeat=2):
        for e in ((0, 0), (1, 3), (8, 2)):
            record = CovariantRecord((a,), (c,), ((a*secret[0]+e[0]) % q, (c*secret[0]+e[1]) % q), q)
            assert record.residual(secret) == e
            assert abs(record.probability(secret)-noise[e]) < 1e-15


def test_heldout_character_score_means_for_all_secret_orders_not_only_primitive_difference():
    q, true = 9, (2,)
    for wrong in ((2,), (3,), (5,)):
        total = 0.
        for a, c in product(range(q), repeat=2):
            for e in product(range(q), repeat=2):
                record = CovariantRecord((a,), (c,), ((a*2+e[0]) % q, (c*2+e[1]) % q), q)
                total += noise_probability(q, *e)*heldout_score((record,), wrong)/(q*q)
        assert abs(total-(1 if wrong == true else 0)) < 1e-11


def test_chosen_radix_decoder_has_actual_growing_root_recovery_no_secret_enumeration():
    n, digits, q, repeats = 2, 12, 3**12, 192
    secret, rng, batches = (127493, 381742), random.Random(81103), []
    for _, _, first in chosen_radix_plan(n, digits):
        batches.append([simulated_record(first, tuple(rng.randrange(q) for _ in range(n)), secret, q, rng)[0]
                        for _ in range(repeats)])
    result = decode_chosen_radix(batches, n, digits)
    assert result["secret"] == secret and not result["random_native_source_decoder_supplied"]
    assert len(result["decisions"]) == n*digits


def test_radix_decoder_rejects_random_frequency_substitution_and_ledgers_charge_it():
    record = CovariantRecord((1,), (2,), (0, 0), 9)
    with pytest.raises(ValueError, match="substituted"):
        decode_chosen_radix(((record,), (record,)), 1, 2)
    ledger = radix_access_ledger(8, 32, 16)
    assert ledger["expected_native_qutrits_for_rejection_compiling_this_exact_schedule"] == str(
        ledger["chosen_qutrits_required"]*3**256)
    assert Fraction(ledger["native_exact_first_frequency_probability"]) == Fraction(1, 3**256)
    assert not ledger["random_native_label_access_is_chosen_query_access"]
    M = ledger["chosen_frequency_samples_per_digit"]
    assert 2*8*32*math.exp(-M/24) <= 2**-16


def test_chosen_radix_decoder_handles_every_small_secret_without_hidden_truth_input():
    q = 9
    # Algebraic estimator control, not a claim about the physical noise law:
    # a positive aligned empirical phase mean suffices for each radix step.
    for secret in range(q):
        batches = []
        for _, _, first in chosen_radix_plan(1, 2):
            center = first[0]*secret % q
            outcomes = [center]*5+[(center+q//3) % q, (center+2*q//3) % q]
            batches.append([CovariantRecord(first, (0,), (b, 0), q) for b in outcomes])
        assert decode_chosen_radix(batches, 1, 2)["secret"] == (secret,)


def test_heldout_gate_does_not_grant_training_reuse_or_candidate_generation():
    gate = heldout_gate(1024, 5)
    assert gate["false_acceptance_union_bound_approximation"] < 1e-9
    assert gate["candidates_independent_of_this_holdout_required"]
    assert not gate["adaptive_reuse_or_label_selected_holdout_certified"]
    assert not gate["efficient_candidate_generation_supplied"]


def test_classical_collimation_exact_noise_law_keeps_every_residue_with_phase_tag():
    q, counts = 9, {}
    marginal = [(1+(2/3)*phase(e, q).real)/q for e in range(q)]
    for secret in range(q):
        for e1, e2 in product(range(q), repeat=2):
            inputs = tuple(TaggedEquation((a,), (a*secret+e) % q, q, Fraction(1, 3), Fraction(0), frozenset((i,)))
                           for i, (a, e) in enumerate(((1, e1), (4, e2))))
            output, ledger = collimate_tagged(inputs)
            assert ledger["signed_weights"] == (-1, 1) and output.first == (1,)
            assert output.bias == Fraction(1, 9)
            key = secret, ledger["observed_residue"], output.outcome
            counts[key] = counts.get(key, 0)+marginal[e1]*marginal[e2]
        for residue, outcome in product(range(3), repeat=2):
            record = TaggedEquation((1,), outcome, 3, Fraction(1, 9), -Fraction(residue, 9), frozenset((0, 1)))
            assert abs(counts[secret, residue, outcome]-record.probability((secret % 3,))/3) < 1e-12


def test_collimation_preserves_nonzero_parent_phase_tags_and_charges_inactive_parents():
    inputs = (TaggedEquation((0,), 5, 9, Fraction(1, 9), Fraction(2, 9), frozenset((0, 1))),
              TaggedEquation((2,), 7, 9, Fraction(1, 3), Fraction(1, 9), frozenset((2,))))
    output, ledger = collimate_tagged(inputs)
    assert ledger["signed_weights"] == (1, 0)
    assert output.origins == frozenset((0, 1, 2)) and output.bias == Fraction(1, 9)
    assert output.noise_phase_turns == 0 and ledger["original_qutrits_charged"] == 3


def test_shared_noise_or_field_shadow_cannot_be_treated_as_fresh_collimation_inputs():
    record = TaggedEquation((1,), 3, 9, Fraction(1, 3), Fraction(0), frozenset((0,)))
    with pytest.raises(ValueError, match="shared original"):
        collimate_tagged((record, record))
    field = TaggedEquation((1,), 0, 3, Fraction(1, 3), Fraction(0), frozenset((1,)))
    with pytest.raises(ValueError, match="above3"):
        collimate_tagged((field, field))


def test_exact_BKW_ledger_does_not_offer_free_collisions_or_independent_reused_parents():
    ledger = bkw_collision_ledger(8, 32, 4096, eliminated_coordinates=1, leaves=8)
    assert Fraction(ledger["exact_coordinate_collisions_probability_upper"]) == Fraction(math.comb(4096, 2), 3**32)
    assert ledger["surviving_character_bias"] == "1/6561"
    assert ledger["inverse_squared_bias_sampling_scale"] == str(9**8)
    assert not ledger["low_modulus_bucket_match_is_full_modulus_elimination"]
    assert not ledger["shared_combined_records_are_independent"]


def test_native_receiver_is_information_sufficient_with_polynomial_surplus_not_a_fast_search():
    n, r, k = 8, 32, 16
    ledger = native_identifiability_ledger(n, r, k)
    log_union = n*r*math.log(3)-2*ledger["native_qutrit_samples"]/81
    assert log_union <= -k*math.log(2)
    assert ledger["all_secret_search_required_by_reference_decoder"]
    assert not ledger["efficient_random_label_candidate_search_supplied"]
    assert not ledger["information_sufficiency_is_a_quantum_speedup"]


def test_zero_final_frequency_is_not_secret_information_despite_nonzero_noise_bias():
    record = TaggedEquation((0, 0), 1, 3, Fraction(1, 6561), Fraction(74, 81), frozenset(range(27)))
    probabilities = [record.probability(s) for s in product(range(3), repeat=2)]
    assert max(probabilities)-min(probabilities) == 0


def test_invalid_inputs_fail_closed_instead_of_dropping_correlations_or_modulus():
    with pytest.raises(ValueError):
        noise_probability(8, 0, 0)
    with pytest.raises(ValueError):
        CovariantRecord((1,), (2,), (True, 0), 9)
    with pytest.raises(ValueError):
        scalar_projection_gate(9, ())
    with pytest.raises(ValueError):
        compression_character(9, ((1, 2, 3),), (1,))
    with pytest.raises(ValueError):
        chosen_radix_plan(True, 2)
