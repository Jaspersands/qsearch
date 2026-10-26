"""Independent matrix ground truth and exact fresh-tree accounting.

No old BCH compiler, Rees receiver, or offloaded theorem dependency is imported.
These tests certify finite controls, not the general proposed HSP theorem.
"""
from fractions import Fraction
from math import gcd, prod
import random

import pytest

from theorems.uniform_bch_rees import (
    bch_via_ode, inverse_left_dexp_coefficients, lift_scalar_witness, scalar_line_budget,
)


def _zero(size):
    return tuple((0,) * size for _ in range(size))


def _identity(size):
    return tuple(tuple(int(i == j) for j in range(size)) for i in range(size))


def _add(a, b, p, scale=1):
    return tuple(tuple((x + scale*y) % p for x, y in zip(u, v)) for u, v in zip(a, b))


def _multiply(a, b, p):
    size = len(a)
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(size)) % p
                       for j in range(size)) for i in range(size))


def _exp(a, p):
    out = power = _identity(len(a))
    factorial = 1
    for degree in range(1, len(a)):
        power = _multiply(power, a, p)
        factorial = factorial * degree % p
        out = _add(out, power, p, pow(factorial, -1, p))
    return out


def _log(a, p):
    minus_one = _add(a, _identity(len(a)), p, -1)
    out, power = _zero(len(a)), _identity(len(a))
    for degree in range(1, len(a)):
        power = _multiply(power, minus_one, p)
        out = _add(out, power, p, (-1)**(degree+1) * pow(degree, -1, p))
    return out


def _matrix_bch(a, b, p):
    return _log(_multiply(_exp(a, p), _exp(b, p), p), p)


def _unitriangular(class_bound, p):
    size = class_bound + 1
    positions = tuple((i, j) for i in range(size) for j in range(i+1, size))
    index = {ij: k for k, ij in enumerate(positions)}
    triples = tuple((index[i, j], index[i, k], index[k, j])
                    for i, j in positions for k in range(i+1, j))

    def matrix(vector):
        result = [[0] * size for _ in range(size)]
        for value, (i, j) in zip(vector, positions):
            result[i][j] = value
        return tuple(map(tuple, result))

    def bracket(x, y):
        result = [0] * len(positions)
        for output, a, b in triples:
            result[output] += x[a]*y[b] - y[a]*x[b]
        return tuple(value % p for value in result)

    return len(positions), matrix, bracket


def _filiform(class_bound, p):
    size = class_bound + 1

    def matrix(vector):
        result = [[0] * size for _ in range(size)]
        for i in range(size-1):
            result[i][i+1] = vector[0]
        for i in range(1, size):
            result[class_bound-i][class_bound] += vector[i]
        return tuple(tuple(x % p for x in row) for row in result)

    def bracket(x, y):
        return (0, 0) + tuple((x[0]*y[i-1] - y[0]*x[i-1]) % p
                             for i in range(2, size))

    return size, matrix, bracket


@pytest.mark.parametrize("c,p", [(1, 2), (2, 3), (3, 5), (4, 5), (6, 7), (9, 11), (5, 2**127-1)])
def test_ode_against_independent_matrix_exponential_and_logarithm(c, p):
    dimension, matrix, bracket = _unitriangular(c, p)
    rng = random.Random(397 + c)
    for _ in range(3):
        x = tuple(rng.randrange(p) for _ in range(dimension))
        y = tuple(rng.randrange(p) for _ in range(dimension))
        result = bch_via_ode(x, y, prime=p, nilpotency_class=c, bracket=bracket)
        assert matrix(result) == _matrix_bch(matrix(x), matrix(y), p)


@pytest.mark.parametrize("c,p", [(4, 5), (8, 11), (12, 17)])
def test_growing_class_filiform_uses_uniform_polynomial_bracket_count(c, p):
    dimension, matrix, bracket = _filiform(c, p)
    calls = 0

    def counted(x, y):
        nonlocal calls
        calls += 1
        return bracket(x, y)

    rng = random.Random(911 + c)
    x, y = (tuple(rng.randrange(p) for _ in range(dimension)) for _ in range(2))
    result = bch_via_ode(x, y, prime=p, nilpotency_class=c, bracket=counted)
    assert matrix(result) == _matrix_bch(matrix(x), matrix(y), p)
    assert calls == (c-1)*c*(c+1)*(c+2)//6
    e0, e1 = (1,) + (0,)*c, (0, 1) + (0,)*(c-1)
    top = e1
    for _ in range(c-1):
        top = bracket(e0, top)
    assert top[-1] == 1  # The class bound is attained, not an abelian padded fixture.
    assert bracket(e0, top) == (0,)*dimension


def test_dexp_orientation_and_reciprocal_series():
    p, c = 101, 9
    coefficients = inverse_left_dexp_coefficients(p, c)
    expected = [Fraction(1), Fraction(1, 2), Fraction(1, 12), 0,
                Fraction(-1, 720), 0, Fraction(1, 30240), 0, Fraction(-1, 1209600)]
    assert coefficients == tuple(int(x.numerator) * pow(int(x.denominator), -1, p) % p
                                 for x in map(Fraction, expected))
    dimension, matrix, bracket = _unitriangular(2, 3)
    x, y = (1, 0, 0), (0, 0, 1)
    xy = bch_via_ode(x, y, prime=3, nilpotency_class=2, bracket=bracket)
    assert matrix(xy) != _matrix_bch(matrix(y), matrix(x), 3)
    assert xy[1] == 2  # +[x,y]/2, not the opposite Maurer-Cartan convention.


def test_associativity_inverse_and_abelian_control():
    dimension, _, bracket = _unitriangular(4, 7)
    rng = random.Random(1729)
    x, y, z = (tuple(rng.randrange(7) for _ in range(dimension)) for _ in range(3))
    def multiply(a, b):
        return bch_via_ode(a, b, prime=7, nilpotency_class=4, bracket=bracket)
    assert multiply(multiply(x, y), z) == multiply(x, multiply(y, z))
    assert multiply(x, tuple(-v % 7 for v in x)) == (0,)*dimension
    assert bch_via_ode((3, 2), (4, 6), prime=7, nilpotency_class=1,
                       bracket=lambda a, b: (0, 0)) == (0, 1)


def test_understated_class_is_not_silently_certified_by_vector_checks():
    _, matrix, bracket = _unitriangular(3, 5)
    x, y = (1, 0, 0, 1, 0, 0), (0, 0, 0, 0, 0, 1)
    wrong = bch_via_ode(x, y, prime=5, nilpotency_class=2, bracket=bracket)
    assert matrix(wrong) != _matrix_bch(matrix(x), matrix(y), 5)


@pytest.mark.parametrize("p,c", [(5, 5), (3, 4), (7, 0), (7, True), (1, 1)])
def test_invalid_characteristic_and_class(p, c):
    with pytest.raises(ValueError):
        inverse_left_dexp_coefficients(p, c)


def test_vector_and_bracket_shape_validation():
    kwargs = dict(prime=5, nilpotency_class=2, bracket=lambda x, y: (0,))
    for x, y in [((), ()), ((1,), (1, 0)), ((-1,), (0,)), ((True,), (0,))]:
        with pytest.raises(ValueError):
            bch_via_ode(x, y, **kwargs)
    with pytest.raises(ValueError):
        bch_via_ode((1, 0), (0, 1), **kwargs)


@pytest.mark.parametrize("profile,samples", [((1,), 4), ((3, 1), 5), ((6, 3, 1), 8),
                                             ((13, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1), 16)])
def test_scalar_line_budget_exact_tree_and_parameter_bound(profile, samples):
    budget = scalar_line_budget(profile, samples)
    product = prod((d+1)**rank for d, rank in enumerate(profile[1:], start=2))
    assert budget.leaves_per_terminal == product
    assert budget.lifted_sources == samples * product
    assert budget.original_inputs == len(profile) * samples * product
    assert budget.cover_dimension == sum(profile)
    r = budget.derived_dimension
    assert len(profile) <= r+1
    assert budget.cover_dimension <= profile[0] + r*(r+1)//2
    assert product <= budget.derived_parameter_leaf_bound
    expected = budget.lifted_sources
    for stage in budget.stages:
        assert stage.consumed_targets == expected
        assert expected == stage.conversions * stage.arity
        expected = stage.conversions
    assert expected == samples
    assert budget.central_character_measurements == sum(s.consumed_targets for s in budget.stages)
    assert budget.scalar_solves == sum(s.conversions for s in budget.stages)


def test_budget_agrees_with_literal_small_tree():
    budget = scalar_line_budget((6, 3, 1), 2)
    arities = (4, 3, 3, 3)
    def count(stage):
        if stage < 0:
            return 1, 0, 0
        leaves, solves, targets = count(stage-1)
        arity = arities[stage]
        return arity*leaves, 1 + arity*solves, arity*(1 + targets)
    leaves, solves, targets = count(len(arities)-1)
    assert (budget.lifted_sources, budget.scalar_solves, budget.central_character_measurements) == (
        2*leaves, 2*solves, 2*targets)


@pytest.mark.parametrize("profile,samples", [((), 1), ((3, 1, 0), 1), ((3, 1, 1), 1),
                                             ((3, 2), 1), ((3, True), 1), ((3,), 0), ((3,), True)])
def test_invalid_rank_profiles_are_not_admitted(profile, samples):
    with pytest.raises(ValueError):
        scalar_line_budget(profile, samples)


@pytest.mark.parametrize("p", [3, 5, 7, 11, 17, 23])
def test_reduced_power_witness_lift_all_field_entries_and_degrees(p):
    for degree in range(1, p):
        delta = gcd(degree, p-1)
        for x in range(p):
            labels = (1, -pow(x, delta, p) % p, 0)
            witness = (x, 1, 0)
            lifted = lift_scalar_witness(labels, witness, prime=p, degree=degree)
            assert lifted[-1] == 0
            assert bool(lifted[0]) == bool(x)
            assert any(lifted)
            assert all(pow(a, degree, p) == pow(b, delta, p)
                       for a, b in zip(lifted, witness))
            assert sum(a*pow(b, degree, p) for a, b in zip(labels, lifted)) % p == 0


def test_false_or_empty_scalar_witnesses_fail_before_conversion():
    for labels, witness in [((), ()), ((0, 0), (0, 0)), ((1, 1), (1, 1)),
                            ((1, 0), (1,)), ((1, 0), (-1, 1))]:
        with pytest.raises(ValueError):
            lift_scalar_witness(labels, witness, prime=11, degree=3)


def test_field_sensitive_budget_and_safe_prime_control():
    profile = (13, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1)
    # 47-1=2*23, so for every d<=12 the power index is 1 or 2.
    budget = scalar_line_budget(profile, 16, prime=47)
    assert budget.leaves_per_terminal == prod((gcd(d, 46)+1)**r
                                             for d, r in enumerate(profile[1:], start=2))
    assert {stage.arity for stage in budget.stages} == {2, 3}
    assert budget.leaves_per_terminal <= 3**sum(profile[1:])
    assert budget.leaves_per_terminal < scalar_line_budget(profile, 16).leaves_per_terminal
    with pytest.raises(ValueError):
        scalar_line_budget(profile, 16, prime=11)
