"""Bipartition-based structural decoder for broader promised CFI gadgets.

The regular and degree-separated decoders leave an obvious loophole: choose a
base graph where middle-vertex degrees collide with edge-copy degrees.  CFI
parity graphs are still bipartite under the explicit gadget promise.  This
baseline uses the bipartition, reconstructs edge-copy twin pairs, rebuilds
vertex gadgets, and decodes global twist parity without relying on degree-class
separation.
"""

from __future__ import annotations

import json
from collections import deque
from dataclasses import asdict, dataclass, is_dataclass
from pathlib import Path
from typing import Any

import numpy as np

from cfi_base_family_search import base_edges, base_graph_by_id, cfi_parity_graph_from_base
from cfi_irregular_structural_decoder import irregular_base_graph_by_id, permute_adjacency
from research_registry import ExperimentResultRecord, NegativeResultRecord, upsert_experiment_result, upsert_negative_result, utc_now


COSET_WORKBENCH_DIR = Path("research/coset_workbench")
CFI_BIPARTITE_STRUCTURAL_DECODER_PATH = COSET_WORKBENCH_DIR / "cfi_bipartite_structural_decoder.json"
DEFAULT_BIPARTITE_CFI_BASE_IDS = [
    "complete-k4",
    "mobius-ladder-8",
    "complete-bipartite-3-5",
    "prism-degree4-hub",
]


@dataclass(frozen=True)
class BipartiteCFIBaseSpec:
    id: str
    description: str
    vertex_count: int
    edge_count: int
    degree_sequence: list[int]
    twist_edge: tuple[int, int]
    degree_separated: bool
    construction_note: str


@dataclass(frozen=True)
class BipartiteCFIStructuralDecode:
    success: bool
    status: str
    vertex_count: int
    selected_middle_side: int | None
    bipartition_sizes: tuple[int, int] | None
    middle_vertex_count: int
    edge_copy_vertex_count: int
    edge_pair_count: int
    vertex_gadget_count: int
    inferred_base_degree_sequence: list[int]
    local_parities: list[int]
    global_twist_parity: int | None
    ambiguity: str
    interpretation: str


@dataclass(frozen=True)
class BipartiteCFIStructuralDecoderRecord:
    base: BipartiteCFIBaseSpec
    cfi_vertex_count: int
    shuffled: bool
    untwisted_decode: BipartiteCFIStructuralDecode
    twisted_decode: BipartiteCFIStructuralDecode
    recovers_global_twist: bool
    legal_access_model: str
    status: str
    interpretation: str


@dataclass(frozen=True)
class BipartiteCFIStructuralDecoderReport:
    created_at: str
    base_ids: list[str]
    records: list[BipartiteCFIStructuralDecoderRecord]
    headline_metrics: dict[str, int]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def base_graph_prism_degree4_hub() -> np.ndarray:
    description, prism = base_graph_by_id("triangular-prism")
    _ = description
    adjacency = np.zeros((7, 7), dtype=int)
    adjacency[:6, :6] = prism
    for vertex in (0, 1, 3, 4):
        adjacency[6, vertex] = adjacency[vertex, 6] = 1
    return adjacency


def mixed_cfi_base_graph_by_id(base_id: str) -> tuple[str, np.ndarray]:
    if base_id == "prism-degree4-hub":
        return (
            "Triangular prism plus degree-4 hub; middle degree 4 collides with 3-3 edge-copy degree",
            base_graph_prism_degree4_hub(),
        )
    try:
        return base_graph_by_id(base_id)
    except ValueError:
        return irregular_base_graph_by_id(base_id)


def _degree_separated(base: np.ndarray) -> bool:
    base_degrees = [int(value) for value in base.sum(axis=1).tolist()]
    middle_degrees = set(base_degrees)
    edge_copy_degrees = {
        (1 << (base_degrees[left] - 2)) + (1 << (base_degrees[right] - 2))
        for left, right in base_edges(base)
    }
    return middle_degrees.isdisjoint(edge_copy_degrees)


def _failure_decode(
    status: str,
    adjacency: np.ndarray,
    ambiguity: str,
    bipartition_sizes: tuple[int, int] | None = None,
) -> BipartiteCFIStructuralDecode:
    return BipartiteCFIStructuralDecode(
        success=False,
        status=status,
        vertex_count=int(adjacency.shape[0]),
        selected_middle_side=None,
        bipartition_sizes=bipartition_sizes,
        middle_vertex_count=0,
        edge_copy_vertex_count=0,
        edge_pair_count=0,
        vertex_gadget_count=0,
        inferred_base_degree_sequence=[],
        local_parities=[],
        global_twist_parity=None,
        ambiguity=ambiguity,
        interpretation=ambiguity,
    )


def bipartition_vertices(adjacency: np.ndarray) -> tuple[bool, tuple[list[int], list[int]]]:
    matrix = np.asarray(adjacency, dtype=np.uint8)
    n = int(matrix.shape[0])
    colors = [-1] * n
    for start in range(n):
        if colors[start] != -1:
            continue
        colors[start] = 0
        queue: deque[int] = deque([start])
        while queue:
            vertex = queue.popleft()
            for neighbor in np.flatnonzero(matrix[vertex]):
                neighbor = int(neighbor)
                if colors[neighbor] == -1:
                    colors[neighbor] = 1 - colors[vertex]
                    queue.append(neighbor)
                elif colors[neighbor] == colors[vertex]:
                    return False, ([], [])
    return True, ([idx for idx, color in enumerate(colors) if color == 0], [idx for idx, color in enumerate(colors) if color == 1])


def _decode_with_middle_set(
    matrix: np.ndarray,
    middle_vertices: list[int],
    selected_side: int,
    bipartition_sizes: tuple[int, int],
) -> BipartiteCFIStructuralDecode:
    middle_set = set(middle_vertices)
    edge_copy_vertices = [idx for idx in range(matrix.shape[0]) if idx not in middle_set]
    if len(edge_copy_vertices) % 2:
        return _failure_decode(
            "odd-edge-copy-side",
            matrix,
            "Selected edge-copy side has odd size.",
            bipartition_sizes,
        )

    middle_neighbors = {
        vertex: set(int(item) for item in np.flatnonzero(matrix[vertex]) if int(item) in middle_set)
        for vertex in edge_copy_vertices
    }
    signatures: dict[int, tuple[int, ...]] = {}
    for vertex in edge_copy_vertices:
        sharing = [
            other
            for other in edge_copy_vertices
            if other != vertex and middle_neighbors[vertex].intersection(middle_neighbors[other])
        ]
        signatures[vertex] = tuple(sorted(sharing))

    signature_groups: dict[tuple[int, ...], list[int]] = {}
    for vertex, signature in signatures.items():
        signature_groups.setdefault(signature, []).append(vertex)
    group_sizes = sorted(len(group) for group in signature_groups.values())
    if any(size != 2 for size in group_sizes):
        return _failure_decode(
            "ambiguous-edge-copy-pairing",
            matrix,
            f"Edge-copy twin signatures are not canonical size-two pairs. Observed group sizes: {group_sizes[:12]}.",
            bipartition_sizes,
        )

    pair_id: dict[int, int] = {}
    pair_bit: dict[int, int] = {}
    for idx, group in enumerate(sorted(tuple(sorted(group)) for group in signature_groups.values())):
        for bit, vertex in enumerate(group):
            pair_id[vertex] = idx
            pair_bit[vertex] = bit

    gadget_bits: dict[tuple[int, ...], list[tuple[int, ...]]] = {}
    for middle in middle_vertices:
        incident_copies = [int(item) for item in np.flatnonzero(matrix[middle]) if int(item) in pair_id]
        key = tuple(sorted(pair_id[item] for item in incident_copies))
        bits = tuple(pair_bit[item] for item in sorted(incident_copies, key=lambda item: pair_id[item]))
        if len(key) < 3 or len(key) != len(set(key)):
            return _failure_decode(
                "invalid-middle-gadget-incidence",
                matrix,
                "A selected middle vertex is not incident to one copy from each local base edge.",
                bipartition_sizes,
            )
        gadget_bits.setdefault(key, []).append(bits)

    inferred_degrees = sorted(len(key) for key in gadget_bits)
    if sum(inferred_degrees) != 2 * len(signature_groups):
        return _failure_decode(
            "invalid-base-handshaking",
            matrix,
            "Recovered vertex gadgets do not satisfy the base-graph handshaking relation.",
            bipartition_sizes,
        )

    local_parities: list[int] = []
    for key, assignments in sorted(gadget_bits.items()):
        local_degree = len(key)
        expected_size = 1 << (local_degree - 1)
        parities = {sum(bits) % 2 for bits in assignments}
        if len(assignments) != expected_size or len(parities) != 1:
            return _failure_decode(
                "invalid-vertex-gadget-parity-profile",
                matrix,
                "A reconstructed vertex gadget lacks the expected assignment count with uniform local parity.",
                bipartition_sizes,
            )
        local_parities.append(next(iter(parities)))

    global_parity = sum(local_parities) % 2
    return BipartiteCFIStructuralDecode(
        success=True,
        status="decoded-bipartite-global-twist-parity",
        vertex_count=int(matrix.shape[0]),
        selected_middle_side=selected_side,
        bipartition_sizes=bipartition_sizes,
        middle_vertex_count=len(middle_vertices),
        edge_copy_vertex_count=len(edge_copy_vertices),
        edge_pair_count=len(signature_groups),
        vertex_gadget_count=len(gadget_bits),
        inferred_base_degree_sequence=inferred_degrees,
        local_parities=local_parities,
        global_twist_parity=global_parity,
        ambiguity="none",
        interpretation=(
            "Recovered CFI global twist parity from the bipartition, edge-copy twin signatures, "
            "and vertex-gadget parity profiles without assuming degree separation."
        ),
    )


def decode_bipartite_cfi_twist_parity(adjacency: np.ndarray) -> BipartiteCFIStructuralDecode:
    matrix = np.asarray(adjacency, dtype=np.uint8)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        return _failure_decode("not-square-adjacency", matrix, "Adjacency matrix must be square.")
    is_bipartite, sides = bipartition_vertices(matrix)
    if not is_bipartite:
        return _failure_decode("not-bipartite", matrix, "CFI parity gadget graph should be bipartite.")

    bipartition_sizes = (len(sides[0]), len(sides[1]))
    attempts = [
        _decode_with_middle_set(matrix, sides[0], 0, bipartition_sizes),
        _decode_with_middle_set(matrix, sides[1], 1, bipartition_sizes),
    ]
    successes = [attempt for attempt in attempts if attempt.success]
    if len(successes) == 1:
        return successes[0]
    if len(successes) > 1:
        return _failure_decode(
            "ambiguous-bipartite-side-choice",
            matrix,
            "Both bipartition sides satisfy the current CFI gadget decoder; require an additional side-selection certificate.",
            bipartition_sizes,
        )
    return _failure_decode(
        "bipartite-cfi-decoder-failed",
        matrix,
        "; ".join(f"{attempt.status}: {attempt.ambiguity}" for attempt in attempts),
        bipartition_sizes,
    )


def audit_bipartite_cfi_structural_decoder_record(
    base_id: str,
    shuffle: bool = True,
    seed: int = 17011,
) -> BipartiteCFIStructuralDecoderRecord:
    description, base = mixed_cfi_base_graph_by_id(base_id)
    edge = base_edges(base)[0]
    untwisted = cfi_parity_graph_from_base(base, twisted_edge=None)
    twisted = cfi_parity_graph_from_base(base, twisted_edge=edge)
    if shuffle:
        untwisted = permute_adjacency(untwisted, seed + 17 * len(base_id))
        twisted = permute_adjacency(twisted, seed + 101 + 17 * len(base_id))

    untwisted_decode = decode_bipartite_cfi_twist_parity(untwisted)
    twisted_decode = decode_bipartite_cfi_twist_parity(twisted)
    recovers = (
        untwisted_decode.success
        and twisted_decode.success
        and untwisted_decode.global_twist_parity == 0
        and twisted_decode.global_twist_parity == 1
    )
    if recovers:
        status = "dequantized-by-bipartite-structural-cfi-decoder"
        interpretation = (
            f"CFI base {base_id} has global twist parity classically recovered from bipartition and gadget structure "
            "under the explicit CFI-gadget promise."
        )
    else:
        status = "bipartite-structural-decoder-proof-debt"
        interpretation = (
            f"CFI base {base_id} was not decoded by the bipartite structural baseline; keep it as proof debt, not evidence."
        )

    degrees = [int(value) for value in base.sum(axis=1).tolist()]
    spec = BipartiteCFIBaseSpec(
        id=base_id,
        description=description,
        vertex_count=int(base.shape[0]),
        edge_count=len(base_edges(base)),
        degree_sequence=sorted(degrees),
        twist_edge=edge,
        degree_separated=_degree_separated(base),
        construction_note="Single-edge twist in a CFI parity gadget audited through bipartition reconstruction.",
    )
    return BipartiteCFIStructuralDecoderRecord(
        base=spec,
        cfi_vertex_count=int(untwisted.shape[0]),
        shuffled=shuffle,
        untwisted_decode=untwisted_decode,
        twisted_decode=twisted_decode,
        recovers_global_twist=recovers,
        legal_access_model="unlabeled adjacency matrix with explicit CFI gadget-family promise",
        status=status,
        interpretation=interpretation,
    )


def run_bipartite_cfi_structural_decoder(
    base_ids: list[str] | None = None,
    shuffle: bool = True,
    seed: int = 17011,
) -> BipartiteCFIStructuralDecoderReport:
    active = base_ids or DEFAULT_BIPARTITE_CFI_BASE_IDS
    records = [audit_bipartite_cfi_structural_decoder_record(base_id, shuffle=shuffle, seed=seed) for base_id in active]
    metrics = {
        "base_count": len(records),
        "decoded_count": sum(1 for record in records if record.untwisted_decode.success and record.twisted_decode.success),
        "dequantized_count": sum(1 for record in records if record.status == "dequantized-by-bipartite-structural-cfi-decoder"),
        "proof_debt_count": sum(1 for record in records if record.status == "bipartite-structural-decoder-proof-debt"),
        "non_degree_separated_count": sum(1 for record in records if not record.base.degree_separated),
        "max_vertex_count": max((record.cfi_vertex_count for record in records), default=0),
    }
    if metrics["dequantized_count"]:
        status = "cfi-family-dequantized-under-bipartite-gadget-promise"
    elif metrics["proof_debt_count"]:
        status = "bipartite-cfi-structural-decoder-proof-debt"
    else:
        status = "bipartite-cfi-structural-decoder-incomplete"
    summary = (
        f"Ran bipartition-based CFI structural decoding on {metrics['base_count']} row(s). "
        f"{metrics['dequantized_count']} row(s) were dequantized under the gadget promise; "
        f"{metrics['proof_debt_count']} remain proof debt."
    )
    falsifiers = []
    if metrics["dequantized_count"]:
        falsifiers.append("Bipartition-visible CFI gadget structure classically reveals global twist parity.")
    if metrics["proof_debt_count"]:
        falsifiers.append("Rows not decoded by this baseline remain proof debt, not positive evidence.")
    return BipartiteCFIStructuralDecoderReport(utc_now(), active, records, metrics, status, summary, falsifiers)


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


def write_bipartite_cfi_structural_decoder_negative_results(report: BipartiteCFIStructuralDecoderReport) -> int:
    written = 0
    for record in report.records:
        if record.status != "dequantized-by-bipartite-structural-cfi-decoder":
            continue
        upsert_negative_result(
            NegativeResultRecord(
                id=f"CFI-BIPARTITE-STRUCTURAL-DECODER-DEQUANTIZED-{_safe_id(record.base.id)}",
                source="cfi_bipartite_structural_decoder.py",
                claim=f"CFI base {record.base.id} supplies nonclassical coset-state evidence under the CFI gadget promise.",
                reason_invalid=record.interpretation,
                lesson=(
                    "If the CFI gadget promise exposes a bipartite middle/edge-copy structure, irregular degree collisions "
                    "do not suffice: the global twist parity is still structurally recoverable."
                ),
                applies_to=["CODE-COSET-COLLECTIVE", "PO-DEQUANTIZATION", "PO-MEASUREMENT"],
                evidence=asdict(record),
            )
        )
        written += 1
    return written


def write_bipartite_cfi_structural_decoder_report(
    output_path: Path = CFI_BIPARTITE_STRUCTURAL_DECODER_PATH,
    base_ids: list[str] | None = None,
    shuffle: bool = True,
    seed: int = 17011,
    write_registry: bool = True,
    registry_experiment_id: str = "EXP-COSET-CFI-BIPARTITE-STRUCTURAL-DECODER",
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "RESULT-COSET-CFI-BIPARTITE-STRUCTURAL-DECODER-LATEST",
) -> dict[str, Any]:
    report = run_bipartite_cfi_structural_decoder(base_ids=base_ids, shuffle=shuffle, seed=seed)
    payload = _json_ready(report)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    if write_registry:
        negative_results_written = write_bipartite_cfi_structural_decoder_negative_results(report)
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
                artifacts={"cfi_bipartite_structural_decoder": str(output_path)},
            )
        )
    return payload
