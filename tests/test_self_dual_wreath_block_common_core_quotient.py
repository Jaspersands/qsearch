from self_dual_wreath_block_common_core_quotient import (
    block_quotient_scaling_record,
    run_block_common_core_quotient,
    validate_block_common_core_quotient,
)


def test_exact_quotient_annihilates_explicit_common_range() -> None:
    record = validate_block_common_core_quotient()
    assert record.compressed_carrier_dimension == 400
    assert record.common_range_dimension > 0
    assert record.common_range_annihilation_residual < 1e-8
    assert record.quotient_projector_idempotence_residual < 1e-8
    assert record.maximum_replicated_orientation_action_commutator_norm < 1e-8
    assert record.maximum_mixed_orientation_action_commutator_norm > 0.9
    assert not record.naive_branchwise_physical_lift_covariant
    assert record.exact_block_common_core_quotient_validation


def test_plancherel_quotient_dimension_loss_is_negligible() -> None:
    record = block_quotient_scaling_record(128)
    assert record.complete_block_count > 80
    assert record.expected_removed_quotient_fraction_upper_bound < 1e-200
    assert record.expected_retained_quotient_fraction == 1.0
    assert record.retained_fraction_tends_to_one


def test_report_preserves_physical_lift_and_residual_norm_gates() -> None:
    report = run_block_common_core_quotient()
    assert report.headline_metrics["finite_quotient_validation_failure_count"] == 0
    assert report.claim_gate["block_one_dimensional_projectors_explicit"]
    assert report.claim_gate["replicated_bit_common_cores_annihilated"]
    assert report.claim_gate[
        "expected_quotient_dimension_retained_one_minus_o_one"
    ]
    assert not report.claim_gate["physical_carrier_quotient_circuit_proved"]
    assert not report.claim_gate["naive_branchwise_physical_lift_covariant"]
    assert not report.claim_gate["residual_polynomial_frame_norm_proved"]
    assert not report.claim_gate["all_high_frame_spikes_removed"]
    assert not report.claim_gate["speedup_claim_allowed"]
