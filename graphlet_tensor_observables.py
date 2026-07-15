"""Graphlet and homomorphism tensor-observable baselines.

Many proposed low-bond collective measurements over graph/coset states amount
to counting small patterns or contracting bounded-rank tensors over the
adjacency relation.  This module makes that classical shadow explicit.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, is_dataclass
from itertools import combinations
from pathlib import Path
from typing import Any

import numpy as np

from collective_observable_search import DEFAULT_PAIR_IDS, graph_pair_matrices
from coset_state_workbench import GraphPairSpec
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


COSET_WORKBENCH_DIR = Path("research/coset_workbench")
GRAPHLET_TENSOR_OBSERVABLES_PATH = COSET_WORKBENCH_DIR / "graphlet_tensor_observables.json"
DEFAULT_TENSOR_PAIR_IDS = [*DEFAULT_PAIR_IDS, "cfi-k6-parity-twist"]


@dataclass(frozen=True)
class GraphletTensorRecord:
    id: str
    pair_id: str
    observable_name: str
    register_count: int
    bond_dimension: int
    evaluated: bool
    tuple_count: int
    distinguishes: bool
    classical_shadow: str
    value_a: str
    value_b: str
    status: str
    interpretation: str


@dataclass(frozen=True)
class PairGraphletTensorAudit:
    pair: GraphPairSpec
    records: list[GraphletTensorRecord]
    status: str
    falsifiers_triggered: list[str]


@dataclass(frozen=True)
class GraphletTensorObservableResult:
    created_at: str
    tuple_cap: int
    pair_audits: list[PairGraphletTensorAudit]
    headline_metrics: dict[str, int]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _short(value: Any, limit: int = 360) -> str:
    text = str(value)
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."


def edge_count(adjacency: np.ndarray) -> int:
    return int(adjacency.sum() // 2)


def wedge_count(adjacency: np.ndarray) -> int:
    degrees = adjacency.sum(axis=1)
    return int(sum(int(degree) * (int(degree) - 1) // 2 for degree in degrees))


def triangle_count(adjacency: np.ndarray) -> int:
    return int(np.trace(adjacency @ adjacency @ adjacency) // 6)


def four_cycle_count(adjacency: np.ndarray) -> int:
    total = 0
    n = int(adjacency.shape[0])
    for left in range(n):
        for right in range(left + 1, n):
            common = int(np.logical_and(adjacency[left], adjacency[right]).sum())
            total += common * (common - 1) // 2
    return int(total // 2)


def induced_four_vertex_edge_histogram(adjacency: np.ndarray, tuple_cap: int) -> tuple[tuple[int, int], ...] | str:
    n = int(adjacency.shape[0])
    tuple_count = n * (n - 1) * (n - 2) * (n - 3) // 24
    if tuple_count > tuple_cap:
        return "skipped"
    counts = {edge_total: 0 for edge_total in range(7)}
    for vertices in combinations(range(n), 4):
        edge_total = 0
        for left, right in combinations(vertices, 2):
            edge_total += int(adjacency[left, right])
        counts[edge_total] += 1
    return tuple(sorted(counts.items()))


def homomorphism_moment_signature(adjacency: np.ndarray) -> tuple[tuple[str, int], ...]:
    return (
        ("edges", edge_count(adjacency)),
        ("wedges", wedge_count(adjacency)),
        ("triangles", triangle_count(adjacency)),
        ("four_cycles", four_cycle_count(adjacency)),
    )


def graphlet_tensor_signature(adjacency: np.ndarray, tuple_cap: int) -> tuple[tuple[int, int], ...] | str:
    return induced_four_vertex_edge_histogram(adjacency, tuple_cap=tuple_cap)


def _record(
    pair_id: str,
    observable_id: str,
    observable_name: str,
    register_count: int,
    bond_dimension: int,
    tuple_count: int,
    evaluated: bool,
    classical_shadow: str,
    value_a: Any,
    value_b: Any,
) -> GraphletTensorRecord:
    if not evaluated:
        status = "skipped-scaling-cap"
        distinguishes = False
        interpretation = (
            f"{observable_name} exceeded the tuple cap; a real tensor ansatz needs an implicit contraction certificate."
        )
    else:
        distinguishes = value_a != value_b
        if distinguishes:
            status = "classical-shadow-collapse"
            interpretation = (
                f"{observable_name} distinguishes the pair, but it is a classical {classical_shadow} computation."
            )
        else:
            status = "no-signal"
            interpretation = f"{observable_name} gives matching signatures; no tensor-observable evidence."
    return GraphletTensorRecord(
        id=f"GRAPHLET-TENSOR-{pair_id}-{observable_id}",
        pair_id=pair_id,
        observable_name=observable_name,
        register_count=register_count,
        bond_dimension=bond_dimension,
        evaluated=evaluated,
        tuple_count=tuple_count,
        distinguishes=distinguishes,
        classical_shadow=classical_shadow,
        value_a=_short(value_a),
        value_b=_short(value_b),
        status=status,
        interpretation=interpretation,
    )


def audit_graphlet_tensor_pair(pair_id: str, tuple_cap: int = 1_000_000) -> PairGraphletTensorAudit:
    spec, graph_a, graph_b = graph_pair_matrices(pair_id)
    n = int(graph_a.shape[0])
    four_tuple_count = n * (n - 1) * (n - 2) * (n - 3) // 24
    four_eval = four_tuple_count <= tuple_cap
    records = [
        _record(
            pair_id,
            "homomorphism-moments",
            "Rank-2/3 homomorphism moment tensor",
            3,
            4,
            n**3,
            True,
            "edge/wedge/triangle/four-cycle count invariant",
            homomorphism_moment_signature(graph_a),
            homomorphism_moment_signature(graph_b),
        ),
        _record(
            pair_id,
            "four-vertex-graphlet-histogram",
            "Four-register graphlet histogram tensor",
            4,
            7,
            four_tuple_count,
            four_eval,
            "induced four-vertex graphlet count invariant",
            graphlet_tensor_signature(graph_a, tuple_cap) if four_eval else "skipped",
            graphlet_tensor_signature(graph_b, tuple_cap) if four_eval else "skipped",
        ),
    ]
    shadow_count = sum(1 for record in records if record.status == "classical-shadow-collapse")
    skipped_count = sum(1 for record in records if record.status == "skipped-scaling-cap")
    no_signal_count = sum(1 for record in records if record.status == "no-signal")
    falsifiers = []
    if shadow_count:
        falsifiers.append("A graphlet/tensor observable is exactly a classical small-pattern count.")
    if spec.known_nonisomorphic and no_signal_count == len(records) - skipped_count:
        falsifiers.append("Known non-isomorphic graph pair has no separating graphlet tensor signal at this bond/register budget.")
    if skipped_count:
        falsifiers.append("Graphlet tensor enumeration hit the tuple cap; implicit contraction proof is required.")
    if shadow_count:
        status = "classical-shadow-collapse"
    elif spec.known_nonisomorphic:
        status = "boundary-no-graphlet-signal"
    else:
        status = "no-signal"
    return PairGraphletTensorAudit(spec, records, status, sorted(set(falsifiers)))


def run_graphlet_tensor_observables(
    pair_ids: list[str] | None = None,
    tuple_cap: int = 1_000_000,
) -> GraphletTensorObservableResult:
    active_pairs = pair_ids or DEFAULT_TENSOR_PAIR_IDS
    audits = [audit_graphlet_tensor_pair(pair_id, tuple_cap=tuple_cap) for pair_id in active_pairs]
    records = [record for audit in audits for record in audit.records]
    metrics = {
        "pair_count": len(audits),
        "observable_count": len(records),
        "classical_shadow_collapse_count": sum(1 for record in records if record.status == "classical-shadow-collapse"),
        "no_signal_count": sum(1 for record in records if record.status == "no-signal"),
        "skipped_scaling_count": sum(1 for record in records if record.status == "skipped-scaling-cap"),
        "boundary_pair_count": sum(1 for audit in audits if audit.status == "boundary-no-graphlet-signal"),
        "nonclassical_candidate_count": 0,
        "max_vertex_count": max((audit.pair.vertex_count for audit in audits), default=0),
        "max_bond_dimension": max((record.bond_dimension for record in records if record.evaluated), default=0),
    }
    if metrics["boundary_pair_count"]:
        status = "blocked-no-graphlet-tensor-separator"
    elif metrics["classical_shadow_collapse_count"]:
        status = "dequantized-by-graphlet-tensor-shadow"
    else:
        status = "no-separating-signal"
    summary = (
        f"Audited {metrics['observable_count']} graphlet tensor observables across {metrics['pair_count']} graph pairs. "
        f"{metrics['classical_shadow_collapse_count']} signal(s) collapse to small-pattern classical counts; "
        f"{metrics['boundary_pair_count']} boundary pair(s) remain without graphlet-tensor signal."
    )
    falsifiers = sorted({item for audit in audits for item in audit.falsifiers_triggered})
    return GraphletTensorObservableResult(utc_now(), tuple_cap, audits, metrics, status, summary, falsifiers)


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


def write_graphlet_tensor_negative_results(result: GraphletTensorObservableResult) -> int:
    written = 0
    for audit in result.pair_audits:
        for record in audit.records:
            if record.status != "classical-shadow-collapse":
                continue
            upsert_negative_result(
                NegativeResultRecord(
                    id=f"GRAPHLET-TENSOR-SHADOW-{_safe_id(record.pair_id)}-{_safe_id(record.observable_name)}",
                    source="graphlet_tensor_observables.py",
                    claim=f"{record.observable_name} is nonclassical evidence for {record.pair_id}.",
                    reason_invalid=f"The tensor observable is exactly a classical shadow: {record.classical_shadow}.",
                    lesson="Bounded graphlet/homomorphism tensor contractions are classical invariants, not quantum speedup evidence.",
                    applies_to=["CODE-COSET-COLLECTIVE", "EXP-CODE-TENSOR-MEASUREMENT", "PO-DEQUANTIZATION"],
                    evidence={
                        "pair_id": record.pair_id,
                        "observable_id": record.id,
                        "register_count": record.register_count,
                        "bond_dimension": record.bond_dimension,
                        "classical_shadow": record.classical_shadow,
                    },
                )
            )
            written += 1
    return written


def write_graphlet_tensor_observables(
    output_path: Path = GRAPHLET_TENSOR_OBSERVABLES_PATH,
    pair_ids: list[str] | None = None,
    tuple_cap: int = 1_000_000,
    write_registry: bool = True,
    registry_experiment_id: str = "EXP-CODE-TENSOR-MEASUREMENT",
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "RESULT-CODE-TENSOR-MEASUREMENT-LATEST",
) -> dict[str, Any]:
    result = run_graphlet_tensor_observables(pair_ids=pair_ids, tuple_cap=tuple_cap)
    payload = _json_ready(result)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    if write_registry:
        negative_results_written = write_graphlet_tensor_negative_results(result)
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
                artifacts={"graphlet_tensor_observables": str(output_path)},
            )
        )
    return payload
