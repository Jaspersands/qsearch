"""Higher-order coordinate tuple profiles for code-equivalence rows.

Single-coordinate support-splitting profiles already kill the current generated
code rows.  This module raises the bar for future rows: it computes
permutation-invariant profiles over coordinate tuples, searches for collisions
at the 2-coordinate level, and immediately attacks any collision with the
existing profile-pruned canonicalization baseline.

These profiles are classical invariants.  They are not a route to a quantum
speedup; they are a filter that code-coset candidates must survive before any
collective observable is worth designing.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, is_dataclass
from itertools import combinations, permutations
from pathlib import Path
from typing import Any

import numpy as np

from code_canonicalization_baseline import audit_code_canonicalization_pair, default_code_canonicalization_pairs
from code_equivalence_workbench import codeword_int_set
from code_family_search import (
    coordinate_refinement_profiles,
    enumerate_unique_codewords,
    random_full_rank_generator,
    strong_invariant_differences,
    weak_invariant_key,
)
from research_registry import ExperimentResultRecord, NegativeResultRecord, upsert_experiment_result, upsert_negative_result, utc_now


CODE_EQUIVALENCE_DIR = Path("research/code_equivalence")
CODE_TUPLE_PROFILE_BASELINE_PATH = CODE_EQUIVALENCE_DIR / "code_tuple_profile_baseline.json"


@dataclass(frozen=True)
class TupleProfileResult:
    evaluated: bool
    tuple_size: int
    tuple_count: int
    profile_digest: str
    cost_model: str
    interpretation: str


@dataclass(frozen=True)
class CodeTupleProfileRecord:
    id: str
    source: str
    length: int
    dimension: int
    known_equivalent: bool | None
    weak_invariants_match: bool
    strong_distinguishing_invariants: list[str]
    first_distinguishing_tuple_size: int | None
    tuple_results: list[TupleProfileResult]
    status: str
    interpretation: str


@dataclass(frozen=True)
class TupleProfileCollisionSpec:
    id: str
    length: int
    dimension: int
    tuple_size: int
    max_trials: int
    max_collisions: int
    seed: int


@dataclass(frozen=True)
class TupleProfileCollisionAudit:
    id: str
    trial: int
    tuple_profile_bucket_size: int
    tuple_size: int
    canonical_status: str
    canonical_equal: bool | None
    higher_tuple_status: str
    interpretation: str


@dataclass(frozen=True)
class TupleProfileCollisionRecord:
    spec: TupleProfileCollisionSpec
    trials_run: int
    tuple_profile_key_count: int
    tuple_collision_count: int
    equivalent_collision_count: int
    rejected_collision_count: int
    proof_debt_collision_count: int
    max_profile_bucket_size: int
    collision_audits: list[TupleProfileCollisionAudit]
    status: str
    interpretation: str


@dataclass(frozen=True)
class CodeTupleProfileReport:
    created_at: str
    records: list[CodeTupleProfileRecord]
    collision_records: list[TupleProfileCollisionRecord]
    max_tuple_size: int
    tuple_cap: int
    headline_metrics: dict[str, int]
    status: str
    summary: str
    falsifiers_triggered: list[str]


DEFAULT_TUPLE_COLLISION_SPECS = [
    TupleProfileCollisionSpec("tuple-profile-8-4-t2", length=8, dimension=4, tuple_size=2, max_trials=220, max_collisions=4, seed=751),
    TupleProfileCollisionSpec("tuple-profile-9-4-t2", length=9, dimension=4, tuple_size=2, max_trials=320, max_collisions=4, seed=752),
    TupleProfileCollisionSpec("tuple-profile-10-5-t2", length=10, dimension=5, tuple_size=2, max_trials=360, max_collisions=4, seed=753),
]


def _weight_counts(values: list[int]) -> tuple[tuple[int, int], ...]:
    counts: dict[int, int] = {}
    for value in values:
        counts[int(value)] = counts.get(int(value), 0) + 1
    return tuple(sorted(counts.items()))


def _permute_local_pattern(pattern: int, permutation: tuple[int, ...]) -> int:
    value = 0
    for old_offset, new_offset in enumerate(permutation):
        if (pattern >> old_offset) & 1:
            value |= 1 << new_offset
    return value


def _canonical_local_tuple_profile(
    pattern_residual_weights: dict[tuple[int, int], int],
    tuple_size: int,
) -> tuple[tuple[int, int, int], ...]:
    """Canonicalize bit-pattern labels under reordering inside a coordinate tuple."""

    best: tuple[tuple[int, int, int], ...] | None = None
    for permutation in permutations(range(tuple_size)):
        transformed = tuple(
            sorted(
                (
                    _permute_local_pattern(pattern, permutation),
                    residual_weight,
                    count,
                )
                for (pattern, residual_weight), count in pattern_residual_weights.items()
            )
        )
        if best is None or transformed < best:
            best = transformed
    return best or tuple()


def coordinate_tuple_profile_multiset(
    generator: np.ndarray,
    tuple_size: int,
    tuple_cap: int = 50_000,
) -> TupleProfileResult:
    words = enumerate_unique_codewords(generator)
    length = int(words.shape[1])
    tuples = list(combinations(range(length), tuple_size))
    if len(tuples) > tuple_cap:
        return TupleProfileResult(
            evaluated=False,
            tuple_size=tuple_size,
            tuple_count=len(tuples),
            profile_digest="skipped",
            cost_model=f"Skipped {len(tuples)} coordinate tuples above cap {tuple_cap}.",
            interpretation="Higher-order coordinate profile exceeded the tuple cap; this is proof debt.",
        )

    profiles = []
    for coords in tuples:
        pattern_residual_weights: dict[tuple[int, int], int] = {}
        for word in words:
            pattern = 0
            selected_weight = 0
            for offset, coordinate in enumerate(coords):
                bit = int(word[coordinate])
                if bit:
                    pattern |= 1 << offset
                    selected_weight += 1
            residual_weight = int(word.sum()) - selected_weight
            key = (pattern, residual_weight)
            pattern_residual_weights[key] = pattern_residual_weights.get(key, 0) + 1
        profiles.append(_canonical_local_tuple_profile(pattern_residual_weights, tuple_size))
    digest = repr(tuple(sorted(profiles)))
    return TupleProfileResult(
        evaluated=True,
        tuple_size=tuple_size,
        tuple_count=len(tuples),
        profile_digest=digest,
        cost_model=(
            f"Enumerated C({length},{tuple_size})={len(tuples)} coordinate tuples and residual weight profiles "
            f"over {words.shape[0]} codewords."
        ),
        interpretation="Computed a permutation-invariant coordinate-tuple residual weight profile.",
    )


def tuple_profile_key(generator: np.ndarray, tuple_size: int, tuple_cap: int = 50_000) -> str:
    result = coordinate_tuple_profile_multiset(generator, tuple_size=tuple_size, tuple_cap=tuple_cap)
    return result.profile_digest


def audit_code_tuple_profile_pair(
    record_id: str,
    source: str,
    left: np.ndarray,
    right: np.ndarray,
    known_equivalent: bool | None = None,
    max_tuple_size: int = 3,
    tuple_cap: int = 50_000,
) -> CodeTupleProfileRecord:
    left = np.asarray(left, dtype=np.uint8) & 1
    right = np.asarray(right, dtype=np.uint8) & 1
    tuple_results: list[TupleProfileResult] = []
    first_separator: int | None = None
    proof_debt = False
    for tuple_size in range(1, max_tuple_size + 1):
        left_result = coordinate_tuple_profile_multiset(left, tuple_size=tuple_size, tuple_cap=tuple_cap)
        right_result = coordinate_tuple_profile_multiset(right, tuple_size=tuple_size, tuple_cap=tuple_cap)
        evaluated = bool(left_result.evaluated and right_result.evaluated)
        tuple_results.append(
            TupleProfileResult(
                evaluated=evaluated,
                tuple_size=tuple_size,
                tuple_count=max(left_result.tuple_count, right_result.tuple_count),
                profile_digest=left_result.profile_digest[:500],
                cost_model=left_result.cost_model,
                interpretation=(
                    "Left/right tuple-profile multisets differ at this tuple size."
                    if evaluated and left_result.profile_digest != right_result.profile_digest
                    else left_result.interpretation
                ),
            )
        )
        if not evaluated:
            proof_debt = True
            break
        if left_result.profile_digest != right_result.profile_digest:
            first_separator = tuple_size
            break

    weak_match = weak_invariant_key(left) == weak_invariant_key(right)
    strong = strong_invariant_differences(left, right)
    if first_separator is not None:
        status = "rejected-by-coordinate-tuple-profile"
        interpretation = (
            f"{first_separator}-coordinate tuple residual weight profiles separate this code pair; "
            "a matching coset observable is a classical invariant shadow."
        )
    elif known_equivalent:
        status = "tuple-profile-equivalent-control"
        interpretation = "Tuple profiles match on a known equivalent control pair."
    elif proof_debt:
        status = "tuple-profile-proof-debt"
        interpretation = "Tuple-profile evaluation hit a cap; keep this row as proof debt."
    else:
        status = "tuple-profile-survivor-needs-canonicalization"
        interpretation = (
            "Tuple profiles match through the configured order; promote only as proof debt and compare against "
            "canonicalization, automorphism, and exact/pruned baselines."
        )

    return CodeTupleProfileRecord(
        id=record_id,
        source=source,
        length=int(left.shape[1]),
        dimension=int(left.shape[0]),
        known_equivalent=known_equivalent,
        weak_invariants_match=weak_match,
        strong_distinguishing_invariants=strong,
        first_distinguishing_tuple_size=first_separator,
        tuple_results=tuple_results,
        status=status,
        interpretation=interpretation,
    )


def run_tuple_profile_collision_spec(
    spec: TupleProfileCollisionSpec,
    tuple_cap: int = 50_000,
    canonical_max_assignments: int = 2_000_000,
) -> TupleProfileCollisionRecord:
    rng = np.random.default_rng(spec.seed)
    seen: dict[str, list[np.ndarray]] = {}
    audits: list[TupleProfileCollisionAudit] = []
    equivalent = 0
    rejected = 0
    proof_debt = 0
    trials_run = 0
    max_bucket = 0

    for trial in range(1, spec.max_trials + 1):
        trials_run = trial
        candidate = random_full_rank_generator(rng, spec.dimension, spec.length)
        key = tuple_profile_key(candidate, spec.tuple_size, tuple_cap=tuple_cap)
        if key == "skipped":
            break
        bucket = seen.setdefault(key, [])
        max_bucket = max(max_bucket, len(bucket) + 1)
        for prior_index, previous in enumerate(bucket):
            if codeword_int_set(previous) == codeword_int_set(candidate):
                continue
            canonical = audit_code_canonicalization_pair(
                record_id=f"{spec.id}-trial-{trial}-prior-{prior_index}",
                source="code_tuple_profile_baseline",
                left=previous,
                right=candidate,
                known_equivalent=None,
                max_assignments=canonical_max_assignments,
            )
            higher = audit_code_tuple_profile_pair(
                record_id=f"{spec.id}-higher-{trial}-{prior_index}",
                source="code_tuple_profile_baseline",
                left=previous,
                right=candidate,
                known_equivalent=None,
                max_tuple_size=min(3, spec.tuple_size + 1),
                tuple_cap=tuple_cap,
            )
            if canonical.status.startswith("canonical-equivalent"):
                equivalent += 1
            elif canonical.status == "canonicalization-proof-debt":
                proof_debt += 1
            else:
                rejected += 1
            audits.append(
                TupleProfileCollisionAudit(
                    id=canonical.id,
                    trial=trial,
                    tuple_profile_bucket_size=len(bucket) + 1,
                    tuple_size=spec.tuple_size,
                    canonical_status=canonical.status,
                    canonical_equal=canonical.canonical_equal,
                    higher_tuple_status=higher.status,
                    interpretation=canonical.interpretation,
                )
            )
            if len(audits) >= spec.max_collisions:
                break
        if len(audits) >= spec.max_collisions:
            break
        if len(bucket) < 4:
            bucket.append(candidate)

    if proof_debt:
        status = "tuple-profile-collision-proof-debt"
        interpretation = "Some tuple-profile collisions exceeded canonicalization caps; these are proof obligations."
    elif rejected:
        status = "tuple-profile-collisions-rejected-by-canonicalization"
        interpretation = "Tuple-profile collisions exist but stronger canonicalization rejects them."
    elif equivalent:
        status = "tuple-profile-collisions-all-equivalent-controls"
        interpretation = "Tuple-profile collisions found so far are equivalent controls."
    else:
        status = "no-tuple-profile-collision-found"
        interpretation = "No nontrivial tuple-profile collision was found under this deterministic search budget."

    return TupleProfileCollisionRecord(
        spec=spec,
        trials_run=trials_run,
        tuple_profile_key_count=len(seen),
        tuple_collision_count=len(audits),
        equivalent_collision_count=equivalent,
        rejected_collision_count=rejected,
        proof_debt_collision_count=proof_debt,
        max_profile_bucket_size=max_bucket,
        collision_audits=audits,
        status=status,
        interpretation=interpretation,
    )


def run_code_tuple_profile_baseline(
    max_tuple_size: int = 3,
    tuple_cap: int = 50_000,
    collision_specs: list[TupleProfileCollisionSpec] | None = None,
    include_code_family_search: bool = True,
) -> CodeTupleProfileReport:
    records = [
        audit_code_tuple_profile_pair(
            record_id=record_id,
            source=source,
            left=left,
            right=right,
            known_equivalent=known_equivalent,
            max_tuple_size=max_tuple_size,
            tuple_cap=tuple_cap,
        )
        for record_id, source, left, right, known_equivalent in default_code_canonicalization_pairs(
            include_code_family_search=include_code_family_search
        )
    ]
    active_collision_specs = collision_specs or DEFAULT_TUPLE_COLLISION_SPECS
    collision_records = [
        run_tuple_profile_collision_spec(
            spec,
            tuple_cap=tuple_cap,
        )
        for spec in active_collision_specs
    ]
    metrics = {
        "pair_count": len(records),
        "tuple_profile_rejection_count": sum(1 for record in records if record.status == "rejected-by-coordinate-tuple-profile"),
        "tuple_profile_survivor_count": sum(1 for record in records if record.status == "tuple-profile-survivor-needs-canonicalization"),
        "tuple_profile_proof_debt_count": sum(1 for record in records if record.status == "tuple-profile-proof-debt"),
        "equivalent_control_count": sum(1 for record in records if record.status == "tuple-profile-equivalent-control"),
        "collision_search_count": len(collision_records),
        "tuple_collision_count": sum(record.tuple_collision_count for record in collision_records),
        "tuple_collision_equivalent_count": sum(record.equivalent_collision_count for record in collision_records),
        "tuple_collision_rejected_count": sum(record.rejected_collision_count for record in collision_records),
        "tuple_collision_proof_debt_count": sum(record.proof_debt_collision_count for record in collision_records),
        "no_tuple_collision_count": sum(1 for record in collision_records if record.status == "no-tuple-profile-collision-found"),
    }
    if metrics["tuple_profile_proof_debt_count"] or metrics["tuple_collision_proof_debt_count"]:
        status = "code-tuple-profile-proof-debt"
    elif metrics["tuple_profile_rejection_count"] or metrics["tuple_collision_rejected_count"] or metrics["tuple_collision_equivalent_count"]:
        status = "code-tuple-profile-baselines-dequantize-current-rows"
    else:
        status = "code-tuple-profile-search-incomplete"
    summary = (
        f"Audited {metrics['pair_count']} code pair row(s) with coordinate tuple profiles through t={max_tuple_size}; "
        f"{metrics['tuple_profile_rejection_count']} were rejected and {metrics['tuple_profile_survivor_count']} survived only as proof debt. "
        f"Searched {metrics['collision_search_count']} tuple-profile collision budget(s), finding {metrics['tuple_collision_count']} collision(s)."
    )
    falsifiers = []
    if metrics["tuple_profile_rejection_count"]:
        falsifiers.append("Higher-order coordinate tuple profiles separate current code-equivalence rows.")
    if metrics["tuple_collision_equivalent_count"] or metrics["tuple_collision_rejected_count"]:
        falsifiers.append("Tuple-profile collisions found so far are equivalent controls or canonicalization rejections.")
    if metrics["no_tuple_collision_count"]:
        falsifiers.append("Random tuple-profile collision search found no nontrivial hard rows under current budgets.")
    if metrics["tuple_profile_survivor_count"] or metrics["tuple_profile_proof_debt_count"]:
        falsifiers.append("Tuple-profile survivors remain proof debt until canonicalization and lower-bound obligations are resolved.")
    return CodeTupleProfileReport(utc_now(), records, collision_records, max_tuple_size, tuple_cap, metrics, status, summary, falsifiers)


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


def write_code_tuple_profile_negative_results(report: CodeTupleProfileReport) -> int:
    written = 0
    for record in report.records:
        if record.status != "rejected-by-coordinate-tuple-profile":
            continue
        upsert_negative_result(
            NegativeResultRecord(
                id=f"CODE-TUPLE-PROFILE-REJECTED-{_safe_id(record.id)}",
                source="code_tuple_profile_baseline.py",
                claim=f"{record.id} supplies hard code-equivalence coset evidence beyond classical tuple profiles.",
                reason_invalid=record.interpretation,
                lesson=(
                    "Code-coset rows must survive higher-order coordinate tuple profiles before motivating "
                    "collective quantum observables."
                ),
                applies_to=["CODE-COSET-COLLECTIVE", "PO-DEQUANTIZATION", "PO-FALSIFIERS"],
                evidence=asdict(record),
            )
        )
        written += 1
    for record in report.collision_records:
        if record.status not in {
            "tuple-profile-collisions-rejected-by-canonicalization",
            "tuple-profile-collisions-all-equivalent-controls",
        }:
            continue
        upsert_negative_result(
            NegativeResultRecord(
                id=f"CODE-TUPLE-PROFILE-COLLISION-{_safe_id(record.spec.id)}",
                source="code_tuple_profile_baseline.py",
                claim=f"{record.spec.id} tuple-profile collisions provide hard code-equivalence coset evidence.",
                reason_invalid=record.interpretation,
                lesson=(
                    "Tuple-profile collisions are not hard evidence unless they are non-equivalent and survive "
                    "canonicalization, automorphism, and exact/pruned baselines."
                ),
                applies_to=["CODE-COSET-COLLECTIVE", "PO-DEQUANTIZATION", "PO-FALSIFIERS"],
                evidence=asdict(record),
            )
        )
        written += 1
    return written


def write_code_tuple_profile_baseline(
    output_path: Path = CODE_TUPLE_PROFILE_BASELINE_PATH,
    max_tuple_size: int = 3,
    tuple_cap: int = 50_000,
    collision_specs: list[TupleProfileCollisionSpec] | None = None,
    include_code_family_search: bool = True,
    write_registry: bool = True,
    registry_experiment_id: str = "EXP-CODE-TUPLE-PROFILE-BASELINE",
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "RESULT-CODE-TUPLE-PROFILE-BASELINE-LATEST",
) -> dict[str, Any]:
    report = run_code_tuple_profile_baseline(
        max_tuple_size=max_tuple_size,
        tuple_cap=tuple_cap,
        collision_specs=collision_specs,
        include_code_family_search=include_code_family_search,
    )
    payload = _json_ready(report)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    if write_registry:
        negative_results_written = write_code_tuple_profile_negative_results(report)
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
                artifacts={"code_tuple_profile_baseline": str(output_path)},
            )
        )
    return payload
