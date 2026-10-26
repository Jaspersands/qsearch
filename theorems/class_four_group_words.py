"""Public Lazard words for class <=4 p-groups, p>4.

Multiplication, identity, p and an annihilating power of p are inputs. Elements
are opaque to this module. These are classical word evaluators, not a
coherent compiler, basis-acquisition routine or hidden-subgroup solver.
The default annihilator is p. The group, annihilator, class and
unique-encoding promises are NOT certified.
"""
from __future__ import annotations

from theorems.prime_character_opi import ring


class ClassFourGroupWords:
    def __init__(self, p, identity, multiply, *, exponent_bound=None):
        ring(p)
        if p <= 4 or not callable(multiply):
            raise ValueError("p>4 and a public multiplication operation required")
        self.p = p
        self.exponent_bound = p if exponent_bound is None else exponent_bound
        if type(self.exponent_bound) is not int or self.exponent_bound < p:
            raise ValueError("annihilating positive power of p required")
        reduced = self.exponent_bound
        while reduced % p == 0:
            reduced //= p
        if reduced != 1:
            raise ValueError("annihilator must be a power of the supplied prime")
        self.identity = identity
        self._multiply = multiply
        self.multiplication_calls = 0

    def multiply(self, a, b):
        self.multiplication_calls += 1
        return self._multiply(a, b)

    def power(self, a, exponent):
        if type(exponent) is not int:
            raise ValueError("integer exponent required")
        return self._binary_power(a, exponent % self.exponent_bound)

    def _binary_power(self, a, exponent):
        result = self.identity
        while exponent:
            if exponent & 1:
                result = self.multiply(result, a)
            a = self.multiply(a, a)
            exponent //= 2
        return result

    def commutator(self, a, b):
        """Convention a^-1 b^-1 a b; inverse uses the annihilator promise."""
        return self.multiply(self.multiply(self.multiply(self.power(a, -1),
                                                        self.power(b, -1)), a), b)

    def _rational_power(self, a, numerator, denominator):
        return self.power(a, numerator*pow(denominator, -1, self.exponent_bound))

    def lie_add(self, a, b):
        """ADD_4(a,b)=exp(log(a)+log(b)), not ordinary group multiplication."""
        w = self.commutator(a, b)
        u, v = self.commutator(a, w), self.commutator(b, w)
        A, C = self.commutator(a, u), self.commutator(b, v)
        result = self.multiply(a, b)
        for element, numerator, denominator in (
            (w, -1, 2), (u, -1, 12), (v, 1, 12), (A, -1, 24), (C, 1, 24)
        ):
            result = self.multiply(result, self._rational_power(element, numerator, denominator))
        return result

    def lie_bracket(self, a, b):
        """BRACKET_4(a,b)=exp([log(a),log(b)]), with weight-four corrections."""
        w = self.commutator(a, b)
        u, v = self.commutator(a, w), self.commutator(b, w)
        A, B, C = self.commutator(a, u), self.commutator(b, u), self.commutator(b, v)
        result = w
        for element, numerator, denominator in (
            (u, 1, 2), (v, 1, 2), (A, 1, 3), (B, 1, 4), (C, 1, 3)
        ):
            result = self.multiply(result, self._rational_power(element, numerator, denominator))
        return result

    def linear_combination(self, elements, coefficients):
        """Forward additive encoding over Z/M; not necessarily injective."""
        if len(elements) != len(coefficients) or any(
            type(c) is not int or not 0 <= c < self.exponent_bound for c in coefficients
        ):
            raise ValueError("one canonical residue modulo the annihilator per element required")
        result = self.identity
        for element, coefficient in zip(elements, coefficients):
            if coefficient:
                result = self.lie_add(result, self.power(element, coefficient))
        return result

    def lie_spanning_family(self, group_generators):
        """All right-nested brackets through length four, not a certified basis.

        Group generators alone need not generate the additive Lie ring.
        At most sum(s**k for k=1..4) entries; no group/field enumeration.
        """
        generators = tuple(group_generators)
        layer = [g for g in generators if g != self.identity]
        result = list(layer)
        for _ in range(3):
            layer = [self.lie_bracket(g, h) for g in generators for h in layer]
            layer = [g for g in layer if g != self.identity]
            result.extend(layer)
        return tuple(result)

    def p_torsion_from_decomposition(self, cyclic_generators, cyclic_orders):
        """Order-p generators from an ACQUIRED additive cyclic decomposition.

        Exact cyclic orders are checked, but independence and spanning are
        NOT. Those require actual relation-kernel acquisition/decomposition.
        Supplying an arbitrary irredundant group generating set is invalid.
        """
        if len(cyclic_generators) != len(cyclic_orders):
            raise ValueError("one cyclic order per additive generator required")
        result = []
        for generator, order in zip(cyclic_generators, cyclic_orders):
            if (type(order) is not int or order < 1
                    or self.exponent_bound % order):
                raise ValueError("cyclic orders must divide the annihilating prime power")
            # Do not reduce this exponent: this is an actual order check.
            if self._binary_power(generator, order) != self.identity:
                raise ValueError("reported cyclic order does not annihilate its generator")
            if order == 1:
                continue
            torsion = self._binary_power(generator, order//self.p)
            if torsion == self.identity:
                raise ValueError("reported cyclic order is not exact")
            result.append(torsion)
        return tuple(result)

    def operation_caps(self):
        """Worst-case original multiplication calls per public operation."""
        bits = self.exponent_bound.bit_length()
        return {"power": 2*bits, "lie_add": 30*bits+21,
                "lie_bracket": 34*bits+23, "linear_combination_per_term": 32*bits+21,
                "p_torsion_per_factor": 4*bits}
