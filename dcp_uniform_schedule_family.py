"""Uniform DCP block-schedule family search across unseen modulus sizes."""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

from dcp_sample_workbench import run_dcp_sieve_trial
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


DCP_UNIFORM_SCHEDULE_PATH = Path("research/phase_workbench/dcp_uniform_schedule_family.json")
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-UNIFORM-SCHEDULE-FAMILY"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class UniformSchedulePoint:
    split: str
    n_bits: int
    rule: str
    block_scale: float
    schedule: list[int]
    sample_count: int
    trial_count: int
    generated_success_count: int
    generated_success_rate: float
    mean_generated_targets: float
    mean_target_opportunities: float
    no_opportunity_count: int
    evaluator_query_count: int


@dataclass(frozen=True)
class UniformScheduleFamilyRecord:
    rule: str
    selected_block_scale: float
    default_block_scale: float
    training_points: list[UniformSchedulePoint]
    unseen_size_points: list[UniformSchedulePoint]
    unseen_default_points: list[UniformSchedulePoint]
    mean_unseen_success_improvement: float
    unseen_size_improvement_count: int
    unseen_size_regression_count: int
    uniform_formula: str
    asymptotic_class_changed: bool
    status: str


@dataclass(frozen=True)
class DCPUniformScheduleReport:
    created_at: str
    theorem_contract_id: str
    records: list[UniformScheduleFamilyRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def block_schedule(n_bits: int, block_scale: float) -> tuple[int, ...]:
    if n_bits < 4 or block_scale <= 0:
        raise ValueError("require n_bits >= 4 and positive block_scale")
    target = n_bits - 1
    block = max(1, int(math.ceil(block_scale * math.sqrt(n_bits))))
    schedule = list(range(block, target + 1, block))
    if not schedule or schedule[-1] != target:
        schedule.append(target)
    return tuple(schedule)


def _evaluate_point(
    split: str,
    n_bits: int,
    rule: str,
    block_scale: float,
    budget_multiplier: float,
    trial_count: int,
    seed_start: int,
) -> UniformSchedulePoint:
    schedule = block_schedule(n_bits, block_scale)
    sample_count = 1 << int(math.ceil(budget_multiplier * math.sqrt(n_bits)))
    trials = [
        run_dcp_sieve_trial(
            n_bits=n_bits,
            sample_count=sample_count,
            rule=rule,
            schedule=schedule,
            seed=seed_start + 10007 * index,
        )
        for index in range(trial_count)
    ]
    generated = [
        max(0, trial.harvested_target_state_count - trial.direct_target_input_count) for trial in trials
    ]
    opportunities = [sum(row.target_capable_pair_count for row in trial.rounds) for trial in trials]
    successes = sum(count > 0 for count in generated)
    return UniformSchedulePoint(
        split=split,
        n_bits=int(n_bits),
        rule=rule,
        block_scale=float(block_scale),
        schedule=list(schedule),
        sample_count=sample_count,
        trial_count=trial_count,
        generated_success_count=successes,
        generated_success_rate=successes / trial_count,
        mean_generated_targets=sum(generated) / trial_count,
        mean_target_opportunities=sum(opportunities) / trial_count,
        no_opportunity_count=sum(count == 0 for count in opportunities),
        evaluator_query_count=sum(trial.evaluator_query_count for trial in trials),
    )


def search_uniform_schedule_family(
    rule: str,
    train_n_values: Sequence[int],
    unseen_n_values: Sequence[int],
    block_scales: Sequence[float],
    budget_multiplier: float,
    train_trials: int,
    unseen_trials: int,
    seed: int,
) -> UniformScheduleFamilyRecord:
    by_scale: dict[float, list[UniformSchedulePoint]] = {}
    for scale_index, scale in enumerate(block_scales):
        by_scale[float(scale)] = [
            _evaluate_point(
                "train",
                n_bits,
                rule,
                float(scale),
                budget_multiplier,
                train_trials,
                seed + 1_000_003 * n_index + 1009 * scale_index,
            )
            for n_index, n_bits in enumerate(train_n_values)
        ]

    def training_objective(scale: float) -> tuple[float, float, float]:
        points = by_scale[scale]
        return (
            sum(point.generated_success_rate for point in points) / len(points),
            sum(math.log2(1.0 + point.mean_generated_targets) for point in points) / len(points),
            -scale,
        )

    selected = max(by_scale, key=training_objective)
    unseen_seed = seed + 100_000_007
    selected_points = [
        _evaluate_point(
            "unseen-size",
            n_bits,
            rule,
            selected,
            budget_multiplier,
            unseen_trials,
            unseen_seed + 1_000_003 * index,
        )
        for index, n_bits in enumerate(unseen_n_values)
    ]
    default_points = [
        _evaluate_point(
            "unseen-size-default",
            n_bits,
            rule,
            1.0,
            budget_multiplier,
            unseen_trials,
            unseen_seed + 1_000_003 * index,
        )
        for index, n_bits in enumerate(unseen_n_values)
    ]
    improvements = [
        selected_point.generated_success_rate - default_point.generated_success_rate
        for selected_point, default_point in zip(selected_points, default_points)
    ]
    positive = sum(value > 0 for value in improvements)
    regressions = sum(value < 0 for value in improvements)
    mean_improvement = sum(improvements) / len(improvements)
    return UniformScheduleFamilyRecord(
        rule=rule,
        selected_block_scale=selected,
        default_block_scale=1.0,
        training_points=by_scale[selected],
        unseen_size_points=selected_points,
        unseen_default_points=default_points,
        mean_unseen_success_improvement=mean_improvement,
        unseen_size_improvement_count=positive,
        unseen_size_regression_count=regressions,
        uniform_formula="b_j(n)=min(n-1, j*ceil(c*sqrt(n))) with the terminal n-1 bucket appended",
        asymptotic_class_changed=False,
        status=(
            "uniform-constant-improves-finite-unseen-sizes"
            if mean_improvement > 0 and positive > regressions
            else "uniform-constant-does-not-generalize"
        ),
    )


def run_dcp_uniform_schedule_report(
    train_n_values: Sequence[int] = (20, 24, 28),
    unseen_n_values: Sequence[int] = (32, 36, 40),
    block_scales: Sequence[float] = (0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5),
    rules: Sequence[str] = (
        "randomized-equal-residue-difference",
        "opposite-residue-sum",
    ),
    budget_multiplier: float = 2.0,
    train_trials: int = 12,
    unseen_trials: int = 64,
    seed: int = 0,
) -> DCPUniformScheduleReport:
    records = [
        search_uniform_schedule_family(
            rule,
            train_n_values,
            unseen_n_values,
            block_scales,
            budget_multiplier,
            train_trials,
            unseen_trials,
            seed + 1009 * index,
        )
        for index, rule in enumerate(rules)
    ]
    metrics: dict[str, int | float] = {
        "rule_count": len(records),
        "block_scale_candidate_count": len(block_scales),
        "training_size_count": len(train_n_values),
        "unseen_size_count": len(unseen_n_values),
        "training_trial_count": len(rules) * len(block_scales) * len(train_n_values) * train_trials,
        "unseen_trial_count": len(rules) * len(unseen_n_values) * unseen_trials * 2,
        "positive_mean_unseen_improvement_count": sum(record.mean_unseen_success_improvement > 0 for record in records),
        "asymptotic_class_change_count": sum(record.asymptotic_class_changed for record in records),
        "max_mean_unseen_success_improvement": max(
            (record.mean_unseen_success_improvement for record in records), default=0.0
        ),
        "evaluator_query_count": sum(
            point.evaluator_query_count
            for record in records
            for point in record.training_points + record.unseen_size_points + record.unseen_default_points
        ),
    }
    falsifiers = [
        "The grammar only tunes the constant multiplying sqrt(log N); it cannot change the generic subexponential class.",
        "Unseen-size success at one sample frontier does not prove a uniform endpoint lower bound.",
        "Any constant improvement must still include recursive failure, time, memory, and lattice composition costs.",
    ]
    claim_gate = {
        "single_uniform_schedule_grammar": True,
        "unseen_modulus_sizes_tested": True,
        "state_access_contract_preserved": metrics["evaluator_query_count"] == 0,
        "uniform_recurrence_proved": False,
        "asymptotic_class_changed": False,
        "speedup_claim_allowed": False,
        "reason": "The searched grammar can tune constants only and has no symbolic occupancy/failure proof.",
    }
    summary = (
        f"Selected one block-scale constant per rule on {len(train_n_values)} training sizes and tested "
        f"{len(unseen_n_values)} unseen sizes. {int(metrics['positive_mean_unseen_improvement_count'])} rule(s) had "
        "positive mean finite-size improvement, but zero changed the 2^O(sqrt(log N)) asymptotic class."
    )
    return DCPUniformScheduleReport(
        created_at=utc_now(),
        theorem_contract_id="THM-REGEV-USVP-TO-DCP-2003",
        records=records,
        headline_metrics=metrics,
        claim_gate=claim_gate,
        status="uniform-schedule-constant-search-proof-debt",
        summary=summary,
        falsifiers_triggered=falsifiers,
    )


def write_dcp_uniform_schedule_report(
    path: Path = DCP_UNIFORM_SCHEDULE_PATH,
    train_n_values: Sequence[int] = (20, 24, 28),
    unseen_n_values: Sequence[int] = (32, 36, 40),
    train_trials: int = 12,
    unseen_trials: int = 64,
    seed: int = 0,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    report = run_dcp_uniform_schedule_report(
        train_n_values=train_n_values,
        unseen_n_values=unseen_n_values,
        train_trials=train_trials,
        unseen_trials=unseen_trials,
        seed=seed,
    )
    payload = asdict(report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-BLOCK-SCALE-TUNING-NOT-ASYMPTOTIC-ADVANCE",
                source=str(path),
                claim="Tuning the constant in a Kuperberg-style sqrt(log N) bucket schedule is a new asymptotic algorithm.",
                reason_invalid="Every searched schedule remains in the same 2^O(sqrt(log N)) grammar and has no proved recurrence.",
                lesson="Use constant tuning to strengthen the baseline; require a new recurrence class for breakthrough evidence.",
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence=payload["headline_metrics"],
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-DCP-UNIFORM-SCHEDULE"
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
                artifacts={"dcp_uniform_schedule_family": str(path)},
            )
        )
    return payload
