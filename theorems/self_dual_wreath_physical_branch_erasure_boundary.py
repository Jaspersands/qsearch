"""Physical branch coherence alone does not implement the orientation polar.

The normalized-analysis no-go does not directly apply when the received wreath
state already contains an orientation register.  This module closes the
simplest resulting loophole: "the branch is already present, so Hadamard it
away."

Let the physical branch carrier be

    K = direct_sum_i |i> tensor S_i,

with every ``S_i`` nonzero.  Consider one-pass branch erasure consisting of a
branch-controlled carrier unitary ``U=direct_sum_i U_i``, a branch-only unitary
``F``, and postselection on one output branch ``j``.  On input branch ``i`` the
Kraus map has norm exactly ``|F[j,i]|``.  If it approximates ``c`` times an
isometry on all of ``K`` with operator error ``epsilon``, then

    epsilon >= max_i ||F[j,i]|-c|
            >= c - 1/sqrt(q),                            (1)

because one row of a unitary has squared norm one.  Exact scaled-isometry
branch erasure therefore satisfies ``|c|^2 <= 1/q``.  A Walsh row attains the
bound.

The strongest stress case is the flat orthogonal frame.  If ``E_i`` are
pairwise orthogonal nonzero projections with ``sum_i E_i=I``, then the frame
analysis

    Q x = sum_i |i> E_i x

is already its exact polar and maps onto all of ``K``.  Equation (1) therefore
applies to the desired polar adjoint itself despite perfect conditioning, zero
support error, and a physical input branch register.  Postselecting ``r``
branch characters can retain at most ``r/q`` of a covariant uniform branch
mixture; keeping ``r=Theta(q)`` avoids postselection loss but does not erase the
orientation information.

The result is deliberately scoped.  It does not cover a circuit that
coherently computes the branch index from the carrier and uncomputes it, a
multi-round representation-specific transform that moves branch information
into an ancilla, or a source image with enforced inter-branch correlations.
Indeed, on the diagonal correlated subspace

    x -> q^-1/2 sum_i |i> x,

a Walsh transform erases the branch deterministically.  A positive physical
factorization must prove that the actual row-copy image has an efficiently
accessible correlation of this kind.  Controlled GPE membership and the
existing physical orientation filter do not prove it: the former preserves
the candidate branch, while the latter retains many nontrivial characters as
outcomes rather than implementing the polar coisometry.
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
    "research/representation/self_dual_wreath_physical_branch_erasure_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-PHYSICAL-BRANCH-ERASURE-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class FlatPolarBranchErasureControl:
    control_id: str
    branch_count: int
    block_dimension: int
    carrier_dimension: int
    flat_frame_gram_residual: float
    polar_isometry_residual: float
    branch_row_minimum_magnitude: float
    branch_row_maximum_magnitude: float
    postselected_scaled_polar_amplitude: float | None
    postselected_success_probability: float | None
    inverse_width_success_upper_bound: float
    scaled_polar_residual: float | None
    exact_inverse_width_boundary_verified: bool
    status: str


@dataclass(frozen=True)
class RobustBranchErasureBound:
    branch_count: int
    requested_isometry_amplitude: float
    unitary_row_magnitudes: tuple[float, ...]
    minimum_row_magnitude: float
    maximum_possible_minimum_row_magnitude: float
    operator_error_lower_bound: float
    constant_amplitude_vanishing_error_possible: bool
    bound_verified: bool
    status: str


@dataclass(frozen=True)
class AcceptedCharacterRankControl:
    branch_count: int
    accepted_character_count: int
    covariant_uniform_branch_acceptance: float
    rank_fraction_upper_bound: float
    branch_label_erased: bool
    constant_acceptance_requires_linear_rank: bool
    status: str


@dataclass(frozen=True)
class CorrelatedInputEscapeControl:
    branch_count: int
    carrier_dimension: int
    diagonal_embedding_isometry_residual: float
    branch_erasure_residual: float
    deterministic_branch_erasure_verified: bool
    flat_orthogonal_full_direct_sum_input: bool
    status: str


@dataclass(frozen=True)
class PhysicalBranchErasureScalingRecord:
    n: int
    information_threshold_copy_count: int
    branch_count_decimal: str
    one_pass_success_probability_log2_upper_bound: int
    amplitude_amplification_query_log2_lower_bound: float
    polynomial_benchmark_degree: int
    polynomial_benchmark_log2: float
    one_pass_erasure_amplification_superpolynomial: bool
    direct_source_correlated_transform_ruled_out: bool
    status: str


@dataclass(frozen=True)
class PhysicalBranchErasureTheorem:
    one_pass_kraus_restriction: str
    robust_error_bound: str
    flat_polar_consequence: str
    accepted_rank_consequence: str
    escape_condition: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class PhysicalBranchErasureBoundaryReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: PhysicalBranchErasureTheorem
    flat_polar_controls: list[FlatPolarBranchErasureControl]
    robust_bounds: list[RobustBranchErasureBound]
    accepted_rank_controls: list[AcceptedCharacterRankControl]
    correlated_escape_controls: list[CorrelatedInputEscapeControl]
    scaling_records: list[PhysicalBranchErasureScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def walsh_matrix(branch_count: int) -> np.ndarray:
    if branch_count < 2 or branch_count & (branch_count - 1):
        raise ValueError("branch_count must be a power of two at least two")
    matrix = np.ones((1, 1), dtype=complex)
    hadamard = np.asarray(((1.0, 1.0), (1.0, -1.0)), dtype=complex)
    while matrix.shape[0] < branch_count:
        matrix = np.kron(matrix, hadamard)
    return matrix / math.sqrt(branch_count)


def _flat_block_bases(
    branch_count: int,
    block_dimension: int,
) -> tuple[np.ndarray, ...]:
    if branch_count < 2 or block_dimension < 1:
        raise ValueError("need at least two nonzero branch blocks")
    carrier_dimension = branch_count * block_dimension
    bases = []
    for branch in range(branch_count):
        basis = np.zeros((carrier_dimension, block_dimension), dtype=complex)
        start = branch * block_dimension
        basis[start : start + block_dimension, :] = np.eye(block_dimension)
        bases.append(basis)
    return tuple(bases)


def _flat_polar_adjoint(
    bases: tuple[np.ndarray, ...],
) -> np.ndarray:
    """Map ``direct_sum_i |i>S_i`` back to the orthogonal carrier sum."""

    branch_count = len(bases)
    carrier_dimension = bases[0].shape[0]
    block_dimension = bases[0].shape[1]
    output = np.zeros(
        (carrier_dimension, branch_count * block_dimension),
        dtype=complex,
    )
    for branch, basis in enumerate(bases):
        block = slice(branch * block_dimension, (branch + 1) * block_dimension)
        output[:, block] = basis
    return output


def audit_flat_polar_branch_erasure(
    branch_count: int,
    block_dimension: int,
    *,
    output_character: int = 0,
    control_id: str = "flat-polar",
    tolerance: float = 1e-10,
) -> FlatPolarBranchErasureControl:
    bases = _flat_block_bases(branch_count, block_dimension)
    carrier_dimension = branch_count * block_dimension
    projectors = tuple(basis @ basis.conj().T for basis in bases)
    frame = sum(projectors, np.zeros((carrier_dimension, carrier_dimension), complex))
    polar_adjoint = _flat_polar_adjoint(bases)
    gram_residual = float(
        np.linalg.norm(frame - np.eye(carrier_dimension), ord=2)
    )
    polar_residual = float(
        np.linalg.norm(
            polar_adjoint.conj().T @ polar_adjoint
            - np.eye(branch_count * block_dimension),
            ord=2,
        )
    )
    branch_unitary = walsh_matrix(branch_count)
    if not 0 <= output_character < branch_count:
        raise ValueError("output character out of range")
    row = branch_unitary[output_character]
    postselected = np.zeros_like(polar_adjoint)
    phase_matched_target = np.zeros_like(polar_adjoint)
    for branch, basis in enumerate(bases):
        block = slice(branch * block_dimension, (branch + 1) * block_dimension)
        postselected[:, block] = row[branch] * basis
        phase = row[branch] / abs(row[branch])
        phase_matched_target[:, block] = phase * basis
    magnitudes = np.abs(row)
    uniform = bool(np.max(magnitudes) - np.min(magnitudes) <= tolerance)
    amplitude = float(magnitudes[0]) if uniform else None
    residual = (
        None
        if amplitude is None
        else float(
            np.linalg.norm(
                postselected - amplitude * phase_matched_target,
                ord=2,
            )
        )
    )
    success = None if amplitude is None else amplitude**2
    inverse_width = 1.0 / branch_count
    verified = bool(
        gram_residual <= 100 * tolerance
        and polar_residual <= 100 * tolerance
        and amplitude is not None
        and abs(success - inverse_width) <= 100 * tolerance
        and residual is not None
        and residual <= 100 * tolerance
    )
    return FlatPolarBranchErasureControl(
        control_id=control_id,
        branch_count=branch_count,
        block_dimension=block_dimension,
        carrier_dimension=carrier_dimension,
        flat_frame_gram_residual=gram_residual,
        polar_isometry_residual=polar_residual,
        branch_row_minimum_magnitude=float(np.min(magnitudes)),
        branch_row_maximum_magnitude=float(np.max(magnitudes)),
        postselected_scaled_polar_amplitude=amplitude,
        postselected_success_probability=success,
        inverse_width_success_upper_bound=inverse_width,
        scaled_polar_residual=residual,
        exact_inverse_width_boundary_verified=verified,
        status=(
            "physical-walsh-erasure-attains-inverse-width"
            if verified
            else "physical-branch-erasure-control-failure"
        ),
    )


def robust_branch_erasure_bound(
    unitary_row: tuple[complex, ...],
    requested_isometry_amplitude: float,
    *,
    tolerance: float = 1e-10,
) -> RobustBranchErasureBound:
    row = np.asarray(unitary_row, dtype=complex)
    if row.ndim != 1 or len(row) < 2:
        raise ValueError("unitary row must have at least two entries")
    if abs(float(np.linalg.norm(row)) - 1.0) > 100 * tolerance:
        raise ValueError("unitary row must have norm one")
    if not 0.0 <= requested_isometry_amplitude <= 1.0:
        raise ValueError("requested amplitude must lie in [0,1]")
    magnitudes = np.abs(row)
    minimum = float(np.min(magnitudes))
    universal_maximum = 1.0 / math.sqrt(len(row))
    lower = max(0.0, requested_isometry_amplitude - minimum)
    verified = bool(
        minimum <= universal_maximum + 100 * tolerance
        and lower + 100 * tolerance
        >= max(0.0, requested_isometry_amplitude - universal_maximum)
    )
    return RobustBranchErasureBound(
        branch_count=len(row),
        requested_isometry_amplitude=requested_isometry_amplitude,
        unitary_row_magnitudes=tuple(float(value) for value in magnitudes),
        minimum_row_magnitude=minimum,
        maximum_possible_minimum_row_magnitude=universal_maximum,
        operator_error_lower_bound=lower,
        constant_amplitude_vanishing_error_possible=bool(
            requested_isometry_amplitude <= universal_maximum + tolerance
        ),
        bound_verified=verified,
        status=(
            "robust-one-pass-erasure-error-bound"
            if verified
            else "branch-erasure-bound-control-failure"
        ),
    )


def accepted_character_rank_control(
    branch_count: int,
    accepted_character_count: int,
) -> AcceptedCharacterRankControl:
    if branch_count < 2 or not 0 <= accepted_character_count <= branch_count:
        raise ValueError("invalid accepted branch rank")
    acceptance = accepted_character_count / branch_count
    return AcceptedCharacterRankControl(
        branch_count=branch_count,
        accepted_character_count=accepted_character_count,
        covariant_uniform_branch_acceptance=acceptance,
        rank_fraction_upper_bound=acceptance,
        branch_label_erased=accepted_character_count == 1,
        constant_acceptance_requires_linear_rank=bool(
            acceptance >= 0.1 and accepted_character_count >= 0.1 * branch_count
        ),
        status=(
            "constant-acceptance-retains-linear-character-space"
            if acceptance >= 0.1
            else "sublinear-character-rank-has-vanishing-acceptance"
        ),
    )


def audit_correlated_input_escape(
    branch_count: int,
    carrier_dimension: int,
    *,
    tolerance: float = 1e-10,
) -> CorrelatedInputEscapeControl:
    if carrier_dimension < 1:
        raise ValueError("carrier_dimension must be positive")
    branch_unitary = walsh_matrix(branch_count)
    embedding = np.vstack(
        [np.eye(carrier_dimension, dtype=complex) for _ in range(branch_count)]
    ) / math.sqrt(branch_count)
    transformed = np.kron(branch_unitary, np.eye(carrier_dimension)) @ embedding
    target = np.vstack(
        [
            np.eye(carrier_dimension, dtype=complex),
            np.zeros(
                ((branch_count - 1) * carrier_dimension, carrier_dimension),
                dtype=complex,
            ),
        ]
    )
    isometry_residual = float(
        np.linalg.norm(
            embedding.conj().T @ embedding - np.eye(carrier_dimension),
            ord=2,
        )
    )
    erasure_residual = float(np.linalg.norm(transformed - target, ord=2))
    verified = bool(
        isometry_residual <= 100 * tolerance
        and erasure_residual <= 100 * tolerance
    )
    return CorrelatedInputEscapeControl(
        branch_count=branch_count,
        carrier_dimension=carrier_dimension,
        diagonal_embedding_isometry_residual=isometry_residual,
        branch_erasure_residual=erasure_residual,
        deterministic_branch_erasure_verified=verified,
        flat_orthogonal_full_direct_sum_input=False,
        status=(
            "source-correlated-subspace-evades-erasure-boundary"
            if verified
            else "correlated-input-escape-control-failure"
        ),
    )


def physical_branch_erasure_scaling_record(
    n: int,
    *,
    extra_copies: int = 2,
    polynomial_benchmark_degree: int = 10,
) -> PhysicalBranchErasureScalingRecord:
    if n < 3 or extra_copies < 0 or polynomial_benchmark_degree < 1:
        raise ValueError("invalid scaling parameters")
    order = math.factorial(n)
    copies = (order - 1).bit_length() + extra_copies
    amplification_log2 = copies / 2.0
    benchmark = polynomial_benchmark_degree * math.log2(n)
    return PhysicalBranchErasureScalingRecord(
        n=n,
        information_threshold_copy_count=copies,
        branch_count_decimal=str(1 << copies),
        one_pass_success_probability_log2_upper_bound=-copies,
        amplitude_amplification_query_log2_lower_bound=amplification_log2,
        polynomial_benchmark_degree=polynomial_benchmark_degree,
        polynomial_benchmark_log2=benchmark,
        one_pass_erasure_amplification_superpolynomial=(
            amplification_log2 > benchmark
        ),
        direct_source_correlated_transform_ruled_out=False,
        status=(
            "physical-one-pass-erasure-superpolynomial"
            if amplification_log2 > benchmark
            else "finite-size-erasure-benchmark-not-separated"
        ),
    )


def run_physical_branch_erasure_boundary() -> PhysicalBranchErasureBoundaryReport:
    flat_controls = [
        audit_flat_polar_branch_erasure(q, d, control_id=f"FLAT-Q{q}-D{d}")
        for q, d in ((2, 1), (4, 1), (4, 2), (8, 1), (8, 3), (16, 1))
    ]
    robust_bounds = []
    for q in (2, 4, 8, 16):
        walsh_row = tuple(walsh_matrix(q)[0])
        robust_bounds.append(robust_branch_erasure_bound(walsh_row, 1.0))
        concentrated = np.zeros(q, dtype=complex)
        concentrated[0] = math.sqrt(0.75)
        concentrated[1:] = math.sqrt(0.25 / (q - 1))
        robust_bounds.append(
            robust_branch_erasure_bound(tuple(concentrated), 2 / 3)
        )
    accepted_rank = [
        accepted_character_rank_control(q, r)
        for q, r in ((16, 1), (16, 2), (16, 8), (64, 1), (64, 8), (64, 32))
    ]
    escapes = [
        audit_correlated_input_escape(q, d)
        for q, d in ((2, 3), (4, 2), (8, 1), (16, 2))
    ]
    scaling = [
        physical_branch_erasure_scaling_record(n)
        for n in (8, 12, 16, 20, 24, 32, 40, 48, 64, 80)
    ]
    failures = sum(
        not row.exact_inverse_width_boundary_verified for row in flat_controls
    ) + sum(not row.bound_verified for row in robust_bounds) + sum(
        not row.deterministic_branch_erasure_verified for row in escapes
    )
    separated = [
        row for row in scaling
        if row.one_pass_erasure_amplification_superpolynomial
    ]
    verified = bool(not failures and separated and escapes)
    theorem = PhysicalBranchErasureTheorem(
        one_pass_kraus_restriction=(
            "For L=(<j|F tensor I)(direct_sum_i U_i), the restriction of L to branch i has norm |F[j,i]|."
        ),
        robust_error_bound=(
            "If L is epsilon-close to c times an isometry on every nonzero branch block, epsilon >= c-min_i|F[j,i]| >= c-1/sqrt(q)."
        ),
        flat_polar_consequence=(
            "For pairwise orthogonal E_i summing to I, the exact polar image is the full direct sum, so exact one-pass physical branch erasure succeeds with probability at most 1/q; Walsh attains it."
        ),
        accepted_rank_consequence=(
            "Retaining r branch characters accepts at most r/q of a covariant uniform branch mixture; constant acceptance retains Theta(q) unresolved characters."
        ),
        escape_condition=(
            "A source-restricted correlated image can erase deterministically; a positive wreath result must exhibit and coherently access such correlations or relocate the branch index into the carrier."
        ),
        scope=(
            "The theorem excludes one-pass block-diagonal carrier processing plus branch-only mixing/postselection. It is not a lower bound on arbitrary representation-specific, multi-round, or source-restricted circuits."
        ),
        theorem_verified=verified,
        status=(
            "physical-one-pass-branch-erasure-refuted"
            if verified
            else "physical-branch-erasure-boundary-control-failure"
        ),
    )
    return PhysicalBranchErasureBoundaryReport(
        created_at=utc_now(),
        theorem_contract=asdict(theorem),
        theorem=theorem,
        flat_polar_controls=flat_controls,
        robust_bounds=robust_bounds,
        accepted_rank_controls=accepted_rank,
        correlated_escape_controls=escapes,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "test_physical_branch_hadamard_as_orientation_polar",
                "resolved": verified,
                "resolution": "Resolved negatively for one-pass erasure by the unitary-row norm bound, including the exact flat polar control.",
            },
            {
                "obligation": "test_whether_retaining_many_characters_avoids_width",
                "resolved": verified,
                "resolution": "Rank-r acceptance is r/q; constant mass leaves a linear-dimensional unresolved branch output and is not polar erasure.",
            },
            {
                "obligation": "derive_actual_row_copy_source_correlation_or_classifier",
                "resolved": False,
                "resolution": "The actual C_U image must be shown to admit efficient branch-index relocation, correlated compression, or a coherent decoder beyond membership GPE.",
            },
            {
                "obligation": "rule_out_arbitrary_direct_physical_branch_to_polar_circuit",
                "resolved": False,
                "resolution": "The diagonal correlated escape proves that no such general conclusion follows from branch width alone.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "The normalized-analysis no-go is irrelevant because the physical branch register is already present.",
                "resolved": True,
                "resolution": "Presence removes branch preparation but not coherent erasure: a one-pass Fourier row still has total squared amplitude one across q inputs.",
            },
            {
                "objection": "Perfectly orthogonal leaf ranges make branch erasure easy.",
                "resolved": True,
                "resolution": "They make the polar perfectly conditioned but also make its image the full direct sum; Walsh postselection is exactly Q^*/sqrt(q).",
            },
            {
                "objection": "Accepting every nontrivial character gives near-unit success and therefore implements the polar.",
                "resolved": True,
                "resolution": "It retains q-1 orthogonal branch outcomes. The physical filter is useful but is not a branch-erasing coisometry.",
            },
            {
                "objection": "Equation (1) rules out the direct physical carrier route completely.",
                "resolved": True,
                "resolution": "False. The correlated-input controls erase with unit probability, so a representation-specific source-image factorization remains possible.",
            },
            {
                "objection": "Controlled GPE membership already computes the carrier-side branch label needed for erasure.",
                "resolved": False,
                "resolution": "Membership tests a supplied candidate i and preserves it; no polynomial coherent index-recovery transform over all orientations is known.",
            },
        ],
        headline_metrics={
            "one_pass_branch_erasure_theorem_count": int(verified),
            "flat_polar_inverse_width_control_count": len(flat_controls),
            "robust_error_bound_control_count": len(robust_bounds),
            "accepted_rank_control_count": len(accepted_rank),
            "correlated_input_escape_control_count": len(escapes),
            "finite_control_failure_count": failures,
            "superpolynomial_scaling_row_count": len(separated),
            "physical_source_correlation_factorization_count": 0,
            "coherent_orientation_index_classifier_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "physical_branch_register_removes_preparation_cost": True,
            "physical_branch_register_removes_erasure_width": False,
            "one_pass_branch_fourier_erasure_polynomial": False,
            "accept_many_characters_equals_orientation_polar": False,
            "flat_orthogonal_conditioning_removes_erasure_width": False,
            "source_correlated_escape_exists_abstractly": True,
            "actual_wreath_row_copy_correlated_factorization_proved": False,
            "coherent_orientation_index_classifier_proved": False,
            "arbitrary_direct_physical_router_ruled_out": False,
            "hierarchical_orientation_polar_proved": False,
            "speedup_claim_allowed": False,
        },
        status=theorem.status,
        summary=(
            "A physical orientation register avoids preparing a candidate mask but does not make one-pass Fourier erasure free. On the exact flat polar, any branch-controlled carrier processing followed by one branch-only postselection has success at most 1/q, with a robust constant-error bound. The surviving route must exploit a proved source-image correlation or coherently relocate the orientation index into the carrier before erasure."
        ),
        falsifiers_triggered=[
            "The phrase 'the branch register is already present' does not by itself remove the exponential orientation-width cost.",
            "Near-unit acceptance of many nontrivial orientation characters is not implementation of the polar coisometry.",
            "The no-go cannot be extended to source-correlated or carrier-classifying transforms without new arguments.",
        ],
    )


def write_physical_branch_erasure_boundary_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-PHYSICAL-BRANCH-ERASURE-BOUNDARY"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_physical_branch_erasure_boundary" in globals():
        report = run_physical_branch_erasure_boundary(**kwargs)
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
                id="NEG-SELF-DUAL-WREATH-PHYSICAL-BRANCH-ERASURE-BOUNDARY",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-PHYSICAL-BRANCH-ERASURE-BOUNDARY.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-PHYSICAL-BRANCH-ERASURE-BOUNDARY.",
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
                    "self_dual_wreath_physical_branch_erasure_boundary": str(path)
                },
            )
        )
    return payload
