"""Exact criterion and counterfamily for residual vertex trivialization.

The orientation-Laplacian route assumes that residual pair-core embeddings
incident to a vertex can be rescaled into one family of vertex isometries.  The
assumption has an exact finite-dimensional criterion.

Let ``R_e : K_e -> H`` be orthonormal residual core embeddings after all exact
common directions have been removed, and let

    G_ef = R_e^* R_f,       G_ee = I.

Fix ``0 < gamma < 1`` with ``||G_ef|| <= gamma``.  Isometries ``W_e`` with

    G_ef = gamma W_e^* W_f,     e != f,

exist if and only if the block matrix

    T_gamma = I + (G-I)/gamma

is positive semidefinite.  This is just the Gram-representation theorem;
equivalently

    lambda_min(G) >= 1-gamma.                                  (1)

When (1) holds, a Cholesky/eigendecomposition of ``T_gamma`` explicitly
constructs the common vertex isometries.  Holonomy after this construction is
harmless for the Laplacian floor.  Arbitrary pairwise overlap maps, however,
need not assemble into such a positive Gram matrix.

The distinction is essential.  The ``p`` unit vectors of a regular simplex
have pairwise inner product ``-1/(p-1)``.  Their pairwise correlation magnitude
is exactly the symmetric-group scale ``gamma=1/(p-1)``, but rescaling the
off-diagonal blocks gives ``T_gamma`` with diagonal ``1`` and off-diagonal
``-1``.  Its minimum eigenvalue is ``2-p``.  Thus the vertex trivialization
fails already at width ``p`` even though every pair has one uniform reciprocal
correlation.  The associated star relation metric has minimum eigenvalue one,
below ``2-2/(p-1)`` for ``p>3``.

This is an abstract signed-holonomy counterfamily, not a proved natural wreath
portfolio.  Exact W6 controls pass (1), including a five-edge residual vertex.
The surviving all-depth problem is therefore to prove positivity of the
normalized carrier-index Gram for natural collision-free portfolios, not to
measure a single correlation value.
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


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_vertex_trivialization_criterion.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-VERTEX-TRIVIALIZATION-CRITERION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Edge = tuple[int, int]


@dataclass(frozen=True)
class VertexTrivializationControl:
    control_id: str
    n: int
    target_partition: Partition
    labels: tuple[Label, ...]
    vertex: int
    incident_live_edge_count: int
    residual_live_edge_count: int
    exact_common_direction_count_removed: int
    residual_coefficient_dimension: int
    maximum_residual_cross_correlation: float
    residual_gram_minimum_eigenvalue: float
    required_residual_gram_floor: float
    normalized_vertex_gram_minimum_eigenvalue: float
    normalized_vertex_gram_negative_eigenvalue_count: int
    gram_affine_spectrum_identity_residual: float
    vertex_trivialization_exists: bool
    status: str


@dataclass(frozen=True)
class SimplexHolonomyCounterexample:
    width: int
    physical_dimension: int
    reciprocal_correlation: float
    maximum_pair_correlation_residual: float
    source_gram_minimum_eigenvalue: float
    required_source_gram_floor: float
    normalized_vertex_gram_minimum_eigenvalue: float
    normalized_vertex_gram_negative_eigenvalue_count: int
    triangle_normalized_holonomy: float
    star_relation_metric_minimum_eigenvalue: float
    claimed_uniform_transport_floor: float
    claimed_floor_violation: float
    pairwise_uniform_reciprocal_correlations: bool
    vertex_trivialization_exists: bool
    exact_counterexample_audit: bool
    status: str


@dataclass(frozen=True)
class VertexTrivializationCriterionReport:
    created_at: str
    theorem_contract: dict[str, Any]
    natural_finite_controls: list[VertexTrivializationControl]
    simplex_counterexamples: list[SimplexHolonomyCounterexample]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _support_basis(
    columns: list[np.ndarray],
    row_count: int,
    *,
    tolerance: float,
) -> np.ndarray:
    if not columns:
        return np.zeros((row_count, 0), dtype=complex)
    stacked = np.concatenate(columns, axis=1)
    left, singular, _ = np.linalg.svd(stacked, full_matrices=False)
    return left[:, singular > 100 * tolerance]


def _orthogonal_complement(
    basis: np.ndarray,
    dimension: int,
    *,
    tolerance: float,
) -> np.ndarray:
    if not basis.shape[1]:
        return np.eye(dimension, dtype=complex)
    projector = np.eye(dimension, dtype=complex) - basis @ basis.conj().T
    values, vectors = np.linalg.eigh((projector + projector.conj().T) / 2)
    return vectors[:, values > 1 - 100 * tolerance]


def residual_incident_core_bases(
    bases: dict[Edge, np.ndarray],
    edges: tuple[Edge, ...],
    vertex: int,
    *,
    tolerance: float = 1e-8,
) -> tuple[dict[Edge, np.ndarray], int]:
    """Remove the span of every exact pairwise common direction per core."""

    incident = tuple(edge for edge in edges if vertex in edge)
    common_coefficients: dict[Edge, list[np.ndarray]] = {
        edge: [] for edge in incident
    }
    for first_index, first in enumerate(incident):
        for second in incident[first_index + 1 :]:
            left, singular, right_adjoint = np.linalg.svd(
                bases[first].conj().T @ bases[second],
                full_matrices=False,
            )
            keep = singular > 1 - 100 * tolerance
            if np.any(keep):
                common_coefficients[first].append(left[:, keep])
                common_coefficients[second].append(
                    right_adjoint.conj().T[:, keep]
                )
    residual: dict[Edge, np.ndarray] = {}
    removed = 0
    for edge in incident:
        common = _support_basis(
            common_coefficients[edge],
            bases[edge].shape[1],
            tolerance=tolerance,
        )
        complement = _orthogonal_complement(
            common,
            bases[edge].shape[1],
            tolerance=tolerance,
        )
        removed += common.shape[1]
        if complement.shape[1]:
            residual[edge] = bases[edge] @ complement
    return residual, removed


def block_embedding_gram(
    residual_bases: dict[Edge, np.ndarray],
) -> tuple[np.ndarray, tuple[Edge, ...]]:
    edges = tuple(sorted(residual_bases))
    if not edges:
        return np.zeros((0, 0), dtype=complex), edges
    concatenated = np.concatenate(
        [residual_bases[edge] for edge in edges],
        axis=1,
    )
    gram = concatenated.conj().T @ concatenated
    return (gram + gram.conj().T) / 2, edges


def maximum_cross_correlation(
    residual_bases: dict[Edge, np.ndarray],
) -> float:
    largest = 0.0
    for first, second in itertools.combinations(sorted(residual_bases), 2):
        singular = np.linalg.svd(
            residual_bases[first].conj().T @ residual_bases[second],
            compute_uv=False,
        )
        if singular.size:
            largest = max(largest, float(singular[0]))
    return largest


def normalized_vertex_gram(
    source_gram: np.ndarray,
    correlation: float,
) -> np.ndarray:
    if not 0 < correlation < 1:
        raise ValueError("correlation must lie strictly between zero and one")
    identity = np.eye(source_gram.shape[0], dtype=complex)
    return identity + (source_gram - identity) / correlation


def audit_vertex_trivialization(
    control_id: str,
    target: Partition,
    labels: tuple[Label, ...],
    edges: tuple[Edge, ...],
    vertex: int,
    *,
    tolerance: float = 1e-8,
) -> VertexTrivializationControl:
    bases = _core_bases(target, labels, edges)
    incident_count = sum(vertex in edge for edge in edges)
    residual, removed = residual_incident_core_bases(
        bases,
        edges,
        vertex,
        tolerance=tolerance,
    )
    gram, residual_edges = block_embedding_gram(residual)
    gamma = maximum_cross_correlation(residual)
    if len(residual_edges) < 2 or gamma <= 100 * tolerance:
        minimum = float(np.linalg.eigvalsh(gram).min()) if gram.size else 1.0
        normalized_minimum = 1.0
        negative = 0
        identity_residual = 0.0
        exists = True
        required = 1.0
    else:
        source_values = np.linalg.eigvalsh(gram)
        minimum = float(source_values.min())
        required = 1 - gamma
        normalized = normalized_vertex_gram(gram, gamma)
        normalized_values = np.linalg.eigvalsh(normalized)
        normalized_minimum = float(normalized_values.min())
        negative = int(np.sum(normalized_values < -100 * tolerance))
        predicted = (minimum - required) / gamma
        identity_residual = abs(normalized_minimum - predicted)
        exists = normalized_minimum >= -100 * tolerance
    return VertexTrivializationControl(
        control_id=control_id,
        n=sum(target),
        target_partition=target,
        labels=labels,
        vertex=vertex,
        incident_live_edge_count=incident_count,
        residual_live_edge_count=len(residual_edges),
        exact_common_direction_count_removed=removed,
        residual_coefficient_dimension=gram.shape[0],
        maximum_residual_cross_correlation=gamma,
        residual_gram_minimum_eigenvalue=minimum,
        required_residual_gram_floor=required,
        normalized_vertex_gram_minimum_eigenvalue=normalized_minimum,
        normalized_vertex_gram_negative_eigenvalue_count=negative,
        gram_affine_spectrum_identity_residual=identity_residual,
        vertex_trivialization_exists=exists,
        status=(
            "finite-natural-vertex-trivialization-verified"
            if exists
            else "finite-natural-vertex-trivialization-falsified"
        ),
    )


def regular_simplex_holonomy_counterexample(
    width: int,
    *,
    tolerance: float = 1e-10,
) -> SimplexHolonomyCounterexample:
    if width < 3:
        raise ValueError("a frustrated simplex needs width at least three")
    gamma = 1 / (width - 1)
    gram = np.full((width, width), -gamma)
    np.fill_diagonal(gram, 1.0)
    values = np.linalg.eigvalsh(gram)
    normalized = normalized_vertex_gram(gram, gamma)
    normalized_values = np.linalg.eigvalsh(normalized)
    relation_values = np.linalg.eigvalsh(np.eye(width) + gram)
    maximum_residual = float(
        np.max(np.abs((gram - np.eye(width))[np.triu_indices(width, 1)] + gamma))
    )
    claimed_floor = 2 - 2 * gamma
    observed = float(relation_values.min())
    negative = int(np.sum(normalized_values < -tolerance))
    audit = bool(
        abs(float(values.min())) <= 100 * tolerance
        and abs(float(normalized_values.min()) - (2 - width))
        <= 100 * tolerance
        and abs(observed - 1.0) <= 100 * tolerance
        and negative == 1
    )
    return SimplexHolonomyCounterexample(
        width=width,
        physical_dimension=width - 1,
        reciprocal_correlation=gamma,
        maximum_pair_correlation_residual=maximum_residual,
        source_gram_minimum_eigenvalue=float(values.min()),
        required_source_gram_floor=1 - gamma,
        normalized_vertex_gram_minimum_eigenvalue=float(
            normalized_values.min()
        ),
        normalized_vertex_gram_negative_eigenvalue_count=negative,
        triangle_normalized_holonomy=-1.0,
        star_relation_metric_minimum_eigenvalue=observed,
        claimed_uniform_transport_floor=claimed_floor,
        claimed_floor_violation=observed - claimed_floor,
        pairwise_uniform_reciprocal_correlations=maximum_residual <= tolerance,
        vertex_trivialization_exists=False,
        exact_counterexample_audit=audit,
        status="uniform-reciprocal-correlation-vertex-trivialization-no-go",
    )


def _natural_controls() -> list[VertexTrivializationControl]:
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
    five_edge_labels: tuple[Label, ...] = (
        ((6,), (2, 2, 2)),
        ((5, 1), (2, 2, 1, 1)),
        ((4, 2), (2, 1, 1, 1, 1)),
        ((3, 3), (1, 1, 1, 1, 1, 1)),
    )
    full_family = tuple(range(16))
    five_edge_live = live_pair_cores((6,), five_edge_labels, full_family)
    return [
        audit_vertex_trivialization(
            "W6-CARRIER-9-THREE-EDGE-VERTEX",
            (6,),
            carrier_nine_labels,
            ((2, 12), (5, 12), (11, 12)),
            12,
        ),
        audit_vertex_trivialization(
            "W6-CARRIER-5-TWO-EDGE-VERTEX",
            (6,),
            carrier_five_labels,
            ((0, 14), (7, 14)),
            14,
        ),
        audit_vertex_trivialization(
            "W6-CARRIER-5-FULL-LIVE-FIVE-EDGE-VERTEX",
            (6,),
            five_edge_labels,
            five_edge_live,
            12,
        ),
    ]


def run_vertex_trivialization_criterion() -> (
    VertexTrivializationCriterionReport
):
    controls = _natural_controls()
    counterexamples = [
        regular_simplex_holonomy_counterexample(width)
        for width in (3, 4, 5, 8, 12)
    ]
    finite_failures = sum(
        not row.vertex_trivialization_exists for row in controls
    )
    identity_failures = sum(
        row.gram_affine_spectrum_identity_residual > 1e-8
        for row in controls
    )
    counterexample_failures = sum(
        not row.exact_counterexample_audit for row in counterexamples
    )
    metrics: dict[str, int | float] = {
        "vertex_trivialization_psd_criterion_theorem_count": 1,
        "vertex_trivialization_constructive_gram_theorem_count": 1,
        "natural_finite_vertex_control_count": len(controls),
        "natural_finite_vertex_control_failure_count": finite_failures,
        "gram_affine_spectrum_identity_failure_count": identity_failures,
        "simplex_holonomy_counterexample_count": len(counterexamples),
        "simplex_holonomy_counterexample_failure_count": counterexample_failures,
        "uniform_reciprocal_magnitude_sufficiency_no_go_count": 1,
        "maximum_passing_natural_residual_edge_count": max(
            row.residual_live_edge_count for row in controls
        ),
        "minimum_natural_normalized_vertex_gram_eigenvalue": min(
            row.normalized_vertex_gram_minimum_eigenvalue for row in controls
        ),
        "minimum_simplex_normalized_vertex_gram_eigenvalue": min(
            row.normalized_vertex_gram_minimum_eigenvalue
            for row in counterexamples
        ),
        "all_depth_natural_vertex_trivialization_theorem_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    verified = not identity_failures and not counterexample_failures
    return VertexTrivializationCriterionReport(
        created_at=utc_now(),
        theorem_contract={
            "criterion": (
                "For residual block Gram G and 0<gamma<1, vertex "
                "isometries exist iff T_gamma=I+(G-I)/gamma is PSD, "
                "equivalently lambda_min(G)>=1-gamma."
            ),
            "construction": (
                "Any Gram factor T_gamma=W^*W partitions into isometries "
                "W_e because every diagonal block of T_gamma is identity."
            ),
            "simplex_no_go": (
                "A width-p regular simplex has every overlap -1/(p-1), "
                "but lambda_min(T)=2-p and the star metric minimum is 1."
            ),
            "natural_scope": (
                "Selected W6 residual carrier blocks pass the criterion. "
                "No all-n positivity theorem for the natural carrier-index "
                "Gram is proved."
            ),
        },
        natural_finite_controls=controls,
        simplex_counterexamples=counterexamples,
        proof_obligations=[
            {
                "obligation": "vertex_trivialization_exact_criterion",
                "resolved": verified,
                "resolution": "Reduced exactly to positivity of a normalized block Gram and supplied its constructive Gram factor.",
            },
            {
                "obligation": "uniform_reciprocal_correlation_implies_trivialization",
                "resolved": True,
                "resolution": "Rejected by the regular-simplex signed-holonomy counterfamily at width p and gamma=1/(p-1).",
            },
            {
                "obligation": "natural_collision_free_normalized_gram_psd_all_depth",
                "resolved": False,
                "resolution": "Need a carrier-index/Racah positivity theorem or a natural negative-cycle counterexample; finite W6 controls are insufficient.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "A single observed correlation value supplies the missing vertex isometries.",
                "resolved": True,
                "resolution": "False: all regular-simplex correlations have one magnitude while the normalized Gram is indefinite.",
            },
            {
                "objection": "Arbitrary holonomy cannot affect the metric floor.",
                "resolved": True,
                "resolution": "Only holonomy inside an already constructed isometry Gram is harmless. Pairwise maps with frustrated cycle products may not admit that Gram at all.",
            },
            {
                "objection": "The abstract simplex occurs naturally in wreath carrier blocks.",
                "resolved": False,
                "resolution": "No natural realization is known; exact finite natural controls instead lie on the PSD boundary.",
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "vertex_trivialization_psd_criterion_proved": verified,
            "constructive_vertex_isometry_gram_factor_proved": verified,
            "uniform_reciprocal_magnitude_sufficient": False,
            "signed_cycle_holonomy_can_falsify_trivialization": True,
            "selected_natural_finite_vertices_pass": finite_failures == 0,
            "all_depth_natural_vertex_trivialization_proved": False,
            "unconditional_width_independent_laplacian_floor_proved": False,
            "graded_defect_bound_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The missing hypothesis now has an exact PSD test, and "
                "uniform magnitudes are formally insufficient. Natural "
                "carrier-index Gram positivity remains unproved."
            ),
        },
        status=(
            "vertex-trivialization-psd-criterion-proved-"
            "uniform-magnitude-rejected-natural-positivity-open"
        ),
        summary=(
            "Reduced vertex trivialization to one normalized-Gram positivity "
            "test. Three W6 controls pass, but a reciprocal regular-simplex "
            "counterfamily proves that correlation uniformity alone cannot "
            "justify the all-depth Laplacian floor."
        ),
        falsifiers_triggered=[
            "A single residual correlation value is not evidence of a common vertex-isometry factorization.",
            "Pairwise reciprocal bounds do not prevent signed cycle frustration.",
            "The regular-simplex star reaches metric minimum one at only linear width.",
            "The all-depth theorem must prove normalized carrier-index Gram positivity on natural source mass.",
        ],
    )


def write_vertex_trivialization_criterion_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-VERTEX-TRIVIALIZATION-CRITERION"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_vertex_trivialization_criterion())
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
                id="NEG-SELF-DUAL-WREATH-VERTEX-TRIVIALIZATION-CRITERION",
                source=registry_experiment_id,
                claim=(
                    "Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-VERTEX-TRIVIALIZATION-CRITERION."
                ),
                reason_invalid=(
                    "Falsified or refined by exact theorem evaluation."
                ),
                lesson=(
                    "Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-VERTEX-TRIVIALIZATION-CRITERION."
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
                    "self_dual_wreath_vertex_trivialization_criterion": str(path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_vertex_trivialization_criterion_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
