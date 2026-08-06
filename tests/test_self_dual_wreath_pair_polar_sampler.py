import math

import numpy as np

from self_dual_wreath_pair_polar_sampler import (
    pair_polar_scaling_record,
    projector_sum_spectrum_from_correlations,
    run_pair_polar_sampler,
)


def test_two_projector_sum_spectrum_handles_common_and_noncommon_blocks():
    spectrum = projector_sum_spectrum_from_correlations(
        left_rank=4,
        right_rank=3,
        correlations=(1.0, 0.5),
    )

    assert np.allclose(
        spectrum,
        np.asarray([0.5, 1.0, 1.0, 1.0, 1.5, 2.0]),
    )


def test_wreath_pair_polar_controls_match_principal_angle_formula():
    report = run_pair_polar_sampler()

    assert report.headline_metrics["finite_pair_control_count"] > 0
    assert report.headline_metrics["finite_pair_validation_failure_count"] == 0
    assert report.headline_metrics["finite_noncommuting_pair_control_count"] > 0
    assert report.headline_metrics[
        "maximum_finite_pair_support_condition_number"
    ] <= 3.0 + 1e-8
    assert report.claim_gate["pair_polar_sampler_polynomial"]
    assert not report.claim_gate["recursive_pair_sampler_polynomial"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_all_n_pair_polar_gap_is_constant_and_improves_with_n():
    small = pair_polar_scaling_record(5)
    large = pair_polar_scaling_record(512)

    assert small.normalized_analysis_singular_gap_lower_bound > 0.6
    assert large.normalized_analysis_singular_gap_lower_bound > small.normalized_analysis_singular_gap_lower_bound
    assert large.support_condition_number_upper_bound < small.support_condition_number_upper_bound
    assert large.polar_query_prefactor_upper_bound < math.sqrt(2.01)
    assert large.pair_polar_sampler_polynomial
    assert not large.recursive_global_sampler_proved
