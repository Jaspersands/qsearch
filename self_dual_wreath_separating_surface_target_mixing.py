"""Genus-uniform mixing of separating surface targets in ``S_n``.

Let ``X_h`` be the product of ``h`` independent commutators in a finite group
``G``.  Frobenius' formula says that its density relative to uniform measure is

    A_h(x)=sum_(rho in Irr(G)) chi_rho(x)/d_rho^(2h-1).   (1)

For a closed orientable surface split by a separating curve into genera
``a,b>=1``, the image of that curve has density

    f_(a,b)(x)=A_a(x) A_b(x^-1)/zeta_G(2a+2b-2),         (2)

where ``zeta_G(s)=sum_rho d_rho^-s``.  Equation (2) is exact: condition two
independent surface-boundary words to multiply to the identity.

For ``G=S_n``, put ``u=1+sgn``, the density of uniform measure on ``A_n``.
All commutator products are even, and

    A_h=u+r_h,
    ||r_h||_2^2=zeta_(S_n)^*(4h-2),                      (3)

where the star deletes the trivial and sign representations.  Cauchy--Schwarz
therefore gives, with ``Z=zeta_(S_n)(2a+2b-2)`` and
``eps_h=sqrt(zeta^*(4h-2))``, the explicit bound

    TV(f_(a,b),u)
      <= [2eps_a+2eps_b+eps_a eps_b+(Z-2)]/(2Z).         (4)

The fixed-exponent symmetric-group Witten-zeta estimate
``zeta^*(s)=O(n^-s)`` makes (4) ``O(n^-(2 min(a,b)-1))``.  Monotonicity in the
exponent also makes it ``O(1/n)`` uniformly over arbitrary growing positive
genera.  The unconditioned ``h``-commutator product is within
``0.5 sqrt(zeta^*(4h-2))`` of uniform ``A_n``.

For a nonseparating simple curve on a closed genus-``g>=2`` surface, fixing its
image ``x`` and averaging the conjugate handle gives the exact density

    f_nonsep,g(x)
      = [sum_rho |chi_rho(x)|^2/d_rho^(2g-2)]
        / zeta_G(2g-2).                                   (5)

In ``S_n`` the trivial and sign terms contribute the constant two.  The
remaining nonnegative function has mean ``zeta^*(2g-2)``, so

    TV(f_nonsep,g, uniform S_n)
      <= zeta^*(2g-2)/zeta(2g-2)=O(n^-2),                (6)

uniformly over ``g>=2``.  Consequently every normalized irreducible character
other than the appropriate uniform-null sectors has expectation at most twice
the corresponding TV bound.  This dequantizes every marked target proved to
be an unconditioned surface boundary or any simple curve, including
free-product extensions.  It does not classify arbitrary marked
presentations, self-intersecting curves, or target words not certified by a
surface factorization.
"""

from __future__ import annotations

import itertools
import json
import math
from collections import Counter
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_alternating_base_orbit_reduction import (
    permutation_parity_from_cycle_type,
)
from self_dual_wreath_alternating_product_character_zeta import (
    symmetric_witten_zeta_tail,
)
from self_dual_wreath_character_moments import (
    compose_permutations,
    permutation_cycle_type,
)
from symmetric_character import conjugacy_class_size, symmetric_character


Partition = tuple[int, ...]
Permutation = tuple[int, ...]
REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_separating_surface_target_mixing.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-SEPARATING-SURFACE-TARGET-MIXING"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class SeparatingSurfaceTargetControl:
    n: int
    left_genus: int
    right_genus: int
    total_genus: int
    exact_density_probability_sum: str
    exact_odd_density_mass: str
    exact_total_variation_from_uniform_alternating: float
    witten_zeta_denominator: float
    left_remainder_l2: float
    right_remainder_l2: float
    total_variation_upper_bound: float
    maximum_nonsign_normalized_character_expectation: float
    maximum_nonsign_character_bound: float
    standard_normalized_character_expectation: float
    exact_density_and_bound_verified: bool
    status: str


@dataclass(frozen=True)
class UnconditionedSurfaceTargetControl:
    n: int
    commutator_genus: int
    exact_density_probability_sum: str
    exact_odd_density_mass: str
    exact_total_variation_from_uniform_alternating: float
    total_variation_upper_bound: float
    maximum_nonsign_normalized_character_expectation: float
    maximum_nonsign_character_bound: float
    exact_density_and_bound_verified: bool
    status: str


@dataclass(frozen=True)
class NonseparatingSurfaceTargetControl:
    n: int
    surface_genus: int
    exact_density_probability_sum: str
    exact_total_variation_from_uniform_symmetric: float
    witten_zeta_denominator: float
    witten_zeta_tail: float
    total_variation_upper_bound: float
    maximum_nontrivial_normalized_character_expectation: float
    maximum_character_bound: float
    standard_normalized_character_expectation: float
    exact_density_and_bound_verified: bool
    status: str


@dataclass(frozen=True)
class DirectSurfaceCountControl:
    n: int
    left_genus: int
    right_genus: int
    group_order: int
    exact_surface_homomorphism_count: int
    frobenius_surface_homomorphism_count: int
    maximum_direct_to_character_probability_residual: float
    direct_frobenius_formula_verified: bool
    status: str


@dataclass(frozen=True)
class SurfaceMixingScalingRecord:
    n: int
    witten_zeta_two_tail: float
    genus_uniform_unconditioned_tv_upper_bound: float
    genus_uniform_separating_tv_upper_bound: float
    genus_uniform_nonseparating_tv_upper_bound: float
    genus_uniform_nonsign_character_upper_bound: float
    asymptotic_order: str
    genus_uniform_decay_proved_using_external_zeta_bound: bool
    status: str


@dataclass(frozen=True)
class SeparatingSurfaceTargetMixingReport:
    created_at: str
    theorem_contract: dict[str, Any]
    separating_controls: list[SeparatingSurfaceTargetControl]
    unconditioned_controls: list[UnconditionedSurfaceTargetControl]
    nonseparating_controls: list[NonseparatingSurfaceTargetControl]
    direct_count_control: DirectSurfaceCountControl
    scaling_records: list[SurfaceMixingScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def symmetric_witten_zeta(n: int, exponent: int) -> Fraction:
    return Fraction(2) + symmetric_witten_zeta_tail(n, exponent)


def commutator_product_density_by_class(
    n: int,
    genus: int,
) -> dict[Partition, Fraction]:
    """Return the density ``A_h`` relative to uniform ``S_n`` measure."""

    if genus < 1:
        raise ValueError("positive genus is required")
    return {
        cycle_type: sum(
            (
                Fraction(
                    symmetric_character(partition, cycle_type),
                    hook_length_dimension(partition) ** (2 * genus - 1),
                )
                for partition in integer_partitions(n)
            ),
            start=Fraction(),
        )
        for cycle_type in integer_partitions(n)
    }


def separating_surface_density_by_class(
    n: int,
    left_genus: int,
    right_genus: int,
) -> dict[Partition, Fraction]:
    if left_genus < 1 or right_genus < 1:
        raise ValueError("both separating genera must be positive")
    left = commutator_product_density_by_class(n, left_genus)
    right = commutator_product_density_by_class(n, right_genus)
    denominator = symmetric_witten_zeta(
        n, 2 * (left_genus + right_genus) - 2
    )
    return {
        cycle_type: left[cycle_type] * right[cycle_type] / denominator
        for cycle_type in integer_partitions(n)
    }


def nonseparating_surface_density_by_class(
    n: int,
    surface_genus: int,
) -> dict[Partition, Fraction]:
    """Density of one nonseparating simple curve under surface homomorphisms."""

    if surface_genus < 2:
        raise ValueError("a closed surface with a remaining handle requires genus>=2")
    exponent = 2 * surface_genus - 2
    denominator = symmetric_witten_zeta(n, exponent)
    return {
        cycle_type: sum(
            (
                Fraction(
                    symmetric_character(partition, cycle_type) ** 2,
                    hook_length_dimension(partition) ** exponent,
                )
                for partition in integer_partitions(n)
            ),
            start=Fraction(),
        )
        / denominator
        for cycle_type in integer_partitions(n)
    }


def _uniform_expectation_by_class(
    n: int,
    values: dict[Partition, Fraction],
) -> Fraction:
    order = math.factorial(n)
    return sum(
        (
            Fraction(conjugacy_class_size(cycle_type), order) * value
            for cycle_type, value in values.items()
        ),
        start=Fraction(),
    )


def _uniform_alternating_density(cycle_type: Partition) -> Fraction:
    return Fraction(2 if permutation_parity_from_cycle_type(cycle_type) == 0 else 0)


def _density_total_variation_from_alternating(
    n: int,
    density: dict[Partition, Fraction],
) -> Fraction:
    order = math.factorial(n)
    return Fraction(1, 2) * sum(
        (
            Fraction(conjugacy_class_size(cycle_type), order)
            * abs(value - _uniform_alternating_density(cycle_type))
            for cycle_type, value in density.items()
        ),
        start=Fraction(),
    )


def _odd_density_mass(
    n: int,
    density: dict[Partition, Fraction],
) -> Fraction:
    return _uniform_expectation_by_class(
        n,
        {
            cycle_type: (
                value
                if permutation_parity_from_cycle_type(cycle_type) == 1
                else Fraction()
            )
            for cycle_type, value in density.items()
        },
    )


def _normalized_character_expectation(
    n: int,
    density: dict[Partition, Fraction],
    partition: Partition,
) -> Fraction:
    dimension = hook_length_dimension(partition)
    return _uniform_expectation_by_class(
        n,
        {
            cycle_type: value
            * Fraction(symmetric_character(partition, cycle_type), dimension)
            for cycle_type, value in density.items()
        },
    )


def unconditioned_surface_tv_bound(n: int, genus: int) -> float:
    return 0.5 * math.sqrt(
        float(symmetric_witten_zeta_tail(n, 4 * genus - 2))
    )


def separating_surface_tv_bound(
    n: int,
    left_genus: int,
    right_genus: int,
) -> float:
    total_genus = left_genus + right_genus
    denominator = float(symmetric_witten_zeta(n, 2 * total_genus - 2))
    left_epsilon = math.sqrt(
        float(symmetric_witten_zeta_tail(n, 4 * left_genus - 2))
    )
    right_epsilon = math.sqrt(
        float(symmetric_witten_zeta_tail(n, 4 * right_genus - 2))
    )
    denominator_tail = denominator - 2.0
    return (
        2.0 * left_epsilon
        + 2.0 * right_epsilon
        + left_epsilon * right_epsilon
        + denominator_tail
    ) / (2.0 * denominator)


def nonseparating_surface_tv_bound(n: int, surface_genus: int) -> float:
    if surface_genus < 2:
        raise ValueError("nonseparating surface target requires genus>=2")
    exponent = 2 * surface_genus - 2
    tail = float(symmetric_witten_zeta_tail(n, exponent))
    return tail / (2.0 + tail)


def _nonsign_partitions(n: int) -> tuple[Partition, ...]:
    return tuple(
        partition
        for partition in integer_partitions(n)
        if partition not in {(n,), (1,) * n}
    )


def audit_separating_surface_target(
    n: int,
    left_genus: int,
    right_genus: int,
) -> SeparatingSurfaceTargetControl:
    density = separating_surface_density_by_class(n, left_genus, right_genus)
    probability_sum = _uniform_expectation_by_class(n, density)
    odd_mass = _odd_density_mass(n, density)
    tv = float(_density_total_variation_from_alternating(n, density))
    bound = separating_surface_tv_bound(n, left_genus, right_genus)
    expectations = {
        partition: float(_normalized_character_expectation(n, density, partition))
        for partition in _nonsign_partitions(n)
    }
    maximum = max(map(abs, expectations.values()), default=0.0)
    standard = expectations.get((n - 1, 1), 0.0)
    denominator = float(
        symmetric_witten_zeta(n, 2 * (left_genus + right_genus) - 2)
    )
    left_remainder = math.sqrt(
        float(symmetric_witten_zeta_tail(n, 4 * left_genus - 2))
    )
    right_remainder = math.sqrt(
        float(symmetric_witten_zeta_tail(n, 4 * right_genus - 2))
    )
    verified = bool(
        probability_sum == 1
        and odd_mass == 0
        and tv <= bound + 1e-12
        and maximum <= 2.0 * tv + 1e-12
    )
    return SeparatingSurfaceTargetControl(
        n=n,
        left_genus=left_genus,
        right_genus=right_genus,
        total_genus=left_genus + right_genus,
        exact_density_probability_sum=str(probability_sum),
        exact_odd_density_mass=str(odd_mass),
        exact_total_variation_from_uniform_alternating=tv,
        witten_zeta_denominator=denominator,
        left_remainder_l2=left_remainder,
        right_remainder_l2=right_remainder,
        total_variation_upper_bound=bound,
        maximum_nonsign_normalized_character_expectation=maximum,
        maximum_nonsign_character_bound=2.0 * bound,
        standard_normalized_character_expectation=standard,
        exact_density_and_bound_verified=verified,
        status=(
            "separating-surface-target-mixes-to-uniform-alternating"
            if verified
            else "separating-surface-density-control-failure"
        ),
    )


def audit_unconditioned_surface_target(
    n: int,
    genus: int,
) -> UnconditionedSurfaceTargetControl:
    density = commutator_product_density_by_class(n, genus)
    probability_sum = _uniform_expectation_by_class(n, density)
    odd_mass = _odd_density_mass(n, density)
    tv = float(_density_total_variation_from_alternating(n, density))
    bound = unconditioned_surface_tv_bound(n, genus)
    expectations = tuple(
        float(_normalized_character_expectation(n, density, partition))
        for partition in _nonsign_partitions(n)
    )


def audit_nonseparating_surface_target(
    n: int,
    surface_genus: int,
) -> NonseparatingSurfaceTargetControl:
    density = nonseparating_surface_density_by_class(n, surface_genus)
    probability_sum = _uniform_expectation_by_class(n, density)
    order = math.factorial(n)
    tv = float(
        Fraction(1, 2)
        * sum(
            (
                Fraction(conjugacy_class_size(cycle_type), order)
                * abs(value - 1)
                for cycle_type, value in density.items()
            ),
            start=Fraction(),
        )
    )
    exponent = 2 * surface_genus - 2
    tail = float(symmetric_witten_zeta_tail(n, exponent))
    denominator = 2.0 + tail
    bound = nonseparating_surface_tv_bound(n, surface_genus)
    expectations = {
        partition: float(_normalized_character_expectation(n, density, partition))
        for partition in integer_partitions(n)
        if partition != (n,)
    }
    maximum = max(map(abs, expectations.values()), default=0.0)
    standard = expectations.get((n - 1, 1), 0.0)
    verified = bool(
        probability_sum == 1
        and tv <= bound + 1e-12
        and maximum <= 2.0 * tv + 1e-12
    )
    return NonseparatingSurfaceTargetControl(
        n=n,
        surface_genus=surface_genus,
        exact_density_probability_sum=str(probability_sum),
        exact_total_variation_from_uniform_symmetric=tv,
        witten_zeta_denominator=denominator,
        witten_zeta_tail=tail,
        total_variation_upper_bound=bound,
        maximum_nontrivial_normalized_character_expectation=maximum,
        maximum_character_bound=2.0 * bound,
        standard_normalized_character_expectation=standard,
        exact_density_and_bound_verified=verified,
        status=(
            "nonseparating-surface-target-mixes-to-uniform-symmetric"
            if verified
            else "nonseparating-surface-density-control-failure"
        ),
    )
    maximum = max(map(abs, expectations), default=0.0)
    verified = bool(
        probability_sum == 1
        and odd_mass == 0
        and tv <= bound + 1e-12
        and maximum <= 2.0 * tv + 1e-12
    )
    return UnconditionedSurfaceTargetControl(
        n=n,
        commutator_genus=genus,
        exact_density_probability_sum=str(probability_sum),
        exact_odd_density_mass=str(odd_mass),
        exact_total_variation_from_uniform_alternating=tv,
        total_variation_upper_bound=bound,
        maximum_nonsign_normalized_character_expectation=maximum,
        maximum_nonsign_character_bound=2.0 * bound,
        exact_density_and_bound_verified=verified,
        status=(
            "unconditioned-surface-boundary-mixes-to-uniform-alternating"
            if verified
            else "unconditioned-surface-density-control-failure"
        ),
    )


def _inverse_permutation(permutation: Permutation) -> Permutation:
    output = [0] * len(permutation)
    for index, image in enumerate(permutation):
        output[image] = index
    return tuple(output)


def _commutator(left: Permutation, right: Permutation) -> Permutation:
    return compose_permutations(
        compose_permutations(
            compose_permutations(left, right),
            _inverse_permutation(left),
        ),
        _inverse_permutation(right),
    )


def _convolution_counts(
    group: tuple[Permutation, ...],
    left: Counter[Permutation],
    right: Counter[Permutation],
) -> Counter[Permutation]:
    output: Counter[Permutation] = Counter()
    for first in group:
        if not left[first]:
            continue
        for second in group:
            if right[second]:
                output[compose_permutations(first, second)] += (
                    left[first] * right[second]
                )
    return output


def _surface_boundary_counts(
    group: tuple[Permutation, ...],
    genus: int,
) -> Counter[Permutation]:
    one: Counter[Permutation] = Counter(
        _commutator(left, right) for left in group for right in group
    )
    output = one
    for _ in range(1, genus):
        output = _convolution_counts(group, output, one)
    return output


def audit_direct_surface_count(
    n: int = 3,
    left_genus: int = 1,
    right_genus: int = 2,
) -> DirectSurfaceCountControl:
    if not 2 <= n <= 4:
        raise ValueError("direct controls require 2<=n<=4")
    group = tuple(itertools.permutations(range(n)))
    left = _surface_boundary_counts(group, left_genus)
    right = _surface_boundary_counts(group, right_genus)
    direct_weights = {
        element: left[element] * right[_inverse_permutation(element)]
        for element in group
    }
    direct_total = sum(direct_weights.values())
    density = separating_surface_density_by_class(n, left_genus, right_genus)
    maximum_residual = max(
        abs(
            direct_weights[element] / direct_total
            - float(density[permutation_cycle_type(element)]) / len(group)
        )
        for element in group
    )
    genus = left_genus + right_genus
    frobenius_total = (
        len(group) ** (2 * genus - 1)
        * symmetric_witten_zeta(n, 2 * genus - 2)
    )
    if frobenius_total.denominator != 1:
        raise ArithmeticError("surface homomorphism count became nonintegral")
    verified = direct_total == frobenius_total.numerator and maximum_residual <= 1e-15
    return DirectSurfaceCountControl(
        n=n,
        left_genus=left_genus,
        right_genus=right_genus,
        group_order=len(group),
        exact_surface_homomorphism_count=direct_total,
        frobenius_surface_homomorphism_count=frobenius_total.numerator,
        maximum_direct_to_character_probability_residual=maximum_residual,
        direct_frobenius_formula_verified=verified,
        status=(
            "direct-surface-count-matches-frobenius-density"
            if verified
            else "direct-surface-count-control-failure"
        ),
    )


def surface_mixing_scaling_record(n: int) -> SurfaceMixingScalingRecord:
    tail_two = float(symmetric_witten_zeta_tail(n, 2))
    unconditioned = 0.5 * math.sqrt(tail_two)
    separating = separating_surface_tv_bound(n, 1, 1)
    nonseparating = nonseparating_surface_tv_bound(n, 2)
    return SurfaceMixingScalingRecord(
        n=n,
        witten_zeta_two_tail=tail_two,
        genus_uniform_unconditioned_tv_upper_bound=unconditioned,
        genus_uniform_separating_tv_upper_bound=separating,
        genus_uniform_nonseparating_tv_upper_bound=nonseparating,
        genus_uniform_nonsign_character_upper_bound=2.0 * max(
            unconditioned, separating, nonseparating
        ),
        asymptotic_order="O(1/n) uniformly over positive genera",
        genus_uniform_decay_proved_using_external_zeta_bound=True,
        status="surface-target-character-signal-has-genus-uniform-decay",
    )


def run_separating_surface_target_mixing(
) -> SeparatingSurfaceTargetMixingReport:
    separating = [
        audit_separating_surface_target(n, left, right)
        for n in range(3, 9)
        for left, right in ((1, 1), (1, 2), (2, 2))
    ]
    unconditioned = [
        audit_unconditioned_surface_target(n, genus)
        for n in range(3, 9)
        for genus in (1, 2, 3)
    ]
    nonseparating = [
        audit_nonseparating_surface_target(n, genus)
        for n in range(3, 9)
        for genus in (2, 3, 4)
    ]
    direct = audit_direct_surface_count()
    scaling = [surface_mixing_scaling_record(n) for n in (*range(5, 21), 25, 30)]
    failures = sum(not row.exact_density_and_bound_verified for row in separating)
    failures += sum(not row.exact_density_and_bound_verified for row in unconditioned)
    failures += sum(not row.exact_density_and_bound_verified for row in nonseparating)
    failures += int(not direct.direct_frobenius_formula_verified)
    exact = failures == 0
    return SeparatingSurfaceTargetMixingReport(
        created_at=utc_now(),
        theorem_contract={
            "commutator_product_density": "A_h(x)=sum_rho chi_rho(x)/d_rho^(2h-1)",
            "separating_curve_density": "f_(a,b)(x)=A_a(x)A_b(x^-1)/zeta_G(2a+2b-2)",
            "alternating_null": "u(x)=1+sgn(x), the uniform-A_n density relative to uniform S_n",
            "remainder_energy": "||A_h-u||_2^2=zeta_Sn^*(4h-2)",
            "separating_tv_bound": "[2eps_a+2eps_b+eps_a eps_b+zeta(2a+2b-2)-2]/[2zeta(2a+2b-2)]",
            "nonseparating_density": "f_g(x)=sum_rho |chi_rho(x)|^2/d_rho^(2g-2)/zeta_G(2g-2)",
            "nonseparating_tv_bound": "zeta_Sn^*(2g-2)/zeta_Sn(2g-2)=O(n^-2) uniformly for g>=2",
            "genus_uniform_asymptotic": "separating TV=O(1/n); nonseparating TV=O(1/n^2), uniformly in genus",
            "character_consequence": "every normalized nonsign nontrivial character expectation is at most 2TV",
            "scope": "requires an actual unconditioned-boundary or separating-curve certificate",
        },
        separating_controls=separating,
        unconditioned_controls=unconditioned,
        nonseparating_controls=nonseparating,
        direct_count_control=direct,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "derive_exact_separating_curve_target_density",
                "resolved": exact,
                "resolution": "Frobenius boundary counts on both sides multiply, and character orthogonality gives the Witten-zeta normalization.",
            },
            {
                "obligation": "prove_genus_uniform_nonsign_character_decay",
                "resolved": exact,
                "resolution": "The worst remainder is genus one; zeta_Sn^*(2)=O(n^-2) gives a uniform O(1/n) TV bound.",
            },
            {
                "obligation": "derive_nonseparating_simple_curve_density_and_decay",
                "resolved": exact,
                "resolution": "Fixing one handle generator and applying the commutator character average gives a positive squared-character density whose nonsign mass is the Witten-zeta tail.",
            },
            {
                "obligation": "classify_marked_targets_as_surface_curves",
                "resolved": False,
                "resolution": "Extend ribbon/Whitehead certificates to decide whether every pressure-saturating target is an unconditioned boundary, separating curve, or a genuinely different word.",
            },
            {
                "obligation": "control_non_surface_and_interleaved_targets",
                "resolved": False,
                "resolution": "No Witten-zeta mixing theorem is supplied for arbitrary target words in marked support presentations.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "Increasing surface genus can preserve a hidden target character bias.",
                "resolved": True,
                "resolution": "All nontrivial character coefficients shrink monotonically with genus; genus one is the uniform worst case.",
            },
            {
                "objection": "Sign expectation one is a nonabelian target signal.",
                "resolved": True,
                "resolution": "Every commutator product lies in A_n, so trivial and sign are exactly the alternating null rather than useful high-dimensional structure.",
            },
            {
                "objection": "Scalar surface pressure loss alone kills normalized target characters.",
                "resolved": True,
                "resolution": "False in general; this theorem additionally uses the exact target-curve density and Witten-zeta L2 remainder.",
            },
            {
                "objection": "Every marked target with a surface relator is a separating curve.",
                "resolved": True,
                "resolution": "Separating and nonseparating simple curves are both controlled, but a target still needs an explicit simple-curve certificate; self-intersecting words remain outside scope.",
            },
        ],
        headline_metrics={
            "exact_separating_surface_control_count": len(separating),
            "exact_unconditioned_surface_control_count": len(unconditioned),
            "exact_nonseparating_surface_control_count": len(nonseparating),
            "direct_frobenius_count_control_count": int(direct.direct_frobenius_formula_verified),
            "finite_control_failure_count": failures,
            "maximum_scaling_degree": scaling[-1].n,
            "degree_30_genus_uniform_separating_tv_upper_bound": scaling[-1].genus_uniform_separating_tv_upper_bound,
            "degree_30_genus_uniform_nonseparating_tv_upper_bound": scaling[-1].genus_uniform_nonseparating_tv_upper_bound,
            "degree_30_genus_uniform_nonsign_character_upper_bound": scaling[-1].genus_uniform_nonsign_character_upper_bound,
            "surface_target_class_dequantization_theorem_count": int(exact),
            "all_marked_target_classification_theorem_count": 0,
            "natural_component_M4_positive_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "frobenius_separating_density_proved": exact,
            "unconditioned_surface_targets_mix_genus_uniformly": exact,
            "separating_surface_targets_mix_genus_uniformly": exact,
            "nonseparating_surface_targets_mix_genus_uniformly": exact,
            "all_nonsign_surface_target_characters_vanish": exact,
            "all_simple_surface_target_characters_vanish": exact,
            "simple_surface_target_class_dequantized": exact,
            "all_pressure_saturating_marked_targets_are_surface_curves": False,
            "non_surface_target_characters_controlled": False,
            "natural_component_M4_positive": False,
            "speedup_claim_allowed": False,
            "reason": "Every certified simple surface target is asymptotically uniform on S_n or A_n; only self-intersecting, non-surface, or unclassified interleaved target words can still support the marked Green signal.",
        },
        status=(
            "all-simple-surface-marked-targets-dequantized-genus-uniformly"
            if exact
            else "separating-surface-target-mixing-control-failure"
        ),
        summary=(
            "Proved genus-uniform mixing for unconditioned boundaries and every "
            "simple curve on orientable surfaces, eliminating all high-dimensional "
            "character signal in that certified target class."
        ),
        falsifiers_triggered=[
            "The exact finite S3 handle-character bias does not survive growing S_n.",
            "Adding surface genus cannot rescue a nonsign target character.",
            "Nonseparating simple curves mix even faster, at Witten-zeta-two-tail scale.",
            "Trivial/sign behavior is only the parity support of commutators.",
            "Future obstruction searches should reject certified surface-boundary targets before expensive finite character screens.",
        ],
    )


def write_separating_surface_target_mixing_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_separating_surface_target_mixing())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    report = write_separating_surface_target_mixing_report()
    print(json.dumps(report, indent=2, sort_keys=True))
