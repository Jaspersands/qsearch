"""Matrix-free frame probe for globally collision-free unequal tuples.

The global source-law reduction shows that natural threshold tuples have
2k distinct source partitions with probability 1-o(1).  This module asks the
first spectral question on that restricted domain:

    B = (1/n!) sum_s tensor_i (I + pi_i(h_s))/2

for unequal physical irreps pi_i whose left and right source partitions are
all distinct.

The complete W_4, k=2 portfolio and a deterministic W_5, k=3 portfolio are
small enough for matrix-free Lanczos diagonalization.  At k=3 the natural
frame scale suggested by the second moment is 2^{1-k}=1/4.  The finite probes
slightly violate the exact 1/4 bound but remain within a small constant
factor.  This falsifies an exact projector-independence conjecture while
preserving the higher-value target

    ||B|| <= poly(n) 2^{-k}

for arbitrary globally distinct source tuples.  No asymptotic theorem is
claimed.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable

import numpy as np
from scipy.sparse.linalg import LinearOperator, eigsh

from representation_obstruction import (
    hook_length_dimension,
    integer_partitions,
)
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from self_dual_wreath_unequal_frame_blocks import (
    unequal_pair_bridge_matrices,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_collision_free_frame_probe.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-COLLISION-FREE-FRAME-PROBE"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Label = tuple[Partition, Partition]


@dataclass(frozen=True)
class CollisionFreeFrameProbeRecord:
    n: int
    copy_count: int
    labels: tuple[Label, ...]
    source_partitions: tuple[Partition, ...]
    source_dimensions: tuple[int, ...]
    block_dimensions: tuple[int, ...]
    total_block_dimension: int
    all_source_partitions_distinct: bool
    top_eigenvalue: float
    top_eigenpair_residual: float
    target_two_to_one_minus_k: float
    top_to_target_ratio: float
    log2_top_to_target_ratio: float
    exact_target_bound_satisfied: bool
    factor_two_target_bound_satisfied: bool
    matrix_free_lanczos_used: bool
    finite_probe_only: bool
    status: str


@dataclass(frozen=True)
class CollisionFreeFrameProbeReport:
    created_at: str
    probe_contract: dict[str, Any]
    records: list[CollisionFreeFrameProbeRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def perfect_matchings(
    partitions: tuple[Partition, ...],
) -> tuple[tuple[Label, ...], ...]:
    if len(partitions) % 2:
        raise ValueError("partition count must be even")
    if not partitions:
        return ((),)
    first = partitions[0]
    output: list[tuple[Label, ...]] = []
    for index in range(1, len(partitions)):
        second = partitions[index]
        remainder = partitions[1:index] + partitions[index + 1 :]
        for tail in perfect_matchings(remainder):
            output.append(((first, second),) + tail)
    return tuple(output)


@lru_cache(maxsize=None)
def _bridge_tables(
    labels: tuple[Label, ...],
) -> tuple[tuple[np.ndarray, ...], ...]:
    tables = [
        dict(unequal_pair_bridge_matrices(left, right))
        for left, right in labels
    ]
    permutations = tuple(tables[0])
    return tuple(
        tuple(tables[index][permutation] for index in range(len(labels)))
        for permutation in permutations
    )


def _apply_kronecker(
    matrices: tuple[np.ndarray, ...],
    vector: np.ndarray,
    dimensions: tuple[int, ...],
) -> np.ndarray:
    tensor = vector.reshape(dimensions)
    for axis, matrix in enumerate(matrices):
        tensor = np.tensordot(matrix, tensor, axes=(1, axis))
        tensor = np.moveaxis(tensor, 0, axis)
    return tensor.reshape(-1)


def collision_free_frame_operator(
    labels: tuple[Label, ...],
) -> tuple[LinearOperator, tuple[int, ...]]:
    if not labels:
        raise ValueError("labels must be nonempty")
    source = tuple(partition for label in labels for partition in label)
    if len(source) != len(set(source)):
        raise ValueError("source partitions must be globally distinct")
    bridge_rows = _bridge_tables(labels)
    dimensions = tuple(row.shape[0] for row in bridge_rows[0])
    projectors = tuple(
        tuple(
            (np.eye(dimension) + matrix) / 2.0
            for dimension, matrix in zip(dimensions, row)
        )
        for row in bridge_rows
    )
    total_dimension = math.prod(dimensions)

    def matvec(vector: np.ndarray) -> np.ndarray:
        output = np.zeros_like(vector)
        for row in projectors:
            output += _apply_kronecker(row, vector, dimensions)
        return output / len(projectors)

    return (
        LinearOperator(
            (total_dimension, total_dimension),
            matvec=matvec,
            rmatvec=matvec,
            dtype=float,
        ),
        dimensions,
    )


def audit_collision_free_frame_tuple(
    n: int,
    labels: tuple[Label, ...],
    tolerance: float = 1e-9,
) -> CollisionFreeFrameProbeRecord:
    source = tuple(partition for label in labels for partition in label)
    if any(sum(partition) != n for partition in source):
        raise ValueError("every partition must have size n")
    operator, dimensions = collision_free_frame_operator(labels)
    rng = np.random.default_rng(20260729)
    initial = rng.normal(size=operator.shape[0])
    eigenvalues, eigenvectors = eigsh(
        operator,
        k=1,
        which="LA",
        v0=initial,
        tol=tolerance,
        maxiter=4000,
    )
    top = float(eigenvalues[0])
    vector = eigenvectors[:, 0]
    residual = float(np.linalg.norm(operator @ vector - top * vector))
    copy_count = len(labels)
    target = 2 ** (1 - copy_count)
    ratio = top / target
    return CollisionFreeFrameProbeRecord(
        n=n,
        copy_count=copy_count,
        labels=labels,
        source_partitions=source,
        source_dimensions=tuple(
            hook_length_dimension(partition) for partition in source
        ),
        block_dimensions=dimensions,
        total_block_dimension=math.prod(dimensions),
        all_source_partitions_distinct=len(source) == len(set(source)),
        top_eigenvalue=top,
        top_eigenpair_residual=residual,
        target_two_to_one_minus_k=target,
        top_to_target_ratio=ratio,
        log2_top_to_target_ratio=math.log2(ratio),
        exact_target_bound_satisfied=top <= target + 10 * tolerance,
        factor_two_target_bound_satisfied=top <= 2 * target + 10 * tolerance,
        matrix_free_lanczos_used=True,
        finite_probe_only=True,
        status=(
            "finite-collision-free-exact-target"
            if top <= target + 10 * tolerance
            else "finite-collision-free-constant-factor-target"
        ),
    )


def _w4_complete_labels() -> tuple[tuple[Label, ...], ...]:
    partitions = integer_partitions(4)
    return tuple(
        labels
        for subset in itertools.combinations(partitions, 4)
        for labels in perfect_matchings(subset)
    )


def _w5_probe_labels() -> tuple[tuple[Label, ...], ...]:
    partitions = integer_partitions(5)
    maximum_dimension = max(
        hook_length_dimension(partition) for partition in partitions
    )
    minimum_block_subset = tuple(
        partition
        for partition in partitions
        if hook_length_dimension(partition) != maximum_dimension
    )
    complete_minimum_block = perfect_matchings(minimum_block_subset)
    omitted_partition_probes = []
    for omitted_index in range(len(partitions)):
        selected = (
            partitions[:omitted_index]
            + partitions[omitted_index + 1 :]
        )
        omitted_partition_probes.append(
            (
                (selected[0], selected[1]),
                (selected[2], selected[3]),
                (selected[4], selected[5]),
            )
        )
    return tuple(
        dict.fromkeys(
            complete_minimum_block + tuple(omitted_partition_probes)
        )
    )


def run_collision_free_frame_probe() -> CollisionFreeFrameProbeReport:
    labels = (
        tuple((4, item) for item in _w4_complete_labels())
        + tuple((5, item) for item in _w5_probe_labels())
    )
    records = [
        audit_collision_free_frame_tuple(n, item)
        for n, item in labels
    ]
    w5 = [record for record in records if record.n == 5]
    maximum_ratio = max(record.top_to_target_ratio for record in w5)
    maximum_residual = max(
        record.top_eigenpair_residual for record in records
    )
    metrics: dict[str, int | float] = {
        "collision_free_probe_count": len(records),
        "complete_w4_collision_free_pairing_count": sum(
            record.n == 4 for record in records
        ),
        "w5_collision_free_three_copy_probe_count": len(w5),
        "maximum_probe_block_dimension": max(
            record.total_block_dimension for record in records
        ),
        "maximum_top_eigenpair_residual": maximum_residual,
        "w5_exact_two_to_one_minus_k_violation_count": sum(
            not record.exact_target_bound_satisfied for record in w5
        ),
        "w5_factor_two_target_bound_success_count": sum(
            record.factor_two_target_bound_satisfied for record in w5
        ),
        "maximum_w5_top_to_target_ratio": maximum_ratio,
        "maximum_w5_log2_top_to_target_ratio": math.log2(maximum_ratio),
        "finite_collision_free_constant_factor_signal_count": sum(
            record.factor_two_target_bound_satisfied for record in w5
        ),
        "collision_free_polynomial_factor_norm_theorem_count": 0,
        "collision_free_growing_moment_contraction_count": 0,
        "natural_average_inverse_polynomial_conclusive_theorem_count": 0,
        "structured_maximal_effect_dilation_count": 0,
        "polynomial_hidden_permutation_decoder_count": 0,
    }
    return CollisionFreeFrameProbeReport(
        created_at=utc_now(),
        probe_contract={
            "frame": (
                "B=(1/n!) sum_s tensor_i(I+pi_i(h_s))/2 for unequal "
                "physical labels with globally distinct source partitions"
            ),
            "finite_target": "compare ||B|| with 2^{1-k}",
            "numerical_method": (
                "matrix-free Hermitian Lanczos with deterministic initial "
                "vector and explicit eigenpair residual"
            ),
            "portfolio": (
                "complete W4 k=2 collision-free pairings; all perfect "
                "matchings of the minimum-dimension W5 six-partition subset "
                "plus one deterministic probe for every omitted partition"
            ),
            "asymptotic_target": (
                "prove ||B||<=poly(n)2^-k for arbitrary globally distinct "
                "source tuples"
            ),
        },
        records=records,
        headline_metrics=metrics,
        claim_gate={
            "collision_free_mixed_tuple_operator_constructed": True,
            "complete_w4_collision_free_portfolio_audited": True,
            "w5_three_copy_collision_free_portfolio_audited": True,
            "exact_two_to_one_minus_k_bound_survives_finite_probes": (
                metrics["w5_exact_two_to_one_minus_k_violation_count"] == 0
            ),
            "factor_two_target_bound_survives_finite_probes": (
                metrics["w5_factor_two_target_bound_success_count"]
                == len(w5)
            ),
            "collision_free_polynomial_factor_norm_bound_proved": False,
            "collision_free_growing_moment_contraction_proved": False,
            "natural_average_inverse_polynomial_conclusive_proved": False,
            "structured_maximal_effect_dilation_proved": False,
            "polynomial_hidden_permutation_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Finite collision-free tuples stay near the 2^{1-k} scale "
                "but slightly violate the exact bound. No all-n polynomial-"
                "factor norm theorem or coherent measurement follows."
            ),
        },
        status=(
            "finite-collision-free-constant-factor-signal-"
            "all-n-norm-theorem-open"
        ),
        summary=(
            f"Audited {len(records)} collision-free mixed tuples with "
            f"eigenpair residual at most {maximum_residual:.3g}; every W5 "
            "probe lies within factor "
            f"{maximum_ratio:.6g} of the 2^(1-k) target, but exact equality "
            "is false."
        ),
        falsifiers_triggered=[
            "Global partition distinctness does not make the frame exactly independent.",
            "The exact ||B||<=2^{1-k} conjecture fails on finite W5 collision-free tuples.",
            "All audited W5 collision-free tuples remain within a small constant factor of 2^{1-k}.",
            "Finite matrix-free spectra do not establish an all-n polynomial-factor norm theorem.",
            "A spectral norm signal is not a coherent maximal-effect circuit or hidden-permutation decoder.",
        ],
    )


def write_collision_free_frame_probe_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, Any]:
    payload = asdict(run_collision_free_frame_probe())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_collision_free_frame_probe_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
