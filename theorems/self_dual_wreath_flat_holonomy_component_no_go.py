"""Flat unitary holonomy cannot realize the natural component POVM.

The existing GPE holonomy reduction treats one flat equal-rank carrier
channel.  Choose a root fiber, unitary tree transports ``T_v``, a holonomy
fixed-space isometry ``B``, and scalar vertex amplitudes ``a_v`` with
``sum_v |a_v|^2=1``.  Its section isometry is

    W x = direct_sum_v a_v T_v B x.                         (1)

For the coordinate projector ``D_v``, the induced component effect is

    H_v = W^* D_v W
        = |a_v|^2 B^* T_v^* T_v B
        = |a_v|^2 I.                                       (2)

This remains true after imposing arbitrary cycle-holonomy fixed-space
conditions: they only change ``B``.  Therefore every flat equal-rank unitary
connection produces a scalar commuting component POVM and has ``M4=0``.

The natural final-root component POVM instead has

    liminf E M4(H)/r >= 3/64,                               (3)

and every commuting POVM approximation has aggregate normalized Frobenius
error at least ``3/512-o(1)``.  Its retained support projectors have
``E M4(Q)/r -> alpha(alpha-1)>=2``.  Flat scalar support patterns are even
more mismatched: their nonzero support at a vertex is the whole root fiber,
whereas natural component support ranks are ``o(r)`` leafwise and have total
rank ``alpha r+o(r)``.

Hence proving coherent SELECT and an inverse-polynomial frustration gap for
the current flat holonomy model would still not compile the natural component
measurement.  The resolver must first be generalized to vertex-dependent
partial supports, operator-valued endpoint metrics, or an equivalent direct
global polar transform.

This is not an all-GPE no-go.  GPE pair polars can be ingredients in a
nonflat partial-isometry connection.  No such all-leaf connection, coherent
support SELECT, decoder, algorithm, or speedup is proved here.
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
    "self_dual_wreath_flat_holonomy_component_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-FLAT-HOLONOMY-COMPONENT-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
NATURAL_EFFECT_M4_FLOOR = 3.0 / 64.0
NATURAL_COMMUTING_EFFECT_ERROR_FLOOR = 3.0 / 512.0
NATURAL_SUPPORT_M4_FLOOR = 2.0


@dataclass(frozen=True)
class FlatHolonomyComponentControl:
    control_id: str
    vertex_count: int
    ambient_fiber_dimension: int
    holonomy_fixed_space_dimension: int
    scalar_vertex_weights: tuple[float, ...]
    section_isometry_residual: float
    maximum_transport_unitarity_residual: float
    maximum_component_scalar_residual: float
    component_effect_sum_residual: float
    normalized_component_m4: float
    component_effects_pairwise_commute: bool
    exact_flat_holonomy_scalarization_verified: bool
    status: str


@dataclass(frozen=True)
class FlatSupportPatternControl:
    control_id: str
    fiber_dimension: int
    leaf_count: int
    active_flat_vertex_count: int
    normalized_natural_total_support_rank: float
    maximum_normalized_natural_leaf_rank: float
    normalized_flat_support_approximation_error: float
    rank_only_error_lower_bound: float
    rank_mismatch_bound_verified: bool
    status: str


@dataclass(frozen=True)
class FlatHolonomyScalingRecord:
    child_aspect: float
    natural_effect_m4_limit: float
    natural_support_m4_limit: float
    flat_holonomy_effect_m4: float
    commuting_effect_error_floor: float
    natural_total_support_rank_to_fiber: float
    flat_equal_rank_holonomy_sufficient: bool
    partial_support_or_operator_metric_required: bool
    nonflat_gpe_holonomy_compiled: bool
    status: str


@dataclass(frozen=True)
class FlatHolonomyNoGoTheorem:
    section_isometry: str
    component_effects: str
    fixed_space_invariance: str
    natural_separation: str
    required_extension: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class FlatHolonomyComponentNoGoReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: FlatHolonomyNoGoTheorem
    flat_holonomy_controls: list[FlatHolonomyComponentControl]
    flat_support_controls: list[FlatSupportPatternControl]
    scaling_records: list[FlatHolonomyScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _hermitian(matrix: np.ndarray) -> np.ndarray:
    return (matrix + matrix.conj().T) / 2.0


def _orthonormal_columns(matrix: np.ndarray, tolerance: float) -> bool:
    if matrix.ndim != 2 or not matrix.shape[1]:
        return False
    return bool(
        np.linalg.norm(
            matrix.conj().T @ matrix - np.eye(matrix.shape[1]),
            ord=2,
        )
        <= 1000 * tolerance
    )


def flat_holonomy_section(
    root_transports: tuple[np.ndarray, ...],
    fixed_space_basis: np.ndarray,
    vertex_weights: tuple[complex, ...],
    *,
    tolerance: float = 1e-9,
) -> np.ndarray:
    if not root_transports or len(root_transports) != len(vertex_weights):
        raise ValueError("one transport and scalar amplitude are required per vertex")
    dimension = root_transports[0].shape[0]
    if any(
        transport.ndim != 2 or transport.shape != (dimension, dimension)
        for transport in root_transports
    ):
        raise ValueError("flat transports must be square on one common fiber")
    if fixed_space_basis.shape[0] != dimension or not _orthonormal_columns(
        fixed_space_basis,
        tolerance,
    ):
        raise ValueError("fixed-space basis must be an isometry in the root fiber")
    if any(
        np.linalg.norm(
            transport.conj().T @ transport - np.eye(dimension),
            ord=2,
        )
        > 1000 * tolerance
        for transport in root_transports
    ):
        raise ValueError("flat root transports must be unitary")
    weight_norm = sum(abs(weight) ** 2 for weight in vertex_weights)
    if abs(weight_norm - 1.0) > 1000 * tolerance:
        raise ValueError("squared vertex amplitudes must sum to one")
    return np.vstack(
        tuple(
            weight * transport @ fixed_space_basis
            for weight, transport in zip(vertex_weights, root_transports)
        )
    )


def coordinate_component_effects(
    section: np.ndarray,
    vertex_count: int,
) -> tuple[np.ndarray, ...]:
    if section.ndim != 2 or vertex_count < 1 or section.shape[0] % vertex_count:
        raise ValueError("section rows must split into equal nonempty vertex blocks")
    width = section.shape[0] // vertex_count
    return tuple(
        _hermitian(
            section[index * width : (index + 1) * width].conj().T
            @ section[index * width : (index + 1) * width]
        )
        for index in range(vertex_count)
    )


def component_m4(effects: tuple[np.ndarray, ...]) -> float:
    return sum(
        float(np.linalg.norm(left @ right - right @ left, ord="fro") ** 2 / 2)
        for left in effects
        for right in effects
    )


def audit_flat_holonomy_component(
    control_id: str,
    root_transports: tuple[np.ndarray, ...],
    fixed_space_basis: np.ndarray,
    vertex_weights: tuple[complex, ...],
    *,
    tolerance: float = 1e-9,
) -> FlatHolonomyComponentControl:
    section = flat_holonomy_section(
        root_transports,
        fixed_space_basis,
        vertex_weights,
        tolerance=tolerance,
    )
    effects = coordinate_component_effects(section, len(root_transports))
    fixed_dimension = fixed_space_basis.shape[1]
    identity = np.eye(fixed_dimension, dtype=complex)
    scalars = tuple(float(abs(weight) ** 2) for weight in vertex_weights)
    isometry_residual = float(
        np.linalg.norm(section.conj().T @ section - identity, ord=2)
    )
    unitary_residual = max(
        float(
            np.linalg.norm(
                transport.conj().T @ transport
                - np.eye(transport.shape[0]),
                ord=2,
            )
        )
        for transport in root_transports
    )
    scalar_residual = max(
        float(np.linalg.norm(effect - scalar * identity, ord=2))
        for effect, scalar in zip(effects, scalars)
    )
    sum_residual = float(
        np.linalg.norm(sum(effects, np.zeros_like(identity)) - identity, ord=2)
    )
    m4 = component_m4(effects) / fixed_dimension
    commute = all(
        np.linalg.norm(left @ right - right @ left, ord=2) <= 1000 * tolerance
        for index, left in enumerate(effects)
        for right in effects[index + 1 :]
    )
    verified = bool(
        max(
            isometry_residual,
            unitary_residual,
            scalar_residual,
            sum_residual,
            m4,
        )
        <= 1000 * tolerance
        and commute
    )
    return FlatHolonomyComponentControl(
        control_id=control_id,
        vertex_count=len(root_transports),
        ambient_fiber_dimension=root_transports[0].shape[0],
        holonomy_fixed_space_dimension=fixed_dimension,
        scalar_vertex_weights=scalars,
        section_isometry_residual=isometry_residual,
        maximum_transport_unitarity_residual=unitary_residual,
        maximum_component_scalar_residual=scalar_residual,
        component_effect_sum_residual=sum_residual,
        normalized_component_m4=m4,
        component_effects_pairwise_commute=commute,
        exact_flat_holonomy_scalarization_verified=verified,
        status=(
            "flat-holonomy-component-povm-exactly-scalar"
            if verified
            else "flat-holonomy-component-control-failure"
        ),
    )


def audit_flat_support_pattern(
    control_id: str,
    natural_supports: tuple[np.ndarray, ...],
    active_flat_vertices: tuple[int, ...],
    *,
    tolerance: float = 1e-9,
) -> FlatSupportPatternControl:
    if not natural_supports:
        raise ValueError("at least one natural support is required")
    dimension = natural_supports[0].shape[0]
    if any(support.shape != (dimension, dimension) for support in natural_supports):
        raise ValueError("supports must share one square dimension")
    active = set(active_flat_vertices)
    if any(index < 0 or index >= len(natural_supports) for index in active):
        raise ValueError("active flat vertex is out of range")
    identity = np.eye(dimension, dtype=complex)
    ranks = []
    error = 0.0
    for index, support in enumerate(natural_supports):
        projector = _hermitian(support)
        if np.linalg.norm(projector @ projector - projector, ord=2) > 1000 * tolerance:
            raise ValueError("natural supports must be projections")
        rank = float(np.trace(projector).real)
        ranks.append(rank)
        target = identity if index in active else np.zeros_like(identity)
        error += float(np.linalg.norm(projector - target, ord="fro") ** 2)
    total_ratio = sum(ranks) / dimension
    maximum_ratio = max(ranks) / dimension
    active_count = len(active)
    lower = total_ratio + active_count * (1.0 - 2.0 * maximum_ratio)
    verified = error / dimension + 1000 * tolerance >= lower
    return FlatSupportPatternControl(
        control_id=control_id,
        fiber_dimension=dimension,
        leaf_count=len(natural_supports),
        active_flat_vertex_count=active_count,
        normalized_natural_total_support_rank=total_ratio,
        maximum_normalized_natural_leaf_rank=maximum_ratio,
        normalized_flat_support_approximation_error=error / dimension,
        rank_only_error_lower_bound=lower,
        rank_mismatch_bound_verified=verified,
        status=(
            "flat-full-fiber-support-rank-mismatch-verified"
            if verified
            else "flat-support-rank-mismatch-control-failure"
        ),
    )


def _rotation(angle: float) -> np.ndarray:
    return np.asarray(
        [
            [math.cos(angle), -math.sin(angle), 0.0],
            [math.sin(angle), math.cos(angle), 0.0],
            [0.0, 0.0, 1.0],
        ],
        dtype=complex,
    )


def _phase(first: float, second: float) -> np.ndarray:
    return np.diag([np.exp(1j * first), np.exp(1j * second), 1.0]).astype(complex)


def _finite_controls() -> list[FlatHolonomyComponentControl]:
    identity = np.eye(3, dtype=complex)
    full = identity
    fixed_two = identity[:, (0, 2)]
    fixed_one = identity[:, (2,)]
    return [
        audit_flat_holonomy_component(
            "UNIFORM-UNITARY-TREE-FULL-FIBER",
            (identity, _rotation(0.31), _phase(0.2, -0.4)),
            full,
            tuple([1 / math.sqrt(3)] * 3),
        ),
        audit_flat_holonomy_component(
            "NONUNIFORM-WEIGHTED-FIXED-SUBSPACE",
            (identity, _rotation(0.47), _phase(0.7, -0.2)),
            fixed_two,
            (math.sqrt(0.2), math.sqrt(0.3), math.sqrt(0.5)),
        ),
        audit_flat_holonomy_component(
            "RANK-ONE-HOLONOMY-FIXED-SPACE",
            (identity, _rotation(0.63), _phase(0.4, 0.8), _rotation(-0.28)),
            fixed_one,
            (0.5, 0.5, 0.5, 0.5),
        ),
    ]


def _support_controls() -> list[FlatSupportPatternControl]:
    dimension = 12
    supports = []
    for start in (0, 2, 4, 6, 8, 10):
        projector = np.zeros((dimension, dimension), dtype=complex)
        projector[start, start] = 1.0
        projector[(start + 1) % dimension, (start + 1) % dimension] = 1.0
        supports.append(projector)
    family = tuple(supports)
    return [
        audit_flat_support_pattern("NO-FLAT-ACTIVE-VERTEX", family, ()),
        audit_flat_support_pattern("ONE-FLAT-ACTIVE-VERTEX", family, (0,)),
        audit_flat_support_pattern("ALL-FLAT-ACTIVE-VERTICES", family, tuple(range(6))),
    ]


def flat_holonomy_scaling_record(child_aspect: float) -> FlatHolonomyScalingRecord:
    if not 2 <= child_aspect <= 4:
        raise ValueError("the natural final-root aspect lies in [2,4]")
    gamma = 1.0 / child_aspect
    return FlatHolonomyScalingRecord(
        child_aspect=child_aspect,
        natural_effect_m4_limit=gamma**2 * (1.0 - gamma),
        natural_support_m4_limit=child_aspect * (child_aspect - 1.0),
        flat_holonomy_effect_m4=0.0,
        commuting_effect_error_floor=NATURAL_COMMUTING_EFFECT_ERROR_FLOOR,
        natural_total_support_rank_to_fiber=child_aspect,
        flat_equal_rank_holonomy_sufficient=False,
        partial_support_or_operator_metric_required=True,
        nonflat_gpe_holonomy_compiled=False,
        status="flat-holonomy-falsified-nonflat-partial-support-required",
    )


def flat_holonomy_no_go_theorem() -> FlatHolonomyNoGoTheorem:
    return FlatHolonomyNoGoTheorem(
        section_isometry="W=stack_v a_v T_v B with sum_v|a_v|^2=1",
        component_effects="W^*D_vW=|a_v|^2 I on every holonomy fixed space",
        fixed_space_invariance=(
            "arbitrary cycle constraints only replace the root basis by an "
            "isometry B and cannot create operator-valued vertex effects"
        ),
        natural_separation=(
            "natural M4/r has liminf 3/64, so every flat scalar/commuting "
            "component POVM has normalized aggregate error at least 3/512-o(1)"
        ),
        required_extension=(
            "vertex-dependent partial supports, operator-valued endpoint metrics, "
            "or a direct representation-specific global polar"
        ),
        theorem_verified=True,
        status="flat-equal-rank-holonomy-component-architecture-falsified",
    )


def run_flat_holonomy_component_no_go() -> FlatHolonomyComponentNoGoReport:
    flat_controls = _finite_controls()
    support_controls = _support_controls()
    scaling = [
        flat_holonomy_scaling_record(alpha)
        for alpha in (2.0, 2.25, 2.5, 3.0, 3.5, 4.0)
    ]
    theorem = flat_holonomy_no_go_theorem()
    failures = sum(
        not row.exact_flat_holonomy_scalarization_verified for row in flat_controls
    )
    failures += sum(not row.rank_mismatch_bound_verified for row in support_controls)
    verified = theorem.theorem_verified and failures == 0
    return FlatHolonomyComponentNoGoReport(
        created_at=utc_now(),
        theorem_contract={
            "section": theorem.section_isometry,
            "effects": theorem.component_effects,
            "holonomy": theorem.fixed_space_invariance,
            "separation": theorem.natural_separation,
            "required_extension": theorem.required_extension,
        },
        theorem=theorem,
        flat_holonomy_controls=flat_controls,
        flat_support_controls=support_controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "test_flat_equal_rank_holonomy_against_natural_component_m4",
                "resolved": verified,
                "resolution": (
                    "Every flat section has scalar coordinate effects and zero M4, "
                    "separated from the positive natural limit."
                ),
            },
            {
                "obligation": "generalize_gpe_holonomy_to_partial_support_connections",
                "resolved": False,
                "resolution": (
                    "Need coherently selectable initial/final support projections, "
                    "partial transports, and an operator-valued frustration gap."
                ),
            },
            {
                "obligation": "compile_direct_global_orientation_polar",
                "resolved": False,
                "resolution": (
                    "A direct representation transform could bypass componentwise "
                    "partial-holonomy assembly but is not known."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Nontrivial cycle holonomy makes flat vertex effects noncommuting.",
                "resolved": True,
                "resolution": (
                    "Cycle constraints only choose B; unitarity still gives "
                    "B^*T_v^*T_vB=I at every vertex."
                ),
            },
            {
                "objection": "Nonuniform scalar vertex weights create the natural geometry.",
                "resolved": True,
                "resolution": "They change probabilities but every effect remains scalar.",
            },
            {
                "objection": "This rules out pair-polar GPE as an ingredient.",
                "resolved": True,
                "resolution": (
                    "No. It rules out only a flat equal-rank assembly; pair GPE may "
                    "supply edges in a genuinely partial-support connection."
                ),
            },
            {
                "objection": "A flat model can match retained supports by activating all vertices.",
                "resolved": True,
                "resolution": (
                    "Its support is then the full fiber at every vertex, while "
                    "natural leaf support is sparse and total support rank is only alpha r."
                ),
            },
        ],
        headline_metrics={
            "flat_holonomy_scalar_effect_theorem_count": int(verified),
            "flat_holonomy_architecture_no_go_count": int(verified),
            "finite_flat_holonomy_control_count": len(flat_controls),
            "finite_flat_support_control_count": len(support_controls),
            "finite_control_failure_count": failures,
            "natural_effect_m4_uniform_floor": NATURAL_EFFECT_M4_FLOOR,
            "natural_commuting_effect_error_uniform_floor": NATURAL_COMMUTING_EFFECT_ERROR_FLOOR,
            "natural_support_m4_uniform_floor": NATURAL_SUPPORT_M4_FLOOR,
            "partial_support_holonomy_compiler_count": 0,
            "direct_global_polar_compiler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "flat_equal_rank_holonomy_component_povm_rejected": verified,
            "partial_support_or_operator_metric_required": verified,
            "all_gpe_holonomy_routes_rejected": False,
            "partial_support_gpe_holonomy_compiled": False,
            "direct_global_orientation_polar_compiled": False,
            "hidden_label_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Flat holonomy can only produce scalar vertex effects; the natural "
                "nonabelian support geometry requires a nonflat coherent architecture."
            ),
        },
        status=(
            "flat-holonomy-component-route-falsified-partial-support-required"
            if verified
            else "flat-holonomy-component-no-go-control-failure"
        ),
        summary=(
            "A flat equal-rank unitary GPE-holonomy resolver has exactly scalar "
            "coordinate effects on every fixed space and cannot realize the positive "
            "natural component M4. Partial supports, operator-valued metrics, or a "
            "direct global polar are mandatory."
        ),
        falsifiers_triggered=[
            "Solving only the flat holonomy gap would not compile the natural component POVM.",
            "Nontrivial unitary cycle holonomy does not create noncommuting vertex effects.",
            "Scalar vertex reweighting cannot substitute for partial support geometry.",
        ],
    )


def write_flat_holonomy_component_no_go_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-FLAT-HOLONOMY-COMPONENT-NO-GO"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_flat_holonomy_component_no_go" in globals():
        report = run_flat_holonomy_component_no_go(**kwargs)
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
                id="NEG-SELF-DUAL-WREATH-FLAT-HOLONOMY-COMPONENT-NO-GO",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-FLAT-HOLONOMY-COMPONENT-NO-GO.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-FLAT-HOLONOMY-COMPONENT-NO-GO.",
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
                    "self_dual_wreath_flat_holonomy_component_no_go": str(path)
                },
            )
        )
    return payload
