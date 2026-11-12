"""Asymptotic obstruction to fixed-order self-dual support certificates.

The finite automorphism workbench succeeds at weight eight for length 48 and
weight ten for length 64.  This module prevents that success from being
extrapolated into a scalable method.

Every binary self-dual code contains the all-ones vector.  Modulo its span, a
uniform self-dual code is a uniform Lagrangian in a symplectic space of
dimension n-2.  Hence a fixed nontrivial even vector belongs to a uniform
self-dual code with probability

    1 / (2^(n/2 - 1) + 1).

The expected number of codewords through fixed weight w is therefore a
polynomial in n times 2^(-n/2), and tends to zero.  Obtaining even linearly
many support vertices requires weight Theta(n); explicit meet-in-the-middle
enumeration at half that order is exponential.

This is an obstruction to the current classical certificate architecture, not
evidence of quantum advantage or a lower bound for code equivalence.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from self_dual_automorphism_workbench import SELF_DUAL_AUTOMORPHISM_PATH
from self_dual_high_order_automorphism_resolver import (
    SELF_DUAL_HIGH_ORDER_AUTOMORPHISM_PATH,
)


SELF_DUAL_FIXED_ORDER_SPARSITY_PATH = Path(
    "research/code_equivalence/self_dual_fixed_order_sparsity_obstruction.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-CODE-SELF-DUAL-FIXED-ORDER-SPARSITY-OBSTRUCTION"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class FixedOrderSparsitySpec:
    lengths: tuple[int, ...] = (32, 48, 64, 80, 96, 128, 160, 192, 256, 384, 512)
    fixed_weights: tuple[int, ...] = (8, 10)


@dataclass(frozen=True)
class SelfDualSparsityScalingRecord:
    length: int
    dimension: int
    expected_supports_weight_8: float
    expected_supports_weight_10: float
    minimum_even_weight_expected_one: int
    minimum_even_weight_expected_length: int
    required_weight_fraction_for_length_expectation: float
    half_order_subset_log2_count: float
    explicit_enumeration_exponential_scale: bool


@dataclass(frozen=True)
class ObservedSupportComparison:
    family_id: str
    length: int
    maximum_weight: int
    instance_count: int
    mean_observed_support_count: float
    ensemble_expected_support_count: float
    observed_to_expected_ratio: float
    interpretation: str


@dataclass(frozen=True)
class SelfDualFixedOrderSparsityReport:
    created_at: str
    spec: FixedOrderSparsitySpec
    theorem: dict[str, Any]
    scaling_records: list[SelfDualSparsityScalingRecord]
    observed_comparisons: list[ObservedSupportComparison]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _read_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text())
    except (json.JSONDecodeError, OSError):
        return fallback


def self_dual_membership_probability(length: int) -> float:
    if length < 4 or length % 2:
        raise ValueError("length must be even and at least four")
    return 1.0 / (2 ** (length // 2 - 1) + 1)


def even_vector_count_through_weight(length: int, maximum_weight: int) -> int:
    if maximum_weight < 0:
        raise ValueError("maximum_weight must be nonnegative")
    return sum(
        math.comb(length, weight)
        for weight in range(2, min(maximum_weight, length - 1) + 1, 2)
    )


def expected_low_weight_support_count(
    length: int,
    maximum_weight: int,
) -> float:
    return (
        even_vector_count_through_weight(length, maximum_weight)
        * self_dual_membership_probability(length)
    )


def minimum_even_weight_for_expectation(
    length: int,
    target: float,
) -> int:
    if target <= 0:
        return 0
    for weight in range(2, length, 2):
        if expected_low_weight_support_count(length, weight) >= target:
            return weight
    return length


def binary_entropy(probability: float) -> float:
    if probability <= 0 or probability >= 1:
        return 0.0
    return (
        -probability * math.log2(probability)
        - (1.0 - probability) * math.log2(1.0 - probability)
    )


def entropy_half_root(iterations: int = 100) -> float:
    lower = 0.0
    upper = 0.5
    for _ in range(iterations):
        middle = (lower + upper) / 2
        if binary_entropy(middle) < 0.5:
            lower = middle
        else:
            upper = middle
    return (lower + upper) / 2


def _log2_subset_count(length: int, maximum_size: int) -> float:
    count = sum(
        math.comb(length, size)
        for size in range(maximum_size + 1)
    )
    return math.log2(max(count, 1))


def _scaling_record(length: int) -> SelfDualSparsityScalingRecord:
    one_weight = minimum_even_weight_for_expectation(length, 1.0)
    length_weight = minimum_even_weight_for_expectation(length, float(length))
    half_order = length_weight // 2
    return SelfDualSparsityScalingRecord(
        length=length,
        dimension=length // 2,
        expected_supports_weight_8=round(
            expected_low_weight_support_count(length, 8), 12
        ),
        expected_supports_weight_10=round(
            expected_low_weight_support_count(length, 10), 12
        ),
        minimum_even_weight_expected_one=one_weight,
        minimum_even_weight_expected_length=length_weight,
        required_weight_fraction_for_length_expectation=round(
            length_weight / length, 9
        ),
        half_order_subset_log2_count=round(
            _log2_subset_count(length, half_order), 6
        ),
        explicit_enumeration_exponential_scale=(
            length >= 128 and half_order >= int(0.04 * length)
        ),
    )


def _observed_comparisons(
    base_path: Path,
    high_order_path: Path,
) -> list[ObservedSupportComparison]:
    base = _read_json(base_path, {})
    high_order = _read_json(high_order_path, {})
    grouped: dict[tuple[str, int, int], list[int]] = {}
    for record in base.get("records", []):
        key = (
            str(record.get("family_id", "unknown-self-dual-family")),
            int(record.get("length", 0) or 0),
            int(
                record.get("low_weight_supports", {}).get(
                    "maximum_weight", 0
                )
                or 0
            ),
        )
        grouped.setdefault(key, []).append(
            int(
                record.get("low_weight_supports", {}).get("support_count", 0)
                or 0
            )
        )
    for record in high_order.get("records", []):
        key = (
            str(record.get("family_id", "unknown-self-dual-family")),
            int(record.get("length", 0) or 0),
            int(
                record.get("high_order_supports", {}).get(
                    "maximum_weight", 0
                )
                or 0
            ),
        )
        grouped.setdefault(key, []).append(
            int(
                record.get("high_order_supports", {}).get("support_count", 0)
                or 0
            )
        )

    comparisons = []
    for (family_id, length, weight), counts in sorted(grouped.items()):
        if not length or not weight or not counts:
            continue
        observed = sum(counts) / len(counts)
        expected = expected_low_weight_support_count(length, weight)
        ratio = observed / expected if expected else 0.0
        comparisons.append(
            ObservedSupportComparison(
                family_id=family_id,
                length=length,
                maximum_weight=weight,
                instance_count=len(counts),
                mean_observed_support_count=round(observed, 6),
                ensemble_expected_support_count=round(expected, 6),
                observed_to_expected_ratio=round(ratio, 6),
                interpretation=(
                    "Observed fixed-weight support density is compared with the "
                    "uniform self-dual ensemble expectation as a calibration, "
                    "not as an independence test or family proof."
                ),
            )
        )
    return comparisons


def run_self_dual_fixed_order_sparsity_obstruction(
    base_path: Path = SELF_DUAL_AUTOMORPHISM_PATH,
    high_order_path: Path = SELF_DUAL_HIGH_ORDER_AUTOMORPHISM_PATH,
    spec: FixedOrderSparsitySpec = FixedOrderSparsitySpec(),
) -> SelfDualFixedOrderSparsityReport:
    scaling = [_scaling_record(length) for length in spec.lengths]
    comparisons = _observed_comparisons(base_path, high_order_path)
    root = entropy_half_root()
    fixed_weight_vanishing_rows = sum(
        record.expected_supports_weight_10 < 1.0 for record in scaling
    )
    linear_weight_rows = sum(
        record.minimum_even_weight_expected_length
        >= 0.08 * record.length
        for record in scaling
    )
    exponential_rows = sum(
        record.explicit_enumeration_exponential_scale for record in scaling
    )
    metrics: dict[str, int | float] = {
        "scaling_length_count": len(scaling),
        "maximum_length": max(spec.lengths, default=0),
        "observed_comparison_count": len(comparisons),
        "weight_10_expected_below_one_length_count": fixed_weight_vanishing_rows,
        "linear_required_weight_length_count": linear_weight_rows,
        "exponential_enumeration_length_count": exponential_rows,
        "entropy_half_relative_weight_threshold": round(root, 9),
        "asymptotic_fixed_order_rigidity_certificate_count": 0,
        "infinite_family_automorphism_theorem_count": 0,
        "collective_measurement_count": 0,
    }
    return SelfDualFixedOrderSparsityReport(
        created_at=utc_now(),
        spec=spec,
        theorem={
            "name": "uniform self-dual fixed-weight sparsity obstruction",
            "membership_probability": (
                "For nontrivial even v, Pr[v in C] = "
                "1/(2^(n/2-1)+1) under the uniform binary self-dual ensemble."
            ),
            "expected_count": (
                "E[A_{<=w}] = sum_{2<=j<=w, j even} binom(n,j) / "
                "(2^(n/2-1)+1)."
            ),
            "fixed_order_consequence": (
                "For fixed w, E[A_{<=w}] = n^O(w) 2^(-n/2) -> 0. The explicit "
                "bounded-support incidence graph is eventually empty with high "
                "probability by Markov's inequality."
            ),
            "linear_order_consequence": (
                f"The entropy threshold H_2(delta)=1/2 is delta={root:.9f}. "
                "Nonvanishing low-weight mass occurs at linear relative weight, "
                "so meet-in-the-middle half-order enumeration is exponential."
            ),
            "scope": (
                "This theorem is exact for the uniform self-dual ensemble and "
                "calibrates the sampled construction. It is not a worst-case "
                "code-equivalence lower bound."
            ),
        },
        scaling_records=scaling,
        observed_comparisons=comparisons,
        headline_metrics=metrics,
        claim_gate={
            "fixed_order_support_rigidity_is_asymptotically_scalable": False,
            "weight_ten_finite_success_proves_family_rigidity": False,
            "classical_certificate_obstruction_is_quantum_advantage": False,
            "implicit_growing_weight_invariants_ruled_out": False,
            "explicit_collective_measurement_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The explicit fixed-order certificate architecture fails "
                "asymptotically, while implicit classical invariants, family "
                "theorems, and collective quantum measurements all remain open."
            ),
        },
        status="fixed-order-self-dual-rigidity-architecture-obstructed",
        summary=(
            f"Weight-ten expected support count drops below one on "
            f"{fixed_weight_vanishing_rows}/{len(scaling)} scaling rows; "
            f"the entropy threshold for nonvanishing mass is relative weight "
            f"{root:.4f}, forcing growing-order explicit enumeration."
        ),
        falsifiers_triggered=[
            "Finite weight-ten success is never extrapolated to a growing family.",
            "The exact ensemble expectation is separated from worst-case code behavior.",
            "An obstruction to one classical certificate is not quantum evidence.",
            "Implicit algebraic growing-weight invariants are not ruled out.",
            "The collective-measurement and decoder obligations remain open.",
        ],
    )


def write_self_dual_fixed_order_sparsity_obstruction(
    path: Path = SELF_DUAL_FIXED_ORDER_SPARSITY_PATH,
    base_path: Path = SELF_DUAL_AUTOMORPHISM_PATH,
    high_order_path: Path = SELF_DUAL_HIGH_ORDER_AUTOMORPHISM_PATH,
    spec: FixedOrderSparsitySpec = FixedOrderSparsitySpec(),
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, Any]:
    payload = asdict(
        run_self_dual_fixed_order_sparsity_obstruction(
            base_path=base_path,
            high_order_path=high_order_path,
            spec=spec,
        )
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-CODE-SELF-DUAL-FIXED-ORDER-RIGIDITY-SCALING",
                source=str(path),
                claim=(
                    "The successful fixed weight-ten support certificate scales "
                    "to a growing random self-dual family."
                ),
                reason_invalid=payload["summary"],
                lesson=(
                    "Replace explicit fixed-order support enumeration with an "
                    "implicit growing-weight invariant or a uniform automorphism "
                    "theorem; do not infer quantum advantage from this obstruction."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence=payload["headline_metrics"],
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-LATEST"
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
                artifacts={
                    "self_dual_fixed_order_sparsity_obstruction": str(path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_self_dual_fixed_order_sparsity_obstruction()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
