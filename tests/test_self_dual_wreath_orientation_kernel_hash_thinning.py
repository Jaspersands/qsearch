from __future__ import annotations

import numpy as np
import pytest

from self_dual_wreath_joint_character_multiplicity_gram import (
    orientation_overlap_kernel,
    predicted_joint_multiplicity_operator,
)
from self_dual_wreath_orientation_kernel_hash_thinning import (
    affine_hash_mask,
    audit_orientation_kernel_hash,
    audit_spectral_trim,
    enumerate_affine_hash_masks,
    kernel_parameters,
    orientation_kernel_hash_scaling_record,
    run_orientation_kernel_hash_thinning,
)


THRESHOLD_LABELS = (
    ((3,), (2, 1)),
    ((3,), (1, 1, 1)),
    ((2, 1), (1, 1, 1)),
)


def test_affine_hash_family_is_exactly_pairwise_independent() -> None:
    masks = enumerate_affine_hash_masks(4, 2)
    probabilities = np.mean(np.stack(masks), axis=0)
    assert np.allclose(probabilities, 0.25)
    for left in range(16):
        for right in range(left + 1, 16):
            joint = np.mean([mask[left] and mask[right] for mask in masks])
            assert joint == pytest.approx(1 / 16)


def test_hash_mask_rejects_invalid_parameters() -> None:
    with pytest.raises(ValueError, match="output width"):
        affine_hash_mask(3, (), 0)
    with pytest.raises(ValueError, match="row out of range"):
        affine_hash_mask(3, (8,), 0)
    with pytest.raises(ValueError, match="offset out of range"):
        affine_hash_mask(3, (1,), 2)


def test_exact_hash_error_formula_on_physical_orientation_kernel() -> None:
    control = audit_orientation_kernel_hash(
        3,
        (2, 1),
        THRESHOLD_LABELS,
        hash_output_bits=1,
        control_id="threshold",
    )
    assert control.exact_hash_thinning_theorem_verified
    assert control.enumerated_hash_count == 16
    assert control.expectation_formula_residual < 1e-10
    assert control.deterministic_bound_violation == 0
    assert control.retention_density == pytest.approx(0.5)


def test_offdiagonal_energy_bound_survives_all_active_w3_sectors() -> None:
    for target in ((3,), (2, 1), (1, 1, 1)):
        _, _, projectors = predicted_joint_multiplicity_operator(
            target,
            THRESHOLD_LABELS,
        )
        kernel = orientation_overlap_kernel(
            projectors,
            1 if target != (2, 1) else 2,
        )
        _, _, _, offdiagonal_squared, upper = kernel_parameters(kernel)
        assert offdiagonal_squared <= upper + 1e-10


def test_frobenius_error_controls_bad_rank_and_native_trace_mass() -> None:
    matrix = np.diag([0.8, 0.95, 1.0, 1.05, 1.2])
    control = audit_spectral_trim(
        matrix,
        1.0,
        0.1,
        control_id="diagonal",
    )
    assert control.spectral_trim_bounds_verified
    assert control.observed_bad_eigenvalue_count == 2
    assert control.observed_bad_trace_mass <= control.bad_trace_mass_upper_bound
    assert control.retained_condition_number_upper_bound == pytest.approx(1.1 / 0.9)


def test_polynomial_hash_scaling_does_not_claim_compiled_filter() -> None:
    record = orientation_kernel_hash_scaling_record(128)
    assert record.hash_projection_inverse_polynomial_acceptance
    assert record.retention_probability_lower_bound > 0
    assert record.expected_normalized_frobenius_error_upper_bound < 1e-4
    assert not record.simultaneous_all_sector_kernel_bound_proved
    assert not record.coherent_exceptional_spectrum_filter_proved
    assert not record.polynomial_joint_decoder_proved


def test_report_keeps_outlier_and_decoder_gates_closed() -> None:
    report = run_orientation_kernel_hash_thinning()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate[
        "kernel_fourth_energy_bounded_by_frame_second_moment"
    ]
    assert report.claim_gate[
        "pairwise_independent_hash_reduces_normalized_kernel_error"
    ]
    assert report.claim_gate["inverse_polynomial_physical_hash_acceptance"]
    assert not report.claim_gate[
        "simultaneous_all_sector_kernel_bound_proved"
    ]
    assert not report.claim_gate["coherent_exceptional_spectrum_filter_proved"]
    assert not report.claim_gate["polynomial_joint_decoder_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
