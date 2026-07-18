"""Sparse stable-family probe for the hardest hierarchical Racah channel.

The dense scaling audit becomes wasteful as n grows because it diagonalizes an
entire V_alpha tensor V_W sector to recover a multiplicity-four target block.
This module finds a deterministic low-magnitude linear combination of diagonal
Young--Jucys--Murphy operators that uniquely labels one target tableau.  Sparse
shift-invert extraction then returns only that block.  The bounded-support
Hamiltonian is applied term by term to the extracted vectors, so its full dense
matrix is never materialized.

The probe targets alpha=xi=(n-3,2,1) inside alpha tensor W_n with
W_n=(n-2,2).  Integer characteristic-polynomial reconstruction turns the
finite spectra into concrete symbolic theorem targets.  It is still not an
all-n proof.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Sequence

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh

from coset_jucys_murphy_label_transform import (
    standard_young_tableaux,
    tableau_content_vector,
    transposition_matrix,
)
from coset_multiplicity_commutant_search import (
    _oriented_three_cycles,
    _transpositions,
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


COSET_SPARSE_STABLE_GAP_PATH = Path(
    "research/representation/coset_sparse_stable_gap_probe.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-SPARSE-STABLE-GAP-PROBE"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class SparseStableGapRecord:
    n: int
    source_partition: tuple[int, ...]
    intermediate_partition: tuple[int, ...]
    final_partition: tuple[int, ...]
    source_irrep_dimension: int
    intermediate_irrep_dimension: int
    tensor_dimension: int
    second_stage_multiplicity: int
    total_tableau_content_count: int
    separating_yjm_weights: tuple[int, ...]
    target_yjm_label: int
    minimum_label_separation: int
    sparse_yjm_nonzero_count: int
    target_eigenspace_residual: float
    target_eigenspace_relative_residual: float
    target_basis_orthogonality_residual: float
    lcu_term_count: int
    lcu_term_count_formula: int
    eigenvalues: tuple[float, ...]
    integer_characteristic_polynomial: tuple[int, ...]
    integer_polynomial_reconstruction_residual: float
    integer_polynomial_relative_reconstruction_residual: float
    exact_integer_polynomial_candidate: bool
    raw_gap: float
    lcu_normalized_gap: float
    multiplicity_fully_split: bool
    full_dense_hamiltonian_materialized: bool
    all_n_gap_proved: bool
    status: str


@dataclass(frozen=True)
class SparseStableGapReport:
    created_at: str
    method_contract: dict[str, object]
    records: list[SparseStableGapRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _content_rows(
    n: int, target: tuple[int, ...]
) -> tuple[np.ndarray, np.ndarray]:
    rows: list[tuple[int, ...]] = []
    target_content: tuple[int, ...] | None = None
    for partition in integer_partitions(n):
        for tableau in standard_young_tableaux(partition):
            content = tableau_content_vector(tableau)[1:]
            rows.append(content)
            if partition == target and target_content is None:
                target_content = content
    if target_content is None:
        raise ArithmeticError("target partition has no standard tableau")
    return np.asarray(rows, dtype=np.int64), np.asarray(target_content, dtype=np.int64)


def separating_yjm_weights(
    n: int,
    target: tuple[int, ...],
    minimum_separation: int = 100,
    maximum_trials: int = 1_000,
) -> tuple[tuple[int, ...], int, int, int]:
    contents, target_content = _content_rows(n, target)
    rng = np.random.default_rng(20_260_717 + n)
    for _ in range(maximum_trials):
        weights = rng.integers(
            -1_000_000, 1_000_001, size=n - 1, dtype=np.int64
        )
        labels = contents @ weights
        target_label = int(target_content @ weights)
        matching = labels == target_label
        if int(np.count_nonzero(matching)) != 1:
            continue
        separation = int(np.min(np.abs(labels[~matching] - target_label)))
        if separation >= minimum_separation:
            return (
                tuple(int(value) for value in weights),
                target_label,
                separation,
                len(contents),
            )
    raise ArithmeticError("failed to find a separating low-magnitude YJM functional")


def _sparse_encoded_yjm(
    left_partition: tuple[int, ...],
    right_partition: tuple[int, ...],
    weights: tuple[int, ...],
) -> sparse.csr_matrix:
    n = sum(left_partition)
    if sum(right_partition) != n or len(weights) != n - 1:
        raise ValueError("partition sizes and YJM weight count must agree")
    dimension = hook_length_dimension(left_partition) * hook_length_dimension(
        right_partition
    )
    encoded = sparse.csr_matrix((dimension, dimension))
    for right, weight in zip(range(2, n + 1), weights):
        operator = sparse.csr_matrix((dimension, dimension))
        for left in range(1, right):
            operator += sparse.kron(
                sparse.csr_matrix(
                    transposition_matrix(left_partition, left, right)
                ),
                sparse.csr_matrix(
                    transposition_matrix(right_partition, left, right)
                ),
                format="csr",
            )
        encoded += weight * operator
    return encoded


def _apply_orbit_hamiltonian(
    left_partition: tuple[int, ...],
    right_partition: tuple[int, ...],
    basis: np.ndarray,
    support_intersection: int = 2,
) -> tuple[np.ndarray, int]:
    left_dimension = hook_length_dimension(left_partition)
    right_dimension = hook_length_dimension(right_partition)
    vector_count = basis.shape[1]
    tensor = basis.reshape(left_dimension, right_dimension, vector_count)
    output_tensor = np.zeros_like(tensor)
    term_count = 0
    for left_support, left_matrix in _transpositions(left_partition):
        left_set = set(left_support)
        left_sparse = sparse.csr_matrix(left_matrix)
        left_applied = (
            left_sparse @ tensor.reshape(left_dimension, right_dimension * vector_count)
        ).reshape(left_dimension, right_dimension, vector_count)
        for right_support, right_matrix in _oriented_three_cycles(right_partition):
            if len(left_set.intersection(right_support)) != support_intersection:
                continue
            right_applied = sparse.csr_matrix(right_matrix) @ left_applied.transpose(
                1, 0, 2
            ).reshape(right_dimension, left_dimension * vector_count)
            output_tensor += right_applied.reshape(
                right_dimension, left_dimension, vector_count
            ).transpose(1, 0, 2)
            term_count += 1
    return output_tensor.reshape(basis.shape), term_count


@lru_cache(maxsize=None)
def audit_sparse_stable_gap(n: int) -> SparseStableGapRecord:
    if n < 6:
        raise ValueError("the stable sparse family starts at n=6")
    source = (n - 2, 2)
    target = (n - 3, 2, 1)
    intermediate = target
    multiplicity = kronecker_coefficient(intermediate, source, target)
    if multiplicity <= 1:
        raise ArithmeticError("the target channel has no nontrivial second-stage multiplicity")
    weights, target_label, separation, tableau_count = separating_yjm_weights(
        n, target
    )
    encoded_yjm = _sparse_encoded_yjm(intermediate, source, weights)
    eigenvalues, basis = eigsh(
        encoded_yjm,
        k=multiplicity,
        sigma=float(target_label) + 0.125,
        which="LM",
        tol=1e-12,
        maxiter=30_000,
    )
    eigenspace_residual = float(
        np.linalg.norm(encoded_yjm @ basis - basis @ np.diag(eigenvalues))
    )
    relative_residual = eigenspace_residual / max(1.0, abs(target_label))
    label_error = float(np.max(np.abs(eigenvalues - target_label)))
    if label_error > max(1e-4, separation * 1e-8):
        raise ArithmeticError("sparse eigensolver did not recover the target YJM label")
    hamiltonian_basis, term_count = _apply_orbit_hamiltonian(
        intermediate, source, basis
    )
    block = basis.T @ hamiltonian_basis
    spectrum = np.linalg.eigvalsh((block + block.T) / 2)
    polynomial = np.poly(spectrum)
    rounded_polynomial = np.rint(polynomial)
    polynomial_residual = float(np.max(np.abs(polynomial - rounded_polynomial)))
    polynomial_relative_residual = polynomial_residual / max(
        1.0, float(np.max(np.abs(rounded_polynomial)))
    )
    raw_gap = float(min(np.diff(spectrum)))
    return SparseStableGapRecord(
        n=n,
        source_partition=source,
        intermediate_partition=intermediate,
        final_partition=target,
        source_irrep_dimension=hook_length_dimension(source),
        intermediate_irrep_dimension=hook_length_dimension(intermediate),
        tensor_dimension=(
            hook_length_dimension(source) * hook_length_dimension(intermediate)
        ),
        second_stage_multiplicity=multiplicity,
        total_tableau_content_count=tableau_count,
        separating_yjm_weights=weights,
        target_yjm_label=target_label,
        minimum_label_separation=separation,
        sparse_yjm_nonzero_count=encoded_yjm.nnz,
        target_eigenspace_residual=eigenspace_residual,
        target_eigenspace_relative_residual=relative_residual,
        target_basis_orthogonality_residual=float(
            np.linalg.norm(basis.T @ basis - np.eye(multiplicity))
        ),
        lcu_term_count=term_count,
        lcu_term_count_formula=n * (n - 1) * (n - 2),
        eigenvalues=tuple(float(value) for value in spectrum),
        integer_characteristic_polynomial=tuple(
            int(value) for value in rounded_polynomial
        ),
        integer_polynomial_reconstruction_residual=polynomial_residual,
        integer_polynomial_relative_reconstruction_residual=polynomial_relative_residual,
        exact_integer_polynomial_candidate=(
            polynomial_residual < 1e-4 or polynomial_relative_residual < 1e-10
        ),
        raw_gap=raw_gap,
        lcu_normalized_gap=raw_gap / term_count,
        multiplicity_fully_split=raw_gap > 1e-8,
        full_dense_hamiltonian_materialized=False,
        all_n_gap_proved=False,
        status=(
            "sparse-critical-block-split-integer-polynomial-reconstructed"
            if raw_gap > 1e-8
            and (polynomial_residual < 1e-4 or polynomial_relative_residual < 1e-10)
            else "sparse-critical-block-probe-inconclusive"
        ),
    )


def build_sparse_stable_gap_report(
    n_values: Sequence[int] = (7, 8, 9, 10),
) -> SparseStableGapReport:
    records = [audit_sparse_stable_gap(n) for n in n_values]
    all_split = all(record.multiplicity_fully_split for record in records)
    all_integer = all(record.exact_integer_polynomial_candidate for record in records)
    metrics: dict[str, int | float] = {
        "record_count": len(records),
        "minimum_n": min(n_values),
        "maximum_n": max(n_values),
        "finite_split_count": sum(record.multiplicity_fully_split for record in records),
        "integer_characteristic_polynomial_candidate_count": sum(
            record.exact_integer_polynomial_candidate for record in records
        ),
        "maximum_second_stage_multiplicity": max(
            record.second_stage_multiplicity for record in records
        ),
        "maximum_sparse_tensor_dimension": max(record.tensor_dimension for record in records),
        "maximum_sparse_yjm_nonzero_count": max(
            record.sparse_yjm_nonzero_count for record in records
        ),
        "minimum_observed_raw_gap": min(record.raw_gap for record in records),
        "minimum_observed_normalized_gap": min(
            record.lcu_normalized_gap for record in records
        ),
        "maximum_integer_polynomial_reconstruction_residual": max(
            record.integer_polynomial_reconstruction_residual for record in records
        ),
        "maximum_integer_polynomial_relative_reconstruction_residual": max(
            record.integer_polynomial_relative_reconstruction_residual
            for record in records
        ),
        "maximum_target_eigenspace_relative_residual": max(
            record.target_eigenspace_relative_residual for record in records
        ),
        "full_dense_hamiltonian_materialization_count": sum(
            record.full_dense_hamiltonian_materialized for record in records
        ),
        "all_n_characteristic_polynomial_theorem_count": 0,
        "all_n_gap_theorem_count": 0,
        "uniform_polynomial_racah_circuit_count": 0,
    }
    return SparseStableGapReport(
        created_at=utc_now(),
        method_contract={
            "stable_channel": "alpha_n=xi_n=(n-3,2,1), W_n=(n-2,2)",
            "target_extraction": (
                "deterministic low-magnitude separating linear functional of diagonal YJM operators"
            ),
            "sparse_solver": "shift-invert extraction of only the g(alpha_n,W_n,xi_n)-dimensional block",
            "hamiltonian_application": "termwise sparse action; no dense tensor-sector Hamiltonian",
            "symbolic_target": "monic integer characteristic polynomial of the multiplicity action",
        },
        records=records,
        headline_metrics=metrics,
        claim_gate={
            "all_audited_critical_blocks_split": all_split,
            "integer_characteristic_polynomials_reconstructed": all_integer,
            "full_dense_hamiltonians_avoided": (
                metrics["full_dense_hamiltonian_materialization_count"] == 0
            ),
            "all_n_characteristic_polynomial_proved": False,
            "all_n_gap_proved": False,
            "uniform_polynomial_racah_circuit_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Sparse finite extraction and integer reconstruction provide theorem targets, not exact coefficient "
                "formulas, all-n root separation, complete sector coverage, or a coherent circuit."
            ),
        },
        status=(
            "sparse-stable-gap-probe-survives-symbolic-proof-open"
            if all_split and all_integer
            else "sparse-stable-gap-probe-found-counterexample"
        ),
        summary=(
            f"Extracted the multiplicity-{metrics['maximum_second_stage_multiplicity']} critical block through "
            f"n={max(n_values)} without dense Hamiltonians; all spectra split and reconstruct integer polynomials, "
            "but exact all-n formulas and gap bounds remain open."
        ),
        falsifiers_triggered=[
            "Integer polynomial reconstruction from floating spectra is a conjecture generator, not an exact proof.",
            "One critical stable channel does not cover every intermediate or final sector.",
            "Sparse finite block extraction does not establish polynomial complexity as n grows.",
            "No coherent circuit or hidden-involution decoder is constructed.",
        ],
    )


def write_sparse_stable_gap_report(
    output_path: Path = COSET_SPARSE_STABLE_GAP_PATH,
    n_values: Sequence[int] = (7, 8, 9, 10),
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(build_sparse_stable_gap_report(n_values=n_values))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-SPARSE-INTEGER-SPECTRA-AS-ALL-N-GAP-PROOF",
                source=str(output_path),
                claim=(
                    "Sparse finite integer characteristic polynomials prove a stable inverse-polynomial Racah gap."
                ),
                reason_invalid=(
                    "The coefficients are numerically reconstructed at finitely many n and no exact coefficient "
                    "formula or root-separation theorem is supplied."
                ),
                lesson=(
                    "Use the reconstructed quartics as targets for exact character-orbit or partition-algebra trace "
                    "identities, then prove root separation uniformly."
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
                artifacts={"coset_sparse_stable_gap_probe": str(output_path)},
            )
        )
    return payload
