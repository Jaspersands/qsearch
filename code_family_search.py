"""Adversarial hard-family search for code-equivalence candidates.

The purpose is not to celebrate random collisions.  It searches for code pairs
that fool weak invariants, then immediately attacks them with stronger
classical invariants.  Survivors would become proof obligations; rejected rows
become negative evidence against low-ceiling coset observables.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, is_dataclass
from pathlib import Path
from typing import Any

import numpy as np

from code_equivalence_workbench import (
    CodeEquivalenceCertificate,
    bounded_exact_permutation_certificate,
    codeword_int_set,
    column_weight_signature,
    gf2_rank,
    math_factorial,
    pairwise_column_inner_signature,
    permute_codeword_set,
    support_splitting_signature,
    weight_enumerator,
)
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


CODE_EQUIVALENCE_DIR = Path("research/code_equivalence")
CODE_FAMILY_SEARCH_PATH = CODE_EQUIVALENCE_DIR / "code_family_search.json"


@dataclass(frozen=True)
class CodeFamilySearchSpec:
    id: str
    length: int
    dimension: int
    max_trials: int
    seed: int


@dataclass(frozen=True)
class CodeFamilySearchRecord:
    spec: CodeFamilySearchSpec
    trials_run: int
    collision_found: bool
    weak_invariants_match: bool
    strong_distinguishing_invariants: list[str]
    exact_certificate: CodeEquivalenceCertificate
    status: str
    interpretation: str
    generator_a: list[list[int]]
    generator_b: list[list[int]]


@dataclass(frozen=True)
class CodeFamilySearchResult:
    created_at: str
    records: list[CodeFamilySearchRecord]
    headline_metrics: dict[str, int]
    status: str
    summary: str
    falsifiers_triggered: list[str]


DEFAULT_SEARCH_SPECS = [
    CodeFamilySearchSpec("random-weak-collision-9-4", length=9, dimension=4, max_trials=600, seed=123),
    CodeFamilySearchSpec("random-weak-collision-10-4", length=10, dimension=4, max_trials=600, seed=123),
    CodeFamilySearchSpec("random-weak-collision-12-5", length=12, dimension=5, max_trials=1200, seed=123),
]


def random_full_rank_generator(rng: np.random.Generator, dimension: int, length: int) -> np.ndarray:
    for _ in range(10_000):
        generator = rng.integers(0, 2, size=(dimension, length), dtype=np.uint8)
        if gf2_rank(generator) == dimension:
            return generator
    raise RuntimeError(f"failed to sample full-rank [{length},{dimension}] generator")


def weak_invariant_key(generator: np.ndarray) -> tuple[Any, ...]:
    return (
        weight_enumerator(generator),
        column_weight_signature(generator),
        pairwise_column_inner_signature(generator),
    )


def _row_reduce_gf2(matrix: np.ndarray) -> tuple[np.ndarray, list[int]]:
    values = np.asarray(matrix, dtype=np.uint8).copy() & 1
    rows, cols = values.shape
    rank = 0
    pivots: list[int] = []
    for col in range(cols):
        pivot = None
        for row in range(rank, rows):
            if values[row, col]:
                pivot = row
                break
        if pivot is None:
            continue
        if pivot != rank:
            values[[rank, pivot]] = values[[pivot, rank]]
        for row in range(rows):
            if row != rank and values[row, col]:
                values[row] ^= values[rank]
        pivots.append(col)
        rank += 1
        if rank == rows:
            break
    return values[:rank], pivots


def gf2_nullspace_basis(matrix: np.ndarray) -> np.ndarray:
    reduced, pivots = _row_reduce_gf2(matrix)
    cols = int(matrix.shape[1])
    pivot_set = set(pivots)
    free_cols = [col for col in range(cols) if col not in pivot_set]
    basis = []
    for free_col in free_cols:
        vector = np.zeros(cols, dtype=np.uint8)
        vector[free_col] = 1
        for row, pivot_col in enumerate(pivots):
            if reduced[row, free_col]:
                vector[pivot_col] = 1
        basis.append(vector)
    if not basis:
        return np.zeros((0, cols), dtype=np.uint8)
    return np.vstack(basis).astype(np.uint8)


def unique_weight_enumerator_from_words(words: np.ndarray) -> tuple[tuple[int, int], ...]:
    seen: dict[int, int] = {}
    for word in np.asarray(words, dtype=np.uint8):
        value = 0
        for index, bit in enumerate(word.tolist()):
            if bit:
                value |= 1 << index
        seen[value] = int(word.sum())
    counts: dict[int, int] = {}
    for weight in seen.values():
        counts[weight] = counts.get(weight, 0) + 1
    return tuple(sorted(counts.items()))


def enumerate_unique_codewords(generator: np.ndarray) -> np.ndarray:
    matrix = np.asarray(generator, dtype=np.uint8) & 1
    words = []
    seen = set()
    for mask in range(1 << matrix.shape[0]):
        word = np.zeros(matrix.shape[1], dtype=np.uint8)
        for row in range(matrix.shape[0]):
            if (mask >> row) & 1:
                word ^= matrix[row]
        value = 0
        for index, bit in enumerate(word.tolist()):
            if bit:
                value |= 1 << index
        if value not in seen:
            seen.add(value)
            words.append(word)
    return np.vstack(words) if words else np.zeros((0, matrix.shape[1]), dtype=np.uint8)


def dual_weight_enumerator(generator: np.ndarray) -> tuple[tuple[int, int], ...]:
    dual = gf2_nullspace_basis(generator)
    if dual.shape[0] > 12:
        return (("skipped_dual_dimension", int(dual.shape[0])),)
    return weight_enumerator(dual)


def hull_dimension(generator: np.ndarray) -> int:
    matrix = np.asarray(generator, dtype=np.uint8) & 1
    gram = (matrix @ matrix.T) & 1
    return int(matrix.shape[0] - gf2_rank(gram))


def punctured_weight_profile(generator: np.ndarray) -> tuple[tuple[tuple[int, int], ...], ...]:
    words = enumerate_unique_codewords(generator)
    profiles = []
    for coordinate in range(words.shape[1]):
        punctured = np.delete(words, coordinate, axis=1)
        profiles.append(unique_weight_enumerator_from_words(punctured))
    return tuple(sorted(profiles))


def shortened_weight_profile(generator: np.ndarray) -> tuple[tuple[tuple[int, int], ...], ...]:
    words = enumerate_unique_codewords(generator)
    profiles = []
    for coordinate in range(words.shape[1]):
        shortened = words[words[:, coordinate] == 0]
        shortened = np.delete(shortened, coordinate, axis=1)
        profiles.append(unique_weight_enumerator_from_words(shortened))
    return tuple(sorted(profiles))


def coordinate_refinement_profiles(generator: np.ndarray) -> list[tuple[Any, ...]]:
    words = enumerate_unique_codewords(generator)
    weights = words.sum(axis=1)
    profiles = []
    for coordinate in range(words.shape[1]):
        containing_weights = tuple(sorted(int(weights[index]) for index in range(words.shape[0]) if words[index, coordinate]))
        punctured = unique_weight_enumerator_from_words(np.delete(words, coordinate, axis=1))
        shortened = words[words[:, coordinate] == 0]
        shortened = unique_weight_enumerator_from_words(np.delete(shortened, coordinate, axis=1))
        profiles.append((containing_weights, punctured, shortened))
    return profiles


def strong_invariant_differences(left: np.ndarray, right: np.ndarray) -> list[str]:
    checks = [
        ("support_splitting_fingerprint", support_splitting_signature(left), support_splitting_signature(right)),
        ("dual_weight_enumerator", dual_weight_enumerator(left), dual_weight_enumerator(right)),
        ("hull_dimension", hull_dimension(left), hull_dimension(right)),
        ("punctured_weight_profile", punctured_weight_profile(left), punctured_weight_profile(right)),
        ("shortened_weight_profile", shortened_weight_profile(left), shortened_weight_profile(right)),
    ]
    return [name for name, value_left, value_right in checks if value_left != value_right]


def profile_pruned_permutation_certificate(
    left: np.ndarray,
    right: np.ndarray,
    max_assignments: int = 500_000,
) -> CodeEquivalenceCertificate:
    length = int(left.shape[1])
    left_profiles = coordinate_refinement_profiles(left)
    right_profiles = coordinate_refinement_profiles(right)
    if sorted(left_profiles) != sorted(right_profiles):
        return CodeEquivalenceCertificate(
            name="profile_pruned_permutation_search",
            evaluated=True,
            equivalent=False,
            cost_model="Coordinate refinement profile multisets differ before permutation search.",
            interpretation="Profile-pruned exact check rejects equivalence.",
        )

    buckets: dict[tuple[Any, ...], list[int]] = {}
    for index, profile in enumerate(right_profiles):
        buckets.setdefault(profile, []).append(index)
    estimated = 1
    for values in buckets.values():
        estimated *= math_factorial(len(values))
    if estimated > max_assignments:
        return CodeEquivalenceCertificate(
            name="profile_pruned_permutation_search",
            evaluated=False,
            equivalent=None,
            cost_model=f"Skipped: profile buckets allow {estimated} assignments, above cap {max_assignments}.",
            interpretation="Profile-pruned exact check skipped; add a stronger canonical baseline.",
        )

    source = codeword_int_set(left)
    target = codeword_int_set(right)
    order = sorted(range(length), key=lambda idx: (len(buckets[left_profiles[idx]]), left_profiles[idx], idx))
    permutation = [-1] * length
    used: set[int] = set()
    checked = 0

    def backtrack(position: int) -> bool:
        nonlocal checked
        if position == len(order):
            checked += 1
            return permute_codeword_set(source, length, permutation) == target
        left_index = order[position]
        for right_index in buckets[left_profiles[left_index]]:
            if right_index in used:
                continue
            permutation[left_index] = right_index
            used.add(right_index)
            if backtrack(position + 1):
                return True
            used.remove(right_index)
            permutation[left_index] = -1
        return False

    equivalent = backtrack(0)
    return CodeEquivalenceCertificate(
        name="profile_pruned_permutation_search",
        evaluated=True,
        equivalent=equivalent,
        cost_model=f"Checked {checked} profile-compatible assignment(s) out of estimated {estimated}.",
        interpretation=(
            "Profile-pruned exact check found an equivalence permutation."
            if equivalent
            else "Profile-pruned exact check rejects equivalence."
        ),
    )


def _is_exact_equivalent_control(left: np.ndarray, right: np.ndarray, max_permutations: int) -> bool:
    certificate = profile_pruned_permutation_certificate(left, right, max_assignments=max_permutations)
    if certificate.evaluated:
        return bool(certificate.equivalent)
    if math_factorial(int(left.shape[1])) > max_permutations:
        return False
    fallback = bounded_exact_permutation_certificate(left, right, max_permutations=max_permutations)
    return bool(fallback.evaluated and fallback.equivalent)


def find_weak_invariant_collision(
    spec: CodeFamilySearchSpec,
    exact_equivalence_skip_cap: int = 4_000_000,
) -> tuple[int, np.ndarray | None, np.ndarray | None]:
    rng = np.random.default_rng(spec.seed)
    seen: dict[tuple[Any, ...], np.ndarray] = {}
    for trial in range(1, spec.max_trials + 1):
        candidate = random_full_rank_generator(rng, spec.dimension, spec.length)
        key = weak_invariant_key(candidate)
        previous = seen.get(key)
        if previous is not None and codeword_int_set(previous) != codeword_int_set(candidate):
            if _is_exact_equivalent_control(previous, candidate, exact_equivalence_skip_cap):
                continue
            return trial, previous, candidate
        seen.setdefault(key, candidate)
    return spec.max_trials, None, None


def exact_certificate_for_search_record(left: np.ndarray, right: np.ndarray, max_permutations: int = 4_000_000) -> CodeEquivalenceCertificate:
    length = int(left.shape[1])
    pruned = profile_pruned_permutation_certificate(left, right, max_assignments=max_permutations)
    if pruned.evaluated:
        return pruned
    if math_factorial(length) <= max_permutations:
        return bounded_exact_permutation_certificate(left, right, max_permutations=max_permutations)
    return pruned


def run_search_spec(spec: CodeFamilySearchSpec) -> CodeFamilySearchRecord:
    trials, left, right = find_weak_invariant_collision(spec)
    if left is None or right is None:
        certificate = CodeEquivalenceCertificate(
            name="bounded_exact_permutation_search",
            evaluated=False,
            equivalent=None,
            cost_model="No weak-invariant collision was found, so exact search was not run.",
            interpretation="Increase search budget or change family parameters.",
        )
        return CodeFamilySearchRecord(
            spec=spec,
            trials_run=trials,
            collision_found=False,
            weak_invariants_match=False,
            strong_distinguishing_invariants=[],
            exact_certificate=certificate,
            status="no-collision-found",
            interpretation="No weak-invariant collision found under this deterministic budget.",
            generator_a=[],
            generator_b=[],
        )

    strong = strong_invariant_differences(left, right)
    certificate = exact_certificate_for_search_record(left, right)
    if strong:
        status = "rejected-by-strong-classical-invariant"
        interpretation = (
            "The pair fools weak invariants but is separated by stronger classical code invariants: "
            + ", ".join(strong)
        )
    elif certificate.evaluated and certificate.equivalent is False:
        status = "rejected-by-bounded-exact-search"
        interpretation = "Weak and strong invariants match, but bounded exact permutation search rejects equivalence at this size."
    else:
        status = "hard-family-candidate-needs-proof"
        interpretation = "Weak and implemented strong invariants match; promote only as proof debt, not as positive quantum evidence."

    return CodeFamilySearchRecord(
        spec=spec,
        trials_run=trials,
        collision_found=True,
        weak_invariants_match=weak_invariant_key(left) == weak_invariant_key(right),
        strong_distinguishing_invariants=strong,
        exact_certificate=certificate,
        status=status,
        interpretation=interpretation,
        generator_a=[[int(bit) for bit in row] for row in left.tolist()],
        generator_b=[[int(bit) for bit in row] for row in right.tolist()],
    )


def run_code_family_search(specs: list[CodeFamilySearchSpec] | None = None) -> CodeFamilySearchResult:
    active_specs = specs or DEFAULT_SEARCH_SPECS
    records = [run_search_spec(spec) for spec in active_specs]
    metrics = {
        "search_count": len(records),
        "collision_found_count": sum(1 for record in records if record.collision_found),
        "strong_invariant_rejection_count": sum(1 for record in records if record.status == "rejected-by-strong-classical-invariant"),
        "bounded_exact_rejection_count": sum(1 for record in records if record.status == "rejected-by-bounded-exact-search"),
        "hard_family_candidate_count": sum(1 for record in records if record.status == "hard-family-candidate-needs-proof"),
        "no_collision_count": sum(1 for record in records if record.status == "no-collision-found"),
        "max_length": max((record.spec.length for record in records), default=0),
    }
    if metrics["hard_family_candidate_count"]:
        status = "needs-proof-gate-review"
    elif metrics["strong_invariant_rejection_count"] or metrics["bounded_exact_rejection_count"]:
        status = "all-generated-collisions-dequantized"
    else:
        status = "search-incomplete"
    summary = (
        f"Searched {metrics['search_count']} code-family budgets and found {metrics['collision_found_count']} weak-invariant collision(s). "
        f"{metrics['strong_invariant_rejection_count']} were rejected by stronger classical invariants; "
        f"{metrics['hard_family_candidate_count']} survived implemented baselines."
    )
    falsifiers = []
    if metrics["strong_invariant_rejection_count"]:
        falsifiers.append("Generated weak-invariant collisions are separated by stronger classical code invariants.")
    if metrics["hard_family_candidate_count"]:
        falsifiers.append("Surviving code-family rows lack proof-gate, canonicalization, and lower-bound certification.")
    return CodeFamilySearchResult(utc_now(), records, metrics, status, summary, falsifiers)


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


def write_code_family_negative_results(result: CodeFamilySearchResult) -> int:
    written = 0
    for record in result.records:
        if record.status not in {"rejected-by-strong-classical-invariant", "rejected-by-bounded-exact-search"}:
            continue
        upsert_negative_result(
            NegativeResultRecord(
                id=f"CODE-FAMILY-SEARCH-REJECTED-{_safe_id(record.spec.id)}",
                source="code_family_search.py",
                claim=f"{record.spec.id} is a hard code-equivalence family for nonclassical coset observables.",
                reason_invalid=record.interpretation,
                lesson=(
                    "Weak code-invariant collisions are not evidence.  Search rows must survive support splitting, dual/hull "
                    "profiles, puncturing/shortening profiles, and canonicalization baselines before they motivate quantum observables."
                ),
                applies_to=["CODE-COSET-COLLECTIVE", "PO-DEQUANTIZATION", "PO-FALSIFIERS"],
                evidence={
                    "search_id": record.spec.id,
                    "length": record.spec.length,
                    "dimension": record.spec.dimension,
                    "trials_run": record.trials_run,
                    "strong_distinguishing_invariants": record.strong_distinguishing_invariants,
                    "status": record.status,
                },
            )
        )
        written += 1
    return written


def write_code_family_search(
    output_path: Path = CODE_FAMILY_SEARCH_PATH,
    specs: list[CodeFamilySearchSpec] | None = None,
    write_registry: bool = True,
    registry_experiment_id: str = "EXP-CODE-HARD-FAMILY-SEARCH",
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "RESULT-CODE-HARD-FAMILY-SEARCH-LATEST",
) -> dict[str, Any]:
    result = run_code_family_search(specs=specs)
    payload = _json_ready(result)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    if write_registry:
        negative_results_written = write_code_family_negative_results(result)
        metrics = dict(result.headline_metrics)
        metrics["negative_results_written"] = negative_results_written
        upsert_experiment_result(
            ExperimentResultRecord(
                id=registry_result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=result.created_at,
                status=result.status,
                summary=result.summary,
                metrics=metrics,
                falsifiers_triggered=result.falsifiers_triggered,
                artifacts={"code_family_search": str(output_path)},
            )
        )
    return payload
