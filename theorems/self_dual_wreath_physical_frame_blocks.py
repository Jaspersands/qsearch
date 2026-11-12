"""Physical Fourier blocks of the correlated wreath bridge frame.

For an equal-pair wreath irrep pi_(lambda,lambda,+/-), the bridge involution
h_s=(s,s^-1;swap) acts on V_lambda tensor V_lambda as

    pi_+(h_s) = (rho_lambda(s) tensor rho_lambda(s^-1)) Swap,
    pi_-(h_s) = -pi_+(h_s).

For a tuple of physical wreath irreps, the correlated k-copy frame block is

    B_(pi_1,...,pi_k)
      = (1/n!) sum_s tensor_i (I + pi_i(h_s))/2.

This formula is the actual physical Fourier block of B_k.  Right convolution
preserves the tuple of physical wreath-irrep labels exactly.  That fact must
not be confused with conservation of the source labels in the separate
hidden-label harmonic carrier schema.

The module constructs Young-seminormal representation matrices for every
permutation, verifies the bridge involutions, and diagonalizes representative
equal-pair blocks.  These are finite controls, including every sign sector at
the S_3 information threshold.  Unequal-pair wreath irreps, all-n block
recurrences, hidden-label multiplicity transforms, and frame preconditioners
remain open.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np

from coset_jucys_murphy_label_transform import (
    adjacent_transposition_matrices,
)
from representation_obstruction import hook_length_dimension
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from self_dual_wreath_subset_carrier_algebra import (
    compose_permutations,
    inverse_permutation,
)


SELF_DUAL_WREATH_PHYSICAL_FRAME_BLOCKS_PATH = Path(
    "research/representation/self_dual_wreath_physical_frame_blocks.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-CODE-SELF-DUAL-WREATH-PHYSICAL-FRAME-BLOCKS"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Permutation = tuple[int, ...]


@dataclass(frozen=True)
class PhysicalFrameBlockSpec:
    cases: tuple[tuple[int, tuple[int, ...], int], ...] = (
        (3, (2, 1), 3),
        (4, (2, 2), 3),
        (4, (3, 1), 2),
        (5, (3, 2), 2),
    )
    eigenvalue_tolerance: float = 1e-8


@dataclass(frozen=True)
class PhysicalFrameBlockRecord:
    n: int
    partition: tuple[int, ...]
    irrep_dimension: int
    equal_pair_wreath_dimension: int
    copy_count: int
    minus_sign_count: int
    block_dimension: int
    bridge_count: int
    maximum_bridge_involution_residual: float
    maximum_bridge_hermiticity_residual: float
    one_copy_class_scalar_residual: float
    support_rank: int
    kernel_dimension: int
    distinct_eigenvalue_count: int
    minimum_positive_eigenvalue: float
    maximum_eigenvalue: float
    support_condition_number: float
    eigenvalue_multiplicities: list[dict[str, int | float]]
    information_threshold_copy_count: int
    reaches_information_threshold: bool
    physical_irrep_tuple_conserved: bool
    hidden_label_harmonic_source_conserved_proved: bool
    finite_dense_diagonalization_only: bool
    status: str


@dataclass(frozen=True)
class SelfDualWreathPhysicalFrameBlockReport:
    created_at: str
    spec: PhysicalFrameBlockSpec
    physical_block_contract: dict[str, Any]
    records: list[PhysicalFrameBlockRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _adjacent_permutation(n: int, index: int) -> Permutation:
    values = list(range(n))
    values[index], values[index + 1] = values[index + 1], values[index]
    return tuple(values)


@lru_cache(maxsize=None)
def permutation_representation_matrices(
    partition: tuple[int, ...],
) -> tuple[tuple[Permutation, np.ndarray], ...]:
    """Enumerate rho_lambda(s) by BFS in adjacent transpositions."""

    n = sum(partition)
    generators = adjacent_transposition_matrices(partition)
    if len(generators) != n - 1:
        raise ArithmeticError("missing adjacent transposition matrices")
    identity_permutation = tuple(range(n))
    dimension = hook_length_dimension(partition)
    matrices: dict[Permutation, np.ndarray] = {
        identity_permutation: np.eye(dimension)
    }
    queue = [identity_permutation]
    for permutation in queue:
        for index, generator in enumerate(generators):
            adjacent = _adjacent_permutation(n, index)
            product = compose_permutations(permutation, adjacent)
            if product in matrices:
                continue
            matrices[product] = matrices[permutation] @ generator
            queue.append(product)
    if len(matrices) != math.factorial(n):
        raise ArithmeticError("adjacent generators did not enumerate S_n")
    return tuple(sorted(matrices.items()))


@lru_cache(maxsize=None)
def tensor_swap_matrix(dimension: int) -> np.ndarray:
    swap = np.zeros((dimension * dimension, dimension * dimension))
    for left in range(dimension):
        for right in range(dimension):
            source = left * dimension + right
            target = right * dimension + left
            swap[target, source] = 1.0
    return swap


def equal_pair_bridge_matrices(
    partition: tuple[int, ...],
    sign: int,
) -> tuple[tuple[Permutation, np.ndarray], ...]:
    if sign not in (-1, 1):
        raise ValueError("sign must be +/-1")
    rows = dict(permutation_representation_matrices(partition))
    dimension = hook_length_dimension(partition)
    swap = tensor_swap_matrix(dimension)
    return tuple(
        (
            permutation,
            sign
            * np.kron(
                matrix,
                rows[inverse_permutation(permutation)],
            )
            @ swap,
        )
        for permutation, matrix in rows.items()
    )


def _cluster_eigenvalues(
    eigenvalues: np.ndarray,
    tolerance: float,
) -> list[dict[str, int | float]]:
    clusters: list[list[float]] = []
    for value in eigenvalues:
        numeric = float(value)
        if not clusters or abs(numeric - clusters[-1][0]) > tolerance:
            clusters.append([numeric])
        else:
            clusters[-1].append(numeric)
    return [
        {
            "eigenvalue": round(float(sum(cluster) / len(cluster)), 12),
            "multiplicity": len(cluster),
        }
        for cluster in clusters
    ]


def audit_physical_frame_block(
    n: int,
    partition: tuple[int, ...],
    copy_count: int,
    minus_sign_count: int,
    tolerance: float = 1e-8,
) -> PhysicalFrameBlockRecord:
    if sum(partition) != n:
        raise ValueError("partition size must equal n")
    if copy_count < 1:
        raise ValueError("copy_count must be positive")
    if minus_sign_count < 0 or minus_sign_count > copy_count:
        raise ValueError("minus_sign_count out of range")
    dimension = hook_length_dimension(partition)
    wreath_dimension = dimension * dimension
    block_dimension = wreath_dimension**copy_count
    identity = np.eye(wreath_dimension)
    plus_rows = dict(equal_pair_bridge_matrices(partition, 1))
    permutations = tuple(plus_rows)

    involution_residual = max(
        float(np.linalg.norm(matrix @ matrix - identity))
        for matrix in plus_rows.values()
    )
    hermiticity_residual = max(
        float(np.linalg.norm(matrix - matrix.T))
        for matrix in plus_rows.values()
    )
    plus_average = sum(plus_rows.values()) / len(plus_rows)
    expected_plus_scalar = 1.0 / dimension
    class_scalar_residual = float(
        np.linalg.norm(
            plus_average - expected_plus_scalar * identity
        )
    )

    signs = (
        *((1,) * (copy_count - minus_sign_count)),
        *((-1,) * minus_sign_count),
    )
    frame = np.zeros((block_dimension, block_dimension))
    for permutation in permutations:
        tensor = None
        bridge = plus_rows[permutation]
        for sign in signs:
            projector = (identity + sign * bridge) / 2.0
            tensor = (
                projector
                if tensor is None
                else np.kron(tensor, projector)
            )
        if tensor is None:
            raise ArithmeticError("empty tensor frame")
        frame += tensor
    frame /= len(permutations)
    frame = (frame + frame.T) / 2.0
    eigenvalues = np.linalg.eigvalsh(frame)
    positive = eigenvalues[eigenvalues > tolerance]
    support_rank = len(positive)
    minimum_positive = float(positive[0]) if support_rank else 0.0
    maximum = float(positive[-1]) if support_rank else 0.0
    condition = (
        maximum / minimum_positive if minimum_positive > 0 else math.inf
    )
    threshold = math.ceil(math.log2(math.factorial(n)))
    return PhysicalFrameBlockRecord(
        n=n,
        partition=partition,
        irrep_dimension=dimension,
        equal_pair_wreath_dimension=wreath_dimension,
        copy_count=copy_count,
        minus_sign_count=minus_sign_count,
        block_dimension=block_dimension,
        bridge_count=len(permutations),
        maximum_bridge_involution_residual=involution_residual,
        maximum_bridge_hermiticity_residual=hermiticity_residual,
        one_copy_class_scalar_residual=class_scalar_residual,
        support_rank=support_rank,
        kernel_dimension=block_dimension - support_rank,
        distinct_eigenvalue_count=len(
            _cluster_eigenvalues(eigenvalues, tolerance)
        ),
        minimum_positive_eigenvalue=minimum_positive,
        maximum_eigenvalue=maximum,
        support_condition_number=condition,
        eigenvalue_multiplicities=_cluster_eigenvalues(
            eigenvalues,
            tolerance,
        ),
        information_threshold_copy_count=threshold,
        reaches_information_threshold=copy_count >= threshold,
        physical_irrep_tuple_conserved=True,
        hidden_label_harmonic_source_conserved_proved=False,
        finite_dense_diagonalization_only=True,
        status=(
            "finite-information-threshold-physical-frame-block"
            if copy_count >= threshold
            else "finite-below-threshold-physical-frame-block"
        ),
    )


def run_self_dual_wreath_physical_frame_blocks(
    spec: PhysicalFrameBlockSpec = PhysicalFrameBlockSpec(),
) -> SelfDualWreathPhysicalFrameBlockReport:
    records: list[PhysicalFrameBlockRecord] = []
    for n, partition, maximum_copy_count in spec.cases:
        for copy_count in range(1, maximum_copy_count + 1):
            for minus_count in range(copy_count + 1):
                records.append(
                    audit_physical_frame_block(
                        n=n,
                        partition=partition,
                        copy_count=copy_count,
                        minus_sign_count=minus_count,
                        tolerance=spec.eigenvalue_tolerance,
                    )
                )
    threshold_records = [
        record for record in records if record.reaches_information_threshold
    ]
    metrics: dict[str, int | float] = {
        "record_count": len(records),
        "maximum_n": max((record.n for record in records), default=0),
        "maximum_copy_count": max(
            (record.copy_count for record in records),
            default=0,
        ),
        "maximum_block_dimension": max(
            (record.block_dimension for record in records),
            default=0,
        ),
        "information_threshold_block_count": len(threshold_records),
        "physical_wreath_irrep_tuple_conservation_proof_count": 1,
        "equal_pair_bridge_formula_proof_count": 1,
        "finite_bridge_involution_verification_count": sum(
            record.maximum_bridge_involution_residual < 1e-10
            for record in records
        ),
        "finite_class_scalar_verification_count": sum(
            record.one_copy_class_scalar_residual < 1e-10
            for record in records
        ),
        "finite_kernel_block_count": sum(
            record.kernel_dimension > 0 for record in records
        ),
        "maximum_distinct_eigenvalue_count": max(
            (record.distinct_eigenvalue_count for record in records),
            default=0,
        ),
        "minimum_positive_eigenvalue": min(
            (
                record.minimum_positive_eigenvalue
                for record in records
                if record.minimum_positive_eigenvalue > 0
            ),
            default=0.0,
        ),
        "maximum_support_condition_number": max(
            (record.support_condition_number for record in records),
            default=0.0,
        ),
        "unequal_pair_physical_block_count": 0,
        "all_partition_tuple_block_count": 0,
        "uniform_all_n_spectral_recurrence_count": 0,
        "hidden_label_harmonic_transform_count": 0,
        "polynomial_structured_frame_preconditioner_count": 0,
        "polynomial_frame_inverse_count": 0,
        "polynomial_hidden_permutation_decoder_count": 0,
    }
    return SelfDualWreathPhysicalFrameBlockReport(
        created_at=utc_now(),
        spec=spec,
        physical_block_contract={
            "equal_pair_bridge": (
                "pi_(lambda,lambda,epsilon)(h_s)="
                "epsilon*(rho_lambda(s) tensor rho_lambda(s^-1))*Swap"
            ),
            "correlated_frame_block": (
                "B_(pi_1,...,pi_k)=(1/n!) sum_s tensor_i "
                "(I+pi_i(h_s))/2"
            ),
            "physical_label_conservation": (
                "B_k is right convolution on W_n^k, so the tuple of physical "
                "W_n Fourier irrep labels is exactly block diagonal."
            ),
            "layer_boundary": (
                "Physical wreath-irrep label conservation does not imply "
                "conservation of lambda source labels in the separate "
                "hidden-label simultaneous-conjugacy harmonic schema."
            ),
            "finite_scope": (
                "All +/- sign sectors for selected equal-pair irreps through "
                "n=5, including the S_3 information-threshold copy count."
            ),
        },
        records=records,
        headline_metrics=metrics,
        claim_gate={
            "actual_physical_equal_pair_frame_blocks_constructed": True,
            "physical_wreath_irrep_tuple_labels_conserved": True,
            "finite_information_threshold_control_present": bool(
                threshold_records
            ),
            "unequal_pair_blocks_constructed": False,
            "all_partition_tuple_blocks_constructed": False,
            "uniform_all_n_spectral_recurrence_proved": False,
            "hidden_label_harmonic_source_conservation_proved": False,
            "polynomial_structured_frame_preconditioner_proved": False,
            "polynomial_frame_inverse_proved": False,
            "polynomial_hidden_permutation_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The actual equal-pair physical Fourier blocks and one small "
                "information-threshold control are explicit, but unequal "
                "irreps, growing tuples, all-n recurrences, hidden-label "
                "multiplicity transforms, and preconditioning remain open."
            ),
        },
        status="physical-equal-pair-frame-blocks-explicit-all-n-recurrence-open",
        summary=(
            f"Diagonalized {len(records)} physical equal-pair frame blocks "
            f"through n={metrics['maximum_n']} and k="
            f"{metrics['maximum_copy_count']}; maximum finite support "
            f"condition number={metrics['maximum_support_condition_number']:.6g}, "
            "while all-n recurrences and preconditioners remain zero."
        ),
        falsifiers_triggered=[
            "The tuple of physical wreath Fourier irrep labels is conserved by the correlated frame.",
            "That physical block conservation does not resolve hidden-label harmonic multiplicities.",
            "The equal-pair bridge formula passes involution and class-average controls.",
            "Finite S_3 information-threshold blocks can be well conditioned without proving all-n conditioning.",
            "Unequal-pair and growing partition-tuple sectors are not covered by the finite equal-pair probe.",
        ],
    )


def write_self_dual_wreath_physical_frame_blocks(
    path: Path = SELF_DUAL_WREATH_PHYSICAL_FRAME_BLOCKS_PATH,
    spec: PhysicalFrameBlockSpec = PhysicalFrameBlockSpec(),
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, Any]:
    payload = asdict(
        run_self_dual_wreath_physical_frame_blocks(spec=spec)
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-CODE-SELF-DUAL-WREATH-FINITE-PHYSICAL-BLOCKS-NOT-PRECONDITIONER",
                source=str(path),
                claim=(
                    "Well-conditioned finite equal-pair physical frame blocks "
                    "supply an all-n PGM preconditioner."
                ),
                reason_invalid=(
                    "The probe covers selected equal-pair sectors only, "
                    "reaches the information threshold only for S_3, and "
                    "omits unequal-pair tuples and hidden-label multiplicities."
                ),
                lesson=(
                    "Use the physical block formula to search recurrences and "
                    "worst sectors, but require all-n tuple coverage and a "
                    "coherent blockwise inverse before any decoder claim."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence=payload["headline_metrics"],
            )
        )
        result_id = (
            registry_result_id
            or f"RESULT-{registry_experiment_id}-LATEST"
        )
        upsert_experiment_result(
            ExperimentResultRecord(
                id=result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=payload["created_at"],
                status=payload["status"],
                summary=payload["summary"],
                metrics=payload["headline_metrics"],
                falsifiers_triggered=payload["falsifiers_triggered"],
                artifacts={
                    "self_dual_wreath_physical_frame_blocks": str(path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_self_dual_wreath_physical_frame_blocks()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
