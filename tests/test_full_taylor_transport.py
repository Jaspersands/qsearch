"""Coefficient-level controls for the Lean full-jet model, not HSP evidence."""

from math import comb
import random

import pytest

from theorems.affine_phase_erasure import monomials
from theorems.class_three_monomial_jet import FullTaylorJetChart
from theorems.nonlinear_jet_erasure import _jet_terms, pullback_phase
from theorems.ut5_scalar_phase_compiler import SymbolicScalarPacket
from theorems.ut5_matrix_phase_alignment import _identity, _product


def _add(left, right, p, factor=1):
    result = dict(left)
    for exponent, value in right.items():
        result[exponent] = (result.get(exponent, 0) + factor*value) % p
    return {exponent: value for exponent, value in result.items() if value}


def _multiply(left, right, p):
    result = {}
    for a, u in left.items():
        for b, v in right.items():
            exponent = tuple(x+y for x, y in zip(a, b))
            result[exponent] = (result.get(exponent, 0)+u*v) % p
    return {exponent: value for exponent, value in result.items() if value}


def _substitute(polynomial, images, width, p):
    """Expand products directly; do not reuse chart binomial formulas."""
    result = {}
    for exponent, coefficient in polynomial.items():
        term = {(0,)*width: coefficient}
        for power, image in zip(exponent, images):
            for _ in range(power):
                term = _multiply(term, image, p)
        result = _add(result, term, p)
    return result


def _images(y, scale, p):
    m = len(y)
    s = (0,)*m+(1,)
    return [{tuple(int(i == j) for j in range(m))+(0,): 1, s: y[i]}
            for i in range(m)]+[{s: scale % p}]


def _jet(polynomial, q, p):
    m = len(q)
    shifted = _substitute(polynomial, _images(q, 1, p)[:m], m+1, p)
    base = {a+(0,): c for a, c in polynomial.items()}
    return _add(shifted, base, p, -1)


def _evaluate_public_coordinates(packet, point):
    """Leave every hidden-parameter monomial formal, including products."""
    result = {}
    for (alpha, parameters), coefficient in packet.terms.items():
        value = coefficient
        for x, power in zip(point, alpha):
            value = value*pow(x, power, packet.p) % packet.p
        result[parameters] = (result.get(parameters, 0)+value) % packet.p
    return {parameters: value for parameters, value in result.items() if value}


@pytest.mark.parametrize("p", [5, 2**127-1])
@pytest.mark.parametrize("degree", [2, 3])
def test_entire_symbolic_phase_matches_actual_coefficient_transport(p, degree, monkeypatch):
    chart, rng = FullTaylorJetChart(p, 2, 2, degree), random.Random(613+degree)
    terms = {}
    for parameters in [(), (0,), (1,), (0, 0), (0, 1), (1, 1)]:
        for _ in range(8):
            alpha = [0]*chart.width
            for i in rng.sample(range(chart.width), 3):
                alpha[i] += 1
            terms[(tuple(alpha), parameters)] = rng.randrange(1, p)
        terms[((0,)*chart.width, parameters)] = rng.randrange(1, p)
    packet = SymbolicScalarPacket(p, 2, chart.jet_width,
                                  ((0, (1, 0)), (1, (0, 1))), terms)
    def forbidden(*args):
        raise AssertionError("the bridge must not evaluate hidden coefficients")
    monkeypatch.setattr(SymbolicScalarPacket, "evaluate_fixture", forbidden)
    for _ in range(4):
        y, scale = tuple(rng.randrange(p) for _ in range(2)), rng.randrange(1, p)
        offset = tuple(rng.randrange(p) for _ in chart.indices)
        point = tuple(rng.randrange(p) for _ in range(chart.width))
        # Reconstruct an ARBITRARY register vector, not just one hidden jet.
        components = [{alpha+(k,): point[2+i] for i, (alpha, k, a) in enumerate(chart.indices)
                       if a == component} for component in range(2)]
        transformed = [_substitute(P, _images(y, scale, p), 3, p) for P in components]
        expected_point = tuple((a+scale*b) % p for a, b in zip(y, point[:2]))
        expected_point += tuple((offset[i]+transformed[a].get(alpha+(k,), 0)) % p
                                for i, (alpha, k, a) in enumerate(chart.indices))
        pulled = pullback_phase(chart, packet, y, offset, scale)
        assert _evaluate_public_coordinates(pulled, point) == \
            _evaluate_public_coordinates(packet, expected_point)


@pytest.mark.parametrize("p", [5, 11, 2**127-1])
@pytest.mark.parametrize("degree", [2, 3, 4])
def test_actual_matrix_equals_public_substitution_on_every_basis_vector(p, degree):
    chart = FullTaylorJetChart(p, 2, 2, degree)
    assert chart.jet_width == 2*comb(2+degree, 3)
    z, t = (2, p-1), 3
    matrix = chart.transport_matrix(z, t)
    for column, (alpha, k, component) in enumerate(chart.indices):
        source = {alpha+(k,): 1}
        expected = _substitute(source, _images(z, t, p), 3, p)
        assert all(a[-1] > 0 and sum(a) <= degree for a in expected)
        for row, (beta, j, output_component) in enumerate(chart.indices):
            coefficient = expected.get(beta+(j,), 0) if output_component == component else 0
            assert matrix[row][column] == coefficient


@pytest.mark.parametrize("p", [5, 11, 2**127-1])
@pytest.mark.parametrize("degree", [2, 3, 4])
def test_jet_coefficient_schema_and_transport_with_arbitrary_hidden_coefficients(p, degree):
    chart = FullTaylorJetChart(p, 2, 2, degree)
    rng = random.Random(902+degree)
    basis = tuple((a, nu) for a in range(2) for nu in monomials(2, degree))
    parameters = tuple(rng.randrange(p) for _ in basis)
    polynomials = [{nu: parameters[i] for i, (a, nu) in enumerate(basis) if a == component}
                   for component in range(2)]
    for _ in range(4):
        q, z = tuple(rng.randrange(p) for _ in range(2)), (2, 3)
        t = rng.randrange(1, p)
        jet = [_jet(P, q, p) for P in polynomials]
        at_z = [_jet(P, z, p) for P in polynomials]
        translated = [_jet(P, tuple((a+t*b) % p for a, b in zip(z, q)), p)
                      for P in polynomials]
        values = [jet[a].get(alpha+(k,), 0) for alpha, k, a in chart.indices]
        for i, (alpha, k, a) in enumerate(chart.indices):
            symbolic = _jet_terms(chart, basis, i, chart.width)
            expected = 0
            for (exponent, parameter), coefficient in symbolic.items():
                value = coefficient*parameters[parameter[0]]
                for x, power in zip(q, exponent[:2]):
                    value *= pow(x, power, p)
                expected = (expected+value) % p
            assert values[i] == expected
        for i, (alpha, k, a) in enumerate(chart.indices):
            transported = sum(c*v for c, v in zip(chart.transport_matrix(z, t)[i], values))
            assert translated[a].get(alpha+(k,), 0) == (at_z[a].get(alpha+(k,), 0)+transported) % p


@pytest.mark.parametrize("p", [5, 11, 2**127-1])
def test_public_composition_inverse_and_weight_triangularity(p):
    chart = FullTaylorJetChart(p, 2, 2, 4)
    z, w, t, u = (2, 1), (1, 3), 2, 3
    A, B = chart.transport_matrix(z, t), chart.transport_matrix(w, u)
    combined = chart.transport_matrix(tuple((a+t*b) % p for a, b in zip(z, w)), t*u % p)
    assert _product(A, B, p) == [list(row) for row in combined]
    inv_t = pow(t, -1, p)
    inverse = chart.transport_matrix(tuple(-inv_t*a % p for a in z), inv_t)
    assert _product(A, inverse, p) == _identity(chart.jet_width)
    assert _product(inverse, A, p) == _identity(chart.jet_width)
    for i, (_, k, _) in enumerate(chart.indices):
        assert A[i][i] == pow(t, k, p)
        for j, (_, ell, _) in enumerate(chart.indices):
            if ell >= k and i != j:
                assert A[i][j] == 0
    with pytest.raises(ValueError, match="nonzero scale"):
        chart.transport_matrix(z, 0)


def test_transpose_is_not_a_valid_substitute_for_the_public_transport():
    chart = FullTaylorJetChart(11, 2, 1, 3)
    matrix = chart.transport_matrix((2, 3), 4)
    assert matrix != tuple(zip(*matrix))
    # A top-s-degree input acquires no Y terms under substitution. A transpose
    # reverses this dependency and would silently change the physical channel.
    top = chart.indices.index(((0, 0), 3, 0))
    assert sum(bool(row[top]) for row in matrix) == 1
    assert sum(bool(value) for value in matrix[top]) > 1
