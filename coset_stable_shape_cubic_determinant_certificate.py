"""Exact determinant for the last unresolved stable Racah shape spectrum.

After exact first and second moments, only the determinant of the
multiplicity-three intermediate family eta_n=(n-4,3,1) remains.  Fixing one
term in Tr(H^3) leaves 129 simultaneous-conjugacy classes of relative orbit
terms.  This module evaluates those classes with eta_n's falling character
polynomial and applies Newton's third identity.

The result completes the characteristic polynomials of all nine intermediate
shapes in the stable final-xi sector.  It does not prove normalized root gaps,
coherent orbit-LCU compilation, coupling-tree transitions, a decoder, or a
quantum advantage.
"""

from __future__ import annotations

import json
import math
import multiprocessing
import os
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict, dataclass
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

import sympy as sp

from coset_stable_second_moment_certificate import generalized_equality_pattern_counts
from coset_stable_shape_second_moment_certificate import (
    symbolic_shape_second_moment,
)
from coset_stable_shape_trace_certificate import (
    FINAL_TAIL,
    falling_character_terms,
    symbolic_shape_trace,
)
from coset_stable_third_moment_certificate import (
    ShiftPair,
    third_relative_orbit_class_counts,
)
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


COSET_STABLE_SHAPE_CUBIC_DETERMINANT_PATH = Path(
    "research/representation/coset_stable_shape_cubic_determinant_certificate.json"
)
COSET_STABLE_SHAPE_CUBIC_PATTERN_PATH = Path(
    "research/representation/coset_stable_shape_cubic_pattern_checkpoint.json"
)
COSET_STABLE_SHAPE_LABEL_PATH = Path(
    "research/representation/coset_stable_shape_label_probe.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-STABLE-SHAPE-CUBIC-DETERMINANT-CERTIFICATE"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
TARGET_TAIL = (3, 1)
PatternCoefficient = tuple[int, int, Fraction]


@dataclass(frozen=True)
class CubicDeterminantEndpoint:
    n: int
    exact_pattern_third_power_trace: int
    symbolic_formula_value: int
    trace_residual: int
    exact_determinant: int
    sparse_reference_determinant: int | None
    sparse_reference_residual: int | None
    verified: bool


@dataclass(frozen=True)
class StableShapeCubicDeterminantCertificate:
    created_at: str
    theorem: dict[str, object]
    relative_orbit_certificate: dict[str, object]
    symbolic_certificate: dict[str, object]
    endpoint_records: list[CubicDeterminantEndpoint]
    newton_certificate: dict[str, object]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


@lru_cache(maxsize=None)
def shifted_cubic_shape_pattern_coefficients(
    left_shift: tuple[int, ...], right_shift: tuple[int, ...]
) -> tuple[tuple[PatternCoefficient, ...], int]:
    coefficients: defaultdict[tuple[int, int], Fraction] = defaultdict(Fraction)
    raw_pattern_count = 0
    for first, first_coefficient in falling_character_terms(FINAL_TAIL):
        for second, second_coefficient in falling_character_terms(TARGET_TAIL):
            for third, third_coefficient in falling_character_terms((2,)):
                rotation_denominator = math.prod((*first, *second, *third))
                character_coefficient = (
                    first_coefficient
                    * second_coefficient
                    * third_coefficient
                    / rotation_denominator
                )
                patterns = generalized_equality_pattern_counts(
                    first,
                    second,
                    third,
                    left_shift,
                    right_shift,
                )
                raw_pattern_count += sum(count for _, count in patterns)
                for key, pattern_count in patterns:
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
    coefficients, raw_count = shifted_cubic_shape_pattern_coefficients(*class_key)
    return class_key, coefficients, raw_count


def _load_pattern_checkpoint(
    path: Path,
) -> dict[ShiftPair, tuple[tuple[PatternCoefficient, ...], int]] | None:
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text())
    except (json.JSONDecodeError, OSError):
        return None
    if payload.get("target_tail") != list(TARGET_TAIL):
        return None
    summaries: dict[ShiftPair, tuple[tuple[PatternCoefficient, ...], int]] = {}
    for row in payload.get("class_summaries", []):
        class_key = (tuple(row["left_shift"]), tuple(row["right_shift"]))
        coefficients = tuple(
            (
                int(item["generic_count"]),
                int(item["constraint_count"]),
                Fraction(int(item["numerator"]), int(item["denominator"])),
            )
            for item in row["coefficients"]
        )
        summaries[class_key] = (coefficients, int(row["raw_pattern_count"]))
    expected_keys = set(third_relative_orbit_class_counts())
    return summaries if set(summaries) == expected_keys else None


def _write_pattern_checkpoint(
    path: Path,
    summaries: dict[ShiftPair, tuple[tuple[PatternCoefficient, ...], int]],
) -> None:
    payload = {
        "target_tail": list(TARGET_TAIL),
        "exact_rational_coefficients": True,
        "relative_orbit_class_count": len(summaries),
        "class_summaries": [
            {
                "left_shift": list(class_key[0]),
                "right_shift": list(class_key[1]),
                "raw_pattern_count": raw_count,
                "coefficients": [
                    {
                        "generic_count": generic_count,
                        "constraint_count": constraint_count,
                        "numerator": coefficient.numerator,
                        "denominator": coefficient.denominator,
                    }
                    for generic_count, constraint_count, coefficient in coefficients
                ],
            }
            for class_key, (coefficients, raw_count) in sorted(summaries.items())
        ],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))


def all_cubic_shape_pattern_summaries(
    workers: int | None = None,
    checkpoint_path: Path = COSET_STABLE_SHAPE_CUBIC_PATTERN_PATH,
) -> dict[ShiftPair, tuple[tuple[PatternCoefficient, ...], int]]:
    checkpoint = _load_pattern_checkpoint(checkpoint_path)
    if checkpoint is not None:
        return checkpoint
    class_keys = list(third_relative_orbit_class_counts())
    worker_count = workers if workers is not None else min(8, os.cpu_count() or 1)
    if worker_count <= 1:
        summaries = {
            class_key: shifted_cubic_shape_pattern_coefficients(*class_key)
            for class_key in class_keys
        }
    else:
        context = multiprocessing.get_context("fork")
        with ProcessPoolExecutor(
            max_workers=worker_count, mp_context=context
        ) as executor:
            rows = executor.map(_pattern_worker, class_keys, chunksize=1)
            summaries = {
                class_key: (coefficients, raw_count)
                for class_key, coefficients, raw_count in rows
            }
    _write_pattern_checkpoint(checkpoint_path, summaries)
    return summaries


def _falling(value: sp.Expr, count: int) -> sp.Expr:
    return sp.prod(value - offset for offset in range(count))


def _falling_integer(value: int, count: int) -> int:
    return math.prod(value - offset for offset in range(count))


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
    if n < 8:
        raise ValueError("the stable nine-shape endpoint starts at n=8")
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
        raise ArithmeticError("cubic-shape third power trace is not integral")
    return value.numerator


def _finite_probe_determinants() -> dict[int, int]:
    if not COSET_STABLE_SHAPE_LABEL_PATH.exists():
        return {}
    try:
        payload = json.loads(COSET_STABLE_SHAPE_LABEL_PATH.read_text())
    except (json.JSONDecodeError, OSError):
        return {}
    determinants: dict[int, int] = {}
    for row in payload.get("records", []):
        if tuple(row.get("intermediate_tail", ())) != TARGET_TAIL:
            continue
        polynomial = row.get("integer_characteristic_polynomial_candidate", [])
        if len(polynomial) == 4:
            determinants[int(row["n"])] = -int(polynomial[3])
    return determinants


@lru_cache(maxsize=4)
def build_stable_shape_cubic_determinant_certificate(
    workers: int | None = None,
) -> StableShapeCubicDeterminantCertificate:
    n = sp.symbols("n", integer=True, positive=True)
    orbit_size = n * (n - 1) * (n - 2)
    classes = third_relative_orbit_class_counts()
    summaries = all_cubic_shape_pattern_summaries(workers=workers)
    total = sp.Integer(0)
    maximum_support_plus_generic = 0
    maximum_constraint = 0
    for class_key, multiplicities in classes.items():
        coefficients, _ = summaries[class_key]
        symbolic_multiplicity = sum(
            multiplicity * sp.binomial(n - 3, outside_count)
            for outside_count, multiplicity in enumerate(multiplicities)
        )
        total += symbolic_multiplicity * symbolic_correlation_from_patterns(
            class_key[0], coefficients
        )
        maximum_support_plus_generic = max(
            maximum_support_plus_generic,
            max(
                (len(class_key[0]) + row[0] for row in coefficients),
                default=len(class_key[0]),
            ),
        )
        maximum_constraint = max(
            maximum_constraint,
            max((row[1] for row in coefficients), default=0),
        )
    third_trace = sp.cancel(sp.expand_func(orbit_size * total))
    trace_numerator, trace_denominator = sp.fraction(third_trace)
    stable_polynomial_proved = (
        trace_denominator == 1
        and sp.Poly(sp.expand(trace_numerator), n).degree() <= 9
    )
    third_trace = sp.expand(trace_numerator)

    first_trace = sp.expand(symbolic_shape_trace(TARGET_TAIL)["trace"])
    second_moment = symbolic_shape_second_moment(TARGET_TAIL)
    second_trace = sp.expand(second_moment["second_power_trace"])
    second_coefficient = sp.factor((first_trace**2 - second_trace) / 2)
    determinant = sp.factor(
        (third_trace - first_trace * second_trace + second_coefficient * first_trace)
        / 3
    )
    determinant_numerator, determinant_denominator = sp.fraction(determinant)
    newton_proved = (
        determinant_denominator == 1
        and sp.Poly(sp.expand(determinant_numerator), n).degree() <= 9
    )
    determinant = sp.factor(determinant_numerator)
    literal_start = max(8, maximum_support_plus_generic, maximum_constraint)
    finite_determinants = _finite_probe_determinants()
    endpoints: list[CubicDeterminantEndpoint] = []
    for endpoint_n in range(8, literal_start):
        exact_trace = exact_endpoint_third_power_trace(endpoint_n, summaries)
        formula_trace = int(third_trace.subs(n, endpoint_n))
        exact_determinant = int(determinant.subs(n, endpoint_n))
        sparse_reference = finite_determinants.get(endpoint_n)
        sparse_residual = (
            exact_determinant - sparse_reference
            if sparse_reference is not None
            else None
        )
        endpoints.append(
            CubicDeterminantEndpoint(
                n=endpoint_n,
                exact_pattern_third_power_trace=exact_trace,
                symbolic_formula_value=formula_trace,
                trace_residual=exact_trace - formula_trace,
                exact_determinant=exact_determinant,
                sparse_reference_determinant=sparse_reference,
                sparse_reference_residual=sparse_residual,
                verified=(
                    exact_trace == formula_trace
                    and (sparse_residual is None or sparse_residual == 0)
                ),
            )
        )

    raw_counts_by_outside = [
        sum(multiplicities[outside] for multiplicities in classes.values())
        for outside in range(7)
    ]
    expected_raw_counts = [36, 540, 2484, 5292, 5832, 3240, 720]
    classification_proved = (
        len(classes) == 129 and raw_counts_by_outside == expected_raw_counts
    )
    endpoints_proved = all(record.verified for record in endpoints)
    finite_match_count = sum(
        record.sparse_reference_residual == 0
        for record in endpoints
        if record.sparse_reference_residual is not None
    )
    theorem_proved = (
        classification_proved
        and stable_polynomial_proved
        and newton_proved
        and endpoints_proved
        and finite_match_count == len(finite_determinants)
    )
    metrics: dict[str, int | float] = {
        "relative_orbit_class_count": len(classes),
        "raw_relative_term_type_count": sum(raw_counts_by_outside),
        "maximum_active_support_size": max(len(key[0]) for key in classes),
        "nonzero_pattern_coefficient_count": sum(
            len(coefficients) for coefficients, _ in summaries.values()
        ),
        "raw_canonical_pattern_count": sum(
            raw_count for _, raw_count in summaries.values()
        ),
        "literal_symbolic_minimum_n": literal_start,
        "exact_endpoint_verified_count": sum(record.verified for record in endpoints),
        "finite_sparse_determinant_comparison_count": len(finite_determinants),
        "finite_sparse_determinant_match_count": finite_match_count,
        "exact_cubic_shape_determinant_theorem_count": int(theorem_proved),
        "new_exact_complete_cubic_shape_polynomial_count": int(theorem_proved),
        "exact_complete_stable_shape_polynomial_count": 9 if theorem_proved else 8,
        "remaining_open_shape_characteristic_coefficient_family_count": (
            0 if theorem_proved else 1
        ),
        "new_normalized_gap_theorem_count": 0,
        "new_coherent_shape_label_count": 0,
        "complete_racah_associator_count": 0,
        "hidden_involution_decoder_count": 0,
    }
    return StableShapeCubicDeterminantCertificate(
        created_at=utc_now(),
        theorem={
            "range": "every integer n>=8",
            "intermediate_partition": "eta_n=(n-4,3,1)",
            "third_power_trace": str(third_trace),
            "determinant": str(determinant),
            "statement": (
                "The multiplicity-three stable-shape orbit Hamiltonian has the displayed exact determinant and "
                "complete cubic characteristic polynomial for every n>=8."
            ),
            "proved": theorem_proved,
        },
        relative_orbit_certificate={
            "fixed_first_term": "tau_0=(1 2), c_0=(1 2 3)",
            "relative_orbit_class_count": len(classes),
            "raw_counts_by_outside_support": raw_counts_by_outside,
            "expected_raw_counts_by_outside_support": expected_raw_counts,
            "classification_verified": classification_proved,
            "canonicalization": "two-colored permutation graph canonical form",
            "exact_pattern_checkpoint": str(
                COSET_STABLE_SHAPE_CUBIC_PATTERN_PATH
            ),
        },
        symbolic_certificate={
            "literal_range": f"n>={literal_start}",
            "third_power_trace": str(third_trace),
            "polynomial_degree": (
                int(sp.Poly(third_trace, n).degree())
                if stable_polynomial_proved
                else -1
            ),
            "maximum_support_plus_generic_count": maximum_support_plus_generic,
            "maximum_constraint_count": maximum_constraint,
            "identity_verified": stable_polynomial_proved,
            "interpolation_used": False,
        },
        endpoint_records=endpoints,
        newton_certificate={
            "identity": "p3-e1*p2+e2*p1-3*e3=0",
            "first_characteristic_coefficient": str(first_trace),
            "second_characteristic_coefficient": str(second_coefficient),
            "third_characteristic_coefficient_determinant": str(determinant),
            "identity_verified": newton_proved,
        },
        headline_metrics=metrics,
        claim_gate={
            "cubic_shape_determinant_proved": theorem_proved,
            "all_nine_stable_shape_characteristic_polynomials_proved": theorem_proved,
            "all_six_normalized_gaps_proved": False,
            "all_six_coherent_label_circuits_proved": False,
            "complete_racah_associator_proved": False,
            "hidden_involution_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "All stable-shape spectra are exact, but six normalized gap bounds, coherent label circuits, "
                "coupling-tree transitions, hidden-involution decoding, and classical separation remain unproved."
            ),
        },
        status=(
            "all-nine-stable-shape-polynomials-exact-six-gap-and-circuit-proofs-open"
            if theorem_proved
            else "stable-shape-cubic-determinant-certificate-failed"
        ),
        summary=(
            "Proved the final multiplicity-three determinant by 129 exact relative orbit classes, completing all "
            "nine stable-shape characteristic polynomials; gap, circuit, transition, and decoder proofs remain."
            if theorem_proved
            else "The cubic determinant failed an orbit, endpoint, sparse-reference, or Newton check."
        ),
        falsifiers_triggered=[
            "Exact characteristic polynomials do not imply inverse-polynomial normalized root gaps.",
            "Exact spectral formulas do not compile the common orbit Hamiltonian coherently.",
            "Shape-wise eigenlabels do not implement the left/right associator transition.",
            "No hidden-involution information or classical separation follows from spectral completeness alone.",
        ],
    )


def write_stable_shape_cubic_determinant_certificate(
    output_path: Path = COSET_STABLE_SHAPE_CUBIC_DETERMINANT_PATH,
    workers: int | None = None,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(
        build_stable_shape_cubic_determinant_certificate(workers=workers)
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-EXACT-NINE-SHAPE-SPECTRA-AS-SHOR-LEVEL-ALGORITHM",
                source=str(output_path),
                claim=(
                    "Exact characteristic polynomials for all nine stable shapes constitute a major quantum algorithm."
                ),
                reason_invalid=(
                    "Normalized gaps, coherent label/transition circuits, a hidden-involution decoder, sample "
                    "complexity, and classical separation are all independent unresolved obligations."
                ),
                lesson=(
                    "Proceed next to exact normalized root separation and common-orbit LCU compilation, then test "
                    "whether complete label outcomes carry reduction-compatible information."
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
                    "coset_stable_shape_cubic_determinant_certificate": str(
                        output_path
                    )
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_stable_shape_cubic_determinant_certificate()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
