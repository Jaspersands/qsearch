import numpy as np

from self_dual_wreath_orientation_fourier_reduction import (
    _w4_collision_free_labels,
)
from self_dual_wreath_physical_orientation_interference import (
    _physical_orientation_operators,
)
from self_dual_wreath_postfilter_frame_compression import (
    _physical_orientation_linear_maps,
    audit_exact_compression,
    run_postfilter_frame_compression,
)


def test_matrix_free_orientation_maps_match_dense_physical_operators() -> None:
    labels = _w4_collision_free_labels()[0]
    generators = (1, 2)
    dense_transform, dense_accepted = _physical_orientation_operators(
        labels,
        generators,
    )
    transform, transform_adjoint, accepted = _physical_orientation_linear_maps(
        labels,
        generators,
    )
    vector = np.random.default_rng(20260806).normal(size=len(dense_transform))
    assert np.allclose(transform(vector), dense_transform @ vector)
    assert np.allclose(transform_adjoint(vector), dense_transform.T @ vector)
    assert np.allclose(accepted(vector), dense_accepted @ vector)


def test_exact_kraus_frame_reduces_to_principal_compression() -> None:
    labels = _w4_collision_free_labels()[0]
    control = audit_exact_compression(
        4,
        labels,
        (1, 2),
        control_id="W4-COMPRESSION",
    )
    assert control.exact_compression_theorem_verified
    assert control.kraus_to_direct_compression_residual < 1e-10
    assert control.isotypic_frame_commutator_residual < 1e-10
    assert control.interlacing_bound_verified
    assert control.equality_criterion_predicts_top_preservation
    assert control.raw_top_preserved


def test_complete_finite_portfolio_blocks_conditioned_norm_claim() -> None:
    report = run_postfilter_frame_compression()
    metrics = report.headline_metrics
    assert metrics["exact_w4_control_count"] == 30
    assert metrics["matrix_free_w5_probe_count"] == 21
    assert metrics["exact_validation_failure_count"] == 0
    assert metrics["raw_top_preservation_count"] == 45
    assert metrics["raw_top_reduction_count"] == 6
    assert metrics[
        "discarded_label_conditioned_frame_norm_improvement_count"
    ] == 0
    assert metrics[
        "coherent_tagged_w4_conditioned_frame_norm_improvement_count"
    ] == 2
    assert metrics[
        "coherent_tagged_w4_conditioned_frame_norm_nonworsening_count"
    ] == 8
    assert metrics[
        "coherent_tagged_w5_conditioned_frame_norm_improvement_count"
    ] == 9
    assert metrics[
        "coherent_tagged_all_finite_conditioned_frame_norm_improvement_count"
    ] == 11
    assert metrics["minimum_conditioned_top_norm_ratio"] > 1
    assert metrics["minimum_coherent_tagged_conditioned_top_norm_ratio"] < 1
    assert metrics["minimum_coherent_tagged_w5_conditioned_top_norm_ratio"] < 0.86
    assert report.claim_gate["exact_average_frame_compression_proved"]
    assert report.claim_gate[
        "coherent_isotypic_label_can_reduce_conditioned_frame_norm"
    ]
    assert not report.claim_gate["postfilter_polynomial_frame_norm_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
