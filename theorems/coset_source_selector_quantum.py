"""Finite quantum-selector mixture checks; no optimal POVM compiler."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from functools import lru_cache
import itertools
import math

import numpy as np

from isotypic_instruments import source_selector_quantum_information_contract, source_selector_polynomial_budget_contract


def _half_trace_norm(matrix: np.ndarray) -> float:
    return float(np.linalg.svd(matrix, compute_uv=False).sum()/2)


def _prepend_tensor(current: np.ndarray, local: np.ndarray) -> np.ndarray:
    # Source i controls the little-endian bit 2**i in the existing mask schema.
    result = np.einsum("pab,pcd->pcadb", current, local)
    dimension = current.shape[1]*2
    return result.reshape(len(current), dimension, dimension)


def _typical_mask_kernel_decomposition(kernels: np.ndarray, subgroup: np.ndarray, products: np.ndarray):
    count, order = len(kernels), len(subgroup)
    local = kernels.reshape(count, order, order, 2, 2)
    base = np.zeros_like(local)
    base[:, :, :, 0, 0] = local[:, :, :, 0, 0]
    # On an endpoint pair the dominant factor pins only one side to |0>.
    base[:, subgroup, :, 0, 1] = local[:, subgroup, :, 0, 0]
    base[:, :, subgroup, 1, 0] = local[:, :, subgroup, 0, 0]
    base = base.reshape(kernels.shape)
    remainder = kernels-base
    b = np.linalg.svd(base, compute_uv=False).sum(axis=-1).sum(axis=0)
    epsilon = np.linalg.svd(remainder, compute_uv=False).sum(axis=-1).sum(axis=0)
    off_coset = ~subgroup[products].reshape(-1)
    return base, remainder, b, epsilon, off_coset


def _typical_mask_tensor_tail(base_radius, remainder_radius, copies: int, minimum_weight: int):
    return sum(math.comb(copies, d)*base_radius**(copies-d)*remainder_radius**d
               for d in range(minimum_weight, copies+1))


@lru_cache(maxsize=21, typed=True)
def source_selector_quantum_mixture_control(n: int, transposition_count: int, copies: int, phase_rule: str) -> dict:
    from coset_binary_carrier_instruments import (
        _source_parity_group_data, _coherent_phase_values, _conditional_selector_kernel,
        evaluate_coherent_subset_phase_query,
    )
    if (type(n) is not int or type(transposition_count) is not int or (n, transposition_count) not in ((3, 1), (4, 2))
            or type(copies) is not int or not 1 <= copies <= (4 if n == 3 else 3)):
        raise ValueError("quantum-selector controls require S3 copies 1..4 or S4 copies 1..3")
    data = _source_parity_group_data(n, transposition_count)
    order, partitions = len(data[0]), data[1]
    phases = _coherent_phase_values(partitions, transposition_count, phase_rule)
    coefficients = (data[3]*np.array([phases[lam] for lam in partitions])) @ data[2] / order
    outer = np.outer(coefficients.conjugate(), coefficients).reshape(-1)
    projectors = data[3][:, None]*data[2]/order
    translated = data[8][0]
    p_values = (projectors, projectors+projectors[:, translated])
    size = 2**copies
    masks = tuple(range(size))
    walsh = np.array([[(-1)**((s&t).bit_count()) for t in masks] for s in masks])/math.sqrt(size)
    kernels, diagonals, mixture_locals, mixture_weights, tails = [], [], [], [], []
    radius_records = []
    for b, values in enumerate(p_values):
        local, positive = [], []
        for p in values:
            kernel = np.zeros((order, order, 2, 2))
            kernel[:, :, 0, 0] = p[0]/2
            kernel[:, :, 0, 1] = p[data[6], None]/2
            kernel[:, :, 1, 0] = p[None, :]/2
            kernel[:, :, 1, 1] = p[data[7]]/2
            local.append(kernel.reshape(order**2, 2, 2))
            positive.append(np.array([[np.full(order, p[0]), p], [p, np.full(order, p[0])]]).transpose(2, 0, 1)/2)
        local = np.asarray(local)
        radius = np.linalg.svd(local, compute_uv=False).sum(axis=-1).sum(axis=0)
        subgroup = np.zeros(order, dtype=bool)
        subgroup[0] = True
        if b:
            subgroup[translated[0]] = True
        diagonal = subgroup[data[7]].reshape(-1)
        exceptional = ((subgroup[:, None] | subgroup[None, :]).reshape(-1)) & ~diagonal
        if radius.max() > 1+1e-12:
            raise ArithmeticError("source-resolved quantum kernel exceeded its unit trace-norm radius")
        amplitude = coefficients if not b else coefficients+coefficients[translated]
        weights = np.abs(amplitude)**2/(b+1)
        if abs(weights.sum()-1) > 1e-12 or np.linalg.eigvalsh(np.asarray(positive)).min() < -1e-12:
            raise ArithmeticError("quantum coset-diagonal mixture is not positive and normalized")
        kernels.append(local)
        diagonals.append(diagonal)
        mixture_locals.append(np.asarray(positive))
        mixture_weights.append(weights)
        tails.append(float(np.dot(np.abs(outer[~diagonal]), radius[~diagonal]**copies)/2))
        radius_records.append({"hypothesis": "alternative" if b else "null",
            "maximum_off_coset_trace_norm_radius": float(radius[~diagonal].max()),
            "minimum_endpoint_trace_norm_radius": float(radius[exceptional].min()),
            "maximum_endpoint_trace_norm_radius": float(radius[exceptional].max()),
            "walsh_endpoint_half_radius_is_valid_here": bool(radius[exceptional].max() <= .5+1e-12)})
    residuals = dict.fromkeys(("conditional_matrix", "positive_diagonal_mixture", "hermiticity", "positivity",
                              "natural_source_mass", "mixture_walsh_off_diagonal", "fixed_weight_filter"), 0.0)
    full_distance = walsh_distance = mixture_distance = 0.0
    remainder_distances = [0.0, 0.0]
    filter_weights = list(range(copies+1))
    filtered_distances = {m: 0.0 for m in filter_weights}
    source_blocks = expanded_blocks = zero_blocks = 0
    for sources in itertools.combinations_with_replacement(range(len(partitions)), copies):
        multiplicity = math.factorial(copies)//math.prod(math.factorial(c) for c in Counter(sources).values())
        blocks, mixtures = [], []
        for b in (0, 1):
            tensor = np.ones((order**2, 1, 1), dtype=complex)
            positive = np.ones((order, 1, 1), dtype=complex)
            for j in sources:
                tensor = _prepend_tensor(tensor, kernels[b][j])
                positive = _prepend_tensor(positive, mixture_locals[b][j])
            block = np.einsum("p,pab->ab", outer, tensor)
            diagonal = np.einsum("p,pab->ab", outer[diagonals[b]], tensor[diagonals[b]])
            mixture = np.einsum("g,gab->ab", mixture_weights[b], positive)
            mass = math.prod(p_values[b][j, 0] for j in sources)
            residuals["positive_diagonal_mixture"] = max(residuals["positive_diagonal_mixture"], float(np.linalg.norm(diagonal-mixture)))
            residuals["hermiticity"] = max(residuals["hermiticity"], float(np.linalg.norm(block-block.conj().T)))
            residuals["positivity"] = max(residuals["positivity"], -float(np.linalg.eigvalsh(block).min()))
            residuals["natural_source_mass"] = max(residuals["natural_source_mass"], float(abs(np.trace(block)-mass)), float(abs(np.trace(mixture)-mass)))
            transformed = walsh @ mixture @ walsh.T
            residuals["mixture_walsh_off_diagonal"] = max(residuals["mixture_walsh_off_diagonal"], float(np.linalg.norm(transformed-np.diag(np.diag(transformed)))))
            if mass:
                moments = np.array([p_values[b][j]/p_values[b][j, 0] for j in sources])
                reference = mass*_conditional_selector_kernel(coefficients, moments, masks, data[6], data[7])/size
                residuals["conditional_matrix"] = max(residuals["conditional_matrix"], float(np.linalg.norm(block-reference)))
                for m in filter_weights:
                    selected = tuple(s for s in masks if s.bit_count() == m)
                    p = len(selected)/size
                    projected = block[np.ix_(selected, selected)]/p
                    direct = mass*_conditional_selector_kernel(coefficients, moments, selected, data[6], data[7])/len(selected)
                    residuals["fixed_weight_filter"] = max(residuals["fixed_weight_filter"], float(np.linalg.norm(projected-direct)), float(abs(np.trace(projected)-mass)))
            else:
                zero_blocks += 1
                residuals["natural_source_mass"] = max(residuals["natural_source_mass"], float(np.linalg.norm(block)))
            remainder_distances[b] += multiplicity*_half_trace_norm(block-mixture)
            blocks.append(block)
            mixtures.append(mixture)
        difference = blocks[1]-blocks[0]
        full_distance += multiplicity*_half_trace_norm(difference)
        walsh_distance += multiplicity*float(np.abs(np.diag(walsh @ difference @ walsh.T)).sum()/2)
        mixture_distance += multiplicity*_half_trace_norm(mixtures[1]-mixtures[0])
        for m in filter_weights:
            selected = tuple(s for s in masks if s.bit_count() == m)
            filtered_distances[m] += multiplicity*_half_trace_norm(difference[np.ix_(selected, selected)])*size/len(selected)
        source_blocks += 1
        expanded_blocks += multiplicity
    if expanded_blocks != len(partitions)**copies:
        raise ArithmeticError("source-multiset reduction did not preserve every source tuple")
    if any(actual > bound+1e-10 for actual, bound in zip(remainder_distances, tails)):
        raise ArithmeticError("quantum-state remainder exceeds its complete source-weighted kernel bound")
    physical = evaluate_coherent_subset_phase_query(n, transposition_count, copies, phase_rule, True)
    residuals["physical_full_source_distance"] = abs(full_distance-physical["selector_and_source_label_trace_distance"])
    residuals["physical_walsh_distance"] = abs(walsh_distance-physical["walsh_readout_with_source_labels"]["total_variation"])
    filter_rows = []
    for m in filter_weights:
        p = Fraction(math.comb(copies, m), size)
        if filtered_distances[m] > full_distance/float(p)+1e-10:
            raise ArithmeticError("fixed-weight mask comparison omitted its success probability")
        filter_rows.append({"mask_weight": m, "comparison_success_probability": str(p),
            "selector_quantum_trace_distance": filtered_distances[m],
            "charged_uniform_distance_upper_bound": min(1.0, full_distance/float(p)),
            "physical_postselection_required": False, "efficient_final_povm_supplied": False})
    if max(residuals.values()) > 1e-9:
        raise ArithmeticError("source-selector quantum mixture control failed independent checks")
    return {"degree": n, "copy_count": copies, "phase_rule": phase_rule,
        "source_multisets_evaluated": source_blocks, "ordered_source_blocks_represented": expanded_blocks,
        "zero_mass_source_blocks_retained": zero_blocks,
        "selector_quantum_trace_distance": full_distance, "walsh_trace_distance": walsh_distance,
        "positive_quantum_mixture_trace_distance": mixture_distance,
        "remainder_trace_distances": remainder_distances, "finite_remainder_upper_bounds": tails,
        "kernel_radius_controls": radius_records, "fixed_weight_filter_controls": filter_rows,
        "residuals": residuals, "verified": True,
        "one_hidden_representative_by_conjugation_covariance": True,
        "source_records_are_classical": True, "physical_inputs_discarded": True,
        "optimal_quantum_povm_is_compiled": False, "is_classical_dequantization": False,
        "formal_proof_verification": False, "novelty_established": False, "speedup_claim_allowed": False}


@lru_cache(maxsize=1)
def audit_unmeasured_source_labels() -> dict:
    """A coherent COPY is not a coherent resource on block-diagonal inputs."""
    from coset_binary_carrier_instruments import _source_parity_group_data
    rows = []
    for n, t in ((3, 1), (4, 2)):
        data = _source_parity_group_data(n, t)
        order, count = len(data[0]), len(data[1])
        coefficient = data[3][:, None]*data[2]/order
        projectors = coefficient[:, data[7]]
        isometry = np.concatenate(projectors, axis=0)
        residual = float(np.linalg.norm(isometry.conj().T @ isometry-np.eye(order)))
        actions = np.eye(order)[data[7]]
        for projector in projectors:
            residual = max(residual, float(np.linalg.norm(projector @ actions - actions @ projector)))

        def erase_label_coherences(state: np.ndarray) -> np.ndarray:
            blocks = state.reshape(count, order, count, order)
            dephased = np.zeros_like(blocks)
            for j in range(count):
                dephased[j, :, j, :] = blocks[j, :, j, :]
            return dephased.reshape(count*order, count*order)

        distances = []
        for h in (None, *(indices[0] for indices in data[8])):
            state = np.eye(order)/order if h is None else (np.eye(order)+actions[h])/order
            copied = isometry @ state @ isometry.conj().T
            distances.append(_half_trace_norm(copied-erase_label_coherences(copied)))
        trivial = np.ones(order)/math.sqrt(order)
        sign = data[2][data[1].index((1,)*n)]/math.sqrt(order)
        vector = (trivial+sign)/math.sqrt(2)
        copied = isometry @ np.outer(vector, vector) @ isometry.conj().T
        witness = _half_trace_norm(copied-erase_label_coherences(copied))
        if max(distances) > 1e-10 or residual > 1e-10 or abs(witness-.5) > 1e-10:
            raise ArithmeticError("source-label dephasing identity or its nonstandard-input counterexample failed")
        rows.append({"degree": n, "standard_coset_inputs_checked": len(distances),
            "source_projector_group_action_commutators_checked": count*order,
            "maximum_standard_input_dephasing_distance": max(distances), "isometry_commutation_residual": residual,
            "nonstandard_cross_irrep_pure_input_dephasing_distance": witness,
            "coherent_label_copy_alone_adds_a_resource": False})
    return {"controls": rows, "verified": True,
        "reason": "Central P_j commute with rho_h and every individual group action. A label-copy isometry sum_j |j> P_j therefore has no off-label blocks on standard inputs; common subset queries preserve those blocks.",
        "covers_retaining_nontrivial_physical_carrier_registers": False,
        "arbitrary_pure_inputs_are_not_standard_coset_inputs": True,
        "novelty_established": False}


@lru_cache(maxsize=20, typed=True)
def noncentral_group_algebra_control(n: int, copies: int, unitary_rule: str, retain_irreps: bool) -> dict:
    """Check every hidden member against the regular-basis physical channel."""
    from scipy import sparse
    from coset_binary_carrier_instruments import _source_parity_group_data
    if (type(n) is not int or n not in (3, 4) or type(copies) is not int
            or not 1 <= copies <= (3 if n == 3 else 2) or type(retain_irreps) is not bool):
        raise ValueError("noncentral controls require S3 copies 1..3 or S4 copies 1..2 and an explicit source flag")
    data = _source_parity_group_data(n, 1 if n == 3 else 2)
    order, inverse, products = len(data[0]), data[6], data[7]
    actions = np.eye(order)[products]
    hidden_members = tuple(indices[0] for indices in data[8])
    if unitary_rule == "pointed_involution":
        unitary = actions[hidden_members[0]].astype(complex)
    elif unitary_rule == "ordered_rotations":
        unitary = np.eye(order, dtype=complex)
        for pair, angle in (((0, 1), .37), ((1, 2), .61), ((0, 1), .29)):
            permutation = list(range(n))
            permutation[pair[0]], permutation[pair[1]] = permutation[pair[1]], permutation[pair[0]]
            g = data[0].index(tuple(permutation))
            unitary = unitary @ (math.cos(angle)*np.eye(order)+1j*math.sin(angle)*actions[g])
    else:
        raise ValueError("unknown noncentral unitary rule")
    coefficients = unitary[:, 0]
    outer = np.outer(coefficients.conjugate(), coefficients).reshape(-1)
    p = data[3][:, None]*data[2]/order
    if not retain_irreps:
        p = p.sum(axis=0, keepdims=True)
    projectors = p[:, products]
    count, size = len(p), 2**copies
    active = np.flatnonzero(coefficients)
    physical_size = order**copies
    physical_queries = []
    for mask in range(size):
        query = sparse.csr_matrix((physical_size, physical_size), dtype=complex)
        for g in active:
            term = sparse.csr_matrix([[1.0]])
            for i in range(copies):
                factor = actions[g] if mask & (1 << i) else np.eye(order)
                term = sparse.kron(sparse.csr_matrix(factor), term, format="csr")
            query += coefficients[g]*term
        physical_queries.append(query)
    residuals = {"regular_unitary": float(np.linalg.norm(unitary.conj().T @ unitary-np.eye(order))),
        "coefficient_reconstruction": float(np.linalg.norm(np.einsum("g,gab->ab", coefficients, actions)-unitary)),
        "every_mask_unitary": max(float(sparse.linalg.norm(q.conj().T @ q-sparse.eye(physical_size))) for q in physical_queries),
        "physical_channel": 0.0, "coset_diagonal": 0.0, "natural_mass": 0.0,
        "positivity": 0.0, "right_translation_cancellation": 0.0, "mixture_normalization": 0.0}
    inputs, kernels, diagonal_masks, positive_locals, weights, overlaps = [], [], [], [], [], []
    projected_errors = np.zeros((1+len(hidden_members), copies))
    discarded_masses = np.zeros_like(projected_errors)
    local_tail_bounds = []
    for h in (None, *hidden_members):
        left = None if h is None else products[inverse[h]]
        right = None if h is None else products[inverse, h]
        values = p if h is None else p+p[:, left]
        rho = np.eye(order)/order if h is None else (np.eye(order)+actions[h])/order
        inputs.append(projectors @ rho)
        local = np.zeros((count, order, order, 2, 2))
        local[:, :, :, 0, 0] = values[:, 0, None, None]/2
        local[:, :, :, 0, 1] = values[:, inverse, None]/2
        local[:, :, :, 1, 0] = values[:, None, :]/2
        local[:, :, :, 1, 1] = values[:, products]/2
        kernels.append(local.reshape(count, order**2, 2, 2))
        subgroup = np.zeros(order, dtype=bool)
        subgroup[0] = True
        if h is not None:
            subgroup[h] = True
            residuals["right_translation_cancellation"] = max(residuals["right_translation_cancellation"], float(abs(np.vdot(coefficients, coefficients[right]))))
            overlaps.append((p[:, left]**2) @ np.abs(coefficients)**2)
        diagonal_masks.append(subgroup[products].reshape(-1))
        _, _, b_radius, e_radius, off = _typical_mask_kernel_decomposition(kernels[-1], subgroup, products)
        local_tail_bounds.append([float(np.dot(np.abs(outer[off]),
            _typical_mask_tensor_tail(b_radius[off], e_radius[off], copies, t))/2) for t in range(1, copies+1)])
        positive = np.zeros((count, order, 2, 2))
        positive[:, :, 0, 0] = positive[:, :, 1, 1] = values[:, 0, None]/2
        positive[:, :, 0, 1] = positive[:, :, 1, 0] = values/2
        positive_locals.append(positive)
        amplitude = coefficients if h is None else coefficients+coefficients[right]
        weights.append(np.abs(amplitude)**2/(1 if h is None else 2))
        residuals["mixture_normalization"] = max(residuals["mixture_normalization"], float(abs(weights[-1].sum()-1)))
    overlap_average = np.mean(overlaps, axis=0)
    overlap_cap = p[:, 0]/len(hidden_members)
    if np.any(overlap_average > overlap_cap+1e-12):
        raise ArithmeticError("class-averaged mixed overlap bound failed")
    distances = np.zeros(len(hidden_members))
    decision_distance = average_mixture_distance = independent_hidden_distance = hidden_model_distance = 0.0
    source_blocks = 0
    for sources in itertools.combinations_with_replacement(range(count), copies):
        multiplicity = math.factorial(copies)//math.prod(math.factorial(c) for c in Counter(sources).values())
        blocks, mixtures = [], []
        for b in range(1+len(hidden_members)):
            tensor = np.ones((order**2, 1, 1), dtype=complex)
            positive = np.ones((order, 1, 1), dtype=complex)
            sigma = np.ones((1, 1), dtype=complex)
            for j in sources:
                tensor = _prepend_tensor(tensor, kernels[b][j])
                positive = _prepend_tensor(positive, positive_locals[b][j])
                sigma = np.kron(inputs[b][j], sigma)
            block = np.einsum("p,pab->ab", outer, tensor)
            physical = np.zeros_like(block)
            for s, query in enumerate(physical_queries):
                evolved = query @ sigma
                for t, other in enumerate(physical_queries):
                    physical[s, t] = other.conjugate().multiply(evolved).sum()/size
            mixture = np.einsum("g,gab->ab", weights[b], positive)
            diagonal = diagonal_masks[b]
            diagonal_block = np.einsum("p,pab->ab", outer[diagonal], tensor[diagonal])
            residuals["physical_channel"] = max(residuals["physical_channel"], float(np.linalg.norm(physical-block)))
            residuals["coset_diagonal"] = max(residuals["coset_diagonal"], float(np.linalg.norm(diagonal_block-mixture)))
            residuals["natural_mass"] = max(residuals["natural_mass"], float(abs(np.trace(block)-np.trace(sigma))))
            residuals["positivity"] = max(residuals["positivity"], -float(np.linalg.eigvalsh(block).min()), -float(np.linalg.eigvalsh(mixture).min()))
            for t in range(1, copies+1):
                retained = [s for s in range(size) if s.bit_count() >= t]
                removed = [s for s in range(size) if s.bit_count() < t]
                projected_errors[b, t-1] += multiplicity*_half_trace_norm((block-mixture)[np.ix_(retained, retained)])
                discarded_masses[b, t-1] += multiplicity*float(np.diag(block)[removed].real.sum())
            blocks.append(block)
            mixtures.append(mixture)
        decision_distance += multiplicity*_half_trace_norm(np.mean(blocks[1:], axis=0)-blocks[0])
        for b in range(len(hidden_members)):
            distances[b] += multiplicity*_half_trace_norm(blocks[b+1]-blocks[0])
            average_mixture_distance += multiplicity*_half_trace_norm(mixtures[b+1]-mixtures[0])/len(hidden_members)
        independent_tensor = np.ones((order**2, 1, 1), dtype=complex)
        for j in sources:
            independent_tensor = _prepend_tensor(independent_tensor, np.mean([kernel[j] for kernel in kernels[1:]], axis=0))
        independent_block = np.einsum("p,pab->ab", outer, independent_tensor)
        independent_hidden_distance += multiplicity*_half_trace_norm(independent_block-blocks[0])
        hidden_model_distance += multiplicity*_half_trace_norm(independent_block-np.mean(blocks[1:], axis=0))
        source_blocks += 1
    if max(residuals.values()) > 1e-9 or decision_distance > distances.mean()+1e-10:
        raise ArithmeticError("noncentral physical-channel or class-average control failed")
    pointed_expected = (1-1/size)/len(hidden_members) if unitary_rule == "pointed_involution" and count == 1 else None
    if pointed_expected is not None and abs(decision_distance-pointed_expected) > 1e-10:
        raise ArithmeticError("pointed-involution analytic countercontrol failed")
    mask_checks = []
    for t in range(1, copies+1):
        pi = Fraction(sum(math.comb(copies, w) for w in range(t)), size)
        errors = projected_errors[:, t-1]
        tails = np.asarray(local_tail_bounds)[:, t-1]
        gentle_bound = 2*math.sqrt(float(pi))+average_mixture_distance+errors[0]+float(errors[1:].mean())
        if (np.max(np.abs(discarded_masses[:, t-1]-float(pi))) > 1e-10
                or np.any(errors > tails+1e-10) or distances.mean() > gentle_bound+1e-10):
            raise ArithmeticError("typical-mask projected remainder or gentle-comparison inequality failed")
        mask_checks.append({"minimum_retained_weight": t, "discarded_uniform_mask_mass": str(pi),
            "actual_discarded_masses": discarded_masses[:, t-1].tolist(),
            "projected_remainder_distances": errors.tolist(), "kernel_tail_upper_bounds": tails.tolist(),
            "gentle_comparison_average_individual_upper_bound": min(1.0, gentle_bound), "verified": True})
    return {"degree": n, "copy_count": copies, "unitary_rule": unitary_rule, "retained_source_categories": count,
        "hidden_members_evaluated": len(hidden_members), "source_multisets_evaluated": source_blocks,
        "class_average_decision_trace_distance": decision_distance,
        "average_individual_trace_distance": float(distances.mean()), "individual_trace_distances": distances.tolist(),
        "independent_hidden_per_copy_decision_distance": independent_hidden_distance,
        "same_hidden_vs_independent_hidden_trace_distance": hidden_model_distance,
        "average_positive_mixture_trace_distance": average_mixture_distance,
        "maximum_pointwise_mixed_overlap_violation": float(np.max(np.asarray(overlaps)-overlap_cap)),
        "maximum_class_average_mixed_overlap_violation": float(np.max(overlap_average-overlap_cap)),
        "pointed_involution_analytic_decision_distance": pointed_expected,
        "typical_mask_projection_controls": mask_checks,
        "noncentrality_commutator_norm": max(float(np.linalg.norm(unitary @ action-action @ unitary)) for action in actions),
        "residuals": residuals, "verified": True,
        "hidden_average_taken_after_tensor_products": True, "one_representative_used_without_covariance": False,
        "raw_copy_bound_applies_to_average_individual_distance": False,
        "optimal_quantum_povm_is_compiled": False, "novelty_established": False, "speedup_claim_allowed": False}


def source_selector_quantum_scaling_controls() -> list[dict]:
    rows = []
    flags = dict(one_common_subset_query=True, common_group_algebra_unitary=True,
        unitary_and_partition_fixed_before_inputs=True, hidden_prior_uniform_on_involution_class=True,
        no_hidden_correlated_preprocessing_or_side_information=True,
        source_records_classical=True,
        only_source_records_and_selector_qubits_retained=True, physical_inputs_discarded=True,
        mask_filter_diagonal_and_fixed_before_input=True, mask_filter_is_a_contraction=True)
    for n in (128, 1024, 4096):
        log_class = (math.prod(range(1, n, 2))-1).bit_length()
        for k in (log_class//2, 2*log_class, 4*log_class):
            for filtered in (False, True):
                p = Fraction(1, k+1) if filtered else Fraction(1)
                row = source_selector_quantum_information_contract(n, k, None,
                    hypothesis_independent_filter_success_lower_bound=p, **flags)
                row["mask_family"] = "central_fixed_weight" if filtered else "uniform_full_mask"
                row["fixed_mask_weight"] = k//2 if filtered else None
                rows.append(row)
    return rows


def source_selector_polynomial_budget_controls() -> list[dict]:
    flags = dict(one_common_subset_query=True, common_group_algebra_unitary=True,
        unitary_and_partition_fixed_before_inputs=True, hidden_prior_uniform_on_involution_class=True,
        no_hidden_correlated_preprocessing_or_side_information=True,
        source_records_classical=True, only_source_records_and_selector_qubits_retained=True,
        physical_inputs_discarded=True, mask_filter_diagonal_and_fixed_before_input=True,
        mask_filter_is_a_contraction=True)
    rows = []
    for n in (1024, 4096, 8192):
        for exponent in (2, 4):
            budget = n**exponent
            for filtered in (False, True):
                row = source_selector_polynomial_budget_contract(n, budget, None,
                    filter_success_lower_bound_uniform_over_copy_counts=Fraction(1, budget+1) if filtered else Fraction(1),
                    **flags)
                row["budget_polynomial_degree"] = exponent
                row["mask_family"] = "central_fixed_weight" if filtered else "uniform_full_mask"
                rows.append(row)
    return rows
