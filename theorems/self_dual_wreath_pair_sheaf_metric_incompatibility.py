"""Noncommon pair-polars cannot be glued into the global frame polar.

Let ``E_v`` be the orientation projectors, ``F=sum_v E_v``, and let

    W_v = E_v F^(+/2)

be the coordinate maps of the canonical analysis polar.  For a pair ``u,v``,
write

    U = polar(E_v E_u),   P=U^*U,   Q=UU^*.

The unweighted partial-holonomy sheaf imposes

    Q x_v = U P x_u.                                      (1)

If the canonical polar range satisfied (1), equality of the two endpoint
Gram operators would be necessary.  Since ``P<=E_u`` and ``Q<=E_v``, this is

    W_u^* P W_u = W_v^* Q W_v
    iff F^(+/2) P F^(+/2) = F^(+/2) Q F^(+/2)
    iff P=Q.                                               (2)

The final equivalence holds on ``supp(F)``, which contains both ``P`` and
``Q``.  A noncommon principal-angle channel has ``P!=Q``.  Consequently its
exact pair-GPE polar transport cannot be an unweighted sheaf edge of the
global orientation polar.  Common channels are compatible but carry only
literal shared subspaces.

This obstruction is invariant under arbitrary vertex-local output gauges:
conjugating ``W_u,W_v,P,Q,U`` by local isometries leaves the two pulled-back
Gram operators in (2) unchanged.  Proving coherent edge SELECT and a sheaf
gap would therefore not rescue the current unweighted architecture.

The result does not rule out operator-valued endpoint metrics, constraints
with a latent master fiber, higher-arity relations, or a direct rectangular
CS transform.  Those constructions must be analyzed separately; no complete
polar, decoder, classical separation, or speedup is claimed.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_orientation_fourier_reduction import (
    orientation_invariant_projector,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_pair_sheaf_metric_incompatibility.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-PAIR-SHEAF-METRIC-INCOMPATIBILITY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Label = tuple[Partition, Partition]


@dataclass(frozen=True)
class PairSheafMetricControl:
    control_id: str
    n: int
    target_partition: Partition
    labels: tuple[Label, ...]
    left_orientation_mask: int
    right_orientation_mask: int
    frame_rank: int
    active_pair_channel_rank: int
    common_pair_channel_rank: int
    noncommon_pair_channel_rank: int
    minimum_active_principal_correlation: float
    maximum_active_principal_correlation: float
    initial_final_projection_distance: float
    endpoint_metric_difference_norm: float
    canonical_section_residual: float
    endpoint_metric_identity_residual: float
    common_channel_compatibility_verified: bool
    noncommon_channel_incompatibility_verified: bool
    exact_metric_obstruction_verified: bool
    status: str


@dataclass(frozen=True)
class PairSheafMetricScalingRecord:
    n: int
    information_threshold_copy_count: int
    orientation_vertex_count_log2: int
    pair_gpe_noncommon_transport_polynomial: bool
    endpoint_metric_equality_necessary: bool
    vertex_local_gauge_can_repair_metric_mismatch: bool
    noncommon_pair_edges_compile_global_polar: bool
    common_edges_cover_complete_natural_frame_proved: bool
    operator_metric_or_higher_relation_compiler_proved: bool
    complete_orientation_polar_compiled: bool
    status: str


@dataclass(frozen=True)
class PairSheafMetricTheorem:
    canonical_coordinate_maps: str
    edge_gluing_condition: str
    endpoint_metric_necessity: str
    injective_support_consequence: str
    gauge_invariance: str
    surviving_architectures: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class PairSheafMetricReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: PairSheafMetricTheorem
    finite_controls: list[PairSheafMetricControl]
    scaling_records: list[PairSheafMetricScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _inverse_square_root(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    values, vectors = np.linalg.eigh((matrix + matrix.conj().T) / 2.0)
    inverse = np.zeros_like(values)
    inverse[values > tolerance] = 1.0 / np.sqrt(values[values > tolerance])
    return (vectors * inverse) @ vectors.conj().T


def _polar(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    left, singular_values, right_adjoint = np.linalg.svd(
        matrix,
        full_matrices=False,
    )
    active = singular_values > tolerance
    return left[:, active] @ right_adjoint[active, :]


def audit_pair_sheaf_metric(
    control_id: str,
    target_partition: Partition,
    labels: tuple[Label, ...],
    left_orientation_mask: int,
    right_orientation_mask: int,
    *,
    tolerance: float = 1e-9,
) -> PairSheafMetricControl:
    if not labels:
        raise ValueError("at least one orientation label is required")
    orientation_count = 1 << len(labels)
    if not 0 <= left_orientation_mask < orientation_count:
        raise ValueError("left orientation mask out of range")
    if not 0 <= right_orientation_mask < orientation_count:
        raise ValueError("right orientation mask out of range")
    if left_orientation_mask == right_orientation_mask:
        raise ValueError("the pair must use distinct orientations")

    projectors = tuple(
        orientation_invariant_projector(target_partition, labels, orientation)
        for orientation in range(orientation_count)
    )
    frame = sum(projectors, np.zeros_like(projectors[0]))
    inverse = _inverse_square_root(frame, tolerance)
    left_projector = projectors[left_orientation_mask]
    right_projector = projectors[right_orientation_mask]
    left_coordinate = left_projector @ inverse
    right_coordinate = right_projector @ inverse

    cross = right_projector @ left_projector
    singular_values = np.linalg.svd(cross, compute_uv=False)
    active_values = singular_values[singular_values > tolerance]
    if not len(active_values):
        raise ValueError("the selected pair has no active principal channel")
    transport = _polar(cross, tolerance)
    initial = transport.conj().T @ transport
    initial = (initial + initial.conj().T) / 2
    final = transport @ transport.conj().T
    final = (final + final.conj().T) / 2

    left_metric = left_coordinate.conj().T @ initial @ left_coordinate
    right_metric = right_coordinate.conj().T @ final @ right_coordinate
    metric_difference = left_metric - right_metric
    predicted_difference = inverse @ (initial - final) @ inverse
    identity_residual = float(
        np.linalg.norm(metric_difference - predicted_difference, ord=2)
    )
    projection_distance = float(np.linalg.norm(initial - final, ord=2))
    metric_difference_norm = float(np.linalg.norm(metric_difference, ord=2))
    section_residual = float(
        np.linalg.norm(
            final @ right_coordinate
            - transport @ initial @ left_coordinate,
            ord=2,
        )
    )
    common_rank = int(np.count_nonzero(active_values >= 1 - 100 * tolerance))
    noncommon_rank = len(active_values) - common_rank
    common_compatible = bool(
        noncommon_rank > 0
        or max(projection_distance, metric_difference_norm, section_residual)
        <= 1000 * tolerance
    )
    noncommon_incompatible = bool(
        noncommon_rank == 0
        or min(projection_distance, metric_difference_norm, section_residual)
        > 1000 * tolerance
    )
    verified = bool(
        identity_residual <= 1000 * tolerance
        and common_compatible
        and noncommon_incompatible
    )
    return PairSheafMetricControl(
        control_id=control_id,
        n=sum(target_partition),
        target_partition=target_partition,
        labels=labels,
        left_orientation_mask=left_orientation_mask,
        right_orientation_mask=right_orientation_mask,
        frame_rank=int(np.linalg.matrix_rank(frame, tol=100 * tolerance)),
        active_pair_channel_rank=len(active_values),
        common_pair_channel_rank=common_rank,
        noncommon_pair_channel_rank=noncommon_rank,
        minimum_active_principal_correlation=float(np.min(active_values)),
        maximum_active_principal_correlation=float(np.max(active_values)),
        initial_final_projection_distance=projection_distance,
        endpoint_metric_difference_norm=metric_difference_norm,
        canonical_section_residual=section_residual,
        endpoint_metric_identity_residual=identity_residual,
        common_channel_compatibility_verified=common_compatible,
        noncommon_channel_incompatibility_verified=noncommon_incompatible,
        exact_metric_obstruction_verified=verified,
        status=(
            "common-channel-unweighted-gluing-compatible"
            if verified and noncommon_rank == 0
            else "noncommon-pair-polar-unweighted-sheaf-incompatible"
            if verified
            else "pair-sheaf-metric-control-failure"
        ),
    )


def pair_sheaf_metric_scaling_record(n: int) -> PairSheafMetricScalingRecord:
    if n < 5:
        raise ValueError("n must be at least five")
    copies = math.ceil(math.lgamma(n + 1) / math.log(2)) + 2
    return PairSheafMetricScalingRecord(
        n=n,
        information_threshold_copy_count=copies,
        orientation_vertex_count_log2=copies,
        pair_gpe_noncommon_transport_polynomial=True,
        endpoint_metric_equality_necessary=True,
        vertex_local_gauge_can_repair_metric_mismatch=False,
        noncommon_pair_edges_compile_global_polar=False,
        common_edges_cover_complete_natural_frame_proved=False,
        operator_metric_or_higher_relation_compiler_proved=False,
        complete_orientation_polar_compiled=False,
        status="unweighted-noncommon-pair-sheaf-rejected-weighted-or-higher-relations-open",
    )


def _finite_controls() -> list[PairSheafMetricControl]:
    return [
        audit_pair_sheaf_metric(
            "S4-CORRELATION-ONE-HALF",
            (2, 2),
            (((4,), (3, 1)), ((2, 2), (2, 1, 1))),
            0,
            3,
        ),
        audit_pair_sheaf_metric(
            "S4-CORRELATION-ONE-THIRD",
            (2, 1, 1),
            (((4,), (3, 1)), ((2, 2), (2, 1, 1))),
            1,
            2,
        ),
        audit_pair_sheaf_metric(
            "S5-CORRELATION-ONE-QUARTER",
            (2, 1, 1, 1),
            (((5,), (4, 1)), ((2, 1, 1, 1), (1, 1, 1, 1, 1))),
            0,
            3,
        ),
        audit_pair_sheaf_metric(
            "S4-COMMON-CHANNEL-CONTROL",
            (1, 1, 1, 1),
            (((4,), (3, 1)), ((2, 1, 1), (1, 1, 1, 1))),
            1,
            2,
        ),
    ]


def run_pair_sheaf_metric_incompatibility() -> PairSheafMetricReport:
    controls = _finite_controls()
    scaling = [
        pair_sheaf_metric_scaling_record(n)
        for n in (5, 6, 8, 10, 12, 16, 20, 24, 32, 48, 64, 96, 128)
    ]
    failures = sum(not row.exact_metric_obstruction_verified for row in controls)
    noncommon = [row for row in controls if row.noncommon_pair_channel_rank]
    common = [row for row in controls if not row.noncommon_pair_channel_rank]
    verified = bool(
        failures == 0
        and len(noncommon) == 3
        and len(common) == 1
        and all(row.noncommon_channel_incompatibility_verified for row in noncommon)
        and all(row.common_channel_compatibility_verified for row in common)
    )
    theorem = PairSheafMetricTheorem(
        canonical_coordinate_maps="W_v=E_v F^(+/2), F=sum_v E_v",
        edge_gluing_condition="Q W_v=U P W_u for U=polar(E_vE_u)",
        endpoint_metric_necessity=(
            "edge gluing implies W_u^*P W_u=W_v^*Q W_v"
        ),
        injective_support_consequence=(
            "F^(+/2)(P-Q)F^(+/2)=0 iff P=Q on supp(F)"
        ),
        gauge_invariance=(
            "vertex-local output isometries conjugate edge supports but leave "
            "the pulled-back endpoint metrics unchanged"
        ),
        surviving_architectures=(
            "operator-valued endpoint metrics, latent master fibers, higher-arity "
            "relations, and direct rectangular CS transforms remain open"
        ),
        theorem_verified=verified,
        status=(
            "noncommon-pair-polar-unweighted-sheaf-no-go"
            if verified
            else "pair-sheaf-metric-theorem-control-failure"
        ),
    )
    return PairSheafMetricReport(
        created_at=utc_now(),
        theorem_contract=asdict(theorem),
        theorem=theorem,
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "derive_pair_edge_endpoint_metric_necessity",
                "resolved": True,
                "resolution": (
                    "Taking adjoint products of the sheaf edge equation gives "
                    "equality of the two pulled-back active endpoint effects."
                ),
            },
            {
                "obligation": "test_canonical_orientation_polar_against_pair_edges",
                "resolved": verified,
                "resolution": (
                    "Injectivity of F^(+/2) on support reduces compatibility to "
                    "P=Q; three noncommon physical controls fail and one common "
                    "control passes exactly."
                ),
            },
            {
                "obligation": "construct_metric_weighted_or_higher_relation_resolver",
                "resolved": False,
                "resolution": (
                    "A replacement must reproduce the canonical coordinate "
                    "effects without assuming one vertex coordinate determines another."
                ),
            },
            {
                "obligation": "compile_direct_rectangular_cs_polar",
                "resolved": False,
                "resolution": (
                    "No normalization-one singular-vector pairing is supplied."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "A different local gauge can make noncommon edges flat.",
                "resolved": True,
                "resolution": (
                    "Local gauges cancel from B_v^*Q_vB_v and B_u^*P_uB_u; "
                    "the unequal endpoint metrics are gauge invariant."
                ),
            },
            {
                "objection": "A good sheaf-Laplacian gap would fix the mismatch.",
                "resolved": True,
                "resolution": (
                    "A gap only projects onto the specified kernel. The canonical "
                    "polar range is not in that kernel on a noncommon edge."
                ),
            },
            {
                "objection": "Pair GPE is therefore useless.",
                "resolved": True,
                "resolution": (
                    "False. It still gives exact local reassociation and may enter "
                    "a weighted, higher-arity, or direct CS construction."
                ),
            },
            {
                "objection": "This proves all holonomy architectures impossible.",
                "resolved": True,
                "resolution": (
                    "No. The theorem rejects unweighted pair-equality gluing with "
                    "noncommon channels, not operator metrics or latent variables."
                ),
            },
        ],
        headline_metrics={
            "pair_edge_metric_necessity_theorem_count": int(verified),
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "noncommon_pair_incompatibility_control_count": len(noncommon),
            "common_pair_compatibility_control_count": len(common),
            "maximum_endpoint_metric_identity_residual": max(
                row.endpoint_metric_identity_residual for row in controls
            ),
            "minimum_noncommon_endpoint_metric_obstruction": min(
                row.endpoint_metric_difference_norm for row in noncommon
            ),
            "minimum_noncommon_canonical_section_residual": min(
                row.canonical_section_residual for row in noncommon
            ),
            "scaling_record_count": len(scaling),
            "operator_metric_or_higher_relation_compiler_count": 0,
            "complete_orientation_polar_compiler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "pair_edge_endpoint_metric_equality_necessary": True,
            "endpoint_metric_obstruction_vertex_gauge_invariant": True,
            "common_pair_channels_unweighted_compatible": verified,
            "noncommon_pair_gpe_edges_unweighted_compatible": False,
            "unweighted_noncommon_pair_sheaf_compiles_global_polar": False,
            "all_partial_holonomy_architectures_rejected": False,
            "operator_metric_or_higher_relation_compiler_proved": False,
            "complete_natural_orientation_polar_compiled": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Noncommon pair-polars align principal vectors but impose unequal "
                "canonical endpoint metrics, so the current unweighted sheaf "
                "projects onto the wrong section space."
            ),
        },
        status=theorem.status,
        summary=(
            "Rejected unweighted noncommon pair-polar gluing as a global "
            "orientation-polar architecture and isolated weighted or higher-arity "
            "relations as the surviving holonomy route."
        ),
        falsifiers_triggered=[
            "Exact pair transport does not imply that global-polar coordinates satisfy an edge equality.",
            "Vertex-local output gauges cannot repair unequal pulled-back endpoint metrics.",
            "A sheaf gap for the unweighted pair connection would efficiently project onto the wrong subspace.",
        ],
    )


def write_pair_sheaf_metric_incompatibility_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_pair_sheaf_metric_incompatibility())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    report = write_pair_sheaf_metric_incompatibility_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
