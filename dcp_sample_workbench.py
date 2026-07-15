"""State-sample-native workbench for the dihedral coset problem.

The lattice-to-DCP theorem contract supplies independent coset states, not a
coherent phase evaluator.  This module keeps that boundary explicit and models
the physical sum/difference branch of a two-state phase-label combine.  It is a
baseline and falsification tool, not a claimed improvement to Kuperberg or
Regev.
"""

from __future__ import annotations

import json
import heapq
import math
import random
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


DCP_SAMPLE_WORKBENCH_PATH = Path("research/phase_workbench/dcp_sample_native_sieve.json")
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-SAMPLE-NATIVE-SIEVE"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class DCPStateAccessContract:
    theorem_contract_id: str
    source_problem: str
    target_problem: str
    supplied_resources: list[str]
    allowed_operations: list[str]
    forbidden_resources: list[str]
    label_distribution: str
    state_expression: str
    failure_parameter: int
    maximum_bad_register_probability: str
    bad_register_state: str
    current_workbench_models_bad_registers: bool
    full_family_scope: str
    full_family_coverage: bool


@dataclass(frozen=True)
class DCPPhaseState:
    id: str
    modulus: int
    label: int
    two_adic_valuation: int
    source_sample_ids: list[int]
    merge_depth: int
    phase_expression: str


@dataclass(frozen=True)
class DCPMergeBranch:
    branch: str
    probability: float
    output_state: DCPPhaseState
    relative_phase_rule: str


@dataclass(frozen=True)
class DCPRoundRecord:
    round_index: int
    requested_rule: str
    pairing_mode: str
    bucket_bits: int
    input_states: int
    pair_count: int
    desired_nonzero_pair_count: int
    target_capable_pair_count: int
    exact_conditional_expected_outputs: float
    exact_conditional_expected_targets: float
    exact_conditional_no_target_probability: float
    unpaired_discard_count: int
    favorable_branch_count: int
    unfavorable_branch_count: int
    zero_information_output_count: int
    actual_output_states: int
    harvested_target_states: int
    legacy_optimistic_output_states: int
    postselection_optimism_gap: int
    best_two_adic_valuation: int


@dataclass(frozen=True)
class DCPDecoderAudit:
    target_label: int
    target_state_count: int
    parity_observation_available: bool
    independent_congruence_bits_recovered: int
    hidden_reflection_bits_required: int
    full_hidden_reflection_recovered: bool
    missing_decoder_stages: list[str]
    interpretation: str


@dataclass(frozen=True)
class DCPSieveTrial:
    id: str
    n_bits: int
    modulus: int
    rule: str
    schedule: list[int]
    input_sample_count: int
    zero_information_input_count: int
    direct_target_input_count: int
    coset_state_query_count: int
    evaluator_query_count: int
    final_active_state_count: int
    harvested_target_state_count: int
    best_two_adic_valuation: int
    reached_target_valuation: bool
    sample_exponent_log2: float
    normalized_sqrt_exponent_proxy: float
    memory_peak_states: int
    merge_depth: int
    rounds: list[DCPRoundRecord]
    decoder: DCPDecoderAudit
    status: str


@dataclass(frozen=True)
class DCPSampleWorkbenchReport:
    created_at: str
    access_contract: DCPStateAccessContract
    known_asymptotic_baselines: list[dict[str, str]]
    trials: list[DCPSieveTrial]
    headline_metrics: dict[str, int | float]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def two_adic_valuation(label: int, n_bits: int) -> int:
    modulus = 1 << int(n_bits)
    value = int(label) % modulus
    if value == 0:
        return int(n_bits)
    valuation = 0
    while value % 2 == 0:
        valuation += 1
        value //= 2
    return valuation


def dcp_state_access_contract() -> DCPStateAccessContract:
    return DCPStateAccessContract(
        theorem_contract_id="THM-REGEV-USVP-TO-DCP-2003",
        source_problem="theta(n^2.5)-unique-SVP",
        target_problem="dihedral-coset-problem-state-input",
        supplied_resources=[
            "independent D_N register samples, each normally a coset state but subject to the theorem's bad-register promise",
            "known uniformly distributed Fourier label k after the group Fourier transform",
            "single-qubit phase state (|0> + omega_N^(k*s)|1>)/sqrt(2)",
        ],
        allowed_operations=[
            "classical computation on known labels",
            "two-state CNOT combine",
            "computational-basis branch measurement",
            "postselection with charged success probability",
        ],
        forbidden_resources=[
            "coherent phase evaluator",
            "chosen label queries",
            "full phase truth table",
            "family-specific advice not constructed from the lattice instance",
        ],
        label_distribution="for a good register k is uniform in Z_N; k=0 is legal and carries no hidden-shift information",
        state_expression="|psi_k> = (|0> + exp(2*pi*i*k*s/N)|1>)/sqrt(2)",
        failure_parameter=1,
        maximum_bad_register_probability="1/log2(N) for the f=1 theorem specialization",
        bad_register_state="arbitrary computational-basis state |b,x> rather than a coset state",
        current_workbench_models_bad_registers=False,
        full_family_scope="all good and bad-register DCP inputs emitted by the exact f=1 lattice-to-DCP theorem contract",
        full_family_coverage=False,
    )


def _phase_state(state_id: str, modulus: int, label: int, sources: list[int], depth: int) -> DCPPhaseState:
    n_bits = int(math.log2(modulus))
    normalized = int(label) % modulus
    return DCPPhaseState(
        id=state_id,
        modulus=modulus,
        label=normalized,
        two_adic_valuation=two_adic_valuation(normalized, n_bits),
        source_sample_ids=sorted(set(int(item) for item in sources)),
        merge_depth=int(depth),
        phase_expression=f"omega_{modulus}^({normalized}*s)",
    )


def generate_dcp_phase_samples(n_bits: int, sample_count: int, seed: int = 0) -> list[DCPPhaseState]:
    if n_bits < 3:
        raise ValueError("n_bits must be at least 3")
    if sample_count < 1:
        raise ValueError("sample_count must be positive")
    modulus = 1 << int(n_bits)
    rng = random.Random(seed)
    return [
        _phase_state(f"dcp-0-{index}", modulus, rng.randrange(modulus), [index], 0)
        for index in range(sample_count)
    ]


def combine_dcp_phase_states(left: DCPPhaseState, right: DCPPhaseState, branch: str) -> DCPMergeBranch:
    """Return the exact known-label state conditioned on one CNOT measurement branch."""
    if left.modulus != right.modulus:
        raise ValueError("phase states must use the same modulus")
    if branch not in {"sum", "difference"}:
        raise ValueError("branch must be 'sum' or 'difference'")
    if branch == "sum":
        label = left.label + right.label
        rule = "measurement branch 0 gives label k_left + k_right"
    else:
        label = left.label - right.label
        rule = "measurement branch 1 gives label k_left - k_right up to global phase"
    state = _phase_state(
        f"{left.id}-{branch}-{right.id}",
        left.modulus,
        label,
        left.source_sample_ids + right.source_sample_ids,
        max(left.merge_depth, right.merge_depth) + 1,
    )
    return DCPMergeBranch(branch=branch, probability=0.5, output_state=state, relative_phase_rule=rule)


def _equal_residue_pairs(states: Sequence[DCPPhaseState], bucket_bits: int, valuation_first: bool) -> tuple[list[tuple[DCPPhaseState, DCPPhaseState]], int]:
    bucket_modulus = 1 << int(bucket_bits)
    buckets: dict[int, list[DCPPhaseState]] = {}
    for state in states:
        buckets.setdefault(state.label % bucket_modulus, []).append(state)
    pairs: list[tuple[DCPPhaseState, DCPPhaseState]] = []
    unpaired = 0
    for bucket in buckets.values():
        if valuation_first:
            bucket.sort(key=lambda item: (-item.two_adic_valuation, item.label, item.id))
        else:
            bucket.sort(key=lambda item: (item.label, item.id))
        pairs.extend((bucket[index], bucket[index + 1]) for index in range(0, len(bucket) - 1, 2))
        unpaired += len(bucket) % 2
    return pairs, unpaired


def _randomized_equal_residue_pairs(
    states: Sequence[DCPPhaseState], bucket_bits: int, rng: random.Random
) -> tuple[list[tuple[DCPPhaseState, DCPPhaseState]], int]:
    bucket_modulus = 1 << int(bucket_bits)
    buckets: dict[int, list[DCPPhaseState]] = {}
    for state in states:
        buckets.setdefault(state.label % bucket_modulus, []).append(state)
    pairs: list[tuple[DCPPhaseState, DCPPhaseState]] = []
    unpaired = 0
    for residue in sorted(buckets):
        bucket = list(buckets[residue])
        rng.shuffle(bucket)
        pairs.extend((bucket[index], bucket[index + 1]) for index in range(0, len(bucket) - 1, 2))
        unpaired += len(bucket) % 2
    return pairs, unpaired


def _nonzero_equal_residue_pairs(
    states: Sequence[DCPPhaseState], bucket_bits: int
) -> tuple[list[tuple[DCPPhaseState, DCPPhaseState]], int]:
    """Maximize legal pairs with unequal labels inside each residue bucket."""
    bucket_modulus = 1 << int(bucket_bits)
    buckets: dict[int, dict[int, list[DCPPhaseState]]] = {}
    for state in states:
        buckets.setdefault(state.label % bucket_modulus, {}).setdefault(state.label, []).append(state)
    pairs: list[tuple[DCPPhaseState, DCPPhaseState]] = []
    total_states = len(states)
    for residue in sorted(buckets):
        groups = buckets[residue]
        heap = [(-len(group), label, group) for label, group in groups.items()]
        heapq.heapify(heap)
        while len(heap) >= 2:
            neg_left, left_label, left_group = heapq.heappop(heap)
            neg_right, right_label, right_group = heapq.heappop(heap)
            pairs.append((left_group.pop(), right_group.pop()))
            if left_group:
                heapq.heappush(heap, (neg_left + 1, left_label, left_group))
            if right_group:
                heapq.heappush(heap, (neg_right + 1, right_label, right_group))
    return pairs, total_states - 2 * len(pairs)


def _target_complement_pairs(
    states: Sequence[DCPPhaseState], target_label: int
) -> tuple[list[tuple[DCPPhaseState, DCPPhaseState]], int]:
    """Legal birthday baseline: pair known labels whose difference is N/2."""
    by_label: dict[int, list[DCPPhaseState]] = {}
    for state in states:
        by_label.setdefault(state.label, []).append(state)
    pairs: list[tuple[DCPPhaseState, DCPPhaseState]] = []
    used: set[int] = set()
    for label in sorted(by_label):
        if label in used:
            continue
        complement = label ^ int(target_label)
        used.add(label)
        used.add(complement)
        left = by_label.get(label, [])
        right = by_label.get(complement, [])
        pairs.extend((left[index], right[index]) for index in range(min(len(left), len(right))))
    return pairs, len(states) - 2 * len(pairs)


def _opposite_residue_pairs(states: Sequence[DCPPhaseState], bucket_bits: int) -> tuple[list[tuple[DCPPhaseState, DCPPhaseState]], int]:
    bucket_modulus = 1 << int(bucket_bits)
    buckets: dict[int, list[DCPPhaseState]] = {}
    for state in states:
        buckets.setdefault(state.label % bucket_modulus, []).append(state)
    pairs: list[tuple[DCPPhaseState, DCPPhaseState]] = []
    used_residues: set[int] = set()
    unpaired = 0
    for residue in sorted(buckets):
        if residue in used_residues:
            continue
        opposite = (-residue) % bucket_modulus
        left_bucket = sorted(buckets.get(residue, []), key=lambda item: (item.label, item.id))
        right_bucket = sorted(buckets.get(opposite, []), key=lambda item: (item.label, item.id))
        used_residues.add(residue)
        used_residues.add(opposite)
        if residue == opposite:
            pairs.extend((left_bucket[index], left_bucket[index + 1]) for index in range(0, len(left_bucket) - 1, 2))
            unpaired += len(left_bucket) % 2
        else:
            pair_count = min(len(left_bucket), len(right_bucket))
            pairs.extend((left_bucket[index], right_bucket[index]) for index in range(pair_count))
            unpaired += len(left_bucket) + len(right_bucket) - 2 * pair_count
    return pairs, unpaired


def _pairs_for_rule(
    states: Sequence[DCPPhaseState], bucket_bits: int, rule: str, rng: random.Random | None = None
) -> tuple[list[tuple[DCPPhaseState, DCPPhaseState]], int, str, str]:
    if rule == "equal-residue-difference":
        pairs, unpaired = _equal_residue_pairs(states, bucket_bits, valuation_first=False)
        return pairs, unpaired, "equal-residue", "difference"
    if rule == "valuation-prioritized-difference":
        pairs, unpaired = _equal_residue_pairs(states, bucket_bits, valuation_first=True)
        return pairs, unpaired, "valuation-prioritized-equal-residue", "difference"
    if rule == "randomized-equal-residue-difference":
        pairs, unpaired = _randomized_equal_residue_pairs(states, bucket_bits, rng or random.Random(0))
        return pairs, unpaired, "randomized-equal-residue", "difference"
    if rule == "nonzero-equal-residue-difference":
        pairs, unpaired = _nonzero_equal_residue_pairs(states, bucket_bits)
        return pairs, unpaired, "maximum-nonzero-equal-residue", "difference"
    if rule == "target-complement-difference":
        target = states[0].modulus // 2 if states else 0
        pairs, unpaired = _target_complement_pairs(states, target)
        return pairs, unpaired, "target-complement-birthday", "difference"
    if rule == "opposite-residue-sum":
        pairs, unpaired = _opposite_residue_pairs(states, bucket_bits)
        return pairs, unpaired, "opposite-residue", "sum"
    if rule == "adaptive-signed":
        equal_pairs, equal_unpaired = _equal_residue_pairs(states, bucket_bits, valuation_first=True)
        opposite_pairs, opposite_unpaired = _opposite_residue_pairs(states, bucket_bits)
        if len(opposite_pairs) > len(equal_pairs):
            return opposite_pairs, opposite_unpaired, "adaptive-opposite-residue", "sum"
        return equal_pairs, equal_unpaired, "adaptive-equal-residue", "difference"
    raise ValueError(f"unknown merge rule: {rule}")


def default_dcp_schedule(n_bits: int) -> list[int]:
    target = int(n_bits) - 1
    block = max(1, int(math.ceil(math.sqrt(n_bits))))
    schedule = list(range(block, target + 1, block))
    if not schedule or schedule[-1] != target:
        schedule.append(target)
    return schedule


def audit_dcp_decoder(target_states: Sequence[DCPPhaseState], n_bits: int) -> DCPDecoderAudit:
    modulus = 1 << int(n_bits)
    target_label = modulus // 2
    useful = [state for state in target_states if state.label == target_label]
    has_parity = bool(useful)
    return DCPDecoderAudit(
        target_label=target_label,
        target_state_count=len(useful),
        parity_observation_available=has_parity,
        independent_congruence_bits_recovered=1 if has_parity else 0,
        hidden_reflection_bits_required=int(n_bits),
        full_hidden_reflection_recovered=False,
        missing_decoder_stages=[
            "recover the remaining hidden-reflection bits by a uniform recursive modulus-reduction procedure",
            "prove bounded total failure probability across all bit-recovery stages",
            "compose the recovered reflection with the exact lattice decoder and parameter map",
        ],
        interpretation=(
            "A label N/2 phase state yields the parity of s after a Hadamard measurement. It is one congruence bit, "
            "not a full hidden-reflection decoder."
            if has_parity
            else "No N/2 phase state was produced, so even the parity-bit endpoint was not reached."
        ),
    )


def run_dcp_sieve_trial(
    n_bits: int,
    sample_count: int,
    rule: str,
    seed: int = 0,
    schedule: Sequence[int] | None = None,
) -> DCPSieveTrial:
    if n_bits < 4:
        raise ValueError("n_bits must be at least 4")
    active_schedule = list(schedule) if schedule is not None else default_dcp_schedule(n_bits)
    if not active_schedule or any(bits < 1 or bits >= n_bits for bits in active_schedule):
        raise ValueError("schedule bucket bits must lie in [1, n_bits - 1]")
    modulus = 1 << int(n_bits)
    target_valuation = int(n_bits) - 1
    rng = random.Random(seed + 991)
    states = generate_dcp_phase_samples(n_bits, sample_count, seed)
    zero_inputs = sum(1 for state in states if state.label == 0)
    harvested = [state for state in states if state.label == modulus // 2]
    direct_target_inputs = len(harvested)
    states = [state for state in states if state.label not in {0, modulus // 2}]
    memory_peak = sample_count
    best_valuation = max((state.two_adic_valuation for state in harvested), default=0)
    rounds: list[DCPRoundRecord] = []

    for round_index, bucket_bits in enumerate(active_schedule, start=1):
        if len(states) < 2:
            break
        pairs, unpaired, pairing_mode, desired_branch = _pairs_for_rule(states, int(bucket_bits), rule, rng=rng)
        outputs: list[DCPPhaseState] = []
        favorable = 0
        unfavorable = 0
        zero_outputs = 0
        legacy_outputs = 0
        target_capable_pairs = 0
        new_targets: list[DCPPhaseState] = []
        for left, right in pairs:
            optimistic = combine_dcp_phase_states(left, right, desired_branch).output_state
            if optimistic.label != 0:
                legacy_outputs += 1
            if optimistic.label == modulus // 2:
                target_capable_pairs += 1
            observed_branch = "sum" if rng.randrange(2) == 0 else "difference"
            observed = combine_dcp_phase_states(left, right, observed_branch).output_state
            if observed_branch != desired_branch:
                unfavorable += 1
                continue
            favorable += 1
            if observed.label == 0:
                zero_outputs += 1
                continue
            if observed.label == modulus // 2:
                new_targets.append(observed)
            else:
                outputs.append(observed)
        harvested.extend(new_targets)
        valuations = [state.two_adic_valuation for state in outputs + new_targets]
        best_valuation = max(best_valuation, max(valuations, default=0))
        rounds.append(
            DCPRoundRecord(
                round_index=round_index,
                requested_rule=rule,
                pairing_mode=pairing_mode,
                bucket_bits=int(bucket_bits),
                input_states=len(states),
                pair_count=len(pairs),
                desired_nonzero_pair_count=legacy_outputs,
                target_capable_pair_count=target_capable_pairs,
                exact_conditional_expected_outputs=0.5 * legacy_outputs,
                exact_conditional_expected_targets=0.5 * target_capable_pairs,
                exact_conditional_no_target_probability=2.0 ** (-target_capable_pairs),
                unpaired_discard_count=unpaired,
                favorable_branch_count=favorable,
                unfavorable_branch_count=unfavorable,
                zero_information_output_count=zero_outputs,
                actual_output_states=len(outputs) + len(new_targets),
                harvested_target_states=len(new_targets),
                legacy_optimistic_output_states=legacy_outputs,
                postselection_optimism_gap=max(0, legacy_outputs - len(outputs) - len(new_targets)),
                best_two_adic_valuation=max(valuations, default=0),
            )
        )
        states = outputs
        memory_peak = max(memory_peak, len(states) + len(harvested))

    decoder = audit_dcp_decoder(harvested, n_bits)
    status = "parity-endpoint-only" if decoder.parity_observation_available else "target-valuation-not-reached"
    return DCPSieveTrial(
        id=f"dcp-n{n_bits}-{rule}-seed{seed}",
        n_bits=int(n_bits),
        modulus=modulus,
        rule=rule,
        schedule=active_schedule,
        input_sample_count=int(sample_count),
        zero_information_input_count=zero_inputs,
        direct_target_input_count=direct_target_inputs,
        coset_state_query_count=int(sample_count),
        evaluator_query_count=0,
        final_active_state_count=len(states),
        harvested_target_state_count=len(harvested),
        best_two_adic_valuation=best_valuation,
        reached_target_valuation=best_valuation >= target_valuation,
        sample_exponent_log2=float(math.log2(max(1, sample_count))),
        normalized_sqrt_exponent_proxy=float(math.log2(max(1, sample_count)) / math.sqrt(n_bits)),
        memory_peak_states=memory_peak,
        merge_depth=len(rounds),
        rounds=rounds,
        decoder=decoder,
        status=status,
    )


def known_asymptotic_sieve_baselines() -> list[dict[str, str]]:
    return [
        {
            "id": "kuperberg-dhsp-2003",
            "access_model": "independent DCP coset/phase-state samples",
            "time_and_query_class": "2^O(sqrt(log N))",
            "space_class": "subexponential",
            "role": "generic benchmark; this workbench does not claim a better hidden constant or exponent",
        },
        {
            "id": "regev-polyspace-dhsp",
            "access_model": "independent DCP coset/phase-state samples",
            "time_and_query_class": "2^O(sqrt(log N * log log N))",
            "space_class": "polynomial",
            "role": "polynomial-space benchmark; schedule simulation is not a proof of matching this bound",
        },
    ]


def run_dcp_sample_workbench(
    n_values: Sequence[int] = (8, 10, 12),
    sample_count: int = 4096,
    rules: Sequence[str] = (
        "equal-residue-difference",
        "opposite-residue-sum",
        "valuation-prioritized-difference",
        "adaptive-signed",
        "randomized-equal-residue-difference",
        "nonzero-equal-residue-difference",
        "target-complement-difference",
    ),
    seed: int = 0,
) -> DCPSampleWorkbenchReport:
    trials = [
        run_dcp_sieve_trial(n_bits, sample_count, rule, seed=seed + 100 * n_index + rule_index)
        for n_index, n_bits in enumerate(n_values)
        for rule_index, rule in enumerate(rules)
    ]
    rounds = [round_record for trial in trials for round_record in trial.rounds]
    metrics: dict[str, int | float] = {
        "trial_count": len(trials),
        "full_family_contract_count": int(dcp_state_access_contract().full_family_coverage),
        "total_input_coset_states": sum(trial.input_sample_count for trial in trials),
        "zero_information_input_count": sum(trial.zero_information_input_count for trial in trials),
        "direct_target_input_count": sum(trial.direct_target_input_count for trial in trials),
        "evaluator_query_count": sum(trial.evaluator_query_count for trial in trials),
        "merge_attempt_count": sum(item.pair_count for item in rounds),
        "target_capable_pair_count": sum(item.target_capable_pair_count for item in rounds),
        "exact_conditional_expected_target_count": sum(item.exact_conditional_expected_targets for item in rounds),
        "favorable_branch_count": sum(item.favorable_branch_count for item in rounds),
        "unfavorable_branch_count": sum(item.unfavorable_branch_count for item in rounds),
        "actual_output_state_count": sum(item.actual_output_states for item in rounds),
        "legacy_optimistic_output_state_count": sum(item.legacy_optimistic_output_states for item in rounds),
        "postselection_optimism_gap": sum(item.postselection_optimism_gap for item in rounds),
        "target_valuation_trial_count": sum(1 for trial in trials if trial.reached_target_valuation),
        "parity_endpoint_trial_count": sum(1 for trial in trials if trial.decoder.parity_observation_available),
        "full_hidden_reflection_decode_count": sum(1 for trial in trials if trial.decoder.full_hidden_reflection_recovered),
        "max_best_two_adic_valuation": max((trial.best_two_adic_valuation for trial in trials), default=0),
    }
    falsifiers = []
    if metrics["postselection_optimism_gap"]:
        falsifiers.append(
            "Deterministically retaining the favorable subtraction/sum label overstates physical sieve yield because each branch has probability 1/2."
        )
    if not metrics["full_hidden_reflection_decode_count"]:
        falsifiers.append(
            "Reaching label N/2 supplies at most the parity of the hidden reflection; no uniform full-shift decoder is implemented."
        )
    falsifiers.append(
        "No tested merge rule proves an asymptotic improvement over the generic Kuperberg or polynomial-space Regev benchmarks."
    )
    summary = (
        f"Ran {len(trials)} state-sample-native DCP sieve trial(s) using {int(metrics['total_input_coset_states'])} "
        f"charged coset states and zero evaluator queries. Physical branch accounting removed "
        f"{int(metrics['postselection_optimism_gap'])} output(s) retained by the deterministic favorable-branch proxy; "
        f"{int(metrics['parity_endpoint_trial_count'])} trial(s) reached a parity endpoint and none decoded the full reflection."
    )
    return DCPSampleWorkbenchReport(
        created_at=utc_now(),
        access_contract=dcp_state_access_contract(),
        known_asymptotic_baselines=known_asymptotic_sieve_baselines(),
        trials=trials,
        headline_metrics=metrics,
        status="sample-native-baseline-blocks-speedup-claim",
        summary=summary,
        falsifiers_triggered=falsifiers,
    )


def write_dcp_sample_workbench(
    path: Path = DCP_SAMPLE_WORKBENCH_PATH,
    n_values: Sequence[int] = (8, 10, 12),
    sample_count: int = 4096,
    seed: int = 0,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    report = run_dcp_sample_workbench(n_values=n_values, sample_count=sample_count, seed=seed)
    payload = asdict(report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-DETERMINISTIC-FAVORABLE-BRANCH",
                source=str(path),
                claim="A bucketed phase-label trace may deterministically subtract matched labels when estimating sample yield.",
                reason_invalid=(
                    "The physical CNOT combine produces sum and difference labels with probability 1/2. "
                    f"The live audit found an optimism gap of {payload['headline_metrics']['postselection_optimism_gap']} outputs."
                ),
                lesson="Charge measurement branches and postselection in every phase-state sample exponent.",
                applies_to=["DHS-GOWERS-SIEVE", "HYP-LIT-HIDDEN-SHIFT-SIEVE", "EXP-DHS-PHASE-SIEVE"],
                evidence=payload["headline_metrics"],
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-PARITY-ENDPOINT-NOT-FULL-DECODER",
                source=str(path),
                claim="A high-valuation N/2 phase label constitutes recovery of the hidden reflection.",
                reason_invalid="The corresponding Hadamard measurement reveals only s mod 2; all remaining bits and reduction composition remain unproved.",
                lesson="Track decoded congruence bits and the complete recursive decoder separately from target valuation.",
                applies_to=["DHS-GOWERS-SIEVE", "HYP-LIT-HIDDEN-SHIFT-SIEVE", "EXP-DHS-PHASE-SIEVE"],
                evidence={
                    "parity_endpoint_trial_count": payload["headline_metrics"]["parity_endpoint_trial_count"],
                    "full_hidden_reflection_decode_count": payload["headline_metrics"]["full_hidden_reflection_decode_count"],
                },
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-DCP-SAMPLE-NATIVE"
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
                artifacts={"dcp_sample_native_sieve": str(path)},
            )
        )
    return payload
