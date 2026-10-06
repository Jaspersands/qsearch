from dataclasses import replace
from fractions import Fraction
from itertools import permutations, product
import math
import random

import numpy as np
import pytest

from cyclotomic_fiber_receiver import frequency_coordinates
from ternary_carry_packets import compile_packet
from ternary_incidence_decoder import (
    IncidenceDecoder, IncidenceSample, decode_native_control, exact_zero_support,
    exclusion_ledger, feature_basis, field_probabilities, field_sample,
    first_kernel_line, full_source_control, incidence_polynomial,
    local_line_matrix, low_shadow_countercontrol, measurement_probabilities,
    sample_budget, sample_native_line,
)
from ternary_quotient_decoder import Span


@pytest.mark.parametrize("modulus", [3, 9, 27])
def test_all_integer_line_maps_are_bijections_not_just_field_maps(modulus):
    for digits in permutations(range(3)):
        M = local_line_matrix(digits)
        assert abs(M[0][0]*M[1][1]-M[0][1]*M[1][0]) == 1
        outputs = {tuple(sum(row[j]*v[j] for j in range(2)) % modulus for row in M)
                   for v in product(range(modulus), repeat=2)}
        assert len(outputs) == modulus**2


def test_entire_unfiltered_native_source_and_every_affine_branch():
    record = full_source_control()
    assert record["native_source_batches_enumerated"] == 729
    assert record["all_affine_branches_replayed"] == 2187
    assert record["conditional_low_and_outcome_strata"] == 27
    assert record["parent_secret"] > record["retained_secret_residue"]


@pytest.mark.parametrize("level", [3, 5, 7, 9, 19])
def test_actual_growing_native_packet_matches_lower_even_source_amplitudes(level):
    rng = random.Random(61100+level)
    line = sample_native_line(2, level, rng)
    for y, a, b in zip(line.native_output_labels, line.first, line.second):
        assert frequency_coordinates(y, level-1) == (a, b)
    # Independent rational trace-pairing evaluator, not hierarchy.derivative.
    from cyclotomic_rescaling_gate import ideal_chart
    h0, _, h1 = ideal_chart(level)[0]
    packet = compile_packet([[(rng.randrange(h0), rng.randrange(h1)) for _ in range(2)] for _ in range(4)], level)
    packet = replace(packet, syndrome=tuple(2 for _ in packet.pivots))
    line = first_kernel_line(packet, tuple(1 for _ in range(packet.retained-1)))
    parent = packet.phase_modulus
    secret = (parent-1, parent-2)
    native = [packet.component_frequencies(word) for word in line.physical_words]
    difference = [sum(s*(a-b) for s, a, b in zip(secret, row, native[0])) % parent for row in native]
    lower = [0]+[sum(s*f for s, f in zip(secret, row)) % line.modulus for row in (line.first, line.second)]
    assert all(a == 3*b for a, b in zip(difference, lower))
    assert line.resources()["qutrits_measured"] == packet.consumed-1
    assert not line.resources()["intermediate_odd_source_acquisition_charged"]


def test_field_measurement_exact_law_and_every_legal_cubic_constraint():
    for a, b, s, basis in product(range(3), repeat=4):
        first, second = ((a+b) % 3,), ((2*a+b) % 3,)
        numeric = measurement_probabilities(first, second, (s,), 3, basis)
        exact = field_probabilities((a,), (b,), (s,), basis)
        assert np.allclose(numeric, list(map(float, exact)), atol=2e-14)
        assert abs(sum(numeric)-1) < 2e-14
        for outcome, probability in enumerate(exact):
            if probability:
                assert IncidenceSample((a,), (b,), basis, outcome).value((s,)) == 0


def test_symbolic_reduced_cubic_matches_direct_constraint_on_every_field_point():
    rng = random.Random(61200)
    for _ in range(50):
        sample = IncidenceSample(tuple(rng.randrange(3) for _ in range(3)),
                                 tuple(rng.randrange(3) for _ in range(3)), rng.randrange(3), rng.randrange(3))
        polynomial = incidence_polynomial(sample)
        assert all(sum(a) <= 3 and max(a) <= 2 for a in polynomial)
        for trial in product(range(3), repeat=3):
            value = sum(c*math.prod(x**a for x, a in zip(trial, powers)) for powers, c in polynomial.items()) % 3
            assert value == sample.value(trial)


@pytest.mark.parametrize("n,secret", [(1, (0,)), (1, (1,)), (1, (2,)), (2, (0, 0)), (2, (1, 2)), (3, (2, 0, 1))])
def test_complete_feasible_support_spans_entire_evaluation_hyperplane(n, secret):
    decoder = IncidenceDecoder(n)
    vectors = tuple(product(range(3), repeat=n))
    for a, b in product(vectors, repeat=2):
        for basis in range(3):
            for o, probability in enumerate(field_probabilities(a, b, secret, basis)):
                if probability:
                    decoder.add(IncidenceSample(a, b, basis, o))
    result = decoder.result()
    assert result["status"] == "FIELD_SECRET_CERTIFIED"
    assert result["rank"] == len(feature_basis(n))-1
    assert result["secret"] == secret


def test_rank_escape_bound_against_every_nonzero_one_variable_functional():
    for s in range(3):
        basis = feature_basis(1)
        evaluation = tuple(s**a[0] % 3 for a in basis)
        for functional in product(range(3), repeat=len(basis)):
            if not any(functional) or functional == evaluation or functional == tuple(2*x % 3 for x in evaluation):
                continue
            escape = Fraction(0)
            for a, b, choice in product(range(3), repeat=3):
                for o, p in enumerate(field_probabilities((a,), (b,), (s,), choice)):
                    sample = IncidenceSample((a,), (b,), choice, o)
                    vector = incidence_polynomial(sample)
                    if sum(functional[j]*vector.get(exponent, 0) for j, exponent in enumerate(basis)) % 3:
                        escape += p/27
            assert escape >= Fraction(2, 81)


@pytest.mark.parametrize("n", [1, 2, 4, 8])
def test_decoder_uses_fresh_actual_native_batches_and_charges_consumption(n):
    result = decode_native_control(n, 61300+n)
    assert result["result"]["status"] == "FIELD_SECRET_CERTIFIED"
    assert result["odd_native_qutrits_consumed"] == (n+1)*result["source_batches"]
    assert not result["secret_given_to_classical_decoder"]
    assert not result["result"]["complete_parent_secret_recovered"]
    assert not result["result"]["secret_assignments_enumerated"]


def test_insufficient_and_inconsistent_constraints_never_emit_secret():
    decoder = IncidenceDecoder(1)
    assert decoder.result()["status"] == "INSUFFICIENT_CONSTRAINT_RANK"
    # Basis0, beta0 makes alpha*x-outcome=0 a deterministic exact equation.
    decoder.add(IncidenceSample((1,), (0,), 0, 0))
    decoder.add(IncidenceSample((1,), (0,), 0, 1))
    decoder.add(IncidenceSample((0,), (1,), 0, 1))
    assert decoder.result()["status"] == "INCONSISTENT_FIELD_DATA"
    assert decoder.result()["secret"] is None


def test_non_evaluation_nullvector_is_rejected():
    decoder = IncidenceDecoder(1)
    decoder.span.add([0, 1, 0])
    decoder.span.add([2, 0, 1])  # Nullvector(1,0,1) cannot be (1,s,s^2).
    assert decoder.result()["status"] == "NULLVECTOR_IS_NOT_A_SECRET_EVALUATION"


@pytest.mark.parametrize("bad", [9, True, 3.0, 1])
def test_non_field_or_invalid_modulus_is_rejected(bad):
    with pytest.raises(ValueError):
        IncidenceSample((1,), (2,), 0, 0, phase_modulus=bad)
    with pytest.raises(ValueError):
        field_sample(sample_native_line(1, 5, random.Random(61390)), (1,), random.Random(1))


@pytest.mark.parametrize("q", [3, 9, 27])
def test_growing_root_exact_zeros_are_rare_and_match_independent_Born_amplitudes(q):
    any_zero, per_outcome = 0, {pair: 0 for pair in product(range(3), repeat=2)}
    for a, c in product(range(q), repeat=2):
        zeros = []
        for b in range(3):
            probabilities = measurement_probabilities((a,), (c,), (1,), q, b)
            for o, probability in enumerate(probabilities):
                zero = exact_zero_support(a, c, q, b, o)
                assert zero == (probability < 1e-25)
                per_outcome[b, o] += zero
                zeros.append(zero)
        any_zero += any(zeros)
    assert set(per_outcome.values()) == {2}
    assert any_zero == 9


def test_independent_trial_elimination_probability_weights_actual_true_outcomes():
    q = 3
    elimination = 0.
    for a1, c1, a2, c2, b in product(range(q), range(q), range(q), range(q), range(3)):
        for o, probability in enumerate(measurement_probabilities((a1,), (c1,), (1,), q, b)):
            elimination += probability*exact_zero_support(a2, c2, q, b, o)/(3*q**4)
    assert abs(elimination-2/q**2) < 1e-12
    ledger = exclusion_ledger(8, 1000)
    assert Fraction(ledger["independent_trial_elimination_union_bound"]) == Fraction(2000, 3**16)
    assert not ledger["positive_likelihood_information_ruled_out"]
    assert not ledger["general_classical_or_quantum_decoder_lower_bound"]


def test_actual_level5_native_state_falsifies_low_digit_shadow_constraint():
    record = low_shadow_countercontrol()
    predicted = (2-2*math.cos(4*math.pi/9))/9
    assert record["false_constraint_value_at_true_secret"] == 2
    assert abs(record["actual_outcome_probabilities"][1]-predicted) < 1e-14
    assert abs(record["actual_outcome_probabilities"][2]-predicted) < 1e-14
    assert not record["field_shadow_transfer_admitted"]


def test_budget_charges_full_feature_dimension_and_confidence():
    for n in (1, 2, 8, 12, 1024):
        D = 1+n+n*(n+1)//2+n*(n-1)+math.comb(n, 3)
        budget = sample_budget(n, 20)
        assert budget["feature_dimension"] == D
        assert budget["sufficient_fresh_IID_samples"] == 81*(D-1+80)
    for bad in (0, True, 1.5):
        with pytest.raises(ValueError):
            sample_budget(2, bad)


def test_frozen_sample_copies_mutable_input_and_rejects_noncanonical_fields():
    alpha = [1, 2]
    sample = IncidenceSample(alpha, [0, 1], 2, 0)
    alpha[0] = 0
    assert sample.alpha == (1, 2)
    for args in [((True,), (1,), 0, 0), ((3,), (1,), 0, 0), ((1,), (), 0, 0), ((1,), (1,), 3, 0)]:
        with pytest.raises(ValueError):
            IncidenceSample(*args)
    with pytest.raises(ValueError):
        measurement_probabilities((1,), (2,), (True,), 3, 0)
    with pytest.raises(ValueError):
        measurement_probabilities((3,), (2,), (1,), 3, 0)
