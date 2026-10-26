"""Copy-only polynomial-phase baseline derived from known SDE phase elimination.

Public classical controllers and a conditional copy envelope, NOT an executed
quantum learner or a new speedup. No hidden coefficients enter these APIs.
See research/POLYNOMIAL_PHASE_COPY_LEARNING_BASELINE.md.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
import json
from math import comb, prod
from pathlib import Path

from theorems.affine_phase_erasure import (
    PhasePacket, leading_columns, monomials, translate_combine,
)
from theorems.full_jet_resource_certificate import sde_arity
from theorems.prime_character_opi import ring
from theorems.ut5_matrix_phase_alignment import _canonical, _rank


def _parameters(p, width, degree):
    ring(p)
    if type(width) is not int or width < 1:
        raise ValueError("positive variable count required")
    if type(degree) is not int or not 1 <= degree < p:
        raise ValueError("fixed positive total degree strictly below prime required")


@dataclass(frozen=True)
class LearningFrame:
    """Public F=known+sum eta_j*basis_j, with global constant omitted.

    eta is never supplied here. Basis independence prevents a spurious
    parameter relation from being counted as progress.
    """
    p: int
    width: int
    degree: int
    known: tuple[int, ...]
    basis: tuple[tuple[int, ...], ...]

    def __post_init__(self):
        _parameters(self.p, self.width, self.degree)
        object.__setattr__(self, "known", tuple(self.known))
        object.__setattr__(self, "basis", tuple(tuple(v) for v in self.basis))
        count = comb(self.width+self.degree, self.degree)-1
        _canonical(self.known, count, self.p)
        for row in self.basis:
            _canonical(row, count, self.p)
        if _rank(self.basis, self.p) != len(self.basis):
            raise ValueError("independent public polynomial basis required")

    @property
    def indices(self):
        return tuple(a for a in monomials(self.width, self.degree) if any(a))

    @classmethod
    def initial(cls, p, width, degree):
        _parameters(p, width, degree)
        count = comb(width+degree, degree)-1
        return cls(p, width, degree, (0,)*count,
                   tuple(tuple(int(i == j) for j in range(count)) for i in range(count)))

    def next_axis(self):
        for row in self.basis:
            for alpha, value in zip(self.indices, row):
                if value:
                    return next(j for j, a in enumerate(alpha) if a)
        raise ValueError("no unknown parameters remain")

    def restrict(self, axis, observed):
        """One fresh copy, measuring all but axis; observed is NOT chosen input.

        Returns a known diagonal correction and a public univariate packet.
        Unknown constant terms are global phases, deliberately not recovered.
        """
        if not self.basis or type(axis) is not int or not 0 <= axis < self.width:
            raise ValueError("active frame and valid coordinate required")
        _canonical(observed, self.width-1, self.p)
        correction = [0]*(self.degree+1)
        rows = [[0]*len(self.basis) for _ in range(self.degree+1)]
        for column, alpha in enumerate(self.indices):
            factor = prod(pow(x, a, self.p) for x, a in
                          zip(observed, alpha[:axis]+alpha[axis+1:])) % self.p
            r = alpha[axis]
            correction[r] = (correction[r]+factor*self.known[column]) % self.p
            for j, basis in enumerate(self.basis):
                rows[r][j] = (rows[r][j]+factor*basis[column]) % self.p
        return tuple(correction), PhasePacket(
            self.p, 1, len(self.basis),
            {(r,): tuple(rows[r]) for r in range(1, self.degree+1)})

    def learn_relation(self, relation, observed_value):
        """Use one measured Fourier relation, not a supplied hidden parameter."""
        _canonical(relation, len(self.basis), self.p)
        _canonical((observed_value,), 1, self.p)
        if not any(relation):
            raise ValueError("zero relation supplies no information")
        pivot = next(j for j, value in enumerate(relation) if value)
        inv = pow(relation[pivot], -1, self.p)
        row = self.basis[pivot]
        known = tuple((x+observed_value*inv*y) % self.p for x, y in zip(self.known, row))
        basis = tuple(tuple((x-relation[j]*inv*y) % self.p for x, y in zip(v, row))
                      for j, v in enumerate(self.basis) if j != pivot)
        return LearningFrame(self.p, self.width, self.degree, known, basis)


def erase_line_degree(packets, scales, outcomes):
    """Check a supplied public SDE witness, then reuse the existing shear map.

    The general SDE search is a published dependency, not implemented here.
    A degree-zero returned packet is a failed attempt, never a learned row.
    """
    if not packets:
        raise ValueError("fresh source packets required")
    first = packets[0]
    degree = max(packet.degree for packet in packets)
    _parameters(first.p, first.width, degree)
    if first.width != 1 or degree < 2:
        raise ValueError("univariate degree at least two required")
    _canonical(scales, len(packets), first.p)
    if not any(scales):
        raise ValueError("nonzero public diagonal witness required")
    columns = leading_columns(packets, degree)
    if any(sum(pow(s, degree, first.p)*v[j] for s, v in zip(scales, columns)) % first.p
           for j in range(len(columns[0]))):
        raise ValueError("witness does not cancel leading coefficient map")
    result = translate_combine(packets, scales, outcomes)
    if result.degree >= degree:
        raise ArithmeticError("degree cancellation failed")
    return result


def copy_envelope(p, width, degree, error=Fraction(1, 3)):
    """Conservative expected/capped original-copy costs at FIXED degree.

    Local retries, not a large-p union bound. Markov's cap gets error/2;
    the other half remains for quantum gate/measurement approximations.
    No claim that the required general SDE/quantum backends are implemented.
    """
    _parameters(p, width, degree)
    if not isinstance(error, Fraction) or not 0 < error < 1:
        raise ValueError("exact error fraction in (0,1) required")
    count = comb(width+degree, degree)-1
    line_accept = Fraction(p-degree+1, p)
    expected = Fraction(count, 1)/line_accept
    arities = {}
    for r in range(2, degree+1):
        arities[r] = sde_arity(r, count)
        expected *= arities[r]*Fraction(p, p-1)
    cap = 2*expected/error
    return {
        "unknown_coefficients_mod_constant": count,
        "line_acceptance_lower_bound": line_accept,
        "merge_acceptance_lower_bound": Fraction(p-1, p),
        "sde_arities": arities,
        "expected_original_copies_upper_bound": expected,
        "original_copy_abort_cap": -(-cap.numerator//cap.denominator),
        "abort_probability_bound": error/2,
        "reserved_quantum_precision_budget": error/2,
    }


def report():
    profiles = []
    for p, width, degree in ((5, 2, 3), (101, 8, 3), (2**127-1, 8, 3)):
        budget = copy_envelope(p, width, degree)
        profiles.append({"prime": p, "variables": width, "degree": degree, **budget})
    return {
        "status": "KNOWN_TECHNIQUE_ADAPTATION_UNDER_REVIEW",
        "source": "fresh full-domain unknown Fp polynomial-phase copies; p>fixed degree",
        "baseline": "random coordinate restriction plus Ivanyos-Santha section 5 elimination",
        "decision": "do not promote this family as needing the Rees receiver",
        "classical_dequantization": False,
        "novelty_established": False,
        "quantum_learner_implemented": False,
        "general_sde_backend_implemented": False,
        "asymptotic_theorem_independently_verified": False,
        "global_constant_recoverable": False,
        "profiles": profiles,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    encoded = json.dumps(report(), indent=2,
                         default=lambda x: {"numerator": x.numerator, "denominator": x.denominator})
    if args.write:
        path = Path(__file__).resolve().parents[1]/"research/reductions/polynomial_phase_copy_learning.json"
        path.write_text(encoded+"\n")
    print(encoded)


if __name__ == "__main__":
    main()
