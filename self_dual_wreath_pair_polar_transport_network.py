"""Pair-polar transport networks for affine coefficient fibers.

For two leaf projectors ``E_i,E_j``, the polar factor of ``E_j E_i`` maps
principal-vector subspaces of ``ran(E_i)`` to those of ``ran(E_j)``.  A path
of such polar factors can therefore implement an affine-bundle fiber
transport when every edge preserves the relevant fiber and the accumulated
internal gauge is known.

The finite label-distinct ``W_3`` affine plane has a complete bipartite
pair-overlap graph.  Directly orthogonal generator fibers are connected by
two pair-polar edges, and every active-fiber pair is connected with diameter
two.  The two tested coefficient normalizations produce only ``+I`` or
``-I`` endpoint gauges.  The ``W_5`` isolated anchor line uses one common-
range edge.

The normalized-cross-overlap implementation in this module does not scale:
its singular values are ``1/d_alpha``.  The later GPE pair-polar theorem
bypasses that access model and implements every active edge polar directly,
independent of ``d_alpha``.  The surviving all-n requirements are polynomial
coherent path selection, active-fiber coverage, and controlled nonabelian
gauge/holonomy.  Small pair correlation is still a valid QSVT obstruction,
but no longer a fundamental transport obstruction.
"""

from __future__ import annotations

import collections
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_collision_free_frame_probe import Label, _w5_probe_labels
from self_dual_wreath_level_three_flag_audit import _reduced_projector_family
from self_dual_wreath_shorted_overlap_balance import (
    _psd_pseudoinverse,
    _range_intersection_basis,
    _support_basis,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_pair_polar_transport_network.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-PAIR-POLAR-TRANSPORT-NETWORK"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class PairPolarTransportControl:
    control_id: str
    n: int
    target_partition: tuple[int, ...]
    labels: tuple[Label, ...]
    left_orientation_masks: tuple[int, ...]
    right_orientation_masks: tuple[int, ...]
    active_orientation_masks: tuple[int, ...]
    intersection_dimension: int
    transport_graph_edge_count: int
    transport_graph_connected: bool
    transport_graph_diameter: int | None
    minimum_used_edge_principal_correlation: float | None
    maximum_used_edge_principal_correlation: float | None
    maximum_path_fiber_range_leakage: float
    maximum_path_fiber_isometry_residual: float
    maximum_endpoint_scalar_sign_gauge_residual: float
    positive_sign_path_count: int
    negative_sign_path_count: int
    unreachable_ordered_fiber_pair_count: int
    direct_pair_transport_count: int
    two_edge_pair_transport_count: int
    exact_pair_polar_transport_network_verified: bool
    finite_inverse_polynomial_correlation_control: bool
    status: str


@dataclass(frozen=True)
class PairPolarTransportScalingRecord:
    n: int
    information_threshold_copy_count: int
    noncommon_pair_correlation_form: str
    smallest_possible_nonzero_pair_correlation_log2_lower_bound: float
    smallest_possible_nonzero_pair_correlation_can_be_exponential: bool
    polynomial_transport_graph_diameter_proved: bool
    inverse_polynomial_used_edge_correlation_proved: bool
    gpe_direct_pair_polar_bypasses_edge_correlation: bool
    polynomial_coherent_path_finder_proved: bool
    efficiently_correctable_internal_gauge_proved: bool
    hierarchical_orientation_polar_proved: bool
    status: str


@dataclass(frozen=True)
class PairPolarTransportNetworkReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[PairPolarTransportControl]
    scaling_records: list[PairPolarTransportScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _polar_factor(
    matrix: np.ndarray,
    tolerance: float,
) -> tuple[np.ndarray, np.ndarray]:
    left, singular_values, right = np.linalg.svd(matrix, full_matrices=False)
    positive = singular_values > tolerance
    if not np.any(positive):
        return np.zeros_like(matrix), np.asarray([], dtype=float)
    return (
        left[:, positive] @ right[positive, :],
        singular_values[positive],
    )


def _shortest_paths(
    adjacency: dict[int, tuple[int, ...]],
    source: int,
) -> dict[int, tuple[int, ...]]:
    paths = {source: (source,)}
    queue = collections.deque((source,))
    while queue:
        node = queue.popleft()
        for neighbor in adjacency[node]:
            if neighbor not in paths:
                paths[neighbor] = (*paths[node], neighbor)
                queue.append(neighbor)
    return paths


def audit_pair_polar_transport_network(
    control_id: str,
    n: int,
    target: tuple[int, ...],
    labels: tuple[Label, ...],
    left_masks: tuple[int, ...],
    right_masks: tuple[int, ...],
    *,
    tolerance: float = 1e-8,
) -> PairPolarTransportControl:
    projectors, _, _ = _reduced_projector_family(target, labels, tolerance)
    dimension = len(projectors[0])
    zero = np.zeros((dimension, dimension), dtype=complex)
    left = sum((projectors[mask] for mask in left_masks), zero.copy())
    right = sum((projectors[mask] for mask in right_masks), zero.copy())
    core = _range_intersection_basis(
        _support_basis(left, tolerance),
        _support_basis(right, tolerance),
        tolerance,
    )
    rank = core.shape[1]
    if not rank:
        raise ValueError("the selected merge has no child-range intersection")

    fiber_maps: dict[int, np.ndarray] = {}
    for masks, frame in ((left_masks, left), (right_masks, right)):
        inverse = _psd_pseudoinverse(frame, tolerance)
        for mask in masks:
            mapping = projectors[mask] @ inverse @ core
            weight = float(
                np.trace(mapping.conj().T @ mapping).real / rank
            )
            if weight > 100 * tolerance:
                effect = mapping.conj().T @ mapping
                if np.linalg.norm(effect - weight * np.eye(rank), ord=2) > 100 * tolerance:
                    raise ValueError("active component does not define an isometric fiber")
                fiber_maps[mask] = mapping / math.sqrt(weight)
    active = tuple(sorted(fiber_maps))
    if len(active) < 2:
        raise ValueError("at least two active fibers are required")

    edge_polars: dict[tuple[int, int], np.ndarray] = {}
    edge_correlations: dict[tuple[int, int], float] = {}
    adjacency_lists: dict[int, list[int]] = {mask: [] for mask in active}
    identity = np.eye(rank)
    for source_index, source in enumerate(active):
        for target_mask in active[source_index + 1 :]:
            polar, singular_values = _polar_factor(
                projectors[target_mask] @ projectors[source],
                tolerance,
            )
            if not len(singular_values):
                continue
            image = polar @ fiber_maps[source]
            target_projection = (
                fiber_maps[target_mask] @ fiber_maps[target_mask].conj().T
            )
            leakage = float(
                np.linalg.norm(
                    (np.eye(dimension) - target_projection) @ image,
                    ord=2,
                )
            )
            isometry = float(
                np.linalg.norm(image.conj().T @ image - identity, ord=2)
            )
            if leakage > 100 * tolerance or isometry > 100 * tolerance:
                continue
            edge_polars[(source, target_mask)] = polar
            edge_polars[(target_mask, source)] = polar.conj().T
            fiber_cross = (
                fiber_maps[target_mask].conj().T
                @ projectors[target_mask]
                @ projectors[source]
                @ fiber_maps[source]
            )
            fiber_correlations = np.linalg.svd(
                fiber_cross,
                compute_uv=False,
            )
            correlation = float(np.min(fiber_correlations))
            edge_correlations[(source, target_mask)] = correlation
            edge_correlations[(target_mask, source)] = correlation
            adjacency_lists[source].append(target_mask)
            adjacency_lists[target_mask].append(source)
    adjacency = {
        mask: tuple(sorted(neighbors))
        for mask, neighbors in adjacency_lists.items()
    }

    path_rows = []
    unreachable = 0
    direct = 0
    two_edge = 0
    positive_signs = 0
    negative_signs = 0
    used_correlations = []
    for source in active:
        paths = _shortest_paths(adjacency, source)
        for target_mask in active:
            if source == target_mask:
                continue
            if target_mask not in paths:
                unreachable += 1
                continue
            path = paths[target_mask]
            operator = np.eye(dimension)
            for start, end in zip(path, path[1:]):
                operator = edge_polars[(start, end)] @ operator
                used_correlations.append(edge_correlations[(start, end)])
            image = operator @ fiber_maps[source]
            target_map = fiber_maps[target_mask]
            target_projection = target_map @ target_map.conj().T
            leakage = float(
                np.linalg.norm(
                    (np.eye(dimension) - target_projection) @ image,
                    ord=2,
                )
            )
            isometry = float(
                np.linalg.norm(image.conj().T @ image - identity, ord=2)
            )
            gauge = target_map.conj().T @ image
            positive_residual = float(np.linalg.norm(gauge - identity, ord=2))
            negative_residual = float(np.linalg.norm(gauge + identity, ord=2))
            sign_residual = min(positive_residual, negative_residual)
            positive_signs += positive_residual <= negative_residual
            negative_signs += negative_residual < positive_residual
            edge_count = len(path) - 1
            direct += edge_count == 1
            two_edge += edge_count == 2
            path_rows.append((edge_count, leakage, isometry, sign_residual))

    connected = unreachable == 0
    diameter = max((row[0] for row in path_rows), default=None)
    maximum_leakage = max((row[1] for row in path_rows), default=math.inf)
    maximum_isometry = max((row[2] for row in path_rows), default=math.inf)
    maximum_sign = max((row[3] for row in path_rows), default=math.inf)
    finite_correlation = bool(
        used_correlations and min(used_correlations) >= 1 / max(2, n)
    )
    verified = bool(
        connected
        and maximum_leakage <= 100 * tolerance
        and maximum_isometry <= 100 * tolerance
        and maximum_sign <= 100 * tolerance
    )
    return PairPolarTransportControl(
        control_id=control_id,
        n=n,
        target_partition=target,
        labels=labels,
        left_orientation_masks=left_masks,
        right_orientation_masks=right_masks,
        active_orientation_masks=active,
        intersection_dimension=rank,
        transport_graph_edge_count=sum(len(row) for row in adjacency.values()) // 2,
        transport_graph_connected=connected,
        transport_graph_diameter=diameter,
        minimum_used_edge_principal_correlation=(
            min(used_correlations) if used_correlations else None
        ),
        maximum_used_edge_principal_correlation=(
            max(used_correlations) if used_correlations else None
        ),
        maximum_path_fiber_range_leakage=maximum_leakage,
        maximum_path_fiber_isometry_residual=maximum_isometry,
        maximum_endpoint_scalar_sign_gauge_residual=maximum_sign,
        positive_sign_path_count=int(positive_signs),
        negative_sign_path_count=int(negative_signs),
        unreachable_ordered_fiber_pair_count=unreachable,
        direct_pair_transport_count=int(direct),
        two_edge_pair_transport_count=int(two_edge),
        exact_pair_polar_transport_network_verified=verified,
        finite_inverse_polynomial_correlation_control=finite_correlation,
        status=(
            "finite-pair-polar-transport-network-compiled"
            if verified and finite_correlation
            else "pair-polar-transport-network-validation-failure"
        ),
    )


def pair_polar_transport_scaling_record(n: int) -> PairPolarTransportScalingRecord:
    if n < 5:
        raise ValueError("the all-n symmetric-group dimension bound starts at n=5")
    copies = math.ceil(math.lgamma(n + 1) / math.log(2))
    return PairPolarTransportScalingRecord(
        n=n,
        information_threshold_copy_count=copies,
        noncommon_pair_correlation_form="1/d_alpha",
        smallest_possible_nonzero_pair_correlation_log2_lower_bound=(
            -0.5 * math.lgamma(n + 1) / math.log(2)
        ),
        smallest_possible_nonzero_pair_correlation_can_be_exponential=True,
        polynomial_transport_graph_diameter_proved=False,
        inverse_polynomial_used_edge_correlation_proved=False,
        gpe_direct_pair_polar_bypasses_edge_correlation=True,
        polynomial_coherent_path_finder_proved=False,
        efficiently_correctable_internal_gauge_proved=False,
        hierarchical_orientation_polar_proved=False,
        status="gpe-edge-polar-polynomial-path-and-holonomy-open",
    )


def run_pair_polar_transport_network() -> PairPolarTransportNetworkReport:
    distinct: tuple[Label, ...] = (
        ((3,), (2, 1)),
        ((3,), (1, 1, 1)),
        ((2, 1), (1, 1, 1)),
    )
    controls = [
        audit_pair_polar_transport_network(
            "W3-DISTINCT-AFFINE-PLANE",
            3,
            (2, 1),
            distinct,
            (0, 2),
            (5, 7),
        ),
        audit_pair_polar_transport_network(
            "W3-DISTINCT-SCALED-AFFINE-PLANE",
            3,
            (2, 1),
            distinct,
            (0, 5),
            (2, 7),
        ),
        audit_pair_polar_transport_network(
            "W5-ISOLATED-ANCHOR-LINE",
            5,
            (3, 2),
            _w5_probe_labels()[0],
            (0, 1, 2, 3),
            (4, 5, 6, 7),
        ),
    ]
    scaling = [
        pair_polar_transport_scaling_record(n)
        for n in (5, 8, 16, 32, 64, 128, 256, 512)
    ]
    failures = sum(
        not row.exact_pair_polar_transport_network_verified for row in controls
    )
    finite_correlation_failures = sum(
        not row.finite_inverse_polynomial_correlation_control for row in controls
    )
    w3 = controls[:2]
    w5 = controls[2]
    verified = failures == 0 and finite_correlation_failures == 0
    return PairPolarTransportNetworkReport(
        created_at=utc_now(),
        theorem_contract={
            "edge_transport": (
                "The polar factor of E_jE_i transports the relevant fiber when "
                "that fiber occupies a nonzero principal-angle block."
            ),
            "path_transport": (
                "Products of edge polars transport along graph paths; endpoint "
                "gauges must be computed and corrected coherently."
            ),
            "finite_network": (
                "The W3 active graph is K_(2,2) with diameter two and sign-only "
                "gauges; the W5 anchor line is one common-range edge."
            ),
            "conditioning_boundary": (
                "Generic normalized-access QSVT costs inverse in correlation "
                "1/d_alpha, but the companion coherent-GPE construction "
                "implements the pair polar directly and bypasses that scalar."
            ),
            "all_n_target": (
                "Find a polynomial coherent path/generator selector with "
                "nonnegligible active-fiber coverage and efficiently resolvable "
                "gauge/holonomy."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "finite_affine_fiber_pair_transport",
                "resolved": verified,
                "resolution": (
                    "Every active-fiber pair in the finite controls has an exact "
                    "path of length at most two with correlation at least 1/2."
                ),
            },
            {
                "obligation": "all_n_polynomial_transport_diameter",
                "resolved": False,
                "resolution": (
                    "No representation theorem controls connectivity or diameter "
                    "of the active pair-overlap graph at growing copy count."
                ),
            },
            {
                "obligation": "audit_normalized_qsvt_edge_correlation",
                "resolved": True,
                "resolution": (
                    "Pair correlations are 1/d_alpha and natural S_n dimensions "
                    "can be exponential. This remains a normalized-QSVT fact but "
                    "is not required by the direct GPE pair polar."
                ),
            },
            {
                "obligation": "coherent_transport_path_and_gauge_compiler",
                "resolved": False,
                "resolution": (
                    "The finite BFS and sign gauges are classical witnesses, not "
                    "a uniform coherent path finder for exponentially many masks."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "The constant-conditioned pair sampler compiles pair polar transport.",
                "resolved": True,
                "resolution": (
                    "The stacked sampler inverts singular values near one, while "
                    "transport polarizes E_jE_i. The stacked sampler does not "
                    "compile it, but the separate coherent-GPE circuit does."
                ),
            },
            {
                "objection": "Orthogonal affine-generator fibers make W3 transport impossible.",
                "resolved": True,
                "resolution": (
                    "Each orthogonal generator pair has an exact two-edge path "
                    "through the opposite bipartition."
                ),
            },
            {
                "objection": "Finite diameter two suggests constant asymptotic diameter.",
                "resolved": False,
                "resolution": (
                    "The W3 graph is a fixed low-dimensional control and gives no "
                    "growing representation-graph expansion theorem."
                ),
            },
            {
                "objection": "Endpoint gauges are always scalar signs.",
                "resolved": False,
                "resolution": (
                    "Higher multiplicity fibers can carry nonabelian holonomy; no "
                    "all-n scalar-gauge theorem exists."
                ),
            },
        ],
        headline_metrics={
            "finite_pair_polar_transport_network_count": len(controls) - failures,
            "finite_transport_validation_failure_count": failures,
            "finite_qsvt_correlation_control_failure_count": finite_correlation_failures,
            "maximum_finite_transport_graph_diameter": max(
                row.transport_graph_diameter or 0 for row in controls
            ),
            "minimum_finite_used_edge_correlation": min(
                row.minimum_used_edge_principal_correlation or 0.0
                for row in controls
            ),
            "w3_two_edge_transport_count": sum(
                row.two_edge_pair_transport_count for row in w3
            ),
            "w3_negative_sign_gauge_path_count": sum(
                row.negative_sign_path_count for row in w3
            ),
            "w5_common_range_direct_transport_count": (
                w5.direct_pair_transport_count
            ),
            "all_n_polynomial_transport_diameter_theorem_count": 0,
            "all_n_inverse_polynomial_transport_correlation_theorem_count": 0,
            "gpe_direct_pair_correlation_bypass_theorem_count": 1,
            "coherent_transport_path_compiler_count": 0,
            "hierarchical_orientation_polar_sampler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "finite_affine_fiber_pair_transport_compiled": verified,
            "w3_orthogonal_generator_transport_resolved_by_two_edges": all(
                row.transport_graph_diameter == 2 for row in w3
            ),
            "w5_anchor_transport_is_direct_common_range": (
                w5.transport_graph_diameter == 1
            ),
            "all_n_polynomial_transport_graph_diameter_proved": False,
            "all_n_inverse_polynomial_used_edge_correlation_proved": False,
            "gpe_direct_pair_polar_bypasses_edge_correlation": True,
            "polynomial_coherent_path_finder_proved": False,
            "efficient_internal_gauge_correction_proved": False,
            "hierarchical_orientation_polar_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Finite fibers have short pair-polar paths and GPE removes the "
                "inverse-correlation cost, but no all-n coherent path, active-"
                "coverage, or holonomy resolver is known."
            ),
        },
        status=(
            "finite-pair-polar-transports-gpe-edge-bypass-path-holonomy-open"
            if verified
            else "pair-polar-transport-network-validation-failure"
        ),
        summary=(
            "Compiled all finite affine fiber transports through paths of at most "
            "two pair polars; coherent GPE removes the edge-correlation barrier, "
            "leaving path selection, coverage, and holonomy."
        ),
        falsifiers_triggered=[
            (
                "Direct affine-generator overlap is not necessary; a short pair-"
                "overlap path can transport the fiber."
            ),
            (
                "The stacked pair sampler does not compile pair-overlap transport, "
                "but coherent GPE implements that polar without inverse-dimension "
                "amplification."
            ),
            (
                "Fixed W3 diameter and sign gauges do not imply polynomial "
                "diameter or abelian gauges at growing multiplicity."
            ),
        ],
    )


def write_pair_polar_transport_network_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-PAIR-POLAR-TRANSPORT-NETWORK"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_pair_polar_transport_network())
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
                id="NEG-SELF-DUAL-WREATH-PAIR-POLAR-TRANSPORT-NETWORK",
                source=registry_experiment_id,
                claim=(
                    "Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-PAIR-POLAR-TRANSPORT-NETWORK."
                ),
                reason_invalid=(
                    "Falsified or refined by exact theorem evaluation."
                ),
                lesson=(
                    "Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-PAIR-POLAR-TRANSPORT-NETWORK."
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
                    "self_dual_wreath_pair_polar_transport_network": str(path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_pair_polar_transport_network_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
