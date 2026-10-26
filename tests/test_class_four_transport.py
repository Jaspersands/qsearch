"""Exact universal coefficient checks, not an oracle-driven HSP execution.

The free-word regular representation retains every weighted word through
the truncation degree. It checks identities, not random matrix examples.
"""
from itertools import product

import sympy as sp


def free_word_matrices(weights, cutoff):
    words = [word for size in range(cutoff+1)
             for word in product(range(len(weights)), repeat=size)
             if sum(weights[letter] for letter in word) <= cutoff]
    index = {word: i for i, word in enumerate(words)}
    matrices = [sp.SparseMatrix(len(words), len(words), {
        (index[(letter,)+word], index[word]): 1
        for word in words if (letter,)+word in index
    }) for letter in range(len(weights))]
    return words, matrices


def bracket(x, y):
    return x*y-y*x


def exponential(x, cutoff):
    return sum((x**k/sp.factorial(k) for k in range(1, cutoff+1)), sp.eye(x.rows))


def logarithm(g, cutoff):
    t = g-sp.eye(g.rows)
    return sum(((-1)**(k+1)*t**k/sp.Integer(k) for k in range(1, cutoff+1)),
               sp.zeros(g.rows))


def potential_terms(x, y, a):
    c = bracket(x, y)
    return [
        (1, a), (sp.Rational(1, 2), c),
        (1, bracket(x, a)), (-sp.Rational(1, 2), bracket(y, a)),
        (sp.Rational(1, 3), bracket(x, c)), (-sp.Rational(1, 6), bracket(y, c)),
        (sp.Rational(1, 2), bracket(x, bracket(x, a))),
        (-sp.Rational(1, 2), bracket(y, bracket(x, a))),
        (sp.Rational(1, 6), bracket(y, bracket(y, a))),
        (sp.Rational(1, 4), bracket(a, c)),
        (sp.Rational(1, 8), bracket(x, bracket(x, c))),
        (-sp.Rational(1, 8), bracket(y, bracket(x, c))),
        (sp.Rational(1, 24), bracket(y, bracket(y, c))),
    ]


def test_full_weighted_free_algebra_potential_identity():
    words, (x, y, a) = free_word_matrices((1, 1, 2), 4)
    assert len(words) == 49
    actual = logarithm(exponential(x-y, 4)*exponential(y+a, 4)*exponential(-x, 4), 4)
    terms = potential_terms(x, y, a)
    expected = sum((coefficient*term for coefficient, term in terms), sp.zeros(x.rows))
    assert actual == expected
    # Coefficients are uniquely checked, not a redundant bracket identity.
    assert sp.Matrix.hstack(*(term[:, 0] for _, term in terms)).rank() == len(terms)
    for coefficient, _ in terms:
        assert set(sp.factorint(sp.denom(coefficient))) <= {2, 3}
    # A normal-first/normal-last sign swap is not an innocuous convention.
    assert actual != expected-bracket(x, y)


def test_residual_is_central_in_the_derived_algebra_at_class_four():
    words, (x, y, a) = free_word_matrices((1, 1, 2), 4)
    q = logarithm(exponential(x-y, 4)*exponential(y+a, 4)*exponential(-x, 4), 4)
    remainder = q-a-bracket(x, y)/2
    assert remainder != sp.zeros(x.rows)
    assert all(sum((1, 1, 2)[letter] for letter in words[i]) >= 3
               for i, value in enumerate(remainder[:, 0]) if value)
    # These generate the weight-two Lie component; higher weights vanish
    # against this residual by the same additive filtration inequality.
    assert bracket(remainder, a) == sp.zeros(x.rows)
    assert bracket(remainder, bracket(x, y)) == sp.zeros(x.rows)


def test_class_five_has_a_noncentral_cubic_potential_coefficient():
    _, (x, y) = free_word_matrices((1, 1), 5)
    c = bracket(x, y)
    cubic = bracket(x, c)/3+bracket(y, c)/6
    obstruction = bracket(cubic, c)
    assert obstruction != sp.zeros(x.rows)
    # A coefficient +/-1/3 survives every prime >5, not just a sampled p.
    assert any(abs(value) == sp.Rational(1, 3) for value in obstruction[:, 0])
    # Read the cubic part of the actual exp/log word along q=(t,t).
    t = sp.symbols("t")
    q = logarithm(exponential(t*x, 5)*exponential(t*y, 5)
                  *exponential(-t*(x+y), 5), 5)
    assert q.applyfunc(lambda value: sp.expand(value).coeff(t, 3)) == cubic


def test_normalizer_logarithm_recovers_the_full_adjoint_not_only_first_order():
    t = sp.symbols("t")
    e_minus_one = t+t**2/2+t**3/6
    recovered = sp.Poly(sp.expand(e_minus_one-e_minus_one**2/2+e_minus_one**3/3), t)
    assert [recovered.nth(i) for i in range(4)] == [0, 1, 0, 0]
    assert e_minus_one != t
