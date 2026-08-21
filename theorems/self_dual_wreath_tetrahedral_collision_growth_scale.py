"""Sharp polynomial scale for the tetrahedral collision transfer problem.

The physical rank-profile transfer theorem requires

    M_n S_n -> 0,
    S_n = 8 V_n + 2 W_n,

where ``M_n`` is the tetrahedral likelihood second moment and

    V_n = sum_(C != {e}) |C|^-1,
    W_n = sum_(C != {e}) |C|^-2.

This module identifies the exact scale hidden in that condition.  Write a
nonidentity cycle type in ``S_n`` as ``1^(n-m) union rho``, where ``rho`` is a
partition of ``m`` with no part one.  If

    z_rho = product_i i^a_i a_i!,
    A_m = sum_rho z_rho,
    B_m = sum_rho z_rho^2,

then the class-size formula gives

    V_n = sum_(m=2)^n A_m/(n)_m,
    W_n = sum_(m=2)^n B_m/(n)_m^2.                      (1)

The first coefficients are ``A_2=2``, ``A_3=3``, ``A_4=12`` and
``B_2=4``, ``B_3=9``.  For every fixed-point-free partition of ``m``,

    z_rho <= m^(m/2),

because it has at most ``m/2`` cycles.  There are at most ``2^(m-1)``
partitions.  Also ``(n)_m >= (n/e)^m``: the geometric mean of the largest
``m`` integers in ``[n]`` is at least the geometric mean of all ``n``
integers, and ``n! >= (n/e)^n``.  Hence, uniformly for ``m<=n``,

    A_m/(n)_m   <= (1/2)(2e/sqrt(n))^m,
    B_m/(n)_m^2 <= (1/2)(2e^2/n)^m.                    (2)

Taking the tails after ``m=7`` and ``m=5`` respectively makes (2) geometric.
The finitely many preceding terms then prove

    V_n = 2/(n)_2 + 3/(n)_3 + O(n^-4),
    W_n = 4/(n)_2^2 + O(n^-6),
    S_n = 16/n^2 (1+O(1/n)).                            (3)

Therefore the physical rank-profile transfer criterion is equivalent to

    M_n = o(n^2).                                       (4)

This is the decisive growth target for the classical six-word
cycle-signature collision problem.  It does not prove (4).  In particular,
the exact values through ``S_5`` are controls only, and fixed/stable-character
word-measure estimates do not bound the high-dimensional collision spectrum.
"""

from __future__ import annotations

import json
import math
from collections import Counter
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from representation_obstruction import integer_partitions
from research_registry import utc_now
from self_dual_wreath_parity_rank_profile_plancherel_mixing import class_power_sum


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_tetrahedral_collision_growth_scale.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-TETRAHEDRAL-COLLISION-GROWTH-SCALE"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]


@dataclass(frozen=True)
class SupportExpansionControl:
    n: int
    exact_reciprocal_class_sum: str
    support_expansion_reciprocal_class_sum: str
    exact_inverse_class_square_sum: str
    support_expansion_inverse_class_square_sum: str
    exact_reference_union_variance: str
    n_squared_scaled_reciprocal_sum: float
    n_fourth_scaled_inverse_square_sum: float
    n_squared_scaled_reference_union_variance: float
    transposition_fraction_of_reciprocal_sum: float
    exact_support_expansions_verified: bool
    status: str


@dataclass(frozen=True)
class TailBoundControl:
    n: int
    exact_v_remainder_after_support_three: float
    analytic_v_remainder_upper: float
    exact_w_remainder_after_support_two: float
    analytic_w_remainder_upper: float
    v_tail_bound_verified: bool
    w_tail_bound_verified: bool
    status: str


@dataclass(frozen=True)
class CollisionGrowthScaleTheorem:
    reciprocal_class_asymptotic: str
    inverse_square_asymptotic: str
    reference_union_variance_asymptotic: str
    transfer_condition_original: str
    transfer_condition_equivalent: str
    equivalence_proved: bool
    tetrahedral_subquadratic_growth_proved: bool
    status: str


@dataclass(frozen=True)
class TetrahedralCollisionGrowthScaleReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: CollisionGrowthScaleTheorem
    exact_controls: list[SupportExpansionControl]
    tail_bound_controls: list[TailBoundControl]
    proof_obligations: list[dict[str, str | bool]]
    literature_boundary: list[dict[str, str]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def falling_factorial(n: int, m: int) -> int:
    if n < 0 or m < 0 or m > n:
        raise ValueError("require 0<=m<=n")
    return math.prod(range(n - m + 1, n + 1))


def fixed_point_free_partitions(m: int) -> tuple[Partition, ...]:
    if m < 0:
        raise ValueError("m must be nonnegative")
    if m == 0:
        return ((),)
    return tuple(
        partition for partition in integer_partitions(m) if 1 not in partition
    )


def centralizer_order(cycle_type: Partition) -> int:
    counts = Counter(cycle_type)
    return math.prod(
        length**multiplicity * math.factorial(multiplicity)
        for length, multiplicity in counts.items()
    )


def support_centralizer_power_sum(m: int, power: int) -> int:
    if m < 2 or power < 1:
        raise ValueError("require m>=2 and positive power")
    return sum(
        centralizer_order(partition) ** power
        for partition in fixed_point_free_partitions(m)
    )


def reciprocal_class_support_expansion(n: int, power: int) -> Fraction:
    if n < 2 or power < 1:
        raise ValueError("require n>=2 and positive power")
    return sum(
        (
            Fraction(
                support_centralizer_power_sum(m, power),
                falling_factorial(n, m) ** power,
            )
            for m in range(2, n + 1)
        ),
        start=Fraction(),
    )


def analytic_remainder_bounds(n: int) -> tuple[float, float]:
    """Return certified remainders for V after m=3 and W after m=2."""

    if n < 30:
        raise ValueError("geometric tail bounds require n>=30")
    v_fixed = sum(
        Fraction(support_centralizer_power_sum(m, 1), falling_factorial(n, m))
        for m in range(4, min(7, n) + 1)
    )
    v_ratio = 2.0 * math.e / math.sqrt(n)
    if v_ratio >= 1:
        raise ValueError("V-tail ratio is not geometric")
    v_tail = 0.5 * v_ratio**8 / (1.0 - v_ratio)

    w_fixed = sum(
        Fraction(
            support_centralizer_power_sum(m, 2),
            falling_factorial(n, m) ** 2,
        )
        for m in range(3, min(5, n) + 1)
    )
    w_ratio = 2.0 * math.e**2 / n
    if w_ratio >= 1:
        raise ValueError("W-tail ratio is not geometric")
    w_tail = 0.5 * w_ratio**6 / (1.0 - w_ratio)
    return float(v_fixed) + v_tail, float(w_fixed) + w_tail


def audit_support_expansion(n: int) -> SupportExpansionControl:
    if not 2 <= n <= 40:
        raise ValueError("exact partition controls require 2<=n<=40")
    v = class_power_sum(n, 1)
    w = class_power_sum(n, 2)
    expanded_v = reciprocal_class_support_expansion(n, 1)
    expanded_w = reciprocal_class_support_expansion(n, 2)
    union = 8 * v + 2 * w
    verified = v == expanded_v and w == expanded_w
    transposition = Fraction(2, n * (n - 1))
    return SupportExpansionControl(
        n=n,
        exact_reciprocal_class_sum=str(v),
        support_expansion_reciprocal_class_sum=str(expanded_v),
        exact_inverse_class_square_sum=str(w),
        support_expansion_inverse_class_square_sum=str(expanded_w),
        exact_reference_union_variance=str(union),
        n_squared_scaled_reciprocal_sum=n * n * float(v),
        n_fourth_scaled_inverse_square_sum=n**4 * float(w),
        n_squared_scaled_reference_union_variance=n * n * float(union),
        transposition_fraction_of_reciprocal_sum=float(transposition / v),
        exact_support_expansions_verified=verified,
        status=(
            "exact-support-size-class-expansions-verified"
            if verified
            else "support-size-class-expansion-failure"
        ),
    )


def audit_tail_bounds(n: int) -> TailBoundControl:
    if not 30 <= n <= 40:
        raise ValueError("exact tail controls require 30<=n<=40")
    v = class_power_sum(n, 1)
    w = class_power_sum(n, 2)
    v_leading = Fraction(2, falling_factorial(n, 2)) + Fraction(
        3, falling_factorial(n, 3)
    )
    w_leading = Fraction(4, falling_factorial(n, 2) ** 2)
    v_remainder = float(v - v_leading)
    w_remainder = float(w - w_leading)
    v_upper, w_upper = analytic_remainder_bounds(n)
    v_verified = -1e-18 <= v_remainder <= v_upper * (1 + 1e-12)
    w_verified = -1e-18 <= w_remainder <= w_upper * (1 + 1e-12)
    return TailBoundControl(
        n=n,
        exact_v_remainder_after_support_three=v_remainder,
        analytic_v_remainder_upper=v_upper,
        exact_w_remainder_after_support_two=w_remainder,
        analytic_w_remainder_upper=w_upper,
        v_tail_bound_verified=v_verified,
        w_tail_bound_verified=w_verified,
        status=(
            "support-tail-bounds-verified"
            if v_verified and w_verified
            else "support-tail-bound-control-failure"
        ),
    )


def run_tetrahedral_collision_growth_scale() -> TetrahedralCollisionGrowthScaleReport:
    exact = [audit_support_expansion(n) for n in (4, 8, 12, 20, 30)]
    tails = [audit_tail_bounds(n) for n in (30, 36, 40)]
    failures = sum(not row.exact_support_expansions_verified for row in exact)
    failures += sum(
        not (row.v_tail_bound_verified and row.w_tail_bound_verified)
        for row in tails
    )
    verified = failures == 0
    theorem = CollisionGrowthScaleTheorem(
        reciprocal_class_asymptotic=(
            "V_n=2/(n)_2+3/(n)_3+O(n^-4)=2n^-2(1+O(n^-1))"
        ),
        inverse_square_asymptotic=(
            "W_n=4/(n)_2^2+O(n^-6)=4n^-4(1+O(n^-1))"
        ),
        reference_union_variance_asymptotic=(
            "S_n=8V_n+2W_n=16n^-2(1+O(n^-1))"
        ),
        transfer_condition_original="M_n(8V_n+2W_n)->0",
        transfer_condition_equivalent="M_n=o(n^2)",
        equivalence_proved=verified,
        tetrahedral_subquadratic_growth_proved=False,
        status=(
            "physical-transfer-scale-sharpened-to-subquadratic-collision-growth"
            if verified
            else "collision-growth-scale-control-failure"
        ),
    )
    return TetrahedralCollisionGrowthScaleReport(
        created_at=utc_now(),
        theorem_contract={
            "support_decomposition": (
                "Every nonidentity class is uniquely 1^(n-m) union rho with rho "
                "fixed-point-free, and |C|=(n)_m/z_rho."
            ),
            "coefficient_bounds": (
                "A_m<=2^(m-1)m^(m/2), B_m<=2^(m-1)m^m."
            ),
            "falling_factorial_bound": "(n)_m>=(n/e)^m uniformly for m<=n.",
            "reference_scale": theorem.reference_union_variance_asymptotic,
            "physical_transfer_target": theorem.transfer_condition_equivalent,
            "scope": (
                "The transfer threshold is exact, but no subquadratic bound on "
                "the physical tetrahedral collision moment M_n is proved."
            ),
        },
        theorem=theorem,
        exact_controls=exact,
        tail_bound_controls=tails,
        proof_obligations=[
            {
                "obligation": "identify_exact_reference-variance_polynomial_scale",
                "resolved": verified,
                "resolution": (
                    "The support-size expansion and geometric tails give "
                    "8V_n+2W_n~16/n^2."
                ),
            },
            {
                "obligation": "prove_physical_tetrahedral_collision_moment_is_subquadratic",
                "resolved": False,
                "resolution": (
                    "Control the fully nonidentity six-word class-signature core "
                    "Z6_n strongly enough to show M_n=o(n^2)."
                ),
            },
            {
                "obligation": "replace_full_collision_moment_by_trimmed_bulk_control_if_needed",
                "resolved": False,
                "resolution": (
                    "The bounded rank observable permits removal of vanishing "
                    "physical-mass label tails before applying change of measure."
                ),
            },
        ],
        literature_boundary=[
            {
                "id": "hanany-puder-word-measures-symmetric-groups",
                "url": "https://arxiv.org/abs/2009.00897",
                "boundary": (
                    "Stable-character and fixed-cycle estimates do not control the "
                    "full joint cycle-signature L2 norm."
                ),
            },
            {
                "id": "feray-sniady-character-bounds",
                "url": "https://arxiv.org/abs/math/0701051",
                "boundary": (
                    "Pointwise normalized-character estimates do not preserve the "
                    "cancellation in the correlated six-word contraction."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "The earlier o(1) class-sum bound already fixes the transfer scale.",
                "resolved": True,
                "resolution": (
                    "No: transfer depends on its reciprocal. The leading transposition "
                    "term fixes the exact n^2 collision-growth threshold."
                ),
            },
            {
                "objection": "A divergent M_n automatically blocks physical mixing.",
                "resolved": True,
                "resolution": "False. Every growth rate o(n^2) is sufficient.",
            },
            {
                "objection": "Finite M_n values support a subquadratic theorem.",
                "resolved": False,
                "resolution": (
                    "Values through S_5 cannot distinguish bounded, polynomial, or "
                    "faster asymptotic collision growth."
                ),
            },
            {
                "objection": "Subquadratic M_n would settle the full adaptive channel.",
                "resolved": True,
                "resolution": (
                    "It settles only rank-profile transfer; non-Haar Racah cumulants "
                    "remain outside this likelihood argument."
                ),
            },
        ],
        headline_metrics={
            "reference_variance_scale_theorem_count": int(verified),
            "exact_support_expansion_control_count": len(exact),
            "analytic_tail_bound_control_count": len(tails),
            "finite_control_failure_count": failures,
            "tetrahedral_subquadratic_growth_theorem_count": 0,
            "physical_rank_mixing_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "reference_variance_asymptotic_scale_proved": verified,
            "physical_transfer_equivalent_to_subquadratic_collision_growth": verified,
            "tetrahedral_collision_moment_subquadratic_proved": False,
            "physical_rank_profile_mixes_proved": False,
            "irreducible_racah_cmi_vanishes_proved": False,
            "adaptive_syndrome_decouples_proved": False,
            "adaptive_syndrome_survives_proved": False,
            "classical_separation_proved": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The exact target is now M_n=o(n^2), but no all-n bound on M_n or "
                "the fully nonidentity core Z6_n is available."
            ),
        },
        status=(
            "tetrahedral-collision-subquadratic-growth-is-exact-transfer-target"
            if verified
            else "tetrahedral-collision-growth-scale-failure"
        ),
        summary=(
            "Proved that the product-law variance is asymptotic to 16/n^2, "
            "making M_n=o(n^2) the exact physical rank-transfer target."
        ),
        falsifiers_triggered=[
            "Uniform boundedness of the tetrahedral collision moment is stronger than needed.",
            "Merely proving M_n=O(n^2) does not cross the transfer threshold.",
            "Stable-character word-measure estimates do not establish the required full-spectrum L2 bound.",
        ],
    )


def write_tetrahedral_collision_growth_scale_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_tetrahedral_collision_growth_scale())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    result = write_tetrahedral_collision_growth_scale_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))
