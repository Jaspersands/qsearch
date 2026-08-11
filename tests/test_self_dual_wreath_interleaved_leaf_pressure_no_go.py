from functools import lru_cache

import itertools

import pytest

from self_dual_wreath_interleaved_leaf_pressure_no_go import (
    audit_interleaved_leaf_pressure,
    audit_interleaved_outer_conjugacy,
    exhaustive_outer_scaling,
    exhaustive_support_census,
    interleaved_leaf_all_depth_certificate,
    interleaved_pair_pattern,
    interleaved_suffix_pivot_steps,
    run_interleaved_leaf_pressure_no_go,
)


@lru_cache(maxsize=1)
def _report():
    return run_interleaved_leaf_pressure_no_go()


@pytest.mark.parametrize(
    ("blocks", "types", "base"),
    (
        ((0, 0, 0, 0), (), ()),
        ((4, 0, 0, 0), ("A", "B", "A", "B"), (1, 0, 1, 0)),
        ((1, 1, 1, 1), ("B", "A", "B", "A"), (1, 1, 0, 1)),
        ((0, 2, 0, 3), ("B", "B", "A", "B", "A"), (0, 1, 1, 0, 1)),
    ),
)
def test_outer_relations_always_reduce_to_coefficient_twisted_conjugacy(
    blocks,
    types,
    base,
):
    control = audit_interleaved_outer_conjugacy(blocks, types, base)
    e = control.first_E_generator
    f = control.first_F_generator
    assert control.residual_leaf_occurrence_word == (e, f, -e, -f)
    assert control.transformed_conjugacy_relation == (
        control.expected_conjugacy_relation
    )
    assert control.uniform_finite_group_outer_bound == "|G|*k(G)"
    assert control.exact_coefficient_conjugacy_normal_form_verified


def test_fixed_interleaved_F_markers_cancel_above_every_suffix_pivot():
    pattern = interleaved_pair_pattern((1, 1, 1, 1), ("A", "B", "A", "B"))
    support = tuple(itertools.product((0, 1), repeat=4))
    certificate, steps = interleaved_suffix_pivot_steps(
        pattern,
        support,
        support_kind="different",
    )
    assert certificate.exact_suffix_branch_elimination_verified
    assert len(steps) == 4
    assert all(
        step.pivot_occurrence_count == 1
        and step.higher_frame_generator_occurrence_count == 0
        and step.endpoint_relators_available
        and step.exact_marker_stable_suffix_pivot_verified
        for step in steps
    )


def test_scalar_saturation_requires_zero_same_cell_and_kills_target():
    support = (
        (0, 0, 0, 0),
        (1, 1, 0, 0),
        (0, 0, 1, 1),
        (1, 1, 1, 1),
    )
    different = (
        (1, 0, 1, 0),
        (0, 1, 0, 1),
        (1, 1, 0, 0),
        (0, 0, 1, 1),
    )
    control = audit_interleaved_leaf_pressure(
        "SATURATION",
        (1, 1, 1, 1),
        ("A", "B", "A", "B"),
        support,
        different,
    )
    assert control.scalar_crossing_pressure_upper_bound == pytest.approx(-1.0)
    assert control.scalar_crossing_pressure_margin == pytest.approx(0.0)
    assert control.scalar_pressure_saturated
    assert control.saturation_condition_verified
    assert control.zero_same_assignment_present
    assert control.zero_same_cell_forces_target_identity
    assert control.exact_control_verified


def test_pruned_power_boundary_has_strict_but_vanishing_generic_margin():
    for width in range(2, 9):
        cube = tuple(itertools.product((0, 1), repeat=width))
        zero = (0,) * width
        blocks = (width // 4, width // 4, width // 4, width - 3 * (width // 4))
        control = audit_interleaved_leaf_pressure(
            f"PRUNED-{width}",
            blocks,
            tuple("AB"[index % 2] for index in range(width)),
            tuple(row for row in cube if row != zero),
            cube,
        )
        assert not control.scalar_pressure_saturated
        assert control.scalar_crossing_pressure_margin > 0
        assert control.nontrivial_target_strict_finite_width_margin
        assert control.exact_control_verified
    width_eight = audit_interleaved_leaf_pressure(
        "PRUNED-8-CHECK",
        (2, 2, 2, 2),
        tuple("AB"[index % 2] for index in range(8)),
        tuple(row for row in itertools.product((0, 1), repeat=8) if any(row)),
        tuple(itertools.product((0, 1), repeat=8)),
    )
    assert width_eight.scalar_crossing_pressure_margin < 0.01


def test_exhaustive_outer_normal_form_screen_has_no_failure():
    scaling = exhaustive_outer_scaling()
    assert sum(row.checked_placement_type_base_count for row in scaling) == 67_761
    assert sum(row.outer_normal_form_failure_count for row in scaling) == 0
    assert max(row.frame_position_count for row in scaling) == 5


def test_exhaustive_width_three_support_pair_census_passes():
    census = exhaustive_support_census()
    assert census.nonempty_support_count == 255
    assert census.checked_support_pair_count == 65_025
    assert census.same_suffix_certificate_failure_count == 0
    assert census.different_marker_suffix_certificate_failure_count == 0
    assert census.pressure_inequality_failure_count == 0
    assert census.saturation_equivalence_failure_count == 0
    assert census.saturated_support_pair_count > 0
    assert census.minimum_pressure_margin == pytest.approx(0.0)
    assert census.exhaustive_census_verified


def test_all_depth_certificate_has_correct_scope_and_claim_boundary():
    theorem = interleaved_leaf_all_depth_certificate()
    assert theorem.arbitrary_frame_width
    assert theorem.arbitrary_leaf_placement
    assert theorem.arbitrary_frame_types
    assert theorem.arbitrary_nonempty_supports
    assert theorem.universal_interleaved_scalar_no_go_verified
    assert theorem.uniform_finite_group_outer_bound == "|G|*k(G)"


def test_report_closes_scalar_interleaving_but_not_signed_or_higher_boundary():
    report = _report()
    assert report.headline_metrics[
        "all_depth_interleaved_leaf_scalar_no_go_theorem_count"
    ] == 1
    assert report.headline_metrics["control_failure_count"] == 0
    assert report.headline_metrics[
        "exhaustive_outer_normal_form_failure_count"
    ] == 0
    assert report.headline_metrics["exhaustive_support_census_failure_count"] == 0
    assert report.claim_gate["interleaved_F_marker_suffix_elimination_proved"]
    assert report.claim_gate["interleaved_outer_conjugacy_bound_proved"]
    assert report.claim_gate["all_four_leaf_pair_word_scalar_pressure_controlled"]
    assert report.claim_gate["scalar_saturation_forces_target_identity"]
    assert not report.claim_gate["uniform_growing_nontrivial_target_gap_proved"]
    assert not report.claim_gate["higher_multi_boundary_words_controlled"]
    assert not report.claim_gate["speedup_claim_allowed"]
