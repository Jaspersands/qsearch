"""Faithful graph-isomorphism to binary-code-equivalence reduction.

For a simple graph G on vertices 0,...,v-1, the generator contains two
copies of every unit column e_i and one column e_i + e_j for every edge.
The duplicate columns are an intrinsic tag set.  Any linear-code equivalence
must map multiplicity-two projective points to multiplicity-two projective
points, hence it permutes the vertex basis and preserves exactly the edges.

This module uses the reduction as a research control, not as evidence for a
quantum advantage.  It verifies the iff theorem computationally, recovers the
graph after arbitrary row operations and coordinate permutations, and then
runs legal graph-side attacks.  Recovering the graph is only a reduction back
to graph isomorphism; a row is dequantized only when a graph-side baseline
actually distinguishes it.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from dataclasses import asdict, dataclass, is_dataclass
from pathlib import Path
from typing import Any, Sequence

import networkx as nx
import numpy as np

from cfi_base_family_search import DEFAULT_BASE_IDS, base_edges, base_graph_by_id, cfi_parity_graph_from_base
from cfi_structural_decoder import decode_regular_cfi_twist_parity
from code_equivalence_workbench import gf2_rank
from coset_state_workbench import degree_signature, spectrum_signature, walk_count_signature, wl1_signature, wl2_signature
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


CODE_EQUIVALENCE_DIR = Path("research/code_equivalence")
CFI_CODE_REDUCTION_PATH = CODE_EQUIVALENCE_DIR / "cfi_code_reduction.json"


@dataclass(frozen=True)
class ReductionTheoremCertificate:
    theorem_id: str
    domain: str
    construction: str
    graph_isomorphism_implies_code_equivalence: bool
    code_equivalence_implies_graph_isomorphism: bool
    polynomial_graph_recovery: bool
    forward_proof: str
    reverse_proof: str
    recovery_proof: str
    size_bound: str
    caveats: list[str]


@dataclass(frozen=True)
class GraphRecoveryCertificate:
    success: bool
    status: str
    input_dimension: int
    input_length: int
    tag_point_count: int
    edge_point_count: int
    recovered_vertex_count: int
    recovered_edge_count: int
    tag_basis_rank: int
    graph_digest: str
    cost_model: str
    interpretation: str


@dataclass(frozen=True)
class CFIGraphCodeRecord:
    base_id: str
    base_description: str
    cfi_vertex_count: int
    cfi_edge_count: int
    code_dimension: int
    code_length: int
    code_rate: float
    equivalent_control_witness_verified: bool
    untwisted_recovery: GraphRecoveryCertificate
    twisted_recovery: GraphRecoveryCertificate
    recovered_graphs_match_sources_up_to_isomorphism: bool
    cheap_graph_invariants_distinguish: bool
    wl2_distinguishes: bool
    promised_decoder_legal: bool
    untwisted_decoder_status: str
    twisted_decoder_status: str
    promised_decoder_recovers_parity: bool
    graph_recovery_is_gi_solution: bool
    status: str
    interpretation: str


@dataclass(frozen=True)
class CFIGraphCodeReductionReport:
    created_at: str
    theorem: ReductionTheoremCertificate
    access_model_ledger: list[dict[str, Any]]
    records: list[CFIGraphCodeRecord]
    headline_metrics: dict[str, int | float]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _validate_simple_adjacency(adjacency: np.ndarray) -> np.ndarray:
    matrix = np.asarray(adjacency, dtype=np.uint8) & 1
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("graph adjacency matrix must be square")
    if np.any(np.diag(matrix)):
        raise ValueError("faithful tagged encoding requires a loopless graph")
    if not np.array_equal(matrix, matrix.T):
        raise ValueError("faithful tagged encoding requires an undirected graph")
    return matrix


def graph_to_tagged_code(adjacency: np.ndarray) -> np.ndarray:
    """Encode a simple graph as a full-rank binary generator matrix."""

    matrix = _validate_simple_adjacency(adjacency)
    vertex_count = int(matrix.shape[0])
    columns: list[np.ndarray] = []
    for vertex in range(vertex_count):
        unit = np.zeros(vertex_count, dtype=np.uint8)
        unit[vertex] = 1
        columns.extend((unit.copy(), unit.copy()))
    for left in range(vertex_count):
        for right in range(left + 1, vertex_count):
            if matrix[left, right]:
                edge = np.zeros(vertex_count, dtype=np.uint8)
                edge[left] = edge[right] = 1
                columns.append(edge)
    return np.column_stack(columns).astype(np.uint8)


def _gf2_inverse(matrix: np.ndarray) -> np.ndarray:
    values = np.asarray(matrix, dtype=np.uint8).copy() & 1
    if values.ndim != 2 or values.shape[0] != values.shape[1]:
        raise ValueError("GF(2) inverse requires a square matrix")
    size = int(values.shape[0])
    augmented = np.concatenate((values, np.eye(size, dtype=np.uint8)), axis=1)
    for col in range(size):
        pivot = next((row for row in range(col, size) if augmented[row, col]), None)
        if pivot is None:
            raise ValueError("matrix is singular over GF(2)")
        if pivot != col:
            augmented[[col, pivot]] = augmented[[pivot, col]]
        for row in range(size):
            if row != col and augmented[row, col]:
                augmented[row] ^= augmented[col]
    return augmented[:, size:]


def _random_invertible_matrix(size: int, rng: np.random.Generator) -> np.ndarray:
    values = np.eye(size, dtype=np.uint8)
    for _ in range(max(8, 6 * size)):
        left, right = rng.choice(size, size=2, replace=False)
        if rng.integers(2):
            values[[left, right]] = values[[right, left]]
        else:
            values[left] ^= values[right]
    return values


def scramble_generator(generator: np.ndarray, seed: int) -> tuple[np.ndarray, np.ndarray]:
    """Apply hidden row operations and a hidden coordinate permutation."""

    values = np.asarray(generator, dtype=np.uint8) & 1
    rng = np.random.default_rng(seed)
    row_map = _random_invertible_matrix(int(values.shape[0]), rng)
    permutation = rng.permutation(values.shape[1])
    return ((row_map @ values[:, permutation]) & 1).astype(np.uint8), permutation.astype(int)


def _digest_graph(adjacency: np.ndarray) -> str:
    degrees = sorted(int(value) for value in np.asarray(adjacency).sum(axis=1).tolist())
    edges = int(np.asarray(adjacency).sum() // 2)
    payload = f"v={adjacency.shape[0]};e={edges};d={degrees}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:24]


def _recovery_failure(generator: np.ndarray, status: str, interpretation: str, tag_count: int = 0) -> tuple[None, GraphRecoveryCertificate]:
    dimension, length = np.asarray(generator).shape
    return None, GraphRecoveryCertificate(
        success=False,
        status=status,
        input_dimension=int(dimension),
        input_length=int(length),
        tag_point_count=int(tag_count),
        edge_point_count=0,
        recovered_vertex_count=0,
        recovered_edge_count=0,
        tag_basis_rank=0,
        graph_digest="",
        cost_model="Column multiplicity scan plus GF(2) elimination; rejected before reconstruction.",
        interpretation=interpretation,
    )


def recover_graph_from_tagged_code(generator: np.ndarray) -> tuple[np.ndarray | None, GraphRecoveryCertificate]:
    """Recover an unlabeled graph from any generator of a tagged graph code."""

    values = np.asarray(generator, dtype=np.uint8) & 1
    if values.ndim != 2:
        raise ValueError("generator matrix must be two-dimensional")
    dimension, length = values.shape
    if gf2_rank(values) != dimension:
        return _recovery_failure(values, "non-full-rank-generator", "The supplied rows are not a full-rank code basis.")

    column_keys = [tuple(int(bit) for bit in values[:, coordinate]) for coordinate in range(length)]
    multiplicities = Counter(column_keys)
    if tuple(0 for _ in range(dimension)) in multiplicities:
        return _recovery_failure(values, "zero-column-present", "Tagged graph codes contain no zero coordinate.")
    tags = sorted(point for point, count in multiplicities.items() if count == 2)
    if len(tags) != dimension:
        return _recovery_failure(
            values,
            "tag-multiplicity-profile-invalid",
            f"Expected {dimension} multiplicity-two tag points, found {len(tags)}.",
            tag_count=len(tags),
        )
    if any(count not in {1, 2} for count in multiplicities.values()):
        return _recovery_failure(
            values,
            "unsupported-column-multiplicity",
            "Only multiplicity-two vertex tags and multiplicity-one edge points are permitted.",
            tag_count=len(tags),
        )

    tag_matrix = np.asarray(tags, dtype=np.uint8).T
    tag_rank = gf2_rank(tag_matrix)
    if tag_rank != dimension:
        return _recovery_failure(
            values,
            "tag-points-not-a-basis",
            f"Multiplicity-two points have GF(2) rank {tag_rank}, expected {dimension}.",
            tag_count=len(tags),
        )
    normalized = (_gf2_inverse(tag_matrix) @ values) & 1
    normalized_keys = [tuple(int(bit) for bit in normalized[:, coordinate]) for coordinate in range(length)]
    normalized_counts = Counter(normalized_keys)
    adjacency = np.zeros((dimension, dimension), dtype=np.uint8)
    edge_count = 0
    for point, count in normalized_counts.items():
        weight = sum(point)
        if count == 2 and weight == 1:
            continue
        if count == 1 and weight == 2:
            endpoints = [index for index, bit in enumerate(point) if bit]
            left, right = endpoints
            if adjacency[left, right]:
                return _recovery_failure(values, "parallel-edge-point", "Recovered duplicate edge points.", len(tags))
            adjacency[left, right] = adjacency[right, left] = 1
            edge_count += 1
            continue
        return _recovery_failure(
            values,
            "non-graph-point-after-normalization",
            f"Normalized point of weight {weight} and multiplicity {count} violates the tagged graph schema.",
            tag_count=len(tags),
        )

    certificate = GraphRecoveryCertificate(
        success=True,
        status="graph-recovered-up-to-vertex-permutation",
        input_dimension=int(dimension),
        input_length=int(length),
        tag_point_count=len(tags),
        edge_point_count=edge_count,
        recovered_vertex_count=int(dimension),
        recovered_edge_count=edge_count,
        tag_basis_rank=tag_rank,
        graph_digest=_digest_graph(adjacency),
        cost_model=f"O({dimension}^3 + {dimension}*{length}) GF(2) operations plus column hashing.",
        interpretation=(
            "Multiplicity-two points recover a vertex basis; multiplicity-one weight-two points recover the graph. "
            "This is a reduction to graph isomorphism, not a graph-isomorphism solution."
        ),
    )
    return adjacency.astype(int), certificate


def _isomorphic(left: np.ndarray, right: np.ndarray) -> bool:
    return bool(nx.is_isomorphic(nx.from_numpy_array(left), nx.from_numpy_array(right)))


def _equivalent_control_witness(generator: np.ndarray, seed: int) -> bool:
    left, left_permutation = scramble_generator(generator, seed)
    right, right_permutation = scramble_generator(generator, seed + 1)
    left_aligned = left[:, np.argsort(left_permutation)]
    right_aligned = right[:, np.argsort(right_permutation)]
    return gf2_rank(np.vstack((left_aligned, right_aligned))) == gf2_rank(generator)


def reduction_theorem_certificate() -> ReductionTheoremCertificate:
    return ReductionTheoremCertificate(
        theorem_id="THM-GI-TO-BINARY-CODE-EQUIVALENCE-TAGGED-POINTS",
        domain="Finite simple undirected graphs; binary linear codes may contain repeated coordinates.",
        construction="G maps to columns {e_i,e_i : i in V} union {e_i+e_j : {i,j} in E}.",
        graph_isomorphism_implies_code_equivalence=True,
        code_equivalence_implies_graph_isomorphism=True,
        polynomial_graph_recovery=True,
        forward_proof=(
            "A vertex permutation acts linearly on the unit basis, permutes both copies of every vertex tag, "
            "and maps an edge column e_i+e_j exactly to the corresponding relabeled edge column."
        ),
        reverse_proof=(
            "Code equivalence of full-rank generators induces an invertible linear map on their column multisets. "
            "Point multiplicity is preserved. The only multiplicity-two points are the unit tags, so the map "
            "permutes a basis. Every multiplicity-one edge point therefore maps as e_i+e_j to e_pi(i)+e_pi(j), "
            "which is exactly a graph isomorphism."
        ),
        recovery_proof=(
            "Hash columns, select the multiplicity-two points, invert that basis, and read every remaining "
            "multiplicity-one weight-two point as an edge. The output is canonical only up to vertex permutation."
        ),
        size_bound="dimension v; length 2v+|E| <= v(v+3)/2; construction and recovery are polynomial.",
        caveats=[
            "The reduction deliberately exposes the graph; it transfers GI hardness but adds no hardness beyond GI.",
            "Repeated coordinates are essential to this simple proof.",
            "Recovery requires an explicit full-rank generator matrix, not sample-only or coset-state-only access.",
            "A promised CFI-family decoder remains legal after recovery when the promise is part of the problem.",
        ],
    )


def access_model_ledger() -> list[dict[str, Any]]:
    return [
        {
            "model": "explicit-full-rank-generator-matrix",
            "graph_recovery_legal": True,
            "promised_cfi_decoder_legal": True,
            "reason": "Column multiplicities and a tag basis are explicitly available in polynomial time.",
        },
        {
            "model": "random-codeword-samples",
            "graph_recovery_legal": False,
            "promised_cfi_decoder_legal": False,
            "reason": "The coordinate-column multiset is not exposed by random codeword samples alone.",
        },
        {
            "model": "coset-state-copies-only",
            "graph_recovery_legal": False,
            "promised_cfi_decoder_legal": False,
            "reason": "A classical generator recovery theorem from bounded coset-state copies is not supplied.",
        },
        {
            "model": "coherent-code-membership-oracle",
            "graph_recovery_legal": False,
            "promised_cfi_decoder_legal": False,
            "reason": "The explicit-generator recovery cost cannot be charged to a membership oracle without a reduction.",
        },
    ]


def _cheap_graph_signature(adjacency: np.ndarray) -> tuple[Any, ...]:
    return (
        degree_signature(adjacency),
        spectrum_signature(adjacency),
        walk_count_signature(adjacency, max_length=8),
        wl1_signature(adjacency),
    )


def audit_cfi_graph_code(base_id: str, seed: int = 14_071) -> CFIGraphCodeRecord:
    description, base = base_graph_by_id(base_id)
    twist_edge = base_edges(base)[0]
    untwisted = cfi_parity_graph_from_base(base, twisted_edge=None)
    twisted = cfi_parity_graph_from_base(base, twisted_edge=twist_edge)
    untwisted_code = graph_to_tagged_code(untwisted)
    twisted_code = graph_to_tagged_code(twisted)

    control_verified = _equivalent_control_witness(untwisted_code, seed + len(base_id))
    scrambled_untwisted, _ = scramble_generator(untwisted_code, seed + 101 * len(base_id))
    scrambled_twisted, _ = scramble_generator(twisted_code, seed + 203 * len(base_id))
    recovered_untwisted, untwisted_certificate = recover_graph_from_tagged_code(scrambled_untwisted)
    recovered_twisted, twisted_certificate = recover_graph_from_tagged_code(scrambled_twisted)

    recovered_match = bool(
        recovered_untwisted is not None
        and recovered_twisted is not None
        and _isomorphic(untwisted, recovered_untwisted)
        and _isomorphic(twisted, recovered_twisted)
    )
    cheap_distinguishes = False
    wl2_distinguishes = False
    promised_recovers = False
    untwisted_decoder_status = "not-run-recovery-failed"
    twisted_decoder_status = "not-run-recovery-failed"
    if recovered_untwisted is not None and recovered_twisted is not None:
        cheap_distinguishes = _cheap_graph_signature(recovered_untwisted) != _cheap_graph_signature(recovered_twisted)
        wl2_distinguishes = wl2_signature(recovered_untwisted) != wl2_signature(recovered_twisted)
        untwisted_decode = decode_regular_cfi_twist_parity(recovered_untwisted)
        twisted_decode = decode_regular_cfi_twist_parity(recovered_twisted)
        untwisted_decoder_status = untwisted_decode.status
        twisted_decoder_status = twisted_decode.status
        promised_recovers = bool(
            untwisted_decode.success
            and twisted_decode.success
            and untwisted_decode.global_twist_parity == 0
            and twisted_decode.global_twist_parity == 1
        )

    if not control_verified or not recovered_match:
        status = "invalid-reduction-implementation"
        interpretation = "The equivalent control or graph recovery sanity check failed; no research conclusion is valid."
    elif promised_recovers:
        status = "faithful-reduction-cfi-promise-dequantized"
        interpretation = (
            "The code pair faithfully represents the CFI graph pair, but explicit-generator access recovers the graph "
            "and the legal regular-CFI promise decoder recovers global twist parity classically."
        )
    elif cheap_distinguishes or wl2_distinguishes:
        status = "faithful-reduction-classically-separated"
        interpretation = "The faithful code pair reduces to graphs that a polynomial graph invariant already separates."
    else:
        status = "faithful-reduction-proof-debt-no-general-gi-solver"
        interpretation = (
            "The tagged code is faithfully equivalent to the graph instance and survives current graph baselines, "
            "but this is only transferred GI proof debt and supplies no quantum signal."
        )

    vertex_count = int(untwisted.shape[0])
    edge_count = int(untwisted.sum() // 2)
    return CFIGraphCodeRecord(
        base_id=base_id,
        base_description=description,
        cfi_vertex_count=vertex_count,
        cfi_edge_count=edge_count,
        code_dimension=int(untwisted_code.shape[0]),
        code_length=int(untwisted_code.shape[1]),
        code_rate=float(untwisted_code.shape[0] / untwisted_code.shape[1]),
        equivalent_control_witness_verified=control_verified,
        untwisted_recovery=untwisted_certificate,
        twisted_recovery=twisted_certificate,
        recovered_graphs_match_sources_up_to_isomorphism=recovered_match,
        cheap_graph_invariants_distinguish=cheap_distinguishes,
        wl2_distinguishes=wl2_distinguishes,
        promised_decoder_legal=True,
        untwisted_decoder_status=untwisted_decoder_status,
        twisted_decoder_status=twisted_decoder_status,
        promised_decoder_recovers_parity=promised_recovers,
        graph_recovery_is_gi_solution=False,
        status=status,
        interpretation=interpretation,
    )


def run_cfi_graph_code_reduction(base_ids: Sequence[str] | None = None, seed: int = 14_071) -> CFIGraphCodeReductionReport:
    active = list(base_ids) if base_ids is not None else list(DEFAULT_BASE_IDS)
    records = [audit_cfi_graph_code(base_id, seed=seed) for base_id in active]
    metrics: dict[str, int | float] = {
        "base_count": len(records),
        "theorem_direction_count": 2,
        "recovery_verified_count": sum(record.recovered_graphs_match_sources_up_to_isomorphism for record in records),
        "equivalent_control_verified_count": sum(record.equivalent_control_witness_verified for record in records),
        "promised_decoder_dequantized_count": sum(
            record.status == "faithful-reduction-cfi-promise-dequantized" for record in records
        ),
        "graph_invariant_rejection_count": sum(
            record.status == "faithful-reduction-classically-separated" for record in records
        ),
        "transferred_gi_proof_debt_count": sum(
            record.status == "faithful-reduction-proof-debt-no-general-gi-solver" for record in records
        ),
        "invalid_count": sum(record.status == "invalid-reduction-implementation" for record in records),
        "max_code_dimension": max((record.code_dimension for record in records), default=0),
        "max_code_length": max((record.code_length for record in records), default=0),
        "positive_quantum_evidence_count": 0,
    }
    if metrics["invalid_count"]:
        status = "cfi-code-reduction-invalid"
    elif metrics["transferred_gi_proof_debt_count"]:
        status = "faithful-cfi-code-reduction-has-transferred-gi-proof-debt"
    else:
        status = "faithful-cfi-code-reduction-current-promised-families-dequantized"
    summary = (
        f"Certified both directions of the tagged graph/code reduction on {len(records)} CFI family row(s); "
        f"{metrics['promised_decoder_dequantized_count']} were dequantized after legal graph recovery and "
        f"{metrics['transferred_gi_proof_debt_count']} remain only transferred GI proof debt."
    )
    falsifiers = []
    if metrics["promised_decoder_dequantized_count"]:
        falsifiers.append("Explicit tagged-code recovery exposes a graph on which the promised CFI parity decoder succeeds.")
    if metrics["invalid_count"]:
        falsifiers.append("A reduction control or recovery certificate failed.")
    return CFIGraphCodeReductionReport(
        created_at=utc_now(),
        theorem=reduction_theorem_certificate(),
        access_model_ledger=access_model_ledger(),
        records=records,
        headline_metrics=metrics,
        status=status,
        summary=summary,
        falsifiers_triggered=falsifiers,
    )


def _json_ready(value: Any) -> Any:
    if is_dataclass(value):
        return _json_ready(asdict(value))
    if isinstance(value, dict):
        return {str(key): _json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_ready(item) for item in value]
    if isinstance(value, (np.integer, np.bool_)):
        return value.item()
    return value


def _safe_id(value: str) -> str:
    return "".join(character if character.isalnum() else "_" for character in value.upper()).strip("_")


def write_cfi_graph_code_negative_results(report: CFIGraphCodeReductionReport) -> int:
    written = 0
    for record in report.records:
        if record.status not in {
            "faithful-reduction-cfi-promise-dequantized",
            "faithful-reduction-classically-separated",
        }:
            continue
        upsert_negative_result(
            NegativeResultRecord(
                id=f"CFI-CODE-REDUCTION-DEQUANTIZED-{_safe_id(record.base_id)}",
                source="cfi_code_reduction.py",
                claim=f"Tagged-code encoding of CFI base {record.base_id} supplies hard code-equivalence evidence.",
                reason_invalid=record.interpretation,
                lesson=(
                    "A faithful reduction does not make a promised benchmark hard. Charge explicit graph recovery and "
                    "every legal graph-side decoder before using the row in nonabelian coset measurement research."
                ),
                applies_to=["CODE-COSET-COLLECTIVE", "PO-DEQUANTIZATION", "PO-REDUCTION"],
                evidence={
                    "base_id": record.base_id,
                    "status": record.status,
                    "code_dimension": record.code_dimension,
                    "code_length": record.code_length,
                    "promised_decoder_recovers_parity": record.promised_decoder_recovers_parity,
                    "graph_recovery_is_gi_solution": record.graph_recovery_is_gi_solution,
                },
            )
        )
        written += 1
    return written


def write_cfi_graph_code_reduction(
    output_path: Path = CFI_CODE_REDUCTION_PATH,
    base_ids: Sequence[str] | None = None,
    seed: int = 14_071,
    write_registry: bool = True,
    registry_experiment_id: str = "EXP-CODE-CFI-FAITHFUL-REDUCTION",
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "RESULT-CODE-CFI-FAITHFUL-REDUCTION-LATEST",
) -> dict[str, Any]:
    report = run_cfi_graph_code_reduction(base_ids=base_ids, seed=seed)
    payload = _json_ready(report)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        metrics = dict(report.headline_metrics)
        metrics["negative_results_written"] = write_cfi_graph_code_negative_results(report)
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
                artifacts={"cfi_code_reduction": str(output_path)},
            )
        )
    return payload
