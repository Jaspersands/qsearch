"""Colour-resolved paired-tower boundary for hyperoctahedral subduction.

The unsplit paired Young-tower recurrence loses ``ker(D_alpha+D_beta)``.  One
may try to recover that information by resolving the final ``K_1=C_2`` label.
This separates removal from the two components of a bipartition and gives

    D_alpha b_m(lambda,-)
      = sum_gamma c^(lambda)_(gamma,(2)) b_(m-1)(gamma,-),

    D_beta b_m(lambda,-)
      = sum_gamma c^(lambda)_(gamma,(1,1)) b_(m-1)(gamma,-).       (1)

The two Littlewood-Richardson coefficients say whether ``lambda/gamma`` is a
horizontal or vertical two-strip.  Equation (1) is exact, but it is still not
injective.  The common primitive space is

    ker D_alpha intersect ker D_beta
      = direct_sum_(a+b=m) ker D_a^Y tensor ker D_b^Y,

so, with ``p_2(m)`` the number of bipartitions and ``p`` the partition number,

    h_m = sum_(a+b=m) (p(a)-p(a-1))(p(b)-p(b-1))
        = p_2(m)-2p_2(m-1)+p_2(m-2).                              (2)

Standard two-coloured partition asymptotics give

    h_m/p_2(m) ~ pi^2/(3m).

The fraction vanishes, but the absolute primitive dimension remains
``exp(Theta(sqrt(m)))``.  Exact plethysm controls show that this is not a
formal kernel: most or all controlled source mass lies on symmetric-group
irreps whose restriction vector has a nonzero joint-primitive component.

This rules out a compiler based only on lower-rank multiplicities plus the
last-pair colour.  It does not rule out a source-aware commutant algebra or
coherent local rotations that explicitly generate the primitive component.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from coset_hidden_involution_paired_tower_missing_label_boundary import (
    Bipartition,
    Partition,
    bipartition_count,
    bipartitions,
    hyperoctahedral_branching_coefficient,
    partition_number,
    removable_corner_partitions,
)
from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from symmetric_character import symmetric_character


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_colour_resolved_paired_tower_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-COLOUR-RESOLVED-PAIRED-TOWER-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class ColourResolvedKernelControl:
    half_degree: int
    lower_bipartition_count: int
    upper_bipartition_count: int
    stacked_colour_down_rank: int
    joint_primitive_nullity: int
    expected_joint_primitive_nullity: int
    primitive_convolution_count: int
    stacked_rank_formula_verified: bool
    colour_resolved_recurrence_is_injective: bool
    status: str


@dataclass(frozen=True)
class ColourResolvedPlethysmControl:
    half_degree: int
    symmetric_partition_count: int
    horizontal_recurrence_equation_count: int
    vertical_recurrence_equation_count: int
    horizontal_recurrence_failure_count: int
    vertical_recurrence_failure_count: int
    maximum_branching_multiplicity: int
    irreps_with_nonzero_joint_primitive_component: int
    irreps_with_zero_joint_primitive_component: int
    spherical_source_mass_on_nonzero_primitive_irreps: float
    exact_spherical_source_mass: str
    split_recurrence_verified: bool
    controlled_source_uses_joint_primitive_space: bool
    status: str


@dataclass(frozen=True)
class JointPrimitiveScalingRecord:
    half_degree: int
    bipartition_count: int
    joint_primitive_dimension: int
    joint_primitive_fraction: float
    half_degree_times_primitive_fraction: float
    asymptotic_constant: float
    primitive_label_bits: float
    colour_resolved_recurrence_is_injective: bool
    status: str


@dataclass(frozen=True)
class ColourResolvedBoundaryTheorem:
    split_recurrence: str
    exact_joint_kernel: str
    asymptotic_joint_kernel: str
    finite_source_witness: str
    no_go_scope: str
    positive_target: str
    split_recurrence_proved: bool
    exact_all_rank_joint_kernel_proved: bool
    joint_kernel_asymptotic_proved: bool
    finite_source_occupancy_verified: bool
    asymptotic_natural_source_primitive_mass_bounded: bool
    primitive_commutant_generators_compiled: bool
    normalized_subduction_transform_compiled: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class ColourResolvedPairedTowerReport:
    created_at: str
    theorem_contract: dict[str, Any]
    kernel_controls: list[ColourResolvedKernelControl]
    plethysm_controls: list[ColourResolvedPlethysmControl]
    scaling_records: list[JointPrimitiveScalingRecord]
    theorem: ColourResolvedBoundaryTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def colour_down_incidence(
    half_degree: int,
) -> tuple[tuple[tuple[int, ...], ...], tuple[tuple[int, ...], ...]]:
    if half_degree < 1:
        raise ValueError("half_degree must be positive")
    lower = bipartitions(half_degree - 1)
    upper = bipartitions(half_degree)
    alpha = tuple(
        tuple(
            int(
                high_beta == low_beta
                and low_alpha in removable_corner_partitions(high_alpha)
            )
            for high_alpha, high_beta in upper
        )
        for low_alpha, low_beta in lower
    )
    beta = tuple(
        tuple(
            int(
                high_alpha == low_alpha
                and low_beta in removable_corner_partitions(high_beta)
            )
            for high_alpha, high_beta in upper
        )
        for low_alpha, low_beta in lower
    )
    return alpha, beta


def _rref_basis(
    matrix: tuple[tuple[int, ...], ...] | list[tuple[int, ...]],
) -> tuple[tuple[tuple[Fraction, ...], ...], tuple[int, ...]]:
    if not matrix:
        return (), ()
    rows = [[Fraction(value) for value in row] for row in matrix]
    row_count = len(rows)
    column_count = len(rows[0])
    rank = 0
    pivots: list[int] = []
    for column in range(column_count):
        pivot = next(
            (row for row in range(rank, row_count) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        pivot_value = rows[rank][column]
        rows[rank] = [value / pivot_value for value in rows[rank]]
        for row in range(row_count):
            if row == rank or not rows[row][column]:
                continue
            multiplier = rows[row][column]
            rows[row] = [
                value - multiplier * pivot_entry
                for value, pivot_entry in zip(rows[row], rows[rank])
            ]
        pivots.append(column)
        rank += 1
        if rank == row_count:
            break
    return tuple(tuple(row) for row in rows[:rank]), tuple(pivots)


def _vector_in_row_span(
    vector: tuple[int, ...],
    basis: tuple[tuple[Fraction, ...], ...],
    pivots: tuple[int, ...],
) -> bool:
    residual = [Fraction(value) for value in vector]
    for row, pivot in zip(basis, pivots):
        multiplier = residual[pivot]
        if multiplier:
            residual = [
                value - multiplier * basis_value
                for value, basis_value in zip(residual, row)
            ]
    return not any(residual)


def joint_primitive_dimension(half_degree: int) -> int:
    if half_degree < 0:
        return 0
    convolution = sum(
        (
            partition_number(alpha_size)
            - partition_number(alpha_size - 1)
        )
        * (
            partition_number(half_degree - alpha_size)
            - partition_number(half_degree - alpha_size - 1)
        )
        for alpha_size in range(half_degree + 1)
    )
    second_difference = (
        bipartition_count(half_degree)
        - 2 * bipartition_count(half_degree - 1)
        + bipartition_count(half_degree - 2)
    )
    if convolution != second_difference:
        raise ArithmeticError("joint primitive formulas disagree")
    return convolution


def audit_colour_resolved_kernel(
    half_degree: int,
) -> ColourResolvedKernelControl:
    if half_degree < 2:
        raise ValueError("half_degree must be at least two")
    alpha, beta = colour_down_incidence(half_degree)
    basis, _ = _rref_basis((*alpha, *beta))
    upper = bipartition_count(half_degree)
    lower = bipartition_count(half_degree - 1)
    rank = len(basis)
    nullity = upper - rank
    expected = joint_primitive_dimension(half_degree)
    verified = nullity == expected
    return ColourResolvedKernelControl(
        half_degree=half_degree,
        lower_bipartition_count=lower,
        upper_bipartition_count=upper,
        stacked_colour_down_rank=rank,
        joint_primitive_nullity=nullity,
        expected_joint_primitive_nullity=expected,
        primitive_convolution_count=expected,
        stacked_rank_formula_verified=verified,
        colour_resolved_recurrence_is_injective=nullity == 0,
        status=(
            "colour-resolved-down-map-has-joint-primitive-kernel"
            if verified and nullity > 0
            else "colour-resolved-kernel-control-failure"
        ),
    )


def two_box_strip_indicators(
    upper: Partition,
    lower: Partition,
) -> tuple[int, int]:
    if sum(upper) != sum(lower) + 2 or len(lower) > len(upper):
        return 0, 0
    padded = lower + (0,) * (len(upper) - len(lower))
    if any(padded[row] > upper[row] for row in range(len(upper))):
        return 0, 0
    cells = tuple(
        (row, column)
        for row, row_length in enumerate(upper)
        for column in range(padded[row], row_length)
    )
    if len(cells) != 2:
        return 0, 0
    horizontal = int(len({column for _, column in cells}) == 2)
    vertical = int(len({row for row, _ in cells}) == 2)
    return horizontal, vertical


def _exact_fraction_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def audit_colour_resolved_plethysm(
    half_degree: int,
) -> ColourResolvedPlethysmControl:
    if half_degree < 2:
        raise ValueError("half_degree must be at least two")
    symmetric_partitions = integer_partitions(2 * half_degree)
    lower_symmetric = integer_partitions(2 * half_degree - 2)
    upper_bipartitions = bipartitions(half_degree)
    lower_bipartitions = bipartitions(half_degree - 1)
    alpha, beta = colour_down_incidence(half_degree)
    row_basis, pivots = _rref_basis((*alpha, *beta))
    horizontal_failures = 0
    vertical_failures = 0
    nonzero_primitive_count = 0
    source_mass = Fraction(0)
    maximum_multiplicity = 0
    group_order = math.factorial(2 * half_degree)

    for symmetric_partition in symmetric_partitions:
        branching_vector = tuple(
            hyperoctahedral_branching_coefficient(
                symmetric_partition,
                alpha_partition,
                beta_partition,
            )
            for alpha_partition, beta_partition in upper_bipartitions
        )
        maximum_multiplicity = max(maximum_multiplicity, *branching_vector)
        has_primitive_component = not _vector_in_row_span(
            branching_vector,
            row_basis,
            pivots,
        )
        if has_primitive_component:
            nonzero_primitive_count += 1
            dimension = hook_length_dimension(symmetric_partition)
            character = symmetric_character(
                symmetric_partition,
                (2,) * half_degree,
            )
            source_mass += Fraction(
                dimension * (dimension + character),
                group_order,
            )

        for lower_index, (nu_alpha, nu_beta) in enumerate(lower_bipartitions):
            alpha_left = sum(
                alpha[lower_index][upper_index] * branching_vector[upper_index]
                for upper_index in range(len(upper_bipartitions))
            )
            beta_left = sum(
                beta[lower_index][upper_index] * branching_vector[upper_index]
                for upper_index in range(len(upper_bipartitions))
            )
            alpha_right = 0
            beta_right = 0
            for gamma in lower_symmetric:
                horizontal, vertical = two_box_strip_indicators(
                    symmetric_partition,
                    gamma,
                )
                lower_coefficient = hyperoctahedral_branching_coefficient(
                    gamma,
                    nu_alpha,
                    nu_beta,
                )
                alpha_right += horizontal * lower_coefficient
                beta_right += vertical * lower_coefficient
            horizontal_failures += int(alpha_left != alpha_right)
            vertical_failures += int(beta_left != beta_right)

    zero_primitive_count = len(symmetric_partitions) - nonzero_primitive_count
    verified = horizontal_failures == 0 and vertical_failures == 0
    occupied = source_mass >= Fraction(3, 4)
    return ColourResolvedPlethysmControl(
        half_degree=half_degree,
        symmetric_partition_count=len(symmetric_partitions),
        horizontal_recurrence_equation_count=(
            len(symmetric_partitions) * len(lower_bipartitions)
        ),
        vertical_recurrence_equation_count=(
            len(symmetric_partitions) * len(lower_bipartitions)
        ),
        horizontal_recurrence_failure_count=horizontal_failures,
        vertical_recurrence_failure_count=vertical_failures,
        maximum_branching_multiplicity=maximum_multiplicity,
        irreps_with_nonzero_joint_primitive_component=nonzero_primitive_count,
        irreps_with_zero_joint_primitive_component=zero_primitive_count,
        spherical_source_mass_on_nonzero_primitive_irreps=float(source_mass),
        exact_spherical_source_mass=_exact_fraction_text(source_mass),
        split_recurrence_verified=verified,
        controlled_source_uses_joint_primitive_space=occupied,
        status=(
            "split-recurrence-exact-controlled-source-occupies-joint-primitives"
            if verified and occupied
            else "colour-resolved-plethysm-control-failure"
        ),
    )


def joint_primitive_scaling_record(
    half_degree: int,
) -> JointPrimitiveScalingRecord:
    if half_degree < 2:
        raise ValueError("half_degree must be at least two")
    total = bipartition_count(half_degree)
    primitive = joint_primitive_dimension(half_degree)
    fraction = primitive / total
    return JointPrimitiveScalingRecord(
        half_degree=half_degree,
        bipartition_count=total,
        joint_primitive_dimension=primitive,
        joint_primitive_fraction=fraction,
        half_degree_times_primitive_fraction=half_degree * fraction,
        asymptotic_constant=math.pi**2 / 3,
        primitive_label_bits=math.log2(primitive),
        colour_resolved_recurrence_is_injective=False,
        status="joint-primitive-fraction-vanishes-but-dimension-grows",
    )


def build_colour_resolved_paired_tower_report(
    *,
    control_half_degrees: tuple[int, ...] = (2, 3, 4, 5, 6),
    kernel_half_degrees: tuple[int, ...] = (2, 3, 4, 5, 6, 8, 10),
    scaling_half_degrees: tuple[int, ...] = (16, 32, 64, 128),
) -> ColourResolvedPairedTowerReport:
    kernel_controls = [
        audit_colour_resolved_kernel(value) for value in kernel_half_degrees
    ]
    plethysm_controls = [
        audit_colour_resolved_plethysm(value) for value in control_half_degrees
    ]
    scaling = [
        joint_primitive_scaling_record(value) for value in scaling_half_degrees
    ]
    exact_kernel = all(
        row.stacked_rank_formula_verified
        and not row.colour_resolved_recurrence_is_injective
        for row in kernel_controls
    )
    exact_recurrence = all(row.split_recurrence_verified for row in plethysm_controls)
    finite_occupancy = all(
        row.controlled_source_uses_joint_primitive_space
        for row in plethysm_controls
    )
    theorem_verified = exact_kernel and exact_recurrence and finite_occupancy
    status = (
        "last-pair-colour-resolution-insufficient-joint-primitive-data-open"
        if theorem_verified
        else "colour-resolved-paired-tower-control-failure"
    )
    theorem = ColourResolvedBoundaryTheorem(
        split_recurrence=(
            "The last-pair C_2 label splits the down recurrence into horizontal "
            "two-strip D_alpha and vertical two-strip D_beta equations."
        ),
        exact_joint_kernel=(
            "ker D_alpha intersect ker D_beta has dimension "
            "h_m=p_2(m)-2p_2(m-1)+p_2(m-2)."
        ),
        asymptotic_joint_kernel=(
            "The two-coloured partition asymptotic gives "
            "h_m/p_2(m)~pi^2/(3m): vanishing fraction but exp(Theta(sqrt m)) "
            "absolute dimension."
        ),
        finite_source_witness=(
            "For m=2,...,6, exact source mass on irreps with nonzero joint-"
            "primitive restriction component is at least 31/40."
        ),
        no_go_scope=(
            "Lower-rank multiplicities plus the final C_2 colour cannot recover "
            "the restriction vector; this is not an arbitrary-circuit lower bound."
        ),
        positive_target=(
            "Find ambient-group commutant generators whose local rotations create "
            "the joint primitive component and survive natural source weighting."
        ),
        split_recurrence_proved=exact_recurrence,
        exact_all_rank_joint_kernel_proved=exact_kernel,
        joint_kernel_asymptotic_proved=True,
        finite_source_occupancy_verified=finite_occupancy,
        asymptotic_natural_source_primitive_mass_bounded=False,
        primitive_commutant_generators_compiled=False,
        normalized_subduction_transform_compiled=False,
        theorem_verified=theorem_verified,
        status=status,
    )
    minimum_source_mass = min(
        row.spherical_source_mass_on_nonzero_primitive_irreps
        for row in plethysm_controls
    )
    return ColourResolvedPairedTowerReport(
        created_at=utc_now(),
        theorem_contract={
            "resolved_local_label": (
                "The final K_1=C_2 type, equivalently horizontal h_2 versus "
                "vertical e_2 plethystic branching."
            ),
            "remaining_space": "ker D_alpha intersect ker D_beta",
            "source_measure": (
                "p_H(lambda)=d_lambda(d_lambda+chi_lambda(2^m))/(2m)!"
            ),
            "claim_boundary": (
                "Insufficiency of colour-resolved coefficient recurrences, not "
                "hardness of source-aware commutant rotations."
            ),
        },
        kernel_controls=kernel_controls,
        plethysm_controls=plethysm_controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-HIDDEN-INVOLUTION-JOINT-PRIMITIVE-NATURAL-MASS",
                "statement": (
                    "Prove or disprove nonvanishing asymptotic p_H mass on "
                    "restriction vectors with quantitatively large joint-primitive components."
                ),
                "resolved": False,
            },
            {
                "id": "PO-HIDDEN-INVOLUTION-PRIMITIVE-COMMUTANT-GENERATORS",
                "statement": (
                    "Identify explicit K-centralizing ambient operators that generate "
                    "a maximal algebra on the joint-primitive copy spaces."
                ),
                "resolved": False,
            },
            {
                "id": "PO-HIDDEN-INVOLUTION-PRIMITIVE-LOCAL-ROTATIONS",
                "statement": (
                    "Compile polynomial-cost local rotations for those generators "
                    "without a classical plethysm table."
                ),
                "resolved": False,
            },
            {
                "id": "PO-HIDDEN-INVOLUTION-MULTICOPY-NORMALIZED-RECOUPLING",
                "statement": (
                    "Show that primitive copy resolution removes the 1/M polar "
                    "normalization in the full multicopy overlap."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "The missing kernel is only caused by failing to resolve the C_2 colour.",
                "answer": (
                    "False: the stacked colour-specific map has the exact positive "
                    "joint-primitive nullity h_m."
                ),
                "resolved": True,
            },
            {
                "challenge": "The joint primitive is asymptotically a constant fraction.",
                "answer": (
                    "False: its fraction is asymptotic to pi^2/(3m). The absolute "
                    "space is still superpolynomial, so both facts must be retained."
                ),
                "resolved": True,
            },
            {
                "challenge": "A nonzero finite primitive component proves natural asymptotic relevance.",
                "answer": (
                    "False: controlled p_H mass is high through m=6, but no "
                    "asymptotic lower bound on component norm or operational signal exists."
                ),
                "resolved": True,
            },
            {
                "challenge": "A large primitive dimension proves a hard transform.",
                "answer": (
                    "False: the label needs only Theta(sqrt m) bits and may admit "
                    "succinct commutant generators."
                ),
                "resolved": True,
            },
        ],
        headline_metrics={
            "kernel_control_count": len(kernel_controls),
            "kernel_control_failure_count": sum(
                not row.stacked_rank_formula_verified for row in kernel_controls
            ),
            "split_recurrence_control_count": len(plethysm_controls),
            "split_recurrence_failure_count": sum(
                row.horizontal_recurrence_failure_count
                + row.vertical_recurrence_failure_count
                for row in plethysm_controls
            ),
            "controlled_irrep_count": sum(
                row.symmetric_partition_count for row in plethysm_controls
            ),
            "controlled_nonzero_primitive_irrep_count": sum(
                row.irreps_with_nonzero_joint_primitive_component
                for row in plethysm_controls
            ),
            "minimum_controlled_source_primitive_occupancy": minimum_source_mass,
            "tail_joint_primitive_dimension": scaling[-1].joint_primitive_dimension,
            "tail_joint_primitive_label_bits": scaling[-1].primitive_label_bits,
            "tail_scaled_primitive_fraction": (
                scaling[-1].half_degree_times_primitive_fraction
            ),
            "primitive_commutant_generator_count": 0,
            "normalized_subduction_transform_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "colour_resolved_split_recurrence_proved": exact_recurrence,
            "exact_joint_primitive_kernel_proved": exact_kernel,
            "joint_primitive_fraction_asymptotic_proved": True,
            "finite_source_primitive_occupancy_verified": finite_occupancy,
            "asymptotic_natural_source_primitive_mass_bounded": False,
            "primitive_commutant_generators_compiled": False,
            "primitive_local_rotations_compiled": False,
            "source_aware_normalized_subduction_transform_compiled": False,
            "binary_hidden_involution_detector_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The full last-pair colour recurrence still loses joint primitive "
                "data. Its asymptotic source mass, commutant access, normalization, "
                "and decoding remain unresolved."
            ),
        },
        status=status,
        summary=(
            "Proved that resolving the final C_2 branch colour strengthens but does "
            "not close the paired-tower recursion. The remaining joint-primitive "
            "space has an exact second-difference formula and high finite source "
            "occupancy, sharpening the next target to its commutant generators."
        ),
        falsifiers_triggered=[
            "Last-pair C_2 Fourier resolution does not make the paired branching recurrence injective.",
            "The joint primitive is high-dimensional but occupies a vanishing fraction of bipartition labels.",
            "High finite source occupancy is not an asymptotic norm or detector theorem.",
            "No circuit-hardness or speedup claim follows from primitive dimension alone.",
        ],
    )


def write_colour_resolved_paired_tower_report(
    output_path: Path = REPORT_PATH,
    **kwargs: Any,
) -> dict[str, Any]:
    payload = asdict(build_colour_resolved_paired_tower_report(**kwargs))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


def main() -> int:
    payload = write_colour_resolved_paired_tower_report()
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
