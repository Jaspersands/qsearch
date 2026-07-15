"""Finite DCP merge-recurrence audit with exact pair kernels.

This module strengthens the generic sieve baseline without turning finite
scaling fits into a theorem.  It verifies the one-pair transition kernel,
searches legal label-only pairing rules, excludes target labels present in the
raw input, and estimates endpoint yields over growing moduli.
"""

from __future__ import annotations

import json
import math
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


DCP_RECURRENCE_PATH = Path("research/phase_workbench/dcp_recurrence_analysis.json")
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-RECURRENCE-SCALING"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class PairKernelCertificate:
    n_bits: int
    modulus: int
    bucket_bits: int
    rule: str
    eligibility_relation: str
    eligible_ordered_label_pairs: int
    possible_desired_output_labels: int
    desired_branch_target_probability: float
    physical_target_probability_per_eligible_pair: float
    desired_branch_zero_probability: float
    exhaustive_pair_count: int
    exhaustive_failure_count: int
    exact_kernel_verified: bool
    scope_limitation: str


@dataclass(frozen=True)
class RecurrenceScalingRow:
    n_bits: int
    modulus: int
    rule: str
    schedule: list[int]
    budget_multiplier_sqrt_n: float
    budget_exponent_log2: int
    sample_count: int
    trial_count: int
    direct_target_input_count: int
    sieve_generated_target_count: int
    sieve_generated_endpoint_success_count: int
    observed_endpoint_success_rate: float
    wilson_success_lower_95: float
    wilson_success_upper_95: float
    mean_generated_targets: float
    mean_target_capable_pairs: float
    mean_exact_conditional_expected_targets: float
    target_yield_over_conditional_expectation: float | None
    no_target_opportunity_trial_count: int
    mean_conditional_no_target_probability: float
    predicted_endpoint_success_rate_from_opportunities: float
    endpoint_success_calibration_residual: float
    mean_merge_attempts: float
    mean_unfavorable_branches: float
    mean_zero_information_outputs: float
    mean_final_active_states: float
    max_merge_depth: int
    evaluator_query_count: int


@dataclass(frozen=True)
class ScalingFit:
    rule: str
    successful_n_count: int
    threshold_points: list[dict[str, int | float]]
    sqrt_n_slope: float | None
    sqrt_n_intercept: float | None
    sqrt_n_r_squared: float | None
    linear_n_slope: float | None
    linear_n_intercept: float | None
    linear_n_r_squared: float | None
    interpretation: str


@dataclass(frozen=True)
class DCPRecurrenceReport:
    created_at: str
    theorem_contract_id: str
    pair_kernel_certificates: list[PairKernelCertificate]
    scaling_rows: list[RecurrenceScalingRow]
    scaling_fits: list[ScalingFit]
    headline_metrics: dict[str, int | float | str]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _rule_relation(rule: str) -> str:
    if rule == "opposite-residue-sum":
        return "k_left + k_right = 0 mod 2^b"
    if rule == "target-complement-difference":
        return "k_left - k_right = N/2 mod N"
    if rule == "nonzero-equal-residue-difference":
        return "k_left = k_right mod 2^b and k_left != k_right mod N"
    return "k_left = k_right mod 2^b"


def _eligible_and_output(left: int, right: int, modulus: int, bucket_bits: int, rule: str) -> tuple[bool, int]:
    bucket_modulus = 1 << int(bucket_bits)
    if rule == "opposite-residue-sum":
        return (left + right) % bucket_modulus == 0, (left + right) % modulus
    if rule == "target-complement-difference":
        output = (left - right) % modulus
        return output == modulus // 2, output
    output = (left - right) % modulus
    eligible = left % bucket_modulus == right % bucket_modulus
    if rule == "nonzero-equal-residue-difference":
        eligible = eligible and left != right
    return eligible, output


def certify_pair_kernel(n_bits: int, bucket_bits: int, rule: str) -> PairKernelCertificate:
    if n_bits < 3 or not 1 <= bucket_bits < n_bits:
        raise ValueError("require n_bits >= 3 and 1 <= bucket_bits < n_bits")
    modulus = 1 << int(n_bits)
    bucket_modulus = 1 << int(bucket_bits)
    quotient = modulus // bucket_modulus
    if rule == "target-complement-difference":
        eligible_formula = modulus
        output_count = 1
        target_desired = 1.0
        zero_desired = 0.0
    elif rule == "nonzero-equal-residue-difference":
        eligible_formula = modulus * (quotient - 1)
        output_count = quotient - 1
        target_desired = 1.0 / output_count
        zero_desired = 0.0
    else:
        eligible_formula = modulus * quotient
        output_count = quotient
        target_desired = 1.0 / output_count
        zero_desired = 1.0 / output_count

    exhaustive_pairs = 0
    target_pairs = 0
    zero_pairs = 0
    failures = 0
    if n_bits <= 9:
        for left in range(modulus):
            for right in range(modulus):
                eligible, output = _eligible_and_output(left, right, modulus, bucket_bits, rule)
                if not eligible:
                    continue
                exhaustive_pairs += 1
                target_pairs += output == modulus // 2
                zero_pairs += output == 0
        if exhaustive_pairs != eligible_formula:
            failures += 1
        if exhaustive_pairs and not math.isclose(target_pairs / exhaustive_pairs, target_desired):
            failures += 1
        if exhaustive_pairs and not math.isclose(zero_pairs / exhaustive_pairs, zero_desired):
            failures += 1

    return PairKernelCertificate(
        n_bits=int(n_bits),
        modulus=modulus,
        bucket_bits=int(bucket_bits),
        rule=rule,
        eligibility_relation=_rule_relation(rule),
        eligible_ordered_label_pairs=eligible_formula,
        possible_desired_output_labels=output_count,
        desired_branch_target_probability=target_desired,
        physical_target_probability_per_eligible_pair=0.5 * target_desired,
        desired_branch_zero_probability=zero_desired,
        exhaustive_pair_count=exhaustive_pairs,
        exhaustive_failure_count=failures,
        exact_kernel_verified=failures == 0,
        scope_limitation=(
            "Exact for one eligible independent label pair. It does not prove bucket occupancy, pair independence, "
            "or endpoint yield after adaptive multi-round depletion."
        ),
    )


def _wilson_interval(successes: int, trials: int, z: float = 1.959963984540054) -> tuple[float, float]:
    if trials <= 0:
        return 0.0, 1.0
    rate = successes / trials
    denominator = 1.0 + z * z / trials
    center = (rate + z * z / (2.0 * trials)) / denominator
    radius = z * math.sqrt(rate * (1.0 - rate) / trials + z * z / (4.0 * trials * trials)) / denominator
    return max(0.0, center - radius), min(1.0, center + radius)


def run_scaling_row(
    n_bits: int,
    rule: str,
    budget_multiplier: float,
    trials: int,
    seed: int,
) -> RecurrenceScalingRow:
    exponent = max(1, int(math.ceil(float(budget_multiplier) * math.sqrt(n_bits))))
    sample_count = 1 << exponent
    trial_rows = [
        run_dcp_sieve_trial(
            n_bits=n_bits,
            sample_count=sample_count,
            rule=rule,
            seed=seed + 10007 * trial_index,
        )
        for trial_index in range(trials)
    ]
    generated_counts = [
        max(0, trial.harvested_target_state_count - trial.direct_target_input_count)
        for trial in trial_rows
    ]
    successes = sum(count > 0 for count in generated_counts)
    lower, upper = _wilson_interval(successes, trials)
    round_rows = [round_row for trial in trial_rows for round_row in trial.rounds]
    per_trial_target_opportunities = [
        sum(round_row.target_capable_pair_count for round_row in trial.rounds) for trial in trial_rows
    ]
    mean_no_target_probability = sum(2.0 ** (-count) for count in per_trial_target_opportunities) / trials
    predicted_success = 1.0 - mean_no_target_probability
    expected_targets = sum(round_row.exact_conditional_expected_targets for round_row in round_rows)
    observed_targets = sum(generated_counts)
    return RecurrenceScalingRow(
        n_bits=int(n_bits),
        modulus=1 << int(n_bits),
        rule=rule,
        schedule=default_dcp_schedule(n_bits),
        budget_multiplier_sqrt_n=float(budget_multiplier),
        budget_exponent_log2=exponent,
        sample_count=sample_count,
        trial_count=trials,
        direct_target_input_count=sum(trial.direct_target_input_count for trial in trial_rows),
        sieve_generated_target_count=sum(generated_counts),
        sieve_generated_endpoint_success_count=successes,
        observed_endpoint_success_rate=successes / trials,
        wilson_success_lower_95=lower,
        wilson_success_upper_95=upper,
        mean_generated_targets=sum(generated_counts) / trials,
        mean_target_capable_pairs=sum(per_trial_target_opportunities) / trials,
        mean_exact_conditional_expected_targets=expected_targets / trials,
        target_yield_over_conditional_expectation=(observed_targets / expected_targets if expected_targets else None),
        no_target_opportunity_trial_count=sum(count == 0 for count in per_trial_target_opportunities),
        mean_conditional_no_target_probability=mean_no_target_probability,
        predicted_endpoint_success_rate_from_opportunities=predicted_success,
        endpoint_success_calibration_residual=successes / trials - predicted_success,
        mean_merge_attempts=sum(row.pair_count for row in round_rows) / trials,
        mean_unfavorable_branches=sum(row.unfavorable_branch_count for row in round_rows) / trials,
        mean_zero_information_outputs=sum(row.zero_information_output_count for row in round_rows) / trials,
        mean_final_active_states=sum(trial.final_active_state_count for trial in trial_rows) / trials,
        max_merge_depth=max((trial.merge_depth for trial in trial_rows), default=0),
        evaluator_query_count=sum(trial.evaluator_query_count for trial in trial_rows),
    )


def _linear_fit(points: Sequence[tuple[float, float]]) -> tuple[float | None, float | None, float | None]:
    if len(points) < 2:
        return None, None, None
    mean_x = sum(x for x, _ in points) / len(points)
    mean_y = sum(y for _, y in points) / len(points)
    denominator = sum((x - mean_x) ** 2 for x, _ in points)
    if denominator == 0:
        return None, None, None
    slope = sum((x - mean_x) * (y - mean_y) for x, y in points) / denominator
    intercept = mean_y - slope * mean_x
    residual = sum((y - (slope * x + intercept)) ** 2 for x, y in points)
    total = sum((y - mean_y) ** 2 for _, y in points)
    r_squared = 1.0 - residual / total if total else 1.0
    return slope, intercept, r_squared


def _fit_rule(rule: str, rows: Sequence[RecurrenceScalingRow], threshold: float = 0.5) -> ScalingFit:
    threshold_points: list[dict[str, int | float]] = []
    for n_bits in sorted({row.n_bits for row in rows if row.rule == rule}):
        eligible = sorted(
            (
                row
                for row in rows
                if row.rule == rule and row.n_bits == n_bits and row.observed_endpoint_success_rate >= threshold
            ),
            key=lambda row: row.sample_count,
        )
        if eligible:
            row = eligible[0]
            threshold_points.append(
                {
                    "n_bits": n_bits,
                    "sample_count": row.sample_count,
                    "sample_exponent_log2": row.budget_exponent_log2,
                    "observed_success_rate": row.observed_endpoint_success_rate,
                    "wilson_lower_95": row.wilson_success_lower_95,
                }
            )
    sqrt_fit = _linear_fit(
        [(math.sqrt(int(point["n_bits"])), float(point["sample_exponent_log2"])) for point in threshold_points]
    )
    linear_fit = _linear_fit(
        [(float(point["n_bits"]), float(point["sample_exponent_log2"])) for point in threshold_points]
    )
    return ScalingFit(
        rule=rule,
        successful_n_count=len(threshold_points),
        threshold_points=threshold_points,
        sqrt_n_slope=sqrt_fit[0],
        sqrt_n_intercept=sqrt_fit[1],
        sqrt_n_r_squared=sqrt_fit[2],
        linear_n_slope=linear_fit[0],
        linear_n_intercept=linear_fit[1],
        linear_n_r_squared=linear_fit[2],
        interpretation=(
            "Finite-horizon descriptive fit only. Selecting the first tested budget above 50% success, adaptive "
            "schedule effects, and small n preclude an asymptotic inference."
        ),
    )


def run_dcp_recurrence_report(
    n_values: Sequence[int] = (8, 12, 16, 20, 24),
    budget_multipliers: Sequence[float] = (1.5, 2.0, 2.5, 3.0),
    rules: Sequence[str] = (
        "randomized-equal-residue-difference",
        "nonzero-equal-residue-difference",
        "opposite-residue-sum",
        "target-complement-difference",
    ),
    trials_per_point: int = 12,
    seed: int = 0,
) -> DCPRecurrenceReport:
    if trials_per_point < 2:
        raise ValueError("trials_per_point must be at least 2 for interval estimation")
    kernel_rules = list(dict.fromkeys(rules))
    certificates = [
        certify_pair_kernel(n_bits, default_dcp_schedule(n_bits)[0], rule)
        for n_bits in sorted(set(min(9, int(value)) for value in n_values))
        for rule in kernel_rules
    ]
    rows = [
        run_scaling_row(
            n_bits=int(n_bits),
            rule=rule,
            budget_multiplier=float(multiplier),
            trials=trials_per_point,
            seed=seed + 1000003 * n_index + 1009 * rule_index + budget_index,
        )
        for n_index, n_bits in enumerate(n_values)
        for rule_index, rule in enumerate(rules)
        for budget_index, multiplier in enumerate(budget_multipliers)
    ]
    fits = [_fit_rule(rule, rows) for rule in rules]
    identity_failures = sum(item.exhaustive_failure_count for item in certificates)
    evaluator_queries = sum(row.evaluator_query_count for row in rows)
    generated_success_rows = sum(row.sieve_generated_endpoint_success_count > 0 for row in rows)
    target_birthday_fit = next((fit for fit in fits if fit.rule == "target-complement-difference"), None)
    randomized_fit = next((fit for fit in fits if fit.rule == "randomized-equal-residue-difference"), None)
    nonzero_fit = next((fit for fit in fits if fit.rule == "nonzero-equal-residue-difference"), None)
    metrics: dict[str, int | float | str] = {
        "pair_kernel_certificate_count": len(certificates),
        "pair_kernel_failure_count": identity_failures,
        "scaling_row_count": len(rows),
        "total_trial_count": sum(row.trial_count for row in rows),
        "total_charged_coset_states": sum(row.sample_count * row.trial_count for row in rows),
        "direct_target_input_count": sum(row.direct_target_input_count for row in rows),
        "sieve_generated_target_count": sum(row.sieve_generated_target_count for row in rows),
        "target_capable_pair_count": sum(row.mean_target_capable_pairs * row.trial_count for row in rows),
        "exact_conditional_expected_target_count": sum(
            row.mean_exact_conditional_expected_targets * row.trial_count for row in rows
        ),
        "target_yield_over_conditional_expectation": (
            sum(row.sieve_generated_target_count for row in rows)
            / sum(row.mean_exact_conditional_expected_targets * row.trial_count for row in rows)
            if sum(row.mean_exact_conditional_expected_targets * row.trial_count for row in rows)
            else -1.0
        ),
        "no_target_opportunity_trial_count": sum(row.no_target_opportunity_trial_count for row in rows),
        "max_abs_endpoint_success_calibration_residual": max(
            (abs(row.endpoint_success_calibration_residual) for row in rows), default=0.0
        ),
        "mean_abs_endpoint_success_calibration_residual": (
            sum(abs(row.endpoint_success_calibration_residual) for row in rows) / len(rows) if rows else 0.0
        ),
        "generated_endpoint_success_row_count": generated_success_rows,
        "evaluator_query_count": evaluator_queries,
        "target_complement_linear_n_slope": (
            target_birthday_fit.linear_n_slope if target_birthday_fit and target_birthday_fit.linear_n_slope is not None else -1.0
        ),
        "target_complement_linear_n_r_squared": (
            target_birthday_fit.linear_n_r_squared
            if target_birthday_fit and target_birthday_fit.linear_n_r_squared is not None
            else -1.0
        ),
        "randomized_equal_residue_threshold_n_count": randomized_fit.successful_n_count if randomized_fit else 0,
        "greedy_nonzero_threshold_n_count": nonzero_fit.successful_n_count if nonzero_fit else 0,
        "proved_uniform_endpoint_lower_bound_count": 0,
        "proved_asymptotic_improvement_count": 0,
    }
    falsifiers = [
        "Exact one-pair kernels do not imply independent bucket occupancies or a multi-round endpoint recurrence.",
        "The tested budget grid and finite n values cannot distinguish asymptotic sqrt(n), sqrt(n log n), or linear-n exponents.",
        "Target-complement pairing is a legal birthday baseline, not a subexponential sieve improvement theorem.",
        "No rule has a proved full-family endpoint lower bound or end-to-end recursive failure budget.",
    ]
    if identity_failures:
        falsifiers.append("At least one analytic pair-kernel formula failed exhaustive verification.")
    if randomized_fit and nonzero_fit and nonzero_fit.successful_n_count < randomized_fit.successful_n_count:
        falsifiers.append(
            "Greedily eliminating every immediate zero-label difference reduced threshold coverage relative to randomized bucket pairing."
        )
    claim_gate = {
        "one_pair_kernel_exact": identity_failures == 0,
        "conditional_branch_transition_exact": True,
        "state_access_contract_preserved": evaluator_queries == 0,
        "bad_register_robustness_proved": False,
        "raw_input_target_hits_excluded": True,
        "uniform_multi_round_recurrence_proved": False,
        "uniform_target_opportunity_lower_bound_proved": False,
        "bounded_recursive_failure_proved": False,
        "asymptotic_improvement_proved": False,
        "speedup_claim_allowed": False,
        "reason": "Pair kernels and finite scaling are audited, but the adaptive multi-round stochastic recurrence is unproved.",
    }
    summary = (
        f"Audited {len(rows)} DCP scaling rows across {sum(row.trial_count for row in rows)} trials and "
        f"{int(metrics['total_charged_coset_states'])} charged states. Exact pair kernels had {identity_failures} "
        f"verification failures; {generated_success_rows} rows generated a post-sieve endpoint after excluding raw-input "
        "target labels. No uniform endpoint or asymptotic improvement theorem was established."
    )
    return DCPRecurrenceReport(
        created_at=utc_now(),
        theorem_contract_id="THM-REGEV-USVP-TO-DCP-2003",
        pair_kernel_certificates=certificates,
        scaling_rows=rows,
        scaling_fits=fits,
        headline_metrics=metrics,
        claim_gate=claim_gate,
        status="finite-recurrence-evidence-proof-debt",
        summary=summary,
        falsifiers_triggered=falsifiers,
    )


def write_dcp_recurrence_report(
    path: Path = DCP_RECURRENCE_PATH,
    n_values: Sequence[int] = (8, 12, 16, 20, 24),
    budget_multipliers: Sequence[float] = (1.5, 2.0, 2.5, 3.0),
    trials_per_point: int = 12,
    seed: int = 0,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    report = run_dcp_recurrence_report(
        n_values=n_values,
        budget_multipliers=budget_multipliers,
        trials_per_point=trials_per_point,
        seed=seed,
    )
    payload = asdict(report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-FINITE-SCALING-NOT-RECURRENCE-THEOREM",
                source=str(path),
                claim="Finite endpoint scaling fits establish an asymptotic DCP sieve improvement.",
                reason_invalid=(
                    "The fits select thresholds on a finite budget grid and do not control adaptive bucket occupancy, "
                    "pair dependence, recursive stage failure, or the lattice parameter map."
                ),
                lesson="Require a symbolic stochastic recurrence and uniform bounds before comparing asymptotic exponents.",
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence=payload["headline_metrics"],
            )
        )
        metrics = payload["headline_metrics"]
        if int(metrics.get("greedy_nonzero_threshold_n_count", 0)) < int(
            metrics.get("randomized_equal_residue_threshold_n_count", 0)
        ):
            upsert_negative_result(
                NegativeResultRecord(
                    id="NEG-DCP-GREEDY-NONZERO-MATCHING-DESTROYS-SCALING",
                    source=str(path),
                    claim="Maximizing immediate nonzero differences improves a DCP bucket sieve.",
                    reason_invalid=(
                        "The live sweep found fewer modulus sizes crossing the endpoint-success threshold under maximum "
                        "nonzero matching than under randomized equal-residue matching. Local yield optimization distorts "
                        "the downstream label distribution."
                    ),
                    lesson="Score merge rules by the complete valuation/occupancy recurrence, not one-round nonzero yield.",
                    applies_to=[registry_candidate_id, registry_experiment_id],
                    evidence={
                        "greedy_nonzero_threshold_n_count": metrics["greedy_nonzero_threshold_n_count"],
                        "randomized_equal_residue_threshold_n_count": metrics[
                            "randomized_equal_residue_threshold_n_count"
                        ],
                    },
                )
            )
        target_slope = float(metrics.get("target_complement_linear_n_slope", -1.0) or -1.0)
        target_r_squared = float(metrics.get("target_complement_linear_n_r_squared", -1.0) or -1.0)
        if 0.35 <= target_slope <= 0.7 and target_r_squared >= 0.8:
            upsert_negative_result(
                NegativeResultRecord(
                    id="NEG-DCP-TARGET-COMPLEMENT-BIRTHDAY-SCALING",
                    source=str(path),
                    claim="Directly pairing known labels separated by N/2 is a subexponential DCP sieve improvement.",
                    reason_invalid=(
                        f"The finite threshold fit scales linearly in n=log2(N), with slope {target_slope:.3f} and "
                        f"R^2={target_r_squared:.3f}, consistent with a square-root-of-N birthday search."
                    ),
                    lesson="Use target-complement pairing as an exponential baseline, not a candidate breakthrough mechanism.",
                    applies_to=[registry_candidate_id, registry_experiment_id],
                    evidence={
                        "linear_n_slope": target_slope,
                        "linear_n_r_squared": target_r_squared,
                    },
                )
            )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-DCP-RECURRENCE"
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
                artifacts={"dcp_recurrence_analysis": str(path)},
            )
        )
    return payload
