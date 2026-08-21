from fractions import Fraction

from coset_hidden_involution_cross_transposition_hecke_degree_five_no_go import (
    degree_five_moment_control,
)
from coset_hidden_involution_cross_transposition_hecke_moment_no_go import (
    _matching_from_edges,
    cross_Hecke_moment_control,
)
from coset_hidden_involution_single_hecke_all_degree_moment_no_go import (
    adjacent_pair_products,
    all_degree_moment_bound_control,
    all_degree_scaling_record,
    audit_adjacent_pair_injection,
    build_all_degree_moment_report,
    ordered_subword_product_histogram,
    write_all_degree_moment_report,
)


def test_distinct_adjacent_involutions_give_four_distinct_bit_products():
    degree = 8
    hidden = _matching_from_edges(
        ((0, 1), (2, 3), (4, 5), (6, 7)),
        degree,
    )
    crossed = _matching_from_edges(
        ((0, 2), (1, 3), (4, 5), (6, 7)),
        degree,
    )
    assert hidden != crossed
    assert len(set(adjacent_pair_products(hidden, crossed))) == 4


def test_ordered_subword_fibers_obey_one_quarter_bound_at_every_tested_degree():
    for half_degree in (3, 4, 5, 8):
        for moment_degree in range(2, 10):
            row = audit_adjacent_pair_injection(
                half_degree,
                moment_degree,
            )
            assert row.first_two_involutions_distinct
            assert row.first_two_bit_products_pairwise_distinct
            assert row.maximum_product_fiber_size <= (
                row.subword_cube_size // 4
            )
            assert row.every_product_fiber_at_most_one_quarter


def test_repeated_later_involutions_do_not_break_first_pair_injection():
    degree = 6
    first = _matching_from_edges(
        ((0, 2), (1, 3), (4, 5)),
        degree,
    )
    second = _matching_from_edges(
        ((0, 4), (1, 3), (2, 5)),
        degree,
    )
    elements = (first, second, first, first, second, first)
    histogram = ordered_subword_product_histogram(elements)
    assert max(histogram.values()) <= (1 << len(elements)) // 4


def test_symbolic_moment_bound_is_independent_of_degree():
    for moment_degree in (1, 2, 3, 4, 5, 8, 16, 64, 256):
        for copy_count in (1, 3, 11, 37):
            row = all_degree_moment_bound_control(
                moment_degree,
                copy_count,
            )
            assert row.alternative_identity_fiber_upper_bound * 2 == (
                row.alternative_binary_denominator
            )
            assert row.baseline_identity_fiber_upper_bound * 2 <= (
                row.baseline_binary_denominator
            )
            assert row.absolute_moment_bias_upper_bound == (
                f"1/{2**copy_count}"
            )
            assert row.all_degree_bound_verified


def test_exact_degree_four_and_five_moments_respect_all_degree_bound():
    for half_degree in (3, 4, 5, 8):
        for copy_count in (1, 2, 5, 11):
            inverse_scale = Fraction(1, 2**copy_count)
            degree_four = cross_Hecke_moment_control(
                half_degree,
                copy_count,
            )
            degree_five = degree_five_moment_control(
                half_degree,
                copy_count,
            )
            assert Fraction(degree_four.baseline_fourth_moment) <= (
                inverse_scale
            )
            assert Fraction(degree_four.likelihood_fourth_moment) <= (
                inverse_scale
            )
            assert abs(Fraction(degree_four.fourth_moment_bias)) <= (
                inverse_scale
            )
            assert Fraction(degree_five.baseline_fifth_moment) <= (
                inverse_scale
            )
            assert Fraction(degree_five.likelihood_fifth_moment) <= (
                inverse_scale
            )
            assert abs(Fraction(degree_five.fifth_moment_bias)) <= (
                inverse_scale
            )


def test_natural_all_degree_bound_is_inverse_candidate():
    for half_degree in (4, 8, 16, 32, 64):
        row = all_degree_scaling_record(half_degree)
        assert row.normalized_any_degree_moment_bias_upper_bound <= (
            row.inverse_64_candidates
        )
        assert row.normalized_polynomial_l1_bias_upper_bound <= (
            row.inverse_64_candidates
        )
        assert row.bound_at_most_inverse_64_candidates


def test_report_closes_single_operator_polynomials_but_not_spectral_projectors():
    report = build_all_degree_moment_report()
    assert report.theorem.adjacent_pair_injection_proved
    assert report.theorem.all_degree_one_quarter_concentration_proved
    assert report.theorem.all_degree_single_Hecke_moment_no_go_proved
    assert report.theorem.normalized_single_Hecke_polynomial_LCU_no_go_proved
    assert not report.theorem.nonlinear_spectral_projector_no_go_proved
    assert not report.theorem.multi_double_coset_no_go_proved
    assert not report.theorem.hidden_involution_detector_constructed
    assert not report.theorem.speedup_claim_allowed
    assert report.theorem.theorem_verified


def test_live_all_degree_report_is_json_serializable(tmp_path):
    output = tmp_path / "all-degree.json"
    payload = write_all_degree_moment_report(output)
    assert output.exists()
    assert payload["theorem"]["theorem_verified"]
    assert payload["claim_gate"][
        "all_degree_one_quarter_concentration_proved"
    ]
    assert not payload["claim_gate"][
        "nonlinear_spectral_projector_no_go_proved"
    ]
    assert not payload["claim_gate"]["speedup_claim_allowed"]
