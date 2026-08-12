"""Spectral-filter no-go for the hidden-involution support-span test.

Let ``C`` be a conjugacy class of ``M`` nonidentity involutions and set

    P_h = ((I + R_h) / 2)^tensor k,
    A_k = M^-1 sum_(h in C) P_h.                         (1)

The information-theoretic support-span measurement is ``supp(A_k)``.  A
normalization-one block encoding of ``A_k`` is easy, but the useful spectrum
is not at inverse-polynomial scale.  The exact class-mixture chi-square
identity gives

    Tr(A_k) / d = 2^-k,
    Tr(A_k^2) / d = 4^-k [1 + (2^k - 1) / M].           (2)

Consequently, under the alternative state
``rho_C=(2^k/d) A_k``, the mean measured eigenvalue is

    mu = 2^-k + (1 - 2^-k) / M.                         (3)

At ``k >= ceil(log2(4M))``, the support test has null acceptance at most
``1/4``, while at least ``3/4`` of the alternative spectral mass lies below
``4 mu <= 5/M``.  Thus the binary signal is carried predominantly by
eigenvalues of order ``1/M``, not by a negligible worst-conditioned tail.

More strongly, suppose a globally bounded polynomial effect ``0 <= p <= 1``
on ``[0,1]`` satisfies

    Tr[p(A_k) rho_0] <= 1/3,
    Tr[p(A_k) rho_C] >= 2/3.                             (4)

The support-rank bound makes the zero eigenspace at least ``3d/4``, hence
``p(0) <= 4/9``.  Equation (3) and Markov's probability inequality imply that
some actual eigenvalue ``lambda <= 4 mu`` has ``p(lambda) >= 5/9``.  The mean
value theorem and Markov brothers' polynomial inequality on ``[0,1]`` then
give

    deg(p) >= 1 / sqrt(72 mu) = Omega(sqrt(M)).          (5)

For fixed-point-free involutions in ``S_n``, ``log M=Theta(n log n)``, so this
degree is exponential in the input register length.  This rules out generic
QSVT/polynomial spectral filtering of the normalization-one ``A_k`` block
encoding, including approximate filters that only need bounded-error binary
discrimination.  It is not a lower bound on arbitrary circuits.  A structured
compiler could still deflate exceptional high-eigenvalue sectors, rescale
source-dependent blocks, or implement the support through a non-polynomial
representation-theoretic transform.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

from coset_hidden_involution_binary_decision_reduction import (
    involution_class_size,
)
from coset_hidden_involution_orbit_hull_twirl_reduction import (
    orbit_average_candidate_projector,
)
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_support_filter_no_go.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-HIDDEN-INVOLUTION-SUPPORT-FILTER-NO-GO"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class SupportSpectrumFiniteControl:
    n: int
    transposition_count: int
    copy_count: int
    conjugacy_class_size: int
    data_dimension: int
    support_rank: int
    support_rank_fraction: float
    normalized_trace: float
    normalized_second_moment: float
    effective_rank: float
    exact_alternative_mean_eigenvalue: float
    empirical_alternative_mean_eigenvalue: float
    smallest_positive_eigenvalue: float
    smallest_eigenvalue_upper_bound: float
    trace_identity_residual: float
    second_moment_identity_residual: float
    effective_rank_bound_verified: bool
    smallest_eigenvalue_bound_verified: bool
    finite_control_verified: bool
    status: str


@dataclass(frozen=True)
class SupportFilterScalingRecord:
    n: int
    conjugacy_class_size: int
    copy_count: int
    support_rank_fraction_upper_bound: float
    alternative_mean_eigenvalue: float
    low_spectrum_threshold: float
    alternative_mass_below_threshold_lower_bound: float
    polynomial_degree_lower_bound: int
    log2_polynomial_degree_lower_bound: float
    degree_over_sqrt_class_size: float
    inverse_polynomial_spectral_filter_possible: bool
    arbitrary_structured_compiler_ruled_out: bool
    status: str


@dataclass(frozen=True)
class SupportFilterNoGoTheorem:
    exact_moment_identity: str
    effective_rank_consequence: str
    alternative_spectral_mass_consequence: str
    bounded_error_polynomial_lower_bound: str
    exact_moments_proved: bool
    low_spectrum_mass_proved: bool
    polynomial_degree_exponential_at_threshold: bool
    generic_qsvt_support_filter_ruled_out: bool
    arbitrary_circuit_lower_bound_proved: bool
    structured_support_compiler_constructed: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class SupportFilterNoGoReport:
    created_at: str
    primary_literature: list[dict[str, str]]
    theorem_contract: dict[str, Any]
    finite_controls: list[SupportSpectrumFiniteControl]
    scaling_records: list[SupportFilterScalingRecord]
    theorem: SupportFilterNoGoTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def ceil_log2(value: int) -> int:
    if value < 1:
        raise ValueError("value must be positive")
    return (value - 1).bit_length()


def exact_normalized_moments(
    conjugacy_class_size: int,
    copy_count: int,
) -> tuple[Fraction, Fraction]:
    """Return ``Tr(A)/d`` and ``Tr(A^2)/d`` from the exact chi-square law."""

    if conjugacy_class_size < 1 or copy_count < 1:
        raise ValueError("class size and copy count must be positive")
    power = 1 << copy_count
    first = Fraction(1, power)
    second = Fraction(
        conjugacy_class_size + power - 1,
        conjugacy_class_size * power * power,
    )
    return first, second


def alternative_mean_eigenvalue(
    conjugacy_class_size: int,
    copy_count: int,
) -> Fraction:
    """Return ``E_(rho_C)[lambda(A)]`` exactly."""

    _, second = exact_normalized_moments(
        conjugacy_class_size, copy_count
    )
    return (1 << copy_count) * second


def effective_rank_fraction_lower_bound(
    conjugacy_class_size: int,
    copy_count: int,
) -> Fraction:
    """Return the exact lower bound ``rank(A)/d >= r_eff/d``."""

    power = 1 << copy_count
    return Fraction(
        conjugacy_class_size,
        conjugacy_class_size + power - 1,
    )


def support_rank_fraction_upper_bound(
    conjugacy_class_size: int,
    copy_count: int,
) -> Fraction:
    """Return the union-of-ranges rank bound, clipped at one."""

    return min(Fraction(1, 1), Fraction(conjugacy_class_size, 1 << copy_count))


def smallest_positive_eigenvalue_upper_bound(
    conjugacy_class_size: int,
    copy_count: int,
) -> Fraction:
    """Bound ``lambda_min^+(A)`` by ``Tr(A)/effective_rank(A)``."""

    return alternative_mean_eigenvalue(conjugacy_class_size, copy_count)


def _ceil_sqrt_fraction(value: Fraction) -> int:
    if value <= 0:
        raise ValueError("value must be positive")
    numerator = value.numerator
    denominator = value.denominator
    root = math.isqrt(numerator // denominator)
    while root * root * denominator < numerator:
        root += 1
    return root


def bounded_error_polynomial_degree_lower_bound(
    conjugacy_class_size: int,
    copy_count: int,
) -> int:
    """Return the Markov-inequality lower bound ``ceil(1/sqrt(72 mu))``.

    The bounded-error argument requires support null mass at least ``3/4`` and
    ``4 mu <= 1``.  Both hold for the fixed-point-free scaling records below.
    """

    rank_upper = support_rank_fraction_upper_bound(
        conjugacy_class_size, copy_count
    )
    mean = alternative_mean_eigenvalue(
        conjugacy_class_size, copy_count
    )
    if rank_upper > Fraction(1, 4):
        raise ValueError("copy count does not force three-quarter null kernel")
    if 4 * mean > 1:
        raise ValueError("low-spectrum threshold exceeds the encoded interval")
    return _ceil_sqrt_fraction(Fraction(1, 72) / mean)


def audit_support_spectrum_control(
    n: int,
    transposition_count: int,
    copy_count: int,
    *,
    tolerance: float = 1e-9,
) -> SupportSpectrumFiniteControl:
    average = orbit_average_candidate_projector(
        n, transposition_count, copy_count
    )
    dimension = average.shape[0]
    class_size = involution_class_size(n, transposition_count)
    eigenvalues = np.linalg.eigvalsh(average)
    positive = eigenvalues[eigenvalues > tolerance]
    support_rank = len(positive)
    normalized_trace = float(np.trace(average).real / dimension)
    normalized_second = float(
        np.trace(average @ average).real / dimension
    )
    exact_first, exact_second = exact_normalized_moments(
        class_size, copy_count
    )
    exact_mean = alternative_mean_eigenvalue(class_size, copy_count)
    empirical_mean = (1 << copy_count) * normalized_second
    effective_rank = float(
        np.trace(average).real ** 2
        / np.trace(average @ average).real
    )
    minimum = float(positive[0])
    minimum_upper = float(
        smallest_positive_eigenvalue_upper_bound(class_size, copy_count)
    )
    effective_bound = effective_rank_fraction_lower_bound(
        class_size, copy_count
    )
    effective_verified = (
        support_rank / dimension + tolerance >= float(effective_bound)
        and support_rank + tolerance >= effective_rank
    )
    minimum_verified = minimum <= minimum_upper + tolerance
    verified = bool(
        abs(normalized_trace - float(exact_first)) <= tolerance
        and abs(normalized_second - float(exact_second)) <= tolerance
        and abs(empirical_mean - float(exact_mean)) <= tolerance
        and effective_verified
        and minimum_verified
    )
    return SupportSpectrumFiniteControl(
        n=n,
        transposition_count=transposition_count,
        copy_count=copy_count,
        conjugacy_class_size=class_size,
        data_dimension=dimension,
        support_rank=support_rank,
        support_rank_fraction=support_rank / dimension,
        normalized_trace=normalized_trace,
        normalized_second_moment=normalized_second,
        effective_rank=effective_rank,
        exact_alternative_mean_eigenvalue=float(exact_mean),
        empirical_alternative_mean_eigenvalue=empirical_mean,
        smallest_positive_eigenvalue=minimum,
        smallest_eigenvalue_upper_bound=minimum_upper,
        trace_identity_residual=abs(normalized_trace - float(exact_first)),
        second_moment_identity_residual=abs(
            normalized_second - float(exact_second)
        ),
        effective_rank_bound_verified=effective_verified,
        smallest_eigenvalue_bound_verified=minimum_verified,
        finite_control_verified=verified,
        status=(
            "exact-moments-and-support-gap-bound-verified"
            if verified
            else "support-spectrum-control-failure"
        ),
    )


def support_filter_scaling_record(n: int) -> SupportFilterScalingRecord:
    if n < 6 or n % 2:
        raise ValueError("n must be even and at least six")
    class_size = involution_class_size(n, n // 2)
    copies = ceil_log2(4 * class_size)
    rank_upper = support_rank_fraction_upper_bound(class_size, copies)
    mean = alternative_mean_eigenvalue(class_size, copies)
    degree = bounded_error_polynomial_degree_lower_bound(class_size, copies)
    return SupportFilterScalingRecord(
        n=n,
        conjugacy_class_size=class_size,
        copy_count=copies,
        support_rank_fraction_upper_bound=float(rank_upper),
        alternative_mean_eigenvalue=float(mean),
        low_spectrum_threshold=float(4 * mean),
        alternative_mass_below_threshold_lower_bound=0.75,
        polynomial_degree_lower_bound=degree,
        log2_polynomial_degree_lower_bound=math.log2(degree),
        degree_over_sqrt_class_size=degree / math.sqrt(class_size),
        inverse_polynomial_spectral_filter_possible=False,
        arbitrary_structured_compiler_ruled_out=False,
        status=(
            "generic-bounded-error-polynomial-filter-exponential-"
            "structured-compiler-open"
        ),
    )


def build_support_filter_no_go_report(
    *,
    finite_specs: tuple[tuple[int, int, int], ...] = (
        (3, 1, 1),
        (3, 1, 2),
        (4, 1, 2),
        (4, 2, 2),
    ),
    scaling_n_values: tuple[int, ...] = (16, 32, 64, 128),
) -> SupportFilterNoGoReport:
    controls = [
        audit_support_spectrum_control(n, transpositions, copies)
        for n, transpositions, copies in finite_specs
    ]
    scaling = [support_filter_scaling_record(n) for n in scaling_n_values]
    verified = all(row.finite_control_verified for row in controls)
    exponential = all(
        row.polynomial_degree_lower_bound > row.copy_count
        and not row.inverse_polynomial_spectral_filter_possible
        for row in scaling
    )
    theorem = SupportFilterNoGoTheorem(
        exact_moment_identity=(
            "Tr(A)/d=2^-k and Tr(A^2)/d=4^-k[1+(2^k-1)/M]."
        ),
        effective_rank_consequence=(
            "rank(A)/d >= 1/[1+(2^k-1)/M], while "
            "lambda_min^+(A) <= 2^-k+(1-2^-k)/M."
        ),
        alternative_spectral_mass_consequence=(
            "At k>=ceil(log2(4M)), at least 3/4 of alternative mass has "
            "lambda<=4mu<=5/M."
        ),
        bounded_error_polynomial_lower_bound=(
            "Any globally [0,1]-bounded polynomial effect with null "
            "acceptance <=1/3 and alternative acceptance >=2/3 has "
            "degree >=1/sqrt(72mu)=Omega(sqrt(M))."
        ),
        exact_moments_proved=True,
        low_spectrum_mass_proved=True,
        polynomial_degree_exponential_at_threshold=exponential,
        generic_qsvt_support_filter_ruled_out=exponential,
        arbitrary_circuit_lower_bound_proved=False,
        structured_support_compiler_constructed=False,
        theorem_verified=verified and exponential,
        status=(
            "generic-support-spectral-filter-refuted-structured-block-"
            "rescaling-open"
            if verified and exponential
            else "support-filter-no-go-control-failure"
        ),
    )
    metrics: dict[str, int | float] = {
        "finite_control_count": len(controls),
        "finite_control_failure_count": sum(
            not row.finite_control_verified for row in controls
        ),
        "exact_moment_theorem_count": 1,
        "alternative_low_spectrum_mass_theorem_count": 1,
        "generic_polynomial_filter_no_go_count": 1 if exponential else 0,
        "structured_support_compiler_count": 0,
        "arbitrary_circuit_lower_bound_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return SupportFilterNoGoReport(
        created_at=utc_now(),
        primary_literature=[
            {
                "id": "HAYASHI-KAWACHI-KOBAYASHI-2006-HSP-SAMPLE-COMPLEXITY",
                "title": "Quantum Measurements for Hidden Subgroup Problems with Optimal Sample Complexity",
                "url": "https://arxiv.org/abs/quant-ph/0604174",
                "scope": (
                    "Provides the information-theoretic support-span test; the "
                    "present result isolates its normalized spectral cost."
                ),
            },
            {
                "id": "GILYEN-SU-LOW-WIEBE-2018-QSVT",
                "title": "Quantum singular value transformation and beyond",
                "url": "https://arxiv.org/abs/1806.01838",
                "scope": (
                    "Supplies the generic bounded-polynomial block-encoding "
                    "framework to which the degree obstruction applies."
                ),
            },
        ],
        theorem_contract={
            "state_model": (
                "The standard k-copy mixed coset-state class mixture for a "
                "uniform conjugacy class of M nonidentity involutions."
            ),
            "compiler_scope": (
                "One globally bounded scalar polynomial effect p(A_k) applied "
                "to a normalization-one block encoding of A_k."
            ),
            "error_scope": (
                "Distributional bounded error, not uniform operator-norm "
                "approximation of the entire support projector."
            ),
            "outside_scope": (
                "Source-conditioned rescaling, exceptional-sector deflation, "
                "rational/variable-time methods with additional structure, "
                "and arbitrary representation-theoretic circuits."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-COSET-BINARY-SECTOR-DEFLATION",
                "statement": (
                    "Decompose and remove the exceptional large-eigenvalue "
                    "sectors, then prove whether the remaining A_k admits a "
                    "polynomial normalization boost."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-BINARY-SOURCE-BLOCK-CONDITIONING",
                "statement": (
                    "Bound the occupied multiplicity-block spectra after "
                    "source-label conditioning, rather than globally."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-BINARY-DIRECT-SUPPORT-TRANSFORM",
                "statement": (
                    "Construct a representation-theoretic range transform for "
                    "W whose cost is not controlled by sigma_min(W)."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-BINARY-FILTER-DEQUANTIZATION",
                "statement": (
                    "Test whether any proposed sector deflation or rescaling is "
                    "also available to a classical query-limited algorithm."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "Only a negligible worst-conditioned tail causes the gap.",
                "answer": (
                    "False: at least three quarters of the alternative spectral "
                    "mass lies at lambda<=4mu=O(1/M)."
                ),
                "resolved": True,
            },
            {
                "challenge": "Approximate bounded-error filtering avoids the support condition number.",
                "answer": (
                    "False for globally bounded polynomial effects: the "
                    "distributional acceptance conditions alone force "
                    "degree Omega(sqrt(M))."
                ),
                "resolved": True,
            },
            {
                "challenge": "The result proves no efficient binary algorithm exists.",
                "answer": (
                    "False. It rules out only scalar polynomial functional "
                    "calculus of the normalization-one average projector."
                ),
                "resolved": True,
            },
            {
                "challenge": "A source-conditioned block normalization is covered.",
                "answer": (
                    "False. Deflating exceptional sectors and renormalizing "
                    "naturally occupied blocks is the main surviving route."
                ),
                "resolved": True,
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "support_span_measurement_information_theoretically_valid": True,
            "useful_spectral_mass_inverse_polynomial": False,
            "normalization_one_qsvt_filter_polynomial_time": False,
            "source_conditioned_rescaling_refuted": False,
            "arbitrary_structured_compiler_refuted": False,
            "efficient_binary_hidden_involution_algorithm_constructed": False,
            "graph_isomorphism_algorithm_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The natural support filter needs exponential polynomial degree, "
                "while the only live escape is an unproved structured sector "
                "deflation/rescaling or direct multiplicity transform."
            ),
        },
        status=theorem.status,
        summary=(
            "Exact moments show that the useful support-span signal itself is "
            "concentrated at normalized eigenvalue scale Theta(1/M). Generic "
            "bounded-error polynomial/QSVT filtering therefore costs "
            "Omega(sqrt(M)); structured block rescaling remains open."
        ),
        falsifiers_triggered=[
            "A normalization-one average-projector block encoding is not an efficient support measurement.",
            "The small-gap obstruction is not confined to negligible alternative mass.",
            "Replacing exact support projection by bounded-error scalar polynomial filtering does not remove the exponential degree.",
            "No arbitrary-circuit or graph-isomorphism lower bound follows from this compiler-specific obstruction.",
        ],
    )


def write_support_filter_no_go_report(
    output_path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-COSET-HIDDEN-INVOLUTION-SUPPORT-FILTER-NO-GO"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    path = output_path
    output_path = output_path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    payload = asdict(build_support_filter_no_go_report(**kwargs))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_support_filter_no_go_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
