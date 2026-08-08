import pytest

from self_dual_wreath_global_carrier_channel_extractor import (
    run_global_carrier_channel_extractor,
)


def test_physical_w6_channels_extract_as_affine_incomplete_stars() -> None:
    report = run_global_carrier_channel_extractor()

    assert report.headline_metrics["physical_extraction_control_count"] == 7
    assert report.headline_metrics["physical_extraction_failure_count"] == 0
    assert report.headline_metrics[
        "extracted_affine_incomplete_channel_count"
    ] >= 2
    assert report.headline_metrics[
        "extracted_three_edge_star_channel_count"
    ] >= 7
    assert report.headline_metrics["extracted_nonstar_channel_count"] == 0

    nontrivial = [
        channel
        for control in report.controls
        for channel in control.channels
        if channel.edge_count == 3
    ]
    assert len(nontrivial) >= 2
    for channel in nontrivial:
        assert channel.orientation_support_is_affine
        assert not channel.channel_edge_support_is_complete
        assert channel.complete_graph_edge_count == 6
        assert channel.missing_complete_graph_edge_count == 3
        assert channel.every_crossing_bit_split_is_vertex_balanced
        assert channel.minimum_endpoint_gap > 0.4


def test_extracted_carrier_multiplicities_and_defects_match_dense_controls() -> None:
    report = run_global_carrier_channel_extractor()
    channels = [
        channel
        for control in report.controls
        for channel in control.channels
        if channel.edge_count == 3
    ]

    by_multiplicity = {
        channel.coefficient_multiplicity: channel for channel in channels
    }
    assert by_multiplicity[9].maximum_grading_defect_norm == pytest.approx(
        1 / 17
    )
    assert by_multiplicity[5].maximum_grading_defect_norm == pytest.approx(
        1 / 9
    )


def test_report_rejects_affine_to_complete_inference() -> None:
    report = run_global_carrier_channel_extractor()

    assert report.claim_gate["physical_global_channel_extractor_verified"]
    assert report.claim_gate[
        "finite_w6_affine_channels_are_incomplete_stars"
    ]
    assert not report.claim_gate[
        "finite_w6_nonstar_residual_channel_found"
    ]
    assert not report.claim_gate[
        "affine_support_sufficient_for_complete_internal_closure"
    ]
    assert not report.claim_gate[
        "natural_threshold_channel_family_classified"
    ]
    assert not report.claim_gate[
        "natural_channel_resolvent_comparability_proved"
    ]
    assert not report.claim_gate["speedup_claim_allowed"]
