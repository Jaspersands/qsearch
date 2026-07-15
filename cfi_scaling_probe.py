"""Scaling probe for CFI-style nonabelian HSP boundary instances."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, is_dataclass
from pathlib import Path
from typing import Any

import numpy as np

from coset_state_workbench import (
    cfi_parity_graph_complete,
    degree_signature,
    spectrum_signature,
    walk_count_signature,
    wl1_signature,
    wl2_signature,
    wl_k_signature,
)
from graphlet_tensor_observables import graphlet_tensor_signature, homomorphism_moment_signature
from research_registry import ExperimentResultRecord, NegativeResultRecord, upsert_experiment_result, upsert_negative_result, utc_now


COSET_WORKBENCH_DIR = Path("research/coset_workbench")
CFI_SCALING_PROBE_PATH = COSET_WORKBENCH_DIR / "cfi_scaling_probe.json"


@dataclass(frozen=True)
class CFIProbeRecord:
    base_size: int
    vertex_count: int
    edge_count: int
    cheap_invariants_distinguish: bool
    wl2_evaluated: bool
    wl2_pair_count: int
    wl2_distinguishes: bool
    wl3_evaluated: bool
    wl3_tuple_count: int
    wl3_distinguishes: bool | None
    graphlet4_evaluated: bool
    graphlet4_tuple_count: int
    graphlet4_distinguishes: bool | None
    status: str
    interpretation: str


@dataclass(frozen=True)
class CFIScalingProbeResult:
    created_at: str
    base_sizes: list[int]
    wl_tuple_cap: int
    graphlet_tuple_cap: int
    records: list[CFIProbeRecord]
    headline_metrics: dict[str, int]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _edge_count(adjacency: np.ndarray) -> int:
    return int(adjacency.sum() // 2)


def _choose_status(
    cheap_distinguishes: bool,
    wl2_distinguishes: bool,
    wl3_evaluated: bool,
    wl3_distinguishes: bool | None,
    graphlet4_evaluated: bool,
    graphlet4_distinguishes: bool | None,
) -> tuple[str, str]:
    if cheap_distinguishes or wl2_distinguishes:
        return (
            "dequantized-by-low-cost-invariant",
            "A low-cost classical invariant distinguishes this CFI instance; it is not useful as a boundary benchmark.",
        )
    if wl3_evaluated and wl3_distinguishes:
        return (
            "dequantized-by-3wl",
            "3-WL distinguishes this instance; a matching low-register observable is classically shadowed.",
        )
    if graphlet4_evaluated and graphlet4_distinguishes:
        return (
            "dequantized-by-graphlet-count",
            "Four-vertex graphlet counts distinguish this instance; graphlet tensor evidence is classical.",
        )
    if (not wl3_evaluated) or (not graphlet4_evaluated):
        return (
            "scaling-boundary-needs-implicit-observable",
            "Low-cost invariants fail, while brute-force WL/graphlet probes hit scaling caps; this is measurement-design proof debt.",
        )
    return (
        "finite-boundary-survives-current-probes",
        "Low-cost, 3-WL, and graphlet probes do not distinguish this CFI instance at the current scale.",
    )


def audit_cfi_base_size(
    base_size: int,
    wl2_pair_cap: int = 10_000,
    wl_tuple_cap: int = 100_000,
    graphlet_tuple_cap: int = 1_000_000,
) -> CFIProbeRecord:
    graph_a = cfi_parity_graph_complete(base_size, twisted_edge=None)
    graph_b = cfi_parity_graph_complete(base_size, twisted_edge=(0, 1))
    n = int(graph_a.shape[0])
    wl2_pair_count = n**2
    wl2_evaluated = wl2_pair_count <= wl2_pair_cap
    wl2_a = wl2_signature(graph_a) if wl2_evaluated else "skipped"
    wl2_b = wl2_signature(graph_b) if wl2_evaluated else "skipped"
    cheap_a = (
        degree_signature(graph_a),
        spectrum_signature(graph_a),
        walk_count_signature(graph_a, max_length=8),
        wl1_signature(graph_a),
        wl2_a,
        homomorphism_moment_signature(graph_a),
    )
    cheap_b = (
        degree_signature(graph_b),
        spectrum_signature(graph_b),
        walk_count_signature(graph_b, max_length=8),
        wl1_signature(graph_b),
        wl2_b,
        homomorphism_moment_signature(graph_b),
    )
    cheap_distinguishes = cheap_a != cheap_b
    wl2_distinguishes = bool(wl2_evaluated and wl2_a != wl2_b)
    wl3_tuple_count = n**3
    wl3_evaluated = wl3_tuple_count <= wl_tuple_cap
    wl3_distinguishes = (
        wl_k_signature(graph_a, k=3) != wl_k_signature(graph_b, k=3)
        if wl3_evaluated
        else None
    )
    graphlet4_tuple_count = n * (n - 1) * (n - 2) * (n - 3) // 24
    graphlet4_evaluated = graphlet4_tuple_count <= graphlet_tuple_cap
    graphlet4_distinguishes = (
        graphlet_tensor_signature(graph_a, graphlet_tuple_cap) != graphlet_tensor_signature(graph_b, graphlet_tuple_cap)
        if graphlet4_evaluated
        else None
    )
    status, interpretation = _choose_status(
        cheap_distinguishes,
        wl2_distinguishes,
        wl3_evaluated,
        wl3_distinguishes,
        graphlet4_evaluated,
        graphlet4_distinguishes,
    )
    return CFIProbeRecord(
        base_size=base_size,
        vertex_count=n,
        edge_count=_edge_count(graph_a),
        cheap_invariants_distinguish=cheap_distinguishes,
        wl2_evaluated=wl2_evaluated,
        wl2_pair_count=wl2_pair_count,
        wl2_distinguishes=wl2_distinguishes,
        wl3_evaluated=wl3_evaluated,
        wl3_tuple_count=wl3_tuple_count,
        wl3_distinguishes=wl3_distinguishes,
        graphlet4_evaluated=graphlet4_evaluated,
        graphlet4_tuple_count=graphlet4_tuple_count,
        graphlet4_distinguishes=graphlet4_distinguishes,
        status=status,
        interpretation=interpretation,
    )


def run_cfi_scaling_probe(
    base_sizes: list[int] | None = None,
    wl2_pair_cap: int = 10_000,
    wl_tuple_cap: int = 100_000,
    graphlet_tuple_cap: int = 1_000_000,
) -> CFIScalingProbeResult:
    sizes = base_sizes or [4, 5, 6, 7]
    records = [
        audit_cfi_base_size(
            size,
            wl2_pair_cap=wl2_pair_cap,
            wl_tuple_cap=wl_tuple_cap,
            graphlet_tuple_cap=graphlet_tuple_cap,
        )
        for size in sizes
    ]
    metrics = {
        "base_size_count": len(records),
        "boundary_record_count": sum(1 for record in records if "boundary" in record.status),
        "cheap_invariant_distinguishes_count": sum(1 for record in records if record.cheap_invariants_distinguish),
        "wl2_distinguishes_count": sum(1 for record in records if record.wl2_distinguishes),
        "wl2_evaluated_count": sum(1 for record in records if record.wl2_evaluated),
        "wl2_skipped_count": sum(1 for record in records if not record.wl2_evaluated),
        "wl3_evaluated_count": sum(1 for record in records if record.wl3_evaluated),
        "wl3_skipped_count": sum(1 for record in records if not record.wl3_evaluated),
        "graphlet4_evaluated_count": sum(1 for record in records if record.graphlet4_evaluated),
        "graphlet4_skipped_count": sum(1 for record in records if not record.graphlet4_evaluated),
        "max_vertex_count": max((record.vertex_count for record in records), default=0),
    }
    status = "cfi-scaling-boundary-open" if metrics["boundary_record_count"] else "dequantized-cfi-family"
    summary = (
        f"Audited CFI parity bases {sizes}. {metrics['boundary_record_count']} row(s) remain boundary/proof-debt cases; "
        f"{metrics['wl3_skipped_count']} skip 3-WL brute force and {metrics['graphlet4_skipped_count']} skip four-graphlet enumeration."
    )
    falsifiers = []
    if metrics["cheap_invariant_distinguishes_count"] or metrics["wl2_distinguishes_count"]:
        falsifiers.append("Some CFI rows are distinguishable by low-cost invariants and cannot support a coset speedup claim.")
    if metrics["boundary_record_count"]:
        falsifiers.append("Boundary CFI rows still lack an explicit nonclassical collective measurement; current evidence is proof debt.")
    return CFIScalingProbeResult(utc_now(), sizes, wl_tuple_cap, graphlet_tuple_cap, records, metrics, status, summary, falsifiers)


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
    if isinstance(value, np.floating):
        return float(value)
    if isinstance(value, np.bool_):
        return bool(value)
    return value


def write_cfi_negative_results(result: CFIScalingProbeResult) -> int:
    written = 0
    for record in result.records:
        if record.status not in {"dequantized-by-low-cost-invariant", "dequantized-by-3wl", "dequantized-by-graphlet-count"}:
            continue
        upsert_negative_result(
            NegativeResultRecord(
                id=f"CFI-SCALING-DEQUANTIZED-K{record.base_size}",
                source="cfi_scaling_probe.py",
                claim=f"CFI K{record.base_size} parity twist supplies nonclassical coset-state evidence.",
                reason_invalid=record.interpretation,
                lesson="CFI rows are useful only when they survive low-cost classical invariants and force explicit collective-measurement proof obligations.",
                applies_to=["CODE-COSET-COLLECTIVE", "PO-DEQUANTIZATION", "PO-MEASUREMENT"],
                evidence=asdict(record),
            )
        )
        written += 1
    return written


def write_cfi_scaling_probe(
    output_path: Path = CFI_SCALING_PROBE_PATH,
    base_sizes: list[int] | None = None,
    wl2_pair_cap: int = 10_000,
    wl_tuple_cap: int = 100_000,
    graphlet_tuple_cap: int = 1_000_000,
    write_registry: bool = True,
    registry_experiment_id: str = "EXP-COSET-CFI-SCALING",
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "RESULT-COSET-CFI-SCALING-LATEST",
) -> dict[str, Any]:
    result = run_cfi_scaling_probe(
        base_sizes=base_sizes,
        wl2_pair_cap=wl2_pair_cap,
        wl_tuple_cap=wl_tuple_cap,
        graphlet_tuple_cap=graphlet_tuple_cap,
    )
    payload = _json_ready(result)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    if write_registry:
        negative_results_written = write_cfi_negative_results(result)
        metrics = dict(result.headline_metrics)
        metrics["negative_results_written"] = negative_results_written
        upsert_experiment_result(
            ExperimentResultRecord(
                id=registry_result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=result.created_at,
                status=result.status,
                summary=result.summary,
                metrics=metrics,
                falsifiers_triggered=result.falsifiers_triggered,
                artifacts={"cfi_scaling_probe": str(output_path)},
            )
        )
    return payload
