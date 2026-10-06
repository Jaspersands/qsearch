"""Native signature obstruction to low-variation physical pivot subcodes.

LOCAL DERIVATION / REVIEW PENDING. Applies the code-product Kneser theorem,
not a general quantum-algorithm no-go. No search through pivot subspaces.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path

from dcp_bell_inference_kernel import exact
from dcp_pivot_span_obstructions import _row_basis

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/dcp_native_schur_expansion.json"
KNESER_SOURCE = "https://arxiv.org/pdf/1501.06419"


def _binary_code(rows, width):
    if type(width) is not int or width < 1:
        raise ValueError("positive physical width required")
    rows = tuple(rows)
    if not rows or len(_row_basis(rows, width)) != len(rows):
        raise ValueError("nonempty independent binary parity rows required")
    return rows


def signature_capacity(n, extension_rank_budget, unit_augmented_dimension_floor):
    r, p = extension_rank_budget, unit_augmented_dimension_floor
    if any(type(x) is not int for x in (n, r, p)) or n < 1 or r < 0 or p < 1:
        raise ValueError("positive rank/dimension and nonnegative extension budget required")
    components = max(1, p - r)
    if components > n + r:
        return components, 0
    capacity = (1 << (n + r - components + 1)) + components - 2
    return components, min(capacity, (1 << n) - 1)


def universal_signature_gate(rows, width, pivot_dimension, extension_rank_budget):
    R = _binary_code(rows, width)
    n, t, r = len(R), pivot_dimension, extension_rank_budget
    if any(type(x) is not int for x in (t, r)) or not 1 <= t <= width - n or r < 0:
        raise ValueError("valid positive kernel subspace dimension and nonnegative rank budget required")
    columns = tuple(sum((row >> i & 1) << l for l, row in enumerate(R)) for i in range(width))
    zero_columns = columns.count(0)
    unit_is_in_kernel = all(row.bit_count() % 2 == 0 for row in R)
    # Puncture the zero columns before applying the full-support product theorem.
    active_rank_floor = max(0, t - zero_columns)
    augmented_floor = max(1, active_rank_floor + int(not unit_is_in_kernel))
    components, capacity = signature_capacity(n, r, augmented_floor)
    distinct = len(set(columns) - {0})
    excluded = distinct > capacity
    return {"status": "ALL_PHYSICAL_KERNEL_SUBSPACES_LOW_VARIATION_SIGNATURE_GATE",
            "dimension": n, "physical_width": width, "pivot_dimension": t,
            "extension_rank_budget": r, "zero_binary_columns": zero_columns,
            "distinct_nonzero_binary_column_signatures": distinct,
            "all_one_physical_vector_in_kernel": unit_is_in_kernel,
            "active_projection_dimension_lower_bound": active_rank_floor,
            "unit_augmented_subcode_dimension_lower_bound": augmented_floor,
            "required_product_stabilizer_component_count_lower_bound": components,
            "nonzero_signature_capacity_upper_bound_decimal": str(capacity),
            "every_t_dimensional_physical_kernel_subspace_with_extension_rank_at_most_r_excluded": excluded,
            "higher_label_adaptive_subspace_selection_evades_this_gate": False,
            "isotropic_chart_or_pivot_basis_selection_needed_by_gate": False,
            "excludes_any_nonsingular_pencil_at_larger_variation_rank": False,
            "background_adaptive_pivots_general_decoders_or_other_phase_sources_excluded": False,
            "kneser_theorem_source": {"url": KNESER_SOURCE, "theorem": "3.3",
                                      "decomposition": "Lemma2.7 and Lemma2.10",
                                      "binary_field_assumptions_checked": True},
            "candidate_record_accepted": False, "speedup_claim_allowed": False}


def _code_components(rows, width):
    basis = _row_basis(rows, width)
    active = 0
    for row in basis:
        active |= row
    graph = {i: set() for i in range(width) if active >> i & 1}
    for row in basis:
        pivot = row.bit_length() - 1
        for i in graph:
            if i != pivot and row >> i & 1:
                graph[pivot].add(i)
                graph[i].add(pivot)
    components = []
    while graph:
        start = min(graph)
        pending, seen = [start], {start}
        while pending:
            for i in graph[pending.pop()]:
                if i not in seen:
                    pending.append(i)
                    seen.add(i)
        components.append(sum(1 << i for i in seen))
        for i in seen:
            del graph[i]
    for block in components:
        assert len(_row_basis((*basis, *(row & block for row in basis)), width)) == len(basis)
    assert sum(len(_row_basis((row & block for row in basis), width)) for block in components) == len(basis)
    return tuple(components)


def selected_schur_subcode_certificate(rows, width, physical_directions):
    R, W = _binary_code(rows, width), tuple(physical_directions)
    t, n = len(W), len(R)
    if not t or len(_row_basis(W, width)) != t or any((b & w).bit_count() % 2 for b in R for w in W):
        raise ValueError("independent physical directions in the binary kernel required")
    unit = (1 << width) - 1
    U = _row_basis((unit, *W), width)
    S = _row_basis((*R, *(b & w for b in R for w in W)), width)
    active = 0
    for b in R:
        active |= b
    p = len(_row_basis((u & active for u in U), width))
    blocks = _code_components(S, width)
    r = len(S) - n
    assert len(S) >= n + p - len(blocks)
    columns = tuple(sum((b >> i & 1) << l for l, b in enumerate(R)) for i in range(width))
    records = []
    for block in blocks:
        Rdim = len(_row_basis((b & block for b in R), width))
        Sdim = len(_row_basis((s & block for s in S), width))
        signatures = {columns[i] for i in range(width) if block >> i & 1}
        assert 0 not in signatures and len(signatures) <= (1 << Rdim) - 1
        records.append({"physical_component_mask_hex": hex(block), "dual_projection_rank": Rdim,
                        "product_projection_rank": Sdim, "nonzero_signatures_in_component": len(signatures)})
    gate = universal_signature_gate(R, width, t, r)
    assert not gate["every_t_dimensional_physical_kernel_subspace_with_extension_rank_at_most_r_excluded"]
    return {"status": "EXACT_SELECTED_SCHUR_PRODUCT_AND_STABILIZER_DECOMPOSITION",
            "parity_rows_hex": [hex(x) for x in R], "physical_directions_hex": [hex(x) for x in W],
            "physical_width": width, "pivot_dimension": t, "product_space_basis_hex": [hex(x) for x in S],
            "product_space_dimension": len(S), "extension_rank": r,
            "active_unit_augmented_subcode_dimension": p, "product_stabilizer_component_count": len(blocks),
            "kneser_dimension_slack": len(S) - n - p + len(blocks),
            "components": records, "signature_gate_at_actual_extension_rank": gate,
            "product_stabilizer_is_a_quantum_clifford_stabilizer": False,
            "nonsingular_pencil_inverse_or_decoder_implemented": False,
            "candidate_record_accepted": False, "speedup_claim_allowed": False}


def _signature_subspace_envelope(n, k, r):
    # The worst case allows the all-one vector in W; no parity conditioning.
    components, capacity = signature_capacity(n, r, n)
    envelope_bits = (n + 1) * (n + r) + (n + r - 1).bit_length()
    ceil_log_capacity = (capacity - 1).bit_length()
    if capacity <= (1 << (n - 1)):
        decay_bits = k * (n - ceil_log_capacity)
        tail_mass_control = "capacity/2^n <= 2^(-n+ceil_log2(capacity))"
    elif 4 * capacity <= 3 * (1 << n):
        decay_bits = 2 * (k // 5)
        tail_mass_control = "capacity/2^n <= 3/4; (3/4)^5 < 1/4"
    else:
        decay_bits = 0
        tail_mass_control = "no nonvacuous dyadic tail cover bound implemented"
    return {"parity_free_signature_capacity_decimal": str(capacity),
            "required_component_count_lower_bound": components,
            "ordered_subspace_envelope_count_binary_exponent_upper_bound": envelope_bits,
            "tail_coverage_decay_binary_exponent_lower_bound": decay_bits,
            "tail_coverage_bound": tail_mass_control,
            "envelope_probability_dyadic_exponent_before_rounding": decay_bits - envelope_bits,
            "all_one_kernel_vector_exception_needed": False,
            "every_required_signature_space_counted_not_each_signature_individually": True}


def _conservative_dyadic(exponent, precision):
    return Fraction(1, 1 << min(exponent, precision)) if exponent > 0 else Fraction(1)


def native_low_variation_source_bound(n, tail_columns, extension_rank_budget):
    k, r = tail_columns, extension_rank_budget
    if any(type(x) is not int for x in (n, k, r)) or n < 1 or k < n or not 0 <= r <= n:
        raise ValueError("positive n, at least n IID tail columns, and rank budget in [0,n] required")
    N, m = 1 << n, n + k
    components, capacity = signature_capacity(n, r, n + 1)
    exceptional = Fraction(k + 1, N)
    expected_pairs = Fraction(k * (k - 1) // 2 + n * k, N)
    if capacity == 0:
        signature_mass, collision_mass, cover_mass, cover_exponent = Fraction(0), Fraction(0), Fraction(0), None
    else:
        deficit = max(0, m - capacity)
        collision_mass = min(Fraction(1), expected_pairs / deficit) if deficit else Fraction(1)
        extra = max(0, capacity - n)
        ceil_log_capacity = (capacity - 1).bit_length()
        cover_exponent = n * (k - extra) - k * ceil_log_capacity
        # Round UP to 2^-n once smaller than the already charged parity event.
        # This keeps the bound polynomial-size while retaining exponential decay.
        cover_mass = Fraction(1, 1 << min(n, cover_exponent)) if cover_exponent > 0 else Fraction(1)
        signature_mass = min(collision_mass, cover_mass)
    envelope = _signature_subspace_envelope(n, k, r)
    envelope_mass = _conservative_dyadic(envelope["envelope_probability_dyadic_exponent_before_rounding"], n)
    parity_free_bound = min(Fraction(1), Fraction(k, N) + envelope_mass)
    bound = min(Fraction(1), exceptional + signature_mass, parity_free_bound)
    return {"status": "NATIVE_ALL_SUBCODE_LOW_VARIATION_EXISTENCE_PROBABILITY_UPPER_BOUND",
            "dimension": n, "iid_uniform_binary_tail_columns": k, "original_packet_states": m,
            "extension_rank_budget": r, "conditional_source": "binary identity prefix plus IID uniform tail; justified by low-only native row transport",
            "required_product_component_count_if_no_zero_columns_and_odd_row_parity": components,
            "nonzero_signature_capacity_if_no_zero_columns_and_odd_row_parity_decimal": str(capacity),
            "zero_column_or_all_even_row_parity_union_upper_bound": exact(min(Fraction(1), exceptional)),
            "expected_equal_signature_pair_count": exact(expected_pairs),
            "distinct_signature_deficit_if_capacity_below_packet_width": max(0, m - capacity),
            "collision_markov_signature_event_upper_bound": exact(collision_mass),
            "signature_cover_dyadic_exponent_before_conservative_rounding": cover_exponent,
            "signature_cover_event_upper_bound": exact(cover_mass),
            "signature_event_upper_bound": exact(signature_mass),
            "parity_free_subspace_envelope": envelope,
            "parity_free_envelope_probability_upper_bound": exact(envelope_mass),
            "zero_column_or_parity_free_low_variation_family_probability_upper_bound": exact(parity_free_bound),
            "final_bound_is_minimum_of_two_valid_source_arguments": True,
            "exists_any_n_dimensional_kernel_subcode_with_extension_rank_at_most_r_probability_upper_bound": exact(bound),
            "subcode_search_may_use_all_public_higher_labels": True,
            "independence_of_exceptional_events_assumed": False,
            "all_code_subspaces_enumerated": False,
            "general_nonsingular_pencils_or_full_quantum_algorithms_excluded": False,
            "candidate_record_accepted": False, "speedup_claim_allowed": False}


def native_adaptive_pool_bound(n, tail_columns, extension_rank_budget, pool_states):
    fixed = native_low_variation_source_bound(n, tail_columns, extension_rank_budget)
    m = n + tail_columns
    if type(pool_states) is not int or pool_states < m:
        raise ValueError("preallocated IID original-state pool must contain a whole packet")
    menu_bits = m * (pool_states - 1).bit_length()
    exponent = fixed["parity_free_subspace_envelope"]["envelope_probability_dyadic_exponent_before_rounding"] - menu_bits
    family_mass = _conservative_dyadic(exponent, n)
    zero_mass = min(Fraction(1), Fraction(pool_states, 1 << n))
    bound = min(Fraction(1), zero_mass + family_mass)
    return {"status": "ADAPTIVE_POOL_REGROUPING_LOW_VARIATION_PROBABILITY_UPPER_BOUND",
            "dimension": n, "packet_states": m, "iid_original_pool_states": pool_states,
            "extension_rank_budget": extension_rank_budget,
            "ordered_packet_menu_count_binary_exponent_upper_bound": menu_bits,
            "envelope_mass_exponent_after_charging_all_ordered_packet_menus": exponent,
            "any_zero_binary_label_in_entire_pool_probability_upper_bound": exact(zero_mass),
            "any_full_rank_selected_packet_low_variation_family_probability_upper_bound": exact(family_mass),
            "existence_probability_upper_bound_including_global_zero_label_exception": exact(bound),
            "arbitrary_public_label_adaptive_grouping_permitted": True,
            "rows_may_be_normalized_from_selected_invertible_binary_prefix": True,
            "zero_label_exception_is_charged_once_on_entire_pool_not_once_per_menu": True,
            "selected_packet_uses_distinct_original_registers": True,
            "same_label_copies_or_non_native_phase_sources_granted": False,
            "rank_deficient_output_or_variable_packet_size_protocols_covered": False,
            "candidate_record_accepted": False, "speedup_claim_allowed": False}


def identity_pencil_middle_source_mass(n):
    if type(n) is not int or n < 2:
        raise ValueError("n>=2 required for the two nonsingular matrices control")
    prefix_mass = math.prod(1 - Fraction(1, 1 << j) for j in range(1, n + 1))
    denominator, fixed_point_free_mass = 1, Fraction(1)
    for j in range(1, n + 1):
        denominator *= (1 << j) - 1
        fixed_point_free_mass += Fraction((-1) ** j, denominator)
    mass = prefix_mass * fixed_point_free_mass
    assert mass >= Fraction(9, 112)
    return {"status": "POSITIVE_IDENTITY_PENCIL_MIDDLE_SOURCE_CONTROL_NOT_NATIVE_LOW_FAMILY",
            "dimension": n, "variation_space": "span{I_n}; two background matrices M0 and M0+I_n",
            "uniform_constant_matrix_all_background_invertibility_probability": exact(mass),
            "conditional_fixed_point_free_probability_inside_GL_n": exact(fixed_point_free_mass),
            "uniform_constant_matrix_acceptance_lower_bound_for_n_at_least_two": exact(Fraction(9, 112)),
            "constant_matrix_native_law_requires_W_selected_before_middle_labels": True,
            "middle_label_acceptance_is_exponentially_small": False,
            "structured_binary_low_signature_is_a_nonrare_native_family": False,
            "general_pencil_or_higher_carry_decoder_implemented": False,
            "candidate_record_accepted": False, "speedup_claim_allowed": False}


def run_controls():
    source = json.loads((ROOT / "research/phase_workbench/dcp_pivot_span_obstructions.json").read_text())
    controls = []
    for row in [source["native_correlated_positive_packet"], *source["systematic_actual_packet_operator_profiles"]]:
        A = row["provenance"]["labels"]
        width = len(A[0])
        R = tuple(sum((a & 1) << i for i, a in enumerate(component)) for component in A)
        W = [int(x, 16) for x in row["physical_code_schur_certificate"]["physical_pivot_directions_hex"]]
        selected = selected_schur_subcode_certificate(R, width, W)
        assert selected["extension_rank"] == row["physical_code_schur_certificate"]["polar_variation_dimension"]
        controls.append(selected)
    structured = []
    for n in (2, 4, 8):
        width = 2 * n + 1
        outside = 1 << (2 * n)
        R = tuple((1 << j) | (1 << (n + j)) | outside for j in range(n))
        W = tuple((1 << j) | (1 << (n + j)) for j in range(n))
        record = selected_schur_subcode_certificate(R, width, W)
        assert record["extension_rank"] == 1
        record["literal_systematic_tail_signature_source_probability"] = exact(Fraction(1, 1 << (n * (n + 1))))
        structured.append(record)
    return {"status": "LOCAL_DERIVATION_REVIEW_PENDING", "actual_selected_packet_subcodes": controls,
            "structured_rank_one_positive_controls": structured,
            "identity_pencil_middle_source_controls": [identity_pencil_middle_source_mass(n) for n in (2, 3, 4, 8, 16, 32)],
            "native_source_scaling_bounds": [native_low_variation_source_bound(n, 4 * n * n + 16, r)
                                            for n, r in ((8, 1), (16, 1), (24, 1), (32, 1), (32, 5), (32, 6),
                                                         (32, 15), (64, 7), (64, 31))],
            "adaptive_pool_bounds": [native_adaptive_pool_bound(n, 4 * n * n + 16, r, n ** 4)
                                     for n, r in ((32, 4), (32, 15), (64, 16), (128, 32))],
            "claim_gate": {"low_variation_gate_covers_every_physical_kernel_subspace": True,
                           "zero_columns_and_all_one_kernel_exceptions_charged": True,
                           "rank_one_native_family_cannot_be_promoted_from_small_positive_control": True,
                           "all_larger_correlated_pencils_or_background_adaptive_pivots_excluded": False,
                           "new_quantum_decoder_or_speedup": False, "independent_theorem_review": False,
                           "candidate_record_accepted": False, "novelty_claim": False, "speedup_claim_allowed": False},
            "dependency_sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                                  for p in (Path(__file__), ROOT / "theorems/dcp_pivot_span_obstructions.py",
                                            ROOT / "theorems/dcp_systematic_source_transport.py",
                                            ROOT / "research/phase_workbench/dcp_pivot_span_obstructions.json")}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--save", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.save:
        REPORT.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"status": report["status"], "claim_gate": report["claim_gate"]}, indent=2))


if __name__ == "__main__":
    main()
