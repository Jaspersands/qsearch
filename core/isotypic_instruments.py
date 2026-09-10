"""Finite checks and uniform access contracts for clean isotypic instruments.

Dense matrices here verify the compute/label-copy/uncompute reduction; they
are not the implementation of a growing-rank symmetric-group QFT.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction
from typing import Hashable, Mapping, Sequence

import numpy as np


def subset_incidence_cells(copy_count: int, subsets: Sequence[Sequence[int]], *, individual_source_labels: bool = False) -> tuple[tuple[int, ...], ...]:
    """Nonzero membership signatures; untouched copies have no allowed readout.

    Observing individual source labels refines the cells to singletons. This
    is a structural contract, not an automatic audit of an arbitrary circuit.
    """
    if type(copy_count) is not int or copy_count < 1:
        raise ValueError("positive integer copy_count required")
    if type(individual_source_labels) is not bool:
        raise ValueError("individual_source_labels must be an explicit boolean")
    signatures = [0] * copy_count
    for bit, subset in enumerate(subsets):
        seen = set()
        for index in subset:
            if type(index) is not int or not 0 <= index < copy_count or index in seen:
                raise ValueError("subsets require distinct in-range integer copy indices")
            signatures[index] |= 1 << bit
            seen.add(index)
    if individual_source_labels:
        return tuple((index,) for index in range(copy_count))
    cells = {}
    for index, signature in enumerate(signatures):
        if signature:
            cells.setdefault(signature, []).append(index)
    return tuple(tuple(cell) for _, cell in sorted(cells.items()))


def fixed_palette_information_contract(class_size: int, copy_count: int, subsets: Sequence[Sequence[int]], *,
        individual_source_labels: bool = False, operations_and_readout_in_palette_algebra: bool) -> dict:
    """Compression applies to a fixed palette, including arbitrary repetitions.

    Every Kraus operator and readout effect must lie in the cellwise diagonal
    group algebra (with ancilla coefficients). Arbitrary unlisted subsets,
    individual source labels and nonalgebra data readouts must not be hidden.
    """
    if type(class_size) is not int or class_size < 1:
        raise ValueError("positive integer class size required")
    if type(operations_and_readout_in_palette_algebra) is not bool:
        raise ValueError("operations_and_readout_in_palette_algebra must be an explicit boolean")
    cells = subset_incidence_cells(copy_count, subsets, individual_source_labels=individual_source_labels)
    count = len(cells)
    bound = (Fraction(1) if count >= (4 * class_size).bit_length()
             else min(Fraction(1), Fraction((1 << count) - 1, 4 * class_size)))
    return {
        "raw_copy_count": copy_count, "listed_subset_count": len(subsets),
        "effective_cell_count": count, "individual_source_labels_retained": individual_source_labels,
        "applicable": bool(operations_and_readout_in_palette_algebra),
        "trace_distance_squared_upper_bound": str(bound) if operations_and_readout_in_palette_algebra else None,
        "exact_output_simulation_by_cell_count_coset_copies": bool(operations_and_readout_in_palette_algebra),
        "assumption_contract_not_arbitrary_program_verifier": True,
        "is_classical_dequantization": False,
        "scope": "Fixed listed subset palette, including adaptive repetitions within it; all instruments and final readouts in its cellwise diagonal group algebra. Ancillas are allowed. Unlisted/coherently addressed subsets require refining the palette; individual source labels split all cells.",
    }


def regular_algebra_state_lift(moments: Sequence[complex], regular_actions: Sequence[np.ndarray]) -> np.ndarray:
    """Canonical finite density for a positive group-algebra functional.

    The caller supplies one regular representation in a common enumeration.
    This checks its orthogonal matrix basis and the resulting state/moments,
    not an efficient physical conversion or the entire group multiplication law.
    """
    values, actions = np.asarray(moments, dtype=complex), np.asarray(regular_actions, dtype=complex)
    order = len(values) if values.ndim == 1 else 0
    if (not order or actions.shape != (order, order, order)
            or not np.isfinite(values).all() or not np.isfinite(actions).all()):
        raise ValueError("finite moments and matching regular matrices required")
    gram = np.einsum("gij,hij->gh", actions.conjugate(), actions)
    if np.linalg.norm(gram - order * np.eye(order)) > 1e-8:
        raise ValueError("regular actions must form the normalized orthogonal algebra basis")
    state = np.einsum("g,gji->ij", values, actions.conjugate()) / order
    residual = max(float(np.linalg.norm(state - state.conj().T)),
                   float(abs(np.trace(state) - 1)),
                   float(np.max(np.abs(np.einsum("ij,gji->g", state, actions) - values))))
    if residual > 1e-8 or np.linalg.eigvalsh((state + state.conj().T) / 2).min() < -1e-8:
        raise ValueError("moments do not define a normalized positive algebra state")
    return state


def _sqrt_ratio_dyadic_exponent(numerator: int, denominator: int) -> int | None:
    """Exact b with min(1,sqrt(numerator/denominator)) <= 2**b; None means zero."""
    if type(numerator) is not int or numerator < 0 or type(denominator) is not int or denominator < 1:
        raise ValueError("nonnegative integer numerator and positive denominator required")
    if not numerator:
        return None
    exponent = numerator.bit_length() - denominator.bit_length()
    if (numerator > denominator << exponent if exponent >= 0 else numerator << -exponent > denominator):
        exponent += 1
    return min(0, (exponent + 1) // 2)


def source_conditioned_palette_information_contract(
    degree: int, copy_count: int, subsets: Sequence[Sequence[int]], *,
    palette_fixed_before_source_labels: bool, operations_and_readout_in_cell_algebra: bool,
    retain_cells_below: int = 0,
) -> dict:
    """Review-pending S_n bound, with every classical source label retained.

    Uses L=n for n>=5 and M=(n-1)!!>=8n for even n>=8, hence t<=min(1,9/n).
    Individual quantum operations/readouts and label-selected palettes are NOT
    covered. Dyadic upper bounds use integer arithmetic, never float underflow.
    """
    if type(degree) is not int or degree < 8 or degree % 2:
        raise ValueError("even symmetric-group degree >=8 required")
    if any(type(flag) is not bool for flag in (palette_fixed_before_source_labels, operations_and_readout_in_cell_algebra)):
        raise ValueError("explicit boolean access assumptions required")
    if type(retain_cells_below) is not int or retain_cells_below < 0:
        raise ValueError("nonnegative integer cell-retention threshold required")
    cells = subset_incidence_cells(copy_count, subsets)
    retained = [cell for cell in cells if len(cell) < retain_cells_below]
    compressed = [cell for cell in cells if len(cell) >= retain_cells_below]
    order = math.factorial(degree)
    class_size = order // (2**(degree // 2) * math.factorial(degree // 2))
    count = len(cells)
    effective_copies = sum(map(len, retained)) + len(compressed)
    applicable = palette_fixed_before_source_labels and operations_and_readout_in_cell_algebra
    components = []
    if applicable:
        components = [
            {"term": "source_label_prior", "upper_bound_power_of_two": _sqrt_ratio_dyadic_exponent(copy_count**2, 4 * class_size)},
            {"term": "shared_hidden_cell_state", "upper_bound_power_of_two": _sqrt_ratio_dyadic_exponent((1 << effective_copies) - 1, 4 * class_size)},
        ]
        for size in sorted(set(map(len, compressed))):
            multiplicity = sum(len(cell) == size for cell in compressed)
            denominator = 4 * degree**size
            components.extend([
                {"term": "null_cell_error", "cell_width": size, "multiplicity": multiplicity,
                 "upper_bound_power_of_two": _sqrt_ratio_dyadic_exponent(order - 1, denominator)},
                {"term": "alternative_cell_error", "cell_width": size, "multiplicity": multiplicity,
                 "upper_bound_power_of_two": _sqrt_ratio_dyadic_exponent((order - 2) * 9**size, denominator)},
            ])
    nonzero = [row for row in components if row["upper_bound_power_of_two"] is not None]
    term_count = sum(row.get("multiplicity", 1) for row in nonzero)
    exponent = (min(0, max(row["upper_bound_power_of_two"] for row in nonzero) + (term_count - 1).bit_length())
                if nonzero else None)
    return {
        "degree": degree, "raw_copy_count": copy_count, "listed_subset_count": len(subsets),
        "effective_cell_count": count, "cell_widths": list(map(len, cells)),
        "effective_coset_copy_count": effective_copies,
        "retained_cell_widths": list(map(len, retained)),
        "compressed_cell_widths": list(map(len, compressed)),
        "retain_cells_below": retain_cells_below,
        "source_labels_retained": copy_count, "untouched_copies": copy_count - sum(map(len, cells)),
        "minimum_nonidentity_class_size_lower_bound": degree,
        "alternative_moment_second_power_upper_bound": str(min(Fraction(1), Fraction(9, degree))),
        "palette_fixed_before_source_labels": palette_fixed_before_source_labels,
        "operations_and_readout_in_cell_algebra": operations_and_readout_in_cell_algebra,
        "applicable": applicable,
        "trace_distance_upper_bound_power_of_two": exponent,
        "bound_is_vacuous": exponent == 0 if applicable else None,
        "bound_components": components,
        "bound_arithmetic": "exact integer outward dyadic rounding; T <= 2**exponent, exponent 0 is vacuous",
        "proof_status": "derived-source-conditioned-bound-review-pending",
        "exact_coset_copy_compression": False,
        "efficient_physical_lift_supplied": False,
        "is_classical_dequantization": False,
        "novelty_established": False,
        "assumption_contract_not_arbitrary_program_verifier": True,
        "scope": "Standard mixed coset inputs and a uniform fixed-point-free involution prior. All classical source labels are retained. Fixed incidence cells are chosen before the labels; subsequent source-controlled operations and final readouts must remain in the cellwise diagonal group algebra. Small cells may be retained as FULL quantum inputs in the upper-bound comparison, charged by their raw copy count. No independent hidden member per cell, source-dependent regrouping or uncharged individual quantum readout is granted.",
    }


def adaptive_palette_catalogue_information_contract(
    degree: int, copy_count: int, palettes: Sequence[Sequence[Sequence[int]]], *,
    catalogue_fixed_before_input: bool, complete_execution_covered: bool,
    support_choices_classically_observed: bool, operators_and_readout_respect_cover: bool,
    retain_cells_below: int = 0,
) -> dict:
    """Abort BEFORE leaving each fixed palette; sum unnormalized output bounds.

    The complete classical transcript is assigned to one covering palette.
    Selecting/conditioning a normalized branch, coherently selecting supports,
    or covering each operation separately is not this access contract.
    """
    flags = (catalogue_fixed_before_input, complete_execution_covered,
             support_choices_classically_observed, operators_and_readout_respect_cover)
    if any(type(flag) is not bool for flag in flags):
        raise ValueError("explicit boolean catalogue assumptions required")
    if len(palettes) == 0:
        raise ValueError("a nonempty predetermined palette catalogue is required")
    fixed = [source_conditioned_palette_information_contract(degree, copy_count, palette,
        palette_fixed_before_source_labels=True, operations_and_readout_in_cell_algebra=True,
        retain_cells_below=retain_cells_below) for palette in palettes]
    applicable = all(flags)
    exponents = [row["trace_distance_upper_bound_power_of_two"] for row in fixed]
    exponent = min(0, max(exponents) + (len(exponents) - 1).bit_length()) if applicable else None
    return {
        "degree": degree, "raw_copy_count": copy_count, "catalogue_size": len(palettes),
        "catalogue_fixed_before_input": catalogue_fixed_before_input,
        "complete_execution_covered": complete_execution_covered,
        "support_choices_classically_observed": support_choices_classically_observed,
        "operators_and_readout_respect_cover": operators_and_readout_respect_cover,
        "fixed_palette_bounds": fixed, "applicable": applicable,
        "trace_distance_upper_bound_power_of_two": exponent,
        "bound_is_vacuous": exponent == 0 if applicable else None,
        "aggregation": "T <= min(1,sum_j delta_j); outward dyadic max-plus-log-count upper bound",
        "source_and_transcript_adaptive_selection_covered": applicable,
        "abort_before_first_outside_operation_required": True,
        "normalized_postselected_branches_used": False,
        "catalogue_size_is_runtime_lower_bound": False,
        "coherent_support_selection_covered": False,
        "assumption_contract_not_arbitrary_program_verifier": True,
        "proof_status": "derived-aborting-catalogue-cover-review-pending",
        "novelty_established": False, "is_classical_dequantization": False,
        "scope": "Every entire execution, including its final readout, lies in at least one predeclared fixed-palette algebra. Selection may depend on initial source labels and later classical outcomes. Each comparison program aborts before leaving its palette, and successful transcript sectors are never renormalized. A catalogue covering individual steps but no whole execution is insufficient. Polynomial description length may describe exponentially many palettes; catalogue size is not selector runtime.",
    }


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
