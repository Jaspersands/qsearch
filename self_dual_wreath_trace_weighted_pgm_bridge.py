"""Transfer trace-weighted orientation truncation to the physical PGM.

The orientation frame uses the unnormalised projector sum

    R x = direct_sum_e E_e x,       S = R^* R = sum_e E_e.

For a fixed ``S_n`` Fourier sector and row, the physical PGM analysis has the
exact factorisation

    A = w^(-1/2) R^* C,             C C^* R = R,             (1)

where ``w=2^k`` is the orientation count and ``C`` is the generalized Fourier
row-copy partial isometry.  Consequently

    A A^* = S/w                                                   (2)

and the exact PGM coisometry is ``Q^* C`` for ``Q=R S^(-1/2)``.

Let ``Q_tau=R S^(-1/2) 1_[tau,infinity)(S)``.  On the normalized physical
sector average ``rho=A^*A/tr(A^*A)``, equations (1)--(2) give

    tr((Q^*C-Q_tau^*C)^*(Q^*C-Q_tau^*C) rho)
      = tr(S 1_(0,tau)(S))/tr(S).                              (3)

The same number is the failure probability of the failure-flagged truncated
coisometry.  Thus the trace-weighted orientation bound is exactly the relevant
physical PGM average-state bound, sector by sector.  Averaging sectors cannot
increase it.

The scale distinction is essential.  A cutoff ``tau`` on ``S`` corresponds to
``tau/w`` on the raw averaged frame ``AA^*``.  Applying the same absolute
``tau`` to ``AA^*`` would generally delete useful mass and is not certified by
this theorem.  The result still assumes a tightly normalized implementation of
the rescaled orientation polar; it does not provide one.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import hook_length_dimension
from research_registry import utc_now
from self_dual_wreath_coherent_fourier_decoder import symmetric_group_fourier_matrix
from self_dual_wreath_orientation_fourier_reduction import (
    orientation_invariant_projector,
)
from self_dual_wreath_physical_pgm_intertwiner import (
    _branch_representation_rows,
    _fourier_offsets,
    _orientation_order_sector_row,
    _sector_row_block,
    generalized_fourier_row_copy_isometry,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_trace_weighted_pgm_bridge.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-CODE-SELF-DUAL-WREATH-TRACE-WEIGHTED-PGM-BRIDGE"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Label = tuple[Partition, Partition]


@dataclass(frozen=True)
class PhysicalTraceWeightedBridgeControl:
    control_id: str
    n: int
    labels: tuple[Label, ...]
    target_partition: Partition
    fourier_row_index: int
    orientation_count: int
    physical_sector_dimension: int
    rescaled_frame_dimension: int
    rescaled_frame_trace: float
    rescaled_frame_rank: int
    truncation_threshold: float
    corresponding_raw_frame_threshold: float
    minimum_positive_rescaled_frame_eigenvalue: float
    minimum_positive_raw_frame_eigenvalue: float
    discarded_rescaled_frame_mass: float
    physical_average_polar_error: float
    physical_average_failure_probability: float
    single_sector_trace_distance_upper_bound: float
    physical_analysis_factorization_residual: float
    row_copy_range_identity_residual: float
    raw_to_rescaled_frame_spectrum_residual: float
    physical_weighted_error_identity_residual: float
    physical_failure_identity_residual: float
    exact_physical_trace_weighted_bridge_verified: bool
    status: str


@dataclass(frozen=True)
class TraceWeightedPgmBridgeReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[PhysicalTraceWeightedBridgeControl]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _spectral_polar_data(
    analysis: np.ndarray,
    frame: np.ndarray,
    threshold: float,
    tolerance: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    hermitian = (frame + frame.conj().T) / 2
    values, vectors = np.linalg.eigh(hermitian)
    if values[0] < -100 * tolerance:
        raise ValueError("frame must be positive semidefinite")
    positive = values > tolerance
    retained = values >= threshold
    low = positive & ~retained
    inverse_values = np.zeros_like(values)
    truncated_values = np.zeros_like(values)
    inverse_values[positive] = values[positive] ** -0.5
    truncated_values[retained] = values[retained] ** -0.5
    inverse = (vectors * inverse_values) @ vectors.conj().T
    truncated_inverse = (vectors * truncated_values) @ vectors.conj().T
    low_projector = vectors[:, low] @ vectors[:, low].conj().T
    return analysis @ inverse, analysis @ truncated_inverse, low_projector, values


def _positive_spectrum(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    values = np.linalg.eigvalsh((matrix + matrix.conj().T) / 2)
    return values[values > tolerance]


def audit_physical_trace_weighted_bridge(
    n: int,
    labels: tuple[Label, ...],
    threshold: float,
    *,
    control_prefix: str,
    tolerance: float = 1e-9,
) -> list[PhysicalTraceWeightedBridgeControl]:
    """Audit equation (3) in every active Fourier sector and row."""

    if not labels or threshold <= 100 * tolerance:
        raise ValueError("need unequal labels and a positive threshold")
    if any(
        sum(left) != n or sum(right) != n or left == right
        for left, right in labels
    ):
        raise ValueError("labels must be unequal partition pairs of n")

    orientation_count = 1 << len(labels)
    carrier_dimension = math.prod(
        hook_length_dimension(left) * hook_length_dimension(right)
        for left, right in labels
    )
    physical_dimension = orientation_count * carrier_dimension
    rows = _branch_representation_rows(labels)
    row_copy, permutations, partitions = generalized_fourier_row_copy_isometry(
        n,
        rows,
    )
    base_adjoint = np.hstack(
        tuple(np.eye(carrier_dimension) for _ in range(orientation_count))
    ) / math.sqrt(orientation_count)
    group_analysis = np.vstack(
        [base_adjoint @ matrix.conj().T for _, matrix in rows]
    ) / math.sqrt(len(permutations))
    fourier, _, _ = symmetric_group_fourier_matrix(n)
    physical_analysis = (
        np.kron(fourier.T.conj(), np.eye(carrier_dimension)) @ group_analysis
    )
    offsets = _fourier_offsets(n)

    controls: list[PhysicalTraceWeightedBridgeControl] = []
    for partition in partitions:
        irrep_dimension = hook_length_dimension(partition)
        projectors = tuple(
            orientation_invariant_projector(partition, labels, orientation)
            for orientation in range(orientation_count)
        )
        orientation_analysis = np.vstack(projectors)
        frame = orientation_analysis.conj().T @ orientation_analysis
        frame_trace = float(np.trace(frame).real)
        if frame_trace <= tolerance:
            continue
        polar, truncated_polar, low_projector, frame_values = _spectral_polar_data(
            orientation_analysis,
            frame,
            threshold,
            tolerance,
        )
        positive_frame = frame_values[frame_values > tolerance]
        discarded = float(np.trace(frame @ low_projector).real / frame_trace)

        for row_index in range(irrep_dimension):
            physical_sector = _sector_row_block(
                physical_analysis,
                group_offset=offsets[partition],
                irrep_dimension=irrep_dimension,
                row_index=row_index,
                residual_dimension=carrier_dimension,
            )
            if np.linalg.norm(physical_sector, ord=2) <= tolerance:
                continue
            row_copy_sector = _sector_row_block(
                row_copy,
                group_offset=offsets[partition],
                irrep_dimension=irrep_dimension,
                row_index=row_index,
                residual_dimension=physical_dimension,
            )
            oriented_row_copy = _orientation_order_sector_row(
                row_copy_sector,
                orientation_count=orientation_count,
                irrep_dimension=irrep_dimension,
                carrier_dimension=carrier_dimension,
            )
            expected_analysis = (
                orientation_analysis.conj().T @ oriented_row_copy
            ) / math.sqrt(orientation_count)
            factorization_residual = float(
                np.linalg.norm(physical_sector - expected_analysis, ord=2)
            )
            range_residual = float(
                np.linalg.norm(
                    (np.eye(oriented_row_copy.shape[0])
                     - oriented_row_copy @ oriented_row_copy.conj().T)
                    @ orientation_analysis,
                    ord=2,
                )
            )

            raw_frame = physical_sector @ physical_sector.conj().T
            raw_positive = _positive_spectrum(raw_frame, tolerance)
            if len(raw_positive) != len(positive_frame):
                spectrum_residual = math.inf
            else:
                spectrum_residual = float(
                    np.max(
                        np.abs(
                            np.sort(raw_positive) * orientation_count
                            - np.sort(positive_frame)
                        )
                    )
                )

            physical_average = physical_sector.conj().T @ physical_sector
            physical_trace = float(np.trace(physical_average).real)
            if physical_trace <= tolerance:
                continue
            physical_average /= physical_trace
            exact_coisometry = polar.conj().T @ oriented_row_copy
            truncated_coisometry = (
                truncated_polar.conj().T @ oriented_row_copy
            )
            difference = exact_coisometry - truncated_coisometry
            weighted_error = float(
                np.trace(
                    difference.conj().T @ difference @ physical_average
                ).real
            )
            exact_effect = exact_coisometry.conj().T @ exact_coisometry
            retained_effect = (
                truncated_coisometry.conj().T @ truncated_coisometry
            )
            failure = float(
                np.trace((exact_effect - retained_effect) @ physical_average).real
            )
            error_residual = abs(weighted_error - discarded)
            failure_residual = abs(failure - discarded)
            verified = bool(
                factorization_residual <= 100 * tolerance
                and range_residual <= 100 * tolerance
                and spectrum_residual <= 100 * tolerance
                and error_residual <= 100 * tolerance
                and failure_residual <= 100 * tolerance
                and -100 * tolerance <= failure <= 1 + 100 * tolerance
            )
            controls.append(
                PhysicalTraceWeightedBridgeControl(
                    control_id=(
                        f"{control_prefix}-{'-'.join(map(str, partition))}-"
                        f"ROW-{row_index}"
                    ),
                    n=n,
                    labels=labels,
                    target_partition=partition,
                    fourier_row_index=row_index,
                    orientation_count=orientation_count,
                    physical_sector_dimension=physical_average.shape[0],
                    rescaled_frame_dimension=len(frame),
                    rescaled_frame_trace=frame_trace,
                    rescaled_frame_rank=len(positive_frame),
                    truncation_threshold=threshold,
                    corresponding_raw_frame_threshold=(
                        threshold / orientation_count
                    ),
                    minimum_positive_rescaled_frame_eigenvalue=float(
                        positive_frame[0]
                    ),
                    minimum_positive_raw_frame_eigenvalue=float(raw_positive[0]),
                    discarded_rescaled_frame_mass=discarded,
                    physical_average_polar_error=weighted_error,
                    physical_average_failure_probability=failure,
                    single_sector_trace_distance_upper_bound=math.sqrt(
                        max(0.0, 2 * discarded)
                    ),
                    physical_analysis_factorization_residual=factorization_residual,
                    row_copy_range_identity_residual=range_residual,
                    raw_to_rescaled_frame_spectrum_residual=spectrum_residual,
                    physical_weighted_error_identity_residual=error_residual,
                    physical_failure_identity_residual=failure_residual,
                    exact_physical_trace_weighted_bridge_verified=verified,
                    status=(
                        "exact-physical-trace-weighted-pgm-bridge"
                        if verified
                        else "physical-trace-weighted-pgm-bridge-failure"
                    ),
                )
            )
    if not controls:
        raise ValueError("no active physical Fourier sectors")
    return controls


def run_trace_weighted_pgm_bridge() -> TraceWeightedPgmBridgeReport:
    controls = [
        *audit_physical_trace_weighted_bridge(
            3,
            (
                ((3,), (2, 1)),
                ((3,), (1, 1, 1)),
                ((2, 1), (1, 1, 1)),
            ),
            1.5,
            control_prefix="W3-COLLISION-FREE",
        ),
        *audit_physical_trace_weighted_bridge(
            4,
            (
                ((4,), (3, 1)),
                ((2, 2), (2, 1, 1)),
            ),
            0.75,
            control_prefix="W4-PAIR",
        ),
    ]
    failures = sum(
        not row.exact_physical_trace_weighted_bridge_verified for row in controls
    )
    nonzero_discard = sum(row.discarded_rescaled_frame_mass > 1e-10 for row in controls)
    verified = failures == 0 and nonzero_discard > 0
    maximum_residual = max(
        max(
            row.physical_analysis_factorization_residual,
            row.row_copy_range_identity_residual,
            row.raw_to_rescaled_frame_spectrum_residual,
            row.physical_weighted_error_identity_residual,
            row.physical_failure_identity_residual,
        )
        for row in controls
    )
    return TraceWeightedPgmBridgeReport(
        created_at=utc_now(),
        theorem_contract={
            "physical_sector_factorization": (
                "A_(nu,a)=w^(-1/2)R_nu^*C_(nu,a), with "
                "C_(nu,a)C_(nu,a)^*R_nu=R_nu."
            ),
            "raw_frame_scale": "A_(nu,a)A_(nu,a)^*=S_nu/w.",
            "physical_average_identity": (
                "On rho_(nu,a)=A^*A/tr(A^*A), replacing Q_R^*C by "
                "Q_(R,tau)^*C has mean-square error and failure probability "
                "tr(S_nu 1_(0,tau)(S_nu))/tr(S_nu)."
            ),
            "sector_averaging": (
                "The identity is pointwise in every active Fourier sector and "
                "row, so its upper bound survives the natural sector mixture."
            ),
            "scale_warning": (
                "The rescaled-frame cutoff tau corresponds to tau/w on the raw "
                "averaged frame; the same absolute cutoff cannot be transferred."
            ),
        },
        finite_controls=controls,
        proof_obligations=[
            {
                "obligation": "physical_average_state_matches_native_frame_weighting",
                "resolved": verified,
                "resolution": (
                    "Cyclic trace and CC^*R=R reduce the physical sector error "
                    "exactly to the discarded S_nu trace mass."
                ),
            },
            {
                "obligation": "rescaled_vs_raw_cutoff_accounting",
                "resolved": verified,
                "resolution": (
                    "The nonzero spectrum of AA^* is the spectrum of S_nu "
                    "divided by the orientation count w."
                ),
            },
            {
                "obligation": "tightly_normalized_orientation_polar_access",
                "resolved": False,
                "resolution": (
                    "The bridge proves the correct error measure but does not "
                    "construct access to the rescaled polar without sqrt(w) cost."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "The native S/tr(S) state is unrelated to the physical PGM input.",
                "resolved": verified,
                "resolution": (
                    "It is exactly the pullback of A^*A/tr(A^*A) through the "
                    "physical row-copy intertwiner, sector by sector."
                ),
            },
            {
                "objection": "An inverse-polynomial cutoff can be applied directly to the raw PGM frame.",
                "resolved": True,
                "resolution": (
                    "False: the raw frame is S/w. The corresponding raw cutoff "
                    "is tau/w, which is factorially small at information threshold."
                ),
            },
            {
                "objection": "The bridge itself supplies a polynomial PGM circuit.",
                "resolved": False,
                "resolution": (
                    "No tightly normalized implementation of Q_R or its tree "
                    "relative isometries is supplied."
                ),
            },
        ],
        headline_metrics={
            "physical_trace_weighted_bridge_theorem_count": int(verified),
            "finite_sector_row_control_count": len(controls),
            "finite_nonzero_discard_control_count": nonzero_discard,
            "finite_validation_failure_count": failures,
            "maximum_identity_residual": maximum_residual,
            "tight_orientation_polar_access_theorem_count": 0,
            "polynomial_pgm_circuit_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "physical_average_state_bridge_proved": verified,
            "pointwise_fourier_sector_bridge_proved": verified,
            "rescaled_orientation_cutoff_is_the_correct_cutoff": verified,
            "same_absolute_cutoff_on_raw_pgm_frame_allowed": False,
            "tightly_normalized_orientation_polar_access_proved": False,
            "polynomial_physical_pgm_circuit_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Trace-weighted truncation now transfers exactly to the physical "
                "PGM average state, but efficient normalized orientation-polar "
                "access remains open."
            ),
        },
        status=(
            "physical-trace-weighted-bridge-proved-tight-access-open"
            if verified
            else "physical-trace-weighted-bridge-validation-failure"
        ),
        summary=(
            "Proved that discarded rescaled orientation-frame trace mass is "
            "exactly the physical PGM average failure, while isolating the "
            "factorial raw-frame rescaling that an implementation must bypass."
        ),
        falsifiers_triggered=[
            "The trace-weighted native frame is not an artificial surrogate; it is the physical sector average under the exact intertwiner.",
            "The same inverse-polynomial absolute cutoff cannot be applied to the raw averaged PGM frame.",
            "The remaining obstacle is normalized structured access, not a missing average-state bridge.",
        ],
    )


def write_trace_weighted_pgm_bridge_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_trace_weighted_pgm_bridge())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_trace_weighted_pgm_bridge_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
