"""Quantum-sampling normal form for the wreath-product PGM.

The covariance-compressed PGM leaves one controlled carrier operation.  If
``P`` is the base support projector and the ``nu`` isotypic input is written
as ``V_nu tensor M_nu``, define

    A_nu |m> = sum_j |j> tensor P |nu,j,m>.

Then

    A_nu^* A_nu = D_nu

where ``D_nu=Tr_(V_nu)(Pi_nu P Pi_nu)``, and the carrier operation in the PGM
is exactly the polar isometry

    Q_nu = A_nu D_nu^(-1/2).

This is the nonabelian analogue of the quantum-sampling step used by Bacon,
Childs, and van Dam to turn PGMs into algorithms for semidirect-product HSPs.
The correct algorithm-design question is therefore not merely whether
``D_nu`` has a favorable spectrum.  It is whether the polar isometry has a
direct structured implementation.

The orientation reduction gives a second exact normal form.  For controlled
invariant projectors ``E_epsilon`` put

    R |psi> = sum_epsilon |epsilon> tensor E_epsilon |psi>,
    S = R^* R = sum_epsilon E_epsilon,
    F = S / 2^k.

The required normalization is the nonorthogonal sampling isometry
``R S^(-1/2)``.  If the projectors commute and their common eigenbasis and
membership sets are coherently accessible, this reduces to ordinary uniform
fiber sampling.  Actual wreath orientation sectors already contain
noncommuting projectors at ``S_4``, so that successful abelian-HSP mechanism
does not transfer directly.  Conversely, a known one-element fiber has an
easy polar isometry even though the normalized analysis singular value is
``2^(-k/2)``.  Thus factorial spectral scale alone is not a hardness proof;
the missing object is a structured nonorthogonal fiber sampler.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import integer_partitions
from research_registry import utc_now
from self_dual_wreath_collision_free_frame_probe import Label
from self_dual_wreath_orientation_fourier_reduction import (
    _w4_collision_free_labels,
    compressed_fourier_block,
    orientation_invariant_projector,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_pgm_quantum_sampling_reduction.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-PGM-QUANTUM-SAMPLING-REDUCTION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class CarrierPolarControl:
    control_id: str
    row_dimension: int
    multiplicity_dimension: int
    physical_dimension: int
    projector_rank: int
    carrier_support_rank: int
    minimum_positive_carrier_eigenvalue: float
    maximum_carrier_eigenvalue: float
    analysis_gram_residual: float
    polar_support_isometry_residual: float
    exact_carrier_polar_identity_verified: bool
    status: str


@dataclass(frozen=True)
class OrientationSamplingControl:
    control_id: str
    n: int
    target_partition: tuple[int, ...]
    labels: tuple[Label, ...]
    orientation_count: int
    carrier_dimension: int
    nonzero_projector_count: int
    projector_rank_sum: int
    frame_support_rank: int
    common_range_dimension: int
    minimum_positive_projector_sum_eigenvalue: float
    maximum_projector_sum_eigenvalue: float
    maximum_pair_commutator_norm: float
    analysis_gram_residual: float
    normalized_fourier_frame_residual: float
    polar_support_isometry_residual: float
    commuting_fiber_normal_form_applicable: bool
    exact_nonorthogonal_sampling_identity_verified: bool
    status: str


@dataclass(frozen=True)
class ExplicitFiberControl:
    control_id: str
    orientation_count: int
    carrier_dimension: int
    normalized_analysis_minimum_positive_singular_value: float
    inverse_singular_value_cost: float
    maximum_pair_commutator_norm: float
    commuting_membership_sampler_residual: float
    direct_fiber_sampler_available: bool
    factorial_scale_alone_implies_hardness: bool
    status: str


@dataclass(frozen=True)
class QuantumSamplingScalingRecord:
    n: int
    hidden_label_count_decimal: str
    information_threshold_copy_count: int
    orientation_count_log2: int
    retained_projector_sum_eigenvalue_lower: float
    retained_projector_sum_eigenvalue_upper: float
    normalized_analysis_minimum_singular_value_upper: float
    black_box_polar_query_cost_log2_lower: float
    polynomial_black_box_polar: bool
    direct_structured_nonorthogonal_sampler_proved: bool
    status: str


@dataclass(frozen=True)
class PgmQuantumSamplingReductionReport:
    created_at: str
    theorem_contract: dict[str, Any]
    carrier_polar_controls: list[CarrierPolarControl]
    explicit_fiber_controls: list[ExplicitFiberControl]
    wreath_orientation_controls: list[OrientationSamplingControl]
    scaling_records: list[QuantumSamplingScalingRecord]
    proof_obligations: list[dict[str, bool | str]]
    adversarial_audit: list[dict[str, bool | str]]
    literature_links: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _psd_inverse_square_root(
    matrix: np.ndarray,
    tolerance: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    hermitian = (matrix + matrix.conj().T) / 2
    eigenvalues, eigenvectors = np.linalg.eigh(hermitian)
    if eigenvalues[0] < -100 * tolerance:
        raise ValueError("matrix must be positive semidefinite")
    positive = eigenvalues > tolerance
    inverse_values = np.zeros_like(eigenvalues)
    inverse_values[positive] = eigenvalues[positive] ** -0.5
    inverse = (eigenvectors * inverse_values) @ eigenvectors.conj().T
    support = eigenvectors[:, positive] @ eigenvectors[:, positive].conj().T
    return inverse, support, eigenvalues[positive]


def row_partial_trace(
    operator: np.ndarray,
    row_dimension: int,
    multiplicity_dimension: int,
) -> np.ndarray:
    expected = row_dimension * multiplicity_dimension
    if operator.shape != (expected, expected):
        raise ValueError("operator has the wrong tensor-product dimension")
    output = np.zeros(
        (multiplicity_dimension, multiplicity_dimension),
        dtype=complex,
    )
    for row in range(row_dimension):
        block = slice(
            row * multiplicity_dimension,
            (row + 1) * multiplicity_dimension,
        )
        output += operator[block, block]
    return output


def carrier_analysis_operator(
    projector: np.ndarray,
    row_dimension: int,
    multiplicity_dimension: int,
) -> np.ndarray:
    """Return ``A|m>=sum_j |j> tensor P|j,m>``."""

    physical_dimension = row_dimension * multiplicity_dimension
    if projector.shape != (physical_dimension, physical_dimension):
        raise ValueError("projector has the wrong tensor-product dimension")
    analysis = np.zeros(
        (row_dimension * physical_dimension, multiplicity_dimension),
        dtype=complex,
    )
    for row in range(row_dimension):
        source = slice(
            row * multiplicity_dimension,
            (row + 1) * multiplicity_dimension,
        )
        output = slice(row * physical_dimension, (row + 1) * physical_dimension)
        analysis[output, :] = projector[:, source]
    return analysis


def audit_carrier_polar_identity(
    control_id: str,
    projector: np.ndarray,
    row_dimension: int,
    multiplicity_dimension: int,
    *,
    tolerance: float = 1e-10,
) -> CarrierPolarControl:
    physical_dimension = row_dimension * multiplicity_dimension
    identity = np.eye(physical_dimension)
    projector_residual = max(
        float(np.linalg.norm(projector @ projector - projector, ord=2)),
        float(np.linalg.norm(projector - projector.conj().T, ord=2)),
    )
    if projector_residual > 100 * tolerance:
        raise ValueError("an orthogonal projector is required")
    carrier = row_partial_trace(
        projector,
        row_dimension,
        multiplicity_dimension,
    )
    analysis = carrier_analysis_operator(
        projector,
        row_dimension,
        multiplicity_dimension,
    )
    gram_residual = float(
        np.linalg.norm(analysis.conj().T @ analysis - carrier, ord=2)
    )
    inverse, support, positive = _psd_inverse_square_root(carrier, tolerance)
    polar = analysis @ inverse
    isometry_residual = float(
        np.linalg.norm(polar.conj().T @ polar - support, ord=2)
    )
    verified = (
        projector_residual <= 100 * tolerance
        and gram_residual <= 100 * tolerance
        and isometry_residual <= 100 * tolerance
        and float(np.linalg.norm(projector @ identity - projector, ord=2))
        <= 100 * tolerance
    )
    return CarrierPolarControl(
        control_id=control_id,
        row_dimension=row_dimension,
        multiplicity_dimension=multiplicity_dimension,
        physical_dimension=physical_dimension,
        projector_rank=int(round(float(np.trace(projector).real))),
        carrier_support_rank=len(positive),
        minimum_positive_carrier_eigenvalue=(
            float(positive[0]) if len(positive) else 0.0
        ),
        maximum_carrier_eigenvalue=(
            float(positive[-1]) if len(positive) else 0.0
        ),
        analysis_gram_residual=gram_residual,
        polar_support_isometry_residual=isometry_residual,
        exact_carrier_polar_identity_verified=verified,
        status=(
            "exact-carrier-polar-identity"
            if verified
            else "carrier-polar-validation-failure"
        ),
    )


def orientation_analysis_operator(
    projectors: tuple[np.ndarray, ...],
) -> np.ndarray:
    if not projectors:
        raise ValueError("at least one projector is required")
    dimension = len(projectors[0])
    if any(projector.shape != (dimension, dimension) for projector in projectors):
        raise ValueError("all projectors must share one carrier")
    return np.vstack(projectors)


def _maximum_commutator_norm(projectors: tuple[np.ndarray, ...]) -> float:
    return max(
        (
            float(
                np.linalg.norm(
                    left @ right - right @ left,
                    ord=2,
                )
            )
            for index, left in enumerate(projectors)
            for right in projectors[index + 1 :]
        ),
        default=0.0,
    )


def audit_orientation_sampling_frame(
    control_id: str,
    n: int,
    target: tuple[int, ...],
    labels: tuple[Label, ...],
    *,
    tolerance: float = 1e-9,
) -> OrientationSamplingControl:
    orientation_count = 1 << len(labels)
    projectors = tuple(
        orientation_invariant_projector(target, labels, mask)
        for mask in range(orientation_count)
    )
    dimension = len(projectors[0])
    projector_residual = max(
        max(
            float(np.linalg.norm(projector @ projector - projector, ord=2)),
            float(np.linalg.norm(projector - projector.conj().T, ord=2)),
        )
        for projector in projectors
    )
    analysis = orientation_analysis_operator(projectors)
    projector_sum = sum(projectors, np.zeros_like(projectors[0]))
    gram_residual = float(
        np.linalg.norm(analysis.conj().T @ analysis - projector_sum, ord=2)
    )
    fourier_frame = compressed_fourier_block(target, labels)
    frame_residual = float(
        np.linalg.norm(projector_sum / orientation_count - fourier_frame, ord=2)
    )
    inverse, support, positive = _psd_inverse_square_root(
        projector_sum,
        tolerance,
    )
    polar = analysis @ inverse
    polar_residual = float(
        np.linalg.norm(polar.conj().T @ polar - support, ord=2)
    )
    commutator = _maximum_commutator_norm(projectors)
    common_range = int(
        np.count_nonzero(
            np.linalg.eigvalsh((projector_sum + projector_sum.conj().T) / 2)
            >= orientation_count - 100 * tolerance
        )
    )
    verified = (
        projector_residual <= 100 * tolerance
        and gram_residual <= 100 * tolerance
        and frame_residual <= 100 * tolerance
        and polar_residual <= 100 * tolerance
    )
    commuting = commutator <= 100 * tolerance
    return OrientationSamplingControl(
        control_id=control_id,
        n=n,
        target_partition=target,
        labels=labels,
        orientation_count=orientation_count,
        carrier_dimension=dimension,
        nonzero_projector_count=sum(
            float(np.trace(projector).real) > tolerance
            for projector in projectors
        ),
        projector_rank_sum=sum(
            int(round(float(np.trace(projector).real)))
            for projector in projectors
        ),
        frame_support_rank=len(positive),
        common_range_dimension=common_range,
        minimum_positive_projector_sum_eigenvalue=(
            float(positive[0]) if len(positive) else 0.0
        ),
        maximum_projector_sum_eigenvalue=(
            float(positive[-1]) if len(positive) else 0.0
        ),
        maximum_pair_commutator_norm=commutator,
        analysis_gram_residual=gram_residual,
        normalized_fourier_frame_residual=frame_residual,
        polar_support_isometry_residual=polar_residual,
        commuting_fiber_normal_form_applicable=commuting,
        exact_nonorthogonal_sampling_identity_verified=verified,
        status=(
            "exact-noncommuting-orientation-sampling-frame"
            if verified and not commuting
            else "exact-commuting-orientation-sampling-frame"
            if verified
            else "orientation-sampling-validation-failure"
        ),
    )


def _diagonal_membership_polar(
    projectors: tuple[np.ndarray, ...],
    tolerance: float,
) -> np.ndarray:
    dimension = len(projectors[0])
    output = np.zeros((len(projectors) * dimension, dimension))
    for basis in range(dimension):
        memberships = [
            index
            for index, projector in enumerate(projectors)
            if float(projector[basis, basis].real) > 1 - tolerance
        ]
        if not memberships:
            continue
        amplitude = 1 / math.sqrt(len(memberships))
        for index in memberships:
            output[index * dimension + basis, basis] = amplitude
    return output


def audit_explicit_diagonal_fiber(
    control_id: str,
    projectors: tuple[np.ndarray, ...],
    *,
    tolerance: float = 1e-10,
) -> ExplicitFiberControl:
    analysis = orientation_analysis_operator(projectors)
    count = len(projectors)
    projector_sum = analysis.conj().T @ analysis
    inverse, _, positive = _psd_inverse_square_root(projector_sum, tolerance)
    polar = analysis @ inverse
    expected = _diagonal_membership_polar(projectors, tolerance)
    residual = float(np.linalg.norm(polar - expected, ord=2))
    normalized_minimum = (
        math.sqrt(float(positive[0]) / count) if len(positive) else 0.0
    )
    direct = residual <= 100 * tolerance
    return ExplicitFiberControl(
        control_id=control_id,
        orientation_count=count,
        carrier_dimension=len(projectors[0]),
        normalized_analysis_minimum_positive_singular_value=normalized_minimum,
        inverse_singular_value_cost=(
            1 / normalized_minimum if normalized_minimum else math.inf
        ),
        maximum_pair_commutator_norm=_maximum_commutator_norm(projectors),
        commuting_membership_sampler_residual=residual,
        direct_fiber_sampler_available=direct,
        factorial_scale_alone_implies_hardness=False,
        status=(
            "direct-known-fiber-polar-sampler"
            if direct
            else "diagonal-fiber-sampler-validation-failure"
        ),
    )


def quantum_sampling_scaling_record(
    n: int,
    *,
    lower_sum_eigenvalue: float = 1e-4,
    upper_sum_eigenvalue: float = 400.0,
) -> QuantumSamplingScalingRecord:
    if n < 3:
        raise ValueError("n must be at least three")
    if not 0 < lower_sum_eigenvalue <= upper_sum_eigenvalue:
        raise ValueError("invalid retained spectral window")
    hidden_count = math.factorial(n)
    copies = math.ceil(math.lgamma(n + 1) / math.log(2))
    # The normalized controlled-projector analysis is R/sqrt(2^k).
    minimum_singular = math.sqrt(lower_sum_eigenvalue) * math.exp2(-copies / 2)
    query_log = copies / 2 - 0.5 * math.log2(lower_sum_eigenvalue)
    return QuantumSamplingScalingRecord(
        n=n,
        hidden_label_count_decimal=str(hidden_count),
        information_threshold_copy_count=copies,
        orientation_count_log2=copies,
        retained_projector_sum_eigenvalue_lower=lower_sum_eigenvalue,
        retained_projector_sum_eigenvalue_upper=upper_sum_eigenvalue,
        normalized_analysis_minimum_singular_value_upper=minimum_singular,
        black_box_polar_query_cost_log2_lower=query_log,
        polynomial_black_box_polar=query_log <= 10 * math.log2(n),
        direct_structured_nonorthogonal_sampler_proved=False,
        status="black-box-polar-factorial-structured-sampler-open",
    )


def _carrier_controls() -> list[CarrierPolarControl]:
    bell = np.asarray([1.0, 0.0, 0.0, 1.0]) / math.sqrt(2)
    bell_projector = np.outer(bell, bell)
    product_projector = np.diag([1.0, 1.0, 0.0, 0.0])
    raw = np.asarray(
        [
            [1.0, 0.0],
            [1.0, 1.0],
            [0.0, 1.0],
            [1.0, -1.0],
            [0.5, 1.0],
            [1.0, 0.5],
        ]
    )
    basis, _ = np.linalg.qr(raw)
    rank_two = basis @ basis.T
    return [
        audit_carrier_polar_identity("bell-rank-one", bell_projector, 2, 2),
        audit_carrier_polar_identity("product-rank-two", product_projector, 2, 2),
        audit_carrier_polar_identity("generic-rank-two", rank_two, 2, 3),
    ]


def _explicit_fiber_controls() -> list[ExplicitFiberControl]:
    count = 16
    rank_one = np.diag([1.0, 0.0, 0.0])
    zero = np.zeros((3, 3))
    single_known = (rank_one,) + (zero,) * (count - 1)
    overlapping = (
        np.diag([1.0, 1.0, 0.0, 0.0]),
        np.diag([1.0, 0.0, 1.0, 0.0]),
        np.diag([0.0, 1.0, 1.0, 0.0]),
        np.diag([0.0, 0.0, 0.0, 1.0]),
    )
    return [
        audit_explicit_diagonal_fiber("single-known-small-fiber", single_known),
        audit_explicit_diagonal_fiber("overlapping-diagonal-fibers", overlapping),
    ]


def _wreath_controls() -> list[OrientationSamplingControl]:
    controls: list[OrientationSamplingControl] = []
    for tuple_index, labels in enumerate(_w4_collision_free_labels()[:3]):
        for target in integer_partitions(4):
            control = audit_orientation_sampling_frame(
                f"W4-{tuple_index}-{'-'.join(map(str, target))}",
                4,
                target,
                labels,
            )
            if control.nonzero_projector_count:
                controls.append(control)
    return controls


def run_pgm_quantum_sampling_reduction() -> PgmQuantumSamplingReductionReport:
    carrier_controls = _carrier_controls()
    fiber_controls = _explicit_fiber_controls()
    wreath_controls = _wreath_controls()
    scaling = [
        quantum_sampling_scaling_record(n)
        for n in (16, 24, 32, 64, 128, 256, 512)
    ]
    carrier_failures = sum(
        not row.exact_carrier_polar_identity_verified
        for row in carrier_controls
    )
    wreath_failures = sum(
        not row.exact_nonorthogonal_sampling_identity_verified
        for row in wreath_controls
    )
    noncommuting = [
        row
        for row in wreath_controls
        if not row.commuting_fiber_normal_form_applicable
    ]
    fiber_failures = sum(not row.direct_fiber_sampler_available for row in fiber_controls)
    verified = carrier_failures == wreath_failures == fiber_failures == 0
    return PgmQuantumSamplingReductionReport(
        created_at=utc_now(),
        theorem_contract={
            "carrier_analysis": (
                "A_nu|m>=sum_j |j> tensor P|nu,j,m>, with "
                "A_nu^*A_nu=D_nu=Tr_V(Pi_nu P Pi_nu)."
            ),
            "pgm_carrier_map": (
                "The covariance-compressed PGM uses the polar isometry "
                "Q_nu=A_nu D_nu^(-1/2), coherently controlled by nu."
            ),
            "orientation_analysis": (
                "R=sum_epsilon |epsilon> tensor E_epsilon and "
                "R^*R=sum_epsilon E_epsilon=2^k F_nu."
            ),
            "commuting_fiber_special_case": (
                "In a coherently accessible joint eigenbasis, Q maps a basis "
                "state to the uniform superposition of projector indices that "
                "contain it. This is ordinary quantum sampling over fibers."
            ),
            "noncommuting_generalization": (
                "For actual orientation sectors the E_epsilon need not commute; "
                "the target is a polar isometry for overlapping subspaces, not "
                "a classical preimage sampler."
            ),
            "black_box_boundary": (
                "PREPARE/SELECT exposes R/sqrt(2^k). On a constant-eigenvalue "
                "window of sum E_epsilon, generic polar transformation costs "
                "Theta(2^(k/2)); only a direct structured sampler can bypass it."
            ),
        },
        carrier_polar_controls=carrier_controls,
        explicit_fiber_controls=fiber_controls,
        wreath_orientation_controls=wreath_controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "covariant_carrier_polar_identity",
                "resolved": carrier_failures == 0,
                "resolution": (
                    "Projector idempotence gives A_nu^*A_nu=D_nu exactly; "
                    "polar normalization gives an isometry on supp(D_nu)."
                ),
            },
            {
                "obligation": "orientation_projector_analysis_identity",
                "resolved": wreath_failures == 0,
                "resolution": (
                    "Vertical projector analysis has Gram sum E_epsilon, and "
                    "the exact W4 Fourier controls equal its 2^-k normalization."
                ),
            },
            {
                "obligation": "factorial_scale_not_intrinsic_hardness",
                "resolved": fiber_failures == 0,
                "resolution": (
                    "A known singleton fiber has normalized singular value "
                    "2^(-k/2) but an explicit one-step polar sampler."
                ),
            },
            {
                "obligation": "ordinary_commuting_fiber_reduction_for_wreath",
                "resolved": bool(noncommuting),
                "resolution": (
                    "Resolved negatively: exact S4 sectors have nonzero pair "
                    "commutators, so no joint membership basis exists generically."
                ),
            },
            {
                "obligation": "structured_nonorthogonal_quantum_sampler",
                "resolved": False,
                "resolution": (
                    "No polynomial circuit constructs the controlled polar of "
                    "the overlapping invariant-subspace frame."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "The 1/n! eigenvalue scale alone proves the PGM hard.",
                "resolved": True,
                "resolution": (
                    "False. A known singleton fiber has the same normalized "
                    "scale and a trivial direct polar isometry. Hardness must be "
                    "attached to absence of a structured sampler."
                ),
            },
            {
                "objection": "The Bacon-Childs-van Dam fiber sampler transfers directly.",
                "resolved": True,
                "resolution": (
                    "It does not: their fibers are orthogonal computational "
                    "preimages, while the wreath orientation projectors already "
                    "fail to commute in exact S4 controls."
                ),
            },
            {
                "objection": "Noncommutation proves that no efficient sampler exists.",
                "resolved": False,
                "resolution": (
                    "No. It only kills the ordinary joint-membership sampler. A "
                    "representation-specific recoupling or polar transform may exist."
                ),
            },
            {
                "objection": "An efficient invariant-projector measurement is enough.",
                "resolved": True,
                "resolution": (
                    "It supplies normalized analysis access, not the polar "
                    "normalization. Generic conversion retains the factorial-root cost."
                ),
            },
        ],
        literature_links=[
            {
                "paper_id": "bacon-childs-van-dam-2005",
                "title": (
                    "From optimal measurement to efficient quantum algorithms "
                    "for the hidden subgroup problem over semidirect product groups"
                ),
                "url": "https://arxiv.org/abs/quant-ph/0504083",
                "use": (
                    "Successful PGM implementations reduce to coherent uniform "
                    "sampling over solutions of an average-case algebraic problem."
                ),
                "external_theorem_not_reproved_here": True,
            },
            {
                "paper_id": "bravyi-et-al-2023-kronecker",
                "title": "Quantum complexity of the Kronecker coefficients",
                "url": "https://arxiv.org/abs/2302.11454",
                "use": (
                    "Invariant-sector projectors are efficiently measurable, "
                    "while resolving their multiplicity structure remains a "
                    "nontrivial quantum counting problem."
                ),
                "external_theorem_not_reproved_here": True,
            },
        ],
        headline_metrics={
            "covariant_carrier_polar_reduction_theorem_count": 1,
            "orientation_nonorthogonal_sampling_reduction_theorem_count": 1,
            "commuting_fiber_sampler_special_case_theorem_count": 1,
            "carrier_control_count": len(carrier_controls),
            "carrier_validation_failure_count": carrier_failures,
            "explicit_fiber_control_count": len(fiber_controls),
            "explicit_fiber_validation_failure_count": fiber_failures,
            "wreath_orientation_control_count": len(wreath_controls),
            "wreath_orientation_validation_failure_count": wreath_failures,
            "noncommuting_wreath_sector_count": len(noncommuting),
            "maximum_wreath_pair_commutator_norm": max(
                row.maximum_pair_commutator_norm for row in wreath_controls
            ),
            "tail_n": scaling[-1].n,
            "tail_black_box_polar_query_cost_log2_lower": (
                scaling[-1].black_box_polar_query_cost_log2_lower
            ),
            "structured_nonorthogonal_sampler_count": 0,
            "polynomial_hidden_permutation_decoder_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "pgm_reduced_to_controlled_carrier_polar": verified,
            "orientation_frame_reduced_to_nonorthogonal_sampling": verified,
            "ordinary_commuting_fiber_sampler_applies_generically": False,
            "factorial_spectral_scale_is_standalone_hardness_proof": False,
            "structured_nonorthogonal_sampler_proved": False,
            "polynomial_pgm_circuit_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The algorithmic target is now a concrete average-case "
                "nonorthogonal quantum-sampling problem. Exact W4 controls "
                "falsify the ordinary commuting-fiber mechanism, while no "
                "representation-specific polar sampler is known."
            ),
        },
        status=(
            "pgm-reduced-to-nonorthogonal-quantum-sampling-open"
            if verified and noncommuting
            else "pgm-quantum-sampling-reduction-validation-failure"
        ),
        summary=(
            "Reduced the remaining wreath PGM operation to a controlled polar "
            "isometry and its orientation form to nonorthogonal quantum "
            "sampling. Known-fiber controls show that tiny singular scale is "
            "not inherently hard, while exact S4 sectors rule out the direct "
            "commuting-fiber strategy used by successful semidirect HSP PGMs."
        ),
        falsifiers_triggered=[
            (
                "Do not cite factorial eigenvalue scale alone as evidence that "
                "the PGM is computationally hard."
            ),
            (
                "Do not mutate classical matrix-sum or subset-sum fiber samplers "
                "without handling noncommuting invariant subspaces."
            ),
            (
                "The next positive mechanism must directly synthesize the polar "
                "of an overlapping projector frame, ideally from recoupling or "
                "an efficiently navigable average-case witness structure."
            ),
        ],
    )


def write_pgm_quantum_sampling_reduction_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-PGM-QUANTUM-SAMPLING-REDUCTION"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_pgm_quantum_sampling_reduction())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    return payload


if __name__ == "__main__":
    report = write_pgm_quantum_sampling_reduction_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
