"""The companion-only Schur stack does not supply the orientation polar.

The separate-to-joint Schur dilation gives, in a fixed target sector ``nu``,
orthogonal encoded source branches

    K_nu = direct_sum_e K_(nu,e),       K_(nu,e)=B_(nu,e) M_(nu,e),

where ``M_(nu,e)=ran(E_(nu,e))`` and every ``B_(nu,e)`` is an isometry into
the joint Schur companion.  The physical orientation kernel is

    H_nu[e,f] = Tr(E_(nu,e) E_(nu,f))/d_nu.                 (1)

This module audits a tempting compiler hypothesis: compose published Schur
or Clebsch--Gordan transforms, their inverses, source/target label controls,
and generalized-phase-estimation membership reflections, and regard the
result as a compiler for the polar of (1).

The exact companion-only access model is the branch-preserving algebra

    A_br = direct_sum_e End(K_(nu,e) tensor W),             (2)

with arbitrary polynomial workspace ``W``.  It is deliberately generous:
inside each source branch it permits an arbitrary coherent operation.  Every
product, adjoint, label-controlled operation, and selected workspace top block
from (2) still commutes with every source-branch projector ``Z_e``.  Published
Schur transforms provide the coordinate changes defining the ``B_(nu,e)``;
published invariant-projector/#BQP constructions provide labels or membership
reflections.  If the computation stays inside this encoded companion algebra,
none supplies a deterministic normalization-one operator with nonzero
``Z_f O Z_e`` for ``e != f``.

The successor addressed-cross-map theorem records an important distinction.
Once the already-compiled physical-invariant interface is used as a detour,
``decode e -> block-encode E_f -> encode f`` has signal block ``J_f^*J_e``
with LCU normalization one, and coherent GPE directly compiles each pair
polar.  This does not contradict the algebra statement because the detour
leaves ``A_br``.  Raw queried cross-map access is available; the unresolved
operation is the global positive metric assembly and its inverse-square-root
polar action across the address register.

By contrast, if ``H_nu`` has a cross-branch entry, its Moore--Penrose inverse
square root cannot lie in (2).  Indeed, with ``K=H_nu^(+/2)``,

    H_nu = ((K)^+)^2,                                      (3)

so commutation of ``K`` with every coordinate projector would force the same
commutation for ``H_nu``.  The Schur branch-merger equivalence then says that
the normalized merger requires either this cross multiplier or an equivalent
non-branch-preserving direct polar.

Exact ``S_3/S_4`` controls verify nonzero cross blocks in both ``H_nu`` and
``H_nu^(+/2)``, equation (3), and closure of branch-preserving workspace
circuits under selected top blocks.  Natural relevance is not inferred from
those controls: the existing Plancherel covering theorem separately proves
nonzero overlaps for a density-one set of balanced orientation pairs, while
the joint-sector theorem puts ``1-o(1)`` mass on high-dimensional targets.

This is a capability and typed-oracle no-go, not an arbitrary-circuit lower
bound.  High-dimensional Schur ``F``-moves are Schur--Weyl/Pieri basis changes;
they are not a published internal ``S_n`` Kronecker/Racah transition oracle.
A new non-branch-preserving companion operation could still compile the polar.
The minimal surviving target is therefore explicit: assemble the operator-
valued factors in all ``J_e^*J_f`` queries into the global positive address
kernel and compile its merger polar with polynomial normalization and an
inverse-polynomial useful spectral window on natural mass.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import hook_length_dimension
from research_registry import (
    NegativeResultRecord,
    upsert_negative_result,
    utc_now,
)
from self_dual_wreath_joint_character_multiplicity_gram import (
    Label,
    Partition,
    orientation_overlap_kernel,
)
from self_dual_wreath_orientation_fourier_reduction import (
    _w4_collision_free_labels,
    orientation_invariant_projector,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_schur_companion_transform_scope_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-SCHUR-COMPANION-TRANSFORM-SCOPE-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
NEGATIVE_RESULT_ID = "SCHUR-COMPANION-KNOWN-TRANSFORM-STACK-NO-POLAR"


PRIMARY_LITERATURE = (
    {
        "id": "beals-symmetric-qft-1997",
        "url": "https://doi.org/10.1145/258533.258548",
        "proved_primitive": "polynomial quantum Fourier transform over S_n",
        "not_supplied": "internal Specht tensor-product multiplicity transform",
    },
    {
        "id": "bacon-chuang-harrow-schur-2004",
        "url": "https://arxiv.org/abs/quant-ph/0407082",
        "proved_primitive": (
            "polynomial Schur--Weyl/Clebsch--Gordan transform and irrep-label GPE"
        ),
        "not_supplied": "internal S_n Kronecker branch transition",
    },
    {
        "id": "ikenmeyer-subramanian-kronecker-2023",
        "url": "https://arxiv.org/abs/2307.02389",
        "proved_primitive": "#BQP dimension of a commuting-projector image",
        "not_supplied": "coherent basis or state-dependent transition amplitudes",
    },
    {
        "id": "burchardt-high-dimensional-schur-2025",
        "url": "https://arxiv.org/abs/2509.22640",
        "proved_primitive": (
            "high-dimensional Schur transform with explicit Schur--Weyl F-moves"
        ),
        "not_supplied": "arbitrary internal Specht Kronecker/Racah F-move",
    },
    {
        "id": "christandl-et-al-plethysm-sharp-bqp-2026",
        "url": "https://arxiv.org/abs/2602.08441",
        "proved_primitive": "#BQP multiplicity access from repeated Schur transforms",
        "not_supplied": "multiplicity-coordinate basis or orientation polar",
    },
)


@dataclass(frozen=True)
class SchurCompanionScopeControl:
    control_id: str
    n: int
    target_partition: Partition
    labels: tuple[Label, ...]
    orientation_count: int
    active_orientation_count: int
    target_irrep_dimension: int
    orientation_kernel_rank: int
    minimum_positive_kernel_eigenvalue: float
    maximum_kernel_eigenvalue: float
    kernel_offdiagonal_frobenius_norm: float
    inverse_sqrt_offdiagonal_frobenius_norm: float
    maximum_kernel_branch_commutator_norm: float
    maximum_inverse_sqrt_branch_commutator_norm: float
    inverse_sqrt_reconstruction_residual: float
    branch_workspace_closure_residual: float
    selected_top_block_closure_residual: float
    best_branch_diagonal_inverse_sqrt_error: float
    cross_branch_multiplier_required: bool
    known_transform_stack_compiles_polar: bool
    exact_scope_boundary_verified: bool
    status: str


@dataclass(frozen=True)
class SchurCompanionScopeScalingRecord:
    n: int
    information_threshold_copy_count: int
    orientation_log2_width: int
    joint_local_dimension_log2: float
    collision_free_source_probability_tends_one: bool
    natural_high_dimensional_target_mass_tends_one: bool
    natural_balanced_pair_cross_overlap_density_tends_one: bool
    symmetric_group_qft_polynomial: bool
    high_dimensional_schur_transform_polynomial: bool
    invariant_membership_reflections_polynomial: bool
    known_stack_exposes_internal_kronecker_coordinates: bool
    known_stack_supplies_cross_branch_multiplier: bool
    physical_interface_supplies_addressed_raw_cross_map_block_encoding: bool
    addressed_raw_cross_map_block_encoding_normalization: float
    coherent_gpe_supplies_direct_pair_polar: bool
    known_stack_supplies_normalization_one_orientation_polar: bool
    direct_non_branch_preserving_companion_circuit_ruled_out: bool
    status: str


@dataclass(frozen=True)
class SchurCompanionScopeTheorem:
    input_space: str
    output_space: str
    access_model: str
    closure_theorem: str
    required_multiplier: str
    literature_type_boundary: str
    natural_relevance: str
    normalization_boundary: str
    classical_alternative: str
    minimal_surviving_oracle: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class SchurCompanionScopeReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: SchurCompanionScopeTheorem
    primary_literature: list[dict[str, str]]
    finite_controls: list[SchurCompanionScopeControl]
    scaling_records: list[SchurCompanionScopeScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _hermitian(matrix: np.ndarray) -> np.ndarray:
    return (matrix + matrix.conj().T) / 2.0


def _psd_pseudoinverse_square_root(
    matrix: np.ndarray,
    tolerance: float,
) -> np.ndarray:
    values, vectors = np.linalg.eigh(_hermitian(matrix))
    if values[0] < -100 * tolerance:
        raise ValueError("matrix must be positive semidefinite")
    transformed = np.zeros_like(values)
    positive = values > 100 * tolerance
    transformed[positive] = values[positive] ** -0.5
    return (vectors * transformed) @ vectors.conj().T


def _psd_pseudoinverse(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    values, vectors = np.linalg.eigh(_hermitian(matrix))
    transformed = np.zeros_like(values)
    positive = values > 100 * tolerance
    transformed[positive] = values[positive] ** -1.0
    return (vectors * transformed) @ vectors.conj().T


def _coordinate_projectors(dimension: int) -> tuple[np.ndarray, ...]:
    output = []
    for index in range(dimension):
        projector = np.zeros((dimension, dimension), dtype=complex)
        projector[index, index] = 1.0
        output.append(projector)
    return tuple(output)


def _maximum_branch_commutator(
    matrix: np.ndarray,
    projectors: tuple[np.ndarray, ...],
) -> float:
    return max(
        float(np.linalg.norm(matrix @ projector - projector @ matrix, ord=2))
        for projector in projectors
    )


def _offdiagonal_frobenius_norm(matrix: np.ndarray) -> float:
    diagonal = np.diag(np.diag(matrix))
    return float(np.linalg.norm(matrix - diagonal, ord="fro"))


def _branch_workspace_closure_control(
    branch_count: int,
    tolerance: float,
) -> tuple[float, float]:
    """Verify products and selected workspace blocks stay branch preserving."""

    workspace_dimension = 2
    total = branch_count * workspace_dimension
    first = np.zeros((total, total), dtype=complex)
    second = np.zeros_like(first)
    for branch in range(branch_count):
        angle = (branch + 1) / (branch_count + 2)
        rotation = np.asarray(
            [
                [math.cos(angle), -math.sin(angle)],
                [math.sin(angle), math.cos(angle)],
            ],
            dtype=complex,
        )
        phase = np.diag(
            [
                np.exp(1j * angle),
                np.exp(-1j * angle),
            ]
        )
        block = slice(
            branch * workspace_dimension,
            (branch + 1) * workspace_dimension,
        )
        first[block, block] = rotation
        second[block, block] = phase
    circuit = first.conj().T @ second @ first
    branch_projectors = []
    for branch in range(branch_count):
        projector = np.zeros((total, total), dtype=complex)
        block = slice(
            branch * workspace_dimension,
            (branch + 1) * workspace_dimension,
        )
        projector[block, block] = np.eye(workspace_dimension)
        branch_projectors.append(projector)
    closure = max(
        float(np.linalg.norm(circuit @ projector - projector @ circuit, ord=2))
        for projector in branch_projectors
    )
    top = np.zeros((branch_count, branch_count), dtype=complex)
    for left in range(branch_count):
        for right in range(branch_count):
            top[left, right] = circuit[
                left * workspace_dimension,
                right * workspace_dimension,
            ]
    top_closure = _maximum_branch_commutator(
        top,
        _coordinate_projectors(branch_count),
    )
    if max(closure, top_closure) > 100 * tolerance:
        raise ArithmeticError("branch-preserving closure control failed")
    return closure, top_closure


def audit_schur_companion_scope(
    n: int,
    target: Partition,
    labels: tuple[Label, ...],
    *,
    control_id: str,
    tolerance: float = 1e-9,
) -> SchurCompanionScopeControl:
    if not labels or any(
        sum(left) != n or sum(right) != n or left == right
        for left, right in labels
    ):
        raise ValueError("labels must be unequal partition pairs of n")
    if sum(target) != n:
        raise ValueError("target must partition n")
    target_dimension = hook_length_dimension(target)
    orientation_count = 1 << len(labels)
    projectors = tuple(
        orientation_invariant_projector(target, labels, orientation)
        for orientation in range(orientation_count)
    )
    active_projectors = tuple(
        projector
        for projector in projectors
        if np.trace(projector).real > 0.5
    )
    if len(active_projectors) < 2:
        raise ValueError("scope control requires two active orientation branches")
    kernel = _hermitian(
        orientation_overlap_kernel(active_projectors, target_dimension)
    )
    values = np.linalg.eigvalsh(kernel)
    positive = values[values > 100 * tolerance]
    if not len(positive):
        raise ValueError("orientation kernel must have positive support")
    inverse_root = _psd_pseudoinverse_square_root(kernel, tolerance)
    inverse_root_pseudoinverse = _psd_pseudoinverse(inverse_root, tolerance)
    reconstruction = inverse_root_pseudoinverse @ inverse_root_pseudoinverse
    reconstruction_residual = float(
        np.linalg.norm(reconstruction - kernel, ord=2)
    )
    coordinates = _coordinate_projectors(len(active_projectors))
    kernel_commutator = _maximum_branch_commutator(kernel, coordinates)
    inverse_commutator = _maximum_branch_commutator(inverse_root, coordinates)
    kernel_offdiagonal = _offdiagonal_frobenius_norm(kernel)
    inverse_offdiagonal = _offdiagonal_frobenius_norm(inverse_root)
    closure, top_closure = _branch_workspace_closure_control(
        len(active_projectors),
        tolerance,
    )
    cross_required = bool(
        kernel_offdiagonal > 100 * tolerance
        and inverse_offdiagonal > 100 * tolerance
        and kernel_commutator > 100 * tolerance
        and inverse_commutator > 100 * tolerance
    )
    verified = bool(
        cross_required
        and reconstruction_residual <= 1000 * tolerance
        and closure <= 100 * tolerance
        and top_closure <= 100 * tolerance
    )
    return SchurCompanionScopeControl(
        control_id=control_id,
        n=n,
        target_partition=target,
        labels=labels,
        orientation_count=orientation_count,
        active_orientation_count=len(active_projectors),
        target_irrep_dimension=target_dimension,
        orientation_kernel_rank=len(positive),
        minimum_positive_kernel_eigenvalue=float(positive[0]),
        maximum_kernel_eigenvalue=float(positive[-1]),
        kernel_offdiagonal_frobenius_norm=kernel_offdiagonal,
        inverse_sqrt_offdiagonal_frobenius_norm=inverse_offdiagonal,
        maximum_kernel_branch_commutator_norm=kernel_commutator,
        maximum_inverse_sqrt_branch_commutator_norm=inverse_commutator,
        inverse_sqrt_reconstruction_residual=reconstruction_residual,
        branch_workspace_closure_residual=closure,
        selected_top_block_closure_residual=top_closure,
        best_branch_diagonal_inverse_sqrt_error=inverse_offdiagonal,
        cross_branch_multiplier_required=cross_required,
        known_transform_stack_compiles_polar=False,
        exact_scope_boundary_verified=verified,
        status=(
            "known-transform-stack-cross-branch-type-mismatch-verified"
            if verified
            else "schur-companion-scope-control-failure"
        ),
    )


def schur_companion_scope_scaling(
    n: int,
) -> SchurCompanionScopeScalingRecord:
    if n < 3:
        raise ValueError("n must be at least three")
    log_order = math.lgamma(n + 1) / math.log(2.0)
    copies = math.ceil(3.0 * log_order) + 2
    return SchurCompanionScopeScalingRecord(
        n=n,
        information_threshold_copy_count=copies,
        orientation_log2_width=copies,
        joint_local_dimension_log2=copies * math.log2(n),
        collision_free_source_probability_tends_one=True,
        natural_high_dimensional_target_mass_tends_one=True,
        natural_balanced_pair_cross_overlap_density_tends_one=True,
        symmetric_group_qft_polynomial=True,
        high_dimensional_schur_transform_polynomial=True,
        invariant_membership_reflections_polynomial=True,
        known_stack_exposes_internal_kronecker_coordinates=False,
        known_stack_supplies_cross_branch_multiplier=False,
        physical_interface_supplies_addressed_raw_cross_map_block_encoding=True,
        addressed_raw_cross_map_block_encoding_normalization=1.0,
        coherent_gpe_supplies_direct_pair_polar=True,
        known_stack_supplies_normalization_one_orientation_polar=False,
        direct_non_branch_preserving_companion_circuit_ruled_out=False,
        status="companion-only-stack-insufficient-global-whitening-open",
    )


def run_schur_companion_transform_scope_boundary() -> SchurCompanionScopeReport:
    w4 = _w4_collision_free_labels()
    controls = [
        audit_schur_companion_scope(
            3,
            (2, 1),
            (
                ((3,), (2, 1)),
                ((3,), (1, 1, 1)),
                ((2, 1), (1, 1, 1)),
            ),
            control_id="S3-INFORMATION-THRESHOLD-CROSS-BRANCH",
        ),
        audit_schur_companion_scope(
            4,
            (2, 1, 1),
            w4[0],
            control_id="S4-COLLISION-FREE-CROSS-BRANCH-A",
        ),
        audit_schur_companion_scope(
            4,
            (3, 1),
            w4[1],
            control_id="S4-COLLISION-FREE-CROSS-BRANCH-B",
        ),
    ]
    scaling = [
        schur_companion_scope_scaling(n)
        for n in (8, 16, 32, 64, 128, 256, 512)
    ]
    failures = sum(not row.exact_scope_boundary_verified for row in controls)
    verified = failures == 0
    theorem = SchurCompanionScopeTheorem(
        input_space=(
            "K_nu=direct_sum_e K_(nu,e), the orthogonal fixed-source subspaces "
            "inside the joint Schur companion, with polynomial workspace W"
        ),
        output_space=(
            "the physical invariant span or, equivalently, the normalized "
            "Schur-branch merger range from the predecessor equivalence theorem"
        ),
        access_model=(
            "Companion-only Schur/QFT coordinate changes, source and target "
            "label controls, and supplied-label invariant membership reflections, "
            "before the separate physical-interface detour is admitted"
        ),
        closure_theorem=(
            "Every product, adjoint, coherent label control, and selected "
            "workspace top block in A_br=direct_sum_e End(K_e tensor W) "
            "commutes with every source-branch projector Z_e."
        ),
        required_multiplier=(
            "If H_nu has a cross entry, H_nu^(+/2) is not branch preserving; "
            "the orientation polar therefore requires a cross-branch primitive "
            "or an equivalent direct non-branch-preserving construction."
        ),
        literature_type_boundary=(
            "Schur--Weyl/Pieri F-moves and #BQP invariant-space projectors do "
            "not, by their proved interfaces, furnish internal Specht "
            "Kronecker branch transition amplitudes."
        ),
        natural_relevance=(
            "Existing target-uniform Plancherel covering gives nonzero cross "
            "overlaps on a density-one set of balanced natural orientation "
            "pairs; the joint-sector theorem puts 1-o(1) mass on large rows."
        ),
        normalization_boundary=(
            "The physical-interface/projector detour supplies each addressed raw "
            "J_f^*J_e query at alpha=1, but entry-query normalization does not "
            "set the normalization or hard edge of the full dense address kernel. "
            "A surviving global assembly must state alpha=poly(n) and an "
            "inverse-polynomial useful spectral window."
        ),
        classical_alternative=(
            "Exact character and representation-ring contractions form H_nu "
            "and diagonalize the finite controls classically. No polynomial "
            "all-n classical polar construction or quantum/classical separation "
            "is inferred from this finite computation."
        ),
        minimal_surviving_oracle=(
            "A coherent polynomial-normalized global PSD assembly of the "
            "operator-valued J_e^*J_f entries, with their positive metrics and "
            "holonomy retained, or a direct compiler for the equivalent merger polar."
        ),
        scope=(
            "This rejects only the claim that the cited transform/projector "
            "stack already supplies the cross operation. It does not reject "
            "new entangling companion circuits, a noncommuting Racah network, "
            "multi-round branch relocation, or a character-retaining decoder."
        ),
        theorem_verified=verified,
        status=(
            "companion-only-schur-stack-insufficient-global-whitening-open"
            if verified
            else "schur-companion-transform-scope-validation-failure"
        ),
    )
    return SchurCompanionScopeReport(
        created_at=utc_now(),
        theorem_contract=asdict(theorem),
        theorem=theorem,
        primary_literature=[dict(row) for row in PRIMARY_LITERATURE],
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "type_known_schur_and_projector_primitives",
                "resolved": True,
                "resolution": (
                    "Primary sources establish Schur--Weyl transforms, label "
                    "projection, and multiplicity counting, not the internal "
                    "Specht branch-transition oracle used by the orientation polar."
                ),
            },
            {
                "obligation": "prove_branch_preserving_stack_closure",
                "resolved": verified,
                "resolution": (
                    "The direct-sum algebra is closed under products, adjoints, "
                    "coherent label control, workspace extension, and selected top blocks."
                ),
            },
            {
                "obligation": "show_actual_orientation_multiplier_crosses_branches",
                "resolved": verified,
                "resolution": (
                    "Three exact S3/S4 controls have nonzero offdiagonal H_nu and "
                    "H_nu^(+/2), with equation H=((H^(+/2))^+)^2 verified."
                ),
            },
            {
                "obligation": "transfer_type_mismatch_to_natural_source_family",
                "resolved": True,
                "resolution": (
                    "The existing target-uniform Plancherel tensor-covering theorem "
                    "makes balanced cross overlaps density one after collision-free conditioning."
                ),
            },
            {
                "obligation": "compile_addressed_raw_cross_map_oracle",
                "resolved": True,
                "resolution": (
                    "The physical-interface/projector/interface sandwich has "
                    "signal block J_f^*J_e at alpha one for coherent e,f queries."
                ),
            },
            {
                "obligation": "compile_global_operator_valued_metric_assembly",
                "resolved": False,
                "resolution": (
                    "Entry-query access and direct pair polars do not construct "
                    "the dense PSD address-transition kernel. The full assembly "
                    "must retain positive cross metrics and charge its normalization."
                ),
            },
            {
                "obligation": "prove_high_dimensional_blocks_carry_hidden_information",
                "resolved": False,
                "resolution": (
                    "Natural target mass is proved, but a hidden-label information "
                    "and outcome-decoding theorem remains absent."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "High-dimensional Schur F-moves are the missing Racah transform.",
                "resolved": True,
                "resolution": (
                    "Their proved wires are Schur--Weyl GT/SYT and one-box Pieri "
                    "coupling wires, not arbitrary internal S_n Specht multiplicity wires."
                ),
            },
            {
                "objection": "A #BQP multiplicity projector exposes a basis of its image.",
                "resolved": True,
                "resolution": (
                    "Dimension of a projector image and membership reflection do "
                    "not supply coordinates or cross-image transition amplitudes."
                ),
            },
            {
                "objection": "Arbitrary coherent label control leaves the branch algebra.",
                "resolved": True,
                "resolution": (
                    "Control changes the within-branch block but has no nonzero "
                    "Z_f O Z_e block unless a cross-branch primitive is separately supplied."
                ),
            },
            {
                "objection": "The companion-only closure rules out queried raw cross-map access.",
                "resolved": True,
                "resolution": (
                    "It does not: the compiled physical interface leaves A_br, "
                    "block-encodes E_f, and returns through branch f. The closure "
                    "still rules out obtaining this transition without such a detour."
                ),
            },
            {
                "objection": "The finite offdiagonal controls prove an approximate circuit lower bound.",
                "resolved": True,
                "resolution": (
                    "They do not. The theorem is an exact access-type boundary; "
                    "no asymptotic approximation lower bound for new structured circuits is claimed."
                ),
            },
            {
                "objection": "Natural target mass proves hidden-involution information.",
                "resolved": False,
                "resolution": (
                    "The target irrep law is hidden-label independent; internal "
                    "multiplicity information and decoding are separate open gates."
                ),
            },
            {
                "objection": "Finite classical diagonalization supplies an asymptotic dequantization.",
                "resolved": True,
                "resolution": (
                    "Exact finite character contraction is a control and classical "
                    "alternative, not a polynomial all-n algorithm for the exponentially "
                    "wide orientation kernel. No separation claim is made in either direction."
                ),
            },
        ],
        headline_metrics={
            "known_transform_stack_scope_theorem_count": int(verified),
            "branch_algebra_closure_theorem_count": int(verified),
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "cross_branch_inverse_sqrt_control_count": sum(
                row.cross_branch_multiplier_required for row in controls
            ),
            "maximum_finite_inverse_sqrt_branch_commutator_norm": max(
                row.maximum_inverse_sqrt_branch_commutator_norm for row in controls
            ),
            "primary_literature_scope_count": len(PRIMARY_LITERATURE),
            "polynomial_global_cross_branch_whitening_oracle_count": 0,
            "addressed_raw_cross_map_block_encoding_count": 1,
            "direct_gpe_pair_polar_compiler_count": 1,
            "direct_structured_orientation_polar_compiler_count": 0,
            "hidden_involution_decoder_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "known_schur_qft_and_projector_interfaces_typed": verified,
            "branch_preserving_stack_closed_under_coherent_composition": verified,
            "actual_orientation_inverse_sqrt_requires_cross_branch_action": verified,
            "companion_only_stack_supplies_cross_branch_action": False,
            "known_transform_stack_compiles_orientation_polar": False,
            "physical_interface_supplies_addressed_raw_cross_map_block_encoding": True,
            "addressed_raw_cross_map_block_encoding_normalization_one": True,
            "coherent_gpe_supplies_direct_pair_polar": True,
            "high_dimensional_schur_f_moves_equal_internal_kronecker_racah": False,
            "multiplicity_counting_implies_coherent_basis": False,
            "natural_cross_orientation_overlap_density_one_proved": True,
            "natural_high_dimensional_target_mass_proved": True,
            "polynomial_normalized_global_cross_branch_whitening_oracle_compiled": False,
            "full_global_cross_branch_block_encoding_normalization_charged": False,
            "global_operator_valued_metric_assembly_compiled": False,
            "direct_structured_companion_polar_ruled_out": False,
            "multi_round_companion_transform_ruled_out": False,
            "branch_character_retaining_decoder_ruled_out": False,
            "high_dimensional_hidden_information_proved": False,
            "physical_pgm_compiled": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The companion-only stack is branch preserving, while the physical "
                "interface supplies alpha-one addressed raw cross maps and GPE "
                "supplies their pair polars. Neither result assembles the global "
                "positive address kernel or compiles its inverse-square-root polar."
            ),
        },
        status=theorem.status,
        summary=(
            "Falsified the hypothesis that companion-only Schur/CG and invariant-"
            "projector primitives already compile the physical orientation polar. "
            "The physical detour does supply addressed raw cross maps and pair "
            "polars; global positive metric assembly and whitening remain open."
        ),
        falsifiers_triggered=[
            "A Schur--Weyl F-move is not automatically an internal S_n Kronecker/Racah move.",
            "A #BQP invariant-space projector does not expose multiplicity coordinates.",
            "Coherent composition of branch-preserving primitives cannot create a cross-branch top block.",
            "Finite cross-block witnesses are not arbitrary-circuit or approximation lower bounds.",
        ],
    )


def write_schur_companion_transform_scope_boundary_report(
    path: Path = REPORT_PATH,
    *,
    write_registry: bool = True,
) -> dict[str, Any]:
    payload = asdict(run_schur_companion_transform_scope_boundary())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id=NEGATIVE_RESULT_ID,
                source=str(path),
                claim=(
                    "Published Schur/CG transforms and invariant-space projectors "
                    "already contain the cross-branch operation needed for the "
                    "joint-character orientation polar."
                ),
                reason_invalid=(
                    "The companion-only interface is branch preserving. The physical "
                    "detour supplies raw cross maps, but neither it nor pair GPE "
                    "assembles the global positive kernel or its H_nu^(+/2) action."
                ),
                lesson=(
                    "Require an explicit polynomial-normalized operator-valued "
                    "global metric assembly or a direct non-branch-preserving polar; "
                    "raw entry queries and pair phases are insufficient."
                ),
                applies_to=[
                    DEFAULT_CANDIDATE_ID,
                    "PO-MECHANISM",
                    "PO-MEASUREMENT",
                    "PO-COMPLEXITY",
                ],
                evidence={
                    "finite_control_count": payload["headline_metrics"][
                        "finite_control_count"
                    ],
                    "finite_control_failure_count": payload["headline_metrics"][
                        "finite_control_failure_count"
                    ],
                    "cross_branch_inverse_sqrt_control_count": payload[
                        "headline_metrics"
                    ]["cross_branch_inverse_sqrt_control_count"],
                    "primary_literature_scope_count": payload["headline_metrics"][
                        "primary_literature_scope_count"
                    ],
                    "natural_cross_orientation_overlap_density_one_proved": True,
                    "direct_structured_companion_polar_ruled_out": False,
                    "speedup_claim_allowed": False,
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_schur_companion_transform_scope_boundary_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
