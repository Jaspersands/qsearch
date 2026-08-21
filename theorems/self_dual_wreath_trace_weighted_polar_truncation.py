"""Trace-weighted polar truncation removes the natural hard-edge gate.

The orientation research path has demanded a uniform lower edge for every
natural node frame.  That is stronger than an average-success PGM needs.

Let ``R:H->K`` be an analysis operator, ``S=R^*R``, and ``Q=RS^(-1/2)`` its
support polar.  For ``tau>0`` define the truncated polar

    Q_tau = R f_tau(S),
    f_tau(lambda)=lambda^(-1/2) 1_{lambda>=tau}.           (1)

On the native frame state ``rho_S=S/tr(S)``, the exact squared polar error is

    tr((Q-Q_tau)^*(Q-Q_tau) rho_S)
      = tr(S 1_{0<S<tau})/tr(S).                          (2)

Every orientation node frame is a sum of orthogonal projectors,
``S=sum_e P_e``.  Therefore

    rank(S) <= sum_e rank(P_e) = tr(S),                   (3)

and (2) is at most ``tau`` for every fixed source block and target.  No
Plancherel averaging, global-distinct transfer, central-support bound, or
minimum-positive-eigenvalue theorem is required.

The statement composes.  At any level of a polar tree, the node leaf sets
partition the full orientation family.  The exact intermediate frame state
has node diagonal block ``S_T/tr(S_root)``.  Hence the total discarded frame
mass at that level is at most ``tau``.  Replacing each level by a coherent
failure-flagged truncated polar changes the average output state by trace
distance at most ``sqrt(2 tau)``.  A hybrid argument over ``L`` levels gives

    output trace distance <= L sqrt(2 tau).               (4)

Taking ``tau=epsilon^2/(2L^2)`` keeps total error at most ``epsilon``.  Since
``L=Theta(log |S_n|)=poly(n)``, the retained singular-value threshold
``sqrt(tau)=epsilon/(sqrt(2)L)`` is inverse polynomial.

This removes natural all-block hard-edge control as a prerequisite for
constant *average* hidden-label success.  It does not construct the required
tightly normalized node-analysis block encoding.  A naive width-normalized
LCU still makes the encoded singular threshold exponentially small.  It also
does not prove worst-case conditional-branch success.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_pgm_success_theorem import pgm_success_lower_bound


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_trace_weighted_polar_truncation.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-TRACE-WEIGHTED-POLAR-TRUNCATION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
POLAR_QSVT_URL = "https://arxiv.org/abs/2106.07634"


@dataclass(frozen=True)
class TraceWeightedPolarControl:
    control_id: str
    physical_dimension: int
    projector_count: int
    total_projector_rank: int
    frame_rank: int
    frame_trace: float
    minimum_positive_frame_eigenvalue: float
    truncation_threshold: float
    low_positive_eigenvalue_count: int
    exact_discarded_frame_mass: float
    universal_discarded_frame_mass_upper_bound: float
    exact_weighted_polar_error: float
    weighted_error_identity_residual: float
    exact_polar_support_residual: float
    truncated_polar_support_residual: float
    hard_lower_edge_exists_at_threshold: bool
    trace_weighted_bound_verified: bool
    status: str


@dataclass(frozen=True)
class PolarTreeTruncationControl:
    control_id: str
    physical_dimension: int
    leaf_count: int
    nontrivial_level_count: int
    truncation_threshold: float
    maximum_level_discarded_frame_mass: float
    sum_level_discarded_frame_mass: float
    sum_level_trace_distance_upper_bound: float
    theorem_trace_distance_upper_bound: float
    every_level_mass_bound_respected: bool
    coherent_hybrid_bound_respected: bool
    status: str


@dataclass(frozen=True)
class TraceWeightedPolarScalingRecord:
    n: int
    group_order_decimal: str
    selected_copy_count: int
    binary_polar_tree_depth: int
    target_total_trace_distance_error: float
    per_level_frame_eigenvalue_threshold: float
    retained_analysis_singular_value_threshold: float
    unit_normalized_inverse_singular_threshold_cost: float
    certified_total_trace_distance_upper_bound: float
    information_theoretic_pgm_success_lower_bound: float
    truncated_pgm_success_lower_bound: float
    pointwise_source_block_bound: bool
    collision_free_event_transfer_required: bool
    natural_hard_lower_edge_required: bool
    center_valued_local_law_required_for_average_success: bool
    tightly_normalized_node_analysis_encoding_proved: bool
    polynomial_truncated_polar_sampler_proved: bool
    status: str


@dataclass(frozen=True)
class TraceWeightedPolarTruncationReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_polar_controls: list[TraceWeightedPolarControl]
    finite_tree_controls: list[PolarTreeTruncationControl]
    scaling_records: list[TraceWeightedPolarScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    literature_links: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _orthogonal_projector(basis: np.ndarray) -> np.ndarray:
    if basis.ndim != 2:
        raise ValueError("basis must be a matrix")
    if basis.shape[1] and np.linalg.norm(
        basis.conj().T @ basis - np.eye(basis.shape[1]), ord=2
    ) > 1e-9:
        raise ValueError("basis columns must be orthonormal")
    return basis @ basis.conj().T


def _spectral_data(
    frame: np.ndarray,
    threshold: float,
    tolerance: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    hermitian = (frame + frame.conj().T) / 2
    values, vectors = np.linalg.eigh(hermitian)
    if values[0] < -100 * tolerance:
        raise ValueError("frame is not positive semidefinite")
    positive = values > tolerance
    retained = values >= threshold
    inverse = np.zeros_like(values)
    truncated_inverse = np.zeros_like(values)
    inverse[positive] = values[positive] ** -0.5
    truncated_inverse[retained] = values[retained] ** -0.5
    support = vectors[:, positive] @ vectors[:, positive].conj().T
    retained_support = vectors[:, retained] @ vectors[:, retained].conj().T
    inverse_root = (vectors * inverse) @ vectors.conj().T
    truncated_inverse_root = (vectors * truncated_inverse) @ vectors.conj().T
    return values, support, retained_support, inverse_root, truncated_inverse_root


def audit_trace_weighted_polar(
    control_id: str,
    projectors: tuple[np.ndarray, ...],
    threshold: float,
    *,
    tolerance: float = 1e-10,
) -> TraceWeightedPolarControl:
    if not projectors or threshold <= tolerance:
        raise ValueError("need projectors and a positive threshold")
    dimension = projectors[0].shape[0]
    if any(projector.shape != (dimension, dimension) for projector in projectors):
        raise ValueError("projectors must share one square carrier")
    if any(
        np.linalg.norm(projector @ projector - projector, ord=2) > 100 * tolerance
        for projector in projectors
    ):
        raise ValueError("inputs must be orthogonal projectors")
    frame = sum(projectors, np.zeros_like(projectors[0]))
    analysis = np.vstack(projectors)
    values, support, retained_support, inverse, truncated_inverse = _spectral_data(
        frame, threshold, tolerance
    )
    polar = analysis @ inverse
    truncated = analysis @ truncated_inverse
    trace = float(np.trace(frame).real)
    if trace <= tolerance:
        raise ValueError("the frame must have positive trace")
    low = (values > tolerance) & (values < threshold)
    discarded = float(np.sum(values[low]) / trace)
    difference = polar - truncated
    weighted_error = float(
        np.trace(difference.conj().T @ difference @ frame).real / trace
    )
    frame_rank = int(np.count_nonzero(values > tolerance))
    total_rank = int(round(sum(np.trace(projector).real for projector in projectors)))
    universal = threshold * frame_rank / trace
    exact_support_residual = float(
        np.linalg.norm(polar.conj().T @ polar - support, ord=2)
    )
    truncated_support_residual = float(
        np.linalg.norm(
            truncated.conj().T @ truncated - retained_support,
            ord=2,
        )
    )
    identity_residual = abs(weighted_error - discarded)
    verified = bool(
        frame_rank <= total_rank
        and total_rank == round(trace)
        and discarded <= universal + 100 * tolerance
        and universal <= threshold + 100 * tolerance
        and identity_residual <= 100 * tolerance
        and exact_support_residual <= 100 * tolerance
        and truncated_support_residual <= 100 * tolerance
    )
    positive_values = values[values > tolerance]
    minimum = float(positive_values[0])
    return TraceWeightedPolarControl(
        control_id=control_id,
        physical_dimension=dimension,
        projector_count=len(projectors),
        total_projector_rank=total_rank,
        frame_rank=frame_rank,
        frame_trace=trace,
        minimum_positive_frame_eigenvalue=minimum,
        truncation_threshold=threshold,
        low_positive_eigenvalue_count=int(np.count_nonzero(low)),
        exact_discarded_frame_mass=discarded,
        universal_discarded_frame_mass_upper_bound=universal,
        exact_weighted_polar_error=weighted_error,
        weighted_error_identity_residual=identity_residual,
        exact_polar_support_residual=exact_support_residual,
        truncated_polar_support_residual=truncated_support_residual,
        hard_lower_edge_exists_at_threshold=minimum >= threshold,
        trace_weighted_bound_verified=verified,
        status=(
            "trace-weighted-polar-truncation-bound-verified"
            if verified
            else "trace-weighted-polar-truncation-control-failure"
        ),
    )


def frame_truncation_mass(
    frame: np.ndarray,
    threshold: float,
    *,
    tolerance: float = 1e-10,
) -> float:
    values = np.linalg.eigvalsh((frame + frame.conj().T) / 2)
    if values[0] < -100 * tolerance:
        raise ValueError("frame is not positive semidefinite")
    trace = float(np.sum(values))
    if trace <= tolerance:
        return 0.0
    low = (values > tolerance) & (values < threshold)
    return float(np.sum(values[low]) / trace)


def audit_polar_tree_truncation(
    control_id: str,
    leaf_projectors: tuple[np.ndarray, ...],
    threshold: float,
) -> PolarTreeTruncationControl:
    leaf_count = len(leaf_projectors)
    if leaf_count < 2 or leaf_count & (leaf_count - 1):
        raise ValueError("a power-of-two leaf family is required")
    dimension = leaf_projectors[0].shape[0]
    if any(projector.shape != (dimension, dimension) for projector in leaf_projectors):
        raise ValueError("leaf projectors must share one carrier")
    root = sum(leaf_projectors, np.zeros_like(leaf_projectors[0]))
    root_trace = float(np.trace(root).real)
    if root_trace <= 0:
        raise ValueError("root frame has zero trace")
    level_losses = []
    width = 2
    while width <= leaf_count:
        loss = 0.0
        for start in range(0, leaf_count, width):
            frame = sum(
                leaf_projectors[start : start + width],
                np.zeros_like(leaf_projectors[0]),
            )
            values = np.linalg.eigvalsh((frame + frame.conj().T) / 2)
            low = (values > 1e-10) & (values < threshold)
            loss += float(np.sum(values[low])) / root_trace
        level_losses.append(loss)
        width *= 2
    trace_bound = sum(math.sqrt(2 * loss) for loss in level_losses)
    theorem_bound = len(level_losses) * math.sqrt(2 * threshold)
    mass_ok = all(loss <= threshold + 1e-9 for loss in level_losses)
    hybrid_ok = trace_bound <= theorem_bound + 1e-9
    return PolarTreeTruncationControl(
        control_id=control_id,
        physical_dimension=dimension,
        leaf_count=leaf_count,
        nontrivial_level_count=len(level_losses),
        truncation_threshold=threshold,
        maximum_level_discarded_frame_mass=max(level_losses, default=0.0),
        sum_level_discarded_frame_mass=sum(level_losses),
        sum_level_trace_distance_upper_bound=trace_bound,
        theorem_trace_distance_upper_bound=theorem_bound,
        every_level_mass_bound_respected=mass_ok,
        coherent_hybrid_bound_respected=hybrid_ok,
        status=(
            "polar-tree-truncation-hybrid-bound-verified"
            if mass_ok and hybrid_ok
            else "polar-tree-truncation-control-failure"
        ),
    )


def trace_weighted_polar_scaling_record(
    n: int,
    *,
    target_total_trace_distance_error: float = 0.01,
) -> TraceWeightedPolarScalingRecord:
    if n < 3 or not 0 < target_total_trace_distance_error < 1:
        raise ValueError("invalid n or target error")
    order = math.factorial(n)
    copies = (order - 1).bit_length() + 2
    levels = copies
    epsilon = target_total_trace_distance_error
    threshold = epsilon * epsilon / (2 * levels * levels)
    singular_threshold = math.sqrt(threshold)
    condition = 1 / singular_threshold
    exact_success = pgm_success_lower_bound(order, copies)
    return TraceWeightedPolarScalingRecord(
        n=n,
        group_order_decimal=str(order),
        selected_copy_count=copies,
        binary_polar_tree_depth=levels,
        target_total_trace_distance_error=epsilon,
        per_level_frame_eigenvalue_threshold=threshold,
        retained_analysis_singular_value_threshold=singular_threshold,
        unit_normalized_inverse_singular_threshold_cost=condition,
        certified_total_trace_distance_upper_bound=(
            levels * math.sqrt(2 * threshold)
        ),
        information_theoretic_pgm_success_lower_bound=exact_success,
        truncated_pgm_success_lower_bound=max(0.0, exact_success - epsilon),
        pointwise_source_block_bound=True,
        collision_free_event_transfer_required=False,
        natural_hard_lower_edge_required=False,
        center_valued_local_law_required_for_average_success=False,
        tightly_normalized_node_analysis_encoding_proved=False,
        polynomial_truncated_polar_sampler_proved=False,
        status="inverse-polynomial-truncation-threshold-tight-access-open",
    )


def _finite_controls() -> tuple[
    list[TraceWeightedPolarControl],
    list[PolarTreeTruncationControl],
]:
    e0 = np.asarray([[1.0], [0.0], [0.0]])
    angle = 1e-3
    near = np.asarray([[math.cos(angle)], [math.sin(angle)], [0.0]])
    hard_edge = audit_trace_weighted_polar(
        "NEAR-COINCIDENT-LINES-NO-HARD-EDGE",
        (_orthogonal_projector(e0), _orthogonal_projector(near)),
        threshold=1e-5,
    )

    rng = np.random.default_rng(20_260_808)
    random_projectors = []
    for _ in range(7):
        basis, _ = np.linalg.qr(rng.normal(size=(9, 3)), mode="reduced")
        random_projectors.append(_orthogonal_projector(basis))
    random_control = audit_trace_weighted_polar(
        "RANDOM-Q9-SEVEN-RANK3-PROJECTORS",
        tuple(random_projectors),
        threshold=0.2,
    )

    tree_leaves = []
    for index in range(8):
        theta = (index // 2) * 0.7 + (index % 2) * 1e-3
        vector = np.asarray(
            [[math.cos(theta)], [math.sin(theta)], [0.0], [0.0]]
        )
        tree_leaves.append(_orthogonal_projector(vector))
    tree = audit_polar_tree_truncation(
        "EIGHT-LEAF-NEAR-DEPENDENT-BINARY-TREE",
        tuple(tree_leaves),
        threshold=1e-5,
    )
    return [hard_edge, random_control], [tree]


def run_trace_weighted_polar_truncation(
) -> TraceWeightedPolarTruncationReport:
    polar_controls, tree_controls = _finite_controls()
    scaling = [
        trace_weighted_polar_scaling_record(n)
        for n in (8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48)
    ]
    failures = sum(
        not row.trace_weighted_bound_verified for row in polar_controls
    ) + sum(
        not row.every_level_mass_bound_respected
        or not row.coherent_hybrid_bound_respected
        for row in tree_controls
    )
    hard_edge_counter = polar_controls[0]
    tail = scaling[-1]
    verified = failures == 0 and not hard_edge_counter.hard_lower_edge_exists_at_threshold
    return TraceWeightedPolarTruncationReport(
        created_at=utc_now(),
        theorem_contract={
            "single_node_weighted_error": (
                "For Q_tau=R f_tau(R^*R), the native-frame mean-square polar "
                "error is exactly tr(S 1_(0,tau)(S))/tr(S)."
            ),
            "projector_sum_bound": (
                "If S is a sum of projectors, rank(S)<=tr(S), so discarded "
                "native frame mass is at most tau pointwise in every source block."
            ),
            "level_budget": (
                "At each polar-tree level, node frames partition the root leaf "
                "sum, so total discarded frame mass is at most tau."
            ),
            "coherent_hybrid": (
                "Failure-flagged truncation changes the average output by at "
                "most sqrt(2 tau) per level and L sqrt(2 tau) in total."
            ),
            "inverse_polynomial_cutoff": (
                "tau=epsilon^2/(2L^2) gives total error epsilon and retained "
                "analysis singular values at least epsilon/(sqrt(2)L)."
            ),
            "scope": (
                "The theorem is average-state and pointwise in source labels. "
                "It does not construct a tightly normalized node analysis, "
                "prove worst-case branch success, or finish the decoder."
            ),
        },
        finite_polar_controls=polar_controls,
        finite_tree_controls=tree_controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "replace_uniform_hard_edge_by_trace_weighted_truncation",
                "resolved": verified,
                "resolution": (
                    "Spectral calculus gives the exact native-frame loss, and "
                    "rank(sum P_e)<=sum rank(P_e)=tr(sum P_e) bounds it by tau."
                ),
            },
            {
                "obligation": "compose_truncation_through_the_polar_tree",
                "resolved": verified,
                "resolution": (
                    "Node frames partition leaf traces at every level; a "
                    "failure-flagged channel hybrid gives L sqrt(2 tau)."
                ),
            },
            {
                "obligation": "build_tightly_normalized_node_analysis_block_encoding",
                "resolved": False,
                "resolution": (
                    "Naive SELECT/PREP over a width-w node normalizes the "
                    "analysis by sqrt(w), which would erase the polynomial cutoff."
                ),
            },
            {
                "obligation": "compile_end_to_end_truncated_pgm_decoder",
                "resolved": False,
                "resolution": (
                    "Need tight node access, controlled failure propagation, "
                    "and the existing physical Fourier output transform."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "A single arbitrarily small positive eigenvalue forces factorial PGM cost.",
                "resolved": True,
                "resolution": (
                    "The near-coincident-line control has no edge at the chosen "
                    "threshold, yet its exact native-frame loss obeys the tau bound."
                ),
            },
            {
                "objection": "Many bad source blocks invalidate scalar truncation mass.",
                "resolved": True,
                "resolution": (
                    "The bound is deterministic inside every fixed source block; "
                    "no scalar-to-central-support conversion is used."
                ),
            },
            {
                "objection": "Per-node loss tau can be union-bounded over exponentially many nodes.",
                "resolved": True,
                "resolution": (
                    "Nodes at one level are weighted by their frame traces, "
                    "which sum to the root trace. The cost is per level, not per node."
                ),
            },
            {
                "objection": "Inverse-polynomial cutoff already gives a polynomial circuit.",
                "resolved": False,
                "resolution": (
                    "Only under a polynomially normalized node-analysis block "
                    "encoding. The current generic encoding has exponential width normalization."
                ),
            },
            {
                "objection": "Average-success truncation proves every measured source branch succeeds.",
                "resolved": False,
                "resolution": (
                    "The theorem preserves the natural average hidden-label "
                    "success criterion, not worst-case conditional branches."
                ),
            },
        ],
        literature_links=[
            {
                "paper": "Fast algorithm for quantum polar decomposition, pretty-good measurements, and the Procrustes problem",
                "url": POLAR_QSVT_URL,
                "used_for": "QSVT polar implementation context",
                "closes_tight_node_access_gate": False,
            }
        ],
        headline_metrics={
            "trace_weighted_polar_truncation_theorem_count": int(verified),
            "pointwise_source_block_low_mass_theorem_count": int(verified),
            "polar_tree_level_budget_theorem_count": int(verified),
            "finite_polar_control_count": len(polar_controls),
            "finite_tree_control_count": len(tree_controls),
            "finite_control_failure_count": failures,
            "hard_edge_countercontrol_count": int(
                not hard_edge_counter.hard_lower_edge_exists_at_threshold
            ),
            "scaling_row_count": len(scaling),
            "tail_n": tail.n,
            "tail_copy_count": tail.selected_copy_count,
            "tail_frame_eigenvalue_threshold": (
                tail.per_level_frame_eigenvalue_threshold
            ),
            "tail_inverse_singular_threshold_cost": (
                tail.unit_normalized_inverse_singular_threshold_cost
            ),
            "tail_truncated_pgm_success_lower_bound": (
                tail.truncated_pgm_success_lower_bound
            ),
            "natural_hard_edge_prerequisite_count": 0,
            "center_valued_local_law_prerequisite_count": 0,
            "tight_node_analysis_encoding_theorem_count": 0,
            "polynomial_truncated_polar_sampler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "pointwise_trace_weighted_truncation_bound_proved": verified,
            "coherent_polar_tree_average_error_bound_proved": verified,
            "inverse_polynomial_frame_cutoff_suffices_for_average_success": verified,
            "natural_uniform_hard_lower_edge_is_required": False,
            "center_valued_bad_block_local_law_is_required_for_average_success": False,
            "global_distinct_event_union_bound_is_required_for_truncation": False,
            "worst_case_conditional_branch_success_proved": False,
            "tightly_normalized_node_analysis_block_encoding_proved": False,
            "polynomial_hierarchical_polar_sampler_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Trace-weighted truncation reduces spectral resolution to an "
                "inverse-polynomial cutoff without a hard-edge theorem, but "
                "the node analysis still lacks a polynomial normalization."
            ),
        },
        status=(
            "trace-weighted-hard-edge-bypass-proved-tight-node-access-open"
            if verified
            else "trace-weighted-polar-truncation-control-failure"
        ),
        summary=(
            "Proved that inverse-polynomial trace-weighted truncation preserves "
            "average PGM success through the full polar tree even when natural "
            "node frames have arbitrarily small positive eigenvalues."
        ),
        falsifiers_triggered=[
            "A uniform natural minimum-positive frame edge is not necessary for average PGM success.",
            "Central support of tiny-eigenvalue blocks is not the relevant truncation observable.",
            "The polar-tree truncation budget scales with depth, not the exponential node count.",
            "Tight coherent node normalization remains necessary; truncation does not fix naive LCU width cost.",
        ],
    )


def write_trace_weighted_polar_truncation_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-TRACE-WEIGHTED-POLAR-TRUNCATION"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_trace_weighted_polar_truncation())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    return payload


if __name__ == "__main__":
    report = write_trace_weighted_polar_truncation_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
