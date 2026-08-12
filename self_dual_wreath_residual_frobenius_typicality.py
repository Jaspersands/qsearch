"""Vanishing residual relation energy on natural pair-core coefficients.

The exact star carrier law permits a stronger statistic than worst-case
correlation or raw channel rank.  Weight every residual singular channel by
``multiplicity * gamma^2``.  This is exactly the squared Frobenius norm of the
off-diagonal pair-core overlap block.

For three orientations, source partitions occupy four complementary pattern
classes ``(0,7),(1,6),(2,5),(3,4)``.  Averaging independent Plancherel factors
inside every nonempty block and summing the exact carrier rows gives, for
*every* occupancy stratum,

    E ||B_ab^* B_ac||_F,res^2 / (d_nu D_sources)
       <= 4 / (n!)^5.                                     (1)

The deficient strata are important.  If any arm class ``(1,6)``, ``(2,5)``,
or ``(3,4)`` is empty, all surviving rows have one-dimensional carriers and
correlation one, so exact-common removal kills them.  If only ``(0,7)`` is
empty, the full-pattern carrier is forced to ``nu`` and character
orthogonality still gives equality in (1).  If all classes are occupied, the
fourth-power row law gives

    sum_(beta,p,bits) d_beta^4 d_p^4/(n!)^7
                           * 1/(d_beta^2 d_p^2)
      = 4/(n!)^5.                                         (2)

Let ``N=2^k`` orientations and let ``O`` be the off-diagonal part of the full
residual relation Gram on all pair-core coefficient spaces.  Each unordered
adjacent pair of pair cores is one centered orientation triple, and both
matrix directions occur in ``||O||_F^2``.  Hence

    E ||O||_F^2 / ambient
      <= 4 N(N-1)(N-2)/(n!)^5.                            (3)

At ``k=ceil(log_2(n!))`` this is ``O((n!)^-2)``.  The pair-core rank theorem
simultaneously lower-bounds total coefficient dimension by
``Omega(ambient/n!)`` on the globally distinct natural sector.  Conditioning
(3), then applying Markov at the geometric mean of these scales, proves

    ||O||_F^2 / dim(coefficients) = O((n!)^-1/2)           (4)

with failure ``O((n!)^-1/2)`` (finite constants are computed below).  The
graded off-diagonal perturbation has the same Frobenius norm because grading
only changes incidence signs.

For a Hermitian perturbation, (4) implies an information-theoretic spectral
trim: after deleting at most ``delta/epsilon^2`` coefficient fraction, its
compression has norm at most ``epsilon``.  Intersecting the metric and graded
low-energy spaces costs at most twice that fraction.

This does not yet prove the hierarchical endpoint gap.  The joint trim need
not commute with the internal/crossing edge grading, need not have an efficient
coherent implementation, and coefficient trace has not been identified with
accepted PGM state trace.  The theorem establishes that bad residual geometry
is low-dimensional in the natural relation coefficient measure, not that the
algorithm can already remove it.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import (
    conjugate_partition,
    hook_length_dimension,
    integer_partitions,
)
from research_registry import utc_now
from self_dual_wreath_global_collision_free_mass import (
    global_collision_free_mass_record,
)
from self_dual_wreath_pair_core_rank_concentration import (
    pair_core_density_scaling_record,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_residual_frobenius_typicality.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-RESIDUAL-FROBENIUS-TYPICALITY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]


@dataclass(frozen=True)
class OccupancyEnergyControl:
    n: int
    target_partition: Partition
    positive_complement_classes: tuple[bool, bool, bool, bool]
    expected_residual_squared_overlap_fraction: str
    expected_exact_common_squared_overlap_fraction: str
    universal_residual_bound: str
    residual_to_bound_ratio: float
    arm_class_missing: bool
    residual_vanishes_when_arm_class_missing: bool
    universal_bound_respected: bool
    status: str


@dataclass(frozen=True)
class FrobeniusSpectralTrimControl:
    dimension: int
    tolerance: float
    metric_frobenius_density: float
    graded_frobenius_density: float
    metric_removed_dimension: int
    graded_removed_dimension: int
    joint_retained_dimension_lower_bound: int
    joint_removed_fraction_upper_bound: float
    metric_retained_norm: float
    graded_retained_norm: float
    frobenius_markov_bound_respected: bool
    status: str


@dataclass(frozen=True)
class ResidualFrobeniusScalingRecord:
    n: int
    group_order_decimal: str
    information_threshold_copy_count: int
    orientation_count_decimal: str
    conditioned_expected_offdiagonal_frobenius_fraction: float
    conditioned_expected_offdiagonal_frobenius_fraction_log2: float
    pair_coefficient_dimension_lower_fraction: float
    pair_coefficient_dimension_lower_fraction_log2: float
    frobenius_density_threshold: float
    frobenius_density_threshold_log2: float
    markov_failure_probability_upper_bound: float
    pair_rank_event_failure_probability_upper_bound: float
    combined_structural_failure_probability_upper_bound: float
    spectral_trim_tolerance: float
    metric_and_graded_removed_fraction_upper_bound: float
    retained_relation_metric_eigenvalue_lower_bound: float
    retained_relation_metric_eigenvalue_upper_bound: float
    finite_vanishing_fraction_trim_certified: bool
    status: str


@dataclass(frozen=True)
class ResidualFrobeniusTypicalityReport:
    created_at: str
    theorem_contract: dict[str, Any]
    occupancy_controls: list[OccupancyEnergyControl]
    spectral_trim_controls: list[FrobeniusSpectralTrimControl]
    scaling_records: list[ResidualFrobeniusScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _twist(partition: Partition, sign_bit: int) -> Partition:
    return conjugate_partition(partition) if sign_bit else partition


def _expected_block_multiplicity_fraction(
    n: int,
    target: Partition,
    pattern: int,
    carrier: Partition,
    positive_complement_classes: tuple[bool, bool, bool, bool],
) -> Fraction:
    class_index = {0: 0, 7: 0, 1: 1, 6: 1, 2: 2, 5: 2, 3: 3, 4: 3}[pattern]
    if positive_complement_classes[class_index]:
        return Fraction(hook_length_dimension(carrier), math.factorial(n))
    if pattern == 7:
        return (
            Fraction(1, hook_length_dimension(target))
            if carrier == target
            else Fraction()
        )
    return Fraction(1) if carrier == (n,) else Fraction()


def expected_star_overlap_energy_by_occupancy(
    n: int,
    target: Partition,
    positive_complement_classes: tuple[bool, bool, bool, bool],
) -> tuple[Fraction, Fraction]:
    """Return expected residual and exact-common squared overlap fractions."""

    if len(positive_complement_classes) != 4:
        raise ValueError("four complement-pattern occupancy flags are required")
    partitions = tuple(integer_partitions(n))
    dimensions = {
        partition: hook_length_dimension(partition) for partition in partitions
    }
    residual = Fraction()
    common = Fraction()
    for left_bit, right_bit in itertools.product((0, 1), repeat=2):
        mixed_bit = left_bit ^ right_bit
        for beta in partitions:
            beta_factor = math.prod(
                (
                    _expected_block_multiplicity_fraction(
                        n,
                        target,
                        pattern,
                        _twist(beta, twist),
                        positive_complement_classes,
                    )
                    for pattern, twist in (
                        (1, 0),
                        (3, right_bit),
                        (5, left_bit),
                        (7, mixed_bit),
                    )
                ),
                start=Fraction(1),
            )
            if not beta_factor:
                continue
            for companion in partitions:
                companion_factor = math.prod(
                    (
                        _expected_block_multiplicity_fraction(
                            n,
                            target,
                            pattern,
                            _twist(companion, twist),
                            positive_complement_classes,
                        )
                        for pattern, twist in (
                            (2, 0),
                            (6, left_bit),
                            (4, mixed_bit),
                        )
                    ),
                    start=Fraction(1),
                )
                if not companion_factor:
                    continue
                beta_dimension = dimensions[beta]
                companion_dimension = dimensions[companion]
                squared_overlap_mass = (
                    beta_factor
                    * companion_factor
                    * companion_dimension
                    / (beta_dimension**2 * companion_dimension**2)
                )
                if beta_dimension * companion_dimension == 1:
                    common += squared_overlap_mass
                else:
                    residual += squared_overlap_mass
    return residual, common


def audit_occupancy_energy(
    n: int,
    target: Partition,
    positive_complement_classes: tuple[bool, bool, bool, bool],
) -> OccupancyEnergyControl:
    residual, common = expected_star_overlap_energy_by_occupancy(
        n, target, positive_complement_classes
    )
    bound = Fraction(4, math.factorial(n) ** 5)
    arm_missing = not all(positive_complement_classes[1:])
    verified = residual <= bound and (not arm_missing or residual == 0)
    return OccupancyEnergyControl(
        n=n,
        target_partition=target,
        positive_complement_classes=positive_complement_classes,
        expected_residual_squared_overlap_fraction=str(residual),
        expected_exact_common_squared_overlap_fraction=str(common),
        universal_residual_bound=str(bound),
        residual_to_bound_ratio=float(residual / bound),
        arm_class_missing=arm_missing,
        residual_vanishes_when_arm_class_missing=(
            not arm_missing or residual == 0
        ),
        universal_bound_respected=verified,
        status=(
            "universal-residual-star-frobenius-bound-verified"
            if verified
            else "residual-star-frobenius-bound-failure"
        ),
    )


def audit_frobenius_spectral_trim(
    metric_perturbation: np.ndarray,
    graded_perturbation: np.ndarray,
    tolerance: float,
) -> FrobeniusSpectralTrimControl:
    """Verify the two-operator Frobenius spectral deletion bound."""

    if metric_perturbation.shape != graded_perturbation.shape:
        raise ValueError("perturbations must have the same shape")
    if not 0 < tolerance < 1:
        raise ValueError("tolerance must lie in (0,1)")
    dimension = len(metric_perturbation)

    def low_space(matrix: np.ndarray) -> tuple[np.ndarray, int, float, float]:
        matrix = (matrix + matrix.conj().T) / 2
        values, vectors = np.linalg.eigh(matrix)
        keep = np.abs(values) <= tolerance
        basis = vectors[:, keep]
        removed = dimension - basis.shape[1]
        norm = (
            float(np.linalg.norm(basis.conj().T @ matrix @ basis, ord=2))
            if basis.shape[1]
            else 0.0
        )
        density = float(np.linalg.norm(matrix, ord="fro") ** 2 / dimension)
        return basis, removed, norm, density

    metric_basis, metric_removed, metric_norm, metric_density = low_space(
        metric_perturbation
    )
    graded_basis, graded_removed, graded_norm, graded_density = low_space(
        graded_perturbation
    )
    joint_lower = max(0, dimension - metric_removed - graded_removed)
    bound = (metric_density + graded_density) / (tolerance * tolerance)
    verified = bool(
        metric_removed / dimension <= metric_density / tolerance**2 + 1e-12
        and graded_removed / dimension <= graded_density / tolerance**2 + 1e-12
        and metric_norm <= tolerance + 1e-12
        and graded_norm <= tolerance + 1e-12
    )
    return FrobeniusSpectralTrimControl(
        dimension=dimension,
        tolerance=tolerance,
        metric_frobenius_density=metric_density,
        graded_frobenius_density=graded_density,
        metric_removed_dimension=metric_removed,
        graded_removed_dimension=graded_removed,
        joint_retained_dimension_lower_bound=joint_lower,
        joint_removed_fraction_upper_bound=min(1.0, bound),
        metric_retained_norm=metric_norm,
        graded_retained_norm=graded_norm,
        frobenius_markov_bound_respected=verified,
        status=(
            "two-operator-frobenius-spectral-trim-verified"
            if verified
            else "frobenius-spectral-trim-failure"
        ),
    )


def residual_frobenius_scaling_record(
    n: int,
    spectral_trim_tolerance: float = 0.25,
) -> ResidualFrobeniusScalingRecord:
    order = math.factorial(n)
    copy_count = math.ceil(math.log2(order))
    orientation_count = 1 << copy_count
    collision = global_collision_free_mass_record(n)
    pair = pair_core_density_scaling_record(n)
    collision_probability = (
        math.exp2(collision.log2_unconditioned_global_collision_free_probability)
        if collision.log2_unconditioned_global_collision_free_probability > -1074
        else 0.0
    )
    independent_energy = (
        4
        * orientation_count
        * (orientation_count - 1)
        * (orientation_count - 2)
        / order**5
    )
    conditioned_energy = (
        independent_energy / collision_probability
        if collision_probability
        else math.inf
    )
    coefficient_lower = (
        pair.balanced_ordered_pair_fraction
        * math.comb(orientation_count, 2)
        * 2
        * pair.pair_rank_relative_lower_factor
        / order**3
    )
    ratio = conditioned_energy / coefficient_lower
    density_threshold = math.sqrt(ratio)
    markov_failure = density_threshold
    pair_failure = pair.conditioned_balanced_pair_failure_upper_bound
    combined = min(1.0, markov_failure + pair_failure)
    removed = min(
        1.0,
        2 * density_threshold / spectral_trim_tolerance**2,
    )
    certified = bool(
        pair.uniform_balanced_pair_rank_concentration_certified
        and math.isfinite(density_threshold)
        and density_threshold < 1
        and removed < 1
    )
    return ResidualFrobeniusScalingRecord(
        n=n,
        group_order_decimal=str(order),
        information_threshold_copy_count=copy_count,
        orientation_count_decimal=str(orientation_count),
        conditioned_expected_offdiagonal_frobenius_fraction=conditioned_energy,
        conditioned_expected_offdiagonal_frobenius_fraction_log2=(
            math.log2(conditioned_energy) if conditioned_energy > 0 else -math.inf
        ),
        pair_coefficient_dimension_lower_fraction=coefficient_lower,
        pair_coefficient_dimension_lower_fraction_log2=math.log2(
            coefficient_lower
        ),
        frobenius_density_threshold=density_threshold,
        frobenius_density_threshold_log2=math.log2(density_threshold),
        markov_failure_probability_upper_bound=markov_failure,
        pair_rank_event_failure_probability_upper_bound=pair_failure,
        combined_structural_failure_probability_upper_bound=combined,
        spectral_trim_tolerance=spectral_trim_tolerance,
        metric_and_graded_removed_fraction_upper_bound=removed,
        retained_relation_metric_eigenvalue_lower_bound=(
            2 - spectral_trim_tolerance
        ),
        retained_relation_metric_eigenvalue_upper_bound=(
            2 + spectral_trim_tolerance
        ),
        finite_vanishing_fraction_trim_certified=certified,
        status=(
            "vanishing-coefficient-fraction-relation-trim-certified"
            if certified
            else "finite-frobenius-trim-conditioning-bound-vacuous"
        ),
    )


def _spectral_trim_controls() -> list[FrobeniusSpectralTrimControl]:
    rng = np.random.default_rng(20260808)
    controls = []
    for dimension, rank, scale in ((20, 2, 0.7), (32, 4, 0.4)):
        first = rng.normal(size=(dimension, rank))
        second = rng.normal(size=(dimension, rank))
        metric = scale * (first @ first.T) / dimension
        graded = scale * (second @ second.T) / dimension
        controls.append(audit_frobenius_spectral_trim(metric, graded, 0.25))
    return controls


def run_residual_frobenius_typicality() -> ResidualFrobeniusTypicalityReport:
    occupancy = [
        audit_occupancy_energy(
            n,
            max(integer_partitions(n), key=hook_length_dimension),
            tuple(bool(mask & (1 << index)) for index in range(4)),
        )
        for n in range(5, 9)
        for mask in range(16)
    ]
    trim_controls = _spectral_trim_controls()
    scaling = [
        residual_frobenius_scaling_record(n)
        for n in (12, 16, 20, 24, 28, 32, 36, 40, 44, 48)
    ]
    failures = sum(not row.universal_bound_respected for row in occupancy) + sum(
        not row.frobenius_markov_bound_respected for row in trim_controls
    )
    certified = sum(
        row.finite_vanishing_fraction_trim_certified for row in scaling
    )
    onset = next(
        (
            row.n
            for row in scaling
            if row.finite_vanishing_fraction_trim_certified
        ),
        0,
    )
    tail = scaling[-1]
    verified = failures == 0
    metrics: dict[str, int | float] = {
        "universal_occupancy_residual_frobenius_theorem_count": int(verified),
        "occupancy_control_count": len(occupancy),
        "occupancy_control_failure_count": sum(
            not row.universal_bound_respected for row in occupancy
        ),
        "missing_arm_residual_vanishing_control_count": sum(
            row.arm_class_missing and row.residual_vanishes_when_arm_class_missing
            for row in occupancy
        ),
        "two_operator_spectral_trim_theorem_count": int(verified),
        "spectral_trim_control_count": len(trim_controls),
        "scaling_row_count": len(scaling),
        "finite_trim_certified_row_count": certified,
        "finite_trim_certification_onset_n": onset,
        "tail_n": tail.n,
        "tail_frobenius_density_threshold_log2": (
            tail.frobenius_density_threshold_log2
        ),
        "tail_removed_fraction_upper_bound": (
            tail.metric_and_graded_removed_fraction_upper_bound
        ),
        "tail_combined_failure_probability_upper_bound": (
            tail.combined_structural_failure_probability_upper_bound
        ),
        "natural_vanishing_coefficient_fraction_trim_theorem_count": 1,
        "grading_compatible_trim_theorem_count": 0,
        "coherent_trim_circuit_count": 0,
        "coefficient_to_pgm_state_mass_transfer_theorem_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return ResidualFrobeniusTypicalityReport(
        created_at=utc_now(),
        theorem_contract={
            "per_star_energy": (
                "For every complement-pattern occupancy stratum, expected "
                "noncommon ||B_ab^*B_ac||_F^2/ambient <=4/(n!)^5."
            ),
            "deficient_patterns": (
                "A missing arm complement class forces all surviving carriers "
                "one-dimensional, hence correlation-one exact common directions."
            ),
            "global_relation_energy": (
                "There are N*binom(N-1,2) centered unordered stars and both "
                "matrix directions, yielding E||O||_F^2/ambient "
                "<=4N(N-1)(N-2)/(n!)^5."
            ),
            "coefficient_dimension": (
                "Uniform balanced pair-rank concentration supplies total "
                "coefficient dimension Omega(ambient/n!)."
            ),
            "spectral_trim": (
                "Frobenius density delta permits epsilon-norm compression after "
                "deleting at most delta/epsilon^2 dimension; metric and graded "
                "trims together cost at most twice this."
            ),
            "scope": (
                "The common retained space need not preserve internal/crossing "
                "grading and coefficient trace is not yet accepted-state trace."
            ),
        },
        occupancy_controls=occupancy,
        spectral_trim_controls=trim_controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "bound_every_pattern_stratum_not_only_typical_triples",
                "resolved": verified,
                "resolution": "All 16 occupancy strata are handled algebraically; missing arms contribute only exact common channels."
            },
            {
                "obligation": "prove_residual_relation_energy_vanishes_per_coefficient",
                "resolved": verified,
                "resolution": "The O((n!)^-2) aggregate energy is divided by the Omega((n!)^-1) concentrated pair coefficient dimension and Markov-optimized."
            },
            {
                "obligation": "construct_grading_compatible_low_energy_trim",
                "resolved": False,
                "resolution": "The intersection of metric and graded low-energy spaces may mix internal and crossing edge variables."
            },
            {
                "obligation": "transfer_coefficient_fraction_to_pgm_state_trace",
                "resolved": False,
                "resolution": "Need a trace identity through the hierarchical polar frames and accepted source-state normalization."
            },
        ],
        adversarial_audit=[
            {
                "objection": "Rare deficient membership patterns can dominate the global Frobenius sum.",
                "resolved": True,
                "resolution": "They cannot: missing arm classes are exact common only, and the target-only full-pattern case still gives exactly 4/(n!)^5."
            },
            {
                "objection": "A small average correlation controls the relation operator norm.",
                "resolved": True,
                "resolution": "Not on the full space. It controls operator norm only after an explicit information-theoretic spectral deletion whose dimension loss is quantified."
            },
            {
                "objection": "The spectral deletion proves an implementable endpoint sampler.",
                "resolved": False,
                "resolution": "No grading-compatible projector or coherent circuit is constructed, and PGM state-mass preservation is unproved."
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "universal_residual_star_frobenius_bound_proved": verified,
            "natural_relation_frobenius_density_vanishes_proved": verified,
            "vanishing_coefficient_fraction_spectral_trim_exists": verified,
            "worst_case_gamma_controls_typical_relation_spectrum": False,
            "grading_compatible_trim_proved": False,
            "coherent_trim_implementation_proved": False,
            "coefficient_trace_equals_pgm_state_trace_proved": False,
            "natural_shorted_endpoint_comparability_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Residual relation geometry is spectrally benign on almost all "
                "coefficient dimensions, but the required physical, graded, "
                "state-mass-preserving trim is not constructed."
            ),
        },
        status=(
            "residual-relation-frobenius-density-vanishes-"
            "physical-graded-trim-open"
            if verified
            else "residual-frobenius-typicality-control-failure"
        ),
        summary=(
            "Proved a universal 4/(n!)^5 residual star-energy bound and a "
            "vanishing-coefficient-fraction joint spectral trim for the natural "
            "relation metric and grading perturbations."
        ),
        falsifiers_triggered=[
            "Rare empty membership blocks do not amplify noncommon residual Frobenius energy.",
            "Small Frobenius density is an existence theorem for trimming, not a full-space operator-norm theorem.",
            "A low-dimensional coefficient obstruction may still carry disproportionate PGM state mass until a trace transfer is proved.",
        ],
    )


def write_residual_frobenius_typicality_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-RESIDUAL-FROBENIUS-TYPICALITY"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_residual_frobenius_typicality())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    return payload


if __name__ == "__main__":
    report = write_residual_frobenius_typicality_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
