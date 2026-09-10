"""Finite checks and uniform access contracts for clean isotypic instruments.

Dense matrices here verify the compute/label-copy/uncompute reduction; they
are not the implementation of a growing-rank symmetric-group QFT.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Hashable, Mapping, Sequence

import numpy as np


@dataclass(frozen=True)
class IsotypicInstrument:
    labels: tuple[Hashable, ...]
    projectors: Mapping[Hashable, np.ndarray]
    fourier_kraus: Mapping[Hashable, tuple[np.ndarray, ...]]
    residuals: Mapping[str, float]
    group_order: int
    dimension: int

    def clean_label(self, label: Hashable, matrix: np.ndarray) -> np.ndarray:
        projector = self.projectors[label]
        return projector @ matrix @ projector.conj().T

    def discard_reference(self, label: Hashable, matrix: np.ndarray) -> np.ndarray:
        return sum((a @ matrix @ a.conj().T for a in self.fourier_kraus[label]),
                   np.zeros((self.dimension, self.dimension), dtype=complex))


def finite_isotypic_instrument(
    actions: Sequence[np.ndarray],
    irreps: Mapping[Hashable, Sequence[np.ndarray]],
    *, tolerance: float = 1e-9,
) -> IsotypicInstrument:
    """Build GPE Kraus operators with one common enumeration of group elements.

    A_(lambda,i,j) = sqrt(d_lambda)/|G| sum_g conj(rho_lambda(g)_ij) U_g.
    Clean uncomputation is certified by Pi_lambda V = V P_lambda, not by
    postselecting an accidentally nonzero clean-workspace amplitude.
    """
    if not math.isfinite(tolerance) or not 0 < tolerance <= 1e-6:
        raise ValueError("a positive finite numerical tolerance <= 1e-6 is required")
    values = np.asarray(actions, dtype=complex)
    if (values.ndim != 3 or values.shape[0] == 0 or values.shape[1] == 0
            or values.shape[1] != values.shape[2] or not np.isfinite(values).all()):
        raise ValueError("finite square action matrices are required")
    order, dimension, _ = values.shape
    identity = np.eye(dimension)
    unitarity = max(float(np.linalg.norm(u.conj().T @ u - identity)) for u in values)
    rows, slices, characters = [], {}, {}
    for label, matrices in irreps.items():
        rep = np.asarray(matrices, dtype=complex)
        if (rep.ndim != 3 or rep.shape[0] != order or rep.shape[1] == 0
                or rep.shape[1] != rep.shape[2] or not np.isfinite(rep).all()):
            raise ValueError("each irrep must use the same group enumeration and square matrices")
        width = rep.shape[1]
        start = len(rows)
        rows.extend(math.sqrt(width / order) * rep[:, i, j].conjugate()
                    for i in range(width) for j in range(width))
        slices[label] = slice(start, len(rows))
        characters[label] = width / order * np.einsum("g,gab->ab", np.trace(rep, axis1=1, axis2=2).conjugate(), values)
    fourier = np.asarray(rows)
    if fourier.shape != (order, order):
        raise ValueError("complete irreps with sum of squared dimensions equal to |G| are required")
    fourier_residual = float(np.linalg.norm(fourier @ fourier.conj().T - np.eye(order)))
    all_kraus = np.einsum("ag,gij->aij", fourier, values) / math.sqrt(order)
    isometry = all_kraus.reshape(order * dimension, dimension)
    projectors, kraus = {}, {}
    projection_residual = 0.0
    clean_workspace_residual = 0.0
    character_residual = 0.0
    for label, selection in slices.items():
        branch_kraus = all_kraus[selection]
        projector = sum((a.conj().T @ a for a in branch_kraus), np.zeros_like(identity, dtype=complex))
        projection_residual = max(projection_residual, float(np.linalg.norm(projector @ projector - projector)))
        character_residual = max(character_residual, float(np.linalg.norm(projector - characters[label])))
        selected_isometry = np.zeros_like(all_kraus)
        selected_isometry[selection] = branch_kraus
        clean_workspace_residual = max(clean_workspace_residual,
            float(np.linalg.norm(selected_isometry.reshape(order * dimension, dimension) - isometry @ projector)))
        projector.setflags(write=False)
        branch_kraus.setflags(write=False)
        projectors[label], kraus[label] = projector, tuple(branch_kraus)
    residuals = {
        "action_unitarity": unitarity,
        "fourier_unitarity": fourier_residual,
        "gpe_isometry": float(np.linalg.norm(isometry.conj().T @ isometry - identity)),
        "projector_idempotence": projection_residual,
        "character_projector_identity": character_residual,
        "clean_workspace_intertwining": clean_workspace_residual,
        "projector_completeness": float(np.linalg.norm(sum(projectors.values()) - identity)),
    }
    if max(residuals.values()) > tolerance:
        raise ValueError(f"incompatible representation/Fourier contract: {residuals}")
    return IsotypicInstrument(tuple(irreps), projectors, kraus, residuals, order, dimension)


def isotypic_label_resource_contract(
    degree: int, subset_copy_count: int, label_queries: int = 1,
    forward_gpe_operator_error: float = 0.0,
) -> dict:
    """Uniform reduction to supplied S_n QFT and controlled known group actions.

    Each clean query uses W, label copy, W^dagger. If ||Wtilde-W||<=delta,
    its channel error is <=4 delta; q adaptive uses accumulate <=4q delta.
    """
    if (type(degree) is not int or degree < 2 or type(subset_copy_count) is not int
            or subset_copy_count < 1 or type(label_queries) is not int or label_queries < 0):
        raise ValueError("degree >=2, positive subset width and nonnegative query count required")
    if not math.isfinite(forward_gpe_operator_error) or forward_gpe_operator_error < 0:
        raise ValueError("finite nonnegative operator error required")
    return {
        "program": ["PREPARE_UNIFORM_SN", "CONTROLLED_SUBSET_GROUP_ACTION", "SN_QFT",
                    "COPY_IRREP_LABEL_ONLY", "SN_QFT_INVERSE", "CONTROLLED_SUBSET_GROUP_ACTION_INVERSE",
                    "UNPREPARE_UNIFORM_SN"],
        "degree": degree,
        "subset_copy_count": subset_copy_count,
        "label_queries": label_queries,
        "group_qft_or_inverse_calls": 2 * label_queries,
        "uniform_preparation_or_inverse_calls": 2 * label_queries,
        "controlled_single_copy_group_action_or_inverse_calls": 2 * subset_copy_count * label_queries,
        "reference_register_qubits": (math.factorial(degree) - 1).bit_length(),
        "partition_label_register_bits_upper_bound": degree * degree.bit_length(),
        "composed_channel_diamond_distance_upper_bound": min(2.0, 4 * label_queries * forward_gpe_operator_error),
        "postselection_required": False,
        "inverse_is_adjoint_of_same_approximate_circuit": True,
        "clean_workspace_required": True,
        "multiplicity_basis_transform_supplied": False,
        "gate_level_sn_qft_backend_supplied_here": False,
        "uniform_reduction_to_known_primitives": True,
        "controlled_representation_access_must_be_charged": True,
        "scope": "S_n physical regular registers or efficient supplied irrep actions; subset may grow polynomially. No hard multiplicity transform is granted.",
    }
