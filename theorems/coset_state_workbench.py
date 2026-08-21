"""Coset-state and nonabelian HSP workbench.

This workbench focuses on hidden-permutation boundary cases where naive
nonabelian Fourier sampling is known to be inadequate.  It starts with explicit
strongly regular graph pairs, computes classical invariant baselines, and
records whether low-register relation observables have any signal beyond those
baselines.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, is_dataclass
from itertools import combinations
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import ExperimentResultRecord, NegativeResultRecord, upsert_experiment_result, upsert_negative_result, utc_now


COSET_WORKBENCH_DIR = Path("research/coset_workbench")
COSET_AUDIT_PATH = COSET_WORKBENCH_DIR / "nonabelian_hsp_audit.json"


@dataclass(frozen=True)
class GraphPairSpec:
    id: str
    graph_a: str
    graph_b: str
    vertex_count: int
    known_nonisomorphic: bool
    reason: str


@dataclass(frozen=True)
class InvariantResult:
    name: str
    distinguishes: bool
    signature_a: str
    signature_b: str
    interpretation: str


@dataclass(frozen=True)
class RelationObservableResult:
    name: str
    distinguishes: bool
    value_a: str
    value_b: str
    interpretation: str


@dataclass(frozen=True)
class WLScalingResult:
    k: int
    rounds: int
    tuple_count: int
    evaluated: bool
    distinguishes: bool
    signature_a: str
    signature_b: str
    interpretation: str


@dataclass(frozen=True)
class ExactIsomorphismCheck:
    name: str
    evaluated: bool
    isomorphic: bool | None
    supports_known_status: bool
    cost_model: str
    interpretation: str


@dataclass(frozen=True)
class CosetPairAudit:
    pair: GraphPairSpec
    classical_invariants: list[InvariantResult]
    relation_observables: list[RelationObservableResult]
    wl_scaling: list[WLScalingResult]
    exact_isomorphism_check: ExactIsomorphismCheck
    positive_signal: str
    falsifiers_triggered: list[str]


@dataclass(frozen=True)
class CosetWorkbenchResult:
    created_at: str
    pair_audits: list[CosetPairAudit]
    summary: str
    falsifiers_triggered: list[str]


def rook_graph_4x4() -> np.ndarray:
    """Return the 4x4 rook graph adjacency matrix."""

    vertices = [(row, col) for row in range(4) for col in range(4)]
    n = len(vertices)
    adjacency = np.zeros((n, n), dtype=int)
    for i, (row_i, col_i) in enumerate(vertices):
        for j, (row_j, col_j) in enumerate(vertices):
            if i != j and (row_i == row_j or col_i == col_j):
                adjacency[i, j] = 1
    return adjacency


def shrikhande_graph() -> np.ndarray:
    """Return the Shrikhande graph adjacency matrix.

    It is the Cayley graph on Z_4 x Z_4 with connection set
    +/-(1,0), +/-(0,1), +/-(1,1).  Together with the 4x4 rook graph it gives a
    standard pair of non-isomorphic strongly regular graphs with parameters
    (16, 6, 2, 2).
    """

    vertices = [(x, y) for x in range(4) for y in range(4)]
    index = {vertex: idx for idx, vertex in enumerate(vertices)}
    connections = {(1, 0), (3, 0), (0, 1), (0, 3), (1, 1), (3, 3)}
    adjacency = np.zeros((16, 16), dtype=int)
    for i, (x, y) in enumerate(vertices):
        for dx, dy in connections:
            j = index[((x + dx) % 4, (y + dy) % 4)]
            adjacency[i, j] = 1
    return adjacency


def cycle_graph(n: int) -> np.ndarray:
    adjacency = np.zeros((n, n), dtype=int)
    for vertex in range(n):
        adjacency[vertex, (vertex - 1) % n] = 1
        adjacency[vertex, (vertex + 1) % n] = 1
    return adjacency


def chorded_cycle_graph(n: int) -> np.ndarray:
    adjacency = cycle_graph(n)
    for vertex in range(n):
        adjacency[vertex, (vertex + 2) % n] = 1
        adjacency[(vertex + 2) % n, vertex] = 1
    return adjacency


def cfi_parity_graph_complete(base_size: int, twisted_edge: tuple[int, int] | None = None) -> np.ndarray:
    """CFI-style parity gadget over a complete base graph.

    For each base vertex v, create one middle vertex for every even subset of
    incident base edges.  For each base edge e, create two edge vertices.  A
    twist flips one endpoint's attachment convention for one base edge.  The
    untwisted and single-twist graphs are compact hidden-permutation stress
    tests: low-dimensional WL and spectral checks should fail before exact or
    high-dimensional methods see the parity obstruction.
    """

    if base_size < 4:
        raise ValueError("CFI complete-graph base must have at least 4 vertices")

    base_vertices = list(range(base_size))
    base_edges = [tuple(sorted(edge)) for edge in combinations(base_vertices, 2)]
    normalized_twist = tuple(sorted(twisted_edge)) if twisted_edge is not None else None
    incident_edges: dict[int, list[tuple[int, int]]] = {vertex: [] for vertex in base_vertices}
    for edge in base_edges:
        left, right = edge
        incident_edges[left].append(edge)
        incident_edges[right].append(edge)

    vertices: list[tuple[Any, ...]] = []
    index: dict[tuple[Any, ...], int] = {}
    for vertex in base_vertices:
        degree = len(incident_edges[vertex])
        for mask in range(1 << degree):
            if mask.bit_count() % 2 == 0:
                key = ("middle", vertex, mask)
                index[key] = len(vertices)
                vertices.append(key)
    for edge in base_edges:
        for bit in (0, 1):
            key = ("edge", edge, bit)
            index[key] = len(vertices)
            vertices.append(key)

    adjacency = np.zeros((len(vertices), len(vertices)), dtype=int)
    for vertex in base_vertices:
        local_edges = incident_edges[vertex]
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
    return adjacency


def cfi_parity_graph_k4(twisted_edge: tuple[int, int] | None = None) -> np.ndarray:
    return cfi_parity_graph_complete(4, twisted_edge=twisted_edge)


def degree_signature(adjacency: np.ndarray) -> tuple[int, ...]:
    return tuple(sorted(int(value) for value in adjacency.sum(axis=1)))


def spectrum_signature(adjacency: np.ndarray, precision: int = 8) -> tuple[float, ...]:
    values = np.linalg.eigvalsh(adjacency.astype(float))
    return tuple(float(round(value, precision)) for value in values)


def triangle_profile(adjacency: np.ndarray) -> tuple[int, ...]:
    a2 = adjacency @ adjacency
    per_vertex = np.diag(a2 @ adjacency) // 2
    return tuple(sorted(int(value) for value in per_vertex))


def wl1_signature(adjacency: np.ndarray, rounds: int = 6) -> tuple[tuple[int, int], ...]:
    n = adjacency.shape[0]
    colors = [int(adjacency[v].sum()) for v in range(n)]
    for _ in range(rounds):
        labels = []
        for vertex in range(n):
            neighborhood = sorted(colors[neighbor] for neighbor in range(n) if adjacency[vertex, neighbor])
            labels.append((colors[vertex], tuple(neighborhood)))
        palette = {label: idx for idx, label in enumerate(sorted(set(labels)))}
        new_colors = [palette[label] for label in labels]
        if new_colors == colors:
            break
        colors = new_colors
    return tuple(sorted((color, colors.count(color)) for color in set(colors)))


def wl2_signature(adjacency: np.ndarray, rounds: int = 3) -> tuple[tuple[int, int], ...]:
    n = adjacency.shape[0]
    colors: dict[tuple[int, int], int] = {}
    for i in range(n):
        for j in range(n):
            if i == j:
                colors[(i, j)] = 0
            elif adjacency[i, j]:
                colors[(i, j)] = 1
            else:
                colors[(i, j)] = 2

    for _ in range(rounds):
        labels = {}
        for i in range(n):
            for j in range(n):
                witness = tuple(sorted((colors[(i, k)], colors[(k, j)]) for k in range(n)))
                labels[(i, j)] = (colors[(i, j)], witness)
        palette = {label: idx for idx, label in enumerate(sorted(set(labels.values())))}
        new_colors = {pair: palette[label] for pair, label in labels.items()}
        if new_colors == colors:
            break
        colors = new_colors

    counts: dict[int, int] = {}
    for color in colors.values():
        counts[color] = counts.get(color, 0) + 1
    return tuple(sorted(counts.items()))


def _tuple_initial_color(adjacency: np.ndarray, item: tuple[int, ...]) -> tuple[int, ...]:
    color = []
    for left in item:
        for right in item:
            if left == right:
                color.append(0)
            elif adjacency[left, right]:
                color.append(1)
            else:
                color.append(2)
    return tuple(color)


def wl_k_signature(adjacency: np.ndarray, k: int = 3, rounds: int = 3) -> tuple[tuple[int, int], ...]:
    """Naive k-WL color refinement signature for small graph pairs."""

    if k < 1:
        raise ValueError("k must be positive")
    n = adjacency.shape[0]
    tuples = [tuple(int(x) for x in item) for item in np.ndindex(*(n for _ in range(k)))]
    colors = {item: _tuple_initial_color(adjacency, item) for item in tuples}
    palette = {label: idx for idx, label in enumerate(sorted(set(colors.values())))}
    color_ids = {item: palette[label] for item, label in colors.items()}

    for _ in range(rounds):
        labels = {}
        for item in tuples:
            neighborhoods = []
            for position in range(k):
                neighborhood = []
                prefix = list(item)
                for replacement in range(n):
                    prefix[position] = replacement
                    neighborhood.append(color_ids[tuple(prefix)])
                neighborhoods.append(tuple(sorted(neighborhood)))
            labels[item] = (color_ids[item], tuple(neighborhoods))
        palette = {label: idx for idx, label in enumerate(sorted(set(labels.values())))}
        new_color_ids = {item: palette[label] for item, label in labels.items()}
        if new_color_ids == color_ids:
            break
        color_ids = new_color_ids

    counts: dict[int, int] = {}
    for color in color_ids.values():
        counts[color] = counts.get(color, 0) + 1
    return tuple(sorted(counts.items()))


def coherent_adjacency_algebra_rank(adjacency: np.ndarray, max_power: int = 5) -> int:
    n = adjacency.shape[0]
    matrices = [np.eye(n), adjacency.astype(float)]
    current = adjacency.astype(float)
    for _ in range(2, max_power + 1):
        current = current @ adjacency
        matrices.append(current.copy())
    flattened = np.vstack([matrix.reshape(1, n * n) for matrix in matrices])
    return int(np.linalg.matrix_rank(flattened, tol=1e-8))


def walk_count_signature(adjacency: np.ndarray, max_length: int = 5) -> tuple[int, ...]:
    current = np.eye(adjacency.shape[0], dtype=int)
    counts = []
    for _ in range(max_length):
        current = current @ adjacency
        counts.append(int(np.trace(current)))
    return tuple(counts)


def _invariant_result(name: str, sig_a: Any, sig_b: Any, solved_name: str) -> InvariantResult:
    distinguishes = sig_a != sig_b
    return InvariantResult(
        name=name,
        distinguishes=distinguishes,
        signature_a=str(sig_a),
        signature_b=str(sig_b),
        interpretation=(
            f"{solved_name} distinguishes the pair; quantum observable would be dequantized."
            if distinguishes
            else f"{solved_name} does not distinguish the pair."
        ),
    )


def _skipped_invariant(name: str, reason: str) -> InvariantResult:
    return InvariantResult(
        name=name,
        distinguishes=False,
        signature_a="skipped",
        signature_b="skipped",
        interpretation=reason,
    )


def classical_invariant_suite(graph_a: np.ndarray, graph_b: np.ndarray, tuple_cap: int = 100_000) -> list[InvariantResult]:
    results = [
        _invariant_result("degree_sequence", degree_signature(graph_a), degree_signature(graph_b), "Degree sequence"),
        _invariant_result("adjacency_spectrum", spectrum_signature(graph_a), spectrum_signature(graph_b), "Adjacency spectrum"),
        _invariant_result("triangle_profile", triangle_profile(graph_a), triangle_profile(graph_b), "Triangle profile"),
        _invariant_result("wl1_color_refinement", wl1_signature(graph_a), wl1_signature(graph_b), "1-WL color refinement"),
        _invariant_result("wl2_pair_refinement", wl2_signature(graph_a), wl2_signature(graph_b), "2-WL pair refinement"),
    ]
    tuple_count = int(graph_a.shape[0] ** 3)
    if tuple_count <= tuple_cap:
        results.append(
            _invariant_result(
                "wl3_tuple_refinement",
                wl_k_signature(graph_a, k=3),
                wl_k_signature(graph_b, k=3),
                "3-WL tuple refinement",
            )
        )
    else:
        results.append(
            _skipped_invariant(
                "wl3_tuple_refinement",
                f"3-WL skipped because {tuple_count} tuples exceeds cap {tuple_cap}; this is a classical scaling blocker.",
            )
        )
    return results


def wl_scaling_suite(
    graph_a: np.ndarray,
    graph_b: np.ndarray,
    max_k: int = 4,
    rounds: int = 3,
    tuple_cap: int = 100_000,
) -> list[WLScalingResult]:
    results: list[WLScalingResult] = []
    n = int(graph_a.shape[0])
    for k in range(1, max_k + 1):
        tuple_count = int(n**k)
        if tuple_count > tuple_cap:
            results.append(
                WLScalingResult(
                    k=k,
                    rounds=rounds,
                    tuple_count=tuple_count,
                    evaluated=False,
                    distinguishes=False,
                    signature_a="skipped",
                    signature_b="skipped",
                    interpretation=(
                        f"{k}-WL skipped because {tuple_count} tuples exceeds cap {tuple_cap}; "
                        "this is a scaling blocker for brute-force classical refinement."
                    ),
                )
            )
            continue
        if k == 1:
            sig_a = wl1_signature(graph_a, rounds=rounds)
            sig_b = wl1_signature(graph_b, rounds=rounds)
        elif k == 2:
            sig_a = wl2_signature(graph_a, rounds=rounds)
            sig_b = wl2_signature(graph_b, rounds=rounds)
        else:
            sig_a = wl_k_signature(graph_a, k=k, rounds=rounds)
            sig_b = wl_k_signature(graph_b, k=k, rounds=rounds)
        distinguishes = sig_a != sig_b
        results.append(
            WLScalingResult(
                k=k,
                rounds=rounds,
                tuple_count=tuple_count,
                evaluated=True,
                distinguishes=distinguishes,
                signature_a=str(sig_a[:12] if isinstance(sig_a, tuple) else sig_a),
                signature_b=str(sig_b[:12] if isinstance(sig_b, tuple) else sig_b),
                interpretation=(
                    f"{k}-WL distinguishes the pair; corresponding low-register relation signal is classically dequantized."
                    if distinguishes
                    else f"{k}-WL does not distinguish the pair at {rounds} refinement round(s)."
                ),
            )
        )
    return results


def exact_isomorphism_check(
    graph_a: np.ndarray,
    graph_b: np.ndarray,
    expected_nonisomorphic: bool,
    max_vertices: int = 40,
) -> ExactIsomorphismCheck:
    if int(graph_a.shape[0]) > max_vertices:
        return ExactIsomorphismCheck(
            name="networkx_exact_isomorphism",
            evaluated=False,
            isomorphic=None,
            supports_known_status=False,
            cost_model=f"Skipped: vertex count {graph_a.shape[0]} exceeds exact-check cap {max_vertices}.",
            interpretation="Known CFI parity status is construction-derived; exact GI sanity is skipped at this scale.",
        )
    try:
        import networkx as nx  # type: ignore
    except Exception:
        return ExactIsomorphismCheck(
            name="networkx_exact_isomorphism",
            evaluated=False,
            isomorphic=None,
            supports_known_status=False,
            cost_model="Skipped: networkx is not available.",
            interpretation="Exact sanity check skipped; keep known-status claims tied to construction/literature.",
        )
    graph_left = nx.from_numpy_array(graph_a)
    graph_right = nx.from_numpy_array(graph_b)
    isomorphic = bool(nx.is_isomorphic(graph_left, graph_right))
    supports = (not isomorphic) if expected_nonisomorphic else isomorphic
    return ExactIsomorphismCheck(
        name="networkx_exact_isomorphism",
        evaluated=True,
        isomorphic=isomorphic,
        supports_known_status=supports,
        cost_model="Exact backtracking GI sanity check; not treated as a scalable low-complexity invariant.",
        interpretation=(
            "Exact GI sanity check confirms the pair is non-isomorphic."
            if expected_nonisomorphic and not isomorphic
            else "Exact GI sanity check does not support the expected status; inspect the generator."
            if not supports
            else "Exact GI sanity check supports the expected isomorphic status."
        ),
    )


def relation_observable_suite(graph_a: np.ndarray, graph_b: np.ndarray, tuple_cap: int = 100_000) -> list[RelationObservableResult]:
    rank_a = coherent_adjacency_algebra_rank(graph_a)
    rank_b = coherent_adjacency_algebra_rank(graph_b)
    walks_a = walk_count_signature(graph_a)
    walks_b = walk_count_signature(graph_b)
    results = [
        RelationObservableResult(
            name="adjacency_algebra_rank",
            distinguishes=rank_a != rank_b,
            value_a=str(rank_a),
            value_b=str(rank_b),
            interpretation=(
                "Low-register relation algebra rank separates the pair."
                if rank_a != rank_b
                else "Adjacency algebra rank matches; this low-register observable gives no separation."
            ),
        ),
        RelationObservableResult(
            name="closed_walk_counts",
            distinguishes=walks_a != walks_b,
            value_a=str(walks_a),
            value_b=str(walks_b),
            interpretation=(
                "Closed-walk counts separate the pair and likely dequantize this observable."
                if walks_a != walks_b
                else "Closed-walk counts match; spectral walk observables give no separation."
            ),
        ),
    ]
    tuple_count = int(graph_a.shape[0] ** 3)
    if tuple_count <= tuple_cap:
        wl3_a = wl_k_signature(graph_a, k=3)
        wl3_b = wl_k_signature(graph_b, k=3)
        results.append(
            RelationObservableResult(
                name="three_register_tuple_relation_colors",
                distinguishes=wl3_a != wl3_b,
                value_a=str(wl3_a[:8]),
                value_b=str(wl3_b[:8]),
                interpretation=(
                    "A 3-register tuple relation separates the pair, but this is mirrored by classical 3-WL."
                    if wl3_a != wl3_b
                    else "3-register tuple relation colors match; this observable gives no separation."
                ),
            )
        )
    else:
        results.append(
            RelationObservableResult(
                name="three_register_tuple_relation_colors",
                distinguishes=False,
                value_a="skipped",
                value_b="skipped",
                interpretation=(
                    f"3-register tuple relation skipped because {tuple_count} tuples exceeds cap {tuple_cap}; "
                    "larger CFI instances need tensor/implicit observables rather than brute-force relation tables."
                ),
            )
        )
    return results


def audit_graph_pair(pair_id: str) -> CosetPairAudit:
    if pair_id == "shrikhande-vs-rook":
        graph_a = shrikhande_graph()
        graph_b = rook_graph_4x4()
        spec = GraphPairSpec(
            id=pair_id,
            graph_a="Shrikhande graph",
            graph_b="4x4 rook graph",
            vertex_count=16,
            known_nonisomorphic=True,
            reason="Standard non-isomorphic strongly regular pair with identical parameters (16,6,2,2).",
        )
    elif pair_id == "cycle-vs-chorded-cycle":
        graph_a = cycle_graph(16)
        graph_b = chorded_cycle_graph(16)
        spec = GraphPairSpec(
            id=pair_id,
            graph_a="Cycle graph C16",
            graph_b="C16 with distance-2 chords",
            vertex_count=16,
            known_nonisomorphic=True,
            reason="Control pair that classical invariants should distinguish immediately.",
        )
    elif pair_id == "cfi-k4-parity-twist" or (
        pair_id.startswith("cfi-k") and pair_id.endswith("-parity-twist")
    ):
        if pair_id == "cfi-k4-parity-twist":
            base_size = 4
        else:
            base_token = pair_id.split("-")[1]
            base_size = int(base_token[1:])
        graph_a = cfi_parity_graph_complete(base_size, twisted_edge=None)
        graph_b = cfi_parity_graph_complete(base_size, twisted_edge=(0, 1))
        spec = GraphPairSpec(
            id=pair_id,
            graph_a=f"Untwisted CFI-style parity graph over K{base_size}",
            graph_b=f"Single-edge twisted CFI-style parity graph over K{base_size}",
            vertex_count=int(graph_a.shape[0]),
            known_nonisomorphic=True,
            reason=(
                "Compact Cai-Furer-Immerman-style parity obstruction: exact GI detects non-isomorphism, "
                "but low-dimensional WL and spectral invariants are designed to fail."
            ),
        )
    else:
        raise ValueError(f"unknown graph pair: {pair_id}")

    invariants = classical_invariant_suite(graph_a, graph_b)
    observables = relation_observable_suite(graph_a, graph_b)
    wl_scaling = wl_scaling_suite(graph_a, graph_b)
    exact_check = exact_isomorphism_check(graph_a, graph_b, expected_nonisomorphic=spec.known_nonisomorphic)
    falsifiers = []
    if any(item.distinguishes for item in invariants):
        falsifiers.append("A classical graph invariant distinguishes the pair; any matching quantum observable is dequantized.")
    if any(item.distinguishes for item in observables):
        falsifiers.append("A low-register relation observable separates the pair but may reduce to a classical invariant.")
    if any(item.evaluated and item.distinguishes for item in wl_scaling):
        falsifiers.append("A higher-k WL baseline separates the pair; low-register tensor signals must exceed this classical refinement.")
    if exact_check.evaluated and not exact_check.supports_known_status:
        falsifiers.append("Exact isomorphism sanity check contradicts the pair metadata; generator or assumptions are invalid.")

    cheap_distinguishes = any(item.distinguishes for item in invariants + observables) or any(
        item.evaluated and item.distinguishes for item in wl_scaling
    )
    if spec.known_nonisomorphic and not cheap_distinguishes:
        positive = "boundary instance: known non-isomorphic pair survives current classical and low-register relation tests"
    elif any(item.distinguishes for item in invariants):
        positive = "control: classical baseline distinguishes this pair"
    elif any(item.evaluated and item.distinguishes for item in wl_scaling):
        positive = "partial: higher-k WL baseline distinguishes this pair before any quantum observable is needed"
    else:
        positive = "partial: relation observable separates but needs dequantization audit"

    return CosetPairAudit(spec, invariants, observables, wl_scaling, exact_check, positive, falsifiers)


def run_coset_workbench(pair_ids: list[str] | None = None) -> CosetWorkbenchResult:
    active_pairs = pair_ids or ["shrikhande-vs-rook", "cfi-k4-parity-twist", "cfi-k5-parity-twist", "cycle-vs-chorded-cycle"]
    audits = [audit_graph_pair(pair_id) for pair_id in active_pairs]
    falsifiers = sorted({item for audit in audits for item in audit.falsifiers_triggered})
    boundary_count = sum(1 for audit in audits if audit.positive_signal.startswith("boundary"))
    classical_solved_count = sum(1 for audit in audits if "classical baseline" in audit.positive_signal)
    cfi_count = sum(1 for audit in audits if audit.pair.id.startswith("cfi-"))
    summary = (
        f"Audited {len(audits)} hidden-permutation graph pairs. "
        f"{boundary_count} pair survives current classical and low-register tests; "
        f"{classical_solved_count} control pair is classically distinguished; "
        f"{cfi_count} CFI-style parity benchmark(s) included."
    )
    return CosetWorkbenchResult(utc_now(), audits, summary, falsifiers)


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


def write_coset_negative_results(result: CosetWorkbenchResult) -> int:
    written = 0
    for audit in result.pair_audits:
        distinguishing_invariants = [item.name for item in audit.classical_invariants if item.distinguishes]
        if not distinguishing_invariants:
            continue
        upsert_negative_result(
            NegativeResultRecord(
                id=f"COSET-DEQUANTIZED-{audit.pair.id.upper().replace('-', '_')}",
                source="coset_state_workbench.py",
                claim=f"{audit.pair.id} relation observable provides nonclassical coset-state evidence.",
                reason_invalid=(
                    "Classical graph invariant(s) distinguish the pair: "
                    + ", ".join(distinguishing_invariants)
                ),
                lesson="Do not count a coset-state observable as quantum evidence if WL, spectrum, walk counts, or related invariants already separate the instances.",
                applies_to=["CODE-COSET-COLLECTIVE", "HYP-LIT-COSET-OBSERVABLES", "PO-DEQUANTIZATION", "PO-FALSIFIERS"],
                evidence={
                    "pair_id": audit.pair.id,
                    "distinguishing_invariants": distinguishing_invariants,
                    "distinguishing_observables": [item.name for item in audit.relation_observables if item.distinguishes],
                },
            )
        )
        written += 1
    return written


def write_coset_workbench(
    output_path: Path = COSET_AUDIT_PATH,
    pair_ids: list[str] | None = None,
    write_registry: bool = True,
    registry_experiment_id: str = "EXP-CODE-COSET-RANK",
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "RESULT-COSET-WORKBENCH-LATEST",
) -> dict[str, Any]:
    result = run_coset_workbench(pair_ids=pair_ids)
    payload = _json_ready(result)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    if write_registry:
        negative_results_written = write_coset_negative_results(result)
        metrics = {
            "pair_audit_count": len(result.pair_audits),
            "boundary_pair_count": sum(1 for audit in result.pair_audits if audit.positive_signal.startswith("boundary")),
            "classically_distinguished_pair_count": sum(
                1 for audit in result.pair_audits if any(item.distinguishes for item in audit.classical_invariants)
            ),
            "wl3_distinguishes_count": sum(
                1
                for audit in result.pair_audits
                if any(item.name == "wl3_tuple_refinement" and item.distinguishes for item in audit.classical_invariants)
            ),
            "max_evaluated_wl_k": max(
                (
                    max((item.k for item in audit.wl_scaling if item.evaluated), default=0)
                    for audit in result.pair_audits
                ),
                default=0,
            ),
            "higher_wl_distinguishes_count": sum(
                1 for audit in result.pair_audits if any(item.evaluated and item.distinguishes for item in audit.wl_scaling)
            ),
            "cfi_style_pair_count": sum(1 for audit in result.pair_audits if audit.pair.id.startswith("cfi-")),
            "scalable_cfi_pair_count": sum(1 for audit in result.pair_audits if audit.pair.id.startswith("cfi-k") and audit.pair.vertex_count > 28),
            "max_vertex_count": max((audit.pair.vertex_count for audit in result.pair_audits), default=0),
            "skipped_wl_scaling_count": sum(
                1 for audit in result.pair_audits for item in audit.wl_scaling if not item.evaluated
            ),
            "exact_nonisomorphism_certificate_count": sum(
                1
                for audit in result.pair_audits
                if audit.exact_isomorphism_check.evaluated and audit.exact_isomorphism_check.supports_known_status
            ),
            "low_register_observable_distinguishes_count": sum(
                1 for audit in result.pair_audits if any(item.distinguishes for item in audit.relation_observables)
            ),
            "negative_results_written": negative_results_written,
        }
        upsert_experiment_result(
            ExperimentResultRecord(
                id=registry_result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=result.created_at,
                status="needs-collective-observable" if metrics["boundary_pair_count"] else "dequantized-by-classical-baseline",
                summary=result.summary,
                metrics=metrics,
                falsifiers_triggered=result.falsifiers_triggered,
                artifacts={"coset_audit": str(output_path)},
            )
        )
    return payload
