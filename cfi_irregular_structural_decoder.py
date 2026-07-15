"""Structural CFI decoder for degree-separated irregular promised gadgets.

Regular CFI rows were already dequantized by ``cfi_structural_decoder.py``.
This module tests the next obvious escape attempt: use irregular base graphs so
the regular degree-class decoder no longer applies.  For degree-separated CFI
gadgets, the unlabeled adjacency matrix still reveals the middle vertices,
edge-copy twin pairs, vertex gadgets, and global twist parity.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, is_dataclass
from pathlib import Path
from typing import Any

import numpy as np

from cfi_base_family_search import base_edges, cfi_parity_graph_from_base
from research_registry import ExperimentResultRecord, NegativeResultRecord, upsert_experiment_result, upsert_negative_result, utc_now


COSET_WORKBENCH_DIR = Path("research/coset_workbench")
CFI_IRREGULAR_STRUCTURAL_DECODER_PATH = COSET_WORKBENCH_DIR / "cfi_irregular_structural_decoder.json"
DEFAULT_IRREGULAR_CFI_BASE_IDS = [
    "complete-bipartite-3-5",
    "complete-bipartite-4-5",
    "complete-tripartite-2-3-4",
]


@dataclass(frozen=True)
class IrregularCFIBaseSpec:
    id: str
    description: str
    vertex_count: int
    edge_count: int
    degree_sequence: list[int]
    twist_edge: tuple[int, int]
    construction_note: str


@dataclass(frozen=True)
class IrregularCFIStructuralDecode:
    success: bool
    status: str
    vertex_count: int
    inferred_middle_degrees: list[int]
    inferred_middle_degree_counts: dict[int, int]
    inferred_base_vertex_count: int | None
    middle_vertex_count: int
    edge_copy_vertex_count: int
    edge_pair_count: int
    vertex_gadget_count: int
    local_parities: list[int]
    global_twist_parity: int | None
    ambiguity: str
    interpretation: str


@dataclass(frozen=True)
class IrregularCFIStructuralDecoderRecord:
    base: IrregularCFIBaseSpec
    cfi_vertex_count: int
    shuffled: bool
    degree_separated: bool
    untwisted_decode: IrregularCFIStructuralDecode
    twisted_decode: IrregularCFIStructuralDecode
    recovers_global_twist: bool
    legal_access_model: str
    status: str
    interpretation: str


@dataclass(frozen=True)
class IrregularCFIStructuralDecoderReport:
    created_at: str
    base_ids: list[str]
    records: list[IrregularCFIStructuralDecoderRecord]
    headline_metrics: dict[str, int]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def base_graph_complete_bipartite(left_count: int, right_count: int) -> np.ndarray:
    adjacency = np.zeros((left_count + right_count, left_count + right_count), dtype=int)
    for left in range(left_count):
        for right in range(left_count, left_count + right_count):
            adjacency[left, right] = adjacency[right, left] = 1
    return adjacency


def base_graph_complete_tripartite(parts: tuple[int, int, int]) -> np.ndarray:
    offsets = [0, parts[0], parts[0] + parts[1]]
    n = sum(parts)
    adjacency = np.zeros((n, n), dtype=int)
    ranges = [range(offsets[idx], offsets[idx] + parts[idx]) for idx in range(3)]
    for group_a in range(3):
        for group_b in range(group_a + 1, 3):
            for left in ranges[group_a]:
                for right in ranges[group_b]:
                    adjacency[left, right] = adjacency[right, left] = 1
    return adjacency


def irregular_base_graph_by_id(base_id: str) -> tuple[str, np.ndarray]:
    if base_id == "complete-bipartite-3-5":
        return "Degree-separated complete bipartite K3,5 base", base_graph_complete_bipartite(3, 5)
    if base_id == "complete-bipartite-4-5":
        return "Degree-separated complete bipartite K4,5 base", base_graph_complete_bipartite(4, 5)
    if base_id == "complete-tripartite-2-3-4":
        return "Degree-separated complete tripartite K2,3,4 base", base_graph_complete_tripartite((2, 3, 4))
    raise ValueError(f"unknown irregular CFI base id: {base_id}")


def permute_adjacency(adjacency: np.ndarray, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    permutation = rng.permutation(adjacency.shape[0])
    return adjacency[permutation][:, permutation]


def _failure_decode(
    status: str,
    adjacency: np.ndarray,
    ambiguity: str,
    inferred_middle_degrees: list[int] | None = None,
    inferred_middle_degree_counts: dict[int, int] | None = None,
    inferred_base_vertex_count: int | None = None,
    middle_vertex_count: int = 0,
    edge_copy_vertex_count: int = 0,
    edge_pair_count: int = 0,
    vertex_gadget_count: int = 0,
) -> IrregularCFIStructuralDecode:
    return IrregularCFIStructuralDecode(
        success=False,
        status=status,
        vertex_count=int(adjacency.shape[0]),
        inferred_middle_degrees=inferred_middle_degrees or [],
        inferred_middle_degree_counts=inferred_middle_degree_counts or {},
        inferred_base_vertex_count=inferred_base_vertex_count,
        middle_vertex_count=middle_vertex_count,
        edge_copy_vertex_count=edge_copy_vertex_count,
        edge_pair_count=edge_pair_count,
        vertex_gadget_count=vertex_gadget_count,
        local_parities=[],
        global_twist_parity=None,
        ambiguity=ambiguity,
        interpretation=ambiguity,
    )


def _degree_counts(matrix: np.ndarray) -> dict[int, int]:
    degrees = matrix.sum(axis=1).astype(int).tolist()
    counts: dict[int, int] = {}
    for degree in degrees:
        counts[int(degree)] = counts.get(int(degree), 0) + 1
    return counts


def infer_degree_separated_middle_vertices(matrix: np.ndarray, max_middle_degree: int = 12) -> tuple[list[int], dict[int, int]]:
    """Infer CFI middle vertices from degree divisibility in separated rows.

    A base vertex of degree d contributes 2^(d-1) middle vertices, all of graph
    degree d.  The irregular stress families here are designed so edge-copy
    degrees do not collide with those middle degrees.
    """

    degrees = matrix.sum(axis=1).astype(int).tolist()
    counts = _degree_counts(matrix)
    middle_degrees = {
        degree
        for degree, count in counts.items()
        if 3 <= degree <= max_middle_degree and count % (1 << (degree - 1)) == 0
    }
    middle_vertices = [idx for idx, degree in enumerate(degrees) if int(degree) in middle_degrees]
    middle_counts = {degree: counts[degree] for degree in sorted(middle_degrees)}
    return middle_vertices, middle_counts


def decode_degree_separated_cfi_twist_parity(adjacency: np.ndarray) -> IrregularCFIStructuralDecode:
    matrix = np.asarray(adjacency, dtype=np.uint8)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        return _failure_decode("not-square-adjacency", matrix, "Adjacency matrix must be square.")

    middle_vertices, middle_counts = infer_degree_separated_middle_vertices(matrix)
    inferred_degrees = sorted(middle_counts)
    if not middle_vertices:
        return _failure_decode(
            "no-degree-separated-middle-class",
            matrix,
            "No degree class has the divisibility profile of degree-separated CFI middle gadgets.",
        )

    inferred_base_vertex_count = sum(count // (1 << (degree - 1)) for degree, count in middle_counts.items())
    middle_set = set(middle_vertices)
    edge_copy_vertices = [idx for idx in range(matrix.shape[0]) if idx not in middle_set]
    if len(edge_copy_vertices) % 2:
        return _failure_decode(
            "odd-edge-copy-count",
            matrix,
            "The non-middle vertex count is odd, so it cannot be partitioned into CFI edge-copy pairs.",
            inferred_degrees,
            middle_counts,
            inferred_base_vertex_count,
            middle_vertex_count=len(middle_vertices),
            edge_copy_vertex_count=len(edge_copy_vertices),
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
            inferred_degrees,
            middle_counts,
            inferred_base_vertex_count,
            middle_vertex_count=len(middle_vertices),
            edge_copy_vertex_count=len(edge_copy_vertices),
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
                "A reconstructed middle vertex is not incident to one copy from each local base edge.",
                inferred_degrees,
                middle_counts,
                inferred_base_vertex_count,
                middle_vertex_count=len(middle_vertices),
                edge_copy_vertex_count=len(edge_copy_vertices),
                edge_pair_count=len(signature_groups),
            )
        gadget_bits.setdefault(key, []).append(bits)

    if len(gadget_bits) != inferred_base_vertex_count:
        return _failure_decode(
            "invalid-vertex-gadget-count",
            matrix,
            f"Recovered {len(gadget_bits)} vertex gadgets, expected {inferred_base_vertex_count}.",
            inferred_degrees,
            middle_counts,
            inferred_base_vertex_count,
            middle_vertex_count=len(middle_vertices),
            edge_copy_vertex_count=len(edge_copy_vertices),
            edge_pair_count=len(signature_groups),
            vertex_gadget_count=len(gadget_bits),
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
                (
                    "A reconstructed vertex gadget does not have the expected even/odd assignment count "
                    "with uniform local parity."
                ),
                inferred_degrees,
                middle_counts,
                inferred_base_vertex_count,
                middle_vertex_count=len(middle_vertices),
                edge_copy_vertex_count=len(edge_copy_vertices),
                edge_pair_count=len(signature_groups),
                vertex_gadget_count=len(gadget_bits),
            )
        local_parities.append(next(iter(parities)))

    global_parity = sum(local_parities) % 2
    return IrregularCFIStructuralDecode(
        success=True,
        status="decoded-degree-separated-global-twist-parity",
        vertex_count=int(matrix.shape[0]),
        inferred_middle_degrees=inferred_degrees,
        inferred_middle_degree_counts=middle_counts,
        inferred_base_vertex_count=inferred_base_vertex_count,
        middle_vertex_count=len(middle_vertices),
        edge_copy_vertex_count=len(edge_copy_vertices),
        edge_pair_count=len(signature_groups),
        vertex_gadget_count=len(gadget_bits),
        local_parities=local_parities,
        global_twist_parity=global_parity,
        ambiguity="none",
        interpretation=(
            "Recovered irregular degree-separated CFI global twist parity from middle-degree divisibility, "
            "edge-copy twin signatures, and vertex-gadget parity profiles."
        ),
    )


def _degree_separated(base: np.ndarray) -> bool:
    base_degrees = [int(value) for value in base.sum(axis=1).tolist()]
    middle_degrees = set(base_degrees)
    edge_copy_degrees = {
        (1 << (base_degrees[left] - 2)) + (1 << (base_degrees[right] - 2))
        for left, right in base_edges(base)
    }
    return middle_degrees.isdisjoint(edge_copy_degrees)


def audit_irregular_cfi_structural_decoder_record(
    base_id: str,
    shuffle: bool = True,
    seed: int = 13001,
) -> IrregularCFIStructuralDecoderRecord:
    description, base = irregular_base_graph_by_id(base_id)
    edge = base_edges(base)[0]
    untwisted = cfi_parity_graph_from_base(base, twisted_edge=None)
    twisted = cfi_parity_graph_from_base(base, twisted_edge=edge)
    if shuffle:
        untwisted = permute_adjacency(untwisted, seed + 17 * len(base_id))
        twisted = permute_adjacency(twisted, seed + 101 + 17 * len(base_id))

    untwisted_decode = decode_degree_separated_cfi_twist_parity(untwisted)
    twisted_decode = decode_degree_separated_cfi_twist_parity(twisted)
    recovers = (
        untwisted_decode.success
        and twisted_decode.success
        and untwisted_decode.global_twist_parity == 0
        and twisted_decode.global_twist_parity == 1
    )
    if recovers:
        status = "dequantized-by-irregular-structural-cfi-decoder"
        interpretation = (
            f"Irregular CFI base {base_id} still has global twist parity classically recovered from the unlabeled "
            "adjacency matrix under the degree-separated CFI-gadget promise."
        )
    else:
        status = "irregular-structural-decoder-proof-debt"
        interpretation = (
            f"Irregular CFI base {base_id} was not decoded by the degree-separated structural baseline; this is "
            "proof debt, not positive evidence."
        )

    degrees = [int(value) for value in base.sum(axis=1).tolist()]
    spec = IrregularCFIBaseSpec(
        id=base_id,
        description=description,
        vertex_count=int(base.shape[0]),
        edge_count=len(base_edges(base)),
        degree_sequence=sorted(degrees),
        twist_edge=edge,
        construction_note="Single-edge twist in a degree-separated irregular CFI parity gadget.",
    )
    return IrregularCFIStructuralDecoderRecord(
        base=spec,
        cfi_vertex_count=int(untwisted.shape[0]),
        shuffled=shuffle,
        degree_separated=_degree_separated(base),
        untwisted_decode=untwisted_decode,
        twisted_decode=twisted_decode,
        recovers_global_twist=recovers,
        legal_access_model="unlabeled adjacency matrix with degree-separated irregular CFI gadget-family promise",
        status=status,
        interpretation=interpretation,
    )


def run_irregular_cfi_structural_decoder(
    base_ids: list[str] | None = None,
    shuffle: bool = True,
    seed: int = 13001,
) -> IrregularCFIStructuralDecoderReport:
    active = base_ids or DEFAULT_IRREGULAR_CFI_BASE_IDS
    records = [audit_irregular_cfi_structural_decoder_record(base_id, shuffle=shuffle, seed=seed) for base_id in active]
    metrics = {
        "base_count": len(records),
        "decoded_count": sum(1 for record in records if record.untwisted_decode.success and record.twisted_decode.success),
        "dequantized_count": sum(1 for record in records if record.status == "dequantized-by-irregular-structural-cfi-decoder"),
        "proof_debt_count": sum(1 for record in records if record.status == "irregular-structural-decoder-proof-debt"),
        "degree_separated_count": sum(1 for record in records if record.degree_separated),
        "max_vertex_count": max((record.cfi_vertex_count for record in records), default=0),
    }
    if metrics["dequantized_count"]:
        status = "irregular-cfi-family-dequantized-under-degree-separated-gadget-promise"
    elif metrics["proof_debt_count"]:
        status = "irregular-cfi-structural-decoder-proof-debt"
    else:
        status = "irregular-cfi-structural-decoder-incomplete"
    summary = (
        f"Ran degree-separated irregular CFI structural decoding on {metrics['base_count']} row(s). "
        f"{metrics['dequantized_count']} row(s) were dequantized under the gadget promise; "
        f"{metrics['proof_debt_count']} remain proof debt."
    )
    falsifiers = []
    if metrics["dequantized_count"]:
        falsifiers.append("Degree-separated irregular CFI gadget structure classically reveals global twist parity.")
    if metrics["proof_debt_count"]:
        falsifiers.append("Irregular rows not decoded by this baseline remain proof debt, not positive evidence.")
    return IrregularCFIStructuralDecoderReport(utc_now(), active, records, metrics, status, summary, falsifiers)


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


def write_irregular_cfi_structural_decoder_negative_results(report: IrregularCFIStructuralDecoderReport) -> int:
    written = 0
    for record in report.records:
        if record.status != "dequantized-by-irregular-structural-cfi-decoder":
            continue
        upsert_negative_result(
            NegativeResultRecord(
                id=f"CFI-IRREGULAR-STRUCTURAL-DECODER-DEQUANTIZED-{_safe_id(record.base.id)}",
                source="cfi_irregular_structural_decoder.py",
                claim=(
                    f"Irregular degree-separated CFI base {record.base.id} supplies nonclassical coset-state evidence "
                    "under the CFI gadget promise."
                ),
                reason_invalid=record.interpretation,
                lesson=(
                    "Irregularity is not enough. Degree-separated CFI gadget rows can still expose a classical "
                    "structural parity decoder, so they must be rejected unless the input model makes the promise "
                    "illegal or a stronger construction escapes reconstruction."
                ),
                applies_to=["CODE-COSET-COLLECTIVE", "PO-DEQUANTIZATION", "PO-MEASUREMENT"],
                evidence=asdict(record),
            )
        )
        written += 1
    return written


def write_irregular_cfi_structural_decoder_report(
    output_path: Path = CFI_IRREGULAR_STRUCTURAL_DECODER_PATH,
    base_ids: list[str] | None = None,
    shuffle: bool = True,
    seed: int = 13001,
    write_registry: bool = True,
    registry_experiment_id: str = "EXP-COSET-CFI-IRREGULAR-STRUCTURAL-DECODER",
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "RESULT-COSET-CFI-IRREGULAR-STRUCTURAL-DECODER-LATEST",
) -> dict[str, Any]:
    report = run_irregular_cfi_structural_decoder(base_ids=base_ids, shuffle=shuffle, seed=seed)
    payload = _json_ready(report)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    if write_registry:
        negative_results_written = write_irregular_cfi_structural_decoder_negative_results(report)
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
                artifacts={"cfi_irregular_structural_decoder": str(output_path)},
            )
        )
    return payload
