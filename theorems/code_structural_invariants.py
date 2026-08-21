"""First-class structural invariant suite for code-equivalence candidates.

Code-equivalence rows should not survive because a baseline forgot to run the
standard structural fingerprints.  This module turns support splitting, dual
weight enumerators, hull dimension, puncturing, and shortening profiles into a
registry artifact instead of leaving them as diagnostics inside random search.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, is_dataclass
from pathlib import Path
from typing import Any

import numpy as np

from code_canonicalization_baseline import default_code_canonicalization_pairs
from code_equivalence_workbench import gf2_rank, weight_enumerator
from code_family_search import (
    dual_weight_enumerator,
    hull_dimension,
    punctured_weight_profile,
    shortened_weight_profile,
    support_splitting_signature,
    weak_invariant_key,
)
from research_registry import ExperimentResultRecord, NegativeResultRecord, upsert_experiment_result, upsert_negative_result, utc_now


CODE_EQUIVALENCE_DIR = Path("research/code_equivalence")
CODE_STRUCTURAL_INVARIANTS_PATH = CODE_EQUIVALENCE_DIR / "code_structural_invariants.json"


@dataclass(frozen=True)
class StructuralInvariantComparison:
    name: str
    distinguishes: bool
    signature_a: str
    signature_b: str
    interpretation: str


@dataclass(frozen=True)
class CodeStructuralInvariantRecord:
    id: str
    source: str
    length: int
    dimension: int
    known_equivalent: bool | None
    weak_invariants_match: bool
    distinguishing_invariants: list[str]
    comparisons: list[StructuralInvariantComparison]
    status: str
    interpretation: str


@dataclass(frozen=True)
class CodeStructuralInvariantReport:
    created_at: str
    records: list[CodeStructuralInvariantRecord]
    include_code_family_search: bool
    headline_metrics: dict[str, int]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _short(value: Any, limit: int = 500) -> str:
    text = str(value)
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."


def _comparison(name: str, left: Any, right: Any, label: str) -> StructuralInvariantComparison:
    distinguishes = left != right
    return StructuralInvariantComparison(
        name=name,
        distinguishes=distinguishes,
        signature_a=_short(left),
        signature_b=_short(right),
        interpretation=(
            f"{label} separates the code pair; any matching coset observable is a classical structural shadow."
            if distinguishes
            else f"{label} matches on this pair."
        ),
    )


def structural_invariant_comparisons(left: np.ndarray, right: np.ndarray) -> list[StructuralInvariantComparison]:
    left = np.asarray(left, dtype=np.uint8) & 1
    right = np.asarray(right, dtype=np.uint8) & 1
    return [
        _comparison(
            "length_dimension_rank",
            (int(left.shape[1]), gf2_rank(left)),
            (int(right.shape[1]), gf2_rank(right)),
            "Length/dimension/rank",
        ),
        _comparison("weight_enumerator", weight_enumerator(left), weight_enumerator(right), "Codeword weight enumerator"),
        _comparison("dual_weight_enumerator", dual_weight_enumerator(left), dual_weight_enumerator(right), "Dual-code weight enumerator"),
        _comparison("hull_dimension", hull_dimension(left), hull_dimension(right), "Hull dimension"),
        _comparison(
            "support_splitting_fingerprint",
            support_splitting_signature(left),
            support_splitting_signature(right),
            "Support-splitting coordinate fingerprint",
        ),
        _comparison("punctured_weight_profile", punctured_weight_profile(left), punctured_weight_profile(right), "Punctured-code profile"),
        _comparison("shortened_weight_profile", shortened_weight_profile(left), shortened_weight_profile(right), "Shortened-code profile"),
    ]


def audit_code_structural_invariants_pair(
    record_id: str,
    source: str,
    left: np.ndarray,
    right: np.ndarray,
    known_equivalent: bool | None = None,
) -> CodeStructuralInvariantRecord:
    left = np.asarray(left, dtype=np.uint8) & 1
    right = np.asarray(right, dtype=np.uint8) & 1
    comparisons = structural_invariant_comparisons(left, right)
    distinguishing = [comparison.name for comparison in comparisons if comparison.distinguishes]
    weak_match = weak_invariant_key(left) == weak_invariant_key(right)
    if distinguishing:
        status = "rejected-by-structural-code-invariant"
        interpretation = (
            "The pair is separated by structural classical code invariants: " + ", ".join(distinguishing)
        )
    elif known_equivalent:
        status = "structural-invariant-equivalent-control"
        interpretation = "Structural invariants match on a known equivalent control pair."
    else:
        status = "structural-invariant-survivor-proof-debt"
        interpretation = (
            "Implemented structural invariants match; this is proof debt requiring tuple profiles, canonicalization, "
            "automorphism-aware checks, and lower-bound evidence."
        )
    return CodeStructuralInvariantRecord(
        id=record_id,
        source=source,
        length=int(left.shape[1]),
        dimension=int(left.shape[0]),
        known_equivalent=known_equivalent,
        weak_invariants_match=weak_match,
        distinguishing_invariants=distinguishing,
        comparisons=comparisons,
        status=status,
        interpretation=interpretation,
    )


def run_code_structural_invariants(
    include_code_family_search: bool = True,
) -> CodeStructuralInvariantReport:
    records = [
        audit_code_structural_invariants_pair(record_id, source, left, right, known_equivalent)
        for record_id, source, left, right, known_equivalent in default_code_canonicalization_pairs(
            include_code_family_search=include_code_family_search
        )
    ]
    metrics = {
        "record_count": len(records),
        "structural_rejection_count": sum(1 for record in records if record.status == "rejected-by-structural-code-invariant"),
        "equivalent_control_count": sum(1 for record in records if record.status == "structural-invariant-equivalent-control"),
        "proof_debt_count": sum(1 for record in records if record.status == "structural-invariant-survivor-proof-debt"),
        "weak_invariant_match_count": sum(1 for record in records if record.weak_invariants_match),
        "support_splitting_rejection_count": sum(
            1 for record in records if "support_splitting_fingerprint" in record.distinguishing_invariants
        ),
        "dual_rejection_count": sum(1 for record in records if "dual_weight_enumerator" in record.distinguishing_invariants),
        "puncture_shorten_rejection_count": sum(
            1
            for record in records
            if {"punctured_weight_profile", "shortened_weight_profile"}.intersection(record.distinguishing_invariants)
        ),
    }
    if metrics["proof_debt_count"]:
        status = "code-structural-invariant-proof-debt"
    elif metrics["structural_rejection_count"]:
        status = "code-rows-dequantized-by-structural-invariants"
    else:
        status = "structural-invariant-controls-only"
    summary = (
        f"Audited {metrics['record_count']} code-equivalence row(s) against structural invariants. "
        f"{metrics['structural_rejection_count']} row(s) were separated; "
        f"{metrics['proof_debt_count']} row(s) remain proof debt."
    )
    falsifiers = []
    if metrics["structural_rejection_count"]:
        falsifiers.append("Structural code invariants separate current code-equivalence rows.")
    if metrics["proof_debt_count"]:
        falsifiers.append("Rows surviving structural invariants remain proof debt until stronger baselines and lower bounds run.")
    return CodeStructuralInvariantReport(utc_now(), records, include_code_family_search, metrics, status, summary, falsifiers)


def _json_ready(value: Any) -> Any:
    if is_dataclass(value):
        return _json_ready(asdict(value))
    if isinstance(value, dict):
        return {str(key): _json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_ready(item) for item in value]
    if isinstance(value, tuple):
        return [_json_ready(item) for item in value]
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.bool_):
        return bool(value)
    return value


def _safe_id(value: str) -> str:
    return "".join(ch if ch.isalnum() else "_" for ch in value.upper()).strip("_")


def write_code_structural_negative_results(report: CodeStructuralInvariantReport) -> int:
    written = 0
    for record in report.records:
        if record.status != "rejected-by-structural-code-invariant":
            continue
        upsert_negative_result(
            NegativeResultRecord(
                id=f"CODE-STRUCTURAL-INVARIANT-REJECTED-{_safe_id(record.id)}",
                source="code_structural_invariants.py",
                claim=f"{record.id} supplies hard code-equivalence coset evidence beyond classical structural invariants.",
                reason_invalid=record.interpretation,
                lesson=(
                    "Code-equivalence rows must survive support splitting, dual/hull, puncturing, shortening, "
                    "tuple-profile, and canonicalization baselines before motivating a collective quantum observable."
                ),
                applies_to=["CODE-COSET-COLLECTIVE", "PO-DEQUANTIZATION", "PO-FALSIFIERS"],
                evidence={
                    "record_id": record.id,
                    "source": record.source,
                    "status": record.status,
                    "weak_invariants_match": record.weak_invariants_match,
                    "distinguishing_invariants": record.distinguishing_invariants,
                },
            )
        )
        written += 1
    return written


def write_code_structural_invariants(
    output_path: Path = CODE_STRUCTURAL_INVARIANTS_PATH,
    include_code_family_search: bool = True,
    write_registry: bool = True,
    registry_experiment_id: str = "EXP-CODE-STRUCTURAL-INVARIANTS",
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "RESULT-CODE-STRUCTURAL-INVARIANTS-LATEST",
) -> dict[str, Any]:
    report = run_code_structural_invariants(include_code_family_search=include_code_family_search)
    payload = _json_ready(report)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    if write_registry:
        negative_results_written = write_code_structural_negative_results(report)
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
                artifacts={"code_structural_invariants": str(output_path)},
            )
        )
    return payload
