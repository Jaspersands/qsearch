from functools import lru_cache

import pytest

from self_dual_wreath_all_codimension_baba_no_go import (
    FEEDBACK_GATE_CROSSING_CODE,
    SHARP_SEPARATOR_CODE,
    all_codimension_baba_certificate,
    audit_all_codimension_baba_code,
    exhaustive_small_code_census,
    run_all_codimension_baba_no_go,
    suffix_triangular_elimination_steps,
)
from self_dual_wreath_frame_subword_entropy import (
    frame_subword_suffix_branch_certificate,
)
from self_dual_wreath_separator_defect_frontier import (
    audit_separator_defect_code,
)


@lru_cache(maxsize=1)
def _report():
    return run_all_codimension_baba_no_go()


@pytest.mark.parametrize(
    ("control_id", "code"),
    (
        ("SHARP", SHARP_SEPARATOR_CODE),
        ("CROSSING", FEEDBACK_GATE_CROSSING_CODE),
        (
            "CROSSING-CODIMENSION-FOUR",
            tuple((*row, 0) for row in FEEDBACK_GATE_CROSSING_CODE),
        ),
    ),
)
def test_suffix_chain_eliminates_information_dimension_without_information_set(
    control_id,
    code,
):
    control = audit_all_codimension_baba_code(control_id, code)
    assert control.all_codeword_identities_forced
    assert control.suffix_branch_certificate.exact_suffix_branch_elimination_verified
    assert control.eliminated_appended_generator_count >= control.information_dimension
    assert control.residual_appended_generator_upper_bound <= control.codimension
    assert all(
        step.exact_triangular_elimination_verified
        and step.pivot_occurrence_count == 1
        and step.greater_generator_occurrence_count == 0
        for step in control.suffix_elimination_steps
    )
    assert control.exact_control_verified


def test_exact_feedback_gate_crossing_falsifies_separator_conjecture_but_not_no_go():
    separator = audit_separator_defect_code(
        "EXACT-FEEDBACK-GATE-CROSSING",
        FEEDBACK_GATE_CROSSING_CODE,
    )
    assert separator.separator_defect == 1
    assert separator.minimum_feedback_vertex_count == 2
    assert not separator.feedback_no_go_criterion_satisfied

    universal = audit_all_codimension_baba_code(
        "EXACT-FEEDBACK-GATE-CROSSING",
        FEEDBACK_GATE_CROSSING_CODE,
    )
    assert universal.residual_appended_generator_upper_bound <= 3
    assert universal.theoretical_solution_exponent_upper_bound == 7.0
    assert universal.theoretical_true_pressure_margin_lower_bound > 1.0
    assert universal.reducer_solution_exponent_upper_bound <= 5.0
    assert universal.reducer_true_pressure_margin > 3.0
    assert universal.exact_control_verified


def test_marked_relations_force_every_codeword_identity_before_surface_bound():
    for control in _report().representative_controls:
        assert control.split_relation_present
        assert control.all_unpruned_codeword_relations_present
        assert control.common_different_suffix_relations_present
        assert control.all_codeword_identities_forced
        assert control.surface_coefficient_control.exact_coefficient_absorption_verified


def test_pressure_formula_is_exact_for_every_representative_control():
    for control in _report().representative_controls:
        expected = 1.0 + 0.5 * __import__("math").log2(
            control.code_size / (control.code_size - 1)
        )
        assert control.theoretical_true_pressure_margin_lower_bound == pytest.approx(
            expected
        )
        assert control.theoretical_remaining_generator_upper_bound == (
            control.codimension + 5
        )
        assert control.theoretical_solution_exponent_upper_bound == (
            control.codimension + 4
        )


def test_suffix_witnesses_are_direct_relator_quotients_not_sampling_evidence():
    certificate = frame_subword_suffix_branch_certificate(
        FEEDBACK_GATE_CROSSING_CODE
    )
    steps = suffix_triangular_elimination_steps(certificate)
    assert len(steps) >= 3
    assert all(step.raw_relative_relation for step in steps)
    assert all(step.higher_suffix_equal and step.pivot_flipped for step in steps)


def test_width_four_census_exhausts_every_minimum_distance_two_quarter_code():
    census = exhaustive_small_code_census()
    assert census.candidate_code_count == 1_820
    assert census.minimum_distance_two_code_count > 0
    assert census.suffix_certificate_failure_count == 0
    assert census.codeword_identity_derivation_failure_count == 0
    assert census.maximum_residual_appended_generator_bound <= 2
    assert census.exhaustive_census_verified


def test_all_depth_certificate_removes_every_old_code_assumption():
    theorem = all_codimension_baba_certificate()
    assert theorem.arbitrary_width
    assert theorem.arbitrary_codimension
    assert not theorem.separator_feedback_assumption_required
    assert not theorem.information_set_assumption_required
    assert not theorem.affine_normalization_required
    assert theorem.universal_single_fiber_BABA_no_go_verified
    assert theorem.uniform_pressure_margin_lower_bound == 1.0


def test_report_closes_single_fiber_family_and_preserves_real_scope_limits():
    report = _report()
    assert report.headline_metrics[
        "all_depth_all_codimension_BABA_no_go_theorem_count"
    ] == 1
    assert report.headline_metrics["feedback_gate_crossing_control_count"] == 1
    assert report.headline_metrics[
        "feedback_crossing_surviving_full_relations_count"
    ] == 0
    assert report.headline_metrics["control_failure_count"] == 0
    assert report.headline_metrics["exhaustive_census_failure_count"] == 0
    assert report.claim_gate["all_single_fiber_BABA_code_supports_controlled"]
    assert not report.claim_gate["separator_feedback_escape_survives"]
    assert not report.claim_gate["multiple_base_fiber_patterns_controlled"]
    assert not report.claim_gate["other_marked_words_controlled"]
    assert not report.claim_gate["speedup_claim_allowed"]
