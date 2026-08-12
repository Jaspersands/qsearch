import numpy as np
import pytest

from self_dual_wreath_component_dependency_ridge_parity_stability import (
    _commuting_nested_grams,
    _random_nested_grams,
    audit_dependency_ridge_parity_stability,
    dependency_projection_and_ridge,
    dependency_ridge_parity_stability_theorem,
    normalized_parity_curl_stability_bound,
    physical_parity_curl_transfer_bound,
    run_component_dependency_ridge_parity_stability,
)


def test_ordered_resolvent_difference_is_positive_contraction() -> None:
    gram, excluded = _random_nested_grams(16, 6, seed=17)
    projection, ridge, order_minimum = dependency_projection_and_ridge(
        gram,
        excluded,
        1e-2,
    )
    values = np.linalg.eigvalsh(ridge)
    assert order_minimum > -1e-10
    assert values[0] > -1e-10
    assert values[-1] < 1 + 1e-10
    assert np.linalg.norm(projection @ projection - projection, ord=2) < 1e-9


def test_random_nested_grams_satisfy_parity_curl_stability() -> None:
    gram, excluded = _random_nested_grams(16, 6, seed=19)
    row = audit_dependency_ridge_parity_stability(
        "RANDOM",
        gram,
        excluded,
        4,
        1e-3,
    )
    assert row.spectral_tail_bound_verified
    assert row.parity_curl_stability_verified
    assert row.exact_and_ridge_curls_both_nonnegative
    assert row.normalized_parity_curl_difference <= (
        row.dimension_free_stability_upper_bound + 1e-10
    )


def test_commuting_nested_grams_have_zero_exact_and_ridge_curls() -> None:
    gram, excluded = _commuting_nested_grams(16, 6)
    row = audit_dependency_ridge_parity_stability(
        "COMMUTING",
        gram,
        excluded,
        4,
        1e-2,
    )
    assert row.parity_curl_stability_verified
    assert row.exact_normalized_parity_curl_M4 == pytest.approx(0.0, abs=1e-12)
    assert row.ridge_normalized_parity_curl_M4 == pytest.approx(0.0, abs=1e-12)


def test_smaller_eta_reduces_projection_and_curl_error() -> None:
    gram, excluded = _random_nested_grams(16, 6, seed=23)
    coarse = audit_dependency_ridge_parity_stability(
        "COARSE",
        gram,
        excluded,
        4,
        1e-2,
    )
    fine = audit_dependency_ridge_parity_stability(
        "FINE",
        gram,
        excluded,
        4,
        1e-3,
    )
    assert fine.dependency_ridge_frobenius_error_squared < (
        coarse.dependency_ridge_frobenius_error_squared
    )
    assert fine.normalized_parity_curl_difference < (
        coarse.normalized_parity_curl_difference
    )


def test_physical_transfer_bound_is_trace_weighted_and_edge_free() -> None:
    assert physical_parity_curl_transfer_bound(0.0) == 0.0
    assert physical_parity_curl_transfer_bound(1e-10) < 2e-4
    assert normalized_parity_curl_stability_bound(0.01) == pytest.approx(0.1608)
    with pytest.raises(ValueError, match="nonnegative"):
        physical_parity_curl_transfer_bound(-1.0)


def test_invalid_gram_order_and_leaf_partition_are_rejected() -> None:
    gram = np.eye(4)
    with pytest.raises(ValueError, match="0<=M<=L"):
        dependency_projection_and_ridge(gram, 2 * gram, 0.1)
    good_gram, good_excluded = _commuting_nested_grams(8, 2)
    with pytest.raises(ValueError, match="equal integral"):
        audit_dependency_ridge_parity_stability(
            "BAD-BLOCKS",
            good_gram,
            good_excluded,
            16,
            0.1,
        )


def test_report_preserves_natural_ridge_M4_and_speedup_gates() -> None:
    report = run_component_dependency_ridge_parity_stability()
    assert report.headline_metrics[
        "dependency_support_ridge_parity_stability_theorem_count"
    ] == 1
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate[
        "dependency_support_has_positive_contraction_resolvent_approximation"
    ]
    assert report.claim_gate["parity_curl_M4_is_outcome_count_free_stable"]
    assert not report.claim_gate[
        "natural_trace_weighted_dependency_ridge_error_small"
    ]
    assert not report.claim_gate["natural_bounded_ridge_parity_curl_positive"]
    assert not report.claim_gate["natural_component_M4_positive"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_theorem_removes_uniform_edge_and_common_metric_requirements() -> None:
    theorem = dependency_ridge_parity_stability_theorem()
    assert theorem.theorem_verified
    assert theorem.arbitrary_nested_positive_grams
    assert "16 epsilon" in theorem.normalized_stability
    assert "16sqrt(R)" in theorem.physical_annealed_stability
