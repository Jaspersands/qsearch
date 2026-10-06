"""Conditional fresh carry-bit source in compact physical Boolean features.

LOCAL DERIVATION / REVIEW PENDING. No iterated decoder or accepted candidate.
Source identities require features/offsets chosen before the fresh label bits.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import random
from collections import Counter
from dataclasses import replace
from fractions import Fraction
from pathlib import Path

from dcp_bell_inference_kernel import exact
from dcp_boolean_phase_pullback import BooleanANFMap
from dcp_carry_packets import compile_packet, greedy_common_isotropic, isotropic_readout_rows, single_packet_conductor_radical
from dcp_lowbit_fiber_normalizer import _anf, _apply_rows, _columns_value, _independent_extension, _inverse_rows, compile_normalizer

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/dcp_conditional_carry_features.json"


def _xor_terms(*polynomials):
    terms = set()
    for polynomial in polynomials:
        terms.symmetric_difference_update(polynomial)
    return tuple(sorted(terms))


def _translate(terms, direction, expansion_cap=100000):
    result, work = set(), 0
    for mask in terms:
        fixed, shifted = mask & ~direction, mask & direction
        work += 1 << shifted.bit_count()
        if work > expansion_cap:
            raise ValueError("explicit ANF translation exceeds charged expansion cap")
        subset = shifted
        while True:
            term = fixed | subset
            if term in result:
                result.remove(term)
            else:
                result.add(term)
            if subset == 0:
                break
            subset = (subset - 1) & shifted
    return tuple(sorted(result))


def _mixed_derivative(terms, u, v, expansion_cap=100000):
    return _xor_terms(terms, _translate(terms, u, expansion_cap),
                      _translate(terms, v, expansion_cap), _translate(terms, u ^ v, expansion_cap))


def _solve(equations, width):
    """Sparse binary elimination; includes an explicit consistency witness."""
    pivots, consistent = {}, True
    for coefficients, rhs in equations:
        coefficients, rhs = int(coefficients), int(rhs)
        if not 0 <= coefficients < 1 << width or rhs not in (0, 1):
            raise ValueError("valid binary linear equation required")
        for p in sorted(pivots, reverse=True):
            if coefficients >> p & 1:
                row, bit = pivots[p]
                coefficients ^= row
                rhs ^= bit
        if not coefficients:
            if rhs:
                consistent = False
        else:
            pivots[coefficients.bit_length() - 1] = (coefficients, rhs)
    if not consistent:
        return len(pivots), None
    solution = 0
    for p in sorted(pivots):
        row, bit = pivots[p]
        if bit ^ ((row & solution).bit_count() & 1):
            solution |= 1 << p
    return len(pivots), solution


def _coefficient_rows(functions):
    masks = sorted({mask for terms in functions for mask in terms})
    return {mask: sum((mask in terms) << i for i, terms in enumerate(functions)) for mask in masks}


def conditional_bit_source_certificate(features, offsets, *, selected_before_fresh_bits=False):
    if type(selected_before_fresh_bits) is not bool:
        raise ValueError("Boolean prior-selection declaration required")
    if features.input_bits != offsets.input_bits:
        raise ValueError("matching public feature and carry-offset domains required")
    rows = _coefficient_rows(features.outputs)
    m, n, d = len(features.outputs), len(offsets.outputs), features.input_bits
    rank, _ = _solve([(row, 0) for row in rows.values()], m)
    nonlinear_rank, _ = _solve([(row, 0) for mask, row in rows.items() if mask.bit_count() >= 2], m)
    recovery = []
    for j in range(d):
        _, solution = _solve([(rows.get(mask, 0), int(mask == 1 << j))
                              for mask in sorted(set(rows) | {1 << j})], m)
        if solution is None:
            break
        recovery.append(solution)
    injective = len(recovery) == d
    return {"status": "CONDITIONAL_FEATURE_SOURCE_NOT_NATIVE_QUADRATIC_RESTART",
            "input_bits": d, "physical_feature_count": m, "output_dimension": n,
            "feature_function_space_rank": rank,
            "nonlinear_feature_function_space_rank": nonlinear_rank,
            "conditional_distinct_functions_per_output_row": hex(1 << rank),
            "each_row_function_has_equal_fresh_label_multiplicity": hex(1 << (m - rank)),
            "fresh_bit_law": "next(r)=carry(r) XOR H_fresh*physical_features(r)",
            "features_and_carry_selected_before_fresh_labels_as_declared": selected_before_fresh_bits,
            "conditional_source_identity_usable_as_declared": selected_before_fresh_bits,
            "lineage_declaration_is_programmatically_proved": False,
            "iid_uniform_fresh_label_matrix_independent_of_all_lower_data_required": True,
            "linear_feature_recovery_proves_injectivity": injective,
            "linear_recovery_rows_hex": [hex(x) for x in recovery] if injective else None,
            "failure_to_find_linear_recovery_proves_noninjectivity": False,
            "full_cube_uniform_input_mean_residue_chi_squared": exact(Fraction((1 << n) - 1, 1 << d)) if injective else None,
            "histogram_moment_requires_full_cube_uniform_domain_and_prior_selection": True,
            "fresh_label_bits_are_iid_random_ANF_coefficients": False,
            "feature_resources": features.resource_upper_bound(),
            "carry_resources": offsets.resource_upper_bound(),
            "candidate_record_accepted": False, "speedup_claim_allowed": False}


def fixed_direction_affine_gate(features, offsets, directions, *, selected_before_fresh_bits=False,
                                expansion_cap=100000):
    if type(selected_before_fresh_bits) is not bool:
        raise ValueError("Boolean prior-selection declaration required")
    d, m, n = features.input_bits, len(features.outputs), len(offsets.outputs)
    if offsets.input_bits != d or not directions or any(type(u) is not int or not 0 < u < 1 << d for u in directions):
        raise ValueError("matching domains and nonzero valid directions required")
    rank, _ = _solve([(u, 0) for u in directions], d)
    if rank != len(directions):
        raise ValueError("independent retained directions required")
    equations = [[] for _ in range(n)]
    for u, v in itertools.combinations(directions, 2):
        derivatives = [_mixed_derivative(terms, u, v, expansion_cap) for terms in features.outputs]
        coefficients = _coefficient_rows(derivatives)
        for l, terms in enumerate(offsets.outputs):
            carry = set(_mixed_derivative(terms, u, v, expansion_cap))
            for mask in sorted(set(coefficients) | carry):
                equations[l].append((coefficients.get(mask, 0), int(mask in carry)))
    solved = [_solve(row, m) for row in equations]
    consistent = all(solution is not None for _, solution in solved)
    source_mass = Fraction(1, 1 << sum(r for r, _ in solved)) if consistent else Fraction(0)
    return {"status": "EXACT_FIXED_DIRECTION_FRESH_BIT_AFFINENESS_GATE",
            "directions_hex": [hex(u) for u in directions],
            "all_backgrounds_and_all_retained_assignments_required": True,
            "fresh_label_constraint_ranks": [r for r, _ in solved],
            "source_constraints_consistent": consistent,
            "exact_fixed_direction_affine_source_mass": exact(source_mass),
            "source_universal_affine_on_these_directions": source_mass == 1,
            "fresh_bit_source_mass_usable_as_declared": selected_before_fresh_bits,
            "directions_features_and_offsets_must_precede_fresh_H": True,
            "fresh_H_adaptive_direction_search_source_mass_covered": False,
            "higher_layer_decoder_or_general_quantum_no_go": False,
            "explicit_derivative_equations": [len(row) for row in equations],
            "translation_expansion_cap_per_polynomial": expansion_cap,
            "expansion_polynomial_at_unbounded_ANF_degree": False,
            "candidate_record_accepted": False, "speedup_claim_allowed": False}


def constant_pivot_radical_gate(packet):
    if packet.modulus < 8 or packet.syndrome or len(packet.pivots) != packet.dimension:
        raise ValueError("full-rank zero-origin packet with q>=8 required")
    base = compile_packet([[a & 1 for a in row] for row in packet.labels], 4)
    radical = single_packet_conductor_radical(base)
    return {"status": "COMMON_ISOTROPIC_GLOBALLY_CONSTANT_PIVOT_NECESSITY",
            "low_labels": [[a & 1 for a in row] for row in packet.labels],
            "dimension": packet.dimension, "logical_width": packet.retained_qubits,
            "common_binary_quadratic_radical_dimension": len(radical),
            "radical_directions_hex": [hex(u) for u in radical],
            "n_independent_globally_constant_pivot_directions_not_excluded": len(radical) >= packet.dimension,
            "necessary_condition_is_a_rank_or_decoder_sufficiency_proof": False,
            "requires_isotropic_U_and_constant_pivot_coefficients_on_every_complement": True,
            "connected_fundamental_graph_bounds_common_radical_by_one": True,
            "adaptive_pivots_or_nonisotropic_constructions_ruled_out": False,
            "fixed_but_background_varying_nonsingular_pivot_pencils_ruled_out": False,
            "candidate_record_accepted": False, "speedup_claim_allowed": False}


def _matrix_columns(rows):
    n = len(rows)
    return tuple(sum((row >> j & 1) << i for i, row in enumerate(rows)) for j in range(n))


def _matrix_flat(rows):
    return sum(column << (len(rows) * j) for j, column in enumerate(_matrix_columns(rows)))


def pivot_pencil_coverage_certificate(constant_rows, variation_rows):
    """Exact background-image test, without enumerating background values.

    The input pencil must describe the ACTUAL selected chart. A singular
    background does not imply a large failure fraction or a decoder no-go.
    """
    constant_rows, variation_rows = tuple(constant_rows), tuple(tuple(M) for M in variation_rows)
    n = len(constant_rows)
    if not n or any(len(M) != n or any(type(row) is not int or not 0 <= row < 1 << n for row in M)
                    for M in (constant_rows, *variation_rows)):
        raise ValueError("valid square binary constant and variation matrices required")
    image_rank, _ = _solve([(_matrix_flat(M), 0) for M in variation_rows], n * n)
    column_ranks = [_solve([(_matrix_columns(M)[j], 0) for M in variation_rows], n)[0] for j in range(n)]
    separable = image_rank == sum(column_ranks)
    rank0 = _solve([(row, 0) for row in constant_rows], n)[0]
    bad_background, null_vector, cycle = None, None, None
    globally_invertible, fraction = False, None
    if rank0 != n:
        bad_background = 0
    elif separable:
        inverse = _inverse_rows(constant_rows)
        normalized_columns = [tuple(_apply_rows(inverse, column) for column in _matrix_columns(M)) for M in variation_rows]
        graph = [sorted({i for M in normalized_columns for i in range(n) if M[j] >> i & 1}) for j in range(n)]
        cycles = []
        for start in range(n):
            pending, visited = [[start]], {start}
            while pending:
                path = pending.pop(0)
                successors = graph[path[-1]]
                if start in successors:
                    cycles.append(path)
                    break
                for next_vertex in successors:
                    if next_vertex not in visited:
                        visited.add(next_vertex)
                        pending.append(path + [next_vertex])
        if not cycles:
            globally_invertible, fraction = True, Fraction(1)
        else:
            cycle = min(cycles, key=lambda path: (len(path), path))
            desired_columns = [0] * n
            for j, next_vertex in zip(cycle, cycle[1:] + cycle[:1]):
                generator = next(i for i, M in enumerate(normalized_columns) if M[j] >> next_vertex & 1)
                desired_columns[j] = _matrix_columns(variation_rows[generator])[j]
            desired = sum(column << (n * j) for j, column in enumerate(desired_columns))
            flattened = [_matrix_flat(M) for M in variation_rows]
            equations = [(sum((M >> bit & 1) << i for i, M in enumerate(flattened)), desired >> bit & 1)
                         for bit in range(n * n)]
            _, bad_background = _solve(equations, len(variation_rows))
            assert bad_background is not None
    if image_rank == n * n:
        fraction = math.prod(1 - Fraction(1, 1 << j) for j in range(1, n + 1))
    elif image_rank == 0:
        fraction = Fraction(rank0 == n)
    if bad_background is not None:
        actual = constant_rows
        for i, M in enumerate(variation_rows):
            if bad_background >> i & 1:
                actual = tuple(a ^ b for a, b in zip(actual, M))
        assert _solve([(row, 0) for row in actual], n)[0] < n
        for j in range(n):
            _, solution = _solve([*((row, 0) for row in actual), (1 << j, 1)], n)
            if solution is not None:
                null_vector = solution
                break
        assert null_vector and _apply_rows(actual, null_vector) == 0
    return {"status": "EXACT_SELECTED_BINARY_PIVOT_PENCIL_COVERAGE_NOT_DECODER_BOUND",
            "constant_matrix_rows": constant_rows, "variation_generator_rows": variation_rows,
            "dimension": n, "background_bits": len(variation_rows),
            "constant_matrix_rank": rank0, "background_matrix_image_rank": image_rank,
            "individual_column_variation_ranks": column_ranks,
            "background_image_is_cartesian_product_of_column_spaces": separable,
            "all_columns_vary_and_separability_rules_out_every_constant_part": separable and all(column_ranks),
            "all_backgrounds_invertible_certified": globally_invertible,
            "exact_uniform_background_invertibility_fraction": exact(fraction) if fraction is not None else None,
            "singular_background_mask_hex": hex(bad_background) if bad_background is not None else None,
            "singular_matrix_nonzero_kernel_vector_hex": hex(null_vector) if null_vector is not None else None,
            "shortest_normalized_variation_cycle": cycle,
            "backgrounds_enumerated_by_certificate": False,
            "actual_native_chart_or_source_prevalence_proved_by_matrix_input": False,
            "one_singular_background_proves_large_failure_mass": False,
            "approximate_transport_or_general_algorithms_ruled_out": False,
            "candidate_record_accepted": False, "speedup_claim_allowed": False}


def packet_pivot_pencil_certificate(packet, isotropic_directions, pivot_indices=None):
    if packet.modulus < 8 or packet.syndrome or len(packet.pivots) != packet.dimension:
        raise ValueError("full-rank zero-origin packet with q>=8 required")
    n, k, U = packet.dimension, packet.retained_qubits, tuple(isotropic_directions)
    pivots = tuple(range(n)) if pivot_indices is None else tuple(pivot_indices)
    if len(U) < n or len(pivots) != n or len(set(pivots)) != n or any(type(i) is not int or not 0 <= i < len(U) for i in pivots):
        raise ValueError("n distinct valid pivot indices in a large enough isotropic chart required")
    low_packet = compile_packet([[a % 4 for a in row] for row in packet.labels], 4)
    slopes0 = isotropic_readout_rows(low_packet, U)
    V = _independent_extension(U, k)[len(U):]
    constant = tuple(sum((slopes0[j] >> l & 1) << h for h, j in enumerate(pivots)) for l in range(n))
    variations = []
    for v in V:
        c = low_packet.residual(v)
        slopes = [sum((a ^ b) << l for l, (a, b) in enumerate(zip(low_packet.residual(v ^ U[j]), c)))
                  for j in pivots]
        matrix = tuple(sum((slope >> l & 1) << h for h, slope in enumerate(slopes)) for l in range(n))
        variations.append(tuple(a ^ b for a, b in zip(matrix, constant)))
    report = pivot_pencil_coverage_certificate(constant, variations)
    report.update({"actual_packet_first_residue_plane_pencil_extracted": True,
                   "logical_width": k, "isotropic_width": len(U),
                   "isotropic_directions_hex": [hex(u) for u in U],
                   "complement_directions_hex": [hex(v) for v in V], "pivot_indices": pivots,
                   "actual_native_selection_prevalence_and_iteration_success_verified": False})
    return report


def _systematic_packet_pencil_profiles():
    rng, records = random.Random(20261004), []
    for n in (2, 3, 4):
        q, k = 1 << (4 * n + 1), 4 * n * n + 16
        A = [[(int(l == i) + 2 * rng.randrange(q // 2)) if i < n else rng.randrange(q)
              for i in range(n + k)] for l in range(n)]
        packet = compile_packet(A, q)
        low = compile_packet([[a & 1 for a in row] for row in A], 4)
        U = greedy_common_isotropic(low)
        record = packet_pivot_pencil_certificate(packet, U)
        record.update({"labels": A, "modulus": q,
                       "source": "fixed_identity_binary_prefix_with_fair_systematic_tail_and_native_uniform_higher_labels",
                       "systematic_chart_profile_not_unconditional_source_success_experiment": True,
                       "physical_assignments_or_secret_states_enumerated": False,
                       "finite_profiles_prove_typical_large_n_source_behavior": False})
        records.append(record)
    return records


def _fixed_pivot_control():
    lower = (1, 1, 3, 1, 1, 3)
    packet = compile_packet([lower], 16)
    U, V = (31, 6, 24), (2, 8)
    physical, carry, permutation = [], [], []
    for w in range(32):
        t, r = w & 1, w >> 1
        u1, u2, y = r & 1, r >> 1 & 1, r >> 2
        background = _columns_value(V, y)
        c = packet.residual(background)[0] & 1
        L = [(packet.residual(background ^ u)[0] ^ c) & 1 for u in U]
        assert L[0] == 1
        u0 = t ^ c ^ (L[1] & u1) ^ (L[2] & u2)
        z = background ^ _columns_value(U, u0 | (u1 << 1) | (u2 << 2))
        permutation.append(z)
        if t == 0:
            x = packet.assignment(z)
            value = sum(a * b for a, b in zip(lower, x))
            assert value % 4 == 0
            physical.append(x)
            carry.append(value // 4 & 1)
    assert sorted(permutation) == list(range(32))
    features = BooleanANFMap(4, tuple(_anf([x[i] for x in physical]) for i in range(6)))
    offsets = BooleanANFMap(4, (_anf(carry),))
    certificate = conditional_bit_source_certificate(features, offsets, selected_before_fresh_bits=True)
    functions, weights, derivatives, total_chi = Counter(), Counter(), 0, Fraction(0)
    for h in range(64):
        values = tuple(carry[r] ^ (sum((h >> i & 1) * x for i, x in enumerate(physical[r])) & 1) for r in range(16))
        for r, x in enumerate(physical):
            actual = sum((a + 4 * (h >> i & 1)) * b for i, (a, b) in enumerate(zip(lower, x))) // 4 & 1
            assert actual == values[r]
        functions[values] += 1
        weights[sum(values)] += 1
        total_chi += Fraction((16 - 2 * sum(values))**2, 256)
        assert max(mask.bit_count() for mask in _anf(values)) == 4
        for u, v in itertools.combinations(range(1, 16), 2):
            assert any(values[r] ^ values[r ^ u] ^ values[r ^ v] ^ values[r ^ u ^ v] for r in range(16))
            derivatives += 1
    assert len(functions) == 32 and set(functions.values()) == {2}
    assert total_chi / 64 == Fraction(1, 16)
    gates = [fixed_direction_affine_gate(features, offsets, (u, v), selected_before_fresh_bits=True)
             for u, v in itertools.combinations(range(1, 16), 2)]
    assert all(not row["source_constraints_consistent"] for row in gates)
    return {"lower_labels": [lower], "modulus": 16, "division_binary_exponent": 2,
            "fixed_low_residue": [0], "isotropic_directions_hex": [hex(x) for x in U],
            "complement_directions_hex": [hex(x) for x in V],
            "globally_constant_pivot_coefficient": 1,
            "bounded_normalized_to_logical_permutation": permutation,
            "physical_features_anf_hex": [[hex(mask) for mask in terms] for terms in features.outputs],
            "carry_offset_anf_hex": [[hex(mask) for mask in terms] for terms in offsets.outputs],
            "conditional_source_certificate": certificate,
            "all_fresh_label_bit_tables": 64, "distinct_next_bit_functions": len(functions),
            "each_next_bit_function_source_multiplicity": 2,
            "all_source_Hamming_weight_histogram": {str(w): count for w, count in sorted(weights.items())},
            "exact_mean_next_bit_histogram_chi_squared": exact(total_chi / 64),
            "all_fresh_functions_have_degree_four": True,
            "degree_four_persists_without_adaptive_pivots": True,
            "full_cube_top_coefficient_forces_odd_weight_and_unbalanced_functions": True,
            "exact_one_bit_permutation_normalizer_possible_for_this_complete_domain": False,
            "all_background_second_derivative_direction_pairs_per_source": 105,
            "complete_source_direction_pairs_checked": derivatives,
            "fixed_direction_affine_gates": gates,
            "other_parameterizations_approximate_normalizers_or_general_algorithms_excluded": False}


def _adaptive_feature_countercontrol():
    maps = []
    for h in range(4):
        direction = next(v for v in range(1, 4) if (h & v).bit_count() % 2 == 0)
        assert direction != 0 and ((h & direction).bit_count() & 1) == 0
        maps.append({"fresh_label_mask": h, "chosen_physical_direction": direction,
                     "feature_map_is_injective": True, "output_values": [0, 0]})
    return {"all_fresh_label_tables": maps, "actual_mean_histogram_chi_squared": exact(1),
            "invalid_fixed_feature_injective_formula": exact(Fraction(1, 2)),
            "fresh_label_adaptive_feature_selection_falsifies_prior_selection_assumption": True,
            "algorithm_candidate": False}


def _nonconstant_pivot_pencil_control():
    B = ((1, 0, 1, 0, 1), (0, 1, 0, 1, 1))
    base = compile_normalizer(compile_packet(B, 8))
    assert base.isotropic_directions == (1, 2) and base.basis_columns == (1, 2, 4)
    histogram, first_matrix_histogram = Counter(), Counter()
    for middle in range(1 << 10):
        labels = tuple(tuple(B[l][i] + 2 * (middle >> (5 * l + i) & 1) for i in range(5)) for l in range(2))
        normalizer = replace(base, packet=replace(base.packet, labels=labels))
        plans = [normalizer.background_plan(y) for y in range(2)]
        M0, M1 = [row["residue_bit_rows"] for row in plans]
        assert M1 == (M0[0] ^ 1, M0[1] ^ 2)
        histogram[sum(p["full_residue_bit_rank"] for p in plans)] += 1
        first_matrix_histogram[M0] += 1
    assert len(first_matrix_histogram) == 16 and set(first_matrix_histogram.values()) == {64}
    assert histogram == {0: 384, 1: 512, 2: 128}
    A = ((1, 0, 3, 2, 1), (0, 1, 2, 1, 1))
    normalizer = compile_normalizer(compile_packet(A, 8))
    plans = [normalizer.background_plan(y) for y in range(2)]
    assert [p["residue_bit_rows"] for p in plans] == [(2, 3), (3, 1)]
    assert all(p["full_residue_bit_rank"] for p in plans)
    outputs = [normalizer.normalize(z) for z in range(8)]
    for z, w in enumerate(outputs):
        assert normalizer.denormalize(w) == z
        assert w & 3 == sum((t & 1) << l for l, t in enumerate(normalizer.packet.residual(z)))
    radical = constant_pivot_radical_gate(normalizer.packet)
    assert radical["common_binary_quadratic_radical_dimension"] == 0
    return {"status": "NATIVE_FIXED_LABEL_MATRIX_PENCIL_COUNTERCONTROL_NOT_SCALABLE_DECODER",
            "low_labels": B, "specific_labels": A, "modulus": 8,
            "logical_width": 3, "isotropic_directions_hex": ["0x1", "0x2"],
            "complement_directions_hex": ["0x4"],
            "pivot_matrix_rows_per_background": [p["residue_bit_rows"] for p in plans],
            "pivot_matrix_is_globally_constant": False,
            "every_background_has_an_invertible_fixed_direction_pivot_matrix": True,
            "common_binary_quadratic_radical_dimension": 0,
            "whole_space_normalization_permutation": outputs,
            "all_middle_label_tables": 1024,
            "number_of_good_backgrounds_source_histogram": {str(x): histogram[x] for x in sorted(histogram)},
            "conditional_all_backgrounds_invertible_probability": exact(Fraction(1, 8)),
            "specified_systematic_low_label_source_probability": exact(Fraction(1, 64)),
            "structured_n_dimensional_low_signature_probability_expression": "2^(-n*(n+1))_for_R=[I_n|1]",
            "selected_low_signature_is_a_polynomial_native_source_family": False,
            "growing_modulus_or_dense_packet_extension_implemented": False,
            "constant_matrix_radical_obstruction_is_a_general_fixed_pivot_no_go": False,
            "abstract_nonsingular_pencil_prior_art": "https://arxiv.org/abs/1405.1575",
            "candidate_record_accepted": False, "speedup_claim_allowed": False}


def run_controls():
    return {"status": "LOCAL_DERIVATION_REVIEW_PENDING",
            "fixed_pivot_conditional_carry_control": _fixed_pivot_control(),
            "constant_pivot_radical_controls": [constant_pivot_radical_gate(compile_packet(B, 8)) for B in
                 ([[1] * 6], [[1, 0, 1, 1, 1, 1], [0, 1, 1, 1, 1, 1]],
                  [[1, 0, 1, 1, 1, 1, 1], [0, 1, 1, 1, 1, 1, 1]])],
            "fresh_H_adaptive_feature_countercontrol": _adaptive_feature_countercontrol(),
            "nonconstant_nonsingular_pivot_pencil_control": _nonconstant_pivot_pencil_control(),
            "pivot_pencil_coverage_controls": [pivot_pencil_coverage_certificate(M0, generators) for M0, generators in
                 (((1, 2), ()), ((1, 2), ((2, 0),)), ((1, 2), ((2, 0), (0, 1))),
                  ((2, 3), ((1, 2),)), ((1, 2), ((1, 0), (2, 0), (0, 1), (0, 2))),
                  ((1, 2, 4), ((0, 1, 0), (0, 0, 2), (4, 0, 0))))],
            "systematic_packet_pencil_profiles": _systematic_packet_pencil_profiles(),
            "claim_gate": {"fresh_carry_features_have_an_explicit_conditional_source_law": True,
                           "first_layer_quartic_failure_is_only_an_adaptive_pivot_artifact": False,
                           "fresh_label_bits_restore_a_native_quadratic_family": False,
                           "fixed_pivot_rank_condition_always_suffices": False,
                           "full_growing_modulus_decoder_implemented": False,
                           "candidate_record_accepted": False, "speedup_claim_allowed": False,
                           "independent_theorem_review": False, "novelty_claim": False},
            "dependency_sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                                  for p in (Path(__file__), ROOT / "theorems/dcp_lowbit_fiber_normalizer.py",
                                            ROOT / "theorems/dcp_carry_packets.py",
                                            ROOT / "theorems/dcp_boolean_phase_pullback.py")}}


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
