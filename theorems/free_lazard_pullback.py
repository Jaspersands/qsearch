"""Public free-domain pullback for exponent-p, bounded-class HSP inputs.

Free Lie construction and Lazard words are standard ingredients. This
compiler evaluates a possibly noninjective map without target coordinates
or relation learning. It does NOT execute hidden-subgroup recovery.
An exact universal backend handles fixed class c<p; the shorter existing
class-four words are retained on their valid range.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from itertools import product
import json
from pathlib import Path

from theorems.ambient_section_potential import _nested_expansion
from theorems.class_four_group_words import ClassFourGroupWords
from theorems.jet_oracle_homogenization import lie_bch
from theorems.prime_character_opi import ring
from theorems.rees_hsp_reduction import _canonical, _tensor_algebra
from theorems.symbolic_scalar_phase_erasure import _fmpz_rref, _fmpz_solve_coordinates
from theorems.universal_lazard_words import UniversalLazardWords


@dataclass(frozen=True)
class FreeLazardDomain:
    p: int
    generator_count: int
    class_bound: int
    associative_words: tuple
    bracket_words: tuple
    basis_expansions: tuple
    algebra: object

    @property
    def dimension(self):
        return len(self.bracket_words)

    def word_coordinates(self, word):
        if (not word or len(word) > self.class_bound
                or any(type(i) is not int or not 0 <= i < self.generator_count for i in word)):
            raise ValueError("a generator bracket word of length 1..c is required")
        expansion = dict(_nested_expansion(tuple(word)))
        vector = tuple(int(expansion.get(w, 0)) % self.p for w in self.associative_words)
        coordinates = _fmpz_solve_coordinates(self.basis_expansions, vector, self.p)
        if coordinates is None:
            raise ArithmeticError("free bracket word was lost from the spanning set")
        return coordinates

    def multiply(self, left, right):
        return lie_bch(self.algebra, left, right, self.class_bound)

    def dilate(self, vector, scale):
        _canonical(vector, self.dimension, self.p)
        if type(scale) is not int or not 0 < scale < self.p:
            raise ValueError("a nonzero canonical scale is required")
        return tuple(x*pow(scale, len(word), self.p) % self.p
                     for x, word in zip(vector, self.bracket_words))


def free_lazard_domain(p, generator_count, class_bound):
    """Build the standard free nilpotent Lie algebra inside truncated tensors.

    Dimension is bounded by sum(s**j,j=1..c). Only word length is enumerated,
    never field elements or group elements. This is polynomial for FIXED c.
    Selected basis elements remain actual right-nested bracket words.
    """
    ring(p)
    if (type(generator_count) is not int or generator_count < 1
            or type(class_bound) is not int or not 1 <= class_bound < p):
        raise ValueError("positive generator count and 1<=c<p required")
    words = tuple(w for length in range(1, class_bound+1)
                  for w in product(range(generator_count), repeat=length))
    positions = {w: i for i, w in enumerate(words)}
    expansions = [dict(_nested_expansion(w)) for w in words]
    vectors = [tuple(int(expansion.get(w, 0)) % p for w in words) for expansion in expansions]
    # Pivot columns of the transpose select independent ORIGINAL bracket words.
    reduced, rank = _fmpz_rref(list(zip(*vectors)), p)
    selected = [next(j for j, value in enumerate(row) if value) for row in reduced]
    basis = tuple(vectors[j] for j in selected)
    bracket_words = tuple(words[j] for j in selected)
    supports = [tuple((w, int(value) % p) for w, value in expansions[j].items() if value)
                for j in selected]
    tensor = {}
    for i in range(rank):
        for j in range(i+1, rank):
            if len(bracket_words[i])+len(bracket_words[j]) > class_bound:
                continue
            vector = [0]*len(words)
            for a, x in supports[i]:
                for b, y in supports[j]:
                    vector[positions[a+b]] += x*y
                    vector[positions[b+a]] -= x*y
            coordinates = _fmpz_solve_coordinates(basis, tuple(x % p for x in vector), p)
            if coordinates is None:
                raise ArithmeticError("free Lie span is not bracket closed")
            if any(coordinates):
                tensor[i, j] = coordinates
                tensor[j, i] = tuple(-x % p for x in coordinates)
    return FreeLazardDomain(p, generator_count, class_bound, words, bracket_words,
                            basis, _tensor_algebra(p, rank, tensor))


class OpaqueFreePullback:
    """Evaluate the public surjection using only supplied opaque generators.

    Contract: supplied generators generate the target exponent-p group of
    class<=c. No kernel, target Lie tensor, normal form, or H is accepted.
    The promises are not inferred from individual relation checks.
    """
    def __init__(self, domain, generators, identity, multiply):
        self.domain = domain
        self.generators = tuple(generators)
        if len(self.generators) != domain.generator_count:
            raise ValueError("one target generator for each free generator required")
        self.words = (ClassFourGroupWords(domain.p, identity, multiply)
                      if domain.class_bound <= 4 and domain.p > 4 else
                      UniversalLazardWords(domain.p, domain.class_bound, identity, multiply))
        cache = {}
        def evaluate_word(word):
            if word not in cache:
                cache[word] = (self.generators[word[0]] if len(word) == 1 else
                               self.words.lie_bracket(self.generators[word[0]], evaluate_word(word[1:])))
            return cache[word]
        self.basis_images = tuple(evaluate_word(word) for word in domain.bracket_words)
        self.setup_group_multiplications = self.words.multiplication_calls

    def evaluate(self, vector):
        _canonical(vector, self.domain.dimension, self.domain.p)
        return self.words.linear_combination(self.basis_images, vector)

    def query(self, ordinary_hiding_oracle, vector):
        """One original ordinary query, after paid public word evaluation."""
        return ordinary_hiding_oracle(self.evaluate(vector))

    def project_recovered_generators(self, vectors):
        """Project a separately recovered FULL hidden preimage; do not solve it.

        Soundness/completeness of the supplied recovery are external. Zero
        images are harmless kernel generators and are removed by equality.
        """
        return tuple(image for vector in vectors
                     if (image := self.evaluate(vector)) != self.words.identity)

    def accounting(self):
        caps = self.words.operation_caps()
        return {"free_dimension": self.domain.dimension,
                "associative_coordinate_count": len(self.domain.associative_words),
                "setup_group_multiplications": self.setup_group_multiplications,
                "per_map_group_multiplication_cap": self.domain.dimension*caps["linear_combination_per_term"],
                "original_hiding_queries_per_pulled_back_query": 1,
                "source_copies_per_pulled_back_copy": 1,
                "word_backend": type(self.words).__name__,
                "target_relation_kernel_acquired": False,
                "target_lie_coordinates_acquired": False,
                "surjectivity_is_supplied_generator_promise": True,
                "coherent_circuit_synthesized": False,
                "hidden_preimage_recovery_implemented": False}


def build_report():
    records = []
    for p, s, c in ((7, 2, 3), (43, 3, 3), (2**127-1, 2, 4)):
        domain = free_lazard_domain(p, s, c)
        records.append({"prime": p, "generator_count": s, "class_bound": c,
                        "free_dimension": domain.dimension,
                        "associative_coordinate_count": len(domain.associative_words),
                        "bracket_words": domain.bracket_words})
    return {"status": "FREE_LAZARD_INPUT_PULLBACK_UNDER_REVIEW", "domains": records,
            "target_chart_acquisition_required_by_this_bridge": False,
            "unknown_target_kernel_required": False,
            "general_inverse_bch_backend_implemented": True,
            "quantum_receiver_implemented": False,
            "independent_review": False, "novelty_established": False,
            "speedup_claim_allowed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    content = json.dumps(build_report(), indent=2)+"\n"
    if args.write:
        path = Path(__file__).resolve().parents[1]/"research/reductions/free_lazard_pullback.json"
        path.write_text(content)
        print(path)
    else:
        print(content, end="")


if __name__ == "__main__":
    main()
