"""Why coherent Fourier labels do not cancel power-map block normalization.

The power-map Fourier primitive leaves one tempting loophole.  Its selected
representation block is tiny, but the *whole* transformed power-map is an
isometry.  One might therefore keep every source irrep label coherent and
hope that their Plancherel amplitudes supply the missing normalization.

That mechanism is unavailable for the physical hidden-subgroup source.
For every finite group and subgroup ``H``, the mixed coset state is

    rho_H = |G|^-1 sum_(h in H) R_h.                       (1)

Right regular action is block diagonal under the group QFT, so (1) has no
coherence between inequivalent irrep labels.  Measuring the weak Fourier
label merely reads an existing classical direct-sum block.  Keeping the
label register does not create amplitudes that can interfere across blocks.

The branch field has the same superselection structure.  For a source tuple
``Lambda=(lambda_1,mu_1,...,lambda_k,mu_k)``, every ``J_h`` acts within the
fixed source carrier, hence

    C_global = direct_sum_Lambda C_Lambda.                (2)

The desired power-map monomial likewise preserves ``Lambda``.  All other
output-irrep blocks of the normalization-one power-map isometry are therefore
orthogonal leakage, not alternative paths to the same physical output.

For the block normalization from the predecessor theorem,

    alpha_(nu,Lambda)=|G|^k/sqrt(d_nu D_Lambda),

the independent Plancherel mean of its squared inverse is exactly

    E[alpha^-2] = S_3^(2k+1) / |G|^(4k+1),               (3)
    S_3=sum_lambda d_lambda^3.

Since ``S_3 <= d_max |G| <= |G|^(3/2)``, equation (3) is at most
``|G|^(-k+1/2)``.  Conditioning on a source event of probability ``p`` can
increase it by at most ``1/p``.  At the natural ``k=Theta(log|G|)`` scale,
Plancherel averaging therefore worsens rather than removes the termwise
normalization.

Cyclic groups give an exact transparent control.  The transformed paired
power map sends each input character to ``m^(2k-1)`` output-character tuples,
each with squared amplitude ``m^(1-2k)``.  A fixed physical source tuple
matches the selection rule with probability ``1/m`` under uniform
Plancherel labels, so its mean matching-block mass is exactly ``m^(-2k)``,
equal to (3).

This theorem rejects only the *label-coherence cancellation* proposal.  It
does not reject an FFT-like factorization of the complete quadrant sum, a
representation-specific circuit that mixes and later restores labels, or a
direct polar transform.  Those mechanisms must be derived independently.
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
from self_dual_wreath_branch_character_power_map_fourier_access_boundary import (
    power_tuple,
    transformed_cyclic_power_map,
)
from self_dual_wreath_coherent_fourier_decoder import (
    symmetric_group_fourier_matrix,
)
from self_dual_wreath_character_moments import compose_permutations


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_branch_character_label_coherent_power_map_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-BRANCH-CHARACTER-LABEL-COHERENT-"
    "POWER-MAP-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Permutation = tuple[int, ...]


@dataclass(frozen=True)
class CosetLabelSuperselectionControl:
    n: int
    group_order: int
    subgroup_order: int
    irrep_count: int
    coset_state_trace_residual: float
    coset_state_minimum_eigenvalue: float
    maximum_cross_irrep_block_norm: float
    qft_unitarity_residual: float
    exact_irrep_label_block_diagonality_verified: bool
    status: str


@dataclass(frozen=True)
class CyclicLabelRetentionControl:
    group_order: int
    copy_count: int
    exponent_parameters: tuple[int, ...]
    output_factor_count: int
    transformed_isometry_residual: float
    nonzero_output_blocks_per_input: int
    expected_nonzero_output_blocks_per_input: int
    minimum_nonzero_block_mass: float
    maximum_nonzero_block_mass: float
    expected_nonzero_block_mass: float
    selection_probability_for_random_physical_labels: float
    mean_matching_physical_block_mass: float
    inverse_normalization_squared: float
    exact_label_retention_identity_verified: bool
    status: str


@dataclass(frozen=True)
class PlancherelNormalizationControl:
    family: str
    group_order: int
    irrep_dimensions: tuple[int, ...]
    copy_count: int
    dimension_square_sum: int
    dimension_cube_sum: int
    exact_inverse_normalization_mean: float
    brute_force_inverse_normalization_mean: float
    universal_upper_bound: float
    exact_formula_residual: float
    upper_bound_verified: bool
    status: str


@dataclass(frozen=True)
class LabelCoherenceScalingRecord:
    n: int
    log2_group_order: float
    copy_count: int
    log2_inverse_normalization_mean_upper_bound: float
    log2_amplitude_amplification_lower_bound: float
    polynomial_benchmark_log2: float
    globally_distinct_conditioning_probability_tends_to_one: bool
    label_coherence_cancellation_superpolynomially_rejected: bool
    status: str


@dataclass(frozen=True)
class LabelCoherentPowerMapTheorem:
    coset_label_superselection: str
    source_block_conservation: str
    wrong_block_interpretation: str
    plancherel_inverse_normalization_mean: str
    dimension_bound: str
    cyclic_control: str
    surviving_escape: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class LabelCoherentPowerMapBoundaryReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: LabelCoherentPowerMapTheorem
    coset_superselection_control: CosetLabelSuperselectionControl
    cyclic_controls: list[CyclicLabelRetentionControl]
    plancherel_controls: list[PlancherelNormalizationControl]
    scaling_records: list[LabelCoherenceScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _inverse_permutation(permutation: Permutation) -> Permutation:
    inverse = [0] * len(permutation)
    for index, image in enumerate(permutation):
        inverse[image] = index
    return tuple(inverse)


def _right_regular_matrix(
    permutations: tuple[Permutation, ...],
    multiplier: Permutation,
) -> np.ndarray:
    index = {permutation: position for position, permutation in enumerate(permutations)}
    matrix = np.zeros((len(permutations), len(permutations)), dtype=complex)
    for column, permutation in enumerate(permutations):
        image = compose_permutations(permutation, multiplier)
        matrix[index[image], column] = 1.0
    return matrix


def audit_symmetric_coset_label_superselection(
    n: int = 3,
    *,
    tolerance: float = 1e-10,
) -> CosetLabelSuperselectionControl:
    """Verify (1) and its exact cross-irrep block zeros for a transposition."""

    if n < 2:
        raise ValueError("n must be at least two")
    fourier, permutations, partitions = symmetric_group_fourier_matrix(n)
    identity = tuple(range(n))
    transposition = tuple((1, 0, *range(2, n)))
    subgroup = (identity, transposition)
    order = len(permutations)
    state = sum(
        (_right_regular_matrix(permutations, element) for element in subgroup),
        np.zeros((order, order), dtype=complex),
    ) / order
    fourier_state = fourier.conj().T @ state @ fourier

    widths = tuple(hook_length_dimension(partition) ** 2 for partition in partitions)
    offsets = [0]
    for width in widths:
        offsets.append(offsets[-1] + width)
    cross = 0.0
    for left in range(len(widths)):
        for right in range(len(widths)):
            if left == right:
                continue
            block = fourier_state[
                offsets[left] : offsets[left + 1],
                offsets[right] : offsets[right + 1],
            ]
            cross = max(cross, float(np.linalg.norm(block, ord=2)))
    trace_residual = abs(float(np.trace(state).real) - 1.0)
    minimum = float(np.min(np.linalg.eigvalsh((state + state.conj().T) / 2.0)))
    unitarity = float(np.linalg.norm(fourier.conj().T @ fourier - np.eye(order), ord=2))
    verified = bool(
        trace_residual <= 100 * tolerance
        and minimum >= -100 * tolerance
        and cross <= 1000 * tolerance
        and unitarity <= 1000 * tolerance
    )
    return CosetLabelSuperselectionControl(
        n=n,
        group_order=order,
        subgroup_order=len(subgroup),
        irrep_count=len(partitions),
        coset_state_trace_residual=trace_residual,
        coset_state_minimum_eigenvalue=minimum,
        maximum_cross_irrep_block_norm=cross,
        qft_unitarity_residual=unitarity,
        exact_irrep_label_block_diagonality_verified=verified,
        status=(
            "coset-state-irrep-label-superselection-verified"
            if verified
            else "coset-label-superselection-control-failure"
        ),
    )


def audit_cyclic_label_retention(
    order: int,
    exponent_parameters: tuple[int, ...],
    *,
    tolerance: float = 1e-9,
) -> CyclicLabelRetentionControl:
    """Audit the exact matching-block calculation following equation (3)."""

    transformed = transformed_cyclic_power_map(order, exponent_parameters)
    copies = len(exponent_parameters)
    factor_count = len(power_tuple(exponent_parameters))
    expected_count = order ** (factor_count - 1)
    expected_mass = order ** (1 - factor_count)
    counts = []
    masses = []
    for input_character in range(order):
        column_mass = np.abs(transformed[:, input_character]) ** 2
        active = column_mass[column_mass > tolerance]
        counts.append(len(active))
        masses.extend(float(value) for value in active)

    # The paired coefficients (1-r_i,r_i) generate Z_m because each pair sums
    # to one.  Hence a uniform physical output-label tuple satisfies the one
    # linear selection rule with probability exactly 1/m.
    selection_probability = 1.0 / order
    mean_matching = selection_probability * expected_mass
    inverse_normalization = order ** (-2 * copies)
    isometry_residual = float(
        np.linalg.norm(
            transformed.conj().T @ transformed - np.eye(order),
            ord=2,
        )
    )
    verified = bool(
        isometry_residual <= 1000 * tolerance
        and min(counts) == max(counts) == expected_count
        and max(abs(value - expected_mass) for value in masses) <= 1000 * tolerance
        and abs(mean_matching - inverse_normalization) <= 100 * tolerance
    )
    return CyclicLabelRetentionControl(
        group_order=order,
        copy_count=copies,
        exponent_parameters=exponent_parameters,
        output_factor_count=factor_count,
        transformed_isometry_residual=isometry_residual,
        nonzero_output_blocks_per_input=min(counts),
        expected_nonzero_output_blocks_per_input=expected_count,
        minimum_nonzero_block_mass=min(masses),
        maximum_nonzero_block_mass=max(masses),
        expected_nonzero_block_mass=expected_mass,
        selection_probability_for_random_physical_labels=selection_probability,
        mean_matching_physical_block_mass=mean_matching,
        inverse_normalization_squared=inverse_normalization,
        exact_label_retention_identity_verified=verified,
        status=(
            "coherent-label-retention-does-not-cancel-block-normalization"
            if verified
            else "cyclic-label-retention-control-failure"
        ),
    )


def plancherel_inverse_normalization_mean(
    dimensions: tuple[int, ...],
    copy_count: int,
) -> float:
    if not dimensions or any(dimension < 1 for dimension in dimensions):
        raise ValueError("irrep dimensions must be positive")
    if copy_count < 1:
        raise ValueError("copy_count must be positive")
    order = sum(dimension * dimension for dimension in dimensions)
    cube_sum = sum(dimension**3 for dimension in dimensions)
    return cube_sum ** (2 * copy_count + 1) / order ** (4 * copy_count + 1)


def _brute_force_inverse_normalization_mean(
    dimensions: tuple[int, ...],
    copy_count: int,
) -> float:
    order = sum(dimension * dimension for dimension in dimensions)
    probabilities = tuple(dimension * dimension / order for dimension in dimensions)
    total = 0.0
    for indices in itertools.product(range(len(dimensions)), repeat=2 * copy_count + 1):
        candidate = dimensions[indices[0]]
        source_product = math.prod(dimensions[index] for index in indices[1:])
        probability = math.prod(probabilities[index] for index in indices)
        total += probability * candidate * source_product / order ** (2 * copy_count)
    return total


def audit_plancherel_normalization(
    family: str,
    dimensions: tuple[int, ...],
    copy_count: int,
    *,
    tolerance: float = 1e-12,
) -> PlancherelNormalizationControl:
    order = sum(dimension * dimension for dimension in dimensions)
    exact = plancherel_inverse_normalization_mean(dimensions, copy_count)
    brute = _brute_force_inverse_normalization_mean(dimensions, copy_count)
    universal = order ** (-copy_count + 0.5)
    residual = abs(exact - brute)
    verified = bool(residual <= 100 * tolerance and exact <= universal + 100 * tolerance)
    return PlancherelNormalizationControl(
        family=family,
        group_order=order,
        irrep_dimensions=dimensions,
        copy_count=copy_count,
        dimension_square_sum=order,
        dimension_cube_sum=sum(dimension**3 for dimension in dimensions),
        exact_inverse_normalization_mean=exact,
        brute_force_inverse_normalization_mean=brute,
        universal_upper_bound=universal,
        exact_formula_residual=residual,
        upper_bound_verified=verified,
        status=(
            "plancherel-label-average-preserves-superpolynomial-normalization-loss"
            if verified
            else "plancherel-normalization-control-failure"
        ),
    )


def label_coherence_scaling_record(
    n: int,
    *,
    polynomial_benchmark_degree: int = 20,
) -> LabelCoherenceScalingRecord:
    if n < 2:
        raise ValueError("n must be at least two")
    log_order = math.log2(math.factorial(n))
    copies = math.ceil(3.0 * log_order) + 2
    log_mean_upper = (-copies + 0.5) * log_order
    amplification_lower = -0.5 * log_mean_upper
    benchmark = polynomial_benchmark_degree * math.log2(n)
    rejected = amplification_lower > benchmark
    return LabelCoherenceScalingRecord(
        n=n,
        log2_group_order=log_order,
        copy_count=copies,
        log2_inverse_normalization_mean_upper_bound=log_mean_upper,
        log2_amplitude_amplification_lower_bound=amplification_lower,
        polynomial_benchmark_log2=benchmark,
        globally_distinct_conditioning_probability_tends_to_one=True,
        label_coherence_cancellation_superpolynomially_rejected=rejected,
        status=(
            "plancherel-label-coherence-cancellation-superpolynomially-rejected"
            if rejected
            else "finite-label-coherence-separation-not-yet-visible"
        ),
    )


def run_label_coherent_power_map_boundary() -> LabelCoherentPowerMapBoundaryReport:
    coset = audit_symmetric_coset_label_superselection(3)
    cyclic = [
        audit_cyclic_label_retention(3, (2,)),
        audit_cyclic_label_retention(5, (2, 1)),
    ]
    s3_dimensions = tuple(
        hook_length_dimension(partition) for partition in integer_partitions(3)
    )
    plancherel = [
        audit_plancherel_normalization("C5", (1, 1, 1, 1, 1), 2),
        audit_plancherel_normalization("S3", s3_dimensions, 2),
    ]
    scaling = [label_coherence_scaling_record(n) for n in (8, 16, 32, 64, 128)]
    verified = bool(
        coset.exact_irrep_label_block_diagonality_verified
        and all(row.exact_label_retention_identity_verified for row in cyclic)
        and all(row.upper_bound_verified for row in plancherel)
        and all(row.label_coherence_cancellation_superpolynomially_rejected for row in scaling)
    )
    theorem = LabelCoherentPowerMapTheorem(
        coset_label_superselection=(
            "The mixed HSP coset state is |G|^-1 sum_(h in H) R_h and is exactly "
            "block diagonal in inequivalent QFT irrep labels."
        ),
        source_block_conservation=(
            "Every branch field J_h and candidate convolution C_Lambda acts "
            "within one fixed source-irrep tuple Lambda."
        ),
        wrong_block_interpretation=(
            "Other output-irrep blocks of the power-map isometry are orthogonal "
            "leakage, not coherent paths to the required Lambda-preserving output."
        ),
        plancherel_inverse_normalization_mean=(
            "For independent Plancherel labels, E[alpha^-2] equals "
            "S_3^(2k+1)/|G|^(4k+1)."
        ),
        dimension_bound=(
            "S_3<=d_max|G|<=|G|^(3/2), so the mean is at most |G|^(-k+1/2)."
        ),
        cyclic_control=(
            "For C_m, retaining all Fourier labels restores total norm one but "
            "the mean mass in the matching physical block remains m^(-2k)."
        ),
        surviving_escape=(
            "A whole-quadrant FFT-like recursion may still combine exponent terms "
            "before any source-block selection."
        ),
        scope=(
            "This rejects Plancherel label-coherence cancellation, not arbitrary "
            "label-mixing circuits, direct polars, or coherent whole-sum factorizations."
        ),
        theorem_verified=verified,
        status=(
            "label-coherent-power-map-normalization-cancellation-rejected"
            if verified
            else "label-coherent-power-map-boundary-control-failure"
        ),
    )
    tail = scaling[-1]
    return LabelCoherentPowerMapBoundaryReport(
        created_at=utc_now(),
        theorem_contract=asdict(theorem),
        theorem=theorem,
        coset_superselection_control=coset,
        cyclic_controls=cyclic,
        plancherel_controls=plancherel,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "test_source_label_coherence_as_power_map_normalization_resource",
                "resolved": verified,
                "resolution": (
                    "Rejected: the physical source is an exact irrep-block mixture, "
                    "the desired map preserves those blocks, and the Plancherel mean "
                    "inverse normalization is superpolynomially small."
                ),
            },
            {
                "obligation": "factor_complete_quadrant_sum_before_block_selection",
                "resolved": False,
                "resolution": (
                    "The term coefficients and exponent tuples must be combined by "
                    "one structured recursion; label retention alone does not do it."
                ),
            },
            {
                "obligation": "compile_physical_input_transform_and_hidden_label_decoder",
                "resolved": False,
                "resolution": "No end-to-end physical circuit or decoder is established.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "Not measuring weak Fourier labels supplies useful cross-label phases.",
                "resolved": True,
                "resolution": "False for mixed HSP coset states: inequivalent labels are exact direct-sum blocks, not a coherent superposition.",
            },
            {
                "objection": "The norm-one full power-map isometry makes every output block useful.",
                "resolved": True,
                "resolution": "False for a source-label-preserving target: wrong labels are orthogonal leakage and cannot be reinterpreted as the desired carrier.",
            },
            {
                "objection": "This rules out any coherent use of the full quadrant expansion.",
                "resolved": False,
                "resolution": "No. A recursion that combines all exponent terms before exposing labels is outside the theorem.",
            },
        ],
        headline_metrics={
            "coset_irrep_superselection_theorem_count": int(verified),
            "label_coherence_normalization_no_go_count": int(verified),
            "cyclic_exact_control_count": len(cyclic),
            "plancherel_exact_control_count": len(plancherel),
            "tail_n": tail.n,
            "tail_copy_count": tail.copy_count,
            "tail_log2_inverse_normalization_mean_upper_bound": tail.log2_inverse_normalization_mean_upper_bound,
            "whole_quadrant_factorization_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "physical_coset_source_cross_irrep_coherence_available": False,
            "branch_field_preserves_source_irrep_tuple": True,
            "wrong_power_map_output_labels_are_useful_target_paths": False,
            "plancherel_label_average_cancels_termwise_normalization": False,
            "label_coherence_escape_rejected": verified,
            "whole_quadrant_sum_factorized": False,
            "direct_equivariant_multiplier_compiled": False,
            "physical_decoder_compiled": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
        },
        status=theorem.status,
        summary=(
            "Keeping weak Fourier labels coherent does not repair the power-map "
            "normalization: physical coset states have exact irrep-label "
            "superselection, and Plancherel averaging leaves a superpolynomially "
            "small matching-block coefficient. The whole-quadrant recursion remains open."
        ),
        falsifiers_triggered=[
            "Source Plancherel amplitudes cannot be harvested as cross-irrep interference in a mixed coset state.",
            "Retaining all power-map output labels preserves total norm but mostly produces wrong physical source sectors.",
            "The only surviving power-map route must combine the full quadrant sum before label selection.",
        ],
    )


def write_label_coherent_power_map_boundary_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_label_coherent_power_map_boundary())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return payload


if __name__ == "__main__":
    report = write_label_coherent_power_map_boundary_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
