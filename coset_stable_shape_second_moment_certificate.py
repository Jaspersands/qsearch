"""Exact second spectral coefficient across the stable Racah shape family.

The common support-intersection-two orbit Hamiltonian has 17 relative
simultaneous-conjugacy classes after one term of H^2 is fixed.  This module
combines that universal relative-orbit classification with each of the nine
proved stable intermediate character polynomials.  Exact marked-cycle sums
give Tr(H^2); Newton's identity gives the second characteristic coefficient.

For the five previously open multiplicity-two shapes this coefficient is the
determinant, so their complete quadratic characteristic polynomials become
exact.  The multiplicity-three (3,1)-tail shape is left with only its
determinant.  Root separation, coherent compilation, transition synthesis,
and hidden-involution decoding remain separate proof obligations.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

import sympy as sp

from coset_stable_second_moment_certificate import (
    generalized_equality_pattern_counts,
    relative_orbit_class_counts,
)
from coset_stable_shape_family_certificate import (
    FINAL_TAIL,
    STABLE_TAILS,
    padded_partition,
    reconstruct_character_polynomial,
)
from coset_stable_shape_trace_certificate import (
    falling_character_terms,
    symbolic_shape_trace,
)
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from symmetric_character import kronecker_coefficient


COSET_STABLE_SHAPE_SECOND_MOMENT_PATH = Path(
    "research/representation/coset_stable_shape_second_moment_certificate.json"
)
COSET_STABLE_SHAPE_LABEL_PATH = Path(
    "research/representation/coset_stable_shape_label_probe.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-STABLE-SHAPE-SECOND-MOMENT-CERTIFICATE"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class ShapeSecondMomentEndpoint:
    n: int
    exact_pattern_second_power_trace: int
    symbolic_formula_value: int
    residual: int
    verified: bool


@dataclass(frozen=True)
class StableShapeSecondMomentRecord:
    intermediate_tail: tuple[int, ...]
    intermediate_partition: str
    second_stage_multiplicity: int
    falling_character_term_count: int
    relative_orbit_class_count: int
    shifted_correlation_monomial_product_count: int
    maximum_special_plus_generic_count: int
    maximum_partial_permutation_constraint_count: int
    literal_symbolic_range_start: int
    exact_first_power_trace: str
    exact_second_power_trace: str
    exact_second_characteristic_coefficient: str
    second_power_trace_degree: int
    endpoint_records: list[ShapeSecondMomentEndpoint]
    finite_probe_comparison_count: int
    finite_probe_agreement_count: int
    exact_all_n_at_least_8_second_moment_proved: bool
    complete_characteristic_polynomial_proved_by_this_pass: bool
    complete_characteristic_polynomial_already_proved: bool
    remaining_exact_characteristic_coefficient_count: int
    status: str


@dataclass(frozen=True)
class StableShapeSecondMomentCertificate:
    created_at: str
    theorem: dict[str, object]
    method_contract: dict[str, object]
    shape_records: list[StableShapeSecondMomentRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _tail_formula(tail: tuple[int, ...]) -> str:
    return f"(n-{sum(tail)},{','.join(str(value) for value in tail)})"


def _falling(value: sp.Expr, count: int) -> sp.Expr:
    return sp.prod(value - offset for offset in range(count))


def _falling_integer(value: int, count: int) -> int:
    return math.prod(value - offset for offset in range(count))


@lru_cache(maxsize=None)
def shifted_shape_character_correlation(
    intermediate_tail: tuple[int, ...],
    left_shift: tuple[int, ...],
    right_shift: tuple[int, ...],
) -> tuple[sp.Expr, int, int]:
    n = sp.symbols("n", integer=True, positive=True)
    special_count = len(left_shift)
    first_terms = falling_character_terms(FINAL_TAIL)
    second_terms = falling_character_terms(intermediate_tail)
    third_terms = falling_character_terms((2,))
    total = sp.Integer(0)
    maximum_special_plus_generic = special_count
    maximum_constraint = 0
    for first, first_coefficient in first_terms:
        for second, second_coefficient in second_terms:
            for third, third_coefficient in third_terms:
                rotation_denominator = math.prod((*first, *second, *third))
                patterns = generalized_equality_pattern_counts(
                    first,
                    second,
                    third,
                    left_shift,
                    right_shift,
                )
                maximum_special_plus_generic = max(
                    maximum_special_plus_generic,
                    max(
                        (special_count + key[0] for key, _ in patterns),
                        default=special_count,
                    ),
                )
                maximum_constraint = max(
                    maximum_constraint,
                    max((key[1] for key, _ in patterns), default=0),
                )
                expectation = sum(
                    sp.Rational(pattern_count, rotation_denominator)
                    * _falling(n - special_count, generic_count)
                    / _falling(n, constraint_count)
                    for (
                        generic_count,
                        constraint_count,
                    ), pattern_count in patterns
                )
                coefficient = (
                    sp.Rational(first_coefficient.numerator, first_coefficient.denominator)
                    * sp.Rational(second_coefficient.numerator, second_coefficient.denominator)
                    * sp.Rational(third_coefficient.numerator, third_coefficient.denominator)
                )
                total += coefficient * expectation
    return sp.factor(total), maximum_special_plus_generic, maximum_constraint


@lru_cache(maxsize=None)
def symbolic_shape_second_moment(
    intermediate_tail: tuple[int, ...],
) -> dict[str, object]:
    if intermediate_tail not in STABLE_TAILS:
        raise ValueError("intermediate tail is outside the exact stable family")
    n = sp.symbols("n", integer=True, positive=True)
    orbit_size = n * (n - 1) * (n - 2)
    total = sp.Integer(0)
    maximum_special_plus_generic = 0
    maximum_constraint = 0
    classes = relative_orbit_class_counts()
    for (left_shift, right_shift), multiplicities in classes.items():
        symbolic_multiplicity = sum(
            multiplicity * sp.binomial(n - 3, outside_count)
            for outside_count, multiplicity in enumerate(multiplicities)
        )
        correlation, special_plus_generic, constraint = (
            shifted_shape_character_correlation(
                intermediate_tail, left_shift, right_shift
            )
        )
        maximum_special_plus_generic = max(
            maximum_special_plus_generic, special_plus_generic
        )
        maximum_constraint = max(maximum_constraint, constraint)
        total += symbolic_multiplicity * correlation
    second_trace = sp.cancel(sp.expand_func(orbit_size * total))
    numerator, denominator = sp.fraction(second_trace)
    if denominator != 1:
        raise ArithmeticError("shape second moment did not simplify to a polynomial")
    polynomial = sp.Poly(sp.expand(numerator), n)
    if polynomial.degree() > 6:
        raise ArithmeticError("second power trace exceeds the expected degree six")
    _, character_certificate = reconstruct_character_polynomial(intermediate_tail)
    literal_start = max(
        8,
        int(character_certificate["threshold"]),
        maximum_special_plus_generic,
        maximum_constraint,
    )
    return {
        "second_power_trace": sp.expand(polynomial.as_expr()),
        "second_power_trace_degree": polynomial.degree(),
        "relative_orbit_class_count": len(classes),
        "monomial_product_count": (
            len(classes)
            * len(falling_character_terms(FINAL_TAIL))
            * len(falling_character_terms(intermediate_tail))
            * len(falling_character_terms((2,)))
        ),
        "maximum_special_plus_generic_count": maximum_special_plus_generic,
        "maximum_constraint_count": maximum_constraint,
        "literal_symbolic_range_start": literal_start,
    }


@lru_cache(maxsize=None)
def exact_numeric_shape_shifted_correlation(
    n: int,
    intermediate_tail: tuple[int, ...],
    left_shift: tuple[int, ...],
    right_shift: tuple[int, ...],
) -> Fraction:
    special_count = len(left_shift)
    total = Fraction(0)
    for first, first_coefficient in falling_character_terms(FINAL_TAIL):
        for second, second_coefficient in falling_character_terms(intermediate_tail):
            for third, third_coefficient in falling_character_terms((2,)):
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


@lru_cache(maxsize=None)
def exact_endpoint_shape_second_power_trace(
    n: int, intermediate_tail: tuple[int, ...]
) -> int:
    if n < 8:
        raise ValueError("the exact nine-shape endpoint starts at n=8")
    relative_sum = Fraction(0)
    for (left_shift, right_shift), multiplicities in relative_orbit_class_counts().items():
        multiplicity = sum(
            count * math.comb(n - 3, outside_count)
            for outside_count, count in enumerate(multiplicities)
        )
        relative_sum += multiplicity * exact_numeric_shape_shifted_correlation(
            n,
            intermediate_tail,
            left_shift,
            right_shift,
        )
    value = n * (n - 1) * (n - 2) * relative_sum
    if value.denominator != 1:
        raise ArithmeticError("shape second power trace is not integral")
    return value.numerator


def _finite_probe_second_coefficients() -> dict[
    tuple[tuple[int, ...], int], int
]:
    if not COSET_STABLE_SHAPE_LABEL_PATH.exists():
        return {}
    try:
        payload = json.loads(COSET_STABLE_SHAPE_LABEL_PATH.read_text())
    except (json.JSONDecodeError, OSError):
        return {}
    coefficients: dict[tuple[tuple[int, ...], int], int] = {}
    for row in payload.get("records", []):
        polynomial = row.get("integer_characteristic_polynomial_candidate", [])
        if len(polynomial) < 3:
            continue
        coefficients[(tuple(row["intermediate_tail"]), int(row["n"]))] = int(
            polynomial[2]
        )
    return coefficients


@lru_cache(maxsize=1)
def build_stable_shape_second_moment_certificate() -> (
    StableShapeSecondMomentCertificate
):
    n = sp.symbols("n", integer=True, positive=True)
    finite_coefficients = _finite_probe_second_coefficients()
    records: list[StableShapeSecondMomentRecord] = []
    for tail in STABLE_TAILS:
        symbolic = symbolic_shape_second_moment(tail)
        first_trace = sp.expand(symbolic_shape_trace(tail)["trace"])
        second_trace = sp.expand(symbolic["second_power_trace"])
        second_coefficient = sp.factor((first_trace**2 - second_trace) / 2)
        second_multiplicity = kronecker_coefficient(
            padded_partition(8, tail),
            padded_partition(8, (2,)),
            padded_partition(8, FINAL_TAIL),
        )
        endpoint_rows: list[ShapeSecondMomentEndpoint] = []
        for endpoint_n in range(
            8, int(symbolic["literal_symbolic_range_start"])
        ):
            exact_trace = exact_endpoint_shape_second_power_trace(
                endpoint_n, tail
            )
            formula_value = int(second_trace.subs(n, endpoint_n))
            endpoint_rows.append(
                ShapeSecondMomentEndpoint(
                    n=endpoint_n,
                    exact_pattern_second_power_trace=exact_trace,
                    symbolic_formula_value=formula_value,
                    residual=exact_trace - formula_value,
                    verified=exact_trace == formula_value,
                )
            )
        comparisons = [
            (size, coefficient)
            for (record_tail, size), coefficient in finite_coefficients.items()
            if record_tail == tail
        ]
        agreements = sum(
            int(second_coefficient.subs(n, size)) == coefficient
            for size, coefficient in comparisons
        )
        theorem_proved = all(row.verified for row in endpoint_rows) and (
            agreements == len(comparisons)
        )
        complete_by_pass = second_multiplicity == 2 and theorem_proved
        complete_already = tail == FINAL_TAIL
        remaining = (
            0
            if complete_by_pass or complete_already or second_multiplicity == 1
            else max(0, second_multiplicity - 2)
        )
        records.append(
            StableShapeSecondMomentRecord(
                intermediate_tail=tail,
                intermediate_partition=_tail_formula(tail),
                second_stage_multiplicity=second_multiplicity,
                falling_character_term_count=len(falling_character_terms(tail)),
                relative_orbit_class_count=int(symbolic["relative_orbit_class_count"]),
                shifted_correlation_monomial_product_count=int(
                    symbolic["monomial_product_count"]
                ),
                maximum_special_plus_generic_count=int(
                    symbolic["maximum_special_plus_generic_count"]
                ),
                maximum_partial_permutation_constraint_count=int(
                    symbolic["maximum_constraint_count"]
                ),
                literal_symbolic_range_start=int(
                    symbolic["literal_symbolic_range_start"]
                ),
                exact_first_power_trace=str(first_trace),
                exact_second_power_trace=str(second_trace),
                exact_second_characteristic_coefficient=str(
                    second_coefficient
                ),
                second_power_trace_degree=int(
                    symbolic["second_power_trace_degree"]
                ),
                endpoint_records=endpoint_rows,
                finite_probe_comparison_count=len(comparisons),
                finite_probe_agreement_count=agreements,
                exact_all_n_at_least_8_second_moment_proved=theorem_proved,
                complete_characteristic_polynomial_proved_by_this_pass=(
                    complete_by_pass
                ),
                complete_characteristic_polynomial_already_proved=(
                    complete_already
                ),
                remaining_exact_characteristic_coefficient_count=remaining,
                status=(
                    "exact-quadratic-characteristic-polynomial-proved-gap-open"
                    if complete_by_pass
                    else (
                        "exact-cubic-first-two-coefficients-proved-determinant-open"
                        if theorem_proved and second_multiplicity == 3
                        else (
                            "exact-second-moment-proved-complete-polynomial-already-known"
                            if theorem_proved and complete_already
                            else "exact-second-moment-proved-multiplicity-one"
                            if theorem_proved
                            else "shape-second-moment-certificate-failed"
                        )
                    )
                ),
            )
        )

    theorem_count = sum(
        record.exact_all_n_at_least_8_second_moment_proved for record in records
    )
    metrics: dict[str, int | float] = {
        "stable_shape_count": len(records),
        "exact_all_n_shape_second_moment_theorem_count": theorem_count,
        "new_exact_open_shape_second_moment_theorem_count": sum(
            record.exact_all_n_at_least_8_second_moment_proved
            and record.second_stage_multiplicity > 1
            and not record.complete_characteristic_polynomial_already_proved
            for record in records
        ),
        "new_exact_complete_quadratic_shape_polynomial_count": sum(
            record.complete_characteristic_polynomial_proved_by_this_pass
            for record in records
        ),
        "finite_probe_second_coefficient_comparison_count": sum(
            record.finite_probe_comparison_count for record in records
        ),
        "finite_probe_second_coefficient_agreement_count": sum(
            record.finite_probe_agreement_count for record in records
        ),
        "exact_endpoint_verified_count": sum(
            endpoint.verified
            for record in records
            for endpoint in record.endpoint_records
        ),
        "remaining_open_shape_characteristic_coefficient_family_count": sum(
            record.remaining_exact_characteristic_coefficient_count
            for record in records
        ),
        "new_normalized_gap_theorem_count": 0,
        "new_coherent_shape_label_count": 0,
        "complete_racah_associator_count": 0,
        "hidden_involution_decoder_count": 0,
    }
    all_proved = theorem_count == len(records)
    return StableShapeSecondMomentCertificate(
        created_at=utc_now(),
        theorem={
            "range": "every integer n>=8",
            "statement": (
                "The common orbit Hamiltonian has the listed exact Tr(H^2) and second characteristic coefficient "
                "on every stable intermediate shape; all five open multiplicity-two characteristic polynomials "
                "are therefore exact."
            ),
            "proved": all_proved,
        },
        method_contract={
            "relative_orbit_class_count": len(relative_orbit_class_counts()),
            "fixed_first_term": "tau_0=(1 2), c_0=(1 2 3)",
            "symbolic_method": (
                "exact relative-orbit multiplicities times falling-cycle partial-permutation correlations"
            ),
            "newton_identity": "e2=(Tr(H)^2-Tr(H^2))/2",
            "interpolation_used": False,
            "floating_arithmetic_used_for_theorem": False,
        },
        shape_records=records,
        headline_metrics=metrics,
        claim_gate={
            "all_nine_second_moments_proved": all_proved,
            "all_five_open_quadratic_characteristic_polynomials_proved": (
                metrics["new_exact_complete_quadratic_shape_polynomial_count"]
                == 5
            ),
            "multiplicity_three_characteristic_polynomial_proved": False,
            "all_normalized_gaps_proved": False,
            "all_coherent_label_circuits_proved": False,
            "complete_racah_associator_proved": False,
            "hidden_involution_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Five quadratic spectra are exact, but their normalized root gaps and coherent implementations "
                "are unproved; the multiplicity-three determinant, transitions, and decoder also remain open."
            ),
        },
        status=(
            "five-exact-quadratic-shape-polynomials-proved-one-cubic-determinant-open"
            if all_proved
            and metrics["new_exact_complete_quadratic_shape_polynomial_count"]
            == 5
            else "stable-shape-second-moment-certificate-failed"
        ),
        summary=(
            f"Proved {theorem_count}/9 exact second moments, completing all five previously open quadratic shape "
            f"characteristic polynomials; {metrics['remaining_open_shape_characteristic_coefficient_family_count']} "
            "higher coefficient family remains before every stable-shape spectrum is exact."
        ),
        falsifiers_triggered=[
            "Exact quadratic characteristic polynomials still require normalized discriminant bounds.",
            "The multiplicity-three shape still lacks its determinant.",
            "Exact spectra do not compile the common orbit Hamiltonian into a coherent circuit.",
            "Complete shape labels do not synthesize coupling-tree transitions or decode a hidden involution.",
        ],
    )


def write_stable_shape_second_moment_certificate(
    output_path: Path = COSET_STABLE_SHAPE_SECOND_MOMENT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(build_stable_shape_second_moment_certificate())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-FIVE-EXACT-QUADRATIC-SHAPES-AS-COMPLETE-RACAH",
                source=str(output_path),
                claim=(
                    "Exact characteristic polynomials for five complementary shapes close the stable Racah transform."
                ),
                reason_invalid=(
                    "The multiplicity-three determinant, six normalized gap theorems, coherent orbit-LCU "
                    "compilation, coupling-tree transitions, and hidden-involution decoder remain unproved."
                ),
                lesson=(
                    "Finish the lone cubic determinant, prove each quadratic/cubic normalized discriminant bound, "
                    "then satisfy circuit and decoder proof gates independently."
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
                    "coset_stable_shape_second_moment_certificate": str(
                        output_path
                    )
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_stable_shape_second_moment_certificate()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
