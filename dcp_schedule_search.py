"""Held-out search for state-native DCP bucket schedules.

Schedules are selected on training seeds and evaluated once on disjoint holdout
seeds.  The search is a falsification tool for local merge heuristics, not an
asymptotic optimizer or proof.
"""

from __future__ import annotations

import json
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

from dcp_sample_workbench import default_dcp_schedule, run_dcp_sieve_trial
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


DCP_SCHEDULE_SEARCH_PATH = Path("research/phase_workbench/dcp_schedule_search.json")
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-SCHEDULE-SEARCH"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class ScheduleEvaluation:
    n_bits: int
    rule: str
    schedule: list[int]
    split: str
    seed_start: int
    trial_count: int
    sample_count: int
    generated_endpoint_success_count: int
    generated_endpoint_success_rate: float
    mean_generated_target_count: float
    mean_target_capable_pair_count: float
    mean_conditional_predicted_success_rate: float
    no_target_opportunity_count: int
    mean_merge_attempt_count: float
    mean_zero_information_output_count: float
    max_merge_depth: int
    evaluator_query_count: int
    objective_score: float


@dataclass(frozen=True)
class ScheduleSearchRecord:
    n_bits: int
    rule: str
    sample_count: int
    default_schedule: list[int]
    selected_schedule: list[int]
    unique_schedule_count: int
    evaluated_schedule_count: int
    optimizer_trial_count: int
    generation_count: int
    sample_exponent_log2: float
    birthday_exponent_log2: float
    below_birthday_sample_regime: bool
    selected_initial_bucket_bits: int
    selected_initial_bucket_over_sqrt_n: float
    train_evaluation: ScheduleEvaluation
    holdout_evaluation: ScheduleEvaluation
    default_holdout_evaluation: ScheduleEvaluation
    holdout_success_improvement: float
    selection_optimism_gap: float
    heldout_seed_improvement: bool
    confirmation_seed_start: int
    confirmation_trial_count: int
    confirmation_selected_success_rate: float
    confirmation_default_success_rate: float
    confirmation_selected_only_count: int
    confirmation_default_only_count: int
    confirmation_discordant_count: int
    confirmation_unadjusted_p_value: float
    confirmation_adjusted_p_value: float
    statistically_confirmed_improvement: bool
    status: str


@dataclass(frozen=True)
class DCPScheduleSearchReport:
    created_at: str
    theorem_contract_id: str
    records: list[ScheduleSearchRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def normalize_schedule(n_bits: int, schedule: Sequence[int]) -> tuple[int, ...]:
    values = sorted({int(value) for value in schedule if 1 <= int(value) < int(n_bits)})
    if not values:
        values = [int(n_bits) - 1]
    if values[-1] != int(n_bits) - 1:
        values.append(int(n_bits) - 1)
    return tuple(values)


def mutate_schedule(n_bits: int, schedule: Sequence[int], rng: random.Random) -> tuple[int, ...]:
    values = list(normalize_schedule(n_bits, schedule))
    operation = rng.choice(["shift", "insert", "delete", "resample"])
    if operation == "shift" and len(values) > 1:
        index = rng.randrange(len(values) - 1)
        values[index] += rng.choice([-2, -1, 1, 2])
    elif operation == "insert":
        values.append(rng.randrange(1, n_bits))
    elif operation == "delete" and len(values) > 1:
        values.pop(rng.randrange(len(values) - 1))
    elif operation == "resample":
        length = rng.randint(1, min(7, n_bits - 1))
        values = rng.sample(range(1, n_bits), length)
    return normalize_schedule(n_bits, values)


def _evaluate_schedule(
    n_bits: int,
    rule: str,
    schedule: Sequence[int],
    sample_count: int,
    trial_count: int,
    seed_start: int,
    split: str,
) -> ScheduleEvaluation:
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
    predicted = [1.0 - 2.0 ** (-count) for count in opportunities]
    round_rows = [row for trial in trials for row in trial.rounds]
    successes = sum(count > 0 for count in generated)
    success_rate = successes / trial_count
    mean_targets = sum(generated) / trial_count
    mean_opportunities = sum(opportunities) / trial_count
    no_opportunity = sum(count == 0 for count in opportunities)
    mean_attempts = sum(row.pair_count for row in round_rows) / trial_count
    mean_zero = sum(row.zero_information_output_count for row in round_rows) / trial_count
    depth = max((trial.merge_depth for trial in trials), default=0)
    objective = (
        100.0 * success_rate
        + 8.0 * math.log2(1.0 + mean_targets)
        + 2.0 * math.log2(1.0 + mean_opportunities)
        - 4.0 * no_opportunity / trial_count
        - 0.25 * depth
    )
    return ScheduleEvaluation(
        n_bits=int(n_bits),
        rule=rule,
        schedule=list(normalize_schedule(n_bits, schedule)),
        split=split,
        seed_start=int(seed_start),
        trial_count=trial_count,
        sample_count=sample_count,
        generated_endpoint_success_count=successes,
        generated_endpoint_success_rate=success_rate,
        mean_generated_target_count=mean_targets,
        mean_target_capable_pair_count=mean_opportunities,
        mean_conditional_predicted_success_rate=sum(predicted) / trial_count,
        no_target_opportunity_count=no_opportunity,
        mean_merge_attempt_count=mean_attempts,
        mean_zero_information_output_count=mean_zero,
        max_merge_depth=depth,
        evaluator_query_count=sum(trial.evaluator_query_count for trial in trials),
        objective_score=objective,
    )


def _endpoint_success(
    n_bits: int,
    rule: str,
    schedule: Sequence[int],
    sample_count: int,
    seed: int,
) -> bool:
    trial = run_dcp_sieve_trial(
        n_bits=n_bits,
        sample_count=sample_count,
        rule=rule,
        schedule=schedule,
        seed=seed,
    )
    return trial.harvested_target_state_count > trial.direct_target_input_count


def _two_sided_discordant_p_value(selected_only: int, default_only: int) -> float:
    discordant = selected_only + default_only
    if discordant == 0:
        return 1.0
    tail = sum(math.comb(discordant, index) for index in range(min(selected_only, default_only) + 1))
    return min(1.0, 2.0 * tail / (2.0**discordant))


def search_schedule(
    n_bits: int,
    rule: str,
    budget_multiplier: float = 2.0,
    population_size: int = 10,
    generations: int = 6,
    train_trials: int = 8,
    holdout_trials: int = 24,
    confirmation_trials: int = 128,
    multiple_test_count: int = 1,
    seed: int = 0,
) -> ScheduleSearchRecord:
    if population_size < 4 or generations < 1:
        raise ValueError("population_size must be >= 4 and generations must be positive")
    sample_count = 1 << int(math.ceil(float(budget_multiplier) * math.sqrt(n_bits)))
    rng = random.Random(seed)
    default = normalize_schedule(n_bits, default_dcp_schedule(n_bits))
    population = {default}
    while len(population) < population_size:
        population.add(mutate_schedule(n_bits, default, rng))
    cache: dict[tuple[int, ...], ScheduleEvaluation] = {}
    all_schedules = set(population)
    train_seed = seed + 1_000_003
    for _ in range(generations):
        for schedule in population:
            if schedule not in cache:
                cache[schedule] = _evaluate_schedule(
                    n_bits, rule, schedule, sample_count, train_trials, train_seed, "train"
                )
        ranked = sorted(population, key=lambda item: (cache[item].objective_score, item), reverse=True)
        elites = ranked[: max(2, population_size // 3)]
        next_population = set(elites)
        while len(next_population) < population_size:
            next_population.add(mutate_schedule(n_bits, rng.choice(elites), rng))
        population = next_population
        all_schedules.update(population)
    for schedule in population:
        if schedule not in cache:
            cache[schedule] = _evaluate_schedule(
                n_bits, rule, schedule, sample_count, train_trials, train_seed, "train"
            )
    selected = max(cache, key=lambda item: (cache[item].objective_score, item))
    holdout_seed = seed + 100_000_007
    selected_holdout = _evaluate_schedule(
        n_bits, rule, selected, sample_count, holdout_trials, holdout_seed, "holdout"
    )
    default_holdout = _evaluate_schedule(
        n_bits, rule, default, sample_count, holdout_trials, holdout_seed, "holdout-default"
    )
    improvement = (
        selected_holdout.generated_endpoint_success_rate - default_holdout.generated_endpoint_success_rate
    )
    optimism = cache[selected].generated_endpoint_success_rate - selected_holdout.generated_endpoint_success_rate
    sample_exponent = math.log2(sample_count)
    birthday_exponent = n_bits / 2.0
    below_birthday = sample_exponent < birthday_exponent
    heldout_seed_improvement = improvement > 0.0 and optimism <= 0.25 and below_birthday
    confirmation_seed = seed + 200_000_011
    paired = [
        (
            _endpoint_success(n_bits, rule, selected, sample_count, confirmation_seed + 10007 * index),
            _endpoint_success(n_bits, rule, default, sample_count, confirmation_seed + 10007 * index),
        )
        for index in range(confirmation_trials)
    ]
    selected_confirmation_count = sum(selected_success for selected_success, _ in paired)
    default_confirmation_count = sum(default_success for _, default_success in paired)
    selected_only = sum(selected_success and not default_success for selected_success, default_success in paired)
    default_only = sum(default_success and not selected_success for selected_success, default_success in paired)
    unadjusted_p = _two_sided_discordant_p_value(selected_only, default_only)
    adjusted_p = min(1.0, unadjusted_p * max(1, multiple_test_count))
    confirmed = (
        heldout_seed_improvement
        and selected_only > default_only
        and adjusted_p < 0.05
    )
    if improvement > 0.0 and not below_birthday:
        status = "heldout-gain-in-birthday-regime-rejected"
    elif confirmed:
        status = "statistically-confirmed-seed-improvement-proof-debt"
    elif heldout_seed_improvement:
        status = "heldout-improvement-not-confirmed"
    else:
        status = "no-heldout-schedule-improvement"
    return ScheduleSearchRecord(
        n_bits=int(n_bits),
        rule=rule,
        sample_count=sample_count,
        default_schedule=list(default),
        selected_schedule=list(selected),
        unique_schedule_count=len(all_schedules),
        evaluated_schedule_count=len(cache),
        optimizer_trial_count=len(cache) * train_trials,
        generation_count=generations,
        sample_exponent_log2=sample_exponent,
        birthday_exponent_log2=birthday_exponent,
        below_birthday_sample_regime=below_birthday,
        selected_initial_bucket_bits=int(selected[0]),
        selected_initial_bucket_over_sqrt_n=float(selected[0] / math.sqrt(n_bits)),
        train_evaluation=cache[selected],
        holdout_evaluation=selected_holdout,
        default_holdout_evaluation=default_holdout,
        holdout_success_improvement=improvement,
        selection_optimism_gap=optimism,
        heldout_seed_improvement=heldout_seed_improvement,
        confirmation_seed_start=confirmation_seed,
        confirmation_trial_count=confirmation_trials,
        confirmation_selected_success_rate=selected_confirmation_count / confirmation_trials,
        confirmation_default_success_rate=default_confirmation_count / confirmation_trials,
        confirmation_selected_only_count=selected_only,
        confirmation_default_only_count=default_only,
        confirmation_discordant_count=selected_only + default_only,
        confirmation_unadjusted_p_value=unadjusted_p,
        confirmation_adjusted_p_value=adjusted_p,
        statistically_confirmed_improvement=confirmed,
        status=status,
    )


def run_dcp_schedule_search_report(
    n_values: Sequence[int] = (20, 24, 28, 32),
    rules: Sequence[str] = (
        "randomized-equal-residue-difference",
        "opposite-residue-sum",
    ),
    budget_multiplier: float = 2.0,
    population_size: int = 10,
    generations: int = 6,
    train_trials: int = 8,
    holdout_trials: int = 24,
    confirmation_trials: int = 128,
    seed: int = 0,
) -> DCPScheduleSearchReport:
    records = [
        search_schedule(
            n_bits=n_bits,
            rule=rule,
            budget_multiplier=budget_multiplier,
            population_size=population_size,
            generations=generations,
            train_trials=train_trials,
            holdout_trials=holdout_trials,
            confirmation_trials=confirmation_trials,
            multiple_test_count=len(n_values) * len(rules),
            seed=seed + 1_000_003 * n_index + 1009 * rule_index,
        )
        for n_index, n_bits in enumerate(n_values)
        for rule_index, rule in enumerate(rules)
    ]
    heldout_improvements = [record for record in records if record.heldout_seed_improvement]
    confirmed = [record for record in records if record.statistically_confirmed_improvement]
    metrics: dict[str, int | float] = {
        "search_record_count": len(records),
        "unique_schedule_count": sum(record.unique_schedule_count for record in records),
        "evaluated_schedule_count": sum(record.evaluated_schedule_count for record in records),
        "optimizer_trial_count": sum(record.optimizer_trial_count for record in records),
        "selected_train_trial_count": sum(record.train_evaluation.trial_count for record in records),
        "holdout_trial_count": sum(
            record.holdout_evaluation.trial_count + record.default_holdout_evaluation.trial_count
            for record in records
        ),
        "heldout_seed_improvement_count": len(heldout_improvements),
        "statistically_confirmed_improvement_count": len(confirmed),
        "birthday_regime_record_count": sum(not record.below_birthday_sample_regime for record in records),
        "no_confirmed_improvement_count": len(records) - len(confirmed),
        "confirmation_trial_count": sum(record.confirmation_trial_count for record in records),
        "max_holdout_success_improvement": max(
            (record.holdout_success_improvement for record in records), default=0.0
        ),
        "max_selection_optimism_gap": max((record.selection_optimism_gap for record in records), default=0.0),
        "evaluator_query_count": sum(
            record.train_evaluation.evaluator_query_count
            + record.holdout_evaluation.evaluator_query_count
            + record.default_holdout_evaluation.evaluator_query_count
            for record in records
        ),
        "proved_uniform_recurrence_count": 0,
        "proved_asymptotic_improvement_count": 0,
    }
    falsifiers = [
        "Schedule selection and holdout evaluation are finite statistical tests, not a uniform recurrence proof.",
        "A held-out gain at one fixed sample budget may disappear at larger n or under a different resource objective.",
        "No selected schedule is evidence unless it beats named generic sample, time, and memory recurrences.",
    ]
    if metrics["no_confirmed_improvement_count"]:
        falsifiers.append(
            f"{int(metrics['no_confirmed_improvement_count'])} search row(s) lacked a family-wise corrected confirmation gain."
        )
    if metrics["birthday_regime_record_count"]:
        falsifiers.append(
            f"{int(metrics['birthday_regime_record_count'])} row(s) used at least sqrt(N) input states and were ineligible for generalized improvement status."
        )
    claim_gate = {
        "train_holdout_separation_enforced": True,
        "state_access_contract_preserved": metrics["evaluator_query_count"] == 0,
        "at_least_one_heldout_seed_improvement": bool(heldout_improvements),
        "at_least_one_statistically_confirmed_improvement": bool(confirmed),
        "uniform_schedule_family_synthesized": False,
        "uniform_recurrence_proved": False,
        "asymptotic_improvement_proved": False,
        "speedup_claim_allowed": False,
        "reason": "Held-out schedule search cannot replace a uniform stochastic recurrence and named baseline comparison.",
    }
    summary = (
        f"Searched {int(metrics['unique_schedule_count'])} schedule instances across {len(records)} size/rule rows. "
        f"{len(heldout_improvements)} selected schedule(s) improved held-out endpoint success and {len(confirmed)} "
        f"survived an untouched paired confirmation cohort with family-wise correction. No uniform schedule family or "
        "asymptotic recurrence was proved."
    )
    return DCPScheduleSearchReport(
        created_at=utc_now(),
        theorem_contract_id="THM-REGEV-USVP-TO-DCP-2003",
        records=records,
        headline_metrics=metrics,
        claim_gate=claim_gate,
        status="heldout-schedule-search-proof-debt",
        summary=summary,
        falsifiers_triggered=falsifiers,
    )


def write_dcp_schedule_search_report(
    path: Path = DCP_SCHEDULE_SEARCH_PATH,
    n_values: Sequence[int] = (20, 24, 28, 32),
    budget_multiplier: float = 2.0,
    population_size: int = 10,
    generations: int = 6,
    train_trials: int = 8,
    holdout_trials: int = 24,
    confirmation_trials: int = 128,
    seed: int = 0,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    report = run_dcp_schedule_search_report(
        n_values=n_values,
        budget_multiplier=budget_multiplier,
        population_size=population_size,
        generations=generations,
        train_trials=train_trials,
        holdout_trials=holdout_trials,
        confirmation_trials=confirmation_trials,
        seed=seed,
    )
    payload = asdict(report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-SCHEDULE-SELECTION-NOT-ASYMPTOTIC-PROOF",
                source=str(path),
                claim="A schedule selected by finite held-out endpoint success is an improved DHSP algorithm.",
                reason_invalid=(
                    "Train/holdout separation controls seed overfitting only. It does not prove a uniform recurrence, "
                    "bounded recursive failure, or a resource improvement over generic sieves."
                ),
                lesson="Use schedule search to generate recurrence conjectures, then require symbolic proof.",
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence=payload["headline_metrics"],
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-DCP-SCHEDULE-SEARCH"
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
                artifacts={"dcp_schedule_search": str(path)},
            )
        )
    return payload
