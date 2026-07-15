"""Random-label local-quadrature DCP decoder and exponential FFT baseline."""

from __future__ import annotations

import json
import math
import random
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

import numpy as np

from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


DCP_RANDOM_DESIGN_DECODER_PATH = Path("research/classical_baselines/dcp_random_design_decoder.json")
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-RANDOM-DESIGN-DECODER"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class RandomDesignTrial:
    n_bits: int
    modulus: int
    sample_count: int
    sample_multiplier: float
    hidden_reflection: int
    fft_decoded_reflection: int
    fft_success: bool
    true_frequency_rank: int
    true_frequency_score: float
    maximum_false_frequency_score: float
    score_margin: float
    polynomial_random_candidate_budget: int
    polynomial_random_candidate_success: bool
    local_quantum_measurement_count: int
    fft_time_proxy: int
    fft_memory_proxy: int
    evaluator_query_count: int


@dataclass(frozen=True)
class RandomDesignScalingRow:
    n_bits: int
    modulus: int
    sample_count: int
    sample_multiplier: float
    trial_count: int
    fft_success_count: int
    mean_true_frequency_rank: float
    mean_score_margin: float
    polynomial_random_candidate_success_count: int
    fft_time_proxy: int
    fft_memory_proxy: int
    log2_fft_time_over_n: float
    local_measurement_only: bool


@dataclass(frozen=True)
class DCPRandomDesignDecoderReport:
    created_at: str
    access_contract: dict[str, str]
    rows: list[RandomDesignScalingRow]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def generate_local_quadrature_samples(
    n_bits: int,
    hidden_reflection: int,
    sample_count: int,
    seed: int,
) -> list[tuple[int, str, int]]:
    if n_bits < 2 or sample_count < 1:
        raise ValueError("require n_bits >= 2 and a positive sample count")
    modulus = 1 << n_bits
    hidden_reflection %= modulus
    rng = random.Random(seed)
    samples = []
    for _ in range(sample_count):
        label = rng.randrange(modulus)
        basis = "X" if rng.randrange(2) == 0 else "Y"
        theta = 2.0 * math.pi * ((label * hidden_reflection) % modulus) / modulus
        expectation = math.cos(theta) if basis == "X" else math.sin(theta)
        outcome = 1 if rng.random() < 0.5 * (1.0 + expectation) else -1
        samples.append((label, basis, outcome))
    return samples


def quadrature_frequency_scores(samples: Sequence[tuple[int, str, int]], modulus: int) -> np.ndarray:
    observations = np.zeros(modulus, dtype=np.complex128)
    for label, basis, outcome in samples:
        # Random basis choice makes this an unbiased estimate of exp(+i theta).
        observations[int(label) % modulus] += 2.0 * outcome if basis == "X" else 2.0j * outcome
    return np.abs(np.fft.fft(observations))


def run_random_design_trial(
    n_bits: int,
    sample_multiplier: float,
    seed: int,
    hidden_reflection: int | None = None,
) -> RandomDesignTrial:
    if sample_multiplier <= 0.0:
        raise ValueError("sample_multiplier must be positive")
    modulus = 1 << n_bits
    rng = random.Random(seed + 37)
    reflection = rng.randrange(modulus) if hidden_reflection is None else hidden_reflection % modulus
    sample_count = max(1, int(math.ceil(sample_multiplier * n_bits)))
    samples = generate_local_quadrature_samples(n_bits, reflection, sample_count, seed)
    scores = quadrature_frequency_scores(samples, modulus)
    decoded = int(np.argmax(scores))
    true_score = float(scores[reflection])
    false_scores = scores.copy()
    false_scores[reflection] = -1.0
    maximum_false = float(np.max(false_scores))
    rank = int(1 + np.count_nonzero(scores > true_score))

    candidate_budget = max(1, n_bits * n_bits)
    candidates = {rng.randrange(modulus) for _ in range(candidate_budget)}
    candidate_success = reflection in candidates
    return RandomDesignTrial(
        n_bits=n_bits,
        modulus=modulus,
        sample_count=sample_count,
        sample_multiplier=sample_multiplier,
        hidden_reflection=reflection,
        fft_decoded_reflection=decoded,
        fft_success=decoded == reflection,
        true_frequency_rank=rank,
        true_frequency_score=true_score,
        maximum_false_frequency_score=maximum_false,
        score_margin=true_score - maximum_false,
        polynomial_random_candidate_budget=candidate_budget,
        polynomial_random_candidate_success=candidate_success,
        local_quantum_measurement_count=sample_count,
        fft_time_proxy=modulus * n_bits,
        fft_memory_proxy=modulus,
        evaluator_query_count=0,
    )


def run_random_design_decoder_report(
    n_values: Sequence[int] = (8, 10, 12, 14, 16),
    sample_multipliers: Sequence[float] = (2.0, 4.0, 8.0, 16.0),
    trials_per_row: int = 24,
    seed: int = 0,
) -> DCPRandomDesignDecoderReport:
    if trials_per_row < 1:
        raise ValueError("trials_per_row must be positive")
    rows: list[RandomDesignScalingRow] = []
    trials: list[RandomDesignTrial] = []
    for n_index, n_bits in enumerate(n_values):
        for multiplier_index, multiplier in enumerate(sample_multipliers):
            trial_rows = [
                run_random_design_trial(
                    n_bits,
                    multiplier,
                    seed + 1_000_003 * n_index + 10_007 * multiplier_index + trial_index,
                )
                for trial_index in range(trials_per_row)
            ]
            trials.extend(trial_rows)
            first = trial_rows[0]
            rows.append(
                RandomDesignScalingRow(
                    n_bits=n_bits,
                    modulus=first.modulus,
                    sample_count=first.sample_count,
                    sample_multiplier=multiplier,
                    trial_count=trials_per_row,
                    fft_success_count=sum(item.fft_success for item in trial_rows),
                    mean_true_frequency_rank=sum(item.true_frequency_rank for item in trial_rows) / trials_per_row,
                    mean_score_margin=sum(item.score_margin for item in trial_rows) / trials_per_row,
                    polynomial_random_candidate_success_count=sum(
                        item.polynomial_random_candidate_success for item in trial_rows
                    ),
                    fft_time_proxy=first.fft_time_proxy,
                    fft_memory_proxy=first.fft_memory_proxy,
                    log2_fft_time_over_n=math.log2(first.fft_time_proxy) / n_bits,
                    local_measurement_only=True,
                )
            )

    successful_rows = [row for row in rows if row.fft_success_count >= math.ceil(0.75 * row.trial_count)]
    metrics: dict[str, int | float] = {
        "scaling_row_count": len(rows),
        "trial_count": len(trials),
        "local_quantum_measurement_count": sum(item.local_quantum_measurement_count for item in trials),
        "fft_success_count": sum(item.fft_success for item in trials),
        "high_success_fft_row_count": len(successful_rows),
        "minimum_multiplier_with_high_success": min(
            (row.sample_multiplier for row in successful_rows), default=-1.0
        ),
        "polynomial_random_candidate_success_count": sum(
            item.polynomial_random_candidate_success for item in trials
        ),
        "maximum_fft_time_proxy": max((item.fft_time_proxy for item in trials), default=0),
        "maximum_fft_memory_proxy": max((item.fft_memory_proxy for item in trials), default=0),
        "evaluator_query_count": sum(item.evaluator_query_count for item in trials),
        "proved_polynomial_time_decoder_count": 0,
        "proved_dcp_decoder_count": 0,
    }
    falsifiers = [
        "Polynomially many local X/Y measurements can make the hidden reflection the largest Fourier score, but the full FFT costs Theta(N log N) time and Theta(N) memory.",
        "Testing only polynomially many random candidate frequencies almost never includes the hidden reflection.",
        "Chosen-frequency sparse Fourier access is unavailable because DCP supplies random public labels and repeated labels are exponentially rare.",
        "A finite FFT success curve is not a polynomial-time DCP decoder or a lattice algorithm."
    ]
    claim_gate = {
        "state_sample_native": True,
        "local_measurements_only": True,
        "evaluator_queries_used": False,
        "polynomial_sample_recovery_observed": bool(successful_rows),
        "fft_time_polynomial_in_log_n": False,
        "fft_memory_polynomial_in_log_n": False,
        "polynomial_time_decoder_proved": False,
        "speedup_claim_allowed": False,
        "reason": (
            "The baseline isolates an information-versus-computation gap: random-label quadrature samples can identify a "
            "Fourier peak with exhaustive FFT resources, but no poly(log N)-time decoder is known."
        ),
    }
    summary = (
        f"Ran {len(trials)} random-design local-quadrature trials using polynomially many DCP states. The full length-N "
        f"FFT succeeded in {int(metrics['fft_success_count'])} trials and polynomial random candidate testing in "
        f"{int(metrics['polynomial_random_candidate_success_count'])}; zero polynomial-time decoders were proved."
    )
    return DCPRandomDesignDecoderReport(
        created_at=utc_now(),
        access_contract={
            "input": "independent DCP phase qubits with random public Fourier labels",
            "measurement": "independent uniformly random X/Y basis measurement",
            "classical_record": "(label, basis, outcome) with E[2 z] or E[2 i z] equal to one phase quadrature",
            "illegal_shortcut": "chosen labels, repeated-label tomography, coherent evaluator, or hidden-reflection verification",
        },
        rows=rows,
        headline_metrics=metrics,
        claim_gate=claim_gate,
        status="polynomial-samples-exponential-decoding-time",
        summary=summary,
        falsifiers_triggered=falsifiers,
    )


def write_random_design_decoder_report(
    path: Path = DCP_RANDOM_DESIGN_DECODER_PATH,
    n_values: Sequence[int] = (8, 10, 12, 14, 16),
    sample_multipliers: Sequence[float] = (2.0, 4.0, 8.0, 16.0),
    trials_per_row: int = 24,
    seed: int = 0,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    report = run_random_design_decoder_report(
        n_values=n_values,
        sample_multipliers=sample_multipliers,
        trials_per_row=trials_per_row,
        seed=seed,
    )
    payload = asdict(report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-RANDOM-DESIGN-POLY-SAMPLES-DO-NOT-IMPLY-POLY-TIME",
                source=str(path),
                claim="Recovering the hidden DCP frequency from O(log N) local measurement records establishes an efficient decoder.",
                reason_invalid=(
                    "The implemented decoder computes a length-N FFT with Theta(N log N) time and Theta(N) memory. "
                    "Polynomial random candidate testing does not locate the hidden frequency."
                ),
                lesson="Track sample and decoding complexity separately; the remaining random-design frequency-search gap is computational.",
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence=payload["headline_metrics"],
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-DCP-RANDOM-DESIGN-DECODER"
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
                artifacts={"dcp_random_design_decoder": str(path)},
            )
        )
    return payload
