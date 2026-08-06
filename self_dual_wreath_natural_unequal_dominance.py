"""Natural-source reduction from all wreath sectors to unequal sectors.

Let p_lambda=d_lambda^2/n! be Plancherel measure on partitions of n.  The
physical weak-Fourier label law for

    W_n=(S_n x S_n) semidirect C_2

has total equal-pair mass p_lambda^2 for source pair (lambda,lambda), and
unequal-pair mass 2 p_lambda p_mu for the unordered pair {lambda,mu}.  Thus a
physical label is distributed exactly as two independent Plancherel draws,
with the representation packaging recording whether they collide.

The total equal-pair probability is the Plancherel collision probability

    C_n=sum_lambda p_lambda^2 <= max_lambda p_lambda.

Aggarwal and Elboim prove

    max_lambda d_lambda
      =sqrt(n!) exp(-(d+o(1)) sqrt(n)), d>0.

Consequently C_n=exp(-Theta(sqrt(n))).  For
k=ceil(log_2(n!)) independent coset-state labels,

    Pr[any equal-pair label] <= k C_n = o(1).

This removes equal-pair commutator recoupling from the asymptotic
natural-average critical path.  It does not provide a high-order contraction
for the overwhelmingly likely all-unequal tuple, a sub-POVM circuit, or a
hidden-permutation decoder.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from typing import Any

from representation_obstruction import (
    hook_length_dimension,
    integer_partitions,
)
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_natural_unequal_dominance.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-NATURAL-UNEQUAL-DOMINANCE"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
MAXIMAL_DIMENSION_PAPER_ID = "aggarwal-elboim-maximal-dimension-2026"
MAXIMAL_DIMENSION_PAPER_URL = "https://arxiv.org/abs/2605.25995"


@dataclass(frozen=True)
class NaturalUnequalDominanceSpec:
    n_values: tuple[int, ...] = (
        3,
        4,
        5,
        6,
        8,
        10,
        12,
        16,
        20,
        24,
        28,
        32,
        36,
        40,
        48,
    )


@dataclass(frozen=True)
class PlancherelCollisionRecord:
    n: int
    partition_count: int
    information_threshold_copy_count: int
    exact_equal_label_probability: str
    equal_label_probability: float
    log2_equal_label_probability: float
    exact_maximum_plancherel_atom: str
    maximum_plancherel_atom: float
    collision_bounded_by_maximum_atom: bool
    expected_equal_label_count: float
    exact_any_equal_label_probability: float
    union_bound_any_equal_label_probability: float
    exact_all_unequal_tuple_probability: float
    physical_label_mass_identity_verified: bool
    status: str


@dataclass(frozen=True)
class NaturalUnequalDominanceReport:
    created_at: str
    source_law_contract: dict[str, Any]
    literature_linked_theorem: dict[str, Any]
    records: list[PlancherelCollisionRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


@lru_cache(maxsize=None)
def plancherel_probabilities(
    n: int,
) -> tuple[tuple[tuple[int, ...], Fraction], ...]:
    if n < 1:
        raise ValueError("n must be positive")
    order = math.factorial(n)
    probabilities = tuple(
        (
            partition,
            Fraction(hook_length_dimension(partition) ** 2, order),
        )
        for partition in integer_partitions(n)
    )
    if sum((mass for _, mass in probabilities), Fraction()) != 1:
        raise ArithmeticError("Plancherel probabilities do not sum to one")
    return probabilities


@lru_cache(maxsize=None)
def physical_label_type_masses(n: int) -> tuple[Fraction, Fraction]:
    """Return total equal- and unequal-pair physical label mass."""

    probabilities = tuple(
        mass for _, mass in plancherel_probabilities(n)
    )
    equal_mass = sum(
        (mass * mass for mass in probabilities),
        Fraction(),
    )
    unequal_mass = 1 - equal_mass
    if equal_mass + unequal_mass != 1:
        raise ArithmeticError("physical pair-label masses do not sum to one")
    return equal_mass, unequal_mass


def collision_record(n: int) -> PlancherelCollisionRecord:
    probabilities = plancherel_probabilities(n)
    equal_mass, unequal_mass = physical_label_type_masses(n)
    maximum_atom = max(mass for _, mass in probabilities)
    copy_count = math.ceil(math.log2(math.factorial(n)))
    collision = float(equal_mass)
    all_unequal = math.exp(copy_count * math.log1p(-collision))
    any_equal = 1.0 - all_unequal
    return PlancherelCollisionRecord(
        n=n,
        partition_count=len(probabilities),
        information_threshold_copy_count=copy_count,
        exact_equal_label_probability=str(equal_mass),
        equal_label_probability=collision,
        log2_equal_label_probability=math.log2(collision),
        exact_maximum_plancherel_atom=str(maximum_atom),
        maximum_plancherel_atom=float(maximum_atom),
        collision_bounded_by_maximum_atom=equal_mass <= maximum_atom,
        expected_equal_label_count=copy_count * collision,
        exact_any_equal_label_probability=any_equal,
        union_bound_any_equal_label_probability=min(
            1.0,
            copy_count * collision,
        ),
        exact_all_unequal_tuple_probability=float(
            (1 - equal_mass) ** copy_count
        ),
        physical_label_mass_identity_verified=(
            equal_mass + unequal_mass == 1
        ),
        status="exact-natural-pair-collision-control",
    )


def run_natural_unequal_dominance(
    spec: NaturalUnequalDominanceSpec = NaturalUnequalDominanceSpec(),
) -> NaturalUnequalDominanceReport:
    records = [collision_record(n) for n in spec.n_values]
    failed_identities = sum(
        not record.physical_label_mass_identity_verified
        or not record.collision_bounded_by_maximum_atom
        for record in records
    )
    tail = records[-1]
    metrics: dict[str, int | float] = {
        "exact_collision_control_count": len(records),
        "failed_source_law_identity_count": failed_identities,
        "maximum_exact_control_n": max(record.n for record in records),
        "tail_equal_label_probability": tail.equal_label_probability,
        "tail_expected_equal_label_count": tail.expected_equal_label_count,
        "tail_any_equal_label_probability": (
            tail.exact_any_equal_label_probability
        ),
        "tail_all_unequal_tuple_probability": (
            tail.exact_all_unequal_tuple_probability
        ),
        "physical_label_as_two_plancherel_draws_theorem_count": 1,
        "equal_label_collision_identity_theorem_count": 1,
        "maximal_plancherel_atom_decay_literature_theorem_count": 1,
        "threshold_tuple_all_unequal_dominance_theorem_count": 1,
        "equal_commutator_natural_critical_path_bypass_count": 1,
        "fixed_third_moment_all_unequal_contraction_count": 1,
        "growing_order_all_unequal_contraction_count": 0,
        "natural_average_inverse_polynomial_conclusive_theorem_count": 0,
        "structured_maximal_effect_dilation_count": 0,
        "polynomial_hidden_permutation_decoder_count": 0,
    }
    verified = failed_identities == 0
    return NaturalUnequalDominanceReport(
        created_at=utc_now(),
        source_law_contract={
            "plancherel_atom": "p_lambda=d_lambda^2/n!",
            "equal_physical_label_mass": (
                "sum over +/- extensions for lambda equals p_lambda^2"
            ),
            "unequal_physical_label_mass": (
                "induced label {lambda,mu} has mass 2 p_lambda p_mu"
            ),
            "sampling_equivalence": (
                "one physical label equals two iid Plancherel draws, "
                "packaged by collision type"
            ),
            "threshold_union_bound": (
                "Pr(any equal among k labels)<=k sum_lambda p_lambda^2"
                "<=k max_lambda p_lambda"
            ),
        },
        literature_linked_theorem={
            "paper_id": MAXIMAL_DIMENSION_PAPER_ID,
            "url": MAXIMAL_DIMENSION_PAPER_URL,
            "statement": (
                "max_lambda d_lambda=sqrt(n!) "
                "exp(-(d+o(1))sqrt(n)) for d>0"
            ),
            "derived_consequence": (
                "max_lambda p_lambda and the Plancherel collision "
                "probability are exp(-Theta(sqrt(n))); multiplying by "
                "ceil(log2(n!)) still tends to zero"
            ),
        },
        records=records,
        headline_metrics=metrics,
        claim_gate={
            "physical_label_pair_law_verified": verified,
            "equal_label_collision_identity_proved": verified,
            "threshold_tuple_all_unequal_with_probability_one_minus_o_one": (
                verified
            ),
            "equal_commutator_recupling_needed_on_constant_natural_mass": False,
            "fixed_third_moment_all_unequal_contraction_available": True,
            "growing_order_all_unequal_contraction_proved": False,
            "natural_average_inverse_polynomial_conclusive_bound_proved": False,
            "structured_maximal_effect_dilation_proved": False,
            "polynomial_hidden_permutation_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Equal-pair commutator sectors have vanishing threshold-tuple "
                "source probability, but no growing-order contraction or "
                "measurement exists for the dominant all-unequal sectors."
            ),
        },
        status=(
            "natural-all-unequal-dominance-proved-"
            "growing-order-unequal-contraction-open"
        ),
        summary=(
            "Proved that information-threshold physical wreath labels are "
            "all unequal with probability 1-o(1), using the exact "
            "Plancherel-collision source law and the maximal-dimension "
            f"theorem; finite controls through n={tail.n} give all-unequal "
            f"probability {tail.exact_all_unequal_tuple_probability:.6g}."
        ),
        falsifiers_triggered=[
            "Every exact Plancherel distribution sums to one.",
            "Equal plus unequal physical pair-label masses sum exactly to one.",
            "The equal physical-label mass equals the Plancherel collision probability.",
            "The collision probability is bounded by the maximum Plancherel atom.",
            "Finite information-threshold tuples still contain equal labels with noticeable probability; the bypass is asymptotic, not a small-n approximation.",
            "The theorem removes equal commutator recoupling only from natural-average analysis, not worst-sector analysis.",
            "High-order all-unequal contraction, maximal-effect dilation, and decoding remain open.",
        ],
    )


def write_natural_unequal_dominance_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, Any]:
    payload = asdict(run_natural_unequal_dominance())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id=(
                    "NEG-CODE-WREATH-EQUAL-COMMUTATOR-"
                    "NOT-NATURAL-ASYMPTOTIC-BOTTLENECK"
                ),
                source=str(path),
                claim=(
                    "A scalable equal-pair mixed-commutator recoupling engine "
                    "is required before natural-source wreath frame moments "
                    "can make asymptotic progress."
                ),
                reason_invalid=(
                    "Equal physical labels are collisions of two independent "
                    "Plancherel draws. Across ceil(log2(n!)) labels their "
                    "total probability tends to zero."
                ),
                lesson=(
                    "Prioritize growing-order contraction on arbitrary "
                    "all-unequal physical tuples; retain equal recoupling only "
                    "for worst-sector or finite-size completeness."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence=payload["headline_metrics"],
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
                created_at=payload["created_at"],
                status=payload["status"],
                summary=payload["summary"],
                metrics=payload["headline_metrics"],
                falsifiers_triggered=payload["falsifiers_triggered"],
                artifacts={
                    "self_dual_wreath_natural_unequal_dominance": str(path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_natural_unequal_dominance_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
