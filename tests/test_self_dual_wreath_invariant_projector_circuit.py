from self_dual_wreath_invariant_projector_circuit import (
    audit_symmetric_qft_intertwining,
    invariant_projector_circuit_scaling_record,
    run_invariant_projector_circuit,
)


def test_qft_intertwines_left_regular_and_irrep_row_action() -> None:
    for n in (3, 4):
        control = audit_symmetric_qft_intertwining(n)
        assert control.exact_finite_intertwining_verified
        assert control.maximum_fourier_unitarity_residual < 1e-12
        assert control.maximum_left_regular_intertwining_residual < 1e-12


def test_natural_copy_count_circuit_schema_is_polynomial_without_amplification() -> None:
    record = invariant_projector_circuit_scaling_record(512)
    assert record.information_threshold_copy_count > 3800
    assert record.qft_calls_per_projector_block_encoding < 8000
    assert record.polynomial_circuit_schema
    assert record.inverse_polynomial_error_suffices
    assert not record.factorial_amplitude_amplification_required


def test_projected_group_average_matches_physical_orientation_projectors() -> None:
    report = run_invariant_projector_circuit()
    assert report.headline_metrics["projected_block_finite_control_count"] == 20
    assert report.headline_metrics["projected_block_validation_failure_count"] == 0
    assert report.claim_gate[
        "polynomial_controlled_invariant_projector_schema_proved"
    ]


def test_report_leaves_postfilter_information_and_decoder_open() -> None:
    report = run_invariant_projector_circuit()
    assert not report.claim_gate["all_n_constant_postfilter_information_proved"]
    assert not report.claim_gate["complete_covariant_measurement_proved"]
    assert not report.claim_gate["polynomial_hidden_permutation_decoder_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
