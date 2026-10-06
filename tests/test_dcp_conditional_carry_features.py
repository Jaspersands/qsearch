from fractions import Fraction

import pytest

from dcp_boolean_phase_pullback import BooleanANFMap
from dcp_carry_packets import compile_packet
from dcp_physical_phase_noise import read
from dcp_conditional_carry_features import (
    _adaptive_feature_countercontrol, _fixed_pivot_control, _mixed_derivative,
    _nonconstant_pivot_pencil_control, _solve, _translate,
    conditional_bit_source_certificate, constant_pivot_radical_gate, fixed_direction_affine_gate,
    pivot_pencil_coverage_certificate,
    packet_pivot_pencil_certificate,
)


def test_sparse_boolean_translation_and_mixed_derivative_are_exact():
    terms = (0, 1, 3, 7)
    original = BooleanANFMap(3, (terms,))
    for u in range(8):
        shifted = BooleanANFMap(3, (_translate(terms, u),))
        for r in range(8):
            assert shifted.evaluate(r) == original.evaluate(r ^ u)
        for v in range(8):
            derivative = BooleanANFMap(3, (_mixed_derivative(terms, u, v),))
            for r in range(8):
                assert derivative.evaluate(r)[0] == (original.evaluate(r)[0] ^ original.evaluate(r ^ u)[0] ^ original.evaluate(r ^ v)[0] ^ original.evaluate(r ^ u ^ v)[0])


def test_linear_constraint_solver_returns_actual_witness_and_detects_conflicts():
    equations = [(3, 1), (6, 0), (4, 1)]
    rank, solution = _solve(equations, 3)
    assert rank == 3
    assert all((mask & solution).bit_count() % 2 == rhs for mask, rhs in equations)
    assert _solve([(1, 0), (1, 1)], 1)[1] is None
    assert _solve([(1, 0), (1, 1), (2, 0)], 2) == (2, None)


def test_physical_linear_recovery_proves_injectivity_without_truth_table_enumeration():
    features = BooleanANFMap(3, ((1,), (2,), (4,), (3,)))
    offsets = BooleanANFMap(3, ((7,), (1, 2)))
    row = conditional_bit_source_certificate(features, offsets, selected_before_fresh_bits=True)
    assert row["linear_feature_recovery_proves_injectivity"]
    assert read(row["full_cube_uniform_input_mean_residue_chi_squared"]) == Fraction(3, 8)
    assert row["feature_function_space_rank"] == 4
    assert not row["fresh_label_bits_are_iid_random_ANF_coefficients"]


def test_failed_linear_recovery_is_not_a_noninjectivity_theorem():
    row = conditional_bit_source_certificate(BooleanANFMap(2, ((3,),)), BooleanANFMap(2, ((),)))
    assert not row["linear_feature_recovery_proves_injectivity"]
    assert not row["failure_to_find_linear_recovery_proves_noninjectivity"]
    assert row["full_cube_uniform_input_mean_residue_chi_squared"] is None


def test_fresh_label_prior_selection_is_an_explicit_required_obligation():
    features, offset = BooleanANFMap(1, ((1,),)), BooleanANFMap(1, ((),))
    assert not conditional_bit_source_certificate(features, offset)["conditional_source_identity_usable_as_declared"]
    counter = _adaptive_feature_countercontrol()
    assert read(counter["actual_mean_histogram_chi_squared"]) > read(counter["invalid_fixed_feature_injective_formula"])
    assert not counter["algorithm_candidate"]


def test_affine_gate_charges_nonuniversal_fresh_source_success():
    features, offsets = BooleanANFMap(2, ((3,),)), BooleanANFMap(2, ((),))
    row = fixed_direction_affine_gate(features, offsets, (1, 2), selected_before_fresh_bits=True)
    assert row["source_constraints_consistent"]
    assert read(row["exact_fixed_direction_affine_source_mass"]) == Fraction(1, 2)
    assert not row["source_universal_affine_on_these_directions"]


def test_affine_gate_retains_nonzero_carry_right_hand_side():
    features, offsets = BooleanANFMap(2, ((3,),)), BooleanANFMap(2, ((3,),))
    row = fixed_direction_affine_gate(features, offsets, (1, 2))
    assert row["source_constraints_consistent"]
    assert read(row["exact_fixed_direction_affine_source_mass"]) == Fraction(1, 2)
    assert not row["fresh_bit_source_mass_usable_as_declared"]


def test_vector_source_gate_charges_every_independent_fresh_label_row():
    features, offsets = BooleanANFMap(2, ((3,),)), BooleanANFMap(2, ((3,), ()))
    row = fixed_direction_affine_gate(features, offsets, (1, 2), selected_before_fresh_bits=True)
    assert row["fresh_label_constraint_ranks"] == [1, 1]
    assert read(row["exact_fixed_direction_affine_source_mass"]) == Fraction(1, 4)


def test_fixed_pivot_high_carry_remains_quartic_for_every_fresh_table():
    row = _fixed_pivot_control()
    assert row["degree_four_persists_without_adaptive_pivots"]
    assert row["all_fresh_label_bit_tables"] == 64
    assert row["distinct_next_bit_functions"] == 32
    assert row["complete_source_direction_pairs_checked"] == 6720
    assert read(row["exact_mean_next_bit_histogram_chi_squared"]) == Fraction(1, 16)
    assert all(read(gate["exact_fixed_direction_affine_source_mass"]) == 0 for gate in row["fixed_direction_affine_gates"])
    assert not row["exact_one_bit_permutation_normalizer_possible_for_this_complete_domain"]
    assert not row["other_parameterizations_approximate_normalizers_or_general_algorithms_excluded"]


def test_global_constant_pivot_requires_enough_common_radical_directions():
    scalar = constant_pivot_radical_gate(compile_packet([[1] * 6], 8))
    assert scalar["common_binary_quadratic_radical_dimension"] == 1
    for B in ([[1, 0, 1, 1, 1, 1], [0, 1, 1, 1, 1, 1]],
              [[1, 0, 1, 1, 1, 1, 1], [0, 1, 1, 1, 1, 1, 1]]):
        row = constant_pivot_radical_gate(compile_packet(B, 8))
        assert row["common_binary_quadratic_radical_dimension"] <= 1
        assert not row["n_independent_globally_constant_pivot_directions_not_excluded"]
        assert not row["adaptive_pivots_or_nonisotropic_constructions_ruled_out"]


def test_nonconstant_nonsingular_pencil_survives_zero_common_radical():
    row = _nonconstant_pivot_pencil_control()
    assert row["common_binary_quadratic_radical_dimension"] == 0
    assert row["every_background_has_an_invertible_fixed_direction_pivot_matrix"]
    assert not row["pivot_matrix_is_globally_constant"]
    assert read(row["conditional_all_backgrounds_invertible_probability"]) == Fraction(1, 8)
    assert read(row["specified_systematic_low_label_source_probability"]) == Fraction(1, 64)
    assert row["number_of_good_backgrounds_source_histogram"] == {"0": 384, "1": 512, "2": 128}
    assert not row["selected_low_signature_is_a_polynomial_native_source_family"]
    assert not row["constant_matrix_radical_obstruction_is_a_general_fixed_pivot_no_go"]


def test_column_separable_cycle_supplies_an_explicit_singular_background():
    row = pivot_pencil_coverage_certificate((1, 2), ((2, 0), (0, 1)))
    assert row["background_image_is_cartesian_product_of_column_spaces"]
    assert row["all_columns_vary_and_separability_rules_out_every_constant_part"]
    assert row["singular_background_mask_hex"] == "0x3"
    assert row["singular_matrix_nonzero_kernel_vector_hex"] == "0x3"
    assert not row["one_singular_background_proves_large_failure_mass"]


def test_correlated_pencil_is_not_rejected_by_a_column_separable_criterion():
    row = pivot_pencil_coverage_certificate((2, 3), ((1, 2),))
    assert not row["background_image_is_cartesian_product_of_column_spaces"]
    assert row["singular_background_mask_hex"] is None
    assert row["exact_uniform_background_invertibility_fraction"] is None


def test_full_matrix_background_image_has_exact_native_binary_rank_fraction():
    row = pivot_pencil_coverage_certificate((1, 2), ((1, 0), (2, 0), (0, 1), (0, 2)))
    assert row["background_matrix_image_rank"] == 4
    assert read(row["exact_uniform_background_invertibility_fraction"]) == Fraction(3, 8)


def test_acyclic_column_variation_is_a_real_positive_global_pencil_certificate():
    row = pivot_pencil_coverage_certificate((1, 2), ((2, 0),))
    assert row["all_backgrounds_invertible_certified"]
    assert read(row["exact_uniform_background_invertibility_fraction"]) == 1
    assert not row["backgrounds_enumerated_by_certificate"]


def test_pencil_certificates_match_every_two_by_two_two_generator_pencil():
    def determinant(rows):
        a, b = rows
        return ((a & 1) * (b >> 1)) ^ ((a >> 1) * (b & 1))
    matrices = [(code & 3, code >> 2) for code in range(16)]
    for constant in matrices:
        for left in matrices:
            for right in matrices:
                row = pivot_pencil_coverage_certificate(constant, (left, right))
                actual = [tuple(c ^ (a if bits & 1 else 0) ^ (b if bits & 2 else 0)
                                for c, a, b in zip(constant, left, right)) for bits in range(4)]
                good = sum(determinant(M) for M in actual)
                if row["all_backgrounds_invertible_certified"]:
                    assert good == 4
                if row["exact_uniform_background_invertibility_fraction"] is not None:
                    assert read(row["exact_uniform_background_invertibility_fraction"]) == Fraction(good, 4)
                if row["singular_background_mask_hex"] is not None:
                    mask = int(row["singular_background_mask_hex"], 16)
                    assert determinant(actual[mask]) == 0
                    v = int(row["singular_matrix_nonzero_kernel_vector_hex"], 16)
                    assert v and all((r & v).bit_count() % 2 == 0 for r in actual[mask])
                if row["all_columns_vary_and_separability_rules_out_every_constant_part"]:
                    assert good < 4


def test_actual_packet_pencil_is_extracted_without_fiber_enumeration():
    packet = compile_packet([[1, 0, 3, 2, 1], [0, 1, 2, 1, 1]], 8)
    row = packet_pivot_pencil_certificate(packet, (1, 2))
    assert row["constant_matrix_rows"] == (2, 3)
    assert row["variation_generator_rows"] == ((1, 2),)
    assert not row["background_image_is_cartesian_product_of_column_spaces"]
    assert row["actual_packet_first_residue_plane_pencil_extracted"]
    assert not row["backgrounds_enumerated_by_certificate"]
    with pytest.raises(ValueError):
        packet_pivot_pencil_certificate(packet, (1, 2), (0, 0))


def test_invalid_directions_domains_and_expansion_budget_rejected():
    features, offset = BooleanANFMap(2, ((3,),)), BooleanANFMap(2, ((),))
    for directions in ((), (0,), (4,), (1, 1), (1, 2, 3)):
        with pytest.raises(ValueError):
            fixed_direction_affine_gate(features, offset, directions)
    with pytest.raises(ValueError):
        conditional_bit_source_certificate(features, BooleanANFMap(1, ((),)))
    with pytest.raises(ValueError):
        _translate((15,), 15, expansion_cap=8)
