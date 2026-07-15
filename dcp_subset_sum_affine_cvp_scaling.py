"""Source-native scaling audit for marker-aware affine-CVP baselines.

This extends the exact-rational affine Babai attack beyond truth-table sizes.
Independent uniform targets remain the source contract.  Exact legality and
witness multiplicity are computed by meet in the middle in time and memory
``2^(m/2)``, preventing failed decoder runs from being silently counted as
illegal inputs.  Standard and carry-sliced distance, constraint, and binary
defects are retained at every scale.

The audit is deliberately not a theorem.  It can falsify a finite-success
narrative or expose a classical attack that must be beaten, but cannot promote
an empirical slope to inverse-polynomial coverage.
"""

from __future__ import annotations

import json
import math
import random
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

from dcp_subset_sum_affine_cvp_baseline import (
    AffineCVPDiagnostics,
    carry_sliced_affine_babai,
    standard_affine_babai,
)
from dcp_subset_sum_carry_slice_lattice import constrained_low_bits
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


DCP_SUBSET_SUM_AFFINE_CVP_SCALING_PATH = Path(
    "research/classical_baselines/dcp_subset_sum_affine_cvp_scaling.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-SUBSET-SUM-AFFINE-CVP-SCALING"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class AffineCVPScalingTrial:
    n_bits: int
    register_offset: int
    register_count: int
    trial_index: int
    legality_method: str
    exact_legal_witness_count: int
    target_legal: bool
    constrained_low_bits: int
    reachable_carry_count: int
    standard_solved: bool
    carry_sliced_solved: bool
    standard_distance_ratio: float
    carry_sliced_distance_ratio: float
    standard_constraint_norm_squared: int
    carry_sliced_constraint_norm_squared: int
    standard_binary_defect: int
    carry_sliced_binary_defect: int
    standard_diagnostics: AffineCVPDiagnostics
    carry_sliced_diagnostics: AffineCVPDiagnostics


@dataclass(frozen=True)
class AffineCVPScaleSummary:
    n_bits: int
    register_offset: int
    trial_count: int
    legal_trial_count: int
    standard_success_count: int
    carry_sliced_success_count: int
    standard_legal_coverage: float | None
    carry_sliced_legal_coverage: float | None
    mean_standard_distance_ratio: float
    mean_carry_sliced_distance_ratio: float
    mean_standard_binary_defect: float
    mean_carry_sliced_binary_defect: float
    zero_invalid_witnesses_verified: bool
    empirical_row_is_coverage_theorem: bool


@dataclass(frozen=True)
class DCPSubsetSumAffineCVPScalingReport:
    created_at: str
    scaling_contract: dict[str, str]
    rows: list[AffineCVPScaleSummary]
    trials: list[AffineCVPScalingTrial]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def subset_sums_modulus(labels: Sequence[int], modulus: int) -> list[int]:
    sums = [0]
    for label in labels:
        shift = int(label) % modulus
        sums += [(value + shift) % modulus for value in sums]
    return sums


def exact_mitm_witness_count(labels: Sequence[int], target: int, modulus: int) -> int:
    """Count binary witnesses exactly in O(2^(m/2)) time and memory."""
    if modulus <= 0:
        raise ValueError("modulus must be positive")
    middle = len(labels) // 2
    left_counts = Counter(subset_sums_modulus(labels[:middle], modulus))
    right_sums = subset_sums_modulus(labels[middle:], modulus)
    target_mod = int(target) % modulus
    return sum(left_counts[(target_mod - value) % modulus] for value in right_sums)


def exact_mitm_witnesses(
    labels: Sequence[int],
    target: int,
    modulus: int,
    witness_cap: int = 256,
) -> tuple[int, list[list[int]], bool]:
    """Count all witnesses and materialize up to witness_cap exact witnesses."""
    if modulus <= 0 or witness_cap < 1:
        raise ValueError("modulus and witness cap must be positive")
    middle = len(labels) // 2
    left_rows: list[tuple[int, int]] = [(0, 0)]
    for index, label in enumerate(labels[:middle]):
        shift = int(label) % modulus
        left_rows += [
            ((value + shift) % modulus, mask | (1 << index))
            for value, mask in left_rows
        ]
    buckets: dict[int, list[int]] = defaultdict(list)
    for value, mask in left_rows:
        buckets[value].append(mask)

    right_rows: list[tuple[int, int]] = [(0, 0)]
    for index, label in enumerate(labels[middle:]):
        shift = int(label) % modulus
        right_rows += [
            ((value + shift) % modulus, mask | (1 << index))
            for value, mask in right_rows
        ]
    target_mod = int(target) % modulus
    count = 0
    witnesses: list[list[int]] = []
    for right_value, right_mask in right_rows:
        left_masks = buckets.get((target_mod - right_value) % modulus, [])
        count += len(left_masks)
        for left_mask in left_masks:
            if len(witnesses) >= witness_cap:
                continue
            witnesses.append(
                [
                    *((left_mask >> index) & 1 for index in range(middle)),
                    *((right_mask >> index) & 1 for index in range(len(labels) - middle)),
                ]
            )
    return count, witnesses, count > len(witnesses)


def run_affine_cvp_scaling_trial(
    n_bits: int,
    register_offset: int,
    trial_index: int,
    log_multiplier: int,
    embedding_scale: int,
    low_constraint_scale: int,
    lll_delta: float,
    seed: int,
) -> AffineCVPScalingTrial:
    modulus = 1 << n_bits
    register_count = n_bits + register_offset
    rng = random.Random(seed)
    labels = [rng.randrange(modulus) for _ in range(register_count)]
    target = rng.randrange(modulus)
    legal_count = exact_mitm_witness_count(labels, target, modulus)
    standard_witness, standard = standard_affine_babai(
        n_bits, labels, target, embedding_scale, lll_delta
    )
    low_bits = constrained_low_bits(n_bits, log_multiplier)
    sliced_witness, _, carry_count, sliced = carry_sliced_affine_babai(
        n_bits,
        labels,
        target,
        low_bits,
        embedding_scale,
        low_constraint_scale,
        lll_delta,
    )
    if standard_witness is not None and sum(
        label * bit for label, bit in zip(labels, standard_witness)
    ) % modulus != target:
        raise AssertionError("standard affine baseline returned an invalid witness")
    if sliced_witness is not None and sum(
        label * bit for label, bit in zip(labels, sliced_witness)
    ) % modulus != target:
        raise AssertionError("carry-sliced affine baseline returned an invalid witness")
    return AffineCVPScalingTrial(
        n_bits=n_bits,
        register_offset=register_offset,
        register_count=register_count,
        trial_index=trial_index,
        legality_method="exact-meet-in-the-middle",
        exact_legal_witness_count=legal_count,
        target_legal=legal_count > 0,
        constrained_low_bits=low_bits,
        reachable_carry_count=carry_count,
        standard_solved=standard_witness is not None,
        carry_sliced_solved=sliced_witness is not None,
        standard_distance_ratio=standard.distance_squared / standard.witness_radius_squared,
        carry_sliced_distance_ratio=sliced.distance_squared / sliced.witness_radius_squared,
        standard_constraint_norm_squared=standard.constraint_coordinate_norm_squared,
        carry_sliced_constraint_norm_squared=sliced.constraint_coordinate_norm_squared,
        standard_binary_defect=standard.binary_coordinate_defect,
        carry_sliced_binary_defect=sliced.binary_coordinate_defect,
        standard_diagnostics=standard,
        carry_sliced_diagnostics=sliced,
    )


def run_affine_cvp_scaling(
    n_values: Sequence[int] = (16, 20, 24, 28, 32),
    register_offsets: Sequence[int] = (2,),
    trials_per_row: int = 2,
    log_multiplier: int = 1,
    embedding_scale: int = 4,
    low_constraint_scale: int = 4,
    lll_delta: float = 0.75,
    seed: int = 0,
) -> DCPSubsetSumAffineCVPScalingReport:
    if trials_per_row < 1:
        raise ValueError("trials per row must be positive")
    trials = [
        run_affine_cvp_scaling_trial(
            n_bits,
            offset,
            trial_index,
            log_multiplier,
            embedding_scale,
            low_constraint_scale,
            lll_delta,
            seed + 1_000_003 * n_index + 10_007 * offset_index + trial_index,
        )
        for n_index, n_bits in enumerate(n_values)
        for offset_index, offset in enumerate(register_offsets)
        for trial_index in range(trials_per_row)
    ]
    rows: list[AffineCVPScaleSummary] = []
    for n_bits in n_values:
        for offset in register_offsets:
            group = [
                trial
                for trial in trials
                if trial.n_bits == n_bits and trial.register_offset == offset
            ]
            legal = [trial for trial in group if trial.target_legal]
            standard_success = sum(trial.standard_solved for trial in legal)
            sliced_success = sum(trial.carry_sliced_solved for trial in legal)
            rows.append(
                AffineCVPScaleSummary(
                    n_bits=n_bits,
                    register_offset=offset,
                    trial_count=len(group),
                    legal_trial_count=len(legal),
                    standard_success_count=standard_success,
                    carry_sliced_success_count=sliced_success,
                    standard_legal_coverage=(standard_success / len(legal) if legal else None),
                    carry_sliced_legal_coverage=(sliced_success / len(legal) if legal else None),
                    mean_standard_distance_ratio=sum(item.standard_distance_ratio for item in group)
                    / len(group),
                    mean_carry_sliced_distance_ratio=sum(
                        item.carry_sliced_distance_ratio for item in group
                    )
                    / len(group),
                    mean_standard_binary_defect=sum(item.standard_binary_defect for item in group)
                    / len(group),
                    mean_carry_sliced_binary_defect=sum(
                        item.carry_sliced_binary_defect for item in group
                    )
                    / len(group),
                    zero_invalid_witnesses_verified=True,
                    empirical_row_is_coverage_theorem=False,
                )
            )
    tail_n = max(n_values)
    tail = [row for row in rows if row.n_bits == tail_n]
    metrics: dict[str, int | float] = {
        "trial_count": len(trials),
        "row_count": len(rows),
        "exact_mitm_legality_trial_count": len(trials),
        "legal_trial_count": sum(trial.target_legal for trial in trials),
        "standard_legal_success_count": sum(
            trial.standard_solved and trial.target_legal for trial in trials
        ),
        "carry_sliced_legal_success_count": sum(
            trial.carry_sliced_solved and trial.target_legal for trial in trials
        ),
        "tail_standard_success_count": sum(row.standard_success_count for row in tail),
        "tail_carry_sliced_success_count": sum(row.carry_sliced_success_count for row in tail),
        "tail_mean_standard_distance_ratio": sum(row.mean_standard_distance_ratio for row in tail)
        / len(tail),
        "tail_mean_carry_sliced_distance_ratio": sum(
            row.mean_carry_sliced_distance_ratio for row in tail
        )
        / len(tail),
        "maximum_n_bits": tail_n,
        "invalid_witness_count": 0,
        "proved_inverse_polynomial_legal_coverage_count": 0,
        "proved_asymptotic_affine_cvp_advantage_count": 0,
        "polynomial_witness_decoder_count": 0,
    }
    return DCPSubsetSumAffineCVPScalingReport(
        created_at=utc_now(),
        scaling_contract={
            "source": "independent uniform labels and independent uniform targets modulo 2^n",
            "legality": "exact meet-in-the-middle witness count, including failed decoder trials",
            "attack": "exact-rational standard and all-reachable-carry affine Babai",
            "claim_rule": "no empirical row or finite slope is an asymptotic coverage theorem",
        },
        rows=rows,
        trials=trials,
        headline_metrics=metrics,
        claim_gate={
            "source_contract_satisfied": True,
            "exact_legality_known": True,
            "finite_scaling_is_coverage_theorem": False,
            "inverse_polynomial_coverage_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The scaling audit is a source-native classical attack. It can kill a proposed geometry but cannot "
                "establish coverage without an analytic source-conditioned decoding theorem."
            ),
        },
        status="source-native-affine-cvp-scaling-no-coverage-theorem",
        summary=(
            f"Ran {len(trials)} exact-legality affine-CVP trials through n={tail_n}; tail standard/carry successes="
            f"{metrics['tail_standard_success_count']}/{metrics['tail_carry_sliced_success_count']}, tail distance "
            f"ratios={metrics['tail_mean_standard_distance_ratio']:.6g}/"
            f"{metrics['tail_mean_carry_sliced_distance_ratio']:.6g}; no asymptotic coverage theorem."
        ),
        falsifiers_triggered=[
            "Independent uniform targets and failed runs retain exact legality labels.",
            "Any persistent affine Babai success is a classical attack that candidate mechanisms must beat.",
            "Any collapsing success rate falsifies finite-size marker-coset optimism.",
            "Neither outcome is promoted without an analytic coverage theorem.",
        ],
    )


def write_affine_cvp_scaling(
    path: Path = DCP_SUBSET_SUM_AFFINE_CVP_SCALING_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
    **kwargs,
) -> dict:
    payload = asdict(run_affine_cvp_scaling(**kwargs))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-SUBSET-SUM-AFFINE-CVP-FINITE-SCALING-NOT-COVERAGE",
                source=str(path),
                claim="Finite source-native affine-CVP scaling establishes an asymptotic partial solver.",
                reason_invalid=(
                    "Exact legality and held-out scaling remove source bias but still do not prove an "
                    "inverse-polynomial asymptotic coverage lower bound."
                ),
                lesson=(
                    "Use the tail as a classical falsifier and formulate a source-conditioned BDD theorem; never fit a "
                    "speedup claim directly to these rows."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence=payload["headline_metrics"],
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-AFFINE-CVP-SCALING"
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
                artifacts={"dcp_subset_sum_affine_cvp_scaling": str(path)},
            )
        )
    return payload
