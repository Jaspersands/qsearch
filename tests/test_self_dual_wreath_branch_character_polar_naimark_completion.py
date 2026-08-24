from __future__ import annotations

import json

import numpy as np

from self_dual_wreath_branch_character_polar_naimark_completion import (
    REPORT_PATH,
    audit_candidate_relative_convolution,
    audit_local_polar_naimark,
    audit_tensor_polar_naimark,
    candidate_relative_convolution,
    convolution_autocorrelation_gram,
    local_polar_naimark_data,
    run_branch_character_polar_naimark_completion,
    tensor_polar_naimark_isometry,
    write_branch_character_polar_naimark_completion_report,
)


THRESHOLD_LABELS = (
    ((3,), (2, 1)),
    ((3,), (1, 1, 1)),
    ((2, 1), (1, 1, 1)),
)
THREE_CYCLE = (1, 2, 0)


def test_local_support_frame_has_only_one_and_two_eigenvalues() -> None:
    _plus, _minus, frame, _whitener, isometry = local_polar_naimark_data(
        (3,),
        (2, 1),
        THREE_CYCLE,
    )
    values = np.linalg.eigvalsh(frame)
    assert all(min(abs(value - 1), abs(value - 2)) < 1e-9 for value in values)
    assert np.linalg.norm(isometry.conj().T @ isometry - np.eye(2)) < 1e-9


def test_local_control_certifies_condition_at_most_two() -> None:
    control = audit_local_polar_naimark(
        "S3-LOCAL",
        (3,),
        (2, 1),
        THREE_CYCLE,
    )
    assert control.exact_local_polar_naimark_completion_verified
    assert control.support_frame_condition_number <= 2.0 + 1e-9
    assert control.naimark_isometry_residual < 1e-9


def test_mixed_phase_control_attains_condition_two_boundary() -> None:
    control = audit_local_polar_naimark(
        "S4-MIXED",
        (3, 1),
        (4,),
        (0, 2, 3, 1),
    )
    assert control.exact_local_polar_naimark_completion_verified
    assert abs(control.support_frame_minimum_eigenvalue - 1.0) < 1e-9
    assert abs(control.support_frame_maximum_eigenvalue - 2.0) < 1e-9
    assert abs(control.support_frame_condition_number - 2.0) < 1e-9


def test_tensor_completion_is_full_character_isometry() -> None:
    isometry = tensor_polar_naimark_isometry(THRESHOLD_LABELS, THREE_CYCLE)
    control = audit_tensor_polar_naimark(
        "S3-THRESHOLD",
        THRESHOLD_LABELS,
        THREE_CYCLE,
    )
    assert isometry.shape == (32, 4)
    assert np.linalg.norm(isometry.conj().T @ isometry - np.eye(4)) < 1e-9
    assert control.character_output_count == 8
    assert control.exact_tensor_polar_naimark_completion_verified


def test_candidate_convolution_gram_equals_operator_autocorrelation() -> None:
    convolution, group, fields = candidate_relative_convolution(THRESHOLD_LABELS)
    predicted = convolution_autocorrelation_gram(group, fields)
    assert np.linalg.norm(convolution.conj().T @ convolution - predicted) < 1e-9


def test_pointwise_completion_does_not_fake_global_isometry() -> None:
    control = audit_candidate_relative_convolution(
        "S3-THRESHOLD",
        THRESHOLD_LABELS,
    )
    assert control.pointwise_isometries_do_not_imply_global_isometry
    assert control.convolution_isometry_residual > 0.1
    assert control.finite_constant_condition_observed
    assert 1.0 < control.condition_number < 2.0
    assert control.maximum_nonidentity_autocorrelation_norm > 0.25


def test_report_keeps_global_decoder_gates_false() -> None:
    report = run_branch_character_polar_naimark_completion()
    assert report.theorem.theorem_verified
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate[
        "known_relative_tensor_polar_naimark_isometry_compiled"
    ]
    assert not report.claim_gate["all_n_natural_autocorrelation_gap_proved"]
    assert not report.claim_gate[
        "normalization_one_candidate_convolution_compiled"
    ]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_writer_generates_live_artifact(tmp_path) -> None:
    path = tmp_path / REPORT_PATH.name
    payload = write_branch_character_polar_naimark_completion_report(path)
    loaded = json.loads(path.read_text())
    assert loaded["status"] == payload["status"]
    assert loaded["headline_metrics"]["finite_control_failure_count"] == 0
    assert not loaded["claim_gate"]["speedup_claim_allowed"]
