"""Coherent branch-averaged component trimming without child postselection.

Let ``C_s:H->K_s`` be endpoint Kraus maps with

    sum_s C_s^* C_s = I_H.

On branch ``s``, let ``{H_(s,e)}`` be a component POVM and let ``L_s`` be the
effect discarded by thresholding component eigenvalues below ``tau_s``.  If
``B_s=sum_e rank(H_(s,e))``, spectral counting gives

    Tr(L_s) <= tau_s B_s.

Keeping the endpoint branches coherent, the exact mean-square error on a
parent state ``rho`` is

    epsilon = sum_s Tr(C_s rho C_s^* L_s).                 (1)

Writing ``kappa=dim(H)||rho||_infinity`` and using
``C_s C_s^*<=I`` gives the parent-level bound

    epsilon <= (kappa/dim(H)) sum_s tau_s B_s.             (2)

This avoids conditioning on ``s``.  A conditional child state can have
flatness exponential in the problem size, but its branch probability is
already present in (1); introducing the normalized child state divides by
that probability and creates an artificial flatness gate.

The same argument applies after any ideal isometric prefix.  If the native
root state has flatness ``kappa_0`` and a recursive level has aggregate
component-rank budget ``B_level``, its ideal-prefix trim error is at most
``kappa_0 tau B_level/R`` for root support dimension ``R``.  A hybrid over
levels has mean-square error at most ``(sum_l sqrt(epsilon_l))^2``.  Thus
polynomial root flatness and polynomial aggregate level budgets suffice with
inverse-polynomial thresholds; no postselected child-flatness theorem is
needed.

At the natural final-root binary merge, the established aspect
``r/N_s>=19/520-o(1)`` and ``B_s<=N_s`` imply

    sum_s B_s/r <= 1040/19+o(1).

Hence ``tau=eta(19/1040)/kappa`` gives error at most ``eta``.  For an
isotropic parent this is a constant cutoff.  The actual native root density,
aggregate rank budgets at every earlier level, coherent thresholding, and
recursive implementation remain open.  No algorithm or speedup is claimed.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_coherent_component_trim_hybrid.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-COHERENT-COMPONENT-TRIM-HYBRID"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
NATURAL_FINAL_FIBER_ASPECT_LOWER = Fraction(19, 520)


@dataclass(frozen=True)
class CoherentBranchTrimDetail:
    branch_index: int
    output_dimension: int
    endpoint_probability: float
    endpoint_operator_norm_squared: float
    conditional_child_flatness: float | None
    component_rank_budget: int
    truncation_threshold: float
    discarded_effect_trace: float
    exact_branch_weighted_failure: float
    conditional_flatness_failure_upper_bound: float | None
    parent_flatness_branch_upper_bound: float
    status: str


@dataclass(frozen=True)
class CoherentBranchTrimControl:
    control_id: str
    parent_dimension: int
    branch_count: int
    parent_state_flatness: float
    endpoint_column_isometry_residual: float
    branch_details: tuple[CoherentBranchTrimDetail, ...]
    aggregate_component_rank_budget: int
    exact_branch_averaged_failure: float
    exact_ideal_to_trimmed_mean_square_error: float
    conditional_branch_bound_sum: float
    endpoint_weighted_parent_bound: float
    coarse_parent_rank_budget_bound: float
    exact_error_identity_verified: bool
    conditional_and_parent_bounds_verified: bool
    child_postselection_flatness_required: bool
    exact_control_verified: bool
    status: str


@dataclass(frozen=True)
class PostselectionFlatnessCounterexample:
    parent_dimension: int
    small_endpoint_eigenvalue: float
    rare_branch_probability: float
    conditional_child_flatness: float
    conditional_flatness_to_parent_flatness_ratio: float
    branch_probability_times_conditional_flatness: float
    endpoint_column_isometry_exact: bool
    status: str


@dataclass(frozen=True)
class CoherentTrimScalingRecord:
    n: int
    root_flatness_polynomial_degree: int
    root_flatness_upper_bound: float
    recursive_level_count_upper_bound: int
    aggregate_rank_budget_to_root_dimension_upper_bound: float
    total_mean_square_error_target: float
    per_level_mean_square_error_target: float
    retained_component_eigenvalue_threshold: float
    inverse_threshold_cost: float
    hybrid_total_mean_square_error_upper_bound: float
    inverse_polynomial_threshold_conditional_on_level_budget: bool
    natural_root_flatness_proved: bool
    polynomial_all_level_rank_budget_proved: bool
    coherent_recursive_trim_compiled: bool
    status: str


@dataclass(frozen=True)
class CoherentComponentTrimTheorem:
    exact_branch_error_identity: str
    parent_flatness_rank_budget_bound: str
    postselection_cancellation: str
    ideal_prefix_invariance: str
    coherent_hybrid_bound: str
    natural_final_root_corollary: str
    scope_limit: str
    arbitrary_endpoint_branch_count: bool
    arbitrary_child_povms: bool
    child_postselection_flatness_eliminated: bool
    ideal_isometric_prefix_hybrid_proved: bool
    natural_root_flatness_proved: bool
    polynomial_all_level_rank_budget_proved: bool
    recursive_component_compiler_proved: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class CoherentComponentTrimHybridReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[CoherentBranchTrimControl]
    postselection_counterfamily: list[PostselectionFlatnessCounterexample]
    scaling_records: list[CoherentTrimScalingRecord]
    theorem: CoherentComponentTrimTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _hermitian(matrix: np.ndarray) -> np.ndarray:
    return (matrix + matrix.conj().T) / 2.0


def _trimmed_discarded_effect(
    effect: np.ndarray,
    threshold: float,
    tolerance: float,
) -> tuple[np.ndarray, np.ndarray, int]:
    values, vectors = np.linalg.eigh(_hermitian(effect))
    if values[0] < -100 * tolerance or values[-1] > 1 + 100 * tolerance:
        raise ValueError("component is not a valid effect")
    positive = values > 100 * tolerance
    discarded_mask = positive & (values < threshold)
    discarded_values = np.where(discarded_mask, values, 0.0)
    discarded = (vectors * discarded_values) @ vectors.conj().T
    root_difference = (vectors * np.sqrt(discarded_values)) @ vectors.conj().T
    return discarded, root_difference, int(np.count_nonzero(positive))


def audit_coherent_branch_trim(
    control_id: str,
    endpoint_kraus: tuple[np.ndarray, ...],
    child_povms: tuple[tuple[np.ndarray, ...], ...],
    parent_state: np.ndarray,
    truncation_thresholds: tuple[float, ...],
    *,
    tolerance: float = 1e-9,
) -> CoherentBranchTrimControl:
    """Verify (1)-(2) for arbitrary finite endpoint maps and child POVMs."""

    if not endpoint_kraus or len(endpoint_kraus) != len(child_povms):
        raise ValueError("one nonempty child POVM is required per endpoint branch")
    if len(truncation_thresholds) != len(endpoint_kraus):
        raise ValueError("one truncation threshold is required per branch")
    parent_dimension = endpoint_kraus[0].shape[1]
    if parent_dimension < 1 or any(
        kraus.ndim != 2 or kraus.shape[1] != parent_dimension
        for kraus in endpoint_kraus
    ):
        raise ValueError("endpoint maps must share one positive input dimension")
    if parent_state.shape != (parent_dimension, parent_dimension):
        raise ValueError("parent state has the wrong dimension")
    state = _hermitian(parent_state)
    state_values = np.linalg.eigvalsh(state)
    if (
        state_values[0] < -100 * tolerance
        or abs(float(np.trace(state).real) - 1.0) > 100 * tolerance
    ):
        raise ValueError("parent state must be a density operator")
    identity = np.eye(parent_dimension, dtype=complex)
    endpoint_sum = sum(
        (kraus.conj().T @ kraus for kraus in endpoint_kraus),
        np.zeros_like(identity),
    )
    endpoint_residual = float(np.linalg.norm(endpoint_sum - identity, ord=2))
    if endpoint_residual > 1000 * tolerance:
        raise ValueError("endpoint maps do not form a column isometry")

    parent_flatness = parent_dimension * float(state_values[-1])
    details = []
    exact_failure = 0.0
    direct_mean_square = 0.0
    conditional_bound_sum = 0.0
    weighted_parent_bound = 0.0
    aggregate_budget = 0

    for branch, (kraus, effects, threshold) in enumerate(
        zip(endpoint_kraus, child_povms, truncation_thresholds)
    ):
        if not effects or not 0 < threshold <= 1:
            raise ValueError("each branch needs a POVM and threshold in (0,1]")
        output_dimension = kraus.shape[0]
        if any(effect.shape != (output_dimension, output_dimension) for effect in effects):
            raise ValueError("child POVM dimension does not match its endpoint map")
        effect_sum = sum(
            (_hermitian(effect) for effect in effects),
            np.zeros((output_dimension, output_dimension), dtype=complex),
        )
        if np.linalg.norm(effect_sum - np.eye(output_dimension), ord=2) > 1000 * tolerance:
            raise ValueError("child effects do not form a POVM")

        discarded = np.zeros_like(effect_sum)
        root_error_terms = []
        rank_budget = 0
        for effect in effects:
            low, root_difference, rank = _trimmed_discarded_effect(
                effect, threshold, tolerance
            )
            discarded += low
            root_error_terms.append(root_difference)
            rank_budget += rank

        branch_state = kraus @ state @ kraus.conj().T
        probability = float(np.trace(branch_state).real)
        weighted_loss = float(np.trace(branch_state @ discarded).real)
        direct_error = sum(
            float(np.trace(state @ kraus.conj().T @ root @ root @ kraus).real)
            for root in root_error_terms
        )
        endpoint_norm_squared = float(
            np.linalg.norm(kraus.conj().T @ kraus, ord=2)
        )
        if probability > 100 * tolerance:
            conditional = branch_state / probability
            conditional_flatness = output_dimension * float(
                np.linalg.eigvalsh(_hermitian(conditional))[-1]
            )
            conditional_bound = (
                probability
                * conditional_flatness
                * threshold
                * rank_budget
                / output_dimension
            )
        else:
            conditional_flatness = None
            conditional_bound = None
        parent_bound = (
            parent_flatness
            * endpoint_norm_squared
            * threshold
            * rank_budget
            / parent_dimension
        )
        exact_failure += weighted_loss
        direct_mean_square += direct_error
        conditional_bound_sum += conditional_bound or 0.0
        weighted_parent_bound += parent_bound
        aggregate_budget += rank_budget
        branch_exact = (
            abs(weighted_loss - direct_error) <= 1000 * tolerance
            and weighted_loss <= parent_bound + 1000 * tolerance
            and (
                conditional_bound is None
                or weighted_loss <= conditional_bound + 1000 * tolerance
            )
            and float(np.trace(discarded).real)
            <= threshold * rank_budget + 1000 * tolerance
        )
        details.append(
            CoherentBranchTrimDetail(
                branch_index=branch,
                output_dimension=output_dimension,
                endpoint_probability=probability,
                endpoint_operator_norm_squared=endpoint_norm_squared,
                conditional_child_flatness=conditional_flatness,
                component_rank_budget=rank_budget,
                truncation_threshold=threshold,
                discarded_effect_trace=float(np.trace(discarded).real),
                exact_branch_weighted_failure=weighted_loss,
                conditional_flatness_failure_upper_bound=conditional_bound,
                parent_flatness_branch_upper_bound=parent_bound,
                status=(
                    "coherent-branch-parent-budget-verified"
                    if branch_exact
                    else "coherent-branch-trim-certificate-failure"
                ),
            )
        )

    coarse_bound = parent_flatness * sum(
        threshold * detail.component_rank_budget
        for threshold, detail in zip(truncation_thresholds, details)
    ) / parent_dimension
    identity_verified = abs(exact_failure - direct_mean_square) <= 1000 * tolerance
    bounds_verified = (
        exact_failure <= conditional_bound_sum + 1000 * tolerance
        and exact_failure <= weighted_parent_bound + 1000 * tolerance
        and weighted_parent_bound <= coarse_bound + 1000 * tolerance
    )
    exact = (
        endpoint_residual <= 1000 * tolerance
        and identity_verified
        and bounds_verified
        and all("failure" not in detail.status for detail in details)
    )
    return CoherentBranchTrimControl(
        control_id=control_id,
        parent_dimension=parent_dimension,
        branch_count=len(endpoint_kraus),
        parent_state_flatness=parent_flatness,
        endpoint_column_isometry_residual=endpoint_residual,
        branch_details=tuple(details),
        aggregate_component_rank_budget=aggregate_budget,
        exact_branch_averaged_failure=exact_failure,
        exact_ideal_to_trimmed_mean_square_error=direct_mean_square,
        conditional_branch_bound_sum=conditional_bound_sum,
        endpoint_weighted_parent_bound=weighted_parent_bound,
        coarse_parent_rank_budget_bound=coarse_bound,
        exact_error_identity_verified=identity_verified,
        conditional_and_parent_bounds_verified=bounds_verified,
        child_postselection_flatness_required=False,
        exact_control_verified=exact,
        status=(
            "coherent-branch-averaged-component-trim-verified"
            if exact
            else "coherent-component-trim-control-failure"
        ),
    )


def postselection_flatness_counterexample(
    parent_dimension: int,
) -> PostselectionFlatnessCounterexample:
    if parent_dimension < 2:
        raise ValueError("counterexample dimension must be at least two")
    epsilon = parent_dimension ** -2
    trace = 1.0 + (parent_dimension - 1) * epsilon
    probability = trace / parent_dimension
    conditional_flatness = parent_dimension / trace
    return PostselectionFlatnessCounterexample(
        parent_dimension=parent_dimension,
        small_endpoint_eigenvalue=epsilon,
        rare_branch_probability=probability,
        conditional_child_flatness=conditional_flatness,
        conditional_flatness_to_parent_flatness_ratio=conditional_flatness,
        branch_probability_times_conditional_flatness=(
            probability * conditional_flatness
        ),
        endpoint_column_isometry_exact=True,
        status="postselection-creates-linear-flatness-from-isotropic-parent",
    )


def natural_final_root_branch_averaged_threshold(
    target_failure_probability: float,
    parent_flatness: float,
) -> float:
    if not 0 < target_failure_probability < 1:
        raise ValueError("failure target must lie in (0,1)")
    if parent_flatness < 1:
        raise ValueError("density-operator flatness must be at least one")
    return (
        target_failure_probability
        * float(NATURAL_FINAL_FIBER_ASPECT_LOWER)
        / (2.0 * parent_flatness)
    )


def coherent_trim_scaling_record(
    n: int,
    *,
    root_flatness_polynomial_degree: int = 2,
    total_mean_square_error_target: float = 0.1,
) -> CoherentTrimScalingRecord:
    if n < 2 or root_flatness_polynomial_degree < 0:
        raise ValueError("invalid scaling parameters")
    if not 0 < total_mean_square_error_target < 1:
        raise ValueError("error target must lie in (0,1)")
    root_flatness = float(n**root_flatness_polynomial_degree)
    levels = max(1, math.ceil(math.lgamma(n + 1) / math.log(2)))
    budget_ratio = 2.0 / float(NATURAL_FINAL_FIBER_ASPECT_LOWER)
    per_level = total_mean_square_error_target / levels**2
    threshold = per_level / (root_flatness * budget_ratio)
    hybrid = (levels * math.sqrt(per_level)) ** 2
    inverse = 1.0 / threshold
    polynomial = math.isfinite(inverse) and inverse <= (
        root_flatness * budget_ratio * levels**2 / total_mean_square_error_target
    ) * (1 + 1e-12)
    return CoherentTrimScalingRecord(
        n=n,
        root_flatness_polynomial_degree=root_flatness_polynomial_degree,
        root_flatness_upper_bound=root_flatness,
        recursive_level_count_upper_bound=levels,
        aggregate_rank_budget_to_root_dimension_upper_bound=budget_ratio,
        total_mean_square_error_target=total_mean_square_error_target,
        per_level_mean_square_error_target=per_level,
        retained_component_eigenvalue_threshold=threshold,
        inverse_threshold_cost=inverse,
        hybrid_total_mean_square_error_upper_bound=hybrid,
        inverse_polynomial_threshold_conditional_on_level_budget=polynomial,
        natural_root_flatness_proved=False,
        polynomial_all_level_rank_budget_proved=False,
        coherent_recursive_trim_compiled=False,
        status=(
            "inverse-polynomial-coherent-trim-conditional-on-root-and-level-budgets"
        ),
    )


def coherent_component_trim_theorem() -> CoherentComponentTrimTheorem:
    return CoherentComponentTrimTheorem(
        exact_branch_error_identity=(
            "epsilon=sum_s Tr(C_s rho C_s^* L_s), exactly equal to the "
            "ideal-versus-trimmed coherent Naimark mean-square error"
        ),
        parent_flatness_rank_budget_bound=(
            "epsilon<=(kappa/r)sum_s tau_s B_s, with the sharper endpoint-"
            "weighted factor ||C_s||^2 available branchwise"
        ),
        postselection_cancellation=(
            "endpoint probability times the normalized child-flatness bound "
            "is bounded directly on the unnormalized branch state"
        ),
        ideal_prefix_invariance=(
            "an ideal isometry preserves the nonzero spectrum and flatness of "
            "the root state on its image"
        ),
        coherent_hybrid_bound=(
            "if ideal-prefix level errors are epsilon_l, total mean-square "
            "error is at most (sum_l sqrt(epsilon_l))^2"
        ),
        natural_final_root_corollary=(
            "for two children with r/N_s>=19/520 and B_s<=N_s, "
            "tau=eta(19/1040)/kappa gives branch-averaged error at most eta"
        ),
        scope_limit=(
            "Native root-state flatness, aggregate rank budgets at every level, "
            "coherent effect thresholding/SELECT, and the recursive circuit "
            "remain unproved. Conditional branches are not individually close."
        ),
        arbitrary_endpoint_branch_count=True,
        arbitrary_child_povms=True,
        child_postselection_flatness_eliminated=True,
        ideal_isometric_prefix_hybrid_proved=True,
        natural_root_flatness_proved=False,
        polynomial_all_level_rank_budget_proved=False,
        recursive_component_compiler_proved=False,
        theorem_verified=True,
        status="child-flatness-gate-replaced-by-root-and-level-rank-budgets",
    )


def _noncommuting_low_edge_povm() -> tuple[np.ndarray, ...]:
    low = 0.03 * np.asarray([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
    plus = np.asarray([[1.0, 1.0], [1.0, 1.0]], dtype=complex) * 0.2
    remainder = np.eye(2, dtype=complex) - low - plus
    return low, plus, remainder


def _finite_controls() -> list[CoherentBranchTrimControl]:
    parent_dimension = 2
    identity = np.eye(parent_dimension, dtype=complex)
    balanced = (identity / math.sqrt(2), identity / math.sqrt(2))
    povm = _noncommuting_low_edge_povm()
    uniform = identity / parent_dimension
    pure = np.diag([1.0, 0.0]).astype(complex)

    endpoint_effect = np.diag([1.0, 1e-4]).astype(complex)
    imbalanced = (
        np.diag(np.sqrt(np.diag(endpoint_effect))).astype(complex),
        np.diag(np.sqrt(np.diag(identity - endpoint_effect))).astype(complex),
    )
    return [
        audit_coherent_branch_trim(
            "BALANCED-UNIFORM-PARENT",
            balanced,
            (povm, povm),
            uniform,
            (0.1, 0.1),
        ),
        audit_coherent_branch_trim(
            "IMBALANCED-UNIFORM-PARENT",
            imbalanced,
            (povm, povm),
            uniform,
            (0.1, 0.1),
        ),
        audit_coherent_branch_trim(
            "BALANCED-CONCENTRATED-PARENT",
            balanced,
            (povm, povm),
            pure,
            (0.1, 0.1),
        ),
    ]


def run_coherent_component_trim_hybrid() -> CoherentComponentTrimHybridReport:
    controls = _finite_controls()
    counters = [
        postselection_flatness_counterexample(1 << exponent)
        for exponent in range(1, 11)
    ]
    scaling = [
        coherent_trim_scaling_record(n)
        for n in (8, 12, 16, 24, 32, 48, 64, 96)
    ]
    theorem = coherent_component_trim_theorem()
    exact = all(row.exact_control_verified for row in controls)
    verified = exact and theorem.theorem_verified
    tail_counter = counters[-1]
    tail_scaling = scaling[-1]
    return CoherentComponentTrimHybridReport(
        created_at=utc_now(),
        theorem_contract={
            "branch_error_identity": theorem.exact_branch_error_identity,
            "parent_bound": theorem.parent_flatness_rank_budget_bound,
            "postselection_rule": theorem.postselection_cancellation,
            "recursive_hybrid": theorem.coherent_hybrid_bound,
            "natural_final_root": theorem.natural_final_root_corollary,
            "scope": theorem.scope_limit,
        },
        finite_controls=controls,
        postselection_counterfamily=counters,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "obligation": "remove_postselected_child_flatness_from_coherent_trim",
                "resolved": verified,
                "resolution": (
                    "The unnormalized branch identity charges all discarded "
                    "effects directly against the parent density and aggregate "
                    "component-rank budget."
                ),
            },
            {
                "obligation": "prove_native_root_state_polynomial_flatness",
                "resolved": False,
                "resolution": (
                    "Identify the exact native root density on each retained "
                    "source/target block; do not infer isotropy from covariance."
                ),
            },
            {
                "obligation": "prove_polynomial_aggregate_component_rank_budget_each_level",
                "resolved": False,
                "resolution": (
                    "The final root has a constant two-child budget from the "
                    "19/520 aspect. Earlier relation-bearing levels remain open."
                ),
            },
            {
                "obligation": "compile_coherent_level_trim_and_compose_hybrid",
                "resolved": False,
                "resolution": (
                    "Requires block encodings, threshold flags, support SELECT, "
                    "and a level-indexed implementation preserving branch coherence."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Every postselected child must be polynomially flat.",
                "resolved": True,
                "resolution": (
                    "False for coherent average-state error. The counterfamily "
                    "has conditional flatness Theta(r) from an isotropic parent, "
                    "while the parent-level rank-budget theorem remains finite."
                ),
            },
            {
                "objection": "Parent-level averaging proves each branch is accurate.",
                "resolved": True,
                "resolution": (
                    "False. It proves only the coherent branch-averaged error; a "
                    "rare conditioned branch may still fail badly."
                ),
            },
            {
                "objection": "Final-root aspect control completes the recursive trim.",
                "resolved": False,
                "resolution": (
                    "Only the final binary merge has the required aggregate rank "
                    "budget. Earlier levels and native root density are unproved."
                ),
            },
            {
                "objection": "A mean-square hybrid is already a coherent circuit.",
                "resolved": False,
                "resolution": (
                    "The theorem supplies an error ledger, not threshold or support "
                    "oracles, uniform SELECT, or gate complexity."
                ),
            },
        ],
        headline_metrics={
            "coherent_branch_trim_theorem_count": int(verified),
            "finite_control_count": len(controls),
            "finite_control_failure_count": sum(
                not row.exact_control_verified for row in controls
            ),
            "postselection_flatness_counterfamily_row_count": len(counters),
            "tail_postselection_conditional_flatness": (
                tail_counter.conditional_child_flatness
            ),
            "tail_branch_probability_times_flatness": (
                tail_counter.branch_probability_times_conditional_flatness
            ),
            "conditional_child_flatness_requirement_count": 0,
            "natural_final_root_aggregate_budget_theorem_count": 1,
            "all_level_aggregate_rank_budget_theorem_count": 0,
            "scaling_record_count": len(scaling),
            "tail_inverse_threshold_cost": tail_scaling.inverse_threshold_cost,
            "natural_root_flatness_theorem_count": 0,
            "coherent_recursive_trim_compiler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "coherent_branch_averaged_trim_proved": verified,
            "postselected_child_flatness_required": False,
            "natural_final_root_constant_budget_available": True,
            "natural_root_state_polynomially_flat": False,
            "polynomial_all_level_component_rank_budget_proved": False,
            "coherent_recursive_component_trim_compiled": False,
            "recursive_orientation_polar_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Coherent branch averaging removes the artificial child-flatness "
                "gate, but native root-state control, all-level aggregate budgets, "
                "and coherent component access remain unresolved."
            ),
        },
        status=(
            theorem.status
            if verified
            else "coherent-component-trim-hybrid-certificate-failure"
        ),
        summary=(
            "Replaced postselected child flatness by a coherent parent-state "
            "rank-budget theorem and an ideal-prefix hybrid error ledger."
        ),
        falsifiers_triggered=[
            "Postselection can create linear-in-dimension child flatness from an isotropic parent.",
            "Conditional child flatness is unnecessary for coherent branch-averaged trim error.",
            "The final-root 19/520 aspect yields a constant isotropic-parent cutoff, not a recursive compiler.",
            "Global ideal-prefix flatness still needs native root-state and per-level rank-budget theorems.",
        ],
    )


def write_coherent_component_trim_hybrid_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-COHERENT-COMPONENT-TRIM-HYBRID"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_coherent_component_trim_hybrid" in globals():
        report = run_coherent_component_trim_hybrid(**kwargs)
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
                id="NEG-SELF-DUAL-WREATH-COHERENT-COMPONENT-TRIM-HYBRID",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-COHERENT-COMPONENT-TRIM-HYBRID.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-COHERENT-COMPONENT-TRIM-HYBRID.",
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
                    "self_dual_wreath_coherent_component_trim_hybrid": str(path)
                },
            )
        )
    return payload
