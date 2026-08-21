"""Aggregate coset/nonabelian frontier rows across classical baselines.

The project should not design collective measurements for rows already killed
by WL, graphlet/tensor, individualization, rooted tensor, or promised CFI
structural decoders.  This module builds the gate: per graph/coset row it
collects baseline evidence, rejects dequantized rows, and marks unresolved rows
as proof debt rather than positive evidence.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, is_dataclass
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


COSET_WORKBENCH_DIR = Path("research/coset_workbench")
COSET_FRONTIER_TRIAGE_PATH = COSET_WORKBENCH_DIR / "coset_frontier_triage.json"
COSET_AUDIT_PATH = COSET_WORKBENCH_DIR / "nonabelian_hsp_audit.json"
COLLECTIVE_OBSERVABLE_SEARCH_PATH = COSET_WORKBENCH_DIR / "collective_observable_search.json"
GRAPHLET_TENSOR_OBSERVABLES_PATH = COSET_WORKBENCH_DIR / "graphlet_tensor_observables.json"
GODSIL_MCKAY_SEARCH_PATH = COSET_WORKBENCH_DIR / "godsil_mckay_switching_search.json"
INDIVIDUALIZED_WL_BASELINE_PATH = COSET_WORKBENCH_DIR / "individualized_wl_baseline.json"
INDIVIDUALIZED_TENSOR_OBSERVABLES_PATH = COSET_WORKBENCH_DIR / "individualized_tensor_observables.json"
CFI_BASE_FAMILY_SEARCH_PATH = COSET_WORKBENCH_DIR / "cfi_base_family_search.json"
CFI_SCALING_PROBE_PATH = COSET_WORKBENCH_DIR / "cfi_scaling_probe.json"
CFI_PARITY_SOLVER_PATH = COSET_WORKBENCH_DIR / "cfi_parity_solver.json"
CFI_STRUCTURAL_DECODER_PATH = COSET_WORKBENCH_DIR / "cfi_structural_decoder.json"
CFI_IRREGULAR_STRUCTURAL_DECODER_PATH = COSET_WORKBENCH_DIR / "cfi_irregular_structural_decoder.json"
CFI_BIPARTITE_STRUCTURAL_DECODER_PATH = COSET_WORKBENCH_DIR / "cfi_bipartite_structural_decoder.json"


@dataclass(frozen=True)
class CosetTriageEvidence:
    source: str
    status: str
    verdict: str
    detail: str


@dataclass(frozen=True)
class CosetFrontierTriageRecord:
    pair_id: str
    graph_a: str
    graph_b: str
    vertex_count: int
    evidence: list[CosetTriageEvidence]
    final_status: str
    required_next_step: str


@dataclass(frozen=True)
class CosetFrontierTriageReport:
    created_at: str
    records: list[CosetFrontierTriageRecord]
    headline_metrics: dict[str, int]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _read_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError:
        return fallback


def _classify_status(status: str) -> str:
    lower = status.lower()
    if "dequantized" in lower or "classical-shadow-collapse" in lower or "classical-shadow" in lower:
        return "dequantizing"
    if "proof-debt" in lower or "boundary" in lower or "skipped" in lower or "needs" in lower or "ambiguous" in lower:
        return "proof-debt"
    if "survives" in lower or "no-signal" in lower or "no-current-observable" in lower:
        return "survivor"
    return "unclassified"


def _pair_stub(pair_id: str) -> dict[str, Any]:
    return {
        "id": pair_id,
        "graph_a": pair_id,
        "graph_b": pair_id,
        "vertex_count": 0,
    }


def _add_evidence(
    rows: dict[str, dict[str, Any]],
    pair: dict[str, Any],
    source: str,
    status: str,
    detail: str,
) -> None:
    pair_id = str(pair.get("id", "unknown"))
    if pair_id not in rows:
        rows[pair_id] = {
            "pair": {
                "id": pair_id,
                "graph_a": pair.get("graph_a", pair_id),
                "graph_b": pair.get("graph_b", pair_id),
                "vertex_count": int(pair.get("vertex_count", 0) or 0),
            },
            "evidence": [],
        }
    rows[pair_id]["evidence"].append(
        CosetTriageEvidence(
            source=source,
            status=status,
            verdict=_classify_status(status),
            detail=detail,
        )
    )


def _collect_pair_audits(
    rows: dict[str, dict[str, Any]],
    path: Path,
    source: str,
) -> None:
    payload = _read_json(path, {})
    for audit in payload.get("pair_audits", []):
        pair = dict(audit.get("pair", {}))
        status_value = audit.get("status", audit.get("boundary_status"))
        if status_value is None:
            positive_signal = str(audit.get("positive_signal", ""))
            falsifiers = list(audit.get("falsifiers_triggered", []))
            if falsifiers:
                status_value = "dequantized-by-coset-workbench-falsifier"
            elif "boundary" in positive_signal.lower():
                status_value = "boundary-survives-current-coset-workbench"
            else:
                status_value = positive_signal or "unknown"
        status = str(status_value)
        falsifiers = audit.get("falsifiers_triggered", [])
        detail = "; ".join(str(item) for item in falsifiers) or payload.get("summary", source)
        _add_evidence(rows, pair, source, status, detail)


def _base_record_pair(record: dict[str, Any]) -> dict[str, Any]:
    base = dict(record.get("base", {}))
    base_id = str(record.get("base_id") or record.get("id") or base.get("id") or "unknown")
    description = str(base.get("description") or base_id)
    if base_id.startswith("complete-k") and base_id.removeprefix("complete-k").isdigit():
        base_size = int(base_id.removeprefix("complete-k"))
        return {
            "id": f"cfi-k{base_size}-parity-twist",
            "graph_a": f"Untwisted complete-CFI K{base_size}",
            "graph_b": f"Single-edge twisted complete-CFI K{base_size}",
            "vertex_count": int(record.get("cfi_vertex_count", record.get("vertex_count", 0)) or 0),
        }
    return {
        "id": f"cfi-base-{base_id}",
        "graph_a": f"Untwisted CFI parity graph over {description}",
        "graph_b": f"Single-edge twisted CFI parity graph over {description}",
        "vertex_count": int(record.get("cfi_vertex_count", record.get("vertex_count", 0)) or 0),
    }


def _collect_cfi_base_family(rows: dict[str, dict[str, Any]], path: Path = CFI_BASE_FAMILY_SEARCH_PATH) -> None:
    payload = _read_json(path, {})
    for record in payload.get("records", []):
        _add_evidence(
            rows,
            _base_record_pair(record),
            "cfi_base_family_search",
            str(record.get("status", "unknown")),
            str(record.get("interpretation", "")),
        )


def _collect_cfi_scaling(rows: dict[str, dict[str, Any]], path: Path = CFI_SCALING_PROBE_PATH) -> None:
    payload = _read_json(path, {})
    for record in payload.get("records", []):
        base_size = int(record.get("base_size", 0) or 0)
        if not base_size:
            continue
        pair = {
            "id": f"cfi-k{base_size}-parity-twist",
            "graph_a": f"Untwisted complete-CFI K{base_size}",
            "graph_b": f"Single-edge twisted complete-CFI K{base_size}",
            "vertex_count": int(record.get("vertex_count", 0) or 0),
        }
        _add_evidence(
            rows,
            pair,
            "cfi_scaling_probe",
            str(record.get("status", "unknown")),
            str(record.get("interpretation", "")),
        )


def _collect_cfi_parity(rows: dict[str, dict[str, Any]], path: Path = CFI_PARITY_SOLVER_PATH) -> None:
    payload = _read_json(path, {})
    for record in payload.get("records", []):
        base_size = int(record.get("base_size", 0) or 0)
        if not base_size:
            continue
        pair_id = f"cfi-k{base_size}-parity-twist"
        pair = {
            "id": pair_id,
            "graph_a": f"Untwisted complete-CFI K{base_size}",
            "graph_b": f"Single-edge twisted complete-CFI K{base_size}",
            "vertex_count": int(record.get("vertex_count", 0) or 0),
        }
        _add_evidence(
            rows,
            pair,
            "cfi_parity_solver",
            str(record.get("status", "unknown")),
            str(record.get("interpretation", "")),
        )


def _collect_godsil_mckay(rows: dict[str, dict[str, Any]], path: Path = GODSIL_MCKAY_SEARCH_PATH) -> None:
    payload = _read_json(path, {})
    for family in payload.get("family_records", []):
        for record in family.get("records", []):
            pair = dict(record.get("pair", _pair_stub(record.get("id", "unknown"))))
            baselines = [
                item.get("name", "unknown")
                for item in record.get("baselines", [])
                if item.get("distinguishes")
            ]
            detail = record.get("interpretation", "")
            if baselines:
                detail = f"{detail} Distinguishing baselines: {', '.join(baselines)}."
            _add_evidence(
                rows,
                pair,
                "godsil_mckay_search",
                str(record.get("status", "unknown")),
                detail,
            )


def _collect_cfi_structural(
    rows: dict[str, dict[str, Any]],
    path: Path,
    source: str,
) -> None:
    payload = _read_json(path, {})
    for record in payload.get("records", []):
        _add_evidence(
            rows,
            _base_record_pair(record),
            source,
            str(record.get("status", "unknown")),
            str(record.get("interpretation", "")),
        )


def build_coset_frontier_triage() -> CosetFrontierTriageReport:
    rows: dict[str, dict[str, Any]] = {}
    _collect_pair_audits(rows, COSET_AUDIT_PATH, "coset_state_workbench")
    _collect_pair_audits(rows, COLLECTIVE_OBSERVABLE_SEARCH_PATH, "collective_observable_search")
    _collect_pair_audits(rows, GRAPHLET_TENSOR_OBSERVABLES_PATH, "graphlet_tensor_observables")
    _collect_godsil_mckay(rows)
    _collect_pair_audits(rows, INDIVIDUALIZED_WL_BASELINE_PATH, "individualized_wl_baseline")
    _collect_pair_audits(rows, INDIVIDUALIZED_TENSOR_OBSERVABLES_PATH, "individualized_tensor_observables")
    _collect_cfi_base_family(rows)
    _collect_cfi_scaling(rows)
    _collect_cfi_parity(rows)
    _collect_cfi_structural(rows, CFI_STRUCTURAL_DECODER_PATH, "cfi_structural_decoder")
    _collect_cfi_structural(rows, CFI_IRREGULAR_STRUCTURAL_DECODER_PATH, "cfi_irregular_structural_decoder")
    _collect_cfi_structural(rows, CFI_BIPARTITE_STRUCTURAL_DECODER_PATH, "cfi_bipartite_structural_decoder")

    records: list[CosetFrontierTriageRecord] = []
    for pair_id, payload in sorted(rows.items()):
        evidence: list[CosetTriageEvidence] = payload["evidence"]
        verdicts = {item.verdict for item in evidence}
        if "dequantizing" in verdicts:
            final_status = "rejected-by-classical-coset-baseline"
            required_next_step = (
                "Do not use this row for measurement design; mutate to a graph/coset family that survives the listed baselines."
            )
        elif "proof-debt" in verdicts:
            final_status = "proof-debt-not-positive-evidence"
            required_next_step = (
                "Resolve cap/ambiguity evidence with implicit baselines, stronger decoders, or a lower-bound argument before promotion."
            )
        else:
            final_status = "survives-current-baselines-measurement-proof-debt"
            required_next_step = (
                "Only now search for a polynomial-description collective measurement, and immediately compare it against stronger classical shadows."
            )
        pair = payload["pair"]
        records.append(
            CosetFrontierTriageRecord(
                pair_id=pair_id,
                graph_a=str(pair.get("graph_a", pair_id)),
                graph_b=str(pair.get("graph_b", pair_id)),
                vertex_count=int(pair.get("vertex_count", 0) or 0),
                evidence=sorted(evidence, key=lambda item: (item.source, item.status)),
                final_status=final_status,
                required_next_step=required_next_step,
            )
        )

    metrics = {
        "record_count": len(records),
        "rejected_pair_count": sum(1 for record in records if record.final_status == "rejected-by-classical-coset-baseline"),
        "proof_debt_pair_count": sum(1 for record in records if record.final_status == "proof-debt-not-positive-evidence"),
        "survivor_pair_count": sum(
            1 for record in records if record.final_status == "survives-current-baselines-measurement-proof-debt"
        ),
        "evidence_count": sum(len(record.evidence) for record in records),
        "dequantizing_evidence_count": sum(
            1 for record in records for item in record.evidence if item.verdict == "dequantizing"
        ),
        "proof_debt_evidence_count": sum(1 for record in records for item in record.evidence if item.verdict == "proof-debt"),
        "nonclassical_candidate_count": 0,
    }
    if metrics["rejected_pair_count"]:
        status = "coset-frontier-mostly-dequantized"
    elif metrics["proof_debt_pair_count"]:
        status = "coset-frontier-proof-debt"
    else:
        status = "coset-frontier-survivors-need-measurement-proof"
    summary = (
        f"Triage aggregated {metrics['record_count']} graph/coset row(s) across {metrics['evidence_count']} baseline evidence items. "
        f"{metrics['rejected_pair_count']} row(s) are rejected by classical baselines, "
        f"{metrics['proof_debt_pair_count']} remain proof debt, and {metrics['survivor_pair_count']} survive current baselines "
        "only as measurement-design proof debt."
    )
    falsifiers = []
    if metrics["rejected_pair_count"]:
        falsifiers.append("Some coset frontier rows are already dequantized by classical baselines.")
    if metrics["proof_debt_pair_count"]:
        falsifiers.append("Some coset frontier rows are cap/ambiguity proof debt, not positive evidence.")
    return CosetFrontierTriageReport(utc_now(), records, metrics, status, summary, falsifiers)


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


def write_coset_frontier_negative_results(report: CosetFrontierTriageReport) -> int:
    written = 0
    for record in report.records:
        if record.final_status != "rejected-by-classical-coset-baseline":
            continue
        dequantizing = [item for item in record.evidence if item.verdict == "dequantizing"]
        reason = "; ".join(f"{item.source}: {item.status}" for item in dequantizing[:4])
        upsert_negative_result(
            NegativeResultRecord(
                id=f"COSET-FRONTIER-TRIAGE-{_safe_id(record.pair_id)}",
                source="coset_frontier_triage.py",
                claim=f"{record.pair_id} is a viable nonabelian coset-state measurement frontier row.",
                reason_invalid=f"Classical baseline evidence rejects the row: {reason}.",
                lesson=(
                    "A graph/coset row must survive WL, tensor, individualization, rooted tensor, and structural CFI "
                    "baselines before it can motivate collective-measurement design."
                ),
                applies_to=["CODE-COSET-COLLECTIVE", "HYP-LIT-COSET-OBSERVABLES", "PO-DEQUANTIZATION"],
                evidence={
                    "pair_id": record.pair_id,
                    "vertex_count": record.vertex_count,
                    "final_status": record.final_status,
                    "dequantizing_sources": [item.source for item in dequantizing],
                },
            )
        )
        written += 1
    return written


def write_coset_frontier_triage(
    output_path: Path = COSET_FRONTIER_TRIAGE_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = "EXP-COSET-FRONTIER-TRIAGE",
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "RESULT-COSET-FRONTIER-TRIAGE-LATEST",
) -> dict[str, Any]:
    report = build_coset_frontier_triage()
    payload = _json_ready(report)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    if write_registry:
        negative_results_written = write_coset_frontier_negative_results(report)
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
                artifacts={"coset_frontier_triage": str(output_path)},
            )
        )
    return payload
