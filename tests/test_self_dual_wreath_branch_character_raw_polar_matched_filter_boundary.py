import math

from self_dual_wreath_branch_character_raw_polar_matched_filter_boundary import (
    THREE_QUARTER_EXPONENT,
    audit_raw_polar_matched_filter,
    raw_polar_matched_filter_scaling,
    run_raw_polar_matched_filter_boundary,
)


SINGLE = (((3,), (2, 1)),)
THRESHOLD = (
    ((3,), (2, 1)),
    ((3,), (1, 1, 1)),
    ((2, 1), (1, 1, 1)),
)


def test_local_raw_polar_cross_maps_are_positive_contractions():
    control = audit_raw_polar_matched_filter("single", SINGLE)
    assert control.exact_raw_polar_matched_filter_boundary_verified
    assert control.maximum_local_cross_hermiticity_residual < 1e-9
    assert control.minimum_local_cross_eigenvalue >= -1e-9
    assert control.maximum_local_cross_eigenvalue <= 1 + 1e-9


def test_correct_blocks_equal_the_average_positive_cross_map():
    control = audit_raw_polar_matched_filter("threshold", THRESHOLD)
    assert control.correct_block_identity_residual < 1e-9
    assert control.global_overlap_identity_residual < 1e-9
    assert control.matched_cross_minimum_eigenvalue >= -1e-9


def test_unwhitened_correct_success_is_bounded_by_raw_polar_overlap():
    control = audit_raw_polar_matched_filter("threshold", THRESHOLD)
    assert control.unwhitened_matched_filter_success <= (
        control.normalized_raw_polar_overlap + 1e-9
    )
    assert control.matched_success_upper_bound_residual < 1e-9


def test_polar_distance_is_bounded_by_gram_residual():
    control = audit_raw_polar_matched_filter("threshold", THRESHOLD)
    assert control.polar_distance_below_gram_residual
    assert control.polar_to_convolution_distance <= (
        control.polar_convolution_gram_residual + 1e-9
    )


def test_whitened_decoder_obeys_concentration_times_gram_bound():
    control = audit_raw_polar_matched_filter("single", SINGLE)
    assert control.whitened_success_bound_verified
    assert control.whitened_correct_success <= control.whitened_success_upper_bound + 1e-9


def test_polynomial_raw_domination_forces_asymptotic_failure():
    row = raw_polar_matched_filter_scaling(256, polynomial_concentration_degree=20)
    assert math.isclose(
        row.three_quarter_power_exponent,
        THREE_QUARTER_EXPONENT,
    )
    assert row.polynomial_domination_forces_decoder_failure_asymptotically
    assert row.finite_polynomial_domination_failure_visible
    assert row.whitened_success_upper_bound < 0.1


def test_report_reverses_physical_domination_gate_without_rejecting_actual_pgm():
    report = run_raw_polar_matched_filter_boundary()
    assert report.theorem.theorem_verified
    assert report.claim_gate["unwhitened_polar_matched_filter_success_vanishes"]
    assert report.claim_gate[
        "polynomial_raw_domination_would_force_whitened_decoder_failure"
    ]
    assert not report.claim_gate["physical_input_domination_is_positive_completion_gate"]
    assert not report.claim_gate["actual_physical_pgm_rejected"]
    assert not report.claim_gate["speedup_claim_allowed"]
