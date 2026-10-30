"""Exact spectral-grid controls for a proposed copies-only mixed-state source.

The known-spectrum routines are finite mathematical references, NOT an
eigenvalue oracle available to the proposed quantum algorithm. Coherent
spectral filtering, rank acquisition and the full receiver are unimplemented.
"""
from dataclasses import dataclass
from fractions import Fraction

from theorems.nil3_complete_budget import ceil_log


def _ceil(value):
    return -(-value.numerator//value.denominator)


def _positive_integer(value, name):
    if type(value) is not int or value < 1:
        raise ValueError(f"{name} must be a positive integer")


def _probability(value, name):
    if not isinstance(value, Fraction) or not 0 < value <= 1:
        raise ValueError(f"{name} must be an exact Fraction in (0,1]")


@dataclass(frozen=True)
class SpectralGridPlan:
    rank_bound: int
    trace_gap: Fraction
    failure_budget: Fraction

    def __post_init__(self):
        _positive_integer(self.rank_bound, "rank bound")
        _probability(self.trace_gap, "global trace gap")
        _probability(self.failure_budget, "failure budget")

    @property
    def width(self):
        return self.trace_gap/(16*self.rank_bound)

    @property
    def threshold_count(self):
        return _ceil(1/self.width)

    @property
    def offset_bits(self):
        return ceil_log(2, 8*self.rank_bound/self.failure_budget)

    @property
    def offset_count(self):
        return 2**self.offset_bits

    @property
    def spectral_margin(self):
        return self.width/(4*self.offset_count)

    @property
    def offset_failure_bound(self):
        return Fraction(self.rank_bound, self.offset_count)

    @property
    def rank_estimation_precision(self):
        return min(self.spectral_margin/2, self.width**2/128)

    @property
    def rank_estimation_tail(self):
        return self.width/128

    @property
    def rank_training_samples(self):
        bits = ceil_log(2, 2*self.threshold_count/self.failure_budget)
        return _ceil(128*bits/self.width**2)

    @property
    def joint_overlap_gap(self):
        return self.trace_gap**2/8

    def _offset(self, offset):
        if type(offset) is not int or not 0 <= offset < self.offset_count:
            raise ValueError("offset outside the prescribed uniform bit sample")

    def threshold(self, offset, index):
        self._offset(offset)
        if type(index) is not int or not 0 <= index < self.threshold_count:
            raise ValueError("threshold index outside the grid")
        return self.width*(1+Fraction(offset, self.offset_count)+index)

    def rounded_eigenvalue(self, value, offset):
        self._offset(offset)
        if not isinstance(value, Fraction) or not 0 <= value <= 1:
            raise ValueError("reference eigenvalue must be an exact probability")
        count = (value/self.width-Fraction(offset, self.offset_count)).__floor__()
        return self.width*max(0, min(self.threshold_count, count))


def _spectrum(plan, eigenvalues):
    values = tuple(eigenvalues)
    if not values or any(not isinstance(x, Fraction) or not 0 <= x <= 1 for x in values):
        raise ValueError("reference spectrum requires exact nonnegative Fractions")
    if sum(values) != 1 or sum(x > 0 for x in values) > plan.rank_bound:
        raise ValueError("reference spectrum violates trace or rank promise")
    return values


def reference_profile(plan, eigenvalues, offset, *, max_thresholds=10000):
    """Inspect supplied exact eigenvalues; unavailable in the copies-only model."""
    values = _spectrum(plan, eigenvalues)
    plan._offset(offset)
    _positive_integer(max_thresholds, "reference threshold cap")
    if plan.threshold_count > max_thresholds:
        raise ValueError("reference threshold enumeration cap exceeded")
    thresholds = tuple(plan.threshold(offset, j) for j in range(plan.threshold_count))
    ranks = tuple(sum(x >= t for x in values) for t in thresholds)
    rounded = tuple(plan.rounded_eigenvalue(x, offset) for x in values)
    flags, previous = [], None
    for index, rank in enumerate(ranks):
        if rank and rank != previous:
            flags.append({"threshold_index": index, "threshold": thresholds[index], "rank": rank})
        previous = rank
    residual = sum(x-y for x, y in zip(values, rounded, strict=True))
    if not 0 <= residual < 2*plan.rank_bound*plan.width:
        raise ArithmeticError("spectral compression bound failed")
    if sum(ranks)*plan.width != sum(rounded):
        raise ArithmeticError("layer-cake trace identity failed")
    return {
        "known_spectrum_reference_only": True,
        "ranks": ranks, "distinct_flags": flags, "rounded_eigenvalues": rounded,
        "trace_residual": residual, "trace_rounded": sum(rounded),
        "good_offset": all(abs(x-t) >= plan.spectral_margin
                           for x in values if x > 0 for t in thresholds),
        "physical_registers_per_flag_product": sum(row["rank"] for row in flags),
    }


def reference_bad_offsets(plan, eigenvalues, *, max_offsets=4096):
    """Exact finite replay of the random-grid union bound, not a spectrum test."""
    values = _spectrum(plan, eigenvalues)
    _positive_integer(max_offsets, "reference offset cap")
    if plan.offset_count > max_offsets:
        raise ValueError("reference offset enumeration cap exceeded")
    bad = []
    for offset in range(plan.offset_count):
        first = plan.threshold(offset, 0)
        near = False
        for value in values:
            if value == 0:
                continue
            lower = ((value-first)/plan.width).__floor__()
            for index in (lower, lower+1):
                if 0 <= index < plan.threshold_count:
                    near |= abs(value-plan.threshold(offset, index)) < plan.spectral_margin
        if near:
            bad.append(offset)
    if len(bad) > sum(x > 0 for x in values):
        raise ArithmeticError("one bad offset per eigenvalue bound failed")
    return tuple(bad)


def flag_preparation_caps(plan, flag_ranks, outputs):
    """Conditional herald caps AFTER successful rank acquisition.

    These count filtered-input acquisitions, their target-copy trials and
    antisymmetry growth, NOT the program copies consumed by spectral filters.
    The note separately charges those dimension-independent DME programs.
    """
    ranks = tuple(flag_ranks)
    _positive_integer(outputs, "flag-product outputs")
    if (not ranks or any(type(r) is not int or not 1 <= r <= plan.rank_bound for r in ranks)
            or tuple(sorted(set(ranks), reverse=True)) != ranks):
        raise ValueError("distinct decreasing positive flag ranks required")
    if sum(ranks) > 1/plan.width:
        raise ValueError("ranks violate the layer-cake register bound")
    bits = ceil_log(2, plan.rank_bound*len(ranks)*outputs/plan.failure_budget)
    attempts = tuple(0 if r == 1 else _ceil(r/plan.width)*bits for r in ranks)
    filtered = outputs*sum(n+1 for n in attempts)
    filter_bits = ceil_log(2, Fraction(filtered)/plan.failure_budget)
    trials = max(1, _ceil(filter_bits/plan.width))
    return {
        "distinct_flag_ranks": ranks, "output_products": outputs,
        "growth_tail_bits": bits, "growth_attempts_per_component": attempts,
        "growth_attempt_cap": outputs*sum(attempts),
        "filtered_inputs_cap": filtered, "filter_trials_per_input": trials,
        "filter_target_copy_cap": filtered*trials,
        "controlled_original_actions_per_product": sum(ranks),
        "growth_abort_bound": Fraction(outputs*sum(r for r in ranks if r > 1), 2**bits),
        "filter_abort_bound": Fraction(filtered, 2**filter_bits),
        "dme_program_copies_included": False,
        "quantum_preparer_implemented": False,
    }


def report():
    """Replay actual exact-spectrum controls, not hypothetical receiver runs."""
    import hashlib
    from pathlib import Path

    tiny = Fraction(1, 2**80)
    cases = (
        ("nonflat_full_support", (Fraction(1, 2), Fraction(1, 3), Fraction(1, 6))),
        ("unresolved_tiny_internal_gap", (Fraction(1, 2), Fraction(1, 4)+tiny, Fraction(1, 4)-tiny)),
        ("unresolved_tiny_tail", (Fraction(1, 2), Fraction(1, 3), Fraction(1, 6)-tiny, tiny)),
    )
    rows = []
    for name, spectrum in cases:
        plan = SpectralGridPlan(len(spectrum), Fraction(1, 8), Fraction(1, 16))
        offset = plan.offset_count//2
        profile = reference_profile(plan, spectrum, offset)
        gap = min(sum(abs(spectrum[i]-spectrum[(i+power) % 3]) for i in range(3))/2
                  for power in (1, 2))
        subgroup = []
        for power in range(3):
            if all(all((spectrum[i] >= flag["threshold"]) ==
                       (spectrum[(i+power) % 3] >= flag["threshold"]) for i in range(3))
                   for flag in profile["distinct_flags"]):
                subgroup.append(power)
        rows.append({
            "name": name, "spectrum": spectrum, "cyclic_action_on_first_three_levels": True,
            "actual_nonidentity_trace_gap": gap, "supplied_trace_gap": plan.trace_gap,
            "width": plan.width, "spectral_margin": plan.spectral_margin,
            "offset": offset, "profile": {k: v for k, v in profile.items() if k != "ranks"},
            "bad_offset_count": len(reference_bad_offsets(plan, spectrum)),
            "offset_count": plan.offset_count, "bad_offset_bound": plan.offset_failure_bound,
            "flag_stabilizer_from_known_diagonal_reference": subgroup,
            "whole_support_wedge_stabilizer": [0, 1, 2],
            "joint_overlap_gap_bound": plan.joint_overlap_gap,
            "single_product_preparation_caps": flag_preparation_caps(
                plan, [f["rank"] for f in profile["distinct_flags"]], 1),
        })
    root = Path(__file__).resolve().parents[1]
    sources = ("theorems/mixed_spectral_source.py", "tests/test_mixed_spectral_source.py",
               "research/REES_MIXED_SPECTRAL_SOURCE.md",
               "theorems/copy_spectral_reference.py", "tests/test_copy_spectral_reference.py",
               "qsearch_cli/commands/rees.py", "tests/test_cli_parser_integrity.py")
    return {
        "schema": "mixed_spectral_source_v1", "status": "CONDITIONAL_REDUCTION_FINITE_CONTROLS_ONLY",
        "cases": rows, "exact_spectra_supplied_only_to_reference": True,
        "quantum_rank_acquisition_implemented": False, "quantum_spectral_filter_implemented": False,
        "total_raw_copy_budget_implemented": False,
        "dme_program_copy_bound_in_research_note": True,
        "end_to_end_quantum_execution": False, "novelty_established": False,
        "natural_hard_family_established": False, "speedup_claim_allowed": False,
        "source_sha256": {p: hashlib.sha256((root/p).read_bytes()).hexdigest() for p in sources},
    }
