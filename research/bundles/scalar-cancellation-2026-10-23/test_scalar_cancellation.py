from fractions import Fraction
from itertools import product
import random

import pytest

from scalar_cancellation import (
    ScalarBackend, SmoothPowerRoots, TrialBudgetExceeded, prime_factors,
    scalar_call_cap, verify_scalar,
)
from composer_bridge import composer, solve_matrix


LARGE_PRIME = 170141183460469231731687303715884465961


class ConstantRandom:
    def __init__(self, value):
        self.value = value

    def randrange(self, start, stop):
        return self.value


@pytest.mark.parametrize("prime", [3, 5, 7, 13, 17, 19, 31, 41, 97, 109, 211, 257])
def test_all_small_field_roots_against_exhaustive_power_images(prime):
    for degree in range(1, min(12, prime-1)+1):
        if (prime-1) % degree:
            continue
        engine = SmoothPowerRoots(prime, degree, rng=random.Random(419))
        powers = {pow(x, degree, prime) for x in range(prime)}
        for value in range(prime):
            result = engine.root(value)
            assert (result is not None) == (value in powers)
            if result is not None:
                assert pow(result, degree, prime) == value


@pytest.mark.parametrize("degree", range(2, 13))
def test_128_bit_roots_without_general_factorization_or_field_enumeration(degree):
    rng = random.Random(887+degree)
    engine = SmoothPowerRoots(LARGE_PRIME, degree, rng=rng)
    for _ in range(10):
        x = rng.randrange(1, LARGE_PRIME)
        value = pow(x, degree, LARGE_PRIME)
        assert pow(engine.root(value), degree, LARGE_PRIME) == value
    assert engine.stats.small_field_elements == 0
    assert engine.stats.pohlig_hellman_digits > 0
    assert engine.smooth*engine.rough == LARGE_PRIME-1


def test_smooth_part_digit_lengths_not_just_first_residue_class():
    prime = 2013265921  # 15 * 2^27 + 1; long 2-primary digit chain.
    engine = SmoothPowerRoots(prime, 12, rng=random.Random(2))
    x = 1234567
    assert pow(engine.root(pow(x, 12, prime)), 12, prime) == pow(x, 12, prime)
    assert engine.stats.pohlig_hellman_digits >= 28


@pytest.mark.parametrize("prime,degree", [(5, 2), (7, 3)])
def test_all_scalar_coefficients_in_small_controls(prime, degree):
    backend = ScalarBackend(prime, degree, max_scalar_calls=prime**(degree+1))
    for coefficients in product(range(prime), repeat=degree+1):
        weights = backend(coefficients, degree, prime)
        verify_scalar(prime, degree, coefficients, weights)
    assert backend.stats.small_field_elements == prime
    assert backend.stats.generator_draws == 0
    assert backend.abort_bound == 0


@pytest.mark.parametrize("prime,degree", [(13, 4), (17, 8), (31, 5), (97, 6), (109, 9)])
def test_nonbijective_higher_degree_small_field_solver(prime, degree):
    rng = random.Random(182)
    backend = ScalarBackend(prime, degree, max_scalar_calls=40)
    for _ in range(40):
        coefficients = tuple(rng.randrange(1, prime) for _ in range(degree+1))
        result = backend(coefficients, degree, prime)
        verify_scalar(prime, degree, coefficients, result)
    assert backend.stats.small_field_solves == 40
    assert backend.stats.small_field_elements == prime
    assert backend.stats.curve_trials == 0


@pytest.mark.parametrize("degree", [2, 3, 4, 5, 6, 8, 9, 10, 11, 12])
def test_large_prime_scalar_equations_and_capped_failure_bound(degree):
    rng = random.Random(171+degree)
    backend = ScalarBackend(LARGE_PRIME, degree, max_scalar_calls=20, rng=rng)
    for _ in range(20):
        coefficients = tuple(rng.randrange(1, LARGE_PRIME) for _ in range(degree+1))
        result = backend(coefficients, degree, LARGE_PRIME)
        verify_scalar(LARGE_PRIME, degree, coefficients, result)
        assert result[2] == 1  # Nontriviality does not depend on a random hit.
    assert backend.stats.small_field_elements == 0
    assert backend.stats.large_field_solves == 20
    assert backend.stats.curve_trials <= 20*backend.curve_cap
    assert 21*Fraction(1, 2**backend.bits) <= backend.abort_bound
    assert backend.roots.abort_bound <= Fraction(1, 2**backend.bits)
    assert Fraction(2*degree-1, 2*degree)**backend.curve_cap <= Fraction(1, 2**backend.bits)


@pytest.mark.parametrize("prime,degree,rank", [
    (5, 2, 3), (13, 4, 3), (17, 8, 2), (13, 9, 2),
    (LARGE_PRIME, 4, 3), (LARGE_PRIME, 6, 3), (LARGE_PRIME, 11, 2),
    (2**127-1, 4, 3), (LARGE_PRIME, 1, 3),
])
def test_existing_rank_composer_with_new_backend(prime, degree, rank):
    from math import gcd
    g = gcd(degree, prime-1)
    count = composer.bank_arity(g, rank)
    rng = random.Random(456)
    matrix = [[rng.randrange(prime) for _ in range(count)] for _ in range(rank)]
    witness, report = solve_matrix(matrix, prime, degree, rank, rng=rng)
    assert composer.valid_witness(matrix, witness.weights, prime, degree)
    assert report["scalar_call_count_matches_composer"]
    assert report["original_matrix_moment_verified"]
    assert report["acquired_columns"] == count
    assert not report["quantum_receiver_executed"]
    assert not report["speedup_claim_allowed"]
    assert witness.scalar_calls == scalar_call_cap(g, witness.observed_rank)


def test_unused_bank_and_redundant_rows_remain_paid():
    p, degree, cap = LARGE_PRIME, 4, 3
    width = composer.bank_arity(degree, cap)
    row = [(i+1) % p for i in range(width)]
    matrix = [row, [2*x % p for x in row], [0]*width]
    witness, report = solve_matrix(matrix, p, degree, cap, rng=random.Random(2))
    assert witness.observed_rank == 1
    assert witness.acquired_columns == 125
    assert witness.used_prefix_columns == 5
    assert not any(witness.weights[5:])
    assert report["counters"]["scalar_calls"] == 1


def test_zero_rank_does_not_call_backend_but_does_pay_cap():
    witness, report = solve_matrix([[0]*25], LARGE_PRIME, 4, 2)
    assert witness.weights == (1,)+(0,)*24
    assert report["counters"]["scalar_calls"] == 0
    assert report["acquired_columns"] == 25


def test_bad_rank_promise_and_missing_bank_are_not_repaired():
    with pytest.raises(ValueError, match="rank exceeds"):
        solve_matrix([[1, 0, 1], [0, 1, 1]], 5, 2, 1)
    with pytest.raises(ValueError, match="full preallocated"):
        solve_matrix([[1, 2, 3]], 5, 2, 2)
    with pytest.raises(ValueError, match="degree < prime"):
        solve_matrix([[1]*16], 7, 9, 2)


def test_generator_sampler_aborts_instead_of_scanning_field():
    with pytest.raises(TrialBudgetExceeded, match="generator cap"):
        SmoothPowerRoots(LARGE_PRIME, 4, rng=ConstantRandom(1), attempt_cap=4)


def test_curve_clock_aborts_without_returning_a_false_witness():
    backend = ScalarBackend(1009, 2, security_bits=1, rng=random.Random(3))
    backend.roots = SmoothPowerRoots(1009, 2, rng=random.Random(5), counters=backend.stats)
    nonresidue = next(a for a in range(2, 1009) if pow(a, 504, 1009) != 1)
    backend.rng = ConstantRandom(0)
    with pytest.raises(TrialBudgetExceeded, match="curve trial cap"):
        backend((1, 1, -nonresidue % 1009), 2, 1009)
    assert backend.stats.curve_trials == backend.curve_cap
    with pytest.raises(TrialBudgetExceeded, match="already aborted"):
        backend((0, 1, 1), 2, 1009)


def test_call_cap_and_invalid_rng_are_not_silent():
    backend = ScalarBackend(5, 2)
    backend((1, 2, 3), 2, 5)
    with pytest.raises(TrialBudgetExceeded, match="call budget"):
        backend((0, 0, 0), 2, 5)
    with pytest.raises(ValueError, match="random source"):
        SmoothPowerRoots(1009, 2, rng=ConstantRandom(1009))


def test_field_scan_guard_and_zero_witness_falsifier():
    backend = ScalarBackend(LARGE_PRIME, 4)
    with pytest.raises(ValueError, match="enumeration forbidden"):
        backend._small_field((1, 1, 1, 1, 1))
    with pytest.raises(ArithmeticError, match="nonzero"):
        verify_scalar(13, 4, (1, 2, 3, 4, 5), (0, 0, 0, 0, 0))


def test_even_power_sign_shortcut_is_not_assumed():
    # In F5 every nonzero fourth power is 1: all five inputs are necessary.
    backend = ScalarBackend(5, 4)
    weights = backend((1, 1, 1, 1, 1), 4, 5)
    assert all(weights)
    assert all(pow(x, 4, 5) == 1 for x in weights)
    assert all(pow(x, 4, 5) != 4 for x in range(5))


def test_corrupt_root_cannot_escape_the_final_scalar_check(monkeypatch):
    backend = ScalarBackend(1009, 2, rng=random.Random(12))
    backend.roots = SmoothPowerRoots(1009, 2, rng=random.Random(7))
    monkeypatch.setattr(backend.roots, "root", lambda value: 0)
    backend.rng = ConstantRandom(0)
    with pytest.raises(ArithmeticError, match="moment did not vanish"):
        backend((1, 1, 1), 2, 1009)


@pytest.mark.parametrize("prime,degree", [(15, 2), (2, 1), (13, 5), (True, 2), (13, 0)])
def test_malformed_fields_and_degrees_rejected(prime, degree):
    with pytest.raises(ValueError):
        ScalarBackend(prime, degree)


def test_linear_and_zero_coefficient_branches():
    backend = ScalarBackend(LARGE_PRIME, 1, max_scalar_calls=2)
    verify_scalar(LARGE_PRIME, 1, (3, 8), backend((3, 8), 1, LARGE_PRIME))
    assert backend((5, 0), 1, LARGE_PRIME) == (0, 1)
    assert backend.stats.generator_draws == 0
    assert prime_factors(2**4*3**2*11) == (2, 3, 11)
