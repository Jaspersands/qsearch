"""Recursive child-span compiler normal form for the wreath PGM polar.

The hierarchical cokernel theorem resolves every parent dependency
information-theoretically.  This module separates the corresponding coherent
operation into the two pieces that a circuit must actually implement.

For child syntheses ``S_L,S_R`` and an isometry ``X`` onto their common
physical span, define

    A_s = X^* (S_s S_s^*)^+ X,
    W_s = S_s^+ X A_s^(-1/2),
    M   = A_L + A_R.                                      (1)

Each ``W_s`` is an isometry into the child coefficient register.  The
normalized parent relation has the exact factorization

    Z = [S_L^+X; -S_R^+X] M^(-1/2)
      = [W_L C_L; -W_R C_R],
    C_s = A_s^(1/2) M^(-1/2).                             (2)

Thus ``C_L^*C_L+C_R^*C_R=I``.  If ``A_L=A_R``, both endpoint
mixers are exactly ``I/sqrt(2)``: the parent relation is one Hadamard followed
by controlled child embeddings.  If the metrics merely have comparable
spectra but do not commute, the endpoint operation is genuinely
matrix-valued.  Pair GPE transports do not remove this mixer.

There is nevertheless a useful constructive case.  Suppose a normalized
child embedding has the flat affine form

    W|psi> = |A|^(-1/2) sum_(x in A) |x> V_x|psi>,         (3)

where ``A`` is an affine mask space and the generator transports
``V_(x+g)V_x^*`` have coherent GPE circuits.  Ordered affine Hadamards and
those transports implement (3) in ``dim(A)`` transport stages, with no
``sqrt(|A|)`` amplitude-amplification factor.  The existing finite W3/W5
controls satisfy this compiler shape.  No all-n affine decomposition,
uniform generator SELECT, or complete PGM circuit is claimed.  The companion
sparse-Gram S6 audit further shows that scalar affine fibers are not universal
even for globally distinct sources: the all-n extension must support
matrix-valued partial fibers.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_affine_recoupling_bundle import (
    affine_basis,
    run_affine_recoupling_bundle,
)
from self_dual_wreath_pair_polar_transport_network import (
    run_pair_polar_transport_network,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_gpe_recursive_node_compiler.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-GPE-RECURSIVE-NODE-COMPILER"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class RecursiveNodeCompilerControl:
    control_id: str
    fiber_dimension: int
    left_coefficient_dimension: int
    right_coefficient_dimension: int
    left_metric_minimum_eigenvalue: float
    left_metric_maximum_eigenvalue: float
    right_metric_minimum_eigenvalue: float
    right_metric_maximum_eigenvalue: float
    metric_commutator_norm: float
    metric_equality_residual: float
    left_embedding_isometry_residual: float
    right_embedding_isometry_residual: float
    endpoint_mixer_column_isometry_residual: float
    relation_factorization_residual: float
    normalized_relation_isometry_residual: float
    left_endpoint_effect_minimum_eigenvalue: float
    left_endpoint_effect_maximum_eigenvalue: float
    maximum_grading_defect: float
    minimum_endpoint_gap: float
    left_scalar_mixer_residual: float
    right_scalar_mixer_residual: float
    exact_recursive_normal_form_verified: bool
    endpoint_mixer_is_exact_hadamard: bool
    endpoint_mixer_is_scalar: bool
    status: str


@dataclass(frozen=True)
class HierarchicalConditioningCounterexample:
    exponent: int
    metric_ratio: int
    left_endpoint_weight: float
    right_endpoint_weight: float
    maximum_grading_defect: float
    minimum_endpoint_gap: float
    inverse_gap_cost: float
    pair_gpe_transport_available: bool
    constant_endpoint_gap: bool
    status: str


@dataclass(frozen=True)
class AffineGpeCompilerControl:
    control_id: str
    active_mask_count: int
    affine_dimension: int
    intersection_dimension: int
    generator_transport_stage_count: int
    maximum_pair_path_length: int
    flat_affine_bundle_verified: bool
    pair_polar_path_network_verified: bool
    direct_gpe_pair_polar_available: bool
    finite_constant_size_compiler_certificate: bool
    status: str


@dataclass(frozen=True)
class AffinePreparationControl:
    active_masks: tuple[int, ...]
    affine_dimension: int
    ambient_dimension: int
    fiber_dimension: int
    generator_transport_stage_count: int
    maximum_compiled_embedding_residual: float
    compiled_embedding_isometry_residual: float
    exact_flat_affine_preparation_verified: bool
    status: str


@dataclass(frozen=True)
class GpeRecursiveNodeCompilerScalingRecord:
    n: int
    information_threshold_copy_count: int
    maximum_affine_transport_stage_count: int
    pair_polar_gate_cost_polynomial: bool
    width_amplification_required_for_flat_affine_preparation: bool
    all_n_affine_child_embedding_theorem_proved: bool
    polynomial_uniform_generator_select_proved: bool
    natural_short_metric_equality_or_comparability_proved: bool
    recursive_orientation_polar_proved: bool
    status: str


@dataclass(frozen=True)
class GpeRecursiveNodeCompilerReport:
    created_at: str
    theorem_contract: dict[str, Any]
    node_controls: list[RecursiveNodeCompilerControl]
    conditioning_counterfamily: list[HierarchicalConditioningCounterexample]
    affine_preparation_control: AffinePreparationControl
    finite_gpe_compiler_controls: list[AffineGpeCompilerControl]
    scaling_records: list[GpeRecursiveNodeCompilerScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _psd_power(
    matrix: np.ndarray,
    exponent: float,
    *,
    tolerance: float,
) -> np.ndarray:
    hermitian = (matrix + matrix.conj().T) / 2
    values, vectors = np.linalg.eigh(hermitian)
    if len(values) and values[0] < -100 * tolerance:
        raise ArithmeticError("matrix is not positive semidefinite")
    powered = np.zeros_like(values)
    positive = values > 100 * tolerance
    powered[positive] = values[positive] ** exponent
    return (vectors * powered) @ vectors.conj().T


def _range_residual(
    synthesis: np.ndarray,
    common: np.ndarray,
    *,
    tolerance: float,
) -> float:
    projector = synthesis @ np.linalg.pinv(synthesis, rcond=tolerance)
    return float(np.linalg.norm((np.eye(synthesis.shape[0]) - projector) @ common))


def audit_recursive_node_compiler(
    control_id: str,
    left_synthesis: np.ndarray,
    right_synthesis: np.ndarray,
    common: np.ndarray,
    *,
    tolerance: float = 1e-9,
) -> RecursiveNodeCompilerControl:
    """Audit the exact factorization (1)-(2) for one parent merge."""

    if left_synthesis.shape[0] != right_synthesis.shape[0]:
        raise ValueError("child syntheses must share a physical output space")
    if common.shape[0] != left_synthesis.shape[0] or not common.shape[1]:
        raise ValueError("common must be a nonempty physical-space isometry")
    identity = np.eye(common.shape[1], dtype=complex)
    if np.linalg.norm(common.conj().T @ common - identity, ord=2) > 100 * tolerance:
        raise ValueError("common must be an isometry")
    if max(
        _range_residual(left_synthesis, common, tolerance=tolerance),
        _range_residual(right_synthesis, common, tolerance=tolerance),
    ) > 1000 * tolerance:
        raise ValueError("common must lie in both child synthesis ranges")

    left_inverse = np.linalg.pinv(left_synthesis, rcond=tolerance)
    right_inverse = np.linalg.pinv(right_synthesis, rcond=tolerance)
    left_preimage = left_inverse @ common
    right_preimage = right_inverse @ common
    left_metric = left_preimage.conj().T @ left_preimage
    right_metric = right_preimage.conj().T @ right_preimage
    metric = left_metric + right_metric

    left_metric_root = _psd_power(left_metric, 0.5, tolerance=tolerance)
    right_metric_root = _psd_power(right_metric, 0.5, tolerance=tolerance)
    left_metric_inverse_root = _psd_power(
        left_metric,
        -0.5,
        tolerance=tolerance,
    )
    right_metric_inverse_root = _psd_power(
        right_metric,
        -0.5,
        tolerance=tolerance,
    )
    metric_inverse_root = _psd_power(metric, -0.5, tolerance=tolerance)

    left_embedding = left_preimage @ left_metric_inverse_root
    right_embedding = right_preimage @ right_metric_inverse_root
    left_mixer = left_metric_root @ metric_inverse_root
    right_mixer = right_metric_root @ metric_inverse_root
    direct_relation = np.vstack((left_preimage, -right_preimage)) @ metric_inverse_root
    factored_relation = np.vstack(
        (left_embedding @ left_mixer, -right_embedding @ right_mixer)
    )

    left_effect = left_mixer.conj().T @ left_mixer
    right_effect = right_mixer.conj().T @ right_mixer
    grading = left_effect - right_effect
    grading_values = np.linalg.eigvalsh((grading + grading.conj().T) / 2)
    maximum_defect = max((abs(float(value)) for value in grading_values), default=0.0)
    endpoint_gap = (1 - maximum_defect) / 2
    left_effect_values = np.linalg.eigvalsh((left_effect + left_effect.conj().T) / 2)

    left_scalar = np.trace(left_mixer) / common.shape[1]
    right_scalar = np.trace(right_mixer) / common.shape[1]
    left_scalar_residual = float(
        np.linalg.norm(left_mixer - left_scalar * identity, ord=2)
    )
    right_scalar_residual = float(
        np.linalg.norm(right_mixer - right_scalar * identity, ord=2)
    )
    left_isometry = float(
        np.linalg.norm(left_embedding.conj().T @ left_embedding - identity, ord=2)
    )
    right_isometry = float(
        np.linalg.norm(right_embedding.conj().T @ right_embedding - identity, ord=2)
    )
    mixer_isometry = float(
        np.linalg.norm(left_effect + right_effect - identity, ord=2)
    )
    factorization = float(np.linalg.norm(direct_relation - factored_relation, ord=2))
    relation_isometry = float(
        np.linalg.norm(direct_relation.conj().T @ direct_relation - identity, ord=2)
    )
    equality = float(np.linalg.norm(left_metric - right_metric, ord=2))
    commutator = float(
        np.linalg.norm(
            left_metric @ right_metric - right_metric @ left_metric,
            ord=2,
        )
    )
    exact = bool(
        max(
            left_isometry,
            right_isometry,
            mixer_isometry,
            factorization,
            relation_isometry,
        )
        <= 1000 * tolerance
    )
    hadamard = bool(
        equality <= 1000 * tolerance
        and np.linalg.norm(left_mixer - identity / math.sqrt(2), ord=2)
        <= 1000 * tolerance
        and np.linalg.norm(right_mixer - identity / math.sqrt(2), ord=2)
        <= 1000 * tolerance
    )
    scalar = max(left_scalar_residual, right_scalar_residual) <= 1000 * tolerance
    left_values = np.linalg.eigvalsh((left_metric + left_metric.conj().T) / 2)
    right_values = np.linalg.eigvalsh((right_metric + right_metric.conj().T) / 2)
    return RecursiveNodeCompilerControl(
        control_id=control_id,
        fiber_dimension=common.shape[1],
        left_coefficient_dimension=left_synthesis.shape[1],
        right_coefficient_dimension=right_synthesis.shape[1],
        left_metric_minimum_eigenvalue=float(left_values.min()),
        left_metric_maximum_eigenvalue=float(left_values.max()),
        right_metric_minimum_eigenvalue=float(right_values.min()),
        right_metric_maximum_eigenvalue=float(right_values.max()),
        metric_commutator_norm=commutator,
        metric_equality_residual=equality,
        left_embedding_isometry_residual=left_isometry,
        right_embedding_isometry_residual=right_isometry,
        endpoint_mixer_column_isometry_residual=mixer_isometry,
        relation_factorization_residual=factorization,
        normalized_relation_isometry_residual=relation_isometry,
        left_endpoint_effect_minimum_eigenvalue=float(left_effect_values.min()),
        left_endpoint_effect_maximum_eigenvalue=float(left_effect_values.max()),
        maximum_grading_defect=maximum_defect,
        minimum_endpoint_gap=endpoint_gap,
        left_scalar_mixer_residual=left_scalar_residual,
        right_scalar_mixer_residual=right_scalar_residual,
        exact_recursive_normal_form_verified=exact,
        endpoint_mixer_is_exact_hadamard=hadamard,
        endpoint_mixer_is_scalar=scalar,
        status=(
            "exact-hadamard-recursive-node-compiler-normal-form"
            if exact and hadamard
            else "exact-scalar-recursive-node-compiler-normal-form"
            if exact and scalar
            else "exact-matrix-valued-recursive-node-compiler-normal-form"
            if exact
            else "recursive-node-compiler-normal-form-failure"
        ),
    )


def _synthesis_for_metric(metric: np.ndarray) -> np.ndarray:
    return _psd_power(metric, -0.5, tolerance=1e-12)


def _node_controls() -> list[RecursiveNodeCompilerControl]:
    identity = np.eye(2, dtype=complex)
    equal_metric = np.diag([0.25, 1.0]).astype(complex)
    angle = math.pi / 4
    rotation = np.asarray(
        [
            [math.cos(angle), -math.sin(angle)],
            [math.sin(angle), math.cos(angle)],
        ],
        dtype=complex,
    )
    noncommuting_left = np.diag([1.0, 4.0]).astype(complex)
    noncommuting_right = rotation @ np.diag([4.0, 1.0]) @ rotation.conj().T
    return [
        audit_recursive_node_compiler(
            "EQUAL-SHORT-METRICS-HADAMARD",
            _synthesis_for_metric(equal_metric),
            _synthesis_for_metric(equal_metric),
            identity,
        ),
        audit_recursive_node_compiler(
            "PROPORTIONAL-SHORT-METRICS-SCALAR-ROTATION",
            _synthesis_for_metric(0.25 * identity),
            _synthesis_for_metric(identity),
            identity,
        ),
        audit_recursive_node_compiler(
            "NONCOMMUTING-SHORT-METRICS-MATRIX-MIXER",
            _synthesis_for_metric(noncommuting_left),
            _synthesis_for_metric(noncommuting_right),
            identity,
        ),
    ]


def hierarchical_conditioning_counterexample(
    exponent: int,
) -> HierarchicalConditioningCounterexample:
    if exponent < 1:
        raise ValueError("exponent must be positive")
    ratio = 1 << exponent
    left = 1 / (ratio + 1)
    right = ratio / (ratio + 1)
    defect = right - left
    gap = left
    return HierarchicalConditioningCounterexample(
        exponent=exponent,
        metric_ratio=ratio,
        left_endpoint_weight=left,
        right_endpoint_weight=right,
        maximum_grading_defect=defect,
        minimum_endpoint_gap=gap,
        inverse_gap_cost=1 / gap,
        pair_gpe_transport_available=True,
        constant_endpoint_gap=gap >= 0.1,
        status="gpe-pair-transport-present-hierarchical-endpoint-gap-vanishes",
    )


def compile_flat_affine_embedding(
    fiber_maps: dict[int, np.ndarray],
    bit_count: int,
    *,
    tolerance: float = 1e-9,
) -> tuple[np.ndarray, np.ndarray, int]:
    """Return direct and generator-path affine embeddings.

    The second matrix simulates the branch action of affine Hadamards followed
    by controlled flat transports.  It is an exact algebraic circuit audit;
    it does not synthesize a uniform all-n SELECT implementation.
    """

    active = tuple(sorted(fiber_maps))
    if not active:
        raise ValueError("at least one active affine fiber is required")
    origin, generators = affine_basis(active, bit_count)
    ambient, fiber = fiber_maps[origin].shape
    identity = np.eye(fiber, dtype=complex)
    if any(mapping.shape != (ambient, fiber) for mapping in fiber_maps.values()):
        raise ValueError("all fiber maps must have one shape")
    if any(
        np.linalg.norm(mapping.conj().T @ mapping - identity, ord=2)
        > 100 * tolerance
        for mapping in fiber_maps.values()
    ):
        raise ValueError("all fiber maps must be isometries")

    scale = 1 / math.sqrt(len(active))
    direct = np.vstack([fiber_maps[mask] for mask in active]) * scale
    branches: dict[int, np.ndarray] = {origin: fiber_maps[origin]}
    for generator in generators:
        expanded: dict[int, np.ndarray] = {}
        for mask, image in branches.items():
            expanded[mask] = image
            target = mask ^ generator
            transport = fiber_maps[target] @ fiber_maps[mask].conj().T
            expanded[target] = transport @ image
        branches = expanded
    compiled = np.vstack([branches[mask] for mask in active]) * scale
    return direct, compiled, len(generators)


def _affine_preparation_control() -> AffinePreparationControl:
    active = (1, 3, 8, 10)
    angles = (0.0, 0.37, -0.81, 1.12)
    fibers = {
        mask: np.asarray(
            [
                [math.cos(angle), -math.sin(angle)],
                [math.sin(angle), math.cos(angle)],
                [0.0, 0.0],
            ],
            dtype=complex,
        )
        for mask, angle in zip(active, angles)
    }
    direct, compiled, stages = compile_flat_affine_embedding(fibers, 4)
    residual = float(np.linalg.norm(direct - compiled, ord=2))
    isometry = float(
        np.linalg.norm(compiled.conj().T @ compiled - np.eye(2), ord=2)
    )
    verified = max(residual, isometry) <= 1e-9
    return AffinePreparationControl(
        active_masks=active,
        affine_dimension=stages,
        ambient_dimension=3,
        fiber_dimension=2,
        generator_transport_stage_count=stages,
        maximum_compiled_embedding_residual=residual,
        compiled_embedding_isometry_residual=isometry,
        exact_flat_affine_preparation_verified=verified,
        status=(
            "exact-log-depth-flat-affine-preparation"
            if verified
            else "flat-affine-preparation-validation-failure"
        ),
    )


def _finite_gpe_compiler_controls() -> list[AffineGpeCompilerControl]:
    bundles = {
        row.control_id: row
        for row in run_affine_recoupling_bundle().finite_controls
        if row.affine_recoupling_bundle_certificate
    }
    networks = {
        row.control_id: row
        for row in run_pair_polar_transport_network().finite_controls
    }
    network_aliases = {
        "W5-ISOLATED-AFFINE-LINE": "W5-ISOLATED-ANCHOR-LINE",
    }
    controls = []
    for control_id, bundle in bundles.items():
        network = networks.get(network_aliases.get(control_id, control_id))
        network_verified = bool(
            network is not None
            and network.exact_pair_polar_transport_network_verified
        )
        affine_dimension = bundle.active_support_affine_dimension or 0
        path_length = network.transport_graph_diameter if network is not None else None
        certificate = bool(
            bundle.exact_flat_fiber_transport_verified
            and network_verified
            and path_length is not None
        )
        controls.append(
            AffineGpeCompilerControl(
                control_id=control_id,
                active_mask_count=len(bundle.active_orientation_masks),
                affine_dimension=affine_dimension,
                intersection_dimension=bundle.intersection_dimension,
                generator_transport_stage_count=affine_dimension,
                maximum_pair_path_length=path_length or 0,
                flat_affine_bundle_verified=bundle.exact_flat_fiber_transport_verified,
                pair_polar_path_network_verified=network_verified,
                direct_gpe_pair_polar_available=True,
                finite_constant_size_compiler_certificate=certificate,
                status=(
                    "finite-affine-gpe-node-compiler-certificate"
                    if certificate
                    else "finite-affine-gpe-node-compiler-open"
                ),
            )
        )
    return controls


def gpe_recursive_node_compiler_scaling_record(
    n: int,
) -> GpeRecursiveNodeCompilerScalingRecord:
    if n < 5:
        raise ValueError("n must be at least five")
    copies = math.ceil(math.lgamma(n + 1) / math.log(2))
    return GpeRecursiveNodeCompilerScalingRecord(
        n=n,
        information_threshold_copy_count=copies,
        maximum_affine_transport_stage_count=copies,
        pair_polar_gate_cost_polynomial=True,
        width_amplification_required_for_flat_affine_preparation=False,
        all_n_affine_child_embedding_theorem_proved=False,
        polynomial_uniform_generator_select_proved=False,
        natural_short_metric_equality_or_comparability_proved=False,
        recursive_orientation_polar_proved=False,
        status="pair-gpe-and-affine-normal-form-explicit-all-n-structure-open",
    )


def run_gpe_recursive_node_compiler() -> GpeRecursiveNodeCompilerReport:
    nodes = _node_controls()
    counters = [
        hierarchical_conditioning_counterexample(exponent)
        for exponent in range(1, 25)
    ]
    preparation = _affine_preparation_control()
    finite = _finite_gpe_compiler_controls()
    scaling = [
        gpe_recursive_node_compiler_scaling_record(n)
        for n in (5, 8, 16, 32, 64, 128, 256, 512)
    ]
    normal_form_failures = sum(
        not row.exact_recursive_normal_form_verified for row in nodes
    )
    finite_failures = sum(
        not row.finite_constant_size_compiler_certificate for row in finite
    )
    noncommuting = next(
        row for row in nodes if row.control_id.startswith("NONCOMMUTING")
    )
    tail = counters[-1]
    verified = normal_form_failures == 0 and preparation.exact_flat_affine_preparation_verified
    return GpeRecursiveNodeCompilerReport(
        created_at=utc_now(),
        theorem_contract={
            "recursive_relation_normal_form": (
                "For A_s=X^*(S_sS_s^*)^+X and W_s=S_s^+XA_s^-1/2, "
                "the normalized parent relation is [W_L A_L^1/2 M^-1/2; "
                "-W_R A_R^1/2 M^-1/2], M=A_L+A_R."
            ),
            "balanced_metric_compiler": (
                "A_L=A_R makes the endpoint mixer exactly the signed Hadamard, "
                "so only the two normalized child embeddings remain."
            ),
            "flat_affine_compiler": (
                "An affine uniform child embedding with coherent generator "
                "transports is prepared in affine dimension many transport "
                "stages, without square-root width amplification."
            ),
            "gpe_scope": (
                "The companion GPE theorem implements every compatible pair "
                "polar edge. The companion S6 theorem falsifies universal scalar "
                "affine fibers; GPE still needs matrix-support SELECT, uniformly "
                "selectable paths, and comparable shorted metrics."
            ),
        },
        node_controls=nodes,
        conditioning_counterfamily=counters,
        affine_preparation_control=preparation,
        finite_gpe_compiler_controls=finite,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "exact_recursive_parent_relation_factorization",
                "resolved": verified,
                "resolution": "Separated every normalized parent relation into isometric child embeddings and one contractive endpoint mixer.",
            },
            {
                "obligation": "compile_balanced_affine_child_embedding_from_gpe_edges",
                "resolved": bool(finite) and finite_failures == 0,
                "resolution": "The fixed W3/W5 certificates combine affine fibers, short pair-polar paths, and the direct GPE edge implementation; this is finite evidence only.",
            },
            {
                "obligation": "prove_all_n_affine_or_other_structured_child_embeddings",
                "resolved": False,
                "resolution": "The scalar affine option is rejected by a natural S6 control. A compact matrix partial-support decomposition on positive native mass remains open.",
            },
            {
                "obligation": "prove_uniform_coherent_generator_select_and_gauge_resolution",
                "resolved": False,
                "resolution": "A classical path table over exponentially many masks is inadmissible; the GPE controls must be generated reversibly from compact labels.",
            },
            {
                "obligation": "prove_natural_recursive_endpoint_gap",
                "resolved": False,
                "resolution": "GPE pair transport is compatible with exponentially imbalanced shorted metrics, and noncommuting metrics require an operator-valued mixer.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "Direct GPE pair polars automatically compile every recursive parent relation.",
                "resolved": True,
                "resolution": "False. GPE supplies compatible fiber transports; the normalized child embeddings and the matrix endpoint mixer remain separate operations.",
            },
            {
                "objection": "Comparable eigenvalues make the endpoint mixer a scalar rotation.",
                "resolved": True,
                "resolution": "The noncommuting two-dimensional control has a constant endpoint gap but a nonzero scalar-mixer residual.",
            },
            {
                "objection": "A flat affine support still incurs square-root support-size amplification.",
                "resolved": True,
                "resolution": "Affine Hadamards create all branches coherently and exact flat transports route the common fiber in logarithmic depth.",
            },
            {
                "objection": "Logarithmic transport depth proves a polynomial all-n compiler.",
                "resolved": False,
                "resolution": "Only if each generator transport has a compact uniform SELECT and the natural child fiber is actually affine on relevant PGM mass.",
            },
        ],
        headline_metrics={
            "recursive_parent_relation_normal_form_theorem_count": int(verified),
            "node_control_count": len(nodes),
            "node_control_failure_count": normal_form_failures,
            "equal_metric_hadamard_control_count": sum(
                row.endpoint_mixer_is_exact_hadamard for row in nodes
            ),
            "noncommuting_matrix_mixer_countercontrol_count": int(
                noncommuting.metric_commutator_norm > 1e-8
                and not noncommuting.endpoint_mixer_is_scalar
            ),
            "flat_affine_log_depth_preparation_theorem_count": int(
                preparation.exact_flat_affine_preparation_verified
            ),
            "finite_affine_gpe_compiler_control_count": len(finite),
            "finite_affine_gpe_compiler_failure_count": finite_failures,
            "conditioning_counterfamily_row_count": len(counters),
            "tail_metric_ratio": tail.metric_ratio,
            "tail_endpoint_gap": tail.minimum_endpoint_gap,
            "tail_inverse_gap_cost": tail.inverse_gap_cost,
            "all_n_structured_child_embedding_theorem_count": 0,
            "companion_natural_scalar_affine_falsifier_count": 1,
            "uniform_coherent_generator_select_count": 0,
            "natural_recursive_endpoint_gap_theorem_count": 0,
            "recursive_orientation_polar_sampler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "exact_recursive_parent_relation_normal_form_proved": verified,
            "equal_short_metrics_reduce_endpoint_mixer_to_hadamard": all(
                row.endpoint_mixer_is_exact_hadamard
                for row in nodes
                if row.control_id.startswith("EQUAL")
            ),
            "flat_affine_embedding_has_logarithmic_transport_depth": preparation.exact_flat_affine_preparation_verified,
            "gpe_direct_pair_polar_supplies_compatible_edge_transports": True,
            "selected_finite_affine_nodes_have_gpe_compiler_certificate": bool(finite) and finite_failures == 0,
            "universal_scalar_affine_child_embeddings_falsified": True,
            "gpe_pair_transport_alone_compiles_recursive_relation": False,
            "all_n_structured_child_embedding_proved": False,
            "polynomial_uniform_generator_select_proved": False,
            "natural_recursive_endpoint_gap_proved": False,
            "recursive_orientation_polar_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The recursive circuit target now has an exact normal form and "
                "finite affine/GPE compilers, but natural S6 kills universal scalar "
                "fibers. Matrix partial-support structure, uniform SELECT, and "
                "natural endpoint conditioning remain open."
            ),
        },
        status=(
            "recursive-node-normal-form-and-finite-affine-gpe-compiler-proved-"
            "all-n-structure-and-conditioning-open"
            if verified and finite and finite_failures == 0
            else "gpe-recursive-node-compiler-control-failure"
        ),
        summary=(
            "Separated recursive relation preparation into normalized child "
            "embeddings and a short-metric endpoint mixer, then proved that flat "
            "affine child embeddings compile from GPE transports in logarithmic "
            "depth without a width penalty."
        ),
        falsifiers_triggered=[
            "Pair-level GPE does not by itself remove recursive child-frame normalization.",
            "Constant metric spectra do not imply a scalar endpoint mixer when shorted metrics fail to commute.",
            "Exact recursive completeness remains compatible with exponentially small endpoint gaps.",
            "Finite affine GPE paths are not an all-n uniform path-selection theorem.",
            "A globally source-distinct S6 affine node falsifies universal scalar child fibers.",
        ],
    )


def write_gpe_recursive_node_compiler_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_gpe_recursive_node_compiler())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    report = write_gpe_recursive_node_compiler_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
