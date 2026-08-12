import numpy as np
import pytest

from self_dual_wreath_component_dependency_ridge_physical_curl import (
    _block_aligned_commuting_control,
    audit_dependency_ridge_physical_curl,
    dependency_ridge_physical_curl_theorem,
    physical_resolvent_kernel,
    run_component_dependency_ridge_physical_curl,
)
from self_dual_wreath_component_dependency_ridge_physical_spectrum import (
    _random_synthesis_with_common_subspace,
)


def test_physical_resolvent_difference_has_positive_rank_r_schur_factor() -> None:
    synthesis, common = _random_synthesis_with_common_subspace(
        12,
        16,
        10,
        4,
        seed=101,
    )
    _, _, kernel, schur, factorized, _ = physical_resolvent_kernel(
        synthesis,
        common,
        1e-2,
    )
    assert np.linalg.eigvalsh(kernel)[0] > -1e-9
    assert np.linalg.eigvalsh(schur)[0] > 0
    assert np.linalg.matrix_rank(kernel, tol=1e-8) == 4
    assert np.linalg.norm(kernel - factorized, ord=2) < 1e-8


def test_coefficient_ridge_words_and_curl_transfer_exactly_to_physical_space() -> None:
    synthesis, common = _random_synthesis_with_common_subspace(
        10,
        12,
        9,
        3,
        seed=103,
    )
    row = audit_dependency_ridge_physical_curl(
        "TRANSFER",
        synthesis,
        common,
        4,
        1e-3,
    )
    assert row.exact_physical_curl_reduction_verified
    assert row.kernel_rank_residual == 0
    assert row.coefficient_to_physical_ridge_residual < 1e-8
    assert row.maximum_word_trace_residual_through_degree_four < 1e-8
    assert row.maximum_pair_gap_residual < 1e-8
    assert row.normalized_ridge_curl_residual < 1e-8
    assert row.physical_ridge_curl_positive


def test_rank_deficient_child_synthesis_preserves_physical_curl_identity() -> None:
    synthesis, common = _random_synthesis_with_common_subspace(
        14,
        16,
        10,
        4,
        seed=107,
    )
    row = audit_dependency_ridge_physical_curl(
        "RANK-DEFICIENT",
        synthesis,
        common,
        8,
        3e-3,
    )
    assert row.child_synthesis_rank == 10
    assert row.exact_physical_curl_reduction_verified
    assert row.coefficient_normalized_ridge_curl == pytest.approx(
        row.physical_normalized_ridge_curl,
        abs=1e-8,
    )


def test_block_aligned_common_fiber_is_exact_zero_curl_boundary() -> None:
    synthesis, common = _block_aligned_commuting_control()
    row = audit_dependency_ridge_physical_curl(
        "COMMUTING",
        synthesis,
        common,
        4,
        1e-2,
    )
    assert row.exact_physical_curl_reduction_verified
    assert row.coefficient_normalized_ridge_curl == pytest.approx(0.0, abs=1e-12)
    assert row.physical_normalized_ridge_curl == pytest.approx(0.0, abs=1e-12)
    assert not row.physical_ridge_curl_positive


def test_invalid_leaf_partition_and_ridge_are_rejected() -> None:
    synthesis, common = _block_aligned_commuting_control()
    with pytest.raises(ValueError, match="power of two"):
        audit_dependency_ridge_physical_curl(
            "BAD-LEAVES",
            synthesis,
            common,
            3,
            1e-2,
        )
    with pytest.raises(ValueError, match="positive"):
        physical_resolvent_kernel(synthesis, common, 0.0)


def test_report_preserves_natural_curl_tail_M4_and_speedup_gates() -> None:
    report = run_component_dependency_ridge_physical_curl()
    assert report.headline_metrics[
        "exact_physical_ridge_curl_reduction_theorem_count"
    ] == 1
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.headline_metrics["zero_commuting_boundary_control_count"] == 1
    assert report.claim_gate[
        "bounded_ridge_has_exact_physical_resolvent_normal_form"
    ]
    assert report.claim_gate["all_bounded_ridge_parity_words_are_physical"]
    assert not report.claim_gate[
        "natural_signed_frame_resolvent_words_controlled"
    ]
    assert not report.claim_gate["natural_physical_ridge_curl_positive"]
    assert not report.claim_gate["natural_support_ridge_tail_small"]
    assert not report.claim_gate["natural_component_M4_positive"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_theorem_removes_coefficient_support_and_common_metric() -> None:
    theorem = dependency_ridge_physical_curl_theorem()
    assert theorem.theorem_verified
    assert theorem.arbitrary_child_synthesis
    assert theorem.coefficient_support_removed_from_ridge_curl
    assert theorem.common_metric_removed_from_ridge_curl
    assert "Schur" not in theorem.schur_factorization or "S_eta" in theorem.schur_factorization
