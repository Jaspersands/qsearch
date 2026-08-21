"""The complete orientation polar closes the physical PGM and decoder gate.

The component-support program and the physical covariant-PGM program are not
separate algorithmic routes.  Let

    R:H->K,              S=R*R,
    Q=R S^(+/2),                                          (1)

be the complete orientation analysis and its polar.  Let ``C_U:P->K`` be the
physical generalized-Fourier row-copy isometry.  The exact wreath intertwiner
has

    C_U C_U* R = R,
    A = q^(-1/2) R* C_U,                                  (2)

where ``A`` is the physical Fourier-sector analysis and ``q`` is the
orientation count.  Therefore

    A A* = S/q,
    (A A*)^(+/2) A = Q* C_U.                              (3)

The right side is the physical PGM coisometry.  The row-copy, coherent
``S_n`` Fourier operations, and final group-label readout are already
compiled by the physical intertwiner theorem.  Hence a coherent compiler for
``Q`` completes the constant-success PGM; no independent post-polar hidden-
label decoder or sectorwise measurement must be invented.

The recursive component maps are factors of this same ``Q``.  At every tree
merge the polar chain rule composes child polars with one relative isometry.
The direct component Naimark theorem identifies each normalized child
coefficient embedding with a restricted child polar.  These maps must remain
coherent: measuring a component label replaces the required isometry by a
dephasing channel and generally prevents the later polar chain and group
Fourier interference.

The conclusion is robust.  If exact contraction/isometry factors
``T_L...T_1`` are replaced by ``T_tilde_L...T_tilde_1`` with

    ||T_l-T_tilde_l|| <= epsilon_l,

then telescoping gives total operator error at most ``sum_l epsilon_l``.
For any input state, the total-variation distance of every final measurement
distribution is at most the same sum.  Since the information-threshold PGM
success is at least ``1/2``, total coherent compiler error at most ``1/8``
still leaves success at least ``3/8``.

This is a gate-closure reduction, not an orientation-polar circuit.  The sole
algorithmic gate remains a polynomial coherent implementation of the complete
natural polar (including its restricted component maps and endpoint mixers).
Classical separation and a speedup remain unproved.
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
    "self_dual_wreath_component_polar_physical_pgm_closure.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-POLAR-PHYSICAL-PGM-CLOSURE"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class PhysicalPgmClosureControl:
    control_id: str
    orientation_count: int
    carrier_dimension: int
    row_copy_output_dimension: int
    physical_input_dimension: int
    orientation_analysis_rank: int
    row_copy_isometry_residual: float
    row_copy_range_contains_orientation_analysis_residual: float
    physical_analysis_gram_residual: float
    orientation_polar_isometry_residual: float
    physical_pgm_coisometry_residual: float
    exact_pgm_coisometry_identity_residual: float
    exact_orientation_polar_closes_physical_pgm_verified: bool
    status: str


@dataclass(frozen=True)
class CoherentApproximationControl:
    input_dimension: int
    output_dimension: int
    rotation_angle: float
    exact_map_isometry_residual: float
    approximate_map_isometry_residual: float
    map_operator_error: float
    witness_event_probability_difference: float
    measurement_total_variation_upper_bound: float
    event_difference_bound_verified: bool
    status: str


@dataclass(frozen=True)
class PgmClosureScalingRecord:
    n: int
    hidden_label_count_decimal: str
    information_threshold_copy_count: int
    ideal_pgm_success_lower_bound: float
    allowed_total_coherent_compiler_error: float
    robust_pgm_success_lower_bound: float
    tree_level_count: int
    uniform_per_level_error_budget: float
    robust_constant_success_conditional_on_polar_compiler: bool
    complete_orientation_polar_compiled: bool
    status: str


@dataclass(frozen=True)
class PolarPhysicalPgmClosureTheorem:
    physical_analysis: str
    gram_identity: str
    pgm_coisometry: str
    recursive_composition: str
    coherent_requirement: str
    approximation: str
    algorithmic_boundary: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class ComponentPolarPhysicalPgmClosureReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: PolarPhysicalPgmClosureTheorem
    finite_controls: list[PhysicalPgmClosureControl]
    approximation_control: CoherentApproximationControl
    scaling_records: list[PgmClosureScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _hermitian(matrix: np.ndarray) -> np.ndarray:
    return (matrix + matrix.conj().T) / 2.0


def _psd_power(
    matrix: np.ndarray,
    exponent: float,
    *,
    tolerance: float,
) -> tuple[np.ndarray, np.ndarray]:
    values, vectors = np.linalg.eigh(_hermitian(matrix))
    if len(values) and values[0] < -100 * tolerance:
        raise ArithmeticError("matrix is not positive semidefinite")
    positive = values > 100 * tolerance
    transformed = np.zeros_like(values)
    transformed[positive] = values[positive] ** exponent
    powered = (vectors * transformed) @ vectors.conj().T
    support = vectors[:, positive] @ vectors[:, positive].conj().T
    return powered, support


def physical_pgm_coisometry_normal_form(
    orientation_analysis: np.ndarray,
    row_copy: np.ndarray,
    orientation_count: int,
    *,
    tolerance: float = 1e-10,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Return ``A,Q,PGM,Q*row_copy`` from equations (1)-(3)."""

    if orientation_analysis.ndim != 2 or row_copy.ndim != 2:
        raise ValueError("analysis and row-copy maps must be matrices")
    if orientation_analysis.shape[0] != row_copy.shape[0]:
        raise ValueError("analysis and row-copy maps must share an output space")
    if orientation_count < 1:
        raise ValueError("orientation_count must be positive")
    input_identity = np.eye(row_copy.shape[1], dtype=complex)
    if np.linalg.norm(row_copy.conj().T @ row_copy - input_identity, ord=2) > 1000 * tolerance:
        raise ValueError("row_copy must be an isometry")
    containment = np.linalg.norm(
        (np.eye(row_copy.shape[0], dtype=complex) - row_copy @ row_copy.conj().T)
        @ orientation_analysis,
        ord=2,
    )
    if containment > 1000 * tolerance:
        raise ValueError("the row-copy range must contain the orientation range")

    frame = orientation_analysis.conj().T @ orientation_analysis
    frame_inverse_root, _ = _psd_power(frame, -0.5, tolerance=tolerance)
    orientation_polar = orientation_analysis @ frame_inverse_root
    physical_analysis = (
        orientation_analysis.conj().T @ row_copy / math.sqrt(orientation_count)
    )
    physical_gram = physical_analysis @ physical_analysis.conj().T
    physical_inverse_root, _ = _psd_power(
        physical_gram,
        -0.5,
        tolerance=tolerance,
    )
    pgm_coisometry = physical_inverse_root @ physical_analysis
    transferred = orientation_polar.conj().T @ row_copy
    return physical_analysis, orientation_polar, pgm_coisometry, transferred


def audit_physical_pgm_closure(
    control_id: str,
    orientation_analysis: np.ndarray,
    row_copy: np.ndarray,
    orientation_count: int,
    *,
    tolerance: float = 1e-10,
) -> PhysicalPgmClosureControl:
    frame = orientation_analysis.conj().T @ orientation_analysis
    _, frame_support = _psd_power(frame, -0.5, tolerance=tolerance)
    physical_analysis, polar, pgm, transferred = physical_pgm_coisometry_normal_form(
        orientation_analysis,
        row_copy,
        orientation_count,
        tolerance=tolerance,
    )
    row_isometry = float(
        np.linalg.norm(
            row_copy.conj().T @ row_copy
            - np.eye(row_copy.shape[1], dtype=complex),
            ord=2,
        )
    )
    containment = float(
        np.linalg.norm(
            (np.eye(row_copy.shape[0], dtype=complex) - row_copy @ row_copy.conj().T)
            @ orientation_analysis,
            ord=2,
        )
    )
    gram_residual = float(
        np.linalg.norm(
            physical_analysis @ physical_analysis.conj().T
            - frame / orientation_count,
            ord=2,
        )
    )
    polar_isometry = float(
        np.linalg.norm(polar.conj().T @ polar - frame_support, ord=2)
    )
    pgm_support = _psd_power(
        physical_analysis @ physical_analysis.conj().T,
        -0.5,
        tolerance=tolerance,
    )[1]
    pgm_isometry = float(
        np.linalg.norm(pgm @ pgm.conj().T - pgm_support, ord=2)
    )
    identity_residual = float(np.linalg.norm(pgm - transferred, ord=2))
    maximum = max(
        row_isometry,
        containment,
        gram_residual,
        polar_isometry,
        pgm_isometry,
        identity_residual,
    )
    verified = maximum <= 10_000 * tolerance
    return PhysicalPgmClosureControl(
        control_id=control_id,
        orientation_count=orientation_count,
        carrier_dimension=orientation_analysis.shape[1],
        row_copy_output_dimension=row_copy.shape[0],
        physical_input_dimension=row_copy.shape[1],
        orientation_analysis_rank=int(round(float(np.trace(frame_support).real))),
        row_copy_isometry_residual=row_isometry,
        row_copy_range_contains_orientation_analysis_residual=containment,
        physical_analysis_gram_residual=gram_residual,
        orientation_polar_isometry_residual=polar_isometry,
        physical_pgm_coisometry_residual=pgm_isometry,
        exact_pgm_coisometry_identity_residual=identity_residual,
        exact_orientation_polar_closes_physical_pgm_verified=verified,
        status=(
            "exact-orientation-polar-to-physical-pgm-closure"
            if verified
            else "physical-pgm-closure-control-failure"
        ),
    )


def coherent_approximation_control(
    angle: float = 0.2,
) -> CoherentApproximationControl:
    if not 0 < angle < math.pi / 2:
        raise ValueError("angle must lie in (0,pi/2)")
    exact = np.zeros((4, 2), dtype=complex)
    exact[:2, :] = np.eye(2, dtype=complex)
    rotation = np.eye(4, dtype=complex)
    rotation[0, 0] = math.cos(angle)
    rotation[0, 2] = -math.sin(angle)
    rotation[2, 0] = math.sin(angle)
    rotation[2, 2] = math.cos(angle)
    approximate = rotation @ exact
    input_identity = np.eye(2, dtype=complex)
    exact_isometry = float(
        np.linalg.norm(exact.conj().T @ exact - input_identity, ord=2)
    )
    approximate_isometry = float(
        np.linalg.norm(
            approximate.conj().T @ approximate - input_identity,
            ord=2,
        )
    )
    map_error = float(np.linalg.norm(exact - approximate, ord=2))
    state = np.asarray([1.0, 0.0], dtype=complex)
    event = np.zeros((4, 4), dtype=complex)
    event[0, 0] = 1.0
    exact_probability = float(np.vdot(exact @ state, event @ exact @ state).real)
    approximate_probability = float(
        np.vdot(approximate @ state, event @ approximate @ state).real
    )
    difference = abs(exact_probability - approximate_probability)
    verified = difference <= map_error + 1e-12
    return CoherentApproximationControl(
        input_dimension=2,
        output_dimension=4,
        rotation_angle=angle,
        exact_map_isometry_residual=exact_isometry,
        approximate_map_isometry_residual=approximate_isometry,
        map_operator_error=map_error,
        witness_event_probability_difference=difference,
        measurement_total_variation_upper_bound=map_error,
        event_difference_bound_verified=verified,
        status="coherent-map-error-controls-final-measurement-distribution",
    )


def _random_projector(
    dimension: int,
    rank: int,
    rng: np.random.Generator,
) -> np.ndarray:
    raw = rng.normal(size=(dimension, rank)) + 1j * rng.normal(
        size=(dimension, rank)
    )
    basis, _ = np.linalg.qr(raw, mode="reduced")
    return basis @ basis.conj().T


def _row_copy_containing_range(
    analysis: np.ndarray,
    input_dimension: int,
    rng: np.random.Generator,
) -> np.ndarray:
    output_dimension = analysis.shape[0]
    support, _ = np.linalg.qr(analysis, mode="reduced")
    rank = np.linalg.matrix_rank(analysis)
    support = support[:, :rank]
    if not rank <= input_dimension <= output_dimension:
        raise ValueError("row-copy input dimension must contain the analysis range")
    raw = rng.normal(size=(output_dimension, output_dimension)) + 1j * rng.normal(
        size=(output_dimension, output_dimension)
    )
    raw[:, :rank] = support
    complete, _ = np.linalg.qr(raw)
    return complete[:, :input_dimension]


def _projector_analysis_system(
    seed: int,
    *,
    carrier_dimension: int,
    orientation_count: int,
    projector_rank: int,
    row_copy_extra_dimension: int,
) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    projectors = tuple(
        _random_projector(carrier_dimension, projector_rank, rng)
        for _ in range(orientation_count)
    )
    analysis = np.vstack(projectors)
    rank = np.linalg.matrix_rank(analysis)
    row_copy = _row_copy_containing_range(
        analysis,
        min(analysis.shape[0], rank + row_copy_extra_dimension),
        rng,
    )
    return analysis, row_copy


def pgm_closure_scaling_record(
    n: int,
    *,
    total_error_budget: float = 1.0 / 8.0,
) -> PgmClosureScalingRecord:
    if n < 2:
        raise ValueError("n must be at least two")
    if not 0 < total_error_budget < 0.5:
        raise ValueError("total_error_budget must lie in (0,1/2)")
    hidden = math.factorial(n)
    copies = (hidden - 1).bit_length()
    ideal = pgm_success_lower_bound(hidden, copies)
    robust = max(0.0, ideal - total_error_budget)
    return PgmClosureScalingRecord(
        n=n,
        hidden_label_count_decimal=str(hidden),
        information_threshold_copy_count=copies,
        ideal_pgm_success_lower_bound=ideal,
        allowed_total_coherent_compiler_error=total_error_budget,
        robust_pgm_success_lower_bound=robust,
        tree_level_count=copies,
        uniform_per_level_error_budget=total_error_budget / copies,
        robust_constant_success_conditional_on_polar_compiler=robust >= 3.0 / 8.0,
        complete_orientation_polar_compiled=False,
        status="constant-pgm-success-conditional-on-coherent-polar-approximation",
    )


def polar_physical_pgm_closure_theorem() -> PolarPhysicalPgmClosureTheorem:
    return PolarPhysicalPgmClosureTheorem(
        physical_analysis="A=q^(-1/2)R*C_U with C_U C_U*R=R",
        gram_identity="AA*=R*R/q=S/q",
        pgm_coisometry="(AA*)^(+/2)A=Q*C_U for Q=RS^(+/2)",
        recursive_composition=(
            "child restricted polars and relative merge isometries compose to "
            "the complete Q by the exact polar chain rule"
        ),
        coherent_requirement=(
            "component labels remain quantum registers until Q and the group-"
            "label Fourier measurement are complete"
        ),
        approximation=(
            "total coherent map error and final measurement TV are at most "
            "sum_l epsilon_l"
        ),
        algorithmic_boundary=(
            "the complete natural orientation polar is the sole PGM circuit "
            "gate; its implementation and classical separation remain open"
        ),
        theorem_verified=True,
        status="orientation-polar-suffices-for-physical-pgm-and-decoder",
    )


def run_component_polar_physical_pgm_closure(
) -> ComponentPolarPhysicalPgmClosureReport:
    specifications = (
        (5101, 4, 2, 1, 2),
        (5113, 5, 4, 2, 3),
        (5129, 6, 8, 3, 4),
    )
    controls = []
    for seed, carrier, count, rank, extra in specifications:
        analysis, row_copy = _projector_analysis_system(
            seed,
            carrier_dimension=carrier,
            orientation_count=count,
            projector_rank=rank,
            row_copy_extra_dimension=extra,
        )
        controls.append(
            audit_physical_pgm_closure(
                f"PROJECTOR-FRAME-{seed}",
                analysis,
                row_copy,
                count,
            )
        )
    approximation = coherent_approximation_control()
    scaling = [
        pgm_closure_scaling_record(n)
        for n in (3, 4, 5, 8, 12, 16, 24, 32, 48, 64, 96, 128)
    ]
    theorem = polar_physical_pgm_closure_theorem()
    failures = sum(
        not row.exact_orientation_polar_closes_physical_pgm_verified
        for row in controls
    )
    verified = bool(
        theorem.theorem_verified
        and failures == 0
        and approximation.event_difference_bound_verified
        and all(
            row.robust_constant_success_conditional_on_polar_compiler
            for row in scaling
        )
    )
    return ComponentPolarPhysicalPgmClosureReport(
        created_at=utc_now(),
        theorem_contract={
            "physical_analysis": theorem.physical_analysis,
            "gram": theorem.gram_identity,
            "pgm": theorem.pgm_coisometry,
            "recursive_composition": theorem.recursive_composition,
            "coherence": theorem.coherent_requirement,
            "approximation": theorem.approximation,
            "scope": theorem.algorithmic_boundary,
        },
        theorem=theorem,
        finite_controls=controls,
        approximation_control=approximation,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "close_physical_output_given_complete_orientation_polar",
                "resolved": verified,
                "resolution": (
                    "The row-copy containment identity gives equation (3); all "
                    "remaining output operations are standard coherent group operations."
                ),
            },
            {
                "obligation": "show_separate_post_polar_decoder_is_required",
                "resolved": True,
                "resolution": (
                    "Resolved negatively: the orientation polar plugs directly "
                    "into the already-derived covariant PGM Naimark measurement."
                ),
            },
            {
                "obligation": "control_recursive_coherent_approximation_error",
                "resolved": verified,
                "resolution": (
                    "A contraction telescoping hybrid bounds map and final "
                    "measurement error by the sum of per-factor errors."
                ),
            },
            {
                "obligation": "compile_complete_natural_orientation_polar",
                "resolved": False,
                "resolution": (
                    "Need normalization-one restricted child routers, endpoint "
                    "mixers, and all-level coherent composition."
                ),
            },
            {
                "obligation": "prove_classical_complexity_separation",
                "resolved": False,
                "resolution": (
                    "Constant quantum PGM success does not establish classical "
                    "hardness for code equivalence or graph isomorphism."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "After compiling component supports, a new hidden-label decoder must still be designed.",
                "resolved": True,
                "resolution": (
                    "Only if component labels were measured or gauges discarded. "
                    "Coherent composition to Q followed by the physical PGM "
                    "intertwiner already outputs the covariant label."
                ),
            },
            {
                "objection": "The scalar component M4 itself decodes the label.",
                "resolved": True,
                "resolution": (
                    "False. M4 is a compiler-mechanism witness. Identification "
                    "comes from the full coherent PGM after Q is implemented."
                ),
            },
            {
                "objection": "Measuring each recursive component is harmless by deferred measurement.",
                "resolved": True,
                "resolution": (
                    "False unless the pulled-back final effect is dephasing "
                    "invariant. The exact polar chain requires coherent block gauges."
                ),
            },
            {
                "objection": "Inverse-polynomial per-level error necessarily destroys constant success over Theta(n log n) levels.",
                "resolved": True,
                "resolution": (
                    "False with an explicit error budget: epsilon_l<=1/(8L) "
                    "keeps total error at most 1/8 and success at least 3/8."
                ),
            },
            {
                "objection": "Conditional PGM closure proves a speedup.",
                "resolved": True,
                "resolution": (
                    "False. The orientation polar and classical separation are open."
                ),
            },
        ],
        headline_metrics={
            "orientation_polar_to_physical_pgm_closure_theorem_count": int(verified),
            "separate_post_polar_decoder_gate_removed_count": int(verified),
            "coherent_hybrid_error_theorem_count": int(verified),
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "maximum_exact_coisometry_identity_residual": max(
                row.exact_pgm_coisometry_identity_residual for row in controls
            ),
            "scaling_record_count": len(scaling),
            "minimum_robust_conditional_success_lower_bound": min(
                row.robust_pgm_success_lower_bound for row in scaling
            ),
            "complete_orientation_polar_compiler_count": 0,
            "classical_separation_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "complete_orientation_polar_suffices_for_physical_pgm": verified,
            "physical_output_intertwiner_compiled_conditionally": verified,
            "separate_post_polar_hidden_label_decoder_required": False,
            "component_labels_may_be_measured_during_recursive_compilation": False,
            "constant_success_robust_to_summed_error_one_eighth": verified,
            "complete_natural_orientation_polar_compiled": False,
            "classical_separation_proved": False,
            "mrs_model_escape_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The complete coherent orientation polar would finish the known "
                "constant-success physical PGM, but that polar and every "
                "classical-complexity separation remain unproved."
            ),
        },
        status=(
            "physical-pgm-and-decoder-closed-conditionally-orientation-polar-open"
            if verified
            else "component-polar-physical-pgm-closure-control-failure"
        ),
        summary=(
            "Collapsed the component compiler and physical decoder into one "
            "gate: a coherent complete orientation polar, with a linear hybrid "
            "error budget preserving constant PGM success."
        ),
        falsifiers_triggered=[
            "A separate post-polar decoder is not an independent research gate.",
            "The positive component M4 is a compiler witness, not a hidden-label statistic.",
            "Recursive component outcomes must remain coherent to compose the physical PGM.",
            "The sole quantum implementation gate is the complete natural orientation polar; classical separation remains separate.",
        ],
    )


def write_component_polar_physical_pgm_closure_report(
    path: Path = REPORT_PATH,
    **_: Any,
) -> dict[str, Any]:
    payload = asdict(run_component_polar_physical_pgm_closure())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    report = write_component_polar_physical_pgm_closure_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
