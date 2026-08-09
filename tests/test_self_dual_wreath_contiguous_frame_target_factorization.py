import itertools

import pytest

from self_dual_wreath_contiguous_frame_target_factorization import (
    audit_contiguous_frame_target_factorization,
    audit_target_survival_identity_frame_lift,
    run_contiguous_frame_target_factorization,
)


def test_outer_and_target_factorizations_hold_for_all_types_and_bases_through_width_five():
    for width in range(1, 6):
        zero = ((0,) * width,)
        for frame_types in itertools.product("AB", repeat=width):
            for base in itertools.product((0, 1), repeat=width):
                control = audit_contiguous_frame_target_factorization(
                    "EXHAUSTIVE-SYMBOLIC",
                    frame_types,
                    zero,
                    (base,),
                )
                assert control.exact_outer_conjugacy_factorization_verified
                assert control.exact_target_conjugacy_factorization_verified
                assert control.exact_mixed_frame_scalar_pressure_verified


def test_all_a_target_is_freely_killed():
    control = audit_contiguous_frame_target_factorization(
        "ALL-A",
        ("A", "A", "A", "A"),
        ((0, 0, 0, 0),),
        ((0, 0, 0, 0),),
    )
    assert not control.target_frame_word
    assert not control.selected_frame_target_residual
    assert control.full_presentation_symbolically_kills_target


def test_alternating_frames_leave_the_split_genus_one_commutator():
    control = audit_contiguous_frame_target_factorization(
        "ABAB",
        ("A", "B", "A", "B"),
        ((0, 1, 0, 1),),
        ((0, 0, 0, 0),),
    )
    assert control.split_b_run_count == 2
    assert control.split_target_genus == 1
    assert control.target_frame_word
    assert control.selected_frame_target_residual
    assert control.selected_frame_target_orientable_genus == 1
    assert control.full_reduced_frame_target_residual
    assert control.full_reduced_frame_target_orientable_genus == 1
    assert not control.zero_same_assignment_present
    assert control.scalar_crossing_pressure_margin == 1
    assert control.target_survival_pressure_tradeoff_verified
    assert not control.weighted_frame_character_bound_proved


def test_support_relations_can_kill_a_split_surviving_target():
    control = audit_contiguous_frame_target_factorization(
        "ABAB-KILLED",
        ("A", "B", "A", "B"),
        ((0, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 1)),
        ((0, 0, 0, 0),),
    )
    assert control.split_target_genus == 1
    assert not control.selected_frame_target_residual
    assert not control.full_reduced_frame_target_residual
    assert control.full_presentation_symbolically_kills_target


def test_scalar_pressure_saturation_forces_target_identity():
    control = audit_contiguous_frame_target_factorization(
        "SATURATING",
        ("A", "B", "A", "B"),
        ((0, 0, 0, 0), (0, 1, 0, 1)),
        ((0, 0, 0, 0), (1, 0, 1, 0)),
    )
    assert control.scalar_crossing_pressure_margin == 0
    assert control.scalar_pressure_saturation_condition_verified
    assert control.zero_same_assignment_present
    assert control.zero_same_cell_forces_target_identity
    assert control.full_reduced_frame_target_is_relator


def test_nonzero_target_has_quantified_strict_pressure_margin():
    same = ((0, 0, 1), (0, 1, 0), (1, 0, 0))
    different = (
        (0, 0, 0),
        (0, 0, 1),
        (0, 1, 0),
        (1, 0, 0),
    )
    control = audit_contiguous_frame_target_factorization(
        "MINIMAL-MARGIN",
        ("A", "B", "B"),
        same,
        different,
    )
    assert not control.zero_same_assignment_present
    assert control.nonzero_target_pressure_margin_lower_bound > 0
    assert control.scalar_crossing_pressure_margin == pytest.approx(
        control.nonzero_target_pressure_margin_lower_bound
    )
    assert control.target_survival_pressure_tradeoff_verified


def test_integer_suffix_branch_bound_closes_old_identity_frame_margin_falsifier():
    controls = [
        audit_target_survival_identity_frame_lift(depth)
        for depth in range(9)
    ]
    assert all(row.exact_identity_frame_lift_verified for row in controls)
    assert all(row.all_full_presentation_relations_satisfied for row in controls)
    assert all(row.target_is_nonidentity for row in controls)
    assert [row.same_support_size for row in controls] == [
        2**depth for depth in range(9)
    ]
    assert [row.different_support_size for row in controls] == [
        2**depth + 1 for depth in range(9)
    ]
    assert all(
        later.real_entropy_certificate_margin
        < earlier.real_entropy_certificate_margin
        for earlier, later in zip(controls, controls[1:])
    )
    assert all(
        later.scalar_crossing_pressure_margin
        > earlier.scalar_crossing_pressure_margin
        for earlier, later in zip(controls, controls[1:])
    )
    assert controls[-1].scalar_crossing_pressure_margin > 0.99


def test_report_keeps_weighted_character_gate_closed():
    report = run_contiguous_frame_target_factorization(maximum_frame_count=6)
    metrics = report.headline_metrics
    assert metrics["checked_frame_type_base_pair_count"] == sum(
        4**width for width in range(1, 7)
    )
    assert metrics["outer_factorization_failure_count"] == 0
    assert metrics["target_factorization_failure_count"] == 0
    assert metrics["growing_width_mixed_frame_scalar_pressure_theorem_count"] == 1
    assert metrics["exact_target_to_frame_character_reduction_theorem_count"] == 1
    assert metrics["target_survival_strict_pressure_tradeoff_theorem_count"] == 1
    assert metrics[
        "growing_width_uniform_target_survival_pressure_gap_theorem_count"
    ] == 0
    assert metrics["exact_S3_target_survival_identity_frame_lift_count"] == 13
    assert metrics["target_survival_lift_failure_count"] == 0
    assert metrics["real_entropy_certificate_gap_falsified_count"] == 1
    assert metrics["integer_suffix_branch_identity_lift_gap_closed_count"] == 1
    assert metrics["uniform_certificate_pressure_gap_falsified_count"] == 0
    assert metrics["power_boundary_integer_certificate_gap_falsified_count"] == 1
    assert metrics["power_boundary_actual_presentation_escape_count"] == 0
    assert metrics["weighted_frame_character_theorem_count"] == 0
    assert report.claim_gate["contiguous_mixed_frame_scalar_pressure_proved"]
    assert report.claim_gate["target_character_value_reduced_to_frame_word"]
    assert report.claim_gate["pressure_saturation_forces_target_identity"]
    assert report.claim_gate["fixed_width_nontrivial_target_strictly_subthreshold"]
    assert not report.claim_gate["growing_width_uniform_target_survival_gap_proved"]
    assert report.claim_gate["real_entropy_certificate_gap_falsified"]
    assert report.claim_gate[
        "identity_lift_closed_by_integer_suffix_branch_bound"
    ]
    assert not report.claim_gate["uniform_certificate_pressure_gap_falsified"]
    assert report.claim_gate[
        "power_boundary_integer_certificate_gap_falsified"
    ]
    assert not report.claim_gate[
        "power_boundary_actual_presentation_survives"
    ]
    assert not report.claim_gate["asymptotic_Sn_target_survival_lower_bound_proved"]
    assert not report.claim_gate["weighted_frame_character_average_controlled"]
    assert not report.claim_gate["speedup_claim_allowed"]
