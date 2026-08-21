from fractions import Fraction

from coset_hidden_involution_binary_decision_reduction import (
    involution_class_size,
)
from coset_hidden_involution_cross_transposition_hecke_moment_no_go import (
    cross_Hecke_moment_control,
)
from coset_hidden_involution_orbit_synthesis_flatness import (
    flatness_copy_count,
)
from coset_hidden_involution_single_hecke_bounded_spectral_no_go import (
    bounded_polynomial_degree_control,
    bounded_spectral_scaling_record,
    build_bounded_spectral_report,
    spectral_concentration_control,
    write_bounded_spectral_report,
)


def test_spectral_concentration_uses_exact_second_moments():
    for half_degree in (3, 4, 5, 8, 16):
        for copy_count in (1, 4, 9, 17):
            row = spectral_concentration_control(
                half_degree,
                copy_count,
            )
            exact = cross_Hecke_moment_control(
                half_degree,
                copy_count,
            )
            assert Fraction(row.baseline_second_moment) == Fraction(
                exact.baseline_second_moment
            )
            assert Fraction(row.likelihood_second_moment) == Fraction(
                exact.likelihood_second_moment
            )
            assert row.exact_second_moment_formula_verified


def test_markov_cauchy_schwarz_degree_bound_is_symbolically_consistent():
    for half_degree in (3, 4, 5, 8, 16):
        candidates = involution_class_size(2 * half_degree, half_degree)
        copies = flatness_copy_count(candidates)
        for target_bias in (0.01, 0.1, 0.5):
            row = bounded_polynomial_degree_control(
                half_degree,
                copies,
                target_bias,
            )
            assert row.constant_term_cancels
            assert row.exact_degree_lower_bound >= (
                row.simplified_natural_degree_lower_bound
                * (1.0 - 1e-14)
            )
            assert row.integer_degree_lower_bound >= (
                row.integer_simplified_degree_lower_bound
            )
            assert row.exact_bound_implies_simplified_bound


def test_constant_bias_requires_superpolynomial_natural_degree():
    rows = [
        bounded_spectral_scaling_record(half_degree)
        for half_degree in (8, 16, 32, 64)
    ]
    assert all(
        row.required_degree_exceeds_half_candidate_fourth_root
        for row in rows
    )
    assert all(row.required_degree_exceeds_half_degree_squared for row in rows)
    assert all(
        right.required_polynomial_degree_log2
        > left.required_polynomial_degree_log2
        for left, right in zip(rows, rows[1:])
    )


def test_degree_bound_tracks_candidate_fourth_root_asymptotically():
    for half_degree in (8, 16, 32, 64):
        row = bounded_spectral_scaling_record(half_degree)
        assert row.required_polynomial_degree_log2 >= (
            row.candidate_fourth_root_log2 - 1.0
        )
        assert row.required_polynomial_degree > 0.0


def test_report_rules_out_bounded_QSVT_but_preserves_access_boundary():
    report = build_bounded_spectral_report()
    assert report.theorem.exact_spectral_concentration_proved
    assert report.theorem.bounded_polynomial_bias_theorem_proved
    assert report.theorem.superpolynomial_natural_degree_lower_bound_proved
    assert report.theorem.efficient_single_operator_QSVT_filter_ruled_out
    assert not report.theorem.unrestricted_spectral_projector_ruled_out
    assert not report.theorem.multi_operator_spectral_algorithm_ruled_out
    assert not report.theorem.hidden_involution_detector_constructed
    assert not report.theorem.speedup_claim_allowed
    assert report.theorem.theorem_verified


def test_live_bounded_spectral_report_is_json_serializable(tmp_path):
    output = tmp_path / "bounded-spectral.json"
    payload = write_bounded_spectral_report(output)
    assert output.exists()
    assert payload["theorem"]["theorem_verified"]
    assert payload["claim_gate"][
        "efficient_single_operator_QSVT_filter_ruled_out"
    ]
    assert not payload["claim_gate"][
        "unrestricted_spectral_projector_ruled_out"
    ]
    assert not payload["claim_gate"]["speedup_claim_allowed"]
