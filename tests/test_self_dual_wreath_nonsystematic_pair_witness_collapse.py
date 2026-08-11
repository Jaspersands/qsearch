from functools import lru_cache

import pytest

from self_dual_wreath_nonsystematic_incidence_lattice_bound import (
    INDEX_THREE_CODE,
    RANK_DEFICIENT_CODE,
)
from self_dual_wreath_nonsystematic_mod_four_no_go import mod_four_code
from self_dual_wreath_nonsystematic_pair_witness_collapse import (
    audit_pair_witness_collapse,
    pair_witness_all_depth_certificate,
    pair_witness_elimination_steps,
    run_nonsystematic_pair_witness_collapse,
)
from self_dual_wreath_nonsystematic_twisted_star_no_go import twisted_star_code


CONTROLS = (
    ("INDEX-TWO", twisted_star_code(5), 2),
    ("INDEX-THREE", INDEX_THREE_CODE, 3),
    ("INDEX-FOUR", mod_four_code(6), 4),
    ("INFINITE-CYCLIC", RANK_DEFICIENT_CODE, 0),
)


@lru_cache(maxsize=1)
def _report():
    return run_nonsystematic_pair_witness_collapse()


@pytest.mark.parametrize(("control_id", "code", "expected_order"), CONTROLS)
def test_every_pair_witness_eliminates_the_next_generator_triangularly(
    control_id,
    code,
    expected_order,
):
    steps, signs = pair_witness_elimination_steps(code)
    assert len(steps) == len(code[0]) - 1
    assert len(signs) == len(code[0])
    assert signs[0] == 1
    for expected_coordinate, step in enumerate(steps, start=2):
        assert step.eliminated_coordinate_one_based == expected_coordinate
        assert all(
            coordinate < expected_coordinate
            for coordinate in step.common_middle_coordinates_one_based
        )
        assert step.root_sign in (-1, 1)
        assert step.middle_is_power_of_root
        assert step.relation_vanishes_after_solved_substitution
        assert step.exact_step_verified


@pytest.mark.parametrize(("control_id", "code", "expected_order"), CONTROLS)
def test_full_ordered_codeword_presentations_are_exactly_cyclic(
    control_id,
    code,
    expected_order,
):
    control = audit_pair_witness_collapse(control_id, code)
    assert control.all_coordinate_pairs_covered
    assert not control.has_dimension_sized_information_set
    assert control.codeword_presentation_remaining_generator_count == 1
    assert control.cyclic_order == expected_order
    assert control.exact_ordered_codeword_cyclic_collapse_verified


@pytest.mark.parametrize(("control_id", "code", "expected_order"), CONTROLS)
def test_marked_presentations_have_uniform_surface_loss(
    control_id,
    code,
    expected_order,
):
    control = audit_pair_witness_collapse(control_id, code)
    assert control.marked_support_difference_peeling_stalls
    assert control.marked_remaining_generator_count == 6
    assert control.marked_solution_exponent_upper_bound == 5.0
    assert "surface-genus-2" in control.marked_solution_exponent_certificate_source
    assert control.marked_true_pressure_margin_lower_bound > 2.0
    assert control.marked_residual_target_word
    assert control.exact_marked_control_verified


def test_affine_translation_needs_only_relative_codeword_relators():
    affine = tuple(
        sorted(
            tuple(bit ^ int(index == 0) for index, bit in enumerate(row))
            for row in twisted_star_code(5)
        )
    )
    assert (0, 0, 0, 0, 0) not in affine
    control = audit_pair_witness_collapse("AFFINE", affine)
    assert control.reference_codeword != (0, 0, 0, 0, 0)
    assert control.exact_ordered_codeword_cyclic_collapse_verified
    assert control.marked_remaining_generator_count <= 6
    assert control.marked_solution_exponent_upper_bound <= 5.0
    assert control.marked_true_pressure_margin_lower_bound > 2.0
    assert control.exact_marked_control_verified


def test_report_closes_all_no_information_set_scope_without_overclaiming():
    theorem = pair_witness_all_depth_certificate()
    assert theorem.arbitrary_width
    assert theorem.universal_no_information_set_no_go_verified
    assert theorem.symmetric_group_solution_exponent_upper_bound == 5.0
    report = _report()
    assert report.headline_metrics[
        "all_depth_pair_witness_collapse_theorem_count"
    ] == 1
    assert report.headline_metrics["stored_finite_cyclic_orders_realized"] == 3
    assert report.headline_metrics["infinite_cyclic_control_count"] == 1
    assert report.headline_metrics["control_failure_count"] == 0
    assert not report.claim_gate["nonabelian_pair_witness_kernel_survives"]
    assert not report.claim_gate[
        "normalized_no_information_set_actual_pressure_survives"
    ]
    assert report.claim_gate[
        "all_normalized_no_information_set_BABA_cores_controlled"
    ]
    assert report.claim_gate["all_unnormalized_no_information_set_cores_controlled"]
    assert report.claim_gate["all_no_information_set_BABA_cores_controlled"]
    assert not report.claim_gate["all_interleaved_information_set_cores_controlled"]
    assert not report.claim_gate["speedup_claim_allowed"]
