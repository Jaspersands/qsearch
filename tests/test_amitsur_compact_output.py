"""Bounded primitive algebra controls over Q(sqrt(2)), not a quantum algorithm.

Tensor bases are lexicographic in (1, s), with s**2 = 2 in each slot.
These checks do not prove a general height bound or force an algorithm to
choose the poor gauge. All expanded Pell examples have exponent at most 64.
"""

from fractions import Fraction as Q
from itertools import product
from math import gcd

import pytest


def _qvec(*entries):
    return tuple(Q(entry) for entry in entries)


ONE2 = _qvec(1, 0)
ONE4 = _qvec(1, 0, 0, 0)
ONE8 = _qvec(1, 0, 0, 0, 0, 0, 0, 0)
BASIS4 = tuple(_qvec(*(int(i == j) for i in range(4))) for j in range(4))
IDENTITY_MATRIX = (_qvec(1, 0), _qvec(0, 1))
# The identity for the trace-product algebra is not the tensor-ring unit.
TRACE_IDENTITY = _qvec(Q(1, 2), 0, 0, Q(1, 4))
ALPHA = _qvec(3, 1, 2, 1)
ALPHA_INVERSE = _qvec(Q(-1, 7), Q(-5, 7), Q(2, 7), Q(3, 7))


def _mul(x, y):
    """Commutative multiplication in F, F tensor F, or F tensor F tensor F."""
    assert len(x) == len(y) and len(x) in (2, 4, 8)
    result = [Q(0)] * len(x)
    for i, a in enumerate(x):
        for j, b in enumerate(y):
            result[i ^ j] += a * b * 2 ** (i & j).bit_count()
    return tuple(result)


def _tensor(x, y):
    assert len(x) == len(y) == 2
    return tuple(a * b for a in x for b in y)


def _inverse2(x):
    a, b = x
    norm = a * a - 2 * b * b
    return (a / norm, -b / norm)


def _inverse4(x):
    # F tensor F -> F x F evaluates (s0, s1) at (s, s) and (s, -s).
    a, b, c, d = x
    p, q = _inverse2((a + 2 * d, b + c))
    r, t = _inverse2((a - 2 * d, c - b))
    return ((p + r) / 2, (q - t) / 2, (q + t) / 2, (p - r) / 4)


def _lift01(x):
    a, b, c, d = x
    return (a, Q(0), b, Q(0), c, Q(0), d, Q(0))


def _lift02(x):
    a, b, c, d = x
    return (a, b, Q(0), Q(0), c, d, Q(0), Q(0))


def _lift12(x):
    return x + (Q(0),) * 4


def _delta0(gamma):
    return _tensor(_inverse2(gamma), gamma)


def _delta1(alpha):
    return _mul(_mul(_lift12(alpha), _lift02(_inverse4(alpha))), _lift01(alpha))


def _twisted(x, y, cocycle):
    value = _mul(_mul(_lift01(x), cocycle), _lift12(y))
    # Trace over the middle slot: Tr(1) = 2, Tr(s) = 0.
    return tuple(2 * value[i] for i in (0, 1, 4, 5))


def _rho(x):
    # r tensor t acts on z by r * Tr(t*z), in the basis (1, s).
    a, b, c, d = x
    return ((2 * a, 4 * b), (2 * c, 4 * d))


def _matmul(x, y):
    return tuple(tuple(sum(x[i][k] * y[k][j] for k in range(2))
                       for j in range(2)) for i in range(2))


def _convert(alpha, x):
    return _rho(_mul(alpha, x))


def _combine(coefficients, vectors):
    return tuple(sum(c * v[i] for c, v in zip(coefficients, vectors))
                 for i in range(4))


def _pell(exponent):
    assert 0 <= exponent <= 64
    a, b = 1, 0
    for _ in range(exponent):
        a, b = 3 * a + 4 * b, 2 * a + 3 * b
    return a, b


def test_fixed_tensor_arithmetic_and_nontrivial_cochain_inverse():
    assert _mul(_qvec(0, 1), _qvec(0, 1)) == _qvec(2, 0)
    for size in (4, 8):
        for index in (1, 2) if size == 4 else (1, 2, 4):
            s = _qvec(*(int(i == index) for i in range(size)))
            assert _mul(s, s) == _qvec(2, *([0] * (size - 1)))
    assert _mul(BASIS4[1], BASIS4[2]) == BASIS4[3]
    assert _inverse2(_qvec(1, 1)) == _qvec(-1, 1)
    assert _inverse4(ALPHA) == ALPHA_INVERSE
    assert _mul(ALPHA, ALPHA_INVERSE) == ONE4
    assert _inverse4(ALPHA_INVERSE) == ALPHA


@pytest.mark.parametrize("gamma", [
    _qvec(1, 0), _qvec(3, 2), _qvec(2, 1), _qvec(Q(3, 2), Q(1, 3)),
])
def test_delta_of_delta_gamma_is_one(gamma):
    alpha = _delta0(gamma)
    assert _mul(gamma, _inverse2(gamma)) == ONE2
    assert _mul(alpha, _inverse4(alpha)) == ONE4
    assert _delta1(alpha) == ONE8


def test_trace_map_preserves_multiplication_on_all_basis_pairs():
    for x, y in product(BASIS4, repeat=2):
        assert _rho(_twisted(x, y, ONE8)) == _matmul(_rho(x), _rho(y))
    assert _rho(TRACE_IDENTITY) == IDENTITY_MATRIX
    assert _rho(ONE4) != IDENTITY_MATRIX
    for x in BASIS4:
        assert _twisted(TRACE_IDENTITY, x, ONE8) == x
        assert _twisted(x, TRACE_IDENTITY, ONE8) == x


def test_nontrivial_coboundary_requires_alpha_not_its_inverse():
    cocycle = _delta1(ALPHA)
    assert cocycle != ONE8
    samples = BASIS4 + (_qvec(Q(1, 2), Q(-2, 3), Q(3, 5), Q(1, 7)),)
    wrong_orientation_failures = 0
    for x, y in product(samples, repeat=2):
        xy = _twisted(x, y, cocycle)
        assert _mul(ALPHA, xy) == _twisted(_mul(ALPHA, x), _mul(ALPHA, y), ONE8)
        assert _convert(ALPHA, xy) == _matmul(_convert(ALPHA, x), _convert(ALPHA, y))
        wrong_orientation_failures += (
            _convert(ALPHA_INVERSE, xy)
            != _matmul(_convert(ALPHA_INVERSE, x), _convert(ALPHA_INVERSE, y))
        )
    assert wrong_orientation_failures > 0
    unit = _mul(ALPHA_INVERSE, TRACE_IDENTITY)
    assert _convert(ALPHA, unit) == IDENTITY_MATRIX
    for x in BASIS4:
        assert _twisted(unit, x, cocycle) == x
        assert _twisted(x, unit, cocycle) == x


def test_selected_ideal_is_left_stable_for_nontrivial_coboundary():
    cocycle = _delta1(ALPHA)
    ideal = tuple(_mul(ALPHA_INVERSE, x) for x in (BASIS4[0], BASIS4[2]))
    assert tuple(_mul(ALPHA, v) for v in ideal) == (BASIS4[0], BASIS4[2])
    # These independent images certify dimension two, hence minimality in M_2(Q).
    for x, j in product(BASIS4, range(2)):
        matrix = _convert(ALPHA, x)
        expected = _combine((matrix[0][j], matrix[1][j]), ideal)
        assert _twisted(x, ideal[j], cocycle) == expected
    assert any(
        any(_mul(ALPHA, _twisted(v, x, cocycle))[i] != 0 for i in (1, 3))
        for v, x in product(ideal, BASIS4)
    )  # This left ideal is not a right ideal.


@pytest.mark.parametrize("m", range(7))
def test_bounded_pell_poor_gauge_coordinates_and_growth(m):
    exponent = 1 << m
    a, b = _pell(exponent)
    assert a * a - 2 * b * b == 1 and gcd(a, b) == 1
    assert 2 * exponent <= a.bit_length() <= 3 * exponent
    assert 2 * exponent <= b.bit_length() <= 3 * exponent
    gamma = _qvec(a, b)
    assert _inverse2(gamma) == _qvec(a, -b)
    alpha = _delta0(gamma)
    assert alpha == _qvec(a * a, a * b, -a * b, -b * b)
    assert _delta1(alpha) == ONE8

    compact_value = _delta0(_qvec(3, 2))
    for _ in range(m):
        compact_value = _mul(compact_value, compact_value)
    assert compact_value == alpha  # m squarings, independently checked by recurrence.

    ideal = (_qvec(a, -b, 0, 0), _qvec(0, 0, a, -b))
    images = tuple(_mul(alpha, v) for v in ideal)
    assert images == (_qvec(a, 0, -b, 0), _qvec(-2 * b, 0, a, 0))
    assert images[0][0] * images[1][2] - images[1][0] * images[0][2] == 1
    for x, j in product(BASIS4, range(2)):
        matrix = _rho(x)
        assert _twisted(x, ideal[j], ONE8) == _combine(
            (matrix[0][j], matrix[1][j]), ideal
        )

    slope = Q(-b, a)
    assert slope.numerator == -b and slope.denominator == a
    for scale in (Q(1), Q(1, a), Q(1, b), Q(-2, 5)):
        assert (-scale * b) / (scale * a) == slope
    assert slope.denominator.bit_length() >= 2 * exponent
    assert _convert(alpha, ONE4)[0][0] == 2 * a * a
    assert (2 * a * a).bit_length() >= 4 * exponent


def test_tiny_alternative_trivialization_and_ideal_remain_available():
    assert _delta1(ONE4) == ONE8
    small_ideal = (BASIS4[0], BASIS4[2])
    assert all(coordinate in (Q(0), Q(1)) for v in small_ideal for coordinate in v)
    for x in BASIS4:
        assert _convert(ONE4, x) == _rho(x)
    for x, j in product(BASIS4, range(2)):
        matrix = _rho(x)
        assert _twisted(x, small_ideal[j], ONE8) == _combine(
            (matrix[0][j], matrix[1][j]), small_ideal
        )
    for m in range(7):
        a, b = _pell(1 << m)
        assert _delta1(_delta0(_qvec(a, b))) == _delta1(ONE4)
        assert -b != 0  # F tensor (a-b*s) differs from F tensor 1.
