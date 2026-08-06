from self_dual_wreath_orientation_filter_physical_access import (
    dual_access_scaling_record,
    finite_dual_access_control,
    run_orientation_filter_physical_access,
)


def test_finite_physical_gram_factorization_and_success_bound() -> None:
    control = finite_dual_access_control(3, 1, ((2, 1), (2, 1)))
    assert control.exact_physical_dual_access_bound_verified
    assert control.synthesis_frame_identity_residual < 1e-12
    assert control.gram_spectrum_identity_residual < 1e-12
    assert control.contraction_bound_violation == 0
    assert (
        control.contracted_dual_filter_average_success
        <= control.maximum_allowed_dual_contraction_success + 1e-12
    )


def test_direct_dual_access_is_factorial_at_natural_copy_count() -> None:
    record = dual_access_scaling_record(512)
    assert record.direct_dual_access_success_log2_upper_bound < -3800
    assert record.generic_amplitude_amplification_lower_bound_log2 > 1900
    assert not record.direct_dual_access_inverse_polynomial


def test_report_falsifies_direct_access_not_structured_transfer() -> None:
    report = run_orientation_filter_physical_access()
    assert report.claim_gate["factorial_direct_access_obstruction_proved"]
    assert not report.claim_gate[
        "direct_physical_to_dual_filter_polynomially_conclusive"
    ]
    assert not report.claim_gate["structured_polar_transfer_ruled_out"]
    assert not report.claim_gate["direct_physical_filter_ruled_out"]
    assert report.claim_gate[
        "direct_physical_orientation_filter_constructed"
    ]
    assert not report.claim_gate["speedup_claim_allowed"]
