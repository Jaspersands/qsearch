"""Exact small-instance code-equivalence resolver via incidence graphs.

For a binary linear code C, form a colored bipartite graph with one vertex for
every codeword, one vertex for every coordinate, and incidence edges for the
support of each codeword.  Two such graphs are color-preserving isomorphic if
and only if the codes are equivalent under a coordinate permutation.  This is
an exact finite-instance resolver, not an efficient asymptotic algorithm: the
graph has 2^k codeword vertices and graph-isomorphism search can still be hard.

The resolver targets proof-debt rows emitted by the rank-metric and
quasi-cyclic searches.  Every positive isomorphism result is independently
verified by applying the recovered coordinate permutation to the full codeword
set.  Caps and timeouts remain proof debt rather than evidence.
"""

from __future__ import annotations

import json
import signal
import threading
import time
from collections import Counter
from dataclasses import asdict, dataclass, is_dataclass
from pathlib import Path
from typing import Any

import networkx as nx
import numpy as np

from code_equivalence_workbench import gf2_rank, permute_codeword_set
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


CODE_EQUIVALENCE_DIR = Path("research/code_equivalence")
CODE_INCIDENCE_RESOLVER_PATH = CODE_EQUIVALENCE_DIR / "code_incidence_resolver.json"
RANK_METRIC_CODE_SEARCH_PATH = CODE_EQUIVALENCE_DIR / "rank_metric_code_search.json"
QUASI_CYCLIC_CODE_SEARCH_PATH = CODE_EQUIVALENCE_DIR / "quasi_cyclic_code_search.json"
QC_CANONICALIZATION_PATH = CODE_EQUIVALENCE_DIR / "quasi_cyclic_canonicalization.json"
QC_INFORMATION_SET_RESOLVER_PATH = CODE_EQUIVALENCE_DIR / "qc_information_set_resolver.json"


@dataclass(frozen=True)
class CodeIncidenceInput:
    id: str
    source: str
    source_family_id: str
    triage_row_id: str
    row_family: str
    source_status: str
    generator_a: list[list[int]]
    generator_b: list[list[int]]


@dataclass(frozen=True)
class IncidenceIsomorphismWitness:
    evaluated: bool
    equivalent: bool | None
    verification_passed: bool | None
    timed_out: bool
    skip_reason: str | None
    algorithm: str
    dimension_a: int
    dimension_b: int
    length_a: int
    length_b: int
    codeword_count_a: int
    codeword_count_b: int
    node_count_a: int
    node_count_b: int
    edge_count_a: int
    edge_count_b: int
    coordinate_permutation: list[int] | None
    search_seconds: float
    cost_model: str
    interpretation: str


@dataclass(frozen=True)
class CodeIncidenceRecord:
    id: str
    source: str
    source_family_id: str
    triage_row_id: str
    row_family: str
    source_status: str
    witness: IncidenceIsomorphismWitness
    status: str
    interpretation: str


@dataclass(frozen=True)
class CodeIncidenceFamilyRecord:
    triage_row_id: str
    row_family: str
    sources: list[str]
    pair_count: int
    equivalent_control_count: int
    exact_rejection_count: int
    proof_debt_count: int
    status: str
    interpretation: str


@dataclass(frozen=True)
class CodeIncidenceResolverReport:
    created_at: str
    records: list[CodeIncidenceRecord]
    family_records: list[CodeIncidenceFamilyRecord]
    max_codewords: int
    max_search_seconds: float
    headline_metrics: dict[str, int | float]
    status: str
    summary: str
    falsifiers_triggered: list[str]


class _IncidenceSearchTimeout(RuntimeError):
    pass


def _read_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text())
    except (json.JSONDecodeError, OSError):
        return fallback


def _row_basis(generator: np.ndarray) -> np.ndarray:
    values = np.asarray(generator, dtype=np.uint8).copy() & 1
    if values.ndim != 2:
        raise ValueError("generator must be a two-dimensional binary matrix")
    rows, cols = values.shape
    rank = 0
    for col in range(cols):
        pivot = next((row for row in range(rank, rows) if values[row, col]), None)
        if pivot is None:
            continue
        if pivot != rank:
            values[[rank, pivot]] = values[[pivot, rank]]
        for row in range(rows):
            if row != rank and values[row, col]:
                values[row] ^= values[rank]
        rank += 1
        if rank == rows:
            break
    return values[:rank]


def _codeword_set_from_basis(basis: np.ndarray) -> frozenset[int]:
    dimension, length = basis.shape
    row_values: list[int] = []
    for row in basis:
        value = 0
        for coordinate, bit in enumerate(row.tolist()):
            if bit:
                value |= 1 << coordinate
        row_values.append(value)
    words = set()
    for mask in range(1 << dimension):
        word = 0
        for row, value in enumerate(row_values):
            if (mask >> row) & 1:
                word ^= value
        words.add(word)
    if len(words) != 1 << dimension:
        raise RuntimeError("row-basis codeword enumeration produced duplicates")
    return frozenset(words)


def _coordinate_support_profiles(words: frozenset[int], length: int) -> list[tuple[tuple[int, int], ...]]:
    profiles: list[tuple[tuple[int, int], ...]] = []
    for coordinate in range(length):
        counts = Counter(word.bit_count() for word in words if (word >> coordinate) & 1)
        profiles.append(tuple(sorted((int(weight), int(count)) for weight, count in counts.items())))
    return profiles


def _incidence_graph(
    words: frozenset[int],
    length: int,
) -> nx.Graph:
    profiles = _coordinate_support_profiles(words, length)
    graph = nx.Graph()
    for coordinate, profile in enumerate(profiles):
        graph.add_node(("coordinate", coordinate), color=("coordinate", profile))
    for word in sorted(words):
        support = [coordinate for coordinate in range(length) if (word >> coordinate) & 1]
        support_profile = tuple(sorted(profiles[coordinate] for coordinate in support))
        graph.add_node(("codeword", word), color=("codeword", word.bit_count(), support_profile))
        for coordinate in support:
            graph.add_edge(("codeword", word), ("coordinate", coordinate))
    return graph


def _structural_witness(
    left: np.ndarray,
    right: np.ndarray,
    interpretation: str,
) -> IncidenceIsomorphismWitness:
    return IncidenceIsomorphismWitness(
        evaluated=True,
        equivalent=False,
        verification_passed=True,
        timed_out=False,
        skip_reason=None,
        algorithm="length-rank structural precheck",
        dimension_a=gf2_rank(left),
        dimension_b=gf2_rank(right),
        length_a=int(left.shape[1]),
        length_b=int(right.shape[1]),
        codeword_count_a=1 << gf2_rank(left),
        codeword_count_b=1 << gf2_rank(right),
        node_count_a=0,
        node_count_b=0,
        edge_count_a=0,
        edge_count_b=0,
        coordinate_permutation=None,
        search_seconds=0.0,
        cost_model="Polynomial length/rank precheck; no incidence graph was constructed.",
        interpretation=interpretation,
    )


def _cap_witness(
    left: np.ndarray,
    right: np.ndarray,
    max_codewords: int,
) -> IncidenceIsomorphismWitness:
    dimension_a = gf2_rank(left)
    dimension_b = gf2_rank(right)
    count_a = 1 << dimension_a
    count_b = 1 << dimension_b
    return IncidenceIsomorphismWitness(
        evaluated=False,
        equivalent=None,
        verification_passed=None,
        timed_out=False,
        skip_reason="codeword-expansion-cap",
        algorithm="colored codeword-coordinate incidence graph plus NetworkX VF2",
        dimension_a=dimension_a,
        dimension_b=dimension_b,
        length_a=int(left.shape[1]),
        length_b=int(right.shape[1]),
        codeword_count_a=count_a,
        codeword_count_b=count_b,
        node_count_a=count_a + int(left.shape[1]),
        node_count_b=count_b + int(right.shape[1]),
        edge_count_a=0,
        edge_count_b=0,
        coordinate_permutation=None,
        search_seconds=0.0,
        cost_model=(
            f"Incidence expansion requires {max(count_a, count_b)} codeword vertices, exceeding cap {max_codewords}; "
            "the method is exponential in code dimension."
        ),
        interpretation="Exact incidence resolution was skipped at the expansion cap; the row remains proof debt.",
    )


def _run_graph_matcher(
    left_graph: nx.Graph,
    right_graph: nx.Graph,
    max_search_seconds: float,
) -> tuple[bool, dict[Any, Any], bool]:
    matcher = nx.algorithms.isomorphism.GraphMatcher(
        left_graph,
        right_graph,
        node_match=lambda left, right: left.get("color") == right.get("color"),
    )
    can_alarm = (
        max_search_seconds > 0
        and hasattr(signal, "SIGALRM")
        and threading.current_thread() is threading.main_thread()
    )
    previous_handler: Any = None
    previous_timer = (0.0, 0.0)
    if can_alarm:
        previous_handler = signal.getsignal(signal.SIGALRM)
        previous_timer = signal.getitimer(signal.ITIMER_REAL)

        def _timeout(_signum: int, _frame: Any) -> None:
            raise _IncidenceSearchTimeout

        signal.signal(signal.SIGALRM, _timeout)
        signal.setitimer(signal.ITIMER_REAL, max_search_seconds)
    try:
        equivalent = bool(matcher.is_isomorphic())
        return equivalent, dict(matcher.mapping) if equivalent else {}, False
    except _IncidenceSearchTimeout:
        return False, {}, True
    finally:
        if can_alarm:
            signal.setitimer(signal.ITIMER_REAL, 0)
            signal.signal(signal.SIGALRM, previous_handler)
            if previous_timer[0] > 0 or previous_timer[1] > 0:
                signal.setitimer(signal.ITIMER_REAL, previous_timer[0], previous_timer[1])


def exact_code_incidence_isomorphism(
    generator_a: np.ndarray,
    generator_b: np.ndarray,
    max_codewords: int = 4_096,
    max_search_seconds: float = 20.0,
) -> IncidenceIsomorphismWitness:
    left = _row_basis(np.asarray(generator_a, dtype=np.uint8) & 1)
    right = _row_basis(np.asarray(generator_b, dtype=np.uint8) & 1)
    if left.shape[1] != right.shape[1]:
        return _structural_witness(left, right, "Code lengths differ, so no coordinate-permutation equivalence exists.")
    if left.shape[0] != right.shape[0]:
        return _structural_witness(left, right, "Code dimensions differ, so no coordinate-permutation equivalence exists.")

    codeword_count = 1 << int(left.shape[0])
    if codeword_count > max_codewords:
        return _cap_witness(left, right, max_codewords)

    left_words = _codeword_set_from_basis(left)
    right_words = _codeword_set_from_basis(right)
    length = int(left.shape[1])
    left_graph = _incidence_graph(left_words, length)
    right_graph = _incidence_graph(right_words, length)
    started = time.perf_counter()
    equivalent, mapping, timed_out = _run_graph_matcher(left_graph, right_graph, max_search_seconds)
    elapsed = round(time.perf_counter() - started, 6)
    cost_model = (
        f"Expanded both [n={length}, k={left.shape[0]}] codes to {codeword_count} codeword vertices each; "
        "colored VF2 is exact on this finite graph but has no polynomial worst-case guarantee."
    )
    if timed_out:
        return IncidenceIsomorphismWitness(
            evaluated=False,
            equivalent=None,
            verification_passed=None,
            timed_out=True,
            skip_reason="graph-isomorphism-timeout",
            algorithm="support-colored codeword-coordinate incidence graph plus NetworkX VF2",
            dimension_a=int(left.shape[0]),
            dimension_b=int(right.shape[0]),
            length_a=length,
            length_b=length,
            codeword_count_a=codeword_count,
            codeword_count_b=codeword_count,
            node_count_a=left_graph.number_of_nodes(),
            node_count_b=right_graph.number_of_nodes(),
            edge_count_a=left_graph.number_of_edges(),
            edge_count_b=right_graph.number_of_edges(),
            coordinate_permutation=None,
            search_seconds=elapsed,
            cost_model=cost_model,
            interpretation="Exact incidence-graph search timed out; this is unresolved proof debt, not hardness evidence.",
        )

    coordinate_permutation: list[int] | None = None
    verification_passed = True
    if equivalent:
        coordinate_permutation = []
        for coordinate in range(length):
            image = mapping.get(("coordinate", coordinate))
            if not isinstance(image, tuple) or len(image) != 2 or image[0] != "coordinate":
                verification_passed = False
                coordinate_permutation = None
                break
            coordinate_permutation.append(int(image[1]))
        if coordinate_permutation is not None:
            verification_passed = (
                len(set(coordinate_permutation)) == length
                and permute_codeword_set(left_words, length, coordinate_permutation) == right_words
            )

    interpretation = (
        "A color-preserving incidence-graph isomorphism yielded a coordinate permutation that was verified against "
        "the complete codeword sets."
        if equivalent and verification_passed
        else "The complete colored incidence graphs are non-isomorphic, so the codes are not coordinate-permutation equivalent."
        if not equivalent
        else "The graph matcher reported an isomorphism, but the recovered coordinate permutation failed verification."
    )
    return IncidenceIsomorphismWitness(
        evaluated=True,
        equivalent=equivalent if verification_passed else None,
        verification_passed=verification_passed,
        timed_out=False,
        skip_reason=None if verification_passed else "witness-verification-failed",
        algorithm="support-colored codeword-coordinate incidence graph plus NetworkX VF2",
        dimension_a=int(left.shape[0]),
        dimension_b=int(right.shape[0]),
        length_a=length,
        length_b=length,
        codeword_count_a=codeword_count,
        codeword_count_b=codeword_count,
        node_count_a=left_graph.number_of_nodes(),
        node_count_b=right_graph.number_of_nodes(),
        edge_count_a=left_graph.number_of_edges(),
        edge_count_b=right_graph.number_of_edges(),
        coordinate_permutation=coordinate_permutation if verification_passed else None,
        search_seconds=elapsed,
        cost_model=cost_model,
        interpretation=interpretation,
    )


def _rank_metric_inputs(path: Path = RANK_METRIC_CODE_SEARCH_PATH) -> list[CodeIncidenceInput]:
    payload = _read_json(path, {})
    inputs: list[CodeIncidenceInput] = []
    for family in payload.get("records", []):
        family_id = str(family.get("spec", {}).get("id", "unknown-rank-metric-family"))
        for audit in family.get("collision_audits", []):
            status = str(audit.get("status", ""))
            if "proof-debt" not in status or not audit.get("generator_a") or not audit.get("generator_b"):
                continue
            inputs.append(
                CodeIncidenceInput(
                    id=str(audit.get("id", "unknown-rank-metric-row")),
                    source="rank_metric_code_search",
                    source_family_id=family_id,
                    triage_row_id=f"rank-metric-family-{family_id}",
                    row_family="binary-expanded-rank-metric-family",
                    source_status=status,
                    generator_a=audit["generator_a"],
                    generator_b=audit["generator_b"],
                )
            )
    return inputs


def _quasi_cyclic_inputs(
    search_path: Path = QUASI_CYCLIC_CODE_SEARCH_PATH,
    canonicalization_path: Path = QC_CANONICALIZATION_PATH,
    information_set_path: Path = QC_INFORMATION_SET_RESOLVER_PATH,
) -> list[CodeIncidenceInput]:
    search = _read_json(search_path, {})
    canonicalization = _read_json(canonicalization_path, {})
    information_set = _read_json(information_set_path, {})
    already_resolved = {
        str(record.get("id"))
        for record in information_set.get("records", [])
        if str(record.get("status", ""))
        in {
            "equivalent-control-under-information-set-canonicalization",
            "rejected-by-information-set-canonicalization",
        }
    }
    debt_status = {
        str(record.get("id")): str(record.get("status", ""))
        for record in canonicalization.get("records", [])
        if "proof-debt" in str(record.get("status", ""))
    }
    inputs: list[CodeIncidenceInput] = []
    for family in search.get("records", []):
        family_id = str(family.get("spec", {}).get("id", "unknown-qc-family"))
        for audit in family.get("collision_audits", []):
            audit_id = str(audit.get("id", ""))
            if (
                audit_id not in debt_status
                or audit_id in already_resolved
                or not audit.get("generator_a")
                or not audit.get("generator_b")
            ):
                continue
            inputs.append(
                CodeIncidenceInput(
                    id=audit_id,
                    source="quasi_cyclic_canonicalization",
                    source_family_id=family_id,
                    triage_row_id=f"qc-family-{family_id}",
                    row_family="quasi-cyclic-family",
                    source_status=debt_status[audit_id],
                    generator_a=audit["generator_a"],
                    generator_b=audit["generator_b"],
                )
            )
    return inputs


def load_code_incidence_inputs(
    include_rank_metric: bool = True,
    include_quasi_cyclic: bool = True,
) -> list[CodeIncidenceInput]:
    inputs: list[CodeIncidenceInput] = []
    if include_rank_metric:
        inputs.extend(_rank_metric_inputs())
    if include_quasi_cyclic:
        inputs.extend(_quasi_cyclic_inputs())
    deduplicated: dict[tuple[str, str], CodeIncidenceInput] = {}
    for item in inputs:
        deduplicated[(item.source, item.id)] = item
    return [deduplicated[key] for key in sorted(deduplicated)]


def audit_code_incidence_input(
    item: CodeIncidenceInput,
    max_codewords: int = 4_096,
    max_search_seconds: float = 20.0,
) -> CodeIncidenceRecord:
    witness = exact_code_incidence_isomorphism(
        np.asarray(item.generator_a, dtype=np.uint8),
        np.asarray(item.generator_b, dtype=np.uint8),
        max_codewords=max_codewords,
        max_search_seconds=max_search_seconds,
    )
    if witness.evaluated and witness.equivalent is True and witness.verification_passed:
        status = "equivalent-control-under-exact-incidence-isomorphism"
        interpretation = (
            "Exact codeword-coordinate incidence isomorphism proves this proof-debt row is an equivalent control; "
            "the recovered coordinate permutation passed full-code verification."
        )
    elif witness.evaluated and witness.equivalent is False:
        status = "rejected-by-exact-incidence-isomorphism"
        interpretation = (
            "Exact colored incidence-graph search proves the small code pair is non-equivalent. This solves the finite "
            "decision row classically but supplies no asymptotic hardness evidence."
        )
    else:
        status = "incidence-isomorphism-proof-debt"
        interpretation = witness.interpretation
    return CodeIncidenceRecord(
        id=item.id,
        source=item.source,
        source_family_id=item.source_family_id,
        triage_row_id=item.triage_row_id,
        row_family=item.row_family,
        source_status=item.source_status,
        witness=witness,
        status=status,
        interpretation=interpretation,
    )


def _family_records(records: list[CodeIncidenceRecord]) -> list[CodeIncidenceFamilyRecord]:
    grouped: dict[tuple[str, str], list[CodeIncidenceRecord]] = {}
    for record in records:
        grouped.setdefault((record.triage_row_id, record.row_family), []).append(record)
    families: list[CodeIncidenceFamilyRecord] = []
    for (triage_row_id, row_family), rows in sorted(grouped.items()):
        controls = sum(1 for row in rows if row.status == "equivalent-control-under-exact-incidence-isomorphism")
        rejections = sum(1 for row in rows if row.status == "rejected-by-exact-incidence-isomorphism")
        proof_debt = sum(1 for row in rows if "proof-debt" in row.status)
        if proof_debt:
            status = "incidence-family-proof-debt"
            interpretation = (
                f"Exact incidence resolution handled {len(rows) - proof_debt} of {len(rows)} source proof-debt row(s); "
                f"{proof_debt} remain unresolved."
            )
        elif rejections:
            status = "incidence-family-dequantized-by-exact-isomorphism"
            interpretation = (
                f"Exact incidence resolution classically decided all {len(rows)} source proof-debt row(s): "
                f"{controls} equivalent control(s) and {rejections} non-equivalent finite-instance rejection(s)."
            )
        else:
            status = "incidence-family-all-equivalent-controls"
            interpretation = (
                f"Every one of the {len(rows)} source proof-debt row(s) is coordinate-permutation equivalent under "
                "an independently verified exact incidence-isomorphism witness."
            )
        families.append(
            CodeIncidenceFamilyRecord(
                triage_row_id=triage_row_id,
                row_family=row_family,
                sources=sorted({row.source for row in rows}),
                pair_count=len(rows),
                equivalent_control_count=controls,
                exact_rejection_count=rejections,
                proof_debt_count=proof_debt,
                status=status,
                interpretation=interpretation,
            )
        )
    return families


def run_code_incidence_resolver(
    inputs: list[CodeIncidenceInput] | None = None,
    max_codewords: int = 4_096,
    max_search_seconds: float = 20.0,
) -> CodeIncidenceResolverReport:
    selected = load_code_incidence_inputs() if inputs is None else inputs
    records = [
        audit_code_incidence_input(item, max_codewords=max_codewords, max_search_seconds=max_search_seconds)
        for item in selected
    ]
    families = _family_records(records)
    metrics: dict[str, int | float] = {
        "input_count": len(selected),
        "family_count": len(families),
        "evaluated_count": sum(1 for record in records if record.witness.evaluated),
        "equivalent_control_count": sum(
            1 for record in records if record.status == "equivalent-control-under-exact-incidence-isomorphism"
        ),
        "exact_rejection_count": sum(1 for record in records if record.status == "rejected-by-exact-incidence-isomorphism"),
        "proof_debt_count": sum(1 for record in records if "proof-debt" in record.status),
        "timeout_count": sum(1 for record in records if record.witness.timed_out),
        "expansion_cap_count": sum(1 for record in records if record.witness.skip_reason == "codeword-expansion-cap"),
        "verified_permutation_count": sum(
            1
            for record in records
            if record.witness.equivalent is True and record.witness.verification_passed is True
        ),
        "max_search_seconds_observed": max((record.witness.search_seconds for record in records), default=0.0),
    }
    if metrics["proof_debt_count"]:
        status = "code-incidence-resolver-proof-debt"
    elif records:
        status = "code-incidence-resolver-resolved"
    else:
        status = "code-incidence-resolver-no-inputs"
    summary = (
        f"Audited {metrics['input_count']} code proof-debt row(s) across {metrics['family_count']} family bucket(s) "
        f"with exact colored incidence isomorphism: {metrics['equivalent_control_count']} equivalent control(s), "
        f"{metrics['exact_rejection_count']} exact finite-instance rejection(s), and "
        f"{metrics['proof_debt_count']} unresolved row(s)."
    )
    falsifiers: list[str] = []
    if metrics["equivalent_control_count"]:
        falsifiers.append("Exact incidence isomorphism resolves some proof-debt rows as coordinate-permutation controls.")
    if metrics["exact_rejection_count"]:
        falsifiers.append("Exact incidence isomorphism classically decides some non-equivalent finite code rows.")
    if metrics["proof_debt_count"]:
        falsifiers.append("Expansion caps or exact-search timeouts remain proof debt and cannot support a speedup claim.")
    if not records:
        falsifiers.append("No supported code proof-debt rows were available for exact incidence resolution.")
    return CodeIncidenceResolverReport(
        utc_now(),
        records,
        families,
        max_codewords,
        max_search_seconds,
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
    return "".join(character if character.isalnum() else "_" for character in value.upper()).strip("_")


def write_code_incidence_negative_results(report: CodeIncidenceResolverReport) -> int:
    written = 0
    for record in report.records:
        if record.status not in {
            "equivalent-control-under-exact-incidence-isomorphism",
            "rejected-by-exact-incidence-isomorphism",
        }:
            continue
        upsert_negative_result(
            NegativeResultRecord(
                id=f"CODE-INCIDENCE-RESOLVED-{_safe_id(record.source)}-{_safe_id(record.id)}",
                source="code_incidence_resolver.py",
                claim=f"{record.id} supplies unresolved hard code-equivalence evidence for a collective coset measurement.",
                reason_invalid=record.interpretation,
                lesson=(
                    "Small code rows must survive exact full-code incidence isomorphism when dimension permits it. "
                    "A cap or timeout is proof debt; an exact control or decision is negative evidence."
                ),
                applies_to=["CODE-COSET-COLLECTIVE", "PO-DEQUANTIZATION", "PO-FALSIFIERS"],
                evidence=asdict(record),
            )
        )
        written += 1
    return written


def write_code_incidence_resolver(
    output_path: Path = CODE_INCIDENCE_RESOLVER_PATH,
    inputs: list[CodeIncidenceInput] | None = None,
    max_codewords: int = 4_096,
    max_search_seconds: float = 20.0,
    write_registry: bool = True,
    registry_experiment_id: str = "EXP-CODE-INCIDENCE-ISOMORPHISM-RESOLVER",
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "RESULT-CODE-INCIDENCE-ISOMORPHISM-RESOLVER-LATEST",
) -> dict[str, Any]:
    report = run_code_incidence_resolver(
        inputs=inputs,
        max_codewords=max_codewords,
        max_search_seconds=max_search_seconds,
    )
    payload = _json_ready(report)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    negative_results_written = 0
    if write_registry:
        negative_results_written = write_code_incidence_negative_results(report)
        metrics = dict(payload["headline_metrics"])
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
                artifacts={"code_incidence_resolver": str(output_path)},
            )
        )
    payload["negative_results_written"] = negative_results_written
    return payload
