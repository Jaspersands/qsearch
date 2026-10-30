"""Exact weighted-square certificates in a totally positive unit algebra.

The certificate is sum weights[i]*polynomials[i]^2 = D^2*x mod f.
This is not a PPAV model, a quantum oracle, or a proof of novelty. Expansion
of each integer weight into four squares is a separate arithmetic step.
"""

from dataclasses import dataclass
from math import prod

from sympy import Matrix, Poly, QQ, Rational, ZZ, floor, isprime, nextprime, oo, symbols

X = symbols("x")


def vector(expression, f):
    p = Poly(expression, X, domain=QQ).rem(f)
    return Matrix([p.nth(i) for i in range(f.degree())])


def checked_polynomial(expression):
    f = Poly(expression, X, domain=ZZ)
    if f.degree() < 1 or f.LC() != 1 or abs(f.TC()) != 1:
        raise ValueError("monic integral unit polynomial required")
    if f.gcd(f.diff()).degree() != 0:
        raise ValueError("squarefree polynomial required")
    if f.count_roots(0, oo) != f.degree():
        raise ValueError("all roots must be real and strictly positive")
    return f


def uniform_bounds(degree, height):
    """Conservative explicit bounds, shared by every f in this height class."""
    d, height = int(degree), int(height)
    if d < 1 or height < 1:
        raise ValueError("positive degree and height required")
    r = 1+height
    # Root separation >= (2r)^(-d^2); Q controls dyadic root centers.
    inverse_eta = 96*d*d*r*r*(6*r*(2*r)**(d*d))**d
    q = 1 << int(inverse_eta).bit_length()
    epsilon_denominator = 8*d*r**(2*d+1)
    polynomial_bound = (3*r*q)**(d*d-1)
    column_bound = max(4, 4*d*d*polynomial_bound**2*(d*r)**(2*d))
    rounding_bound = 4*(3*d-1)*column_bound
    threshold = (rounding_bound+8)*epsilon_denominator
    return {"degree": d, "height": height, "root_denominator": q,
            "epsilon_denominator": epsilon_denominator,
            "column_bound": column_bound, "rounding_bound": rounding_bound,
            "denominator_threshold": threshold}


def shared_denominator(bounds, forbidden=()):
    forbidden = set(forbidden)
    if 2 in forbidden:
        raise ValueError("the construction requires an even denominator")
    d, primes, p = 1, [], 2
    while d <= bounds["denominator_threshold"]:
        if p not in forbidden:
            d *= p
            primes.append(int(p))
        p = int(nextprime(p))
    return d, tuple(primes)


@dataclass
class SmoothSOS:
    polynomial: Poly
    denominator: int
    primes: tuple
    polynomials: tuple
    weights: tuple
    bounds: dict

    def verify(self):
        if len(self.weights) != len(self.polynomials):
            return False
        if any(not isinstance(w, int) or w < 0 for w in self.weights):
            return False
        if self.denominator != prod(self.primes) or len(set(self.primes)) != len(self.primes):
            return False
        if self.denominator % 2 or any(not isprime(p) for p in self.primes):
            return False
        lhs = sum((w*p*p for w, p in zip(self.weights, self.polynomials)), 0)
        return vector(lhs-self.denominator**2*X, self.polynomial) == Matrix.zeros(self.polynomial.degree(), 1)


def certify(expression, *, degree_bound=None, height_bound=None, forbidden=(), denominator=None):
    f = checked_polynomial(expression)
    n = f.degree()
    degree = n if degree_bound is None else int(degree_bound)
    height = max(abs(int(c)) for c in f.all_coeffs()) if height_bound is None else int(height_bound)
    if degree < n or height < max(abs(int(c)) for c in f.all_coeffs()):
        raise ValueError("uniform bounds do not cover the polynomial")
    bounds = uniform_bounds(degree, height)
    if denominator is None:
        d, primes = shared_denominator(bounds, forbidden)
    else:
        d, primes = denominator
        if d != prod(primes) or len(set(primes)) != len(primes) or d % 2 or any(not isprime(p) for p in primes):
            raise ValueError("squarefree even denominator required")
        if d <= bounds["denominator_threshold"] or set(primes) & set(forbidden):
            raise ValueError("denominator violates uniform bound or excluded primes")
    q = bounds["root_denominator"]
    intervals = f.intervals(eps=Rational(1, 4*q))
    centers = [int(floor(q*(a+b)/2+Rational(1, 2))) for (a, b), multiplicity in intervals]
    if len(centers) != n or len(set(centers)) != n:
        raise AssertionError("root isolation did not separate all roots")
    denominators = [prod(centers[i]-centers[j] for j in range(n) if j != i) for i in range(n)]
    common = prod(abs(value) for value in denominators)
    spectral = [Poly((common//denominators[i])*prod(q*X-centers[j] for j in range(n) if j != i), X, domain=ZZ).as_expr()
                for i in range(n)]
    fixed = [1]+[p for j in range(1, n) for p in (1+X**j, 1-X**j)]
    polynomials = tuple(fixed+spectral)
    a = Matrix.hstack(*(vector(p*p, f) for p in polynomials))
    epsilon = Rational(1, bounds["epsilon_denominator"])
    target = vector(X, f)
    fixed_sum = sum((a[:, i] for i in range(len(fixed))), Matrix.zeros(n, 1))
    spectral_weights = a[:, len(fixed):].inv()*(target-epsilon*fixed_sum)
    weights = [epsilon]*len(fixed)+list(spectral_weights)
    if any(w <= 0 for w in weights):
        raise AssertionError("positive-cone construction failed")
    if max(abs(v) for v in a) > bounds["column_bound"]:
        raise AssertionError("uniform column bound failed")
    integer_weights = [4*int(floor(d*d*w/4)) for w in weights]
    residual = d*d*target-a*Matrix(integer_weights)
    if any(v.q != 1 or v % 4 for v in residual):
        raise AssertionError("rounding residual is not in 4 Z[x]/f")
    integer_weights[0] += int(residual[0])
    for j in range(1, n):
        correction = int(residual[j])//4
        integer_weights[2*j-1] += correction
        integer_weights[2*j] -= correction
    result = SmoothSOS(f, int(d), tuple(primes), polynomials,
                       tuple(integer_weights), bounds)
    if not result.verify():
        raise AssertionError("nonnegative integral square certificate failed")
    return result
