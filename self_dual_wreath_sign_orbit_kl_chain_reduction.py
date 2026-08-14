"""Exact KL chain rule for tetrahedral sign orbits and syndromes.

Augment every self-conjugate partition with an independent fair orientation
bit.  Let ``O`` be the six unordered transposition orbits and let
``Z in F_2^6`` be the six orientations.  Under product Plancherel law,
``Z|O`` is exactly uniform.  The sign-twist theorem proves that the physical
likelihood depends on ``Z`` only through ``Y=A^T Z in F_2^3`` and is constant
on every eight-point kernel fiber.  Therefore

    D(P_six || Plancherel^6)
      = D(P_O || Q_O) + E_(O~P) D(P_(Y|O) || Uniform(F_2^3)).       (1)

The artificial fair bits cancel from the left side, so it is the original
six-label KL.  Moreover

    E_O D(P_(Y|O)||U) = I_P(O:Y) + D(P_Y||U).                       (2)

The preceding unconditional theorem makes the final term ``o(1)``.  Hence an
asymptotic measured-label survivor must be either dependence among the six
unoriented sign orbits or orbit-adaptive syndrome mutual information.  There
is no additional six-bit orientation channel hidden inside the labels.

This is a lossless information decomposition, not an asymptotic estimate of
either surviving term.  Both terms are classical functions of measured Young
diagrams and need same-access dequantization checks.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_sign_orbit_syndrome_reduction import (
    BitVector,
    orientation_syndrome,
    transpose_partition,
)
from self_dual_wreath_tetrahedral_chi_square_tail_no_go import (
    finite_physical_likelihood_arrays,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_sign_orbit_kl_chain_reduction.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-SIGN-ORBIT-KL-CHAIN-REDUCTION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
SignOrbit = tuple[Partition, ...]


@dataclass(frozen=True)
class SignOrbitKLChainControl:
    n: int
    partition_count: int
    sign_orbit_count: int
    nonself_sign_orbit_count: int
    self_conjugate_sign_orbit_count: int
    sign_orbit_tuple_count: int
    augmented_probability_sum_residual: float
    augmented_product_sum_residual: float
    full_six_label_kl_bits: float
    base_sign_orbit_kl_bits: float
    expected_conditional_syndrome_kl_bits: float
    unconditional_syndrome_kl_bits: float
    orbit_syndrome_mutual_information_bits: float
    kl_chain_rule_residual: float
    conditional_syndrome_information_identity_residual: float
    maximum_within_syndrome_likelihood_residual: float
    maximum_orbit_conditional_syndrome_kl_bits: float
    base_orbit_fraction_of_full_kl: float
    orbit_adaptive_fraction_of_full_kl: float
    exact_lossless_orientation_reduction_verified: bool
    status: str


@dataclass(frozen=True)
class SignOrbitKLChainReductionReport:
    created_at: str
    theorem_contract: dict[str, Any]
    exact_controls: list[SignOrbitKLChainControl]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def partition_sign_orbits(partitions: tuple[Partition, ...]) -> tuple[SignOrbit, ...]:
    remaining = set(partitions)
    output = []
    while remaining:
        partition = min(remaining)
        partner = transpose_partition(partition)
        orbit = tuple(sorted({partition, partner}))
        if any(item not in remaining for item in orbit):
            raise AssertionError("partition set is not closed under transposition")
        remaining.difference_update(orbit)
        output.append(orbit)
    return tuple(sorted(output))


def _kl_term(probability: float, reference: float) -> float:
    if probability <= 0:
        return 0.0
    if reference <= 0:
        return math.inf
    return probability * math.log2(probability / reference)


def audit_sign_orbit_kl_chain(n: int) -> SignOrbitKLChainControl:
    if not 2 <= n <= 5:
        raise ValueError("exact KL-chain controls require 2<=n<=5")
    partitions, likelihood, product, physical = finite_physical_likelihood_arrays(n)
    index = {partition: position for position, partition in enumerate(partitions)}
    orbits = partition_sign_orbits(partitions)
    orbit_weights = {
        orbit: sum(float(product[(index[partition],) * 6]) ** (1.0 / 6.0) for partition in orbit)
        for orbit in orbits
    }
    # The root above is numerically fragile for tiny atoms. Recover exact one-coordinate
    # product marginals directly from the six-dimensional array instead.
    one_coordinate_weights = {
        partition: float(np.sum(product[index[partition], ...]))
        for partition in partitions
    }
    orbit_weights = {
        orbit: sum(one_coordinate_weights[partition] for partition in orbit)
        for orbit in orbits
    }

    joint: dict[tuple[tuple[int, ...], BitVector], float] = {}
    base_probability: dict[tuple[int, ...], float] = {}
    base_reference: dict[tuple[int, ...], float] = {}
    maximum_within = 0.0
    augmented_sum = 0.0
    augmented_reference_sum = 0.0
    maximum_conditional_kl = 0.0

    for orbit_indices in itertools.product(range(len(orbits)), repeat=6):
        orbit_tuple = tuple(orbits[position] for position in orbit_indices)
        reference = math.prod(orbit_weights[orbit] for orbit in orbit_tuple)
        fixed_count = sum(len(orbit) == 1 for orbit in orbit_tuple)
        syndrome_likelihoods: dict[BitVector, list[float]] = {}
        syndrome_probability = {
            syndrome: 0.0 for syndrome in itertools.product((0, 1), repeat=3)
        }
        for orientation in itertools.product((0, 1), repeat=6):
            labels = tuple(
                orbit[orientation[axis]] if len(orbit) == 2 else orbit[0]
                for axis, orbit in enumerate(orbit_tuple)
            )
            label_indices = tuple(index[label] for label in labels)
            augmented_probability = float(physical[label_indices]) / 2**fixed_count
            augmented_reference = float(product[label_indices]) / 2**fixed_count
            syndrome = orientation_syndrome(orientation)
            syndrome_probability[syndrome] += augmented_probability
            syndrome_likelihoods.setdefault(syndrome, []).append(
                augmented_probability / augmented_reference
                if augmented_reference > 0
                else 0.0
            )
            augmented_sum += augmented_probability
            augmented_reference_sum += augmented_reference
        maximum_within = max(
            maximum_within,
            max(
                max(values) - min(values)
                for values in syndrome_likelihoods.values()
            ),
        )
        base = sum(syndrome_probability.values())
        base_probability[orbit_indices] = base
        base_reference[orbit_indices] = reference
        for syndrome, probability in syndrome_probability.items():
            joint[orbit_indices, syndrome] = probability
        if base > 0:
            conditional = tuple(
                syndrome_probability[syndrome] / base
                for syndrome in itertools.product((0, 1), repeat=3)
            )
            conditional_kl = sum(
                probability * math.log2(8.0 * probability)
                for probability in conditional
                if probability > 0
            )
            maximum_conditional_kl = max(maximum_conditional_kl, conditional_kl)

    full_kl = float(
        np.sum(
            physical[physical > 0] * np.log2(likelihood[physical > 0])
        )
    )
    base_kl = sum(
        _kl_term(base_probability[key], base_reference[key])
        for key in base_probability
    )
    conditional_kl = 0.0
    syndrome_marginal = {
        syndrome: 0.0 for syndrome in itertools.product((0, 1), repeat=3)
    }
    for (orbit_indices, syndrome), probability in joint.items():
        base = base_probability[orbit_indices]
        if probability > 0 and base > 0:
            conditional_kl += probability * math.log2(8.0 * probability / base)
        syndrome_marginal[syndrome] += probability
    syndrome_kl = sum(
        probability * math.log2(8.0 * probability)
        for probability in syndrome_marginal.values()
        if probability > 0
    )
    mutual_information = 0.0
    for (orbit_indices, syndrome), probability in joint.items():
        reference = base_probability[orbit_indices] * syndrome_marginal[syndrome]
        mutual_information += _kl_term(probability, reference)
    chain_residual = abs(full_kl - base_kl - conditional_kl)
    information_residual = abs(conditional_kl - syndrome_kl - mutual_information)
    tolerance = 1e-8
    exact = (
        abs(augmented_sum - 1.0) <= tolerance
        and abs(augmented_reference_sum - 1.0) <= tolerance
        and maximum_within <= tolerance
        and chain_residual <= tolerance
        and information_residual <= tolerance
        and conditional_kl <= 3.0 + tolerance
    )
    return SignOrbitKLChainControl(
        n=n,
        partition_count=len(partitions),
        sign_orbit_count=len(orbits),
        nonself_sign_orbit_count=sum(len(orbit) == 2 for orbit in orbits),
        self_conjugate_sign_orbit_count=sum(len(orbit) == 1 for orbit in orbits),
        sign_orbit_tuple_count=len(orbits) ** 6,
        augmented_probability_sum_residual=abs(augmented_sum - 1.0),
        augmented_product_sum_residual=abs(augmented_reference_sum - 1.0),
        full_six_label_kl_bits=max(0.0, full_kl),
        base_sign_orbit_kl_bits=max(0.0, base_kl),
        expected_conditional_syndrome_kl_bits=max(0.0, conditional_kl),
        unconditional_syndrome_kl_bits=max(0.0, syndrome_kl),
        orbit_syndrome_mutual_information_bits=max(0.0, mutual_information),
        kl_chain_rule_residual=chain_residual,
        conditional_syndrome_information_identity_residual=information_residual,
        maximum_within_syndrome_likelihood_residual=maximum_within,
        maximum_orbit_conditional_syndrome_kl_bits=maximum_conditional_kl,
        base_orbit_fraction_of_full_kl=(base_kl / full_kl if full_kl > 0 else 0.0),
        orbit_adaptive_fraction_of_full_kl=(
            conditional_kl / full_kl if full_kl > 0 else 0.0
        ),
        exact_lossless_orientation_reduction_verified=exact,
        status=(
            "exact-sign-orbit-syndrome-kl-chain-verified"
            if exact
            else "sign-orbit-kl-chain-control-failure"
        ),
    )


def run_sign_orbit_kl_chain_reduction() -> SignOrbitKLChainReductionReport:
    controls = [audit_sign_orbit_kl_chain(n) for n in range(2, 6)]
    exact = all(row.exact_lossless_orientation_reduction_verified for row in controls)
    tail = controls[-1]
    return SignOrbitKLChainReductionReport(
        created_at=utc_now(),
        theorem_contract={
            "augmented_coordinates": (
                "O is the unordered transposition-orbit tuple and Z has one fair "
                "orientation bit per label, including artificial bits on fixed orbits."
            ),
            "product_factorization": "Under Plancherel^6, Q(O,Z)=Q_O(O)/64.",
            "orientation_sufficiency": (
                "The physical likelihood depends on Z only through Y=A^T Z and is "
                "constant on every eight-point kernel fiber."
            ),
            "kl_chain": (
                "D(P_six||Pl^6)=D(P_O||Q_O)+E_O D(P(Y|O)||Uniform(F_2^3))."
            ),
            "mutual_information_split": (
                "E_O D(P(Y|O)||U)=I_P(O:Y)+D(P_Y||U)."
            ),
            "scope": (
                "The reduction is exact but does not bound base-orbit KL or "
                "orbit-syndrome mutual information asymptotically."
            ),
        },
        exact_controls=controls,
        proof_obligations=[
            {
                "obligation": "prove_three_bit_syndrome_is_sufficient_for_all_orientation_information",
                "resolved": exact,
                "resolution": (
                    "Sign twisting gives likelihood invariance on ker(A^T), including "
                    "fairly lifted self-conjugate coordinates."
                ),
            },
            {
                "obligation": "decompose_full_six_label_kl_losslessly",
                "resolved": exact,
                "resolution": (
                    "Apply the KL chain rule to (O,Z), then use the sufficient statistic Y."
                ),
            },
            {
                "obligation": "bound_high_dimensional_base_sign_orbit_kl",
                "resolved": False,
                "resolution": (
                    "Project the tetrahedral word map onto transposition-even central "
                    "functions and prove mixing or find positive retained mass."
                ),
            },
            {
                "obligation": "bound_high_dimensional_orbit_syndrome_mutual_information",
                "resolved": False,
                "resolution": (
                    "Control the seven parity-sector Fourier kernels after conditioning "
                    "on six base orbits, or construct a positive-mass survivor."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Six orientation bits may contain information beyond Y.",
                "resolved": True,
                "resolution": (
                    "False: the exact likelihood is constant on all eight z values with "
                    "the same syndrome, so the kernel coordinates are ancillary."
                ),
            },
            {
                "objection": "Artificial self-conjugate bits change the original KL.",
                "resolved": True,
                "resolution": (
                    "False: the same independent fair kernel is appended to P and Q, "
                    "which leaves relative entropy invariant."
                ),
            },
            {
                "objection": "Vanishing unconditional syndrome closes orientation dependence.",
                "resolved": True,
                "resolution": (
                    "False: the exact split leaves I(O:Y), which can remain nonzero even "
                    "when P_Y is uniform."
                ),
            },
            {
                "objection": "Either remaining KL term is automatically quantum leverage.",
                "resolved": True,
                "resolution": (
                    "False: both are statistics of measured Young diagrams and require "
                    "natural-input classical comparison."
                ),
            },
        ],
        headline_metrics={
            "lossless_sign_orbit_kl_chain_theorem_count": int(exact),
            "orientation_input_bit_count": 6,
            "sufficient_orientation_syndrome_bit_count": 3,
            "discarded_ancillary_orientation_bit_count": 3,
            "finite_control_count": len(controls),
            "maximum_finite_chain_residual": max(
                row.kl_chain_rule_residual for row in controls
            ),
            "S5_full_six_label_kl_bits": tail.full_six_label_kl_bits,
            "S5_base_sign_orbit_kl_bits": tail.base_sign_orbit_kl_bits,
            "S5_orbit_adaptive_syndrome_kl_bits": (
                tail.expected_conditional_syndrome_kl_bits
            ),
            "S5_orbit_syndrome_mutual_information_bits": (
                tail.orbit_syndrome_mutual_information_bits
            ),
            "asymptotic_surviving_term_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "orientation_information_reduces_losslessly_to_three_bits": exact,
            "full_six_label_kl_chain_decomposition_proved": exact,
            "base_sign_orbit_kl_vanishes_proved": False,
            "orbit_syndrome_mutual_information_vanishes_proved": False,
            "measured_label_signal_survives_proved": False,
            "classical_separation_proved": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The exact decomposition removes ancillary orientations but leaves two "
                "high-dimensional classical label-information terms unbounded."
            ),
        },
        status=(
            "six-label-kl-reduced-to-base-orbits-and-adaptive-syndrome"
            if exact
            else "sign-orbit-kl-chain-control-failure"
        ),
        summary=(
            "Decomposed all measured tetrahedral KL into base sign-orbit dependence and "
            "a three-bit orbit-adaptive syndrome channel."
        ),
        falsifiers_triggered=[
            "Three of six orientation bits are exactly ancillary.",
            "Uniform raw syndrome does not imply zero orbit-adaptive information.",
            "The surviving measured-label problem has two explicit classical terms.",
        ],
    )


def write_sign_orbit_kl_chain_reduction_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_sign_orbit_kl_chain_reduction())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    result = write_sign_orbit_kl_chain_reduction_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))
