"""Individualized rooted tensor-observable baselines for graph/coset rows.

Low-register collective observables can look more interesting than they are
when they are just rooted graphlet counts after conditioning on a few vertices.
This module makes that shadow explicit: individualize small root sets, compute
rooted one/two-extension graphlet signatures, compare the multisets, and record
separations as classical dequantization evidence.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, is_dataclass
from itertools import combinations, permutations
from math import comb
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
INDIVIDUALIZED_TENSOR_OBSERVABLES_PATH = COSET_WORKBENCH_DIR / "individualized_tensor_observables.json"
DEFAULT_INDIVIDUALIZED_TENSOR_PAIR_IDS = [*DEFAULT_PAIR_IDS, "cfi-k6-parity-twist"]


@dataclass(frozen=True)
class IndividualizedTensorRecord:
    pair_id: str
    root_size: int
    root_subset_count: int
    extension_tuple_count: int
    evaluated: bool
    distinguishes: bool
    classical_shadow: str
    signature_a: str
    signature_b: str
    status: str
    interpretation: str


@dataclass(frozen=True)
class PairIndividualizedTensorAudit:
    pair: GraphPairSpec
    records: list[IndividualizedTensorRecord]
    status: str
    falsifiers_triggered: list[str]


@dataclass(frozen=True)
class IndividualizedTensorObservableReport:
    created_at: str
    max_root_size: int
    tuple_cap: int
    pair_audits: list[PairIndividualizedTensorAudit]
    headline_metrics: dict[str, int]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _short(value: Any, limit: int = 700) -> str:
    text = str(value)
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."


def _rooted_signature_for_order(
    adjacency: np.ndarray,
    ordered_roots: tuple[int, ...],
    outside: list[int],
    degrees: list[int],
) -> tuple[Any, ...]:
    root_size = len(ordered_roots)
    root_edges = tuple(
        int(adjacency[ordered_roots[left], ordered_roots[right]])
        for left in range(root_size)
        for right in range(left + 1, root_size)
    )
    root_degrees = tuple(degrees[root] for root in ordered_roots)

    masks: dict[int, int] = {}
    vertex_hist: dict[tuple[int, int, int], int] = {}
    for vertex in outside:
        mask = 0
        for position, root in enumerate(ordered_roots):
            if adjacency[vertex, root]:
                mask |= 1 << position
        masks[vertex] = mask
        degree_to_roots = int(mask.bit_count())
        signature = (mask, degrees[vertex], degrees[vertex] - degree_to_roots)
        vertex_hist[signature] = vertex_hist.get(signature, 0) + 1

    pair_hist: dict[tuple[int, int, int, int], int] = {}
    for left_index, left in enumerate(outside):
        left_mask = masks[left]
        for right in outside[left_index + 1 :]:
            right_mask = masks[right]
            ordered_masks = tuple(sorted((left_mask, right_mask)))
            signature = (
                ordered_masks[0],
                ordered_masks[1],
                int(adjacency[left, right]),
                int((left_mask & right_mask).bit_count()),
            )
            pair_hist[signature] = pair_hist.get(signature, 0) + 1

    return (
        root_edges,
        root_degrees,
        tuple(sorted(vertex_hist.items())),
        tuple(sorted(pair_hist.items())),
    )


def rooted_tensor_signature(adjacency: np.ndarray, roots: tuple[int, ...]) -> tuple[Any, ...]:
    """Return a labeling-invariant rooted two-extension graphlet signature."""

    root_set = set(roots)
    outside = [vertex for vertex in range(int(adjacency.shape[0])) if vertex not in root_set]
    degrees = [int(value) for value in adjacency.sum(axis=1)]
    candidates = [
        _rooted_signature_for_order(adjacency, tuple(roots[index] for index in order), outside, degrees)
        for order in permutations(range(len(roots)))
    ]
    return min(candidates)


def rooted_tensor_multiset(
    adjacency: np.ndarray,
    root_size: int,
    tuple_cap: int,
) -> tuple[bool, int, int, tuple[tuple[str, int], ...] | str]:
    n = int(adjacency.shape[0])
    if root_size <= 0 or root_size >= n:
        raise ValueError("root_size must be between 1 and n-1")
    root_subset_count = comb(n, root_size)
    extension_count_per_root = (n - root_size) + comb(n - root_size, 2)
    extension_tuple_count = root_subset_count * extension_count_per_root
    if extension_tuple_count > tuple_cap:
        return False, root_subset_count, extension_tuple_count, "skipped"

    counts: dict[str, int] = {}
    for roots in combinations(range(n), root_size):
        signature = _short(rooted_tensor_signature(adjacency, roots), limit=1400)
        counts[signature] = counts.get(signature, 0) + 1
    return True, root_subset_count, extension_tuple_count, tuple(sorted(counts.items()))


def audit_individualized_tensor_pair(
    pair_id: str,
    max_root_size: int = 2,
    tuple_cap: int = 3_000_000,
) -> PairIndividualizedTensorAudit:
    spec, graph_a, graph_b = graph_pair_matrices(pair_id)
    records: list[IndividualizedTensorRecord] = []
    for root_size in range(1, max_root_size + 1):
        eval_a, root_count_a, tuple_count_a, signature_a = rooted_tensor_multiset(graph_a, root_size, tuple_cap)
        eval_b, root_count_b, tuple_count_b, signature_b = rooted_tensor_multiset(graph_b, root_size, tuple_cap)
        evaluated = bool(eval_a and eval_b)
        root_subset_count = max(root_count_a, root_count_b)
        extension_tuple_count = max(tuple_count_a, tuple_count_b)
        distinguishes = bool(evaluated and signature_a != signature_b)
        classical_shadow = "individualization plus rooted two-extension graphlet tensor"
        if not evaluated:
            status = "skipped-scaling-cap"
            interpretation = (
                f"{root_size}-root individualized tensor signatures require {extension_tuple_count} rooted extension "
                f"tuples, exceeding cap {tuple_cap}; this is proof debt for implicit or sampled rooted tensor baselines."
            )
        elif distinguishes:
            status = "dequantized-by-individualized-tensor-shadow"
            interpretation = (
                f"{root_size}-root individualized rooted tensor signatures separate the graph pair classically; "
                "any matching collective observable is a rooted graphlet/tensor shadow."
            )
        else:
            status = "no-individualized-tensor-signal"
            interpretation = (
                f"{root_size}-root individualized rooted tensor signatures match; no separator was found at this budget."
            )
        records.append(
            IndividualizedTensorRecord(
                pair_id=pair_id,
                root_size=root_size,
                root_subset_count=root_subset_count,
                extension_tuple_count=extension_tuple_count,
                evaluated=evaluated,
                distinguishes=distinguishes,
                classical_shadow=classical_shadow,
                signature_a=_short(signature_a),
                signature_b=_short(signature_b),
                status=status,
                interpretation=interpretation,
            )
        )

    falsifiers = []
    if any(record.distinguishes for record in records):
        falsifiers.append("Individualized rooted graphlet/tensor signatures separate this graph/coset row classically.")
    if any(record.status == "skipped-scaling-cap" for record in records):
        falsifiers.append("Individualized rooted tensor enumeration hit scaling caps; unresolved rows are proof debt.")
    if any(record.distinguishes for record in records):
        status = "dequantized-by-individualized-tensor-shadow"
    elif any(record.status == "skipped-scaling-cap" for record in records):
        status = "individualized-tensor-proof-debt"
    else:
        status = "survives-individualized-tensor-baseline"
    return PairIndividualizedTensorAudit(spec, records, status, sorted(set(falsifiers)))


def run_individualized_tensor_observables(
    pair_ids: list[str] | None = None,
    max_root_size: int = 2,
    tuple_cap: int = 3_000_000,
) -> IndividualizedTensorObservableReport:
    active_pairs = pair_ids or DEFAULT_INDIVIDUALIZED_TENSOR_PAIR_IDS
    audits = [
        audit_individualized_tensor_pair(pair_id, max_root_size=max_root_size, tuple_cap=tuple_cap)
        for pair_id in active_pairs
    ]
    records = [record for audit in audits for record in audit.records]
    metrics = {
        "pair_count": len(audits),
        "record_count": len(records),
        "dequantized_pair_count": sum(1 for audit in audits if audit.status == "dequantized-by-individualized-tensor-shadow"),
        "survivor_pair_count": sum(1 for audit in audits if audit.status == "survives-individualized-tensor-baseline"),
        "proof_debt_pair_count": sum(1 for audit in audits if audit.status == "individualized-tensor-proof-debt"),
        "distinguishing_record_count": sum(1 for record in records if record.distinguishes),
        "skipped_record_count": sum(1 for record in records if record.status == "skipped-scaling-cap"),
        "nonclassical_candidate_count": 0,
        "max_root_subset_count": max((record.root_subset_count for record in records), default=0),
        "max_extension_tuple_count": max((record.extension_tuple_count for record in records), default=0),
    }
    if metrics["dequantized_pair_count"]:
        status = "individualized-tensor-shadows-collapse-rows"
    elif metrics["proof_debt_pair_count"]:
        status = "individualized-tensor-proof-debt"
    else:
        status = "survives-individualized-tensor-baseline"
    summary = (
        f"Audited {metrics['pair_count']} graph/coset pair(s) with individualized rooted tensor signatures up to "
        f"root size {max_root_size}. {metrics['dequantized_pair_count']} pair(s) were separated by classical rooted "
        f"tensor shadows, {metrics['survivor_pair_count']} survived, and {metrics['proof_debt_pair_count']} hit caps."
    )
    falsifiers = sorted({item for audit in audits for item in audit.falsifiers_triggered})
    return IndividualizedTensorObservableReport(
        utc_now(),
        max_root_size,
        tuple_cap,
        audits,
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


def write_individualized_tensor_negative_results(report: IndividualizedTensorObservableReport) -> int:
    written = 0
    for audit in report.pair_audits:
        distinguishing = [record for record in audit.records if record.distinguishes]
        if not distinguishing:
            continue
        best = min(distinguishing, key=lambda record: record.root_size)
        upsert_negative_result(
            NegativeResultRecord(
                id=f"INDIVIDUALIZED-TENSOR-SHADOW-{_safe_id(audit.pair.id)}",
                source="individualized_tensor_observables.py",
                claim=f"{audit.pair.id} supplies nonclassical collective-observable evidence.",
                reason_invalid=(
                    f"The pair is separated by {best.root_size}-root individualized rooted tensor signatures, "
                    f"a classical shadow: {best.classical_shadow}."
                ),
                lesson=(
                    "Do not promote coset-state observables until they are checked against individualized rooted "
                    "graphlet/tensor signatures, not just unrooted WL or small-pattern counts."
                ),
                applies_to=["CODE-COSET-COLLECTIVE", "HYP-LIT-COSET-OBSERVABLES", "PO-DEQUANTIZATION"],
                evidence={
                    "pair_id": audit.pair.id,
                    "root_size": best.root_size,
                    "root_subset_count": best.root_subset_count,
                    "extension_tuple_count": best.extension_tuple_count,
                    "status": best.status,
                    "classical_shadow": best.classical_shadow,
                },
            )
        )
        written += 1
    return written


def write_individualized_tensor_observables(
    output_path: Path = INDIVIDUALIZED_TENSOR_OBSERVABLES_PATH,
    pair_ids: list[str] | None = None,
    max_root_size: int = 2,
    tuple_cap: int = 3_000_000,
    write_registry: bool = True,
    registry_experiment_id: str = "EXP-COSET-INDIVIDUALIZED-TENSOR-OBSERVABLES",
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "RESULT-COSET-INDIVIDUALIZED-TENSOR-OBSERVABLES-LATEST",
) -> dict[str, Any]:
    report = run_individualized_tensor_observables(
        pair_ids=pair_ids,
        max_root_size=max_root_size,
        tuple_cap=tuple_cap,
    )
    payload = _json_ready(report)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    if write_registry:
        negative_results_written = write_individualized_tensor_negative_results(report)
        metrics = dict(report.headline_metrics)
        metrics["negative_results_written"] = negative_results_written
        falsifiers = list(report.falsifiers_triggered)
        if metrics["dequantized_pair_count"]:
            falsifiers.append("At least one graph/coset row is separated by individualized rooted tensor shadows.")
        if metrics["proof_debt_pair_count"]:
            falsifiers.append("Some rooted tensor baselines hit tuple caps and remain proof debt.")
        upsert_experiment_result(
            ExperimentResultRecord(
                id=registry_result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=report.created_at,
                status=report.status,
                summary=report.summary,
                metrics=metrics,
                falsifiers_triggered=sorted(set(falsifiers)),
                artifacts={"individualized_tensor_observables": str(output_path)},
            )
        )
    return payload
