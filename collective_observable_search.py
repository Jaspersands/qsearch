"""Collective-observable search for nonabelian coset-state candidates.

This module is adversarial by design.  It searches low-register graph/coset
observable families and immediately labels every separating signal by its
classical shadow.  A signal is useful only if it survives WL, spectrum, walk,
and low-rank tensor-contraction explanations; current probes are therefore
mostly negative evidence and boundary tracking.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, is_dataclass
from pathlib import Path
from typing import Any

import numpy as np

from coset_state_workbench import (
    GraphPairSpec,
    audit_graph_pair,
    cfi_parity_graph_complete,
    chorded_cycle_graph,
    coherent_adjacency_algebra_rank,
    cycle_graph,
    rook_graph_4x4,
    shrikhande_graph,
    spectrum_signature,
    walk_count_signature,
    wl2_signature,
    wl_k_signature,
)
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


COSET_WORKBENCH_DIR = Path("research/coset_workbench")
COLLECTIVE_OBSERVABLE_SEARCH_PATH = COSET_WORKBENCH_DIR / "collective_observable_search.json"
DEFAULT_PAIR_IDS = ["shrikhande-vs-rook", "cfi-k4-parity-twist", "cfi-k5-parity-twist", "cycle-vs-chorded-cycle"]


@dataclass(frozen=True)
class CollectiveObservableRecord:
    id: str
    pair_id: str
    observable_name: str
    register_count: int
    tuple_count: int
    evaluated: bool
    distinguishes: bool
    classical_shadow: str
    value_a: str
    value_b: str
    bond_dimension_or_rank: int | None
    status: str
    interpretation: str
    required_next_step: str


@dataclass(frozen=True)
class PairCollectiveAudit:
    pair: GraphPairSpec
    observable_records: list[CollectiveObservableRecord]
    boundary_status: str
    falsifiers_triggered: list[str]


@dataclass(frozen=True)
class CollectiveObservableSearchResult:
    created_at: str
    tuple_cap: int
    pair_audits: list[PairCollectiveAudit]
    headline_metrics: dict[str, int]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def graph_pair_matrices(pair_id: str) -> tuple[GraphPairSpec, np.ndarray, np.ndarray]:
    if pair_id == "shrikhande-vs-rook":
        return (
            GraphPairSpec(
                id=pair_id,
                graph_a="Shrikhande graph",
                graph_b="4x4 rook graph",
                vertex_count=16,
                known_nonisomorphic=True,
                reason="Standard non-isomorphic strongly regular pair with identical parameters (16,6,2,2).",
            ),
            shrikhande_graph(),
            rook_graph_4x4(),
        )
    if pair_id == "cycle-vs-chorded-cycle":
        return (
            GraphPairSpec(
                id=pair_id,
                graph_a="Cycle graph C16",
                graph_b="C16 with distance-2 chords",
                vertex_count=16,
                known_nonisomorphic=True,
                reason="Control pair that classical invariants should distinguish immediately.",
            ),
            cycle_graph(16),
            chorded_cycle_graph(16),
        )
    if pair_id == "cfi-k4-parity-twist" or (pair_id.startswith("cfi-k") and pair_id.endswith("-parity-twist")):
        base_size = 4 if pair_id == "cfi-k4-parity-twist" else int(pair_id.split("-")[1][1:])
        graph_a = cfi_parity_graph_complete(base_size, twisted_edge=None)
        graph_b = cfi_parity_graph_complete(base_size, twisted_edge=(0, 1))
        return (
            GraphPairSpec(
                id=pair_id,
                graph_a=f"Untwisted CFI-style parity graph over K{base_size}",
                graph_b=f"Single-edge twisted CFI-style parity graph over K{base_size}",
                vertex_count=int(graph_a.shape[0]),
                known_nonisomorphic=True,
                reason=(
                    "CFI-style parity obstruction: low-dimensional WL and spectral checks are expected to fail "
                    "before high-register or exact methods see the twist."
                ),
            ),
            graph_a,
            graph_b,
        )
    raise ValueError(f"unknown graph pair: {pair_id}")


def _short(value: Any, limit: int = 360) -> str:
    text = str(value)
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."


def _make_record(
    pair_id: str,
    observable_id: str,
    observable_name: str,
    register_count: int,
    tuple_count: int,
    evaluated: bool,
    classical_shadow: str,
    value_a: Any,
    value_b: Any,
    bond_dimension_or_rank: int | None = None,
) -> CollectiveObservableRecord:
    if not evaluated:
        status = "skipped-scaling-cap"
        distinguishes = False
        interpretation = (
            f"{observable_name} was skipped because {tuple_count} tuples exceed the cap; "
            "a useful next step needs an implicit/tensor representation rather than brute-force tuple enumeration."
        )
        next_step = "Replace brute-force tuple enumeration with an invariant tensor-network or representation-theoretic ansatz."
    else:
        distinguishes = value_a != value_b
        if distinguishes:
            status = "classical-shadow-collapse"
            interpretation = (
                f"{observable_name} separates this pair, but the signal is exactly mirrored by {classical_shadow}; "
                "this is dequantization evidence, not a quantum advantage signal."
            )
            next_step = "Reject this observable as positive evidence and search for measurements not expressible by the named classical shadow."
        else:
            status = "no-signal"
            interpretation = (
                f"{observable_name} has matching signatures.  This gives no separating evidence for the coset-state candidate."
            )
            next_step = "Escalate to a more structured collective observable only if it comes with cost and classical-shadow accounting."

    return CollectiveObservableRecord(
        id=f"OBS-{pair_id}-{observable_id}",
        pair_id=pair_id,
        observable_name=observable_name,
        register_count=register_count,
        tuple_count=tuple_count,
        evaluated=evaluated,
        distinguishes=distinguishes,
        classical_shadow=classical_shadow,
        value_a=_short(value_a),
        value_b=_short(value_b),
        bond_dimension_or_rank=bond_dimension_or_rank,
        status=status,
        interpretation=interpretation,
        required_next_step=next_step,
    )


def relation_density_signature(adjacency: np.ndarray) -> tuple[tuple[str, int], ...]:
    n = int(adjacency.shape[0])
    directed_edges = int(adjacency.sum())
    loops = n
    non_edges = n * n - loops - directed_edges
    return (("loop", loops), ("edge", directed_edges), ("non_edge", non_edges))


def low_rank_walk_sketch(adjacency: np.ndarray, max_power: int = 6) -> tuple[int, tuple[float, ...]]:
    matrices = []
    current = np.eye(adjacency.shape[0], dtype=float)
    for _ in range(max_power + 1):
        matrices.append(current.reshape(-1))
        current = current @ adjacency
    stacked = np.vstack(matrices)
    singular_values = np.linalg.svd(stacked, compute_uv=False)
    rounded = tuple(float(round(value, 6)) for value in singular_values[: max_power + 1])
    return int(np.linalg.matrix_rank(stacked, tol=1e-8)), rounded


def build_observable_records(pair_id: str, graph_a: np.ndarray, graph_b: np.ndarray, tuple_cap: int) -> list[CollectiveObservableRecord]:
    n = int(graph_a.shape[0])
    rank_a = coherent_adjacency_algebra_rank(graph_a, max_power=6)
    rank_b = coherent_adjacency_algebra_rank(graph_b, max_power=6)
    sketch_a = low_rank_walk_sketch(graph_a)
    sketch_b = low_rank_walk_sketch(graph_b)
    records = [
        _make_record(
            pair_id,
            "spectral-moment-tensor",
            "Spectral moment tensor observable",
            1,
            n,
            True,
            "adjacency spectrum and closed-walk counts",
            (spectrum_signature(graph_a), walk_count_signature(graph_a, max_length=8)),
            (spectrum_signature(graph_b), walk_count_signature(graph_b, max_length=8)),
        ),
        _make_record(
            pair_id,
            "adjacency-algebra-rank",
            "Two-register adjacency-algebra rank observable",
            2,
            n * n,
            True,
            "coherent adjacency algebra rank",
            rank_a,
            rank_b,
            bond_dimension_or_rank=max(rank_a, rank_b),
        ),
        _make_record(
            pair_id,
            "two-register-relation-density",
            "Two-register relation-density observable",
            2,
            n * n,
            True,
            "degree/edge-count invariant",
            relation_density_signature(graph_a),
            relation_density_signature(graph_b),
        ),
        _make_record(
            pair_id,
            "two-register-wl-colors",
            "Two-register WL relation-color observable",
            2,
            n * n,
            True,
            "2-WL color refinement",
            wl2_signature(graph_a),
            wl2_signature(graph_b),
        ),
        _make_record(
            pair_id,
            "low-rank-walk-sketch",
            "Low-rank walk tensor sketch",
            2,
            n * n,
            True,
            "bounded-rank walk algebra contraction",
            sketch_a,
            sketch_b,
            bond_dimension_or_rank=max(sketch_a[0], sketch_b[0]),
        ),
    ]

    tuple_count_3 = n**3
    records.append(
        _make_record(
            pair_id,
            "three-register-wl-colors",
            "Three-register tuple-color observable",
            3,
            tuple_count_3,
            tuple_count_3 <= tuple_cap,
            "3-WL tuple refinement",
            wl_k_signature(graph_a, k=3) if tuple_count_3 <= tuple_cap else "skipped",
            wl_k_signature(graph_b, k=3) if tuple_count_3 <= tuple_cap else "skipped",
        )
    )

    tuple_count_4 = n**4
    records.append(
        _make_record(
            pair_id,
            "four-register-wl-boundary",
            "Four-register WL boundary observable",
            4,
            tuple_count_4,
            tuple_count_4 <= tuple_cap,
            "4-WL tuple refinement",
            wl_k_signature(graph_a, k=4, rounds=3) if tuple_count_4 <= tuple_cap else "skipped",
            wl_k_signature(graph_b, k=4, rounds=3) if tuple_count_4 <= tuple_cap else "skipped",
        )
    )
    return records


def audit_collective_observables(pair_id: str, tuple_cap: int = 120_000) -> PairCollectiveAudit:
    spec, graph_a, graph_b = graph_pair_matrices(pair_id)
    base_audit = audit_graph_pair(pair_id)
    records = build_observable_records(pair_id, graph_a, graph_b, tuple_cap)
    shadow_count = sum(1 for item in records if item.status == "classical-shadow-collapse")
    nonclassical_count = sum(1 for item in records if item.status == "nonclassical-candidate-needs-proof")
    skipped_count = sum(1 for item in records if item.status == "skipped-scaling-cap")
    evaluated_distinguishers = [item for item in records if item.evaluated and item.distinguishes]

    falsifiers: list[str] = []
    if shadow_count:
        falsifiers.append("A searched collective observable separates only through a known classical shadow.")
    if spec.known_nonisomorphic and not evaluated_distinguishers:
        falsifiers.append("Known non-isomorphic boundary pair has no implemented separating low-rank collective observable.")
    if skipped_count:
        falsifiers.append("Higher-register brute-force observable search hit the tuple cap; implicit tensor machinery is required.")
    falsifiers.extend(base_audit.falsifiers_triggered)

    if nonclassical_count:
        status = "nonclassical-candidate-needs-proof"
    elif shadow_count:
        status = "classical-shadow-collapse"
    elif spec.known_nonisomorphic:
        status = "boundary-no-current-observable"
    else:
        status = "no-signal"

    return PairCollectiveAudit(spec, records, status, sorted(set(falsifiers)))


def run_collective_observable_search(
    pair_ids: list[str] | None = None,
    tuple_cap: int = 120_000,
) -> CollectiveObservableSearchResult:
    active_pairs = pair_ids or DEFAULT_PAIR_IDS
    audits = [audit_collective_observables(pair_id, tuple_cap=tuple_cap) for pair_id in active_pairs]
    records = [record for audit in audits for record in audit.observable_records]
    metrics = {
        "pair_count": len(audits),
        "observable_count": len(records),
        "classical_shadow_collapse_count": sum(1 for record in records if record.status == "classical-shadow-collapse"),
        "no_signal_count": sum(1 for record in records if record.status == "no-signal"),
        "skipped_scaling_count": sum(1 for record in records if record.status == "skipped-scaling-cap"),
        "nonclassical_candidate_count": sum(1 for record in records if record.status == "nonclassical-candidate-needs-proof"),
        "boundary_pair_count": sum(1 for audit in audits if audit.boundary_status == "boundary-no-current-observable"),
        "classical_shadow_pair_count": sum(1 for audit in audits if audit.boundary_status == "classical-shadow-collapse"),
        "cfi_pair_count": sum(1 for audit in audits if audit.pair.id.startswith("cfi-")),
        "max_vertex_count": max((audit.pair.vertex_count for audit in audits), default=0),
        "max_register_count_evaluated": max((record.register_count for record in records if record.evaluated), default=0),
    }
    if metrics["nonclassical_candidate_count"]:
        status = "needs-proof-gate-review"
    elif metrics["boundary_pair_count"]:
        status = "blocked-needs-new-collective-observable"
    elif metrics["classical_shadow_collapse_count"]:
        status = "blocked-by-classical-shadow-collapse"
    else:
        status = "no-separating-signal"
    summary = (
        f"Searched {metrics['observable_count']} low-register collective observables across {metrics['pair_count']} graph pairs. "
        f"{metrics['classical_shadow_collapse_count']} separating signal(s) collapse to classical shadows; "
        f"{metrics['boundary_pair_count']} boundary pair(s) remain without an implemented nonclassical separator; "
        f"{metrics['skipped_scaling_count']} high-register probe(s) hit scaling caps."
    )
    falsifiers = sorted({item for audit in audits for item in audit.falsifiers_triggered})
    return CollectiveObservableSearchResult(utc_now(), tuple_cap, audits, metrics, status, summary, falsifiers)


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
    if isinstance(value, np.floating):
        return float(value)
    if isinstance(value, np.bool_):
        return bool(value)
    return value


def _safe_id(value: str) -> str:
    return "".join(ch if ch.isalnum() else "_" for ch in value.upper()).strip("_")


def write_collective_observable_negative_results(result: CollectiveObservableSearchResult) -> int:
    written = 0
    for audit in result.pair_audits:
        for record in audit.observable_records:
            if record.status != "classical-shadow-collapse":
                continue
            upsert_negative_result(
                NegativeResultRecord(
                    id=f"COSET-OBSERVABLE-SHADOW-{_safe_id(record.pair_id)}-{_safe_id(record.observable_name)}",
                    source="collective_observable_search.py",
                    claim=f"{record.observable_name} supplies nonclassical evidence for {record.pair_id}.",
                    reason_invalid=(
                        f"The observable distinguishes the pair but collapses to the classical shadow: {record.classical_shadow}."
                    ),
                    lesson=(
                        "A collective coset-state observable is not useful if the same separator is a WL, spectral, walk-count, "
                        "or bounded tensor-contraction invariant."
                    ),
                    applies_to=["CODE-COSET-COLLECTIVE", "HYP-LIT-COSET-OBSERVABLES", "PO-DEQUANTIZATION", "PO-MEASUREMENT"],
                    evidence={
                        "pair_id": record.pair_id,
                        "observable_id": record.id,
                        "register_count": record.register_count,
                        "classical_shadow": record.classical_shadow,
                        "status": record.status,
                    },
                )
            )
            written += 1
    return written


def write_collective_observable_search(
    output_path: Path = COLLECTIVE_OBSERVABLE_SEARCH_PATH,
    pair_ids: list[str] | None = None,
    tuple_cap: int = 120_000,
    write_registry: bool = True,
    registry_experiment_id: str = "EXP-COSET-COLLECTIVE-OBSERVABLE-SEARCH",
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "RESULT-COSET-COLLECTIVE-OBSERVABLE-SEARCH-LATEST",
) -> dict[str, Any]:
    result = run_collective_observable_search(pair_ids=pair_ids, tuple_cap=tuple_cap)
    payload = _json_ready(result)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    if write_registry:
        negative_results_written = write_collective_observable_negative_results(result)
        metrics = dict(result.headline_metrics)
        metrics["negative_results_written"] = negative_results_written
        falsifiers = list(result.falsifiers_triggered)
        if metrics["classical_shadow_collapse_count"]:
            falsifiers.append("At least one searched observable is fully explained by a classical invariant shadow.")
        if metrics["boundary_pair_count"]:
            falsifiers.append("Boundary CFI/coset pairs still lack an implemented nonclassical collective separator.")
        if metrics["skipped_scaling_count"]:
            falsifiers.append("Brute-force high-register observable search exceeded tuple caps.")
        upsert_experiment_result(
            ExperimentResultRecord(
                id=registry_result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=result.created_at,
                status=result.status,
                summary=result.summary,
                metrics=metrics,
                falsifiers_triggered=sorted(set(falsifiers)),
                artifacts={"collective_observable_search": str(output_path)},
            )
        )
    return payload
