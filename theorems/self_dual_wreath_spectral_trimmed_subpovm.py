"""Spectrally trimmed projector sub-POVM with constant recovery success.

Let ``P_s`` be ``M`` equal-rank projectors of rank ``r`` and

    B = M^-1 sum_s P_s,       mu = Tr(B^2)/r.

For any ``c>1``, let ``R`` be the spectral projector of ``B`` onto
eigenvalues at most ``tau=c*mu``.  The effects

    E_s = R P_s R / (M tau)

form a sub-POVM because their sum is ``R B R/tau <= I``.  If
``eta_s=Tr(RP_s)/r``, then the discarded average trace fraction is at most
``1/c`` by the second-moment Markov bound.  Rank Cauchy and Jensen give

    p_correct
      = M^-1 sum_s Tr(E_s P_s/r)
      >= (1-1/c)^2 / (M c mu).

No covariance or spectral-gap assumption is needed for this existence
theorem.  For the ``k``-copy bridge projectors with ``M=n!`` hidden labels,

    mu = (2^k + M - 1)/(M 2^k).

At ``k=ceil(log2 M)`` and ``c=2``, ``M mu <= 2`` and therefore
``p_correct>=1/16``.  Thus the large common-core frame spikes do not cause an
information-theoretic failure: deleting them preserves a constant-success
measurement.

This is not yet an efficient quantum algorithm.  Implementing the low-pass
spectral projector at threshold ``Theta(1/n!)`` without a promised gap, and
compressing ``n!`` measurement outcomes into an efficiently decodable
register, remain the decisive circuit-level barriers.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from coset_natural_multicopy_pgm_benchmark import (
    _source_data,
    _tensor_states,
)
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_spectral_trimmed_subpovm.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-SPECTRAL-TRIMMED-SUBPOVM"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]


@dataclass(frozen=True)
class SpectralTrimControlRecord:
    n: int
    transposition_count: int
    source_partitions: tuple[Partition, ...]
    hidden_label_count: int
    copy_count: int
    carrier_dimension: int
    projector_rank: int
    frame_second_moment_per_rank: float
    clip_multiplier: float
    clip_threshold: float
    clipped_eigenvalue_count: int
    retained_average_trace_fraction: float
    retained_trace_fraction_lower_bound: float
    correct_label_success_probability: float
    correct_label_success_lower_bound: float
    conclusive_probability: float
    maximum_projector_identity_residual: float
    maximum_effect_completeness_violation: float
    correct_success_bound_residual: float
    exact_finite_trimmed_subpovm_validation: bool
    status: str


@dataclass(frozen=True)
class WreathTrimmedScalingRecord:
    n: int
    hidden_label_count_decimal: str
    information_threshold_copy_count: int
    subset_count_decimal: str
    frame_second_moment_per_rank: float
    hidden_count_times_second_moment_scale: float
    clip_multiplier: float
    clip_threshold: float
    retained_average_trace_fraction_lower_bound: float
    correct_label_success_probability_lower_bound: float
    universal_one_sixteenth_bound_verified: bool
    exact_spectral_projector_circuit_known: bool
    polynomial_outcome_transform_known: bool
    status: str


@dataclass(frozen=True)
class SpectralTrimmedSubPOVMReport:
    created_at: str
    theorem_contract: dict[str, str]
    finite_controls: list[SpectralTrimControlRecord]
    scaling_records: list[WreathTrimmedScalingRecord]
    adversarial_audit: list[dict[str, bool | str]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def wreath_frame_second_moment_per_rank(
    hidden_label_count: int,
    copy_count: int,
) -> float:
    if hidden_label_count < 2:
        raise ValueError("hidden_label_count must be at least two")
    if copy_count < 1:
        raise ValueError("copy_count must be positive")
    subset_count = 1 << copy_count
    return (
        subset_count + hidden_label_count - 1
    ) / (hidden_label_count * subset_count)


def trimmed_correct_success_lower_bound(
    hidden_label_count: int,
    frame_second_moment_per_rank: float,
    clip_multiplier: float = 2.0,
) -> float:
    if hidden_label_count < 1:
        raise ValueError("hidden_label_count must be positive")
    if frame_second_moment_per_rank <= 0:
        raise ValueError("second-moment scale must be positive")
    if clip_multiplier <= 1:
        raise ValueError("clip_multiplier must exceed one")
    retained = 1 - 1 / clip_multiplier
    return retained * retained / (
        hidden_label_count
        * clip_multiplier
        * frame_second_moment_per_rank
    )


def _projectors_from_normalized_states(
    states: tuple[np.ndarray, ...],
    tolerance: float,
) -> tuple[tuple[np.ndarray, ...], int, float]:
    if not states:
        raise ValueError("at least one state is required")
    dimension = states[0].shape[0]
    if any(state.shape != (dimension, dimension) for state in states):
        raise ValueError("all states must have the same square shape")
    purities = [float(np.trace(state @ state).real) for state in states]
    if any(purity <= tolerance for purity in purities):
        raise ValueError("state purity must be positive")
    ranks = [round(1 / purity) for purity in purities]
    if len(set(ranks)) != 1:
        raise ValueError("normalized projectors must have equal rank")
    rank = ranks[0]
    projectors = tuple(rank * state for state in states)
    residual = max(
        float(np.linalg.norm(projector @ projector - projector, ord=2))
        for projector in projectors
    )
    trace_residual = max(
        abs(float(np.trace(state).real) - 1.0) for state in states
    )
    if residual > 100 * tolerance or trace_residual > 100 * tolerance:
        raise ValueError("states are not normalized equal-rank projectors")
    return projectors, rank, max(residual, trace_residual)


def audit_spectral_trimmed_subpovm(
    states: tuple[np.ndarray, ...],
    *,
    n: int,
    transposition_count: int,
    source_partitions: tuple[Partition, ...],
    clip_multiplier: float = 2.0,
    tolerance: float = 1e-10,
) -> SpectralTrimControlRecord:
    """Construct the finite clipped effects and verify the theorem."""

    if clip_multiplier <= 1:
        raise ValueError("clip_multiplier must exceed one")
    projectors, rank, projector_residual = (
        _projectors_from_normalized_states(states, tolerance)
    )
    hidden_count = len(states)
    frame = sum(projectors) / hidden_count
    second_scale = float(np.trace(frame @ frame).real / rank)
    threshold = clip_multiplier * second_scale
    eigenvalues, eigenvectors = np.linalg.eigh(frame)
    retained = eigenvalues <= threshold + tolerance
    low_projector = (
        eigenvectors[:, retained]
        @ eigenvectors[:, retained].conj().T
    )
    effects = tuple(
        low_projector @ projector @ low_projector
        / (hidden_count * threshold)
        for projector in projectors
    )
    effect_sum = sum(effects)
    completeness_violation = max(
        0.0,
        float(np.linalg.eigvalsh(effect_sum - np.eye(frame.shape[0]))[-1]),
    )
    signal = np.asarray(
        [
            [
                float(np.trace(effect @ state).real)
                for effect in effects
            ]
            for state in states
        ]
    )
    correct = float(np.trace(signal) / hidden_count)
    conclusive = float(signal.sum(axis=1).mean())
    retained_fraction = float(
        np.trace(low_projector @ frame).real / rank
    )
    retained_lower = 1 - 1 / clip_multiplier
    success_lower = trimmed_correct_success_lower_bound(
        hidden_count,
        second_scale,
        clip_multiplier,
    )
    bound_residual = max(0.0, success_lower - correct)
    verified = (
        projector_residual <= 100 * tolerance
        and completeness_violation <= 100 * tolerance
        and retained_fraction + 100 * tolerance >= retained_lower
        and bound_residual <= 100 * tolerance
    )
    return SpectralTrimControlRecord(
        n=n,
        transposition_count=transposition_count,
        source_partitions=source_partitions,
        hidden_label_count=hidden_count,
        copy_count=len(source_partitions),
        carrier_dimension=frame.shape[0],
        projector_rank=rank,
        frame_second_moment_per_rank=second_scale,
        clip_multiplier=clip_multiplier,
        clip_threshold=threshold,
        clipped_eigenvalue_count=int(np.sum(~retained)),
        retained_average_trace_fraction=retained_fraction,
        retained_trace_fraction_lower_bound=retained_lower,
        correct_label_success_probability=correct,
        correct_label_success_lower_bound=success_lower,
        conclusive_probability=conclusive,
        maximum_projector_identity_residual=projector_residual,
        maximum_effect_completeness_violation=completeness_violation,
        correct_success_bound_residual=bound_residual,
        exact_finite_trimmed_subpovm_validation=verified,
        status=(
            "exact-spectral-trimmed-subpovm-validation"
            if verified
            else "spectral-trimmed-subpovm-validation-failure"
        ),
    )


def finite_trim_control(
    n: int,
    transposition_count: int,
    source_partitions: tuple[Partition, ...],
    clip_multiplier: float = 2.0,
) -> SpectralTrimControlRecord:
    partitions, _, state_families = _source_data(n, transposition_count)
    by_partition = dict(zip(partitions, state_families))
    if any(partition not in by_partition for partition in source_partitions):
        raise ValueError("requested source partition has zero natural mass")
    states = _tensor_states(
        tuple(by_partition[partition] for partition in source_partitions)
    )
    return audit_spectral_trimmed_subpovm(
        states,
        n=n,
        transposition_count=transposition_count,
        source_partitions=source_partitions,
        clip_multiplier=clip_multiplier,
    )


def wreath_trimmed_scaling_record(
    n: int,
    clip_multiplier: float = 2.0,
) -> WreathTrimmedScalingRecord:
    if n < 2:
        raise ValueError("n must be at least two")
    hidden_count = math.factorial(n)
    copies = math.ceil(math.log2(hidden_count))
    subset_count = 1 << copies
    second_scale = wreath_frame_second_moment_per_rank(
        hidden_count,
        copies,
    )
    lower = trimmed_correct_success_lower_bound(
        hidden_count,
        second_scale,
        clip_multiplier,
    )
    return WreathTrimmedScalingRecord(
        n=n,
        hidden_label_count_decimal=str(hidden_count),
        information_threshold_copy_count=copies,
        subset_count_decimal=str(subset_count),
        frame_second_moment_per_rank=second_scale,
        hidden_count_times_second_moment_scale=hidden_count * second_scale,
        clip_multiplier=clip_multiplier,
        clip_threshold=clip_multiplier * second_scale,
        retained_average_trace_fraction_lower_bound=(
            1 - 1 / clip_multiplier
        ),
        correct_label_success_probability_lower_bound=lower,
        universal_one_sixteenth_bound_verified=lower >= 1 / 16,
        exact_spectral_projector_circuit_known=False,
        polynomial_outcome_transform_known=False,
        status=(
            "constant-information-theoretic-recovery-circuit-open"
        ),
    )


def run_spectral_trimmed_subpovm() -> SpectralTrimmedSubPOVMReport:
    finite_controls = [
        finite_trim_control(5, 2, ((3, 1, 1), (3, 1, 1))),
        finite_trim_control(5, 2, ((4, 1), (2, 1, 1, 1))),
        finite_trim_control(5, 2, ((3, 2), (3, 1, 1))),
    ]
    scaling = [
        wreath_trimmed_scaling_record(n)
        for n in (3, 4, 5, 6, 8, 10, 16, 24, 32, 48, 64, 96, 128)
    ]
    validation_failures = sum(
        not record.exact_finite_trimmed_subpovm_validation
        for record in finite_controls
    )
    metrics: dict[str, int | float] = {
        "spectral_trimmed_subpovm_theorem_count": 1,
        "rank_cauchy_correct_success_theorem_count": 1,
        "finite_trimmed_subpovm_control_count": len(finite_controls),
        "finite_trimmed_subpovm_validation_failure_count": validation_failures,
        "finite_control_with_nonempty_clipped_spectrum_count": sum(
            record.clipped_eigenvalue_count > 0
            for record in finite_controls
        ),
        "maximum_effect_completeness_violation": max(
            record.maximum_effect_completeness_violation
            for record in finite_controls
        ),
        "maximum_correct_success_bound_residual": max(
            record.correct_success_bound_residual
            for record in finite_controls
        ),
        "minimum_finite_retained_trace_fraction": min(
            record.retained_average_trace_fraction
            for record in finite_controls
        ),
        "minimum_finite_correct_label_success_probability": min(
            record.correct_label_success_probability
            for record in finite_controls
        ),
        "information_threshold_scaling_record_count": len(scaling),
        "universal_one_sixteenth_scaling_row_count": sum(
            record.universal_one_sixteenth_bound_verified
            for record in scaling
        ),
        "minimum_scaling_correct_success_lower_bound": min(
            record.correct_label_success_probability_lower_bound
            for record in scaling
        ),
        "tail_n": scaling[-1].n,
        "tail_hidden_count_times_second_moment_scale": (
            scaling[-1].hidden_count_times_second_moment_scale
        ),
        "tail_correct_label_success_lower_bound": (
            scaling[-1].correct_label_success_probability_lower_bound
        ),
        "exact_spectral_projector_circuit_count": 0,
        "polynomial_outcome_transform_count": 0,
        "polynomial_hidden_permutation_decoder_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    theorem_verified = validation_failures == 0
    return SpectralTrimmedSubPOVMReport(
        created_at=utc_now(),
        theorem_contract={
            "projector_ensemble": (
                "P_s are M equal-rank-r projectors and "
                "B=M^-1 sum_s P_s."
            ),
            "low_spectrum_projector": (
                "For mu=Tr(B^2)/r, R=1[B<=c mu] with c>1."
            ),
            "valid_effects": (
                "E_s=R P_s R/(M c mu), so sum_s E_s=RBR/(c mu)<=I."
            ),
            "retained_trace": (
                "The average discarded projector trace is at most 1/c by "
                "Tr(1[B>c mu]B)<=Tr(B^2)/(c mu)."
            ),
            "correct_success": (
                "Rank Cauchy followed by Jensen gives average exact-label "
                "success at least (1-1/c)^2/(M c mu); covariance is not used."
            ),
            "wreath_specialization": (
                "For bridge projectors, mu=(2^k+M-1)/(M2^k). At "
                "k=ceil(log2 M), c=2 gives success at least 1/16."
            ),
            "implementation_boundary": (
                "The existence proof requires a sharp spectral low-pass at "
                "Theta(1/n!) and n! labeled effects. No polynomial circuit, "
                "gap theorem, outcome compression, or decoder follows."
            ),
        },
        finite_controls=finite_controls,
        scaling_records=scaling,
        adversarial_audit=[
            {
                "objection": (
                    "The block-common-core spike forces every sub-POVM to "
                    "have exponentially small correct-label success."
                ),
                "resolved": True,
                "resolution": (
                    "Discarding eigenvalues above twice the exact second-"
                    "moment scale leaves at least half the average trace and "
                    "provably retains at least 1/16 correct success."
                ),
            },
            {
                "objection": (
                    "Covariance is needed to make retained trace uniform over "
                    "hidden labels."
                ),
                "resolved": True,
                "resolution": (
                    "The theorem bounds average success. Jensen converts the "
                    "average retained trace directly; no per-label equality "
                    "or covariance is required."
                ),
            },
            {
                "objection": (
                    "A sharp spectral projector at a factorially small "
                    "threshold has a known efficient block-encoding circuit."
                ),
                "resolved": False,
                "resolution": (
                    "No gap is known at the cutoff and generic polynomial "
                    "approximation resolves an absolute Theta(1/n!) scale."
                ),
            },
            {
                "objection": (
                    "An information-theoretic family of n! effects already "
                    "provides an efficient hidden-permutation decoder."
                ),
                "resolved": False,
                "resolution": (
                    "Outcome synthesis, compressed labeling, and classical "
                    "decoding remain unconstructed and may be factorial."
                ),
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "spectral_trimmed_subpovm_theorem_proved": theorem_verified,
            "constant_information_theoretic_correct_success_at_threshold_proved": (
                theorem_verified
                and all(
                    record.universal_one_sixteenth_bound_verified
                    for record in scaling
                )
            ),
            "large_frame_norm_implies_information_theoretic_failure": False,
            "block_common_core_spikes_can_be_trimmed_with_constant_mass_retained": True,
            "covariance_required_for_average_success_bound": False,
            "exact_spectral_projector_circuit_proved": False,
            "inverse_polynomial_spectral_gap_proved": False,
            "polynomial_outcome_transform_proved": False,
            "polynomial_hidden_permutation_decoder_proved": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "A constant-success exact-label measurement exists after "
                "spectral trimming, so common-core spikes are not an "
                "information-theoretic no-go. The required factorial-scale "
                "spectral filter and n!-outcome transform have no efficient "
                "implementation or decoder."
            ),
        },
        status=(
            "constant-information-recovery-spectral-filter-circuit-open"
            if theorem_verified
            else "spectral-trimmed-subpovm-validation-failure"
        ),
        summary=(
            "Proved a generic second-moment spectral-trimming theorem. At the "
            "wreath information threshold it retains exact hidden-label "
            "success at least 1/16 despite the typical common-core norm spike; "
            "efficient spectral filtering and outcome decoding remain open."
        ),
        falsifiers_triggered=[
            (
                "The typical exponential common core kills the uniform norm "
                "normalization, but not information-theoretic recovery after "
                "discarding the high-frame spectrum."
            ),
            (
                "The exact first and second moments suffice for a constant "
                "success lower bound; higher moments are not needed for "
                "information-theoretic existence."
            ),
            (
                "The result does not reduce the absolute spectral cutoff, "
                "measurement-outcome count, or decoding complexity."
            ),
        ],
    )


def write_spectral_trimmed_subpovm_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, Any]:
    payload = asdict(run_spectral_trimmed_subpovm())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-CODE-WREATH-LARGE-NORM-IS-NOT-INFORMATION-NOGO",
                source=str(path),
                claim=(
                    "The typical exponential common-core frame spike makes "
                    "constant-success hidden-permutation recovery "
                    "information-theoretically impossible."
                ),
                reason_invalid=(
                    "A second-moment spectral cutoff removes at most half the "
                    "average trace and yields a valid sub-POVM with exact-label "
                    "success at least 1/16 at k=ceil(log2(n!))."
                ),
                lesson=(
                    "Move the critical path from frame-norm existence to an "
                    "efficient low-spectrum filter, compressed covariant "
                    "outcome transform, and decoder."
                ),
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-MEASUREMENT",
                    "PO-COMPLEXITY",
                    "PO-SUCCESS",
                ],
                evidence=payload["headline_metrics"],
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
                created_at=payload["created_at"],
                status=payload["status"],
                summary=payload["summary"],
                metrics=payload["headline_metrics"],
                falsifiers_triggered=payload["falsifiers_triggered"],
                artifacts={
                    "self_dual_wreath_spectral_trimmed_subpovm": str(path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_spectral_trimmed_subpovm_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
