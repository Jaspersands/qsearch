"""Cross-synthesis dependency theorem for balanced orientation merges.

Let ``R_L : C_L -> H`` and ``R_R : C_R -> H`` be synthesis maps for two
children, so their frame operators are ``A=R_L R_L^*`` and
``B=R_R R_R^*``.  Internal coefficient redundancies are

    N = ker(R_L) direct_sum ker(R_R).

The genuinely cross-child dependencies are the quotient represented by

    W = ker[R_L,-R_R] intersect N^perp.                         (1)

Every ``y`` in ``K=ran(R_L) intersect ran(R_R)`` has a unique vector in W,

    T y = (R_L^+ y, R_R^+ y),

and ``T`` is an isomorphism from K onto W.  If
``J=diag(I_C_L,-I_C_R)`` is the coefficient grading, then

    T^* T   = U^*(A^+ + B^+)U,
    T^* J T = U^*(A^+ - B^+)U.                                (2)

Consequently the fractional relative-effect eigenvalues are

    lambda = (1-delta)/2,  delta in spec(P_W J P_W |_W).       (3)

In particular, every common channel is exactly one half if and only if W is
totally neutral for the grading: ``P_W J P_W=0``.  This is equivalent to the
shorted-metric equality ``U^*A^+U=U^*B^+U``.

Unlike the pseudoinverse statement, (1) is a kernel/quotient formulation.  It
is therefore the right target for a representation-theoretic decomposition:
decompose the cross relations after removing each child's internal syzygies,
rather than attempting to invert exponentially large frame operators.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_collision_free_frame_probe import Label, _w5_probe_labels
from self_dual_wreath_level_three_flag_audit import _reduced_projector_family
from self_dual_wreath_shorted_overlap_balance import (
    _range_intersection_basis,
    _relative_effect_spectrum,
    _support_basis,
    unique_affine_flag_merges,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_cross_dependency_neutrality.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-CROSS-DEPENDENCY-NEUTRALITY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class CrossDependencyRecord:
    record_id: str
    left_coefficient_dimension: int
    right_coefficient_dimension: int
    left_synthesis_rank: int
    right_synthesis_rank: int
    common_range_dimension: int
    cross_dependency_dimension: int
    dependency_to_common_range_dimension_residual: int
    maximum_dependency_subspace_residual: float
    grading_neutrality_residual: float
    actual_fractional_eigenvalues: tuple[float, ...]
    dependency_predicted_fractional_eigenvalues: tuple[float, ...]
    maximum_fractional_spectrum_residual: float
    exact_dependency_quotient_theorem_verified: bool
    grading_neutral: bool
    status: str


@dataclass(frozen=True)
class CrossDependencyControl:
    control_id: str
    n: int
    target_partition: tuple[int, ...]
    labels: tuple[Label, ...]
    globally_distinct_source_partitions: bool
    fractional_merge_count: int
    neutral_fractional_merge_count: int
    nonneutral_fractional_merge_count: int
    maximum_dependency_subspace_residual: float
    maximum_fractional_spectrum_residual: float
    exact_dependency_theorem_failure_count: int
    records: list[CrossDependencyRecord]
    status: str


@dataclass(frozen=True)
class CrossDependencyNeutralityReport:
    created_at: str
    theorem_contract: dict[str, Any]
    generic_controls: list[CrossDependencyRecord]
    wreath_controls: list[CrossDependencyControl]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _svd_rank(matrix: np.ndarray, tolerance: float) -> int:
    singular_values = np.linalg.svd(matrix, compute_uv=False)
    return int(np.sum(singular_values > tolerance))


def _row_space_basis(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    """Return an isometry onto ``ker(matrix)^perp`` in its domain."""

    _, singular_values, right = np.linalg.svd(matrix, full_matrices=False)
    positive = singular_values > tolerance
    return right[positive, :].conj().T


def _null_space_basis(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    _, singular_values, right = np.linalg.svd(matrix, full_matrices=True)
    rank = int(np.sum(singular_values > tolerance))
    return right[rank:, :].conj().T


def _block_diagonal(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    output = np.zeros(
        (left.shape[0] + right.shape[0], left.shape[1] + right.shape[1]),
        dtype=complex,
    )
    output[: left.shape[0], : left.shape[1]] = left
    output[left.shape[0] :, left.shape[1] :] = right
    return output


def _leaf_synthesis(
    projectors: tuple[np.ndarray, ...],
    masks: tuple[int, ...],
    tolerance: float,
) -> np.ndarray:
    bases = tuple(_support_basis(projectors[mask], tolerance) for mask in masks)
    return np.concatenate(bases, axis=1)


def audit_cross_dependency(
    record_id: str,
    left_synthesis: np.ndarray,
    right_synthesis: np.ndarray,
    *,
    tolerance: float = 1e-8,
) -> CrossDependencyRecord:
    """Verify (1)--(3) directly from two arbitrary synthesis maps."""

    if left_synthesis.ndim != 2 or right_synthesis.ndim != 2:
        raise ValueError("synthesis maps must be matrices")
    if left_synthesis.shape[0] != right_synthesis.shape[0]:
        raise ValueError("synthesis maps must have the same physical codomain")

    left_row = _row_space_basis(left_synthesis, tolerance)
    right_row = _row_space_basis(right_synthesis, tolerance)
    quotient_domain = _block_diagonal(left_row, right_row)
    signed_synthesis = np.concatenate(
        (left_synthesis, -right_synthesis),
        axis=1,
    )
    quotient_kernel = _null_space_basis(
        signed_synthesis @ quotient_domain,
        tolerance,
    )
    dependency = quotient_domain @ quotient_kernel

    left_range = _support_basis(
        left_synthesis @ left_synthesis.conj().T,
        tolerance,
    )
    right_range = _support_basis(
        right_synthesis @ right_synthesis.conj().T,
        tolerance,
    )
    common = _range_intersection_basis(left_range, right_range, tolerance)
    common_dimension = common.shape[1]

    if common_dimension:
        canonical = np.vstack(
            (
                np.linalg.pinv(left_synthesis, rcond=tolerance) @ common,
                np.linalg.pinv(right_synthesis, rcond=tolerance) @ common,
            )
        )
        canonical_basis = _support_basis(
            canonical @ canonical.conj().T,
            tolerance,
        )
        dependency_projection = dependency @ dependency.conj().T
        canonical_projection = canonical_basis @ canonical_basis.conj().T
        subspace_residual = float(
            np.linalg.norm(dependency_projection - canonical_projection, ord=2)
        )
    else:
        subspace_residual = float(
            np.linalg.norm(dependency @ dependency.conj().T, ord=2)
        )

    left_coefficients = left_synthesis.shape[1]
    grading = np.diag(
        np.concatenate(
            (
                np.ones(left_coefficients),
                -np.ones(right_synthesis.shape[1]),
            )
        )
    )
    compressed_grading = dependency.conj().T @ grading @ dependency
    compressed_grading = (compressed_grading + compressed_grading.conj().T) / 2
    neutrality = float(
        np.linalg.norm(compressed_grading, ord=2)
        if compressed_grading.size
        else 0.0
    )
    defects = np.linalg.eigvalsh(compressed_grading)
    predicted = np.sort((1.0 - defects) / 2.0)

    left_frame = left_synthesis @ left_synthesis.conj().T
    right_frame = right_synthesis @ right_synthesis.conj().T
    actual, _ = _relative_effect_spectrum(left_frame, right_frame, tolerance)
    actual = np.sort(actual)
    if len(actual) == len(predicted):
        spectrum_residual = float(
            np.max(np.abs(actual - predicted)) if len(actual) else 0.0
        )
    else:
        spectrum_residual = float("inf")

    dimension_residual = dependency.shape[1] - common_dimension
    verified = bool(
        dimension_residual == 0
        and subspace_residual <= 100 * tolerance
        and spectrum_residual <= 100 * tolerance
    )
    neutral = neutrality <= 100 * tolerance
    return CrossDependencyRecord(
        record_id=record_id,
        left_coefficient_dimension=left_synthesis.shape[1],
        right_coefficient_dimension=right_synthesis.shape[1],
        left_synthesis_rank=_svd_rank(left_synthesis, tolerance),
        right_synthesis_rank=_svd_rank(right_synthesis, tolerance),
        common_range_dimension=common_dimension,
        cross_dependency_dimension=dependency.shape[1],
        dependency_to_common_range_dimension_residual=dimension_residual,
        maximum_dependency_subspace_residual=subspace_residual,
        grading_neutrality_residual=neutrality,
        actual_fractional_eigenvalues=tuple(float(value) for value in actual),
        dependency_predicted_fractional_eigenvalues=tuple(
            float(value) for value in predicted
        ),
        maximum_fractional_spectrum_residual=spectrum_residual,
        exact_dependency_quotient_theorem_verified=verified,
        grading_neutral=neutral,
        status=(
            "exact-neutral-cross-dependency"
            if verified and neutral
            else "exact-nonneutral-cross-dependency"
            if verified
            else "cross-dependency-theorem-validation-failure"
        ),
    )


def audit_wreath_cross_dependencies(
    control_id: str,
    n: int,
    target: tuple[int, ...],
    labels: tuple[Label, ...],
    *,
    tolerance: float = 1e-8,
) -> CrossDependencyControl:
    projectors, _, _ = _reduced_projector_family(target, labels, tolerance)
    records = []
    for left, right in unique_affine_flag_merges():
        left_synthesis = _leaf_synthesis(projectors, left, tolerance)
        right_synthesis = _leaf_synthesis(projectors, right, tolerance)
        record = audit_cross_dependency(
            f"{control_id}-W{len(left)}-{'-'.join(map(str, left))}-{'-'.join(map(str, right))}",
            left_synthesis,
            right_synthesis,
            tolerance=tolerance,
        )
        if record.common_range_dimension:
            records.append(record)
    source = tuple(partition for label in labels for partition in label)
    failures = sum(
        not row.exact_dependency_quotient_theorem_verified for row in records
    )
    neutral = sum(row.grading_neutral for row in records)
    return CrossDependencyControl(
        control_id=control_id,
        n=n,
        target_partition=target,
        labels=labels,
        globally_distinct_source_partitions=len(source) == len(set(source)),
        fractional_merge_count=len(records),
        neutral_fractional_merge_count=neutral,
        nonneutral_fractional_merge_count=len(records) - neutral,
        maximum_dependency_subspace_residual=max(
            (row.maximum_dependency_subspace_residual for row in records),
            default=0.0,
        ),
        maximum_fractional_spectrum_residual=max(
            (row.maximum_fractional_spectrum_residual for row in records),
            default=0.0,
        ),
        exact_dependency_theorem_failure_count=failures,
        records=records,
        status=(
            "all-cross-dependencies-neutral"
            if records and not failures and neutral == len(records)
            else "exact-nonneutral-cross-dependencies-present"
            if not failures
            else "cross-dependency-audit-failure"
        ),
    )


def run_cross_dependency_neutrality() -> CrossDependencyNeutralityReport:
    balanced = audit_cross_dependency(
        "GENERIC-EQUAL-METRIC",
        np.diag((1.0, 2.0)),
        np.diag((1.0, 2.0)),
    )
    unbalanced = audit_cross_dependency(
        "GENERIC-UNEQUAL-METRIC",
        np.diag((np.sqrt(2.0), 1.0)),
        np.diag((1.0, np.sqrt(2.0))),
    )
    distinct_triangle: tuple[Label, ...] = (
        ((3,), (2, 1)),
        ((3,), (1, 1, 1)),
        ((2, 1), (1, 1, 1)),
    )
    controls = [
        audit_wreath_cross_dependencies(
            "W3-DISTINCT-LABEL-TRIANGLE",
            3,
            (2, 1),
            distinct_triangle,
        ),
        audit_wreath_cross_dependencies(
            "W3-REPEATED-LABEL-FALSIFIER",
            3,
            (2, 1),
            (((3,), (2, 1)),) * 3,
        ),
        audit_wreath_cross_dependencies(
            "W5-COLLISION-FREE-3-2",
            5,
            (3, 2),
            _w5_probe_labels()[0],
        ),
    ]
    failures = sum(
        row.exact_dependency_theorem_failure_count for row in controls
    ) + sum(
        not row.exact_dependency_quotient_theorem_verified
        for row in (balanced, unbalanced)
    )
    label_simple = [row for row in controls if row.globally_distinct_source_partitions]
    repeated = [row for row in controls if not row.globally_distinct_source_partitions]
    finite_signal = bool(label_simple) and all(
        row.nonneutral_fractional_merge_count == 0 for row in label_simple
    )
    repeated_falsifier = any(
        row.nonneutral_fractional_merge_count > 0 for row in repeated
    )
    metrics: dict[str, int | float] = {
        "exact_cross_dependency_theorem_count": int(failures == 0),
        "generic_control_count": 2,
        "wreath_control_count": len(controls),
        "finite_cross_dependency_record_count": sum(
            len(row.records) for row in controls
        ),
        "finite_theorem_validation_failure_count": failures,
        "label_simple_nonneutral_dependency_count": sum(
            row.nonneutral_fractional_merge_count for row in label_simple
        ),
        "repeated_label_nonneutral_dependency_count": sum(
            row.nonneutral_fractional_merge_count for row in repeated
        ),
        "symbolic_representation_dependency_decomposition_count": 0,
        "all_n_neutrality_theorem_count": 0,
        "coherent_dependency_transform_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return CrossDependencyNeutralityReport(
        created_at=utc_now(),
        theorem_contract={
            "cross_dependency_space": (
                "W=ker[R_L,-R_R] intersect (ker R_L direct_sum ker R_R)^perp"
            ),
            "common_range_isomorphism": (
                "y maps to (R_L^+y,R_R^+y), an isomorphism from the child-range intersection onto W"
            ),
            "grading_pencil": (
                "The grading compression P_W diag(I,-I) P_W has eigenvalues delta=1-2 lambda, where lambda are the fractional relative-effect eigenvalues."
            ),
            "balance_criterion": (
                "Every fractional channel is one half iff W is totally neutral for the coefficient grading."
            ),
            "research_use": (
                "Decompose cross-child syzygies modulo internal syzygies in representation labels; do not invert the full frame."
            ),
        },
        generic_controls=[balanced, unbalanced],
        wreath_controls=controls,
        proof_obligations=[
            {
                "obligation": "cross_dependency_quotient_theorem",
                "resolved": failures == 0,
                "resolution": "Linear-algebra proof and finite controls identify W with the common range and recover its full fractional spectrum.",
            },
            {
                "obligation": "symbolic_wreath_dependency_decomposition",
                "resolved": False,
                "resolution": "The current finite construction still forms leaf bases; an all-n Kronecker/Racah decomposition of W is open.",
            },
            {
                "obligation": "all_n_collision_free_neutrality",
                "resolved": False,
                "resolution": "Label-simple W3/W5 controls are neutral, but no growing-depth theorem excludes nonneutral cross syzygies.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "Balanced child dimensions force half channels.",
                "resolved": True,
                "resolution": "The generic unequal-metric control has equal dimensions but grading defects +/-1/3 and channels 1/3,2/3.",
            },
            {
                "objection": "Removing internal kernels is cosmetic.",
                "resolved": True,
                "resolution": "Without quotienting internal syzygies, ker[R_L,-R_R] contains unrelated child redundancies and its grading is not the common-range metric.",
            },
            {
                "objection": "The dependency theorem itself supplies an efficient transform.",
                "resolved": False,
                "resolution": "It changes the mathematical target from inversion to structured kernel decomposition but does not yet compute that decomposition coherently.",
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "cross_dependency_quotient_theorem_proved": failures == 0,
            "finite_label_simple_dependencies_neutral": finite_signal,
            "repeated_labels_falsify_universal_neutrality": repeated_falsifier,
            "symbolic_wreath_dependency_decomposition_proved": False,
            "all_n_collision_free_neutrality_proved": False,
            "coherent_dependency_transform_compiled": False,
            "hierarchical_orientation_polar_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The exact obstruction is now a graded cross-syzygy space, but its all-n representation decomposition and coherent transform remain open."
            ),
        },
        status="cross-dependency-neutrality-theorem-symbolic-wreath-decomposition-open",
        summary=(
            "Replaced compressed frame inversion by an exact cross-synthesis dependency quotient; all label-simple finite dependencies are neutral, while repeated labels and a generic equal-dimension control exhibit nonneutral defects."
        ),
        falsifiers_triggered=[
            "Equal child dimensions do not imply equal shorted metrics.",
            "A child-range intersection is not characterized by the raw cross-kernel until internal synthesis kernels are quotiented out.",
            "The kernel formulation is not a circuit without a sparse representation-theoretic dependency decomposition.",
        ],
    )


def write_cross_dependency_neutrality(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_cross_dependency_neutrality())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    output = write_cross_dependency_neutrality()
    print(json.dumps(output["headline_metrics"], indent=2, sort_keys=True))
