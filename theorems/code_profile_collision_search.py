"""Search for code-equivalence collisions that survive coordinate profiles.

The earlier code-family search collided only weak invariants and was
immediately killed by support-splitting/profile canonicalization.  This module
raises the search bar: it buckets random full-rank binary codes by their full
coordinate-refinement profile multiset, then attacks every collision with the
profile-pruned canonicalization baseline.

Equivalent collisions are controls.  Non-equivalent rows rejected by canonical
forms are negative results.  Rows skipped only because the assignment cap is too
small become proof debt, never positive evidence.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, is_dataclass
from pathlib import Path
from typing import Any

import numpy as np

from code_canonicalization_baseline import audit_code_canonicalization_pair
from code_equivalence_workbench import codeword_int_set
from code_family_search import coordinate_refinement_profiles, random_full_rank_generator
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


CODE_EQUIVALENCE_DIR = Path("research/code_equivalence")
CODE_PROFILE_COLLISION_SEARCH_PATH = CODE_EQUIVALENCE_DIR / "code_profile_collision_search.json"


@dataclass(frozen=True)
class ProfileCollisionSearchSpec:
    id: str
    length: int
    dimension: int
    max_trials: int
    max_collisions: int
    seed: int


@dataclass(frozen=True)
class ProfileCollisionAudit:
    id: str
    trial: int
    profile_bucket_size: int
    canonical_status: str
    canonical_equal: bool | None
    estimated_assignments: int
    interpretation: str


@dataclass(frozen=True)
class ProfileCollisionSearchRecord:
    spec: ProfileCollisionSearchSpec
    trials_run: int
    profile_key_count: int
    profile_collision_count: int
    equivalent_collision_count: int
    rejected_collision_count: int
    proof_debt_collision_count: int
    max_profile_bucket_size: int
    collision_audits: list[ProfileCollisionAudit]
    status: str
    interpretation: str


@dataclass(frozen=True)
class ProfileCollisionSearchReport:
    created_at: str
    records: list[ProfileCollisionSearchRecord]
    max_assignments: int
    headline_metrics: dict[str, int]
    status: str
    summary: str
    falsifiers_triggered: list[str]


DEFAULT_PROFILE_COLLISION_SPECS = [
    ProfileCollisionSearchSpec("profile-collision-8-4", length=8, dimension=4, max_trials=400, max_collisions=8, seed=411),
    ProfileCollisionSearchSpec("profile-collision-9-4", length=9, dimension=4, max_trials=700, max_collisions=8, seed=412),
    ProfileCollisionSearchSpec("profile-collision-10-4", length=10, dimension=4, max_trials=900, max_collisions=8, seed=413),
    ProfileCollisionSearchSpec("profile-collision-10-5", length=10, dimension=5, max_trials=900, max_collisions=8, seed=414),
]


def profile_key(generator: np.ndarray) -> tuple[Any, ...]:
    return tuple(sorted(coordinate_refinement_profiles(generator)))


def _estimated_from_canonical_audit(audit: Any) -> int:
    return max(
        int(audit.left_canonical.estimated_assignments),
        int(audit.right_canonical.estimated_assignments),
    )


def run_profile_collision_spec(
    spec: ProfileCollisionSearchSpec,
    max_assignments: int = 2_000_000,
    max_stored_per_key: int = 4,
) -> ProfileCollisionSearchRecord:
    rng = np.random.default_rng(spec.seed)
    seen: dict[tuple[Any, ...], list[np.ndarray]] = {}
    audits: list[ProfileCollisionAudit] = []
    equivalent = 0
    rejected = 0
    proof_debt = 0
    trials_run = 0
    max_bucket = 0

    for trial in range(1, spec.max_trials + 1):
        trials_run = trial
        candidate = random_full_rank_generator(rng, spec.dimension, spec.length)
        key = profile_key(candidate)
        bucket = seen.setdefault(key, [])
        max_bucket = max(max_bucket, len(bucket) + 1)
        for prior_index, previous in enumerate(bucket):
            if codeword_int_set(previous) == codeword_int_set(candidate):
                continue
            canonical = audit_code_canonicalization_pair(
                record_id=f"{spec.id}-trial-{trial}-prior-{prior_index}",
                source="code_profile_collision_search",
                left=previous,
                right=candidate,
                known_equivalent=None,
                max_assignments=max_assignments,
            )
            if canonical.status.startswith("canonical-equivalent"):
                equivalent += 1
            elif canonical.status == "canonicalization-proof-debt":
                proof_debt += 1
            else:
                rejected += 1
            audits.append(
                ProfileCollisionAudit(
                    id=canonical.id,
                    trial=trial,
                    profile_bucket_size=len(bucket) + 1,
                    canonical_status=canonical.status,
                    canonical_equal=canonical.canonical_equal,
                    estimated_assignments=_estimated_from_canonical_audit(canonical),
                    interpretation=canonical.interpretation,
                )
            )
            if len(audits) >= spec.max_collisions:
                break
        if len(audits) >= spec.max_collisions:
            break
        if len(bucket) < max_stored_per_key:
            bucket.append(candidate)

    if proof_debt:
        status = "profile-collision-proof-debt"
        interpretation = "Some profile collisions exceeded canonicalization caps; these are proof obligations, not evidence."
    elif rejected:
        status = "profile-collisions-rejected-by-canonicalization"
        interpretation = "Profile collisions exist but are rejected by exact/profile-pruned canonicalization."
    elif equivalent:
        status = "profile-collisions-all-equivalent-controls"
        interpretation = "Profile collisions found so far are equivalent controls under profile-pruned canonicalization."
    else:
        status = "no-profile-collision-found"
        interpretation = "No coordinate-profile collision found under this deterministic search budget."

    return ProfileCollisionSearchRecord(
        spec=spec,
        trials_run=trials_run,
        profile_key_count=len(seen),
        profile_collision_count=len(audits),
        equivalent_collision_count=equivalent,
        rejected_collision_count=rejected,
        proof_debt_collision_count=proof_debt,
        max_profile_bucket_size=max_bucket,
        collision_audits=audits,
        status=status,
        interpretation=interpretation,
    )


def run_profile_collision_search(
    specs: list[ProfileCollisionSearchSpec] | None = None,
    max_assignments: int = 2_000_000,
) -> ProfileCollisionSearchReport:
    active_specs = specs or DEFAULT_PROFILE_COLLISION_SPECS
    records = [run_profile_collision_spec(spec, max_assignments=max_assignments) for spec in active_specs]
    metrics = {
        "search_count": len(records),
        "profile_collision_count": sum(record.profile_collision_count for record in records),
        "equivalent_collision_count": sum(record.equivalent_collision_count for record in records),
        "rejected_collision_count": sum(record.rejected_collision_count for record in records),
        "proof_debt_collision_count": sum(record.proof_debt_collision_count for record in records),
        "no_collision_count": sum(1 for record in records if record.status == "no-profile-collision-found"),
        "max_length": max((record.spec.length for record in records), default=0),
    }
    if metrics["proof_debt_collision_count"]:
        status = "profile-collision-proof-debt"
    elif metrics["rejected_collision_count"] or metrics["equivalent_collision_count"]:
        status = "profile-collision-search-dequantized"
    else:
        status = "profile-collision-search-incomplete"
    summary = (
        f"Searched {metrics['search_count']} profile-collision budgets and audited {metrics['profile_collision_count']} collision(s). "
        f"{metrics['equivalent_collision_count']} were equivalent controls, {metrics['rejected_collision_count']} were canonicalization rejections, "
        f"and {metrics['proof_debt_collision_count']} remain proof debt."
    )
    falsifiers = []
    if metrics["equivalent_collision_count"] or metrics["rejected_collision_count"]:
        falsifiers.append("Coordinate-profile collisions do not yet produce hard non-equivalent code rows.")
    if metrics["proof_debt_collision_count"]:
        falsifiers.append("Some profile collisions exceed canonicalization caps and need stronger exact/canonical baselines.")
    return ProfileCollisionSearchReport(utc_now(), records, max_assignments, metrics, status, summary, falsifiers)


def _json_ready(value: Any) -> Any:
    if is_dataclass(value):
        return _json_ready(asdict(value))
    if isinstance(value, dict):
        return {str(key): _json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_ready(item) for item in value]
    if isinstance(value, tuple):
        return _json_ready(list(value))
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.bool_):
        return bool(value)
    return value


def _safe_id(value: str) -> str:
    return "".join(ch if ch.isalnum() else "_" for ch in value.upper()).strip("_")


def write_profile_collision_negative_results(report: ProfileCollisionSearchReport) -> int:
    written = 0
    for record in report.records:
        if record.status not in {
            "profile-collisions-rejected-by-canonicalization",
            "profile-collisions-all-equivalent-controls",
        }:
            continue
        upsert_negative_result(
            NegativeResultRecord(
                id=f"CODE-PROFILE-COLLISION-SEARCH-{_safe_id(record.spec.id)}",
                source="code_profile_collision_search.py",
                claim=f"{record.spec.id} profile collisions provide hard code-equivalence coset evidence.",
                reason_invalid=record.interpretation,
                lesson=(
                    "Search must collide strong coordinate profiles and survive exact canonicalization; equivalent profile collisions "
                    "or canonicalization rejections are not evidence for quantum advantage."
                ),
                applies_to=["CODE-COSET-COLLECTIVE", "PO-DEQUANTIZATION", "PO-FALSIFIERS"],
                evidence=asdict(record),
            )
        )
        written += 1
    return written


def write_profile_collision_search(
    output_path: Path = CODE_PROFILE_COLLISION_SEARCH_PATH,
    specs: list[ProfileCollisionSearchSpec] | None = None,
    max_assignments: int = 2_000_000,
    write_registry: bool = True,
    registry_experiment_id: str = "EXP-CODE-PROFILE-COLLISION-SEARCH",
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "RESULT-CODE-PROFILE-COLLISION-SEARCH-LATEST",
) -> dict[str, Any]:
    report = run_profile_collision_search(specs=specs, max_assignments=max_assignments)
    payload = _json_ready(report)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    if write_registry:
        negative_results_written = write_profile_collision_negative_results(report)
        metrics = dict(report.headline_metrics)
        metrics["negative_results_written"] = negative_results_written
        upsert_experiment_result(
            ExperimentResultRecord(
                id=registry_result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=report.created_at,
                status=report.status,
                summary=report.summary,
                metrics=metrics,
                falsifiers_triggered=report.falsifiers_triggered,
                artifacts={"code_profile_collision_search": str(output_path)},
            )
        )
    return payload
