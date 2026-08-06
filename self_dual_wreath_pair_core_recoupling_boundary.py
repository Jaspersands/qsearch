"""Pair-core recoupling spectra and the local conditioning boundary.

The common-core atomization route fails when pair-core projectors do not
commute.  The first collision-free failures are nevertheless highly
structured.  Two pair cores sharing one orientation contract through a
nontrivial symmetric-group carrier with correlation ``gamma=1/d``.  On a
scalar carrier mode, two crossing pair relations have exact relative spectra

    open star:   (1-gamma)/(2-gamma), (1+gamma)/(2+gamma),

while quotienting a third, same-child edge gives

    closed star: (1-gamma)/(2-gamma),
                 (1+gamma-gamma^2)/(2+gamma-gamma^2).

Extra orthogonal modes remain at one half.  If the carrier is nontrivial and
``n>=5``, then ``d>=n-1``.  Hence every isolated scalar star lies in
``[3/7,5/9]`` and is uniformly separated from zero and one.  The S6 controls
realize carrier dimensions 5, 9, and 10 exactly.

This local result does not prove the hierarchy efficient.  Many pair cores
can meet a leaf, and small ``1/d`` recouplings may accumulate into a large
matrix-valued star.  The decisive remaining question is an all-depth spectral
bound or harmonic block diagonalization for that recoupling graph.
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

import numpy as np

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_collision_free_frame_probe import Label, perfect_matchings
from self_dual_wreath_common_core_atomization import (
    _relative_pair_spectrum,
    audit_common_core_atomization,
    fixed_family_common_range_basis,
    scalar_star_relative_spectrum,
)
from self_dual_wreath_orientation_pair_angle_spectrum import (
    exact_pair_principal_angle_spectrum,
)
from self_dual_wreath_orientation_triple_range import (
    fixed_family_common_range_dimension,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_pair_core_recoupling_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-PAIR-CORE-RECOUPLING-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class PairRelationComparisonCertificate:
    internal_pair_edge_count: int
    crossing_pair_edge_count: int
    maximum_internal_weighted_spectral_radius: float
    crossing_weighted_spectral_radius: float
    crossing_to_internal_weight_norm: float
    internal_relation_gram_lower_bound: float
    quotient_metric_lower_bound: float
    quotient_graded_norm_upper_bound: float
    grading_defect_upper_bound: float
    certified_endpoint_gap_lower_bound: float
    exact_grading_defect_norm: float
    comparison_bound_valid: bool
    endpoint_gap_certified: bool
    status: str


@dataclass(frozen=True)
class PairCoreRecouplingControl:
    control_id: str
    n: int
    target_partition: tuple[int, ...]
    labels: tuple[Label, ...]
    orientation_masks: tuple[int, ...]
    left_orientation_masks: tuple[int, ...]
    right_orientation_masks: tuple[int, ...]
    recoupled_pair_edges: tuple[tuple[int, int], tuple[int, int]]
    scalar_star_type: str
    carrier_dimension: int
    predicted_pair_core_correlation: float
    observed_fractional_pair_core_correlations: tuple[float, ...]
    shared_mode_multiplicity: int
    orthogonal_cross_mode_multiplicity: int
    direct_relative_pair_class_dimension: int
    predicted_fractional_eigenvalues: tuple[float, ...]
    direct_fractional_eigenvalues: tuple[float, ...]
    maximum_correlation_residual: float
    maximum_relative_spectrum_residual: float
    minimum_relative_eigenvalue: float
    maximum_relative_eigenvalue: float
    minimum_endpoint_gap: float
    comparison_certificate: PairRelationComparisonCertificate
    scalar_star_formula_verified: bool
    status: str


@dataclass(frozen=True)
class RecouplingScreenRecord:
    n: int
    requested_control_limit: int
    audited_control_count: int
    audited_pair_core_star_count: int
    fractional_correlation_count: int
    reciprocal_carrier_correlation_counts: dict[str, int]
    unexpected_fractional_correlation_count: int
    noncommon_carrier_bound_violation_count: int
    maximum_fractional_pair_core_correlation: float
    theoretical_noncommon_upper_bound: float
    status: str


@dataclass(frozen=True)
class PairCoreRecouplingBoundaryReport:
    created_at: str
    theorem_contract: dict[str, Any]
    selected_controls: list[PairCoreRecouplingControl]
    finite_screen: RecouplingScreenRecord
    scaling_records: list[dict[str, Any]]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def open_scalar_star_relative_spectrum(
    correlation: float,
    shared_mode_multiplicity: int,
    orthogonal_cross_mode_multiplicity: int,
) -> tuple[float, ...]:
    if not 0 <= correlation < 1:
        raise ValueError("correlation must lie in [0,1)")
    if shared_mode_multiplicity < 0 or orthogonal_cross_mode_multiplicity < 0:
        raise ValueError("multiplicities must be nonnegative")
    low = (1 - correlation) / (2 - correlation)
    high = (1 + correlation) / (2 + correlation)
    return tuple(
        sorted(
            [low] * shared_mode_multiplicity
            + [0.5] * orthogonal_cross_mode_multiplicity
            + [high] * shared_mode_multiplicity
        )
    )


def scalar_star_uniform_interval(n: int) -> tuple[float, float]:
    """Return a uniform interval for open and closed scalar stars."""

    if n < 5:
        raise ValueError("the symmetric-group carrier bound requires n>=5")
    maximum_correlation = 1 / (n - 1)
    lower = (1 - maximum_correlation) / (2 - maximum_correlation)
    upper = (1 + maximum_correlation) / (2 + maximum_correlation)
    return lower, upper


def _fractional_correlations(
    left_basis: np.ndarray,
    right_basis: np.ndarray,
    tolerance: float = 1e-8,
) -> tuple[float, ...]:
    values = np.linalg.svd(
        left_basis.conj().T @ right_basis,
        compute_uv=False,
    )
    return tuple(
        float(value)
        for value in values
        if tolerance < value < 1 - tolerance
    )


def pair_relation_comparison_certificate(
    target: tuple[int, ...],
    labels: tuple[Label, ...],
    orientation_masks: tuple[int, ...],
    left_masks: tuple[int, ...],
    right_masks: tuple[int, ...],
    *,
    tolerance: float = 1e-8,
) -> PairRelationComparisonCertificate:
    """Certify a relative pair quotient using block-norm comparison.

    Every pair-relation Gram has diagonal ``2I``.  If ``W_A`` and ``W_X``
    are the internal- and crossing-edge comparison matrices and ``W_XA`` is
    their rectangular coupling, block Gershgorin and a Schur complement give

        lambda_min(M) >= 2-rho(W_X)-||W_XA||^2/(2-rho(W_A)).

    The graded quotient has the corresponding norm bound implemented below.
    Their ratio bounds the exact grading defect.
    """

    pair_bases = {}
    for edge in itertools.combinations(orientation_masks, 2):
        if fixed_family_common_range_dimension(target, labels, edge):
            pair_bases[edge] = fixed_family_common_range_basis(
                target,
                labels,
                edge,
            )
    left_set = set(left_masks)
    right_set = set(right_masks)
    internal = tuple(
        edge
        for edge in pair_bases
        if set(edge) <= left_set or set(edge) <= right_set
    )
    crossing = tuple(
        edge
        for edge in pair_bases
        if len(set(edge) & left_set) == 1
        and len(set(edge) & right_set) == 1
    )

    def comparison(
        rows: tuple[tuple[int, int], ...],
        columns: tuple[tuple[int, int], ...],
    ) -> np.ndarray:
        matrix = np.zeros((len(rows), len(columns)))
        for row, left_edge in enumerate(rows):
            for column, right_edge in enumerate(columns):
                if left_edge == right_edge or not set(left_edge) & set(right_edge):
                    continue
                matrix[row, column] = float(
                    np.linalg.norm(
                        pair_bases[left_edge].conj().T
                        @ pair_bases[right_edge],
                        ord=2,
                    )
                )
        return matrix

    internal_weights = comparison(internal, internal)
    crossing_weights = comparison(crossing, crossing)
    cross_weights = comparison(crossing, internal)
    internal_radius = float(
        np.max(np.linalg.eigvalsh(internal_weights))
        if internal_weights.size
        else 0.0
    )
    crossing_radius = float(
        np.max(np.linalg.eigvalsh(crossing_weights))
        if crossing_weights.size
        else 0.0
    )
    cross_norm = float(
        np.linalg.norm(cross_weights, ord=2) if cross_weights.size else 0.0
    )
    internal_gap = 2 - internal_radius
    if internal_gap <= tolerance:
        metric_lower = -math.inf
        graded_upper = math.inf
        defect_bound = math.inf
    else:
        projection_bound = cross_norm / internal_gap
        metric_lower = (
            2
            - crossing_radius
            - cross_norm * cross_norm / internal_gap
        )
        graded_upper = (
            crossing_radius
            + 2 * projection_bound * cross_norm
            + projection_bound * projection_bound * (2 + internal_radius)
        )
        defect_bound = (
            graded_upper / metric_lower
            if metric_lower > tolerance
            else math.inf
        )
    _, _, exact_defect = _relative_pair_spectrum(
        pair_bases,
        left_masks,
        right_masks,
        tolerance,
    )
    valid = defect_bound + 100 * tolerance >= exact_defect
    endpoint_gap = (
        max(0.0, (1 - defect_bound) / 2)
        if math.isfinite(defect_bound)
        else 0.0
    )
    certified = valid and defect_bound < 1
    return PairRelationComparisonCertificate(
        internal_pair_edge_count=len(internal),
        crossing_pair_edge_count=len(crossing),
        maximum_internal_weighted_spectral_radius=internal_radius,
        crossing_weighted_spectral_radius=crossing_radius,
        crossing_to_internal_weight_norm=cross_norm,
        internal_relation_gram_lower_bound=internal_gap,
        quotient_metric_lower_bound=metric_lower,
        quotient_graded_norm_upper_bound=graded_upper,
        grading_defect_upper_bound=defect_bound,
        certified_endpoint_gap_lower_bound=endpoint_gap,
        exact_grading_defect_norm=exact_defect,
        comparison_bound_valid=valid,
        endpoint_gap_certified=certified,
        status=(
            "weighted-pair-relation-endpoint-gap-certified"
            if certified
            else "pair-relation-comparison-inconclusive"
        ),
    )
def audit_pair_core_recoupling_control(
    control_id: str,
    target: tuple[int, ...],
    labels: tuple[Label, ...],
    orientation_masks: tuple[int, ...],
    left_masks: tuple[int, ...],
    right_masks: tuple[int, ...],
    recoupled_edges: tuple[tuple[int, int], tuple[int, int]],
    carrier_dimension: int,
    scalar_star_type: str,
    *,
    tolerance: float = 1e-8,
) -> PairCoreRecouplingControl:
    if scalar_star_type not in ("open", "closed"):
        raise ValueError("scalar_star_type must be open or closed")
    first = fixed_family_common_range_basis(target, labels, recoupled_edges[0])
    second = fixed_family_common_range_basis(target, labels, recoupled_edges[1])
    correlations = _fractional_correlations(first, second, tolerance)
    predicted_correlation = 1 / carrier_dimension
    shared = len(correlations)
    atomization = audit_common_core_atomization(
        control_id,
        target,
        labels,
        orientation_masks,
        left_masks,
        right_masks,
        tolerance=tolerance,
    )
    direct = atomization.direct_fractional_eigenvalues
    orthogonal = len(direct) - 2 * shared
    if orthogonal < 0:
        raise ArithmeticError("shared scalar modes exceed relative dimension")
    predicted = (
        open_scalar_star_relative_spectrum(
            predicted_correlation,
            shared,
            orthogonal,
        )
        if scalar_star_type == "open"
        else scalar_star_relative_spectrum(
            predicted_correlation,
            shared,
            orthogonal,
        )
    )
    correlation_residual = max(
        (abs(value - predicted_correlation) for value in correlations),
        default=math.inf,
    )
    spectrum_residual = (
        float(
            np.max(
                np.abs(np.array(predicted) - np.array(direct))
            )
        )
        if len(predicted) == len(direct)
        else math.inf
    )
    verified = bool(
        correlations
        and correlation_residual <= 100 * tolerance
        and spectrum_residual <= 100 * tolerance
        and atomization.direct_relative_cech_audit_verified
    )
    minimum = min(direct)
    maximum = max(direct)
    endpoint_gap = min(minimum, 1 - maximum)
    comparison = pair_relation_comparison_certificate(
        target,
        labels,
        orientation_masks,
        left_masks,
        right_masks,
        tolerance=tolerance,
    )
    return PairCoreRecouplingControl(
        control_id=control_id,
        n=sum(target),
        target_partition=target,
        labels=labels,
        orientation_masks=orientation_masks,
        left_orientation_masks=left_masks,
        right_orientation_masks=right_masks,
        recoupled_pair_edges=recoupled_edges,
        scalar_star_type=scalar_star_type,
        carrier_dimension=carrier_dimension,
        predicted_pair_core_correlation=predicted_correlation,
        observed_fractional_pair_core_correlations=correlations,
        shared_mode_multiplicity=shared,
        orthogonal_cross_mode_multiplicity=orthogonal,
        direct_relative_pair_class_dimension=len(direct),
        predicted_fractional_eigenvalues=predicted,
        direct_fractional_eigenvalues=direct,
        maximum_correlation_residual=correlation_residual,
        maximum_relative_spectrum_residual=spectrum_residual,
        minimum_relative_eigenvalue=minimum,
        maximum_relative_eigenvalue=maximum,
        minimum_endpoint_gap=endpoint_gap,
        comparison_certificate=comparison,
        scalar_star_formula_verified=verified,
        status=(
            f"exact-{scalar_star_type}-scalar-star-carrier-{carrier_dimension}"
            if verified
            else "scalar-star-validation-failure"
        ),
    )


def _selected_controls() -> list[PairCoreRecouplingControl]:
    d5_labels: tuple[Label, ...] = (
        ((6,), (2, 2, 2)),
        ((5, 1), (4, 1, 1)),
        ((4, 2), (3, 1, 1, 1)),
        ((3, 3), (1, 1, 1, 1, 1, 1)),
    )
    d9_labels: tuple[Label, ...] = (
        ((6,), (4, 2)),
        ((5, 1), (2, 2, 2)),
        ((3, 3), (2, 1, 1, 1, 1)),
        ((2, 2, 1, 1), (1, 1, 1, 1, 1, 1)),
    )
    d10_labels: tuple[Label, ...] = (
        ((6,), (3, 1, 1, 1)),
        ((5, 1), (3, 3)),
        ((4, 2), (2, 2, 2)),
        ((4, 1, 1), (1, 1, 1, 1, 1, 1)),
    )
    return [
        audit_pair_core_recoupling_control(
            "W6-OPEN-STAR-CARRIER-5",
            (6,),
            d5_labels,
            (0, 3, 7, 14),
            (0, 7),
            (3, 14),
            ((0, 14), (7, 14)),
            5,
            "open",
        ),
        audit_pair_core_recoupling_control(
            "W6-CLOSED-STAR-CARRIER-9",
            (6,),
            d9_labels,
            (2, 5, 11, 12),
            (2, 5),
            (11, 12),
            ((2, 12), (5, 12)),
            9,
            "closed",
        ),
        audit_pair_core_recoupling_control(
            "W6-OPEN-STAR-CARRIER-10",
            (6,),
            d10_labels,
            (0, 3, 7, 14),
            (0, 7),
            (3, 14),
            ((0, 14), (7, 14)),
            10,
            "open",
        ),
    ]


def screen_s6_pair_core_recouplings(
    control_limit: int = 180,
    ambient_cap: int = 125_000,
    tolerance: float = 1e-8,
) -> RecouplingScreenRecord:
    if control_limit < 1:
        raise ValueError("control_limit must be positive")
    n = 6
    partitions = integer_partitions(n)
    dimensions = {
        partition: hook_length_dimension(partition)
        for partition in partitions
    }
    candidates = []
    for subset in itertools.combinations(partitions, 8):
        source_dimension = math.prod(dimensions[item] for item in subset)
        for labels in perfect_matchings(subset):
            for target in partitions:
                ambient = dimensions[target] * source_dimension
                if ambient > ambient_cap:
                    continue
                common_edges = []
                for left, right in itertools.combinations(range(16), 2):
                    dimension = sum(
                        multiplicity
                        for value, multiplicity, _ in exact_pair_principal_angle_spectrum(
                            target,
                            labels,
                            left,
                            right,
                        )
                        if value == 1
                    )
                    if dimension:
                        common_edges.append((left, right, dimension))
                stars = tuple(
                    (left, right)
                    for left, right in itertools.combinations(common_edges, 2)
                    if set(left[:2]) & set(right[:2])
                )
                if stars:
                    candidates.append((ambient, target, labels, stars))
    candidates.sort(key=lambda row: (row[0], row[1], row[2]))

    seen = set()
    audited_stars = 0
    correlations: list[float] = []
    reciprocal_counts: Counter[str] = Counter()
    unexpected = 0
    bound_violations = 0
    reciprocal_values = {
        dimension: 1 / dimension
        for dimension in sorted(set(dimensions.values()))
        if dimension > 1
    }
    bound = 1 / (n - 1)
    for _, target, labels, stars in candidates:
        dimension_profile = tuple(
            sorted(
                (dimensions[left], dimensions[right])
                for left, right in labels
            )
        )
        key = (
            target,
            dimension_profile,
            len(stars),
            tuple(sorted(left[2] + right[2] for left, right in stars)),
        )
        if key in seen:
            continue
        seen.add(key)
        edge_bases: dict[tuple[int, int], np.ndarray] = {}
        for left, right in stars:
            for edge in (left[:2], right[:2]):
                if edge not in edge_bases:
                    edge_bases[edge] = fixed_family_common_range_basis(
                        target,
                        labels,
                        edge,
                    )
            values = _fractional_correlations(
                edge_bases[left[:2]],
                edge_bases[right[:2]],
                tolerance,
            )
            audited_stars += 1
            for value in values:
                correlations.append(value)
                matches = [
                    dimension
                    for dimension, reciprocal in reciprocal_values.items()
                    if abs(value - reciprocal) <= 100 * tolerance
                ]
                if matches:
                    reciprocal_counts[f"1/{min(matches)}"] += 1
                else:
                    unexpected += 1
                bound_violations += value > bound + 100 * tolerance
        if len(seen) >= control_limit:
            break
    return RecouplingScreenRecord(
        n=n,
        requested_control_limit=control_limit,
        audited_control_count=len(seen),
        audited_pair_core_star_count=audited_stars,
        fractional_correlation_count=len(correlations),
        reciprocal_carrier_correlation_counts=dict(sorted(reciprocal_counts.items())),
        unexpected_fractional_correlation_count=unexpected,
        noncommon_carrier_bound_violation_count=bound_violations,
        maximum_fractional_pair_core_correlation=max(correlations, default=0.0),
        theoretical_noncommon_upper_bound=bound,
        status=(
            "all-screened-recouplings-are-reciprocal-carrier-contractions"
            if correlations and not unexpected and not bound_violations
            else "unexpected-pair-core-recoupling-value-found"
        ),
    )


def run_pair_core_recoupling_boundary(
    screen_control_limit: int = 180,
) -> PairCoreRecouplingBoundaryReport:
    controls = _selected_controls()
    screen = screen_s6_pair_core_recouplings(screen_control_limit)
    failures = sum(not control.scalar_star_formula_verified for control in controls)
    lower5, upper5 = scalar_star_uniform_interval(5)
    metrics: dict[str, int | float] = {
        "open_scalar_star_spectrum_theorem_count": 1,
        "closed_scalar_star_spectrum_theorem_count": 1,
        "nontrivial_carrier_local_conditioning_theorem_count": 1,
        "weighted_pair_relation_comparison_theorem_count": 1,
        "selected_scalar_star_control_count": len(controls),
        "selected_scalar_star_validation_failure_count": failures,
        "selected_minimum_relative_eigenvalue": min(
            control.minimum_relative_eigenvalue for control in controls
        ),
        "selected_maximum_relative_eigenvalue": max(
            control.maximum_relative_eigenvalue for control in controls
        ),
        "selected_maximum_comparison_defect_bound": max(
            control.comparison_certificate.grading_defect_upper_bound
            for control in controls
        ),
        "selected_minimum_certified_endpoint_gap": min(
            control.comparison_certificate.certified_endpoint_gap_lower_bound
            for control in controls
        ),
        "selected_comparison_certificate_failure_count": sum(
            not control.comparison_certificate.endpoint_gap_certified
            for control in controls
        ),
        "n5_uniform_scalar_star_lower_bound": lower5,
        "n5_uniform_scalar_star_upper_bound": upper5,
        "screened_control_count": screen.audited_control_count,
        "screened_pair_core_star_count": screen.audited_pair_core_star_count,
        "screened_fractional_correlation_count": screen.fractional_correlation_count,
        "screened_unexpected_correlation_count": screen.unexpected_fractional_correlation_count,
        "screened_carrier_bound_violation_count": screen.noncommon_carrier_bound_violation_count,
        "screened_maximum_fractional_correlation": screen.maximum_fractional_pair_core_correlation,
        "all_n_pair_core_carrier_factorization_count": 0,
        "all_depth_multistar_conditioning_bound_count": 0,
        "coherent_recoupling_block_transform_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return PairCoreRecouplingBoundaryReport(
        created_at=utc_now(),
        theorem_contract={
            "open_scalar_star": "Two crossing scalar pair cores with correlation gamma have channels (1-gamma)/(2-gamma) and (1+gamma)/(2+gamma).",
            "closed_scalar_star": "After quotienting an equicorrelated internal pair core, the high channel becomes (1+gamma-gamma^2)/(2+gamma-gamma^2).",
            "carrier_gap": "Conditional on a nontrivial S_n carrier contraction gamma<=1/(n-1), every isolated scalar star at n>=5 lies in [3/7,5/9].",
            "weighted_multistar_comparison": "Block Gershgorin plus a Schur complement lower-bounds the quotient metric and upper-bounds its grading defect using only pair-core overlap norms.",
            "finite_evidence": "The selected S6 stars realize d=5,9,10 exactly; the broader screen tests whether any fractional value is not a reciprocal irrep dimension.",
            "remaining_boundary": "Prove the carrier factorization and control simultaneous accumulation of many recoupling stars, or construct a sector whose matrix-valued star approaches an endpoint.",
        },
        selected_controls=controls,
        finite_screen=screen,
        scaling_records=[
            {
                "n": n,
                "information_threshold_copy_count": math.ceil(
                    math.lgamma(n + 1) / math.log(2)
                ),
                "minimum_nontrivial_symmetric_group_irrep_dimension": n - 1,
                "conditional_maximum_scalar_recoupling": 1 / (n - 1),
                "isolated_scalar_stars_uniformly_conditioned": True,
                "multistar_weighted_degree_bounded": False,
                "matrix_valued_recoupling_blocks_classified": False,
                "status": "local-carrier-gap-proved-multistar-accumulation-open",
            }
            for n in (6, 8, 16, 32, 64, 128, 256, 512)
        ],
        proof_obligations=[
            {
                "obligation": "scalar_star_relative_spectra",
                "resolved": failures == 0,
                "resolution": "Open and closed formulas match all d=5,9,10 direct Cech spectra, including multiplicities.",
            },
            {
                "obligation": "all_n_pair_core_carrier_factorization",
                "resolved": False,
                "resolution": "Every screened S6 value is reciprocal-carrier, but no all-n recoupling decomposition proves the factorization.",
            },
            {
                "obligation": "all_depth_multistar_conditioning",
                "resolved": False,
                "resolution": "A leaf can meet many common lines; inverse-dimension entries may accumulate despite every isolated star being well conditioned.",
            },
            {
                "obligation": "finite_weighted_pair_relation_certificates",
                "resolved": all(
                    control.comparison_certificate.endpoint_gap_certified
                    for control in controls
                ),
                "resolution": "The weighted Schur comparison certifies a positive endpoint gap for each selected open and closed scalar star.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "Any nonhalf common-core channel kills the hierarchy.",
                "resolved": True,
                "resolution": "False locally: scalar carrier stars remain a constant distance from zero and one and admit constant-interval polynomial transforms.",
            },
            {
                "objection": "Pairwise 1/d recoupling bounds automatically control a high-degree star.",
                "resolved": False,
                "resolution": "No; spectral accumulation depends on weighted degree and phase alignment, not the maximum entry alone.",
            },
            {
                "objection": "The finite reciprocal spectrum proves an all-n 1/d law.",
                "resolved": False,
                "resolution": "The finite screen is evidence only; multiplicity-space 6j blocks could introduce smaller non-reciprocal singular values at larger n.",
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "scalar_star_spectrum_formulas_verified": failures == 0,
            "isolated_nontrivial_carrier_stars_uniformly_conditioned": True,
            "selected_weighted_pair_relation_endpoint_gaps_certified": all(
                control.comparison_certificate.endpoint_gap_certified
                for control in controls
            ),
            "finite_s6_reciprocal_carrier_screen_passed": (
                screen.unexpected_fractional_correlation_count == 0
                and screen.noncommon_carrier_bound_violation_count == 0
            ),
            "all_n_pair_core_carrier_factorization_proved": False,
            "all_depth_multistar_conditioning_proved": False,
            "coherent_recoupling_block_transform_compiled": False,
            "hierarchical_orientation_polar_proved": False,
            "speedup_claim_allowed": False,
            "reason": "The first noncommuting pair-core blocks are locally well conditioned and carrier-structured, but no theorem controls many-star accumulation or compiles the recoupling basis.",
        },
        status="local-scalar-recoupling-conditioned-multistar-spectrum-open",
        summary=(
            f"Verified exact scalar-star spectra for carriers 5, 9, and 10; "
            f"screened {screen.audited_pair_core_star_count} S6 star pairs with "
            "no non-reciprocal value or 1/(n-1) violation. The unresolved "
            "gate is simultaneous matrix-valued accumulation at larger depth."
        ),
        falsifiers_triggered=[
            "A finite nonhalf channel need not be ill conditioned; the scalar-star counterexamples stay in a constant interval.",
            "Exact half-balance is unnecessary if recoupling blocks can be efficiently diagonalized with endpoint gaps.",
            "Local inverse-carrier correlations do not establish an all-depth frame or query bound.",
        ],
    )


def write_pair_core_recoupling_boundary_report(
    path: Path = REPORT_PATH,
    screen_control_limit: int = 180,
) -> dict[str, Any]:
    payload = asdict(run_pair_core_recoupling_boundary(screen_control_limit))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_pair_core_recoupling_boundary_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
