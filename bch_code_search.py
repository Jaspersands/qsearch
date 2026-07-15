"""BCH-code family search for code-equivalence frontiers.

BCH codes are a more structured cyclic-code source than arbitrary divisors of
``x^n - 1``.  This module generates primitive binary BCH codes from cyclotomic
cosets and finite-field minimal polynomials, then immediately attacks weak
tuple-profile collisions with the natural decimation/multiplier automorphisms,
low-weight matroid structure, and exact code canonicalization.

The goal is negative pressure, not optimism: BCH rows only become useful proof
debt if they survive the algebraic controls and the generic code baselines.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, is_dataclass
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations
from pathlib import Path
from typing import Any

import numpy as np

from code_canonicalization_baseline import audit_code_canonicalization_pair
from code_family_search import enumerate_unique_codewords, strong_invariant_differences
from code_low_weight_structure import CodePairInput, audit_low_weight_structure_pair
from code_tuple_profile_baseline import audit_code_tuple_profile_pair, coordinate_tuple_profile_multiset, tuple_profile_key
from cyclic_code_search import cyclic_generator_matrix, poly_mul
from research_registry import ExperimentResultRecord, NegativeResultRecord, upsert_experiment_result, upsert_negative_result, utc_now


CODE_EQUIVALENCE_DIR = Path("research/code_equivalence")
BCH_CODE_SEARCH_PATH = CODE_EQUIVALENCE_DIR / "bch_code_search.json"
EXACT_CODEWORD_DIMENSION_LIMIT = 14


@dataclass(frozen=True)
class BCHSearchSpec:
    id: str
    extension_degree: int
    min_designed_distance: int
    max_designed_distance: int
    starts: tuple[int, ...]
    tuple_size: int
    max_collisions: int


@dataclass(frozen=True)
class BCHCodeDescriptor:
    id: str
    extension_degree: int
    length: int
    start: int
    designed_distance: int
    dimension: int
    generator_poly: str
    defining_set: list[int]
    cyclotomic_cosets: list[list[int]]


@dataclass(frozen=True)
class DecimationEquivalence:
    equivalent: bool
    multiplier: int | None
    maps_checked: int
    interpretation: str


@dataclass(frozen=True)
class BCHCollisionAudit:
    id: str
    length: int
    dimension_a: int
    dimension_b: int
    code_a: BCHCodeDescriptor
    code_b: BCHCodeDescriptor
    tuple_profile_bucket_size: int
    strong_distinguishing_invariants: list[str]
    tuple_profile_status: str
    multiplier_affine_equivalent: bool
    multiplier: int | None
    multiplier_shift: int | None
    multiplier_maps_checked: int
    low_weight_status: str
    canonical_status: str
    canonical_equal: bool | None
    dual_dimension_a: int | None
    dual_dimension_b: int | None
    dual_higher_tuple_status: str
    dual_higher_tuple_size: int | None
    status: str
    interpretation: str
    generator_a: list[list[int]]
    generator_b: list[list[int]]
    dual_generator_a: list[list[int]]
    dual_generator_b: list[list[int]]


@dataclass(frozen=True)
class BCHSearchRecord:
    spec: BCHSearchSpec
    length: int
    generated_code_count: int
    duplicate_code_count: int
    profile_key_count: int
    tuple_collision_count: int
    structural_rejection_count: int
    tuple_profile_rejection_count: int
    multiplier_equivalent_count: int
    low_weight_rejection_count: int
    dual_rejection_count: int
    dual_higher_tuple_rejection_count: int
    canonicalization_rejection_count: int
    equivalent_control_count: int
    proof_debt_collision_count: int
    no_collision_count: int
    collision_audits: list[BCHCollisionAudit]
    status: str
    interpretation: str


@dataclass(frozen=True)
class BCHCodeSearchReport:
    created_at: str
    records: list[BCHSearchRecord]
    headline_metrics: dict[str, int]
    status: str
    summary: str
    falsifiers_triggered: list[str]


DEFAULT_BCH_SPECS = [
    BCHSearchSpec("bch-m4-d3-9-shifted", 4, 3, 9, (1, 2, 3, 5, 7), 2, 8),
    BCHSearchSpec("bch-m5-d3-11-shifted", 5, 3, 11, (1, 2, 3, 5, 7, 11), 2, 10),
]


PRIMITIVE_POLYNOMIALS = {
    2: 0b111,
    3: 0b1011,
    4: 0b10011,
    5: 0b100101,
    6: 0b1000011,
}


_DUAL_TUPLE_DIGEST_CACHE: dict[tuple[Any, ...], tuple[bool, str, int, int, str]] = {}


def _poly_label(poly: int) -> str:
    return f"0b{int(poly):b}"


def gf2m_mul(left: int, right: int, extension_degree: int, modulus: int | None = None) -> int:
    if modulus is None:
        modulus = PRIMITIVE_POLYNOMIALS[extension_degree]
    product = 0
    a = int(left)
    b = int(right)
    while b:
        if b & 1:
            product ^= a
        a <<= 1
        b >>= 1
    while product.bit_length() > extension_degree:
        shift = product.bit_length() - extension_degree - 1
        product ^= modulus << shift
    return product & ((1 << extension_degree) - 1)


def primitive_power_table(extension_degree: int) -> list[int]:
    if extension_degree not in PRIMITIVE_POLYNOMIALS:
        raise ValueError(f"no primitive polynomial is configured for GF(2^{extension_degree})")
    length = (1 << extension_degree) - 1
    modulus = PRIMITIVE_POLYNOMIALS[extension_degree]
    powers = [1]
    for _ in range(1, length):
        powers.append(gf2m_mul(powers[-1], 2, extension_degree, modulus))
    if len(set(powers)) != length:
        raise ValueError(f"configured polynomial for GF(2^{extension_degree}) is not primitive")
    return powers


def cyclotomic_coset(exponent: int, length: int) -> tuple[int, ...]:
    values = []
    seen = set()
    current = int(exponent) % length
    while current not in seen:
        seen.add(current)
        values.append(current)
        current = (2 * current) % length
    return tuple(sorted(values))


def minimal_polynomial_for_coset(coset: tuple[int, ...], extension_degree: int) -> int:
    length = (1 << extension_degree) - 1
    powers = primitive_power_table(extension_degree)
    polynomial = [1]
    for exponent in coset:
        root = powers[int(exponent) % length]
        new_polynomial = [0] * (len(polynomial) + 1)
        for index, coefficient in enumerate(polynomial):
            new_polynomial[index] ^= gf2m_mul(coefficient, root, extension_degree)
            new_polynomial[index + 1] ^= coefficient
        polynomial = new_polynomial
    result = 0
    for index, coefficient in enumerate(polynomial):
        if coefficient not in {0, 1}:
            raise ValueError(f"minimal polynomial coefficient left GF(2): {coefficient}")
        if coefficient:
            result |= 1 << index
    return result


def bch_defining_cosets(
    extension_degree: int,
    designed_distance: int,
    start: int = 1,
) -> tuple[tuple[int, ...], ...]:
    length = (1 << extension_degree) - 1
    reps: dict[int, tuple[int, ...]] = {}
    for offset in range(designed_distance - 1):
        coset = cyclotomic_coset(start + offset, length)
        reps[min(coset)] = coset
    return tuple(coset for _, coset in sorted(reps.items()))


def bch_generator_polynomial(extension_degree: int, designed_distance: int, start: int = 1) -> int:
    generator = 1
    for coset in bch_defining_cosets(extension_degree, designed_distance, start=start):
        generator = poly_mul(generator, minimal_polynomial_for_coset(coset, extension_degree))
    return generator


def bch_generator_matrix(extension_degree: int, designed_distance: int, start: int = 1) -> np.ndarray:
    length = (1 << extension_degree) - 1
    return cyclic_generator_matrix(length, bch_generator_polynomial(extension_degree, designed_distance, start=start))


def _row_reduce_gf2(matrix: np.ndarray) -> np.ndarray:
    values = np.asarray(matrix, dtype=np.uint8).copy() & 1
    rows, cols = values.shape
    rank = 0
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
        rank += 1
        if rank == rows:
            break
    return values[:rank].astype(np.uint8)


def bch_dual_generator_from_descriptor(descriptor: BCHCodeDescriptor) -> np.ndarray:
    """Build a binary generator for the BCH dual from expanded parity checks."""

    extension_degree = int(descriptor.extension_degree)
    length = int(descriptor.length)
    powers = primitive_power_table(extension_degree)
    rows: list[list[int]] = []
    for exponent in sorted(int(item) for item in descriptor.defining_set):
        field_row = [powers[(exponent * coordinate) % length] for coordinate in range(length)]
        for bit in range(extension_degree):
            rows.append([(element >> bit) & 1 for element in field_row])
    if not rows:
        return np.zeros((0, length), dtype=np.uint8)
    return _row_reduce_gf2(np.asarray(rows, dtype=np.uint8))


def _descriptor_from_code(spec: BCHSearchSpec, start: int, designed_distance: int, generator_poly: int, generator: np.ndarray) -> BCHCodeDescriptor:
    cosets = bch_defining_cosets(spec.extension_degree, designed_distance, start=start)
    defining_set = sorted({exponent for coset in cosets for exponent in coset})
    return BCHCodeDescriptor(
        id=f"{spec.id}-s{start}-d{designed_distance}",
        extension_degree=spec.extension_degree,
        length=(1 << spec.extension_degree) - 1,
        start=int(start),
        designed_distance=int(designed_distance),
        dimension=int(generator.shape[0]),
        generator_poly=_poly_label(generator_poly),
        defining_set=[int(item) for item in defining_set],
        cyclotomic_cosets=[[int(item) for item in coset] for coset in cosets],
    )


def enumerate_bch_codes(spec: BCHSearchSpec) -> tuple[list[tuple[BCHCodeDescriptor, np.ndarray]], int]:
    codes: list[tuple[BCHCodeDescriptor, np.ndarray]] = []
    duplicate_count = 0
    seen_generator_polys: set[int] = set()
    for designed_distance in range(spec.min_designed_distance, spec.max_designed_distance + 1):
        for start in spec.starts:
            generator_poly = bch_generator_polynomial(spec.extension_degree, designed_distance, start=start)
            if generator_poly in seen_generator_polys:
                duplicate_count += 1
                continue
            seen_generator_polys.add(generator_poly)
            generator = cyclic_generator_matrix((1 << spec.extension_degree) - 1, generator_poly)
            codes.append((_descriptor_from_code(spec, start, designed_distance, generator_poly, generator), generator))
    return codes, duplicate_count


def defining_set_decimation_equivalence(code_a: BCHCodeDescriptor, code_b: BCHCodeDescriptor) -> DecimationEquivalence:
    if code_a.length != code_b.length or code_a.dimension != code_b.dimension:
        return DecimationEquivalence(
            equivalent=False,
            multiplier=None,
            maps_checked=0,
            interpretation="BCH rows have different length or dimension, so decimation equivalence is impossible.",
        )
    length = int(code_a.length)
    source = set(int(item) for item in code_a.defining_set)
    target = set(int(item) for item in code_b.defining_set)
    checked = 0
    for multiplier in range(1, length):
        if np.gcd(multiplier, length) != 1:
            continue
        checked += 1
        if {int((multiplier * exponent) % length) for exponent in source} == target:
            return DecimationEquivalence(
                equivalent=True,
                multiplier=int(multiplier),
                maps_checked=checked,
                interpretation=(
                    "The BCH defining sets are equivalent under a cyclotomic decimation/multiplier "
                    f"(multiplier={multiplier}); this is an algebraic automorphism control, not hardness evidence."
                ),
            )
    return DecimationEquivalence(
        equivalent=False,
        multiplier=None,
        maps_checked=checked,
        interpretation="No unit multiplier maps the first BCH defining set to the second.",
    )


def _requires_exact_codeword_baselines(left: np.ndarray, right: np.ndarray) -> bool:
    return max(int(left.shape[0]), int(right.shape[0])) <= EXACT_CODEWORD_DIMENSION_LIMIT


def _bch_algebraic_profile_key(descriptor: BCHCodeDescriptor) -> str:
    coset_sizes = tuple(sorted(len(coset) for coset in descriptor.cyclotomic_cosets))
    return repr(
        (
            "bch-algebraic-profile",
            descriptor.length,
            descriptor.dimension,
            len(descriptor.defining_set),
            coset_sizes,
        )
    )


def _canonical_pattern_count_digest(counts: Counter[tuple[int, int]], tuple_size: int) -> str:
    best: tuple[tuple[int, int, int], ...] | None = None
    for permutation in permutations(range(tuple_size)):
        transformed = []
        for (pattern, residual_weight), count in counts.items():
            new_pattern = 0
            for old_offset, new_offset in enumerate(permutation):
                if (pattern >> old_offset) & 1:
                    new_pattern |= 1 << new_offset
            transformed.append((new_pattern, residual_weight, count))
        candidate = tuple(sorted(transformed))
        if best is None or candidate < best:
            best = candidate
    return sha256(repr(best or tuple()).encode()).hexdigest()


def dual_tuple_profile_digest(
    generator: np.ndarray,
    tuple_size: int,
    tuple_cap: int = 40_000,
    max_codewords: int = 32_768,
) -> tuple[bool, str, int, int, str]:
    matrix = np.ascontiguousarray(np.asarray(generator, dtype=np.uint8) & 1)
    cache_key = (matrix.shape, matrix.tobytes(), tuple_size, tuple_cap, max_codewords)
    if cache_key in _DUAL_TUPLE_DIGEST_CACHE:
        return _DUAL_TUPLE_DIGEST_CACHE[cache_key]
    words = enumerate_unique_codewords(matrix).astype(np.uint8)
    word_count = int(words.shape[0])
    tuple_count = 1
    length = int(words.shape[1])
    for value in range(length - tuple_size + 1, length + 1):
        tuple_count *= value
    for value in range(2, tuple_size + 1):
        tuple_count //= value
    if word_count > max_codewords:
        result = (False, "skipped", tuple_count, word_count, f"Skipped {word_count} codeword(s) above cap {max_codewords}.")
        _DUAL_TUPLE_DIGEST_CACHE[cache_key] = result
        return result
    if tuple_count > tuple_cap:
        result = (False, "skipped", tuple_count, word_count, f"Skipped C({length},{tuple_size})={tuple_count} tuples above cap {tuple_cap}.")
        _DUAL_TUPLE_DIGEST_CACHE[cache_key] = result
        return result

    weights = words.sum(axis=1).astype(np.int16)
    tuple_digests = []
    for coords in combinations(range(length), tuple_size):
        patterns = np.zeros(word_count, dtype=np.int16)
        selected_weights = np.zeros(word_count, dtype=np.int16)
        for offset, coordinate in enumerate(coords):
            column = words[:, coordinate].astype(np.int16)
            patterns += column << offset
            selected_weights += column
        residual_weights = weights - selected_weights
        counts = Counter(zip(patterns.tolist(), residual_weights.tolist()))
        tuple_digests.append(_canonical_pattern_count_digest(counts, tuple_size))
    digest = sha256("|".join(sorted(tuple_digests)).encode()).hexdigest()
    result = (True, digest, tuple_count, word_count, (
        f"Computed C({length},{tuple_size})={tuple_count} tuple profile digests over {word_count} dual codeword(s)."
    ))
    _DUAL_TUPLE_DIGEST_CACHE[cache_key] = result
    return result


def _dual_higher_tuple_rejection(
    left: np.ndarray,
    right: np.ndarray,
    tuple_cap: int,
) -> tuple[bool, str, int | None]:
    candidates = [
        (3, 32_768),
        (4, 2_048),
    ]
    last_status = "dual-higher-tuple-not-evaluated"
    for tuple_size, max_codewords in candidates:
        left_eval, left_digest, tuple_count, word_count, left_cost = dual_tuple_profile_digest(
            left,
            tuple_size=tuple_size,
            tuple_cap=max(tuple_cap, 40_000),
            max_codewords=max_codewords,
        )
        right_eval, right_digest, _right_tuple_count, right_word_count, right_cost = dual_tuple_profile_digest(
            right,
            tuple_size=tuple_size,
            tuple_cap=max(tuple_cap, 40_000),
            max_codewords=max_codewords,
        )
        if left_eval and right_eval and left_digest != right_digest:
            return (
                True,
                f"rejected-by-bch-dual-{tuple_size}-tuple-profile",
                tuple_size,
            )
        if left_eval and right_eval:
            last_status = f"dual-{tuple_size}-tuple-profile-survivor"
        else:
            last_status = (
                f"dual-{tuple_size}-tuple-profile-skipped: "
                f"left=({left_cost}, tuples={tuple_count}, words={word_count}); "
                f"right=({right_cost}, words={right_word_count})"
            )
    return False, last_status, None


def _audit_dual_side_bch_collision(
    record_id: str,
    spec: BCHSearchSpec,
    code_a: BCHCodeDescriptor,
    code_b: BCHCodeDescriptor,
    canonical_max_assignments: int,
    tuple_cap: int,
) -> tuple[str, str, list[str], str, str, str, bool | None, str, int | None, np.ndarray, np.ndarray]:
    dual_a = bch_dual_generator_from_descriptor(code_a)
    dual_b = bch_dual_generator_from_descriptor(code_b)
    strong = strong_invariant_differences(dual_a, dual_b)
    if strong:
        return (
            "rejected-by-bch-dual-structural-invariant",
            "BCH high-rate primal rows are separated by structural invariants on their low-dimensional dual codes: "
            + ", ".join(strong),
            strong,
            "dual-side-structural-baseline",
            "skipped-after-earlier-baseline",
            "skipped-after-earlier-baseline",
            None,
            "skipped-after-structural-rejection",
            None,
            dual_a,
            dual_b,
        )

    left_eval, left_digest, tuple_count, word_count, left_cost = dual_tuple_profile_digest(
        dual_a,
        tuple_size=spec.tuple_size,
        tuple_cap=tuple_cap,
        max_codewords=32_768,
    )
    right_eval, right_digest, _right_tuple_count, right_word_count, right_cost = dual_tuple_profile_digest(
        dual_b,
        tuple_size=spec.tuple_size,
        tuple_cap=tuple_cap,
        max_codewords=32_768,
    )
    tuple_status = (
        (
            f"dual-tuple-profile-proof-debt: left=({left_cost}, tuples={tuple_count}, words={word_count}); "
            f"right=({right_cost}, words={right_word_count})"
        )
        if not (left_eval and right_eval)
        else "rejected-by-coordinate-tuple-profile"
        if left_digest != right_digest
        else "dual-tuple-profile-survivor"
    )
    if tuple_status == "rejected-by-coordinate-tuple-profile":
        return (
            "rejected-by-bch-dual-tuple-profile",
            "BCH high-rate primal rows are separated by higher-order tuple profiles on their dual codes.",
            [],
            tuple_status,
            "skipped-after-earlier-baseline",
            "skipped-after-earlier-baseline",
            None,
            "skipped-after-dual-tuple-rejection",
            None,
            dual_a,
            dual_b,
        )

    low_weight = audit_low_weight_structure_pair(
        CodePairInput(
            id=f"{record_id}-dual",
            row_id=f"bch-dual-family-{spec.id}",
            row_family="bch-dual-code-family",
            source="bch_code_search_dual",
            left=dual_a,
            right=dual_b,
            known_equivalent=None,
        )
    )
    if low_weight.status in {"rejected-by-low-weight-matroid-structure", "rejected-by-low-weight-incidence-isomorphism"}:
        return (
            "rejected-by-bch-dual-low-weight-structure",
            "BCH high-rate primal rows are separated by low-weight support structure on their dual codes. "
            + low_weight.interpretation,
            [],
            tuple_status,
            low_weight.status,
            "skipped-after-earlier-baseline",
            None,
            "skipped-after-low-weight-rejection",
            None,
            dual_a,
            dual_b,
        )

    higher_rejected, higher_status, higher_tuple_size = _dual_higher_tuple_rejection(
        dual_a,
        dual_b,
        tuple_cap=tuple_cap,
    )
    if higher_rejected:
        return (
            higher_status,
            f"BCH high-rate primal rows are separated by a dual {higher_tuple_size}-coordinate tuple profile digest.",
            [],
            tuple_status,
            low_weight.status,
            "skipped-after-dual-higher-tuple-rejection",
            None,
            higher_status,
            higher_tuple_size,
            dual_a,
            dual_b,
        )

    canonical = audit_code_canonicalization_pair(
        record_id=f"{record_id}-dual",
        source="bch_code_search_dual",
        left=dual_a,
        right=dual_b,
        known_equivalent=None,
        max_assignments=canonical_max_assignments,
    )
    if canonical.status.startswith("canonical-equivalent"):
        status = "bch-dual-canonical-equivalent-control"
        interpretation = "Dual-code canonicalization proves this BCH high-rate row is an equivalent control."
    elif canonical.status == "canonicalization-proof-debt":
        status = "bch-dual-canonicalization-proof-debt"
        interpretation = "BCH dual-side canonicalization exceeded the cap; the high-rate row remains proof debt."
    else:
        status = "rejected-by-bch-dual-canonicalization"
        interpretation = "Dual-code profile-pruned canonicalization rejects this BCH high-rate row."
    return (
        status,
        interpretation,
        [],
        tuple_status,
        low_weight.status,
        canonical.status,
        canonical.canonical_equal,
        higher_status,
        higher_tuple_size,
        dual_a,
        dual_b,
    )


def audit_bch_collision(
    spec: BCHSearchSpec,
    code_a: BCHCodeDescriptor,
    generator_a: np.ndarray,
    code_b: BCHCodeDescriptor,
    generator_b: np.ndarray,
    bucket_size: int,
    canonical_max_assignments: int = 200_000,
    tuple_cap: int = 50_000,
) -> BCHCollisionAudit:
    record_id = f"{code_a.id}--{code_b.id}"
    decimation = defining_set_decimation_equivalence(code_a, code_b)
    exact_ok = _requires_exact_codeword_baselines(generator_a, generator_b)
    strong: list[str] = []
    tuple_profile_status = "skipped-after-decimation-control" if decimation.equivalent else "skipped-high-dimension-bch-row"
    low_weight_status = "skipped-after-earlier-baseline"
    canonical_status = "skipped-after-earlier-baseline"
    canonical_equal: bool | None = None
    dual_generator_a = np.zeros((0, int(generator_a.shape[1])), dtype=np.uint8)
    dual_generator_b = np.zeros((0, int(generator_b.shape[1])), dtype=np.uint8)
    dual_higher_tuple_status = "not-a-dual-audit"
    dual_higher_tuple_size: int | None = None
    status: str | None = None
    interpretation = ""

    if decimation.equivalent:
        status = "equivalent-under-bch-decimation-automorphism"
        interpretation = decimation.interpretation
    elif int(generator_a.shape[0]) != int(generator_b.shape[0]):
        strong = ["dimension_mismatch"]
        status = "rejected-by-structural-code-invariant"
        interpretation = "BCH-code collision is separated by dimension mismatch."
    elif not exact_ok:
        (
            status,
            interpretation,
            strong,
            tuple_profile_status,
            low_weight_status,
            canonical_status,
            canonical_equal,
            dual_higher_tuple_status,
            dual_higher_tuple_size,
            dual_generator_a,
            dual_generator_b,
        ) = _audit_dual_side_bch_collision(
            record_id,
            spec,
            code_a,
            code_b,
            canonical_max_assignments=canonical_max_assignments,
            tuple_cap=tuple_cap,
        )
    else:
        strong = strong_invariant_differences(generator_a, generator_b)
        tuple_audit = audit_code_tuple_profile_pair(
            record_id=record_id,
            source="bch_code_search",
            left=generator_a,
            right=generator_b,
            known_equivalent=None,
            max_tuple_size=max(3, spec.tuple_size + 1),
            tuple_cap=tuple_cap,
        )
        tuple_profile_status = tuple_audit.status
    if status is None and strong:
        status = "rejected-by-structural-code-invariant"
        interpretation = "BCH-code collision is separated by structural invariants: " + ", ".join(strong)
    elif status is None and tuple_profile_status == "rejected-by-coordinate-tuple-profile":
        status = "rejected-by-coordinate-tuple-profile"
        interpretation = "BCH-code collision is separated by higher-order coordinate tuple profiles."
    elif status is None:
        low_weight = audit_low_weight_structure_pair(
            CodePairInput(
                id=record_id,
                row_id=f"bch-family-{spec.id}",
                row_family="bch-code-family",
                source="bch_code_search",
                left=generator_a,
                right=generator_b,
                known_equivalent=None,
            )
        )
        low_weight_status = low_weight.status
        if low_weight.status in {"rejected-by-low-weight-matroid-structure", "rejected-by-low-weight-incidence-isomorphism"}:
            status = low_weight.status
            interpretation = low_weight.interpretation
        else:
            canonical = audit_code_canonicalization_pair(
                record_id=record_id,
                source="bch_code_search",
                left=generator_a,
                right=generator_b,
                known_equivalent=None,
                max_assignments=canonical_max_assignments,
            )
            canonical_status = canonical.status
            canonical_equal = canonical.canonical_equal
            if canonical.status.startswith("canonical-equivalent"):
                status = "canonical-equivalent-control"
                interpretation = "Profile-pruned canonicalization proves this BCH collision is an equivalent control."
            elif canonical.status == "canonicalization-proof-debt":
                status = "bch-canonicalization-proof-debt"
                interpretation = "BCH collision survives implemented baselines but canonicalization exceeded the cap."
            else:
                status = "rejected-by-canonicalization"
                interpretation = "Profile-pruned canonicalization rejects this BCH-code collision."
    if status is None:
        raise RuntimeError("BCH collision audit did not assign a status")

    return BCHCollisionAudit(
        id=record_id,
        length=int(generator_a.shape[1]),
        dimension_a=int(generator_a.shape[0]),
        dimension_b=int(generator_b.shape[0]),
        code_a=code_a,
        code_b=code_b,
        tuple_profile_bucket_size=int(bucket_size),
        strong_distinguishing_invariants=strong,
        tuple_profile_status=tuple_profile_status,
        multiplier_affine_equivalent=bool(decimation.equivalent),
        multiplier=decimation.multiplier,
        multiplier_shift=0 if decimation.equivalent else None,
        multiplier_maps_checked=int(decimation.maps_checked),
        low_weight_status=low_weight_status,
        canonical_status=canonical_status,
        canonical_equal=canonical_equal,
        dual_dimension_a=int(dual_generator_a.shape[0]) if dual_generator_a.size else None,
        dual_dimension_b=int(dual_generator_b.shape[0]) if dual_generator_b.size else None,
        dual_higher_tuple_status=dual_higher_tuple_status,
        dual_higher_tuple_size=dual_higher_tuple_size,
        status=status,
        interpretation=interpretation,
        generator_a=[[int(bit) for bit in row] for row in generator_a.tolist()],
        generator_b=[[int(bit) for bit in row] for row in generator_b.tolist()],
        dual_generator_a=[[int(bit) for bit in row] for row in dual_generator_a.tolist()],
        dual_generator_b=[[int(bit) for bit in row] for row in dual_generator_b.tolist()],
    )


def run_bch_search_spec(
    spec: BCHSearchSpec,
    tuple_cap: int = 50_000,
    canonical_max_assignments: int = 200_000,
) -> BCHSearchRecord:
    codes, duplicate_count = enumerate_bch_codes(spec)
    buckets: dict[str, list[tuple[BCHCodeDescriptor, np.ndarray]]] = {}
    for descriptor, generator in codes:
        if _requires_exact_codeword_baselines(generator, generator):
            key = tuple_profile_key(generator, tuple_size=spec.tuple_size, tuple_cap=tuple_cap)
            if key == "skipped":
                key = _bch_algebraic_profile_key(descriptor)
        else:
            key = _bch_algebraic_profile_key(descriptor)
        buckets.setdefault(key, []).append((descriptor, generator))

    audits: list[BCHCollisionAudit] = []
    for bucket in buckets.values():
        if len(bucket) < 2:
            continue
        for (code_a, generator_a), (code_b, generator_b) in combinations(bucket, 2):
            audits.append(
                audit_bch_collision(
                    spec,
                    code_a,
                    generator_a,
                    code_b,
                    generator_b,
                    bucket_size=len(bucket),
                    canonical_max_assignments=canonical_max_assignments,
                    tuple_cap=tuple_cap,
                )
            )
            if len(audits) >= spec.max_collisions:
                break
        if len(audits) >= spec.max_collisions:
            break

    structural = sum(1 for audit in audits if audit.status == "rejected-by-structural-code-invariant")
    tuple_rejected = sum(1 for audit in audits if audit.status == "rejected-by-coordinate-tuple-profile")
    multiplier = sum(1 for audit in audits if audit.status == "equivalent-under-bch-decimation-automorphism")
    low_weight = sum(
        1
        for audit in audits
        if audit.status in {"rejected-by-low-weight-matroid-structure", "rejected-by-low-weight-incidence-isomorphism"}
    )
    dual_rejected = sum(1 for audit in audits if audit.status.startswith("rejected-by-bch-dual-"))
    dual_higher_tuple_rejected = sum(1 for audit in audits if "tuple-profile" in audit.status and audit.status.startswith("rejected-by-bch-dual-"))
    canonical_rejected = sum(1 for audit in audits if audit.status == "rejected-by-canonicalization")
    canonical_controls = sum(1 for audit in audits if audit.status in {"canonical-equivalent-control", "bch-dual-canonical-equivalent-control"})
    proof_debt = sum(1 for audit in audits if audit.status in {"bch-canonicalization-proof-debt", "bch-dual-canonicalization-proof-debt"})

    if proof_debt:
        status = "bch-code-search-proof-debt"
        interpretation = "Some BCH-code collisions survived implemented algebraic/code baselines and remain proof debt."
    elif structural or tuple_rejected or low_weight or dual_rejected or canonical_rejected:
        status = "bch-code-search-dequantized"
        interpretation = "BCH-code collisions are rejected by structural, tuple, low-weight, or canonical baselines."
    elif multiplier or canonical_controls:
        status = "bch-collisions-all-equivalent-controls"
        interpretation = "BCH-code collisions found so far are equivalent controls under decimation/canonicalization."
    else:
        status = "no-bch-code-collision-found"
        interpretation = "No nontrivial BCH tuple-profile collision was found in this parameter window."

    return BCHSearchRecord(
        spec=spec,
        length=(1 << spec.extension_degree) - 1,
        generated_code_count=len(codes),
        duplicate_code_count=int(duplicate_count),
        profile_key_count=len(buckets),
        tuple_collision_count=len(audits),
        structural_rejection_count=structural,
        tuple_profile_rejection_count=tuple_rejected,
        multiplier_equivalent_count=multiplier,
        low_weight_rejection_count=low_weight,
        dual_rejection_count=dual_rejected,
        dual_higher_tuple_rejection_count=dual_higher_tuple_rejected,
        canonicalization_rejection_count=canonical_rejected,
        equivalent_control_count=canonical_controls,
        proof_debt_collision_count=proof_debt,
        no_collision_count=1 if not audits else 0,
        collision_audits=audits,
        status=status,
        interpretation=interpretation,
    )


def run_bch_code_search(
    specs: list[BCHSearchSpec] | None = None,
    tuple_cap: int = 50_000,
    canonical_max_assignments: int = 200_000,
) -> BCHCodeSearchReport:
    records = [
        run_bch_search_spec(spec, tuple_cap=tuple_cap, canonical_max_assignments=canonical_max_assignments)
        for spec in (specs or DEFAULT_BCH_SPECS)
    ]
    metrics = {
        "search_count": len(records),
        "generated_code_count": sum(record.generated_code_count for record in records),
        "duplicate_code_count": sum(record.duplicate_code_count for record in records),
        "tuple_collision_count": sum(record.tuple_collision_count for record in records),
        "structural_rejection_count": sum(record.structural_rejection_count for record in records),
        "tuple_profile_rejection_count": sum(record.tuple_profile_rejection_count for record in records),
        "multiplier_equivalent_count": sum(record.multiplier_equivalent_count for record in records),
        "low_weight_rejection_count": sum(record.low_weight_rejection_count for record in records),
        "dual_rejection_count": sum(record.dual_rejection_count for record in records),
        "dual_higher_tuple_rejection_count": sum(record.dual_higher_tuple_rejection_count for record in records),
        "canonicalization_rejection_count": sum(record.canonicalization_rejection_count for record in records),
        "equivalent_control_count": sum(record.equivalent_control_count for record in records),
        "proof_debt_collision_count": sum(record.proof_debt_collision_count for record in records),
        "no_collision_count": sum(record.no_collision_count for record in records),
        "max_length": max((record.length for record in records), default=0),
    }
    if metrics["proof_debt_collision_count"]:
        status = "bch-code-search-proof-debt"
    elif metrics["tuple_collision_count"]:
        status = "bch-code-search-dequantized-or-controls"
    else:
        status = "bch-code-search-incomplete"
    summary = (
        f"Searched {metrics['search_count']} BCH parameter window(s), generating {metrics['generated_code_count']} unique code(s) "
        f"and {metrics['duplicate_code_count']} duplicate defining-set control(s). "
        f"Found {metrics['tuple_collision_count']} tuple-profile collision(s): "
        f"{metrics['multiplier_equivalent_count']} decimation control(s), "
        f"{metrics['equivalent_control_count']} canonical equivalent control(s), "
        f"{metrics['structural_rejection_count'] + metrics['tuple_profile_rejection_count'] + metrics['low_weight_rejection_count'] + metrics['dual_rejection_count'] + metrics['canonicalization_rejection_count']} "
        f"classical rejection(s), and {metrics['proof_debt_collision_count']} proof-debt row(s)."
    )
    falsifiers = []
    if metrics["duplicate_code_count"]:
        falsifiers.append("Many BCH defining intervals close to duplicate cyclotomic defining sets.")
    if metrics["multiplier_equivalent_count"] or metrics["equivalent_control_count"]:
        falsifiers.append("Some BCH collisions are explained by decimation/multiplier or canonical equivalence controls.")
    if (
        metrics["structural_rejection_count"]
        or metrics["tuple_profile_rejection_count"]
        or metrics["low_weight_rejection_count"]
        or metrics["dual_rejection_count"]
        or metrics["canonicalization_rejection_count"]
    ):
        falsifiers.append("Some BCH collisions are rejected by classical structural, tuple, dual-side, low-weight, or canonical baselines.")
    if metrics["no_collision_count"]:
        falsifiers.append("Some BCH parameter windows contain no nontrivial tuple-profile collision under current bounds.")
    if metrics["proof_debt_collision_count"]:
        falsifiers.append("BCH proof-debt rows require stronger canonicalization and asymptotic family evidence.")
    return BCHCodeSearchReport(utc_now(), records, metrics, status, summary, falsifiers)


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


def write_bch_code_negative_results(report: BCHCodeSearchReport) -> int:
    written = 0
    for record in report.records:
        if record.status not in {
            "bch-code-search-dequantized",
            "bch-collisions-all-equivalent-controls",
            "no-bch-code-collision-found",
        }:
            continue
        upsert_negative_result(
            NegativeResultRecord(
                id=f"BCH-CODE-SEARCH-{_safe_id(record.spec.id)}",
                source="bch_code_search.py",
                claim=f"{record.spec.id} BCH tuple-profile rows provide hard code-equivalence coset evidence.",
                reason_invalid=record.interpretation,
                lesson=(
                    "BCH algebraic structure is not hard evidence when defining sets duplicate under cyclotomic closure, "
                    "collisions are decimation controls, or rows collapse under standard code baselines."
                ),
                applies_to=["CODE-COSET-COLLECTIVE", "PO-DEQUANTIZATION", "PO-FALSIFIERS"],
                evidence=asdict(record),
            )
        )
        written += 1
    return written


def write_bch_code_search(
    output_path: Path = BCH_CODE_SEARCH_PATH,
    specs: list[BCHSearchSpec] | None = None,
    tuple_cap: int = 50_000,
    canonical_max_assignments: int = 200_000,
    write_registry: bool = True,
    registry_experiment_id: str = "EXP-CODE-BCH-ALGEBRAIC-SEARCH",
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "RESULT-CODE-BCH-ALGEBRAIC-SEARCH-LATEST",
) -> dict[str, Any]:
    report = run_bch_code_search(specs=specs, tuple_cap=tuple_cap, canonical_max_assignments=canonical_max_assignments)
    payload = _json_ready(report)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    if write_registry:
        negative_results_written = write_bch_code_negative_results(report)
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
                artifacts={"bch_code_search": str(output_path)},
            )
        )
    return payload
