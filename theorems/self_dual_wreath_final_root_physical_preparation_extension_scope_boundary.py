"""The compiled physical row-copy unitary is not an endpoint preparation.

The previous oracle boundary showed that non-first columns of a preparation
unitary matter.  This module audits the unitary interfaces that are actually
present in the Schur/QFT/GPE proof stack.

The one complete physical circuit relevant here is generalized Fourier
row-copy.  Write the aligned physical carrier as

    H_phys = direct_sum_epsilon H_e,
    U_s = direct_sum_epsilon U_(s,epsilon),                 (1)

and let ``Z_epsilon`` be its branch projectors.  For any full ancilla unitary
``P`` whose zero column prepares the uniform group state, the entire row-copy
unitary is

    W_P = (F_G^* tensor I)
          (sum_s |s><s| tensor U_s^*)
          (P tensor I).                                   (2)

Its zero-ancilla column is the previously proved row-copy isometry.  More is
true: since all endpoint-independent ancilla gates act trivially on
``H_phys`` and every ``U_s`` is branch diagonal,

    [W_P, I tensor Z_epsilon] = 0                          (3)

for every ``P`` and every branch.  Consequently every selected ancilla block

    W_(x,y)=(<x| tensor I) W_P (|y> tensor I)              (4)

commutes with all ``Z_epsilon``.  Products with the known companion-only
Schur/QFT/GPE workspace algebra retain the same property.  Changing the
uniform-state unitary extension changes nonzero ancilla columns, but none of
them becomes a cross-branch primitive.

This cannot hide the final endpoint Weyl byproduct.  For

    V_C=[sqrt(C);sqrt(I-C)],       B_U=V_C U V_C^*,         (5)

the left-to-right block is

    Z_0 B_U Z_1 = sqrt(C) U sqrt(I-C).                     (6)

If ``delta I<=C<=(1-delta)I`` and ``U`` is unitary, this block has minimum
singular value at least ``delta``.  Hence every branch-preserving operator
``O`` obeys

    ||B_U-O|| >= ||Z_0 B_U Z_1|| >= delta.                 (7)

No non-program column or ancilla block of (2) can therefore be a sufficiently
accurate block encoding of ``B_U`` on this strict effect window.

The register audit also finds that the current stack contains no compiled
full-domain unitary ``A_V`` satisfying ``A_V|0>=|V_C>>/sqrt(D)``.  The joint
character purification and final-root ``F=V sqrt(rho)`` are supplied as
purification/isometry or algebraic operator-state interfaces.  The physical
intertwiner explicitly factors the desired PGM through the still-uncompiled
orientation polar ``Q_R``.  Assuming a full endpoint preparation would thus
assume the missing operation rather than expose an overlooked column.

There is one genuine cross-branch resource: the physical-interface detour
already block-encodes each addressed ``J_f^*J_e`` at normalization one and GPE
compiles its pair polar.  These are pair-addressed signal oracles, not a full
endpoint preparation and not an assembled endpoint Weyl block.  The surviving
route is to build the byproduct or merger polar explicitly from those
available cross maps.

This is a typed-interface and algebra-closure theorem, not a lower bound for
new physical circuits.  It proves no typical-effect mass, physical PGM,
decoder, classical separation, or speedup.
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
from self_dual_wreath_final_root_byproduct_covariance_no_go import (
    canonical_endpoint,
)
from self_dual_wreath_final_root_purification_naimark_program_boundary import (
    _psd_power,
    weyl_unitary_error_basis,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_final_root_physical_preparation_extension_scope_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-FINAL-ROOT-"
    "PHYSICAL-PREPARATION-EXTENSION-SCOPE-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
NEGATIVE_RESULT_ID = (
    "SCHUR-COMPANION-FINAL-ROOT-PHYSICAL-PREPARATION-"
    "NONPROGRAM-COLUMNS-NO-BYPRODUCT"
)
BEALS_PAPER_ID = "beals-symmetric-qft-1997"
BEALS_PAPER_URL = "https://doi.org/10.1145/258533.258548"
BCH_PAPER_ID = "bacon-chuang-harrow-schur-2004"
BCH_PAPER_URL = "https://arxiv.org/abs/quant-ph/0407082"


@dataclass(frozen=True)
class FullRowCopyUnitaryControl:
    control_id: str
    group_dimension: int
    logical_dimension_per_branch: int
    physical_branch_count: int
    physical_data_dimension: int
    full_unitary_dimension: int
    uniform_preparation_extension_distance: float
    uniform_seed_column_residual: float
    maximum_preparation_unitarity_residual: float
    maximum_full_row_copy_unitarity_residual: float
    maximum_seeded_row_copy_isometry_residual: float
    seeded_row_copy_extension_invariance_residual: float
    maximum_full_unitary_branch_commutator_norm: float
    maximum_selected_ancilla_block_branch_commutator_norm: float
    maximum_composed_stack_branch_commutator_norm: float
    every_nonprogram_ancilla_block_branch_preserving: bool
    exact_full_row_copy_extension_scope_verified: bool
    status: str


@dataclass(frozen=True)
class EndpointByproductBranchSeparationControl:
    control_id: str
    logical_dimension: int
    effect_minimum_eigenvalue: float
    effect_maximum_eigenvalue: float
    strict_effect_window_delta: float
    endpoint_isometry_residual: float
    byproduct_operator_norm: float
    left_to_right_block_operator_norm: float
    left_to_right_block_minimum_singular_value: float
    certified_distance_from_branch_preserving_algebra: float
    actual_distance_to_branch_dephased_byproduct: float
    strict_window_lower_bound_residual: float
    row_copy_selected_block_can_equal_byproduct: bool
    exact_branch_separation_verified: bool
    status: str


@dataclass(frozen=True)
class PhysicalPreparationInterfaceRecord:
    primitive_id: str
    source_module: str
    input_registers: str
    output_registers: str
    contract_type: str
    full_domain_unitary_or_block_encoding_specified: bool
    branch_preserving_by_typed_interface: bool
    supplies_endpoint_program_column: bool
    supplies_addressed_cross_branch_signal: bool
    supplies_assembled_endpoint_weyl_byproduct: bool
    compiled: bool
    status: str


@dataclass(frozen=True)
class PhysicalPreparationScalingRecord:
    n: int
    information_threshold_copy_count: int
    permutation_register_log2_dimension: float
    orientation_branch_register_qubit_count: int
    generalized_row_copy_full_unitary_polynomial: bool
    generalized_row_copy_all_columns_branch_preserving: bool
    addressed_cross_map_block_encoding_normalization: float
    full_endpoint_preparation_unitary_compiled: bool
    endpoint_weyl_pair_compiled: bool
    typical_natural_effect_branch_separation_proved: bool
    status: str


@dataclass(frozen=True)
class PhysicalPreparationExtensionScopeTheorem:
    full_row_copy_unitary: str
    all_column_closure: str
    endpoint_byproduct_separation: str
    interface_inventory: str
    addressed_cross_map_exception: str
    surviving_route: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class PhysicalPreparationExtensionScopeReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: PhysicalPreparationExtensionScopeTheorem
    row_copy_controls: list[FullRowCopyUnitaryControl]
    byproduct_separation_controls: list[EndpointByproductBranchSeparationControl]
    interface_inventory: list[PhysicalPreparationInterfaceRecord]
    scaling_records: list[PhysicalPreparationScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    primary_literature: list[dict[str, str]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _fourier_unitary(dimension: int) -> np.ndarray:
    if dimension < 2:
        raise ValueError("dimension must be at least two")
    indices = np.arange(dimension, dtype=float)
    return np.exp(2j * np.pi * np.outer(indices, indices) / dimension) / math.sqrt(
        dimension
    )


def _block_diagonal(blocks: tuple[np.ndarray, ...]) -> np.ndarray:
    if not blocks:
        raise ValueError("at least one block is required")
    sizes = [block.shape[0] for block in blocks]
    if any(block.ndim != 2 or block.shape[1] != block.shape[0] for block in blocks):
        raise ValueError("blocks must be square")
    output = np.zeros((sum(sizes), sum(sizes)), dtype=complex)
    offset = 0
    for block, size in zip(blocks, sizes, strict=True):
        output[offset : offset + size, offset : offset + size] = block
        offset += size
    return output


def _cyclic_branch_representation_rows(
    group_dimension: int,
    logical_dimension: int,
) -> tuple[np.ndarray, ...]:
    """Return a two-branch unitary representation of a cyclic control group."""

    if group_dimension < 2 or logical_dimension < 2:
        raise ValueError("group and logical dimensions must be at least two")
    omega = np.exp(2j * np.pi / group_dimension)
    charges = np.arange(logical_dimension) % group_dimension
    basis = _fourier_unitary(logical_dimension)
    rows = []
    for element in range(group_dimension):
        left = np.diag(omega ** (element * charges))
        right_diagonal = np.diag(omega ** (element * (charges + 1)))
        right = basis @ right_diagonal @ basis.conj().T
        rows.append(_block_diagonal((left, right)))
    return tuple(rows)


def _uniform_preparation_extensions(
    group_dimension: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Return two full unitaries with the same uniform zero column."""

    first = _fourier_unitary(group_dimension)
    gauge = np.eye(group_dimension, dtype=complex)
    if group_dimension == 2:
        gauge[1, 1] = -1.0
    else:
        angle = 0.731
        cosine = math.cos(angle)
        sine = math.sin(angle)
        gauge[1:3, 1:3] = np.array(
            [[cosine, -sine], [sine, cosine]],
            dtype=complex,
        )
    second = first @ gauge
    return first, second


def full_generalized_row_copy_unitary(
    representation_rows: tuple[np.ndarray, ...],
    uniform_preparation: np.ndarray,
) -> np.ndarray:
    """Return the full unitary in equation (2)."""

    group_dimension = len(representation_rows)
    if uniform_preparation.shape != (group_dimension, group_dimension):
        raise ValueError("uniform preparation has the wrong shape")
    if not representation_rows:
        raise ValueError("representation rows cannot be empty")
    data_dimension = representation_rows[0].shape[0]
    identity = np.eye(data_dimension, dtype=complex)
    if any(row.shape != (data_dimension, data_dimension) for row in representation_rows):
        raise ValueError("representation row dimensions do not match")
    if any(
        np.linalg.norm(row.conj().T @ row - identity, ord=2) > 1e-8
        for row in representation_rows
    ):
        raise ValueError("representation rows must be unitary")
    select = _block_diagonal(
        tuple(row.conj().T for row in representation_rows)
    )
    fourier = _fourier_unitary(group_dimension)
    return (
        np.kron(fourier.conj().T, identity)
        @ select
        @ np.kron(uniform_preparation, identity)
    )


def _branch_projectors(logical_dimension: int) -> tuple[np.ndarray, np.ndarray]:
    zero = np.zeros((logical_dimension, logical_dimension), dtype=complex)
    identity = np.eye(logical_dimension, dtype=complex)
    return (
        np.block([[identity, zero], [zero, zero]]),
        np.block([[zero, zero], [zero, identity]]),
    )


def audit_full_row_copy_unitary(
    control_id: str,
    group_dimension: int,
    logical_dimension: int,
    *,
    tolerance: float = 1e-9,
) -> FullRowCopyUnitaryControl:
    """Verify full-unitary, seeded-column, and every-block closure identities."""

    rows = _cyclic_branch_representation_rows(group_dimension, logical_dimension)
    preparation_zero, preparation_one = _uniform_preparation_extensions(
        group_dimension
    )
    row_zero = full_generalized_row_copy_unitary(rows, preparation_zero)
    row_one = full_generalized_row_copy_unitary(rows, preparation_one)
    data_dimension = 2 * logical_dimension
    full_dimension = group_dimension * data_dimension
    identity_group = np.eye(group_dimension, dtype=complex)
    identity_data = np.eye(data_dimension, dtype=complex)
    identity_full = np.eye(full_dimension, dtype=complex)
    uniform = np.ones(group_dimension, dtype=complex) / math.sqrt(group_dimension)
    seed = np.zeros(group_dimension, dtype=complex)
    seed[0] = 1.0
    seed_embedding = np.kron(seed[:, None], identity_data)
    fourier = _fourier_unitary(group_dimension)
    expected_seeded = np.kron(fourier.conj().T, identity_data) @ (
        np.vstack(tuple(row.conj().T for row in rows))
        / math.sqrt(group_dimension)
    )
    seeded_zero = row_zero @ seed_embedding
    seeded_one = row_one @ seed_embedding
    branch_projectors = _branch_projectors(logical_dimension)

    preparation_unitarity = max(
        float(
            np.linalg.norm(
                preparation.conj().T @ preparation - identity_group,
                ord=2,
            )
        )
        for preparation in (preparation_zero, preparation_one)
    )
    full_unitarity = max(
        float(np.linalg.norm(row.conj().T @ row - identity_full, ord=2))
        for row in (row_zero, row_one)
    )
    seeded_isometry = max(
        float(np.linalg.norm(seeded.conj().T @ seeded - identity_data, ord=2))
        for seeded in (seeded_zero, seeded_one)
    )
    seeded_residual = max(
        float(np.linalg.norm(seeded_zero - expected_seeded, ord=2)),
        float(np.linalg.norm(seeded_one - expected_seeded, ord=2)),
    )
    full_commutator = 0.0
    selected_block_commutator = 0.0
    for row in (row_zero, row_one):
        tensor = row.reshape(
            group_dimension,
            data_dimension,
            group_dimension,
            data_dimension,
        )
        for projector in branch_projectors:
            extended = np.kron(identity_group, projector)
            full_commutator = max(
                full_commutator,
                float(np.linalg.norm(row @ extended - extended @ row, ord=2)),
            )
            for output_index in range(group_dimension):
                for input_index in range(group_dimension):
                    block = tensor[output_index, :, input_index, :]
                    selected_block_commutator = max(
                        selected_block_commutator,
                        float(
                            np.linalg.norm(
                                block @ projector - projector @ block,
                                ord=2,
                            )
                        ),
                    )

    phase = np.diag(np.exp(0.37j * np.arange(logical_dimension)))
    branch_workspace = _block_diagonal((phase, phase.conj().T))
    composed = (
        np.kron(identity_group, branch_workspace)
        @ row_one
        @ np.kron(identity_group, branch_workspace.conj().T)
    )
    composed_commutator = max(
        float(
            np.linalg.norm(
                composed @ np.kron(identity_group, projector)
                - np.kron(identity_group, projector) @ composed,
                ord=2,
            )
        )
        for projector in branch_projectors
    )
    extension_distance = float(
        np.linalg.norm(preparation_zero - preparation_one, ord=2)
    )
    uniform_seed_residual = max(
        float(np.linalg.norm(preparation_zero @ seed - uniform)),
        float(np.linalg.norm(preparation_one @ seed - uniform)),
    )
    extension_invariance = float(np.linalg.norm(seeded_zero - seeded_one, ord=2))
    verified = bool(
        extension_distance > 100 * tolerance
        and uniform_seed_residual <= 100 * tolerance
        and preparation_unitarity <= 100 * tolerance
        and full_unitarity <= 100 * tolerance
        and seeded_isometry <= 100 * tolerance
        and seeded_residual <= 100 * tolerance
        and extension_invariance <= 100 * tolerance
        and full_commutator <= 100 * tolerance
        and selected_block_commutator <= 100 * tolerance
        and composed_commutator <= 100 * tolerance
    )
    return FullRowCopyUnitaryControl(
        control_id=control_id,
        group_dimension=group_dimension,
        logical_dimension_per_branch=logical_dimension,
        physical_branch_count=2,
        physical_data_dimension=data_dimension,
        full_unitary_dimension=full_dimension,
        uniform_preparation_extension_distance=extension_distance,
        uniform_seed_column_residual=uniform_seed_residual,
        maximum_preparation_unitarity_residual=preparation_unitarity,
        maximum_full_row_copy_unitarity_residual=full_unitarity,
        maximum_seeded_row_copy_isometry_residual=seeded_isometry,
        seeded_row_copy_extension_invariance_residual=extension_invariance,
        maximum_full_unitary_branch_commutator_norm=full_commutator,
        maximum_selected_ancilla_block_branch_commutator_norm=selected_block_commutator,
        maximum_composed_stack_branch_commutator_norm=composed_commutator,
        every_nonprogram_ancilla_block_branch_preserving=verified,
        exact_full_row_copy_extension_scope_verified=verified,
        status=(
            "full-row-copy-unitary-all-columns-branch-preserving"
            if verified
            else "full-row-copy-unitary-scope-control-failure"
        ),
    )


def audit_endpoint_byproduct_branch_separation(
    control_id: str,
    effect: np.ndarray,
    logical_error: np.ndarray,
    *,
    tolerance: float = 1e-9,
) -> EndpointByproductBranchSeparationControl:
    """Verify the distance bound (7) for one strict canonical endpoint."""

    value = np.asarray(effect, dtype=complex)
    error = np.asarray(logical_error, dtype=complex)
    endpoint = canonical_endpoint(value, tolerance=tolerance)
    dimension = value.shape[0]
    if error.shape != (dimension, dimension):
        raise ValueError("effect and logical error dimensions must match")
    identity = np.eye(dimension, dtype=complex)
    if np.linalg.norm(error.conj().T @ error - identity, ord=2) > 1000 * tolerance:
        raise ValueError("logical error must be unitary")
    eigenvalues = np.linalg.eigvalsh((value + value.conj().T) / 2.0)
    minimum = float(eigenvalues[0])
    maximum = float(eigenvalues[-1])
    delta = min(minimum, 1.0 - maximum)
    if delta <= 100 * tolerance:
        raise ValueError("effect must lie in a strict interior window")
    byproduct = endpoint @ error @ endpoint.conj().T
    root = _psd_power(value, 0.5, tolerance=tolerance)
    complement_root = _psd_power(identity - value, 0.5, tolerance=tolerance)
    cross = root @ error @ complement_root
    singular_values = np.linalg.svd(cross, compute_uv=False)
    branch_dephased = byproduct.copy()
    branch_dephased[:dimension, dimension:] = 0.0
    branch_dephased[dimension:, :dimension] = 0.0
    distance = float(np.linalg.norm(byproduct - branch_dephased, ord=2))
    cross_norm = float(singular_values[0])
    cross_minimum = float(singular_values[-1])
    endpoint_residual = float(
        np.linalg.norm(endpoint.conj().T @ endpoint - identity, ord=2)
    )
    lower_residual = max(0.0, delta - cross_minimum)
    verified = bool(
        endpoint_residual <= 100 * tolerance
        and abs(float(np.linalg.norm(byproduct, ord=2)) - 1.0) <= 100 * tolerance
        and cross_norm + 100 * tolerance >= cross_minimum
        and cross_minimum + 100 * tolerance >= delta
        and distance + 100 * tolerance >= cross_norm
        and lower_residual <= 100 * tolerance
    )
    return EndpointByproductBranchSeparationControl(
        control_id=control_id,
        logical_dimension=dimension,
        effect_minimum_eigenvalue=minimum,
        effect_maximum_eigenvalue=maximum,
        strict_effect_window_delta=delta,
        endpoint_isometry_residual=endpoint_residual,
        byproduct_operator_norm=float(np.linalg.norm(byproduct, ord=2)),
        left_to_right_block_operator_norm=cross_norm,
        left_to_right_block_minimum_singular_value=cross_minimum,
        certified_distance_from_branch_preserving_algebra=cross_norm,
        actual_distance_to_branch_dephased_byproduct=distance,
        strict_window_lower_bound_residual=lower_residual,
        row_copy_selected_block_can_equal_byproduct=False,
        exact_branch_separation_verified=verified,
        status=(
            "endpoint-byproduct-uniformly-separated-from-branch-algebra"
            if verified
            else "endpoint-byproduct-branch-separation-control-failure"
        ),
    )


def _rotated_effect(dimension: int) -> np.ndarray:
    seed = np.arange(1, dimension * dimension + 1, dtype=float).reshape(
        dimension,
        dimension,
    )
    seed = seed + 1j * np.flipud(seed) / 7.0
    basis, _ = np.linalg.qr(seed + (dimension + 2) * np.eye(dimension))
    eigenvalues = np.linspace(0.25, 0.75, dimension)
    return (basis * eigenvalues) @ basis.conj().T


def physical_preparation_interface_inventory(
) -> list[PhysicalPreparationInterfaceRecord]:
    """Return the typed inventory distilled from the predecessor theorems."""

    return [
        PhysicalPreparationInterfaceRecord(
            primitive_id="schur-qft-coordinate-transforms",
            source_module="self_dual_wreath_schur_dilated_multiplicity_access.py",
            input_registers="physical tensor powers plus fixed Schur companions",
            output_registers="Schur labels, Specht rows, and opaque companion workspace",
            contract_type="specified-full-unitary-coordinate-change",
            full_domain_unitary_or_block_encoding_specified=True,
            branch_preserving_by_typed_interface=True,
            supplies_endpoint_program_column=False,
            supplies_addressed_cross_branch_signal=False,
            supplies_assembled_endpoint_weyl_byproduct=False,
            compiled=True,
            status="full-unitary-branch-coordinate-access-only",
        ),
        PhysicalPreparationInterfaceRecord(
            primitive_id="generalized-fourier-row-copy",
            source_module="self_dual_wreath_physical_pgm_intertwiner.py",
            input_registers="group ancilla and aligned physical orientation carrier",
            output_registers="Fourier row/column labels and physical residual carrier",
            contract_type="specified-full-unitary-with-seeded-isometry-column",
            full_domain_unitary_or_block_encoding_specified=True,
            branch_preserving_by_typed_interface=True,
            supplies_endpoint_program_column=False,
            supplies_addressed_cross_branch_signal=False,
            supplies_assembled_endpoint_weyl_byproduct=False,
            compiled=True,
            status="full-row-copy-unitary-not-endpoint-preparation",
        ),
        PhysicalPreparationInterfaceRecord(
            primitive_id="gpe-invariant-membership",
            source_module="self_dual_wreath_schur_companion_transform_scope_boundary.py",
            input_registers="supplied source label, companion carrier, and GPE workspace",
            output_registers="same branch carrier with membership phase/flag",
            contract_type="specified-reflection-and-label-control",
            full_domain_unitary_or_block_encoding_specified=True,
            branch_preserving_by_typed_interface=True,
            supplies_endpoint_program_column=False,
            supplies_addressed_cross_branch_signal=False,
            supplies_assembled_endpoint_weyl_byproduct=False,
            compiled=True,
            status="full-reflection-branch-membership-only",
        ),
        PhysicalPreparationInterfaceRecord(
            primitive_id="addressed-physical-cross-map",
            source_module="self_dual_wreath_addressed_cross_map_pair_polar_gram_boundary.py",
            input_registers="coherent source and target branch addresses plus source carrier",
            output_registers="target branch carrier and block-encoding workspace",
            contract_type="specified-normalization-one-block-encoding",
            full_domain_unitary_or_block_encoding_specified=True,
            branch_preserving_by_typed_interface=False,
            supplies_endpoint_program_column=False,
            supplies_addressed_cross_branch_signal=True,
            supplies_assembled_endpoint_weyl_byproduct=False,
            compiled=True,
            status="pair-addressed-cross-signal-available-global-assembly-open",
        ),
        PhysicalPreparationInterfaceRecord(
            primitive_id="joint-character-global-purification",
            source_module="self_dual_wreath_joint_character_purification_access_boundary.py",
            input_registers="native purification resource and coherent hidden-label twirl",
            output_registers="global-average system/environment purification",
            contract_type="normalization-one-global-density-block-encoding-from-seeded-purification",
            full_domain_unitary_or_block_encoding_specified=True,
            branch_preserving_by_typed_interface=False,
            supplies_endpoint_program_column=False,
            supplies_addressed_cross_branch_signal=False,
            supplies_assembled_endpoint_weyl_byproduct=False,
            compiled=True,
            status="global-density-access-not-final-endpoint-preparation",
        ),
        PhysicalPreparationInterfaceRecord(
            primitive_id="final-root-label-retaining-program",
            source_module="self_dual_wreath_final_root_purification_naimark_program_boundary.py",
            input_registers="none specified beyond the normalized resource state",
            output_registers="operator-state F=V sqrt(rho)",
            contract_type="algebraic-operator-state-column",
            full_domain_unitary_or_block_encoding_specified=False,
            branch_preserving_by_typed_interface=False,
            supplies_endpoint_program_column=True,
            supplies_addressed_cross_branch_signal=False,
            supplies_assembled_endpoint_weyl_byproduct=False,
            compiled=False,
            status="program-state-identity-no-full-preparation-unitary",
        ),
        PhysicalPreparationInterfaceRecord(
            primitive_id="orientation-polar-Q_R",
            source_module="self_dual_wreath_physical_pgm_intertwiner.py",
            input_registers="common logical orientation carrier",
            output_registers="stacked physical invariant branch ranges",
            contract_type="required-isometry-uncompiled",
            full_domain_unitary_or_block_encoding_specified=False,
            branch_preserving_by_typed_interface=False,
            supplies_endpoint_program_column=False,
            supplies_addressed_cross_branch_signal=True,
            supplies_assembled_endpoint_weyl_byproduct=False,
            compiled=False,
            status="decisive-orientation-polar-gate-open",
        ),
        PhysicalPreparationInterfaceRecord(
            primitive_id="endpoint-whitening-filter",
            source_module="self_dual_wreath_final_root_purification_naimark_program_boundary.py",
            input_registers="reference leg of F=V sqrt(rho)",
            output_registers="flattened endpoint program V/sqrt(D)",
            contract_type="unique-contraction-known-circuit-uncompiled",
            full_domain_unitary_or_block_encoding_specified=False,
            branch_preserving_by_typed_interface=False,
            supplies_endpoint_program_column=True,
            supplies_addressed_cross_branch_signal=False,
            supplies_assembled_endpoint_weyl_byproduct=False,
            compiled=False,
            status="inverse-metric-whitening-filter-open",
        ),
    ]


def physical_preparation_scaling_record(n: int) -> PhysicalPreparationScalingRecord:
    if n < 3:
        raise ValueError("n must be at least three")
    copy_count = math.ceil(math.log2(math.factorial(n))) + 2
    return PhysicalPreparationScalingRecord(
        n=n,
        information_threshold_copy_count=copy_count,
        permutation_register_log2_dimension=math.lgamma(n + 1) / math.log(2),
        orientation_branch_register_qubit_count=copy_count,
        generalized_row_copy_full_unitary_polynomial=True,
        generalized_row_copy_all_columns_branch_preserving=True,
        addressed_cross_map_block_encoding_normalization=1.0,
        full_endpoint_preparation_unitary_compiled=False,
        endpoint_weyl_pair_compiled=False,
        typical_natural_effect_branch_separation_proved=False,
        status="polynomial-row-copy-full-unitary-endpoint-preparation-open",
    )


def run_final_root_physical_preparation_extension_scope_boundary(
) -> PhysicalPreparationExtensionScopeReport:
    row_controls = [
        audit_full_row_copy_unitary(
            f"cyclic-g{group}-d{dimension}",
            group,
            dimension,
        )
        for group, dimension in ((2, 2), (3, 2), (3, 3), (4, 3), (5, 4))
    ]
    separation_controls: list[EndpointByproductBranchSeparationControl] = []
    for dimension in (2, 3, 4):
        effect = _rotated_effect(dimension)
        errors = weyl_unitary_error_basis(dimension)
        separation_controls.append(
            audit_endpoint_byproduct_branch_separation(
                f"shift-rotated-d{dimension}",
                effect,
                errors[dimension],
            )
        )
        separation_controls.append(
            audit_endpoint_byproduct_branch_separation(
                f"clock-rotated-d{dimension}",
                effect,
                errors[1],
            )
        )
    inventory = physical_preparation_interface_inventory()
    scaling = [
        physical_preparation_scaling_record(n)
        for n in (3, 4, 8, 16, 32, 64, 128, 256)
    ]
    row_failures = sum(
        not row.exact_full_row_copy_extension_scope_verified
        for row in row_controls
    )
    separation_failures = sum(
        not row.exact_branch_separation_verified
        for row in separation_controls
    )
    endpoint_preparation_count = sum(
        row.compiled
        and row.supplies_endpoint_program_column
        and row.full_domain_unitary_or_block_encoding_specified
        for row in inventory
    )
    addressed_cross_count = sum(
        row.compiled and row.supplies_addressed_cross_branch_signal
        for row in inventory
    )
    assembled_byproduct_count = sum(
        row.compiled and row.supplies_assembled_endpoint_weyl_byproduct
        for row in inventory
    )
    verified = bool(
        row_failures == 0
        and separation_failures == 0
        and endpoint_preparation_count == 0
        and addressed_cross_count == 1
        and assembled_byproduct_count == 0
    )
    theorem = PhysicalPreparationExtensionScopeTheorem(
        full_row_copy_unitary=(
            "W_P=(F_G^* tensor I) SELECT_s(U_s^*) (P tensor I) is a complete unitary for every declared uniform-state extension P; its zero-ancilla column is the generalized Fourier row-copy isometry."
        ),
        all_column_closure=(
            "Because U_s is a direct sum over orientation branches, W_P and every selected ancilla block commute with every branch projector, independently of all nonzero columns of P."
        ),
        endpoint_byproduct_separation=(
            "For delta I<=C<=(1-delta)I, the cross block sqrt(C)U sqrt(I-C) has sigma_min>=delta, so V_C U V_C^* is operator-norm distance at least delta from every branch-preserving operator."
        ),
        interface_inventory=(
            "The compiled stack contains full Schur/QFT/GPE and row-copy unitaries plus pair-addressed cross-map block encodings, but no compiled full-domain A_V preparing the final endpoint program. The program F and whitening filter are resource/algebraic interfaces."
        ),
        addressed_cross_map_exception=(
            "The physical detour supplies J_f^*J_e at normalization one and its pair polar, so cross-branch access is not absent; it is pair addressed and has not been assembled into the endpoint Weyl pair or global merger polar."
        ),
        surviving_route=(
            "Construct V_C X V_C^* and V_C Z V_C^* directly from normalization-one addressed cross maps and positive child metrics, or compile Q_R; do not search unspecified row-copy ancilla columns."
        ),
        scope=(
            "This types the existing physical circuit family and proves its branch-algebra closure. It does not rule out a new cross-branch circuit, assign typical natural mass to the strict effect window, or implement the physical PGM."
        ),
        theorem_verified=verified,
        status=(
            "full-row-copy-extension-branch-preserving-endpoint-preparation-absent"
            if verified
            else "physical-preparation-extension-scope-control-failure"
        ),
    )
    return PhysicalPreparationExtensionScopeReport(
        created_at=utc_now(),
        theorem_contract={
            "hypothesis": (
                "The actual label-retaining Schur/QFT/GPE endpoint preparation is already a fully specified unitary whose non-program columns may contain a constant-normalization block of V_C X V_C^* or V_C Z V_C^*."
            ),
            "typed_access_model": (
                "Full group-ancilla generalized row-copy unitaries, companion-only Schur/QFT/GPE coordinate and membership operations with workspace, the normalization-one addressed physical cross-map block encoding, and the separately stated purification/final-root resource interfaces."
            ),
            "positive_result": (
                "The generalized row-copy circuit is a complete polynomial unitary for every chosen uniform-preparation extension, and addressed cross-branch maps J_f^*J_e are available at normalization one."
            ),
            "negative_boundary": (
                "Every row-copy ancilla block is branch preserving and uniformly separated from strict-window endpoint Weyl byproducts. No compiled full-domain endpoint preparation A_V exists in the current stack."
            ),
            "claim_boundary": (
                "New circuits assembled from addressed cross maps or a compiled Q_R remain outside the branch-preserving row-copy closure and are not ruled out."
            ),
        },
        theorem=theorem,
        row_copy_controls=row_controls,
        byproduct_separation_controls=separation_controls,
        interface_inventory=inventory,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "write_complete_generalized_row_copy_unitary",
                "resolved": True,
                "evidence": "Equation (2) is a product of a declared full uniform-preparation unitary, branch-diagonal controlled representation actions, and the full inverse group Fourier transform.",
            },
            {
                "obligation": "audit_all_nonprogram_row_copy_columns",
                "resolved": True,
                "evidence": "The full unitary commutes with every branch projector, so every ancilla matrix element and every composition with the known branch workspace algebra does too.",
            },
            {
                "obligation": "separate_branch_algebra_from_endpoint_weyl_byproducts",
                "resolved": True,
                "evidence": "The left-to-right target block is sqrt(C)U sqrt(I-C), whose minimum singular value is at least delta on the strict effect window; compression lower-bounds distance from all branch-preserving operators.",
            },
            {
                "obligation": "locate_compiled_full_endpoint_preparation_unitary",
                "resolved": True,
                "evidence": "The typed inventory finds none: row-copy is not Q_R, the final-root program is an operator-state resource, the unique whitening filter is uncompiled, and the physical PGM theorem explicitly leaves Q_R open.",
            },
            {
                "obligation": "assemble_endpoint_weyl_pair_from_addressed_cross_maps",
                "resolved": False,
                "evidence": "Normalization-one J_f^*J_e queries and pair polars exist, but no coherent positive-metric assembly realizes the four endpoint byproduct blocks."
            },
            {
                "obligation": "prove_strict_effect_window_on_typical_natural_mass",
                "resolved": False,
                "evidence": "Finite strict-window separation controls are access witnesses; no typical free-Jacobi spectral-edge event is imported or claimed."
            },
        ],
        adversarial_audit=[
            {
                "objection": "Only the row-copy zero column is branch preserving; other columns of its uniform preparation may mix branches.",
                "resolved": True,
                "resolution": "Ancilla preparation acts as P tensor I and therefore commutes with every data-branch projector on every input column. Two inequivalent P extensions verify the distinction explicitly."
            },
            {
                "objection": "A selected ancilla top block can leave the branch algebra even if the full unitary commutes with branch projectors.",
                "resolved": True,
                "resolution": "Taking an ancilla matrix element preserves the commutator identity exactly; all group input/output blocks remain branch diagonal."
            },
            {
                "objection": "The generalized Fourier row-copy is the missing endpoint polar Q_R.",
                "resolved": True,
                "resolution": "The physical PGM intertwiner theorem factors the PGM as Q_R^* C_U and explicitly marks Q_R uncompiled; C_U is the row-copy unitary column audited here."
            },
            {
                "objection": "No physical cross-branch primitive is known.",
                "resolved": True,
                "resolution": "Too strong. The addressed physical-interface/projector sandwich block-encodes each J_f^*J_e at alpha one and GPE compiles its pair polar."
            },
            {
                "objection": "Pair-addressed cross maps already constitute a full endpoint preparation unitary.",
                "resolved": True,
                "resolution": "They are coherent signal blocks indexed by e,f. Their positive global metric assembly, inverse-square-root merger, and endpoint Weyl combination remain separate operations."
            },
            {
                "objection": "The finite strict effect window proves typical natural byproduct separation.",
                "resolved": False,
                "resolution": "It does not. The theorem is exact for endpoints satisfying the stated delta window; typical spectral-edge control remains open."
            },
        ],
        primary_literature=[
            {
                "paper_id": BEALS_PAPER_ID,
                "url": BEALS_PAPER_URL,
                "scope": "Full polynomial S_n Fourier coordinate transform used in the row-copy circuit; it is not an orientation polar."
            },
            {
                "paper_id": BCH_PAPER_ID,
                "url": BCH_PAPER_URL,
                "scope": "Full Schur/GPE label and invariant-projection interfaces; their typed action does not supply the missing cross-branch endpoint operation."
            },
        ],
        headline_metrics={
            "full_generalized_row_copy_unitary_theorem_count": int(verified),
            "all_row_copy_columns_branch_preserving_theorem_count": int(verified),
            "strict_window_endpoint_byproduct_separation_theorem_count": int(verified),
            "typed_interface_inventory_count": len(inventory),
            "row_copy_control_count": len(row_controls),
            "row_copy_control_failure_count": row_failures,
            "byproduct_separation_control_count": len(separation_controls),
            "byproduct_separation_control_failure_count": separation_failures,
            "compiled_full_endpoint_preparation_unitary_count": endpoint_preparation_count,
            "compiled_addressed_cross_branch_signal_count": addressed_cross_count,
            "compiled_assembled_endpoint_weyl_byproduct_count": assembled_byproduct_count,
            "physical_pgm_circuit_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "complete_full_domain_generalized_row_copy_unitary_typed": verified,
            "every_row_copy_nonprogram_ancilla_block_branch_preserving": verified,
            "strict_window_endpoint_weyl_byproduct_outside_branch_algebra": verified,
            "row_copy_nonprogram_columns_supply_endpoint_weyl_byproduct": False,
            "joint_purification_is_full_endpoint_preparation_unitary": False,
            "compiled_full_domain_endpoint_preparation_A_V_exists": False,
            "addressed_cross_map_signal_normalization_one_available": True,
            "addressed_cross_maps_assembled_into_endpoint_weyl_pair": False,
            "orientation_polar_Q_R_compiled": False,
            "typical_natural_effect_branch_separation_proved": False,
            "physical_pgm_circuit_proved": False,
            "hidden_involution_decoder_proved": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The only complete physical preparation-like unitary is row-copy, and its full ancilla extension is branch preserving. The endpoint program and Q_R are not compiled full-domain unitaries. Available addressed cross maps must still be assembled into the endpoint byproduct or merger polar."
            ),
        },
        status=theorem.status,
        summary=(
            "Typed the complete physical row-copy unitary and proved all of its ancilla blocks remain branch preserving, then showed strict-window endpoint Weyl byproducts are uniformly outside that algebra and that the current stack contains no compiled full endpoint preparation A_V."
        ),
        falsifiers_triggered=[
            "The generalized Fourier row-copy has a full unitary extension, but it is not the endpoint-program preparation and all of its columns remain branch preserving.",
            "Changing the uniform-state preparation extension cannot hide a cross-branch endpoint byproduct in nonzero ancilla columns.",
            "Assuming a full A_V for the final endpoint would assume the missing whitening/orientation polar rather than exploit an already compiled circuit.",
            "The claim that no cross-branch primitive exists is false: addressed J_f^*J_e blocks and pair polars are available at normalization one.",
            "Those pair-addressed primitives have not yet been assembled into V_C X V_C^*, V_C Z V_C^*, or the physical PGM."
        ],
    )


def write_final_root_physical_preparation_extension_scope_boundary_report(
    path: Path = REPORT_PATH,
    *,
    write_registry: bool = True,
) -> dict[str, Any]:
    payload = asdict(run_final_root_physical_preparation_extension_scope_boundary())
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
                title="Final-root physical preparation extension scope boundary",
                status="completed-typed-interface-boundary-theorem",
                hypothesis=payload["theorem_contract"]["hypothesis"],
                protocol=(
                    "Write the complete group-ancilla row-copy unitary, audit every ancilla block under inequivalent uniform-state extensions, prove strict-window endpoint Weyl separation from the branch algebra, and inventory all compiled versus resource-only physical preparation interfaces."
                ),
                positive_signal=(
                    "An explicit polynomial assembly of V_C X V_C^* and V_C Z V_C^* from the available normalization-one addressed J_f^*J_e block encodings and positive child metrics, or a direct compiler for Q_R."
                ),
                falsifiers=payload["falsifiers_triggered"],
                metrics=list(payload["headline_metrics"].keys()),
                dependencies=[
                    "self_dual_wreath_physical_pgm_intertwiner.py",
                    "self_dual_wreath_schur_companion_transform_scope_boundary.py",
                    "self_dual_wreath_addressed_cross_map_pair_polar_gram_boundary.py",
                    "self_dual_wreath_joint_character_purification_access_boundary.py",
                    "self_dual_wreath_final_root_state_preparation_oracle_query_boundary.py",
                ],
                next_actions=[
                    "Derive the final two-child endpoint Weyl four-block formula directly in the addressed cross-map oracle language and decide whether O(1) positive-metric queries suffice, before invoking any dense global address assembly."
                ],
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id=NEGATIVE_RESULT_ID,
                source=str(path),
                claim=(
                    "The actual compiled generalized-Fourier row-copy or Schur/QFT/GPE preparation stack is a full endpoint preparation whose non-program columns may already expose V_C X V_C^* and V_C Z V_C^*."
                ),
                reason_invalid=(
                    "The complete row-copy unitary commutes with every orientation-branch projector for every uniform-preparation extension, so all selected ancilla blocks are branch preserving. Strict-window endpoint Weyl byproducts have a cross block with minimum singular value at least delta. The endpoint program, whitening filter, and Q_R are not compiled full-domain unitaries in the current stack."
                ),
                lesson=(
                    "Do not mine unspecified columns of a nonexistent endpoint-preparation circuit. Use the genuinely available normalization-one addressed cross-map signals to construct the endpoint Weyl blocks, or compile Q_R explicitly."
                ),
                applies_to=[
                    DEFAULT_CANDIDATE_ID,
                    "PO-MECHANISM",
                    "PO-MEASUREMENT",
                    "PO-COMPLEXITY",
                ],
                evidence={
                    "full_row_copy_unitary": "(F_G^* tensor I) SELECT_s(U_s^*) (P tensor I)",
                    "all_ancilla_blocks_branch_preserving": True,
                    "strict_window_target_distance_lower_bound": "delta",
                    "compiled_full_endpoint_preparation_A_V": False,
                    "addressed_cross_map_normalization": 1.0,
                    "assembled_endpoint_weyl_pair": False,
                    "typical_natural_effect_window_proved": False,
                    "speedup_claim_allowed": False,
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_final_root_physical_preparation_extension_scope_boundary_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
