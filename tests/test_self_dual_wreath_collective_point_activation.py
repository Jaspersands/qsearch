from __future__ import annotations

from self_dual_wreath_collective_point_activation import (
    audit_pairwise_nonadjacent_activation,
    audit_s4_collective_activation,
    nonadjacent_family_record,
    run_collective_point_activation,
)


def test_every_s4_collision_free_two_pair_portfolio_is_activated() -> None:
    control = audit_s4_collective_activation()
    assert control.globally_distinct_portfolio_count == 15
    assert control.positive_collective_signal_count == 15
    assert control.both_isolated_signals_zero_count == 3
    assert control.zero_zero_collectively_activated_count == 3
    assert control.minimum_zero_zero_collective_signal > 0
    assert control.all_s4_collision_free_two_pair_portfolios_activated
    assert control.isolated_signal_additivity_falsified


def test_s6_collective_signal_exists_without_any_source_young_edge() -> None:
    sources = ((6,), (4, 2), (3, 1, 1, 1), (2, 2, 2))
    for index, matching in enumerate(
        (
            ((0, 1), (2, 3)),
            ((0, 2), (1, 3)),
            ((0, 3), (1, 2)),
        )
    ):
        control = audit_pairwise_nonadjacent_activation(
            6,
            tuple((sources[left], sources[right]) for left, right in matching),
            control_id=str(index),
        )
        assert control.source_young_edge_count == 0
        assert control.first_isolated_signal == 0
        assert control.second_isolated_signal == 0
        assert control.collective_centered_signal > 1e-8
        assert control.pairwise_nonadjacent_sources
        assert control.collective_activation_verified


def test_scalable_four_source_family_is_pairwise_nonadjacent() -> None:
    for n in range(8, 65):
        record = nonadjacent_family_record(n)
        assert record.source_partitions_distinct
        assert record.source_young_edge_count == 0
        assert record.every_pair_isolated_signal_zero
        assert not record.collective_signal_proved_positive


def test_report_forbids_source_local_pruning_without_claiming_scalability() -> None:
    report = run_collective_point_activation()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["isolated_point_signal_additivity_falsified"]
    assert not report.claim_gate["source_young_adjacency_pruning_valid"]
    assert report.claim_gate["pairwise_nonadjacent_collective_activation_exists"]
    assert report.claim_gate["scalable_pairwise_nonadjacent_source_family_proved"]
    assert not report.claim_gate["scalable_family_collective_activation_proved"]
    assert not report.claim_gate["all_n_collective_standard_energy_bound_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
