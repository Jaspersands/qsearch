"""Stretched-exponential admission no-go for exact conjugate-pair sign twists.

Replacing the rare trivial/sign source pair by a high-dimensional conjugate
pair ``(A,A^T)`` preserves the exact sign-twist identity

    V_(A^T) = V_A tensor sgn.

But under independent Plancherel sampling, with
``p_lambda=d_lambda^2/n!``, the probability that two labels are conjugate is

    P_conj = sum_lambda p_lambda p_(lambda^T)
           = sum_lambda p_lambda^2.                       (1)

Thus exact conjugate matching is precisely a Plancherel collision event.  If
``p(n)`` is the partition number and ``p_*`` the largest Plancherel atom,

    1/p(n) <= P_conj <= p_*.                              (2)

Hardy--Ramanujan gives ``p(n)=exp(Theta(sqrt(n)))``.  The maximal-irrep
dimension theorem used elsewhere in this repository gives
``p_*=exp(-Theta(sqrt(n)))``.  Hence

    P_conj = exp(-Theta(sqrt(n))).                        (3)

Even among ``m=poly(n)`` independent labels, a union bound leaves exact
conjugate admission stretched-exponentially small; amplitude amplification
costs ``exp(Theta(sqrt(n)))``.  Conditioning a polynomial-size pool on global
distinctness does not change the asymptotic conclusion because its mass tends
to one, and it removes rather than adds self-conjugate duplicate pairs.

This no-go applies only to postselecting an exact conjugate pair from natural
sampled labels.  It does not rule out a label-adaptive transform summing
coherently over many pairs, an approximate/distributed sign twist, or a
different recoupling mechanism that does not require ``B=A^T``.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_joint_character_purity_decoupling import partition_number
from self_dual_wreath_sign_twist_collective_activation import transpose_partition


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_conjugate_pair_admission_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-CONJUGATE-PAIR-ADMISSION-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
MAXIMAL_DIMENSION_PAPER_ID = "aggarwal-elboim-maximal-dimension-2026"
MAXIMAL_DIMENSION_PAPER_URL = "https://arxiv.org/abs/2605.25995"

Partition = tuple[int, ...]


@dataclass(frozen=True)
class ConjugatePairAdmissionControl:
    n: int
    partition_count: int
    group_order: int
    exact_plancherel_collision_probability: str
    plancherel_collision_probability: float
    exact_distinct_conjugate_pair_probability: str
    distinct_conjugate_pair_probability: float
    exact_self_conjugate_duplicate_probability: str
    self_conjugate_duplicate_probability: float
    exact_unequal_conditioned_conjugate_probability: str
    unequal_conditioned_conjugate_probability: float
    reciprocal_partition_lower_bound: float
    maximum_plancherel_atom: float
    lower_bound_residual: float
    upper_bound_residual: float
    conjugation_preserves_plancherel_weight_verified: bool
    exact_collision_identity_verified: bool
    status: str


@dataclass(frozen=True)
class ConjugatePairAdmissionScalingRecord:
    n: int
    polynomial_sample_exponent: int
    sample_pool_size_log2: float
    candidate_pair_count_log2_upper: float
    partition_count_log2_asymptotic: float
    conjugate_pair_probability_asymptotic: str
    any_conjugate_pair_probability_upper_asymptotic: str
    amplitude_amplification_query_lower_asymptotic: str
    global_distinct_conditioning_mass_tends_to_one: bool
    inverse_polynomial_exact_conjugate_admission: bool
    approximate_or_distributed_twist_ruled_out: bool
    status: str


@dataclass(frozen=True)
class ConjugatePairAdmissionTheorem:
    exact_identity: str
    probability_sandwich: str
    asymptotic: str
    polynomial_pool: str
    collision_free_scope: str
    escape_routes: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class ConjugatePairAdmissionReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: ConjugatePairAdmissionTheorem
    finite_controls: list[ConjugatePairAdmissionControl]
    scaling_records: list[ConjugatePairAdmissionScalingRecord]
    literature_links: list[dict[str, str | bool]]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def audit_conjugate_pair_admission(
    n: int,
    *,
    tolerance: float = 1e-15,
) -> ConjugatePairAdmissionControl:
    if n < 2:
        raise ValueError("n must be at least two")
    partitions = tuple(integer_partitions(n))
    order = math.factorial(n)
    weights = {
        partition: Fraction(hook_length_dimension(partition) ** 2, order)
        for partition in partitions
    }
    collision = sum((weight**2 for weight in weights.values()), Fraction())
    conjugate = sum(
        (
            weight * weights[transpose_partition(partition)]
            for partition, weight in weights.items()
        ),
        Fraction(),
    )
    self_duplicate = sum(
        (
            weight**2
            for partition, weight in weights.items()
            if transpose_partition(partition) == partition
        ),
        Fraction(),
    )
    distinct = conjugate - self_duplicate
    unequal_probability = Fraction(1) - collision
    unequal_conditioned = distinct / unequal_probability
    reciprocal = Fraction(1, len(partitions))
    maximum = max(weights.values())
    conjugation_preserved = all(
        weight == weights[transpose_partition(partition)]
        for partition, weight in weights.items()
    )
    identity = conjugate == collision
    lower_residual = max(0.0, float(reciprocal - collision))
    upper_residual = max(0.0, float(collision - maximum))
    verified = bool(
        conjugation_preserved
        and identity
        and lower_residual <= tolerance
        and upper_residual <= tolerance
        and distinct >= 0
        and 0 <= unequal_conditioned <= 1
    )
    return ConjugatePairAdmissionControl(
        n=n,
        partition_count=len(partitions),
        group_order=order,
        exact_plancherel_collision_probability=str(collision),
        plancherel_collision_probability=float(collision),
        exact_distinct_conjugate_pair_probability=str(distinct),
        distinct_conjugate_pair_probability=float(distinct),
        exact_self_conjugate_duplicate_probability=str(self_duplicate),
        self_conjugate_duplicate_probability=float(self_duplicate),
        exact_unequal_conditioned_conjugate_probability=str(unequal_conditioned),
        unequal_conditioned_conjugate_probability=float(unequal_conditioned),
        reciprocal_partition_lower_bound=float(reciprocal),
        maximum_plancherel_atom=float(maximum),
        lower_bound_residual=lower_residual,
        upper_bound_residual=upper_residual,
        conjugation_preserves_plancherel_weight_verified=conjugation_preserved,
        exact_collision_identity_verified=identity,
        status=(
            "exact-conjugate-pair-equals-plancherel-collision"
            if verified
            else "conjugate-pair-admission-validation-failure"
        ),
    )


def conjugate_pair_admission_scaling_record(
    n: int,
    *,
    polynomial_sample_exponent: int = 4,
) -> ConjugatePairAdmissionScalingRecord:
    if n < 2 or polynomial_sample_exponent < 1:
        raise ValueError("invalid scaling parameters")
    pool_log2 = polynomial_sample_exponent * math.log2(n)
    return ConjugatePairAdmissionScalingRecord(
        n=n,
        polynomial_sample_exponent=polynomial_sample_exponent,
        sample_pool_size_log2=pool_log2,
        candidate_pair_count_log2_upper=2 * pool_log2 - 1,
        partition_count_log2_asymptotic=(
            math.pi * math.sqrt(2 * n / 3) / math.log(2)
            - math.log2(4 * n * math.sqrt(3))
        ),
        conjugate_pair_probability_asymptotic="exp(-Theta(sqrt(n)))",
        any_conjugate_pair_probability_upper_asymptotic=(
            "poly(n)^2 exp(-Theta(sqrt(n)))=exp(-Theta(sqrt(n)))"
        ),
        amplitude_amplification_query_lower_asymptotic="exp(Theta(sqrt(n)))",
        global_distinct_conditioning_mass_tends_to_one=True,
        inverse_polynomial_exact_conjugate_admission=False,
        approximate_or_distributed_twist_ruled_out=False,
        status="exact-conjugate-sign-twist-stretched-exponential-admission",
    )


def run_conjugate_pair_admission_no_go() -> ConjugatePairAdmissionReport:
    controls = [audit_conjugate_pair_admission(n) for n in range(4, 17)]
    scaling = [
        conjugate_pair_admission_scaling_record(n)
        for n in (32, 64, 128, 256, 512, 1024)
    ]
    failures = sum(
        not row.conjugation_preserves_plancherel_weight_verified
        or not row.exact_collision_identity_verified
        or row.lower_bound_residual > 0
        or row.upper_bound_residual > 0
        for row in controls
    )
    verified = failures == 0
    theorem = ConjugatePairAdmissionTheorem(
        exact_identity=(
            "Pr[B=A^T]=sum_lambda p_lambda p_(lambda^T)=sum_lambda p_lambda^2."
        ),
        probability_sandwich=(
            "1/p(n)<=sum_lambda p_lambda^2<=max_lambda p_lambda."
        ),
        asymptotic=(
            "Hardy--Ramanujan and the maximal-irrep theorem imply exact conjugate "
            "admission exp(-Theta(sqrt(n)))."
        ),
        polynomial_pool=(
            "A polynomial label pool contains any conjugate pair with probability at "
            "most poly(n)^2 exp(-Theta(sqrt(n)))."
        ),
        collision_free_scope=(
            "Global-distinct conditioning has asymptotic mass one and excludes "
            "self-conjugate duplicate pairs, so it does not restore polynomial mass."
        ),
        escape_routes=(
            "Coherent distributed sums, approximate twists, and recoupling without "
            "exact conjugate labels are outside the theorem."
        ),
        theorem_verified=verified,
        status=(
            "exact-conjugate-pair-sign-twist-admission-no-go"
            if verified
            else "conjugate-pair-admission-validation-failure"
        ),
    )
    return ConjugatePairAdmissionReport(
        created_at=utc_now(),
        theorem_contract=asdict(theorem),
        theorem=theorem,
        finite_controls=controls,
        scaling_records=scaling,
        literature_links=[
            {
                "paper_id": MAXIMAL_DIMENSION_PAPER_ID,
                "url": MAXIMAL_DIMENSION_PAPER_URL,
                "supports": (
                    "max d_lambda=sqrt(n!) exp(-(d+o(1))sqrt(n)), d>0, "
                    "hence max Plancherel atom exp(-Theta(sqrt(n)))."
                ),
                "external_theorem_not_reproved_here": True,
            }
        ],
        proof_obligations=[
            {
                "obligation": "test_high_dimensional_exact_conjugate_pair_repair",
                "resolved": verified,
                "resolution": (
                    "Its admission is exactly the Plancherel collision probability, "
                    "which is stretched-exponentially small."
                ),
            },
            {
                "obligation": "find_distributed_or_approximate_transpose_mechanism",
                "resolved": False,
                "resolution": (
                    "Need a label-adaptive transform whose useful mass is spread over "
                    "many typical pairs rather than an exact A^T match."
                ),
            },
            {
                "obligation": "prove_typical_pair_recoupling_energy",
                "resolved": False,
                "resolution": (
                    "No natural high-weight analogue of the sign-twist energy theorem "
                    "has been established."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "High-dimensional A and A^T each have enough mass to be selected polynomially.",
                "resolved": True,
                "resolution": (
                    "False. Even the largest individual Plancherel atom is "
                    "exp(-Theta(sqrt(n)))."
                ),
            },
            {
                "objection": "A polynomial pool makes a conjugate match likely by a birthday effect.",
                "resolved": True,
                "resolution": (
                    "False. The polynomial pair count cannot overcome a "
                    "stretched-exponential collision probability."
                ),
            },
            {
                "objection": "Conditioning all labels distinct increases conjugate matching to polynomial mass.",
                "resolved": True,
                "resolution": (
                    "False asymptotically: the conditioning mass tends to one and only "
                    "removes equal self-conjugate pairs."
                ),
            },
            {
                "objection": "The no-go rules out every use of sign duality.",
                "resolved": True,
                "resolution": (
                    "False. It covers exact sampled conjugate matching only."
                ),
            },
        ],
        headline_metrics={
            "exact_conjugate_collision_identity_theorem_count": 1,
            "stretched_exponential_admission_no_go_theorem_count": 1,
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "polynomial_pool_exact_conjugate_admission_count": 0,
            "distributed_approximate_twist_theorem_count": 0,
            "natural_high_weight_recoupling_algorithm_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "exact_conjugate_probability_equals_plancherel_collision": verified,
            "exact_conjugate_admission_stretched_exponential": verified,
            "polynomial_sample_pool_repairs_exact_matching": False,
            "collision_free_conditioning_repairs_exact_matching": False,
            "approximate_or_distributed_sign_twist_ruled_out": False,
            "typical_pair_collective_energy_proved": False,
            "polynomial_point_decoder_proved": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Exact conjugate matching remains stretched-exponentially rare; a "
                "viable mechanism must distribute over typical unmatched labels."
            ),
        },
        status=theorem.status,
        summary=(
            "Proved that replacing trivial/sign by an exact high-dimensional conjugate "
            "pair only improves factorial rarity to stretched-exponential rarity. The "
            "next admissible target is a distributed or approximate twist."
        ),
        falsifiers_triggered=[
            (
                "A high-dimensional exact conjugate pair is not naturally available "
                "with inverse-polynomial probability."
            ),
            (
                "Polynomially many sampled labels do not create a Plancherel birthday "
                "match against a stretched-exponential collision law."
            ),
            (
                "The no-go is about exact label matching, not coherent sign-duality "
                "operations spread over many sectors."
            ),
        ],
    )


def write_conjugate_pair_admission_no_go_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-CONJUGATE-PAIR-ADMISSION-NO-GO"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_conjugate_pair_admission_no_go" in globals():
        report = run_conjugate_pair_admission_no_go(**kwargs)
        payload = asdict(report) if hasattr(report, "__dataclass_fields__") else (dict(report) if isinstance(report, dict) else report)
    else:
        report = {}
        payload = {}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    if write_registry:
        from research_registry import (
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-SELF-DUAL-WREATH-CONJUGATE-PAIR-ADMISSION-NO-GO",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-CONJUGATE-PAIR-ADMISSION-NO-GO.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-CONJUGATE-PAIR-ADMISSION-NO-GO.",
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
                    "self_dual_wreath_conjugate_pair_admission_no_go": str(path)
                },
            )
        )
    return payload
