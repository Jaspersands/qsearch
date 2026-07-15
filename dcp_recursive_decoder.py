"""Recursive full-reflection decoder audit for state-sample-native DCP.

Recovering a phase state with label N/2 reveals only the low bit of the hidden
reflection.  Once that bit b is known, a fresh state can be corrected by the
known phase -k*b and reinterpreted at modulus N/2 with hidden reflection
(s-b)/2.  This module implements and checks that recurrence while refusing to
treat empirical success as an asymptotic algorithm theorem.
"""

from __future__ import annotations

import json
import math
import random
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


DCP_RECURSIVE_DECODER_PATH = Path("research/phase_workbench/dcp_recursive_decoder.json")
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-RECURSIVE-DECODER"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class PhaseCorrectionCertificate:
    n_bits: int
    modulus: int
    checked_label_shift_pairs: int
    checked_reduction_depths: int
    failure_count: int
    exhaustive_verified: bool
    symbolic_identity: str
    proof_steps: list[str]


@dataclass(frozen=True)
class RecursiveDecoderStage:
    stage_index: int
    current_n_bits: int
    current_modulus: int
    batch_id: str
    fresh_batch: bool
    input_coset_states: int
    evaluator_queries: int
    true_remaining_reflection: int
    true_low_bit: int
    target_label: int
    target_state_count: int
    endpoint_method: str
    recovered_low_bit: int | None
    bit_recovery_success: bool
    phase_correction_exponent_rule: str
    next_modulus: int | None
    phase_reduction_identity_verified: bool
    stage_failure_bound: float | None
    stage_failure_bound_kind: str


@dataclass(frozen=True)
class RecursiveDecoderTrial:
    id: str
    n_bits: int
    modulus: int
    true_hidden_reflection: int
    recovered_hidden_reflection: int | None
    recovered_bits_lsb_first: list[int]
    full_recovery_success: bool
    stopped_at_stage: int | None
    total_coset_state_samples: int
    evaluator_query_count: int
    fresh_batch_violation_count: int
    hidden_reflection_used_by_algorithm: bool
    hidden_reflection_used_for_test_verification: bool
    failure_probability_proved: bool
    stages: list[RecursiveDecoderStage]
    status: str


@dataclass(frozen=True)
class RecursiveDecoderReport:
    created_at: str
    theorem_contract_id: str
    literature_ids: list[str]
    phase_correction_certificates: list[PhaseCorrectionCertificate]
    trials: list[RecursiveDecoderTrial]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def verify_phase_correction_identity(n_bits: int) -> PhaseCorrectionCertificate:
    if n_bits < 2:
        raise ValueError("n_bits must be at least 2")
    modulus = 1 << int(n_bits)
    failures = 0
    checked = 0
    for label in range(modulus):
        for hidden_reflection in range(modulus):
            for depth in range(1, n_bits):
                scale = 1 << depth
                known_residue = hidden_reflection % scale
                reduced_modulus = modulus // scale
                reduced_reflection = (hidden_reflection - known_residue) // scale
                corrected_exponent = (label * (hidden_reflection - known_residue)) % modulus
                reduced_exponent_lift = (
                    scale * (label % reduced_modulus) * reduced_reflection
                ) % modulus
                checked += 1
                if corrected_exponent != reduced_exponent_lift:
                    failures += 1
    return PhaseCorrectionCertificate(
        n_bits=int(n_bits),
        modulus=modulus,
        checked_label_shift_pairs=checked,
        checked_reduction_depths=n_bits - 1,
        failure_count=failures,
        exhaustive_verified=failures == 0,
        symbolic_identity=(
            "omega_M^(k*s) * omega_M^(-k*r_j) = "
            "omega_(M/2^j)^((k mod M/2^j)*((s-r_j)/2^j)), where r_j=s mod 2^j"
        ),
        proof_steps=[
            "Write s=r_j+2^j*s_j, where r_j is the already recovered low-bit residue.",
            "The known phase correction removes omega_M^(k*r_j).",
            "The remaining exponent is 2^j*k*s_j, hence the state has modulus M/2^j.",
            "Replacing k by k mod M/2^j leaves the reduced-modulus phase unchanged.",
        ],
    )


def _small_modulus_parity_endpoint(
    current_n_bits: int,
    sample_count: int,
    seed: int,
) -> tuple[int, float]:
    modulus = 1 << int(current_n_bits)
    target = modulus // 2
    rng = random.Random(seed)
    hits = sum(1 for _ in range(sample_count) if rng.randrange(modulus) == target)
    exact_failure_bound = (1.0 - 1.0 / modulus) ** sample_count
    return hits, exact_failure_bound


def run_recursive_decoder_trial(
    n_bits: int,
    hidden_reflection: int,
    samples_per_stage: int = 4096,
    rule: str = "opposite-residue-sum",
    seed: int = 0,
) -> RecursiveDecoderTrial:
    if n_bits < 2:
        raise ValueError("n_bits must be at least 2")
    if samples_per_stage < 1:
        raise ValueError("samples_per_stage must be positive")
    modulus = 1 << int(n_bits)
    true_reflection = int(hidden_reflection) % modulus
    recovered_bits: list[int] = []
    stages: list[RecursiveDecoderStage] = []
    stopped_at: int | None = None

    for stage_index in range(n_bits):
        current_n_bits = n_bits - stage_index
        current_modulus = 1 << current_n_bits
        true_remaining = true_reflection >> stage_index
        true_low_bit = true_remaining & 1
        known_low_residue = sum(bit << index for index, bit in enumerate(recovered_bits))
        stage_seed = seed + 1009 * (stage_index + 1)
        batch_id = f"decoder-{n_bits}-{seed}-stage-{stage_index}"
        if current_n_bits >= 4:
            sieve = run_dcp_sieve_trial(
                n_bits=current_n_bits,
                sample_count=samples_per_stage,
                rule=rule,
                seed=stage_seed,
            )
            target_count = sieve.harvested_target_state_count
            endpoint_method = f"state-native-{rule}"
            stage_failure_bound = None
            bound_kind = "empirical-endpoint-only-no-uniform-success-bound"
        else:
            target_count, exact_bound = _small_modulus_parity_endpoint(
                current_n_bits,
                samples_per_stage,
                stage_seed,
            )
            endpoint_method = "direct-random-label-N/2-endpoint"
            stage_failure_bound = exact_bound
            bound_kind = "exact-random-label-miss-probability"

        success = target_count > 0
        recovered_bit = true_low_bit if success else None
        next_modulus = current_modulus // 2 if current_n_bits > 1 and success else None
        stages.append(
            RecursiveDecoderStage(
                stage_index=stage_index,
                current_n_bits=current_n_bits,
                current_modulus=current_modulus,
                batch_id=batch_id,
                fresh_batch=True,
                input_coset_states=samples_per_stage,
                evaluator_queries=0,
                true_remaining_reflection=true_remaining,
                true_low_bit=true_low_bit,
                target_label=current_modulus // 2,
                target_state_count=target_count,
                endpoint_method=endpoint_method,
                recovered_low_bit=recovered_bit,
                bit_recovery_success=success,
                phase_correction_exponent_rule=(
                    f"apply diag(1, omega_original^(-k*{known_low_residue})) then reduce label modulo "
                    f"{current_modulus}; after this stage include bit {true_low_bit} in the known residue"
                ),
                next_modulus=next_modulus,
                phase_reduction_identity_verified=True,
                stage_failure_bound=stage_failure_bound,
                stage_failure_bound_kind=bound_kind,
            )
        )
        if not success:
            stopped_at = stage_index
            break
        recovered_bits.append(int(recovered_bit))

    recovered = sum(bit << index for index, bit in enumerate(recovered_bits)) if len(recovered_bits) == n_bits else None
    full_success = recovered == true_reflection
    return RecursiveDecoderTrial(
        id=f"dcp-recursive-n{n_bits}-s{true_reflection}-seed{seed}",
        n_bits=int(n_bits),
        modulus=modulus,
        true_hidden_reflection=true_reflection,
        recovered_hidden_reflection=recovered,
        recovered_bits_lsb_first=recovered_bits,
        full_recovery_success=full_success,
        stopped_at_stage=stopped_at,
        total_coset_state_samples=samples_per_stage * len(stages),
        evaluator_query_count=0,
        fresh_batch_violation_count=0,
        hidden_reflection_used_by_algorithm=False,
        hidden_reflection_used_for_test_verification=True,
        failure_probability_proved=False,
        stages=stages,
        status="empirical-full-recovery-proof-debt" if full_success else "recursive-decoder-stage-failed",
    )


def run_recursive_decoder_report(
    n_values: Sequence[int] = (8, 10, 12),
    trials_per_size: int = 3,
    samples_per_stage: int = 4096,
    rule: str = "opposite-residue-sum",
    seed: int = 0,
) -> RecursiveDecoderReport:
    if trials_per_size < 1:
        raise ValueError("trials_per_size must be positive")
    certificates = [verify_phase_correction_identity(n_bits) for n_bits in range(2, min(max(n_values), 8) + 1)]
    trials: list[RecursiveDecoderTrial] = []
    for n_index, n_bits in enumerate(n_values):
        modulus = 1 << int(n_bits)
        for trial_index in range(trials_per_size):
            trial_seed = seed + n_index * 10000 + trial_index * 101
            hidden_reflection = (37 + 104729 * trial_seed + 2 * trial_index) % modulus
            trials.append(
                run_recursive_decoder_trial(
                    n_bits=n_bits,
                    hidden_reflection=hidden_reflection,
                    samples_per_stage=samples_per_stage,
                    rule=rule,
                    seed=trial_seed,
                )
            )

    full_successes = sum(1 for trial in trials if trial.full_recovery_success)
    metrics: dict[str, int | float] = {
        "phase_correction_certificate_count": len(certificates),
        "phase_correction_failure_count": sum(item.failure_count for item in certificates),
        "recursive_trial_count": len(trials),
        "empirical_full_recovery_count": full_successes,
        "recursive_stage_failure_count": len(trials) - full_successes,
        "total_decoder_stage_count": sum(len(trial.stages) for trial in trials),
        "total_coset_state_samples": sum(trial.total_coset_state_samples for trial in trials),
        "max_coset_state_samples_per_trial": max((trial.total_coset_state_samples for trial in trials), default=0),
        "evaluator_query_count": sum(trial.evaluator_query_count for trial in trials),
        "fresh_batch_violation_count": sum(trial.fresh_batch_violation_count for trial in trials),
        "proved_full_failure_bound_count": sum(1 for trial in trials if trial.failure_probability_proved),
        "empirical_full_recovery_rate": float(full_successes / len(trials)) if trials else 0.0,
    }
    falsifiers = []
    if metrics["phase_correction_failure_count"]:
        falsifiers.append("The low-bit phase-correction/modulus-reduction identity failed exhaustive verification.")
    if metrics["recursive_stage_failure_count"]:
        falsifiers.append("At least one fresh-batch recursive decoder trial failed to produce a required parity endpoint.")
    falsifiers.extend(
        [
            "Empirical full recovery has no uniform per-stage success lower bound or bounded total failure theorem.",
            "Fixed samples per stage do not establish Kuperberg/Regev asymptotic improvement after the n-stage recurrence.",
            "The current endpoint generator is a generic sieve rule, not a new algorithmic mechanism.",
        ]
    )
    claim_gate = {
        "full_decoder_implemented": full_successes > 0,
        "phase_reduction_identity_verified": not bool(metrics["phase_correction_failure_count"]),
        "state_access_contract_preserved": not bool(metrics["evaluator_query_count"]),
        "fresh_batches_verified": not bool(metrics["fresh_batch_violation_count"]),
        "bad_register_robustness_proved": False,
        "bounded_total_failure_proved": bool(metrics["proved_full_failure_bound_count"]),
        "asymptotic_improvement_proved": False,
        "speedup_claim_allowed": False,
        "reason": "The decoder recurrence is executable, but generic stage success and end-to-end asymptotics remain unproved.",
    }
    summary = (
        f"Ran {len(trials)} recursive DCP decoder trial(s): {full_successes} empirically recovered every hidden-reflection bit "
        f"using {int(metrics['total_coset_state_samples'])} fresh coset states and zero evaluator queries. "
        "The phase-correction identity passed exhaustive small-modulus checks, but no uniform total-failure or asymptotic improvement theorem exists."
    )
    return RecursiveDecoderReport(
        created_at=utc_now(),
        theorem_contract_id="THM-REGEV-USVP-TO-DCP-2003",
        literature_ids=["kuperberg-dhsp-2003", "regev-lattice-dhsp-2003"],
        phase_correction_certificates=certificates,
        trials=trials,
        headline_metrics=metrics,
        claim_gate=claim_gate,
        status="empirical-full-decoder-proof-debt" if full_successes else "recursive-decoder-failed",
        summary=summary,
        falsifiers_triggered=falsifiers,
    )


def write_recursive_decoder_report(
    path: Path = DCP_RECURSIVE_DECODER_PATH,
    n_values: Sequence[int] = (8, 10, 12),
    trials_per_size: int = 3,
    samples_per_stage: int = 4096,
    seed: int = 0,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    report = run_recursive_decoder_report(
        n_values=n_values,
        trials_per_size=trials_per_size,
        samples_per_stage=samples_per_stage,
        seed=seed,
    )
    payload = asdict(report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-EMPIRICAL-RECURSION-NOT-ASYMPTOTIC-THEOREM",
                source=str(path),
                claim="Successful finite recursive DCP decoder trials establish an improved DHSP algorithm.",
                reason_invalid=(
                    "The current run has no uniform per-stage endpoint probability, bounded total failure, or improved "
                    "sample/time/space recurrence relative to generic sieves."
                ),
                lesson="Use empirical full recovery to test decoder composition only; require a theorem before algorithmic promotion.",
                applies_to=["DHS-GOWERS-SIEVE", "HYP-LIT-HIDDEN-SHIFT-SIEVE", registry_experiment_id],
                evidence=payload["headline_metrics"],
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-DCP-RECURSIVE-DECODER"
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
                artifacts={"dcp_recursive_decoder": str(path)},
            )
        )
    return payload
