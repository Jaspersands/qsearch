"""Public query compiler for the deterministic polynomial-jet oracle lift.

This constructs original-oracle INPUTS, never a hidden potential. With a
coherent function oracle, the tuple can be evaluated reversibly using one
original query per point. This module is classical control, not a quantum
receiver or a source-only oracle upgrade. See JET_ORACLE_HOMOGENIZATION.md.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from functools import cached_property, lru_cache
import json
from math import comb, prod
from pathlib import Path

from theorems.affine_phase_erasure import monomials
from theorems.full_jet_resource_certificate import sde_arity
from theorems.nonabelian_jet_homogenization import ambient_jet_certificate, bch_certificate
from theorems.prime_character_opi import ring
from theorems.ut5_matrix_phase_alignment import _canonical


def simplex_indices(width, degree):
    return tuple(sorted(monomials(width, degree), key=lambda a: (sum(a), a)))


def simplex_design(p, quotient_width, degree):
    """Unisolvent for t*polynomials of total degree<=degree-1, with t!=0.

    On nodes beta in N^(m+1), |beta|<=degree-1, the Newton basis
    prod_j binom(v_j,alpha_j) has a unit triangular evaluation matrix.
    Put u=beta[:-1], t=beta[-1]+1. No random sampling or field scan.
    """
    ring(p)
    if (type(degree) is not int or degree < 1 or p <= degree
            or type(quotient_width) is not int or quotient_width < 1):
        raise ValueError("positive dimensions/degree and p>degree required")
    return tuple((beta[:-1], beta[-1]+1) for beta in simplex_indices(quotient_width+1, degree-1))


def lie_bch(algebra, left, right, class_bound):
    """Known public Lazard operations; caller supplies a genuine class bound."""
    if type(class_bound) is not int or not 1 <= class_bound < algebra.p:
        raise ValueError("Lazard class bound below p required")
    _canonical(left, algebra.dimension, algebra.p)
    _canonical(right, algebra.dimension, algebra.p)
    values = tuple(left), tuple(right)
    @lru_cache(maxsize=None)
    def nested(word):
        return values[word[0]] if len(word) == 1 else algebra.bracket(values[word[0]], nested(word[1:]))
    result = [0]*algebra.dimension
    for word, coefficient in bch_certificate(class_bound):
        scale = coefficient.numerator*pow(coefficient.denominator, -1, algebra.p) % algebra.p
        result = [(a+scale*b) % algebra.p for a, b in zip(result, nested(word))]
    return tuple(result)


@dataclass(frozen=True)
class LiftedOraclePlan:
    """Public compiler for f_hat(a,q) = tuple_i f(E_i(a)*s(Y_i+s_i*q)).

    Elements of J use logarithmic polynomial coordinates. The original
    oracle is queried on logarithms in the supplied ambient coordinate
    space. No U, H, potential or oracle outputs enter plan construction.
    The graph-hiding theorem requires H intersect exp(L')=1; this promise
    cannot be inferred by inspecting the public Lie algebra.
    """
    algebra: object
    certificate: object

    def __post_init__(self):
        self.certificate.verify(self.algebra)

    @property
    def group(self):
        return self.certificate.group

    @cached_property
    def points(self):
        return simplex_design(self.algebra.p, self.group.quotient_width, self.group.class_bound)

    @property
    def original_queries(self):
        return comb(self.group.quotient_width+self.group.class_bound, self.group.quotient_width+1)

    def input_at(self, element, index):
        a, q = element
        self.group.validate(a, jet=True)
        _canonical(q, self.group.quotient_width, self.algebra.p)
        if type(index) is not int or not 0 <= index < self.original_queries:
            raise ValueError("evaluation index outside public simplex design")
        y, scale = self.points[index]
        normal = self.group.evaluate(a, y, scale)
        quotient = tuple((yi+scale*qi) % self.algebra.p for yi, qi in zip(y, q))
        def embed(coefficients, basis):
            return tuple(sum(a*v[k] for a, v in zip(coefficients, basis)) % self.algebra.p
                         for k in range(self.algebra.dimension))
        left = embed(normal, self.certificate.normal_basis)
        right = embed(quotient, self.certificate.section_basis)
        return lie_bch(self.algebra, left, right, self.group.class_bound)

    def inputs(self, element):
        return tuple(self.input_at(element, i) for i in range(self.original_queries))

    def evaluate_fixture(self, original_oracle, element):
        """Classical diagnostic only; no claim of coherent oracle synthesis."""
        return tuple(original_oracle(x) for x in self.inputs(element))


def make_oracle_plan(algebra, ambient_basis):
    return LiftedOraclePlan(algebra, ambient_jet_certificate(algebra, ambient_basis))


def deterministic_resource_profile(weights, quotient_width, p):
    """One transverse image call, ideal SDE/gates, fixed class only."""
    ring(p)
    if (not weights or any(type(w) is not int or w < 2 for w in weights)
            or type(quotient_width) is not int or quotient_width < 1 or p <= max(weights)):
        raise ValueError("positive filtered dimensions and p>c required")
    m, c = quotient_width, max(weights)
    grades = {d: sum(comb(m+w-d, m) for w in weights if w >= d) for d in range(1, c+1)}
    arities = [sde_arity(d, grades[d]) for d in range(2, c+1) if grades[d]]
    samples = m+grades[1]+p.bit_length()+2
    lifted_calls = samples*prod(arities)
    width = comb(m+c, m+1)
    return {"p": p, "class_bound": c, "quotient_width": m,
            "jet_dimension": sum(grades.values()), "grade_dimensions": grades,
            "queries_per_lifted_oracle": width, "retained_original_label_registers": width,
            "alignment_retries": 0, "spectator_measurements": 0,
            "abelian_samples": samples,
            "original_queries_ceil_log2": (lifted_calls*width-1).bit_length(),
            "interpretation": "conditional sufficient single-image query upper bound, not runtime",
            "access": "ordinary coherent function oracle; not source-only access",
            "coherent_circuit_implemented": False, "general_sde_implemented": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    from theorems.right_abelian_induced_source import derived_length_three_witness
    profiles = []
    for p in (43, 2**127-1):
        algebra, basis, _ = derived_length_three_witness(p)
        plan = make_oracle_plan(algebra, basis)
        profiles.append(deterministic_resource_profile(plan.group.weights, plan.group.quotient_width, p))
    report = {"schema": "jet_oracle_homogenization_v1",
              "status": "public query compiler and provisional written oracle reduction",
              "profiles": profiles,
              "not_established": ["novelty", "whole quantum algorithm", "hard application",
                                  "coherent circuit refinement", "general SDE backend"],
              "hidden_potential_evaluated": False, "requires_transverse_hidden_subgroup": True}
    if args.write:
        path = Path(__file__).resolve().parents[1]/"research/reductions/jet_oracle_homogenization.json"
        path.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
