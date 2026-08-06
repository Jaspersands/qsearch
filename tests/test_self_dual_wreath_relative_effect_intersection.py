import numpy as np

from self_dual_wreath_relative_effect_intersection import (
    audit_relative_effect_rank_identity,
    run_relative_effect_intersection,
)


def _projector(vector):
    vector = np.asarray(vector, dtype=float)
    vector /= np.linalg.norm(vector)
    return np.outer(vector, vector)


def test_nonorthogonal_disjoint_ranges_become_exact_routing_channels():
    record = audit_relative_effect_rank_identity(
        "nonorthogonal",
        _projector([1, 0]),
        _projector([1, 1]),
    )

    assert record.exact_intersection_localization_verified
    assert record.child_range_intersection_dimension == 0
    assert record.strict_fractional_eigenvalue_count == 0
    assert record.zero_relative_eigenvalue_count == 1
    assert record.one_relative_eigenvalue_count == 1


def test_shared_range_dimension_equals_fractional_channel_count():
    shared = _projector([1, 0, 0])
    record = audit_relative_effect_rank_identity(
        "shared",
        3 * shared + _projector([0, 1, 0]),
        shared + 2 * _projector([0, 0, 1]),
    )

    assert record.exact_intersection_localization_verified
    assert record.child_range_intersection_dimension == 1
    assert record.strict_fractional_eigenvalue_count == 1
    assert abs(record.minimum_fractional_eigenvalue - 0.75) < 1e-10
    assert abs(record.maximum_fractional_eigenvalue - 0.75) < 1e-10


def test_complete_w4_overlap_cores_are_balanced_and_commuting():
    report = run_relative_effect_intersection()
    metrics = report.headline_metrics

    assert metrics["generic_validation_failure_count"] == 0
    assert metrics["complete_w4_control_count"] == 156
    assert metrics["w4_validation_failure_count"] == 0
    assert metrics["w4_balanced_overlap_failure_count"] == 0
    assert metrics["w4_fractional_relative_channel_count"] == 4
    assert metrics["w4_intersecting_control_count"] == 4
    assert metrics["w4_noncommuting_intersection_control_count"] == 0
    assert report.claim_gate[
        "relative_complexity_localized_to_child_intersections"
    ]
    assert not report.claim_gate["typical_large_n_overlap_cores_classified"]
    assert not report.claim_gate["speedup_claim_allowed"]
