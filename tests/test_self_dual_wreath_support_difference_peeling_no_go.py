import itertools

import pytest

from self_dual_wreath_support_difference_peeling_no_go import (
    audit_full_suffix_cube_lift,
    audit_support_difference_peeling_lift,
    run_support_difference_peeling_no_go,
)
from self_dual_wreath_target_survival_surface_seed import (
    target_survival_lift_supports,
    target_survival_power_boundary_supports,
)


@pytest.mark.parametrize("depth", range(1, 7))
def test_original_identity_lift_reduces_exactly_to_projected_seed(depth):
    _, same, different = target_survival_lift_supports(depth)
    control = audit_full_suffix_cube_lift(
        "ORIGINAL",
        tuple("BABA"),
        depth,
        same,
        different,
        (0, 0, 0, 0),
    )
    assert control.every_appended_generator_forced_to_identity
    assert len(control.forcing_witnesses) == depth
    assert all(
        row.exact_conjugate_identity_verified for row in control.forcing_witnesses
    )
    assert control.projected_same_support == ((1, 0, 1, 0),)
    assert control.projected_different_support == (
        (0, 0, 0, 0),
        (0, 1, 1, 1),
    )
    assert control.exact_relation_projection_verified
    assert control.exact_target_projection_verified
    assert control.exact_marked_tietze_reduction_verified


@pytest.mark.parametrize("depth", range(1, 7))
def test_power_boundary_lift_reduces_to_one_cell_projected_seed(depth):
    _, same, different = target_survival_power_boundary_supports(depth)
    control = audit_full_suffix_cube_lift(
        "POWER-BOUNDARY",
        tuple("BABA"),
        depth,
        same,
        different,
        (0, 0, 0, 0),
    )
    assert control.projected_same_support == ((1, 0, 1, 0),)
    assert control.projected_different_support == ((0, 0, 0, 0),)
    assert control.exact_marked_tietze_reduction_verified


def test_sparse_star_fiber_kills_every_coordinate_without_complete_cube():
    depth = 5
    zero = (0,) * depth
    same = ((1, 0, 1, 0, *zero),)
    different = (
        (0, 0, 0, 0, *zero),
        *tuple(
            (0, 0, 0, 0, *tuple(int(i == j) for i in range(depth)))
            for j in range(depth)
        ),
    )
    control = audit_support_difference_peeling_lift(
        "SPARSE-STAR",
        "E" + "BABA" + "A" * depth + "FEF",
        range(5, 5 + depth),
        same,
        different,
    )
    assert len(different) == depth + 1
    assert len(different) < 2**depth
    assert not control.uncovered_appended_coordinates_one_based
    assert control.every_appended_generator_forced_to_identity
    assert control.exact_marked_tietze_reduction_verified


def test_interleaved_edges_can_be_split_across_support_classes():
    control = audit_support_difference_peeling_lift(
        "INTERLEAVED",
        "EBAABAAFEF",
        (2, 5),
        (
            (0, 0, 0, 0, 0, 0),
            (0, 1, 0, 0, 0, 0),
        ),
        (
            (1, 0, 0, 1, 0, 1),
            (1, 0, 0, 1, 1, 1),
        ),
    )
    assert control.insertions_interleaved
    assert {row.support_kind for row in control.forcing_witnesses} == {
        "same",
        "different",
    }
    assert control.projected_pattern == "EBABAFEF"
    assert control.exact_marked_tietze_reduction_verified


def test_nonpeelable_difference_core_is_left_open_instead_of_overclaimed():
    control = audit_support_difference_peeling_lift(
        "EDGE-FREE",
        "EBAAFEF",
        (2, 3),
        ((0, 0, 0), (0, 1, 1)),
        (),
    )
    assert control.uncovered_appended_coordinates_one_based == (2, 3)
    assert control.support_difference_hyperedges_one_based == ((2, 3),)
    assert control.residual_core_is_stopping_set
    assert control.peeling_core_pattern == control.lifted_pattern
    assert control.exact_peeling_core_relation_projection_verified
    assert control.exact_peeling_core_target_projection_verified
    assert control.exact_peeling_core_tietze_reduction_verified
    assert control.nonpeelable_core_support_size_upper_bound == 4
    assert control.nonpeelable_core_half_cube_bound_verified
    assert control.scalar_pressure_cannot_increase_under_peeling
    assert not control.every_appended_generator_forced_to_identity
    assert control.exact_relation_projection_verified
    assert control.exact_target_projection_verified
    assert not control.exact_marked_tietze_reduction_verified


def test_multi_difference_pairs_bootstrap_after_singleton_seed():
    control = audit_support_difference_peeling_lift(
        "CHAIN",
        "EBABAAAAFEF",
        (5, 6, 7),
        ((1, 0, 1, 0, 0, 0, 0),),
        (
            (0, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 1, 0, 0),
            (0, 0, 0, 1, 0, 0, 0),
            (0, 0, 0, 1, 1, 1, 0),
            (0, 0, 1, 0, 0, 0, 0),
            (0, 0, 1, 0, 0, 1, 1),
        ),
    )
    assert control.direct_coordinate_edge_witness_count == 1
    assert control.multi_difference_peeling_witness_count == 2
    assert tuple(
        row.pair_difference_coordinates_one_based
        for row in control.forcing_witnesses
    ) == ((5,), (5, 6), (6, 7))
    assert tuple(
        row.appended_frame_coordinate_one_based
        for row in control.forcing_witnesses
    ) == (5, 6, 7)
    assert control.exact_marked_tietze_reduction_verified


def test_word_and_projection_identities_hold_exhaustively_through_width_four():
    for width in range(1, 5):
        zero = (0,) * width
        for frame_types in itertools.product("AB", repeat=width):
            pattern = "E" + "".join(frame_types) + "FEF"
            for mask in range(1, 1 << width):
                inserted = tuple(
                    index + 1 for index in range(width) if mask & (1 << index)
                )
                same = (
                    zero,
                    *tuple(
                        tuple(int(index == coordinate) for index in range(width))
                        for coordinate in range(width)
                        if coordinate + 1 in inserted
                    ),
                )
                control = audit_support_difference_peeling_lift(
                    "EXHAUSTIVE",
                    pattern,
                    inserted,
                    same,
                    (),
                )
                assert control.exact_marked_tietze_reduction_verified
                assert control.residual_core_is_stopping_set


def test_canonical_stopping_core_projection_exhaustive_through_width_three():
    for width in range(1, 4):
        assignments = tuple(itertools.product((0, 1), repeat=width))
        for frame_types in itertools.product("AB", repeat=width):
            pattern = "E" + "".join(frame_types) + "FEF"
            for mask in range(1, 1 << len(assignments)):
                same = tuple(
                    row
                    for index, row in enumerate(assignments)
                    if mask & (1 << index)
                )
                control = audit_support_difference_peeling_lift(
                    "EXHAUSTIVE-CORE",
                    pattern,
                    range(1, width + 1),
                    same,
                    (),
                )
                assert control.residual_core_is_stopping_set
                assert control.exact_peeling_core_relation_projection_verified
                assert control.exact_peeling_core_target_projection_verified
                assert control.exact_peeling_core_tietze_reduction_verified
                assert control.nonpeelable_core_half_cube_bound_verified
                assert control.scalar_pressure_cannot_increase_under_peeling


def test_missing_suffix_row_is_rejected_by_full_cube_corollary():
    _, same, different = target_survival_power_boundary_supports(3)
    with pytest.raises(ValueError, match="complete suffix fiber"):
        audit_full_suffix_cube_lift(
            "MISSING",
            tuple("BABA"),
            3,
            same,
            different[:-1],
            (0, 0, 0, 0),
        )


def test_report_closes_peelable_partial_and_interleaved_lifts_only():
    report = run_support_difference_peeling_no_go()
    assert report.headline_metrics[
        "all_pattern_support_difference_peeling_no_go_theorem_count"
    ] == 1
    assert report.headline_metrics["lift_control_failure_count"] == 0
    assert report.claim_gate[
        "support_difference_peelable_lifts_reduce_to_projection"
    ]
    assert report.claim_gate["partial_suffix_peelable_lifts_controlled"]
    assert report.claim_gate["interleaved_peelable_lifts_controlled"]
    assert report.claim_gate["multi_difference_peeling_controlled"]
    assert report.headline_metrics["stopping_set_boundary_theorem_count"] == 1
    assert report.headline_metrics[
        "canonical_peeling_core_projection_theorem_count"
    ] == 1
    assert report.headline_metrics[
        "peeling_scalar_pressure_monotonicity_theorem_count"
    ] == 1
    assert report.headline_metrics[
        "nonpeelable_core_half_cube_bound_theorem_count"
    ] == 1
    assert len(report.nonpeelable_boundary_controls) == 1
    assert report.nonpeelable_boundary_controls[
        0
    ].residual_core_is_stopping_set
    assert not report.claim_gate["all_partial_suffix_lifts_controlled"]
    assert not report.claim_gate["all_interleaved_lifts_controlled"]
    assert not report.claim_gate["nonpeelable_difference_core_lifts_controlled"]
    assert report.claim_gate[
        "nonpeelable_core_exactly_identified_as_stopping_set"
    ]
    assert report.claim_gate[
        "arbitrary_lift_reduces_to_canonical_peeling_core"
    ]
    assert not report.claim_gate["peeling_padding_can_improve_scalar_pressure"]
    assert report.claim_gate[
        "nonempty_stopping_core_requires_one_codensity_bit"
    ]
    assert not report.claim_gate["speedup_claim_allowed"]
