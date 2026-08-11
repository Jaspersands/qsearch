from functools import lru_cache

import pytest

from self_dual_wreath_information_set_universal_no_go import (
    _representative_information_set_codes,
    audit_information_set_code,
    find_dimension_information_set,
    information_set_all_depth_certificate,
    run_information_set_universal_no_go,
)


@lru_cache(maxsize=1)
def _report():
    return run_information_set_universal_no_go()


@pytest.mark.parametrize(
    ("control_id", "code"),
    _representative_information_set_codes(),
)
def test_dimension_sized_information_sets_exist_at_multiple_codimensions(
    control_id,
    code,
):
    information_set = find_dimension_information_set(code)
    assert information_set is not None
    assert len(information_set) == (len(code).bit_length() - 1)
    assert len(
        {tuple(row[index] for index in information_set) for row in code}
    ) == len(code)


@pytest.mark.parametrize(
    ("control_id", "code"),
    _representative_information_set_codes(),
)
def test_unit_information_projections_eliminate_every_information_generator(
    control_id,
    code,
):
    control = audit_information_set_code(control_id, code)
    assert len(control.elimination_steps) == control.information_dimension
    for step in control.elimination_steps:
        assert step.pivot_occurrence_count == 1
        assert step.other_information_generator_occurrence_count == 0
        assert step.exact_singleton_elimination_verified
    assert control.all_information_generators_eliminated


@pytest.mark.parametrize(
    ("control_id", "code"),
    _representative_information_set_codes(),
)
def test_full_marked_presentations_obey_d_plus_four_exponent_bound(
    control_id,
    code,
):
    control = audit_information_set_code(control_id, code)
    assert control.minimum_distance >= 2
    assert control.all_codeword_relations_forced_by_mixed_supports
    assert control.support_difference_peeling_stalls_on_full_core
    assert (
        control.theoretical_remaining_generator_upper_bound
        == control.codimension + 5
    )
    assert (
        control.theoretical_solution_exponent_upper_bound
        == control.codimension + 4
    )
    assert (
        control.reducer_remaining_generator_count
        <= control.theoretical_remaining_generator_upper_bound
    )
    assert (
        control.reducer_solution_exponent_upper_bound
        <= control.theoretical_solution_exponent_upper_bound
    )
    assert control.theoretical_true_pressure_margin_lower_bound > 1.0
    assert control.reducer_true_pressure_margin >= (
        control.theoretical_true_pressure_margin_lower_bound - 1e-12
    )
    assert control.residual_target_word
    assert control.exact_control_verified


def test_report_closes_all_information_set_codes_without_closing_separator_defects():
    theorem = information_set_all_depth_certificate()
    assert theorem.arbitrary_information_dimension
    assert theorem.arbitrary_codimension
    assert theorem.arbitrary_coordinate_order
    assert theorem.affine_normalization_not_required
    assert theorem.universal_information_set_BABA_no_go_verified
    report = _report()
    assert report.headline_metrics[
        "all_depth_information_set_universal_no_go_theorem_count"
    ] == 1
    assert report.headline_metrics["maximum_stored_codimension"] == 5
    assert report.headline_metrics["interleaved_control_count"] >= 2
    assert report.headline_metrics["affine_control_count"] == 1
    assert report.headline_metrics["control_failure_count"] == 0
    assert report.claim_gate["all_information_set_BABA_cores_controlled"]
    assert not report.claim_gate["information_set_actual_pressure_survives"]
    assert not report.claim_gate["interleaved_information_set_escape_survives"]
    assert not report.claim_gate["high_codimension_information_set_escape_survives"]
    assert not report.claim_gate[
        "all_higher_codimension_separator_defect_codes_controlled"
    ]
    assert not report.claim_gate["speedup_claim_allowed"]
