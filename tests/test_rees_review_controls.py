"""Exact countercontrols for overstatements in the external AI review.

These are not a validation of the whole Rees theorem or hardness claims.
"""
from itertools import combinations, product
from math import factorial, gcd

import pytest
from sympy import Matrix, Rational, expand, eye, symbols

from theorems.full_jet_resource_certificate import sde_arity
from theorems.uniform_bch_rees import lift_scalar_witness


def test_class_three_bch_denominator_need_not_divide_class_factorial():
    x = Matrix([[0, 1, 0, 0], [0, 0, 1, 0],
                [0, 0, 0, 0], [0, 0, 0, 0]])
    y = Matrix([[0, 0, 0, 0], [0, 0, 0, 0],
                [0, 0, 0, 1], [0, 0, 0, 0]])
    # Exact finite exponential and logarithm in strictly triangular matrices.
    z = (eye(4) + x + x**2 / 2) * (eye(4) + y) - eye(4)
    bch = z - z**2 / 2 + z**3 / 3
    assert bch[0, 3] == Rational(1, 12)
    assert factorial(3) % int(bch[0, 3].q) != 0
    assert gcd(int(bch[0, 3].q), 5) == 1


def test_quadratic_truncation_does_not_define_a_class_three_group():
    def unit(i, j):
        value = Matrix.zeros(4)
        value[i, j] = 1
        return value

    def truncated(x, y):
        return x + y + (x * y - y * x) / 2

    x, y, z = unit(0, 1) + unit(1, 2), unit(2, 3), unit(0, 1)
    defect = truncated(truncated(x, y), z) - truncated(x, truncated(y, z))
    assert defect == -unit(0, 3) / 4


def test_class_three_bch_formula_requires_the_class_bound():
    def unit(i, j):
        value = Matrix.zeros(5)
        value[i, j] = 1
        return value

    def bracket(x, y):
        return x * y - y * x

    def cubic(x, y):
        return (x + y + bracket(x, y) / 2
                + (bracket(x, bracket(x, y)) + bracket(y, bracket(y, x))) / 12)

    x, y, z = unit(0, 1), unit(1, 2), unit(2, 3) + unit(3, 4)
    defect = cubic(cubic(x, y), z) - cubic(x, cubic(y, z))
    assert defect == -unit(0, 4) / 24
    # The missing length-four bracket is real, not a loose class label.
    assert bracket(x, bracket(y, bracket(unit(2, 3), unit(3, 4)))) == unit(0, 4)


def test_class_three_subgroup_reconstruction_words_symbolically():
    def generic(prefix):
        matrix = Matrix.zeros(4)
        for (i, j), value in zip(combinations(range(4), 2), symbols(prefix + "0:6")):
            matrix[i, j] = value
        return matrix

    def bracket(x, y):
        return x * y - y * x

    def multiply(x, y):
        return (x + y + bracket(x, y) / 2
                + (bracket(x, bracket(x, y)) + bracket(y, bracket(y, x))) / 12)

    def commutator(x, y):
        return multiply(multiply(multiply(x, y), -x), -y)

    x, y = generic("x"), generic("y")
    c = commutator(x, y)
    a, b = commutator(x, c), commutator(y, c)
    bracket_word = multiply(c, -multiply(a, b) / 2)
    addition_word = multiply(multiply(multiply(multiply(x, y),
                                              -bracket_word / 2), a / 6), b / 3)
    assert all(expand(value) == 0 for value in bracket_word - bracket(x, y))
    assert all(expand(value) == 0 for value in addition_word - x - y)


@pytest.mark.parametrize("prime,degree,rank", [(5, 3, 3), (11, 3, 4), (11, 7, 5)])
def test_full_label_rank_does_not_require_collision_bound(prime, degree, rank):
    assert gcd(degree, prime - 1) == 1
    # The first rank columns are the identity; the last gives a known kernel.
    last = tuple((i + 2) % prime for i in range(rank))
    rows = [tuple(int(i == j) for j in range(rank)) + (last[i],)
            for i in range(rank)]
    linear_witness = tuple(-value % prime for value in last) + (1,)
    scales = lift_scalar_witness(rows[0], linear_witness,
                                 prime=prime, degree=degree)
    assert any(scales)
    assert all(sum(a * pow(s, degree, prime) for a, s in zip(row, scales))
               % prime == 0 for row in rows)
    assert len(scales) == rank + 1 < sde_arity(degree, rank)


@pytest.mark.parametrize("prime", [3, 5])
def test_elementary_abelianization_is_not_exponent_p(prime):
    modulus = prime**2
    elements = list(product(range(modulus), range(prime)))
    identity = (0, 0)

    def multiply(x, y):
        return ((x[0] + pow(1 + prime, x[1], modulus) * y[0]) % modulus,
                (x[1] + y[1]) % prime)

    def inverse(x):
        return (-x[0] * pow(1 + prime, -x[1], modulus) % modulus,
                -x[1] % prime)

    def power(x, exponent):
        out = identity
        for _ in range(exponent):
            out = multiply(out, x)
        return out

    assert pow(1 + prime, prime, modulus) == 1
    commutators = set()
    for x, y in product(elements, repeat=2):
        xy = multiply(x, y)
        assert (xy[0] % prime, xy[1]) == (
            (x[0] + y[0]) % prime, (x[1] + y[1]) % prime)
        commutators.add(multiply(multiply(inverse(x), inverse(y)), xy))
    derived = {(prime * i, 0) for i in range(prime)}
    assert commutators == derived
    assert all(multiply(z, x) == multiply(x, z)
               for z, x in product(derived, elements))
    assert power((1, 0), prime) == (prime, 0) != identity
    assert power((1, 0), modulus) == identity
    omega = {x for x in elements if power(x, prime) == identity}
    assert omega == {x for x in elements if x[0] % prime == 0}
    assert len(omega) == prime**2 < len(elements)
