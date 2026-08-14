from fractions import Fraction

import pytest

from self_dual_wreath_parity_rank_profile_physical_transfer_boundary import (
    audit_physical_transfer_finite,
    good_event_rank_chi_square_bound,
    optimized_asymptotic_epsilon,
    physical_transfer_bound,
    rare_event_transfer_counterexample,
    run_parity_rank_profile_physical_transfer_boundary,
    write_parity_rank_profile_physical_transfer_boundary_report,
)


def test_good_event_bound_vanishes_quadratically_with_epsilon() -> None:
    values = [good_event_rank_chi_square_bound(epsilon) for epsilon in (0.2, 0.1, 0.05)]

    assert values == sorted(values, reverse=True)
    assert values[-1] < values[0] / 10
    assert good_event_rank_chi_square_bound(0.0) == 0.0
    with pytest.raises(ValueError):
        good_event_rank_chi_square_bound(1.0)


def test_transfer_bound_vanishes_when_moment_times_variance_vanishes() -> None:
    expected = []
    for scale in (10**6, 10**9, 10**12):
        moment = scale**0.25
        variance = 1.0 / scale
        epsilon = optimized_asymptotic_epsilon(moment, variance)
        _q_bad, _p_bad, _good, bound = physical_transfer_bound(
            moment, variance, epsilon
        )
        expected.append(bound)

    assert expected == sorted(expected, reverse=True)
    assert expected[-1] < expected[0]


def test_exact_finite_likelihood_moment_matches_signature_duality() -> None:
    for n in (3, 4, 5):
        control = audit_physical_transfer_finite(n)
        assert control.exact_tetrahedral_likelihood_second_moment == (
            control.exact_signature_second_moment
        )
        assert control.class_signature_duality_verified
        assert control.second_moment_times_union_variance > 0
        assert not control.finite_bound_numerically_nontrivial


def test_rare_event_reweighting_destroys_reference_mixing_at_threshold() -> None:
    rows = [rare_event_transfer_counterexample(scale) for scale in (10, 100, 1_000)]

    assert [Fraction(row.reference_observable_mean) for row in rows] == sorted(
        (Fraction(row.reference_observable_mean) for row in rows), reverse=True
    )
    assert all(row.likelihood_normalizes for row in rows)
    assert all(row.physical_observable_mean == "1" for row in rows)
    assert all(row.second_moment_times_reference_mean == "1" for row in rows)
    assert all(row.exact_change_of_measure_counterexample_verified for row in rows)


def test_report_records_conditional_theorem_without_promoting_physical_claim(tmp_path) -> None:
    report = run_parity_rank_profile_physical_transfer_boundary()

    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["physical_rank_transfer_threshold_proved"]
    assert not report.claim_gate["bounded_tetrahedral_second_moment_required"]
    assert not report.claim_gate["reference_mixing_alone_sufficient"]
    assert not report.claim_gate[
        "tetrahedral_collision_growth_condition_verified"
    ]
    assert not report.claim_gate["physical_rank_profile_mixes_proved"]
    assert not report.claim_gate["irreducible_racah_cmi_vanishes_proved"]
    assert not report.claim_gate["adaptive_syndrome_survives_proved"]
    assert not report.claim_gate["algorithm_claim_allowed"]
    assert not report.claim_gate["speedup_claim_allowed"]

    path = tmp_path / "transfer.json"
    payload = write_parity_rank_profile_physical_transfer_boundary_report(path)
    assert path.exists()
    assert payload["headline_metrics"]["new_quantum_algorithm_count"] == 0
