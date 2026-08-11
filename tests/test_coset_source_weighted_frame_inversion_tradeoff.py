import math

import numpy as np
import pytest

from coset_source_weighted_frame_inversion_tradeoff import (
    audit_uniform_projector_ensemble,
    build_coset_source_weighted_frame_inversion_report,
    natural_source_controls,
    perfect_matching_scaling_record,
    write_coset_source_weighted_frame_inversion_report,
)


def test_uniform_projector_source_moment_and_entropy_bound_are_exact():
    states = (
        np.diag([1.0, 0.0, 0.0]),
        np.diag([0.0, 1.0, 0.0]),
        np.diag([0.0, 0.0, 1.0]),
    )
    row = audit_uniform_projector_ensemble("orthogonal", states)
    assert row.theorem_control_passed
    assert row.average_frame_support_rank == 3
    assert row.individual_projector_rank == 1
    assert row.conditional_holevo_bits == pytest.approx(math.log2(3))
    assert row.source_weighted_inverse_root_second_moment == pytest.approx(3.0)
    assert row.entropy_forced_second_moment_lower_bound == pytest.approx(3.0)
    assert row.source_moment_identity_residual < 1e-12


def test_nonorthogonal_projectors_have_slack_but_obey_both_rank_bounds():
    plus = np.asarray([1.0, 1.0]) / math.sqrt(2)
    states = (
        np.diag([1.0, 0.0]),
        np.outer(plus, plus),
    )
    row = audit_uniform_projector_ensemble("overlap", states)
    assert row.theorem_control_passed
    assert row.source_weighted_inverse_root_second_moment == pytest.approx(2.0)
    assert row.entropy_forced_second_moment_lower_bound < 2.0
    assert row.source_weighted_inverse_root_second_moment <= len(states)


def test_natural_source_controls_verify_jensen_tradeoff_and_copy_growth():
    _, one = natural_source_controls(5, 2, 1)
    _, three = natural_source_controls(5, 2, 3)
    assert one.all_finite_controls_passed
    assert three.all_finite_controls_passed
    assert one.jensen_bound_residual < 1e-10
    assert three.jensen_bound_residual < 1e-10
    assert three.average_conditional_holevo_bits > one.average_conditional_holevo_bits
    assert (
        three.global_source_weighted_inverse_root_rms_factor
        > one.global_source_weighted_inverse_root_rms_factor
    )


def test_perfect_matching_fano_obstruction_is_superpolynomial():
    row = perfect_matching_scaling_record(64, bounded_error=1 / 3)
    assert row.elementary_log2_hypothesis_lower_bound <= (
        row.log2_hidden_hypothesis_count
    )
    assert row.fano_forced_log2_direct_inverse_rms > 40
    assert row.elementary_log2_direct_inverse_rms_lower_bound > 20
    assert row.direct_inverse_rms_lower_bound_is_superpolynomial


def test_scaling_record_rejects_noncertificate_sizes():
    with pytest.raises(ValueError, match="multiple of four"):
        perfect_matching_scaling_record(10)


def test_report_closes_only_standalone_direct_inverse(tmp_path):
    report = build_coset_source_weighted_frame_inversion_report()
    assert report.theorem.theorem_verified
    assert report.theorem.exact_source_moment_identity_proved
    assert report.theorem.entropy_rank_tradeoff_proved
    assert report.theorem.bounded_error_direct_inverse_obstruction_proved
    assert not report.theorem.fused_polar_isometry_ruled_out
    assert not report.theorem.arbitrary_collective_measurement_ruled_out
    assert not report.theorem.general_quantum_circuit_lower_bound_proved
    assert not report.claim_gate[
        "bounded_error_direct_projected_lcu_inverse_rescued"
    ]
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_coset_source_weighted_frame_inversion_report(
        tmp_path / "report.json"
    )
    assert payload["status"] == (
        "coset-source-weighted-direct-inverse-closed-fused-polar-open"
    )
