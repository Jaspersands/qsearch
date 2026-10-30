"""230 bounded class-three controls, not emitted-circuit verification.

Expected products use exp/log of 4-by-4 matrices over F_p[t]/(t^4),
independently of the production BCH recurrence and bracket callback.
"""
from random import Random

import pytest

from theorems.guarded_bch_permutation import GuardedBCHPermutation
from theorems.uniform_bch_rees import bch_via_ode


_COORDS = tuple(
    (degree, i, j)
    for degree in (1, 2, 3)
    for i in range(4)
    for j in range(i + degree, 4)
)
_INDEX = {coordinate: k for k, coordinate in enumerate(_COORDS)}
_WEIGHTS = tuple(degree for degree, _, _ in _COORDS)
_BCH_CASES = 40
_TRANSLATION_CASES = 25


def _matrix(vector):
    assert len(vector) == 10
    result = [[[0] * 4 for _ in range(4)] for _ in range(4)]
    for value, (degree, i, j) in zip(vector, _COORDS):
        result[degree][i][j] = value
    return result


def _identity():
    result = _matrix((0,) * 10)
    for i in range(4):
        result[0][i][i] = 1
    return result


def _add(a, b, p, scale=1):
    return [
        [[(a[d][i][j] + scale * b[d][i][j]) % p for j in range(4)]
         for i in range(4)]
        for d in range(4)
    ]


def _multiply(a, b, p):
    return [
        [[sum(a[e][i][k] * b[d - e][k][j]
              for e in range(d + 1) for k in range(4)) % p
          for j in range(4)] for i in range(4)]
        for d in range(4)
    ]


def _exp(a, p):
    power = result = _identity()
    factorial = 1
    for degree in (1, 2, 3):
        factorial = factorial * degree % p
        power = _multiply(power, a, p)
        result = _add(result, power, p, pow(factorial, -1, p))
    return result


def _log(a, p):
    minus_one = _add(a, _identity(), p, -1)
    result, power = _matrix((0,) * 10), _identity()
    for degree in (1, 2, 3):
        power = _multiply(power, minus_one, p)
        result = _add(result, power, p,
                      (-1) ** (degree + 1) * pow(degree, -1, p))
    return result


def _matrix_product(x, y, p):
    return _log(_multiply(_exp(_matrix(x), p), _exp(_matrix(y), p), p), p)


def _encode(vector, p):
    bits = (p - 1).bit_length()
    return sum(value << (i * bits) for i, value in enumerate(vector))


def _counted_bracket(p):
    calls = [0]

    def bracket(x, y):
        calls[0] += 1
        result = [0] * 10
        for (d, i, j), a in zip(_COORDS, x):
            for (e, k, ell), b in zip(_COORDS, y):
                if d + e <= 3:
                    if j == k:
                        result[_INDEX[d + e, i, ell]] += a * b
                    if ell == i:
                        result[_INDEX[d + e, k, j]] -= a * b
        return tuple(value % p for value in result)

    return bracket, calls


@pytest.mark.parametrize("p", [5, 65537])
def test_class_three_bch_against_polynomial_matrix_exp_log(p):
    assert len(_COORDS) == 10
    assert _WEIGHTS == (1,) * 6 + (2,) * 3 + (3,)
    bracket, calls = _counted_bracket(p)
    units = [tuple(int(k == _INDEX[coordinate]) for k in range(10))
             for coordinate in ((1, 0, 1), (1, 1, 2), (1, 2, 3))]
    top = bracket(units[0], bracket(units[1], units[2]))
    assert top == (0,) * 9 + (1,)  # Class three is attained.
    assert bracket(units[0], top) == (0,) * 10

    rng = Random(412301 + p)
    for _ in range(_BCH_CASES):
        x, y = (tuple(rng.randrange(p) for _ in range(10)) for _ in range(2))
        expected = _matrix_product(x, y, p)
        calls[0] = 0
        actual = bch_via_ode(x, y, prime=p, nilpotency_class=3, bracket=bracket)
        assert calls[0] == 20
        assert _matrix(actual) == expected


@pytest.mark.parametrize("p", [5, 65537])
@pytest.mark.parametrize("scale_choice", [0, 1, -1])
def test_class_three_right_translation_cleanup_padding_and_dirty_scratch(p, scale_choice):
    scale = scale_choice % p
    bracket, calls = _counted_bracket(p)
    model = GuardedBCHPermutation(
        prime=p, nilpotency_class=3, group_dimension=10, control_dimension=9,
        section=lambda u: u + (0,), weights=_WEIGHTS, scale=scale, bracket=bracket,
    )
    rng = Random(412301 + p + scale)
    for _ in range(_TRANSLATION_CASES):
        u = tuple(rng.randrange(p) for _ in range(9))
        x = tuple(rng.randrange(p) for _ in range(10))
        control, target = _encode(u, p), _encode(x, p)
        translation = tuple(-value * pow(scale, d, p) % p
                            for value, d in zip(u + (0,), _WEIGHTS))
        expected_matrix = _matrix_product(x, translation, p) if scale else _matrix(x)
        expected = _encode(tuple(expected_matrix[d][i][j] for d, i, j in _COORDS), p)

        calls[0] = 0
        assert model.permutation(control, target) == expected
        assert calls[0] == (20 if scale else 0)
        assert model.permutation(control, expected, inverse=True) == target

        calls[0] = 0
        assert model.lift(control, target) == (control, expected, 0)
        # Two semantic evaluators; the four-pass compiled cap is not executed.
        assert calls[0] == (40 if scale else 0)
        assert model.lift(control, expected, inverse=True) == (control, target, 0)

        scratch = rng.getrandbits((p - 1).bit_length() * 10)
        start = (control, target, scratch)
        assert model.lift(*model.lift(*start), inverse=True) == start
        assert model.lift(*model.lift(*start, inverse=True)) == start

    # Cover every limb position, including padding in the top central grade.
    for dimension, is_control in ((9, True), (10, False)):
        for limb in range(dimension):
            padded = _encode(tuple(p if i == limb else 0 for i in range(dimension)), p)
            u_word, x_word = (padded, target) if is_control else (control, padded)
            calls[0] = 0
            assert model.permutation(u_word, x_word) == x_word
            assert model.permutation(u_word, x_word, inverse=True) == x_word
            assert model.lift(u_word, x_word) == (u_word, x_word, 0)
            assert calls[0] == 0

    if scale == 0:
        def forbidden(_):
            pytest.fail("zero-scale slot evaluated the section")

        zero_model = GuardedBCHPermutation(
            prime=p, nilpotency_class=3, group_dimension=10, control_dimension=9,
            section=forbidden, weights=_WEIGHTS, scale=0, bracket=bracket,
        )
        calls[0] = 0
        assert zero_model.lift(control, target) == (control, target, 0)
        assert calls[0] == 0
