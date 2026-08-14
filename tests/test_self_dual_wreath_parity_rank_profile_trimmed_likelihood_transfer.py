import pytest

from self_dual_wreath_parity_rank_profile_trimmed_likelihood_transfer import (
    optimized_weak_l1_epsilon,
    quadratic_rare_event_boundary,
    run_parity_rank_profile_trimmed_likelihood_transfer,
    trimmed_weak_l1_transfer_bound,
    weak_l1_scaling_control,
    write_parity_rank_profile_trimmed_likelihood_transfer_report,
)


def test_weak_l1_transfer_bound_decreases_on_valid_asymptotic_family() -> None:
    rows = [weak_l1_scaling_control(n) for n in (10**8, 10**12, 10**16)]

    assert all(row.asymptotic_hypotheses_satisfied for row in rows)
    assert [row.cap_times_reference_variance for row in rows] == sorted(
        (row.cap_times_reference_variance for row in rows), reverse=True
    )
    assert [row.expected_physical_rank_chi_square_upper for row in rows] == sorted(
        (row.expected_physical_rank_chi_square_upper for row in rows), reverse=True
    )
    assert rows[-1].expected_physical_rank_chi_square_upper < 0.01


def test_bound_charges_removed_mass_cap_and_physical_tail_separately() -> None:
    epsilon = optimized_weak_l1_epsilon(100.0, 1e-8)
    good, bad, expected = trimmed_weak_l1_transfer_bound(
        removed_physical_mass=0.01,
        retained_high_likelihood_physical_mass=0.02,
        likelihood_cap=100.0,
        union_variance=1e-8,
        epsilon=epsilon,
    )

    assert good > 0
    assert bad >= 0.02
    assert expected >= 7 * 0.01 + 7 * 0.02
    with pytest.raises(ValueError):
        trimmed_weak_l1_transfer_bound(
            removed_physical_mass=-0.1,
            retained_high_likelihood_physical_mass=0,
            likelihood_cap=1,
            union_variance=1,
            epsilon=0.1,
        )


def test_quadratic_rare_event_is_exact_boundary_counterexample() -> None:
    rows = [quadratic_rare_event_boundary(n) for n in (10, 100, 1_000)]

    assert all(row.exact_quadratic_boundary_verified for row in rows)
    assert all(row.physical_rare_event_mass == "1" for row in rows)
    assert all(row.bounded_observable_physical_mean == "1" for row in rows)
    assert all(row.physical_mass_above_test_cap == "1" for row in rows)


def test_report_keeps_retained_tail_and_physical_claims_open(tmp_path) -> None:
    report = run_parity_rank_profile_trimmed_likelihood_transfer()

    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["trimmed_weak_l1_transfer_criterion_proved"]
    assert not report.claim_gate["full_second_moment_required_for_rank_transfer"]
    assert report.claim_gate["canonical_low_dimension_tail_removed"]
    assert not report.claim_gate[
        "retained_subquadratic_likelihood_tail_vanishes_proved"
    ]
    assert not report.claim_gate["physical_rank_profile_mixes_proved"]
    assert not report.claim_gate["algorithm_claim_allowed"]
    assert not report.claim_gate["speedup_claim_allowed"]

    path = tmp_path / "weak-l1.json"
    payload = write_parity_rank_profile_trimmed_likelihood_transfer_report(path)
    assert path.exists()
    assert payload["headline_metrics"]["new_quantum_algorithm_count"] == 0
