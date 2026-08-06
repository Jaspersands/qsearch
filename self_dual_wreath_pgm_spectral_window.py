"""Constant-condition spectral window retaining constant PGM success.

For the hidden-bridge projector frame ``B`` with ``N`` hypotheses, choose

    R = 1[alpha/N <= B <= beta/N].

The low tail has average input mass at most ``alpha`` by ``rank(B)<=Nr``.
The high tail is bounded by the exact second moment:

    delta_high <= N Tr(B^2)/(beta r)
               = [1+(N-1)2^-k]/beta.

Hence

    delta_window <= alpha + [1+(N-1)2^-k]/beta.        (1)

Restricting the ideal PGM effects to ``R`` loses at most
``2 sqrt(delta_window)`` average correct probability.  At
``k=ceil(log2 N)``, fixed constants such as ``alpha=10^-4`` and ``beta=400``
leave a success lower bound above 0.35 while every retained eigenvalue of
``N B`` lies in ``[alpha,beta]``.  The retained condition number is the fixed
constant ``beta/alpha``, independent of ``n``.

This closes minimum-eigenvalue and asymptotic-condition-number objections at
the information-theoretic level.  It does not implement ``R``.  Generic raw
frame filtering at endpoints Theta(1/n!) remains superpolynomial; a useful
algorithm must realize this window from representation/multiplicity labels or
another better-scaled access model.
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
    "research/representation/self_dual_wreath_pgm_spectral_window.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-CODE-SELF-DUAL-WREATH-PGM-SPECTRAL-WINDOW"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class PgmSpectralWindowControl:
    control_id: str
    n: int
    hidden_label_count: int
    projector_rank: int
    frame_support_rank: int
    lower_rescaled_cutoff: float
    upper_rescaled_cutoff: float
    retained_condition_number_upper_bound: float
    observed_discarded_average_mass: float
    low_tail_mass_upper_bound: float
    high_tail_mass_upper_bound: float
    total_discarded_mass_upper_bound: float
    ideal_pgm_success_probability: float
    windowed_pgm_success_probability: float
    gentle_window_success_lower_bound: float
    maximum_effect_completeness_violation: float
    exact_spectral_window_validation: bool
    status: str


@dataclass(frozen=True)
class PgmSpectralWindowScalingRecord:
    n: int
    hidden_label_count_decimal: str
    information_threshold_copy_count: int
    lower_rescaled_cutoff: float
    upper_rescaled_cutoff: float
    raw_lower_cutoff_log2: float
    raw_upper_cutoff_log2: float
    retained_condition_number_upper_bound: float
    discarded_mass_upper_bound: float
    ideal_pgm_success_lower_bound: float
    windowed_pgm_success_lower_bound: float
    constant_condition_and_success_certified: bool
    structured_window_projector_circuit_proved: bool
    status: str


@dataclass(frozen=True)
class PgmSpectralWindowReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[PgmSpectralWindowControl]
    scaling_records: list[PgmSpectralWindowScalingRecord]
    proof_obligations: list[dict[str, bool | str]]
    adversarial_audit: list[dict[str, bool | str]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def window_discarded_mass_upper_bound(
    hidden_count: int,
    copy_count: int,
    alpha: float,
    beta: float,
) -> float:
    if hidden_count < 2:
        raise ValueError("hidden count must be at least two")
    if copy_count < 1:
        raise ValueError("copy count must be positive")
    if not 0 < alpha < beta:
        raise ValueError("window constants must satisfy 0<alpha<beta")
    collision_factor = 1 + (hidden_count - 1) / (1 << copy_count)
    return min(1.0, alpha + collision_factor / beta)


def windowed_pgm_success_lower_bound(
    hidden_count: int,
    copy_count: int,
    alpha: float,
    beta: float,
) -> float:
    discarded = window_discarded_mass_upper_bound(
        hidden_count,
        copy_count,
        alpha,
        beta,
    )
    return max(
        0.0,
        pgm_success_lower_bound(hidden_count, copy_count)
        - 2 * math.sqrt(discarded),
    )


def _inverse_sqrt(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    eigenvalues, eigenvectors = np.linalg.eigh((matrix + matrix.conj().T) / 2)
    positive = eigenvalues > tolerance
    values = np.zeros_like(eigenvalues)
    values[positive] = 1 / np.sqrt(eigenvalues[positive])
    return (eigenvectors * values) @ eigenvectors.conj().T


def audit_physical_spectral_window(
    control_id: str,
    labels: tuple[Label, ...],
    *,
    alpha: float = 0.01,
    beta: float = 20.0,
    tolerance: float = 1e-10,
) -> PgmSpectralWindowControl:
    if not labels:
        raise ValueError("at least one source label is required")
    if not 0 < alpha < beta:
        raise ValueError("window constants must satisfy 0<alpha<beta")
    n = sum(labels[0][0])
    hidden_count = math.factorial(n)
    projector = _base_tensor_projector(labels)
    rank = int(round(float(np.trace(projector).real)))
    state = projector / rank
    frame = _direct_frame(labels)
    average_state = frame / rank
    inverse = _inverse_sqrt(average_state, tolerance)
    seed = inverse @ state @ inverse / hidden_count
    seed = (seed + seed.conj().T) / 2
    ideal_success = float(np.trace(seed @ state).real)

    eigenvalues, eigenvectors = np.linalg.eigh(frame)
    lower = alpha / hidden_count
    upper = beta / hidden_count
    retained = (eigenvalues >= lower - tolerance) & (
        eigenvalues <= upper + tolerance
    )
    window = eigenvectors[:, retained] @ eigenvectors[:, retained].conj().T
    discarded = np.eye(len(frame)) - window
    discarded_mass = float(np.trace(discarded @ frame).real / rank)
    low_bound = alpha
    # Conditional Fourier-source branches need not retain the uniform global
    # overlap formula, so the finite control uses its directly measured second
    # moment.  The scalable full-ensemble theorem substitutes the exact bridge
    # overlap expression below.
    high_bound = (
        hidden_count * float(np.trace(frame @ frame).real) / (beta * rank)
    )
    total_bound = min(1.0, low_bound + high_bound)

    windowed_seed = window @ seed @ window
    windowed_success = float(np.trace(windowed_seed @ state).real)
    gentle_lower = ideal_success - 2 * math.sqrt(max(discarded_mass, 0.0))
    group_rows = tuple_left_subgroup_matrices(labels)
    effect_sum = sum(
        matrix @ windowed_seed @ matrix.conj().T
        for _, matrix in group_rows
    )
    violation = max(
        0.0,
        float(np.linalg.eigvalsh(effect_sum - np.eye(len(frame)))[-1]),
    )
    verified = (
        discarded_mass <= total_bound + 100 * tolerance
        and windowed_success + 100 * tolerance >= gentle_lower
        and violation <= 100 * tolerance
    )
    return PgmSpectralWindowControl(
        control_id=control_id,
        n=n,
        hidden_label_count=hidden_count,
        projector_rank=rank,
        frame_support_rank=int(np.count_nonzero(eigenvalues > tolerance)),
        lower_rescaled_cutoff=alpha,
        upper_rescaled_cutoff=beta,
        retained_condition_number_upper_bound=beta / alpha,
        observed_discarded_average_mass=discarded_mass,
        low_tail_mass_upper_bound=low_bound,
        high_tail_mass_upper_bound=high_bound,
        total_discarded_mass_upper_bound=total_bound,
        ideal_pgm_success_probability=ideal_success,
        windowed_pgm_success_probability=windowed_success,
        gentle_window_success_lower_bound=gentle_lower,
        maximum_effect_completeness_violation=violation,
        exact_spectral_window_validation=verified,
        status=(
            "exact-constant-condition-pgm-window-control"
            if verified
            else "pgm-spectral-window-validation-failure"
        ),
    )


def spectral_window_scaling_record(
    n: int,
    *,
    alpha: float = 1e-4,
    beta: float = 400.0,
) -> PgmSpectralWindowScalingRecord:
    if n < 2:
        raise ValueError("n must be at least two")
    hidden_count = math.factorial(n)
    log_count = math.lgamma(n + 1) / math.log(2)
    copies = math.ceil(log_count)
    discarded = window_discarded_mass_upper_bound(
        hidden_count,
        copies,
        alpha,
        beta,
    )
    ideal = pgm_success_lower_bound(hidden_count, copies)
    lower = max(0.0, ideal - 2 * math.sqrt(discarded))
    return PgmSpectralWindowScalingRecord(
        n=n,
        hidden_label_count_decimal=str(hidden_count),
        information_threshold_copy_count=copies,
        lower_rescaled_cutoff=alpha,
        upper_rescaled_cutoff=beta,
        raw_lower_cutoff_log2=math.log2(alpha) - log_count,
        raw_upper_cutoff_log2=math.log2(beta) - log_count,
        retained_condition_number_upper_bound=beta / alpha,
        discarded_mass_upper_bound=discarded,
        ideal_pgm_success_lower_bound=ideal,
        windowed_pgm_success_lower_bound=lower,
        constant_condition_and_success_certified=(
            beta / alpha < math.inf and lower > 0.3
        ),
        structured_window_projector_circuit_proved=False,
        status="constant-condition-window-exists-structured-projector-open",
    )


def run_pgm_spectral_window() -> PgmSpectralWindowReport:
    controls = [
        audit_physical_spectral_window(
            "W3-THREE-UNEQUAL-TYPES",
            (
                ((3,), (2, 1)),
                ((3,), (1, 1, 1)),
                ((2, 1), (1, 1, 1)),
            ),
        ),
        audit_physical_spectral_window(
            "W3-REPEATED-STANDARD-UNEQUAL",
            (((3,), (2, 1)),) * 3,
        ),
    ]
    scaling = [
        spectral_window_scaling_record(n)
        for n in (8, 12, 16, 24, 32, 64, 128, 256, 512)
    ]
    failures = sum(not row.exact_spectral_window_validation for row in controls)
    verified = failures == 0 and all(
        row.constant_condition_and_success_certified for row in scaling
    )
    return PgmSpectralWindowReport(
        created_at=utc_now(),
        theorem_contract={
            "window": "R=1[alpha/N<=B<=beta/N].",
            "low_tail": "delta_low<=alpha from rank(B)<=Nr.",
            "high_tail": (
                "delta_high<=[1+(N-1)2^-k]/beta from Tr(B^2)."
            ),
            "window_mass": (
                "delta_window<=alpha+[1+(N-1)2^-k]/beta."
            ),
            "window_success": (
                "p_window>=p_PGM-2sqrt(delta_window)."
            ),
            "condition_number": (
                "On the retained support, kappa(NB)<=beta/alpha, independent of n."
            ),
            "implementation_boundary": (
                "Construct R from representation/multiplicity structure; generic raw "
                "spectral filtering at 1/n! scale is already ruled out."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "constant_mass_two_sided_spectral_window",
                "resolved": verified,
                "resolution": (
                    "Rank controls the low tail and the exact frame second moment "
                    "controls the high tail."
                ),
            },
            {
                "obligation": "constant_condition_constant_success_subspace",
                "resolved": verified,
                "resolution": (
                    "Fixed alpha,beta retain bounded correct probability and make "
                    "the rescaled frame condition number beta/alpha."
                ),
            },
            {
                "obligation": "structured_spectral_window_projector_circuit",
                "resolved": False,
                "resolution": (
                    "No coherent predicate on multiplicity labels identifies the "
                    "window without factorial raw-frame resolution."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Typical multiplicity conditioning must diverge with n.",
                "resolved": True,
                "resolution": (
                    "A fixed rescaled window with condition beta/alpha retains constant "
                    "average decoding success for every n."
                ),
            },
            {
                "objection": "Existence of the window makes it measurable efficiently.",
                "resolved": False,
                "resolution": (
                    "Its raw endpoints remain Theta(1/n!), where generic polynomial "
                    "and indexed-projector query methods are superpolynomial."
                ),
            },
            {
                "objection": "The window must retain every source branch.",
                "resolved": False,
                "resolution": (
                    "The theorem is natural-average. Rare or adversarial branches may "
                    "be almost entirely discarded."
                ),
            },
            {
                "objection": "A constant 4,000,000 condition number is practical.",
                "resolved": False,
                "resolution": (
                    "Only asymptotic polynomiality matters here; constants can be "
                    "optimized after a structured window circuit exists."
                ),
            },
        ],
        headline_metrics={
            "two_sided_spectral_window_theorem_count": 1,
            "constant_condition_constant_success_theorem_count": 1,
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "scaling_record_count": len(scaling),
            "retained_condition_number_upper_bound": (
                scaling[0].retained_condition_number_upper_bound
            ),
            "minimum_windowed_pgm_success_lower_bound": min(
                row.windowed_pgm_success_lower_bound for row in scaling
            ),
            "maximum_discarded_mass_upper_bound": max(
                row.discarded_mass_upper_bound for row in scaling
            ),
            "structured_window_projector_circuit_count": 0,
            "polynomial_covariant_pgm_circuit_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "constant_condition_constant_success_subspace_proved": verified,
            "minimum_eigenvalue_or_growing_condition_number_is_core_barrier": False,
            "structured_window_projector_circuit_proved": False,
            "normalization_one_generic_filter_polynomial": False,
            "polynomial_covariant_pgm_circuit_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "A fixed-condition rescaled spectral window retains constant PGM "
                "success. The sole unresolved step is exposing that window through "
                "efficient representation/multiplicity structure."
            ),
        },
        status=(
            "constant-condition-pgm-window-proved-structured-projector-open"
            if verified
            else "pgm-spectral-window-validation-failure"
        ),
        summary=(
            "Proved an all-n constant-condition spectral subspace retaining constant "
            "PGM correct probability."
        ),
        falsifiers_triggered=[
            (
                "Neither the minimum frame eigenvalue nor an asymptotically growing "
                "condition number is necessary for constant average success."
            ),
            (
                "The unresolved algorithmic content is now exactly a structured "
                "multiplicity-window projector or equivalently rescaled frame access."
            ),
            (
                "Raw spectral filtering remains closed despite the well-conditioned "
                "retained subspace."
            ),
        ],
    )


def write_pgm_spectral_window_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_pgm_spectral_window())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_pgm_spectral_window_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
