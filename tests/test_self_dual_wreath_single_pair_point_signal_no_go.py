from __future__ import annotations

import math

import pytest

from self_dual_wreath_single_pair_point_signal_no_go import (
    audit_single_pair_point_signal,
    exact_single_pair_point_signal,
    natural_single_pair_no_go_record,
    run_single_pair_point_signal_no_go,
)


def test_exact_pair_formula_matches_every_unequal_pair_through_s5() -> None:
    for n in (3, 4, 5):
        control = audit_single_pair_point_signal(n)
        assert control.maximum_formula_residual < 1e-10
        assert control.maximum_zero_criterion_residual < 1e-10
        assert control.exact_single_pair_signal_formula_verified
        assert control.exact_shared_child_zero_criterion_verified
        assert control.positive_signal_pair_count > 0
        assert control.zero_signal_pair_count > 0


def test_formula_uses_standard_kronecker_multiplicity_and_dimension_cube() -> None:
    assert exact_single_pair_point_signal((3,), (2, 1)) == pytest.approx(1 / 16)
    assert exact_single_pair_point_signal((4,), (3, 1)) == pytest.approx(1 / 54)
    assert exact_single_pair_point_signal((3, 1), (2, 2)) == pytest.approx(1 / 432)
    assert exact_single_pair_point_signal((4,), (2, 2)) == 0
    with pytest.raises(ValueError, match="unequal"):
        exact_single_pair_point_signal((3,), (3,))


def test_natural_optimal_success_bound_decays_faster_than_inverse_polynomial() -> None:
    records = [natural_single_pair_no_go_record(n) for n in (8, 12, 16, 20)]
    for record in records:
        assert record.ordered_positive_young_edge_count <= (
            record.ordered_positive_young_edge_count_upper_bound
        )
        assert record.optimal_point_success_excess_upper_bound <= (
            record.combinatorial_success_excess_upper_bound + 1e-15
        )
        assert record.one_pair_inverse_polynomial_point_advantage_ruled_out
        assert not record.information_threshold_collective_block_ruled_out
    assert all(
        left.optimal_point_success_excess_upper_bound_log2
        > right.optimal_point_success_excess_upper_bound_log2
        for left, right in zip(records, records[1:])
    )
    assert records[-1].optimal_point_success_excess_upper_bound < 1e-8


def test_report_kills_one_pair_route_but_not_collective_route() -> None:
    report = run_single_pair_point_signal_no_go()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["exact_single_pair_point_signal_proved"]
    assert report.claim_gate["single_pair_shared_child_criterion_proved"]
    assert report.claim_gate[
        "natural_single_pair_inverse_polynomial_point_advantage_ruled_out"
    ]
    assert not report.claim_gate[
        "information_threshold_collective_point_decoder_ruled_out"
    ]
    assert not report.claim_gate["carrier_retaining_point_decoder_ruled_out"]
    assert not report.claim_gate["speedup_claim_allowed"]
