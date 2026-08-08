from fractions import Fraction

from representation_obstruction import integer_partitions
from self_dual_wreath_sibling_frame_joint_freeness import (
    audit_direct_sibling_joint_moments,
    joint_freeness_scaling_record,
    run_sibling_frame_joint_freeness,
    sibling_joint_moment_formula,
)


def test_exact_s3_mixed_word_formulas_include_target_crossing_term() -> None:
    trivial = sibling_joint_moment_formula(6, 2, 3, 3, 1)
    standard = sibling_joint_moment_formula(6, 2, 3, 3, 2)

    assert Fraction(trivial.expected_a_squared_b) == Fraction(7, 54)
    assert Fraction(trivial.expected_a_squared_b_squared) == Fraction(1, 6)
    assert Fraction(trivial.expected_abab) == Fraction(5, 36)
    assert Fraction(standard.expected_abab) == Fraction(7, 72)
    assert trivial.crossing_q2_count == 18
    assert trivial.crossing_q4_count == 0
    assert trivial.q6_count == 4
    assert trivial.q8_count == 13


def test_explicit_projectors_match_all_mixed_words_for_every_s3_target() -> None:
    controls = [
        audit_direct_sibling_joint_moments(3, 2, target)
        for target in integer_partitions(3)
    ]

    assert all(control.source_tuple_count == 81 for control in controls)
    assert all(control.maximum_formula_residual < 1e-10 for control in controls)
    assert all(control.exact_direct_projector_validation for control in controls)


def test_adaptive_scaling_residuals_vanish_uniformly_in_target() -> None:
    early = joint_freeness_scaling_record(8)
    late = joint_freeness_scaling_record(48)

    assert late.a_squared_b_free_residual < early.a_squared_b_free_residual
    assert late.a_squared_b_squared_free_residual < 1e-15
    assert late.uniform_target_abab_free_residual_bound < 1e-15
    assert late.conjugacy_class_fraction < early.conjugacy_class_fraction
    assert late.involution_fraction < early.involution_fraction
    assert late.independent_plancherel_degree_four_freeness_proved
    assert late.extra_copy_count == 2
    assert not late.globally_distinct_degree_four_freeness_proved
    assert not late.growing_word_or_resolvent_control_proved


def test_report_proves_finite_order_joint_freeness_but_blocks_edges() -> None:
    report = run_sibling_frame_joint_freeness()

    assert report.headline_metrics["direct_projector_control_failure_count"] == 0
    assert report.claim_gate[
        "exact_independent_mixed_moments_through_degree_four_proved"
    ]
    assert report.claim_gate[
        "independent_plancherel_joint_freeness_through_degree_four_proved"
    ]
    assert not report.claim_gate[
        "globally_distinct_joint_freeness_through_degree_four_proved"
    ]
    assert not report.claim_gate["growing_word_or_resolvent_control_proved"]
    assert not report.claim_gate["natural_sibling_frame_spectral_edge_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
