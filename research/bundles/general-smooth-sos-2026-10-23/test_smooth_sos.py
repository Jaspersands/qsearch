from dataclasses import replace
from pathlib import Path
import sys

import pytest
from sympy import Matrix, Poly, eye

from smooth_sos import X, certify, shared_denominator, uniform_bounds, vector

sys.path.insert(0, str(Path(__file__).resolve().parent.parent/"kernel-output-2026-10-23"))
from kernel_output import matrix_multiply, matrix_star, odd_maximal_order


@pytest.mark.parametrize("f", [X-1, X**2-3*X+1, X**2-7*X+1,
                               X**3-6*X**2+5*X-1,
                               (X-1)*(X**2-3*X+1)])
def test_exact_smooth_square_certificates(f):
    result = certify(f, forbidden=(11, 13))
    assert result.verify()
    assert result.denominator % 2 == 0
    assert not set(result.primes) & {11, 13}
    assert len(result.polynomials) == 3*Poly(f, X).degree()-1
    assert all(weight >= 0 for weight in result.weights)
    assert max(result.primes) < result.denominator.bit_length()*4


def test_uniform_denominator_for_different_degrees_and_heights():
    bounds = uniform_bounds(3, 7)
    denominator = shared_denominator(bounds, (11, 13))
    cases = [certify(f, degree_bound=3, height_bound=7, forbidden=(11, 13), denominator=denominator)
             for f in (X-1, X**2-3*X+1, X**2-7*X+1, X**3-6*X**2+5*X-1)]
    assert len({r.denominator for r in cases}) == 1
    assert all(r.verify() for r in cases)


def test_matrix_evaluation_of_cubic_certificate():
    # S=sigma^t sigma is a positive symmetric integral unit of degree 3.
    sigma = Matrix([[1, 1, 0], [0, 1, 1], [0, 0, 1]])
    s = sigma.T*sigma
    f = s.charpoly(X).as_expr()
    result = certify(f)
    def evaluate(p):
        polynomial = Poly(p, X)
        return sum((polynomial.nth(i)*s**i for i in range(polynomial.degree()+1)), Matrix.zeros(3))
    lhs = sum((w*evaluate(p)**2 for w, p in zip(result.weights, result.polynomials)), Matrix.zeros(3))
    assert lhs == result.denominator**2*s


def test_tampered_certificate_rejected():
    result = certify(X**2-3*X+1)
    assert not replace(result, weights=(result.weights[0]+1,)+result.weights[1:]).verify()
    assert not replace(result, weights=(-1,)+result.weights[1:]).verify()
    assert not replace(result, primes=(2, result.denominator//2)).verify()


@pytest.mark.parametrize("n", [2, 3, 4])
@pytest.mark.parametrize("shear", [1, 2, 4])
def test_integral_positive_unit_family(n, shear):
    sigma = eye(n)
    for i in range(n-1):
        sigma[i, i+1] = shear
    f = (sigma.T*sigma).charpoly(X).as_expr()
    assert certify(f).verify()


@pytest.mark.parametrize("f", [X**2+1, X**2-1, (X-1)**2, 2*X-1, X**2-3*X+2])
def test_input_promises_enforced(f):
    with pytest.raises(ValueError):
        certify(f)


def test_uniform_contract_rejected_if_undercharged():
    with pytest.raises(ValueError, match="cover"):
        certify(X**2-7*X+1, height_bound=3)
    with pytest.raises(ValueError, match="even"):
        certify(X-1, forbidden=(2,))
    with pytest.raises(ValueError, match="bound"):
        certify(X**2-3*X+1, denominator=(6, (2, 3)))


def test_noncommuting_quaternionic_source_unit():
    order, g, ell = odd_maximal_order(11), 3, 3
    identity = Matrix.vstack(*(order.unit if i == j else Matrix.zeros(4, 1)
                               for i in range(g) for j in range(g)))
    sigma = identity.copy()
    sigma[4:8, :] = ell*eye(4)[:, 1]
    sigma[20:24, :] = ell*eye(4)[:, 2]
    n = sigma-identity
    inverse = identity-n+matrix_multiply(order, n, n, g)
    assert matrix_multiply(order, sigma, inverse, g) == identity
    assert order.multiply(eye(4)[:, 1], eye(4)[:, 2]) != order.multiply(eye(4)[:, 2], eye(4)[:, 1])
    s = matrix_multiply(order, matrix_star(order, sigma, g), sigma, g)
    assert all(int(x) % ell == 0 for x in s-identity)
    powers = [identity]
    for _ in range(g):
        powers.append(matrix_multiply(order, powers[-1], s, g))
    relation = Matrix.hstack(*powers).nullspace()
    assert len(relation) == 1 and relation[0][-1] != 0
    coefficients = relation[0]/relation[0][-1]
    f = sum(coefficients[i]*X**i for i in range(g+1))
    certificate = certify(f)
    def evaluate(p):
        coefficients = vector(p, certificate.polynomial)
        return sum((coefficients[i]*powers[i] for i in range(g)), Matrix.zeros(4*g*g, 1))
    lhs = sum((w*matrix_multiply(order, evaluate(p), evaluate(p), g)
               for w, p in zip(certificate.weights, certificate.polynomials)), Matrix.zeros(4*g*g, 1))
    assert lhs == certificate.denominator**2*s
