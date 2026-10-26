"""Exact scope/falsifier controls, not a higher-class quantum receiver.

The supplied matrices are proof examples. They do not supply hidden advice
to an algorithm, instantiate an HSP oracle, or establish a hard problem.
"""
from functools import lru_cache

import pytest
import sympy as sp


def unit(size, row, column):
    return sp.SparseMatrix(size, size, {(row, column): 1})


def bracket(left, right):
    return left*right-right*left


def span(matrices):
    nonzero = [matrix for matrix in matrices if not matrix.is_zero_matrix]
    if not nonzero:
        return ()
    size = nonzero[0].rows
    columns = sp.Matrix.hstack(*(matrix.reshape(size*size, 1) for matrix in nonzero))
    return tuple(column.reshape(size, size) for column in columns.columnspace())


def bracket_span(left, right):
    return span(bracket(x, y) for x in left for y in right)


def lower_central(basis, cap):
    series = [tuple(basis)]
    for _ in range(cap):
        series.append(bracket_span(basis, series[-1]))
        if not series[-1]:
            return tuple(series)
    raise AssertionError("nilpotency cap exhausted")


@lru_cache(None)
def coupled_family(c):
    # UT5 acts on an abelian length-c chain through its E12 coefficient.
    # Sharing this generator gives a semidirect product, not an independent
    # direct-product example with an appended high-class factor.
    size = c+6
    triangular = {(i, j): unit(size, i, j) for i in range(5) for j in range(i+1, 5)}
    chain = tuple(unit(size, 5+c-1-j, 5+c) for j in range(c))
    x = triangular[0, 1]+sum((unit(size, 5+j, 6+j) for j in range(c-1)),
                            sp.zeros(size))
    triangular[0, 1] = x
    basis = tuple(triangular.values())+chain
    return basis, triangular, chain


def exponential(value, degree):
    result = power = sp.eye(value.rows)
    for k in range(1, degree+1):
        power = power*value
        result += power/sp.factorial(k)
    return result


def logarithm(value, degree):
    delta = value-sp.eye(value.rows)
    result = sp.zeros(value.rows)
    power = sp.eye(value.rows)
    for k in range(1, degree+1):
        power = power*delta
        result += (-1)**(k+1)*power/sp.Integer(k)
    return result.applyfunc(sp.expand)


@pytest.mark.parametrize('c', [5, 6, 8])
def test_coupled_family_has_arbitrary_class_and_commuting_third_term(c):
    basis, triangular, chain = coupled_family(c)
    series = lower_central(basis, c)
    assert len(span(basis)) == 10+c
    assert len(series)-1 == c
    assert len(span(basis+series[1])) == len(basis)  # Actual bracket closure.
    derived, third = series[1:3]
    second_derived = bracket_span(derived, derived)
    assert len(second_derived) == 1  # Not metabelian.
    assert not bracket_span(derived, second_derived)
    assert not bracket_span(third, derived)
    assert not bracket_span(basis, second_derived)
    x = triangular[0, 1]
    assert all(bracket(x, chain[j]) == chain[j+1] for j in range(c-1))
    assert bracket(x, chain[-1]).is_zero_matrix


@pytest.mark.parametrize('c', [5, 6, 8])
def test_actual_potential_has_quadratic_noncentral_and_degree_c_central_parts(c):
    _, triangular, chain = coupled_family(c)
    x, h = triangular[0, 1], triangular[1, 2]+chain[0]
    t = sp.symbols('t')
    actual = logarithm(exponential(t*x, c)*exponential(t*h, c)
                       *exponential(-t*(x+h), c), c)
    noncentral = t**2*triangular[0, 2]/2
    central = sum((sp.Rational(j, sp.factorial(j+1))*t**(j+1)*chain[j]
                   for j in range(1, c)), sp.zeros(x.rows))
    assert actual == noncentral+central
    derived = bracket_span(coupled_family(c)[0], coupled_family(c)[0])
    assert all(bracket(central, value).is_zero_matrix for value in derived)
    assert not bracket(noncentral, triangular[2, 4]).is_zero_matrix
    top = actual.applyfunc(lambda value: value.coeff(t, c))
    assert top == sp.Rational(c-1, sp.factorial(c))*chain[-1]
    assert not top.is_zero_matrix  # A cubic-only scalar backend is inadequate.


@pytest.mark.parametrize('c', [5, 6, 8])
def test_quartic_witness_alone_does_not_remove_the_higher_central_phase(c):
    p = 257
    # These can multiply a nonzero central character with both an E15 and
    # a v_(c-1) component, so this is not limited to zero-rank Weyl sectors.
    labels, scales, shifts = (-16, 1), (1, 2), (1, 0)
    assert sum(label*scale**4 for label, scale in zip(labels, scales)) % p == 0
    coefficient = (c-1)*pow(int(sp.factorial(c)), -1, p) % p
    top = coefficient*sum(label*scale**c for label, scale in zip(labels, scales))
    quartic = coefficient*int(sp.binomial(c, 4))*sum(
        label*shift**(c-4)*scale**4 for label, shift, scale in zip(labels, shifts, scales))
    assert top % p != 0
    assert quartic % p != 0  # Translation of the high-degree term matters too.


def test_class_two_derived_group_alone_does_not_give_a_quadratic_potential():
    basis = tuple(unit(6, i, j) for i in range(6) for j in range(i+1, 6))
    derived = bracket_span(basis, basis)
    assert bracket_span(derived, derived)
    assert not bracket_span(derived, bracket_span(derived, derived))
    assert bracket_span(bracket_span(basis, derived), derived)
    x = unit(6, 0, 1)+unit(6, 2, 3)+unit(6, 4, 5)
    y = unit(6, 1, 2)+unit(6, 3, 4)
    t = sp.symbols('t')
    actual = logarithm(exponential(t*x, 5)*exponential(t*y, 5)
                       *exponential(-t*(x+y), 5), 5)
    cubic = actual.applyfunc(lambda value: value.coeff(t, 3))
    assert bracket(cubic, bracket(x, y)) == sp.Rational(4, 3)*unit(6, 0, 5)


@pytest.mark.parametrize('c', [5, 6])
def test_arbitrary_h_finish_needs_more_than_the_old_two_image_calls(c):
    basis, triangular, _ = coupled_family(c)
    hidden_line = (triangular[0, 1],)
    original_derived = bracket_span(basis, basis)
    assert len(span(hidden_line+original_derived)) == len(original_derived)+1
    ambient = basis
    for step in range(1, c-1):
        ambient = span(hidden_line+bracket_span(ambient, ambient))
        derived = bracket_span(ambient, ambient)
        assert not bracket_span(derived, derived)
        assert len(lower_central(ambient, c))-1 == c-step
    assert len(lower_central(ambient, c))-1 == 2
