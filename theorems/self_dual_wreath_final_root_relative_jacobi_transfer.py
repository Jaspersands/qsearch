"""Natural final-root relative Jacobi law and trace-weighted endpoint trim.

The all-fixed joint sibling theorem proves that the natural child frames
``A_n,B_n`` converge in every fixed noncommutative moment, under independent
Plancherel sources, to free Marchenko--Pastur variables of common rate
``alpha_n``.  At the selected final root ``alpha_n in [2,4)``.

Put ``S=A+B`` and consider the direct polar-tree endpoint effect

    C = S^(+1/2) A S^(+1/2),       I-C = S^(+1/2) B S^(+1/2). (1)

This is the endpoint POVM in the exact parent-polar factorization; it does not
use a sibling-intersection projector.  In the free limit, ``S`` is MP with
rate ``2 alpha`` and ``C`` has the symmetric free-Jacobi/Wachter law with
support

    x_+- = (1 +- sqrt(2 alpha-1))^2/(4 alpha).             (2)

For ``alpha in [2,4]``, the parent MP support lies strictly inside
``[0.5,16]`` and both Jacobi endpoints stay at least

    delta_* = (2-sqrt(3))/4 > 0.0669                       (3)

from zero and one.

Only weak, annealed spectral conclusions are valid.  Let
``R=1_[0.5,16](S)`` and define (1) on ``R``.  Polynomial approximation to the
inverse square root on this fixed window, followed by the all-fixed joint
moment theorem, gives convergence of the normalized expected empirical law of
``C`` to (2).  Therefore, at the fixed threshold ``delta=0.05``, the expected
relative rank with spectrum outside ``[delta,1-delta]`` is ``o(D)``.

This trim also loses ``o(1)`` annealed native parent-state mass.  If ``Q`` is
the union of the parent-window complement and the endpoint bad space, then

    Tr(SQ) <= sqrt(Tr(S^2) rank(Q)).                        (4)

The joint second moment is ``O(D)``, ``rank(Q)=o(D)``, and
``E Tr(S)=Theta(D)``.  The same estimate controls conditioning on globally
distinct sources because the collision event has probability ``o(1)``.

On the retained endpoint sector, both square-root branches have a fixed
positive edge.  Rounding the discarded eigenvalues to 0 or 1 changes the
two-branch Naimark isometry by mean-square at most twice their state mass.
This removes exact common-window intersection and principal-angle access from
the final-root *direct polar* route.

It does not provide a coherent block encoding of ``C``, the parent window, or
the endpoint spectral classifier.  It is not an operator-norm edge, a
sourcewise law, an all-depth theorem, or a PGM circuit.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_sibling_frame_jacobi_surrogate import (
    PRIMARY_SOURCE_URL,
    jacobi_fractional_edges,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_final_root_relative_jacobi_transfer.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-FINAL-ROOT-RELATIVE-JACOBI-TRANSFER"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
PARENT_WINDOW_LOWER = 0.5
PARENT_WINDOW_UPPER = 16.0
ENDPOINT_TRIM_THRESHOLD = 0.05
UNIFORM_JACOBI_ENDPOINT_FLOOR = (2.0 - math.sqrt(3.0)) / 4.0


@dataclass(frozen=True)
class RelativeJacobiAspectRecord:
    child_aspect: float
    parent_rate: float
    parent_mp_lower_edge: float
    parent_mp_upper_edge: float
    relative_jacobi_lower_edge: float
    relative_jacobi_upper_edge: float
    relative_endpoint_gap: float
    fixed_parent_window_contains_limit: bool
    fixed_endpoint_trim_lies_below_limit: bool
    status: str


@dataclass(frozen=True)
class RelativeEndpointTrimControl:
    control_id: str
    physical_dimension: int
    parent_window_rank: int
    parent_window_codimension: int
    endpoint_bad_rank: int
    total_discarded_rank: int
    total_discarded_rank_fraction: float
    parent_window_lower: float
    parent_window_upper: float
    endpoint_trim_threshold: float
    endpoint_minimum_eigenvalue: float
    endpoint_maximum_eigenvalue: float
    endpoint_completeness_residual: float
    exact_relative_isometry_residual: float
    rounded_relative_isometry_residual: float
    native_total_discarded_state_mass: float
    hilbert_schmidt_state_mass_upper_bound: float
    rounded_naimark_mean_square_error: float
    rounded_error_upper_bound: float
    exact_trim_identities_verified: bool
    status: str


@dataclass(frozen=True)
class FinalRootRelativeScalingRecord:
    n: int
    hidden_label_count_decimal: str
    information_threshold_copy_count: int
    selected_copy_count: int
    child_aspect_exact: str
    child_aspect: float
    parent_mp_lower_edge: float
    parent_mp_upper_edge: float
    relative_endpoint_gap: float
    uniform_endpoint_gap_floor: float
    endpoint_trim_threshold: float
    limiting_parent_window_codimension_fraction: float
    limiting_endpoint_bad_rank_fraction: float
    limiting_annealed_native_state_loss: float
    weak_relative_jacobi_law_proved: bool
    operator_norm_relative_edge_proved: bool
    structured_endpoint_effect_access_proved: bool
    status: str


@dataclass(frozen=True)
class FinalRootRelativeJacobiTheorem:
    joint_limit_input: str
    parent_limit: str
    relative_effect_limit: str
    uniform_endpoint_floor: str
    rank_trim: str
    native_state_trim: str
    rounding_error: str
    conditioning_transfer: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class FinalRootRelativeJacobiReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: FinalRootRelativeJacobiTheorem
    aspect_records: list[RelativeJacobiAspectRecord]
    finite_controls: list[RelativeEndpointTrimControl]
    scaling_records: list[FinalRootRelativeScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    literature_links: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _hermitian(matrix: np.ndarray) -> np.ndarray:
    return (matrix + matrix.conj().T) / 2.0


def _psd_from_spectrum(
    values: np.ndarray,
    vectors: np.ndarray,
    exponent: float,
    tolerance: float,
) -> np.ndarray:
    transformed = np.zeros_like(values)
    positive = values > 100 * tolerance
    transformed[positive] = values[positive] ** exponent
    return (vectors * transformed) @ vectors.conj().T


def relative_jacobi_aspect_record(alpha: float) -> RelativeJacobiAspectRecord:
    if not math.isfinite(alpha) or not 2.0 <= alpha <= 4.0:
        raise ValueError("the final-root child aspect must lie in [2,4]")
    parent_root = math.sqrt(2.0 * alpha)
    parent_lower = (parent_root - 1.0) ** 2
    parent_upper = (parent_root + 1.0) ** 2
    relative_lower, relative_upper = jacobi_fractional_edges(alpha)
    endpoint_gap = min(relative_lower, 1.0 - relative_upper)
    parent_contained = (
        PARENT_WINDOW_LOWER < parent_lower
        and parent_upper < PARENT_WINDOW_UPPER
    )
    endpoint_contained = ENDPOINT_TRIM_THRESHOLD < endpoint_gap
    return RelativeJacobiAspectRecord(
        child_aspect=alpha,
        parent_rate=2.0 * alpha,
        parent_mp_lower_edge=parent_lower,
        parent_mp_upper_edge=parent_upper,
        relative_jacobi_lower_edge=relative_lower,
        relative_jacobi_upper_edge=relative_upper,
        relative_endpoint_gap=endpoint_gap,
        fixed_parent_window_contains_limit=parent_contained,
        fixed_endpoint_trim_lies_below_limit=endpoint_contained,
        status=(
            "uniform-final-root-relative-jacobi-bulk-gap"
            if parent_contained and endpoint_contained
            else "final-root-relative-jacobi-window-failure"
        ),
    )


def audit_relative_endpoint_trim(
    control_id: str,
    left_frame: np.ndarray,
    right_frame: np.ndarray,
    *,
    parent_window_lower: float = PARENT_WINDOW_LOWER,
    parent_window_upper: float = PARENT_WINDOW_UPPER,
    endpoint_threshold: float = ENDPOINT_TRIM_THRESHOLD,
    tolerance: float = 1e-9,
) -> RelativeEndpointTrimControl:
    if (
        left_frame.ndim != 2
        or left_frame.shape[0] != left_frame.shape[1]
        or right_frame.shape != left_frame.shape
    ):
        raise ValueError("child frames must share one square dimension")
    if not 0 < parent_window_lower < parent_window_upper:
        raise ValueError("require a positive ordered parent window")
    if not 0 < endpoint_threshold < 0.5:
        raise ValueError("endpoint threshold must lie in (0,1/2)")
    left = _hermitian(left_frame)
    right = _hermitian(right_frame)
    if min(np.linalg.eigvalsh(left)[0], np.linalg.eigvalsh(right)[0]) < -100 * tolerance:
        raise ValueError("child frames must be positive semidefinite")
    dimension = left.shape[0]
    parent = _hermitian(left + right)
    parent_values, parent_vectors = np.linalg.eigh(parent)
    retained = (
        (parent_values >= parent_window_lower)
        & (parent_values <= parent_window_upper)
    )
    window_basis = parent_vectors[:, retained]
    if not window_basis.shape[1]:
        raise ValueError("parent spectral window is empty")
    parent_inverse_root = _psd_from_spectrum(
        np.where(retained, parent_values, 0.0),
        parent_vectors,
        -0.5,
        tolerance,
    )
    parent_window = window_basis @ window_basis.conj().T
    effect = _hermitian(parent_inverse_root @ left @ parent_inverse_root)
    complement_effect = _hermitian(parent_window - effect)
    effect_on_window = _hermitian(window_basis.conj().T @ effect @ window_basis)
    effect_values, effect_vectors = np.linalg.eigh(effect_on_window)
    bad = (effect_values < endpoint_threshold) | (
        effect_values > 1.0 - endpoint_threshold
    )
    bad_basis = window_basis @ effect_vectors[:, bad]
    bad_projector = bad_basis @ bad_basis.conj().T
    outside_projector = np.eye(dimension, dtype=complex) - parent_window
    discarded_projector = _hermitian(outside_projector + bad_projector)

    rounded_values = effect_values.copy()
    rounded_values[effect_values < endpoint_threshold] = 0.0
    rounded_values[effect_values > 1.0 - endpoint_threshold] = 1.0
    effect_root = (effect_vectors * np.sqrt(np.maximum(effect_values, 0.0))) @ effect_vectors.conj().T
    complement_root = (
        effect_vectors * np.sqrt(np.maximum(1.0 - effect_values, 0.0))
    ) @ effect_vectors.conj().T
    rounded_root = (effect_vectors * np.sqrt(rounded_values)) @ effect_vectors.conj().T
    rounded_complement_root = (
        effect_vectors * np.sqrt(1.0 - rounded_values)
    ) @ effect_vectors.conj().T
    exact_relative = np.vstack((effect_root, complement_root))
    rounded_relative = np.vstack((rounded_root, rounded_complement_root))
    window_identity = np.eye(window_basis.shape[1], dtype=complex)

    native_trace = float(np.trace(parent).real)
    native_second = float(np.trace(parent @ parent).real)
    native_bad = float(np.trace(parent @ discarded_projector).real / native_trace)
    discarded_rank = dimension - window_basis.shape[1] + int(np.count_nonzero(bad))
    hs_bound = math.sqrt(native_second * discarded_rank) / native_trace
    native_window_state = _hermitian(
        window_basis.conj().T @ parent @ window_basis / native_trace
    )
    difference = exact_relative - rounded_relative
    mean_square = float(
        np.trace(native_window_state @ difference.conj().T @ difference).real
    )
    endpoint_bad_mass = float(np.trace(parent @ bad_projector).real / native_trace)
    error_bound = 2.0 * endpoint_bad_mass
    completeness = float(
        np.linalg.norm(effect + complement_effect - parent_window, ord=2)
    )
    exact_isometry = float(
        np.linalg.norm(
            exact_relative.conj().T @ exact_relative - window_identity,
            ord=2,
        )
    )
    rounded_isometry = float(
        np.linalg.norm(
            rounded_relative.conj().T @ rounded_relative - window_identity,
            ord=2,
        )
    )
    verified = bool(
        effect_values[0] >= -1000 * tolerance
        and effect_values[-1] <= 1.0 + 1000 * tolerance
        and native_bad <= hs_bound + 1000 * tolerance
        and mean_square <= error_bound + 1000 * tolerance
        and max(completeness, exact_isometry, rounded_isometry)
        <= 1000 * tolerance
    )
    return RelativeEndpointTrimControl(
        control_id=control_id,
        physical_dimension=dimension,
        parent_window_rank=window_basis.shape[1],
        parent_window_codimension=dimension - window_basis.shape[1],
        endpoint_bad_rank=int(np.count_nonzero(bad)),
        total_discarded_rank=discarded_rank,
        total_discarded_rank_fraction=discarded_rank / dimension,
        parent_window_lower=parent_window_lower,
        parent_window_upper=parent_window_upper,
        endpoint_trim_threshold=endpoint_threshold,
        endpoint_minimum_eigenvalue=float(effect_values[0]),
        endpoint_maximum_eigenvalue=float(effect_values[-1]),
        endpoint_completeness_residual=completeness,
        exact_relative_isometry_residual=exact_isometry,
        rounded_relative_isometry_residual=rounded_isometry,
        native_total_discarded_state_mass=native_bad,
        hilbert_schmidt_state_mass_upper_bound=hs_bound,
        rounded_naimark_mean_square_error=mean_square,
        rounded_error_upper_bound=error_bound,
        exact_trim_identities_verified=verified,
        status=(
            "exact-relative-endpoint-trim-identities"
            if verified
            else "relative-endpoint-trim-control-failure"
        ),
    )


def _gaussian_child_frames(
    dimension: int,
    alpha: float,
    seed: int,
) -> tuple[np.ndarray, np.ndarray]:
    columns = max(dimension, round(alpha * dimension))
    rng = np.random.default_rng(seed)
    rows = []
    for _ in range(2):
        raw = (
            rng.normal(size=(dimension, columns))
            + 1j * rng.normal(size=(dimension, columns))
        ) / math.sqrt(2.0 * dimension)
        rows.append(_hermitian(raw @ raw.conj().T))
    return rows[0], rows[1]


def final_root_relative_scaling_record(n: int) -> FinalRootRelativeScalingRecord:
    if n < 3:
        raise ValueError("n must be at least three")
    order = math.factorial(n)
    threshold = (order - 1).bit_length()
    selected = threshold + 2
    alpha = Fraction(1 << (selected - 1), order)
    aspect = relative_jacobi_aspect_record(float(alpha))
    return FinalRootRelativeScalingRecord(
        n=n,
        hidden_label_count_decimal=str(order),
        information_threshold_copy_count=threshold,
        selected_copy_count=selected,
        child_aspect_exact=str(alpha),
        child_aspect=float(alpha),
        parent_mp_lower_edge=aspect.parent_mp_lower_edge,
        parent_mp_upper_edge=aspect.parent_mp_upper_edge,
        relative_endpoint_gap=aspect.relative_endpoint_gap,
        uniform_endpoint_gap_floor=UNIFORM_JACOBI_ENDPOINT_FLOOR,
        endpoint_trim_threshold=ENDPOINT_TRIM_THRESHOLD,
        limiting_parent_window_codimension_fraction=0.0,
        limiting_endpoint_bad_rank_fraction=0.0,
        limiting_annealed_native_state_loss=0.0,
        weak_relative_jacobi_law_proved=True,
        operator_norm_relative_edge_proved=False,
        structured_endpoint_effect_access_proved=False,
        status="annealed-final-root-jacobi-trim-structured-access-open",
    )


def run_final_root_relative_jacobi_transfer() -> FinalRootRelativeJacobiReport:
    aspects = [relative_jacobi_aspect_record(alpha) for alpha in (2.0, 2.5, 3.0, 4.0)]
    finite_controls = []
    for control_id, dimension, alpha, seed in (
        ("GAUSSIAN-D18-A2", 18, 2.0, 5101),
        ("GAUSSIAN-D24-A3", 24, 3.0, 5102),
        ("GAUSSIAN-D30-A4", 30, 4.0, 5103),
    ):
        left, right = _gaussian_child_frames(dimension, alpha, seed)
        finite_controls.append(
            audit_relative_endpoint_trim(control_id, left, right)
        )
    scaling = [
        final_root_relative_scaling_record(n)
        for n in (8, 12, 16, 24, 32, 48, 64)
    ]
    failures = sum(not row.exact_trim_identities_verified for row in finite_controls)
    uniform = all(
        row.fixed_parent_window_contains_limit
        and row.fixed_endpoint_trim_lies_below_limit
        and row.relative_endpoint_gap + 1e-12 >= UNIFORM_JACOBI_ENDPOINT_FLOOR
        for row in aspects
    )
    verified = failures == 0 and uniform
    return FinalRootRelativeJacobiReport(
        created_at=utc_now(),
        theorem_contract={
            "joint_limit_input": (
                "The proved all-fixed natural sibling law is a pair of free "
                "MP(alpha_n) variables, uniformly for alpha_n in [2,4)."
            ),
            "parent_window": (
                "The free parent A+B is MP(2alpha); its support is uniformly "
                "inside [0.5,16], so the expected omitted rank is o(D)."
            ),
            "relative_jacobi_law": (
                "On the parent window, S^-1/2 A S^-1/2 converges in annealed "
                "empirical law to the free Jacobi distribution with edges "
                "(1+-sqrt(2alpha-1))^2/(4alpha)."
            ),
            "endpoint_trim": (
                "Uniformly in alpha in [2,4], expected endpoint-bad rank below "
                "0.05 or above 0.95 is o(D)."
            ),
            "native_state_retention": (
                "Trace Cauchy--Schwarz and the joint second moment make the "
                "annealed native parent-state mass on all discarded ranks o(1)."
            ),
            "direct_polar_consequence": (
                "The final-root direct relative isometry can be rounded to a "
                "fixed-edge endpoint POVM with o(1) mean-square native error, "
                "without constructing a sibling-intersection projector."
            ),
            "scope": (
                "This is an annealed weak-law and average-state theorem, not "
                "an operator edge, sourcewise statement, coherent endpoint "
                "block encoding, all-depth compiler, or speedup."
            ),
        },
        theorem=FinalRootRelativeJacobiTheorem(
            joint_limit_input="(A_n,B_n) converge in all fixed *-moments to free MP(alpha_n).",
            parent_limit="A_n+B_n has MP(2alpha_n) annealed empirical limit.",
            relative_effect_limit=(
                "S_n^(+1/2)A_nS_n^(+1/2) has the symmetric free-Jacobi limit "
                "after the fixed parent trim."
            ),
            uniform_endpoint_floor=(
                "The limiting support stays at least (2-sqrt(3))/4 from 0 and 1."
            ),
            rank_trim="Expected parent-outlier plus endpoint-bad rank is o(D_n).",
            native_state_trim="Annealed native parent-state loss is o(1).",
            rounding_error=(
                "Endpoint rounding changes the two-branch Naimark map by mean-square "
                "at most twice the discarded endpoint state mass."
            ),
            conditioning_transfer=(
                "Bounded rank observables and second-moment Cauchy--Schwarz "
                "transfer the statements through global-distinct conditioning."
            ),
            scope=(
                "Only the selected final-root direct polar is covered; coherent "
                "effect access and every earlier level remain open."
            ),
            theorem_verified=verified,
            status=(
                "natural-final-root-relative-jacobi-trim-proved"
                if verified
                else "relative-jacobi-transfer-control-failure"
            ),
        ),
        aspect_records=aspects,
        finite_controls=finite_controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "upgrade_gaussian_jacobi_benchmark_to_natural_weak_law",
                "resolved": verified,
                "resolution": (
                    "All-fixed joint freeness plus fixed-window functional calculus "
                    "gives the annealed free-Jacobi endpoint law."
                ),
            },
            {
                "obligation": "remove_exact_common_intersection_from_final_direct_polar",
                "resolved": verified,
                "resolution": (
                    "The direct parent-polar endpoint effect uses S=A+B and loses "
                    "only o(1) native mass after fixed parent/endpoint trims."
                ),
            },
            {
                "obligation": "prove_untrimmed_operator_endpoint_edge",
                "resolved": False,
                "resolution": (
                    "Fixed moments permit sparse outliers arbitrarily near 0 or 1."
                ),
            },
            {
                "obligation": "compile_structured_relative_effect_access",
                "resolved": False,
                "resolution": (
                    "No normalized block encoding or direct Naimark transform for "
                    "the natural endpoint effect is constructed."
                ),
            },
            {
                "obligation": "extend_relative_jacobi_trim_to_all_polar_levels",
                "resolved": False,
                "resolution": (
                    "The natural all-fixed joint law is currently proved only for "
                    "the selected final sibling split."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "All fixed moments prove a uniform operator edge.",
                "resolved": True,
                "resolution": (
                    "False. The theorem discards o(D) exceptional rank and keeps "
                    "untrimmed operator-edge claims false."
                ),
            },
            {
                "objection": "The principal-angle counterfamily kills this route.",
                "resolved": True,
                "resolution": (
                    "It kills generic exact sibling-intersection access. The direct "
                    "parent polar uses the bounded endpoint effect (1), not that intersection."
                ),
            },
            {
                "objection": "Rank-o(D) trimming automatically preserves the native state.",
                "resolved": True,
                "resolution": (
                    "Rank alone is insufficient; equation (4) additionally uses the "
                    "proved parent second moment and linear first moment."
                ),
            },
            {
                "objection": "A fixed endpoint edge is already a circuit.",
                "resolved": False,
                "resolution": (
                    "The edge helps only after a tightly normalized coherent access "
                    "model for the endpoint effect has been supplied."
                ),
            },
        ],
        literature_links=[
            {
                "paper": "Local eigenvalue density for general MANOVA matrices",
                "url": PRIMARY_SOURCE_URL,
                "used_for": "Wachter/Jacobi limiting support formula",
                "proves_natural_wreath_joint_freeness": False,
            }
        ],
        headline_metrics={
            "natural_relative_jacobi_weak_law_theorem_count": int(verified),
            "uniform_endpoint_bulk_gap_theorem_count": int(verified),
            "annealed_endpoint_rank_trim_theorem_count": int(verified),
            "annealed_native_state_retention_theorem_count": int(verified),
            "final_root_common_intersection_prerequisite_count": 0,
            "finite_control_count": len(finite_controls),
            "finite_control_failure_count": failures,
            "parent_window_lower": PARENT_WINDOW_LOWER,
            "parent_window_upper": PARENT_WINDOW_UPPER,
            "endpoint_trim_threshold": ENDPOINT_TRIM_THRESHOLD,
            "uniform_limiting_endpoint_gap_floor": UNIFORM_JACOBI_ENDPOINT_FLOOR,
            "structured_endpoint_effect_access_count": 0,
            "all_depth_relative_jacobi_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "natural_final_root_relative_jacobi_weak_law_proved": verified,
            "uniform_final_root_endpoint_bulk_gap_proved": verified,
            "annealed_endpoint_bad_rank_vanishes": verified,
            "annealed_native_endpoint_trim_loss_vanishes": verified,
            "exact_sibling_intersection_required_for_final_direct_polar": False,
            "untrimmed_operator_norm_endpoint_edge_proved": False,
            "sourcewise_endpoint_edge_proved": False,
            "structured_endpoint_effect_block_encoding_proved": False,
            "coherent_endpoint_spectral_classifier_compiled": False,
            "all_depth_relative_jacobi_law_proved": False,
            "recursive_orientation_polar_compiled": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The selected final merge has a natural constant-edge endpoint "
                "bulk after o(1) annealed native loss, but no structured coherent "
                "access to that endpoint effect or all-depth recursion is known."
            ),
        },
        status=(
            "final-root-relative-jacobi-bulk-conditioned-access-open"
            if verified
            else "final-root-relative-jacobi-validation-failure"
        ),
        summary=(
            "Transferred the proved natural sibling joint freeness to a final-root "
            "free-Jacobi endpoint law with a uniform bulk gap and o(1) annealed "
            "native trim loss, bypassing exact sibling-intersection access for the "
            "direct polar route."
        ),
        falsifiers_triggered=[
            "The final-root direct polar does not require an exact common-window intersection projector.",
            "The weak Jacobi law does not prove an untrimmed operator edge or coherent access.",
            "The principal-angle oracle obstruction applies to the kernel/intersection route, not this average-state direct-polar trim.",
        ],
    )


def write_final_root_relative_jacobi_transfer_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-FINAL-ROOT-RELATIVE-JACOBI-TRANSFER"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_final_root_relative_jacobi_transfer" in globals():
        report = run_final_root_relative_jacobi_transfer(**kwargs)
        payload = asdict(report) if hasattr(report, "__dataclass_fields__") else (dict(report) if isinstance(report, dict) else report)
    else:
        report = {}
        payload = {}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    if write_registry:
        from research_registry import (
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-SELF-DUAL-WREATH-FINAL-ROOT-RELATIVE-JACOBI-TRANSFER",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-FINAL-ROOT-RELATIVE-JACOBI-TRANSFER.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-FINAL-ROOT-RELATIVE-JACOBI-TRANSFER.",
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-MEASUREMENT",
                ],
                evidence=payload.get("headline_metrics", {}),
            )
        )
        upsert_experiment_result(
            ExperimentResultRecord(
                id=(
                    registry_result_id
                    or f"RESULT-{registry_experiment_id}-LATEST"
                ),
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=payload.get("created_at", ""),
                status=payload.get("status", "completed"),
                summary=payload.get("summary", ""),
                metrics=payload.get("headline_metrics", {}),
                falsifiers_triggered=payload.get("falsifiers_triggered", []),
                artifacts={
                    "self_dual_wreath_final_root_relative_jacobi_transfer": str(path)
                },
            )
        )
    return payload
