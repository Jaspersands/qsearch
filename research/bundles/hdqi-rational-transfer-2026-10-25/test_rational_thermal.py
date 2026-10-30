from fractions import Fraction as Q
from pathlib import Path
import sys

import mpmath as mp
import numpy as np
import pytest

from rational_thermal import (block_moments, construct, evaluate,
                              ceil_log2, integer_transfer_polynomial, native_certificate,
                              pi_squared_quarter, power_sums, root_rounding_plan)


def high(value):
    return mp.mpf(value.numerator)/value.denominator


@pytest.mark.parametrize("stop", [0, 1, 2, 17, 91])
def test_power_sums_against_enumeration(stop):
    assert power_sums(stop, 12) == [sum(n**k for n in range(stop)) for k in range(13)]


def test_huge_power_sum_without_enumeration():
    n = 10**100
    sums = power_sums(n, 3)
    assert sums == [n, n*(n-1)//2, n*(n-1)*(2*n-1)//6, (n*(n-1)//2)**2]


@pytest.mark.parametrize("low,high", [(0, 0), (1, 2), (3, 6), (7, 14)])
def test_block_moments_exact(low, high):
    center, moments = block_moments(low, high, 10)
    assert moments == [sum(((2*n+1)**2-center)**k for n in range(low, high+1)) for k in range(10)]


@pytest.mark.parametrize("tolerance", [Q(1, 100), Q(1, 10**8), Q(1, 10**20)])
def test_rational_pi_enclosure(tolerance):
    certificate = pi_squared_quarter(tolerance)
    with mp.workdps(100):
        assert high(certificate["lo"]) < mp.pi**2/4 < high(certificate["hi"])
    assert certificate["relative_error_upper"] <= tolerance


@pytest.mark.parametrize("maximum,error", [(Q(1, 10), Q(1, 20)), (1, Q(1, 100)),
    (10, Q(1, 1000)), (100, Q(1, 100))])
def test_uniform_budget_and_high_precision_grid(maximum, error):
    certificate = construct(maximum, error)
    assert certificate["uniform_error_upper"] <= error
    assert evaluate(certificate, 0) == 0
    with mp.workdps(80):
        for i in range(11):
            x = Q(maximum)*i/10
            actual = evaluate(certificate, x)
            assert evaluate(certificate, -x) == -actual
            assert abs(high(actual)-mp.tanh(high(x))) <= high(certificate["uniform_error_upper"])
    assert all(block["center"] > 0 for block in certificate["blocks"])


def test_representation_does_not_enumerate_effective_poles():
    certificate = construct(10**12, Q(1, 1000))
    assert certificate["effective_pole_count"] > 10**15
    assert certificate["groups"] < 60
    assert len(certificate["blocks"]) == certificate["groups"]
    assert certificate["transfer_degree_upper"] == 2*certificate["groups"]*certificate["order"]


def test_native_state_error_and_unimplemented_boundary():
    certificate = native_certificate([1]*64, 7, 1, Q(1, 100))
    assert certificate["thermal_squared_state_error_upper"] <= Q(1, 100)**2/16
    assert not certificate["complex_factor_sampler_implemented"]
    assert not certificate["quantum_advantage_claim"]


def test_outside_interval_rejected():
    with pytest.raises(ValueError, match="outside"):
        evaluate(construct(1, Q(1, 10)), 2)


def test_expanded_transfer_polynomial_exactly_encodes_rational_angles():
    certificate = construct(1, Q(1, 4))
    coefficients = integer_transfer_polynomial(certificate)

    def polynomial(x):
        return sum((a*x**k for k, a in enumerate(coefficients)), Q(0))

    for x in (Q(0), Q(1, 4), Q(1), Q(2)):
        plus, minus = polynomial(x), polynomial(-x)
        assert plus+minus >= 2*coefficients[0]
        assert (minus-plus)/(minus+plus) == evaluate(certificate, x/2)


def test_root_rounding_plan_does_not_claim_a_compiler():
    native = native_certificate([1]*3, 1, Q(1, 10), Q(1, 4))
    coefficients = integer_transfer_polynomial(native["approximation"], native["beta"])
    plan = root_rounding_plan(native)
    factors = len(coefficients)-1
    budget = Q(8*factors*3, 1)/native["target_error"]*(plan["root_modulus_upper"]+2)**(3*factors)
    assert Q(2)**plan["root_disk_radius_target_bits"] >= budget
    assert not plan["root_disks_produced"]
    assert not plan["complex_sampler_executed"]


def test_changed_approximation_cannot_receive_a_normalization_claim():
    native = native_certificate([1]*3, 1, Q(1, 10), Q(1, 4))
    native["approximation"]["blocks"][0]["center"] = Q(-1)
    with pytest.raises(ValueError, match="does not reproduce"):
        root_rounding_plan(native)


def test_zero_constant_tolerance_rejected():
    with pytest.raises(ValueError, match="tolerance"):
        pi_squared_quarter(0)


@pytest.mark.parametrize("couplings,radius", [([1]*5, 2), ([1, -1, Q(1, 2), 1, -1], 2)])
def test_rational_angles_on_full_native_state(couplings, radius):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent/"hdqi-hidden-mode-access-2026-10-25"))
    from controls import dense_modes, reference_matrix

    native = native_certificate(couplings, radius, 1, Q(1, 100))
    h, _, modes, spectrum = dense_modes(couplings, radius, radius+1)
    state = np.eye(len(h), dtype=complex)[:, 0]
    for row, (_, _, c, d) in zip(spectrum["modes"], modes):
        angle = evaluate(native["approximation"], row["energy"].midpoint/2)
        state = state-float(angle)*(-1j*c @ d @ state)
    state /= np.linalg.norm(state)
    target = reference_matrix(h, 1)[:, 0]
    target /= np.linalg.norm(target)
    assert np.linalg.norm(state-target)**2 <= float(native["thermal_squared_state_error_upper"])+1e-12


@pytest.mark.parametrize("value", [Q(1, 8), Q(1, 7), 1, 2, 3, Q(9, 2), 10**50])
def test_ceil_log_exact(value):
    exponent = ceil_log2(value)
    assert Q(2)**(exponent-1) < value <= Q(2)**exponent


@pytest.mark.parametrize("maximum,error", [(0, Q(1, 10)), (1, 0), (1, 1), (1., Q(1, 10))])
def test_invalid_budget(maximum, error):
    with pytest.raises((TypeError, ValueError)):
        construct(maximum, error)
