"""Exact search over polynomial-description Clifford witnesses for DCP batches.

The circuits apply a public-label-derived quadratic Boolean phase followed by
Hadamards.  Computational-basis bad states always produce a uniform output,
while common-reflection phase states can produce nonuniformity through modular
subset-sum collisions.  Exact simulation reports both unrestricted total
variation distance and efficiently decoded Hamming-weight statistics.
"""

from __future__ import annotations

import json
import math
import random
from collections import Counter, defaultdict
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


DCP_CLIFFORD_WITNESS_PATH = Path("research/phase_workbench/dcp_clifford_witness_search.json")
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-CLIFFORD-WITNESS-SEARCH"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class CliffordMeasurementScore:
    schema_id: str
    cz_edge_count: int
    full_total_variation_distance: float
    hamming_weight_total_variation_distance: float
    zero_outcome_bias: float
    log2_shots_for_hamming_bias: float
    polynomial_circuit_description: bool
    polynomial_decision_rule: bool


@dataclass(frozen=True)
class CliffordWitnessInstance:
    n_bits: int
    register_count: int
    label_seed: int
    subset_sum_collision_excess: int
    exact_trace_distance_to_uniform: float
    scores: list[CliffordMeasurementScore]
    best_full_tv_schema: str
    best_full_tv: float
    best_hamming_schema: str
    best_hamming_tv: float
    all_good_probability_at_f1_rate: float


@dataclass(frozen=True)
class CliffordWitnessScalingRow:
    n_bits: int
    register_count: int
    trial_count: int
    schema_count: int
    collision_instance_count: int
    mean_exact_trace_distance: float
    mean_best_full_tv: float
    mean_best_hamming_tv: float
    maximum_best_hamming_tv: float
    inverse_polynomial_hamming_signal_count: int
    mean_log2_shots_for_best_hamming_bias: float
    best_hamming_schema_histogram: dict[str, int]


@dataclass(frozen=True)
class DCPCliffordWitnessReport:
    created_at: str
    theorem_contract_id: str
    measurement_contract: dict[str, str]
    rows: list[CliffordWitnessScalingRow]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _subset_sum_buckets(labels: Sequence[int], modulus: int) -> dict[int, list[int]]:
    sums = [0]
    for label in labels:
        sums += [((value + label) % modulus) for value in sums]
    buckets: dict[int, list[int]] = defaultdict(list)
    for mask, value in enumerate(sums):
        buckets[value].append(mask)
    return buckets


def _quadratic_phase_values(register_count: int, lower_neighbors: Sequence[int]) -> list[int]:
    values = [0] * (1 << register_count)
    for mask in range(1, 1 << register_count):
        bit = (mask & -mask).bit_length() - 1
        rest = mask & (mask - 1)
        values[mask] = values[rest] ^ ((lower_neighbors[bit] & rest).bit_count() & 1)
    return values


def _fwht(values: list[int]) -> None:
    span = 1
    while span < len(values):
        for start in range(0, len(values), 2 * span):
            for offset in range(span):
                left = start + offset
                right = left + span
                a, b = values[left], values[right]
                values[left] = a + b
                values[right] = a - b
        span *= 2


def _measurement_score(
    schema_id: str,
    lower_neighbors: Sequence[int],
    buckets: dict[int, list[int]],
    register_count: int,
) -> CliffordMeasurementScore:
    dimension = 1 << register_count
    phases = _quadratic_phase_values(register_count, lower_neighbors)
    xor_correlations = [0] * dimension
    for bucket in buckets.values():
        for left in bucket:
            left_sign = 1 if phases[left] == 0 else -1
            for right in bucket:
                right_sign = 1 if phases[right] == 0 else -1
                xor_correlations[left ^ right] += left_sign * right_sign
    _fwht(xor_correlations)
    denominator = float(dimension * dimension)
    probabilities = [value / denominator for value in xor_correlations]
    uniform = 1.0 / dimension
    full_tv = 0.5 * sum(abs(probability - uniform) for probability in probabilities)
    good_weight = [0.0] * (register_count + 1)
    uniform_weight = [0.0] * (register_count + 1)
    for outcome, probability in enumerate(probabilities):
        weight = outcome.bit_count()
        good_weight[weight] += probability
        uniform_weight[weight] += uniform
    hamming_tv = 0.5 * sum(abs(good - bad) for good, bad in zip(good_weight, uniform_weight))
    zero_bias = abs(probabilities[0] - uniform)
    log2_shots = -1.0 if hamming_tv <= 0.0 else math.log2(2.0 * math.log(6.0)) - 2.0 * math.log2(hamming_tv)
    return CliffordMeasurementScore(
        schema_id=schema_id,
        cz_edge_count=sum(mask.bit_count() for mask in lower_neighbors),
        full_total_variation_distance=full_tv,
        hamming_weight_total_variation_distance=hamming_tv,
        zero_outcome_bias=zero_bias,
        log2_shots_for_hamming_bias=log2_shots,
        polynomial_circuit_description=True,
        polynomial_decision_rule=True,
    )


def _schema_neighbors(labels: Sequence[int], n_bits: int) -> list[tuple[str, list[int]]]:
    register_count = len(labels)

    def build(predicate) -> list[int]:
        neighbors = [0] * register_count
        for right in range(register_count):
            for left in range(right):
                if predicate(left, right):
                    neighbors[right] |= 1 << left
        return neighbors

    schemas: list[tuple[str, list[int]]] = [
        ("hadamard-product", [0] * register_count),
        ("complete-cz", build(lambda _left, _right: True)),
        (
            "label-inner-product-cz",
            build(lambda left, right: ((labels[left] & labels[right]).bit_count() & 1) == 1),
        ),
        (
            "label-order-cz",
            build(lambda left, right: ((labels[left] + labels[right]) % (1 << n_bits)) < (1 << (n_bits - 1))),
        ),
    ]
    for bit in sorted({0, n_bits // 4, n_bits // 2, (3 * n_bits) // 4, n_bits - 1}):
        schemas.append(
            (
                f"label-product-bit-{bit}-cz",
                build(lambda left, right, bit=bit: ((labels[left] * labels[right]) >> bit) & 1),
            )
        )
    for random_seed in range(4):
        rng = random.Random(97_003 * n_bits + random_seed)
        schemas.append((f"fixed-random-{random_seed}-cz", build(lambda _left, _right, rng=rng: rng.randrange(2))))
    return schemas


def analyze_clifford_witness_instance(n_bits: int, labels: Sequence[int], label_seed: int = 0) -> CliffordWitnessInstance:
    if n_bits < 2 or not labels:
        raise ValueError("require n_bits >= 2 and at least one label")
    modulus = 1 << n_bits
    normalized = [int(label) % modulus for label in labels]
    buckets = _subset_sum_buckets(normalized, modulus)
    dimension = 1 << len(normalized)
    collision_excess = dimension - len(buckets)
    trace_distance = collision_excess / dimension
    scores = [
        _measurement_score(schema_id, neighbors, buckets, len(normalized))
        for schema_id, neighbors in _schema_neighbors(normalized, n_bits)
    ]
    best_full = max(scores, key=lambda item: item.full_total_variation_distance)
    best_hamming = max(scores, key=lambda item: item.hamming_weight_total_variation_distance)
    return CliffordWitnessInstance(
        n_bits=n_bits,
        register_count=len(normalized),
        label_seed=label_seed,
        subset_sum_collision_excess=collision_excess,
        exact_trace_distance_to_uniform=trace_distance,
        scores=scores,
        best_full_tv_schema=best_full.schema_id,
        best_full_tv=best_full.full_total_variation_distance,
        best_hamming_schema=best_hamming.schema_id,
        best_hamming_tv=best_hamming.hamming_weight_total_variation_distance,
        all_good_probability_at_f1_rate=(1.0 - 1.0 / n_bits) ** len(normalized),
    )


def _finite_log_slope(rows: Sequence[CliffordWitnessScalingRow]) -> float:
    points = [(row.n_bits, row.mean_best_hamming_tv) for row in rows if row.mean_best_hamming_tv > 0.0]
    if len(points) < 2:
        return 0.0
    mean_x = sum(x for x, _ in points) / len(points)
    mean_y = sum(math.log2(y) for _, y in points) / len(points)
    denominator = sum((x - mean_x) ** 2 for x, _ in points)
    return sum((x - mean_x) * (math.log2(y) - mean_y) for x, y in points) / denominator if denominator else 0.0


def run_clifford_witness_search(
    n_values: Sequence[int] = (8, 10, 12, 14, 16),
    trials_per_row: int = 4,
    seed: int = 0,
) -> DCPCliffordWitnessReport:
    if trials_per_row < 1:
        raise ValueError("trials_per_row must be positive")
    rows: list[CliffordWitnessScalingRow] = []
    all_instances: list[CliffordWitnessInstance] = []
    for n_index, n_bits in enumerate(n_values):
        modulus = 1 << n_bits
        instances = []
        for trial_index in range(trials_per_row):
            label_seed = seed + 1_000_003 * n_index + trial_index
            rng = random.Random(label_seed)
            labels = [rng.randrange(modulus) for _ in range(n_bits)]
            instances.append(analyze_clifford_witness_instance(n_bits, labels, label_seed))
        all_instances.extend(instances)
        histogram = Counter(instance.best_hamming_schema for instance in instances)
        best_shots = []
        for instance in instances:
            finite = [score.log2_shots_for_hamming_bias for score in instance.scores if score.log2_shots_for_hamming_bias >= 0.0]
            best_shots.append(min(finite) if finite else -1.0)
        rows.append(
            CliffordWitnessScalingRow(
                n_bits=n_bits,
                register_count=n_bits,
                trial_count=trials_per_row,
                schema_count=len(instances[0].scores),
                collision_instance_count=sum(instance.subset_sum_collision_excess > 0 for instance in instances),
                mean_exact_trace_distance=sum(instance.exact_trace_distance_to_uniform for instance in instances)
                / trials_per_row,
                mean_best_full_tv=sum(instance.best_full_tv for instance in instances) / trials_per_row,
                mean_best_hamming_tv=sum(instance.best_hamming_tv for instance in instances) / trials_per_row,
                maximum_best_hamming_tv=max(instance.best_hamming_tv for instance in instances),
                inverse_polynomial_hamming_signal_count=sum(
                    instance.best_hamming_tv >= 1.0 / (n_bits * n_bits) for instance in instances
                ),
                mean_log2_shots_for_best_hamming_bias=sum(best_shots) / trials_per_row,
                best_hamming_schema_histogram=dict(sorted(histogram.items())),
            )
        )

    slope = _finite_log_slope(rows)
    metrics: dict[str, int | float] = {
        "scaling_row_count": len(rows),
        "instance_count": len(all_instances),
        "schema_evaluation_count": sum(len(instance.scores) for instance in all_instances),
        "collision_instance_count": sum(instance.subset_sum_collision_excess > 0 for instance in all_instances),
        "inverse_polynomial_hamming_signal_count": sum(
            instance.best_hamming_tv >= 1.0 / (instance.n_bits * instance.n_bits) for instance in all_instances
        ),
        "maximum_full_tv": max((instance.best_full_tv for instance in all_instances), default=0.0),
        "maximum_hamming_tv": max((instance.best_hamming_tv for instance in all_instances), default=0.0),
        "finite_log2_hamming_tv_slope_per_n": slope,
        "proved_inverse_polynomial_signal_family_count": 0,
        "proved_adversarial_threshold_count": 0,
        "proved_full_decoder_count": 0,
    }
    falsifiers = [
        "Unrestricted output total variation may require an exponentially described accepting set; it is not counted as an efficient decoder.",
        "Hamming-weight decoding is polynomial but finite inverse-polynomial signals are not asymptotic proofs.",
        "All-bad computational-basis inputs are exactly uniform under every searched diagonal-Clifford-plus-Hadamard circuit.",
        "Partial arbitrary contamination, repeated-batch sample cost, and full-reflection recovery remain unproved.",
    ]
    claim_gate = {
        "public_labels_only": True,
        "polynomial_circuit_descriptions": True,
        "polynomial_hamming_decision_rule": True,
        "unrestricted_tv_counted_as_efficient_decoder": False,
        "inverse_polynomial_signal_proved": False,
        "adversarial_threshold_proved": False,
        "full_decoder_proved": False,
        "speedup_claim_allowed": False,
        "reason": (
            "The search evaluates a legitimate global Clifford measurement language, but finite Hamming-weight biases have "
            "no uniform lower bound, contamination theorem, or full reflection decoder."
        ),
    }
    summary = (
        f"Evaluated {int(metrics['schema_evaluation_count'])} public-label Clifford measurements on "
        f"{len(all_instances)} exact DCP batches. {int(metrics['inverse_polynomial_hamming_signal_count'])} finite instances "
        "had Hamming-weight bias at least 1/n^2, but zero asymptotic signal families, adversarial thresholds, or full decoders were proved."
    )
    return DCPCliffordWitnessReport(
        created_at=utc_now(),
        theorem_contract_id="THM-REGEV-USVP-TO-DCP-2003",
        measurement_contract={
            "circuit": "public-label-derived CZ phase layer followed by H on every phase qubit",
            "bad_input": "every computational-basis input yields the uniform output distribution",
            "efficient_decoder": "Hamming weight of the measured output; unrestricted optimal accepting sets are excluded",
            "simulation": "exact subset-sum collision blocks and Walsh-Hadamard transform; exponential simulation cost is not algorithm cost",
        },
        rows=rows,
        headline_metrics=metrics,
        claim_gate=claim_gate,
        status="finite-clifford-signal-proof-blocked",
        summary=summary,
        falsifiers_triggered=falsifiers,
    )


def write_clifford_witness_search(
    path: Path = DCP_CLIFFORD_WITNESS_PATH,
    n_values: Sequence[int] = (8, 10, 12, 14, 16),
    trials_per_row: int = 4,
    seed: int = 0,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    report = run_clifford_witness_search(n_values=n_values, trials_per_row=trials_per_row, seed=seed)
    payload = asdict(report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        if payload["headline_metrics"]["proved_inverse_polynomial_signal_family_count"] == 0:
            upsert_negative_result(
                NegativeResultRecord(
                    id="NEG-DCP-CLIFFORD-FINITE-BIAS-LACKS-UNIFORM-ROBUST-DECODER",
                    source=str(path),
                    claim="Finite nonuniformity from a public-label Clifford measurement establishes a robust DCP algorithm.",
                    reason_invalid=(
                        "The efficient Hamming-weight statistic has no proved uniform inverse-polynomial bias, and arbitrary "
                        "partial contamination plus full-reflection decoding remain unproved."
                    ),
                    lesson="Require an analytic signal bound and adversarial decoder theorem; never promote unrestricted TV alone.",
                    applies_to=[registry_candidate_id, registry_experiment_id],
                    evidence=payload["headline_metrics"],
                )
            )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-DCP-CLIFFORD-WITNESS"
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
                artifacts={"dcp_clifford_witness_search": str(path)},
            )
        )
    return payload
