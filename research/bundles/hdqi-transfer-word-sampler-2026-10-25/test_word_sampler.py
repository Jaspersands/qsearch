from fractions import Fraction as Q
from itertools import product
import random
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent/"hdqi-hidden-mode-access-2026-10-25"))
from controls import native_matrices, reference_matrix
from word_sampler import WordSampler, repeated_transfer_bound


def dense_product(couplings, radius, parameters):
    m, d = len(couplings), 1 << len(couplings)
    operators = [native_matrices([int(i == j) for j in range(m)], radius, 1)[0] for i in range(m)]
    answer = np.eye(d)
    for u in parameters:
        transfer = np.zeros((d, d), dtype=complex)
        for mask in range(d):
            sites = [i for i in range(m) if mask >> i & 1]
            if any(b-a <= radius for a, b in zip(sites, sites[1:])):
                continue
            term = np.eye(d, dtype=complex)
            for i in sites:
                term = term @ (-float(u*couplings[i])*operators[i])
            transfer += term
        answer = answer @ transfer
    return answer


@pytest.mark.parametrize("m,radius,parameters", [(3, 1, [Q(1, 3)]),
    (4, 2, [Q(1, 3), Q(-2, 5)]), (5, 2, [Q(1, 4), Q(2, 7)]),
    (7, 2, [Q(1, 3), Q(1, 3)]), (5, 2, [Q(1, 3), Q(-1, 4), Q(1, 5)])])
@pytest.mark.parametrize("basis", ["Z", "X"])
def test_full_native_vector_and_norm(m, radius, parameters, basis):
    couplings = [Q((-1)**i, 1+i % 2) for i in range(m)]
    sampler = WordSampler(couplings, radius, parameters, basis=basis)
    expected = dense_product(couplings, radius, parameters)[:, 0]
    if basis == "X":
        expected = np.array([sum((-1)**((x & y).bit_count())*a for y, a in enumerate(expected))
                             for x in range(1 << m)])
    actual = np.array([float(sampler.amplitude(tuple(x >> i & 1 for i in range(m))))
                       for x in range(1 << m)])
    assert np.linalg.norm(actual-expected) < 1e-12
    assert abs(float(sampler.norm_squared)-np.vdot(expected, expected)) < 1e-11


def test_negative_crossing_sign_cannot_be_dropped():
    sampler = WordSampler([1]*3, 1, [Q(1, 3), Q(2, 5)])
    # The full-path word gets the opposite sign from unsigned independent layers.
    assert sampler.amplitude((1, 1, 1)) > 0
    assert Q(-1, 3)**2*Q(-2, 5)+Q(-2, 5)**2*Q(-1, 3) < 0


@pytest.mark.parametrize("basis", ["Z", "X"])
def test_exact_probabilities_and_actual_samples(basis):
    sampler = WordSampler([1]*5, 2, [Q(1, 3), Q(1, 7)], basis=basis)
    words = list(product((0, 1), repeat=5))
    assert sum(map(sampler.probability, words)) == 1
    rng = random.Random(714)
    for _ in range(30):
        assert sampler.probability(sampler.sample(rng)) > 0


def test_scalar_zero_product_rejected():
    with pytest.raises(ValueError, match="zero vector"):
        WordSampler([Q(3, 5), Q(4, 5)], 1, [1, -1])


@pytest.mark.parametrize("basis", ["Z", "X"])
def test_every_conditional_mass_against_full_output_distribution(basis):
    sampler = WordSampler([1, -1, Q(1, 2), 1], 2, [Q(1, 3), Q(-2, 7)], basis=basis)
    words = list(product((0, 1), repeat=4))
    for length in range(4):
        for prefix in product((0, 1), repeat=length):
            row = {0: Q(1)}
            for site, bit in enumerate(prefix):
                row = sampler._advance(row, site, bit)
            for bit in (0, 1):
                branch = sampler._advance(row, length, bit)
                right = sampler.right[length+1]
                mass = sum((a*b*right[i][j] for i, a in branch.items() for j, b in branch.items()), Q(0))
                expected = sum((sampler.amplitude(w)**2 for w in words if w[:length+1] == prefix+(bit,)), Q(0))
                assert mass == expected


def test_no_factors_is_native_vacuum():
    sampler = WordSampler([1]*5, 2, [])
    assert sampler.probability((0,)*5) == 1
    assert sampler.sample(random.Random(1)) == (0,)*5


@pytest.mark.parametrize("m,radius,beta,factors", [(5, 2, Q(1, 10), 2),
    (7, 2, Q(1, 5), 2), (6, 3, Q(1, 4), 3)])
def test_repeated_transfer_thermal_bound_on_full_native_state(m, radius, beta, factors):
    couplings = [Q((-1)**i, 1+i % 2) for i in range(m)]
    bound = repeated_transfer_bound(couplings, beta, factors)
    sampler = WordSampler(couplings, radius, [bound["transfer_parameter"]]*factors)
    vector = np.array([float(sampler.amplitude(tuple(x >> i & 1 for i in range(m))))
                       for x in range(1 << m)])
    vector /= np.linalg.norm(vector)
    h, _ = native_matrices(couplings, radius, 1)
    thermal = reference_matrix(h, beta)[:, 0]
    thermal /= np.linalg.norm(thermal)
    assert np.linalg.norm(vector-thermal)**2 <= float(bound["thermal_squared_vector_error_upper"])+1e-14


def test_uncertified_thermal_regime_rejected():
    with pytest.raises(ValueError, match="not certified"):
        repeated_transfer_bound([1]*7, 10, 1)


@pytest.mark.parametrize("couplings,radius,parameters", [([1., 1], 1, [1]),
    ([0, 1], 1, [1]), ([1, 1], 0, [1]), ([1, 1], 1, [0.5])])
def test_invalid_input(couplings, radius, parameters):
    with pytest.raises((TypeError, ValueError)):
        WordSampler(couplings, radius, parameters)
