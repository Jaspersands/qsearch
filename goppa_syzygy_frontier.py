"""Exact syzygy baseline for the scalable Goppa code-equivalence frontier.

This pass applies the quadratic-relation and first linear-syzygy invariants of
the dual projective system.  It also computes the complete histogram over all
single-coordinate shortenings.  Both are exact permutation invariants.  A
mismatch rejects a pair classically; a collision remains proof debt.

This is a distinguisher/canonicalization baseline, not a solver and not a
classical lower bound.  In particular, a Betti collision cannot be promoted to
evidence that a collective nonabelian measurement is necessary.
"""

from __future__ import annotations

import hashlib
import json
import random
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Sequence

import numpy as np

from code_family_search import gf2_nullspace_basis
from code_schur_filtration import row_basis, shorten
from code_syzygy_invariants import SyzygyInvariant, syzygy_invariant, validate_syzygy_certificate
from goppa_scaling_frontier import GOPPA_SCALING_FRONTIER_PATH
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


GOPPA_SYZYGY_FRONTIER_PATH = Path("research/code_equivalence/goppa_syzygy_frontier.json")
DEFAULT_EXPERIMENT_ID = "EXP-CODE-GOPPA-SYZYGY-FRONTIER"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
LITERATURE_IDS = [
    "mora-tillich-dual-goppa-square-2021",
    "bardet-high-rate-alternant-2023",
    "randriambololona-syzygy-distinguisher-2024",
]


@dataclass(frozen=True)
class ShorteningSyzygyProfile:
    coordinate_count: int
    evaluated_coordinate_count: int
    complete: bool
    invariant_histogram: list[dict[str, Any]]
    digest: str | None


@dataclass(frozen=True)
class GoppaSyzygySignature:
    instance_id: str
    primal_dimension: int
    dual_dimension: int
    whole_dual: SyzygyInvariant
    shortening_profile: ShorteningSyzygyProfile
    exact_signature_digest: str | None
    certificate_issues: list[str]


@dataclass(frozen=True)
class GoppaSyzygyPairAudit:
    id: str
    family_id: str
    left_id: str
    right_id: str
    known_equivalent: bool
    prior_status: str | None
    whole_invariants_match: bool
    shortening_profiles_complete: bool
    shortening_profiles_match: bool | None
    exact_signatures_match: bool | None
    status: str
    interpretation: str


@dataclass(frozen=True)
class GoppaSyzygyFamilyRecord:
    family_id: str
    signatures: list[GoppaSyzygySignature]
    control_audits: list[GoppaSyzygyPairAudit]
    pair_audits: list[GoppaSyzygyPairAudit]
    exact_syzygy_rejection_count: int
    exact_syzygy_collision_count: int
    shortening_cap_pair_count: int
    status: str
    interpretation: str


@dataclass(frozen=True)
class GoppaSyzygyFrontierReport:
    created_at: str
    literature_ids: list[str]
    source_artifact: str
    records: list[GoppaSyzygyFamilyRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _histogram_key(invariant: SyzygyInvariant) -> tuple[int, ...]:
    return invariant.key


def complete_shortening_profile(
    generator: np.ndarray,
    coordinate_limit: int | None = None,
) -> ShorteningSyzygyProfile:
    basis = row_basis(np.asarray(generator, dtype=np.uint8) & 1)
    length = int(basis.shape[1])
    evaluated = length if coordinate_limit is None else min(length, max(0, int(coordinate_limit)))
    counts: Counter[tuple[int, ...]] = Counter()
    for coordinate in range(evaluated):
        counts[_histogram_key(syzygy_invariant(shorten(basis, coordinate)))] += 1
    histogram = [
        {"invariant_key": list(key), "count": int(count)}
        for key, count in sorted(counts.items())
    ]
    complete = evaluated == length
    digest = (
        hashlib.sha256(repr(tuple((tuple(item["invariant_key"]), item["count"]) for item in histogram)).encode("ascii")).hexdigest()[:24]
        if complete
        else None
    )
    return ShorteningSyzygyProfile(
        coordinate_count=length,
        evaluated_coordinate_count=evaluated,
        complete=complete,
        invariant_histogram=histogram,
        digest=digest,
    )


def goppa_syzygy_signature(
    instance: dict[str, Any],
    coordinate_limit: int | None = None,
) -> GoppaSyzygySignature:
    primal = row_basis(np.asarray(instance["generator"], dtype=np.uint8) & 1)
    dual = row_basis(gf2_nullspace_basis(primal))
    whole = syzygy_invariant(dual)
    profile = complete_shortening_profile(dual, coordinate_limit=coordinate_limit)
    issues = validate_syzygy_certificate(whole)
    exact_digest = None
    if not issues and profile.complete:
        exact_digest = hashlib.sha256(
            repr((whole.key, profile.digest)).encode("ascii")
        ).hexdigest()[:24]
    return GoppaSyzygySignature(
        instance_id=str(instance["id"]),
        primal_dimension=int(primal.shape[0]),
        dual_dimension=int(dual.shape[0]),
        whole_dual=whole,
        shortening_profile=profile,
        exact_signature_digest=exact_digest,
        certificate_issues=issues,
    )


def audit_syzygy_pair(
    family_id: str,
    left: GoppaSyzygySignature,
    right: GoppaSyzygySignature,
    *,
    known_equivalent: bool,
    audit_id: str,
    prior_status: str | None = None,
) -> GoppaSyzygyPairAudit:
    whole_match = left.whole_dual.key == right.whole_dual.key
    profiles_complete = left.shortening_profile.complete and right.shortening_profile.complete
    profile_match = (
        left.shortening_profile.digest == right.shortening_profile.digest
        if profiles_complete
        else None
    )
    exact_match = (
        left.exact_signature_digest == right.exact_signature_digest
        if left.exact_signature_digest is not None and right.exact_signature_digest is not None
        else None
    )
    if known_equivalent:
        passed = whole_match and profile_match is not False
        status = (
            "equivalent-control-syzygy-invariants-preserved"
            if passed
            else "control-failure-syzygy-invariant-not-preserved"
        )
        interpretation = (
            "Known coordinate permutation preserves the exact whole-code and complete shortening syzygy signatures."
            if passed
            else "A purported syzygy invariant failed on a known coordinate-permutation control."
        )
    elif not whole_match or (profiles_complete and profile_match is False):
        status = "rejected-by-exact-goppa-syzygy-invariant"
        interpretation = (
            "Exact whole-code or complete single-coordinate-shortening Betti invariants differ, proving the codes are not permutation equivalent."
        )
    elif prior_status == "rejected-by-scalable-goppa-invariant":
        status = "prior-classical-rejection-preserved-syzygy-collision"
        interpretation = (
            "The syzygy invariant collides, but a stronger previously completed exact Goppa invariant already rejects this pair. The pair remains classically resolved."
        )
    elif not profiles_complete:
        status = "goppa-syzygy-shortening-cap-proof-debt"
        interpretation = (
            "Whole-code Betti invariants collide and the shortening profile is incomplete. This is a classical baseline cap, not hardness evidence."
        )
    else:
        status = "goppa-syzygy-invariant-collision-proof-debt"
        interpretation = (
            "The exact whole-code and complete one-coordinate-shortening Betti invariants collide. Stronger shortening depths or support recovery are required; the collision is not quantum evidence."
        )
    return GoppaSyzygyPairAudit(
        id=audit_id,
        family_id=family_id,
        left_id=left.instance_id,
        right_id=right.instance_id,
        known_equivalent=known_equivalent,
        prior_status=prior_status,
        whole_invariants_match=whole_match,
        shortening_profiles_complete=profiles_complete,
        shortening_profiles_match=profile_match,
        exact_signatures_match=exact_match,
        status=status,
        interpretation=interpretation,
    )


def _permuted_instance(instance: dict[str, Any], seed: int) -> dict[str, Any]:
    generator = np.asarray(instance["generator"], dtype=np.uint8)
    permutation = list(range(generator.shape[1]))
    random.Random(seed).shuffle(permutation)
    return {
        "id": f"{instance['id']}-permuted",
        "generator": generator[:, permutation].tolist(),
    }


def run_goppa_syzygy_frontier(
    scaling_path: Path = GOPPA_SCALING_FRONTIER_PATH,
    coordinate_limit: int | None = None,
    recompute_permutation_controls: bool = True,
    audit_resolved_pairs: bool = False,
) -> GoppaSyzygyFrontierReport:
    if not scaling_path.exists():
        raise FileNotFoundError(
            f"missing scalable Goppa artifact {scaling_path}; run `python qsearch.py code-goppa-scaling` first"
        )
    scaling = json.loads(scaling_path.read_text())
    family_records: list[GoppaSyzygyFamilyRecord] = []
    for family_index, source_family in enumerate(scaling["records"]):
        family_id = str(source_family["spec"]["id"])
        frontier_instance_ids = {
            str(audit[side])
            for audit in source_family["collision_audits"]
            if audit["status"] != "rejected-by-scalable-goppa-invariant"
            for side in ("left_id", "right_id")
        }
        if source_family["instances"]:
            frontier_instance_ids.add(str(source_family["instances"][0]["id"]))
        signatures = [
            goppa_syzygy_signature(
                instance,
                coordinate_limit=(
                    coordinate_limit
                    if audit_resolved_pairs or str(instance["id"]) in frontier_instance_ids
                    else 0
                ),
            )
            for instance in source_family["instances"]
        ]
        by_id = {signature.instance_id: signature for signature in signatures}
        pair_audits = []
        for source_audit in source_family["collision_audits"]:
            pair_audits.append(
                audit_syzygy_pair(
                    family_id,
                    by_id[source_audit["left_id"]],
                    by_id[source_audit["right_id"]],
                    known_equivalent=False,
                    audit_id=str(source_audit["id"]),
                    prior_status=str(source_audit["status"]),
                )
            )
        controls: list[GoppaSyzygyPairAudit] = []
        if signatures:
            left = signatures[0]
            if recompute_permutation_controls:
                permuted = goppa_syzygy_signature(
                    _permuted_instance(source_family["instances"][0], 8_000_009 + family_index),
                    coordinate_limit=coordinate_limit,
                )
            else:
                permuted = left
            controls.append(
                audit_syzygy_pair(
                    family_id,
                    left,
                    permuted,
                    known_equivalent=True,
                    audit_id=f"{family_id}-known-permutation-syzygy-control",
                )
            )
        rejections = sum(audit.status == "rejected-by-exact-goppa-syzygy-invariant" for audit in pair_audits)
        collisions = sum(audit.status == "goppa-syzygy-invariant-collision-proof-debt" for audit in pair_audits)
        caps = sum(audit.status == "goppa-syzygy-shortening-cap-proof-debt" for audit in pair_audits)
        control_failures = sum(audit.status.startswith("control-failure") for audit in controls)
        if control_failures:
            status = "rejected-syzygy-pipeline-control-failure"
            interpretation = "The exact-invariant implementation failed a known permutation control."
        elif collisions:
            status = "exact-goppa-syzygy-collision-proof-debt"
            interpretation = f"{collisions} pair(s) survive exact whole-code and one-coordinate-shortening Betti invariants."
        elif caps:
            status = "goppa-syzygy-shortening-cap-proof-debt"
            interpretation = f"{caps} pair(s) remain unresolved because the exact shortening profile was capped."
        else:
            status = "goppa-syzygy-pairs-classically-resolved"
            interpretation = (
                "Every audited unrelated pair is already classically resolved by the prior scalable signature or an exact Betti mismatch."
            )
        family_records.append(
            GoppaSyzygyFamilyRecord(
                family_id=family_id,
                signatures=signatures,
                control_audits=controls,
                pair_audits=pair_audits,
                exact_syzygy_rejection_count=rejections,
                exact_syzygy_collision_count=collisions,
                shortening_cap_pair_count=caps,
                status=status,
                interpretation=interpretation,
            )
        )
    metrics: dict[str, int | float] = {
        "family_count": len(family_records),
        "instance_count": sum(len(record.signatures) for record in family_records),
        "maximum_length": max(
            (signature.whole_dual.length for record in family_records for signature in record.signatures),
            default=0,
        ),
        "exact_whole_syzygy_signature_count": sum(len(record.signatures) for record in family_records),
        "complete_shortening_profile_count": sum(
            signature.shortening_profile.complete
            for record in family_records
            for signature in record.signatures
        ),
        "evaluated_shortening_count": sum(
            signature.shortening_profile.evaluated_coordinate_count
            for record in family_records
            for signature in record.signatures
        ),
        "exact_syzygy_rejection_count": sum(record.exact_syzygy_rejection_count for record in family_records),
        "exact_syzygy_collision_count": sum(record.exact_syzygy_collision_count for record in family_records),
        "prior_classical_rejection_count": sum(
            audit.status == "prior-classical-rejection-preserved-syzygy-collision"
            for record in family_records
            for audit in record.pair_audits
        ),
        "shortening_cap_pair_count": sum(record.shortening_cap_pair_count for record in family_records),
        "control_failure_count": sum(
            audit.status.startswith("control-failure")
            for record in family_records
            for audit in record.control_audits
        ),
        "code_equivalence_solver_count": 0,
        "classical_superpolynomial_lower_bound_count": 0,
        "nonabelian_measurement_necessity_proof_count": 0,
    }
    unresolved = int(metrics["exact_syzygy_collision_count"] + metrics["shortening_cap_pair_count"])
    status = (
        "exact-syzygy-controls-failed"
        if metrics["control_failure_count"]
        else "exact-goppa-syzygy-baseline-complete-proof-debt-only"
    )
    return GoppaSyzygyFrontierReport(
        created_at=utc_now(),
        literature_ids=list(LITERATURE_IDS),
        source_artifact=str(scaling_path),
        records=family_records,
        headline_metrics=metrics,
        claim_gate={
            "exact_gf2_computation": True,
            "complete_profiles_required_for_shortening_rejection": True,
            "known_permutation_controls_pass": metrics["control_failure_count"] == 0,
            "syzygy_collision_is_hardness_evidence": False,
            "family_distinguisher_is_code_equivalence_solver": False,
            "classical_superpolynomial_lower_bound_proved": False,
            "nonabelian_measurement_necessity_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Betti mismatches are polynomial-time classical rejections, while Betti collisions are only proof debt. "
                "No code-equivalence solver, classical lower bound, or collective-measurement necessity theorem follows."
            ),
        },
        status=status,
        summary=(
            f"Computed exact low-degree dual syzygy invariants for {metrics['instance_count']} scalable Goppa codes; "
            f"pair rejections/collisions/caps={metrics['exact_syzygy_rejection_count']}/{unresolved - metrics['shortening_cap_pair_count']}/"
            f"{metrics['shortening_cap_pair_count']}."
        ),
        falsifiers_triggered=[
            "A whole-code or complete shortening-profile Betti mismatch classically rejects permutation equivalence.",
            "A complete Betti collision does not prove equivalence, hardness, or a quantum advantage.",
            "An incomplete shortening profile is a baseline cap and cannot reject a pair.",
            "A family-versus-random distinguisher is not a solver for pairwise code equivalence.",
            "Known coordinate permutations must preserve every exact signature.",
        ],
    )


def write_goppa_syzygy_frontier(
    path: Path = GOPPA_SYZYGY_FRONTIER_PATH,
    scaling_path: Path = GOPPA_SCALING_FRONTIER_PATH,
    coordinate_limit: int | None = None,
    recompute_permutation_controls: bool = True,
    audit_resolved_pairs: bool = False,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, Any]:
    payload = asdict(
        run_goppa_syzygy_frontier(
            scaling_path=scaling_path,
            coordinate_limit=coordinate_limit,
            recompute_permutation_controls=recompute_permutation_controls,
            audit_resolved_pairs=audit_resolved_pairs,
        )
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        for record in payload["records"]:
            for audit in record["pair_audits"]:
                if audit["status"] == "rejected-by-exact-goppa-syzygy-invariant":
                    upsert_negative_result(
                        NegativeResultRecord(
                            id=f"NEG-CODE-GOPPA-SYZYGY-{audit['id'].upper()}",
                            source=str(path),
                            claim=f"{audit['id']} survives the exact low-degree syzygy baseline.",
                            reason_invalid=audit["interpretation"],
                            lesson="Charge exact Betti and complete shortening-profile invariants before designing a collective measurement for a code pair.",
                            applies_to=[registry_candidate_id, registry_experiment_id],
                            evidence=audit,
                        )
                    )
                elif audit["status"] == "goppa-syzygy-invariant-collision-proof-debt":
                    upsert_negative_result(
                        NegativeResultRecord(
                            id=f"NEG-CODE-GOPPA-SYZYGY-COLLISION-{audit['id'].upper()}",
                            source=str(path),
                            claim=f"Low-degree whole-code and one-coordinate-shortening syzygies separate {audit['id']}.",
                            reason_invalid=audit["interpretation"],
                            lesson=(
                                "Do not rerun the same beta_1,2/beta_2,3 baseline on this row. Move to deeper "
                                "shortenings, higher Betti degrees, algebraic support recovery, or canonicalization."
                            ),
                            applies_to=[registry_candidate_id, registry_experiment_id],
                            evidence=audit,
                        )
                    )
        upsert_experiment_result(
            ExperimentResultRecord(
                id=registry_result_id or f"RESULT-{registry_experiment_id}-LATEST",
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=payload["created_at"],
                status=payload["status"],
                summary=payload["summary"],
                metrics=payload["headline_metrics"],
                falsifiers_triggered=payload["falsifiers_triggered"],
                artifacts={"goppa_syzygy_frontier": str(path)},
            )
        )
    return payload


if __name__ == "__main__":
    print(json.dumps(write_goppa_syzygy_frontier()["headline_metrics"], indent=2, sort_keys=True))
