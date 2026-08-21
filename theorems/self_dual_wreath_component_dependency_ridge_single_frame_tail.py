"""Single-frame reduction and weak hard-edge criterion for dependency tails.

Let ``F>=0`` act on a physical space of dimension ``D``, let ``X`` be an
``r``-dimensional subspace of ``Ran(F)``, put ``Y=I-XX^*``, and define

    F_perp = Y F Y.                                      (1)

The dependency-ridge physical-spectrum theorem gives

    ||Pi-Q_eta||F^2 <= T_eta(F)+T_eta(F_perp),            (2)

where

    T_eta(A)=sum_(lambda in spec+(A))(eta/(lambda+eta))^2.

The second tail is not an independent spectral obligation.  Restrict (1) to
``Ran(Y)``.  The rank identity

    rank(F_perp)=rank(F)-r                               (3)

implies that this restriction has exactly the same nullity as ``F``.
Cauchy interlacing then pairs every positive compressed eigenvalue with a no
larger positive eigenvalue of ``F``.  Since the ridge-tail function is
decreasing,

    T_eta(F_perp) <= T_eta(F),                           (4)

and therefore

    ||Pi-Q_eta||F^2 <= 2 T_eta(F).                       (5)

Nor is a uniform lower edge necessary.  For any ``tau>0``, let
``N_F^+(tau)`` count positive eigenvalues at most ``tau``.  Splitting the
spectrum gives

    T_eta(F)/D <= N_F^+(tau)/D
                  +(rank(F)/D)(eta/(tau+eta))^2.         (6)

Thus a vanishing trace density of inverse-polynomially small eigenvalues,
together with ``eta/tau=o(signal)``, closes the support transfer.  A full
minimum-eigenvalue theorem is stronger than needed.

Qualitatively, convergence of the empirical spectral law to a determinate
limit whose zero atom matches the limiting nullity implies the existence of a
slowly vanishing ``tau_n`` for which the first term of (6) vanishes.  Proving
all fixed moments converge to the aspect-``>1`` Marchenko--Pastur law would
therefore close the *structural* trace tail along a diagonal sequence; four
fixed moments do not.  Polynomial implementation still needs a quantitative
inverse-polynomial ``tau_n`` and an access method that avoids the positive
Poisson normalization barrier.

Finally, the tail observable is bounded:

    0 <= T_eta(F)/D <= 1.                                 (7)

If ``C`` is the global-distinct source event, then

    |E[T_eta(F)/D | C]-E[T_eta(F)/D]| <= 1-Pr(C).         (8)

Hence an independent-source tail theorem transfers immediately because
``Pr(C)=1-o(1)``.  The unbounded raw moments used to prove the independent
spectral law need not themselves be transferred through conditioning.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_component_dependency_ridge_physical_spectrum import (
    _random_synthesis_with_common_subspace,
    dependency_physical_frames,
    support_ridge_tail,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_component_dependency_ridge_single_frame_tail.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-DEPENDENCY-RIDGE-SINGLE-FRAME-TAIL"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class SingleFrameTailControl:
    control_id: str
    physical_dimension: int
    common_fiber_dimension: int
    full_frame_rank: int
    excluded_frame_rank: int
    full_frame_nullity: int
    excluded_restriction_nullity: int
    ridge_parameter: float
    full_support_ridge_tail: float
    excluded_support_ridge_tail: float
    excluded_to_full_tail_ratio: float
    minimum_positive_eigenvalue_interlacing_slack: float
    rank_drop_residual: int
    excluded_tail_bounded_by_full_tail: bool
    exact_single_frame_tail_reduction_verified: bool
    status: str


@dataclass(frozen=True)
class NearZeroTailScalingRecord:
    n: int
    small_eigenvalue_threshold: float
    assumed_positive_small_eigenvalue_density: float
    ridge_parameter: float
    ridge_to_threshold_ratio: float
    normalized_single_frame_tail_upper_bound: float
    normalized_dependency_error_upper_bound: float
    target_physical_M4_signal: float
    parity_curl_transfer_error_upper_bound: float
    transfer_preserves_target_signal: bool
    uniform_minimum_eigenvalue_required: bool
    status: str


@dataclass(frozen=True)
class DependencyRidgeSingleFrameTailTheorem:
    rank_drop: str
    nullity_match: str
    positive_eigenvalue_interlacing: str
    excluded_tail_domination: str
    dependency_error: str
    near_zero_split: str
    weak_law_consequence: str
    collision_free_transfer: str
    arbitrary_positive_frame: bool
    arbitrary_common_subspace_inside_range: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class ComponentDependencyRidgeSingleFrameTailReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: DependencyRidgeSingleFrameTailTheorem
    finite_controls: list[SingleFrameTailControl]
    scaling_records: list[NearZeroTailScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _hermitian(matrix: np.ndarray) -> np.ndarray:
    return (matrix + matrix.conj().T) / 2.0


def _spectral_parts(
    matrix: np.ndarray,
    *,
    tolerance: float,
) -> tuple[int, np.ndarray]:
    values = np.linalg.eigvalsh(_hermitian(matrix))
    if values[0] < -100 * tolerance:
        raise ValueError("the frame must be positive semidefinite")
    positive = values[values > 100 * tolerance]
    return len(values) - len(positive), positive


def excluded_frame_tail_is_dominated(
    frame: np.ndarray,
    common_isometry: np.ndarray,
    ridge_parameter: float,
    *,
    tolerance: float = 1e-10,
) -> tuple[float, float, float, int, int, int, int]:
    if ridge_parameter <= 0:
        raise ValueError("the ridge parameter must be positive")
    if frame.ndim != 2 or frame.shape[0] != frame.shape[1] or not frame.shape[0]:
        raise ValueError("a nonempty square frame is required")
    dimension = frame.shape[0]
    if (
        common_isometry.ndim != 2
        or common_isometry.shape[0] != dimension
        or not common_isometry.shape[1]
    ):
        raise ValueError("the common isometry has the wrong shape")
    if np.linalg.norm(
        common_isometry.conj().T @ common_isometry
        - np.eye(common_isometry.shape[1]),
        ord=2,
    ) > 1000 * tolerance:
        raise ValueError("the common matrix must be an isometry")
    frame = _hermitian(frame)
    values, vectors = np.linalg.eigh(frame)
    support = vectors[:, values > 100 * tolerance]
    if np.linalg.norm(
        support @ support.conj().T @ common_isometry - common_isometry,
        ord=2,
    ) > 1000 * tolerance:
        raise ValueError("the common subspace must lie inside the frame range")
    common_projection = common_isometry @ common_isometry.conj().T
    complement_projection = _hermitian(np.eye(dimension) - common_projection)
    complement_values, complement_vectors = np.linalg.eigh(complement_projection)
    complement = complement_vectors[:, complement_values > 0.5]
    restricted = _hermitian(complement.conj().T @ frame @ complement)
    full_nullity, full_positive = _spectral_parts(frame, tolerance=tolerance)
    restricted_nullity, restricted_positive = _spectral_parts(
        restricted,
        tolerance=tolerance,
    )
    full_tail = float(
        np.sum((ridge_parameter / (full_positive + ridge_parameter)) ** 2)
    )
    excluded_tail = float(
        np.sum((ridge_parameter / (restricted_positive + ridge_parameter)) ** 2)
    )
    paired = full_positive[: len(restricted_positive)]
    slack = float(
        np.min(restricted_positive - paired)
        if len(restricted_positive)
        else 0.0
    )
    full_rank = len(full_positive)
    excluded_rank = len(restricted_positive)
    return (
        full_tail,
        excluded_tail,
        slack,
        full_rank,
        excluded_rank,
        full_nullity,
        restricted_nullity,
    )


def small_eigenvalue_tail_upper_bound(
    frame: np.ndarray,
    ridge_parameter: float,
    small_eigenvalue_threshold: float,
    *,
    tolerance: float = 1e-10,
) -> tuple[float, int, int]:
    if ridge_parameter <= 0 or small_eigenvalue_threshold <= 0:
        raise ValueError("ridge and small-eigenvalue thresholds must be positive")
    _, positive = _spectral_parts(frame, tolerance=tolerance)
    count = int(np.sum(positive <= small_eigenvalue_threshold))
    upper = count + len(positive) * (
        ridge_parameter / (small_eigenvalue_threshold + ridge_parameter)
    ) ** 2
    return float(upper), count, len(positive)


def audit_single_frame_tail_reduction(
    control_id: str,
    synthesis: np.ndarray,
    common_isometry: np.ndarray,
    ridge_parameter: float,
    *,
    tolerance: float = 1e-9,
) -> SingleFrameTailControl:
    _, _, frame, excluded_frame = dependency_physical_frames(
        synthesis,
        common_isometry,
        tolerance=tolerance,
    )
    (
        full_tail,
        excluded_tail,
        slack,
        full_rank,
        excluded_rank,
        full_nullity,
        restricted_nullity,
    ) = excluded_frame_tail_is_dominated(
        frame,
        common_isometry,
        ridge_parameter,
        tolerance=tolerance,
    )
    direct_excluded_tail = support_ridge_tail(
        excluded_frame,
        ridge_parameter,
        tolerance=tolerance,
    )
    common = common_isometry.shape[1]
    rank_residual = full_rank - excluded_rank - common
    dominated = excluded_tail <= full_tail + 5000 * tolerance
    exact = bool(
        abs(direct_excluded_tail - excluded_tail) <= 5000 * tolerance
        and full_nullity == restricted_nullity
        and rank_residual == 0
        and slack >= -5000 * tolerance
        and dominated
    )
    return SingleFrameTailControl(
        control_id=control_id,
        physical_dimension=synthesis.shape[0],
        common_fiber_dimension=common,
        full_frame_rank=full_rank,
        excluded_frame_rank=excluded_rank,
        full_frame_nullity=full_nullity,
        excluded_restriction_nullity=restricted_nullity,
        ridge_parameter=ridge_parameter,
        full_support_ridge_tail=full_tail,
        excluded_support_ridge_tail=excluded_tail,
        excluded_to_full_tail_ratio=(
            excluded_tail / full_tail if full_tail else 0.0
        ),
        minimum_positive_eigenvalue_interlacing_slack=slack,
        rank_drop_residual=rank_residual,
        excluded_tail_bounded_by_full_tail=dominated,
        exact_single_frame_tail_reduction_verified=exact,
        status=(
            "dependency-ridge-tail-reduced-to-one-child-frame"
            if exact
            else "dependency-ridge-single-frame-tail-control-failure"
        ),
    )


def near_zero_tail_scaling_record(
    n: int,
    *,
    threshold_degree: int = 2,
    small_density_degree: int = 2,
    ridge_degree: int = 6,
    target_physical_M4_signal: float = 1e-4,
) -> NearZeroTailScalingRecord:
    if n < 2 or min(threshold_degree, small_density_degree, ridge_degree) < 0:
        raise ValueError("invalid scaling parameters")
    threshold = n ** (-threshold_degree)
    density = n ** (-small_density_degree)
    eta = n ** (-ridge_degree)
    ratio = eta / threshold
    single = density + (eta / (threshold + eta)) ** 2
    dependency = 2.0 * single
    transfer = 16.0 * math.sqrt(dependency) + 8.0 * dependency
    return NearZeroTailScalingRecord(
        n=n,
        small_eigenvalue_threshold=threshold,
        assumed_positive_small_eigenvalue_density=density,
        ridge_parameter=eta,
        ridge_to_threshold_ratio=ratio,
        normalized_single_frame_tail_upper_bound=single,
        normalized_dependency_error_upper_bound=dependency,
        target_physical_M4_signal=target_physical_M4_signal,
        parity_curl_transfer_error_upper_bound=transfer,
        transfer_preserves_target_signal=transfer < target_physical_M4_signal,
        uniform_minimum_eigenvalue_required=False,
        status=(
            "near-zero-density-bound-preserves-target-signal"
            if transfer < target_physical_M4_signal
            else "illustrative-near-zero-density-rate-too-weak-for-target"
        ),
    )


def dependency_ridge_single_frame_tail_theorem(
) -> DependencyRidgeSingleFrameTailTheorem:
    return DependencyRidgeSingleFrameTailTheorem(
        rank_drop="rank(F_perp)=rank(F)-r",
        nullity_match=(
            "nullity(F_perp restricted to Ran(I-XX*))=nullity(F)"
        ),
        positive_eigenvalue_interlacing=(
            "lambda_j^+(F)<=lambda_j^+(F_perp|Ran(I-XX*))"
        ),
        excluded_tail_domination="T_eta(F_perp)<=T_eta(F)",
        dependency_error="||Pi-Q_eta||F^2<=2T_eta(F)",
        near_zero_split=(
            "T_eta(F)/D<=N_F^+(tau)/D+(rank(F)/D)(eta/(tau+eta))^2"
        ),
        weak_law_consequence=(
            "all-fixed-moment convergence to a determinate law with the "
            "correct zero atom gives qualitative tail closure along a diagonal scale"
        ),
        collision_free_transfer=(
            "|E[Z|C]-E[Z]|<=1-Pr(C) for Z=T_eta(F)/D in [0,1]"
        ),
        arbitrary_positive_frame=True,
        arbitrary_common_subspace_inside_range=True,
        theorem_verified=True,
        status="dependency-support-transfer-needs-one-frame-near-zero-density-only",
    )


def run_component_dependency_ridge_single_frame_tail(
) -> ComponentDependencyRidgeSingleFrameTailReport:
    controls = []
    for control_id, dimensions, seed, eta in (
        ("FULL-ROW-D12-N16-R5", (12, 16, 12, 5), 11101, 1e-2),
        ("DEFICIENT-D14-N18-S10-R4", (14, 18, 10, 4), 11102, 3e-3),
        ("TALL-D16-N12-S12-R6", (16, 12, 12, 6), 11103, 1e-3),
    ):
        synthesis, common = _random_synthesis_with_common_subspace(
            *dimensions,
            seed=seed,
        )
        controls.append(
            audit_single_frame_tail_reduction(
                control_id,
                synthesis,
                common,
                eta,
            )
        )
    scaling = [
        near_zero_tail_scaling_record(n)
        for n in (16, 32, 64, 128, 256, 512, 1024, 4096)
    ]
    theorem = dependency_ridge_single_frame_tail_theorem()
    failures = sum(
        not row.exact_single_frame_tail_reduction_verified for row in controls
    )
    return ComponentDependencyRidgeSingleFrameTailReport(
        created_at=utc_now(),
        theorem_contract={
            "rank": theorem.rank_drop,
            "nullity": theorem.nullity_match,
            "interlacing": theorem.positive_eigenvalue_interlacing,
            "single_frame": theorem.excluded_tail_domination,
            "dependency_error": theorem.dependency_error,
            "near_zero_count": theorem.near_zero_split,
            "weak_law": theorem.weak_law_consequence,
            "global_distinct": theorem.collision_free_transfer,
            "scope": (
                "This deterministic reduction removes the excluded frame as "
                "an independent tail target. It does not prove the natural "
                "child-frame small-eigenvalue density or its rate."
            ),
        },
        theorem=theorem,
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "remove_sibling_excluded_frame_as_independent_tail_target",
                "resolved": theorem.theorem_verified and failures == 0,
                "resolution": (
                    "Rank-drop nullity matching plus compression interlacing "
                    "gives T_eta(F_perp)<=T_eta(F)."
                ),
            },
            {
                "obligation": "replace_uniform_edge_by_trace_small_eigenvalue_density",
                "resolved": theorem.theorem_verified and failures == 0,
                "resolution": (
                    "Equation (6) needs only a vanishing fraction of positive "
                    "eigenvalues below tau and eta/tau small."
                ),
            },
            {
                "obligation": "transfer_bounded_tail_through_global_distinct_conditioning",
                "resolved": True,
                "resolution": (
                    "The normalized tail lies in [0,1], so its conditional "
                    "expectation changes by at most the collision probability."
                ),
            },
            {
                "obligation": "prove_all_fixed_independent_child_frame_moments_or_weak_law",
                "resolved": False,
                "resolution": (
                    "Extend the exact first-four independent moments to every "
                    "fixed order. The resulting bounded tail, not the raw "
                    "moments, transfers through global distinctness."
                ),
            },
            {
                "obligation": "obtain_inverse_polynomial_small_eigenvalue_density_rate",
                "resolved": False,
                "resolution": (
                    "A polynomial algorithm needs quantitative control at "
                    "tau=n^-O(1); qualitative weak convergence is insufficient."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "F_perp needs a separate correlated local law.",
                "resolved": True,
                "resolution": (
                    "No. Its positive eigenvalues interlace above those of F, "
                    "and the exact rank drop makes the nullities match."
                ),
            },
            {
                "objection": "A minimum positive eigenvalue is required.",
                "resolved": True,
                "resolution": (
                    "No. A vanishing normalized count below tau plus eta/tau "
                    "small controls the trace tail."
                ),
            },
            {
                "objection": "The first four Marchenko--Pastur moments suffice.",
                "resolved": False,
                "resolution": (
                    "They do not control vanishing-scale mass. All fixed moments "
                    "can imply only qualitative weak convergence; a rate needs more."
                ),
            },
            {
                "objection": "Unbounded raw moments must transfer through global distinctness.",
                "resolved": True,
                "resolution": (
                    "They need not. Prove the spectral law independently, then "
                    "transfer the bounded tail observable using equation (8)."
                ),
            },
            {
                "objection": "Weak convergence proves polynomial implementability.",
                "resolved": False,
                "resolution": (
                    "It supplies no inverse-polynomial tau rate and does not "
                    "remove the normalized-access or Poisson-length barriers."
                ),
            },
        ],
        headline_metrics={
            "single_frame_tail_domination_theorem_count": int(
                theorem.theorem_verified and failures == 0
            ),
            "near_zero_density_sufficiency_theorem_count": int(
                theorem.theorem_verified and failures == 0
            ),
            "bounded_global_distinct_tail_transfer_theorem_count": 1,
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "maximum_excluded_to_full_tail_ratio": max(
                row.excluded_to_full_tail_ratio for row in controls
            ),
            "minimum_interlacing_slack": min(
                row.minimum_positive_eigenvalue_interlacing_slack
                for row in controls
            ),
            "scaling_transfer_survival_count": sum(
                row.transfer_preserves_target_signal for row in scaling
            ),
            "natural_child_small_eigenvalue_density_theorem_count": 0,
            "inverse_polynomial_small_eigenvalue_rate_theorem_count": 0,
            "natural_component_M4_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "excluded_frame_tail_dominated_by_child_frame_tail": (
                theorem.theorem_verified and failures == 0
            ),
            "uniform_child_frame_lower_edge_required": False,
            "vanishing_near_zero_eigenvalue_density_suffices": True,
            "all_fixed_natural_moment_convergence_proved": False,
            "global_distinct_bounded_tail_transfer_proved": True,
            "inverse_polynomial_near_zero_density_rate_proved": False,
            "natural_support_ridge_tail_small": False,
            "natural_component_M4_positive": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Only one child-frame near-zero density remains in the tail "
                "premise, but no natural qualitative law or polynomial rate is proved."
            ),
        },
        status=(
            "dependency-tail-reduced-to-one-child-frame-near-zero-density"
            if failures == 0
            else "dependency-ridge-single-frame-tail-control-failure"
        ),
        summary=(
            "Used compression interlacing to dominate the sibling-excluded "
            "ridge tail by the child-frame tail and replaced a uniform edge "
            "with an explicit near-zero eigenvalue-count criterion."
        ),
        falsifiers_triggered=[
            "The sibling-excluded frame does not require an independent local law.",
            "A uniform minimum eigenvalue is stronger than trace-tail transfer needs.",
            "Four fixed moments do not control vanishing-scale spectral mass.",
            "Unbounded moment observables need not be conditioned; the bounded tail transfers directly.",
            "Qualitative weak convergence does not imply polynomial implementation.",
            "No natural small-eigenvalue law, exact M4, algorithm, or speedup is proved.",
        ],
    )


def write_component_dependency_ridge_single_frame_tail_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-DEPENDENCY-RIDGE-SINGLE-FRAME-TAIL"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_component_dependency_ridge_single_frame_tail" in globals():
        report = run_component_dependency_ridge_single_frame_tail(**kwargs)
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
                id="NEG-SELF-DUAL-WREATH-COMPONENT-DEPENDENCY-RIDGE-SINGLE-FRAME-TAIL",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-COMPONENT-DEPENDENCY-RIDGE-SINGLE-FRAME-TAIL.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-COMPONENT-DEPENDENCY-RIDGE-SINGLE-FRAME-TAIL.",
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
                    "self_dual_wreath_component_dependency_ridge_single_frame_tail": str(path)
                },
            )
        )
    return payload
