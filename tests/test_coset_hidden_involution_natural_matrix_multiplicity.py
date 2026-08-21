import pytest

from coset_hidden_involution_natural_matrix_multiplicity import (
    audit_involution_dimension_sum,
    build_natural_matrix_multiplicity_report,
    low_source_multiplicity_fraction_log2_bound,
    natural_matrix_multiplicity_scaling_record,
    symmetric_group_involution_count,
)


def test_involution_recurrence_and_irrep_dimension_sum_match() -> None:
    assert [symmetric_group_involution_count(n) for n in range(7)] == [
        1,
        1,
        2,
        4,
        10,
        26,
        76,
    ]
    for n in range(3, 9):
        row = audit_involution_dimension_sum(n)
        assert row.exact_irrep_dimension_sum == row.involution_recurrence_count
        assert row.robinson_schensted_dimension_sum_verified


def test_low_multiplicity_bound_improves_with_natural_scale() -> None:
    rows = [natural_matrix_multiplicity_scaling_record(value) for value in (4, 6, 8, 12, 16)]
    assert all(row.high_multiplicity_blocks_carry_constant_alternative_mass for row in rows)
    assert all(row.high_multiplicity_alternative_mass_lower_bound >= 0.9 for row in rows)
    assert all(
        later.low_multiplicity_source_fraction_log2_upper_bound
        < earlier.low_multiplicity_source_fraction_log2_upper_bound
        for earlier, later in zip(rows, rows[1:])
    )
    assert rows[-1].multiplicity_threshold_log2 > rows[0].multiplicity_threshold_log2


def test_bound_is_monotone_in_multiplicity_threshold() -> None:
    low = low_source_multiplicity_fraction_log2_bound(16, 27, 100.0)
    high = low_source_multiplicity_fraction_log2_bound(16, 27, 120.0)
    assert high - low == pytest.approx(20.0)


def test_report_keeps_occupied_rank_and_algorithm_gates_open() -> None:
    report = build_natural_matrix_multiplicity_report()
    assert report.headline_metrics["robinson_schensted_control_failure_count"] == 0
    assert report.headline_metrics["minimum_high_multiplicity_alternative_mass_lower_bound"] >= 0.9
    assert report.claim_gate["natural_matrix_multiplicity_mass_proved"] is True
    assert report.claim_gate["low_multiplicity_blocks_negligible_on_alternative"] is True
    assert report.claim_gate["scalar_spherical_transform_sufficient"] is False
    assert report.claim_gate["occupied_cosine_sine_rank_lower_bound_proved"] is False
    assert report.claim_gate["matrix_cosine_sine_transform_compiled"] is False
    assert report.claim_gate["binary_hidden_involution_detector_constructed"] is False
    assert report.claim_gate["speedup_claim_allowed"] is False
