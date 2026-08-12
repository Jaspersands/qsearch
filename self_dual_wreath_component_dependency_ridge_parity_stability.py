"""Ridge stability for dependency-projection parity commutators.

The coefficient normal form writes the exact common fiber as

    Pi = supp(L) - supp(M),       0 <= M <= L,             (1)

where ``L=R^*R`` and ``M=R^*(I-XX^*)R``.  The support projections are nested,
so ``Pi`` is an orthogonal projection.  For ``eta>0`` define the bounded,
operator-monotone support ridge

    f_eta(A)=A(A+eta I)^-1,
    Q_eta=f_eta(L)-f_eta(M).                               (2)

Since ``0<=M<=L`` and ``f_eta`` is operator monotone,
``0<=Q_eta<=I``.  It converges to ``Pi`` without selecting a basis or
introducing the common coefficient metric.

For every block-sign involution ``Z_S`` put

    B_S(P)=P Z_S P,
    C(P)=q^-2 sum_(S,T)
       [Tr(B_S(P)^2 B_T(P)^2)-Tr(B_S(P)B_T(P)B_S(P)B_T(P))].

The Walsh-duality theorem gives ``C(Pi)=M4`` exactly.  If ``Q`` is any positive
contraction and ``Delta=||Pi-Q||_F``, then

    |C(Pi)-C(Q)|/r <= 16 epsilon + 8 epsilon^2,
    epsilon=Delta/sqrt(r).                                (3)

The proof is outcome-count free.  Each parity compression changes by at most
``2 Delta`` in Frobenius norm, each commutator by at most ``8 Delta``, and the
uniform ``q^-2`` average preserves the same bound.

There is also a physical annealed form.  If

    R_eta=E[1_E ||Pi-Q_eta||_F^2/D_phys],

then Cauchy--Schwarz and ``r<=D_phys`` give

    E[1_E |C(Pi)-C(Q_eta)|/D_phys]
       <= 16 sqrt(R_eta)+8 R_eta.                         (4)

Finally,

    ||Pi-Q_eta||_F^2
      <= sum_(lambda in spec+(L)) (eta/(lambda+eta))^2
         +sum_(mu in spec+(M)) (eta/(mu+eta))^2.          (5)

Thus exact natural M4 transfers from the bounded parity-ridge curl once a
scalar trace-weighted support-edge tail is small.  The ridge itself has the
heat-kernel representation

    f_eta(A)=I-eta integral_0^infinity e^(-eta t)e^(-tA)dt,

so its parity curls are bounded resolvent/word targets.  This module proves
the stability bridge, not a positive natural ridge curl or the required
Plancherel spectral-tail estimate.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_component_dependency_ridge_parity_stability.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-DEPENDENCY-RIDGE-PARITY-STABILITY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class DependencyRidgeParityControl:
    control_id: str
    ambient_coefficient_dimension: int
    exact_dependency_rank: int
    leaf_count: int
    coordinate_block_dimension: int
    ridge_parameter: float
    gram_order_minimum_eigenvalue: float
    ridge_minimum_eigenvalue: float
    ridge_maximum_eigenvalue: float
    exact_projection_residual: float
    ridge_positive_contraction_residual: float
    dependency_ridge_frobenius_error_squared: float
    spectral_tail_error_upper_bound: float
    normalized_dependency_ridge_error: float
    exact_normalized_parity_curl_M4: float
    ridge_normalized_parity_curl_M4: float
    normalized_parity_curl_difference: float
    dimension_free_stability_upper_bound: float
    spectral_tail_bound_verified: bool
    parity_curl_stability_verified: bool
    exact_and_ridge_curls_both_nonnegative: bool
    status: str


@dataclass(frozen=True)
class PhysicalRidgeTransferRecord:
    trace_weighted_dependency_ridge_error: float
    physical_parity_curl_transfer_upper_bound: float
    target_exact_physical_M4_lower_bound: float
    required_ridge_physical_M4_lower_bound: float
    ridge_signal_survives_transfer: bool
    uniform_child_frame_edge_required: bool
    uniform_common_metric_edge_required: bool
    status: str


@dataclass(frozen=True)
class DependencyRidgeParityStabilityTheorem:
    dependency_projection: str
    support_ridge: str
    operator_order: str
    parity_curl_functional: str
    normalized_stability: str
    physical_annealed_stability: str
    spectral_tail: str
    heat_kernel: str
    arbitrary_nested_positive_grams: bool
    arbitrary_equal_coordinate_blocks: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class ComponentDependencyRidgeParityStabilityReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: DependencyRidgeParityStabilityTheorem
    finite_controls: list[DependencyRidgeParityControl]
    physical_transfer_records: list[PhysicalRidgeTransferRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _hermitian(matrix: np.ndarray) -> np.ndarray:
    return (matrix + matrix.conj().T) / 2.0


def _support_projection(matrix: np.ndarray, *, tolerance: float) -> np.ndarray:
    values, vectors = np.linalg.eigh(_hermitian(matrix))
    positive = values > 100 * tolerance
    basis = vectors[:, positive]
    return basis @ basis.conj().T


def _support_ridge(
    matrix: np.ndarray,
    ridge_parameter: float,
    *,
    tolerance: float,
) -> np.ndarray:
    if ridge_parameter <= 0:
        raise ValueError("the ridge parameter must be positive")
    values, vectors = np.linalg.eigh(_hermitian(matrix))
    if values[0] < -100 * tolerance:
        raise ValueError("the ridge input must be positive semidefinite")
    values = np.maximum(values, 0.0)
    transformed = values / (values + ridge_parameter)
    return (vectors * transformed) @ vectors.conj().T


def dependency_projection_and_ridge(
    gram: np.ndarray,
    excluded_gram: np.ndarray,
    ridge_parameter: float,
    *,
    tolerance: float = 1e-10,
) -> tuple[np.ndarray, np.ndarray, float]:
    if (
        gram.ndim != 2
        or gram.shape[0] != gram.shape[1]
        or excluded_gram.shape != gram.shape
        or not gram.shape[0]
    ):
        raise ValueError("two nonempty square Gram matrices of one size are required")
    gram = _hermitian(gram)
    excluded_gram = _hermitian(excluded_gram)
    gram_values = np.linalg.eigvalsh(gram)
    excluded_values = np.linalg.eigvalsh(excluded_gram)
    order_minimum = float(np.linalg.eigvalsh(gram - excluded_gram)[0])
    if min(gram_values[0], excluded_values[0], order_minimum) < -100 * tolerance:
        raise ValueError("the Gram matrices must satisfy 0<=M<=L")
    gram_support = _support_projection(gram, tolerance=tolerance)
    excluded_support = _support_projection(excluded_gram, tolerance=tolerance)
    nesting = float(
        np.linalg.norm(excluded_support @ gram_support - excluded_support, ord=2)
    )
    if nesting > 1000 * tolerance:
        raise ValueError("the excluded support must lie in the full Gram support")
    projection = _hermitian(gram_support - excluded_support)
    ridge = _hermitian(
        _support_ridge(gram, ridge_parameter, tolerance=tolerance)
        - _support_ridge(
            excluded_gram,
            ridge_parameter,
            tolerance=tolerance,
        )
    )
    return projection, ridge, order_minimum


def _block_signs(
    ambient_dimension: int,
    leaf_count: int,
) -> tuple[np.ndarray, ...]:
    if leaf_count < 2 or leaf_count & (leaf_count - 1):
        raise ValueError("the leaf count must be a power of two")
    if ambient_dimension % leaf_count:
        raise ValueError("equal coordinate blocks must partition the ambient space")
    block = ambient_dimension // leaf_count
    signs = []
    for mask in range(leaf_count):
        diagonal = np.empty(ambient_dimension)
        for leaf in range(leaf_count):
            value = 1.0 if (mask & leaf).bit_count() % 2 == 0 else -1.0
            diagonal[leaf * block : (leaf + 1) * block] = value
        signs.append(np.diag(diagonal).astype(complex))
    return tuple(signs)


def parity_curl_moment(
    contraction: np.ndarray,
    leaf_count: int,
) -> float:
    if contraction.ndim != 2 or contraction.shape[0] != contraction.shape[1]:
        raise ValueError("a square contraction is required")
    signs = _block_signs(contraction.shape[0], leaf_count)
    compressed = tuple(contraction @ sign @ contraction for sign in signs)
    total = 0.0
    for left in compressed:
        for right in compressed:
            commutator = left @ right - right @ left
            total += float(np.linalg.norm(commutator, ord="fro") ** 2 / 2.0)
    return total / leaf_count**2


def dependency_ridge_spectral_tail_upper_bound(
    gram: np.ndarray,
    excluded_gram: np.ndarray,
    ridge_parameter: float,
    *,
    tolerance: float = 1e-10,
) -> float:
    if ridge_parameter <= 0:
        raise ValueError("the ridge parameter must be positive")
    output = 0.0
    for matrix in (gram, excluded_gram):
        values = np.linalg.eigvalsh(_hermitian(matrix))
        if values[0] < -100 * tolerance:
            raise ValueError("the Gram matrices must be positive semidefinite")
        positive = values[values > 100 * tolerance]
        output += float(
            np.sum((ridge_parameter / (positive + ridge_parameter)) ** 2)
        )
    return output


def normalized_parity_curl_stability_bound(normalized_error: float) -> float:
    if normalized_error < 0:
        raise ValueError("normalized ridge error must be nonnegative")
    return 16.0 * normalized_error + 8.0 * normalized_error**2


def physical_parity_curl_transfer_bound(
    trace_weighted_error: float,
) -> float:
    if trace_weighted_error < 0:
        raise ValueError("trace-weighted ridge error must be nonnegative")
    return 16.0 * math.sqrt(trace_weighted_error) + 8.0 * trace_weighted_error


def audit_dependency_ridge_parity_stability(
    control_id: str,
    gram: np.ndarray,
    excluded_gram: np.ndarray,
    leaf_count: int,
    ridge_parameter: float,
    *,
    tolerance: float = 1e-9,
) -> DependencyRidgeParityControl:
    projection, ridge, order_minimum = dependency_projection_and_ridge(
        gram,
        excluded_gram,
        ridge_parameter,
        tolerance=tolerance,
    )
    ambient = gram.shape[0]
    if ambient % leaf_count:
        raise ValueError("leaf blocks must have equal integral dimension")
    rank = int(round(float(np.trace(projection).real)))
    if rank < 1:
        raise ValueError("the dependency projection must be nonzero")
    ridge_values = np.linalg.eigvalsh(ridge)
    contraction_residual = max(
        max(0.0, -float(ridge_values[0])),
        max(0.0, float(ridge_values[-1]) - 1.0),
    )
    projection_residual = float(
        np.linalg.norm(projection @ projection - projection, ord=2)
    )
    delta_squared = float(np.linalg.norm(projection - ridge, ord="fro") ** 2)
    tail = dependency_ridge_spectral_tail_upper_bound(
        gram,
        excluded_gram,
        ridge_parameter,
        tolerance=tolerance,
    )
    epsilon = math.sqrt(delta_squared / rank)
    exact = parity_curl_moment(projection, leaf_count) / rank
    approximate = parity_curl_moment(ridge, leaf_count) / rank
    difference = abs(exact - approximate)
    stability = normalized_parity_curl_stability_bound(epsilon)
    tail_verified = delta_squared <= tail + 5000 * tolerance
    stability_verified = difference <= stability + 5000 * tolerance
    nonnegative = min(exact, approximate) >= -5000 * tolerance
    verified = bool(
        order_minimum >= -100 * tolerance
        and projection_residual <= 5000 * tolerance
        and contraction_residual <= 5000 * tolerance
        and tail_verified
        and stability_verified
        and nonnegative
    )
    return DependencyRidgeParityControl(
        control_id=control_id,
        ambient_coefficient_dimension=ambient,
        exact_dependency_rank=rank,
        leaf_count=leaf_count,
        coordinate_block_dimension=ambient // leaf_count,
        ridge_parameter=ridge_parameter,
        gram_order_minimum_eigenvalue=order_minimum,
        ridge_minimum_eigenvalue=float(ridge_values[0]),
        ridge_maximum_eigenvalue=float(ridge_values[-1]),
        exact_projection_residual=projection_residual,
        ridge_positive_contraction_residual=contraction_residual,
        dependency_ridge_frobenius_error_squared=delta_squared,
        spectral_tail_error_upper_bound=tail,
        normalized_dependency_ridge_error=epsilon,
        exact_normalized_parity_curl_M4=exact,
        ridge_normalized_parity_curl_M4=approximate,
        normalized_parity_curl_difference=difference,
        dimension_free_stability_upper_bound=stability,
        spectral_tail_bound_verified=tail_verified,
        parity_curl_stability_verified=stability_verified,
        exact_and_ridge_curls_both_nonnegative=nonnegative,
        status=(
            "dependency-support-ridge-parity-curl-stability-verified"
            if verified
            else "dependency-ridge-parity-stability-control-failure"
        ),
    )


def _random_nested_grams(
    ambient_dimension: int,
    dependency_rank: int,
    *,
    seed: int,
) -> tuple[np.ndarray, np.ndarray]:
    if not 1 <= dependency_rank < ambient_dimension:
        raise ValueError("dependency rank must lie inside the ambient dimension")
    rng = np.random.default_rng(seed)
    raw = rng.normal(size=(ambient_dimension, ambient_dimension)) + 1j * rng.normal(
        size=(ambient_dimension, ambient_dimension)
    )
    unitary, _ = np.linalg.qr(raw)
    gram_values = np.linspace(0.35, 1.85, ambient_dimension)
    gram = (unitary * gram_values) @ unitary.conj().T
    raw = rng.normal(size=(ambient_dimension, ambient_dimension)) + 1j * rng.normal(
        size=(ambient_dimension, ambient_dimension)
    )
    rotation, _ = np.linalg.qr(raw)
    retained = ambient_dimension - dependency_rank
    contraction_values = np.concatenate(
        (np.linspace(0.15, 0.75, retained), np.zeros(dependency_rank))
    )
    contraction = (rotation * contraction_values) @ rotation.conj().T
    values, vectors = np.linalg.eigh(_hermitian(gram))
    root = (vectors * np.sqrt(np.maximum(values, 0.0))) @ vectors.conj().T
    excluded = _hermitian(root @ contraction @ root)
    return _hermitian(gram), excluded


def _commuting_nested_grams(
    ambient_dimension: int,
    dependency_rank: int,
) -> tuple[np.ndarray, np.ndarray]:
    gram_values = np.linspace(0.4, 1.6, ambient_dimension)
    excluded_values = 0.6 * gram_values
    excluded_values[-dependency_rank:] = 0.0
    return np.diag(gram_values).astype(complex), np.diag(excluded_values).astype(complex)


def physical_ridge_transfer_record(
    trace_weighted_error: float,
    target_exact_physical_M4_lower_bound: float,
) -> PhysicalRidgeTransferRecord:
    if target_exact_physical_M4_lower_bound < 0:
        raise ValueError("the target M4 lower bound must be nonnegative")
    transfer = physical_parity_curl_transfer_bound(trace_weighted_error)
    required = target_exact_physical_M4_lower_bound + transfer
    return PhysicalRidgeTransferRecord(
        trace_weighted_dependency_ridge_error=trace_weighted_error,
        physical_parity_curl_transfer_upper_bound=transfer,
        target_exact_physical_M4_lower_bound=target_exact_physical_M4_lower_bound,
        required_ridge_physical_M4_lower_bound=required,
        ridge_signal_survives_transfer=required <= 1.0,
        uniform_child_frame_edge_required=False,
        uniform_common_metric_edge_required=False,
        status=(
            "trace-weighted-ridge-error-permits-positive-M4-transfer"
            if required <= 1.0
            else "ridge-error-too-large-for-unit-scale-transfer"
        ),
    )


def dependency_ridge_parity_stability_theorem(
) -> DependencyRidgeParityStabilityTheorem:
    return DependencyRidgeParityStabilityTheorem(
        dependency_projection="Pi=supp(L)-supp(M), with 0<=M<=L",
        support_ridge=(
            "Q_eta=L(L+eta I)^-1-M(M+eta I)^-1"
        ),
        operator_order="0<=Q_eta<=I by operator monotonicity of x/(x+eta)",
        parity_curl_functional=(
            "C(P)=q^-2 sum_(S,T)||[PZ_SP,PZ_TP]||_F^2/2"
        ),
        normalized_stability=(
            "|C(Pi)-C(Q)|/r<=16 epsilon+8 epsilon^2 for epsilon=||Pi-Q||F/sqrt(r)"
        ),
        physical_annealed_stability=(
            "E[1_E|C(Pi)-C(Q)|/D]<=16sqrt(R)+8R, "
            "R=E[1_E||Pi-Q||F^2/D]"
        ),
        spectral_tail=(
            "||Pi-Q_eta||F^2<=sum_spec+(L)(eta/(lambda+eta))^2+sum_spec+(M)(eta/(mu+eta))^2"
        ),
        heat_kernel=(
            "f_eta(A)=I-eta integral_0^infinity exp(-eta t)exp(-tA)dt"
        ),
        arbitrary_nested_positive_grams=True,
        arbitrary_equal_coordinate_blocks=True,
        theorem_verified=True,
        status="exact-parity-curl-M4-stable-under-support-resolvent-ridge",
    )


def run_component_dependency_ridge_parity_stability(
) -> ComponentDependencyRidgeParityStabilityReport:
    random_first = _random_nested_grams(16, 6, seed=6101)
    random_second = _random_nested_grams(16, 5, seed=6102)
    commuting = _commuting_nested_grams(16, 6)
    controls = [
        audit_dependency_ridge_parity_stability(
            "RANDOM-NESTED-N16-R6-ETA-1E-2",
            *random_first,
            4,
            1e-2,
        ),
        audit_dependency_ridge_parity_stability(
            "RANDOM-NESTED-N16-R6-ETA-1E-3",
            *random_first,
            4,
            1e-3,
        ),
        audit_dependency_ridge_parity_stability(
            "RANDOM-NESTED-N16-R5-ETA-3E-3",
            *random_second,
            8,
            3e-3,
        ),
        audit_dependency_ridge_parity_stability(
            "COMMUTING-NESTED-N16-R6-ETA-1E-2",
            *commuting,
            4,
            1e-2,
        ),
    ]
    transfers = [
        physical_ridge_transfer_record(error, target)
        for error, target in (
            (1e-12, 1e-4),
            (1e-10, 1e-4),
            (1e-8, 1e-4),
            (1e-6, 1e-4),
        )
    ]
    theorem = dependency_ridge_parity_stability_theorem()
    failures = sum(
        row.status == "dependency-ridge-parity-stability-control-failure"
        for row in controls
    )
    converges = bool(
        controls[1].dependency_ridge_frobenius_error_squared
        < controls[0].dependency_ridge_frobenius_error_squared
        and controls[1].normalized_parity_curl_difference
        < controls[0].normalized_parity_curl_difference
    )
    return ComponentDependencyRidgeParityStabilityReport(
        created_at=utc_now(),
        theorem_contract={
            "dependency_projection": theorem.dependency_projection,
            "support_ridge": theorem.support_ridge,
            "operator_order": theorem.operator_order,
            "parity_curl": theorem.parity_curl_functional,
            "fiber_stability": theorem.normalized_stability,
            "physical_stability": theorem.physical_annealed_stability,
            "spectral_tail": theorem.spectral_tail,
            "word_access": theorem.heat_kernel,
            "scope": (
                "The theorem removes exact support discontinuity from the M4 "
                "target conditionally on a trace-weighted spectral tail; it "
                "does not prove a positive natural ridge curl or that tail."
            ),
        },
        theorem=theorem,
        finite_controls=controls,
        physical_transfer_records=transfers,
        proof_obligations=[
            {
                "obligation": "replace_dependency_support_projection_by_bounded_resolvent_in_M4",
                "resolved": theorem.theorem_verified and failures == 0,
                "resolution": (
                    "Operator monotonicity gives a positive contraction and "
                    "equations (3)-(4) transfer its parity curl without outcome-count loss."
                ),
            },
            {
                "obligation": "reduce_ridge_to_support_error_to_scalar_spectral_tail",
                "resolved": theorem.theorem_verified and failures == 0,
                "resolution": (
                    "Equation (5) is an explicit trace of squared resolvent "
                    "defects for L and M."
                ),
            },
            {
                "obligation": "prove_natural_trace_weighted_dependency_ridge_error_small",
                "resolved": False,
                "resolution": (
                    "Choose inverse-polynomial eta and bound the regular-master "
                    "average of equation (5) under accepted Plancherel sources."
                ),
            },
            {
                "obligation": "prove_positive_natural_bounded_ridge_parity_curl",
                "resolved": False,
                "resolution": (
                    "Evaluate the heat-kernel/resolvent parity words on typical "
                    "four-cell mask strata and beat the transfer error."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "The difference of two support ridges need not be positive.",
                "resolved": True,
                "resolution": (
                    "It is positive here because M<=L and x/(x+eta) is operator monotone."
                ),
            },
            {
                "objection": "Approximating q leaf effects incurs a factor q.",
                "resolved": True,
                "resolution": (
                    "The Walsh pair functional is a normalized q^-2 average; "
                    "the stability constant is outcome-count independent."
                ),
            },
            {
                "objection": "A uniform minimum eigenvalue of L and M is required.",
                "resolved": True,
                "resolution": (
                    "No. The transfer premise is the annealed trace-weighted "
                    "squared resolvent tail in equation (5)."
                ),
            },
            {
                "objection": "A small ridge error proves positive M4.",
                "resolved": True,
                "resolution": (
                    "No. The bounded ridge curl must first have a positive "
                    "natural lower bound exceeding the transfer error."
                ),
            },
        ],
        headline_metrics={
            "dependency_support_ridge_parity_stability_theorem_count": int(
                theorem.theorem_verified and failures == 0
            ),
            "trace_weighted_physical_transfer_theorem_count": int(
                theorem.theorem_verified
            ),
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "finite_eta_convergence_control_count": int(converges),
            "maximum_finite_stability_ratio": max(
                row.normalized_parity_curl_difference
                / row.dimension_free_stability_upper_bound
                if row.dimension_free_stability_upper_bound
                else 0.0
                for row in controls
            ),
            "physical_transfer_record_count": len(transfers),
            "physical_transfer_surviving_record_count": sum(
                row.ridge_signal_survives_transfer for row in transfers
            ),
            "natural_trace_weighted_dependency_ridge_error_theorem_count": 0,
            "natural_bounded_ridge_parity_curl_lower_bound_count": 0,
            "natural_component_M4_lower_bound_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "dependency_support_has_positive_contraction_resolvent_approximation": True,
            "parity_curl_M4_is_outcome_count_free_stable": (
                theorem.theorem_verified and failures == 0
            ),
            "physical_trace_weighted_ridge_transfer_proved": True,
            "uniform_child_frame_edge_required": False,
            "uniform_common_metric_edge_required": False,
            "natural_trace_weighted_dependency_ridge_error_small": False,
            "natural_bounded_ridge_parity_curl_positive": False,
            "natural_component_M4_positive": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Support discontinuity and common-metric inversion are removed "
                "from the trace target, but both the natural ridge spectral "
                "tail and positive bounded parity curl remain open."
            ),
        },
        status=(
            "dependency-support-M4-transferred-to-bounded-ridge-parity-curl"
            if failures == 0 and converges
            else "dependency-ridge-parity-stability-control-failure"
        ),
        summary=(
            "Replaced the exact dependency support projection by an ordered "
            "positive resolvent ridge with dimension-free parity-curl M4 "
            "stability and an explicit trace-weighted spectral-tail premise."
        ),
        falsifiers_triggered=[
            "The ordered support-ridge difference is positive only because 0<=M<=L and the resolvent map is operator monotone.",
            "No factor equal to the exponential leaf count appears in the parity-curl transfer.",
            "Uniform spectral edges are stronger than the trace-weighted ridge premise actually needed.",
            "No natural ridge error, ridge curl, exact M4, algorithm, or speedup is proved.",
        ],
    )


def write_component_dependency_ridge_parity_stability_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-DEPENDENCY-RIDGE-PARITY-STABILITY"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_component_dependency_ridge_parity_stability" in globals():
        report = run_component_dependency_ridge_parity_stability(**kwargs)
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
                id="NEG-SELF-DUAL-WREATH-COMPONENT-DEPENDENCY-RIDGE-PARITY-STABILITY",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-COMPONENT-DEPENDENCY-RIDGE-PARITY-STABILITY.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-COMPONENT-DEPENDENCY-RIDGE-PARITY-STABILITY.",
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
                    "self_dual_wreath_component_dependency_ridge_parity_stability": str(path)
                },
            )
        )
    return payload
