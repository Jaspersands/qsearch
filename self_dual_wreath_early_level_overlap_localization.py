"""Common-free early-level overlap exclusion for orientation polar trees.

Let ``V_1,...,V_(2m)`` be leaf subspaces with isometries ``U_i``.  Assume no
two leaves have an exact common range and every pairwise principal correlation
is at most ``c``:

    ||U_i^* U_j|| <= c,  i != j.

For one child, the block Gram matrix of ``[U_1 ... U_m]`` has diagonal identity
and off-diagonal block norms at most ``c``.  Block Gershgorin/Schur bounds give

    lambda_min(G_child) >= 1-(m-1)c.

The cross-child block Gram has norm at most ``m c``.  Orthonormalizing both
child spans therefore yields

    ||Pi_L Pi_R||
      <= m c / (1-(m-1)c).                            (1)

For wreath orientation projectors, the exact pair-angle theorem gives
``c<=1/(n-1)`` outside exact common ranges.  Equation (1) becomes

    ||Pi_L Pi_R|| <= m/(n-m).

If ``m<n/2``, this is strictly below one, so the child spans have zero
intersection.  Consequently, through every balanced-tree level with fewer
than ``n/2`` leaves per child, a fractional relative channel cannot emerge
from noncommon correlations alone.  Any such channel must involve an exact
pairwise common range (or violate the pair-angle premise).

This theorem covers only common-free families.  Existing natural portfolios
have proliferating exact common ranges; those must be resolved or quotiented
before applying the bound.  At child width ``Theta(n)`` and above, the bound
becomes vacuous and genuinely many-subspace intersections remain open.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import integer_partitions
from research_registry import utc_now
from self_dual_wreath_collision_free_frame_probe import Label
from self_dual_wreath_orientation_fourier_reduction import (
    orientation_invariant_projector,
)
from self_dual_wreath_orientation_pair_angle_spectrum import (
    _w5_control_labels,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_early_level_overlap_localization.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-EARLY-LEVEL-OVERLAP-LOCALIZATION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class CoherenceBoundControl:
    control_id: str
    leaves_per_child: int
    pairwise_correlation_upper_bound: float
    child_gram_minimum_eigenvalue_lower_bound: float
    cross_child_gram_norm_upper_bound: float
    child_span_correlation_upper_bound: float
    strict_below_one: bool
    exact_child_span_correlation: float
    child_range_intersection_dimension: int
    coherence_bound_verified: bool
    status: str


@dataclass(frozen=True)
class WreathEarlyLevelControl:
    control_id: str
    n: int
    target_partition: tuple[int, ...]
    labels: tuple[Label, ...]
    left_orientation_masks: tuple[int, ...]
    right_orientation_masks: tuple[int, ...]
    active_leaf_count: int
    exact_pairwise_common_range_count: int
    maximum_noncommon_pair_correlation: float
    child_range_intersection_dimension: int
    theorem_premise_common_free: bool
    theorem_predicted_zero_intersection: bool
    exact_common_free_overlap_exclusion_verified: bool
    status: str


@dataclass(frozen=True)
class EarlyLevelScalingRecord:
    n: int
    information_threshold_copy_count: int
    maximum_certified_child_leaf_count: int
    maximum_certified_power_of_two_child_leaf_count: int
    certified_common_free_merge_level_count: int
    total_orientation_tree_depth: int
    certified_level_fraction: float
    common_free_emergent_intersection_excluded: bool
    exact_common_range_resolver_proved: bool
    linear_width_and_larger_overlap_controlled: bool
    status: str


@dataclass(frozen=True)
class EarlyLevelOverlapLocalizationReport:
    created_at: str
    theorem_contract: dict[str, Any]
    synthetic_controls: list[CoherenceBoundControl]
    wreath_controls: list[WreathEarlyLevelControl]
    scaling_records: list[EarlyLevelScalingRecord]
    proof_obligations: list[dict[str, bool | str]]
    adversarial_audit: list[dict[str, bool | str]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def child_span_correlation_bound(
    leaves_per_child: int,
    pairwise_correlation: float,
) -> float:
    if leaves_per_child < 1:
        raise ValueError("leaves per child must be positive")
    if not 0 <= pairwise_correlation < 1:
        raise ValueError("pairwise correlation must lie in [0,1)")
    denominator = 1 - (leaves_per_child - 1) * pairwise_correlation
    if denominator <= 0:
        return math.inf
    return leaves_per_child * pairwise_correlation / denominator


def wreath_child_span_correlation_bound(n: int, leaves_per_child: int) -> float:
    if n < 5:
        raise ValueError("the nontrivial S_n dimension bound starts at n=5")
    return child_span_correlation_bound(leaves_per_child, 1 / (n - 1))


def _span_basis(bases: tuple[np.ndarray, ...], tolerance: float) -> np.ndarray:
    dimension = bases[0].shape[0]
    active = [basis for basis in bases if basis.shape[1]]
    if not active:
        return np.zeros((dimension, 0))
    columns = np.concatenate(active, axis=1)
    left, singular_values, _ = np.linalg.svd(columns, full_matrices=False)
    return left[:, singular_values > tolerance]


def _intersection_dimension(
    left: np.ndarray,
    right: np.ndarray,
    tolerance: float,
) -> tuple[int, float]:
    if not left.shape[1] or not right.shape[1]:
        return 0, 0.0
    correlations = np.linalg.svd(left.conj().T @ right, compute_uv=False)
    return (
        int(np.count_nonzero(correlations >= 1 - tolerance)),
        float(correlations[0] if len(correlations) else 0.0),
    )


def audit_coherence_bound(
    control_id: str,
    left_bases: tuple[np.ndarray, ...],
    right_bases: tuple[np.ndarray, ...],
    *,
    tolerance: float = 1e-9,
) -> CoherenceBoundControl:
    if not left_bases or len(left_bases) != len(right_bases):
        raise ValueError("equal nonempty child leaf families are required")
    all_bases = (*left_bases, *right_bases)
    correlations = []
    for index, left in enumerate(all_bases):
        for right in all_bases[index + 1 :]:
            if not left.shape[1] or not right.shape[1]:
                continue
            singular_values = np.linalg.svd(
                left.conj().T @ right,
                compute_uv=False,
            )
            correlations.append(
                float(singular_values[0] if len(singular_values) else 0.0)
            )
    coherence = max(correlations, default=0.0)
    m = len(left_bases)
    lower = 1 - (m - 1) * coherence
    cross = m * coherence
    bound = child_span_correlation_bound(m, coherence)
    left_span = _span_basis(left_bases, tolerance)
    right_span = _span_basis(right_bases, tolerance)
    intersection, actual = _intersection_dimension(
        left_span,
        right_span,
        100 * tolerance,
    )
    verified = bool(
        actual <= bound + 100 * tolerance
        and (bound >= 1 - 100 * tolerance or intersection == 0)
    )
    return CoherenceBoundControl(
        control_id=control_id,
        leaves_per_child=m,
        pairwise_correlation_upper_bound=coherence,
        child_gram_minimum_eigenvalue_lower_bound=lower,
        cross_child_gram_norm_upper_bound=cross,
        child_span_correlation_upper_bound=bound,
        strict_below_one=bound < 1,
        exact_child_span_correlation=actual,
        child_range_intersection_dimension=intersection,
        coherence_bound_verified=verified,
        status=(
            "coherence-bound-excludes-child-intersection"
            if verified and bound < 1
            else "coherence-bound-verified-vacuous"
            if verified
            else "coherence-bound-validation-failure"
        ),
    )


def _orthonormal_columns(raw: np.ndarray) -> np.ndarray:
    basis, _ = np.linalg.qr(raw)
    return basis


def _synthetic_controls() -> list[CoherenceBoundControl]:
    rng = np.random.default_rng(73021)
    controls = []
    for m, ambient, rank in ((1, 8, 2), (2, 24, 2), (4, 80, 2)):
        bases = tuple(
            _orthonormal_columns(rng.normal(size=(ambient, rank)))
            for _ in range(2 * m)
        )
        controls.append(
            audit_coherence_bound(
                f"gaussian-subspaces-m-{m}",
                bases[:m],
                bases[m:],
            )
        )
    return controls


def _projector_basis(projector: np.ndarray, tolerance: float) -> np.ndarray:
    eigenvalues, eigenvectors = np.linalg.eigh(
        (projector + projector.conj().T) / 2
    )
    return eigenvectors[:, eigenvalues > 1 - tolerance]


def _wreath_control(
    control_id: str,
    n: int,
    target: tuple[int, ...],
    labels: tuple[Label, ...],
    left_masks: tuple[int, ...],
    right_masks: tuple[int, ...],
    tolerance: float = 1e-8,
) -> WreathEarlyLevelControl:
    masks = (*left_masks, *right_masks)
    bases = {
        mask: _projector_basis(
            orientation_invariant_projector(target, labels, mask),
            tolerance,
        )
        for mask in masks
    }
    common_count = 0
    max_noncommon = 0.0
    for left_mask, right_mask in itertools.combinations(masks, 2):
        left = bases[left_mask]
        right = bases[right_mask]
        if not left.shape[1] or not right.shape[1]:
            continue
        correlations = np.linalg.svd(left.conj().T @ right, compute_uv=False)
        common_count += int(
            np.count_nonzero(correlations >= 1 - 100 * tolerance)
        )
        noncommon = correlations[correlations < 1 - 100 * tolerance]
        if len(noncommon):
            max_noncommon = max(max_noncommon, float(noncommon[0]))
    left_span = _span_basis(tuple(bases[mask] for mask in left_masks), tolerance)
    right_span = _span_basis(tuple(bases[mask] for mask in right_masks), tolerance)
    intersection, _ = _intersection_dimension(
        left_span,
        right_span,
        100 * tolerance,
    )
    common_free = common_count == 0
    predicted = common_free and len(left_masks) < n / 2
    verified = bool(not predicted or intersection == 0)
    return WreathEarlyLevelControl(
        control_id=control_id,
        n=n,
        target_partition=target,
        labels=labels,
        left_orientation_masks=left_masks,
        right_orientation_masks=right_masks,
        active_leaf_count=sum(bases[mask].shape[1] > 0 for mask in masks),
        exact_pairwise_common_range_count=common_count,
        maximum_noncommon_pair_correlation=max_noncommon,
        child_range_intersection_dimension=intersection,
        theorem_premise_common_free=common_free,
        theorem_predicted_zero_intersection=predicted,
        exact_common_free_overlap_exclusion_verified=verified,
        status=(
            "common-free-child-intersection-excluded"
            if predicted and verified
            else "exact-common-range-premise-fails"
            if not common_free
            else "finite-control-outside-strict-width-premise"
        ),
    )


def _wreath_controls() -> list[WreathEarlyLevelControl]:
    pairings = (
        ((0, 1), (2, 3)),
        ((0, 2), (1, 3)),
        ((0, 3), (1, 2)),
    )
    controls: list[WreathEarlyLevelControl] = []
    for tuple_index, labels in enumerate(_w5_control_labels()):
        for target in integer_partitions(5):
            if not any(
                float(
                    np.trace(
                        orientation_invariant_projector(target, labels, mask)
                    ).real
                )
                > 1e-8
                for mask in range(4)
            ):
                continue
            for pairing_index, (left, right) in enumerate(pairings):
                controls.append(
                    _wreath_control(
                        (
                            f"W5-{tuple_index}-{'-'.join(map(str, target))}-"
                            f"PAIRING-{pairing_index}"
                        ),
                        5,
                        target,
                        labels,
                        left,
                        right,
                    )
                )
    return controls


def early_level_scaling_record(n: int) -> EarlyLevelScalingRecord:
    if n < 5:
        raise ValueError("n must be at least five")
    copies = math.ceil(math.lgamma(n + 1) / math.log(2))
    maximum = (n - 1) // 2
    power = 1 << (maximum.bit_length() - 1)
    levels = int(math.log2(power)) + 1
    return EarlyLevelScalingRecord(
        n=n,
        information_threshold_copy_count=copies,
        maximum_certified_child_leaf_count=maximum,
        maximum_certified_power_of_two_child_leaf_count=power,
        certified_common_free_merge_level_count=levels,
        total_orientation_tree_depth=copies,
        certified_level_fraction=levels / copies,
        common_free_emergent_intersection_excluded=True,
        exact_common_range_resolver_proved=False,
        linear_width_and_larger_overlap_controlled=False,
        status="common-free-overlap-excluded-through-logarithmic-depth",
    )


def run_early_level_overlap_localization() -> EarlyLevelOverlapLocalizationReport:
    synthetic = _synthetic_controls()
    wreath = _wreath_controls()
    scaling = [
        early_level_scaling_record(n)
        for n in (5, 8, 16, 32, 64, 128, 256, 512)
    ]
    synthetic_failures = sum(not row.coherence_bound_verified for row in synthetic)
    tested_wreath = [row for row in wreath if row.theorem_predicted_zero_intersection]
    wreath_failures = sum(
        not row.exact_common_free_overlap_exclusion_verified
        for row in tested_wreath
    )
    exact_common = [row for row in wreath if not row.theorem_premise_common_free]
    verified = synthetic_failures == wreath_failures == 0 and bool(tested_wreath)
    return EarlyLevelOverlapLocalizationReport(
        created_at=utc_now(),
        theorem_contract={
            "pairwise_premise": (
                "Every distinct leaf pair has zero common range and principal "
                "correlation at most c."
            ),
            "child_gram_bound": "lambda_min(G_child)>=1-(m-1)c.",
            "cross_gram_bound": "||G_LR||<=m c by the block Schur test.",
            "span_correlation_bound": (
                "||Pi_L Pi_R||<=m c/[1-(m-1)c]."
            ),
            "wreath_substitution": (
                "With c=1/(n-1), the bound is m/(n-m), strictly below one "
                "for m<n/2."
            ),
            "polar_consequence": (
                "At common-free early nodes the relative effect has only exact "
                "endpoint channels; no fractional intersection can emerge."
            ),
            "scope": (
                "The theorem is conditional on removing/resolving all exact "
                "pairwise common ranges and becomes vacuous at linear child width."
            ),
        },
        synthetic_controls=synthetic,
        wreath_controls=wreath,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "block_gram_coherence_bound",
                "resolved": verified,
                "resolution": (
                    "Block row-sum bounds control child conditioning and the "
                    "cross Gram; orthonormalization yields equation (1)."
                ),
            },
            {
                "obligation": "wreath_pair_angle_substitution",
                "resolved": True,
                "resolution": (
                    "The exact pair-angle theorem supplies c<=1/(n-1) whenever "
                    "the pair has no exact trivial/sign common range."
                ),
            },
            {
                "obligation": "finite_w5_common_free_controls",
                "resolved": wreath_failures == 0 and bool(tested_wreath),
                "resolution": (
                    "Every applicable curated W5 four-leaf control has zero "
                    "child-span intersection."
                ),
            },
            {
                "obligation": "coherent_exact_common_range_resolver",
                "resolved": False,
                "resolution": (
                    "Natural families have many exact common ranges; no circuit "
                    "yet decomposes all of them before applying the bound."
                ),
            },
            {
                "obligation": "linear_width_overlap_theorem",
                "resolved": False,
                "resolution": (
                    "At m=Theta(n), accumulated noncommon correlations can make "
                    "the coherence bound reach one."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Many small pairwise angles can create an early intersection anyway.",
                "resolved": True,
                "resolution": (
                    "Not before m reaches n/2 under the exact 1/(n-1) pairwise "
                    "bound and the no-common-range premise."
                ),
            },
            {
                "objection": "The theorem handles the natural portfolio directly.",
                "resolved": False,
                "resolution": (
                    "No. Exact common ranges proliferate in the natural scaling "
                    "records, so a common-core resolver is a prerequisite."
                ),
            },
            {
                "objection": "Logarithmic certified depth covers the full k=Theta(n log n) tree.",
                "resolved": False,
                "resolution": (
                    "It covers only the first O(log n) levels. The majority of "
                    "the tree has linear or larger child width."
                ),
            },
            {
                "objection": "Pairwise common generation of every intersection is now proved.",
                "resolved": False,
                "resolution": (
                    "The theorem says emergent intersections require exact common "
                    "ranges at early width; it does not prove those ranges span "
                    "the full child intersection after quotienting."
                ),
            },
        ],
        headline_metrics={
            "common_free_early_overlap_exclusion_theorem_count": 1,
            "block_gram_span_correlation_bound_theorem_count": 1,
            "synthetic_control_count": len(synthetic),
            "synthetic_validation_failure_count": synthetic_failures,
            "w5_control_count": len(wreath),
            "w5_applicable_common_free_control_count": len(tested_wreath),
            "w5_applicable_validation_failure_count": wreath_failures,
            "w5_exact_common_range_control_count": len(exact_common),
            "tail_n": scaling[-1].n,
            "tail_maximum_certified_child_leaf_count": (
                scaling[-1].maximum_certified_child_leaf_count
            ),
            "tail_certified_common_free_merge_level_count": (
                scaling[-1].certified_common_free_merge_level_count
            ),
            "tail_total_orientation_tree_depth": (
                scaling[-1].total_orientation_tree_depth
            ),
            "exact_common_range_resolver_count": 0,
            "linear_width_overlap_theorem_count": 0,
            "global_nonorthogonal_sampler_count": 0,
            "polynomial_hidden_permutation_decoder_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "common_free_emergent_intersections_excluded_below_half_n_width": verified,
            "early_fractional_channels_require_exact_common_ranges": verified,
            "coherent_exact_common_range_resolver_proved": False,
            "linear_and_larger_child_width_controlled": False,
            "all_tree_levels_controlled": False,
            "hierarchical_polar_sampler_polynomial": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Noncommon correlations cannot create early fractional channels, "
                "but exact common ranges are prevalent and widths from Theta(n) "
                "through n! remain uncontrolled."
            ),
        },
        status=(
            "common-free-overlap-excluded-early-common-resolver-open"
            if verified
            else "early-overlap-localization-validation-failure"
        ),
        summary=(
            "Proved that common-free orientation families cannot develop child-"
            "span intersections while each child has fewer than n/2 leaves. "
            "This localizes early fractional channels to exact common ranges; "
            "linear-width overlap and a coherent common-range resolver remain open."
        ),
        falsifiers_triggered=[
            (
                "Do not search for emergent noncommon intersections at constant "
                "or sublinear child width before resolving exact common ranges."
            ),
            (
                "Do not extrapolate the coherence bound beyond m<n/2."
            ),
            (
                "Do not call early-level localization a full sampler without a "
                "coherent common-range decomposition and large-width theorem."
            ),
        ],
    )


def write_early_level_overlap_localization_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_early_level_overlap_localization())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_early_level_overlap_localization_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
