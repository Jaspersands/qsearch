"""Peak-weight, not low-rank, certificates for noisy polynomial-phase learning.

No quantum source, spectral oracle, rank learner, or physical receiver is
implemented. Compressed exact spectra enter only explicitly named references.
See research/PEAKED_PHASE_NOISE_LEARNING.md.
"""
from dataclasses import dataclass
from fractions import Fraction
from math import prod

from theorems.nil3_complete_budget import ceil_log
from theorems.prime_character_opi import ring


def _integer(value, name):
    if type(value) is not int or value < 1:
        raise ValueError(f"{name}: positive integer required")


def _error(value):
    if not isinstance(value, Fraction) or not 0 < value < 1:
        raise ValueError("error: exact Fraction in (0,1) required")


def _ceil(value):
    return -(-value.numerator//value.denominator)


@dataclass(frozen=True)
class PeakPhasePlan:
    """Public promise max_b w_b >= 1/R, R < prime; full support is allowed.

    One random threshold must be fixed throughout the entire learning run.
    No exact rank, noise support, minimum weight, or orbit gap is supplied.
    """
    prime: int
    inverse_peak: int
    failure_budget: Fraction = Fraction(1, 48)

    def __post_init__(self):
        ring(self.prime)
        _integer(self.inverse_peak, "inverse peak")
        if not self.inverse_peak < self.prime:
            raise ValueError("inverse peak must be strictly less than prime")
        _error(self.failure_budget)

    @property
    def peak_lower_bound(self):
        return Fraction(1, self.inverse_peak)

    @property
    def minimum_retained_weight(self):
        return self.peak_lower_bound/2

    @property
    def lower_threshold(self):
        return (self.peak_lower_bound+Fraction(1, self.prime))/2

    @property
    def interval_width(self):
        return (self.peak_lower_bound-Fraction(1, self.prime))/2

    @property
    def offset_bits(self):
        return ceil_log(2, 32*self.inverse_peak/self.failure_budget)

    @property
    def offset_count(self):
        return 2**self.offset_bits

    @property
    def spectral_margin(self):
        return self.interval_width/(4*self.offset_count)

    @property
    def nearby_eigenvalue_count_bound(self):
        # Only eigenvalues > 1/(4R) can approach any candidate threshold.
        return 4*self.inverse_peak

    @property
    def bad_offset_probability_bound(self):
        return Fraction(self.nearby_eigenvalue_count_bound, self.offset_count)

    @property
    def retained_rank_bound(self):
        return min(self.prime-1, 2*self.inverse_peak-1)

    def threshold(self, offset):
        if type(offset) is not int or not 0 <= offset < self.offset_count:
            raise ValueError("offset outside fixed midpoint grid")
        return self.lower_threshold + self.interval_width*Fraction(2*offset+1, 2*self.offset_count)

    def preparation_caps(self, outputs):
        """Worst-case target-copy clocks, with program-copy exclusions explicit.

        The rank-training and filter PROGRAM costs are in the note. Never
        treat target_copy_cap as the total consumed source-copy count.
        """
        _integer(outputs, "wedge outputs")
        R, K, beta = self.inverse_peak, self.retained_rank_bound, self.failure_budget
        w = self.minimum_retained_weight
        b = ceil_log(2, Fraction(K*outputs)/beta)
        attempts = 0 if K == 1 else 2*R*K*b
        filtered_inputs = outputs*(attempts+1)
        filter_bits = ceil_log(2, Fraction(filtered_inputs)/beta)
        trials = 2*R*filter_bits
        targets = filtered_inputs*trials
        training_bits = ceil_log(2, 2/beta)
        return {
            "fixed_threshold_required": True,
            "retained_rank_bound": K,
            "output_cap": outputs,
            "growth_attempts_per_output": attempts,
            "filtered_input_cap": filtered_inputs,
            "filter_trials_per_input": trials,
            "filter_target_copy_cap": targets,
            "rank_training_target_copies": _ceil(128*training_bits/w**2),
            "rank_training_precision": min(self.spectral_margin/2, w**2/128),
            "rank_training_ideal_tail": w/128,
            "rank_training_output_tv_allowance": w/128,
            "filter_half_diamond_allowance_per_call": beta/(2*targets),
            "total_growth_gate_error_allowance": beta/2,
            "bad_grid_probability_bound": self.bad_offset_probability_bound,
            "rank_error_budget": beta,
            "growth_abort_bound": Fraction(K*outputs, 2**b) if K > 1 else Fraction(0),
            "filter_abort_bound": Fraction(filtered_inputs, 2**filter_bits),
            "complete_preparation_error_budget": beta,
            "all_source_failure_upper_bound": 5*beta,
            "dme_program_copies_included": False,
            "source_promise_certified": False,
            "physical_quantum_preparer_implemented": False,
        }


def _spectrum_bands(plan, bands):
    """Compressed KNOWN eigenvalues/multiplicities for finite reference only."""
    bands = tuple(bands)
    if not bands:
        raise ValueError("nonempty known-spectrum reference required")
    for value, multiplicity in bands:
        if not isinstance(value, Fraction) or not 0 <= value <= 1:
            raise ValueError("reference eigenvalues must be exact nonnegative Fractions")
        _integer(multiplicity, "eigenvalue multiplicity")
    if sum(value*multiplicity for value, multiplicity in bands) != 1:
        raise ValueError("reference spectrum must have trace one")
    if max(value for value, _ in bands) < plan.peak_lower_bound:
        raise ValueError("reference spectrum violates supplied peak promise")
    return bands


def reference_selection(plan, bands, offset):
    """Inspect a supplied spectrum, NOT acquire it from quantum copies."""
    bands = _spectrum_bands(plan, bands)
    threshold = plan.threshold(offset)
    selected = [(value, count) for value, count in bands if value >= threshold]
    rank = sum(count for _, count in selected)
    mass = sum(value*count for value, count in selected)
    if not 1 <= rank <= plan.retained_rank_bound or mass < plan.peak_lower_bound:
        raise ArithmeticError("peak-selection invariant failed")
    return {
        "known_spectrum_reference_only": True,
        "input_rank": sum(count for value, count in bands if value),
        "threshold": threshold,
        "retained_rank": rank,
        "retained_mass": mass,
        "retained_minimum_normalized_weight": min(value for value, _ in selected)/mass,
        "good_grid_offset": all(abs(value-threshold) >= plan.spectral_margin for value, _ in bands),
        "spectrum_measured": False,
    }


def reference_bad_offsets(plan, bands, *, cap=4096):
    bands = _spectrum_bands(plan, bands)
    _integer(cap, "offset enumeration cap")
    if plan.offset_count > cap:
        raise ValueError("reference offset enumeration cap exceeded")
    bad = tuple(i for i in range(plan.offset_count)
                if any(abs(value-plan.threshold(i)) < plan.spectral_margin for value, _ in bands))
    if len(bad) > plan.nearby_eigenvalue_count_bound:
        raise ArithmeticError("trace-based nearby eigenvalue bound failed")
    return bad


def quadratic_verifier_caps(prime, width, inverse_peak, error=Fraction(1, 3)):
    """Conservative four-copy/SWAP clocks under a peak-weight promise.

    Uses no spectral selection or known rank. Conic witness generation and
    complete quantum precision retain separate budgets; neither is executed.
    """
    _integer(width, "variables")
    _error(error)
    plan = PeakPhasePlan(prime, inverse_peak, error/16)
    if prime <= 2:
        raise ValueError("quadratic phase requires odd prime")
    R = plan.inverse_peak
    gap = Fraction(1, 2*R**5)
    candidates = 16*R**4*(width+ceil_log(2, 4/error))
    trials = _ceil(128*ceil_log(2, 8*(candidates+1)/error)/gap**2)
    return {
        "zero_error_probability_lower_bound": Fraction(1, R**4),
        "wrong_candidate_purity_loss_lower_bound": gap,
        "candidate_count": candidates,
        "purity_and_overlap_estimate_count": candidates+1,
        "swap_trials_per_estimate": trials,
        "mean_estimation_absolute_error": gap/8,
        "raw_copy_cap": 4*candidates+2*(candidates+1)*trials,
        "candidate_span_failure_budget": error/4,
        "simultaneous_estimation_failure_budget": error/4,
        "public_conic_witness_abort_budget": error/4,
        "complete_instrument_error_budget": error/4,
        "total_error_budget": error,
        "known_rank_required": False,
        "classical_only_verifier_claimed": False,
        "end_to_end_quantum_execution": False,
    }


def graph_basis_probability(prime, width):
    """Counting ratio for a uniform Clifford image of a fixed Lagrangian.

    Counts all symmetric graph matrices divided by all Lagrangians. This
    does not sample a Clifford or inspect the hidden stabilizer basis.
    """
    ring(prime)
    _integer(width, "variables")
    return prod((Fraction(prime**j, prime**j+1) for j in range(1, width+1)),
                start=Fraction(1))


def stabilizer_basis_caps(prime, width, inverse_peak, error=Fraction(1, 3)):
    """Repeated graph-chart clocks for phase-free stabilizer BASIS learning.

    On a nontransverse chart the regression law need not hold, but the
    source-copy SWAP verifier remains valid. Return only after n verified
    candidates have independent translation parts; otherwise abort that
    chart. Uniform Clifford sampling/compilation is an imported obligation.
    """
    _error(error)
    charts = ceil_log(2, 4/error)
    inner_error = error/(4*charts)
    inner = quadratic_verifier_caps(prime, width, inverse_peak, inner_error)
    return {
        "target": "phase-free maximal commuting Pauli label space; not original eigenvalue signs",
        "chart_count_cap": charts,
        "good_chart_probability_lower_bound": Fraction(1, 2),
        "no_good_chart_probability_bound": Fraction(1, 2**charts),
        "inner_trial_error_budget": inner_error,
        "all_inner_trial_error_budget": charts*inner_error,
        "uniform_clifford_sampling_abort_budget": error/4,
        "clifford_instrument_precision_budget": error/4,
        "total_error_upper_bound": Fraction(1, 2**charts)+3*error/4,
        "raw_copy_cap": charts*inner["raw_copy_cap"],
        "single_chart": inner,
        "bad_chart_regression_law_claimed": False,
        "original_pure_state_identified": False,
        "uniform_clifford_sampler_implemented": False,
        "full_basis_learner_implemented": False,
    }


def report():
    import hashlib
    from pathlib import Path

    plan = PeakPhasePlan(101, 3)
    dimension = 101**40
    bands = ((Fraction(1, 3), 1), (Fraction(2, 3*(dimension-1)), dimension-1))
    root = Path(__file__).resolve().parents[1]
    sources = ("theorems/peaked_phase_source.py", "tests/test_peaked_phase_source.py",
               "research/PEAKED_PHASE_NOISE_LEARNING.md", "theorems/exterior_phase_learning.py",
               "theorems/mixed_spectral_source.py", "qsearch_cli/commands/sde.py",
               "research/audits/reviews/2026-10-30-noisy-phase-native-scope.md")
    return {
        "status": "PEAK_WEIGHT_SOURCE_REDUCTION_REFERENCE_ONLY",
        "input_contract": "IID polynomial-phase-diagonal state; max error weight >= 1/R; R < p",
        "stabilizer_basis_contract": "IID state diagonal in one unknown maximal stabilizer basis; same peak promise",
        "input_rank_bound_required": False,
        "prime": plan.prime, "inverse_peak": plan.inverse_peak,
        "selection": reference_selection(plan, bands, plan.offset_count//2),
        "interval_width": plan.interval_width,
        "spectral_margin": plan.spectral_margin,
        "bad_grid_probability_bound": plan.bad_offset_probability_bound,
        "example_wedge_target_caps": plan.preparation_caps(4),
        "quadratic_competitor_caps": quadratic_verifier_caps(101, 40, 3),
        "stabilizer_basis_caps": stabilizer_basis_caps(101, 40, 3),
        "known_spectrum_reference_only": True,
        "quantum_filter_executed": False,
        "quantum_learner_executed": False,
        "novelty_established": False,
        "native_classical_input_reduction_established": False,
        "speedup_claim_allowed": False,
        "source_sha256": {path: hashlib.sha256((root/path).read_bytes()).hexdigest() for path in sources},
    }
