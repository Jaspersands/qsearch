"""Exact relation-cokernel transfer for the orientation PGM polar.

Let ``Q_e : C_e -> H`` be isometries onto orientation ranges ``U_e`` and put

    D_0 = [Q_1 ... Q_N] : direct_sum_e C_e -> H.             (1)

The coefficient form of the orientation analysis is ``D_0^*``.  If ``T``
embeds each coefficient fiber back into its own copy of ``H``, then the
physical analysis used by the PGM is

    R = vertical_stack_e (Q_e Q_e^*) = T D_0^*.              (2)

Consequently its polar output has coefficient support

    range(D_0^*) = ker(D_0)^perp.                             (3)

The pair-common boundary ``D_1`` inserts a vector in ``U_e intersection U_f``
with opposite signs at its two endpoints.  Hence ``D_0 D_1=0`` and

    image(D_1) subset ker(D_0).                               (4)

Equations (3)-(4) settle one ambiguity in the graded Frobenius trim.  Trimming
or retaining *any* subspace of pair-relation image has exactly zero overlap
with every ideal PGM polar output.  There is no coefficient-to-state-mass
conversion factor to prove: the state loss is identically zero.

This does not prove that pair relations characterize the polar output.  The
remaining spurious coefficient directions are exactly

    H_0 = ker(D_0) / image(D_1),                              (5)

and the complement of pair relations equals the PGM output support if and only
if ``H_0=0``.  Three distinct lines in a plane give the decisive generic
counterexample: all pair intersections vanish while ``ker(D_0)`` is
one-dimensional.  Thus a constant endpoint gap on a trimmed pair complex is a
conditioning theorem for known constraints, not yet a complete polar sampler.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_augmented_common_core_cech import (
    augmented_common_core_cech_data,
)
from self_dual_wreath_collision_free_frame_probe import Label


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_relation_cokernel_transfer.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-RELATION-COKERNEL-TRANSFER"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class RelationCokernelControl:
    control_id: str
    control_family: str
    physical_dimension: int
    leaf_count: int
    leaf_coefficient_dimension: int
    synthesis_rank: int
    synthesis_kernel_dimension: int
    pair_relation_coefficient_dimension: int
    pair_relation_rank: int
    emergent_h0_dimension: int
    polar_output_rank: int
    trimmed_relation_rank: int
    maximum_leaf_isometry_residual: float
    analysis_factorization_residual: float
    polar_factorization_residual: float
    pair_boundary_annihilation_residual: float
    full_kernel_polar_overlap_residual: float
    pair_relation_polar_overlap_residual: float
    trimmed_relation_polar_overlap_residual: float
    trimmed_relation_pgm_trace_loss: float
    polar_support_cokernel_identity_residual: float
    pair_complement_polar_support_residual: float
    pair_relations_exhaust_synthesis_kernel: bool
    relation_trim_has_zero_ideal_pgm_state_loss: bool
    exact_relation_cokernel_audit: bool
    status: str


@dataclass(frozen=True)
class RelationCokernelTransferReport:
    created_at: str
    theorem_contract: dict[str, Any]
    controls: list[RelationCokernelControl]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _matrix_rank(matrix: np.ndarray, tolerance: float) -> int:
    if not matrix.size:
        return 0
    return int(np.sum(np.linalg.svd(matrix, compute_uv=False) > 100 * tolerance))


def _orthonormal_span(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    if not matrix.size or not matrix.shape[1]:
        return np.zeros((matrix.shape[0], 0), dtype=complex)
    left, values, _ = np.linalg.svd(matrix, full_matrices=False)
    return left[:, values > 100 * tolerance]


def _kernel_basis(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    if not matrix.shape[1]:
        return np.zeros((0, 0), dtype=complex)
    _, values, right = np.linalg.svd(matrix, full_matrices=True)
    rank = int(np.sum(values > 100 * tolerance))
    return right[rank:, :].conj().T


def _psd_inverse_square_root(
    matrix: np.ndarray,
    tolerance: float,
) -> np.ndarray:
    hermitian = (matrix + matrix.conj().T) / 2
    values, vectors = np.linalg.eigh(hermitian)
    if len(values) and values[0] < -100 * tolerance:
        raise ArithmeticError("frame operator is not positive semidefinite")
    inverse = np.zeros_like(values)
    positive = values > 100 * tolerance
    inverse[positive] = values[positive] ** -0.5
    return (vectors * inverse) @ vectors.conj().T


def _leaf_embedding(leaf_bases: tuple[np.ndarray, ...]) -> np.ndarray:
    physical_dimension = leaf_bases[0].shape[0]
    coefficient_dimension = sum(basis.shape[1] for basis in leaf_bases)
    embedding = np.zeros(
        (len(leaf_bases) * physical_dimension, coefficient_dimension),
        dtype=complex,
    )
    cursor = 0
    for leaf, basis in enumerate(leaf_bases):
        width = basis.shape[1]
        embedding[
            leaf * physical_dimension : (leaf + 1) * physical_dimension,
            cursor : cursor + width,
        ] = basis
        cursor += width
    return embedding


def pair_common_boundary(
    leaf_bases: tuple[np.ndarray, ...],
    *,
    tolerance: float = 1e-9,
) -> np.ndarray:
    """Construct ``D_1`` directly from exact pair intersections."""

    if not leaf_bases:
        raise ValueError("at least one leaf basis is required")
    physical_dimension = leaf_bases[0].shape[0]
    if any(basis.shape[0] != physical_dimension for basis in leaf_bases):
        raise ValueError("all leaf bases must share a physical carrier")
    widths = tuple(basis.shape[1] for basis in leaf_bases)
    offsets = np.cumsum((0, *widths))
    columns: list[np.ndarray] = []
    for left in range(len(leaf_bases)):
        for right in range(left + 1, len(leaf_bases)):
            overlap = leaf_bases[left].conj().T @ leaf_bases[right]
            left_vectors, singular_values, _ = np.linalg.svd(
                overlap,
                full_matrices=False,
            )
            common_dimension = int(
                np.sum(singular_values >= 1 - 100 * tolerance)
            )
            if not common_dimension:
                continue
            common = leaf_bases[left] @ left_vectors[:, :common_dimension]
            boundary = np.zeros((int(offsets[-1]), common_dimension), dtype=complex)
            boundary[
                offsets[left] : offsets[left + 1],
                :,
            ] = leaf_bases[left].conj().T @ common
            boundary[
                offsets[right] : offsets[right + 1],
                :,
            ] = -(leaf_bases[right].conj().T @ common)
            columns.append(boundary)
    if not columns:
        return np.zeros((int(offsets[-1]), 0), dtype=complex)
    return np.concatenate(columns, axis=1)


def audit_relation_cokernel_maps(
    control_id: str,
    control_family: str,
    leaf_bases: tuple[np.ndarray, ...],
    pair_boundary: np.ndarray,
    *,
    trim_seed: int = 20_260_808,
    tolerance: float = 1e-9,
) -> RelationCokernelControl:
    """Audit (1)-(5) for arbitrary finite subspaces and a pair boundary."""

    if not leaf_bases:
        raise ValueError("at least one leaf basis is required")
    physical_dimension = leaf_bases[0].shape[0]
    if any(basis.shape[0] != physical_dimension for basis in leaf_bases):
        raise ValueError("all leaf bases must share a physical carrier")
    isometry_residual = max(
        (
            float(
                np.linalg.norm(
                    basis.conj().T @ basis - np.eye(basis.shape[1]),
                    ord=2,
                )
            )
            for basis in leaf_bases
            if basis.shape[1]
        ),
        default=0.0,
    )
    if isometry_residual > 1000 * tolerance:
        raise ValueError("leaf bases must be isometries")

    synthesis = np.concatenate(leaf_bases, axis=1)
    coefficient_dimension = synthesis.shape[1]
    if pair_boundary.shape[0] != coefficient_dimension:
        raise ValueError("pair boundary has the wrong leaf coefficient dimension")
    embedding = _leaf_embedding(leaf_bases)
    projectors = tuple(basis @ basis.conj().T for basis in leaf_bases)
    physical_analysis = np.vstack(projectors)
    coefficient_analysis = synthesis.conj().T
    analysis_factorization = float(
        np.linalg.norm(
            physical_analysis - embedding @ coefficient_analysis,
            ord=2,
        )
    )

    frame = synthesis @ synthesis.conj().T
    inverse_root = _psd_inverse_square_root(frame, tolerance)
    coefficient_polar = coefficient_analysis @ inverse_root
    physical_polar = physical_analysis @ inverse_root
    polar_factorization = float(
        np.linalg.norm(physical_polar - embedding @ coefficient_polar, ord=2)
    )

    synthesis_kernel = _kernel_basis(synthesis, tolerance)
    pair_image = _orthonormal_span(pair_boundary, tolerance)
    kernel_dimension = synthesis_kernel.shape[1]
    pair_rank = pair_image.shape[1]
    emergent_dimension = kernel_dimension - pair_rank
    if emergent_dimension < 0:
        raise ArithmeticError("pair relation rank exceeds the synthesis kernel")

    rng = np.random.default_rng(trim_seed)
    if pair_rank:
        trim_rank = max(1, (pair_rank + 1) // 2)
        trial = rng.normal(size=(pair_rank, trim_rank)) + 1j * rng.normal(
            size=(pair_rank, trim_rank)
        )
        trim_coordinates, _ = np.linalg.qr(trial)
        trimmed_relations = pair_image @ trim_coordinates[:, :trim_rank]
    else:
        trimmed_relations = np.zeros((coefficient_dimension, 0), dtype=complex)
    trim_rank = trimmed_relations.shape[1]

    kernel_projector = synthesis_kernel @ synthesis_kernel.conj().T
    pair_projector = pair_image @ pair_image.conj().T
    trim_projector = trimmed_relations @ trimmed_relations.conj().T
    polar_support = coefficient_polar @ coefficient_polar.conj().T
    identity = np.eye(coefficient_dimension)

    annihilation = float(np.linalg.norm(synthesis @ pair_boundary, ord=2))
    full_kernel_overlap = float(
        np.linalg.norm(synthesis_kernel.conj().T @ coefficient_polar, ord=2)
        if kernel_dimension
        else 0.0
    )
    pair_overlap = float(
        np.linalg.norm(pair_image.conj().T @ coefficient_polar, ord=2)
        if pair_rank
        else 0.0
    )
    trim_overlap = float(
        np.linalg.norm(trimmed_relations.conj().T @ coefficient_polar, ord=2)
        if trim_rank
        else 0.0
    )
    trace_loss = float(
        np.linalg.norm(
            coefficient_polar.conj().T
            @ trim_projector
            @ coefficient_polar,
            ord=2,
        )
    )
    support_identity = float(
        np.linalg.norm(polar_support - (identity - kernel_projector), ord=2)
    )
    pair_complement_residual = float(
        np.linalg.norm((identity - pair_projector) - polar_support, ord=2)
    )
    complete = emergent_dimension == 0
    zero_loss = bool(
        trim_overlap <= 1000 * tolerance
        and trace_loss <= 1000 * tolerance
    )
    polar_rank = _matrix_rank(coefficient_polar, tolerance)
    verified = bool(
        isometry_residual <= 1000 * tolerance
        and analysis_factorization <= 1000 * tolerance
        and polar_factorization <= 1000 * tolerance
        and annihilation <= 1000 * tolerance
        and full_kernel_overlap <= 1000 * tolerance
        and pair_overlap <= 1000 * tolerance
        and zero_loss
        and support_identity <= 1000 * tolerance
        and polar_rank == _matrix_rank(synthesis, tolerance)
        and kernel_dimension == coefficient_dimension - polar_rank
        and ((pair_complement_residual <= 1000 * tolerance) == complete)
    )
    return RelationCokernelControl(
        control_id=control_id,
        control_family=control_family,
        physical_dimension=physical_dimension,
        leaf_count=len(leaf_bases),
        leaf_coefficient_dimension=coefficient_dimension,
        synthesis_rank=_matrix_rank(synthesis, tolerance),
        synthesis_kernel_dimension=kernel_dimension,
        pair_relation_coefficient_dimension=pair_boundary.shape[1],
        pair_relation_rank=pair_rank,
        emergent_h0_dimension=emergent_dimension,
        polar_output_rank=polar_rank,
        trimmed_relation_rank=trim_rank,
        maximum_leaf_isometry_residual=isometry_residual,
        analysis_factorization_residual=analysis_factorization,
        polar_factorization_residual=polar_factorization,
        pair_boundary_annihilation_residual=annihilation,
        full_kernel_polar_overlap_residual=full_kernel_overlap,
        pair_relation_polar_overlap_residual=pair_overlap,
        trimmed_relation_polar_overlap_residual=trim_overlap,
        trimmed_relation_pgm_trace_loss=trace_loss,
        polar_support_cokernel_identity_residual=support_identity,
        pair_complement_polar_support_residual=pair_complement_residual,
        pair_relations_exhaust_synthesis_kernel=complete,
        relation_trim_has_zero_ideal_pgm_state_loss=zero_loss,
        exact_relation_cokernel_audit=verified,
        status=(
            "exact-complete-pair-cokernel-zero-state-loss"
            if verified and complete
            else "exact-incomplete-pair-cokernel-zero-state-loss"
            if verified
            else "relation-cokernel-audit-failure"
        ),
    )


def audit_leaf_subspaces(
    control_id: str,
    control_family: str,
    leaf_bases: tuple[np.ndarray, ...],
    *,
    tolerance: float = 1e-9,
) -> RelationCokernelControl:
    boundary = pair_common_boundary(leaf_bases, tolerance=tolerance)
    return audit_relation_cokernel_maps(
        control_id,
        control_family,
        leaf_bases,
        boundary,
        tolerance=tolerance,
    )


def _abstract_controls() -> list[RelationCokernelControl]:
    e0 = np.asarray([[1.0], [0.0]], dtype=complex)
    e1 = np.asarray([[0.0], [1.0]], dtype=complex)
    diagonal = (e0 + e1) / np.sqrt(2)
    return [
        audit_leaf_subspaces(
            "THREE-IDENTICAL-LINES-PAIR-COMPLETE",
            "abstract-pair-generated",
            (e0, e0, e0),
        ),
        audit_leaf_subspaces(
            "THREE-LINES-IN-PLANE-EMERGENT-H0",
            "abstract-emergent-dependency",
            (e0, e1, diagonal),
        ),
        audit_leaf_subspaces(
            "MIXED-PAIR-AND-EMERGENT-DEPENDENCY",
            "abstract-partially-pair-generated",
            (e0, e0, e1, diagonal),
        ),
    ]


def _physical_control(
    control_id: str,
    target: tuple[int, ...],
    labels: tuple[Label, ...],
    orientation_masks: tuple[int, ...],
) -> RelationCokernelControl:
    bases, cells, boundaries, _, _ = augmented_common_core_cech_data(
        target,
        labels,
        orientation_masks,
    )
    leaf_bases = tuple(bases[cell] for cell in cells[1])
    boundary = boundaries.get(
        2,
        np.zeros((sum(basis.shape[1] for basis in leaf_bases), 0), dtype=complex),
    )
    return audit_relation_cokernel_maps(
        control_id,
        "physical-wreath-orientation-family",
        leaf_bases,
        boundary,
    )


def _physical_controls() -> list[RelationCokernelControl]:
    distinct_w3: tuple[Label, ...] = (
        ((3,), (2, 1)),
        ((3,), (1, 1, 1)),
        ((2, 1), (1, 1, 1)),
    )
    w5_labels: tuple[Label, ...] = (
        ((5,), (4, 1)),
        ((3, 2), (2, 2, 1)),
        ((2, 1, 1, 1), (1, 1, 1, 1, 1)),
    )
    return [
        _physical_control(
            "W3-DISTINCT-EMERGENT-H0-COKERNEL",
            (2, 1),
            distinct_w3,
            (0, 2, 5, 7),
        ),
        _physical_control(
            "W5-PAIR-GENERATED-COKERNEL",
            (3, 2),
            w5_labels,
            (0, 3, 5, 6),
        ),
    ]


def run_relation_cokernel_transfer() -> RelationCokernelTransferReport:
    controls = [*_abstract_controls(), *_physical_controls()]
    failures = sum(not row.exact_relation_cokernel_audit for row in controls)
    incomplete = [row for row in controls if row.emergent_h0_dimension]
    zero_loss = sum(
        row.relation_trim_has_zero_ideal_pgm_state_loss for row in controls
    )
    physical = [row for row in controls if row.control_family.startswith("physical")]
    metrics: dict[str, int | float] = {
        "exact_relation_cokernel_theorem_count": int(failures == 0),
        "finite_control_count": len(controls),
        "finite_control_failure_count": failures,
        "zero_state_loss_control_count": zero_loss,
        "emergent_h0_control_count": len(incomplete),
        "maximum_emergent_h0_dimension": max(
            (row.emergent_h0_dimension for row in controls),
            default=0,
        ),
        "physical_control_count": len(physical),
        "physical_emergent_h0_control_count": sum(
            bool(row.emergent_h0_dimension) for row in physical
        ),
        "all_n_pair_cokernel_exactness_count": 0,
        "coherent_full_cokernel_projector_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    verified = failures == 0
    return RelationCokernelTransferReport(
        created_at=utc_now(),
        theorem_contract={
            "analysis_factorization": (
                "For leaf isometries Q_e, the physical orientation analysis "
                "R=stack_e(Q_e Q_e^*) factors as T D_0^*."
            ),
            "polar_cokernel_identity": (
                "The coefficient polar output is range(D_0^*)=ker(D_0)^perp."
            ),
            "relation_orthogonality": (
                "D_0 D_1=0, so every retained or removed pair-relation "
                "subspace has exactly zero ideal PGM output amplitude."
            ),
            "completeness_criterion": (
                "The pair-relation complement equals the polar output support "
                "iff H_0=ker(D_0)/im(D_1) vanishes."
            ),
            "scope": (
                "This is an exact finite-dimensional identity. It proves zero "
                "state loss from relation trimming, not all-n H0 vanishing or "
                "a coherent projector onto the full synthesis cokernel."
            ),
        },
        controls=controls,
        proof_obligations=[
            {
                "obligation": "transfer_pair_relation_trim_to_pgm_state_mass",
                "resolved": verified,
                "resolution": (
                    "No asymptotic dimension-to-trace comparison is needed: "
                    "pair relations lie exactly in the orthogonal complement "
                    "of the PGM polar output."
                ),
            },
            {
                "obligation": "prove_all_n_augmented_h0_vanishing_or_resolve_h0",
                "resolved": False,
                "resolution": (
                    "Generic and physical W3 controls have emergent H0. "
                    "Selected W5 controls are pair-generated, but no typical "
                    "all-n theorem is known."
                ),
            },
            {
                "obligation": "compile_full_cokernel_complement_coherently",
                "resolved": False,
                "resolution": (
                    "The pinched pair-energy projector and any additional H0 "
                    "resolver still lack a polynomial coherent implementation."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": (
                    "Removing a positive fraction of relation coefficients may "
                    "remove a disproportionate fraction of PGM state mass."
                ),
                "resolved": True,
                "resolution": (
                    "Every relation vector is orthogonal to the entire ideal "
                    "polar output, so the loss is exactly zero for every input."
                ),
            },
            {
                "objection": (
                    "Zero relation-state overlap means pair constraints suffice "
                    "to characterize the polar output."
                ),
                "resolved": True,
                "resolution": (
                    "Three lines in a plane have no pair intersections and a "
                    "one-dimensional synthesis dependency. The missing space "
                    "is precisely augmented H0."
                ),
            },
            {
                "objection": (
                    "A constant endpoint gap on retained relations is already "
                    "a complete PGM sampler."
                ),
                "resolved": False,
                "resolution": (
                    "The gap conditions known constraints only. One must also "
                    "resolve emergent H0 and implement the complement coherently."
                ),
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "exact_relation_cokernel_identity_proved": verified,
            "relation_trim_zero_pgm_state_loss_proved": verified,
            "coefficient_to_pgm_trace_comparison_still_needed": False,
            "pair_relations_exhaust_full_cokernel_for_all_n": False,
            "typical_augmented_h0_vanishing_proved": False,
            "coherent_full_cokernel_projector_proved": False,
            "polynomial_hierarchical_polar_sampler_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Relation trimming is exactly signal-free, but pair relations "
                "need not exhaust the synthesis cokernel and no coherent full "
                "constraint projector is known."
            ),
        },
        status=(
            "relation-state-transfer-resolved-h0-and-circuit-open"
            if verified
            else "relation-cokernel-control-failure"
        ),
        summary=(
            "Proved that every pair-relation trim has exactly zero ideal PGM "
            "state loss and isolated augmented H0, rather than state-mass "
            "transfer, as the remaining completeness obstruction."
        ),
        falsifiers_triggered=[
            "The old coefficient-to-PGM state-mass transfer obligation was misposed; relation directions carry exactly zero ideal signal.",
            "Pairwise common cores do not universally generate the synthesis kernel.",
            "A well-conditioned partial relation complex can still leave spurious H0 output directions.",
        ],
    )


def write_relation_cokernel_transfer_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-RELATION-COKERNEL-TRANSFER"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_relation_cokernel_transfer())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")

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
                id="NEG-SELF-DUAL-WREATH-RELATION-COKERNEL-TRANSFER",
                source=registry_experiment_id,
                claim=(
                    "Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-RELATION-COKERNEL-TRANSFER."
                ),
                reason_invalid=(
                    "Falsified or refined by exact theorem evaluation."
                ),
                lesson=(
                    "Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-RELATION-COKERNEL-TRANSFER."
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
                    "self_dual_wreath_relation_cokernel_transfer": str(path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_relation_cokernel_transfer_report()
    print(json.dumps(report, indent=2))
