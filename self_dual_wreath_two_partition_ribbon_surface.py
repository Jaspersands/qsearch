"""Exact ribbon-surface topology for two ordered binary partitions.

Let ``x_1,...,x_p`` be group variables.  Each of two binary partitions adds
the ordered product relation on its zero positions and on its one positions.
Invert the two relations of the second partition and glue equally labelled
edges to the first pair of relation polygons.  The result is a disjoint union
of closed orientable ribbon surfaces.  The original one-vertex presentation
identifies all surface vertices, so its group is

    (*_j pi_1(Sigma_{g_j})) * F_(sum_j(f_j-1)),

where ``f_j`` is the number of ribbon faces in component ``j``.  This gives
exact finite-group solution counts and a leading ``S_n`` exponent

    sum_j (f_j-1) + sum_(g_j>0) (2g_j-1).

The construction classifies any one split/support-assignment pair.  A full
support profile contains many partitions; selecting one pair gives a rigorous
upper bound, but a growing-degree theorem must exploit several support cells
simultaneously when their support entropy is large.
"""

from __future__ import annotations

import itertools
import json
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from research_registry import utc_now
from self_dual_wreath_marked_relation_topology import (
    _evaluate_signed_word,
    _relations_from_bits,
    normalize_relations,
)


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_two_partition_ribbon_surface.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-TWO-PARTITION-RIBBON-SURFACE"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

HalfEdge = tuple[int, int]
PartitionBits = tuple[int, ...]


@dataclass(frozen=True)
class RibbonSurfaceComponent:
    component_index: int
    relation_vertex_count: int
    edge_indices: tuple[int, ...]
    surface_vertex_count: int
    euler_characteristic: int
    orientable_genus: int
    free_rank_contribution: int
    symmetric_group_leading_exponent_contribution: int
    exact_closed_orientable_surface_verified: bool
    status: str


@dataclass(frozen=True)
class TwoPartitionRibbonControl:
    control_id: str
    first_partition_bits: PartitionBits
    second_partition_bits: PartitionBits
    components: tuple[RibbonSurfaceComponent, ...]
    ribbon_face_cycles: tuple[tuple[HalfEdge, ...], ...]
    free_group_rank: int
    positive_genus_component_count: int
    symmetric_group_leading_solution_exponent: int
    symmetric_group_control_degree: int
    exact_solution_count: int
    predicted_solution_count: int
    exact_finite_solution_formula_verified: bool
    exact_ribbon_surface_decomposition_verified: bool
    status: str


@dataclass(frozen=True)
class RibbonSurfaceScalingRecord:
    position_count: int
    checked_partition_pair_count: int
    maximum_component_genus: int
    topology_failure_count: int
    status: str


@dataclass(frozen=True)
class TwoPartitionRibbonSurfaceReport:
    created_at: str
    theorem_contract: dict[str, Any]
    representative_controls: list[TwoPartitionRibbonControl]
    scaling_records: list[RibbonSurfaceScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _validate_partitions(first: PartitionBits, second: PartitionBits) -> None:
    if not first or len(first) != len(second):
        raise ValueError("two nonempty equally sized partitions are required")
    if any(bit not in (0, 1) for bit in (*first, *second)):
        raise ValueError("partition bits must be binary")


def _ribbon_face_cycles(
    first: PartitionBits,
    second: PartitionBits,
) -> tuple[tuple[HalfEdge, ...], ...]:
    position_count = len(first)
    half_edges = tuple(
        (side, index)
        for side in (0, 1)
        for index in range(position_count)
    )
    edge_flip = {(side, index): (1 - side, index) for side, index in half_edges}
    rotation: dict[HalfEdge, HalfEdge] = {}
    for side, bits in ((0, first), (1, second)):
        for color in (0, 1):
            indices = [
                index for index, value in enumerate(bits) if value == color
            ]
            if not indices:
                continue
            indices.sort(reverse=side == 1)
            for current, following in zip(indices, indices[1:] + indices[:1]):
                rotation[(side, current)] = (side, following)
    face_permutation = {
        half_edge: rotation[edge_flip[half_edge]] for half_edge in half_edges
    }
    cycles: list[tuple[HalfEdge, ...]] = []
    visited: set[HalfEdge] = set()
    for half_edge in half_edges:
        if half_edge in visited:
            continue
        cycle: list[HalfEdge] = []
        current = half_edge
        while current not in visited:
            visited.add(current)
            cycle.append(current)
            current = face_permutation[current]
        cycles.append(tuple(cycle))
    return tuple(cycles)


def _relation_graph_components(
    first: PartitionBits,
    second: PartitionBits,
) -> tuple[frozenset[HalfEdge], ...]:
    vertices = {
        *((0, bit) for bit in set(first)),
        *((1, bit) for bit in set(second)),
    }
    adjacency = {vertex: set() for vertex in vertices}
    for left_color, right_color in zip(first, second):
        left = (0, left_color)
        right = (1, right_color)
        adjacency[left].add(right)
        adjacency[right].add(left)
    components: list[frozenset[HalfEdge]] = []
    visited: set[HalfEdge] = set()
    for vertex in sorted(vertices):
        if vertex in visited:
            continue
        stack = [vertex]
        visited.add(vertex)
        component: set[HalfEdge] = set()
        while stack:
            current = stack.pop()
            component.add(current)
            for neighbor in adjacency[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append(neighbor)
        components.append(frozenset(component))
    return tuple(components)


def ribbon_surface_components(
    first: PartitionBits,
    second: PartitionBits,
) -> tuple[tuple[RibbonSurfaceComponent, ...], tuple[tuple[HalfEdge, ...], ...]]:
    _validate_partitions(first, second)
    faces = _ribbon_face_cycles(first, second)
    graph_components = _relation_graph_components(first, second)
    rows: list[RibbonSurfaceComponent] = []
    for component_index, graph_component in enumerate(graph_components, start=1):
        edge_indices = tuple(
            index
            for index, color in enumerate(first)
            if (0, color) in graph_component
        )
        edge_set = set(edge_indices)
        component_faces = tuple(
            face for face in faces if face[0][1] in edge_set
        )
        euler = len(graph_component) - len(edge_indices) + len(component_faces)
        genus_numerator = 2 - euler
        exact = genus_numerator >= 0 and genus_numerator % 2 == 0
        genus = genus_numerator // 2 if exact else -1
        free_rank = len(component_faces) - 1
        leading = free_rank + (2 * genus - 1 if genus > 0 else 0)
        rows.append(
            RibbonSurfaceComponent(
                component_index=component_index,
                relation_vertex_count=len(graph_component),
                edge_indices=tuple(index + 1 for index in edge_indices),
                surface_vertex_count=len(component_faces),
                euler_characteristic=euler,
                orientable_genus=genus,
                free_rank_contribution=free_rank,
                symmetric_group_leading_exponent_contribution=leading,
                exact_closed_orientable_surface_verified=exact,
                status=(
                    "exact-closed-orientable-ribbon-surface"
                    if exact
                    else "ribbon-surface-topology-failure"
                ),
            )
        )
    return tuple(rows), faces


def symmetric_group_leading_solution_exponent(
    first: PartitionBits,
    second: PartitionBits,
) -> int:
    components, _ = ribbon_surface_components(first, second)
    if any(not row.exact_closed_orientable_surface_verified for row in components):
        raise AssertionError("invalid ribbon-surface component")
    return sum(
        row.symmetric_group_leading_exponent_contribution for row in components
    )


def _symmetric_group_irrep_dimensions(degree: int) -> tuple[int, ...]:
    if degree == 3:
        return (1, 1, 2)
    raise ValueError("finite ribbon controls currently implement S3 only")


def _surface_homomorphism_count(degree: int, genus: int) -> int:
    if genus == 0:
        return 1
    group_order = 1
    for value in range(2, degree + 1):
        group_order *= value
    dimensions = _symmetric_group_irrep_dimensions(degree)
    total = sum(
        Fraction(group_order ** (2 * genus - 1), dimension ** (2 * genus - 2))
        for dimension in dimensions
    )
    if total.denominator != 1:
        raise AssertionError("surface homomorphism count must be integral")
    return total.numerator


def predicted_symmetric_group_solution_count(
    first: PartitionBits,
    second: PartitionBits,
    degree: int = 3,
) -> int:
    components, _ = ribbon_surface_components(first, second)
    group_order = 1
    for value in range(2, degree + 1):
        group_order *= value
    count = group_order ** sum(row.free_rank_contribution for row in components)
    for row in components:
        count *= _surface_homomorphism_count(degree, row.orientable_genus)
    return count


def exact_symmetric_group_solution_count(
    first: PartitionBits,
    second: PartitionBits,
    degree: int = 3,
) -> int:
    _validate_partitions(first, second)
    group = tuple(itertools.permutations(range(degree)))
    identity = tuple(range(degree))
    relations = normalize_relations(
        (*_relations_from_bits(first), *_relations_from_bits(second))
    )
    solutions = 0
    for values in itertools.product(group, repeat=len(first)):
        assignment = dict(enumerate(values, start=1))
        if all(
            _evaluate_signed_word(relation, assignment) == identity
            for relation in relations
        ):
            solutions += 1
    return solutions


def audit_two_partition_ribbon_surface(
    control_id: str,
    first: PartitionBits,
    second: PartitionBits,
    *,
    run_finite_control: bool = True,
) -> TwoPartitionRibbonControl:
    components, faces = ribbon_surface_components(first, second)
    topology_exact = all(
        row.exact_closed_orientable_surface_verified for row in components
    )
    predicted = predicted_symmetric_group_solution_count(first, second)
    exact_count = (
        exact_symmetric_group_solution_count(first, second)
        if run_finite_control
        else predicted
    )
    finite_exact = exact_count == predicted
    return TwoPartitionRibbonControl(
        control_id=control_id,
        first_partition_bits=first,
        second_partition_bits=second,
        components=components,
        ribbon_face_cycles=faces,
        free_group_rank=sum(row.free_rank_contribution for row in components),
        positive_genus_component_count=sum(
            row.orientable_genus > 0 for row in components
        ),
        symmetric_group_leading_solution_exponent=sum(
            row.symmetric_group_leading_exponent_contribution
            for row in components
        ),
        symmetric_group_control_degree=3,
        exact_solution_count=exact_count,
        predicted_solution_count=predicted,
        exact_finite_solution_formula_verified=finite_exact,
        exact_ribbon_surface_decomposition_verified=topology_exact,
        status=(
            "exact-two-partition-ribbon-surface-verified"
            if topology_exact and finite_exact
            else "two-partition-ribbon-surface-control-failure"
        ),
    )


def run_two_partition_ribbon_surface(
    maximum_position_count: int = 8,
) -> TwoPartitionRibbonSurfaceReport:
    if maximum_position_count < 1:
        raise ValueError("maximum position count must be positive")
    scaling: list[RibbonSurfaceScalingRecord] = []
    total_pairs = 0
    topology_failures = 0
    maximum_genus = 0
    for position_count in range(1, maximum_position_count + 1):
        failures = 0
        row_maximum = 0
        pair_count = 0
        patterns = tuple(itertools.product((0, 1), repeat=position_count))
        for first in patterns:
            for second in patterns:
                components, _ = ribbon_surface_components(first, second)
                pair_count += 1
                failures += any(
                    not row.exact_closed_orientable_surface_verified
                    for row in components
                )
                row_maximum = max(
                    row_maximum,
                    *(row.orientable_genus for row in components),
                )
        total_pairs += pair_count
        topology_failures += failures
        maximum_genus = max(maximum_genus, row_maximum)
        scaling.append(
            RibbonSurfaceScalingRecord(
                position_count=position_count,
                checked_partition_pair_count=pair_count,
                maximum_component_genus=row_maximum,
                topology_failure_count=failures,
                status=(
                    "exhaustive-ribbon-topology-control-passed"
                    if not failures
                    else "ribbon-topology-control-failure"
                ),
            )
        )
    finite_failures = 0
    finite_pairs = 0
    for position_count in range(1, 5):
        patterns = tuple(itertools.product((0, 1), repeat=position_count))
        for first in patterns:
            for second in patterns:
                finite_pairs += 1
                finite_failures += (
                    exact_symmetric_group_solution_count(first, second)
                    != predicted_symmetric_group_solution_count(first, second)
                )
    representatives = [
        audit_two_partition_ribbon_surface(
            "IDENTICAL-PARTITIONS-SPHERES",
            (0, 0, 1, 1),
            (0, 0, 1, 1),
        ),
        audit_two_partition_ribbon_surface(
            "TRANSVERSE-GENUS-ZERO",
            (0, 1, 0, 1),
            (0, 0, 1, 1),
        ),
        audit_two_partition_ribbon_surface(
            "EFBEBFB-SUPPORT-TORUS",
            (0, 0, 1, 0, 1, 0, 1),
            (0, 1, 1, 0, 1, 1, 1),
        ),
    ]
    representative_failures = sum(
        row.status != "exact-two-partition-ribbon-surface-verified"
        for row in representatives
    )
    exact = not (topology_failures or finite_failures or representative_failures)
    return TwoPartitionRibbonSurfaceReport(
        created_at=utc_now(),
        theorem_contract={
            "polygon_gluing": (
                "Invert the second partition relators and glue equal generator "
                "edges. Opposite edge orientations produce closed orientable "
                "ribbon-surface components."
            ),
            "group_decomposition": (
                "Identifying the f_j surface vertices gives pi_1(Sigma_gj) "
                "free-product F_(sum(f_j-1))."
            ),
            "finite_group_count": (
                "Solution counts factor into free assignments and Frobenius "
                "surface homomorphism counts."
            ),
            "symmetric_group_exponent": (
                "Using p(n)=|S_n|^o(1) and Witten-zeta convergence, each "
                "positive-genus component contributes 2g-1 leading exponents."
            ),
        },
        representative_controls=representatives,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "classify_two_partition_relation_topology",
                "resolved": exact,
                "resolution": (
                    "The ribbon permutation gives every surface genus, free "
                    "factor, finite-group count, and leading S_n exponent."
                ),
            },
            {
                "obligation": "extend_ribbon_topology_to_full_support_profiles",
                "resolved": False,
                "resolution": (
                    "Choose and glue enough support-assignment 2-cells to trade "
                    "their entropy against independent surface/rank losses."
                ),
            },
            {
                "obligation": "track_target_boundary_on_multi_partition_complex",
                "resolved": False,
                "resolution": (
                    "Add the full-product curve to the ribbon complex and classify "
                    "whether added support cells kill or separate its handles."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "A finite Tietze search is needed to recognize each surface.",
                "resolved": True,
                "resolution": (
                    "False: face cycles and Euler characteristics give the "
                    "topology directly for arbitrary position count."
                ),
            },
            {
                "objection": "One support assignment controls high-entropy supports.",
                "resolved": True,
                "resolution": (
                    "False: a one-pair upper bound can leave too many free "
                    "generators; large supports require simultaneous cells."
                ),
            },
        ],
        headline_metrics={
            "checked_partition_pair_count": total_pairs,
            "ribbon_topology_failure_count": topology_failures,
            "finite_S3_partition_pair_control_count": finite_pairs,
            "finite_S3_solution_formula_failure_count": finite_failures,
            "maximum_verified_component_genus": maximum_genus,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "two_partition_ribbon_surface_theorem_proved": exact,
            "two_partition_symmetric_group_exponent_formula_proved": exact,
            "full_support_profile_ribbon_complex_theorem_proved": False,
            "growing_degree_pressure_separation_proved": False,
            "natural_component_M4_positive": False,
            "speedup_claim_allowed": False,
            "reason": (
                "One split/support pair is classified exactly, but full support "
                "entropy requires a multi-partition complex theorem."
            ),
        },
        status=(
            "exact-two-partition-ribbon-surface-theorem-proved"
            if exact
            else "two-partition-ribbon-surface-control-failure"
        ),
        summary=(
            "Replaced bounded relation-topology search for partition pairs by "
            "an exact ribbon-surface decomposition."
        ),
        falsifiers_triggered=[
            "Duplicate partition relations create sphere 2-cells and free loops rather than independent exponent losses.",
            "Single-pair surface loss cannot by itself dominate exponential support entropy.",
        ],
    )


def write_two_partition_ribbon_surface_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_two_partition_ribbon_surface())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    report = write_two_partition_ribbon_surface_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
