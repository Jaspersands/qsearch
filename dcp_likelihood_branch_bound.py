"""Exact nonlinear branch-and-bound baseline for random-label DCP likelihoods."""

from __future__ import annotations

import heapq
import json
import math
import random
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


DCP_LIKELIHOOD_BRANCH_BOUND_PATH = Path("research/classical_baselines/dcp_likelihood_branch_bound.json")
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-LIKELIHOOD-BRANCH-BOUND"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class BranchBoundTrial:
    n_bits: int
    modulus: int
    sample_count: int
    bad_register_count: int
    hidden_reflection: int
    decoded_reflection: int
    exact_decode_success: bool
    unique_score_evaluation_count: int
    score_evaluation_fraction: float
    interval_pop_count: int
    pruned_interval_count: int
    maximum_queue_size: int
    root_saturated_term_fraction: float
    complete_exact_search: bool


@dataclass(frozen=True)
class BranchBoundScalingRow:
    n_bits: int
    modulus: int
    trial_count: int
    sample_count: int
    exact_decode_success_count: int
    mean_score_evaluation_count: float
    mean_score_evaluation_fraction: float
    minimum_score_evaluation_fraction: float
    mean_pruned_interval_count: float
    mean_root_saturated_term_fraction: float
    maximum_queue_size: int


@dataclass(frozen=True)
class DCPLikelihoodBranchBoundReport:
    created_at: str
    decoder_contract: dict[str, str]
    rows: list[BranchBoundScalingRow]
    headline_metrics: dict[str, int | float]
    asymptotic_fit: dict[str, float | str]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def generate_contaminated_quadrature_samples(
    n_bits: int,
    hidden_reflection: int,
    sample_count: int,
    bad_register_rate: float,
    seed: int,
) -> tuple[list[tuple[int, complex]], int]:
    if n_bits < 2 or sample_count < 1:
        raise ValueError("require n_bits >= 2 and positive sample_count")
    if not 0.0 <= bad_register_rate < 1.0:
        raise ValueError("bad_register_rate must lie in [0,1)")
    modulus = 1 << n_bits
    reflection = hidden_reflection % modulus
    rng = random.Random(seed)
    records: list[tuple[int, complex]] = []
    bad_count = 0
    for _ in range(sample_count):
        label = rng.randrange(modulus)
        basis = "X" if rng.randrange(2) == 0 else "Y"
        is_bad = rng.random() < bad_register_rate
        if is_bad:
            # Either computational-basis state is uniform under X/Y measurement.
            outcome = 1 if rng.randrange(2) == 0 else -1
            bad_count += 1
        else:
            theta = 2.0 * math.pi * ((label * reflection) % modulus) / modulus
            expectation = math.cos(theta) if basis == "X" else math.sin(theta)
            outcome = 1 if rng.random() < 0.5 * (1.0 + expectation) else -1
        observation = complex(2.0 * outcome, 0.0) if basis == "X" else complex(0.0, 2.0 * outcome)
        records.append((label, observation))
    return records, bad_count


def likelihood_score(records: Sequence[tuple[int, complex]], modulus: int, candidate: int) -> float:
    angle_scale = -2.0 * math.pi * (candidate % modulus) / modulus
    return sum(
        (observation * complex(math.cos(angle_scale * label), math.sin(angle_scale * label))).real
        for label, observation in records
    )


def interval_score_upper_bound(
    records: Sequence[tuple[int, complex]],
    modulus: int,
    lower: int,
    upper: int,
    center_score: float | None = None,
) -> float:
    """Rigorous Lipschitz upper bound for every integer candidate in [lower, upper]."""
    if not 0 <= lower <= upper < modulus:
        raise ValueError("interval must lie inside [0,N-1]")
    center = (lower + upper) // 2
    score = likelihood_score(records, modulus, center) if center_score is None else center_score
    radius = max(center - lower, upper - center)
    variation = 0.0
    for label, observation in records:
        folded_label = min(label % modulus, (-label) % modulus)
        derivative_bound = abs(observation) * 2.0 * math.pi * folded_label / modulus
        variation += min(2.0 * abs(observation), derivative_bound * radius)
    return score + variation


def exact_branch_bound_decode(
    records: Sequence[tuple[int, complex]],
    modulus: int,
) -> tuple[int, dict[str, int | float | bool]]:
    if modulus < 2 or modulus & (modulus - 1):
        raise ValueError("modulus must be a power of two")
    cache: dict[int, float] = {}

    def score(candidate: int) -> float:
        if candidate not in cache:
            cache[candidate] = likelihood_score(records, modulus, candidate)
        return cache[candidate]

    lower, upper = 0, modulus - 1
    center = (lower + upper) // 2
    center_score = score(center)
    best_candidate = center
    best_score = center_score
    root_bound = interval_score_upper_bound(records, modulus, lower, upper, center_score)
    queue: list[tuple[float, int, int]] = [(-root_bound, lower, upper)]
    popped = 0
    pruned = 0
    max_queue = 1
    tolerance = 1e-12

    while queue:
        negative_bound, lower, upper = heapq.heappop(queue)
        popped += 1
        if -negative_bound <= best_score + tolerance:
            pruned += 1
            continue
        if lower == upper:
            value = score(lower)
            if value > best_score:
                best_score = value
                best_candidate = lower
            continue
        midpoint = (lower + upper) // 2
        for child_lower, child_upper in ((lower, midpoint), (midpoint + 1, upper)):
            child_center = (child_lower + child_upper) // 2
            child_score = score(child_center)
            if child_score > best_score:
                best_score = child_score
                best_candidate = child_center
            bound = interval_score_upper_bound(
                records,
                modulus,
                child_lower,
                child_upper,
                child_score,
            )
            if bound > best_score + tolerance:
                heapq.heappush(queue, (-bound, child_lower, child_upper))
            else:
                pruned += 1
        max_queue = max(max_queue, len(queue))

    root_radius = (modulus - 1) // 2
    saturated = 0
    for label, observation in records:
        folded = min(label % modulus, (-label) % modulus)
        derivative = abs(observation) * 2.0 * math.pi * folded / modulus
        saturated += derivative * root_radius >= 2.0 * abs(observation)
    return best_candidate, {
        "unique_score_evaluation_count": len(cache),
        "interval_pop_count": popped,
        "pruned_interval_count": pruned,
        "maximum_queue_size": max_queue,
        "root_saturated_term_fraction": saturated / max(1, len(records)),
        "complete_exact_search": True,
    }


def run_branch_bound_trial(
    n_bits: int,
    sample_multiplier: float,
    seed: int,
) -> BranchBoundTrial:
    modulus = 1 << n_bits
    rng = random.Random(seed + 71)
    reflection = rng.randrange(modulus)
    sample_count = max(1, math.ceil(sample_multiplier * n_bits))
    records, bad_count = generate_contaminated_quadrature_samples(
        n_bits,
        reflection,
        sample_count,
        bad_register_rate=1.0 / n_bits,
        seed=seed,
    )
    decoded, metrics = exact_branch_bound_decode(records, modulus)
    evaluations = int(metrics["unique_score_evaluation_count"])
    return BranchBoundTrial(
        n_bits=n_bits,
        modulus=modulus,
        sample_count=sample_count,
        bad_register_count=bad_count,
        hidden_reflection=reflection,
        decoded_reflection=decoded,
        exact_decode_success=decoded == reflection,
        unique_score_evaluation_count=evaluations,
        score_evaluation_fraction=evaluations / modulus,
        interval_pop_count=int(metrics["interval_pop_count"]),
        pruned_interval_count=int(metrics["pruned_interval_count"]),
        maximum_queue_size=int(metrics["maximum_queue_size"]),
        root_saturated_term_fraction=float(metrics["root_saturated_term_fraction"]),
        complete_exact_search=bool(metrics["complete_exact_search"]),
    )


def run_likelihood_branch_bound_report(
    n_values: Sequence[int] = (8, 10, 12, 14, 16),
    sample_multiplier: float = 12.0,
    trials_per_size: int = 4,
    seed: int = 0,
) -> DCPLikelihoodBranchBoundReport:
    if trials_per_size < 1 or sample_multiplier <= 0.0:
        raise ValueError("trials_per_size and sample_multiplier must be positive")
    rows: list[BranchBoundScalingRow] = []
    trials: list[BranchBoundTrial] = []
    for n_index, n_bits in enumerate(n_values):
        row_trials = [
            run_branch_bound_trial(
                n_bits,
                sample_multiplier,
                seed + 1_000_003 * n_index + trial_index,
            )
            for trial_index in range(trials_per_size)
        ]
        trials.extend(row_trials)
        rows.append(
            BranchBoundScalingRow(
                n_bits=n_bits,
                modulus=1 << n_bits,
                trial_count=trials_per_size,
                sample_count=row_trials[0].sample_count,
                exact_decode_success_count=sum(item.exact_decode_success for item in row_trials),
                mean_score_evaluation_count=sum(item.unique_score_evaluation_count for item in row_trials)
                / trials_per_size,
                mean_score_evaluation_fraction=sum(item.score_evaluation_fraction for item in row_trials)
                / trials_per_size,
                minimum_score_evaluation_fraction=min(item.score_evaluation_fraction for item in row_trials),
                mean_pruned_interval_count=sum(item.pruned_interval_count for item in row_trials) / trials_per_size,
                mean_root_saturated_term_fraction=sum(item.root_saturated_term_fraction for item in row_trials)
                / trials_per_size,
                maximum_queue_size=max(item.maximum_queue_size for item in row_trials),
            )
        )
    if len(rows) >= 2:
        slope, intercept = np.polyfit(
            [row.n_bits for row in rows],
            [math.log2(max(1.0, row.mean_score_evaluation_count)) for row in rows],
            1,
        )
        exponent_fit = float(slope)
        intercept_fit = float(intercept)
    else:
        exponent_fit = 0.0
        intercept_fit = 0.0
    asymptotically_exponential = exponent_fit >= 0.5
    metrics: dict[str, int | float] = {
        "scaling_row_count": len(rows),
        "trial_count": len(trials),
        "exact_decode_success_count": sum(item.exact_decode_success for item in trials),
        "complete_exact_search_count": sum(item.complete_exact_search for item in trials),
        "maximum_score_evaluation_count": max((item.unique_score_evaluation_count for item in trials), default=0),
        "minimum_score_evaluation_fraction": min((item.score_evaluation_fraction for item in trials), default=0.0),
        "mean_score_evaluation_fraction": sum(item.score_evaluation_fraction for item in trials) / max(1, len(trials)),
        "fitted_log2_evaluation_slope_per_n": exponent_fit,
        "proved_polynomial_branch_bound_count": 0,
        "proved_nonlinear_decoder_lower_bound_count": 0,
    }
    falsifiers = [
        "Random high-frequency labels saturate the separable Lipschitz bound over broad candidate intervals.",
        "Avoiding an N-entry score table does not help when exact search still evaluates an exponential fraction of candidates.",
        "Finite exact recovery under f=1 contamination is information evidence, not polynomial decoding evidence.",
        "This baseline rejects only the implemented interval bound; stronger nonlinear or algebraic global optimization remains open.",
    ]
    return DCPLikelihoodBranchBoundReport(
        created_at=utc_now(),
        decoder_contract={
            "input": "iid random-label quadrature records with computational-basis bad-register rate 1/n",
            "objective": "maximize the exact correlation likelihood over every d in Z_(2^n)",
            "search": "priority branch-and-bound over integer frequency intervals",
            "bound": "center score plus the sum of exact per-term Lipschitz variation caps",
            "correctness": "complete search with a rigorous upper bound; no hidden-reflection verification is used",
        },
        rows=rows,
        headline_metrics=metrics,
        asymptotic_fit={
            "model": "log2(mean unique candidate score evaluations)=slope*n+intercept",
            "slope": exponent_fit,
            "intercept": intercept_fit,
            "classified_exponential": asymptotically_exponential,
        },
        claim_gate={
            "random_label_access_respected": True,
            "exact_search_certified": True,
            "exact_f1_measurement_channel_used": True,
            "polynomial_branch_bound_proved": False,
            "general_nonlinear_lower_bound_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The exact nonlinear decoder preserves access and avoids a score table, but its interval bounds leave "
                "exponentially many candidate evaluations in the observed scaling."
            ),
        },
        status="exact-nonlinear-decoder-observed-exponential-scaling",
        summary=(
            f"Ran {len(trials)} exact branch-and-bound decodes with f=1-rate contamination. Exact reflection recoveries="
            f"{int(metrics['exact_decode_success_count'])}; fitted log2 candidate-evaluation slope={exponent_fit:.4f}; "
            "polynomial branch-and-bound proofs=0."
        ),
        falsifiers_triggered=falsifiers,
    )


def write_likelihood_branch_bound_report(
    path: Path = DCP_LIKELIHOOD_BRANCH_BOUND_PATH,
    n_values: Sequence[int] = (8, 10, 12, 14, 16),
    sample_multiplier: float = 12.0,
    trials_per_size: int = 4,
    seed: int = 0,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    report = run_likelihood_branch_bound_report(n_values, sample_multiplier, trials_per_size, seed)
    payload = asdict(report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-LIKELIHOOD-INTERVAL-BOUND-EXPONENTIAL-SCALING",
                source=str(path),
                claim="A separable Lipschitz branch-and-bound localizes the random-label DCP likelihood in poly(log N) time.",
                reason_invalid=(
                    "Random high-frequency terms saturate broad interval bounds. The exact implementation evaluates an "
                    "exponential candidate set in finite scaling and has no polynomial resource theorem."
                ),
                lesson="Require a nonseparable global certificate or algebraic sketch; removing the N-entry table alone is insufficient.",
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence={
                    "fitted_log2_evaluation_slope_per_n": payload["headline_metrics"][
                        "fitted_log2_evaluation_slope_per_n"
                    ],
                    "proved_general_nonlinear_lower_bound_count": 0,
                },
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-DCP-LIKELIHOOD-BRANCH-BOUND"
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
                artifacts={"dcp_likelihood_branch_bound": str(path)},
            )
        )
    return payload
