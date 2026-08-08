import math

from self_dual_wreath_signed_steiner_bulk_edge import (
    audit_signed_steiner_bulk,
    full_steiner_outlier_count_bound,
    rich_steiner_frobenius_bound,
    run_signed_steiner_bulk_edge,
    signed_steiner_bulk_scaling_record,
)


def test_full_signed_frame_has_exact_sign_independent_centered_moment() -> None:
    for kind in ("unsigned", "quotient-kernel", "random-balanced"):
        for copy_count in (4, 6, 8):
            record = audit_signed_steiner_bulk(
                f"full-{kind}-K{copy_count}",
                copy_count,
                "all",
                kind,
                seed=500 + copy_count,
            )
            point_count = (1 << copy_count) - 1
            assert math.isclose(
                record.centered_frobenius_squared,
                point_count * (point_count - 1),
                rel_tol=1e-12,
                abs_tol=1e-8,
            )
            assert record.exact_or_bounded_moment_verified
            assert record.outlier_bound_respected


def test_full_outlier_rank_fraction_vanishes_for_every_signing() -> None:
    previous = 1.0
    for copy_count in range(5, 18):
        record = signed_steiner_bulk_scaling_record(copy_count, "all")
        assert math.isclose(
            record.spectral_outlier_count_bound,
            full_steiner_outlier_count_bound(copy_count, 0.5),
        )
        assert record.spectral_outlier_rank_fraction_bound < previous
        previous = record.spectral_outlier_rank_fraction_bound


def test_rich_degree_normalized_frame_has_constant_frobenius_burden() -> None:
    for kind in ("unsigned", "quotient-kernel", "random-balanced"):
        for copy_count in (5, 7, 8):
            record = audit_signed_steiner_bulk(
                f"rich-{kind}-K{copy_count}",
                copy_count,
                "pattern-rich",
                kind,
                seed=600 + copy_count,
            )
            assert record.centered_frobenius_squared <= (
                rich_steiner_frobenius_bound(copy_count) + 1e-9
            )
            assert record.exact_or_bounded_moment_verified
            assert record.outlier_bound_respected


def test_rich_trim_fraction_vanishes_despite_constant_outlier_bound() -> None:
    records = [
        signed_steiner_bulk_scaling_record(copy_count, "pattern-rich")
        for copy_count in (8, 12, 16, 20, 24)
    ]
    assert all(
        later.spectral_outlier_rank_fraction_bound
        < earlier.spectral_outlier_rank_fraction_bound
        for earlier, later in zip(records, records[1:])
    )
    assert records[-1].centered_frobenius_bound < 16.01


def test_report_moves_boundary_to_matrix_weighted_channel_aggregation() -> None:
    report = run_signed_steiner_bulk_edge()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["full_scalar_near_null_rank_fraction_vanishes"]
    assert report.claim_gate["rich_scalar_near_null_rank_fraction_vanishes"]
    assert not report.claim_gate["scalar_bulk_edge_requires_gauge_randomness"]
    assert not report.claim_gate["natural_carrier_sector_trim_aggregated"]
    assert not report.claim_gate[
        "operator_valued_frobenius_burden_controlled"
    ]
    assert not report.claim_gate["pgm_bad_state_mass_controlled"]
    assert not report.claim_gate["speedup_claim_allowed"]
