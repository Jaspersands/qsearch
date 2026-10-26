"""Exact public inverse-BCH word compilation at any fixed class c<p.

Known Lazard / Dynkin-Specht-Wever ingredients. Rational straight-line
programs are certified in the free associative algebra, then evaluated on
opaque exponent-p group elements. No target coordinates, source queries,
group enumeration or quantum receiver. Cost is NOT uniform polynomial in c.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
import json
from math import factorial, gcd
from pathlib import Path

from theorems.ambient_section_potential import _add, _exponential, _multiply, _nested_expansion
from theorems.prime_character_opi import ring


def _logarithm(group_element, degree):
    reduced = dict(group_element)
    if reduced.pop((), None) != 1:
        raise ValueError("formal group element must have constant term one")
    result, power = {}, {(): Fraction(1)}
    for k in range(1, degree+1):
        power = _multiply(power, reduced, degree)
        _add(result, power, Fraction((-1)**(k+1), k))
    return result


def _target(operation, degree):
    if operation == "add":
        return {(0,): Fraction(1), (1,): Fraction(1)}
    if operation == "bracket":
        return dict(_nested_expansion((0, 1))) if degree >= 2 else {}
    raise ValueError("operation must be add or bracket")


def _allowed_denominator(denominator, degree):
    allowed = factorial(degree)
    while denominator > 1:
        common = gcd(denominator, allowed)
        if common == 1:
            return False
        denominator //= common
    return True


@dataclass(frozen=True)
class LazardWordCertificate:
    class_bound: int
    operation: str
    instructions: tuple
    output: int
    stages: tuple

    def verify(self):
        c = self.class_bound
        if type(c) is not int or c < 1:
            raise ValueError("positive fixed class required")
        target = _target(self.operation, c)
        values = [{(): Fraction(1)}, _exponential({(0,): Fraction(1)}, c),
                  _exponential({(1,): Fraction(1)}, c)]
        for instruction in self.instructions:
            if not isinstance(instruction, tuple) or not instruction:
                raise ValueError("invalid word instruction")
            kind, *args = instruction
            if kind == "mul" and len(args) == 2:
                if any(type(i) is not int or not 0 <= i < len(values) for i in args):
                    raise ValueError("multiply must reference earlier values")
                value = _multiply(values[args[0]], values[args[1]], c)
            elif kind == "pow" and len(args) == 3:
                i, numerator, denominator = args
                if (any(type(x) is not int for x in args) or not 0 <= i < len(values)
                        or denominator < 1 or not _allowed_denominator(denominator, c)):
                    raise ValueError("invalid power or denominator outside Z[1/c!]")
                scalar = Fraction(numerator, denominator)
                value = _exponential({w: a*scalar for w, a in _logarithm(values[i], c).items()}, c)
            else:
                raise ValueError("unknown word instruction")
            values.append(value)
        if type(self.output) is not int or not 0 <= self.output < len(values):
            raise ValueError("invalid output reference")
        if len(self.stages) != c:
            raise ValueError("one completed correction stage per degree required")
        for expected, stage in enumerate(self.stages, 1):
            if (not isinstance(stage, tuple) or len(stage) != 2
                    or type(stage[0]) is not int or stage[0] != expected
                    or type(stage[1]) is not int or not 0 <= stage[1] < len(values)):
                raise ValueError("invalid correction stage")
            logarithm = _logarithm(values[stage[1]], c)
            if {w: a for w, a in logarithm.items() if len(w) <= expected} != {
                    w: a for w, a in target.items() if len(w) <= expected}:
                raise ValueError("filtration correction failed")
        if self.stages[-1][1] != self.output or values[self.output] != _exponential(target, c):
            raise ValueError("word is not the exact requested inverse-BCH operation")

    def multiplication_cap(self, p):
        return sum(1 if step[0] == "mul" else 2*p.bit_length() for step in self.instructions)


class _Builder:
    def __init__(self, degree):
        self.degree, self.instructions, self.interned = degree, [], {}
        self.nested_cache = {}
        self.values = [{(): Fraction(1)}, _exponential({(0,): Fraction(1)}, degree),
                       _exponential({(1,): Fraction(1)}, degree)]

    def append(self, instruction, compute):
        if instruction not in self.interned:
            self.interned[instruction] = len(self.values)
            self.instructions.append(instruction)
            self.values.append(compute())
        return self.interned[instruction]

    def multiply(self, left, right):
        if left == 0 or right == 0:
            return right if left == 0 else left
        return self.append(("mul", left, right),
                           lambda: _multiply(self.values[left], self.values[right], self.degree))

    def power(self, value, scalar):
        scalar = Fraction(scalar)
        if not scalar or value == 0:
            return 0
        if scalar == 1:
            return value
        return self.append(("pow", value, scalar.numerator, scalar.denominator), lambda: _exponential(
            {w: a*scalar for w, a in _logarithm(self.values[value], self.degree).items()}, self.degree))

    def commutator(self, left, right):
        # xyx^-1y^-1 has leading Lie term [X,Y]. Keep this convention explicit.
        if left == right or left == 0 or right == 0:
            return 0
        return self.multiply(self.multiply(self.multiply(left, right), self.power(left, -1)),
                             self.power(right, -1))

    def nested(self, word):
        if word not in self.nested_cache:
            self.nested_cache[word] = (word[0]+1 if len(word) == 1 else
                                       self.commutator(word[0]+1, self.nested(word[1:])))
        return self.nested_cache[word]


@lru_cache(maxsize=None, typed=True)
def compile_lazard_word(class_bound, operation):
    if type(class_bound) is not int or class_bound < 1:
        raise ValueError("positive fixed class required")
    target = _target(operation, class_bound)
    builder = _Builder(class_bound)
    result = builder.multiply(1, 2) if operation == "add" else builder.commutator(1, 2)
    stages = []
    for degree in range(1, class_bound+1):
        residual = _logarithm(builder.values[result], class_bound)
        _add(residual, target, Fraction(-1))
        if any(len(w) < degree for w in residual):
            raise ArithmeticError("an earlier filtration correction was lost")
        homogeneous = {w: a for w, a in residual.items() if len(w) == degree}
        projected = {}
        for word, coefficient in sorted(homogeneous.items()):
            expansion = dict(_nested_expansion(word))
            _add(projected, expansion, coefficient/degree)
            if expansion:
                result = builder.multiply(result, builder.power(builder.nested(word), -coefficient/degree))
        if projected != homogeneous:
            raise ArithmeticError("homogeneous residual failed the Dynkin projection identity")
        stages.append((degree, result))
    certificate = LazardWordCertificate(class_bound, operation, tuple(builder.instructions), result, tuple(stages))
    certificate.verify()
    return certificate


class UniversalLazardWords:
    """Opaque exponent-p evaluator; class/exponent promises are NOT certified.

    All branches depend only on public coefficients. Reversible synthesis
    and workspace cleanup must still be paid by a quantum implementation.
    """
    def __init__(self, p, class_bound, identity, multiply):
        ring(p)
        if type(class_bound) is not int or not 1 <= class_bound < p or not callable(multiply):
            raise ValueError("1<=c<p and public multiplication required")
        self.p, self.class_bound, self.identity = p, class_bound, identity
        self._multiply, self.multiplication_calls = multiply, 0
        self.certificates = {op: compile_lazard_word(class_bound, op) for op in ("add", "bracket")}

    def multiply(self, left, right):
        self.multiplication_calls += 1
        return self._multiply(left, right)

    def power(self, element, exponent):
        if type(exponent) is not int:
            raise ValueError("integer exponent required")
        exponent %= self.p
        result = self.identity
        while exponent:
            if exponent & 1:
                result = self.multiply(result, element)
            element = self.multiply(element, element)
            exponent //= 2
        return result

    def _evaluate(self, operation, left, right):
        certificate = self.certificates[operation]
        values = [self.identity, left, right]
        for instruction in certificate.instructions:
            if instruction[0] == "mul":
                value = self.multiply(values[instruction[1]], values[instruction[2]])
            else:
                _, i, numerator, denominator = instruction
                value = self.power(values[i], numerator*pow(denominator, -1, self.p))
            values.append(value)
        return values[certificate.output]

    def lie_add(self, left, right):
        return self._evaluate("add", left, right)

    def lie_bracket(self, left, right):
        return self._evaluate("bracket", left, right)

    def linear_combination(self, elements, coefficients):
        if len(elements) != len(coefficients) or any(
                type(x) is not int or not 0 <= x < self.p for x in coefficients):
            raise ValueError("one canonical field coefficient per element required")
        result = self.identity
        for element, coefficient in zip(elements, coefficients):
            if coefficient:
                result = self.lie_add(result, self.power(element, coefficient))
        return result

    def operation_caps(self):
        add = self.certificates["add"].multiplication_cap(self.p)
        return {"power": 2*self.p.bit_length(), "lie_add": add,
                "lie_bracket": self.certificates["bracket"].multiplication_cap(self.p),
                "linear_combination_per_term": add+2*self.p.bit_length()}


def build_report():
    records = []
    for c in range(1, 7):
        for operation in ("add", "bracket"):
            certificate = compile_lazard_word(c, operation)
            records.append({"class_bound": c, "operation": operation,
                            "instructions": certificate.instructions, "output": certificate.output,
                            "stages": certificate.stages, "exact_free_identity_verified": True,
                            "denominators_in_Z_inverting_c_factorial": True,
                            "group_multiplication_cap_at_127_bit_prime": certificate.multiplication_cap(2**127-1)})
    return {"status": "KNOWN_LAZARD_WORD_CONSTRUCTION_IMPLEMENTED", "certificates": records,
            "uniform_polynomial_cost_in_class": False, "target_chart_required": False,
            "quantum_circuit_synthesized": False, "hidden_subgroup_recovery_implemented": False,
            "novelty_established": False, "speedup_claim_allowed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    content = json.dumps(build_report(), indent=2)+"\n"
    if args.write:
        path = Path(__file__).resolve().parents[1]/"research/reductions/universal_lazard_words.json"
        path.write_text(content)
        print(path)
    else:
        print(content, end="")


if __name__ == "__main__":
    main()
