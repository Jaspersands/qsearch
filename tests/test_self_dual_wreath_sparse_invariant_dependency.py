import numpy as np
import pytest

from self_dual_wreath_cross_dependency_neutrality import audit_cross_dependency
from self_dual_wreath_orientation_fourier_reduction import (
    orientation_invariant_projector,
)
from self_dual_wreath_sparse_invariant_dependency import (
    _w6_high_multiplicity_control,
    _w6_multiplicity_control,
    audit_dependency_from_gram,
    orientation_invariant_range_basis,
    run_sparse_invariant_dependency,
)


def _distinct_triangle():
    return (
        ((3,), (2, 1)),
        ((3,), (1, 1, 1)),
        ((2, 1), (1, 1, 1)),
    )


def test_sparse_invariant_basis_matches_dense_orientation_projector() -> None:
    labels = _distinct_triangle()
    for mask in range(8):
        basis, record = orientation_invariant_range_basis(
            (2, 1),
            labels,
            mask,
        )
        dense = orientation_invariant_projector((2, 1), labels, mask)

        assert record.exact_rank_matched_representation_ring
        assert record.maximum_generator_invariance_residual < 1e-8
        assert record.leaf_basis_isometry_residual < 1e-8
        assert np.linalg.norm(basis @ basis.T - dense, ord=2) < 1e-8


def test_coefficient_gram_dependency_matches_physical_synthesis() -> None:
    labels = _distinct_triangle()
    bases = tuple(
        orientation_invariant_range_basis((2, 1), labels, mask)[0]
        for mask in range(8)
    )
    active = (0, 2, 5, 7)
    synthesis = np.concatenate(tuple(bases[mask] for mask in active), axis=1)
    gram = synthesis.T @ synthesis
    slices = {}
    offset = 0
    for mask in active:
        width = bases[mask].shape[1]
        slices[mask] = tuple(range(offset, offset + width))
        offset += width
    left_masks = (0, 2)
    right_masks = (5, 7)
    left_indices = tuple(index for mask in left_masks for index in slices[mask])
    right_indices = tuple(index for mask in right_masks for index in slices[mask])
    sparse = audit_dependency_from_gram(
        "sparse",
        gram,
        left_indices,
        right_indices,
        left_masks,
        right_masks,
        left_masks,
        right_masks,
    )
    physical = audit_cross_dependency(
        "physical",
        np.concatenate(tuple(bases[mask] for mask in left_masks), axis=1),
        np.concatenate(tuple(bases[mask] for mask in right_masks), axis=1),
    )

    assert sparse.common_range_dimension == physical.common_range_dimension == 2
    assert sparse.fractional_eigenvalues == pytest.approx(
        physical.actual_fractional_eigenvalues
    )
    assert sparse.grading_neutrality_residual < 1e-8


def test_s6_rich_multiplicity_two_control_has_only_half_channels() -> None:
    record = _w6_multiplicity_control()

    assert record.physical_ambient_dimension == 5625
    assert record.maximum_exact_invariant_multiplicity == 2
    assert record.active_orientation_count == 5
    assert record.total_leaf_coefficient_dimension == 303
    assert record.fractional_merge_count == 10
    assert record.nonneutral_fractional_merge_count == 0
    assert record.observed_fractional_eigenvalues == (0.5,)


def test_s6_multiplicity_five_control_reaches_seven_active_orientations() -> None:
    record = _w6_high_multiplicity_control()

    assert record.physical_ambient_dimension == 22500
    assert record.maximum_exact_invariant_multiplicity == 5
    assert record.active_orientation_count == 7
    assert record.total_leaf_coefficient_dimension == 500
    assert record.fractional_merge_count == 11
    assert record.nonneutral_fractional_merge_count == 0
    assert record.maximum_fractional_half_residual < 1e-8


def test_report_keeps_finite_sparse_audit_separate_from_all_n_transform() -> None:
    report = run_sparse_invariant_dependency()

    assert report.headline_metrics["sparse_invariant_validation_failure_count"] == 0
    assert report.headline_metrics["maximum_exact_invariant_multiplicity_reached"] == 5
    assert report.headline_metrics["w6_fractional_merge_count"] == 21
    assert report.headline_metrics["w6_nonneutral_fractional_merge_count"] == 0
    assert report.claim_gate["sparse_invariant_range_audit_verified"]
    assert report.claim_gate["first_s6_collision_free_multiplicity_sector_audited"]
    assert not report.claim_gate["all_n_collision_free_neutrality_proved"]
    assert not report.claim_gate["polynomial_all_n_invariant_transform_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
