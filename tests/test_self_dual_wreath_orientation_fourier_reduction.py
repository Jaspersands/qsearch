import numpy as np

from self_dual_wreath_orientation_fourier_reduction import (
    audit_orientation_fourier_tuple,
    compressed_fourier_block,
    orientation_invariant_projector,
    orientation_support_scaling_record,
    run_orientation_fourier_reduction,
)


W4_LABELS = (
    ((4,), (3, 1)),
    ((2, 2), (2, 1, 1)),
)


def test_orientation_projectors_are_exact_and_average_to_fourier_block() -> None:
    target = (3, 1)
    projectors = [
        orientation_invariant_projector(target, W4_LABELS, mask)
        for mask in range(4)
    ]
    for projector in projectors:
        assert np.linalg.norm(projector @ projector - projector) < 1e-10
        assert np.linalg.norm(projector - projector.T) < 1e-10
    expected = sum(projectors) / 4
    block = compressed_fourier_block(target, W4_LABELS)
    assert np.linalg.norm(block - expected) < 1e-10


def test_orbit_gram_fourier_spectrum_matches_physical_frame() -> None:
    record = audit_orientation_fourier_tuple(4, W4_LABELS)
    assert record.exact_finite_orientation_fourier_validation
    assert record.maximum_single_label_overlap_formula_residual < 1e-10
    assert record.maximum_fourier_orientation_decomposition_residual < 1e-10
    assert record.orbit_gram_spectral_residual < 1e-10
    assert record.maximum_active_orientation_count > 1


def test_threshold_support_sparsity_shortcut_is_falsified() -> None:
    record = orientation_support_scaling_record(11)
    assert record.reaches_information_threshold
    assert record.total_orientation_count == 1 << record.copy_count
    assert record.every_target_supports_every_orientation
    assert record.minimum_active_orientation_fraction == 1.0
    assert record.first_full_support_saturation_step == 3
    assert record.support_count_exceeds_quartic_benchmark
    assert not record.polynomial_orientation_support_proved


def test_support_dynamic_merges_exponential_orientations_exactly() -> None:
    record = orientation_support_scaling_record(8)
    assert record.copy_count == 11
    assert record.total_orientation_count == 2048
    assert record.final_merged_support_state_count == 1
    assert record.maximum_active_orientation_count == 2048
    assert record.step_records[-1].full_support_orientation_count == 2048


def test_report_proves_reduction_and_records_support_no_go() -> None:
    report = run_orientation_fourier_reduction()
    metrics = report.headline_metrics
    assert metrics["complete_w4_orientation_fourier_validation_count"] == 15
    assert metrics["finite_orientation_fourier_validation_failure_count"] == 0
    assert metrics["full_orientation_support_saturation_record_count"] == 7
    assert metrics["tail_log2_maximum_active_orientation_count"] == 29.0
    assert report.claim_gate[
        "operator_valued_orbit_gram_fourier_reduction_proved"
    ]
    assert report.claim_gate["orientation_projector_decomposition_proved"]
    assert report.claim_gate["tail_orientation_support_saturated"]
    assert not report.claim_gate["uniform_projector_sum_norm_bound_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
