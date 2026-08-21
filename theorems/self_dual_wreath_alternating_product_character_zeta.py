"""Exact character-zeta formulas kill the order-three and order-four blocks.

Let ``G=A_n`` and retain only class functions that are constant on the
``S_n`` cycle type.  These functions have an orthonormal character basis
indexed by transpose orbits of ``S_n`` partitions.  A non-self-conjugate
orbit restricts to one ``A_n`` irrep.  A self-conjugate partition splits into
two equal-dimensional irreps, and the coarse character is their normalized
sum.

The normalized convolution algebra is diagonal in this basis.  Excluding the
constant orbit, one multiplication-triangle ANOVA block has energy

    E3(n) = sum_(nonself orbits) d_lambda^-2
            + 2 sum_(self-conjugate lambda) d_lambda^-2,       (1)

and one three-input/product-output block has energy

    E4(n) = sum_(nonself orbits) d_lambda^-4
            + 4 sum_(self-conjugate lambda) d_lambda^-4.       (2)

There are four order-three and three order-four blocks.  If

    Zeta_s^*(S_n)=sum_(lambda notin {triv,sign}) d_lambda^-s,

then ``E3<=2 Zeta_2^*`` and ``E4<=4 Zeta_4^*``.  The symmetric-group Witten
zeta estimate ``Zeta_2^*=O(n^-2)`` proves order-three decay.  For ``n>=5``,
every nontrivial nonsign irrep has dimension at least ``n-1``, hence

    Zeta_4^* <= (n-1)^-2 Zeta_2^* = O(n^-4).              (3)

Thus the seven order-three/order-four blocks vanish by exact harmonic
diagonalization, independently of the five-label marginal bound.  This does
not estimate the order-five blocks, the unique order-six synergy, or any
non-Haar Racah information.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable

from representation_obstruction import (
    conjugate_partition,
    hook_length_dimension,
    integer_partitions,
)
from research_registry import utc_now
from self_dual_wreath_alternating_block_operator_anova import (
    audit_block_operator_anova,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_alternating_product_character_zeta.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-ALTERNATING-PRODUCT-CHARACTER-ZETA"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]


@dataclass(frozen=True)
class CoarseCharacterOrbit:
    representative: Partition
    transpose: Partition
    dimension: int
    self_conjugate: bool
    constant_orbit: bool


@dataclass(frozen=True)
class ProductCharacterZetaFiniteControl:
    n: int
    nonconstant_nonself_orbit_count: int
    nonconstant_self_conjugate_count: int
    order_three_block_count: int
    order_four_block_count: int
    exact_one_order_three_energy: str
    exact_one_order_four_energy: str
    numerical_one_order_three_energy: float
    numerical_one_order_four_energy: float
    numerical_order_three_total_energy: float
    numerical_order_four_total_energy: float
    maximum_order_three_formula_residual: float
    maximum_order_four_formula_residual: float
    order_three_total_formula_residual: float
    order_four_total_formula_residual: float
    exact_product_character_formulas_verified: bool
    status: str


@dataclass(frozen=True)
class ProductCharacterZetaScalingControl:
    n: int
    partition_count: int
    minimum_nontrivial_nonsign_dimension: int
    witten_zeta_two_tail: float
    witten_zeta_four_tail: float
    one_order_three_energy: float
    one_order_four_energy: float
    order_three_zeta_upper: float
    order_four_zeta_upper: float
    order_four_minimum_degree_upper: float
    n_squared_order_three_energy: float
    n_fourth_order_four_energy: float
    zeta_domination_verified: bool
    minimum_degree_transfer_verified: bool
    status: str


@dataclass(frozen=True)
class ProductCharacterZetaTheorem:
    coarse_character_convolution_diagonalization: str
    one_order_three_block_formula: str
    one_order_four_block_formula: str
    order_three_total_asymptotic: str
    order_four_total_asymptotic: str
    order_five_blocks_controlled_by_this_theorem: bool
    order_six_block_controlled_by_this_theorem: bool
    status: str


@dataclass(frozen=True)
class AlternatingProductCharacterZetaReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: ProductCharacterZetaTheorem
    exact_controls: list[ProductCharacterZetaFiniteControl]
    scaling_controls: list[ProductCharacterZetaScalingControl]
    literature_basis: list[dict[str, str]]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def coarse_character_orbits(n: int) -> tuple[CoarseCharacterOrbit, ...]:
    if n < 2:
        raise ValueError("coarse alternating character orbits require n>=2")
    seen: set[Partition] = set()
    output: list[CoarseCharacterOrbit] = []
    constant_pair = {(n,), (1,) * n}
    for partition in integer_partitions(n):
        if partition in seen:
            continue
        transpose = conjugate_partition(partition)
        seen.update((partition, transpose))
        output.append(
            CoarseCharacterOrbit(
                representative=partition,
                transpose=transpose,
                dimension=hook_length_dimension(partition),
                self_conjugate=partition == transpose,
                constant_orbit=partition in constant_pair,
            )
        )
    return tuple(output)


def coarse_product_character_energy(n: int, input_count: int) -> Fraction:
    """Return one centered multiplication-block energy exactly.

    ``input_count=2`` is the order-three triangle and ``input_count=3`` is
    the order-four three-input/product-output tensor.
    """

    if input_count not in (2, 3):
        raise ValueError("implemented multiplication blocks have two or three inputs")
    exponent = 2 * (input_count - 1)
    total = Fraction(0, 1)
    for orbit in coarse_character_orbits(n):
        if orbit.constant_orbit:
            continue
        split_multiplier = 2 ** (input_count - 1) if orbit.self_conjugate else 1
        total += Fraction(split_multiplier, orbit.dimension**exponent)
    return total


def symmetric_witten_zeta_tail(n: int, exponent: int) -> Fraction:
    if exponent <= 0:
        raise ValueError("Witten-zeta exponent must be positive")
    return sum(
        (
            Fraction(0, 1)
            if partition in {(n,), (1,) * n}
            else Fraction(1, hook_length_dimension(partition) ** exponent)
        )
        for partition in integer_partitions(n)
    )


def minimum_nontrivial_nonsign_dimension(n: int) -> int:
    dimensions = [
        hook_length_dimension(partition)
        for partition in integer_partitions(n)
        if partition not in {(n,), (1,) * n}
    ]
    return min(dimensions) if dimensions else 0


def _maximum_residual(values: Iterable[float], target: float) -> float:
    return max((abs(value - target) for value in values), default=0.0)


def audit_product_character_zeta_finite(
    n: int,
) -> ProductCharacterZetaFiniteControl:
    if not 2 <= n <= 5:
        raise ValueError("exact ANOVA controls require 2<=n<=5")
    order_three = coarse_product_character_energy(n, 2)
    order_four = coarse_product_character_energy(n, 3)
    anova, blocks = audit_block_operator_anova(n)
    three_blocks = [
        row.hilbert_schmidt_energy
        for row in blocks
        if row.allowed_by_forward_private_generator_test
        and row.allowed_by_inverse_private_generator_test
        and row.selected_word_count == 3
    ]
    four_blocks = [
        row.hilbert_schmidt_energy
        for row in blocks
        if row.allowed_by_forward_private_generator_test
        and row.allowed_by_inverse_private_generator_test
        and row.selected_word_count == 4
    ]
    three_value = float(order_three)
    four_value = float(order_four)
    three_residual = _maximum_residual(three_blocks, three_value)
    four_residual = _maximum_residual(four_blocks, four_value)
    three_total_residual = abs(anova.order_three_total_energy - 4.0 * three_value)
    four_total_residual = abs(anova.order_four_total_energy - 3.0 * four_value)
    tolerance = 2e-9
    exact = bool(
        len(three_blocks) == 4
        and len(four_blocks) == 3
        and three_residual <= tolerance
        and four_residual <= tolerance
        and three_total_residual <= tolerance
        and four_total_residual <= tolerance
    )
    orbits = coarse_character_orbits(n)
    return ProductCharacterZetaFiniteControl(
        n=n,
        nonconstant_nonself_orbit_count=sum(
            not orbit.constant_orbit and not orbit.self_conjugate for orbit in orbits
        ),
        nonconstant_self_conjugate_count=sum(
            not orbit.constant_orbit and orbit.self_conjugate for orbit in orbits
        ),
        order_three_block_count=len(three_blocks),
        order_four_block_count=len(four_blocks),
        exact_one_order_three_energy=str(order_three),
        exact_one_order_four_energy=str(order_four),
        numerical_one_order_three_energy=three_value,
        numerical_one_order_four_energy=four_value,
        numerical_order_three_total_energy=anova.order_three_total_energy,
        numerical_order_four_total_energy=anova.order_four_total_energy,
        maximum_order_three_formula_residual=three_residual,
        maximum_order_four_formula_residual=four_residual,
        order_three_total_formula_residual=three_total_residual,
        order_four_total_formula_residual=four_total_residual,
        exact_product_character_formulas_verified=exact,
        status=(
            "exact-coarse-product-character-zeta-formulas-verified"
            if exact
            else "product-character-zeta-formula-control-failure"
        ),
    )


def product_character_zeta_scaling_control(
    n: int,
) -> ProductCharacterZetaScalingControl:
    if n < 5:
        raise ValueError("minimum-degree zeta transfer requires n>=5")
    zeta_two = float(symmetric_witten_zeta_tail(n, 2))
    zeta_four = float(symmetric_witten_zeta_tail(n, 4))
    three = float(coarse_product_character_energy(n, 2))
    four = float(coarse_product_character_energy(n, 3))
    minimum = minimum_nontrivial_nonsign_dimension(n)
    three_upper = 2.0 * zeta_two
    four_upper = 4.0 * zeta_four
    minimum_upper = zeta_two / (n - 1) ** 2
    tolerance = 2e-14
    domination = bool(
        three <= three_upper + tolerance and four <= four_upper + tolerance
    )
    degree_transfer = bool(
        minimum >= n - 1 and zeta_four <= minimum_upper + tolerance
    )
    return ProductCharacterZetaScalingControl(
        n=n,
        partition_count=len(integer_partitions(n)),
        minimum_nontrivial_nonsign_dimension=minimum,
        witten_zeta_two_tail=zeta_two,
        witten_zeta_four_tail=zeta_four,
        one_order_three_energy=three,
        one_order_four_energy=four,
        order_three_zeta_upper=three_upper,
        order_four_zeta_upper=four_upper,
        order_four_minimum_degree_upper=minimum_upper,
        n_squared_order_three_energy=n * n * three,
        n_fourth_order_four_energy=n**4 * four,
        zeta_domination_verified=domination,
        minimum_degree_transfer_verified=degree_transfer,
        status=(
            "product-character-energies-dominated-by-witten-zeta-tails"
            if domination and degree_transfer
            else "product-character-zeta-scaling-control-failure"
        ),
    )


def run_alternating_product_character_zeta(
) -> AlternatingProductCharacterZetaReport:
    exact_controls = [audit_product_character_zeta_finite(n) for n in range(2, 6)]
    scaling = [
        product_character_zeta_scaling_control(n)
        for n in (5, 8, 12, 16, 20, 24, 30)
    ]
    failures = sum(
        not row.exact_product_character_formulas_verified for row in exact_controls
    )
    failures += sum(
        not row.zeta_domination_verified or not row.minimum_degree_transfer_verified
        for row in scaling
    )
    exact = failures == 0
    theorem = ProductCharacterZetaTheorem(
        coarse_character_convolution_diagonalization=(
            "Projected normalized convolution is diagonal in transpose-orbit characters"
        ),
        one_order_three_block_formula=(
            "E3=sum_nonself d^-2+2 sum_self d^-2"
        ),
        one_order_four_block_formula=(
            "E4=sum_nonself d^-4+4 sum_self d^-4"
        ),
        order_three_total_asymptotic="4E3=O(n^-2)",
        order_four_total_asymptotic="3E4=O(n^-4)",
        order_five_blocks_controlled_by_this_theorem=False,
        order_six_block_controlled_by_this_theorem=False,
        status=(
            "lower-product-anova-blocks-have-exact-zeta-decay"
            if exact
            else "product-character-zeta-theorem-control-failure"
        ),
    )
    return AlternatingProductCharacterZetaReport(
        created_at=utc_now(),
        theorem_contract={
            "coarse_basis": theorem.coarse_character_convolution_diagonalization,
            "triangle_energy": theorem.one_order_three_block_formula,
            "three_input_energy": theorem.one_order_four_block_formula,
            "block_multiplicities": "four order-three and three order-four blocks",
            "zeta_bounds": (
                "E3<=2 Zeta_2^*=O(n^-2); E4<=4 Zeta_4^*=O(n^-4)"
            ),
            "scope": (
                "Exact only for coarse cycle-type ANOVA blocks; order five, order six, "
                "split alternating labels, and non-Haar multiplicity data are untouched."
            ),
        },
        theorem=theorem,
        exact_controls=exact_controls,
        scaling_controls=scaling,
        literature_basis=[
            {
                "id": "teyssier-thevenin-witten-zeta-2025",
                "url": "https://arxiv.org/abs/2411.04347",
                "precise_use": (
                    "Section 6 recalls the fixed-s symmetric-group Witten-zeta tail "
                    "O(n^-s) and sharpens its range; this theorem uses s=2."
                ),
            },
            {
                "id": "symmetric-group-minimal-degree",
                "precise_use": (
                    "For n>=5 the least nontrivial nonsign S_n irrep degree is n-1, "
                    "which transfers the zeta-two tail to zeta four."
                ),
            },
        ],
        proof_obligations=[
            {
                "obligation": "diagonalize_coarse_multiplication_channel",
                "resolved": exact,
                "resolution": (
                    "Character idempotents diagonalize convolution; self-conjugate "
                    "restriction contributes the explicit split multiplicity."
                ),
            },
            {
                "obligation": "prove_order_three_and_four_anova_decay",
                "resolved": exact,
                "resolution": (
                    "Exact energy formulas plus Witten-zeta and minimum-degree bounds."
                ),
            },
            {
                "obligation": "bound_canonical_trimmed_sixway_energy",
                "resolved": False,
                "resolution": (
                    "No one-label convolution diagonalization survives the all-six "
                    "tetrahedral coupling; a multilinear projected bound is required."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Self-conjugate partitions can be counted like ordinary orbits.",
                "resolved": True,
                "resolution": (
                    "False. Restriction splits, producing factors two and four in the "
                    "triangle and three-input energies."
                ),
            },
            {
                "objection": "Finite ANOVA agreement establishes asymptotic decay.",
                "resolved": True,
                "resolution": (
                    "Decay comes from the external Witten-zeta and minimal-degree "
                    "theorems, not from S2-S5 numerics."
                ),
            },
            {
                "objection": "The same diagonal formula controls the six-way block.",
                "resolved": True,
                "resolution": (
                    "False. The tetrahedral six-way contraction couples several "
                    "character labels and is the remaining target."
                ),
            },
        ],
        headline_metrics={
            "coarse_convolution_diagonalization_theorem_count": int(exact),
            "exact_order_three_energy_formula_count": int(exact),
            "exact_order_four_energy_formula_count": int(exact),
            "order_three_decay_theorem_count": int(exact),
            "order_four_decay_theorem_count": int(exact),
            "exact_finite_control_count": len(exact_controls),
            "finite_control_failure_count": failures,
            "canonical_trimmed_sixway_bound_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "coarse_product_character_formulas_proved": exact,
            "order_three_anova_energy_vanishes_proved": exact,
            "order_four_anova_energy_vanishes_proved": exact,
            "order_five_anova_energy_vanishes_from_this_theorem": False,
            "canonical_trimmed_sixway_subpolynomial_proved": False,
            "physical_rank_profile_mixes_proved": False,
            "irreducible_racah_cmi_vanishes_proved": False,
            "classical_separation_proved": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The lower product blocks vanish exactly as zeta tails, but the unique "
                "canonical high-dimensional six-way synergy remains unbounded."
            ),
        },
        status=(
            "order-three-and-order-four-coarse-blocks-closed-by-character-zeta"
            if exact
            else "alternating-product-character-zeta-failure"
        ),
        summary=(
            "Derived exact transpose-orbit character formulas and zeta decay for all "
            "seven order-three/order-four ANOVA blocks."
        ),
        falsifiers_triggered=[
            "Ignoring self-conjugate restriction multiplicity gives wrong finite energies.",
            "A one-character convolution diagonalization does not extend to six-way synergy.",
            "Closing lower ANOVA blocks is a no-go refinement, not an algorithmic signal.",
        ],
    )


def write_alternating_product_character_zeta_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_alternating_product_character_zeta())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    result = write_alternating_product_character_zeta_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))
