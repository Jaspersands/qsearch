"""Public normal-word to class-three Lie-coordinate bridge, p>3.

Input promise: exponent p, class <=3, unique refined polycyclic normal
words, and a polynomial-time collection procedure. No HSP oracle or hidden
subgroup is read. The classical maps can be reversibly compiled; this
module does not implement that quantum compiler or the ISS recursion.
"""
from __future__ import annotations

import argparse
from itertools import combinations
import json
from pathlib import Path
import random

from flint import nmod_mat
import numpy as np

from theorems.nil3_cocycle_receiver import ClassThreeBCH
from theorems.prime_character_opi import ring

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/reductions/nil3_normal_word_bridge.json"


def matvec(matrix, vector, p):
    return tuple(sum(a*b for a, b in zip(row, vector)) % p for row in matrix)


class NormalWordLieBridge:
    def __init__(self, p, dimension, collect):
        ring(p)
        if p <= 3 or type(dimension) is not int or dimension < 1 or not callable(collect):
            raise ValueError("p>3, positive dimension and public collector required")
        self.p, self.dimension, self.collect = p, dimension, collect
        self.zero = (0,)*dimension
        self.generators = [tuple(int(i == j) for j in range(dimension))
                           for i in range(dimension)]
        self.collection_calls = 0

    def canonical(self, word):
        if len(word) != self.dimension or any(type(x) is not int or not 0 <= x < self.p for x in word):
            raise ValueError("canonical normal word required")
        return tuple(word)

    def multiply(self, a, b):
        self.collection_calls += 1
        return self.canonical(self.collect(self.canonical(a), self.canonical(b)))

    def power(self, a, exponent):
        """Repeated squaring; exponent reduction uses the explicit exponent-p promise."""
        a = self.canonical(a)
        if type(exponent) is not int:
            raise ValueError("integer exponent required")
        exponent %= self.p
        result = self.zero
        while exponent:
            if exponent & 1:
                result = self.multiply(result, a)
            a = self.multiply(a, a)
            exponent //= 2
        return result

    def commutator(self, a, b):
        """ISS convention: a^-1 b^-1 a b."""
        return self.multiply(self.multiply(self.multiply(self.power(a, -1),
                                                        self.power(b, -1)), a), b)

    def lie_bracket(self, a, b):
        w = self.commutator(a, b)
        half = pow(2, -1, self.p)
        result = self.multiply(w, self.power(self.commutator(a, w), half))
        return self.multiply(result, self.power(self.commutator(b, w), half))

    def lie_add(self, a, b):
        w = self.commutator(a, b)
        result = self.multiply(self.multiply(a, b), self.power(w, -pow(2, -1, self.p)))
        result = self.multiply(result, self.power(self.commutator(a, w), -pow(12, -1, self.p)))
        return self.multiply(result, self.power(self.commutator(b, w), pow(12, -1, self.p)))

    def coordinates(self, word):
        """Peel an additive basis along the supplied polycyclic flag."""
        current, result = self.canonical(word), []
        for i, generator in enumerate(self.generators):
            if any(current[:i]):
                raise ArithmeticError("normal-word flag was not preserved")
            coefficient = current[i]
            result.append(coefficient)
            current = self.lie_add(current, self.power(generator, -coefficient))
            if any(current[:i+1]):
                raise ArithmeticError("coordinate peeling failed; check presentation promises")
        if current != self.zero:
            raise ArithmeticError("normal-word residual is not identity")
        return tuple(result)

    def element(self, vector):
        vector = self.canonical(vector)
        result = self.zero
        for c, generator in zip(vector, self.generators):
            result = self.lie_add(result, self.power(generator, c))
        return result

    def adapted_presentation(self):
        """Compute public structure constants and a derived-ideal-adapted basis."""
        p, d = self.p, self.dimension
        brackets = {(i, j): self.coordinates(self.lie_bracket(self.generators[i], self.generators[j]))
                    for i, j in combinations(range(d), 2)}
        values = [row for row in brackets.values() if any(row)]
        if not values:
            raise ValueError("abelian input: use the abelian HSP route directly")
        reduced, n = nmod_mat(values, p).rref()
        derived = [tuple(int(reduced[i, j]) for j in range(d)) for i in range(n)]
        spanning, complement = list(derived), []
        for e in self.generators:
            if nmod_mat(spanning + [e], p).rref()[1] > len(spanning):
                spanning.append(e)
                complement.append(e)
        if len(spanning) != d:
            raise ArithmeticError("failed to construct a full public Lie basis")
        basis = complement + derived
        forward = [list(row) for row in zip(*basis)]
        augmented = [row + list(e) for row, e in zip(forward, self.generators)]
        inverse_rref, rank = nmod_mat(augmented, p).rref()
        if rank != d:
            raise ArithmeticError("public basis matrix is singular")
        inverse = [[int(inverse_rref[i, d+j]) for j in range(d)] for i in range(d)]

        def old_bracket(a, b):
            return tuple(sum((a[i]*b[j]-a[j]*b[i])*value[k]
                             for (i, j), value in brackets.items()) % p for k in range(d))

        new_brackets = {(i, j): matvec(inverse, old_bracket(basis[i], basis[j]), p)
                        for i, j in combinations(range(d), 2)}
        group = ClassThreeBCH(p, len(complement), n,
                              {key: value for key, value in new_brackets.items() if any(value)})
        return group, forward, inverse


def ut4_matrix(word, p):
    """Fixture only: ordered E12,E23,E34,E13,E24,E14 normal words."""
    a, b, c, d, e, f = word
    return np.array([[1, a, (a*b+d) % p, (a*b*c+a*e+f) % p],
                     [0, 1, b, (b*c+e) % p],
                     [0, 0, 1, c], [0, 0, 0, 1]], dtype=object)


def ut4_normal_word(matrix, p):
    a, b, c = (int(matrix[i, i+1]) % p for i in range(3))
    u, v, w = (int(matrix[i, j]) % p for i, j in [(0, 2), (1, 3), (0, 3)])
    return a, b, c, (u-a*b) % p, (v-b*c) % p, (w-a*v) % p


def ut4_bridge(p=5):
    return NormalWordLieBridge(
        p, 6, lambda a, b: ut4_normal_word(ut4_matrix(a, p) @ ut4_matrix(b, p) % p, p))


def controls(seed=20261024):
    bridge, rng = ut4_bridge(), random.Random(seed)
    group, forward, inverse = bridge.adapted_presentation()
    public_setup_calls = bridge.collection_calls
    failures = 0
    old_coordinates_are_not_log = False
    for _ in range(64):
        a, b = [tuple(rng.randrange(5) for _ in range(6)) for _ in range(2)]
        av, bv = [bridge.coordinates(w) for w in (a, b)]
        old_coordinates_are_not_log |= av != a
        if bridge.element(av) != a:
            failures += 1
        expected_sum = tuple((x+y) % 5 for x, y in zip(av, bv))
        if bridge.coordinates(bridge.lie_add(a, b)) != expected_sum:
            failures += 1
        actual = matvec(inverse, bridge.coordinates(bridge.multiply(a, b)), 5)
        expected = group.bch(matvec(inverse, av, 5), matvec(inverse, bv, 5))
        if actual != expected:
            failures += 1
        adapted = matvec(inverse, av, 5)
        if bridge.element(matvec(forward, adapted, 5)) != a:
            failures += 1
    if failures or not old_coordinates_are_not_log:
        raise ArithmeticError("normal-word bridge or false-coordinate control failed")
    return {
        "id": "NIL3-NORMAL-WORD-LIE-BRIDGE",
        "status": "public-classical-conversion-local-derivation-review-pending",
        "p": 5, "dimension": group.dimension, "quotient_dimension": group.m,
        "derived_dimension": group.n, "pairs_checked": 64, "failures": failures,
        "public_setup_collection_calls": public_setup_calls,
        "total_diagnostic_collection_calls": bridge.collection_calls,
        "normal_word_coordinates_are_not_logarithmic_coordinates": old_coordinates_are_not_log,
        "source_input": "unique refined polycyclic normal words and public collection",
        "public_operations": ["multiplication", "exponent-p powering", "leading normal-word digit"],
        "hidden_subgroup_or_oracle_accessed": False,
        "coordinate_inverse_uses_discrete_log_or_enumeration": False,
        "efficient_classical_maps_explicit": True,
        "coherent_compiler_executed": False,
        "black_box_presentation_acquisition_implemented": False,
        "iss_recursive_hsp_solver_executed": False,
        "general_nil3_hsp_claim_admitted": False,
        "novelty_established": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = controls()
    output = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write:
        REPORT.write_text(output)
    print(output, end="")


if __name__ == "__main__":
    main()
