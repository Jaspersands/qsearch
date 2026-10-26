"""Public zero-moment Rees designs for copy-only scalar-support symmetry.

Exact classical design compilation and source budgets, not a quantum receiver.
A verified scalar Fermat backend completes the odd/quadratic fast paths.
This is not the receiver's general many-equation diagonal solver.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
import json
from math import factorial, gcd
from pathlib import Path
import random

from flint import fmpz

from theorems.rees_hsp_reduction import recovery_budget
from theorems.state_symmetry_coset_transfer import plan_orbit_state_transfer
from theorems.scalar_fermat_solver import scalar_fermat_witness


def _parameters(p, degree):
    if type(p) is not int or p <= 2 or not fmpz(p).is_prime():
        raise ValueError("odd prime required")
    if type(degree) is not int or not 1 <= degree < p:
        raise ValueError("positive class bound strictly below p required")


@dataclass(frozen=True)
class MomentDesign:
    p: int
    degree: int
    points: tuple[int, ...]
    method: str

    def __post_init__(self):
        _parameters(self.p, self.degree)
        object.__setattr__(self, "points", tuple(self.points))
        if not self.points or any(type(s) is not int or not 0 < s < self.p for s in self.points):
            raise ValueError("nonempty nonzero canonical evaluation multiset required")
        if len(self.points) > factorial(self.degree+1):
            raise ValueError("design exceeds the prime-independent fixed-class copy cap")
        if len(set(self.points)) < self.degree:
            raise ValueError("at least c distinct points are needed to separate coefficients")
        if any(self.moments):
            raise ValueError("unknown character is not erased: nonzero power moment")

    @property
    def moments(self):
        return tuple(sum(pow(s, r, self.p) for s in self.points) % self.p
                     for r in range(1, self.degree+1))

    @property
    def copies_per_block(self):
        # Equal points still require distinct fresh physical copies.
        return len(self.points)

    def inputs(self, cover, vector):
        if cover.p != self.p or cover.class_bound != self.degree:
            raise ValueError("design and Rees cover disagree")
        return tuple(cover.evaluate(vector, s) for s in self.points)


def design_from_scalar_rows(p, degree, rows):
    """Multiply certified Fermat solutions; no state or hidden subgroup input.

    Row r has at most r+1 entries, is nonzero, and sum x_i**r=0.
    The multiplicative convolution kills all moments through c. The row
    size bound is essential to the automatic Vandermonde coverage proof.
    """
    _parameters(p, degree)
    if len(rows) != degree:
        raise ValueError("one scalar certificate for each degree required")
    points = (1,)
    for r, row in enumerate(rows, 1):
        if not 1 <= len(row) <= r+1 or any(type(x) is not int or not 0 <= x < p for x in row):
            raise ValueError("canonical scalar row of length at most r+1 required")
        active = tuple(x for x in row if x)
        if not active or sum(pow(x, r, p) for x in active) % p:
            raise ValueError("invalid nonzero scalar diagonal certificate")
        points = tuple(x*y % p for x in points for y in active)
    if len(points) > factorial(degree+1):
        raise ArithmeticError("fixed-class copy cap exceeded")
    return MomentDesign(p, degree, points, "scalar_certificate_multiplicative_convolution")


def _prime_divisors(n):
    # n is the explicitly capped small order, never the large integer p-1.
    result, d = [], 2
    while d*d <= n:
        if n % d == 0:
            result.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        result.append(n)
    return result


def find_moment_design(p, degree, *, max_order=64, max_trials=128, rng=None):
    """Capped fast paths followed by the verified scalar Fermat backend.

    General existence uses the scalar diagonal algorithm cited in the note.
    Large primes are not enumerated. The scalar backend has a separately
    proved degree-bounded small-field path. Seeded rng reproduces diagnostics.
    """
    _parameters(p, degree)
    if any(type(x) is not int or x < 1 for x in (max_order, max_trials)):
        raise ValueError("positive public search caps required")
    rng = random.SystemRandom() if rng is None else rng
    order_cap = min(max_order, factorial(degree+1))
    order = next((m for m in range(degree+1, order_cap+1) if (p-1) % m == 0), None)
    if order is not None:
        divisors = _prime_divisors(order)
        for _ in range(max_trials):
            root = pow(rng.randrange(1, p), (p-1)//order, p)
            if all(pow(root, order//q, p) != 1 for q in divisors):
                return MomentDesign(p, degree, tuple(pow(root, j, p) for j in range(order)),
                                    "verified_small_cyclic_subgroup")
    rows, quadratic = [], None
    for r in range(1, degree+1):
        if r % 2:
            rows.append((1, p-1))
            continue
        if gcd(r, p-1) != 2:
            rows.append(scalar_fermat_witness(p, r, max_trials=max_trials, rng=rng).weights)
            continue
        if quadratic is None:
            for _ in range(max_trials):
                a = rng.randrange(p)
                value = (-1-a*a) % p
                if value == 0 or pow(value, (p-1)//2, p) == 1:
                    quadratic = (a, int(fmpz(value).sqrtmod(p)), 1)
                    break
            if quadratic is None:
                raise RuntimeError("capped quadratic search aborted")
        modulus = (p-1)//2
        exponent = pow(r//2, -1, modulus) if modulus > 1 else 1
        rows.append(tuple(pow(x, exponent, p) for x in quadratic))
    return design_from_scalar_rows(p, degree, rows)


def projective_source_budget(cover, design, gap, error=Fraction(1, 3)):
    """Whole Rees leaf budget, conditional on the receiver and gap promise.

    Each prepared leaf consumes M*k IID copies and controlled actions.
    No ordinary f, conjugate copies, or preparation inverse are supplied.
    """
    if design.p != cover.p or design.degree != cover.class_bound:
        raise ValueError("design and Rees cover disagree")
    if not isinstance(error, Fraction) or not 0 < error < 1:
        raise ValueError("exact total error in (0,1) required")
    receiver = recovery_budget(cover, error/2)
    leaves = receiver["source_preparations"]
    transfer = plan_orbit_state_transfer(cover.p**cover.dimension, gap, leaves, error)
    copies = design.copies_per_block*transfer.copies_per_label*leaves
    total_error = receiver["total_error_bound"]+transfer.hybrid_error_bound+error/4
    if total_error > error:
        raise ArithmeticError("whole-run error budget exceeded")
    return {
        "source_leaves": leaves, "design_copies_per_block": design.copies_per_block,
        "blocks_per_leaf": transfer.copies_per_label,
        "copies_per_leaf": design.copies_per_block*transfer.copies_per_label,
        "total_fresh_copies": copies, "total_controlled_action_calls": copies,
        "receiver_error_bound": receiver["total_error_bound"],
        "source_replacement_error_bound": transfer.hybrid_error_bound,
        "copy_and_action_error_per_use": error/(4*copies),
        "total_error_bound": total_error,
        "ordinary_hiding_oracle_required": False,
        "conjugate_state_required": False, "preparation_inverse_required": False,
        "iid_copies_required": True, "controlled_linear_action_required": True,
        "gap_is_supplied_not_certified": True, "quantum_receiver_implemented": False,
        "mixed_conjugation_symmetry_covered": False, "speedup_claim_allowed": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    from theorems.rees_hsp_reduction import make_rees_cover
    from theorems.right_abelian_induced_source import derived_length_three_witness
    rows = []
    for p in (43, 2**127-1):
        design = find_moment_design(p, 9, rng=random.Random(1729))
        rows.append({"p": p, "class": 9, "method": design.method,
                     "copies_per_block": design.copies_per_block, "moments": design.moments,
                     "distinct_points": len(set(design.points))})
    for p in (13, 2**128-275):
        design = find_moment_design(p, 4, max_order=4, rng=random.Random(19))
        rows.append({"p": p, "class": 4, "method": design.method,
                     "copies_per_block": design.copies_per_block, "moments": design.moments,
                     "distinct_points": len(set(design.points)), "small_cyclic_fast_path_disabled": True})
    algebra, ambient, *_ = derived_length_three_witness(43)
    cover = make_rees_cover(algebra, ambient)
    design = find_moment_design(43, 9, rng=random.Random(1729))
    budget = projective_source_budget(cover, design, Fraction(1, 10))
    report = {"status": "proposed_copy_only_projective_Rees_source_not_discovery",
              "design_controls": rows, "profile": {
                  "cover_dimension": cover.dimension,
                  "hypothetical_gap": "1/10, not a measured state-family promise",
                  "blocks_per_leaf": budget["blocks_per_leaf"],
                  "total_fresh_copies_ceil_log2": (budget["total_fresh_copies"]-1).bit_length(),
                  "total_error_bound": str(budget["total_error_bound"])},
              "access_and_status": {k: v for k, v in budget.items() if type(v) is bool},
              "scalar_fermat_backend_implemented": True,
              "general_many_equation_sde_backend_implemented": False,
              "independent_review": False, "novelty_established": False,
              "formal_compiler_checked": False, "natural_hard_state_family_established": False,
              "research_note": "research/REES_PROJECTIVE_STATE_SOURCE.md"}
    if args.write:
        path = Path(__file__).resolve().parents[1]/"research/reductions/rees_projective_source.json"
        path.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
