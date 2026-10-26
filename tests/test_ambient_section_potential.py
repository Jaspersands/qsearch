"""Universal coefficients and input-origin falsifiers, not HSP benchmarks."""
from dataclasses import replace
from fractions import Fraction
from math import factorial
import random

import pytest

from theorems.ambient_section_potential import (
    evaluate_section_fixture, polynomial_section_fixture, section_word_certificate,
)
from theorems.class_three_ambient_frontend import (
    certify_ambient_class_three_derived, compute_subalgebra_center, make_ut7_ambient_algebra,
)
from theorems.symbolic_scalar_phase_erasure import PublicLieAlgebra, _fmpz_solve_coordinates


def _ut(n, p):
    slots = tuple((i, j) for i in range(n) for j in range(i+1, n))
    def matrix(v):
        result = [[0]*n for _ in range(n)]
        for (i, j), value in zip(slots, v):
            result[i][j] = value
        return result
    def bracket(a, b):
        A, B = matrix(a), matrix(b)
        return tuple(sum(A[i][k]*B[k][j]-B[i][k]*A[k][j] for k in range(n)) % p
                     for i, j in slots)
    return PublicLieAlgebra(p, len(slots), bracket), slots, matrix


def _matrix_multiply(A, B, p):
    n = len(A)
    return [[sum(A[i][k]*B[k][j] for k in range(n)) % p for j in range(n)] for i in range(n)]


def _matrix_exp(A, p):
    n = len(A)
    power = [[int(i == j) for j in range(n)] for i in range(n)]
    result = [row[:] for row in power]
    for k in range(1, n):
        power = _matrix_multiply(power, A, p)
        scale = pow(factorial(k), -1, p)
        result = [[(a+scale*b) % p for a, b in zip(row, other)]
                  for row, other in zip(result, power)]
    return result


def _matrix_log(U, p):
    n = len(U)
    A = [[(U[i][j]-int(i == j)) % p for j in range(n)] for i in range(n)]
    power = [[int(i == j) for j in range(n)] for i in range(n)]
    result = [[0]*n for _ in range(n)]
    for k in range(1, n):
        power = _matrix_multiply(power, A, p)
        scale = (-1)**(k+1)*pow(k, -1, p)
        result = [[(a+scale*b) % p for a, b in zip(row, other)]
                  for row, other in zip(result, power)]
    return result


@pytest.mark.parametrize("c", range(1, 8))
def test_universal_right_nested_coefficients_equal_actual_section_log(c):
    cert = section_word_certificate(c)
    cert.verify()
    assert all(isinstance(value, Fraction) for _, value in cert.lie_terms)
    assert {w: v for w, v in cert.associative_terms if len(w) == 1} == {(2,): Fraction(1)}
    with pytest.raises(ValueError, match="Lazard"):
        cert.field_terms(c)
    for p in (17, 2**127-1):
        assert all(0 <= value < p for _, value in cert.field_terms(p))


def test_mutated_universal_certificates_are_rejected():
    cert = section_word_certificate(5)
    mutated = list(cert.lie_terms)
    word, coefficient = mutated[-1]
    mutated[-1] = (word, coefficient+1)
    with pytest.raises(ValueError, match="every associative coefficient"):
        replace(cert, lie_terms=tuple(mutated)).verify()
    with pytest.raises(ValueError, match="actual section-word"):
        replace(cert, associative_terms=(((2,), Fraction(2)),)).verify()
    with pytest.raises(ValueError, match="distinct"):
        replace(cert, lie_terms=cert.lie_terms+cert.lie_terms[:1]).verify()
    with pytest.raises(ValueError):
        cert.field_terms(21)


@pytest.mark.parametrize("n,p", [(5, 17), (6, 17), (7, 19), (8, 23), (8, 2**127-1)])
def test_lie_certificate_agrees_with_independent_matrix_exp_log(n, p):
    algebra, slots, matrix = _ut(n, p)
    cert, rng = section_word_certificate(n-1), random.Random(831+n)
    for _ in range(8):
        x, y = (tuple(rng.randrange(p) for _ in slots) for _ in range(2))
        z = tuple(rng.randrange(p) if j-i >= 2 else 0 for i, j in slots)
        actual = evaluate_section_fixture(cert, algebra, x, y, z)
        yz = tuple((a+b) % p for a, b in zip(y, z))
        minus_xy = tuple((-a-b) % p for a, b in zip(x, y))
        G = _matrix_multiply(_matrix_multiply(_matrix_exp(matrix(x), p),
                             _matrix_exp(matrix(yz), p), p), _matrix_exp(matrix(minus_xy), p), p)
        assert matrix(actual) == _matrix_log(G, p)
        assert all(value == 0 for (i, j), value in zip(slots, actual) if j-i == 1)


def _section_example(p):
    algebra, basis, slots = make_ut7_ambient_algebra(p)
    X = tuple(int(j == i+1 and i >= 1) for i, j in slots)
    Y = tuple(int((i, j) == (0, 1)) for i, j in slots)
    zero = (0,)*len(slots)
    # pi(q0,q1)=(0,q1), s=q0*X+q1*Y, hidden H=exp(<Y>).
    # Z=0 is an actual transverse rank-one subgroup, not hidden advice
    # in a controller. Only this diagnostic is supplied the witnesses.
    inputs = ((X, zero), (zero, Y), (zero, zero))
    polynomial = polynomial_section_fixture(section_word_certificate(6), algebra, inputs)
    return algebra, basis, slots, inputs, polynomial


@pytest.mark.parametrize("p", [19, 2**127-1])
def test_actual_potential_coefficients_obey_filtration_and_full_center_degree(p):
    algebra, basis, slots, inputs, polynomial = _section_example(p)
    frontend = certify_ambient_class_three_derived(algebra, basis)
    series = algebra.lower_central_series(basis)
    adapted = frontend.a_basis+frontend.b_basis+frontend.c_basis
    projected_degrees, central_degrees = [], []
    for alpha, coefficient in polynomial.items():
        degree = sum(alpha)
        assert _fmpz_solve_coordinates(series[degree-1], coefficient, p) is not None
        coordinates = _fmpz_solve_coordinates(adapted, coefficient, p)
        assert coordinates is not None
        split = len(frontend.a_basis)+len(frontend.b_basis)
        if any(coordinates[:split]):
            projected_degrees.append(degree)
        if any(coordinates[split:]):
            central_degrees.append(degree)
        if degree >= frontend.ambient_class-1:
            assert all(not any(algebra.bracket(coefficient, v)) for v in series[1])
    assert max(projected_degrees) == frontend.jet_degree == 4
    assert max(central_degrees) == frontend.ambient_class == 6
    # Independent evaluation at points tests the coefficient expansion bridge.
    for q in [(0, 0), (1, 2), (3, 4), (p-1, p-2)]:
        actual = tuple(sum(vector[i]*pow(q[0], alpha[0], p)*pow(q[1], alpha[1], p)
                           for alpha, vector in polynomial.items()) % p for i in range(len(slots)))
        values = [tuple(sum(q[j]*rows[j][i] for j in range(2)) % p for i in range(len(slots)))
                  for rows in inputs]
        assert actual == evaluate_section_fixture(section_word_certificate(6), algebra, *values)


def test_ambient_center_is_too_small_and_nonlinear_witnesses_break_the_bound():
    p = 19
    algebra, basis, slots, _inputs, polynomial = _section_example(p)
    coefficient = polynomial[(4, 1)]
    assert coefficient[slots.index((0, 5))] == pow(30, -1, p)
    ambient_center = compute_subalgebra_center(algebra, basis)
    assert _fmpz_solve_coordinates(ambient_center, coefficient, p) is None
    with pytest.raises(ValueError, match="proper subspace"):
        certify_ambient_class_three_derived(algebra, basis, proposed_c_basis=ambient_center)
    # Before projection, degree five really survives mod Z(L). Choosing
    # Z(L) instead of Z([L,L]) would falsify the advertised D=4 bound.
    assert sum((4, 1)) > 4
    # A nonlinear proof input q0->q0^2 turns the noncentral degree-four
    # coefficient (3,1) into degree seven. Linear sections/projections matter.
    noncentral = polynomial[(3, 1)]
    derived = algebra.lower_central_series(basis)[1]
    assert any(any(algebra.bracket(noncentral, v)) for v in derived)
    assert 2*3+1 > 4


def test_valid_truncated_certificate_does_not_certify_input_nilpotency_class():
    p = 23
    algebra, slots, matrix = _ut(8, p)
    x = tuple(int(j == i+1 and i >= 1) for i, j in slots)
    y = tuple(int((i, j) == (0, 1)) for i, j in slots)
    z = (0,)*len(slots)
    full = evaluate_section_fixture(section_word_certificate(7), algebra, x, y, z)
    truncated = evaluate_section_fixture(section_word_certificate(6), algebra, x, y, z)
    assert full != truncated
    assert full[slots.index((0, 7))] != 0 == truncated[slots.index((0, 7))]
    minus_xy = tuple((-a-b) % p for a, b in zip(x, y))
    expected = _matrix_log(_matrix_multiply(_matrix_multiply(_matrix_exp(matrix(x), p),
                             _matrix_exp(matrix(y), p), p), _matrix_exp(matrix(minus_xy), p), p), p)
    assert matrix(full) == expected
