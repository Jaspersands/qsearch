import pytest

from coset_covariant_multiplicity_whitening_escape import (
    build_coset_covariant_multiplicity_whitening_report,
    natural_whitening_controls,
    write_coset_covariant_multiplicity_whitening_report,
)


def test_one_copy_covariance_cancels_carrier_dimension():
    controls, aggregate = natural_whitening_controls(5, 2, 1)
    assert aggregate.all_finite_controls_passed
    assert aggregate.average_direct_frame_inverse_second_moment == pytest.approx(2.0)
    assert aggregate.average_raw_multiplicity_inverse_second_moment < 0.5
    assert all(row.theorem_control_passed for row in controls)
    assert all(
        row.raw_multiplicity_inverse_second_moment
        <= row.direct_frame_inverse_second_moment + 1e-10
        for row in controls
    )


def test_three_copy_natural_controls_keep_multiplicity_target_small():
    _, aggregate = natural_whitening_controls(5, 2, 3)
    assert aggregate.all_finite_controls_passed
    assert aggregate.average_direct_frame_inverse_second_moment == pytest.approx(
        7.332518518518519
    )
    assert aggregate.average_raw_multiplicity_inverse_second_moment == pytest.approx(
        1.606962962962963
    )
    assert aggregate.average_carrier_cancellation_factor > 4.0
    assert aggregate.maximum_branch_raw_multiplicity_inverse_second_moment <= 3.0


def test_clipped_cost_obeys_rank_support_upper_bound():
    controls, _ = natural_whitening_controls(4, 2, 2)
    for row in controls:
        assert row.clipped_moment_upper_bound_residual < 1e-10
        assert row.clipped_multiplicity_inverse_second_moment <= (
            1.0 + row.raw_multiplicity_inverse_second_moment + 1e-10
        )
        assert row.rank_divisibility_failure_count == 0


def test_report_keeps_scalable_access_and_decoder_gates_false(tmp_path):
    report = build_coset_covariant_multiplicity_whitening_report()
    assert report.theorem.theorem_verified
    assert report.theorem.carrier_dimension_cancellation_proved
    assert report.theorem.raw_multiplicity_moment_identity_proved
    assert report.theorem.natural_finite_escape_controls_passed
    assert not report.theorem.all_n_polynomial_multiplicity_moment_proved
    assert not report.theorem.coherent_multiplicity_transform_constructed
    assert not report.theorem.controlled_multiplicity_whitening_circuit_constructed
    assert not report.theorem.polynomial_hidden_involution_decoder_constructed
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_coset_covariant_multiplicity_whitening_report(
        tmp_path / "report.json"
    )
    assert payload["status"] == (
        "covariant-carrier-cost-cancelled-multiplicity-whitening-open"
    )
