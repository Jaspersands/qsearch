"""Public section composition and whole-recursion resource contracts.

No hidden subgroup or ideal image oracle is an operational input here.
This does not implement the quantum image decoder or the general SDE.
See research/RECURSIVE_JET_RECOVERY.md for the conditional theorem.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
import json
from math import comb
from pathlib import Path

from theorems.central_character_descent import tree_budget
from theorems.full_jet_resource_certificate import sde_arity
from theorems.nil3_complete_budget import ceil_log
from theorems.prime_character_opi import ring


def _check_prime(p):
    # The abelian base case also permits F_2; the shared character ring is odd-only.
    if not (type(p) is int and p == 2):
        ring(p)


@dataclass(frozen=True)
class PublicLinearSection:
    """Public linear representative map; NOT asserted a group homomorphism.

The i-th basis vector is the output of the i-th input unit vector. An
external quotient theorem must establish that its kernel lies in H.
Explicit output width also represents the zero-dimensional input correctly.
"""
    p: int
    output_width: int
    basis: tuple[tuple[int, ...], ...]

    def __post_init__(self):
        _check_prime(self.p)
        if type(self.output_width) is not int or self.output_width < 0:
            raise ValueError("nonnegative output width required")
        basis = tuple(tuple(v) for v in self.basis)
        if any(len(v) != self.output_width or any(type(x) is not int or not 0 <= x < self.p for x in v)
               for v in basis):
            raise ValueError("canonical public basis coordinates required")
        object.__setattr__(self, "basis", basis)

    @property
    def input_width(self):
        return len(self.basis)

    def apply(self, vector):
        if len(vector) != self.input_width or any(type(x) is not int or not 0 <= x < self.p for x in vector):
            raise ValueError("canonical input coordinates required")
        return tuple(sum(a*v[j] for a, v in zip(vector, self.basis)) % self.p for j in range(self.output_width))

    def then(self, outer):
        """Flatten two public sections; no oracle evaluation or label copying."""
        if self.p != outer.p or self.output_width != outer.input_width:
            raise ValueError("section field/dimension mismatch")
        return PublicLinearSection(self.p, outer.output_width, tuple(outer.apply(v) for v in self.basis))

    def evaluate_fixture(self, original_oracle, vector):
        """Classical one-query control, not synthesized coherent software."""
        return original_oracle(self.apply(vector))


def recursion_call_envelope(class_bound):
    """All branches must enforce class-drop and recursively halve class."""
    if type(class_bound) is not int or class_bound < 0:
        raise ValueError("nonnegative class bound required")
    if class_bound == 0:
        return {"intersection_classes": (), "image_calls": 0, "abelian_calls": 0, "total_calls": 0}
    classes = []
    c = class_bound
    while c:
        classes.append(c)
        c //= 2
    images = sum(c-1 for c in classes)
    return {"intersection_classes": tuple(classes), "image_calls": images,
            "abelian_calls": len(classes), "total_calls": images+len(classes)}


def whole_recovery_budget(n, c, p, error=Fraction(1, 3)):
    """Dimension-uniform envelope for the entire proposed algorithm.

Every ORIGINAL recursive ambient has dimension<=n. Lifted jet groups are
internal image workspaces, never fed into another arbitrary-H recursion.
The complete-instrument errors are not elementary-gate error estimates.
"""
    _check_prime(p)
    if type(n) is not int or n < 1 or type(c) is not int or not 1 <= c < p:
        raise ValueError("positive dimension and 1<=class<p required")
    if not isinstance(error, Fraction) or not 0 < error < 1:
        raise ValueError("exact error Fraction in (0,1) required")
    calls = recursion_call_envelope(c)
    R = calls["total_calls"]
    slack = ceil_log(p, 3*R/error)
    abelian_samples = n+slack
    if c == 1:
        ranks, arities, width, final_dimension = {}, (), 0, n
    else:
        ranks = {d: n*comb(n+c-d, c-d) for d in range(1, c+1)}
        arities = tuple(sde_arity(d, ranks[d]) for d in range(c, 1, -1))
        width = comb(n+c, c-1)
        final_dimension = n+ranks[1]
    samples = final_dimension+slack
    tree = tree_budget(arities)
    images, bases = calls["image_calls"], calls["abelian_calls"]
    image_leaves = samples*tree["source_leaves"]
    sde_calls = images*samples*sum(tree["stage_calls"])
    leaf_calls = images*image_leaves+bases*abelian_samples
    instrument_calls = leaf_calls+sde_calls
    original_queries = images*image_leaves*width+bases*abelian_samples
    rank_error = Fraction(R, (p-1)*p**slack)
    return {**calls, "dimension_bound": n, "class_bound": c, "prime": p,
            "central_rank_bounds": ranks, "stage_arities_top_down": arities,
            "tuple_queries_per_leaf_bound": width, "terminal_dimension_bound": final_dimension,
            "rank_slack": slack, "image_fourier_samples": samples,
            "base_fourier_samples": abelian_samples, "source_preparations": leaf_calls,
            "sde_calls": sde_calls, "complete_instrument_calls": instrument_calls,
            "original_queries": original_queries, "rank_failure_bound": rank_error,
            "solver_abort_per_call": error/(3*sde_calls) if sde_calls else Fraction(0),
            "instrument_error_per_call": error/(3*instrument_calls),
            "total_error_bound": rank_error+(error/3 if sde_calls else 0)+error/3,
            "query_dimension_exponent": (2*c-1+sum(d*d.bit_length()*(c-d+1) for d in range(2, c+1)))
                                        if c > 1 else 1}


def report_profile(n, c, p):
    raw = whole_recovery_budget(n, c, p)
    return {key: raw[key] for key in ("dimension_bound", "class_bound", "prime", "intersection_classes",
                                     "image_calls", "abelian_calls", "total_calls", "query_dimension_exponent")} | {
        "original_queries_ceil_log2": (raw["original_queries"]-1).bit_length(),
        "sde_calls_ceil_log2": (raw["sde_calls"]-1).bit_length() if raw["sde_calls"] else 0,
        "per_instrument_error_bits": ceil_log(2, 1/raw["instrument_error_per_call"]),
        "rank_failure_bound": str(raw["rank_failure_bound"]),
        "total_error_bound": str(raw["total_error_bound"]),
        "interpretation": "loose conditional whole-recovery upper bound, not time or executed performance"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = {"status": "provisional_fixed_class_Lazard_HSP_composition_not_discovery",
              "profiles": [report_profile(19, 9, p) for p in (43, 2**127-1)],
              "input_model": "explicit F_p Lie structure constants, fixed class c<p, coherent ordinary hiding function",
              "formal_module": "formal/Formal/RecursiveOracleReduction.lean",
              "research_note": "research/RECURSIVE_JET_RECOVERY.md",
              "coherent_receiver_implemented": False, "general_sde_implemented": False,
              "independent_correctness_or_novelty_review": False, "speedup_claim_allowed": False}
    if args.write:
        path = Path(__file__).resolve().parents[1]/"research/reductions/recursive_jet_recovery.json"
        path.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
