from fractions import Fraction

from coset_hidden_involution_cross_transposition_hecke_degree_five_no_go import (
    audit_degree_five_support_catalog,
    build_degree_five_report,
    degree_five_moment_control,
    degree_five_return_branch_control,
    degree_five_scaling_record,
    direct_degree_five_binary_histogram,
    write_degree_five_report,
)


def test_nine_degree_five_support_cores_are_exact():
    controls = audit_degree_five_support_catalog()
    assert len(controls) == 9
    assert [
        row.canonical_all_active_path_count for row in controls
    ] == [
        16,
        1280,
        18160,
        101664,
        289248,
        460800,
        417600,
        201600,
        40320,
    ]
    assert all(
        row.exact_canonical_support_enumeration_verified
        for row in controls
    )
    odd = {
        row.active_unaffected_pair_count: (
            row.odd_identity_path_count,
            row.odd_identity_occurrence_count,
        )
        for row in controls
        if row.odd_identity_path_count
    }
    assert odd == {0: (15, 120), 2: (156, 216)}


def test_all_rank_degree_five_histogram_and_m4_exception():
    expected = {
        3: {1: 440, 2: 564, 4: 252, 8: 39, 16: 1},
        4: {1: 12880, 2: 6376, 4: 1386, 8: 93, 16: 1},
        5: {1: 119856, 2: 35544, 4: 4422, 8: 177, 16: 1},
    }
    for half_degree, histogram in expected.items():
        row = degree_five_return_branch_control(half_degree)
        assert row.alternative_identity_histogram == histogram
        assert row.histogram_sums_to_all_paths
        assert row.support_deletion_bijection_verified
        assert row.exact_degree_five_return_classification_verified
        assert row.odd_exception_path_count == (
            156 if half_degree == 4 else 0
        )
        assert row.odd_exception_identity_occurrence_count == (
            216 if half_degree == 4 else 0
        )

    assert direct_degree_five_binary_histogram(3) == expected[3]
    assert direct_degree_five_binary_histogram(4) == expected[4]


def test_baseline_degree_five_closure_histogram_is_independently_enumerated():
    expected = {
        3: {1: 48, 2: 20, 4: 5},
        4: {1: 96, 2: 60, 4: 5},
        5: {1: 144, 2: 120, 4: 5},
        8: {1: 288, 2: 420, 4: 5},
    }
    for half_degree, histogram in expected.items():
        row = degree_five_return_branch_control(half_degree)
        assert row.baseline_closure_histogram == histogram
        assert row.maximum_alternative_identity_count == 16
        assert row.maximum_baseline_identity_count == 4


def test_exact_fifth_moment_has_uncancelled_but_sparse_leading_term():
    for half_degree in (3, 4, 5, 8, 16):
        r = half_degree * (half_degree - 1)
        for copy_count in (1, 2, 5, 11):
            x = 2**copy_count
            row = degree_five_moment_control(half_degree, copy_count)
            bias = Fraction(row.fifth_moment_bias)
            leading = Fraction(row.surviving_leading_transporter_term)
            remainder = Fraction(row.remaining_bias_after_leading_term)
            assert leading == Fraction(1, x * r**4)
            assert bias == leading + remainder
            assert remainder >= 0
            assert remainder <= Fraction(4, x**2)
            assert not row.leading_copy_weight_cancels_against_baseline
            assert row.exact_fifth_moment_formula_verified


def test_natural_quintic_bias_remains_inverse_candidate_scale():
    for half_degree in (4, 8, 16, 32, 64):
        row = degree_five_scaling_record(half_degree)
        candidates = int(row.conjugacy_class_size_decimal)
        assert row.remainder_at_most_four_over_copy_scale_squared
        assert row.fifth_bias_at_most_twice_inverse_copy_scale
        assert row.quintic_unit_coefficient_bias_upper_bound <= (
            6.0 / (64.0 * candidates)
        )
        assert row.quintic_bias_at_most_six_times_inverse_64_candidates


def test_report_falsifies_cancellation_without_promoting_speedup():
    report = build_degree_five_report()
    assert report.theorem.exact_nine_core_support_catalog_proved
    assert report.theorem.exact_all_rank_degree_five_histogram_proved
    assert report.theorem.exact_baseline_fifth_moment_proved
    assert report.theorem.exact_likelihood_fifth_moment_proved
    assert (
        report.theorem.blanket_leading_transporter_cancellation_conjecture_falsified
    )
    assert not report.theorem.normalized_quintic_filter_amplifies_to_constant_bias
    assert not report.theorem.full_spectral_no_go_proved
    assert not report.theorem.hidden_involution_detector_constructed
    assert not report.theorem.speedup_claim_allowed
    assert report.theorem.theorem_verified


def test_live_degree_five_report_is_json_serializable(tmp_path):
    output = tmp_path / "degree-five.json"
    payload = write_degree_five_report(output)
    assert output.exists()
    assert payload["theorem"]["theorem_verified"]
    assert payload["claim_gate"]["exact_cross_Hecke_fifth_moment_proved"]
    assert not payload["claim_gate"][
        "degree_four_leading_cancellation_extends_to_degree_five"
    ]
    assert not payload["claim_gate"]["speedup_claim_allowed"]
