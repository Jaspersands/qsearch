"""Exact centralizer cycle index and the residual Plancherel carrier tail.

The natural carrier-contextuality reduction leaves the central probability

    kappa_n = Pr_(g,h iid mu_n)[gh=hg],

where ``mu_n(g)=(n!)^-2 sum_lambda d_lambda^2 chi_lambda(g)^2``.  Direct
enumeration previously stopped at ``n=8``.  This module replaces permutation
enumeration by the exact cycle index of

    C_{S_n}(g) = product_i C_i wr S_{m_i(g)}.

If a cycle of length ``k`` in the ``S_{m_i}`` component has net rotation
``r mod i``, its action on the underlying ``ik`` points has
``gcd(i,r)`` cycles of length ``ik/gcd(i,r)``.  There are ``i^(k-1)`` rotation
assignments with each prescribed net rotation.  Dynamic programming over
these wreath-product blocks returns the exact number of centralizer elements
of every cycle type and evaluates ``kappa_n`` through ``n=20`` cheaply.

Let ``c_n=mu_n(e)`` and condition both draws to be nonidentity.  Then exactly

    kappa_n = 2 c_n - c_n^2 + (1-c_n)^2 kappa_n^*.          (1)

Column orthogonality also gives a useful all-n domination.  If ``Q_n(C)`` is
the ``mu_n`` mass of conjugacy class ``C`` and ``p_max(n)`` is the largest
Plancherel atom, then

    Q_n(C) <= p_max(n).                                    (2)

Indeed ``sum_lambda chi_lambda(C)^2=z_C`` and hence
``sum d_lambda^2 chi_lambda(C)^2 <= d_max^2 z_C``.  The
Aggarwal--Elboim maximal-dimension theorem makes ``p_max(n)``
``exp(-Theta(sqrt(n)))``.  Since the number of cycle types moving at most
``n^delta`` points is ``exp(O(n^(delta/2)))``, (2) proves that for every fixed
``delta<1`` the conditional ``mu_n`` mass on support at most ``n^delta``
vanishes.  It also proves ``c_n->0``.

Thus neither the identity atom nor fixed/sublinear moved support can sustain
the asymptotic commuting probability.  The remaining theorem obligation is
the commuting mass where both permutations move more than ``n^delta`` points.
Finite exact data says low support supplies most of the residual tail through
``n=20``; the new asymptotic bound proves that this finite mechanism cannot be
extrapolated.  No asymptotic contextuality gap, Racah resolver, PGM, decoder,
or speedup is claimed.
"""

from __future__ import annotations

import itertools
import json
import math
from collections import Counter
from dataclasses import asdict, dataclass
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from typing import Any

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_character_moments import permutation_cycle_type
from self_dual_wreath_commutator_sector_filter_no_go import cycle_centralizer_size
from self_dual_wreath_plancherel_carrier_contextuality import (
    Partition,
    _canonical_permutation,
    _commute,
    character_squared_weight,
)
from self_dual_wreath_plancherel_recoupling_stationarity import (
    MAXIMAL_DIMENSION_PAPER_ID,
    MAXIMAL_DIMENSION_PAPER_URL,
)
from symmetric_character import conjugacy_class_size


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_plancherel_carrier_nonidentity_tail.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-CARRIER-NONIDENTITY-TAIL"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class CentralizerCycleIndexAudit:
    n: int
    conjugacy_class_count: int
    checked_class_count: int
    maximum_cycle_type_count_residual: int
    maximum_commuting_kernel_symmetry_residual: str
    maximum_support_invariance_bound_violation: str
    exact_cycle_index_verified: bool
    status: str


@dataclass(frozen=True)
class SupportCutoffControl:
    n: int
    moved_support_cutoff: int
    eligible_nonidentity_cycle_type_count: int
    exact_conditional_low_support_mass: str
    conditional_low_support_mass: float
    exact_class_atom_domination_bound: str
    class_atom_domination_bound: float
    exact_conditional_commuting_mass_with_low_support: str
    conditional_commuting_mass_with_low_support: float
    exact_conditional_high_high_commuting_mass: str
    conditional_high_high_commuting_mass: float
    residual_tail_fraction_captured_by_low_support: float
    exact_union_bound: str
    union_bound: float
    class_atom_domination_verified: bool
    commuting_tail_decomposition_verified: bool
    status: str


@dataclass(frozen=True)
class ExactNonidentityTailControl:
    n: int
    group_order: int
    conjugacy_class_count: int
    centralizer_cycle_type_state_count: int
    exact_identity_atom: str
    identity_atom: float
    exact_maximum_plancherel_atom: str
    maximum_plancherel_atom: float
    exact_maximum_class_mass: str
    maximum_class_mass: float
    exact_weighted_commuting_probability: str
    weighted_commuting_probability: float
    exact_identity_pair_contribution: str
    identity_pair_contribution: float
    exact_nonidentity_conditional_commuting_probability: str
    nonidentity_conditional_commuting_probability: float
    identity_share_of_total_commuting_probability: float
    exact_identity_tail_decomposition_verified: bool
    class_mass_domination_verified: bool
    support_cutoffs: tuple[SupportCutoffControl, ...]
    status: str


@dataclass(frozen=True)
class PlancherelCarrierTailTheorem:
    centralizer_structure: str
    wreath_cycle_rule: str
    exact_commuting_formula: str
    identity_tail_decomposition: str
    class_mass_domination: str
    identity_atom_asymptotic: str
    sublinear_support_asymptotic: str
    residual_obligation: str
    exact_cycle_index_proved: bool
    identity_contribution_vanishes_proved: bool
    every_sublinear_support_window_vanishes_proved: bool
    mesoscopic_macroscopic_commuting_tail_vanishes_proved: bool
    weighted_commuting_probability_vanishes_proved: bool
    status: str


@dataclass(frozen=True)
class PlancherelCarrierNonidentityTailReport:
    created_at: str
    theorem_contract: dict[str, Any]
    cycle_index_audits: list[CentralizerCycleIndexAudit]
    exact_tail_controls: list[ExactNonidentityTailControl]
    theorem: PlancherelCarrierTailTheorem
    literature_links: list[dict[str, Any]]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _euler_totient(value: int) -> int:
    result = value
    remainder = value
    prime = 2
    while prime * prime <= remainder:
        if remainder % prime == 0:
            while remainder % prime == 0:
                remainder //= prime
            result -= result // prime
        prime += 1
    if remainder > 1:
        result -= result // remainder
    return result


@lru_cache(maxsize=None)
def _divisors(value: int) -> tuple[int, ...]:
    return tuple(divisor for divisor in range(1, value + 1) if value % divisor == 0)


def _merge_cycle_types(left: Partition, right: Partition) -> Partition:
    return tuple(sorted(left + right, reverse=True))


@lru_cache(maxsize=None)
def wreath_block_cycle_type_counts(
    base_cycle_length: int,
    multiplicity: int,
) -> dict[Partition, int]:
    """Cycle-type counts in ``C_i wr S_m`` on ``i*m`` points."""

    if base_cycle_length < 1 or multiplicity < 1:
        raise ValueError("base cycle length and multiplicity must be positive")
    output: Counter[Partition] = Counter()
    for block_permutation_type in integer_partitions(multiplicity):
        block_permutation_count = (
            math.factorial(multiplicity)
            // cycle_centralizer_size(block_permutation_type)
        )
        current: dict[Partition, int] = {(): block_permutation_count}
        for block_orbit_length in block_permutation_type:
            updated: Counter[Partition] = Counter()
            for prefix, prefix_count in current.items():
                for gcd_value in _divisors(base_cycle_length):
                    output_cycle_length = (
                        block_orbit_length * base_cycle_length // gcd_value
                    )
                    output_type = (output_cycle_length,) * gcd_value
                    net_rotation_count = _euler_totient(
                        base_cycle_length // gcd_value
                    )
                    rotation_assignment_count = (
                        base_cycle_length ** (block_orbit_length - 1)
                    )
                    updated[_merge_cycle_types(prefix, output_type)] += (
                        prefix_count
                        * net_rotation_count
                        * rotation_assignment_count
                    )
            current = dict(updated)
        output.update(current)
    expected_order = base_cycle_length**multiplicity * math.factorial(multiplicity)
    if sum(output.values()) != expected_order:
        raise ArithmeticError("wreath-block cycle index failed to normalize")
    return dict(output)


@lru_cache(maxsize=None)
def centralizer_cycle_type_counts(cycle_type: Partition) -> dict[Partition, int]:
    """Count every cycle type inside the centralizer of ``cycle_type``."""

    if not cycle_type or tuple(sorted(cycle_type, reverse=True)) != cycle_type:
        raise ValueError("cycle_type must be a nonempty integer partition")
    multiplicities = Counter(cycle_type)
    current: dict[Partition, int] = {(): 1}
    for base_cycle_length, multiplicity in multiplicities.items():
        updated: Counter[Partition] = Counter()
        for prefix, prefix_count in current.items():
            for block_type, block_count in wreath_block_cycle_type_counts(
                base_cycle_length,
                multiplicity,
            ).items():
                updated[_merge_cycle_types(prefix, block_type)] += (
                    prefix_count * block_count
                )
        current = dict(updated)
    if sum(current.values()) != cycle_centralizer_size(cycle_type):
        raise ArithmeticError("centralizer cycle index failed to normalize")
    return current


def class_pair_commuting_probability(
    left_type: Partition,
    right_type: Partition,
) -> Fraction:
    """Exact probability that uniform elements of two classes commute."""

    if sum(left_type) != sum(right_type):
        raise ValueError("cycle types must have the same degree")
    count = centralizer_cycle_type_counts(left_type).get(right_type, 0)
    return Fraction(count, conjugacy_class_size(right_type))


def invariant_subset_count(cycle_type: Partition, subset_size: int) -> int:
    """Number of subsets of the requested size invariant under a permutation."""

    n = sum(cycle_type)
    if not 0 <= subset_size <= n:
        return 0
    counts = [0] * (subset_size + 1)
    counts[0] = 1
    for cycle_length in cycle_type:
        for size in range(subset_size, cycle_length - 1, -1):
            counts[size] += counts[size - cycle_length]
    return counts[subset_size]


def class_pair_commuting_upper_bound(
    left_type: Partition,
    right_type: Partition,
) -> Fraction:
    """Support-invariance and centralizer-size upper bound for a class pair."""

    n = sum(left_type)
    if n != sum(right_type):
        raise ValueError("cycle types must have the same degree")
    left_support = n - left_type.count(1)
    right_support = n - right_type.count(1)
    left_invariance = Fraction(
        invariant_subset_count(left_type, right_support),
        math.comb(n, right_support),
    )
    right_invariance = Fraction(
        invariant_subset_count(right_type, left_support),
        math.comb(n, left_support),
    )
    centralizer_bound = Fraction(
        cycle_centralizer_size(left_type)
        * cycle_centralizer_size(right_type),
        math.factorial(n),
    )
    return min(Fraction(1), left_invariance, right_invariance, centralizer_bound)


def _brute_centralizer_cycle_type_counts(cycle_type: Partition) -> dict[Partition, int]:
    representative = _canonical_permutation(cycle_type)
    output: Counter[Partition] = Counter()
    for permutation in itertools.permutations(range(sum(cycle_type))):
        if _commute(representative, permutation):
            output[permutation_cycle_type(permutation)] += 1
    return dict(output)


def audit_centralizer_cycle_index(n: int) -> CentralizerCycleIndexAudit:
    if not 2 <= n <= 7:
        raise ValueError("brute cycle-index audits require 2<=n<=7")
    partitions = tuple(integer_partitions(n))
    maximum_count_residual = 0
    maximum_symmetry_residual = Fraction(0)
    maximum_bound_violation = Fraction(0)
    for left_type in partitions:
        exact_counts = centralizer_cycle_type_counts(left_type)
        brute_counts = _brute_centralizer_cycle_type_counts(left_type)
        for right_type in partitions:
            maximum_count_residual = max(
                maximum_count_residual,
                abs(exact_counts.get(right_type, 0) - brute_counts.get(right_type, 0)),
            )
            forward = class_pair_commuting_probability(left_type, right_type)
            reverse = class_pair_commuting_probability(right_type, left_type)
            maximum_symmetry_residual = max(
                maximum_symmetry_residual,
                abs(forward - reverse),
            )
            maximum_bound_violation = max(
                maximum_bound_violation,
                forward - class_pair_commuting_upper_bound(left_type, right_type),
            )
    verified = (
        maximum_count_residual == 0
        and maximum_symmetry_residual == 0
        and maximum_bound_violation <= 0
    )
    return CentralizerCycleIndexAudit(
        n=n,
        conjugacy_class_count=len(partitions),
        checked_class_count=len(partitions),
        maximum_cycle_type_count_residual=maximum_count_residual,
        maximum_commuting_kernel_symmetry_residual=str(maximum_symmetry_residual),
        maximum_support_invariance_bound_violation=str(maximum_bound_violation),
        exact_cycle_index_verified=verified,
        status=(
            "centralizer-wreath-cycle-index-exactly-verified"
            if verified
            else "centralizer-wreath-cycle-index-audit-failure"
        ),
    )


def _eligible_support_type_count(cutoff: int) -> int:
    return sum(
        1
        for moved_support in range(2, cutoff + 1)
        for partition in integer_partitions(moved_support)
        if 1 not in partition
    )


def exact_nonidentity_tail_control(
    n: int,
    *,
    support_cutoffs: tuple[int, ...] | None = None,
) -> ExactNonidentityTailControl:
    if n < 2:
        raise ValueError("n must be at least two")
    if support_cutoffs is None:
        support_cutoffs = tuple(cutoff for cutoff in (2, 4, 6) if cutoff <= n)
    if any(cutoff < 2 or cutoff > n for cutoff in support_cutoffs):
        raise ValueError("support cutoffs must lie between two and n")
    order = math.factorial(n)
    partitions = tuple(integer_partitions(n))
    identity_type = (1,) * n
    weights = {
        cycle_type: character_squared_weight(cycle_type)
        for cycle_type in partitions
    }
    class_masses = {
        cycle_type: Fraction(
            conjugacy_class_size(cycle_type) * weights[cycle_type],
            order**2,
        )
        for cycle_type in partitions
    }
    identity_atom = class_masses[identity_type]
    maximum_plancherel_atom = max(
        Fraction(hook_length_dimension(partition) ** 2, order)
        for partition in partitions
    )
    maximum_class_mass = max(class_masses.values())
    raw_commuting_numerator = 0
    raw_nonidentity_numerator = 0
    low_support_numerators = {cutoff: 0 for cutoff in support_cutoffs}
    centralizer_state_count = 0
    for left_type in partitions:
        centralizer_counts = centralizer_cycle_type_counts(left_type)
        centralizer_state_count += len(centralizer_counts)
        left_class_size = conjugacy_class_size(left_type)
        left_support = n - left_type.count(1)
        for right_type, commuting_count in centralizer_counts.items():
            term = (
                left_class_size
                * weights[left_type]
                * commuting_count
                * weights[right_type]
            )
            raw_commuting_numerator += term
            if left_type == identity_type or right_type == identity_type:
                continue
            raw_nonidentity_numerator += term
            right_support = n - right_type.count(1)
            for cutoff in support_cutoffs:
                if min(left_support, right_support) <= cutoff:
                    low_support_numerators[cutoff] += term

    weighted_commuting = Fraction(raw_commuting_numerator, order**4)
    identity_pair_contribution = 2 * identity_atom - identity_atom**2
    conditional_denominator = (1 - identity_atom) ** 2
    conditional_tail = (
        Fraction(raw_nonidentity_numerator, order**4) / conditional_denominator
    )
    decomposition_verified = bool(
        weighted_commuting
        == identity_pair_contribution + conditional_denominator * conditional_tail
    )
    support_rows: list[SupportCutoffControl] = []
    for cutoff in support_cutoffs:
        eligible_count = _eligible_support_type_count(cutoff)
        low_mass = sum(
            mass
            for cycle_type, mass in class_masses.items()
            if cycle_type != identity_type and n - cycle_type.count(1) <= cutoff
        ) / (1 - identity_atom)
        atom_bound = min(
            Fraction(1),
            Fraction(eligible_count) * maximum_plancherel_atom / (1 - identity_atom),
        )
        low_commuting = (
            Fraction(low_support_numerators[cutoff], order**4)
            / conditional_denominator
        )
        high_high = conditional_tail - low_commuting
        union_bound = 2 * low_mass - low_mass**2 + high_high
        atom_verified = low_mass <= atom_bound
        tail_verified = conditional_tail <= union_bound and high_high >= 0
        support_rows.append(
            SupportCutoffControl(
                n=n,
                moved_support_cutoff=cutoff,
                eligible_nonidentity_cycle_type_count=eligible_count,
                exact_conditional_low_support_mass=str(low_mass),
                conditional_low_support_mass=float(low_mass),
                exact_class_atom_domination_bound=str(atom_bound),
                class_atom_domination_bound=float(atom_bound),
                exact_conditional_commuting_mass_with_low_support=str(low_commuting),
                conditional_commuting_mass_with_low_support=float(low_commuting),
                exact_conditional_high_high_commuting_mass=str(high_high),
                conditional_high_high_commuting_mass=float(high_high),
                residual_tail_fraction_captured_by_low_support=(
                    float(low_commuting / conditional_tail) if conditional_tail else 0.0
                ),
                exact_union_bound=str(union_bound),
                union_bound=float(union_bound),
                class_atom_domination_verified=atom_verified,
                commuting_tail_decomposition_verified=tail_verified,
                status=(
                    "low-support-tail-separated-exactly"
                    if atom_verified and tail_verified
                    else "low-support-tail-control-failure"
                ),
            )
        )
    class_domination = maximum_class_mass <= maximum_plancherel_atom
    return ExactNonidentityTailControl(
        n=n,
        group_order=order,
        conjugacy_class_count=len(partitions),
        centralizer_cycle_type_state_count=centralizer_state_count,
        exact_identity_atom=str(identity_atom),
        identity_atom=float(identity_atom),
        exact_maximum_plancherel_atom=str(maximum_plancherel_atom),
        maximum_plancherel_atom=float(maximum_plancherel_atom),
        exact_maximum_class_mass=str(maximum_class_mass),
        maximum_class_mass=float(maximum_class_mass),
        exact_weighted_commuting_probability=str(weighted_commuting),
        weighted_commuting_probability=float(weighted_commuting),
        exact_identity_pair_contribution=str(identity_pair_contribution),
        identity_pair_contribution=float(identity_pair_contribution),
        exact_nonidentity_conditional_commuting_probability=str(conditional_tail),
        nonidentity_conditional_commuting_probability=float(conditional_tail),
        identity_share_of_total_commuting_probability=(
            float(identity_pair_contribution / weighted_commuting)
            if weighted_commuting
            else 0.0
        ),
        exact_identity_tail_decomposition_verified=decomposition_verified,
        class_mass_domination_verified=class_domination,
        support_cutoffs=tuple(support_rows),
        status=(
            "exact-nonidentity-commuting-tail-isolated"
            if decomposition_verified
            and class_domination
            and all(
                row.class_atom_domination_verified
                and row.commuting_tail_decomposition_verified
                for row in support_rows
            )
            else "nonidentity-tail-certificate-failure"
        ),
    )


def plancherel_carrier_tail_theorem(
    *,
    exact_cycle_index_verified: bool,
) -> PlancherelCarrierTailTheorem:
    return PlancherelCarrierTailTheorem(
        centralizer_structure=(
            "For cycle multiplicities m_i(g), C_Sn(g)=product_i C_i wr S_(m_i)."
        ),
        wreath_cycle_rule=(
            "A k-cycle of equal i-cycles with net rotation r yields gcd(i,r) "
            "cycles of length ik/gcd(i,r), with i^(k-1) assignments per r."
        ),
        exact_commuting_formula=(
            "kappa_n=(n!)^-4 sum_alpha |C_alpha| A(alpha) "
            "sum_beta N_alpha(beta) A(beta), where N_alpha is the exact "
            "centralizer cycle index."
        ),
        identity_tail_decomposition=(
            "kappa_n=2c_n-c_n^2+(1-c_n)^2 kappa_n^*, c_n=mu_n(e)."
        ),
        class_mass_domination=(
            "For every conjugacy class C, Q_n(C)<=p_max(n), by character "
            "column orthogonality and d_lambda<=d_max."
        ),
        identity_atom_asymptotic=(
            "c_n<=p_max(n)=exp(-Theta(sqrt(n))), so the identity-pair term vanishes."
        ),
        sublinear_support_asymptotic=(
            "For every fixed delta<1, Q_n(2<=supp(g)<=n^delta) "
            "<=exp(O(n^(delta/2)))p_max(n)=o(1)."
        ),
        residual_obligation=(
            "Prove that the conditional commuting mass with both supports "
            "greater than n^delta vanishes for one delta<1, or find its carrier classes."
        ),
        exact_cycle_index_proved=exact_cycle_index_verified,
        identity_contribution_vanishes_proved=True,
        every_sublinear_support_window_vanishes_proved=True,
        mesoscopic_macroscopic_commuting_tail_vanishes_proved=False,
        weighted_commuting_probability_vanishes_proved=False,
        status=(
            "identity-and-sublinear-support-removed-high-support-tail-open"
            if exact_cycle_index_verified
            else "centralizer-cycle-index-certificate-failure"
        ),
    )


def run_plancherel_carrier_nonidentity_tail(
    *,
    exact_degrees: tuple[int, ...] = (3, 4, 5, 6, 8, 10, 12, 14, 16, 18, 20),
) -> PlancherelCarrierNonidentityTailReport:
    if not exact_degrees or any(n < 2 for n in exact_degrees):
        raise ValueError("exact_degrees must contain degrees at least two")
    audits = [audit_centralizer_cycle_index(n) for n in range(2, 8)]
    controls = [
        exact_nonidentity_tail_control(
            n,
            support_cutoffs=tuple(cutoff for cutoff in (2, 4, 6) if cutoff <= n),
        )
        for n in exact_degrees
    ]
    cycle_index_verified = all(row.exact_cycle_index_verified for row in audits)
    exact_controls_verified = all(
        row.exact_identity_tail_decomposition_verified
        and row.class_mass_domination_verified
        and all(
            cutoff.class_atom_domination_verified
            and cutoff.commuting_tail_decomposition_verified
            for cutoff in row.support_cutoffs
        )
        for row in controls
    )
    theorem = plancherel_carrier_tail_theorem(
        exact_cycle_index_verified=cycle_index_verified and exact_controls_verified
    )
    tail = controls[-1]
    tail_cutoff = tail.support_cutoffs[-1]
    return PlancherelCarrierNonidentityTailReport(
        created_at=utc_now(),
        theorem_contract={
            "exact_engine": (
                "Use the cycle index of product_i C_i wr S_(m_i) to count "
                "commuting class pairs without enumerating S_n."
            ),
            "asymptotic_reduction": (
                "Remove the identity and every support window at most n^delta, "
                "delta<1, using maximal Plancherel class-atom domination."
            ),
            "remaining_target": (
                "Bound the commuting kernel on two mesoscopic/macroscopic "
                "character-squared draws."
            ),
            "scope": (
                "Exact finite commuting data and support elimination do not "
                "prove the remaining high-support tail, a Racah resolver, or speedup."
            ),
        },
        cycle_index_audits=audits,
        exact_tail_controls=controls,
        theorem=theorem,
        literature_links=[
            {
                "paper_id": MAXIMAL_DIMENSION_PAPER_ID,
                "url": MAXIMAL_DIMENSION_PAPER_URL,
                "supports": "p_max(n)=exp(-Theta(sqrt(n))) for S_n Plancherel measure.",
                "external_theorem_not_reproved_here": True,
            }
        ],
        proof_obligations=[
            {
                "obligation": "replace_factorial_commuting_enumeration_by_exact_centralizer_cycle_index",
                "resolved": cycle_index_verified and exact_controls_verified,
                "resolution": (
                    "The wreath-product cycle rule is normalized blockwise and "
                    "matches every centralizer cycle-type count through n=7."
                ),
            },
            {
                "obligation": "separate_identity_from_nonidentity_commuting_tail",
                "resolved": exact_controls_verified,
                "resolution": (
                    "Equation (1) is exact in every finite control through the "
                    f"largest requested degree n={tail.n}."
                ),
            },
            {
                "obligation": "rule_out_identity_and_sublinear_support_as_asymptotic_tail_source",
                "resolved": True,
                "resolution": (
                    "Class mass is at most the maximal Plancherel atom; partition "
                    "growth below n^delta cannot offset stretched-exponential decay."
                ),
            },
            {
                "obligation": "bound_mesoscopic_macroscopic_character_squared_commuting_kernel",
                "resolved": False,
                "resolution": (
                    "Use the exact class kernel plus support-invariance and "
                    "centralizer-size bounds; no uniform high-support estimate exists yet."
                ),
            },
            {
                "obligation": "compile_coherent_racah_resolver_after_contextuality_gap",
                "resolved": False,
                "resolution": (
                    "Even a vanishing kappa theorem would identify incompatible "
                    "labels, not implement their coherent resolution."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "The observed decay is Monte Carlo noise.",
                "resolved": True,
                "resolution": (
                    "The cycle-index engine now evaluates every reported value "
                    "exactly through n=20."
                ),
            },
            {
                "objection": "The identity atom alone creates the finite trend.",
                "resolved": True,
                "resolution": (
                    "Identity and nonidentity terms are separated exactly; both "
                    "decrease, but only the identity term has an asymptotic proof."
                ),
            },
            {
                "objection": "Low-support classes dominating finite tail prove an asymptotic obstruction.",
                "resolved": True,
                "resolution": (
                    "False: their entire mass, even through support n^delta for "
                    "any delta<1, vanishes by class-atom domination."
                ),
            },
            {
                "objection": "The existing class-uniform 7/(4p(n)) theorem automatically bounds this law.",
                "resolved": True,
                "resolution": (
                    "It does not: the character-squared class law is nonuniform. "
                    "A comparison or direct kernel estimate must be proved."
                ),
            },
            {
                "objection": "Finite contextuality supplies an efficient quantum measurement.",
                "resolved": False,
                "resolution": (
                    "No coherent multistar Racah transform or decoder is compiled."
                ),
            },
        ],
        headline_metrics={
            "exact_centralizer_wreath_cycle_index_theorem_count": int(
                cycle_index_verified and exact_controls_verified
            ),
            "brute_cycle_index_audit_degree_count": len(audits),
            "exact_weighted_commuting_degree_count": len(controls),
            "largest_exact_weighted_commuting_degree": tail.n,
            "tail_exact_weighted_commuting_probability": tail.weighted_commuting_probability,
            "tail_exact_nonidentity_conditional_commuting_probability": (
                tail.nonidentity_conditional_commuting_probability
            ),
            "tail_identity_share_of_commuting_probability": (
                tail.identity_share_of_total_commuting_probability
            ),
            "tail_low_support_cutoff": tail_cutoff.moved_support_cutoff,
            "tail_fraction_captured_by_low_support": (
                tail_cutoff.residual_tail_fraction_captured_by_low_support
            ),
            "identity_tail_vanishing_theorem_count": 1,
            "sublinear_support_mass_vanishing_theorem_count": 1,
            "mesoscopic_macroscopic_tail_vanishing_theorem_count": 0,
            "asymptotic_constant_contextuality_theorem_count": 0,
            "coherent_multistar_racah_resolver_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "exact_character_squared_commuting_probability_available_through_n20": (
                tail.n >= 20 and cycle_index_verified and exact_controls_verified
            ),
            "identity_commuting_contribution_asymptotically_vanishes_proved": True,
            "every_sublinear_moved_support_window_asymptotically_vanishes_proved": True,
            "finite_low_support_tail_dominance_is_asymptotic_evidence": False,
            "class_uniform_reciprocal_bound_transfers_without_comparison_theorem": False,
            "mesoscopic_macroscopic_commuting_tail_vanishes_proved": False,
            "weighted_commuting_probability_asymptotically_vanishes_proved": False,
            "collision_free_positive_constant_contextuality_proved": False,
            "structured_multistar_racah_resolver_compiled": False,
            "physical_pgm_compiled": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Exact cycle-index computation and maximal-atom domination remove "
                "the identity and all sublinear-support explanations, but the "
                "mesoscopic/macroscopic commuting kernel remains unbounded."
            ),
        },
        status=(
            "plancherel-carrier-tail-reduced-to-high-support-commuting-kernel"
            if cycle_index_verified and exact_controls_verified
            else "plancherel-carrier-tail-certificate-failure"
        ),
        summary=(
            "Replaced factorial commuting enumeration by an exact centralizer "
            "wreath-product cycle index, isolated the nonidentity tail through "
            "n=20, and proved that identity and every sublinear support window "
            "vanish, leaving one high-support kernel obligation."
        ),
        falsifiers_triggered=[
            "The sampled weighted-commuting trend is no longer needed for n<=20; exact values are available.",
            "Identity-heavy finite data cannot by itself decide the nonidentity commuting tail.",
            "Finite low-support dominance cannot persist as an asymptotic mass mechanism.",
            "The class-uniform reciprocal-class theorem cannot be imported without a measure comparison.",
            "A character-moment gap still would not constitute a coherent Racah compiler or speedup.",
        ],
    )


def write_plancherel_carrier_nonidentity_tail_report(
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
    payload = asdict(run_plancherel_carrier_nonidentity_tail(**kwargs))
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
                title="Plancherel carrier nonidentity commuting tail",
                status="completed-exact-cycle-index-high-support-tail-open",
                hypothesis=(
                    "The character-squared weighted commuting probability vanishes "
                    "after identity and low-support artifacts are removed, yielding "
                    "a constant natural carrier-contextuality gap."
                ),
                protocol=(
                    "Build the exact product_i C_i wr S_(m_i) centralizer cycle "
                    "index, verify it against brute centralizers, compute the full "
                    "and conditional commuting laws, stratify by moved support, "
                    "and apply maximal Plancherel atom domination."
                ),
                positive_signal=(
                    "A uniform vanishing bound for the commuting kernel when both "
                    "permutations have support greater than n^delta."
                ),
                falsifiers=[
                    "sampled values are reported where exact cycle-index values exist",
                    "identity contribution is confused with the conditional tail",
                    "finite low-support dominance is extrapolated asymptotically",
                    "the class-uniform 7/(4p(n)) bound is transferred without proof",
                    "contextuality is promoted to a Racah circuit or speedup",
                ],
                metrics=[
                    "exact_centralizer_wreath_cycle_index_theorem_count",
                    "tail_exact_nonidentity_conditional_commuting_probability",
                    "tail_fraction_captured_by_low_support",
                    "sublinear_support_mass_vanishing_theorem_count",
                    "mesoscopic_macroscopic_tail_vanishing_theorem_count",
                ],
                dependencies=[
                    "self_dual_wreath_plancherel_carrier_contextuality.py",
                    "symmetric-group centralizer wreath-product structure",
                    "character column orthogonality",
                    "Aggarwal-Elboim maximal Plancherel atom theorem",
                ],
                next_actions=[
                    "bound the exact high-support commuting kernel by support and centralizer profile",
                    "derive asymptotics for the character-squared cycle-count law",
                    "search for a measure comparison tailored to the commuting kernel",
                    "compile a structured Racah resolver only after a natural gap theorem",
                ],
            )
        )
        result_id = registry_result_id or (
            "RESULT-EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-CARRIER-"
            "NONIDENTITY-TAIL-LATEST"
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
                    "self_dual_wreath_plancherel_carrier_nonidentity_tail": str(path)
                },
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id="FINITE-LOW-SUPPORT-CARRIER-TAIL-NOT-ASYMPTOTIC-MECHANISM",
                source=registry_experiment_id,
                claim=(
                    "The low moved-support classes dominating the finite "
                    "nonidentity commuting tail can sustain its asymptotic mass."
                ),
                reason_invalid=(
                    "Every class has character-squared mass at most the maximal "
                    "Plancherel atom, so even all classes moving at most n^delta "
                    "points have total mass o(1) for every delta<1."
                ),
                lesson=(
                    "The asymptotic analysis must control two mesoscopic or "
                    "macroscopic permutations rather than extrapolate finite transpositions."
                ),
                applies_to=[
                    registry_candidate_id,
                    "weighted commuting asymptotics",
                    "natural carrier contextuality",
                ],
                evidence={"artifact": str(path), **payload["headline_metrics"]},
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id="CLASS-UNIFORM-COMMUTATOR-BOUND-NOT-DIRECT-PLANCHEREL-TAIL-PROOF",
                source=registry_experiment_id,
                claim=(
                    "The existing class-uniform 7/(4p(n)) theorem directly proves "
                    "the character-squared weighted commuting tail vanishes."
                ),
                reason_invalid=(
                    "The character-squared law is nonuniform on conjugacy classes; "
                    "the class-uniform proof supplies no domination or kernel comparison."
                ),
                lesson=(
                    "Prove a measure comparison or bound the exact centralizer "
                    "kernel under the actual class law."
                ),
                applies_to=[
                    registry_candidate_id,
                    "class-uniform commutator filtering",
                    "character-squared commuting tail",
                ],
                evidence={"artifact": str(path), **payload["headline_metrics"]},
            )
        )
    return payload


if __name__ == "__main__":
    result = write_plancherel_carrier_nonidentity_tail_report()
    print(json.dumps(result, indent=2))
