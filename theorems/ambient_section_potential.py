"""Universal coefficient certificates for the full-jet section potential.

This computes log(exp(X) exp(Y+Z) exp(-X-Y)) in the truncated FREE
associative algebra over Q, and independently expands a right-nested Lie
representation to certify every coefficient. For the HSP section word,
X=s(q-pi(q)), Y=s(pi(q)), Z=a(pi(q)); these maps are proof witnesses.
Nothing here supplies a hidden-potential evaluator to the quantum receiver.

Known BCH/Lazard and Dynkin-Specht-Wever algebra, not a novel algorithm.
Certificate generation is exponential in c but independent of p and input
dimension. The proposed algorithm treats c as a fixed constant.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache

from theorems.prime_character_opi import ring
from theorems.symbolic_scalar_phase_erasure import _canonical_vec


Word = tuple[int, ...]
Terms = tuple[tuple[Word, Fraction], ...]


def _add(target, source, scalar=Fraction(1)):
    for word, coefficient in source.items():
        value = target.get(word, Fraction(0)) + scalar*coefficient
        if value:
            target[word] = value
        else:
            target.pop(word, None)


def _multiply(left, right, degree):
    result = {}
    for u, a in left.items():
        for v, b in right.items():
            if len(u)+len(v) <= degree:
                word = u+v
                result[word] = result.get(word, Fraction(0))+a*b
    return {word: value for word, value in result.items() if value}


def _exponential(linear, degree):
    result, power = {(): Fraction(1)}, {(): Fraction(1)}
    for k in range(1, degree+1):
        power = {word: value/k for word, value in _multiply(power, linear, degree).items()}
        _add(result, power)
    return result


@lru_cache(maxsize=None)
def _section_log(degree: int) -> Terms:
    if type(degree) is not int or degree < 1:
        raise ValueError("positive integer truncation degree required")
    factors = [{(0,): Fraction(1)}, {(1,): Fraction(1), (2,): Fraction(1)},
               {(0,): Fraction(-1), (1,): Fraction(-1)}]
    expanded = {(): Fraction(1)}
    for factor in factors:
        expanded = _multiply(expanded, _exponential(factor, degree), degree)
    expanded.pop(())
    logarithm, power = {}, {(): Fraction(1)}
    for k in range(1, degree+1):
        power = _multiply(power, expanded, degree)
        _add(logarithm, power, Fraction((-1)**(k+1), k))
    return tuple(sorted(logarithm.items()))


@lru_cache(maxsize=None)
def _nested_expansion(word: Word) -> Terms:
    """Expand [x0,[x1,...]] by AB-BA, independently of exp/log."""
    if not word:
        raise ValueError("nonempty Lie word required")
    if len(word) == 1:
        return ((word, Fraction(1)),)
    result = {}
    for tail, value in _nested_expansion(word[1:]):
        _add(result, {(word[0],)+tail: value})
        _add(result, {tail+(word[0],): value}, Fraction(-1))
    return tuple(sorted(result.items()))


@dataclass(frozen=True)
class SectionWordCertificate:
    class_bound: int
    associative_terms: Terms
    lie_terms: Terms

    def verify(self) -> None:
        """Check the full universal identity, not finitely many evaluations."""
        if self.associative_terms != _section_log(self.class_bound):
            raise ValueError("certificate is not the actual section-word logarithm")
        if tuple(sorted(dict(self.lie_terms).items())) != self.lie_terms:
            raise ValueError("canonical distinct Lie words required")
        expansion = {}
        for word, coefficient in self.lie_terms:
            if (not word or len(word) > self.class_bound or not coefficient
                    or not isinstance(coefficient, Fraction)
                    or any(type(letter) is not int or not 0 <= letter < 3 for letter in word)):
                raise ValueError("invalid rational Lie coefficient or word")
            _add(expansion, dict(_nested_expansion(word)), coefficient)
        if tuple(sorted(expansion.items())) != self.associative_terms:
            raise ValueError("Lie expansion does not reproduce every associative coefficient")
        linear = {word: value for word, value in self.associative_terms if len(word) == 1}
        if linear != {(2,): Fraction(1)}:
            raise ValueError("section word must have only Z as its linear part")

    def field_terms(self, p: int) -> tuple[tuple[Word, int], ...]:
        """Reduce only over a prime field in the Lazard range."""
        self.verify()
        if type(p) is not int or p <= self.class_bound:
            raise ValueError("Lazard range p>c required")
        ring(p)
        return tuple((word, value.numerator*pow(value.denominator, -1, p) % p)
                     for word, value in self.lie_terms)


@lru_cache(maxsize=None)
def section_word_certificate(class_bound: int) -> SectionWordCertificate:
    logarithm = _section_log(class_bound)
    # Dynkin-Specht-Wever suggests this representation. Its correctness is
    # then checked coefficientwise, so the projection is not trusted blindly.
    lie = tuple((word, value/len(word)) for word, value in logarithm
                if _nested_expansion(word))
    certificate = SectionWordCertificate(class_bound, logarithm, lie)
    certificate.verify()
    return certificate


def evaluate_section_fixture(certificate, algebra, x, y, z):
    """Known-element diagnostic ONLY; the receiver never receives x,y,z."""
    for value in (x, y, z):
        _canonical_vec(value, algebra.dimension, algebra.p)
    values = (tuple(x), tuple(y), tuple(z))
    @lru_cache(maxsize=None)
    def nested(word):
        if len(word) == 1:
            return values[word[0]]
        return algebra.bracket(values[word[0]], nested(word[1:]))
    result = [0]*algebra.dimension
    for word, coefficient in certificate.field_terms(algebra.p):
        value = nested(word)
        result = [(a+coefficient*b) % algebra.p for a, b in zip(result, value)]
    return tuple(result)


def polynomial_section_fixture(certificate, algebra, linear_inputs):
    """Expand the actual Lie word on supplied linear proof witnesses.

    linear_inputs[letter][quotient_variable] is a vector in L. This is a
    coefficient-level falsifier with KNOWN witnesses, not an operational
    potential-learning routine or oracle. Lie/Jacobi and nilpotency are
    input promises; PublicLieAlgebra's callable alone does not prove them.
    """
    if len(linear_inputs) != 3 or not linear_inputs[0]:
        raise ValueError("three positive-width linear input maps required")
    m, p, n = len(linear_inputs[0]), algebra.p, algebra.dimension
    if any(len(rows) != m for rows in linear_inputs):
        raise ValueError("matching quotient dimensions required")
    for rows in linear_inputs:
        for row in rows:
            _canonical_vec(row, n, p)
    def accumulate(target, exponent, vector, coefficient=1):
        value = tuple((a+coefficient*b) % p
                      for a, b in zip(target.get(exponent, (0,)*n), vector))
        if any(value):
            target[exponent] = value
        else:
            target.pop(exponent, None)
    linear = tuple({tuple(int(i == j) for i in range(m)): tuple(row)
                    for j, row in enumerate(rows) if any(row)} for rows in linear_inputs)
    @lru_cache(maxsize=None)
    def nested(word):
        if len(word) == 1:
            return linear[word[0]]
        result = {}
        for alpha, left in linear[word[0]].items():
            for beta, right in nested(word[1:]).items():
                exponent = tuple(a+b for a, b in zip(alpha, beta))
                accumulate(result, exponent, algebra.bracket(left, right))
        return result
    result = {}
    for word, coefficient in certificate.field_terms(p):
        for exponent, vector in nested(word).items():
            accumulate(result, exponent, vector, coefficient)
    return result


def certificate_summary(class_bound: int) -> dict:
    certificate = section_word_certificate(class_bound)
    degrees = range(1, class_bound+1)
    return {
        "class_bound": class_bound,
        "coefficient_identity_verified": True,
        "associative_words_by_degree": {d: sum(len(w) == d for w, _ in certificate.associative_terms)
                                         for d in degrees},
        "right_nested_words_by_degree": {d: sum(len(w) == d for w, _ in certificate.lie_terms)
                                          for d in degrees},
        "linear_part": "Z",
        "central_tail_starts_at_degree": class_bound-1 if class_bound >= 3 else None,
        "noncentral_degree_bound": class_bound-2 if class_bound >= 3 else None,
        "scope": "Universal coefficient certificate; c>=3 for the projected bound; p>c for Lazard.",
        "speedup_claim_allowed": False,
    }
