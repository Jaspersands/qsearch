"""Profile-pruned canonicalization baseline for binary code equivalence.

Code equivalence is only a credible nonabelian-HSP frontier after generated
pairs survive classical canonicalization attempts.  This module turns the
single-coordinate support-splitting profiles already used elsewhere into an
exact canonical-form baseline whenever the profile buckets are small enough.

Rows that fail profile multiset checks or exact canonical-form comparison are
negative evidence.  Rows with large unresolved buckets become proof debt, not
positive quantum evidence.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, is_dataclass
from itertools import product, permutations
from pathlib import Path
from typing import Any

import numpy as np

from code_equivalence_workbench import (
    hamming_7_4_generator,
    math_factorial,
    permute_codeword_set,
    permute_columns,
    twisted_hamming_7_4_generator,
    weak_invariant_collision_8_4_generators,
)
from code_family_search import (
    CODE_FAMILY_SEARCH_PATH,
    coordinate_refinement_profiles,
    run_code_family_search,
    strong_invariant_differences,
    weak_invariant_key,
)
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


CODE_EQUIVALENCE_DIR = Path("research/code_equivalence")
CODE_CANONICALIZATION_BASELINE_PATH = CODE_EQUIVALENCE_DIR / "code_canonicalization_baseline.json"


@dataclass(frozen=True)
class CanonicalFormResult:
    evaluated: bool
    estimated_assignments: int
    profile_bucket_sizes: list[int]
    canonical_form: tuple[int, ...] | None
    cost_model: str
    interpretation: str


@dataclass(frozen=True)
class CodeCanonicalizationRecord:
    id: str
    source: str
    length: int
    dimension: int
    known_equivalent: bool | None
    weak_invariants_match: bool
    strong_distinguishing_invariants: list[str]
    profile_multisets_match: bool
    left_canonical: CanonicalFormResult
    right_canonical: CanonicalFormResult
    canonical_equal: bool | None
    status: str
    interpretation: str


@dataclass(frozen=True)
class CodeCanonicalizationReport:
    created_at: str
    records: list[CodeCanonicalizationRecord]
    max_assignments: int
    headline_metrics: dict[str, int]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _codeword_int_set_from_rows(generator: np.ndarray) -> frozenset[int]:
    matrix = np.asarray(generator, dtype=np.uint8) & 1
    values = []
    for mask in range(1 << matrix.shape[0]):
        word = np.zeros(matrix.shape[1], dtype=np.uint8)
        for row in range(matrix.shape[0]):
            if (mask >> row) & 1:
                word ^= matrix[row]
        encoded = 0
        for index, bit in enumerate(word.tolist()):
            if bit:
                encoded |= 1 << index
        values.append(encoded)
    return frozenset(values)


def _profile_buckets(generator: np.ndarray) -> list[tuple[tuple[Any, ...], list[int]]]:
    buckets: dict[tuple[Any, ...], list[int]] = {}
    for index, profile in enumerate(coordinate_refinement_profiles(generator)):
        buckets.setdefault(profile, []).append(index)
    return [(profile, buckets[profile]) for profile in sorted(buckets)]


def _estimated_assignments(buckets: list[tuple[tuple[Any, ...], list[int]]]) -> int:
    total = 1
    for _profile, indices in buckets:
        total *= math_factorial(len(indices))
    return total


def canonical_form_under_profile_refinement(
    generator: np.ndarray,
    max_assignments: int = 2_000_000,
) -> CanonicalFormResult:
    matrix = np.asarray(generator, dtype=np.uint8) & 1
    length = int(matrix.shape[1])
    buckets = _profile_buckets(matrix)
    bucket_sizes = [len(indices) for _profile, indices in buckets]
    estimated = _estimated_assignments(buckets)
    if estimated > max_assignments:
        return CanonicalFormResult(
            evaluated=False,
            estimated_assignments=estimated,
            profile_bucket_sizes=bucket_sizes,
            canonical_form=None,
            cost_model=f"Skipped exact canonicalization: {estimated} profile-compatible assignments exceed cap {max_assignments}.",
            interpretation=(
                "Profile refinement leaves large coordinate buckets; add stronger canonicalization before treating "
                "this row as hard."
            ),
        )

    codewords = _codeword_int_set_from_rows(matrix)
    bucket_permutation_iters = [permutations(indices) for _profile, indices in buckets]
    best: tuple[int, ...] | None = None
    checked = 0
    for bucket_orders in product(*bucket_permutation_iters):
        old_to_new = [-1] * length
        next_position = 0
        for ordered_indices in bucket_orders:
            for old_index in ordered_indices:
                old_to_new[int(old_index)] = next_position
                next_position += 1
        checked += 1
        canonical = tuple(sorted(permute_codeword_set(codewords, length, old_to_new)))
        if best is None or canonical < best:
            best = canonical

    return CanonicalFormResult(
        evaluated=True,
        estimated_assignments=estimated,
        profile_bucket_sizes=bucket_sizes,
        canonical_form=best,
        cost_model=f"Checked {checked} profile-compatible assignment(s); exact only within the profile bucket cap.",
        interpretation="Computed an exact canonical form under all profile-compatible coordinate assignments.",
    )


def _short_canonical(result: CanonicalFormResult, limit: int = 32) -> CanonicalFormResult:
    if result.canonical_form is None or len(result.canonical_form) <= limit:
        return result
    return CanonicalFormResult(
        evaluated=result.evaluated,
        estimated_assignments=result.estimated_assignments,
        profile_bucket_sizes=result.profile_bucket_sizes,
        canonical_form=tuple(result.canonical_form[:limit]),
        cost_model=result.cost_model,
        interpretation=result.interpretation + f" Canonical form truncated to first {limit} codewords for the artifact.",
    )


def audit_code_canonicalization_pair(
    record_id: str,
    source: str,
    left: np.ndarray,
    right: np.ndarray,
    known_equivalent: bool | None = None,
    max_assignments: int = 2_000_000,
) -> CodeCanonicalizationRecord:
    left = np.asarray(left, dtype=np.uint8) & 1
    right = np.asarray(right, dtype=np.uint8) & 1
    left_profiles = sorted(coordinate_refinement_profiles(left))
    right_profiles = sorted(coordinate_refinement_profiles(right))
    profile_match = left_profiles == right_profiles
    weak_match = weak_invariant_key(left) == weak_invariant_key(right)
    strong = strong_invariant_differences(left, right)

    left_form = canonical_form_under_profile_refinement(left, max_assignments=max_assignments)
    right_form = canonical_form_under_profile_refinement(right, max_assignments=max_assignments)
    canonical_equal = (
        left_form.canonical_form == right_form.canonical_form
        if left_form.evaluated and right_form.evaluated
        else None
    )

    if not profile_match:
        status = "rejected-by-coordinate-profile-partition"
        interpretation = (
            "Coordinate refinement profiles differ; this pair is separated by a support-splitting-style "
            "classical canonicalization invariant."
        )
    elif canonical_equal is False:
        status = "rejected-by-exact-profile-canonical-form"
        interpretation = "Profile multisets match, but exact profile-pruned canonical forms differ."
    elif canonical_equal is True:
        status = "canonical-equivalent-control" if known_equivalent else "canonical-equivalent-or-automorphic"
        interpretation = "Exact profile-pruned canonical forms match; the pair is equivalent under this baseline."
    else:
        status = "canonicalization-proof-debt"
        interpretation = (
            "Profile multisets match but exact canonicalization exceeded the assignment cap; this is proof debt, "
            "not positive quantum evidence."
        )

    return CodeCanonicalizationRecord(
        id=record_id,
        source=source,
        length=int(left.shape[1]),
        dimension=int(left.shape[0]),
        known_equivalent=known_equivalent,
        weak_invariants_match=weak_match,
        strong_distinguishing_invariants=strong,
        profile_multisets_match=profile_match,
        left_canonical=_short_canonical(left_form),
        right_canonical=_short_canonical(right_form),
        canonical_equal=canonical_equal,
        status=status,
        interpretation=interpretation,
    )


def _artifact_search_pairs(path: Path = CODE_FAMILY_SEARCH_PATH) -> list[tuple[str, str, np.ndarray, np.ndarray, bool | None]]:
    if path.exists():
        payload = json.loads(path.read_text())
        records = payload.get("records", [])
    else:
        records = [asdict(record) for record in run_code_family_search().records]

    pairs = []
    for record in records:
        left = record.get("generator_a") or []
        right = record.get("generator_b") or []
        if not left or not right:
            continue
        spec = record.get("spec", {})
        record_id = str(spec.get("id", record.get("id", "unknown")))
        pairs.append(
            (
                f"code-family-{record_id}",
                "code_family_search",
                np.asarray(left, dtype=np.uint8),
                np.asarray(right, dtype=np.uint8),
                False if record.get("status") in {"rejected-by-strong-classical-invariant", "rejected-by-bounded-exact-search"} else None,
            )
        )
    return pairs


def default_code_canonicalization_pairs(
    include_code_family_search: bool = True,
) -> list[tuple[str, str, np.ndarray, np.ndarray, bool | None]]:
    hamming = hamming_7_4_generator()
    weak_left, weak_right = weak_invariant_collision_8_4_generators()
    pairs: list[tuple[str, str, np.ndarray, np.ndarray, bool | None]] = [
        (
            "hamming-7-4-permuted",
            "code_equivalence_workbench",
            hamming,
            permute_columns(hamming, [2, 0, 6, 1, 5, 3, 4]),
            True,
        ),
        (
            "hamming-7-4-column-twist",
            "code_equivalence_workbench",
            hamming,
            twisted_hamming_7_4_generator(),
            False,
        ),
        (
            "random-8-4-weak-invariant-collision",
            "code_equivalence_workbench",
            weak_left,
            weak_right,
            False,
        ),
    ]
    if include_code_family_search:
        pairs.extend(_artifact_search_pairs())
    return pairs


def run_code_canonicalization_baseline(
    max_assignments: int = 2_000_000,
    include_code_family_search: bool = True,
) -> CodeCanonicalizationReport:
    records = [
        audit_code_canonicalization_pair(
            record_id=record_id,
            source=source,
            left=left,
            right=right,
            known_equivalent=known_equivalent,
            max_assignments=max_assignments,
        )
        for record_id, source, left, right, known_equivalent in default_code_canonicalization_pairs(
            include_code_family_search=include_code_family_search
        )
    ]
    metrics = {
        "record_count": len(records),
        "profile_rejection_count": sum(1 for record in records if record.status == "rejected-by-coordinate-profile-partition"),
        "canonical_form_rejection_count": sum(1 for record in records if record.status == "rejected-by-exact-profile-canonical-form"),
        "canonical_equivalent_count": sum(1 for record in records if record.status.startswith("canonical-equivalent")),
        "proof_debt_count": sum(1 for record in records if record.status == "canonicalization-proof-debt"),
        "weak_invariant_match_count": sum(1 for record in records if record.weak_invariants_match),
        "max_estimated_assignments": max(
            (
                max(record.left_canonical.estimated_assignments, record.right_canonical.estimated_assignments)
                for record in records
            ),
            default=0,
        ),
    }
    rejected = metrics["profile_rejection_count"] + metrics["canonical_form_rejection_count"]
    if metrics["proof_debt_count"]:
        status = "canonicalization-proof-debt"
    elif rejected:
        status = "code-pairs-dequantized-by-canonicalization"
    else:
        status = "canonicalization-controls-only"
    summary = (
        f"Audited {metrics['record_count']} code-pair row(s) with profile-pruned canonicalization. "
        f"{rejected} row(s) were rejected by canonicalization/profile baselines; "
        f"{metrics['proof_debt_count']} row(s) exceeded the assignment cap."
    )
    falsifiers = []
    if rejected:
        falsifiers.append("Code-equivalence rows are separated by profile or exact canonical-form baselines.")
    if metrics["proof_debt_count"]:
        falsifiers.append("Some code rows need stronger canonicalization before any quantum signal can be trusted.")
    return CodeCanonicalizationReport(utc_now(), records, max_assignments, metrics, status, summary, falsifiers)


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


def write_code_canonicalization_negative_results(report: CodeCanonicalizationReport) -> int:
    written = 0
    for record in report.records:
        if record.status not in {
            "rejected-by-coordinate-profile-partition",
            "rejected-by-exact-profile-canonical-form",
        }:
            continue
        upsert_negative_result(
            NegativeResultRecord(
                id=f"CODE-CANONICALIZATION-REJECTED-{_safe_id(record.id)}",
                source="code_canonicalization_baseline.py",
                claim=f"{record.id} is a hard code-equivalence row for nonclassical coset observables.",
                reason_invalid=record.interpretation,
                lesson=(
                    "Generated code-equivalence evidence must survive profile refinement and exact/pruned canonicalization, "
                    "not merely weak weight-enumerator or column-statistic collisions."
                ),
                applies_to=["CODE-COSET-COLLECTIVE", "PO-DEQUANTIZATION", "PO-FALSIFIERS"],
                evidence={
                    "record_id": record.id,
                    "source": record.source,
                    "status": record.status,
                    "weak_invariants_match": record.weak_invariants_match,
                    "strong_distinguishing_invariants": record.strong_distinguishing_invariants,
                },
            )
        )
        written += 1
    return written


def write_code_canonicalization_baseline(
    output_path: Path = CODE_CANONICALIZATION_BASELINE_PATH,
    max_assignments: int = 2_000_000,
    include_code_family_search: bool = True,
    write_registry: bool = True,
    registry_experiment_id: str = "EXP-CODE-CANONICALIZATION-BASELINE",
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "RESULT-CODE-CANONICALIZATION-BASELINE-LATEST",
) -> dict[str, Any]:
    report = run_code_canonicalization_baseline(
        max_assignments=max_assignments,
        include_code_family_search=include_code_family_search,
    )
    payload = _json_ready(report)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    if write_registry:
        negative_results_written = write_code_canonicalization_negative_results(report)
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
                artifacts={"code_canonicalization_baseline": str(output_path)},
            )
        )
    return payload
