from fractions import Fraction

from self_dual_wreath_sibling_frame_joint_conditioning_surrogate import (
    TWO_EXTRA_COPY_PARENT_CONDITION_UPPER,
    TWO_EXTRA_COPY_RELATIVE_GAP_FLOOR,
    gaussian_joint_conditioning_record,
    run_sibling_frame_joint_conditioning_surrogate,
    two_choice_failure_boundary_record,
    two_extra_copy_scaling_record,
)


def test_parent_and_relative_hard_edges_are_distinct() -> None:
    near_half = gaussian_joint_conditioning_record(0.500001)
    near_one = gaussian_joint_conditioning_record(1.000001)

    assert near_half.parent_frame_edge_lower < 1e-10
    assert near_half.relative_effect_endpoint_gap > 0.49
    assert near_one.parent_frame_edge_lower > 0.17
    assert near_one.relative_effect_endpoint_gap < 1e-10


def test_k_or_k_plus_one_joint_score_tends_to_zero_near_half() -> None:
    coarse = two_choice_failure_boundary_record(0.51)
    fine = two_choice_failure_boundary_record(0.500001)

    assert fine.best_threshold_or_one_extra_joint_score < coarse.best_threshold_or_one_extra_joint_score
    assert fine.best_threshold_or_one_extra_joint_score < 1e-10
    assert fine.tends_to_zero_near_threshold_half


def test_two_extra_copy_interval_has_uniform_gaussian_joint_bounds() -> None:
    lower = gaussian_joint_conditioning_record(2.0)
    upper = gaussian_joint_conditioning_record(4.0)

    assert lower.parent_frame_edge_lower == 1.0
    assert lower.parent_frame_condition_number == 9.0
    assert abs(
        lower.relative_effect_endpoint_gap
        - TWO_EXTRA_COPY_RELATIVE_GAP_FLOOR
    ) < 1e-14
    assert upper.parent_frame_edge_lower > lower.parent_frame_edge_lower
    assert upper.parent_frame_condition_number < lower.parent_frame_condition_number
    assert upper.relative_effect_endpoint_gap > lower.relative_effect_endpoint_gap


def test_factorial_scaling_uses_exactly_two_extra_copies() -> None:
    for n in range(3, 101):
        row = two_extra_copy_scaling_record(n)
        threshold = Fraction(row.threshold_child_aspect_exact)
        selected = Fraction(row.selected_child_aspect_exact)

        assert Fraction(1, 2) < threshold < 1
        assert selected == 4 * threshold
        assert 2 < selected < 4
        assert row.extra_copy_count == 2
        assert row.uniform_parent_edge_verified
        assert row.uniform_parent_condition_verified
        assert row.uniform_relative_gap_verified
        assert row.parent_frame_condition_number <= TWO_EXTRA_COPY_PARENT_CONDITION_UPPER
        assert not row.natural_joint_conditioning_proved


def test_report_blocks_gaussian_to_natural_overclaim() -> None:
    report = run_sibling_frame_joint_conditioning_surrogate()

    assert report.headline_metrics["two_extra_copy_scaling_failure_count"] == 0
    assert report.claim_gate[
        "k_or_k_plus_one_interval_uniform_joint_certificate_rejected"
    ]
    assert report.claim_gate[
        "two_extra_copy_gaussian_joint_conditioning_proved"
    ]
    assert not report.claim_gate[
        "binary_all_depth_gaussian_joint_conditioning_proved"
    ]
    assert not report.claim_gate[
        "natural_independent_joint_spectral_edges_proved"
    ]
    assert not report.claim_gate[
        "globally_distinct_joint_spectral_edges_proved"
    ]
    assert not report.claim_gate["speedup_claim_allowed"]
