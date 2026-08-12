import numpy as np
import pytest

from self_dual_wreath_component_dependency_ridge_physical_spectrum import (
    _random_synthesis_with_common_subspace,
    audit_dependency_physical_spectrum,
    dependency_physical_frames,
    dependency_ridge_physical_spectrum_theorem,
    physical_tail_transfer_scaling_record,
    run_component_dependency_ridge_physical_spectrum,
    support_ridge_tail,
    support_ridge_tail_trace_formula,
)


def test_nonzero_full_and_excluded_spectra_transfer_to_physical_frames() -> None:
    synthesis, common = _random_synthesis_with_common_subspace(
        12,
        16,
        12,
        5,
        seed=31,
    )
    row = audit_dependency_physical_spectrum(
        "FULL",
        synthesis,
        common,
        1e-2,
    )
    assert row.exact_physical_spectral_reduction_verified
    assert row.maximum_full_nonzero_spectrum_residual < 1e-9
    assert row.maximum_excluded_nonzero_spectrum_residual < 1e-9
    assert row.rank_difference_residual == 0
    assert row.child_synthesis_rank - row.excluded_synthesis_rank == 5


def test_rank_deficient_synthesis_preserves_tail_and_rank_identity() -> None:
    synthesis, common = _random_synthesis_with_common_subspace(
        14,
        18,
        10,
        4,
        seed=37,
    )
    row = audit_dependency_physical_spectrum(
        "DEFICIENT",
        synthesis,
        common,
        3e-3,
    )
    assert row.exact_physical_spectral_reduction_verified
    assert row.child_synthesis_rank == 10
    assert row.excluded_synthesis_rank == 6
    assert row.coefficient_spectral_tail_upper_bound == pytest.approx(
        row.physical_spectral_tail_upper_bound
    )
    assert row.exact_dependency_ridge_error_squared <= (
        row.physical_spectral_tail_upper_bound + 1e-10
    )


def test_tail_equals_rank_resolvent_trace_formula() -> None:
    matrix = np.diag([0.0, 0.2, 0.7, 1.5]).astype(complex)
    direct = support_ridge_tail(matrix, 0.03)
    trace = support_ridge_tail_trace_formula(matrix, 0.03)
    assert direct == pytest.approx(trace)
    with pytest.raises(ValueError, match="positive"):
        support_ridge_tail(matrix, 0.0)


def test_common_subspace_must_lie_in_child_range() -> None:
    synthesis = np.zeros((4, 3), dtype=complex)
    synthesis[0, 0] = 1
    common = np.zeros((4, 1), dtype=complex)
    common[1, 0] = 1
    with pytest.raises(ValueError, match="inside"):
        dependency_physical_frames(synthesis, common)


def test_physical_tail_scaling_requires_no_uniform_edge_or_coefficient_analysis() -> None:
    row = physical_tail_transfer_scaling_record(1e-4, 1e-12)
    assert row.transfer_can_preserve_target_signal
    assert not row.uniform_minimum_frame_eigenvalue_required
    assert not row.coefficient_space_analysis_required
    assert row.required_bounded_ridge_physical_curl > 1e-4


def test_report_preserves_natural_tail_M4_and_speedup_gates() -> None:
    report = run_component_dependency_ridge_physical_spectrum()
    assert report.headline_metrics[
        "dependency_ridge_physical_spectrum_theorem_count"
    ] == 1
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate[
        "coefficient_dependency_ridge_error_reduced_to_physical_spectra"
    ]
    assert not report.claim_gate["natural_physical_frame_resolvent_tail_small"]
    assert not report.claim_gate["natural_bounded_ridge_parity_curl_positive"]
    assert not report.claim_gate["natural_component_M4_positive"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_theorem_identifies_two_physical_frames() -> None:
    theorem = dependency_ridge_physical_spectrum_theorem()
    assert theorem.theorem_verified
    assert theorem.arbitrary_child_synthesis
    assert "RR*" in theorem.full_spectrum_transfer
    assert "F_perp" in theorem.dependency_error_bound
