from functools import lru_cache

import pytest

from self_dual_wreath_codimension_two_universal_no_go import (
    _representative_codes,
    audit_codimension_two_code,
    audit_surface_coefficient_absorption,
    codimension_two_all_depth_certificate,
    find_information_set,
    information_set_elimination_steps,
    run_codimension_two_universal_no_go,
)


@lru_cache(maxsize=1)
def _report():
    return run_codimension_two_universal_no_go()


@pytest.mark.parametrize(
    "coefficient_word",
    (
        (6,),
        (6, -7, 6),
        (8, 7, -6, 8, -7),
        (6, 7, 8, -7, 9, -6, -9),
    ),
)
def test_arbitrary_residual_word_is_absorbed_by_one_nielsen_move(
    coefficient_word,
):
    control = audit_surface_coefficient_absorption(coefficient_word)
    assert control.nielsen_generator == 3
    assert control.inverse_nielsen_recovers_original
    assert control.transformed_surface_word == control.coefficient_free_surface_word
    assert control.orientable_surface_genus == 2
    assert control.exact_coefficient_absorption_verified


def test_information_set_steps_eliminate_only_their_own_information_pivots():
    for control_id, code in _representative_codes()[:3]:
        information_set = find_information_set(code)
        assert information_set is not None
        assert len(information_set) == len(code[0]) - 2
        steps = information_set_elimination_steps(code, information_set)
        assert len(steps) == len(information_set)
        assert all(step.pivot_occurrence_count == 1 for step in steps)
        assert all(
            step.other_information_generator_occurrence_count == 0
            for step in steps
        )
        assert all(step.exact_singleton_elimination_verified for step in steps)


def test_no_information_set_controls_use_pair_witness_branch():
    for control_id, code in _representative_codes()[3:]:
        assert find_information_set(code) is None
        control = audit_codimension_two_code(control_id, code)
        assert control.branch == "no-dimension-sized-information-set"
        assert control.pair_witness_elimination_count == control.code_width - 1
        assert control.theoretical_remaining_generator_upper_bound == 6
        assert control.theoretical_solution_exponent_upper_bound == 5.0
        assert control.theoretical_true_pressure_margin_lower_bound > 2.0
        assert control.exact_control_verified


@pytest.mark.parametrize(
    ("control_id", "code"),
    _representative_codes(),
)
def test_full_marked_controls_respect_the_universal_branch_bound(control_id, code):
    control = audit_codimension_two_code(control_id, code)
    assert control.minimum_distance >= 2
    assert control.all_codeword_relations_forced_by_mixed_supports
    assert control.support_difference_peeling_stalls_on_full_core
    assert (
        control.reducer_remaining_generator_count
        <= control.theoretical_remaining_generator_upper_bound
    )
    assert (
        control.reducer_solution_exponent_upper_bound
        <= control.theoretical_solution_exponent_upper_bound
    )
    assert (
        control.reducer_true_pressure_margin
        >= control.theoretical_true_pressure_margin_lower_bound - 1e-12
    )
    assert control.residual_target_word
    assert control.exact_control_verified


def test_report_closes_every_codimension_two_BABA_code_without_overclaiming():
    theorem = codimension_two_all_depth_certificate()
    assert theorem.arbitrary_width
    assert theorem.arbitrary_coordinate_order
    assert theorem.affine_normalization_not_required
    assert theorem.universal_codimension_two_BABA_no_go_verified
    assert theorem.information_set_solution_exponent_upper_bound == 6.0
    assert theorem.no_information_set_solution_exponent_upper_bound == 5.0
    report = _report()
    assert report.headline_metrics[
        "all_depth_codimension_two_universal_no_go_theorem_count"
    ] == 1
    assert report.headline_metrics["information_set_branch_control_count"] == 3
    assert report.headline_metrics["no_information_set_branch_control_count"] == 2
    assert report.headline_metrics["surface_coefficient_failure_count"] == 0
    assert report.headline_metrics["control_failure_count"] == 0
    assert report.claim_gate["all_codimension_two_BABA_stopping_cores_controlled"]
    assert not report.claim_gate["codimension_two_actual_pressure_survives"]
    assert not report.claim_gate["interleaved_information_set_escape_survives"]
    assert not report.claim_gate["no_information_set_escape_survives"]
    assert not report.claim_gate["affine_translation_escape_survives"]
    assert not report.claim_gate["all_higher_codimension_stopping_cores_controlled"]
    assert not report.claim_gate["speedup_claim_allowed"]
