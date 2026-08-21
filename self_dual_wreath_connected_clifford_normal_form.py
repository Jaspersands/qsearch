"""Clifford theory exposes, but does not solve, the connected CS polar.

Let ``L=A_n^(2K+1) semidirect P_K`` be the zero-syndrome connected group.
Consider an ``A_n`` tensor label with no self-conjugate constituent and no
two coordinate constituents related by equality or odd conjugation.  Its
inertia group in ``L`` is

    H=A_n^(2K+1) semidirect C,

where ``C`` is the ``K+1`` dimensional orientation sign code.  The branch
group ``B=C_2^K`` acts freely on the coordinate tuple, so a corresponding
Clifford irrep has the induced normal form

    Ind_H^L(alpha_tilde) = direct_sum_(e in B) V_alpha.    (1)

The ``B`` action is regular translation on the branch index.  Therefore

    Fix_B = {|+_B> tensor v : v in V_alpha}.               (2)

The zero diagonal ``D`` lies in ``H``.  On branch ``e``, its action is the
conjugated orientation diagonal ``H_e`` on ``V_alpha``.  If ``E_e`` is the
corresponding invariant projector, then

    P_D = direct_sum_e E_e,
    Fix_D = direct_sum_e |e> tensor Ran(E_e).               (3)

Let ``S_B:v -> |+_B> tensor v`` be the fixed-space embedding.  Equations
(2)-(3) give the exact cross Gram

    S_B^* P_D S_B = (1/q) sum_e E_e = F/q,   q=2^K.        (4)

More strongly, the polar of ``P_D S_B`` is

    polar(P_D S_B) = stack_e E_e F^(+/2),                  (5)

which is exactly the complete orientation analysis polar.  Thus a coherent
Clifford transform that only exposes the induced branch orbit, inertia labels,
and subgroup-fixed projectors has merely reconstructed the original frame.
It has not diagonalized or normalized the matrix CS overlap.

The solved pair-GPE primitive remains compatible with this normal form but
does not change (4): it transports one carrier through a pair principal block
while preserving opaque multiplicity.  A full compiler needs a direct polar
for the many-way operator in (4), or a polynomial holonomy/F-move network
proved to equal (5).

The normal form is conditional on the nonsplit, odd-conjugacy-collision-free
``A_n`` tuple.  Equality or conjugate collisions among independent Plancherel
draws have asymptotically vanishing union bound because the Plancherel
collision probability is ``exp(-Theta(sqrt(n)))`` and there are only
``poly(n)`` draws.  No asymptotic theorem excluding self-conjugate partitions
from the whole natural tuple is used here; split sectors remain a separate
obligation.

This is a no-free-lunch theorem for ordinary Clifford/QFT completion, not an
arbitrary-circuit lower bound.  A Clifford transform augmented with the
actual fixed-space CS SVD would solve the gate by definition.  No such
normalization-one transform, decoder, classical separation, or speedup is
claimed.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_orientation_fourier_reduction import (
    orientation_invariant_projector,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_connected_clifford_normal_form.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-CONNECTED-CLIFFORD-NORMAL-FORM"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Label = tuple[Partition, Partition]


@dataclass(frozen=True)
class CliffordFixedSpaceControl:
    control_id: str
    n: int
    target_partition: Partition
    labels: tuple[Label, ...]
    orientation_count: int
    base_carrier_dimension: int
    induced_carrier_dimension: int
    branch_fixed_dimension: int
    diagonal_fixed_dimension: int
    frame_rank: int
    distinct_positive_cross_gram_eigenvalue_count: int
    minimum_positive_cross_gram_eigenvalue: float
    maximum_positive_cross_gram_eigenvalue: float
    maximum_branch_fixed_isometry_residual: float
    maximum_diagonal_projector_residual: float
    cross_gram_identity_residual: float
    polar_orientation_analysis_residual: float
    normalized_overlap_already_partial_isometry: bool
    exact_clifford_fixed_space_normal_form_verified: bool
    status: str


@dataclass(frozen=True)
class CliffordNormalFormScalingRecord:
    n: int
    copy_count: int
    orientation_count_log2: int
    inertia_sign_code_dimension: int
    branch_orbit_dimension_log2: int
    induced_branch_basis_polynomial: bool
    ordinary_clifford_orbit_transform_polynomial_if_a_qft_available: bool
    self_conjugate_tuple_absence_proved: bool
    normalized_flat_overlap_singular_amplitude_log2: float
    ordinary_clifford_labels_compile_cs_polar: bool
    status: str


@dataclass(frozen=True)
class ConnectedCliffordNormalFormTheorem:
    sector_condition: str
    inertia_group: str
    induced_carrier: str
    branch_fixed_space: str
    diagonal_fixed_space: str
    cross_gram: str
    cross_polar: str
    qft_boundary: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class ConnectedCliffordNormalFormReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: ConnectedCliffordNormalFormTheorem
    finite_controls: list[CliffordFixedSpaceControl]
    scaling_records: list[CliffordNormalFormScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _support(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    values, vectors = np.linalg.eigh((matrix + matrix.conj().T) / 2.0)
    basis = vectors[:, values > tolerance]
    return basis @ basis.conj().T


def _inverse_square_root(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    values, vectors = np.linalg.eigh((matrix + matrix.conj().T) / 2.0)
    inverse = np.zeros_like(values)
    inverse[values > tolerance] = 1.0 / np.sqrt(values[values > tolerance])
    return (vectors * inverse) @ vectors.conj().T


def _polar(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    left, singular_values, right_star = np.linalg.svd(matrix, full_matrices=False)
    retained = singular_values > tolerance
    return left[:, retained] @ right_star[retained, :]


def audit_clifford_fixed_space_normal_form(
    control_id: str,
    target_partition: Partition,
    labels: tuple[Label, ...],
    *,
    tolerance: float = 1e-9,
) -> CliffordFixedSpaceControl:
    if not labels:
        raise ValueError("at least one source pair is required")
    projectors = tuple(
        orientation_invariant_projector(target_partition, labels, orientation)
        for orientation in range(1 << len(labels))
    )
    dimension = projectors[0].shape[0]
    orientation_count = len(projectors)
    induced_dimension = orientation_count * dimension
    branch_embedding = np.vstack(
        tuple(np.eye(dimension) for _ in range(orientation_count))
    ) / math.sqrt(orientation_count)
    diagonal_projector = np.zeros(
        (induced_dimension, induced_dimension),
        dtype=complex,
    )
    for orientation, projector in enumerate(projectors):
        start = orientation * dimension
        diagonal_projector[
            start : start + dimension,
            start : start + dimension,
        ] = projector
    frame = sum(projectors, np.zeros_like(projectors[0]))
    cross_gram = branch_embedding.conj().T @ diagonal_projector @ branch_embedding
    predicted_gram = frame / orientation_count
    cross_map = diagonal_projector @ branch_embedding
    exact_polar = _polar(cross_map, tolerance)
    predicted_polar = np.vstack(projectors) @ _inverse_square_root(frame, tolerance)
    eigenvalues = np.linalg.eigvalsh((cross_gram + cross_gram.conj().T) / 2.0)
    positive = eigenvalues[eigenvalues > tolerance]
    rounded = {round(float(value), 10) for value in positive}
    branch_isometry = float(
        np.linalg.norm(
            branch_embedding.conj().T @ branch_embedding - np.eye(dimension),
            ord=2,
        )
    )
    diagonal_residual = float(
        np.linalg.norm(
            diagonal_projector @ diagonal_projector - diagonal_projector,
            ord=2,
        )
    )
    gram_residual = float(np.linalg.norm(cross_gram - predicted_gram, ord=2))
    polar_residual = float(np.linalg.norm(exact_polar - predicted_polar, ord=2))
    already_polar = bool(
        len(positive)
        and np.max(np.abs(positive - 1.0)) <= tolerance
    )
    frame_rank = int(np.count_nonzero(np.linalg.eigvalsh(frame) > tolerance))
    diagonal_rank = sum(
        int(np.count_nonzero(np.linalg.eigvalsh(projector) > tolerance))
        for projector in projectors
    )
    verified = bool(
        branch_isometry <= tolerance
        and diagonal_residual <= tolerance
        and gram_residual <= tolerance
        and polar_residual <= 100 * tolerance
        and frame_rank == len(positive)
    )
    return CliffordFixedSpaceControl(
        control_id=control_id,
        n=sum(target_partition),
        target_partition=target_partition,
        labels=labels,
        orientation_count=orientation_count,
        base_carrier_dimension=dimension,
        induced_carrier_dimension=induced_dimension,
        branch_fixed_dimension=dimension,
        diagonal_fixed_dimension=diagonal_rank,
        frame_rank=frame_rank,
        distinct_positive_cross_gram_eigenvalue_count=len(rounded),
        minimum_positive_cross_gram_eigenvalue=(
            float(positive[0]) if len(positive) else 0.0
        ),
        maximum_positive_cross_gram_eigenvalue=(
            float(positive[-1]) if len(positive) else 0.0
        ),
        maximum_branch_fixed_isometry_residual=branch_isometry,
        maximum_diagonal_projector_residual=diagonal_residual,
        cross_gram_identity_residual=gram_residual,
        polar_orientation_analysis_residual=polar_residual,
        normalized_overlap_already_partial_isometry=already_polar,
        exact_clifford_fixed_space_normal_form_verified=verified,
        status=(
            "exact-clifford-fixed-space-cross-gram-recovers-orientation-frame"
            if verified
            else "clifford-fixed-space-control-failure"
        ),
    )


def clifford_normal_form_scaling_record(n: int) -> CliffordNormalFormScalingRecord:
    if n < 5:
        raise ValueError("n must be at least five")
    group_order = math.factorial(n)
    copy_count = (group_order - 1).bit_length() + 2
    return CliffordNormalFormScalingRecord(
        n=n,
        copy_count=copy_count,
        orientation_count_log2=copy_count,
        inertia_sign_code_dimension=copy_count + 1,
        branch_orbit_dimension_log2=copy_count,
        induced_branch_basis_polynomial=True,
        ordinary_clifford_orbit_transform_polynomial_if_a_qft_available=True,
        self_conjugate_tuple_absence_proved=False,
        normalized_flat_overlap_singular_amplitude_log2=(
            -0.5 * math.log2(group_order)
        ),
        ordinary_clifford_labels_compile_cs_polar=False,
        status="clifford-orbit-basis-exposes-original-frame-cs-polar-open",
    )


def run_connected_clifford_normal_form() -> ConnectedCliffordNormalFormReport:
    controls = [
        audit_clifford_fixed_space_normal_form(
            "S3-ONE-UNEQUAL-PAIR",
            (2, 1),
            (((3,), (2, 1)),),
        ),
        audit_clifford_fixed_space_normal_form(
            "S3-TWO-MIXED-PAIRS",
            (2, 1),
            (
                ((3,), (2, 1)),
                ((2, 1), (1, 1, 1)),
            ),
        ),
        audit_clifford_fixed_space_normal_form(
            "S4-TWO-UNEQUAL-PAIRS",
            (3, 1),
            (
                ((4,), (3, 1)),
                ((2, 2), (2, 1, 1)),
            ),
        ),
    ]
    scaling = [
        clifford_normal_form_scaling_record(n)
        for n in (5, 6, 8, 10, 12, 16, 20, 24, 32, 48, 64, 96, 128)
    ]
    failures = sum(
        not row.exact_clifford_fixed_space_normal_form_verified for row in controls
    )
    nontrivial = sum(not row.normalized_overlap_already_partial_isometry for row in controls)
    verified = failures == 0 and nontrivial == len(controls)
    theorem = ConnectedCliffordNormalFormTheorem(
        sector_condition=(
            "All A_n coordinate constituents are nonsplit and distinct up to odd conjugation."
        ),
        inertia_group="H=A_n^(2K+1) semidirect C, with C the orientation sign code.",
        induced_carrier="Ind_H^L(alpha_tilde)=direct_sum_(e in B)V_alpha.",
        branch_fixed_space="Fix_B=|+_B> tensor V_alpha.",
        diagonal_fixed_space=(
            "P_D=direct_sum_e E_e and Fix_D=direct_sum_e |e> Ran(E_e)."
        ),
        cross_gram="S_B^*P_DS_B=(1/2^K)sum_e E_e=F/2^K.",
        cross_polar="polar(P_DS_B)=stack_e E_e F^(+/2), the orientation analysis polar.",
        qft_boundary=(
            "Ordinary Clifford orbit/stabilizer labels reconstruct this cross "
            "Gram but do not perform its matrix CS normalization."
        ),
        scope=(
            "Split self-conjugate sectors, a direct CS transform, complete "
            "orientation polar, classical separation, and speedup remain open."
        ),
        theorem_verified=verified,
        status=(
            "connected-clifford-normal-form-reconstructs-orientation-cs-polar-open"
            if verified
            else "connected-clifford-normal-form-control-failure"
        ),
    )
    return ConnectedCliffordNormalFormReport(
        created_at=utc_now(),
        theorem_contract=asdict(theorem),
        theorem=theorem,
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "derive_generic_nonsplit_clifford_induced_carrier",
                "resolved": True,
                "resolution": (
                    "The sign code is the inertia quotient and B acts freely, "
                    "giving the regular branch-orbit normal form."
                ),
            },
            {
                "obligation": "compute_B_and_D_fixed_spaces_in_clifford_basis",
                "resolved": verified,
                "resolution": (
                    "B fixes the uniform branch vector and D is block diagonal "
                    "with orientation invariant projectors E_e."
                ),
            },
            {
                "obligation": "identify_clifford_fixed_space_cs_polar",
                "resolved": verified,
                "resolution": (
                    "Its cross Gram is F/2^K and its exact polar is the original "
                    "stacked orientation polar in all three controls."
                ),
            },
            {
                "obligation": "compile_matrix_cs_normalization_inside_L_transform",
                "resolved": False,
                "resolution": (
                    "A conventional orbit/stabilizer QFT exposes the two fixed "
                    "spaces but does not apply the inverse square root of F."
                ),
            },
            {
                "obligation": "handle_self_conjugate_split_A_n_constituents",
                "resolved": False,
                "resolution": (
                    "Odd conjugation swaps split constituents and no natural-tuple "
                    "absence theorem is assumed."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Completing the full connected-group QFT automatically diagonalizes the polar.",
                "resolved": True,
                "resolution": (
                    "False for the ordinary Clifford transform: it yields exactly "
                    "the branch basis in which the cross Gram is F/2^K."
                ),
            },
            {
                "objection": "The Clifford branch orbit removes inverse-width normalization.",
                "resolved": True,
                "resolution": (
                    "False. The uniform B-fixed embedding contributes the explicit "
                    "1/2^K factor in equation (4)."
                ),
            },
            {
                "objection": "This proves no L-based circuit can work.",
                "resolved": True,
                "resolution": (
                    "Not proved. An L transform augmented by a direct fixed-space "
                    "CS basis or holonomy network could still implement the polar."
                ),
            },
            {
                "objection": "A-collision-free nonsplit tuples are already proved to have full natural mass.",
                "resolved": True,
                "resolution": (
                    "Equality/conjugate collisions are asymptotically controlled, "
                    "but self-conjugate split incidence remains an explicit open condition."
                ),
            },
        ],
        headline_metrics={
            "connected_clifford_normal_form_theorem_count": int(verified),
            "clifford_cross_gram_orientation_frame_identity_count": int(verified),
            "clifford_cross_polar_orientation_polar_identity_count": int(verified),
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "nontrivial_normalized_overlap_control_count": nontrivial,
            "maximum_cross_gram_residual": max(
                row.cross_gram_identity_residual for row in controls
            ),
            "maximum_cross_polar_residual": max(
                row.polar_orientation_analysis_residual for row in controls
            ),
            "scaling_record_count": len(scaling),
            "ordinary_clifford_transform_cs_compiler_count": 0,
            "direct_matrix_cs_polar_compiler_count": 0,
            "complete_orientation_polar_compiler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "generic_nonsplit_connected_clifford_normal_form_proved": True,
            "clifford_fixed_space_cross_gram_equals_normalized_orientation_frame": verified,
            "clifford_fixed_space_cross_polar_equals_orientation_polar": verified,
            "ordinary_connected_group_qft_labels_compile_cs_polar": False,
            "self_conjugate_split_sectors_resolved": False,
            "direct_matrix_cs_polar_compiled": False,
            "complete_natural_orientation_polar_compiled": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Clifford theory gives an efficient-looking branch orbit but its "
                "fixed-space overlap is exactly the original normalized orientation "
                "frame. The matrix CS normalization remains the whole gate."
            ),
        },
        status=theorem.status,
        summary=(
            "Derived the generic connected-group Clifford normal form and proved "
            "that its B/D fixed-space CS problem is exactly the original orientation "
            "polar, closing ordinary full-group QFT completion as a shortcut."
        ),
        falsifiers_triggered=[
            "An ordinary connected-group Clifford/QFT basis change only exposes the original F/2^K cross Gram.",
            "The uniform branch orbit retains the inverse-width normalization explicitly.",
            "This equivalence is not an arbitrary-circuit lower bound; direct CS and holonomy transforms remain open.",
        ],
    )


def write_connected_clifford_normal_form_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_connected_clifford_normal_form())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    report = write_connected_clifford_normal_form_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
