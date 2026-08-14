import math

import pytest

from self_dual_wreath_character_triangle_barrier import (
    character_triangle_barrier_record,
    partition_number,
    run_character_triangle_barrier,
)


def test_continuous_canonical_threshold_leaves_sixth_power_normalizer():
    for n in (10, 20, 50, 100):
        row = character_triangle_barrier_record(n)
        expected = 6.0 * math.log2(
            row.partition_count * row.group_order_log2
        )
        assert row.continuous_threshold_partition_function_bound_log2 == pytest.approx(
            expected,
            abs=1e-12,
        )
        assert expected > 0


def test_pentagonal_partition_numbers_match_known_values():
    assert [partition_number(n) for n in range(11)] == [
        1,
        1,
        2,
        3,
        5,
        7,
        11,
        15,
        22,
        30,
        42,
    ]
    assert partition_number(100) == 190569292


def test_seven_sector_energy_bound_is_square_of_partition_bound():
    for n in (10, 30, 100):
        row = character_triangle_barrier_record(n)
        assert row.continuous_threshold_energy_bound_log2 == pytest.approx(
            math.log2(7.0)
            + 2.0 * row.continuous_threshold_partition_function_bound_log2,
            abs=1e-12,
        )


def test_flooring_the_threshold_only_weakens_the_idealized_bound():
    for n in (10, 12, 16, 20, 30, 50, 100):
        row = character_triangle_barrier_record(n)
        assert row.idealized_partition_function_bound_log2 >= (
            row.continuous_threshold_partition_function_bound_log2 - 1e-9
        )
        assert not row.idealized_bound_is_below_one
        assert not row.pointwise_triangle_method_certifies_decay


def test_report_eliminates_only_the_proof_strategy():
    report = run_character_triangle_barrier()
    assert report.headline_metrics["pointwise_triangle_strategy_no_go_theorem_count"] == 1
    assert report.claim_gate["pointwise_triangle_route_eliminated_proved"]
    assert not report.claim_gate["known_character_bounds_close_adaptive_energy"]
    assert not report.claim_gate["canonical_adaptive_energy_vanishes_proved"]
    assert not report.claim_gate["canonical_adaptive_energy_survives_proved"]
    assert not report.claim_gate["algorithm_claim_allowed"]
    assert not report.claim_gate["speedup_claim_allowed"]
