"""Exact arithmetic controls for a point-Gaussian quaternion-source proxy.

These are algebraic countercontrols and identities, not a theta evaluator,
finite-source backend, or growing-dimensional convergence experiment. The
irrational fixture is native: O*(1+i), q=2, over the Lipschitz order. Keeping
both coefficient z and physical grid k makes the Gaussian exponent quadratic;
replacing k by rounded real coordinates does not preserve that property.
"""

from itertools import product
from math import isqrt

import sympy as sp


RIGHT_ONE_PLUS_I = sp.Matrix([
    [1, -1, 0, 0],
    [1, 1, 0, 0],
    [0, 0, 1, 1],
    [0, 0, -1, 1],
])
RIGHT_THREE_PLUS_FOUR_I = sp.Matrix([
    [3, -4, 0, 0],
    [4, 3, 0, 0],
    [0, 0, 3, 4],
    [0, 0, -4, 3],
])


def _round_scaled_inverse_sqrt_two(n, bits):
    """Nearest integer to 2**bits*n/sqrt(2), using integer comparisons only."""
    assert n >= 0 and bits >= 1
    square = n * n * 2 ** (2 * bits - 1)
    lower = isqrt(square)
    return lower + int(4 * square > (2 * lower + 1) ** 2)


def _third_differences(values):
    return [
        values[j + 3] - 3 * values[j + 2] + 3 * values[j + 1] - values[j]
        for j in range(len(values) - 3)
    ]


def test_native_irrational_rounding_is_not_linear_or_a_quadratic_pullback():
    assert RIGHT_ONE_PLUS_I.T * RIGHT_ONE_PLUS_I == 2 * sp.eye(4)
    rotation = RIGHT_ONE_PLUS_I / sp.sqrt(2)
    assert rotation.T * rotation == sp.eye(4)
    prime = 2**61 - 1
    assert sp.isprime(prime)

    for bits in (12, 20, 40):
        # On z=(n,0,0,0), both first coordinates equal n/sqrt(2).
        labels = [_round_scaled_inverse_sqrt_two(n, bits) for n in range(8)]
        assert 2 * max(labels) < prime  # No signed-coordinate wrap anywhere.
        assert any(labels[n] != n * labels[1] for n in range(8))
        assert len(set(labels[j + 1] - labels[j] for j in range(7))) > 1
        # A legitimate arithmetic Clifford phase Q(k)=k_0**2 is quadratic
        # in k, but Q(round(M*z/h)) is not quadratic in n, even modulo p.
        differences = _third_differences([label**2 for label in labels])
        assert any(value % prime for value in differences)


def test_exact_rational_grid_is_a_valid_linear_encoding_promise():
    rotation = RIGHT_THREE_PLUS_FOUR_I / 5
    assert rotation.T * rotation == sp.eye(4)
    spacing = sp.Rational(1, 5 * 2**12)
    integer_map = rotation / spacing
    assert all(value.is_Integer for value in integer_map)
    prime = 2**61 - 1
    for entries in product(range(-1, 2), repeat=4):
        coefficients = sp.Matrix(entries)
        labels = integer_map * coefficients
        assert all(abs(value) < prime // 2 for value in labels)
        assert spacing * labels == rotation * coefficients
        residues = [int(value) % prime for value in labels]
        lifted = sp.Matrix([r if r <= prime // 2 else r - prime for r in residues])
        assert lifted == labels
    ray = [int((integer_map * sp.Matrix([n, 0, 0, 0]))[0]) for n in range(8)]
    assert _third_differences([label**2 for label in ray]) == [0] * 5


def test_prime_field_arithmetic_is_not_a_real_embedding():
    # Rational reduction is well-defined here, but its centered lift is not
    # the nearest real grid coordinate at spacing one.
    field_value = 3 * pow(5, -1, 101) % 101
    assert field_value == 41
    assert sp.floor(sp.Rational(3, 5) + sp.Rational(1, 2)) == 1
    assert field_value != 1

    # An algebraic reduction can exist at one prime and fail at another.
    assert {x for x in range(17) if x*x % 17 == 2} == {6, 11}
    assert not any(x*x % 11 == 2 for x in range(11))
    assert sp.floor(sp.sqrt(2) + sp.Rational(1, 2)) == 1
    # A reduced quadratic form is not the positive real norm in the weight.
    assert (5**2 + 1**2) % 13 == 0
    assert 5**2 + 1**2 == 26


def test_prime_padding_requires_coordinate_span_not_maximum_magnitude():
    prime, radius = 101, 60
    assert prime > radius
    assert -radius <= -50 < 51 <= radius
    assert (-50) % prime == 51 % prime

    radius = 50
    labels = tuple(range(-radius, radius + 1))
    assert prime > 2 * radius
    assert len({label % prime for label in labels}) == len(labels)
    assert (40 + 40) % prime == 80
    assert 80 - prime == -21  # Arithmetic on encoded labels may still wrap.

    proxy_radius, source_radius, prime = 2, 6, 11
    assert prime > 2*proxy_radius
    assert (-5) % prime == 6 % prime  # Both labels are in the actual source.
    assert prime <= 2*source_radius
    common_prime = 13
    assert common_prime > 2*max(proxy_radius, source_radius)
    common_support = range(-source_radius, source_radius+1)
    assert len({label % common_prime for label in common_support}) == 13
    # The norm comparison needs the SAME injective map on both states.


def test_basis_rounding_requires_coefficient_range_in_its_error_budget():
    bits = 12
    spacing = sp.Rational(1, 2**bits)
    integer_map = _round_scaled_inverse_sqrt_two(1, bits) * RIGHT_ONE_PLUS_I
    approximate_basis = spacing * integer_map
    true_basis = RIGHT_ONE_PLUS_I / sp.sqrt(2)
    entry_error = sp.sqrt(2) / 2 - approximate_basis[0, 0]
    assert 0 < entry_error < spacing / 2
    coefficients = sp.Matrix([2**20, 0, 0, 0])
    error = (true_basis - approximate_basis) * coefficients
    packet_width = sp.Rational(1, 16)
    assert spacing / packet_width == sp.Rational(1, 256)
    assert error[0] > 64 * packet_width
    # The approximation is linear, but it is not pointwise rounding and
    # cannot be justified solely by the small mesh-to-packet-width ratio.
    assert integer_map[0, 0] * 2**20 != _round_scaled_inverse_sqrt_two(2**20, bits)
    coefficient_l1 = sum(abs(value) for value in coefficients)
    assert sp.simplify(error.dot(error)) <= 4 * (spacing * coefficient_l1 / 2)**2


def test_joint_gaussian_exponent_is_spd_without_rounding_irrational_centers():
    h, s, nu = sp.symbols("h s nu", positive=True)
    z = sp.Matrix(sp.symbols("z0:4", real=True))
    k = sp.Matrix(sp.symbols("k0:4", real=True))
    matrix = RIGHT_ONE_PLUS_I / sp.sqrt(2)
    gram = matrix.T * matrix
    upper = (1/s**2 + 1/(2*nu**2)) * gram
    cross = -h * matrix.T / (2*nu**2)
    lower = h**2 * sp.eye(4) / (2*nu**2)
    joint = upper.row_join(cross).col_join(cross.T.row_join(lower))
    variables = z.col_join(k)
    displacement = h*k - matrix*z
    expected = (z.T * gram * z)[0] / s**2 + displacement.dot(displacement) / (2*nu**2)
    assert sp.expand((variables.T * joint * variables)[0] - expected) == 0
    # Positive lower block and positive Schur complement prove SPD.
    assert sp.simplify(upper - cross * lower.inv() * cross.T) == gram / s**2
    assert joint.det() == h**8 / (16 * nu**8 * s**8)
    phase = k[0]**2 + 3*k[0]*k[2] - k[1]
    assert sp.Poly(expected + sp.I*phase, *z, *k).total_degree() == 2
    auxiliary = sp.Symbol("t", real=True)
    magic_exponent = expected + sp.I * (phase + auxiliary*k[0] + auxiliary**3)
    assert sp.Poly(magic_exponent, *z, *k, auxiliary).total_degree() == 3


def test_sampled_packet_gram_has_a_shifted_theta_not_unit_normalizer():
    u, x, y, nu, h = sp.symbols("u x y nu h", real=True, positive=True)
    original = ((u - x)**2 + (u - y)**2) / (2*nu**2)
    completed = (x - y)**2 / (4*nu**2) + (u - (x+y)/2)**2 / nu**2
    assert sp.expand(original - completed) == 0
    # Poisson: the nonzero reciprocal mode carries the midpoint, so its
    # multiplier cannot be replaced identically by one for every rotation.
    ell = sp.Symbol("ell", integer=True)
    phase = sp.exp(-2*sp.pi*sp.I*ell*((x+y)/2)/h)
    assert sp.simplify(phase.subs({x: 0, y: 0})) == 1
    assert sp.simplify(phase.subs({x: h/2, y: h/2})) == (-1)**ell
    # A finite Gaussian packet gives an exact normalization countercontrol.
    q = sp.Rational(1, 4)
    on_grid_squared_norm = 1 + q**4
    half_grid_squared_norm = 2*q
    assert on_grid_squared_norm != half_grid_squared_norm
    coefficients = (sp.Rational(3, 5), sp.Rational(4, 5))
    norm_squared = coefficients[0]**2 * on_grid_squared_norm + coefficients[1]**2 * half_grid_squared_norm
    assert sum(c*c for c in coefficients) == 1
    assert norm_squared != 1
    # Even one global renormalization changes the coefficient probabilities.
    assert coefficients[0]**2 * on_grid_squared_norm / norm_squared != coefficients[0]**2


def test_small_discarded_probability_does_not_bound_coherent_periodization():
    prime, aliases = 101, 100
    amplitudes = {0: sp.sqrt(99)/10}
    amplitudes.update({1 + j*prime: sp.Rational(1, 100) for j in range(1, aliases+1)})
    assert sum(value**2 for value in amplitudes.values()) == 1
    discarded_mass = sum(value**2 for label, value in amplitudes.items() if label != 0)
    assert discarded_mass == sp.Rational(1, 100)
    periodized = {}
    for label, amplitude in amplitudes.items():
        residue = label % prime
        periodized[residue] = periodized.get(residue, 0) + amplitude
    assert periodized == {0: sp.sqrt(99)/10, 1: 1}
    squared_norm = sum(value**2 for value in periodized.values())
    assert squared_norm == sp.Rational(199, 100)
    # Crop-then-normalize gives |0>. Normalize-after-aliasing has fidelity
    # below one half, despite the original one-percent discarded mass.
    assert periodized[0]**2 / squared_norm == sp.Rational(99, 199) < sp.Rational(1, 2)


def test_hard_window_gaussian_sum_keeps_congruences_but_is_not_complete():
    prime = 11
    q, omega = sp.symbols("q omega")
    coefficients = range(-1, 2)
    grid = tuple(product(range(-2, 3), repeat=2))
    # Rational toy weights make the two finite contractions exactly
    # comparable as polynomials, without floating root-of-unity evaluation.
    def weight(z, k):
        return q ** (z*z + (k[0]-2*z)**2 + (k[1]-3*z)**2)

    def phase(k):
        return (k[0]**2 + 2*k[0]*k[1] + k[1]) % prime

    def supported(k):
        return (2*k[0] + k[1]) % prime == 0

    comb = {k: sum(weight(z, k) for z in coefficients) for k in grid}
    direct = sum(comb[k] * omega**phase(k) for k in grid if supported(k))
    contracted = sum(
        weight(z, k) * omega**phase(k)
        for z, k in product(coefficients, grid) if supported(k)
    )
    assert sp.expand(direct - contracted) == 0
    # Replacing a finite grid by all congruent lifts introduces nonzero
    # Gaussian terms. The chirp is periodic, the amplitude is not.
    z, k, lifted = 0, (0, 0), (prime, 0)
    assert supported(k) and supported(lifted)
    assert phase(k) == phase(lifted)
    assert weight(z, k) != weight(z, lifted)
    assert k in grid and lifted not in grid


def test_magic_shadow_proxy_error_uses_hilbert_schmidt_not_dimension_scaling():
    parameter = sp.Symbol("t", positive=True)
    reference = sp.Matrix([1, 0])
    proxy = sp.Matrix([(1-parameter**2)/(1+parameter**2), 2*parameter/(1+parameter**2)])
    assert sp.simplify(proxy.dot(proxy)) == 1
    difference = reference*reference.T - proxy*proxy.T
    hilbert_schmidt_squared = sp.simplify(sp.trace(difference**2))
    ket_error_squared = sp.simplify((reference-proxy).dot(reference-proxy))
    assert sp.factor(hilbert_schmidt_squared) == 8*parameter**2/(1+parameter**2)**2
    assert ket_error_squared == 4*parameter**2/(1+parameter**2)
    # Conditional on the magic ensemble's 15/2 traceless-observable bound.
    slack = sp.factor(15*ket_error_squared - sp.Rational(15, 2)*hilbert_schmidt_squared)
    assert slack == 60*parameter**4/(1+parameter**2)**2
    assert slack.is_positive
