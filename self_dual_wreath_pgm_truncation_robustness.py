"""Robust PGM truncation removes dependence on the minimum frame eigenvalue.

Let ``N`` equal-rank-r projectors have average ``B=N^-1 sum_s P_s`` and let
``R_tau=1[B>=tau]``.  Since ``rank(B)<=Nr``, the average input mass discarded
by the low-eigenvalue subspace is

    delta = Tr((I-R_tau)B)/r <= tau rank(B)/r <= N tau. (1)

If ``{E_s}`` is the ideal PGM, then ``{R_tau E_s R_tau}`` plus a failure
outcome is a valid sub-POVM.  The gentle measurement lemma and Jensen give

    p_truncated >= p_PGM - 2 sqrt(delta).               (2)

Choosing ``tau=eta^2/(4N)`` therefore loses at most ``eta`` average correct
probability.  Combined with the all-n PGM theorem,

    p_truncated >= 1/[1+(N-1)2^-k] - eta.              (3)

Thus the implementation need not resolve the actual minimum nonzero
eigenvalue.  It only needs inverse-square-root accuracy above a controlled
``Theta(1/N)`` cutoff.  For ``N=n!`` this is still factorially small in the
normalization-one frame encoding, so generic QSVT remains superpolynomial.
The exact surviving target is a polynomially normalized structured encoding
of ``N B`` (equivalently the coherently controlled rescaled multiplicity
operators ``(N/d_nu)D_nu``).
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_pgm_success_theorem import pgm_success_lower_bound
from self_dual_wreath_subgroup_twirl_reduction import (
    Label,
    _base_tensor_projector,
    _direct_frame,
    tuple_left_subgroup_matrices,
)


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_pgm_truncation_robustness.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-PGM-TRUNCATION-ROBUSTNESS"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class PgmTruncationControl:
    control_id: str
    n: int
    hidden_label_count: int
    physical_dimension: int
    projector_rank: int
    frame_support_rank: int
    loss_budget_eta: float
    spectral_cutoff: float
    discarded_average_input_mass: float
    discarded_mass_rank_upper_bound: float
    ideal_pgm_success_probability: float
    truncated_pgm_success_probability: float
    gentle_success_lower_bound: float
    observed_success_loss: float
    maximum_effect_completeness_violation: float
    exact_truncation_robustness_verified: bool
    status: str


@dataclass(frozen=True)
class PgmTruncationScalingRecord:
    n: int
    hidden_label_count_decimal: str
    information_threshold_copy_count: int
    loss_budget_eta: float
    cutoff_log2: float
    cutoff_value: float
    ideal_pgm_success_lower_bound: float
    truncated_pgm_success_lower_bound: float
    bounded_correct_success_retained: bool
    minimum_eigenvalue_required: bool
    normalization_one_qsvt_polynomial: bool
    polynomial_rescaled_frame_encoding_proved: bool
    status: str


@dataclass(frozen=True)
class PgmTruncationRobustnessReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[PgmTruncationControl]
    scaling_records: list[PgmTruncationScalingRecord]
    proof_obligations: list[dict[str, bool | str]]
    adversarial_audit: list[dict[str, bool | str]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def robust_cutoff(hidden_count: int, loss_budget_eta: float) -> float:
    if hidden_count < 2:
        raise ValueError("hidden count must be at least two")
    if not 0 < loss_budget_eta < 1:
        raise ValueError("loss budget must lie in (0,1)")
    return loss_budget_eta * loss_budget_eta / (4 * hidden_count)


def truncation_success_lower_bound(
    hidden_count: int,
    copy_count: int,
    loss_budget_eta: float,
) -> float:
    if not 0 < loss_budget_eta < 1:
        raise ValueError("loss budget must lie in (0,1)")
    return max(
        0.0,
        pgm_success_lower_bound(hidden_count, copy_count) - loss_budget_eta,
    )


def _inverse_sqrt(matrix: np.ndarray, tolerance: float) -> tuple[np.ndarray, np.ndarray]:
    eigenvalues, eigenvectors = np.linalg.eigh((matrix + matrix.conj().T) / 2)
    positive = eigenvalues > tolerance
    values = np.zeros_like(eigenvalues)
    values[positive] = 1 / np.sqrt(eigenvalues[positive])
    inverse = (eigenvectors * values) @ eigenvectors.conj().T
    return inverse, eigenvalues


def audit_physical_truncation(
    control_id: str,
    labels: tuple[Label, ...],
    *,
    loss_budget_eta: float = 0.5,
    tolerance: float = 1e-10,
) -> PgmTruncationControl:
    if not labels:
        raise ValueError("at least one source label is required")
    n = sum(labels[0][0])
    hidden_count = math.factorial(n)
    projector = _base_tensor_projector(labels)
    rank = int(round(float(np.trace(projector).real)))
    state = projector / rank
    frame = _direct_frame(labels)
    average_state = frame / rank
    inverse, eigenvalues = _inverse_sqrt(average_state, tolerance)
    seed = inverse @ state @ inverse / hidden_count
    seed = (seed + seed.conj().T) / 2
    ideal_success = float(np.trace(seed @ state).real)

    cutoff = robust_cutoff(hidden_count, loss_budget_eta)
    frame_values, frame_vectors = np.linalg.eigh(frame)
    retained = frame_values >= cutoff - tolerance
    high_projector = (
        frame_vectors[:, retained] @ frame_vectors[:, retained].conj().T
    )
    low_projector = np.eye(len(frame)) - high_projector
    discarded_mass = float(np.trace(low_projector @ frame).real / rank)
    rank_bound = cutoff * len(frame_values[frame_values > tolerance]) / rank

    truncated_seed = high_projector @ seed @ high_projector
    truncated_success = float(np.trace(truncated_seed @ state).real)
    gentle_lower = ideal_success - 2 * math.sqrt(max(discarded_mass, 0.0))
    group_rows = tuple_left_subgroup_matrices(labels)
    effect_sum = sum(
        matrix @ truncated_seed @ matrix.conj().T
        for _, matrix in group_rows
    )
    violation = max(
        0.0,
        float(np.linalg.eigvalsh(effect_sum - np.eye(len(frame)))[-1]),
    )
    verified = (
        discarded_mass <= rank_bound + 100 * tolerance
        and rank_bound <= hidden_count * cutoff + 100 * tolerance
        and truncated_success + 100 * tolerance >= gentle_lower
        and violation <= 100 * tolerance
    )
    return PgmTruncationControl(
        control_id=control_id,
        n=n,
        hidden_label_count=hidden_count,
        physical_dimension=len(frame),
        projector_rank=rank,
        frame_support_rank=int(np.count_nonzero(frame_values > tolerance)),
        loss_budget_eta=loss_budget_eta,
        spectral_cutoff=cutoff,
        discarded_average_input_mass=discarded_mass,
        discarded_mass_rank_upper_bound=rank_bound,
        ideal_pgm_success_probability=ideal_success,
        truncated_pgm_success_probability=truncated_success,
        gentle_success_lower_bound=gentle_lower,
        observed_success_loss=ideal_success - truncated_success,
        maximum_effect_completeness_violation=violation,
        exact_truncation_robustness_verified=verified,
        status=(
            "exact-pgm-low-eigenvalue-truncation-control"
            if verified
            else "pgm-truncation-robustness-validation-failure"
        ),
    )


def pgm_truncation_scaling_record(
    n: int,
    *,
    loss_budget_eta: float = 0.1,
) -> PgmTruncationScalingRecord:
    if n < 2:
        raise ValueError("n must be at least two")
    if not 0 < loss_budget_eta < 1:
        raise ValueError("loss budget must lie in (0,1)")
    hidden_count = math.factorial(n)
    log_count = math.lgamma(n + 1) / math.log(2)
    copies = math.ceil(log_count)
    cutoff_log = 2 * math.log2(loss_budget_eta) - 2 - log_count
    lower = truncation_success_lower_bound(
        hidden_count,
        copies,
        loss_budget_eta,
    )
    return PgmTruncationScalingRecord(
        n=n,
        hidden_label_count_decimal=str(hidden_count),
        information_threshold_copy_count=copies,
        loss_budget_eta=loss_budget_eta,
        cutoff_log2=cutoff_log,
        cutoff_value=math.exp2(cutoff_log),
        ideal_pgm_success_lower_bound=pgm_success_lower_bound(
            hidden_count,
            copies,
        ),
        truncated_pgm_success_lower_bound=lower,
        bounded_correct_success_retained=lower > 0.3,
        minimum_eigenvalue_required=False,
        normalization_one_qsvt_polynomial=False,
        polynomial_rescaled_frame_encoding_proved=False,
        status="minimum-eigenvalue-removed-rescaled-frame-access-open",
    )


def run_pgm_truncation_robustness() -> PgmTruncationRobustnessReport:
    controls = [
        audit_physical_truncation(
            "W3-THREE-UNEQUAL-TYPES",
            (
                ((3,), (2, 1)),
                ((3,), (1, 1, 1)),
                ((2, 1), (1, 1, 1)),
            ),
        ),
        audit_physical_truncation(
            "W3-REPEATED-STANDARD-UNEQUAL",
            (((3,), (2, 1)),) * 3,
        ),
    ]
    scaling = [
        pgm_truncation_scaling_record(n)
        for n in (3, 4, 5, 8, 12, 16, 24, 32, 64, 128, 256, 512)
    ]
    failures = sum(not row.exact_truncation_robustness_verified for row in controls)
    verified = failures == 0 and all(row.bounded_correct_success_retained for row in scaling)
    return PgmTruncationRobustnessReport(
        created_at=utc_now(),
        theorem_contract={
            "support_rank": "rank(B)<=N r.",
            "discarded_mass": (
                "For R_tau=1[B>=tau], delta=Tr((I-R_tau)B)/r<=N tau."
            ),
            "gentle_measurement": (
                "Replacing E_s by R_tau E_s R_tau loses at most 2 sqrt(delta) "
                "average correct probability."
            ),
            "robust_cutoff": (
                "tau=eta^2/(4N) implies p_truncated>=p_PGM-eta."
            ),
            "wreath_success": (
                "At k=ceil(log2 n!), p_truncated>=1/[1+(n!-1)2^-k]-eta."
            ),
            "rescaled_access_target": (
                "A polynomial implementation needs structured access to n! B, or "
                "coherently to (n!/d_nu)D_nu, above constant rescaled cutoff."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "minimum_eigenvalue_independent_pgm_truncation",
                "resolved": verified,
                "resolution": (
                    "Rank(B)<=Nr and the gentle measurement lemma control average "
                    "loss without any lower bound on lambda_min(B)."
                ),
            },
            {
                "obligation": "constant_success_above_inverse_label_cutoff",
                "resolved": verified,
                "resolution": (
                    "Combining eta=0.1 with the all-n threshold PGM bound leaves "
                    "more than 0.4 certified average correct probability."
                ),
            },
            {
                "obligation": "polynomially_normalized_rescaled_frame_encoding",
                "resolved": False,
                "resolution": (
                    "The available LCU has normalization one for B, so resolving "
                    "Theta(1/n!) remains factorial despite truncation robustness."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "An exponentially tiny lambda_min forces exact inversion.",
                "resolved": True,
                "resolution": (
                    "Low eigenvalues carrying at most eta^2/4 average mass can be "
                    "discarded with at most eta success loss."
                ),
            },
            {
                "objection": "The cutoff can be raised to inverse polynomial in n.",
                "resolved": False,
                "resolution": (
                    "The universal rank bound only permits Theta(1/n!) in the raw "
                    "normalization. A stronger spectral/rank theorem would be needed."
                ),
            },
            {
                "objection": "Robust truncation makes generic QSVT efficient.",
                "resolved": False,
                "resolution": (
                    "The cutoff is still factorially small; existing Bernstein and "
                    "black-box search lower bounds still apply to raw frame access."
                ),
            },
            {
                "objection": "The finite controls prove the asymptotic circuit.",
                "resolved": False,
                "resolution": (
                    "They validate the inequality only. No rescaled block encoding or "
                    "multiplicity inverse circuit is constructed."
                ),
            },
        ],
        headline_metrics={
            "minimum_eigenvalue_independent_truncation_theorem_count": 1,
            "gentle_pgm_success_robustness_theorem_count": 1,
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "scaling_record_count": len(scaling),
            "minimum_truncated_threshold_success_lower_bound": min(
                row.truncated_pgm_success_lower_bound for row in scaling
            ),
            "maximum_n": scaling[-1].n,
            "tail_cutoff_log2": scaling[-1].cutoff_log2,
            "polynomial_rescaled_frame_encoding_count": 0,
            "polynomial_multiplicity_inverse_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "minimum_frame_eigenvalue_required_for_constant_success": False,
            "inverse_label_scale_cutoff_suffices": verified,
            "constant_truncated_pgm_success_proved": verified,
            "normalization_one_qsvt_route_polynomial": False,
            "polynomial_rescaled_frame_encoding_proved": False,
            "polynomial_multiplicity_inverse_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The minimum eigenvalue is removed from the success obligation, but "
                "the sufficient cutoff remains Theta(1/n!) in raw frame units. A "
                "structured encoding of n!B is still required."
            ),
        },
        status=(
            "pgm-robust-above-inverse-label-cutoff-rescaled-access-open"
            if verified
            else "pgm-truncation-robustness-validation-failure"
        ),
        summary=(
            "Proved that constant PGM success only requires inversion above a "
            "controlled Theta(1/n!) cutoff, independent of lambda_min(B)."
        ),
        falsifiers_triggered=[
            (
                "The actual minimum nonzero frame eigenvalue is not an algorithmic "
                "proof obligation for bounded average success."
            ),
            (
                "Raw normalization-one QSVT remains factorial because the robust "
                "cutoff is still Theta(1/n!)."
            ),
            (
                "The decisive positive target is now a polynomially normalized "
                "representation-specific encoding of n!B or its multiplicity blocks."
            ),
        ],
    )


def write_pgm_truncation_robustness_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_pgm_truncation_robustness())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_pgm_truncation_robustness_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
