"""Register-ratio scaling and analytic bounds for Hadamard DCP witnesses."""

from __future__ import annotations

import json
import math
import random
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


DCP_HADAMARD_SCALING_PATH = Path("research/phase_workbench/dcp_hadamard_scaling.json")
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-HADAMARD-SCALING"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"
SUBCRITICAL_REGISTER_RATIO = 1.0 / math.log2(1.5)


@dataclass(frozen=True)
class HadamardHammingInstance:
    n_bits: int
    register_count: int
    register_ratio: float
    label_seed: int
    prior_mixture_hamming_tv: float
    mean_fixed_reflection_hamming_tv: float
    minimum_fixed_reflection_hamming_tv: float
    maximum_fixed_reflection_hamming_tv: float
    log2_shots_for_prior_mixture_bias: float
    all_good_probability_at_f1_rate: float


@dataclass(frozen=True)
class HadamardScalingRow:
    n_bits: int
    register_count: int
    register_ratio: float
    trial_count: int
    mean_prior_mixture_hamming_tv: float
    maximum_prior_mixture_hamming_tv: float
    mean_minimum_fixed_reflection_hamming_tv: float
    mean_fixed_reflection_hamming_tv: float
    mean_log2_shots_for_prior_mixture_bias: float
    mean_all_good_probability_at_f1_rate: float
    analytic_expected_full_tv_upper_bound: float
    analytic_log2_chi_exponent_per_n: float
    analytically_subcritical: bool
    inverse_polynomial_prior_signal_count: int


@dataclass(frozen=True)
class DCPHadamardScalingReport:
    created_at: str
    theorem_contract_id: str
    analytic_certificate: dict[str, str | float]
    rows: list[HadamardScalingRow]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _binomial_distribution(register_count: int) -> list[float]:
    denominator = float(1 << register_count)
    return [math.comb(register_count, weight) / denominator for weight in range(register_count + 1)]


def _fixed_reflection_hamming_distribution(labels: Sequence[int], n_bits: int, reflection: int) -> list[float]:
    modulus = 1 << n_bits
    distribution = [1.0]
    for label in labels:
        cosine = math.cos(2.0 * math.pi * ((int(label) * reflection) % modulus) / modulus)
        probability_one = 0.5 * (1.0 - cosine)
        probability_zero = 1.0 - probability_one
        updated = [0.0] * (len(distribution) + 1)
        for weight, probability in enumerate(distribution):
            updated[weight] += probability * probability_zero
            updated[weight + 1] += probability * probability_one
        distribution = updated
    return distribution


def _total_variation(left: Sequence[float], right: Sequence[float]) -> float:
    return 0.5 * sum(abs(a - b) for a, b in zip(left, right))


def analyze_hadamard_hamming_instance(
    n_bits: int,
    labels: Sequence[int],
    label_seed: int = 0,
) -> HadamardHammingInstance:
    if n_bits < 2 or not labels:
        raise ValueError("require n_bits >= 2 and at least one label")
    modulus = 1 << n_bits
    bad_distribution = _binomial_distribution(len(labels))
    mixture = [0.0] * (len(labels) + 1)
    fixed_tvs = []
    for reflection in range(modulus):
        distribution = _fixed_reflection_hamming_distribution(labels, n_bits, reflection)
        fixed_tvs.append(_total_variation(distribution, bad_distribution))
        for weight, probability in enumerate(distribution):
            mixture[weight] += probability / modulus
    mixture_tv = _total_variation(mixture, bad_distribution)
    log2_shots = (
        -1.0
        if mixture_tv <= 0.0
        else math.log2(2.0 * math.log(6.0)) - 2.0 * math.log2(mixture_tv)
    )
    return HadamardHammingInstance(
        n_bits=n_bits,
        register_count=len(labels),
        register_ratio=len(labels) / n_bits,
        label_seed=label_seed,
        prior_mixture_hamming_tv=mixture_tv,
        mean_fixed_reflection_hamming_tv=sum(fixed_tvs) / len(fixed_tvs),
        minimum_fixed_reflection_hamming_tv=min(fixed_tvs),
        maximum_fixed_reflection_hamming_tv=max(fixed_tvs),
        log2_shots_for_prior_mixture_bias=log2_shots,
        all_good_probability_at_f1_rate=(1.0 - 1.0 / n_bits) ** len(labels),
    )


def analytic_expected_full_tv_upper_bound(n_bits: int, register_count: int) -> float:
    """Average over independent uniform public labels.

    For an XOR support of weight r, dependent sign-pair equations contribute
    at most 2^(r+1)/N and all other equation pairs at most 2/N^2. Parseval and
    TV <= sqrt(chi^2)/2 give the stated bound.
    """

    modulus = float(1 << n_bits)
    chi_bound = 2.0 * ((1.5**register_count) - 1.0) / modulus
    chi_bound += 2.0 * ((2.0**register_count) - 1.0) / (modulus * modulus)
    return min(1.0, 0.5 * math.sqrt(max(0.0, chi_bound)))


def run_hadamard_scaling_report(
    n_values: Sequence[int] = (6, 8, 10, 12),
    register_ratios: Sequence[float] = (0.5, 1.0, 1.5, 2.0),
    trials_per_row: int = 3,
    seed: int = 0,
) -> DCPHadamardScalingReport:
    if trials_per_row < 1:
        raise ValueError("trials_per_row must be positive")
    rows: list[HadamardScalingRow] = []
    instances: list[HadamardHammingInstance] = []
    for n_index, n_bits in enumerate(n_values):
        modulus = 1 << n_bits
        for ratio_index, ratio in enumerate(register_ratios):
            if ratio <= 0.0:
                raise ValueError("register ratios must be positive")
            register_count = max(1, int(math.ceil(ratio * n_bits)))
            trial_instances = []
            for trial_index in range(trials_per_row):
                label_seed = seed + 1_000_003 * n_index + 10_007 * ratio_index + trial_index
                rng = random.Random(label_seed)
                labels = [rng.randrange(modulus) for _ in range(register_count)]
                trial_instances.append(analyze_hadamard_hamming_instance(n_bits, labels, label_seed))
            instances.extend(trial_instances)
            ratio_actual = register_count / n_bits
            rows.append(
                HadamardScalingRow(
                    n_bits=n_bits,
                    register_count=register_count,
                    register_ratio=ratio_actual,
                    trial_count=trials_per_row,
                    mean_prior_mixture_hamming_tv=sum(
                        item.prior_mixture_hamming_tv for item in trial_instances
                    )
                    / trials_per_row,
                    maximum_prior_mixture_hamming_tv=max(
                        item.prior_mixture_hamming_tv for item in trial_instances
                    ),
                    mean_minimum_fixed_reflection_hamming_tv=sum(
                        item.minimum_fixed_reflection_hamming_tv for item in trial_instances
                    )
                    / trials_per_row,
                    mean_fixed_reflection_hamming_tv=sum(
                        item.mean_fixed_reflection_hamming_tv for item in trial_instances
                    )
                    / trials_per_row,
                    mean_log2_shots_for_prior_mixture_bias=sum(
                        item.log2_shots_for_prior_mixture_bias for item in trial_instances
                    )
                    / trials_per_row,
                    mean_all_good_probability_at_f1_rate=sum(
                        item.all_good_probability_at_f1_rate for item in trial_instances
                    )
                    / trials_per_row,
                    analytic_expected_full_tv_upper_bound=analytic_expected_full_tv_upper_bound(
                        n_bits, register_count
                    ),
                    analytic_log2_chi_exponent_per_n=ratio_actual * math.log2(1.5) - 1.0,
                    analytically_subcritical=ratio_actual < SUBCRITICAL_REGISTER_RATIO,
                    inverse_polynomial_prior_signal_count=sum(
                        item.prior_mixture_hamming_tv >= 1.0 / (n_bits * n_bits)
                        for item in trial_instances
                    ),
                )
            )

    supercritical_rows = [row for row in rows if not row.analytically_subcritical]
    metrics: dict[str, int | float] = {
        "scaling_row_count": len(rows),
        "instance_count": len(instances),
        "analytic_subcritical_ratio_threshold": SUBCRITICAL_REGISTER_RATIO,
        "analytically_subcritical_row_count": sum(row.analytically_subcritical for row in rows),
        "supercritical_row_count": len(supercritical_rows),
        "supercritical_inverse_polynomial_signal_row_count": sum(
            row.inverse_polynomial_prior_signal_count > 0 for row in supercritical_rows
        ),
        "maximum_supercritical_mean_hamming_tv": max(
            (row.mean_prior_mixture_hamming_tv for row in supercritical_rows), default=0.0
        ),
        "minimum_supercritical_all_good_probability": min(
            (row.mean_all_good_probability_at_f1_rate for row in supercritical_rows), default=0.0
        ),
        "proved_worst_case_reflection_signal_family_count": 0,
        "proved_f1_robust_decoder_count": 0,
    }
    falsifiers = [
        "For m/n below 1/log2(3/2), the expected full Hadamard-output TV over random labels is exponentially upper bounded; no decoder on those outcomes can evade data processing.",
        "Prior-mixture Hamming TV is average-case over the hidden reflection and does not establish worst-case DCP success.",
        "Supercritical finite signal must include sample cost, arbitrary bad-register contamination, and a full reflection decoder.",
        "The analytic bound is for independent uniform public labels and does not by itself cover every label stream."
    ]
    claim_gate = {
        "subcritical_average_case_no_go_proved": True,
        "supercritical_finite_rows_tested": bool(supercritical_rows),
        "worst_case_reflection_signal_proved": False,
        "full_f1_robustness_proved": False,
        "full_decoder_proved": False,
        "speedup_claim_allowed": False,
        "reason": (
            "Subcritical register ratios are average-case obstructed. Supercritical finite Hamming signals have no "
            "worst-case hidden-reflection theorem, f=1 robustness proof, or decoder."
        ),
    }
    summary = (
        f"Swept {len(rows)} Hadamard register-ratio rows ({len(instances)} label batches). "
        f"{int(metrics['analytically_subcritical_row_count'])} rows lie below the certified average-case threshold "
        f"alpha={SUBCRITICAL_REGISTER_RATIO:.4f}; {int(metrics['supercritical_inverse_polynomial_signal_row_count'])} "
        "supercritical finite rows had an inverse-polynomial prior-mixture Hamming signal, with no worst-case or robust decoder proof."
    )
    return DCPHadamardScalingReport(
        created_at=utc_now(),
        theorem_contract_id="THM-REGEV-USVP-TO-DCP-2003",
        analytic_certificate={
            "label_model": "m independent uniform Fourier labels in Z_(2^n)",
            "chi_square_bound": "E[chi^2] <= 2((3/2)^m-1)/2^n + 2(2^m-1)/2^(2n)",
            "tv_bound": "E[TV] <= (1/2)sqrt(E[chi^2])",
            "subcritical_ratio": SUBCRITICAL_REGISTER_RATIO,
            "scope": "full Hadamard output, hence every classical decoder of that output, averaged over random labels",
        },
        rows=rows,
        headline_metrics=metrics,
        claim_gate=claim_gate,
        status="supercritical-hadamard-signal-proof-debt",
        summary=summary,
        falsifiers_triggered=falsifiers,
    )


def write_hadamard_scaling_report(
    path: Path = DCP_HADAMARD_SCALING_PATH,
    n_values: Sequence[int] = (6, 8, 10, 12),
    register_ratios: Sequence[float] = (0.5, 1.0, 1.5, 2.0),
    trials_per_row: int = 3,
    seed: int = 0,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    report = run_hadamard_scaling_report(
        n_values=n_values,
        register_ratios=register_ratios,
        trials_per_row=trials_per_row,
        seed=seed,
    )
    payload = asdict(report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-HADAMARD-SUBCRITICAL-REGISTER-RATIO-AVERAGE-TV-BOUND",
                source=str(path),
                claim="A Hadamard-output decoder with m below 1.7096 log2(N) phase states has inverse-polynomial average signal.",
                reason_invalid=(
                    "The signed-relation second-moment and Parseval bound makes expected full-output TV exponentially "
                    "small for every fixed register ratio below 1/log2(3/2)."
                ),
                lesson="Do not spend effort tuning decoders in the analytically subcritical regime; test supercritical ratios and exact robustness.",
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence={
                    "subcritical_threshold": SUBCRITICAL_REGISTER_RATIO,
                    "subcritical_rows": payload["headline_metrics"]["analytically_subcritical_row_count"],
                },
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-DCP-HADAMARD-SCALING"
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
                artifacts={"dcp_hadamard_scaling": str(path)},
            )
        )
    return payload
