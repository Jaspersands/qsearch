"""Diagonal Young--Jucys--Murphy label extraction for S_n tensor sectors.

For irreducibles V_lambda and V_mu, the diagonal S_n action on
V_lambda tensor V_mu decomposes as

    direct_sum_nu V_nu tensor C^{g(lambda, mu, nu)}.

The diagonal Young--Jucys--Murphy (YJM) operators

    X_k = sum_{i < k} rho_lambda((i k)) tensor rho_mu((i k))

commute.  Their joint eigenvalues are the content vectors of standard Young
tableaux of shape nu.  Thus they expose the target tableau/Gelfand--Tsetlin
path, but act as the identity on the Kronecker multiplicity register.  This
module verifies that boundary exactly on finite sectors and records the
uniform circuit contract for measuring the labels with controlled diagonal
group actions and block-encoded Hamiltonian simulation.

The construction is deliberately not called an internal Kronecker transform:
it neither chooses a basis in a g(lambda, mu, nu)-dimensional multiplicity
space nor supplies Racah associators, transition filters, or a hidden-
involution decoder.
"""

from __future__ import annotations

import json
import math
from collections import Counter
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Sequence

import numpy as np

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from symmetric_character import kronecker_coefficient


COSET_JM_LABEL_TRANSFORM_PATH = Path(
    "research/representation/coset_jucys_murphy_label_transform.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-JUCYS-MURPHY-LABEL-TRANSFORM"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Tableau = tuple[tuple[int, ...], ...]


@dataclass(frozen=True)
class JucysMurphySectorRecord:
    n: int
    left_partition: tuple[int, ...]
    right_partition: tuple[int, ...]
    left_dimension: int
    right_dimension: int
    tensor_dimension: int
    diagonal_transposition_term_count: int
    encoding_base: int
    coxeter_maximum_residual: float
    transposition_involution_maximum_residual: float
    yjm_commutator_maximum_residual: float
    encoded_spectrum_maximum_residual: float
    expected_joint_label_count: int
    observed_joint_label_count: int
    maximum_kronecker_multiplicity: int
    maximum_multiplicity_target: tuple[int, ...]
    maximum_joint_eigenspace_degeneracy: int
    kronecker_degeneracies_exactly_reproduced: bool
    target_tableau_labels_resolved: bool
    multiplicity_basis_resolved: bool
    finite_matrix_verification_only: bool
    status: str


@dataclass(frozen=True)
class JucysMurphyLabelTransformReport:
    created_at: str
    literature_scope: list[dict[str, str]]
    theorem_contract: dict[str, object]
    circuit_contract: dict[str, object]
    records: list[JucysMurphySectorRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _remove_corner(partition: tuple[int, ...], row: int) -> tuple[int, ...]:
    reduced = list(partition)
    reduced[row] -= 1
    return tuple(value for value in reduced if value)


@lru_cache(maxsize=None)
def standard_young_tableaux(partition: tuple[int, ...]) -> tuple[Tableau, ...]:
    """Enumerate standard tableaux by recursively removing the cell containing n."""

    n = sum(partition)
    if n == 0:
        return ((),)
    rows: list[Tableau] = []
    for row, length in enumerate(partition):
        next_length = partition[row + 1] if row + 1 < len(partition) else 0
        if length <= next_length:
            continue
        reduced = _remove_corner(partition, row)
        for tableau in standard_young_tableaux(reduced):
            mutable = [list(values) for values in tableau]
            while len(mutable) <= row:
                mutable.append([])
            mutable[row].append(n)
            rows.append(tuple(tuple(values) for values in mutable))
    return tuple(rows)


def tableau_positions(tableau: Tableau) -> tuple[tuple[int, int], ...]:
    n = sum(len(row) for row in tableau)
    positions: list[tuple[int, int] | None] = [None] * n
    for row, values in enumerate(tableau):
        for column, value in enumerate(values):
            positions[value - 1] = (row, column)
    if any(position is None for position in positions):
        raise ValueError("tableau entries must be exactly 1..n")
    return tuple(position for position in positions if position is not None)


def tableau_content_vector(tableau: Tableau) -> tuple[int, ...]:
    return tuple(column - row for row, column in tableau_positions(tableau))


@lru_cache(maxsize=None)
def adjacent_transposition_matrices(partition: tuple[int, ...]) -> tuple[np.ndarray, ...]:
    """Young's orthogonal seminormal matrices for s_i=(i,i+1)."""

    tableaux = standard_young_tableaux(partition)
    index = {tableau: position for position, tableau in enumerate(tableaux)}
    positions = [tableau_positions(tableau) for tableau in tableaux]
    matrices: list[np.ndarray] = []
    for adjacent in range(1, sum(partition)):
        matrix = np.zeros((len(tableaux), len(tableaux)), dtype=float)
        for column, tableau in enumerate(tableaux):
            row_i, col_i = positions[column][adjacent - 1]
            row_j, col_j = positions[column][adjacent]
            axial_distance = (col_j - row_j) - (col_i - row_i)
            matrix[column, column] = 1.0 / axial_distance
            if abs(axial_distance) == 1:
                continue
            mutable = [list(row) for row in tableau]
            mutable[row_i][col_i], mutable[row_j][col_j] = (
                mutable[row_j][col_j],
                mutable[row_i][col_i],
            )
            swapped = tuple(tuple(row) for row in mutable)
            matrix[index[swapped], column] = math.sqrt(
                1.0 - 1.0 / (axial_distance * axial_distance)
            )
        matrices.append(matrix)
    return tuple(matrices)


@lru_cache(maxsize=None)
def transposition_matrix(
    partition: tuple[int, ...], left: int, right: int
) -> np.ndarray:
    """Return rho((left,right)) for one-indexed left < right."""

    n = sum(partition)
    if not (1 <= left < right <= n):
        raise ValueError("expected 1 <= left < right <= n")
    adjacent = adjacent_transposition_matrices(partition)
    word = [*range(left - 1, right - 1), *range(right - 3, left - 2, -1)]
    result = np.eye(len(standard_young_tableaux(partition)))
    for generator in word:
        result = result @ adjacent[generator]
    return result


def coxeter_maximum_residual(partition: tuple[int, ...]) -> float:
    generators = adjacent_transposition_matrices(partition)
    dimension = len(standard_young_tableaux(partition))
    identity = np.eye(dimension)
    residuals = [np.linalg.norm(generator @ generator - identity) for generator in generators]
    residuals.extend(
        np.linalg.norm(generators[i] @ generators[j] - generators[j] @ generators[i])
        for i in range(len(generators))
        for j in range(i + 2, len(generators))
    )
    residuals.extend(
        np.linalg.norm(
            generators[i] @ generators[i + 1] @ generators[i]
            - generators[i + 1] @ generators[i] @ generators[i + 1]
        )
        for i in range(len(generators) - 1)
    )
    return float(max(residuals, default=0.0))


def diagonal_jucys_murphy_operators(
    left_partition: tuple[int, ...], right_partition: tuple[int, ...]
) -> tuple[np.ndarray, ...]:
    if sum(left_partition) != sum(right_partition):
        raise ValueError("partitions must have equal size")
    left_dimension = len(standard_young_tableaux(left_partition))
    right_dimension = len(standard_young_tableaux(right_partition))
    operators = [np.zeros((left_dimension * right_dimension,) * 2)]
    for k in range(2, sum(left_partition) + 1):
        operator = np.zeros((left_dimension * right_dimension,) * 2)
        for i in range(1, k):
            operator += np.kron(
                transposition_matrix(left_partition, i, k),
                transposition_matrix(right_partition, i, k),
            )
        operators.append(operator)
    return tuple(operators)


def _encoded_content(content: tuple[int, ...], base: int, shift: int) -> int:
    return sum((value + shift) * base**index for index, value in enumerate(content[1:]))


def expected_encoded_spectrum(
    left_partition: tuple[int, ...], right_partition: tuple[int, ...], base: int
) -> list[int]:
    n = sum(left_partition)
    spectrum: list[int] = []
    for target in integer_partitions(n):
        multiplicity = kronecker_coefficient(left_partition, right_partition, target)
        for tableau in standard_young_tableaux(target):
            spectrum.extend(
                [_encoded_content(tableau_content_vector(tableau), base, n)] * multiplicity
            )
    return sorted(spectrum)


def encoded_jucys_murphy_operator(
    operators: Sequence[np.ndarray], base: int, shift: int
) -> np.ndarray:
    dimension = operators[0].shape[0]
    encoded = np.zeros((dimension, dimension))
    identity = np.eye(dimension)
    for index, operator in enumerate(operators[1:]):
        encoded += (operator + shift * identity) * base**index
    return encoded


def select_audit_sectors(n: int) -> tuple[tuple[tuple[int, ...], tuple[int, ...]], ...]:
    """Select the largest tensor sector and the strongest multiplicity sector."""

    partitions = integer_partitions(n)
    dimensions = {partition: hook_length_dimension(partition) for partition in partitions}
    pairs = [(left, right) for i, left in enumerate(partitions) for right in partitions[i:]]
    largest = max(pairs, key=lambda pair: (dimensions[pair[0]] * dimensions[pair[1]], pair))

    def multiplicity_score(pair: tuple[tuple[int, ...], tuple[int, ...]]) -> tuple[int, int]:
        maximum = max(
            kronecker_coefficient(pair[0], pair[1], target) for target in partitions
        )
        return maximum, dimensions[pair[0]] * dimensions[pair[1]]

    multiplicity = max(pairs, key=multiplicity_score)
    return tuple(dict.fromkeys((largest, multiplicity)))


def audit_jucys_murphy_sector(
    left_partition: tuple[int, ...], right_partition: tuple[int, ...]
) -> JucysMurphySectorRecord:
    n = sum(left_partition)
    if n != sum(right_partition):
        raise ValueError("partitions must have equal size")
    left_dimension = hook_length_dimension(left_partition)
    right_dimension = hook_length_dimension(right_partition)
    if len(standard_young_tableaux(left_partition)) != left_dimension:
        raise ArithmeticError("left tableau enumeration disagrees with hook-length formula")
    if len(standard_young_tableaux(right_partition)) != right_dimension:
        raise ArithmeticError("right tableau enumeration disagrees with hook-length formula")

    operators = diagonal_jucys_murphy_operators(left_partition, right_partition)
    commutator_residual = max(
        (
            np.linalg.norm(operators[i] @ operators[j] - operators[j] @ operators[i])
            for i in range(1, n)
            for j in range(i + 1, n)
        ),
        default=0.0,
    )
    involution_residual = max(
        (
            np.linalg.norm(
                transposition_matrix(partition, i, k)
                @ transposition_matrix(partition, i, k)
                - np.eye(hook_length_dimension(partition))
            )
            for partition in (left_partition, right_partition)
            for k in range(2, n + 1)
            for i in range(1, k)
        ),
        default=0.0,
    )
    base = 2 * n + 1
    encoded = encoded_jucys_murphy_operator(operators, base, n)
    observed = sorted(float(value) for value in np.linalg.eigvalsh(encoded))
    expected = expected_encoded_spectrum(left_partition, right_partition, base)
    if len(observed) != len(expected):
        raise ArithmeticError("Kronecker decomposition dimension mismatch")
    spectrum_residual = max(
        (abs(observed_value - expected_value) for observed_value, expected_value in zip(observed, expected)),
        default=0.0,
    )
    rounded_observed = Counter(round(value) for value in observed)
    expected_counts = Counter(expected)
    multiplicities = {
        target: kronecker_coefficient(left_partition, right_partition, target)
        for target in integer_partitions(n)
    }
    maximum_target = max(multiplicities, key=lambda target: (multiplicities[target], target))
    maximum_multiplicity = multiplicities[maximum_target]
    exact = rounded_observed == expected_counts and spectrum_residual < 1e-7
    return JucysMurphySectorRecord(
        n=n,
        left_partition=left_partition,
        right_partition=right_partition,
        left_dimension=left_dimension,
        right_dimension=right_dimension,
        tensor_dimension=left_dimension * right_dimension,
        diagonal_transposition_term_count=n * (n - 1) // 2,
        encoding_base=base,
        coxeter_maximum_residual=max(
            coxeter_maximum_residual(left_partition),
            coxeter_maximum_residual(right_partition),
        ),
        transposition_involution_maximum_residual=float(involution_residual),
        yjm_commutator_maximum_residual=float(commutator_residual),
        encoded_spectrum_maximum_residual=float(spectrum_residual),
        expected_joint_label_count=len(expected_counts),
        observed_joint_label_count=len(rounded_observed),
        maximum_kronecker_multiplicity=maximum_multiplicity,
        maximum_multiplicity_target=maximum_target,
        maximum_joint_eigenspace_degeneracy=max(rounded_observed.values(), default=0),
        kronecker_degeneracies_exactly_reproduced=exact,
        target_tableau_labels_resolved=exact,
        multiplicity_basis_resolved=False,
        finite_matrix_verification_only=True,
        status=(
            "label-spectrum-verified-multiplicity-unresolved"
            if exact
            else "finite-seminormal-verification-failed"
        ),
    )


def build_jucys_murphy_label_transform_report(
    n_values: Sequence[int] = (4, 5, 6),
) -> JucysMurphyLabelTransformReport:
    records = [
        audit_jucys_murphy_sector(left, right)
        for n in n_values
        for left, right in select_audit_sectors(n)
    ]
    all_verified = all(record.kronecker_degeneracies_exactly_reproduced for record in records)
    multiplicity_witnesses = sum(record.maximum_kronecker_multiplicity > 1 for record in records)
    metrics: dict[str, int | float] = {
        "record_count": len(records),
        "maximum_n": max(n_values),
        "finite_label_spectrum_verified_count": sum(
            record.kronecker_degeneracies_exactly_reproduced for record in records
        ),
        "nontrivial_multiplicity_witness_count": multiplicity_witnesses,
        "diagonal_jm_label_poly_contract_count": 1,
        "coherent_multiplicity_basis_count": 0,
        "kcopy_associator_count": 0,
        "hidden_involution_decoder_count": 0,
        "maximum_tensor_dimension": max(record.tensor_dimension for record in records),
        "maximum_kronecker_multiplicity": max(
            record.maximum_kronecker_multiplicity for record in records
        ),
        "maximum_yjm_commutator_residual": max(
            record.yjm_commutator_maximum_residual for record in records
        ),
        "maximum_encoded_spectrum_residual": max(
            record.encoded_spectrum_maximum_residual for record in records
        ),
    }
    return JucysMurphyLabelTransformReport(
        created_at=utc_now(),
        literature_scope=[
            {
                "id": "okounkov-vershik-yjm-2005",
                "url": "https://arxiv.org/abs/math/0503040",
            },
            {
                "id": "beals-symmetric-qft-1997",
                "url": "https://doi.org/10.1145/258533.258548",
            },
            {
                "id": "bravyi-et-al-kronecker-2023",
                "url": "https://arxiv.org/abs/2302.11454",
            },
            {
                "id": "ikenmeyer-subramanian-kronecker-2023",
                "url": "https://arxiv.org/abs/2307.02389",
            },
        ],
        theorem_contract={
            "input_space": "V_lambda tensor V_mu under the diagonal S_n action",
            "operators": "X_k=sum_{i<k} rho_lambda((i k)) tensor rho_mu((i k))",
            "commuting_algebra": "Young--Jucys--Murphy/Gelfand--Tsetlin algebra",
            "joint_eigenlabel": "target standard-tableau content vector",
            "decomposition": "direct_sum_nu V_nu tensor C^{g(lambda,mu,nu)}",
            "multiplicity_action": "identity on C^{g(lambda,mu,nu)}",
            "integer_content_gap": 1,
            "target_label_is_multiplicity_basis": False,
        },
        circuit_contract={
            "claim": "polynomial target-tableau label measurement, conditional on standard known primitives",
            "assumptions": [
                "uniform polynomial controlled S_n QFT and inverse QFT",
                "uniform polynomial reversible permutation multiplication",
                "standard LCU/block encoding and Hamiltonian simulation with explicit precision",
            ],
            "diagonal_group_action_implementation": (
                "Conjugate reversible multiplication by the S_n QFT to apply each Young-basis "
                "rho_lambda((i k)) tensor rho_mu((i k)) block."
            ),
            "total_diagonal_transposition_terms": "n(n-1)/2 across X_2,...,X_n",
            "required_eigenvalue_precision": "strictly less than 1/2 because contents are integers",
            "complexity_conclusion": "polynomial in n and log(1/error) under the listed primitives",
            "finite_matrix_diagonalization_used_by_circuit": False,
            "coherent_multiplicity_basis_produced": False,
        },
        records=records,
        headline_metrics=metrics,
        claim_gate={
            "finite_seminormal_verification_passed": all_verified,
            "diagonal_jm_label_measurement_polynomial_contract": True,
            "target_partition_and_tableau_label_accessible": True,
            "coherent_multiplicity_basis_proved": False,
            "internal_sn_kronecker_transform_polynomial_proved": False,
            "kcopy_associator_polynomial_proved": False,
            "hidden_involution_decoder_proved": False,
            "classical_superpolynomial_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Commuting YJM operators expose target tableau labels but are exactly degenerate on Kronecker "
                "multiplicity spaces; the state-dependent multiplicity basis, associators, and decoder remain open."
            ),
        },
        status=(
            "diagonal-label-transform-isolated-multiplicity-space-open"
            if all_verified
            else "finite-yjm-verification-failed"
        ),
        summary=(
            f"Verified diagonal YJM content spectra on {len(records)} finite Kronecker sectors through n={max(n_values)}; "
            f"{multiplicity_witnesses} sector(s) explicitly retain nontrivial unresolved multiplicity degeneracy."
        ),
        falsifiers_triggered=[
            "Target partition/tableau labels do not select a basis inside Kronecker multiplicity spaces.",
            "A polynomial diagonal-label measurement is not a full internal Kronecker transform.",
            "Finite eigendecomposition is used only as verification and is not part of the uniform circuit.",
            "Neither label extraction nor multiplicity counting supplies a hidden-involution decoder.",
        ],
    )


def write_jucys_murphy_label_transform_report(
    output_path: Path = COSET_JM_LABEL_TRANSFORM_PATH,
    n_values: Sequence[int] = (4, 5, 6),
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(build_jucys_murphy_label_transform_report(n_values=n_values))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-JM-LABELS-AS-KRONECKER-MULTIPLICITY-BASIS",
                source=str(output_path),
                claim=(
                    "Simultaneous diagonal Young--Jucys--Murphy labels implement the full internal S_n "
                    "Kronecker transform and its hidden-involution decoder."
                ),
                reason_invalid=(
                    "The YJM algebra acts identically on every copy of V_nu. Its joint eigenspaces retain exact "
                    "degeneracy g(lambda,mu,nu), so no multiplicity basis, associator, transition filter, or decoder follows."
                ),
                lesson=(
                    "Use the polynomial label transform as a front end, then state multiplicity-space control and "
                    "decoding as separate typed proof obligations."
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
                artifacts={"coset_jucys_murphy_label_transform": str(output_path)},
            )
        )
    return payload
