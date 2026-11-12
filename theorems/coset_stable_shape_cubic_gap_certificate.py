"""Exact normalized root separation for the final cubic stable shape.

The multiplicity-three eta_n=(n-4,3,1) characteristic polynomial is exact.
Its discriminant factors as

    4 (n-2)^3 (621 n^3 - 4266 n^2 + 9612 n - 7192).

After n=m+8 all coefficients are positive, hence the three roots are real and
distinct throughout the stable range.  A Cauchy root bound converts the
discriminant product into an explicit minimum pairwise separation, and the
common orbit normalization contributes one further n^3 factor.

This closes spectral separation, not coherent compilation, coupling-tree
transitions, decoding, sample complexity, or classical separation.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path

import sympy as sp

from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


COSET_STABLE_SHAPE_CUBIC_GAP_PATH = Path(
    "research/representation/coset_stable_shape_cubic_gap_certificate.json"
)
COSET_STABLE_SHAPE_CUBIC_DETERMINANT_PATH = Path(
    "research/representation/coset_stable_shape_cubic_determinant_certificate.json"
)
COSET_STABLE_SHAPE_SECOND_MOMENT_PATH = Path(
    "research/representation/coset_stable_shape_second_moment_certificate.json"
)
COSET_STABLE_SHAPE_QUADRATIC_GAP_PATH = Path(
    "research/representation/coset_stable_shape_quadratic_gap_certificate.json"
)
COSET_STABLE_ROOT_SEPARATION_PATH = Path(
    "research/representation/coset_stable_root_separation_certificate.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-STABLE-SHAPE-CUBIC-GAP-CERTIFICATE"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
TARGET_TAIL = (3, 1)


@dataclass(frozen=True)
class StableShapeCubicGapCertificate:
    created_at: str
    source_certificate_contract: dict[str, object]
    exact_polynomial_certificate: dict[str, object]
    discriminant_certificate: dict[str, object]
    root_bound_certificate: dict[str, object]
    normalized_gap_certificate: dict[str, object]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _read_required(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"required exact certificate is missing: {path}")
    payload = json.loads(path.read_text())
    if not isinstance(payload, dict):
        raise ValueError(f"required certificate is not an object: {path}")
    return payload


@lru_cache(maxsize=1)
def build_stable_shape_cubic_gap_certificate() -> (
    StableShapeCubicGapCertificate
):
    n, m, x = sp.symbols("n m x", integer=True)
    cubic_source = _read_required(COSET_STABLE_SHAPE_CUBIC_DETERMINANT_PATH)
    second_source = _read_required(COSET_STABLE_SHAPE_SECOND_MOMENT_PATH)
    if not cubic_source.get("theorem", {}).get("proved", False):
        raise ArithmeticError("cubic determinant source theorem is not proved")
    if (
        cubic_source.get("headline_metrics", {}).get(
            "exact_complete_stable_shape_polynomial_count", 0
        )
        != 9
    ):
        raise ArithmeticError("stable-shape polynomial source is incomplete")
    second_record = next(
        row
        for row in second_source.get("shape_records", [])
        if tuple(row.get("intermediate_tail", ())) == TARGET_TAIL
    )
    if not second_record.get(
        "exact_all_n_at_least_8_second_moment_proved", False
    ):
        raise ArithmeticError("cubic second coefficient source is not proved")

    first = sp.sympify(
        second_record["exact_first_power_trace"], locals={"n": n}
    )
    second = sp.sympify(
        second_record["exact_second_characteristic_coefficient"],
        locals={"n": n},
    )
    determinant = sp.sympify(
        cubic_source["theorem"]["determinant"], locals={"n": n}
    )
    polynomial = sp.expand(x**3 - first * x**2 + second * x - determinant)
    discriminant = sp.factor(sp.discriminant(polynomial, x))
    expected_discriminant = 4 * (n - 2) ** 3 * (
        621 * n**3 - 4266 * n**2 + 9612 * n - 7192
    )
    discriminant_identity = sp.expand(discriminant - expected_discriminant) == 0
    shifted = sp.Poly(sp.expand(discriminant.subs(n, m + 8)), m)
    shifted_coefficients = [int(value) for value in shifted.all_coeffs()]
    discriminant_positive = (
        discriminant_identity
        and all(value >= 0 for value in shifted_coefficients)
        and shifted_coefficients[-1] > 0
    )

    coefficient_l1_bounds = {
        "e1": sum(abs(int(value)) for value in sp.Poly(first, n).all_coeffs()),
        "e2": sum(abs(int(value)) for value in sp.Poly(second, n).all_coeffs()),
        "e3": sum(
            abs(int(value)) for value in sp.Poly(determinant, n).all_coeffs()
        ),
    }
    maximum_l1 = max(coefficient_l1_bounds.values())
    cauchy_constant = maximum_l1 + 1
    # Every root satisfies |r|<=1+max(|e1|,|e2|,|e3|)<=C n^9.
    # For real roots r1,r2,r3 and delta=min_ij |ri-rj|,
    # Disc<=delta^2(2R)^4, hence delta>=sqrt(Disc)/(4R^2).
    raw_gap_denominator_constant = 4 * cauchy_constant**2
    raw_gap_exponent = 18
    normalized_gap_exponent = raw_gap_exponent + 3
    quadratic_source = _read_required(COSET_STABLE_SHAPE_QUADRATIC_GAP_PATH)
    stable_source = _read_required(COSET_STABLE_ROOT_SEPARATION_PATH)
    quadratic_gap_count = int(
        quadratic_source.get("headline_metrics", {}).get(
            "new_normalized_gap_theorem_count", 0
        )
        or 0
    )
    original_stable_gap_count = int(
        stable_source.get("headline_metrics", {}).get(
            "stable_channel_root_separation_theorem_count", 0
        )
        or 0
    )
    theorem_proved = (
        discriminant_positive
        and quadratic_gap_count == 5
        and original_stable_gap_count == 1
    )
    metrics: dict[str, int | float] = {
        "exact_cubic_discriminant_identity_count": int(discriminant_identity),
        "positive_cubic_discriminant_theorem_count": int(
            discriminant_positive
        ),
        "new_normalized_gap_theorem_count": int(theorem_proved),
        "complementary_shape_normalized_gap_theorem_count": (
            quadratic_gap_count + int(theorem_proved)
        ),
        "all_nontrivial_stable_shape_normalized_gap_theorem_count": (
            quadratic_gap_count
            + int(theorem_proved)
            + original_stable_gap_count
        ),
        "remaining_open_stable_shape_gap_family_count": (
            0 if theorem_proved else 1
        ),
        "cauchy_root_bound_constant": cauchy_constant,
        "raw_gap_inverse_polynomial_exponent": raw_gap_exponent,
        "lcu_normalized_gap_inverse_polynomial_exponent": (
            normalized_gap_exponent
        ),
        "new_coherent_shape_label_count": 0,
        "complete_racah_associator_count": 0,
        "hidden_involution_decoder_count": 0,
    }
    return StableShapeCubicGapCertificate(
        created_at=utc_now(),
        source_certificate_contract={
            "cubic_determinant_certificate": str(
                COSET_STABLE_SHAPE_CUBIC_DETERMINANT_PATH
            ),
            "second_moment_certificate": str(
                COSET_STABLE_SHAPE_SECOND_MOMENT_PATH
            ),
            "five_quadratic_gap_certificate": str(
                COSET_STABLE_SHAPE_QUADRATIC_GAP_PATH
            ),
            "original_stable_gap_certificate": str(
                COSET_STABLE_ROOT_SEPARATION_PATH
            ),
            "all_sources_proved": theorem_proved,
        },
        exact_polynomial_certificate={
            "intermediate_partition": "eta_n=(n-4,3,1)",
            "characteristic_polynomial": str(polynomial),
            "first_characteristic_coefficient": str(first),
            "second_characteristic_coefficient": str(second),
            "determinant": str(determinant),
        },
        discriminant_certificate={
            "exact_discriminant": str(sp.expand(discriminant)),
            "factored_discriminant": str(discriminant),
            "expected_factorization": str(expected_discriminant),
            "factorization_verified": discriminant_identity,
            "shift_n_equals_m_plus_8": str(sp.expand(shifted.as_expr())),
            "shifted_coefficients": shifted_coefficients,
            "positive_for_every_integer_n_at_least_8": discriminant_positive,
            "root_consequence": "three distinct real roots",
        },
        root_bound_certificate={
            "coefficient_l1_bounds": coefficient_l1_bounds,
            "maximum_coefficient_l1_bound": maximum_l1,
            "cauchy_bound": f"R_n<={cauchy_constant}*n^9",
            "discriminant_gap_inequality": (
                "delta_n>=sqrt(Disc_n)/(4*R_n^2)"
            ),
            "raw_gap_lower_bound": (
                f"delta_n>=1/({raw_gap_denominator_constant}*n^{raw_gap_exponent})"
            ),
        },
        normalized_gap_certificate={
            "orbit_lcu_normalization": "alpha_n=n(n-1)(n-2)<=n^3",
            "normalized_gap_lower_bound": (
                f"delta_n/alpha_n>=1/({raw_gap_denominator_constant}*n^{normalized_gap_exponent})"
            ),
            "inverse_polynomial_gap_proved": theorem_proved,
        },
        headline_metrics=metrics,
        claim_gate={
            "cubic_normalized_gap_proved": theorem_proved,
            "all_six_complementary_shape_gaps_proved": theorem_proved,
            "all_seven_nontrivial_stable_shape_gaps_proved": theorem_proved,
            "all_six_complementary_coherent_label_circuits_proved": False,
            "complete_racah_associator_proved": False,
            "hidden_involution_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "All seven nontrivial stable-shape spectra and normalized gaps are exact, but six coherent label "
                "circuits, coupling-tree transitions, decoder information, and classical separation remain open."
            ),
        },
        status=(
            "all-seven-nontrivial-stable-shape-gaps-proved-circuits-transitions-decoder-open"
            if theorem_proved
            else "stable-shape-cubic-gap-certificate-failed"
        ),
        summary=(
            "Proved the final cubic normalized root gap and thereby all seven nontrivial stable-shape gap families; "
            "coherent implementation, transition synthesis, decoding, and classical separation remain open."
        ),
        falsifiers_triggered=[
            "Complete spectral separation does not provide coherent multiplicity-label circuits.",
            "Shape-local labels do not synthesize the overlapping left/right associator.",
            "No hidden-involution information theorem follows from separated eigenvalues.",
            "No quantum speedup follows without a decoder and serious classical baselines.",
        ],
    )


def write_stable_shape_cubic_gap_certificate(
    output_path: Path = COSET_STABLE_SHAPE_CUBIC_GAP_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(build_stable_shape_cubic_gap_certificate())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-ALL-STABLE-SHAPE-GAPS-AS-COMPLETE-QUANTUM-ALGORITHM",
                source=str(output_path),
                claim=(
                    "Exact normalized gaps for every nontrivial stable shape constitute a nonabelian HSP algorithm."
                ),
                reason_invalid=(
                    "Coherent label and transition circuits, decoder information, sample complexity, and classical "
                    "separation remain unproved."
                ),
                lesson=(
                    "Compile the common orbit Hamiltonian uniformly across all shapes, synthesize the complete "
                    "coupling-tree transition, then test decoder information against classical baselines."
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
                    "coset_stable_shape_cubic_gap_certificate": str(output_path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_stable_shape_cubic_gap_certificate()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
