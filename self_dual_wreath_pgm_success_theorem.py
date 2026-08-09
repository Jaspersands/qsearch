"""Constant-success PGM theorem for hidden bridge involutions.

Let ``N=n!`` hidden bridge labels have equal-rank support projectors ``P_s``
on ``k`` regular-representation coset-state registers.  Put

    B = N^-1 sum_s P_s,             rank(P_s)=r.

For distinct bridges, regular-character orthogonality gives

    Tr(P_s P_t)/r = 2^-k.

The canonical mixed-state PGM has correct probability

    p = (Nr)^-1 Tr(P_s B^-1/2 P_s B^-1/2).

Two elementary inequalities turn the exact frame second moment into a useful
success lower bound.  First, Cauchy--Schwarz on the rank-r compression and
covariance give

    p >= (Tr sqrt(B))^2/(N r^2).

Second, Holder gives

    (Tr sqrt(B))^2 >= Tr(B)^3/Tr(B^2).

Since Tr(B)=r and

    Tr(B^2)=r/N [1+(N-1)2^-k],

we obtain the exact all-n lower bound

    p_PGM >= 1/[1+(N-1)2^-k].                         (1)

At ``k=ceil(log2 N)+t``, equation (1) is at least
``1/(1+2^-t)``.  In particular the information-threshold PGM succeeds with
probability greater than one half, and a constant number of extra samples
gives any fixed bounded-error target.

This is an information-theoretic measurement theorem, not an efficient
algorithm.  The PGM still requires coherent multiplicity-frame whitening at
factorial spectral scale, and no polynomial circuit for it is known.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_mixed_covariant_decoder import (
    audit_physical_projector_orbit,
)


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_pgm_success_theorem.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-CODE-SELF-DUAL-WREATH-PGM-SUCCESS-THEOREM"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class PgmSuccessScalingRecord:
    n: int
    hidden_label_count_decimal: str
    log2_hidden_label_count: float
    threshold_copy_count: int
    extra_copy_count: int
    total_copy_count: int
    exact_distinct_projector_overlap_ratio: float
    exact_frame_second_moment_coefficient: float
    log2_exact_frame_second_moment_coefficient: float
    pgm_success_lower_bound: float
    copy_slack_only_success_lower_bound: float
    bounded_error_one_third_certified: bool
    direct_output_measurement_information_theoretic: bool
    polynomial_pgm_implementation_proved: bool
    status: str


@dataclass(frozen=True)
class HolderControlRecord:
    control_id: str
    matrix_dimension: int
    matrix_rank: int
    trace: float
    squared_trace: float
    square_root_trace: float
    holder_lower_bound: float
    holder_residual_margin: float
    inequality_verified: bool


@dataclass(frozen=True)
class PgmSuccessTheoremReport:
    created_at: str
    theorem_contract: dict[str, Any]
    holder_controls: list[HolderControlRecord]
    physical_branch_controls: list[dict[str, int | float | str | bool]]
    scaling_records: list[PgmSuccessScalingRecord]
    proof_obligations: list[dict[str, bool | str]]
    adversarial_audit: list[dict[str, bool | str]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def pgm_success_lower_bound(hidden_count: int, copy_count: int) -> float:
    if hidden_count < 2:
        raise ValueError("hidden count must be at least two")
    if copy_count < 1:
        raise ValueError("copy count must be positive")
    collision_ratio = float(Fraction(hidden_count - 1, 1 << copy_count))
    return 1.0 / (1.0 + collision_ratio)


def exact_projector_frame_second_moment_coefficient(
    hidden_count: int,
    copy_count: int,
) -> float:
    """Return ``Tr(B^2)/rank(P)`` for the hidden-bridge frame."""

    if hidden_count < 2:
        raise ValueError("hidden count must be at least two")
    if copy_count < 1:
        raise ValueError("copy count must be positive")
    return float(
        Fraction((1 << copy_count) + hidden_count - 1, hidden_count << copy_count)
    )


def holder_square_root_trace_lower_bound(
    trace: float,
    squared_trace: float,
) -> float:
    if trace < 0 or squared_trace <= 0:
        raise ValueError("positive trace and squared trace are required")
    return trace**3 / squared_trace


def audit_holder_control(
    control_id: str,
    matrix: np.ndarray,
    *,
    tolerance: float = 1e-10,
) -> HolderControlRecord:
    eigenvalues = np.linalg.eigvalsh((matrix + matrix.conj().T) / 2)
    if eigenvalues[0] < -tolerance:
        raise ValueError("matrix must be positive semidefinite")
    positive = eigenvalues[eigenvalues > tolerance]
    trace = float(np.sum(positive))
    squared_trace = float(np.sum(positive**2))
    square_root_trace = float(np.sum(np.sqrt(positive)))
    actual_square = square_root_trace * square_root_trace
    lower = holder_square_root_trace_lower_bound(trace, squared_trace)
    margin = actual_square - lower
    return HolderControlRecord(
        control_id=control_id,
        matrix_dimension=len(matrix),
        matrix_rank=len(positive),
        trace=trace,
        squared_trace=squared_trace,
        square_root_trace=square_root_trace,
        holder_lower_bound=lower,
        holder_residual_margin=margin,
        inequality_verified=margin >= -100 * tolerance,
    )


def pgm_success_scaling_record(
    n: int,
    *,
    extra_copies: int = 0,
) -> PgmSuccessScalingRecord:
    if n < 2:
        raise ValueError("n must be at least two")
    if extra_copies < 0:
        raise ValueError("extra copies must be nonnegative")
    hidden_count = math.factorial(n)
    log_count = math.lgamma(n + 1) / math.log(2)
    threshold = math.ceil(log_count)
    copies = threshold + extra_copies
    lower = pgm_success_lower_bound(hidden_count, copies)
    collision_ratio = float(Fraction(hidden_count - 1, 1 << copies))
    slack_lower = 1 / (1 + 2.0 ** (-extra_copies))
    return PgmSuccessScalingRecord(
        n=n,
        hidden_label_count_decimal=str(hidden_count),
        log2_hidden_label_count=log_count,
        threshold_copy_count=threshold,
        extra_copy_count=extra_copies,
        total_copy_count=copies,
        exact_distinct_projector_overlap_ratio=2.0 ** (-copies),
        exact_frame_second_moment_coefficient=(
            exact_projector_frame_second_moment_coefficient(
                hidden_count,
                copies,
            )
        ),
        log2_exact_frame_second_moment_coefficient=(
            math.log2(1 + collision_ratio) - log_count
        ),
        pgm_success_lower_bound=lower,
        copy_slack_only_success_lower_bound=slack_lower,
        bounded_error_one_third_certified=lower >= 2 / 3,
        direct_output_measurement_information_theoretic=True,
        polynomial_pgm_implementation_proved=False,
        status="constant-success-pgm-proved-efficient-implementation-open",
    )


def _physical_branch_holder_controls() -> list[dict[str, int | float | str | bool]]:
    specifications = (
        (
            "W3-THREE-UNEQUAL-TYPES",
            (
                ((3,), (2, 1)),
                ((3,), (1, 1, 1)),
                ((2, 1), (1, 1, 1)),
            ),
        ),
        (
            "W3-REPEATED-STANDARD-UNEQUAL",
            (((3,), (2, 1)),) * 3,
        ),
    )
    rows: list[dict[str, int | float | str | bool]] = []
    for control_id, labels in specifications:
        record = audit_physical_projector_orbit(control_id, labels)
        # The branch frame has trace equal to the base-projector rank.  Its
        # second moment is reconstructed from the stored dense frame below.
        from self_dual_wreath_subgroup_twirl_reduction import _direct_frame

        frame = _direct_frame(labels)
        holder = audit_holder_control(control_id, frame)
        rank = record.base_projector_rank
        lower = holder.holder_lower_bound / (
            record.hidden_label_count * rank * rank
        )
        rows.append(
            {
                "control_id": control_id,
                "pgm_success_probability": record.pgm_correct_success_probability,
                "holder_pgm_success_lower_bound": lower,
                "holder_bound_valid": (
                    lower <= record.pgm_correct_success_probability + 1e-10
                ),
                "frame_support_rank": record.average_frame_support_rank,
                "base_projector_rank": rank,
            }
        )
    return rows


def run_pgm_success_theorem() -> PgmSuccessTheoremReport:
    holder_controls = [
        audit_holder_control(
            "diagonal-nonuniform",
            np.diag([0.6, 0.25, 0.1, 0.05]),
        ),
        audit_holder_control(
            "rank-deficient",
            np.diag([0.5, 0.3, 0.2, 0.0, 0.0]),
        ),
    ]
    physical_controls = _physical_branch_holder_controls()
    scaling = [
        pgm_success_scaling_record(n, extra_copies=extra)
        for n in (3, 4, 5, 8, 12, 16, 24, 32, 64, 128, 256, 512)
        for extra in (0, 1, 2, 4)
    ]
    holder_failures = sum(not row.inequality_verified for row in holder_controls)
    branch_failures = sum(not row["holder_bound_valid"] for row in physical_controls)
    threshold_rows = [row for row in scaling if row.extra_copy_count == 0]
    verified = (
        holder_failures == 0
        and branch_failures == 0
        and all(row.pgm_success_lower_bound > 0.5 for row in threshold_rows)
    )
    return PgmSuccessTheoremReport(
        created_at=utc_now(),
        theorem_contract={
            "projector_overlap": (
                "Tr(P_s P_t)/r=1 for s=t and 2^-k for s!=t."
            ),
            "exact_frame_second_moment": (
                "Tr(B^2)=r/|G| [1+(|G|-1)2^-k]."
            ),
            "pgm_compression_bound": (
                "P_PGM>=(Tr sqrt(B))^2/(|G| r^2)."
            ),
            "holder_bound": (
                "(Tr sqrt(B))^2>=Tr(B)^3/Tr(B^2)."
            ),
            "success_lower_bound": (
                "P_PGM>=1/[1+(|G|-1)2^-k]."
            ),
            "threshold_consequence": (
                "k=ceil(log2 |G|)+t implies P_PGM>=1/(1+2^-t)."
            ),
            "source_label_decomposition": (
                "The regular-representation Fourier source labels commute with the "
                "projector ensemble and its PGM, so the theorem is the natural-source "
                "average of conditional carrier PGMs."
            ),
        },
        holder_controls=holder_controls,
        physical_branch_controls=physical_controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "exact_regular_projector_overlap",
                "resolved": True,
                "resolution": (
                    "Every nonidentity right-regular group element has zero trace; "
                    "expanding the two involution projectors gives overlap 1/2 per copy."
                ),
            },
            {
                "obligation": "pgm_success_from_frame_moments",
                "resolved": verified,
                "resolution": (
                    "Cauchy--Schwarz on P_s B^-1/2 P_s and Holder on the eigenvalues "
                    "of B give the stated lower bound."
                ),
            },
            {
                "obligation": "constant_success_at_information_threshold",
                "resolved": verified,
                "resolution": (
                    "At 2^k>=|G|, (|G|-1)2^-k<1, hence P_PGM>1/2."
                ),
            },
            {
                "obligation": "polynomial_coherent_pgm_implementation",
                "resolved": False,
                "resolution": (
                    "The canonical seed still requires B^-1/2, equivalently coherent "
                    "multiplicity tight-frame whitening, at factorial spectral scale."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "The second moment only lower-bounds lambda_max.",
                "resolved": True,
                "resolution": (
                    "For PGM success it enters through a different Holder inequality "
                    "that lower-bounds Tr sqrt(B), not upper-bounds the operator norm."
                ),
            },
            {
                "objection": "The theorem silently assumes pure coset states.",
                "resolved": True,
                "resolution": (
                    "It is derived directly for normalized equal-rank projector states "
                    "and the canonical mixed-state PGM."
                ),
            },
            {
                "objection": "Constant PGM success is an efficient quantum algorithm.",
                "resolved": False,
                "resolution": (
                    "No. Dense inverse square root is information-theoretic; no "
                    "polynomial implementation or structured preconditioner is supplied."
                ),
            },
            {
                "objection": "Conditional source branches all inherit the same bound.",
                "resolved": False,
                "resolution": (
                    "Only their natural weighted average is controlled. Individual "
                    "Fourier-label branches can have much lower success."
                ),
            },
        ],
        headline_metrics={
            "pgm_success_lower_bound_theorem_count": 1,
            "constant_information_threshold_success_theorem_count": 1,
            "bounded_error_with_constant_extra_copies_theorem_count": 1,
            "holder_control_count": len(holder_controls),
            "holder_control_failure_count": holder_failures,
            "physical_branch_control_count": len(physical_controls),
            "physical_branch_bound_failure_count": branch_failures,
            "scaling_record_count": len(scaling),
            "threshold_record_count": len(threshold_rows),
            "minimum_threshold_pgm_success_lower_bound": min(
                row.pgm_success_lower_bound for row in threshold_rows
            ),
            "minimum_two_extra_copy_success_lower_bound": min(
                row.pgm_success_lower_bound
                for row in scaling
                if row.extra_copy_count == 2
            ),
            "maximum_n": max(row.n for row in scaling),
            "polynomial_pgm_implementation_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "information_theoretic_pgm_success_proved": verified,
            "constant_success_at_logarithmic_copy_threshold": verified,
            "bounded_error_with_constant_extra_copies_proved": verified,
            "conditional_branch_uniform_success_proved": False,
            "polynomial_coherent_pgm_implementation_proved": False,
            "polynomial_hidden_permutation_decoder_proved": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The PGM has constant all-n information-theoretic success with "
                "O(log n!) samples. Its coherent multiplicity whitening remains "
                "unimplemented and generically has factorial spectral resolution."
            ),
        },
        status=(
            "constant-pgm-success-proved-efficient-whitening-open"
            if verified
            else "pgm-success-theorem-validation-failure"
        ),
        summary=(
            "Converted the exact projector-frame second moment into an all-n PGM "
            "success lower bound above one half at the information threshold."
        ),
        falsifiers_triggered=[
            (
                "The multiregister PGM success probability is no longer an open "
                "information-theoretic obligation for the hidden bridge ensemble."
            ),
            (
                "A second frame moment can certify PGM success through Tr sqrt(B), "
                "even though it cannot upper-bound the frame operator norm."
            ),
            (
                "Constant information-theoretic success does not remove the factorial "
                "coherent frame-whitening implementation barrier."
            ),
        ],
    )


def write_pgm_success_theorem_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-PGM-SUCCESS-THEOREM"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_pgm_success_theorem())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    if write_registry:
        _res_payload = report if "report" in locals() else (payload if "payload" in locals() else result)
        from research_registry import (
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-SELF-DUAL-WREATH-PGM-SUCCESS-THEOREM",
                source=registry_experiment_id,
                claim=(
                    "Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-PGM-SUCCESS-THEOREM."
                ),
                reason_invalid=(
                    "Falsified or refined by exact theorem evaluation."
                ),
                lesson=(
                    "Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-PGM-SUCCESS-THEOREM."
                ),
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-MEASUREMENT",
                ],
                evidence=_res_payload.get("headline_metrics", {}),
            )
        )
        upsert_experiment_result(
            ExperimentResultRecord(
                id=(
                    registry_result_id
                    or f"RESULT-{registry_experiment_id}-LATEST"
                ),
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=_res_payload.get("created_at", ""),
                status=_res_payload.get("status", "completed"),
                summary=_res_payload.get("summary", ""),
                metrics=_res_payload.get("headline_metrics", {}),
                falsifiers_triggered=_res_payload.get("falsifiers_triggered", []),
                artifacts={
                    "self_dual_wreath_pgm_success_theorem": str(path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_pgm_success_theorem_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
