"""Search and no-go certificates for state-native DCP collective witnesses.

An X/Y Pauli correlator supported on labels ``k_i`` has nonzero expectation
after averaging the unknown reflection only if a signed modular relation
``sum_i epsilon_i k_i = 0 (mod N)`` exists on its support.  This gives an
exact finite search and an asymptotic union-bound obstruction for bounded-
locality observables over polynomially many random DCP labels.
"""

from __future__ import annotations

import itertools
import json
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


DCP_COLLECTIVE_WITNESS_PATH = Path("research/phase_workbench/dcp_collective_witness_search.json")
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-COLLECTIVE-WITNESS-SEARCH"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class SignedRelationWitness:
    weight: int
    terms: list[tuple[int, int]]
    residue: int


@dataclass(frozen=True)
class BoundedCorrelatorTrial:
    n_bits: int
    label_count: int
    maximum_weight: int
    relation_count: int
    minimum_relation_weight: int
    patterns_checked: int
    first_witness: SignedRelationWitness | None


@dataclass(frozen=True)
class BoundedCorrelatorScalingRow:
    n_bits: int
    label_count: int
    maximum_weight: int
    trial_count: int
    signed_pattern_count: int
    relation_union_bound: float
    relation_trial_count: int
    total_relation_count: int
    minimum_observed_relation_weight: int
    polynomial_description: bool
    asymptotic_signal_class: str


@dataclass(frozen=True)
class LocalityBarrierCertificate:
    n_bits: int
    polynomial_label_count: int
    tested_locality: int
    log2_relation_union_bound: float
    negligible_below_inverse_polynomial: bool
    first_weight_not_ruled_out_by_union_bound: int
    first_unruled_weight_over_n: float
    balanced_measurement_depth_at_threshold: int
    all_good_probability_at_f1_rate_at_threshold: float
    conclusion: str


@dataclass(frozen=True)
class DCPCollectiveWitnessReport:
    created_at: str
    theorem_contract_id: str
    observable_schema: dict[str, str]
    scaling_rows: list[BoundedCorrelatorScalingRow]
    locality_certificates: list[LocalityBarrierCertificate]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def signed_relation_search(labels: Sequence[int], n_bits: int, maximum_weight: int) -> BoundedCorrelatorTrial:
    if n_bits < 2:
        raise ValueError("n_bits must be at least two")
    if maximum_weight < 1:
        raise ValueError("maximum_weight must be positive")
    modulus = 1 << n_bits
    normalized = [int(label) % modulus for label in labels]
    relation_count = 0
    patterns_checked = 0
    minimum_weight = 0
    first_witness: SignedRelationWitness | None = None
    for weight in range(1, min(maximum_weight, len(normalized)) + 1):
        for support in itertools.combinations(range(len(normalized)), weight):
            # Global sign reversal is the same relation, so fix the first sign.
            for tail_signs in itertools.product((-1, 1), repeat=weight - 1):
                signs = (1, *tail_signs)
                residue = sum(sign * normalized[index] for index, sign in zip(support, signs)) % modulus
                patterns_checked += 1
                if residue:
                    continue
                relation_count += 1
                if minimum_weight == 0:
                    minimum_weight = weight
                if first_witness is None:
                    first_witness = SignedRelationWitness(
                        weight=weight,
                        terms=[(index, sign) for index, sign in zip(support, signs)],
                        residue=0,
                    )
    return BoundedCorrelatorTrial(
        n_bits=n_bits,
        label_count=len(normalized),
        maximum_weight=maximum_weight,
        relation_count=relation_count,
        minimum_relation_weight=minimum_weight,
        patterns_checked=patterns_checked,
        first_witness=first_witness,
    )


def _signed_pattern_count(label_count: int, maximum_weight: int) -> int:
    return sum(
        math.comb(label_count, weight) * (1 << (weight - 1))
        for weight in range(1, min(label_count, maximum_weight) + 1)
    )


def _log2_add(left: float, right: float) -> float:
    if left == -math.inf:
        return right
    high, low = max(left, right), min(left, right)
    return high + math.log2(1.0 + 2.0 ** (low - high))


def _log2_signed_patterns(label_count: int, maximum_weight: int) -> float:
    total = -math.inf
    for weight in range(1, min(label_count, maximum_weight) + 1):
        log2_comb = (
            math.lgamma(label_count + 1)
            - math.lgamma(weight + 1)
            - math.lgamma(label_count - weight + 1)
        ) / math.log(2.0)
        total = _log2_add(total, log2_comb + weight - 1)
    return total


def certify_locality_barrier(n_bits: int, label_polynomial_power: int = 2) -> LocalityBarrierCertificate:
    if n_bits < 4 or label_polynomial_power < 1:
        raise ValueError("require n_bits >= 4 and a positive label polynomial power")
    label_count = n_bits**label_polynomial_power
    tested_locality = int(math.ceil(math.log2(n_bits)))
    log2_bound = _log2_signed_patterns(label_count, tested_locality) - math.log2((1 << n_bits) - 1)
    inverse_polynomial_log2 = -label_polynomial_power * math.log2(n_bits)
    threshold = 1
    while threshold < n_bits and _log2_signed_patterns(label_count, threshold) < math.log2((1 << n_bits) - 1):
        threshold += 1
    depth = int(math.ceil(math.log2(threshold))) if threshold > 1 else 0
    all_good = (1.0 - 1.0 / n_bits) ** threshold
    return LocalityBarrierCertificate(
        n_bits=n_bits,
        polynomial_label_count=label_count,
        tested_locality=tested_locality,
        log2_relation_union_bound=min(0.0, log2_bound),
        negligible_below_inverse_polynomial=log2_bound < inverse_polynomial_log2,
        first_weight_not_ruled_out_by_union_bound=threshold,
        first_unruled_weight_over_n=threshold / n_bits,
        balanced_measurement_depth_at_threshold=depth,
        all_good_probability_at_f1_rate_at_threshold=all_good,
        conclusion=(
            "All X/Y correlators of support at most ceil(log2 n) have negligible aggregate relation probability over "
            "n^2 random labels. A viable polynomial-time witness needs substantially more global support or a non-Pauli structure."
        ),
    )


def run_collective_witness_search(
    n_values: Sequence[int] = (12, 16, 20, 24),
    label_multiplier: int = 1,
    maximum_weight: int = 4,
    trials_per_row: int = 12,
    seed: int = 0,
) -> DCPCollectiveWitnessReport:
    if label_multiplier < 1 or trials_per_row < 1:
        raise ValueError("label_multiplier and trials_per_row must be positive")
    scaling_rows: list[BoundedCorrelatorScalingRow] = []
    all_trials: list[BoundedCorrelatorTrial] = []
    for n_index, n_bits in enumerate(n_values):
        modulus = 1 << n_bits
        label_count = label_multiplier * n_bits
        trials = []
        for trial_index in range(trials_per_row):
            rng = random.Random(seed + 1_000_003 * n_index + trial_index)
            # Zero-label states carry no hidden-reflection phase and may be discarded.
            labels = [rng.randrange(1, modulus) for _ in range(label_count)]
            trials.append(signed_relation_search(labels, n_bits, maximum_weight))
        all_trials.extend(trials)
        pattern_count = _signed_pattern_count(label_count, maximum_weight)
        scaling_rows.append(
            BoundedCorrelatorScalingRow(
                n_bits=n_bits,
                label_count=label_count,
                maximum_weight=maximum_weight,
                trial_count=trials_per_row,
                signed_pattern_count=pattern_count,
                relation_union_bound=min(1.0, pattern_count / ((1 << n_bits) - 1)),
                relation_trial_count=sum(trial.relation_count > 0 for trial in trials),
                total_relation_count=sum(trial.relation_count for trial in trials),
                minimum_observed_relation_weight=min(
                    (trial.minimum_relation_weight for trial in trials if trial.minimum_relation_weight), default=0
                ),
                polynomial_description=True,
                asymptotic_signal_class="finite-relation-only" if any(trial.relation_count for trial in trials) else "none",
            )
        )

    certificates = [certify_locality_barrier(n_bits) for n_bits in (32, 64, 128, 256, 512, 1024)]
    relation_trials = sum(trial.relation_count > 0 for trial in all_trials)
    metrics: dict[str, int | float] = {
        "scaling_row_count": len(scaling_rows),
        "finite_trial_count": len(all_trials),
        "finite_relation_trial_count": relation_trials,
        "finite_relation_count": sum(trial.relation_count for trial in all_trials),
        "locality_certificate_count": len(certificates),
        "logarithmic_locality_negligible_count": sum(item.negligible_below_inverse_polynomial for item in certificates),
        "minimum_first_unruled_relation_weight": min(
            item.first_weight_not_ruled_out_by_union_bound for item in certificates
        ),
        "maximum_first_unruled_relation_weight": max(
            item.first_weight_not_ruled_out_by_union_bound for item in certificates
        ),
        "polynomial_time_robust_witness_count": 0,
        "proved_full_decoder_count": 0,
    }
    falsifiers = [
        "A bounded-support X/Y correlator has zero hidden-reflection-averaged signal unless its public labels satisfy a signed modular relation.",
        "With polynomially many random labels, the union bound eventually makes logarithmic-locality signed-relation witnesses negligible; small-n rows where the bound is vacuous are not counted as certificates.",
        "Finite low-weight relations are postselected rare label events, not a uniform asymptotic DCP algorithm.",
        "No polynomial-time robust measurement or full-reflection decoder is produced by relation enumeration.",
    ]
    claim_gate = {
        "state_sample_native": True,
        "hidden_bad_flags_used": False,
        "finite_signed_relations_observed": relation_trials > 0,
        "logarithmic_locality_asymptotically_viable": False,
        "polynomial_time_robust_witness_known": False,
        "full_decoder_proved": False,
        "speedup_claim_allowed": False,
        "reason": (
            "Efficient bounded-locality Pauli observables almost surely lack the required modular relation; more global "
            "measurements remain computationally and adversarially unresolved."
        ),
    }
    summary = (
        f"Enumerated {sum(trial.patterns_checked for trial in all_trials)} bounded-weight signed-label patterns in "
        f"{len(all_trials)} finite trials and found relations in {relation_trials}. "
        f"{int(metrics['logarithmic_locality_negligible_count'])}/{len(certificates)} scaling rows certify logarithmic-locality "
        "Pauli witnesses below inverse-polynomial scale; no robust decoder was proved."
    )
    return DCPCollectiveWitnessReport(
        created_at=utc_now(),
        theorem_contract_id="THM-REGEV-USVP-TO-DCP-2003",
        observable_schema={
            "family": "bounded-support products of X/Y Pauli operators on public-label phase qubits",
            "signal_condition": "sum_i epsilon_i k_i = 0 mod N for a sign assignment on the observable support",
            "bad_state_response": "any uniformly randomized bad basis bit dephases an X/Y-supported coordinate",
            "search_legality": "uses only public Fourier labels; no evaluator, hidden reflection, or bad-validity flags",
        },
        scaling_rows=scaling_rows,
        locality_certificates=certificates,
        headline_metrics=metrics,
        claim_gate=claim_gate,
        status="bounded-locality-witness-class-obstructed",
        summary=summary,
        falsifiers_triggered=falsifiers,
    )


def write_collective_witness_search(
    path: Path = DCP_COLLECTIVE_WITNESS_PATH,
    n_values: Sequence[int] = (12, 16, 20, 24),
    label_multiplier: int = 1,
    maximum_weight: int = 4,
    trials_per_row: int = 12,
    seed: int = 0,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    report = run_collective_witness_search(
        n_values=n_values,
        label_multiplier=label_multiplier,
        maximum_weight=maximum_weight,
        trials_per_row=trials_per_row,
        seed=seed,
    )
    payload = asdict(report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-BOUNDED-LOCALITY-PAULI-WITNESSES-NEGLIGIBLE",
                source=str(path),
                claim="A polynomial-size search over bounded-locality Pauli correlators yields a uniform f=1 DCP contamination witness.",
                reason_invalid=(
                    "Nonzero common-reflection signal requires a signed modular relation among supported random labels. "
                    "For polynomially many labels, the aggregate probability for logarithmic support is negligible."
                ),
                lesson="Search genuinely global implicit measurements; finite rare relations cannot support a uniform decoder claim.",
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence={
                    "certificate_count": payload["headline_metrics"]["locality_certificate_count"],
                    "negligible_count": payload["headline_metrics"]["logarithmic_locality_negligible_count"],
                    "polynomial_time_robust_witness_count": 0,
                },
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-DCP-COLLECTIVE-WITNESS"
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
                artifacts={"dcp_collective_witness_search": str(path)},
            )
        )
    return payload
