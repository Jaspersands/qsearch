from __future__ import annotations

from self_dual_wreath_plancherel_recoupling_rank_pressure_no_go import (
    good_event_probability_lower_bound,
    partition_number,
    pressure_record,
    raw_squared_bound_lower_log2,
    run_plancherel_recoupling_rank_pressure_no_go,
    write_plancherel_recoupling_rank_pressure_no_go_report,
)


def test_partition_counter_matches_exact_partition_enumeration_values() -> None:
    assert partition_number(0) == 1
    assert partition_number(8) == 22
    assert partition_number(16) == 231
    assert partition_number(30) == 5604


def test_factorial_rank_pressure_crosses_one_and_grows() -> None:
    values = [raw_squared_bound_lower_log2(n) for n in (12, 16, 20, 24, 30)]

    assert values[0] < 0 < values[1]
    assert values == sorted(values)
    assert values[-1] > 40


def test_certified_good_event_is_nonvacuous_and_improves() -> None:
    values = [good_event_probability_lower_bound(n) for n in (12, 16, 20, 24, 30)]

    assert values[0] > 0
    assert values == sorted(values)
    assert values[-1] > 0.75


def test_pressure_record_keeps_finite_and_asymptotic_claims_distinct() -> None:
    row = pressure_record(30)

    assert row.raw_squared_bound_lower_exceeds_one
    assert row.simultaneous_good_event_probability_lower_bound > 0.75
    assert row.raw_squared_bound_lower_log2 > 40


def test_report_closes_only_independent_bulk(tmp_path) -> None:
    report = run_plancherel_recoupling_rank_pressure_no_go()

    assert report.claim_gate[
        "independent_plancherel_bulk_certificate_trivial_aas_proved"
    ]
    assert not report.claim_gate[
        "physical_dimension_weighted_path_certificate_trivial_proved"
    ]
    assert not report.claim_gate[
        "physical_dimension_weighted_path_contraction_proved"
    ]
    assert not report.claim_gate["generalized_3nj_contraction_proved"]
    assert not report.claim_gate["algorithm_claim_allowed"]
    assert not report.claim_gate["speedup_claim_allowed"]

    path = tmp_path / "rank-pressure.json"
    payload = write_plancherel_recoupling_rank_pressure_no_go_report(path)
    assert path.exists()
    assert payload["headline_metrics"]["new_quantum_algorithm_count"] == 0
