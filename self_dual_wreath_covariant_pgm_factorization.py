"""Covariance-compressed Fourier factorization of the mixed-state PGM.

Let ``rho_g=U_g rho U_g^*`` be a uniform covariant ensemble and decompose

    U = direct_sum_nu rho_nu tensor I_(M_nu),
    B = E_g rho_g
      = direct_sum_nu I_(d_nu)/d_nu tensor C_nu.

The PGM seed factor is

    T = |G|^-1/2 rho^1/2 B^-1/2,

and a Naimark isometry is

    W|psi> = sum_g |g> tensor T U_g^* |psi>.

Apply the nonabelian Fourier transform to the group-label register.  Schur
orthogonality cancels both the ``|G|^-1/2`` factor and the ``sqrt(d_nu)`` in
``B^-1/2``.  The exact result is

    (F_G^* tensor I) W |nu,a,m>
      = sum_j |nu,a,j> tensor
        rho^1/2 (I tensor C_nu^-1/2)|nu,j,m>.          (1)

The right side is an isometry on ``supp(B)`` because summing over ``j`` takes
the row partial trace and yields ``C_nu^-1/2 C_nu C_nu^-1/2``.

For a normalized projector state ``rho=P/r``, write

    D_nu = Tr_(V_nu)(Pi_nu P Pi_nu).

Then all projector-rank normalization cancels as well:

    rho^1/2(I tensor C_nu^-1/2)
      = P(I tensor D_nu^-1/2).                         (2)

Equations (1)--(2) are an exact covariance-compressed Stinespring
factorization.  They evade the explicit ``sqrt(|G|)`` environment charge of a
generic Petz implementation.  They do not provide a polynomial circuit for
the controlled multiplicity inverse ``D_nu^-1/2``; that is now the isolated
algorithmic bottleneck.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_coherent_fourier_decoder import symmetric_group_fourier_matrix
from self_dual_wreath_orientation_fourier_reduction import (
    _source_representation_rows,
)


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_covariant_pgm_factorization.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-COVARIANT-PGM-FACTORIZATION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Permutation = tuple[int, ...]


@dataclass(frozen=True)
class CovariantFactorizationControl:
    control_id: str
    n: int
    group_order: int
    representation_dimension: int
    state_rank: int
    average_state_support_rank: int
    maximum_average_block_formula_residual: float
    fourier_factorization_residual: float
    compressed_isometry_support_residual: float
    projector_rank_cancellation_residual: float | None
    exact_covariant_factorization_verified: bool
    status: str


@dataclass(frozen=True)
class CovariantFactorizationScalingRecord:
    n: int
    group_order_decimal: str
    log2_group_order: float
    generic_petz_environment_sqrt_log2_charge: float
    explicit_group_size_factor_after_covariant_fourier_reduction: float
    efficient_symmetric_group_qft_available: bool
    controlled_multiplicity_inverse_block_encoding_proved: bool
    polynomial_covariant_pgm_circuit_proved: bool
    status: str


@dataclass(frozen=True)
class CovariantPgmFactorizationReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[CovariantFactorizationControl]
    scaling_records: list[CovariantFactorizationScalingRecord]
    proof_obligations: list[dict[str, bool | str]]
    adversarial_audit: list[dict[str, bool | str]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _psd_power(
    matrix: np.ndarray,
    power: float,
    tolerance: float,
) -> tuple[np.ndarray, np.ndarray, int]:
    hermitian = (matrix + matrix.conj().T) / 2
    eigenvalues, eigenvectors = np.linalg.eigh(hermitian)
    if eigenvalues[0] < -100 * tolerance:
        raise ValueError("matrix must be positive semidefinite")
    positive = eigenvalues > tolerance
    transformed = np.zeros_like(eigenvalues)
    transformed[positive] = eigenvalues[positive] ** power
    output = (eigenvectors * transformed) @ eigenvectors.conj().T
    support = eigenvectors[:, positive] @ eigenvectors[:, positive].conj().T
    return output, support, int(np.count_nonzero(positive))


def _direct_sum_representation(
    n: int,
    multiplicities: dict[Partition, int],
) -> tuple[tuple[Permutation, np.ndarray], ...]:
    tables = {
        partition: _source_representation_rows(partition)
        for partition, multiplicity in multiplicities.items()
        if multiplicity
    }
    permutations = tuple(next(iter(tables.values())))
    rows = []
    for permutation in permutations:
        blocks = [
            np.kron(tables[partition][permutation], np.eye(multiplicity))
            for partition, multiplicity in multiplicities.items()
            if multiplicity
        ]
        dimension = sum(len(block) for block in blocks)
        matrix = np.zeros((dimension, dimension))
        offset = 0
        for block in blocks:
            width = len(block)
            matrix[offset : offset + width, offset : offset + width] = block
            offset += width
        rows.append((permutation, matrix))
    return tuple(rows)


def _sector_layout(
    multiplicities: dict[Partition, int],
) -> dict[Partition, tuple[int, int, int]]:
    layout = {}
    offset = 0
    for partition, multiplicity in multiplicities.items():
        if multiplicity < 1:
            continue
        dimension = hook_length_dimension(partition)
        layout[partition] = (offset, dimension, multiplicity)
        offset += dimension * multiplicity
    return layout


def _partial_trace_row(block: np.ndarray, dimension: int, multiplicity: int) -> np.ndarray:
    output = np.zeros((multiplicity, multiplicity), dtype=complex)
    for row in range(dimension):
        section = slice(row * multiplicity, (row + 1) * multiplicity)
        output += block[section, section]
    return output


def _fourier_column_offsets(n: int) -> dict[Partition, int]:
    output = {}
    offset = 0
    for partition in integer_partitions(n):
        output[partition] = offset
        dimension = hook_length_dimension(partition)
        offset += dimension * dimension
    return output


def audit_covariant_factorization(
    control_id: str,
    n: int,
    multiplicities: dict[Partition, int],
    state: np.ndarray,
    *,
    projector: np.ndarray | None = None,
    tolerance: float = 1e-9,
) -> CovariantFactorizationControl:
    group_rows = _direct_sum_representation(n, multiplicities)
    group_order = math.factorial(n)
    dimension = len(group_rows[0][1])
    if state.shape != (dimension, dimension):
        raise ValueError("state has wrong representation dimension")
    if abs(float(np.trace(state).real) - 1) > 100 * tolerance:
        raise ValueError("state must have trace one")

    state_sqrt, _, state_rank = _psd_power(state, 0.5, tolerance)
    average = sum(
        matrix @ state @ matrix.conj().T
        for _, matrix in group_rows
    ) / group_order
    average_inverse, average_support, average_rank = _psd_power(
        average,
        -0.5,
        tolerance,
    )
    layout = _sector_layout(multiplicities)
    sector_data: dict[Partition, tuple[np.ndarray, np.ndarray, np.ndarray]] = {}
    expected_average = np.zeros_like(state, dtype=complex)
    maximum_block_residual = 0.0
    for partition, (offset, irrep_dimension, multiplicity) in layout.items():
        width = irrep_dimension * multiplicity
        block = state[offset : offset + width, offset : offset + width]
        carrier = _partial_trace_row(block, irrep_dimension, multiplicity)
        carrier_inverse, carrier_support, _ = _psd_power(
            carrier,
            -0.5,
            tolerance,
        )
        expected_block = np.kron(
            np.eye(irrep_dimension) / irrep_dimension,
            carrier,
        )
        observed_block = average[offset : offset + width, offset : offset + width]
        maximum_block_residual = max(
            maximum_block_residual,
            float(np.linalg.norm(observed_block - expected_block, ord=2)),
        )
        expected_average[offset : offset + width, offset : offset + width] = expected_block
        sector_data[partition] = (carrier, carrier_inverse, carrier_support)
    maximum_block_residual = max(
        maximum_block_residual,
        float(np.linalg.norm(average - expected_average, ord=2)),
    )

    seed_factor = state_sqrt @ average_inverse / math.sqrt(group_order)
    group_isometry = np.vstack(
        [seed_factor @ matrix.conj().T for _, matrix in group_rows]
    )
    fourier, _, _ = symmetric_group_fourier_matrix(n)
    transformed = np.kron(fourier.T, np.eye(dimension)) @ group_isometry

    compressed = np.zeros_like(transformed, dtype=complex)
    fourier_offsets = _fourier_column_offsets(n)
    for partition, (input_offset, irrep_dimension, multiplicity) in layout.items():
        _, carrier_inverse, _ = sector_data[partition]
        fourier_offset = fourier_offsets[partition]
        for row_index in range(irrep_dimension):
            for multiplicity_index in range(multiplicity):
                input_column = (
                    input_offset + row_index * multiplicity + multiplicity_index
                )
                for dual_row in range(irrep_dimension):
                    basis = np.zeros(dimension, dtype=complex)
                    carrier_column = carrier_inverse[:, multiplicity_index]
                    start = input_offset + dual_row * multiplicity
                    basis[start : start + multiplicity] = carrier_column
                    junk = state_sqrt @ basis
                    fourier_column = (
                        fourier_offset
                        + row_index * irrep_dimension
                        + dual_row
                    )
                    output_slice = slice(
                        fourier_column * dimension,
                        (fourier_column + 1) * dimension,
                    )
                    compressed[output_slice, input_column] = junk

    factorization_residual = float(np.linalg.norm(transformed - compressed, ord=2))
    isometry_residual = float(
        np.linalg.norm(
            compressed.conj().T @ compressed - average_support,
            ord=2,
        )
    )

    projector_residual: float | None = None
    if projector is not None:
        rank = int(round(float(np.trace(projector).real)))
        if np.linalg.norm(state - projector / rank, ord=2) > 100 * tolerance:
            raise ValueError("projector does not normalize to the supplied state")
        simplified = np.zeros_like(compressed, dtype=complex)
        for partition, (input_offset, irrep_dimension, multiplicity) in layout.items():
            width = irrep_dimension * multiplicity
            projector_block = projector[
                input_offset : input_offset + width,
                input_offset : input_offset + width,
            ]
            carrier = _partial_trace_row(
                projector_block,
                irrep_dimension,
                multiplicity,
            )
            carrier_inverse, _, _ = _psd_power(carrier, -0.5, tolerance)
            fourier_offset = fourier_offsets[partition]
            for row_index in range(irrep_dimension):
                for multiplicity_index in range(multiplicity):
                    input_column = input_offset + row_index * multiplicity + multiplicity_index
                    for dual_row in range(irrep_dimension):
                        basis = np.zeros(dimension, dtype=complex)
                        start = input_offset + dual_row * multiplicity
                        basis[start : start + multiplicity] = carrier_inverse[:, multiplicity_index]
                        junk = projector @ basis
                        fourier_column = fourier_offset + row_index * irrep_dimension + dual_row
                        output_slice = slice(
                            fourier_column * dimension,
                            (fourier_column + 1) * dimension,
                        )
                        simplified[output_slice, input_column] = junk
        projector_residual = float(np.linalg.norm(compressed - simplified, ord=2))

    verified = (
        maximum_block_residual <= 100 * tolerance
        and factorization_residual <= 100 * tolerance
        and isometry_residual <= 100 * tolerance
        and (projector_residual is None or projector_residual <= 100 * tolerance)
    )
    return CovariantFactorizationControl(
        control_id=control_id,
        n=n,
        group_order=group_order,
        representation_dimension=dimension,
        state_rank=state_rank,
        average_state_support_rank=average_rank,
        maximum_average_block_formula_residual=maximum_block_residual,
        fourier_factorization_residual=factorization_residual,
        compressed_isometry_support_residual=isometry_residual,
        projector_rank_cancellation_residual=projector_residual,
        exact_covariant_factorization_verified=verified,
        status=(
            "exact-covariance-compressed-pgm-factorization"
            if verified
            else "covariant-pgm-factorization-validation-failure"
        ),
    )


def _deterministic_controls() -> list[CovariantFactorizationControl]:
    partitions = integer_partitions(3)
    multiplicities = {
        partition: hook_length_dimension(partition)
        for partition in partitions
    }
    dimension = math.factorial(3)
    raw = np.arange(1, dimension * dimension + 1, dtype=float).reshape(
        dimension,
        dimension,
    )
    positive = raw @ raw.T + np.eye(dimension)
    full_state = positive / np.trace(positive)

    vector = np.arange(1, dimension + 1, dtype=float)
    vector /= np.linalg.norm(vector)
    pure_state = np.outer(vector, vector)

    projector = np.zeros((dimension, dimension))
    projector[0, 0] = 1
    projector[1, 1] = 1
    projector_state = projector / 2
    return [
        audit_covariant_factorization(
            "S3-REGULAR-FULL-RANK",
            3,
            multiplicities,
            full_state,
        ),
        audit_covariant_factorization(
            "S3-REGULAR-PURE-RANK-DEFICIENT",
            3,
            multiplicities,
            pure_state,
        ),
        audit_covariant_factorization(
            "S3-REGULAR-PROJECTOR-CANCELLATION",
            3,
            multiplicities,
            projector_state,
            projector=projector,
        ),
    ]


def covariant_factorization_scaling_record(
    n: int,
) -> CovariantFactorizationScalingRecord:
    if n < 2:
        raise ValueError("n must be at least two")
    order = math.factorial(n)
    log_order = math.lgamma(n + 1) / math.log(2)
    return CovariantFactorizationScalingRecord(
        n=n,
        group_order_decimal=str(order),
        log2_group_order=log_order,
        generic_petz_environment_sqrt_log2_charge=log_order / 2,
        explicit_group_size_factor_after_covariant_fourier_reduction=1.0,
        efficient_symmetric_group_qft_available=True,
        controlled_multiplicity_inverse_block_encoding_proved=False,
        polynomial_covariant_pgm_circuit_proved=False,
        status="group-normalization-cancelled-multiplicity-inverse-circuit-open",
    )


def run_covariant_pgm_factorization() -> CovariantPgmFactorizationReport:
    controls = _deterministic_controls()
    scaling = [
        covariant_factorization_scaling_record(n)
        for n in (3, 4, 5, 8, 12, 16, 24, 32, 64, 128, 256, 512)
    ]
    failures = sum(not row.exact_covariant_factorization_verified for row in controls)
    verified = failures == 0
    return CovariantPgmFactorizationReport(
        created_at=utc_now(),
        theorem_contract={
            "pgm_naimark_isometry": (
                "W=sum_g |g> tensor |G|^-1/2 rho^1/2 B^-1/2 U_g^*."
            ),
            "covariant_fourier_factorization": (
                "(F_G^* tensor I)W|nu,a,m>=sum_j |nu,a,j> tensor "
                "rho^1/2(I tensor C_nu^-1/2)|nu,j,m>."
            ),
            "support_isometry": (
                "The compressed map squares to direct_sum_nu I_V tensor "
                "Pi_supp(C_nu)."
            ),
            "projector_cancellation": (
                "For rho=P/r and D_nu=Tr_V(Pi_nu P Pi_nu), the carrier map is "
                "P(I tensor D_nu^-1/2), with r and |G| absent."
            ),
            "implementation_boundary": (
                "Beals supplies F_(S_n); the unresolved operation is a coherent "
                "source-adapted implementation of every D_nu^-1/2."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "covariance_compressed_stinespring_factorization",
                "resolved": verified,
                "resolution": (
                    "Schur orthogonality evaluates the Fourier transform of the "
                    "covariant PGM Naimark isometry exactly."
                ),
            },
            {
                "obligation": "group_and_projector_rank_normalization_cancellation",
                "resolved": verified,
                "resolution": (
                    "The Fourier coefficient, B-sector inverse, and normalized "
                    "projector square root cancel all explicit |G|, d_nu, and r factors."
                ),
            },
            {
                "obligation": "efficient_symmetric_group_fourier_transform",
                "resolved": True,
                "resolution": "Beals gives a polynomial S_n quantum Fourier transform.",
            },
            {
                "obligation": "controlled_multiplicity_inverse_implementation",
                "resolved": False,
                "resolution": (
                    "No block encoding or direct transform for D_nu^-1/2 with "
                    "polynomial normalization and precision is known."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "The generic sqrt(|G|) Petz charge is unavoidable.",
                "resolved": True,
                "resolution": (
                    "It cancels algebraically after the covariant Fourier transform; "
                    "the generic Petz lower bound does not specialize to this symmetry."
                ),
            },
            {
                "objection": "Cancellation proves a polynomial PGM circuit.",
                "resolved": False,
                "resolution": (
                    "No. D_nu may remain ill-conditioned or lack an efficient coherent "
                    "block encoding; the identity isolates rather than solves that task."
                ),
            },
            {
                "objection": "A pure dual-row state is the required output.",
                "resolved": True,
                "resolution": (
                    "The output retains a physical junk vector for every dual row, "
                    "realizing the mixed multiplicity tight frame."
                ),
            },
            {
                "objection": "The finite S3 controls prove typical large-n conditioning.",
                "resolved": False,
                "resolution": (
                    "They validate exact algebra only; no asymptotic D_nu spectrum or "
                    "source-adapted circuit follows."
                ),
            },
        ],
        headline_metrics={
            "covariance_compressed_pgm_factorization_theorem_count": 1,
            "group_size_normalization_cancellation_theorem_count": 1,
            "projector_rank_normalization_cancellation_theorem_count": 1,
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "scaling_record_count": len(scaling),
            "maximum_removed_generic_sqrt_group_log2_charge": (
                scaling[-1].generic_petz_environment_sqrt_log2_charge
            ),
            "controlled_multiplicity_inverse_block_encoding_count": 0,
            "polynomial_covariant_pgm_circuit_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "covariance_compressed_stinespring_factorization_proved": verified,
            "explicit_sqrt_group_environment_charge_survives": False,
            "projector_rank_normalization_charge_survives": False,
            "efficient_symmetric_group_qft_available": True,
            "controlled_multiplicity_inverse_block_encoding_proved": False,
            "polynomial_covariant_pgm_circuit_proved": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Covariance removes the generic label-environment and projector-rank "
                "normalizations exactly. Efficient controlled inversion of the physical "
                "multiplicity operators D_nu is the remaining circuit bottleneck."
            ),
        },
        status=(
            "covariant-pgm-factorized-multiplicity-inverse-circuit-open"
            if verified
            else "covariant-pgm-factorization-validation-failure"
        ),
        summary=(
            "Derived and validated the exact Fourier-domain PGM Stinespring "
            "factorization, cancelling explicit factorial environment normalization."
        ),
        falsifiers_triggered=[
            (
                "The sqrt(n!) dimension charge in the generic Petz implementation is "
                "not intrinsic to the group-covariant PGM."
            ),
            (
                "The physical mixed decoder is a dual-row-indexed tight-frame isometry, "
                "not a single pure Fourier state."
            ),
            (
                "After exact covariance compression, multiplicity inversion is the sole "
                "nontrivial state-dependent linear-algebra operation."
            ),
        ],
    )


def write_covariant_pgm_factorization_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_covariant_pgm_factorization())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_covariant_pgm_factorization_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
