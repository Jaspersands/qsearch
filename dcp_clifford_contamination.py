"""Adversarial one-bad-register audit for global DCP Clifford witnesses."""

from __future__ import annotations

import json
import math
import random
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

from dcp_clifford_witness_search import (
    _fwht,
    _quadratic_phase_values,
    _schema_neighbors,
    _subset_sum_buckets,
    analyze_clifford_witness_instance,
)
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


DCP_CLIFFORD_CONTAMINATION_PATH = Path("research/phase_workbench/dcp_clifford_contamination.json")
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-CLIFFORD-CONTAMINATION"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class OneBadSchemaScore:
    schema_id: str
    all_good_hamming_tv: float
    worst_one_bad_hamming_tv: float
    mean_one_bad_hamming_tv: float
    worst_bad_coordinate: int
    worst_bad_basis_bit: int
    retained_signal_ratio: float
    log2_shots_for_worst_one_bad_bias: float


@dataclass(frozen=True)
class CliffordContaminationInstance:
    n_bits: int
    register_count: int
    label_seed: int
    schema_scores: list[OneBadSchemaScore]
    best_robust_schema: str
    best_robust_one_bad_hamming_tv: float
    corresponding_all_good_hamming_tv: float
    best_retained_signal_ratio: float
    inverse_polynomial_one_bad_signal: bool


@dataclass(frozen=True)
class CliffordContaminationScalingRow:
    n_bits: int
    register_count: int
    trial_count: int
    mean_best_robust_one_bad_hamming_tv: float
    maximum_best_robust_one_bad_hamming_tv: float
    mean_corresponding_all_good_hamming_tv: float
    mean_best_retained_signal_ratio: float
    inverse_polynomial_one_bad_signal_count: int
    best_robust_schema_histogram: dict[str, int]


@dataclass(frozen=True)
class DCPCliffordContaminationReport:
    created_at: str
    theorem_contract_id: str
    adversarial_model: dict[str, str | int]
    rows: list[CliffordContaminationScalingRow]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _embed_good_mask(reduced_mask: int, good_coordinates: Sequence[int], bad_coordinate: int, bad_bit: int) -> int:
    full_mask = bad_bit << bad_coordinate
    for reduced_index, full_index in enumerate(good_coordinates):
        if (reduced_mask >> reduced_index) & 1:
            full_mask |= 1 << full_index
    return full_mask


def fixed_one_bad_hamming_tv(
    labels: Sequence[int],
    n_bits: int,
    lower_neighbors: Sequence[int],
    bad_coordinate: int,
    bad_bit: int,
) -> float:
    register_count = len(labels)
    if not 0 <= bad_coordinate < register_count or bad_bit not in {0, 1}:
        raise ValueError("invalid bad coordinate or basis bit")
    modulus = 1 << n_bits
    good_coordinates = [index for index in range(register_count) if index != bad_coordinate]
    good_labels = [int(labels[index]) % modulus for index in good_coordinates]
    reduced_buckets = _subset_sum_buckets(good_labels, modulus)
    dimension = 1 << register_count
    good_dimension = 1 << len(good_coordinates)
    phases = _quadratic_phase_values(register_count, lower_neighbors)
    xor_correlations = [0] * dimension
    for bucket in reduced_buckets.values():
        embedded = [
            _embed_good_mask(mask, good_coordinates, bad_coordinate, bad_bit) for mask in bucket
        ]
        for left in embedded:
            left_sign = 1 if phases[left] == 0 else -1
            for right in embedded:
                right_sign = 1 if phases[right] == 0 else -1
                xor_correlations[left ^ right] += left_sign * right_sign
    _fwht(xor_correlations)
    denominator = float(dimension * good_dimension)
    probabilities = [value / denominator for value in xor_correlations]
    uniform = 1.0 / dimension
    good_weight = [0.0] * (register_count + 1)
    uniform_weight = [0.0] * (register_count + 1)
    for outcome, probability in enumerate(probabilities):
        weight = outcome.bit_count()
        good_weight[weight] += probability
        uniform_weight[weight] += uniform
    return 0.5 * sum(abs(good - bad) for good, bad in zip(good_weight, uniform_weight))


def analyze_clifford_contamination_instance(
    n_bits: int,
    labels: Sequence[int],
    label_seed: int = 0,
) -> CliffordContaminationInstance:
    clean = analyze_clifford_witness_instance(n_bits, labels, label_seed)
    clean_by_schema = {score.schema_id: score for score in clean.scores}
    schema_scores: list[OneBadSchemaScore] = []
    for schema_id, neighbors in _schema_neighbors(labels, n_bits):
        bad_scores = [
            (fixed_one_bad_hamming_tv(labels, n_bits, neighbors, coordinate, bit), coordinate, bit)
            for coordinate in range(len(labels))
            for bit in (0, 1)
        ]
        worst_value, worst_coordinate, worst_bit = min(bad_scores)
        clean_value = clean_by_schema[schema_id].hamming_weight_total_variation_distance
        ratio = worst_value / clean_value if clean_value > 0.0 else 0.0
        log2_shots = (
            -1.0
            if worst_value <= 0.0
            else math.log2(2.0 * math.log(6.0)) - 2.0 * math.log2(worst_value)
        )
        schema_scores.append(
            OneBadSchemaScore(
                schema_id=schema_id,
                all_good_hamming_tv=clean_value,
                worst_one_bad_hamming_tv=worst_value,
                mean_one_bad_hamming_tv=sum(value for value, _, _ in bad_scores) / len(bad_scores),
                worst_bad_coordinate=worst_coordinate,
                worst_bad_basis_bit=worst_bit,
                retained_signal_ratio=ratio,
                log2_shots_for_worst_one_bad_bias=log2_shots,
            )
        )
    best = max(schema_scores, key=lambda item: item.worst_one_bad_hamming_tv)
    return CliffordContaminationInstance(
        n_bits=n_bits,
        register_count=len(labels),
        label_seed=label_seed,
        schema_scores=schema_scores,
        best_robust_schema=best.schema_id,
        best_robust_one_bad_hamming_tv=best.worst_one_bad_hamming_tv,
        corresponding_all_good_hamming_tv=best.all_good_hamming_tv,
        best_retained_signal_ratio=best.retained_signal_ratio,
        inverse_polynomial_one_bad_signal=best.worst_one_bad_hamming_tv >= 1.0 / (n_bits * n_bits),
    )


def _finite_log_slope(rows: Sequence[CliffordContaminationScalingRow]) -> float:
    points = [(row.n_bits, row.mean_best_robust_one_bad_hamming_tv) for row in rows if row.mean_best_robust_one_bad_hamming_tv > 0.0]
    if len(points) < 2:
        return 0.0
    mean_x = sum(x for x, _ in points) / len(points)
    mean_y = sum(math.log2(value) for _, value in points) / len(points)
    denominator = sum((x - mean_x) ** 2 for x, _ in points)
    return sum((x - mean_x) * (math.log2(value) - mean_y) for x, value in points) / denominator if denominator else 0.0


def run_clifford_contamination_report(
    n_values: Sequence[int] = (6, 8, 10, 12),
    trials_per_row: int = 3,
    seed: int = 0,
) -> DCPCliffordContaminationReport:
    if trials_per_row < 1:
        raise ValueError("trials_per_row must be positive")
    rows: list[CliffordContaminationScalingRow] = []
    all_instances: list[CliffordContaminationInstance] = []
    for n_index, n_bits in enumerate(n_values):
        modulus = 1 << n_bits
        instances = []
        for trial_index in range(trials_per_row):
            label_seed = seed + 1_000_003 * n_index + trial_index
            rng = random.Random(label_seed)
            labels = [rng.randrange(modulus) for _ in range(n_bits)]
            instances.append(analyze_clifford_contamination_instance(n_bits, labels, label_seed))
        all_instances.extend(instances)
        histogram = Counter(instance.best_robust_schema for instance in instances)
        rows.append(
            CliffordContaminationScalingRow(
                n_bits=n_bits,
                register_count=n_bits,
                trial_count=trials_per_row,
                mean_best_robust_one_bad_hamming_tv=sum(
                    instance.best_robust_one_bad_hamming_tv for instance in instances
                )
                / trials_per_row,
                maximum_best_robust_one_bad_hamming_tv=max(
                    instance.best_robust_one_bad_hamming_tv for instance in instances
                ),
                mean_corresponding_all_good_hamming_tv=sum(
                    instance.corresponding_all_good_hamming_tv for instance in instances
                )
                / trials_per_row,
                mean_best_retained_signal_ratio=sum(instance.best_retained_signal_ratio for instance in instances)
                / trials_per_row,
                inverse_polynomial_one_bad_signal_count=sum(
                    instance.inverse_polynomial_one_bad_signal for instance in instances
                ),
                best_robust_schema_histogram=dict(sorted(histogram.items())),
            )
        )

    metrics: dict[str, int | float] = {
        "scaling_row_count": len(rows),
        "instance_count": len(all_instances),
        "schema_instance_count": sum(len(instance.schema_scores) for instance in all_instances),
        "adversarial_one_bad_case_count": sum(
            2 * instance.register_count * len(instance.schema_scores) for instance in all_instances
        ),
        "inverse_polynomial_one_bad_signal_count": sum(
            instance.inverse_polynomial_one_bad_signal for instance in all_instances
        ),
        "zero_worst_case_signal_count": sum(
            instance.best_robust_one_bad_hamming_tv == 0.0 for instance in all_instances
        ),
        "maximum_robust_one_bad_hamming_tv": max(
            (instance.best_robust_one_bad_hamming_tv for instance in all_instances), default=0.0
        ),
        "finite_log2_robust_tv_slope_per_n": _finite_log_slope(rows),
        "proved_uniform_one_bad_signal_family_count": 0,
        "proved_full_f1_threshold_count": 0,
        "proved_full_decoder_count": 0,
    }
    falsifiers = [
        "The audit hides neither the bad coordinate nor basis value from the adversarial minimization, but the algorithm is not given either one.",
        "Survival under exactly one bad register is weaker than the full per-register f=1 theorem promise.",
        "Finite inverse-polynomial Hamming bias is not a uniform lower bound and does not recover the hidden reflection.",
        "Any schema with exponential sampling cost or no full decoder is rejected even if nonzero bias survives.",
    ]
    claim_gate = {
        "bad_coordinate_exposed_to_algorithm": False,
        "bad_basis_bit_exposed_to_algorithm": False,
        "all_single_bad_cases_enumerated": True,
        "uniform_one_bad_signal_proved": False,
        "full_f1_threshold_proved": False,
        "full_decoder_proved": False,
        "speedup_claim_allowed": False,
        "reason": (
            "The exact audit covers one arbitrary bad basis qubit only. It supplies no uniform signal theorem, full f=1 "
            "contamination threshold, or hidden-reflection decoder."
        ),
    }
    summary = (
        f"Evaluated {int(metrics['adversarial_one_bad_case_count'])} fixed one-bad-coordinate/basis cases across "
        f"{len(all_instances)} label batches. {int(metrics['inverse_polynomial_one_bad_signal_count'])} finite instances "
        "retained at least 1/n^2 Hamming bias, but no uniform one-bad family, full f=1 threshold, or decoder was proved."
    )
    return DCPCliffordContaminationReport(
        created_at=utc_now(),
        theorem_contract_id="THM-REGEV-USVP-TO-DCP-2003",
        adversarial_model={
            "bad_register_count": 1,
            "bad_coordinate": "minimized over every coordinate and hidden from the algorithm",
            "bad_basis_value": "minimized over |0> and |1> and hidden from the algorithm",
            "scope_limit": "diagnostic one-bad threshold only; not the complete f=1 promise",
        },
        rows=rows,
        headline_metrics=metrics,
        claim_gate=claim_gate,
        status="one-bad-clifford-signal-proof-blocked",
        summary=summary,
        falsifiers_triggered=falsifiers,
    )


def write_clifford_contamination_report(
    path: Path = DCP_CLIFFORD_CONTAMINATION_PATH,
    n_values: Sequence[int] = (6, 8, 10, 12),
    trials_per_row: int = 3,
    seed: int = 0,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    report = run_clifford_contamination_report(n_values=n_values, trials_per_row=trials_per_row, seed=seed)
    payload = asdict(report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-CLIFFORD-ONE-BAD-SIGNAL-DOES-NOT-ESTABLISH-F1-DECODER",
                source=str(path),
                claim="A finite Clifford statistic surviving one arbitrary bad register solves the exact f=1 DCP promise.",
                reason_invalid=(
                    "The audit has no uniform lower bound, covers exactly one bad register rather than the full promise, "
                    "and does not recover the hidden reflection."
                ),
                lesson="Extend only surviving schemas to t-bad thresholds and full decoding; kill exponentially decaying statistics.",
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence=payload["headline_metrics"],
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-DCP-CLIFFORD-CONTAMINATION"
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
                artifacts={"dcp_clifford_contamination": str(path)},
            )
        )
    return payload
