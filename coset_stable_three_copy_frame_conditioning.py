"""All-n coercivity certificate for the stable three-copy involution frame.

For W_n=(n-2,2), final xi_n=(n-3,2,1), and an involution class with t
transpositions, the exact frame is

    F = a I + A_12 + A_13 + A_23,
    a = 1 + 3 r_W + r_xi.

Each pair operator A_ij has eigenvalues r_eta over the nine stable
intermediate shapes eta.  Weyl's inequality therefore gives

    lambda_min(F) >= min_eta (a + 3 r_eta).

This module substitutes exact stable character polynomials into every one of
those nine bounds.  For partial matchings t=floor(n/4) and dense matchings
t=floor(n/2), each residue class becomes a rational function of a shifted
nonnegative integer.  Nonnegative numerator and denominator coefficients,
with positive constants, prove positivity and an explicit inverse-polynomial
lower bound for every n>=8.

Conditioning plus the existing frame block encoding gives a polynomial QSVT
inverse-square-root filter.  It does not prove that filter outcomes identify
the hidden involution or beat classical representation-theoretic algorithms.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

import sympy as sp

from coset_stable_shape_family_certificate import (
    FINAL_TAIL,
    SOURCE_TAIL,
    STABLE_TAILS,
    X,
    reconstruct_character_polynomial,
)
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


COSET_STABLE_THREE_COPY_FRAME_CONDITIONING_PATH = Path(
    "research/representation/coset_stable_three_copy_frame_conditioning.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-STABLE-THREE-COPY-FRAME-CONDITIONING"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

N, T, M, U = sp.symbols("n t m u", integer=True, nonnegative=True)


@dataclass(frozen=True)
class CoercivityResidueRecord:
    family: str
    residue: int
    modulus: int
    n_formula: str
    transposition_formula: str
    minimum_n: int
    minimum_m: int
    intermediate_tail: tuple[int, ...]
    intermediate_partition: str
    character_polynomial_threshold: int
    exact_character_ratio: str
    exact_weyl_bound: str
    shifted_variable: str
    shifted_numerator: str
    shifted_denominator: str
    numerator_coefficients_low_to_high: tuple[str, ...]
    denominator_coefficients_low_to_high: tuple[str, ...]
    numerator_coefficients_nonnegative: bool
    denominator_coefficients_nonnegative: bool
    positive_constant_terms: bool
    lower_bound_constant: str
    lower_bound_exponent: int
    theorem_verified: bool


@dataclass(frozen=True)
class StableThreeCopyFrameConditioningReport:
    created_at: str
    operator_theorem: dict[str, object]
    character_ratio_contract: dict[str, object]
    positivity_method: dict[str, object]
    records: list[CoercivityResidueRecord]
    qsvt_filter_contract: dict[str, object]
    headline_metrics: dict[str, int | float | str]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _character_ratio_expression(tail: tuple[int, ...]) -> sp.Expr:
    polynomial, certificate = reconstruct_character_polynomial(tail)
    if int(certificate["threshold"]) > 8:
        raise ArithmeticError("stable character polynomial starts above n=8")
    involution_character = polynomial.subs(
        {X[0]: N - 2 * T, X[1]: T, X[2]: 0, X[3]: 0}
    )
    dimension = polynomial.subs({X[0]: N, X[1]: 0, X[2]: 0, X[3]: 0})
    return sp.factor(sp.cancel(involution_character / dimension))


@lru_cache(maxsize=1)
def exact_weyl_bounds() -> dict[tuple[int, ...], sp.Expr]:
    source_ratio = _character_ratio_expression(SOURCE_TAIL)
    final_ratio = _character_ratio_expression(FINAL_TAIL)
    identity_scalar = 1 + 3 * source_ratio + final_ratio
    return {
        tail: sp.factor(
            sp.cancel(identity_scalar + 3 * _character_ratio_expression(tail))
        )
        for tail in STABLE_TAILS
    }


def _coefficient_strings(polynomial: sp.Poly) -> tuple[str, ...]:
    return tuple(str(polynomial.nth(index)) for index in range(polynomial.degree() + 1))


def _positive_shifted_fraction(
    expression: sp.Expr,
    modulus: int,
    residue: int,
    minimum_m: int,
) -> tuple[sp.Poly, sp.Poly, sp.Expr]:
    residue_expression = sp.cancel(
        expression.subs({N: modulus * M + residue, T: M})
    )
    shifted = sp.cancel(residue_expression.subs(M, U + minimum_m))
    numerator, denominator = sp.fraction(shifted)
    numerator_poly = sp.Poly(numerator, U, domain=sp.QQ)
    denominator_poly = sp.Poly(denominator, U, domain=sp.QQ)
    if denominator_poly.eval(0) < 0:
        numerator_poly = -numerator_poly
        denominator_poly = -denominator_poly
    return numerator_poly, denominator_poly, residue_expression


def _record(
    family: str,
    modulus: int,
    residue: int,
    minimum_m: int,
    tail: tuple[int, ...],
    expression: sp.Expr,
) -> CoercivityResidueRecord:
    numerator, denominator, residue_expression = _positive_shifted_fraction(
        expression,
        modulus,
        residue,
        minimum_m,
    )
    numerator_coefficients = tuple(numerator.nth(index) for index in range(numerator.degree() + 1))
    denominator_coefficients = tuple(
        denominator.nth(index) for index in range(denominator.degree() + 1)
    )
    numerator_nonnegative = all(bool(value >= 0) for value in numerator_coefficients)
    denominator_nonnegative = all(
        bool(value >= 0) for value in denominator_coefficients
    )
    constants_positive = bool(
        numerator_coefficients[0] > 0 and denominator_coefficients[0] > 0
    )
    denominator_coefficient_sum = sum(denominator_coefficients)
    lower_bound_constant = sp.cancel(
        numerator_coefficients[0] / denominator_coefficient_sum
    )
    polynomial, certificate = reconstruct_character_polynomial(tail)
    _ = polynomial
    minimum_n = modulus * minimum_m + residue
    tail_size = sum(tail)
    return CoercivityResidueRecord(
        family=family,
        residue=residue,
        modulus=modulus,
        n_formula=f"n={modulus}*m+{residue}",
        transposition_formula="t=m",
        minimum_n=minimum_n,
        minimum_m=minimum_m,
        intermediate_tail=tail,
        intermediate_partition=f"(n-{tail_size},{','.join(map(str, tail))})",
        character_polynomial_threshold=int(certificate["threshold"]),
        exact_character_ratio=str(_character_ratio_expression(tail)),
        exact_weyl_bound=str(expression),
        shifted_variable=f"u=m-{minimum_m}>=0",
        shifted_numerator=str(sp.factor(numerator.as_expr())),
        shifted_denominator=str(sp.factor(denominator.as_expr())),
        numerator_coefficients_low_to_high=_coefficient_strings(numerator),
        denominator_coefficients_low_to_high=_coefficient_strings(denominator),
        numerator_coefficients_nonnegative=numerator_nonnegative,
        denominator_coefficients_nonnegative=denominator_nonnegative,
        positive_constant_terms=constants_positive,
        lower_bound_constant=str(lower_bound_constant),
        lower_bound_exponent=denominator.degree(),
        theorem_verified=(
            numerator_nonnegative and denominator_nonnegative and constants_positive
        ),
    )


@lru_cache(maxsize=1)
def build_stable_three_copy_frame_conditioning_report(
) -> StableThreeCopyFrameConditioningReport:
    bounds = exact_weyl_bounds()
    records: list[CoercivityResidueRecord] = []
    family_specs = (
        ("partial_matching_t_floor_n_over_4", 4, range(4), 2),
        ("dense_matching_t_floor_n_over_2", 2, range(2), 4),
    )
    for family, modulus, residues, minimum_m in family_specs:
        for residue in residues:
            for tail in STABLE_TAILS:
                records.append(
                    _record(
                        family,
                        modulus,
                        residue,
                        minimum_m,
                        tail,
                        bounds[tail],
                    )
                )
    if not all(record.theorem_verified for record in records):
        raise ArithmeticError("a stable frame residue-class positivity proof failed")

    constants = [Fraction(record.lower_bound_constant) for record in records]
    global_constant = min(constants)
    global_exponent = max(record.lower_bound_exponent for record in records)
    family_count = len({record.family for record in records})
    residue_count = len({(record.family, record.residue) for record in records})
    metrics: dict[str, int | float | str] = {
        "stable_intermediate_shape_count": len(STABLE_TAILS),
        "involution_family_count": family_count,
        "residue_class_count": residue_count,
        "exact_character_ratio_count": len(STABLE_TAILS),
        "coercivity_residue_certificate_count": len(records),
        "verified_coercivity_residue_certificate_count": sum(
            record.theorem_verified for record in records
        ),
        "all_n_inverse_polynomial_minimum_eigenvalue_theorem_count": family_count,
        "global_minimum_eigenvalue_lower_bound_constant": str(global_constant),
        "global_minimum_eigenvalue_lower_bound_exponent": global_exponent,
        "polynomial_inverse_square_root_filter_count": family_count,
        "hidden_involution_decoder_count": 0,
    }
    return StableThreeCopyFrameConditioningReport(
        created_at=utc_now(),
        operator_theorem={
            "frame": "F=(1+3*r_W+r_xi)I+A_12+A_13+A_23",
            "pair_spectrum": "spectrum(A_ij)={r_eta: eta in the nine stable intermediate shapes}",
            "weyl_bound": "lambda_min(F)>=min_eta(1+3*r_W+r_xi+3*r_eta)",
            "all_n_range": "every integer n>=8",
            "conditioned_branch": "W_n^tensor3 with final xi_n=(n-3,2,1)",
        },
        character_ratio_contract={
            "involution_cycle_counts": "X1=n-2t, X2=t, Xj=0 for j>=3",
            "ratio": "r_eta=character_polynomial_eta(n-2t,t,0,...)/dimension_eta(n)",
            "stable_tail_count": len(STABLE_TAILS),
            "maximum_character_polynomial_threshold": max(
                record.character_polynomial_threshold for record in records
            ),
            "exact_from_n": 8,
        },
        positivity_method={
            "partial_matching_substitution": "n=4m+s, t=m, s in {0,1,2,3}, m>=2",
            "dense_matching_substitution": "n=2m+s, t=m, s in {0,1}, m>=4",
            "shift": "u=m-m_min>=0",
            "certificate": (
                "Every shifted numerator and denominator has nonnegative rational coefficients and a positive "
                "constant. If denominator degree is d and coefficient sum is D, then B_eta>=c/(D*(u+1)^d)>=c/(D*n^d)."
            ),
            "global_bound": f"lambda_min(F)>={global_constant}/n^{global_exponent}",
            "operator_norm_bound": "norm(F)<=abs(1+3*r_W+r_xi)+3<=8",
        },
        records=records,
        qsvt_filter_contract={
            "input": "existing polynomial block encoding of F on the stable branch",
            "spectral_interval": f"[{global_constant}/n^{global_exponent},8]",
            "transform": "uniform polynomial approximation to x^(-1/2) on the certified positive interval",
            "complexity": "poly(n,log(1/epsilon)) controlled block-encoding uses and gates",
            "family_selector": "known n and involution class parameter t",
            "dense_racah_table_required": False,
            "outcome_decoder_supplied": False,
        },
        headline_metrics=metrics,
        claim_gate={
            "all_n_inverse_polynomial_minimum_eigenvalue_proved": True,
            "partial_matching_conditioning_proved": True,
            "dense_matching_conditioning_proved": True,
            "polynomial_inverse_square_root_filter_proved": True,
            "hidden_involution_decoder_proved": False,
            "classical_superpolynomial_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The stable frame can now be inverted in polynomial time on two reduction-relevant involution "
                "families, but no theorem shows that the resulting measurement outcome identifies the hidden "
                "involution or resists classical character/tensor contraction."
            ),
        },
        status="stable-three-copy-frame-conditioned-and-filterable-decoder-open",
        summary=(
            f"Proved {len(records)} exact residue/shape coercivity bounds, giving lambda_min(F)>="
            f"{global_constant}/n^{global_exponent} and polynomial inverse-square-root filters for partial and dense "
            "matching classes; hidden-involution information and decoding remain open."
        ),
        falsifiers_triggered=[
            "The finite n=8 conditioning pattern was not a numerical accident: exact character-ratio coercivity proves all-n conditioning.",
            "No growing Racah matrix is needed for the conditioning proof or inverse filter.",
            "Conditioning and QSVT implementability alone do not imply useful hidden-involution information.",
            "The theorem covers one conditioned stable branch and two involution families, not the full coset-state ensemble.",
        ],
    )


def write_stable_three_copy_frame_conditioning_report(
    output_path: Path = COSET_STABLE_THREE_COPY_FRAME_CONDITIONING_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(build_stable_three_copy_frame_conditioning_report())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-STABLE-THREE-COPY-CONDITIONING-AS-HIDDEN-INVOLUTION-DECODER",
                source=str(output_path),
                claim=(
                    "An all-n conditioned stable frame and polynomial inverse-square-root filter constitute a hidden-involution decoder."
                ),
                reason_invalid=(
                    "The filter is only an implementable measurement primitive on one conditioned branch; no outcome-information, "
                    "reconstruction, branch-probability, or classical-separation theorem follows."
                ),
                lesson=(
                    "Compute the parameter-dependent PGM outcome law, prove mutual-information or reconstruction guarantees, "
                    "and attack it with classical character and bounded-treewidth tensor contractions."
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
                    "coset_stable_three_copy_frame_conditioning": str(output_path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_stable_three_copy_frame_conditioning_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
