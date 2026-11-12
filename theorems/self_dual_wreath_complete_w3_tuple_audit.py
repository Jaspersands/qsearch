"""Complete physical-irrep tuple audit for W_3 at the copy threshold.

W_3=(S_3 x S_3) semidirect C_2 has nine irreducible representations:
six equal-pair +/- extensions and three unequal-pair induced irreps.  The
hidden bridge ensemble has size 3!=6, so the information threshold is three
copies.

This module constructs all nine bridge representations and diagonalizes every
unordered three-irrep tuple block, 165 blocks in total.  It also computes the
exact weak-Fourier/coset-state label probability

    p_pi = d_pi [d_pi + chi_pi(h)] / |W_3|,

and the multinomial mass of each unordered tuple.  Two one-dimensional
minus extensions have zero natural mass.  The remaining 84 tuples carry all
mass and provide a complete finite worst-sector conditioning control.

This is not an asymptotic result.  A complete W_3 table does not provide
all-n character recurrences, a coherent blockwise inverse, a hidden-label
harmonic transform, or a hidden-permutation decoder.
"""

from __future__ import annotations

import itertools
import json
import math
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

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
from self_dual_wreath_physical_frame_blocks import (
    equal_pair_bridge_matrices,
)
from self_dual_wreath_unequal_frame_blocks import (
    unequal_pair_bridge_matrices,
)


SELF_DUAL_WREATH_COMPLETE_W3_TUPLE_PATH = Path(
    "research/representation/self_dual_wreath_complete_w3_tuple_audit.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-CODE-SELF-DUAL-WREATH-COMPLETE-W3-TUPLES"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Permutation = tuple[int, ...]


@dataclass(frozen=True)
class W3PhysicalIrrepRecord:
    id: str
    kind: str
    left_partition: tuple[int, ...]
    right_partition: tuple[int, ...]
    sign: int | None
    dimension: int
    bridge_character: int
    natural_label_probability: float
    naturally_occupied: bool


@dataclass(frozen=True)
class W3TupleFrameRecord:
    label_ids: tuple[str, str, str]
    label_indices: tuple[int, int, int]
    tuple_orbit_multiplicity: int
    aggregate_natural_probability: float
    naturally_occupied: bool
    block_dimension: int
    support_rank: int
    kernel_dimension: int
    distinct_eigenvalue_count: int
    minimum_positive_eigenvalue: float | None
    maximum_eigenvalue: float | None
    support_condition_number: float | None
    eigenvalue_multiplicities: list[dict[str, int | float]]
    status: str


@dataclass(frozen=True)
class CompleteW3TupleAuditReport:
    created_at: str
    group_contract: dict[str, Any]
    irrep_records: list[W3PhysicalIrrepRecord]
    tuple_records: list[W3TupleFrameRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _cluster_eigenvalues(
    eigenvalues: np.ndarray,
    tolerance: float = 1e-8,
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


def w3_physical_irreps() -> tuple[
    list[W3PhysicalIrrepRecord],
    list[dict[Permutation, np.ndarray]],
]:
    n = 3
    order = 2 * math.factorial(n) ** 2
    partitions = integer_partitions(n)
    records: list[W3PhysicalIrrepRecord] = []
    bridges: list[dict[Permutation, np.ndarray]] = []
    for partition in partitions:
        source_dimension = hook_length_dimension(partition)
        dimension = source_dimension * source_dimension
        for sign in (1, -1):
            character = sign * source_dimension
            probability = (
                dimension * (dimension + character) / order
            )
            records.append(
                W3PhysicalIrrepRecord(
                    id=(
                        "EQ-"
                        + "-".join(map(str, partition))
                        + ("-PLUS" if sign > 0 else "-MINUS")
                    ),
                    kind="equal-pair-extension",
                    left_partition=partition,
                    right_partition=partition,
                    sign=sign,
                    dimension=dimension,
                    bridge_character=character,
                    natural_label_probability=probability,
                    naturally_occupied=probability > 0,
                )
            )
            bridges.append(
                dict(equal_pair_bridge_matrices(partition, sign))
            )
    for left_index, left in enumerate(partitions):
        for right in partitions[left_index + 1 :]:
            dimension = (
                2
                * hook_length_dimension(left)
                * hook_length_dimension(right)
            )
            probability = dimension * dimension / order
            records.append(
                W3PhysicalIrrepRecord(
                    id=(
                        "UNEQ-"
                        + "-".join(map(str, left))
                        + "__"
                        + "-".join(map(str, right))
                    ),
                    kind="unequal-pair-induced",
                    left_partition=left,
                    right_partition=right,
                    sign=None,
                    dimension=dimension,
                    bridge_character=0,
                    natural_label_probability=probability,
                    naturally_occupied=True,
                )
            )
            bridges.append(
                dict(unequal_pair_bridge_matrices(left, right))
            )
    if len(records) != 9:
        raise ArithmeticError("W_3 must have nine irreps")
    if not math.isclose(
        sum(record.natural_label_probability for record in records),
        1.0,
        abs_tol=1e-12,
    ):
        raise ArithmeticError("W_3 natural irrep probabilities do not sum to one")
    return records, bridges


def _multiset_orbit_size(indices: tuple[int, int, int]) -> int:
    multiplicities = Counter(indices)
    size = math.factorial(len(indices))
    for count in multiplicities.values():
        size //= math.factorial(count)
    return size


def audit_w3_tuple(
    indices: tuple[int, int, int],
    irrep_records: list[W3PhysicalIrrepRecord],
    bridge_tables: list[dict[Permutation, np.ndarray]],
    tolerance: float = 1e-8,
) -> W3TupleFrameRecord:
    if tuple(sorted(indices)) != indices:
        raise ValueError("indices must be a sorted tuple")
    labels = [irrep_records[index] for index in indices]
    block_dimension = math.prod(label.dimension for label in labels)
    frame = np.zeros((block_dimension, block_dimension))
    permutations = tuple(bridge_tables[indices[0]])
    for permutation in permutations:
        tensor = None
        for index in indices:
            dimension = irrep_records[index].dimension
            projector = (
                np.eye(dimension) + bridge_tables[index][permutation]
            ) / 2.0
            tensor = (
                projector
                if tensor is None
                else np.kron(tensor, projector)
            )
        if tensor is None:
            raise ArithmeticError("empty tuple block")
        frame += tensor
    frame /= len(permutations)
    frame = (frame + frame.T) / 2.0
    eigenvalues = np.linalg.eigvalsh(frame)
    clusters = _cluster_eigenvalues(eigenvalues, tolerance)
    positive = eigenvalues[eigenvalues > tolerance]
    rank = len(positive)
    minimum = float(positive[0]) if rank else None
    maximum = float(positive[-1]) if rank else None
    condition = (
        float(maximum / minimum)
        if minimum is not None and maximum is not None
        else None
    )
    orbit_size = _multiset_orbit_size(indices)
    probability = orbit_size * math.prod(
        label.natural_label_probability for label in labels
    )
    occupied = probability > 0
    return W3TupleFrameRecord(
        label_ids=tuple(label.id for label in labels),
        label_indices=indices,
        tuple_orbit_multiplicity=orbit_size,
        aggregate_natural_probability=probability,
        naturally_occupied=occupied,
        block_dimension=block_dimension,
        support_rank=rank,
        kernel_dimension=block_dimension - rank,
        distinct_eigenvalue_count=len(clusters),
        minimum_positive_eigenvalue=minimum,
        maximum_eigenvalue=maximum,
        support_condition_number=condition,
        eigenvalue_multiplicities=clusters,
        status=(
            "naturally-occupied-threshold-block"
            if occupied
            else "zero-natural-mass-threshold-block"
        ),
    )


def run_complete_w3_tuple_audit() -> CompleteW3TupleAuditReport:
    irrep_records, bridge_tables = w3_physical_irreps()
    tuple_records = [
        audit_w3_tuple(indices, irrep_records, bridge_tables)
        for indices in itertools.combinations_with_replacement(range(9), 3)
    ]
    occupied = [
        record for record in tuple_records if record.naturally_occupied
    ]
    occupied_mass = sum(
        record.aggregate_natural_probability for record in occupied
    )
    kernel_mass = sum(
        record.aggregate_natural_probability
        for record in occupied
        if record.kernel_dimension > 0
    )
    well_conditioned_mass = sum(
        record.aggregate_natural_probability
        for record in occupied
        if record.support_condition_number is not None
        and record.support_condition_number <= 4.0 + 1e-8
    )
    maximum_condition = max(
        (
            record.support_condition_number or 0.0
            for record in occupied
        ),
        default=0.0,
    )
    minimum_positive = min(
        (
            record.minimum_positive_eigenvalue
            for record in occupied
            if record.minimum_positive_eigenvalue is not None
        ),
        default=0.0,
    )
    worst = max(
        occupied,
        key=lambda record: (
            record.support_condition_number or 0.0,
            record.aggregate_natural_probability,
            record.label_ids,
        ),
    )
    metrics: dict[str, int | float] = {
        "physical_irrep_count": len(irrep_records),
        "naturally_occupied_irrep_count": sum(
            record.naturally_occupied for record in irrep_records
        ),
        "zero_natural_mass_irrep_count": sum(
            not record.naturally_occupied for record in irrep_records
        ),
        "unordered_threshold_tuple_count": len(tuple_records),
        "naturally_occupied_threshold_tuple_count": len(occupied),
        "zero_natural_mass_threshold_tuple_count": (
            len(tuple_records) - len(occupied)
        ),
        "natural_tuple_mass_sum": occupied_mass,
        "natural_mass_in_kernel_blocks": kernel_mass,
        "natural_mass_with_condition_number_at_most_four": (
            well_conditioned_mass
        ),
        "maximum_block_dimension": max(
            (record.block_dimension for record in tuple_records),
            default=0,
        ),
        "naturally_occupied_kernel_block_count": sum(
            record.kernel_dimension > 0 for record in occupied
        ),
        "minimum_naturally_occupied_positive_eigenvalue": minimum_positive,
        "maximum_naturally_occupied_support_condition_number": (
            maximum_condition
        ),
        "worst_block_aggregate_natural_probability": (
            worst.aggregate_natural_probability
        ),
        "complete_finite_physical_tuple_spectrum_count": 1,
        "uniform_all_n_character_moment_recurrence_count": 0,
        "coherent_blockwise_frame_inverse_count": 0,
        "hidden_label_harmonic_transform_count": 0,
        "polynomial_hidden_permutation_decoder_count": 0,
    }
    return CompleteW3TupleAuditReport(
        created_at=utc_now(),
        group_contract={
            "group": "W_3=(S_3 x S_3) semidirect C_2",
            "group_order": 72,
            "bridge_ensemble_size": 6,
            "information_threshold_copy_count": 3,
            "irrep_count": 9,
            "tuple_count": 165,
            "natural_label_probability": (
                "p_pi=d_pi[d_pi+chi_pi(h)]/|W_3|"
            ),
            "unordered_tuple_mass": (
                "multinomial orbit size times product of one-copy label "
                "probabilities"
            ),
        },
        irrep_records=irrep_records,
        tuple_records=tuple_records,
        headline_metrics=metrics,
        claim_gate={
            "all_w3_physical_irreps_constructed": True,
            "all_unordered_threshold_tuples_diagonalized": True,
            "natural_tuple_mass_complete": math.isclose(
                occupied_mass,
                1.0,
                abs_tol=1e-12,
            ),
            "all_naturally_occupied_blocks_condition_at_most_four": (
                maximum_condition <= 4.0 + 1e-8
            ),
            "all_naturally_occupied_positive_eigenvalues_at_least_one_eighth": (
                minimum_positive >= 0.125 - 1e-8
            ),
            "uniform_all_n_character_moment_recurrence_proved": False,
            "coherent_blockwise_frame_inverse_proved": False,
            "hidden_label_harmonic_transform_proved": False,
            "polynomial_hidden_permutation_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The complete W_3 threshold tuple distribution is mildly "
                "conditioned on support, but this finite theorem supplies no "
                "all-n recurrence, coherent inverse, harmonic transform, or "
                "decoder."
            ),
        },
        status="complete-w3-threshold-blocks-conditioned-all-n-open",
        summary=(
            f"Diagonalized all {len(tuple_records)} unordered W_3 threshold "
            f"tuples; {len(occupied)} occupied blocks carry natural mass "
            f"{occupied_mass:.12f}, have minimum positive eigenvalue "
            f"{minimum_positive:.6g}, and condition number at most "
            f"{maximum_condition:.6g}."
        ),
        falsifiers_triggered=[
            "The repeated-irrep probes did not miss a worse naturally occupied W_3 threshold tuple.",
            "Two one-dimensional minus irreps and every tuple containing them have zero natural coset-state mass.",
            "All naturally occupied W_3 threshold blocks have support condition number at most four.",
            "Kernel support occurs on positive-mass blocks and must be handled by a pseudoinverse, not a full inverse.",
            "A complete finite W_3 conditioning theorem does not imply an all-n recurrence or decoder.",
        ],
    )


def write_complete_w3_tuple_audit(
    path: Path = SELF_DUAL_WREATH_COMPLETE_W3_TUPLE_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, Any]:
    payload = asdict(run_complete_w3_tuple_audit())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-CODE-SELF-DUAL-WREATH-COMPLETE-W3-NOT-ALL-N-INVERSE",
                source=str(path),
                claim=(
                    "Complete mild conditioning of all naturally occupied "
                    "W_3 threshold blocks supplies a scalable frame inverse."
                ),
                reason_invalid=(
                    "The result is confined to n=3, uses dense finite "
                    "diagonalization, and supplies no character recurrence, "
                    "coherent pseudoinverse, harmonic transform, or decoder."
                ),
                lesson=(
                    "Use W_3 as an exact regression target for all-n moment "
                    "recurrences, but require a growing-n theorem before "
                    "promoting conditioning."
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
                    "self_dual_wreath_complete_w3_tuple_audit": str(path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_complete_w3_tuple_audit()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
