import math

from self_dual_wreath_early_level_overlap_localization import (
    child_span_correlation_bound,
    early_level_scaling_record,
    run_early_level_overlap_localization,
    wreath_child_span_correlation_bound,
)


def test_block_gram_bound_is_strict_exactly_below_half_n_width():
    assert wreath_child_span_correlation_bound(9, 4) == 4 / 5
    assert wreath_child_span_correlation_bound(9, 5) == 5 / 4
    assert math.isclose(child_span_correlation_bound(3, 0.1), 0.375)


def test_w5_common_free_controls_have_no_emergent_intersection():
    report = run_early_level_overlap_localization()
    metrics = report.headline_metrics

    assert metrics["synthetic_validation_failure_count"] == 0
    assert metrics["w5_control_count"] == 48
    assert metrics["w5_applicable_common_free_control_count"] > 0
    assert metrics["w5_applicable_validation_failure_count"] == 0
    assert metrics["w5_exact_common_range_control_count"] > 0
    assert report.claim_gate[
        "common_free_emergent_intersections_excluded_below_half_n_width"
    ]
    assert not report.claim_gate["linear_and_larger_child_width_controlled"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_certified_depth_is_only_logarithmic_fraction_of_full_tree():
    record = early_level_scaling_record(512)

    assert record.maximum_certified_child_leaf_count == 255
    assert record.maximum_certified_power_of_two_child_leaf_count == 128
    assert record.certified_common_free_merge_level_count == 8
    assert record.total_orientation_tree_depth > 3000
    assert record.certified_level_fraction < 0.01
    assert record.common_free_emergent_intersection_excluded
    assert not record.exact_common_range_resolver_proved
    assert not record.linear_width_and_larger_overlap_controlled
