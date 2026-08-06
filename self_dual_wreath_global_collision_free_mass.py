"""Exact natural mass of globally collision-free source partitions.

An unequal wreath label is an unordered pair of independent Plancherel
partitions ``{lambda,mu}``.  For ``k`` labels, global collision freedom means
that all ``2k`` source partitions are distinct.  If

    p_lambda = d_lambda^2 / n!,

then the exact unconditioned mass is

    P_cf(n,k) = (2k)! e_(2k)({p_lambda}),                 (1)

where ``e_r`` is the elementary symmetric polynomial.  Conditioning each
label on being unequal divides (1) by ``(1-C_n)^k``, where
``C_n=sum_lambda p_lambda^2``.

Equation (1) is a necessary physical-mass gate for every theorem restricted
to globally distinct source partitions.  At the information threshold the
event is absent for small n and remains tiny through the exact finite range
below, despite trending upward.  An asymptotic claim requires a quantitative
upper bound on Plancherel collision probability strong enough to beat
``k^2``; finite collision-free recoupling controls do not supply that bound.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import (
    hook_length_dimension,
    integer_partitions,
)
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_global_collision_free_mass.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-GLOBAL-COLLISION-FREE-MASS"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class GlobalCollisionFreeMassRecord:
    n: int
    partition_count: int
    information_threshold_copy_count: int
    required_distinct_partition_count: int
    plancherel_collision_probability: float
    log2_unconditioned_global_collision_free_probability: float
    log2_within_pair_unequal_conditioned_global_collision_free_probability: float
    unconditioned_global_collision_free_probability: float
    within_pair_unequal_conditioned_global_collision_free_probability: float
    birthday_union_collision_upper_bound: float
    enough_distinct_partitions_exist: bool
    global_collision_free_mass_inverse_polynomial: bool
    exact_elementary_symmetric_evaluation: bool
    status: str


@dataclass(frozen=True)
class GlobalCollisionFreeMassReport:
    created_at: str
    theorem_contract: dict[str, Any]
    exact_validations: list[dict[str, Any]]
    scaling_records: list[GlobalCollisionFreeMassRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


@lru_cache(maxsize=None)
def plancherel_weights(n: int) -> tuple[Fraction, ...]:
    if n < 1:
        raise ValueError("n must be positive")
    factorial = math.factorial(n)
    weights = tuple(
        Fraction(hook_length_dimension(partition) ** 2, factorial)
        for partition in integer_partitions(n)
    )
    if sum(weights, Fraction()) != 1:
        raise ArithmeticError("Plancherel weights do not sum to one")
    return weights


def elementary_symmetric_fraction(
    weights: tuple[Fraction, ...],
    degree: int,
) -> Fraction:
    if degree < 0:
        raise ValueError("degree must be nonnegative")
    if degree > len(weights):
        return Fraction()
    coefficients = [Fraction()] * (degree + 1)
    coefficients[0] = Fraction(1)
    for weight in weights:
        for index in range(degree, 0, -1):
            coefficients[index] += weight * coefficients[index - 1]
    return coefficients[degree]


def exact_global_collision_free_probability(
    n: int,
    copy_count: int,
    *,
    condition_within_pairs_unequal: bool = False,
) -> Fraction:
    if copy_count < 0:
        raise ValueError("copy count must be nonnegative")
    weights = plancherel_weights(n)
    degree = 2 * copy_count
    probability = math.factorial(degree) * elementary_symmetric_fraction(
        weights,
        degree,
    )
    if condition_within_pairs_unequal and copy_count:
        collision = sum((weight * weight for weight in weights), Fraction())
        probability /= (1 - collision) ** copy_count
    return probability


def _log_elementary_symmetric(log_weights: np.ndarray, degree: int) -> float:
    if degree > len(log_weights):
        return -math.inf
    coefficients = np.full(degree + 1, -math.inf)
    coefficients[0] = 0.0
    for log_weight in log_weights:
        previous = coefficients.copy()
        coefficients[1:] = np.logaddexp(
            previous[1:],
            log_weight + previous[:-1],
        )
    return float(coefficients[degree])


def global_collision_free_mass_record(n: int) -> GlobalCollisionFreeMassRecord:
    partitions = tuple(integer_partitions(n))
    log_factorial = math.lgamma(n + 1)
    log_weights = np.asarray(
        [
            2 * math.log(hook_length_dimension(partition)) - log_factorial
            for partition in partitions
        ]
    )
    weights = np.exp(log_weights)
    collision = float(weights @ weights)
    copy_count = math.ceil(log_factorial / math.log(2))
    degree = 2 * copy_count
    log_elementary = _log_elementary_symmetric(log_weights, degree)
    log_unconditioned = (
        math.lgamma(degree + 1) + log_elementary
        if math.isfinite(log_elementary)
        else -math.inf
    )
    log_conditioned = (
        log_unconditioned - copy_count * math.log1p(-collision)
        if math.isfinite(log_unconditioned)
        else -math.inf
    )
    log2_unconditioned = log_unconditioned / math.log(2)
    log2_conditioned = log_conditioned / math.log(2)
    inverse_polynomial = bool(
        math.isfinite(log2_unconditioned)
        and log2_unconditioned >= -2 * math.log2(max(n, 2))
    )
    return GlobalCollisionFreeMassRecord(
        n=n,
        partition_count=len(partitions),
        information_threshold_copy_count=copy_count,
        required_distinct_partition_count=degree,
        plancherel_collision_probability=collision,
        log2_unconditioned_global_collision_free_probability=log2_unconditioned,
        log2_within_pair_unequal_conditioned_global_collision_free_probability=log2_conditioned,
        unconditioned_global_collision_free_probability=(
            math.exp(log_unconditioned) if log_unconditioned > -745 else 0.0
        ),
        within_pair_unequal_conditioned_global_collision_free_probability=(
            math.exp(log_conditioned) if log_conditioned > -745 else 0.0
        ),
        birthday_union_collision_upper_bound=math.comb(degree, 2) * collision,
        enough_distinct_partitions_exist=degree <= len(partitions),
        global_collision_free_mass_inverse_polynomial=inverse_polynomial,
        exact_elementary_symmetric_evaluation=True,
        status=(
            "collision-free-event-combinatorially-impossible"
            if degree > len(partitions)
            else "collision-free-mass-at-least-inverse-polynomial"
            if inverse_polynomial
            else "collision-free-mass-subinverse-polynomial-finite-row"
        ),
    )


def _direct_distinct_draw_probability(
    weights: tuple[Fraction, ...],
    draw_count: int,
) -> Fraction:
    total = Fraction()
    for sequence in __import__("itertools").permutations(
        range(len(weights)),
        draw_count,
    ):
        contribution = Fraction(1)
        for index in sequence:
            contribution *= weights[index]
        total += contribution
    return total


def _exact_validations() -> list[dict[str, Any]]:
    rows = []
    for n, copies in ((3, 1), (4, 1), (4, 2), (5, 2), (5, 3)):
        weights = plancherel_weights(n)
        degree = 2 * copies
        direct = _direct_distinct_draw_probability(weights, degree)
        formula = exact_global_collision_free_probability(n, copies)
        conditioned = exact_global_collision_free_probability(
            n,
            copies,
            condition_within_pairs_unequal=True,
        )
        collision = sum((weight * weight for weight in weights), Fraction())
        rows.append(
            {
                "n": n,
                "copy_count": copies,
                "draw_count": degree,
                "direct_probability": str(direct),
                "elementary_symmetric_probability": str(formula),
                "within_pair_unequal_conditioned_probability": str(conditioned),
                "conditioned_formula_residual": str(
                    conditioned - formula / (1 - collision) ** copies
                ),
                "exact_match": direct == formula,
            }
        )
    return rows


def run_global_collision_free_mass() -> GlobalCollisionFreeMassReport:
    validations = _exact_validations()
    scaling = [
        global_collision_free_mass_record(n)
        for n in (5, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48)
    ]
    failures = sum(not row["exact_match"] for row in validations)
    tail = scaling[-1]
    possible = [row for row in scaling if row.enough_distinct_partitions_exist]
    metrics: dict[str, int | float] = {
        "global_collision_free_mass_formula_count": int(failures == 0),
        "exact_validation_count": len(validations),
        "exact_validation_failure_count": failures,
        "finite_scaling_row_count": len(scaling),
        "combinatorially_impossible_threshold_row_count": sum(
            not row.enough_distinct_partitions_exist for row in scaling
        ),
        "inverse_polynomial_mass_row_count": sum(
            row.global_collision_free_mass_inverse_polynomial for row in scaling
        ),
        "minimum_finite_log2_collision_free_mass": min(
            row.log2_unconditioned_global_collision_free_probability
            for row in possible
        ),
        "tail_n": tail.n,
        "tail_partition_count": tail.partition_count,
        "tail_copy_count": tail.information_threshold_copy_count,
        "tail_log2_collision_free_mass": tail.log2_unconditioned_global_collision_free_probability,
        "tail_plancherel_collision_probability": tail.plancherel_collision_probability,
        "asymptotic_inverse_polynomial_mass_theorem_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return GlobalCollisionFreeMassReport(
        created_at=utc_now(),
        theorem_contract={
            "unconditioned_mass": "P_cf=(2k)! e_(2k)({d_lambda^2/n!}).",
            "within_pair_unequal_conditioning": "P_cf|unequal=P_cf/(1-C_n)^k, C_n=sum_lambda(d_lambda^2/n!)^2.",
            "birthday_sufficient_condition": "If k^2 C_n=o(1), a union bound makes global collision freedom typical.",
            "scope": "The elementary-symmetric formula is exact; no asymptotic upper bound on C_n is proved here.",
        },
        exact_validations=validations,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "exact_global_collision_free_mass",
                "resolved": failures == 0,
                "resolution": "Ordered distinct Plancherel draws are counted exactly by the elementary symmetric polynomial.",
            },
            {
                "obligation": "asymptotic_plancherel_collision_bound",
                "resolved": False,
                "resolution": "Need a cited quantitative bound making k(n)^2 C_n vanish at k=ceil(log2 n!).",
            },
            {
                "obligation": "positive_mass_transfer_of_collision_free_spectral_theorems",
                "resolved": False,
                "resolution": "The exact finite mass is tiny through n=48; no natural-average performance theorem follows from collision-free blocks alone.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "There are many partitions, so polynomially many labels are automatically distinct.",
                "resolved": True,
                "resolution": "Plancherel weights are highly nonuniform; the exact event is zero at n=5,8 and remains about 2^-26.4 at n=48.",
            },
            {
                "objection": "Finite tiny mass proves collision freedom is asymptotically negligible.",
                "resolved": False,
                "resolution": "Collision probability decreases rapidly and the exact mass trends upward; a quantitative asymptotic theorem is required.",
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "exact_global_collision_free_mass_formula_proved": failures == 0,
            "finite_collision_free_controls_represent_natural_mass": False,
            "asymptotic_collision_free_mass_inverse_polynomial_proved": False,
            "collision_free_spectral_results_transferred_to_natural_average": False,
            "speedup_claim_allowed": False,
            "reason": "The exact source mass is now computable, but its asymptotic scale and transfer to the natural PGM remain unproved.",
        },
        status="global-collision-free-mass-exact-asymptotic-transfer-open",
        summary=(
            "Derived the exact Plancherel mass of globally distinct source "
            f"partitions; at n={tail.n} and k={tail.information_threshold_copy_count} "
            f"the finite mass is about 2^{tail.log2_unconditioned_global_collision_free_probability:.3f}."
        ),
        falsifiers_triggered=[
            "Globally collision-free finite recoupling controls need a separate physical-mass theorem.",
            "Within-pair unequal conditioning is not the same as collision freedom across copies.",
            "Finite low-n spectral gaps cannot be weighted as representative natural behavior without source-mass accounting.",
        ],
    )


def write_global_collision_free_mass_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_global_collision_free_mass())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_global_collision_free_mass_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
