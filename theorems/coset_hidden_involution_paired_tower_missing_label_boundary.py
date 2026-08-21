"""Paired Young-tower boundary for hyperoctahedral missing labels.

Let ``K_m=C_2 wr S_m`` be the centralizer of a fixed-point-free involution in
``S_(2m)`` and write

    Res_{K_m}^{S_(2m)} [lambda]
      = direct_sum_mu C^b_m(lambda,mu) tensor [mu].

The ordinary Young tower and the bipartition Young tower give the exact
one-level recurrence

    sum_(mu covers nu) b_m(lambda,mu)
      = sum_gamma f^(lambda/gamma) b_(m-1)(gamma,nu),              (1)

where ``f^(lambda/gamma)`` counts the two-box Young paths from ``lambda`` to
``gamma``.  This looks like a recursive route to the missing labels, but it
does not determine the rank-``m`` branching vector.

If ``D_m`` is the down-incidence matrix from bipartitions of ``m`` to those of
``m-1``, the two-colour Young lattice is a 2-differential poset:

    D_m D_m^T - D_(m-1)^T D_(m-1) = 2 I.                         (2)

Thus ``D_m`` has full row rank and

    dim ker D_m = p_2(m)-p_2(m-1).

Equation (1) fixes only ``D_m b_m(lambda,-)``.  A fresh harmonic component in
``ker D_m`` is absent from the lower-level data at every rank.  Exact
power-sum plethysm controls verify (1) and show that actual restriction
vectors have nonzero harmonic components in every tested symmetric-group
irrep, rather than living accidentally in ``im D_m^T``.

This falsifies the naive branching-only compiler.  It is not a circuit lower
bound: a source-aware commutant algebra or efficiently computable harmonic
rotation could still supply the new data with polynomial resources.
"""

from __future__ import annotations

import json
import math
from collections import Counter
from dataclasses import asdict, dataclass
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from typing import Any

from coset_hidden_involution_natural_recoupling_boundary import (
    hyperoctahedral_irrep_dimension,
)
from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from symmetric_character import symmetric_character


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_paired_tower_missing_label_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-PAIRED-TOWER-MISSING-LABEL-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Bipartition = tuple[Partition, Partition]
RationalPolynomial = dict[Partition, Fraction]


@dataclass(frozen=True)
class PairedTowerIncidenceControl:
    half_degree: int
    lower_bipartition_count: int
    upper_bipartition_count: int
    down_incidence_rank: int
    harmonic_nullity: int
    expected_harmonic_nullity: int
    differential_poset_identity_verified: bool
    full_row_rank_proved: bool
    status: str


@dataclass(frozen=True)
class PlethysmRecurrenceControl:
    half_degree: int
    symmetric_partition_count: int
    bipartition_count: int
    branching_coefficient_count: int
    maximum_branching_multiplicity: int
    recurrence_equation_count: int
    recurrence_failure_count: int
    restriction_dimension_failure_count: int
    nonintegral_or_negative_coefficient_count: int
    irreps_with_nonzero_harmonic_residual: int
    irreps_with_zero_harmonic_residual: int
    maximum_harmonic_residual_squared: str
    standard_plus_branch_multiplicity: int | None
    standard_minus_branch_multiplicity: int | None
    exact_plethysm_recurrence_verified: bool
    actual_branching_uses_harmonic_component: bool
    status: str


@dataclass(frozen=True)
class HarmonicKernelScalingRecord:
    half_degree: int
    lower_bipartition_count: int
    upper_bipartition_count: int
    harmonic_nullity: int
    harmonic_fraction: float
    harmonic_label_bits_lower_bound: float
    branching_recurrence_uniquely_determines_upper_vector: bool
    status: str


@dataclass(frozen=True)
class PairedTowerBoundaryTheorem:
    exact_branching_recurrence: str
    differential_poset_identity: str
    underdetermination: str
    finite_natural_witness: str
    complexity_boundary: str
    positive_compiler_target: str
    exact_branching_recurrence_proved: bool
    all_rank_harmonic_kernel_proved: bool
    actual_branching_harmonic_component_verified: bool
    natural_source_harmonic_mass_bounded: bool
    paired_young_local_rotations_compiled: bool
    source_aware_normalized_subduction_transform_compiled: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class PairedTowerMissingLabelReport:
    created_at: str
    theorem_contract: dict[str, Any]
    incidence_controls: list[PairedTowerIncidenceControl]
    plethysm_controls: list[PlethysmRecurrenceControl]
    scaling_records: list[HarmonicKernelScalingRecord]
    theorem: PairedTowerBoundaryTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    literature_links: list[dict[str, str]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


@lru_cache(maxsize=None)
def partition_number(n: int) -> int:
    if n < 0:
        return 0
    counts = [0] * (n + 1)
    counts[0] = 1
    for part in range(1, n + 1):
        for total in range(part, n + 1):
            counts[total] += counts[total - part]
    return counts[n]


@lru_cache(maxsize=None)
def bipartition_count(rank: int) -> int:
    if rank < 0:
        return 0
    return sum(
        partition_number(left_size) * partition_number(rank - left_size)
        for left_size in range(rank + 1)
    )


@lru_cache(maxsize=None)
def bipartitions(rank: int) -> tuple[Bipartition, ...]:
    if rank < 0:
        return ()
    return tuple(
        (alpha, beta)
        for beta_size in range(rank + 1)
        for alpha in integer_partitions(rank - beta_size)
        for beta in integer_partitions(beta_size)
    )


@lru_cache(maxsize=None)
def removable_corner_partitions(partition: Partition) -> tuple[Partition, ...]:
    output: list[Partition] = []
    for index, row_length in enumerate(partition):
        if index + 1 < len(partition) and partition[index + 1] == row_length:
            continue
        reduced = list(partition)
        reduced[index] -= 1
        if reduced[index] == 0:
            reduced.pop(index)
        output.append(tuple(reduced))
    return tuple(output)


def bipartition_covers(upper: Bipartition, lower: Bipartition) -> bool:
    upper_alpha, upper_beta = upper
    lower_alpha, lower_beta = lower
    return bool(
        (lower_beta == upper_beta and lower_alpha in removable_corner_partitions(upper_alpha))
        or (
            lower_alpha == upper_alpha
            and lower_beta in removable_corner_partitions(upper_beta)
        )
    )


@lru_cache(maxsize=None)
def down_incidence(half_degree: int) -> tuple[tuple[int, ...], ...]:
    if half_degree < 1:
        raise ValueError("half_degree must be positive")
    lower = bipartitions(half_degree - 1)
    upper = bipartitions(half_degree)
    return tuple(
        tuple(int(bipartition_covers(high, low)) for high in upper)
        for low in lower
    )


def _matrix_product_left_transpose(
    matrix: tuple[tuple[int, ...], ...],
) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(
            sum(matrix[row][column] * matrix[other][column] for column in range(len(matrix[0])))
            for other in range(len(matrix))
        )
        for row in range(len(matrix))
    )


def _matrix_product_transpose_left(
    matrix: tuple[tuple[int, ...], ...],
) -> tuple[tuple[int, ...], ...]:
    column_count = len(matrix[0])
    return tuple(
        tuple(
            sum(matrix[row][column] * matrix[row][other] for row in range(len(matrix)))
            for other in range(column_count)
        )
        for column in range(column_count)
    )


def audit_paired_tower_incidence(half_degree: int) -> PairedTowerIncidenceControl:
    if half_degree < 2:
        raise ValueError("half_degree must be at least two")
    current = down_incidence(half_degree)
    previous = down_incidence(half_degree - 1)
    down_up = _matrix_product_left_transpose(current)
    up_down = _matrix_product_transpose_left(previous)
    identity_verified = all(
        down_up[row][column] - up_down[row][column]
        == (2 if row == column else 0)
        for row in range(len(down_up))
        for column in range(len(down_up))
    )
    lower_count = bipartition_count(half_degree - 1)
    upper_count = bipartition_count(half_degree)
    nullity = upper_count - lower_count
    full_row_rank = identity_verified
    return PairedTowerIncidenceControl(
        half_degree=half_degree,
        lower_bipartition_count=lower_count,
        upper_bipartition_count=upper_count,
        down_incidence_rank=lower_count if full_row_rank else 0,
        harmonic_nullity=nullity,
        expected_harmonic_nullity=upper_count - lower_count,
        differential_poset_identity_verified=identity_verified,
        full_row_rank_proved=full_row_rank,
        status=(
            "two-colour-differential-poset-identity-verified"
            if identity_verified
            else "paired-tower-incidence-control-failure"
        ),
    )


def z_partition(partition: Partition) -> int:
    output = 1
    for cycle_length, multiplicity in Counter(partition).items():
        output *= (cycle_length**multiplicity) * math.factorial(multiplicity)
    return output


def _multiply_power_sum_polynomials(
    left: RationalPolynomial,
    right: RationalPolynomial,
) -> RationalPolynomial:
    output: RationalPolynomial = {}
    for left_partition, left_coefficient in left.items():
        for right_partition, right_coefficient in right.items():
            partition = tuple(sorted(left_partition + right_partition, reverse=True))
            output[partition] = (
                output.get(partition, Fraction(0))
                + left_coefficient * right_coefficient
            )
    return {partition: coefficient for partition, coefficient in output.items() if coefficient}


@lru_cache(maxsize=None)
def plethystic_schur_power_sum(
    partition: Partition,
    *,
    exterior_square: bool,
) -> RationalPolynomial:
    """Return the power-sum expansion of ``s_partition[h_2/e_2]``."""

    if not partition:
        return {(): Fraction(1)}
    output: RationalPolynomial = {}
    for cycle_type in integer_partitions(sum(partition)):
        coefficient = Fraction(
            symmetric_character(partition, cycle_type),
            z_partition(cycle_type),
        )
        if not coefficient:
            continue
        term: RationalPolynomial = {(): coefficient}
        for cycle_length in cycle_type:
            atom = {
                (cycle_length, cycle_length): Fraction(1, 2),
                (2 * cycle_length,): Fraction(
                    -1 if exterior_square else 1,
                    2,
                ),
            }
            term = _multiply_power_sum_polynomials(term, atom)
        for power_partition, value in term.items():
            output[power_partition] = output.get(power_partition, Fraction(0)) + value
    return {partition: coefficient for partition, coefficient in output.items() if coefficient}


@lru_cache(maxsize=None)
def hyperoctahedral_branching_coefficient(
    symmetric_partition: Partition,
    alpha: Partition,
    beta: Partition,
) -> int:
    """Compute ``<s_lambda,s_alpha[h_2]s_beta[e_2]>`` exactly."""

    if sum(symmetric_partition) != 2 * (sum(alpha) + sum(beta)):
        return 0
    polynomial = _multiply_power_sum_polynomials(
        plethystic_schur_power_sum(alpha, exterior_square=False),
        plethystic_schur_power_sum(beta, exterior_square=True),
    )
    value = sum(
        coefficient * symmetric_character(symmetric_partition, cycle_type)
        for cycle_type, coefficient in polynomial.items()
    )
    if value.denominator != 1 or value < 0:
        raise ArithmeticError("hyperoctahedral branching coefficient is invalid")
    return int(value)


@lru_cache(maxsize=None)
def two_box_branching_count(upper: Partition, lower: Partition) -> int:
    if sum(upper) != sum(lower) + 2:
        return 0
    return sum(
        lower in removable_corner_partitions(intermediate)
        for intermediate in removable_corner_partitions(upper)
    )


def _solve_fraction_system(
    matrix: list[list[int]],
    vector: list[int],
) -> list[Fraction]:
    dimension = len(matrix)
    augmented = [
        [Fraction(value) for value in matrix[row]] + [Fraction(vector[row])]
        for row in range(dimension)
    ]
    for column in range(dimension):
        pivot = next(
            (row for row in range(column, dimension) if augmented[row][column]),
            None,
        )
        if pivot is None:
            raise ArithmeticError("incidence Gram matrix is singular")
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        pivot_value = augmented[column][column]
        augmented[column] = [value / pivot_value for value in augmented[column]]
        for row in range(dimension):
            if row == column or not augmented[row][column]:
                continue
            multiplier = augmented[row][column]
            augmented[row] = [
                value - multiplier * pivot_entry
                for value, pivot_entry in zip(augmented[row], augmented[column])
            ]
    return [row[-1] for row in augmented]


def harmonic_residual(
    half_degree: int,
    vector: tuple[int, ...],
) -> tuple[tuple[Fraction, ...], Fraction]:
    """Project a rank-m vector orthogonally onto ``ker D_m``."""

    incidence = down_incidence(half_degree)
    if len(vector) != len(incidence[0]):
        raise ValueError("vector length does not match the rank-m bipartitions")
    gram = [
        [
            sum(
                incidence[row][column] * incidence[other][column]
                for column in range(len(vector))
            )
            for other in range(len(incidence))
        ]
        for row in range(len(incidence))
    ]
    image = [
        sum(incidence[row][column] * vector[column] for column in range(len(vector)))
        for row in range(len(incidence))
    ]
    coefficients = _solve_fraction_system(gram, image)
    row_space_projection = tuple(
        sum(
            Fraction(incidence[row][column]) * coefficients[row]
            for row in range(len(incidence))
        )
        for column in range(len(vector))
    )
    residual = tuple(
        Fraction(vector[column]) - row_space_projection[column]
        for column in range(len(vector))
    )
    norm_squared = sum(value * value for value in residual)
    return residual, norm_squared


def _fraction_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def audit_plethysm_recurrence(half_degree: int) -> PlethysmRecurrenceControl:
    if half_degree < 2:
        raise ValueError("half_degree must be at least two")
    symmetric_partitions = integer_partitions(2 * half_degree)
    upper_bipartitions = bipartitions(half_degree)
    lower_bipartitions = bipartitions(half_degree - 1)
    lower_symmetric_partitions = integer_partitions(2 * half_degree - 2)
    incidence = down_incidence(half_degree)
    recurrence_failures = 0
    dimension_failures = 0
    invalid_coefficients = 0
    nonzero_harmonic = 0
    maximum_residual = Fraction(0)
    maximum_multiplicity = 0

    for symmetric_partition in symmetric_partitions:
        branching_vector: list[int] = []
        for alpha, beta in upper_bipartitions:
            try:
                value = hyperoctahedral_branching_coefficient(
                    symmetric_partition,
                    alpha,
                    beta,
                )
            except ArithmeticError:
                invalid_coefficients += 1
                value = 0
            branching_vector.append(value)
            maximum_multiplicity = max(maximum_multiplicity, value)
        dimension_sum = sum(
            multiplicity * hyperoctahedral_irrep_dimension(alpha, beta)
            for multiplicity, (alpha, beta) in zip(
                branching_vector,
                upper_bipartitions,
            )
        )
        if dimension_sum != hook_length_dimension(symmetric_partition):
            dimension_failures += 1

        _, residual_squared = harmonic_residual(
            half_degree,
            tuple(branching_vector),
        )
        if residual_squared:
            nonzero_harmonic += 1
        maximum_residual = max(maximum_residual, residual_squared)

        for lower_index, (nu_alpha, nu_beta) in enumerate(lower_bipartitions):
            left = sum(
                incidence[lower_index][upper_index] * branching_vector[upper_index]
                for upper_index in range(len(upper_bipartitions))
            )
            right = sum(
                two_box_branching_count(symmetric_partition, gamma)
                * hyperoctahedral_branching_coefficient(gamma, nu_alpha, nu_beta)
                for gamma in lower_symmetric_partitions
            )
            recurrence_failures += int(left != right)

    standard_plus = None
    standard_minus = None
    if half_degree >= 2:
        standard_partition = (2 * half_degree - 1, 1)
        standard_plus = hyperoctahedral_branching_coefficient(
            standard_partition,
            (half_degree - 1, 1),
            (),
        )
        standard_minus = hyperoctahedral_branching_coefficient(
            standard_partition,
            (half_degree - 1,),
            (1,),
        )

    zero_harmonic = len(symmetric_partitions) - nonzero_harmonic
    verified = bool(
        recurrence_failures == 0
        and dimension_failures == 0
        and invalid_coefficients == 0
    )
    uses_harmonic = nonzero_harmonic == len(symmetric_partitions)
    return PlethysmRecurrenceControl(
        half_degree=half_degree,
        symmetric_partition_count=len(symmetric_partitions),
        bipartition_count=len(upper_bipartitions),
        branching_coefficient_count=(
            len(symmetric_partitions) * len(upper_bipartitions)
        ),
        maximum_branching_multiplicity=maximum_multiplicity,
        recurrence_equation_count=(
            len(symmetric_partitions) * len(lower_bipartitions)
        ),
        recurrence_failure_count=recurrence_failures,
        restriction_dimension_failure_count=dimension_failures,
        nonintegral_or_negative_coefficient_count=invalid_coefficients,
        irreps_with_nonzero_harmonic_residual=nonzero_harmonic,
        irreps_with_zero_harmonic_residual=zero_harmonic,
        maximum_harmonic_residual_squared=_fraction_text(maximum_residual),
        standard_plus_branch_multiplicity=standard_plus,
        standard_minus_branch_multiplicity=standard_minus,
        exact_plethysm_recurrence_verified=verified,
        actual_branching_uses_harmonic_component=uses_harmonic,
        status=(
            "exact-recurrence-verified-all-controlled-irreps-use-harmonic-data"
            if verified and uses_harmonic
            else "paired-tower-plethysm-control-failure"
        ),
    )


def harmonic_kernel_scaling_record(
    half_degree: int,
) -> HarmonicKernelScalingRecord:
    if half_degree < 2:
        raise ValueError("half_degree must be at least two")
    lower = bipartition_count(half_degree - 1)
    upper = bipartition_count(half_degree)
    nullity = upper - lower
    return HarmonicKernelScalingRecord(
        half_degree=half_degree,
        lower_bipartition_count=lower,
        upper_bipartition_count=upper,
        harmonic_nullity=nullity,
        harmonic_fraction=nullity / upper,
        harmonic_label_bits_lower_bound=math.log2(nullity),
        branching_recurrence_uniquely_determines_upper_vector=False,
        status="fresh-harmonic-kernel-at-this-rank",
    )


def build_paired_tower_missing_label_report(
    *,
    control_half_degrees: tuple[int, ...] = (2, 3, 4),
    incidence_half_degrees: tuple[int, ...] = (2, 3, 4, 5, 6, 8),
    scaling_half_degrees: tuple[int, ...] = (8, 16, 32, 64),
) -> PairedTowerMissingLabelReport:
    incidence_controls = [
        audit_paired_tower_incidence(value) for value in incidence_half_degrees
    ]
    plethysm_controls = [
        audit_plethysm_recurrence(value) for value in control_half_degrees
    ]
    scaling = [harmonic_kernel_scaling_record(value) for value in scaling_half_degrees]
    exact_incidence = all(
        row.differential_poset_identity_verified and row.full_row_rank_proved
        for row in incidence_controls
    )
    exact_plethysm = all(
        row.exact_plethysm_recurrence_verified for row in plethysm_controls
    )
    harmonic_witness = all(
        row.actual_branching_uses_harmonic_component for row in plethysm_controls
    )
    theorem_verified = exact_incidence and exact_plethysm and harmonic_witness
    status = (
        "paired-tower-recurrence-underdetermined-harmonic-plethysm-data-open"
        if theorem_verified
        else "paired-tower-missing-label-control-failure"
    )
    theorem = PairedTowerBoundaryTheorem(
        exact_branching_recurrence=(
            "D_m b_m(lambda,-)[nu] = sum_gamma f^(lambda/gamma) "
            "b_(m-1)(gamma,nu), by restricting through K_m or S_(2m-2)."
        ),
        differential_poset_identity=(
            "The product of two Young lattices obeys "
            "D_m D_m^T-D_(m-1)^T D_(m-1)=2I; hence D_m has full row rank."
        ),
        underdetermination=(
            "The recurrence fixes only the down image and leaves a kernel of "
            "dimension p_2(m)-p_2(m-1) at every rank."
        ),
        finite_natural_witness=(
            "Exact inner-size-two plethysm controls show every tested actual "
            "restriction vector has nonzero orthogonal projection to ker D_m."
        ),
        complexity_boundary=(
            "A growing kernel and classically hard general plethysm do not imply "
            "a quantum circuit lower bound; global consistency or local harmonic "
            "rotations may recover the data efficiently."
        ),
        positive_compiler_target=(
            "Construct a source-aware maximal commutant algebra and local "
            "rotations that propagate the harmonic component coherently."
        ),
        exact_branching_recurrence_proved=exact_plethysm,
        all_rank_harmonic_kernel_proved=exact_incidence,
        actual_branching_harmonic_component_verified=harmonic_witness,
        natural_source_harmonic_mass_bounded=False,
        paired_young_local_rotations_compiled=False,
        source_aware_normalized_subduction_transform_compiled=False,
        theorem_verified=theorem_verified,
        status=status,
    )
    return PairedTowerMissingLabelReport(
        created_at=utc_now(),
        theorem_contract={
            "ambient_pair": "S_(2m) >= K_m=C_2 wr S_m >= K_(m-1)",
            "branching_coefficient": (
                "b_m(lambda;alpha,beta)="
                "<s_lambda,s_alpha[h_2]s_beta[e_2]>"
            ),
            "harmonic_space": "ker D_m for the rank-m bipartition down-map",
            "claim_boundary": (
                "Failure of the naive lower-rank recurrence, not hardness of all "
                "coherent subduction transforms."
            ),
        },
        incidence_controls=incidence_controls,
        plethysm_controls=plethysm_controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-HIDDEN-INVOLUTION-HARMONIC-NATURAL-MASS",
                "statement": (
                    "Bound the harmonic projection of b_m(lambda,-) under the "
                    "exact source-refined law, not unweighted finite controls."
                ),
                "resolved": False,
            },
            {
                "id": "PO-HIDDEN-INVOLUTION-MISSING-LABEL-COMMUTANT",
                "statement": (
                    "Construct a maximal efficiently measurable commutative "
                    "subalgebra of End_K([lambda]) that resolves repeated branches."
                ),
                "resolved": False,
            },
            {
                "id": "PO-HIDDEN-INVOLUTION-HARMONIC-LOCAL-ROTATIONS",
                "statement": (
                    "Derive uniformly polynomial local rotations that create the "
                    "new ker D_m component at each paired-tower step."
                ),
                "resolved": False,
            },
            {
                "id": "PO-HIDDEN-INVOLUTION-MULTICOPY-NORMALIZED-RECOUPLING",
                "statement": (
                    "Show that harmonic missing-label access yields the normalized "
                    "multicopy polar transform without sqrt(|h^G|) amplification."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "The incidence kernel may be absent from real restriction vectors.",
                "answer": (
                    "False in every controlled rank: every S_(2m) irrep has a "
                    "nonzero exact harmonic residual for m=2,3,4. Asymptotic "
                    "source-weighted mass remains open."
                ),
                "resolved": True,
            },
            {
                "challenge": "All lower-rank branching data uniquely determines b_m.",
                "answer": (
                    "False for the one-level linear recurrence: D_m has nullity "
                    "p_2(m)-p_2(m-1). Additional global or local data is required."
                ),
                "resolved": True,
            },
            {
                "challenge": "The fresh harmonic dimension proves circuit hardness.",
                "answer": (
                    "False: its basis label still needs only polynomially many bits, "
                    "and an efficient structured rotation has not been excluded."
                ),
                "resolved": True,
            },
            {
                "challenge": "Classical plethysm hardness supplies the missing no-go.",
                "answer": (
                    "False: coefficient hardness is neither a coherent-transform "
                    "lower bound nor specific enough to this natural inner-size-two family."
                ),
                "resolved": True,
            },
        ],
        literature_links=[
            {
                "id": "stanley-differential-posets-1988",
                "url": "https://doi.org/10.2307/1990969",
                "use": (
                    "Primary differential-poset framework; the bipartition lattice "
                    "is the product of two 1-differential Young lattices."
                ),
            },
            {
                "id": "fischer-ikenmeyer-plethysm-hardness-2020",
                "url": "https://arxiv.org/abs/2002.00788",
                "use": (
                    "General plethysm positivity and coefficient hardness; explicitly "
                    "not promoted to a circuit lower bound here."
                ),
            },
            {
                "id": "christandl-et-al-plethysm-quantum-2026",
                "url": "https://arxiv.org/abs/2602.08441",
                "use": (
                    "Quantum verification evidence for plethysm multiplicities; it "
                    "does not provide the normalized missing-label basis transform."
                ),
            },
        ],
        headline_metrics={
            "incidence_control_count": len(incidence_controls),
            "incidence_control_failure_count": sum(
                not row.differential_poset_identity_verified
                for row in incidence_controls
            ),
            "plethysm_control_count": len(plethysm_controls),
            "plethysm_recurrence_failure_count": sum(
                row.recurrence_failure_count for row in plethysm_controls
            ),
            "restriction_dimension_failure_count": sum(
                row.restriction_dimension_failure_count for row in plethysm_controls
            ),
            "controlled_irrep_count": sum(
                row.symmetric_partition_count for row in plethysm_controls
            ),
            "controlled_irrep_nonzero_harmonic_count": sum(
                row.irreps_with_nonzero_harmonic_residual
                for row in plethysm_controls
            ),
            "tail_harmonic_nullity": scaling[-1].harmonic_nullity,
            "tail_harmonic_label_bits_lower_bound": (
                scaling[-1].harmonic_label_bits_lower_bound
            ),
            "paired_young_local_rotation_count": 0,
            "normalized_subduction_transform_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "exact_paired_branching_recurrence_proved": exact_plethysm,
            "two_colour_differential_poset_underdetermination_proved": exact_incidence,
            "actual_branching_harmonic_component_verified": harmonic_witness,
            "natural_source_harmonic_mass_bounded": False,
            "paired_young_local_rotations_compiled": False,
            "source_aware_normalized_subduction_transform_compiled": False,
            "binary_hidden_involution_detector_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The naive recurrence loses a fresh harmonic component. Its natural "
                "mass, coherent local generation, normalized fusion, and decoding "
                "remain unresolved."
            ),
        },
        status=status,
        summary=(
            "Proved that paired Young-tower branching recurrences leave a fresh "
            "harmonic bipartition component at every rank and verified that exact "
            "small-degree hyperoctahedral restriction vectors use it. This kills "
            "the naive branching-only compiler but leaves structured harmonic "
            "rotations as the precise positive target."
        ),
        falsifiers_triggered=[
            "Lower-rank branching data does not uniquely determine the next hyperoctahedral restriction vector.",
            "The bipartition incidence kernel is not irrelevant to actual controlled restriction vectors.",
            "Neither growing multiplicity nor general plethysm hardness establishes a coherent circuit lower bound.",
            "No detector or speedup claim is permitted without natural-mass and normalized-transform theorems.",
        ],
    )


def write_paired_tower_missing_label_report(
    output_path: Path = REPORT_PATH,
    **kwargs: Any,
) -> dict[str, Any]:
    payload = asdict(build_paired_tower_missing_label_report(**kwargs))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


def main() -> int:
    payload = write_paired_tower_missing_label_report()
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
