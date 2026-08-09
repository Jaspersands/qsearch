from functools import lru_cache

from self_dual_wreath_high_codimension_face_word_frontier import (
    audit_high_codimension_face_word,
    run_high_codimension_face_word_frontier,
)


@lru_cache(maxsize=1)
def _report():
    return run_high_codimension_face_word_frontier()


def test_reverse_block_union_is_exactly_the_free_cancellation_pattern():
    control = audit_high_codimension_face_word(
        (0, 0, 1, 1),
        (1, 1, 0, 0),
        (1, 1, 1, 1),
    )
    assert control.freely_trivial
    assert control.exact_reverse_block_union_cancellation_verified
    assert control.elementary_class == "reverse-block-union-cancellation"

    wrong_order = audit_high_codimension_face_word(
        (1, 1, 0, 0),
        (0, 0, 1, 1),
        (1, 1, 1, 1),
    )
    assert not wrong_order.freely_trivial
    assert wrong_order.exact_reverse_block_union_cancellation_verified


def test_singleton_and_quadratic_incidence_have_uniform_elementary_loss():
    singleton = audit_high_codimension_face_word(
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
    )
    assert singleton.elementary_class == "once-occurring-generator"
    assert singleton.elementary_solution_exponent_loss_lower_bound == 1

    quadratic = audit_high_codimension_face_word(
        (1, 0),
        (1, 0),
        (0, 0),
    )
    assert quadratic.elementary_class == "quadratic-surface-word"
    assert quadratic.elementary_solution_exponent_loss_lower_bound >= 0.5


def test_width_three_cubic_frontier_is_finitely_primitive_not_promoted_to_theorem():
    report = _report()
    assert len(report.representative_cubic_controls) == 4
    assert all(
        row.maximum_generator_occurrence == 3
        and row.cubic_overlap_frontier
        and row.finite_control_solution_exponent_loss is not None
        and row.finite_control_solution_exponent_loss >= 1
        for row in report.representative_cubic_controls
    )
    assert not report.claim_gate[
        "all_growing_width_cubic_overlap_words_controlled"
    ]


def test_report_excludes_growing_power_degree_and_keeps_cubic_word_debt_open():
    report = _report()
    assert report.headline_metrics[
        "high_power_escape_exclusion_theorem_count"
    ] == 1
    assert report.headline_metrics["maximum_face_word_generator_occurrence"] == 3
    assert report.headline_metrics["maximum_possible_proper_power_degree"] == 3
    assert report.headline_metrics["certificate_failure_count"] == 0
    assert not report.claim_gate["growing_power_degree_face_escape_possible"]
    assert report.claim_gate["empty_face_words_exactly_classified"]
    assert report.claim_gate["singleton_and_quadratic_face_words_controlled"]
    assert not report.claim_gate["all_high_codimension_local_words_controlled"]
    assert not report.claim_gate["speedup_claim_allowed"]
