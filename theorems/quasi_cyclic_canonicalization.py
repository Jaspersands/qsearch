"""Quasi-cyclic automorphism-aware canonicalization for code proof-debt rows.

The quasi-cyclic search can find tuple-profile collisions whose unrestricted
profile-pruned canonicalization is too expensive.  Before treating those rows
as hard, we should ask a cheaper and more structured question: are they already
equivalent under the natural block permutation and cyclic-rotation symmetries
of quasi-cyclic codes?

This module is deliberately conservative.  Equivalence under the quasi-cyclic
automorphism group is a negative/equivalent-control result.  Non-equivalence
under that restricted group is only proof debt; it does not prove full code
non-equivalence.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, is_dataclass
from itertools import permutations, product
from pathlib import Path
from typing import Any

import numpy as np

from code_equivalence_workbench import codeword_int_set, math_factorial, permute_codeword_set
from quasi_cyclic_code_search import QUASI_CYCLIC_CODE_SEARCH_PATH
from research_registry import ExperimentResultRecord, NegativeResultRecord, upsert_experiment_result, upsert_negative_result, utc_now


CODE_EQUIVALENCE_DIR = Path("research/code_equivalence")
QC_CANONICALIZATION_PATH = CODE_EQUIVALENCE_DIR / "quasi_cyclic_canonicalization.json"


@dataclass(frozen=True)
class QCCanonicalForm:
    evaluated: bool
    index: int
    block_count: int
    group_size: int
    checked_permutations: int
    canonical_form: tuple[int, ...] | None
    cost_model: str
    interpretation: str


@dataclass(frozen=True)
class QCCanonicalizationRecord:
    id: str
    source_search_id: str
    length: int
    dimension: int
    index: int
    block_count: int
    tuple_profile_status: str
    unrestricted_estimated_assignments: int
    left_canonical: QCCanonicalForm
    right_canonical: QCCanonicalForm
    qc_canonical_equal: bool | None
    status: str
    interpretation: str


@dataclass(frozen=True)
class QCCanonicalizationReport:
    created_at: str
    records: list[QCCanonicalizationRecord]
    max_group_size: int
    headline_metrics: dict[str, int]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def qc_group_size(index: int, block_count: int) -> int:
    return math_factorial(block_count) * (index**block_count)


def qc_coordinate_permutation(
    index: int,
    block_count: int,
    block_permutation: tuple[int, ...],
    shifts: tuple[int, ...],
) -> list[int]:
    old_to_new = [-1] * (index * block_count)
    for old_block in range(block_count):
        new_block = int(block_permutation[old_block])
        shift = int(shifts[old_block])
        for position in range(index):
            old_coordinate = old_block * index + position
            new_coordinate = new_block * index + ((position + shift) % index)
            old_to_new[old_coordinate] = new_coordinate
    return old_to_new


def apply_old_to_new_permutation(generator: np.ndarray, old_to_new: list[int]) -> np.ndarray:
    matrix = np.asarray(generator, dtype=np.uint8) & 1
    result = np.zeros_like(matrix)
    for old_index, new_index in enumerate(old_to_new):
        result[:, int(new_index)] = matrix[:, old_index]
    return result


def qc_canonical_form(
    generator: np.ndarray,
    index: int,
    max_group_size: int = 250_000,
) -> QCCanonicalForm:
    matrix = np.asarray(generator, dtype=np.uint8) & 1
    length = int(matrix.shape[1])
    if index <= 0 or length % index:
        return QCCanonicalForm(
            evaluated=False,
            index=index,
            block_count=0,
            group_size=0,
            checked_permutations=0,
            canonical_form=None,
            cost_model="Skipped: code length is not divisible by the proposed quasi-cyclic index.",
            interpretation="The row does not match the expected quasi-cyclic block structure.",
        )
    block_count = length // index
    group_size = qc_group_size(index, block_count)
    if group_size > max_group_size:
        return QCCanonicalForm(
            evaluated=False,
            index=index,
            block_count=block_count,
            group_size=group_size,
            checked_permutations=0,
            canonical_form=None,
            cost_model=f"Skipped: QC automorphism group size {group_size} exceeds cap {max_group_size}.",
            interpretation="QC automorphism canonicalization exceeded the configured cap; keep as proof debt.",
        )

    source = codeword_int_set(matrix)
    best: tuple[int, ...] | None = None
    checked = 0
    for block_permutation in permutations(range(block_count)):
        for shifts in product(range(index), repeat=block_count):
            old_to_new = qc_coordinate_permutation(index, block_count, block_permutation, shifts)
            canonical = tuple(sorted(permute_codeword_set(source, length, old_to_new)))
            checked += 1
            if best is None or canonical < best:
                best = canonical

    return QCCanonicalForm(
        evaluated=True,
        index=index,
        block_count=block_count,
        group_size=group_size,
        checked_permutations=checked,
        canonical_form=best,
        cost_model=f"Enumerated {checked} block-permutation/cyclic-shift coordinate permutation(s).",
        interpretation="Computed canonical form under the quasi-cyclic block automorphism group.",
    )


def _load_qc_collision_rows(path: Path = QUASI_CYCLIC_CODE_SEARCH_PATH) -> list[tuple[str, dict[str, Any]]]:
    if not path.exists():
        return []
    payload = json.loads(path.read_text())
    rows: list[tuple[str, dict[str, Any]]] = []
    for record in payload.get("records", []):
        source_id = str(record.get("spec", {}).get("id", "unknown"))
        for audit in record.get("collision_audits", []):
            if audit.get("generator_a") and audit.get("generator_b"):
                rows.append((source_id, audit))
    return rows


def audit_qc_collision(
    source_search_id: str,
    audit: dict[str, Any],
    max_group_size: int = 250_000,
) -> QCCanonicalizationRecord:
    left = np.asarray(audit["generator_a"], dtype=np.uint8)
    right = np.asarray(audit["generator_b"], dtype=np.uint8)
    dimension = int(audit.get("dimension", left.shape[0]))
    length = int(audit.get("length", left.shape[1]))
    index = dimension
    block_count = length // index if index else 0
    left_form = qc_canonical_form(left, index=index, max_group_size=max_group_size)
    right_form = qc_canonical_form(right, index=index, max_group_size=max_group_size)
    canonical_equal = (
        left_form.canonical_form == right_form.canonical_form
        if left_form.evaluated and right_form.evaluated
        else None
    )
    tuple_status = str(audit.get("tuple_profile_status", "unknown"))
    if tuple_status == "rejected-by-coordinate-tuple-profile":
        status = "rejected-by-higher-tuple-profile"
        interpretation = (
            "The row is already separated by a higher-order coordinate tuple profile; no quantum observable should "
            "treat it as hard code-equivalence evidence."
        )
    elif canonical_equal is True:
        status = "equivalent-under-qc-automorphism-control"
        interpretation = (
            "The tuple-profile collision is equivalent under quasi-cyclic block permutations and cyclic shifts; "
            "it is a structured control, not hard evidence."
        )
    elif canonical_equal is False:
        status = "qc-automorphism-no-equivalence-proof-debt"
        interpretation = (
            "No equivalence was found inside the quasi-cyclic automorphism group.  This does not prove full "
            "non-equivalence; keep the row as proof debt for stronger canonicalization."
        )
    else:
        status = "qc-automorphism-canonicalization-proof-debt"
        interpretation = "QC automorphism canonicalization was skipped or incomplete; keep the row as proof debt."

    return QCCanonicalizationRecord(
        id=str(audit.get("id", "unknown")),
        source_search_id=source_search_id,
        length=length,
        dimension=dimension,
        index=index,
        block_count=block_count,
        tuple_profile_status=tuple_status,
        unrestricted_estimated_assignments=int(audit.get("estimated_assignments", 0) or 0),
        left_canonical=left_form,
        right_canonical=right_form,
        qc_canonical_equal=canonical_equal,
        status=status,
        interpretation=interpretation,
    )


def run_qc_canonicalization(
    max_group_size: int = 250_000,
    source_path: Path = QUASI_CYCLIC_CODE_SEARCH_PATH,
) -> QCCanonicalizationReport:
    rows = _load_qc_collision_rows(source_path)
    records = [audit_qc_collision(source_id, audit, max_group_size=max_group_size) for source_id, audit in rows]
    metrics = {
        "record_count": len(records),
        "evaluated_count": sum(1 for record in records if record.left_canonical.evaluated and record.right_canonical.evaluated),
        "equivalent_control_count": sum(1 for record in records if record.status == "equivalent-under-qc-automorphism-control"),
        "tuple_profile_rejection_count": sum(1 for record in records if record.status == "rejected-by-higher-tuple-profile"),
        "qc_no_equivalence_proof_debt_count": sum(1 for record in records if record.status == "qc-automorphism-no-equivalence-proof-debt"),
        "canonicalization_cap_proof_debt_count": sum(
            1 for record in records if record.status == "qc-automorphism-canonicalization-proof-debt"
        ),
        "max_qc_group_size": max((record.left_canonical.group_size for record in records), default=0),
        "max_unrestricted_estimated_assignments": max((record.unrestricted_estimated_assignments for record in records), default=0),
    }
    rejected = metrics["tuple_profile_rejection_count"]
    proof_debt = metrics["qc_no_equivalence_proof_debt_count"] + metrics["canonicalization_cap_proof_debt_count"]
    if proof_debt:
        status = "qc-automorphism-proof-debt"
    elif metrics["equivalent_control_count"] or rejected:
        status = "qc-automorphism-controls-dequantized"
    else:
        status = "qc-automorphism-no-rows"
    summary = (
        f"Audited {metrics['record_count']} quasi-cyclic tuple-profile collision row(s) under block automorphisms. "
        f"{metrics['equivalent_control_count']} were equivalent controls; {rejected} were tuple-profile rejections; "
        f"{proof_debt} remain proof debt."
    )
    falsifiers = []
    if metrics["equivalent_control_count"]:
        falsifiers.append("Some quasi-cyclic tuple-profile collisions are equivalent under block automorphisms.")
    if rejected:
        falsifiers.append("Some quasi-cyclic rows are separated by higher-order coordinate tuple profiles.")
    if proof_debt:
        falsifiers.append("Rows not resolved by QC automorphisms require stronger canonicalization before observable search.")
    if not records:
        falsifiers.append("No quasi-cyclic collision rows were available to audit.")
    return QCCanonicalizationReport(utc_now(), records, max_group_size, metrics, status, summary, falsifiers)


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


def write_qc_canonicalization_negative_results(report: QCCanonicalizationReport) -> int:
    written = 0
    for record in report.records:
        if record.status not in {"equivalent-under-qc-automorphism-control", "rejected-by-higher-tuple-profile"}:
            continue
        upsert_negative_result(
            NegativeResultRecord(
                id=f"QC-AUTOMORPHISM-REJECTED-{_safe_id(record.id)}",
                source="quasi_cyclic_canonicalization.py",
                claim=f"{record.id} quasi-cyclic tuple-profile collision supplies hard code-equivalence evidence.",
                reason_invalid=record.interpretation,
                lesson=(
                    "Quasi-cyclic tuple-profile collisions must survive the natural block automorphism group before "
                    "they can be used as hard code-equivalence rows."
                ),
                applies_to=["CODE-COSET-COLLECTIVE", "PO-DEQUANTIZATION", "PO-FALSIFIERS"],
                evidence=asdict(record),
            )
        )
        written += 1
    return written


def write_qc_canonicalization_report(
    output_path: Path = QC_CANONICALIZATION_PATH,
    max_group_size: int = 250_000,
    write_registry: bool = True,
    registry_experiment_id: str = "EXP-CODE-QC-AUTOMORPHISM-CANONICALIZATION",
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "RESULT-CODE-QC-AUTOMORPHISM-CANONICALIZATION-LATEST",
) -> dict[str, Any]:
    report = run_qc_canonicalization(max_group_size=max_group_size)
    payload = _json_ready(report)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    if write_registry:
        negative_results_written = write_qc_canonicalization_negative_results(report)
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
                artifacts={"quasi_cyclic_canonicalization": str(output_path)},
            )
        )
    return payload
