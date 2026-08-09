import itertools
import math
from functools import lru_cache

import pytest

from self_dual_wreath_boolean_graph_stopping_core_pressure import (
    algebraic_normal_form_degree,
    boolean_face_relator_certificate,
    boolean_function_table,
    boolean_graph_code,
    minimum_hamming_distance,
    proper_four_color_face_certificates,
    proper_four_coloring_code,
    proper_four_coloring_table,
    run_boolean_graph_stopping_core_pressure,
)


@lru_cache(maxsize=1)
def _report():
    return run_boolean_graph_stopping_core_pressure()


@pytest.mark.parametrize("values", itertools.product((0, 1), repeat=3))
def test_all_boolean_face_words_have_a_bounded_loss_normal_form(values):
    certificate = boolean_face_relator_certificate(*values)
    assert certificate.residual_word
    assert certificate.two_generator_solution_exponent_upper_bound <= 1.5
    assert certificate.normal_form_kind in {
        "involution",
        "solve-generator",
        "inverse-conjugacy",
        "involution-after-nielsen",
        "solve-after-nielsen",
    }
    assert certificate.exact_case_classification_verified


@pytest.mark.parametrize("width", (2, 3, 4, 5))
@pytest.mark.parametrize(
    "family",
    ("zero", "and", "quadratic_cycle", "majority", "random"),
)
def test_boolean_graph_code_is_nonpeelable_for_arbitrary_check_function(
    width,
    family,
):
    table = boolean_function_table(width, family)
    code = boolean_graph_code(width, table)
    assert table[0] == 0
    assert len(code) == 2**width
    assert minimum_hamming_distance(code) >= 2
    assert all(row[-2] == sum(row[:-2]) % 2 for row in code)


def test_algebraic_normal_form_detects_affine_and_high_degree_controls():
    assert algebraic_normal_form_degree(boolean_function_table(4, "zero")) == 0
    assert algebraic_normal_form_degree(boolean_function_table(4, "and")) == 4
    assert algebraic_normal_form_degree(
        boolean_function_table(4, "quadratic_cycle")
    ) == 2


def test_all_proper_four_color_square_patterns_have_one_exceptional_ordering():
    certificates = proper_four_color_face_certificates()
    assert len(certificates) == 21
    exceptional = [
        row for row in certificates if row.exceptional_ordered_linear_cancellation
    ]
    assert len(exceptional) == 1
    assert exceptional[0].first_singleton_color == (0, 1)
    assert exceptional[0].second_singleton_color == (1, 0)
    assert exceptional[0].opposite_corner_color == (1, 1)
    assert exceptional[0].residual_word == ()
    assert all(
        row.two_generator_solution_exponent_upper_bound <= 1.5
        for row in certificates
        if not row.exceptional_ordered_linear_cancellation
    )
    assert all(row.exact_case_classification_verified for row in certificates)


def test_nonfactor_proper_four_coloring_builds_a_stopping_code():
    table = proper_four_coloring_table(3, "nonfactor_width_three")
    code = proper_four_coloring_code(3, table)
    assert len(code) == 8
    assert minimum_hamming_distance(code) >= 2
    control = next(
        row
        for row in _report().proper_four_coloring_controls
        if row.coloring_family == "nonfactor_width_three"
    )
    assert not control.has_linear_parity_factor
    assert control.selected_nonexceptional_face.residual_word
    assert control.local_face_pressure_margin > 0.5
    assert control.exact_control_verified


def test_representative_nonlinear_codes_restore_half_exponent_gap():
    report = _report()
    assert report.headline_metrics["stored_nonlinear_graph_code_control_count"] > 0
    for control in report.representative_controls:
        expected = 0.5 + 0.5 * math.log2(
            2**control.information_width
            / (2**control.information_width - 1)
        )
        assert control.support_difference_peeling_stalls_on_full_core
        assert control.remaining_generator_count <= 7
        assert control.reducer_solution_exponent_upper_bound <= 6.5
        assert control.local_face_pressure_margin == pytest.approx(expected)
        assert control.reducer_pressure_margin >= control.local_face_pressure_margin
        assert control.exact_control_verified


def test_report_controls_arbitrary_boolean_graph_functions_without_overclaiming():
    report = _report()
    assert report.headline_metrics[
        "all_depth_boolean_graph_core_no_go_theorem_count"
    ] == 1
    assert report.headline_metrics["classified_boolean_face_case_count"] == 8
    assert report.headline_metrics[
        "classified_proper_four_color_face_case_count"
    ] == 21
    assert report.headline_metrics[
        "exceptional_proper_four_color_face_case_count"
    ] == 1
    assert report.headline_metrics["face_case_failure_count"] == 0
    assert report.headline_metrics["control_failure_count"] == 0
    assert report.claim_gate["nonlinear_nonpeelable_graph_codes_constructed"]
    assert report.claim_gate["all_eight_local_face_words_controlled"]
    assert report.claim_gate["arbitrary_boolean_graph_function_controlled"]
    assert report.claim_gate["all_proper_four_color_face_words_classified"]
    assert report.claim_gate[
        "all_systematic_codimension_two_stopping_codes_controlled"
    ]
    assert not report.claim_gate["boolean_graph_core_actual_pressure_survives"]
    assert not report.claim_gate["all_codimension_two_stopping_codes_controlled"]
    assert not report.claim_gate["all_nonlinear_stopping_cores_controlled"]
    assert not report.claim_gate["speedup_claim_allowed"]
