"""Exact pair-core quotient overlap criterion for augmented H0.

For child spans ``A`` and ``B``, let

    K = span_{i in L, j in R} (U_i intersection U_j).       (1)

Then ``K subseteq A intersection B`` and crossing pair relations generate
exactly the physical classes in ``K`` after internal child dependencies are
quotiented.  Hence

    H_cross = 0
      iff (A intersection K^perp) intersection
          (B intersection K^perp) = {0}
      iff ||P_(A minus K) P_(B minus K)|| < 1.              (2)

Equation (2) is the phase-sensitive pair-rich analogue of the common-free
weighted-overlap theorem.  Projecting each leaf off ``K`` also yields a
sign-blind residual comparison graph.  Its normalized bound is sufficient
when below one, but can be infinite or inconclusive even when the exact gap is
positive; phases and internal cancellations are retained only by (2).

This is an exact finite criterion and the correct asymptotic norm target.  It
does not provide an all-n lower bound or a coherent quotient circuit.
"""

from __future__ import annotations

import itertools
import json
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import integer_partitions
from research_registry import utc_now
from self_dual_wreath_collision_free_frame_probe import Label, _w5_probe_labels
from self_dual_wreath_level_three_flag_audit import _reduced_projector_family
from self_dual_wreath_shorted_overlap_balance import (
    _range_intersection_basis,
    _support_basis,
    unique_affine_flag_merges,
)
from self_dual_wreath_recursive_pair_generation import build_orientation_leaf_gram
from self_dual_wreath_weighted_overlap_exclusion import (
    weighted_span_correlation_bound,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_pair_quotient_overlap.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-PAIR-QUOTIENT-OVERLAP"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class PairQuotientOverlapControl:
    control_id: str
    n: int
    target_partition: tuple[int, ...]
    labels: tuple[Label, ...]
    left_orientation_masks: tuple[int, ...]
    right_orientation_masks: tuple[int, ...]
    carrier_dimension: int
    left_span_dimension: int
    right_span_dimension: int
    child_intersection_dimension: int
    crossing_pair_core_count: int
    crossing_pair_core_dimension_sum: int
    crossing_pair_core_span_dimension: int
    emergent_cross_dependency_dimension: int
    left_pair_quotient_dimension: int
    right_pair_quotient_dimension: int
    exact_residual_principal_correlation: float
    exact_pair_quotient_gap_below_one: float
    residual_weighted_span_correlation_bound: float
    residual_left_weight_spectral_radius: float
    residual_right_weight_spectral_radius: float
    residual_sign_blind_bound_certifies_pair_generation: bool
    exact_pair_quotient_certifies_pair_generation: bool
    exact_pair_quotient_overlap_audit: bool
    status: str


@dataclass(frozen=True)
class PairQuotientPortfolioScreen:
    screen_id: str
    n: int
    labels: tuple[Label, ...]
    target_count: int
    active_target_count: int
    affine_merge_audit_count: int
    pair_rich_merge_count: int
    emergent_cross_dependency_merge_count: int
    phase_only_certificate_count: int
    minimum_exact_pair_quotient_gap: float
    minimum_pair_rich_exact_quotient_gap: float
    maximum_exact_residual_principal_correlation: float
    exact_pair_quotient_audit_failure_count: int
    status: str


@dataclass(frozen=True)
class PairQuotientOverlapReport:
    created_at: str
    theorem_contract: dict[str, Any]
    controls: list[PairQuotientOverlapControl]
    s6_portfolio_screen: PairQuotientPortfolioScreen
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _orthonormal_span(columns: list[np.ndarray], dimension: int, tolerance: float) -> np.ndarray:
    active = [column for column in columns if column.shape[1]]
    if not active:
        return np.zeros((dimension, 0), dtype=complex)
    joined = np.concatenate(active, axis=1)
    left, singular_values, _ = np.linalg.svd(joined, full_matrices=False)
    return left[:, singular_values > 100 * tolerance]


def _projected_basis(
    basis: np.ndarray,
    removed: np.ndarray,
    tolerance: float,
) -> np.ndarray:
    projected = basis - removed @ (removed.conj().T @ basis)
    return _orthonormal_span([projected], basis.shape[0], tolerance)


def audit_pair_quotient_overlap(
    control_id: str,
    projectors: tuple[np.ndarray, ...],
    left_masks: tuple[int, ...],
    right_masks: tuple[int, ...],
    *,
    n: int = 0,
    target: tuple[int, ...] = (),
    labels: tuple[Label, ...] = (),
    tolerance: float = 1e-8,
) -> PairQuotientOverlapControl:
    if not projectors:
        raise ValueError("at least one projector is required")
    if not left_masks or not right_masks or set(left_masks) & set(right_masks):
        raise ValueError("children must be disjoint and nonempty")
    dimension = projectors[0].shape[0]
    if any(projector.shape != (dimension, dimension) for projector in projectors):
        raise ValueError("all projectors must act on one carrier")
    leaf_bases = {
        mask: _support_basis(projectors[mask], tolerance)
        for mask in (*left_masks, *right_masks)
    }
    left_span = _orthonormal_span(
        [leaf_bases[mask] for mask in left_masks],
        dimension,
        tolerance,
    )
    right_span = _orthonormal_span(
        [leaf_bases[mask] for mask in right_masks],
        dimension,
        tolerance,
    )
    child_intersection = _range_intersection_basis(
        left_span,
        right_span,
        tolerance,
    )
    pair_cores = []
    pair_dimension_sum = 0
    for left_mask in left_masks:
        for right_mask in right_masks:
            core = _range_intersection_basis(
                leaf_bases[left_mask],
                leaf_bases[right_mask],
                tolerance,
            )
            if core.shape[1]:
                pair_cores.append(core)
                pair_dimension_sum += core.shape[1]
    pair_span = _orthonormal_span(pair_cores, dimension, tolerance)
    left_residual = _projected_basis(left_span, pair_span, tolerance)
    right_residual = _projected_basis(right_span, pair_span, tolerance)
    if left_residual.shape[1] and right_residual.shape[1]:
        singular_values = np.linalg.svd(
            left_residual.conj().T @ right_residual,
            compute_uv=False,
        )
        exact_correlation = float(max(singular_values, default=0.0))
        residual_intersection = int(
            np.sum(singular_values >= 1 - 10 * tolerance)
        )
    else:
        exact_correlation = 0.0
        residual_intersection = 0
    emergent = child_intersection.shape[1] - pair_span.shape[1]

    residual_leaf_bases = {
        mask: _projected_basis(leaf_bases[mask], pair_span, tolerance)
        for mask in (*left_masks, *right_masks)
    }
    ordered_masks = (*left_masks, *right_masks)
    weights = np.zeros((len(ordered_masks), len(ordered_masks)))
    for left_index, left_mask in enumerate(ordered_masks):
        for right_index in range(left_index + 1, len(ordered_masks)):
            right_mask = ordered_masks[right_index]
            left_basis = residual_leaf_bases[left_mask]
            right_basis = residual_leaf_bases[right_mask]
            if left_basis.shape[1] and right_basis.shape[1]:
                weight = float(
                    np.linalg.norm(left_basis.conj().T @ right_basis, ord=2)
                )
                weights[left_index, right_index] = weight
                weights[right_index, left_index] = weight
    bound, left_radius, right_radius = weighted_span_correlation_bound(
        weights,
        tuple(range(len(left_masks))),
        tuple(range(len(left_masks), len(ordered_masks))),
    )
    exact_certified = exact_correlation < 1 - 10 * tolerance
    weighted_certified = bound < 1 - 10 * tolerance
    containment_residual = (
        float(
            np.linalg.norm(
                child_intersection @ child_intersection.conj().T @ pair_span
                - pair_span,
                ord=2,
            )
        )
        if pair_span.shape[1]
        else 0.0
    )
    verified = bool(
        emergent >= 0
        and emergent == residual_intersection
        and containment_residual <= 100 * tolerance
        and exact_certified == (emergent == 0)
        and (not weighted_certified or exact_certified)
    )
    return PairQuotientOverlapControl(
        control_id=control_id,
        n=n,
        target_partition=target,
        labels=labels,
        left_orientation_masks=left_masks,
        right_orientation_masks=right_masks,
        carrier_dimension=dimension,
        left_span_dimension=left_span.shape[1],
        right_span_dimension=right_span.shape[1],
        child_intersection_dimension=child_intersection.shape[1],
        crossing_pair_core_count=len(pair_cores),
        crossing_pair_core_dimension_sum=pair_dimension_sum,
        crossing_pair_core_span_dimension=pair_span.shape[1],
        emergent_cross_dependency_dimension=emergent,
        left_pair_quotient_dimension=left_residual.shape[1],
        right_pair_quotient_dimension=right_residual.shape[1],
        exact_residual_principal_correlation=exact_correlation,
        exact_pair_quotient_gap_below_one=1 - exact_correlation,
        residual_weighted_span_correlation_bound=bound,
        residual_left_weight_spectral_radius=left_radius,
        residual_right_weight_spectral_radius=right_radius,
        residual_sign_blind_bound_certifies_pair_generation=weighted_certified,
        exact_pair_quotient_certifies_pair_generation=exact_certified,
        exact_pair_quotient_overlap_audit=verified,
        status=(
            "exact-pair-quotient-sign-blind-certified"
            if verified and exact_certified and weighted_certified
            else "exact-pair-quotient-phase-only-certified"
            if verified and exact_certified
            else "exact-emergent-cross-dependency"
            if verified
            else "pair-quotient-overlap-audit-failure"
        ),
    )


def _wreath_control(
    control_id: str,
    n: int,
    target: tuple[int, ...],
    labels: tuple[Label, ...],
    left: tuple[int, ...],
    right: tuple[int, ...],
) -> PairQuotientOverlapControl:
    projectors, _, _ = _reduced_projector_family(target, labels, 1e-8)
    return audit_pair_quotient_overlap(
        control_id,
        projectors,
        left,
        right,
        n=n,
        target=target,
        labels=labels,
    )


def _canonical_projectors_from_leaf_gram(
    gram: np.ndarray,
    slices: dict[int, tuple[int, ...]],
    orientation_count: int,
    tolerance: float,
) -> tuple[np.ndarray, ...]:
    values, vectors = np.linalg.eigh((gram + gram.conj().T) / 2)
    if len(values) and values[0] < -100 * tolerance:
        raise ArithmeticError("leaf Gram is not positive semidefinite")
    positive = values > tolerance
    factor = (
        np.sqrt(values[positive])[:, None] * vectors[:, positive].conj().T
    )
    projectors = []
    for mask in range(orientation_count):
        indices = slices.get(mask, ())
        leaf = (
            factor[:, indices]
            if indices
            else np.zeros((factor.shape[0], 0), dtype=complex)
        )
        projectors.append(leaf @ leaf.conj().T)
    return tuple(projectors)


@lru_cache(maxsize=1)
def audit_s6_pair_quotient_portfolio() -> PairQuotientPortfolioScreen:
    labels: tuple[Label, ...] = (
        ((6,), (2, 2, 2)),
        ((5, 1), (2, 1, 1, 1, 1)),
        ((3, 3), (1, 1, 1, 1, 1, 1)),
    )
    records = []
    active_targets = 0
    for target in integer_partitions(6):
        gram, slices = build_orientation_leaf_gram(
            target,
            labels,
            tuple(range(8)),
        )
        if not gram.size:
            continue
        active_targets += 1
        projectors = _canonical_projectors_from_leaf_gram(
            gram,
            slices,
            8,
            1e-8,
        )
        for left, right in unique_affine_flag_merges():
            records.append(
                audit_pair_quotient_overlap(
                    f"W6-PAIR-QUOTIENT-{target}-{left}-{right}",
                    projectors,
                    left,
                    right,
                    n=6,
                    target=target,
                    labels=labels,
                )
            )
    exact = [
        record
        for record in records
        if record.exact_pair_quotient_certifies_pair_generation
    ]
    pair_rich = [
        record for record in exact if record.crossing_pair_core_span_dimension
    ]
    phase_only = [
        record
        for record in exact
        if not record.residual_sign_blind_bound_certifies_pair_generation
    ]
    emergent = [
        record for record in records if record.emergent_cross_dependency_dimension
    ]
    failures = sum(not record.exact_pair_quotient_overlap_audit for record in records)
    return PairQuotientPortfolioScreen(
        screen_id="W6-GLOBALLY-DISTINCT-LOW-CARRIER-PAIR-QUOTIENT",
        n=6,
        labels=labels,
        target_count=len(integer_partitions(6)),
        active_target_count=active_targets,
        affine_merge_audit_count=len(records),
        pair_rich_merge_count=len(pair_rich),
        emergent_cross_dependency_merge_count=len(emergent),
        phase_only_certificate_count=len(phase_only),
        minimum_exact_pair_quotient_gap=min(
            record.exact_pair_quotient_gap_below_one for record in exact
        ),
        minimum_pair_rich_exact_quotient_gap=min(
            record.exact_pair_quotient_gap_below_one for record in pair_rich
        ),
        maximum_exact_residual_principal_correlation=max(
            record.exact_residual_principal_correlation for record in records
        ),
        exact_pair_quotient_audit_failure_count=failures,
        status=(
            "finite-s6-pair-quotient-gap-positive"
            if not failures and not emergent
            else "finite-s6-pair-quotient-emergent-or-audit-failure"
        ),
    )


@lru_cache(maxsize=1)
def _cached_controls() -> tuple[PairQuotientOverlapControl, ...]:
    distinct_w3: tuple[Label, ...] = (
        ((3,), (2, 1)),
        ((3,), (1, 1, 1)),
        ((2, 1), (1, 1, 1)),
    )
    repeated_w3: tuple[Label, ...] = (((3,), (2, 1)),) * 3
    w5_labels = _w5_probe_labels()[0]
    return (
        _wreath_control(
            "W3-DISTINCT-EMERGENT-PAIR-QUOTIENT-BOUNDARY",
            3,
            (2, 1),
            distinct_w3,
            (0, 2),
            (5, 7),
        ),
        _wreath_control(
            "W3-REPEATED-EMERGENT-PAIR-QUOTIENT-BOUNDARY",
            3,
            (2, 1),
            repeated_w3,
            (1, 2),
            (4, 7),
        ),
        _wreath_control(
            "W5-PAIR-RICH-QUOTIENT-CERTIFICATE",
            5,
            (3, 2),
            w5_labels,
            (0, 3),
            (5, 6),
        ),
        _wreath_control(
            "W5-PHASE-ONLY-RESIDUAL-CERTIFICATE",
            5,
            (3, 2),
            w5_labels,
            (0, 1, 4, 5),
            (2, 3, 6, 7),
        ),
    )


def _controls() -> list[PairQuotientOverlapControl]:
    return list(_cached_controls())


def run_pair_quotient_overlap() -> PairQuotientOverlapReport:
    controls = _controls()
    s6_screen = audit_s6_pair_quotient_portfolio()
    distinct, repeated, w5, phase_only_control = controls
    failures = sum(not control.exact_pair_quotient_overlap_audit for control in controls)
    phase_only = sum(
        control.exact_pair_quotient_certifies_pair_generation
        and not control.residual_sign_blind_bound_certifies_pair_generation
        for control in controls
    )
    metrics: dict[str, int | float] = {
        "pair_core_quotient_overlap_theorem_count": 1,
        "finite_control_count": len(controls),
        "finite_pair_quotient_audit_failure_count": failures,
        "finite_phase_only_certificate_count": phase_only,
        "w3_distinct_emergent_dimension": distinct.emergent_cross_dependency_dimension,
        "w3_repeated_emergent_dimension": repeated.emergent_cross_dependency_dimension,
        "w5_pair_quotient_gap": w5.exact_pair_quotient_gap_below_one,
        "w5_phase_only_exact_quotient_gap": phase_only_control.exact_pair_quotient_gap_below_one,
        "w5_phase_only_sign_blind_bound": phase_only_control.residual_weighted_span_correlation_bound,
        "s6_affine_merge_audit_count": s6_screen.affine_merge_audit_count,
        "s6_emergent_cross_dependency_merge_count": s6_screen.emergent_cross_dependency_merge_count,
        "s6_phase_only_certificate_count": s6_screen.phase_only_certificate_count,
        "s6_minimum_exact_pair_quotient_gap": s6_screen.minimum_exact_pair_quotient_gap,
        "all_n_pair_quotient_gap_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return PairQuotientOverlapReport(
        created_at=utc_now(),
        theorem_contract={
            "pair_core_span": "K is the physical span of all crossing leaf-pair intersections.",
            "cross_pair_classes": "After internal child dependencies are quotiented, crossing pair relations generate exactly K.",
            "exact_criterion": "The cross H0 quotient vanishes iff the principal correlation between A minus K and B minus K is strictly below one.",
            "residual_weighted_bound": "Projecting leaves off K and applying the weighted comparison theorem gives a sufficient sign-blind certificate.",
            "scope": "The exact criterion is general finite-dimensional linear algebra; no all-n lower bound or coherent K transform is supplied.",
        },
        controls=controls,
        s6_portfolio_screen=s6_screen,
        proof_obligations=[
            {
                "obligation": "exact_pair_rich_cross_quotient_criterion",
                "resolved": failures == 0,
                "resolution": "Residual principal-correlation-one multiplicity exactly matches the emergent child-intersection dimension.",
            },
            {
                "obligation": "uniform_natural_pair_quotient_gap",
                "resolved": False,
                "resolution": "Finite positive gaps do not bound the minimum residual angle at threshold depth.",
            },
            {
                "obligation": "finite_s6_low_carrier_pair_quotient_screen",
                "resolved": (
                    s6_screen.exact_pair_quotient_audit_failure_count == 0
                    and s6_screen.emergent_cross_dependency_merge_count == 0
                ),
                "resolution": f"All {s6_screen.affine_merge_audit_count} active affine merges have positive exact residual gap; {s6_screen.phase_only_certificate_count} are invisible to the scalar residual bound.",
            },
            {
                "obligation": "coherent_pair_core_span_transform",
                "resolved": False,
                "resolution": "The explicit projector onto K is a validation object, not a polynomial Racah/common-core circuit.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "Quotienting pair cores can be replaced by deleting pairwise unit singular values from a scalar graph.",
                "resolved": True,
                "resolution": "K is a phase-sensitive span with overlapping pair cores; residual leaf normalization changes all blocks.",
            },
            {
                "objection": "A positive finite pair-quotient gap proves all-depth pair generation.",
                "resolved": False,
                "resolution": "The gap may close as node width and multiplicity grow, and its physical mass is unbounded.",
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "exact_pair_core_quotient_overlap_criterion_verified": failures == 0,
            "w3_emergent_boundary_recovered": distinct.emergent_cross_dependency_dimension == 2,
            "selected_w5_pair_rich_node_certified": w5.exact_pair_quotient_certifies_pair_generation,
            "finite_phase_only_residual_certificate_exists": (
                phase_only_control.exact_pair_quotient_certifies_pair_generation
                and not phase_only_control.residual_sign_blind_bound_certifies_pair_generation
            ),
            "finite_s6_pair_quotient_screen_positive": (
                s6_screen.exact_pair_quotient_audit_failure_count == 0
                and s6_screen.emergent_cross_dependency_merge_count == 0
            ),
            "residual_sign_blind_bound_universally_sufficient": False,
            "uniform_all_n_pair_quotient_gap_proved": False,
            "coherent_pair_core_span_transform_compiled": False,
            "speedup_claim_allowed": False,
            "reason": "The exact local norm target is now isolated, but no asymptotic gap or coherent quotient implementation is known.",
        },
        status="exact-pair-quotient-criterion-all-n-gap-open",
        summary=(
            "Reduced pair-rich augmented H0 to the residual principal angle "
            "after removing the physical span of all crossing pair cores."
        ),
        falsifiers_triggered=[
            "Raw pair weights are not invariant under the exact common-core quotient.",
            "Finite pair generation does not imply a uniform residual principal-angle gap.",
        ],
    )


def write_pair_quotient_overlap_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_pair_quotient_overlap())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_pair_quotient_overlap_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
