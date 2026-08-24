"""Canonical analysis-map normalization for joint-character multiplicity blocks.

The joint-character multiplicity Gram theorem gives, for an ``S_n`` irrep
``nu`` of dimension ``r``, source carrier dimension ``d``, and ``q=2^k``
orientation branches,

    D_nu = r/(q d) (I_r tensor W) G_nu (I_r tensor W)^*,
    G_nu = L_nu^* L_nu.                                  (1)

This module identifies the corresponding rectangular analysis map

    A_nu = sqrt(r/(q d)) L_nu (I_r tensor W)^*,
    A_nu^* A_nu = D_nu.                                  (2)

Equation (2) is the direct polar target: ``polar(A_nu)`` is the whitening
isometry without explicitly forming ``D_nu^-1/2``.

The obvious coherent implementation is not normalized as ``A_nu``.  Starting
from ``|b,z>``, apply the branch Walsh transform, prepare a maximally entangled
carrier pair, apply controlled invariant projection ``E_e``, and erase the
orientation work label into one Walsh row.  Its selected top block is exactly

    N_nu = L_nu (I_r tensor W)^* / sqrt(q d)
         = A_nu / sqrt(r),
    N_nu^* N_nu = D_nu/r.                                (3)

Thus the canonical direct-analysis circuit is the square-root counterpart of
the Schur-row density block encoding: both carry the same exact ``1/r`` Gram
normalization.  Direct access improves generic rescaling from ``Omega(r)`` for
the density to ``Omega(sqrt(r))`` for the rectangular factor, but it does not
make the route polynomial on growing-row sectors.

Indeed, a bounded singular-value polynomial that uniformly maps
``A/sqrt(r)`` to ``A`` for all contractions ``A`` has degree
``Omega(sqrt(r))`` by Bernstein's inequality, using a singular value equal to
one.  Balanced two-row irreps have ``r=Catalan(n/2)=2^Theta(n)/poly(n)``.

This is a lower bound for the canonical normalized access plus a uniform
polynomial transform, not for direct structured polar synthesis.  Scaling by
``1/sqrt(r)`` does not change the mathematical polar.  A representation-
specific circuit, multi-round branch relocation, or fused covariant isometry
could implement ``polar(A_nu)`` without amplitude-amplifying ``N_nu``.  No
such circuit, natural large-row mass theorem, decoder, or speedup is proved.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import hook_length_dimension
from research_registry import utc_now
from self_dual_wreath_joint_character_multiplicity_gram import (
    Label,
    Partition,
    predicted_joint_multiplicity_operator,
    projection_gram_factor,
    walsh_matrix,
)
from self_dual_wreath_joint_character_purification_access_boundary import (
    balanced_two_row_irrep_dimension,
)
from self_dual_wreath_orientation_fourier_reduction import (
    _w4_collision_free_labels,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_joint_character_analysis_map_normalization.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-JOINT-CHARACTER-ANALYSIS-MAP-NORMALIZATION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class JointAnalysisMapControl:
    control_id: str
    n: int
    target_partition: Partition
    labels: tuple[Label, ...]
    irrep_dimension: int
    orientation_count: int
    source_carrier_dimension: int
    analysis_input_dimension: int
    analysis_output_dimension: int
    multiplicity_operator_rank: int
    minimum_positive_multiplicity_eigenvalue: float
    maximum_multiplicity_eigenvalue: float
    minimum_positive_target_analysis_singular_value: float
    maximum_target_analysis_singular_value: float
    canonical_analysis_normalization_sqrt_irrep: float
    target_gram_residual: float
    canonical_erasure_map_residual: float
    canonical_gram_residual: float
    singular_value_scaling_residual: float
    polar_scale_invariance_residual: float
    generic_amplification_degree_lower_bound: int
    exact_analysis_normalization_theorem_verified: bool
    status: str


@dataclass(frozen=True)
class JointAnalysisMapScalingRecord:
    n: int
    witness_partition: Partition
    witness_irrep_dimension_decimal: str
    witness_irrep_dimension_log2: float
    canonical_direct_analysis_normalization: str
    density_rescaling_degree_order: str
    direct_analysis_amplification_degree_order: str
    generic_direct_analysis_degree_lower_bound_decimal: str
    generic_direct_analysis_degree_log2_lower_bound: float
    balanced_two_row_dimension_exponential: bool
    witness_sector_natural_mass_proved: bool
    direct_polar_compiled: bool
    direct_structured_polar_ruled_out: bool
    status: str


@dataclass(frozen=True)
class JointAnalysisMapTheorem:
    exact_analysis_factor: str
    exact_gram: str
    canonical_circuit: str
    canonical_normalization: str
    density_access_equivalence: str
    generic_amplification_boundary: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class JointAnalysisMapReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: JointAnalysisMapTheorem
    finite_controls: list[JointAnalysisMapControl]
    scaling_records: list[JointAnalysisMapScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _direct_polar(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    left, singular_values, right_star = np.linalg.svd(matrix, full_matrices=False)
    active = singular_values > tolerance
    return left[:, active] @ right_star[active, :]


def canonical_projector_erasure_map(
    projectors: tuple[np.ndarray, ...],
    irrep_dimension: int,
    carrier_dimension: int,
) -> np.ndarray:
    """Return the selected top block of the canonical circuit in equation (3)."""

    count = len(projectors)
    if count < 1 or count & (count - 1):
        raise ValueError("projector count must be a positive power of two")
    expected = irrep_dimension * carrier_dimension
    if any(projector.shape != (expected, expected) for projector in projectors):
        raise ValueError("projector dimension mismatch")
    output = np.zeros(
        (
            irrep_dimension * carrier_dimension * carrier_dimension,
            irrep_dimension * count,
        ),
        dtype=complex,
    )
    normalization = count * math.sqrt(carrier_dimension)
    for column in range(irrep_dimension):
        for character in range(count):
            target_column = column * count + character
            for orientation, projector in enumerate(projectors):
                sign = (
                    -1.0
                    if (character & orientation).bit_count() % 2
                    else 1.0
                )
                tensor = projector.reshape(
                    irrep_dimension,
                    carrier_dimension,
                    irrep_dimension,
                    carrier_dimension,
                )
                output[:, target_column] += (
                    sign
                    * tensor[:, :, column, :].reshape(-1)
                    / normalization
                )
    return output


def joint_character_analysis_maps(
    target: Partition,
    labels: tuple[Label, ...],
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Return ``(D_nu, A_nu, N_nu, N_nu_circuit)`` from (2)--(3)."""

    multiplicity, _, projectors = predicted_joint_multiplicity_operator(
        target,
        labels,
    )
    irrep_dimension = hook_length_dimension(target)
    carrier_dimension = math.prod(
        hook_length_dimension(left) * hook_length_dimension(right)
        for left, right in labels
    )
    count = len(projectors)
    factor = projection_gram_factor(
        projectors,
        irrep_dimension,
        carrier_dimension,
    )
    rotation = np.kron(
        np.eye(irrep_dimension),
        walsh_matrix(len(labels)),
    )
    target_analysis = (
        math.sqrt(irrep_dimension / (count * carrier_dimension))
        * factor
        @ rotation.conj().T
    )
    canonical = (
        factor @ rotation.conj().T / math.sqrt(count * carrier_dimension)
    )
    circuit = canonical_projector_erasure_map(
        projectors,
        irrep_dimension,
        carrier_dimension,
    )
    return multiplicity, target_analysis, canonical, circuit


def generic_analysis_amplification_degree_lower_bound(
    irrep_dimension: int,
    error: float = 0.01,
) -> int:
    """Conservative Bernstein bound for ``A/sqrt(d) -> A`` uniformly."""

    if irrep_dimension < 1:
        raise ValueError("irrep_dimension must be positive")
    if not 0 <= error < 0.5:
        raise ValueError("error must lie in [0, 1/2)")
    if irrep_dimension == 1:
        return 1
    # The exact Bernstein consequence is degree >= (1-2e)sqrt(d-1).
    root_lower = math.isqrt(irrep_dimension - 1)
    epsilon = Fraction(str(error))
    lower = (1 - 2 * epsilon) * root_lower
    return max(1, (lower.numerator + lower.denominator - 1) // lower.denominator)


def audit_joint_analysis_map(
    n: int,
    target: Partition,
    labels: tuple[Label, ...],
    *,
    control_id: str,
    tolerance: float = 1e-9,
) -> JointAnalysisMapControl:
    if sum(target) != n:
        raise ValueError("target partition has the wrong degree")
    multiplicity, target_analysis, canonical, circuit = (
        joint_character_analysis_maps(target, labels)
    )
    dimension = hook_length_dimension(target)
    carrier_dimension = math.prod(
        hook_length_dimension(left) * hook_length_dimension(right)
        for left, right in labels
    )
    count = 1 << len(labels)
    eigenvalues = np.linalg.eigvalsh((multiplicity + multiplicity.conj().T) / 2)
    positive = eigenvalues[eigenvalues > tolerance]
    if not len(positive):
        raise ValueError("target multiplicity operator is inactive")
    target_singular = np.linalg.svd(target_analysis, compute_uv=False)
    target_positive = target_singular[target_singular > tolerance]
    canonical_singular = np.linalg.svd(canonical, compute_uv=False)
    canonical_positive = canonical_singular[canonical_singular > tolerance]
    target_gram_residual = float(
        np.linalg.norm(target_analysis.conj().T @ target_analysis - multiplicity)
    )
    circuit_residual = float(np.linalg.norm(canonical - circuit))
    canonical_gram_residual = float(
        np.linalg.norm(canonical.conj().T @ canonical - multiplicity / dimension)
    )
    singular_residual = float(
        np.linalg.norm(
            np.sort(target_positive)
            - math.sqrt(dimension) * np.sort(canonical_positive)
        )
    )
    polar_residual = float(
        np.linalg.norm(
            _direct_polar(target_analysis, tolerance)
            - _direct_polar(canonical, tolerance)
        )
    )
    verified = bool(
        target_gram_residual <= 100 * tolerance
        and circuit_residual <= 100 * tolerance
        and canonical_gram_residual <= 100 * tolerance
        and singular_residual <= 100 * tolerance
        and polar_residual <= 100 * tolerance
    )
    return JointAnalysisMapControl(
        control_id=control_id,
        n=n,
        target_partition=target,
        labels=labels,
        irrep_dimension=dimension,
        orientation_count=count,
        source_carrier_dimension=carrier_dimension,
        analysis_input_dimension=dimension * count,
        analysis_output_dimension=dimension * carrier_dimension**2,
        multiplicity_operator_rank=len(positive),
        minimum_positive_multiplicity_eigenvalue=float(positive[0]),
        maximum_multiplicity_eigenvalue=float(positive[-1]),
        minimum_positive_target_analysis_singular_value=float(target_positive[-1]),
        maximum_target_analysis_singular_value=float(target_positive[0]),
        canonical_analysis_normalization_sqrt_irrep=math.sqrt(dimension),
        target_gram_residual=target_gram_residual,
        canonical_erasure_map_residual=circuit_residual,
        canonical_gram_residual=canonical_gram_residual,
        singular_value_scaling_residual=singular_residual,
        polar_scale_invariance_residual=polar_residual,
        generic_amplification_degree_lower_bound=(
            generic_analysis_amplification_degree_lower_bound(dimension)
        ),
        exact_analysis_normalization_theorem_verified=verified,
        status=(
            "exact-joint-analysis-map-sqrt-row-normalization"
            if verified
            else "joint-analysis-map-normalization-validation-failure"
        ),
    )


def joint_analysis_map_scaling_record(
    n: int,
    *,
    error: float = 0.01,
) -> JointAnalysisMapScalingRecord:
    partition, dimension = balanced_two_row_irrep_dimension(n)
    lower = generic_analysis_amplification_degree_lower_bound(dimension, error)
    return JointAnalysisMapScalingRecord(
        n=n,
        witness_partition=partition,
        witness_irrep_dimension_decimal=str(dimension),
        witness_irrep_dimension_log2=math.log2(dimension),
        canonical_direct_analysis_normalization="sqrt(d_nu)",
        density_rescaling_degree_order="Omega(d_nu)",
        direct_analysis_amplification_degree_order="Omega(sqrt(d_nu))",
        generic_direct_analysis_degree_lower_bound_decimal=str(lower),
        generic_direct_analysis_degree_log2_lower_bound=math.log2(lower),
        balanced_two_row_dimension_exponential=True,
        witness_sector_natural_mass_proved=False,
        direct_polar_compiled=False,
        direct_structured_polar_ruled_out=False,
        status="canonical-analysis-access-has-exponential-generic-amplification",
    )


def run_joint_analysis_map_normalization() -> JointAnalysisMapReport:
    threshold_labels = (
        ((3,), (2, 1)),
        ((3,), (1, 1, 1)),
        ((2, 1), (1, 1, 1)),
    )
    w4_labels = _w4_collision_free_labels()[0]
    controls = [
        audit_joint_analysis_map(
            3,
            (2, 1),
            threshold_labels,
            control_id="W3-THRESHOLD-STANDARD",
        ),
        audit_joint_analysis_map(
            4,
            (3, 1),
            w4_labels,
            control_id="W4-COLLISION-FREE-31",
        ),
        audit_joint_analysis_map(
            4,
            (2, 2),
            w4_labels,
            control_id="W4-COLLISION-FREE-22",
        ),
    ]
    scaling = [
        joint_analysis_map_scaling_record(n)
        for n in (8, 16, 32, 64, 128, 256, 512)
    ]
    failures = sum(
        not row.exact_analysis_normalization_theorem_verified
        for row in controls
    )
    verified = failures == 0
    theorem = JointAnalysisMapTheorem(
        exact_analysis_factor=(
            "A_nu=sqrt(d_nu/(q dim(C))) L_nu(I tensor W)^*."
        ),
        exact_gram="A_nu^*A_nu=D_nu.",
        canonical_circuit=(
            "Walsh preparation, carrier EPR preparation, controlled E_e, and one "
            "Walsh-row work-label erasure implement N_nu."
        ),
        canonical_normalization=(
            "N_nu=A_nu/sqrt(d_nu), so N_nu^*N_nu=D_nu/d_nu."
        ),
        density_access_equivalence=(
            "The canonical direct-analysis Gram is exactly the fixed-row block of "
            "the global purification density encoding."
        ),
        generic_amplification_boundary=(
            "Uniform bounded-polynomial amplification from N_nu to A_nu has degree "
            "Omega(sqrt(d_nu)); balanced two-row dimensions make this exponential."
        ),
        scope=(
            "The bound applies to this normalized access plus uniform polynomial "
            "transformation. It does not rule out direct polar synthesis, multi-round "
            "branch relocation, or a fused representation-specific isometry."
        ),
        theorem_verified=verified,
        status=(
            "joint-analysis-map-exact-canonical-sqrt-row-boundary"
            if verified
            else "joint-analysis-map-normalization-validation-failure"
        ),
    )
    return JointAnalysisMapReport(
        created_at=utc_now(),
        theorem_contract=asdict(theorem),
        theorem=theorem,
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "identify_rectangular_joint_multiplicity_analysis",
                "resolved": verified,
                "resolution": (
                    "The projection-Gram factor and branch Walsh rotation give A_nu "
                    "with Gram D_nu exactly."
                ),
            },
            {
                "obligation": "charge_canonical_projector_erasure_normalization",
                "resolved": verified,
                "resolution": (
                    "The carrier EPR contributes 1/sqrt(dim(C)) and selected Walsh-row "
                    "erasure contributes 1/sqrt(q), yielding A_nu/sqrt(d_nu)."
                ),
            },
            {
                "obligation": "reconcile_direct_and_density_access",
                "resolved": verified,
                "resolution": (
                    "The canonical direct Gram is D_nu/d_nu, exactly the Schur-row "
                    "density block."
                ),
            },
            {
                "obligation": "construct_direct_structured_polar",
                "resolved": False,
                "resolution": (
                    "The scalar normalization leaves polar(A_nu) unchanged, but no "
                    "circuit implements that polar without generic amplification."
                ),
            },
            {
                "obligation": "prove_large_row_natural_information_mass",
                "resolved": False,
                "resolution": (
                    "The balanced irrep is an access witness only; source probability "
                    "and hidden-label information remain unproved."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "The projection-Gram factor already gives normalization-one A_nu.",
                "resolved": True,
                "resolution": (
                    "Algebraically yes, operationally no: the canonical coherent "
                    "projector-erasure top block is A_nu/sqrt(d_nu)."
                ),
            },
            {
                "objection": "Direct analysis has the same Omega(d_nu) cost as density access.",
                "resolved": True,
                "resolution": (
                    "False: the rectangular factor exposes square-root singular values, "
                    "improving the generic burden to Omega(sqrt(d_nu))."
                ),
            },
            {
                "objection": "The scalar loss changes the desired polar.",
                "resolved": True,
                "resolution": (
                    "It does not: polar(A_nu/sqrt(d_nu))=polar(A_nu) exactly."
                ),
            },
            {
                "objection": "Small normalized singular values prove the polar is hard.",
                "resolved": False,
                "resolution": (
                    "They prove only a generic polynomial-transform boundary. Structured "
                    "direct polars can bypass small normalized singular scales."
                ),
            },
            {
                "objection": "The balanced dimension alone closes the physical route.",
                "resolved": False,
                "resolution": (
                    "No natural source-mass theorem or all-circuit lower bound is supplied."
                ),
            },
        ],
        headline_metrics={
            "exact_rectangular_analysis_factor_theorem_count": 1,
            "canonical_projector_erasure_normalization_theorem_count": 1,
            "direct_density_gram_equivalence_theorem_count": 1,
            "generic_sqrt_row_amplification_boundary_count": 1,
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "maximum_finite_irrep_dimension": max(
                row.irrep_dimension for row in controls
            ),
            "maximum_scaling_witness_irrep_log2_dimension": max(
                row.witness_irrep_dimension_log2 for row in scaling
            ),
            "maximum_generic_direct_analysis_degree_log2_lower_bound": max(
                row.generic_direct_analysis_degree_log2_lower_bound
                for row in scaling
            ),
            "direct_structured_polar_compiler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "joint_rectangular_analysis_factor_identified": verified,
            "joint_rectangular_analysis_gram_equals_D_nu": verified,
            "canonical_projector_erasure_access_constructed": verified,
            "canonical_access_normalization_is_sqrt_d_nu": verified,
            "canonical_access_gram_equals_D_nu_over_d_nu": verified,
            "generic_direct_analysis_amplification_costs_omega_sqrt_d_nu": True,
            "normalization_one_A_nu_access_constructed": False,
            "large_row_sector_natural_information_mass_proved": False,
            "direct_structured_polar_compiled": False,
            "direct_structured_polar_ruled_out": False,
            "polynomial_joint_decoder_proved": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The exact direct factor is known, but its canonical coherent access is "
                "A_nu/sqrt(d_nu). Generic amplification remains exponential on growing "
                "balanced sectors, while a direct structured polar remains open."
            ),
        },
        status=theorem.status,
        summary=(
            "Identified the exact rectangular joint-character analysis map and proved "
            "the sqrt(d_nu) normalization of its canonical coherent implementation."
        ),
        falsifiers_triggered=[
            (
                "Writing D_nu as an explicit Gram does not by itself supply "
                "normalization-one coherent access to its factor."
            ),
            (
                "Direct factor access is strictly better normalized than density "
                "rescaling but is still generically exponential on growing-row sectors."
            ),
            (
                "The normalization barrier cannot be promoted to a polar or circuit "
                "lower bound because scalar rescaling leaves the polar unchanged."
            ),
        ],
    )


def write_joint_analysis_map_normalization_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str = "",
) -> dict[str, Any]:
    del write_registry, registry_experiment_id, registry_candidate_id, registry_result_id
    payload = asdict(run_joint_analysis_map_normalization())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_joint_analysis_map_normalization_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
