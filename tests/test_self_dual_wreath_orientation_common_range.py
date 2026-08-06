import numpy as np

from self_dual_wreath_orientation_common_range import (
    audit_common_range_tuple,
    common_range_multiplicity_components,
    common_range_scaling_record,
)
from self_dual_wreath_orientation_fourier_reduction import (
    orientation_invariant_projector,
)


COMMON_W4_LABELS = (
    ((4,), (3, 1)),
    ((2, 1, 1), (1, 1, 1, 1)),
)


def _range_basis(projector: np.ndarray) -> np.ndarray:
    eigenvalues, eigenvectors = np.linalg.eigh(projector)
    return eigenvectors[:, eigenvalues > 1 - 1e-8]


def test_sign_mediated_common_range_formula_matches_matrix() -> None:
    target = (1, 1, 1, 1)
    total, trivial, sign = common_range_multiplicity_components(
        target,
        COMMON_W4_LABELS,
        1,
        2,
    )
    left = _range_basis(
        orientation_invariant_projector(
            target,
            COMMON_W4_LABELS,
            1,
        )
    )
    right = _range_basis(
        orientation_invariant_projector(
            target,
            COMMON_W4_LABELS,
            2,
        )
    )
    singular_values = np.linalg.svd(left.T @ right, compute_uv=False)
    matrix_dimension = int(np.sum(singular_values > 1 - 1e-8))
    assert (total, trivial, sign) == (1, 0, 1)
    assert matrix_dimension == total


def test_complete_w4_tuple_common_range_formula_is_exact() -> None:
    record = audit_common_range_tuple(4, COMMON_W4_LABELS)
    assert record.formula_validation_count == 50
    assert record.formula_mismatch_count == 0
    assert record.maximum_common_range_dimension_residual == 0
    assert record.distinct_common_range_pair_count == 1
    assert record.sign_mediated_common_range_pair_count == 1


def test_common_ranges_proliferate_before_information_threshold() -> None:
    record = common_range_scaling_record(8)
    assert record.copy_count == 11
    assert record.minimum_distinct_common_range_pair_fraction > 0.80
    assert record.maximum_distinct_common_range_pair_fraction > 0.87
    assert record.every_target_common_range_fraction_above_half
    assert not record.every_target_common_range_fraction_above_99_percent
    assert not record.common_range_incidence_norm_bound_proved


def test_common_ranges_are_nearly_universal_near_n10_threshold() -> None:
    record = common_range_scaling_record(10)
    assert not record.reaches_information_threshold
    assert record.copy_count == 21
    assert record.information_threshold_copy_count == 22
    assert record.minimum_distinct_common_range_pair_fraction > 0.998
    assert record.every_target_common_range_fraction_above_99_percent
    assert all(
        not sector.pairwise_transversality_holds
        for sector in record.sector_records
    )
