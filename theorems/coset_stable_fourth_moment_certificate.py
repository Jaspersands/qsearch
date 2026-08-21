"""Resumable exact fourth-moment certificate for the stable Racah block.

Tr(H^4) fixes one orbit term and leaves three relative terms.  A naive labeled
enumeration has 27,787,968 cases.  Outside points are instead encoded by their
three-bit incidence mask across the relative supports.  Multinomial weights
recover the labeled count exactly and reduce canonicalization to roughly
810,000 weighted cases, which collapse to 1,628 simultaneous-conjugacy
classes.

The per-class falling-cycle calculation is intentionally checkpointed: the
largest support-twelve class contains hundreds of millions of canonical
patterns.  A completed checkpoint proves the stable symbolic identity for
n>=20, while exact finite evaluations close n=7..19.  Newton's fourth identity
then determines the determinant of the multiplicity-four block.  Root
separation, coherent implementation, and decoding remain separate obligations.
"""

from __future__ import annotations

import itertools
import json
import math
import multiprocessing
import os
from collections import Counter
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import asdict, dataclass
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from typing import Iterable

import sympy as sp

from coset_stable_second_moment_certificate import _compose, _cycle_permutation
from coset_stable_third_moment_certificate import (
    FIRST_POWER_TRACE,
    SECOND_CHARACTERISTIC_COEFFICIENT,
    SECOND_POWER_TRACE,
    SPARSE_QUARTIC_REFERENCES,
    PatternCoefficient,
    ShiftPair,
    canonical_shift_pair,
    exact_correlation_from_patterns,
    shifted_character_pattern_coefficients,
    symbolic_correlation_from_patterns,
)
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


COSET_STABLE_FOURTH_MOMENT_PATH = Path(
    "research/representation/coset_stable_fourth_moment_certificate.json"
)
COSET_STABLE_FOURTH_PATTERN_PATH = Path(
    "research/representation/coset_stable_fourth_moment_patterns.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-STABLE-FOURTH-MOMENT-CERTIFICATE"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
CHECKPOINT_SCHEMA_VERSION = 1

THIRD_POWER_TRACE = (
    4 * sp.Symbol("n") ** 9
    - 138 * sp.Symbol("n") ** 8
    + 2037 * sp.Symbol("n") ** 7
    - 16798 * sp.Symbol("n") ** 6
    + 84810 * sp.Symbol("n") ** 5
    - 270165 * sp.Symbol("n") ** 4
    + 539231 * sp.Symbol("n") ** 3
    - 646446 * sp.Symbol("n") ** 2
    + 422442 * sp.Symbol("n")
    - 115228
)
THIRD_CHARACTERISTIC_COEFFICIENT = (
    4 * sp.Symbol("n") ** 9
    - 138 * sp.Symbol("n") ** 8
    + 2033 * sp.Symbol("n") ** 7
    - 16692 * sp.Symbol("n") ** 6
    + 83608 * sp.Symbol("n") ** 5
    - 262838 * sp.Symbol("n") ** 4
    + 514175 * sp.Symbol("n") ** 3
    - 599392 * sp.Symbol("n") ** 2
    + 377636 * sp.Symbol("n")
    - 98432
)

EXPECTED_RAW_COUNTS_BY_OUTSIDE_SUPPORT = (
    216,
    13_608,
    188_568,
    1_121_256,
    3_589_920,
    6_816_960,
    7_938_000,
    5_579_280,
    2_177_280,
    362_880,
)


@dataclass(frozen=True)
class FourthRelativeOrbitClassRecord:
    left_shift: tuple[int, ...]
    right_shift: tuple[int, ...]
    active_support_size: int
    multiplicities_by_outside_support_count: tuple[
        int, int, int, int, int, int, int, int, int, int
    ]
    symbolic_multiplicity: str
    nonzero_pattern_coefficient_count: int
    raw_canonical_pattern_count: int
    shifted_character_correlation: str


@dataclass(frozen=True)
class FourthMomentEndpointRecord:
    n: int
    exact_pattern_trace: int
    formula_trace: int
    trace_residual: int
    determinant: int
    sparse_reference_determinant: int | None
    sparse_reference_residual: int | None
    verified: bool


@dataclass(frozen=True)
class StableFourthMomentCertificate:
    created_at: str
    theorem: dict[str, object]
    relative_orbit_certificate: dict[str, object]
    pattern_checkpoint_certificate: dict[str, object]
    class_records: list[FourthRelativeOrbitClassRecord]
    stable_symbolic_certificate: dict[str, object]
    endpoint_records: list[FourthMomentEndpointRecord]
    newton_certificate: dict[str, object]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _orbit_terms(
    ambient_size: int, support: tuple[int, int, int]
) -> Iterable[ShiftPair]:
    for transposition_support in itertools.combinations(support, 2):
        transposition = _cycle_permutation(ambient_size, transposition_support)
        for cycle_support in (support, (support[0], support[2], support[1])):
            yield transposition, _cycle_permutation(ambient_size, cycle_support)


def _outside_count_vectors(
    required_column_sizes: tuple[int, int, int],
) -> Iterable[tuple[int, int, int, int, int, int, int]]:
    counts = [0] * 7

    def visit(mask: int, remaining: tuple[int, int, int]) -> Iterable[tuple[int, ...]]:
        if mask == 8:
            if remaining == (0, 0, 0):
                yield tuple(counts)
            return
        columns = tuple(index for index in range(3) if mask & (1 << index))
        maximum = min((remaining[index] for index in columns), default=0)
        for count in range(maximum + 1):
            next_remaining = tuple(
                remaining[index] - (count if index in columns else 0)
                for index in range(3)
            )
            counts[mask - 1] = count
            yield from visit(mask + 1, next_remaining)
        counts[mask - 1] = 0

    yield from visit(1, required_column_sizes)


def fourth_support_incidence_patterns() -> Iterable[
    tuple[
        tuple[int, int, int],
        tuple[int, int, int, int, int, int, int],
        int,
        int,
    ]
]:
    """Yield inside masks, outside-mask counts, outside size, and label weight."""

    for inside_masks in itertools.product(range(8), repeat=3):
        inside_column_sizes = tuple(
            sum(bool(mask & (1 << column)) for mask in inside_masks)
            for column in range(3)
        )
        required = tuple(3 - size for size in inside_column_sizes)
        if min(required) < 0:
            continue
        for outside_counts in _outside_count_vectors(required):
            outside_count = sum(outside_counts)
            weight = math.factorial(outside_count) // math.prod(
                math.factorial(count) for count in outside_counts
            )
            yield inside_masks, outside_counts, outside_count, weight


def _supports_from_incidence(
    inside_masks: tuple[int, int, int],
    outside_counts: tuple[int, int, int, int, int, int, int],
) -> tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]:
    supports: list[list[int]] = [[], [], []]
    for point, mask in enumerate(inside_masks):
        for column in range(3):
            if mask & (1 << column):
                supports[column].append(point)
    point = 3
    for mask, count in enumerate(outside_counts, start=1):
        for _ in range(count):
            for column in range(3):
                if mask & (1 << column):
                    supports[column].append(point)
            point += 1
    if any(len(support) != 3 for support in supports):
        raise ArithmeticError("incidence pattern did not produce three 3-supports")
    return tuple(tuple(support) for support in supports)  # type: ignore[return-value]


@lru_cache(maxsize=1)
def fourth_relative_orbit_class_counts() -> dict[
    ShiftPair, tuple[int, int, int, int, int, int, int, int, int, int]
]:
    ambient_size = 12
    base_transposition = _cycle_permutation(ambient_size, (0, 1))
    base_cycle = _cycle_permutation(ambient_size, (0, 1, 2))
    counts_by_outside: list[Counter[ShiftPair]] = [Counter() for _ in range(10)]
    for inside_masks, outside_counts, outside_count, weight in (
        fourth_support_incidence_patterns()
    ):
        supports = _supports_from_incidence(inside_masks, outside_counts)
        orbit_terms = [tuple(_orbit_terms(ambient_size, support)) for support in supports]
        for first, second, third in itertools.product(*orbit_terms):
            class_key = canonical_shift_pair(
                _compose(
                    _compose(_compose(base_transposition, first[0]), second[0]),
                    third[0],
                ),
                _compose(
                    _compose(_compose(base_cycle, first[1]), second[1]), third[1]
                ),
            )
            counts_by_outside[outside_count][class_key] += weight
    all_classes = set().union(*(set(counts) for counts in counts_by_outside))
    return {
        class_key: tuple(
            int(counts_by_outside[outside].get(class_key, 0))
            for outside in range(10)
        )
        for class_key in sorted(all_classes)
    }


def _class_key_text(class_key: ShiftPair) -> str:
    return ",".join(map(str, class_key[0])) + "|" + ",".join(
        map(str, class_key[1])
    )


def _serialize_summary(
    class_key: ShiftPair,
    summary: tuple[tuple[PatternCoefficient, ...], int],
) -> dict[str, object]:
    coefficients, raw_count = summary
    return {
        "left_shift": list(class_key[0]),
        "right_shift": list(class_key[1]),
        "coefficients": [
            [
                generic_count,
                constraint_count,
                coefficient.numerator,
                coefficient.denominator,
            ]
            for generic_count, constraint_count, coefficient in coefficients
        ],
        "raw_canonical_pattern_count": raw_count,
    }


def _deserialize_summary(
    payload: dict[str, object],
) -> tuple[ShiftPair, tuple[tuple[PatternCoefficient, ...], int]]:
    class_key = (
        tuple(int(value) for value in payload["left_shift"]),  # type: ignore[arg-type]
        tuple(int(value) for value in payload["right_shift"]),  # type: ignore[arg-type]
    )
    coefficients = tuple(
        (int(row[0]), int(row[1]), Fraction(int(row[2]), int(row[3])))
        for row in payload["coefficients"]  # type: ignore[union-attr]
    )
    return class_key, (
        coefficients,
        int(payload["raw_canonical_pattern_count"]),
    )


def load_pattern_checkpoint(
    checkpoint_path: Path = COSET_STABLE_FOURTH_PATTERN_PATH,
) -> dict[ShiftPair, tuple[tuple[PatternCoefficient, ...], int]]:
    try:
        payload = json.loads(checkpoint_path.read_text())
    except (OSError, json.JSONDecodeError):
        return {}
    if payload.get("schema_version") != CHECKPOINT_SCHEMA_VERSION:
        raise ValueError("unsupported fourth-moment checkpoint schema")
    summaries = {}
    for record in payload.get("summaries", {}).values():
        class_key, summary = _deserialize_summary(record)
        summaries[class_key] = summary
    return summaries


def write_pattern_checkpoint(
    summaries: dict[ShiftPair, tuple[tuple[PatternCoefficient, ...], int]],
    checkpoint_path: Path = COSET_STABLE_FOURTH_PATTERN_PATH,
) -> None:
    classes = fourth_relative_orbit_class_counts()
    payload = {
        "schema_version": CHECKPOINT_SCHEMA_VERSION,
        "class_count": len(classes),
        "completed_class_count": len(summaries),
        "complete": len(summaries) == len(classes),
        "summaries": {
            _class_key_text(class_key): _serialize_summary(class_key, summary)
            for class_key, summary in sorted(summaries.items())
        },
    }
    checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = checkpoint_path.with_suffix(checkpoint_path.suffix + ".tmp")
    temporary_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    temporary_path.replace(checkpoint_path)


def _pattern_worker(
    class_key: ShiftPair,
) -> tuple[ShiftPair, tuple[PatternCoefficient, ...], int]:
    coefficients, raw_count = shifted_character_pattern_coefficients(*class_key)
    return class_key, coefficients, raw_count


def compute_fourth_pattern_checkpoint(
    checkpoint_path: Path = COSET_STABLE_FOURTH_PATTERN_PATH,
    workers: int | None = None,
    resume: bool = True,
    maximum_new_classes: int | None = None,
) -> dict[ShiftPair, tuple[tuple[PatternCoefficient, ...], int]]:
    classes = fourth_relative_orbit_class_counts()
    summaries = load_pattern_checkpoint(checkpoint_path) if resume else {}
    invalid = set(summaries) - set(classes)
    if invalid:
        raise ValueError("checkpoint contains classes outside the fourth orbit")
    missing = sorted(
        set(classes) - set(summaries),
        key=lambda class_key: (-len(class_key[0]), class_key),
    )
    if maximum_new_classes is not None:
        missing = missing[:maximum_new_classes]
    if not missing:
        write_pattern_checkpoint(summaries, checkpoint_path)
        return summaries
    worker_count = workers if workers is not None else min(8, os.cpu_count() or 1)
    print(
        f"Fourth-moment patterns: {len(summaries)}/{len(classes)} complete; "
        f"evaluating {len(missing)} with {worker_count} workers",
        flush=True,
    )
    if worker_count <= 1:
        for index, class_key in enumerate(missing, start=1):
            summaries[class_key] = shifted_character_pattern_coefficients(*class_key)
            write_pattern_checkpoint(summaries, checkpoint_path)
            print(
                f"Fourth-moment patterns: {len(summaries)}/{len(classes)} complete "
                f"(new {index}/{len(missing)}, support {len(class_key[0])})",
                flush=True,
            )
        return summaries
    context = multiprocessing.get_context("fork")
    with ProcessPoolExecutor(max_workers=worker_count, mp_context=context) as executor:
        futures = {executor.submit(_pattern_worker, class_key): class_key for class_key in missing}
        completed = 0
        for future in as_completed(futures):
            class_key, coefficients, raw_count = future.result()
            summaries[class_key] = (coefficients, raw_count)
            completed += 1
            write_pattern_checkpoint(summaries, checkpoint_path)
            print(
                f"Fourth-moment patterns: {len(summaries)}/{len(classes)} complete "
                f"(new {completed}/{len(missing)}, support {len(class_key[0])}, raw {raw_count})",
                flush=True,
            )
    return summaries


def exact_endpoint_fourth_power_trace(
    n: int,
    summaries: dict[ShiftPair, tuple[tuple[PatternCoefficient, ...], int]],
) -> int:
    if n < 7:
        raise ValueError("the multiplicity-four stable channel starts at n=7")
    relative_sum = Fraction(0)
    for class_key, multiplicities in fourth_relative_orbit_class_counts().items():
        multiplicity = sum(
            count * math.comb(n - 3, outside_count)
            for outside_count, count in enumerate(multiplicities)
            if outside_count <= n - 3
        )
        if not multiplicity:
            continue
        coefficients, _ = summaries[class_key]
        relative_sum += multiplicity * exact_correlation_from_patterns(
            n, class_key[0], coefficients
        )
    value = n * (n - 1) * (n - 2) * relative_sum
    if value.denominator != 1:
        raise ArithmeticError("fourth power trace is not integral")
    return value.numerator


@lru_cache(maxsize=4)
def build_stable_fourth_moment_certificate(
    checkpoint_path: Path = COSET_STABLE_FOURTH_PATTERN_PATH,
    workers: int | None = None,
    resume: bool = True,
) -> StableFourthMomentCertificate:
    n = sp.symbols("n", integer=True, positive=True)
    classes = fourth_relative_orbit_class_counts()
    summaries = compute_fourth_pattern_checkpoint(
        checkpoint_path=checkpoint_path, workers=workers, resume=resume
    )
    missing = set(classes) - set(summaries)
    if missing:
        raise RuntimeError(
            f"fourth-moment checkpoint incomplete: {len(summaries)}/{len(classes)} classes"
        )
    orbit_size = n * (n - 1) * (n - 2)
    total = sp.Integer(0)
    class_records: list[FourthRelativeOrbitClassRecord] = []
    for class_key, multiplicities in classes.items():
        coefficients, raw_pattern_count = summaries[class_key]
        symbolic_multiplicity = sum(
            multiplicity * sp.binomial(n - 3, outside_count)
            for outside_count, multiplicity in enumerate(multiplicities)
        )
        correlation = symbolic_correlation_from_patterns(
            class_key[0], coefficients
        )
        total += symbolic_multiplicity * correlation
        class_records.append(
            FourthRelativeOrbitClassRecord(
                left_shift=class_key[0],
                right_shift=class_key[1],
                active_support_size=len(class_key[0]),
                multiplicities_by_outside_support_count=multiplicities,
                symbolic_multiplicity=str(symbolic_multiplicity),
                nonzero_pattern_coefficient_count=len(coefficients),
                raw_canonical_pattern_count=raw_pattern_count,
                shifted_character_correlation=str(correlation),
            )
        )
    fourth_trace = sp.factor(sp.cancel(sp.expand_func(orbit_size * total)))
    numerator, denominator = sp.together(fourth_trace).as_numer_denom()
    stable_polynomial_proved = denominator == 1 and sp.Poly(numerator, n).degree() <= 12
    first_trace = FIRST_POWER_TRACE.subs(sp.Symbol("n"), n)
    second_trace = SECOND_POWER_TRACE.subs(sp.Symbol("n"), n)
    second_coefficient = SECOND_CHARACTERISTIC_COEFFICIENT.subs(sp.Symbol("n"), n)
    third_trace = THIRD_POWER_TRACE.subs(sp.Symbol("n"), n)
    third_coefficient = THIRD_CHARACTERISTIC_COEFFICIENT.subs(sp.Symbol("n"), n)
    determinant = sp.factor(
        (-fourth_trace + first_trace * third_trace - second_coefficient * second_trace + third_coefficient * first_trace)
        / 4
    )
    determinant_numerator, determinant_denominator = sp.together(
        determinant
    ).as_numer_denom()
    newton_polynomial_proved = (
        determinant_denominator == 1
        and sp.Poly(determinant_numerator, n).degree() <= 12
    )
    endpoints: list[FourthMomentEndpointRecord] = []
    for endpoint_n in range(7, 20):
        exact_trace = exact_endpoint_fourth_power_trace(endpoint_n, summaries)
        formula_trace = int(fourth_trace.subs(n, endpoint_n))
        endpoint_determinant = int(determinant.subs(n, endpoint_n))
        sparse_reference = SPARSE_QUARTIC_REFERENCES.get(endpoint_n)
        sparse_determinant = sparse_reference[4] if sparse_reference else None
        sparse_residual = (
            endpoint_determinant - sparse_determinant
            if sparse_determinant is not None
            else None
        )
        endpoints.append(
            FourthMomentEndpointRecord(
                n=endpoint_n,
                exact_pattern_trace=exact_trace,
                formula_trace=formula_trace,
                trace_residual=exact_trace - formula_trace,
                determinant=endpoint_determinant,
                sparse_reference_determinant=sparse_determinant,
                sparse_reference_residual=sparse_residual,
                verified=(
                    exact_trace == formula_trace
                    and (sparse_residual is None or sparse_residual == 0)
                ),
            )
        )
    raw_counts = tuple(
        sum(multiplicities[outside] for multiplicities in classes.values())
        for outside in range(10)
    )
    orbit_classification_proved = (
        len(classes) == 1628 and raw_counts == EXPECTED_RAW_COUNTS_BY_OUTSIDE_SUPPORT
    )
    endpoints_proved = all(record.verified for record in endpoints)
    theorem_proved = (
        orbit_classification_proved
        and stable_polynomial_proved
        and endpoints_proved
        and newton_polynomial_proved
    )
    metrics: dict[str, int | float] = {
        "exact_fourth_power_trace_theorem_count": int(theorem_proved),
        "exact_determinant_theorem_count": int(theorem_proved),
        "relative_orbit_class_count": len(classes),
        "raw_relative_term_type_count": sum(raw_counts),
        "maximum_active_support_size": max(len(class_key[0]) for class_key in classes),
        "completed_pattern_class_count": len(summaries),
        "nonzero_pattern_coefficient_count": sum(
            len(coefficients) for coefficients, _ in summaries.values()
        ),
        "raw_canonical_pattern_count": sum(
            raw_count for _, raw_count in summaries.values()
        ),
        "stable_symbolic_minimum_n": 20,
        "exact_endpoint_verified_count": sum(record.verified for record in endpoints),
        "sparse_quartic_reference_match_count": sum(
            record.sparse_reference_residual == 0
            for record in endpoints
            if record.sparse_reference_residual is not None
        ),
        "proved_quartic_coefficient_count": 4 if theorem_proved else 3,
        "required_quartic_coefficient_count": 4,
        "all_n_quartic_theorem_count": int(theorem_proved),
        "all_n_root_separation_theorem_count": 0,
        "uniform_polynomial_racah_circuit_count": 0,
        "hidden_involution_decoder_count": 0,
    }
    return StableFourthMomentCertificate(
        created_at=utc_now(),
        theorem={
            "range": "every integer n>=7",
            "fourth_power_trace": str(fourth_trace),
            "determinant": str(determinant),
            "statement": (
                "The stable multiplicity-four hierarchical orbit Hamiltonian has the displayed exact Tr(H^4) and determinant."
            ),
            "proved": theorem_proved,
        },
        relative_orbit_certificate={
            "fixed_first_term": "tau_0=(1 2), c_0=(1 2 3)",
            "remaining_relative_term_count": "[n(n-1)(n-2)]^3",
            "classification": (
                "simultaneous conjugacy class of (tau_0 tau_1 tau_2 tau_3,c_0 c_1 c_2 c_3), with outside points grouped by three-support incidence masks"
            ),
            "relative_orbit_class_count": len(classes),
            "raw_counts_by_outside_support": list(raw_counts),
            "expected_raw_counts_by_outside_support": list(
                EXPECTED_RAW_COUNTS_BY_OUTSIDE_SUPPORT
            ),
            "classification_verified": orbit_classification_proved,
        },
        pattern_checkpoint_certificate={
            "path": str(checkpoint_path),
            "schema_version": CHECKPOINT_SCHEMA_VERSION,
            "completed_class_count": len(summaries),
            "required_class_count": len(classes),
            "complete": len(summaries) == len(classes),
            "checkpointed_incrementally": True,
        },
        class_records=class_records,
        stable_symbolic_certificate={
            "literal_range": "n>=20",
            "reason": (
                "at most twelve marked shift-support points and eight selected falling-cycle points occur"
            ),
            "fourth_power_trace": str(fourth_trace),
            "polynomial_degree": (
                int(sp.Poly(fourth_trace, n).degree())
                if stable_polynomial_proved
                else -1
            ),
            "identity_verified": stable_polynomial_proved,
            "interpolation_used": False,
        },
        endpoint_records=endpoints,
        newton_certificate={
            "identity": "p4 - e1*p3 + e2*p2 - e3*p1 + 4*e4 = 0",
            "determinant": str(determinant),
            "identity_verified": newton_polynomial_proved,
        },
        headline_metrics=metrics,
        claim_gate={
            "fourth_power_trace_proved": theorem_proved,
            "determinant_proved": theorem_proved,
            "full_quartic_proved": theorem_proved,
            "all_n_root_separation_proved": False,
            "uniform_polynomial_racah_circuit_proved": False,
            "hidden_involution_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Even a complete exact quartic does not prove normalized root separation, a coherent polynomial-size "
                "Racah implementation, or a hidden-involution decoder."
            ),
        },
        status=(
            "stable-quartic-proved-root-separation-open"
            if theorem_proved
            else "stable-fourth-moment-certificate-failed"
        ),
        summary=(
            "Proved the complete all-n stable quartic through 1,628 exact relative classes; root separation and "
            "algorithmic obligations remain open."
            if theorem_proved
            else "The fourth-moment certificate failed an orbit, endpoint, polynomial, or Newton check."
        ),
        falsifiers_triggered=[
            "A complete characteristic polynomial does not itself prove inverse-polynomial normalized root separation.",
            "One stable multiplicity-four channel does not cover every decoder-relevant sector.",
            "Exact spectral labels do not supply a coherent polynomial-size Racah transform.",
            "No measurement outcome has been connected to a hidden-involution decoder.",
        ],
    )


def write_stable_fourth_moment_certificate(
    output_path: Path = COSET_STABLE_FOURTH_MOMENT_PATH,
    checkpoint_path: Path = COSET_STABLE_FOURTH_PATTERN_PATH,
    workers: int | None = None,
    resume: bool = True,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(
        build_stable_fourth_moment_certificate(
            checkpoint_path=checkpoint_path, workers=workers, resume=resume
        )
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-COMPLETE-QUARTIC-AS-RACAH-ALGORITHM",
                source=str(output_path),
                claim=(
                    "A complete exact stable Racah quartic establishes an efficient collective measurement or speedup."
                ),
                reason_invalid=(
                    "Root separation, uniform coherent implementation, sector coverage, and hidden-involution decoding remain open."
                ),
                lesson=(
                    "Use the exact quartic to prove or falsify normalized root separation, then address circuit synthesis and decoder information."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence=payload["headline_metrics"],
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
                artifacts={
                    "coset_stable_fourth_moment_certificate": str(output_path),
                    "coset_stable_fourth_moment_patterns": str(checkpoint_path),
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_stable_fourth_moment_certificate()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
