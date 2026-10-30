"""Exact accounting controls for the bounded-drift entropy argument."""
from fractions import Fraction
from math import ceil, isqrt

import pytest
import sympy as sp


def _ceil_sqrt(value):
    floor = isqrt(value.numerator // value.denominator)
    return floor + int(floor*floor*value.denominator < value.numerator)


def test_integrated_euler_increment_has_no_cross_term_or_gronwall_factor():
    u, h, K, B, L, D, beta = sp.symbols("u h K B L D beta", positive=True)
    # Conditional expectation of the drift/Brownian cross term is zero.
    increment_second_moment = B**2*u**2 + 2*D*u/beta
    bound = beta*L**2*K*sp.integrate(increment_second_moment, (u, 0, h))/4
    assert sp.simplify(bound - (L**2*D*K*h**2/4 + beta*L**2*B**2*K*h**3/12)) == 0


@pytest.mark.parametrize("dimension,drift,lipschitz,beta,time,error", [
    (1, 1, 1, 1, 1, Fraction(1, 10)),
    (100, 1000, 100, 4, 5, Fraction(1, 100)),
    (1000, 1000000, 1000, 10, 20, Fraction(1, 1000)),
    (3, 0, 0, 7, 9, Fraction(1, 3)),
])
def test_integer_step_budget_pays_endpoint_bias(dimension, drift, lipschitz,
                                               beta, time, error):
    A = Fraction(lipschitz**2*dimension*time**2, 4)
    C = Fraction(beta*lipschitz**2*drift**2*time**3, 12)
    steps = max(1, ceil(16*A/error**2), _ceil_sqrt(16*C/error**2))
    kl = A/steps+C/steps**2
    assert kl/2 <= error**2/16
    if lipschitz == 0:
        assert steps == 1 and kl == 0


def test_equal_covariance_gaussian_kl_and_quantization_budget():
    h, beta, displacement = sp.symbols("h beta displacement", positive=True)
    variance = 2*h/beta
    kl = displacement**2/(2*variance)
    assert sp.simplify(kl-beta*displacement**2/(4*h)) == 0
    # Check a concrete rational finite-precision allocation independently
    # of its square root: K * sqrt(beta/(8h)) * a <= error/8.
    K, h, beta, D, L = 100, Fraction(1, 100), 2, 4, 3
    error = Fraction(1, 10)
    eta, zeta = Fraction(1, 10**8), Fraction(1, 10**6)
    mean_bound = (1+h*L)*eta + h*zeta  # sqrt(D)/2 = 1.
    assert K**2*Fraction(beta, 8*h)*mean_bound**2 <= error**2/64
    initial, transition = error/16, error/(16*K)
    assert initial+K*transition+error/8 == error/4


@pytest.mark.parametrize("particles", [2, 3, 5])
def test_pairwise_hessian_graph_identity_is_polynomial(particles):
    # The scalar identity applies coordinatewise to vector-valued particles.
    v = sp.symbols(f"v0:{particles}")
    pair_energy = sum((v[i]-v[j])**2 for i in range(particles)
                      for j in range(i+1, particles))
    assert sp.expand(pair_energy-particles*sum(x*x for x in v)+sum(v)**2) == 0


def test_large_time_or_relative_rare_event_precision_remains_exponential():
    # A polynomial in numerical T or epsilon^-1 is not a polynomial in
    # their binary input lengths, for either the classical or quantum route.
    for n in (8, 16, 32):
        time, error = 2**n, Fraction(1, 2**n)
        assert time**2 == 2**(2*n)
        assert 1/error**2 == 2**(2*n)
        assert time >= 2**(n//2)


def test_reversible_overlap_requires_both_endpoint_directions():
    # An exact two-basin reversible kernel checks normalization, not SDE
    # convergence. Flux c gives transition probabilities c/Z_R and c/Z_P.
    zr, zp, flux = sp.symbols("zr zp flux", positive=True)
    forward, reverse = flux/zr, flux/zp
    overlap = flux/sp.sqrt(zr*zp)
    assert sp.simplify(sp.sqrt(forward*reverse)-overlap) == 0
    assert sp.simplify(sp.sqrt(zp/zr)*overlap-forward) == 0
    assert forward.subs({zr: 1, zp: 100, flux: 1}) == 1
    assert overlap.subs({zr: 1, zp: 100, flux: 1}) == sp.Rational(1, 10)


def test_clipped_product_error_and_square_root_modulus():
    grid = [Fraction(i, 4) for i in range(5)]
    for a in grid:
        for b in grid:
            for x in grid:
                for y in grid:
                    assert abs(a*b-x*y) <= abs(a-x)+abs(b-y)
    # For u>=v>=0, (sqrt(u)-sqrt(v))^2 <= u-v, without
    # a division by v or an assumption that the signal is nonzero.
    v, gap = sp.symbols("v gap", nonnegative=True)
    difference = sp.expand((v+gap-v) - (sp.sqrt(v+gap)-sp.sqrt(v))**2)
    assert sp.simplify(difference-2*sp.sqrt(v)*(sp.sqrt(v+gap)-sp.sqrt(v))) == 0
    assert sp.simplify(difference.subs(v, 0)) == 0


def test_wrapped_quartic_force_is_not_smooth_periodic():
    x = sp.symbols("x")
    derivative = sp.diff(x**4-x**2, x)
    assert derivative.subs(x, 2) == 28
    assert derivative.subs(x, -2) == -28


def test_tiny_time_needs_fine_spacing_but_only_linear_precision_bits():
    # K=beta=D=1, B=L=zeta=0. eta=sqrt(h)*epsilon makes
    # the quantization contribution eta/sqrt(32h) < epsilon/4.
    error = Fraction(1, 16)
    for n in (16, 32, 128):
        h, eta = Fraction(1, 2**n), error/Fraction(2**(n//2))
        assert eta**2/(32*h) <= error**2/16
        assert eta.denominator.bit_length() == n//2+5
