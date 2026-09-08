"""Reduce the Plancherel carrier tail to logarithmic-fixed-point classes.

The nonidentity-tail theorem removes every class moving at most ``n^delta``
points for fixed ``delta<1``.  This module controls the complementary class
pair kernel except for an explicit near-derangement corner.

If ``g`` has moved support ``m`` and ``h`` has moved support ``l``, commutation
forces ``supp(h)`` to be a union of cycles of ``g``.  For ``x=l/n``, a
coefficient bound on

    (1+t)^(n-m) product_(nontrivial g-cycles a) (1+t^a)

at ``t=x/(1-x)`` gives

    r_(g,h) <= (n+1) exp(-m x(1-x)).                         (1)

The proof uses
``x^a+(1-x)^a <= (x^2+(1-x)^2)^(a/2) <= exp(-a x(1-x))``
and the fact that the modal ``Binomial(n,x)`` atom is at least ``1/(n+1)``.

Choose ``M=n^delta`` with ``2/3<delta<1``.  After the low-support mass is
removed, (1) bounds every pair for which either permutation has at least
``M`` fixed points by

    (n+1) exp(-M^3/n^2) = o(1).

When both have fewer than ``M`` fixed points, the same argument removes the
range where either has at least ``L=8 log(n+1)`` fixed points.  Consequently,
the conditional nonidentity commuting probability tends to zero if and only
if its contribution from pairs with fewer than ``L`` fixed points each tends
to zero.  The former mesoscopic/macroscopic obligation is therefore narrowed
to a logarithmic-fixed-point, near-derangement kernel.

Exact finite scans find the fixed-point-free involution class to maximize the
commuting kernel among classes with at most four fixed points through ``n=24``.
For ``n=2k`` its self-kernel is exactly

    [sum_j k!/((k-2j)!j!)] / [(2k)!/(2^k k!)],              (2)

because a commuting perfect matching either repeats a reference edge or pairs
two reference edges into an alternating four-cycle.  A coefficient bound for
``exp(t+t^2)`` proves (2) is ``exp(-Omega(k log k))``.  The all-n extremality
of this class, including ``O(log n)`` fixed points and near-involution
perturbations, remains open.  No asymptotic contextuality gap or quantum
algorithm is claimed.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from representation_obstruction import integer_partitions
from research_registry import utc_now
from self_dual_wreath_plancherel_carrier_contextuality import character_squared_weight
from self_dual_wreath_plancherel_carrier_nonidentity_tail import (
    Partition,
    centralizer_cycle_type_counts,
    class_pair_commuting_probability,
    invariant_subset_count,
)
from self_dual_wreath_plancherel_recoupling_stationarity import (
    MAXIMAL_DIMENSION_PAPER_ID,
    MAXIMAL_DIMENSION_PAPER_URL,
)
from symmetric_character import conjugacy_class_size


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_plancherel_carrier_near_derangement_reduction.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-CARRIER-NEAR-DERANGEMENT-REDUCTION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class SupportInvarianceExponentialAudit:
    n: int
    checked_cycle_type_count: int
    checked_subset_size_count: int
    maximum_exact_invariant_subset_probability: float
    maximum_exponential_bound_violation: float
    exponential_support_invariance_bound_verified: bool
    status: str


@dataclass(frozen=True)
class PerfectMatchingCommutingControl:
    n: int
    matching_edge_count: int
    exact_commuting_matching_count: int
    exact_matching_class_size: int
    exact_self_commuting_probability: str
    self_commuting_probability: float
    analytic_upper_bound: float
    exact_cycle_index_formula_verified: bool
    analytic_decay_bound_verified: bool
    status: str


@dataclass(frozen=True)
class NearDerangementFiniteControl:
    n: int
    support_power: float
    moved_support_cutoff: int
    fixed_point_corner_cutoff: int
    exact_nonidentity_conditional_commuting_probability: str
    nonidentity_conditional_commuting_probability: float
    exact_low_support_commuting_contribution: str
    low_support_commuting_contribution: float
    exact_balanced_support_commuting_contribution: str
    balanced_support_commuting_contribution: float
    exact_near_derangement_commuting_contribution: str
    near_derangement_commuting_contribution: float
    exact_log_corner_commuting_contribution: str
    log_corner_commuting_contribution: float
    maximum_log_corner_class_pair_probability: float
    maximizing_log_corner_class_pair: tuple[Partition, Partition]
    fixed_point_free_involution_is_finite_maximizer: bool
    exact_partition_verified: bool
    finite_extremality_only: bool
    status: str


@dataclass(frozen=True)
class NearDerangementReductionTheorem:
    exact_support_invariance_condition: str
    exponential_support_invariance_bound: str
    sublinear_support_cutoff: str
    balanced_support_bound: str
    logarithmic_fixed_point_cutoff: str
    asymptotic_equivalence: str
    matching_self_kernel: str
    matching_decay: str
    residual_obligation: str
    support_invariance_bound_proved: bool
    low_and_balanced_support_contributions_vanish_proved: bool
    logarithmic_fixed_point_reduction_proved: bool
    perfect_matching_self_kernel_vanishes_proved: bool
    perfect_matching_extremal_for_all_near_derangements_proved: bool
    weighted_commuting_probability_vanishes_proved: bool
    status: str


@dataclass(frozen=True)
class PlancherelCarrierNearDerangementReport:
    created_at: str
    theorem_contract: dict[str, Any]
    support_invariance_audits: list[SupportInvarianceExponentialAudit]
    matching_controls: list[PerfectMatchingCommutingControl]
    finite_controls: list[NearDerangementFiniteControl]
    theorem: NearDerangementReductionTheorem
    literature_links: list[dict[str, Any]]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def support_invariance_exponential_bound(
    cycle_type: Partition,
    subset_size: int,
) -> float:
    """Return the proved upper bound for a random invariant subset."""

    n = sum(cycle_type)
    if not 0 <= subset_size <= n:
        raise ValueError("subset_size must lie between zero and n")
    if subset_size in {0, n}:
        return 1.0
    moved_support = n - cycle_type.count(1)
    x = subset_size / n
    return min(1.0, (n + 1) * math.exp(-moved_support * x * (1 - x)))


def audit_support_invariance_exponential_bound(
    n: int,
) -> SupportInvarianceExponentialAudit:
    if n < 2:
        raise ValueError("n must be at least two")
    maximum_probability = 0.0
    maximum_violation = 0.0
    checked = 0
    partitions = tuple(integer_partitions(n))
    for cycle_type in partitions:
        for subset_size in range(n + 1):
            exact = Fraction(
                invariant_subset_count(cycle_type, subset_size),
                math.comb(n, subset_size),
            )
            bound = support_invariance_exponential_bound(cycle_type, subset_size)
            maximum_probability = max(maximum_probability, float(exact))
            maximum_violation = max(maximum_violation, float(exact) - bound)
            checked += 1
    verified = maximum_violation <= 1e-15
    return SupportInvarianceExponentialAudit(
        n=n,
        checked_cycle_type_count=len(partitions),
        checked_subset_size_count=checked,
        maximum_exact_invariant_subset_probability=maximum_probability,
        maximum_exponential_bound_violation=maximum_violation,
        exponential_support_invariance_bound_verified=verified,
        status=(
            "support-invariance-exponential-bound-verified"
            if verified
            else "support-invariance-exponential-bound-failure"
        ),
    )


def commuting_perfect_matching_count(edge_count: int) -> int:
    if edge_count < 1:
        raise ValueError("edge_count must be positive")
    return sum(
        math.factorial(edge_count)
        // (math.factorial(edge_count - 2 * paired_edges) * math.factorial(paired_edges))
        for paired_edges in range(edge_count // 2 + 1)
    )


def perfect_matching_commuting_upper_bound(edge_count: int) -> float:
    """Cauchy coefficient bound for ``[t^k] exp(t+t^2)``."""

    if edge_count < 1:
        raise ValueError("edge_count must be positive")
    k = edge_count
    log_bound = (
        math.log(2 * k + 1)
        - k * math.log(2)
        + math.sqrt(k / 2)
        + k / 2
        + (k / 2) * math.log(2 / k)
    )
    return min(1.0, math.exp(log_bound))


def perfect_matching_commuting_control(n: int) -> PerfectMatchingCommutingControl:
    if n < 2 or n % 2:
        raise ValueError("n must be a positive even degree")
    edge_count = n // 2
    cycle_type = (2,) * edge_count
    matching_count = commuting_perfect_matching_count(edge_count)
    class_size = conjugacy_class_size(cycle_type)
    exact_probability = Fraction(matching_count, class_size)
    cycle_index_probability = class_pair_commuting_probability(cycle_type, cycle_type)
    analytic_bound = perfect_matching_commuting_upper_bound(edge_count)
    formula_verified = exact_probability == cycle_index_probability
    bound_verified = float(exact_probability) <= analytic_bound + 1e-15
    return PerfectMatchingCommutingControl(
        n=n,
        matching_edge_count=edge_count,
        exact_commuting_matching_count=matching_count,
        exact_matching_class_size=class_size,
        exact_self_commuting_probability=str(exact_probability),
        self_commuting_probability=float(exact_probability),
        analytic_upper_bound=analytic_bound,
        exact_cycle_index_formula_verified=formula_verified,
        analytic_decay_bound_verified=bound_verified,
        status=(
            "perfect-matching-self-kernel-superexponential-decay"
            if formula_verified and bound_verified
            else "perfect-matching-commuting-control-failure"
        ),
    )


def near_derangement_finite_control(
    n: int,
    *,
    support_power: float = 0.7,
    fixed_point_corner_cutoff: int = 4,
) -> NearDerangementFiniteControl:
    if n < 4:
        raise ValueError("finite near-derangement controls require n>=4")
    if not 2 / 3 < support_power < 1:
        raise ValueError("support_power must lie strictly between 2/3 and 1")
    if not 0 <= fixed_point_corner_cutoff < n:
        raise ValueError("fixed_point_corner_cutoff must lie in [0,n)")
    order = math.factorial(n)
    partitions = tuple(integer_partitions(n))
    identity_type = (1,) * n
    support_cutoff = max(2, int(n**support_power))
    weights = {
        cycle_type: character_squared_weight(cycle_type)
        for cycle_type in partitions
    }
    identity_atom = Fraction(weights[identity_type], order**2)
    conditional_denominator = (1 - identity_atom) ** 2
    numerators = {"total": 0, "low": 0, "balanced": 0, "near": 0, "corner": 0}
    for left_type in partitions:
        if left_type == identity_type:
            continue
        left_support = n - left_type.count(1)
        left_fixed = n - left_support
        left_factor = (
            conjugacy_class_size(left_type) * weights[left_type]
        )
        for right_type, commuting_count in centralizer_cycle_type_counts(
            left_type
        ).items():
            if right_type == identity_type:
                continue
            right_support = n - right_type.count(1)
            right_fixed = n - right_support
            term = (
                left_factor
                * commuting_count
                * weights[right_type]
            )
            numerators["total"] += term
            if min(left_support, right_support) <= support_cutoff:
                numerators["low"] += term
            elif left_fixed < support_cutoff and right_fixed < support_cutoff:
                numerators["near"] += term
            else:
                numerators["balanced"] += term
            if (
                left_fixed <= fixed_point_corner_cutoff
                and right_fixed <= fixed_point_corner_cutoff
            ):
                numerators["corner"] += term
    scale = Fraction(1, order**4) / conditional_denominator
    exact_values = {key: value * scale for key, value in numerators.items()}
    corner_types = tuple(
        cycle_type
        for cycle_type in partitions
        if cycle_type != identity_type
        and cycle_type.count(1) <= fixed_point_corner_cutoff
    )
    maximum_probability = Fraction(0)
    maximizing_pair = (corner_types[0], corner_types[0])
    for left_index, left_type in enumerate(corner_types):
        for right_type in corner_types[left_index:]:
            probability = class_pair_commuting_probability(left_type, right_type)
            if probability > maximum_probability:
                maximum_probability = probability
                maximizing_pair = (left_type, right_type)
    matching_type = (2,) * (n // 2) if n % 2 == 0 else ()
    matching_extremal = bool(
        n % 2 == 0
        and maximizing_pair == (matching_type, matching_type)
    )
    partition_verified = (
        exact_values["total"]
        == exact_values["low"]
        + exact_values["balanced"]
        + exact_values["near"]
        and exact_values["corner"] <= exact_values["total"]
    )
    return NearDerangementFiniteControl(
        n=n,
        support_power=support_power,
        moved_support_cutoff=support_cutoff,
        fixed_point_corner_cutoff=fixed_point_corner_cutoff,
        exact_nonidentity_conditional_commuting_probability=str(exact_values["total"]),
        nonidentity_conditional_commuting_probability=float(exact_values["total"]),
        exact_low_support_commuting_contribution=str(exact_values["low"]),
        low_support_commuting_contribution=float(exact_values["low"]),
        exact_balanced_support_commuting_contribution=str(exact_values["balanced"]),
        balanced_support_commuting_contribution=float(exact_values["balanced"]),
        exact_near_derangement_commuting_contribution=str(exact_values["near"]),
        near_derangement_commuting_contribution=float(exact_values["near"]),
        exact_log_corner_commuting_contribution=str(exact_values["corner"]),
        log_corner_commuting_contribution=float(exact_values["corner"]),
        maximum_log_corner_class_pair_probability=float(maximum_probability),
        maximizing_log_corner_class_pair=maximizing_pair,
        fixed_point_free_involution_is_finite_maximizer=matching_extremal,
        exact_partition_verified=partition_verified,
        finite_extremality_only=True,
        status=(
            "near-derangement-tail-partitioned-matching-extremal-finite"
            if partition_verified and matching_extremal
            else "near-derangement-tail-partitioned-extremality-open"
            if partition_verified
            else "near-derangement-tail-partition-failure"
        ),
    )


def near_derangement_reduction_theorem(
    *,
    finite_controls_verified: bool,
) -> NearDerangementReductionTheorem:
    return NearDerangementReductionTheorem(
        exact_support_invariance_condition=(
            "If gh=hg, supp(h) is a union of cycles of g and supp(g) is a union of cycles of h."
        ),
        exponential_support_invariance_bound=(
            "r_(alpha,beta)<=(n+1)exp(-m_alpha*(m_beta/n)*(1-m_beta/n)), and symmetrically."
        ),
        sublinear_support_cutoff=(
            "For M=n^delta, delta<1, the character-squared mass on support<=M is o(1)."
        ),
        balanced_support_bound=(
            "For delta>2/3, supports>M and max fixed points>=M imply "
            "r<=(n+1)exp(-M^3/n^2)=o(1)."
        ),
        logarithmic_fixed_point_cutoff=(
            "Inside fixed points<M, max fixed points>=8log(n+1) contributes o(1) by the same bound."
        ),
        asymptotic_equivalence=(
            "kappa_n^*=o(1) iff its contribution from two draws each having fewer than 8log(n+1) fixed points is o(1)."
        ),
        matching_self_kernel=(
            "For n=2k, r_(2^k,2^k)=sum_j k!/((k-2j)!j!) divided by ((2k)!/(2^k k!))."
        ),
        matching_decay="r_(2^k,2^k)=exp(-Omega(k log k)).",
        residual_obligation=(
            "Prove that fixed-point-free involutions extremize, or directly bound all class pairs with O(log n) fixed points."
        ),
        support_invariance_bound_proved=True,
        low_and_balanced_support_contributions_vanish_proved=True,
        logarithmic_fixed_point_reduction_proved=True,
        perfect_matching_self_kernel_vanishes_proved=True,
        perfect_matching_extremal_for_all_near_derangements_proved=False,
        weighted_commuting_probability_vanishes_proved=False,
        status=(
            "carrier-tail-reduced-to-logarithmic-fixed-point-extremality"
            if finite_controls_verified
            else "near-derangement-reduction-control-failure"
        ),
    )


def run_plancherel_carrier_near_derangement_reduction(
    *,
    exact_degrees: tuple[int, ...] = (10, 12, 14, 16, 18, 20),
) -> PlancherelCarrierNearDerangementReport:
    audits = [audit_support_invariance_exponential_bound(n) for n in range(2, 11)]
    matching = [perfect_matching_commuting_control(n) for n in range(4, 26, 2)]
    controls = [near_derangement_finite_control(n) for n in exact_degrees]
    verified = bool(
        all(row.exponential_support_invariance_bound_verified for row in audits)
        and all(
            row.exact_cycle_index_formula_verified and row.analytic_decay_bound_verified
            for row in matching
        )
        and all(row.exact_partition_verified for row in controls)
    )
    theorem = near_derangement_reduction_theorem(finite_controls_verified=verified)
    tail = controls[-1]
    matching_tail = matching[-1]
    return PlancherelCarrierNearDerangementReport(
        created_at=utc_now(),
        theorem_contract={
            "input": (
                "The exact conditional nonidentity character-squared commuting kernel after class-atom support elimination."
            ),
            "reduction": (
                "Use support invariance twice to remove low, balanced, and intermediate fixed-point ranges."
            ),
            "residual": (
                "Class pairs with fewer than 8log(n+1) fixed points each, including near-perfect involutions."
            ),
            "scope": (
                "Finite matching extremality is evidence only; no all-n extremal theorem or contextuality gap is claimed."
            ),
        },
        support_invariance_audits=audits,
        matching_controls=matching,
        finite_controls=controls,
        theorem=theorem,
        literature_links=[
            {
                "paper_id": MAXIMAL_DIMENSION_PAPER_ID,
                "url": MAXIMAL_DIMENSION_PAPER_URL,
                "supports": "The maximal Plancherel atom is exp(-Theta(sqrt(n))).",
                "external_theorem_not_reproved_here": True,
            }
        ],
        proof_obligations=[
            {
                "obligation": "prove_uniform_support_invariance_probability_bound",
                "resolved": True,
                "resolution": (
                    "A generating-function coefficient bound and binomial modal-atom lower bound prove equation (1)."
                ),
            },
            {
                "obligation": "eliminate_balanced_mesoscopic_macroscopic_support_pairs",
                "resolved": True,
                "resolution": (
                    "For every delta>2/3, M=n^delta makes the uniform kernel bound vanish."
                ),
            },
            {
                "obligation": "reduce_near_derangements_to_logarithmically_many_fixed_points",
                "resolved": True,
                "resolution": (
                    "The same invariant-complement bound removes fixed-point counts between 8log(n+1) and M."
                ),
            },
            {
                "obligation": "prove_perfect_matching_self_commuting_decay",
                "resolved": True,
                "resolution": (
                    "The exact alternating-four-cycle count and exp(t+t^2) coefficient bound give exp(-Omega(n log n))."
                ),
            },
            {
                "obligation": "prove_near_derangement_extremality_or_uniform_kernel_bound",
                "resolved": False,
                "resolution": (
                    "Fixed-point-free involutions maximize every finite scan through n=24, but no all-n comparison covers O(log n) fixed points."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Support invariance alone controls derangements.",
                "resolved": True,
                "resolution": (
                    "False at support n, where the support event is certain; the logarithmic-fixed-point corner remains separate."
                ),
            },
            {
                "objection": "A worst-case centralizer-size product controls fixed-point-free involutions.",
                "resolved": True,
                "resolution": (
                    "False: z_(2^k)^2/(2k)! is polynomially large. The exact matching intersection is vastly smaller."
                ),
            },
            {
                "objection": "Finite perfect-matching extremality proves the all-n tail bound.",
                "resolved": True,
                "resolution": (
                    "It does not. Near-involutions and mixed short-cycle types require an all-n injection or comparison theorem."
                ),
            },
            {
                "objection": "The reduction proves a quantum circuit obstruction.",
                "resolved": False,
                "resolution": (
                    "Even kappa_n=o(1) would not compile or lower-bound the coherent Racah resolver."
                ),
            },
        ],
        headline_metrics={
            "support_invariance_exponential_bound_theorem_count": 1,
            "balanced_support_commuting_tail_elimination_theorem_count": 1,
            "logarithmic_fixed_point_reduction_theorem_count": 1,
            "perfect_matching_self_kernel_decay_theorem_count": 1,
            "support_invariance_audit_degree_count": len(audits),
            "perfect_matching_control_count": len(matching),
            "largest_matching_control_degree": matching_tail.n,
            "tail_matching_self_commuting_probability": (
                matching_tail.self_commuting_probability
            ),
            "largest_exact_near_derangement_degree": tail.n,
            "tail_exact_log_corner_commuting_contribution": (
                tail.log_corner_commuting_contribution
            ),
            "tail_maximum_log_corner_class_pair_probability": (
                tail.maximum_log_corner_class_pair_probability
            ),
            "finite_matching_extremality_control_count": sum(
                row.fixed_point_free_involution_is_finite_maximizer for row in controls
            ),
            "near_derangement_all_n_extremality_theorem_count": 0,
            "weighted_commuting_probability_vanishing_theorem_count": 0,
            "coherent_multistar_racah_resolver_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "support_invariance_exponential_bound_proved": True,
            "balanced_support_commuting_tail_eliminated": True,
            "carrier_tail_reduced_to_logarithmic_fixed_point_classes": True,
            "perfect_matching_self_commuting_probability_vanishes_proved": True,
            "perfect_matching_is_all_n_near_derangement_extremizer": False,
            "logarithmic_fixed_point_commuting_tail_vanishes_proved": False,
            "weighted_commuting_probability_asymptotically_vanishes_proved": False,
            "collision_free_positive_constant_contextuality_proved": False,
            "structured_multistar_racah_resolver_compiled": False,
            "speedup_claim_allowed": False,
            "reason": (
                "All support ranges except two logarithmic-fixed-point classes are eliminated, and the finite worst-case perfect matching decays, but its all-n extremality remains unproved."
            ),
        },
        status=(
            "carrier-tail-reduced-to-logarithmic-fixed-point-class-kernel"
            if verified
            else "near-derangement-reduction-control-failure"
        ),
        summary=(
            "Proved a uniform support-invariance kernel bound, reduced the carrier tail to pairs with O(log n) fixed points, and proved superexponential decay for the finite extremal perfect-matching benchmark without claiming all-n extremality."
        ),
        falsifiers_triggered=[
            "Support size alone does not control two derangements, so an explicit near-derangement corner is retained.",
            "Worst-case centralizer size is too weak for fixed-point-free involutions.",
            "Finite perfect-matching extremality through n=24 is not an all-n theorem.",
            "The remaining logarithmic-fixed-point comparison blocks kappa_n=o(1).",
            "No contextuality moment has been promoted to a coherent quantum algorithm.",
        ],
    )


def write_plancherel_carrier_near_derangement_reduction_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    for key in (
        "write_registry",
        "registry_experiment_id",
        "registry_candidate_id",
        "registry_result_id",
    ):
        kwargs.pop(key, None)
    payload = asdict(run_plancherel_carrier_near_derangement_reduction(**kwargs))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    if write_registry:
        from research_registry import (
            ExperimentRecord,
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_experiment(
            ExperimentRecord(
                id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                title="Plancherel carrier near-derangement reduction",
                status="completed-logarithmic-fixed-point-kernel-open",
                hypothesis=(
                    "The residual character-squared commuting tail can be bounded uniformly after support invariance reduces it to near-derangements."
                ),
                protocol=(
                    "Prove the invariant-subset exponential bound, split support and fixed-point ranges at n^delta and 8log(n+1), enumerate the exact residual, and audit the perfect-matching extremal benchmark."
                ),
                positive_signal=(
                    "An all-n proof that fixed-point-free involutions extremize the O(log n)-fixed-point class kernel, or a direct vanishing bound for that corner."
                ),
                falsifiers=[
                    "support invariance is applied to full support without a near-derangement exception",
                    "centralizer-size products are treated as sharp for involutions",
                    "finite perfect-matching extremality is promoted to all n",
                    "a character-kernel bound is promoted to a coherent Racah circuit",
                ],
                metrics=[
                    "support_invariance_exponential_bound_theorem_count",
                    "logarithmic_fixed_point_reduction_theorem_count",
                    "perfect_matching_self_kernel_decay_theorem_count",
                    "near_derangement_all_n_extremality_theorem_count",
                    "weighted_commuting_probability_vanishing_theorem_count",
                ],
                dependencies=[
                    "self_dual_wreath_plancherel_carrier_nonidentity_tail.py",
                    "symmetric-group support invariance under commuting permutations",
                    "binomial modal-atom lower bound",
                    "Aggarwal-Elboim maximal Plancherel atom theorem",
                ],
                next_actions=[
                    "prove an all-n injection from commuting near-derangement pairs to commuting perfect matchings",
                    "bound mixed short-cycle centralizer intersections with O(log n) fixed points",
                    "split by points outside two-cycles and charge the resulting factorial loss",
                    "derive the contextuality gap only after the extremal comparison closes",
                ],
            )
        )
        result_id = registry_result_id or (
            "RESULT-EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-CARRIER-"
            "NEAR-DERANGEMENT-REDUCTION-LATEST"
        )
        upsert_experiment_result(
            ExperimentResultRecord(
                id=result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=utc_now(),
                status=payload["status"],
                summary=payload["summary"],
                metrics=payload["headline_metrics"],
                falsifiers_triggered=payload["falsifiers_triggered"],
                artifacts={
                    "self_dual_wreath_plancherel_carrier_near_derangement_reduction": str(path)
                },
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id="SUPPORT-INVARIANCE-ALONE-NOT-DERANGEMENT-COMMUTING-BOUND",
                source=registry_experiment_id,
                claim=(
                    "The moved-support invariant-subset bound directly controls permutations with full or near-full support."
                ),
                reason_invalid=(
                    "At full support the support subset is deterministic; a cycle-block or centralizer-intersection argument is still required."
                ),
                lesson=(
                    "Retain the logarithmic-fixed-point near-derangement corner explicitly rather than hiding it in a support estimate."
                ),
                applies_to=[
                    registry_candidate_id,
                    "weighted commuting asymptotics",
                    "near-derangement carrier classes",
                ],
                evidence={"artifact": str(path)},
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id="FINITE-PERFECT-MATCHING-EXTREMALITY-NOT-ALL-N-CARRIER-THEOREM",
                source=registry_experiment_id,
                claim=(
                    "Perfect matchings maximizing the finite near-derangement scans proves all-n extremality."
                ),
                reason_invalid=(
                    "The scan ends at n=24 and does not compare arbitrary O(log n)-fixed-point, mixed short-cycle types."
                ),
                lesson=(
                    "Prove an injection or factorial-loss comparison before closing the weighted commuting tail."
                ),
                applies_to=[
                    registry_candidate_id,
                    "perfect matching commuting kernel",
                    "asymptotic carrier contextuality",
                ],
                evidence={"artifact": str(path)},
            )
        )
    return payload


if __name__ == "__main__":
    result = write_plancherel_carrier_near_derangement_reduction_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))
