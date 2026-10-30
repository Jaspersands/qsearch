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
from math import comb, gcd, prod
from pathlib import Path
import random
from typing import Protocol, Sequence

from theorems.affine_phase_erasure import (
    PhasePacket, leading_columns, monomials, translate_combine,
)
from theorems.full_jet_resource_certificate import sde_arity
from theorems.prime_character_opi import ring
from theorems.ut5_matrix_phase_alignment import _basis, _canonical, _rank


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

    def coordinate_row_space(self, axis, power):
        """Image of original coefficients with alpha[axis]>=power in eta-space.

        A fixed-axis restriction/translation tree preserves these nested
        spaces. This checks public maps, not quantum-source provenance.
        """
        if type(axis) is not int or not 0 <= axis < self.width:
            raise ValueError("valid coordinate axis required")
        if type(power) is not int or not 1 <= power <= self.degree:
            raise ValueError("power between one and total degree required")
        if not self.basis:
            return ()
        rows = [tuple(row[i] for row in self.basis)
                for i, alpha in enumerate(self.indices) if alpha[axis] >= power]
        return tuple(map(tuple, _basis(rows, self.p)))

    def check_coordinate_packet(self, axis, packet):
        """Reject maps outside the fixed-axis coefficient filtration.

        Membership alone does not certify a legal physical preparation.
        Both the same frame and axis must be fixed for the whole tree.
        """
        self.coordinate_row_space(axis, 1)
        if (packet.p, packet.width, packet.parameter_count) != (self.p, 1, len(self.basis)):
            raise ValueError("packet and active learning frame are incompatible (frame mismatch)")
        if packet.degree > self.degree:
            raise ValueError("packet degree exceeds the learning frame")
        for (power,), row in packet.coefficients.items():
            space = self.coordinate_row_space(axis, power)
            if _rank([*space, row], self.p) != len(space):
                raise ValueError("packet violates the fixed-axis coefficient filtration")


def coordinate_rank_cap(width, degree, power):
    """Count alpha with |alpha|<=degree and alpha[axis]>=power."""
    if (type(width) is not int or width < 1 or type(degree) is not int or degree < 1
            or type(power) is not int or not 1 <= power <= degree):
        raise ValueError("positive width and power between one and degree required")
    return comb(width+degree-power, degree-power)


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


def coordinate_copy_envelope(p, width, degree, error=Fraction(1, 3), *,
                             construction="published"):
    """Fixed-axis source envelope; NOT an executed receiver or total clock.

    Uses published SDE arities by default. The symmetric alternative has
    its separate large-field guard. As with copy_envelope, solver runtime
    and abort allocation must be supplied separately; do not treat this
    source-only cap as a complete error/resource certificate.
    """
    _parameters(p, width, degree)
    if not isinstance(error, Fraction) or not 0 < error < 1:
        raise ValueError("exact error fraction in (0,1) required")
    if construction not in ("published", "symmetric"):
        raise ValueError("unknown SDE construction")
    count = comb(width+degree, degree)-1
    ranks = {r: coordinate_rank_cap(width, degree, r) for r in range(2, degree+1)}
    arities = {}
    for r, rank in ranks.items():
        if construction == "published":
            arities[r] = sde_arity(r, rank)
        else:
            from theorems.power_sde import power_arity, validate_family
            reduced = gcd(r, p-1)
            if reduced == 1:
                arities[r] = rank+1
            else:
                validate_family(p, reduced)
                arities[r] = power_arity(rank, reduced)
    line_accept = Fraction(p-degree+1, p)
    expected = Fraction(count, 1)/line_accept
    for arity in arities.values():
        expected *= arity*Fraction(p, p-1)
    cap = 2*expected/error
    return {
        "construction": construction,
        "fixed_axis_per_tree_required": True,
        "fresh_frame_per_learning_round_required": True,
        "unknown_coefficients_mod_constant": count,
        "coordinate_rank_caps": ranks,
        "sde_arities": arities,
        "line_acceptance_lower_bound": line_accept,
        "merge_acceptance_lower_bound": Fraction(p-1, p),
        "expected_original_copies_upper_bound": expected,
        "original_copy_abort_cap": -(-cap.numerator//cap.denominator),
        "source_abort_probability_bound": error/2,
        "reserved_quantum_precision_budget": error/2,
        "arithmetic_failure_budget_included": False,
        "quantum_learner_implemented": False,
    }


class SourceCapExhausted(RuntimeError):
    """Raised when the original-copy draw cap is exhausted."""


class PhaseCopySource(Protocol):
    """Protocol for an opaque quantum source of unknown polynomial-phase states.

    The controller receives ONLY opaque handle IDs and public measurement outcomes.
    No hidden coefficients, value oracles, or state vectors enter the controller.
    """

    @property
    def fourier_convention(self) -> int:
        ...

    def draw(self) -> int:
        ...

    def measure_all_but(self, handle_id: int, axis: int) -> tuple[tuple[int, ...], int]:
        ...

    def apply_known_phase(self, handle_id: int, correction: tuple[int, ...]) -> int:
        ...

    def shear_merge(
        self,
        handle_ids: Sequence[int],
        scales: Sequence[int],
    ) -> tuple[tuple[tuple[int], ...], int]:
        ...

    def fourier_measure(self, handle_id: int) -> int:
        ...


@dataclass
class CopyLedger:
    drawn: int = 0
    discarded_slices: int = 0
    zero_scale_consumed: int = 0
    failed_merges: int = 0
    used_in_relations: int = 0
    aborted_leaves: int = 0
    solver_calls: int = 0
    max_solver_bits: int = 0

    def check_balance(self) -> None:
        accounted = (self.discarded_slices + self.zero_scale_consumed +
                     self.failed_merges + self.used_in_relations + self.aborted_leaves)
        if self.drawn != accounted:
            raise ArithmeticError(
                f"copy ledger imbalance: drawn={self.drawn} != accounted={accounted} "
                f"(discarded={self.discarded_slices}, zero_scale={self.zero_scale_consumed}, "
                f"failed_merges={self.failed_merges}, used={self.used_in_relations}, "
                f"aborted={self.aborted_leaves})"
            )


@dataclass(frozen=True)
class ControllerBudget:
    p: int
    width: int
    degree: int
    total_error: Fraction
    source_abort_bound: Fraction
    solver_abort_bound: Fraction
    reserved_quantum_precision: Fraction
    expected_copies: Fraction
    copy_cap: int
    solver_bits: int

    @classmethod
    def compute(
        cls,
        p: int,
        width: int,
        degree: int,
        error: Fraction = Fraction(1, 3),
        *,
        construction: str = "symmetric",
    ) -> ControllerBudget:
        _parameters(p, width, degree)
        if not isinstance(error, Fraction) or not 0 < error < 1:
            raise ValueError("exact error fraction in (0, 1) required")
        env = coordinate_copy_envelope(p, width, degree, error=error, construction=construction)
        expected = env["expected_original_copies_upper_bound"]
        # Markov's inequality: P(draws >= cap) <= expected / cap <= error / 3
        cap_fraction = 3 * expected / error
        cap = -(-cap_fraction.numerator // cap_fraction.denominator)

        # Union bound over all merge nodes in the tree:
        # Since each merge node has >= 2 children, total merge nodes across the entire
        # learning process is strictly bounded by the total number of drawn leaves <= cap.
        # We need total solver abort <= cap * 2^(-solver_bits) <= error / 3.
        ratio = 3 * cap / error
        solver_bits = (int(ratio.numerator // ratio.denominator) + 1).bit_length()
        solver_bits = max(solver_bits, 16)
        assert Fraction(expected, cap) <= error / 3
        assert Fraction(cap, 1 << solver_bits) <= error / 3

        return cls(
            p=p,
            width=width,
            degree=degree,
            total_error=error,
            source_abort_bound=error / 3,
            solver_abort_bound=error / 3,
            reserved_quantum_precision=error / 3,
            expected_copies=expected,
            copy_cap=cap,
            solver_bits=solver_bits,
        )


@dataclass(frozen=True)
class LearnResult:
    status: str
    known: tuple[int, ...]
    ledger: CopyLedger
    budget: ControllerBudget
    reason: str | None = None


class PhaseCopyController:
    """Instrument controller for learning unknown polynomial-phase states.

    Receives ONLY opaque state handles and public measurement outcomes.
    Charges every original copy against the budget ledger.
    Fixes both frame and coordinate axis for each entire tree.
    """

    def __init__(
        self,
        p: int,
        width: int,
        degree: int,
        source: PhaseCopySource,
        *,
        error: Fraction = Fraction(1, 3),
        construction: str = "symmetric",
        rng: random.Random | None = None,
    ):
        _parameters(p, width, degree)
        if construction != "symmetric":
            raise ValueError("only certified symmetric construction is currently supported")
        # In symmetric regime, degree-2 erasure has reduced degree g = gcd(2, p-1) = 2.
        # Certified field threshold for g=2: 16 * 2^6 = 1024.
        if p < 1024:
            raise ValueError(f"prime {p} is below certified symmetric threshold p >= 1024")

        self.p = p
        self.width = width
        self.degree = degree
        self.source = source
        self.budget = ControllerBudget.compute(p, width, degree, error=error, construction=construction)
        self.ledger = CopyLedger()
        self.rng = rng if rng is not None else random.Random()

    def learn(self) -> LearnResult:
        frame = LearningFrame.initial(self.p, self.width, self.degree)
        try:
            while frame.basis:
                axis = frame.next_axis()
                tree_id = object()
                hid, pkt, count = self._produce(frame, axis, tree_id, target=1)
                meas = self.source.fourier_measure(hid)
                relation_val = (meas * self.source.fourier_convention) % self.p
                relation = pkt.coefficients[(1,)]
                self.ledger.used_in_relations += count
                frame = frame.learn_relation(relation, relation_val)
        except SourceCapExhausted as exc:
            accounted = (self.ledger.discarded_slices + self.ledger.zero_scale_consumed +
                         self.ledger.failed_merges + self.ledger.used_in_relations)
            self.ledger.aborted_leaves += self.ledger.drawn - accounted
            self.ledger.check_balance()
            return LearnResult("ABORT", frame.known, self.ledger, self.budget, reason=str(exc))
        except RuntimeError as exc:
            if "exhausted" in str(exc) or "budget" in str(exc):
                accounted = (self.ledger.discarded_slices + self.ledger.zero_scale_consumed +
                             self.ledger.failed_merges + self.ledger.used_in_relations)
                self.ledger.aborted_leaves += self.ledger.drawn - accounted
                self.ledger.check_balance()
                return LearnResult("ABORT", frame.known, self.ledger, self.budget, reason=str(exc))
            raise

        self.ledger.check_balance()
        return LearnResult("OK", frame.known, self.ledger, self.budget)

    def _produce(
        self,
        frame: LearningFrame,
        axis: int,
        tree_id: object,
        target: int,
    ) -> tuple[int, PhasePacket, int]:
        powers = [alpha[axis] for row in frame.basis for alpha, val in zip(frame.indices, row)
                  if val and alpha[axis] > 0]
        max_d = max(powers, default=0)
        if target >= max_d:
            while True:
                if self.ledger.drawn >= self.budget.copy_cap:
                    raise SourceCapExhausted("controller original-copy cap exhausted")
                hid = self.source.draw()
                self.ledger.drawn += 1
                observed, hid = self.source.measure_all_but(hid, axis)
                correction, packet = frame.restrict(axis, observed)
                hid = self.source.apply_known_phase(hid, correction)
                if packet.degree == 0:
                    self.ledger.discarded_slices += 1
                    continue
                frame.check_coordinate_packet(axis, packet)
                return hid, packet, 1

        D = target + 1
        rank_cap = coordinate_rank_cap(self.width, self.degree, D)
        g = gcd(D, self.p - 1)
        if g == 1:
            M = rank_cap + 1
        else:
            from theorems.power_sde import power_arity
            M = power_arity(rank_cap, g)

        while True:
            children = [self._produce(frame, axis, tree_id, D) for _ in range(M)]
            packets = [c[1] for c in children]
            for pkt in packets:
                frame.check_coordinate_packet(axis, pkt)
            lower = next((i for i, pkt in enumerate(packets) if pkt.degree <= target), None)
            if lower is not None:
                scales = [int(i == lower) for i in range(M)]
                outcomes, merged_hid = self.source.shear_merge([c[0] for c in children], scales)
                merged_pkt = translate_combine(packets, scales, outcomes)
                for i, child in enumerate(children):
                    if i != lower:
                        self.ledger.zero_scale_consumed += child[2]
                if merged_pkt.degree == 0:
                    self.ledger.failed_merges += children[lower][2]
                    continue
                frame.check_coordinate_packet(axis, merged_pkt)
                return merged_hid, merged_pkt, children[lower][2]

            # Every child now has a nonzero degree-D map. A nonzero witness
            # therefore activates a leading row, as the merge-success proof needs.
            curr_d = max(p.degree for p in packets)
            columns = leading_columns(packets, curr_d)
            self.ledger.solver_calls += 1
            self.ledger.max_solver_bits = max(self.ledger.max_solver_bits, self.budget.solver_bits)

            from theorems.weighted_two_erasure_cascade import solve_bezout_sde_weights
            weights, rank, reduced_g, u = solve_bezout_sde_weights(
                self.p, columns, curr_d, rng=self.rng, bounded_randomness_bits=self.budget.solver_bits
            )

            active_leaf_count = 0
            for w, c in zip(weights, children):
                if w % self.p == 0:
                    self.ledger.zero_scale_consumed += c[2]
                else:
                    active_leaf_count += c[2]

            outcomes, merged_hid = self.source.shear_merge([c[0] for c in children], weights)
            merged_pkt = erase_line_degree(packets, weights, outcomes)

            if merged_pkt.degree == 0:
                self.ledger.failed_merges += active_leaf_count
                continue

            frame.check_coordinate_packet(axis, merged_pkt)
            return merged_hid, merged_pkt, active_leaf_count


def report():
    profiles = []
    for p, width, degree in ((5, 2, 3), (101, 8, 3), (2**127-1, 8, 3)):
        budget = copy_envelope(p, width, degree)
        profiles.append({"prime": p, "variables": width, "degree": degree, **budget})
    coordinate_profiles = []
    for p, width, degree, construction in ((5, 2, 3, "published"),
                                          (101, 8, 3, "published"),
                                          (2**127-1, 8, 3, "symmetric"),
                                          (2**127-1, 8, 5, "symmetric")):
        coordinate_profiles.append({"prime": p, "variables": width, "degree": degree,
                                    **coordinate_copy_envelope(p, width, degree,
                                                               construction=construction)})
    return {
        "status": "KNOWN_TECHNIQUE_ADAPTATION_UNDER_REVIEW",
        "source": "fresh full-domain unknown Fp polynomial-phase copies; p>fixed degree",
        "baseline": "random coordinate restriction plus Ivanyos-Santha section 5 elimination",
        "decision": "do not promote this family as needing the Rees receiver",
        "classical_dequantization": False,
        "novelty_established": False,
        "quantum_learner_implemented": False,
        "bounded_controller_implemented": True,
        "controller_backend": "finite_statevector_fixture_only",
        "general_sde_backend_implemented": False,
        "asymptotic_theorem_independently_verified": False,
        "global_constant_recoverable": False,
        "profiles": profiles,
        "coordinate_profiles": coordinate_profiles,
        "coordinate_rank_bound_independently_reviewed": True,
        "optimal_copy_complexity_established": False,
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
