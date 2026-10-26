"""Exact control algebra for a provisional nonabelian polynomial-jet lift.

This is NOT an executed quantum receiver. Hidden potentials occur only in
explicitly named fixtures. Public operations use a filtered Lie tensor and
observed evaluation points, not a hidden subgroup or potential evaluator.
See research/NONABELIAN_JET_HOMOGENIZATION.md for the unproved composition.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
from functools import cached_property, lru_cache
from itertools import combinations, product
import json
from math import comb, prod
from pathlib import Path

from theorems.affine_phase_erasure import monomials
from theorems.ambient_section_potential import (
    _add, _exponential, _multiply, _nested_expansion,
)
from theorems.full_jet_resource_certificate import sde_arity
from theorems.prime_character_opi import ring
from theorems.symbolic_scalar_phase_erasure import PublicLieAlgebra, _fmpz_solve_coordinates
from theorems.ut5_matrix_phase_alignment import _canonical, _identity, _lists, _matrix, _rank


@lru_cache(maxsize=None)
def bch_certificate(degree):
    """Universal rational BCH, checked against every associative coefficient."""
    if type(degree) is not int or degree < 1:
        raise ValueError("positive BCH class bound required")
    expanded = _multiply(_exponential({(0,): Fraction(1)}, degree),
                         _exponential({(1,): Fraction(1)}, degree), degree)
    expanded.pop(())
    logarithm, power = {}, {(): Fraction(1)}
    for k in range(1, degree+1):
        power = _multiply(power, expanded, degree)
        _add(logarithm, power, Fraction((-1)**(k+1), k))
    terms = tuple((word, coefficient/len(word)) for word, coefficient in sorted(logarithm.items())
                  if _nested_expansion(word))
    check = {}
    for word, coefficient in terms:
        _add(check, dict(_nested_expansion(word)), coefficient)
    if check != logarithm:
        raise ArithmeticError("universal BCH Lie expansion failed")
    return terms


@dataclass(frozen=True)
class PolynomialJetGroup:
    """Filtered normal Lie algebra with polynomial coefficients in (u,t).

    Basis coordinate i has total polynomial degree at most weights[i].
    The jet ideal is the subspace divisible by t. The constructor checks
    the tabulated tensor's Jacobi and filtration identities. It does NOT
    certify that these weights arise from a supplied ambient HSP instance.
    """
    algebra: object
    weights: tuple[int, ...]
    quotient_width: int
    class_bound: int

    def __post_init__(self):
        ring(self.p)
        if (type(self.class_bound) is not int or self.class_bound < 2
                or self.p <= self.class_bound
                or type(self.quotient_width) is not int or self.quotient_width < 1
                or len(self.weights) != self.algebra.dimension
                or any(type(w) is not int or not 2 <= w <= self.class_bound for w in self.weights)):
            raise ValueError("positive quotient, actual normal weights 2..c and prime p>c required")
        tensor = self.tensor
        for i in range(self.algebra.dimension):
            if tensor.get((i, i)):
                raise ValueError("alternating Lie tensor required")
        for (i, j), value in tensor.items():
            opposite = dict(tensor.get((j, i), ()))
            if any((a+opposite.get(k, 0)) % self.p for k, a in value):
                raise ValueError("alternating Lie tensor required")
            if any(self.weights[k] < self.weights[i]+self.weights[j] for k, _ in value):
                raise ValueError("bracket violates coordinate filtration")
        for i, j, k in combinations(range(self.algebra.dimension), 3):
            jacobi = {}
            for a, b, c in ((i, j, k), (j, k, i), (k, i, j)):
                for v, x in tensor.get((b, c), ()):
                    for w, y in tensor.get((a, v), ()):
                        jacobi[w] = (jacobi.get(w, 0)+x*y) % self.p
            if any(jacobi.values()):
                raise ValueError("Jacobi identity failed")

    @property
    def p(self):
        return self.algebra.p

    @cached_property
    def tensor(self):
        basis = _identity(self.algebra.dimension)
        return {(i, j): tuple((k, a) for k, a in enumerate(value) if a)
                for i, x in enumerate(basis) for j, y in enumerate(basis)
                if any(value := self.algebra.bracket(x, y))}

    @cached_property
    def indices(self):
        return tuple((i, alpha, d) for i, w in enumerate(self.weights)
                     for d in range(1, w+1) for alpha in monomials(self.quotient_width, w-d))

    @property
    def dimension(self):
        return sum(comb(self.quotient_width+w, self.quotient_width+1) for w in self.weights)

    def validate(self, polynomial, *, jet=False):
        for (i, alpha, d), value in polynomial.items():
            if (type(i) is not int or not 0 <= i < len(self.weights)
                    or len(alpha) != self.quotient_width
                    or any(type(a) is not int or a < 0 for a in alpha)
                    or type(d) is not int or d < int(jet)
                    or sum(alpha)+d > self.weights[i]
                    or type(value) is not int or not 0 < value < self.p):
                raise ValueError("canonical filtered polynomial support required")
        return polynomial

    def add(self, *polynomials):
        result = {}
        for polynomial in polynomials:
            self.validate(polynomial)
            for key, value in polynomial.items():
                result[key] = (result.get(key, 0)+value) % self.p
        return {key: value for key, value in result.items() if value}

    def scale(self, polynomial, scalar):
        self.validate(polynomial)
        return {key: value*scalar % self.p for key, value in polynomial.items() if value*scalar % self.p}

    def bracket(self, left, right):
        self.validate(left)
        self.validate(right)
        result = {}
        for (i, alpha, d), a in left.items():
            for (j, beta, e), b in right.items():
                for k, c in self.tensor.get((i, j), ()):
                    key = k, tuple(x+y for x, y in zip(alpha, beta)), d+e
                    result[key] = (result.get(key, 0)+a*b*c) % self.p
        result = {key: value for key, value in result.items() if value}
        return self.validate(result)  # Never silently truncate an invalid bracket.

    def multiply(self, left, right):
        """BCH group multiplication in logarithmic polynomial coordinates."""
        self.validate(left)
        self.validate(right)
        values = left, right
        @lru_cache(maxsize=None)
        def nested(word):
            return values[word[0]] if len(word) == 1 else self.bracket(values[word[0]], nested(word[1:]))
        result = {}
        for word, coefficient in bch_certificate(self.class_bound // min(self.weights)):
            c = coefficient.numerator*pow(coefficient.denominator, -1, self.p) % self.p
            result = self.add(result, self.scale(nested(word), c))
        return result

    def substitute(self, polynomial, y, scale=1):
        """Public pullback R(u,t) -> R(u+t*y, scale*t)."""
        self.validate(polynomial)
        _canonical(y, self.quotient_width, self.p)
        if type(scale) is not int or not 0 < scale < self.p:
            raise ValueError("nonzero canonical scale required")
        result = {}
        for (i, alpha, d), a in polynomial.items():
            for beta in product(*(range(x+1) for x in alpha)):
                coefficient = a*pow(scale, d, self.p)*prod(
                    comb(x, b)*pow(v, b, self.p) for x, b, v in zip(alpha, beta, y)) % self.p
                key = i, tuple(x-b for x, b in zip(alpha, beta)), d+sum(beta)
                result[key] = (result.get(key, 0)+coefficient) % self.p
        return self.validate({key: value for key, value in result.items() if value})

    def evaluate(self, polynomial, u, t):
        self.validate(polynomial)
        _canonical(u, self.quotient_width, self.p)
        _canonical((t,), 1, self.p)
        result = [0]*len(self.weights)
        for (i, alpha, d), a in polynomial.items():
            result[i] += a*pow(t, d, self.p)*prod(pow(v, e, self.p) for v, e in zip(u, alpha))
        return tuple(v % self.p for v in result)

    def normal_multiply(self, x, y):
        _canonical(x, len(self.weights), self.p)
        _canonical(y, len(self.weights), self.p)
        zero = (0,)*self.quotient_width
        polynomial = lambda v: {(i, zero, 0): a for i, a in enumerate(v) if a}
        return self.evaluate(self.multiply(polynomial(x), polynomial(y)), zero, 0)

    def semidirect_multiply(self, left, right):
        x, q = left
        y, r = right
        self.validate(x, jet=True)
        self.validate(y, jet=True)
        _canonical(q, self.quotient_width, self.p)
        _canonical(r, self.quotient_width, self.p)
        return self.multiply(x, self.substitute(y, q)), tuple((a+b) % self.p for a, b in zip(q, r))

    def dilate(self, element, scale):
        x, q = element
        self.validate(x, jet=True)
        _canonical(q, self.quotient_width, self.p)
        return (self.substitute(x, (0,)*self.quotient_width, scale),
                tuple(scale*a % self.p for a in q))

    def normalized_curve_fixture(self, potential, q):
        """Secret-bearing proof fixture F(q)=P(u)^-1 P(u+tq), NOT a receiver."""
        self.validate(potential)
        if any(d for _, _, d in potential):
            raise ValueError("proof potential must be independent of t")
        result = self.multiply(self.scale(potential, -1), self.substitute(potential, q))
        return self.validate(result, jet=True)


@dataclass(frozen=True)
class AmbientJetCertificate:
    group: PolynomialJetGroup
    ambient_basis: tuple
    normal_basis: tuple
    section_basis: tuple

    def verify(self, algebra):
        g = self.group
        if algebra.p != g.p:
            raise ValueError("field mismatch")
        ambient = algebra.span(self.ambient_basis)
        series = algebra.lower_central_series(ambient)
        if len(ambient) != len(self.ambient_basis) or len(series)-1 != g.class_bound:
            raise ValueError("ambient basis or class mismatch")
        if len(algebra.span(ambient+series[1])) != len(ambient):
            raise ValueError("ambient space is not bracket closed")
        if (len(self.normal_basis) != len(g.weights)
                or len(self.section_basis) != g.quotient_width
                or len(self.normal_basis)+len(self.section_basis) != len(ambient)
                or len(algebra.span(list(self.normal_basis+self.section_basis))) != len(ambient)
                or len(algebra.span(ambient+list(self.normal_basis+self.section_basis))) != len(ambient)):
            raise ValueError("normal/quotient decomposition mismatch")
        for w in range(2, g.class_bound+1):
            chosen = [v for v, weight in zip(self.normal_basis, g.weights) if weight >= w]
            if len(chosen) != len(series[w-1]) or len(algebra.span(chosen+series[w-1])) != len(chosen):
                raise ValueError("basis does not split actual ambient filtration")
        for i, x in enumerate(self.normal_basis):
            for j, y in enumerate(self.normal_basis):
                actual = _fmpz_solve_coordinates(self.normal_basis, algebra.bracket(x, y), g.p)
                expected = dict(g.tensor.get((i, j), ()))
                if actual != tuple(expected.get(k, 0) for k in range(len(g.weights))):
                    raise ValueError("normal tensor mismatch")
        return True


def ambient_jet_certificate(algebra, ambient_basis):
    """Adapt to the actual lower-central flag without an N''=0 promise."""
    ambient = algebra.span(ambient_basis)
    series = algebra.lower_central_series(ambient)
    c = len(series)-1
    if c < 2 or algebra.p <= c:
        raise ValueError("nonabelian ambient and p>c required; use abelian solver otherwise")
    normal, weights = [], []
    for w in range(c, 1, -1):
        extended = algebra.span(normal+series[w-1])
        weights.extend([w]*(len(extended)-len(normal)))
        normal = extended
    full = algebra.span(normal+ambient)
    section = full[len(normal):]
    tensor = tuple(tuple(_fmpz_solve_coordinates(normal, algebra.bracket(x, y), algebra.p)
                         for y in normal) for x in normal)
    def bracket(x, y):
        return tuple(sum(a*b*tensor[i][j][k] for i, a in enumerate(x) for j, b in enumerate(y)) % algebra.p
                     for k in range(len(normal)))
    group = PolynomialJetGroup(PublicLieAlgebra(algebra.p, len(normal), bracket),
                               tuple(weights), len(section), c)
    certificate = AmbientJetCertificate(group, tuple(ambient), tuple(normal), tuple(section))
    certificate.verify(algebra)
    return certificate


class FilteredEvaluation:
    """Public subgroup embedding E and a filtered, nonnormal coset chart.

    Coordinates are logarithms. A carrier is a tuple of B normal vectors.
    Factorization returns (j,k) such that x=E(j)*exp(k). The spectator k
    lies in a component-separated linear complement, not a subgroup.
    """
    def __init__(self, group, points):
        self.group, self.points = group, tuple(points)
        if not self.points:
            raise ValueError("nonempty evaluation batch required")
        for y, s in self.points:
            _canonical(y, group.quotient_width, group.p)
            if type(s) is not int or not 0 < s < group.p:
                raise ValueError("evaluation scales must be nonzero")
        self.blocks = []
        for i in range(len(group.weights)):
            indices = [key for key in group.indices if key[0] == i]
            columns = [tuple(pow(s, d, group.p)*prod(pow(v, e, group.p) for v, e in zip(y, alpha)) % group.p
                             for y, s in self.points) for _, alpha, d in indices]
            if _rank(columns, group.p) != len(columns):
                raise ValueError("evaluation design is not injective")
            complement = []
            for unit in _identity(len(self.points)):
                if _rank(columns+complement+[unit], group.p) > len(columns)+len(complement):
                    complement.append(unit)
            matrix = _matrix(list(zip(*(columns+complement))), group.p)
            self.blocks.append((indices, complement, _lists(matrix.inv())))

    @property
    def spectator_dimension(self):
        return len(self.points)*len(self.group.weights)-self.group.dimension

    def embed(self, polynomial):
        self.group.validate(polynomial, jet=True)
        return tuple(self.group.evaluate(polynomial, y, s) for y, s in self.points)

    def _validate_carrier(self, carrier):
        if len(carrier) != len(self.points):
            raise ValueError("one normal register per evaluation point required")
        for row in carrier:
            _canonical(row, len(self.group.weights), self.group.p)

    def multiply(self, left, right):
        self._validate_carrier(left)
        self._validate_carrier(right)
        return tuple(self.group.normal_multiply(x, y) for x, y in zip(left, right))

    def split_linear(self, carrier):
        self._validate_carrier(carrier)
        polynomial, spectator = {}, [[0]*len(self.group.weights) for _ in self.points]
        for i, (indices, complement, inverse) in enumerate(self.blocks):
            coefficients = [sum(a*x[i] for a, x in zip(row, carrier)) % self.group.p for row in inverse]
            polynomial.update((key, a) for key, a in zip(indices, coefficients) if a)
            for a, column in zip(coefficients[len(indices):], complement):
                for b, value in enumerate(column):
                    spectator[b][i] = (spectator[b][i]+a*value) % self.group.p
        return polynomial, tuple(map(tuple, spectator))

    def factor(self, carrier):
        """Triangular BCH inversion; at most c corrections, no enumeration."""
        self._validate_carrier(carrier)
        z = tuple(map(tuple, carrier))
        for _ in range(self.group.class_bound+1):
            polynomial, spectator = self.split_linear(z)
            reconstructed = self.multiply(self.embed(polynomial), spectator)
            if reconstructed == tuple(map(tuple, carrier)):
                return polynomial, spectator
            z = tuple(tuple((x-a+b) % self.group.p for x, a, b in zip(row, actual, old))
                      for row, actual, old in zip(carrier, reconstructed, z))
        raise ArithmeticError("filtered BCH factorization did not converge")


def resource_profile(weights, quotient_width, p):
    """Conditional single-image budget; no synthesis/SDE runtime claim."""
    ring(p)
    if (not weights or any(type(w) is not int or w < 2 for w in weights)
            or type(quotient_width) is not int or quotient_width < 1 or p <= 2*max(weights)):
        raise ValueError("positive normal weights, quotient and p>2c required")
    c, m = max(weights), quotient_width
    grades = {d: sum(comb(m+w-d, m) for w in weights if w >= d) for d in range(1, c+1)}
    features = comb(m+c, m+1)
    batch = (features+1)*p.bit_length()+2
    stages = [(d, grades[d], sde_arity(d, grades[d])) for d in range(c, 1, -1) if grades[d]]
    leaves = prod(arity for _, _, arity in stages)
    # Oversampling by bit_length(p)+2 gives abelian rank failure <1/(4p).
    samples = m+grades[1]+p.bit_length()+2
    aligned_sources = leaves*samples
    # Public full-rank failures <=1/(4p); logarithmically many fresh retries
    # per leaf bound the union of all aborts by <1/(4p).
    retries = (aligned_sources*4*p).bit_length()
    queries = aligned_sources*retries*batch
    return {"class_bound": c, "quotient_width": m, "p": p,
            "normal_dimension": len(weights), "jet_dimension": sum(grades.values()),
            "semidirect_dimension": m+sum(grades.values()), "grade_dimensions": grades,
            "scalar_features": features, "batch_sources": batch,
            "stages": [{"degree": d, "equations": r, "arity_ceil_log2": (a-1).bit_length()}
                       for d, r, a in stages],
            "abelian_samples": samples, "alignment_retries_per_leaf": retries,
            "original_queries_ceil_log2": (queries-1).bit_length(),
            "interpretation": "sufficient conditional upper bound for one transverse image call",
            "receiver_executed": False, "general_sde_implemented": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    weights = (6, 5, 4, 4, 3, 3, 2, 9, 8, 8, 7, 7, 7, 6, 6, 5, 5)
    report = {"schema": "nonabelian_jet_homogenization_v1",
              "status": "provisional written reduction with exact algebraic controls",
              "profiles": [resource_profile(weights, 2, p) for p in (43, 2**127-1)],
              "not_established": ["end-to-end physical receiver", "independent proof review", "novelty",
                                  "hard external application", "arbitrary-H recursion refinement"],
              "hidden_evaluator_available": False, "requires_metabelian_normal": False}
    if args.write:
        path = Path(__file__).resolve().parents[1]/"research/reductions/nonabelian_jet_homogenization.json"
        path.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
