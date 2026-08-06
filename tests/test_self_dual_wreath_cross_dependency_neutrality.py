import numpy as np
import pytest

from self_dual_wreath_cross_dependency_neutrality import (
    audit_cross_dependency,
    audit_wreath_cross_dependencies,
    run_cross_dependency_neutrality,
)


def _distinct_triangle():
    return (
        ((3,), (2, 1)),
        ((3,), (1, 1, 1)),
        ((2, 1), (1, 1, 1)),
    )


def test_dependency_grading_recovers_unbalanced_fractional_spectrum() -> None:
    record = audit_cross_dependency(
        "unequal",
        np.diag((np.sqrt(2.0), 1.0)),
        np.diag((1.0, np.sqrt(2.0))),
    )

    assert record.exact_dependency_quotient_theorem_verified
    assert record.cross_dependency_dimension == 2
    assert not record.grading_neutral
    assert record.actual_fractional_eigenvalues == pytest.approx((1 / 3, 2 / 3))
    assert record.dependency_predicted_fractional_eigenvalues == pytest.approx(
        (1 / 3, 2 / 3)
    )


def test_internal_synthesis_kernels_are_removed_from_cross_dependencies() -> None:
    left = np.array([[1.0, 1.0], [0.0, 0.0]])
    right = np.array([[2.0, 0.0], [0.0, 0.0]])
    record = audit_cross_dependency("redundant", left, right)

    assert record.left_coefficient_dimension + record.right_coefficient_dimension == 4
    assert record.common_range_dimension == 1
    assert record.cross_dependency_dimension == 1
    assert record.dependency_to_common_range_dimension_residual == 0
    assert record.exact_dependency_quotient_theorem_verified


def test_distinct_w3_dependencies_are_all_neutral() -> None:
    record = audit_wreath_cross_dependencies(
        "distinct",
        3,
        (2, 1),
        _distinct_triangle(),
    )

    assert record.fractional_merge_count == 9
    assert record.exact_dependency_theorem_failure_count == 0
    assert record.nonneutral_fractional_merge_count == 0
    assert all(row.grading_neutral for row in record.records)


def test_repeated_labels_produce_nonneutral_cross_dependencies() -> None:
    record = audit_wreath_cross_dependencies(
        "repeated",
        3,
        (2, 1),
        (((3,), (2, 1)),) * 3,
    )

    assert record.exact_dependency_theorem_failure_count == 0
    assert record.nonneutral_fractional_merge_count > 0
    observed = {
        round(value, 8)
        for row in record.records
        for value in row.actual_fractional_eigenvalues
    }
    assert round(1 / 3, 8) in observed
    assert round(2 / 3, 8) in observed


def test_report_keeps_symbolic_and_algorithmic_claims_open() -> None:
    report = run_cross_dependency_neutrality()

    assert report.headline_metrics["finite_theorem_validation_failure_count"] == 0
    assert report.claim_gate["cross_dependency_quotient_theorem_proved"]
    assert report.claim_gate["finite_label_simple_dependencies_neutral"]
    assert report.claim_gate["repeated_labels_falsify_universal_neutrality"]
    assert not report.claim_gate[
        "symbolic_wreath_dependency_decomposition_proved"
    ]
    assert not report.claim_gate["all_n_collision_free_neutrality_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
