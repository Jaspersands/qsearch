from functools import lru_cache

import pytest

from self_dual_wreath_separator_defect_frontier import (
    FEEDBACK_GATE_CROSSING_CONTROL,
    SAT_CODIMENSION_THREE_CONTROL,
    SHARP_SEPARATOR_FEEDBACK_CONTROL,
    audit_feedback_rich_parity_family,
    audit_separator_defect_code,
    exhaustive_separator_feedback_census,
    feedback_rich_parity_code,
    minimum_separating_sets,
    run_separator_defect_frontier,
    separator_defect_all_depth_certificate,
)


@lru_cache(maxsize=1)
def _report():
    return run_separator_defect_frontier()


def test_exact_codimension_three_control_has_acyclic_separator_witnesses():
    control = audit_separator_defect_code(
        "SAT-CODIMENSION-THREE-ACYCLIC",
        SAT_CODIMENSION_THREE_CONTROL,
    )
    assert control.codimension == 3
    assert control.separator_defect == 1
    assert control.minimum_separator_size == control.information_dimension + 1
    assert control.minimum_feedback_vertex_count == 0
    assert control.feedback_no_go_criterion_satisfied
    assert control.exact_acyclic_tietze_elimination_verified
    assert control.residual_appended_generator_upper_bound == 2
    assert control.feedback_pressure_margin_lower_bound > 2.0
    assert control.exact_control_verified


@pytest.mark.parametrize("tail_width", range(5))
def test_upper_star_local_cycle_is_rejected_by_global_separator_search(tail_width):
    family = audit_feedback_rich_parity_family(tail_width)
    assert family.codimension == 3
    assert not family.has_dimension_sized_information_set
    assert family.minimum_separator_size == family.information_dimension + 1
    assert family.separator_defect == 1
    assert family.obvious_projection_feedback_vertex_count == 2
    assert family.minimum_feedback_vertex_count == 0
    assert not family.feedback_exceeds_separator_defect
    assert family.alternative_acyclic_separator_found
    assert family.exact_control_verified


@pytest.mark.parametrize("tail_width", range(5))
def test_rejected_local_cycle_family_also_collapses_to_C2_free_Z(tail_width):
    family = audit_feedback_rich_parity_family(tail_width)
    assert family.codeword_presentation_remaining_generator_count == 2
    assert any(
        len(relation) == 2
        for relation in family.codeword_presentation_residual_relations
    )
    assert family.exact_C2_free_Z_factorization_verified
    assert family.appended_solution_exponent_upper_bound == 1.5
    assert family.marked_solution_exponent_upper_bound == 5.5
    assert family.marked_pressure_margin_lower_bound > 2.5


def test_width_five_separator_feedback_census_is_exhaustive():
    census = exhaustive_separator_feedback_census()
    assert census.candidate_code_count == 35_960
    assert census.minimum_distance_two_no_information_set_code_count == 1_920
    assert census.globally_acyclic_witness_code_count == 1_920
    assert census.positive_feedback_code_count == 0
    assert census.maximum_observed_feedback_vertex_count == 0
    assert census.exhaustive_census_verified


def test_width_six_exact_controls_make_separator_bound_sharp_and_then_cross_it():
    sharp = audit_separator_defect_code(
        "SAT-SEPARATOR-BOUND-SHARP",
        SHARP_SEPARATOR_FEEDBACK_CONTROL,
    )
    assert sharp.separator_defect == 1
    assert sharp.minimum_feedback_vertex_count == 1
    assert sharp.feedback_no_go_criterion_satisfied
    assert sharp.feedback_pressure_margin_lower_bound > 1.0

    crossing = audit_separator_defect_code(
        "SAT-FEEDBACK-GATE-CROSSING",
        FEEDBACK_GATE_CROSSING_CONTROL,
    )
    assert crossing.separator_defect == 1
    assert crossing.minimum_feedback_vertex_count == 2
    assert not crossing.feedback_no_go_criterion_satisfied
    assert crossing.codeword_reducer_remaining_generator_count == 1
    assert crossing.codeword_reducer_solution_exponent_upper_bound == 0.5
    assert crossing.marked_reducer_solution_exponent_upper_bound == 5.0
    assert crossing.marked_reducer_true_pressure_margin > 3.0
    assert crossing.exact_control_verified


def test_minimum_separator_is_strictly_larger_than_information_dimension():
    for tail_width in range(3):
        code = feedback_rich_parity_code(tail_width)
        separators = minimum_separating_sets(code)
        dimension = len(code).bit_length() - 1
        assert separators
        assert len(separators[0]) == dimension + 1


def test_report_records_crossing_and_rejects_feedback_as_complete_frontier():
    theorem = separator_defect_all_depth_certificate()
    assert theorem.arbitrary_width_feedback_bound
    assert theorem.rigorous_no_go_condition == "f<=k"
    assert theorem.global_feedback_gate_crossing_constructed
    report = _report()
    assert report.headline_metrics["separator_feedback_bound_theorem_count"] == 1
    assert report.headline_metrics["feedback_gate_crossing_family_count"] == 1
    assert report.headline_metrics["rejected_local_cycle_family_count"] == 1
    assert report.headline_metrics[
        "exhaustive_width_five_separator_defect_code_count"
    ] == 1_920
    assert report.headline_metrics["exhaustive_positive_feedback_code_count"] == 0
    assert report.headline_metrics["feedback_family_failure_count"] == 0
    assert report.headline_metrics["control_failure_count"] == 0
    assert report.claim_gate["separator_feedback_pressure_bound_proved"]
    assert report.claim_gate["feedback_gate_crossing_family_constructed"]
    assert not report.claim_gate["feedback_rich_weak_relation_family_constructed"]
    assert report.claim_gate[
        "all_higher_codimension_separator_defect_codes_controlled"
    ]
    assert not report.claim_gate["speedup_claim_allowed"]
