from fractions import Fraction

from self_dual_wreath_pair_core_recoupling_boundary import (
    _selected_controls,
    open_scalar_star_relative_spectrum,
    run_pair_core_recoupling_boundary,
    scalar_star_uniform_interval,
    screen_s6_pair_core_recouplings,
)


def test_open_scalar_star_has_exact_carrier_five_spectrum() -> None:
    spectrum = open_scalar_star_relative_spectrum(1 / 5, 5, 40)

    assert len(spectrum) == 50
    assert sum(abs(value - 4 / 9) < 1e-12 for value in spectrum) == 5
    assert spectrum.count(0.5) == 40
    assert sum(abs(value - 6 / 11) < 1e-12 for value in spectrum) == 5


def test_nontrivial_scalar_stars_have_uniform_endpoint_gap() -> None:
    lower, upper = scalar_star_uniform_interval(5)

    assert lower == 3 / 7
    assert upper == 5 / 9
    assert lower > 0.4
    assert upper < 0.6


def test_selected_carrier_five_nine_and_ten_controls_match_exactly() -> None:
    controls = _selected_controls()

    assert [control.carrier_dimension for control in controls] == [5, 9, 10]
    assert all(control.scalar_star_formula_verified for control in controls)
    assert controls[0].minimum_relative_eigenvalue == 4 / 9
    assert abs(controls[0].maximum_relative_eigenvalue - 6 / 11) < 1e-12
    assert abs(controls[1].minimum_relative_eigenvalue - 8 / 17) < 1e-12
    assert abs(controls[1].maximum_relative_eigenvalue - 89 / 170) < 1e-12
    assert abs(controls[2].minimum_relative_eigenvalue - 9 / 19) < 1e-12
    assert abs(controls[2].maximum_relative_eigenvalue - 11 / 21) < 1e-12
    assert all(
        control.comparison_certificate.endpoint_gap_certified
        for control in controls
    )
    assert abs(
        controls[0].comparison_certificate.grading_defect_upper_bound
        - 1 / 9
    ) < 1e-12


def test_small_s6_screen_finds_only_reciprocal_carrier_values() -> None:
    screen = screen_s6_pair_core_recouplings(control_limit=12)

    assert screen.audited_control_count == 12
    assert screen.audited_pair_core_star_count > 0
    assert screen.fractional_correlation_count > 0
    assert screen.unexpected_fractional_correlation_count == 0
    assert screen.noncommon_carrier_bound_violation_count == 0
    assert Fraction(screen.maximum_fractional_pair_core_correlation).limit_denominator(100) in {
        Fraction(1, 5),
        Fraction(1, 9),
        Fraction(1, 10),
    }


def test_report_keeps_multistar_and_coherent_transform_open() -> None:
    report = run_pair_core_recoupling_boundary(screen_control_limit=12)

    assert report.headline_metrics[
        "selected_scalar_star_validation_failure_count"
    ] == 0
    assert report.claim_gate["scalar_star_spectrum_formulas_verified"]
    assert report.claim_gate[
        "isolated_nontrivial_carrier_stars_uniformly_conditioned"
    ]
    assert report.claim_gate[
        "selected_weighted_pair_relation_endpoint_gaps_certified"
    ]
    assert report.claim_gate["finite_s6_reciprocal_carrier_screen_passed"]
    assert not report.claim_gate["all_n_pair_core_carrier_factorization_proved"]
    assert not report.claim_gate["all_depth_multistar_conditioning_proved"]
    assert not report.claim_gate["coherent_recoupling_block_transform_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]
