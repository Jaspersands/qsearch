import numpy as np
import pytest

from self_dual_wreath_weighted_overlap_exclusion import (
    _w3_boundary_control,
    run_weighted_overlap_exclusion,
    weighted_span_correlation_bound,
)


def test_weighted_bound_uses_graph_spectrum_not_max_degree_count() -> None:
    weights = np.zeros((6, 6))
    for left, right in ((0, 3), (1, 4), (2, 5)):
        weights[left, right] = weights[right, left] = 0.4

    bound, left_radius, right_radius = weighted_span_correlation_bound(
        weights,
        (0, 1, 2),
        (3, 4, 5),
    )

    assert left_radius == 0
    assert right_radius == 0
    assert bound == pytest.approx(0.4)


def test_w3_emergent_plane_reaches_exact_weighted_boundary() -> None:
    record = _w3_boundary_control()

    assert record.exact_pairwise_common_dimension == 0
    assert record.minimum_nonzero_pair_carrier_dimension == 2
    assert record.maximum_weighted_span_correlation_bound == pytest.approx(1.0)
    assert not record.all_affine_merges_strictly_subcritical


def test_s6_common_free_screen_is_strictly_subcritical() -> None:
    report = run_weighted_overlap_exclusion()

    assert len(report.s6_screen_controls) == 30
    assert all(
        record.exact_pairwise_common_dimension == 0
        for record in report.s6_screen_controls
    )
    assert all(
        record.maximum_invariant_multiplicity >= 2
        for record in report.s6_screen_controls
    )
    assert all(
        record.all_affine_merges_strictly_subcritical
        for record in report.s6_screen_controls
    )
    assert report.headline_metrics["s6_affine_merge_comparison_count"] == 1920
    assert report.headline_metrics[
        "s6_strict_zero_intersection_certificate_count"
    ] == 1920
    assert report.headline_metrics["s6_uncertified_merge_count"] == 0
    assert report.headline_metrics[
        "s6_maximum_weighted_span_correlation_bound"
    ] < 0.436


def test_report_keeps_all_depth_quotient_problem_open() -> None:
    report = run_weighted_overlap_exclusion()

    assert report.claim_gate[
        "weighted_carrier_graph_overlap_exclusion_proved"
    ]
    assert report.claim_gate[
        "w3_emergent_fiber_saturates_weighted_boundary"
    ]
    assert report.claim_gate[
        "finite_s6_common_free_screen_strictly_subcritical"
    ]
    assert not report.claim_gate[
        "all_depth_quotient_carrier_graph_subcriticality_proved"
    ]
    assert not report.claim_gate["speedup_claim_allowed"]
