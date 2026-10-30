"""Bounded controls for Gaussian/straddle signatures of a quaternion orbit.

Use Hamilton's Lipschitz order O=Z[1,i,j,k], column lattice bases, and RIGHT
multiplication by g=(3+4i)/5. These fixtures do not prove the parent's broad
Gaussian signature theorem or implement a receiver, oracle search, HSP
algorithm, or quantum backend. No growing-dimensional state is allocated.

The Gaussian amplitude is exp(-pi*||x||^2/(2*s^2)); its squared mass has
exponent -pi*||x||^2/s^2. Here s=s_test=s_parent/sqrt(2), matching the
parent's amplitude exp(-pi*||x||^2/s_parent^2). A one-dimensional EHKS
straddle has amplitudes cos(pi*t/2), sin(pi*t/2) at the two neighboring
grid sites, hence probabilities cos^2(pi*t/2), sin^2(pi*t/2). Grid spacing
1/10 with offset 1/20 gives disjoint supports on (1/5)Z. Only planar sparse
states and scalar theta sums are used for numerical calibration. Tail
bounds are explicit analytic bounds evaluated with mpmath, not certified
interval arithmetic or evidence for a general convergence theorem.
"""

from fractions import Fraction
from functools import lru_cache
from itertools import product
from math import isqrt

import mpmath as mp
import sympy as sp


ONE, I, J, K = BASIS = tuple(
    tuple(int(row == column) for row in range(4)) for column in range(4)
)
G = (Fraction(3, 5), Fraction(4, 5), 0, 0)
FINE_STEP = Fraction(1, 10)
FINE_OFFSET = Fraction(1, 20)


def _mul(x, y):
    a, b, c, d = x
    e, f, h, l = y
    return (
        a * e - b * f - c * h - d * l,
        a * f + b * e + c * l - d * h,
        a * h - b * l + c * e + d * f,
        a * l + b * h - c * f + d * e,
    )


def _norm(x):
    return sum(value * value for value in x)


def _conjugate(x):
    return (x[0],) + tuple(-value for value in x[1:])


def _inverse(x):
    return tuple(Fraction(value) / _norm(x) for value in _conjugate(x))


def _right_matrix(x):
    return sp.Matrix.hstack(*(sp.Matrix(_mul(e, x)) for e in BASIS))


def _integral(values):
    return all(sp.sympify(value).is_Integer is True for value in values)


@lru_cache(maxsize=32)
def _ehks_weights(t):
    angle = sp.pi * sp.Rational(t) / 2
    return sp.simplify(sp.cos(angle) ** 2), sp.simplify(sp.sin(angle) ** 2)


def _straddle_probabilities(x, step=FINE_STEP, offset=FINE_OFFSET):
    coordinate = (Fraction(x) - offset) / step
    lower = coordinate.numerator // coordinate.denominator
    t = coordinate - lower
    left, right = _ehks_weights(t)
    return {site: p for site, p in ((lower, left), (lower + 1, right)) if p != 0}


def _mp_real(x):
    x = sp.sympify(x)
    if x.is_Rational:
        return mp.mpf(int(x.p)) / int(x.q)
    return mp.mpf(str(x.evalf(mp.mp.dps + 10)))


def _planar_state(rotation, width, radius):
    """Same physical disk cutoff before/after an exact planar isometry."""
    physical, encoded = {}, {}
    for a, b in product(range(-radius, radius + 1), repeat=2):
        squared_norm = a * a + b * b
        if squared_norm > radius * radius:
            continue
        point = tuple(Fraction(x) for x in rotation * sp.Matrix([a, b]))
        assert _norm(point) == squared_norm
        amplitude = mp.exp(-mp.pi * squared_norm / (2 * width * width))
        physical[point] = amplitude
        first, second = (_straddle_probabilities(x) for x in point)
        for (u, p), (v, q) in product(first.items(), second.items()):
            site = (u, v)
            encoded[site] = encoded.get(site, mp.mpf(0)) + amplitude * mp.sqrt(
                _mp_real(p * q)
            )
    mass = mp.fsum(amplitude**2 for amplitude in physical.values())
    return physical, encoded, mass


def _theta_with_tail(width, cutoff, scale=1):
    """T <= 2*integral_N^infty exp(-scale*pi*x^2/s^2) dx
    <= s^2/(scale*pi*N)*exp(-scale*pi*N^2/s^2), for N>0.
    """
    assert cutoff > 0 and width > 0 and scale > 0
    coefficient = scale * mp.pi / (width * width)
    partial = mp.fsum(mp.exp(-coefficient * n * n) for n in range(-cutoff, cutoff + 1))
    tail = mp.exp(-coefficient * cutoff * cutoff) / (coefficient * cutoff)
    return partial, tail


def _overlap_bounds(width, cutoff):
    # The intersection has Gram matrix 5*I_4, so its mass is theta_5^4.
    denominator, denominator_tail = _theta_with_tail(width, cutoff)
    numerator, numerator_tail = _theta_with_tail(width, cutoff, scale=5)
    lower = (numerator / (denominator + denominator_tail)) ** 4
    upper = ((numerator + numerator_tail) / denominator) ** 4
    # Numerical roundoff allowance is separate from the analytic tails.
    roundoff = mp.mpf("1e-50")
    return lower - roundoff, upper + roundoff


def test_exact_right_rotation_match_and_denominator_container():
    rotation = _right_matrix(G)
    assert rotation == sp.Matrix([
        [3, -4, 0, 0], [4, 3, 0, 0],
        [0, 0, 3, 4], [0, 0, -4, 3],
    ]) / 5
    assert _norm(G) == 1
    assert rotation.T * rotation == sp.eye(4)
    assert rotation.det() == 1
    assert _right_matrix(_inverse(G)) == rotation.T
    q = sp.Matrix(sp.symbols("a b c d"))
    assert sp.expand(_norm(rotation * q) - _norm(q)) == 0

    x, y = (1, 2, 0, 0), (-1, 2, 0, 0)
    denominator = _norm(x)
    assert denominator == _norm(y) == 5
    assert _mul(x, G) == y
    assert _mul(_inverse(x), y) == G
    assert _mul(_conjugate(x), y) == (3, 4, 0, 0)
    # Columns generate Og+O; integrality after multiplying by D proves
    # containment for every integer combination, not only sampled vectors.
    sum_generators = rotation.row_join(sp.eye(4))
    assert _integral(denominator * sum_generators)
    assert sp.ilcm(*(value.q for value in sum_generators)) == denominator
    assert not _integral(rotation)  # Norm one does not imply Og=O.


def test_intersection_congruences_give_two_index_five_factors():
    rotation = _right_matrix(G)
    plus = sp.Matrix([[1, -2], [2, 1]])
    minus = sp.Matrix([[1, 2], [-2, 1]])
    intersection = sp.diag(plus, minus)
    # z in O intersect O*g^-1 iff z*g is integral: b=2a, d=-2c mod 5.
    a, b, c, d = sp.symbols("a b c d", integer=True)
    congruence_vector = sp.Matrix([a, 2 * a + 5 * b, c, -2 * c + 5 * d])
    assert intersection.inv() * congruence_vector == sp.Matrix([a + 2 * b, b, c - 2 * d, d])
    assert _integral(rotation * intersection)
    for block, slope, basis in ((rotation[:2, :2], 2, plus), (rotation[2:, 2:], -2, minus)):
        residues = []
        # Exhaust ALL planar residues; integrality depends only on them.
        for u, v in product(range(5), repeat=2):
            integral_image = _integral(block * sp.Matrix([u, v]))
            assert integral_image == ((v - slope * u) % 5 == 0)
            assert integral_image == _integral(basis.inv() * sp.Matrix([u, v]))
            if integral_image:
                residues.append((u, v))
        assert len(residues) == 5
        assert basis.det() == 25 // len(residues) == 5
    assert intersection.det() == 25
    assert intersection.T * intersection == 5 * sp.eye(4)
    # Right rotation carries the preimage intersection onto O intersect Og.
    image_intersection = rotation * intersection
    assert image_intersection.det() == 25
    assert image_intersection.T * image_intersection == 5 * sp.eye(4)
    assert _integral(intersection.inv() * sp.Matrix([1, 2, 0, 0]))
    assert _integral(image_intersection.inv() * sp.Matrix([-1, 2, 0, 0]))


def test_order_unit_stabilizer_is_exactly_eight_signed_basis_units():
    # If Og=O then g=1*g is integral, and det(R_g)=nrd(g)^2=1.
    # An integral sum of four squares equal to 1 forces |coordinate|<=1.
    # Thus this 81-point enumeration is complete for units, not a search
    # for a hidden generator or a truncation of all rational norm-one g.
    units = {q for q in product((-1, 0, 1), repeat=4) if _norm(q) == 1}
    expected = {tuple(sign * x for x in e) for e in BASIS for sign in (-1, 1)}
    assert units == expected and len(units) == 8
    for unit in units:
        action = _right_matrix(unit)
        assert _integral(action) and _integral(action.inv())
        assert action.T * action == sp.eye(4)
        assert action.det() == 1
        assert _inverse(unit) in units
    assert _norm(G) == 1 and G not in units
    assert not _integral(_mul(ONE, G))


def test_ehks_weights_away_from_endpoints_and_midpoints():
    third = _straddle_probabilities(FINE_OFFSET + FINE_STEP / 3)
    assert third == {0: sp.Rational(3, 4), 1: sp.Rational(1, 4)}
    assert third != {0: sp.Rational(2, 3), 1: sp.Rational(1, 3)}
    assert sum(third.values()) == 1

    # A rational coordinate can have irrational probabilities. Exercise the
    # numerical conversion too, although the planar fixture uses only t=1/2.
    quarter = _straddle_probabilities(FINE_OFFSET + FINE_STEP / 4)
    expected = (sp.Rational(1, 2) + sp.sqrt(2) / 4, sp.Rational(1, 2) - sp.sqrt(2) / 4)
    assert all(sp.simplify(quarter[site] - value) == 0 for site, value in enumerate(expected))
    assert all(value.is_Rational is False for value in quarter.values())
    assert sp.simplify(sum(quarter.values())) == 1
    with mp.workdps(60):
        assert _mp_real(third[0]) == mp.mpf(3) / 4
        assert abs(_mp_real(quarter[0]) - (mp.mpf(1) / 2 + mp.sqrt(2) / 4)) < mp.mpf("1e-55")
        assert abs(mp.fsum(_mp_real(value) for value in quarter.values()) - 1) < mp.mpf("1e-55")


def test_fine_straddle_overlap_is_intersection_mass_not_zero():
    # For every n/5, the shifted fine-grid support is {2n-1, 2n}.
    # Distinct n have disjoint supports, including negative coordinates.
    n = sp.Symbol("n", integer=True)
    assert sp.floor((n / 5 - sp.Rational(1, 20)) / sp.Rational(1, 10)) == 2 * n - 1
    for index in range(-5, 6):
        assert _straddle_probabilities(Fraction(index, 5)) == {
            2 * index - 1: Fraction(1, 2), 2 * index: Fraction(1, 2),
        }

    with mp.workdps(60):
        width, radius = 2, 12
        physical, encoded, mass = _planar_state(sp.eye(2), width, radius)
        rotation = _right_matrix(G)
        planar_overlaps = []
        for block, slope in ((rotation[:2, :2], 2), (rotation[2:, 2:], -2)):
            moved, moved_encoded, moved_mass = _planar_state(block, width, radius)
            assert abs(moved_mass - mass) < mp.mpf("1e-50")
            assert abs(mp.fsum(x * x for x in moved_encoded.values()) / mass - 1) < mp.mpf("1e-50")
            common = physical.keys() & moved.keys()
            intersection_mass = mp.fsum(physical[point] ** 2 for point in common)
            preimage_mass = mp.fsum(
                amplitude**2 for (a, b), amplitude in physical.items()
                if (b - slope * a) % 5 == 0
            )
            assert abs(intersection_mass - preimage_mass) < mp.mpf("1e-50")
            inner = mp.fsum(
                amplitude * moved_encoded.get(site, 0) for site, amplitude in encoded.items()
            ) / mp.sqrt(mass * moved_mass)
            assert abs(inner - intersection_mass / mass) < mp.mpf("1e-50")
            planar_overlaps.append(inner)
        assert abs(mp.fsum(x * x for x in encoded.values()) / mass - 1) < mp.mpf("1e-50")
        # The full 4D INNER PRODUCT is the product, not its squared fidelity.
        full_overlap = mp.fprod(planar_overlaps)
        lower, upper = _overlap_bounds(width, 4 * width)
        # The disk contains [-M,M]^2. Its omitted planar mass is <=2*theta*T.
        square_cutoff = isqrt(radius * radius // 2)
        theta, tail = _theta_with_tail(width, square_cutoff)
        planar_omitted_mass = 2 * (theta + tail) * tail
        product_error = 2 * planar_omitted_mass / mass
        assert 0 < product_error < mp.mpf("1e-20")
        assert lower - product_error < full_overlap < upper + product_error

        # Fixed-width calibration only. The parent supplies the limiting
        # index-density theorem: 1/25, not 0 and not the planar value 1/5.
        windows = (
            (1, "0.71777087639", "0.71777087641"),
            (2, "0.07294723889", "0.07294723890"),
            (6, "0.04000000004", "0.04000000005"),
        )
        for sigma, expected_lower, expected_upper in windows:
            lower, upper = _overlap_bounds(sigma, 4 * sigma)
            assert mp.mpf(expected_lower) < lower < upper < mp.mpf(expected_upper)
            assert upper - lower < mp.mpf("1e-20")
            assert lower > mp.mpf(1) / 25


def test_clean_physical_state_is_rebasis_invariant_but_retained_labels_are_not():
    # A bounded (1,i)-plane fixture embeds in O. Amplitude 2^-||x||^2 is
    # exactly Gaussian with s^2=pi/(2*log(2)); truncate in PHYSICAL space.
    shear = sp.Matrix([[1, 1], [0, 1]])
    assert shear.det() == 1 and _integral(shear.inv())
    physical_states, labelled_states = [], []
    for basis in (sp.eye(2), shear):
        physical, labelled = {}, {}
        for point in product((-1, 0, 1), repeat=2):
            coefficients = tuple(basis.inv() * sp.Matrix(point))
            assert _integral(coefficients)
            assert tuple(basis * sp.Matrix(coefficients)) == point
            amplitude = Fraction(1, 2) ** _norm(point)
            physical[point] = amplitude
            labelled[(coefficients, point)] = amplitude
        physical_states.append(physical)
        labelled_states.append(labelled)
    assert physical_states[0] == physical_states[1]
    mass = sum(amplitude**2 for amplitude in physical_states[0].values())
    assert mass == Fraction(9, 4)
    assert all(sum(a * a for a in state.values()) == mass for state in labelled_states)
    clean_inner = sum(a * physical_states[1][x] for x, a in physical_states[0].items()) / mass
    dirty_inner = sum(
        a * labelled_states[1].get(label, 0) for label, a in labelled_states[0].items()
    ) / mass
    assert clean_inner == 1
    assert dirty_inner == Fraction(2, 3) < 1
    assert ((0, 1), (0, 1)) in labelled_states[0]
    assert ((-1, 1), (0, 1)) in labelled_states[1]
    # Discarding the injective coefficient register yields a diagonal MIXED
    # state, not the clean coherent state; coherent uncomputation matters.
    reduced_purity = sum(a**4 for a in physical_states[0].values()) / mass**2
    assert reduced_purity == Fraction(1, 4) < 1


def test_coarse_straddles_break_the_sum_of_squared_weights_normalization():
    # Two physical sites 0,1 in O suffice; the other coordinates factor out.
    # Gaussian amplitudes 1,1/2 give nominal squared norm 5/4.
    weights = {0: sp.Integer(1), 1: sp.Rational(1, 2)}
    nominal_mass = sum(amplitude**2 for amplitude in weights.values())
    norms = []
    for step, offset in ((FINE_STEP, FINE_OFFSET), (Fraction(2), Fraction(1))):
        encoded = {}
        for point, amplitude in weights.items():
            probabilities = _straddle_probabilities(point, step, offset)
            assert sum(probabilities.values()) == 1
            for site, probability in probabilities.items():
                encoded[site] = encoded.get(site, 0) + amplitude * sp.sqrt(probability)
        norms.append(sp.simplify(sum(a**2 for a in encoded.values()) / nominal_mass))
    assert norms[0] == 1
    assert norms[1] == 1 + 2 * sp.sqrt(2) / 5
    assert norms[1] > 1  # Positive cross terms were omitted by nominal_mass.
    assert _straddle_probabilities(0, Fraction(2), Fraction(1)) == {
        -1: Fraction(1, 2), 0: Fraction(1, 2),
    }
    assert _straddle_probabilities(1, Fraction(2), Fraction(1)) == {0: 1}


def test_nonabelian_inversion_cannot_define_the_naive_dihedral_action():
    assert _mul(I, J) == K
    assert _mul(J, I) == tuple(-x for x in K)
    assert _inverse(_mul(I, J)) == tuple(-x for x in K)
    assert _mul(_inverse(I), _inverse(J)) == K
    assert _inverse(_mul(I, J)) != _mul(_inverse(I), _inverse(J))
    assert _inverse(_mul(I, J)) == _mul(_inverse(J), _inverse(I))
    # Inversion is an anti-automorphism here, so it cannot be the C2 action
    # defining G semidirect C2. This does not exclude other HSP reductions.
