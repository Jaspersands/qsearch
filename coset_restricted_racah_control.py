"""Finite Racah control built from the solved commutant-gap family.

The exact gap certificate resolves the two swap-parity copies of
nu=(n-3,2,1) inside lambda=(n-2,2) tensor lambda.  At three copies, a left
coupling and a right coupling use different intermediate channels.  This
module computes their overlap inside fixed final-tableau sectors at n=6.

The resulting 2x2 matrices are subblocks of a full Racah transform, not
standalone unitaries.  Their measured leakage into other intermediate irreps
is a falsifier for the shortcut "pairwise gap implies associator" and a
control target for any future coherent recoupling construction.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path

import numpy as np

from coset_jucys_murphy_label_transform import (
    encoded_jucys_murphy_operator,
    transposition_matrix,
)
from coset_multiplicity_commutant_search import (
    _encoded_label_targets,
    transposition_three_cycle_intersection_operator,
)
from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from symmetric_character import kronecker_coefficient


COSET_RESTRICTED_RACAH_CONTROL_PATH = Path(
    "research/representation/coset_restricted_racah_control.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-RESTRICTED-RACAH-CONTROL"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class RacahSubblockRecord:
    n: int
    source_partition: tuple[int, ...]
    intermediate_partition: tuple[int, ...]
    final_partition: tuple[int, ...]
    final_irrep_dimension: int
    final_total_multiplicity: int
    final_tableau_count: int
    intermediate_to_final_multiplicity: int
    left_channel_dimension: int
    right_channel_dimension: int
    pair_hamiltonian_eigenvalues: tuple[float, ...]
    absolute_overlap_subblock: list[list[float]]
    rational_absolute_overlap_subblock: list[list[str]]
    overlap_singular_values: tuple[float, ...]
    row_leakage_probabilities: tuple[float, ...]
    minimum_channel_leakage: float
    maximum_channel_leakage: float
    tableau_overlap_consistency_residual: float
    tableau_singular_value_consistency_residual: float
    rational_reconstruction_residual: float
    restricted_subblock_is_unitary: bool
    full_associator_constructed: bool
    finite_dense_control_only: bool
    status: str


@dataclass(frozen=True)
class RestrictedRacahControlReport:
    created_at: str
    interface_contract: dict[str, object]
    records: list[RacahSubblockRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _total_encoded_yjm(
    partition: tuple[int, ...], copy_count: int = 3
) -> np.ndarray:
    if copy_count != 3:
        raise ValueError("this control currently audits exactly three copies")
    n = sum(partition)
    dimension = hook_length_dimension(partition)
    total_dimension = dimension**copy_count
    operators = [np.zeros((total_dimension, total_dimension))]
    for right in range(2, n + 1):
        operator = np.zeros((total_dimension, total_dimension))
        for left in range(1, right):
            transposition = transposition_matrix(partition, left, right)
            operator += np.kron(
                np.kron(transposition, transposition), transposition
            )
        operators.append(operator)
    return encoded_jucys_murphy_operator(operators, 2 * n + 1, n)


def _pair_transposition_class_sum(partition: tuple[int, ...]) -> np.ndarray:
    n = sum(partition)
    dimension = hook_length_dimension(partition)
    operator = np.zeros((dimension * dimension, dimension * dimension))
    for left in range(1, n):
        for right in range(left + 1, n + 1):
            transposition = transposition_matrix(partition, left, right)
            operator += np.kron(transposition, transposition)
    return operator


def _content_sum(partition: tuple[int, ...]) -> int:
    return sum(column - row for row, length in enumerate(partition) for column in range(length))


def _triple_multiplicity(
    source: tuple[int, ...], target: tuple[int, ...]
) -> int:
    return sum(
        kronecker_coefficient(source, source, intermediate)
        * kronecker_coefficient(intermediate, source, target)
        for intermediate in integer_partitions(sum(source))
    )


def _intermediate_channel_basis(
    final_tableau_basis: np.ndarray,
    pair_class_sum: np.ndarray,
    pair_hamiltonian: np.ndarray,
    target_class_eigenvalue: int,
    expected_dimension: int,
) -> tuple[np.ndarray, np.ndarray]:
    restricted_class_sum = final_tableau_basis.T @ pair_class_sum @ final_tableau_basis
    class_values, class_vectors = np.linalg.eigh(
        (restricted_class_sum + restricted_class_sum.T) / 2
    )
    selected = np.where(np.abs(class_values - target_class_eigenvalue) < 1e-7)[0]
    if len(selected) != expected_dimension:
        raise ArithmeticError(
            f"expected intermediate channel dimension {expected_dimension}, observed {len(selected)}"
        )
    channel = final_tableau_basis @ class_vectors[:, selected]
    restricted_hamiltonian = channel.T @ pair_hamiltonian @ channel
    eigenvalues, eigenvectors = np.linalg.eigh(
        (restricted_hamiltonian + restricted_hamiltonian.T) / 2
    )
    return eigenvalues, channel @ eigenvectors


def _rational_matrix(
    matrix: np.ndarray, maximum_denominator: int = 10_000
) -> tuple[list[list[str]], float]:
    rows: list[list[str]] = []
    residual = 0.0
    for source_row in matrix:
        row: list[str] = []
        for value in source_row:
            rational = Fraction(float(value)).limit_denominator(maximum_denominator)
            row.append(str(rational))
            residual = max(residual, abs(float(value) - float(rational)))
        rows.append(row)
    return rows, residual


def audit_restricted_racah_control(n: int = 6) -> list[RacahSubblockRecord]:
    if n != 6:
        raise ValueError(
            "the dense Racah control is intentionally pinned to n=6; scaling needs a compressed construction"
        )
    source = (n - 2, 2)
    intermediate = (n - 3, 2, 1)
    dimension = hook_length_dimension(source)
    identity = np.eye(dimension)

    total_yjm = _total_encoded_yjm(source)
    label_values, label_vectors = np.linalg.eigh(total_yjm)
    label_indices: dict[int, list[int]] = {}
    for index, value in enumerate(label_values):
        label_indices.setdefault(round(float(value)), []).append(index)
    targets = _encoded_label_targets(n, 2 * n + 1)

    pair_class = _pair_transposition_class_sum(source)
    pair_hamiltonian, _ = transposition_three_cycle_intersection_operator(
        source, source, support_intersection=2
    )
    left_class = np.kron(pair_class, identity)
    right_class = np.kron(identity, pair_class)
    left_hamiltonian = np.kron(pair_hamiltonian, identity)
    right_hamiltonian = np.kron(identity, pair_hamiltonian)
    intermediate_class_eigenvalue = _content_sum(intermediate)

    records: list[RacahSubblockRecord] = []
    for final in integer_partitions(n):
        intermediate_to_final = kronecker_coefficient(intermediate, source, final)
        if intermediate_to_final != 1:
            continue
        overlap_matrices: list[np.ndarray] = []
        singular_values: list[np.ndarray] = []
        eigenvalue_rows: list[np.ndarray] = []
        for label, indices in label_indices.items():
            if targets[label] != final:
                continue
            final_basis = label_vectors[:, indices]
            expected_channel_dimension = 2 * intermediate_to_final
            left_eigenvalues, left_basis = _intermediate_channel_basis(
                final_basis,
                left_class,
                left_hamiltonian,
                intermediate_class_eigenvalue,
                expected_channel_dimension,
            )
            right_eigenvalues, right_basis = _intermediate_channel_basis(
                final_basis,
                right_class,
                right_hamiltonian,
                intermediate_class_eigenvalue,
                expected_channel_dimension,
            )
            if np.linalg.norm(left_eigenvalues - right_eigenvalues) > 1e-7:
                raise ArithmeticError("left and right pair spectra disagree")
            overlap = left_basis.T @ right_basis
            overlap_matrices.append(np.abs(overlap))
            singular_values.append(np.linalg.svd(overlap, compute_uv=False))
            eigenvalue_rows.append(left_eigenvalues)
        if not overlap_matrices:
            continue
        reference_overlap = overlap_matrices[0]
        reference_singular_values = singular_values[0]
        overlap_consistency = max(
            float(np.linalg.norm(matrix - reference_overlap))
            for matrix in overlap_matrices
        )
        singular_consistency = max(
            float(np.linalg.norm(values - reference_singular_values))
            for values in singular_values
        )
        rational_overlap, rational_residual = _rational_matrix(reference_overlap)
        leakage = 1.0 - np.sum(reference_overlap * reference_overlap, axis=1)
        unitary = bool(
            np.linalg.norm(reference_overlap.T @ reference_overlap - np.eye(2)) < 1e-8
        )
        records.append(
            RacahSubblockRecord(
                n=n,
                source_partition=source,
                intermediate_partition=intermediate,
                final_partition=final,
                final_irrep_dimension=hook_length_dimension(final),
                final_total_multiplicity=_triple_multiplicity(source, final),
                final_tableau_count=len(overlap_matrices),
                intermediate_to_final_multiplicity=intermediate_to_final,
                left_channel_dimension=reference_overlap.shape[0],
                right_channel_dimension=reference_overlap.shape[1],
                pair_hamiltonian_eigenvalues=tuple(
                    float(value) for value in eigenvalue_rows[0]
                ),
                absolute_overlap_subblock=reference_overlap.tolist(),
                rational_absolute_overlap_subblock=rational_overlap,
                overlap_singular_values=tuple(
                    float(value) for value in reference_singular_values
                ),
                row_leakage_probabilities=tuple(float(value) for value in leakage),
                minimum_channel_leakage=float(np.min(leakage)),
                maximum_channel_leakage=float(np.max(leakage)),
                tableau_overlap_consistency_residual=overlap_consistency,
                tableau_singular_value_consistency_residual=singular_consistency,
                rational_reconstruction_residual=rational_residual,
                restricted_subblock_is_unitary=unitary,
                full_associator_constructed=False,
                finite_dense_control_only=True,
                status=(
                    "nonunitary-racah-subblock-leaks-to-other-intermediate-channels"
                    if not unitary and np.min(leakage) > 1e-8
                    else "restricted-racah-control-degenerate"
                ),
            )
        )
    return records


def build_restricted_racah_control_report(n: int = 6) -> RestrictedRacahControlReport:
    records = audit_restricted_racah_control(n=n)
    consistency = max(
        (record.tableau_overlap_consistency_residual for record in records),
        default=math.inf,
    )
    metrics: dict[str, int | float] = {
        "record_count": len(records),
        "final_target_count": len(records),
        "tableau_consistent_subblock_count": sum(
            record.tableau_overlap_consistency_residual < 1e-8 for record in records
        ),
        "rational_subblock_reconstruction_count": sum(
            record.rational_reconstruction_residual < 1e-8 for record in records
        ),
        "nonunitary_restricted_subblock_count": sum(
            not record.restricted_subblock_is_unitary for record in records
        ),
        "channel_leakage_detected_count": sum(
            record.minimum_channel_leakage > 1e-8 for record in records
        ),
        "maximum_channel_leakage": max(
            (record.maximum_channel_leakage for record in records), default=0.0
        ),
        "maximum_tableau_consistency_residual": consistency,
        "full_racah_associator_count": 0,
        "uniform_polynomial_racah_circuit_count": 0,
        "hidden_involution_decoder_count": 0,
        "maximum_dense_dimension": hook_length_dimension((n - 2, 2)) ** 3,
    }
    all_leak = bool(records) and all(
        not record.restricted_subblock_is_unitary
        and record.minimum_channel_leakage > 1e-8
        for record in records
    )
    return RestrictedRacahControlReport(
        created_at=utc_now(),
        interface_contract={
            "source": "three copies of V_(n-2,2)",
            "solved_pair_channel": "intermediate nu=(n-3,2,1), split by the exact commutant-gap parity basis",
            "left_coupling": "resolve nu in copies (1,2), then condition on one final target tableau",
            "right_coupling": "resolve nu in copies (2,3), then condition on the same final target tableau",
            "reported_object": "absolute 2x2 overlap subblock between the two parity-resolved intermediate channels",
            "not_reported_as": "a complete Racah matrix or uniform coherent circuit",
        },
        records=records,
        headline_metrics=metrics,
        claim_gate={
            "solved_pair_gap_used_as_control": True,
            "tableau_independent_subblocks_verified": consistency < 1e-8,
            "restricted_channel_leakage_detected": all_leak,
            "pair_gap_implies_closed_associator": False,
            "full_racah_associator_constructed": False,
            "uniform_polynomial_racah_circuit_proved": False,
            "hidden_involution_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The parity-resolved 2x2 blocks are reproducible but nonunitary because other intermediate irreps carry amplitude; a full coherent associator remains open."
            ),
        },
        status=(
            "restricted-racah-subblocks-resolved-full-associator-open"
            if all_leak and consistency < 1e-8
            else "restricted-racah-control-failed"
        ),
        summary=(
            f"Resolved {len(records)} parity-channel Racah subblocks at n={n}; every restricted block leaks to other "
            "intermediate irreps, so the exact pair gap does not close the associator obligation."
        ),
        falsifiers_triggered=[
            "An inverse-polynomial pairwise multiplicity gap does not by itself supply a three-copy Racah transform.",
            "The 2x2 parity overlap is a nonunitary subblock; discarding the complementary intermediate channels loses probability.",
            "Finite dense diagonalization at n=6 is a control artifact, not a uniform polynomial circuit.",
            "No hidden-involution decoder follows from a recoupling overlap table.",
        ],
    )


def write_restricted_racah_control_report(
    output_path: Path = COSET_RESTRICTED_RACAH_CONTROL_PATH,
    n: int = 6,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(build_restricted_racah_control_report(n=n))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-PAIR-GAP-AS-THREE-COPY-RACAH-TRANSFORM",
                source=str(output_path),
                claim=(
                    "The solved pairwise commutant gap directly supplies a closed three-copy Racah transform on the same channel."
                ),
                reason_invalid=(
                    "Every audited parity-resolved 2x2 overlap is a nonunitary subblock with explicit leakage to other intermediate irreps."
                ),
                lesson=(
                    "A full associator must coherently include all intermediate partitions and multiplicity channels, not only the solved pair block."
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
                artifacts={"coset_restricted_racah_control": str(output_path)},
            )
        )
    return payload
