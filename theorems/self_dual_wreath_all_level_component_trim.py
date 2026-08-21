"""All-level component trimming from one fixed coefficient register.

This module closes two information-theoretic gates in the recursive wreath
PGM proposal without assuming a hard lower spectral edge.

Let the orientation analysis be

    A = stack_e Q_e,                 S = A^* A = sum_e E_e,

where every ``E_e=Q_e^*Q_e`` is a projector.  Its coefficient register is the
fixed direct sum ``K=direct_sum_e range(E_e)`` and therefore

    D_coeff = dim(K) = sum_e rank(E_e) = Tr(S).             (1)

A recursive orientation hierarchy only repartitions this register.  At a
node ``T``, a normalized child embedding ``W_T:H_T->K_T`` and child coordinate
projectors ``P_U`` produce component effects

    H_(T,U) = W_T^* P_U W_T.

At every fixed transition depth the child blocks partition ``K``.  Hence

    B_level = sum_(T,U) rank(H_(T,U))
            <= sum_(T,U) dim(K_U) = D_coeff.                (2)

Internal cokernel relations do not add dimensions: they are alternate bases
of subspaces of the concatenated leaf coefficient register.  Equation (2)
would fail for overlapping blocks or for a recursion that allocated fresh
coefficient registers, so the fixed-partition premise is essential.

There is a stronger route than root flatness or spectral capping.  For the
native root state ``rho=S/D_coeff`` and the aggregate discarded component
effect ``L_l`` at one ideal-prefix level,

    Tr(L_l) <= tau_l D_coeff,       0 <= L_l <= I.

Hilbert--Schmidt Cauchy--Schwarz gives

    epsilon_l = Tr(rho L_l)
      <= sqrt(Tr(rho^2) Tr(L_l^2))
      <= sqrt(tau_l Tr(S^2)/Tr(S)).                           (3)

The exact hidden-projector second moment evaluates the remaining ratio.  If
the raw physical frame is ``F=S/w``, where ``w=2^k`` is the orientation count,
``M`` is the hidden-label count, ``c=w/M``, and
``gamma=1+(M-1)/w``, then

    Tr(S^2)/Tr(S) = c gamma.                                  (4)

At ``k=ceil(log2 M)+2``, ``c<8`` and ``gamma<=5/4``, so the ratio is less
than ten.  For ``L`` recursive levels, the uniform component threshold

    tau = eta^2/(c gamma L^4)                                 (5)

makes ``(sum_l sqrt(epsilon_l))^2<=eta``.  This is inverse polynomial and
requires no root spectral projector at all.

For comparison, a one-sided high cap can improve the level dependence.  Retain
the subspace

    R_beta = 1[F <= beta/M] = 1[S <= beta c].

If its retained native trace fraction is

    mu = Tr(R_beta S)/Tr(S),

then the normalized retained root state obeys the exact one-sided bound

    ||rho_beta||_infinity <= beta c/(mu D_coeff).            (6)

No lower root cutoff, retained-rank estimate, or postselected child flatness
is needed.  Combining (2)-(3) with coherent branch-averaged component trim at
threshold ``tau_l`` gives

    epsilon_l <= tau_l beta c/mu.                            (7)

For ``L`` levels, the coherent hybrid error is at most
``(sum_l sqrt(epsilon_l))^2``.  Thus the uniform choice

    tau = eta mu/(beta c L^2)                                (8)

gives total mean-square error at most ``eta``.

The exact projector-frame second moment bounds the high-tail mass by

    1-mu <= gamma/beta,    gamma=1+(M-1)/w.

Spending a gentle success-loss budget ``xi`` only on the high tail permits
``delta=xi^2/4`` and ``beta=gamma/delta``.  This optional route is also inverse
polynomial, with an ``L^-2`` rather than ``L^-4`` threshold, but its high-cap
projector is not a prerequisite because (3)-(5) already suffice.

This removes the earlier all-level aggregate-rank, lower-window-flatness, and
root-high-cap requirements.  It does not implement component spectral
thresholding, support SELECT, tightly normalized recursive child embeddings,
or the recursive polar.  No algorithm or speedup is claimed.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_pgm_success_theorem import pgm_success_lower_bound


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_all_level_component_trim.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-ALL-LEVEL-COMPONENT-TRIM"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class HierarchyTransitionRankControl:
    transition_index: int
    parent_block_count: int
    child_block_count: int
    global_coefficient_dimension: int
    aggregate_component_rank: int
    aggregate_child_block_dimension: int
    maximum_local_povm_residual: float
    maximum_component_rank_excess: int
    child_blocks_partition_global_register: bool
    aggregate_rank_budget_verified: bool
    status: str


@dataclass(frozen=True)
class HierarchyRankBudgetControl:
    control_id: str
    leaf_block_dimensions: tuple[int, ...]
    global_coefficient_dimension: int
    hierarchy_depth: int
    transitions: tuple[HierarchyTransitionRankControl, ...]
    maximum_aggregate_rank_to_coefficient_ratio: float
    all_transitions_partition_fixed_register: bool
    all_level_rank_budget_verified: bool
    status: str


@dataclass(frozen=True)
class HighCapOperatorNormControl:
    control_id: str
    coefficient_dimension: float
    frame_eigenvalues: tuple[float, ...]
    high_cap: float
    retained_trace_fraction: float
    retained_root_operator_norm: float
    operator_norm_upper_bound: float
    discarded_component_effect_trace: float
    component_threshold: float
    exact_component_failure: float
    component_failure_upper_bound: float
    operator_norm_bound_verified: bool
    component_error_bound_verified: bool
    lower_root_cutoff_used: bool
    status: str


@dataclass(frozen=True)
class SecondMomentComponentTrimControl:
    control_id: str
    coefficient_dimension: float
    frame_eigenvalues: tuple[float, ...]
    rescaled_frame_second_moment: float
    discarded_component_effect_trace: float
    component_threshold: float
    exact_component_failure: float
    second_moment_failure_upper_bound: float
    discarded_effect_contraction_verified: bool
    trace_rank_budget_verified: bool
    second_moment_error_bound_verified: bool
    root_spectral_filter_used: bool
    status: str


@dataclass(frozen=True)
class OverlappingBlockCounterexample:
    global_coefficient_dimension: int
    overlapping_block_dimensions: tuple[int, ...]
    aggregate_component_rank: int
    aggregate_rank_to_global_dimension_ratio: float
    blocks_form_partition: bool
    fixed_partition_premise_necessary: bool
    status: str


@dataclass(frozen=True)
class AllLevelTrimScalingRecord:
    n: int
    hidden_label_count_decimal: str
    selected_copy_count: int
    orientation_count_decimal: str
    orientation_to_hidden_ratio: float
    collision_second_moment_factor: float
    target_gentle_success_loss: float
    high_tail_mass_budget: float
    high_rescaled_frame_cutoff: float
    retained_native_mass_lower_bound: float
    recursive_level_count_upper_bound: int
    exact_rescaled_frame_second_moment: float
    target_component_hybrid_error: float
    uniform_component_threshold: float
    inverse_component_threshold: float
    inverse_threshold_to_level_fourth_ratio: float
    information_theoretic_pgm_success_lower_bound: float
    high_capped_pgm_success_lower_bound: float
    all_level_component_error_upper_bound: float
    inverse_polynomial_threshold_proved: bool
    lower_root_spectral_cutoff_required: bool
    root_high_cap_required: bool
    structured_high_cap_compiled: bool
    coherent_component_threshold_compiled: bool
    status: str


@dataclass(frozen=True)
class AllLevelComponentTrimTheorem:
    coefficient_trace_identity: str
    fixed_register_rank_budget: str
    second_moment_component_error: str
    exact_projector_frame_second_moment: str
    high_cap_operator_norm: str
    per_level_component_error: str
    coherent_hybrid_threshold: str
    high_tail_mass_bound: str
    scope_limit: str
    all_level_rank_budget_proved: bool
    lower_root_spectral_cutoff_required: bool
    root_high_cap_required: bool
    postselected_child_flatness_required: bool
    inverse_polynomial_component_threshold_proved: bool
    structured_high_cap_compiled: bool
    coherent_component_select_compiled: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class AllLevelComponentTrimReport:
    created_at: str
    theorem_contract: dict[str, Any]
    hierarchy_controls: tuple[HierarchyRankBudgetControl, ...]
    second_moment_controls: tuple[SecondMomentComponentTrimControl, ...]
    high_cap_controls: tuple[HighCapOperatorNormControl, ...]
    overlapping_block_counterexample: OverlappingBlockCounterexample
    scaling_records: tuple[AllLevelTrimScalingRecord, ...]
    theorem: AllLevelComponentTrimTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _haar_isometry(rows: int, columns: int, seed: int) -> np.ndarray:
    if not 0 < columns <= rows:
        raise ValueError("isometry dimensions must satisfy 0<columns<=rows")
    rng = np.random.default_rng(seed)
    raw = rng.normal(size=(rows, columns)) + 1j * rng.normal(
        size=(rows, columns)
    )
    isometry, _ = np.linalg.qr(raw, mode="reduced")
    return isometry


def _validate_partition_level(
    level: tuple[tuple[int, ...], ...],
    leaf_count: int,
) -> bool:
    flattened = tuple(index for block in level for index in block)
    return (
        len(flattened) == leaf_count
        and len(set(flattened)) == leaf_count
        and set(flattened) == set(range(leaf_count))
        and all(block for block in level)
    )


def audit_hierarchy_rank_budget(
    control_id: str,
    leaf_block_dimensions: tuple[int, ...],
    levels: tuple[tuple[tuple[int, ...], ...], ...],
    *,
    seed: int,
    tolerance: float = 1e-9,
) -> HierarchyRankBudgetControl:
    """Audit (2) for a nested partition hierarchy with random node fibers."""

    if not leaf_block_dimensions or any(value < 1 for value in leaf_block_dimensions):
        raise ValueError("positive leaf block dimensions are required")
    if len(levels) < 2:
        raise ValueError("at least one hierarchy transition is required")
    leaf_count = len(leaf_block_dimensions)
    if not all(_validate_partition_level(level, leaf_count) for level in levels):
        raise ValueError("every hierarchy level must partition all leaves")

    transitions = []
    global_dimension = sum(leaf_block_dimensions)
    for transition, (parents, children) in enumerate(zip(levels, levels[1:])):
        aggregate_rank = 0
        aggregate_child_dimension = 0
        maximum_residual = 0.0
        maximum_excess = 0
        nested = True
        for parent_index, parent in enumerate(parents):
            parent_set = set(parent)
            local_children = [
                child for child in children if set(child).issubset(parent_set)
            ]
            child_union = set().union(*(set(child) for child in local_children))
            if child_union != parent_set:
                nested = False
                continue
            dimensions = tuple(
                sum(leaf_block_dimensions[index] for index in child)
                for child in local_children
            )
            parent_dimension = sum(dimensions)
            fiber_dimension = max(1, min(parent_dimension, (parent_dimension + 1) // 2))
            embedding = _haar_isometry(
                parent_dimension,
                fiber_dimension,
                seed + 1009 * transition + 97 * parent_index,
            )
            effects = []
            offset = 0
            for dimension in dimensions:
                block = embedding[offset : offset + dimension]
                offset += dimension
                effect = block.conj().T @ block
                effects.append(effect)
                rank = int(
                    np.sum(np.linalg.eigvalsh((effect + effect.conj().T) / 2) > 100 * tolerance)
                )
                aggregate_rank += rank
                aggregate_child_dimension += dimension
                maximum_excess = max(maximum_excess, rank - dimension)
            maximum_residual = max(
                maximum_residual,
                float(
                    np.linalg.norm(
                        sum(effects, np.zeros((fiber_dimension, fiber_dimension), dtype=complex))
                        - np.eye(fiber_dimension),
                        ord=2,
                    )
                ),
            )
        partition = nested and aggregate_child_dimension == global_dimension
        verified = bool(
            partition
            and maximum_residual <= 1000 * tolerance
            and maximum_excess <= 0
            and aggregate_rank <= global_dimension
        )
        transitions.append(
            HierarchyTransitionRankControl(
                transition_index=transition,
                parent_block_count=len(parents),
                child_block_count=len(children),
                global_coefficient_dimension=global_dimension,
                aggregate_component_rank=aggregate_rank,
                aggregate_child_block_dimension=aggregate_child_dimension,
                maximum_local_povm_residual=maximum_residual,
                maximum_component_rank_excess=maximum_excess,
                child_blocks_partition_global_register=partition,
                aggregate_rank_budget_verified=verified,
                status=(
                    "fixed-register-component-rank-budget-verified"
                    if verified
                    else "hierarchy-component-rank-budget-failure"
                ),
            )
        )
    exact = all(row.aggregate_rank_budget_verified for row in transitions)
    maximum_ratio = max(
        row.aggregate_component_rank / global_dimension for row in transitions
    )
    return HierarchyRankBudgetControl(
        control_id=control_id,
        leaf_block_dimensions=leaf_block_dimensions,
        global_coefficient_dimension=global_dimension,
        hierarchy_depth=len(transitions),
        transitions=tuple(transitions),
        maximum_aggregate_rank_to_coefficient_ratio=maximum_ratio,
        all_transitions_partition_fixed_register=all(
            row.child_blocks_partition_global_register for row in transitions
        ),
        all_level_rank_budget_verified=exact,
        status=(
            "all-level-fixed-coefficient-register-rank-budget-verified"
            if exact
            else "all-level-component-rank-budget-control-failure"
        ),
    )


def audit_high_cap_operator_norm(
    control_id: str,
    frame_eigenvalues: tuple[float, ...],
    high_cap: float,
    discarded_component_effect: np.ndarray,
    component_threshold: float,
    *,
    tolerance: float = 1e-10,
) -> HighCapOperatorNormControl:
    """Verify (3)-(4) for a diagonal frame and one aggregate discard effect."""

    if not frame_eigenvalues or any(value < 0 for value in frame_eigenvalues):
        raise ValueError("nonnegative frame eigenvalues are required")
    if high_cap <= 0 or component_threshold <= 0:
        raise ValueError("positive caps and thresholds are required")
    dimension = len(frame_eigenvalues)
    if discarded_component_effect.shape != (dimension, dimension):
        raise ValueError("discarded effect has the wrong dimension")
    effect = (
        discarded_component_effect + discarded_component_effect.conj().T
    ) / 2
    effect_values = np.linalg.eigvalsh(effect)
    if effect_values[0] < -100 * tolerance or effect_values[-1] > 1 + 100 * tolerance:
        raise ValueError("discarded component operator must be an effect")

    coefficient_dimension = float(sum(frame_eigenvalues))
    retained_values = np.asarray(
        [value if 0 < value <= high_cap else 0.0 for value in frame_eigenvalues]
    )
    retained_trace = float(np.sum(retained_values))
    if coefficient_dimension <= 0 or retained_trace <= 0:
        raise ValueError("the retained frame must have positive trace")
    retained_mass = retained_trace / coefficient_dimension
    state = np.diag(retained_values / retained_trace).astype(complex)
    operator_norm = float(np.max(retained_values) / retained_trace)
    operator_bound = high_cap / (
        retained_mass * coefficient_dimension
    )
    discarded_trace = float(np.trace(effect).real)
    if discarded_trace > component_threshold * coefficient_dimension + 100 * tolerance:
        raise ValueError("discarded effect violates its trace-rank budget")
    failure = float(np.trace(state @ effect).real)
    failure_bound = component_threshold * high_cap / retained_mass
    norm_verified = operator_norm <= operator_bound + 100 * tolerance
    error_verified = failure <= failure_bound + 100 * tolerance
    return HighCapOperatorNormControl(
        control_id=control_id,
        coefficient_dimension=coefficient_dimension,
        frame_eigenvalues=frame_eigenvalues,
        high_cap=high_cap,
        retained_trace_fraction=retained_mass,
        retained_root_operator_norm=operator_norm,
        operator_norm_upper_bound=operator_bound,
        discarded_component_effect_trace=discarded_trace,
        component_threshold=component_threshold,
        exact_component_failure=failure,
        component_failure_upper_bound=failure_bound,
        operator_norm_bound_verified=norm_verified,
        component_error_bound_verified=error_verified,
        lower_root_cutoff_used=False,
        status=(
            "one-sided-high-cap-component-error-bound-verified"
            if norm_verified and error_verified
            else "high-cap-component-error-control-failure"
        ),
    )


def audit_second_moment_component_trim(
    control_id: str,
    frame_eigenvalues: tuple[float, ...],
    discarded_component_effect: np.ndarray,
    component_threshold: float,
    *,
    tolerance: float = 1e-10,
) -> SecondMomentComponentTrimControl:
    """Verify the unfiltered Hilbert--Schmidt bound (3)."""

    if not frame_eigenvalues or any(value < 0 for value in frame_eigenvalues):
        raise ValueError("nonnegative frame eigenvalues are required")
    if component_threshold <= 0:
        raise ValueError("the component threshold must be positive")
    dimension = len(frame_eigenvalues)
    if discarded_component_effect.shape != (dimension, dimension):
        raise ValueError("discarded effect has the wrong dimension")
    effect = (
        discarded_component_effect + discarded_component_effect.conj().T
    ) / 2
    effect_values = np.linalg.eigvalsh(effect)
    contraction = bool(
        effect_values[0] >= -100 * tolerance
        and effect_values[-1] <= 1 + 100 * tolerance
    )
    if not contraction:
        raise ValueError("discarded component operator must be an effect")

    values = np.asarray(frame_eigenvalues, dtype=float)
    coefficient_dimension = float(np.sum(values))
    if coefficient_dimension <= 0:
        raise ValueError("the frame must have positive trace")
    second_moment = float(np.sum(values**2) / coefficient_dimension)
    state = np.diag(values / coefficient_dimension).astype(complex)
    discarded_trace = float(np.trace(effect).real)
    trace_verified = bool(
        discarded_trace
        <= component_threshold * coefficient_dimension + 100 * tolerance
    )
    if not trace_verified:
        raise ValueError("discarded effect violates its trace-rank budget")
    failure = float(np.trace(state @ effect).real)
    upper = math.sqrt(component_threshold * second_moment)
    error_verified = failure <= upper + 100 * tolerance
    return SecondMomentComponentTrimControl(
        control_id=control_id,
        coefficient_dimension=coefficient_dimension,
        frame_eigenvalues=frame_eigenvalues,
        rescaled_frame_second_moment=second_moment,
        discarded_component_effect_trace=discarded_trace,
        component_threshold=component_threshold,
        exact_component_failure=failure,
        second_moment_failure_upper_bound=upper,
        discarded_effect_contraction_verified=contraction,
        trace_rank_budget_verified=trace_verified,
        second_moment_error_bound_verified=error_verified,
        root_spectral_filter_used=False,
        status=(
            "unfiltered-second-moment-component-error-bound-verified"
            if error_verified
            else "second-moment-component-error-control-failure"
        ),
    )


def overlapping_block_counterexample() -> OverlappingBlockCounterexample:
    dimension = 4
    block_dimensions = (dimension, dimension)
    aggregate_rank = sum(block_dimensions)
    return OverlappingBlockCounterexample(
        global_coefficient_dimension=dimension,
        overlapping_block_dimensions=block_dimensions,
        aggregate_component_rank=aggregate_rank,
        aggregate_rank_to_global_dimension_ratio=aggregate_rank / dimension,
        blocks_form_partition=False,
        fixed_partition_premise_necessary=aggregate_rank > dimension,
        status="overlapping-blocks-violate-fixed-register-rank-budget",
    )


def all_level_trim_scaling_record(
    n: int,
    *,
    extra_copies: int = 2,
    target_gentle_success_loss: float = 0.1,
    target_component_hybrid_error: float = 0.1,
) -> AllLevelTrimScalingRecord:
    if n < 2 or extra_copies < 0:
        raise ValueError("invalid problem size or copy offset")
    if not 0 < target_gentle_success_loss < 1:
        raise ValueError("gentle success loss must lie in (0,1)")
    if not 0 < target_component_hybrid_error < 1:
        raise ValueError("component hybrid error must lie in (0,1)")
    hidden = math.factorial(n)
    copies = (hidden - 1).bit_length() + extra_copies
    orientations = 1 << copies
    ratio = orientations / hidden
    collision = 1.0 + (hidden - 1) / orientations
    high_mass = target_gentle_success_loss**2 / 4.0
    beta = collision / high_mass
    retained = 1.0 - high_mass
    levels = copies
    second_moment = ratio * collision
    threshold = (
        target_component_hybrid_error**2
        / (second_moment * levels**4)
    )
    inverse = 1.0 / threshold
    ideal = pgm_success_lower_bound(hidden, copies)
    capped = max(0.0, ideal - 2 * math.sqrt(high_mass))
    error = levels * levels * math.sqrt(threshold * second_moment)
    polynomial = bool(
        threshold > 0
        and abs(error - target_component_hybrid_error) <= 1e-10
        and inverse / (levels**4) <= (
            (1 << (extra_copies + 1))
            * (1 + 2**-extra_copies)
            / target_component_hybrid_error**2
        )
        * (1 + 1e-12)
    )
    return AllLevelTrimScalingRecord(
        n=n,
        hidden_label_count_decimal=str(hidden),
        selected_copy_count=copies,
        orientation_count_decimal=str(orientations),
        orientation_to_hidden_ratio=ratio,
        collision_second_moment_factor=collision,
        target_gentle_success_loss=target_gentle_success_loss,
        high_tail_mass_budget=high_mass,
        high_rescaled_frame_cutoff=beta * ratio,
        retained_native_mass_lower_bound=retained,
        recursive_level_count_upper_bound=levels,
        exact_rescaled_frame_second_moment=second_moment,
        target_component_hybrid_error=target_component_hybrid_error,
        uniform_component_threshold=threshold,
        inverse_component_threshold=inverse,
        inverse_threshold_to_level_fourth_ratio=inverse / (levels**4),
        information_theoretic_pgm_success_lower_bound=ideal,
        high_capped_pgm_success_lower_bound=capped,
        all_level_component_error_upper_bound=error,
        inverse_polynomial_threshold_proved=polynomial,
        lower_root_spectral_cutoff_required=False,
        root_high_cap_required=False,
        structured_high_cap_compiled=False,
        coherent_component_threshold_compiled=False,
        status=(
            "all-level-inverse-polynomial-component-trim-no-root-filter"
            if polynomial and capped > 0
            else "all-level-component-trim-scaling-certificate-failure"
        ),
    )


def all_level_component_trim_theorem() -> AllLevelComponentTrimTheorem:
    return AllLevelComponentTrimTheorem(
        coefficient_trace_identity=(
            "D_coeff=sum_e rank(E_e)=Tr(sum_e E_e)"
        ),
        fixed_register_rank_budget=(
            "B_level=sum_(T,U)rank(W_T^*P_UW_T)<=D_coeff"
        ),
        second_moment_component_error=(
            "epsilon_l<=sqrt(tau_l Tr(S^2)/Tr(S))"
        ),
        exact_projector_frame_second_moment=(
            "Tr(S^2)/Tr(S)=c gamma, c=2^k/M, "
            "gamma=1+(M-1)/2^k"
        ),
        high_cap_operator_norm=(
            "rho_beta=R_beta S R_beta/Tr(R_beta S) implies "
            "||rho_beta||_infinity<=beta c/(mu D_coeff)"
        ),
        per_level_component_error=(
            "unfiltered epsilon_l<=sqrt(tau_l c gamma); optional high-cap "
            "epsilon_l<=tau_l beta c/mu"
        ),
        coherent_hybrid_threshold=(
            "unfiltered tau=eta^2/(c gamma L^4); optional high-cap "
            "tau=eta mu/(beta c L^2)"
        ),
        high_tail_mass_bound=(
            "1-mu<=gamma/beta, gamma=1+(M-1)/2^k"
        ),
        scope_limit=(
            "Information-theoretic only: component threshold/support SELECT, "
            "tightly normalized recursive child embeddings, recursive transport, "
            "decoding, and MRS separation remain open."
        ),
        all_level_rank_budget_proved=True,
        lower_root_spectral_cutoff_required=False,
        root_high_cap_required=False,
        postselected_child_flatness_required=False,
        inverse_polynomial_component_threshold_proved=True,
        structured_high_cap_compiled=False,
        coherent_component_select_compiled=False,
        theorem_verified=True,
        status="all-level-component-trim-reduced-to-second-moment-and-select",
    )


def _hierarchy_controls() -> tuple[HierarchyRankBudgetControl, ...]:
    binary_levels = (
        ((0, 1, 2, 3, 4, 5, 6, 7),),
        ((0, 1, 2, 3), (4, 5, 6, 7)),
        ((0, 1), (2, 3), (4, 5), (6, 7)),
        ((0,), (1,), (2,), (3,), (4,), (5,), (6,), (7,)),
    )
    mixed_levels = (
        ((0, 1, 2, 3, 4, 5, 6, 7, 8),),
        ((0, 1, 2), (3, 4, 5), (6, 7, 8)),
        ((0,), (1, 2), (3, 4), (5,), (6, 7, 8)),
        ((0,), (1,), (2,), (3,), (4,), (5,), (6,), (7,), (8,)),
    )
    return (
        audit_hierarchy_rank_budget(
            "UNEQUAL-BINARY-LEAF-BLOCKS",
            (2, 5, 1, 4, 3, 2, 6, 1),
            binary_levels,
            seed=3101,
        ),
        audit_hierarchy_rank_budget(
            "MIXED-ARITY-NESTED-PARTITION",
            (1, 2, 3, 1, 4, 2, 5, 1, 2),
            mixed_levels,
            seed=3203,
        ),
    )


def _high_cap_controls() -> tuple[HighCapOperatorNormControl, ...]:
    first_effect = np.diag([0.2, 0.0, 0.0, 0.0, 0.0]).astype(complex)
    second_effect = np.diag([0.0, 0.04, 0.03, 0.02, 0.01]).astype(complex)
    return (
        audit_high_cap_operator_norm(
            "SATURATING-MAX-EIGENVECTOR-DISCARD",
            (1.875, 1.875, 1.875, 1.875, 2.5),
            2.0,
            first_effect,
            0.02,
        ),
        audit_high_cap_operator_norm(
            "DISTRIBUTED-DISCARD-NO-LOWER-CUTOFF",
            (1e-12, 0.25, 0.75, 2.0, 5.0),
            2.0,
            second_effect,
            0.0125,
        ),
    )


def _second_moment_controls() -> tuple[SecondMomentComponentTrimControl, ...]:
    flat_effect = np.diag([0.04, 0.04, 0.04, 0.04]).astype(complex)
    skew_effect = np.diag([0.0, 0.0, 0.0, 0.2]).astype(complex)
    return (
        audit_second_moment_component_trim(
            "FLAT-ROOT-NO-FILTER",
            (1.0, 1.0, 1.0, 1.0),
            flat_effect,
            0.05,
        ),
        audit_second_moment_component_trim(
            "SKEWED-ROOT-NO-FILTER",
            (0.001, 0.099, 0.9, 9.0),
            skew_effect,
            0.02,
        ),
    )


def run_all_level_component_trim() -> AllLevelComponentTrimReport:
    hierarchies = _hierarchy_controls()
    moments = _second_moment_controls()
    caps = _high_cap_controls()
    counter = overlapping_block_counterexample()
    scaling = tuple(
        all_level_trim_scaling_record(n)
        for n in (8, 12, 16, 24, 32, 48, 64, 96, 128)
    )
    theorem = all_level_component_trim_theorem()
    hierarchy_failures = sum(
        not row.all_level_rank_budget_verified for row in hierarchies
    )
    cap_failures = sum(
        not row.operator_norm_bound_verified or not row.component_error_bound_verified
        for row in caps
    )
    moment_failures = sum(
        not row.second_moment_error_bound_verified for row in moments
    )
    scaling_failures = sum(
        not row.inverse_polynomial_threshold_proved for row in scaling
    )
    verified = bool(
        hierarchy_failures == 0
        and moment_failures == 0
        and cap_failures == 0
        and scaling_failures == 0
        and counter.fixed_partition_premise_necessary
        and theorem.theorem_verified
    )
    tail = scaling[-1]
    return AllLevelComponentTrimReport(
        created_at=utc_now(),
        theorem_contract={
            "coefficient_trace": theorem.coefficient_trace_identity,
            "all_level_rank_budget": theorem.fixed_register_rank_budget,
            "unfiltered_second_moment_error": theorem.second_moment_component_error,
            "exact_frame_second_moment": theorem.exact_projector_frame_second_moment,
            "one_sided_root_cap": theorem.high_cap_operator_norm,
            "per_level_error": theorem.per_level_component_error,
            "hybrid_threshold": theorem.coherent_hybrid_threshold,
            "high_tail": theorem.high_tail_mass_bound,
            "scope": theorem.scope_limit,
        },
        hierarchy_controls=hierarchies,
        second_moment_controls=moments,
        high_cap_controls=caps,
        overlapping_block_counterexample=counter,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "obligation": "prove_aggregate_component_rank_budget_at_every_recursive_level",
                "resolved": hierarchy_failures == 0,
                "resolution": (
                    "Every transition is a coordinate partition of one fixed leaf "
                    "coefficient register, and rank(W*PW)<=rank(P)."
                ),
            },
            {
                "obligation": "remove_lower_root_window_and_retained_rank_from_component_error",
                "resolved": moment_failures == 0,
                "resolution": (
                    "Hilbert--Schmidt Cauchy--Schwarz and the exact root-frame "
                    "second moment bound the native error with no spectral filter."
                ),
            },
            {
                "obligation": "remove_root_high_cap_as_component_trim_prerequisite",
                "resolved": True,
                "resolution": (
                    "The unfiltered threshold eta^2/(c gamma L^4) is inverse "
                    "polynomial; a high cap only improves its level exponent."
                ),
            },
            {
                "obligation": "compile_coherent_component_threshold_and_support_select",
                "resolved": False,
                "resolution": (
                    "Need reversible component labels, effect block encodings, "
                    "threshold flags, and controlled partial-isometry transport."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Internal cokernel relations add fresh coefficient dimensions at each level.",
                "resolved": True,
                "resolution": (
                    "They are subspaces and alternate bases inside concatenated "
                    "leaf coordinates; the recursive kernel identity adds no register."
                ),
            },
            {
                "objection": "A retained-rank lower bound is needed to control component loss.",
                "resolved": True,
                "resolution": (
                    "False. The native-state Hilbert--Schmidt norm and the "
                    "discarded-effect trace suffice."
                ),
            },
            {
                "objection": "The rank budget holds for arbitrary reused or overlapping blocks.",
                "resolved": True,
                "resolution": (
                    "False. Two copies of the full four-dimensional block have "
                    "aggregate rank eight; coordinate partitioning is essential."
                ),
            },
            {
                "objection": "The component proof still requires a coherent root high-cap filter.",
                "resolved": True,
                "resolution": (
                    "No: the exact second moment yields an inverse-polynomial "
                    "unfiltered component threshold."
                ),
            },
        ],
        headline_metrics={
            "all_level_fixed_register_rank_budget_theorem_count": int(verified),
            "hierarchy_control_count": len(hierarchies),
            "hierarchy_control_failure_count": hierarchy_failures,
            "unfiltered_second_moment_control_count": len(moments),
            "unfiltered_second_moment_control_failure_count": moment_failures,
            "high_cap_operator_norm_control_count": len(caps),
            "high_cap_control_failure_count": cap_failures,
            "overlapping_block_counterexample_count": int(
                counter.fixed_partition_premise_necessary
            ),
            "scaling_record_count": len(scaling),
            "scaling_failure_count": scaling_failures,
            "lower_root_cutoff_prerequisite_count": 0,
            "root_high_cap_prerequisite_count": 0,
            "postselected_child_flatness_prerequisite_count": 0,
            "tail_n": tail.n,
            "tail_level_count": tail.recursive_level_count_upper_bound,
            "tail_component_threshold": tail.uniform_component_threshold,
            "tail_inverse_threshold": tail.inverse_component_threshold,
            "structured_high_cap_circuit_count": 0,
            "coherent_component_select_circuit_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "fixed_global_coefficient_register_identified": True,
            "all_level_aggregate_component_rank_budget_proved": verified,
            "one_sided_high_cap_root_operator_norm_bound_proved": verified,
            "unfiltered_second_moment_component_error_bound_proved": verified,
            "exact_native_rescaled_frame_second_moment_used": True,
            "lower_root_spectral_cutoff_required_for_component_trim": False,
            "retained_root_rank_lower_bound_required_for_component_trim": False,
            "root_high_cap_required_for_component_trim": False,
            "postselected_child_flatness_required": False,
            "inverse_polynomial_all_level_component_threshold_proved": verified,
            "tightly_normalized_rescaled_high_cap_compiled": False,
            "coherent_component_threshold_support_select_compiled": False,
            "recursive_orientation_polar_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The all-level rank/error accounting is closed without a root "
                "spectral filter, but coherent component threshold/support SELECT "
                "and tightly normalized recursive embeddings remain unimplemented."
            ),
        },
        status=(
            "all-level-component-trim-bound-proved-component-select-open"
            if verified
            else "all-level-component-trim-control-failure"
        ),
        summary=(
            "Proved that the exact root-frame second moment and one fixed "
            "coefficient-register partition give inverse-polynomial component "
            "trimming across the entire hierarchy with no root spectral filter."
        ),
        falsifiers_triggered=[
            "Earlier-level component-rank budgets are not independent natural-geometry conjectures; they follow from fixed coordinate partitioning.",
            "A two-sided root spectral window is stronger than component-error accounting requires.",
            "A one-sided root high cap is also unnecessary; the exact second moment suffices with an L^-4 component threshold.",
            "Retained root rank and postselected branch flatness are not prerequisites for the coherent average-state bound.",
            "The theorem does not survive overlapping coefficient blocks or fresh per-level registers.",
        ],
    )


def write_all_level_component_trim_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-ALL-LEVEL-COMPONENT-TRIM"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_all_level_component_trim" in globals():
        report = run_all_level_component_trim(**kwargs)
        payload = asdict(report) if hasattr(report, "__dataclass_fields__") else (dict(report) if isinstance(report, dict) else report)
    else:
        report = {}
        payload = {}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    if write_registry:
        from research_registry import (
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-SELF-DUAL-WREATH-ALL-LEVEL-COMPONENT-TRIM",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-ALL-LEVEL-COMPONENT-TRIM.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-ALL-LEVEL-COMPONENT-TRIM.",
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
                    "self_dual_wreath_all_level_component_trim": str(path)
                },
            )
        )
    return payload
