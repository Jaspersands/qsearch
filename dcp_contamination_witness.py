"""Exact state-only contamination witnesses for Regev's noisy DCP promise.

After Fourier sampling the second register, a good DCP sample with public label
``k`` is the qubit ``(|0> + omega_N^(k d)|1>)/sqrt(2)``.  A bad sample is a
computational-basis qubit.  This module averages over the unknown reflection
``d`` and computes exact distinguishability certificates without exposing
simulator-only validity flags to the algorithm.
"""

from __future__ import annotations

import json
import math
import random
from collections import Counter
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


DCP_CONTAMINATION_WITNESS_PATH = Path("research/phase_workbench/dcp_contamination_witness.json")
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-CONTAMINATION-WITNESS"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class ContaminationWitnessInstance:
    n_bits: int
    register_count: int
    labels: list[int]
    hilbert_dimension: int
    distinct_subset_sum_count: int
    colliding_subset_pair_count: int
    maximum_subset_sum_bucket: int
    good_vs_uniform_basis_trace_distance: float
    minimum_single_bad_coordinate_trace_distance: float
    maximum_single_bad_coordinate_trace_distance: float
    collision_free_exact_indistinguishability: bool
    information_theoretic_collective_signal: bool
    balanced_dependency_depth: int
    all_good_probability_at_f1_rate: float
    exhaustive_subset_sum_log2_work: float
    meet_in_middle_log2_work: float
    polynomial_time_witness_known: bool


@dataclass(frozen=True)
class ContaminationWitnessScalingRow:
    n_bits: int
    register_count: int
    register_fraction_of_n: float
    trial_count: int
    collision_union_bound: float
    collision_free_trial_count: int
    information_signal_trial_count: int
    mean_good_vs_uniform_basis_trace_distance: float
    maximum_good_vs_uniform_basis_trace_distance: float
    mean_maximum_single_bad_coordinate_trace_distance: float
    balanced_dependency_depth: int
    mean_all_good_probability_at_f1_rate: float
    meet_in_middle_log2_work: float
    polynomial_time_witness_count: int


@dataclass(frozen=True)
class DCPContaminationWitnessReport:
    created_at: str
    theorem_contract_id: str
    ensemble_identity: dict[str, str]
    rows: list[ContaminationWitnessScalingRow]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _subset_sum_counts(labels: Sequence[int], modulus: int) -> Counter[int]:
    sums = [0]
    for label in labels:
        sums += [((value + label) % modulus) for value in sums]
    return Counter(sums)


def _single_bad_trace_distance(labels: Sequence[int], coordinate: int, modulus: int) -> float:
    """Trace distance between the all-good ensemble and dephasing one qubit.

    Randomizing the bad basis bit dephases its coordinate.  The off-diagonal
    block decomposes by subset-sum value, so its singular values are available
    directly from subset-sum bucket multiplicities.
    """

    reduced = [label for index, label in enumerate(labels) if index != coordinate]
    counts = _subset_sum_counts(reduced, modulus)
    shift = labels[coordinate] % modulus
    dimension = 1 << len(labels)
    return sum(math.sqrt(count * counts.get((value - shift) % modulus, 0)) for value, count in counts.items()) / dimension


def analyze_contamination_labels(n_bits: int, labels: Sequence[int]) -> ContaminationWitnessInstance:
    if n_bits < 2:
        raise ValueError("n_bits must be at least two")
    if not labels:
        raise ValueError("at least one Fourier label is required")
    modulus = 1 << n_bits
    normalized = [int(label) % modulus for label in labels]
    counts = _subset_sum_counts(normalized, modulus)
    dimension = 1 << len(normalized)
    distinct = len(counts)
    collision_pairs = sum(count * (count - 1) // 2 for count in counts.values())

    # The hidden-d average is one rank-one all-ones block per equal-subset-sum
    # bucket.  Its trace distance from I/2^m is exactly (2^m-buckets)/2^m.
    good_vs_mixed = (dimension - distinct) / dimension
    coordinate_distances = [
        _single_bad_trace_distance(normalized, coordinate, modulus) for coordinate in range(len(normalized))
    ]
    dependency_depth = int(math.ceil(math.log2(len(normalized)))) if len(normalized) > 1 else 0
    all_good = (1.0 - 1.0 / n_bits) ** len(normalized)
    return ContaminationWitnessInstance(
        n_bits=n_bits,
        register_count=len(normalized),
        labels=normalized,
        hilbert_dimension=dimension,
        distinct_subset_sum_count=distinct,
        colliding_subset_pair_count=collision_pairs,
        maximum_subset_sum_bucket=max(counts.values()),
        good_vs_uniform_basis_trace_distance=good_vs_mixed,
        minimum_single_bad_coordinate_trace_distance=min(coordinate_distances),
        maximum_single_bad_coordinate_trace_distance=max(coordinate_distances),
        collision_free_exact_indistinguishability=distinct == dimension,
        information_theoretic_collective_signal=good_vs_mixed > 0.0,
        balanced_dependency_depth=dependency_depth,
        all_good_probability_at_f1_rate=all_good,
        exhaustive_subset_sum_log2_work=float(len(normalized)),
        meet_in_middle_log2_work=len(normalized) / 2.0,
        polynomial_time_witness_known=False,
    )


def _collision_union_bound(n_bits: int, register_count: int) -> float:
    dimension = 1 << register_count
    modulus = 1 << n_bits
    return min(1.0, dimension * (dimension - 1) / (2.0 * modulus))


def run_contamination_witness_report(
    n_values: Sequence[int] = (8, 10, 12, 14, 16),
    register_fractions: Sequence[float] = (0.25, 0.5, 1.0),
    trials_per_row: int = 8,
    seed: int = 0,
) -> DCPContaminationWitnessReport:
    if trials_per_row < 1:
        raise ValueError("trials_per_row must be positive")
    rows: list[ContaminationWitnessScalingRow] = []
    instances: list[ContaminationWitnessInstance] = []
    for n_index, n_bits in enumerate(n_values):
        if n_bits < 2:
            raise ValueError("all n_values must be at least two")
        modulus = 1 << n_bits
        for fraction_index, fraction in enumerate(register_fractions):
            if fraction <= 0:
                raise ValueError("register fractions must be positive")
            register_count = max(1, int(math.ceil(fraction * n_bits)))
            trial_instances = []
            for trial in range(trials_per_row):
                rng = random.Random(seed + 1_000_003 * n_index + 10_007 * fraction_index + trial)
                labels = [rng.randrange(modulus) for _ in range(register_count)]
                trial_instances.append(analyze_contamination_labels(n_bits, labels))
            instances.extend(trial_instances)
            rows.append(
                ContaminationWitnessScalingRow(
                    n_bits=n_bits,
                    register_count=register_count,
                    register_fraction_of_n=register_count / n_bits,
                    trial_count=trials_per_row,
                    collision_union_bound=_collision_union_bound(n_bits, register_count),
                    collision_free_trial_count=sum(item.collision_free_exact_indistinguishability for item in trial_instances),
                    information_signal_trial_count=sum(item.information_theoretic_collective_signal for item in trial_instances),
                    mean_good_vs_uniform_basis_trace_distance=sum(
                        item.good_vs_uniform_basis_trace_distance for item in trial_instances
                    )
                    / trials_per_row,
                    maximum_good_vs_uniform_basis_trace_distance=max(
                        item.good_vs_uniform_basis_trace_distance for item in trial_instances
                    ),
                    mean_maximum_single_bad_coordinate_trace_distance=sum(
                        item.maximum_single_bad_coordinate_trace_distance for item in trial_instances
                    )
                    / trials_per_row,
                    balanced_dependency_depth=trial_instances[0].balanced_dependency_depth,
                    mean_all_good_probability_at_f1_rate=sum(
                        item.all_good_probability_at_f1_rate for item in trial_instances
                    )
                    / trials_per_row,
                    meet_in_middle_log2_work=register_count / 2.0,
                    polynomial_time_witness_count=sum(item.polynomial_time_witness_known for item in trial_instances),
                )
            )

    collision_free = sum(item.collision_free_exact_indistinguishability for item in instances)
    signal = sum(item.information_theoretic_collective_signal for item in instances)
    linear_rows = [row for row in rows if row.register_count >= row.n_bits]
    metrics: dict[str, int | float] = {
        "row_count": len(rows),
        "trial_count": len(instances),
        "single_register_nonzero_label_trace_distance": 0.0,
        "collision_free_exact_indistinguishability_count": collision_free,
        "information_signal_instance_count": signal,
        "linear_register_signal_row_count": sum(row.information_signal_trial_count > 0 for row in linear_rows),
        "maximum_trace_distance": max((item.good_vs_uniform_basis_trace_distance for item in instances), default=0.0),
        "minimum_linear_register_all_good_probability": min(
            (row.mean_all_good_probability_at_f1_rate for row in linear_rows), default=0.0
        ),
        "maximum_linear_register_dependency_depth": max(
            (row.balanced_dependency_depth for row in linear_rows), default=0
        ),
        "polynomial_time_witness_count": sum(item.polynomial_time_witness_known for item in instances),
        "proved_robust_decoder_count": 0,
    }
    falsifiers = [
        "For every nonzero public label, the hidden-reflection-averaged good single-qubit ensemble is exactly I/2, matching a uniformly randomized bad basis qubit.",
        "Any collision-free batch of Fourier labels has an all-good ensemble exactly equal to the maximally mixed basis-state ensemble, so no state-only measurement can detect contamination on that batch.",
        "Collective distinguishability appears only through modular subset-sum collisions; the implemented exact witness enumerates 2^m subsets and supplies no polynomial-time measurement.",
        "A detectable linear-size batch can have constant all-good probability and logarithmic balanced depth, but this is only an information-theoretic opening, not a DCP decoder.",
    ]
    claim_gate = {
        "simulator_bad_flags_exposed": False,
        "single_register_detector_exists": False,
        "collision_free_batch_detector_exists": False,
        "linear_size_collective_signal_observed": metrics["linear_register_signal_row_count"] > 0,
        "polynomial_time_collective_witness_known": False,
        "adversarial_bad_register_robustness_proved": False,
        "speedup_claim_allowed": False,
        "reason": (
            "The first exact state-only signal is a global subset-sum correlation. No polynomial-time measurement, "
            "adversarial contamination threshold, or full reflection decoder is known."
        ),
    }
    summary = (
        f"Audited {len(instances)} exact hidden-reflection-averaged DCP label batches. "
        f"{collision_free} were exactly indistinguishable from randomized bad basis states; {signal} had a collective "
        "subset-sum signal, but zero polynomial-time witnesses or robust decoders were established."
    )
    return DCPContaminationWitnessReport(
        created_at=utc_now(),
        theorem_contract_id="THM-REGEV-USVP-TO-DCP-2003",
        ensemble_identity={
            "good_batch": (
                "rho_good=2^-m sum_{a,b: sum_i k_i(a_i-b_i)=0 mod N} |a><b| after averaging the unknown reflection d"
            ),
            "uniform_bad_batch": "rho_bad=I/2^m when adversarial bad basis bits are uniformly randomized",
            "collision_free_consequence": "rho_good=rho_bad exactly when all subset sums of the public labels are distinct",
            "single_bad_coordinate": "uniformly randomizing one bad basis bit is dephasing of that coordinate",
        },
        rows=rows,
        headline_metrics=metrics,
        claim_gate=claim_gate,
        status="collective-signal-computationally-blocked",
        summary=summary,
        falsifiers_triggered=falsifiers,
    )


def write_contamination_witness_report(
    path: Path = DCP_CONTAMINATION_WITNESS_PATH,
    n_values: Sequence[int] = (8, 10, 12, 14, 16),
    register_fractions: Sequence[float] = (0.25, 0.5, 1.0),
    trials_per_row: int = 8,
    seed: int = 0,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    report = run_contamination_witness_report(
        n_values=n_values,
        register_fractions=register_fractions,
        trials_per_row=trials_per_row,
        seed=seed,
    )
    payload = asdict(report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-LOCAL-BAD-REGISTER-DETECTION-ENSEMBLE-IDENTITY",
                source=str(path),
                claim="A state-only local measurement can identify arbitrary bad DCP basis registers before the reflection is known.",
                reason_invalid=(
                    "For every nonzero Fourier label, averaging a good phase qubit over the unknown reflection gives I/2. "
                    "An allowed randomized bad basis qubit has the same density operator."
                ),
                lesson="Search for collective common-reflection correlations; do not add a local bad-flag oracle.",
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence={
                    "single_register_trace_distance": 0.0,
                    "simulator_bad_flags_exposed": False,
                },
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-COLLISION-FREE-BATCH-CANNOT-WITNESS-CONTAMINATION",
                source=str(path),
                claim="An arbitrary small batch of public-label DCP qubits contains a state-only contamination witness.",
                reason_invalid=(
                    "When the label subset sums are collision-free, the exact hidden-reflection-averaged good ensemble is "
                    "I/2^m, identical to the uniformly randomized bad basis ensemble."
                ),
                lesson="A viable witness must exploit global modular subset-sum collisions and charge how they are found and measured.",
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence={
                    "collision_free_count": payload["headline_metrics"][
                        "collision_free_exact_indistinguishability_count"
                    ],
                    "trial_count": payload["headline_metrics"]["trial_count"],
                    "polynomial_time_witness_count": 0,
                },
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-DCP-CONTAMINATION-WITNESS"
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
                artifacts={"dcp_contamination_witness": str(path)},
            )
        )
    return payload
