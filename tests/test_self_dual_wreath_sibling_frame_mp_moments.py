from fractions import Fraction

from representation_obstruction import integer_partitions
from self_dual_wreath_sibling_frame_mp_moments import (
    audit_direct_sibling_moments,
    run_sibling_frame_mp_moments,
    sibling_frame_scaling_record,
    sibling_moment_formula,
    symmetric_group_nonidentity_involution_count,
)


def test_exact_sibling_moment_formulas_at_s3_threshold() -> None:
    row = sibling_moment_formula(
        6,
        2,
        conjugacy_class_count=3,
        nonidentity_involution_count=3,
    )

    assert Fraction(row.child_aspect_ratio) == Fraction(1, 3)
    assert Fraction(row.expected_normalized_trace) == Fraction(1, 3)
    assert Fraction(row.expected_normalized_second_moment) == Fraction(7, 18)
    assert Fraction(row.expected_normalized_third_moment) == Fraction(1, 2)
    assert Fraction(row.expected_normalized_fourth_moment) == Fraction(25, 36)
    assert Fraction(row.expected_normalized_mixed_second_moment) == Fraction(1, 9)
    assert Fraction(row.expected_normalized_sibling_difference_energy) == Fraction(5, 9)
    assert Fraction(row.expected_best_scalar_residual_energy) == Fraction(5, 18)
    assert symmetric_group_nonidentity_involution_count(3) == 3


def test_explicit_projectors_match_all_five_statistics_for_every_s3_target() -> None:
    controls = [
        audit_direct_sibling_moments(3, 2, target)
        for target in integer_partitions(3)
    ]

    assert all(control.source_tuple_count == 81 for control in controls)
    assert all(control.maximum_formula_residual < 1e-10 for control in controls)
    assert all(control.direct_projector_moments_verified for control in controls)


def test_mp_moment_residuals_are_finite_group_corrections() -> None:
    row = sibling_frame_scaling_record(48)

    assert 0.5 <= row.child_aspect_ratio < 1
    assert row.second_moment_mp_residual < 1e-60
    assert row.third_moment_mp_residual < 1e-60
    assert row.fourth_moment_mp_residual < 1e-20
    assert row.scalar_residual_energy > 0.5
    assert row.sibling_difference_energy > 1.0


def test_wishart_edge_is_explicitly_only_a_heuristic() -> None:
    row = sibling_frame_scaling_record(48)

    assert row.wishart_edge_lower_heuristic > 0
    assert row.wishart_edge_upper_heuristic > row.wishart_edge_lower_heuristic
    assert row.condition_number_endpoint_gap_heuristic > 0
    assert not row.growing_moment_spectral_edge_proved
    assert not row.natural_pseudoinverse_comparability_proved


def test_report_falsifies_scalar_route_and_blocks_mp_overclaim() -> None:
    report = run_sibling_frame_mp_moments()

    assert report.headline_metrics["direct_projector_control_failure_count"] == 0
    assert report.claim_gate[
        "independent_plancherel_moments_through_four_proved"
    ]
    assert not report.claim_gate[
        "child_frames_frobenius_close_to_equal_scalars"
    ]
    assert report.claim_gate["marchenko_pastur_fixed_moment_signal_present"]
    assert not report.claim_gate["globally_distinct_fixed_moments_proved"]
    assert not report.claim_gate["marchenko_pastur_law_proved"]
    assert not report.claim_gate[
        "natural_child_frame_spectral_edges_proved"
    ]
    assert not report.claim_gate["speedup_claim_allowed"]
