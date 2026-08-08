import math

import numpy as np

from self_dual_wreath_trace_weighted_polar_truncation import (
    _orthogonal_projector,
    audit_polar_tree_truncation,
    audit_trace_weighted_polar,
    run_trace_weighted_polar_truncation,
    trace_weighted_polar_scaling_record,
)


def test_near_coincident_projectors_need_no_hard_edge() -> None:
    e0 = np.asarray([[1.0], [0.0]])
    angle = 1e-4
    near = np.asarray([[math.cos(angle)], [math.sin(angle)]])
    control = audit_trace_weighted_polar(
        "TEST-NEAR-LINES",
        (_orthogonal_projector(e0), _orthogonal_projector(near)),
        threshold=1e-6,
    )
    assert control.minimum_positive_frame_eigenvalue < 1e-6
    assert not control.hard_lower_edge_exists_at_threshold
    assert control.low_positive_eigenvalue_count == 1
    assert control.trace_weighted_bound_verified
    assert control.exact_discarded_frame_mass <= 1e-6


def test_weighted_polar_error_is_exactly_discarded_frame_mass() -> None:
    rng = np.random.default_rng(43)
    projectors = []
    for _ in range(5):
        basis, _ = np.linalg.qr(rng.normal(size=(7, 2)), mode="reduced")
        projectors.append(_orthogonal_projector(basis))
    control = audit_trace_weighted_polar(
        "TEST-RANDOM-PROJECTORS",
        tuple(projectors),
        threshold=0.3,
    )
    assert control.trace_weighted_bound_verified
    assert control.weighted_error_identity_residual < 1e-9
    assert math.isclose(
        control.exact_weighted_polar_error,
        control.exact_discarded_frame_mass,
        abs_tol=1e-9,
    )
    assert control.universal_discarded_frame_mass_upper_bound <= 0.3


def test_tree_budget_is_per_level_not_per_node() -> None:
    leaves = []
    for index in range(16):
        theta = (index // 2) * 0.31 + (index % 2) * 1e-4
        vector = np.asarray([[math.cos(theta)], [math.sin(theta)], [0.0]])
        leaves.append(_orthogonal_projector(vector))
    threshold = 1e-6
    control = audit_polar_tree_truncation(
        "TEST-SIXTEEN-LEAF-TREE",
        tuple(leaves),
        threshold,
    )
    assert control.nontrivial_level_count == 4
    assert control.every_level_mass_bound_respected
    assert control.coherent_hybrid_bound_respected
    assert control.maximum_level_discarded_frame_mass <= threshold + 1e-9
    assert control.theorem_trace_distance_upper_bound == 4 * math.sqrt(
        2 * threshold
    )


def test_inverse_singular_threshold_is_polynomial_in_tree_depth() -> None:
    row = trace_weighted_polar_scaling_record(48)
    predicted = math.sqrt(2) * row.binary_polar_tree_depth / 0.01
    assert math.isclose(
        row.unit_normalized_inverse_singular_threshold_cost,
        predicted,
        rel_tol=1e-12,
    )
    assert math.isclose(row.certified_total_trace_distance_upper_bound, 0.01)
    assert row.truncated_pgm_success_lower_bound > 0.49
    assert not row.natural_hard_lower_edge_required
    assert not row.center_valued_local_law_required_for_average_success
    assert not row.polynomial_truncated_polar_sampler_proved


def test_report_reframes_the_gate_without_claiming_an_algorithm() -> None:
    report = run_trace_weighted_polar_truncation()
    assert report.headline_metrics[
        "trace_weighted_polar_truncation_theorem_count"
    ] == 1
    assert report.claim_gate[
        "inverse_polynomial_frame_cutoff_suffices_for_average_success"
    ]
    assert not report.claim_gate["natural_uniform_hard_lower_edge_is_required"]
    assert not report.claim_gate[
        "center_valued_bad_block_local_law_is_required_for_average_success"
    ]
    assert not report.claim_gate[
        "tightly_normalized_node_analysis_block_encoding_proved"
    ]
    assert not report.claim_gate["polynomial_hierarchical_polar_sampler_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
