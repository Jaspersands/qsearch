from fractions import Fraction as F
from itertools import product
import inspect
import math
import random

import numpy as np
import pytest

from native_sketch import (
    NativeRecord, checked_bank, dot, exact_quarter_turn_probability,
    finite_channel_control, quarter_turn_sketch, resource_ledger,
    root_digits, support_bound, ternary_correlation,
)


def records_for(secret, q, errors=(0,), labels=None):
    """Construct a labeled finite control, not an IID sampler or attack input."""
    labels = product(range(q), repeat=len(secret)) if labels is None else labels
    records = []
    for a in labels:
        for e in errors:
            records.append(NativeRecord(tuple(a), (dot(a, secret)+e) % q, q, str(len(records))))
    return tuple(records)


def evaluate_cyclotomic(coefficients, q):
    return sum(float(c)*np.exp(2j*np.pi*j/(4*q)) for j, c in enumerate(coefficients))


def dense_quarter_probability(records, outcome, repetitions=1):
    q, n = records[0].modulus, len(records[0].label)
    labels = tuple(product(range(q), repeat=n))
    lookup = {a: i for i, a in enumerate(labels)}
    state = np.zeros((q**n, 2), complex)
    state[:, 0] = 1/np.sqrt(q**n)
    for _ in range(repetitions):
        for z in records:
            j = lookup[z.label]
            phase = np.exp(2j*np.pi*z.value/q)
            state[j] = 1j*np.array([[0, phase.conjugate()], [phase, 0]])@state[j]
    amplitude = sum(np.exp(-2j*np.pi*dot(a, outcome)/q)*state[j, 1]
                    for j, a in enumerate(labels))/np.sqrt(q**n)
    return float(abs(amplitude)**2), float(np.linalg.norm(state[:, 1])**2)


@pytest.mark.parametrize("q,r", [(3, 1), (9, 2), (3**17, 17), (3**300, 300)])
def test_native_root_sizes(q, r):
    assert root_digits(q) == r


@pytest.mark.parametrize("q", [True, 0, 1, 2, 6, 12, 3.0])
def test_non_native_roots_rejected(q):
    with pytest.raises(ValueError):
        root_digits(q)


def test_record_scope_and_unique_originals():
    record = NativeRecord([0, 1], 2, 3, "original")
    assert record.label == (0, 1)
    with pytest.raises(ValueError, match="duplicate"):
        checked_bank([record, record])
    with pytest.raises(ValueError, match="shared"):
        checked_bank([record, NativeRecord((0,), 0, 3, "other")])
    with pytest.raises(ValueError):
        NativeRecord((3,), 0, 3, "bad")
    with pytest.raises(ValueError):
        NativeRecord((0,), -1, 3, "bad")
    with pytest.raises(ValueError):
        NativeRecord((0,), 0, 3, "")


@pytest.mark.parametrize("visited", [0, 1, 2, 8, 9])
def test_exact_support_bounds(visited):
    bound = support_bound(3, 2, visited)
    assert bound["herald_probability_upper"] == F(visited, 9)
    assert bound["correct_and_herald_probability_upper"] == F(visited**2, 81)
    assert bound["conditional_fixed_answer_probability_upper"] == F(visited, 9)
    assert not bound["arbitrary_native_algorithms_ruled_out"]


@pytest.mark.parametrize("visited", [-1, 10, True, 1.5])
def test_invalid_support_rejected(visited):
    with pytest.raises(ValueError):
        support_bound(3, 2, visited)


@pytest.mark.parametrize("q,n,v", [(3, 2, 1), (3, 2, 5), (3, 2, 9), (9, 1, 4), (27, 1, 7)])
def test_noiseless_quarter_turn_saturates_bound(q, n, v):
    secret = tuple(range(1, n+1))
    labels = tuple(product(range(q), repeat=n))[:v]
    bank = records_for(secret, q, labels=labels)
    probability = exact_quarter_turn_probability(bank, secret)
    assert probability == (F(v*v, q**(2*n)),)
    dense, herald = dense_quarter_probability(bank, secret)
    assert dense == pytest.approx(float(probability[0]))
    assert herald == pytest.approx(v/q**n)
    assert dense/herald == pytest.approx(v/q**n)


def test_frozen_bank_replay_is_not_new_support():
    bank = records_for((2, 1), 3, labels=[(0, 0), (1, 1)])
    once = quarter_turn_sketch(bank)
    odd = quarter_turn_sketch(bank, 19)
    assert once["state"].keys() == odd["state"].keys()
    assert odd["distinct_originals"] == 2
    assert odd["gate_updates"] == 38
    assert not odd["repetitions_are_fresh_samples"]
    assert exact_quarter_turn_probability(bank, (2, 1), 19) == (F(4, 81),)
    assert exact_quarter_turn_probability(bank, (2, 1), 2) == (F(0),)


@pytest.mark.parametrize("q,n", [(3, 2), (9, 1)])
def test_noisy_exact_evolution_matches_independent_dense_readout(q, n):
    rng = random.Random(124)
    bank = tuple(NativeRecord(tuple(rng.randrange(q) for _ in range(n)), rng.randrange(q), q, str(j))
                 for j in range(13))
    visited = len({z.label for z in bank})
    bounds = support_bound(q, n, visited)
    for outcome in product(range(q), repeat=n):
        polynomial = exact_quarter_turn_probability(bank, outcome, 3)
        exact_numeric = evaluate_cyclotomic(polynomial, q)
        dense, herald = dense_quarter_probability(bank, outcome, 3)
        assert abs(exact_numeric.imag) < 1e-12
        assert exact_numeric.real == pytest.approx(dense, abs=1e-12)
        assert dense <= float(bounds["correct_and_herald_probability_upper"])+1e-12
        assert herald <= float(bounds["herald_probability_upper"])+1e-12
        if herald > 1e-12:
            assert dense/herald <= float(bounds["conditional_fixed_answer_probability_upper"])+1e-12


def test_secret_not_an_attack_or_processor_parameter():
    for function in [quarter_turn_sketch, ternary_correlation]:
        assert "secret" not in inspect.signature(function).parameters


@pytest.mark.parametrize("secret", list(product(range(3), repeat=2)))
def test_classical_same_record_baseline_exact_noise(secret):
    bank = records_for(secret, 3, errors=(0, 0, 0, 0, 1, -1))
    result = ternary_correlation(bank)
    assert result["maximizers"] == (secret,)
    assert result["scores"][secret] == F(1, 2)
    assert set(result["scores"].values()) == {F(0), F(1, 2)}
    assert not result["secret_used_by_attack"]


def test_baseline_keeps_ties_not_false_recovery():
    result = ternary_correlation([NativeRecord((0, 0), 0, 3, "0")])
    assert len(result["maximizers"]) == 9
    assert result["ties_are_not_recovery"]


def test_composite_root_orthogonality_including_nonprimitive_differences():
    q = 9
    for difference in [(1, 0), (3, 0), (0, 6), (3, 6), (8, 8)]:
        mean = sum(np.exp(2j*np.pi*(dot(a, difference) % q)/q)
                   for a in product(range(q), repeat=2))/q**2
        assert abs(mean) < 1e-12


@pytest.mark.parametrize("q,secret,u,harmonic,expected_exponent", [
    (3, (2, 0), 1, 1, 2), (3, (2, 1), 1, 1, None),
    (9, (2, 3), 1, 1, None), (9, (2, 3), 1, 3, 6),
    (9, (2, 0), 2, 1, 4), (9, (2, 6), 2, 1, None),
])
def test_exact_compressed_harmonic_and_composite_root_escape(q, secret, u, harmonic, expected_exponent):
    from sympy import Poly, Symbol, cyclotomic_poly

    x = Symbol("x")
    modulus = Poly(cyclotomic_poly(q, x), x)
    total = Poly(sum(x**((harmonic*dot((u, v), secret)) % q) for v in range(q)), x).rem(modulus)
    expected = Poly(0 if expected_exponent is None else q*x**expected_exponent, x).rem(modulus)
    assert total == expected


def test_arbitrary_noisy_angles_preserve_support_readout_bound():
    rng = random.Random(96)
    q, n = 3, 2
    labels = tuple(product(range(q), repeat=n))
    state = np.zeros((9, 2), complex)
    state[:, 0] = 1/3
    visited = {0, 3, 7}
    for _ in range(80):
        j, b = rng.choice(sorted(visited)), rng.randrange(q)
        theta = rng.uniform(-20, 20)
        phase = np.exp(2j*np.pi*b/q)
        h = np.array([[0, phase.conjugate()], [phase, 0]])
        state[j] = (np.cos(theta)*np.eye(2)+1j*np.sin(theta)*h)@state[j]
    herald = float(np.linalg.norm(state[:, 1])**2)
    assert herald <= len(visited)/9+1e-12
    for outcome in labels:
        amplitude = sum(np.exp(-2j*np.pi*dot(a, outcome)/q)*state[j, 1]
                        for j, a in enumerate(labels))/3
        probability = float(abs(amplitude)**2)
        assert probability <= (len(visited)/9)**2+1e-12
        assert probability/herald <= len(visited)/9+1e-12


def test_resource_bounds_charge_domain_and_queries():
    one = resource_ledger(9, 2, F(1, 2))
    three = resource_ledger(9, 2, F(1, 2), queries=3)
    assert three["fresh_originals_total_sufficient"] >= 9*one["fresh_originals_total_sufficient"]-9
    for result in [one, three]:
        Q = result["queries"]
        M = result["fresh_originals_per_query_sufficient"]
        assert Q*math.pi**2*(81+.25)/(4*.25*M) <= float(result["total_half_diamond_error_budget"])
        assert not result["known_values_available_to_copy_only_receiver"]
        assert not result["accepted_speedup_candidate"]
    required_classical = 32*4*math.log(2*81*2**32)
    assert one["classical_originals_sufficient"] >= required_classical


def test_big_native_parameters_do_not_enumerate_domain():
    n = 32
    result = resource_ledger(3**(2*n), n, F(1))
    assert result["domain_size"] == 3**2048
    assert result["fresh_originals_total_sufficient"] > result["domain_size"]
    assert result["classical_originals_sufficient"] == 32*(1+4096+32)
    assert not result["query_cost_is_polylog_domain"]


@pytest.mark.parametrize("visibility,error", [(0, F(1, 10)), (-1, F(1, 10)), (2, F(1, 10)),
                                                  (.5, F(1, 10)), (True, F(1, 10)), (1, 0), (1, 1)])
def test_invalid_resource_promises_rejected(visibility, error):
    with pytest.raises(ValueError):
        resource_ledger(3, 2, visibility, error=error)


@pytest.mark.parametrize("samples", [3, 12, 48, 192])
def test_actual_mean_channel_and_mixing_bound(samples):
    result = finite_channel_control(3, 1, (2,), {0: F(2, 3), 1: F(1, 6), 2: F(1, 6)}, samples)
    assert result["visibility"] == pytest.approx(.5)
    assert result["mean_hamiltonian_identity_residual"] < 1e-12
    assert result["mean_step_identity_residual"] < 1e-12
    assert result["trace"] == pytest.approx(1, abs=1e-12)
    assert result["minimum_eigenvalue"] > -1e-12
    assert result["trace_distance_to_ideal"] <= result["half_diamond_proved_upper"]+1e-12
    assert result["correct_and_herald_probability"] >= 1-result["half_diamond_proved_upper"]-1e-12
    assert result["channel_vs_mean_unitary_conjugation_gap"] > 1e-6


def test_composite_root_mean_channel():
    result = finite_channel_control(9, 1, (3,), {0: F(1)}, 60)
    assert result["mean_hamiltonian_identity_residual"] < 1e-12
    assert result["trace_distance_to_ideal"] <= result["half_diamond_proved_upper"]+1e-12


def test_control_caps_and_noise_promises():
    with pytest.raises(ValueError, match="capped"):
        finite_channel_control(3, 3, (1, 1, 1), {0: F(1)}, 10)
    with pytest.raises(ValueError, match="normalized"):
        finite_channel_control(3, 1, (1,), {0: F(1, 2)}, 10)
    with pytest.raises(ValueError, match="positive real"):
        finite_channel_control(3, 1, (1,), {1: F(1)}, 10)
    with pytest.raises(ValueError, match="capped"):
        exact_quarter_turn_probability(records_for((1,), 243, labels=[(0,)]), (1,))
    with pytest.raises(ValueError, match="scope"):
        ternary_correlation(records_for((1,), 9))
