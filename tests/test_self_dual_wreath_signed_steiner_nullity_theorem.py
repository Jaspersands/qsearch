import math

from self_dual_wreath_signed_steiner_nullity_theorem import (
    audit_all_fano_signings,
    audit_random_signing_nullity,
    run_signed_steiner_nullity_theorem,
    signed_steiner_nullity_scaling_record,
)


def test_all_fano_signings_have_nullity_at_most_two() -> None:
    record = audit_all_fano_signings()
    assert record.signing_count == 4**7
    assert record.nullity_histogram == {
        "0": 5632,
        "1": 8960,
        "2": 1792,
    }
    assert record.maximum_nullity == 2
    assert record.sharp_two_dimensional_example_count == 1792
    assert math.isclose(
        record.minimum_third_eigenvalue,
        3 - math.sqrt(5),
        abs_tol=1e-9,
    )
    assert record.maximum_nullity_bound_verified


def test_quotient_signing_attains_the_all_depth_nullity_bound() -> None:
    for copy_count in range(3, 9):
        record = signed_steiner_nullity_scaling_record(copy_count)
        assert record.proved_maximum_nullity == 2
        assert record.quotient_witness_rank == 2
        assert record.quotient_signing_nullity == 2
        assert record.upper_bound_attained
        assert math.isclose(
            record.proved_maximum_exact_null_rank_fraction,
            2 / ((1 << copy_count) - 1),
        )


def test_seeded_signings_respect_the_analytic_nullity_bound() -> None:
    for copy_count, seed in ((4, 304), (5, 305), (6, 306), (7, 307)):
        record = audit_random_signing_nullity(copy_count, seed)
        assert record.observed_nullity <= 2
        assert record.theorem_bound_respected


def test_report_limits_claim_to_exact_scalar_null_rank() -> None:
    report = run_signed_steiner_nullity_theorem()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["scalar_full_line_nullity_at_most_two"]
    assert report.claim_gate["scalar_nullity_bound_sharp"]
    assert report.claim_gate["exact_scalar_null_rank_fraction_vanishes"]
    assert not report.claim_gate["near_null_scalar_mass_controlled"]
    assert not report.claim_gate["natural_weighted_channel_sum_controlled"]
    assert not report.claim_gate["matrix_valued_flat_sections_controlled"]
    assert not report.claim_gate["speedup_claim_allowed"]
