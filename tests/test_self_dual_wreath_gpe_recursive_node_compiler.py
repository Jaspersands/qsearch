import math

import numpy as np

from self_dual_wreath_gpe_recursive_node_compiler import (
    _synthesis_for_metric,
    audit_recursive_node_compiler,
    compile_flat_affine_embedding,
    hierarchical_conditioning_counterexample,
    run_gpe_recursive_node_compiler,
)


def test_equal_shorted_metrics_give_exact_hadamard_mixer() -> None:
    metric = np.diag([0.2, 0.7, 1.4]).astype(complex)
    synthesis = _synthesis_for_metric(metric)
    record = audit_recursive_node_compiler(
        "TEST-EQUAL-METRICS",
        synthesis,
        synthesis,
        np.eye(3, dtype=complex),
    )
    assert record.exact_recursive_normal_form_verified
    assert record.endpoint_mixer_is_exact_hadamard
    assert record.endpoint_mixer_is_scalar
    assert abs(record.minimum_endpoint_gap - 0.5) <= 1e-10
    assert record.relation_factorization_residual <= 1e-10


def test_noncommuting_metrics_require_matrix_valued_endpoint_mixer() -> None:
    angle = 0.43
    rotation = np.asarray(
        [
            [math.cos(angle), -math.sin(angle)],
            [math.sin(angle), math.cos(angle)],
        ],
        dtype=complex,
    )
    left_metric = np.diag([1.0, 5.0]).astype(complex)
    right_metric = rotation @ np.diag([4.0, 1.5]) @ rotation.conj().T
    record = audit_recursive_node_compiler(
        "TEST-NONCOMMUTING-METRICS",
        _synthesis_for_metric(left_metric),
        _synthesis_for_metric(right_metric),
        np.eye(2, dtype=complex),
    )
    assert record.exact_recursive_normal_form_verified
    assert record.metric_commutator_norm > 0.1
    assert not record.endpoint_mixer_is_scalar
    assert not record.endpoint_mixer_is_exact_hadamard
    assert record.minimum_endpoint_gap > 0.05


def test_gpe_pair_availability_does_not_prevent_vanishing_recursive_gap() -> None:
    rows = [hierarchical_conditioning_counterexample(e) for e in (4, 8, 16)]
    assert all(row.pair_gpe_transport_available for row in rows)
    assert all(
        right.minimum_endpoint_gap < left.minimum_endpoint_gap
        for left, right in zip(rows, rows[1:])
    )
    assert rows[-1].inverse_gap_cost == (1 << 16) + 1
    assert not rows[-1].constant_endpoint_gap


def test_flat_affine_embedding_compiles_in_affine_dimension() -> None:
    masks = (2, 3, 12, 13)
    angles = (0.0, 0.2, -0.7, 1.1)
    fibers = {
        mask: np.asarray(
            [
                [math.cos(angle), -math.sin(angle)],
                [math.sin(angle), math.cos(angle)],
                [0.0, 0.0],
            ],
            dtype=complex,
        )
        for mask, angle in zip(masks, angles)
    }
    direct, compiled, stages = compile_flat_affine_embedding(fibers, 4)
    assert stages == 2
    assert np.linalg.norm(direct - compiled, ord=2) <= 1e-10
    assert np.linalg.norm(compiled.conj().T @ compiled - np.eye(2), ord=2) <= 1e-10


def test_report_keeps_all_n_recursive_claims_closed() -> None:
    report = run_gpe_recursive_node_compiler()
    assert report.headline_metrics[
        "recursive_parent_relation_normal_form_theorem_count"
    ] == 1
    assert report.headline_metrics[
        "finite_affine_gpe_compiler_failure_count"
    ] == 0
    assert report.claim_gate[
        "flat_affine_embedding_has_logarithmic_transport_depth"
    ]
    assert report.claim_gate[
        "universal_scalar_affine_child_embeddings_falsified"
    ]
    assert not report.claim_gate[
        "gpe_pair_transport_alone_compiles_recursive_relation"
    ]
    assert not report.claim_gate["all_n_structured_child_embedding_proved"]
    assert not report.claim_gate["polynomial_uniform_generator_select_proved"]
    assert not report.claim_gate["natural_recursive_endpoint_gap_proved"]
    assert not report.claim_gate["recursive_orientation_polar_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
