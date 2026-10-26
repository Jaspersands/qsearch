import cmath
from fractions import Fraction as Q
from itertools import product
import json
import math

import numpy as np
import pytest

from theorems import integer_character_interpolation as integer
from theorems import integer_character_resonance as resonance


def small_problem():
    primes = (2, 5, 7)
    exponent = 7
    return resonance.ResonanceProblem(
        primes, tuple(integer.lifted_log(p, exponent)[0] for p in primes),
        exponent, 1)


def source_distribution(primes, exponent, centers=None):
    """Independent explicit small Fourier control, never a search benchmark."""
    modulus, order = 3**exponent, 2*3**(exponent-1)
    logs = {pow(2, a, modulus): a for a in range(order)}
    labels = [logs[p % modulus] for p in primes]
    centers = centers or [0]*len(primes)
    state = np.zeros(order, dtype=np.complex128)
    words = [y for y in product((-1, 0, 1), repeat=len(primes))
             if y.count(1) <= 1 and y.count(-1) <= 1]
    amplitudes = {}
    for y in words:
        active = sum(v != 0 for v in y)
        mass = .025**active*.95**(len(primes)-active)
        amplitudes[y] = math.sqrt(mass)
        phase = cmath.exp(2j*math.pi*sum(c*v for c, v in zip(centers, y))/order)
        state[sum(a*v for a, v in zip(labels, y)) % order] += math.sqrt(mass)*phase
    state /= np.linalg.norm(state)
    probabilities = np.abs(np.fft.fft(state))**2/order
    mass = sum(a*a for a in amplitudes.values())
    overlap = 0.0
    for y, amplitude in amplitudes.items():
        neighbor = (y[0]+1, *y[1:])
        overlap += amplitude*amplitudes.get(neighbor, 0)/mass
    return labels, probabilities, overlap


@pytest.mark.parametrize("exponent", [2, 3, 4])
def test_primitivity_matches_failure_to_descend_to_smaller_modulus(exponent):
    modulus, order = 3**exponent, 2*3**(exponent-1)
    logs = {pow(2, a, modulus): a for a in range(order)}
    for x in range(order):
        fibers = {}
        descends = True
        for u, a in logs.items():
            phase = a*x % order
            key = u % (modulus//3)
            if key in fibers and fibers[key] != phase:
                descends = False
            fibers[key] = phase
        assert (not descends) == (x % 3 != 0)


@pytest.mark.parametrize("centers", [None, [11, 19, 37]])
def test_guarded_primitive_projection_preserves_each_cosine_moment(centers):
    problem = small_problem()
    labels, probabilities, overlap = source_distribution(problem.primes, 7, centers)
    centers = centers or [0]*3
    x = np.arange(problem.order)
    assert sum(probabilities) == pytest.approx(1, abs=1e-14)
    for residue in range(3):
        mask = x % 3 == residue
        assert probabilities[mask].sum() == pytest.approx(1/3, abs=1e-14)
        for a, c in zip(labels, centers):
            score = np.cos(2*np.pi*((x*a-c) % problem.order)/problem.order)
            assert (probabilities[mask]*score[mask]).sum() == pytest.approx(overlap/3, abs=1e-14)
    predicted = integer.source_mean(3, 1, Q(1, 20))
    assert float(Q(predicted["mean_cosine_lower"])) == pytest.approx(overlap, abs=1e-14)


def test_unlicensed_projection_can_change_the_mean():
    labels, probabilities, _ = source_distribution((2, 5, 7), 3)
    x = np.arange(len(probabilities))
    mask = x % 3 != 0
    score = np.cos(2*np.pi*((x*labels[0]) % len(x))/len(x))
    unconditional = (probabilities*score).sum()
    conditional = (probabilities[mask]*score[mask]).sum()/probabilities[mask].sum()
    assert abs(unconditional-conditional) > 1e-3


def test_original_guard_alone_does_not_license_primitive_projection():
    integer.height_license((2, 5, 7), 1, 6)
    with pytest.raises(ValueError, match="smaller-modulus"):
        resonance.primitive_license((2, 5, 7), 1, 6)


def test_principal_character_is_rejected_despite_perfect_score():
    row = small_problem().evaluate(0)
    assert Q(row["score_lower"]) <= 1 <= Q(row["score_upper"])
    assert not row["primitive"]
    assert not row["accepted"]


def test_interval_score_and_euler_product_match_independent_complex_evaluation():
    problem = small_problem()
    for x in [1, 2, 3, 18, 93, problem.order-1]:
        row = problem.evaluate(x)
        characters = [cmath.exp(2j*math.pi*(a*x % problem.order)/problem.order)
                      for a in problem.labels]
        weighted = sum(z.real/p for z, p in zip(characters, problem.primes))
        weight = sum(1/p for p in problem.primes)
        product_log = sum(-math.log(abs(1-z/p))
                          for z, p in zip(characters, problem.primes))
        assert float(Q(row["score_lower"])) == pytest.approx(weighted/weight, abs=1e-13)
        assert float(Q(row["log_truncated_euler_modulus_lower"])) == pytest.approx(product_log, abs=1e-13)
        assert Q(row["log_truncated_euler_modulus_lower"]) >= Q(row["weighted_sum_upper"])-1
        assert Q(row["score_upper"])-Q(row["score_lower"]) < Q(1, 10**20)
        assert row["accepted"] == (x % 3 != 0 and Q(row["score_lower"]) >= Q(1, 4))
        assert not row["full_L_value_computed"]


@pytest.mark.parametrize("assignment", [-1, True, 1.0, 1458])
def test_noncanonical_or_lossy_character_rejected(assignment):
    with pytest.raises(ValueError):
        small_problem().evaluate(assignment)


def test_public_labels_and_complete_prime_prefix_are_checked():
    problem = small_problem()
    with pytest.raises(ValueError, match="public logarithm"):
        resonance.ResonanceProblem(problem.primes, (0, *problem.labels[1:]), 7, 1)
    with pytest.raises(ValueError, match="complete prime prefix"):
        resonance.ResonanceProblem((2, 7), (problem.labels[0], problem.labels[2]), 7, 1)
    with pytest.raises(ValueError, match="immutable"):
        resonance.ResonanceProblem(list(problem.primes), problem.labels, 7, 1)


def test_joint_error_budget_subtracts_tv_before_conditioning():
    cert = resonance.primitive_success_budget()
    robust, mu = Q(cert["robust_threshold"]), Q(cert["normalized_weighted_mean_lower"])
    joint = Q(2, 3)*(mu-robust)/(1-robust)-Q(1, 10000)
    assert Q(cert["primitive_and_accepted_given_herald_lower"]) == joint
    assert joint/8 > Q(1, 256)
    assert cert["minimum_length"] == 20000
    assert Q(cert["accepted_per_charged_trial_lower"])*cert["trials_per_failure_bit"] == 1


@pytest.mark.parametrize("bound", [2, 7, 8167, 10**100])
def test_analytic_bridge_is_near_one_not_at_one(bound):
    cert = resonance.analytic_bridge(bound)
    assert Q(cert["sigma"]) == 1+Q(1, bound.bit_length())
    assert not cert["at_s_equal_one_claimed"]
    assert not cert["critical_strip_claimed"]
    assert not cert["full_L_value_computed"]
    assert Q(cert["higher_prime_powers_upper"]) == 1
    assert cert["log_abs_L_lower_formula"] == "log(log(B+1))/4 - 43"


def test_control_sampling_preserves_primitivity_and_is_reproducible():
    problem = small_problem()
    a = resonance.classical_control(problem, trials=12, seed=108)
    assert a == resonance.classical_control(problem, trials=12, seed=108)
    assert all(row["primitive"] for row in a["records"])
    assert a["accepted_count"] == sum(row["accepted"] for row in a["records"])
    assert Q(a["best"]["score_lower"]) == max(Q(row["score_lower"]) for row in a["records"])


def test_live_report_replays_with_no_advantage_or_quantum_execution_claim():
    saved = json.loads(resonance.REPORT.read_text())
    assert saved == resonance.report()
    assert saved["classical_control"]["trials"] == 32
    assert saved["classical_control"]["seed"] == 2026102027
    assert [i for i, row in enumerate(saved["classical_control"]["records"])
            if row["accepted"]] == [2, 24]
    assert not saved["quantum_optimizer_executed"]
    assert not saved["kernel_checked_proof"]
    assert not saved["novelty_established"]
    assert not saved["classical_hardness_or_speedup_proved"]
    assert not saved["analytic_bridge"]["implies_abs_L_above_one"]
