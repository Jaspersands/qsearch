"""Exact failure boundary for matrix-valued Cayley orientation fibers.

Scalar XOR-circulant coefficient fibers force half-integral affine merges.
Growing Kronecker multiplicities can replace the scalar kernel by an operator-
valued positive-definite function

    V_f^* V_e = Gamma(f+e) in End(X).                       (1)

For an affine half split ``G_0`` and ``t+G_0``, Walsh transform on ``G_0``
still gives, for every character chi,

    Gram_chi = [[C_chi,D_chi],[D_chi,C_chi]],               (2)

with ``C_chi +/- D_chi >= 0``.  Restrict to ``supp(C_chi)`` and define

    X_+ = ker(C_chi-D_chi),   X_- = ker(C_chi+D_chi).       (3)

The cross-synthesis dependency space consists of the normalized relations
``(x,x)`` for ``x in X_+`` and ``(y,-y)`` for ``y in X_-``.  Compression of
the left-minus-right grading has nonzero eigenvalues

    +/- singular_values(Q_+^* Q_-),                         (4)

where ``Q_+`` and ``Q_-`` are orthonormal bases of the two saturation spaces.
Therefore the fractional relative channels are

    (1 +/- singular_values(Q_+^*Q_-))/2,                    (5)

plus one-half channels for unmatched dimensions.

This is the exact matrix-valued boundary.  Cayley covariance forces balance
iff opposite saturation spaces are orthogonal for every Walsh character.
Scalar kernels satisfy this automatically because at most one sign can
saturate on a nonzero scalar mode.  Pairwise commuting ``C_chi,D_chi`` also
suffice.  A two-dimensional positive-definite matrix-Cayley counterfamily
below has nonorthogonal opposite kernels and produces nonhalf channels despite
perfect XOR translation invariance and isometric leaf fibers.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_cross_dependency_neutrality import audit_cross_dependency
from self_dual_wreath_shorted_overlap_balance import _relative_effect_spectrum


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_matrix_cayley_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-MATRIX-CAYLEY-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class MatrixCayleyCharacterRecord:
    character_signs: tuple[int, ...]
    restricted_internal_dimension: int
    plus_saturation_dimension: int
    minus_saturation_dimension: int
    opposite_saturation_overlap_singular_values: tuple[float, ...]
    maximum_opposite_saturation_overlap: float
    child_cross_commutator_residual: float
    predicted_fractional_eigenvalues: tuple[float, ...]
    opposite_saturation_spaces_orthogonal: bool
    commuting_character_operators: bool


@dataclass(frozen=True)
class MatrixCayleyBoundaryRecord:
    record_id: str
    group_size: int
    internal_fiber_dimension: int
    child_size: int
    maximum_leaf_isometry_residual: float
    maximum_matrix_cayley_translation_residual: float
    maximum_scalar_kernel_residual: float
    minimum_full_gram_eigenvalue: float
    actual_common_range_dimension: int
    predicted_common_range_dimension: int
    actual_fractional_eigenvalues: tuple[float, ...]
    predicted_fractional_eigenvalues: tuple[float, ...]
    maximum_fractional_spectrum_residual: float
    maximum_opposite_saturation_overlap: float
    grading_neutrality_residual: float
    matrix_cayley_boundary_theorem_verified: bool
    scalar_cayley_kernel: bool
    all_character_operators_commute: bool
    opposite_saturation_spaces_orthogonal: bool
    all_fractional_channels_half: bool
    character_records: list[MatrixCayleyCharacterRecord]
    status: str


@dataclass(frozen=True)
class MatrixCayleyBoundaryReport:
    created_at: str
    theorem_contract: dict[str, Any]
    controls: list[MatrixCayleyBoundaryRecord]
    scaling_records: list[dict[str, Any]]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _support_basis(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    hermitian = (matrix + matrix.conj().T) / 2
    values, vectors = np.linalg.eigh(hermitian)
    return vectors[:, values > tolerance]


def _null_basis(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    hermitian = (matrix + matrix.conj().T) / 2
    values, vectors = np.linalg.eigh(hermitian)
    return vectors[:, np.abs(values) <= 100 * tolerance]


def _unique_characters(
    subgroup: tuple[int, ...],
    ambient_bits: int,
) -> tuple[tuple[int, ...], ...]:
    rows: dict[tuple[int, ...], tuple[int, ...]] = {}
    for functional in range(1 << ambient_bits):
        signs = tuple(
            -1 if (functional & value).bit_count() % 2 else 1
            for value in subgroup
        )
        rows.setdefault(signs, signs)
    return tuple(rows)


def matrix_kernel_from_fourier_symbols(
    symbols: dict[int, np.ndarray],
    group_bits: int,
) -> dict[int, np.ndarray]:
    """Inverse Walsh transform of positive matrix Fourier symbols."""

    size = 1 << group_bits
    if set(symbols) != set(range(size)):
        raise ValueError("one Fourier symbol is required for every character")
    dimension = symbols[0].shape[0]
    if any(value.shape != (dimension, dimension) for value in symbols.values()):
        raise ValueError("Fourier symbols must have a common square shape")
    return {
        element: sum(
            (
                (-1 if (character & element).bit_count() % 2 else 1)
                * symbols[character]
                for character in range(size)
            ),
            np.zeros((dimension, dimension), dtype=complex),
        )
        / size
        for element in range(size)
    }


def factor_matrix_cayley_fibers(
    kernel: dict[int, np.ndarray],
    group_bits: int,
    *,
    tolerance: float = 1e-10,
) -> tuple[np.ndarray, ...]:
    """Return leaf isometries whose block Gram is the matrix Cayley kernel."""

    size = 1 << group_bits
    internal = kernel[0].shape[0]
    gram = np.block(
        [
            [kernel[left ^ right] for right in range(size)]
            for left in range(size)
        ]
    )
    values, vectors = np.linalg.eigh((gram + gram.conj().T) / 2)
    if values[0] < -100 * tolerance:
        raise ValueError("matrix kernel is not positive definite")
    positive = values > tolerance
    factor = (
        np.sqrt(values[positive])[:, None] * vectors[:, positive].conj().T
    )
    return tuple(
        factor[:, index * internal : (index + 1) * internal]
        for index in range(size)
    )


def audit_matrix_cayley_boundary(
    record_id: str,
    fibers: tuple[np.ndarray, ...],
    left_masks: tuple[int, ...],
    right_masks: tuple[int, ...],
    *,
    tolerance: float = 1e-8,
) -> MatrixCayleyBoundaryRecord:
    if not fibers or len(fibers) & (len(fibers) - 1):
        raise ValueError("a power-of-two nonempty fiber family is required")
    if len(left_masks) != len(right_masks) or set(left_masks) & set(right_masks):
        raise ValueError("disjoint balanced children are required")
    if set(left_masks) | set(right_masks) != set(range(len(fibers))):
        raise ValueError("children must partition the full group")
    physical_dimension, internal = fibers[0].shape
    if any(fiber.shape != (physical_dimension, internal) for fiber in fibers):
        raise ValueError("all fibers must have the same shape")

    identity = np.eye(internal)
    isometry_residual = max(
        float(np.linalg.norm(fiber.conj().T @ fiber - identity, ord=2))
        for fiber in fibers
    )
    values_by_difference: dict[int, list[np.ndarray]] = {
        difference: [] for difference in range(len(fibers))
    }
    scalar_residual = 0.0
    for left, left_fiber in enumerate(fibers):
        for right, right_fiber in enumerate(fibers):
            value = left_fiber.conj().T @ right_fiber
            values_by_difference[left ^ right].append(value)
            scalar = np.trace(value) / internal
            scalar_residual = max(
                scalar_residual,
                float(np.linalg.norm(value - scalar * identity, ord=2)),
            )
    kernel = {
        difference: sum(values) / len(values)
        for difference, values in values_by_difference.items()
    }
    translation_residual = max(
        float(np.linalg.norm(value - kernel[difference], ord=2))
        for difference, values in values_by_difference.items()
        for value in values
    )
    full_gram = np.block(
        [
            [kernel[left ^ right] for right in range(len(fibers))]
            for left in range(len(fibers))
        ]
    )
    minimum_gram = float(
        np.min(np.linalg.eigvalsh((full_gram + full_gram.conj().T) / 2))
    )

    left_anchor = left_masks[0]
    subgroup = tuple(sorted(mask ^ left_anchor for mask in left_masks))
    if set(left_masks) != {left_anchor ^ value for value in subgroup}:
        raise ValueError("left child must be an affine subgroup coset")
    translation = right_masks[0] ^ left_anchor
    if set(right_masks) != {
        left_anchor ^ translation ^ value for value in subgroup
    }:
        raise ValueError("right child must be its translated affine coset")
    ambient_bits = (len(fibers) - 1).bit_length()

    character_records = []
    predicted_values: list[float] = []
    predicted_common = 0
    maximum_overlap = 0.0
    for signs in _unique_characters(subgroup, ambient_bits):
        child = sum(
            (
                sign * kernel[value]
                for value, sign in zip(subgroup, signs)
            ),
            np.zeros((internal, internal), dtype=complex),
        )
        cross = sum(
            (
                sign * kernel[translation ^ value]
                for value, sign in zip(subgroup, signs)
            ),
            np.zeros((internal, internal), dtype=complex),
        )
        child = (child + child.conj().T) / 2
        cross = (cross + cross.conj().T) / 2
        support = _support_basis(child, tolerance)
        restricted_child = support.conj().T @ child @ support
        restricted_cross = support.conj().T @ cross @ support
        plus = _null_basis(restricted_child - restricted_cross, tolerance)
        minus = _null_basis(restricted_child + restricted_cross, tolerance)
        overlap = plus.conj().T @ minus
        singular_values = np.linalg.svd(overlap, compute_uv=False)
        singular_values = singular_values[singular_values > 100 * tolerance]
        defects = [
            value
            for singular in singular_values
            for value in (-float(singular), float(singular))
        ]
        unmatched = plus.shape[1] + minus.shape[1] - 2 * len(singular_values)
        predicted_values.extend((1.0 - defect) / 2.0 for defect in defects)
        predicted_values.extend([0.5] * unmatched)
        predicted_common += plus.shape[1] + minus.shape[1]
        mode_overlap = float(
            singular_values[0] if len(singular_values) else 0.0
        )
        maximum_overlap = max(maximum_overlap, mode_overlap)
        commutator = float(
            np.linalg.norm(
                restricted_child @ restricted_cross
                - restricted_cross @ restricted_child,
                ord=2,
            )
            if restricted_child.size
            else 0.0
        )
        character_records.append(
            MatrixCayleyCharacterRecord(
                character_signs=signs,
                restricted_internal_dimension=support.shape[1],
                plus_saturation_dimension=plus.shape[1],
                minus_saturation_dimension=minus.shape[1],
                opposite_saturation_overlap_singular_values=tuple(
                    float(value) for value in singular_values
                ),
                maximum_opposite_saturation_overlap=mode_overlap,
                child_cross_commutator_residual=commutator,
                predicted_fractional_eigenvalues=tuple(
                    sorted((1.0 - defect) / 2.0 for defect in defects)
                    + [0.5] * unmatched
                ),
                opposite_saturation_spaces_orthogonal=(
                    mode_overlap <= 100 * tolerance
                ),
                commuting_character_operators=commutator <= 100 * tolerance,
            )
        )

    left_synthesis = np.concatenate(
        tuple(fibers[mask] for mask in left_masks),
        axis=1,
    )
    right_synthesis = np.concatenate(
        tuple(fibers[mask] for mask in right_masks),
        axis=1,
    )
    dependency = audit_cross_dependency(
        f"{record_id}-DEPENDENCY",
        left_synthesis,
        right_synthesis,
        tolerance=tolerance,
    )
    left_frame = left_synthesis @ left_synthesis.conj().T
    right_frame = right_synthesis @ right_synthesis.conj().T
    actual, _ = _relative_effect_spectrum(left_frame, right_frame, tolerance)
    actual_values = tuple(float(value) for value in np.sort(actual))
    predicted_tuple = tuple(sorted(predicted_values))
    spectrum_residual = (
        float(np.max(np.abs(np.asarray(actual_values) - predicted_tuple)))
        if len(actual_values) == len(predicted_tuple)
        else math.inf
    )
    verified = bool(
        dependency.exact_dependency_quotient_theorem_verified
        and translation_residual <= 100 * tolerance
        and isometry_residual <= 100 * tolerance
        and predicted_common == dependency.common_range_dimension
        and spectrum_residual <= 100 * tolerance
        and abs(maximum_overlap - dependency.grading_neutrality_residual)
        <= 100 * tolerance
    )
    all_half = max(
        (abs(value - 0.5) for value in actual_values),
        default=0.0,
    ) <= 100 * tolerance
    all_commute = all(
        row.commuting_character_operators for row in character_records
    )
    orthogonal = all(
        row.opposite_saturation_spaces_orthogonal
        for row in character_records
    )
    scalar = scalar_residual <= 100 * tolerance
    return MatrixCayleyBoundaryRecord(
        record_id=record_id,
        group_size=len(fibers),
        internal_fiber_dimension=internal,
        child_size=len(left_masks),
        maximum_leaf_isometry_residual=isometry_residual,
        maximum_matrix_cayley_translation_residual=translation_residual,
        maximum_scalar_kernel_residual=scalar_residual,
        minimum_full_gram_eigenvalue=minimum_gram,
        actual_common_range_dimension=dependency.common_range_dimension,
        predicted_common_range_dimension=predicted_common,
        actual_fractional_eigenvalues=actual_values,
        predicted_fractional_eigenvalues=predicted_tuple,
        maximum_fractional_spectrum_residual=spectrum_residual,
        maximum_opposite_saturation_overlap=maximum_overlap,
        grading_neutrality_residual=dependency.grading_neutrality_residual,
        matrix_cayley_boundary_theorem_verified=verified,
        scalar_cayley_kernel=scalar,
        all_character_operators_commute=all_commute,
        opposite_saturation_spaces_orthogonal=orthogonal,
        all_fractional_channels_half=all_half,
        character_records=character_records,
        status=(
            "matrix-cayley-neutral-saturation"
            if verified and all_half
            else "matrix-cayley-nonorthogonal-saturation-counterexample"
            if verified
            else "matrix-cayley-boundary-validation-failure"
        ),
    )


def _rank_one(vector: np.ndarray) -> np.ndarray:
    vector = vector / np.linalg.norm(vector)
    return vector[:, None] @ vector[None, :]


def _matrix_cayley_control(
    record_id: str,
    *,
    nonorthogonal: bool,
) -> MatrixCayleyBoundaryRecord:
    identity = np.eye(2)
    first = np.array([1.0, 0.0])
    second = (
        np.array([1.0, 1.0])
        if nonorthogonal
        else np.array([0.0, 1.0])
    )
    plus_symbol = _rank_one(first)
    minus_symbol = _rank_one(second)
    remainder = (4 * identity - plus_symbol - minus_symbol) / 2
    symbols = {
        0: plus_symbol,
        1: remainder,
        2: minus_symbol,
        3: remainder,
    }
    kernel = matrix_kernel_from_fourier_symbols(symbols, group_bits=2)
    fibers = factor_matrix_cayley_fibers(kernel, group_bits=2)
    return audit_matrix_cayley_boundary(
        record_id,
        fibers,
        (0, 1),
        (2, 3),
    )


def run_matrix_cayley_boundary() -> MatrixCayleyBoundaryReport:
    commuting = _matrix_cayley_control(
        "COMMUTING-ORTHOGONAL-SATURATION",
        nonorthogonal=False,
    )
    counterexample = _matrix_cayley_control(
        "NONCOMMUTING-NONORTHOGONAL-SATURATION",
        nonorthogonal=True,
    )
    controls = [commuting, counterexample]
    failures = sum(
        not row.matrix_cayley_boundary_theorem_verified for row in controls
    )
    metrics: dict[str, int | float] = {
        "matrix_cayley_boundary_theorem_count": int(failures == 0),
        "exact_control_count": len(controls),
        "theorem_validation_failure_count": failures,
        "commuting_neutral_control_count": int(
            commuting.all_fractional_channels_half
        ),
        "noncommuting_nonneutral_counterexample_count": int(
            not counterexample.all_fractional_channels_half
        ),
        "counterexample_maximum_opposite_saturation_overlap": (
            counterexample.maximum_opposite_saturation_overlap
        ),
        "counterexample_maximum_half_residual": max(
            abs(value - 0.5)
            for value in counterexample.actual_fractional_eigenvalues
        ),
        "finite_wreath_matrix_valued_cayley_counterexample_count": 0,
        "all_n_saturation_orthogonality_theorem_count": 0,
        "coherent_internal_saturation_projector_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    scaling = [
        {
            "n": n,
            "information_threshold_copy_count": math.ceil(
                math.lgamma(n + 1) / math.log(2)
            ),
            "kronecker_multiplicity_spaces_can_be_matrix_valued": True,
            "collision_free_saturation_orthogonality_proved": False,
            "collision_free_matrix_cayley_counterexample_found": False,
            "coherent_internal_saturation_projectors_proved": False,
            "status": "matrix-valued-saturation-boundary-open-on-natural-wreath-fibers",
        }
        for n in (6, 8, 16, 32, 64, 128, 256, 512)
    ]
    return MatrixCayleyBoundaryReport(
        created_at=utc_now(),
        theorem_contract={
            "operator_cayley_reduction": "Walsh transform reduces an End(X)-valued XOR kernel to child/cross operators C_chi,D_chi.",
            "opposite_saturation_spaces": "X_+=ker(C_chi-D_chi) and X_-=ker(C_chi+D_chi) after removing ker(C_chi).",
            "grading_defects": "Nonzero dependency-grading eigenvalues are +/- singular values of Q_+^*Q_-.",
            "relative_channels": "Fractional channels are (1 +/- s_j)/2, with extra one-half channels for unmatched saturation dimensions.",
            "balance_boundary": "All channels are one half iff X_+ is orthogonal to X_- for every Walsh character.",
            "sufficient_conditions": "Scalar kernels or pairwise commuting C_chi,D_chi imply saturation orthogonality.",
        },
        controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "matrix_cayley_saturation_boundary",
                "resolved": failures == 0,
                "resolution": "Exact kernel decomposition and two positive-definite controls reproduce both common dimension and every fractional eigenvalue.",
            },
            {
                "obligation": "natural_wreath_saturation_orthogonality",
                "resolved": False,
                "resolution": "Finite label-simple fibers are scalar, but growing Kronecker multiplicities can create the matrix-valued countermechanism.",
            },
            {
                "obligation": "coherent_internal_saturation_projectors",
                "resolved": False,
                "resolution": "Even neutral matrix-valued sectors require coherent kernels of C_chi +/- D_chi in multiplicity space.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "XOR translation covariance alone proves half balance.",
                "resolved": True,
                "resolution": "The noncommuting matrix-Cayley control has exact covariance but nonorthogonal opposite kernels and nonhalf channels.",
            },
            {
                "objection": "Equal diagonal child Gram blocks force neutral cross relations.",
                "resolved": True,
                "resolution": "Plus and minus relation sectors can have nonzero ordinary overlap even though they are orthogonal in a C-weighted metric.",
            },
            {
                "objection": "A matrix-valued kernel necessarily destroys balance.",
                "resolved": True,
                "resolution": "The commuting matrix-valued control has orthogonal saturation spaces and only one-half channels.",
            },
            {
                "objection": "Half balance gives an efficient internal transform.",
                "resolved": False,
                "resolution": "Projecting onto kernels of matrix-valued Fourier symbols may be as hard as the original recoupling problem.",
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "matrix_cayley_saturation_boundary_proved": failures == 0,
            "matrix_cayley_covariance_alone_suffices_for_balance": False,
            "noncommuting_matrix_cayley_counterexample_verified": (
                counterexample.matrix_cayley_boundary_theorem_verified
                and not counterexample.all_fractional_channels_half
            ),
            "commuting_matrix_cayley_sufficient_condition_verified": (
                commuting.matrix_cayley_boundary_theorem_verified
                and commuting.all_fractional_channels_half
            ),
            "natural_collision_free_saturation_orthogonality_proved": False,
            "coherent_internal_saturation_projectors_compiled": False,
            "hierarchical_orientation_polar_proved": False,
            "speedup_claim_allowed": False,
            "reason": "The exact multiplicity-space failure mode is known, but it has not been excluded or found in the natural all-n wreath portfolio.",
        },
        status="matrix-cayley-saturation-boundary-natural-wreath-case-open",
        summary=(
            "Proved the exact matrix-valued Cayley boundary: opposite saturation-space overlap produces nonhalf channels. An explicit positive-definite XOR-covariant counterfamily kills covariance-only proofs, while commuting sectors remain balanced."
        ),
        falsifiers_triggered=[
            "Matrix-valued XOR covariance does not by itself force half-integral affine merges.",
            "Equal child Gram blocks do not make the cross-dependency quotient neutral when opposite saturation kernels overlap.",
            "Matrix-valued multiplicity sectors are not automatically fatal; commuting or saturation-orthogonal sectors remain balanced.",
            "A spectral balance theorem does not implement the multiplicity-space kernel projectors.",
        ],
    )


def write_matrix_cayley_boundary(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_matrix_cayley_boundary())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    output = write_matrix_cayley_boundary()
    print(json.dumps(output["headline_metrics"], indent=2, sort_keys=True))
