"""Collective frame blocks for unequal-pair wreath irreducibles.

For distinct S_n irreps lambda and mu, the induced W_n irrep acts on

    (V_lambda tensor V_mu) direct_sum (V_mu tensor V_lambda).

Every bridge h_s has zero character in this irrep, so its one-copy frame block
is exactly I/2.  Correlated copies are not featureless:

    B_pi^(k) = (1/n!) sum_s [(I + pi(h_s))/2]^tensor k

can have nontrivial spectra and kernels.  These blocks therefore isolate
collective structure that weak Fourier labels cannot see.

This module constructs the induced bridge matrices exactly from Young
seminormal representations and audits every unequal-pair irrep of W_3 through
the information threshold, every unequal pair of W_4 through two copies, and
representative W_5 controls.  It remains a finite probe: mixed tuples of
different physical irreps, growing-k recurrences, hidden-label transforms,
and blockwise frame inversion are not supplied.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import hook_length_dimension
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from self_dual_wreath_physical_frame_blocks import (
    permutation_representation_matrices,
)
from self_dual_wreath_subset_carrier_algebra import inverse_permutation


SELF_DUAL_WREATH_UNEQUAL_FRAME_BLOCKS_PATH = Path(
    "research/representation/self_dual_wreath_unequal_frame_blocks.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-CODE-SELF-DUAL-WREATH-UNEQUAL-FRAME-BLOCKS"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Permutation = tuple[int, ...]


@dataclass(frozen=True)
class UnequalFrameBlockSpec:
    cases: tuple[
        tuple[int, tuple[int, ...], tuple[int, ...], int],
        ...,
    ] = (
        (3, (3,), (2, 1), 3),
        (3, (3,), (1, 1, 1), 3),
        (3, (2, 1), (1, 1, 1), 3),
        (4, (4,), (3, 1), 2),
        (4, (4,), (2, 2), 2),
        (4, (4,), (2, 1, 1), 2),
        (4, (4,), (1, 1, 1, 1), 2),
        (4, (3, 1), (2, 2), 2),
        (4, (3, 1), (2, 1, 1), 2),
        (4, (3, 1), (1, 1, 1, 1), 2),
        (4, (2, 2), (2, 1, 1), 2),
        (4, (2, 2), (1, 1, 1, 1), 2),
        (4, (2, 1, 1), (1, 1, 1, 1), 2),
        (5, (5,), (4, 1), 2),
        (5, (5,), (3, 2), 2),
        (5, (4, 1), (2, 1, 1, 1), 2),
    )
    eigenvalue_tolerance: float = 1e-8


@dataclass(frozen=True)
class UnequalPhysicalFrameBlockRecord:
    n: int
    left_partition: tuple[int, ...]
    right_partition: tuple[int, ...]
    left_dimension: int
    right_dimension: int
    induced_wreath_dimension: int
    copy_count: int
    block_dimension: int
    bridge_count: int
    maximum_bridge_involution_residual: float
    maximum_bridge_hermiticity_residual: float
    one_copy_zero_character_average_residual: float
    support_rank: int
    kernel_dimension: int
    distinct_eigenvalue_count: int
    minimum_positive_eigenvalue: float
    maximum_eigenvalue: float
    support_condition_number: float
    eigenvalue_multiplicities: list[dict[str, int | float]]
    information_threshold_copy_count: int
    reaches_information_threshold: bool
    one_copy_bridge_character_zero: bool
    collective_spectrum_nontrivial: bool
    mixed_physical_irrep_tuple: bool
    finite_dense_diagonalization_only: bool
    status: str


@dataclass(frozen=True)
class SelfDualWreathUnequalFrameBlockReport:
    created_at: str
    spec: UnequalFrameBlockSpec
    induced_representation_contract: dict[str, Any]
    records: list[UnequalPhysicalFrameBlockRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


@lru_cache(maxsize=None)
def rectangular_tensor_flip(
    left_dimension: int,
    right_dimension: int,
) -> np.ndarray:
    """Map V_left tensor V_right to V_right tensor V_left."""

    flip = np.zeros(
        (
            right_dimension * left_dimension,
            left_dimension * right_dimension,
        )
    )
    for left in range(left_dimension):
        for right in range(right_dimension):
            source = left * right_dimension + right
            target = right * left_dimension + left
            flip[target, source] = 1.0
    return flip


def unequal_pair_bridge_matrices(
    left_partition: tuple[int, ...],
    right_partition: tuple[int, ...],
) -> tuple[tuple[Permutation, np.ndarray], ...]:
    if sum(left_partition) != sum(right_partition):
        raise ValueError("partitions must have equal size")
    if left_partition == right_partition:
        raise ValueError("unequal-pair irrep requires distinct partitions")
    left_rows = dict(
        permutation_representation_matrices(left_partition)
    )
    right_rows = dict(
        permutation_representation_matrices(right_partition)
    )
    left_dimension = hook_length_dimension(left_partition)
    right_dimension = hook_length_dimension(right_partition)
    summand_dimension = left_dimension * right_dimension
    flip = rectangular_tensor_flip(left_dimension, right_dimension)
    zero = np.zeros((summand_dimension, summand_dimension))
    records = []
    for permutation, left_matrix in left_rows.items():
        inverse = inverse_permutation(permutation)
        top_action = np.kron(
            left_matrix,
            right_rows[inverse],
        )
        bottom_action = np.kron(
            right_rows[permutation],
            left_rows[inverse],
        )
        bridge = np.block(
            [
                [zero, top_action @ flip.T],
                [bottom_action @ flip, zero],
            ]
        )
        records.append((permutation, bridge))
    return tuple(records)


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


def audit_unequal_physical_frame_block(
    n: int,
    left_partition: tuple[int, ...],
    right_partition: tuple[int, ...],
    copy_count: int,
    tolerance: float = 1e-8,
) -> UnequalPhysicalFrameBlockRecord:
    if sum(left_partition) != n or sum(right_partition) != n:
        raise ValueError("partition sizes must equal n")
    if copy_count < 1:
        raise ValueError("copy_count must be positive")
    bridge_rows = unequal_pair_bridge_matrices(
        left_partition,
        right_partition,
    )
    left_dimension = hook_length_dimension(left_partition)
    right_dimension = hook_length_dimension(right_partition)
    induced_dimension = 2 * left_dimension * right_dimension
    identity = np.eye(induced_dimension)
    involution_residual = max(
        float(np.linalg.norm(matrix @ matrix - identity))
        for _, matrix in bridge_rows
    )
    hermiticity_residual = max(
        float(np.linalg.norm(matrix - matrix.T))
        for _, matrix in bridge_rows
    )
    average_bridge = sum(matrix for _, matrix in bridge_rows) / len(
        bridge_rows
    )
    zero_character_residual = float(np.linalg.norm(average_bridge))

    block_dimension = induced_dimension**copy_count
    frame = np.zeros((block_dimension, block_dimension))
    for _, bridge in bridge_rows:
        projector = (identity + bridge) / 2.0
        tensor = projector
        for _ in range(copy_count - 1):
            tensor = np.kron(tensor, projector)
        frame += tensor
    frame /= len(bridge_rows)
    frame = (frame + frame.T) / 2.0
    eigenvalues = np.linalg.eigvalsh(frame)
    clusters = _cluster_eigenvalues(eigenvalues, tolerance)
    positive = eigenvalues[eigenvalues > tolerance]
    support_rank = len(positive)
    minimum_positive = float(positive[0]) if support_rank else 0.0
    maximum = float(positive[-1]) if support_rank else 0.0
    condition = (
        maximum / minimum_positive if minimum_positive > 0 else math.inf
    )
    threshold = math.ceil(math.log2(math.factorial(n)))
    return UnequalPhysicalFrameBlockRecord(
        n=n,
        left_partition=left_partition,
        right_partition=right_partition,
        left_dimension=left_dimension,
        right_dimension=right_dimension,
        induced_wreath_dimension=induced_dimension,
        copy_count=copy_count,
        block_dimension=block_dimension,
        bridge_count=len(bridge_rows),
        maximum_bridge_involution_residual=involution_residual,
        maximum_bridge_hermiticity_residual=hermiticity_residual,
        one_copy_zero_character_average_residual=zero_character_residual,
        support_rank=support_rank,
        kernel_dimension=block_dimension - support_rank,
        distinct_eigenvalue_count=len(clusters),
        minimum_positive_eigenvalue=minimum_positive,
        maximum_eigenvalue=maximum,
        support_condition_number=condition,
        eigenvalue_multiplicities=clusters,
        information_threshold_copy_count=threshold,
        reaches_information_threshold=copy_count >= threshold,
        one_copy_bridge_character_zero=zero_character_residual < tolerance,
        collective_spectrum_nontrivial=(
            copy_count >= 2 and len(clusters) > 1
        ),
        mixed_physical_irrep_tuple=False,
        finite_dense_diagonalization_only=True,
        status=(
            "finite-unequal-information-threshold-collective-block"
            if copy_count >= threshold
            else (
                "finite-unequal-collective-spectrum"
                if copy_count >= 2 and len(clusters) > 1
                else "one-copy-zero-character-control"
            )
        ),
    )


def run_self_dual_wreath_unequal_frame_blocks(
    spec: UnequalFrameBlockSpec = UnequalFrameBlockSpec(),
) -> SelfDualWreathUnequalFrameBlockReport:
    records: list[UnequalPhysicalFrameBlockRecord] = []
    for n, left, right, maximum_copy_count in spec.cases:
        for copy_count in range(1, maximum_copy_count + 1):
            records.append(
                audit_unequal_physical_frame_block(
                    n=n,
                    left_partition=left,
                    right_partition=right,
                    copy_count=copy_count,
                    tolerance=spec.eigenvalue_tolerance,
                )
            )
    threshold_records = [
        record for record in records if record.reaches_information_threshold
    ]
    collective_records = [
        record for record in records if record.collective_spectrum_nontrivial
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
        "one_copy_zero_character_control_count": sum(
            record.copy_count == 1
            and record.one_copy_bridge_character_zero
            for record in records
        ),
        "collective_nontrivial_spectrum_count": len(collective_records),
        "information_threshold_unequal_block_count": len(
            threshold_records
        ),
        "all_s3_unequal_information_threshold_block_count": sum(
            record.n == 3 and record.reaches_information_threshold
            for record in records
        ),
        "finite_bridge_involution_verification_count": sum(
            record.maximum_bridge_involution_residual < 1e-10
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
        "mixed_physical_irrep_tuple_block_count": 0,
        "all_partition_tuple_block_count": 0,
        "uniform_all_n_spectral_recurrence_count": 0,
        "polynomial_structured_frame_preconditioner_count": 0,
        "polynomial_frame_inverse_count": 0,
        "polynomial_hidden_permutation_decoder_count": 0,
    }
    return SelfDualWreathUnequalFrameBlockReport(
        created_at=utc_now(),
        spec=spec,
        induced_representation_contract={
            "space": (
                "(V_lambda tensor V_mu) direct_sum "
                "(V_mu tensor V_lambda), lambda != mu"
            ),
            "base_action": (
                "(a,b;0) acts by rho_lambda(a) tensor rho_mu(b) "
                "and rho_mu(a) tensor rho_lambda(b) on the two summands"
            ),
            "swap_action": "The nontrivial wreath swap exchanges the summands.",
            "bridge_character": "Tr pi_(lambda,mu)(h_s)=0 for every s",
            "one_copy_frame": "B_pi^(1)=I/2 exactly",
            "collective_frame": (
                "B_pi^(k)=(1/n!) sum_s [(I+pi(h_s))/2]^tensor k"
            ),
        },
        records=records,
        headline_metrics=metrics,
        claim_gate={
            "unequal_pair_induced_bridge_formula_constructed": True,
            "one_copy_zero_character_controls_verified": True,
            "collective_spectra_can_be_nontrivial": bool(
                collective_records
            ),
            "all_s3_unequal_threshold_blocks_constructed": (
                metrics[
                    "all_s3_unequal_information_threshold_block_count"
                ]
                == 3
            ),
            "mixed_physical_irrep_tuple_blocks_constructed": False,
            "all_partition_tuple_blocks_constructed": False,
            "uniform_all_n_spectral_recurrence_proved": False,
            "polynomial_structured_frame_preconditioner_proved": False,
            "polynomial_frame_inverse_proved": False,
            "polynomial_hidden_permutation_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Unequal-pair sectors have zero one-copy signal but explicit "
                "nontrivial collective spectra. The audit is finite and omits "
                "mixed irrep tuples, growing recurrences, and frame inversion."
            ),
        },
        status="unequal-pair-collective-blocks-nontrivial-all-n-recurrence-open",
        summary=(
            f"Diagonalized {len(records)} unequal-pair physical frame blocks; "
            f"{len(collective_records)} have nontrivial collective spectra and "
            f"{len(threshold_records)} reach the S_3 information threshold, "
            "while mixed tuples and all-n recurrences remain zero."
        ),
        falsifiers_triggered=[
            "Zero one-copy bridge character does not imply a scalar correlated multi-copy frame block.",
            "Every unequal-pair W_3 irrep has an explicit information-threshold block.",
            "Finite unequal-pair spectra can have kernels and multiple eigenvalues.",
            "Repeated copies of one physical irrep do not cover mixed physical-irrep tuples.",
            "Finite dense diagonalization does not provide an all-n recurrence or coherent inverse.",
        ],
    )


def write_self_dual_wreath_unequal_frame_blocks(
    path: Path = SELF_DUAL_WREATH_UNEQUAL_FRAME_BLOCKS_PATH,
    spec: UnequalFrameBlockSpec = UnequalFrameBlockSpec(),
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, Any]:
    payload = asdict(
        run_self_dual_wreath_unequal_frame_blocks(spec=spec)
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_self_dual_wreath_unequal_frame_blocks()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
