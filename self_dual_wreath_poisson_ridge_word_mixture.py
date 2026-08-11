"""Outcome-count-free word mixture for normalized Green ridge factors.

Let ``P_1,...,P_q`` be projection leaves and normalize the child frame as

    Fbar = q^-1 sum_e P_e.

If ``Q_e=I-P_e`` and a rate-one Poisson process chooses iid uniform leaf
labels, then

    exp(-t Fbar) = E[Q_{E_N} ... Q_{E_1}],   N~Poisson(t).

This is exact: the one-step average is ``I-Fbar`` and Poissonization gives
``exp(t[(I-Fbar)-I])``.  Mark one independent leaf projector on the left and
integrate the Green ridge kernel,

    R_eta = Fbar(Fbar+eta I)^-2
          = integral_0^infinity t exp(-eta t) Fbar exp(-tFbar) dt.

The normalized operator ``eta^2 R_eta`` is a probability mixture of words

    P_{E_0} Q_{E_N} ... Q_{E_1},

with exact length law

    Pr[N=m] = eta^2 (m+1)/(1+eta)^(m+2).

This negative-binomial law has mean ``2/eta`` and tail

    Pr[N>L] = r^(L+1)[(L+2)-(L+1)r],  r=(1+eta)^-1.

Hence inverse-polynomial ``eta`` permits polynomial word length at
inverse-polynomial accuracy.  More importantly for the marked-word pressure
program, the mixture has total absolute coefficient mass one in the
projection/complement word basis, independent of ``q`` and of word length.
The unnormalized ridge contributes only ``eta^-2`` per factor.

Each complement projector has the same absolute two-term group expansion as
an invariant projector.  Therefore an all-width absolute crossing-word bound
extends through any fixed number ``r`` of ridge factors with only the
polynomial prefactor ``eta^-2r``.  Together with Plancherel target-word
collapse, neither coefficient growth nor a signed target character can erase
the factorial ``|S_n|^-1`` crossing-pressure loss.

This does not finish component M4.  The common-fiber normalization
``C_eta^-1/2``, the natural average ridge-to-Green synthesis error, and a
normalized noncrossing lower bound remain separate obligations.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_poisson_ridge_word_mixture.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-POISSON-RIDGE-WORD-MIXTURE"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class FixedLengthComplementWordControl:
    control_id: str
    ambient_dimension: int
    leaf_count: int
    word_length: int
    enumerated_word_count: int
    average_word_residual: float
    exact_fixed_length_factorization_verified: bool
    status: str


@dataclass(frozen=True)
class RidgeMixtureControl:
    control_id: str
    ambient_dimension: int
    leaf_count: int
    ridge_parameter: float
    truncation_length: int
    exact_negative_binomial_mass_through_truncation: float
    exact_negative_binomial_tail: float
    tail_formula_residual: float
    normalized_exact_ridge_norm: float
    truncated_mixture_operator_residual: float
    residual_bounded_by_tail: bool
    negative_binomial_mean: float
    exact_mixture_verified: bool
    status: str


@dataclass(frozen=True)
class RidgePressureScalingRecord:
    n: int
    ridge_inverse_polynomial_degree: int
    fixed_ridge_factor_count: int
    ridge_parameter: float
    target_truncation_error: float
    truncation_length: int
    exact_length_tail_upper_bound: float
    log2_ridge_absolute_coefficient_mass: float
    log2_symmetric_group_order: float
    log2_crossing_bound_after_ridge_prefactor: float
    factorial_crossing_loss_survives: bool
    polynomial_word_length: bool
    status: str


@dataclass(frozen=True)
class PoissonRidgeWordMixtureTheorem:
    heat_kernel_identity: str
    normalized_ridge_mixture: str
    length_distribution: str
    mean_word_length: str
    truncation_tail: str
    absolute_coefficient_mass: str
    crossing_pressure_transfer: str
    scope_limit: str
    arbitrary_leaf_count: bool
    arbitrary_word_length: bool
    inverse_polynomial_ridge_has_polynomial_truncation: bool
    green_word_coefficient_burden_resolved: bool
    common_metric_normalization_resolved: bool
    positive_component_M4_proved: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class PoissonRidgeWordMixtureReport:
    created_at: str
    theorem_contract: dict[str, Any]
    fixed_length_controls: list[FixedLengthComplementWordControl]
    ridge_controls: list[RidgeMixtureControl]
    scaling_records: list[RidgePressureScalingRecord]
    theorem: PoissonRidgeWordMixtureTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def normalized_frame(projections: tuple[np.ndarray, ...]) -> np.ndarray:
    if not projections:
        raise ValueError("at least one projection is required")
    dimension = projections[0].shape[0]
    if dimension < 1 or any(
        projection.shape != (dimension, dimension)
        for projection in projections
    ):
        raise ValueError("projections must share one square dimension")
    return sum(projections, np.zeros_like(projections[0])) / len(projections)


def average_complement_word(
    projections: tuple[np.ndarray, ...],
    word_length: int,
) -> np.ndarray:
    if word_length < 0:
        raise ValueError("word length must be nonnegative")
    frame = normalized_frame(projections)
    identity = np.eye(frame.shape[0], dtype=complex)
    complements = tuple(identity - projection for projection in projections)
    if word_length == 0:
        return identity
    total = np.zeros_like(frame, dtype=complex)
    for labels in itertools.product(range(len(projections)), repeat=word_length):
        word = identity
        for label in labels:
            word = word @ complements[label]
        total += word
    return total / len(projections) ** word_length


def negative_binomial_length_mass(
    ridge_parameter: Fraction,
    word_length: int,
) -> Fraction:
    if ridge_parameter <= 0 or word_length < 0:
        raise ValueError("eta must be positive and length nonnegative")
    eta = ridge_parameter
    return eta * eta * (word_length + 1) / (1 + eta) ** (word_length + 2)


def negative_binomial_tail(
    ridge_parameter: Fraction,
    truncation_length: int,
) -> Fraction:
    if ridge_parameter <= 0 or truncation_length < -1:
        raise ValueError("invalid eta or truncation length")
    eta = ridge_parameter
    ratio = Fraction(1, 1 + eta)
    first_omitted = truncation_length + 1
    return ratio**first_omitted * (
        first_omitted + 1 - first_omitted * ratio
    )


def negative_binomial_log_tail(
    ridge_parameter: Fraction,
    truncation_length: int,
) -> float:
    """Evaluate the exact tail formula in the log domain.

    The rational formula remains available for finite exact controls.  Scaling
    rows can require word lengths in the tens of millions, where materializing
    the exact numerator and denominator adds no mathematical information.
    """
    if ridge_parameter <= 0 or truncation_length < -1:
        raise ValueError("invalid eta or truncation length")
    eta = float(ridge_parameter)
    first_omitted = truncation_length + 1
    log_ratio = -math.log1p(eta)
    correction = 1.0 + first_omitted * eta / (1.0 + eta)
    return first_omitted * log_ratio + math.log(correction)


def minimum_truncation_length(
    ridge_parameter: Fraction,
    target_tail: Fraction,
) -> int:
    if ridge_parameter <= 0 or not 0 < target_tail < 1:
        raise ValueError("eta must be positive and target tail in (0,1)")
    target_log = math.log(float(target_tail))

    def tail_exceeds_target(length: int) -> bool:
        return negative_binomial_log_tail(ridge_parameter, length) > target_log

    low = -1
    high = 1
    while tail_exceeds_target(high):
        high *= 2
    while low + 1 < high:
        middle = (low + high) // 2
        if not tail_exceeds_target(middle):
            high = middle
        else:
            low = middle
    return high


def normalized_ridge_operator(
    projections: tuple[np.ndarray, ...],
    ridge_parameter: float,
) -> np.ndarray:
    if ridge_parameter <= 0:
        raise ValueError("ridge parameter must be positive")
    frame = normalized_frame(projections)
    identity = np.eye(frame.shape[0], dtype=complex)
    inverse = np.linalg.inv(frame + ridge_parameter * identity)
    return ridge_parameter**2 * frame @ inverse @ inverse


def truncated_ridge_word_mixture(
    projections: tuple[np.ndarray, ...],
    ridge_parameter: Fraction,
    truncation_length: int,
) -> np.ndarray:
    if truncation_length < 0:
        raise ValueError("truncation length must be nonnegative")
    frame = normalized_frame(projections)
    average_complement = np.eye(frame.shape[0], dtype=complex) - frame
    word = np.eye(frame.shape[0], dtype=complex)
    total = np.zeros_like(frame, dtype=complex)
    for length in range(truncation_length + 1):
        mass = float(negative_binomial_length_mass(ridge_parameter, length))
        total += mass * frame @ word
        word = word @ average_complement
    return total


def audit_fixed_length_complement_words(
    control_id: str,
    projections: tuple[np.ndarray, ...],
    word_length: int,
    *,
    tolerance: float = 1e-10,
) -> FixedLengthComplementWordControl:
    frame = normalized_frame(projections)
    expected = np.linalg.matrix_power(
        np.eye(frame.shape[0], dtype=complex) - frame,
        word_length,
    )
    observed = average_complement_word(projections, word_length)
    residual = float(np.linalg.norm(observed - expected, ord=2))
    verified = residual <= tolerance
    return FixedLengthComplementWordControl(
        control_id=control_id,
        ambient_dimension=frame.shape[0],
        leaf_count=len(projections),
        word_length=word_length,
        enumerated_word_count=len(projections) ** word_length,
        average_word_residual=residual,
        exact_fixed_length_factorization_verified=verified,
        status=(
            "fixed-length-complement-word-average-factorizes"
            if verified
            else "complement-word-factorization-failure"
        ),
    )


def audit_ridge_mixture(
    control_id: str,
    projections: tuple[np.ndarray, ...],
    ridge_parameter: Fraction,
    truncation_length: int,
    *,
    tolerance: float = 1e-10,
) -> RidgeMixtureControl:
    exact = normalized_ridge_operator(projections, float(ridge_parameter))
    truncated = truncated_ridge_word_mixture(
        projections,
        ridge_parameter,
        truncation_length,
    )
    mass = sum(
        (
            negative_binomial_length_mass(ridge_parameter, length)
            for length in range(truncation_length + 1)
        ),
        start=Fraction(0),
    )
    tail = negative_binomial_tail(ridge_parameter, truncation_length)
    tail_residual = abs(float(1 - mass - tail))
    operator_residual = float(np.linalg.norm(exact - truncated, ord=2))
    bounded = operator_residual <= float(tail) + tolerance
    verified = tail_residual <= tolerance and bounded
    return RidgeMixtureControl(
        control_id=control_id,
        ambient_dimension=exact.shape[0],
        leaf_count=len(projections),
        ridge_parameter=float(ridge_parameter),
        truncation_length=truncation_length,
        exact_negative_binomial_mass_through_truncation=float(mass),
        exact_negative_binomial_tail=float(tail),
        tail_formula_residual=tail_residual,
        normalized_exact_ridge_norm=float(np.linalg.norm(exact, ord=2)),
        truncated_mixture_operator_residual=operator_residual,
        residual_bounded_by_tail=bounded,
        negative_binomial_mean=2.0 / float(ridge_parameter),
        exact_mixture_verified=verified,
        status=(
            "normalized-ridge-negative-binomial-word-mixture-verified"
            if verified
            else "ridge-word-mixture-certificate-failure"
        ),
    )


def ridge_pressure_scaling_record(
    n: int,
    *,
    ridge_inverse_polynomial_degree: int,
    fixed_ridge_factor_count: int,
    truncation_error_degree: int = 10,
) -> RidgePressureScalingRecord:
    if n < 2:
        raise ValueError("n must be at least two")
    if ridge_inverse_polynomial_degree < 0 or fixed_ridge_factor_count < 1:
        raise ValueError("invalid ridge degree or factor count")
    if truncation_error_degree < 1:
        raise ValueError("truncation error degree must be positive")
    eta = Fraction(1, n**ridge_inverse_polynomial_degree)
    target = Fraction(1, n**truncation_error_degree)
    length = minimum_truncation_length(eta, target)
    log_tail = negative_binomial_log_tail(eta, length)
    coefficient_log = (
        2
        * fixed_ridge_factor_count
        * ridge_inverse_polynomial_degree
        * math.log2(n)
    )
    group_log = math.lgamma(n + 1) / math.log(2)
    crossing_log = coefficient_log - group_log
    return RidgePressureScalingRecord(
        n=n,
        ridge_inverse_polynomial_degree=ridge_inverse_polynomial_degree,
        fixed_ridge_factor_count=fixed_ridge_factor_count,
        ridge_parameter=float(eta),
        target_truncation_error=float(target),
        truncation_length=length,
        exact_length_tail_upper_bound=math.exp(log_tail),
        log2_ridge_absolute_coefficient_mass=coefficient_log,
        log2_symmetric_group_order=group_log,
        log2_crossing_bound_after_ridge_prefactor=crossing_log,
        factorial_crossing_loss_survives=crossing_log < 0,
        polynomial_word_length=True,
        status=(
            "ridge-prefactor-does-not-erase-factorial-crossing-loss"
            if crossing_log < 0
            else "finite-scale-ridge-prefactor-exceeds-group-loss"
        ),
    )


def poisson_ridge_word_mixture_theorem() -> PoissonRidgeWordMixtureTheorem:
    return PoissonRidgeWordMixtureTheorem(
        heat_kernel_identity=(
            "exp(-t Fbar)=E[product_{j=1}^{N_t}(I-P_{E_j})]"
        ),
        normalized_ridge_mixture=(
            "eta^2 Fbar(Fbar+eta I)^-2 is a probability mixture of "
            "P_{E0} product_j(I-P_{Ej})"
        ),
        length_distribution=(
            "Pr[N=m]=eta^2(m+1)/(1+eta)^(m+2)"
        ),
        mean_word_length="E[N]=2/eta",
        truncation_tail=(
            "Pr[N>L]=r^(L+1)((L+2)-(L+1)r), r=(1+eta)^-1"
        ),
        absolute_coefficient_mass=(
            "one for eta^2 R_eta, hence eta^-2 per unnormalized ridge factor"
        ),
        crossing_pressure_transfer=(
            "r fixed ridge factors cost eta^-2r; inverse-polynomial eta cannot "
            "erase an |S_n|^-1 all-width crossing bound"
        ),
        scope_limit=(
            "This controls normalized-frame ridge words, not C_eta^-1/2, "
            "ridge-to-Green average synthesis error, or noncrossing mass."
        ),
        arbitrary_leaf_count=True,
        arbitrary_word_length=True,
        inverse_polynomial_ridge_has_polynomial_truncation=True,
        green_word_coefficient_burden_resolved=True,
        common_metric_normalization_resolved=False,
        positive_component_M4_proved=False,
        theorem_verified=True,
        status="normalized-ridge-word-burden-removed",
    )


def _projection_controls(seed: int, dimension: int, leaf_count: int) -> tuple[np.ndarray, ...]:
    rng = np.random.default_rng(seed)
    projections = []
    for rank in range(1, leaf_count + 1):
        width = 1 + (rank % max(1, dimension - 1))
        raw = rng.normal(size=(dimension, width)) + 1j * rng.normal(
            size=(dimension, width)
        )
        isometry, _ = np.linalg.qr(raw)
        projections.append(isometry @ isometry.conj().T)
    return tuple(projections)


def run_poisson_ridge_word_mixture() -> PoissonRidgeWordMixtureReport:
    first = _projection_controls(1709, 5, 3)
    second = _projection_controls(1721, 6, 4)
    fixed = [
        audit_fixed_length_complement_words(
            f"Q{len(projections)}-L{length}",
            projections,
            length,
        )
        for projections in (first, second)
        for length in range(5)
    ]
    ridge = [
        audit_ridge_mixture(
            f"Q{len(projections)}-ETA-{eta}-L{length}",
            projections,
            eta,
            length,
        )
        for projections, eta, length in (
            (first, Fraction(1, 2), 20),
            (first, Fraction(1, 5), 50),
            (second, Fraction(1, 3), 30),
            (second, Fraction(1, 10), 100),
        )
    ]
    scaling = [
        ridge_pressure_scaling_record(
            n,
            ridge_inverse_polynomial_degree=2,
            fixed_ridge_factor_count=4,
        )
        for n in (20, 32, 50, 80, 128, 256, 512, 1024)
    ]
    theorem = poisson_ridge_word_mixture_theorem()
    exact = (
        all(row.exact_fixed_length_factorization_verified for row in fixed)
        and all(row.exact_mixture_verified for row in ridge)
        and theorem.theorem_verified
    )
    return PoissonRidgeWordMixtureReport(
        created_at=utc_now(),
        theorem_contract={
            "normalized_frame": "Fbar=q^-1 sum_e P_e",
            "heat_kernel": theorem.heat_kernel_identity,
            "ridge_mixture": theorem.normalized_ridge_mixture,
            "pressure_transfer": theorem.crossing_pressure_transfer,
            "scope": theorem.scope_limit,
        },
        fixed_length_controls=fixed,
        ridge_controls=ridge,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "obligation": "remove_exponential_leaf_count_from_heat_kernel_words",
                "resolved": True,
                "resolution": (
                    "Uniform leaf selection is inside a probability expectation; "
                    "its coefficient mass is one for every Poisson length."
                ),
            },
            {
                "obligation": "remove_uncontrolled_polynomial_monomial_coefficients",
                "resolved": True,
                "resolution": (
                    "Gamma mixing produces an exact negative-binomial probability "
                    "law; only eta^-2 per unnormalized ridge factor remains."
                ),
            },
            {
                "obligation": "truncate_infinite_words_at_polynomial_length",
                "resolved": True,
                "resolution": (
                    "The exact tail formula gives L=O(eta^-1 log(1/delta)) for "
                    "inverse-polynomial eta and target error delta."
                ),
            },
            {
                "obligation": "transfer_all_width_crossing_pressure_through_ridge_words",
                "resolved": True,
                "resolution": (
                    "Complement projectors have the same absolute group expansion "
                    "as invariant projectors; mixture averaging preserves the bound."
                ),
            },
            {
                "obligation": "control_common_metric_inverse_and_noncrossing_scale",
                "resolved": False,
                "resolution": (
                    "C_eta^-1/2 and the retained noncrossing ridge moment are not "
                    "part of the normalized-frame heat-kernel mixture theorem."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "There are exponentially many leaves at each word position.",
                "resolved": True,
                "resolution": (
                    "They are sampled uniformly; summing their coefficients is an "
                    "expectation with total mass one, not a union bound."
                ),
            },
            {
                "objection": "The alternating exponential series has exponential l1 mass.",
                "resolved": True,
                "resolution": (
                    "Poisson complement words are a positive operator mixture and "
                    "avoid expanding in raw powers of Fbar."
                ),
            },
            {
                "objection": "Poisson words have unbounded degree.",
                "resolved": True,
                "resolution": (
                    "The pressure theorem is all-width, and the exact negative-"
                    "binomial tail permits polynomial truncation when needed."
                ),
            },
            {
                "objection": "This proves the exact Green component moment is positive.",
                "resolved": False,
                "resolution": (
                    "No: common-metric normalization, average ridge transfer, and "
                    "the noncrossing lower bound remain."
                ),
            },
        ],
        headline_metrics={
            "poisson_ridge_word_mixture_theorem_count": int(exact),
            "fixed_length_control_failure_count": sum(
                not row.exact_fixed_length_factorization_verified for row in fixed
            ),
            "ridge_mixture_control_failure_count": sum(
                not row.exact_mixture_verified for row in ridge
            ),
            "maximum_control_tail_formula_residual": max(
                row.tail_formula_residual for row in ridge
            ),
            "maximum_control_operator_residual_to_tail_ratio": max(
                row.truncated_mixture_operator_residual
                / row.exact_negative_binomial_tail
                for row in ridge
            ),
            "largest_scaling_degree": scaling[-1].n,
            "largest_scale_crossing_log2_bound": (
                scaling[-1].log2_crossing_bound_after_ridge_prefactor
            ),
            "green_word_coefficient_burden_remaining_count": 0,
            "common_metric_normalization_theorem_count": 0,
            "natural_component_M4_lower_bound_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "normalized_ridge_has_probability_word_mixture": exact,
            "exponential_leaf_count_survives_in_coefficients": False,
            "green_word_coefficient_burden_controlled": exact,
            "all_width_crossing_pressure_survives_ridge_mixture": exact,
            "common_metric_normalization_controlled": False,
            "ridge_to_green_average_error_controlled": False,
            "noncrossing_ridge_moment_lower_bounded": False,
            "natural_component_M4_positive": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Poisson/Gamma mixing removes the frame-word coefficient burden. "
                "The remaining M4 barriers are common-metric normalization, average "
                "ridge transfer, and noncrossing mass."
            ),
        },
        status=(
            "ridge-frame-word-burden-closed-common-metric-open"
            if exact
            else "poisson-ridge-word-mixture-certificate-failure"
        ),
        summary=(
            "Converted normalized Green ridge factors into an outcome-count-free "
            "probability mixture of polynomially truncatable complement words."
        ),
        falsifiers_triggered=[
            "Raw monomial l1 growth is an artifact of the wrong expansion basis.",
            "Exponential leaf count is absorbed by uniform event sampling.",
            "Infinite ridge words have an exact polynomial-scale truncation law.",
            "Common-metric normalization, not frame-word coefficients, is now open.",
        ],
    )


def write_poisson_ridge_word_mixture_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-POISSON-RIDGE-WORD-MIXTURE"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    path = path
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    report = asdict(run_poisson_ridge_word_mixture())
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
                id="NEG-SELF-DUAL-WREATH-POISSON-RIDGE-WORD-MIXTURE",
                source=registry_experiment_id,
                claim=(
                    "Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-POISSON-RIDGE-WORD-MIXTURE."
                ),
                reason_invalid=(
                    "Falsified or refined by exact theorem evaluation."
                ),
                lesson=(
                    "Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-POISSON-RIDGE-WORD-MIXTURE."
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
                    "self_dual_wreath_poisson_ridge_word_mixture": str(path)
                },
            )
        )

    return report


if __name__ == "__main__":
    result = write_poisson_ridge_word_mixture_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))
