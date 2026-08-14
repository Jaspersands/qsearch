import math

import numpy as np
import pytest

from self_dual_wreath_parity_rank_profile_entropy_transfer import (
    NEGATIVE_INFORMATION_BOUND_BITS,
    audit_finite_likelihood_information,
    entropy_transfer_scaling_control,
    information_likelihood_tail_upper,
    likelihood_information_parts,
    logarithmic_entropy_boundary,
    run_parity_rank_profile_entropy_transfer,
    write_parity_rank_profile_entropy_transfer_report,
)


def test_positive_negative_information_decomposition_is_exact() -> None:
    likelihood = np.asarray([2.0, 0.5, 0.0])
    reference = np.asarray([0.25, 0.5, 0.25])
    kl, positive, negative = likelihood_information_parts(likelihood, reference)

    assert math.isclose(positive, 0.5)
    assert math.isclose(negative, 0.25)
    assert math.isclose(kl, 0.25)
    assert negative <= NEGATIVE_INFORMATION_BOUND_BITS
    with pytest.raises(ValueError):
        likelihood_information_parts(likelihood, reference[:2])


def test_finite_physical_laws_obey_information_tail_bound() -> None:
    for n in (2, 3, 4, 5):
        row = audit_finite_likelihood_information(n)
        assert row.kl_decomposition_residual < 1e-12
        assert row.negative_information_bound_verified
        assert row.likelihood_tail_bound_verified
        assert row.exact_physical_mass_above_threshold <= row.information_tail_mass_upper


def test_sublogarithmic_entropy_family_gives_vanishing_transfer_bound() -> None:
    rows = [entropy_transfer_scaling_control(n) for n in (10**8, 10**16, 10**32)]

    assert all(row.sublogarithmic_entropy_hypothesis_satisfied for row in rows)
    assert [row.total_correlation_over_log2_n for row in rows] == sorted(
        (row.total_correlation_over_log2_n for row in rows), reverse=True
    )
    assert [row.expected_physical_rank_chi_square_upper for row in rows] == sorted(
        (row.expected_physical_rank_chi_square_upper for row in rows), reverse=True
    )
    assert information_likelihood_tail_upper(0.0, 2.0) > 0


def test_quadratic_rare_event_has_logarithmic_entropy_and_unit_signal() -> None:
    rows = [logarithmic_entropy_boundary(n) for n in (10, 100, 1_000)]

    assert all(row.exact_logarithmic_boundary_verified for row in rows)
    assert all(math.isclose(row.relative_entropy_over_log2_n, 2.0) for row in rows)
    assert all(math.isclose(row.physical_rare_mass, 1.0) for row in rows)
    assert all(math.isclose(row.bounded_observable_physical_mean, 1.0) for row in rows)


def test_report_keeps_physical_entropy_and_algorithm_gates_closed(tmp_path) -> None:
    report = run_parity_rank_profile_entropy_transfer()

    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["entropy_to_rank_transfer_criterion_proved"]
    assert not report.claim_gate["vanishing_kl_required_for_rank_transfer"]
    assert report.claim_gate["bounded_total_correlation_would_suffice"]
    assert not report.claim_gate["physical_total_correlation_sublogarithmic_proved"]
    assert not report.claim_gate["physical_rank_profile_mixes_proved"]
    assert not report.claim_gate["algorithm_claim_allowed"]
    assert not report.claim_gate["speedup_claim_allowed"]

    path = tmp_path / "entropy-transfer.json"
    payload = write_parity_rank_profile_entropy_transfer_report(path)
    assert path.exists()
    assert payload["headline_metrics"]["new_quantum_algorithm_count"] == 0
