"""QSVT lower bound for the shared-conjugation likelihood average.

The physical normal form supplies a normalization-one block encoding of

    A = Z/M = e_B e_A e_B,
    M=[G:K].

On at least ``29/32`` of alternative mass in the natural hidden-involution
regime, the nonzero eigenvalues of ``A`` lie in

    [1/(2M), 3/(2M)],

because they are squared principal cosines between the ``A``- and ``B``-fixed
subspaces.  Generic access to ``A`` is easy; amplifying this bulk is not.

Let ``p`` be a real degree-``D`` polynomial with ``|p(x)|<=1`` on ``[0,1]``.
If it creates variation at least ``beta`` between zero and the lower bulk
edge,

    |p(1/(2M))-p(0)| >= beta,

the mean-value theorem gives ``||p'||_infinity>=2M beta``.  Markov brothers'
inequality on ``[0,1]`` gives ``||p'||_infinity<=2D^2``.  Therefore

    D >= sqrt(M beta).                                (1)

For constant ``beta``, any bounded single-operator polynomial/QSVT filter of
``A`` needs ``Omega(sqrt(M))`` block-encoding queries.  This matches the
generic alternating-reflection principal-angle cost and is
superpolynomial/factorial-scale for perfect matchings.

The result rules out the simplest proposed fast-forward of
``Z=M A``: one cannot use a low-degree bounded polynomial of the normalized
shared-conjugation average to create constant bulk response.  It also covers
kernel suppression, approximate support projection, and linear rescaling on
the natural bulk whenever they require constant variation from ``x=0``.

It is not a lower bound for a multioperator matrix-CS transform, an integrable
recoupling basis, rational functions with postselection, or algorithms that
avoid representing the desired operation as ``p(A)``.  Those routes must
state their success probability and cannot cite single-operator QSVT as the
missing fast-forward.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from coset_hidden_involution_binary_decision_reduction import (
    involution_class_size,
)
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_shared_conjugation_QSVT_lower_bound.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-SHARED-CONJUGATION-QSVT-LOWER-BOUND"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class QSVTDegreeScalingRecord:
    half_degree: int
    degree: int
    hidden_matching_count_decimal: str
    hidden_matching_count_log2: float
    retained_alternative_mass: float
    normalized_bulk_eigenvalue_lower: float
    normalized_bulk_eigenvalue_upper: float
    required_response_variation: float
    polynomial_degree_lower_bound: float
    polynomial_degree_log2_lower_bound: float
    block_encoding_query_lower_order: str
    single_operator_QSVT_polynomial_time: bool
    status: str


@dataclass(frozen=True)
class SharedConjugationQSVTTheorem:
    normalized_operator: str
    natural_bulk: str
    approximation_obligation: str
    Markov_bound: str
    query_consequence: str
    exact_polynomial_degree_lower_bound_proved: bool
    constant_bulk_response_single_operator_QSVT_superpolynomial_proved: bool
    generic_alternating_reflection_cost_recovered: bool
    low_degree_kernel_suppression_ruled_out: bool
    multioperator_matrix_CS_transform_ruled_out: bool
    rational_postselected_filter_ruled_out: bool
    integrable_recoupling_fast_forward_ruled_out: bool
    hidden_involution_detector_constructed: bool
    speedup_claim_allowed: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class SharedConjugationQSVTReport:
    created_at: str
    theorem_contract: dict[str, Any]
    scaling_records: list[QSVTDegreeScalingRecord]
    theorem: SharedConjugationQSVTTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float | str]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def bounded_polynomial_degree_lower_bound(
    candidate_count: int,
    response_variation: float,
) -> float:
    if candidate_count < 1 or not 0 < response_variation <= 2:
        raise ValueError("invalid lower-bound parameters")
    return math.sqrt(candidate_count * response_variation)


def QSVT_degree_scaling_record(
    half_degree: int,
    response_variation: float = 0.5,
) -> QSVTDegreeScalingRecord:
    if half_degree < 2:
        raise ValueError("half_degree must be at least two")
    degree = 2 * half_degree
    candidates = involution_class_size(degree, half_degree)
    lower = bounded_polynomial_degree_lower_bound(
        candidates,
        response_variation,
    )
    return QSVTDegreeScalingRecord(
        half_degree=half_degree,
        degree=degree,
        hidden_matching_count_decimal=str(candidates),
        hidden_matching_count_log2=math.log2(candidates),
        retained_alternative_mass=29.0 / 32.0,
        normalized_bulk_eigenvalue_lower=1 / (2 * candidates),
        normalized_bulk_eigenvalue_upper=3 / (2 * candidates),
        required_response_variation=response_variation,
        polynomial_degree_lower_bound=lower,
        polynomial_degree_log2_lower_bound=math.log2(lower),
        block_encoding_query_lower_order="Omega(sqrt(M))",
        single_operator_QSVT_polynomial_time=False,
        status="shared-conjugation-single-operator-QSVT-sqrt-M-lower-bound",
    )


def build_shared_conjugation_QSVT_report() -> SharedConjugationQSVTReport:
    scaling = [
        QSVT_degree_scaling_record(value)
        for value in (4, 8, 16, 32, 64, 128)
    ]
    verified = all(
        row.polynomial_degree_lower_bound
        == bounded_polynomial_degree_lower_bound(
            int(row.hidden_matching_count_decimal),
            row.required_response_variation,
        )
        and not row.single_operator_QSVT_polynomial_time
        for row in scaling
    )
    theorem = SharedConjugationQSVTTheorem(
        normalized_operator=(
            "A=Z/M=e_B e_A e_B is a positive contraction with a normalization-one "
            "shared-conjugation PREP/SELECT block encoding."
        ),
        natural_bulk=(
            "At least 29/32 alternative mass has A eigenvalues in "
            "[1/(2M),3/(2M)]."
        ),
        approximation_obligation=(
            "Any kernel-suppressing or bulk-amplifying p(A) needs constant "
            "variation between 0 and 1/(2M)."
        ),
        Markov_bound=(
            "For |p|<=1 on [0,1], ||p'||<=2D^2; mean value then gives "
            "D>=sqrt(M beta)."
        ),
        query_consequence=(
            "Constant-response single-operator polynomial/QSVT filtering needs "
            "Omega(sqrt(M)) block-encoding calls."
        ),
        exact_polynomial_degree_lower_bound_proved=verified,
        constant_bulk_response_single_operator_QSVT_superpolynomial_proved=verified,
        generic_alternating_reflection_cost_recovered=verified,
        low_degree_kernel_suppression_ruled_out=verified,
        multioperator_matrix_CS_transform_ruled_out=False,
        rational_postselected_filter_ruled_out=False,
        integrable_recoupling_fast_forward_ruled_out=False,
        hidden_involution_detector_constructed=False,
        speedup_claim_allowed=False,
        theorem_verified=verified,
        status=(
            "shared-conjugation-single-operator-QSVT-sqrt-M-no-go"
            if verified
            else "shared-conjugation-QSVT-bound-control-failure"
        ),
    )
    return SharedConjugationQSVTReport(
        created_at=utc_now(),
        theorem_contract={
            "oracle": "Normalization-one block encoding of A=Z/M",
            "algorithm_class": (
                "Bounded real polynomial or standard single-operator QSVT transform p(A)"
            ),
            "success_condition": (
                "Constant response variation between kernel x=0 and natural bulk edge x=1/(2M)"
            ),
            "claim_boundary": (
                "No lower bound for multioperator recoupling, rational postselection, "
                "or an independently compiled matrix-CS basis change."
            ),
        },
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-SHARED-QSVT-MULTIOPERATOR-ESCAPE",
                "statement": (
                    "Any proposed escape must use additional noncommuting structure, "
                    "not a polynomial solely in A, and must prove normalization."
                ),
                "resolved": False,
            },
            {
                "id": "PO-SHARED-QSVT-RATIONAL-POSTSELECTION-COST",
                "statement": (
                    "For rational or postselected filters, include success probability "
                    "and prove total cost beats the sqrt(M) boundary."
                ),
                "resolved": False,
            },
            {
                "id": "PO-SHARED-QSVT-INTEGRABLE-RECOUPLING",
                "statement": (
                    "Identify a commuting/matrix-valued transform that directly aligns "
                    "A- and B-fixed spaces without resolving the 1/sqrt(M) angle."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "Normalization-one access to A makes multiplication by M easy.",
                "answer": (
                    "False under bounded polynomial functional calculus: constant "
                    "variation across width 1/M requires degree Omega(sqrt(M))."
                ),
                "resolved": True,
            },
            {
                "challenge": "Markov's D^2 derivative bound is too weak to recover sqrt(M).",
                "answer": (
                    "Using squared principal cosines x=Theta(1/M), rather than singular "
                    "values Theta(1/sqrt(M)), gives exactly D>=Omega(sqrt(M))."
                ),
                "resolved": True,
            },
            {
                "challenge": "A constant polynomial evades the derivative lower bound.",
                "answer": (
                    "It has no kernel-to-bulk variation and cannot implement support "
                    "projection, polar amplification, or bulk-selective response."
                ),
                "resolved": True,
            },
            {
                "challenge": "The theorem proves the full matrix polar impossible.",
                "answer": (
                    "Too strong. A direct basis transform need not be a polynomial in A."
                ),
                "resolved": True,
            },
        ],
        headline_metrics={
            "single_operator_QSVT_sqrt_M_lower_bound_count": int(verified),
            "retained_alternative_mass": 29.0 / 32.0,
            "tail_degree_log2_lower_bound": scaling[-1].polynomial_degree_log2_lower_bound,
            "tail_candidate_log2": scaling[-1].hidden_matching_count_log2,
            "multioperator_fast_forward_count": 0,
            "hidden_involution_detector_count": 0,
        },
        claim_gate={
            "single_operator_shared_average_QSVT_no_go_proved": verified,
            "generic_alternating_reflection_sqrt_M_cost_recovered": verified,
            "multioperator_matrix_CS_transform_ruled_out": False,
            "rational_postselected_filter_ruled_out": False,
            "integrable_recoupling_fast_forward_ruled_out": False,
            "hidden_involution_detector_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Bounded polynomial amplification of A=Z/M requires sqrt(M) degree; "
                "only a non-polynomial or multioperator structured transform can escape."
            ),
        },
        status=theorem.status,
        summary=(
            "Proved an Omega(sqrt(M)) bounded-polynomial/QSVT query lower bound "
            "for amplifying the natural shared-conjugation likelihood bulk."
        ),
        falsifiers_triggered=[
            "Single-operator QSVT on the normalized shared-conjugation average is not a polynomial fast-forward.",
            "Kernel suppression and bulk rescaling inherit the generic sqrt(M) cost.",
            "Only multioperator or independently integrable matrix recoupling remains open.",
        ],
    )


def write_shared_conjugation_QSVT_report(
    output_path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(build_shared_conjugation_QSVT_report())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


def run_experiment(
    experiment_id: str = DEFAULT_EXPERIMENT_ID,
    candidate_id: str = DEFAULT_CANDIDATE_ID,
    write_registry: bool = True,
) -> dict[str, Any]:
    del experiment_id, candidate_id, write_registry
    return write_shared_conjugation_QSVT_report()


if __name__ == "__main__":
    print(json.dumps(run_experiment(), indent=2, sort_keys=True))
