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


def corrected_walsh_output_information_contract(degree: int, copy_count: int, *,
        one_uniform_subset_query: bool, real_central_reflection: bool,
        phase_rule_fixed_before_source_labels: bool,
        matching_source_phase_correction: bool, source_labels_discarded_after_correction: bool,
        physical_inputs_discarded: bool) -> dict:
    """Full corrected output, not all retained-source decisions; review pending.

    The binomial-mixture comparison uses central amplitude overlap. Its
    off-coset remainder is small at large k, not throughout the copy window.
    """
    if type(degree) is not int or degree < 16 or degree % 2 or type(copy_count) is not int or copy_count < 1:
        raise ValueError("even S_n degree at least 16 and positive integer copy count required")
    flags = (one_uniform_subset_query, real_central_reflection, phase_rule_fixed_before_source_labels, matching_source_phase_correction,
             source_labels_discarded_after_correction, physical_inputs_discarded)
    if any(type(flag) is not bool for flag in flags):
        raise ValueError("all corrected-output assumptions must be explicit booleans")
    applicable = all(flags)
    order = math.factorial(degree)
    class_size = math.prod(range(1, degree, 2))
    root = math.isqrt(degree)
    exponents = [
        _sqrt_ratio_dyadic_exponent(9 * copy_count**2, 4 * class_size),
        min(0, (order - 1).bit_length() - copy_count),
        _sqrt_ratio_dyadic_exponent(16 * order * (root + 2)**(2 * copy_count), (2 * root)**(2 * copy_count)),
    ]
    mixture_exponent = min(0, max(exponents) + 2)
    raw_exponent = (0 if copy_count >= (4 * class_size).bit_length() else
                    _sqrt_ratio_dyadic_exponent((1 << copy_count) - 1, 4 * class_size))
    exponent = min(mixture_exponent, raw_exponent) if applicable else None
    return {"degree": degree, "copy_count": copy_count, "applicable": applicable,
        "all_source_labels_retained_after_correction": not source_labels_discarded_after_correction,
        "phase_rule_fixed_before_source_labels": phase_rule_fixed_before_source_labels,
        "covers_entire_corrected_bit_string": applicable, "covers_arbitrary_corrected_weight_classifier": applicable,
        "covers_source_selected_parity": False, "covers_arbitrary_retained_source_readout": False,
        "minimum_nonidentity_class_size_used": degree,
        "off_coset_exception_radius_upper_bound": str(Fraction(root + 2, 2 * root)),
        "component_upper_bound_powers_of_two": dict(zip(("mixture_overlap", "bulk_remainder", "exceptional_remainder"), exponents)),
        "mixture_comparison_upper_bound_power_of_two": mixture_exponent if applicable else None,
        "raw_copy_upper_bound_power_of_two": raw_exponent if applicable else None,
        "trace_distance_upper_bound_power_of_two": exponent,
        "bound_is_vacuous": exponent == 0 if applicable else None,
        "all_polynomial_copy_counts_ruled_out": False,
        "copy_count_means_participating_mask_positions": True,
        "is_lower_bound_for_all_algorithms_with_larger_copy_budgets": False,
        "formula": "T <= min(1, raw_copy_bound, 3k/(2 sqrt(M)) + |G|*2^-k + 4 sqrt(|G|)*(1/2+1/sqrt(n))^k)",
        "scope": "One uniform full-mask query with a common real central reflection chosen BEFORE source labels; correct each output bit by that source irrep's phase, then discard source labels and physical inputs. The corrected output is exchangeable, so its full-string distance equals its Hamming-weight distance. Large-copy and small-raw-copy bounds need not meet in the intermediate window.",
        "proof_status": "derived-corrected-output-mixture-bound-review-pending",
        "novelty_established": False, "positive_mixture_is_efficient_classical_sampler": False,
        "is_classical_dequantization": False}


def coarse_source_walsh_information_contract(degree: int, copy_count: int, category_count: int | None, *,
        one_uniform_full_mask_query: bool, common_central_unitary: bool,
        phase_and_common_partition_fixed_before_sources: bool,
        walsh_readout_up_to_category_known_bit_flips: bool,
        only_categories_and_walsh_bits_retained: bool, physical_inputs_discarded: bool) -> dict:
    """Full paired transcript, even all irreps and complex phases; review pending.

    None retains all irreps and uses p(n) <= 2**(n-1), not an irrep enumeration.
    Column orthogonality removes category count from the off-coset radius.
    This is an assumption contract, not a verifier for an arbitrary circuit.
    """
    if (type(degree) is not int or degree < 8 or degree % 2 or type(copy_count) is not int or copy_count < 1
            or (category_count is not None and (type(category_count) is not int or category_count < 1))):
        raise ValueError("even S_n degree >=8, positive integer copies, and positive category count or None required")
    flags = (one_uniform_full_mask_query, common_central_unitary, phase_and_common_partition_fixed_before_sources,
             walsh_readout_up_to_category_known_bit_flips, only_categories_and_walsh_bits_retained, physical_inputs_discarded)
    if any(type(flag) is not bool for flag in flags):
        raise ValueError("explicit boolean coarse-source access assumptions required")
    applicable = all(flags)
    order, class_size = math.factorial(degree), math.prod(range(1, degree, 2))
    category_bound = (1 << (degree - 1)) if category_count is None else category_count
    minimum_class_size = degree * (degree - 1) // 2
    root_l = math.isqrt(minimum_class_size)
    radius = min(Fraction(1), Fraction(root_l + 6, 2 * root_l))
    mixture_exponent = _sqrt_ratio_dyadic_exponent(4 * copy_count**2 * category_bound, class_size)
    remainder_exponent = _sqrt_ratio_dyadic_exponent(order**2 * radius.numerator**(2 * copy_count),
                                                     radius.denominator**(2 * copy_count))
    combined = min(0, max(mixture_exponent, remainder_exponent) + 1)
    raw = (0 if copy_count >= (4 * class_size).bit_length() else
           _sqrt_ratio_dyadic_exponent((1 << copy_count) - 1, 4 * class_size))
    bound = min(raw, combined) if applicable else None
    return {"degree": degree, "copy_count": copy_count, "retained_category_count": category_count,
        "category_count_upper_bound": str(category_bound),
        "all_irrep_labels_retained": category_count is None,
        "all_irrep_count_bound": "p(n) <= 2^(n-1)" if category_count is None else None,
        "minimum_nonidentity_class_size_used": minimum_class_size, "applicable": applicable,
        "off_coset_radius_upper_bound": str(radius),
        "off_coset_radius_independent_of_category_count": True,
        "mixture_upper_bound_power_of_two": mixture_exponent if applicable else None,
        "remainder_upper_bound_power_of_two": remainder_exponent if applicable else None,
        "raw_copy_upper_bound_power_of_two": raw if applicable else None,
        "trace_distance_upper_bound_power_of_two": bound, "bound_is_vacuous": bound == 0 if applicable else None,
        "retains_all_category_and_walsh_bit_pairs": applicable,
        "covers_category_selected_parity_and_count_decisions": applicable,
        "covers_arbitrary_complex_central_phases": applicable,
        "covers_arbitrary_classical_full_source_walsh_decisions": applicable and category_count is None,
        "covers_unrecorded_irrep_information": False, "covers_input_adaptive_partitions": False,
        "covers_multiple_queries_or_final_coherent_povm": False,
        "all_copy_counts_obstructed": False, "copy_count_is_available_resource_budget": False,
        "category_count_is_computational_runtime": False, "positive_mixture_is_efficient_classical_sampler": False,
        "formula": "T <= min(1, raw_copy_bound, 2k*sqrt(r/M) + |G|*min(1,1/2+3/sqrt(L))^k), L=n(n-1)/2",
        "scope": "One uniform full-mask query with a common central UNITARY (complex phases allowed) and common irrep partition fixed BEFORE sources. Keep every paired category label and raw Walsh bit, with optional category-known classical bit flips, and discard physical inputs. All irreps are covered using r<=2^(n-1); phase need not be constant within a raw-readout category. The intermediate participating-copy window remains open. No claim about arbitrary coherent final measurements, input-adaptive phases, or algorithms that ignore extra available copies.",
        "proof_status": "derived-full-source-walsh-bound-review-pending",
        "novelty_established": False, "is_classical_dequantization": False}


def _typical_mask_component_exponents(order: int, class_size: int, categories: int, root: int,
                                     copies: int, mixture_copy_budget: int | None = None) -> dict | None:
    if root <= 8:
        return None
    t = copies//4
    budget = copies if mixture_copy_budget is None else mixture_copy_budget
    return {
        "mixture": _sqrt_ratio_dyadic_exponent(4*budget**2*categories, class_size),
        "discarded_mask": min(0, 1-copies//16),
        "bulk_remainder": _sqrt_ratio_dyadic_exponent(order**2*6**(2*t), root**(2*t)),
        # k <= 4t+3 removes endpoint oscillations, giving a monotone envelope.
        "endpoint_remainder": _sqrt_ratio_dyadic_exponent(128*order*8**(2*t), root**(2*t)),
    }


def source_selector_quantum_information_contract(degree: int, copy_count: int, category_count: int | None, *,
        one_common_subset_query: bool, common_group_algebra_unitary: bool,
        unitary_and_partition_fixed_before_inputs: bool, hidden_prior_uniform_on_involution_class: bool,
        no_hidden_correlated_preprocessing_or_side_information: bool,
        source_records_classical: bool,
        only_source_records_and_selector_qubits_retained: bool, physical_inputs_discarded: bool,
        mask_filter_diagonal_and_fixed_before_input: bool, mask_filter_is_a_contraction: bool,
        hypothesis_independent_filter_success_lower_bound: Fraction = Fraction(1)) -> dict:
    """Before ANY selector POVM, including charged mask filters; review pending.

    Source records are classical, not coherent physical source registers.
    Bounds are assumptions/contracts, not arbitrary-program verification.
    """
    if (type(degree) is not int or degree < 8 or degree % 2 or type(copy_count) is not int or copy_count < 1
            or (category_count is not None and (type(category_count) is not int or category_count < 1))):
        raise ValueError("even S_n degree >=8, positive integer copies, and positive category count or None required")
    flags = (one_common_subset_query, common_group_algebra_unitary, unitary_and_partition_fixed_before_inputs,
             hidden_prior_uniform_on_involution_class,
             no_hidden_correlated_preprocessing_or_side_information,
             source_records_classical, only_source_records_and_selector_qubits_retained,
             physical_inputs_discarded, mask_filter_diagonal_and_fixed_before_input, mask_filter_is_a_contraction)
    if any(type(flag) is not bool for flag in flags):
        raise ValueError("explicit boolean source/selector assumptions required")
    p = hypothesis_independent_filter_success_lower_bound
    if type(p) not in (int, Fraction) or not 0 < p <= 1:
        raise ValueError("exact rational filter-success lower bound in (0,1] required")
    p = Fraction(p)
    applicable = all(flags)
    order, class_size = math.factorial(degree), math.prod(range(1, degree, 2))
    r = 1 << (degree-1) if category_count is None else category_count
    minimum_class = degree*(degree-1)//2
    root = math.isqrt(minimum_class)
    bulk = min(Fraction(1), Fraction(root+6, 2*root))
    endpoint_squared = min(Fraction(1), Fraction((root+2)**2, 2*root**2))
    components = {
        "mixture": _sqrt_ratio_dyadic_exponent(4*copy_count**2*r, class_size),
        "bulk_remainder": _sqrt_ratio_dyadic_exponent(order**2*bulk.numerator**(2*copy_count), bulk.denominator**(2*copy_count)),
        "endpoint_remainder": _sqrt_ratio_dyadic_exponent(16*order*endpoint_squared.numerator**copy_count,
                                                         endpoint_squared.denominator**copy_count),
    }
    unpruned = min(0, max(components.values())+2)
    typical = _typical_mask_component_exponents(order, class_size, r, root, copy_count)
    typical_bound = min(0, max(typical.values())+2) if typical is not None else None
    uniform = unpruned if typical_bound is None else min(unpruned, typical_bound)
    filtered = _sqrt_ratio_dyadic_exponent(p.denominator**2, p.numerator**2*(1 << (-2*uniform)))
    raw = (0 if copy_count >= (4*class_size).bit_length() else
           _sqrt_ratio_dyadic_exponent((1 << copy_count)-1, 4*class_size))
    bound = min(raw, filtered) if applicable else None
    return {"degree": degree, "copy_count": copy_count, "retained_category_count": category_count,
        "all_irrep_labels_retained": category_count is None, "category_count_upper_bound": str(r),
        "applicable": applicable, "source_records_classical": source_records_classical,
        "minimum_nonidentity_class_size_used": minimum_class,
        "bulk_trace_norm_radius_upper_bound": str(bulk),
        "endpoint_trace_norm_radius_squared_upper_bound": str(endpoint_squared),
        "uniform_component_upper_bound_powers_of_two": components,
        "unpruned_uniform_upper_bound_power_of_two": unpruned if applicable else None,
        "typical_mask_component_upper_bound_powers_of_two": typical if applicable else None,
        "typical_mask_uniform_upper_bound_power_of_two": typical_bound if applicable else None,
        "typical_mask_minimum_retained_weight": copy_count//4,
        "uniform_quantum_upper_bound_power_of_two": uniform if applicable else None,
        "filter_success_lower_bound": str(p), "filter_information_penalty_charged": str(1/p),
        "filtered_quantum_upper_bound_power_of_two": filtered if applicable else None,
        "raw_copy_upper_bound_power_of_two": raw if applicable else None,
        "trace_distance_upper_bound_power_of_two": bound, "bound_is_vacuous": bound == 0 if applicable else None,
        "covers_arbitrary_final_selector_povm": applicable,
        "covers_complex_common_central_phases": applicable,
        "covers_noncentral_common_group_algebra_unitaries": applicable,
        "bounded_quantity": "T(Omega_0, E_h Omega_h), one shared h drawn uniformly from the involution class",
        "pointwise_hidden_bound_for_noncentral_unitary": False,
        "raw_copy_bound_applies_to_average_individual_distance": False,
        "polynomial_budget_obstruction_derived_asymptotically": applicable,
        "all_copy_budget_certificate_requires_separate_interval_bound": True,
        "covers_coherent_source_or_retained_physical_registers": False,
        "covers_source_adaptive_phase_or_multiple_queries": False,
        "all_copy_counts_obstructed": False, "copy_count_is_available_resource_budget": False,
        "comparison_filter_is_required_physical_preparation": False,
        "formula": "T <= min(1, raw_copy_bound, unpruned_quantum_bound/p, typical_mask_quantum_bound/p)",
        "scope": "Standard mixed coset inputs alone, without hidden-correlated side information. One shared unknown involution is uniform on its class and averaged AFTER tensor products. One common group-algebra UNITARY, not necessarily central, and source partition are fixed before inputs; retain CLASSICAL source records and the ENTIRE quantum selector, discard physical inputs. The mixture/remainder bounds control E_h T(Omega_0,Omega_h), but their minimum with the raw-copy bound controls only T(Omega_0,E_h Omega_h). The typical-mask refinement removes weights below floor(k/4) with a charged gentle-projection error. Uniform masks and inverse-polynomial-overlap diagonal filters are obstructed for every polynomial copy budget asymptotically, not for every n or exponential budget. A separate interval certificate covers variable participation. No physical retention, source-adaptive unitary, multiple queries or arbitrary mask state is covered.",
        "proof_status": "derived-source-selector-quantum-bound-review-pending",
        "assumption_contract_not_arbitrary_program_verifier": True,
        "novelty_established": False, "is_classical_dequantization": False}


def source_selector_polynomial_budget_contract(degree: int, max_copy_count: int, category_count: int | None, *,
        filter_success_lower_bound_uniform_over_copy_counts: Fraction = Fraction(1), **assumptions) -> dict:
    """Bound EVERY participating count <= a budget, without sweeping that budget."""
    if type(max_copy_count) is not int or max_copy_count < 1:
        raise ValueError("positive integer copy budget required")
    if type(degree) is not int or degree < 16 or degree % 2:
        raise ValueError("even degree >=16 required for the monotone typical-mask envelope")
    pivot = min(max_copy_count, 5*degree)
    check = source_selector_quantum_information_contract(degree, pivot, category_count,
        hypothesis_independent_filter_success_lower_bound=filter_success_lower_bound_uniform_over_copy_counts, **assumptions)
    applicable = check["applicable"]
    raw = check["raw_copy_upper_bound_power_of_two"]
    terms = None
    uniform = filtered = None
    p = Fraction(check["filter_success_lower_bound"])
    if max_copy_count > pivot:
        order, class_size = math.factorial(degree), math.prod(range(1, degree, 2))
        root = math.isqrt(degree*(degree-1)//2)
        r = int(check["category_count_upper_bound"])
        terms = _typical_mask_component_exponents(order, class_size, r, root, pivot+1, max_copy_count)
        uniform = min(0, max(terms.values())+2)
        filtered = _sqrt_ratio_dyadic_exponent(p.denominator**2, p.numerator**2*(1 << (-2*uniform)))
    bound = (raw if filtered is None else max(raw, filtered)) if applicable else None
    return {"degree": degree, "maximum_available_copy_budget": max_copy_count,
        "retained_category_count": category_count, "category_count_upper_bound": check["category_count_upper_bound"],
        "raw_copy_prefix_end": pivot, "typical_mask_suffix_start": pivot+1 if max_copy_count > pivot else None,
        "applicable": applicable, "all_participating_counts_through_budget_covered": applicable,
        "raw_prefix_upper_bound_power_of_two": raw,
        "suffix_component_upper_bound_powers_of_two": terms if applicable else None,
        "uniform_suffix_upper_bound_power_of_two": uniform if applicable else None,
        "filtered_suffix_upper_bound_power_of_two": filtered if applicable else None,
        "trace_distance_upper_bound_power_of_two": bound, "bound_is_vacuous": bound == 0 if applicable else None,
        "filter_success_lower_bound_uniform_over_copy_counts": str(p),
        "bounded_quantity": check["bounded_quantity"],
        "polynomial_budget_and_inverse_filter_overlap_required_for_asymptotic_claim": True,
        "covers_exponential_copy_budgets_asymptotically": False, "covers_arbitrary_masks": False,
        "scope": check["scope"], "proof_status": "derived-typical-mask-budget-obstruction-review-pending",
        "formal_proof_verification": False, "novelty_established": False, "is_classical_dequantization": False}


def source_selector_mask_tail_information_contract(degree: int, copy_count: int, category_count: int | None,
        minimum_mask_weight: int, *, mask_lower_tail_probability_upper_bound: Fraction,
        one_common_subset_query: bool, common_group_algebra_unitary: bool,
        unitary_and_partition_fixed_before_inputs: bool, hidden_prior_uniform_on_involution_class: bool,
        no_hidden_correlated_preprocessing_or_side_information: bool, source_records_classical: bool,
        only_source_records_and_selector_qubits_retained: bool, physical_inputs_discarded: bool,
        mask_fixed_before_inputs_and_source_records: bool) -> dict:
    """Conditional arbitrary-mask tail bound, not a verifier of a supplied program/mask."""
    if type(degree) is not int or degree < 8 or degree % 2:
        raise ValueError("even symmetric-group degree >=8 required")
    if type(copy_count) is not int or copy_count < 1:
        raise ValueError("positive integer copy count required")
    if type(minimum_mask_weight) is not int or not 0 <= minimum_mask_weight <= copy_count:
        raise ValueError("mask weight threshold must be an integer between zero and copy count")
    if category_count is not None and (type(category_count) is not int or category_count < 1):
        raise ValueError("positive integer category count or None required")
    pi = mask_lower_tail_probability_upper_bound
    if type(pi) not in (int, Fraction) or not 0 <= pi <= 1:
        raise ValueError("exact rational mask lower-tail probability bound in [0,1] required")
    flags = (one_common_subset_query, common_group_algebra_unitary,
        unitary_and_partition_fixed_before_inputs, hidden_prior_uniform_on_involution_class,
        no_hidden_correlated_preprocessing_or_side_information, source_records_classical,
        only_source_records_and_selector_qubits_retained, physical_inputs_discarded,
        mask_fixed_before_inputs_and_source_records)
    if any(type(flag) is not bool for flag in flags):
        raise ValueError("all architecture assumptions must be explicit booleans")
    applicable, pi = all(flags), Fraction(pi)
    d, m = math.factorial(degree), math.prod(range(1, degree, 2))
    r = 2**(degree-1) if category_count is None else category_count
    root = math.isqrt(degree*(degree-1)//2)
    bulk, endpoint = min(Fraction(1), Fraction(12, root)), min(Fraction(1), Fraction(2, root))
    squares = {"mixture": Fraction(4*copy_count**2*r, m), "discarded_mask": 4*pi,
        "bulk_remainder": d*d*bulk**minimum_mask_weight,
        "endpoint_remainder": 16*d*endpoint**minimum_mask_weight}
    terms = {key: _sqrt_ratio_dyadic_exponent(value.numerator, value.denominator) for key, value in squares.items()}
    comparison = min(0, max(value for value in terms.values() if value is not None)+2)
    raw = (0 if copy_count >= (4*m).bit_length() else
        _sqrt_ratio_dyadic_exponent((1 << copy_count)-1, 4*m))
    bound = min(raw, comparison) if applicable else None
    return {"degree": degree, "copy_count": copy_count, "minimum_mask_weight": minimum_mask_weight,
        "category_count_upper_bound": str(r), "mask_lower_tail_probability_upper_bound": str(pi),
        "applicable": applicable, "component_upper_bound_powers_of_two": terms if applicable else None,
        "bulk_environment_failure_probability_upper_bound": str(bulk),
        "endpoint_environment_failure_probability_upper_bound": str(endpoint),
        "comparison_upper_bound_power_of_two": comparison if applicable else None,
        "raw_copy_upper_bound_power_of_two": raw if applicable else None,
        "trace_distance_upper_bound_power_of_two": bound, "bound_is_vacuous": bound == 0 if applicable else None,
        "bounded_quantity": "T(Omega_0, E_h Omega_h), one shared hidden h averaged AFTER products",
        "uniform_mask_overlap_penalty_required": False, "all_arbitrary_masks_obstructed": False,
        "source_dependent_masks_covered": False, "mask_tail_bound_supplied_not_independently_verified": True,
        "formula": "T <= min(1, raw_copy_bound, 2k sqrt(r/M)+2sqrt(pi)+D min(1,12/sqrt(L))^(t/2)+4sqrt(D) min(1,2/sqrt(L))^(t/2))",
        "scope": "One fixed common group-algebra query; standard mixed inputs, a shared uniform hidden involution, classical source records and full physical discard. The normalized pure mask is fixed independently of hidden inputs AND source records. pi bounds its mass on weights <t. The positive comparison is a channel image of the commuting Walsh mixture, not the exact output. Arbitrary low-occupation masks, source adaptation, retained physical data and multiple queries are NOT ruled out.",
        "proof_status": "derived-mask-tail-fidelity-bound-review-pending", "formal_proof_verification": False,
        "independent_review": False, "novelty_established": False, "is_classical_dequantization": False}


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

    def phase_unitary(self, phases: Mapping[Hashable, complex]) -> np.ndarray:
        """W^dagger D_phase W on clean workspace, not an irrep measurement.

        Every occupied or unoccupied irrep needs a unit phase. In particular,
        assigning phase zero to a vanishing character is not a unitary query.
        """
        if set(phases) != set(self.labels):
            raise ValueError("one phase for every irrep label is required")
        values = np.asarray([phases[label] for label in self.labels], dtype=complex)
        if not np.isfinite(values).all() or np.max(np.abs(np.abs(values) - 1)) > 1e-10:
            raise ValueError("finite unit-modulus irrep phases required")
        return sum((value * self.projectors[label] for label, value in zip(self.labels, values)),
                   np.zeros((self.dimension, self.dimension), dtype=complex))

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


def coherent_subset_phase_resource_contract(degree: int, copy_count: int, *,
        source_qft_operator_error: float = 0.0, phase_gpe_operator_error: float = 0.0) -> dict:
    """Physical regular-register implementation with ALL source labels retained.

    Each source uses QFT, copy/measure label, inverse QFT before known group
    multiplication. The coherent mask query then uses W^dagger D_sign W.
    Exact fixed-point-free character SIGN is reversible classical arithmetic,
    not a generic QSVT sign approximation through a tiny spectral gap.
    """
    if type(degree) is not int or degree < 2 or degree % 2:
        raise ValueError("even symmetric-group degree required")
    base = isotypic_label_resource_contract(degree, copy_count)
    if any(not math.isfinite(error) or error < 0 for error in (source_qft_operator_error, phase_gpe_operator_error)):
        raise ValueError("finite nonnegative implementation errors required")
    return {
        "degree": degree, "coset_samples_required": copy_count,
        "program": ["SOURCE_QFT_COPY_LABEL_INVERSE_QFT", "HADAMARD_ALL_MASK_QUBITS",
            "COHERENT_MASK_CONTROLLED_GPE", "EXACT_NEGATIVE_CHARACTER_PHASE_ZERO_MAPS_TO_PLUS_ONE",
            "INVERSE_COHERENT_MASK_CONTROLLED_GPE", "DISCARD_PHYSICAL_INPUTS",
            "HADAMARD_MASK_READOUT_RETAIN_SOURCE_LABELS"],
        "source_qft_or_inverse_calls": 2 * copy_count,
        "phase_query_group_qft_or_inverse_calls": 2,
        "total_group_qft_or_inverse_calls": 2 * copy_count + 2,
        "mask_register_qubits": copy_count, "addressed_mask_count": "2^k (including empty mask)",
        "controlled_single_copy_group_action_or_inverse_calls": 2 * copy_count,
        "reference_register_qubits": base["reference_register_qubits"],
        "exact_character_arithmetic_and_uncomputation_calls": 2,
        "terminal_classical_character_evaluations_upper_bound": copy_count,
        "terminal_parity_or_threshold_bit_work": "O(k), in addition to exact character arithmetic",
        "composed_channel_diamond_distance_upper_bound": min(2.0,
            4 * copy_count * source_qft_operator_error + 4 * phase_gpe_operator_error),
        "source_labels_retained": True, "spectral_gap_resolution_required": False,
        "uses_exact_irrep_labels_not_generic_class_sum_block_encoding": True,
        "uniform_reduction_to_known_primitives": True,
        "gate_level_qft_or_reversible_arithmetic_backend_supplied": False,
        "phase_predicate_is_a_binary_hypothesis_classifier": False,
        "polynomial_terminal_rules_supplied": True,
        "terminal_rule_with_scalable_signal_supplied": False, "scalable_signal_proved": False,
        "coset_preparation_and_natural_reduction_must_be_charged": True,
        "scope": "One common isotypic sign phase coherently addressed by k mask bits on S_n fixed-point-free coset inputs. All 2^k masks cost 2k controlled group actions, not 2^k calls. Initial source-label extraction costs 2k additional group QFTs on the physical-register route. This supplies a measurement family, not the sign of the full noncommuting many-copy likelihood operator or a useful classifier.",
    }


def unlabeled_coherent_selector_information_contract(class_size: int, *, source_labels_discarded: bool,
        physical_inputs_discarded: bool, one_common_phase_element: bool, include_empty_mask: bool) -> dict:
    """One uniform mask query ONLY; never apply to the retained-source experiment."""
    if type(class_size) is not int or class_size < 1:
        raise ValueError("positive integer class size required")
    flags = (source_labels_discarded, physical_inputs_discarded, one_common_phase_element, include_empty_mask)
    if any(type(flag) is not bool for flag in flags):
        raise ValueError("explicit boolean selector assumptions required")
    applicable = source_labels_discarded and physical_inputs_discarded and one_common_phase_element
    numerator = 5 if include_empty_mask else 3
    return {"applicable": applicable, "source_labels_discarded": source_labels_discarded,
        "physical_inputs_discarded": physical_inputs_discarded,
        "one_common_phase_element": one_common_phase_element, "include_empty_mask": include_empty_mask,
        "trace_distance_squared_bound_formula": f"min(1,{numerator}/M)" if applicable else None,
        "trace_distance_upper_bound_power_of_two": _sqrt_ratio_dyadic_exponent(numerator, class_size) if applicable else None,
        "covers_retained_source_labels": False, "is_classical_dequantization": False,
        "proof_status": "derived-unlabeled-selector-kernel-review-pending", "novelty_established": False,
        "scope": "Uniform coherent superposition over all nonempty masks, or all masks including empty. One fixed group-algebra unitary is applied on the chosen subset, after which ONLY the selector remains. Source-dependent phases, retained source labels, retained physical inputs, or multiple queries are not covered.",
    }


def low_order_coherent_selector_information_contract(degree: int, copy_count: int, observed_bits: int, *,
        one_uniform_subset_query: bool, output_is_fixed_mask_marginal: bool,
        physical_inputs_discarded: bool) -> dict:
    """All source labels retained, but only fixed d mask qubits observed.

    Tracing the other masks produces an INPUT-INDEPENDENT uniform mixture
    over background subsets. Each branch uses d singleton cells and one
    background cell. Charge its rare-small-cell tail, never postselect it.
    """
    if type(degree) is not int or degree < 8 or degree % 2:
        raise ValueError("even symmetric-group degree >=8 required")
    if (type(copy_count) is not int or type(observed_bits) is not int
            or not 1 <= observed_bits < copy_count):
        raise ValueError("positive fixed observed bits fewer than input copies required")
    flags = (one_uniform_subset_query, output_is_fixed_mask_marginal, physical_inputs_discarded)
    if any(type(flag) is not bool for flag in flags):
        raise ValueError("explicit boolean marginal assumptions required")
    applicable = all(flags)
    background_bits, threshold = copy_count - observed_bits, 2 * degree
    class_size = math.factorial(degree) // (2**(degree // 2) * math.factorial(degree // 2))
    raw_exponent = (0 if copy_count >= (4 * class_size).bit_length()
                    else _sqrt_ratio_dyadic_exponent((1 << copy_count) - 1, 4 * class_size))
    tail_exponent = large_exponent = 0
    large = None
    if applicable and background_bits >= threshold:
        term, tail_numerator = 1, 0
        for j in range(threshold):
            tail_numerator += term
            term = term * (background_bits - j) // (j + 1)
        tail_exponent = _sqrt_ratio_dyadic_exponent(tail_numerator**2, 1 << (2 * background_bits))
        palette = (tuple(range(observed_bits, observed_bits + threshold)),) + tuple((i,) for i in range(observed_bits))
        large = source_conditioned_palette_information_contract(degree, copy_count, palette,
            palette_fixed_before_source_labels=True, operations_and_readout_in_cell_algebra=True,
            retain_cells_below=threshold)
        large_exponent = large["trace_distance_upper_bound_power_of_two"]
    return {"degree": degree, "copy_count": copy_count, "observed_mask_bits": observed_bits,
        "all_source_labels_retained": True, "applicable": applicable,
        "background_cell_threshold": threshold,
        "rare_background_probability_upper_bound_power_of_two": tail_exponent if applicable else None,
        "large_background_bound": large,
        "raw_input_trace_distance_upper_bound_power_of_two": raw_exponent,
        "trace_distance_upper_bound_power_of_two": min(raw_exponent, max(tail_exponent, large_exponent) + 1) if applicable else None,
        "aggregation": "Minimum of the raw-copy information bound and Pr[Binomial(k-d,1/2)<2n] + delta(d raw inputs, one cell of width 2n, all k source labels)",
        "background_selection_is_input_independent": True,
        "postselection_normalization_used": False,
        "covers_arbitrary_full_selector_classifier": False,
        "covers_threshold_of_low_degree_score": False,
        "proof_status": "derived-fixed-selector-marginal-bound-review-pending",
        "novelty_established": False, "is_classical_dequantization": False,
        "scope": "One uniform full-mask subset group-algebra query on standard mixed S_n fixed-point-free coset inputs. All classical source labels remain, but only d mask positions fixed BEFORE the input are retained. Other mask qubits are traced without joint processing, and physical inputs are discarded. The bound does not cover source-selected positions, multiple queries, full-bit thresholding, or joint selector processing before the trace.",
    }


def coherent_parity_information_contract(degree: int, copy_count: int, parity_size: int, *,
        one_uniform_subset_query: bool, parity_positions_fixed_before_input: bool,
        physical_inputs_discarded: bool) -> dict:
    """Any fixed Walsh parity reduces to an input-independent two-subset test.

    All source labels remain. A random S and T=S xor B create at most three
    incidence cells (two for full parity). Uniform worst-profile cell bounds
    require no factor equal to the number of possible random subsets.
    """
    if type(degree) is not int or degree < 8 or degree % 2:
        raise ValueError("even symmetric-group degree >=8 required")
    if (type(copy_count) is not int or copy_count < 1 or type(parity_size) is not int
            or not 0 <= parity_size <= copy_count):
        raise ValueError("positive copy count and parity size in [0,k] required")
    flags = (one_uniform_subset_query, parity_positions_fixed_before_input, physical_inputs_discarded)
    if any(type(flag) is not bool for flag in flags):
        raise ValueError("explicit boolean parity assumptions required")
    applicable = all(flags)
    order = math.factorial(degree)
    class_size = order // (2**(degree // 2) * math.factorial(degree // 2))
    cells = 0 if parity_size == 0 else (2 if parity_size == copy_count else 3)
    threshold = (4 * degree + 2) // 3
    effective = cells * (threshold - 1)
    terms = [{"term": "all_source_labels", "multiplicity": 1,
              "upper_bound_power_of_two": _sqrt_ratio_dyadic_exponent(copy_count**2, 4 * class_size)}]
    if cells:
        terms.extend([
            {"term": "worst_profile_effective_copies", "multiplicity": 1,
             "upper_bound_power_of_two": _sqrt_ratio_dyadic_exponent((1 << effective) - 1, 4 * class_size)},
            {"term": "null_large_cell_error", "multiplicity": cells,
             "upper_bound_power_of_two": _sqrt_ratio_dyadic_exponent(order - 1, 4 * degree**threshold)},
            {"term": "alternative_large_cell_error", "multiplicity": cells,
             "upper_bound_power_of_two": _sqrt_ratio_dyadic_exponent((order - 2) * 9**threshold, 4 * degree**threshold)},
        ])
    term_count = sum(row["multiplicity"] for row in terms)
    exponent = min(0, max(row["upper_bound_power_of_two"] for row in terms) + (term_count - 1).bit_length())
    raw_exponent = (0 if copy_count >= (4 * class_size).bit_length()
                    else _sqrt_ratio_dyadic_exponent((1 << copy_count) - 1, 4 * class_size))
    return {"degree": degree, "copy_count": copy_count, "parity_size": parity_size,
        "all_source_labels_retained": True, "applicable": applicable,
        "random_test_subset_count": 0 if cells == 0 else 2, "maximum_incidence_cells": cells,
        "cell_retention_threshold": threshold, "worst_profile_effective_copy_bound": effective,
        "bound_components": terms, "raw_copy_bound_power_of_two": raw_exponent,
        "trace_distance_upper_bound_power_of_two": min(exponent, raw_exponent) if applicable else None,
        "random_subset_selection_is_input_independent": True,
        "exponential_catalogue_factor_charged": False,
        "full_parity_is_covered": parity_size == copy_count,
        "arbitrary_threshold_is_covered": False, "classical_quantum_frontend_replacement": False,
        "fourier_transfer_requires_sum_of_source_supremum_coefficients": True,
        "bounded_norm_separately_for_each_source_is_sufficient": False,
        "proof_status": "derived-random-two-subset-parity-bound-review-pending",
        "novelty_established": False,
        "scope": "One uniform full-mask subset query; all classical source labels and one parity on positions fixed BEFORE the input. Reproduce that parity by a Hadamard test of U_(S xor B)^dagger U_S for input-independent uniform S. Source-based output-bit flips are allowed; source-selected parity positions, joint parity vectors, arbitrary full-output decisions and multiple queries are not covered."}
