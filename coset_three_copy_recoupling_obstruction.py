"""Three-copy overlapping-recoupling obstruction for symmetric involutions.

Let V be the standard representation of S_n in the integer basis
``e_i-e_{n-1}``, and let

    K = sum_{tau transposition} V(tau) tensor V(tau).

On V tensor V tensor V, the class sums K_12 and K_23 are each diagonal in a
different Kronecker recoupling basis.  Direct counting gives the exact witness

    [K_12, K_23]_{(0,0,0),(0,0,1)} = n,  n >= 3.

Indeed, the intermediate coordinate y=0 cancels, y=1 contributes 3, and each
of the n-3 remaining coordinates contributes 1.  Therefore no single pairwise
Kronecker basis diagonalizes the three-copy frame for the transposition class.
This is an obstruction, not a no-algorithm theorem: a scalable route could use
coherent Racah/associator transforms, but must specify their multiplicity-space
cost and an outcome decoder.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

import numpy as np

from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from weak_fourier_signal import involution_specs_for_n


COSET_THREE_COPY_RECOUPLING_PATH = Path(
    "research/representation/coset_three_copy_recoupling_obstruction.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-THREE-COPY-RECOUPLING-OBSTRUCTION"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class ThreeCopyRecouplingRecord:
    n: int
    involution_type: str
    transposition_count: int
    class_size: int
    standard_dimension: int
    pair_space_dimension: int
    three_copy_block_dimension: int
    exact_commutator_nonzero_entry_count: int
    exact_commutator_maximum_absolute_numerator: int
    exact_commutator_frobenius_numerator_squared: int
    witness_row: tuple[int, int, int]
    witness_column: tuple[int, int, int]
    witness_numerator: int
    normalized_witness: float
    single_transposition_closed_form_witness: int | None
    single_transposition_all_n_noncommutation_proved: bool
    overlapping_pair_sums_commute: bool
    three_copy_frame_minimum_eigenvalue: float
    three_copy_frame_maximum_eigenvalue: float
    three_copy_frame_rank: int
    three_copy_frame_condition_number: float
    explicit_class_enumeration_used: bool
    uniform_coherent_associator_proved: bool
    polynomial_multiplicity_space_decoder_proved: bool
    status: str


@dataclass(frozen=True)
class ThreeCopyRecouplingReport:
    created_at: str
    theorem_contract: dict[str, str | bool]
    records: list[ThreeCopyRecouplingRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _perfect_matchings(points: tuple[int, ...]):
    if not points:
        yield ()
        return
    first = points[0]
    for index in range(1, len(points)):
        second = points[index]
        remainder = points[1:index] + points[index + 1 :]
        for tail in _perfect_matchings(remainder):
            yield ((first, second), *tail)


def involutions(n: int, transposition_count: int) -> list[tuple[int, ...]]:
    rows: list[tuple[int, ...]] = []
    for support in itertools.combinations(range(n), 2 * transposition_count):
        for matching in _perfect_matchings(tuple(support)):
            permutation = list(range(n))
            for left, right in matching:
                permutation[left], permutation[right] = right, left
            rows.append(tuple(permutation))
    return rows


def integer_standard_matrix(permutation: tuple[int, ...]) -> np.ndarray:
    """Return the standard representation in the basis e_i-e_{n-1}."""

    n = len(permutation)
    dimension = n - 1
    matrix = np.zeros((dimension, dimension), dtype=np.int64)
    for column in range(dimension):
        image = np.zeros(n, dtype=np.int64)
        image[permutation[column]] += 1
        image[permutation[n - 1]] -= 1
        matrix[:, column] = image[:dimension]
    return matrix


def transposition_commutator_witness_theorem(n: int) -> dict[str, int | bool]:
    if n < 3:
        raise ValueError("the witness needs n >= 3")
    return {
        "n": n,
        "canceling_y0_contribution": 0,
        "distinguished_y1_contribution": 3,
        "generic_coordinate_count": n - 3,
        "generic_coordinate_contribution": 1,
        "witness_numerator": n,
        "nonzero_for_all_n_at_least_three": True,
    }


def _orthonormal_standard_matrices(permutations: list[tuple[int, ...]]) -> list[np.ndarray]:
    n = len(permutations[0])
    spanning = np.zeros((n, n - 1))
    for column in range(n - 1):
        spanning[column, column] = 1.0
        spanning[n - 1, column] = -1.0
    basis, _ = np.linalg.qr(spanning)
    matrices = []
    for permutation in permutations:
        permutation_matrix = np.zeros((n, n))
        for column, row in enumerate(permutation):
            permutation_matrix[row, column] = 1.0
        matrices.append(basis.T @ permutation_matrix @ basis)
    return matrices


def audit_three_copy_recoupling(
    n: int,
    transposition_count: int,
    involution_type: str,
) -> ThreeCopyRecouplingRecord:
    permutations = involutions(n, transposition_count)
    dimension = n - 1
    integer_matrices = [integer_standard_matrix(permutation) for permutation in permutations]
    pair_sum = sum(
        (np.kron(matrix, matrix) for matrix in integer_matrices),
        start=np.zeros((dimension * dimension, dimension * dimension), dtype=np.int64),
    )
    identity = np.eye(dimension, dtype=np.int64)
    left_pair = np.kron(pair_sum, identity)
    right_pair = np.kron(identity, pair_sum)
    commutator = left_pair @ right_pair - right_pair @ left_pair
    witness_row = (0, 0, 0)
    witness_column = (0, 0, 1)
    witness_row_index = 0
    witness_column_index = 1
    witness = int(commutator[witness_row_index, witness_column_index])
    theorem = transposition_commutator_witness_theorem(n) if transposition_count == 1 else None
    if theorem is not None and witness != theorem["witness_numerator"]:
        raise ArithmeticError("direct class sum disagrees with the all-n witness formula")

    orthonormal_matrices = _orthonormal_standard_matrices(permutations)
    block_dimension = dimension**3
    frame_scalar = sum(
        (
            np.kron(np.kron(np.eye(dimension) + matrix, np.eye(dimension) + matrix), np.eye(dimension) + matrix)
            for matrix in orthonormal_matrices
        ),
        start=np.zeros((block_dimension, block_dimension)),
    ) / len(permutations)
    frame_scalar = (frame_scalar + frame_scalar.T) / 2
    eigenvalues = np.linalg.eigvalsh(frame_scalar)
    positive = eigenvalues[eigenvalues > 1e-10]
    commuting = not np.any(commutator)
    return ThreeCopyRecouplingRecord(
        n=n,
        involution_type=involution_type,
        transposition_count=transposition_count,
        class_size=len(permutations),
        standard_dimension=dimension,
        pair_space_dimension=dimension * dimension,
        three_copy_block_dimension=block_dimension,
        exact_commutator_nonzero_entry_count=int(np.count_nonzero(commutator)),
        exact_commutator_maximum_absolute_numerator=int(np.max(np.abs(commutator))),
        exact_commutator_frobenius_numerator_squared=int(np.sum(commutator * commutator)),
        witness_row=witness_row,
        witness_column=witness_column,
        witness_numerator=witness,
        normalized_witness=witness / (len(permutations) ** 2),
        single_transposition_closed_form_witness=(
            int(theorem["witness_numerator"]) if theorem is not None else None
        ),
        single_transposition_all_n_noncommutation_proved=theorem is not None,
        overlapping_pair_sums_commute=commuting,
        three_copy_frame_minimum_eigenvalue=float(np.min(eigenvalues)),
        three_copy_frame_maximum_eigenvalue=float(np.max(eigenvalues)),
        three_copy_frame_rank=len(positive),
        three_copy_frame_condition_number=(
            float(np.max(positive) / np.min(positive)) if len(positive) else math.inf
        ),
        explicit_class_enumeration_used=True,
        uniform_coherent_associator_proved=False,
        polynomial_multiplicity_space_decoder_proved=False,
        status=(
            "commuting-class-control"
            if commuting
            else "overlapping-recoupling-obstruction-associator-open"
        ),
    )


def build_three_copy_recoupling_report(
    n_values: Sequence[int] = (3, 4, 5, 6, 7),
) -> ThreeCopyRecouplingReport:
    specs: list[tuple[int, int, str]] = []
    seen: set[tuple[int, int]] = set()
    for n in n_values:
        for label, transpositions in involution_specs_for_n(n):
            key = (n, transpositions)
            if key not in seen:
                seen.add(key)
                specs.append((n, transpositions, label))
    records = [
        audit_three_copy_recoupling(n, transpositions, label)
        for n, transpositions, label in specs
    ]
    metrics: dict[str, int | float] = {
        "record_count": len(records),
        "single_transposition_all_n_theorem_row_count": sum(
            record.single_transposition_all_n_noncommutation_proved for record in records
        ),
        "noncommuting_overlapping_pair_count": sum(
            not record.overlapping_pair_sums_commute for record in records
        ),
        "commuting_class_control_count": sum(
            record.overlapping_pair_sums_commute for record in records
        ),
        "uniform_coherent_associator_count": 0,
        "polynomial_multiplicity_space_decoder_count": 0,
        "maximum_n": max(n_values),
        "maximum_class_size": max(record.class_size for record in records),
        "maximum_three_copy_block_dimension": max(
            record.three_copy_block_dimension for record in records
        ),
        "maximum_exact_commutator_nonzero_entry_count": max(
            record.exact_commutator_nonzero_entry_count for record in records
        ),
    }
    return ThreeCopyRecouplingReport(
        created_at=utc_now(),
        theorem_contract={
            "representation": "standard S_n representation in basis e_i-e_{n-1}",
            "pair_class_sum": "K=sum_tau V(tau) tensor V(tau) over all transpositions",
            "overlap_witness": "[K_12,K_23]_(000,001)=3+(n-3)=n",
            "all_n_range": "n>=3",
            "single_pairwise_basis_suffices": False,
            "remaining_route": "coherent Racah/associator transforms plus multiplicity-space decoder",
        },
        records=records,
        headline_metrics=metrics,
        claim_gate={
            "single_transposition_overlapping_noncommutation_proved_all_n": True,
            "single_pairwise_kronecker_basis_sufficient": False,
            "uniform_coherent_associator_proved": False,
            "polynomial_multiplicity_space_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The all-n commutator theorem rules out a single pairwise Kronecker basis at three copies; no uniform "
                "associator circuit or multiplicity-space hidden-involution decoder has replaced it."
            ),
        },
        status="three-copy-overlap-obstruction-proved-associator-open",
        summary=(
            f"Proved the all-n transposition-class overlapping-recoupling obstruction and audited {len(records)} "
            f"standard-representation rows through n={max(n_values)}."
        ),
        falsifiers_triggered=[
            "A single pairwise Kronecker recoupling basis cannot diagonalize the three-copy transposition frame.",
            "Finite standard-block diagonalization is not a uniform coherent associator transform.",
            "Exceptional commuting classes do not establish a mechanism for noncommuting involution classes.",
            "No multiplicity-space outcome decoder follows from the commutator theorem.",
        ],
    )


def write_three_copy_recoupling_report(
    output_path: Path = COSET_THREE_COPY_RECOUPLING_PATH,
    n_values: Sequence[int] = (3, 4, 5, 6, 7),
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(build_three_copy_recoupling_report(n_values=n_values))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-K3-SINGLE-PAIRWISE-RECOUPLING-BASIS",
                source=str(output_path),
                claim="One pairwise Kronecker basis diagonalizes the three-copy transposition coset-state frame.",
                reason_invalid=(
                    "The exact standard-representation class sums satisfy "
                    "[K_12,K_23]_(000,001)=n for every n>=3."
                ),
                lesson=(
                    "Any k>=3 route must implement overlapping Racah/associator transformations and account for "
                    "multiplicity-space decoding rather than extending the two-copy diagonalization verbatim."
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
                artifacts={"coset_three_copy_recoupling_obstruction": str(output_path)},
            )
        )
    return payload
