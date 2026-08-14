"""Sign-orbit syndrome reduction for the tetrahedral six-label law.

Removing the trivial and sign representations does not remove the action of
the sign character.  For every partition ``rho`` of ``n``, tensoring the
corresponding irrep with sign transposes the Young diagram.  On a six-tuple of
non-self-conjugate sign orbits, write ``z in F_2^6`` for the six transpose
choices in label order ``(alpha,beta,gamma,mu,nu,lambda)``.

The exact word-map likelihood uses

    (gk, ghk, hk, g, h, k).

If ``x=(sgn(g),sgn(h),sgn(k))`` is encoded additively, transposing labels by
``z`` multiplies the summand by ``(-1)^(z . A x)``, where

    A x = (x_g+x_k, x_g+x_h+x_k, x_h+x_k, x_g, x_h, x_k).

Consequently the likelihood depends on ``z`` only through

    A^T z = (
        z_alpha+z_beta+z_mu,
        z_beta+z_gamma+z_nu,
        z_alpha+z_beta+z_gamma+z_lambda,
    ).

There are eight syndromes and every syndrome has eight transpose choices.
Equivalently, the Walsh transform of the 64 orientation likelihoods is
supported on the three-dimensional image of ``A``.  This is an exact
representation-theoretic reduction, not a finite-size conjecture.

After conditioning on any retained non-self-conjugate sign-orbit sector, the
product Plancherel law is uniform on the 64 orientation choices.  The KL chain
rule therefore becomes

    D(P || Q) = D(P_orbit || Q_orbit)
              + E_(P_orbit) D(P_syndrome || Uniform(F_2^3)).

The second term is at most three bits.  It is a directly readable classical
label statistic.  Finite controls show that it can be nonzero even after
one-dimensional labels are removed, so the old parity-tail deletion is not a
proof of a product law.  No asymptotic survival follows: self-conjugate
partitions, canonical high-dimensional mass, coherent multiplicity phases,
and classical access costs remain separate obligations.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

import numpy as np

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_tetrahedral_chi_square_tail_no_go import (
    finite_physical_likelihood_arrays,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_sign_orbit_syndrome_reduction.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-SIGN-ORBIT-SYNDROME-REDUCTION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
BitVector = tuple[int, ...]
SignOrbit = tuple[Partition, Partition]

LABEL_NAMES = ("alpha", "beta", "gamma", "mu", "nu", "lambda")


@dataclass(frozen=True)
class SignOrbitFourierControl:
    control_id: str
    n: int
    base_partitions: tuple[Partition, ...]
    base_dimensions: tuple[int, ...]
    orientation_count: int
    syndrome_count: int
    orientations_per_syndrome: int
    walsh_support: tuple[BitVector, ...]
    expected_walsh_support: tuple[BitVector, ...]
    maximum_outside_support_coefficient: float
    maximum_within_syndrome_likelihood_residual: float
    distinct_likelihood_values: tuple[float, ...]
    conditional_orientation_total_variation: float
    conditional_orientation_kl_bits: float
    exact_three_bit_syndrome_reduction_verified: bool
    status: str


@dataclass(frozen=True)
class RetainedSignOrbitControl:
    n: int
    minimum_retained_dimension_exclusive: int
    retained_sign_pair_count: int
    retained_self_conjugate_partition_count: int
    retained_paired_plancherel_mass: float
    retained_self_conjugate_plancherel_mass: float
    self_conjugate_six_label_union_mass_upper_bound: float
    nonself_orbit_tuple_count: int
    nonself_product_sector_mass: float
    nonself_physical_sector_mass: float
    conditional_total_variation: float
    conditional_base_orbit_total_variation: float
    expected_conditional_syndrome_total_variation: float
    conditional_kl_bits: float
    conditional_base_orbit_kl_bits: float
    conditional_syndrome_kl_bits: float
    kl_chain_rule_residual: float
    maximum_conditional_syndrome_total_variation: float
    maximum_within_syndrome_likelihood_residual: float
    exact_conditional_kl_decomposition_verified: bool
    status: str


@dataclass(frozen=True)
class SelfConjugateMassScalingRecord:
    n: int
    self_conjugate_partition_count: int
    self_conjugate_plancherel_mass: float
    six_label_union_mass_upper_bound: float
    asymptotic_vanishing_proved: bool
    status: str


@dataclass(frozen=True)
class SignOrbitSyndromeReductionReport:
    created_at: str
    theorem_contract: dict[str, Any]
    exact_fourier_controls: list[SignOrbitFourierControl]
    retained_sector_controls: list[RetainedSignOrbitControl]
    self_conjugate_mass_scaling: list[SelfConjugateMassScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def transpose_partition(partition: Partition) -> Partition:
    """Return the conjugate Young diagram."""

    if not partition or any(part <= 0 for part in partition):
        raise ValueError("partition must contain positive parts")
    return tuple(
        sum(part >= column for part in partition)
        for column in range(1, partition[0] + 1)
    )


def sign_frequency(input_parities: BitVector) -> BitVector:
    """Map parities of ``(g,h,k)`` to the six word parities ``A x``."""

    if len(input_parities) != 3 or any(bit not in (0, 1) for bit in input_parities):
        raise ValueError("input parity must belong to F_2^3")
    g, h, k = input_parities
    return (g ^ k, g ^ h ^ k, h ^ k, g, h, k)


def orientation_syndrome(orientation: BitVector) -> BitVector:
    """Return ``A^T z`` for six Young-diagram transpose choices."""

    if len(orientation) != 6 or any(bit not in (0, 1) for bit in orientation):
        raise ValueError("orientation must belong to F_2^6")
    alpha, beta, gamma, mu, nu, lam = orientation
    return (
        alpha ^ beta ^ mu,
        beta ^ gamma ^ nu,
        alpha ^ beta ^ gamma ^ lam,
    )


def sign_orbits(
    n: int,
    minimum_dimension_exclusive: int = 0,
) -> tuple[tuple[SignOrbit, ...], tuple[Partition, ...]]:
    """Split a dimension-retained set into sign pairs and fixed partitions."""

    if n < 2 or minimum_dimension_exclusive < 0:
        raise ValueError("invalid sign-orbit parameters")
    pairs: list[SignOrbit] = []
    fixed: list[Partition] = []
    for partition in integer_partitions(n):
        if hook_length_dimension(partition) <= minimum_dimension_exclusive:
            continue
        partner = transpose_partition(partition)
        if partition == partner:
            fixed.append(partition)
        elif partition < partner:
            pairs.append((partition, partner))
    return tuple(pairs), tuple(fixed)


def _orientation_likelihoods(
    n: int,
    base_partitions: Iterable[Partition],
) -> dict[BitVector, float]:
    partitions, likelihood, _product, _physical = finite_physical_likelihood_arrays(n)
    base = tuple(base_partitions)
    if len(base) != 6:
        raise ValueError("exactly six base partitions are required")
    index = {partition: position for position, partition in enumerate(partitions)}
    orbits = []
    for partition in base:
        partner = transpose_partition(partition)
        if partition == partner:
            raise ValueError("Fourier controls require non-self-conjugate partitions")
        orbits.append((index[partition], index[partner]))
    return {
        orientation: float(
            likelihood[
                tuple(orbits[axis][orientation[axis]] for axis in range(6))
            ]
        )
        for orientation in itertools.product((0, 1), repeat=6)
    }


def audit_sign_orbit_fourier_control(
    control_id: str,
    n: int,
    base_partitions: Iterable[Partition],
) -> SignOrbitFourierControl:
    """Verify the exact three-bit reduction on one finite label-orbit tuple."""

    base = tuple(base_partitions)
    values = _orientation_likelihoods(n, base)
    orientations = tuple(values)
    expected_support = tuple(
        sign_frequency(bits) for bits in itertools.product((0, 1), repeat=3)
    )
    coefficients: dict[BitVector, float] = {}
    for frequency in itertools.product((0, 1), repeat=6):
        coefficients[frequency] = sum(
            (-1) ** sum(a * b for a, b in zip(frequency, orientation))
            * value
            for orientation, value in values.items()
        ) / 64.0
    scale = max(1.0, max(abs(value) for value in values.values()))
    tolerance = 1e-9 * scale
    support = tuple(
        frequency
        for frequency, coefficient in coefficients.items()
        if abs(coefficient) > tolerance
    )
    expected_set = set(expected_support)
    outside = max(
        (
            abs(coefficient)
            for frequency, coefficient in coefficients.items()
            if frequency not in expected_set
        ),
        default=0.0,
    )
    syndrome_rows: dict[BitVector, list[float]] = {}
    for orientation, value in values.items():
        syndrome_rows.setdefault(orientation_syndrome(orientation), []).append(value)
    within = max(
        max(row) - min(row)
        for row in syndrome_rows.values()
    )
    total = sum(values.values())
    if total <= 0:
        orientation_tv = 0.0
        orientation_kl = 0.0
    else:
        probabilities = np.asarray(tuple(values.values()), dtype=float) / total
        orientation_tv = 0.5 * float(np.sum(np.abs(probabilities - 1.0 / 64.0)))
        positive = probabilities > 0
        orientation_kl = float(
            np.sum(probabilities[positive] * np.log2(64.0 * probabilities[positive]))
        )
    exact = (
        len(syndrome_rows) == 8
        and all(len(row) == 8 for row in syndrome_rows.values())
        and outside <= tolerance
        and within <= tolerance
        and orientation_kl <= 3.0 + 1e-9
    )
    return SignOrbitFourierControl(
        control_id=control_id,
        n=n,
        base_partitions=base,
        base_dimensions=tuple(hook_length_dimension(partition) for partition in base),
        orientation_count=64,
        syndrome_count=len(syndrome_rows),
        orientations_per_syndrome=min(len(row) for row in syndrome_rows.values()),
        walsh_support=support,
        expected_walsh_support=expected_support,
        maximum_outside_support_coefficient=outside,
        maximum_within_syndrome_likelihood_residual=within,
        distinct_likelihood_values=tuple(
            sorted({round(value, 14) for value in values.values()})
        ),
        conditional_orientation_total_variation=orientation_tv,
        conditional_orientation_kl_bits=max(0.0, orientation_kl),
        exact_three_bit_syndrome_reduction_verified=exact,
        status=(
            "exact-three-bit-sign-orbit-syndrome-verified"
            if exact
            else "sign-orbit-syndrome-control-failure"
        ),
    )


def _kl_term(probability: float, reference: float) -> float:
    if probability <= 0:
        return 0.0
    if reference <= 0:
        return math.inf
    return probability * math.log2(probability / reference)


def audit_retained_sign_orbit_sector(
    n: int,
    minimum_dimension_exclusive: int,
) -> RetainedSignOrbitControl:
    """Split retained non-self-conjugate KL into orbit and syndrome terms."""

    partitions, likelihood, product, physical = finite_physical_likelihood_arrays(n)
    index = {partition: position for position, partition in enumerate(partitions)}
    pairs, fixed = sign_orbits(n, minimum_dimension_exclusive)
    order = math.factorial(n)
    paired_mass = sum(
        2 * hook_length_dimension(pair[0]) ** 2 / order for pair in pairs
    )
    fixed_mass = sum(
        hook_length_dimension(partition) ** 2 / order for partition in fixed
    )
    orbit_rows: list[tuple[float, float, np.ndarray]] = []
    maximum_within = 0.0
    for orbit_tuple in itertools.product(pairs, repeat=6):
        point_probabilities = []
        point_references = []
        likelihood_by_syndrome: dict[BitVector, list[float]] = {}
        for orientation in itertools.product((0, 1), repeat=6):
            label_indices = tuple(
                index[orbit_tuple[axis][orientation[axis]]]
                for axis in range(6)
            )
            point_probabilities.append(float(physical[label_indices]))
            point_references.append(float(product[label_indices]))
            likelihood_by_syndrome.setdefault(
                orientation_syndrome(orientation), []
            ).append(float(likelihood[label_indices]))
        maximum_within = max(
            maximum_within,
            max(
                max(rows) - min(rows)
                for rows in likelihood_by_syndrome.values()
            ),
        )
        p_points = np.asarray(point_probabilities, dtype=float)
        q_points = np.asarray(point_references, dtype=float)
        orbit_rows.append((float(np.sum(p_points)), float(np.sum(q_points)), p_points))

    physical_mass = sum(row[0] for row in orbit_rows)
    product_mass = sum(row[1] for row in orbit_rows)
    total_tv = 0.0
    base_tv = 0.0
    expected_orientation_tv = 0.0
    total_kl = 0.0
    base_kl = 0.0
    orientation_kl = 0.0
    maximum_orientation_tv = 0.0
    if physical_mass > 0 and product_mass > 0:
        for p_orbit, q_orbit, p_points in orbit_rows:
            p_base = p_orbit / physical_mass
            q_base = q_orbit / product_mass
            base_tv += abs(p_base - q_base) / 2.0
            base_kl += _kl_term(p_base, q_base)
            q_point = q_orbit / 64.0
            for p_point in p_points:
                total_tv += abs(
                    p_point / physical_mass - q_point / product_mass
                ) / 2.0
                total_kl += _kl_term(
                    p_point / physical_mass,
                    q_point / product_mass,
                )
            if p_orbit > 0:
                conditional = p_points / p_orbit
                orientation_tv = 0.5 * float(
                    np.sum(np.abs(conditional - 1.0 / 64.0))
                )
                positive = conditional > 0
                conditional_kl = float(
                    np.sum(
                        conditional[positive]
                        * np.log2(64.0 * conditional[positive])
                    )
                )
                expected_orientation_tv += p_base * orientation_tv
                orientation_kl += p_base * conditional_kl
                maximum_orientation_tv = max(
                    maximum_orientation_tv,
                    orientation_tv,
                )
    chain_residual = abs(total_kl - base_kl - orientation_kl)
    tolerance = 1e-8
    exact = (
        len(orbit_rows) == len(pairs) ** 6
        and abs(product_mass - paired_mass**6) <= tolerance
        and maximum_within <= tolerance
        and chain_residual <= tolerance
        and orientation_kl <= 3.0 + tolerance
    )
    return RetainedSignOrbitControl(
        n=n,
        minimum_retained_dimension_exclusive=minimum_dimension_exclusive,
        retained_sign_pair_count=len(pairs),
        retained_self_conjugate_partition_count=len(fixed),
        retained_paired_plancherel_mass=paired_mass,
        retained_self_conjugate_plancherel_mass=fixed_mass,
        self_conjugate_six_label_union_mass_upper_bound=min(1.0, 6.0 * fixed_mass),
        nonself_orbit_tuple_count=len(orbit_rows),
        nonself_product_sector_mass=product_mass,
        nonself_physical_sector_mass=physical_mass,
        conditional_total_variation=total_tv,
        conditional_base_orbit_total_variation=base_tv,
        expected_conditional_syndrome_total_variation=expected_orientation_tv,
        conditional_kl_bits=max(0.0, total_kl),
        conditional_base_orbit_kl_bits=max(0.0, base_kl),
        conditional_syndrome_kl_bits=max(0.0, orientation_kl),
        kl_chain_rule_residual=chain_residual,
        maximum_conditional_syndrome_total_variation=maximum_orientation_tv,
        maximum_within_syndrome_likelihood_residual=maximum_within,
        exact_conditional_kl_decomposition_verified=exact,
        status=(
            "exact-retained-orbit-syndrome-kl-decomposition"
            if exact
            else "retained-orbit-syndrome-control-failure"
        ),
    )


def self_conjugate_mass_scaling_record(n: int) -> SelfConjugateMassScalingRecord:
    pairs, fixed = sign_orbits(n)
    del pairs
    order = math.factorial(n)
    mass = sum(hook_length_dimension(partition) ** 2 for partition in fixed) / order
    return SelfConjugateMassScalingRecord(
        n=n,
        self_conjugate_partition_count=len(fixed),
        self_conjugate_plancherel_mass=mass,
        six_label_union_mass_upper_bound=min(1.0, 6.0 * mass),
        asymptotic_vanishing_proved=False,
        status="finite-self-conjugate-mass-only-asymptotic-gate-open",
    )


def run_sign_orbit_syndrome_reduction() -> SignOrbitSyndromeReductionReport:
    fourier = [
        audit_sign_orbit_fourier_control(
            "one-dimensional-parity-tail",
            3,
            ((3,),) * 6,
        ),
        audit_sign_orbit_fourier_control(
            "S4-standard-sign-pair",
            4,
            ((3, 1),) * 6,
        ),
        audit_sign_orbit_fourier_control(
            "S5-two-row-sign-pair",
            5,
            ((3, 2),) * 6,
        ),
        audit_sign_orbit_fourier_control(
            "S5-standard-sign-pair",
            5,
            ((4, 1),) * 6,
        ),
    ]
    retained = [
        audit_retained_sign_orbit_sector(n, threshold)
        for n, threshold in ((3, 0), (4, 1), (4, 2), (5, 1), (5, 4))
    ]
    self_scaling = [
        self_conjugate_mass_scaling_record(n)
        for n in (3, 4, 5, 6, 8, 10, 15, 20, 30, 40, 50)
    ]
    exact = all(
        row.exact_three_bit_syndrome_reduction_verified for row in fourier
    ) and all(row.exact_conditional_kl_decomposition_verified for row in retained)
    high_dimension_finite_signal = next(
        row for row in fourier if row.control_id == "S5-two-row-sign-pair"
    )
    n4_standard = next(
        row for row in fourier if row.control_id == "S4-standard-sign-pair"
    )
    maximum_chain_residual = max(row.kl_chain_rule_residual for row in retained)
    return SignOrbitSyndromeReductionReport(
        created_at=utc_now(),
        theorem_contract={
            "sign_twist": "V_(rho^T)=V_rho tensor sign and chi_(rho^T)(g)=sgn(g)chi_rho(g).",
            "word_parity_map": (
                "A(g,h,k)=(g+k,g+h+k,h+k,g,h,k) over F_2 in label order "
                "(alpha,beta,gamma,mu,nu,lambda)."
            ),
            "orientation_syndrome": (
                "A^T z=(z_alpha+z_beta+z_mu, z_beta+z_gamma+z_nu, "
                "z_alpha+z_beta+z_gamma+z_lambda)."
            ),
            "exact_reduction": (
                "The 64 transpose-choice likelihoods are constant on the eight "
                "cosets of ker(A^T), and their Walsh support is im(A)."
            ),
            "kl_chain_rule": (
                "On a retained non-self-conjugate sector, conditional KL equals "
                "base sign-orbit KL plus expected three-bit syndrome KL."
            ),
            "scope": (
                "The theorem neither proves self-conjugate Plancherel mass vanishes "
                "nor bounds the canonical high-dimensional syndrome law."
            ),
        },
        exact_fourier_controls=fourier,
        retained_sector_controls=retained,
        self_conjugate_mass_scaling=self_scaling,
        proof_obligations=[
            {
                "obligation": "reduce_high_dimensional_sign_orientation_to_exact_syndromes",
                "resolved": exact,
                "resolution": (
                    "The sign-twist character identity gives the rank-three word-parity "
                    "map and exact Walsh support im(A)."
                ),
            },
            {
                "obligation": "separate_base_orbit_and_orientation_information",
                "resolved": exact,
                "resolution": (
                    "The conditional product law is uniform on orientations, so KL "
                    "splits exactly by the chain rule."
                ),
            },
            {
                "obligation": "prove_self_conjugate_plancherel_mass_vanishes",
                "resolved": False,
                "resolution": (
                    "Finite scaling is recorded, but no local-limit or anti-concentration "
                    "theorem is imported as an asymptotic proof."
                ),
            },
            {
                "obligation": "bound_canonical_high_dimension_syndrome_kl",
                "resolved": False,
                "resolution": (
                    "Prove the three nonlocal parity-sector character moments vanish, "
                    "or exhibit a retained positive-mass orbit family."
                ),
            },
            {
                "obligation": "establish_nonclassical_value_of_any_syndrome_survivor",
                "resolved": False,
                "resolution": (
                    "The syndrome is computed directly from six measured Young diagrams; "
                    "a survivor needs an oracle-access separation or coherent extension."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Deleting one-dimensional labels deletes sign parity.",
                "resolved": True,
                "resolution": (
                    "False: every non-self-conjugate high-dimensional irrep belongs to "
                    "a sign pair, and S5 has an exact nonuniform retained control."
                ),
            },
            {
                "objection": "A finite nonuniform syndrome is asymptotic evidence.",
                "resolved": True,
                "resolution": (
                    "False: the finite controls do not establish retained Plancherel mass "
                    "or a nonvanishing limit under the canonical dimension trim."
                ),
            },
            {
                "objection": "Three syndrome bits constitute a quantum decoder.",
                "resolved": True,
                "resolution": (
                    "False: they are a deterministic classical function of measured "
                    "partition labels and carry at most three bits per sample."
                ),
            },
            {
                "objection": "Orientation uniformity forces the whole retained law to be product.",
                "resolved": True,
                "resolution": (
                    "False: the base sign-orbit term remains independent in the exact KL split."
                ),
            },
        ],
        headline_metrics={
            "exact_sign_orbit_syndrome_theorem_count": int(exact),
            "orientation_bit_count": 6,
            "effective_syndrome_bit_count": 3,
            "maximum_orientation_kl_bits": 3,
            "finite_non_one_dimensional_syndrome_signal_count": int(
                high_dimension_finite_signal.conditional_orientation_kl_bits > 1e-9
            ),
            "S5_two_row_orientation_kl_bits": (
                high_dimension_finite_signal.conditional_orientation_kl_bits
            ),
            "S4_standard_orientation_kl_bits": n4_standard.conditional_orientation_kl_bits,
            "maximum_finite_kl_chain_rule_residual": maximum_chain_residual,
            "canonical_asymptotic_syndrome_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "exact_three_bit_orientation_reduction_proved": exact,
            "deleting_one_dimensional_labels_removes_all_parity_signal": False,
            "self_conjugate_plancherel_mass_vanishes_proved": False,
            "canonical_high_dimension_syndrome_kl_vanishes_proved": False,
            "canonical_high_dimension_syndrome_survives_proved": False,
            "coherent_multiplicity_signal_absent_proved": False,
            "classical_separation_proved": False,
            "algorithm_claim_allowed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The exact reduction isolates a three-bit measured-label channel, but "
                "its positive-mass asymptotics and any nonclassical value remain open."
            ),
        },
        status=(
            "sign-orbit-syndrome-reduced-asymptotic-channel-open"
            if exact
            else "sign-orbit-syndrome-control-failure"
        ),
        summary=(
            "Reduced all high-dimensional sign-orbit orientation dependence to an "
            "exact three-bit syndrome and split its retained KL contribution."
        ),
        falsifiers_triggered=[
            "Removing trivial/sign labels does not remove the sign action on high-dimensional irreps.",
            "Finite retained sign-orbit bias is not evidence of asymptotic positive mass.",
            "Any orientation-only survivor is a classical measured-label statistic.",
        ],
    )


def write_sign_orbit_syndrome_reduction_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_sign_orbit_syndrome_reduction())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    result = write_sign_orbit_syndrome_reduction_report()
    print(json.dumps(result["headline_metrics"], indent=2, sort_keys=True))
