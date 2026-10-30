from fractions import Fraction as F
from itertools import combinations, product
import math
from pathlib import Path
import random
import sys

import numpy as np
import pytest
from scipy.linalg import expm

import sign_sampler as s

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "hdqi-parent-gap-2026-10-23"))
from parent_gap import build_model


@pytest.mark.parametrize("x,parity", ((F(0), 0), (F(1, 100), 0), (F(1, 100), 1),
                                    (F(1, 2), 0), (F(1, 2), 1)))
def test_parity_law_has_rational_mass_and_certified_tail(x, parity):
    eta = F(1, 10**12)
    law = s.parity_law(x, parity, eta)
    assert sum(p for _, p in law.law.probabilities()) == 1
    assert all(k % 2 == parity for k, _ in law.law.probabilities())
    assert law.omitted_weight_bound <= eta
    target = math.cosh(float(x)) if not parity else math.sinh(float(x)) / float(x)
    assert abs(float(law.law.normalizer) - target) <= float(eta) + 1e-15


def test_odd_zero_input_and_invalid_parameters_are_rejected():
    with pytest.raises(ValueError):
        s.parity_law(0, 1, F(1, 100))
    with pytest.raises(ValueError):
        s.Model.create([1], 2, [])
    with pytest.raises(ValueError):
        s.Model.create([1, 1], F(1, 4), [(0, 1), (1, 0)])
    with pytest.raises(ValueError):
        s.budget(s.Model.create([1], 1, []), delta=F(1, 2))


@pytest.mark.parametrize("k", (1, 2, 3, 8))
@pytest.mark.parametrize("mean", (F(-1), F(-1, 3), F(0), F(2, 5), F(1)))
def test_sample_mean_squared_bias_is_exact(k, mean):
    p = (1 + mean) / 2
    expected = sum(F((2*j-k)**2, k*k) * math.comb(k, j) * p**j * (1-p)**(k-j)
                   for j in range(k+1))
    assert expected == mean**2 + (1-mean**2) / k


def test_rejection_law_is_the_claimed_mixture_including_zero_amplitudes():
    q, ratios, k = (F(1, 4), F(1, 2), F(1, 4)), (F(-1), F(1, 3), F(0)), 7
    inverse_c = sum(p*r*r for p, r in zip(q, ratios))
    c = 1 / inverse_c
    mu = [c*p*r*r for p, r in zip(q, ratios)]
    accepted = [p*(r*r+(1-r*r)/k) for p, r in zip(q, ratios)]
    success = sum(accepted)
    alpha = c / (k-1+c)
    assert success == (k-1+c)/(k*c)
    for p, target, output in zip(q, mu, accepted):
        assert output / success == (1-alpha)*target + alpha*p
    assert accepted[-1] > 0 and mu[-1] == 0
    assert sum(abs(a/success-b) for a, b in zip(accepted, mu))/2 <= alpha


def test_unbiased_signed_product_cannot_be_clipped_into_correct_rejection():
    mean = F(0)
    clipped_acceptance = F(1, 2)
    assert clipped_acceptance != mean**2


@pytest.mark.parametrize("edges", ((), ((0, 1),), ((0, 1), (1, 2))))
def test_conditional_words_match_dense_amplitude_ratios(edges):
    model = s.Model.create((1, F(-1, 2), F(3, 4)), F(1, 2), edges)
    dense = build_model(3, edges, [float(j) for j in model.couplings])
    amplitudes = expm(-float(model.beta) * dense.h / 2)[:, 0]
    eta = F(1, 10**8)
    for y in range(8):
        laws = [s.parity_law(x, y >> i & 1, eta).law.probabilities() for i, x in enumerate(model.x)]
        expectation = F(0)
        for entries in product(*laws):
            counts = tuple(k for k, _ in entries)
            probability = math.prod(p for _, p in entries)
            permutations = math.factorial(sum(counts)) // math.prod(math.factorial(k) for k in counts)
            expectation += probability * F(s.exact_sign_sum(model, counts), permutations)
        envelope = math.prod(math.sinh(float(x)) if y >> i & 1 else math.cosh(float(x))
                             for i, x in enumerate(model.x))
        known_sign = (-1)**y.bit_count() * math.prod(-1 if j < 0 else 1
                                                   for i, j in enumerate(model.couplings) if y >> i & 1)
        ratio = amplitudes[y] / (known_sign * envelope)
        assert abs(float(expectation) - ratio) <= 2 * model.m * float(eta) + 1e-12


def test_entire_truncated_sampler_law_against_dense_pilot():
    model = s.Model.create([1, 1], 1, [(0, 1)])
    sampler = s.Sampler(model)
    k = sampler.plan["signs_per_trial"]
    accepted = []
    for y in range(4):
        proposal = math.prod(sampler.proposal[i].probabilities()[y >> i & 1][1] for i in range(2))
        laws = [(sampler.odd[i] if y >> i & 1 else sampler.even[i]).law.probabilities()
                for i in range(2)]
        mean = F(0)
        for entries in product(*laws):
            counts = tuple(count for count, _ in entries)
            probability = math.prod(p for _, p in entries)
            permutations = math.factorial(sum(counts)) // math.prod(math.factorial(c) for c in counts)
            mean += probability * F(s.exact_sign_sum(model, counts), permutations)
        accepted.append(proposal * (mean**2 + (1-mean**2)/k))
    actual = np.array([float(p / sum(accepted)) for p in accepted])
    dense = build_model(2, [(0, 1)])
    amplitudes = expm(-dense.h / 2)[:, 0]
    target = amplitudes**2 / np.dot(amplitudes, amplitudes)
    error = np.sum(np.abs(actual - target)) / 2
    assert error <= float(sampler.plan["ideal_bias_bound"] +
                          4 * sampler.plan["joint_precision_bound"])
    assert target[3] < 1e-30
    assert actual[3] > 0
    proposal_11 = math.prod(law.probabilities()[1][1] for law in sampler.proposal)
    assert accepted[3] == proposal_11 / k


def test_jordan_flow_has_a_real_frustrated_cycle():
    model = s.Model.create([1]*4, F(1, 4), ((0, 1), (0, 2), (0, 3), (1, 2)))
    neighbors = [sum(1 << j for j in range(4) if tuple(sorted((i, j))) in model.edges)
                 for i in range(4)]
    routes = ((2, 3, 0, 1), (1, 3, 0, 2))
    for route in routes:
        occupied = 0
        for i in route:
            assert (occupied & neighbors[i]).bit_count() % 2 == 0
            occupied ^= 1 << i
    left, endpoint = s.word_sign(model, routes[0])
    right, other = s.word_sign(model, routes[1])
    assert endpoint == other == 15
    assert left == -right


def test_budget_accounts_for_bias_rounding_and_failure():
    edges = [(i, (i+1) % 128) for i in range(128)]
    plan = s.budget(s.Model.create([1]*128, F(1, 8), edges), F(1, 8), F(1, 16))
    assert plan["exponent"] == 1
    assert plan["ratio_upper"] == 3
    assert plan["signs_per_trial"] == 97
    assert plan["max_words"] == 1455
    assert plan["ideal_bias_bound"] <= plan["epsilon"]/4
    assert plan["joint_precision_bound"] <= min(plan["epsilon"], plan["delta"])/16
    assert plan["ideal_failure_bound"] + plan["joint_precision_bound"] < plan["delta"]


def test_execution_budget_refuses_large_sign_problem_without_a_sample():
    model = s.Model.create([1]*64, 1, [(i, i+1) for i in range(63)])
    with pytest.raises(s.BudgetExceeded, match="no sample produced"):
        s.Sampler(model, max_word_budget=10)


def test_zero_temperature_parameter_and_zero_couplings_are_exact():
    for model in (s.Model.create([1]*4, 0, []), s.Model.create([0]*4, 1, [])):
        sampler = s.Sampler(model, max_word_budget=0)
        out = sampler.sample(random.Random(2))
        assert out["status"] == "sample" and out["mask"] == 0
        assert out["words"] == 0 and out["exact_point_mass"]


def test_tiny_rational_input_does_not_underflow_or_wait_for_an_odd_event():
    model = s.Model.create([1], F(1, 10**200), [])
    sampler = s.Sampler(model)
    assert sampler.proposal[0].probabilities()[1][1] > 0
    sign, length = sampler.conditional_word(1, random.Random(1))
    assert sign == 1 and length == 1


def test_live_sampler_is_reproducible_and_never_exceeds_its_word_budget():
    model = s.Model.create([1, -1, F(1, 2)], F(1, 2), ((0, 1), (1, 2)))
    sampler = s.Sampler(model)
    left, right = random.Random(24), random.Random(24)
    for _ in range(12):
        a, b = sampler.sample(left), sampler.sample(right)
        assert a == b
        assert a["words"] <= sampler.plan["max_words"]
        assert a["letters"] <= a["words"] * sampler.word_length_cap
        assert a["status"] in ("sample", "failure")


def test_failure_never_fabricates_a_label():
    class RejectingSampler(s.Sampler):
        def conditional_word(self, mask, rng):
            self.counter = getattr(self, "counter", 0) + 1
            return (1 if self.counter % 2 else -1), 0

    class LastInteger:
        def randrange(self, n):
            return n-1

    sampler = RejectingSampler(s.Model.create([1], F(1, 2), []))
    out = sampler.sample(LastInteger())
    assert out["status"] == "failure"
    assert out["mask"] is None
    assert out["words"] == sampler.plan["max_words"]


def test_core_handles_more_bits_than_dense_reference_without_importing_it():
    m = 96
    model = s.Model.create([1]*m, F(1, 16), [(i, i+1) for i in range(m-1)])
    out = s.Sampler(model).sample(random.Random(3))
    assert out["status"] == "sample"
    assert 0 <= out["mask"] < 1 << m
    resources = s.Sampler(model).resource_ledger()
    assert resources["largest_probability_integer_bits"] > 0
    assert out["letters"] <= resources["max_total_letters_per_sample"]


@pytest.mark.parametrize("n", (2, 8, 32, 128))
def test_cluster_bound_extends_beyond_mass_and_beta_degree_regimes(n):
    bounds = s.ratio_bounds(n**8, n**4, n**8, 1, F(1, 16*n**3))
    assert bounds["mass_exponent"] == F(n*n, 512)
    assert bounds["cluster_exponent"] < F(1, 128)
    assert bounds["ratio_upper"] == 3
    if n >= 32:
        assert bounds["ratio_bound_method"] == "cluster"
        assert F(n, 16) > 1


@pytest.mark.parametrize("edges", ((), ((0, 1),), ((0, 1), (1, 2)),
                                   ((0, 1), (0, 2), (1, 2))))
def test_cluster_sign_bound_against_independent_dense_partition(edges):
    model = s.Model.create([1, F(-1, 2), F(3, 4)], F(1, 32), edges)
    matrix = build_model(3, edges, [float(j) for j in model.couplings]).h
    z = np.trace(expm(-float(model.beta)*matrix))/8
    zc = math.prod(math.cosh(float(model.beta*j)) for j in model.couplings)
    log_c = math.log(zc/z)
    plan = s.budget(model)
    assert log_c >= -1e-14
    assert log_c <= float(plan["exponent"]) + 1e-14
    assert plan["cluster_exponent"] is not None


def test_commuting_ratio_is_exact_and_does_not_pay_total_mass():
    plan = s.budget(s.Model.create([1]*1000, 1, []))
    assert plan["mass_exponent"] == 500
    assert plan["exponent"] == 0
    assert plan["ratio_upper"] == 1
    assert plan["ratio_bound_method"] == "commuting_exact"
