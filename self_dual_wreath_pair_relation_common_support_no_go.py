"""Every exact two-vertex relation is confined to literal common support.

Let ``E_v`` be the orientation projectors, ``F=sum_v E_v``, and let

    B_v=E_v F^(+/2)

be the coordinate maps of the canonical analysis polar on ``supp(F)``.
Consider the most general linear relation involving only vertices ``u,v``:

    R_u B_u + R_v B_v = 0.                                (1)

Put ``T=R_uB_u=-R_vB_v``.  The row space of ``T`` lies in both coordinate row
spaces, so

    rank(T) <= dim(Ran(B_u^*) intersect Ran(B_v^*)).       (2)

Because ``F^(+/2)`` is invertible on the frame support,

    Ran(B_v^*)=F^(+/2)Ran(E_v),

and therefore

    dim(Ran(B_u^*) intersect Ran(B_v^*))
      =dim(Ran(E_u) intersect Ran(E_v)).                   (3)

The bound is tight: choose an orthonormal basis ``Z`` of the intersection and
use pseudoinverse endpoint maps so both sides of (1) equal ``Z^*``.  Thus the
maximum exact pair-relation rank is exactly the multiplicity of principal
angle one.  Noncommon principal-angle channels, including those transported
directly by pair GPE, cannot participate in any exact two-vertex linear
dependency, with or without operator-valued endpoint metrics.

This closes pair-only sheaf presentations of the complete polar, not all
relation-based architectures.  The remaining target is a genuinely
higher-arity, coherently selectable parity-check/preconditioner whose kernel
is the full analysis range and whose nonzero singular gap is polynomial.
Direct rectangular CS transforms also remain open.  No decoder, classical
separation, or speedup is claimed.
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
    "self_dual_wreath_pair_relation_common_support_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-PAIR-RELATION-COMMON-SUPPORT-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Label = tuple[Partition, Partition]


@dataclass(frozen=True)
class PairRelationCommonSupportControl:
    control_id: str
    n: int
    target_partition: Partition
    labels: tuple[Label, ...]
    left_orientation_mask: int
    right_orientation_mask: int
    frame_support_rank: int
    left_coordinate_rank: int
    right_coordinate_rank: int
    active_pair_principal_channel_rank: int
    common_principal_channel_rank: int
    noncommon_principal_channel_rank: int
    coordinate_row_space_intersection_rank: int
    maximum_exact_pair_relation_rank: int
    noncommon_channel_rank_uncovered_by_pair_relations: int
    intersection_common_rank_residual: int
    constructed_maximal_relation_residual: float
    constructed_maximal_relation_rank: int
    exact_pair_relation_rank_theorem_verified: bool
    status: str


@dataclass(frozen=True)
class PairRelationScalingRecord:
    n: int
    information_threshold_copy_count: int
    orientation_vertex_count_log2: int
    maximum_pair_relation_rank_equals_common_support: bool
    operator_endpoint_metrics_recover_noncommon_channels: bool
    pair_only_sheaf_compiles_complete_polar: bool
    genuinely_higher_arity_relations_required: bool
    coherent_higher_arity_parity_check_compiled: bool
    direct_rectangular_cs_transform_open: bool
    status: str


@dataclass(frozen=True)
class PairRelationCommonSupportTheorem:
    general_pair_relation: str
    row_space_bound: str
    canonical_row_spaces: str
    exact_maximum_rank: str
    consequence: str
    surviving_target: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class PairRelationCommonSupportReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: PairRelationCommonSupportTheorem
    finite_controls: list[PairRelationCommonSupportControl]
    scaling_records: list[PairRelationScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _positive_basis(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    values, vectors = np.linalg.eigh((matrix + matrix.conj().T) / 2.0)
    return vectors[:, values > tolerance]


def _inverse_square_root(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    values, vectors = np.linalg.eigh((matrix + matrix.conj().T) / 2.0)
    inverse = np.zeros_like(values)
    inverse[values > tolerance] = 1.0 / np.sqrt(values[values > tolerance])
    return (vectors * inverse) @ vectors.conj().T


def _row_space_basis(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    _, singular_values, right_adjoint = np.linalg.svd(
        matrix,
        full_matrices=False,
    )
    return right_adjoint.conj().T[:, singular_values > tolerance]


def _intersection_basis(
    left: np.ndarray,
    right: np.ndarray,
    tolerance: float,
) -> np.ndarray:
    if not left.shape[1] or not right.shape[1]:
        return np.zeros((left.shape[0], 0), dtype=complex)
    cross_left, singular_values, _ = np.linalg.svd(
        left.conj().T @ right,
        full_matrices=False,
    )
    common = singular_values >= 1 - 100 * tolerance
    return left @ cross_left[:, common]


def audit_pair_relation_common_support(
    control_id: str,
    target_partition: Partition,
    labels: tuple[Label, ...],
    left_orientation_mask: int,
    right_orientation_mask: int,
    *,
    tolerance: float = 1e-9,
) -> PairRelationCommonSupportControl:
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
    support = _positive_basis(frame, tolerance)
    if not support.shape[1]:
        raise ValueError("the orientation frame has empty support")
    inverse = _inverse_square_root(frame, tolerance)
    left_projector = projectors[left_orientation_mask]
    right_projector = projectors[right_orientation_mask]
    left_coordinate = left_projector @ inverse @ support
    right_coordinate = right_projector @ inverse @ support

    left_rows = _row_space_basis(left_coordinate, tolerance)
    right_rows = _row_space_basis(right_coordinate, tolerance)
    row_intersection = _intersection_basis(left_rows, right_rows, tolerance)
    common_rank = row_intersection.shape[1]

    pair_singular_values = np.linalg.svd(
        right_projector @ left_projector,
        compute_uv=False,
    )
    active_values = pair_singular_values[pair_singular_values > tolerance]
    active_rank = len(active_values)
    principal_common_rank = int(
        np.count_nonzero(active_values >= 1 - 100 * tolerance)
    )
    noncommon_rank = active_rank - principal_common_rank

    if common_rank:
        target_relation = row_intersection.conj().T
        left_endpoint = target_relation @ np.linalg.pinv(left_coordinate)
        right_endpoint = -target_relation @ np.linalg.pinv(right_coordinate)
        relation = (
            left_endpoint @ left_coordinate
            + right_endpoint @ right_coordinate
        )
        relation_residual = float(np.linalg.norm(relation, ord=2))
        constructed_rank = int(
            np.linalg.matrix_rank(
                left_endpoint @ left_coordinate,
                tol=100 * tolerance,
            )
        )
    else:
        relation_residual = 0.0
        constructed_rank = 0

    rank_residual = abs(common_rank - principal_common_rank)
    verified = bool(
        rank_residual == 0
        and constructed_rank == common_rank
        and relation_residual <= 1000 * tolerance
    )
    return PairRelationCommonSupportControl(
        control_id=control_id,
        n=sum(target_partition),
        target_partition=target_partition,
        labels=labels,
        left_orientation_mask=left_orientation_mask,
        right_orientation_mask=right_orientation_mask,
        frame_support_rank=support.shape[1],
        left_coordinate_rank=left_rows.shape[1],
        right_coordinate_rank=right_rows.shape[1],
        active_pair_principal_channel_rank=active_rank,
        common_principal_channel_rank=principal_common_rank,
        noncommon_principal_channel_rank=noncommon_rank,
        coordinate_row_space_intersection_rank=common_rank,
        maximum_exact_pair_relation_rank=common_rank,
        noncommon_channel_rank_uncovered_by_pair_relations=noncommon_rank,
        intersection_common_rank_residual=rank_residual,
        constructed_maximal_relation_residual=relation_residual,
        constructed_maximal_relation_rank=constructed_rank,
        exact_pair_relation_rank_theorem_verified=verified,
        status=(
            "pair-relations-confined-to-common-support-noncommon-uncovered"
            if verified and noncommon_rank
            else "common-support-pair-relation-rank-tight"
            if verified
            else "pair-relation-common-support-control-failure"
        ),
    )


def pair_relation_scaling_record(n: int) -> PairRelationScalingRecord:
    if n < 5:
        raise ValueError("n must be at least five")
    copies = math.ceil(math.lgamma(n + 1) / math.log(2)) + 2
    return PairRelationScalingRecord(
        n=n,
        information_threshold_copy_count=copies,
        orientation_vertex_count_log2=copies,
        maximum_pair_relation_rank_equals_common_support=True,
        operator_endpoint_metrics_recover_noncommon_channels=False,
        pair_only_sheaf_compiles_complete_polar=False,
        genuinely_higher_arity_relations_required=True,
        coherent_higher_arity_parity_check_compiled=False,
        direct_rectangular_cs_transform_open=True,
        status="pair-only-relations-closed-higher-arity-preconditioner-open",
    )


def _finite_controls() -> list[PairRelationCommonSupportControl]:
    return [
        audit_pair_relation_common_support(
            "S4-CORRELATION-ONE-HALF",
            (2, 2),
            (((4,), (3, 1)), ((2, 2), (2, 1, 1))),
            0,
            3,
        ),
        audit_pair_relation_common_support(
            "S4-CORRELATION-ONE-THIRD",
            (2, 1, 1),
            (((4,), (3, 1)), ((2, 2), (2, 1, 1))),
            1,
            2,
        ),
        audit_pair_relation_common_support(
            "S5-CORRELATION-ONE-QUARTER",
            (2, 1, 1, 1),
            (((5,), (4, 1)), ((2, 1, 1, 1), (1, 1, 1, 1, 1))),
            0,
            3,
        ),
        audit_pair_relation_common_support(
            "S4-COMMON-CHANNEL-CONTROL",
            (1, 1, 1, 1),
            (((4,), (3, 1)), ((2, 1, 1), (1, 1, 1, 1))),
            1,
            2,
        ),
    ]


def run_pair_relation_common_support_no_go() -> PairRelationCommonSupportReport:
    controls = _finite_controls()
    scaling = [
        pair_relation_scaling_record(n)
        for n in (5, 6, 8, 10, 12, 16, 20, 24, 32, 48, 64, 96, 128)
    ]
    failures = sum(
        not row.exact_pair_relation_rank_theorem_verified for row in controls
    )
    noncommon = [row for row in controls if row.noncommon_principal_channel_rank]
    common = [row for row in controls if not row.noncommon_principal_channel_rank]
    verified = bool(
        failures == 0
        and len(noncommon) == 3
        and len(common) == 1
        and all(row.maximum_exact_pair_relation_rank == 0 for row in noncommon)
        and common[0].maximum_exact_pair_relation_rank == 1
    )
    theorem = PairRelationCommonSupportTheorem(
        general_pair_relation="R_uB_u+R_vB_v=0 with T=R_uB_u=-R_vB_v",
        row_space_bound=(
            "Ran(T^*) is contained in Ran(B_u^*) intersect Ran(B_v^*)"
        ),
        canonical_row_spaces="Ran(B_v^*)=F^(+/2)Ran(E_v)",
        exact_maximum_rank=(
            "max rank(T)=dim(Ran(E_u) intersect Ran(E_v)), attained by pseudoinverse lifts"
        ),
        consequence=(
            "operator-valued two-vertex relations cannot carry noncommon principal channels"
        ),
        surviving_target=(
            "genuinely higher-arity parity checks/preconditioners or a direct rectangular CS transform"
        ),
        theorem_verified=verified,
        status=(
            "pair-relations-exactly-common-support-higher-arity-required"
            if verified
            else "pair-relation-common-support-theorem-control-failure"
        ),
    )
    return PairRelationCommonSupportReport(
        created_at=utc_now(),
        theorem_contract=asdict(theorem),
        theorem=theorem,
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "classify_all_exact_two_vertex_relations",
                "resolved": True,
                "resolution": (
                    "Their shared row image is exactly the intersection of the "
                    "two canonical coordinate row spaces."
                ),
            },
            {
                "obligation": "relate_coordinate_row_intersection_to_projector_common_range",
                "resolved": True,
                "resolution": (
                    "The common invertible map F^(+/2) preserves intersection dimension."
                ),
            },
            {
                "obligation": "construct_coherent_higher_arity_dependency_checks",
                "resolved": False,
                "resolution": (
                    "Need sparse polynomial SELECT, exact full-range kernel, and "
                    "an inverse-polynomial nonzero singular gap."
                ),
            },
            {
                "obligation": "compile_direct_rectangular_cs_polar",
                "resolved": False,
                "resolution": "No normalization-one higher recoupling transform is supplied.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "Positive endpoint weights can repair the pair sheaf.",
                "resolved": True,
                "resolution": (
                    "Arbitrary endpoint maps are already allowed in R_u,R_v; "
                    "their common relation image cannot exceed literal common support."
                ),
            },
            {
                "objection": "Pair GPE creates an exact relation on every active channel.",
                "resolved": True,
                "resolution": (
                    "It creates a transport between carrier subspaces, not an "
                    "equality between the two canonical global-polar coordinates."
                ),
            },
            {
                "objection": "A sufficiently dense graph of pair relations may recover noncommon channels.",
                "resolved": True,
                "resolution": (
                    "Every individual pair row lies in a common-support channel; "
                    "density cannot create a pair row outside the span of those rows."
                ),
            },
            {
                "objection": "This rejects all dependency-based compilers.",
                "resolved": True,
                "resolution": (
                    "No. Relations involving three or more vertices can cancel "
                    "without any pairwise row-space intersection."
                ),
            },
        ],
        headline_metrics={
            "pair_relation_common_support_theorem_count": int(verified),
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "noncommon_pair_control_count": len(noncommon),
            "common_pair_control_count": len(common),
            "total_noncommon_channel_rank_uncovered": sum(
                row.noncommon_channel_rank_uncovered_by_pair_relations
                for row in controls
            ),
            "maximum_intersection_common_rank_residual": max(
                row.intersection_common_rank_residual for row in controls
            ),
            "maximum_constructed_relation_residual": max(
                row.constructed_maximal_relation_residual for row in controls
            ),
            "scaling_record_count": len(scaling),
            "coherent_higher_arity_parity_check_compiler_count": 0,
            "direct_rectangular_cs_compiler_count": 0,
            "complete_orientation_polar_compiler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "maximum_exact_pair_relation_rank_equals_common_support": verified,
            "operator_weighted_pair_relations_recover_noncommon_channels": False,
            "pair_only_sheaf_compiles_complete_polar": False,
            "higher_arity_relations_mathematically_required_for_noncommon_dependencies": True,
            "coherent_higher_arity_parity_check_compiled": False,
            "direct_rectangular_cs_polar_compiled": False,
            "complete_natural_orientation_polar_compiled": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "All exact two-vertex relation rows live in literal common "
                "projector support, so noncommon frame dependencies require "
                "higher arity or a direct transform."
            ),
        },
        status=theorem.status,
        summary=(
            "Classified all exact pair relations of the canonical orientation "
            "polar and proved that their maximum rank is exactly common-support rank."
        ),
        falsifiers_triggered=[
            "Operator-valued endpoint metrics do not extend pair relations beyond common channels.",
            "Exact pair-GPE transport is not an exact dependency among global-polar coordinates.",
            "The complete dependency space cannot be sought inside pair-only sheaf edges.",
        ],
    )


def write_pair_relation_common_support_no_go_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_pair_relation_common_support_no_go())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    report = write_pair_relation_common_support_no_go_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
