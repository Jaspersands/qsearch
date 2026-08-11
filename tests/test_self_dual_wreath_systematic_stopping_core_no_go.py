import math
from functools import lru_cache

import pytest

from self_dual_wreath_systematic_stopping_core_no_go import (
    audit_systematic_coloring_space,
    audit_systematic_stopping_core,
    representative_systematic_coloring,
    run_systematic_stopping_core_no_go,
    systematic_graph_code,
    validate_systematic_coloring,
)


@lru_cache(maxsize=1)
def _report():
    return run_systematic_stopping_core_no_go()


@pytest.mark.parametrize(
    "control_id",
    (
        "NONEMPTY-QUADRATIC-FACE",
        "NONEMPTY-PRIMITIVE-FACE",
        "HIGHER-WEIGHT-DEVIATION",
        "EXACT-BLOCK-UNION",
        "GAPPED-BLOCK-UNION",
    ),
)
def test_representative_systematic_graph_codes_are_nonpeelable_controls(
    control_id,
):
    information_width, check_width, table = representative_systematic_coloring(
        control_id
    )
    validate_systematic_coloring(information_width, check_width, table)
    code = systematic_graph_code(information_width, check_width, table)
    control = audit_systematic_stopping_core(control_id)
    assert len(code) == 2**information_width
    assert control.minimum_code_distance >= 2
    assert control.support_difference_peeling_stalls_on_full_core
    assert control.exact_control_verified


def test_nonempty_face_branches_have_a_uniform_local_loss():
    for control_id in (
        "NONEMPTY-QUADRATIC-FACE",
        "NONEMPTY-PRIMITIVE-FACE",
    ):
        control = audit_systematic_stopping_core(control_id)
        assert control.nonempty_origin_face_count > 0
        assert control.selected_nonempty_face_certificate is not None
        assert control.selected_nonempty_face_certificate.residual_word
        assert (
            control.selected_nonempty_face_certificate
            .elementary_solution_exponent_loss_lower_bound
            >= 0.5
        )
        assert control.theoretical_local_solution_exponent_loss >= 0.5


def test_higher_weight_deviation_is_a_primitive_constraint():
    control = audit_systematic_stopping_core("HIGHER-WEIGHT-DEVIATION")
    assert control.all_origin_faces_cancel
    assert control.reverse_block_singleton_structure_verified
    assert control.higher_weight_block_union_deviation_count == 1
    assert control.selected_higher_weight_deviation_word
    assert control.higher_weight_deviation_has_once_occurring_generator
    assert not control.exact_block_union_coloring
    assert control.theoretical_local_solution_exponent_loss == 1.0


@pytest.mark.parametrize(
    "control_id",
    ("EXACT-BLOCK-UNION", "GAPPED-BLOCK-UNION"),
)
def test_exact_block_union_branch_has_fixed_surface_loss(control_id):
    control = audit_systematic_stopping_core(control_id)
    assert control.all_origin_faces_cancel
    assert control.reverse_block_singleton_structure_verified
    assert control.higher_weight_block_union_deviation_count == 0
    assert control.exact_block_union_coloring
    assert control.reducer_solution_exponent_upper_bound <= control.check_width + 4
    assert control.true_pressure_margin_lower_bound > 1.0


@pytest.mark.parametrize(
    ("information_width", "check_width"),
    ((2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (4, 1)),
)
def test_small_systematic_coloring_spaces_exhaust_the_three_branches(
    information_width,
    check_width,
):
    audit = audit_systematic_coloring_space(information_width, check_width)
    assert audit.proper_coloring_count > 0
    assert (
        audit.nonempty_origin_face_branch_count
        + audit.higher_weight_deviation_branch_count
        + audit.exact_block_union_branch_count
        == audit.proper_coloring_count
    )
    assert audit.face_certificate_failure_count == 0
    assert audit.empty_face_block_rigidity_failure_count == 0
    assert audit.deviation_singleton_failure_count == 0
    assert audit.minimum_distance_failure_count == 0
    assert audit.branch_exhaustion_failure_count == 0
    assert audit.exhaustive_classification_verified


def test_all_depth_report_closes_only_the_systematic_single_fiber_scope():
    report = _report()
    theorem = report.all_depth_certificate
    assert theorem.arbitrary_information_width
    assert theorem.arbitrary_check_width
    assert theorem.universal_systematic_core_no_go_verified
    assert report.headline_metrics[
        "all_depth_systematic_stopping_core_no_go_theorem_count"
    ] == 1
    assert report.headline_metrics[
        "exhaustively_checked_normalized_coloring_count"
    ] == 49_864
    assert report.headline_metrics["exhaustive_coloring_audit_failure_count"] == 0
    assert report.headline_metrics["control_failure_count"] == 0
    assert report.headline_metrics["uniform_true_pressure_margin_lower_bound"] == 0.5
    for control in report.representative_controls:
        expected = 0.5 * math.log2(
            2**control.information_width
            / (2**control.information_width - 1)
        )
        assert control.generic_integer_certificate_margin == pytest.approx(expected)
        assert control.true_pressure_margin_lower_bound >= expected + 0.5 - 1e-12
    assert report.claim_gate[
        "all_systematic_stopping_core_power_boundaries_controlled"
    ]
    assert not report.claim_gate[
        "systematic_stopping_core_actual_pressure_survives"
    ]
    assert not report.claim_gate["all_non_systematic_stopping_codes_controlled"]
    assert not report.claim_gate["all_multiple_base_fiber_patterns_controlled"]
    assert not report.claim_gate["natural_component_M4_positive"]
    assert not report.claim_gate["speedup_claim_allowed"]
