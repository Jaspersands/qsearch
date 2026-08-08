from fractions import Fraction

from representation_obstruction import integer_partitions
from self_dual_wreath_sibling_frame_joint_freeness import (
    sibling_joint_moment_formula,
)
from self_dual_wreath_sibling_word_map_normal_form import (
    audit_direct_word_normal_form,
    canonical_binary_words,
    free_mp_binary_word_moment,
    independent_sibling_word_moment,
    mixed_word_map_strata,
    run_sibling_word_map_normal_form,
)


def test_normal_form_recovers_all_degree_four_exact_formulas() -> None:
    formula = sibling_joint_moment_formula(6, 2, 3, 3, 2)
    target = (2, 1)

    assert independent_sibling_word_moment(3, 2, target, "AAB") == Fraction(
        formula.expected_a_squared_b
    )
    assert independent_sibling_word_moment(3, 2, target, "AABB") == Fraction(
        formula.expected_a_squared_b_squared
    )
    assert independent_sibling_word_moment(3, 2, target, "ABAB") == Fraction(
        formula.expected_abab
    )


def test_free_mp_comparator_counts_color_respecting_noncrossing_partitions() -> None:
    alpha = Fraction(1, 3)

    assert free_mp_binary_word_moment("AAB", alpha) == alpha**2 + alpha**3
    assert free_mp_binary_word_moment("AABB", alpha) == (
        alpha**2 + 2 * alpha**3 + alpha**4
    )
    assert free_mp_binary_word_moment("ABAB", alpha) == 2 * alpha**3 + alpha**4


def test_word_strata_eliminate_two_group_variables_exactly() -> None:
    for word in ("AB", "AAB", "AABB", "ABAB", "AABAB", "AABBAB"):
        strata = mixed_word_map_strata(3, word)
        assert sum(count for _, _, count in strata) == 6 ** (len(word) - 2)
        assert all(q_value % 2 == 0 for q_value, _, _ in strata)


def test_canonical_words_remove_trace_symmetries() -> None:
    assert canonical_binary_words(2) == ("AB",)
    assert set(canonical_binary_words(4)) == {"AAAB", "AABB", "ABAB"}
    assert len(canonical_binary_words(6)) < 2**6 - 2


def test_direct_projectors_match_higher_word_normal_form() -> None:
    controls = [
        audit_direct_word_normal_form(3, 2, target, "AABAB")
        for target in integer_partitions(3)
    ]

    assert all(control.source_tuple_count == 81 for control in controls)
    assert all(control.formula_residual < 1e-10 for control in controls)
    assert all(control.exact_direct_validation for control in controls)


def test_report_exposes_growing_word_and_injective_gates() -> None:
    report = run_sibling_word_map_normal_form()

    assert report.headline_metrics["direct_projector_control_failure_count"] == 0
    assert report.headline_metrics["highest_screened_word_order"] == 6
    assert report.claim_gate[
        "exact_independent_arbitrary_word_normal_form_proved"
    ]
    assert not report.claim_gate["all_fixed_order_joint_freeness_proved"]
    assert not report.claim_gate["growing_word_high_q_rigidity_proved"]
    assert not report.claim_gate["globally_distinct_word_control_proved"]
    assert not report.claim_gate["natural_jacobi_spectral_edge_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
