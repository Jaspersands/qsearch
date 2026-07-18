"""Complete finite Racah controls for three copies of the S_6 irrep (4,2).

The restricted Racah control follows only the multiplicity-two intermediate
partition (3,2,1), so its 2x2 overlap blocks necessarily leak into omitted
channels.  This module includes every intermediate partition for final sectors
where the second coupling is multiplicity-free.  Pair class sums identify the
intermediate partition and the proved-gap orbit Hamiltonian resolves the two
internal multiplicity spaces that occur in (4,2) tensor (4,2).

The resulting signed overlap matrices are complete and unitary for five final
S_6 sectors.  They are finite dense controls, not a uniform Racah circuit:
five other sectors have a second-stage Kronecker multiplicity greater than one,
and no compressed all-n construction or hidden-involution decoder is supplied.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path

import numpy as np

from coset_jucys_murphy_label_transform import transposition_matrix
from coset_multiplicity_commutant_search import (
    _encoded_label_targets,
    _oriented_three_cycles,
    transposition_three_cycle_intersection_operator,
)
from coset_restricted_racah_control import _total_encoded_yjm
from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from symmetric_character import (
    conjugacy_class_size,
    kronecker_coefficient,
    symmetric_character,
)


COSET_COMPLETE_RACAH_CONTROL_PATH = Path(
    "research/representation/coset_complete_racah_control.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-COMPLETE-RACAH-CONTROL"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class RacahChannelRecord:
    intermediate_partition: tuple[int, ...]
    first_stage_multiplicity: int
    second_stage_multiplicity: int
    pair_central_signature: int
    pair_hamiltonian_eigenvalue: float


@dataclass(frozen=True)
class CompleteRacahMatrixRecord:
    n: int
    source_partition: tuple[int, ...]
    final_partition: tuple[int, ...]
    final_irrep_dimension: int
    final_total_multiplicity: int
    final_tableau_count: int
    channels: list[RacahChannelRecord]
    signed_overlap_matrix: list[list[float]]
    absolute_overlap_matrix: list[list[float]]
    transition_probability_matrix: list[list[float]]
    unitarity_residual: float
    tableau_absolute_consistency_residual: float
    tableau_probability_consistency_residual: float
    left_right_pair_spectrum_residual: float
    minimum_nonzero_transition_probability: float
    maximum_transition_probability: float
    nontrivial_recoupling: bool
    complete_for_final_sector: bool
    finite_dense_control_only: bool
    status: str


@dataclass(frozen=True)
class UnresolvedRacahSectorRecord:
    final_partition: tuple[int, ...]
    final_total_multiplicity: int
    maximum_second_stage_multiplicity: int
    unresolved_channels: list[dict[str, object]]
    reason: str


@dataclass(frozen=True)
class CompleteRacahControlReport:
    created_at: str
    interface_contract: dict[str, object]
    records: list[CompleteRacahMatrixRecord]
    unresolved_sectors: list[UnresolvedRacahSectorRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _pair_class_sums(partition: tuple[int, ...]) -> tuple[np.ndarray, np.ndarray]:
    n = sum(partition)
    dimension = hook_length_dimension(partition)
    transposition_sum = np.zeros((dimension * dimension, dimension * dimension))
    for left in range(1, n):
        for right in range(left + 1, n + 1):
            matrix = transposition_matrix(partition, left, right)
            transposition_sum += np.kron(matrix, matrix)
    three_cycle_sum = np.zeros_like(transposition_sum)
    for _, matrix in _oriented_three_cycles(partition):
        three_cycle_sum += np.kron(matrix, matrix)
    return transposition_sum, three_cycle_sum


def _class_sum_eigenvalue(
    partition: tuple[int, ...], cycle_type: tuple[int, ...]
) -> int:
    dimension = hook_length_dimension(partition)
    numerator = (
        conjugacy_class_size(cycle_type)
        * symmetric_character(partition, cycle_type)
    )
    if numerator % dimension:
        raise ArithmeticError("class-sum eigenvalue is not integral")
    return numerator // dimension


def _central_signature(partition: tuple[int, ...]) -> int:
    n = sum(partition)
    transposition_type = (2, *((1,) * (n - 2)))
    three_cycle_type = (3, *((1,) * (n - 3)))
    return 100 * _class_sum_eigenvalue(
        partition, transposition_type
    ) + _class_sum_eigenvalue(partition, three_cycle_type)


def _triple_channels(
    source: tuple[int, ...], final: tuple[int, ...]
) -> list[tuple[tuple[int, ...], int, int]]:
    rows: list[tuple[tuple[int, ...], int, int]] = []
    for intermediate in integer_partitions(sum(source)):
        first = kronecker_coefficient(source, source, intermediate)
        second = kronecker_coefficient(intermediate, source, final)
        if first and second:
            rows.append((intermediate, first, second))
    return rows


def _resolve_complete_pair_basis(
    final_tableau_basis: np.ndarray,
    pair_signature_operator: np.ndarray,
    pair_hamiltonian: np.ndarray,
    channel_specs: list[tuple[tuple[int, ...], int, int]],
) -> tuple[np.ndarray, list[RacahChannelRecord]]:
    restricted_signature = final_tableau_basis.T @ pair_signature_operator @ final_tableau_basis
    signature_values, signature_vectors = np.linalg.eigh(
        (restricted_signature + restricted_signature.T) / 2
    )
    basis_columns: list[np.ndarray] = []
    channel_records: list[RacahChannelRecord] = []
    for intermediate, first_multiplicity, second_multiplicity in channel_specs:
        if second_multiplicity != 1:
            raise ValueError("complete control requires multiplicity-free second coupling")
        signature = _central_signature(intermediate)
        selected = np.where(np.abs(signature_values - signature) < 1e-7)[0]
        if len(selected) != first_multiplicity:
            raise ArithmeticError(
                f"expected {first_multiplicity} copies of {intermediate}, observed {len(selected)}"
            )
        signature_basis = final_tableau_basis @ signature_vectors[:, selected]
        restricted_hamiltonian = signature_basis.T @ pair_hamiltonian @ signature_basis
        hamiltonian_values, hamiltonian_vectors = np.linalg.eigh(
            (restricted_hamiltonian + restricted_hamiltonian.T) / 2
        )
        resolved = signature_basis @ hamiltonian_vectors
        for index, eigenvalue in enumerate(hamiltonian_values):
            basis_columns.append(resolved[:, index])
            channel_records.append(
                RacahChannelRecord(
                    intermediate_partition=intermediate,
                    first_stage_multiplicity=first_multiplicity,
                    second_stage_multiplicity=second_multiplicity,
                    pair_central_signature=signature,
                    pair_hamiltonian_eigenvalue=float(eigenvalue),
                )
            )
    basis = np.column_stack(basis_columns)
    expected = sum(first * second for _, first, second in channel_specs)
    if basis.shape[1] != expected:
        raise ArithmeticError("resolved pair basis has the wrong dimension")
    if np.linalg.norm(basis.T @ basis - np.eye(expected)) > 1e-7:
        raise ArithmeticError("resolved pair basis is not orthonormal")
    return basis, channel_records


@lru_cache(maxsize=1)
def _audit_complete_racah_control_cached(
    n: int = 6,
) -> tuple[tuple[CompleteRacahMatrixRecord, ...], tuple[UnresolvedRacahSectorRecord, ...]]:
    if n != 6:
        raise ValueError(
            "the complete dense Racah control is pinned to n=6; scaling requires a compressed construction"
        )
    source = (n - 2, 2)
    source_dimension = hook_length_dimension(source)
    identity = np.eye(source_dimension)

    total_yjm = _total_encoded_yjm(source)
    label_values, label_vectors = np.linalg.eigh(total_yjm)
    label_indices: dict[int, list[int]] = {}
    for index, value in enumerate(label_values):
        label_indices.setdefault(round(float(value)), []).append(index)
    target_by_label = _encoded_label_targets(n, 2 * n + 1)

    pair_transpositions, pair_three_cycles = _pair_class_sums(source)
    pair_signature = 100 * pair_transpositions + pair_three_cycles
    pair_hamiltonian, _ = transposition_three_cycle_intersection_operator(
        source, source, support_intersection=2
    )
    left_signature = np.kron(pair_signature, identity)
    right_signature = np.kron(identity, pair_signature)
    left_hamiltonian = np.kron(pair_hamiltonian, identity)
    right_hamiltonian = np.kron(identity, pair_hamiltonian)

    records: list[CompleteRacahMatrixRecord] = []
    unresolved: list[UnresolvedRacahSectorRecord] = []
    for final in integer_partitions(n):
        channel_specs = _triple_channels(source, final)
        if not channel_specs:
            continue
        total_multiplicity = sum(first * second for _, first, second in channel_specs)
        if any(second != 1 for _, _, second in channel_specs):
            unresolved.append(
                UnresolvedRacahSectorRecord(
                    final_partition=final,
                    final_total_multiplicity=total_multiplicity,
                    maximum_second_stage_multiplicity=max(
                        second for _, _, second in channel_specs
                    ),
                    unresolved_channels=[
                        {
                            "intermediate_partition": intermediate,
                            "first_stage_multiplicity": first,
                            "second_stage_multiplicity": second,
                        }
                        for intermediate, first, second in channel_specs
                        if second > 1
                    ],
                    reason=(
                        "Pair central signatures and the first-stage gap Hamiltonian do not resolve the "
                        "second-stage Kronecker multiplicity."
                    ),
                )
            )
            continue

        signed_overlaps: list[np.ndarray] = []
        absolute_overlaps: list[np.ndarray] = []
        probability_matrices: list[np.ndarray] = []
        channel_rows: list[list[RacahChannelRecord]] = []
        pair_spectrum_residuals: list[float] = []
        for label, indices in label_indices.items():
            if target_by_label[label] != final:
                continue
            final_basis = label_vectors[:, indices]
            if final_basis.shape[1] != total_multiplicity:
                raise ArithmeticError("final-tableau multiplicity does not match characters")
            left_basis, left_channels = _resolve_complete_pair_basis(
                final_basis, left_signature, left_hamiltonian, channel_specs
            )
            right_basis, right_channels = _resolve_complete_pair_basis(
                final_basis, right_signature, right_hamiltonian, channel_specs
            )
            left_spectrum = np.asarray(
                [channel.pair_hamiltonian_eigenvalue for channel in left_channels]
            )
            right_spectrum = np.asarray(
                [channel.pair_hamiltonian_eigenvalue for channel in right_channels]
            )
            pair_spectrum_residuals.append(float(np.linalg.norm(left_spectrum - right_spectrum)))
            overlap = left_basis.T @ right_basis
            signed_overlaps.append(overlap)
            absolute_overlaps.append(np.abs(overlap))
            probability_matrices.append(overlap * overlap)
            channel_rows.append(left_channels)

        if not signed_overlaps:
            raise ArithmeticError(f"no final tableaux found for {final}")
        reference = signed_overlaps[0]
        absolute_reference = absolute_overlaps[0]
        probability_reference = probability_matrices[0]
        unitarity_residual = max(
            float(np.linalg.norm(matrix.T @ matrix - np.eye(total_multiplicity)))
            for matrix in signed_overlaps
        )
        absolute_consistency = max(
            float(np.linalg.norm(matrix - absolute_reference))
            for matrix in absolute_overlaps
        )
        probability_consistency = max(
            float(np.linalg.norm(matrix - probability_reference))
            for matrix in probability_matrices
        )
        positive_probabilities = probability_reference[probability_reference > 1e-12]
        off_diagonal = reference - np.diag(np.diag(reference))
        records.append(
            CompleteRacahMatrixRecord(
                n=n,
                source_partition=source,
                final_partition=final,
                final_irrep_dimension=hook_length_dimension(final),
                final_total_multiplicity=total_multiplicity,
                final_tableau_count=len(signed_overlaps),
                channels=channel_rows[0],
                signed_overlap_matrix=reference.tolist(),
                absolute_overlap_matrix=absolute_reference.tolist(),
                transition_probability_matrix=probability_reference.tolist(),
                unitarity_residual=unitarity_residual,
                tableau_absolute_consistency_residual=absolute_consistency,
                tableau_probability_consistency_residual=probability_consistency,
                left_right_pair_spectrum_residual=max(pair_spectrum_residuals),
                minimum_nonzero_transition_probability=float(np.min(positive_probabilities)),
                maximum_transition_probability=float(np.max(probability_reference)),
                nontrivial_recoupling=bool(np.linalg.norm(off_diagonal) > 1e-8),
                complete_for_final_sector=unitarity_residual < 1e-8,
                finite_dense_control_only=True,
                status=(
                    "complete-unitary-finite-racah-control"
                    if unitarity_residual < 1e-8
                    else "finite-racah-control-failed-unitarity"
                ),
            )
        )
    return tuple(records), tuple(unresolved)


def audit_complete_racah_control(
    n: int = 6,
) -> tuple[list[CompleteRacahMatrixRecord], list[UnresolvedRacahSectorRecord]]:
    records, unresolved = _audit_complete_racah_control_cached(n)
    return list(records), list(unresolved)


def build_complete_racah_control_report(n: int = 6) -> CompleteRacahControlReport:
    records, unresolved = audit_complete_racah_control(n=n)
    maximum_unitarity = max(
        (record.unitarity_residual for record in records), default=math.inf
    )
    maximum_consistency = max(
        (record.tableau_absolute_consistency_residual for record in records),
        default=math.inf,
    )
    metrics: dict[str, int | float] = {
        "final_target_count": len(records) + len(unresolved),
        "complete_finite_racah_matrix_count": sum(
            record.complete_for_final_sector for record in records
        ),
        "nontrivial_complete_finite_racah_matrix_count": sum(
            record.complete_for_final_sector and record.nontrivial_recoupling
            for record in records
        ),
        "unresolved_second_stage_multiplicity_sector_count": len(unresolved),
        "maximum_complete_matrix_dimension": max(
            (record.final_total_multiplicity for record in records), default=0
        ),
        "maximum_unresolved_matrix_dimension": max(
            (record.final_total_multiplicity for record in unresolved), default=0
        ),
        "maximum_second_stage_multiplicity": max(
            (record.maximum_second_stage_multiplicity for record in unresolved),
            default=1,
        ),
        "maximum_unitarity_residual": maximum_unitarity,
        "maximum_tableau_absolute_consistency_residual": maximum_consistency,
        "uniform_polynomial_racah_circuit_count": 0,
        "all_n_racah_formula_count": 0,
        "hidden_involution_decoder_count": 0,
        "maximum_dense_dimension": hook_length_dimension((n - 2, 2)) ** 3,
    }
    all_complete = bool(records) and all(
        record.complete_for_final_sector for record in records
    )
    return CompleteRacahControlReport(
        created_at=utc_now(),
        interface_contract={
            "source": "three copies of V_(4,2) for S_6",
            "final_sector_resolution": "total diagonal Young-Jucys-Murphy tableau labels",
            "intermediate_partition_resolution": "pair transposition and 3-cycle central signatures",
            "first_stage_multiplicity_resolution": "the bounded-support transposition/3-cycle orbit Hamiltonian",
            "complete_scope": (
                "all intermediate channels for final sectors with g(alpha,(4,2),xi)=1"
            ),
            "reported_object": "signed unitary left-tree/right-tree overlap matrices and gauge-invariant probabilities",
            "not_reported_as": "a uniform all-n coherent circuit, a complete S_6 associator, or a decoder",
        },
        records=records,
        unresolved_sectors=unresolved,
        headline_metrics=metrics,
        claim_gate={
            "complete_finite_matrices_verified": all_complete,
            "restricted_subblock_leakage_explained_by_omitted_channels": all_complete,
            "all_final_sectors_resolved": not unresolved,
            "uniform_polynomial_racah_circuit_proved": False,
            "all_n_racah_formula_proved": False,
            "hidden_involution_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Five finite target sectors have complete unitary controls, but five sectors retain second-stage "
                "multiplicity, and no compressed all-n circuit or hidden-involution decoder exists."
            ),
        },
        status=(
            "finite-complete-racah-controls-verified-uniform-associator-open"
            if all_complete and unresolved
            else "complete-racah-control-audit-inconclusive"
        ),
        summary=(
            f"Constructed {len(records)} complete finite Racah matrices at n={n}, including "
            f"{sum(record.nontrivial_recoupling for record in records)} nontrivial transforms; "
            f"{len(unresolved)} final sectors still require second-stage multiplicity operators."
        ),
        falsifiers_triggered=[
            "The earlier nonunitary 2x2 blocks were not closed Racah transforms; omitted intermediate partitions carry the missing probability.",
            "Pair central signatures plus one first-stage gap Hamiltonian do not resolve second-stage multiplicity in every final sector.",
            "A finite dense unitary overlap table does not imply a uniform polynomial coherent associator.",
            "No hidden-involution decoder follows from finite recoupling matrices.",
        ],
    )


def write_complete_racah_control_report(
    output_path: Path = COSET_COMPLETE_RACAH_CONTROL_PATH,
    n: int = 6,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(build_complete_racah_control_report(n=n))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-FINITE-RACAH-AS-UNIFORM-ASSOCIATOR",
                source=str(output_path),
                claim=(
                    "Complete finite left/right recoupling matrices imply a scalable coherent Racah associator."
                ),
                reason_invalid=(
                    "The construction uses dense n=6 diagonalization, leaves five second-stage multiplicity sectors unresolved, "
                    "and supplies neither an all-n formula nor a circuit."
                ),
                lesson=(
                    "Use the finite matrices as exact controls for deriving compressed partition-level identities; require a uniform "
                    "gate construction and decoder before algorithmic promotion."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence=payload["headline_metrics"],
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-LATEST"
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
                artifacts={"coset_complete_racah_control": str(output_path)},
            )
        )
    return payload
