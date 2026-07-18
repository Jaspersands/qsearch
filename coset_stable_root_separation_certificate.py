"""Exact root-separation theorem for the stable multiplicity-four Racah block.

The complete quartic from the fourth-moment certificate has discriminant

    (n-2)^2 q(n),

where q(n) has degree 18.  After n=m+7, every coefficient of q is positive;
more strongly, every coefficient of 1000*q(n)-n^18 is positive.  Hence the
discriminant is at least n^20/1960 for n>=7.

All four roots are real because the polynomial is the characteristic
polynomial of a Hermitian orbit Hamiltonian.  A Cauchy root bound and the
integer discriminant identity then give a raw minimum gap Omega(n^-50).  After
normalizing the n(n-1)(n-2)-term LCU, the gap is Omega(n^-53).  This proves a
spectral condition in one stable channel only; it does not implement the
Racah transform or decode a hidden involution.
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


COSET_STABLE_ROOT_SEPARATION_PATH = Path(
    "research/representation/coset_stable_root_separation_certificate.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-STABLE-ROOT-SEPARATION-CERTIFICATE"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

COEFFICIENT_NORM_BOUND = 38_014_592
CAUCHY_CONSTANT = COEFFICIENT_NORM_BOUND + 1
RAW_GAP_EXPONENT = 50
NORMALIZED_GAP_EXPONENT = 53


@dataclass(frozen=True)
class StableRootSeparationCertificate:
    created_at: str
    theorem: dict[str, object]
    quartic_certificate: dict[str, object]
    discriminant_certificate: dict[str, object]
    root_bound_certificate: dict[str, object]
    lcu_normalization_certificate: dict[str, object]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def stable_quartic(n: sp.Symbol, x: sp.Symbol) -> sp.Expr:
    first = 4 * n**3 - 46 * n**2 + 149 * n - 118
    second = (
        6 * n**6
        - 138 * n**5
        + 1240 * n**4
        - 5487 * n**3
        + 12351 * n**2
        - 13086 * n
        + 5150
    )
    third = (
        4 * n**9
        - 138 * n**8
        + 2033 * n**7
        - 16692 * n**6
        + 83608 * n**5
        - 262838 * n**4
        + 514175 * n**3
        - 599392 * n**2
        + 377636 * n
        - 98432
    )
    determinant = (
        n**12
        - 46 * n**11
        + 942 * n**10
        - 11323 * n**9
        + 88681 * n**8
        - 474944 * n**7
        + 1776057 * n**6
        - 4651896 * n**5
        + 8434537 * n**4
        - 10291787 * n**3
        + 8012686 * n**2
        - 3577300 * n
        + 694392
    )
    return x**4 - first * x**3 + second * x**2 - third * x + determinant


@lru_cache(maxsize=1)
def build_stable_root_separation_certificate() -> StableRootSeparationCertificate:
    n, x, m = sp.symbols("n x m", integer=True)
    quartic = stable_quartic(n, x)
    discriminant = sp.factor(sp.discriminant(quartic, x))
    quotient = sp.factor(discriminant / (n - 2) ** 2)
    quotient_polynomial = sp.Poly(quotient, n)
    shifted_quotient = sp.Poly(sp.expand(quotient.subs(n, m + 7)), m)
    scaled_margin = sp.Poly(
        sp.expand((1000 * quotient - n**18).subs(n, m + 7)), m
    )
    shifted_positive = all(coefficient > 0 for coefficient in shifted_quotient.all_coeffs())
    scaled_margin_positive = all(
        coefficient > 0 for coefficient in scaled_margin.all_coeffs()
    )
    coefficient_norms = [
        sum(abs(int(coefficient)) for coefficient in sp.Poly(term, n).all_coeffs())
        for term in (
            -quartic.coeff(x, 3),
            quartic.coeff(x, 2),
            -quartic.coeff(x, 1),
            quartic.coeff(x, 0),
        )
    ]
    coefficient_bound_verified = max(coefficient_norms) == COEFFICIENT_NORM_BOUND
    discriminant_identity_verified = (
        sp.simplify(discriminant - (n - 2) ** 2 * quotient) == 0
        and quotient_polynomial.degree() == 18
    )
    theorem_proved = (
        discriminant_identity_verified
        and shifted_positive
        and scaled_margin_positive
        and coefficient_bound_verified
    )
    gap_constant_denominator = 45 * (2 * CAUCHY_CONSTANT) ** 5
    metrics: dict[str, int | float] = {
        "all_n_quartic_theorem_count": 1,
        "all_n_root_separation_theorem_count": int(theorem_proved),
        "stable_channel_root_separation_theorem_count": int(theorem_proved),
        "discriminant_degree": int(sp.degree(discriminant, n)),
        "discriminant_quotient_degree": quotient_polynomial.degree(),
        "shifted_positive_coefficient_count": len(
            shifted_quotient.all_coeffs()
        ),
        "scaled_margin_positive_coefficient_count": len(
            scaled_margin.all_coeffs()
        ),
        "coefficient_norm_bound": COEFFICIENT_NORM_BOUND,
        "raw_gap_inverse_polynomial_exponent": RAW_GAP_EXPONENT,
        "normalized_gap_inverse_polynomial_exponent": NORMALIZED_GAP_EXPONENT,
        "gap_constant_denominator": gap_constant_denominator,
        "uniform_polynomial_racah_circuit_count": 0,
        "hidden_involution_decoder_count": 0,
        "all_sector_uniform_gap_theorem_count": 0,
    }
    return StableRootSeparationCertificate(
        created_at=utc_now(),
        theorem={
            "range": "every integer n>=7",
            "raw_gap_lower_bound": (
                f"1/({gap_constant_denominator}*n^{RAW_GAP_EXPONENT})"
            ),
            "lcu_normalized_gap_lower_bound": (
                f"1/({gap_constant_denominator}*n^{NORMALIZED_GAP_EXPONENT})"
            ),
            "statement": (
                "Every pair of eigenvalues in the stable multiplicity-four Racah block is separated by the displayed "
                "raw bound, and by the displayed bound after orbit-LCU normalization."
            ),
            "proved": theorem_proved,
        },
        quartic_certificate={
            "characteristic_polynomial": str(sp.expand(quartic)),
            "hermitian_source": (
                "the transposition/3-cycle orbit sum includes inverse 3-cycle pairs and is Hermitian"
            ),
            "all_roots_real": True,
            "coefficient_l1_norms": coefficient_norms,
            "maximum_coefficient_l1_norm": max(coefficient_norms),
            "coefficient_bound_verified": coefficient_bound_verified,
        },
        discriminant_certificate={
            "discriminant": str(discriminant),
            "factorization": f"(n - 2)^2*({quotient})",
            "quotient": str(quotient),
            "quotient_shift": "n=m+7",
            "shifted_quotient_coefficients": [
                int(coefficient) for coefficient in shifted_quotient.all_coeffs()
            ],
            "scaled_margin": "1000*q(n)-n^18",
            "scaled_margin_shifted_coefficients": [
                int(coefficient) for coefficient in scaled_margin.all_coeffs()
            ],
            "lower_bound": "Disc(p_n)>=n^20/1960 for n>=7",
            "identity_verified": discriminant_identity_verified,
            "positivity_verified": shifted_positive and scaled_margin_positive,
        },
        root_bound_certificate={
            "cauchy_bound": f"max_i |lambda_i|<={CAUCHY_CONSTANT}*n^12",
            "pair_gap_upper_bound": f"2*{CAUCHY_CONSTANT}*n^12",
            "discriminant_identity": (
                "sqrt(Disc(p_n))=product_{i<j}|lambda_i-lambda_j|"
            ),
            "minimum_gap_argument": (
                "Bound five of the six pair gaps above by twice the Cauchy radius and bound the discriminant below; "
                "the remaining minimum pair gap is at least n^-50 divided by the explicit constant."
            ),
            "raw_gap_exponent": RAW_GAP_EXPONENT,
            "constant_denominator": gap_constant_denominator,
        },
        lcu_normalization_certificate={
            "orbit_term_count": "n(n-1)(n-2)",
            "orbit_term_count_upper_bound": "n^3",
            "normalized_gap_exponent": NORMALIZED_GAP_EXPONENT,
            "normalization_applied": True,
        },
        headline_metrics=metrics,
        claim_gate={
            "complete_stable_quartic_proved": True,
            "stable_channel_root_separation_proved": theorem_proved,
            "all_decoder_relevant_sectors_covered": False,
            "uniform_polynomial_racah_circuit_proved": False,
            "hidden_involution_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "A polynomial spectral gap in one stable multiplicity channel does not implement the Racah transform, "
                "cover all sectors, or turn measurement outcomes into a hidden-involution decoder."
            ),
        },
        status=(
            "stable-root-separation-proved-circuit-decoder-open"
            if theorem_proved
            else "stable-root-separation-certificate-failed"
        ),
        summary=(
            "Proved an explicit inverse-polynomial LCU-normalized eigenvalue gap for the stable multiplicity-four "
            "Racah block; circuit synthesis, sector coverage, and decoding remain open."
            if theorem_proved
            else "The discriminant positivity or coefficient-bound certificate failed."
        ),
        falsifiers_triggered=[
            "A separated abstract spectrum does not provide a coherent circuit for the orbit Hamiltonian or its phase estimation.",
            "One stable multiplicity-four channel does not cover all intermediate and final sectors.",
            "No theorem maps these spectral labels to a hidden-involution decoder.",
            "No classical baseline is defeated by the spectral theorem alone.",
        ],
    )


def write_stable_root_separation_certificate(
    output_path: Path = COSET_STABLE_ROOT_SEPARATION_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(build_stable_root_separation_certificate())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-STABLE-ROOT-GAP-AS-END-TO-END-DECODER",
                source=str(output_path),
                claim=(
                    "An inverse-polynomial normalized gap in one stable Racah channel yields an efficient nonabelian HSP algorithm."
                ),
                reason_invalid=(
                    "Uniform coherent implementation, all-sector coverage, and a reduction-compatible hidden-involution decoder remain absent."
                ),
                lesson=(
                    "Compile the bounded-support hierarchy and phase estimation coherently, then quantify decoder information against classical baselines."
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
                    "coset_stable_root_separation_certificate": str(output_path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_stable_root_separation_certificate()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
