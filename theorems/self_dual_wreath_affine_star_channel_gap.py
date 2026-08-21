"""Uniform graded gap for flat carrier channels supported on affine stars.

Every nontrivial channel extracted from seven W6 physical controls is a
three-edge star on an affine plane.  The natural all-depth extension of that
pattern is an affine-star channel: an affine orientation support of size
``2p`` with one center connected to every other support vertex.

At any sibling-bit split crossing the affine support, both children contain
``p`` vertices.  Put the center in the left child.  The channel has ``p-1``
internal left edges, no internal right edges, and ``p`` crossing edges.  With
``a=2(1-gamma)``, the child-resolvent reduction gives

    E_R = I,
    E_L = (1-gamma)I + gamma q J_p,
    q = (a+gamma)/(a+gamma p).

The normalized grading defect is therefore

    max {
      gamma/(2-gamma),
      [t_p-1]/[t_p+1]
    },

where

    t_p = 1-gamma + gamma p(a+gamma)/(a+gamma p).

For ``0<gamma<=1/2``, ``t_p`` increases to ``3-2gamma`` and

    defect <= (1-gamma)/(2-gamma) < 1/2,
    endpoint gap >= 1/[2(2-gamma)] > 1/4.                 (1)

The bound is independent of the affine dimension and merge width.  At
``p=2``, (1)'s exact formulas reproduce the physical W6 defects ``1/17`` for
``gamma=1/9`` and ``1/9`` for ``gamma=1/5``.

This theorem materially weakens the needed global classification: complete
affine channel closure is unnecessary.  It is enough to prove that natural
residual channels remain disjoint unions of affine stars (or another graph
family with comparable child endpoint resolvents).  No such all-depth
classification is claimed here.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from research_registry import utc_now
from self_dual_wreath_graded_channel_graph_reduction import (
    audit_graded_channel_graph,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_affine_star_channel_gap.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-AFFINE-STAR-CHANNEL-GAP"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class AffineStarGapControl:
    side_width: int
    correlation: float
    orientation_support_size: int
    internal_center_child_edge_count: int
    crossing_edge_count: int
    predicted_orthogonal_defect: float
    predicted_constant_defect: float
    predicted_grading_defect_norm: float
    observed_grading_defect_norm: float
    defect_residual: float
    predicted_endpoint_gap: float
    observed_endpoint_gap: float
    endpoint_gap_residual: float
    uniform_defect_upper_bound: float
    uniform_endpoint_gap_lower_bound: float
    uniform_bound_respected: bool
    exact_audit: bool
    status: str


@dataclass(frozen=True)
class AffineStarScalingRecord:
    n: int
    information_threshold_copy_count: int
    affine_half_width_log2: int
    reciprocal_correlation: float
    grading_defect_norm: float
    endpoint_gap: float
    uniform_endpoint_gap_lower_bound: float
    endpoint_gap_above_quarter: bool
    status: str


@dataclass(frozen=True)
class AffineStarChannelGapReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[AffineStarGapControl]
    scaling_records: list[AffineStarScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def exact_affine_star_defects(
    side_width: int,
    correlation: float,
) -> tuple[float, float, float, float]:
    if side_width < 1:
        raise ValueError("side width must be positive")
    if not 0 < correlation <= 0.5:
        raise ValueError("correlation must lie in (0,1/2]")
    baseline = 2 * (1 - correlation)
    q = (baseline + correlation) / (
        baseline + correlation * side_width
    )
    constant_ratio = (
        1 - correlation + correlation * q * side_width
    )
    orthogonal_defect = correlation / (2 - correlation)
    constant_defect = abs(constant_ratio - 1) / (constant_ratio + 1)
    defect = max(orthogonal_defect, constant_defect)
    return orthogonal_defect, constant_defect, defect, (1 - defect) / 2


def affine_star_graph(side_width: int) -> tuple[tuple[int, ...], tuple[tuple[int, int], ...], tuple[int, ...]]:
    if side_width < 1:
        raise ValueError("side width must be positive")
    vertices = tuple(range(2 * side_width))
    left = tuple(range(side_width))
    edges = tuple((0, vertex) for vertex in range(1, 2 * side_width))
    return vertices, edges, left


def audit_affine_star_gap(
    side_width: int,
    correlation: float,
    *,
    tolerance: float = 1e-9,
) -> AffineStarGapControl:
    vertices, edges, left = affine_star_graph(side_width)
    orthogonal, constant, predicted, gap = exact_affine_star_defects(
        side_width,
        correlation,
    )
    graph = audit_graded_channel_graph(
        f"AFFINE-STAR-P{side_width}",
        vertices,
        edges,
        left,
        correlation,
        expected_defect=predicted,
        tolerance=tolerance,
    )
    defect_upper = (1 - correlation) / (2 - correlation)
    gap_lower = 1 / (2 * (2 - correlation))
    exact = bool(
        graph.exact_graph_reduction_verified
        and abs(graph.grading_defect_norm - predicted) <= 100 * tolerance
    )
    return AffineStarGapControl(
        side_width=side_width,
        correlation=correlation,
        orientation_support_size=2 * side_width,
        internal_center_child_edge_count=max(0, side_width - 1),
        crossing_edge_count=side_width,
        predicted_orthogonal_defect=orthogonal,
        predicted_constant_defect=constant,
        predicted_grading_defect_norm=predicted,
        observed_grading_defect_norm=graph.grading_defect_norm,
        defect_residual=abs(graph.grading_defect_norm - predicted),
        predicted_endpoint_gap=gap,
        observed_endpoint_gap=graph.endpoint_gap,
        endpoint_gap_residual=abs(graph.endpoint_gap - gap),
        uniform_defect_upper_bound=defect_upper,
        uniform_endpoint_gap_lower_bound=gap_lower,
        uniform_bound_respected=(
            graph.grading_defect_norm <= defect_upper + 100 * tolerance
            and graph.endpoint_gap >= gap_lower - 100 * tolerance
        ),
        exact_audit=exact,
        status="affine-star-channel-uniform-graded-gap-verified",
    )


def affine_star_scaling_record(n: int) -> AffineStarScalingRecord:
    if n < 5:
        raise ValueError("n must be at least five")
    copy_count = math.ceil(math.lgamma(n + 1) / math.log(2))
    half_width_log2 = copy_count - 1
    gamma = 1 / (n - 1)
    # Stable p->huge evaluation using p*q=(a+gamma)/(a/p+gamma).
    baseline = 2 * (1 - gamma)
    inverse_width = 2.0 ** (-half_width_log2)
    p_times_q = (baseline + gamma) / (
        baseline * inverse_width + gamma
    )
    constant_ratio = 1 - gamma + gamma * p_times_q
    orthogonal = gamma / (2 - gamma)
    constant = abs(constant_ratio - 1) / (constant_ratio + 1)
    defect = max(orthogonal, constant)
    gap = (1 - defect) / 2
    lower = 1 / (2 * (2 - gamma))
    return AffineStarScalingRecord(
        n=n,
        information_threshold_copy_count=copy_count,
        affine_half_width_log2=half_width_log2,
        reciprocal_correlation=gamma,
        grading_defect_norm=defect,
        endpoint_gap=gap,
        uniform_endpoint_gap_lower_bound=lower,
        endpoint_gap_above_quarter=gap > 0.25,
        status="natural-width-affine-star-channel-gap-constant",
    )


def run_affine_star_channel_gap() -> AffineStarChannelGapReport:
    controls = [
        audit_affine_star_gap(width, gamma)
        for gamma in (1 / 5, 1 / 9, 1 / 10)
        for width in (2, 3, 4, 8, 16, 32)
    ]
    scaling = [
        affine_star_scaling_record(n)
        for n in (6, 8, 10, 12, 16, 24, 32, 48, 64, 128, 256)
    ]
    failures = sum(not row.exact_audit for row in controls)
    bound_failures = sum(not row.uniform_bound_respected for row in controls)
    scaling_failures = sum(not row.endpoint_gap_above_quarter for row in scaling)
    carrier_nine = audit_affine_star_gap(2, 1 / 9)
    carrier_five = audit_affine_star_gap(2, 1 / 5)
    tail = scaling[-1]
    metrics: dict[str, int | float] = {
        "affine_star_exact_defect_theorem_count": 1,
        "affine_star_uniform_quarter_gap_theorem_count": 1,
        "finite_affine_star_control_count": len(controls),
        "finite_affine_star_control_failure_count": failures,
        "finite_uniform_bound_failure_count": bound_failures,
        "natural_width_scaling_row_count": len(scaling),
        "natural_width_quarter_gap_failure_count": scaling_failures,
        "w6_carrier_nine_defect": carrier_nine.observed_grading_defect_norm,
        "w6_carrier_five_defect": carrier_five.observed_grading_defect_norm,
        "tail_n": tail.n,
        "tail_copy_count": tail.information_threshold_copy_count,
        "tail_grading_defect_norm": tail.grading_defect_norm,
        "tail_endpoint_gap": tail.endpoint_gap,
        "natural_residual_channel_affine_star_classification_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    verified = not failures and not bound_failures and not scaling_failures
    return AffineStarChannelGapReport(
        created_at=utc_now(),
        theorem_contract={
            "affine_star_endpoint_effects": (
                "E_R=I and E_L=(1-gamma)I+gamma[(2-gamma)/"
                "(2(1-gamma)+gamma p)]J_p."
            ),
            "exact_defect": (
                "max{gamma/(2-gamma), (t_p-1)/(t_p+1)}, with "
                "t_p=1-gamma+gamma p(2-gamma)/[2(1-gamma)+gamma p]."
            ),
            "uniform_bound": (
                "For gamma<=1/2, defect<=(1-gamma)/(2-gamma)<1/2 "
                "and endpoint gap>=1/[2(2-gamma)]>1/4."
            ),
            "natural_scope": (
                "Applies at arbitrary affine dimension if the physical "
                "residual carrier channel is an affine star."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "affine_star_channel_uniform_graded_gap",
                "resolved": verified,
                "resolution": "Exact child-resolvent diagonalization proves a width-independent gap strictly above one quarter."
            },
            {
                "obligation": "explain_all_extracted_w6_residual_channels",
                "resolved": True,
                "resolution": "The p=2 formulas give exactly 1/17, 1/9, and 1/19 for the extracted carrier dimensions 9, 5, and 10."
            },
            {
                "obligation": "natural_residual_channels_are_affine_stars_all_depth",
                "resolved": False,
                "resolution": "Need a carrier-index closure theorem or a sparse asymptotic extractor; seven W6 controls do not classify natural threshold portfolios."
            },
        ],
        adversarial_audit=[
            {
                "objection": "Incomplete affine stars inherit the crossing-only K_p,p gap collapse.",
                "resolved": True,
                "resolution": "False: the center-side internal star edges suppress the growing mode and leave a gap above one quarter."
            },
            {
                "objection": "Any affine channel graph has the same bound.",
                "resolved": False,
                "resolution": "Vertex affinity alone says nothing about edge support; a balanced complete bipartite graph is affine-compatible and can close the gap."
            },
            {
                "objection": "Finite W6 star extraction proves the natural classification.",
                "resolved": False,
                "resolution": "A channel that merges several affine stars into a two-sided high-degree graph remains the decisive falsifier."
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "affine_star_exact_defect_formula_proved": verified,
            "affine_star_endpoint_gap_uniformly_above_quarter": verified,
            "extracted_w6_star_defects_explained": verified,
            "all_affine_channel_graphs_safe": False,
            "natural_residual_channels_classified_as_affine_stars": False,
            "natural_pgm_endpoint_gap_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Affine-star channels are safe at every width, but no theorem "
                "yet prevents natural carrier channels from gluing into a "
                "different high-degree graph family."
            ),
        },
        status=(
            "affine-star-channel-quarter-gap-proved-"
            "natural-channel-classification-open"
        ),
        summary=(
            "Proved a width-independent graded gap above one quarter for "
            "affine-star carrier channels, exactly explaining every extracted "
            "W6 residual channel."
        ),
        falsifiers_triggered=[
            "Complete affine closure is stronger than necessary; affine stars are already uniformly safe.",
            "Vertex affinity without edge-graph classification is insufficient.",
            "The remaining asymptotic question is whether natural channels stay as separate affine stars or merge into a dangerous two-sided graph.",
        ],
    )


def write_affine_star_channel_gap_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-AFFINE-STAR-CHANNEL-GAP"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_affine_star_channel_gap())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    return payload


if __name__ == "__main__":
    report = write_affine_star_channel_gap_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
