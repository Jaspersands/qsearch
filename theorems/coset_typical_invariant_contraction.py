"""Sparse invariant and YJM-fiber contraction for typical Kronecker blocks.

For invariant tensors in ``nu tensor lambda tensor lambda``, matrix elements
of a simultaneous-conjugacy orbit average equal matrix elements of one orbit
representative.  A direct Coxeter solve proves the identity on controls but
scales in ``dim(nu) * dim(lambda)^2``.  The primary implementation instead
isolates one Jucys-Murphy tableau fiber inside ``V_lambda tensor V_lambda`` and
propagates it through the target tableaux.  This removes the ``dim(nu)`` factor
from the eigensolve, but is still not claimed to scale polynomially.
"""

from __future__ import annotations

import hashlib
import json
import math
import time
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import eigsh

from coset_jucys_murphy_label_transform import transposition_matrix
from coset_stable_subspace_transition_probe import (
    _apply_sparse_axis,
    _coxeter_laplacian_operator,
)
from representation_obstruction import hook_length_dimension
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from symmetric_yjm_multiplicity_contraction import yjm_separator_block


CERTIFICATE_PATH = Path(
    "research/certificates/coset_typical_invariant_contraction_certificate.json"
)
REPORT_PATH = Path(
    "research/representation/coset_typical_invariant_contraction.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-TYPICAL-INVARIANT-CONTRACTION"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
SOURCE_PARTITION = (4, 3, 2, 1)
CONTROL_TARGET = (9, 1)
NEXT_TARGET = (5, 5)
EXACT_CONTROL_TRACES = (
    Fraction(-7, 48),
    Fraction(7247, 1016064),
    Fraction(-815, 2322432),
)
DEPENDENCY_PATHS = (
    Path("coset_stable_subspace_transition_probe.py"),
    Path("coset_jucys_murphy_label_transform.py"),
    Path("symmetric_yjm_multiplicity_contraction.py"),
)


@dataclass(frozen=True)
class InvariantContractionRecord:
    n: int
    source_partition: tuple[int, ...]
    target_partition: tuple[int, ...]
    source_dimension: int
    target_dimension: int
    kronecker_multiplicity: int
    invariant_vector_dimension: int
    arpack_subspace_dimension: int
    estimated_arpack_basis_bytes: int
    coxeter_laplacian_eigenvalues: list[float]
    coxeter_laplacian_gap: float
    maximum_invariant_residual: float
    restricted_separator_matrix: list[list[float]]
    restricted_symmetry_residual: float
    separator_eigenvalues: list[float]
    numerical_power_traces: list[float]
    minimum_numerical_raw_gap: float
    exact_control_power_traces: list[str]
    maximum_exact_control_trace_residual: float
    explicit_group_rows_materialized: bool
    orbit_terms_materialized: bool
    finite_numerical_probe_only: bool
    status: str


@dataclass(frozen=True)
class YJMContractionRecord:
    n: int
    source_partition: tuple[int, ...]
    target_partition: tuple[int, ...]
    source_dimension: int
    target_dimension: int
    kronecker_multiplicity: int
    fiber_vector_dimension: int
    direct_invariant_vector_dimension: int
    vector_dimension_reduction_factor: int
    arpack_subspace_dimension: int
    estimated_arpack_basis_bytes: int
    penalty_eigenvalues: list[float]
    penalty_gap: float
    maximum_penalty_residual: float
    tableau_fiber_count: int
    maximum_fiber_orthogonality_residual: float
    maximum_tableau_propagation_residual: float
    restricted_separator_matrix: list[list[float]]
    restricted_symmetry_residual: float
    separator_eigenvalues: list[float]
    numerical_power_traces: list[float]
    minimum_numerical_raw_gap: float
    exact_control_power_traces: list[str]
    maximum_exact_control_trace_residual: float
    explicit_group_rows_materialized: bool
    orbit_terms_materialized: bool
    finite_numerical_probe_only: bool
    status: str


@dataclass(frozen=True)
class InvariantContractionReport:
    created_at: str
    contraction_contract: dict[str, object]
    records: list[YJMContractionRecord]
    robustness_audit: dict[str, object]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def numerical_invariant_basis(
    partitions: tuple[tuple[int, ...], ...],
    multiplicity: int,
    *,
    arpack_subspace_dimension: int | None = None,
) -> tuple[np.ndarray, tuple[float, ...], float, int]:
    """Compute a numerical basis for diagonal-S_n invariant tensors."""

    if multiplicity < 1:
        raise ValueError("multiplicity must be positive")
    operator, dimensions = _coxeter_laplacian_operator(partitions)
    eigenvector_count = multiplicity + 2
    ncv = arpack_subspace_dimension or max(
        eigenvector_count + 2,
        2 * multiplicity + 4,
    )
    if not eigenvector_count < ncv < operator.shape[0]:
        raise ValueError("ARPACK subspace must exceed k and remain below dimension")
    initial = np.linspace(1.0, 2.0, operator.shape[0], dtype=float)
    initial /= np.linalg.norm(initial)
    eigenvalues, eigenvectors = eigsh(
        operator,
        k=eigenvector_count,
        which="SA",
        tol=5e-10,
        maxiter=5_000,
        ncv=ncv,
        v0=initial,
    )
    order = np.argsort(eigenvalues)
    eigenvalues = eigenvalues[order]
    eigenvectors = eigenvectors[:, order]
    if float(np.max(np.abs(eigenvalues[:multiplicity]))) > 1e-7:
        raise ArithmeticError("Coxeter solve missed the expected invariant nullspace")
    if float(eigenvalues[multiplicity]) <= 1e-7:
        raise ArithmeticError("character multiplicity understates invariant nullity")
    basis = eigenvectors[:, :multiplicity].T.reshape((multiplicity, *dimensions))
    residual = max(
        float(np.linalg.norm(operator @ vector.ravel())) for vector in basis
    )
    return (
        basis,
        tuple(float(value) for value in eigenvalues),
        residual,
        ncv,
    )


def restricted_separator_matrix(
    basis: np.ndarray,
    source_partition: tuple[int, ...],
) -> tuple[np.ndarray, float]:
    """Restrict average(TT1)+average(TC1) using one representative each."""

    if basis.ndim != 4 or basis.shape[2] != basis.shape[3]:
        raise ValueError("expected basis shape (multiplicity,target,source,source)")
    tt_left = csr_matrix(transposition_matrix(source_partition, 1, 2))
    tt_right = csr_matrix(transposition_matrix(source_partition, 1, 3))
    tc_right = csr_matrix(
        transposition_matrix(source_partition, 1, 3)
        @ transposition_matrix(source_partition, 3, 4)
    )

    def apply_pair(left: csr_matrix, right: csr_matrix) -> np.ndarray:
        transformed = _apply_sparse_axis(basis, left, 2)
        return _apply_sparse_axis(transformed, right, 3)

    transformed = apply_pair(tt_left, tt_right) + apply_pair(tt_left, tc_right)
    block = np.einsum(
        "maij,naij->mn",
        basis,
        transformed,
        optimize=True,
    )
    symmetry_residual = float(np.linalg.norm(block - block.T))
    return (block + block.T) / 2, symmetry_residual


def audit_invariant_contraction_block(
    target_partition: tuple[int, ...],
    multiplicity: int,
    *,
    source_partition: tuple[int, ...] = SOURCE_PARTITION,
    arpack_subspace_dimension: int | None = None,
) -> InvariantContractionRecord:
    n = sum(source_partition)
    if sum(target_partition) != n:
        raise ValueError("source and target must be partitions of the same n")
    basis, laplacian, residual, ncv = numerical_invariant_basis(
        (target_partition, source_partition, source_partition),
        multiplicity,
        arpack_subspace_dimension=arpack_subspace_dimension,
    )
    block, symmetry_residual = restricted_separator_matrix(
        basis,
        source_partition,
    )
    eigenvalues = np.linalg.eigvalsh(block)
    traces = [
        float(np.sum(eigenvalues**degree))
        for degree in range(1, multiplicity + 1)
    ]
    exact_control = (
        EXACT_CONTROL_TRACES
        if target_partition == CONTROL_TARGET
        and source_partition == SOURCE_PARTITION
        else ()
    )
    control_residual = max(
        (
            abs(numerical - float(exact))
            for numerical, exact in zip(traces, exact_control)
        ),
        default=0.0,
    )
    if exact_control and control_residual > 1e-9:
        raise ArithmeticError("invariant contraction misses exact control traces")
    source_dimension = hook_length_dimension(source_partition)
    target_dimension = hook_length_dimension(target_partition)
    vector_dimension = target_dimension * source_dimension * source_dimension
    minimum_gap = float(min(np.diff(eigenvalues), default=math.inf))
    return InvariantContractionRecord(
        n=n,
        source_partition=source_partition,
        target_partition=target_partition,
        source_dimension=source_dimension,
        target_dimension=target_dimension,
        kronecker_multiplicity=multiplicity,
        invariant_vector_dimension=vector_dimension,
        arpack_subspace_dimension=ncv,
        estimated_arpack_basis_bytes=ncv * vector_dimension * 8,
        coxeter_laplacian_eigenvalues=list(laplacian),
        coxeter_laplacian_gap=laplacian[multiplicity],
        maximum_invariant_residual=residual,
        restricted_separator_matrix=block.tolist(),
        restricted_symmetry_residual=symmetry_residual,
        separator_eigenvalues=eigenvalues.tolist(),
        numerical_power_traces=traces,
        minimum_numerical_raw_gap=minimum_gap,
        exact_control_power_traces=[str(value) for value in exact_control],
        maximum_exact_control_trace_residual=control_residual,
        explicit_group_rows_materialized=False,
        orbit_terms_materialized=False,
        finite_numerical_probe_only=True,
        status=(
            "exact-control-reproduced-by-invariant-contraction"
            if exact_control
            else (
                "numerically-simple-spectrum-exact-certificate-required"
                if minimum_gap > 1e-7
                else "numerical-collision-detected"
            )
        ),
    )


def audit_yjm_contraction_block(
    target_partition: tuple[int, ...],
    multiplicity: int,
    *,
    source_partition: tuple[int, ...] = SOURCE_PARTITION,
    arpack_subspace_dimension: int | None = None,
) -> YJMContractionRecord:
    """Contract one multiplicity block through a sparse YJM tableau fiber."""

    block, metrics = yjm_separator_block(
        source_partition,
        target_partition,
        multiplicity,
        arpack_subspace_dimension=arpack_subspace_dimension,
    )
    eigenvalues = np.linalg.eigvalsh(block)
    traces = [
        float(np.sum(eigenvalues**degree))
        for degree in range(1, multiplicity + 1)
    ]
    exact_control = (
        EXACT_CONTROL_TRACES
        if target_partition == CONTROL_TARGET
        and source_partition == SOURCE_PARTITION
        else ()
    )
    control_residual = max(
        (
            abs(numerical - float(exact))
            for numerical, exact in zip(traces, exact_control)
        ),
        default=0.0,
    )
    if exact_control and control_residual > 1e-9:
        raise ArithmeticError("YJM contraction misses exact control traces")
    minimum_gap = float(min(np.diff(eigenvalues), default=math.inf))
    return YJMContractionRecord(
        n=metrics.n,
        source_partition=metrics.source_partition,
        target_partition=metrics.target_partition,
        source_dimension=metrics.source_dimension,
        target_dimension=metrics.target_dimension,
        kronecker_multiplicity=metrics.multiplicity,
        fiber_vector_dimension=metrics.fiber_vector_dimension,
        direct_invariant_vector_dimension=(
            metrics.direct_invariant_vector_dimension
        ),
        vector_dimension_reduction_factor=(
            metrics.vector_dimension_reduction_factor
        ),
        arpack_subspace_dimension=metrics.arpack_subspace_dimension,
        estimated_arpack_basis_bytes=metrics.estimated_arpack_basis_bytes,
        penalty_eigenvalues=list(metrics.penalty_eigenvalues),
        penalty_gap=metrics.penalty_gap,
        maximum_penalty_residual=metrics.maximum_penalty_residual,
        tableau_fiber_count=metrics.tableau_fiber_count,
        maximum_fiber_orthogonality_residual=(
            metrics.maximum_fiber_orthogonality_residual
        ),
        maximum_tableau_propagation_residual=(
            metrics.maximum_tableau_propagation_residual
        ),
        restricted_separator_matrix=block.tolist(),
        restricted_symmetry_residual=float(np.linalg.norm(block - block.T)),
        separator_eigenvalues=eigenvalues.tolist(),
        numerical_power_traces=traces,
        minimum_numerical_raw_gap=minimum_gap,
        exact_control_power_traces=[str(value) for value in exact_control],
        maximum_exact_control_trace_residual=control_residual,
        explicit_group_rows_materialized=False,
        orbit_terms_materialized=False,
        finite_numerical_probe_only=True,
        status=(
            "exact-control-reproduced-by-yjm-fiber-contraction"
            if exact_control
            else (
                "numerically-simple-spectrum-exact-certificate-required"
                if minimum_gap > 1e-7
                else "numerical-collision-detected"
            )
        ),
    )


def _dependency_hashes() -> dict[str, str]:
    root = Path(__file__).resolve().parent
    return {
        str(path): hashlib.sha256((root / path).read_bytes()).hexdigest()
        for path in DEPENDENCY_PATHS
    }


def write_numerical_certificate(
    path: Path = CERTIFICATE_PATH,
) -> dict:
    started = time.perf_counter()
    records = [
        audit_yjm_contraction_block(
            CONTROL_TARGET,
            3,
            arpack_subspace_dimension=12,
        ),
        audit_yjm_contraction_block(
            NEXT_TARGET,
            6,
            arpack_subspace_dimension=16,
        ),
    ]
    payload = {
        "certificate_contract": {
            "dependency_sha256": _dependency_hashes(),
            "solver": (
                "ARPACK diagonal-YJM content-penalty eigensolve plus exact "
                "seminormal tableau propagation"
            ),
            "tolerance": 5e-10,
            "scope": "finite numerical n=10 contraction, not an exact or all-n theorem",
            "direct_coxeter_control_seconds": 462.8272747993469,
            "direct_coxeter_multiplicity6_timeout_seconds": 4100,
            "elapsed_seconds": time.perf_counter() - started,
        },
        "records": [asdict(record) for record in records],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


def _load_certificate(path: Path = CERTIFICATE_PATH) -> dict:
    resolved = path
    if not resolved.exists():
        resolved = Path(__file__).resolve().parent / path
    payload = json.loads(resolved.read_text())
    if payload.get("certificate_contract", {}).get(
        "dependency_sha256"
    ) != _dependency_hashes():
        raise ArithmeticError("invariant-contraction dependency hash changed")
    return payload


def _validated_stored_records(certificate: dict) -> list[YJMContractionRecord]:
    records = [
        YJMContractionRecord(**row)
        for row in certificate.get("records", [])
    ]
    if [tuple(record.target_partition) for record in records] != [
        CONTROL_TARGET,
        NEXT_TARGET,
    ]:
        raise ArithmeticError("invariant-contraction certificate targets changed")
    for record in records:
        eigenvalues = np.array(record.separator_eigenvalues)
        traces = [
            float(np.sum(eigenvalues**degree))
            for degree in range(1, record.kronecker_multiplicity + 1)
        ]
        if not np.allclose(traces, record.numerical_power_traces, atol=1e-11):
            raise ArithmeticError("stored invariant power traces are inconsistent")
        if record.maximum_penalty_residual > 1e-7:
            raise ArithmeticError("stored YJM penalty residual is too large")
        if record.maximum_fiber_orthogonality_residual > 1e-7:
            raise ArithmeticError("stored YJM fiber is not orthonormal")
        if record.maximum_tableau_propagation_residual > 1e-7:
            raise ArithmeticError("stored tableau propagation is inconsistent")
        if record.tableau_fiber_count != record.target_dimension:
            raise ArithmeticError("stored YJM fibers do not cover the target")
        if record.restricted_symmetry_residual > 1e-8:
            raise ArithmeticError("stored separator block is not symmetric")
    control = records[0]
    residual = max(
        abs(numerical - float(exact))
        for numerical, exact in zip(
            control.numerical_power_traces,
            EXACT_CONTROL_TRACES,
        )
    )
    if residual > 1e-9:
        raise ArithmeticError("stored control does not reproduce exact traces")
    return records


def _declared_error_budget_audit(
    record: YJMContractionRecord,
    *,
    normwise_roundoff_budget: float = 1e-6,
) -> dict[str, object]:
    """Give a conservative conditional, not interval-verified, gap bound."""

    if normwise_roundoff_budget <= 0:
        raise ValueError("roundoff budget must be positive")
    exact_penalty_gap_lower_bound = 1.0
    root_subspace_distance = (
        math.sqrt(record.kronecker_multiplicity)
        * (record.maximum_penalty_residual + normwise_roundoff_budget)
        / exact_penalty_gap_lower_bound
    )
    cumulative_tableau_error = (
        max(0, record.tableau_fiber_count - 1)
        * (
            record.maximum_tableau_propagation_residual
            + normwise_roundoff_budget
        )
    )
    block_operator_error = (
        16 * root_subspace_distance
        + 8 * (
            record.maximum_fiber_orthogonality_residual
            + cumulative_tableau_error
        )
        + normwise_roundoff_budget
    )
    conditional_gap_lower = (
        record.minimum_numerical_raw_gap - 2 * block_operator_error
    )
    collision_perturbation_radius = (
        record.minimum_numerical_raw_gap / 2
    )
    return {
        "target_partition": list(record.target_partition),
        "normwise_roundoff_budget_assumption": normwise_roundoff_budget,
        "exact_yjm_penalty_gap_lower_bound": exact_penalty_gap_lower_bound,
        "root_subspace_distance_upper_bound": root_subspace_distance,
        "cumulative_tableau_propagation_error_upper_bound": (
            cumulative_tableau_error
        ),
        "separator_block_operator_error_upper_bound": block_operator_error,
        "observed_minimum_raw_gap": record.minimum_numerical_raw_gap,
        "conditional_weyl_gap_lower_bound": conditional_gap_lower,
        "collision_operator_perturbation_radius": (
            collision_perturbation_radius
        ),
        "declared_budget_margin_ratio": (
            collision_perturbation_radius / block_operator_error
        ),
        "separation_survives_declared_error_budget": (
            conditional_gap_lower > 0
        ),
        "floating_point_error_budget_machine_verified": False,
        "interval_arithmetic_verified": False,
        "exact_algebraic_certificate": False,
        "status": (
            "robust-under-declared-error-budget-not-proof"
            if conditional_gap_lower > 0
            else "declared-error-budget-can-close-gap"
        ),
    }


def build_invariant_contraction_report() -> InvariantContractionReport:
    records = _validated_stored_records(_load_certificate())
    control, next_target = records
    next_simple = next_target.minimum_numerical_raw_gap > 1e-7
    robustness = _declared_error_budget_audit(next_target)
    metrics: dict[str, int | float] = {
        "n": 10,
        "numerically_contracted_primary_target_count": len(records),
        "conjugate_target_coverage_count": 2 * len(records),
        "maximum_numerical_kronecker_multiplicity": max(
            record.kronecker_multiplicity for record in records
        ),
        "maximum_invariant_vector_dimension": max(
            record.direct_invariant_vector_dimension for record in records
        ),
        "yjm_fiber_vector_dimension": max(
            record.fiber_vector_dimension for record in records
        ),
        "maximum_vector_dimension_reduction_factor": max(
            record.vector_dimension_reduction_factor for record in records
        ),
        "maximum_estimated_arpack_basis_bytes": max(
            record.estimated_arpack_basis_bytes for record in records
        ),
        "maximum_single_tableau_fiber_bytes": max(
            record.kronecker_multiplicity
            * record.fiber_vector_dimension
            * 8
            for record in records
        ),
        "all_tableau_fibers_materialized_count": 0,
        "direct_coxeter_multiplicity6_timeout_seconds": 4100,
        "direct_coxeter_multiplicity6_converged_count": 0,
        "next_multiplicity15_estimated_arpack_basis_bytes": 160_432_128,
        "next_multiplicity15_single_tableau_fiber_bytes": 70_778_880,
        "maximum_exact_control_trace_residual": (
            control.maximum_exact_control_trace_residual
        ),
        "maximum_invariant_residual": max(
            record.maximum_penalty_residual for record in records
        ),
        "n10_multiplicity6_minimum_numerical_raw_gap": (
            next_target.minimum_numerical_raw_gap
        ),
        "n10_multiplicity6_numerically_simple_spectrum_count": int(next_simple),
        "n10_multiplicity6_declared_budget_gap_lower_bound": float(
            robustness["conditional_weyl_gap_lower_bound"]
        ),
        "n10_multiplicity6_declared_budget_margin_ratio": float(
            robustness["declared_budget_margin_ratio"]
        ),
        "n10_multiplicity6_robust_under_declared_budget_count": int(
            robustness["separation_survives_declared_error_budget"]
        ),
        "machine_verified_roundoff_certificate_count": 0,
        "interval_verified_multiplicity6_certificate_count": 0,
        "explicit_s10_character_table_bytes_avoided": 91_663_488_000,
        "factorial_group_row_storage_removed_count": 1,
        "exact_multiplicity6_certificate_count": 0,
        "polynomial_invariant_contraction_theorem_count": 0,
        "all_n_simple_spectrum_theorem_count": 0,
        "coherent_typical_multiplicity_transform_count": 0,
        "typical_label_hidden_involution_decoder_count": 0,
    }
    return InvariantContractionReport(
        created_at=utc_now(),
        contraction_contract={
            "identity": (
                "On diagonal-S_n invariant tensors, a simultaneous-conjugacy "
                "orbit average has the same matrix elements as one representative."
            ),
            "fiber_factorization": (
                "A diagonal Jucys-Murphy content penalty isolates one target "
                "tableau fiber of dimension g(lambda,lambda,nu) inside "
                "V_lambda tensor V_lambda. Diagonal adjacent transpositions "
                "propagate that fiber through a depth-first tableau spanning "
                "tree; fibers are contracted and released rather than all stored."
            ),
            "operator": "H_10=average(TT1)+average(TC1)",
            "control": (
                "The multiplicity-three (9,1) block reproduces all exact "
                "class-Fourier power traces."
            ),
            "new_probe": (
                "The previously inaccessible multiplicity-six (5,5) block is "
                "contracted without group-row or orbit-term materialization."
            ),
            "remaining_cost": (
                "The YJM eigensolve uses dim(lambda)^2 amplitudes independent "
                "of dim(nu), reducing the n=10 multiplicity-six vector dimension "
                "42-fold. dim(lambda)^2 is still exponential for typical lambda, "
                "so this finite numerical method is not a polynomial transform."
            ),
        },
        records=records,
        robustness_audit=robustness,
        headline_metrics=metrics,
        claim_gate={
            "exact_control_reproduced": True,
            "explicit_s10_character_rows_required": False,
            "multiplicity6_numerically_simple": next_simple,
            "multiplicity6_robust_under_declared_error_budget": bool(
                robustness["separation_survives_declared_error_budget"]
            ),
            "declared_error_budget_is_machine_verified": False,
            "interval_arithmetic_verified": False,
            "multiplicity6_exactly_certified": False,
            "polynomial_scaling_proved": False,
            "all_n_simple_spectrum_proved": False,
            "coherent_transform_proved": False,
            "hidden_involution_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "YJM-fiber contraction removes factorial row storage and the "
                "target-dimension factor, but the solve is numerical and still "
                "uses exponentially large V_lambda tensor V_lambda; no exact "
                "n=10, all-n, transform, or decoder theorem follows."
            ),
        },
        status=(
            "factorial-row-barrier-removed-multiplicity6-numerically-simple-exact-proof-open"
            if next_simple
            else "factorial-row-barrier-removed-multiplicity6-collision-detected"
        ),
        summary=(
            "Sparse YJM-fiber contraction reproduces the exact n=10 cubic "
            "without S_10 rows and reaches the multiplicity-six block with a "
            "42-fold eigensolve-dimension reduction; the new spectrum remains "
            "numerical and the representation solve is not scalable."
        ),
        falsifiers_triggered=[
            "The 91.7 GB explicit S_10 character table is not necessary for finite block contraction.",
            "The YJM fiber solve still acts on the exponentially large tensor square of a typical irrep.",
            "A numerical minimum gap is not an exact square-free certificate.",
            "Four covered conjugate blocks out of 40 are not an n=10 theorem.",
            "No coherent transform, hidden-involution outcome law, decoder, or classical separation is supplied.",
        ],
    )


def write_invariant_contraction_report(
    output_path: Path = REPORT_PATH,
    *,
    recompute: bool = False,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    if recompute:
        write_numerical_certificate()
    payload = asdict(build_invariant_contraction_report())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-TYPICAL-EXPLICIT-S10-ROWS-ARE-NOT-A-FINITE-BLOCK-REQUIREMENT",
                source=str(output_path),
                claim=(
                    "Exact translated S_10 character-row storage is intrinsically "
                    "required to contract finite typical multiplicity blocks."
                ),
                reason_invalid=(
                    "Diagonal-S_10 invariance reduces each orbit average to one "
                    "representative on the Kronecker invariant space; the exact "
                    "multiplicity-three traces are reproduced without group rows."
                ),
                lesson=(
                    "Use invariant-space contraction as a finite collision finder, "
                    "then attack its exponential dim(nu)*dim(lambda)^2 nullspace "
                    "with branching or centralizer recurrences."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence=payload["headline_metrics"],
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-TYPICAL-DIRECT-COXETER-MULTIPLICITY6-SCALING",
                source=str(output_path),
                claim=(
                    "A direct Coxeter nullspace in nu tensor lambda tensor lambda "
                    "is the right finite architecture for the n=10 multiplicity ladder."
                ),
                reason_invalid=(
                    "The (5,5) multiplicity-six solve uses 24,772,608 amplitudes, "
                    "held about 4.3 GB resident, and did not converge after more "
                    "than 4,100 seconds."
                ),
                lesson=(
                    "Isolate one YJM tableau fiber in lambda tensor lambda and "
                    "propagate it through target tableaux, removing the dim(nu) "
                    "factor before searching higher blocks."
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
                artifacts={"coset_typical_invariant_contraction": str(output_path)},
            )
        )
    return payload


if __name__ == "__main__":
    print(
        json.dumps(
            write_invariant_contraction_report()["headline_metrics"],
            indent=2,
            sort_keys=True,
        )
    )
