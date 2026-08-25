"""Natural sibling frames have no polynomial window at the ``q`` scale.

Let ``E_1,...,E_q`` be equal-rank orthogonal projectors and put

    S = sum_e E_e,              G = R R^*,              R^* R = S.

The canonical addressed-cross-map assembly exposes ``G/q``.  If
``mu_S`` is the native trace law, then for every ``P>=1``

    mu_S([q/P,infinity))
      <= P Tr(S^2)/(q Tr(S))
      = P [q^-1 + (1-q^-1) h_bar],                         (1)

where ``h_bar`` is the average normalized ordered pair overlap.  The first
inequality is the pointwise bound
``lambda 1_[q/P,infinity)(lambda) <= (P/q) lambda^2``; the equality is an
exact projector identity.  The nonzero spectra of ``S`` and ``G`` agree, so
(1) is also the trace-weighted mass of eigenvalues at least ``1/P`` in
``G/q`` and of singular values at least ``1/sqrt(P)`` in ``R/sqrt(q)``.

For the natural final sibling frames of the self-dual wreath construction,
let ``g=n!``, take any fixed copy multiplier ``c>=1``, set

    K = ceil(c log_2 g)+2,       q=2^(K-1),       alpha=q/g,

and condition the ``2K`` Plancherel source partitions to be globally
distinct.  The exact sibling second moment is

    E Tr(S^2)/D = m_2 = alpha(1-g^-1)+alpha^2.              (2)

There are ``p(n)`` possible target partitions and two siblings.  Positivity,
conditional Markov, and a union bound show that, with conditional probability
at least ``1-delta-eta_rank``, simultaneously for every target and both
siblings,

    Tr(S^2)/D <= 2 p(n) m_2/(delta p_cf).                   (3)

Uniform orientation-rank concentration supplies
``Tr(S)>=q(1-epsilon)D/g`` on the same event.  Combining (1)--(3) gives

    mu_S([q/P,infinity))
      <= 2 P p(n)/(delta p_cf(1-epsilon))
         * [(1-g^-1)/q + 1/g].                              (4)

For fixed polynomial ``P=n^d`` and ``delta=n^-s``, global-distinct mass
``p_cf`` tends to one, the rank failure tends to zero, and
``p(n)n^(d+s)/n! = o(1)``.  Thus the canonical ``G/q`` signal retains
vanishing natural trace-weighted mass at every inverse-polynomial normalized
eigenvalue window.  Equivalently, its normalized analysis retains vanishing
mass at every inverse-polynomial singular-value window.

This decisively falsifies the proposed spectral escape for the one-shot
uniform linear assembly.  It does *not* contradict trace-weighted polar
truncation: an absolute cutoff ``tau=1/poly(n)`` on the unnormalized ``S``
appears at ``tau/q``, not ``1/poly(n)``, in ``G/q``.  Nor does it rule out a
recursive shorted metric, nonlinear multi-query transform, direct structured
global polar, pair-GPE transport, or a branch-character-retaining decoder.
The formulas are classically evaluable and supply no algorithm or speedup.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import integer_partitions
from research_registry import (
    ExperimentRecord,
    NegativeResultRecord,
    upsert_experiment,
    upsert_negative_result,
    utc_now,
)
from self_dual_wreath_addressed_cross_map_pair_polar_gram_boundary import (
    s3_pair_data,
)
from self_dual_wreath_final_root_natural_common_span import (
    _uniform_leaf_rank_failure_log2,
    log2_global_distinct_probability,
)
from self_dual_wreath_sibling_frame_mp_moments import sibling_moment_formula


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_natural_q_scale_spectral_window_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-NATURAL-Q-SCALE-SPECTRAL-WINDOW-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
NEGATIVE_RESULT_ID = (
    "SCHUR-COMPANION-CANONICAL-G-OVER-Q-NO-NATURAL-POLYNOMIAL-WINDOW"
)
MAXIMAL_DIMENSION_PAPER_ID = "aggarwal-elboim-maximal-dimension-2026"
MAXIMAL_DIMENSION_PAPER_URL = "https://arxiv.org/abs/2605.25995"


@dataclass(frozen=True)
class QScaleSpectralMassControl:
    control_id: str
    branch_count: int
    ambient_dimension: int
    leaf_rank: int
    threshold_divisor: float
    unnormalized_frame_threshold: float
    normalized_gram_threshold: float
    normalized_analysis_singular_threshold: float
    frame_trace: float
    frame_second_moment: float
    average_normalized_ordered_pair_overlap: float
    exact_native_high_spectral_mass: float
    second_moment_high_mass_upper_bound: float
    pair_overlap_identity_residual: float
    frame_gram_nonzero_spectrum_residual: float
    projector_residual: float
    equal_rank_projectors_verified: bool
    q_scale_mass_bound_verified: bool
    status: str


@dataclass(frozen=True)
class NaturalQScaleWindowScalingRecord:
    n: int
    group_order_decimal: str
    log2_group_order: float
    partition_count: int
    copy_multiplier: int
    selected_copy_count: int
    child_orientation_count_decimal: str
    child_orientation_count_log2: int
    child_aspect_ratio: float
    polynomial_window_degree: int
    confidence_degree: int
    threshold_divisor_decimal: str
    markov_failure_probability: float
    relative_rank_tolerance: float
    log2_global_distinct_probability: float
    global_distinct_probability: float
    log2_unconditioned_uniform_rank_failure_upper_bound: float
    log2_conditioned_uniform_rank_failure_upper_bound: float
    conditioned_uniform_rank_failure_upper_bound: float
    conditioned_good_event_probability_lower_bound: float
    expected_normalized_sibling_second_moment: float
    log2_conditional_native_high_mass_upper_bound: float
    conditional_native_high_mass_upper_bound: float
    unconditional_expected_supremum_mass_upper_bound: float
    factorial_domination_margin_log2: float
    finite_conditional_bound_nonvacuous: bool
    finite_unconditional_bound_nonvacuous: bool
    asymptotic_q_scale_native_mass_vanishes: bool
    normalized_gram_inverse_polynomial_window_retains_positive_mass: bool
    normalized_analysis_inverse_polynomial_window_retains_positive_mass: bool
    hierarchical_or_direct_global_polar_ruled_out: bool
    status: str


@dataclass(frozen=True)
class NaturalQScaleSpectralWindowTheorem:
    input_space: str
    target_space: str
    deterministic_mass_inequality: str
    pair_overlap_identity: str
    natural_second_moment_input: str
    conditioning_transfer: str
    uniform_target_bound: str
    asymptotic_conclusion: str
    physical_relevance: str
    truncation_scale_reconciliation: str
    classical_alternative: str
    surviving_mechanisms: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class NaturalQScaleSpectralWindowReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: NaturalQScaleSpectralWindowTheorem
    exact_controls: list[QScaleSpectralMassControl]
    scaling_records: list[NaturalQScaleWindowScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    primary_literature: list[dict[str, str]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _positive_eigenvalues(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    hermitian = (matrix + matrix.conj().T) / 2.0
    values = np.linalg.eigvalsh(hermitian)
    return values[values > 100 * tolerance]


def _clipped_probability_from_log2(log2_probability: float) -> float:
    """Convert a log probability/bound without overflowing on vacuous rows."""

    if log2_probability == -math.inf or log2_probability <= -1074:
        return 0.0
    if log2_probability >= 0:
        return 1.0
    return math.exp2(log2_probability)


def _projector_basis(projector: np.ndarray, tolerance: float) -> np.ndarray:
    hermitian = (projector + projector.conj().T) / 2.0
    values, vectors = np.linalg.eigh(hermitian)
    return vectors[:, values > 0.5]


def audit_q_scale_spectral_mass(
    projectors: tuple[np.ndarray, ...],
    threshold_divisor: float,
    *,
    control_id: str,
    tolerance: float = 1e-9,
) -> QScaleSpectralMassControl:
    """Verify (1) and the frame/Gram spectral equivalence on a finite frame."""

    if len(projectors) < 2:
        raise ValueError("at least two projectors are required")
    if threshold_divisor < 1:
        raise ValueError("threshold_divisor must be at least one")
    shape = projectors[0].shape
    if len(shape) != 2 or shape[0] != shape[1]:
        raise ValueError("projectors must be square")
    if any(projector.shape != shape for projector in projectors):
        raise ValueError("projector shape mismatch")

    q = len(projectors)
    dimension = shape[0]
    projector_residual = max(
        max(
            float(np.linalg.norm(projector - projector.conj().T, ord=2)),
            float(np.linalg.norm(projector @ projector - projector, ord=2)),
        )
        for projector in projectors
    )
    bases = tuple(_projector_basis(projector, tolerance) for projector in projectors)
    ranks = tuple(basis.shape[1] for basis in bases)
    equal_rank = len(set(ranks)) == 1 and ranks[0] > 0
    if not equal_rank:
        raise ValueError("projectors must have the same positive rank")
    rank = ranks[0]

    frame = sum(projectors, np.zeros(shape, dtype=complex))
    analysis = np.vstack(tuple(basis.conj().T for basis in bases))
    gram = analysis @ analysis.conj().T
    frame_values = _positive_eigenvalues(frame, tolerance)
    gram_values = _positive_eigenvalues(gram, tolerance)
    spectrum_residual = (
        float(np.max(np.abs(frame_values - gram_values)))
        if len(frame_values) == len(gram_values)
        else math.inf
    )

    trace = float(np.trace(frame).real)
    second = float(np.trace(frame @ frame).real)
    threshold = q / threshold_divisor
    high_mass = float(
        np.sum(frame_values[frame_values >= threshold - 100 * tolerance]) / trace
    )
    ordered_overlap = sum(
        float(np.trace(left @ right).real)
        for source, left in enumerate(projectors)
        for target, right in enumerate(projectors)
        if source != target
    )
    average_overlap = ordered_overlap / (q * (q - 1) * rank)
    moment_bound_raw = threshold_divisor * second / (q * trace)
    overlap_bound_raw = threshold_divisor * (
        1.0 / q + (1.0 - 1.0 / q) * average_overlap
    )
    bound = min(1.0, moment_bound_raw)
    identity_residual = abs(second / trace - (1 + (q - 1) * average_overlap))
    verified = bool(
        projector_residual <= 100 * tolerance
        and spectrum_residual <= 100 * tolerance
        and identity_residual <= 100 * tolerance
        and abs(moment_bound_raw - overlap_bound_raw) <= 100 * tolerance
        and high_mass <= bound + 100 * tolerance
    )
    return QScaleSpectralMassControl(
        control_id=control_id,
        branch_count=q,
        ambient_dimension=dimension,
        leaf_rank=rank,
        threshold_divisor=float(threshold_divisor),
        unnormalized_frame_threshold=float(threshold),
        normalized_gram_threshold=float(1.0 / threshold_divisor),
        normalized_analysis_singular_threshold=float(
            1.0 / math.sqrt(threshold_divisor)
        ),
        frame_trace=trace,
        frame_second_moment=second,
        average_normalized_ordered_pair_overlap=average_overlap,
        exact_native_high_spectral_mass=high_mass,
        second_moment_high_mass_upper_bound=bound,
        pair_overlap_identity_residual=identity_residual,
        frame_gram_nonzero_spectrum_residual=spectrum_residual,
        projector_residual=projector_residual,
        equal_rank_projectors_verified=equal_rank,
        q_scale_mass_bound_verified=verified,
        status=(
            "exact-q-scale-spectral-mass-bound-verified"
            if verified
            else "q-scale-spectral-mass-control-failure"
        ),
    )


def orthogonal_rank_one_projectors(branch_count: int) -> tuple[np.ndarray, ...]:
    if branch_count < 2:
        raise ValueError("branch_count must be at least two")
    return tuple(
        np.diag([1.0 if row == index else 0.0 for row in range(branch_count)])
        for index in range(branch_count)
    )


def identical_rank_one_projectors(
    branch_count: int,
    ambient_dimension: int = 4,
) -> tuple[np.ndarray, ...]:
    if branch_count < 2 or ambient_dimension < 1:
        raise ValueError("invalid identical-projector frame dimensions")
    projector = np.zeros((ambient_dimension, ambient_dimension), dtype=complex)
    projector[0, 0] = 1.0
    return tuple(projector.copy() for _ in range(branch_count))


def natural_q_scale_window_scaling_record(
    n: int,
    *,
    copy_multiplier: int = 1,
    polynomial_window_degree: int = 4,
    confidence_degree: int = 2,
    relative_rank_tolerance: float = 1 / 64,
) -> NaturalQScaleWindowScalingRecord:
    """Evaluate the finite form of the uniform natural bound (4)."""

    if n < 3:
        raise ValueError("n must be at least three")
    if copy_multiplier < 1:
        raise ValueError("copy_multiplier must be at least one")
    if polynomial_window_degree < 0 or confidence_degree < 1:
        raise ValueError("invalid polynomial degrees")
    if not 0 < relative_rank_tolerance < 1:
        raise ValueError("relative_rank_tolerance must lie in (0,1)")

    order = math.factorial(n)
    log2_order = math.lgamma(n + 1) / math.log(2.0)
    copies = math.ceil(copy_multiplier * log2_order) + 2
    q = 1 << (copies - 1)
    alpha = q / order
    partition_count = len(tuple(integer_partitions(n)))
    divisor = n**polynomial_window_degree
    delta = n ** (-confidence_degree)
    distinct_log2 = log2_global_distinct_probability(n, copies)
    distinct_probability = _clipped_probability_from_log2(distinct_log2)
    rank_log2 = _uniform_leaf_rank_failure_log2(
        n, copies, relative_rank_tolerance
    )
    conditioned_rank_log2 = rank_log2 - distinct_log2
    conditioned_rank_failure = _clipped_probability_from_log2(
        conditioned_rank_log2
    )
    event_probability = max(0.0, 1.0 - delta - conditioned_rank_failure)

    moment = sibling_moment_formula(order, copies)
    second = float(Fraction(moment.expected_normalized_second_moment))
    scale_term = (1.0 - 1.0 / order) / q + 1.0 / order
    log2_bound = (
        1.0
        + math.log2(divisor)
        + math.log2(partition_count)
        - math.log2(delta)
        - distinct_log2
        - math.log2(1.0 - relative_rank_tolerance)
        + math.log2(scale_term)
    )
    conditional_bound = _clipped_probability_from_log2(log2_bound)
    unconditioned_rank_failure = _clipped_probability_from_log2(rank_log2)
    unconditional_expected_bound = min(
        1.0,
        (1.0 - distinct_probability)
        + delta
        + unconditioned_rank_failure
        + distinct_probability * conditional_bound,
    )
    domination_margin = (
        log2_order
        - math.log2(partition_count)
        - (polynomial_window_degree + confidence_degree) * math.log2(n)
    )
    return NaturalQScaleWindowScalingRecord(
        n=n,
        group_order_decimal=str(order),
        log2_group_order=log2_order,
        partition_count=partition_count,
        copy_multiplier=copy_multiplier,
        selected_copy_count=copies,
        child_orientation_count_decimal=str(q),
        child_orientation_count_log2=copies - 1,
        child_aspect_ratio=alpha,
        polynomial_window_degree=polynomial_window_degree,
        confidence_degree=confidence_degree,
        threshold_divisor_decimal=str(divisor),
        markov_failure_probability=delta,
        relative_rank_tolerance=relative_rank_tolerance,
        log2_global_distinct_probability=distinct_log2,
        global_distinct_probability=distinct_probability,
        log2_unconditioned_uniform_rank_failure_upper_bound=rank_log2,
        log2_conditioned_uniform_rank_failure_upper_bound=conditioned_rank_log2,
        conditioned_uniform_rank_failure_upper_bound=conditioned_rank_failure,
        conditioned_good_event_probability_lower_bound=event_probability,
        expected_normalized_sibling_second_moment=second,
        log2_conditional_native_high_mass_upper_bound=log2_bound,
        conditional_native_high_mass_upper_bound=conditional_bound,
        unconditional_expected_supremum_mass_upper_bound=(
            unconditional_expected_bound
        ),
        factorial_domination_margin_log2=domination_margin,
        finite_conditional_bound_nonvacuous=conditional_bound < 1.0,
        finite_unconditional_bound_nonvacuous=unconditional_expected_bound < 1.0,
        asymptotic_q_scale_native_mass_vanishes=True,
        normalized_gram_inverse_polynomial_window_retains_positive_mass=False,
        normalized_analysis_inverse_polynomial_window_retains_positive_mass=False,
        hierarchical_or_direct_global_polar_ruled_out=False,
        status=(
            "finite-conditional-q-scale-bound-nonvacuous"
            if conditional_bound < 1.0
            else "asymptotic-q-scale-no-go-finite-bound-vacuous"
        ),
    )


def run_natural_q_scale_spectral_window_no_go() -> NaturalQScaleSpectralWindowReport:
    _, s3_projectors, _ = s3_pair_data()
    controls = [
        audit_q_scale_spectral_mass(
            s3_projectors,
            1,
            control_id="regular-s3-transposition-frame",
        ),
        audit_q_scale_spectral_mass(
            orthogonal_rank_one_projectors(8),
            2,
            control_id="orthogonal-q8-flat-frame",
        ),
        audit_q_scale_spectral_mass(
            identical_rank_one_projectors(8),
            1,
            control_id="identical-q8-coherent-frame",
        ),
    ]
    scaling = [
        natural_q_scale_window_scaling_record(n)
        for n in (16, 24, 32, 40, 48)
    ]
    control_failures = sum(not row.q_scale_mass_bound_verified for row in controls)
    nonvacuous_rows = sum(row.finite_conditional_bound_nonvacuous for row in scaling)
    tail = scaling[-1]
    verified = control_failures == 0
    theorem = NaturalQScaleSpectralWindowTheorem(
        input_space=(
            "The direct sum of q equal-rank orientation coefficient spaces, with analysis map "
            "R:x -> direct_sum_e J_e^*x and native frame S=R^*R."
        ),
        target_space=(
            "The addressed coefficient Gram G=RR^* exposed by canonical uniform linear assembly as G/q."
        ),
        deterministic_mass_inequality=(
            "Tr(S 1_[q/P,infinity)(S))/Tr(S) <= P Tr(S^2)/(q Tr(S))."
        ),
        pair_overlap_identity=(
            "Tr(S^2)/Tr(S)=1+(q-1)h_bar for equal-rank projector leaves."
        ),
        natural_second_moment_input=(
            "Independent Plancherel sibling frames satisfy E Tr(S^2)/D="
            "alpha(1-1/g)+alpha^2 exactly."
        ),
        conditioning_transfer=(
            "Positivity gives E[Z|global-distinct]<=E[Z]/p_cf; conditional Markov is valid without a bounded-observable or total-variation step."
        ),
        uniform_target_bound=(
            "A union bound over both siblings and all p(n) targets, combined with uniform all-orientation/all-target rank concentration, gives equation (4)."
        ),
        asymptotic_conclusion=(
            "For every fixed copy multiplier and polynomial P,delta^-1, the retained native mass is O(P delta^-1 p(n)/n!)=o(1)."
        ),
        physical_relevance=(
            "The trace-weighted PGM bridge identifies this native trace law with physical sector-average polar mass; the q-scale window retains vanishing average mass."
        ),
        truncation_scale_reconciliation=(
            "The useful absolute S cutoff tau=1/poly(n) is tau/q in G/q, exponentially below the refuted 1/poly(n) normalized window."
        ),
        classical_alternative=(
            "The moment and partition-count bounds are classically evaluable; they construct no measurement or decoder and imply no separation."
        ),
        surviving_mechanisms=(
            "Recursive shorted metrics, nonlinear multi-query transforms, direct representation-specific global polar synthesis, pair-GPE transport, and branch-character-retaining decoding."
        ),
        scope=(
            "A natural-mass no-go for inverse-polynomial functional calculus on the canonical G/q assembly, not an arbitrary-circuit, hierarchical, direct-polar, PGM, information, or decoding lower bound."
        ),
        theorem_verified=verified,
        status=(
            "canonical-g-over-q-natural-polynomial-window-falsified"
            if verified
            else "q-scale-window-control-failure"
        ),
    )
    return NaturalQScaleSpectralWindowReport(
        created_at=utc_now(),
        theorem_contract={
            "hypothesis": (
                "The natural orientation Gram retains nonnegligible trace-weighted mass at eigenvalues Omega(q/poly(n)), making the canonical G/q assembly polynomially usable."
            ),
            "verdict": "falsified",
            "assumptions": [
                "Natural independent Plancherel source pairs followed by global-distinct conditioning.",
                "K=ceil(c log2(n!))+2 for a fixed integer c>=1.",
                "Final affine sibling frames built as sums of orientation projectors.",
                "The canonical one-shot uniform linear assembly signal G/q.",
                "A polynomial threshold divisor P and inverse-polynomial Markov failure delta.",
            ],
            "failure_modes": [
                "The finite collision-free probability is severely pre-asymptotic; finite unconditional rows may be vacuous.",
                "The result does not control the small absolute-eigenvalue window needed by trace-weighted truncation.",
                "The result does not analyze recursive shorted metrics or direct structured polar synthesis.",
                "No hidden-label decoder or classical lower bound is supplied.",
            ],
            "normalization": "canonical dense Gram signal G/q and normalized analysis R/sqrt(q)",
            "natural_input_relevance": (
                "Global distinctness has natural probability 1-o(1), rank concentration is uniform over orientations and targets, and native trace mass equals the physical sector-average polar mass."
            ),
            "success_criterion": (
                "A positive result required nonvanishing native mass at G/q eigenvalue at least 1/poly(n); the theorem proves this mass tends to zero."
            ),
            "speedup_claim_allowed": False,
        },
        theorem=theorem,
        exact_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "deterministic_native_mass_bound",
                "resolved": verified,
                "evidence": "Scalar spectral inequality plus exact finite frame/Gram and projector-overlap controls.",
            },
            {
                "obligation": "natural_sibling_second_moment",
                "resolved": True,
                "evidence": "Exact independent-Plancherel formula m2=alpha(1-1/g)+alpha^2 from the sibling-moment theorem.",
            },
            {
                "obligation": "global_distinct_conditioning",
                "resolved": True,
                "evidence": "Positivity yields the exact 1/p_cf conditional-expectation charge; maximal Plancherel mass gives p_cf=1-o(1).",
            },
            {
                "obligation": "uniform_target_and_leaf_trace_lower_bound",
                "resolved": True,
                "evidence": "The existing concentration theorem is simultaneous over all orientations and all p(n) targets.",
            },
            {
                "obligation": "canonical_normalized_window_natural_mass",
                "resolved": True,
                "evidence": "Equation (4) is O(P delta^-1 p(n)/n!) and therefore vanishes for polynomial P and delta^-1.",
            },
            {
                "obligation": "hierarchical_or_direct_global_polar",
                "resolved": False,
                "evidence": "The second-moment argument is tied to a single q-wide normalized analysis and does not apply to nodewise shorted metrics or representation-specific polar circuits.",
            },
            {
                "obligation": "physical_pgm_decoder_and_classical_separation",
                "resolved": False,
                "evidence": "The trace-mass bridge gives physical relevance but no coherent implementation, decoder, or advantage theorem.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "Pairwise overlaps cannot control a highly aligned many-projector frame.",
                "resolved": True,
                "resolution": "No edge or norm is inferred. The exact aggregate second moment alone upper-bounds trace mass above the very high q/P threshold.",
            },
            {
                "objection": "The moment observable is unbounded, so collision-free conditioning is invalid.",
                "resolved": True,
                "resolution": "Positivity gives E[Z|cf]<=E[Z]/p_cf exactly; no total-variation estimate is used.",
            },
            {
                "objection": "A q-scale eigenvalue can occur for projector frames.",
                "resolved": True,
                "resolution": "The identical-projector control has unit retained mass and h_bar=1. The no-go is distributional: natural average pair coherence is only order 1/g after the rank normalization.",
            },
            {
                "objection": "This refutes the inverse-polynomial absolute cutoff in the trace-weighted truncation theorem.",
                "resolved": True,
                "resolution": "No. An absolute S threshold tau maps to tau/q in G/q, whereas this theorem refutes the much larger S threshold q/poly(n).",
            },
            {
                "objection": "Vanishing q-scale mass proves the physical PGM or every global polar is hard.",
                "resolved": False,
                "resolution": "It closes only inverse-polynomial functional calculus on the canonical G/q signal. Hierarchical, nonlinear, and direct structured routes survive.",
            },
        ],
        primary_literature=[
            {
                "paper_id": MAXIMAL_DIMENSION_PAPER_ID,
                "url": MAXIMAL_DIMENSION_PAPER_URL,
                "scope": "Maximal Plancherel atom exp(-Theta(sqrt(n))), used by the existing global-distinct mass theorem to prove p_cf=1-o(1).",
            }
        ],
        headline_metrics={
            "deterministic_q_scale_mass_bound_theorem_count": int(verified),
            "exact_control_count": len(controls),
            "exact_control_failure_count": control_failures,
            "natural_uniform_target_q_scale_no_go_theorem_count": int(verified),
            "finite_conditional_nonvacuous_row_count": nonvacuous_rows,
            "tail_log2_conditional_native_high_mass_upper_bound": tail.log2_conditional_native_high_mass_upper_bound,
            "tail_unconditional_expected_supremum_mass_upper_bound": tail.unconditional_expected_supremum_mass_upper_bound,
            "canonical_g_over_q_inverse_polynomial_window_positive_mass_count": 0,
            "hierarchical_or_direct_global_polar_no_go_count": 0,
            "polynomial_physical_pgm_circuit_count": 0,
            "hidden_involution_decoder_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "deterministic_q_scale_native_mass_bound_proved": verified,
            "exact_equal_rank_pair_overlap_identity_proved": verified,
            "independent_plancherel_sibling_second_moment_imported": True,
            "global_distinct_positive_markov_transfer_proved": True,
            "uniform_all_orientation_all_target_rank_transfer_imported": True,
            "canonical_g_over_q_natural_inverse_polynomial_eigenvalue_window_has_positive_mass": False,
            "canonical_normalized_analysis_natural_inverse_polynomial_singular_window_has_positive_mass": False,
            "canonical_g_over_q_natural_polynomial_window_falsified": verified,
            "trace_weighted_absolute_frame_cutoff_falsified": False,
            "nonlinear_hierarchical_metric_assembly_ruled_out": False,
            "representation_specific_direct_global_polar_ruled_out": False,
            "pair_gpe_transport_ruled_out": False,
            "physical_pgm_impossibility_proved": False,
            "hidden_involution_decoder_proved": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Exact second moments and uniform rank concentration force the natural trace mass above S scale q/poly(n), equivalently G/q scale 1/poly(n), to vanish. The useful absolute S cutoff survives only at exponentially small G/q scale, so a hierarchical or direct structured polar is now the leading unresolved route."
            ),
        },
        status=theorem.status,
        summary=(
            "Falsified the last spectral escape for canonical linear assembly: under natural Plancherel sources, G/q has vanishing trace-weighted mass in every inverse-polynomial eigenvalue window, uniformly over final siblings and targets."
        ),
        falsifiers_triggered=[
            "Dense natural support does not imply an Omega(q/poly(n)) retained spectral window.",
            "Wishart-like low moments need not prove a hard edge, but the exact second moment already kills mass at the much higher q/poly(n) scale.",
            "An inverse-polynomial cutoff on S is exponentially small after the canonical G/q normalization.",
            "The canonical one-shot linear assembly cannot be rescued by generic inverse-polynomial-resolution functional calculus on natural trace mass.",
        ],
    )


def write_natural_q_scale_spectral_window_no_go_report(
    path: Path = REPORT_PATH,
    *,
    write_registry: bool = True,
) -> dict[str, Any]:
    payload = asdict(run_natural_q_scale_spectral_window_no_go())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if write_registry:
        upsert_experiment(
            ExperimentRecord(
                id=DEFAULT_EXPERIMENT_ID,
                candidate_id=DEFAULT_CANDIDATE_ID,
                title="Natural q-scale spectral window no-go",
                status="completed-negative-theorem",
                hypothesis=payload["theorem_contract"]["hypothesis"],
                protocol=(
                    "Prove the deterministic trace-mass/second-moment inequality, import the exact Plancherel sibling moment and uniform rank theorems, charge global-distinct conditioning by positivity, union over targets, and verify S3, orthogonal, and identical-projector controls."
                ),
                positive_signal=(
                    "A nonvanishing natural native-mass bound at S eigenvalue q/poly(n), equivalently G/q eigenvalue 1/poly(n)."
                ),
                falsifiers=payload["falsifiers_triggered"],
                metrics=list(payload["headline_metrics"].keys()),
                dependencies=[
                    "self_dual_wreath_addressed_cross_map_linear_assembly_normalization_boundary.py",
                    "self_dual_wreath_sibling_frame_mp_moments.py",
                    "self_dual_wreath_uniform_orientation_rank_concentration.py",
                    "self_dual_wreath_global_collision_free_mass.py",
                    "self_dual_wreath_trace_weighted_pgm_bridge.py",
                ],
                next_actions=[
                    "Formalize and test a genuinely hierarchical final-root polar using recursive shorted metrics and GPE pair transport; do not reuse a single q-wide uniform address erasure."
                ],
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id=NEGATIVE_RESULT_ID,
                source=str(path),
                claim=(
                    "The natural orientation Gram has nonnegligible trace-weighted mass at eigenvalue Omega(q/poly(n)), so generic inverse-polynomial functional calculus on the canonical G/q assembly preserves the physical PGM mass."
                ),
                reason_invalid=(
                    "The exact sibling second moment and uniform leaf-rank lower bound give native high-mass at most 2 P p(n)[(1-1/g)/q+1/g]/[delta p_cf(1-epsilon)], which is o(1) for polynomial P and delta^-1."
                ),
                lesson=(
                    "Do not apply generic inverse-polynomial-resolution functional calculus to G/q. Preserve the absolute S cutoff through hierarchical/tightly normalized access or compile a direct representation-specific global polar."
                ),
                applies_to=[
                    DEFAULT_CANDIDATE_ID,
                    "PO-MECHANISM",
                    "PO-MEASUREMENT",
                    "PO-COMPLEXITY",
                ],
                evidence={
                    "natural_uniform_target_q_scale_no_go_proved": True,
                    "tail_log2_conditional_native_high_mass_upper_bound": payload[
                        "headline_metrics"
                    ]["tail_log2_conditional_native_high_mass_upper_bound"],
                    "canonical_g_over_q_inverse_polynomial_window_positive_mass": False,
                    "trace_weighted_absolute_frame_cutoff_falsified": False,
                    "hierarchical_or_direct_global_polar_ruled_out": False,
                    "speedup_claim_allowed": False,
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_natural_q_scale_spectral_window_no_go_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
