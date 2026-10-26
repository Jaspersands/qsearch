"""Universal right-fiber cocycle coefficients for an abelian Lie ideal.

R=ad(A)|I, S=ad(X)|I commute, C=[A,X] belongs to I, B belongs to I.
The cocycle log(exp(-A-X) exp(A+B) exp(X)) is a sum of R^i S^j B,C.
This is classical metabelian Lie algebra, not a new quantum algorithm.
All coefficient certificates are rational identities, not sampled values.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
import json
from math import factorial
from pathlib import Path

from theorems.ambient_section_potential import section_word_certificate
from theorems.prime_character_opi import ring


def _degree(key):
    kind, i, j = key
    return (2 if kind == "C" else 1)+i+j


def _add(target, source, scalar=Fraction(1)):
    for key, value in source.items():
        result = target.get(key, Fraction(0))+scalar*value
        if result:
            target[key] = result
        else:
            target.pop(key, None)


def _basis_bracket(left, right, cap):
    """Universal abelian module, with [A,X]=C and commuting shifts R,S."""
    if _degree(left)+_degree(right) > cap:
        return {}
    a, b = left[0], right[0]
    if a in ("A", "X") and b in ("A", "X"):
        return {} if a == b else {("C", 0, 0): Fraction(1 if a == "A" else -1)}
    if a in ("A", "X"):
        kind, i, j = right
        return {(kind, i+int(a == "A"), j+int(a == "X")): Fraction(1)}
    if b in ("A", "X"):
        return {key: -value for key, value in _basis_bracket(right, left, cap).items()}
    return {}


def _bracket(left, right, cap):
    result = {}
    for a, x in left.items():
        for b, y in right.items():
            _add(result, _basis_bracket(a, b, cap), x*y)
    return result


@lru_cache(maxsize=None)
def operator_coefficients(class_bound: int):
    """Return (seed,i,j), coefficient for every surviving operator monomial."""
    if type(class_bound) is not int or class_bound < 1:
        raise ValueError("positive integer class bound required")
    terms = {}
    for i in range(class_bound):
        for j in range(class_bound-i):
            value = Fraction((-1)**(i+j), factorial(i+1)*factorial(j))
            terms[("B", i, j)] = value
            if i+j+2 <= class_bound:
                terms[("C", i, j)] = value/(i+j+2)
    return tuple(sorted(terms.items()))


def verify_differential_coefficients(class_bound: int, terms=None):
    """Verify the complete formal differential equation, degree by degree.

    dK/dt = exp(-t(R+S)) B + t exp(-tS) phi(-tR) (C-SB).
    Initial K(0)=0. Integration degrees 1..k are invertible when p>k.
    This checks coefficients, not the Lie-group identification of the ODE.
    """
    expected_keys = dict(operator_coefficients(class_bound))
    supplied = operator_coefficients(class_bound) if terms is None else terms
    if tuple(sorted(dict(supplied).items())) != supplied:
        raise ValueError("canonical distinct operator terms required")
    values = dict(supplied)
    if values.keys() != expected_keys.keys() or any(type(c) is not Fraction for c in values.values()):
        raise ValueError("complete exact rational operator support required")
    for i in range(class_bound):
        for j in range(class_bound-i):
            b = values[("B", i, j)]
            exponential = Fraction((-1)**(i+j), factorial(i)*factorial(j))
            previous = values[("B", i, j-1)] if j else 0
            if (i+j+1)*b != exponential-previous:
                raise ValueError("B coefficient violates the differential identity")
            if i+j+2 <= class_bound and (i+j+2)*values[("C", i, j)] != b:
                raise ValueError("curvature coefficient violates the differential identity")


@lru_cache(maxsize=None)
def word_normal_form(class_bound: int):
    """Independently specialize the certified full exp/log Lie word.

    Universal module basis B_ij=R^i S^j B, C_ij=R^i S^j[A,X].
    This basis covers all A,X and B in an abelian ideal, not just filiform
    or semidirect examples. See the written specialization proof.
    """
    certificate = section_word_certificate(class_bound)
    certificate.verify()
    letters = ({("A", 0, 0): Fraction(-1), ("X", 0, 0): Fraction(-1)},
               {("A", 0, 0): Fraction(1)}, {("B", 0, 0): Fraction(1)})
    @lru_cache(maxsize=None)
    def nested(word):
        return letters[word[0]] if len(word) == 1 else _bracket(letters[word[0]], nested(word[1:]), class_bound)
    result = {}
    for word, coefficient in certificate.lie_terms:
        _add(result, nested(word), coefficient)
    return tuple(sorted(result.items()))


@dataclass(frozen=True)
class InducedCocycleCertificate:
    class_bound: int
    terms: tuple

    def verify(self):
        verify_differential_coefficients(self.class_bound, self.terms)
        if self.terms != word_normal_form(self.class_bound):
            raise ValueError("formula does not equal the universal exp/log word")

    def field_terms(self, p):
        self.verify()
        ring(p)
        if p <= self.class_bound:
            raise ValueError("Lazard range p>class required")
        return tuple((key, c.numerator*pow(c.denominator, -1, p) % p) for key, c in self.terms)


@lru_cache(maxsize=None)
def cocycle_certificate(class_bound):
    result = InducedCocycleCertificate(class_bound, operator_coefficients(class_bound))
    result.verify()
    return result


def certificate_report(class_bound):
    certificate = cocycle_certificate(class_bound)
    return {
        "class_bound": class_bound,
        "universal_operator_terms": len(certificate.terms),
        "universal_word_terms": len(section_word_certificate(class_bound).lie_terms),
        "differential_coefficients_verified": True,
        "full_word_normal_form_verified": True,
        "scope": "All class-at-most-k Lie algebras with [N,N]<=I and [I,I]=0, p>k; specialization uses these promises.",
        "terms": [{"seed": key[0], "ad_A": key[1], "ad_X": key[2], "coefficient": str(c)}
                  for key, c in certificate.terms],
        "speedup_claim_allowed": False,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = {"scope": "universal coefficient identities, not finite-source samples or a receiver",
              "reports": [certificate_report(k) for k in range(1, 8)]}
    if args.write:
        path = Path(__file__).resolve().parents[1]/"research/reductions/induced_cocycle_formula.json"
        path.write_text(json.dumps(result, indent=2)+"\n")
        print(path)
    for row in result["reports"]:
        print(json.dumps({key: row[key] for key in ("class_bound", "universal_operator_terms", "universal_word_terms")}))
