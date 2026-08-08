"""Gauge homology of overlapping affine-plane carrier channels.

Positive scalar holonomy trivializes one affine plane, but planes sharing
pair-core coefficient space form a much larger point-line incidence graph.
The remaining signs live on incidence edges.  Point-basis and line-channel
sign changes are vertex gauges on this bipartite graph, so gauge classes are
its first ``F_2`` cohomology:

    dim H^1 = E - V + c.                                  (1)

For all planes through one orientation vertex, the points are the ``2^K-1``
nonzero vectors of ``F_2^K`` and the lines are the projective Steiner triples.
The incidence graph is connected and

    dim H^1 = (2^K-2)(2^K-4)/3.                           (2)

The collision-free support-pressure proof uses the pattern-rich lines, whose
coordinate restrictions contain ``00,01,10,11``.  A point of Hamming weight
``1<=w<=K-1`` has rich degree

    ((2^w-2)(2^(K-w)-2))/2.                               (3)

The all-ones point, of weight ``K``, has degree zero separately.  Thus exactly
``2K+1`` point vertices are isolated: weights ``1``, ``K-1``, and ``K``.
Every point of weight ``2,...,K-2`` lies in one connected giant component.  If
``R_K`` is the rich-line count, then

    dim H^1_rich = 2 R_K - 2^K + 2K + 3.                  (4)

This is ``Theta(4^K)``.  Line-local positive holonomy constrains none of these
longer cycle bits: a line is a three-leaf star in the incidence graph.  The
signed quotient-kernel construction has a negative six-cycle already on the
embedded four-coordinate rich subsystem, proving that it is not gauge
equivalent to the all-positive incidence frame.

Equations (1)-(4) do not assert that natural symmetric-group recoupling
samples arbitrary gauge classes.  They identify the missing theorem exactly:
natural cup/cap and Racah contractions must control a quadratic-dimensional
family of inter-plane cycle holonomies, not merely each local triangle.
"""

from __future__ import annotations

import itertools
import json
from collections import deque
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Literal

import numpy as np

from research_registry import utc_now
from self_dual_wreath_affine_plane_support_pressure_no_go import (
    rich_plane_count_per_vertex,
)
from self_dual_wreath_signed_steiner_incidence_boundary import (
    Line,
    projective_points,
    projective_steiner_lines,
    signed_steiner_incidence_with_quotient_kernel,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_interplane_gauge_homology.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-INTERPLANE-GAUGE-HOMOLOGY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

LineFamily = Literal["all", "pattern-rich"]


@dataclass(frozen=True)
class InterplaneGaugeHomologyControl:
    copy_count: int
    line_family: LineFamily
    point_count: int
    line_count: int
    incidence_edge_count: int
    isolated_point_count: int
    connected_component_count: int
    predicted_connected_component_count: int
    cycle_rank: int
    predicted_cycle_rank: int
    gauge_class_count_log2: int
    negative_six_cycle_points: tuple[int, int, int]
    negative_six_cycle_lines: tuple[Line, Line, Line]
    negative_six_cycle_product: int
    exact_component_and_cycle_count_verified: bool
    nontrivial_signed_cycle_class_verified: bool
    status: str


@dataclass(frozen=True)
class RichPointDegreeControl:
    copy_count: int
    point: int
    hamming_weight: int
    observed_rich_degree: int
    predicted_rich_degree: int
    exact_degree_verified: bool
    status: str


@dataclass(frozen=True)
class InterplaneGaugeHomologyReport:
    created_at: str
    theorem_contract: dict[str, Any]
    full_controls: list[InterplaneGaugeHomologyControl]
    rich_controls: list[InterplaneGaugeHomologyControl]
    rich_degree_controls: list[RichPointDegreeControl]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def line_is_pattern_rich(copy_count: int, line: Line) -> bool:
    first, second, _ = line
    return len(
        {
            ((first >> coordinate) & 1, (second >> coordinate) & 1)
            for coordinate in range(copy_count)
        }
    ) == 4


def pattern_rich_steiner_lines(copy_count: int) -> tuple[Line, ...]:
    if copy_count < 4:
        return ()
    return tuple(
        line
        for line in projective_steiner_lines(copy_count)
        if line_is_pattern_rich(copy_count, line)
    )


def predicted_rich_point_degree(copy_count: int, point: int) -> int:
    if point not in projective_points(copy_count):
        raise ValueError("point must be a nonzero K-bit vector")
    weight = point.bit_count()
    if weight == copy_count:
        return 0
    return (
        (2**weight - 2) * (2 ** (copy_count - weight) - 2) // 2
    )


def audit_rich_point_degree(
    copy_count: int,
    point: int,
) -> RichPointDegreeControl:
    lines = pattern_rich_steiner_lines(copy_count)
    observed = sum(point in line for line in lines)
    predicted = predicted_rich_point_degree(copy_count, point)
    verified = observed == predicted
    return RichPointDegreeControl(
        copy_count=copy_count,
        point=point,
        hamming_weight=point.bit_count(),
        observed_rich_degree=observed,
        predicted_rich_degree=predicted,
        exact_degree_verified=verified,
        status=(
            "exact-rich-point-degree-verified"
            if verified
            else "rich-point-degree-control-failure"
        ),
    )


def _incidence_graph_components(
    copy_count: int,
    lines: tuple[Line, ...],
) -> tuple[int, int]:
    point_nodes = [("point", point) for point in projective_points(copy_count)]
    line_nodes = [("line", index) for index in range(len(lines))]
    adjacency: dict[tuple[str, int], list[tuple[str, int]]] = {
        node: [] for node in point_nodes + line_nodes
    }
    for line_index, line in enumerate(lines):
        line_node = ("line", line_index)
        for point in line:
            point_node = ("point", point)
            adjacency[point_node].append(line_node)
            adjacency[line_node].append(point_node)

    unseen = set(adjacency)
    component_count = 0
    while unseen:
        component_count += 1
        root = unseen.pop()
        queue = deque([root])
        while queue:
            node = queue.popleft()
            for neighbor in adjacency[node]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    queue.append(neighbor)
    isolated = sum(not adjacency[node] for node in point_nodes)
    return component_count, isolated


def _signed_columns_for_lines(
    copy_count: int,
    lines: tuple[Line, ...],
) -> np.ndarray:
    all_lines = projective_steiner_lines(copy_count)
    all_incidence, _ = signed_steiner_incidence_with_quotient_kernel(
        copy_count
    )
    column_index = {line: index for index, line in enumerate(all_lines)}
    return all_incidence[:, [column_index[line] for line in lines]]


def find_negative_six_cycle(
    copy_count: int,
    lines: tuple[Line, ...],
    incidence: np.ndarray,
) -> tuple[tuple[int, int, int], tuple[Line, Line, Line], int] | None:
    points = projective_points(copy_count)
    point_index = {point: index for index, point in enumerate(points)}
    pair_line: dict[frozenset[int], int] = {}
    for line_index, line in enumerate(lines):
        for first, second in itertools.combinations(line, 2):
            pair_line[frozenset((first, second))] = line_index
    for first, second, third in itertools.combinations(points, 3):
        pairs = (
            frozenset((first, second)),
            frozenset((second, third)),
            frozenset((third, first)),
        )
        if any(pair not in pair_line for pair in pairs):
            continue
        line_indices = tuple(pair_line[pair] for pair in pairs)
        if len(set(line_indices)) < 3:
            continue
        product = int(
            incidence[point_index[first], line_indices[0]]
            * incidence[point_index[second], line_indices[0]]
            * incidence[point_index[second], line_indices[1]]
            * incidence[point_index[third], line_indices[1]]
            * incidence[point_index[third], line_indices[2]]
            * incidence[point_index[first], line_indices[2]]
        )
        if product == -1:
            return (
                (first, second, third),
                tuple(lines[index] for index in line_indices),
                product,
            )
    return None


def predicted_interplane_cycle_rank(
    copy_count: int,
    line_family: LineFamily,
) -> int:
    orientation_count = 1 << copy_count
    if line_family == "all":
        return (orientation_count - 2) * (orientation_count - 4) // 3
    if line_family == "pattern-rich":
        return (
            2 * rich_plane_count_per_vertex(copy_count)
            - orientation_count
            + 2 * copy_count
            + 3
        )
    raise ValueError("unknown line family")


def audit_interplane_gauge_homology(
    copy_count: int,
    line_family: LineFamily,
) -> InterplaneGaugeHomologyControl:
    if line_family == "all":
        lines = projective_steiner_lines(copy_count)
        predicted_components = 1
    elif line_family == "pattern-rich":
        if copy_count < 4:
            raise ValueError("pattern-rich controls require K>=4")
        lines = pattern_rich_steiner_lines(copy_count)
        predicted_components = 2 * copy_count + 2
    else:
        raise ValueError("unknown line family")

    point_count = len(projective_points(copy_count))
    edge_count = 3 * len(lines)
    components, isolated = _incidence_graph_components(copy_count, lines)
    cycle_rank = edge_count - point_count - len(lines) + components
    predicted_cycle_rank = predicted_interplane_cycle_rank(
        copy_count,
        line_family,
    )
    incidence = _signed_columns_for_lines(copy_count, lines)
    negative_cycle = find_negative_six_cycle(copy_count, lines, incidence)
    if negative_cycle is None:
        cycle_points: tuple[int, int, int] = ()
        cycle_lines: tuple[Line, Line, Line] = ()
        cycle_product = 1
    else:
        cycle_points, cycle_lines, cycle_product = negative_cycle
    counts_verified = bool(
        components == predicted_components
        and cycle_rank == predicted_cycle_rank
        and (
            isolated == 0
            if line_family == "all"
            else isolated == 2 * copy_count + 1
        )
    )
    nontrivial = cycle_product == -1
    return InterplaneGaugeHomologyControl(
        copy_count=copy_count,
        line_family=line_family,
        point_count=point_count,
        line_count=len(lines),
        incidence_edge_count=edge_count,
        isolated_point_count=isolated,
        connected_component_count=components,
        predicted_connected_component_count=predicted_components,
        cycle_rank=cycle_rank,
        predicted_cycle_rank=predicted_cycle_rank,
        gauge_class_count_log2=cycle_rank,
        negative_six_cycle_points=cycle_points,
        negative_six_cycle_lines=cycle_lines,
        negative_six_cycle_product=cycle_product,
        exact_component_and_cycle_count_verified=counts_verified,
        nontrivial_signed_cycle_class_verified=nontrivial,
        status=(
            "quadratic-interplane-gauge-space-with-negative-cycle"
            if counts_verified and nontrivial
            else "interplane-gauge-homology-control-failure"
        ),
    )


def run_interplane_gauge_homology() -> InterplaneGaugeHomologyReport:
    full_controls = [
        audit_interplane_gauge_homology(copy_count, "all")
        for copy_count in range(3, 9)
    ]
    rich_controls = [
        audit_interplane_gauge_homology(copy_count, "pattern-rich")
        for copy_count in range(4, 9)
    ]
    degree_controls = [
        audit_rich_point_degree(copy_count, point)
        for copy_count in range(4, 9)
        for point in range(1, 1 << copy_count)
    ]
    failures = sum(
        not (
            row.exact_component_and_cycle_count_verified
            and row.nontrivial_signed_cycle_class_verified
        )
        for row in full_controls + rich_controls
    ) + sum(not row.exact_degree_verified for row in degree_controls)
    tail = rich_controls[-1]
    return InterplaneGaugeHomologyReport(
        created_at=utc_now(),
        theorem_contract={
            "gauge_classification": (
                "Incidence-edge signs modulo point and line basis signs form "
                "H^1 of the bipartite point-line graph, of dimension E-V+c."
            ),
            "full_cycle_rank": (
                "For all PG(K-1,2) lines, beta_1=(2^K-2)(2^K-4)/3."
            ),
            "rich_point_degree": (
                "For 1<=w<=K-1, a weight-w point has rich degree "
                "(2^w-2)(2^(K-w)-2)/2; the all-ones point has "
                "degree zero."
            ),
            "rich_connectivity": (
                "Weights 2 through K-2 form one component: each such subset "
                "crosses a two-subset, and the two-subsets form connected "
                "Johnson graph J(K,2)."
            ),
            "rich_cycle_rank": (
                "For pattern-rich lines, beta_1=2R_K-2^K+2K+3="
                "Theta(4^K)."
            ),
            "negative_cycle_witness": (
                "The F_2^2 quotient signing has a negative six-cycle on the "
                "embedded four-coordinate rich subsystem at every K>=4."
            ),
        },
        full_controls=full_controls,
        rich_controls=rich_controls,
        rich_degree_controls=degree_controls,
        proof_obligations=[
            {
                "obligation": "classify_scalar_interplane_sign_gauges",
                "resolved": failures == 0,
                "resolution": (
                    "Standard graph cohomology gives one independent bit per "
                    "incidence cycle after point and line gauges."
                ),
            },
            {
                "obligation": "count_pattern_rich_cycle_debt",
                "resolved": failures == 0,
                "resolution": (
                    "Exact point degrees and crossing-graph connectivity give "
                    "the rich component and cycle-rank formula."
                ),
            },
            {
                "obligation": "derive_natural_cycle_holonomy_law",
                "resolved": False,
                "resolution": (
                    "No theorem yet evaluates the longer cycle products of "
                    "natural S_n cup/cap and Racah contractions."
                ),
            },
            {
                "obligation": "prove_natural_gauge_concentration_or_flatness",
                "resolved": False,
                "resolution": (
                    "The admissible gauge space has Theta(4^K) dimensions; a "
                    "local-plane argument cannot control it."
                ),
            },
            {
                "obligation": "extend_scalar_cohomology_to_orthogonal_transport",
                "resolved": False,
                "resolution": (
                    "Multiplicity spaces require nonabelian O(m) connection "
                    "holonomies and operator-valued cycle moments."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Positive triangle holonomy removes every sign gauge.",
                "resolved": True,
                "resolution": (
                    "A line has no cycle in the bipartite incidence graph; all "
                    "nontrivial invariants run through several planes."
                ),
            },
            {
                "objection": "Restricting to rich planes makes the gauge debt sparse.",
                "resolved": True,
                "resolution": (
                    "False: only 2K+1 points become isolated and the rich cycle "
                    "rank remains Theta(4^K)."
                ),
            },
            {
                "objection": "Every cohomology class is naturally realizable.",
                "resolved": False,
                "resolution": (
                    "The combinatorial classification supplies possibilities, "
                    "not the distribution induced by symmetric-group recoupling."
                ),
            },
            {
                "objection": "A nontrivial scalar cycle forces poor PGM success.",
                "resolved": False,
                "resolution": (
                    "Conditioning depends on weighted matrix traffic and bad-mode "
                    "mass, not merely existence of one frustrated cycle."
                ),
            },
        ],
        headline_metrics={
            "full_homology_control_count": len(full_controls),
            "rich_homology_control_count": len(rich_controls),
            "rich_point_degree_control_count": len(degree_controls),
            "finite_control_failure_count": failures,
            "tail_rich_copy_count": tail.copy_count,
            "tail_rich_cycle_rank": tail.cycle_rank,
            "scalar_interplane_gauge_classification_theorem_count": 1,
            "rich_cycle_rank_theorem_count": 1,
            "natural_cycle_holonomy_theorem_count": 0,
            "operator_valued_connection_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "scalar_interplane_gauges_classified": failures == 0,
            "rich_cycle_rank_quadratic": failures == 0,
            "local_plane_holonomy_controls_global_gauge": False,
            "natural_cycle_holonomy_law_derived": False,
            "natural_gauge_flat_or_concentrated": False,
            "operator_valued_overlap_traffic_controlled": False,
            "collision_free_noncommon_frame_edge_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The missing natural theorem concerns a quadratic family of "
                "long inter-plane cycles and their matrix-valued extensions."
            ),
        },
        status="interplane-gauge-space-classified-natural-cycle-law-open",
        summary=(
            "Classified the scalar inter-plane gauge obstruction and proved "
            "that the pattern-rich hierarchy retains Theta(4^K) independent "
            "cycle bits despite every local plane being positive."
        ),
        falsifiers_triggered=[
            (
                "Single-plane positive-holonomy audits cannot establish a "
                "global gauge or frame edge, even on the rich support family."
            ),
            (
                "The all-positive Steiner surrogate is one gauge class among "
                "2^Theta(4^K) combinatorially admissible classes."
            ),
            (
                "Future finite audits must include multi-plane incidence cycles "
                "and report gauge-invariant cycle products."
            ),
        ],
    )


def write_interplane_gauge_homology_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-INTERPLANE-GAUGE-HOMOLOGY"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_interplane_gauge_homology())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    if write_registry:
        from research_registry import (
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-SELF-DUAL-WREATH-INTERPLANE-GAUGE-HOMOLOGY",
                source=registry_experiment_id,
                claim=(
                    "Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-INTERPLANE-GAUGE-HOMOLOGY."
                ),
                reason_invalid=(
                    "Falsified or refined by exact theorem evaluation."
                ),
                lesson=(
                    "Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-INTERPLANE-GAUGE-HOMOLOGY."
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
                    "self_dual_wreath_interplane_gauge_homology": str(path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_interplane_gauge_homology_report()
    print(json.dumps(report, indent=2, sort_keys=True))
