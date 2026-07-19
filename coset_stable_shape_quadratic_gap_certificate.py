"""Exact normalized root gaps for the five complementary quadratic shapes.

Five nontrivial stable intermediate shapes have second-stage multiplicity two.
Their exact characteristic polynomials are known from the shape trace and
second-moment certificates.  For x^2-e1*x+e2 the raw eigenvalue gap is
sqrt(e1^2-4e2).  This module factors every discriminant, proves positivity for
all integer n>=8 by nonnegative shifted coefficients, and divides by the exact
orbit-LCU normalization alpha=n(n-1)(n-2).

The result supplies inverse-polynomial normalized gaps, not coherent circuits,
coupling-tree transitions, hidden-involution decoding, or quantum advantage.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path

import sympy as sp

from coset_stable_shape_second_moment_certificate import (
    build_stable_shape_second_moment_certificate,
)
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


COSET_STABLE_SHAPE_QUADRATIC_GAP_PATH = Path(
    "research/representation/coset_stable_shape_quadratic_gap_certificate.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-STABLE-SHAPE-QUADRATIC-GAP-CERTIFICATE"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
QUADRATIC_TAILS = ((2,), (1, 1), (3,), (1, 1, 1), (2, 2))


@dataclass(frozen=True)
class QuadraticShapeGapRecord:
    intermediate_tail: tuple[int, ...]
    intermediate_partition: str
    exact_characteristic_polynomial: str
    exact_discriminant: str
    factored_discriminant: str
    shifted_discriminant_at_n_equals_m_plus_8: str
    shifted_coefficient_count: int
    minimum_shifted_coefficient: int
    exact_discriminant_at_n8: int
    conservative_raw_gap_lower_bound: int
    lcu_normalization: str
    normalized_gap_lower_bound: str
    discriminant_positive_for_every_integer_n_at_least_8: bool
    inverse_polynomial_normalized_gap_proved: bool
    coherent_label_circuit_proved: bool
    status: str


@dataclass(frozen=True)
class StableShapeQuadraticGapCertificate:
    created_at: str
    theorem: dict[str, object]
    method_contract: dict[str, object]
    shape_records: list[QuadraticShapeGapRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _partition_formula(tail: tuple[int, ...]) -> str:
    return f"(n-{sum(tail)},{','.join(str(value) for value in tail)})"


@lru_cache(maxsize=1)
def build_stable_shape_quadratic_gap_certificate() -> (
    StableShapeQuadraticGapCertificate
):
    n, m, x = sp.symbols("n m x", integer=True)
    second_moments = build_stable_shape_second_moment_certificate()
    by_tail = {
        record.intermediate_tail: record
        for record in second_moments.shape_records
    }
    records: list[QuadraticShapeGapRecord] = []
    for tail in QUADRATIC_TAILS:
        source = by_tail[tail]
        if source.second_stage_multiplicity != 2:
            raise ArithmeticError("declared quadratic shape is not multiplicity two")
        first_trace = sp.sympify(source.exact_first_power_trace, locals={"n": n})
        determinant = sp.sympify(
            source.exact_second_characteristic_coefficient,
            locals={"n": n},
        )
        polynomial = sp.expand(x**2 - first_trace * x + determinant)
        discriminant = sp.expand(first_trace**2 - 4 * determinant)
        shifted = sp.Poly(sp.expand(discriminant.subs(n, m + 8)), m)
        coefficients = [int(value) for value in shifted.all_coeffs()]
        positivity = all(value >= 0 for value in coefficients) and any(
            value > 0 for value in coefficients
        )
        value_at_8 = int(discriminant.subs(n, 8))
        raw_lower = int(sp.floor(sp.sqrt(value_at_8)))
        if raw_lower**2 > value_at_8:
            raw_lower -= 1
        if not positivity or raw_lower <= 0:
            raise ArithmeticError("quadratic discriminant positivity proof failed")
        records.append(
            QuadraticShapeGapRecord(
                intermediate_tail=tail,
                intermediate_partition=_partition_formula(tail),
                exact_characteristic_polynomial=str(polynomial),
                exact_discriminant=str(discriminant),
                factored_discriminant=str(sp.factor(discriminant)),
                shifted_discriminant_at_n_equals_m_plus_8=str(
                    sp.expand(shifted.as_expr())
                ),
                shifted_coefficient_count=len(coefficients),
                minimum_shifted_coefficient=min(coefficients),
                exact_discriminant_at_n8=value_at_8,
                conservative_raw_gap_lower_bound=raw_lower,
                lcu_normalization="alpha_n=n(n-1)(n-2)",
                normalized_gap_lower_bound=f"{raw_lower}/n^3",
                discriminant_positive_for_every_integer_n_at_least_8=positivity,
                inverse_polynomial_normalized_gap_proved=True,
                coherent_label_circuit_proved=False,
                status="exact-quadratic-normalized-gap-proved-circuit-open",
            )
        )

    minimum_raw_lower = min(
        record.conservative_raw_gap_lower_bound for record in records
    )
    theorem_proved = len(records) == 5 and all(
        record.inverse_polynomial_normalized_gap_proved for record in records
    )
    metrics: dict[str, int | float] = {
        "quadratic_shape_count": len(records),
        "positive_discriminant_theorem_count": sum(
            record.discriminant_positive_for_every_integer_n_at_least_8
            for record in records
        ),
        "new_normalized_gap_theorem_count": sum(
            record.inverse_polynomial_normalized_gap_proved for record in records
        ),
        "minimum_uniform_raw_gap_lower_bound": minimum_raw_lower,
        "uniform_inverse_polynomial_gap_exponent": 3,
        "remaining_open_stable_shape_gap_family_count": 1,
        "new_coherent_shape_label_count": 0,
        "complete_racah_associator_count": 0,
        "hidden_involution_decoder_count": 0,
    }
    return StableShapeQuadraticGapCertificate(
        created_at=utc_now(),
        theorem={
            "range": "every integer n>=8",
            "statement": (
                "Each of the five complementary multiplicity-two shape Hamiltonians has positive discriminant "
                "and LCU-normalized eigenvalue gap at least 12/n^3."
            ),
            "proved": theorem_proved and minimum_raw_lower >= 12,
        },
        method_contract={
            "raw_gap_identity": "gap=sqrt(e1^2-4e2)",
            "positivity_method": (
                "substitute n=m+8 and verify every discriminant coefficient is nonnegative with positive constant term"
            ),
            "lcu_normalization": "n(n-1)(n-2)<=n^3",
            "uniform_bound": "gap_normalized>=12/n^3",
            "interpolation_used": False,
            "floating_arithmetic_used": False,
        },
        shape_records=records,
        headline_metrics=metrics,
        claim_gate={
            "all_five_quadratic_normalized_gaps_proved": theorem_proved,
            "multiplicity_three_normalized_gap_proved": False,
            "all_six_complementary_shape_gaps_proved": False,
            "all_six_coherent_label_circuits_proved": False,
            "complete_racah_associator_proved": False,
            "hidden_involution_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Five normalized quadratic gaps are exact, but the cubic root gap, coherent implementations, "
                "coupling-tree transitions, decoder, and classical separation remain unproved."
            ),
        },
        status=(
            "five-quadratic-normalized-gaps-proved-one-cubic-gap-open"
            if theorem_proved and minimum_raw_lower >= 12
            else "stable-shape-quadratic-gap-certificate-failed"
        ),
        summary=(
            "Factored and proved positivity of all five complementary quadratic discriminants, giving uniform "
            "LCU-normalized gaps at least 12/n^3; the lone cubic gap and all circuit/decoder obligations remain."
        ),
        falsifiers_triggered=[
            "Five quadratic gap theorems do not prove separation of the multiplicity-three roots.",
            "A normalized spectral gap does not by itself compile a coherent phase-estimation circuit.",
            "Shape-wise phase estimation does not implement coupling-tree transitions.",
            "No decoder or classical separation follows from root gaps alone.",
        ],
    )


def write_stable_shape_quadratic_gap_certificate(
    output_path: Path = COSET_STABLE_SHAPE_QUADRATIC_GAP_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(build_stable_shape_quadratic_gap_certificate())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-FIVE-GAPPED-QUADRATIC-SHAPES-AS-COMPLETE-ASSOCIATOR",
                source=str(output_path),
                claim=(
                    "Five exact complementary normalized gaps complete the stable Racah associator."
                ),
                reason_invalid=(
                    "The cubic gap, coherent label circuits, left/right transition synthesis, hidden-involution "
                    "decoder, and classical separation remain unproved."
                ),
                lesson=(
                    "Close the cubic discriminant/root separation next, then prove common-orbit block encoding and "
                    "complete transition behavior before decoder experiments."
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
                    "coset_stable_shape_quadratic_gap_certificate": str(
                        output_path
                    )
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_stable_shape_quadratic_gap_certificate()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
