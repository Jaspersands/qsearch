"""Only the fully nonidentity even-word core can obstruct coarse entropy.

The coarse alternating Renyi target is the even-input collision moment

    C_even = sum_C N_even(C)^2 / product_i |C_i|.

Expand each of the six class-matching kernels into identity and nonidentity
parts.  Exactly the tetrahedral support masks survive.  Restricting every
nonidentity class to even permutations, define

    V_+  = sum_(C even, C!=e) |C|^-1,
    W_+  = sum_(C even, C!=e) |C|^-2,
    M2_+ = E_Pl[(sum_(C even, C!=e) r_lambda(C)^2)^2].

Four support-three masks contribute ``V_+``, three support-four masks
contribute ``W_+``, six support-five masks contribute ``M2_+-W_+``, and the
fully nonidentity mask contributes ``Z6_+``.  Hence

    C_even = 1 + 4V_+ + 6M2_+ - 3W_+ + Z6_+.            (1)

Support-size expansion gives

    V_+ = 3/(n)_3 + 8/(n)_4 + O(n^-5),
    W_+ = 9/(n)_3^2 + O(n^-8).                          (2)

Moreover ``M2_+<=M2`` pointwise before the Plancherel average, and the existing
character-energy theorem proves ``M2->0``.  Thus every term outside ``Z6_+``
vanishes:

    C_even = 1 + Z6_+ + o(1).                           (3)

Therefore the sufficient subpolynomial collision condition is equivalent to
``1+Z6_+=n^o(1)``.  This is the single classical obstruction left for the
Renyi route to physical rank mixing.  Equation (3) does not estimate that
core and finite ``S_4/S_5`` values have no asymptotic force.
"""

from __future__ import annotations

import json
import math
from collections import defaultdict
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_alternating_base_orbit_reduction import (
    permutation_parity_from_cycle_type,
)
from self_dual_wreath_global_collision_free_mass import plancherel_weights
from self_dual_wreath_projected_parity_coset_kernel import (
    full_parity_class_collision_energy,
    parity_coset_signature_counts,
)
from self_dual_wreath_source_conditioned_channel_decoupling import (
    plancherel_character_energy_moments,
)
from self_dual_wreath_tetrahedral_collision_growth_scale import (
    centralizer_order,
    falling_factorial,
    fixed_point_free_partitions,
)
from symmetric_character import conjugacy_class_size, symmetric_character


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_alternating_even_collision_core_reduction.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-ALTERNATING-EVEN-COLLISION-CORE-REDUCTION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class EvenCollisionSupportControl:
    n: int
    support_mask_count: int
    size_three_mask_count: int
    size_four_mask_count: int
    size_five_mask_count: int
    size_six_mask_count: int
    exact_even_collision_moment: str
    exact_even_reciprocal_class_sum: str
    exact_even_inverse_class_square_sum: str
    exact_even_character_energy_second_moment: str
    exact_lower_support_contribution: str
    exact_fully_nonidentity_even_core: str
    exact_decomposition_residual: str
    support_coefficients_verified: bool
    exact_support_decomposition_verified: bool
    status: str


@dataclass(frozen=True)
class EvenClassAsymptoticControl:
    n: int
    exact_even_reciprocal_class_sum: float
    n_cubed_scaled_even_reciprocal_sum: float
    exact_even_inverse_class_square_sum: float
    n_sixth_scaled_even_inverse_square_sum: float
    exact_even_character_energy_second_moment: float
    full_character_energy_second_moment: float
    even_energy_dominated_by_full: bool
    status: str


@dataclass(frozen=True)
class EvenCollisionCoreTheorem:
    exact_decomposition: str
    even_reciprocal_asymptotic: str
    even_inverse_square_asymptotic: str
    even_energy_second_moment_vanishes: bool
    collision_reduction: str
    fully_nonidentity_even_core_subpolynomial_proved: bool
    status: str


@dataclass(frozen=True)
class AlternatingEvenCollisionCoreReductionReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: EvenCollisionCoreTheorem
    exact_support_controls: list[EvenCollisionSupportControl]
    asymptotic_controls: list[EvenClassAsymptoticControl]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def even_nonidentity_classes(n: int) -> tuple[tuple[int, ...], ...]:
    if n < 3:
        return ()
    identity = (1,) * n
    return tuple(
        cycle_type
        for cycle_type in integer_partitions(n)
        if cycle_type != identity
        and permutation_parity_from_cycle_type(cycle_type) == 0
    )


def even_class_power_sum(n: int, power: int) -> Fraction:
    if n < 2 or power < 1:
        raise ValueError("require n>=2 and positive power")
    return sum(
        (
            Fraction(1, conjugacy_class_size(cycle_type) ** power)
            for cycle_type in even_nonidentity_classes(n)
        ),
        start=Fraction(),
    )


def even_support_centralizer_power_sum(m: int, power: int) -> int:
    if m < 2 or power < 1:
        raise ValueError("require m>=2 and positive power")
    return sum(
        centralizer_order(partition) ** power
        for partition in fixed_point_free_partitions(m)
        if permutation_parity_from_cycle_type(partition) == 0
    )


def even_reciprocal_support_expansion(n: int, power: int) -> Fraction:
    if n < 2 or power < 1:
        raise ValueError("require n>=2 and positive power")
    return sum(
        (
            Fraction(
                even_support_centralizer_power_sum(m, power),
                falling_factorial(n, m) ** power,
            )
            for m in range(2, n + 1)
        ),
        start=Fraction(),
    )


def even_character_energy_second_moment(n: int) -> Fraction:
    if n < 2:
        raise ValueError("n must be at least two")
    partitions = tuple(integer_partitions(n))
    weights = dict(zip(partitions, plancherel_weights(n)))
    classes = even_nonidentity_classes(n)
    total = Fraction()
    for partition in partitions:
        dimension = hook_length_dimension(partition)
        energy = sum(
            (
                Fraction(
                    symmetric_character(partition, cycle_type),
                    dimension,
                )
                ** 2
                for cycle_type in classes
            ),
            start=Fraction(),
        )
        total += weights[partition] * energy**2
    return total


def even_support_contributions(n: int) -> dict[int, Fraction]:
    if not 2 <= n <= 5:
        raise ValueError("exact even support enumeration requires 2<=n<=5")
    identity = (1,) * n
    rows: defaultdict[int, Fraction] = defaultdict(Fraction)
    for signature, count in parity_coset_signature_counts(n, (0, 0, 0)).items():
        mask = sum(
            (cycle_type != identity) << index
            for index, cycle_type in enumerate(signature)
        )
        rows[mask] += Fraction(
            count * count,
            math.prod(conjugacy_class_size(cycle_type) for cycle_type in signature),
        )
    return dict(rows)


def audit_even_collision_support(n: int) -> EvenCollisionSupportControl:
    if not 3 <= n <= 5:
        raise ValueError("support controls require 3<=n<=5")
    supports = even_support_contributions(n)
    grouped: defaultdict[int, list[Fraction]] = defaultdict(list)
    for mask, value in supports.items():
        grouped[mask.bit_count()].append(value)
    for values in grouped.values():
        values.sort()
    collision = full_parity_class_collision_energy(n, (0, 0, 0))
    variance = even_class_power_sum(n, 1)
    inverse_square = even_class_power_sum(n, 2)
    energy_second = even_character_energy_second_moment(n)
    lower = 4 * variance + 6 * energy_second - 3 * inverse_square
    full_mask = (1 << 6) - 1
    core = supports.get(full_mask, Fraction())
    residual = collision - 1 - lower - core
    coefficient_check = bool(
        grouped[0] == [Fraction(1)]
        and grouped[3] == [variance] * 4
        and grouped[4] == [inverse_square] * 3
        and grouped[5] == [energy_second - inverse_square] * 6
        and len(grouped[6]) <= 1
    )
    exact = coefficient_check and residual == 0
    return EvenCollisionSupportControl(
        n=n,
        support_mask_count=len(supports),
        size_three_mask_count=len(grouped[3]),
        size_four_mask_count=len(grouped[4]),
        size_five_mask_count=len(grouped[5]),
        size_six_mask_count=len(grouped[6]),
        exact_even_collision_moment=str(collision),
        exact_even_reciprocal_class_sum=str(variance),
        exact_even_inverse_class_square_sum=str(inverse_square),
        exact_even_character_energy_second_moment=str(energy_second),
        exact_lower_support_contribution=str(lower),
        exact_fully_nonidentity_even_core=str(core),
        exact_decomposition_residual=str(residual),
        support_coefficients_verified=coefficient_check,
        exact_support_decomposition_verified=exact,
        status=(
            "even-collision-support-decomposition-verified"
            if exact
            else "even-collision-support-decomposition-failure"
        ),
    )


def audit_even_class_asymptotics(n: int) -> EvenClassAsymptoticControl:
    if not 3 <= n <= 16:
        raise ValueError("exact asymptotic controls require 3<=n<=16")
    variance = even_class_power_sum(n, 1)
    inverse_square = even_class_power_sum(n, 2)
    even_energy = even_character_energy_second_moment(n)
    _full_first, full_energy = plancherel_character_energy_moments(n)
    dominated = even_energy <= full_energy
    return EvenClassAsymptoticControl(
        n=n,
        exact_even_reciprocal_class_sum=float(variance),
        n_cubed_scaled_even_reciprocal_sum=n**3 * float(variance),
        exact_even_inverse_class_square_sum=float(inverse_square),
        n_sixth_scaled_even_inverse_square_sum=n**6 * float(inverse_square),
        exact_even_character_energy_second_moment=float(even_energy),
        full_character_energy_second_moment=float(full_energy),
        even_energy_dominated_by_full=dominated,
        status=(
            "even-class-lower-support-terms-controlled"
            if dominated
            else "even-character-energy-domination-failure"
        ),
    )


def run_alternating_even_collision_core_reduction(
) -> AlternatingEvenCollisionCoreReductionReport:
    supports = [audit_even_collision_support(n) for n in (3, 4, 5)]
    asymptotic = [audit_even_class_asymptotics(n) for n in (5, 8, 12, 16)]
    failures = sum(not row.exact_support_decomposition_verified for row in supports)
    failures += sum(not row.even_energy_dominated_by_full for row in asymptotic)
    exact = failures == 0
    theorem = EvenCollisionCoreTheorem(
        exact_decomposition="C_even=1+4V_+ +6M2_+ -3W_+ +Z6_+",
        even_reciprocal_asymptotic=(
            "V_+=3/(n)_3+8/(n)_4+O(n^-5)=3n^-3(1+O(n^-1))"
        ),
        even_inverse_square_asymptotic=(
            "W_+=9/(n)_3^2+O(n^-8)=9n^-6(1+O(n^-1))"
        ),
        even_energy_second_moment_vanishes=True,
        collision_reduction="C_even=1+Z6_+ +o(1)",
        fully_nonidentity_even_core_subpolynomial_proved=False,
        status=(
            "even-collision-renyi-obstruction-is-fully-nonidentity-core"
            if exact
            else "even-collision-core-reduction-control-failure"
        ),
    )
    return AlternatingEvenCollisionCoreReductionReport(
        created_at=utc_now(),
        theorem_contract={
            "support_masks": (
                "Four size-three, three size-four, six size-five, and one possible "
                "fully nonidentity tetrahedral mask survive."
            ),
            "exact_decomposition": theorem.exact_decomposition,
            "lower_support_asymptotics": (
                "V_+=Theta(n^-3), W_+=Theta(n^-6), and M2_+<=M2=o(1)."
            ),
            "single_open_core": theorem.collision_reduction,
            "rank_sufficient_target": "1+Z6_+=n^o(1).",
            "scope": (
                "No estimate of Z6_+ is proved and collision control remains only a "
                "sufficient Renyi route to rank mixing."
            ),
        },
        theorem=theorem,
        exact_support_controls=supports,
        asymptotic_controls=asymptotic,
        proof_obligations=[
            {
                "obligation": "derive_even_input_support_mask_decomposition",
                "resolved": exact,
                "resolution": (
                    "Exact kernel expansion gives the same tetrahedral masks with all "
                    "nonidentity class sums restricted to even classes."
                ),
            },
            {
                "obligation": "prove_all_lower_support_even_terms_vanish",
                "resolved": exact,
                "resolution": (
                    "Support-size class bounds handle V_+,W_+; pointwise energy "
                    "domination transfers the existing M2=o(1) theorem."
                ),
            },
            {
                "obligation": "prove_fully_nonidentity_even_core_subpolynomial",
                "resolved": False,
                "resolution": (
                    "Bound the six simultaneous nonidentity class matches for two "
                    "even permutation triples, preserving word-map cancellation."
                ),
            },
            {
                "obligation": "bypass_renyi_core_with_direct_entropy_if_tail_dominated",
                "resolved": False,
                "resolution": (
                    "If Z6_+ grows polynomially, test whether its physical mass has "
                    "sublogarithmic positive likelihood information."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Even restriction leaves transposition-scale n^-2 terms.",
                "resolved": True,
                "resolution": (
                    "Transpositions are odd. The leading even class is the 3-cycle, "
                    "so V_+ is Theta(n^-3)."
                ),
            },
            {
                "objection": "The five-support energy needs a new asymptotic theorem.",
                "resolved": True,
                "resolution": (
                    "Its even class energy is pointwise bounded by the full class "
                    "energy whose Plancherel second moment already vanishes."
                ),
            },
            {
                "objection": "Finite Z6_+ near one proves boundedness.",
                "resolved": False,
                "resolution": "No all-n estimate follows from S_4/S_5 values.",
            },
            {
                "objection": "Subpolynomial Z6_+ would settle non-Haar syndrome CMI.",
                "resolved": True,
                "resolution": (
                    "It settles only the base entropy route to Haar rank-profile mixing."
                ),
            },
        ],
        headline_metrics={
            "even_collision_support_decomposition_theorem_count": int(exact),
            "lower_support_vanishing_theorem_count": int(exact),
            "exact_support_control_count": len(supports),
            "finite_control_failure_count": failures,
            "fully_nonidentity_even_core_subpolynomial_theorem_count": 0,
            "physical_rank_mixing_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "even_collision_support_decomposition_proved": exact,
            "all_lower_support_even_terms_vanish_proved": exact,
            "fully_nonidentity_even_core_is_only_renyi_obstruction": exact,
            "fully_nonidentity_even_core_subpolynomial_proved": False,
            "coarse_alternating_total_correlation_sublogarithmic_proved": False,
            "physical_rank_profile_mixes_proved": False,
            "irreducible_racah_cmi_vanishes_proved": False,
            "classical_separation_proved": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Every lower-support term vanishes, but the fully nonidentity even "
                "six-word collision core has no all-n estimate."
            ),
        },
        status=(
            "fully-nonidentity-even-word-core-is-single-renyi-rank-obstruction"
            if exact
            else "alternating-even-collision-core-reduction-failure"
        ),
        summary=(
            "Decomposed the even collision norm and proved all lower-support terms "
            "vanish, isolating Z6_+ as the sole Renyi obstruction."
        ),
        falsifiers_triggered=[
            "Odd transposition classes do not set the coarse alternating collision scale.",
            "No new five-support moment theorem is needed after even/full energy domination.",
            "Only the fully nonidentity even-word collision core can obstruct the Renyi route asymptotically.",
        ],
    )


def write_alternating_even_collision_core_reduction_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_alternating_even_collision_core_reduction())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    result = write_alternating_even_collision_core_reduction_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))
