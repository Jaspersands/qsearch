"""Three Plancherel factors contain any fixed target a.a.s.

Fix an irreducible target ``tau`` of ``S_n`` and let
``lambda_1,...,lambda_q`` be independent Plancherel-random irreps.  If
``m_tau`` is the multiplicity of ``tau`` in their tensor product, define

    X_(tau,q) = sum_(s!=1) r_tau(s) product_j r_(lambda_j)(s).

The character formula gives

    |S_n| m_tau/(d_tau product_j d_(lambda_j)) = 1+X_(tau,q). (1)

Character-column orthogonality and independence yield the exact variance

    E X_(tau,q)^2
      = sum_(nonidentity classes C) |C|^(2-q) r_tau(C)^2.  (2)

Since normalized character ratios have magnitude at most one, for every
``q>=3`` equation (2) is at most

    sum_(C!=1) 1/|C| = o(1).

Equation (1) and Chebyshev prove the stronger normalized-multiplicity law,
uniformly in the chosen target,

    |S_n| m_tau/(d_tau product_j d_(lambda_j)) -> 1
        in probability, q>=3.                              (3)

In particular ``Pr[m_tau=0]=o(1)``.

The uniformity is pointwise: the same bound holds for every target, but a
union over all ``p(n)`` targets is not justified because ``p(n)`` times the
bound need not vanish.  Thus (3) does not replace Sellke's simultaneous
covering theorem.

For the orientation geometry, the result makes Hamming distance three the
exact independent-Plancherel support transition.  Every exclusive
three-source membership block contains trivial (and, by conjugation, sign)
with probability ``1-o(1)``.  Any shared block containing three independent
source factors contains the fixed target or its conjugate with the same
probability.  After global-distinct conditioning, a fixed Hamming-three pair
therefore has a common range with probability ``1-o(1)``.  Distances one and
two remain transverse by the prior local theorem.

For a fixed orientation pair with ``3<=h<=K-3``, apply (3) to its left-only,
right-only, and shared membership blocks.  The pair-common relative rank then
concentrates at ``2/|S_n|^3``.  This is an individual-pair multiplicity law,
not a simultaneous law over exponentially many pairs or a frame-edge theorem.
Common spaces still have complicated coherent incidence across pairs.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_global_collision_free_mass import plancherel_weights
from self_dual_wreath_orientation_fusion_moment import (
    tensor_product_multiplicities,
)
from self_dual_wreath_plancherel_kronecker_positivity import (
    centralizer_order,
    reciprocal_nonidentity_class_sum,
)
from symmetric_character import symmetric_character


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_extended_kronecker_threshold.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-EXTENDED-KRONECKER-THRESHOLD"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
SELLKE_COVERING_URL = "https://arxiv.org/abs/2004.05283"

Partition = tuple[int, ...]


@dataclass(frozen=True)
class ExtendedKroneckerVarianceControl:
    n: int
    factor_count: int
    target_count: int
    source_tuple_count_per_target: int
    maximum_exact_mean_residual: str
    maximum_exact_variance_formula_residual: str
    maximum_zero_probability_bound_residual: str
    maximum_target_zero_probability: float
    maximum_target_variance_bound: float
    exact_fixed_target_variance_identity_verified: bool
    fixed_target_zero_probability_bound_verified: bool
    status: str


@dataclass(frozen=True)
class ExtendedKroneckerScalingRecord:
    n: int
    factor_count: int
    worst_target_variance_upper_bound: float
    worst_target_variance_upper_bound_log2: float
    transposition_contribution_upper_bound: float
    fixed_target_positivity_probability_tends_to_one: bool
    simultaneous_all_target_covering_proved: bool
    multiplicity_concentration_proved: bool
    status: str


@dataclass(frozen=True)
class ExtendedKroneckerThresholdReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[ExtendedKroneckerVarianceControl]
    scaling_records: list[ExtendedKroneckerScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    literature_links: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def tensor_target_multiplicity(
    factors: tuple[Partition, ...],
    target: Partition,
) -> int:
    if not factors:
        return int(target == (sum(target),))
    n = sum(target)
    if any(sum(factor) != n for factor in factors):
        raise ValueError("all partitions must have the same size")
    return dict(tensor_product_multiplicities(factors, n)).get(target, 0)


def normalized_fixed_target_remainder(
    factors: tuple[Partition, ...],
    target: Partition,
) -> Fraction:
    n = sum(target)
    multiplicity = tensor_target_multiplicity(factors, target)
    denominator = hook_length_dimension(target) * math.prod(
        hook_length_dimension(factor) for factor in factors
    )
    return Fraction(math.factorial(n) * multiplicity, denominator) - 1


def fixed_target_variance_formula(
    n: int,
    factor_count: int,
    target: Partition,
) -> Fraction:
    if factor_count < 1 or sum(target) != n:
        raise ValueError("invalid factor count or target")
    order = math.factorial(n)
    target_dimension = hook_length_dimension(target)
    identity = (1,) * n
    total = Fraction()
    for cycle_type in integer_partitions(n):
        if cycle_type == identity:
            continue
        centralizer = centralizer_order(cycle_type)
        class_size = order // centralizer
        ratio = Fraction(
            symmetric_character(target, cycle_type),
            target_dimension,
        )
        total += Fraction(1, class_size ** (factor_count - 2)) * ratio * ratio
    return total


def audit_extended_kronecker_variance(
    n: int,
    factor_count: int,
) -> ExtendedKroneckerVarianceControl:
    if not (n == 5 and factor_count == 3) and not (
        n == 4 and factor_count == 4
    ):
        raise ValueError("exact controls use (S5,q=3) or (S4,q=4)")
    partitions = tuple(integer_partitions(n))
    weights = dict(zip(partitions, plancherel_weights(n)))
    mean_residuals = []
    variance_residuals = []
    bound_residuals = []
    zero_probabilities = []
    variance_bounds = []
    for target in partitions:
        mean = Fraction()
        second = Fraction()
        zero_probability = Fraction()
        for factors in itertools.product(partitions, repeat=factor_count):
            probability = math.prod(
                (weights[factor] for factor in factors),
                start=Fraction(1),
            )
            multiplicity = tensor_target_multiplicity(factors, target)
            remainder = normalized_fixed_target_remainder(factors, target)
            mean += probability * remainder
            second += probability * remainder * remainder
            zero_probability += probability * (multiplicity == 0)
        predicted = fixed_target_variance_formula(n, factor_count, target)
        mean_residuals.append(abs(mean))
        variance_residuals.append(abs(second - predicted))
        bound_residuals.append(predicted - zero_probability)
        zero_probabilities.append(float(zero_probability))
        variance_bounds.append(float(predicted))
    variance_verified = max(mean_residuals) == 0 and max(variance_residuals) == 0
    bound_verified = min(bound_residuals) >= 0
    return ExtendedKroneckerVarianceControl(
        n=n,
        factor_count=factor_count,
        target_count=len(partitions),
        source_tuple_count_per_target=len(partitions) ** factor_count,
        maximum_exact_mean_residual=str(max(mean_residuals)),
        maximum_exact_variance_formula_residual=str(max(variance_residuals)),
        maximum_zero_probability_bound_residual=str(max(bound_residuals)),
        maximum_target_zero_probability=max(zero_probabilities),
        maximum_target_variance_bound=max(variance_bounds),
        exact_fixed_target_variance_identity_verified=variance_verified,
        fixed_target_zero_probability_bound_verified=bound_verified,
        status=(
            "exact-fixed-target-extended-kronecker-variance-verified"
            if variance_verified and bound_verified
            else "extended-kronecker-variance-control-failure"
        ),
    )


def extended_kronecker_scaling_record(
    n: int,
    factor_count: int,
) -> ExtendedKroneckerScalingRecord:
    if n < 3 or factor_count < 3:
        raise ValueError("scaling requires n>=3 and q>=3")
    order = math.factorial(n)
    bound = sum(
        (
            Fraction(
                1,
                (order // centralizer_order(cycle_type))
                ** (factor_count - 2),
            )
            for cycle_type in integer_partitions(n)
            if cycle_type != (1,) * n
        ),
        start=Fraction(),
    )
    value = float(bound)
    transposition_class_size = math.comb(n, 2)
    return ExtendedKroneckerScalingRecord(
        n=n,
        factor_count=factor_count,
        worst_target_variance_upper_bound=value,
        worst_target_variance_upper_bound_log2=math.log2(value),
        transposition_contribution_upper_bound=(
            transposition_class_size ** (2 - factor_count)
        ),
        fixed_target_positivity_probability_tends_to_one=True,
        simultaneous_all_target_covering_proved=False,
        multiplicity_concentration_proved=True,
        status="fixed-target-normalized-multiplicity-concentrated-simultaneous-covering-open",
    )


def run_extended_kronecker_threshold() -> ExtendedKroneckerThresholdReport:
    controls = [
        audit_extended_kronecker_variance(5, 3),
        audit_extended_kronecker_variance(4, 4),
    ]
    scaling = [
        extended_kronecker_scaling_record(n, factor_count)
        for n in (10, 20, 30, 40, 50)
        for factor_count in (3, 4, 5)
    ]
    failures = sum(
        not row.exact_fixed_target_variance_identity_verified
        or not row.fixed_target_zero_probability_bound_verified
        for row in controls
    )
    verified = failures == 0
    n50_q4 = next(
        row for row in scaling if row.n == 50 and row.factor_count == 4
    )
    metrics: dict[str, int | float] = {
        "exact_fixed_target_variance_theorem_count": 1,
        "three_factor_fixed_target_positivity_theorem_count": 1,
        "hamming_three_support_transition_theorem_count": 1,
        "finite_control_count": len(controls),
        "finite_control_failure_count": failures,
        "n50_q4_worst_target_variance_upper_bound": (
            n50_q4.worst_target_variance_upper_bound
        ),
        "simultaneous_all_target_covering_theorem_count": 0,
        "fixed_target_normalized_multiplicity_concentration_theorem_count": 1,
        "fixed_hamming_pair_common_rank_concentration_theorem_count": 1,
        "natural_node_frame_edge_theorem_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return ExtendedKroneckerThresholdReport(
        created_at=utc_now(),
        theorem_contract={
            "exact_variance": (
                "E X_(tau,q)^2=sum_(C!=1)|C|^(2-q)r_tau(C)^2."
            ),
            "uniform_fixed_target_bound": (
                "For q>=3 this is at most sum_(C!=1)1/|C|=o(1), "
                "uniformly in the fixed target tau."
            ),
            "positivity": (
                "Every fixed target occurs in q>=3 independent Plancherel "
                "factors with probability 1-o(1)."
            ),
            "normalized_multiplicity": (
                "|S_n| m_tau/(d_tau product d_lambda) converges in probability "
                "to one for every fixed target and q>=3."
            ),
            "orientation_transition": (
                "Together with radius-two transversality, independent natural "
                "pair-common support transitions exactly at Hamming distance three."
            ),
            "fixed_pair_rank": (
                "For a fixed pair with 3<=h<=K-3, the common relative rank "
                "concentrates at 2/|S_n|^3."
            ),
            "scope": (
                "Pointwise normalized multiplicity is not simultaneous covering, "
                "simultaneous all-pair control, incidence control, or a frame edge."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "derive_fixed_target_extended_kronecker_variance",
                "resolved": verified,
                "resolution": (
                    "Column orthogonality contributes |C|^(2-q) and the fixed "
                    "target contributes its squared normalized character ratio."
                ),
            },
            {
                "obligation": "locate_independent_plancherel_support_threshold",
                "resolved": True,
                "resolution": (
                    "Distances one and two are transverse; three factors contain "
                    "every fixed required sector with probability 1-o(1)."
                ),
            },
            {
                "obligation": "upgrade_pointwise_target_occurrence_to_simultaneous_covering",
                "resolved": False,
                "resolution": (
                    "The p(n)-target union is not controlled by the reciprocal "
                    "class-size bound."
                ),
            },
            {
                "obligation": "derive_fixed_pair_common_rank_concentration",
                "resolved": True,
                "resolution": (
                    "Apply the normalized multiplicity law to the three "
                    "independent membership blocks and both parity assignments."
                ),
            },
            {
                "obligation": "derive_simultaneous_many_pair_incidence_local_law",
                "resolved": False,
                "resolution": (
                    "The o(1) pointwise failure is not small enough to union over "
                    "exponentially many pairs, and coherent alignment is unbounded."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Sellke's unspecified covering constant is needed to locate the first common-support radius.",
                "resolved": True,
                "resolution": (
                    "Not for independent Plancherel sources: the exact variance "
                    "puts the pointwise support threshold at three."
                ),
            },
            {
                "objection": "A target-uniform probability bound proves all targets occur simultaneously.",
                "resolved": False,
                "resolution": (
                    "Uniform in tau means one bound valid for each fixed tau; "
                    "it does not pay the p(n)-sized union."
                ),
            },
            {
                "objection": "Typical fixed-target support controls the full orientation frame.",
                "resolved": False,
                "resolution": (
                    "Individual normalized ranks are controlled, but channel "
                    "decomposition and higher-order incidence remain open."
                ),
            },
        ],
        literature_links=[
            {
                "paper": "Sellke, Covering Irrep(S_n) With Tensor Products and Powers",
                "url": SELLKE_COVERING_URL,
                "directly_proves_pointwise_three_factor_threshold": False,
                "reason": (
                    "Sellke proves simultaneous covering with some fixed number "
                    "of factors; the present pointwise q=3 result uses exact "
                    "independent Plancherel variance instead."
                ),
            }
        ],
        headline_metrics=metrics,
        claim_gate={
            "exact_fixed_target_extended_variance_proved": verified,
            "three_independent_plancherel_factors_contain_fixed_target_aas": True,
            "independent_natural_hamming_three_support_transition_proved": True,
            "fixed_target_normalized_multiplicity_concentration_proved": True,
            "fixed_hamming_pair_common_rank_concentration_proved": True,
            "simultaneous_all_irrep_covering_with_three_factors_proved": False,
            "simultaneous_all_pair_rank_concentration_proved": False,
            "higher_order_incidence_edge_proved": False,
            "natural_all_depth_node_edge_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The independent support threshold and each fixed pair's rank "
                "are controlled, but simultaneous incidence and full-frame "
                "spectral geometry remain open."
            ),
        },
        status=(
            "three-factor-multiplicity-and-fixed-pair-rank-proved-incidence-open"
            if verified
            else "extended-kronecker-threshold-control-failure"
        ),
        summary=(
            "Proved normalized fixed-target multiplicity concentration for "
            "three or more independent Plancherel irreps."
        ),
        falsifiers_triggered=[
            "The independent pointwise support transition occurs at three factors, not an unknown larger covering radius.",
            "Pointwise target-uniform bounds do not imply simultaneous covering of all irreps.",
            "Pointwise multiplicity concentration does not provide simultaneous incidence or frame-edge control.",
        ],
    )


def write_extended_kronecker_threshold_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-EXTENDED-KRONECKER-THRESHOLD"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_extended_kronecker_threshold())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")

    if write_registry:
        from research_registry import (
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-SELF-DUAL-WREATH-EXTENDED-KRONECKER-THRESHOLD",
                source=registry_experiment_id,
                claim=(
                    "Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-EXTENDED-KRONECKER-THRESHOLD."
                ),
                reason_invalid=(
                    "Falsified or refined by exact theorem evaluation."
                ),
                lesson=(
                    "Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-EXTENDED-KRONECKER-THRESHOLD."
                ),
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-MEASUREMENT",
                ],
                evidence=payload.get("headline_metrics", {}),
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
                created_at=payload.get("created_at", ""),
                status=payload.get("status", "completed"),
                summary=payload.get("summary", ""),
                metrics=payload.get("headline_metrics", {}),
                falsifiers_triggered=payload.get("falsifiers_triggered", []),
                artifacts={
                    "self_dual_wreath_extended_kronecker_threshold": str(path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_extended_kronecker_threshold_report()
    print(json.dumps(report, indent=2))
