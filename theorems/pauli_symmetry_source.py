"""Public controls for purity-gap Pauli CONJUGATION symmetry recovery.

No unknown quantum state is acquired or learned here. The clocks assume IID
stabilizer-diagonal copies and a supplied absolute purity-loss gap. References
with supplied eigenweights are explicitly separate from the public kernels.
"""
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from itertools import product

from theorems.nil3_complete_budget import ceil_log
from theorems.prime_character_opi import ring


def _positive(value, name):
    if type(value) is not int or value < 1:
        raise ValueError(f"{name}: positive integer required")


def _fraction(value, name, *, include_one=False):
    if (not isinstance(value, Fraction) or value <= 0
            or (value > 1 if include_one else value >= 1)):
        raise ValueError(f"{name}: exact positive Fraction required, bounded by one")


def _ceil(value):
    return -(-value.numerator//value.denominator)


def _label(value, width, prime):
    value = tuple(value)
    if len(value) != width or any(type(x) is not int or not 0 <= x < prime for x in value):
        raise ValueError("canonical eigenlabel coordinates required")
    return value


@dataclass(frozen=True)
class PurityGapPlan:
    """Supplied promises, not properties certified from a finite sample.

    Tr(rho^2)>=1/R; every nonzero Pauli conjugation loss is >= gap.
    There is NO R<p restriction. Exact stabilizer diagonality is essential.
    """
    prime: int
    width: int
    inverse_purity: int
    gap: Fraction
    error: Fraction = Fraction(1, 3)

    def __post_init__(self):
        ring(self.prime)
        _positive(self.width, "qudit count")
        _positive(self.inverse_purity, "inverse purity")
        _fraction(self.gap, "absolute purity-loss gap", include_one=True)
        _fraction(self.error, "error")

    def caps(self):
        """Alternative graph-chart clocks, including the classical tail stage.

        Prefer direct_caps: skew Bell proposals remove both basis-learning
        charts and the classical tail stage. Retained for independent control.
        """
        R, beta = self.inverse_purity, self.error/8
        charts = ceil_log(2, 1/beta)
        per_chart = 16*R**3*(self.width+ceil_log(2, charts/beta))
        candidates = charts*per_chart
        q_estimates = candidates+1
        q_trials = _ceil(128*ceil_log(2, 2*q_estimates/beta)/self.gap**2)
        anchors = _ceil(16*R**2/beta)
        cover = 2*R*ceil_log(2, R/beta)
        c_estimates = cover+1
        c_trials = _ceil(128*ceil_log(2, 2*c_estimates/beta)/self.gap**2)
        q_copies = 4*candidates+2*q_estimates*q_trials
        c_copies = anchors+cover+2*c_estimates*c_trials
        return {
            "target": "full phase-free Pauli conjugation group, not a designated original basis",
            "purity_lower_bound": Fraction(1, R),
            "zero_error_probability_lower_bound": Fraction(1, R**3),
            "absolute_nonsymmetry_loss_gap": self.gap,
            "mean_estimation_absolute_error": self.gap/8,
            "symmetry_acceptance_loss_threshold": self.gap/2,
            "chart_count_cap": charts,
            "no_good_chart_probability_bound": Fraction(1, 2**charts),
            "candidate_count_per_chart": per_chart,
            "candidate_count_cap": candidates,
            "quantum_purity_and_overlap_estimate_count": q_estimates,
            "swap_trials_per_estimate": q_trials,
            "basis_stage_raw_copy_cap": q_copies,
            "heavy_anchor_sample_count": anchors,
            "heavy_anchor_weight_lower_bound": Fraction(1, 2*R),
            "period_group_order_upper_bound": R,
            "period_cover_sample_count": cover,
            "classical_collision_estimate_count_cap": c_estimates,
            "independent_pairs_per_collision_estimate": c_trials,
            "period_stage_eigenbasis_measurement_copy_cap": c_copies,
            "total_raw_copy_cap": q_copies+c_copies,
            "failure_budgets": {name: beta for name in (
                "no_good_chart", "all_candidate_spans", "all_swap_estimates",
                "heavy_anchor", "period_coset_coverage", "all_collision_estimates",
                "bounded_public_random_constructions", "complete_quantum_instrument_precision")},
            "total_error_upper_bound": 8*beta,
            "source_promises_certified": False,
            "bad_chart_regression_law_claimed": False,
            "period_stage_requires_collective_quantum_measurements": False,
            "original_basis_identified": False,
            "full_quantum_learner_implemented": False,
        }

    def direct_caps(self):
        """Preferred eight-copy skew Bell finder plus fresh SWAP verifier.

        The mixed-input Fourier identity is independently tested using small
        physical Born-probability references, not used as an uncharged oracle.
        """
        beta = self.error/4
        candidates = 16*self.inverse_purity**3*(2*self.width+ceil_log(2, 1/beta))
        estimates = candidates+1
        trials = _ceil(128*ceil_log(2, 2*estimates/beta)/self.gap**2)
        return {
            "mechanism": "eight-copy skew Bell marginal followed by paid purity verification",
            "target": "full phase-free Pauli conjugation group; not restricted to commuting labels",
            "candidate_count_cap": candidates,
            "candidate_membership_probability_lower_bound": Fraction(1, self.inverse_purity**3),
            "conditional_accepted_ideal_distribution": "uniform on full conjugation group",
            "symmetry_dimension_upper_bound": 2*self.width,
            "purity_and_overlap_estimate_count": estimates,
            "swap_trials_per_estimate": trials,
            "absolute_nonsymmetry_loss_gap": self.gap,
            "mean_estimation_absolute_error": self.gap/8,
            "symmetry_acceptance_loss_threshold": self.gap/2,
            "candidate_source_copy_cap": 8*candidates,
            "verification_source_copy_cap": 2*estimates*trials,
            "total_raw_copy_cap": 8*candidates+2*estimates*trials,
            "failure_budgets": {name: beta for name in (
                "candidate_span", "all_swap_estimates", "bounded_public_field_construction",
                "complete_quantum_instrument_precision")},
            "total_error_upper_bound": 4*beta,
            "random_clifford_chart_required": False,
            "diagonalizing_basis_required": False,
            "classical_eigenlabel_stage_required": False,
            "source_promises_certified": False,
            "qudit_unit_cost_equals_bit_cost_assumed": False,
            "full_quantum_learner_implemented": False,
        }


def period_candidates(prime, width, anchor_samples, coverage_samples):
    """Empirical mode and candidate shifts from PUBLIC measured eigenlabels.

    Correctness needs fresh IID batches of the sizes in PurityGapPlan. This
    kernel does not assert that a supplied short batch satisfies that promise.
    """
    ring(prime)
    _positive(width, "label width")
    counts = Counter(_label(x, width, prime) for x in anchor_samples)
    if not counts:
        raise ValueError("nonempty anchor batch required")
    # Deterministic tie breaking, without a hidden distribution or basis.
    anchor = min(counts, key=lambda x: (-counts[x], x))
    shifts = {tuple((x-y) % prime for x, y in zip(_label(b, width, prime), anchor))
              for b in coverage_samples}
    return anchor, tuple(sorted(shifts))


def collision_estimate(prime, width, pairs, shift):
    """Unbiased overlap estimate when pairs are fresh independent eigenlabels.

    E[1_{B-B'=shift}]=sum_b w_b w_{b-shift}. No table of w is read.
    """
    ring(prime)
    _positive(width, "label width")
    shift = _label(shift, width, prime)
    hits = count = 0
    for left, right in pairs:
        left, right = _label(left, width, prime), _label(right, width, prime)
        count += 1
        hits += tuple((x-y) % prime for x, y in zip(left, right)) == shift
    if not count:
        raise ValueError("nonempty independent-pair batch required")
    return Fraction(hits, count)


def symmetry_decision(purity_estimate, overlap_estimate, gap):
    """Threshold public estimates; does NOT certify accuracy or the gap."""
    _fraction(gap, "absolute purity-loss gap", include_one=True)
    for value in (purity_estimate, overlap_estimate):
        if not isinstance(value, Fraction) or not -1 <= value <= 1:
            raise ValueError("exact bounded SWAP/collision sample means required")
    return purity_estimate-overlap_estimate < gap/2


def reference_translation_profile(prime, width, weights, *, cap=4096):
    """Enumerate periods of a SUPPLIED spectrum; never used by the learner."""
    ring(prime)
    _positive(width, "label width")
    _positive(cap, "reference enumeration cap")
    if prime**width > cap:
        raise ValueError("known-spectrum reference enumeration cap exceeded")
    weights = {_label(b, width, prime): w for b, w in weights.items()}
    if (any(not isinstance(w, Fraction) or w < 0 for w in weights.values())
            or sum(weights.values()) != 1):
        raise ValueError("exact nonnegative reference weights summing to one required")
    purity = sum(w*w for w in weights.values())
    periods, losses = [], []
    for shift in product(range(prime), repeat=width):
        overlap = sum(w*weights.get(tuple((x-y) % prime for x, y in zip(b, shift)), 0)
                      for b, w in weights.items())
        loss = purity-overlap
        if loss == 0:
            periods.append(shift)
        else:
            losses.append(loss)
    return {
        "known_spectrum_reference_only": True,
        "purity": purity,
        "four_equal_label_probability": sum(w**4 for w in weights.values()),
        "purity_cubed_lower_bound": purity**3,
        "periods": tuple(periods),
        "period_group_order": len(periods),
        "smallest_positive_loss": min(losses) if losses else None,
        "spectrum_acquired_from_copies": False,
    }


def report():
    import hashlib
    from pathlib import Path

    import numpy as np
    from theorems.coisotropic_symmetry import maximal_isotropic_subspace
    from theorems.skew_bell_mixed_reference import (
        fourier_marginal, pure_convolution_marginal_control, simulate_skew_bell_mixed,
    )

    root = Path(__file__).resolve().parents[1]
    weights = {(a, b): Fraction((3, 2, 1)[b], 18) for a, b in product(range(3), repeat=2)}
    profile = reference_translation_profile(3, 2, weights)
    algebra = maximal_isotropic_subspace(3, 2, (
        (1, 0, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)))
    matrix = np.array([[1, 1j, 0], [1, 2, 1j], [0, 1, 1]], dtype=complex)
    rho = matrix@matrix.conj().T+np.eye(3)
    rho /= np.trace(rho)
    physical = simulate_skew_bell_mixed(rho, 3, 1, 1).eight_copy_first_marginal
    formula = fourier_marginal(rho, 3, 1, 1)
    wrong = pure_convolution_marginal_control(rho, 3, 1, 1)
    discrepancy = float(np.max(np.abs(physical-formula)))
    if discrepancy > 1e-10 or abs(float(physical.sum())-1) > 1e-10:
        raise ArithmeticError("finite physical skew Bell identity control failed")
    sources = (
        "theorems/pauli_symmetry_source.py", "tests/test_pauli_symmetry_source.py",
        "theorems/coisotropic_symmetry.py", "tests/test_coisotropic_symmetry.py",
        "theorems/skew_bell_mixed_reference.py", "tests/test_skew_bell_mixed_reference.py",
        "research/PAULI_CONJUGATION_SYMMETRY_LEARNING.md", "qsearch_cli/commands/sde.py",
        "research/NOISY_QUADRATIC_PHASE_FILTER.md", "theorems/peaked_phase_source.py",
    )
    return {
        "status": "PURITY_GAP_CONJUGATION_SYMMETRY_DEDUCTION_AND_PUBLIC_CONTROLS_ONLY",
        "input_contract": "IID unknown stabilizer-diagonal state; purity >= 1/R; every positive Pauli loss >= supplied delta",
        "sample_profile": profile,
        "finite_skew_bell_control": {
            "known_dense_one_qutrit_reference_only": True,
            "mixed_nondiagonal_input": True,
            "maximum_physical_fourier_discrepancy": discrepancy,
            "physical_probability_mass": float(physical.sum()),
            "incorrect_pure_convolution_mass": float(wrong.sum()),
            "purity_fourth_power": float(np.trace(rho@rho).real**4),
            "source_copies_per_physical_candidate": 8,
            "physical_quantum_execution": False,
        },
        "public_noncommuting_span_control": {
            "span_dimension": algebra.span_dimension,
            "radical_dimension": algebra.radical_dimension,
            "isotropic_dimension": algebra.isotropic_dimension,
            "diagonalizing_generators": algebra.n_generators,
            "symmetry_membership_assumed_not_verified": True,
        },
        "preferred_direct_caps": PurityGapPlan(3, 2, 8, Fraction(1, 36)).direct_caps(),
        "alternative_chart_caps": PurityGapPlan(3, 2, 8, Fraction(1, 36)).caps(),
        "full_rank_noise_allowed": True,
        "inverse_purity_less_than_prime_required": False,
        "noncommuting_symmetries_allowed": True,
        "public_postprocessing_kernels_implemented": True,
        "uniform_clifford_sampler_implemented": False,
        "quantum_learner_executed": False,
        "source_promises_certified": False,
        "novelty_established": False,
        "matched_classical_input_separation_established": False,
        "speedup_claim_allowed": False,
        "source_sha256": {path: hashlib.sha256((root/path).read_bytes()).hexdigest() for path in sources},
    }
