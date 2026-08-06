import numpy as np

from self_dual_wreath_orientation_fourier_reduction import (
    _w4_collision_free_labels,
)
from self_dual_wreath_physical_orientation_interference import (
    audit_physical_orientation_filter,
    orientation_subspace_transform,
    physical_filter_scaling_record,
    run_physical_orientation_interference,
)


def test_binary_subspace_transform_is_unitary_and_marks_nontrivial_characters() -> None:
    transform, accepted, basis = orientation_subspace_transform(4, (0b0011, 0b1100))
    assert np.allclose(transform @ transform.T, np.eye(16))
    assert len(basis) == 4
    assert int(np.sum(accepted)) == 12


def test_full_and_diagonal_w4_filters_obey_trace_transfer() -> None:
    labels = _w4_collision_free_labels()[0]
    full = audit_physical_orientation_filter(
        4,
        labels,
        (1, 2),
        control_id="full",
    )
    diagonal = audit_physical_orientation_filter(
        4,
        labels,
        (3,),
        control_id="diagonal",
    )
    for control in (full, diagonal):
        assert control.exact_physical_trace_transfer_verified
        assert control.maximum_sector_trace_transfer_residual < 1e-12
        assert control.covariantized_acceptance_spread < 1e-12
        assert 0 < control.retained_average_trace_fraction < 1


def test_scaling_schema_is_direct_and_avoids_factorial_amplification() -> None:
    record = physical_filter_scaling_record(512)
    assert record.direct_physical_carrier_operation
    assert not record.synthesis_adjoint_used
    assert not record.factorial_amplitude_amplification_required
    assert record.all_n_retained_information_proved


def test_complete_w4_report_keeps_asymptotic_and_decoder_gates_closed() -> None:
    report = run_physical_orientation_interference()
    assert report.headline_metrics["finite_control_count"] == 30
    assert report.headline_metrics["finite_validation_failure_count"] == 0
    assert report.claim_gate["direct_physical_orientation_filter_constructed"]
    assert report.claim_gate["direct_synthesis_access_obstruction_bypassed"]
    assert report.claim_gate["all_n_constant_retained_information_proved"]
    assert not report.claim_gate["postfilter_polynomial_frame_norm_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
