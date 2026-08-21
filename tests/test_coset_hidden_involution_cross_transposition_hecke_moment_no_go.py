from fractions import Fraction

from coset_hidden_involution_cross_transposition_hecke_moment_no_go import (
    _direct_degree_four_binary_histogram,
    audit_binary_return_branches,
    audit_cubic_return_branches,
    audit_degree_four_support_catalog,
    audit_transporter_boundary,
    build_cross_transposition_Hecke_moment_report,
    cross_Hecke_moment_control,
    cross_Hecke_scaling_record,
    degree_four_return_branch_control,
    write_cross_transposition_Hecke_moment_report,
)


def test_binary_return_branches_have_exact_all_rank_pattern():
    for half_degree in (3, 4, 5):
        control = audit_binary_return_branches(half_degree)
        expected = (2**half_degree) * __import__("math").factorial(
            half_degree - 2
        )
        assert control.common_centralizer_order == expected
        assert control.expected_common_centralizer_order == expected
        assert control.c_equals_two_count == expected
        assert control.c_equals_one_count == control.centralizer_order - expected
        assert control.c_other_count == 0
        assert control.all_zero_branch_universal
        assert control.only_extra_branch_is_011
        assert control.extra_branch_exactly_common_centralizer
        assert control.exact_binary_return_classification_verified


def test_exact_first_four_moment_formulas():
    for half_degree in (3, 4, 5, 8):
        crossing_index = half_degree * (half_degree - 1)
        for copy_count in (1, 2, 5, 11):
            control = cross_Hecke_moment_control(
                half_degree,
                copy_count,
            )
            assert Fraction(control.first_moment_bias) == Fraction(
                1,
                2**copy_count,
            )
            assert Fraction(control.baseline_second_moment) == Fraction(
                1,
                (2**copy_count) * crossing_index,
            )
            assert Fraction(control.second_moment_bias) == Fraction(
                crossing_index - 1,
                (4**copy_count) * crossing_index,
            )
            assert control.exact_second_moment_formula_verified
            assert Fraction(control.baseline_third_moment) == Fraction(
                1,
                (4**copy_count) * crossing_index**2,
            )
            assert control.exact_third_moment_formula_verified
            branch = degree_four_return_branch_control(half_degree)
            copy_scale = 2**copy_count
            expected_baseline_fourth = Fraction(
                branch.baseline_c_equals_one_path_count
                + branch.baseline_c_equals_two_path_count * copy_scale
                + branch.baseline_c_equals_four_path_count * copy_scale**2,
                copy_scale**3 * crossing_index**3,
            )
            expected_likelihood_fourth = Fraction(
                branch.c_equals_one_path_count
                + branch.c_equals_two_path_count * copy_scale
                + branch.c_equals_four_path_count * copy_scale**2
                + branch.c_equals_eight_path_count * copy_scale**3,
                copy_scale**4 * crossing_index**3,
            )
            assert Fraction(control.baseline_fourth_moment) == (
                expected_baseline_fourth
            )
            assert Fraction(control.likelihood_fourth_moment) == (
                expected_likelihood_fourth
            )
            assert Fraction(control.fourth_moment_bias) == (
                expected_likelihood_fourth - expected_baseline_fourth
            )
            assert control.exact_fourth_moment_formula_verified


def test_cubic_return_branches_reduce_to_unaffected_pair_switches():
    for half_degree in (3, 4, 5, 6, 8, 12):
        control = audit_cubic_return_branches(half_degree)
        assert control.switch_neighbour_count == half_degree * (
            half_degree - 1
        )
        assert control.full_product_switch_count == 1 + (
            (half_degree - 2) * (half_degree - 3)
        )
        assert control.c_other_path_count == 0
        assert control.exact_unaffected_switch_classification_verified
        assert control.direct_small_rank_histogram_verified
        assert control.exact_cubic_return_classification_verified


def test_natural_cubic_bias_remains_inverse_candidate_scale():
    for half_degree in (4, 8, 16, 32, 64):
        row = cross_Hecke_scaling_record(half_degree)
        candidates = int(row.conjugacy_class_size_decimal)
        assert row.cubic_unit_coefficient_bias_upper_bound <= (
            3.0 / (64.0 * candidates)
        )
        assert row.cubic_bias_at_most_thrice_inverse_64_candidates
        assert row.relative_second_moment_excess_vanishes


def test_transporter_exists_but_does_not_create_large_degree_four_atom():
    for half_degree in (3, 4, 5, 8, 12):
        control = audit_transporter_boundary(half_degree)
        assert control.matching_walk_length == 3
        assert control.selected_middle_bits == (0, 1, 1)
        assert control.consecutive_switch_path_verified
        assert control.selected_middle_word_transports_H_to_H_crossed
        assert control.three_switch_path_count == 12 * (half_degree - 2)
        assert control.expected_three_switch_path_count == 12 * (
            half_degree - 2
        )
        assert control.total_three_switch_path_count == (
            half_degree * (half_degree - 1)
        ) ** 3
        assert control.exact_transporter_path_count_verified
        assert control.full_subword_cube_size == 32
        assert control.full_subword_product_support_size == 28
        assert control.maximum_full_subword_product_multiplicity == 2
        assert control.identity_full_subword_product_multiplicity == 1
        assert control.maximum_atom_probability == 1.0 / 16.0
        assert not control.one_quarter_concentration_violated
        assert control.six_point_witness_lifts_to_all_higher_ranks


def test_degree_four_support_catalog_is_exact_and_not_interpolated():
    controls = audit_degree_four_support_catalog()
    assert len(controls) == 7
    expected = {
        0: (8, {4: 7, 8: 1}, {2: 2, 4: 1}, 7, 28),
        1: (208, {1: 108, 2: 84, 4: 16}, {1: 8, 2: 8}, 0, 0),
        2: (1304, {1: 1030, 2: 260, 4: 14}, {2: 6}, 6, 6),
        3: (3456, {1: 3120, 2: 336}, {}, 0, 0),
        4: (4512, {1: 4368, 2: 144}, {}, 0, 0),
        5: (2880, {1: 2880}, {}, 0, 0),
        6: (720, {1: 720}, {}, 0, 0),
    }
    for row in controls:
        (
            total,
            histogram,
            baseline_histogram,
            odd_paths,
            odd_occurrences,
        ) = expected[row.active_unaffected_pair_count]
        observed_histogram = {
            count: paths
            for count, paths in (
                (1, row.c_equals_one_path_count),
                (2, row.c_equals_two_path_count),
                (4, row.c_equals_four_path_count),
                (8, row.c_equals_eight_path_count),
            )
            if paths
        }
        assert row.canonical_all_active_path_count == total
        assert observed_histogram == histogram
        observed_baseline_histogram = {
            count: paths
            for count, paths in (
                (1, row.baseline_c_equals_one_path_count),
                (2, row.baseline_c_equals_two_path_count),
                (4, row.baseline_c_equals_four_path_count),
            )
            if paths
        }
        assert observed_baseline_histogram == baseline_histogram
        assert row.odd_identity_path_count == odd_paths
        assert row.odd_identity_occurrence_count == odd_occurrences
        assert row.exact_canonical_support_enumeration_verified


def test_degree_four_all_rank_histogram_and_unique_m4_exception():
    expected = {
        3: {1: 108, 2: 84, 4: 23, 8: 1},
        4: {1: 1240, 2: 434, 4: 53, 8: 1},
        5: {1: 6534, 2: 1368, 4: 97, 8: 1},
        8: {1: 162018, 2: 13284, 4: 313, 8: 1},
        12: {1: 2216070, 2: 83100, 4: 797, 8: 1},
    }
    for half_degree, histogram in expected.items():
        row = degree_four_return_branch_control(half_degree)
        observed = {
            1: row.c_equals_one_path_count,
            2: row.c_equals_two_path_count,
            4: row.c_equals_four_path_count,
            8: row.c_equals_eight_path_count,
        }
        assert observed == histogram
        assert row.odd_identity_exception_path_count == (
            6 if half_degree == 4 else 0
        )
        assert row.histogram_sums_to_all_paths
        assert row.baseline_histogram_sums_to_closure_paths
        assert row.support_deletion_bijection_verified
        assert row.exact_degree_four_return_classification_verified

    for half_degree in (3, 4, 5):
        row = degree_four_return_branch_control(half_degree)
        assert _direct_degree_four_binary_histogram(half_degree) == {
            1: row.c_equals_one_path_count,
            2: row.c_equals_two_path_count,
            4: row.c_equals_four_path_count,
            8: row.c_equals_eight_path_count,
        }


def test_degree_four_transporter_term_cancels_and_bias_is_quadratic_in_copy_scale():
    for half_degree in (3, 4, 5, 8, 16, 32):
        branch = degree_four_return_branch_control(half_degree)
        assert branch.c_equals_eight_path_count == (
            branch.baseline_c_equals_four_path_count
        )
        for copy_count in (1, 3, 7, 13):
            control = cross_Hecke_moment_control(
                half_degree,
                copy_count,
            )
            copy_scale = 2**copy_count
            bias = Fraction(control.fourth_moment_bias)
            assert bias <= Fraction(3, copy_scale**2)
            assert control.exact_fourth_moment_formula_verified


def test_natural_quartic_bias_remains_inverse_candidate_scale():
    for half_degree in (4, 8, 16, 32, 64):
        row = cross_Hecke_scaling_record(half_degree)
        candidates = int(row.conjugacy_class_size_decimal)
        assert row.fourth_moment_absolute_bias <= (
            3.0 * row.linear_bias**2 * (1.0 + 1e-15)
        )
        assert row.fourth_bias_at_most_three_over_copy_scale_squared
        assert row.quartic_unit_coefficient_bias_upper_bound <= (
            4.0 / (64.0 * candidates)
        )
        assert row.quartic_bias_at_most_four_times_inverse_64_candidates


def test_report_preserves_degree_five_escape_and_speedup_boundary():
    report = build_cross_transposition_Hecke_moment_report()
    assert report.theorem.exact_common_centralizer_formula_proved
    assert report.theorem.exact_binary_return_classification_proved
    assert report.theorem.exact_all_rank_second_moment_formula_proved
    assert report.theorem.exact_all_rank_third_moment_formula_proved
    assert report.theorem.exact_all_rank_fourth_moment_formula_proved
    assert not report.theorem.normalized_cubic_filter_amplifies_to_constant_bias
    assert not report.theorem.normalized_quartic_filter_amplifies_to_constant_bias
    assert report.theorem.transporter_exclusion_strategy_falsified
    assert report.theorem.three_switch_transporter_mass_formula_proved
    assert report.theorem.all_degree_one_quarter_concentration_proved
    assert report.theorem.higher_interleaved_moment_no_go_proved
    assert not report.theorem.nonlinear_spectral_decoder_constructed
    assert not report.theorem.hidden_involution_detector_constructed
    assert not report.theorem.speedup_claim_allowed
    assert report.theorem.theorem_verified


def test_live_report_is_json_serializable(tmp_path):
    output_path = tmp_path / "cross-transposition-hecke-moment.json"
    payload = write_cross_transposition_Hecke_moment_report(output_path)
    assert output_path.exists()
    assert payload["theorem"]["theorem_verified"]
    assert payload["claim_gate"]["exact_cross_Hecke_first_three_moments_proved"]
    assert payload["claim_gate"]["exact_cross_Hecke_first_four_moments_proved"]
