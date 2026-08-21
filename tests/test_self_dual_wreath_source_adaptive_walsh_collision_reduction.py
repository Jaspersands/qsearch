import json

import numpy as np
import pytest

from self_dual_wreath_source_adaptive_walsh_collision_reduction import (
    adaptive_subset_collision_bound,
    audit_walsh_collision,
    best_subset_mass,
    collision_from_autocorrelations,
    native_walsh_distribution,
    normalized_orientation_autocorrelations,
    regular_collision_scaling_record,
    run_source_adaptive_walsh_collision_reduction,
    source_adaptive_walsh_collision_theorem,
    write_source_adaptive_walsh_collision_report,
)


def _rank_one_projector(vector: np.ndarray) -> np.ndarray:
    vector = vector / np.linalg.norm(vector)
    return np.outer(vector, vector.conj())


def test_native_distribution_and_autocorrelation_parseval() -> None:
    projectors = (
        _rank_one_projector(np.array([1.0, 0.0])),
        _rank_one_projector(np.array([1.0, 1.0])),
        _rank_one_projector(np.array([0.0, 1.0])),
        _rank_one_projector(np.array([1.0, -1.0])),
    )
    probabilities = native_walsh_distribution(projectors)
    correlations = normalized_orientation_autocorrelations(projectors)
    assert sum(probabilities) == pytest.approx(1.0)
    assert correlations[0] == pytest.approx(1.0)
    assert sum(value * value for value in probabilities) == pytest.approx(
        collision_from_autocorrelations(correlations)
    )


def test_adaptive_subset_bound_holds_for_heavy_modes() -> None:
    probabilities = (0.4, 0.3, 0.2, 0.1)
    collision = sum(value * value for value in probabilities)
    retained = best_subset_mass(probabilities, 2)
    bound = adaptive_subset_collision_bound(collision, 2)
    assert retained == pytest.approx(0.7)
    assert retained <= bound
    with pytest.raises(ValueError):
        best_subset_mass(probabilities, 5)


def test_regular_collision_benchmark_is_asymptotically_uniform() -> None:
    small = regular_collision_scaling_record(16)
    large = regular_collision_scaling_record(128)
    assert small.regular_collision_to_uniform_ratio >= 1.0
    assert large.regular_collision_to_uniform_ratio == pytest.approx(1.0)
    assert large.adaptive_polynomial_mode_retained_upper_bound < (
        small.adaptive_polynomial_mode_retained_upper_bound
    )
    assert not large.physical_plancherel_collision_bound_proved
    assert not large.physical_source_adaptive_router_rejected


def test_physical_collision_control_matches_both_formulas() -> None:
    from self_dual_wreath_orientation_fusion_moment import _w4_collision_free_labels

    control = audit_walsh_collision(
        "W4-TEST",
        4,
        (2, 2),
        _w4_collision_free_labels()[0],
    )
    assert control.exact_native_collision_reduction_verified
    assert control.adaptive_subset_bound_verified
    assert control.collision_parseval_residual <= 1e-10
    assert control.probability_sum_residual <= 1e-10


def test_live_report_keeps_physical_collision_as_open_gate() -> None:
    theorem = source_adaptive_walsh_collision_theorem()
    report = run_source_adaptive_walsh_collision_reduction()
    assert theorem.theorem_verified
    assert report.claim_gate["native_walsh_collision_autocorrelation_identity_proved"]
    assert report.claim_gate["source_adaptive_size_m_retention_bound_proved"]
    assert report.claim_gate[
        "exchangeable_source_law_reduces_to_K_plus_one_hamming_strata"
    ]
    assert not report.claim_gate[
        "globally_distinct_physical_plancherel_collision_small_proved"
    ]
    assert not report.claim_gate["source_label_adaptive_sparse_mode_router_rejected"]
    assert not report.claim_gate["source_label_adaptive_sparse_mode_router_compiled"]
    assert not report.claim_gate["complete_natural_orientation_polar_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_finite_physical_controls_are_near_flat_but_not_promoted() -> None:
    report = run_source_adaptive_walsh_collision_reduction()
    assert report.headline_metrics["finite_physical_control_count"] == 5
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.headline_metrics["maximum_w4_single_mode_probability"] <= 0.3 + 1e-10
    assert report.headline_metrics["maximum_w5_single_mode_probability"] <= 0.128
    assert report.headline_metrics["physical_plancherel_collision_theorem_count"] == 0


def test_report_writer_preserves_open_obligation(tmp_path) -> None:
    path = tmp_path / "adaptive-collision.json"
    payload = write_source_adaptive_walsh_collision_report(path)
    loaded = json.loads(path.read_text())
    assert loaded == payload
    assert loaded["headline_metrics"]["native_walsh_collision_parseval_theorem_count"] == 1
    assert loaded["headline_metrics"]["source_adaptive_subset_collision_bound_count"] == 1
    assert loaded["headline_metrics"]["source_adaptive_sparse_router_no_go_count"] == 0
    assert loaded["headline_metrics"]["source_adaptive_sparse_router_compiler_count"] == 0
    assert loaded["headline_metrics"]["new_quantum_algorithm_count"] == 0
