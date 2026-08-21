"""A denominator-free trim transfer for orbit-adaptive sign syndrome.

Let ``O`` be the six unoriented sign-orbit labels, ``Q`` their product
Plancherel law, and ``F_x(O)`` the eight input-parity partition functions from
the alternating parity-coset reduction.  Thus ``P_O(O)=Q(O)F_0(O)`` and

    P(Y=y|O)=1/8 [1+sum_(x!=0)(-1)^(x.y)F_x(O)/F_0(O)].

The apparent small-denominator problem disappears after weighting by the
physical base law.  For any retained orbit set ``B``, Walsh Parseval and
Cauchy--Schwarz give

    E_P[1_B TV(P_(Y|O),U_3)]
      = sum_(O in B) Q(O)/16 sum_y |sum_(x!=0)(-1)^(x.y)F_x(O)|
      <= 1/2 sqrt(Q(B) S_B),                                  (1)

where

    S_B=sum_(O in B) Q(O) sum_(x!=0) F_x(O)^2.                (2)

If ``B_D`` requires all six Specht dimensions to exceed ``D``, exact
Plancherel marginals imply

    P(B_D^c),Q(B_D^c) <= delta_D=6 p(n)D^2/n!.                (3)

Consequently

    E_P TV(P_(Y|O),U_3) <= delta_D + 1/2 sqrt(Q(B_D)S_(B_D)). (4)

Entropy continuity then bounds the expected conditional KL, and hence
``I(O:Y)``, by ``h_2(epsilon)+epsilon log2(7)`` for the right side of (4)
capped at ``7/8``.

There is also an exact subtraction identity.  Because a sign-invariant
dimension trim has uniform orientation bits under product Plancherel and each
syndrome has eight preimages,

    S_B = M_full(B)-M_base(B) = C_full(B)-C_base(B),           (5)

where ``M`` denotes the retained likelihood second moment and ``C`` the
retained subprobability chi-square.  Thus adaptive syndrome decay requires no
ratio estimate: it is exactly the excess projected ``S_n`` word-map energy
over the coarse ``A_n`` base energy.

Equations (1)--(5) are transfer identities, not asymptotic mixing estimates.
The remaining theorem is to prove ``S_(B_D)=o(1)`` at the canonical
near-maximal dimension threshold, or find positive retained TV/KL mass.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_alternating_base_orbit_reduction import (
    aggregate_sign_orbit_law,
    coarse_alternating_plancherel_weights,
)
from self_dual_wreath_alternating_parity_coset_channel import (
    parity_coset_word_likelihood_arrays,
)
from self_dual_wreath_tetrahedral_chi_square_tail_no_go import (
    finite_physical_likelihood_arrays,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_adaptive_syndrome_trim_transfer.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-ADAPTIVE-SYNDROME-TRIM-TRANSFER"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

BitVector = tuple[int, int, int]


@dataclass(frozen=True)
class AdaptiveSyndromeTrimControl:
    n: int
    minimum_retained_dimension_exclusive: int
    retained_coarse_label_count: int
    retained_product_mass: float
    retained_physical_mass: float
    removed_physical_mass: float
    removed_physical_mass_union_bound: float
    exact_expected_conditional_tv: float
    exact_removed_expected_conditional_tv: float
    exact_retained_expected_conditional_tv: float
    denominator_free_retained_l1_expression: float
    retained_parity_coset_energy: float
    retained_tv_cauchy_upper_bound: float
    total_tv_trim_transfer_upper_bound: float
    exact_expected_conditional_kl_bits: float
    entropy_continuity_kl_upper_bound_bits: float
    full_retained_likelihood_second_moment: float
    base_retained_likelihood_second_moment: float
    second_moment_excess: float
    full_retained_subprobability_chi_square: float
    base_retained_subprobability_chi_square: float
    chi_square_excess: float
    maximum_transfer_identity_residual: float
    exact_denominator_free_trim_transfer_verified: bool
    status: str


@dataclass(frozen=True)
class AdaptiveSyndromeTrimTransferReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[AdaptiveSyndromeTrimControl]
    asymptotic_transfer: dict[str, str | bool]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def binary_entropy_bits(value: float) -> float:
    if value <= 0.0 or value >= 1.0:
        return 0.0
    return -value * math.log2(value) - (1.0 - value) * math.log2(1.0 - value)


def entropy_continuity_bound_bits(average_tv_upper_bound: float) -> float:
    epsilon = min(7.0 / 8.0, max(0.0, average_tv_upper_bound))
    return binary_entropy_bits(epsilon) + epsilon * math.log2(7.0)


def _coarse_retained_mask(
    orbits: tuple[tuple[tuple[int, ...], ...], ...],
    minimum_dimension_exclusive: int,
) -> np.ndarray:
    dimensions = np.asarray(
        [hook_length_dimension(orbit[0]) for orbit in orbits],
        dtype=int,
    )
    retained = dimensions > minimum_dimension_exclusive
    mask = np.ones((len(orbits),) * 6, dtype=bool)
    for axis in range(6):
        shape = [1] * 6
        shape[axis] = len(orbits)
        mask &= retained.reshape(shape)
    return mask


def _full_retained_mask(
    partitions: tuple[tuple[int, ...], ...],
    minimum_dimension_exclusive: int,
) -> np.ndarray:
    dimensions = np.asarray(
        [hook_length_dimension(partition) for partition in partitions],
        dtype=int,
    )
    retained = dimensions > minimum_dimension_exclusive
    mask = np.ones((len(partitions),) * 6, dtype=bool)
    for axis in range(6):
        shape = [1] * 6
        shape[axis] = len(partitions)
        mask &= retained.reshape(shape)
    return mask


def _conditional_information_contributions(
    product: np.ndarray,
    arrays: dict[BitVector, np.ndarray],
) -> tuple[np.ndarray, np.ndarray]:
    """Return the physical-weighted conditional TV and KL per base orbit."""

    base = arrays[(0, 0, 0)]
    tv = np.zeros_like(base)
    kl = np.zeros_like(base)
    nonzero = tuple(parity for parity in arrays if parity != (0, 0, 0))
    for syndrome in itertools.product((0, 1), repeat=3):
        perturbation = sum(
            (-1) ** sum(a * b for a, b in zip(parity, syndrome))
            * arrays[parity]
            for parity in nonzero
        )
        joint = product * (base + perturbation) / 8.0
        reference = product * base / 8.0
        tv += 0.5 * np.abs(joint - reference)
        positive = (joint > 0.0) & (reference > 0.0)
        kl[positive] += joint[positive] * np.log2(
            joint[positive] / reference[positive]
        )
    return tv, kl


def audit_adaptive_syndrome_trim_transfer(
    n: int,
    minimum_dimension_exclusive: int,
) -> AdaptiveSyndromeTrimControl:
    if not 2 <= n <= 5:
        raise ValueError("exact trim-transfer controls require 2<=n<=5")
    if minimum_dimension_exclusive < 0:
        raise ValueError("the dimension threshold must be nonnegative")

    orbits, arrays = parity_coset_word_likelihood_arrays(n)
    aggregate_orbits, base_likelihood, base_product, base_physical = (
        aggregate_sign_orbit_law(n)
    )
    if orbits != aggregate_orbits:
        raise AssertionError("coarse orbit order mismatch")
    _orbits, weight_map = coarse_alternating_plancherel_weights(n)
    retained_mask = _coarse_retained_mask(orbits, minimum_dimension_exclusive)
    retained_label_count = sum(
        hook_length_dimension(orbit[0]) > minimum_dimension_exclusive
        for orbit in orbits
    )

    tv_contribution, kl_contribution = _conditional_information_contributions(
        base_product,
        arrays,
    )
    retained_tv = float(np.sum(tv_contribution[retained_mask]))
    removed_tv = float(np.sum(tv_contribution[~retained_mask]))
    exact_tv = retained_tv + removed_tv
    exact_kl = float(np.sum(kl_contribution))

    nonzero_arrays = tuple(
        array
        for parity, array in arrays.items()
        if parity != (0, 0, 0)
    )
    energy_array = sum(array * array for array in nonzero_arrays)
    retained_energy = float(np.sum(base_product[retained_mask] * energy_array[retained_mask]))

    # This is the first line of (1), evaluated without F_x/F_0 divisions.
    denominator_free_tv = 0.0
    for syndrome in itertools.product((0, 1), repeat=3):
        perturbation = sum(
            (-1) ** sum(a * b for a, b in zip(parity, syndrome))
            * array
            for parity, array in arrays.items()
            if parity != (0, 0, 0)
        )
        denominator_free_tv += float(
            np.sum(base_product[retained_mask] * np.abs(perturbation[retained_mask]))
        ) / 16.0

    retained_product_mass = float(np.sum(base_product[retained_mask]))
    retained_physical_mass = float(np.sum(base_physical[retained_mask]))
    removed_physical_mass = max(0.0, 1.0 - retained_physical_mass)
    cauchy_bound = 0.5 * math.sqrt(
        max(0.0, retained_product_mass * retained_energy)
    )
    partition_count = len(integer_partitions(n))
    union_bound = min(
        1.0,
        6.0
        * partition_count
        * minimum_dimension_exclusive**2
        / math.factorial(n),
    )
    total_tv_bound = min(1.0, union_bound + cauchy_bound)
    kl_bound = entropy_continuity_bound_bits(total_tv_bound)

    partitions, full_likelihood, full_product, full_physical = (
        finite_physical_likelihood_arrays(n)
    )
    full_mask = _full_retained_mask(partitions, minimum_dimension_exclusive)
    full_second = float(
        np.sum(full_product[full_mask] * full_likelihood[full_mask] ** 2)
    )
    base_second = float(
        np.sum(base_product[retained_mask] * base_likelihood[retained_mask] ** 2)
    )
    full_chi = float(
        np.sum(full_product[full_mask] * (full_likelihood[full_mask] - 1.0) ** 2)
    )
    base_chi = float(
        np.sum(base_product[retained_mask] * (base_likelihood[retained_mask] - 1.0) ** 2)
    )
    second_excess = full_second - base_second
    chi_excess = full_chi - base_chi
    mass_residual = max(
        abs(float(np.sum(full_product[full_mask])) - retained_product_mass),
        abs(float(np.sum(full_physical[full_mask])) - retained_physical_mass),
    )
    residual = max(
        abs(retained_tv - denominator_free_tv),
        abs(second_excess - retained_energy),
        abs(chi_excess - retained_energy),
        mass_residual,
        max(0.0, retained_tv - cauchy_bound),
        max(0.0, removed_physical_mass - union_bound),
        max(0.0, exact_tv - (removed_physical_mass + cauchy_bound)),
        max(0.0, exact_kl - entropy_continuity_bound_bits(exact_tv)),
    )
    tolerance = 2e-8
    exact = bool(
        residual <= tolerance
        and abs(sum(weight_map.values()) - 1.0) <= tolerance
        and retained_energy >= -tolerance
    )
    return AdaptiveSyndromeTrimControl(
        n=n,
        minimum_retained_dimension_exclusive=minimum_dimension_exclusive,
        retained_coarse_label_count=retained_label_count,
        retained_product_mass=retained_product_mass,
        retained_physical_mass=retained_physical_mass,
        removed_physical_mass=removed_physical_mass,
        removed_physical_mass_union_bound=union_bound,
        exact_expected_conditional_tv=exact_tv,
        exact_removed_expected_conditional_tv=removed_tv,
        exact_retained_expected_conditional_tv=retained_tv,
        denominator_free_retained_l1_expression=denominator_free_tv,
        retained_parity_coset_energy=max(0.0, retained_energy),
        retained_tv_cauchy_upper_bound=cauchy_bound,
        total_tv_trim_transfer_upper_bound=total_tv_bound,
        exact_expected_conditional_kl_bits=max(0.0, exact_kl),
        entropy_continuity_kl_upper_bound_bits=kl_bound,
        full_retained_likelihood_second_moment=full_second,
        base_retained_likelihood_second_moment=base_second,
        second_moment_excess=max(0.0, second_excess),
        full_retained_subprobability_chi_square=full_chi,
        base_retained_subprobability_chi_square=base_chi,
        chi_square_excess=max(0.0, chi_excess),
        maximum_transfer_identity_residual=residual,
        exact_denominator_free_trim_transfer_verified=exact,
        status=(
            "exact-denominator-free-adaptive-trim-transfer-verified"
            if exact
            else "adaptive-syndrome-trim-transfer-control-failure"
        ),
    )


def run_adaptive_syndrome_trim_transfer() -> AdaptiveSyndromeTrimTransferReport:
    controls = [
        audit_adaptive_syndrome_trim_transfer(n, threshold)
        for n, threshold in (
            (2, 0),
            (3, 0),
            (3, 1),
            (4, 1),
            (4, 2),
            (5, 1),
            (5, 4),
        )
    ]
    exact = all(row.exact_denominator_free_trim_transfer_verified for row in controls)
    n5_trim = next(
        row
        for row in controls
        if row.n == 5 and row.minimum_retained_dimension_exclusive == 1
    )
    return AdaptiveSyndromeTrimTransferReport(
        created_at=utc_now(),
        theorem_contract={
            "denominator_cancellation": (
                "Physical weighting cancels F_0 from conditional syndrome TV, "
                "leaving Q-weighted absolute parity-coset Fourier sums."
            ),
            "retained_tv_bound": (
                "E[1_B TV(P(Y|O),U_3)] <= (1/2)sqrt(Q(B)S_B), where "
                "S_B=sum_(O in B)Q(O)sum_(x!=0)F_x(O)^2."
            ),
            "dimension_tail": "P(B_D^c),Q(B_D^c)<=6p(n)D^2/n!.",
            "conditional_kl_transfer": (
                "If epsilon bounds average conditional TV, expected conditional "
                "KL and I(O:Y) are at most h_2(epsilon)+epsilon log2(7)."
            ),
            "projected_energy_subtraction": (
                "S_B=M_full(B)-M_base(B)=C_full(B)-C_base(B)."
            ),
            "scope": (
                "The identities reduce adaptive decay to S_(B_D)=o(1); they do "
                "not prove that projected excess-energy estimate."
            ),
        },
        finite_controls=controls,
        asymptotic_transfer={
            "canonical_threshold": "D_n=floor(sqrt(n!)/(p(n)log2(n!)))",
            "tail_bound": "delta_n<=6/[p(n)log2(n!)^2]=o(1)",
            "sufficient_energy_condition": "S_(B_(D_n))=o(1)",
            "consequence": "E conditional TV, E conditional KL, and I(O:Y) are o(1)",
            "ratio_denominator_lower_bound_required": False,
            "full_and_base_projected_estimates_must_be_matched": True,
            "canonical_energy_decay_proved": False,
        },
        proof_obligations=[
            {
                "obligation": "remove_F0_denominator_from_adaptive_syndrome_control",
                "resolved": exact,
                "resolution": (
                    "Weight conditional TV by P_O=Q_OF_0, apply Walsh Parseval, "
                    "then Cauchy--Schwarz under Q_O."
                ),
            },
            {
                "obligation": "identify_adaptive_energy_with_projected_word_map_excess",
                "resolved": exact,
                "resolution": (
                    "Uniform sign orientations and eight-to-one syndrome fibers give "
                    "M_full=sum_x E_Q F_x^2; matched mass terms cancel in chi-square."
                ),
            },
            {
                "obligation": "prove_canonical_face_twist_energy_vanishes",
                "resolved": False,
                "resolution": (
                    "Bound one dimension-trimmed face parity-coset partition function "
                    "in product-measure L2, or construct retained positive L1 mass."
                ),
            },
            {
                "obligation": "prove_canonical_opposite_twist_energy_vanishes",
                "resolved": False,
                "resolution": (
                    "Do the same for one opposite-complement twist; tetrahedral "
                    "symmetry supplies the remaining two sectors."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Small F_0 values make conditional ratios uncontrollable.",
                "resolved": True,
                "resolution": (
                    "F_0 cancels exactly in physical-weighted conditional TV; no "
                    "likelihood floor is required."
                ),
            },
            {
                "objection": "Two large projected second moments cannot be subtracted safely.",
                "resolved": True,
                "resolution": (
                    "Their difference is the manifestly nonnegative sum of seven "
                    "parity-coset energies; estimate that direct form analytically."
                ),
            },
            {
                "objection": "Vanishing adaptive syndrome energy proves the full measured law mixes.",
                "resolved": False,
                "resolution": (
                    "The coarse A_n base-orbit KL is a separate term in the lossless chain."
                ),
            },
            {
                "objection": "A finite retained energy is a quantum advantage signal.",
                "resolved": False,
                "resolution": (
                    "It is a classical word-map statistic and has neither asymptotic "
                    "positive mass nor a natural-input separation."
                ),
            },
        ],
        headline_metrics={
            "denominator_free_trim_transfer_theorem_count": int(exact),
            "projected_energy_subtraction_theorem_count": int(exact),
            "finite_control_count": len(controls),
            "maximum_transfer_identity_residual": max(
                row.maximum_transfer_identity_residual for row in controls
            ),
            "S5_after_one_dimensional_trim_adaptive_energy": (
                n5_trim.retained_parity_coset_energy
            ),
            "S5_after_one_dimensional_trim_exact_retained_tv": (
                n5_trim.exact_retained_expected_conditional_tv
            ),
            "canonical_adaptive_energy_decay_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "adaptive_denominator_eliminated_proved": exact,
            "adaptive_energy_is_projected_excess_proved": exact,
            "canonical_face_twist_energy_vanishes_proved": False,
            "canonical_opposite_twist_energy_vanishes_proved": False,
            "canonical_adaptive_syndrome_decouples_proved": False,
            "canonical_adaptive_syndrome_survives_proved": False,
            "coarse_An_base_law_decouples_proved": False,
            "classical_separation_proved": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The ratio problem is removed, but the canonical dimension-trimmed "
                "face and opposite projected energies remain unbounded."
            ),
        },
        status=(
            "adaptive-syndrome-reduced-to-denominator-free-projected-energy"
            if exact
            else "adaptive-syndrome-trim-transfer-control-failure"
        ),
        summary=(
            "Eliminated the conditional-likelihood denominator and reduced adaptive "
            "syndrome information to a nonnegative projected word-map excess energy."
        ),
        falsifiers_triggered=[
            "No lower bound on the coarse A_n likelihood F_0 is needed.",
            "Adaptive syndrome energy is not an independent seventh-order object; it is the full-minus-base projected excess.",
            "Finite retained L2 energy remains insufficient without asymptotic L1/KL mass and dequantization checks.",
        ],
    )


def write_adaptive_syndrome_trim_transfer_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_adaptive_syndrome_trim_transfer())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    result = write_adaptive_syndrome_trim_transfer_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))
