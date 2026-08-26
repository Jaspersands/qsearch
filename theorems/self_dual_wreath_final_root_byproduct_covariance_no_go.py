"""Natural matrix variance forbids a full branch-preserving correction basis.

After the child polars have been factored, the final binary endpoint is the
canonical Naimark isometry

    V_C = [sqrt(C); sqrt(I-C)],          0 <= C <= I.       (1)

For a logical Bell error ``U``, its endpoint-conjugated partial correction is

    B_U = V_C U V_C^*
        = [[sqrt(C) U sqrt(C),
            sqrt(C) U sqrt(I-C)],
           [sqrt(I-C) U sqrt(C),
            sqrt(I-C) U sqrt(I-C)]].                     (2)

The unitary extension ``W_U=B_U+I-V_CV_C^*`` obeys ``W_U V_C=V_C U``.
Equation (2) is the exact formula sought for the Weyl generators.  It already
contains the endpoint square roots and generally mixes the final branch.

The tempting covariance shortcut is now decidable.  Let ``Gamma_U`` be any
output unitary that preserves the final branch flag, not necessarily the same
unitary in both branches.  Then

    Gamma_U V_C = V_C U    iff    [C,U]=0.                 (3)

Necessity follows by compressing the left-branch projector; sufficiency uses
``I_2 tensor U``.  Thus a full Hilbert--Schmidt orthogonal unitary error basis
``{U_a}_(a=1)^(D^2)`` has branch-preserving corrections only if ``C`` is
scalar, because the basis spans ``M_D``.

There is a quantitative version.  For

    eps_a^2 = D^(-1)||Gamma_a V_C-V_C U_a||_F^2,

the two-isometry effect inequality and the unitary-basis depolarizing identity
give

    eps_a^2 >= (4D)^(-1)||[C,U_a]||_F^2,
    D^(-2) sum_a D^(-1)||[C,U_a]||_F^2 = 2 Var(C),
    D^(-2) sum_a eps_a^2 >= Var(C)/2.                     (4)

The proved natural free-Jacobi endpoint has
``Var(C)->1/(8 alpha)``, ``alpha in [2,4]``.  Hence the annealed average
branch-preserving correction error is at least
``1/(16 alpha)>=1/64``.  Since ``0<=Var(C)<=1/4``, an event of asymptotic
mass at least ``1/(4 alpha-1)>=1/15`` has
``Var(C)>=1/(16 alpha)`` and average error at least
``1/(32 alpha)>=1/128``.

Changing the Bell basis cannot evade (4): every orthonormal unitary basis has
the same depolarizing twirl.  Allowing exact branch mixing can evade it, but
then the two labelled conjugated Weyl generators are algebraically complete:
they determine ``V_C`` up to a global phase.  This is an information identity,
not a circuit lower bound.

The result falsifies correction schemes assembled solely from the known
branch-preserving Schur/QFT/GPE/row-copy covariance.  A viable route must
compile the genuinely ``C``-dependent branch-mixing operators (2), or use a
different non-tight program-to-channel transducer.  It does not rule out such
routes, arbitrary quantum circuits, the physical PGM, a decoder, classical
separation, or a speedup.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import (
    ExperimentRecord,
    NegativeResultRecord,
    upsert_experiment,
    upsert_negative_result,
    utc_now,
)
from self_dual_wreath_final_root_purification_naimark_program_boundary import (
    _psd_power,
    weyl_unitary_error_basis,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_final_root_byproduct_covariance_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-FINAL-ROOT-BYPRODUCT-COVARIANCE-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
NEGATIVE_RESULT_ID = (
    "SCHUR-COMPANION-FINAL-ROOT-BRANCH-PRESERVING-BYPRODUCT-COVARIANCE"
)
WERNER_PAPER_ID = "werner-tight-teleportation-unitary-error-bases-2000"
WERNER_PAPER_URL = "https://arxiv.org/abs/quant-ph/0003070"
FREE_LUKACS_PAPER_ID = "szpojankowski-free-lukacs-2015"
FREE_LUKACS_PAPER_URL = "https://arxiv.org/abs/1403.5300"


@dataclass(frozen=True)
class ByproductCovarianceControl:
    control_id: str
    dimension: int
    endpoint_output_dimension: int
    effect_minimum_eigenvalue: float
    effect_maximum_eigenvalue: float
    effect_mean: float
    effect_variance: float
    effect_distinct_eigenvalue_count: int
    effect_commutant_complex_dimension: int
    unitary_error_basis_size: int
    selected_weyl_basis_exact_commuting_error_count: int
    maximum_byproduct_block_formula_residual: float
    maximum_correction_unitarity_residual: float
    maximum_correction_identity_residual: float
    average_normalized_commutator_square: float
    predicted_average_normalized_commutator_square: float
    average_same_action_branch_covariance_residual_square: float
    universal_average_branch_preserving_residual_square_lower_bound: float
    child_transport_conjugation_residual: float
    full_branch_preserving_error_basis_possible: bool
    exact_byproduct_and_covariance_boundary_verified: bool
    status: str


@dataclass(frozen=True)
class LabelledWeylRigidityControl:
    dimension: int
    joint_weyl_commutant_complex_dimension: int
    common_endpoint_range_residual: float
    shift_conjugate_single_generator_residual: float
    clock_conjugate_second_generator_gap: float
    nontrivial_gauge_distance_from_global_phase: float
    one_generator_does_not_fix_endpoint: bool
    labelled_weyl_pair_fixes_endpoint_up_to_phase: bool
    status: str


@dataclass(frozen=True)
class NaturalByproductCovarianceRecord:
    child_aspect: float
    limiting_effect_variance: float
    annealed_average_branch_preserving_residual_square_lower_bound: float
    quantitative_event_variance_threshold: float
    quantitative_event_probability_lower_bound: float
    quantitative_event_average_residual_square_lower_bound: float
    uniform_annealed_residual_square_floor: float
    uniform_event_mass_floor: float
    uniform_event_residual_square_floor: float
    full_branch_preserving_unitary_error_basis_asymptotically_possible: bool
    status: str


@dataclass(frozen=True)
class ByproductCovarianceTheorem:
    endpoint: str
    exact_byproduct_formula: str
    branch_preserving_criterion: str
    unitary_error_basis_average: str
    natural_consequence: str
    labelled_pair_rigidity: str
    physical_relevance: str
    surviving_route: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class ByproductCovarianceReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: ByproductCovarianceTheorem
    exact_controls: list[ByproductCovarianceControl]
    labelled_weyl_rigidity_control: LabelledWeylRigidityControl
    natural_records: list[NaturalByproductCovarianceRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    primary_literature: list[dict[str, str]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _hermitian(matrix: np.ndarray) -> np.ndarray:
    return (matrix + matrix.conj().T) / 2.0


def canonical_endpoint(
    effect: np.ndarray,
    *,
    tolerance: float = 1e-10,
) -> np.ndarray:
    """Return the positive endpoint ``[sqrt(C);sqrt(I-C)]``."""

    value = _hermitian(np.asarray(effect, dtype=complex))
    if value.ndim != 2 or value.shape[0] != value.shape[1]:
        raise ValueError("effect must be square")
    eigenvalues = np.linalg.eigvalsh(value)
    if float(eigenvalues[0]) < -100 * tolerance:
        raise ValueError("effect must be positive semidefinite")
    if float(eigenvalues[-1]) > 1 + 100 * tolerance:
        raise ValueError("effect must be at most identity")
    identity = np.eye(value.shape[0], dtype=complex)
    return np.vstack(
        (
            _psd_power(value, 0.5, tolerance=tolerance),
            _psd_power(identity - value, 0.5, tolerance=tolerance),
        )
    )


def endpoint_byproduct_blocks(
    effect: np.ndarray,
    logical_error: np.ndarray,
    *,
    tolerance: float = 1e-10,
) -> np.ndarray:
    """Return the explicit block matrix in equation (2)."""

    value = _hermitian(np.asarray(effect, dtype=complex))
    error = np.asarray(logical_error, dtype=complex)
    if error.shape != value.shape:
        raise ValueError("logical error and effect dimensions must match")
    identity = np.eye(value.shape[0], dtype=complex)
    left = _psd_power(value, 0.5, tolerance=tolerance)
    right = _psd_power(identity - value, 0.5, tolerance=tolerance)
    return np.block(
        [
            [left @ error @ left, left @ error @ right],
            [right @ error @ left, right @ error @ right],
        ]
    )


def effect_commutant_dimension(
    effect: np.ndarray,
    *,
    tolerance: float = 1e-9,
) -> tuple[int, int]:
    """Return distinct eigenvalue count and complex commutant dimension."""

    values = np.linalg.eigvalsh(_hermitian(np.asarray(effect, dtype=complex)))
    multiplicities: list[int] = []
    for value in values:
        if not multiplicities or abs(value - values[sum(multiplicities) - 1]) > tolerance:
            multiplicities.append(1)
        else:
            multiplicities[-1] += 1
    return len(multiplicities), sum(item * item for item in multiplicities)


def _deterministic_branch_transport(dimension: int) -> np.ndarray:
    blocks = []
    for branch in range(2):
        seed = np.arange(
            1,
            (dimension + 1) * dimension + 1,
            dtype=float,
        ).reshape(dimension + 1, dimension)
        seed = seed + 1j * np.flipud(seed) / (5 + branch)
        seed += (dimension + branch + 2) * np.eye(dimension + 1, dimension)
        block, _ = np.linalg.qr(seed)
        blocks.append(block[:, :dimension])
    zero = np.zeros((dimension + 1, dimension), dtype=complex)
    return np.block([[blocks[0], zero], [zero, blocks[1]]])


def audit_byproduct_covariance(
    control_id: str,
    effect: np.ndarray,
    *,
    tolerance: float = 1e-9,
) -> ByproductCovarianceControl:
    """Verify (2)--(4) for one exact endpoint effect."""

    value = _hermitian(np.asarray(effect, dtype=complex))
    endpoint = canonical_endpoint(value, tolerance=tolerance)
    dimension = value.shape[0]
    output_dimension = endpoint.shape[0]
    identity = np.eye(dimension, dtype=complex)
    output_identity = np.eye(output_dimension, dtype=complex)
    projector = endpoint @ endpoint.conj().T
    errors = weyl_unitary_error_basis(dimension)
    centered = value - np.trace(value).real / dimension * identity
    variance = float(np.trace(centered @ centered).real / dimension)
    distinct_count, commutant_dimension = effect_commutant_dimension(
        value,
        tolerance=tolerance,
    )
    commuting_count = 0
    maximum_formula = 0.0
    maximum_unitarity = 0.0
    maximum_correction = 0.0
    commutator_squares: list[float] = []
    same_action_squares: list[float] = []
    transport = _deterministic_branch_transport(dimension)
    transport_residual = 0.0

    for error in errors:
        commutator = value @ error - error @ value
        commutator_square = float(np.linalg.norm(commutator, ord="fro") ** 2 / dimension)
        commutator_squares.append(commutator_square)
        if math.sqrt(commutator_square) <= 100 * tolerance:
            commuting_count += 1

        byproduct = endpoint @ error @ endpoint.conj().T
        explicit = endpoint_byproduct_blocks(value, error, tolerance=tolerance)
        maximum_formula = max(
            maximum_formula,
            float(np.linalg.norm(byproduct - explicit, ord=2)),
        )
        correction = byproduct + output_identity - projector
        maximum_unitarity = max(
            maximum_unitarity,
            float(np.linalg.norm(correction.conj().T @ correction - output_identity, ord=2)),
        )
        maximum_correction = max(
            maximum_correction,
            float(np.linalg.norm(correction @ endpoint - endpoint @ error, ord=2)),
        )
        same_action = np.kron(np.eye(2), error) @ endpoint - endpoint @ error
        same_action_squares.append(
            float(np.linalg.norm(same_action, ord="fro") ** 2 / dimension)
        )
        transported_endpoint = transport @ endpoint
        transported_direct = (
            transported_endpoint @ error @ transported_endpoint.conj().T
        )
        transport_residual = max(
            transport_residual,
            float(
                np.linalg.norm(
                    transported_direct - transport @ byproduct @ transport.conj().T,
                    ord=2,
                )
            ),
        )

    average_commutator = float(np.mean(commutator_squares))
    predicted_commutator = 2.0 * variance
    average_same_action = float(np.mean(same_action_squares))
    universal_lower_bound = variance / 2.0
    scalar = variance <= 100 * tolerance
    possible = commutant_dimension == dimension**2
    verified = bool(
        np.linalg.norm(endpoint.conj().T @ endpoint - identity, ord=2)
        <= 100 * tolerance
        and maximum_formula <= 100 * tolerance
        and maximum_unitarity <= 100 * tolerance
        and maximum_correction <= 100 * tolerance
        and abs(average_commutator - predicted_commutator) <= 100 * tolerance
        and transport_residual <= 100 * tolerance
        and possible == scalar
        and average_same_action + 100 * tolerance >= universal_lower_bound
    )
    values = np.linalg.eigvalsh(value)
    return ByproductCovarianceControl(
        control_id=control_id,
        dimension=dimension,
        endpoint_output_dimension=output_dimension,
        effect_minimum_eigenvalue=float(values[0]),
        effect_maximum_eigenvalue=float(values[-1]),
        effect_mean=float(np.mean(values)),
        effect_variance=variance,
        effect_distinct_eigenvalue_count=distinct_count,
        effect_commutant_complex_dimension=commutant_dimension,
        unitary_error_basis_size=len(errors),
        selected_weyl_basis_exact_commuting_error_count=commuting_count,
        maximum_byproduct_block_formula_residual=maximum_formula,
        maximum_correction_unitarity_residual=maximum_unitarity,
        maximum_correction_identity_residual=maximum_correction,
        average_normalized_commutator_square=average_commutator,
        predicted_average_normalized_commutator_square=predicted_commutator,
        average_same_action_branch_covariance_residual_square=average_same_action,
        universal_average_branch_preserving_residual_square_lower_bound=(
            universal_lower_bound
        ),
        child_transport_conjugation_residual=transport_residual,
        full_branch_preserving_error_basis_possible=possible,
        exact_byproduct_and_covariance_boundary_verified=verified,
        status=(
            "exact-byproduct-covariance-boundary"
            if verified
            else "byproduct-covariance-control-failure"
        ),
    )


def _joint_commutant_dimension(operators: tuple[np.ndarray, ...], tolerance: float) -> int:
    dimension = operators[0].shape[0]
    columns = []
    for row in range(dimension):
        for column in range(dimension):
            basis = np.zeros((dimension, dimension), dtype=complex)
            basis[row, column] = 1.0
            columns.append(
                np.concatenate(
                    [(basis @ operator - operator @ basis).ravel() for operator in operators]
                )
            )
    linear_map = np.column_stack(columns)
    singular_values = np.linalg.svd(linear_map, compute_uv=False)
    rank = int(np.sum(singular_values > tolerance))
    return dimension**2 - rank


def audit_labelled_weyl_rigidity(
    dimension: int = 4,
    *,
    tolerance: float = 1e-9,
) -> LabelledWeylRigidityControl:
    """Verify that one generator leaves gauge freedom while the pair is rigid."""

    if dimension < 3:
        raise ValueError("dimension must be at least three")
    errors = weyl_unitary_error_basis(dimension)
    clock = errors[1]
    shift = errors[dimension]
    basis_seed = np.arange(1, dimension**2 + 1, dtype=float).reshape(
        dimension,
        dimension,
    )
    basis_seed = basis_seed + 1j * np.flipud(basis_seed) / 9.0
    basis, _ = np.linalg.qr(basis_seed + (dimension + 3) * np.eye(dimension))
    eigenvalues = np.linspace(0.15, 0.85, dimension)
    effect = (basis * eigenvalues) @ basis.conj().T
    endpoint = canonical_endpoint(effect, tolerance=tolerance)

    generator = _hermitian(shift + shift.conj().T)
    values, vectors = np.linalg.eigh(generator)
    gauge = (vectors * np.exp(0.37j * values)) @ vectors.conj().T
    other_endpoint = endpoint @ gauge
    projector = endpoint @ endpoint.conj().T
    other_projector = other_endpoint @ other_endpoint.conj().T
    shift_one = endpoint @ shift @ endpoint.conj().T
    shift_two = other_endpoint @ shift @ other_endpoint.conj().T
    clock_one = endpoint @ clock @ endpoint.conj().T
    clock_two = other_endpoint @ clock @ other_endpoint.conj().T
    joint_dimension = _joint_commutant_dimension((shift, clock), tolerance)
    phase_distance = math.sqrt(
        max(0.0, 2.0 - 2.0 * abs(complex(np.trace(gauge))) / dimension)
    )
    range_residual = float(np.linalg.norm(projector - other_projector, ord=2))
    shift_residual = float(np.linalg.norm(shift_one - shift_two, ord=2))
    clock_gap = float(np.linalg.norm(clock_one - clock_two, ord=2))
    one_not_enough = bool(
        range_residual <= 100 * tolerance
        and shift_residual <= 100 * tolerance
        and phase_distance > 100 * tolerance
        and clock_gap > 100 * tolerance
    )
    pair_rigid = joint_dimension == 1
    return LabelledWeylRigidityControl(
        dimension=dimension,
        joint_weyl_commutant_complex_dimension=joint_dimension,
        common_endpoint_range_residual=range_residual,
        shift_conjugate_single_generator_residual=shift_residual,
        clock_conjugate_second_generator_gap=clock_gap,
        nontrivial_gauge_distance_from_global_phase=phase_distance,
        one_generator_does_not_fix_endpoint=one_not_enough,
        labelled_weyl_pair_fixes_endpoint_up_to_phase=pair_rigid,
        status=(
            "labelled-weyl-pair-rigid-up-to-phase"
            if one_not_enough and pair_rigid
            else "labelled-weyl-rigidity-control-failure"
        ),
    )


def natural_byproduct_covariance_record(
    alpha: float,
) -> NaturalByproductCovarianceRecord:
    if not math.isfinite(alpha) or not 2.0 <= alpha <= 4.0:
        raise ValueError("alpha must lie in [2,4]")
    variance = 1.0 / (8.0 * alpha)
    event_threshold = variance / 2.0
    event_mass = 1.0 / (4.0 * alpha - 1.0)
    return NaturalByproductCovarianceRecord(
        child_aspect=float(alpha),
        limiting_effect_variance=variance,
        annealed_average_branch_preserving_residual_square_lower_bound=(
            variance / 2.0
        ),
        quantitative_event_variance_threshold=event_threshold,
        quantitative_event_probability_lower_bound=event_mass,
        quantitative_event_average_residual_square_lower_bound=(
            event_threshold / 2.0
        ),
        uniform_annealed_residual_square_floor=1.0 / 64.0,
        uniform_event_mass_floor=1.0 / 15.0,
        uniform_event_residual_square_floor=1.0 / 128.0,
        full_branch_preserving_unitary_error_basis_asymptotically_possible=False,
        status="natural-constant-branch-preserving-byproduct-obstruction",
    )


def _rotated_effect(eigenvalues: list[float]) -> np.ndarray:
    dimension = len(eigenvalues)
    seed = np.arange(1, dimension**2 + 1, dtype=float).reshape(dimension, dimension)
    seed = seed + 1j * np.rot90(seed) / 11.0
    basis, _ = np.linalg.qr(seed + (dimension + 2) * np.eye(dimension))
    return _hermitian((basis * np.asarray(eigenvalues)) @ basis.conj().T)


def run_final_root_byproduct_covariance_no_go() -> ByproductCovarianceReport:
    controls = [
        audit_byproduct_covariance(
            "scalar-d3",
            0.4 * np.eye(3, dtype=complex),
        ),
        audit_byproduct_covariance(
            "diagonal-simple-d3",
            np.diag([0.2, 0.5, 0.8]).astype(complex),
        ),
        audit_byproduct_covariance(
            "rotated-simple-d3",
            _rotated_effect([0.2, 0.5, 0.8]),
        ),
        audit_byproduct_covariance(
            "rotated-degenerate-d4",
            _rotated_effect([0.2, 0.2, 0.8, 0.8]),
        ),
    ]
    rigidity = audit_labelled_weyl_rigidity()
    natural = [
        natural_byproduct_covariance_record(alpha)
        for alpha in (2.0, 2.5, 3.0, 3.5, 4.0)
    ]
    failures = sum(
        not row.exact_byproduct_and_covariance_boundary_verified for row in controls
    )
    verified = bool(
        failures == 0
        and rigidity.one_generator_does_not_fix_endpoint
        and rigidity.labelled_weyl_pair_fixes_endpoint_up_to_phase
    )
    theorem = ByproductCovarianceTheorem(
        endpoint="V_C=[sqrt(C);sqrt(I-C)] with V_C^*V_C=I.",
        exact_byproduct_formula=(
            "V_C U V_C^* has the four sqrt(C)/sqrt(I-C) blocks in equation (2), and adding I-V_CV_C^* gives a unitary correction."
        ),
        branch_preserving_criterion=(
            "A branch-preserving output unitary Gamma can obey Gamma V_C=V_CU iff [C,U]=0."
        ),
        unitary_error_basis_average=(
            "For every Hilbert-Schmidt orthogonal unitary basis, average D^-1||[C,U_a]||_F^2=2Var(C), so average branch-preserving correction residual squared is at least Var(C)/2."
        ),
        natural_consequence=(
            "The free-Jacobi endpoint gives annealed residual squared at least 1/(16alpha)>=1/64 and a >=1/15-o(1) event with residual squared at least 1/128."
        ),
        labelled_pair_rigidity=(
            "The exact labelled conjugates of the Weyl shift and clock determine the endpoint isometry up to global phase because their joint commutant is scalar."
        ),
        physical_relevance=(
            "Known Schur/QFT/GPE/row-copy covariance is label controlled and final-branch preserving; it cannot furnish a full Bell correction basis on the natural nonscalar endpoint."
        ),
        surviving_route=(
            "Compile the C-dependent branch-mixing generators in equation (2), including whitening, or construct a different non-tight structured program-to-channel transducer."
        ),
        scope=(
            "This is a no-go for branch-preserving covariance corrections, not for arbitrary branch-mixing circuits or programmable processors."
        ),
        theorem_verified=verified,
        status=(
            "natural-branch-preserving-byproduct-covariance-falsified"
            if verified
            else "byproduct-covariance-theorem-control-failure"
        ),
    )
    return ByproductCovarianceReport(
        created_at=utc_now(),
        theorem_contract={
            "hypothesis": (
                "The physical generalized-Fourier row-copy and existing label-controlled covariance actions supply the full endpoint Bell correction basis without compiling the matrix-valued final mixer."
            ),
            "input_output_spaces": (
                "The logical input is H of dimension D; the canonical endpoint maps H to C^2 tensor H; corrections act on the endpoint output."
            ),
            "allowed_correction_architecture": (
                "For each member of an arbitrary D^2-element Hilbert-Schmidt orthogonal unitary error basis, use any output unitary commuting with the final left/right branch projector."
            ),
            "exact_failure_criterion": (
                "Such a correction exists for logical U iff U lies in comm(C); a complete unitary basis is possible iff C is scalar."
            ),
            "quantitative_failure_criterion": (
                "Average normalized correction residual squared is at least Var(C)/2 for every unitary error basis."
            ),
            "natural_input_relevance": (
                "The proved symmetric free-Jacobi endpoint has Var(C)->1/(8alpha), alpha in [2,4], yielding constant annealed and positive-mass residual floors."
            ),
            "classical_alternative": (
                "All finite controls and commutant dimensions are classically computable dense linear algebra; no quantum/classical separation follows."
            ),
            "claim_boundary": (
                "C-dependent branch mixing, arbitrary structured processors, and all-depth recursive compilation remain outside the theorem."
            ),
        },
        theorem=theorem,
        exact_controls=controls,
        labelled_weyl_rigidity_control=rigidity,
        natural_records=natural,
        proof_obligations=[
            {
                "obligation": "derive_exact_endpoint_conjugated_weyl_generators",
                "resolved": True,
                "evidence": "Equation (2) gives all four branch blocks for arbitrary U, hence in particular for the Weyl shift and clock.",
            },
            {
                "obligation": "test_branch_preserving_physical_covariance_as_bell_correction_basis",
                "resolved": True,
                "evidence": "Compression of the branch projector gives the iff criterion [C,U]=0, and an operator basis can satisfy it only for scalar C.",
            },
            {
                "obligation": "transfer_covariance_obstruction_to_natural_mass",
                "resolved": True,
                "evidence": "The unitary-basis twirl turns the proved free-Jacobi variance into an annealed 1/64 floor and a 1/15-o(1) event with 1/128 floor.",
            },
            {
                "obligation": "compile_C_dependent_branch_mixing_weyl_generators",
                "resolved": False,
                "evidence": "The exact block formula still contains sqrt(C), sqrt(I-C), and off-diagonal branch mixing.",
            },
            {
                "obligation": "compile_scale_free_whitening_filter",
                "resolved": False,
                "evidence": "Constructing C itself retains the unresolved S^(-1/2) metric access from the preceding theorem.",
            },
            {
                "obligation": "rule_out_arbitrary_program_to_channel_processors",
                "resolved": False,
                "evidence": "Only tight unitary-error-basis teleportation with branch-preserving covariance corrections is covered.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "A different Bell or unitary error basis may align with C.",
                "resolved": True,
                "resolution": "Every orthonormal unitary basis spans M_D and obeys the same depolarizing twirl, so the exact and averaged obstructions are basis independent.",
            },
            {
                "objection": "The two output branches may use different known covariance actions.",
                "resolved": True,
                "resolution": "The proof assumes only that the combined correction commutes with the branch projector; the two block unitaries may differ arbitrarily.",
            },
            {
                "objection": "Simple spectrum is required for the commutant obstruction.",
                "resolved": True,
                "resolution": "No. Any nonscalar C has a proper commutant and cannot contain a D^2-element operator basis; a degenerate D=4 control verifies this boundary.",
            },
            {
                "objection": "Compiled child GPE transports remove the correction error.",
                "resolved": True,
                "resolution": "Isometric postcomposition conjugates every byproduct and preserves the exact block identity and residual norms.",
            },
            {
                "objection": "Rigidity of the two labelled generators proves they are circuit hard.",
                "resolved": False,
                "resolution": "It proves algebraic completeness only. A representation-specific sparse compiler for the C-dependent branch-mixing pair remains possible.",
            },
            {
                "objection": "The theorem rules out every use of physical row-copy.",
                "resolved": False,
                "resolution": "It rejects only corrections staying in the final-branch-preserving covariance algebra. A new row-copy-mediated branch mixer lies outside the theorem.",
            },
        ],
        primary_literature=[
            {
                "paper_id": WERNER_PAPER_ID,
                "url": WERNER_PAPER_URL,
                "scope": "Tight teleportation, maximally entangled bases, Hilbert-Schmidt orthogonal unitary bases, and depolarizing unitary twirls."
            },
            {
                "paper_id": FREE_LUKACS_PAPER_ID,
                "url": FREE_LUKACS_PAPER_URL,
                "scope": "Free Lukacs structure used by the preceding final-root theorem to derive the natural free-Jacobi variance."
            },
        ],
        headline_metrics={
            "exact_endpoint_byproduct_block_formula_theorem_count": int(verified),
            "branch_preserving_correction_commutant_criterion_count": int(verified),
            "unitary_error_basis_average_covariance_lower_bound_count": int(verified),
            "natural_constant_byproduct_covariance_no_go_count": int(verified),
            "labelled_weyl_pair_algebraic_rigidity_count": int(rigidity.labelled_weyl_pair_fixes_endpoint_up_to_phase),
            "exact_control_count": len(controls),
            "exact_control_failure_count": failures,
            "uniform_annealed_residual_square_floor": 1.0 / 64.0,
            "uniform_positive_event_mass_floor": 1.0 / 15.0,
            "uniform_positive_event_residual_square_floor": 1.0 / 128.0,
            "branch_preserving_full_error_basis_compiler_count": 0,
            "C_dependent_branch_mixing_generator_compiler_count": 0,
            "scale_free_whitening_filter_compiler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "exact_endpoint_conjugated_weyl_block_formula_proved": verified,
            "branch_preserving_correction_exists_iff_error_commutes_with_effect": verified,
            "full_branch_preserving_unitary_error_basis_requires_scalar_effect": verified,
            "unitary_error_basis_choice_evades_covariance_obstruction": False,
            "natural_branch_preserving_covariance_has_constant_average_error": verified,
            "existing_branch_preserving_row_copy_covariance_supplies_bell_corrections": False,
            "labelled_weyl_pair_determines_endpoint_up_to_phase": rigidity.labelled_weyl_pair_fixes_endpoint_up_to_phase,
            "C_dependent_branch_mixing_weyl_generators_compiled": False,
            "scale_free_whitening_filter_compiled": False,
            "arbitrary_branch_mixing_correction_circuit_ruled_out": False,
            "arbitrary_program_to_channel_processor_lower_bound_proved": False,
            "physical_pgm_circuit_proved": False,
            "hidden_involution_decoder_proved": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The natural endpoint effect is quantitatively nonscalar, so no full Bell error basis can be corrected within the known final-branch-preserving covariance algebra. The required C-dependent branch-mixing generators and whitening remain uncompiled."
            ),
        },
        status=theorem.status,
        summary=(
            "Derived the exact endpoint-conjugated Weyl blocks and proved a basis-independent constant natural-error obstruction to every branch-preserving covariance correction basis; exact branch mixing remains the only tight-teleportation escape."
        ),
        falsifiers_triggered=[
            "Retained Schur/row-copy labels do not make a complete Bell correction basis branch preserving on a nonscalar endpoint.",
            "Changing the unitary error basis cannot hide the endpoint variance because every such basis has the same depolarizing second moment.",
            "Allowing different covariance actions in the two child branches does not evade compression of the branch effect.",
            "The natural free-Jacobi variance makes the correction obstruction constant on annealed and positive natural mass, not a rare finite pathology.",
            "The two exact labelled branch-mixing Weyl generators are algebraically complete endpoint data, not a metric-free covariance primitive."
        ],
    )


def write_final_root_byproduct_covariance_no_go_report(
    path: Path = REPORT_PATH,
    *,
    write_registry: bool = True,
) -> dict[str, Any]:
    payload = asdict(run_final_root_byproduct_covariance_no_go())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if write_registry:
        upsert_experiment(
            ExperimentRecord(
                id=DEFAULT_EXPERIMENT_ID,
                candidate_id=DEFAULT_CANDIDATE_ID,
                title="Final-root byproduct covariance no-go",
                status="completed-negative-theorem",
                hypothesis=payload["theorem_contract"]["hypothesis"],
                protocol=(
                    "Derive the endpoint-conjugated error blocks, compress arbitrary branch-preserving corrections to the endpoint effect, average over a general unitary error basis, transfer the free-Jacobi variance, and verify scalar, simple, rotated, and degenerate controls."
                ),
                positive_signal=(
                    "A polynomial compiler for the C-dependent branch-mixing Weyl shift and clock, or a non-tight structured program-to-channel transducer outside the branch-preserving covariance algebra."
                ),
                falsifiers=payload["falsifiers_triggered"],
                metrics=list(payload["headline_metrics"].keys()),
                dependencies=[
                    "self_dual_wreath_final_root_purification_naimark_program_boundary.py",
                    "self_dual_wreath_final_root_scalar_mixer_no_go.py",
                    "self_dual_wreath_physical_pgm_intertwiner.py",
                    "self_dual_wreath_component_polar_physical_pgm_closure.py",
                ],
                next_actions=[
                    "Test direct block encodings of the two C-dependent branch-mixing generators using the purification resource, without first extracting C or S^(-1/2) as a standalone signal."
                ],
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id=NEGATIVE_RESULT_ID,
                source=str(path),
                claim=(
                    "The known physical row-copy and label-controlled Schur/QFT/GPE covariance can correct a complete Bell error basis while preserving the final left/right branch flag."
                ),
                reason_invalid=(
                    "Any such correction for logical U forces [C,U]=0. A D^2-element unitary error basis spans M_D, so exact correction requires scalar C; quantitatively every basis has average residual squared at least Var(C)/2. The natural endpoint has Var(C)->1/(8alpha)."
                ),
                lesson=(
                    "Do not search for the remaining Bell corrections inside the branch-preserving covariance algebra. A viable tight-teleportation route must compile the C-dependent branch-mixing shift and clock, including the unresolved metric whitening, or change the transduction architecture."
                ),
                applies_to=[
                    DEFAULT_CANDIDATE_ID,
                    "PO-MECHANISM",
                    "PO-MEASUREMENT",
                    "PO-COMPLEXITY",
                ],
                evidence={
                    "exact_criterion": "Gamma_U branch preserving and Gamma_U V_C=V_CU iff [C,U]=0",
                    "basis_average": "D^-2 sum_a D^-1||[C,U_a]||_F^2=2Var(C)",
                    "natural_variance": "1/(8alpha), alpha in [2,4]",
                    "annealed_residual_square_floor": "1/64",
                    "positive_event_mass_floor": "1/15-o(1)",
                    "positive_event_residual_square_floor": "1/128",
                    "arbitrary_branch_mixing_ruled_out": False,
                    "speedup_claim_allowed": False,
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_final_root_byproduct_covariance_no_go_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
