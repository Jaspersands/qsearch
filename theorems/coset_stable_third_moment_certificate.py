"""Exact third power trace for the stable hierarchical Racah Hamiltonian.

Fixing one orbit term in Tr(H^3) leaves two relative orbit terms.  Their
products reduce to simultaneous-conjugacy classes of a pair of permutations.
The canonicalizer below treats that pair as a two-colored directed graph, so
support-nine classes do not require a factorial relabeling search.

Each class is evaluated by the falling-cycle equality-pattern engine from the
second-moment certificate.  The stable symbolic identity is literal once the
nine marked support points and at most eight selected cycle points fit, i.e.
for n>=17.  Exact finite pattern counts close n=7..16.  Newton's third identity
then proves the cubic characteristic coefficient of the multiplicity-four
Racah block.  The determinant, root separation, coherent implementation, and
decoder remain open.
"""

from __future__ import annotations

import itertools
import json
import math
import multiprocessing
import os
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict, dataclass
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from typing import Iterable

import sympy as sp

from coset_stable_second_moment_certificate import (
    _compose,
    _cycle_permutation,
    generalized_equality_pattern_counts,
)
from coset_stable_trace_certificate import W_CHARACTER_TERMS, XI_CHARACTER_TERMS
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


COSET_STABLE_THIRD_MOMENT_PATH = Path(
    "research/representation/coset_stable_third_moment_certificate.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-STABLE-THIRD-MOMENT-CERTIFICATE"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

FIRST_POWER_TRACE = (
    4 * sp.Symbol("n") ** 3
    - 46 * sp.Symbol("n") ** 2
    + 149 * sp.Symbol("n")
    - 118
)
SECOND_POWER_TRACE = (
    4 * sp.Symbol("n") ** 6
    - 92 * sp.Symbol("n") ** 5
    + 828 * sp.Symbol("n") ** 4
    - 3678 * sp.Symbol("n") ** 3
    + 8355 * sp.Symbol("n") ** 2
    - 8992 * sp.Symbol("n")
    + 3624
)
SECOND_CHARACTERISTIC_COEFFICIENT = (
    6 * sp.Symbol("n") ** 6
    - 138 * sp.Symbol("n") ** 5
    + 1240 * sp.Symbol("n") ** 4
    - 5487 * sp.Symbol("n") ** 3
    + 12351 * sp.Symbol("n") ** 2
    - 13086 * sp.Symbol("n")
    + 5150
)

SPARSE_QUARTIC_REFERENCES: dict[int, tuple[int, int, int, int, int]] = {
    7: (1, -43, 474, -156, -10_368),
    8: (1, -178, 11_502, -319_136, 3_196_760),
    9: (1, -413, 63_308, -4_269_052, 106_851_552),
    10: (1, -772, 222_390, -28_333_728, 1_347_172_992),
    11: (1, -1_279, 611_646, -129_624_524, 10_272_159_200),
}


ShiftPair = tuple[tuple[int, ...], tuple[int, ...]]
PatternCoefficient = tuple[int, int, Fraction]


@dataclass(frozen=True)
class ThirdRelativeOrbitClassRecord:
    left_shift: tuple[int, ...]
    right_shift: tuple[int, ...]
    active_support_size: int
    multiplicities_by_outside_support_count: tuple[int, int, int, int, int, int, int]
    symbolic_multiplicity: str
    nonzero_pattern_coefficient_count: int
    raw_canonical_pattern_count: int
    shifted_character_correlation: str


@dataclass(frozen=True)
class ThirdMomentEndpointRecord:
    n: int
    exact_pattern_trace: int
    formula_trace: int
    trace_residual: int
    third_characteristic_coefficient: int
    sparse_reference_coefficient: int | None
    sparse_reference_residual: int | None
    verified: bool


@dataclass(frozen=True)
class StableThirdMomentCertificate:
    created_at: str
    theorem: dict[str, object]
    relative_orbit_certificate: dict[str, object]
    class_records: list[ThirdRelativeOrbitClassRecord]
    stable_symbolic_certificate: dict[str, object]
    endpoint_records: list[ThirdMomentEndpointRecord]
    newton_certificate: dict[str, object]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _inverse(permutation: tuple[int, ...]) -> tuple[int, ...]:
    inverse = [0] * len(permutation)
    for source, target in enumerate(permutation):
        inverse[target] = source
    return tuple(inverse)


def canonical_shift_pair(left: tuple[int, ...], right: tuple[int, ...]) -> ShiftPair:
    """Canonicalize a permutation pair under simultaneous conjugation.

    A rooted connected two-colored permutation graph has a deterministic BFS
    labeling using the generators left, right and their inverses.  Minimizing
    over roots and sorting connected component codes gives an exact unrooted
    canonical form in polynomial time in the active support size.
    """

    if len(left) != len(right):
        raise ValueError("shift permutations must have equal size")
    active = {
        index
        for index in range(len(left))
        if left[index] != index or right[index] != index
    }
    if not active:
        return (), ()
    left_inverse = _inverse(left)
    right_inverse = _inverse(right)
    unseen = set(active)
    component_codes: list[ShiftPair] = []
    while unseen:
        seed = next(iter(unseen))
        component: set[int] = set()
        stack = [seed]
        while stack:
            vertex = stack.pop()
            if vertex in component:
                continue
            component.add(vertex)
            stack.extend(
                (
                    left[vertex],
                    right[vertex],
                    left_inverse[vertex],
                    right_inverse[vertex],
                )
            )
        unseen.difference_update(component)
        best: ShiftPair | None = None
        for root in component:
            labels = {root: 0}
            queue = [root]
            for vertex in queue:
                for permutation in (left, right, left_inverse, right_inverse):
                    neighbor = permutation[vertex]
                    if neighbor not in labels:
                        labels[neighbor] = len(labels)
                        queue.append(neighbor)
            canonical_left = [0] * len(component)
            canonical_right = [0] * len(component)
            for vertex, label in labels.items():
                canonical_left[label] = labels[left[vertex]]
                canonical_right[label] = labels[right[vertex]]
            candidate = (tuple(canonical_left), tuple(canonical_right))
            if best is None or candidate < best:
                best = candidate
        if best is None:
            raise ArithmeticError("failed to canonicalize connected component")
        component_codes.append(best)
    component_codes.sort()
    canonical_left: list[int] = []
    canonical_right: list[int] = []
    offset = 0
    for component_left, component_right in component_codes:
        canonical_left.extend(offset + value for value in component_left)
        canonical_right.extend(offset + value for value in component_right)
        offset += len(component_left)
    return tuple(canonical_left), tuple(canonical_right)


def _orbit_terms(
    ambient_size: int, support: tuple[int, int, int]
) -> Iterable[ShiftPair]:
    for transposition_support in itertools.combinations(support, 2):
        transposition = _cycle_permutation(ambient_size, transposition_support)
        for cycle_support in (support, (support[0], support[2], support[1])):
            yield transposition, _cycle_permutation(ambient_size, cycle_support)


@lru_cache(maxsize=1)
def third_relative_orbit_class_counts() -> dict[
    ShiftPair, tuple[int, int, int, int, int, int, int]
]:
    ambient_size = 9
    base_transposition = _cycle_permutation(ambient_size, (0, 1))
    base_cycle = _cycle_permutation(ambient_size, (0, 1, 2))
    counts_by_outside: list[Counter[ShiftPair]] = []
    all_classes: set[ShiftPair] = set()
    base_support = {0, 1, 2}
    for outside_count in range(7):
        counts: Counter[ShiftPair] = Counter()
        universe = range(3 + outside_count)
        outside = set(range(3, 3 + outside_count))
        supports = list(itertools.combinations(universe, 3))
        for first_support in supports:
            for second_support in supports:
                if (set(first_support) | set(second_support)) - base_support != outside:
                    continue
                for first_transposition, first_cycle in _orbit_terms(
                    ambient_size, first_support
                ):
                    for second_transposition, second_cycle in _orbit_terms(
                        ambient_size, second_support
                    ):
                        class_key = canonical_shift_pair(
                            _compose(
                                _compose(base_transposition, first_transposition),
                                second_transposition,
                            ),
                            _compose(
                                _compose(base_cycle, first_cycle), second_cycle
                            ),
                        )
                        counts[class_key] += 1
                        all_classes.add(class_key)
        counts_by_outside.append(counts)
    return {
        class_key: tuple(
            int(counts_by_outside[outside].get(class_key, 0))
            for outside in range(7)
        )
        for class_key in sorted(all_classes)
    }


@lru_cache(maxsize=None)
def shifted_character_pattern_coefficients(
    left_shift: tuple[int, ...], right_shift: tuple[int, ...]
) -> tuple[tuple[PatternCoefficient, ...], int]:
    coefficients: defaultdict[tuple[int, int], Fraction] = defaultdict(Fraction)
    raw_pattern_count = 0
    for first, first_coefficient in XI_CHARACTER_TERMS:
        for second, second_coefficient in XI_CHARACTER_TERMS:
            for third, third_coefficient in W_CHARACTER_TERMS:
                rotation_denominator = math.prod((*first, *second, *third))
                character_coefficient = (
                    first_coefficient
                    * second_coefficient
                    * third_coefficient
                    / rotation_denominator
                )
                pattern_counts = generalized_equality_pattern_counts(
                    first, second, third, left_shift, right_shift
                )
                raw_pattern_count += sum(count for _, count in pattern_counts)
                for key, pattern_count in pattern_counts:
                    coefficients[key] += character_coefficient * pattern_count
    return (
        tuple(
            (generic_count, constraint_count, coefficient)
            for (generic_count, constraint_count), coefficient in sorted(
                coefficients.items()
            )
            if coefficient
        ),
        raw_pattern_count,
    )


def _pattern_worker(
    class_key: ShiftPair,
) -> tuple[ShiftPair, tuple[PatternCoefficient, ...], int]:
    coefficients, raw_count = shifted_character_pattern_coefficients(*class_key)
    return class_key, coefficients, raw_count


def all_class_pattern_summaries(
    workers: int | None = None,
) -> dict[ShiftPair, tuple[tuple[PatternCoefficient, ...], int]]:
    class_keys = list(third_relative_orbit_class_counts())
    worker_count = workers if workers is not None else min(8, os.cpu_count() or 1)
    if worker_count <= 1:
        return {
            class_key: shifted_character_pattern_coefficients(*class_key)
            for class_key in class_keys
        }
    context = multiprocessing.get_context("fork")
    with ProcessPoolExecutor(
        max_workers=worker_count, mp_context=context
    ) as executor:
        records = executor.map(_pattern_worker, class_keys, chunksize=1)
        return {
            class_key: (coefficients, raw_count)
            for class_key, coefficients, raw_count in records
        }


def _falling(value: sp.Expr, count: int) -> sp.Expr:
    return sp.prod(value - offset for offset in range(count))


def symbolic_correlation_from_patterns(
    left_shift: tuple[int, ...], coefficients: tuple[PatternCoefficient, ...]
) -> sp.Expr:
    n = sp.symbols("n", integer=True, positive=True)
    support_size = len(left_shift)
    return sp.factor(
        sum(
            sp.Rational(coefficient.numerator, coefficient.denominator)
            * _falling(n - support_size, generic_count)
            / _falling(n, constraint_count)
            for generic_count, constraint_count, coefficient in coefficients
        )
    )


def _falling_integer(value: int, count: int) -> int:
    return math.prod(value - offset for offset in range(count))


def exact_correlation_from_patterns(
    n: int,
    left_shift: tuple[int, ...],
    coefficients: tuple[PatternCoefficient, ...],
) -> Fraction:
    support_size = len(left_shift)
    if support_size > n:
        raise ValueError("active support cannot exceed n")
    total = Fraction(0)
    for generic_count, constraint_count, coefficient in coefficients:
        if generic_count > n - support_size or constraint_count > n:
            continue
        total += coefficient * Fraction(
            _falling_integer(n - support_size, generic_count),
            _falling_integer(n, constraint_count),
        )
    return total


def exact_endpoint_third_power_trace(
    n: int,
    summaries: dict[ShiftPair, tuple[tuple[PatternCoefficient, ...], int]],
) -> int:
    if n < 7:
        raise ValueError("the multiplicity-four stable channel starts at n=7")
    relative_sum = Fraction(0)
    for class_key, multiplicities in third_relative_orbit_class_counts().items():
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
        raise ArithmeticError("third power trace is not integral")
    return value.numerator


@lru_cache(maxsize=4)
def build_stable_third_moment_certificate(
    workers: int | None = None,
) -> StableThirdMomentCertificate:
    n = sp.symbols("n", integer=True, positive=True)
    orbit_size = n * (n - 1) * (n - 2)
    classes = third_relative_orbit_class_counts()
    summaries = all_class_pattern_summaries(workers=workers)
    total = sp.Integer(0)
    class_records: list[ThirdRelativeOrbitClassRecord] = []
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
            ThirdRelativeOrbitClassRecord(
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
    third_trace = sp.factor(sp.cancel(sp.expand_func(orbit_size * total)))
    trace_numerator, trace_denominator = sp.together(third_trace).as_numer_denom()
    stable_polynomial_proved = (
        trace_denominator == 1 and sp.Poly(trace_numerator, n).degree() <= 9
    )
    first_trace = FIRST_POWER_TRACE.subs(sp.Symbol("n"), n)
    second_trace = SECOND_POWER_TRACE.subs(sp.Symbol("n"), n)
    second_coefficient = SECOND_CHARACTERISTIC_COEFFICIENT.subs(
        sp.Symbol("n"), n
    )
    third_coefficient = sp.factor(
        (third_trace - first_trace * second_trace + second_coefficient * first_trace)
        / 3
    )
    newton_polynomial_proved = (
        sp.together(third_coefficient).as_numer_denom()[1] == 1
        and sp.Poly(third_coefficient, n).degree() <= 9
    )
    endpoints: list[ThirdMomentEndpointRecord] = []
    for endpoint_n in range(7, 17):
        exact_trace = exact_endpoint_third_power_trace(endpoint_n, summaries)
        formula_trace = int(third_trace.subs(n, endpoint_n))
        coefficient = int(third_coefficient.subs(n, endpoint_n))
        sparse_reference = SPARSE_QUARTIC_REFERENCES.get(endpoint_n)
        sparse_coefficient = -sparse_reference[3] if sparse_reference else None
        sparse_residual = (
            coefficient - sparse_coefficient
            if sparse_coefficient is not None
            else None
        )
        endpoints.append(
            ThirdMomentEndpointRecord(
                n=endpoint_n,
                exact_pattern_trace=exact_trace,
                formula_trace=formula_trace,
                trace_residual=exact_trace - formula_trace,
                third_characteristic_coefficient=coefficient,
                sparse_reference_coefficient=sparse_coefficient,
                sparse_reference_residual=sparse_residual,
                verified=(
                    exact_trace == formula_trace
                    and (sparse_residual is None or sparse_residual == 0)
                ),
            )
        )
    endpoints_proved = all(record.verified for record in endpoints)
    raw_counts_by_outside = [
        sum(multiplicities[outside] for multiplicities in classes.values())
        for outside in range(7)
    ]
    expected_raw_counts = [36, 540, 2484, 5292, 5832, 3240, 720]
    orbit_classification_proved = (
        len(classes) == 129 and raw_counts_by_outside == expected_raw_counts
    )
    theorem_proved = (
        orbit_classification_proved
        and stable_polynomial_proved
        and endpoints_proved
        and newton_polynomial_proved
    )
    metrics: dict[str, int | float] = {
        "exact_third_power_trace_theorem_count": int(theorem_proved),
        "exact_third_characteristic_coefficient_theorem_count": int(
            theorem_proved
        ),
        "relative_orbit_class_count": len(classes),
        "raw_relative_term_type_count": sum(raw_counts_by_outside),
        "maximum_active_support_size": max(len(key[0]) for key in classes),
        "nonzero_pattern_coefficient_count": sum(
            len(coefficients) for coefficients, _ in summaries.values()
        ),
        "raw_canonical_pattern_count": sum(
            raw_count for _, raw_count in summaries.values()
        ),
        "stable_symbolic_minimum_n": 17,
        "exact_endpoint_verified_count": sum(record.verified for record in endpoints),
        "sparse_quartic_reference_match_count": sum(
            record.sparse_reference_residual == 0
            for record in endpoints
            if record.sparse_reference_residual is not None
        ),
        "proved_quartic_coefficient_count": 3 if theorem_proved else 2,
        "required_quartic_coefficient_count": 4,
        "all_n_quartic_theorem_count": 0,
        "all_n_root_separation_theorem_count": 0,
        "uniform_polynomial_racah_circuit_count": 0,
        "hidden_involution_decoder_count": 0,
    }
    return StableThirdMomentCertificate(
        created_at=utc_now(),
        theorem={
            "range": "every integer n>=7",
            "third_power_trace": str(third_trace),
            "third_characteristic_coefficient": str(third_coefficient),
            "statement": (
                "The stable multiplicity-four hierarchical orbit Hamiltonian has the displayed exact Tr(H^3), "
                "and its quartic x coefficient follows by Newton's third identity."
            ),
            "proved": theorem_proved,
        },
        relative_orbit_certificate={
            "fixed_first_term": "tau_0=(1 2), c_0=(1 2 3)",
            "remaining_relative_term_count": "[n(n-1)(n-2)]^2",
            "classification": (
                "simultaneous conjugacy class of (tau_0 tau_1 tau_2, c_0 c_1 c_2), grouped by 0..6 outside support points"
            ),
            "canonicalization": (
                "exact rooted BFS canonical form of the two-colored permutation graph, minimized over roots and sorted by component"
            ),
            "relative_orbit_class_count": len(classes),
            "raw_counts_by_outside_support": raw_counts_by_outside,
            "expected_raw_counts_by_outside_support": expected_raw_counts,
            "classification_verified": orbit_classification_proved,
        },
        class_records=class_records,
        stable_symbolic_certificate={
            "literal_range": "n>=17",
            "reason": (
                "at most nine marked shift-support points and eight selected falling-cycle points occur"
            ),
            "third_power_trace": str(third_trace),
            "polynomial_degree": (
                int(sp.Poly(third_trace, n).degree())
                if stable_polynomial_proved
                else -1
            ),
            "identity_verified": stable_polynomial_proved,
            "interpolation_used": False,
        },
        endpoint_records=endpoints,
        newton_certificate={
            "identity": "p3 - e1*p2 + e2*p1 - 3*e3 = 0",
            "first_characteristic_coefficient": str(first_trace),
            "second_characteristic_coefficient": str(second_coefficient),
            "third_characteristic_coefficient": str(third_coefficient),
            "identity_verified": newton_polynomial_proved,
        },
        headline_metrics=metrics,
        claim_gate={
            "third_power_trace_proved": theorem_proved,
            "third_characteristic_coefficient_proved": theorem_proved,
            "full_quartic_proved": False,
            "all_n_root_separation_proved": False,
            "uniform_polynomial_racah_circuit_proved": False,
            "hidden_involution_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Three exact quartic coefficients still leave the determinant, all-n root separation, coherent "
                "Racah implementation, and reduction-compatible decoder unproved."
            ),
        },
        status=(
            "stable-third-moment-proved-determinant-open"
            if theorem_proved
            else "stable-third-moment-certificate-failed"
        ),
        summary=(
            "Reduced Tr(H^3) to 129 exact relative classes and proved its all-n polynomial plus the third quartic "
            "coefficient; the determinant and algorithmic obligations remain open."
            if theorem_proved
            else "The proposed third-moment identity failed an orbit, endpoint, or Newton check."
        ),
        falsifiers_triggered=[
            "The exact third moment proves only three of four quartic coefficients.",
            "A complete characteristic polynomial would still require uniform root separation after LCU normalization.",
            "Spectral labels do not supply a coherent polynomial-size Racah transform.",
            "No measurement outcome has been connected to a hidden-involution decoder.",
        ],
    )


def write_stable_third_moment_certificate(
    output_path: Path = COSET_STABLE_THIRD_MOMENT_PATH,
    workers: int | None = None,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(build_stable_third_moment_certificate(workers=workers))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-THREE-COEFFICIENTS-AS-COMPLETE-RACAH-SOLUTION",
                source=str(output_path),
                claim=(
                    "Three exact stable quartic coefficients establish a usable collective measurement or quantum speedup."
                ),
                reason_invalid=(
                    "The determinant, normalized root separation, coherent Racah circuit, and hidden-involution decoder remain open."
                ),
                lesson=(
                    "Close Tr(H^4) or the determinant next, then attack root separation and implementation before evaluating decoder information."
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
                    "coset_stable_third_moment_certificate": str(output_path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_stable_third_moment_certificate()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
