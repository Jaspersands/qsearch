"""CFI base-family search beyond complete-graph gadgets.

The complete-graph CFI rows in this repository are now heavily dequantized:
the promised parity decoder and individualized WL both see through them.  This
module broadens the stress tests to several non-complete base graphs and
immediately attacks their CFI twists with cheap invariants and
individualization-refinement.  Survivors are proof debt, not evidence.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, is_dataclass
from itertools import combinations
from pathlib import Path
from typing import Any

import numpy as np

from coset_state_workbench import degree_signature, spectrum_signature, walk_count_signature, wl1_signature, wl2_signature
from individualized_wl_baseline import IndividualizedWLRecord, individualized_wl_multiset
from research_registry import ExperimentResultRecord, NegativeResultRecord, upsert_experiment_result, upsert_negative_result, utc_now


COSET_WORKBENCH_DIR = Path("research/coset_workbench")
CFI_BASE_FAMILY_SEARCH_PATH = COSET_WORKBENCH_DIR / "cfi_base_family_search.json"


@dataclass(frozen=True)
class CFIBaseSpec:
    id: str
    description: str
    vertex_count: int
    edge_count: int
    degree_sequence: list[int]
    twist_edge: tuple[int, int]
    construction_note: str


@dataclass(frozen=True)
class CFIBaseFamilyRecord:
    base: CFIBaseSpec
    cfi_vertex_count: int
    cfi_edge_count: int
    cheap_invariants_distinguish: bool
    wl2_distinguishes: bool
    individualized_records: list[IndividualizedWLRecord]
    first_individualized_separator: int | None
    exact_sanity_evaluated: bool
    exact_sanity_nonisomorphic: bool | None
    status: str
    interpretation: str


@dataclass(frozen=True)
class CFIBaseFamilySearchReport:
    created_at: str
    max_individualization: int
    tuple_cap: int
    exact_vertex_cap: int
    records: list[CFIBaseFamilyRecord]
    headline_metrics: dict[str, int]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def base_edges(adjacency: np.ndarray) -> list[tuple[int, int]]:
    return [
        (left, right)
        for left in range(adjacency.shape[0])
        for right in range(left + 1, adjacency.shape[0])
        if adjacency[left, right]
    ]


def base_graph_complete(n: int) -> np.ndarray:
    return np.ones((n, n), dtype=int) - np.eye(n, dtype=int)


def base_graph_prism() -> np.ndarray:
    adjacency = np.zeros((6, 6), dtype=int)
    for offset in (0, 3):
        for vertex in range(3):
            left = offset + vertex
            right = offset + ((vertex + 1) % 3)
            adjacency[left, right] = adjacency[right, left] = 1
    for vertex in range(3):
        adjacency[vertex, vertex + 3] = adjacency[vertex + 3, vertex] = 1
    return adjacency


def base_graph_cube() -> np.ndarray:
    adjacency = np.zeros((8, 8), dtype=int)
    for vertex in range(8):
        for bit in (1, 2, 4):
            neighbor = vertex ^ bit
            if vertex < neighbor:
                adjacency[vertex, neighbor] = adjacency[neighbor, vertex] = 1
    return adjacency


def base_graph_mobius_ladder(n: int = 8) -> np.ndarray:
    if n % 2 or n < 6:
        raise ValueError("Mobius ladder base requires an even n >= 6")
    adjacency = np.zeros((n, n), dtype=int)
    for vertex in range(n):
        adjacency[vertex, (vertex + 1) % n] = adjacency[(vertex + 1) % n, vertex] = 1
    for vertex in range(n // 2):
        adjacency[vertex, vertex + n // 2] = adjacency[vertex + n // 2, vertex] = 1
    return adjacency


def base_graph_petersen() -> np.ndarray:
    adjacency = np.zeros((10, 10), dtype=int)
    for vertex in range(5):
        adjacency[vertex, (vertex + 1) % 5] = adjacency[(vertex + 1) % 5, vertex] = 1
        adjacency[vertex, 5 + vertex] = adjacency[5 + vertex, vertex] = 1
        adjacency[5 + vertex, 5 + ((vertex + 2) % 5)] = adjacency[5 + ((vertex + 2) % 5), 5 + vertex] = 1
    return adjacency


def base_graph_heawood_like() -> np.ndarray:
    """A compact 3-regular bipartite incidence-style stress test.

    This is not claiming the full Heawood incidence construction; it supplies a
    deterministic cubic base with enough size to trigger individualization caps.
    """

    n = 14
    adjacency = np.zeros((n, n), dtype=int)
    for vertex in range(n):
        adjacency[vertex, (vertex + 1) % n] = adjacency[(vertex + 1) % n, vertex] = 1
    for vertex in range(7):
        adjacency[vertex, vertex + 7] = adjacency[vertex + 7, vertex] = 1
    return adjacency


def base_graph_by_id(base_id: str) -> tuple[str, np.ndarray]:
    if base_id == "complete-k4":
        return "Complete graph K4 ambiguous control", base_graph_complete(4)
    if base_id == "complete-k5":
        return "Complete graph K5 control", base_graph_complete(5)
    if base_id == "triangular-prism":
        return "Triangular prism cubic base", base_graph_prism()
    if base_id == "cube-q3":
        return "3-cube cubic base", base_graph_cube()
    if base_id == "mobius-ladder-8":
        return "Mobius ladder M8 cubic base", base_graph_mobius_ladder(8)
    if base_id == "petersen":
        return "Petersen graph cubic base", base_graph_petersen()
    if base_id == "heawood-like-14":
        return "14-vertex cubic incidence-style base", base_graph_heawood_like()
    raise ValueError(f"unknown CFI base id: {base_id}")


DEFAULT_BASE_IDS = ["complete-k5", "triangular-prism", "cube-q3", "mobius-ladder-8", "petersen", "heawood-like-14"]


def cfi_parity_graph_from_base(base_adjacency: np.ndarray, twisted_edge: tuple[int, int] | None = None) -> np.ndarray:
    base_adjacency = np.asarray(base_adjacency, dtype=np.uint8)
    vertices = list(range(base_adjacency.shape[0]))
    edges = base_edges(base_adjacency)
    normalized_twist = tuple(sorted(twisted_edge)) if twisted_edge is not None else None
    incident: dict[int, list[tuple[int, int]]] = {vertex: [] for vertex in vertices}
    for edge in edges:
        left, right = edge
        incident[left].append(edge)
        incident[right].append(edge)

    cfi_vertices: list[tuple[Any, ...]] = []
    index: dict[tuple[Any, ...], int] = {}
    for vertex in vertices:
        degree = len(incident[vertex])
        for mask in range(1 << degree):
            if mask.bit_count() % 2 == 0:
                key = ("middle", vertex, mask)
                index[key] = len(cfi_vertices)
                cfi_vertices.append(key)
    for edge in edges:
        for bit in (0, 1):
            key = ("edge", edge, bit)
            index[key] = len(cfi_vertices)
            cfi_vertices.append(key)

    adjacency = np.zeros((len(cfi_vertices), len(cfi_vertices)), dtype=np.uint8)
    for vertex in vertices:
        local_edges = incident[vertex]
        for mask in range(1 << len(local_edges)):
            if mask.bit_count() % 2:
                continue
            middle_index = index[("middle", vertex, mask)]
            for position, edge in enumerate(local_edges):
                selected_bit = (mask >> position) & 1
                twist = 1 if normalized_twist == edge and vertex == edge[0] else 0
                edge_index = index[("edge", edge, selected_bit ^ twist)]
                adjacency[middle_index, edge_index] = 1
                adjacency[edge_index, middle_index] = 1
    return adjacency.astype(int)


def _edge_count(adjacency: np.ndarray) -> int:
    return int(adjacency.sum() // 2)


def _exact_sanity_nonisomorphic(graph_a: np.ndarray, graph_b: np.ndarray, vertex_cap: int) -> tuple[bool, bool | None]:
    if int(graph_a.shape[0]) > vertex_cap:
        return False, None
    try:
        import networkx as nx  # type: ignore
    except Exception:
        return False, None
    isomorphic = bool(nx.is_isomorphic(nx.from_numpy_array(graph_a), nx.from_numpy_array(graph_b)))
    return True, not isomorphic


def audit_cfi_base_family(
    base_id: str,
    max_individualization: int = 3,
    tuple_cap: int = 40_000,
    exact_vertex_cap: int = 50,
) -> CFIBaseFamilyRecord:
    description, base = base_graph_by_id(base_id)
    edge = base_edges(base)[0]
    untwisted = cfi_parity_graph_from_base(base, twisted_edge=None)
    twisted = cfi_parity_graph_from_base(base, twisted_edge=edge)
    wl2_a = wl2_signature(untwisted)
    wl2_b = wl2_signature(twisted)
    cheap_a = (
        degree_signature(untwisted),
        spectrum_signature(untwisted),
        walk_count_signature(untwisted, max_length=8),
        wl1_signature(untwisted),
        wl2_a,
    )
    cheap_b = (
        degree_signature(twisted),
        spectrum_signature(twisted),
        walk_count_signature(twisted, max_length=8),
        wl1_signature(twisted),
        wl2_b,
    )
    cheap_distinguishes = cheap_a != cheap_b
    wl2_distinguishes = wl2_a != wl2_b

    individualized: list[IndividualizedWLRecord] = []
    first_separator: int | None = None
    for size in range(1, max_individualization + 1):
        eval_a, tuple_count_a, signature_a = individualized_wl_multiset(untwisted, size, tuple_cap)
        eval_b, tuple_count_b, signature_b = individualized_wl_multiset(twisted, size, tuple_cap)
        evaluated = bool(eval_a and eval_b)
        tuple_count = max(tuple_count_a, tuple_count_b)
        distinguishes = bool(evaluated and signature_a != signature_b)
        if distinguishes and first_separator is None:
            first_separator = size
        if not evaluated:
            status = "skipped-scaling-cap"
            interpretation = f"{size}-individualization skipped at {tuple_count} tuples above cap {tuple_cap}."
        elif distinguishes:
            status = "dequantized-by-individualized-wl"
            interpretation = f"{size}-individualization plus color refinement separates this CFI twist."
        else:
            status = "no-individualized-wl-signal"
            interpretation = f"{size}-individualization plus color refinement does not separate this CFI twist."
        individualized.append(
            IndividualizedWLRecord(
                pair_id=f"cfi-base-{base_id}",
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

    exact_evaluated, exact_nonisomorphic = _exact_sanity_nonisomorphic(untwisted, twisted, exact_vertex_cap)
    if cheap_distinguishes or wl2_distinguishes:
        status = "dequantized-by-low-cost-invariant"
        interpretation = "Low-cost graph invariants or WL2 separate this CFI base row."
    elif first_separator is not None:
        status = "dequantized-by-individualized-wl"
        interpretation = f"{first_separator}-vertex individualization-refinement separates this CFI base row."
    elif any(record.status == "skipped-scaling-cap" for record in individualized):
        status = "survives-tested-baselines-proof-debt"
        interpretation = "The row survives evaluated baselines but higher individualization hit caps; keep as proof debt."
    else:
        status = "finite-survivor-needs-proof"
        interpretation = "The row survives the implemented finite baselines; do not promote without asymptotic proof and stronger attacks."
    if exact_evaluated and exact_nonisomorphic is False:
        status = "twist-isomorphic-control-invalid"
        interpretation = "Exact GI sanity check found the twisted and untwisted rows isomorphic; this base row is not useful."

    degrees = [int(value) for value in base.sum(axis=1).tolist()]
    spec = CFIBaseSpec(
        id=base_id,
        description=description,
        vertex_count=int(base.shape[0]),
        edge_count=len(base_edges(base)),
        degree_sequence=sorted(degrees),
        twist_edge=edge,
        construction_note="Odd single-edge twist in the local CFI parity gadget over this base graph.",
    )
    return CFIBaseFamilyRecord(
        base=spec,
        cfi_vertex_count=int(untwisted.shape[0]),
        cfi_edge_count=_edge_count(untwisted),
        cheap_invariants_distinguish=cheap_distinguishes,
        wl2_distinguishes=wl2_distinguishes,
        individualized_records=individualized,
        first_individualized_separator=first_separator,
        exact_sanity_evaluated=exact_evaluated,
        exact_sanity_nonisomorphic=exact_nonisomorphic,
        status=status,
        interpretation=interpretation,
    )


def run_cfi_base_family_search(
    base_ids: list[str] | None = None,
    max_individualization: int = 3,
    tuple_cap: int = 40_000,
    exact_vertex_cap: int = 50,
) -> CFIBaseFamilySearchReport:
    active = base_ids or DEFAULT_BASE_IDS
    records = [
        audit_cfi_base_family(
            base_id,
            max_individualization=max_individualization,
            tuple_cap=tuple_cap,
            exact_vertex_cap=exact_vertex_cap,
        )
        for base_id in active
    ]
    metrics = {
        "base_count": len(records),
        "low_cost_dequantized_count": sum(1 for record in records if record.status == "dequantized-by-low-cost-invariant"),
        "individualized_wl_dequantized_count": sum(1 for record in records if record.status == "dequantized-by-individualized-wl"),
        "proof_debt_survivor_count": sum(1 for record in records if record.status == "survives-tested-baselines-proof-debt"),
        "finite_survivor_count": sum(1 for record in records if record.status == "finite-survivor-needs-proof"),
        "invalid_isomorphic_count": sum(1 for record in records if record.status == "twist-isomorphic-control-invalid"),
        "max_cfi_vertex_count": max((record.cfi_vertex_count for record in records), default=0),
    }
    dequantized = metrics["low_cost_dequantized_count"] + metrics["individualized_wl_dequantized_count"]
    survivors = metrics["proof_debt_survivor_count"] + metrics["finite_survivor_count"]
    if survivors:
        status = "cfi-base-survivors-are-proof-debt"
    elif dequantized:
        status = "all-cfi-bases-dequantized-or-invalid"
    else:
        status = "cfi-base-search-incomplete"
    summary = (
        f"Audited {metrics['base_count']} CFI base family row(s). {dequantized} were dequantized by implemented baselines; "
        f"{survivors} survived only as proof debt."
    )
    falsifiers = []
    if dequantized:
        falsifiers.append("Some CFI base rows are separated by low-cost or individualized-WL classical baselines.")
    if survivors:
        falsifiers.append("Surviving CFI base rows lack asymptotic proof, exact sanity, or stronger individualization baselines.")
    return CFIBaseFamilySearchReport(utc_now(), max_individualization, tuple_cap, exact_vertex_cap, records, metrics, status, summary, falsifiers)


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


def write_cfi_base_family_negative_results(report: CFIBaseFamilySearchReport) -> int:
    written = 0
    for record in report.records:
        if record.status not in {
            "dequantized-by-low-cost-invariant",
            "dequantized-by-individualized-wl",
            "twist-isomorphic-control-invalid",
        }:
            continue
        upsert_negative_result(
            NegativeResultRecord(
                id=f"CFI-BASE-FAMILY-REJECTED-{_safe_id(record.base.id)}",
                source="cfi_base_family_search.py",
                claim=f"CFI base {record.base.id} supplies nonclassical coset-state evidence.",
                reason_invalid=record.interpretation,
                lesson=(
                    "CFI base-family rows must survive low-cost invariants, individualized-WL, exact sanity checks, "
                    "and structural parity decoders before motivating quantum collective measurements."
                ),
                applies_to=["CODE-COSET-COLLECTIVE", "PO-DEQUANTIZATION", "PO-FALSIFIERS"],
                evidence=asdict(record),
            )
        )
        written += 1
    return written


def write_cfi_base_family_search(
    output_path: Path = CFI_BASE_FAMILY_SEARCH_PATH,
    base_ids: list[str] | None = None,
    max_individualization: int = 3,
    tuple_cap: int = 40_000,
    exact_vertex_cap: int = 50,
    write_registry: bool = True,
    registry_experiment_id: str = "EXP-COSET-CFI-BASE-FAMILY-SEARCH",
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "RESULT-COSET-CFI-BASE-FAMILY-SEARCH-LATEST",
) -> dict[str, Any]:
    report = run_cfi_base_family_search(
        base_ids=base_ids,
        max_individualization=max_individualization,
        tuple_cap=tuple_cap,
        exact_vertex_cap=exact_vertex_cap,
    )
    payload = _json_ready(report)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    if write_registry:
        negative_results_written = write_cfi_base_family_negative_results(report)
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
                artifacts={"cfi_base_family_search": str(output_path)},
            )
        )
    return payload
