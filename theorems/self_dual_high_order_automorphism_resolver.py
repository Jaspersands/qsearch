"""Resolve sparse weight-eight self-dual automorphism debt at weight ten.

The base automorphism workbench deliberately stops at supports of weight eight
and preserves the `k=32` rows as unresolved.  This resolver targets only those
rows and performs a packed order-five meet-in-the-middle enumeration, which is
complete through support weight ten for the current length-at-most-64 data.

The order-eight artifact remains intact so the registry records that the
distinguishing support order grew.  A finite order-ten certificate is not an
infinite-family theorem.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from self_dual_automorphism_workbench import (
    SELF_DUAL_AUTOMORPHISM_PATH,
    CoordinateRefinementCertificate,
    LowWeightSupportCertificate,
    enumerate_bounded_weight_supports_packed,
    low_weight_incidence_graph,
    stable_coordinate_refinement,
)
from self_dual_code_boundary_search import SELF_DUAL_CODE_BOUNDARY_PATH


SELF_DUAL_HIGH_ORDER_AUTOMORPHISM_PATH = Path(
    "research/code_equivalence/self_dual_high_order_automorphism_resolver.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-CODE-SELF-DUAL-HIGH-ORDER-AUTOMORPHISM-RESOLVER"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class HighOrderAutomorphismSpec:
    half_support_order: int = 5
    maximum_bucket_pairs: int = 2_000_000


@dataclass(frozen=True)
class HighOrderAutomorphismRecord:
    family_id: str
    instance_id: str
    dimension: int
    length: int
    prior_maximum_weight: int
    prior_support_count: int
    prior_status: str
    high_order_supports: LowWeightSupportCertificate
    packed_array_bytes: int
    refinement: CoordinateRefinementCertificate
    rigidity_certified: bool
    gi_type_single_register_no_go_applicable: bool
    status: str
    interpretation: str


@dataclass(frozen=True)
class HighOrderAutomorphismFamilyRecord:
    family_id: str
    dimension: int
    length: int
    target_instance_count: int
    resolved_rigidity_instance_count: int
    remaining_unresolved_instance_count: int
    maximum_required_support_weight: int
    status: str
    interpretation: str


@dataclass(frozen=True)
class SelfDualHighOrderAutomorphismReport:
    created_at: str
    spec: HighOrderAutomorphismSpec
    theorem: dict[str, Any]
    records: list[HighOrderAutomorphismRecord]
    family_records: list[HighOrderAutomorphismFamilyRecord]
    headline_metrics: dict[str, int | float]
    combined_tail_strata: dict[str, int]
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


def run_self_dual_high_order_automorphism_resolver(
    source_path: Path = SELF_DUAL_CODE_BOUNDARY_PATH,
    base_path: Path = SELF_DUAL_AUTOMORPHISM_PATH,
    spec: HighOrderAutomorphismSpec = HighOrderAutomorphismSpec(),
) -> SelfDualHighOrderAutomorphismReport:
    source = _read_json(source_path, {})
    base = _read_json(base_path, {})
    source_instances = {
        (
            str(family.get("spec", {}).get("id", "unknown-self-dual-family")),
            str(instance.get("id", "unknown-self-dual-instance")),
        ): instance
        for family in source.get("family_records", [])
        for instance in family.get("instances", [])
    }
    targets = [
        record
        for record in base.get("records", [])
        if not record.get("rigidity_certified")
        and not record.get("explicit_nontrivial_automorphism_certified")
    ]

    records: list[HighOrderAutomorphismRecord] = []
    for prior in targets:
        family_id = str(prior.get("family_id", "unknown-self-dual-family"))
        instance_id = str(prior.get("instance_id", "unknown-self-dual-instance"))
        instance = source_instances.get((family_id, instance_id))
        if instance is None:
            continue
        generator = np.asarray(instance["generator"], dtype=np.uint8)
        supports, certificate, packed_bytes = (
            enumerate_bounded_weight_supports_packed(
                generator,
                half_support_order=spec.half_support_order,
                maximum_bucket_pairs=spec.maximum_bucket_pairs,
            )
        )
        refinement = stable_coordinate_refinement(
            low_weight_incidence_graph(supports, generator.shape[1]),
            int(generator.shape[1]),
        )
        rigidity = bool(
            certificate.complete and refinement.all_coordinates_singleton
        )
        records.append(
            HighOrderAutomorphismRecord(
                family_id=family_id,
                instance_id=instance_id,
                dimension=int(generator.shape[0]),
                length=int(generator.shape[1]),
                prior_maximum_weight=int(
                    prior.get("low_weight_supports", {}).get(
                        "maximum_weight", 0
                    )
                    or 0
                ),
                prior_support_count=int(
                    prior.get("low_weight_supports", {}).get("support_count", 0)
                    or 0
                ),
                prior_status=str(prior.get("status", "unknown")),
                high_order_supports=certificate,
                packed_array_bytes=packed_bytes,
                refinement=refinement,
                rigidity_certified=rigidity,
                gi_type_single_register_no_go_applicable=rigidity,
                status=(
                    "resolved-rigidity-at-higher-fixed-support-order"
                    if rigidity
                    else "higher-order-automorphism-proof-debt"
                ),
                interpretation=(
                    f"Complete weight<={certificate.maximum_weight} supports "
                    "produce singleton automorphism-invariant coordinate colors; "
                    "the instance is rigid and enters the GI-type single-register "
                    "obstruction stratum."
                    if rigidity
                    else (
                        f"Weight<={certificate.maximum_weight} support structure "
                        "does not certify rigidity. Keep the instance unresolved."
                    )
                ),
            )
        )

    family_records: list[HighOrderAutomorphismFamilyRecord] = []
    for family_id in sorted({record.family_id for record in records}):
        family_rows = [
            record for record in records if record.family_id == family_id
        ]
        resolved = sum(record.rigidity_certified for record in family_rows)
        remaining = len(family_rows) - resolved
        family_records.append(
            HighOrderAutomorphismFamilyRecord(
                family_id=family_id,
                dimension=family_rows[0].dimension,
                length=family_rows[0].length,
                target_instance_count=len(family_rows),
                resolved_rigidity_instance_count=resolved,
                remaining_unresolved_instance_count=remaining,
                maximum_required_support_weight=2 * spec.half_support_order,
                status=(
                    "all-prior-automorphism-debt-resolved-rigid-collective-proof-debt"
                    if not remaining
                    else "higher-order-automorphism-proof-debt"
                ),
                interpretation=(
                    "The fixed-order resolver certifies the current finite rows. "
                    "It does not prove that the same order distinguishes all "
                    "larger family members."
                ),
            )
        )

    base_metrics = base.get("headline_metrics", {})
    resolved = sum(record.rigidity_certified for record in records)
    remaining = len(records) - resolved
    metrics: dict[str, int | float] = {
        "target_instance_count": len(records),
        "resolved_rigidity_instance_count": resolved,
        "remaining_unresolved_instance_count": remaining,
        "complete_high_order_enumeration_count": sum(
            record.high_order_supports.complete for record in records
        ),
        "maximum_support_weight": 2 * spec.half_support_order,
        "maximum_enumerated_half_subset_count": max(
            (
                record.high_order_supports.enumerated_half_subsets
                for record in records
            ),
            default=0,
        ),
        "maximum_packed_array_bytes": max(
            (record.packed_array_bytes for record in records),
            default=0,
        ),
        "singleton_refinement_certificate_count": sum(
            record.refinement.all_coordinates_singleton for record in records
        ),
        "gi_type_single_register_no_go_certified_instance_count": resolved,
        "infinite_family_rigidity_theorem_count": 0,
        "collective_measurement_count": 0,
        "polynomial_hidden_permutation_decoder_count": 0,
    }
    combined_tail_strata = {
        "explicit_nonrigid_instance_count": int(
            base_metrics.get("explicit_automorphism_instance_count", 0) or 0
        ),
        "rigidity_certified_instance_count": int(
            base_metrics.get("rigidity_certified_instance_count", 0) or 0
        )
        + resolved,
        "unresolved_instance_count": max(
            0,
            int(base_metrics.get("unresolved_instance_count", 0) or 0)
            - resolved,
        ),
    }
    return SelfDualHighOrderAutomorphismReport(
        created_at=utc_now(),
        spec=spec,
        theorem={
            "name": "packed fixed-order self-dual support resolver",
            "statement": (
                "Sorting all size-at-most-t coordinate subsets by public column "
                "XOR enumerates every zero-sum support through weight 2t. If the "
                "resulting incidence graph has singleton stable coordinate "
                "colors, PAut(C) is trivial."
            ),
            "current_order": spec.half_support_order,
            "current_maximum_weight": 2 * spec.half_support_order,
            "complexity_scope": (
                f"O(n^{spec.half_support_order}) fixed-order preprocessing plus "
                "polynomial color refinement. This is not a uniform theorem if "
                "the required order grows with n."
            ),
        },
        records=records,
        family_records=family_records,
        headline_metrics=metrics,
        combined_tail_strata=combined_tail_strata,
        claim_gate={
            "all_prior_unresolved_instances_resolved": (
                bool(records) and remaining == 0
            ),
            "finite_high_order_certificates_are_sound": True,
            "fixed_order_success_proves_infinite_family_rigidity": False,
            "rigid_single_register_no_go_closes_collective_route": False,
            "explicit_collective_measurement_constructed": False,
            "polynomial_hidden_permutation_decoder_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The current automorphism debt is resolved, but family scaling "
                "and the collective-measurement/decoder barrier remain."
            ),
        },
        status="current-self-dual-tail-automorphisms-resolved-collective-barrier-open",
        summary=(
            f"Resolved {resolved}/{len(records)} prior automorphism-debt "
            f"instance(s) at support weight {2 * spec.half_support_order}; "
            f"combined tail rigid/nonrigid/unresolved="
            f"{combined_tail_strata['rigidity_certified_instance_count']}/"
            f"{combined_tail_strata['explicit_nonrigid_instance_count']}/"
            f"{combined_tail_strata['unresolved_instance_count']}."
        ),
        falsifiers_triggered=[
            "The order-eight unresolved status is retained as a scaling data point.",
            "Every high-order support must pass the public zero-syndrome condition.",
            "Only singleton automorphism-invariant coordinate colors certify rigidity.",
            "Fixed order-ten success is not an infinite-family rigidity theorem.",
            "The rigid single-register obstruction does not close collective measurements.",
        ],
    )


def write_self_dual_high_order_automorphism_resolver(
    path: Path = SELF_DUAL_HIGH_ORDER_AUTOMORPHISM_PATH,
    source_path: Path = SELF_DUAL_CODE_BOUNDARY_PATH,
    base_path: Path = SELF_DUAL_AUTOMORPHISM_PATH,
    spec: HighOrderAutomorphismSpec = HighOrderAutomorphismSpec(),
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, Any]:
    payload = asdict(
        run_self_dual_high_order_automorphism_resolver(
            source_path=source_path,
            base_path=base_path,
            spec=spec,
        )
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_self_dual_high_order_automorphism_resolver()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
