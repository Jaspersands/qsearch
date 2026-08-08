import math

from self_dual_wreath_operator_steiner_bulk_reduction import (
    audit_operator_steiner_control,
    run_operator_steiner_bulk_reduction,
    uniform_operator_steiner_scaling_record,
)


def test_exact_operator_hilbert_schmidt_burden_is_holonomy_blind() -> None:
    for args in (
        ("FULL-K4-Q2-M2", 4, "all", 2, 2, 704),
        ("FULL-K5-Q4-M2", 5, "all", 4, 2, 705),
        ("FULL-K6-Q3-M1", 6, "all", 3, 1, 706),
        ("RICH-K5-Q3-M1", 5, "pattern-rich", 3, 1, 805),
        ("RICH-K6-Q4-M2", 6, "pattern-rich", 4, 2, 806),
    ):
        record = audit_operator_steiner_control(*args)
        assert math.isclose(
            record.centered_hilbert_schmidt_squared,
            record.predicted_centered_hilbert_schmidt_squared,
            rel_tol=1e-10,
            abs_tol=1e-8,
        )
        assert record.exact_operator_burden_verified
        assert record.whitened_hilbert_schmidt_squared <= (
            record.whitened_hilbert_schmidt_upper_bound + 1e-8
        )
        assert record.whitened_outlier_bound_respected


def test_uniform_matrix_fiber_trim_fraction_is_independent_of_multiplicity() -> None:
    for copy_count in (5, 8, 12, 16, 20):
        records = [
            uniform_operator_steiner_scaling_record(copy_count, multiplicity)
            for multiplicity in (1, 4, 64)
        ]
        fractions = {
            round(record.spectral_outlier_rank_fraction_bound, 14)
            for record in records
        }
        assert len(fractions) == 1
        assert all(record.multiplicity_independent_trim_fraction for record in records)


def test_uniform_operator_trim_fraction_vanishes_with_depth() -> None:
    records = [
        uniform_operator_steiner_scaling_record(copy_count, 16)
        for copy_count in (5, 8, 12, 16, 20, 24)
    ]
    assert all(
        later.spectral_outlier_rank_fraction_bound
        < earlier.spectral_outlier_rank_fraction_bound
        for earlier, later in zip(records, records[1:])
    )


def test_report_reduces_matrix_bulk_edge_to_diagonal_coverage() -> None:
    report = run_operator_steiner_bulk_reduction()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["operator_centered_burden_exact"]
    assert report.claim_gate["arbitrary_holonomy_bulk_reduction_proved"]
    assert report.claim_gate["uniform_matrix_fiber_trim_fraction_vanishes"]
    assert not report.claim_gate["natural_diagonal_coverage_edge_proved"]
    assert not report.claim_gate["natural_weighted_burden_ratio_vanishes"]
    assert not report.claim_gate["pgm_bad_state_mass_controlled"]
    assert not report.claim_gate["speedup_claim_allowed"]
