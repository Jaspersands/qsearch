"""Noncentral right-fiber Fourier source and a larger-scope Lie witness.

Known induced representations are used as a candidate source interface,
not claimed as new. This module does NOT execute an HSP receiver. The
filiform normal group is an exact diagnostic; its original-oracle tests
do not assert that it is the derived group of their direct-product ambient.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from math import factorial
from pathlib import Path

from theorems.ambient_section_potential import evaluate_section_fixture, section_word_certificate
from theorems.prime_character_opi import ring
from theorems.symbolic_scalar_phase_erasure import PublicLieAlgebra, _canonical_vec


@dataclass(frozen=True)
class FiliformNormal:
    """F_p acting on F_p^k by exp(aJ), J a nilpotent shift of length k.

    Elements (a,b_0,...,b_(k-1)) are SEMIDIRECT, not logarithmic coordinates.
    I=N'={a=b_0=0} is abelian and noncentral for k>=3. The right-fiber
    section is exp(aX+uY_0), so its logarithm is a public linear section.
    """
    p: int
    nilpotency_class: int

    def __post_init__(self):
        ring(self.p)
        if type(self.nilpotency_class) is not int or not 2 <= self.nilpotency_class < self.p:
            raise ValueError("requires 2<=k<p")

    @property
    def width(self):
        return self.nilpotency_class + 1

    def _convolve(self, coefficients, value):
        k, p = self.nilpotency_class, self.p
        return tuple(sum(coefficients[i]*value[j-i] for i in range(j+1)) % p for j in range(k))

    def action(self, a, value):
        coefficients = [pow(a, j, self.p)*pow(factorial(j), -1, self.p) % self.p
                        for j in range(self.nilpotency_class)]
        return self._convolve(coefficients, value)

    def exp(self, logarithm):
        _canonical_vec(logarithm, self.width, self.p)
        a, values = logarithm[0], logarithm[1:]
        coefficients = [pow(a, j, self.p)*pow(factorial(j+1), -1, self.p) % self.p
                        for j in range(self.nilpotency_class)]
        return (a,)+self._convolve(coefficients, values)

    def multiply(self, left, right):
        for element in (left, right):
            _canonical_vec(element, self.width, self.p)
        translated = self.action(left[0], right[1:])
        return ((left[0]+right[0]) % self.p,)+tuple(
            (a+b) % self.p for a, b in zip(left[1:], translated))

    def inverse(self, element):
        _canonical_vec(element, self.width, self.p)
        a = -element[0] % self.p
        return (a,)+self.action(a, tuple(-x % self.p for x in element[1:]))

    def section(self, point):
        _canonical_vec(point, 2, self.p)
        return self.exp(tuple(point)+(0,)*(self.nilpotency_class-1))

    def from_right_coordinates(self, point, fiber):
        _canonical_vec(fiber, self.nilpotency_class-1, self.p)
        return self.multiply(self.section(point), (0, 0)+tuple(fiber))

    def right_coordinates(self, element):
        _canonical_vec(element, self.width, self.p)
        point = element[:2]
        residual = self.multiply(self.inverse(self.section(point)), element)
        if any(residual[:2]):
            raise ArithmeticError("right section did not isolate the abelian ideal")
        return point, residual[2:]

    def left_coordinates(self, element):
        """Deliberate comparison: left-I coordinates do NOT freeze its Fourier label."""
        point = element[:2]
        residual = self.multiply(element, self.inverse(self.section(point)))
        return point, residual[2:]

    def induced_action(self, element, point):
        """Output quotient address and additive right-fiber cocycle."""
        return self.right_coordinates(self.multiply(element, self.section(point)))


def symbolic_filiform_cocycle(nilpotency_class: int):
    """Exact rational expansion in LOG g and carrier x; no field fitting."""
    import sympy as sp

    k = nilpotency_class
    if type(k) is not int or k < 2:
        raise ValueError("k>=2 required")
    a, x, u = sp.symbols("a x u")
    b = sp.symbols(f"b0:{k}")
    def convolve(coefficients, value):
        return [sum(coefficients[i]*value[j-i] for i in range(j+1)) for j in range(k)]
    def exponential(t):
        return [t**j/sp.factorial(j) for j in range(k)]
    def section_vector(t):
        return [t**j/sp.factorial(j+1) for j in range(k)]
    group_b = convolve(section_vector(a), b)
    right_section = convolve(exponential(a), [u*v for v in section_vector(x)])
    remainder = [left+right-(b[0]+u)*v
                 for left, right, v in zip(group_b, right_section, section_vector(a+x))]
    cocycle = [sp.expand(value) for value in convolve(exponential(-a-x), remainder)]
    if cocycle[0] != 0:
        raise ArithmeticError("symbolic cocycle left the abelian ideal")
    return (a, *b), (x, u), tuple(cocycle[1:])


def evaluate_induced_cocycle_fixture(algebra, normal_class, quotient_part, ideal_part, carrier):
    """Known-element test of log(exp(-A-x) exp(A+B) exp(x)).

    Reuse the verified universal section word with (X,Y,Z)=(-A-x,A,B).
    These known logarithms are diagnostic witnesses, NOT receiver inputs.
    """
    for value in (quotient_part, ideal_part, carrier):
        _canonical_vec(value, algebra.dimension, algebra.p)
    first = tuple((-a-x) % algebra.p for a, x in zip(quotient_part, carrier))
    return evaluate_section_fixture(section_word_certificate(normal_class), algebra,
                                    first, tuple(quotient_part), tuple(ideal_part))


def upper_triangular_lie(size: int, p: int):
    """Exact matrix commutator, so Jacobi is supplied by associative matrices."""
    slots = tuple((i, j) for i in range(size) for j in range(i+1, size))
    lookup = {ij: k for k, ij in enumerate(slots)}
    triples = [(lookup[i, k], lookup[k, j], lookup[i, j])
               for i in range(size) for k in range(i+1, size) for j in range(k+1, size)]
    def bracket(left, right):
        out = [0]*len(slots)
        for ik, kj, ij in triples:
            out[ij] += left[ik]*right[kj]-right[ik]*left[kj]
        return tuple(x % p for x in out)
    return PublicLieAlgebra(p, len(slots), bracket), slots


def derived_length_three_witness(p=43):
    """Strict scope witness: L=<J,sum i^2 E_i,i+1> in ut_10, not an HSP run."""
    ring(p)
    if p <= 9:
        raise ValueError("witness uses the Lazard range p>9")
    algebra, slots = upper_triangular_lie(10, p)
    x = tuple(int(j == i+1) for i, j in slots)
    y = tuple((i+1)**2 % p if j == i+1 else 0 for i, j in slots)
    basis = algebra.span([x, y])
    for _ in range(algebra.dimension):
        extended = algebra.span(basis+[algebra.bracket(g, v) for g in (x, y) for v in basis])
        if len(extended) == len(basis):
            break
        basis = extended
    else:
        raise ArithmeticError("generated Lie subalgebra did not stabilize")
    lcs = algebra.lower_central_series(basis)
    normal = lcs[1]
    ncs = algebra.lower_central_series(normal)
    second_derived = ncs[1]
    third_derived = algebra.span([algebra.bracket(a, b) for a in second_derived for b in second_derived])
    c = algebra.bracket(x, y)
    d = algebra.bracket(x, c)
    value = d
    for _ in range(3):
        value = algebra.bracket(c, value)
    expected = tuple(-1680 % p if ij == (0, 9) else 0 for ij in slots)
    if value != expected or not any(value):
        raise ArithmeticError("exact class-nine commutator witness failed")
    if len(lcs)-1 != 9 or len(ncs)-1 != 4 or third_derived:
        raise ArithmeticError("derived-length-three scope witness failed")
    return algebra, basis, {
        "p": p, "ambient_class": 9, "normal_class": 4,
        "ambient_lcs_dimensions": [len(v) for v in lcs],
        "normal_lcs_dimensions": [len(v) for v in ncs],
        "derived_dimensions": [len(basis), len(normal), len(second_derived), len(third_derived)],
        "word": "ad_[X,Y]^3([X,[X,Y]])=-1680*E_1,10",
        "coefficient_mod_p": -1680 % p,
        "new_source_scope_only": True,
        "receiver_executed": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    witnesses = [derived_length_three_witness(p)[2] for p in (43, 2**127-1)]
    import sympy as sp
    degree_checks = []
    for k in (3, 4, 5, 7):
        g, x, phase = symbolic_filiform_cocycle(k)
        degree_checks.append({"normal_class": k,
                              "max_cocycle_total_degree": max(sp.Poly(v, *g, *x).total_degree() for v in phase)})
    report = {"schema": "right_abelian_induced_source_v1",
              "status": "conditional source/scope proposal; not an executed quantum receiver",
              "scope_witnesses": witnesses, "symbolic_cocycle_checks": degree_checks,
              "generic_cocycle_word": {
                  "existing_certificate": "ambient_section_potential.section_word_certificate",
                  "substitution": "(X,Y,Z)=(-A-x,A,B)",
                  "word": "log(exp(-A-x) exp(A+B) exp(x))",
                  "receiver_has_hidden_evaluator": False},
              "not_established": ["novelty", "whole HSP algorithm correctness",
                                  "general induced-phase compiler", "general SDE backend",
                                  "useful hard application"]}
    if args.write:
        path = Path(__file__).resolve().parents[1]/"research/reductions/right_abelian_induced_source.json"
        path.write_text(json.dumps(report, indent=2)+"\n")
        print(path)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
