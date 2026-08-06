"""Automorphism certificates for the scalable self-dual code tail.

For a binary self-dual code C with generator G, the rows of G are also a
parity check.  A coordinate subset S is therefore the support of a codeword
exactly when the XOR of the corresponding columns of G is zero.

This module enumerates every support of weight at most 2t by grouping column
subsets of size at most t by their XOR.  It then builds the colored incidence
graph between coordinates and the resulting low-weight supports.

Every permutation automorphism of C acts on this graph.  Consequently:

* singleton stable colors on all coordinate vertices are a sound polynomial
  rigidity certificate for that instance;
* a graph automorphism is only an automorphism candidate and is promoted only
  after full rowspace verification;
* a non-singleton color partition, timeout, cap, or spurious graph
  automorphism remains proof debt.

The fixed-weight support enumeration is polynomial for fixed t.  It does not
prove an asymptotic family theorem when the distinguishing weight must grow.
"""

from __future__ import annotations

import itertools
import json
import math
import signal
import time
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import networkx as nx
import numpy as np

from code_equivalence_workbench import gf2_rank
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from self_dual_code_boundary_search import SELF_DUAL_CODE_BOUNDARY_PATH
from self_dual_rowspace_hsp_reduction import canonical_rowspace


SELF_DUAL_AUTOMORPHISM_PATH = Path(
    "research/code_equivalence/self_dual_automorphism_workbench.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-CODE-SELF-DUAL-AUTOMORPHISM-WORKBENCH"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class SelfDualAutomorphismSpec:
    minimum_dimension: int = 16
    half_support_order: int = 4
    maximum_bucket_pairs: int = 2_000_000
    maximum_incidence_nodes: int = 2_000
    graph_search_seconds: float = 15.0


@dataclass(frozen=True)
class LowWeightSupportCertificate:
    complete: bool
    self_dual_check_passed: bool
    maximum_weight: int
    enumerated_half_subsets: int
    equal_syndrome_pair_count: int
    support_count: int
    weight_spectrum: list[list[int]]
    cap_reason: str | None


@dataclass(frozen=True)
class CoordinateRefinementCertificate:
    evaluated: bool
    iteration_count: int
    coordinate_color_class_count: int
    singleton_coordinate_count: int
    maximum_coordinate_color_class_size: int
    all_coordinates_singleton: bool


@dataclass(frozen=True)
class IncidenceAutomorphismSearch:
    evaluated: bool
    exhausted: bool
    timed_out: bool
    nonidentity_graph_automorphism_found: bool
    full_code_automorphism_verified: bool
    moved_coordinate_count: int | None
    coordinate_permutation: list[int] | None
    search_seconds: float
    interpretation: str


@dataclass(frozen=True)
class SelfDualAutomorphismRecord:
    family_id: str
    instance_id: str
    dimension: int
    length: int
    low_weight_supports: LowWeightSupportCertificate
    refinement: CoordinateRefinementCertificate
    incidence_search: IncidenceAutomorphismSearch
    rigidity_certified: bool
    explicit_nontrivial_automorphism_certified: bool
    automorphism_group_size: int | None
    minimal_degree: int | None
    gi_type_single_register_no_go_applicable: bool
    status: str
    interpretation: str


@dataclass(frozen=True)
class SelfDualAutomorphismFamilyRecord:
    family_id: str
    dimension: int
    length: int
    instance_count: int
    rigidity_certified_instance_count: int
    explicit_automorphism_instance_count: int
    unresolved_instance_count: int
    gi_type_single_register_no_go_instance_count: int
    status: str
    interpretation: str


@dataclass(frozen=True)
class SelfDualAutomorphismReport:
    created_at: str
    spec: SelfDualAutomorphismSpec
    theorem: dict[str, Any]
    records: list[SelfDualAutomorphismRecord]
    family_records: list[SelfDualAutomorphismFamilyRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


class _GraphSearchTimeout(RuntimeError):
    pass


def _read_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text())
    except (json.JSONDecodeError, OSError):
        return fallback


def _column_values(generator: np.ndarray) -> list[int]:
    matrix = np.asarray(generator, dtype=np.uint8) & 1
    return [
        sum(int(matrix[row, column]) << row for row in range(matrix.shape[0]))
        for column in range(matrix.shape[1])
    ]


def is_self_dual_generator(generator: np.ndarray) -> bool:
    matrix = np.asarray(generator, dtype=np.uint8) & 1
    dimension, length = matrix.shape
    return (
        length == 2 * dimension
        and gf2_rank(matrix) == dimension
        and not np.any((matrix @ matrix.T) & 1)
    )


def enumerate_bounded_weight_supports(
    generator: np.ndarray,
    half_support_order: int = 4,
    maximum_bucket_pairs: int = 2_000_000,
) -> tuple[set[int], LowWeightSupportCertificate]:
    matrix = np.asarray(generator, dtype=np.uint8) & 1
    dimension, length = matrix.shape
    self_dual = is_self_dual_generator(matrix)
    maximum_weight = 2 * half_support_order
    if not self_dual:
        return set(), LowWeightSupportCertificate(
            complete=False,
            self_dual_check_passed=False,
            maximum_weight=maximum_weight,
            enumerated_half_subsets=0,
            equal_syndrome_pair_count=0,
            support_count=0,
            weight_spectrum=[],
            cap_reason="generator-is-not-a-binary-self-dual-code",
        )

    columns = _column_values(matrix)
    buckets: dict[int, list[int]] = {}
    subset_count = 0
    for size in range(half_support_order + 1):
        for coordinates in itertools.combinations(range(length), size):
            syndrome = 0
            mask = 0
            for coordinate in coordinates:
                syndrome ^= columns[coordinate]
                mask |= 1 << coordinate
            buckets.setdefault(syndrome, []).append(mask)
            subset_count += 1

    pair_count = sum(math.comb(len(bucket), 2) for bucket in buckets.values())
    if pair_count > maximum_bucket_pairs:
        return set(), LowWeightSupportCertificate(
            complete=False,
            self_dual_check_passed=True,
            maximum_weight=maximum_weight,
            enumerated_half_subsets=subset_count,
            equal_syndrome_pair_count=pair_count,
            support_count=0,
            weight_spectrum=[],
            cap_reason=(
                f"equal-syndrome pair count {pair_count} exceeds cap "
                f"{maximum_bucket_pairs}"
            ),
        )

    supports: set[int] = set()
    for bucket in buckets.values():
        for right in range(len(bucket)):
            for left in range(right):
                support = bucket[left] ^ bucket[right]
                weight = support.bit_count()
                if 0 < weight <= maximum_weight:
                    supports.add(support)

    spectrum = Counter(mask.bit_count() for mask in supports)
    complete = all(
        _support_syndrome(mask, columns) == 0 for mask in supports
    )
    return supports, LowWeightSupportCertificate(
        complete=complete,
        self_dual_check_passed=True,
        maximum_weight=maximum_weight,
        enumerated_half_subsets=subset_count,
        equal_syndrome_pair_count=pair_count,
        support_count=len(supports),
        weight_spectrum=[
            [int(weight), int(count)] for weight, count in sorted(spectrum.items())
        ],
        cap_reason=None if complete else "generated-support-failed-zero-syndrome-check",
    )


def enumerate_bounded_weight_supports_packed(
    generator: np.ndarray,
    half_support_order: int = 5,
    maximum_bucket_pairs: int = 2_000_000,
) -> tuple[set[int], LowWeightSupportCertificate, int]:
    """Packed fixed-order enumeration for the current length-at-most-64 tail.

    Storing `(syndrome, support-mask)` records in a NumPy structured array
    avoids the per-object overhead of a Python dictionary at order five.
    """

    matrix = np.asarray(generator, dtype=np.uint8) & 1
    dimension, length = matrix.shape
    maximum_weight = 2 * half_support_order
    if not is_self_dual_generator(matrix):
        certificate = LowWeightSupportCertificate(
            complete=False,
            self_dual_check_passed=False,
            maximum_weight=maximum_weight,
            enumerated_half_subsets=0,
            equal_syndrome_pair_count=0,
            support_count=0,
            weight_spectrum=[],
            cap_reason="generator-is-not-a-binary-self-dual-code",
        )
        return set(), certificate, 0
    if dimension > 64 or length > 64:
        certificate = LowWeightSupportCertificate(
            complete=False,
            self_dual_check_passed=True,
            maximum_weight=maximum_weight,
            enumerated_half_subsets=0,
            equal_syndrome_pair_count=0,
            support_count=0,
            weight_spectrum=[],
            cap_reason="packed-enumerator-requires-dimension-and-length-at-most-64",
        )
        return set(), certificate, 0

    columns = _column_values(matrix)
    subset_count = sum(
        math.comb(length, size) for size in range(half_support_order + 1)
    )
    syndrome_dtype = "<u4" if dimension <= 32 else "<u8"
    records = np.empty(
        subset_count,
        dtype=np.dtype([("syndrome", syndrome_dtype), ("mask", "<u8")]),
    )
    position = 0
    for size in range(half_support_order + 1):
        for coordinates in itertools.combinations(range(length), size):
            syndrome = 0
            mask = 0
            for coordinate in coordinates:
                syndrome ^= columns[coordinate]
                mask |= 1 << coordinate
            records[position] = (syndrome, mask)
            position += 1
    if position != subset_count:
        raise RuntimeError("packed subset enumeration count mismatch")
    packed_bytes = int(records.nbytes)
    records.sort(order="syndrome", kind="quicksort")

    equal_neighbors = np.flatnonzero(
        records["syndrome"][1:] == records["syndrome"][:-1]
    )
    supports: set[int] = set()
    pair_count = 0
    visited_syndromes: set[int] = set()
    cap_reason: str | None = None
    for raw_index in equal_neighbors:
        index = int(raw_index)
        syndrome = int(records["syndrome"][index])
        if syndrome in visited_syndromes:
            continue
        visited_syndromes.add(syndrome)
        lower = index
        while (
            lower > 0
            and int(records["syndrome"][lower - 1]) == syndrome
        ):
            lower -= 1
        upper = index + 1
        while (
            upper + 1 < len(records)
            and int(records["syndrome"][upper + 1]) == syndrome
        ):
            upper += 1
        masks = records["mask"][lower : upper + 1]
        pair_count += math.comb(len(masks), 2)
        if pair_count > maximum_bucket_pairs:
            cap_reason = (
                f"equal-syndrome pair count exceeds cap "
                f"{maximum_bucket_pairs}"
            )
            break
        for right in range(len(masks)):
            for left in range(right):
                support = int(masks[left] ^ masks[right])
                weight = support.bit_count()
                if 0 < weight <= maximum_weight:
                    supports.add(support)
    del records

    complete = cap_reason is None and all(
        _support_syndrome(mask, columns) == 0 for mask in supports
    )
    if cap_reason is None and not complete:
        cap_reason = "generated-support-failed-zero-syndrome-check"
    spectrum = Counter(mask.bit_count() for mask in supports)
    certificate = LowWeightSupportCertificate(
        complete=complete,
        self_dual_check_passed=True,
        maximum_weight=maximum_weight,
        enumerated_half_subsets=subset_count,
        equal_syndrome_pair_count=pair_count,
        support_count=len(supports),
        weight_spectrum=[
            [int(weight), int(count)] for weight, count in sorted(spectrum.items())
        ],
        cap_reason=cap_reason,
    )
    return supports, certificate, packed_bytes


def _support_syndrome(mask: int, columns: list[int]) -> int:
    syndrome = 0
    for coordinate, column in enumerate(columns):
        if (mask >> coordinate) & 1:
            syndrome ^= column
    return syndrome


def low_weight_incidence_graph(supports: set[int], length: int) -> nx.Graph:
    graph = nx.Graph()
    for coordinate in range(length):
        graph.add_node(("coordinate", coordinate), side="coordinate", weight=0)
    for index, mask in enumerate(sorted(supports)):
        support_node = ("support", index)
        graph.add_node(
            support_node,
            side="support",
            weight=int(mask.bit_count()),
        )
        for coordinate in range(length):
            if (mask >> coordinate) & 1:
                graph.add_edge(("coordinate", coordinate), support_node)
    return graph


def stable_coordinate_refinement(
    graph: nx.Graph,
    length: int,
) -> CoordinateRefinementCertificate:
    if graph.number_of_nodes() < length:
        return CoordinateRefinementCertificate(
            evaluated=False,
            iteration_count=0,
            coordinate_color_class_count=0,
            singleton_coordinate_count=0,
            maximum_coordinate_color_class_size=0,
            all_coordinates_singleton=False,
        )
    ordered_nodes = sorted(graph.nodes, key=repr)
    colors: dict[Any, int] = {}
    initial = {
        node: (
            str(graph.nodes[node].get("side")),
            int(graph.nodes[node].get("weight", 0)),
        )
        for node in ordered_nodes
    }
    palette = {
        value: index for index, value in enumerate(sorted(set(initial.values())))
    }
    colors = {node: palette[value] for node, value in initial.items()}
    prior_partition: tuple[tuple[str, ...], ...] | None = None
    iterations = 0
    for _ in range(graph.number_of_nodes() + 1):
        classes: dict[int, list[str]] = {}
        for node in ordered_nodes:
            classes.setdefault(colors[node], []).append(repr(node))
        partition = tuple(
            sorted((tuple(sorted(nodes)) for nodes in classes.values()))
        )
        if partition == prior_partition:
            break
        prior_partition = partition
        signatures = {
            node: (
                colors[node],
                tuple(sorted(colors[neighbor] for neighbor in graph.neighbors(node))),
            )
            for node in ordered_nodes
        }
        signature_palette = {
            value: index
            for index, value in enumerate(sorted(set(signatures.values())))
        }
        colors = {node: signature_palette[value] for node, value in signatures.items()}
        iterations += 1

    coordinate_counts = Counter(
        colors[("coordinate", coordinate)] for coordinate in range(length)
    )
    return CoordinateRefinementCertificate(
        evaluated=True,
        iteration_count=iterations,
        coordinate_color_class_count=len(coordinate_counts),
        singleton_coordinate_count=sum(
            count == 1 for count in coordinate_counts.values()
        ),
        maximum_coordinate_color_class_size=max(coordinate_counts.values(), default=0),
        all_coordinates_singleton=(
            len(coordinate_counts) == length
            and all(count == 1 for count in coordinate_counts.values())
        ),
    )


def verify_coordinate_automorphism(
    generator: np.ndarray,
    permutation: list[int],
) -> bool:
    matrix = np.asarray(generator, dtype=np.uint8) & 1
    if sorted(permutation) != list(range(matrix.shape[1])):
        return False
    return np.array_equal(
        canonical_rowspace(matrix[:, permutation]),
        canonical_rowspace(matrix),
    )


def search_incidence_automorphism(
    generator: np.ndarray,
    graph: nx.Graph,
    maximum_nodes: int,
    search_seconds: float,
) -> IncidenceAutomorphismSearch:
    matrix = np.asarray(generator, dtype=np.uint8) & 1
    length = int(matrix.shape[1])
    if graph.number_of_nodes() > maximum_nodes:
        return IncidenceAutomorphismSearch(
            evaluated=False,
            exhausted=False,
            timed_out=False,
            nonidentity_graph_automorphism_found=False,
            full_code_automorphism_verified=False,
            moved_coordinate_count=None,
            coordinate_permutation=None,
            search_seconds=0.0,
            interpretation=(
                f"Incidence graph has {graph.number_of_nodes()} nodes, exceeding cap "
                f"{maximum_nodes}; keep automorphism status unresolved."
            ),
        )

    matcher = nx.algorithms.isomorphism.GraphMatcher(
        graph,
        graph,
        node_match=lambda left, right: (
            left.get("side") == right.get("side")
            and left.get("weight") == right.get("weight")
        ),
    )
    started = time.monotonic()
    timed_out = False
    exhausted = False
    permutation: list[int] | None = None
    verified = False

    def _alarm_handler(_signum: int, _frame: Any) -> None:
        raise _GraphSearchTimeout()

    can_alarm = (
        search_seconds > 0
        and hasattr(signal, "SIGALRM")
        and hasattr(signal, "setitimer")
    )
    previous_handler: Any = None
    try:
        if can_alarm:
            previous_handler = signal.signal(signal.SIGALRM, _alarm_handler)
            signal.setitimer(signal.ITIMER_REAL, search_seconds)
        for mapping in matcher.isomorphisms_iter():
            candidate = [
                int(mapping[("coordinate", coordinate)][1])
                for coordinate in range(length)
            ]
            if any(image != coordinate for coordinate, image in enumerate(candidate)):
                permutation = candidate
                verified = verify_coordinate_automorphism(matrix, candidate)
                break
        else:
            exhausted = True
    except _GraphSearchTimeout:
        timed_out = True
    finally:
        if can_alarm:
            signal.setitimer(signal.ITIMER_REAL, 0)
            signal.signal(signal.SIGALRM, previous_handler)

    elapsed = time.monotonic() - started
    moved = (
        sum(index != image for index, image in enumerate(permutation))
        if permutation is not None
        else None
    )
    if verified:
        interpretation = (
            "A nonidentity low-weight-incidence automorphism was independently "
            "verified on the full code rowspace."
        )
    elif permutation is not None:
        interpretation = (
            "The low-weight incidence graph has a nonidentity symmetry that does "
            "not preserve the full code; bounded-weight structure is insufficient."
        )
    elif exhausted:
        interpretation = (
            "Exact colored incidence search exhausted with only the identity; "
            "the complete bounded-weight support hypergraph certifies rigidity."
        )
    elif timed_out:
        interpretation = (
            "Exact incidence automorphism search timed out; this is unresolved "
            "proof debt, not a rigidity certificate."
        )
    else:
        interpretation = "No conclusive incidence automorphism result was produced."
    return IncidenceAutomorphismSearch(
        evaluated=True,
        exhausted=exhausted,
        timed_out=timed_out,
        nonidentity_graph_automorphism_found=permutation is not None,
        full_code_automorphism_verified=verified,
        moved_coordinate_count=moved,
        coordinate_permutation=permutation,
        search_seconds=round(elapsed, 6),
        interpretation=interpretation,
    )


def audit_self_dual_automorphism_instance(
    family_id: str,
    instance: dict[str, Any],
    spec: SelfDualAutomorphismSpec,
) -> SelfDualAutomorphismRecord:
    generator = np.asarray(instance["generator"], dtype=np.uint8)
    dimension, length = map(int, generator.shape)
    supports, support_certificate = enumerate_bounded_weight_supports(
        generator,
        half_support_order=spec.half_support_order,
        maximum_bucket_pairs=spec.maximum_bucket_pairs,
    )
    graph = low_weight_incidence_graph(supports, length)
    refinement = stable_coordinate_refinement(graph, length)
    if (
        support_certificate.complete
        and refinement.all_coordinates_singleton
    ):
        incidence = IncidenceAutomorphismSearch(
            evaluated=False,
            exhausted=False,
            timed_out=False,
            nonidentity_graph_automorphism_found=False,
            full_code_automorphism_verified=False,
            moved_coordinate_count=None,
            coordinate_permutation=None,
            search_seconds=0.0,
            interpretation=(
                "Stable automorphism-invariant colors are singleton on every "
                "coordinate, so exact graph search is unnecessary."
            ),
        )
        rigidity = True
        explicit_automorphism = False
    else:
        incidence = search_incidence_automorphism(
            generator,
            graph,
            maximum_nodes=spec.maximum_incidence_nodes,
            search_seconds=spec.graph_search_seconds,
        )
        rigidity = bool(
            support_certificate.complete
            and incidence.exhausted
            and not incidence.nonidentity_graph_automorphism_found
        )
        explicit_automorphism = bool(incidence.full_code_automorphism_verified)

    if rigidity:
        status = "rigidity-certified-by-bounded-weight-support-hypergraph"
        interpretation = (
            f"Complete weight<={support_certificate.maximum_weight} supports give "
            "an automorphism-invariant coordinate structure with trivial "
            "coordinate action. The rigid S_n hidden-shift bridge has the "
            "graph-isomorphism-style order-two form."
        )
    elif explicit_automorphism:
        status = "nonrigid-explicit-full-code-automorphism"
        interpretation = (
            "A nonidentity coordinate permutation from the bounded-weight support "
            "graph was verified against the complete rowspace. Use the full "
            "stabilizer HSP, not the rigid order-two special case."
        )
    else:
        status = "automorphism-proof-debt"
        interpretation = (
            "Bounded-weight support structure neither certifies rigidity nor "
            "produces a verified full-code automorphism. Increase support order "
            "or use an exact algebraic automorphism solver."
        )

    return SelfDualAutomorphismRecord(
        family_id=family_id,
        instance_id=str(instance.get("id", "unknown-self-dual-instance")),
        dimension=dimension,
        length=length,
        low_weight_supports=support_certificate,
        refinement=refinement,
        incidence_search=incidence,
        rigidity_certified=rigidity,
        explicit_nontrivial_automorphism_certified=explicit_automorphism,
        automorphism_group_size=1 if rigidity else None,
        minimal_degree=(
            incidence.moved_coordinate_count if explicit_automorphism else None
        ),
        gi_type_single_register_no_go_applicable=rigidity,
        status=status,
        interpretation=interpretation,
    )


def run_self_dual_automorphism_workbench(
    source_path: Path = SELF_DUAL_CODE_BOUNDARY_PATH,
    spec: SelfDualAutomorphismSpec = SelfDualAutomorphismSpec(),
) -> SelfDualAutomorphismReport:
    source = _read_json(source_path, {})
    records: list[SelfDualAutomorphismRecord] = []
    family_records: list[SelfDualAutomorphismFamilyRecord] = []
    for family in source.get("family_records", []):
        family_spec = family.get("spec", {})
        dimension = int(family_spec.get("dimension", 0) or 0)
        if dimension < spec.minimum_dimension:
            continue
        family_id = str(family_spec.get("id", "unknown-self-dual-family"))
        family_rows = [
            audit_self_dual_automorphism_instance(family_id, instance, spec)
            for instance in family.get("instances", [])
        ]
        records.extend(family_rows)
        rigid = sum(record.rigidity_certified for record in family_rows)
        nonrigid = sum(
            record.explicit_nontrivial_automorphism_certified
            for record in family_rows
        )
        unresolved = len(family_rows) - rigid - nonrigid
        no_go = sum(
            record.gi_type_single_register_no_go_applicable
            for record in family_rows
        )
        if rigid == len(family_rows) and family_rows:
            family_status = (
                "all-sampled-instances-rigidity-certified-single-register-no-go-proof-debt"
            )
        elif nonrigid == len(family_rows) and family_rows:
            family_status = "all-sampled-instances-explicitly-nonrigid-hsp-proof-debt"
        else:
            family_status = "mixed-or-unresolved-automorphism-proof-debt"
        family_records.append(
            SelfDualAutomorphismFamilyRecord(
                family_id=family_id,
                dimension=dimension,
                length=2 * dimension,
                instance_count=len(family_rows),
                rigidity_certified_instance_count=rigid,
                explicit_automorphism_instance_count=nonrigid,
                unresolved_instance_count=unresolved,
                gi_type_single_register_no_go_instance_count=no_go,
                status=family_status,
                interpretation=(
                    "Finite sampled-instance certificates do not establish an "
                    "infinite-family automorphism theorem. Growing dimensions "
                    "must be audited separately."
                ),
            )
        )

    metrics: dict[str, int | float] = {
        "family_count": len(family_records),
        "instance_count": len(records),
        "maximum_dimension": max((record.dimension for record in records), default=0),
        "complete_bounded_support_enumeration_count": sum(
            record.low_weight_supports.complete for record in records
        ),
        "maximum_support_weight": 2 * spec.half_support_order,
        "maximum_enumerated_half_subset_count": max(
            (
                record.low_weight_supports.enumerated_half_subsets
                for record in records
            ),
            default=0,
        ),
        "rigidity_certified_instance_count": sum(
            record.rigidity_certified for record in records
        ),
        "explicit_automorphism_instance_count": sum(
            record.explicit_nontrivial_automorphism_certified
            for record in records
        ),
        "unresolved_instance_count": sum(
            not record.rigidity_certified
            and not record.explicit_nontrivial_automorphism_certified
            for record in records
        ),
        "singleton_refinement_certificate_count": sum(
            record.refinement.all_coordinates_singleton for record in records
        ),
        "gi_type_single_register_no_go_certified_instance_count": sum(
            record.gi_type_single_register_no_go_applicable
            for record in records
        ),
        "infinite_family_rigidity_theorem_count": 0,
        "collective_measurement_count": 0,
        "polynomial_hidden_permutation_decoder_count": 0,
    }
    return SelfDualAutomorphismReport(
        created_at=utc_now(),
        spec=spec,
        theorem={
            "name": "bounded-weight support hypergraph automorphism certificate",
            "support_characterization": (
                "For binary self-dual C generated by G, S is a codeword support "
                "iff XOR_{j in S} G[:,j]=0."
            ),
            "enumeration_completeness": (
                "Every zero-sum support of size at most 2t is the symmetric "
                "difference of two size-at-most-t subsets with equal syndrome."
            ),
            "automorphism_implication": (
                "PAut(C) acts color-preservingly on the coordinate/support "
                "incidence graph. Singleton stable coordinate colors therefore "
                "imply PAut(C) is trivial."
            ),
            "complexity_scope": (
                "Support generation is O(n^t) for fixed t. Singleton color "
                "refinement is polynomial. Exact graph search is a finite "
                "fallback and is not represented as a polynomial family theorem."
            ),
            "hsp_consequence": (
                "For a rigidity-certified instance, the rowspace hidden-shift "
                "bridge subgroup has order two and its nonidentity element moves "
                "all 2n wreath-product points as n disjoint transpositions. "
                "Known graph-isomorphism-style single-register/strong-Fourier "
                "obstructions apply; they do not rule out collective measurements."
            ),
        },
        records=records,
        family_records=family_records,
        headline_metrics=metrics,
        claim_gate={
            "bounded_support_enumeration_complete_for_all_records": (
                metrics["complete_bounded_support_enumeration_count"]
                == metrics["instance_count"]
            ),
            "finite_rigidity_certificates_are_sound": True,
            "finite_certificates_imply_infinite_family_rigidity": False,
            "nontrivial_graph_symmetry_is_full_code_automorphism_without_verification": False,
            "gi_type_single_register_no_go_closes_collective_measurements": False,
            "explicit_collective_measurement_constructed": False,
            "polynomial_hidden_permutation_decoder_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Some finite tail instances are now rigid or explicitly "
                "nonrigid, but the growing family and collective-measurement "
                "questions remain open."
            ),
        },
        status="self-dual-automorphism-strata-certified-family-theorem-open",
        summary=(
            f"Audited {metrics['instance_count']} tail instance(s): rigidity "
            f"certificates={metrics['rigidity_certified_instance_count']}, "
            f"explicit automorphisms={metrics['explicit_automorphism_instance_count']}, "
            f"unresolved={metrics['unresolved_instance_count']}."
        ),
        falsifiers_triggered=[
            "Every bounded support must pass the public parity-check zero-syndrome test.",
            "Singleton WL colors are used as a one-way rigidity certificate only.",
            "Every nonidentity graph symmetry must pass full rowspace verification.",
            "Failure to find an automorphism is never represented as rigidity.",
            "Finite sampled rigidity is never represented as an infinite-family theorem.",
            "A rigid GI-type single-register no-go does not close collective measurements.",
        ],
    )


def write_self_dual_automorphism_workbench(
    path: Path = SELF_DUAL_AUTOMORPHISM_PATH,
    source_path: Path = SELF_DUAL_CODE_BOUNDARY_PATH,
    spec: SelfDualAutomorphismSpec = SelfDualAutomorphismSpec(),
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, Any]:
    payload = asdict(
        run_self_dual_automorphism_workbench(
            source_path=source_path,
            spec=spec,
        )
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        for record in payload["records"]:
            if not (
                record["rigidity_certified"]
                or record["explicit_nontrivial_automorphism_certified"]
            ):
                continue
            claim = (
                f"{record['instance_id']} lies outside the rigid graph-isomorphism-style "
                "rowspace-HSP obstruction."
                if record["rigidity_certified"]
                else f"{record['instance_id']} is a rigid order-two rowspace-HSP instance."
            )
            upsert_negative_result(
                NegativeResultRecord(
                    id=(
                        "NEG-CODE-SELF-DUAL-AUTOMORPHISM-"
                        + str(record["instance_id"]).upper()
                    ),
                    source=str(path),
                    claim=claim,
                    reason_invalid=record["interpretation"],
                    lesson=(
                        "Stratify self-dual instances by certified permutation "
                        "automorphism structure before importing an HSP no-go or "
                        "designing a collective measurement."
                    ),
                    applies_to=[registry_candidate_id, registry_experiment_id],
                    evidence=record,
                )
            )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-LATEST"
        upsert_experiment_result(
            ExperimentResultRecord(
                id=result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=payload["created_at"],
                status=payload["status"],
                summary=payload["summary"],
                metrics=payload["headline_metrics"],
                falsifiers_triggered=payload["falsifiers_triggered"],
                artifacts={"self_dual_automorphism_workbench": str(path)},
            )
        )
    return payload


if __name__ == "__main__":
    report = write_self_dual_automorphism_workbench()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
