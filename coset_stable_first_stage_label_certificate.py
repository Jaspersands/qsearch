"""Exact coherent labels for the two nontrivial first-stage stable blocks.

For W_n=(n-2,2), the exact nine-shape stable Racah family contains only two
intermediate targets with nontrivial first-stage multiplicity:

    g(W_n,W_n,W_n)=2,
    g(W_n,W_n,xi_n)=2,  xi_n=(n-3,2,1).

The xi_n gap was proved by the commutant gap certificate.  This module closes
the remaining W_n block for the same support-intersection-two orbit
Hamiltonian.  Equality-pattern character sums give exact Tr(H) and Tr(H^2),
so the quadratic discriminant and normalized gap follow without fitting
finite spectra.

These labels remain in the original W_n tensor W_n encoding.  They resolve
first-stage multiplicity but do not by themselves identify the intermediate
shape, change coupling trees, or decode a hidden involution.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

import sympy as sp

from coset_commutant_gap_certificate import build_commutant_gap_certificate
from coset_stable_second_moment_certificate import (
    generalized_equality_pattern_counts,
    relative_orbit_class_counts,
)
from coset_stable_shape_family_certificate import (
    _stirling_second,
    build_stable_shape_family_certificate,
)
from coset_stable_shape_trace_certificate import falling_character_terms
from coset_stable_trace_certificate import (
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
from symmetric_character import kronecker_coefficient


COSET_STABLE_FIRST_STAGE_LABEL_PATH = Path(
    "research/representation/coset_stable_first_stage_label_certificate.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-STABLE-FIRST-STAGE-LABEL-CERTIFICATE"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
W_TAIL = (2,)
XI_TAIL = (2, 1)


@dataclass(frozen=True)
class FirstStageEndpointRecord:
    n: int
    exact_pattern_second_power_trace: int
    formula_second_power_trace: int
    residual: int
    verified: bool


@dataclass(frozen=True)
class FirstStageMultiplicityRecord:
    target_tail: tuple[int, ...]
    target_partition: str
    multiplicity: int
    exact_first_power_trace: str
    exact_second_power_trace: str
    exact_characteristic_polynomial: str
    exact_discriminant: str
    exact_raw_gap: str
    lcu_term_count: str
    exact_normalized_gap: str
    normalized_gap_lower_bound: str
    normalized_gap_inverse_polynomial_exponent: int
    proof_source: str
    coherent_phase_estimation_label_proved: bool
    status: str


@dataclass(frozen=True)
class StableFirstStageLabelCertificate:
    created_at: str
    theorem: dict[str, object]
    multiplicity_certificate: dict[str, object]
    equality_pattern_certificate: dict[str, object]
    endpoint_records: list[FirstStageEndpointRecord]
    target_records: list[FirstStageMultiplicityRecord]
    circuit_contract: dict[str, object]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _falling(value: sp.Expr, count: int) -> sp.Expr:
    return sp.prod(value - offset for offset in range(count))


def _falling_integer(value: int, count: int) -> int:
    return math.prod(value - offset for offset in range(count))


@lru_cache(maxsize=1)
def stable_wn_cubic_multiplicity_certificate() -> dict[str, object]:
    """Prove <chi_W^2,chi_W>=2 for every n>=6."""

    x1, x2 = sp.symbols("X1 X2")
    character = x1 * (x1 - 1) / 2 + x2 - x1
    polynomial = sp.Poly(sp.expand(character**3), x1, x2)
    expectation = sp.Integer(0)
    threshold = 0
    falling_term_count = 0
    for powers, coefficient in polynomial.terms():
        for fixed_count in range(powers[0] + 1):
            for two_cycle_count in range(powers[1] + 1):
                transformed = (
                    coefficient
                    * _stirling_second(powers[0], fixed_count)
                    * _stirling_second(powers[1], two_cycle_count)
                )
                if not transformed:
                    continue
                falling_term_count += 1
                threshold = max(threshold, fixed_count + 2 * two_cycle_count)
                expectation += transformed / sp.Integer(2) ** two_cycle_count
    direct_n6 = kronecker_coefficient((4, 2), (4, 2), (4, 2))
    proved = threshold == 6 and expectation == 2 and direct_n6 == 2
    return {
        "character_polynomial": "binomial(X1,2)+X2-X1",
        "stable_factorial_moment_threshold": threshold,
        "stable_multiplicity": int(expectation),
        "direct_n6_multiplicity": direct_n6,
        "falling_factorial_term_count": falling_term_count,
        "all_n_at_least_6_multiplicity": 2,
        "proved": proved,
    }


@lru_cache(maxsize=1)
def symbolic_wn_first_power_trace() -> dict[str, object]:
    n = sp.symbols("n", integer=True, positive=True)
    terms = falling_character_terms(W_TAIL)
    correlation = sp.Integer(0)
    pattern_type_count = 0
    canonical_pattern_count = 0
    maximum_constraint = 0
    for first, first_coefficient in terms:
        for second, second_coefficient in terms:
            for third, third_coefficient in terms:
                lengths = (first, second, third)
                patterns = equality_pattern_counts(*lengths)
                pattern_type_count += 1
                canonical_pattern_count += sum(count for _, count in patterns)
                maximum_constraint = max(
                    maximum_constraint,
                    max((key[1] for key, _ in patterns), default=0),
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
                correlation += coefficient * selected_cycle_expectation(n, lengths)
    trace = sp.cancel(n * (n - 1) * (n - 2) * correlation)
    numerator, denominator = sp.fraction(trace)
    if denominator != 1:
        raise ArithmeticError("first-stage W trace did not simplify to a polynomial")
    return {
        "trace": sp.expand(numerator),
        "pattern_type_count": pattern_type_count,
        "canonical_pattern_count": canonical_pattern_count,
        "maximum_constraint_count": maximum_constraint,
        "literal_symbolic_range_start": max(6, maximum_constraint),
    }


@lru_cache(maxsize=None)
def _wn_shifted_correlation(
    left_shift: tuple[int, ...], right_shift: tuple[int, ...]
) -> tuple[sp.Expr, int, int]:
    n = sp.symbols("n", integer=True, positive=True)
    special_count = len(left_shift)
    terms = falling_character_terms(W_TAIL)
    total = sp.Integer(0)
    maximum_special_plus_generic = special_count
    maximum_constraint = 0
    for first, first_coefficient in terms:
        for second, second_coefficient in terms:
            for third, third_coefficient in terms:
                denominator = math.prod((*first, *second, *third))
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
                    sp.Rational(pattern_count, denominator)
                    * _falling(n - special_count, generic_count)
                    / _falling(n, constraint_count)
                    for (
                        generic_count,
                        constraint_count,
                    ), pattern_count in patterns
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
    return sp.factor(total), maximum_special_plus_generic, maximum_constraint


@lru_cache(maxsize=1)
def symbolic_wn_second_power_trace() -> dict[str, object]:
    n = sp.symbols("n", integer=True, positive=True)
    orbit_size = n * (n - 1) * (n - 2)
    total = sp.Integer(0)
    maximum_special_plus_generic = 0
    maximum_constraint = 0
    classes = relative_orbit_class_counts()
    for (left_shift, right_shift), multiplicities in classes.items():
        multiplicity = sum(
            count * sp.binomial(n - 3, outside_count)
            for outside_count, count in enumerate(multiplicities)
        )
        correlation, special_plus_generic, constraint = _wn_shifted_correlation(
            left_shift, right_shift
        )
        maximum_special_plus_generic = max(
            maximum_special_plus_generic, special_plus_generic
        )
        maximum_constraint = max(maximum_constraint, constraint)
        total += multiplicity * correlation
    second_trace = sp.cancel(sp.expand_func(orbit_size * total))
    numerator, denominator = sp.fraction(second_trace)
    if denominator != 1:
        raise ArithmeticError(
            "first-stage W second moment did not simplify to a polynomial"
        )
    polynomial = sp.Poly(sp.expand(numerator), n)
    return {
        "second_power_trace": polynomial.as_expr(),
        "relative_orbit_class_count": len(classes),
        "maximum_special_plus_generic_count": maximum_special_plus_generic,
        "maximum_constraint_count": maximum_constraint,
        "literal_symbolic_range_start": max(
            6, maximum_special_plus_generic, maximum_constraint
        ),
    }


@lru_cache(maxsize=None)
def _exact_numeric_wn_shifted_correlation(
    n: int, left_shift: tuple[int, ...], right_shift: tuple[int, ...]
) -> Fraction:
    special_count = len(left_shift)
    terms = falling_character_terms(W_TAIL)
    total = Fraction(0)
    for first, first_coefficient in terms:
        for second, second_coefficient in terms:
            for third, third_coefficient in terms:
                denominator = math.prod((*first, *second, *third))
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
                        denominator * _falling_integer(n, constraint_count),
                    )
                total += (
                    first_coefficient
                    * second_coefficient
                    * third_coefficient
                    * expectation
                )
    return total


@lru_cache(maxsize=None)
def exact_wn_second_power_trace(n: int) -> int:
    if n < 6:
        raise ValueError("the stable multiplicity-two W target starts at n=6")
    relative_sum = Fraction(0)
    for (left_shift, right_shift), multiplicities in relative_orbit_class_counts().items():
        multiplicity = sum(
            count * math.comb(n - 3, outside_count)
            for outside_count, count in enumerate(multiplicities)
        )
        relative_sum += multiplicity * _exact_numeric_wn_shifted_correlation(
            n, left_shift, right_shift
        )
    value = n * (n - 1) * (n - 2) * relative_sum
    if value.denominator != 1:
        raise ArithmeticError("first-stage W second moment is not integral")
    return value.numerator


@lru_cache(maxsize=1)
def build_stable_first_stage_label_certificate() -> (
    StableFirstStageLabelCertificate
):
    n = sp.symbols("n", integer=True, positive=True)
    m = sp.symbols("m", integer=True, nonnegative=True)
    x = sp.symbols("x")
    family = build_stable_shape_family_certificate()
    first_multiplicities = {
        tuple(record.tail): record.first_stage_multiplicity
        for record in family.shape_records
    }
    nontrivial = {
        tail: multiplicity
        for tail, multiplicity in first_multiplicities.items()
        if multiplicity > 1
    }
    multiplicity = stable_wn_cubic_multiplicity_certificate()
    first = symbolic_wn_first_power_trace()
    second = symbolic_wn_second_power_trace()
    first_trace = sp.expand(first["trace"])
    second_trace = sp.expand(second["second_power_trace"])
    second_coefficient = sp.factor((first_trace**2 - second_trace) / 2)
    discriminant = sp.factor(2 * second_trace - first_trace**2)
    expected_first = 2 * n**3 - 19 * n**2 + 51 * n - 36
    expected_second = (
        2 * n**6
        - 38 * n**5
        + 283 * n**4
        - 1048 * n**3
        + 2021 * n**2
        - 1904 * n
        + 688
    )
    expected_discriminant = (
        n**4 - 14 * n**3 + 73 * n**2 - 136 * n + 80
    )
    shifted_discriminant = sp.Poly(
        sp.expand(discriminant.subs(n, m + 6)), m
    )
    positive_shift_coefficients = all(
        coefficient > 0 for coefficient in shifted_discriminant.all_coeffs()
    )
    endpoints = [
        FirstStageEndpointRecord(
            n=endpoint_n,
            exact_pattern_second_power_trace=(
                exact_value := exact_wn_second_power_trace(endpoint_n)
            ),
            formula_second_power_trace=(
                formula_value := int(second_trace.subs(n, endpoint_n))
            ),
            residual=exact_value - formula_value,
            verified=exact_value == formula_value,
        )
        for endpoint_n in range(
            6, int(second["literal_symbolic_range_start"])
        )
    ]
    identities_proved = (
        sp.simplify(first_trace - expected_first) == 0
        and sp.simplify(second_trace - expected_second) == 0
        and sp.simplify(discriminant - expected_discriminant) == 0
        and positive_shift_coefficients
        and shifted_discriminant.eval(0) == 164
    )
    wn_proved = (
        bool(multiplicity["proved"])
        and identities_proved
        and all(record.verified for record in endpoints)
    )
    xi = build_commutant_gap_certificate()
    xi_proved = bool(xi.claim_gate["all_n_restricted_gap_theorem_proved"])
    exact_nontrivial_family = nontrivial == {W_TAIL: 2, XI_TAIL: 2}
    theorem_proved = wn_proved and xi_proved and exact_nontrivial_family

    term_count = n * (n - 1) * (n - 2)
    wn_characteristic = sp.Poly(x**2 - first_trace * x + second_coefficient, x)
    records = [
        FirstStageMultiplicityRecord(
            target_tail=W_TAIL,
            target_partition="W_n=(n-2,2)",
            multiplicity=2,
            exact_first_power_trace=str(first_trace),
            exact_second_power_trace=str(second_trace),
            exact_characteristic_polynomial=str(wn_characteristic.as_expr()),
            exact_discriminant=str(discriminant),
            exact_raw_gap=f"sqrt({discriminant})",
            lcu_term_count=str(term_count),
            exact_normalized_gap=f"sqrt({discriminant})/({term_count})",
            normalized_gap_lower_bound="12/n**3",
            normalized_gap_inverse_polynomial_exponent=3,
            proof_source="exact equality-pattern first/second moments and positive discriminant",
            coherent_phase_estimation_label_proved=wn_proved,
            status="exact-first-stage-W-label-proved" if wn_proved else "first-stage-W-label-failed",
        ),
        FirstStageMultiplicityRecord(
            target_tail=XI_TAIL,
            target_partition="xi_n=(n-3,2,1)",
            multiplicity=2,
            exact_first_power_trace="sum of the two parity eigenvalues",
            exact_second_power_trace="sum of the squared parity eigenvalues",
            exact_characteristic_polynomial="product over the exact symmetric/antisymmetric eigenvalues",
            exact_discriminant="4*(n-2)**2",
            exact_raw_gap="2*(n-2)",
            lcu_term_count=str(term_count),
            exact_normalized_gap="2/(n*(n-1))",
            normalized_gap_lower_bound="2/n**2",
            normalized_gap_inverse_polynomial_exponent=2,
            proof_source="coset_commutant_gap_certificate.py",
            coherent_phase_estimation_label_proved=xi_proved,
            status="exact-first-stage-xi-label-proved" if xi_proved else "first-stage-xi-label-failed",
        ),
    ]
    metrics: dict[str, int | float] = {
        "stable_intermediate_shape_count": len(first_multiplicities),
        "nontrivial_first_stage_shape_count": len(nontrivial),
        "multiplicity_free_first_stage_shape_count": sum(
            multiplicity_value == 1
            for multiplicity_value in first_multiplicities.values()
        ),
        "new_exact_first_stage_gap_theorem_count": int(wn_proved),
        "all_nontrivial_first_stage_gap_theorem_count": sum(
            record.coherent_phase_estimation_label_proved for record in records
        ),
        "all_stable_first_stage_multiplicity_resolved_shape_count": (
            len(first_multiplicities) if theorem_proved else 0
        ),
        "exact_endpoint_verified_count": sum(record.verified for record in endpoints),
        "relative_orbit_class_count": int(second["relative_orbit_class_count"]),
        "minimum_uniform_raw_gap_lower_bound": 12,
        "maximum_normalized_gap_inverse_polynomial_exponent": 3,
        "coherent_first_stage_label_transform_count": int(theorem_proved),
        "intermediate_shape_label_transform_count": 0,
        "coupling_tree_transition_circuit_count": 0,
        "hidden_involution_decoder_count": 0,
    }
    return StableFirstStageLabelCertificate(
        created_at=utc_now(),
        theorem={
            "range": "every integer n>=6",
            "statement": (
                "The support-intersection-two orbit Hamiltonian has an inverse-polynomial normalized gap in both "
                "nontrivial first-stage stable multiplicity blocks. Combined with the seven multiplicity-free "
                "targets, every one of the nine stable W_n tensor W_n intermediate shapes has resolved first-stage "
                "multiplicity."
            ),
            "proved": theorem_proved,
        },
        multiplicity_certificate={
            "W_target": multiplicity,
            "xi_target_source": "coset_commutant_gap_certificate.py",
            "exact_nontrivial_target_set": [list(W_TAIL), list(XI_TAIL)],
            "exact_nontrivial_target_set_proved": exact_nontrivial_family,
        },
        equality_pattern_certificate={
            "first_power_trace": str(first_trace),
            "second_power_trace": str(second_trace),
            "second_characteristic_coefficient": str(second_coefficient),
            "discriminant": str(discriminant),
            "discriminant_after_n_equals_m_plus_6": str(
                shifted_discriminant.as_expr()
            ),
            "shifted_discriminant_coefficients": [
                int(value) for value in shifted_discriminant.all_coeffs()
            ],
            "positive_for_every_n_at_least_6": positive_shift_coefficients,
            "literal_first_moment_range_start": int(
                first["literal_symbolic_range_start"]
            ),
            "literal_second_moment_range_start": int(
                second["literal_symbolic_range_start"]
            ),
            "relative_orbit_class_count": int(second["relative_orbit_class_count"]),
            "proved": wn_proved,
        },
        endpoint_records=endpoints,
        target_records=records,
        circuit_contract={
            "operator": (
                "H_12=sum rho_W(tau) tensor rho_W(c) over ordered triples with tau supported on c"
            ),
            "encoding": "the original W_n tensor W_n registers; no dense Clebsch table is used",
            "prepare": "uniform reversible preparation over n(n-1)(n-2) ordered triples",
            "select": "controlled Young-basis transposition and oriented 3-cycle actions",
            "label_method": "coherent phase estimation at the proved target-controlled precision",
            "multiplicity_free_targets": "require no internal eigenlabel",
            "complexity": "polynomial in n and log(1/error)",
            "does_not_produce": [
                "the intermediate shape label",
                "a compressed eta carrier register",
                "a left/right coupling-tree transition",
                "a hidden-involution decoder",
            ],
        },
        headline_metrics=metrics,
        claim_gate={
            "all_nontrivial_first_stage_gaps_proved": theorem_proved,
            "all_stable_first_stage_multiplicity_labels_proved": theorem_proved,
            "intermediate_shape_label_proved_by_this_certificate": False,
            "encoded_channel_router_proved": False,
            "coupling_tree_transition_proved": False,
            "hidden_involution_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "First-stage multiplicity is now fully resolved on the stable family, but shape identification, "
                "encoded channel routing, coupling-tree transitions, decoding, and separation remain separate obligations."
            ),
        },
        status=(
            "all-stable-first-stage-multiplicity-labels-proved-shape-routing-open"
            if theorem_proved
            else "stable-first-stage-label-certificate-failed"
        ),
        summary=(
            "Proved the missing W_n first-stage quadratic gap and combined it with the xi_n parity gap, resolving "
            "all nontrivial first-stage multiplicities in the exact nine-shape stable family."
        ),
        falsifiers_triggered=[
            "Second-stage shape-local labels cannot silently stand in for unresolved first-stage multiplicity.",
            "Exact first-stage gaps do not identify the intermediate shape without a commuting shape label.",
            "A nondestructive encoded eigenlabel is not automatically a compressed Clebsch isometry.",
            "First-stage spectral control alone does not construct a Racah transition or decoder.",
        ],
    )


def write_stable_first_stage_label_certificate(
    output_path: Path = COSET_STABLE_FIRST_STAGE_LABEL_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(build_stable_first_stage_label_certificate())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-SECOND-STAGE-LABELS-AS-COMPLETE-LEFT-TREE-BASIS",
                source=str(output_path),
                claim=(
                    "Second-stage stable-shape eigenlabels alone resolve the complete left-coupled multiplicity basis."
                ),
                reason_invalid=(
                    "Two intermediate targets also have first-stage multiplicity two. Those labels require their "
                    "own exact gap theorem, now supplied here; intermediate shape routing remains separate."
                ),
                lesson=(
                    "Compose commuting shape, first-stage multiplicity, and second-stage multiplicity labels before "
                    "claiming a complete encoded coupling-tree basis."
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
                    "coset_stable_first_stage_label_certificate": str(output_path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_stable_first_stage_label_certificate()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
