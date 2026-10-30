from fractions import Fraction as F
from itertools import product

import numpy as np
import pytest

from decoder_margin import (arbitrary_pauli_plan, lift, recommended_cutoff,
                           short_word_plan, tail_bound, verify_ball)
from margin_controls import (complete_root_quotient, control, cycle_decoder,
    cycle_model, hermitian_word, matrix, native_pilot, pullback, repetition_quotient)


@pytest.mark.parametrize("length", [3, 4, 5, 7])
def test_actual_majorana_cycle_has_repetition_relation_and_nonlinear_decoder(length):
    model = cycle_model(length, F(1, 32))
    decoder = cycle_decoder(model)
    assert model.label((1 << length)-1) == 0
    check = verify_ball(model, decoder, (length-1)//2)
    assert check["status"] == "FINITE_EXHAUSTIVE_CHECK"
    assert not check["all_size_proof"]
    assert verify_ball(model, decoder, (length+1)//2)["status"] == "REJECTED"
    if length == 5:
        a, b = model.label(3), model.label(12)
        assert decoder(a ^ b) != decoder(a) ^ decoder(b)


@pytest.mark.parametrize("length", [3, 4, 5])
@pytest.mark.parametrize("beta", [F(0), F(1, 64), F(1, 8)])
def test_factorial_moment_tail_against_actual_native_state(length, beta):
    model = cycle_model(length, beta, [F((-1)**i, i+1) for i in range(length)])
    state = native_pilot(model)
    for cutoff in range(-1, length+1):
        mass = sum(abs(a)**2 for y, a in enumerate(state) if y.bit_count() > cutoff)
        assert mass <= float(tail_bound(model, cutoff)) + 1e-13


@pytest.mark.parametrize("word", [1, 2, 4, 8, 16, 3, 5, 9, 17])
def test_short_word_good_columns_and_native_error_with_nonlinear_decoder(word):
    model = cycle_model(5, F(1, 16), [1, -1, F(1, 2), 1, F(-1, 3)])
    decoder = cycle_decoder(model)
    q = hermitian_word(model, word)
    cutoff = 2-word.bit_count()
    data = control(model, decoder, q, word, cutoff)
    assert data["good_column_error"] < 1e-14
    gap = abs(data["actual_expectation"] - data["canonical_expectation"])
    assert gap <= data["short_word_error_bound_from_actual_mass"] + 1e-12


@pytest.mark.parametrize("word", range(32))
def test_all_physical_word_observables_obey_arbitrary_margin_block_identity(word):
    model = cycle_model(5, F(1, 16))
    decoder = cycle_decoder(model)
    observable = hermitian_word(model, word)
    plan = arbitrary_pauli_plan(model, decoder, observable, 2, cutoff=1)
    assert plan["classical_reduction_budget_met"]
    assert not plan["decoder_contract_verified_by_plan"]
    assert not plan["production_estimator_executed"]
    actual = pullback(model, decoder, observable)
    lifted = plan["lifted_pauli"]
    other = np.zeros_like(actual) if lifted is None else matrix(lifted, model.pilot.m)
    inside = [0, 1, 2, 4, 8, 16]
    assert np.max(abs((actual-other)[np.ix_(inside, inside)])) < 1e-14
    state = native_pilot(model)
    error = abs(np.vdot(state, (actual-other) @ state))
    assert error**2 <= float(plan["transfer_error_squared_upper"]) + 1e-12


def test_factor_two_margin_cannot_be_dropped_even_for_actual_polynomial_pilot():
    model = cycle_model(4, F(1, 16))
    decoder = cycle_decoder(model)
    assert verify_ball(model, decoder, 1)["status"] == "FINITE_EXHAUSTIVE_CHECK"
    q = hermitian_word(model, 5)
    plan = arbitrary_pauli_plan(model, decoder, q, 1, cutoff=1)
    assert plan["status"] == "INCONCLUSIVE_INSUFFICIENT_DECODING_MARGIN"
    # This is the normalized degree-one native filter H|0>, not a hidden oracle.
    state = np.zeros(16)
    state[[1, 2, 4, 8]] = 0.5
    actual = pullback(model, decoder, q)
    guessed = matrix(lift(model, q, 5), 4)
    assert np.vdot(state, actual @ state) == pytest.approx(1)
    assert np.vdot(state, guessed @ state) == pytest.approx(0.5)


def test_average_correctness_cannot_certify_uniform_radius():
    model = cycle_model(5, F(0))
    bad_decoder = lambda syndrome: 0
    assert native_pilot(model)[0] == 1
    assert verify_ball(model, bad_decoder, 1)["status"] == "REJECTED"
    plan = short_word_plan(model, model.paulis[0], 1, 2)
    assert plan["classical_reduction_budget_met"]
    assert plan["status"] == "CONDITIONAL_ON_UNIFORM_DECODER_CONTRACT"
    assert not plan["decoder_contract_verified_by_plan"]


def test_out_of_span_pauli_is_not_assumed_to_have_a_representative():
    model = cycle_model(5, F(1, 16))
    decoder = cycle_decoder(model)
    image = {model.label(y) for y in range(32)}
    syndrome = next(s for s in range(1 << (2*model.n)) if s not in image)
    x, z = syndrome & ((1 << model.n)-1), syndrome >> model.n
    q = x, z, (x & z).bit_count() % 2
    plan = arbitrary_pauli_plan(model, decoder, q, 2, cutoff=1)
    assert plan["lifted_pauli"] is None
    assert plan["canonical_plan"]["status"] == "zero_on_truncated_ball"
    assert np.max(abs(pullback(model, decoder, q))) == 0


@pytest.mark.parametrize("v", [3, 4, 5, 8])
def test_native_growing_degree_family_has_exact_repetition_decoder(v):
    model = complete_root_quotient(v, F(1, 64))
    m = v*(v-1)//2
    decoder = cycle_decoder(model)
    assert model.pilot.m == m and model.n == m-1
    assert model.pilot.degree == 2*(v-2)
    assert model.label((1 << m)-1) == 0
    assert verify_ball(model, decoder, 1)["status"] == "FINITE_EXHAUSTIVE_CHECK"
    for y in [0, 1, 3, (1 << (m//2))-1]:
        expected = min((y, y ^ ((1 << m)-1)), key=lambda a: (a.bit_count(), a))
        assert decoder(model.label(y)) == expected


def test_caps_invalid_contracts_and_phase_errors_are_not_accepted():
    model = cycle_model(5, F(1, 16))
    decoder = cycle_decoder(model)
    with pytest.raises(ValueError, match="cap"):
        verify_ball(model, decoder, 2, max_masks=15)
    with pytest.raises(ValueError, match="radius"):
        arbitrary_pauli_plan(model, decoder, model.paulis[0], 6, 1)
    with pytest.raises(ValueError, match="represent"):
        lift(model, model.paulis[0], 2)
    with pytest.raises(ValueError, match="Hermitian"):
        lift(model, (1, 1, 0), 1)
    with pytest.raises(ValueError, match="central"):
        repetition_quotient(3, [(0, 1)], F(1, 16))
    with pytest.raises(ValueError, match="exact"):
        recommended_cutoff(model, 0.125)


def test_recommended_radius_has_sufficient_tail_and_does_not_claim_decode_success():
    model = complete_root_quotient(8, F(1, 64))
    cutoff = recommended_cutoff(model, F(1, 8))
    assert tail_bound(model, cutoff) <= F(1, 8)**2/256
    plan = arbitrary_pauli_plan(model, cycle_decoder(model), model.paulis[0],
                                (model.pilot.m-1)//2, epsilon=F(1, 8))
    assert plan["status"] == "INCONCLUSIVE_INSUFFICIENT_DECODING_MARGIN"


def test_bad_or_approximate_guarantee_is_not_promoted_by_small_finite_error():
    model = cycle_model(5, F(1, 8))
    plan = short_word_plan(model, model.paulis[0], 1, 1, epsilon=F(1, 1000))
    assert not plan["transfer_budget_met"]
    assert not plan["classical_reduction_budget_met"]


def test_live_precision_is_not_a_coarse_zero_readout():
    model = complete_root_quotient(32, F(1, 128))
    plan = arbitrary_pauli_plan(model, cycle_decoder(model), model.paulis[-1],
                                (model.pilot.m-1)//2, epsilon=F(1, 4096))
    assert plan["classical_reduction_budget_met"]
    assert plan["pilot_cutoff"] == 31
    assert plan["canonical_plan"]["status"] == "marked_cluster_comparator"
    assert plan["canonical_plan"]["estimate"] is None
    assert not plan["production_estimator_executed"]
