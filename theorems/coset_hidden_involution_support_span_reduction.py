"""Support-span reduction for the published hidden-involution sample test.

Hayashi, Kawachi, and Kobayashi prove the general upper bound for Triviality of
Coset State by a one-sided support test.  For an involution class ``C`` of size
``M``, put

    P_h = ((I+R_h)/2)^tensor k,
    A_k = M^-1 sum_(h in C) P_h,
    T_k = projector onto supp(A_k).                      (1)

Every alternative state is ``rho_h^k=(2^k/|G|^k)P_h``, so

    Tr(T_k rho_h^k)=1                                   (2)

for every ``h``.  Under the trivial subgroup state,

    Tr(T_k I/|G|^k) = rank(T_k)/|G|^k
      <= M rank(P_h)/|G|^k = M/2^k.                    (3)

Thus ``k=ceil(log2(M/delta))`` gives perfect alternative completeness and
null false-positive probability at most ``delta``.  This is the known
information-theoretic upper bound, not a new sample-complexity result.

The computational reduction is still useful.  Define the synthesis operator

    W_k = M^-1/2 sum_h P_h <h|,                          (4)

from a hidden-label register tensored with the data space into the data space.
Then ``W_k W_k^*=A_k`` and

    T_k = polar(W_k) polar(W_k)^* = supp(W_k W_k^*).    (5)

Uniform perfect-matching preparation and controlled right multiplication give
an efficient description/block encoding of ``W_k``.  Generic range projection
depends on the least positive singular value of ``W_k``; the rank argument in
(3) supplies no lower bound on it.  A direct representation-theoretic basis
for the range could bypass that gap, so neither a generic QSVT obstruction nor
the absence of a spectral certificate is an arbitrary-circuit lower bound.

This support projector is a distinct live route from shifted Helstrom
thresholding.  At two copies it reduces to supported ``(lambda,mu;nu)`` target
sectors.  At the logarithmic-copy threshold it requires a uniform description
of the higher recoupling-multiplicity range.  The next algorithmic question is
therefore whether that range has a polynomial subduction/association-scheme
basis, not whether logarithmically many states contain enough information.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from coset_hidden_involution_binary_decision_reduction import (
    dense_binary_states,
    dense_hidden_coset_state,
    involution_class_size,
    involution_conjugacy_class,
    support_rank_sufficient_copies,
)
from coset_hidden_involution_threshold_compiler_boundary import (
    average_projector_from_dense_alternative,
)
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_support_span_reduction.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-SUPPORT-SPAN-REDUCTION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class SupportSpanFiniteControl:
    n: int
    transposition_count: int
    copy_count: int
    conjugacy_class_size: int
    data_dimension: int
    candidate_support_rank: int
    sum_of_candidate_support_ranks: int
    support_span_rank: int
    exact_null_false_positive_probability: float
    rank_union_false_positive_upper_bound: float
    minimum_alternative_acceptance_probability: float
    maximum_alternative_acceptance_residual: float
    equal_prior_support_test_success_probability: float
    equal_prior_helstrom_success_probability: float
    support_test_helstrom_success_gap: float
    minimum_positive_average_projector_eigenvalue: float
    implied_generic_inverse_singular_scale: float
    synthesis_frame_identity_residual: float
    support_span_test_is_helstrom_optimal: bool
    finite_control_verified: bool
    status: str


@dataclass(frozen=True)
class SupportSpanScalingRecord:
    n: int
    conjugacy_class_size: int
    target_null_false_positive: float
    sufficient_copy_count: int
    certified_null_false_positive_upper_bound: float
    alternative_completeness: float
    sample_count_polynomial_in_group_register_length: bool
    least_positive_frame_eigenvalue_certified: bool
    polynomial_range_projector_compiler_known: bool
    status: str


@dataclass(frozen=True)
class HiddenInvolutionSupportSpanTheorem:
    support_test: str
    perfect_completeness: str
    rank_false_positive_bound: str
    synthesis_reduction: str
    implementation_boundary: str
    perfect_alternative_completeness_proved: bool
    logarithmic_sample_upper_bound_proved: bool
    synthesis_frame_identity_proved: bool
    inverse_polynomial_positive_frame_gap_proved: bool
    polynomial_range_projector_compiler_constructed: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class HiddenInvolutionSupportSpanReport:
    created_at: str
    primary_literature: list[dict[str, str]]
    theorem_contract: dict[str, Any]
    finite_controls: list[SupportSpanFiniteControl]
    scaling_records: list[SupportSpanScalingRecord]
    theorem: HiddenInvolutionSupportSpanTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def support_span_sufficient_copies(
    conjugacy_class_size: int,
    null_false_positive: float,
) -> int:
    return support_rank_sufficient_copies(conjugacy_class_size, null_false_positive)


def support_projector(
    positive_operator: np.ndarray,
    *,
    tolerance: float = 1e-10,
) -> tuple[np.ndarray, np.ndarray]:
    eigenvalues, eigenvectors = np.linalg.eigh(
        (positive_operator + positive_operator.conj().T) / 2.0
    )
    if eigenvalues[0] < -100 * tolerance:
        raise ValueError("operator is not positive semidefinite")
    positive = eigenvalues > tolerance
    projector = (
        eigenvectors[:, positive] @ eigenvectors[:, positive].conj().T
        if np.any(positive)
        else np.zeros_like(positive_operator)
    )
    return projector, eigenvalues[positive]


def audit_support_span_control(
    n: int,
    transposition_count: int,
    copy_count: int,
    *,
    maximum_dimension: int = 2048,
) -> SupportSpanFiniteControl:
    null, alternative = dense_binary_states(
        n,
        transposition_count,
        copy_count,
        maximum_dimension=maximum_dimension,
    )
    dimension = null.shape[0]
    class_elements = involution_conjugacy_class(n, transposition_count)
    class_size = len(class_elements)
    average_projector = average_projector_from_dense_alternative(
        alternative, copy_count
    )
    span_projector, positive_values = support_projector(average_projector)
    support_rank = int(round(float(np.trace(span_projector).real)))
    candidate_rank = dimension // (1 << copy_count)
    rank_sum = class_size * candidate_rank
    null_false_positive = float(np.trace(span_projector @ null).real)
    rank_upper = min(1.0, class_size / (1 << copy_count))

    alternative_acceptances = []
    candidate_projector_sum = np.zeros_like(average_projector)
    for hidden in class_elements:
        hidden_state = dense_hidden_coset_state(
            n, hidden, copy_count
        )
        alternative_acceptances.append(
            float(np.trace(span_projector @ hidden_state).real)
        )
        candidate_projector_sum += (
            dimension / (1 << copy_count)
        ) * hidden_state
    candidate_projector_sum /= class_size
    synthesis_residual = float(
        np.linalg.norm(candidate_projector_sum - average_projector, ord=2)
    )

    support_success = 0.5 * (
        min(alternative_acceptances) + 1.0 - null_false_positive
    )
    helstrom_distance = 0.5 * float(
        np.abs(np.linalg.eigvalsh(alternative - null)).sum()
    )
    helstrom_success = 0.5 * (1.0 + helstrom_distance)
    minimum_positive = float(positive_values[0])
    inverse_singular = 1.0 / math.sqrt(minimum_positive)
    optimal = abs(support_success - helstrom_success) <= 1e-9
    acceptance_residual = max(
        abs(value - 1.0) for value in alternative_acceptances
    )
    verified = bool(
        support_rank <= rank_sum
        and null_false_positive <= rank_upper + 1e-9
        and acceptance_residual <= 1e-9
        and synthesis_residual <= 1e-9
        and support_success <= helstrom_success + 1e-9
    )
    return SupportSpanFiniteControl(
        n=n,
        transposition_count=transposition_count,
        copy_count=copy_count,
        conjugacy_class_size=class_size,
        data_dimension=dimension,
        candidate_support_rank=candidate_rank,
        sum_of_candidate_support_ranks=rank_sum,
        support_span_rank=support_rank,
        exact_null_false_positive_probability=null_false_positive,
        rank_union_false_positive_upper_bound=rank_upper,
        minimum_alternative_acceptance_probability=min(
            alternative_acceptances
        ),
        maximum_alternative_acceptance_residual=acceptance_residual,
        equal_prior_support_test_success_probability=support_success,
        equal_prior_helstrom_success_probability=helstrom_success,
        support_test_helstrom_success_gap=(
            helstrom_success - support_success
        ),
        minimum_positive_average_projector_eigenvalue=minimum_positive,
        implied_generic_inverse_singular_scale=inverse_singular,
        synthesis_frame_identity_residual=synthesis_residual,
        support_span_test_is_helstrom_optimal=optimal,
        finite_control_verified=verified,
        status=(
            "support-span-perfect-completeness-rank-bound-verified"
            if verified
            else "support-span-control-failure"
        ),
    )


def support_span_scaling_record(
    n: int,
    *,
    target_null_false_positive: float = 0.1,
) -> SupportSpanScalingRecord:
    if n < 2 or n % 2:
        raise ValueError("n must be positive and even")
    size = involution_class_size(n, n // 2)
    copies = support_span_sufficient_copies(
        size, target_null_false_positive
    )
    upper = size / (1 << copies)
    return SupportSpanScalingRecord(
        n=n,
        conjugacy_class_size=size,
        target_null_false_positive=target_null_false_positive,
        sufficient_copy_count=copies,
        certified_null_false_positive_upper_bound=upper,
        alternative_completeness=1.0,
        sample_count_polynomial_in_group_register_length=True,
        least_positive_frame_eigenvalue_certified=False,
        polynomial_range_projector_compiler_known=False,
        status="published-log-sample-support-test-range-compiler-open",
    )


def build_hidden_involution_support_span_report(
    *,
    finite_specs: tuple[tuple[int, int, int], ...] = (
        (3, 1, 1),
        (3, 1, 2),
        (3, 1, 3),
        (4, 2, 2),
    ),
    scaling_n_values: tuple[int, ...] = (16, 32, 64, 128),
) -> HiddenInvolutionSupportSpanReport:
    controls = [
        audit_support_span_control(n, transpositions, copies)
        for n, transpositions, copies in finite_specs
    ]
    scaling = [support_span_scaling_record(n) for n in scaling_n_values]
    verified = all(row.finite_control_verified for row in controls)
    scaling_verified = all(
        row.certified_null_false_positive_upper_bound
        <= row.target_null_false_positive + 1e-15
        and row.alternative_completeness == 1.0
        for row in scaling
    )
    theorem = HiddenInvolutionSupportSpanTheorem(
        support_test=(
            "T_k is the orthogonal projector onto span_h supp(P_h^tensor k)."
        ),
        perfect_completeness=(
            "supp(rho_h^tensor k) is contained in supp(T_k), so every "
            "alternative is accepted with probability one."
        ),
        rank_false_positive_bound=(
            "rank(T_k)<=sum_h rank(P_h^tensor k)=M|G|^k/2^k, hence "
            "Tr(T_k I/|G|^k)<=M/2^k."
        ),
        synthesis_reduction=(
            "W_k=M^-1/2 sum_h P_h<h| satisfies W_kW_k^*=A_k and "
            "T_k=polar(W_k)polar(W_k)^*."
        ),
        implementation_boundary=(
            "The rank proof has no least-positive-eigenvalue bound and no "
            "uniform representation basis for range(W_k)."
        ),
        perfect_alternative_completeness_proved=True,
        logarithmic_sample_upper_bound_proved=True,
        synthesis_frame_identity_proved=verified,
        inverse_polynomial_positive_frame_gap_proved=False,
        polynomial_range_projector_compiler_constructed=False,
        theorem_verified=verified and scaling_verified,
        status=(
            "published-support-span-test-reduced-to-range-polar-compiler-open"
            if verified and scaling_verified
            else "support-span-reduction-control-failure"
        ),
    )
    metrics: dict[str, int | float] = {
        "finite_control_count": len(controls),
        "finite_control_failure_count": sum(
            not row.finite_control_verified for row in controls
        ),
        "perfect_completeness_control_count": sum(
            row.maximum_alternative_acceptance_residual <= 1e-9
            for row in controls
        ),
        "support_test_helstrom_optimal_control_count": sum(
            row.support_span_test_is_helstrom_optimal for row in controls
        ),
        "scaling_record_count": len(scaling),
        "range_projector_compiler_count": 0,
        "inverse_polynomial_frame_gap_theorem_count": 0,
        "new_sample_complexity_theorem_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return HiddenInvolutionSupportSpanReport(
        created_at=utc_now(),
        primary_literature=[
            {
                "id": "HAYASHI-KAWACHI-KOBAYASHI-2006-HSP-SAMPLE-COMPLEXITY",
                "title": "Quantum Measurements for Hidden Subgroup Problems with Optimal Sample Complexity",
                "url": "https://arxiv.org/abs/quant-ph/0604174",
                "scope": (
                    "Theorem 4 projects onto the span of candidate coset-state "
                    "supports and proves the M/2^k trivial-state error bound."
                ),
            }
        ],
        theorem_contract={
            "access_model": (
                "Independent standard mixed coset states for equal order-two "
                "candidate subgroups."
            ),
            "measurement": (
                "One binary support-span projector with perfect alternative "
                "completeness; no individual-h output."
            ),
            "implementation_scope": (
                "Synthesis-map range projection. A matrix formula or block encoding "
                "is not an efficient polar/range circuit."
            ),
            "non_claim": (
                "No new sample theorem, inverse-polynomial frame gap, polynomial "
                "range projector, GI algorithm, or speedup."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-COSET-BINARY-SUPPORT-RANGE-BASIS",
                "statement": (
                    "Give a polynomial representation-theoretic basis or membership "
                    "test for span_h supp(P_h^tensor k) at k=Theta(log M)."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-BINARY-SUPPORT-POLAR",
                "statement": (
                    "Implement the synthesis-map range projector directly, or prove "
                    "an inverse-polynomial least positive singular value on natural "
                    "source sectors."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-BINARY-SUPPORT-DEQUANTIZATION",
                "statement": (
                    "Test whether support membership is equivalent to a classical "
                    "relation-span, graph invariant, or code invariant."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "The exact Helstrom threshold is the only viable binary test.",
                "answer": (
                    "False. The published support-span projector has perfect "
                    "alternative completeness and logarithmically small null error."
                ),
                "resolved": True,
            },
            {
                "challenge": "The support-span formula is already an efficient circuit.",
                "answer": (
                    "False. Projecting onto the range of an efficient synthesis "
                    "operator requires its polar/range transform or a direct range basis."
                ),
                "resolved": True,
            },
            {
                "challenge": "The rank bound gives a usable singular-value gap.",
                "answer": (
                    "False. It controls only range dimension and is insensitive to "
                    "arbitrarily small positive frame eigenvalues."
                ),
                "resolved": True,
            },
            {
                "challenge": "A small frame eigenvalue proves the range projector hard.",
                "answer": (
                    "False. A structured range basis can bypass generic singular-value "
                    "transformation, so no arbitrary-circuit lower bound follows."
                ),
                "resolved": True,
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "published_support_span_sample_test_recovered": True,
            "sample_complexity_result_new_to_literature": False,
            "perfect_alternative_completeness_proved": True,
            "logarithmic_sample_upper_bound_proved": True,
            "inverse_polynomial_positive_frame_gap_proved": False,
            "polynomial_support_range_projector_constructed": False,
            "support_membership_dequantization_passed": False,
            "polynomial_time_hidden_involution_decision_algorithm": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The known one-sided sample test reduces efficient implementation "
                "to a structured synthesis-range projector; neither a range basis "
                "nor a usable frame gap is known."
            ),
        },
        status=theorem.status,
        summary=(
            "Recovered the published support-span triviality test and reduced its "
            "implementation to the range polar of a controlled-projector synthesis "
            "map. This is a better compiler target than exact Helstrom sign, but no "
            "polynomial range projector is known."
        ),
        falsifiers_triggered=[
            "Exact shifted-likelihood thresholding is not the only binary measurement route.",
            "The support-span rank bound does not supply an efficient range projection.",
            "Published logarithmic sample sufficiency is not a new quantum algorithm.",
        ],
    )


def write_hidden_involution_support_span_report(
    output_path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-COSET-HIDDEN-INVOLUTION-SUPPORT-SPAN-REDUCTION"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    path = output_path
    output_path = output_path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    payload = asdict(build_hidden_involution_support_span_report(**kwargs))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    return payload


if __name__ == "__main__":
    report = write_hidden_involution_support_span_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
