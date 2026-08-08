"""Final-root Haar leverage edge under the K+2 mixed-arity schedule.

The mixed-arity polar schedule already chooses ``K+2`` copies, where
``K=ceil(log2 |G|)``.  At its final binary root, one child has coefficient
width

    N = 2^(K+1),

while the Gaussian-surrogate physical/common dimension is ``r=|G|``.  If
``c=2^K/|G| in [1,2)``, then

    N/r = 2c in [2,4),          alpha=r/N in (1/4,1/2].   (1)

Thus the common-fiber aspect needed by the sparse-support component theorem is
uniformly bounded away from zero without adding copies beyond the existing
schedule.

For a Haar isometry ``W:C^r -> C^N`` and rank-one coordinate blocks, the
component effects are

    H_i = w_i^* w_i,

with one positive eigenvalue ``L_i=||w_i||^2``.  Every marginal leverage score
has the complex-Haar law

    L_i ~ Beta(r,N-r),              E L_i=alpha.           (2)

The beta/binomial identity and a Chernoff bound give, for ``x<r/(N-1)``,

    Pr[L_i <= x]
      = Pr[Bin(N-1,x) >= r]
      <= exp(-(N-1) KL(r/(N-1) || x)).                    (3)

Taking ``x=alpha/2`` and unioning over all ``N`` coordinates proves a uniform
positive component edge with failure ``exp(-Omega(N))`` throughout (1).  On
that event, the coordinate-rank defect bridge gives

    D >= (alpha/2 - 2/r + 1/N) I,                         (4)

which approaches at least ``1/8``.

This is a rigorous Haar/Gaussian-surrogate theorem, not a natural wreath-frame
result.  Natural orientation leaves have representation-dependent block ranks
and arithmetic correlations.  The required transfer is a leverage-score or
component-edge concentration theorem for the regular-master Plancherel/Racah
embedding on positive accepted mass.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_component_defect_gap_bridge import (
    audit_component_defect_gap,
)


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_final_root_leverage_edge.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-FINAL-ROOT-LEVERAGE-EDGE"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class HaarLeverageControl:
    control_id: str
    coefficient_dimension: int
    common_fiber_dimension: int
    common_fiber_aspect: float
    random_seed: int
    minimum_row_leverage: float
    maximum_row_leverage: float
    half_mean_edge_threshold: float
    every_component_above_half_mean: bool
    component_effect_sum_identity_residual: float
    aggregate_defect_minimum_eigenvalue: float
    aggregate_defect_theorem_lower_bound: float
    exact_component_povm_verified: bool
    status: str


@dataclass(frozen=True)
class FinalRootLeverageScalingRecord:
    n: int
    group_order_decimal: str
    information_threshold_copy_count: int
    selected_copy_count: int
    final_child_coefficient_dimension_decimal: str
    final_child_coefficient_to_physical_aspect: float
    common_fiber_aspect: float
    half_mean_edge_threshold: float
    log2_union_lower_edge_failure_upper_bound: float
    coordinate_defect_gap_lower_bound_on_edge_event: float
    positive_defect_gap_on_edge_event: bool
    natural_leverage_edge_transfer_proved: bool
    status: str


@dataclass(frozen=True)
class FinalRootLeverageEdgeReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[HaarLeverageControl]
    scaling_records: list[FinalRootLeverageScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def binary_relative_entropy(left: float, right: float) -> float:
    if not 0 < left < 1 or not 0 < right < 1:
        raise ValueError("binary relative entropy arguments must lie in (0,1)")
    return (
        left * math.log(left / right)
        + (1.0 - left) * math.log((1.0 - left) / (1.0 - right))
    )


def beta_lower_tail_union_log2_bound(
    coefficient_dimension: int,
    fiber_dimension: int,
    threshold: float,
) -> float:
    """Union bound from the exact beta/binomial identity and Chernoff."""

    total = coefficient_dimension
    rank = fiber_dimension
    if not 1 <= rank < total:
        raise ValueError("fiber rank must lie between zero and coefficient dimension")
    binomial_rate = rank / (total - 1)
    if not 0 < threshold < binomial_rate:
        raise ValueError("threshold must lie below the beta/binomial rate")
    exponent = (total - 1) * binary_relative_entropy(
        binomial_rate,
        threshold,
    )
    return min(0.0, math.log2(total) - exponent / math.log(2.0))


def _haar_isometry(
    coefficient_dimension: int,
    fiber_dimension: int,
    seed: int,
) -> np.ndarray:
    rng = np.random.default_rng(seed)
    gaussian = (
        rng.normal(size=(coefficient_dimension, fiber_dimension))
        + 1j * rng.normal(size=(coefficient_dimension, fiber_dimension))
    ) / math.sqrt(2.0)
    isometry, _ = np.linalg.qr(gaussian, mode="reduced")
    return isometry


def audit_haar_leverage_control(
    control_id: str,
    coefficient_dimension: int,
    fiber_dimension: int,
    *,
    seed: int,
    tolerance: float = 1e-9,
) -> HaarLeverageControl:
    isometry = _haar_isometry(coefficient_dimension, fiber_dimension, seed)
    effects = tuple(
        np.outer(row.conj(), row)
        for row in isometry
    )
    leverages = np.asarray(
        [float(np.vdot(row, row).real) for row in isometry]
    )
    aspect = fiber_dimension / coefficient_dimension
    threshold = aspect / 2.0
    defect = audit_component_defect_gap(
        f"{control_id}-DEFECT",
        effects,
        tolerance=tolerance,
    )
    verified = bool(
        defect.exact_defect_gap_bound_verified
        and defect.effect_sum_identity_residual <= 1000 * tolerance
    )
    return HaarLeverageControl(
        control_id=control_id,
        coefficient_dimension=coefficient_dimension,
        common_fiber_dimension=fiber_dimension,
        common_fiber_aspect=aspect,
        random_seed=seed,
        minimum_row_leverage=float(leverages.min()),
        maximum_row_leverage=float(leverages.max()),
        half_mean_edge_threshold=threshold,
        every_component_above_half_mean=bool(leverages.min() >= threshold),
        component_effect_sum_identity_residual=defect.effect_sum_identity_residual,
        aggregate_defect_minimum_eigenvalue=defect.observed_defect_minimum_eigenvalue,
        aggregate_defect_theorem_lower_bound=defect.theorem_defect_gap_lower_bound,
        exact_component_povm_verified=verified,
        status=(
            "finite-haar-leverage-edge-and-defect-control-passed"
            if verified and leverages.min() >= threshold
            else "finite-haar-component-povm-verified-edge-event-missed"
            if verified
            else "haar-leverage-control-failure"
        ),
    )


def final_root_leverage_scaling_record(n: int) -> FinalRootLeverageScalingRecord:
    if n < 3:
        raise ValueError("n must be at least three")
    order = math.factorial(n)
    threshold_copies = (order - 1).bit_length()
    selected_copies = threshold_copies + 2
    coefficient_dimension = 1 << (threshold_copies + 1)
    aspect = coefficient_dimension / order
    alpha = order / coefficient_dimension
    edge = alpha / 2.0
    failure_log2 = beta_lower_tail_union_log2_bound(
        coefficient_dimension,
        order,
        edge,
    )
    defect_gap = edge - 2.0 / order + 1.0 / coefficient_dimension
    positive = defect_gap > 0
    return FinalRootLeverageScalingRecord(
        n=n,
        group_order_decimal=str(order),
        information_threshold_copy_count=threshold_copies,
        selected_copy_count=selected_copies,
        final_child_coefficient_dimension_decimal=str(coefficient_dimension),
        final_child_coefficient_to_physical_aspect=aspect,
        common_fiber_aspect=alpha,
        half_mean_edge_threshold=edge,
        log2_union_lower_edge_failure_upper_bound=failure_log2,
        coordinate_defect_gap_lower_bound_on_edge_event=defect_gap,
        positive_defect_gap_on_edge_event=positive,
        natural_leverage_edge_transfer_proved=False,
        status=(
            "final-root-haar-uniform-leverage-and-defect-gap-certified"
            if positive
            else "small-finite-final-root-defect-bound-not-positive"
        ),
    )


def run_final_root_leverage_edge() -> FinalRootLeverageEdgeReport:
    controls = [
        audit_haar_leverage_control(
            "HAAR-RANK24-IN-64-COORDINATES",
            64,
            24,
            seed=301,
        ),
        audit_haar_leverage_control(
            "HAAR-RANK32-IN-96-COORDINATES",
            96,
            32,
            seed=302,
        ),
        audit_haar_leverage_control(
            "HAAR-RANK48-IN-128-COORDINATES",
            128,
            48,
            seed=303,
        ),
    ]
    scaling = [
        final_root_leverage_scaling_record(n)
        for n in (3, 4, 6, 8, 10, 12, 16, 20, 24, 32, 40, 48)
    ]
    failures = sum(not row.exact_component_povm_verified for row in controls)
    edge_misses = sum(not row.every_component_above_half_mean for row in controls)
    positive_rows = sum(row.positive_defect_gap_on_edge_event for row in scaling)
    tail = scaling[-1]
    exact = failures == 0
    schedule = all(
        2.0 <= row.final_child_coefficient_to_physical_aspect < 4.0
        and 0.25 < row.common_fiber_aspect <= 0.5
        for row in scaling
    )
    return FinalRootLeverageEdgeReport(
        created_at=utc_now(),
        theorem_contract={
            "k_plus_two_final_root_aspect": (
                "With K=ceil(log2|G|), one final-root child has N=2^(K+1) "
                "coefficients and r=|G|, so N/r is in [2,4) and alpha=r/N "
                "is in (1/4,1/2]."
            ),
            "haar_coordinate_effect": (
                "A rank-one coordinate component of a Haar isometry has one "
                "positive eigenvalue L_i distributed as Beta(r,N-r)."
            ),
            "uniform_edge_tail": (
                "The beta/binomial identity, Chernoff, and a union over all N "
                "coordinates bound Pr[min_i L_i<=alpha/2] by "
                "N exp(-(N-1)KL(r/(N-1)||alpha/2))."
            ),
            "defect_bridge": (
                "On the uniform edge event, coordinate rank accounting gives "
                "D>=(alpha/2-2/r+1/N)I, asymptotically at least 1/8."
            ),
            "scope": (
                "This is exact for the Haar/Gaussian final-root surrogate. "
                "Natural representation-valued block ranks, leverage tails, "
                "central-support mass, and coherent SELECT are unproved."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "show_existing_k_plus_two_schedule_bounds_final_root_component_aspect",
                "resolved": schedule,
                "resolution": "The exact dyadic ratio puts every recorded final-root child aspect in [2,4) and common-fiber aspect in (1/4,1/2]."
            },
            {
                "obligation": "prove_uniform_haar_rank_one_component_edge",
                "resolved": True,
                "resolution": "Each leverage is Beta(r,N-r); the exact beta/binomial identity plus Chernoff and a coordinate union gives exp(-Omega(N)) failure at threshold alpha/2."
            },
            {
                "obligation": "transfer_final_root_leverage_edge_to_natural_plancherel_racah_blocks",
                "resolved": False,
                "resolution": "Need a regular-master row/block leverage concentration theorem, including nonuniform leaf ranks and collision-free conditioning, on physical accepted mass."
            },
            {
                "obligation": "extend_component_edge_control_to_every_relation_bearing_multiscale_node",
                "resolved": False,
                "resolution": "The final root is solved only in the surrogate. Classify which earlier binary/eight-way nodes carry nonzero dependency fibers and prove corresponding block/fiber aspect bounds."
            },
        ],
        adversarial_audit=[
            {
                "objection": "The information-threshold copy count can make the component common-fiber aspect arbitrarily small.",
                "resolved": True,
                "resolution": "True for a poorly selected threshold binary node, but false at the existing K+2 final root: alpha is always in (1/4,1/2]."
            },
            {
                "objection": "A marginal constant mean leverage controls the minimum over exponentially many outcomes.",
                "resolved": True,
                "resolution": "Mean alone does not. The beta Chernoff exponent is Omega(N), strong enough to survive the union over N outcomes in the Haar model."
            },
            {
                "objection": "The Haar leverage theorem proves the natural orientation components have a positive edge.",
                "resolved": False,
                "resolution": "No. Natural blocks are structured invariant ranges, not independent Haar rows; representation arithmetic may create tiny-edge central sectors."
            },
            {
                "objection": "A final-root edge theorem resolves all recursive component POVMs.",
                "resolved": False,
                "resolution": "Earlier relation-bearing nodes, multiway component geometry, center-valued mass, support SELECT, transport, and holonomy remain."
            },
        ],
        headline_metrics={
            "k_plus_two_final_root_component_aspect_theorem_count": int(schedule),
            "haar_uniform_rank_one_leverage_edge_theorem_count": 1,
            "haar_edge_to_defect_gap_bridge_count": 1,
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "finite_half_mean_edge_miss_count": edge_misses,
            "scaling_record_count": len(scaling),
            "positive_finite_scaling_defect_gap_row_count": positive_rows,
            "tail_n": tail.n,
            "tail_common_fiber_aspect": tail.common_fiber_aspect,
            "tail_log2_union_edge_failure_upper_bound": tail.log2_union_lower_edge_failure_upper_bound,
            "tail_coordinate_defect_gap_lower_bound": tail.coordinate_defect_gap_lower_bound_on_edge_event,
            "natural_final_root_leverage_edge_theorem_count": 0,
            "all_relation_node_component_edge_theorem_count": 0,
            "natural_component_support_select_circuit_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "existing_k_plus_two_schedule_bounds_final_root_component_aspect": schedule,
            "haar_final_root_minimum_component_edge_is_constant_with_high_probability": True,
            "haar_final_root_aggregate_defect_has_constant_gap": tail.positive_defect_gap_on_edge_event,
            "natural_final_root_component_edge_proved": False,
            "natural_all_relation_node_component_edges_proved": False,
            "regular_master_central_support_controlled": False,
            "natural_component_support_select_compiled": False,
            "recursive_orientation_polar_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The existing copy schedule supplies the right final-root "
                "aspect and the Haar model has overwhelming leverage/defect "
                "gaps, but no natural representation-theoretic transfer exists."
            ),
        },
        status=(
            "final-root-haar-leverage-and-defect-gap-proved-natural-transfer-open"
            if exact and schedule and edge_misses == 0
            else "final-root-leverage-edge-control-failure"
        ),
        summary=(
            "Showed that the existing K+2 schedule already prevents a vanishing "
            "final-root component aspect and proved an all-coordinate constant "
            "edge plus aggregate defect gap in the Haar surrogate."
        ),
        falsifiers_triggered=[
            "The existing K+2 final root does not suffer a vanishing common-fiber aspect in the surrogate.",
            "Marginal mean leverage alone is insufficient; the uniform result needs the beta large-deviation exponent.",
            "Haar rank-one leverage concentration is not a natural wreath-frame theorem.",
            "A final-root surrogate edge does not resolve earlier relation nodes or compile the PGM.",
        ],
    )


def write_final_root_leverage_edge_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_final_root_leverage_edge())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    report = write_final_root_leverage_edge_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
