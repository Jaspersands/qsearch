"""Exact first spectral coefficient for every stable Racah shape family.

For W_n=(n-2,2), xi_n=(n-3,2,1), and any of the nine proved stable
intermediate shapes eta_n, the support-intersection-two orbit Hamiltonian has
multiplicity-space trace

    n(n-1)(n-2) E_g[chi_xi(g) chi_eta(g tau) chi_W(g c)],

with tau=(1 2) and c=(1 2 3).  This module converts reconstructed stable
character polynomials into falling cycle-count monomials and applies the exact
marked-cycle equality-pattern calculation.  Direct S_8 character sums close
the finite endpoint when a symbolic pattern formula starts at n=9.

This proves one characteristic coefficient per shape.  It does not prove the
remaining determinants/higher coefficients, normalized root separation,
coherent LCU compilation, coupling-tree transitions, or decoding.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

import sympy as sp

from coset_stable_shape_family_certificate import (
    FINAL_TAIL,
    STABLE_TAILS,
    X,
    _stirling_second,
    padded_partition,
    reconstruct_character_polynomial,
)
from coset_stable_trace_certificate import (
    _compose,
    _cycle_type,
    equality_pattern_counts,
    selected_cycle_expectation,
)
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from symmetric_character import kronecker_coefficient, symmetric_character


COSET_STABLE_SHAPE_TRACE_PATH = Path(
    "research/representation/coset_stable_shape_trace_certificate.json"
)
COSET_STABLE_SHAPE_LABEL_PATH = Path(
    "research/representation/coset_stable_shape_label_probe.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-STABLE-SHAPE-TRACE-CERTIFICATE"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

CycleMonomial = tuple[int, ...]
FallingTerms = tuple[tuple[CycleMonomial, Fraction], ...]


@dataclass(frozen=True)
class StableShapeTraceRecord:
    intermediate_tail: tuple[int, ...]
    intermediate_partition: str
    second_stage_multiplicity: int
    character_polynomial: str
    falling_character_term_count: int
    falling_monomial_product_count: int
    canonical_equality_pattern_count: int
    maximum_selected_point_count: int
    maximum_partial_permutation_constraint_count: int
    literal_symbolic_range_start: int
    exact_trace_polynomial: str
    trace_polynomial_degree: int
    exact_n8_character_sum_trace: int
    exact_n8_formula_value: int
    exact_n8_endpoint_verified: bool
    finite_probe_comparison_count: int
    finite_probe_trace_agreement_count: int
    exact_all_n_at_least_8_trace_proved: bool
    exact_complete_characteristic_polynomial_already_proved: bool
    remaining_exact_characteristic_coefficient_count: int
    status: str


@dataclass(frozen=True)
class StableShapeTraceCertificate:
    created_at: str
    theorem: dict[str, object]
    method_contract: dict[str, object]
    shape_records: list[StableShapeTraceRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _tail_formula(tail: tuple[int, ...]) -> str:
    return f"(n-{sum(tail)},{','.join(str(value) for value in tail)})"


@lru_cache(maxsize=None)
def falling_character_terms(tail: tuple[int, ...]) -> FallingTerms:
    """Expand a stable character polynomial in products of (X_i)_{k_i}."""
    polynomial, _ = reconstruct_character_polynomial(tail)
    coefficients: dict[tuple[int, ...], sp.Rational] = {}
    for powers, coefficient in sp.Poly(polynomial, *X).terms():
        choices = [
            tuple(
                (falling_degree, _stirling_second(power, falling_degree))
                for falling_degree in range(power + 1)
                if _stirling_second(power, falling_degree)
            )
            for power in powers
        ]
        for row in itertools.product(*choices):
            falling_degrees = tuple(item[0] for item in row)
            contribution = sp.Rational(coefficient) * sp.prod(
                item[1] for item in row
            )
            coefficients[falling_degrees] = sp.simplify(
                coefficients.get(falling_degrees, sp.Rational(0))
                + contribution
            )

    terms: list[tuple[CycleMonomial, Fraction]] = []
    for falling_degrees, coefficient in sorted(coefficients.items()):
        if coefficient == 0:
            continue
        cycle_lengths = tuple(
            cycle_length
            for cycle_length, count in enumerate(falling_degrees, 1)
            for _ in range(count)
        )
        rational = sp.Rational(coefficient)
        terms.append(
            (
                cycle_lengths,
                Fraction(int(rational.p), int(rational.q)),
            )
        )
    return tuple(terms)


@lru_cache(maxsize=None)
def symbolic_shape_trace(intermediate_tail: tuple[int, ...]) -> dict[str, object]:
    if intermediate_tail not in STABLE_TAILS:
        raise ValueError("intermediate tail is outside the exact stable family")
    n = sp.symbols("n", integer=True, positive=True)
    first_terms = falling_character_terms(FINAL_TAIL)
    second_terms = falling_character_terms(intermediate_tail)
    third_terms = falling_character_terms((2,))
    correlation = sp.Integer(0)
    pattern_type_count = 0
    canonical_pattern_count = 0
    maximum_selected_points = 0
    maximum_constraint_count = 0
    for first, first_coefficient in first_terms:
        for second, second_coefficient in second_terms:
            for third, third_coefficient in third_terms:
                lengths = (first, second, third)
                patterns = equality_pattern_counts(*lengths)
                pattern_type_count += 1
                canonical_pattern_count += sum(count for _, count in patterns)
                maximum_selected_points = max(
                    maximum_selected_points, sum(map(sum, lengths))
                )
                maximum_constraint_count = max(
                    maximum_constraint_count,
                    max((key[1] for key, _ in patterns), default=0),
                )
                coefficient = (
                    sp.Rational(first_coefficient.numerator, first_coefficient.denominator)
                    * sp.Rational(second_coefficient.numerator, second_coefficient.denominator)
                    * sp.Rational(third_coefficient.numerator, third_coefficient.denominator)
                )
                correlation += coefficient * selected_cycle_expectation(n, lengths)
    correlation = sp.factor(correlation)
    trace = sp.factor(n * (n - 1) * (n - 2) * correlation)
    cancelled = sp.cancel(trace)
    numerator, denominator = sp.fraction(cancelled)
    if denominator != 1:
        raise ArithmeticError("shape trace did not simplify to a polynomial")
    polynomial = sp.Poly(sp.expand(numerator), n)
    if polynomial.degree() > 3:
        raise ArithmeticError("orbit trace exceeds the expected cubic degree")
    _, certificate = reconstruct_character_polynomial(intermediate_tail)
    literal_start = max(
        int(certificate["threshold"]),
        maximum_constraint_count,
        8,
    )
    return {
        "correlation": correlation,
        "trace": sp.expand(polynomial.as_expr()),
        "trace_degree": polynomial.degree(),
        "falling_term_count": len(second_terms),
        "pattern_type_count": pattern_type_count,
        "canonical_pattern_count": canonical_pattern_count,
        "maximum_selected_point_count": maximum_selected_points,
        "maximum_constraint_count": maximum_constraint_count,
        "literal_symbolic_range_start": literal_start,
    }


@lru_cache(maxsize=1)
def exact_n8_shape_trace_endpoints() -> dict[tuple[int, ...], int]:
    n = 8
    source = padded_partition(n, (2,))
    final = padded_partition(n, FINAL_TAIL)
    intermediates = {
        tail: padded_partition(n, tail) for tail in STABLE_TAILS
    }
    transposition = list(range(n))
    transposition[0], transposition[1] = 1, 0
    cycle = list(range(n))
    cycle[0], cycle[1], cycle[2] = 1, 2, 0
    sums = {tail: 0 for tail in STABLE_TAILS}
    for permutation in itertools.permutations(range(n)):
        cycle_type = _cycle_type(permutation)
        transposed_type = _cycle_type(
            _compose(permutation, tuple(transposition))
        )
        cycled_type = _cycle_type(_compose(permutation, tuple(cycle)))
        common = (
            symmetric_character(final, cycle_type)
            * symmetric_character(source, cycled_type)
        )
        if common == 0:
            continue
        for tail, intermediate in intermediates.items():
            sums[tail] += common * symmetric_character(
                intermediate, transposed_type
            )
    orbit_size = n * (n - 1) * (n - 2)
    traces: dict[tuple[int, ...], int] = {}
    for tail, correlation_sum in sums.items():
        numerator = orbit_size * correlation_sum
        trace, remainder = divmod(numerator, math.factorial(n))
        if remainder:
            raise ArithmeticError("n=8 multiplicity trace is not integral")
        traces[tail] = trace
    return traces


def _finite_probe_traces() -> dict[tuple[tuple[int, ...], int], int]:
    if not COSET_STABLE_SHAPE_LABEL_PATH.exists():
        return {}
    try:
        payload = json.loads(COSET_STABLE_SHAPE_LABEL_PATH.read_text())
    except (json.JSONDecodeError, OSError):
        return {}
    traces: dict[tuple[tuple[int, ...], int], int] = {}
    for row in payload.get("records", []):
        polynomial = row.get("integer_characteristic_polynomial_candidate", [])
        if len(polynomial) < 2:
            continue
        traces[(tuple(row["intermediate_tail"]), int(row["n"]))] = -int(
            polynomial[1]
        )
    return traces


@lru_cache(maxsize=1)
def build_stable_shape_trace_certificate() -> StableShapeTraceCertificate:
    n = sp.symbols("n", integer=True, positive=True)
    endpoints = exact_n8_shape_trace_endpoints()
    finite_traces = _finite_probe_traces()
    records: list[StableShapeTraceRecord] = []
    for tail in STABLE_TAILS:
        symbolic = symbolic_shape_trace(tail)
        formula = sp.expand(symbolic["trace"])
        endpoint_formula = int(formula.subs(n, 8))
        endpoint_verified = endpoints[tail] == endpoint_formula
        comparisons = [
            (size, trace)
            for (record_tail, size), trace in finite_traces.items()
            if record_tail == tail
        ]
        agreements = sum(int(formula.subs(n, size)) == trace for size, trace in comparisons)
        second_multiplicity = kronecker_coefficient(
            padded_partition(8, tail),
            padded_partition(8, (2,)),
            padded_partition(8, FINAL_TAIL),
        )
        complete_already = tail == FINAL_TAIL
        remaining = 0 if complete_already else max(0, second_multiplicity - 1)
        theorem_proved = (
            endpoint_verified
            and int(symbolic["literal_symbolic_range_start"]) <= 9
            and agreements == len(comparisons)
        )
        records.append(
            StableShapeTraceRecord(
                intermediate_tail=tail,
                intermediate_partition=_tail_formula(tail),
                second_stage_multiplicity=second_multiplicity,
                character_polynomial=str(
                    sp.expand(reconstruct_character_polynomial(tail)[0])
                ),
                falling_character_term_count=int(symbolic["falling_term_count"]),
                falling_monomial_product_count=int(symbolic["pattern_type_count"]),
                canonical_equality_pattern_count=int(symbolic["canonical_pattern_count"]),
                maximum_selected_point_count=int(symbolic["maximum_selected_point_count"]),
                maximum_partial_permutation_constraint_count=int(
                    symbolic["maximum_constraint_count"]
                ),
                literal_symbolic_range_start=int(
                    symbolic["literal_symbolic_range_start"]
                ),
                exact_trace_polynomial=str(formula),
                trace_polynomial_degree=int(symbolic["trace_degree"]),
                exact_n8_character_sum_trace=endpoints[tail],
                exact_n8_formula_value=endpoint_formula,
                exact_n8_endpoint_verified=endpoint_verified,
                finite_probe_comparison_count=len(comparisons),
                finite_probe_trace_agreement_count=agreements,
                exact_all_n_at_least_8_trace_proved=theorem_proved,
                exact_complete_characteristic_polynomial_already_proved=(
                    complete_already
                ),
                remaining_exact_characteristic_coefficient_count=remaining,
                status=(
                    "exact-all-n-shape-trace-proved-higher-coefficients-open"
                    if theorem_proved and remaining
                    else (
                        "exact-all-n-shape-trace-proved-complete-polynomial-already-known"
                        if theorem_proved and complete_already
                        else "exact-all-n-shape-trace-proved-multiplicity-one"
                        if theorem_proved
                        else "shape-trace-certificate-failed"
                    )
                ),
            )
        )

    theorem_count = sum(record.exact_all_n_at_least_8_trace_proved for record in records)
    open_nontrivial = [
        record
        for record in records
        if record.second_stage_multiplicity > 1
        and not record.exact_complete_characteristic_polynomial_already_proved
    ]
    metrics: dict[str, int | float] = {
        "stable_shape_count": len(records),
        "exact_all_n_shape_trace_theorem_count": theorem_count,
        "new_exact_open_shape_trace_theorem_count": sum(
            record.exact_all_n_at_least_8_trace_proved for record in open_nontrivial
        ),
        "exact_n8_endpoint_count": sum(
            record.exact_n8_endpoint_verified for record in records
        ),
        "finite_probe_trace_comparison_count": sum(
            record.finite_probe_comparison_count for record in records
        ),
        "finite_probe_trace_agreement_count": sum(
            record.finite_probe_trace_agreement_count for record in records
        ),
        "maximum_canonical_equality_pattern_count": max(
            record.canonical_equality_pattern_count for record in records
        ),
        "maximum_partial_permutation_constraint_count": max(
            record.maximum_partial_permutation_constraint_count for record in records
        ),
        "remaining_open_shape_characteristic_coefficient_family_count": sum(
            record.remaining_exact_characteristic_coefficient_count
            for record in records
        ),
        "new_exact_complete_characteristic_polynomial_count": 0,
        "new_normalized_gap_theorem_count": 0,
        "new_coherent_shape_label_count": 0,
        "complete_racah_associator_count": 0,
        "hidden_involution_decoder_count": 0,
    }
    all_proved = theorem_count == len(records)
    return StableShapeTraceCertificate(
        created_at=utc_now(),
        theorem={
            "range": "every integer n>=8",
            "statement": (
                "The first characteristic coefficient of the common support-intersection-two orbit Hamiltonian "
                "is the listed exact cubic-or-lower polynomial for every one of the nine stable intermediate shapes."
            ),
            "proved": all_proved,
        },
        method_contract={
            "trace_identity": (
                "n(n-1)(n-2) E_g[chi_xi(g) chi_eta(g tau) chi_W(g c)]"
            ),
            "symbolic_method": (
                "falling cycle-count expansion plus exact partial-permutation equality patterns"
            ),
            "endpoint_method": "single exact S_8 character-sum pass over all nine intermediate shapes",
            "interpolation_used": False,
            "floating_arithmetic_used_for_theorem": False,
        },
        shape_records=records,
        headline_metrics=metrics,
        claim_gate={
            "all_nine_exact_trace_polynomials_proved": all_proved,
            "all_six_open_nontrivial_trace_polynomials_proved": (
                metrics["new_exact_open_shape_trace_theorem_count"] == 6
            ),
            "all_characteristic_polynomials_proved": False,
            "all_normalized_gaps_proved": False,
            "all_coherent_label_circuits_proved": False,
            "complete_racah_associator_proved": False,
            "hidden_involution_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The exact traces remove one coefficient obligation per shape, but seven determinant/higher-"
                "coefficient families, six normalized gaps, coherent compilation, transitions, and decoding remain."
            ),
        },
        status=(
            "exact-nine-shape-traces-proved-seven-coefficient-families-open"
            if all_proved
            else "stable-shape-trace-certificate-failed"
        ),
        summary=(
            f"Proved {theorem_count}/9 exact stable-shape trace polynomials for every n>=8, including all six "
            f"previously open nontrivial label families; {metrics['remaining_open_shape_characteristic_coefficient_family_count']} "
            "higher characteristic-coefficient families remain before gap analysis."
        ),
        falsifiers_triggered=[
            "One exact trace does not determine a quadratic or cubic characteristic polynomial.",
            "Exact eigenvalue sums do not prove normalized eigenvalue separation.",
            "A spectral identity does not compile the orbit sum into a coherent circuit.",
            "Shape labels do not implement coupling-tree transitions or decode a hidden involution.",
        ],
    )


def write_stable_shape_trace_certificate(
    output_path: Path = COSET_STABLE_SHAPE_TRACE_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(build_stable_shape_trace_certificate())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-EXACT-NINE-SHAPE-TRACES-AS-COMPLETE-LABEL-PROOF",
                source=str(output_path),
                claim=(
                    "Exact first characteristic coefficients for all nine shapes prove complete coherent labels."
                ),
                reason_invalid=(
                    "Five open multiplicity-two shapes still need determinants, one multiplicity-three shape needs "
                    "two higher coefficients, and all six need normalized gap and circuit theorems."
                ),
                lesson=(
                    "Generalize marked-cycle moments only to the seven remaining coefficient families, then apply "
                    "exact root separation and coherent block-encoding proof gates."
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
                artifacts={"coset_stable_shape_trace_certificate": str(output_path)},
            )
        )
    return payload


if __name__ == "__main__":
    report = write_stable_shape_trace_certificate()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
