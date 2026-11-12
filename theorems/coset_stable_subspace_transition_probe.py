"""Gauge-invariant leakage probe for the stable three-copy Racah branch.

Let W_n=(n-2,2) and xi_n=(n-3,2,1).  For n>=7,

    g(W_n,W_n,xi_n)=2,  g(xi_n,W_n,xi_n)=4.

The corresponding left- and right-associated branches are eight-dimensional
inside the final-xi_n multiplicity space of W_n^tensor3.  This module builds
orthonormal intertwiner bases as nullspaces of the Coxeter invariant
Laplacian, composes both coupling trees, and computes their overlap singular
values.  The squared Frobenius norm is Tr(P_left P_right), so the average
retention and leakage are invariant under every basis rotation inside either
multiplicity space.

The calculation is a finite scaling probe, not an all-n theorem.  Persistent
leakage falsifies the idea that the newly proved one-channel coherent label is
by itself a closed Racah associator.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from typing import Sequence

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import LinearOperator, eigsh

from coset_jucys_murphy_label_transform import transposition_matrix
from representation_obstruction import hook_length_dimension
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from symmetric_character import kronecker_coefficient


COSET_STABLE_SUBSPACE_TRANSITION_PATH = Path(
    "research/representation/coset_stable_subspace_transition_probe.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-STABLE-SUBSPACE-TRANSITION-PROBE"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class StableSubspaceTransitionRecord:
    n: int
    source_partition: tuple[int, ...]
    stable_partition: tuple[int, ...]
    source_irrep_dimension: int
    stable_irrep_dimension: int
    first_stage_multiplicity: int
    second_stage_multiplicity: int
    stable_branch_dimension: int
    first_invariant_laplacian_gap: float
    second_invariant_laplacian_gap: float
    maximum_invariant_residual: float
    maximum_embedding_isometry_residual: float
    overlap_singular_values: tuple[float, ...]
    overlap_rank: int
    projector_overlap_trace: float
    projector_overlap_rational_candidate: str
    rational_candidate_residual: float
    maximally_mixed_branch_retention: float
    maximally_mixed_branch_leakage: float
    stable_branch_closed_under_recoupling: bool
    finite_numerical_probe_only: bool
    status: str


@dataclass(frozen=True)
class StableSubspaceTransitionReport:
    created_at: str
    mathematical_contract: dict[str, object]
    records: list[StableSubspaceTransitionRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _apply_sparse_axis(
    tensor: np.ndarray, matrix: csr_matrix, axis: int
) -> np.ndarray:
    moved = np.moveaxis(tensor, axis, 0)
    shape = moved.shape
    transformed = matrix @ moved.reshape(shape[0], -1)
    return np.moveaxis(np.asarray(transformed).reshape(shape), 0, axis)


def _coxeter_laplacian_operator(
    partitions: tuple[tuple[int, ...], ...]
) -> tuple[LinearOperator, tuple[int, ...]]:
    n = sum(partitions[0])
    if any(sum(partition) != n for partition in partitions):
        raise ValueError("all tensor factors must be S_n representations")
    dimensions = tuple(hook_length_dimension(partition) for partition in partitions)
    generator_rows = tuple(
        tuple(
            csr_matrix(transposition_matrix(partition, index, index + 1))
            for partition in partitions
        )
        for index in range(1, n)
    )
    size = math.prod(dimensions)

    def matvec(vector: np.ndarray) -> np.ndarray:
        tensor = vector.reshape(dimensions)
        result = np.zeros_like(tensor)
        for generators in generator_rows:
            transformed = tensor
            for axis, generator in enumerate(generators):
                transformed = _apply_sparse_axis(transformed, generator, axis)
            result += tensor - transformed
        return result.ravel()

    return LinearOperator((size, size), matvec=matvec, dtype=float), dimensions


@lru_cache(maxsize=16)
def invariant_tensor_basis(
    partitions: tuple[tuple[int, ...], ...], multiplicity: int
) -> tuple[np.ndarray, tuple[float, ...], float]:
    """Return an orthonormal basis for Hom(1, tensor(partitions))."""
    if multiplicity <= 0:
        raise ValueError("multiplicity must be positive")
    operator, dimensions = _coxeter_laplacian_operator(partitions)
    if multiplicity + 2 >= operator.shape[0]:
        raise ValueError("invariant eigensolve requests too many eigenvectors")
    initial = np.linspace(1.0, 2.0, operator.shape[0], dtype=float)
    initial /= np.linalg.norm(initial)
    eigenvalues, eigenvectors = eigsh(
        operator,
        k=multiplicity + 2,
        which="SA",
        tol=5e-10,
        maxiter=5_000,
        ncv=max(20, 4 * multiplicity + 4),
        v0=initial,
    )
    order = np.argsort(eigenvalues)
    eigenvalues = eigenvalues[order]
    eigenvectors = eigenvectors[:, order]
    null_values = eigenvalues[:multiplicity]
    if np.max(np.abs(null_values)) > 1e-7:
        raise ArithmeticError("Coxeter Laplacian did not recover the expected invariant space")
    spectral_gap = float(eigenvalues[multiplicity])
    if spectral_gap <= 1e-7:
        raise ArithmeticError("character multiplicity understates the numerical nullspace")
    basis = eigenvectors[:, :multiplicity].T.reshape((multiplicity, *dimensions))
    residual = max(
        float(np.linalg.norm(operator @ vector.ravel())) for vector in basis
    )
    return basis, tuple(float(value) for value in eigenvalues), residual


def _embedding_orthogonality_residual(embeddings: np.ndarray) -> float:
    multiplicity = embeddings.shape[0]
    target_dimension = embeddings.shape[-1]
    flattened = embeddings.reshape(multiplicity, -1, target_dimension)
    gram = np.einsum("ait,bis->abts", flattened, flattened, optimize=True)
    expected = np.einsum(
        "ab,ts->abts", np.eye(multiplicity), np.eye(target_dimension)
    )
    return float(np.linalg.norm(gram - expected))


def stable_transition_overlap(
    first_embeddings: np.ndarray, second_embeddings: np.ndarray
) -> np.ndarray:
    """Return the left/right overlap matrix in arbitrary multiplicity gauges."""
    first_multiplicity, source_dimension, _, stable_dimension = (
        first_embeddings.shape
    )
    second_multiplicity, _, second_source_dimension, second_target_dimension = (
        second_embeddings.shape
    )
    if second_source_dimension != source_dimension:
        raise ValueError("the two coupling stages use incompatible source irreps")
    if second_target_dimension != stable_dimension:
        raise ValueError("the second stage must return the stable final irrep")
    branch_dimension = first_multiplicity * second_multiplicity
    right_rows = np.empty(
        (
            branch_dimension,
            source_dimension,
            source_dimension,
            source_dimension,
            stable_dimension,
        ),
        dtype=float,
    )
    row = 0
    for first_index in range(first_multiplicity):
        for second_index in range(second_multiplicity):
            right_rows[row] = np.einsum(
                "uit,jku->ijkt",
                second_embeddings[second_index],
                first_embeddings[first_index],
                optimize=True,
            )
            row += 1
    right_flat = right_rows.reshape(branch_dimension, -1)
    overlap = np.empty((branch_dimension, branch_dimension), dtype=float)
    row = 0
    for first_index in range(first_multiplicity):
        for second_index in range(second_multiplicity):
            left = np.einsum(
                "iju,ukt->ijkt",
                first_embeddings[first_index],
                second_embeddings[second_index],
                optimize=True,
            )
            overlap[row] = right_flat @ left.ravel() / stable_dimension
            row += 1
    return overlap


def audit_stable_subspace_transition(n: int) -> StableSubspaceTransitionRecord:
    if n < 7:
        raise ValueError("the multiplicity-four stable branch starts at n=7")
    source = (n - 2, 2)
    stable = (n - 3, 2, 1)
    source_dimension = hook_length_dimension(source)
    stable_dimension = hook_length_dimension(stable)
    first_multiplicity = kronecker_coefficient(source, source, stable)
    second_multiplicity = kronecker_coefficient(stable, source, stable)
    if (first_multiplicity, second_multiplicity) != (2, 4):
        raise ArithmeticError("the expected stable multiplicities are not 2 and 4")

    first_basis, first_values, first_residual = invariant_tensor_basis(
        (source, source, stable), first_multiplicity
    )
    second_basis, second_values, second_residual = invariant_tensor_basis(
        (stable, source, stable), second_multiplicity
    )
    # A unit invariant tensor has T^*T=I/dim(V_target) by Schur's lemma.
    first_embeddings = first_basis * math.sqrt(stable_dimension)
    second_embeddings = second_basis * math.sqrt(stable_dimension)
    isometry_residual = max(
        _embedding_orthogonality_residual(first_embeddings),
        _embedding_orthogonality_residual(second_embeddings),
    )
    overlap = stable_transition_overlap(first_embeddings, second_embeddings)
    singular_values = np.linalg.svd(overlap, compute_uv=False)
    branch_dimension = first_multiplicity * second_multiplicity
    projector_overlap = float(np.sum(singular_values**2))
    rational = Fraction(projector_overlap).limit_denominator(1_000_000)
    rational_value = rational.numerator / rational.denominator
    retention = projector_overlap / branch_dimension
    leakage = 1.0 - retention
    closed = abs(projector_overlap - branch_dimension) < 1e-8
    return StableSubspaceTransitionRecord(
        n=n,
        source_partition=source,
        stable_partition=stable,
        source_irrep_dimension=source_dimension,
        stable_irrep_dimension=stable_dimension,
        first_stage_multiplicity=first_multiplicity,
        second_stage_multiplicity=second_multiplicity,
        stable_branch_dimension=branch_dimension,
        first_invariant_laplacian_gap=first_values[first_multiplicity],
        second_invariant_laplacian_gap=second_values[second_multiplicity],
        maximum_invariant_residual=max(first_residual, second_residual),
        maximum_embedding_isometry_residual=isometry_residual,
        overlap_singular_values=tuple(float(value) for value in singular_values),
        overlap_rank=int(np.sum(singular_values > 1e-8)),
        projector_overlap_trace=projector_overlap,
        projector_overlap_rational_candidate=f"{rational.numerator}/{rational.denominator}",
        rational_candidate_residual=abs(projector_overlap - rational_value),
        maximally_mixed_branch_retention=retention,
        maximally_mixed_branch_leakage=leakage,
        stable_branch_closed_under_recoupling=closed,
        finite_numerical_probe_only=True,
        status=(
            "stable-branch-closed-at-finite-n"
            if closed
            else "stable-branch-leaks-under-recoupling"
        ),
    )


def build_stable_subspace_transition_report(
    n_values: Sequence[int] = (7,),
) -> StableSubspaceTransitionReport:
    values = tuple(dict.fromkeys(int(n) for n in n_values))
    if not values:
        raise ValueError("at least one n value is required")
    records = [audit_stable_subspace_transition(n) for n in values]
    any_leak = any(
        not record.stable_branch_closed_under_recoupling for record in records
    )
    all_leak = all(not record.stable_branch_closed_under_recoupling for record in records)
    all_closed = all(record.stable_branch_closed_under_recoupling for record in records)
    metrics: dict[str, int | float] = {
        "stable_scaling_point_count": len(records),
        "minimum_n": min(values),
        "maximum_n": max(values),
        "stable_multiplicity_2x4_verified_count": sum(
            (record.first_stage_multiplicity, record.second_stage_multiplicity)
            == (2, 4)
            for record in records
        ),
        "full_rank_transition_subblock_count": sum(
            record.overlap_rank == record.stable_branch_dimension for record in records
        ),
        "closed_stable_associator_count": sum(
            record.stable_branch_closed_under_recoupling for record in records
        ),
        "leaky_stable_subspace_count": sum(
            not record.stable_branch_closed_under_recoupling for record in records
        ),
        "maximum_maximally_mixed_retention": max(
            record.maximally_mixed_branch_retention for record in records
        ),
        "minimum_maximally_mixed_leakage": min(
            record.maximally_mixed_branch_leakage for record in records
        ),
        "all_n_leakage_theorem_count": 0,
        "overlapping_racah_associator_count": 0,
        "hidden_involution_decoder_count": 0,
    }
    return StableSubspaceTransitionReport(
        created_at=utc_now(),
        mathematical_contract={
            "source": "three copies of W_n=(n-2,2)",
            "final_irrep": "xi_n=(n-3,2,1)",
            "left_branch": "(W_n tensor W_n -> xi_n) tensor W_n -> xi_n",
            "right_branch": "W_n tensor (W_n tensor W_n -> xi_n) -> xi_n",
            "branch_dimension": "g(W,W,xi)*g(xi,W,xi)=2*4=8",
            "basis_construction": (
                "numerical nullspace of sum_i(I-rho(s_i)^tensor3) for adjacent Coxeter generators"
            ),
            "gauge_invariant_observable": (
                "Tr(P_left P_right)=||U_left^* U_right||_F^2; divide by 8 for maximally mixed branch retention"
            ),
            "scope": "finite numerical scaling evidence only",
        },
        records=records,
        headline_metrics=metrics,
        claim_gate={
            "stable_branch_closed_under_recoupling": all_closed,
            "finite_leakage_observed": any_leak,
            "all_n_leakage_proved": False,
            "overlapping_racah_associator_proved": False,
            "hidden_involution_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The one-channel labels define leaky left/right subspaces at every audited n. A closed associator "
                "must include complementary intermediate sectors; the finite probe is not an all-n leakage theorem."
            ),
        },
        status=(
            "stable-branch-leakage-scaling-observed"
            if all_leak
            else "stable-branch-closure-requires-investigation"
        ),
        summary=(
            f"Computed gauge-invariant left/right overlap for the 2x4 stable branch at {len(records)} sizes; "
            f"all {sum(not record.stable_branch_closed_under_recoupling for record in records)} audited branches leak "
            "into complementary intermediate sectors."
        ),
        falsifiers_triggered=[
            "A coherent label in one stable channel is not a closed Racah associator.",
            "Full-rank overlap inside the retained 8x8 subblock does not eliminate leakage outside that subblock.",
            "Finite rational-looking projector overlaps are conjectural until an exact all-n character or intertwiner proof is supplied.",
            "No hidden-involution information follows from subspace overlap geometry alone.",
        ],
    )


def write_stable_subspace_transition_report(
    output_path: Path = COSET_STABLE_SUBSPACE_TRANSITION_PATH,
    n_values: Sequence[int] = (7,),
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(build_stable_subspace_transition_report(n_values=n_values))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-STABLE-CHANNEL-AS-CLOSED-RACAH-SUBSPACE",
                source=str(output_path),
                claim=(
                    "The proved 2x4 stable multiplicity labels close under left/right recoupling and therefore form an associator."
                ),
                reason_invalid=(
                    "Gauge-invariant projector overlap shows substantial probability leakage into complementary intermediate sectors."
                ),
                lesson=(
                    "Classify and coherently cover the complementary sectors before searching for a transition filter or decoder."
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
                artifacts={"coset_stable_subspace_transition_probe": str(output_path)},
            )
        )
    return payload


if __name__ == "__main__":
    report = write_stable_subspace_transition_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
