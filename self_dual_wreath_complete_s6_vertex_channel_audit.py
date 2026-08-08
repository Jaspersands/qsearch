"""Complete low-dimensional S6 audit of incident carrier-channel geometry.

The all-depth carrier-groupoid conjecture currently rests on selected finite
examples.  This module exhausts the largest globally distinct ``S_6``
four-pair portfolio whose source irreps all have dimension at most nine:

* the eight such irreps admit 105 perfect matchings;
* all eleven target irreps are tested, for 1,155 physical portfolios;
* every orientation vertex incident to at least three live pair cores is
  audited after exact common directions are removed.

There are 64 such vertices.  Sixteen have nonorthogonal residual traffic.
Every one of those sixteen has exactly one nontrivial connected component,
consisting of three incident pair cores.  The component is a clique, and the
three opposite orientation endpoints together with the shared vertex form an
affine plane.  The normalized component Gram has only clique eigenvalues
``0,1,3``; partial-isometry, support-commutation, path, and holonomy residuals
are at numerical roundoff.

This is a complete finite falsification search in a sharply stated portfolio,
not an all-``n`` theorem.  It excludes neither higher multiplicity channels,
larger source dimensions, multiple affine triangles sharing coefficient
space, nor nonflat channels at larger ``n`` or copy count.  Its value is to
replace three hand-selected controls by a precise conjecture and a concrete
counterexample target:

    every nonorthogonal residual incident channel is an affine triangle with
    a positive flat ``J_3`` Gram.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_collision_free_frame_probe import Label, perfect_matchings
from self_dual_wreath_orientation_laplacian_gap import _core_bases, live_pair_cores
from self_dual_wreath_vertex_channel_groupoid import (
    audit_vertex_channel_groupoid,
)
from self_dual_wreath_vertex_trivialization_criterion import (
    maximum_cross_correlation,
    residual_incident_core_bases,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_complete_s6_vertex_channel_audit.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-COMPLETE-S6-VERTEX-CHANNEL-AUDIT"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Edge = tuple[int, int]


@dataclass(frozen=True)
class NonorthogonalS6VertexControl:
    target_partition: Partition
    labels: tuple[Label, ...]
    shared_vertex: int
    live_pair_core_count: int
    incident_live_pair_core_count: int
    residual_edges: tuple[Edge, ...]
    residual_edge_dimensions: tuple[int, ...]
    maximum_residual_correlation: float
    nontrivial_component_count: int
    nontrivial_components: tuple[tuple[Edge, ...], ...]
    every_component_is_three_edge_clique: bool
    every_component_closes_one_affine_plane: bool
    maximum_partial_isometry_residual: float
    maximum_support_projection_commutator_norm: float
    maximum_path_composition_residual: float
    maximum_triangle_holonomy_residual: float
    normalized_gram_minimum_eigenvalue: float
    normalized_gram_distinct_eigenvalues: tuple[float, ...]
    flat_groupoid_verified: bool
    status: str


@dataclass(frozen=True)
class CompleteS6VertexChannelAuditReport:
    created_at: str
    theorem_contract: dict[str, Any]
    source_partition_set: tuple[Partition, ...]
    source_matching_count: int
    target_count: int
    physical_portfolio_count: int
    degree_at_least_three_vertex_count: int
    nonorthogonal_vertex_controls: list[NonorthogonalS6VertexControl]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def low_dimension_s6_source_partitions() -> tuple[Partition, ...]:
    return tuple(
        partition
        for partition in integer_partitions(6)
        if hook_length_dimension(partition) <= 9
    )


def low_dimension_s6_source_matchings() -> tuple[tuple[Label, ...], ...]:
    partitions = low_dimension_s6_source_partitions()
    return tuple(perfect_matchings(partitions))


def _nontrivial_incident_components(
    residual: dict[Edge, np.ndarray],
    *,
    tolerance: float,
) -> tuple[tuple[Edge, ...], ...]:
    adjacency = {edge: set() for edge in residual}
    for left, right in itertools.combinations(residual, 2):
        overlap = residual[left].conj().T @ residual[right]
        if overlap.size and np.linalg.norm(overlap, ord=2) > 100 * tolerance:
            adjacency[left].add(right)
            adjacency[right].add(left)
    unseen = set(adjacency)
    components: list[tuple[Edge, ...]] = []
    while unseen:
        seed = unseen.pop()
        stack = [seed]
        component = {seed}
        while stack:
            current = stack.pop()
            reached = adjacency[current] & unseen
            unseen -= reached
            component |= reached
            stack.extend(reached)
        if len(component) > 1:
            components.append(tuple(sorted(component)))
    return tuple(sorted(components))


def _component_is_clique(
    component: tuple[Edge, ...],
    residual: dict[Edge, np.ndarray],
    *,
    tolerance: float,
) -> bool:
    return all(
        np.linalg.norm(
            residual[left].conj().T @ residual[right],
            ord=2,
        )
        > 100 * tolerance
        for left, right in itertools.combinations(component, 2)
    )


def _component_is_affine_triangle(
    component: tuple[Edge, ...],
    shared_vertex: int,
) -> bool:
    if len(component) != 3:
        return False
    opposite = []
    for edge in component:
        if shared_vertex not in edge:
            return False
        opposite.append(next(iter(set(edge) - {shared_vertex})))
    return shared_vertex ^ opposite[0] ^ opposite[1] ^ opposite[2] == 0


def audit_nonorthogonal_s6_vertex(
    target: Partition,
    labels: tuple[Label, ...],
    live_edges: tuple[Edge, ...],
    shared_vertex: int,
    *,
    tolerance: float = 1e-8,
) -> NonorthogonalS6VertexControl | None:
    incident = tuple(edge for edge in live_edges if shared_vertex in edge)
    bases = _core_bases(target, labels, incident)
    residual, _ = residual_incident_core_bases(
        bases,
        incident,
        shared_vertex,
        tolerance=tolerance,
    )
    correlation = maximum_cross_correlation(residual)
    if correlation <= 100 * tolerance:
        return None
    components = _nontrivial_incident_components(
        residual,
        tolerance=tolerance,
    )
    cliques = all(
        len(component) == 3
        and _component_is_clique(
            component,
            residual,
            tolerance=tolerance,
        )
        for component in components
    )
    affine = all(
        _component_is_affine_triangle(component, shared_vertex)
        for component in components
    )
    groupoid = audit_vertex_channel_groupoid(
        "COMPLETE-S6-LOW-DIMENSION-VERTEX",
        target,
        labels,
        incident,
        shared_vertex,
        tolerance=tolerance,
    )
    verified = bool(
        components
        and cliques
        and affine
        and groupoid.flat_partial_isometry_groupoid_verified
        and groupoid.vertex_trivialization_certified
    )
    return NonorthogonalS6VertexControl(
        target_partition=target,
        labels=labels,
        shared_vertex=shared_vertex,
        live_pair_core_count=len(live_edges),
        incident_live_pair_core_count=len(incident),
        residual_edges=groupoid.residual_edges,
        residual_edge_dimensions=groupoid.residual_edge_dimensions,
        maximum_residual_correlation=groupoid.maximum_residual_correlation,
        nontrivial_component_count=len(components),
        nontrivial_components=components,
        every_component_is_three_edge_clique=cliques,
        every_component_closes_one_affine_plane=affine,
        maximum_partial_isometry_residual=(
            groupoid.maximum_partial_isometry_residual
        ),
        maximum_support_projection_commutator_norm=(
            groupoid.maximum_support_projection_commutator_norm
        ),
        maximum_path_composition_residual=(
            groupoid.maximum_path_composition_residual
        ),
        maximum_triangle_holonomy_residual=(
            groupoid.maximum_triangle_holonomy_projection_residual
        ),
        normalized_gram_minimum_eigenvalue=(
            groupoid.normalized_gram_minimum_eigenvalue
        ),
        normalized_gram_distinct_eigenvalues=(
            groupoid.normalized_gram_distinct_eigenvalues
        ),
        flat_groupoid_verified=verified,
        status=(
            "complete-s6-portfolio-affine-triangle-channel-verified"
            if verified
            else "complete-s6-portfolio-channel-falsifier-triggered"
        ),
    )


@lru_cache(maxsize=1)
def run_complete_s6_vertex_channel_audit(
) -> CompleteS6VertexChannelAuditReport:
    source_partitions = low_dimension_s6_source_partitions()
    matchings = low_dimension_s6_source_matchings()
    targets = tuple(integer_partitions(6))
    controls: list[NonorthogonalS6VertexControl] = []
    degree_at_least_three = 0
    residual_edge_count_histogram: dict[int, int] = {}
    for labels in matchings:
        for target in targets:
            live_edges = live_pair_cores(
                target,
                labels,
                tuple(range(16)),
            )
            incidence = {vertex: 0 for vertex in range(16)}
            for edge in live_edges:
                incidence[edge[0]] += 1
                incidence[edge[1]] += 1
            for vertex, degree in incidence.items():
                if degree < 3:
                    continue
                degree_at_least_three += 1
                control = audit_nonorthogonal_s6_vertex(
                    target,
                    labels,
                    live_edges,
                    vertex,
                )
                if control is None:
                    continue
                controls.append(control)
                residual_edge_count_histogram[len(control.residual_edges)] = (
                    residual_edge_count_histogram.get(
                        len(control.residual_edges),
                        0,
                    )
                    + 1
                )
    failures = sum(not control.flat_groupoid_verified for control in controls)
    component_count = sum(
        control.nontrivial_component_count for control in controls
    )
    every_one_component = all(
        control.nontrivial_component_count == 1 for control in controls
    )
    every_affine_triangle = all(
        control.every_component_is_three_edge_clique
        and control.every_component_closes_one_affine_plane
        for control in controls
    )
    maximum_residuals = {
        "partial": max(
            (row.maximum_partial_isometry_residual for row in controls),
            default=0.0,
        ),
        "commutator": max(
            (
                row.maximum_support_projection_commutator_norm
                for row in controls
            ),
            default=0.0,
        ),
        "path": max(
            (row.maximum_path_composition_residual for row in controls),
            default=0.0,
        ),
        "holonomy": max(
            (row.maximum_triangle_holonomy_residual for row in controls),
            default=0.0,
        ),
    }
    complete = bool(
        len(source_partitions) == 8
        and len(matchings) == 105
        and len(targets) == 11
        and degree_at_least_three == 64
        and len(controls) == 16
        and component_count == 16
        and every_one_component
        and every_affine_triangle
        and failures == 0
    )
    metrics: dict[str, int | float] = {
        "source_partition_count": len(source_partitions),
        "source_matching_count": len(matchings),
        "target_count": len(targets),
        "physical_portfolio_count": len(matchings) * len(targets),
        "degree_at_least_three_vertex_count": degree_at_least_three,
        "nonorthogonal_vertex_count": len(controls),
        "nontrivial_component_count": component_count,
        "three_edge_clique_component_count": sum(
            row.nontrivial_component_count
            for row in controls
            if row.every_component_is_three_edge_clique
        ),
        "affine_plane_component_count": sum(
            row.nontrivial_component_count
            for row in controls
            if row.every_component_closes_one_affine_plane
        ),
        "flat_groupoid_failure_count": failures,
        "maximum_partial_isometry_residual": maximum_residuals["partial"],
        "maximum_support_commutator_residual": maximum_residuals[
            "commutator"
        ],
        "maximum_path_residual": maximum_residuals["path"],
        "maximum_holonomy_residual": maximum_residuals["holonomy"],
        "all_n_affine_triangle_channel_theorem_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return CompleteS6VertexChannelAuditReport(
        created_at=utc_now(),
        theorem_contract={
            "portfolio": (
                "All 105 perfect matchings of the eight S6 irreps with "
                "dimension at most nine, crossed with all eleven targets."
            ),
            "vertex_filter": (
                "Every orientation vertex incident to at least three live "
                "pair cores is audited after removing exact common directions."
            ),
            "observed_channel_law": (
                "Every nonorthogonal residual component is exactly one "
                "three-edge clique whose opposite endpoints and shared vertex "
                "form an affine plane; its normalized Gram has clique spectrum."
            ),
            "scope_exclusion": (
                "This is exhaustive only inside the stated finite S6 source "
                "portfolio. It is not an all-n path law, hierarchy gap, "
                "natural-mass theorem, decoder, or speedup."
            ),
        },
        source_partition_set=source_partitions,
        source_matching_count=len(matchings),
        target_count=len(targets),
        physical_portfolio_count=len(matchings) * len(targets),
        degree_at_least_three_vertex_count=degree_at_least_three,
        nonorthogonal_vertex_controls=controls,
        proof_obligations=[
            {
                "obligation": "replace_selected_s6_groupoid_examples_with_complete_boundary",
                "resolved": complete,
                "resolution": (
                    "All 1,155 portfolios and all 64 high-degree vertices in "
                    "the stated low-dimensional S6 boundary were exhausted."
                ),
            },
            {
                "obligation": "classify_nonorthogonal_s6_incident_components",
                "resolved": complete,
                "resolution": (
                    "All sixteen components are single affine triangles with "
                    "positive flat clique Grams."
                ),
            },
            {
                "obligation": "prove_affine_triangle_channel_law_for_all_n",
                "resolved": False,
                "resolution": (
                    "Need a multiplicity-index tensor proof or a larger-n "
                    "counterexample; finite S6 exhaustion cannot settle it."
                ),
            },
            {
                "obligation": "exclude_overlapping_or_larger_high_multiplicity_channels",
                "resolved": False,
                "resolution": (
                    "The portfolio omits dimension-10 and dimension-16 source "
                    "irreps and every larger symmetric group."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "The original three selected controls could be cherry-picked.",
                "resolved": True,
                "resolution": (
                    "The new boundary enumerates every matching and target in "
                    "a predeclared globally distinct source set."
                ),
            },
            {
                "objection": "Flatness alone identifies the support geometry.",
                "resolved": True,
                "resolution": (
                    "The overlap adjacency was extracted independently; each "
                    "component is directly checked to be a three-edge affine clique."
                ),
            },
            {
                "objection": "Complete S6 exhaustion proves the asymptotic channel law.",
                "resolved": False,
                "resolution": (
                    "Higher Kronecker multiplicities can introduce channel "
                    "geometry absent from this finite boundary."
                ),
            },
            {
                "objection": "A vertex channel law alone proves the complete frame edge.",
                "resolved": False,
                "resolution": (
                    "Disjoint pair-core waist maps, all-depth channel gluing, "
                    "natural mass, and coherent implementation remain separate."
                ),
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "complete_stated_s6_portfolio_audited": complete,
            "every_observed_nonorthogonal_component_is_affine_triangle": (
                complete
            ),
            "every_observed_normalized_component_gram_is_positive_flat": (
                complete
            ),
            "all_n_affine_triangle_channel_law_proved": False,
            "higher_multiplicity_channel_falsifiers_excluded": False,
            "collision_free_noncommon_frame_edge_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The strongest finite vertex-channel conjecture survives a "
                "complete S6 boundary, but the all-n multiplicity-index law "
                "and global high-carrier edge remain open."
            ),
        },
        status=(
            "complete-s6-boundary-affine-triangles-only-all-n-law-open"
            if complete
            else "complete-s6-boundary-falsifier-triggered"
        ),
        summary=(
            "Exhausted 1,155 globally distinct S6 portfolios: all sixteen "
            "nonorthogonal high-degree vertex channels are positive flat "
            "affine triangles."
        ),
        falsifiers_triggered=[
            (
                "The three previously selected W6 controls were insufficient "
                "evidence; the complete finite boundary is now explicit."
            ),
            (
                "No larger, overlapping, noncommuting, or negative-holonomy "
                "channel occurs in the stated low-dimensional S6 portfolio."
            ),
            (
                "The result does not exclude such channels once higher "
                "multiplicity source irreps or larger n are admitted."
            ),
        ],
    )


def write_complete_s6_vertex_channel_audit_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_complete_s6_vertex_channel_audit())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_complete_s6_vertex_channel_audit_report()
    print(json.dumps(report, indent=2, sort_keys=True))
