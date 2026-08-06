import numpy as np

from representation_obstruction import integer_partitions
from self_dual_wreath_orientation_fourier_reduction import (
    compressed_fourier_block,
    orientation_invariant_projector,
)
from self_dual_wreath_orientation_fusion_moment import (
    exact_orientation_projector_overlap,
    fusion_moment_scaling_record,
    orientation_average_moment_vectors,
    run_orientation_fusion_moment,
)


W4_LABELS = (
    ((4,), (3, 1)),
    ((2, 2), (2, 1, 1)),
)


def test_exact_pair_overlap_matches_projector_matrices() -> None:
    target = (2, 2)
    for left_mask in range(4):
        left = orientation_invariant_projector(
            target,
            W4_LABELS,
            left_mask,
        )
        for right_mask in range(4):
            right = orientation_invariant_projector(
                target,
                W4_LABELS,
                right_mask,
            )
            exact = exact_orientation_projector_overlap(
                target,
                W4_LABELS,
                left_mask,
                right_mask,
            )
            assert abs(float(exact) - np.trace(left @ right)) < 1e-10


def test_class_algebra_moments_match_exact_w4_fourier_blocks() -> None:
    traces, squared_traces, residual, total_residual, negatives = (
        orientation_average_moment_vectors(4, W4_LABELS)
    )
    assert residual < 1e-10
    assert total_residual == 0
    assert negatives == 0
    for index, target in enumerate(integer_partitions(4)):
        block = compressed_fourier_block(target, W4_LABELS)
        assert abs(float(traces[index]) - np.trace(block)) < 1e-10
        assert abs(
            float(squared_traces[index]) - np.trace(block @ block)
        ) < 1e-10


def test_threshold_second_moment_is_nonobstructing_but_not_a_norm_bound() -> None:
    record = fusion_moment_scaling_record(12)
    assert record.reaches_information_threshold
    assert record.copy_count == 29
    assert record.negative_reconstructed_class_product_count == 0
    assert record.reconstructed_class_product_total_residual == 0
    assert record.maximum_collision_lower_bound_to_target_ratio < 2
    assert record.second_moment_superquartic_obstruction_count == 0
    assert not record.uniform_projector_sum_norm_proved


def test_report_proves_pair_and_second_moment_reductions_only() -> None:
    report = run_orientation_fusion_moment()
    metrics = report.headline_metrics
    assert metrics["complete_w4_fusion_tuple_validation_count"] == 15
    assert metrics["pair_overlap_formula_validation_count"] == 48
    assert metrics["finite_pair_overlap_validation_failure_count"] == 0
    assert metrics["w4_common_range_pair_count"] == 2
    assert metrics["maximum_w4_nontrivial_canonical_correlation"] < 0.51
    assert report.claim_gate[
        "pairwise_character_convolution_formula_proved"
    ]
    assert report.claim_gate[
        "orientation_average_second_moment_formula_proved"
    ]
    assert not report.claim_gate[
        "second_moment_operator_norm_upper_bound_proved"
    ]
    assert not report.claim_gate["speedup_claim_allowed"]
