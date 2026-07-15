"""Hull-projector reduction and scalable planted code-equivalence benchmark.

For a code C with trivial Euclidean hull and full-rank generator G, the matrix

    Sigma_C = G^T (G G^T)^(-1) G

is independent of the chosen row basis, has image C, and transforms by
coordinate conjugation.  Permutation code equivalence is therefore exactly
weighted graph isomorphism for Sigma_C.  Over GF(2), diagonal entries are
vertex colors and off-diagonal one entries are ordinary edges.

The benchmark samples hull dimensions without conditioning, then constructs
separate trivial-hull planted pairs for executable graph matching.  A finite
graph match is a classical upper-bound witness, not a polynomial-time GI
theorem and not evidence for a quantum speedup.
"""

from __future__ import annotations

import json
import math
import signal
import threading
import time
from collections import Counter
from dataclasses import asdict, dataclass, is_dataclass
from pathlib import Path
from typing import Any, Sequence

import networkx as nx
import numpy as np

from code_equivalence_workbench import gf2_rank
from code_family_search import hull_dimension, random_full_rank_generator
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


CODE_EQUIVALENCE_DIR = Path("research/code_equivalence")
HULL_PROJECTOR_REDUCTION_PATH = CODE_EQUIVALENCE_DIR / "code_hull_projector_reduction.json"
LITERATURE_IDS = ["bardet-otmani-saeed-trivial-hull-2019"]


class _GraphMatchTimeout(Exception):
    pass


@dataclass(frozen=True)
class HullProjectorTheoremCertificate:
    theorem_id: str
    literature_ids: list[str]
    primary_url: str
    theorem_locator: str
    domain: str
    projector_formula: str
    basis_independence_proved: bool
    permutation_conjugacy_proved: bool
    reverse_image_implication_proved: bool
    trivial_hull_reduction_cost: str
    nontrivial_hull_upper_bound: str
    limitations: list[str]


@dataclass(frozen=True)
class HullDistributionRecord:
    length: int
    dimension: int
    sample_count: int
    hull_histogram: list[list[int]]
    trivial_hull_fraction: float
    hull_at_most_two_fraction: float
    mean_hull_dimension: float
    maximum_hull_dimension: int
    maximum_observed_shortening_log2_overhead_excluding_gi: float
    interpretation: str


@dataclass(frozen=True)
class ProjectorCertificate:
    available: bool
    hull_dimension: int
    symmetric: bool
    idempotent: bool
    rank_matches_code: bool
    image_contains_generator_rows: bool
    basis_invariant: bool
    status: str
    interpretation: str


@dataclass(frozen=True)
class ProjectorGraphMatch:
    evaluated: bool
    equivalent: bool | None
    timed_out: bool
    mapping_verified: bool | None
    recovered_coordinate_permutation: list[int] | None
    wl_hash_match: bool
    search_seconds: float
    status: str
    cost_model: str
    interpretation: str


@dataclass(frozen=True)
class PlantedProjectorRecord:
    id: str
    length: int
    dimension: int
    rate: float
    trial: int
    left_sampling_attempts: int
    null_sampling_attempts: int
    projector_certificate: ProjectorCertificate
    planted_conjugacy_verified: bool
    equivalent_match: ProjectorGraphMatch
    null_match: ProjectorGraphMatch
    status: str
    interpretation: str


@dataclass(frozen=True)
class HullProjectorReductionReport:
    created_at: str
    theorem: HullProjectorTheoremCertificate
    access_model_ledger: list[dict[str, Any]]
    hull_distribution_records: list[HullDistributionRecord]
    planted_records: list[PlantedProjectorRecord]
    headline_metrics: dict[str, int | float]
    status: str
    summary: str
    falsifiers_triggered: list[str]


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


def row_spaces_equal(left: np.ndarray, right: np.ndarray) -> bool:
    left = np.asarray(left, dtype=np.uint8) & 1
    right = np.asarray(right, dtype=np.uint8) & 1
    if left.shape[1] != right.shape[1]:
        return False
    return gf2_rank(left) == gf2_rank(right) == gf2_rank(np.vstack((left, right)))


def hull_projector(generator: np.ndarray) -> np.ndarray | None:
    matrix = np.asarray(generator, dtype=np.uint8) & 1
    if matrix.ndim != 2 or gf2_rank(matrix) != matrix.shape[0]:
        raise ValueError("projector reduction requires a full-rank generator basis")
    gram = (matrix @ matrix.T) & 1
    if gf2_rank(gram) != matrix.shape[0]:
        return None
    return ((matrix.T @ _gf2_inverse(gram) @ matrix) & 1).astype(np.uint8)


def certify_hull_projector(generator: np.ndarray, seed: int = 0) -> ProjectorCertificate:
    matrix = np.asarray(generator, dtype=np.uint8) & 1
    hull = hull_dimension(matrix)
    projector = hull_projector(matrix)
    if projector is None:
        return ProjectorCertificate(
            available=False,
            hull_dimension=hull,
            symmetric=False,
            idempotent=False,
            rank_matches_code=False,
            image_contains_generator_rows=False,
            basis_invariant=False,
            status="nontrivial-hull-projector-unavailable",
            interpretation=(
                "The Euclidean Gram matrix is singular. Use the source-linked shortening reduction or another inner "
                "product; do not apply the trivial-hull projector theorem."
            ),
        )
    rng = np.random.default_rng(seed)
    row_map = _random_invertible_matrix(int(matrix.shape[0]), rng)
    alternate = (row_map @ matrix) & 1
    alternate_projector = hull_projector(alternate)
    symmetric = bool(np.array_equal(projector, projector.T))
    idempotent = bool(np.array_equal((projector @ projector) & 1, projector))
    rank_matches = gf2_rank(projector) == matrix.shape[0]
    image_contains = bool(np.array_equal((matrix @ projector) & 1, matrix))
    basis_invariant = bool(alternate_projector is not None and np.array_equal(projector, alternate_projector))
    valid = symmetric and idempotent and rank_matches and image_contains and basis_invariant
    return ProjectorCertificate(
        available=True,
        hull_dimension=hull,
        symmetric=symmetric,
        idempotent=idempotent,
        rank_matches_code=rank_matches,
        image_contains_generator_rows=image_contains,
        basis_invariant=basis_invariant,
        status="trivial-hull-projector-certified" if valid else "invalid-projector-certificate",
        interpretation=(
            "The basis-independent symmetric idempotent has image equal to the code."
            if valid
            else "At least one executable projector identity failed."
        ),
    )


def projector_graph(projector: np.ndarray) -> nx.Graph:
    matrix = np.asarray(projector, dtype=np.uint8) & 1
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1] or not np.array_equal(matrix, matrix.T):
        raise ValueError("projector graph requires a symmetric square matrix")
    graph = nx.Graph()
    for vertex in range(matrix.shape[0]):
        graph.add_node(vertex, loop_weight=int(matrix[vertex, vertex]))
    for left in range(matrix.shape[0]):
        for right in range(left + 1, matrix.shape[0]):
            if matrix[left, right]:
                graph.add_edge(left, right)
    return graph


def _wl_hash(graph: nx.Graph) -> str:
    return nx.weisfeiler_lehman_graph_hash(graph, node_attr="loop_weight", iterations=8)


def _run_graph_matcher(
    left_graph: nx.Graph,
    right_graph: nx.Graph,
    max_search_seconds: float,
) -> tuple[bool, dict[int, int], bool]:
    matcher = nx.algorithms.isomorphism.GraphMatcher(
        left_graph,
        right_graph,
        node_match=lambda left, right: left.get("loop_weight") == right.get("loop_weight"),
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
            raise _GraphMatchTimeout

        signal.signal(signal.SIGALRM, _timeout)
        signal.setitimer(signal.ITIMER_REAL, max_search_seconds)
    try:
        equivalent = bool(matcher.is_isomorphic())
        return equivalent, {int(key): int(value) for key, value in matcher.mapping.items()} if equivalent else {}, False
    except _GraphMatchTimeout:
        return False, {}, True
    finally:
        if can_alarm:
            signal.setitimer(signal.ITIMER_REAL, 0)
            signal.signal(signal.SIGALRM, previous_handler)
            if previous_timer[0] > 0 or previous_timer[1] > 0:
                signal.setitimer(signal.ITIMER_REAL, previous_timer[0], previous_timer[1])


def verify_coordinate_mapping(left: np.ndarray, right: np.ndarray, mapping: dict[int, int]) -> bool:
    left = np.asarray(left, dtype=np.uint8) & 1
    right = np.asarray(right, dtype=np.uint8) & 1
    length = int(left.shape[1])
    if left.shape[1] != right.shape[1] or set(mapping) != set(range(length)) or set(mapping.values()) != set(range(length)):
        return False
    aligned = np.zeros_like(left)
    for source, target in mapping.items():
        aligned[:, target] = left[:, source]
    return row_spaces_equal(aligned, right)


def match_trivial_hull_codes(
    left: np.ndarray,
    right: np.ndarray,
    max_search_seconds: float = 10.0,
) -> ProjectorGraphMatch:
    left_projector = hull_projector(left)
    right_projector = hull_projector(right)
    if left_projector is None or right_projector is None:
        return ProjectorGraphMatch(
            evaluated=False,
            equivalent=None,
            timed_out=False,
            mapping_verified=None,
            recovered_coordinate_permutation=None,
            wl_hash_match=False,
            search_seconds=0.0,
            status="nontrivial-hull-projector-not-applicable",
            cost_model="Trivial-hull precondition failed before graph construction.",
            interpretation="Use a nontrivial-hull shortening reduction; this result is proof debt, not hardness evidence.",
        )
    left_graph = projector_graph(left_projector)
    right_graph = projector_graph(right_projector)
    wl_match = _wl_hash(left_graph) == _wl_hash(right_graph)
    started = time.perf_counter()
    equivalent, mapping, timed_out = _run_graph_matcher(left_graph, right_graph, max_search_seconds)
    elapsed = round(time.perf_counter() - started, 6)
    if timed_out:
        return ProjectorGraphMatch(
            evaluated=False,
            equivalent=None,
            timed_out=True,
            mapping_verified=None,
            recovered_coordinate_permutation=None,
            wl_hash_match=wl_match,
            search_seconds=elapsed,
            status="projector-graph-isomorphism-timeout",
            cost_model="O(n^3) projector construction followed by exact colored VF2 with a wall-clock cap.",
            interpretation="Finite graph matching timed out; retain proof debt and do not infer hardness.",
        )
    verified = verify_coordinate_mapping(left, right, mapping) if equivalent else True
    permutation = [mapping[index] for index in range(left.shape[1])] if equivalent and verified else None
    status = (
        "projector-graph-equivalence-witness-verified"
        if equivalent and verified
        else "projector-graphs-nonisomorphic-code-nonequivalence-certified"
        if not equivalent
        else "projector-graph-mapping-verification-failed"
    )
    return ProjectorGraphMatch(
        evaluated=True,
        equivalent=equivalent if verified else None,
        timed_out=False,
        mapping_verified=verified,
        recovered_coordinate_permutation=permutation,
        wl_hash_match=wl_match,
        search_seconds=elapsed,
        status=status,
        cost_model=(
            "O(n^3) GF(2) projector construction plus exact colored VF2. The reduction is polynomial; "
            "the bundled graph matcher has no polynomial worst-case guarantee."
        ),
        interpretation=(
            "Recovered a graph isomorphism and verified its coordinate permutation on the complete code row spaces."
            if equivalent and verified
            else "Projector graphs are nonisomorphic, which certifies code nonequivalence under the iff theorem."
            if not equivalent
            else "Graph isomorphism output failed code-space verification."
        ),
    )


def theorem_certificate() -> HullProjectorTheoremCertificate:
    return HullProjectorTheoremCertificate(
        theorem_id="THM-TRIVIAL-HULL-PCE-TO-WEIGHTED-GI-2019",
        literature_ids=list(LITERATURE_IDS),
        primary_url="https://arxiv.org/abs/1905.00073",
        theorem_locator="Theorem 6 for trivial hulls; Proposition 9 and Theorem 10 for shortening nontrivial hulls.",
        domain="Permutation equivalence of full-rank linear codes; executable workbench specializes to binary codes.",
        projector_formula="Sigma_C = G^T (G G^T)^(-1) G for hull(C)={0}.",
        basis_independence_proved=True,
        permutation_conjugacy_proved=True,
        reverse_image_implication_proved=True,
        trivial_hull_reduction_cost="O(n^omega) field operations plus one weighted graph-isomorphism instance.",
        nontrivial_hull_upper_bound="O(h n^(omega+h+1) GI(n)) for hull dimension h via shortening.",
        limitations=[
            "The theorem reduces code equivalence to graph isomorphism; it does not put GI in polynomial time.",
            "The executable graph matcher is a finite baseline with no polynomial worst-case guarantee.",
            "The direct projector requires explicit generator matrices and a trivial hull.",
            "For nontrivial hulls this module records the source theorem's shortening cost but does not implement all GI calls.",
            "Random finite hull statistics are not an asymptotic bounded-hull theorem.",
        ],
    )


def access_model_ledger() -> list[dict[str, Any]]:
    return [
        {
            "model": "explicit-full-rank-generator-matrices",
            "projector_reduction_legal": True,
            "reason": "Gram matrices, inverses, projectors, and coordinate graphs are available in polynomial preprocessing.",
        },
        {
            "model": "random-codeword-samples",
            "projector_reduction_legal": False,
            "reason": "No generator-recovery theorem is supplied from bounded random codeword samples.",
        },
        {
            "model": "coset-state-copies-only",
            "projector_reduction_legal": False,
            "reason": "Coset states do not automatically expose the classical generator matrices used by the projector attack.",
        },
        {
            "model": "code-equivalence-hsp-with-public-generators",
            "projector_reduction_legal": True,
            "reason": "Standard code-equivalence HSP instances are constructed from public generator matrices, so preprocessing is legal.",
        },
    ]


def shortening_log2_overhead(length: int, hull: int, omega: float = 2.373) -> float:
    if hull <= 0:
        return float(omega * math.log2(length))
    return float(math.log2(hull) + (omega + hull + 1.0) * math.log2(length))


def sample_hull_distribution(
    length: int,
    dimension: int,
    sample_count: int,
    seed: int,
) -> HullDistributionRecord:
    rng = np.random.default_rng(seed)
    hulls = [hull_dimension(random_full_rank_generator(rng, dimension, length)) for _ in range(sample_count)]
    histogram = Counter(hulls)
    maximum = max(hulls, default=0)
    return HullDistributionRecord(
        length=length,
        dimension=dimension,
        sample_count=sample_count,
        hull_histogram=[[int(value), int(count)] for value, count in sorted(histogram.items())],
        trivial_hull_fraction=float(histogram.get(0, 0) / max(1, sample_count)),
        hull_at_most_two_fraction=float(sum(count for value, count in histogram.items() if value <= 2) / max(1, sample_count)),
        mean_hull_dimension=float(sum(hulls) / max(1, len(hulls))),
        maximum_hull_dimension=int(maximum),
        maximum_observed_shortening_log2_overhead_excluding_gi=shortening_log2_overhead(length, maximum),
        interpretation=(
            "Unconditional random-code hull sample. Bounded finite hulls make the source shortening upper bound "
            "practically relevant, but do not prove an asymptotic hull-tail theorem."
        ),
    )


def _sample_trivial_hull_code(
    rng: np.random.Generator,
    dimension: int,
    length: int,
    max_attempts: int = 10_000,
) -> tuple[np.ndarray, int]:
    for attempt in range(1, max_attempts + 1):
        generator = random_full_rank_generator(rng, dimension, length)
        if hull_dimension(generator) == 0:
            return generator, attempt
    raise RuntimeError(f"failed to sample a trivial-hull [{length},{dimension}] code")


def _planted_equivalent_pair(
    left: np.ndarray,
    rng: np.random.Generator,
) -> tuple[np.ndarray, dict[int, int]]:
    dimension, length = left.shape
    source_order = rng.permutation(length)
    row_map = _random_invertible_matrix(dimension, rng)
    right = (row_map @ left[:, source_order]) & 1
    planted_mapping = {int(source_order[target]): int(target) for target in range(length)}
    return right.astype(np.uint8), planted_mapping


def _conjugacy_holds(left_projector: np.ndarray, right_projector: np.ndarray, mapping: dict[int, int]) -> bool:
    length = int(left_projector.shape[0])
    reordered = np.zeros_like(left_projector)
    for left_i in range(length):
        for left_j in range(length):
            reordered[mapping[left_i], mapping[left_j]] = left_projector[left_i, left_j]
    return bool(np.array_equal(reordered, right_projector))


def audit_planted_projector_pair(
    length: int,
    dimension: int,
    trial: int,
    seed: int,
    max_search_seconds: float = 10.0,
) -> PlantedProjectorRecord:
    rng = np.random.default_rng(seed)
    left, left_attempts = _sample_trivial_hull_code(rng, dimension, length)
    right, planted_mapping = _planted_equivalent_pair(left, rng)
    null, null_attempts = _sample_trivial_hull_code(rng, dimension, length)
    projector_certificate = certify_hull_projector(left, seed=seed + 1)
    left_projector = hull_projector(left)
    right_projector = hull_projector(right)
    planted_conjugacy = bool(
        left_projector is not None
        and right_projector is not None
        and _conjugacy_holds(left_projector, right_projector, planted_mapping)
    )
    equivalent_match = match_trivial_hull_codes(left, right, max_search_seconds=max_search_seconds)
    null_match = match_trivial_hull_codes(left, null, max_search_seconds=max_search_seconds)
    if projector_certificate.status == "invalid-projector-certificate" or not planted_conjugacy:
        status = "invalid-projector-reduction-control"
        interpretation = "A projector identity or planted conjugacy check failed; quarantine all conclusions."
    elif equivalent_match.timed_out or null_match.timed_out:
        status = "projector-gi-finite-search-proof-debt"
        interpretation = "The polynomial reduction succeeded but bundled finite graph matching timed out."
    elif equivalent_match.equivalent is True and equivalent_match.mapping_verified and null_match.equivalent is False:
        status = "random-trivial-hull-code-reduced-to-gi-and-finite-resolved"
        interpretation = (
            "The planted search witness and independent null were exactly resolved through the hull projector. "
            "This removes code-specific hardness but does not solve worst-case GI."
        )
    else:
        status = "projector-gi-unexpected-finite-result"
        interpretation = "The equivalent or null control produced an unexpected graph-matching result."
    return PlantedProjectorRecord(
        id=f"random-trivial-hull-n{length}-k{dimension}-trial{trial}",
        length=length,
        dimension=dimension,
        rate=float(dimension / length),
        trial=trial,
        left_sampling_attempts=left_attempts,
        null_sampling_attempts=null_attempts,
        projector_certificate=projector_certificate,
        planted_conjugacy_verified=planted_conjugacy,
        equivalent_match=equivalent_match,
        null_match=null_match,
        status=status,
        interpretation=interpretation,
    )


def _fit_log2_time_slope(records: Sequence[PlantedProjectorRecord]) -> float:
    by_length: dict[int, list[float]] = {}
    for record in records:
        if record.equivalent_match.evaluated:
            by_length.setdefault(record.length, []).append(max(record.equivalent_match.search_seconds, 1e-6))
    if len(by_length) < 2:
        return 0.0
    lengths = np.asarray(sorted(by_length), dtype=float)
    medians = np.asarray([np.median(by_length[int(length)]) for length in lengths], dtype=float)
    return float(np.polyfit(lengths, np.log2(medians), 1)[0])


def run_hull_projector_reduction(
    lengths: Sequence[int] = (24, 32, 48, 64, 96),
    rate: float = 0.5,
    trials: int = 2,
    hull_samples: int = 64,
    seed: int = 22_071,
    max_search_seconds: float = 10.0,
) -> HullProjectorReductionReport:
    if not 0 < rate < 1:
        raise ValueError("rate must lie strictly between zero and one")
    dimensions = [max(1, min(length - 1, int(round(rate * length)))) for length in lengths]
    hull_records = [
        sample_hull_distribution(length, dimension, hull_samples, seed + 1009 * index)
        for index, (length, dimension) in enumerate(zip(lengths, dimensions))
    ]
    planted_records = [
        audit_planted_projector_pair(
            length,
            dimension,
            trial,
            seed + 100_003 * index + trial,
            max_search_seconds=max_search_seconds,
        )
        for index, (length, dimension) in enumerate(zip(lengths, dimensions))
        for trial in range(trials)
    ]
    total_hull_samples = sum(record.sample_count for record in hull_records)
    trivial_hull_samples = sum(
        next((count for value, count in record.hull_histogram if value == 0), 0) for record in hull_records
    )
    bounded_hull_samples = sum(
        sum(count for value, count in record.hull_histogram if value <= 2) for record in hull_records
    )
    resolved = sum(record.status == "random-trivial-hull-code-reduced-to-gi-and-finite-resolved" for record in planted_records)
    timeouts = sum(record.status == "projector-gi-finite-search-proof-debt" for record in planted_records)
    invalid = sum(record.status in {"invalid-projector-reduction-control", "projector-gi-unexpected-finite-result"} for record in planted_records)
    metrics: dict[str, int | float] = {
        "length_count": len(lengths),
        "planted_pair_count": len(planted_records),
        "hull_sample_count": total_hull_samples,
        "trivial_hull_sample_count": trivial_hull_samples,
        "trivial_hull_fraction": float(trivial_hull_samples / max(1, total_hull_samples)),
        "hull_at_most_two_sample_count": bounded_hull_samples,
        "hull_at_most_two_fraction": float(bounded_hull_samples / max(1, total_hull_samples)),
        "projector_finite_resolved_count": resolved,
        "projector_timeout_count": timeouts,
        "invalid_control_count": invalid,
        "maximum_observed_hull_dimension": max((record.maximum_hull_dimension for record in hull_records), default=0),
        "maximum_length": max(lengths, default=0),
        "fitted_log2_graph_match_time_slope_per_n": _fit_log2_time_slope(planted_records),
        "proved_polynomial_gi_solver_count": 0,
        "positive_quantum_evidence_count": 0,
    }
    if invalid:
        status = "hull-projector-reduction-invalid"
    elif timeouts:
        status = "hull-projector-reduction-finite-gi-proof-debt"
    else:
        status = "random-trivial-hull-code-equivalence-collapses-to-gi"
    summary = (
        f"Sampled {total_hull_samples} unconditional random code(s): {metrics['trivial_hull_fraction']:.3f} had "
        f"trivial hull and {metrics['hull_at_most_two_fraction']:.3f} had hull dimension at most two. "
        f"The projector/GI path exactly resolved {resolved}/{len(planted_records)} planted/null pair sets; "
        "it proves no polynomial GI algorithm and emits no quantum evidence."
    )
    falsifiers = []
    if resolved:
        falsifiers.append("Trivial-hull random code equivalence reduces exactly to graph isomorphism and finite graph matching recovers the planted permutation.")
    if bounded_hull_samples:
        falsifiers.append("Most finite random samples have small hull, activating the source-linked shortening upper bound; no asymptotic tail claim is inferred.")
    if timeouts:
        falsifiers.append("Some finite projector graph matches timed out and remain proof debt.")
    return HullProjectorReductionReport(
        created_at=utc_now(),
        theorem=theorem_certificate(),
        access_model_ledger=access_model_ledger(),
        hull_distribution_records=hull_records,
        planted_records=planted_records,
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
    if isinstance(value, (np.integer, np.bool_, np.floating)):
        return value.item()
    return value


def write_hull_projector_negative_results(report: HullProjectorReductionReport) -> int:
    resolved = int(report.headline_metrics.get("projector_finite_resolved_count", 0) or 0)
    if not resolved:
        return 0
    upsert_negative_result(
        NegativeResultRecord(
            id="RANDOM-TRIVIAL-HULL-CODE-NOT-INDEPENDENT-OF-GI",
            source="code_hull_projector_reduction.py",
            claim="Random trivial-hull binary codes provide code-native hardness beyond graph isomorphism.",
            reason_invalid=(
                "The source theorem and executable projector certificates reduce permutation code equivalence iff to "
                f"weighted GI, and finite graph matching resolved {resolved} planted/null pair set(s)."
            ),
            lesson=(
                "Split code families by hull dimension before observable design. Trivial-hull rows are GI benchmarks, "
                "not independent code-equivalence evidence; nontrivial-hull rows must charge shortening or other attacks."
            ),
            applies_to=["CODE-COSET-COLLECTIVE", "PO-DEQUANTIZATION", "PO-REDUCTION", "PO-CLASSICAL-BASELINE"],
            evidence=dict(report.headline_metrics),
        )
    )
    return 1


def write_hull_projector_reduction(
    output_path: Path = HULL_PROJECTOR_REDUCTION_PATH,
    lengths: Sequence[int] = (24, 32, 48, 64, 96),
    rate: float = 0.5,
    trials: int = 2,
    hull_samples: int = 64,
    seed: int = 22_071,
    max_search_seconds: float = 10.0,
    write_registry: bool = True,
    registry_experiment_id: str = "EXP-CODE-TRIVIAL-HULL-PROJECTOR-GI",
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "RESULT-CODE-TRIVIAL-HULL-PROJECTOR-GI-LATEST",
) -> dict[str, Any]:
    report = run_hull_projector_reduction(
        lengths=lengths,
        rate=rate,
        trials=trials,
        hull_samples=hull_samples,
        seed=seed,
        max_search_seconds=max_search_seconds,
    )
    payload = _json_ready(report)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        metrics = dict(report.headline_metrics)
        metrics["negative_results_written"] = write_hull_projector_negative_results(report)
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
                artifacts={"code_hull_projector_reduction": str(output_path)},
            )
        )
    return payload
