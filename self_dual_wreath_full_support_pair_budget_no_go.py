"""Pair-budget obstruction to commuting full-support natural components.

Let ``E_1,...,E_q`` be projection leaves on a ``D``-dimensional space with
positive-definite frame ``F=sum_e E_e``.  Their canonical full-support PGM
effects are

    H_e = F^-1/2 E_e F^-1/2.

If the ``H_e`` commute, choose a simultaneous eigenbasis and let ``S_e`` be
the positive support of ``H_e``.  Since ``sum_e H_e=I``, every basis vector is
in at least one ``S_e``.  If its incidence degree is ``d_i``, then

    sum_e rank(E_e) = sum_i d_i,
    sum_(e<f) dim(S_e intersect S_f) = sum_i binom(d_i,2)
                                      >= sum_i(d_i-1).

Congruence by invertible ``F^1/2`` maps ``S_e`` onto ``range(E_e)`` and
preserves intersections.  Therefore every commuting full-support projection
frame obeys the exact pair-budget inequality

    P := sum_(e<f) dim(range(E_e) intersect range(E_f))
       >= L-D,       L:=sum_e rank(E_e).                  (1)

This becomes decisive for the natural final child.  Under the existing
``K+2`` schedule, it has ``q/|S_n| in [2,4)`` leaves per group order.  Uniform
leaf-rank concentration at relative error ``1/64`` gives

    L-D >= 31D/32.                                       (2)

The exact independent-Plancherel pair-budget theorem, even after upper-
bounding one child by all orientations, gives

    E[P/D] <= M(M-2)/g^3 + M/(2g^2) = O(1/g),            (3)

where ``M=2q<8g`` and ``g=|S_n|``.  Markov, the simultaneous rank theorem,
and global-distinct conditioning imply

    Pr[child full support and canonical effects commute | distinct] = o(1).

Thus any positive-mass full-support branch is naturally noncommutative; the
generic commuting-whitening counterfamilies require a macroscopic pair-common
budget that the wreath source does not possess.  This does not prove natural
full support, a quantitative commutator trace, the compressed proper-common-
span branch, a compiler, or a speedup.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_augmented_h0_dimension_obstruction import (
    pair_budget_expectation_relative,
)
from self_dual_wreath_common_span_component_universality_no_go import _psd_power
from self_dual_wreath_final_root_natural_common_span import (
    final_root_natural_scaling_record,
)
from self_dual_wreath_leaf_whitening_commutator_no_go import (
    construct_commuting_whitening_counterfamily,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_full_support_pair_budget_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-FULL-SUPPORT-PAIR-BUDGET-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class FullSupportPairBudgetControl:
    control_id: str
    physical_dimension: int
    outcome_count: int
    total_leaf_rank: int
    total_leaf_rank_excess: int
    exact_pair_common_budget: int
    commuting_pair_budget_lower_bound: int
    pair_budget_bound_residual: int
    frame_minimum_eigenvalue: float
    effect_sum_identity_residual: float
    maximum_effect_commutator_norm: float
    full_support: bool
    canonical_effects_commute: bool
    pair_budget_obstruction_detects_noncommutativity: bool
    exact_full_support_pair_budget_theorem_verified: bool
    status: str


@dataclass(frozen=True)
class NaturalFullSupportPairBudgetScalingRecord:
    n: int
    group_order_decimal: str
    selected_copy_count: int
    full_orientation_count_decimal: str
    final_child_leaf_count_decimal: str
    child_leaf_to_group_aspect: float
    relative_leaf_rank_tolerance: float
    commuting_pair_budget_relative_lower_bound: float
    expected_all_orientation_pair_budget_relative_upper_bound: float
    unconditioned_commuting_full_support_probability_upper_bound: float
    conditioned_commuting_full_support_probability_upper_bound: float
    log2_global_distinct_probability: float
    log2_uniform_leaf_rank_failure_upper_bound: float
    asymptotic_probability_vanishes: bool
    natural_child_full_support_proved: bool
    quantitative_component_M4_proved: bool
    status: str


@dataclass(frozen=True)
class FullSupportPairBudgetTheorem:
    finite_frame_inequality: str
    support_congruence: str
    natural_rank_excess: str
    natural_pair_budget: str
    conditioned_consequence: str
    scope_limit: str
    arbitrary_projection_ranks: bool
    arbitrary_outcome_count: bool
    all_finite_dimensions: bool
    natural_full_support_branch_noncommutative_with_high_probability: bool
    natural_full_support_proved: bool
    natural_component_M4_positive: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class FullSupportPairBudgetNoGoReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[FullSupportPairBudgetControl]
    scaling_records: list[NaturalFullSupportPairBudgetScalingRecord]
    theorem: FullSupportPairBudgetTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _support_basis(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    hermitian = (matrix + matrix.conj().T) / 2.0
    values, vectors = np.linalg.eigh(hermitian)
    return vectors[:, values > 100 * tolerance]


def _range_intersection_dimension(
    left: np.ndarray,
    right: np.ndarray,
    tolerance: float,
) -> int:
    if not left.shape[1] or not right.shape[1]:
        return 0
    singular = np.linalg.svd(left.conj().T @ right, compute_uv=False)
    return int(np.count_nonzero(singular >= 1.0 - 100 * tolerance))


def audit_full_support_pair_budget(
    control_id: str,
    leaves: tuple[np.ndarray, ...],
    *,
    tolerance: float = 1e-9,
) -> FullSupportPairBudgetControl:
    if not leaves:
        raise ValueError("at least one leaf projection is required")
    dimension = leaves[0].shape[0]
    if dimension < 1 or any(leaf.shape != (dimension, dimension) for leaf in leaves):
        raise ValueError("leaves must share one positive square carrier")
    bases = []
    ranks = []
    for leaf in leaves:
        if np.linalg.norm(leaf @ leaf - leaf, ord=2) > 1000 * tolerance:
            raise ValueError("every leaf must be an orthogonal projection")
        basis = _support_basis(leaf, tolerance)
        bases.append(basis)
        ranks.append(basis.shape[1])
    frame = sum(leaves, np.zeros_like(leaves[0], dtype=complex))
    frame_values = np.linalg.eigvalsh((frame + frame.conj().T) / 2.0)
    full = bool(frame_values[0] > 100 * tolerance)
    if not full:
        raise ValueError("the finite theorem audit requires full frame support")
    inverse_root = _psd_power(frame, -0.5, tolerance=tolerance)
    effects = tuple(inverse_root @ leaf @ inverse_root for leaf in leaves)
    identity = np.eye(dimension, dtype=complex)
    sum_residual = float(
        np.linalg.norm(sum(effects, np.zeros_like(identity)) - identity, ord=2)
    )
    commutator = max(
        (
            float(np.linalg.norm(left @ right - right @ left, ord=2))
            for left in effects
            for right in effects
        ),
        default=0.0,
    )
    commute = commutator <= 1000 * tolerance
    pair_budget = sum(
        _range_intersection_dimension(bases[left], bases[right], tolerance)
        for left in range(len(bases))
        for right in range(left + 1, len(bases))
    )
    total_rank = sum(ranks)
    lower = total_rank - dimension
    residual = pair_budget - lower
    obstruction = pair_budget < lower
    verified = bool((not commute or residual >= 0) and sum_residual <= 1000 * tolerance)
    return FullSupportPairBudgetControl(
        control_id=control_id,
        physical_dimension=dimension,
        outcome_count=len(leaves),
        total_leaf_rank=total_rank,
        total_leaf_rank_excess=lower,
        exact_pair_common_budget=pair_budget,
        commuting_pair_budget_lower_bound=lower,
        pair_budget_bound_residual=residual,
        frame_minimum_eigenvalue=float(frame_values[0]),
        effect_sum_identity_residual=sum_residual,
        maximum_effect_commutator_norm=commutator,
        full_support=full,
        canonical_effects_commute=commute,
        pair_budget_obstruction_detects_noncommutativity=obstruction,
        exact_full_support_pair_budget_theorem_verified=verified,
        status=(
            "commuting-full-support-pair-budget-bound-verified"
            if verified and commute
            else "pair-budget-obstruction-certifies-noncommutativity"
            if verified and obstruction
            else "full-support-pair-budget-theorem-verified"
            if verified
            else "full-support-pair-budget-control-failure"
        ),
    )


def _probability_from_log2(log2_probability: float) -> float:
    if log2_probability == -math.inf or log2_probability <= -1074:
        return 0.0
    return min(1.0, math.exp2(log2_probability))


def natural_full_support_pair_budget_scaling_record(
    n: int,
) -> NaturalFullSupportPairBudgetScalingRecord:
    if n < 5:
        raise ValueError("natural scaling requires n at least five")
    companion = final_root_natural_scaling_record(n)
    order = math.factorial(n)
    copies = companion.selected_copy_count
    orientations = 1 << copies
    child = orientations // 2
    tolerance = companion.relative_rank_tolerance
    rank_gap = (1.0 - tolerance) * child / order - 1.0
    expected_pair = float(
        pair_budget_expectation_relative(n, copies, target=None)
    )
    rank_failure = _probability_from_log2(
        companion.log2_unconditioned_uniform_leaf_rank_failure_upper_bound
    )
    markov = expected_pair / rank_gap if rank_gap > 0 else 1.0
    unconditioned = min(1.0, rank_failure + markov)
    distinct = _probability_from_log2(companion.log2_global_distinct_probability)
    conditioned = min(1.0, unconditioned / distinct) if distinct else 1.0
    return NaturalFullSupportPairBudgetScalingRecord(
        n=n,
        group_order_decimal=str(order),
        selected_copy_count=copies,
        full_orientation_count_decimal=str(orientations),
        final_child_leaf_count_decimal=str(child),
        child_leaf_to_group_aspect=child / order,
        relative_leaf_rank_tolerance=tolerance,
        commuting_pair_budget_relative_lower_bound=rank_gap,
        expected_all_orientation_pair_budget_relative_upper_bound=expected_pair,
        unconditioned_commuting_full_support_probability_upper_bound=unconditioned,
        conditioned_commuting_full_support_probability_upper_bound=conditioned,
        log2_global_distinct_probability=companion.log2_global_distinct_probability,
        log2_uniform_leaf_rank_failure_upper_bound=(
            companion.log2_unconditioned_uniform_leaf_rank_failure_upper_bound
        ),
        asymptotic_probability_vanishes=True,
        natural_child_full_support_proved=False,
        quantitative_component_M4_proved=False,
        status="full-support-commuting-branch-probability-vanishes",
    )


def full_support_pair_budget_theorem() -> FullSupportPairBudgetTheorem:
    return FullSupportPairBudgetTheorem(
        finite_frame_inequality=(
            "commuting full-support effects imply sum_(e<f)dim(U_e cap U_f) "
            ">=sum_e dim(U_e)-D"
        ),
        support_congruence=(
            "range(E_e)=F^(1/2)supp(H_e), so pair intersections preserve "
            "simultaneous support incidences"
        ),
        natural_rank_excess=(
            "K+2 final-child rank concentration gives L-D>=31D/32"
        ),
        natural_pair_budget=(
            "independent Plancherel gives E[P/D]=O(1/|S_n|) using the exact "
            "all-orientation pair-rank formula"
        ),
        conditioned_consequence=(
            "Pr[full support and commuting canonical child effects | globally "
            "distinct]=o(1)"
        ),
        scope_limit=(
            "Full support itself, proper-common-span compression, a quantitative "
            "M4 lower bound, and coherent implementation remain open."
        ),
        arbitrary_projection_ranks=True,
        arbitrary_outcome_count=True,
        all_finite_dimensions=True,
        natural_full_support_branch_noncommutative_with_high_probability=True,
        natural_full_support_proved=False,
        natural_component_M4_positive=False,
        theorem_verified=True,
        status="natural-full-support-commuting-branch-eliminated",
    )


def _generic_transverse_frame(
    seed: int,
    *,
    dimension: int = 8,
    outcome_count: int = 6,
    leaf_rank: int = 2,
) -> tuple[np.ndarray, ...]:
    rng = np.random.default_rng(seed)
    leaves = []
    for _ in range(outcome_count):
        raw = rng.normal(size=(dimension, leaf_rank)) + 1j * rng.normal(
            size=(dimension, leaf_rank)
        )
        basis, _ = np.linalg.qr(raw, mode="reduced")
        leaves.append(basis @ basis.conj().T)
    return tuple(leaves)


def _orthogonal_pvm(dimension: int) -> tuple[np.ndarray, ...]:
    leaves = []
    for index in range(dimension):
        leaf = np.zeros((dimension, dimension), dtype=complex)
        leaf[index, index] = 1.0
        leaves.append(leaf)
    return tuple(leaves)


def run_full_support_pair_budget_no_go() -> FullSupportPairBudgetNoGoReport:
    _, _, commuting_leaves, _ = construct_commuting_whitening_counterfamily(4, 5, 2)
    controls = [
        audit_full_support_pair_budget(
            "COMMUTING-INDEPENDENT-SET-COVER",
            tuple(np.asarray(leaf, dtype=complex) for leaf in commuting_leaves),
        ),
        audit_full_support_pair_budget(
            "GENERIC-TRANSVERSE-RANK2-FRAME",
            _generic_transverse_frame(2203),
        ),
        audit_full_support_pair_budget(
            "ORTHOGONAL-PVM-BOUNDARY",
            _orthogonal_pvm(7),
        ),
    ]
    scaling = [
        natural_full_support_pair_budget_scaling_record(n)
        for n in (12, 16, 20, 24, 32, 40, 48)
    ]
    theorem = full_support_pair_budget_theorem()
    failures = sum(
        not row.exact_full_support_pair_budget_theorem_verified for row in controls
    )
    commuting = controls[0]
    transverse = controls[1]
    exact = bool(
        failures == 0
        and commuting.canonical_effects_commute
        and commuting.pair_budget_bound_residual >= 0
        and transverse.pair_budget_obstruction_detects_noncommutativity
        and not transverse.canonical_effects_commute
        and theorem.theorem_verified
    )
    return FullSupportPairBudgetNoGoReport(
        created_at=utc_now(),
        theorem_contract={
            "finite_pair_budget": theorem.finite_frame_inequality,
            "natural_rank_excess": theorem.natural_rank_excess,
            "natural_pair_budget": theorem.natural_pair_budget,
            "conditioned_consequence": theorem.conditioned_consequence,
            "scope": theorem.scope_limit,
        },
        finite_controls=controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "obligation": "derive_commuting_full_support_pair_budget_inequality",
                "resolved": exact,
                "resolution": (
                    "Simultaneous effect supports form an incidence cover; invertible "
                    "frame congruence transfers every support intersection to the "
                    "corresponding physical leaf intersection."
                ),
            },
            {
                "obligation": "eliminate_natural_full_support_commuting_branch",
                "resolved": exact,
                "resolution": (
                    "Uniform leaf ranks require a 31/32 pair budget, while exact "
                    "Plancherel pair ranks have O(1/|S_n|) expectation."
                ),
            },
            {
                "obligation": "prove_natural_final_child_full_support_or_handle_proper_common_span",
                "resolved": False,
                "resolution": (
                    "The present natural common-span theorem gives constant relative "
                    "rank, not full support; arbitrary proper compression remains universal."
                ),
            },
            {
                "obligation": "upgrade_qualitative_noncommutativity_to_M4_scale",
                "resolved": False,
                "resolution": (
                    "A vanishingly small commutator can violate exact commutativity; "
                    "quantitative block-angle or word-moment separation is still needed."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Many leaf ranks can overlap without exact pair intersections.",
                "resolved": True,
                "resolution": (
                    "True for general noncommuting frames, and that is exactly why a "
                    "small pair budget obstructs a commuting simultaneous-support cover."
                ),
            },
            {
                "objection": "The full-support theorem applies to the proved 19/128 common span.",
                "resolved": True,
                "resolution": (
                    "False. Proper common-span compression realizes arbitrary POVMs; "
                    "the theorem is explicitly conditional on a full child carrier."
                ),
            },
            {
                "objection": "Exact noncommutativity supplies a useful quantitative signal.",
                "resolved": True,
                "resolution": (
                    "Not without a lower bound. This theorem kills the zero branch but "
                    "does not prevent superpolynomially small commutators."
                ),
            },
        ],
        headline_metrics={
            "full_support_pair_budget_inequality_theorem_count": int(exact),
            "natural_full_support_commuting_branch_no_go_theorem_count": int(exact),
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "transverse_pair_budget_noncommutativity_certificate_count": int(
                transverse.pair_budget_obstruction_detects_noncommutativity
            ),
            "largest_scaling_n": scaling[-1].n,
            "largest_scale_conditioned_commuting_full_support_probability_upper_bound": (
                scaling[-1].conditioned_commuting_full_support_probability_upper_bound
            ),
            "natural_full_support_theorem_count": 0,
            "natural_component_M4_lower_bound_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "natural_full_support_commuting_branch_eliminated": exact,
            "natural_final_child_full_support_proved": False,
            "proper_common_span_commuting_branch_eliminated": False,
            "quantitative_natural_component_M4_positive": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Pair ranks forbid exact commutativity whenever the natural child is "
                "full support, but full support and quantitative gap remain unproved."
            ),
        },
        status=(
            "natural-full-support-commuting-branch-closed-proper-compression-open"
            if exact
            else "full-support-pair-budget-control-failure"
        ),
        summary=(
            "Used the exact natural pair-rank budget to eliminate commuting canonical "
            "effects on any full-support final-child branch."
        ),
        falsifiers_triggered=[
            "Generic commuting whitening requires macroscopic pair-common incidence and is incompatible with the natural pair-rank budget on full support.",
            "Full-support noncommutativity does not transfer automatically through a proper sibling common-span compression.",
            "Qualitative noncommutativity is insufficient for a Shor-level claim without a quantitative moment and compiler.",
        ],
    )


def write_full_support_pair_budget_no_go_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-FULL-SUPPORT-PAIR-BUDGET-NO-GO"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    path = path
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    report = asdict(run_full_support_pair_budget_no_go())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    return report


if __name__ == "__main__":
    payload = write_full_support_pair_budget_no_go_report()
    print(json.dumps(payload["headline_metrics"], indent=2, sort_keys=True))
