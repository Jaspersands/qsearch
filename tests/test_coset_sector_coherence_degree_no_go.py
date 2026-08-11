import math

import numpy as np
import pytest

from coset_sector_coherence_degree_no_go import (
    audit_sector_coherence_bound,
    cyclic_clique_control,
    minimum_sector_local_depth,
    run_sector_coherence_degree_no_go,
    sector_coherence_degree_theorem,
    symmetric_group_coherence_scaling_record,
)


def test_dephased_seed_recovers_largest_atom_bound() -> None:
    control = cyclic_clique_control(
        8,
        (1, 1, 1, 1, 1, 1, 1, 1),
        3,
    )
    assert control.maximum_coherence_degree == 0
    assert control.coherence_graph_spectral_factor == pytest.approx(1.0)
    assert control.exact_success_probability == pytest.approx(1 / 8)
    assert control.maximum_plancherel_atom == pytest.approx(1 / 8)
    assert control.graph_bound_saturated
    assert control.exact_sector_coherence_bound_verified


@pytest.mark.parametrize(
    ("order", "components", "selected", "expected_success"),
    (
        (8, (2, 2, 2, 2), 0, 2 / 8),
        (12, (3, 3, 3, 3), 2, 3 / 12),
        (12, (4, 4, 4), 1, 4 / 12),
    ),
)
def test_clique_controls_saturate_graph_spectral_bound(
    order: int,
    components: tuple[int, ...],
    selected: int,
    expected_success: float,
) -> None:
    control = cyclic_clique_control(order, components, selected)
    width = components[selected]
    assert control.maximum_coherence_degree == width - 1
    assert control.coherence_graph_spectral_factor == pytest.approx(width)
    assert control.exact_success_probability == pytest.approx(expected_success)
    assert control.graph_spectral_success_upper_bound == pytest.approx(
        expected_success
    )
    assert control.graph_bound_saturated
    assert control.exact_sector_coherence_bound_verified


def test_omitted_coherence_is_charged_by_robust_bound() -> None:
    control = cyclic_clique_control(
        12,
        (4, 4, 4),
        0,
        declared_empty_graph=True,
    )
    assert control.maximum_coherence_degree == 0
    assert control.exact_success_probability == pytest.approx(1 / 3)
    assert control.graph_spectral_success_upper_bound == pytest.approx(1 / 12)
    assert control.omitted_block_trace_mass == pytest.approx(1 / 4)
    assert control.robust_graph_success_upper_bound == pytest.approx(1 / 3)
    assert control.robust_bound_residual <= 1e-10
    assert control.exact_sector_coherence_bound_verified


def test_invalid_covariant_seed_constraint_is_rejected() -> None:
    state = np.diag([1.0, 0.0, 0.0, 0.0])
    invalid_seed = np.eye(4) / 3
    with pytest.raises(ValueError, match="covariant completeness"):
        audit_sector_coherence_bound(
            "INVALID",
            4,
            (1, 1, 1, 1),
            (1, 1, 1, 1),
            invalid_seed,
            state,
        )


def test_sector_local_depth_formula_is_exact_integer_corollary() -> None:
    atom = 2.0**-40
    target = 0.5
    degree = 4
    depth = minimum_sector_local_depth(atom, target, degree)
    assert degree ** (2 * depth) * atom >= target
    assert depth == 10
    assert degree ** (2 * (depth - 1)) * atom < target


def test_symmetric_group_scaling_and_scope_gates() -> None:
    row = symmetric_group_coherence_scaling_record(16)
    theorem = sector_coherence_degree_theorem()
    assert row.maximum_plancherel_atom > 0
    assert row.minimum_required_maximum_degree >= 1
    assert row.minimum_sector_local_layer_depth >= 1
    assert theorem.arbitrary_finite_group
    assert theorem.arbitrary_copy_count
    assert not theorem.polynomial_sector_degree_constant_success_possible
    assert not theorem.implicitly_dense_structured_transform_ruled_out


def test_report_preserves_dense_transform_and_speedup_gates() -> None:
    report = run_sector_coherence_degree_no_go()
    assert report.headline_metrics[
        "sector_coherence_graph_bound_theorem_count"
    ] == 1
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.headline_metrics["sharp_finite_control_count"] == 4
    assert not report.claim_gate[
        "structured_dense_cross_sector_transform_ruled_out"
    ]
    assert not report.claim_gate["carrier_sensitive_covariant_decoder_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
    assert report.status == (
        "sector-sparse-decoders-closed-structured-dense-transform-open"
    )
