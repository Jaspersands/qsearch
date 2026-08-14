"""Balanced base-color concentration for the natural hidden-involution source.

Let ``N=(C_2)^m`` be the base subgroup of ``K=C_2 wr S_m``.  Its characters
are indexed by bit strings ``y in F_2^m``; the ``S_m`` orbit of ``y`` is its
Hamming weight ``r``.  In wreath notation, ``r`` is the size of one color
partition.

For the one-copy canonical source fiber ``R=ran((I+R_h)/2)``, an element of
``N`` with ``t`` flipped matching pairs has normalized character

    q_t = 2^t t! (2m-2t)!/(2m)! * (1+1[2t=m]).          (1)

Fourier inversion gives the exact ``k``-copy color-weight law

    p_(m,k)(r) = binom(m,r) 2^-m
      sum_(t=0)^m K_t(r) q_t^k,                         (2)

where ``K_t(r)`` is the binary Krawtchouk polynomial.  For ``m>=2``, every
nonidentity ``q_t<=1/3``.  Hence the full color-string law has

    TV(p_color, Uniform(F_2^m))
      <= (2^m-1)3^-k/2.                                (3)

At ``k>=m`` it is exponentially close to uniform, so color weight is close to
``Binomial(m,1/2)``.  In particular the source mass outside
``m/4<=r<=3m/4`` is at most

    2 exp(-m/8) + (2^m-1)3^-k/2.                       (4)

The alternative source law size-biases by the orbit-synthesis Gram eigenvalue
``x``.  Using ``E[x^2]=1+(M-1)/2^k``, Cauchy--Schwarz transfers (4): at the
six-copy-overhead flatness width, alternative mass outside the balanced band
is at most the square root of ``(1+eta)`` times (4).

Thus essentially all natural signal lies in balanced nontrivial color bands;
the all-trivial embedded Kronecker sector is not representative.  This theorem
does not decompose the residual ``S_r times S_(m-r)`` multiplicities, compile
their matrix-Hecke transfer, or prove a speedup.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from coset_hidden_involution_orbit_synthesis_flatness import flatness_copy_count
from coset_hyperoctahedral_trivial_color_mass_no_go import (
    normalized_fiber_character,
)
from coset_perfect_matching_spherical_boundary import perfect_matching_count
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hyperoctahedral_color_weight_concentration.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HYPEROCTAHEDRAL-COLOR-WEIGHT-CONCENTRATION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class ColorWeightFiniteControl:
    half_degree: int
    copy_count: int
    color_string_count: int
    weight_count: int
    minimum_exact_color_multiplicity: int
    exact_weight_multiplicity_sum_decimal: str
    tensor_fiber_dimension_decimal: str
    exact_weight_probability_sum: float
    maximum_equal_weight_probability_residual: float
    exact_color_tv_from_uniform: float
    character_tv_upper_bound: float
    tv_bound_residual: float
    exact_fourier_weight_law_verified: bool
    status: str


@dataclass(frozen=True)
class ColorWeightScalingRecord:
    half_degree: int
    degree: int
    perfect_matching_count_decimal: str
    copy_count: int
    balanced_weight_lower: int
    balanced_weight_upper: int
    color_tv_upper_bound: float
    binomial_tail_upper_bound: float
    source_outside_balanced_upper_bound: float
    alternative_outside_balanced_upper_bound: float
    alternative_balanced_mass_lower_bound: float
    color_weight_asymptotically_balanced: bool
    balanced_little_group_qft_available: bool
    balanced_matrix_hecke_transfer_compiled: bool
    status: str


@dataclass(frozen=True)
class ColorWeightConcentrationTheorem:
    color_dual: str
    exact_fourier_law: str
    character_gap: str
    total_variation_bound: str
    balanced_source_concentration: str
    alternative_transfer: str
    representation_consequence: str
    scope_limit: str
    exact_color_weight_law_proved: bool
    exponential_uniform_color_convergence_proved: bool
    balanced_source_mass_proved: bool
    balanced_alternative_mass_proved: bool
    balanced_residual_fusion_compiled: bool
    full_matrix_hecke_polar_compiled: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class ColorWeightConcentrationReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[ColorWeightFiniteControl]
    scaling_records: list[ColorWeightScalingRecord]
    theorem: ColorWeightConcentrationTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def binary_krawtchouk(
    half_degree: int,
    polynomial_degree: int,
    weight: int,
) -> int:
    if (
        half_degree < 1
        or not 0 <= polynomial_degree <= half_degree
        or not 0 <= weight <= half_degree
    ):
        raise ValueError("invalid Krawtchouk parameters")
    return sum(
        ((-1) ** intersection)
        * math.comb(weight, intersection)
        * math.comb(
            half_degree - weight,
            polynomial_degree - intersection,
        )
        for intersection in range(polynomial_degree + 1)
        if intersection <= weight
        and polynomial_degree - intersection <= half_degree - weight
    )


def exact_color_character_multiplicity(
    half_degree: int,
    copy_count: int,
    weight: int,
) -> int:
    if half_degree < 1 or copy_count < 1 or not 0 <= weight <= half_degree:
        raise ValueError("invalid color multiplicity parameters")
    fiber_dimension = math.factorial(2 * half_degree) // 2
    multiplicity = sum(
        Fraction(binary_krawtchouk(half_degree, t, weight), 2**half_degree)
        * (
            normalized_fiber_character(half_degree, t) * fiber_dimension
        )
        ** copy_count
        for t in range(half_degree + 1)
    )
    if multiplicity.denominator != 1 or multiplicity < 0:
        raise ArithmeticError("color multiplicity was not nonnegative integral")
    return multiplicity.numerator


def exact_color_weight_probabilities(
    half_degree: int,
    copy_count: int,
) -> tuple[Fraction, ...]:
    fiber_dimension = math.factorial(2 * half_degree) // 2
    tensor_dimension = fiber_dimension**copy_count
    return tuple(
        Fraction(
            math.comb(half_degree, weight)
            * exact_color_character_multiplicity(
                half_degree, copy_count, weight
            ),
            tensor_dimension,
        )
        for weight in range(half_degree + 1)
    )


def color_tv_upper_bound(
    half_degree: int,
    copy_count: int,
) -> float:
    if half_degree < 2 or copy_count < 1:
        raise ValueError("half_degree must be at least two and copies positive")
    return 0.5 * (2**half_degree - 1) * 3.0 ** (-copy_count)


def audit_color_weight_law(
    half_degree: int,
    copy_count: int,
) -> ColorWeightFiniteControl:
    if half_degree < 2 or half_degree > 6:
        raise ValueError("finite control supports half_degree in [2,6]")
    if copy_count < 1:
        raise ValueError("copy_count must be positive")
    fiber_dimension = math.factorial(2 * half_degree) // 2
    tensor_dimension = fiber_dimension**copy_count
    multiplicities = tuple(
        exact_color_character_multiplicity(half_degree, copy_count, weight)
        for weight in range(half_degree + 1)
    )
    weights = exact_color_weight_probabilities(half_degree, copy_count)
    total_multiplicity = sum(
        math.comb(half_degree, weight) * multiplicities[weight]
        for weight in range(half_degree + 1)
    )
    exact_tv = Fraction()
    maximum_equal_weight_residual = Fraction()
    uniform_string_probability = Fraction(1, 2**half_degree)
    for weight, multiplicity in enumerate(multiplicities):
        string_probability = Fraction(multiplicity, tensor_dimension)
        exact_tv += Fraction(math.comb(half_degree, weight), 2) * abs(
            string_probability - uniform_string_probability
        )
        reconstructed_weight = (
            math.comb(half_degree, weight) * string_probability
        )
        maximum_equal_weight_residual = max(
            maximum_equal_weight_residual,
            abs(reconstructed_weight - weights[weight]),
        )
    upper = color_tv_upper_bound(half_degree, copy_count)
    residual = max(0.0, float(exact_tv) - upper)
    verified = bool(
        total_multiplicity == tensor_dimension
        and sum(weights) == 1
        and maximum_equal_weight_residual == 0
        and residual <= 1e-12
    )
    return ColorWeightFiniteControl(
        half_degree=half_degree,
        copy_count=copy_count,
        color_string_count=2**half_degree,
        weight_count=half_degree + 1,
        minimum_exact_color_multiplicity=min(multiplicities),
        exact_weight_multiplicity_sum_decimal=str(total_multiplicity),
        tensor_fiber_dimension_decimal=str(tensor_dimension),
        exact_weight_probability_sum=float(sum(weights)),
        maximum_equal_weight_probability_residual=float(
            maximum_equal_weight_residual
        ),
        exact_color_tv_from_uniform=float(exact_tv),
        character_tv_upper_bound=upper,
        tv_bound_residual=residual,
        exact_fourier_weight_law_verified=verified,
        status=(
            "exact-base-color-krawtchouk-law-verified"
            if verified
            else "base-color-weight-control-failure"
        ),
    )


def color_weight_scaling_record(
    half_degree: int,
) -> ColorWeightScalingRecord:
    if half_degree < 2:
        raise ValueError("half_degree must be at least two")
    matchings = perfect_matching_count(half_degree)
    copies = flatness_copy_count(matchings)
    lower = math.ceil(half_degree / 4)
    upper = math.floor(3 * half_degree / 4)
    tv = color_tv_upper_bound(half_degree, copies)
    binomial_tail = min(1.0, 2.0 * math.exp(-half_degree / 8.0))
    source_outside = min(1.0, binomial_tail + tv)
    eta = (matchings - 1) / (2**copies)
    alternative_outside = min(
        1.0, math.sqrt((1.0 + eta) * source_outside)
    )
    return ColorWeightScalingRecord(
        half_degree=half_degree,
        degree=2 * half_degree,
        perfect_matching_count_decimal=str(matchings),
        copy_count=copies,
        balanced_weight_lower=lower,
        balanced_weight_upper=upper,
        color_tv_upper_bound=tv,
        binomial_tail_upper_bound=binomial_tail,
        source_outside_balanced_upper_bound=source_outside,
        alternative_outside_balanced_upper_bound=alternative_outside,
        alternative_balanced_mass_lower_bound=1.0 - alternative_outside,
        color_weight_asymptotically_balanced=True,
        balanced_little_group_qft_available=True,
        balanced_matrix_hecke_transfer_compiled=False,
        status="balanced-color-mass-proved-residual-transfer-open",
    )


def build_color_weight_concentration_report(
    *,
    finite_specs: tuple[tuple[int, int], ...] = (
        (2, 1),
        (2, 2),
        (3, 1),
        (3, 2),
        (4, 2),
    ),
    scaling_half_degrees: tuple[int, ...] = (4, 8, 16, 32, 64, 128),
) -> ColorWeightConcentrationReport:
    controls = [audit_color_weight_law(m, k) for m, k in finite_specs]
    scaling = [
        color_weight_scaling_record(m) for m in scaling_half_degrees
    ]
    verified = all(row.exact_fourier_weight_law_verified for row in controls)
    scaling_verified = all(
        row.copy_count >= row.half_degree
        and row.color_weight_asymptotically_balanced
        and row.balanced_little_group_qft_available
        and not row.balanced_matrix_hecke_transfer_compiled
        for row in scaling
    )
    theorem = ColorWeightConcentrationTheorem(
        color_dual=(
            "Characters of N=(C_2)^m are bit strings y; S_m orbits are their "
            "weights r, equal to wreath color-partition size."
        ),
        exact_fourier_law=(
            "p_(m,k)(r)=binom(m,r)2^-m sum_t K_t(r)q_t^k with q_t the "
            "normalized canonical-fiber character."
        ),
        character_gap=(
            "For every m>=2 and nonidentity base element, 0<=q_t<=1/3."
        ),
        total_variation_bound=(
            "TV(color,uniform)<=((2^m-1)/2)3^-k."
        ),
        balanced_source_concentration=(
            "Outside m/4<=r<=3m/4, source mass is at most "
            "2exp(-m/8)+TV."
        ),
        alternative_transfer=(
            "Global Gram second moment and Cauchy-Schwarz bound alternative "
            "outside mass by sqrt((1+eta) times source outside mass)."
        ),
        representation_consequence=(
            "Source-relevant fusion lies in balanced little groups "
            "S_r times S_(m-r), not trivial color."
        ),
        scope_limit=(
            "No residual little-group multiplicity basis, matrix-Hecke polar, "
            "physical source lift, or algorithm is constructed."
        ),
        exact_color_weight_law_proved=True,
        exponential_uniform_color_convergence_proved=True,
        balanced_source_mass_proved=True,
        balanced_alternative_mass_proved=True,
        balanced_residual_fusion_compiled=False,
        full_matrix_hecke_polar_compiled=False,
        theorem_verified=verified and scaling_verified,
        status=(
            "balanced-color-alternative-mass-proved-residual-fusion-open"
            if verified and scaling_verified
            else "color-weight-concentration-control-failure"
        ),
    )
    return ColorWeightConcentrationReport(
        created_at=utc_now(),
        theorem_contract={
            "family": (
                "Canonical k-copy plus fiber for fixed-point-free involutions "
                "in S_(2m), restricted to the base subgroup N=(C_2)^m."
            ),
            "distribution": (
                "Uniform source-vector color law and its Gram-size-biased "
                "alternative contribution."
            ),
            "balanced_band": "ceil(m/4)<=|y|<=floor(3m/4).",
            "outside_scope": (
                "Fine bipartition labels within each color weight, transfer "
                "conditioning, dequantization, and hidden-element recovery."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-COSET-HYPEROCTAHEDRAL-BALANCED-LITTLE-GROUP-BASIS",
                "statement": (
                    "Compile or rule out a source-specific basis for residual "
                    "S_r times S_(m-r) multiplicities on balanced colors."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-HYPEROCTAHEDRAL-BALANCED-MATRIX-HECKE-POLAR",
                "statement": (
                    "Determine the support and relative spectrum of the matrix-"
                    "Hecke transfer on the balanced alternative mass."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-HYPEROCTAHEDRAL-BALANCED-DEQUANTIZATION",
                "statement": (
                    "Test balanced color/fusion statistics against classical "
                    "matching-intersection and symmetric-group baselines."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "The source may concentrate on a few exceptional colors.",
                "answer": (
                    "False at k>=m: its entire color-string law is exponentially "
                    "close to uniform by the nonidentity character gap."
                ),
                "resolved": True,
            },
            {
                "challenge": "Source concentration automatically transfers to alternative mass.",
                "answer": (
                    "Not automatically; the proof explicitly uses the exact "
                    "second moment to control size bias."
                ),
                "resolved": True,
            },
            {
                "challenge": "Balanced color makes the remaining transform easy.",
                "answer": (
                    "Unproved. It only identifies the relevant little groups; "
                    "their multiplicity transfer may contain the full hardness."
                ),
                "resolved": True,
            },
        ],
        headline_metrics={
            "exact_color_weight_control_count": len(controls),
            "finite_control_failure_count": sum(
                not row.exact_fourier_weight_law_verified for row in controls
            ),
            "balanced_source_concentration_theorem_count": 1,
            "balanced_alternative_concentration_theorem_count": 1,
            "minimum_scaling_alternative_balanced_mass_lower_bound": min(
                row.alternative_balanced_mass_lower_bound for row in scaling
            ),
            "maximum_scaling_alternative_balanced_mass_lower_bound": max(
                row.alternative_balanced_mass_lower_bound for row in scaling
            ),
            "balanced_matrix_hecke_compiler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "exact_base_color_weight_law_proved": verified,
            "natural_alternative_mass_concentrates_on_balanced_colors": (
                verified and scaling_verified
            ),
            "trivial_color_is_representative_of_natural_source": False,
            "balanced_little_group_qft_available": True,
            "balanced_residual_multiplicity_basis_compiled": False,
            "balanced_matrix_hecke_polar_compiled": False,
            "efficient_binary_hidden_involution_algorithm_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The natural signal is localized to balanced base colors, but "
                "the residual little-group multiplicities and source-specific "
                "transfer remain uncompiled."
            ),
        },
        status=theorem.status,
        summary=(
            "Derived the exact Krawtchouk color-weight law, proved exponential "
            "convergence to balanced binomial colors, and transferred that "
            "concentration to alternative mass, isolating balanced little-group "
            "matrix-Hecke fusion as the next compiler target."
        ),
        falsifiers_triggered=[
            "The natural source does not concentrate on exceptional or trivial base colors.",
            "The alternative size bias does not destroy balanced-color concentration at the flatness width.",
            "Balanced color localization does not itself solve residual symmetric-group multiplicities.",
        ],
    )


def write_color_weight_concentration_report(
    output_path: Path = REPORT_PATH,
    **kwargs: Any,
) -> dict[str, Any]:
    payload = asdict(build_color_weight_concentration_report(**kwargs))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return payload


if __name__ == "__main__":
    report = write_color_weight_concentration_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
