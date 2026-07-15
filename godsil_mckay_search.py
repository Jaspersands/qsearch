"""Godsil-McKay switching search for coset-frontier row generation.

Godsil-McKay switching is a natural source of cospectral graph pairs and a
reasonable stress test for graph-isomorphism/nonabelian-HSP ideas.  This module
does not treat cospectrality as evidence.  It searches deterministic switching
sets, then immediately attacks every non-isomorphic switched row with WL,
graphlet, individualization, rooted tensor, and exact-isomorphism baselines.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, is_dataclass
from itertools import combinations
from pathlib import Path
from typing import Any

import networkx as nx
import numpy as np

from coset_state_workbench import (
    GraphPairSpec,
    degree_signature,
    spectrum_signature,
    walk_count_signature,
    wl2_signature,
    wl_k_signature,
)
from graphlet_tensor_observables import graphlet_tensor_signature, homomorphism_moment_signature
from individualized_tensor_observables import rooted_tensor_multiset
from individualized_wl_baseline import individualized_wl_multiset
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


COSET_WORKBENCH_DIR = Path("research/coset_workbench")
GODSil_MCKAY_SEARCH_PATH = COSET_WORKBENCH_DIR / "godsil_mckay_switching_search.json"


@dataclass(frozen=True)
class GMSearchSpec:
    id: str
    graph_family: str
    vertex_count: int
    switching_set_sizes: list[int]
    max_subsets_checked: int
    max_records: int
    construction_note: str


@dataclass(frozen=True)
class GMBaselineRecord:
    name: str
    evaluated: bool
    distinguishes: bool
    status: str
    detail: str


@dataclass(frozen=True)
class GMSwitchingRecord:
    id: str
    spec: GMSearchSpec
    pair: GraphPairSpec
    switching_set: list[int]
    half_neighbor_vertices: int
    subsets_checked_before_hit: int
    exact_nonisomorphic: bool
    cospectral: bool
    baselines: list[GMBaselineRecord]
    status: str
    interpretation: str


@dataclass(frozen=True)
class GMFamilySearchRecord:
    spec: GMSearchSpec
    subsets_checked: int
    valid_switching_sets_seen: int
    records: list[GMSwitchingRecord]
    status: str
    interpretation: str


@dataclass(frozen=True)
class GodsilMckaySearchReport:
    created_at: str
    family_records: list[GMFamilySearchRecord]
    headline_metrics: dict[str, int]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def rook_graph(rows: int, cols: int) -> np.ndarray:
    vertices = [(row, col) for row in range(rows) for col in range(cols)]
    adjacency = np.zeros((len(vertices), len(vertices)), dtype=int)
    for left, (row_l, col_l) in enumerate(vertices):
        for right, (row_r, col_r) in enumerate(vertices):
            if left != right and (row_l == row_r or col_l == col_r):
                adjacency[left, right] = 1
    return adjacency


def shrikhande_graph() -> np.ndarray:
    vertices = [(x, y) for x in range(4) for y in range(4)]
    index = {vertex: idx for idx, vertex in enumerate(vertices)}
    connections = {(1, 0), (3, 0), (0, 1), (0, 3), (1, 1), (3, 3)}
    adjacency = np.zeros((16, 16), dtype=int)
    for left, (x, y) in enumerate(vertices):
        for dx, dy in connections:
            adjacency[left, index[((x + dx) % 4, (y + dy) % 4)]] = 1
    return adjacency


def base_graph_for_spec(spec_id: str) -> np.ndarray:
    if spec_id == "rook-4x4":
        return rook_graph(4, 4)
    if spec_id == "shrikhande-z4x4":
        return shrikhande_graph()
    if spec_id == "rook-3x4-control":
        return rook_graph(3, 4)
    raise ValueError(f"unknown Godsil-McKay search spec: {spec_id}")


DEFAULT_GM_SPECS = [
    GMSearchSpec(
        id="rook-4x4",
        graph_family="4x4 rook graph",
        vertex_count=16,
        switching_set_sizes=[4],
        max_subsets_checked=20_000,
        max_records=1,
        construction_note="Search 4-vertex Godsil-McKay switching sets inside the lattice/rook graph family.",
    ),
    GMSearchSpec(
        id="shrikhande-z4x4",
        graph_family="Shrikhande Cayley graph on Z_4 x Z_4",
        vertex_count=16,
        switching_set_sizes=[4],
        max_subsets_checked=20_000,
        max_records=1,
        construction_note="Search 4-vertex Godsil-McKay switching sets in a strongly regular Cayley graph.",
    ),
    GMSearchSpec(
        id="rook-3x4-control",
        graph_family="3x4 rectangular rook graph control",
        vertex_count=12,
        switching_set_sizes=[4],
        max_subsets_checked=20_000,
        max_records=1,
        construction_note="Control search where valid switching sets tend to produce isomorphic rows.",
    ),
]


def godsil_mckay_switching_vertices(adjacency: np.ndarray, subset: tuple[int, ...]) -> tuple[bool, list[int]]:
    subset_set = set(subset)
    size = len(subset)
    if size == 0 or size % 2:
        return False, []
    internal_degrees = {
        int(sum(adjacency[vertex, other] for other in subset_set if other != vertex))
        for vertex in subset_set
    }
    if len(internal_degrees) != 1:
        return False, []
    half_vertices: list[int] = []
    for vertex in range(int(adjacency.shape[0])):
        if vertex in subset_set:
            continue
        count = int(sum(adjacency[vertex, other] for other in subset_set))
        if count not in {0, size // 2, size}:
            return False, []
        if count == size // 2:
            half_vertices.append(vertex)
    return bool(half_vertices), half_vertices


def switch_graph(adjacency: np.ndarray, subset: tuple[int, ...], half_vertices: list[int]) -> np.ndarray:
    switched = np.array(adjacency, copy=True)
    for vertex in half_vertices:
        for root in subset:
            switched[vertex, root] = switched[root, vertex] = 1 - int(switched[vertex, root])
    return switched


def _short(value: Any, limit: int = 500) -> str:
    text = str(value)
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."


def _baseline(name: str, evaluated: bool, distinguishes: bool, detail: str) -> GMBaselineRecord:
    if not evaluated:
        status = "skipped-scaling-cap"
    elif distinguishes:
        status = "dequantized-by-classical-baseline"
    else:
        status = "no-signal"
    return GMBaselineRecord(name, evaluated, distinguishes, status, detail)


def evaluate_gm_baselines(
    graph_a: np.ndarray,
    graph_b: np.ndarray,
    wl_tuple_cap: int,
    graphlet_tuple_cap: int,
    individualization_cap: int,
    rooted_tensor_cap: int,
) -> list[GMBaselineRecord]:
    n = int(graph_a.shape[0])
    records: list[GMBaselineRecord] = []
    records.append(
        _baseline(
            "degree-spectrum-walk-wl2",
            True,
            (
                degree_signature(graph_a),
                spectrum_signature(graph_a),
                walk_count_signature(graph_a, max_length=8),
                wl2_signature(graph_a),
            )
            != (
                degree_signature(graph_b),
                spectrum_signature(graph_b),
                walk_count_signature(graph_b, max_length=8),
                wl2_signature(graph_b),
            ),
            "Degree, spectrum, walk-count, and WL2 signatures are cheap classical shadows.",
        )
    )

    wl3_count = n**3
    wl3_eval = wl3_count <= wl_tuple_cap
    records.append(
        _baseline(
            "3-wl",
            wl3_eval,
            wl3_eval and wl_k_signature(graph_a, k=3) != wl_k_signature(graph_b, k=3),
            f"3-WL tuple count {wl3_count}; cap {wl_tuple_cap}.",
        )
    )
    wl4_count = n**4
    wl4_eval = wl4_count <= wl_tuple_cap
    records.append(
        _baseline(
            "4-wl",
            wl4_eval,
            wl4_eval and wl_k_signature(graph_a, k=4, rounds=3) != wl_k_signature(graph_b, k=4, rounds=3),
            f"4-WL tuple count {wl4_count}; cap {wl_tuple_cap}.",
        )
    )

    graphlet_count = n * (n - 1) * (n - 2) * (n - 3) // 24
    graphlet_eval = graphlet_count <= graphlet_tuple_cap
    records.append(
        _baseline(
            "graphlet-tensor",
            graphlet_eval,
            graphlet_eval
            and (
                homomorphism_moment_signature(graph_a),
                graphlet_tensor_signature(graph_a, graphlet_tuple_cap),
            )
            != (
                homomorphism_moment_signature(graph_b),
                graphlet_tensor_signature(graph_b, graphlet_tuple_cap),
            ),
            f"Four-vertex graphlet tuple count {graphlet_count}; cap {graphlet_tuple_cap}.",
        )
    )

    for size in (1, 2):
        eval_a, count_a, signature_a = individualized_wl_multiset(graph_a, size, individualization_cap)
        eval_b, count_b, signature_b = individualized_wl_multiset(graph_b, size, individualization_cap)
        evaluated = bool(eval_a and eval_b)
        records.append(
            _baseline(
                f"individualized-wl-{size}",
                evaluated,
                evaluated and signature_a != signature_b,
                f"{size}-individualization count {max(count_a, count_b)}; cap {individualization_cap}.",
            )
        )

    for root_size in (1, 2):
        eval_a, _, count_a, signature_a = rooted_tensor_multiset(graph_a, root_size, rooted_tensor_cap)
        eval_b, _, count_b, signature_b = rooted_tensor_multiset(graph_b, root_size, rooted_tensor_cap)
        evaluated = bool(eval_a and eval_b)
        records.append(
            _baseline(
                f"rooted-tensor-{root_size}",
                evaluated,
                evaluated and signature_a != signature_b,
                f"{root_size}-root extension tuple count {max(count_a, count_b)}; cap {rooted_tensor_cap}.",
            )
        )
    return records


def audit_switched_pair(
    spec: GMSearchSpec,
    adjacency: np.ndarray,
    subset: tuple[int, ...],
    half_vertices: list[int],
    subsets_checked_before_hit: int,
    wl_tuple_cap: int,
    graphlet_tuple_cap: int,
    individualization_cap: int,
    rooted_tensor_cap: int,
) -> GMSwitchingRecord:
    switched = switch_graph(adjacency, subset, half_vertices)
    exact_nonisomorphic = not nx.is_isomorphic(nx.from_numpy_array(adjacency), nx.from_numpy_array(switched))
    cospectral = spectrum_signature(adjacency) == spectrum_signature(switched)
    baselines = evaluate_gm_baselines(
        adjacency,
        switched,
        wl_tuple_cap=wl_tuple_cap,
        graphlet_tuple_cap=graphlet_tuple_cap,
        individualization_cap=individualization_cap,
        rooted_tensor_cap=rooted_tensor_cap,
    )
    distinguishing = [record for record in baselines if record.distinguishes]
    skipped = [record for record in baselines if not record.evaluated]
    if not exact_nonisomorphic:
        status = "isomorphic-switch-control"
        interpretation = "Switching set is valid and cospectral but the switched graph is isomorphic; this is a control, not a frontier row."
    elif not cospectral:
        status = "invalid-not-cospectral"
        interpretation = "Implementation sanity check failed: Godsil-McKay switch did not preserve spectrum."
    elif distinguishing:
        status = "dequantized-by-gm-classical-baseline"
        interpretation = (
            "The switched pair is cospectral and non-isomorphic, but classical baselines distinguish it: "
            + ", ".join(record.name for record in distinguishing)
        )
    elif skipped:
        status = "gm-proof-debt-due-to-caps"
        interpretation = "The pair survives evaluated baselines but some higher classical shadows hit caps; keep as proof debt."
    else:
        status = "gm-survives-current-baselines-measurement-proof-debt"
        interpretation = "The pair survives implemented baselines; it is only a row for future measurement proof debt."

    pair_id = f"gm-{spec.id}-{len(subset)}-{subsets_checked_before_hit}"
    return GMSwitchingRecord(
        id=pair_id,
        spec=spec,
        pair=GraphPairSpec(
            id=pair_id,
            graph_a=f"{spec.graph_family} before Godsil-McKay switching",
            graph_b=f"{spec.graph_family} after Godsil-McKay switching",
            vertex_count=int(adjacency.shape[0]),
            known_nonisomorphic=exact_nonisomorphic,
            reason=(
                "Godsil-McKay switching preserves spectrum; exact isomorphism check determines whether this row is a "
                "non-isomorphic graph-pair stress test."
            ),
        ),
        switching_set=list(subset),
        half_neighbor_vertices=len(half_vertices),
        subsets_checked_before_hit=subsets_checked_before_hit,
        exact_nonisomorphic=exact_nonisomorphic,
        cospectral=cospectral,
        baselines=baselines,
        status=status,
        interpretation=interpretation,
    )


def search_gm_family(
    spec: GMSearchSpec,
    wl_tuple_cap: int = 120_000,
    graphlet_tuple_cap: int = 1_000_000,
    individualization_cap: int = 40_000,
    rooted_tensor_cap: int = 3_000_000,
) -> GMFamilySearchRecord:
    adjacency = base_graph_for_spec(spec.id)
    records: list[GMSwitchingRecord] = []
    subsets_checked = 0
    valid_seen = 0
    for size in spec.switching_set_sizes:
        for subset in combinations(range(int(adjacency.shape[0])), size):
            subsets_checked += 1
            valid, half_vertices = godsil_mckay_switching_vertices(adjacency, subset)
            if not valid:
                if subsets_checked >= spec.max_subsets_checked:
                    break
                continue
            valid_seen += 1
            record = audit_switched_pair(
                spec,
                adjacency,
                subset,
                half_vertices,
                subsets_checked,
                wl_tuple_cap=wl_tuple_cap,
                graphlet_tuple_cap=graphlet_tuple_cap,
                individualization_cap=individualization_cap,
                rooted_tensor_cap=rooted_tensor_cap,
            )
            if record.exact_nonisomorphic:
                records.append(record)
            if len(records) >= spec.max_records or subsets_checked >= spec.max_subsets_checked:
                break
        if len(records) >= spec.max_records or subsets_checked >= spec.max_subsets_checked:
            break

    if records:
        if any(record.status == "gm-survives-current-baselines-measurement-proof-debt" for record in records):
            status = "gm-survivor-proof-debt"
        elif any(record.status == "gm-proof-debt-due-to-caps" for record in records):
            status = "gm-cap-proof-debt"
        else:
            status = "gm-rows-dequantized"
        interpretation = f"Found {len(records)} non-isomorphic Godsil-McKay switched row(s)."
    elif valid_seen:
        status = "only-isomorphic-switch-controls"
        interpretation = "Valid switching sets were found, but all checked switched graphs were isomorphic controls."
    else:
        status = "no-valid-switching-row-found"
        interpretation = "No valid switching set was found under the deterministic search cap."
    return GMFamilySearchRecord(spec, subsets_checked, valid_seen, records, status, interpretation)


def run_godsil_mckay_search(
    specs: list[GMSearchSpec] | None = None,
    wl_tuple_cap: int = 120_000,
    graphlet_tuple_cap: int = 1_000_000,
    individualization_cap: int = 40_000,
    rooted_tensor_cap: int = 3_000_000,
) -> GodsilMckaySearchReport:
    active_specs = specs or DEFAULT_GM_SPECS
    family_records = [
        search_gm_family(
            spec,
            wl_tuple_cap=wl_tuple_cap,
            graphlet_tuple_cap=graphlet_tuple_cap,
            individualization_cap=individualization_cap,
            rooted_tensor_cap=rooted_tensor_cap,
        )
        for spec in active_specs
    ]
    records = [record for family in family_records for record in family.records]
    metrics = {
        "family_count": len(family_records),
        "row_count": len(records),
        "nonisomorphic_cospectral_count": sum(1 for record in records if record.exact_nonisomorphic and record.cospectral),
        "dequantized_row_count": sum(1 for record in records if record.status == "dequantized-by-gm-classical-baseline"),
        "proof_debt_row_count": sum(1 for record in records if record.status == "gm-proof-debt-due-to-caps"),
        "survivor_row_count": sum(
            1 for record in records if record.status == "gm-survives-current-baselines-measurement-proof-debt"
        ),
        "control_family_count": sum(1 for family in family_records if family.status == "only-isomorphic-switch-controls"),
        "no_valid_switching_family_count": sum(1 for family in family_records if family.status == "no-valid-switching-row-found"),
        "valid_switching_sets_seen": sum(family.valid_switching_sets_seen for family in family_records),
        "subsets_checked": sum(family.subsets_checked for family in family_records),
        "nonclassical_candidate_count": 0,
    }
    if metrics["survivor_row_count"] or metrics["proof_debt_row_count"]:
        status = "gm-search-produced-proof-debt-rows"
    elif metrics["dequantized_row_count"]:
        status = "gm-search-dequantized-current-rows"
    else:
        status = "gm-search-no-frontier-row"
    summary = (
        f"Godsil-McKay search checked {metrics['subsets_checked']} subsets across {metrics['family_count']} graph families, "
        f"found {metrics['nonisomorphic_cospectral_count']} non-isomorphic cospectral row(s), dequantized "
        f"{metrics['dequantized_row_count']} row(s), and left {metrics['survivor_row_count'] + metrics['proof_debt_row_count']} row(s) as proof debt."
    )
    falsifiers = []
    if metrics["dequantized_row_count"]:
        falsifiers.append("Godsil-McKay switched rows were distinguished by classical WL/graphlet/individualization/rooted-tensor baselines.")
    if metrics["survivor_row_count"] or metrics["proof_debt_row_count"]:
        falsifiers.append("Any surviving Godsil-McKay row is proof debt only until stronger baselines and measurement proofs exist.")
    return GodsilMckaySearchReport(utc_now(), family_records, metrics, status, summary, falsifiers)


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


def write_godsil_mckay_negative_results(report: GodsilMckaySearchReport) -> int:
    written = 0
    for family in report.family_records:
        for record in family.records:
            if record.status != "dequantized-by-gm-classical-baseline":
                continue
            distinguishing = [baseline.name for baseline in record.baselines if baseline.distinguishes]
            upsert_negative_result(
                NegativeResultRecord(
                    id=f"GM-SWITCHING-DEQUANTIZED-{_safe_id(record.id)}",
                    source="godsil_mckay_search.py",
                    claim=f"Godsil-McKay switched row {record.id} supplies nonclassical coset-state evidence.",
                    reason_invalid=(
                        "The row is cospectral and non-isomorphic but is separated by classical baselines: "
                        + ", ".join(distinguishing)
                    ),
                    lesson=(
                        "Cospectral graph generation is not enough.  Graph/coset rows must survive WL, graphlet, "
                        "individualization, rooted tensor, and exact sanity baselines before measurement design."
                    ),
                    applies_to=["CODE-COSET-COLLECTIVE", "HYP-LIT-COSET-OBSERVABLES", "PO-DEQUANTIZATION"],
                    evidence={
                        "pair_id": record.pair.id,
                        "spec_id": record.spec.id,
                        "switching_set": record.switching_set,
                        "half_neighbor_vertices": record.half_neighbor_vertices,
                        "distinguishing_baselines": distinguishing,
                    },
                )
            )
            written += 1
    return written


def write_godsil_mckay_search(
    output_path: Path = GODSil_MCKAY_SEARCH_PATH,
    specs: list[GMSearchSpec] | None = None,
    wl_tuple_cap: int = 120_000,
    graphlet_tuple_cap: int = 1_000_000,
    individualization_cap: int = 40_000,
    rooted_tensor_cap: int = 3_000_000,
    write_registry: bool = True,
    registry_experiment_id: str = "EXP-COSET-GM-SWITCHING-SEARCH",
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "RESULT-COSET-GM-SWITCHING-SEARCH-LATEST",
) -> dict[str, Any]:
    report = run_godsil_mckay_search(
        specs=specs,
        wl_tuple_cap=wl_tuple_cap,
        graphlet_tuple_cap=graphlet_tuple_cap,
        individualization_cap=individualization_cap,
        rooted_tensor_cap=rooted_tensor_cap,
    )
    payload = _json_ready(report)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    if write_registry:
        negative_results_written = write_godsil_mckay_negative_results(report)
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
                artifacts={"godsil_mckay_search": str(output_path)},
            )
        )
    return payload
