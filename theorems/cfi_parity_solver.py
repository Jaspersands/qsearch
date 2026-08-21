"""Promised CFI parity decoder for complete-graph gadget families.

The existing CFI scaling probe marks complete-graph parity twists as boundary
rows when low-cost invariants fail and brute-force WL/tensor probes hit caps.
This module attacks that evidence under a stronger but explicit promise: the
input is known to be a CFI gadget family over a complete base graph.  Under that
promise, the global twist parity can be recovered classically from the adjacency
matrix by reconstructing edge-copy pairs and vertex gadgets.

This is not a generic graph-isomorphism solver.  It is a dequantization guard
for our own generated benchmark family: if a proposed coset observable uses the
same complete-CFI promise, the family is classically transparent.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, is_dataclass
from pathlib import Path
from typing import Any

import numpy as np

from coset_state_workbench import cfi_parity_graph_complete
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


COSET_WORKBENCH_DIR = Path("research/coset_workbench")
CFI_PARITY_SOLVER_PATH = COSET_WORKBENCH_DIR / "cfi_parity_solver.json"


@dataclass(frozen=True)
class CFIParityDecode:
    success: bool
    status: str
    inferred_base_size: int | None
    vertex_count: int
    middle_vertex_count: int
    edge_copy_vertex_count: int
    edge_pair_count: int
    vertex_gadget_count: int
    local_parities: list[int]
    global_twist_parity: int | None
    ambiguity: str
    interpretation: str


@dataclass(frozen=True)
class CFIParitySolverRecord:
    base_size: int
    vertex_count: int
    shuffled: bool
    untwisted_decode: CFIParityDecode
    twisted_decode: CFIParityDecode
    recovers_global_twist: bool
    legal_access_model: str
    status: str
    interpretation: str


@dataclass(frozen=True)
class CFIParitySolverReport:
    created_at: str
    base_sizes: list[int]
    records: list[CFIParitySolverRecord]
    headline_metrics: dict[str, int]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def permute_adjacency(adjacency: np.ndarray, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    permutation = rng.permutation(adjacency.shape[0])
    return adjacency[permutation][:, permutation]


def _failure_decode(
    status: str,
    adjacency: np.ndarray,
    ambiguity: str,
    inferred_base_size: int | None = None,
) -> CFIParityDecode:
    return CFIParityDecode(
        success=False,
        status=status,
        inferred_base_size=inferred_base_size,
        vertex_count=int(adjacency.shape[0]),
        middle_vertex_count=0,
        edge_copy_vertex_count=0,
        edge_pair_count=0,
        vertex_gadget_count=0,
        local_parities=[],
        global_twist_parity=None,
        ambiguity=ambiguity,
        interpretation=ambiguity,
    )


def _expected_counts(base_size: int) -> tuple[int, int, int]:
    middle_count = base_size * (1 << (base_size - 2))
    edge_copy_count = base_size * (base_size - 1)
    total = middle_count + edge_copy_count
    return middle_count, edge_copy_count, total


def decode_complete_cfi_twist_parity(adjacency: np.ndarray) -> CFIParityDecode:
    """Recover complete-CFI global twist parity from an unlabeled adjacency matrix.

    The decoder only accepts the degree/count structure of the complete-graph
    CFI family.  K4 is deliberately reported as ambiguous: the line graph of K4
    creates twin groups of size four, so the simple edge-copy pairing rule is
    not canonical.
    """

    matrix = np.asarray(adjacency, dtype=np.uint8)
    degrees = matrix.sum(axis=1).astype(int)
    degree_values = sorted(set(int(value) for value in degrees.tolist()))
    if len(degree_values) != 2:
        return _failure_decode(
            "not-complete-cfi-degree-profile",
            matrix,
            f"Expected two CFI degree classes, found {degree_values}.",
        )

    middle_degree, edge_copy_degree = degree_values
    base_size = middle_degree + 1
    if base_size < 4:
        return _failure_decode(
            "not-complete-cfi-degree-profile",
            matrix,
            f"Inferred base size {base_size} is below the complete-CFI stress-test range.",
            inferred_base_size=base_size,
        )

    middle_vertices = [idx for idx, degree in enumerate(degrees.tolist()) if degree == middle_degree]
    edge_copy_vertices = [idx for idx, degree in enumerate(degrees.tolist()) if degree == edge_copy_degree]
    expected_middle, expected_edge_copy, expected_total = _expected_counts(base_size)
    if (
        len(middle_vertices) != expected_middle
        or len(edge_copy_vertices) != expected_edge_copy
        or int(matrix.shape[0]) != expected_total
        or edge_copy_degree != (1 << (base_size - 2))
    ):
        return CFIParityDecode(
            success=False,
            status="not-complete-cfi-count-profile",
            inferred_base_size=base_size,
            vertex_count=int(matrix.shape[0]),
            middle_vertex_count=len(middle_vertices),
            edge_copy_vertex_count=len(edge_copy_vertices),
            edge_pair_count=0,
            vertex_gadget_count=0,
            local_parities=[],
            global_twist_parity=None,
            ambiguity=(
                "Degree classes exist but counts do not match the complete-graph CFI family "
                f"for K{base_size}."
            ),
            interpretation="Reject this row as outside the promised complete-CFI decoder model.",
        )

    middle_set = set(middle_vertices)
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
        return CFIParityDecode(
            success=False,
            status="ambiguous-edge-copy-pairing",
            inferred_base_size=base_size,
            vertex_count=int(matrix.shape[0]),
            middle_vertex_count=len(middle_vertices),
            edge_copy_vertex_count=len(edge_copy_vertices),
            edge_pair_count=0,
            vertex_gadget_count=0,
            local_parities=[],
            global_twist_parity=None,
            ambiguity=(
                "Edge-copy twin signatures are not size-two pairs. "
                f"Observed group sizes: {group_sizes[:8]}."
            ),
            interpretation=(
                "The simple promised-gadget parity decoder cannot canonicalize this row; "
                "do not treat this as positive evidence."
            ),
        )

    pair_id: dict[int, int] = {}
    pair_bit: dict[int, int] = {}
    for idx, group in enumerate(sorted(tuple(sorted(group)) for group in signature_groups.values())):
        for bit, vertex in enumerate(group):
            pair_id[vertex] = idx
            pair_bit[vertex] = bit

    gadget_bits: dict[tuple[int, ...], list[tuple[int, ...]]] = {}
    for middle in middle_vertices:
        high_neighbors = [int(item) for item in np.flatnonzero(matrix[middle]) if int(item) in pair_id]
        key = tuple(sorted(pair_id[item] for item in high_neighbors))
        bits = tuple(pair_bit[item] for item in sorted(high_neighbors, key=lambda item: pair_id[item]))
        gadget_bits.setdefault(key, []).append(bits)

    expected_gadget_size = 1 << (base_size - 2)
    local_parities: list[int] = []
    for key, assignments in sorted(gadget_bits.items()):
        parities = {sum(bits) % 2 for bits in assignments}
        if len(key) != base_size - 1 or len(assignments) != expected_gadget_size or len(parities) != 1:
            return CFIParityDecode(
                success=False,
                status="invalid-vertex-gadget-parity-profile",
                inferred_base_size=base_size,
                vertex_count=int(matrix.shape[0]),
                middle_vertex_count=len(middle_vertices),
                edge_copy_vertex_count=len(edge_copy_vertices),
                edge_pair_count=len(signature_groups),
                vertex_gadget_count=len(gadget_bits),
                local_parities=[],
                global_twist_parity=None,
                ambiguity=(
                    "A reconstructed vertex gadget does not have the expected uniform parity profile "
                    f"for K{base_size}."
                ),
                interpretation="The row does not pass the complete-CFI parity decoder's structural checks.",
            )
        local_parities.append(next(iter(parities)))

    global_parity = sum(local_parities) % 2
    return CFIParityDecode(
        success=True,
        status="decoded-global-twist-parity",
        inferred_base_size=base_size,
        vertex_count=int(matrix.shape[0]),
        middle_vertex_count=len(middle_vertices),
        edge_copy_vertex_count=len(edge_copy_vertices),
        edge_pair_count=len(signature_groups),
        vertex_gadget_count=len(gadget_bits),
        local_parities=local_parities,
        global_twist_parity=global_parity,
        ambiguity="none",
        interpretation=(
            "Recovered complete-CFI global twist parity from degree classes, edge-copy twins, "
            "and vertex-gadget parity profiles."
        ),
    )


def audit_cfi_parity_solver_record(base_size: int, shuffle: bool = True, seed: int = 2718) -> CFIParitySolverRecord:
    untwisted = cfi_parity_graph_complete(base_size, twisted_edge=None)
    twisted = cfi_parity_graph_complete(base_size, twisted_edge=(0, 1))
    if shuffle:
        untwisted = permute_adjacency(untwisted, seed + 17 * base_size)
        twisted = permute_adjacency(twisted, seed + 101 + 17 * base_size)

    untwisted_decode = decode_complete_cfi_twist_parity(untwisted)
    twisted_decode = decode_complete_cfi_twist_parity(twisted)
    recovers = (
        untwisted_decode.success
        and twisted_decode.success
        and untwisted_decode.global_twist_parity == 0
        and twisted_decode.global_twist_parity == 1
    )
    if recovers:
        status = "dequantized-by-promised-cfi-parity-decoder"
        interpretation = (
            f"Complete-CFI K{base_size} twist parity is classically recovered from the adjacency matrix "
            "under the explicit CFI-gadget promise; this family is not evidence for a nonabelian speedup."
        )
    elif "ambiguous" in untwisted_decode.status or "ambiguous" in twisted_decode.status:
        status = "decoder-ambiguous-control"
        interpretation = (
            f"Complete-CFI K{base_size} has an ambiguous edge-copy pairing for this decoder; keep it as a control/proof-debt row."
        )
    else:
        status = "parity-decoder-failed-boundary-open"
        interpretation = (
            f"The promised parity decoder did not recover the K{base_size} twist. "
            "This is proof debt, not positive quantum evidence."
        )

    return CFIParitySolverRecord(
        base_size=base_size,
        vertex_count=int(untwisted.shape[0]),
        shuffled=shuffle,
        untwisted_decode=untwisted_decode,
        twisted_decode=twisted_decode,
        recovers_global_twist=recovers,
        legal_access_model="unlabeled adjacency matrix with complete-CFI gadget-family promise",
        status=status,
        interpretation=interpretation,
    )


def run_cfi_parity_solver(
    base_sizes: list[int] | None = None,
    shuffle: bool = True,
    seed: int = 2718,
) -> CFIParitySolverReport:
    sizes = base_sizes or [4, 5, 6, 7, 8]
    records = [audit_cfi_parity_solver_record(size, shuffle=shuffle, seed=seed) for size in sizes]
    metrics = {
        "base_size_count": len(records),
        "decoded_count": sum(1 for record in records if record.untwisted_decode.success and record.twisted_decode.success),
        "dequantized_count": sum(1 for record in records if record.status == "dequantized-by-promised-cfi-parity-decoder"),
        "ambiguous_count": sum(1 for record in records if record.status == "decoder-ambiguous-control"),
        "failed_count": sum(1 for record in records if record.status == "parity-decoder-failed-boundary-open"),
        "max_vertex_count": max((record.vertex_count for record in records), default=0),
    }
    if metrics["dequantized_count"]:
        status = "complete-cfi-family-dequantized-under-gadget-promise"
    elif metrics["failed_count"]:
        status = "parity-decoder-boundary-open"
    else:
        status = "decoder-ambiguous-only"
    summary = (
        f"Ran promised complete-CFI parity decoding on bases {sizes}. "
        f"{metrics['dequantized_count']} row(s) were dequantized under the gadget promise; "
        f"{metrics['ambiguous_count']} row(s) were ambiguous controls."
    )
    falsifiers = []
    if metrics["dequantized_count"]:
        falsifiers.append("Complete-CFI parity rows are classically decoded under the explicit gadget-family promise.")
    if metrics["failed_count"] or metrics["ambiguous_count"]:
        falsifiers.append("Rows not decoded by this baseline remain proof debt, not positive evidence.")
    return CFIParitySolverReport(utc_now(), sizes, records, metrics, status, summary, falsifiers)


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


def write_cfi_parity_solver_negative_results(report: CFIParitySolverReport) -> int:
    written = 0
    for record in report.records:
        if record.status != "dequantized-by-promised-cfi-parity-decoder":
            continue
        upsert_negative_result(
            NegativeResultRecord(
                id=f"CFI-PARITY-SOLVER-DEQUANTIZED-K{record.base_size}",
                source="cfi_parity_solver.py",
                claim=f"Complete-CFI K{record.base_size} parity twist supplies nonclassical coset-state evidence under the CFI gadget promise.",
                reason_invalid=record.interpretation,
                lesson=(
                    "Promised CFI gadget structure can itself expose the global twist parity. "
                    "Do not count complete-CFI rows as speedup evidence unless the input model forbids this structural decoder "
                    "or the family moves beyond the decoded promise class."
                ),
                applies_to=["CODE-COSET-COLLECTIVE", "PO-DEQUANTIZATION", "PO-MEASUREMENT"],
                evidence=asdict(record),
            )
        )
        written += 1
    return written


def write_cfi_parity_solver_report(
    output_path: Path = CFI_PARITY_SOLVER_PATH,
    base_sizes: list[int] | None = None,
    shuffle: bool = True,
    seed: int = 2718,
    write_registry: bool = True,
    registry_experiment_id: str = "EXP-COSET-CFI-PARITY-SOLVER",
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "RESULT-COSET-CFI-PARITY-SOLVER-LATEST",
) -> dict[str, Any]:
    report = run_cfi_parity_solver(base_sizes=base_sizes, shuffle=shuffle, seed=seed)
    payload = _json_ready(report)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    if write_registry:
        negative_results_written = write_cfi_parity_solver_negative_results(report)
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
                artifacts={"cfi_parity_solver": str(output_path)},
            )
        )
    return payload
