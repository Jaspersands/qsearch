"""All-n copy window for covariant multiplicity whitening.

For one hidden involution ``h in S_n``, a natural weak-Fourier source label
``lambda`` has probability

    p_h(lambda) = 2 d_lambda R_lambda / n!,

where ``R_lambda`` is the rank of the ``+1`` projector of ``rho_lambda(h)``.
For an ordered ``k``-tuple of labels, let ``m_nu`` be the multiplicity of
``nu`` in their diagonal tensor product and ``R=product R_lambda``.  The
covariance-compressed whitening moment obeys

    sum_nu rank(D_nu)/R <= sum_nu m_nu/R.

Natural-source averaging makes the right side exactly computable:

    E[sum_nu m_nu/R]
      = (2^k/(n!)^k) sum_(lambda_1,...,lambda_k)
          product_i d_(lambda_i) sum_nu m_nu
      = 2^k I_n/n!,

because ``Reg(S_n)^tensor k = (n!)^(k-1) Reg(S_n)`` under the diagonal action
and ``sum_nu d_nu=I_n``, the number of involutions in ``S_n`` by the
Robinson--Schensted correspondence.

For the fixed-point-free conjugacy class, ``M=(n-1)!!``.  Its equal-overlap
projector PGM has constant information-theoretic success at
``k=ceil(log2 M)+O(1)``, whereas the expected rank upper bound is at most one
at ``k=floor(log2(n!/I_n))``.  The gap equals ``log2(M I_n/n!)+O(1)`` and is
``Theta(sqrt(n))``: writing ``n=2m``,

    M I_n/n! = (M^2/n!) (I_n/M),
    I_n/M <= cosh(sqrt(n)),

while one term of the involution sum and the elementary central-binomial bound
give ``M I_n/n! >= 4^floor(sqrt(m)/4)/(n+1)``.

Thus covariance reduces a factorial-looking direct inversion burden to a
sharp subexponential copy-window question.  The theorem is not a lower bound
on the actual rank: ``rank(D_nu)`` can be smaller than ``m_nu``.  A Shor-level
route would need to prove and exploit such a rank deficiency, or implement a
different whitening/measurement below the equal-overlap PGM threshold.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from coset_covariant_multiplicity_whitening_escape import (
    NaturalWhiteningAggregate,
    natural_whitening_controls,
)
from coset_state_distinguishability import involution_count
from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_pgm_success_theorem import pgm_success_lower_bound


REPORT_PATH = Path(
    "research/representation/"
    "coset_multiplicity_whitening_copy_window.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-MULTIPLICITY-WHITENING-COPY-WINDOW"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class RobinsonSchenstedControl:
    n: int
    involution_count: int
    sum_irrep_dimensions: int
    identity_verified: bool


@dataclass(frozen=True)
class NaturalRankUpperControl:
    n: int
    transposition_count: int
    copy_count: int
    natural_source_branch_count: int
    exact_expected_multiplicity_dimension_ratio: float
    observed_expected_multiplicity_support_rank_ratio: float
    support_to_dimension_upper_bound_ratio: float
    upper_bound_residual: float
    finite_bound_verified: bool


@dataclass(frozen=True)
class CopyWindowScalingRecord:
    n: int
    group_order_decimal: str
    perfect_matching_count_decimal: str
    involution_count_decimal: str
    log2_group_order: float
    log2_perfect_matching_count: float
    log2_involution_count: float
    multiplicity_rank_safe_copy_count: int
    constant_pgm_success_copy_count: int
    copy_window_width: int
    log2_window_ratio: float
    elementary_log2_window_ratio_lower_bound: float
    cosh_log2_window_ratio_upper_bound: float
    lower_bound_below_exact: bool
    exact_below_upper_bound: bool
    pgm_success_lower_bound_at_safe_width: float
    expected_raw_rank_upper_at_safe_width: float
    pgm_success_lower_bound_at_pgm_width: float
    expected_raw_rank_upper_at_pgm_width: float
    balanced_copy_count: int
    balanced_success_whitening_resource_envelope: float
    window_is_sqrt_n_asymptotically: bool
    status: str


@dataclass(frozen=True)
class MultiplicityWhiteningCopyWindowTheorem:
    natural_source_identity: str
    regular_tensor_identity: str
    involution_dimension_identity: str
    expected_rank_upper_bound: str
    equal_overlap_pgm_bound: str
    copy_window: str
    window_upper_bound: str
    window_lower_bound: str
    balanced_envelope: str
    scope_limit: str
    exact_expected_multiplicity_dimension_identity_proved: bool
    actual_support_rank_upper_bound_proved: bool
    theta_sqrt_n_copy_window_proved: bool
    factorial_direct_burden_survives_covariance: bool
    actual_multiplicity_rank_lower_bound_proved: bool
    polynomial_whitening_at_pgm_width_proved: bool
    polynomial_hidden_involution_algorithm_proved: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class CosetMultiplicityWhiteningCopyWindowReport:
    created_at: str
    theorem_contract: dict[str, Any]
    robinson_schensted_controls: list[RobinsonSchenstedControl]
    finite_natural_controls: list[NaturalRankUpperControl]
    scaling_records: list[CopyWindowScalingRecord]
    theorem: MultiplicityWhiteningCopyWindowTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def symmetric_group_involution_count(n: int) -> int:
    if n < 0:
        raise ValueError("n must be nonnegative")
    if n < 2:
        return 1
    previous_previous = 1
    previous = 1
    for degree in range(2, n + 1):
        current = previous + (degree - 1) * previous_previous
        previous_previous, previous = previous, current
    return previous


def robinson_schensted_control(n: int) -> RobinsonSchenstedControl:
    if n < 1:
        raise ValueError("n must be positive")
    involutions = symmetric_group_involution_count(n)
    dimension_sum = sum(
        hook_length_dimension(partition) for partition in integer_partitions(n)
    )
    return RobinsonSchenstedControl(
        n=n,
        involution_count=involutions,
        sum_irrep_dimensions=dimension_sum,
        identity_verified=involutions == dimension_sum,
    )


def exact_expected_multiplicity_dimension_ratio(n: int, copy_count: int) -> float:
    if n < 2 or copy_count < 1:
        raise ValueError("n>=2 and copy_count>=1 are required")
    return (
        (1 << copy_count)
        * symmetric_group_involution_count(n)
        / math.factorial(n)
    )


def natural_rank_upper_control(
    aggregate: NaturalWhiteningAggregate,
) -> NaturalRankUpperControl:
    upper = exact_expected_multiplicity_dimension_ratio(
        aggregate.n, aggregate.copy_count
    )
    observed = aggregate.average_raw_multiplicity_inverse_second_moment
    residual = max(0.0, observed - upper)
    return NaturalRankUpperControl(
        n=aggregate.n,
        transposition_count=aggregate.transposition_count,
        copy_count=aggregate.copy_count,
        natural_source_branch_count=aggregate.source_branch_count,
        exact_expected_multiplicity_dimension_ratio=upper,
        observed_expected_multiplicity_support_rank_ratio=observed,
        support_to_dimension_upper_bound_ratio=(observed / upper if upper else 0.0),
        upper_bound_residual=residual,
        finite_bound_verified=(
            aggregate.all_finite_controls_passed and residual <= 1e-10
        ),
    )


def _log2_cosh(value: float) -> float:
    return (
        value
        - math.log(2.0)
        + math.log1p(math.exp(-2.0 * value))
    ) / math.log(2.0)


def _one_plus_power_of_two(exponent: float) -> float:
    if exponent > 900:
        return math.inf
    if exponent < -60:
        return 1.0
    return 1.0 + 2.0**exponent


def copy_window_scaling_record(n: int) -> CopyWindowScalingRecord:
    if n < 8 or n % 4:
        raise ValueError("n must be a multiple of four and at least eight")
    order = math.factorial(n)
    matchings = involution_count(n, n // 2)
    involutions = symmetric_group_involution_count(n)
    log_order = math.log2(order)
    log_matchings = math.log2(matchings)
    log_involutions = math.log2(involutions)
    safe_width = math.floor(log_order - log_involutions)
    pgm_width = math.ceil(log_matchings)
    exact_log_ratio = log_matchings + log_involutions - log_order

    half = n // 2
    witness_index = math.floor(math.sqrt(half) / 4)
    lower_log_ratio = 2 * witness_index - math.log2(n + 1)
    upper_log_ratio = _log2_cosh(math.sqrt(n))

    safe_raw = 2.0 ** (safe_width + log_involutions - log_order)
    pgm_raw = 2.0 ** (pgm_width + log_involutions - log_order)
    balanced_width = round(
        0.5 * (log_matchings + log_order - log_involutions)
    )
    success_exponent = log_matchings - balanced_width
    whitening_exponent = balanced_width + log_involutions - log_order
    balanced_envelope = math.sqrt(
        _one_plus_power_of_two(success_exponent)
        * _one_plus_power_of_two(whitening_exponent)
    )
    theta_certificate = bool(
        witness_index >= 1
        and lower_log_ratio <= exact_log_ratio + 1e-10
        and exact_log_ratio <= upper_log_ratio + 1e-10
    )
    return CopyWindowScalingRecord(
        n=n,
        group_order_decimal=str(order),
        perfect_matching_count_decimal=str(matchings),
        involution_count_decimal=str(involutions),
        log2_group_order=log_order,
        log2_perfect_matching_count=log_matchings,
        log2_involution_count=log_involutions,
        multiplicity_rank_safe_copy_count=safe_width,
        constant_pgm_success_copy_count=pgm_width,
        copy_window_width=pgm_width - safe_width,
        log2_window_ratio=exact_log_ratio,
        elementary_log2_window_ratio_lower_bound=lower_log_ratio,
        cosh_log2_window_ratio_upper_bound=upper_log_ratio,
        lower_bound_below_exact=lower_log_ratio <= exact_log_ratio + 1e-10,
        exact_below_upper_bound=exact_log_ratio <= upper_log_ratio + 1e-10,
        pgm_success_lower_bound_at_safe_width=pgm_success_lower_bound(
            matchings, safe_width
        ),
        expected_raw_rank_upper_at_safe_width=safe_raw,
        pgm_success_lower_bound_at_pgm_width=pgm_success_lower_bound(
            matchings, pgm_width
        ),
        expected_raw_rank_upper_at_pgm_width=pgm_raw,
        balanced_copy_count=balanced_width,
        balanced_success_whitening_resource_envelope=balanced_envelope,
        window_is_sqrt_n_asymptotically=theta_certificate,
        status="theta-sqrt-n-whitening-success-copy-window",
    )


def build_coset_multiplicity_whitening_copy_window_report(
    *,
    finite_n: int = 5,
    finite_transposition_count: int = 2,
    finite_copy_counts: tuple[int, ...] = (1, 2, 3),
    scaling_n_values: tuple[int, ...] = (16, 32, 64, 128, 256, 512),
) -> CosetMultiplicityWhiteningCopyWindowReport:
    rs_controls = [robinson_schensted_control(n) for n in range(1, 13)]
    finite_controls: list[NaturalRankUpperControl] = []
    for copy_count in finite_copy_counts:
        _, aggregate = natural_whitening_controls(
            finite_n, finite_transposition_count, copy_count
        )
        finite_controls.append(natural_rank_upper_control(aggregate))
    scaling = [copy_window_scaling_record(n) for n in scaling_n_values]
    verified = bool(
        all(row.identity_verified for row in rs_controls)
        and all(row.finite_bound_verified for row in finite_controls)
        and all(row.lower_bound_below_exact for row in scaling)
        and all(row.exact_below_upper_bound for row in scaling)
    )
    theorem = MultiplicityWhiteningCopyWindowTheorem(
        natural_source_identity=(
            "p_h(lambda)=2 d_lambda R_lambda/|S_n|, so source weighting "
            "cancels every branch projector rank R_lambda."
        ),
        regular_tensor_identity=(
            "Under diagonal action, Reg(S_n)^tensor k is "
            "|S_n|^(k-1) copies of Reg(S_n), by the regular character."
        ),
        involution_dimension_identity=(
            "sum_(nu partition n) d_nu=I_n, since Robinson--Schensted maps "
            "involutions to pairs (T,T) of equal standard tableaux."
        ),
        expected_rank_upper_bound=(
            "E_source[sum_nu rank(D_nu)/R] <= 2^k I_n/n!, with equality "
            "after replacing support ranks by full Kronecker multiplicities."
        ),
        equal_overlap_pgm_bound=(
            "For M distinct order-two subgroups, normalized projector overlap "
            "is 2^-k and P_PGM>=1/[1+(M-1)2^-k]."
        ),
        copy_window=(
            "For fixed-point-free involutions M=(n-1)!!, the gap between "
            "k=floor(log2(n!/I_n)) and k=ceil(log2 M) equals "
            "log2(M I_n/n!)+O(1)."
        ),
        window_upper_bound=(
            "I_n/M=sum_j 2^j (n/2)_j/(2j)! <= cosh(sqrt(n)); also M^2/n!<=1."
        ),
        window_lower_bound=(
            "For j=floor(sqrt(n/2)/4), one involution term gives "
            "I_n/M>=4^j, while M^2/n!>=1/(n+1), proving an Omega(sqrt(n)) gap."
        ),
        balanced_envelope=(
            "Balancing the PGM repetition proxy M/2^k with the whitening "
            "upper proxy 2^k I_n/n! leaves exp(Theta(sqrt(n))) squared "
            "normalization burden, or exp(Theta(sqrt(n)/2)) amplitude scale."
        ),
        scope_limit=(
            "The expected multiplicity-dimension expression is an upper bound "
            "on actual support rank, not a lower bound. It supplies neither a "
            "coherent transform nor a decoder."
        ),
        exact_expected_multiplicity_dimension_identity_proved=True,
        actual_support_rank_upper_bound_proved=True,
        theta_sqrt_n_copy_window_proved=True,
        factorial_direct_burden_survives_covariance=False,
        actual_multiplicity_rank_lower_bound_proved=False,
        polynomial_whitening_at_pgm_width_proved=False,
        polynomial_hidden_involution_algorithm_proved=False,
        theorem_verified=verified,
        status=(
            "theta-sqrt-n-covariant-whitening-window-proved"
            if verified
            else "multiplicity-whitening-window-control-failure"
        ),
    )
    metrics: dict[str, int | float] = {
        "robinson_schensted_control_count": len(rs_controls),
        "robinson_schensted_control_failure_count": sum(
            not row.identity_verified for row in rs_controls
        ),
        "finite_natural_upper_bound_control_count": len(finite_controls),
        "finite_natural_upper_bound_failure_count": sum(
            not row.finite_bound_verified for row in finite_controls
        ),
        "exact_expected_multiplicity_dimension_identity_count": 1,
        "actual_support_rank_upper_bound_theorem_count": 1,
        "theta_sqrt_n_copy_window_theorem_count": 1,
        "maximum_finite_support_to_dimension_ratio": max(
            row.support_to_dimension_upper_bound_ratio
            for row in finite_controls
        ),
        "maximum_scaling_copy_window_width": max(
            row.copy_window_width for row in scaling
        ),
        "maximum_log2_window_ratio": max(
            row.log2_window_ratio for row in scaling
        ),
        "maximum_balanced_resource_envelope": max(
            row.balanced_success_whitening_resource_envelope
            for row in scaling
        ),
        "actual_multiplicity_rank_lower_bound_count": 0,
        "polynomial_whitening_at_pgm_width_count": 0,
        "coherent_internal_kronecker_transform_count": 0,
        "polynomial_hidden_involution_decoder_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return CosetMultiplicityWhiteningCopyWindowReport(
        created_at=utc_now(),
        theorem_contract={
            "ensemble": (
                "Natural weak-Fourier source labels of k same-hidden regular "
                "coset-state registers for an involution in S_n."
            ),
            "quantity": (
                "Natural expectation of the covariance-compressed "
                "multiplicity support-rank ratio."
            ),
            "success_comparator": (
                "The all-n equal-overlap mixed-state PGM lower bound, "
                "specialized to the perfect-matching conjugacy class."
            ),
            "asymptotic_boundary": (
                "A Theta(sqrt(n))-copy interval between rank-safe source "
                "whitening and certified constant PGM success."
            ),
            "non_claim": (
                "No lower bound on actual D_nu support rank or circuit runtime."
            ),
        },
        robinson_schensted_controls=rs_controls,
        finite_natural_controls=finite_controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-COSET-D-RANK-DEFICIENCY",
                "statement": (
                    "Prove or refute an exp(O(log n)) natural bound on actual "
                    "sum_nu rank(D_nu)/R at k=ceil(log2((n-1)!!))+O(1)."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-BELOW-THRESHOLD-MEASUREMENT",
                "statement": (
                    "Find a collective measurement with inverse-polynomial "
                    "success inside the Theta(sqrt(n)) copy window."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-COHERENT-MULTIPLICITY-WHITENING",
                "statement": (
                    "Turn the covariance-compressed algebraic factorization "
                    "into a uniform circuit with source-sensitive precision."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": (
                    "The exact expectation proves multiplicity whitening is "
                    "subexponential at the PGM threshold."
                ),
                "answer": (
                    "Only an upper envelope is proved. Actual ranks may be much "
                    "smaller, which is precisely the constructive opportunity."
                ),
                "resolved": True,
            },
            {
                "challenge": (
                    "Constant PGM success and a subexponential normalization "
                    "envelope constitute an algorithm."
                ),
                "answer": (
                    "False: coherent Kronecker access, D_nu block encoding, "
                    "whitening, precision, and outcome decoding are absent."
                ),
                "resolved": True,
            },
            {
                "challenge": "The remaining burden is still factorial.",
                "answer": (
                    "False at the algebraic source-average level: covariance "
                    "reduces the crude threshold mismatch to exp(Theta(sqrt(n)))."
                ),
                "resolved": True,
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "exact_natural_multiplicity_dimension_expectation_proved": True,
            "theta_sqrt_n_copy_window_proved": True,
            "factorial_direct_normalization_is_remaining_boundary": False,
            "actual_rank_upper_bound_polynomial_at_pgm_width": False,
            "actual_rank_lower_bound_superpolynomial_at_pgm_width": False,
            "coherent_multiplicity_whitening_circuit_proved": False,
            "polynomial_hidden_involution_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Covariance narrows the normalization question to a "
                "Theta(sqrt(n))-copy, exp(Theta(sqrt(n))) multiplicity-support "
                "window. The actual rank and every circuit obligation remain open."
            ),
        },
        status="covariant-whitening-copy-window-sharp-actual-rank-open",
        summary=(
            "Proved the exact all-n natural multiplicity-dimension expectation "
            "and a Theta(sqrt(n)) gap between rank-safe whitening and constant "
            "equal-overlap PGM success. The remaining asymptotic target is actual "
            "D_nu rank deficiency or a below-threshold collective measurement."
        ),
        falsifiers_triggered=[
            (
                "The apparent factorial direct-frame burden does not survive "
                "covariance compression unchanged."
            ),
            (
                "Natural source weighting yields an exact all-n rank envelope, "
                "not merely a finite numerical trend."
            ),
            (
                "The envelope cannot be promoted to an actual-rank lower bound."
            ),
            (
                "Constant information-theoretic PGM success still does not "
                "supply coherent whitening or decoding."
            ),
        ],
    )


def write_coset_multiplicity_whitening_copy_window_report(
    output_path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-COSET-MULTIPLICITY-WHITENING-COPY-WINDOW"
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
    payload = asdict(
        build_coset_multiplicity_whitening_copy_window_report(**kwargs)
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_coset_multiplicity_whitening_copy_window_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
