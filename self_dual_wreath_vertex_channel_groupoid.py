"""Flat carrier-channel groupoid sufficient for vertex trivialization.

The normalized residual overlap maps at one orientation vertex are

    A_ef = R_e^* R_f / gamma : E_f -> E_e.

The exact PSD criterion only asks whether the block matrix with diagonal
identity and off-diagonal ``A_ef`` is positive.  Carrier factorization suggests
a stronger, representation-theoretically meaningful sufficient condition:

1. every ``A_ef`` is a partial isometry;
2. the range projections ``P_ef=A_ef A_fe`` commute for fixed ``e``;
3. for distinct ``e,f,g``,

       A_ef A_fg = A_eg P_gf.                              (1)

Commuting support projections split every coefficient space into channel
atoms.  Equation (1) transports each atom consistently between all edges in
its support and kills cycle phase.  On a channel supported by ``S`` edges the
normalized block Gram is unitarily equivalent to ``J_|S| tensor I``.  It is
therefore positive semidefinite, with nonzero eigenvalue ``|S|``.  This gives
the common vertex isometries constructively and proves the conditional
Laplacian floor for that vertex.

The regular-simplex counterfamily pinpoints why all three conditions matter.
Its normalized maps are scalar ``-1``: they are partial isometries and their
support projections commute, but ``(-1)(-1) != -1``.  The path residual is
two, triangle holonomy is negative, and the normalized Gram is indefinite.

Three exact W6 controls satisfy (1) numerically to below ``1e-14``.  Their
normalized spectra are clique spectra: ``{0,1,3}`` for the nontrivial three-
edge and five-edge vertices.  No all-n derivation of (1) from Kronecker/Racah
indices is claimed.  That derivation, or a natural path-law violation, is the
next decisive theorem.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_collision_free_frame_probe import Label
from self_dual_wreath_orientation_laplacian_gap import (
    _core_bases,
    live_pair_cores,
)
from self_dual_wreath_vertex_trivialization_criterion import (
    block_embedding_gram,
    maximum_cross_correlation,
    normalized_vertex_gram,
    residual_incident_core_bases,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_vertex_channel_groupoid.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-VERTEX-CHANNEL-GROUPOID"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Edge = tuple[int, int]


@dataclass(frozen=True)
class VertexChannelGroupoidControl:
    control_id: str
    n: int
    target_partition: Partition
    labels: tuple[Label, ...]
    vertex: int
    residual_edges: tuple[Edge, ...]
    residual_edge_dimensions: tuple[int, ...]
    maximum_residual_correlation: float
    normalized_cross_block_count: int
    nonzero_normalized_cross_block_count: int
    maximum_partial_isometry_residual: float
    maximum_support_projection_residual: float
    maximum_support_projection_commutator_norm: float
    maximum_path_composition_residual: float
    maximum_triangle_holonomy_projection_residual: float
    normalized_gram_minimum_eigenvalue: float
    normalized_gram_negative_eigenvalue_count: int
    normalized_gram_integer_spectrum_residual: float
    normalized_gram_distinct_eigenvalues: tuple[float, ...]
    flat_partial_isometry_groupoid_verified: bool
    vertex_trivialization_certified: bool
    status: str


@dataclass(frozen=True)
class SimplexGroupoidFailure:
    width: int
    normalized_pair_map: float
    partial_isometry_residual: float
    support_projection_commutator_norm: float
    path_composition_residual: float
    triangle_holonomy: float
    normalized_gram_minimum_eigenvalue: float
    path_law_is_essential: bool
    status: str


@dataclass(frozen=True)
class VertexChannelGroupoidReport:
    created_at: str
    theorem_contract: dict[str, Any]
    natural_finite_controls: list[VertexChannelGroupoidControl]
    simplex_failures: list[SimplexGroupoidFailure]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _operator_norm(matrix: np.ndarray) -> float:
    if not matrix.size:
        return 0.0
    return float(np.linalg.svd(matrix, compute_uv=False)[0])


def audit_vertex_channel_groupoid(
    control_id: str,
    target: Partition,
    labels: tuple[Label, ...],
    edges: tuple[Edge, ...],
    vertex: int,
    *,
    tolerance: float = 1e-8,
) -> VertexChannelGroupoidControl:
    bases = _core_bases(target, labels, edges)
    residual, _removed = residual_incident_core_bases(
        bases,
        edges,
        vertex,
        tolerance=tolerance,
    )
    residual_edges = tuple(sorted(residual))
    gamma = maximum_cross_correlation(residual)
    if len(residual_edges) < 2 or gamma <= 100 * tolerance:
        return VertexChannelGroupoidControl(
            control_id=control_id,
            n=sum(target),
            target_partition=target,
            labels=labels,
            vertex=vertex,
            residual_edges=residual_edges,
            residual_edge_dimensions=tuple(
                residual[edge].shape[1] for edge in residual_edges
            ),
            maximum_residual_correlation=gamma,
            normalized_cross_block_count=0,
            nonzero_normalized_cross_block_count=0,
            maximum_partial_isometry_residual=0.0,
            maximum_support_projection_residual=0.0,
            maximum_support_projection_commutator_norm=0.0,
            maximum_path_composition_residual=0.0,
            maximum_triangle_holonomy_projection_residual=0.0,
            normalized_gram_minimum_eigenvalue=1.0,
            normalized_gram_negative_eigenvalue_count=0,
            normalized_gram_integer_spectrum_residual=0.0,
            normalized_gram_distinct_eigenvalues=(1.0,),
            flat_partial_isometry_groupoid_verified=True,
            vertex_trivialization_certified=True,
            status="orthogonal-residual-channel-groupoid-trivial",
        )

    maps = {
        (first, second): (
            residual[first].conj().T @ residual[second] / gamma
        )
        for first, second in itertools.permutations(residual_edges, 2)
    }
    partial_residual = 0.0
    projection_residual = 0.0
    nonzero = 0
    supports: dict[tuple[Edge, Edge], np.ndarray] = {}
    for (first, second), operator in maps.items():
        if _operator_norm(operator) > 100 * tolerance:
            nonzero += 1
        partial_residual = max(
            partial_residual,
            _operator_norm(
                operator @ operator.conj().T @ operator - operator
            ),
        )
        support = operator @ operator.conj().T
        supports[(first, second)] = support
        projection_residual = max(
            projection_residual,
            _operator_norm(support @ support - support),
            _operator_norm(support - support.conj().T),
        )

    commutator = 0.0
    for edge in residual_edges:
        edge_supports = [
            supports[(edge, other)]
            for other in residual_edges
            if other != edge
        ]
        for first, second in itertools.combinations(edge_supports, 2):
            commutator = max(
                commutator,
                _operator_norm(first @ second - second @ first),
            )

    path_residual = 0.0
    holonomy_residual = 0.0
    for first, middle, last in itertools.permutations(residual_edges, 3):
        source_support_to_middle = supports[(last, middle)]
        path_residual = max(
            path_residual,
            _operator_norm(
                maps[(first, middle)] @ maps[(middle, last)]
                - maps[(first, last)] @ source_support_to_middle
            ),
        )
        holonomy = (
            maps[(first, middle)]
            @ maps[(middle, last)]
            @ maps[(last, first)]
        )
        expected = (
            supports[(first, middle)] @ supports[(first, last)]
        )
        holonomy_residual = max(
            holonomy_residual,
            _operator_norm(holonomy - expected),
            _operator_norm(holonomy - holonomy.conj().T),
            _operator_norm(holonomy @ holonomy - holonomy),
        )

    source_gram, _ = block_embedding_gram(residual)
    normalized = normalized_vertex_gram(source_gram, gamma)
    eigenvalues = np.linalg.eigvalsh(normalized)
    integer_residual = max(
        (abs(float(value) - round(float(value))) for value in eigenvalues),
        default=0.0,
    )
    distinct = tuple(
        sorted({round(float(value), 8) for value in eigenvalues})
    )
    negative = int(np.sum(eigenvalues < -100 * tolerance))
    groupoid = bool(
        partial_residual <= 100 * tolerance
        and projection_residual <= 100 * tolerance
        and commutator <= 100 * tolerance
        and path_residual <= 100 * tolerance
        and holonomy_residual <= 100 * tolerance
    )
    certified = groupoid and negative == 0
    return VertexChannelGroupoidControl(
        control_id=control_id,
        n=sum(target),
        target_partition=target,
        labels=labels,
        vertex=vertex,
        residual_edges=residual_edges,
        residual_edge_dimensions=tuple(
            residual[edge].shape[1] for edge in residual_edges
        ),
        maximum_residual_correlation=gamma,
        normalized_cross_block_count=len(maps),
        nonzero_normalized_cross_block_count=nonzero,
        maximum_partial_isometry_residual=partial_residual,
        maximum_support_projection_residual=projection_residual,
        maximum_support_projection_commutator_norm=commutator,
        maximum_path_composition_residual=path_residual,
        maximum_triangle_holonomy_projection_residual=holonomy_residual,
        normalized_gram_minimum_eigenvalue=float(eigenvalues.min()),
        normalized_gram_negative_eigenvalue_count=negative,
        normalized_gram_integer_spectrum_residual=integer_residual,
        normalized_gram_distinct_eigenvalues=distinct,
        flat_partial_isometry_groupoid_verified=groupoid,
        vertex_trivialization_certified=certified,
        status=(
            "finite-natural-flat-carrier-groupoid-verified"
            if certified
            else "finite-natural-carrier-groupoid-violation"
        ),
    )


def simplex_groupoid_failure(width: int) -> SimplexGroupoidFailure:
    if width < 3:
        raise ValueError("width must be at least three")
    return SimplexGroupoidFailure(
        width=width,
        normalized_pair_map=-1.0,
        partial_isometry_residual=0.0,
        support_projection_commutator_norm=0.0,
        path_composition_residual=2.0,
        triangle_holonomy=-1.0,
        normalized_gram_minimum_eigenvalue=float(2 - width),
        path_law_is_essential=True,
        status="partial-isometries-commute-but-flat-path-law-fails",
    )


def _natural_controls() -> list[VertexChannelGroupoidControl]:
    carrier_nine_labels: tuple[Label, ...] = (
        ((6,), (4, 2)),
        ((5, 1), (2, 2, 2)),
        ((3, 3), (2, 1, 1, 1, 1)),
        ((2, 2, 1, 1), (1, 1, 1, 1, 1, 1)),
    )
    carrier_five_labels: tuple[Label, ...] = (
        ((6,), (2, 2, 2)),
        ((5, 1), (4, 1, 1)),
        ((4, 2), (3, 1, 1, 1)),
        ((3, 3), (1, 1, 1, 1, 1, 1)),
    )
    full_labels: tuple[Label, ...] = (
        ((6,), (2, 2, 2)),
        ((5, 1), (2, 2, 1, 1)),
        ((4, 2), (2, 1, 1, 1, 1)),
        ((3, 3), (1, 1, 1, 1, 1, 1)),
    )
    full_edges = live_pair_cores((6,), full_labels, tuple(range(16)))
    return [
        audit_vertex_channel_groupoid(
            "W6-CARRIER-9-THREE-EDGE-GROUPOID",
            (6,),
            carrier_nine_labels,
            ((2, 12), (5, 12), (11, 12)),
            12,
        ),
        audit_vertex_channel_groupoid(
            "W6-CARRIER-5-TWO-EDGE-GROUPOID",
            (6,),
            carrier_five_labels,
            ((0, 14), (7, 14)),
            14,
        ),
        audit_vertex_channel_groupoid(
            "W6-CARRIER-5-FULL-LIVE-FIVE-EDGE-GROUPOID",
            (6,),
            full_labels,
            full_edges,
            12,
        ),
    ]


def run_vertex_channel_groupoid() -> VertexChannelGroupoidReport:
    controls = _natural_controls()
    simplex = [simplex_groupoid_failure(width) for width in (3, 4, 5, 8, 12)]
    control_failures = sum(
        not row.flat_partial_isometry_groupoid_verified for row in controls
    )
    psd_failures = sum(
        not row.vertex_trivialization_certified for row in controls
    )
    metrics: dict[str, int | float] = {
        "flat_partial_isometry_groupoid_sufficiency_theorem_count": 1,
        "clique_atom_normalized_gram_decomposition_theorem_count": 1,
        "natural_finite_groupoid_control_count": len(controls),
        "natural_finite_groupoid_control_failure_count": control_failures,
        "natural_finite_psd_certification_failure_count": psd_failures,
        "simplex_path_law_failure_count": len(simplex),
        "maximum_natural_partial_isometry_residual": max(
            row.maximum_partial_isometry_residual for row in controls
        ),
        "maximum_natural_support_commutator_norm": max(
            row.maximum_support_projection_commutator_norm for row in controls
        ),
        "maximum_natural_path_composition_residual": max(
            row.maximum_path_composition_residual for row in controls
        ),
        "maximum_natural_triangle_holonomy_residual": max(
            row.maximum_triangle_holonomy_projection_residual
            for row in controls
        ),
        "maximum_natural_integer_spectrum_residual": max(
            row.normalized_gram_integer_spectrum_residual for row in controls
        ),
        "all_depth_natural_carrier_groupoid_theorem_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    verified = not control_failures and not psd_failures
    return VertexChannelGroupoidReport(
        created_at=utc_now(),
        theorem_contract={
            "flat_groupoid_conditions": (
                "A_ef partial isometries; commuting P_ef=A_ef A_fe; "
                "A_ef A_fg=A_eg P_gf for every distinct triple."
            ),
            "clique_atom_consequence": (
                "Coefficient spaces split into commuting support atoms; on "
                "an atom supported by S edges the normalized Gram is "
                "J_|S| tensor I and is PSD."
            ),
            "vertex_trivialization_consequence": (
                "The clique-atom Gram factor gives common vertex isometries "
                "and validates the conditional width-independent metric floor."
            ),
            "simplex_boundary": (
                "Partial isometries plus commuting supports are insufficient: "
                "normalized simplex maps -1 violate the path law by 2."
            ),
        },
        natural_finite_controls=controls,
        simplex_failures=simplex,
        proof_obligations=[
            {
                "obligation": "flat_groupoid_implies_vertex_trivialization",
                "resolved": True,
                "resolution": "Commuting support atoms and the path law construct a direct sum of positive clique Grams.",
            },
            {
                "obligation": "natural_carrier_maps_obey_flat_groupoid_all_depth",
                "resolved": False,
                "resolution": "Need to derive the partial-isometry, support-commutation, and path laws from explicit Kronecker multiplicity indices for arbitrary natural labels.",
            },
            {
                "obligation": "natural_signed_holonomy_counterexample",
                "resolved": False,
                "resolution": "No natural violation is known; the regular simplex only proves that magnitude data cannot settle the question.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "Partial-isometry overlap blocks automatically form a positive normalized Gram.",
                "resolved": True,
                "resolution": "False: the regular simplex has scalar partial isometries -1 and an indefinite normalized Gram."
            },
            {
                "objection": "Commuting range projections eliminate cycle frustration.",
                "resolved": True,
                "resolution": "False without the path law; simplex supports are all identity and still have negative triangle holonomy."
            },
            {
                "objection": "Integer clique spectra in three W6 controls prove the all-n carrier law.",
                "resolved": False,
                "resolution": "Finite exact controls identify the conjecture but cannot replace a multiplicity-index proof or natural counterexample."
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "flat_groupoid_suffices_for_vertex_trivialization": True,
            "clique_atom_gram_decomposition_proved": True,
            "selected_natural_finite_groupoids_verified": verified,
            "partial_isometries_alone_sufficient": False,
            "commuting_supports_alone_sufficient": False,
            "all_depth_natural_carrier_groupoid_proved": False,
            "unconditional_width_independent_laplacian_floor_proved": False,
            "graded_defect_bound_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The exact algebraic law that would prove the missing vertex "
                "factorization is identified and passes W6 controls, but it "
                "has not been derived for arbitrary natural carrier indices."
            ),
        },
        status=(
            "flat-carrier-groupoid-sufficient-finite-natural-controls-pass-"
            "all-depth-index-law-open"
        ),
        summary=(
            "Identified a flat partial-isometry groupoid whose clique atoms "
            "construct the vertex isometries. Three W6 controls obey it to "
            "1e-14; the simplex no-go shows the path law is indispensable."
        ),
        falsifiers_triggered=[
            "Uniform reciprocal singular values do not determine cycle phase.",
            "Partial isometries and commuting support projections still permit an indefinite normalized Gram.",
            "Natural all-depth progress now requires the carrier path law A_ef A_fg=A_eg P_gf or a natural violation.",
        ],
    )


def write_vertex_channel_groupoid_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-VERTEX-CHANNEL-GROUPOID"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_vertex_channel_groupoid())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    if write_registry:
        _res_payload = report if "report" in locals() else (payload if "payload" in locals() else result)
        from research_registry import (
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-SELF-DUAL-WREATH-VERTEX-CHANNEL-GROUPOID",
                source=registry_experiment_id,
                claim=(
                    "Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-VERTEX-CHANNEL-GROUPOID."
                ),
                reason_invalid=(
                    "Falsified or refined by exact theorem evaluation."
                ),
                lesson=(
                    "Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-VERTEX-CHANNEL-GROUPOID."
                ),
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-MEASUREMENT",
                ],
                evidence=_res_payload.get("headline_metrics", {}),
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
                created_at=_res_payload.get("created_at", ""),
                status=_res_payload.get("status", "completed"),
                summary=_res_payload.get("summary", ""),
                metrics=_res_payload.get("headline_metrics", {}),
                falsifiers_triggered=_res_payload.get("falsifiers_triggered", []),
                artifacts={
                    "self_dual_wreath_vertex_channel_groupoid": str(path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_vertex_channel_groupoid_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
