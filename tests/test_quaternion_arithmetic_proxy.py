"""Finite moment controls for arithmetic-shadow proxies, not a decoder.

We enumerate a single prime-qudit Clifford orbit only to check normalizers
and the distinction between pointwise and Born-weighted score error.
Enumeration costs polynomial in p, not log(p), and is NOT a proposed
large-prime implementation. The uniform bound is the cited shadow theorem,
not inferred from these finite controls.
"""

from itertools import product
from fractions import Fraction

import numpy as np
import pytest
import mpmath as mp


def _clifford_orbit(prime, seed):
    phase = np.exp(2j * np.pi * np.arange(prime) / prime)
    inverse_two = pow(2, -1, prime)
    states = []
    symplectic_count = 0
    for a, b, c, d in product(range(prime), repeat=4):
        if (a*d - b*c) % prime != 1:
            continue
        symplectic_count += 1
        matrix = np.zeros((prime, prime), dtype=complex)
        if b:
            factor = inverse_two * pow(b, -1, prime)
            for x, y in product(range(prime), repeat=2):
                exponent = factor * (d*x*x - 2*x*y + a*y*y) % prime
                matrix[x, y] = phase[exponent] / np.sqrt(prime)
        else:
            for y in range(prime):
                matrix[a*y % prime, y] = phase[c*a*y*y*inverse_two % prime]
        assert np.allclose(matrix.conj().T @ matrix, np.eye(prime), atol=1e-13)
        transformed = matrix @ seed
        for shift, frequency in product(range(prime), repeat=2):
            states.append(np.roll(transformed, shift) * phase[
                (frequency * np.arange(prime)) % prime])
    assert symplectic_count == prime * (prime**2 - 1)
    result = np.asarray(states)
    assert result.shape == (prime**3 * (prime**2 - 1), prime)
    return result


@pytest.fixture(scope="module")
def magic_orbit():
    prime = 5
    # The record seed is T^dagger F^dagger |0>; the cubic sign is negative.
    seed = np.exp(-2j * np.pi * np.arange(prime)**3 / prime) / np.sqrt(prime)
    return _clifford_orbit(prime, seed)


def _born_weights(states, input_ket):
    dimension = states.shape[1]
    weights = dimension * abs(states.conj() @ input_ket)**2 / len(states)
    assert abs(weights.sum() - 1) < 1e-12
    return weights


def test_magic_clifford_orbit_is_a_two_design_not_assumed_three_design(magic_orbit):
    states = magic_orbit
    dimension = states.shape[1]
    first = states.T @ states.conj() / len(states)
    assert np.allclose(first, np.eye(dimension) / dimension, atol=1e-13)
    squares = np.einsum("bi,bj->bij", states, states).reshape(len(states), -1)
    second = squares.T @ squares.conj() / len(states)
    swap = np.zeros_like(second)
    for i, j in product(range(dimension), repeat=2):
        swap[i*dimension+j, j*dimension+i] = 1
    expected = (np.eye(dimension**2) + swap) / (dimension * (dimension + 1))
    assert np.allclose(second, expected, atol=1e-13)
    # An exact 3-design would have this sixth moment. The protocol instead
    # supplies a uniform bound on its third moment, not exact Haar equality.
    sixth = np.mean(abs(states[:, 0])**6)
    haar = 6 / (dimension * (dimension + 1) * (dimension + 2))
    assert abs(sixth - haar) > 1e-5


def test_actual_born_weighting_and_centering_are_required(magic_orbit):
    states = magic_orbit
    dimension = states.shape[1]
    ket = np.zeros(dimension, dtype=complex)
    ket[0] = 1
    weights = _born_weights(states, ket)
    scores = (dimension + 1) * abs(states.conj() @ ket)**2 - 1
    assert abs(weights @ scores - 1) < 1e-12
    assert abs(scores.mean() - 1 / dimension) < 1e-12
    assert abs(scores.mean() - weights @ scores) > 0.5
    gamma = 3 + 4 * (dimension - 2) / dimension  # Theorem 4, k=1, p=2 mod 3.
    centered_hs_squared = 1 - 1 / dimension
    centered_scores = scores - 1 / dimension
    assert weights @ centered_scores**2 <= gamma * centered_hs_squared + 1e-12


def test_close_target_proxy_has_dimension_free_ensemble_error_bound(magic_orbit):
    states = magic_orbit
    dimension = states.shape[1]
    target = np.zeros(dimension, dtype=complex)
    target[0] = 1
    proxy = np.zeros(dimension, dtype=complex)
    proxy[:2] = [np.sqrt(0.99), 0.1]
    input_ket = np.arange(1, dimension + 1, dtype=complex)
    input_ket /= np.linalg.norm(input_ket)
    weights = _born_weights(states, input_ket)
    difference = np.outer(target, target.conj()) - np.outer(proxy, proxy.conj())
    assert abs(np.trace(difference)) < 1e-14
    fidelity = abs(np.vdot(target, proxy))**2
    hs_squared = np.linalg.norm(difference)**2
    ket_error_squared = np.linalg.norm(target - proxy)**2
    assert abs(hs_squared - 2 * (1 - fidelity)) < 1e-14
    score_difference = (dimension + 1) * (
        abs(states.conj() @ target)**2 - abs(states.conj() @ proxy)**2)
    second_moment = weights @ score_difference**2
    gamma = 3 + 4 * (dimension - 2) / dimension
    assert second_moment <= gamma * hs_squared + 1e-12
    assert gamma * hs_squared <= 15 * ket_error_squared + 1e-12
    bias = abs(weights @ score_difference)
    exact_bias = abs(np.vdot(input_ket, difference @ input_ket))
    assert abs(bias - exact_bias) < 1e-12
    assert bias <= np.sqrt(1 - fidelity) + 1e-12


def test_single_magic_gate_shadow_constant_keeps_prime_dependence_explicit():
    for prime in (5, 7, 11, 13, 101, 103, 1009):
        gamma = 3 + 4*(prime-2)/prime if prime % 3 != 1 else 15/2
        assert gamma <= 15/2
    # This bounds variance for the stated ensemble, not the number of terms
    # in a record expansion, the cost of scoring, or orientation search.


def test_relative_probability_evaluation_has_bounded_born_score_error(magic_orbit):
    states = magic_orbit
    dimension = states.shape[1]
    target = np.zeros(dimension, dtype=complex)
    target[0] = 1
    source = np.arange(1, dimension+1, dtype=complex)
    source /= np.linalg.norm(source)
    weights = _born_weights(states, source)
    probability = abs(states.conj() @ target)**2
    scores = (dimension+1)*probability-1
    relative_error = 0.03
    # An outcome-dependent error with its sign correlated with the score.
    approximate = probability*(1+relative_error*np.where(scores >= 0, 1, -1))
    error = (dimension+1)*(approximate-probability)
    assert np.all(abs(error) <= relative_error*(scores+1)+1e-13)
    assert abs(weights @ error) <= 2*relative_error+1e-13
    assert weights @ error**2 <= (23/2)*relative_error**2+1e-13
    # At a true cancellation zero, relative accuracy requires an exact zero.
    assert 0*(1+relative_error) == 0


def test_record_adaptive_close_proxies_do_not_inherit_fixed_observable_bound(magic_orbit):
    states = magic_orbit
    dimension = states.shape[1]
    target = np.zeros(dimension, dtype=complex)
    target[0] = 1
    probabilities = abs(states.conj() @ target)**2
    transverse = 0.01
    # For each record separately rotate target toward its phase-aligned
    # perpendicular component. This is NOT one fixed proxy observable.
    proxy_probabilities = (np.sqrt(1-transverse**2)*np.sqrt(probabilities)
                           +transverse*np.sqrt(1-probabilities))**2
    score_errors = (dimension+1)*(proxy_probabilities-probabilities)
    ket_error_squared = 2*(1-np.sqrt(1-transverse**2))
    actual_mse = _born_weights(states, target) @ score_errors**2
    assert 0.0028 < actual_mse < 0.00281
    assert actual_mse > 15*ket_error_squared


def test_left_endpoint_sampling_cannot_reuse_centered_cell_constant():
    # A scalar packet controls the analytic discretization convention, not
    # a native algorithm. Tails beyond |u|=10 are far below working precision.
    with mp.workdps(80):
        h = mp.mpf(1)/8
        packet = lambda x: mp.exp(-mp.pi*x*x/2)

        def integral(left, right):
            scale = mp.sqrt(mp.pi/2)
            return (mp.erf(scale*right)-mp.erf(scale*left))/mp.sqrt(2)

        sample_norm_squared = h*mp.fsum(packet(k*h)**2 for k in range(-80, 81))
        left_cross = mp.fsum(packet(k*h)*integral(k*h, (k+1)*h)
                             for k in range(-80, 81))
        centered_cross = mp.fsum(packet(k*h)*integral((k-mp.mpf('0.5'))*h,
                                  (k+mp.mpf('0.5'))*h) for k in range(-80, 81))
        left_error_squared = sample_norm_squared+1-2*left_cross
        centered_error_squared = sample_norm_squared+1-2*centered_cross
        assert left_error_squared <= mp.pi*h*h/6 + mp.mpf('1e-70')
        assert centered_error_squared <= mp.pi*h*h/24 + mp.mpf('1e-70')
        assert left_error_squared > mp.pi*h*h/24
        assert left_error_squared > mp.mpf('3.9')*centered_error_squared
        # Tensor products use exactly the same cell convention in N=4.
        dimension = 4
        product_error = sample_norm_squared**dimension+1-2*left_cross**dimension
        assert product_error <= mp.pi*dimension**2*h*h/6


def test_localized_weak_cubic_reduces_to_quadratic_moments_with_paid_error():
    # Check the Taylor reduction, NOT an implementation of Hiary's fast
    # quadratic-moment routine. The latter supplies the polylog(W) contract.
    with mp.workdps(90):
        width, bits = 11, 45
        decay = mp.mpf(2) / width**2
        cubic = mp.mpf(1) / (10 * width**3)
        linear, quadratic = mp.mpf(3)/17, mp.mpf(4)/29
        radius = decay*width**2 + 2*mp.pi*abs(cubic)*width**3
        terms = int(mp.ceil(max(2*mp.e*radius,
            radius/mp.log(2) + mp.log(2*width+1, 2) + bits+3)))
        error_cap = (2*width+1) * mp.exp(radius) * mp.power(2, -terms)
        assert error_cap <= mp.power(2, -bits-3)
        direct, approximation = mp.mpc(0), mp.mpc(0)
        for integer in range(-width, width+1):
            z = -decay*integer**2 + 2j*mp.pi*cubic*integer**3
            assert abs(z) <= radius
            chirp = mp.exp(2j*mp.pi*(linear*integer + quadratic*integer**2))
            direct += chirp * mp.exp(z)
            approximation += chirp * mp.fsum(z**j/mp.factorial(j) for j in range(terms))
        assert abs(direct - approximation) <= error_cap + mp.mpf("1e-75")
        # In v=integer/width the coefficient l1 norm is <=exp(radius).
        coefficient_l1_cap = mp.fsum(radius**j/mp.factorial(j) for j in range(terms))
        assert coefficient_l1_cap <= mp.exp(radius)
        moment_error = mp.power(2, -bits-4) / mp.exp(radius)
        assert coefficient_l1_cap*moment_error <= mp.power(2, -bits-4)


def test_large_interval_requires_coefficient_and_parameter_guard_bits():
    width = 2**80
    length = 2*width+1
    second_moment = Fraction((width+1)*(2*width+1), 3*width)
    coefficient_error = Fraction(1, 2**41)
    assert coefficient_error*second_moment > 10**11
    bits = 100
    allowed_coefficient_error = Fraction(1, 2**bits*16*(length+1))
    assert allowed_coefficient_error*second_moment < Fraction(1, 2**(bits+4))
    # Closed-form Dirichlet sum, not exponential enumeration. A parameter
    # error with 200 bits still loses the requested 100-bit sum accuracy.
    with mp.workdps(140):
        alpha = mp.mpf(1)/length
        delta = mp.power(2, -200)
        perturbed_sum = mp.sin(mp.pi*length*(alpha+delta))/mp.sin(mp.pi*(alpha+delta))
        assert abs(perturbed_sum) > mp.power(2, -100)
        parameter_error_bound = length*2*mp.pi*width*delta
        assert abs(perturbed_sum) <= parameter_error_bound
        paid_delta = mp.power(2, -(bits+4*width.bit_length()+10))
        # Conservatively covers simultaneous decay/linear/quadratic/cubic
        # rounding. The number of requested bits is still polynomial.
        paid_bound = length*(width**2+2*mp.pi*(width+width**2+width**3))*paid_delta
        assert paid_bound < mp.power(2, -bits-3)


def test_positive_gaussian_cubic_sum_can_have_exact_cancellation():
    # W=1, lambda=log(2), alpha=-1/5, c=1/5, beta=1/2.
    # At u=-1,0,1 the linear and cubic cancel; endpoint chirps are -1.
    terms = [Fraction(1, 2)*(-1), Fraction(1), Fraction(1, 2)*(-1)]
    assert sum(terms) == 0
    # Additive evaluation therefore cannot imply nonzero relative accuracy.


def test_small_cubic_coefficient_is_not_enough_on_a_full_prime_interval():
    # Even the smallest positive coefficient 1/p has cubic variation ~p^2
    # over a full field. A p^(1/3)-length interval is a different promise.
    for prime in (101, 1009, 10007):
        half_interval = (prime - 1)//2
        full_variation = 2*np.pi*half_interval**3/prime
        localized_width = int(prime**(1/3))
        localized_variation = 2*np.pi*localized_width**3/prime
        assert full_variation > prime**2/2
        assert localized_variation <= 2*np.pi
    # No assertion here that the random-Clifford auxiliary variable is
    # localized, or that the growing-dimensional native amplitude factors.
