import math

import pytest

from self_dual_wreath_reversible_automaton_fiber_collapse import (
    advance_reversible_counts,
    audit_ordered_subword_suffix_control,
    audit_reversible_program,
    build_reversible_automaton_fiber_report,
    cyclic_ordered_subword_pair_program,
    enumerate_endpoint_fiber,
    reversible_automaton_scaling_record,
    sharp_reversible_program,
    write_reversible_automaton_fiber_report,
)


def test_stable_support_layers_double_minimum_positive_multiplicity():
    identity = (0, 1, 2)
    swap = (1, 0, 2)
    counts = (1, 1, 0)
    output = advance_reversible_counts(counts, (identity, swap))
    assert output == (2, 2, 0)

    with pytest.raises(ValueError, match="permutations"):
        advance_reversible_counts(counts, (identity, (0, 0, 2)))


@pytest.mark.parametrize(("state_count", "layer_count"), ((4, 11), (6, 14)))
def test_support_growth_bound_is_sharp_for_general_reversible_programs(
    state_count,
    layer_count,
):
    row = audit_reversible_program(
        sharp_reversible_program(state_count, layer_count),
        control_id=f"sharp-{state_count}",
    )
    assert row.support_growth_step_count == state_count - 1
    assert row.stable_support_step_count == layer_count - state_count + 1
    assert row.minimum_positive_fiber_size == 2 ** (
        layer_count - state_count + 1
    )
    assert row.theorem_fiber_size_lower_bound == row.minimum_positive_fiber_size
    assert row.lower_bound_attained
    assert row.all_positive_fibers_meet_bound
    assert all(record.layer_inequality_verified for record in row.layer_records)


def test_selected_complement_finite_group_program_is_reversible():
    transitions = cyclic_ordered_subword_pair_program(
        3,
        (1, 2, 1, 1, 2, 2, 1, 2, 1, 2),
    )
    row = audit_reversible_program(transitions, control_id="z3-pair")
    assert row.state_count == 9
    assert row.every_transition_pair_reversible
    assert row.every_layer_inequality_verified
    assert row.minimum_positive_fiber_size >= 2 ** (10 - 9 + 1)
    assert row.minimum_positive_fiber_density >= 2 ** -8

    fiber = enumerate_endpoint_fiber(transitions, 0)
    assert fiber
    assert all(len(assignment) == 10 for assignment in fiber)


def test_suffix_entropy_turns_constant_density_into_constant_generator_rank():
    transitions = sharp_reversible_program(4, 11)
    row = audit_ordered_subword_suffix_control(
        transitions,
        control_id="sharp-suffix",
    )
    assert row.endpoint_fiber_size == 2 ** (11 - 4 + 1)
    assert row.entropy_codimension == pytest.approx(3.0)
    assert row.suffix_forced_generator_count <= 3
    assert row.suffix_entropy_generator_upper_bound == 3
    assert row.triangular_suffix_certificate_verified
    assert row.constant_generator_bound_verified


def test_scaling_closes_fixed_state_but_not_growing_state_routes():
    for state_count in (6, 24, 36, 120):
        row = reversible_automaton_scaling_record(
            state_count,
            8 * state_count,
        )
        assert row.minimum_full_fiber_density_log2 == -(state_count - 1)
        assert row.full_fiber_entropy_codimension_upper_bound == state_count - 1
        assert row.suffix_frame_generator_upper_bound == state_count - 1
        assert row.entropy_compensated_scalar_pressure_upper_bound == -1.0
        assert row.constant_density_theorem_certified


def test_report_keeps_component_and_growing_state_routes_open(tmp_path):
    report = build_reversible_automaton_fiber_report()
    assert report.theorem.theorem_verified
    assert report.theorem.every_nonempty_reversible_fiber_constant_density_proved
    assert report.theorem.general_bound_sharp_proved
    assert report.theorem.finite_group_ordered_subword_automata_covered
    assert report.theorem.constant_suffix_generator_bound_under_relator_contract_proved
    assert not report.theorem.arbitrary_reversible_presentation_covered
    assert not report.theorem.positive_component_signal_proved
    assert not report.claim_gate[
        "constant_state_growing_suffix_dimension_under_contract_alive"
    ]
    assert report.claim_gate["growing_state_automaton_route_alive"]
    assert report.claim_gate["scalar_saturating_component_signal_route_alive"]
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_reversible_automaton_fiber_report(
        tmp_path / "reversible-fiber.json"
    )
    assert payload["status"] == (
        "constant-state-reversible-frame-fiber-escape-closed"
    )
