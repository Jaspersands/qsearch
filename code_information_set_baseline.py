"""Information-set canonicalization baseline for binary code equivalence.

Information-set enumeration is a standard classical attack surface for code
equivalence.  For each independent ordered coordinate basis, this baseline puts
the generator in systematic form and canonicalizes the remaining columns as a
multiset.  Equal signatures are not a hardness proof; differing signatures are
classical rejection evidence.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, is_dataclass
from itertools import combinations, permutations
from pathlib import Path
from typing import Any

import numpy as np

from code_canonicalization_baseline import default_code_canonicalization_pairs
from code_equivalence_workbench import gf2_rank
from research_registry import ExperimentResultRecord, NegativeResultRecord, upsert_experiment_result, upsert_negative_result, utc_now


CODE_EQUIVALENCE_DIR = Path("research/code_equivalence")
CODE_INFORMATION_SET_BASELINE_PATH = CODE_EQUIVALENCE_DIR / "code_information_set_baseline.json"


@dataclass(frozen=True)
class InformationSetCanonicalForm:
    evaluated: bool
    independent_set_count: int
    ordered_information_set_count: int
    estimated_ordered_information_sets: int
    canonical_signature: tuple[int, ...] | None
    cost_model: str
    interpretation: str


@dataclass(frozen=True)
class CodeInformationSetRecord:
    id: str
    source: str
    length: int
    dimension: int
    known_equivalent: bool | None
    left_form: InformationSetCanonicalForm
    right_form: InformationSetCanonicalForm
    canonical_equal: bool | None
    status: str
    interpretation: str


@dataclass(frozen=True)
class CodeInformationSetReport:
    created_at: str
    records: list[CodeInformationSetRecord]
    max_ordered_information_sets: int
    include_code_family_search: bool
    headline_metrics: dict[str, int]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _gf2_inverse(matrix: np.ndarray) -> np.ndarray | None:
    values = np.asarray(matrix, dtype=np.uint8).copy() & 1
    rows, cols = values.shape
    if rows != cols:
        return None
    inverse = np.eye(rows, dtype=np.uint8)
    rank = 0
    for col in range(cols):
        pivot = None
        for row in range(rank, rows):
            if values[row, col]:
                pivot = row
                break
        if pivot is None:
            return None
        if pivot != rank:
            values[[rank, pivot]] = values[[pivot, rank]]
            inverse[[rank, pivot]] = inverse[[pivot, rank]]
        for row in range(rows):
            if row != rank and values[row, col]:
                values[row] ^= values[rank]
                inverse[row] ^= inverse[rank]
        rank += 1
    return inverse


def _column_ints(matrix: np.ndarray) -> tuple[int, ...]:
    values = []
    for col in range(matrix.shape[1]):
        encoded = 0
        for row, bit in enumerate(matrix[:, col].tolist()):
            if bit:
                encoded |= 1 << row
        values.append(encoded)
    return tuple(values)


def information_set_canonical_form(
    generator: np.ndarray,
    max_ordered_information_sets: int = 250_000,
) -> InformationSetCanonicalForm:
    matrix = np.asarray(generator, dtype=np.uint8) & 1
    dimension, length = matrix.shape
    estimated = 1
    for value in range(length - dimension + 1, length + 1):
        estimated *= value
    if estimated > max_ordered_information_sets:
        return InformationSetCanonicalForm(
            evaluated=False,
            independent_set_count=0,
            ordered_information_set_count=0,
            estimated_ordered_information_sets=estimated,
            canonical_signature=None,
            cost_model=(
                f"Skipped full ordered information-set enumeration: P({length},{dimension})={estimated} exceeds cap "
                f"{max_ordered_information_sets}."
            ),
            interpretation="Information-set canonicalization exceeded the cap; keep this row as proof debt.",
        )

    best: tuple[int, ...] | None = None
    independent_sets = 0
    ordered_sets = 0
    columns = list(range(length))
    for info_set in combinations(columns, dimension):
        basis = matrix[:, list(info_set)]
        if gf2_rank(basis) != dimension:
            continue
        independent_sets += 1
        complement = [col for col in columns if col not in set(info_set)]
        for ordered_info_set in permutations(info_set):
            ordered_sets += 1
            ordered_basis = matrix[:, list(ordered_info_set)]
            inverse = _gf2_inverse(ordered_basis)
            if inverse is None:
                continue
            systematic_suffix = (inverse @ matrix[:, complement]) & 1
            suffix_signature = tuple(sorted(_column_ints(systematic_suffix)))
            if best is None or suffix_signature < best:
                best = suffix_signature

    return InformationSetCanonicalForm(
        evaluated=True,
        independent_set_count=independent_sets,
        ordered_information_set_count=ordered_sets,
        estimated_ordered_information_sets=estimated,
        canonical_signature=best,
        cost_model=(
            f"Enumerated {independent_sets} independent information set(s) and {ordered_sets} ordered basis choice(s) "
            f"under cap {max_ordered_information_sets}."
        ),
        interpretation="Computed a canonical systematic-form suffix-column multiset over ordered information sets.",
    )


def audit_code_information_set_pair(
    record_id: str,
    source: str,
    left: np.ndarray,
    right: np.ndarray,
    known_equivalent: bool | None = None,
    max_ordered_information_sets: int = 250_000,
) -> CodeInformationSetRecord:
    left = np.asarray(left, dtype=np.uint8) & 1
    right = np.asarray(right, dtype=np.uint8) & 1
    left_form = information_set_canonical_form(left, max_ordered_information_sets=max_ordered_information_sets)
    right_form = information_set_canonical_form(right, max_ordered_information_sets=max_ordered_information_sets)
    canonical_equal = (
        left_form.canonical_signature == right_form.canonical_signature
        if left_form.evaluated and right_form.evaluated
        else None
    )
    if canonical_equal is False:
        status = "rejected-by-information-set-canonicalization"
        interpretation = "Information-set canonical signatures differ; this row is classically rejected."
    elif canonical_equal is True and known_equivalent:
        status = "information-set-equivalent-control"
        interpretation = "Information-set canonical signatures match on a known equivalent control pair."
    elif canonical_equal is True:
        status = "information-set-survivor-proof-debt"
        interpretation = (
            "Information-set canonical signatures match. This is proof debt, not positive evidence; compare against "
            "automorphism-aware canonicalization and lower-bound obligations."
        )
    else:
        status = "information-set-cap-proof-debt"
        interpretation = "Information-set canonicalization exceeded the configured cap."
    return CodeInformationSetRecord(
        id=record_id,
        source=source,
        length=int(left.shape[1]),
        dimension=int(left.shape[0]),
        known_equivalent=known_equivalent,
        left_form=left_form,
        right_form=right_form,
        canonical_equal=canonical_equal,
        status=status,
        interpretation=interpretation,
    )


def run_code_information_set_baseline(
    max_ordered_information_sets: int = 250_000,
    include_code_family_search: bool = True,
) -> CodeInformationSetReport:
    records = [
        audit_code_information_set_pair(
            record_id,
            source,
            left,
            right,
            known_equivalent=known_equivalent,
            max_ordered_information_sets=max_ordered_information_sets,
        )
        for record_id, source, left, right, known_equivalent in default_code_canonicalization_pairs(
            include_code_family_search=include_code_family_search
        )
    ]
    metrics = {
        "record_count": len(records),
        "information_set_rejection_count": sum(
            1 for record in records if record.status == "rejected-by-information-set-canonicalization"
        ),
        "equivalent_control_count": sum(1 for record in records if record.status == "information-set-equivalent-control"),
        "survivor_proof_debt_count": sum(1 for record in records if record.status == "information-set-survivor-proof-debt"),
        "cap_proof_debt_count": sum(1 for record in records if record.status == "information-set-cap-proof-debt"),
        "max_ordered_information_sets_evaluated": max(
            (max(record.left_form.ordered_information_set_count, record.right_form.ordered_information_set_count) for record in records),
            default=0,
        ),
    }
    proof_debt = metrics["survivor_proof_debt_count"] + metrics["cap_proof_debt_count"]
    if proof_debt:
        status = "code-information-set-proof-debt"
    elif metrics["information_set_rejection_count"]:
        status = "code-rows-dequantized-by-information-set-canonicalization"
    else:
        status = "information-set-controls-only"
    summary = (
        f"Audited {metrics['record_count']} code-equivalence row(s) by information-set canonicalization. "
        f"{metrics['information_set_rejection_count']} row(s) were rejected; {proof_debt} remain proof debt."
    )
    falsifiers = []
    if metrics["information_set_rejection_count"]:
        falsifiers.append("Information-set canonicalization separates current code-equivalence rows.")
    if proof_debt:
        falsifiers.append("Information-set survivors/cap rows remain proof debt, not positive evidence.")
    return CodeInformationSetReport(
        utc_now(),
        records,
        max_ordered_information_sets,
        include_code_family_search,
        metrics,
        status,
        summary,
        falsifiers,
    )


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


def write_code_information_set_negative_results(report: CodeInformationSetReport) -> int:
    written = 0
    for record in report.records:
        if record.status != "rejected-by-information-set-canonicalization":
            continue
        upsert_negative_result(
            NegativeResultRecord(
                id=f"CODE-INFORMATION-SET-REJECTED-{_safe_id(record.id)}",
                source="code_information_set_baseline.py",
                claim=f"{record.id} supplies hard code-equivalence coset evidence beyond information-set baselines.",
                reason_invalid=record.interpretation,
                lesson=(
                    "Rows separated by information-set canonicalization are classical negative evidence. Survivors still need "
                    "automorphism-aware canonicalization and lower-bound support."
                ),
                applies_to=["CODE-COSET-COLLECTIVE", "PO-DEQUANTIZATION", "PO-FALSIFIERS"],
                evidence={
                    "record_id": record.id,
                    "source": record.source,
                    "status": record.status,
                    "left_ordered_information_sets": record.left_form.ordered_information_set_count,
                    "right_ordered_information_sets": record.right_form.ordered_information_set_count,
                },
            )
        )
        written += 1
    return written


def write_code_information_set_baseline(
    output_path: Path = CODE_INFORMATION_SET_BASELINE_PATH,
    max_ordered_information_sets: int = 250_000,
    include_code_family_search: bool = True,
    write_registry: bool = True,
    registry_experiment_id: str = "EXP-CODE-INFORMATION-SET-CANONICALIZATION",
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "RESULT-CODE-INFORMATION-SET-CANONICALIZATION-LATEST",
) -> dict[str, Any]:
    report = run_code_information_set_baseline(
        max_ordered_information_sets=max_ordered_information_sets,
        include_code_family_search=include_code_family_search,
    )
    payload = _json_ready(report)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    if write_registry:
        negative_results_written = write_code_information_set_negative_results(report)
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
                artifacts={"code_information_set_baseline": str(output_path)},
            )
        )
    return payload
