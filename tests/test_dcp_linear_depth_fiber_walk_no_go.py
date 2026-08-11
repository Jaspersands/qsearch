import math

import pytest

from dcp_linear_depth_fiber_walk_no_go import (
    audit_exact_trigger_control,
    legal_probability_lower_bound,
    linear_depth_fiber_walk_no_go_theorem,
    move_union_bound_logs,
    run_linear_depth_fiber_walk_no_go,
    scaling_record,
)


def test_no_trigger_control_has_no_edges_in_any_fiber() -> None:
    control = audit_exact_trigger_control(
        "no-trigger",
        (1, 2, 4, 8, 3, 5),
        modulus_bits=8,
        depth=4,
        block_size=2,
    )
    assert control.total_trigger_count == 0
    assert control.total_graph_edge_count == 0
    assert control.maximum_fiber_vertex_count > 1
    assert control.no_trigger_implies_every_fiber_edgeless


def test_trigger_families_are_detected() -> None:
    flip = audit_exact_trigger_control(
        "flip", (0, 1, 2, 4, 7, 9), 8, 4, 2
    )
    swap = audit_exact_trigger_control(
        "swap", (1, 17, 2, 4, 7, 9), 8, 4, 2
    )
    assert flip.divisible_coordinate_trigger_count >= 1
    assert swap.equal_residue_pair_trigger_count >= 1
    assert flip.total_graph_edge_count > 0
    assert swap.total_graph_edge_count > 0


def test_move_union_bound_decays_at_linear_depth() -> None:
    small = move_union_bound_logs(130, 64, 14, 128**3)[-1]
    large = move_union_bound_logs(514, 256, 18, 512**3)[-1]
    assert large < small
    assert large < -100


def test_low_fiber_legal_probability_is_near_one() -> None:
    bound = legal_probability_lower_bound(register_count=128, depth=64)
    assert 1 - bound < 2**-60
    with pytest.raises(ValueError, match="depth"):
        legal_probability_lower_bound(4, 5)


def test_scaling_proves_edgeless_exponential_fragmentation() -> None:
    row = scaling_record(
        n_bits=1024,
        register_offset=2,
        depth_fraction=0.5,
        block_log_multiplier=2,
        block_family_power=3,
    )
    assert row.mean_fiber_log2_size == 514
    assert row.log2_any_move_union_bound < -400
    assert row.conditioned_legal_failure_probability_upper_bound < 2**-400
    assert row.largest_component_fraction_upper_bound_on_good_event == pytest.approx(
        2.0 ** -513
    )
    assert row.exponentially_fragmented


def test_report_kills_only_the_implemented_local_walk() -> None:
    theorem = linear_depth_fiber_walk_no_go_theorem()
    assert theorem.current_local_fiber_walk_eliminated
    assert theorem.polynomial_log_block_dictionary_eliminated
    assert not theorem.target_dependent_global_moves_eliminated
    assert not theorem.implicit_collision_oracle_eliminated

    report = run_linear_depth_fiber_walk_no_go(n_values=(256, 512))
    assert report.headline_metrics["exact_control_failure_count"] == 0
    assert report.headline_metrics[
        "proved_current_fiber_graph_linear_depth_failure_count"
    ] == 1
    assert not report.claim_gate[
        "implemented_local_fiber_walk_linear_depth_route_alive"
    ]
    assert report.claim_gate["target_dependent_global_transport_route_alive"]
    assert report.claim_gate["implicit_nonlocal_collision_walk_route_alive"]
    assert not report.claim_gate["speedup_claim_allowed"]
