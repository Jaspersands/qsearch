"""Aggregate code-equivalence frontier rows across classical baselines.

Code-equivalence rows are only useful for nonabelian-HSP research if they
survive structural invariants, tuple profiles, information-set canonicalization,
and automorphism-aware canonicalization.  This module provides the same kind of
gate for code rows that ``coset_frontier_triage.py`` provides for graph/coset
rows: merge evidence from all code artifacts, reject classical shadows, and
label unresolved rows as proof debt rather than positive evidence.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, is_dataclass
from pathlib import Path
from typing import Any

from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


CODE_EQUIVALENCE_DIR = Path("research/code_equivalence")
CODE_FRONTIER_TRIAGE_PATH = CODE_EQUIVALENCE_DIR / "code_frontier_triage.json"
CODE_EQUIVALENCE_AUDIT_PATH = CODE_EQUIVALENCE_DIR / "code_equivalence_audit.json"
CODE_FAMILY_SEARCH_PATH = CODE_EQUIVALENCE_DIR / "code_family_search.json"
CODE_STRUCTURAL_INVARIANTS_PATH = CODE_EQUIVALENCE_DIR / "code_structural_invariants.json"
CODE_INFORMATION_SET_BASELINE_PATH = CODE_EQUIVALENCE_DIR / "code_information_set_baseline.json"
CODE_CANONICALIZATION_BASELINE_PATH = CODE_EQUIVALENCE_DIR / "code_canonicalization_baseline.json"
CODE_PROFILE_COLLISION_SEARCH_PATH = CODE_EQUIVALENCE_DIR / "code_profile_collision_search.json"
CODE_TUPLE_PROFILE_BASELINE_PATH = CODE_EQUIVALENCE_DIR / "code_tuple_profile_baseline.json"
CODE_LOW_WEIGHT_STRUCTURE_PATH = CODE_EQUIVALENCE_DIR / "code_low_weight_structure.json"
QUASI_CYCLIC_CODE_SEARCH_PATH = CODE_EQUIVALENCE_DIR / "quasi_cyclic_code_search.json"
QUASI_CYCLIC_CANONICALIZATION_PATH = CODE_EQUIVALENCE_DIR / "quasi_cyclic_canonicalization.json"
QC_INFORMATION_SET_RESOLVER_PATH = CODE_EQUIVALENCE_DIR / "qc_information_set_resolver.json"
CYCLIC_CODE_SEARCH_PATH = CODE_EQUIVALENCE_DIR / "cyclic_code_search.json"
BCH_CODE_SEARCH_PATH = CODE_EQUIVALENCE_DIR / "bch_code_search.json"
GOPPA_CODE_SEARCH_PATH = CODE_EQUIVALENCE_DIR / "goppa_code_search.json"
GOPPA_SCALING_FRONTIER_PATH = CODE_EQUIVALENCE_DIR / "goppa_scaling_frontier.json"
GOPPA_SYZYGY_FRONTIER_PATH = CODE_EQUIVALENCE_DIR / "goppa_syzygy_frontier.json"
GOPPA_HULL_PROJECTOR_PATH = CODE_EQUIVALENCE_DIR / "goppa_hull_projector_frontier.json"
TANNER_CODE_SEARCH_PATH = CODE_EQUIVALENCE_DIR / "tanner_code_search.json"
REED_MULLER_CODE_SEARCH_PATH = CODE_EQUIVALENCE_DIR / "reed_muller_code_search.json"
RANK_METRIC_CODE_SEARCH_PATH = CODE_EQUIVALENCE_DIR / "rank_metric_code_search.json"
CODE_INCIDENCE_RESOLVER_PATH = CODE_EQUIVALENCE_DIR / "code_incidence_resolver.json"
AFFINE_GEOMETRY_CODE_SEARCH_PATH = CODE_EQUIVALENCE_DIR / "affine_geometry_code_search.json"
PROJECTIVE_GEOMETRY_CODE_SEARCH_PATH = CODE_EQUIVALENCE_DIR / "projective_geometry_code_search.json"
CODE_SCHUR_FILTRATION_PATH = CODE_EQUIVALENCE_DIR / "code_schur_filtration.json"
CODE_CLOSURE_ATTACK_PATH = CODE_EQUIVALENCE_DIR / "code_closure_attack.json"
CFI_CODE_REDUCTION_PATH = CODE_EQUIVALENCE_DIR / "cfi_code_reduction.json"
HULL_PROJECTOR_REDUCTION_PATH = CODE_EQUIVALENCE_DIR / "code_hull_projector_reduction.json"


@dataclass(frozen=True)
class CodeTriageEvidence:
    source: str
    status: str
    verdict: str
    detail: str


@dataclass(frozen=True)
class CodeFrontierRecord:
    row_id: str
    row_family: str
    evidence: list[CodeTriageEvidence]
    final_status: str
    required_next_step: str


@dataclass(frozen=True)
class CodeFrontierTriageReport:
    created_at: str
    records: list[CodeFrontierRecord]
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
    if (
        "rejected" in lower
        or "dequantized" in lower
        or "classically-resolved" in lower
        or "collapses-to-gi" in lower
        or "reduced-to-gi" in lower
        or "classical" in lower and "distinguish" in lower
    ):
        return "dequantizing"
    if "equivalent-control" in lower or "all-equivalent-controls" in lower or "control" in lower or lower.startswith("equivalent-"):
        return "control"
    if "canonical-equivalent" in lower or "information-set-equivalent" in lower or "tuple-profile-equivalent" in lower:
        return "control"
    if "proof-debt" in lower or "survivor" in lower or "needs" in lower or "cap" in lower or "incomplete" in lower:
        return "proof-debt"
    if "no-" in lower and "collision" in lower:
        return "no-evidence"
    return "unclassified"


def _safe_id(value: str) -> str:
    return "".join(ch if ch.isalnum() else "_" for ch in value.upper()).strip("_")


def _qc_family_from_collision_id(row_id: str) -> str:
    if "-trial-" in row_id:
        return row_id.split("-trial-", 1)[0]
    return row_id


def _row_id_for_record(record: dict[str, Any], source: str, list_key: str) -> tuple[str, str]:
    if source == "code_equivalence_workbench":
        pair = dict(record.get("pair", {}))
        return str(pair.get("id", "unknown-code-row")), "seed-code-pair"
    spec = dict(record.get("spec", {}))
    if source == "code_family_search":
        spec_id = str(spec.get("id", "unknown-code-family"))
        return f"code-family-{spec_id}", "random-weak-invariant-family"
    if source == "code_profile_collision_search":
        return f"profile-search-{spec.get('id', 'unknown-profile-search')}", "profile-collision-search"
    if source == "code_tuple_profile_collision_search":
        return f"tuple-search-{spec.get('id', 'unknown-tuple-search')}", "tuple-profile-collision-search"
    if source == "code_low_weight_structure":
        return str(record.get("row_id", record.get("id", "unknown-low-weight-row"))), str(
            record.get("row_family", "low-weight-matroid-row")
        )
    if source == "quasi_cyclic_code_search":
        return f"qc-family-{spec.get('id', 'unknown-qc-family')}", "quasi-cyclic-family"
    if source == "quasi_cyclic_canonicalization":
        row_id = str(record.get("id", "unknown-qc-row"))
        return f"qc-family-{_qc_family_from_collision_id(row_id)}", "quasi-cyclic-family"
    if source == "qc_information_set_resolver":
        source_id = str(record.get("source_search_id", "unknown-qc-family"))
        return f"qc-family-{source_id}", "quasi-cyclic-family"
    if source == "cyclic_code_search":
        return f"cyclic-family-{spec.get('id', 'unknown-cyclic-family')}", "cyclic-code-family"
    if source == "bch_code_search":
        return f"bch-family-{spec.get('id', 'unknown-bch-family')}", "bch-code-family"
    if source == "goppa_code_search":
        return f"goppa-family-{spec.get('id', 'unknown-goppa-family')}", "goppa-code-family"
    if source == "goppa_scaling_frontier":
        return f"goppa-scaling-family-{spec.get('id', 'unknown-goppa-scaling-family')}", "punctured-goppa-scaling-family"
    if source == "goppa_syzygy_frontier":
        return f"goppa-scaling-family-{record.get('family_id', 'unknown-goppa-syzygy-family')}", "punctured-goppa-scaling-family"
    if source == "goppa_hull_projector_frontier":
        return f"goppa-scaling-family-{record.get('family_id', 'unknown-goppa-projector-family')}", "punctured-goppa-scaling-family"
    if source == "tanner_code_search":
        return f"tanner-family-{spec.get('id', 'unknown-tanner-family')}", "tanner-ldpc-family"
    if source == "reed_muller_code_search":
        return f"rm-family-{spec.get('id', 'unknown-rm-family')}", "punctured-reed-muller-family"
    if source == "rank_metric_code_search":
        return f"rank-metric-family-{spec.get('id', 'unknown-rank-metric-family')}", "binary-expanded-rank-metric-family"
    if source == "code_incidence_resolver":
        return str(record.get("triage_row_id", "unknown-incidence-family")), str(record.get("row_family", "code-pair"))
    if source == "affine_geometry_code_search":
        return f"ag-family-{spec.get('id', 'unknown-ag-family')}", "affine-geometry-code-family"
    if source == "projective_geometry_code_search":
        return f"pg-family-{spec.get('id', 'unknown-pg-family')}", "projective-geometry-code-family"
    if source == "code_schur_filtration":
        return str(record.get("triage_row_id", "unknown-schur-family")), str(record.get("row_family", "code-pair"))
    if source == "code_closure_attack":
        return str(record.get("triage_row_id", "unknown-closure-family")), str(record.get("row_family", "code-pair"))
    if source == "cfi_code_reduction":
        return f"cfi-code-{record.get('base_id', 'unknown-cfi-base')}", "faithful-cfi-graph-code-reduction"
    return str(record.get("id", "unknown-code-row")), "code-pair"


def _add_evidence(
    rows: dict[str, dict[str, Any]],
    row_id: str,
    row_family: str,
    source: str,
    status: str,
    detail: str,
) -> None:
    rows.setdefault(row_id, {"row_family": row_family, "evidence": []})
    rows[row_id]["evidence"].append(
        CodeTriageEvidence(
            source=source,
            status=status,
            verdict=_classify_status(status),
            detail=detail,
        )
    )


def _proof_debt_resolved_by_controls(evidence: list[CodeTriageEvidence]) -> bool:
    proof_sources = {item.source for item in evidence if item.verdict == "proof-debt"}
    control_sources = {item.source for item in evidence if item.verdict == "control"}
    if not proof_sources:
        return True
    qc_proof = {"quasi_cyclic_code_search", "quasi_cyclic_canonicalization"}
    qc_resolvers = {"quasi_cyclic_canonicalization", "qc_information_set_resolver"}
    if proof_sources.issubset(qc_proof) and control_sources.intersection(qc_resolvers):
        return True
    if "code_incidence_resolver" in control_sources:
        return True
    return False


def _collect_pair_audits(rows: dict[str, dict[str, Any]], path: Path = CODE_EQUIVALENCE_AUDIT_PATH) -> None:
    payload = _read_json(path, {})
    for audit in payload.get("pair_audits", []):
        pair = dict(audit.get("pair", {}))
        row_id = str(pair.get("id", "unknown-code-row"))
        if audit.get("falsifiers_triggered"):
            status = "rejected-by-code-workbench-falsifier"
        elif pair.get("known_equivalent"):
            status = "equivalent-control"
        else:
            status = "code-workbench-survivor-needs-baselines"
        _add_evidence(rows, row_id, "seed-code-pair", "code_equivalence_workbench", status, str(audit.get("positive_signal", "")))


def _collect_records(rows: dict[str, dict[str, Any]], path: Path, source: str, list_key: str = "records") -> None:
    payload = _read_json(path, {})
    for record in payload.get(list_key, []):
        row_id, row_family = _row_id_for_record(record, source, list_key)
        _add_evidence(
            rows,
            row_id,
            row_family,
            source,
            str(record.get("status", "unknown")),
            str(record.get("interpretation", "")),
        )


def _collect_hull_projector_report(
    rows: dict[str, dict[str, Any]],
    path: Path = HULL_PROJECTOR_REDUCTION_PATH,
) -> None:
    payload = _read_json(path, {})
    if not payload:
        return
    metrics = payload.get("headline_metrics", {})
    _add_evidence(
        rows,
        "random-code-hull-projector-family",
        "random-code-hull-projector-family",
        "code_hull_projector_reduction",
        str(payload.get("status", "unknown")),
        (
            f"Trivial-hull fraction={metrics.get('trivial_hull_fraction', 'unknown')}; "
            f"hull<=2 fraction={metrics.get('hull_at_most_two_fraction', 'unknown')}; "
            f"finite projector/GI resolutions={metrics.get('projector_finite_resolved_count', 'unknown')}. "
            "This rejects independent code-native hardness, not graph-isomorphism hardness."
        ),
    )


def build_code_frontier_triage() -> CodeFrontierTriageReport:
    rows: dict[str, dict[str, Any]] = {}
    _collect_pair_audits(rows)
    _collect_records(rows, CODE_FAMILY_SEARCH_PATH, "code_family_search")
    _collect_records(rows, CODE_STRUCTURAL_INVARIANTS_PATH, "code_structural_invariants")
    _collect_records(rows, CODE_INFORMATION_SET_BASELINE_PATH, "code_information_set_baseline")
    _collect_records(rows, CODE_CANONICALIZATION_BASELINE_PATH, "code_canonicalization_baseline")
    _collect_records(rows, CODE_PROFILE_COLLISION_SEARCH_PATH, "code_profile_collision_search")
    _collect_records(rows, CODE_TUPLE_PROFILE_BASELINE_PATH, "code_tuple_profile_baseline")
    _collect_records(rows, CODE_TUPLE_PROFILE_BASELINE_PATH, "code_tuple_profile_collision_search", list_key="collision_records")
    _collect_records(rows, CODE_LOW_WEIGHT_STRUCTURE_PATH, "code_low_weight_structure")
    _collect_records(rows, QUASI_CYCLIC_CODE_SEARCH_PATH, "quasi_cyclic_code_search")
    _collect_records(rows, QUASI_CYCLIC_CANONICALIZATION_PATH, "quasi_cyclic_canonicalization")
    _collect_records(rows, QC_INFORMATION_SET_RESOLVER_PATH, "qc_information_set_resolver")
    _collect_records(rows, CYCLIC_CODE_SEARCH_PATH, "cyclic_code_search")
    _collect_records(rows, BCH_CODE_SEARCH_PATH, "bch_code_search")
    _collect_records(rows, GOPPA_CODE_SEARCH_PATH, "goppa_code_search")
    _collect_records(rows, GOPPA_SCALING_FRONTIER_PATH, "goppa_scaling_frontier")
    _collect_records(rows, GOPPA_SYZYGY_FRONTIER_PATH, "goppa_syzygy_frontier")
    _collect_records(rows, GOPPA_HULL_PROJECTOR_PATH, "goppa_hull_projector_frontier")
    _collect_records(rows, TANNER_CODE_SEARCH_PATH, "tanner_code_search")
    _collect_records(rows, REED_MULLER_CODE_SEARCH_PATH, "reed_muller_code_search")
    _collect_records(rows, RANK_METRIC_CODE_SEARCH_PATH, "rank_metric_code_search")
    _collect_records(rows, CODE_INCIDENCE_RESOLVER_PATH, "code_incidence_resolver", list_key="family_records")
    _collect_records(rows, AFFINE_GEOMETRY_CODE_SEARCH_PATH, "affine_geometry_code_search")
    _collect_records(rows, PROJECTIVE_GEOMETRY_CODE_SEARCH_PATH, "projective_geometry_code_search")
    _collect_records(rows, CODE_SCHUR_FILTRATION_PATH, "code_schur_filtration", list_key="family_records")
    _collect_records(rows, CODE_CLOSURE_ATTACK_PATH, "code_closure_attack", list_key="family_records")
    _collect_records(rows, CFI_CODE_REDUCTION_PATH, "cfi_code_reduction")
    _collect_hull_projector_report(rows)

    records: list[CodeFrontierRecord] = []
    for row_id, payload in sorted(rows.items()):
        evidence: list[CodeTriageEvidence] = payload["evidence"]
        verdicts = {item.verdict for item in evidence}
        if "dequantizing" in verdicts:
            final_status = "rejected-by-classical-code-baseline"
            next_step = "Do not use this code row for coset-state measurement design; mutate to a family that survives all listed baselines."
        elif "proof-debt" in verdicts and not _proof_debt_resolved_by_controls(evidence):
            final_status = "proof-debt-not-positive-evidence"
            next_step = "Resolve cap/survival evidence with stronger canonicalization, automorphism, or lower-bound arguments before promotion."
        elif "control" in verdicts:
            final_status = "control-or-no-hard-row-not-positive-evidence"
            next_step = "Treat equivalent controls and no-collision searches as negative search information; broaden the family generator."
        elif "proof-debt" in verdicts:
            final_status = "proof-debt-not-positive-evidence"
            next_step = "Resolve cap/survival evidence with stronger canonicalization, automorphism, or lower-bound arguments before promotion."
        elif "no-evidence" in verdicts:
            final_status = "control-or-no-hard-row-not-positive-evidence"
            next_step = "Treat equivalent controls and no-collision searches as negative search information; broaden the family generator."
        else:
            final_status = "unclassified-code-frontier-debt"
            next_step = "Inspect this row manually and add a sharper code triage rule."
        records.append(
            CodeFrontierRecord(
                row_id=row_id,
                row_family=str(payload["row_family"]),
                evidence=sorted(evidence, key=lambda item: (item.source, item.status)),
                final_status=final_status,
                required_next_step=next_step,
            )
        )

    metrics = {
        "record_count": len(records),
        "rejected_row_count": sum(1 for record in records if record.final_status == "rejected-by-classical-code-baseline"),
        "proof_debt_row_count": sum(1 for record in records if record.final_status == "proof-debt-not-positive-evidence"),
        "control_or_no_hard_row_count": sum(
            1 for record in records if record.final_status == "control-or-no-hard-row-not-positive-evidence"
        ),
        "unclassified_row_count": sum(1 for record in records if record.final_status == "unclassified-code-frontier-debt"),
        "evidence_count": sum(len(record.evidence) for record in records),
        "dequantizing_evidence_count": sum(
            1 for record in records for item in record.evidence if item.verdict == "dequantizing"
        ),
        "proof_debt_evidence_count": sum(1 for record in records for item in record.evidence if item.verdict == "proof-debt"),
    }
    if metrics["proof_debt_row_count"] or metrics["unclassified_row_count"]:
        status = "code-frontier-proof-debt"
    elif metrics["rejected_row_count"] or metrics["control_or_no_hard_row_count"]:
        status = "code-frontier-dequantized-or-control"
    else:
        status = "code-frontier-empty"
    summary = (
        f"Triage aggregated {metrics['record_count']} code-equivalence row(s) across {metrics['evidence_count']} evidence items. "
        f"{metrics['rejected_row_count']} row(s) are rejected by classical baselines, "
        f"{metrics['proof_debt_row_count']} remain proof debt, and "
        f"{metrics['control_or_no_hard_row_count']} are equivalent controls or no-hard-row searches."
    )
    falsifiers = []
    if metrics["rejected_row_count"]:
        falsifiers.append("Some code-equivalence rows are already separated by classical code baselines.")
    if metrics["control_or_no_hard_row_count"]:
        falsifiers.append("Some code searches find only equivalent controls or no nontrivial hard row.")
    if metrics["proof_debt_row_count"]:
        falsifiers.append("Some code-equivalence rows remain proof debt, not positive evidence.")
    return CodeFrontierTriageReport(utc_now(), records, metrics, status, summary, falsifiers)


def _json_ready(value: Any) -> Any:
    if is_dataclass(value):
        return _json_ready(asdict(value))
    if isinstance(value, dict):
        return {str(key): _json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_ready(item) for item in value]
    if isinstance(value, tuple):
        return [_json_ready(item) for item in value]
    return value


def write_code_frontier_negative_results(report: CodeFrontierTriageReport) -> int:
    written = 0
    for record in report.records:
        if record.final_status not in {
            "rejected-by-classical-code-baseline",
            "control-or-no-hard-row-not-positive-evidence",
        }:
            continue
        blockers = [
            f"{item.source}: {item.status}"
            for item in record.evidence
            if item.verdict in {"dequantizing", "control", "no-evidence"}
        ]
        upsert_negative_result(
            NegativeResultRecord(
                id=f"CODE-FRONTIER-TRIAGE-{_safe_id(record.row_id)}",
                source="code_frontier_triage.py",
                claim=f"{record.row_id} is a viable code-equivalence coset-state frontier row.",
                reason_invalid="; ".join(blockers[:5]) or record.final_status,
                lesson=(
                    "A code-equivalence row must survive structural invariants, tuple profiles, information-set "
                    "canonicalization, automorphism-aware canonicalization, and no-control checks before measurement design."
                ),
                applies_to=["CODE-COSET-COLLECTIVE", "PO-DEQUANTIZATION", "PO-FALSIFIERS"],
                evidence={
                    "row_id": record.row_id,
                    "row_family": record.row_family,
                    "final_status": record.final_status,
                    "evidence_sources": [item.source for item in record.evidence],
                },
            )
        )
        written += 1
    return written


def write_code_frontier_triage(
    output_path: Path = CODE_FRONTIER_TRIAGE_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = "EXP-CODE-FRONTIER-TRIAGE",
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "RESULT-CODE-FRONTIER-TRIAGE-LATEST",
) -> dict[str, Any]:
    report = build_code_frontier_triage()
    payload = _json_ready(report)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    if write_registry:
        negative_results_written = write_code_frontier_negative_results(report)
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
                artifacts={"code_frontier_triage": str(output_path)},
            )
        )
    return payload
