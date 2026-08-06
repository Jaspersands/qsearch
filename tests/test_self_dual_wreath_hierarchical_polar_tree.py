import numpy as np

from self_dual_wreath_hierarchical_polar_tree import (
    hierarchical_polar_scaling_record,
    polar_frame,
    recursive_polar_chain,
    run_hierarchical_polar_tree,
)


def _rank_one(vector):
    normalized = np.asarray(vector, dtype=float)
    normalized /= np.linalg.norm(normalized)
    return np.outer(normalized, normalized)


def test_recursive_chain_equals_direct_polar_for_noncommuting_leaves():
    projectors = (
        _rank_one([1, 0, 0]),
        _rank_one([1, 1, 0]),
        _rank_one([0, 1, 1]),
        _rank_one([0, 0, 1]),
    )

    recursive, frame, effects = recursive_polar_chain(projectors)
    direct, direct_frame = polar_frame(projectors)

    assert np.linalg.norm(frame - direct_frame, ord=2) < 1e-10
    assert np.linalg.norm(recursive - direct, ord=2) < 1e-9
    assert len(effects) == 3


def test_complete_w4_hierarchical_controls_are_exact_and_half_integral():
    report = run_hierarchical_polar_tree()
    metrics = report.headline_metrics

    assert metrics["finite_w4_control_count"] == 156
    assert metrics["finite_hierarchical_validation_failure_count"] == 0
    assert metrics["finite_half_integral_relative_effect_failure_count"] == 0
    assert metrics["finite_noncommuting_child_frame_count"] > 0
    assert metrics["maximum_recursive_to_direct_polar_residual"] < 1e-8
    assert report.claim_gate["exact_hierarchical_polar_factorization_proved"]
    assert not report.claim_gate["higher_level_relative_sampler_polynomial"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_orientation_tree_has_polynomial_depth_but_open_relative_sampler():
    record = hierarchical_polar_scaling_record(128)

    assert record.binary_tree_depth == record.information_threshold_copy_count
    assert record.coherently_indexed_level_count == record.binary_tree_depth
    assert record.base_pair_relative_sampler_polynomial
    assert not record.higher_level_relative_sampler_polynomial
    assert record.proposed_leaf_projector_acts_globally_on_all_source_labels
    assert record.proposed_sampler_preserves_coherent_internal_labels
    assert not record.formal_mrs_sieve_theorem_directly_applies
