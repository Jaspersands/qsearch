"""Natural positive-mass common-span theorem at the final recursive root.

The Haar final-root benchmark has a constant component aspect, but that fact
does not transfer merely by matching dimensions.  This module supplies the
natural dimension theorem that is actually available from existing exact
results.

Let ``g=|G|``, ``K=ceil(log_2 g)``, and use the existing ``C=K+2`` source-pair
schedule.  Splitting the orientation cube on the final bit gives two child
frames

    A = sum_(e_C=0) E_e,       B = sum_(e_C=1) E_e,

with ``q=2^(C-1)`` leaves per child and

    a = q/g in [2,4).                                           (1)

Normalize traces by the full target-carrier dimension ``D``.  Uniform natural
leaf-rank concentration, with tolerance ``epsilon``, gives simultaneously

    (1-epsilon) D/g <= rank(E_e) <= (1+epsilon) D/g.             (2)

The exact sibling-frame second-moment theorem gives, before conditioning,

    E[Tr(A^2)+Tr(B^2)]/D = 2 m_2,
    m_2 = a(1-g^-1)+a^2.                                       (3)

Write ``p_cf`` for the probability that all ``2C`` source irreps are distinct.
For any ``c>1``, conditional Markov implies, with conditional probability at
least ``1-1/c``,

    [Tr(A^2)+Tr(B^2)]/D <= 2 c m_2 / p_cf.                      (4)

For every positive semidefinite matrix, rank(X)>=Tr(X)^2/Tr(X^2).
Titu Andreescu's form of Cauchy--Schwarz and
``dim(range A intersect range B)>=rank(A)+rank(B)-D`` then give, on (2)-(4),

    r/D >= rho(g,a,p_cf)
        := 2(1-epsilon)^2 a p_cf/[c(a+1-g^-1)] - 1,             (5)

where ``r`` is the final sibling common-span dimension.  The rank event fails
with probability ``o(1)`` even after global-distinct conditioning, while
``p_cf=1-o(1)``.  Choosing

    epsilon=1/64,       c=9/8

therefore proves

    Pr_cf[r/D >= 19/128-o(1)] >= 1/9-o(1).                     (6)

This is enough for the component-POVM geometry.  If ``N_A`` is the child
coefficient dimension and ``b_max`` its largest leaf block, then (1)-(2) and
(6) imply on the same positive-mass event

    r/N_A >= 19/520-o(1),
    b_max/r <= (520/19+o(1))/q.                                (7)

Thus natural block/fiber aspect control no longer requires a full-support
theorem.  Combining (7) with the coordinate defect bridge shows that a
relative component edge ``delta>=kappa r/N_A`` would yield an asymptotic
full-rank defect gap at least ``19 kappa/520``.  The natural positive-edge
premise is *not* proved here.  Neither are coherent pseudoinverse access,
component-support SELECT, recursive transport, or a decoder.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import (
    hook_length_dimension,
    integer_partitions,
)
from research_registry import utc_now
from self_dual_wreath_sibling_frame_mp_moments import sibling_moment_formula
from self_dual_wreath_uniform_orientation_rank_concentration import (
    smallest_nonidentity_conjugacy_class_size,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_final_root_natural_common_span.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-FINAL-ROOT-NATURAL-COMMON-SPAN"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

DEFAULT_RANK_TOLERANCE = Fraction(1, 64)
DEFAULT_MARKOV_FACTOR = Fraction(9, 8)
DEFAULT_RELATIVE_EDGE_FACTOR = Fraction(1, 2)


@dataclass(frozen=True)
class CommonSpanRankControl:
    control_id: str
    carrier_dimension: int
    left_support_rank: int
    right_support_rank: int
    observed_common_span_dimension: int
    left_trace: float
    right_trace: float
    total_second_moment: float
    cauchy_common_span_relative_lower_bound: float
    observed_common_span_relative_rank: float
    lower_bound_residual: float
    deterministic_rank_bridge_verified: bool
    status: str


@dataclass(frozen=True)
class NaturalAspectBounds:
    group_order: int
    child_orientation_count: int
    child_orientation_aspect: float
    relative_rank_tolerance: float
    common_span_relative_rank_lower_bound: float
    child_coefficient_to_carrier_lower_bound: float
    child_coefficient_to_carrier_upper_bound: float
    common_fiber_to_coefficient_lower_bound: float
    maximum_component_block_to_fiber_upper_bound: float
    assumed_relative_positive_edge_factor: float
    component_positive_edge_lower_bound: float
    coordinate_defect_gap_lower_bound: float
    positive_asymptotic_defect_gap_predicted: bool


@dataclass(frozen=True)
class FinalRootNaturalScalingRecord:
    n: int
    group_order_decimal: str
    information_threshold_copy_count: int
    selected_copy_count: int
    child_orientation_count_decimal: str
    child_orientation_aspect: float
    relative_rank_tolerance: float
    markov_factor: float
    log2_global_distinct_probability: float
    log2_unconditioned_uniform_leaf_rank_failure_upper_bound: float
    log2_conditioned_uniform_leaf_rank_failure_upper_bound: float
    conditioned_uniform_leaf_rank_failure_upper_bound: float
    conditioned_bridge_event_mass_lower_bound: float
    common_span_relative_rank_lower_bound: float
    common_fiber_to_coefficient_lower_bound: float | None
    maximum_component_block_to_fiber_upper_bound: float | None
    half_relative_edge_defect_gap_lower_bound: float | None
    finite_positive_common_span_bound_certified: bool
    natural_component_positive_edge_proved: bool
    status: str


@dataclass(frozen=True)
class AsymptoticFinalRootCorollary:
    relative_rank_tolerance: str
    markov_factor: str
    conditioned_event_mass_lower_bound: str
    common_span_relative_rank_lower_bound: str
    common_fiber_to_coefficient_lower_bound: str
    maximum_component_block_to_fiber_coefficient: str
    assumed_relative_positive_edge_factor: str
    conditional_defect_gap_limit_lower_bound: str
    natural_component_positive_edge_proved: bool
    statement: str


@dataclass(frozen=True)
class FinalRootNaturalCommonSpanReport:
    created_at: str
    theorem_contract: dict[str, Any]
    deterministic_controls: list[CommonSpanRankControl]
    scaling_records: list[FinalRootNaturalScalingRecord]
    asymptotic_corollary: AsymptoticFinalRootCorollary
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _hermitian_psd(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("frames must be square")
    hermitian = (matrix + matrix.conj().T) / 2.0
    if np.linalg.eigvalsh(hermitian)[0] < -100 * tolerance:
        raise ValueError("frames must be positive semidefinite")
    return hermitian


def audit_common_span_rank_bridge(
    control_id: str,
    left_frame: np.ndarray,
    right_frame: np.ndarray,
    *,
    tolerance: float = 1e-9,
) -> CommonSpanRankControl:
    """Verify the deterministic Cauchy/common-span inequality behind (5)."""

    left = _hermitian_psd(left_frame, tolerance)
    right = _hermitian_psd(right_frame, tolerance)
    if left.shape != right.shape:
        raise ValueError("sibling frames must share one carrier")
    dimension = left.shape[0]
    left_values, left_vectors = np.linalg.eigh(left)
    right_values, right_vectors = np.linalg.eigh(right)
    left_basis = left_vectors[:, left_values > 100 * tolerance]
    right_basis = right_vectors[:, right_values > 100 * tolerance]
    left_rank = left_basis.shape[1]
    right_rank = right_basis.shape[1]
    union_rank = int(
        np.linalg.matrix_rank(
            np.hstack((left_basis, right_basis)),
            tol=100 * tolerance,
        )
    )
    common = left_rank + right_rank - union_rank
    left_trace = float(np.trace(left).real)
    right_trace = float(np.trace(right).real)
    second = float(np.trace(left @ left + right @ right).real)
    raw_lower = (
        (left_trace + right_trace) ** 2 / (dimension * second) - 1.0
        if second > tolerance
        else 0.0
    )
    lower = max(0.0, raw_lower)
    observed = common / dimension
    residual = max(0.0, lower - observed)
    verified = residual <= 1000 * tolerance
    return CommonSpanRankControl(
        control_id=control_id,
        carrier_dimension=dimension,
        left_support_rank=left_rank,
        right_support_rank=right_rank,
        observed_common_span_dimension=common,
        left_trace=left_trace,
        right_trace=right_trace,
        total_second_moment=second,
        cauchy_common_span_relative_lower_bound=lower,
        observed_common_span_relative_rank=observed,
        lower_bound_residual=residual,
        deterministic_rank_bridge_verified=verified,
        status=(
            "deterministic-common-span-rank-bridge-verified"
            if verified
            else "deterministic-common-span-rank-bridge-failure"
        ),
    )


def natural_aspect_bounds(
    group_order: int,
    child_orientation_count: int,
    relative_rank_tolerance: float,
    common_span_relative_rank_lower_bound: float,
    *,
    relative_positive_edge_factor: float = 0.5,
) -> NaturalAspectBounds:
    """Propagate leaf-rank and common-span bounds to component geometry."""

    if group_order < 2 or child_orientation_count < 1:
        raise ValueError("positive nontrivial group and child are required")
    if not 0 <= relative_rank_tolerance < 1:
        raise ValueError("rank tolerance must lie in [0,1)")
    if not 0 < common_span_relative_rank_lower_bound <= 1:
        raise ValueError("common-span lower bound must lie in (0,1]")
    if not 0 < relative_positive_edge_factor <= 1:
        raise ValueError("relative edge factor must lie in (0,1]")
    aspect = child_orientation_count / group_order
    coefficient_lower = (1.0 - relative_rank_tolerance) * aspect
    coefficient_upper = (1.0 + relative_rank_tolerance) * aspect
    fiber_aspect = common_span_relative_rank_lower_bound / coefficient_upper
    block_ratio = (
        (1.0 + relative_rank_tolerance)
        / (group_order * common_span_relative_rank_lower_bound)
    )
    edge = relative_positive_edge_factor * fiber_aspect
    defect = edge - 2.0 * block_ratio + 1.0 / child_orientation_count
    return NaturalAspectBounds(
        group_order=group_order,
        child_orientation_count=child_orientation_count,
        child_orientation_aspect=aspect,
        relative_rank_tolerance=relative_rank_tolerance,
        common_span_relative_rank_lower_bound=common_span_relative_rank_lower_bound,
        child_coefficient_to_carrier_lower_bound=coefficient_lower,
        child_coefficient_to_carrier_upper_bound=coefficient_upper,
        common_fiber_to_coefficient_lower_bound=fiber_aspect,
        maximum_component_block_to_fiber_upper_bound=block_ratio,
        assumed_relative_positive_edge_factor=relative_positive_edge_factor,
        component_positive_edge_lower_bound=edge,
        coordinate_defect_gap_lower_bound=defect,
        positive_asymptotic_defect_gap_predicted=defect > 0,
    )


@lru_cache(maxsize=None)
def log2_global_distinct_probability(n: int, copy_count: int) -> float:
    """Evaluate ``(2C)! e_(2C)(p_lambda)`` stably in the log domain."""

    if n < 1 or copy_count < 0:
        raise ValueError("invalid symmetric-group or copy count")
    partitions = tuple(integer_partitions(n))
    degree = 2 * copy_count
    if degree > len(partitions):
        return -math.inf
    log_order = math.lgamma(n + 1)
    log_weights = np.asarray(
        [
            2.0 * math.log(hook_length_dimension(partition)) - log_order
            for partition in partitions
        ]
    )
    coefficients = np.full(degree + 1, -math.inf)
    coefficients[0] = 0.0
    for log_weight in log_weights:
        previous = coefficients.copy()
        coefficients[1:] = np.logaddexp(
            previous[1:],
            log_weight + previous[:-1],
        )
    return (
        math.lgamma(degree + 1) + float(coefficients[degree])
    ) / math.log(2.0)


def _probability_from_log2(log2_probability: float) -> float:
    if log2_probability == -math.inf or log2_probability <= -1074:
        return 0.0
    return min(1.0, math.exp2(log2_probability))


def _uniform_leaf_rank_failure_log2(
    n: int,
    copy_count: int,
    relative_rank_tolerance: float,
) -> float:
    partitions = tuple(integer_partitions(n))
    partition_count = len(partitions)
    minimum_class = smallest_nonidentity_conjugacy_class_size(n)
    return (
        copy_count
        + math.log2(partition_count)
        + math.log2(partition_count - 1)
        + (2 - copy_count) * math.log2(minimum_class)
        - 2 * math.log2(relative_rank_tolerance)
    )


def final_root_natural_scaling_record(
    n: int,
    *,
    relative_rank_tolerance: float = float(DEFAULT_RANK_TOLERANCE),
    markov_factor: float = float(DEFAULT_MARKOV_FACTOR),
) -> FinalRootNaturalScalingRecord:
    if n < 3:
        raise ValueError("n must be at least three")
    if not 0 < relative_rank_tolerance < 1:
        raise ValueError("rank tolerance must lie in (0,1)")
    if markov_factor <= 1:
        raise ValueError("Markov factor must exceed one")
    order = math.factorial(n)
    threshold = (order - 1).bit_length()
    copies = threshold + 2
    child_orientations = 1 << (copies - 1)
    alpha = child_orientations / order
    distinct_log2 = log2_global_distinct_probability(n, copies)
    distinct_probability = _probability_from_log2(distinct_log2)
    rank_log2 = _uniform_leaf_rank_failure_log2(
        n,
        copies,
        relative_rank_tolerance,
    )
    conditioned_rank_log2 = rank_log2 - distinct_log2
    conditioned_rank_failure = _probability_from_log2(conditioned_rank_log2)
    moment = sibling_moment_formula(order, copies)
    second = float(Fraction(moment.expected_normalized_second_moment))
    rho = (
        2.0
        * (1.0 - relative_rank_tolerance) ** 2
        * alpha**2
        * distinct_probability
        / (markov_factor * second)
        - 1.0
    )
    event_mass = max(
        0.0,
        1.0 - 1.0 / markov_factor - conditioned_rank_failure,
    )
    positive = rho > 0 and event_mass > 0
    bounds = (
        natural_aspect_bounds(
            order,
            child_orientations,
            relative_rank_tolerance,
            rho,
        )
        if positive
        else None
    )
    return FinalRootNaturalScalingRecord(
        n=n,
        group_order_decimal=str(order),
        information_threshold_copy_count=threshold,
        selected_copy_count=copies,
        child_orientation_count_decimal=str(child_orientations),
        child_orientation_aspect=alpha,
        relative_rank_tolerance=relative_rank_tolerance,
        markov_factor=markov_factor,
        log2_global_distinct_probability=distinct_log2,
        log2_unconditioned_uniform_leaf_rank_failure_upper_bound=rank_log2,
        log2_conditioned_uniform_leaf_rank_failure_upper_bound=conditioned_rank_log2,
        conditioned_uniform_leaf_rank_failure_upper_bound=conditioned_rank_failure,
        conditioned_bridge_event_mass_lower_bound=event_mass,
        common_span_relative_rank_lower_bound=max(0.0, rho),
        common_fiber_to_coefficient_lower_bound=(
            bounds.common_fiber_to_coefficient_lower_bound if bounds else None
        ),
        maximum_component_block_to_fiber_upper_bound=(
            bounds.maximum_component_block_to_fiber_upper_bound if bounds else None
        ),
        half_relative_edge_defect_gap_lower_bound=(
            bounds.coordinate_defect_gap_lower_bound if bounds else None
        ),
        finite_positive_common_span_bound_certified=positive,
        natural_component_positive_edge_proved=False,
        status=(
            "finite-conditioned-positive-common-span-bound-certified"
            if positive
            else "asymptotic-common-span-theorem-finite-pcf-bound-vacuous"
        ),
    )


def asymptotic_final_root_corollary() -> AsymptoticFinalRootCorollary:
    epsilon = DEFAULT_RANK_TOLERANCE
    markov = DEFAULT_MARKOV_FACTOR
    event_mass = 1 - 1 / markov
    rho = 4 * (1 - epsilon) ** 2 / (3 * markov) - 1
    fiber_aspect = rho / (4 * (1 + epsilon))
    block_coefficient = 4 * (1 + epsilon) / rho
    defect = DEFAULT_RELATIVE_EDGE_FACTOR * fiber_aspect
    if rho != Fraction(19, 128):
        raise ArithmeticError("the advertised common-span constant changed")
    if fiber_aspect != Fraction(19, 520):
        raise ArithmeticError("the advertised fiber-aspect constant changed")
    if block_coefficient != Fraction(520, 19):
        raise ArithmeticError("the advertised block-ratio constant changed")
    return AsymptoticFinalRootCorollary(
        relative_rank_tolerance=str(epsilon),
        markov_factor=str(markov),
        conditioned_event_mass_lower_bound=str(event_mass),
        common_span_relative_rank_lower_bound=str(rho),
        common_fiber_to_coefficient_lower_bound=str(fiber_aspect),
        maximum_component_block_to_fiber_coefficient=str(block_coefficient),
        assumed_relative_positive_edge_factor=str(DEFAULT_RELATIVE_EDGE_FACTOR),
        conditional_defect_gap_limit_lower_bound=str(defect),
        natural_component_positive_edge_proved=False,
        statement=(
            "On at least 1/9-o(1) of globally distinct natural blocks, the "
            "final sibling common span has relative rank at least 19/128-o(1), "
            "the child fiber aspect is at least 19/520-o(1), and b_max/r is "
            "at most (520/19+o(1))/q. A delta>=(r/N)/2 component edge would "
            "then imply defect gap at least 19/1040-o(1)."
        ),
    )


def _deterministic_controls() -> list[CommonSpanRankControl]:
    left = np.diag([1.0] * 8 + [0.0] * 4).astype(complex)
    right = np.diag([0.0] * 4 + [1.0] * 8).astype(complex)
    weighted_left = np.diag(
        [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.0, 0.0]
    ).astype(complex)
    weighted_right = np.diag(
        [0.0, 0.0, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 0.3]
    ).astype(complex)
    disjoint_left = np.diag([1.0] * 6 + [0.0] * 6).astype(complex)
    disjoint_right = np.diag([0.0] * 6 + [1.0] * 6).astype(complex)
    return [
        audit_common_span_rank_bridge(
            "RANK-EIGHT-PROJECTOR-SIBLINGS-IN-D12",
            left,
            right,
        ),
        audit_common_span_rank_bridge(
            "WEIGHTED-OVERLAPPING-SIBLINGS-IN-D10",
            weighted_left,
            weighted_right,
        ),
        audit_common_span_rank_bridge(
            "DISJOINT-HALF-RANK-BOUNDARY-IN-D12",
            disjoint_left,
            disjoint_right,
        ),
    ]


def run_final_root_natural_common_span() -> FinalRootNaturalCommonSpanReport:
    controls = _deterministic_controls()
    scaling = [
        final_root_natural_scaling_record(n)
        for n in (12, 16, 20, 24, 32, 40, 48)
    ]
    corollary = asymptotic_final_root_corollary()
    failures = sum(not row.deterministic_rank_bridge_verified for row in controls)
    conditioned_rank_rows = sum(
        row.log2_conditioned_uniform_leaf_rank_failure_upper_bound < 0
        for row in scaling
    )
    finite_positive_rows = sum(
        row.finite_positive_common_span_bound_certified for row in scaling
    )
    exact = failures == 0
    return FinalRootNaturalCommonSpanReport(
        created_at=utc_now(),
        theorem_contract={
            "deterministic_common_span_bridge": (
                "For PSD siblings A,B on D dimensions, rank(A)+rank(B) is at "
                "least (Tr A+Tr B)^2/[Tr(A^2)+Tr(B^2)], and their common-span "
                "rank is at least rank(A)+rank(B)-D."
            ),
            "conditioned_second_moment_event": (
                "The exact unconditioned sibling second moment and positivity "
                "give Pr_cf[Z<=2c m2/p_cf]>=1-1/c by conditional Markov."
            ),
            "natural_positive_mass_common_span": (
                "Uniform leaf-rank concentration plus p_cf=1-o(1), epsilon=1/64, "
                "and c=9/8 give r/D>=19/128-o(1) on conditional mass 1/9-o(1)."
            ),
            "component_aspect_corollary": (
                "On that event r/N>=19/520-o(1) and b_max/r<=(520/19+o(1))/q."
            ),
            "conditional_defect_corollary": (
                "If every retained nonzero component eigenvalue obeys "
                "delta>=(r/N)/2, the aggregate defect gap is at least "
                "19/1040-o(1)."
            ),
            "scope": (
                "The theorem proves natural positive-mass dimensions, not a "
                "natural component edge, frame pseudoinverse conditioning, "
                "coherent component SELECT, recursive transport, or decoding."
            ),
        },
        deterministic_controls=controls,
        scaling_records=scaling,
        asymptotic_corollary=corollary,
        proof_obligations=[
            {
                "obligation": "prove_positive_natural_final_sibling_common_span_mass",
                "resolved": True,
                "resolution": "Cauchy rank, the exact sibling second moment, conditional Markov, uniform leaf ranks, and p_cf=1-o(1) give common relative rank 19/128-o(1) on mass 1/9-o(1).",
            },
            {
                "obligation": "control_natural_final_component_block_to_fiber_aspects",
                "resolved": True,
                "resolution": "Uniform leaf ranks and the positive-mass common-span theorem give r/N>=19/520-o(1) and b_max/r=O(1/q).",
            },
            {
                "obligation": "prove_natural_final_component_positive_edge",
                "resolved": False,
                "resolution": "Need a representation-specific lower edge for the normalized component compressions, or a mass-preserving trim of tiny-edge outcomes. Haar/Jacobi behavior is not evidence of this premise.",
            },
            {
                "obligation": "compile_natural_component_support_and_child_pseudoinverses",
                "resolved": False,
                "resolution": "Dimension control does not provide tightly normalized coherent access to frame roots, pseudoinverses, or component support projectors.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "The target dimension d_nu destroys the final-root aspect.",
                "resolved": True,
                "resolution": "Restoring the target row multiplies both the full carrier and every leaf coefficient block by d_nu; uniform leaf mass is D/g, independent of d_nu.",
            },
            {
                "objection": "A full-support theorem is necessary before component aspects can be bounded.",
                "resolved": True,
                "resolution": "False. A constant relative common span is enough, and the rank/second-moment argument proves it on positive natural mass.",
            },
            {
                "objection": "Global-distinct conditioning invalidates the second-moment input because the observable is unbounded with n.",
                "resolved": True,
                "resolution": "No total-variation estimate is used. Positivity gives E[Z|cf]<=E[Z]/p_cf exactly, and p_cf tends to one.",
            },
            {
                "objection": "Constant common-span and block aspects imply a positive component edge.",
                "resolved": False,
                "resolution": "Arbitrarily ill-conditioned normalized leaf compressions can share these dimensions. The natural positive-edge theorem remains the decisive spectral gate.",
            },
        ],
        headline_metrics={
            "deterministic_common_span_rank_bridge_theorem_count": int(exact),
            "deterministic_control_count": len(controls),
            "deterministic_control_failure_count": failures,
            "natural_positive_mass_final_common_span_theorem_count": 1,
            "natural_final_component_aspect_theorem_count": 1,
            "asymptotic_conditioned_event_mass_lower_bound": float(Fraction(1, 9)),
            "asymptotic_common_span_relative_rank_lower_bound": float(Fraction(19, 128)),
            "asymptotic_common_fiber_aspect_lower_bound": float(Fraction(19, 520)),
            "asymptotic_component_block_ratio_coefficient": float(Fraction(520, 19)),
            "conditional_half_relative_edge_defect_gap_lower_bound": float(Fraction(19, 1040)),
            "conditioned_uniform_rank_certified_finite_row_count": conditioned_rank_rows,
            "finite_positive_common_span_bound_row_count": finite_positive_rows,
            "natural_final_component_positive_edge_theorem_count": 0,
            "natural_component_support_select_circuit_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "natural_final_common_span_has_constant_relative_rank_on_positive_mass": True,
            "natural_final_component_block_to_fiber_aspects_controlled_on_positive_mass": True,
            "full_support_required_for_final_component_aspect_control": False,
            "natural_final_component_positive_edge_proved": False,
            "natural_final_child_frame_pseudoinverse_access_proved": False,
            "natural_component_support_select_compiled": False,
            "recursive_orientation_polar_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The final natural common-span mass and component dimensions are "
                "now controlled, but the positive component edge and coherent "
                "implementation gates remain open."
            ),
        },
        status=(
            "natural-final-common-span-and-aspects-proved-component-edge-open"
            if exact
            else "final-root-natural-common-span-control-failure"
        ),
        summary=(
            "Proved a constant relative final sibling common span on positive "
            "globally distinct natural mass and propagated it to constant "
            "component fiber aspect with O(1/q) block ratio."
        ),
        falsifiers_triggered=[
            "The target carrier dimension does not spoil the normalized child aspect; its factor cancels exactly.",
            "Full final-child support is stronger than necessary for component geometry.",
            "Fixed second moments cannot prove a spectral edge, but they do prove positive-mass support rank through Cauchy and Markov.",
            "Natural block/fiber aspect control does not imply a natural positive component eigenvalue edge.",
        ],
    )


def write_final_root_natural_common_span_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-FINAL-ROOT-NATURAL-COMMON-SPAN"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_final_root_natural_common_span())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    if write_registry:
        from research_registry import (
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-SELF-DUAL-WREATH-FINAL-ROOT-NATURAL-COMMON-SPAN",
                source=registry_experiment_id,
                claim=(
                    "Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-FINAL-ROOT-NATURAL-COMMON-SPAN."
                ),
                reason_invalid=(
                    "Falsified or refined by exact theorem evaluation."
                ),
                lesson=(
                    "Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-FINAL-ROOT-NATURAL-COMMON-SPAN."
                ),
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-MEASUREMENT",
                ],
                evidence=payload.get("headline_metrics", {}),
            )
        )
        upsert_experiment_result(
            ExperimentResultRecord(
                id=(
                    registry_result_id
                    or f"RESULT-{registry_experiment_id}-LATEST"
                ),
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=payload.get("created_at", ""),
                status=payload.get("status", "completed"),
                summary=payload.get("summary", ""),
                metrics=payload.get("headline_metrics", {}),
                falsifiers_triggered=payload.get("falsifiers_triggered", []),
                artifacts={
                    "self_dual_wreath_final_root_natural_common_span": str(path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_final_root_natural_common_span_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
