"""Exact flat-source budgets and opaque streaming anti-symmetrization control.

The growth primitive is prior art: Bene Watts et al., arXiv:2610.06737v1,
Algorithms 1 and 2, https://arxiv.org/html/2610.06737v1 . This is neither a
new quantum algorithm nor a physical quantum backend. Finite matrix tests
check small instances only; the Rees receiver remains conditional.

The source promises are exact rho = Pi/r, known rank r, and IID fresh copies.
They are supplied, not certified by this module. The top exterior state
retains support, not a nonflat state's spectrum or conjugation stabilizer.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from theorems.nil3_complete_budget import ceil_log
from theorems.rees_projective_source import projective_source_budget


def _integer(value, name, minimum=1):
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name}: integer >= {minimum} required")


def _fraction(value, name, upper=Fraction(1)):
    if not isinstance(value, Fraction) or not 0 < value <= upper:
        raise ValueError(f"{name}: exact positive Fraction <= {upper} required")


@dataclass(frozen=True)
class SubspacePlan:
    """Conservative caps for T top exterior outputs of a rank-r flat state.

    For r >= 2, b = ceil(log2(r*T/beta)) and N = r*r*b growth attempts
    per output. The known streaming bound gives whole-run abort <= r*T/2**b.
    The initial acquisition is additional to those N attempts. No cap resets
    after failure or a successful intermediate growth. Rank one is passed
    through directly, with no growth measurement and no ideal abort.
    """

    rank: int
    outputs: int
    abort_budget: Fraction

    def __post_init__(self):
        _integer(self.rank, "rank")
        _integer(self.outputs, "outputs")
        _fraction(self.abort_budget, "whole-stream abort budget")

    @property
    def tail_bits(self):
        if self.rank == 1:
            return 0
        return ceil_log(2, Fraction(self.rank*self.outputs)/self.abort_budget)

    @property
    def growth_attempts_per_output(self):
        return self.rank*self.rank*self.tail_bits

    @property
    def growth_attempt_cap(self):
        return self.outputs*self.growth_attempts_per_output

    @property
    def multiplexed_register_swap_cap(self):
        """At most two U_A calls, each with k <= rank-1 controlled SWAP arms.

        Excludes control synthesis and ancilla preparation/unpreparation.
        Each register SWAP costs O(input qubits), not one elementary gate.
        """
        return 2*(self.rank-1)*self.growth_attempt_cap

    @property
    def raw_copy_cap(self):
        return self.outputs*(self.growth_attempts_per_output+1)

    @property
    def preparation_call_cap(self):
        return self.raw_copy_cap+self.growth_attempt_cap

    @property
    def abort_probability_bound(self):
        if self.rank == 1:
            return Fraction(0)
        return Fraction(self.rank*self.outputs, 2**self.tail_bits)


def capped_subspace_stream(plan, *, acquire, grow, consume, discard):
    """Run herald/ownership control, without inspecting any quantum state.

    acquire() returns a new non-None opaque token holding one IID input.
    grow(active, fresh, k) takes ownership of BOTH arguments on entry and
    returns (accepted_bool, updated_active). Success returns k+1 registers;
    failure traces out the NEW input and returns the UPDATED k-register
    state, not the old state. The backend owns that trace-out; the controller
    must not discard either consumed token or reuse the rejected input.
    A backend may update a handle in place, but its returned state must include
    the failure instrument. No quantum-state or IID promise is checked here.

    consume(token) and discard(token) take ownership on entry, even if they
    raise. grow likewise owns cleanup of both inputs if it raises; acquire
    owns anything not successfully returned. The controller cleans up tokens
    it still owns on exceptions. discard must not raise during cleanup.
    None is reserved for 'no owned token'; falsey non-None tokens are valid.

    Acquisitions are charged before calling the backend. The first per-output
    timeout aborts the entire stream; already delivered outputs cannot be
    recalled and the caller must treat the result as a whole-run abort.
    """
    if not isinstance(plan, SubspacePlan):
        raise ValueError("SubspacePlan required")
    active = None
    raw = attempts = delivered = peak = 0
    status = "complete"
    try:
        for _ in range(plan.outputs):
            raw += 1
            active = acquire()
            if active is None:
                raise ValueError("acquire returned the reserved None token")
            k = 1
            peak = max(peak, k)
            for _ in range(plan.growth_attempts_per_output):
                if k == plan.rank:
                    break
                raw += 1
                fresh = acquire()
                if fresh is None:
                    raise ValueError("acquire returned the reserved None token")
                peak = max(peak, k+1)
                previous, active = active, None
                attempts += 1
                accepted, active = grow(previous, fresh, k)
                if type(accepted) is not bool or active is None:
                    raise ValueError("grow must return (bool, non-None updated_active)")
                if accepted:
                    k += 1
            if k != plan.rank:
                status = "abort_per_output_timeout"
                break
            output, active = active, None
            consume(output)
            delivered += 1
        return {
            "status": status, "raw_copies": raw, "growth_attempts": attempts,
            "delivered_outputs": delivered, "peak_live_input_registers": peak,
        }
    finally:
        if active is not None:
            discard(active)


def subspace_rees_budget(cover, design, trace_gap, error=Fraction(1, 3), *, rank):
    """Compose known flat-source preparation with the conditional Rees source.

    Assume TD(Pi/r, R(g) Pi/r R(g)^dagger) >= trace_gap for each nonsymmetry.
    The supplied exterior orbit-gap deduction is trace_gap**2/2. This function
    plans with that bound; it does not certify the group, source, or promise.

    projective_source_budget owns ALL ideal receiver, source replacement, and
    copy/action error allocation. Its actions now mean the r-register tensor
    power R(g)**tensor-r, with its existing per-use accuracy obligation applying
    to the complete action. There is no second copy/action error charge here.
    Each of the r base controlled R(g) actions gets 1/r of that existing
    per-use allowance; the sequential hybrid sum recovers the same allowance.
    The multiplexed register SWAP cap excludes control synthesis and ancilla
    preparation/unpreparation; each register SWAP costs O(input qubits).
    The additional error/8 instrument reserve covers EVERY raw acquisition
    and growth attempt, including failures, using complete-instrument error
    (herald records included), not postselected conditional-state accuracy.
    """
    _integer(rank, "rank")
    _fraction(trace_gap, "mixed-state trace-distance gap")
    _fraction(error, "total error", Fraction(1, 2))
    wedge_gap = trace_gap**2/2
    ideal = projective_source_budget(cover, design, gap=wedge_gap, error=error/2)
    plan = SubspacePlan(rank, ideal["total_fresh_copies"], error/8)
    terms = {
        "ideal_receiver_and_source_bound": ideal["total_error_bound"],
        "whole_stream_abort_bound": plan.abort_probability_bound,
        "preparation_complete_instrument_reserved": error/8,
    }
    total_error = sum(terms.values())
    if total_error > error:
        raise ArithmeticError("complete subspace-source budget exceeded")
    return {
        "rank": rank, "ideal_target_copies": plan.outputs,
        "trace_gap": trace_gap, "wedge_overlap_gap": wedge_gap,
        "tail_bits": plan.tail_bits,
        "growth_attempts_per_output": plan.growth_attempts_per_output,
        "growth_attempt_cap": plan.growth_attempt_cap,
        "multiplexed_register_swap_cap": plan.multiplexed_register_swap_cap,
        "raw_copy_cap": plan.raw_copy_cap,
        "preparation_call_cap": plan.preparation_call_cap,
        "preparer_live_input_register_cap": rank,
        "abort_budget": plan.abort_budget,
        "abort_probability_bound": plan.abort_probability_bound,
        "source_or_growth_instrument_error_per_call": error/(8*plan.preparation_call_cap),
        "ideal_source_budget": ideal,
        "base_controlled_action_error_per_use": ideal["copy_and_action_error_per_use"]/rank,
        "tensor_factor_controlled_action_call_cap": rank*ideal["total_controlled_action_calls"],
        "failure_terms": terms, "total_error_bound": total_error,
        "exact_flat_source_required": True, "iid_raw_copies_required": True,
        "flatness_is_supplied_not_certified": True,
        "rank_is_supplied_not_certified": True,
        "trace_gap_is_supplied_not_certified": True,
        "flat_state_conjugation_symmetry_covered_conditionally": True,
        "nonflat_conjugation_symmetry_covered": False,
        "nonflat_exterior_target_retains_support_only": True,
        "conditional_rees_receiver": True,
        "preparer_herald_controller_implemented": True,
        "preparer_quantum_backend_implemented": False,
        "quantum_receiver_implemented": False,
        "preparation_inverse_required": False, "conjugate_state_required": False,
        "novel_antisymmetrization_primitive": False, "speedup_claim_allowed": False,
    }


def report():
    """Deterministic symbolic budgets, with no state or receiver execution.

    The actual class-nine Lie algebra is an existing public scope witness.
    The ranks and gap below are hypothetical source promises on that group,
    not a constructed representation, measured gap, or hard state family.
    """
    import hashlib
    from pathlib import Path
    import random

    from theorems.rees_hsp_reduction import make_rees_cover
    from theorems.rees_projective_source import find_moment_design
    from theorems.right_abelian_induced_source import derived_length_three_witness

    algebra, ambient, witness = derived_length_three_witness(43)
    cover = make_rees_cover(algebra, ambient)
    design = find_moment_design(43, 9, rng=random.Random(1729))
    profiles = []
    for rank in (1, 2, 8, 32):
        budget = subspace_rees_budget(cover, design, Fraction(1, 10), rank=rank)
        profiles.append({
            "rank": rank, "budget": budget,
            "ideal_exterior_copies_ceil_log2": (budget["ideal_target_copies"]-1).bit_length(),
            "raw_copy_cap_ceil_log2": (budget["raw_copy_cap"]-1).bit_length(),
        })
    root = Path(__file__).resolve().parents[1]
    sources = (
        "theorems/rees_subspace_source.py", "tests/test_rees_subspace_source.py",
        "tests/test_cli_parser_integrity.py",
        "theorems/rees_projective_source.py", "theorems/rees_hsp_reduction.py",
        "theorems/state_symmetry_coset_transfer.py", "theorems/nil3_complete_budget.py",
        "theorems/right_abelian_induced_source.py",
        "qsearch_cli/commands/rees.py", "qsearch_cli/registry.py",
        "research/REES_SUBSPACE_SYMMETRY_SOURCE.md",
    )
    return {
        "schema": "rees_subspace_source_v1",
        "status": "CONDITIONAL_SOURCE_REDUCTION_RESOURCE_PLAN_ONLY",
        "preparation_prior_art": {
            "arxiv": "2610.06737v1", "parts": "Algorithms 1-2, Theorem 5, Remark 6",
            "url": "https://arxiv.org/html/2610.06737v1",
            "new_primitive_claimed": False,
        },
        "public_group_profile": {
            "p": cover.p, "class": cover.class_bound,
            "rees_dimension": cover.dimension,
            "original_lcs_dimensions": witness["ambient_lcs_dimensions"],
            "design_points": list(design.points), "design_moments": list(design.moments),
        },
        "hypothetical_source_promises": {
            "trace_gap": Fraction(1, 10), "requested_total_error": Fraction(1, 3),
            "input_qubits": None, "representation_constructed": False,
            "state_constructed": False, "flatness_rank_and_gap_certified": False,
        },
        "profiles": profiles,
        "quantum_execution_performed": False, "quantum_receiver_implemented": False,
        "natural_hard_state_family_established": False, "novelty_established": False,
        "nonflat_conjugation_symmetry_covered": False, "speedup_claim_allowed": False,
        "scope_note": "Polynomial-rank source bridge, not a practical receiver or classical-input speedup",
        "research_note": "research/REES_SUBSPACE_SYMMETRY_SOURCE.md",
        "source_sha256": {path: hashlib.sha256((root/path).read_bytes()).hexdigest()
                          for path in sources},
    }
