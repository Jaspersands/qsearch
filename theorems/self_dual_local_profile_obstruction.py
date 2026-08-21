"""No-go certificate for bounded local profiles of self-dual codes.

For a binary self-dual code C of length 2k and minimum distance d, let P_S(C)
and Sh_S(C) denote puncturing and shortening on a coordinate set S.  If
|S| < d, then

    dim P_S(C) = k,
    dim Sh_S(C) = k - |S|,
    hull_dim P_S(C) = hull_dim Sh_S(C) = k - |S|.

The reason is structural, not empirical.  Self-duality gives
P_S(C)^perp = Sh_S(C), shortening embeds in puncturing, and d > |S| makes the
restriction map C -> F_2^S surjective while preventing puncturing from losing
dimension.

Consequently every fixed-order puncture/shorten rank-hull signature collapses
on any growing-distance self-dual family.  This module certifies the
hypotheses through order four by an exact zero-sum search on parity-check
columns and verifies the predicted profiles on exhaustive or sampled subsets.
It rules out a baseline family; it does not prove code-equivalence hardness.
"""

from __future__ import annotations

import itertools
import json
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Sequence

import numpy as np

from code_equivalence_workbench import enumerate_codewords
from code_family_search import hull_dimension
from code_schur_filtration import row_basis
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from self_dual_code_boundary_search import (
    SELF_DUAL_CODE_BOUNDARY_PATH,
    puncture_shorten_invariant,
)


SELF_DUAL_LOCAL_OBSTRUCTION_PATH = Path(
    "research/code_equivalence/self_dual_local_profile_obstruction.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-CODE-SELF-DUAL-LOCAL-PROFILE-OBSTRUCTION"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class LocalProfileObstructionSpec:
    maximum_local_order: int = 4
    exhaustive_profile_cap: int = 4_096
    sampled_profile_count: int = 96
    exact_distance_dimension_cap: int = 12
    seed: int = 9_173


@dataclass(frozen=True)
class LowWeightCertificate:
    search_complete_through: int
    minimum_weight_witness_at_most_cap: int | None
    witness_coordinates: tuple[int, ...] | None
    certified_minimum_distance_strictly_greater_than: int | None
    checked_subset_count: int
    cost_model: str


@dataclass(frozen=True)
class LocalProfileInstanceRecord:
    family_id: str
    instance_id: str
    dimension: int
    length: int
    self_dual_certificate_passed: bool
    low_weight_certificate: LowWeightCertificate
    exact_minimum_distance: int | None
    exact_distance_validation_passed: bool | None
    certified_collapse_order: int
    predicted_profiles: tuple[tuple[int, int, int, int, int], ...]
    validated_subset_count: int
    total_subsets_covered_by_theorem: int
    profile_validation_failure_count: int
    status: str
    interpretation: str


@dataclass(frozen=True)
class LocalProfileFamilyRecord:
    family_id: str
    dimension: int
    instance_count: int
    maximum_certified_common_collapse_order: int
    full_order_collapse_instance_count: int
    exact_distance_validation_count: int
    validation_failure_count: int
    local_profile_separator_count: int
    status: str
    interpretation: str


@dataclass(frozen=True)
class SelfDualLocalObstructionReport:
    created_at: str
    theorem: dict[str, Any]
    spec: LocalProfileObstructionSpec
    instance_records: list[LocalProfileInstanceRecord]
    family_records: list[LocalProfileFamilyRecord]
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


def _column_values(generator: np.ndarray) -> list[int]:
    code = row_basis(generator)
    values = []
    for coordinate in range(code.shape[1]):
        value = 0
        for row, bit in enumerate(code[:, coordinate].tolist()):
            if bit:
                value |= 1 << row
        values.append(value)
    return values


def low_weight_zero_sum_certificate(
    generator: np.ndarray,
    maximum_order: int = 4,
) -> LowWeightCertificate:
    """Search exactly for a codeword of weight at most ``maximum_order``.

    A self-dual generator is also a parity-check matrix.  A support is a
    codeword exactly when the XOR of its distinct parity-check columns is zero.
    Enumerating all supports through a fixed order is polynomial in block
    length for that fixed order, but is not a scalable minimum-distance solver
    when the order grows.
    """

    if maximum_order < 1:
        raise ValueError("maximum_order must be positive")
    columns = _column_values(generator)
    checked = 0
    for order in range(1, maximum_order + 1):
        for coordinates in itertools.combinations(range(len(columns)), order):
            checked += 1
            total = 0
            for coordinate in coordinates:
                total ^= columns[coordinate]
            if total == 0:
                return LowWeightCertificate(
                    search_complete_through=maximum_order,
                    minimum_weight_witness_at_most_cap=order,
                    witness_coordinates=tuple(coordinates),
                    certified_minimum_distance_strictly_greater_than=None,
                    checked_subset_count=checked,
                    cost_model=(
                        f"Exact distinct-column zero-sum enumeration through order {maximum_order}; "
                        f"O(n^{maximum_order}) for fixed order."
                    ),
                )
    return LowWeightCertificate(
        search_complete_through=maximum_order,
        minimum_weight_witness_at_most_cap=None,
        witness_coordinates=None,
        certified_minimum_distance_strictly_greater_than=maximum_order,
        checked_subset_count=checked,
        cost_model=(
            f"Exact distinct-column zero-sum enumeration through order {maximum_order}; "
            f"O(n^{maximum_order}) for fixed order."
        ),
    )


def exact_minimum_distance(generator: np.ndarray) -> int:
    words = enumerate_codewords(row_basis(generator))
    nonzero = words[np.any(words, axis=1)]
    if not len(nonzero):
        raise ValueError("zero-dimensional code has no nonzero minimum distance")
    return int(nonzero.sum(axis=1).min())


def _self_dual(generator: np.ndarray) -> bool:
    code = row_basis(generator)
    return (
        code.shape[1] == 2 * code.shape[0]
        and not bool(np.any((code @ code.T) & 1))
        and hull_dimension(code) == code.shape[0]
    )


def _validation_subsets(
    length: int,
    order: int,
    cap: int,
    sample_count: int,
    rng: random.Random,
) -> list[tuple[int, ...]]:
    total = math.comb(length, order)
    if total <= cap:
        return list(itertools.combinations(range(length), order))
    selected: set[tuple[int, ...]] = set()
    while len(selected) < min(sample_count, total):
        selected.add(tuple(sorted(rng.sample(range(length), order))))
    return sorted(selected)


def audit_instance(
    family_id: str,
    instance: dict[str, Any],
    spec: LocalProfileObstructionSpec,
) -> LocalProfileInstanceRecord:
    generator = np.asarray(instance["generator"], dtype=np.uint8)
    dimension = int(generator.shape[0])
    length = int(generator.shape[1])
    self_dual = _self_dual(generator)
    certificate = low_weight_zero_sum_certificate(generator, spec.maximum_local_order)
    witness = certificate.minimum_weight_witness_at_most_cap
    collapse_order = min(spec.maximum_local_order, (witness - 1) if witness is not None else spec.maximum_local_order)
    exact_distance = (
        exact_minimum_distance(generator)
        if dimension <= spec.exact_distance_dimension_cap
        else None
    )
    exact_validation = None
    if exact_distance is not None:
        exact_validation = (
            (witness == exact_distance)
            if witness is not None
            else exact_distance > spec.maximum_local_order
        )

    rng = random.Random(spec.seed + sum(ord(char) for char in str(instance.get("id", ""))))
    predicted = []
    checked = 0
    covered = 0
    failures = 0
    for order in range(1, collapse_order + 1):
        expected = (dimension, dimension - order, dimension - order, dimension - order)
        predicted.append((order, *expected))
        covered += math.comb(length, order)
        for coordinates in _validation_subsets(
            length,
            order,
            spec.exhaustive_profile_cap,
            spec.sampled_profile_count,
            rng,
        ):
            checked += 1
            if puncture_shorten_invariant(generator, coordinates) != expected:
                failures += 1
    passed = self_dual and failures == 0 and exact_validation is not False
    return LocalProfileInstanceRecord(
        family_id=family_id,
        instance_id=str(instance.get("id", "unknown-self-dual-instance")),
        dimension=dimension,
        length=length,
        self_dual_certificate_passed=self_dual,
        low_weight_certificate=certificate,
        exact_minimum_distance=exact_distance,
        exact_distance_validation_passed=exact_validation,
        certified_collapse_order=collapse_order,
        predicted_profiles=tuple(predicted),
        validated_subset_count=checked,
        total_subsets_covered_by_theorem=covered,
        profile_validation_failure_count=failures,
        status=(
            f"proved-local-profile-collapse-through-order-{collapse_order}"
            if passed
            else "rejected-local-profile-theorem-control-failure"
        ),
        interpretation=(
            f"Self-duality and the certified distance bound force every puncture/shorten rank-hull profile through "
            f"order {collapse_order}; matching local signatures carry no distinguishing information."
            if passed
            else "A theorem hypothesis or direct profile control failed; do not use this obstruction certificate."
        ),
    )


def run_self_dual_local_obstruction(
    source_path: Path = SELF_DUAL_CODE_BOUNDARY_PATH,
    spec: LocalProfileObstructionSpec = LocalProfileObstructionSpec(),
) -> SelfDualLocalObstructionReport:
    source = _read_json(source_path, {})
    instance_records = []
    family_records = []
    for family in source.get("family_records", []):
        family_id = str(family.get("spec", {}).get("id", "unknown-self-dual-family"))
        records = [audit_instance(family_id, instance, spec) for instance in family.get("instances", [])]
        instance_records.extend(records)
        common_order = min((record.certified_collapse_order for record in records), default=0)
        full_order = sum(record.certified_collapse_order == spec.maximum_local_order for record in records)
        failures = sum(
            record.profile_validation_failure_count
            + (not record.self_dual_certificate_passed)
            + (record.exact_distance_validation_passed is False)
            for record in records
        )
        family_records.append(
            LocalProfileFamilyRecord(
                family_id=family_id,
                dimension=int(family.get("spec", {}).get("dimension", 0) or 0),
                instance_count=len(records),
                maximum_certified_common_collapse_order=common_order,
                full_order_collapse_instance_count=full_order,
                exact_distance_validation_count=sum(record.exact_minimum_distance is not None for record in records),
                validation_failure_count=failures,
                local_profile_separator_count=0 if records and failures == 0 else failures,
                status=(
                    f"bounded-local-profile-obstruction-proof-debt-through-order-{common_order}"
                    if records and failures == 0
                    else "local-profile-obstruction-control-failure"
                ),
                interpretation=(
                    f"Every instance in the family has forced local rank-hull profiles through common order {common_order}."
                    if records and failures == 0
                    else "The local-profile obstruction was not certified for every family instance."
                ),
            )
        )
    metrics: dict[str, int | float] = {
        "family_count": len(family_records),
        "instance_count": len(instance_records),
        "maximum_dimension": max((record.dimension for record in instance_records), default=0),
        "distance_greater_than_maximum_order_count": sum(
            record.low_weight_certificate.certified_minimum_distance_strictly_greater_than
            == spec.maximum_local_order
            for record in instance_records
        ),
        "full_order_collapse_instance_count": sum(
            record.certified_collapse_order == spec.maximum_local_order for record in instance_records
        ),
        "full_order_collapse_family_count": sum(
            record.maximum_certified_common_collapse_order == spec.maximum_local_order
            for record in family_records
        ),
        "exact_distance_validation_count": sum(
            record.exact_minimum_distance is not None for record in instance_records
        ),
        "profile_validation_subset_count": sum(record.validated_subset_count for record in instance_records),
        "theorem_covered_subset_count": sum(record.total_subsets_covered_by_theorem for record in instance_records),
        "theorem_control_failure_count": sum(record.validation_failure_count for record in family_records),
        "local_profile_separator_count": sum(record.local_profile_separator_count for record in family_records),
        "global_polynomial_canonicalization_count": 0,
        "classical_superpolynomial_lower_bound_count": 0,
        "nonabelian_measurement_necessity_count": 0,
    }
    return SelfDualLocalObstructionReport(
        created_at=utc_now(),
        theorem={
            "name": "self-dual puncture/shorten local-profile collapse",
            "hypotheses": [
                "C is a binary self-dual [2k,k,d] code.",
                "S is a coordinate set with |S| < d.",
            ],
            "conclusions": [
                "dim puncture_S(C) = k.",
                "dim shorten_S(C) = k - |S|.",
                "hull_dim puncture_S(C) = hull_dim shorten_S(C) = k - |S|.",
            ],
            "proof_steps": [
                "Minimum distance d>|S| prevents a nonzero codeword from vanishing outside S, so puncturing preserves dimension.",
                "Dual distance equals d by self-duality, so restriction to S has full rank and shortening has dimension k-|S|.",
                "Duality gives puncture_S(C)^perp = shorten_S(C) and shorten_S(C)^perp = puncture_S(C).",
                "Shortening embeds in puncturing, hence it is exactly the hull of both codes.",
            ],
            "scope": (
                "Rules out bounded-coordinate puncture/shorten dimension and hull profiles below minimum distance. "
                "It does not rule out global canonicalization, growing-order invariants, weight enumerators, "
                "automorphism recovery, or graph-isomorphism reductions."
            ),
        },
        spec=spec,
        instance_records=instance_records,
        family_records=family_records,
        headline_metrics=metrics,
        claim_gate={
            "theorem_controls_pass": metrics["theorem_control_failure_count"] == 0,
            "bounded_local_profile_collisions_are_hardness_evidence": False,
            "fixed_order_zero_sum_search_is_minimum_distance_algorithm": False,
            "global_classical_canonicalization_exhausted": False,
            "classical_superpolynomial_lower_bound_proved": False,
            "nonabelian_measurement_necessity_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The observed local-profile collisions are forced by self-duality and distance. They remove a weak "
                "baseline rather than support code-equivalence hardness."
            ),
        },
        status="self-dual-bounded-local-profiles-structurally-obstructed",
        summary=(
            f"Certified {metrics['full_order_collapse_instance_count']}/{metrics['instance_count']} instances and "
            f"{metrics['full_order_collapse_family_count']}/{metrics['family_count']} families through local order "
            f"{spec.maximum_local_order}; theorem controls failed on {metrics['theorem_control_failure_count']} family rows."
        ),
        falsifiers_triggered=[
            "A self-duality or distance-certificate failure invalidates the theorem on that instance.",
            "Any directly computed local profile that differs from the theorem prediction invalidates the implementation.",
            "Exact small-code minimum distance must agree with the fixed-order zero-sum witness.",
            "Forced local-profile collisions are negative evidence against bounded-local invariant search, not hardness evidence.",
            "Fixed-order zero-sum enumeration is not represented as a general minimum-distance algorithm.",
            "The theorem does not close global canonicalization, growing-order signatures, or graph-isomorphism reductions.",
        ],
    )


def write_self_dual_local_obstruction(
    path: Path = SELF_DUAL_LOCAL_OBSTRUCTION_PATH,
    source_path: Path = SELF_DUAL_CODE_BOUNDARY_PATH,
    spec: LocalProfileObstructionSpec = LocalProfileObstructionSpec(),
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, Any]:
    payload = asdict(run_self_dual_local_obstruction(source_path=source_path, spec=spec))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_self_dual_local_obstruction()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
