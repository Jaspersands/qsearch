"""Exact second power trace for the stable hierarchical Racah Hamiltonian.

The first trace certificate fixes one orbit term.  For Tr(H^2), simultaneous
conjugation fixes the first term and leaves one relative orbit term.  Products
of the two transpositions and two 3-cycles fall into only 17 simultaneous-
conjugacy classes, with multiplicities determined by how the relative support
intersects the fixed three-point support.

For each class, the falling-cycle equality-pattern engine evaluates

    E_g[chi_xi(g) chi_xi(g a) chi_W(g b)]

exactly.  The stable symbolic sum is literal for n>=14.  Exact finite pattern
counts close n=7..13.  The resulting theorem is

    Tr(H^2) = 4n^6 - 92n^5 + 828n^4 - 3678n^3
              + 8355n^2 - 8992n + 3624.

Together with Tr(H), Newton's identity proves the second characteristic
coefficient.  Tr(H^3), Tr(H^4), root separation, circuit synthesis, and
decoding remain open.
"""

from __future__ import annotations

import itertools
import json
import math
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

import sympy as sp

from coset_stable_trace_certificate import (
    W_CHARACTER_TERMS,
    XI_CHARACTER_TERMS,
)
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


COSET_STABLE_SECOND_MOMENT_PATH = Path(
    "research/representation/coset_stable_second_moment_certificate.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-STABLE-SECOND-MOMENT-CERTIFICATE"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class RelativeOrbitClassRecord:
    left_shift: tuple[int, ...]
    right_shift: tuple[int, ...]
    active_support_size: int
    multiplicities_by_outside_support_count: tuple[int, int, int, int]
    symbolic_multiplicity: str
    shifted_character_correlation: str


@dataclass(frozen=True)
class SecondMomentEndpointRecord:
    n: int
    exact_pattern_trace: int
    formula_trace: int
    trace_residual: int
    second_characteristic_coefficient: int
    verified: bool


@dataclass(frozen=True)
class StableSecondMomentCertificate:
    created_at: str
    theorem: dict[str, object]
    relative_orbit_certificate: dict[str, object]
    class_records: list[RelativeOrbitClassRecord]
    stable_symbolic_certificate: dict[str, object]
    endpoint_records: list[SecondMomentEndpointRecord]
    newton_certificate: dict[str, object]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _compose(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(left[right[index]] for index in range(len(left)))


def _cycle_permutation(size: int, cycle: tuple[int, ...]) -> tuple[int, ...]:
    permutation = list(range(size))
    for source, target in zip(cycle, (*cycle[1:], cycle[0])):
        permutation[source] = target
    return tuple(permutation)


def _canonical_shift_pair(
    left: tuple[int, ...], right: tuple[int, ...]
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    active = sorted(
        index
        for index in range(len(left))
        if left[index] != index or right[index] != index
    )
    size = len(active)
    if not active:
        return (), ()
    active_index = {value: index for index, value in enumerate(active)}
    restricted_left = tuple(active_index[left[value]] for value in active)
    restricted_right = tuple(active_index[right[value]] for value in active)
    best: tuple[tuple[int, ...], tuple[int, ...]] | None = None
    for relabeling in itertools.permutations(range(size)):
        conjugated_left = [0] * size
        conjugated_right = [0] * size
        for old_label in range(size):
            conjugated_left[relabeling[old_label]] = relabeling[
                restricted_left[old_label]
            ]
            conjugated_right[relabeling[old_label]] = relabeling[
                restricted_right[old_label]
            ]
        candidate = (tuple(conjugated_left), tuple(conjugated_right))
        if best is None or candidate < best:
            best = candidate
    if best is None:
        raise ArithmeticError("failed to canonicalize relative orbit class")
    return best


@lru_cache(maxsize=1)
def relative_orbit_class_counts() -> dict[
    tuple[tuple[int, ...], tuple[int, ...]], tuple[int, int, int, int]
]:
    ambient_size = 6
    base_transposition = _cycle_permutation(ambient_size, (0, 1))
    base_cycle = _cycle_permutation(ambient_size, (0, 1, 2))
    counts_by_outside: list[Counter] = []
    all_classes: set[tuple[tuple[int, ...], tuple[int, ...]]] = set()
    for outside_count in range(4):
        counts: Counter = Counter()
        for inside in itertools.combinations(range(3), 3 - outside_count):
            support = (*inside, *range(3, 3 + outside_count))
            for transposition_support in itertools.combinations(support, 2):
                transposition = _cycle_permutation(
                    ambient_size, transposition_support
                )
                for cycle_support in (
                    support,
                    (support[0], support[2], support[1]),
                ):
                    cycle = _cycle_permutation(ambient_size, cycle_support)
                    class_key = _canonical_shift_pair(
                        _compose(base_transposition, transposition),
                        _compose(base_cycle, cycle),
                    )
                    counts[class_key] += 1
                    all_classes.add(class_key)
        counts_by_outside.append(counts)
    return {
        class_key: tuple(
            int(counts_by_outside[outside].get(class_key, 0))
            for outside in range(4)
        )
        for class_key in sorted(all_classes)
    }


@lru_cache(maxsize=None)
def generalized_equality_pattern_counts(
    first: tuple[int, ...],
    second: tuple[int, ...],
    third: tuple[int, ...],
    left_shift: tuple[int, ...],
    right_shift: tuple[int, ...],
) -> tuple[tuple[tuple[int, int], int], ...]:
    special_count = len(left_shift)
    if len(right_shift) != special_count:
        raise ValueError("shift permutations must have equal size")
    cycles: list[tuple[int, list[int]]] = []
    factors: list[int] = []
    cycles_ending_at: dict[int, list[tuple[int, list[int]]]] = defaultdict(list)
    position_count = 0
    for factor, lengths in enumerate((first, second, third)):
        for length in lengths:
            positions = list(range(position_count, position_count + length))
            cycles.append((factor, positions))
            cycles_ending_at[positions[-1]].append((factor, positions))
            factors.extend([factor] * length)
            position_count += length
    multipliers = (tuple(range(special_count)), left_shift, right_shift)
    counts: defaultdict[tuple[int, int], int] = defaultdict(int)
    assigned: list[int] = []
    used_by_factor = [set(), set(), set()]
    partial_map: dict[int, int] = {}
    inverse_map: dict[int, int] = {}

    def visit(position: int, generic_count: int) -> None:
        if position == position_count:
            counts[(generic_count, len(partial_map))] += 1
            return
        factor = factors[position]
        for value in range(special_count + generic_count + 1):
            is_new_generic = value == special_count + generic_count
            if value in used_by_factor[factor]:
                continue
            assigned.append(value)
            used_by_factor[factor].add(value)
            added_constraints: list[tuple[int, int]] = []
            consistent = True
            for cycle_factor, cycle_positions in cycles_ending_at.get(position, []):
                values = [assigned[index] for index in cycle_positions]
                for index, source in enumerate(values):
                    domain = (
                        multipliers[cycle_factor][source]
                        if source < special_count
                        else source
                    )
                    output = values[(index + 1) % len(values)]
                    if (
                        domain in partial_map and partial_map[domain] != output
                    ) or (
                        output in inverse_map and inverse_map[output] != domain
                    ):
                        consistent = False
                        break
                    if domain not in partial_map:
                        partial_map[domain] = output
                        inverse_map[output] = domain
                        added_constraints.append((domain, output))
                if not consistent:
                    break
            if consistent:
                visit(position + 1, generic_count + int(is_new_generic))
            for domain, output in reversed(added_constraints):
                del partial_map[domain]
                del inverse_map[output]
            used_by_factor[factor].remove(value)
            assigned.pop()

    visit(0, 0)
    return tuple(sorted(counts.items()))


def _falling(value: sp.Expr, count: int) -> sp.Expr:
    return sp.prod(value - offset for offset in range(count))


@lru_cache(maxsize=None)
def shifted_character_correlation(
    left_shift: tuple[int, ...], right_shift: tuple[int, ...]
) -> sp.Expr:
    n = sp.symbols("n", integer=True, positive=True)
    special_count = len(left_shift)
    total = sp.Integer(0)
    for first, first_coefficient in XI_CHARACTER_TERMS:
        for second, second_coefficient in XI_CHARACTER_TERMS:
            for third, third_coefficient in W_CHARACTER_TERMS:
                rotation_denominator = math.prod((*first, *second, *third))
                expectation = sum(
                    sp.Rational(pattern_count, rotation_denominator)
                    * _falling(n - special_count, generic_count)
                    / _falling(n, constraint_count)
                    for (
                        generic_count,
                        constraint_count,
                    ), pattern_count in generalized_equality_pattern_counts(
                        first,
                        second,
                        third,
                        left_shift,
                        right_shift,
                    )
                )
                coefficient = (
                    sp.Rational(
                        first_coefficient.numerator, first_coefficient.denominator
                    )
                    * sp.Rational(
                        second_coefficient.numerator, second_coefficient.denominator
                    )
                    * sp.Rational(
                        third_coefficient.numerator, third_coefficient.denominator
                    )
                )
                total += coefficient * expectation
    return sp.factor(total)


@lru_cache(maxsize=1)
def symbolic_second_power_trace() -> dict[str, object]:
    n = sp.symbols("n", integer=True, positive=True)
    orbit_size = n * (n - 1) * (n - 2)
    total = sp.Integer(0)
    class_records: list[RelativeOrbitClassRecord] = []
    for (left_shift, right_shift), multiplicities in relative_orbit_class_counts().items():
        symbolic_multiplicity = sum(
            multiplicity * sp.binomial(n - 3, outside_count)
            for outside_count, multiplicity in enumerate(multiplicities)
        )
        correlation = shifted_character_correlation(left_shift, right_shift)
        total += symbolic_multiplicity * correlation
        class_records.append(
            RelativeOrbitClassRecord(
                left_shift=left_shift,
                right_shift=right_shift,
                active_support_size=len(left_shift),
                multiplicities_by_outside_support_count=multiplicities,
                symbolic_multiplicity=str(symbolic_multiplicity),
                shifted_character_correlation=str(correlation),
            )
        )
    second_trace = sp.factor(
        sp.cancel(sp.expand_func(orbit_size * total))
    )
    expected = (
        4 * n**6
        - 92 * n**5
        + 828 * n**4
        - 3678 * n**3
        + 8355 * n**2
        - 8992 * n
        + 3624
    )
    return {
        "orbit_size": orbit_size,
        "second_power_trace": second_trace,
        "expected_second_power_trace": expected,
        "identity_verified": sp.simplify(second_trace - expected) == 0,
        "class_records": class_records,
        "relative_orbit_class_count": len(class_records),
        "shifted_correlation_monomial_product_count": (
            len(class_records) * len(XI_CHARACTER_TERMS) ** 2 * len(W_CHARACTER_TERMS)
        ),
    }


def _falling_integer(value: int, count: int) -> int:
    return math.prod(value - offset for offset in range(count))


@lru_cache(maxsize=None)
def exact_numeric_shifted_correlation(
    n: int, left_shift: tuple[int, ...], right_shift: tuple[int, ...]
) -> Fraction:
    special_count = len(left_shift)
    total = Fraction(0)
    for first, first_coefficient in XI_CHARACTER_TERMS:
        for second, second_coefficient in XI_CHARACTER_TERMS:
            for third, third_coefficient in W_CHARACTER_TERMS:
                rotation_denominator = math.prod((*first, *second, *third))
                expectation = Fraction(0)
                for (
                    generic_count,
                    constraint_count,
                ), pattern_count in generalized_equality_pattern_counts(
                    first,
                    second,
                    third,
                    left_shift,
                    right_shift,
                ):
                    if generic_count > n - special_count or constraint_count > n:
                        continue
                    expectation += Fraction(
                        pattern_count
                        * _falling_integer(n - special_count, generic_count),
                        rotation_denominator
                        * _falling_integer(n, constraint_count),
                    )
                total += (
                    first_coefficient
                    * second_coefficient
                    * third_coefficient
                    * expectation
                )
    return total


def exact_endpoint_second_power_trace(n: int) -> int:
    if n < 7:
        raise ValueError("the multiplicity-four stable channel starts at n=7")
    relative_sum = Fraction(0)
    for (left_shift, right_shift), multiplicities in relative_orbit_class_counts().items():
        multiplicity = sum(
            count * math.comb(n - 3, outside_count)
            for outside_count, count in enumerate(multiplicities)
        )
        relative_sum += multiplicity * exact_numeric_shifted_correlation(
            n, left_shift, right_shift
        )
    value = n * (n - 1) * (n - 2) * relative_sum
    if value.denominator != 1:
        raise ArithmeticError("second power trace is not integral")
    return value.numerator


@lru_cache(maxsize=1)
def build_stable_second_moment_certificate() -> StableSecondMomentCertificate:
    n = sp.symbols("n", integer=True, positive=True)
    symbolic = symbolic_second_power_trace()
    second_trace = symbolic["second_power_trace"]
    first_trace = 4 * n**3 - 46 * n**2 + 149 * n - 118
    second_coefficient = sp.factor((first_trace**2 - second_trace) / 2)
    expected_second_coefficient = (
        6 * n**6
        - 138 * n**5
        + 1240 * n**4
        - 5487 * n**3
        + 12351 * n**2
        - 13086 * n
        + 5150
    )
    endpoints: list[SecondMomentEndpointRecord] = []
    for endpoint_n in range(7, 14):
        exact_trace = exact_endpoint_second_power_trace(endpoint_n)
        formula_trace = int(second_trace.subs(n, endpoint_n))
        coefficient = int(second_coefficient.subs(n, endpoint_n))
        endpoints.append(
            SecondMomentEndpointRecord(
                n=endpoint_n,
                exact_pattern_trace=exact_trace,
                formula_trace=formula_trace,
                trace_residual=exact_trace - formula_trace,
                second_characteristic_coefficient=coefficient,
                verified=exact_trace == formula_trace,
            )
        )
    symbolic_proved = bool(symbolic["identity_verified"])
    endpoints_proved = all(record.verified for record in endpoints)
    newton_proved = (
        sp.simplify(second_coefficient - expected_second_coefficient) == 0
    )
    theorem_proved = symbolic_proved and endpoints_proved and newton_proved
    class_records = symbolic["class_records"]
    return StableSecondMomentCertificate(
        created_at=utc_now(),
        theorem={
            "range": "every integer n>=7",
            "second_power_trace": str(second_trace),
            "second_characteristic_coefficient": str(second_coefficient),
            "statement": (
                "The stable multiplicity-four hierarchical orbit Hamiltonian has the displayed exact Tr(H^2), "
                "and its quartic x^2 coefficient follows by Newton's identity."
            ),
            "proved": theorem_proved,
        },
        relative_orbit_certificate={
            "fixed_first_term": "tau_0=(1 2), c_0=(1 2 3)",
            "relative_term_count": "n(n-1)(n-2)",
            "classification": (
                "simultaneous conjugacy class of (tau_0 tau, c_0 c), grouped by 0..3 outside support points"
            ),
            "relative_orbit_class_count": symbolic["relative_orbit_class_count"],
            "stable_literal_range": "n>=14",
            "finite_exact_endpoint_range": "7<=n<=13",
        },
        class_records=class_records,
        stable_symbolic_certificate={
            "range": "n>=14",
            "second_power_trace": str(second_trace),
            "identity_verified": symbolic_proved,
            "shifted_correlation_monomial_product_count": symbolic[
                "shifted_correlation_monomial_product_count"
            ],
        },
        endpoint_records=endpoints,
        newton_certificate={
            "identity": "e2=(Tr(H)^2-Tr(H^2))/2",
            "first_trace": str(first_trace),
            "second_trace": str(second_trace),
            "second_characteristic_coefficient": str(second_coefficient),
            "identity_verified": newton_proved,
        },
        headline_metrics={
            "exact_second_power_trace_theorem_count": int(theorem_proved),
            "exact_second_characteristic_coefficient_theorem_count": int(
                theorem_proved
            ),
            "relative_orbit_class_count": int(
                symbolic["relative_orbit_class_count"]
            ),
            "exact_endpoint_verified_count": sum(
                record.verified for record in endpoints
            ),
            "minimum_proved_n": 7,
            "proved_quartic_coefficient_count": 2,
            "required_quartic_coefficient_count": 4,
            "all_n_quartic_theorem_count": 0,
            "all_n_root_separation_theorem_count": 0,
            "uniform_polynomial_racah_circuit_count": 0,
            "hidden_involution_decoder_count": 0,
        },
        claim_gate={
            "exact_second_power_trace_proved": theorem_proved,
            "first_two_quartic_coefficients_proved": theorem_proved,
            "complete_quartic_formula_proved": False,
            "root_separation_proved": False,
            "uniform_polynomial_racah_circuit_proved": False,
            "hidden_involution_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Two of four quartic coefficients are exact. Tr(H^3), Tr(H^4), root separation, complete sector "
                "coverage, coherent synthesis, and decoding remain open."
            ),
        },
        status=(
            "exact-stable-second-moment-proved-two-quartic-coefficients-known"
            if theorem_proved
            else "stable-second-moment-certificate-failed"
        ),
        summary=(
            "Proved the stable second power trace and the quartic's second coefficient for every n>=7 using 17 "
            "relative orbit classes; two quartic coefficients, root separation, circuit, and decoder remain open."
        ),
        falsifiers_triggered=[
            "Two exact characteristic coefficients do not determine a quartic spectrum.",
            "A complete characteristic polynomial would still need normalized root separation.",
            "One stable multiplicity-four channel does not cover every decoder-relevant sector.",
            "No coherent recoupling circuit or hidden-involution decoder follows from moment identities.",
        ],
    )


def write_stable_second_moment_certificate(
    output_path: Path = COSET_STABLE_SECOND_MOMENT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(build_stable_second_moment_certificate())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-TWO-QUARTIC-COEFFICIENTS-AS-COMPLETE-GAP-THEOREM",
                source=str(output_path),
                claim=(
                    "The first two exact characteristic coefficients determine the stable Racah spectrum and gap."
                ),
                reason_invalid=(
                    "A quartic still needs its cubic and constant coefficients, followed by a uniform root-separation theorem."
                ),
                lesson=(
                    "Extend the relative-orbit engine to third and fourth moments, reconstruct the complete quartic, "
                    "and prove normalized root separation before circuit claims."
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
                artifacts={"coset_stable_second_moment_certificate": str(output_path)},
            )
        )
    return payload
