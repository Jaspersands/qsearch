"""Mixed-arity polar schedule that skips the Gaussian hard-edge scale.

The exact binary polar chain extends to any constant arity.  For child
analyses ``R_i`` with frames ``S_i=R_i*R_i`` and polars ``Q_i``, put

    S_T = sum_i S_i,
    W_T = col_i(S_i^(1/2)) S_T^(-1/2).

Then

    Q_T = (direct_sum_i Q_i) W_T,    W_T*W_T=Pi_supp(S_T). (1)

Thus pairwise common-span pseudoinverse comparability is not a mathematical
prerequisite for polar factorization.  It is one possible implementation of a
binary merge, not the only identity.

There is a separate all-depth issue.  A Gaussian frame with leaf-count aspect
``gamma=w/D`` has nonzero Marchenko--Pastur edges

    (1-sqrt(gamma))^2, (1+sqrt(gamma))^2.                  (2)

A binary dyadic tree necessarily includes the aspects ``c/2`` and ``c``,
where ``c=2^K/|G| in [1,2)``.  From that interval alone its minimum nonzero
edge has no positive uniform lower bound: it approaches zero as ``c`` tends to
either endpoint.

With ``K+2`` copies, use binary merges only through level ``K-2``, one
eight-way merge from level ``K-2`` to ``K+1``, and one final binary merge to
level ``K+2``.  The retained aspect ranges are

    gamma <= 1/2,       2 <= gamma < 4,       4 <= gamma < 8.

Therefore every Gaussian-surrogate node has

    nonzero lower edge >= 3/2-sqrt(2) > 0.0857,
    support condition number <= 17+12sqrt(2) < 34.         (3)

This proves an all-depth Gaussian frame-spectrum schedule with maximum arity
eight.  It does not prove natural-frame spectral edges.  It also does not by
itself compile (1): naive LCU normalization of a width-``w`` leaf sum is
``w``, so a polynomial circuit still needs tightly normalized coherent node
frame/root block encodings or an equivalent recursive access construction.
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


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_multiscale_polar_schedule.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-MULTISCALE-POLAR-SCHEDULE"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
MIXED_SCHEDULE_EDGE_FLOOR = 1.5 - math.sqrt(2.0)
MIXED_SCHEDULE_CONDITION_UPPER = 17.0 + 12.0 * math.sqrt(2.0)


@dataclass(frozen=True)
class MultiwayPolarControl:
    control_id: str
    child_count: int
    physical_dimension: int
    total_coefficient_dimension: int
    parent_support_rank: int
    maximum_child_polar_residual: float
    merge_isometry_residual: float
    recursive_to_direct_polar_residual: float
    exact_multiway_polar_chain_verified: bool
    status: str


@dataclass(frozen=True)
class MultiscaleGaussianScheduleRecord:
    n: int
    group_order_decimal: str
    information_threshold_copy_count: int
    selected_copy_count: int
    threshold_ratio_exact: str
    threshold_ratio: float
    early_terminal_aspect: float
    eight_way_parent_aspect: float
    root_aspect: float
    maximum_merge_arity: int
    retained_level_count: int
    minimum_gaussian_nonzero_edge: float
    maximum_gaussian_support_condition_number: float
    mixed_schedule_edge_floor: float
    mixed_schedule_condition_upper: float
    all_depth_gaussian_frame_edge_verified: bool
    natural_all_depth_frame_edge_proved: bool
    tight_node_frame_block_encoding_proved: bool
    status: str


@dataclass(frozen=True)
class BinaryHardEdgeBoundaryRecord:
    threshold_ratio: float
    below_threshold_aspect: float
    threshold_aspect: float
    below_threshold_nonzero_edge: float
    threshold_nonzero_edge: float
    binary_minimum_edge: float
    interval_uniform_binary_edge_exists: bool
    status: str


@dataclass(frozen=True)
class MultiscalePolarScheduleReport:
    created_at: str
    theorem_contract: dict[str, Any]
    multiway_polar_controls: list[MultiwayPolarControl]
    binary_hard_edge_boundary: list[BinaryHardEdgeBoundaryRecord]
    mixed_schedule_scaling: list[MultiscaleGaussianScheduleRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _psd_root_and_inverse(
    matrix: np.ndarray,
    tolerance: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    values, vectors = np.linalg.eigh((matrix + matrix.conj().T) / 2.0)
    if values[0] < -100 * tolerance:
        raise ValueError("frame must be positive semidefinite")
    positive = values > tolerance
    roots = np.zeros_like(values)
    inverse_roots = np.zeros_like(values)
    roots[positive] = np.sqrt(values[positive])
    inverse_roots[positive] = values[positive] ** -0.5
    root = (vectors * roots) @ vectors.conj().T
    inverse = (vectors * inverse_roots) @ vectors.conj().T
    support = vectors[:, positive] @ vectors[:, positive].conj().T
    return root, inverse, support


def multiway_relative_isometry(
    child_frames: tuple[np.ndarray, ...],
    *,
    tolerance: float = 1e-10,
) -> tuple[np.ndarray, np.ndarray]:
    if not child_frames:
        raise ValueError("at least one child frame is required")
    shape = child_frames[0].shape
    if shape[0] != shape[1] or any(frame.shape != shape for frame in child_frames):
        raise ValueError("all child frames must share one square carrier")
    roots = tuple(_psd_root_and_inverse(frame, tolerance)[0] for frame in child_frames)
    parent = sum(child_frames, np.zeros(shape, dtype=complex))
    _, inverse, support = _psd_root_and_inverse(parent, tolerance)
    return np.vstack(roots) @ inverse, support


def _block_diagonal(matrices: tuple[np.ndarray, ...]) -> np.ndarray:
    rows = sum(matrix.shape[0] for matrix in matrices)
    columns = sum(matrix.shape[1] for matrix in matrices)
    output = np.zeros((rows, columns), dtype=complex)
    row_cursor = 0
    column_cursor = 0
    for matrix in matrices:
        output[
            row_cursor : row_cursor + matrix.shape[0],
            column_cursor : column_cursor + matrix.shape[1],
        ] = matrix
        row_cursor += matrix.shape[0]
        column_cursor += matrix.shape[1]
    return output


def audit_multiway_polar_chain(
    control_id: str,
    child_analyses: tuple[np.ndarray, ...],
    *,
    tolerance: float = 1e-9,
) -> MultiwayPolarControl:
    if not child_analyses:
        raise ValueError("at least one child analysis is required")
    physical_dimension = child_analyses[0].shape[1]
    if any(analysis.shape[1] != physical_dimension for analysis in child_analyses):
        raise ValueError("child analyses must share a physical input")
    child_frames = tuple(analysis.conj().T @ analysis for analysis in child_analyses)
    child_polars: list[np.ndarray] = []
    child_residuals: list[float] = []
    for analysis, frame in zip(child_analyses, child_frames):
        _, inverse, support = _psd_root_and_inverse(frame, tolerance)
        polar = analysis @ inverse
        child_polars.append(polar)
        child_residuals.append(
            float(np.linalg.norm(polar.conj().T @ polar - support, ord=2))
        )
    relative, parent_support = multiway_relative_isometry(
        child_frames,
        tolerance=tolerance,
    )
    recursive = _block_diagonal(tuple(child_polars)) @ relative
    direct_analysis = np.vstack(child_analyses)
    parent_frame = direct_analysis.conj().T @ direct_analysis
    _, parent_inverse, _ = _psd_root_and_inverse(parent_frame, tolerance)
    direct = direct_analysis @ parent_inverse
    merge_residual = float(
        np.linalg.norm(relative.conj().T @ relative - parent_support, ord=2)
    )
    chain_residual = float(np.linalg.norm(recursive - direct, ord=2))
    maximum_child = max(child_residuals, default=0.0)
    verified = bool(
        maximum_child <= 100 * tolerance
        and merge_residual <= 100 * tolerance
        and chain_residual <= 100 * tolerance
    )
    return MultiwayPolarControl(
        control_id=control_id,
        child_count=len(child_analyses),
        physical_dimension=physical_dimension,
        total_coefficient_dimension=sum(row.shape[0] for row in child_analyses),
        parent_support_rank=int(round(np.trace(parent_support).real)),
        maximum_child_polar_residual=maximum_child,
        merge_isometry_residual=merge_residual,
        recursive_to_direct_polar_residual=chain_residual,
        exact_multiway_polar_chain_verified=verified,
        status=(
            "exact-multiway-polar-chain-verified"
            if verified
            else "multiway-polar-chain-control-failure"
        ),
    )


def gaussian_frame_edges(aspect: float) -> tuple[float, float, float]:
    if aspect <= 0 or not math.isfinite(aspect):
        raise ValueError("aspect must be positive")
    root = math.sqrt(aspect)
    lower = (abs(1.0 - root)) ** 2
    upper = (1.0 + root) ** 2
    condition = math.inf if lower == 0.0 else upper / lower
    return lower, upper, condition


def binary_hard_edge_boundary_record(c: float) -> BinaryHardEdgeBoundaryRecord:
    if not 1.0 < c < 2.0:
        raise ValueError("threshold ratio must lie strictly in (1,2)")
    below = c / 2.0
    below_edge = gaussian_frame_edges(below)[0]
    threshold_edge = gaussian_frame_edges(c)[0]
    return BinaryHardEdgeBoundaryRecord(
        threshold_ratio=c,
        below_threshold_aspect=below,
        threshold_aspect=c,
        below_threshold_nonzero_edge=below_edge,
        threshold_nonzero_edge=threshold_edge,
        binary_minimum_edge=min(below_edge, threshold_edge),
        interval_uniform_binary_edge_exists=False,
        status="binary-dyadic-tree-has-no-threshold-interval-uniform-mp-edge",
    )


def multiscale_gaussian_schedule_record(n: int) -> MultiscaleGaussianScheduleRecord:
    if n < 3:
        raise ValueError("n must be at least three")
    order = math.factorial(n)
    threshold = (order - 1).bit_length()
    c = Fraction(1 << threshold, order)
    early = c / 4
    middle = 2 * c
    root = 4 * c
    aspects = [
        Fraction(1 << level, order) for level in range(threshold - 1)
    ] + [middle, root]
    records = [gaussian_frame_edges(float(aspect)) for aspect in aspects]
    minimum_edge = min(row[0] for row in records)
    maximum_condition = max(row[2] for row in records)
    edge_ok = minimum_edge + 1e-13 >= MIXED_SCHEDULE_EDGE_FLOOR
    condition_ok = (
        maximum_condition <= MIXED_SCHEDULE_CONDITION_UPPER + 1e-10
    )
    return MultiscaleGaussianScheduleRecord(
        n=n,
        group_order_decimal=str(order),
        information_threshold_copy_count=threshold,
        selected_copy_count=threshold + 2,
        threshold_ratio_exact=str(c),
        threshold_ratio=float(c),
        early_terminal_aspect=float(early),
        eight_way_parent_aspect=float(middle),
        root_aspect=float(root),
        maximum_merge_arity=8,
        retained_level_count=threshold + 1,
        minimum_gaussian_nonzero_edge=minimum_edge,
        maximum_gaussian_support_condition_number=maximum_condition,
        mixed_schedule_edge_floor=MIXED_SCHEDULE_EDGE_FLOOR,
        mixed_schedule_condition_upper=MIXED_SCHEDULE_CONDITION_UPPER,
        all_depth_gaussian_frame_edge_verified=edge_ok and condition_ok,
        natural_all_depth_frame_edge_proved=False,
        tight_node_frame_block_encoding_proved=False,
        status=(
            "mixed-arity-gaussian-all-depth-edge-certified-access-open"
            if edge_ok and condition_ok
            else "mixed-arity-gaussian-edge-bound-failed"
        ),
    )


def _multiway_controls() -> list[MultiwayPolarControl]:
    rng = np.random.default_rng(20_260_808)
    controls: list[MultiwayPolarControl] = []
    for child_count, physical_dimension, child_rows in ((3, 6, 3), (8, 7, 2)):
        analyses = tuple(
            (
                rng.normal(size=(child_rows, physical_dimension))
                + 1j * rng.normal(size=(child_rows, physical_dimension))
            )
            / math.sqrt(2 * child_rows)
            for _ in range(child_count)
        )
        controls.append(
            audit_multiway_polar_chain(
                f"GAUSSIAN-{child_count}-WAY",
                analyses,
            )
        )
    return controls


def run_multiscale_polar_schedule() -> MultiscalePolarScheduleReport:
    controls = _multiway_controls()
    boundaries = [
        binary_hard_edge_boundary_record(c)
        for c in (1.000001, 1.01, 4 / 3, 1.99, 1.999999)
    ]
    scaling = [
        multiscale_gaussian_schedule_record(n)
        for n in (8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48)
    ]
    control_failures = sum(not row.exact_multiway_polar_chain_verified for row in controls)
    schedule_failures = sum(not row.all_depth_gaussian_frame_edge_verified for row in scaling)
    verified = control_failures == 0 and schedule_failures == 0
    metrics: dict[str, int | float] = {
        "exact_multiway_polar_chain_theorem_count": 1,
        "multiway_control_count": len(controls),
        "multiway_control_failure_count": control_failures,
        "binary_interval_uniform_edge_no_go_theorem_count": 1,
        "mixed_arity_gaussian_all_depth_edge_theorem_count": 1,
        "mixed_schedule_scaling_count": len(scaling),
        "mixed_schedule_failure_count": schedule_failures,
        "maximum_merge_arity": 8,
        "gaussian_all_depth_edge_floor": MIXED_SCHEDULE_EDGE_FLOOR,
        "gaussian_all_depth_condition_upper": MIXED_SCHEDULE_CONDITION_UPPER,
        "natural_all_depth_edge_theorem_count": 0,
        "tight_node_frame_block_encoding_theorem_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return MultiscalePolarScheduleReport(
        created_at=utc_now(),
        theorem_contract={
            "multiway_chain": (
                "For any finite child family, Q_T=(direct_sum Q_i) "
                "col(S_i^1/2)S_T^-1/2 exactly."
            ),
            "binary_hard_edge": (
                "A dyadic tree contains aspects c/2 and c for c in [1,2), "
                "so its Gaussian nonzero edge has no interval-uniform floor."
            ),
            "mixed_arity_schedule": (
                "Binary levels through K-2, one eight-way merge to K+1, and "
                "one binary root merge keep aspects outside (1/2,2)."
            ),
            "gaussian_bounds": (
                "Every retained Gaussian node has edge at least 3/2-sqrt(2) "
                "and support condition number at most 17+12sqrt(2)."
            ),
            "scope": (
                "Natural spectral edges and tightly normalized coherent node "
                "frame/root block encodings remain open."
            ),
        },
        multiway_polar_controls=controls,
        binary_hard_edge_boundary=boundaries,
        mixed_schedule_scaling=scaling,
        proof_obligations=[
            {
                "obligation": "generalize_binary_polar_chain_to_constant_arity",
                "resolved": control_failures == 0,
                "resolution": (
                    "The direct-sum polar identity is exact for arbitrary arity "
                    "and matches rank-deficient three- and eight-way controls."
                ),
            },
            {
                "obligation": "avoid_every_gaussian_mp_hard_edge_across_depth",
                "resolved": schedule_failures == 0,
                "resolution": (
                    "The single eight-way threshold jump skips all node aspects "
                    "between one half and two."
                ),
            },
            {
                "obligation": "prove_natural_all_depth_frame_edges",
                "resolved": False,
                "resolution": (
                    "The independent Plancherel growing-word/local-law theorem "
                    "is still missing."
                ),
            },
            {
                "obligation": "build_tightly_normalized_coherent_node_frame_roots",
                "resolved": False,
                "resolution": (
                    "Naive LCU has width normalization and can erase the "
                    "constant physical spectral gap."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Two extra copies condition every node of the binary tree.",
                "resolved": True,
                "resolution": (
                    "False: the old near-threshold internal nodes remain and "
                    "can approach aspect one."
                ),
            },
            {
                "objection": "Binary shorted-metric comparability is mathematically required for polar factorization.",
                "resolved": True,
                "resolution": (
                    "False as an identity: the exact constant-arity frame-root "
                    "chain bypasses pairwise intersection coordinates."
                ),
            },
            {
                "objection": "Constant physical frame condition numbers imply an efficient block encoding.",
                "resolved": False,
                "resolution": (
                    "A loose LCU normalization can still make the encoded gap "
                    "exponentially small in node width."
                ),
            },
            {
                "objection": "The Gaussian mixed-arity schedule proves a natural polar sampler.",
                "resolved": False,
                "resolution": (
                    "Neither natural edge universality nor coherent tight access is proved."
                ),
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "exact_constant_arity_polar_chain_proved": control_failures == 0,
            "binary_dyadic_gaussian_all_depth_uniform_edge_proved": False,
            "mixed_arity_gaussian_all_depth_uniform_edge_proved": schedule_failures == 0,
            "binary_pairwise_pseudoinverse_comparability_mathematically_mandatory": False,
            "natural_all_depth_frame_edges_proved": False,
            "tight_coherent_node_frame_block_encodings_proved": False,
            "polynomial_hierarchical_polar_sampler_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Mixed arity fixes the Gaussian multiscale hard edge, but the "
                "natural edge theorem and tight recursive access model are open."
            ),
        },
        status=(
            "mixed-arity-gaussian-multiscale-edge-proved-natural-access-open"
            if verified
            else "multiscale-polar-schedule-control-failure"
        ),
        summary=(
            "Generalized the polar chain to constant arity, exposed the binary "
            "threshold hard edge, and proved an eight-way Gaussian schedule "
            "with all-depth constant frame conditioning."
        ),
        falsifiers_triggered=[
            "Top-level K+2 conditioning does not condition every binary internal node.",
            "Pairwise shorted-metric comparability is not intrinsic to the polar chain identity.",
            "Constant physical spectra do not remove block-encoding normalization costs.",
        ],
    )


def write_multiscale_polar_schedule_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_multiscale_polar_schedule())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")
    return payload


if __name__ == "__main__":
    report = write_multiscale_polar_schedule_report()
    print(json.dumps(report, indent=2))
