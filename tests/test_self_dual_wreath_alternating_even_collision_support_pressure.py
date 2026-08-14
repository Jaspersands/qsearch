import itertools

import pytest

from self_dual_wreath_alternating_even_collision_support_pressure import (
    exhaustive_even_support_pressure,
    permutation_parity,
    run_alternating_even_collision_support_pressure,
    slow_support_scaling_control,
    support_pressure_gap,
    write_alternating_even_collision_support_pressure_report,
)


def test_even_parity_detector_matches_small_alternating_group_orders() -> None:
    for n, expected in ((3, 3), (4, 12), (5, 60)):
        group = [
            permutation
            for permutation in itertools.permutations(range(n))
            if permutation_parity(permutation) == 0
        ]
        assert len(group) == expected


def test_exhaustive_even_full_core_obeys_six_power_gap() -> None:
    rows = [exhaustive_even_support_pressure(n) for n in (3, 4, 5)]

    assert all(row.theorem_bound_verified_exhaustively for row in rows)
    assert rows[0].fully_nonidentity_even_triple_count == 0
    assert rows[1].minimum_observed_support_pressure_gap >= 6
    assert rows[2].minimum_observed_support_pressure_gap >= 6
    assert rows[2].minimum_gap_witness_union_support is not None


def test_embedded_even_three_cycles_have_positive_support_pressure() -> None:
    g = (1, 2, 0, 3, 4)
    h = (2, 0, 1, 3, 4)
    k = (2, 1, 4, 3, 0)
    gap, word_supports, union_support = support_pressure_gap(g, h, k)

    assert all(size >= 3 for size in word_supports)
    assert union_support >= 3
    assert gap >= 6


def test_slow_support_family_has_subpolynomial_overhead() -> None:
    rows = [slow_support_scaling_control(value) for value in (10**3, 10**5, 10**7)]

    assert all(row.overhead_is_subpolynomial_on_declared_family for row in rows)
    assert [row.support_over_log_n_loglog_n_scale for row in rows] == sorted(
        (row.support_over_log_n_loglog_n_scale for row in rows), reverse=True
    )
    with pytest.raises(ValueError):
        slow_support_scaling_control(1.0)


def test_report_forces_obstruction_to_growing_support_without_closing_core(tmp_path) -> None:
    report = run_alternating_even_collision_support_pressure()

    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["even_six_word_support_pressure_gap_proved"]
    assert report.claim_gate["bounded_and_slow_support_core_vanishes_proved"]
    assert report.claim_gate["local_cycle_obstruction_eliminated"]
    assert not report.claim_gate[
        "growing_support_even_core_subpolynomial_proved"
    ]
    assert not report.claim_gate[
        "fully_nonidentity_even_core_subpolynomial_proved"
    ]
    assert not report.claim_gate["physical_rank_profile_mixes_proved"]
    assert not report.claim_gate["algorithm_claim_allowed"]
    assert not report.claim_gate["speedup_claim_allowed"]

    path = tmp_path / "support-pressure.json"
    payload = write_alternating_even_collision_support_pressure_report(path)
    assert path.exists()
    assert payload["headline_metrics"]["new_quantum_algorithm_count"] == 0
