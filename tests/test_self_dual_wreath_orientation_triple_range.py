import numpy as np

from self_dual_wreath_orientation_fourier_reduction import (
    orientation_invariant_projector,
)
from self_dual_wreath_orientation_triple_range import (
    fixed_family_common_range_dimension,
    parity_kernel_assignments,
    probe_triple_support_dp_complexity,
    sample_family_common_ranges,
    sample_triple_common_ranges,
    validate_triple_range_formula,
    viable_sparse_parity_assignments,
    weighted_sparse_parity_kernel_sum,
)


W5_LABELS = (
    ((5,), (4, 1)),
    ((2, 1, 1, 1), (1, 1, 1, 1, 1)),
)


def test_three_orientation_parity_kernel_has_expected_dimension() -> None:
    assignments = parity_kernel_assignments(3)
    assert len(assignments) == 16
    assert 0 in assignments


def test_sparse_parity_kernel_matches_dense_enumeration() -> None:
    multiplicities = (
        (1, 2, 1),
        (3, 1, 3),
        (5, 4, 0),
        (7, 1, 2),
    )
    dense_total = 0
    dense_viable = []
    occupied = {pattern for pattern, _, _ in multiplicities}
    for assignment in parity_kernel_assignments(3):
        weight = 1
        if any(
            pattern not in occupied
            and ((assignment >> (pattern - 1)) & 1)
            for pattern in range(1, 8)
        ):
            weight = 0
        for pattern, trivial, sign in multiplicities:
            weight *= (trivial, sign)[(assignment >> (pattern - 1)) & 1]
        if weight:
            dense_viable.append(assignment)
            dense_total += weight

    assert sorted(viable_sparse_parity_assignments(3, multiplicities)) == sorted(
        dense_viable
    )
    assert weighted_sparse_parity_kernel_sum(3, multiplicities) == dense_total


def test_sparse_fixed_family_formula_handles_eight_orientation_cube() -> None:
    labels = (
        ((6,), (5, 1)),
        ((6,), (5, 1)),
        ((1, 1, 1, 1, 1, 1), (2, 1, 1, 1, 1)),
        ((1, 1, 1, 1, 1, 1), (2, 1, 1, 1, 1)),
        ((6,), (1, 1, 1, 1, 1, 1)),
        ((6,), (1, 1, 1, 1, 1, 1)),
    )

    assert fixed_family_common_range_dimension(
        (6,),
        labels,
        (0, 3, 12, 15, 48, 51, 60, 63),
    ) == 1


def test_fixed_family_formula_matches_projector_intersection() -> None:
    target = (1, 1, 1, 1, 1)
    masks = (1, 2, 3)
    projectors = tuple(
        orientation_invariant_projector(target, W5_LABELS, mask)
        for mask in masks
    )
    matrix_dimension = int(
        np.sum(np.linalg.eigvalsh(sum(projectors) / 3) > 1 - 1e-8)
    )
    exact_dimension = fixed_family_common_range_dimension(
        target,
        W5_LABELS,
        masks,
    )
    assert matrix_dimension == exact_dimension


def test_complete_s5_fixed_family_validation_passes() -> None:
    record = validate_triple_range_formula()
    assert record.formula_validation_count == 140
    assert record.formula_mismatch_count == 0
    assert record.maximum_common_range_dimension_residual == 0
    assert record.exact_fixed_family_formula_validation


def test_n12_triple_intersections_are_prevalent_in_declared_sample() -> None:
    record = sample_triple_common_ranges(
        12,
        (12,),
        sample_count=512,
        seed=91_000 + 1_200,
    )
    assert record.copy_count == 29
    assert record.reaches_information_threshold
    assert record.estimated_common_range_fraction > 0.90
    assert record.wilson_95_lower_bound > 0.88
    assert not record.all_orientation_triples_counted_exactly


def test_naive_exact_triple_support_dp_hits_scaling_boundary() -> None:
    small = probe_triple_support_dp_complexity(6)
    assert small.exact_dynamic_program_completed
    assert small.peak_merged_state_count == 18_784
    assert small.exact_common_range_fraction is not None
    large = probe_triple_support_dp_complexity(8)
    assert not large.exact_dynamic_program_completed
    assert large.peak_merged_state_count > large.state_cap
    assert large.exact_common_range_fraction is None


def test_exact_common_range_incidence_drops_between_four_and_five() -> None:
    four = sample_family_common_ranges(
        12,
        (12,),
        family_size=4,
        sample_count=512,
        seed=124_000,
    )
    five = sample_family_common_ranges(
        12,
        (12,),
        family_size=5,
        sample_count=512,
        seed=125_000,
    )
    assert 0 < four.estimated_common_range_fraction < 0.10
    assert five.common_range_sample_count == 0
    assert five.wilson_95_upper_bound < 0.01
