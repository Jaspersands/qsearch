"""Exact coarse-graining identity for the point-quotient PGM.

The point states are uniform mixtures of the retained fine-label states,

    omega_j = |H|^-1 sum_(g:g(point)=j) tau_g,

with prior ``1/n``.  Both the fine and coarse ensembles have the same average
state ``bar(tau)``.  If ``M_g`` is the fine pretty-good measurement (PGM), then
the point PGM effect is exactly

    E_j = sum_(g:g(point)=j) M_g.                         (1)

Indeed each PGM effect is the average-state inverse square root sandwich of
the corresponding prior-weighted state, and prior-weighted coarse states are
the sums of their fine counterparts.  The identity also holds on the kernel
of the average after distributing the unused support complement according to
the priors.

Operationally, any implementation of the full covariant PGM can be followed
by reversible evaluation of ``g(point)`` and discarding the rest of ``g``.
Thus point-PGM implementation does not intrinsically require square roots of
the Young child-star effects.  For the retained joint-character state it
inherits the existing full-PGM bottleneck: coherent inverse square roots of
the multiplicity operators ``D_nu``, equivalently the orientation projection
Gram kernels.

Equation (1) does not show that the full PGM is efficient.  Nor does it rule
out a direct coarse measurement that bypasses a hard fine-label inverse.  It
corrects the research frontier: a child-star square-root compiler is an
alternative possible bypass, not a prerequisite for point decoding.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_joint_character_correlation_decoder import (
    _permutations,
    joint_character_state,
    left_covariant_state,
)
from self_dual_wreath_orientation_fourier_reduction import _w4_collision_free_labels
from self_dual_wreath_point_stabilizer_quotient import point_quotient_states


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_point_pgm_coarse_graining.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-POINT-PGM-COARSE-GRAINING"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Label = tuple[Partition, Partition]


@dataclass(frozen=True)
class PointPGMCoarseGrainingControl:
    control_id: str
    n: int
    labels: tuple[Label, ...]
    fine_hypothesis_count: int
    point_hypothesis_count: int
    point_fiber_size: int
    copy_count: int
    register_dimension: int
    average_support_rank: int
    maximum_coarse_state_aggregation_residual: float
    maximum_coarse_effect_aggregation_residual: float
    maximum_mapped_confusion_residual: float
    fine_povm_completeness_residual: float
    point_povm_completeness_residual: float
    fine_pgm_success: float
    mapped_fine_pgm_point_success: float
    direct_point_pgm_success: float
    within_fiber_error_recovery_gain: float
    exact_point_pgm_coarse_graining_verified: bool
    status: str


@dataclass(frozen=True)
class PointPGMCoarseGrainingScalingRecord:
    n: int
    fine_hypothesis_count_decimal: str
    point_hypothesis_count: int
    point_fiber_size_decimal: str
    fine_output_register_qubits: int
    point_output_register_qubits: int
    reversible_point_image_evaluation_polynomial: bool
    child_star_square_root_required_for_inherited_route: bool
    full_covariant_multiplicity_inverse_required: bool
    full_covariant_multiplicity_inverse_compiled: bool
    direct_coarse_bypass_ruled_out: bool
    polynomial_point_pgm_circuit_proved: bool
    status: str


@dataclass(frozen=True)
class PointPGMCoarseGrainingTheorem:
    prior_weighted_identity: str
    effect_identity: str
    operational_reduction: str
    inherited_bottleneck: str
    alternative_route: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class PointPGMCoarseGrainingReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: PointPGMCoarseGrainingTheorem
    finite_controls: list[PointPGMCoarseGrainingControl]
    scaling_records: list[PointPGMCoarseGrainingScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _psd_inverse_sqrt_and_support(
    matrix: np.ndarray,
    tolerance: float,
) -> tuple[np.ndarray, np.ndarray, int]:
    hermitian = (matrix + matrix.conj().T) / 2
    eigenvalues, eigenvectors = np.linalg.eigh(hermitian)
    if eigenvalues[0] < -100 * tolerance:
        raise ValueError("matrix must be positive semidefinite")
    positive = eigenvalues > tolerance
    inverse_values = np.zeros_like(eigenvalues)
    inverse_values[positive] = eigenvalues[positive] ** -0.5
    inverse = (eigenvectors * inverse_values) @ eigenvectors.conj().T
    support = (
        eigenvectors[:, positive] @ eigenvectors[:, positive].conj().T
    )
    return inverse, support, int(np.count_nonzero(positive))


def pretty_good_effects(
    states: tuple[np.ndarray, ...],
    *,
    tolerance: float = 1e-10,
) -> tuple[tuple[np.ndarray, ...], np.ndarray, int]:
    """Return an exact full-space PGM for a uniform ensemble."""

    if not states or any(state.shape != states[0].shape for state in states):
        raise ValueError("states must be a nonempty equal-shape tuple")
    count = len(states)
    average = sum(states) / count
    inverse, support, rank = _psd_inverse_sqrt_and_support(average, tolerance)
    complement = np.eye(len(average), dtype=complex) - support
    effects = tuple(
        inverse @ state @ inverse / count + complement / count
        for state in states
    )
    return effects, average, rank


def aggregate_by_fibers(
    matrices: tuple[np.ndarray, ...],
    fibers: tuple[tuple[int, ...], ...],
    *,
    average: bool,
) -> tuple[np.ndarray, ...]:
    """Aggregate matrices over an equal-size partition of their indices."""

    if not matrices or not fibers:
        raise ValueError("matrices and fibers must be nonempty")
    flattened = tuple(index for fiber in fibers for index in fiber)
    if sorted(flattened) != list(range(len(matrices))):
        raise ValueError("fibers must partition the matrix indices")
    sizes = {len(fiber) for fiber in fibers}
    if len(sizes) != 1 or 0 in sizes:
        raise ValueError("fibers must have one common positive size")
    scale = next(iter(sizes)) if average else 1
    zero = np.zeros_like(matrices[0])
    return tuple(
        sum((matrices[index] for index in fiber), zero.copy()) / scale
        for fiber in fibers
    )


def _success(
    effects: tuple[np.ndarray, ...],
    states: tuple[np.ndarray, ...],
) -> float:
    if len(effects) != len(states):
        raise ValueError("effects and states must have equal length")
    return sum(
        float(np.trace(effect @ state).real)
        for effect, state in zip(effects, states)
    ) / len(states)


def _confusion(
    effects: tuple[np.ndarray, ...],
    states: tuple[np.ndarray, ...],
) -> np.ndarray:
    return np.asarray(
        [
            [float(np.trace(effect @ state).real) for effect in effects]
            for state in states
        ]
    )


def audit_point_pgm_coarse_graining(
    n: int,
    labels: tuple[Label, ...],
    *,
    control_id: str,
    point: int | None = None,
    tolerance: float = 1e-9,
) -> PointPGMCoarseGrainingControl:
    """Verify equation (1) on a retained joint-character ensemble."""

    if point is None:
        point = n - 1
    permutations = _permutations(n)
    index_fibers = tuple(
        tuple(
            index
            for index, permutation in enumerate(permutations)
            if permutation[point] == image
        )
        for image in range(n)
    )
    character_count = 1 << len(labels)
    base = joint_character_state(labels, tuple(range(n)))
    fine_states = tuple(
        left_covariant_state(base, permutations, hidden, character_count)
        for hidden in permutations
    )
    aggregated_states = aggregate_by_fibers(
        fine_states,
        index_fibers,
        average=True,
    )
    direct_states = point_quotient_states(labels, point=point)
    state_residual = max(
        float(np.linalg.norm(observed - predicted, ord=2))
        for observed, predicted in zip(direct_states, aggregated_states)
    )

    fine_effects, fine_average, support_rank = pretty_good_effects(
        fine_states,
        tolerance=tolerance,
    )
    direct_effects, point_average, _ = pretty_good_effects(
        direct_states,
        tolerance=tolerance,
    )
    aggregated_effects = aggregate_by_fibers(
        fine_effects,
        index_fibers,
        average=False,
    )
    effect_residual = max(
        float(np.linalg.norm(observed - predicted, ord=2))
        for observed, predicted in zip(direct_effects, aggregated_effects)
    )
    direct_confusion = _confusion(direct_effects, direct_states)
    mapped_confusion = _confusion(aggregated_effects, direct_states)
    confusion_residual = float(np.linalg.norm(direct_confusion - mapped_confusion))
    identity = np.eye(len(base))
    fine_completeness = float(np.linalg.norm(sum(fine_effects) - identity, ord=2))
    point_completeness = float(
        np.linalg.norm(sum(direct_effects) - identity, ord=2)
    )
    fine_success = _success(fine_effects, fine_states)
    mapped_success = _success(aggregated_effects, direct_states)
    direct_success = _success(direct_effects, direct_states)
    average_residual = float(np.linalg.norm(fine_average - point_average, ord=2))
    verified = bool(
        state_residual <= 100 * tolerance
        and effect_residual <= 100 * tolerance
        and confusion_residual <= 100 * tolerance
        and average_residual <= 100 * tolerance
        and fine_completeness <= 100 * tolerance
        and point_completeness <= 100 * tolerance
        and abs(mapped_success - direct_success) <= 100 * tolerance
        and mapped_success + 100 * tolerance >= fine_success
    )
    return PointPGMCoarseGrainingControl(
        control_id=control_id,
        n=n,
        labels=labels,
        fine_hypothesis_count=len(permutations),
        point_hypothesis_count=n,
        point_fiber_size=math.factorial(n - 1),
        copy_count=len(labels),
        register_dimension=len(base),
        average_support_rank=support_rank,
        maximum_coarse_state_aggregation_residual=state_residual,
        maximum_coarse_effect_aggregation_residual=effect_residual,
        maximum_mapped_confusion_residual=confusion_residual,
        fine_povm_completeness_residual=fine_completeness,
        point_povm_completeness_residual=point_completeness,
        fine_pgm_success=fine_success,
        mapped_fine_pgm_point_success=mapped_success,
        direct_point_pgm_success=direct_success,
        within_fiber_error_recovery_gain=mapped_success - fine_success,
        exact_point_pgm_coarse_graining_verified=verified,
        status=(
            "exact-point-pgm-coarse-graining"
            if verified
            else "point-pgm-coarse-graining-validation-failure"
        ),
    )


def point_pgm_coarse_graining_scaling_record(
    n: int,
) -> PointPGMCoarseGrainingScalingRecord:
    if n < 2:
        raise ValueError("n must be at least two")
    return PointPGMCoarseGrainingScalingRecord(
        n=n,
        fine_hypothesis_count_decimal=str(math.factorial(n)),
        point_hypothesis_count=n,
        point_fiber_size_decimal=str(math.factorial(n - 1)),
        fine_output_register_qubits=math.ceil(math.lgamma(n + 1) / math.log(2)),
        point_output_register_qubits=math.ceil(math.log2(n)),
        reversible_point_image_evaluation_polynomial=True,
        child_star_square_root_required_for_inherited_route=False,
        full_covariant_multiplicity_inverse_required=True,
        full_covariant_multiplicity_inverse_compiled=False,
        direct_coarse_bypass_ruled_out=False,
        polynomial_point_pgm_circuit_proved=False,
        status="point-pgm-reduces-to-full-pgm-multiplicity-inverse",
    )


def run_point_pgm_coarse_graining() -> PointPGMCoarseGrainingReport:
    threshold_labels = (
        ((3,), (2, 1)),
        ((3,), (1, 1, 1)),
        ((2, 1), (1, 1, 1)),
    )
    controls = [
        audit_point_pgm_coarse_graining(
            3,
            (((3,), (2, 1)),),
            control_id="W3-SINGLE-UNEQUAL",
        ),
        audit_point_pgm_coarse_graining(
            3,
            threshold_labels,
            control_id="W3-INFORMATION-THRESHOLD",
        ),
        audit_point_pgm_coarse_graining(
            4,
            _w4_collision_free_labels()[0],
            control_id="W4-COLLISION-FREE-PAIR",
        ),
    ]
    scaling = [
        point_pgm_coarse_graining_scaling_record(n)
        for n in (8, 16, 32, 64, 128)
    ]
    failures = sum(
        not row.exact_point_pgm_coarse_graining_verified for row in controls
    )
    verified = failures == 0
    theorem = PointPGMCoarseGrainingTheorem(
        prior_weighted_identity=(
            "p_j omega_j=sum_(g:g(point)=j) p_g tau_g for uniform fine labels."
        ),
        effect_identity=(
            "E_j^point=sum_(g:g(point)=j) M_g^fine, including the average-state "
            "kernel complement distributed by the priors."
        ),
        operational_reduction=(
            "Run the full covariant PGM, reversibly compute g(point), and discard "
            "the remaining fine label."
        ),
        inherited_bottleneck=(
            "For retained joint-character states the route inherits controlled "
            "D_nu^-1/2, equivalently orientation projection-Gram inversion."
        ),
        alternative_route=(
            "A direct Young child-star measurement could still bypass a hard fine "
            "inverse; the coarse-graining identity neither supplies nor rules it out."
        ),
        scope=(
            "This is an exact PGM identity and implementation reduction, not a "
            "polynomial PGM compiler, point decoder, or speedup."
        ),
        theorem_verified=verified,
        status=(
            "point-pgm-exactly-coarse-grained-full-pgm"
            if verified
            else "point-pgm-coarse-graining-validation-failure"
        ),
    )
    return PointPGMCoarseGrainingReport(
        created_at=utc_now(),
        theorem_contract=asdict(theorem),
        theorem=theorem,
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "identify_point_pgm_inside_fine_covariant_pgm",
                "resolved": verified,
                "resolution": (
                    "Linearity in prior-weighted states makes every point effect "
                    "the exact sum of its fine-label PGM effects."
                ),
            },
            {
                "obligation": "compile_full_multiplicity_inverse",
                "resolved": False,
                "resolution": (
                    "No controlled all-n inverse square root for the natural "
                    "D_nu orientation kernels is proved."
                ),
            },
            {
                "obligation": "compare_direct_coarse_and_refined_implementation_cost",
                "resolved": False,
                "resolution": (
                    "A direct child-star transform might avoid resolving fine labels "
                    "and could be easier than the inherited full PGM."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "A point PGM necessarily requires a new child-star square root.",
                "resolved": True,
                "resolution": (
                    "False. Coarse-graining a full PGM implements exactly the same "
                    "point effects."
                ),
            },
            {
                "objection": "The identity proves an efficient point PGM.",
                "resolved": True,
                "resolution": (
                    "False. It transfers the unresolved full-PGM multiplicity inverse."
                ),
            },
            {
                "objection": "A hard full PGM implies every direct point measurement is hard.",
                "resolved": True,
                "resolution": (
                    "False. Coarse measurements can admit implementations that do not "
                    "realize their fine refinements."
                ),
            },
        ],
        headline_metrics={
            "exact_coarse_graining_theorem_count": 1,
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "child_star_square_roots_avoided_by_inherited_route": 1,
            "full_multiplicity_inverse_compiler_count": 0,
            "polynomial_point_pgm_circuit_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "point_pgm_equals_coarse_grained_full_pgm": verified,
            "reversible_point_image_postprocessing_polynomial": True,
            "child_star_square_root_logically_required": False,
            "full_covariant_multiplicity_inverse_compiled": False,
            "direct_coarse_bypass_ruled_out": False,
            "polynomial_point_pgm_circuit_proved": False,
            "polynomial_full_hidden_shift_decoder_proved": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The exact reduction removes a duplicate measurement bottleneck but "
                "inherits the unresolved orientation-kernel inverse."
            ),
        },
        status=theorem.status,
        summary=(
            "Proved that the point PGM is exactly the full retained-state PGM with "
            "its output coarse-grained by point image. This redirects the inherited "
            "route to D_nu inversion while leaving direct coarse bypasses open."
        ),
        falsifiers_triggered=[
            (
                "A separate child-star square-root compiler is not necessary if the "
                "full covariant PGM can be implemented."
            ),
            (
                "Removing the child-star prerequisite does not remove the natural "
                "orientation multiplicity-inverse bottleneck."
            ),
            (
                "Fine-PGM hardness cannot be promoted into a direct coarse-measurement "
                "lower bound."
            ),
        ],
    )


def write_point_pgm_coarse_graining_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-POINT-PGM-COARSE-GRAINING"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_point_pgm_coarse_graining" in globals():
        report = run_point_pgm_coarse_graining(**kwargs)
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
                id="NEG-SELF-DUAL-WREATH-POINT-PGM-COARSE-GRAINING",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-POINT-PGM-COARSE-GRAINING.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-POINT-PGM-COARSE-GRAINING.",
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
                    "self_dual_wreath_point_pgm_coarse_graining": str(path)
                },
            )
        )
    return payload
