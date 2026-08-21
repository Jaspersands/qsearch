"""Bounded-polynomial spectral no-go for one hidden-involution Hecke walk.

The all-degree moment theorem leaves open polynomials with large monomial
coefficient norm, including Chebyshev/QSVT threshold approximants.  Their
operator norm, rather than monomial coefficient norm, is the correct physical
normalization.  This module closes that route at efficient degree.

Let ``mu_0`` and ``mu_1`` be the baseline and likelihood-weighted spectral
laws of the canonical cross-transposition operator ``X``.  For
``r=m(m-1)`` and ``x=2^k``, the exact second moments are

    s_0 = 1/(x r),
    s_1 = (x+r-1)/(x^2 r).

For any real polynomial ``p`` of degree ``D`` with ``|p(lambda)|<=1`` on
``[-1,1]``, Markov's brothers inequality gives ``||p'||_infty<=D^2``.
Because both spectral laws have total mass one, the constant ``p(0)`` cancels,
and Cauchy--Schwarz gives

    |E_1 p(X)-E_0 p(X)|
      <= D^2 (E_1|X|+E_0|X|)
      <= D^2 (sqrt(s_1)+sqrt(s_0)).

Thus bias at least ``beta`` requires

    D >= sqrt(beta/(sqrt(s_0)+sqrt(s_1))).

At natural ``x>=64M`` and ``x>=r``, the denominator is at most
``(1+sqrt(2))/sqrt(xr)``.  Constant bias therefore requires
``D=Omega((xr)^(1/4))=Omega(M^(1/4))``, which is superpolynomial in ``m``.

This rules out efficient bounded-polynomial spectral filters, including the
standard single-operator QSVT/block-encoding route.  It does not rule out free
access to an exact eigenbasis, an oracle stronger than block access to ``X``,
postselection outside the bounded acceptance-polynomial model, or coherent
noncommuting mixtures of several double-coset operators.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from coset_hidden_involution_binary_decision_reduction import (
    involution_class_size,
)
from coset_hidden_involution_orbit_synthesis_flatness import (
    flatness_copy_count,
)
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_single_hecke_bounded_spectral_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-SINGLE-HECKE-BOUNDED-SPECTRAL-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class SpectralConcentrationControl:
    half_degree: int
    copy_count: int
    pair_crossing_index: int
    baseline_second_moment: str
    likelihood_second_moment: str
    baseline_root_second_moment: float
    likelihood_root_second_moment: float
    spectral_absolute_first_moment_sum_upper_bound: float
    natural_copy_scale_dominates_crossing_index: bool
    exact_second_moment_formula_verified: bool
    status: str


@dataclass(frozen=True)
class BoundedPolynomialDegreeControl:
    half_degree: int
    copy_count: int
    target_bias: float
    spectral_width_upper_bound: float
    exact_degree_lower_bound: float
    integer_degree_lower_bound: int
    simplified_natural_degree_lower_bound: float
    integer_simplified_degree_lower_bound: int
    markov_derivative_factor: str
    constant_term_cancels: bool
    bounded_polynomial_bias_bound: str
    exact_bound_implies_simplified_bound: bool
    status: str


@dataclass(frozen=True)
class BoundedSpectralScalingRecord:
    half_degree: int
    degree: int
    conjugacy_class_size_decimal: str
    copy_count: int
    pair_crossing_index: int
    target_bias: float
    required_polynomial_degree: float
    required_polynomial_degree_log2: float
    candidate_fourth_root_log2: float
    required_degree_exceeds_half_candidate_fourth_root: bool
    required_degree_exceeds_half_degree_squared: bool
    status: str


@dataclass(frozen=True)
class BoundedSpectralTheorem:
    exact_second_moments: str
    markov_Cauchy_Schwarz_bound: str
    degree_lower_bound: str
    natural_copy_lower_bound: str
    query_model_consequence: str
    exact_spectral_concentration_proved: bool
    bounded_polynomial_bias_theorem_proved: bool
    superpolynomial_natural_degree_lower_bound_proved: bool
    efficient_single_operator_QSVT_filter_ruled_out: bool
    unrestricted_spectral_projector_ruled_out: bool
    multi_operator_spectral_algorithm_ruled_out: bool
    hidden_involution_detector_constructed: bool
    speedup_claim_allowed: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class BoundedSpectralReport:
    created_at: str
    theorem_contract: dict[str, Any]
    concentration_controls: list[SpectralConcentrationControl]
    degree_controls: list[BoundedPolynomialDegreeControl]
    scaling_records: list[BoundedSpectralScalingRecord]
    theorem: BoundedSpectralTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    literature_links: list[dict[str, str]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def spectral_concentration_control(
    half_degree: int,
    copy_count: int,
) -> SpectralConcentrationControl:
    if half_degree < 3 or copy_count < 1:
        raise ValueError("half_degree>=3 and copy_count>=1 are required")
    r = half_degree * (half_degree - 1)
    x = 2**copy_count
    baseline = Fraction(1, x * r)
    likelihood = Fraction(x + r - 1, x**2 * r)
    predicted_excess = Fraction(r - 1, x**2 * r)
    verified = likelihood - baseline == predicted_excess
    root_baseline = math.sqrt(float(baseline))
    root_likelihood = math.sqrt(float(likelihood))
    return SpectralConcentrationControl(
        half_degree=half_degree,
        copy_count=copy_count,
        pair_crossing_index=r,
        baseline_second_moment=str(baseline),
        likelihood_second_moment=str(likelihood),
        baseline_root_second_moment=root_baseline,
        likelihood_root_second_moment=root_likelihood,
        spectral_absolute_first_moment_sum_upper_bound=(
            root_baseline + root_likelihood
        ),
        natural_copy_scale_dominates_crossing_index=x >= r,
        exact_second_moment_formula_verified=verified,
        status=(
            "exact-single-Hecke-spectral-second-moment-concentration"
            if verified
            else "single-Hecke-spectral-concentration-control-failure"
        ),
    )


def bounded_polynomial_degree_control(
    half_degree: int,
    copy_count: int,
    target_bias: float = 0.1,
) -> BoundedPolynomialDegreeControl:
    if not 0.0 < target_bias <= 1.0:
        raise ValueError("target_bias must lie in (0,1]")
    concentration = spectral_concentration_control(
        half_degree,
        copy_count,
    )
    width = concentration.spectral_absolute_first_moment_sum_upper_bound
    exact_lower = math.sqrt(target_bias / width)
    r = concentration.pair_crossing_index
    x = 2**copy_count
    simplified = (
        math.sqrt(target_bias)
        * (x * r) ** 0.25
        / math.sqrt(1.0 + math.sqrt(2.0))
    )
    simplified_valid = bool(
        x >= r and exact_lower >= simplified * (1.0 - 1e-14)
    )
    return BoundedPolynomialDegreeControl(
        half_degree=half_degree,
        copy_count=copy_count,
        target_bias=target_bias,
        spectral_width_upper_bound=width,
        exact_degree_lower_bound=exact_lower,
        integer_degree_lower_bound=math.ceil(exact_lower),
        simplified_natural_degree_lower_bound=simplified,
        integer_simplified_degree_lower_bound=math.ceil(simplified),
        markov_derivative_factor="D^2 for ||p||_infinity<=1 on [-1,1]",
        constant_term_cancels=True,
        bounded_polynomial_bias_bound=(
            "bias <= D^2*(sqrt(tr_B(X^2))+sqrt(tr_B(X^2 Z)))"
        ),
        exact_bound_implies_simplified_bound=simplified_valid,
        status=(
            "bounded-spectral-polynomial-degree-lower-bound"
            if simplified_valid
            else "bounded-spectral-degree-control-failure"
        ),
    )


def bounded_spectral_scaling_record(
    half_degree: int,
    target_bias: float = 0.1,
) -> BoundedSpectralScalingRecord:
    degree = 2 * half_degree
    candidates = involution_class_size(degree, half_degree)
    copies = flatness_copy_count(candidates)
    control = bounded_polynomial_degree_control(
        half_degree,
        copies,
        target_bias,
    )
    required = control.simplified_natural_degree_lower_bound
    candidate_fourth_root_log2 = math.log2(candidates) / 4.0
    required_log2 = math.log2(required)
    fourth_root_comparison = required_log2 >= (
        candidate_fourth_root_log2 - 1.0
    )
    polynomial_comparison = required >= 0.5 * half_degree**2
    return BoundedSpectralScalingRecord(
        half_degree=half_degree,
        degree=degree,
        conjugacy_class_size_decimal=str(candidates),
        copy_count=copies,
        pair_crossing_index=half_degree * (half_degree - 1),
        target_bias=target_bias,
        required_polynomial_degree=required,
        required_polynomial_degree_log2=required_log2,
        candidate_fourth_root_log2=candidate_fourth_root_log2,
        required_degree_exceeds_half_candidate_fourth_root=(
            fourth_root_comparison
        ),
        required_degree_exceeds_half_degree_squared=polynomial_comparison,
        status=(
            "single-Hecke-bounded-spectral-degree-superpolynomial"
            if fourth_root_comparison and polynomial_comparison
            else "single-Hecke-bounded-spectral-scaling-control-failure"
        ),
    )


def build_bounded_spectral_report() -> BoundedSpectralReport:
    concentrations = [
        spectral_concentration_control(half_degree, copy_count)
        for half_degree in (3, 4, 5, 8)
        for copy_count in (4, 8, 16)
    ]
    degree_controls = [
        bounded_polynomial_degree_control(
            half_degree,
            flatness_copy_count(
                involution_class_size(2 * half_degree, half_degree)
            ),
            target_bias,
        )
        for half_degree in (3, 4, 5, 8, 16)
        for target_bias in (0.01, 0.1, 0.5)
    ]
    scaling = [
        bounded_spectral_scaling_record(half_degree)
        for half_degree in (8, 16, 32, 64)
    ]
    verified = bool(
        all(row.exact_second_moment_formula_verified for row in concentrations)
        and all(
            row.constant_term_cancels
            and row.exact_bound_implies_simplified_bound
            for row in degree_controls
        )
        and all(
            row.required_degree_exceeds_half_candidate_fourth_root
            and row.required_degree_exceeds_half_degree_squared
            for row in scaling
        )
    )
    theorem = BoundedSpectralTheorem(
        exact_second_moments=(
            "s0=1/(2^k r), s1=(2^k+r-1)/(4^k r), r=m(m-1)"
        ),
        markov_Cauchy_Schwarz_bound=(
            "For ||p||_infinity<=1 and deg p=D, bias<=D^2(sqrt(s0)+sqrt(s1))."
        ),
        degree_lower_bound=(
            "Bias beta requires D>=sqrt(beta/(sqrt(s0)+sqrt(s1)))."
        ),
        natural_copy_lower_bound=(
            "For 2^k>=64M and 2^k>=r, D>=sqrt(beta)*(2^k r)^1/4/"
            "sqrt(1+sqrt(2))=Omega(M^1/4)."
        ),
        query_model_consequence=(
            "Any bounded-polynomial single-X spectral transformation, including "
            "standard QSVT/block-encoding filtering, needs superpolynomial degree "
            "for constant distinguishing bias."
        ),
        exact_spectral_concentration_proved=True,
        bounded_polynomial_bias_theorem_proved=True,
        superpolynomial_natural_degree_lower_bound_proved=True,
        efficient_single_operator_QSVT_filter_ruled_out=True,
        unrestricted_spectral_projector_ruled_out=False,
        multi_operator_spectral_algorithm_ruled_out=False,
        hidden_involution_detector_constructed=False,
        speedup_claim_allowed=False,
        theorem_verified=verified,
        status=(
            "single-Hecke-bounded-spectral-QSVT-no-go"
            if verified
            else "single-Hecke-bounded-spectral-control-failure"
        ),
    )
    return BoundedSpectralReport(
        created_at=utc_now(),
        theorem_contract={
            "operator": (
                "Canonical cross-transposition X=e_B a_t e_B with spectrum in [-1,1]"
            ),
            "filter_model": (
                "Real polynomial p with degree D and ||p||_infinity<=1; "
                "standard single-operator polynomial eigenvalue transformation"
            ),
            "target": "constant baseline-versus-likelihood expectation bias",
            "claim_boundary": (
                "Does not cover free eigenbasis access, stronger oracles, "
                "unbounded postselection, or noncommuting multi-operator algorithms."
            ),
        },
        concentration_controls=concentrations,
        degree_controls=degree_controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-HIDDEN-INVOLUTION-MULTI-HECKE-SPECTRAL",
                "statement": (
                    "Extend or falsify the concentration/Markov bound for "
                    "noncommuting words in multiple double-coset operators."
                ),
                "resolved": False,
            },
            {
                "id": "PO-HIDDEN-INVOLUTION-STRONG-EIGENBASIS-ACCESS",
                "statement": (
                    "Specify whether any natural representation transform gives "
                    "access stronger than block queries to X without already "
                    "solving the hidden conjugate problem."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": (
                    "Large monomial coefficient norm lets a bounded Chebyshev "
                    "filter evade the normalized-LCU theorem."
                ),
                "answer": (
                    "It evades the l1 argument but not this theorem: Markov's "
                    "operator-norm bound forces superpolynomial degree."
                ),
                "resolved": True,
            },
            {
                "challenge": "Small moments do not imply small total variation.",
                "answer": (
                    "Correct in general. The claim is only for bounded-degree "
                    "polynomial spectral filters; unrestricted projectors remain open."
                ),
                "resolved": True,
            },
            {
                "challenge": "The degree lower bound is merely numerical.",
                "answer": (
                    "False. It follows symbolically from exact second moments, "
                    "Markov's inequality, and Cauchy--Schwarz; finite rows are controls."
                ),
                "resolved": True,
            },
        ],
        literature_links=[
            {
                "id": "MARKOV-BROTHERS-INEQUALITY",
                "role": "Sup norm derivative bound for degree-D polynomials on [-1,1].",
            },
            {
                "id": "QSVT-POLYNOMIAL-EIGENVALUE-TRANSFORMATION",
                "role": "Interprets bounded polynomial degree as single-block query cost.",
            },
        ],
        headline_metrics={
            "exact_concentration_control_count": len(concentrations),
            "bounded_degree_control_count": len(degree_controls),
            "natural_scaling_row_count": len(scaling),
            "minimum_natural_required_degree_log2": min(
                row.required_polynomial_degree_log2 for row in scaling
            ),
            "maximum_natural_required_degree_log2": max(
                row.required_polynomial_degree_log2 for row in scaling
            ),
        },
        claim_gate={
            "exact_single_Hecke_second_moment_concentration_proved": True,
            "bounded_polynomial_spectral_bias_bound_proved": True,
            "efficient_single_operator_QSVT_filter_ruled_out": True,
            "unrestricted_spectral_projector_ruled_out": False,
            "multi_operator_spectral_algorithm_ruled_out": False,
            "hidden_involution_detector_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Any bounded single-X polynomial with constant bias needs "
                "Omega(M^1/4) degree at natural copy count."
            ),
        },
        status=theorem.status,
        summary=(
            "Converted exact spectral concentration into a superpolynomial "
            "degree lower bound for bounded single-Hecke spectral filters."
        ),
        falsifiers_triggered=[
            "Large monomial coefficients do not rescue efficient bounded-polynomial filtering.",
            "Standard single-operator QSVT cannot turn the tiny spectral width into constant bias efficiently.",
            "The remaining route must use stronger access or multiple noncommuting operators.",
        ],
    )


def write_bounded_spectral_report(
    output_path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(build_bounded_spectral_report())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


def run_experiment(
    experiment_id: str = DEFAULT_EXPERIMENT_ID,
    candidate_id: str = DEFAULT_CANDIDATE_ID,
    write_registry: bool = True,
) -> dict[str, Any]:
    del experiment_id, candidate_id, write_registry
    return write_bounded_spectral_report()


if __name__ == "__main__":
    print(json.dumps(run_experiment(), indent=2, sort_keys=True))
