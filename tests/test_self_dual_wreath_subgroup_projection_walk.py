import numpy as np

from self_dual_wreath_subgroup_projection_walk import (
    audit_subgroup_projection_walk,
    gauge_coordinates,
    predicted_gauge_action,
    run_subgroup_projection_walk,
    subgroup_embedding,
    subgroup_left_action,
    subgroup_projection_regular,
)


def test_subgroup_embedding_selects_one_source_per_pair() -> None:
    element = (1, 2, 0)
    identity = (0, 1, 2)
    assert subgroup_embedding(element, 2, 0) == (
        element,
        element,
        identity,
        element,
        identity,
    )
    assert subgroup_embedding(element, 2, 3) == (
        element,
        identity,
        element,
        identity,
        element,
    )


def test_subgroup_averages_are_projectors() -> None:
    for mask in (0, 1):
        projector = subgroup_projection_regular(3, 1, mask)
        assert np.linalg.norm(projector @ projector - projector, ord=2) < 1e-12


def test_gauge_action_uses_one_common_multiplier() -> None:
    point = ((1, 2, 0), (2, 0, 1), (0, 2, 1))
    element = (2, 1, 0)
    for mask in (0, 1):
        actual = gauge_coordinates(subgroup_left_action(point, element, mask))
        predicted = predicted_gauge_action(
            gauge_coordinates(point),
            element,
            mask,
        )
        assert actual == predicted


def test_complete_s3_fourier_block_and_gauge_control() -> None:
    record = audit_subgroup_projection_walk()
    assert record.ambient_product_group_dimension == 216
    assert record.fourier_block_dimension_sum == 216
    assert record.maximum_fourier_block_spectrum_residual < 2e-12
    assert record.gauge_transition_count == 2592
    assert record.gauge_transition_failure_count == 0
    assert record.exact_subgroup_projection_walk_verified
    assert record.exact_gauge_normal_form_verified


def test_report_keeps_block_expansion_and_algorithm_gates_closed() -> None:
    report = run_subgroup_projection_walk()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["subgroup_projection_walk_lift_proved"]
    assert not report.claim_gate[
        "global_walk_gap_controls_typical_plancherel_blocks"
    ]
    assert not report.claim_gate[
        "block_restricted_local_spectral_expansion_proved"
    ]
    assert not report.claim_gate["natural_all_depth_frame_edge_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
