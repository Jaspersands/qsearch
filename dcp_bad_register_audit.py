"""Adversarial bad-register audit for the exact Regev DCP promise."""

from __future__ import annotations

import json
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

from dcp_sample_workbench import (
    _pairs_for_rule,
    combine_dcp_phase_states,
    default_dcp_schedule,
    generate_dcp_phase_samples,
)
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


DCP_BAD_REGISTER_PATH = Path("research/phase_workbench/dcp_bad_register_audit.json")
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-BAD-REGISTER-ROBUSTNESS"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class BadRegisterTrial:
    n_bits: int
    rule: str
    sample_count: int
    bad_probability: float
    adversarial_bad_pair_branch: bool
    bad_input_count: int
    good_input_count: int
    valid_target_count: int
    corrupted_target_count: int
    total_target_count: int
    selected_endpoint_valid_probability: float
    selected_endpoint_false_bit_probability: float
    estimated_all_bits_valid_probability: float
    contaminated_non_target_output_count: int
    valid_non_target_output_count: int
    final_contaminated_state_count: int
    final_valid_state_count: int
    evaluator_query_count: int


@dataclass(frozen=True)
class BadRegisterScalingRow:
    n_bits: int
    rule: str
    bad_probability: float
    trial_count: int
    sample_count: int
    mean_bad_inputs: float
    endpoint_trial_count: int
    valid_endpoint_trial_count: int
    corrupted_endpoint_trial_count: int
    mean_selected_endpoint_valid_probability: float
    mean_selected_endpoint_false_bit_probability: float
    mean_estimated_all_bits_valid_probability: float
    mean_corrupted_target_count: float
    mean_valid_target_count: float
    zero_valid_endpoint_trial_count: int
    evaluator_query_count: int


@dataclass(frozen=True)
class BadRegisterDepthCertificate:
    n_bits: int
    bad_probability: float
    generic_sieve_depth_proxy: int
    input_leaves_at_generic_depth: int
    all_good_probability_at_generic_depth: float
    inverse_polynomial_threshold: float
    maximum_depth_above_threshold: int
    generic_depth_exceeds_robust_limit: bool
    valid_endpoint_bias: float
    majority_target_bit_failure: float
    log2_majority_endpoints_required: float
    generic_sample_exponent_proxy: float
    majority_log2_endpoints_over_sqrt_n: float
    majority_repair_exceeds_unit_sqrt_n_proxy: bool
    assumption: str


@dataclass(frozen=True)
class DCPBadRegisterReport:
    created_at: str
    theorem_contract_id: str
    theorem_promise: dict[str, str | int]
    rows: list[BadRegisterScalingRow]
    depth_certificates: list[BadRegisterDepthCertificate]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def certify_bad_register_depth(n_bits: int, polynomial_power: float = 1.0) -> BadRegisterDepthCertificate:
    if n_bits < 2 or polynomial_power <= 0:
        raise ValueError("require n_bits >= 2 and positive polynomial_power")
    bad_probability = 1.0 / n_bits
    threshold = n_bits ** (-polynomial_power)
    generic_depth = int(math.ceil(math.sqrt(n_bits)))
    leaves = 1 << generic_depth
    log_good = math.log1p(-bad_probability)
    all_good = math.exp(leaves * log_good) if leaves * log_good > -745 else 0.0
    log2_good = leaves * log_good / math.log(2.0)
    target_bit_failure = 1.0 / (3.0 * n_bits)
    log2_majority = math.log2(2.0 * math.log(1.0 / target_bit_failure)) - 2.0 * log2_good
    generic_sample_exponent = math.sqrt(n_bits)
    maximum_leaves = math.log(threshold) / log_good
    maximum_depth = max(0, int(math.floor(math.log2(maximum_leaves))))
    return BadRegisterDepthCertificate(
        n_bits=n_bits,
        bad_probability=bad_probability,
        generic_sieve_depth_proxy=generic_depth,
        input_leaves_at_generic_depth=leaves,
        all_good_probability_at_generic_depth=all_good,
        inverse_polynomial_threshold=threshold,
        maximum_depth_above_threshold=maximum_depth,
        generic_depth_exceeds_robust_limit=generic_depth > maximum_depth,
        valid_endpoint_bias=all_good,
        majority_target_bit_failure=target_bit_failure,
        log2_majority_endpoints_required=log2_majority,
        generic_sample_exponent_proxy=generic_sample_exponent,
        majority_log2_endpoints_over_sqrt_n=log2_majority / generic_sample_exponent,
        majority_repair_exceeds_unit_sqrt_n_proxy=log2_majority > generic_sample_exponent,
        assumption=(
            "Balanced pairwise merges, independent per-register bad events at the maximum f=1 rate, and an output is "
            "phase-valid only when every input leaf is good. This obstructs the unprotected merge architecture, not all DCP algorithms."
        ),
    )


def run_bad_register_trial(
    n_bits: int,
    sample_count: int,
    rule: str,
    bad_probability: float,
    seed: int,
    adversarial_bad_pair_branch: bool = True,
) -> BadRegisterTrial:
    if not 0.0 <= bad_probability <= 1.0:
        raise ValueError("bad_probability must lie in [0,1]")
    modulus = 1 << n_bits
    target = modulus // 2
    rng = random.Random(seed + 991)
    states = generate_dcp_phase_samples(n_bits, sample_count, seed)
    validity = {state.id: rng.random() >= bad_probability for state in states}
    bad_inputs = sum(not value for value in validity.values())
    valid_targets = sum(state.label == target and validity[state.id] for state in states)
    corrupt_targets = sum(state.label == target and not validity[state.id] for state in states)
    states = [state for state in states if state.label not in {0, target}]
    contaminated_outputs = 0
    valid_outputs = 0

    for bucket_bits in default_dcp_schedule(n_bits):
        if len(states) < 2:
            break
        pairs, _, _, desired_branch = _pairs_for_rule(states, bucket_bits, rule, rng=rng)
        outputs = []
        output_validity: dict[str, bool] = {}
        for left, right in pairs:
            both_valid = validity[left.id] and validity[right.id]
            both_bad = not validity[left.id] and not validity[right.id]
            favorable = True if both_bad and adversarial_bad_pair_branch else rng.randrange(2) == 0
            if not favorable:
                continue
            output = combine_dcp_phase_states(left, right, desired_branch).output_state
            if output.label == 0:
                continue
            if output.label == target:
                if both_valid:
                    valid_targets += 1
                else:
                    corrupt_targets += 1
                continue
            outputs.append(output)
            output_validity[output.id] = both_valid
            if both_valid:
                valid_outputs += 1
            else:
                contaminated_outputs += 1
        states = outputs
        validity = output_validity

    total_targets = valid_targets + corrupt_targets
    endpoint_valid_probability = valid_targets / total_targets if total_targets else 0.0
    false_bit_probability = 0.5 * corrupt_targets / total_targets if total_targets else 1.0
    all_bits_valid = endpoint_valid_probability**n_bits if total_targets else 0.0
    return BadRegisterTrial(
        n_bits=n_bits,
        rule=rule,
        sample_count=sample_count,
        bad_probability=bad_probability,
        adversarial_bad_pair_branch=adversarial_bad_pair_branch,
        bad_input_count=bad_inputs,
        good_input_count=sample_count - bad_inputs,
        valid_target_count=valid_targets,
        corrupted_target_count=corrupt_targets,
        total_target_count=total_targets,
        selected_endpoint_valid_probability=endpoint_valid_probability,
        selected_endpoint_false_bit_probability=false_bit_probability,
        estimated_all_bits_valid_probability=all_bits_valid,
        contaminated_non_target_output_count=contaminated_outputs,
        valid_non_target_output_count=valid_outputs,
        final_contaminated_state_count=sum(not value for value in validity.values()),
        final_valid_state_count=sum(validity.values()),
        evaluator_query_count=0,
    )


def run_bad_register_row(
    n_bits: int,
    rule: str,
    bad_probability: float,
    budget_multiplier: float,
    trials: int,
    seed: int,
) -> BadRegisterScalingRow:
    sample_count = 1 << int(math.ceil(budget_multiplier * math.sqrt(n_bits)))
    trial_rows = [
        run_bad_register_trial(
            n_bits,
            sample_count,
            rule,
            bad_probability,
            seed + 10007 * index,
        )
        for index in range(trials)
    ]
    endpoint_trials = [trial for trial in trial_rows if trial.total_target_count]
    return BadRegisterScalingRow(
        n_bits=n_bits,
        rule=rule,
        bad_probability=bad_probability,
        trial_count=trials,
        sample_count=sample_count,
        mean_bad_inputs=sum(trial.bad_input_count for trial in trial_rows) / trials,
        endpoint_trial_count=len(endpoint_trials),
        valid_endpoint_trial_count=sum(trial.valid_target_count > 0 for trial in trial_rows),
        corrupted_endpoint_trial_count=sum(trial.corrupted_target_count > 0 for trial in trial_rows),
        mean_selected_endpoint_valid_probability=(
            sum(trial.selected_endpoint_valid_probability for trial in endpoint_trials) / len(endpoint_trials)
            if endpoint_trials
            else 0.0
        ),
        mean_selected_endpoint_false_bit_probability=(
            sum(trial.selected_endpoint_false_bit_probability for trial in endpoint_trials) / len(endpoint_trials)
            if endpoint_trials
            else 1.0
        ),
        mean_estimated_all_bits_valid_probability=(
            sum(trial.estimated_all_bits_valid_probability for trial in endpoint_trials) / len(endpoint_trials)
            if endpoint_trials
            else 0.0
        ),
        mean_corrupted_target_count=sum(trial.corrupted_target_count for trial in trial_rows) / trials,
        mean_valid_target_count=sum(trial.valid_target_count for trial in trial_rows) / trials,
        zero_valid_endpoint_trial_count=sum(trial.valid_target_count == 0 for trial in trial_rows),
        evaluator_query_count=sum(trial.evaluator_query_count for trial in trial_rows),
    )


def run_dcp_bad_register_report(
    n_values: Sequence[int] = (12, 16, 20, 24),
    rules: Sequence[str] = (
        "randomized-equal-residue-difference",
        "opposite-residue-sum",
    ),
    budget_multiplier: float = 2.0,
    trials_per_row: int = 32,
    seed: int = 0,
) -> DCPBadRegisterReport:
    rows = [
        run_bad_register_row(
            n_bits,
            rule,
            bad_probability,
            budget_multiplier,
            trials_per_row,
            seed + 1_000_003 * n_index + 1009 * rule_index + condition_index,
        )
        for n_index, n_bits in enumerate(n_values)
        for rule_index, rule in enumerate(rules)
        for condition_index, bad_probability in enumerate((0.0, 1.0 / n_bits))
    ]
    theorem_rows = [row for row in rows if row.bad_probability > 0]
    control_rows = [row for row in rows if row.bad_probability == 0]
    depth_certificates = [certify_bad_register_depth(n_bits) for n_bits in (32, 64, 128, 256, 512, 1024)]
    failing_depths = [item for item in depth_certificates if item.generic_depth_exceeds_robust_limit]
    metrics: dict[str, int | float] = {
        "row_count": len(rows),
        "theorem_promise_row_count": len(theorem_rows),
        "perfect_control_row_count": len(control_rows),
        "total_trial_count": len(rows) * trials_per_row,
        "theorem_corrupted_endpoint_row_count": sum(row.corrupted_endpoint_trial_count > 0 for row in theorem_rows),
        "theorem_zero_valid_endpoint_trial_count": sum(row.zero_valid_endpoint_trial_count for row in theorem_rows),
        "minimum_theorem_endpoint_valid_probability": min(
            (row.mean_selected_endpoint_valid_probability for row in theorem_rows), default=0.0
        ),
        "maximum_theorem_false_bit_probability": max(
            (row.mean_selected_endpoint_false_bit_probability for row in theorem_rows), default=1.0
        ),
        "minimum_theorem_all_bits_valid_probability": min(
            (row.mean_estimated_all_bits_valid_probability for row in theorem_rows), default=0.0
        ),
        "evaluator_query_count": sum(row.evaluator_query_count for row in rows),
        "proved_bad_register_robustness_count": 0,
        "depth_certificate_count": len(depth_certificates),
        "generic_depth_robustness_failure_count": len(failing_depths),
        "first_generic_depth_robustness_failure_n_bits": failing_depths[0].n_bits if failing_depths else -1,
        "majority_repair_exceeds_unit_sqrt_n_proxy_count": sum(
            item.majority_repair_exceeds_unit_sqrt_n_proxy for item in depth_certificates
        ),
    }
    falsifiers = [
        "The perfect-state DCP sieve does not cover the f=1 theorem promise unless arbitrary bad basis-state registers are tolerated.",
        "Bad-register contamination is not observable from the public Fourier label and can propagate through merges.",
        "Finite contamination rates do not establish an adversarial robustness theorem or a decoder error-correction threshold.",
        "Under independent maximum-rate corruptions, an unprotected balanced merge of depth Theta(sqrt(n)) eventually has superpolynomially small all-good probability.",
        "Majority voting on unverified endpoints needs inverse-square samples in the surviving valid-state bias; its log-sample exponent divided by sqrt(n) grows rapidly in the depth certificates.",
    ]
    claim_gate = {
        "exact_f1_bad_rate_tested": True,
        "bad_registers_hidden_from_algorithm": True,
        "state_access_contract_preserved": metrics["evaluator_query_count"] == 0,
        "adversarial_bad_register_robustness_proved": False,
        "recursive_decoder_robustness_proved": False,
        "speedup_claim_allowed": False,
        "reason": "The current sieve and decoder have no proof against arbitrary bad registers allowed by the reduction theorem.",
    }
    summary = (
        f"Ran {int(metrics['total_trial_count'])} perfect-control and exact-f=1 bad-register trials. "
        f"{int(metrics['theorem_corrupted_endpoint_row_count'])}/{len(theorem_rows)} theorem-promise rows produced "
        f"corrupted endpoints; the worst mean false parity-bit probability was "
        f"{float(metrics['maximum_theorem_false_bit_probability']):.3f}. No robustness threshold was proved."
    )
    return DCPBadRegisterReport(
        created_at=utc_now(),
        theorem_contract_id="THM-REGEV-USVP-TO-DCP-2003",
        theorem_promise={
            "failure_parameter": 1,
            "maximum_bad_probability": "1/log2(N)=1/n_bits",
            "bad_state": "arbitrary computational-basis register |b,x>",
            "solver_success": "poly(1/log N)",
        },
        rows=rows,
        depth_certificates=depth_certificates,
        headline_metrics=metrics,
        claim_gate=claim_gate,
        status="bad-register-robustness-unproved",
        summary=summary,
        falsifiers_triggered=falsifiers,
    )


def write_dcp_bad_register_report(
    path: Path = DCP_BAD_REGISTER_PATH,
    n_values: Sequence[int] = (12, 16, 20, 24),
    trials_per_row: int = 32,
    seed: int = 0,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    report = run_dcp_bad_register_report(n_values=n_values, trials_per_row=trials_per_row, seed=seed)
    payload = asdict(report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-PERFECT-STATE-SIEVE-DOES-NOT-COVER-REGEV-F1-PROMISE",
                source=str(path),
                claim="A sieve tested only on perfect DCP coset states covers the Regev f=1 lattice reduction.",
                reason_invalid=(
                    "The theorem permits arbitrary bad basis-state registers at rate 1/log N. They are not identified by "
                    "the Fourier label and can create corrupted endpoints and random decoder bits."
                ),
                lesson="Prove adversarial contamination tolerance or restrict the claimed reduction route.",
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence=payload["headline_metrics"],
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-UNPROTECTED-SQRT-N-MERGE-DEPTH-LOSES-F1-VALIDITY",
                source=str(path),
                claim="An unprotected Theta(sqrt(log N))-depth balanced phase-state sieve remains robust under f=1 bad registers.",
                reason_invalid=(
                    "A depth-d output depends on up to 2^d leaves. At bad rate 1/log N, its all-good probability is "
                    "(1-1/log N)^(2^d); inverse-polynomial validity permits only d=O(log log N), not Theta(sqrt(log N))."
                ),
                lesson="A lattice-relevant DCP algorithm needs shallow architecture, active error detection, or a proof that invalid leaves do not erase the signal.",
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence={
                    "first_failure_n_bits": payload["headline_metrics"]["first_generic_depth_robustness_failure_n_bits"],
                    "failure_count": payload["headline_metrics"]["generic_depth_robustness_failure_count"],
                    "majority_repair_exceeds_unit_sqrt_n_proxy_count": payload["headline_metrics"][
                        "majority_repair_exceeds_unit_sqrt_n_proxy_count"
                    ],
                },
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-DCP-BAD-REGISTERS"
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
                artifacts={"dcp_bad_register_audit": str(path)},
            )
        )
    return payload
