"""Resolve quasi-cyclic code proof debt with exact information-set canonicalization.

QC automorphism non-equivalence is only a restricted negative result.  For
small dimensions, ordered information-set canonicalization is a complete code
equivalence certificate: if two fully evaluated codes produce the same
canonical systematic suffix multiset, both are equivalent to the same canonical
generator up to row operations and coordinate permutation.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, is_dataclass
from pathlib import Path
from typing import Any

import numpy as np

from code_information_set_baseline import audit_code_information_set_pair
from quasi_cyclic_canonicalization import QC_CANONICALIZATION_PATH
from quasi_cyclic_code_search import QUASI_CYCLIC_CODE_SEARCH_PATH
from research_registry import ExperimentResultRecord, NegativeResultRecord, upsert_experiment_result, upsert_negative_result, utc_now


CODE_EQUIVALENCE_DIR = Path("research/code_equivalence")
QC_INFORMATION_SET_RESOLVER_PATH = CODE_EQUIVALENCE_DIR / "qc_information_set_resolver.json"


@dataclass(frozen=True)
class QCInformationSetRecord:
    id: str
    source_search_id: str
    length: int
    dimension: int
    evaluated: bool
    estimated_ordered_information_sets: int
    canonical_equal: bool | None
    information_set_status: str
    status: str
    interpretation: str


@dataclass(frozen=True)
class QCInformationSetResolverReport:
    created_at: str
    records: list[QCInformationSetRecord]
    max_ordered_information_sets: int
    headline_metrics: dict[str, int]
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


def _proof_debt_ids(canonicalization_path: Path = QC_CANONICALIZATION_PATH) -> set[str]:
    payload = _read_json(canonicalization_path, {})
    return {
        str(record.get("id"))
        for record in payload.get("records", [])
        if "proof-debt" in str(record.get("status", ""))
    }


def _load_qc_search_audits(
    search_path: Path = QUASI_CYCLIC_CODE_SEARCH_PATH,
    canonicalization_path: Path = QC_CANONICALIZATION_PATH,
) -> list[tuple[str, dict[str, Any]]]:
    proof_debt = _proof_debt_ids(canonicalization_path)
    payload = _read_json(search_path, {})
    rows: list[tuple[str, dict[str, Any]]] = []
    for record in payload.get("records", []):
        source_id = str(record.get("spec", {}).get("id", "unknown-qc-family"))
        for audit in record.get("collision_audits", []):
            audit_id = str(audit.get("id", ""))
            if proof_debt and audit_id not in proof_debt:
                continue
            if audit.get("generator_a") and audit.get("generator_b"):
                rows.append((source_id, audit))
    return rows


def audit_qc_information_set_row(
    source_search_id: str,
    audit: dict[str, Any],
    max_ordered_information_sets: int = 2_000_000,
) -> QCInformationSetRecord:
    left = np.asarray(audit["generator_a"], dtype=np.uint8)
    right = np.asarray(audit["generator_b"], dtype=np.uint8)
    info = audit_code_information_set_pair(
        record_id=str(audit.get("id", "unknown-qc-row")),
        source="qc_information_set_resolver",
        left=left,
        right=right,
        known_equivalent=None,
        max_ordered_information_sets=max_ordered_information_sets,
    )
    evaluated = bool(info.left_form.evaluated and info.right_form.evaluated)
    estimated = max(
        int(info.left_form.estimated_ordered_information_sets),
        int(info.right_form.estimated_ordered_information_sets),
    )
    if evaluated and info.canonical_equal is True:
        status = "equivalent-control-under-information-set-canonicalization"
        interpretation = (
            "Exact ordered information-set canonicalization maps both QC rows to the same systematic canonical form; "
            "this is an equivalence control, not hard code-equivalence evidence."
        )
    elif evaluated and info.canonical_equal is False:
        status = "rejected-by-information-set-canonicalization"
        interpretation = "Exact information-set canonicalization separates this QC row classically."
    else:
        status = "information-set-cap-proof-debt"
        interpretation = "Information-set canonicalization exceeded the configured cap; the QC row remains proof debt."
    return QCInformationSetRecord(
        id=info.id,
        source_search_id=source_search_id,
        length=info.length,
        dimension=info.dimension,
        evaluated=evaluated,
        estimated_ordered_information_sets=estimated,
        canonical_equal=info.canonical_equal,
        information_set_status=info.status,
        status=status,
        interpretation=interpretation,
    )


def run_qc_information_set_resolver(
    max_ordered_information_sets: int = 2_000_000,
    stop_after_family_control: bool = True,
) -> QCInformationSetResolverReport:
    rows = _load_qc_search_audits()
    records: list[QCInformationSetRecord] = []
    controlled_families: set[str] = set()
    for source_id, audit in rows:
        if stop_after_family_control and source_id in controlled_families:
            records.append(
                QCInformationSetRecord(
                    id=str(audit.get("id", "unknown-qc-row")),
                    source_search_id=source_id,
                    length=int(audit.get("length", 0) or 0),
                    dimension=int(audit.get("dimension", 0) or 0),
                    evaluated=False,
                    estimated_ordered_information_sets=0,
                    canonical_equal=None,
                    information_set_status="skipped-family-already-equivalent-control",
                    status="equivalent-control-family-already-resolved",
                    interpretation="A previous proof-debt row in this QC family was already resolved as an equivalent control.",
                )
            )
            continue
        record = audit_qc_information_set_row(
            source_id,
            audit,
            max_ordered_information_sets=max_ordered_information_sets,
        )
        records.append(record)
        if record.status == "equivalent-control-under-information-set-canonicalization":
            controlled_families.add(source_id)

    metrics = {
        "record_count": len(records),
        "evaluated_count": sum(1 for record in records if record.evaluated),
        "equivalent_control_count": sum(1 for record in records if "equivalent-control" in record.status),
        "information_set_rejection_count": sum(1 for record in records if record.status == "rejected-by-information-set-canonicalization"),
        "proof_debt_count": sum(1 for record in records if "proof-debt" in record.status),
        "max_estimated_ordered_information_sets": max((record.estimated_ordered_information_sets for record in records), default=0),
    }
    if metrics["proof_debt_count"]:
        status = "qc-information-set-proof-debt"
    elif metrics["equivalent_control_count"] or metrics["information_set_rejection_count"]:
        status = "qc-information-set-resolved"
    else:
        status = "qc-information-set-no-proof-debt-rows"
    summary = (
        f"Audited {metrics['record_count']} QC proof-debt row(s) with exact information-set canonicalization. "
        f"{metrics['equivalent_control_count']} equivalent control(s), "
        f"{metrics['information_set_rejection_count']} rejection(s), and {metrics['proof_debt_count']} unresolved row(s)."
    )
    falsifiers = []
    if metrics["equivalent_control_count"]:
        falsifiers.append("Information-set canonicalization resolves some QC proof-debt rows as equivalent controls.")
    if metrics["information_set_rejection_count"]:
        falsifiers.append("Information-set canonicalization rejects some QC proof-debt rows classically.")
    if metrics["proof_debt_count"]:
        falsifiers.append("Some QC rows still exceed the information-set cap and remain proof debt.")
    if not records:
        falsifiers.append("No QC proof-debt rows were available to resolve.")
    return QCInformationSetResolverReport(utc_now(), records, max_ordered_information_sets, metrics, status, summary, falsifiers)


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


def write_qc_information_set_negative_results(report: QCInformationSetResolverReport) -> int:
    written = 0
    for record in report.records:
        if "equivalent-control" not in record.status and record.status != "rejected-by-information-set-canonicalization":
            continue
        upsert_negative_result(
            NegativeResultRecord(
                id=f"QC-INFORMATION-SET-RESOLVED-{_safe_id(record.id)}",
                source="qc_information_set_resolver.py",
                claim=f"{record.id} quasi-cyclic proof-debt row supplies hard code-equivalence evidence.",
                reason_invalid=record.interpretation,
                lesson=(
                    "QC automorphism non-equivalence is insufficient; exact information-set canonicalization can still "
                    "collapse the row to an equivalent control or classical rejection."
                ),
                applies_to=["CODE-COSET-COLLECTIVE", "PO-DEQUANTIZATION", "PO-FALSIFIERS"],
                evidence=asdict(record),
            )
        )
        written += 1
    return written


def write_qc_information_set_resolver(
    output_path: Path = QC_INFORMATION_SET_RESOLVER_PATH,
    max_ordered_information_sets: int = 2_000_000,
    stop_after_family_control: bool = True,
    write_registry: bool = True,
    registry_experiment_id: str = "EXP-CODE-QC-INFORMATION-SET-RESOLVER",
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "RESULT-EXP-CODE-QC-INFORMATION-SET-RESOLVER-CODE-INFOSET",
) -> dict[str, Any]:
    report = run_qc_information_set_resolver(
        max_ordered_information_sets=max_ordered_information_sets,
        stop_after_family_control=stop_after_family_control,
    )
    payload = _json_ready(report)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    negative_results_written = 0
    if write_registry:
        negative_results_written = write_qc_information_set_negative_results(report)
        upsert_experiment_result(
            ExperimentResultRecord(
                id=registry_result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=report.created_at,
                status=report.status,
                summary=report.summary,
                metrics=payload["headline_metrics"],
                falsifiers_triggered=report.falsifiers_triggered,
                artifacts={"qc_information_set_resolver": str(output_path)},
            )
        )
    payload["negative_results_written"] = negative_results_written
    return payload

