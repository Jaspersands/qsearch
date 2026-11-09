"""Prime-power regression tests for UniversalLazardWords (modulus = p^e).

Ground truth is UT_{c+1}(Z/p^e), whose Lie ring is computed directly by
truncated matrix log/exp (1/k! with k <= c < p is a unit mod p^e), never by
BCH words. The words see matrices only through multiplication.
"""
from math import factorial
import random

import pytest

from theorems.universal_lazard_words import UniversalLazardWords


def _mul(a, b, m):
    n = len(a)
    return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(n)) % m for j in range(n)) for i in range(n))


def _lin(terms, n, m):
    return tuple(tuple(sum(c*x[i][j] for c, x in terms) % m for j in range(n)) for i in range(n))


def _eye(n):
    return tuple(tuple(int(i == j) for j in range(n)) for i in range(n))


def _exp(a, m):
    n = len(a)
    result, power = _eye(n), _eye(n)
    for k in range(1, n):
        power = _mul(power, a, m)
        result = _lin([(1, result), (pow(factorial(k), -1, m), power)], n, m)
    return result


def _bracket(a, b, m):
    return _lin([(1, _mul(a, b, m)), (-1, _mul(b, a, m))], len(a), m)


def _nilpotent(n, m, rng):
    return tuple(tuple(rng.randrange(m) if j > i else 0 for j in range(n)) for i in range(n))


def _words(p, c, m, modulus):
    return UniversalLazardWords(p, c, _eye(c+1), lambda a, b: _mul(a, b, m), modulus=modulus)


@pytest.mark.parametrize("p,e,c", [(3, 2, 2), (5, 3, 4), (7, 2, 5), (11, 2, 5), (7, 2, 6), (11, 2, 6)])
def test_prime_power_words_match_matrix_lie_ring(p, e, c):
    m, n, rng = p**e, c+1, random.Random(100*p+10*e+c)
    words = _words(p, c, m, m)
    for _ in range(3):
        a, b = _nilpotent(n, m, rng), _nilpotent(n, m, rng)
        x, y = _exp(a, m), _exp(b, m)
        before = words.multiplication_calls
        assert words.lie_add(x, y) == _exp(_lin([(1, a), (1, b)], n, m), m)
        assert words.multiplication_calls-before <= words.operation_caps()["lie_add"]
        before = words.multiplication_calls
        assert words.lie_bracket(x, y) == _exp(_bracket(a, b, m), m)
        assert words.multiplication_calls-before <= words.operation_caps()["lie_bracket"]


def test_linear_combination_with_coefficients_mod_p_squared():
    p, c, m, rng = 7, 5, 49, random.Random(3)
    words = _words(p, c, m, m)
    logs = [_nilpotent(c+1, m, rng) for _ in range(3)]
    coefficients = [rng.randrange(m) for _ in logs]
    got = words.linear_combination([_exp(a, m) for a in logs], coefficients)
    assert got == _exp(_lin(list(zip(coefficients, logs)), c+1, m), m)


def test_loose_annihilator_is_valid():
    p, c, m, rng = 7, 5, 49, random.Random(4)
    words = _words(p, c, m, p**4)
    a, b = _nilpotent(c+1, m, rng), _nilpotent(c+1, m, rng)
    assert words.lie_add(_exp(a, m), _exp(b, m)) == _exp(_lin([(1, a), (1, b)], c+1, m), m)


def test_default_modulus_is_p_and_unchanged():
    p, c, rng = 7, 5, random.Random(5)
    default, explicit = _words(p, c, p, None), _words(p, c, p, p)
    assert default.modulus == p and default.operation_caps() == explicit.operation_caps()
    a, b = _nilpotent(c+1, p, rng), _nilpotent(c+1, p, rng)
    x, y = _exp(a, p), _exp(b, p)
    assert default.lie_add(x, y) == explicit.lie_add(x, y) == _exp(_lin([(1, a), (1, b)], c+1, p), p)
    assert default.multiplication_calls == explicit.multiplication_calls


def test_default_mod_p_evaluation_fails_at_exponent_p_squared():
    # Smallest exhibited failure: class 2, p=3, UT_3(Z/9); exp(log x+log y) has corner 1/2 = 5 mod 9.
    m = 9
    x, y = _exp(((0, 1, 0), (0, 0, 0), (0, 0, 0)), m), _exp(((0, 0, 0), (0, 0, 1), (0, 0, 0)), m)
    target = _exp(((0, 1, 0), (0, 0, 1), (0, 0, 0)), m)
    assert target[0][2] == 5
    assert _words(3, 2, m, None).lie_add(x, y) != target
    assert _words(3, 2, m, m).lie_add(x, y) == target


@pytest.mark.parametrize("modulus", [48, 98, 1, 0, -49, 49.0, True])
def test_rejects_modulus_that_is_not_a_power_of_p(modulus):
    with pytest.raises(ValueError):
        UniversalLazardWords(7, 5, 0, lambda a, b: a, modulus=modulus)
