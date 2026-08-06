"""Physical transfer gate for an orientation-Gram polar sampler.

Let ``T:D->H_phys`` be the physical synthesis factor of a covariant projector
ensemble and let ``R:D->H_orient`` be any orientation-side factor with the same
Gram operator

    F = T^*T = R^*R.

Their polar isometries are

    Q_T = T F^(-1/2),       Q_R = R F^(-1/2).

Equality of Grams implies the exact partial isometry

    W = Q_T Q_R^*,          W Q_R = Q_T.               (1)

Thus an efficient orientation polar sampler yields the physical PGM carrier
map only if the output intertwiner ``W`` is also efficiently implementable.
The Gram spectrum, projector-sum formula, and hierarchical normalization do
not determine a circuit for ``W``.  Indeed an arbitrary output isometry can be
composed with one factor without changing its Gram.

For the wreath route, equal Gram data initially leaves this gate open.  The
companion physical-PGM intertwiner theorem now uses additional covariant
structure to close it: generalized coherent ``S_n`` Fourier sampling maps the
physical carrier onto the stacked orientation invariant ranges.  That map is
independent of ``Q_T`` and preserves ``nu`` coherently.  The remaining open
operation is the all-n orientation polar sampler itself.

This module is a claim gate, not a no-go theorem.  Its generic warning remains:
Gram equality alone never compiles ``W``.  In this structured wreath instance,
the required representation-theoretic Stinespring transform has now been
identified explicitly.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_polar_factor_transfer.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-POLAR-FACTOR-TRANSFER"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class EqualGramTransferControl:
    control_id: str
    domain_dimension: int
    orientation_output_dimension: int
    physical_output_dimension: int
    gram_support_rank: int
    gram_residual: float
    orientation_polar_support_residual: float
    physical_polar_support_residual: float
    transfer_initial_projection_residual: float
    transfer_final_projection_residual: float
    polar_transfer_residual: float
    output_intertwiner_given_independently: bool
    exact_equal_gram_transfer_verified: bool
    status: str


@dataclass(frozen=True)
class PolarTransferScalingRecord:
    n: int
    hidden_label_count_log2: float
    information_threshold_copy_count: int
    orientation_gram_factorization_available: bool
    hierarchical_orientation_polar_proved: bool
    physical_pgm_polar_target_specified: bool
    full_output_intertwiner_compiled: bool
    selected_trace_transfer_is_full_polar_transfer: bool
    polynomial_physical_pgm_circuit_proved: bool
    status: str


@dataclass(frozen=True)
class PolarFactorTransferReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[EqualGramTransferControl]
    scaling_records: list[PolarTransferScalingRecord]
    proof_obligations: list[dict[str, bool | str]]
    adversarial_audit: list[dict[str, bool | str]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _inverse_square_root(
    matrix: np.ndarray,
    tolerance: float,
) -> tuple[np.ndarray, np.ndarray, int]:
    eigenvalues, eigenvectors = np.linalg.eigh(
        (matrix + matrix.conj().T) / 2
    )
    if eigenvalues[0] < -100 * tolerance:
        raise ValueError("Gram matrix must be positive semidefinite")
    positive = eigenvalues > tolerance
    values = np.zeros_like(eigenvalues)
    values[positive] = eigenvalues[positive] ** -0.5
    inverse = (eigenvectors * values) @ eigenvectors.conj().T
    support = eigenvectors[:, positive] @ eigenvectors[:, positive].conj().T
    return inverse, support, int(np.count_nonzero(positive))


def audit_equal_gram_transfer(
    control_id: str,
    orientation_factor: np.ndarray,
    physical_factor: np.ndarray,
    *,
    output_intertwiner_given_independently: bool,
    tolerance: float = 1e-10,
) -> EqualGramTransferControl:
    if orientation_factor.shape[1] != physical_factor.shape[1]:
        raise ValueError("factors must share a domain")
    orientation_gram = orientation_factor.conj().T @ orientation_factor
    physical_gram = physical_factor.conj().T @ physical_factor
    gram_residual = float(
        np.linalg.norm(orientation_gram - physical_gram, ord=2)
    )
    inverse, support, support_rank = _inverse_square_root(
        (orientation_gram + physical_gram) / 2,
        tolerance,
    )
    orientation_polar = orientation_factor @ inverse
    physical_polar = physical_factor @ inverse
    transfer = physical_polar @ orientation_polar.conj().T
    orientation_range = orientation_polar @ orientation_polar.conj().T
    physical_range = physical_polar @ physical_polar.conj().T
    orientation_support_residual = float(
        np.linalg.norm(
            orientation_polar.conj().T @ orientation_polar - support,
            ord=2,
        )
    )
    physical_support_residual = float(
        np.linalg.norm(
            physical_polar.conj().T @ physical_polar - support,
            ord=2,
        )
    )
    initial_residual = float(
        np.linalg.norm(transfer.conj().T @ transfer - orientation_range, ord=2)
    )
    final_residual = float(
        np.linalg.norm(transfer @ transfer.conj().T - physical_range, ord=2)
    )
    transfer_residual = float(
        np.linalg.norm(transfer @ orientation_polar - physical_polar, ord=2)
    )
    verified = bool(
        gram_residual <= 100 * tolerance
        and orientation_support_residual <= 100 * tolerance
        and physical_support_residual <= 100 * tolerance
        and initial_residual <= 100 * tolerance
        and final_residual <= 100 * tolerance
        and transfer_residual <= 100 * tolerance
    )
    return EqualGramTransferControl(
        control_id=control_id,
        domain_dimension=orientation_factor.shape[1],
        orientation_output_dimension=orientation_factor.shape[0],
        physical_output_dimension=physical_factor.shape[0],
        gram_support_rank=support_rank,
        gram_residual=gram_residual,
        orientation_polar_support_residual=orientation_support_residual,
        physical_polar_support_residual=physical_support_residual,
        transfer_initial_projection_residual=initial_residual,
        transfer_final_projection_residual=final_residual,
        polar_transfer_residual=transfer_residual,
        output_intertwiner_given_independently=output_intertwiner_given_independently,
        exact_equal_gram_transfer_verified=verified,
        status=(
            "exact-equal-gram-polar-transfer-with-known-intertwiner"
            if verified and output_intertwiner_given_independently
            else "exact-equal-gram-transfer-exists-intertwiner-not-compiled"
            if verified
            else "equal-gram-transfer-validation-failure"
        ),
    )


def _isometry(rows: int, columns: int, seed: int) -> np.ndarray:
    if rows < columns:
        raise ValueError("an isometry needs at least as many rows as columns")
    rng = np.random.default_rng(seed)
    basis, _ = np.linalg.qr(
        rng.normal(size=(rows, columns))
        + 1j * rng.normal(size=(rows, columns))
    )
    return basis


def _finite_controls() -> list[EqualGramTransferControl]:
    rng = np.random.default_rng(99173)
    full = rng.normal(size=(5, 3)) + 1j * rng.normal(size=(5, 3))
    known_output = _isometry(8, 5, 431)
    rank_deficient = np.asarray(
        [
            [1.0, 0.0, 1.0, 0.0],
            [0.0, 1.0, 1.0, 0.0],
            [1.0, -1.0, 0.0, 0.0],
        ],
        dtype=complex,
    )
    hidden_output = _isometry(7, 3, 877)
    adversarial = rng.normal(size=(4, 3)) + 1j * rng.normal(size=(4, 3))
    arbitrary_output = _isometry(9, 4, 1201)
    return [
        audit_equal_gram_transfer(
            "known-output-isometry",
            full,
            known_output @ full,
            output_intertwiner_given_independently=True,
        ),
        audit_equal_gram_transfer(
            "rank-deficient-hidden-output",
            rank_deficient,
            hidden_output @ rank_deficient,
            output_intertwiner_given_independently=False,
        ),
        audit_equal_gram_transfer(
            "arbitrary-dense-output-geometry",
            adversarial,
            arbitrary_output @ adversarial,
            output_intertwiner_given_independently=False,
        ),
    ]


def polar_transfer_scaling_record(n: int) -> PolarTransferScalingRecord:
    if n < 3:
        raise ValueError("n must be at least three")
    copies = math.ceil(math.lgamma(n + 1) / math.log(2))
    return PolarTransferScalingRecord(
        n=n,
        hidden_label_count_log2=math.lgamma(n + 1) / math.log(2),
        information_threshold_copy_count=copies,
        orientation_gram_factorization_available=True,
        hierarchical_orientation_polar_proved=False,
        physical_pgm_polar_target_specified=True,
        full_output_intertwiner_compiled=True,
        selected_trace_transfer_is_full_polar_transfer=False,
        polynomial_physical_pgm_circuit_proved=False,
        status="structured-wreath-transfer-compiled-orientation-polar-open",
    )


def run_polar_factor_transfer() -> PolarFactorTransferReport:
    controls = _finite_controls()
    scaling = [
        polar_transfer_scaling_record(n)
        for n in (3, 4, 5, 8, 16, 32, 64, 128, 256, 512)
    ]
    failures = sum(not row.exact_equal_gram_transfer_verified for row in controls)
    independently_known = sum(row.output_intertwiner_given_independently for row in controls)
    verified = failures == 0
    return PolarFactorTransferReport(
        created_at=utc_now(),
        theorem_contract={
            "equal_gram_factors": "T^*T=R^*R=F.",
            "polar_isometries": "Q_T=TF^-1/2 and Q_R=RF^-1/2.",
            "canonical_transfer": (
                "W=Q_TQ_R^* is a partial isometry from ran(Q_R) to ran(Q_T) "
                "and WQ_R=Q_T."
            ),
            "algorithmic_requirement": (
                "An orientation-side polar sampler implements the physical PGM "
                "only together with an independently compiled W."
            ),
            "nonimplication": (
                "Gram equality or spectral equality does not expose W; arbitrary "
                "output isometries preserve the same Gram."
            ),
            "wreath_scope": (
                "The companion physical-PGM intertwiner theorem uses coherent "
                "generalized S_n Fourier sampling to compile the full transfer "
                "across nu; this conclusion uses more than Gram equality."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "equal_gram_partial_isometry_theorem",
                "resolved": verified,
                "resolution": (
                    "Both polar factors have the same initial support, so their "
                    "product gives the exact range-to-range partial isometry."
                ),
            },
            {
                "obligation": "orientation_hierarchical_polar_sampler",
                "resolved": False,
                "resolution": (
                    "The companion hierarchy reduces it to higher-level relative "
                    "effects; no all-n implementation is proved."
                ),
            },
            {
                "obligation": "physical_output_intertwiner",
                "resolved": True,
                "resolution": (
                    "Generalized coherent S_n Fourier row-copy maps the physical "
                    "carrier onto the stacked orientation invariant ranges without "
                    "constructing a Kronecker multiplicity basis."
                ),
            },
            {
                "obligation": "coherent_cross_sector_control",
                "resolved": True,
                "resolution": (
                    "The row-copy transform retains nu and both Fourier matrix "
                    "indices coherently through the orientation polar control."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Equal nonzero spectra make the two polar circuits interchangeable.",
                "resolved": True,
                "resolution": (
                    "No. They can have arbitrary output geometry related by an "
                    "unknown dense isometry while retaining identical Gram data."
                ),
            },
            {
                "objection": "The selected physical trace-transfer identity already supplies W.",
                "resolved": True,
                "resolution": (
                    "The trace identity alone does not, but the separate row-copy "
                    "factorization proves the full range-preserving Stinespring "
                    "identity on every carrier vector."
                ),
            },
            {
                "objection": "Defining W=Q_TQ_R^* is a constructive circuit.",
                "resolved": True,
                "resolution": (
                    "It is circular: Q_T is the physical PGM operation being sought."
                ),
            },
            {
                "objection": "The transfer theorem rules out a physical intertwiner.",
                "resolved": False,
                "resolution": (
                    "It does not. It isolates the exact object; a Young/recoupling "
                    "Stinespring transform may implement it directly."
                ),
            },
        ],
        headline_metrics={
            "equal_gram_polar_transfer_theorem_count": 1,
            "finite_control_count": len(controls),
            "finite_validation_failure_count": failures,
            "finite_independently_known_intertwiner_count": independently_known,
            "orientation_hierarchical_polar_sampler_count": 0,
            "physical_output_intertwiner_count": 1,
            "coherent_cross_sector_transfer_count": 1,
            "polynomial_physical_pgm_circuit_count": 0,
            "tail_n": scaling[-1].n,
            "tail_information_threshold_copy_count": (
                scaling[-1].information_threshold_copy_count
            ),
            "polynomial_hidden_permutation_decoder_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "equal_gram_transfer_exists_algebraically": verified,
            "orientation_polar_circuit_implies_physical_pgm_without_intertwiner": False,
            "existing_trace_transfer_is_full_polar_transfer": False,
            "structured_covariant_row_copy_is_full_polar_transfer": True,
            "physical_output_intertwiner_compiled": True,
            "coherent_cross_sector_transfer_proved": True,
            "polynomial_physical_pgm_circuit_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The structured wreath output transfer is compiled by coherent "
                "row-copy, but Gram equality alone would not have supplied it and "
                "the all-n orientation polar circuit remains open."
            ),
        },
        status=(
            "structured-wreath-transfer-compiled-orientation-polar-open"
            if verified
            else "polar-factor-transfer-validation-failure"
        ),
        summary=(
            "Proved the exact partial-isometry relation between equal-Gram polar "
            "factors, retained the generic nonconstructivity gate, and recorded "
            "that the wreath-specific coherent Fourier row-copy theorem now "
            "supplies the physical-output intertwiner."
        ),
        falsifiers_triggered=[
            (
                "Do not promote orientation Gram normalization to a physical PGM "
                "implementation using spectrum or Gram equality alone."
            ),
            (
                "The selected trace-transfer identity was insufficient by itself; "
                "the stronger vector-level row-copy identity is required."
            ),
            (
                "The physical-output gate is closed; higher-level relative "
                "sampling is now the sole PGM implementation gate."
            ),
        ],
    )


def write_polar_factor_transfer_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_polar_factor_transfer())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_polar_factor_transfer_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
