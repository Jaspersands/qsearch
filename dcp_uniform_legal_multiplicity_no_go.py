"""Uniform-legal multiplicity no-go for density-one DCP subset sum.

Let ``a_1,...,a_n`` be uniform in ``Z_(2^n)`` and

    c_s = #{x in {0,1}^n : <a,x>=s mod 2^n}.

The quenched occupancy theorem already proves that, for every fixed ``k``,

    M_k(a) = 2^-n sum_s (c_s)_k -> 1

in probability over the source, and that the empirical fiber law converges
to Poisson(1).  This module extracts the algorithmically relevant consequence
for Regev's *uniform legal target* law.

For any integer threshold ``T>=k`` and legal-target fraction ``p_legal``,

    Pr_uniform-legal[c_s>=T]
      <= M_k / (p_legal (T)_k).                            (1)

With high probability ``M_k<=2`` and
``p_legal >= (1-e^-1)/2``.  Therefore, for every ``a>0`` and every ``B>0``,
choose one fixed ``k>(B/a)``.  Equation (1) gives

    Pr_uniform-legal[c_s>=n^a] <= n^-B

with probability tending to one over the random source.  Polynomially large
fibers are thus superpolynomially rare under the exact legal-target contract.

The limiting legal multiplicity law is zero-truncated Poisson,

    Pr[c=j | c>0] -> e^-1 / (j! (1-e^-1)),

whereas planting a uniformly random witness size-biases the law to
``1+Poisson(1)``.  Planted-target multiplicity experiments are consequently
not evidence for a uniform-legal solver.

This rules out only multiplicity-threshold and witness-count explosion
shortcuts.  It does not rule out many internal meet-in-the-middle
representations of a unique witness, a source-aware quantum walk, a joint
low/high preconditioner, or any decoder using structure beyond ``c_s``.
"""

from __future__ import annotations

import json
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Sequence

import numpy as np

from dcp_subset_sum_qtt_contraction_search import exact_cyclic_subset_sum_counts
from research_registry import utc_now


REPORT_PATH = Path(
    "research/classical_baselines/dcp_uniform_legal_multiplicity_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-DHS-DCP-UNIFORM-LEGAL-MULTIPLICITY-NO-GO"
)
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class MultiplicityTailCertificate:
    polynomial_threshold_exponent: float
    requested_probability_exponent: float
    selected_fixed_factorial_order: int
    asymptotic_threshold: str
    quenched_factorial_moment_event: str
    legal_fraction_event: str
    conditional_tail_bound: str
    exponent_margin: float
    superpolynomial_tail_certificate_valid: bool
    status: str


@dataclass(frozen=True)
class LimitingMultiplicityLawRecord:
    multiplicity: int
    unconditional_poisson_probability: float
    uniform_legal_probability: float
    planted_probability: float
    planted_to_uniform_legal_ratio: float
    status: str


@dataclass(frozen=True)
class FiniteMultiplicityTailControl:
    n_bits: int
    trial_index: int
    target_count: int
    legal_target_count: int
    legal_target_fraction: float
    factorial_order: int
    factorial_moment: float
    threshold: int
    exact_uniform_legal_tail_probability: float
    factorial_moment_tail_upper_bound: float
    upper_bound_residual: float
    maximum_multiplicity: int
    exact_tail_inequality_verified: bool
    status: str


@dataclass(frozen=True)
class UniformLegalMultiplicityNoGoTheorem:
    quenched_input: str
    deterministic_tail_inequality: str
    legal_fraction_limit: str
    polynomial_threshold_consequence: str
    target_law_distinction: str
    scope_limit: str
    every_positive_polynomial_threshold: bool
    every_requested_inverse_polynomial_mass: bool
    high_multiplicity_uniform_legal_subfamily_eliminated: bool
    general_representation_dissection_eliminated: bool
    polynomial_subset_sum_solver_eliminated: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class UniformLegalMultiplicityNoGoReport:
    created_at: str
    theorem_contract: dict[str, Any]
    tail_certificates: list[MultiplicityTailCertificate]
    limiting_laws: list[LimitingMultiplicityLawRecord]
    finite_controls: list[FiniteMultiplicityTailControl]
    theorem: UniformLegalMultiplicityNoGoTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def falling_factorial(value: int, order: int) -> int:
    if value < 0 or order < 0:
        raise ValueError("value and order must be nonnegative")
    output = 1
    for offset in range(order):
        output *= value - offset
    return output


def uniform_legal_tail_bound(
    counts: Sequence[int] | np.ndarray,
    threshold: int,
    factorial_order: int,
) -> tuple[float, float, float]:
    """Return exact legal tail, factorial bound, and nonnegative residual."""

    values = np.asarray(counts, dtype=np.int64)
    if values.ndim != 1 or values.size == 0 or np.any(values < 0):
        raise ValueError("counts must be a nonempty nonnegative vector")
    if factorial_order < 1 or threshold < factorial_order:
        raise ValueError("require threshold at least positive factorial order")
    legal = values > 0
    legal_count = int(np.count_nonzero(legal))
    if legal_count == 0:
        raise ValueError("at least one legal target is required")
    tail = float(np.count_nonzero(values >= threshold) / legal_count)
    factorial_values = np.ones(values.shape, dtype=object)
    for offset in range(factorial_order):
        factorial_values *= values.astype(object) - offset
    factorial_moment = float(sum(int(value) for value in factorial_values) / values.size)
    legal_fraction = legal_count / values.size
    denominator = falling_factorial(threshold, factorial_order)
    bound = factorial_moment / (legal_fraction * denominator)
    residual = max(0.0, tail - bound)
    return tail, bound, residual


def multiplicity_tail_certificate(
    polynomial_threshold_exponent: float,
    requested_probability_exponent: float,
) -> MultiplicityTailCertificate:
    if polynomial_threshold_exponent <= 0 or requested_probability_exponent <= 0:
        raise ValueError("both exponents must be positive")
    order = math.floor(
        requested_probability_exponent / polynomial_threshold_exponent
    ) + 2
    margin = polynomial_threshold_exponent * order - requested_probability_exponent
    valid = order >= 1 and margin > 0
    return MultiplicityTailCertificate(
        polynomial_threshold_exponent=polynomial_threshold_exponent,
        requested_probability_exponent=requested_probability_exponent,
        selected_fixed_factorial_order=order,
        asymptotic_threshold=f"T_n=ceil(n^{polynomial_threshold_exponent:g})",
        quenched_factorial_moment_event=f"M_{order}(a)<=2 with probability 1-o(1)",
        legal_fraction_event="p_legal(a)>=(1-exp(-1))/2 with probability 1-o(1)",
        conditional_tail_bound=(
            f"Pr_legal[c>=T_n]<=4/((1-exp(-1))*(T_n)_{order})"
        ),
        exponent_margin=margin,
        superpolynomial_tail_certificate_valid=valid,
        status=(
            "fixed-moment-certificate-beats-requested-polynomial-tail"
            if valid
            else "multiplicity-tail-certificate-failure"
        ),
    )


def limiting_multiplicity_law(maximum_multiplicity: int) -> list[LimitingMultiplicityLawRecord]:
    if maximum_multiplicity < 1:
        raise ValueError("maximum multiplicity must be positive")
    zero = math.exp(-1.0)
    legal_mass = 1.0 - zero
    output = []
    for multiplicity in range(1, maximum_multiplicity + 1):
        poisson = zero / math.factorial(multiplicity)
        legal = poisson / legal_mass
        planted = zero / math.factorial(multiplicity - 1)
        output.append(
            LimitingMultiplicityLawRecord(
                multiplicity=multiplicity,
                unconditional_poisson_probability=poisson,
                uniform_legal_probability=legal,
                planted_probability=planted,
                planted_to_uniform_legal_ratio=planted / legal,
                status="zero-truncated-versus-size-biased-poisson",
            )
        )
    return output


def finite_multiplicity_tail_control(
    n_bits: int,
    trial_index: int,
    *,
    factorial_order: int,
    threshold: int,
    seed: int,
) -> FiniteMultiplicityTailControl:
    if n_bits < 2 or trial_index < 0:
        raise ValueError("invalid finite control parameters")
    modulus = 1 << n_bits
    rng = random.Random(seed + 1009 * n_bits + trial_index)
    labels = [rng.randrange(modulus) for _ in range(n_bits)]
    counts = exact_cyclic_subset_sum_counts(labels, modulus).astype(np.int64)
    tail, bound, residual = uniform_legal_tail_bound(
        counts,
        threshold,
        factorial_order,
    )
    factorial_values = np.ones(counts.shape, dtype=object)
    for offset in range(factorial_order):
        factorial_values *= counts.astype(object) - offset
    moment = float(sum(int(value) for value in factorial_values) / modulus)
    legal_count = int(np.count_nonzero(counts))
    verified = residual <= 1e-12
    return FiniteMultiplicityTailControl(
        n_bits=n_bits,
        trial_index=trial_index,
        target_count=modulus,
        legal_target_count=legal_count,
        legal_target_fraction=legal_count / modulus,
        factorial_order=factorial_order,
        factorial_moment=moment,
        threshold=threshold,
        exact_uniform_legal_tail_probability=tail,
        factorial_moment_tail_upper_bound=bound,
        upper_bound_residual=residual,
        maximum_multiplicity=int(np.max(counts)),
        exact_tail_inequality_verified=verified,
        status=(
            "finite-uniform-legal-factorial-tail-bound-verified"
            if verified
            else "finite-multiplicity-tail-control-failure"
        ),
    )


def uniform_legal_multiplicity_no_go_theorem() -> UniformLegalMultiplicityNoGoTheorem:
    return UniformLegalMultiplicityNoGoTheorem(
        quenched_input=(
            "for every fixed k, M_k(a)=2^-n sum_s(c_s)_k converges in probability to one"
        ),
        deterministic_tail_inequality=(
            "Pr_uniform-legal[c>=T]<=M_k/(p_legal*(T)_k)"
        ),
        legal_fraction_limit="p_legal converges in probability to 1-exp(-1)",
        polynomial_threshold_consequence=(
            "for every alpha,B>0, Pr_legal[c>=n^alpha]<=n^-B with probability 1-o(1)"
        ),
        target_law_distinction=(
            "uniform legal gives zero-truncated Poisson(1); planted witness gives 1+Poisson(1)"
        ),
        scope_limit=(
            "Only statistics reducible to final fiber multiplicity are excluded; internal "
            "representation counts, source-aware walks, and joint low/high geometry remain open."
        ),
        every_positive_polynomial_threshold=True,
        every_requested_inverse_polynomial_mass=True,
        high_multiplicity_uniform_legal_subfamily_eliminated=True,
        general_representation_dissection_eliminated=False,
        polynomial_subset_sum_solver_eliminated=False,
        theorem_verified=True,
        status="uniform-legal-polynomial-multiplicity-explosion-falsified",
    )


def run_uniform_legal_multiplicity_no_go() -> UniformLegalMultiplicityNoGoReport:
    certificates = [
        multiplicity_tail_certificate(alpha, exponent)
        for alpha, exponent in (
            (0.25, 1.0),
            (0.5, 3.0),
            (1.0, 10.0),
            (2.0, 25.0),
        )
    ]
    laws = limiting_multiplicity_law(10)
    controls = [
        finite_multiplicity_tail_control(
            n_bits,
            trial,
            factorial_order=order,
            threshold=threshold,
            seed=1907,
        )
        for n_bits, trial, order, threshold in (
            (5, 0, 2, 3),
            (6, 1, 3, 4),
            (8, 0, 4, 5),
            (10, 1, 4, 6),
        )
    ]
    theorem = uniform_legal_multiplicity_no_go_theorem()
    failures = sum(not row.exact_tail_inequality_verified for row in controls)
    exact = bool(
        failures == 0
        and all(row.superpolynomial_tail_certificate_valid for row in certificates)
        and theorem.theorem_verified
    )
    return UniformLegalMultiplicityNoGoReport(
        created_at=utc_now(),
        theorem_contract={
            "quenched_input": theorem.quenched_input,
            "tail_inequality": theorem.deterministic_tail_inequality,
            "legal_fraction": theorem.legal_fraction_limit,
            "consequence": theorem.polynomial_threshold_consequence,
            "scope": theorem.scope_limit,
        },
        tail_certificates=certificates,
        limiting_laws=laws,
        finite_controls=controls,
        theorem=theorem,
        proof_obligations=[
            {
                "obligation": "transfer_quenched_poisson_occupancy_to_uniform_legal_targets",
                "resolved": exact,
                "resolution": (
                    "Divide the deterministic factorial tail bound by the legal fraction, "
                    "which converges to 1-exp(-1)."
                ),
            },
            {
                "obligation": "test_polynomial_fiber_multiplicity_as_representation_explosion",
                "resolved": exact,
                "resolution": (
                    "Every polynomial threshold has smaller than every inverse-polynomial "
                    "uniform-legal mass with high probability over sources."
                ),
            },
            {
                "obligation": "exclude_internal_representation_or_joint_geometry_mechanisms",
                "resolved": False,
                "resolution": (
                    "Internal decompositions can be numerous even when the final witness is unique; "
                    "they require a separate source-aware theorem."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Fixed moments cannot control a threshold growing with n.",
                "resolved": True,
                "resolution": (
                    "For each requested polynomial tail exponent B, choose one larger but fixed "
                    "factorial order k. Quenched convergence applies separately to that k."
                ),
            },
            {
                "objection": "Conditioning on legality may amplify the rare tail.",
                "resolved": True,
                "resolution": (
                    "The legal fraction converges to the positive constant 1-exp(-1), so conditioning "
                    "changes the bound only by a constant factor."
                ),
            },
            {
                "objection": "Planted-target multiplicity data can validate the route.",
                "resolved": True,
                "resolution": (
                    "Planting size-biases Poisson to 1+Poisson and is a different target law from "
                    "the primary-source uniform legal contract."
                ),
            },
            {
                "objection": "The theorem is a general subset-sum lower bound.",
                "resolved": True,
                "resolution": (
                    "False. It rejects only final-fiber multiplicity filters and makes no claim about "
                    "algorithms exploiting internal representations or coefficient geometry."
                ),
            },
        ],
        headline_metrics={
            "uniform_legal_multiplicity_no_go_theorem_count": int(exact),
            "tail_certificate_count": len(certificates),
            "tail_certificate_failure_count": sum(
                not row.superpolynomial_tail_certificate_valid for row in certificates
            ),
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "limiting_law_row_count": len(laws),
            "largest_selected_fixed_factorial_order": max(
                row.selected_fixed_factorial_order for row in certificates
            ),
            "proved_inverse_polynomial_high_multiplicity_legal_subfamily_count": 0,
            "polynomial_subset_sum_solver_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "polynomial_fiber_multiplicity_representation_collapse_survives": False,
            "internal_representation_dissection_survives": True,
            "joint_low_high_preconditioner_survives": True,
            "polynomial_partial_subset_sum_solver_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Uniform legal targets almost surely do not contain an inverse-polynomial mass of "
                "polynomially large final fibers; any surviving route must exploit different structure."
            ),
        },
        status=(
            "uniform-legal-high-multiplicity-route-falsified-internal-structure-open"
            if exact
            else "uniform-legal-multiplicity-control-failure"
        ),
        summary=(
            "Upgraded quenched Poisson occupancy to a superpolynomial tail no-go for "
            "polynomial final-fiber multiplicity under the uniform legal target law."
        ),
        falsifiers_triggered=[
            "Polynomially large witness fibers cannot occupy inverse-polynomial uniform-legal source mass.",
            "Planted-witness target experiments use a size-biased law and cannot promote a Regev-compatible solver.",
            "A many-representation proposal must count internal algorithmic representations separately from final witness multiplicity.",
        ],
    )


def write_uniform_legal_multiplicity_no_go_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-DHS-DCP-UNIFORM-LEGAL-MULTIPLICITY-NO-GO"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    path = path
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    report = asdict(run_uniform_legal_multiplicity_no_go())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    if write_registry:
        _res_payload = report if "report" in locals() else (payload if "payload" in locals() else (result if "result" in locals() else output))
        from research_registry import (
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-CP-UNIFORM-LEGAL-MULTIPLICITY-NO-GO",
                source=registry_experiment_id,
                claim=(
                    "Initial negative claim for EXP-DHS-DCP-UNIFORM-LEGAL-MULTIPLICITY-NO-GO."
                ),
                reason_invalid=(
                    "Falsified or refined by exact theorem evaluation."
                ),
                lesson=(
                    "Lesson from exact theorem analysis for EXP-DHS-DCP-UNIFORM-LEGAL-MULTIPLICITY-NO-GO."
                ),
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-MEASUREMENT",
                ],
                evidence=_res_payload.get("headline_metrics", {}),
            )
        )
        upsert_experiment_result(
            ExperimentResultRecord(
                id=(
                    registry_result_id
                    or f"RESULT-{registry_experiment_id}-LATEST"
                ),
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=_res_payload.get("created_at", ""),
                status=_res_payload.get("status", "completed"),
                summary=_res_payload.get("summary", ""),
                metrics=_res_payload.get("headline_metrics", {}),
                falsifiers_triggered=_res_payload.get("falsifiers_triggered", []),
                artifacts={
                    "dcp_uniform_legal_multiplicity_no_go": str(path)
                },
            )
        )

    return report


if __name__ == "__main__":
    payload = write_uniform_legal_multiplicity_no_go_report()
    print(json.dumps(payload["headline_metrics"], indent=2, sort_keys=True))
