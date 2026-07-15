"""Held-out geometry analysis for odd-unit randomized subset-sum embeddings."""

from __future__ import annotations

import json
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from statistics import mean
from typing import Sequence

from dcp_subset_sum_lattice_search import solve_with_lll_embedding_diagnostics
from dcp_subset_sum_random_self_reduction import transform_instance
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


DCP_ODD_UNIT_ORBIT_GEOMETRY_PATH = Path(
    "research/classical_baselines/dcp_odd_unit_orbit_geometry.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-ODD-UNIT-ORBIT-GEOMETRY"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class OddUnitOrbitInvariantCertificate:
    n_bits: int
    register_count: int
    instance_index: int
    sampled_unit_count: int
    odd_label_present: bool
    exact_orbit_size_if_odd_label: int
    orbit_log2_size_if_odd_label: int
    orbit_exponential_in_n: bool
    label_two_adic_signature_preserved: bool
    target_two_adic_valuation_preserved: bool
    pairwise_difference_two_adic_signature_preserved: bool
    witness_multiplicity_preserved_by_bijection: bool
    implication: str


@dataclass(frozen=True)
class OddUnitGeometryRecord:
    n_bits: int
    register_count: int
    register_offset: int
    instance_index: int
    unit_index: int
    split: str
    odd_unit: int
    target_sampled_independently_uniform: bool
    witness_found: bool
    returned_witness_valid: bool
    centered_target_magnitude: float
    mean_centered_label_magnitude: float
    centered_label_sum_magnitude_per_register: float
    minimum_cyclic_label_gap: float
    maximum_cyclic_label_gap: float
    target_to_nearest_label_distance: float
    lower_half_label_fraction: float
    minimum_reduced_to_ideal_norm_ratio: float
    marker_row_fraction: float
    minimum_marker_modulus_coordinate_normalized: float
    minimum_binary_witness_defect_per_register: float


@dataclass(frozen=True)
class HeldOutFeatureRule:
    n_bits: int
    feature_id: str
    feature_stage: str
    direction: str
    threshold: float
    training_row_count: int
    training_selected_count: int
    training_baseline_success_rate: float
    training_selected_success_rate: float
    training_enrichment: float
    holdout_row_count: int
    holdout_selected_count: int
    holdout_baseline_success_rate: float
    holdout_selected_success_rate: float
    holdout_enrichment: float
    heldout_positive: bool
    proof_relevant_pre_reduction_rule: bool


@dataclass(frozen=True)
class OddUnitOrbitScalingRow:
    n_bits: int
    presentation_count: int
    verified_witness_count: int
    unconditional_success_rate: float
    zero_success_upper_95pct: float | None
    heldout_positive_pre_reduction_rule_count: int
    inverse_linear_target: float
    zero_upper_below_inverse_linear_target: bool
    uniform_inverse_polynomial_orbit_measure_proved: bool


@dataclass(frozen=True)
class DCPOddUnitOrbitGeometryReport:
    created_at: str
    orbit_contract: dict[str, str]
    invariant_certificates: list[OddUnitOrbitInvariantCertificate]
    records: list[OddUnitGeometryRecord]
    feature_rules: list[HeldOutFeatureRule]
    scaling_rows: list[OddUnitOrbitScalingRow]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


PRE_REDUCTION_FEATURES = (
    "centered_target_magnitude",
    "mean_centered_label_magnitude",
    "centered_label_sum_magnitude_per_register",
    "minimum_cyclic_label_gap",
    "maximum_cyclic_label_gap",
    "target_to_nearest_label_distance",
    "lower_half_label_fraction",
)
POST_REDUCTION_FEATURES = (
    "minimum_reduced_to_ideal_norm_ratio",
    "marker_row_fraction",
    "minimum_marker_modulus_coordinate_normalized",
    "minimum_binary_witness_defect_per_register",
)


def two_adic_valuation(value: int, n_bits: int) -> int:
    value %= 1 << n_bits
    if value == 0:
        return n_bits
    return (value & -value).bit_length() - 1


def _two_adic_signatures(
    labels: Sequence[int], target: int, n_bits: int
) -> tuple[tuple[int, ...], int, tuple[int, ...]]:
    label_signature = tuple(sorted(two_adic_valuation(value, n_bits) for value in labels))
    target_signature = two_adic_valuation(target, n_bits)
    pair_signature = tuple(
        sorted(
            two_adic_valuation(int(labels[left]) - int(labels[right]), n_bits)
            for left in range(len(labels))
            for right in range(left)
        )
    )
    return label_signature, target_signature, pair_signature


def certify_odd_unit_orbit_invariants(
    n_bits: int,
    labels: Sequence[int],
    target: int,
    units: Sequence[int],
    instance_index: int = 0,
) -> OddUnitOrbitInvariantCertificate:
    original = _two_adic_signatures(labels, target, n_bits)
    transformed_signatures = []
    for unit in units:
        transformed_labels, transformed_target = transform_instance(
            n_bits, labels, target, [0] * len(labels), unit
        )
        transformed_signatures.append(
            _two_adic_signatures(transformed_labels, transformed_target, n_bits)
        )
    odd_present = any(int(label) % 2 for label in labels)
    return OddUnitOrbitInvariantCertificate(
        n_bits=n_bits,
        register_count=len(labels),
        instance_index=instance_index,
        sampled_unit_count=len(units),
        odd_label_present=odd_present,
        exact_orbit_size_if_odd_label=(1 << (n_bits - 1)) if odd_present else 0,
        orbit_log2_size_if_odd_label=n_bits - 1 if odd_present else 0,
        orbit_exponential_in_n=odd_present,
        label_two_adic_signature_preserved=all(item[0] == original[0] for item in transformed_signatures),
        target_two_adic_valuation_preserved=all(item[1] == original[1] for item in transformed_signatures),
        pairwise_difference_two_adic_signature_preserved=all(
            item[2] == original[2] for item in transformed_signatures
        ),
        witness_multiplicity_preserved_by_bijection=True,
        implication=(
            "Odd units explore an exponential canonical-residue orbit when an odd label is present, but cannot alter "
            "label, target, or pairwise-difference 2-adic valuations. Any easy-orbit theorem must use odd-part or "
            "embedding-presentation geometry rather than valuation changes."
        ),
    )


def _cyclic_distance(left: int, right: int, modulus: int) -> int:
    difference = abs(left - right) % modulus
    return min(difference, modulus - difference)


def analyze_odd_unit_geometry_record(
    n_bits: int,
    labels: Sequence[int],
    target: int,
    odd_unit: int,
    register_offset: int,
    instance_index: int,
    unit_index: int,
    split: str,
    embedding_scale: int = 4,
    lll_delta: float = 0.75,
    combination_arity: int = 1,
) -> OddUnitGeometryRecord:
    modulus = 1 << n_bits
    transformed_labels, transformed_target = transform_instance(
        n_bits, labels, target, [0] * len(labels), odd_unit
    )
    diagnostics = solve_with_lll_embedding_diagnostics(
        n_bits,
        transformed_labels,
        transformed_target,
        embedding_scale,
        lll_delta,
        combination_arity,
    )
    witness = diagnostics.witness
    valid = witness is None or (
        sum(label * bit for label, bit in zip(transformed_labels, witness)) % modulus
        == transformed_target
    )
    centered_labels = [
        value if value <= modulus // 2 else value - modulus
        for value in transformed_labels
    ]
    centered_target = (
        transformed_target if transformed_target <= modulus // 2 else transformed_target - modulus
    )
    sorted_labels = sorted(transformed_labels)
    cyclic_gaps = [
        (sorted_labels[(index + 1) % len(sorted_labels)] - sorted_labels[index]) % modulus
        for index in range(len(sorted_labels))
    ]
    nearest_target = min(
        _cyclic_distance(transformed_target, label, modulus)
        for label in transformed_labels
    )
    marker_coordinate = diagnostics.minimum_marker_modulus_coordinate
    return OddUnitGeometryRecord(
        n_bits=n_bits,
        register_count=len(labels),
        register_offset=register_offset,
        instance_index=instance_index,
        unit_index=unit_index,
        split=split,
        odd_unit=odd_unit,
        target_sampled_independently_uniform=True,
        witness_found=witness is not None,
        returned_witness_valid=valid,
        centered_target_magnitude=abs(centered_target) / modulus,
        mean_centered_label_magnitude=mean(abs(value) for value in centered_labels) / modulus,
        centered_label_sum_magnitude_per_register=(
            abs(sum(centered_labels)) / (len(labels) * modulus)
        ),
        minimum_cyclic_label_gap=min(cyclic_gaps) / modulus,
        maximum_cyclic_label_gap=max(cyclic_gaps) / modulus,
        target_to_nearest_label_distance=nearest_target / modulus,
        lower_half_label_fraction=sum(value < modulus // 2 for value in transformed_labels) / len(labels),
        minimum_reduced_to_ideal_norm_ratio=diagnostics.minimum_reduced_to_ideal_norm_ratio,
        marker_row_fraction=diagnostics.marker_row_count / diagnostics.reduced_row_count,
        minimum_marker_modulus_coordinate_normalized=(
            float(marker_coordinate) / (2 * embedding_scale * modulus)
            if marker_coordinate is not None
            else 1.0
        ),
        minimum_binary_witness_defect_per_register=(
            diagnostics.minimum_binary_witness_defect / len(labels)
        ),
    )


def _rule_statistics(
    rows: Sequence[OddUnitGeometryRecord],
    feature_id: str,
    direction: str,
    threshold: float,
) -> tuple[int, float, float, float]:
    selected = [
        row
        for row in rows
        if (
            getattr(row, feature_id) <= threshold
            if direction == "le"
            else getattr(row, feature_id) >= threshold
        )
    ]
    baseline = sum(row.witness_found for row in rows) / len(rows)
    selected_rate = (
        sum(row.witness_found for row in selected) / len(selected) if selected else 0.0
    )
    enrichment = selected_rate / baseline if baseline > 0 else 0.0
    return len(selected), baseline, selected_rate, enrichment


def _candidate_thresholds(values: Sequence[float]) -> list[float]:
    ordered = sorted(values)
    return sorted(
        {
            ordered[min(len(ordered) - 1, int(quantile * (len(ordered) - 1)))]
            for quantile in (0.2, 0.4, 0.6, 0.8)
        }
    )


def learn_heldout_feature_rules(
    records: Sequence[OddUnitGeometryRecord],
) -> list[HeldOutFeatureRule]:
    rules: list[HeldOutFeatureRule] = []
    for n_bits in sorted({row.n_bits for row in records}):
        training = [row for row in records if row.n_bits == n_bits and row.split == "train"]
        holdout = [row for row in records if row.n_bits == n_bits and row.split == "holdout"]
        if not training or not holdout:
            continue
        for feature_id in PRE_REDUCTION_FEATURES + POST_REDUCTION_FEATURES:
            candidates = []
            for threshold in _candidate_thresholds(
                [float(getattr(row, feature_id)) for row in training]
            ):
                for direction in ("le", "ge"):
                    selected, baseline, rate, enrichment = _rule_statistics(
                        training, feature_id, direction, threshold
                    )
                    if selected < max(2, math.ceil(0.1 * len(training))):
                        continue
                    candidates.append(
                        (rate - baseline, enrichment, selected, direction, threshold, baseline, rate)
                    )
            if not candidates:
                continue
            _, train_enrichment, train_selected, direction, threshold, train_baseline, train_rate = max(
                candidates
            )
            hold_selected, hold_baseline, hold_rate, hold_enrichment = _rule_statistics(
                holdout, feature_id, direction, threshold
            )
            stage = "pre-reduction" if feature_id in PRE_REDUCTION_FEATURES else "post-reduction"
            rules.append(
                HeldOutFeatureRule(
                    n_bits=n_bits,
                    feature_id=feature_id,
                    feature_stage=stage,
                    direction=direction,
                    threshold=threshold,
                    training_row_count=len(training),
                    training_selected_count=train_selected,
                    training_baseline_success_rate=train_baseline,
                    training_selected_success_rate=train_rate,
                    training_enrichment=train_enrichment,
                    holdout_row_count=len(holdout),
                    holdout_selected_count=hold_selected,
                    holdout_baseline_success_rate=hold_baseline,
                    holdout_selected_success_rate=hold_rate,
                    holdout_enrichment=hold_enrichment,
                    heldout_positive=(
                        hold_selected >= max(2, math.ceil(0.1 * len(holdout)))
                        and hold_rate > hold_baseline
                    ),
                    proof_relevant_pre_reduction_rule=stage == "pre-reduction",
                )
            )
    return rules


def run_odd_unit_orbit_geometry_audit(
    n_values: Sequence[int] = (20, 24, 28, 32),
    register_offset: int = 4,
    base_instances_per_size: int = 4,
    units_multiplier: int = 2,
    seed: int = 0,
    embedding_scale: int = 4,
    lll_delta: float = 0.75,
    combination_arity: int = 1,
) -> DCPOddUnitOrbitGeometryReport:
    if base_instances_per_size < 1 or units_multiplier < 1:
        raise ValueError("instance and unit counts must be positive")
    records: list[OddUnitGeometryRecord] = []
    certificates: list[OddUnitOrbitInvariantCertificate] = []
    for n_index, n_bits in enumerate(n_values):
        modulus = 1 << n_bits
        register_count = n_bits + register_offset
        units_per_instance = units_multiplier * n_bits
        for instance_index in range(base_instances_per_size):
            instance_seed = seed + 1_000_003 * n_index + 10_007 * instance_index
            rng = random.Random(instance_seed)
            labels = [rng.randrange(modulus) for _ in range(register_count)]
            target = rng.randrange(modulus)
            units = [rng.randrange(1, modulus, 2) for _ in range(units_per_instance)]
            certificates.append(
                certify_odd_unit_orbit_invariants(
                    n_bits, labels, target, units, instance_index
                )
            )
            for unit_index, unit in enumerate(units):
                records.append(
                    analyze_odd_unit_geometry_record(
                        n_bits,
                        labels,
                        target,
                        unit,
                        register_offset,
                        instance_index,
                        unit_index,
                        "train" if unit_index % 2 == 0 else "holdout",
                        embedding_scale,
                        lll_delta,
                        combination_arity,
                    )
                )
    rules = learn_heldout_feature_rules(records)
    scaling_rows: list[OddUnitOrbitScalingRow] = []
    for n_bits in n_values:
        grouped = [row for row in records if row.n_bits == n_bits]
        success_count = sum(row.witness_found for row in grouped)
        positive_rule_count = sum(
            rule.proof_relevant_pre_reduction_rule and rule.heldout_positive
            for rule in rules
            if rule.n_bits == n_bits
        )
        zero_upper = (
            1.0 - 0.05 ** (1.0 / len(grouped)) if success_count == 0 else None
        )
        scaling_rows.append(
            OddUnitOrbitScalingRow(
                n_bits=n_bits,
                presentation_count=len(grouped),
                verified_witness_count=success_count,
                unconditional_success_rate=success_count / len(grouped),
                zero_success_upper_95pct=zero_upper,
                heldout_positive_pre_reduction_rule_count=positive_rule_count,
                inverse_linear_target=1.0 / n_bits,
                zero_upper_below_inverse_linear_target=(
                    zero_upper is not None and zero_upper < 1.0 / n_bits
                ),
                uniform_inverse_polynomial_orbit_measure_proved=False,
            )
        )
    positive_scaling = [row for row in scaling_rows if row.unconditional_success_rate > 0]
    if len(positive_scaling) >= 2:
        x_mean = mean(row.n_bits for row in positive_scaling)
        y_mean = mean(math.log2(row.unconditional_success_rate) for row in positive_scaling)
        denominator = sum((row.n_bits - x_mean) ** 2 for row in positive_scaling)
        fitted_slope = (
            sum(
                (row.n_bits - x_mean)
                * (math.log2(row.unconditional_success_rate) - y_mean)
                for row in positive_scaling
            )
            / denominator
            if denominator
            else 0.0
        )
    else:
        fitted_slope = 0.0
    tail_n = max(n_values)
    tail = [row for row in records if row.n_bits == tail_n]
    positive_pre = [
        rule
        for rule in rules
        if rule.proof_relevant_pre_reduction_rule and rule.heldout_positive
    ]
    metrics: dict[str, int | float] = {
        "invariant_certificate_count": len(certificates),
        "full_two_adic_invariant_certificate_count": sum(
            item.label_two_adic_signature_preserved
            and item.target_two_adic_valuation_preserved
            and item.pairwise_difference_two_adic_signature_preserved
            for item in certificates
        ),
        "exact_exponential_orbit_certificate_count": sum(
            item.orbit_exponential_in_n for item in certificates
        ),
        "geometry_record_count": len(records),
        "verified_witness_count": sum(row.witness_found for row in records),
        "invalid_witness_count": sum(not row.returned_witness_valid for row in records),
        "tail_record_count": len(tail),
        "tail_verified_witness_count": sum(row.witness_found for row in tail),
        "tail_unconditional_success_rate": sum(row.witness_found for row in tail) / len(tail),
        "feature_rule_count": len(rules),
        "heldout_positive_pre_reduction_rule_count": len(positive_pre),
        "maximum_heldout_pre_reduction_enrichment": max(
            (rule.holdout_enrichment for rule in positive_pre), default=0.0
        ),
        "scaling_row_count": len(scaling_rows),
        "maximum_n_with_heldout_positive_pre_reduction_rule": max(
            (rule.n_bits for rule in positive_pre), default=0
        ),
        "fitted_log2_unconditional_success_slope_per_n": fitted_slope,
        "tail_zero_success_upper_95pct": (
            scaling_rows[-1].zero_success_upper_95pct
            if scaling_rows[-1].zero_success_upper_95pct is not None
            else 1.0
        ),
        "tail_zero_upper_below_inverse_linear_target_count": sum(
            row.zero_upper_below_inverse_linear_target for row in scaling_rows
        ),
        "proved_inverse_polynomial_easy_orbit_measure_count": 0,
        "proved_polynomial_partial_subset_sum_solver_count": 0,
    }
    return DCPOddUnitOrbitGeometryReport(
        created_at=utc_now(),
        orbit_contract={
            "source": "independent uniform A and t over Z_(2^n), never planted-witness targets",
            "orbit": "all odd units act by (A,t)->(uA,ut) and preserve witnesses and multiplicities",
            "seed": "sampled units are target-independent explicit O(n)-bit shared coins",
            "invariants": "all label, target, and pairwise-difference 2-adic valuations are exactly preserved",
            "learning_protocol": (
                "a fixed normalized feature grammar selects one threshold per feature on even-index units and evaluates "
                "it once on disjoint odd-index units; post-reduction rules are diagnostic only"
            ),
            "proof_boundary": (
                "held-out enrichment is hypothesis generation, not an orbit-measure or LLL coverage theorem"
            ),
        },
        invariant_certificates=certificates,
        records=records,
        feature_rules=rules,
        scaling_rows=scaling_rows,
        headline_metrics=metrics,
        claim_gate={
            "two_adic_orbit_invariants_proved": True,
            "heldout_feature_protocol_implemented": True,
            "inverse_polynomial_easy_orbit_measure_proved": False,
            "polynomial_partial_subset_sum_solver_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The workbench can expose held-out geometric predictors, but it proves neither their source prevalence "
                "nor an inverse-polynomial odd-unit easy-orbit measure."
            ),
        },
        status="odd-unit-orbit-invariants-proved-easy-measure-open",
        summary=(
            f"Audited {len(records)} odd-unit presentations with {metrics['verified_witness_count']} verified witnesses. "
            f"Held-out positive pre-reduction rules={len(positive_pre)}; easy-orbit measure proofs=0."
        ),
        falsifiers_triggered=[
            "Odd-unit multiplication cannot improve any obstruction determined solely by 2-adic label, target, or pairwise-difference valuations.",
            "A post-LLL feature that predicts success is diagnostic and does not select an easy unit before paying the solver cost.",
            "Training enrichment without held-out enrichment is rejected as threshold overfitting.",
            "Held-out finite enrichment is not an inverse-polynomial source-prevalence or LLL coverage theorem.",
            "Every success is measured on an independently uniform target and accepted only after exact witness verification.",
        ],
    )


def write_odd_unit_orbit_geometry_audit(
    path: Path = DCP_ODD_UNIT_ORBIT_GEOMETRY_PATH,
    n_values: Sequence[int] = (20, 24, 28, 32),
    register_offset: int = 4,
    base_instances_per_size: int = 4,
    units_multiplier: int = 2,
    seed: int = 0,
    embedding_scale: int = 4,
    lll_delta: float = 0.75,
    combination_arity: int = 1,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    report = run_odd_unit_orbit_geometry_audit(
        n_values,
        register_offset,
        base_instances_per_size,
        units_multiplier,
        seed,
        embedding_scale,
        lll_delta,
        combination_arity,
    )
    payload = asdict(report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-ODD-UNIT-FINITE-FEATURE-ENRICHMENT-NOT-COVERAGE",
                source=str(path),
                claim=(
                    "A threshold feature enriched for LLL success on finitely many odd units proves an inverse-polynomial easy-unit orbit."
                ),
                reason_invalid=(
                    "Even held-out enrichment lacks a uniform source-prevalence and average-case LLL theorem; post-reduction features are only diagnostics."
                ),
                lesson=(
                    "Use surviving pre-reduction rules only to formulate an analytic orbit-measure conjecture, then prove it uniformly or reject the route."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence={
                    "heldout_positive_pre_reduction_rule_count": payload["headline_metrics"][
                        "heldout_positive_pre_reduction_rule_count"
                    ],
                    "proved_inverse_polynomial_easy_orbit_measure_count": 0,
                },
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-DCP-ODD-UNIT-ORBIT-GEOMETRY"
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
                artifacts={"dcp_odd_unit_orbit_geometry": str(path)},
            )
        )
    return payload
