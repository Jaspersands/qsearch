import numpy as np
import pytest

from self_dual_wreath_vertex_trivialization_criterion import (
    normalized_vertex_gram,
    regular_simplex_holonomy_counterexample,
    run_vertex_trivialization_criterion,
)


def test_normalized_vertex_gram_psd_is_exact_factorization_criterion() -> None:
    gamma = 0.2
    source = np.array(
        [
            [1.0, gamma, gamma],
            [gamma, 1.0, gamma],
            [gamma, gamma, 1.0],
        ]
    )
    normalized = normalized_vertex_gram(source, gamma)

    assert np.linalg.eigvalsh(normalized).min() >= -1e-12
    assert np.allclose(np.diag(normalized), 1.0)
    assert np.allclose(
        source,
        (1 - gamma) * np.eye(3) + gamma * normalized,
    )


@pytest.mark.parametrize("width", [3, 4, 5, 8, 12])
def test_regular_simplex_kills_uniform_magnitude_implication(width: int) -> None:
    record = regular_simplex_holonomy_counterexample(width)

    assert record.reciprocal_correlation == pytest.approx(1 / (width - 1))
    assert record.pairwise_uniform_reciprocal_correlations
    assert record.normalized_vertex_gram_minimum_eigenvalue == pytest.approx(
        2 - width,
        abs=1e-9,
    )
    assert record.normalized_vertex_gram_negative_eigenvalue_count == 1
    assert record.triangle_normalized_holonomy == -1
    assert not record.vertex_trivialization_exists
    assert record.star_relation_metric_minimum_eigenvalue == pytest.approx(1)
    if width > 3:
        assert record.claimed_floor_violation < 0
    assert record.exact_counterexample_audit


def test_finite_natural_controls_pass_without_unlocking_all_depth_claim() -> None:
    report = run_vertex_trivialization_criterion()

    assert report.claim_gate["vertex_trivialization_psd_criterion_proved"]
    assert report.claim_gate[
        "constructive_vertex_isometry_gram_factor_proved"
    ]
    assert not report.claim_gate["uniform_reciprocal_magnitude_sufficient"]
    assert report.claim_gate["signed_cycle_holonomy_can_falsify_trivialization"]
    assert report.claim_gate["selected_natural_finite_vertices_pass"]
    assert not report.claim_gate[
        "all_depth_natural_vertex_trivialization_proved"
    ]
    assert not report.claim_gate[
        "unconditional_width_independent_laplacian_floor_proved"
    ]
    assert not report.claim_gate["speedup_claim_allowed"]
