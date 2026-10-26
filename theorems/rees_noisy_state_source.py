"""Costed streaming purification before the proposed copy-only Rees receiver.

The SWAP purification protocol is prior art. This module implements exact
resource bounds and an opaque-token controller, NOT physical quantum gates
or a hidden-subgroup receiver. The target is the principal eigenstate.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
import json
from pathlib import Path

from theorems.nil3_complete_budget import ceil_log
from theorems.rees_projective_source import projective_source_budget


def _fraction(value, name, upper=Fraction(1)):
    if not isinstance(value, Fraction) or not 0 < value <= upper:
        raise ValueError(f"{name}: exact positive Fraction <= {upper} required")


def _integer(value, name, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name}: integer >= {minimum} required")


def _ceil(value):
    return -(-value.numerator//value.denominator)


@dataclass(frozen=True)
class PurificationPlan:
    spectral_gap: Fraction
    output_error: Fraction
    outputs: int
    abort_budget: Fraction

    def __post_init__(self):
        _fraction(self.spectral_gap, "principal spectral gap")
        _fraction(self.output_error, "single-output trace error", Fraction(1, 8))
        _integer(self.outputs, "outputs", 1)
        _fraction(self.abort_budget, "whole-stream abort budget", Fraction(1, 2))

    @property
    def burn_in(self):
        ratio = max(Fraction(1), 7*(1-self.spectral_gap)/self.spectral_gap)
        bits = ceil_log(2, ratio)
        return _ceil(Fraction(2*bits)/self.spectral_gap)

    @property
    def tail_levels(self):
        return ceil_log(2, 1/self.output_error)

    @property
    def depth(self):
        return self.burn_in+self.tail_levels

    @property
    def trace_error_bound(self):
        return Fraction(1, 2**(self.tail_levels+1))

    @property
    def expected_raw_per_output_bound(self):
        return 2**(2*self.burn_in+self.tail_levels+1)

    @property
    def expected_total_raw_bound(self):
        return self.outputs*self.expected_raw_per_output_bound

    @property
    def raw_copy_cap(self):
        # One GLOBAL clock avoids multiplying a per-node retry cap by depth.
        return _ceil(Fraction(self.expected_total_raw_bound)/self.abort_budget)

    @property
    def abort_probability_bound(self):
        return Fraction(self.expected_total_raw_bound, self.raw_copy_cap)


def capped_purification_stream(depth, outputs, raw_copy_cap, *, acquire,
                               symmetric_merge, consume, discard):
    """Execute only herald/ownership control using backend-owned opaque tokens.

    acquire supplies a fresh IID copy. symmetric_merge consumes BOTH inputs
    and returns one retained output on the symmetric branch, None otherwise.
    consume/discard take ownership. No state, eigenvector or subgroup is read.
    Physical validity and instrument precision are separate backend obligations.
    """
    _integer(depth, "depth")
    _integer(outputs, "outputs", 1)
    _integer(raw_copy_cap, "raw copy cap", 1)
    stack = []
    raw = merges = delivered = peak = 0
    try:
        while delivered < outputs:
            if raw == raw_copy_cap:
                break
            state = acquire()
            raw += 1
            if state is None:
                raise ValueError("acquire returned the reserved rejection token")
            stack.append((0, state))
            peak = max(peak, len(stack))
            while len(stack) >= 2 and stack[-1][0] == stack[-2][0]:
                level, right = stack.pop()
                _, left = stack.pop()
                merges += 1
                retained = symmetric_merge(left, right)
                if retained is not None:
                    stack.append((level+1, retained))
            if stack and stack[-1][0] == depth:
                _, state = stack.pop()
                consume(state)
                delivered += 1
        return {"status": "complete" if delivered == outputs else "abort_raw_copy_cap",
                "raw_copies": raw, "swap_tests": merges, "delivered_outputs": delivered,
                "peak_live_input_registers": peak}
    finally:
        for _, state in stack:
            discard(state)


def noisy_rees_budget(cover, design, target_overlap_gap, spectral_gap,
                      error=Fraction(1, 3)):
    """Compose two DISTINCT promises: target orbit gap and input spectral gap.

    Error is unconditional, including aborts and all purification records.
    No promise that purification restores an arbitrary pre-noise state.
    """
    _fraction(error, "total error", Fraction(1, 2))
    ideal = projective_source_budget(cover, design, target_overlap_gap, error/2)
    copies = ideal["total_fresh_copies"]
    plan = PurificationPlan(spectral_gap, error/(8*copies), copies, error/8)
    terms = {
        "ideal_receiver_bound": ideal["total_error_bound"],
        "purified_input_replacement_bound": copies*plan.trace_error_bound,
        "global_cap_abort_bound": plan.abort_probability_bound,
        "purifier_complete_instrument_reserved": error/8,
    }
    total_error = sum(terms.values())
    if total_error > error:
        raise ArithmeticError("complete noisy-source budget exceeded")
    return {
        "ideal_target_copies": copies, "purification_depth": plan.depth,
        "burn_in_levels": plan.burn_in, "tail_levels": plan.tail_levels,
        "purified_copy_trace_error_bound": plan.trace_error_bound,
        "expected_total_raw_copies_bound": plan.expected_total_raw_bound,
        "raw_copy_cap": plan.raw_copy_cap, "swap_test_call_cap": plan.raw_copy_cap,
        "purifier_live_register_cap": plan.depth+1,
        "purifier_extra_ancilla_qubits": 1,
        "source_or_swap_instrument_error_per_call": error/(16*plan.raw_copy_cap),
        "failure_terms": terms, "total_error_bound": total_error,
        "spectral_gap_is_supplied_not_certified": True,
        "target_orbit_gap_is_supplied_not_certified": True,
        "target_is_principal_eigenstate": True, "iid_raw_copies_required": True,
        "purifier_herald_controller_implemented": True,
        "purifier_quantum_backend_implemented": False, "quantum_receiver_implemented": False,
        "arbitrary_noise_correction": False, "mixed_state_conjugation_covered": False,
        "preparation_inverse_required": False, "conjugate_state_required": False,
        "efficient_for_arbitrary_vanishing_spectral_gap": False,
        "novel_purification_protocol": False, "speedup_claim_allowed": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    import random
    from theorems.rees_hsp_reduction import make_rees_cover
    from theorems.rees_projective_source import find_moment_design
    from theorems.right_abelian_induced_source import derived_length_three_witness
    algebra, ambient, *_ = derived_length_three_witness(43)
    cover = make_rees_cover(algebra, ambient)
    design = find_moment_design(43, 9, rng=random.Random(1729))
    budget = noisy_rees_budget(cover, design, Fraction(1, 10), Fraction(3, 4))
    profile = {key: budget[key] for key in (
        "purification_depth", "burn_in_levels", "tail_levels", "purifier_live_register_cap")}
    for key in ("ideal_target_copies", "expected_total_raw_copies_bound", "raw_copy_cap"):
        profile[key+"_ceil_log2"] = (budget[key]-1).bit_length()
    profile["hypothetical_target_orbit_gap"] = "1/10, not measured or certified"
    profile["hypothetical_input_spectral_gap"] = "3/4, e.g. global depolarization <=1/4"
    profile["total_error_within_one_third"] = budget["total_error_bound"] <= Fraction(1, 3)
    report = {
        "status": "known_purification_composed_with_unreviewed_Rees_receiver",
        "profile": profile,
        "scope": {key: value for key, value in budget.items() if type(value) is bool},
        "independent_review": False, "formal_compiler_checked": False,
        "natural_hard_state_family_established": False,
        "literature": ["https://arxiv.org/abs/2309.16387", "https://arxiv.org/abs/2503.22644"],
        "research_note": "research/REES_NOISY_STATE_SOURCE.md",
    }
    if args.write:
        path = Path(__file__).resolve().parents[1]/"research/reductions/rees_noisy_state_source.json"
        path.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
