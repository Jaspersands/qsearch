"""Individualization-refinement WL baselines for graph/coset rows.

Plain k-WL and low-register observables can miss graph pairs that classical GI
heuristics attack by individualizing a few vertices and then running color
refinement.  This module audits that baseline explicitly so low-register coset
signals are not mistaken for quantum evidence when individualization-refinement
already separates the instances.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, is_dataclass
from itertools import combinations
from math import comb
from pathlib import Path
from typing import Any

import numpy as np

from collective_observable_search import DEFAULT_PAIR_IDS, graph_pair_matrices
from coset_state_workbench import GraphPairSpec
from research_registry import ExperimentResultRecord, NegativeResultRecord, upsert_experiment_result, upsert_negative_result, utc_now


COSET_WORKBENCH_DIR = Path("research/coset_workbench")
INDIVIDUALIZED_WL_BASELINE_PATH = COSET_WORKBENCH_DIR / "individualized_wl_baseline.json"


@dataclass(frozen=True)
class IndividualizedWLRecord:
    pair_id: str
    individualization_size: int
    tuple_count: int
    evaluated: bool
    distinguishes: bool
    signature_a: str
    signature_b: str
    status: str
    interpretation: str


@dataclass(frozen=True)
class PairIndividualizedWLAudit:
    pair: GraphPairSpec
    records: list[IndividualizedWLRecord]
    status: str
    falsifiers_triggered: list[str]


@dataclass(frozen=True)
class IndividualizedWLReport:
    created_at: str
    max_individualization: int
    tuple_cap: int
    pair_audits: list[PairIndividualizedWLAudit]
    headline_metrics: dict[str, int]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def individualized_wl_signature(adjacency: np.ndarray, individualized: tuple[int, ...], rounds: int = 8) -> tuple[tuple[int, int], ...]:
    n = int(adjacency.shape[0])
    markers = {vertex: index + 1 for index, vertex in enumerate(individualized)}
    labels = [(int(adjacency[vertex].sum()), markers.get(vertex, 0)) for vertex in range(n)]
    palette = {label: idx for idx, label in enumerate(sorted(set(labels)))}
    colors = [palette[label] for label in labels]
    neighbors = [list(np.flatnonzero(adjacency[vertex])) for vertex in range(n)]
    for _ in range(rounds):
        refined = [
            (colors[vertex], tuple(sorted(colors[neighbor] for neighbor in neighbors[vertex])))
            for vertex in range(n)
        ]
        palette = {label: idx for idx, label in enumerate(sorted(set(refined)))}
        new_colors = [palette[label] for label in refined]
        if new_colors == colors:
            break
        colors = new_colors
    counts: dict[int, int] = {}
    for color in colors:
        counts[color] = counts.get(color, 0) + 1
    return tuple(sorted(counts.items()))


def individualized_wl_multiset(
    adjacency: np.ndarray,
    individualization_size: int,
    tuple_cap: int,
) -> tuple[bool, int, tuple[tuple[str, int], ...] | str]:
    n = int(adjacency.shape[0])
    tuple_count = comb(n, individualization_size)
    if tuple_count > tuple_cap:
        return False, tuple_count, "skipped"
    counts: dict[str, int] = {}
    for subset in combinations(range(n), individualization_size):
        signature = str(individualized_wl_signature(adjacency, subset))
        counts[signature] = counts.get(signature, 0) + 1
    return True, tuple_count, tuple(sorted(counts.items()))


def audit_individualized_wl_pair(
    pair_id: str,
    max_individualization: int = 3,
    tuple_cap: int = 40_000,
) -> PairIndividualizedWLAudit:
    spec, graph_a, graph_b = graph_pair_matrices(pair_id)
    records: list[IndividualizedWLRecord] = []
    for size in range(1, max_individualization + 1):
        eval_a, tuple_count_a, signature_a = individualized_wl_multiset(graph_a, size, tuple_cap)
        eval_b, tuple_count_b, signature_b = individualized_wl_multiset(graph_b, size, tuple_cap)
        evaluated = bool(eval_a and eval_b)
        tuple_count = max(tuple_count_a, tuple_count_b)
        distinguishes = bool(evaluated and signature_a != signature_b)
        if not evaluated:
            status = "skipped-scaling-cap"
            interpretation = (
                f"{size}-vertex individualization skipped because {tuple_count} combinations exceed cap {tuple_cap}; "
                "implicit or sampled individualization baselines are needed."
            )
        elif distinguishes:
            status = "dequantized-by-individualized-wl"
            interpretation = (
                f"{size}-vertex individualization plus color refinement separates the pair; any matching coset observable "
                "is classically shadowed by individualization-refinement."
            )
        else:
            status = "no-individualized-wl-signal"
            interpretation = f"{size}-vertex individualization plus color refinement does not separate the pair."
        records.append(
            IndividualizedWLRecord(
                pair_id=pair_id,
                individualization_size=size,
                tuple_count=tuple_count,
                evaluated=evaluated,
                distinguishes=distinguishes,
                signature_a=str(signature_a)[:500],
                signature_b=str(signature_b)[:500],
                status=status,
                interpretation=interpretation,
            )
        )
    falsifiers = []
    if any(record.distinguishes for record in records):
        falsifiers.append("Individualization-refinement separates this graph pair classically.")
    if any(record.status == "skipped-scaling-cap" for record in records):
        falsifiers.append("Individualization-refinement hit scaling caps; unresolved rows are proof debt, not evidence.")
    if any(record.distinguishes for record in records):
        status = "dequantized-by-individualized-wl"
    elif any(record.status == "skipped-scaling-cap" for record in records):
        status = "individualized-wl-proof-debt"
    else:
        status = "survives-individualized-wl-baseline"
    return PairIndividualizedWLAudit(spec, records, status, falsifiers)


def run_individualized_wl_baseline(
    pair_ids: list[str] | None = None,
    max_individualization: int = 3,
    tuple_cap: int = 40_000,
) -> IndividualizedWLReport:
    active_pairs = pair_ids or DEFAULT_PAIR_IDS
    audits = [
        audit_individualized_wl_pair(pair_id, max_individualization=max_individualization, tuple_cap=tuple_cap)
        for pair_id in active_pairs
    ]
    records = [record for audit in audits for record in audit.records]
    metrics = {
        "pair_count": len(audits),
        "record_count": len(records),
        "dequantized_pair_count": sum(1 for audit in audits if audit.status == "dequantized-by-individualized-wl"),
        "survivor_pair_count": sum(1 for audit in audits if audit.status == "survives-individualized-wl-baseline"),
        "proof_debt_pair_count": sum(1 for audit in audits if audit.status == "individualized-wl-proof-debt"),
        "distinguishing_record_count": sum(1 for record in records if record.distinguishes),
        "skipped_record_count": sum(1 for record in records if record.status == "skipped-scaling-cap"),
        "max_tuple_count": max((record.tuple_count for record in records), default=0),
    }
    if metrics["dequantized_pair_count"]:
        status = "individualized-wl-dequantizes-graph-rows"
    elif metrics["proof_debt_pair_count"]:
        status = "individualized-wl-proof-debt"
    else:
        status = "survives-individualized-wl"
    summary = (
        f"Audited {metrics['pair_count']} graph/coset pair(s) with individualization up to {max_individualization}. "
        f"{metrics['dequantized_pair_count']} pair(s) were separated, {metrics['survivor_pair_count']} survived, "
        f"and {metrics['proof_debt_pair_count']} hit proof-debt caps."
    )
    falsifiers = sorted({item for audit in audits for item in audit.falsifiers_triggered})
    return IndividualizedWLReport(utc_now(), max_individualization, tuple_cap, audits, metrics, status, summary, falsifiers)


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


def write_individualized_wl_negative_results(report: IndividualizedWLReport) -> int:
    written = 0
    for audit in report.pair_audits:
        distinguishing = [record for record in audit.records if record.distinguishes]
        if not distinguishing:
            continue
        best = min(distinguishing, key=lambda record: record.individualization_size)
        upsert_negative_result(
            NegativeResultRecord(
                id=f"GRAPH-INDIVIDUALIZED-WL-DEQUANTIZED-{_safe_id(audit.pair.id)}",
                source="individualized_wl_baseline.py",
                claim=f"{audit.pair.id} supplies nonclassical coset-state evidence.",
                reason_invalid=best.interpretation,
                lesson=(
                    "Graph/coset rows must survive individualization-refinement baselines before any matching low-register or "
                    "collective observable can count as quantum evidence."
                ),
                applies_to=["CODE-COSET-COLLECTIVE", "PO-DEQUANTIZATION", "PO-FALSIFIERS"],
                evidence=asdict(best),
            )
        )
        written += 1
    return written


def write_individualized_wl_baseline(
    output_path: Path = INDIVIDUALIZED_WL_BASELINE_PATH,
    pair_ids: list[str] | None = None,
    max_individualization: int = 3,
    tuple_cap: int = 40_000,
    write_registry: bool = True,
    registry_experiment_id: str = "EXP-COSET-INDIVIDUALIZED-WL",
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "RESULT-COSET-INDIVIDUALIZED-WL-LATEST",
) -> dict[str, Any]:
    report = run_individualized_wl_baseline(pair_ids=pair_ids, max_individualization=max_individualization, tuple_cap=tuple_cap)
    payload = _json_ready(report)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    if write_registry:
        negative_results_written = write_individualized_wl_negative_results(report)
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
                artifacts={"individualized_wl_baseline": str(output_path)},
            )
        )
    return payload
