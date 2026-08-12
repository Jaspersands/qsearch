from __future__ import annotations

import math

import numpy as np
import pytest

from self_dual_wreath_flat_holonomy_component_no_go import (
    NATURAL_COMMUTING_EFFECT_ERROR_FLOOR,
    _phase,
    _rotation,
    audit_flat_holonomy_component,
    audit_flat_support_pattern,
    flat_holonomy_scaling_record,
    flat_holonomy_section,
    run_flat_holonomy_component_no_go,
)


def test_arbitrary_flat_unitary_transports_give_scalar_effects() -> None:
    identity = np.eye(3, dtype=complex)
    control = audit_flat_holonomy_component(
        "ARBITRARY",
        (identity, _rotation(0.37), _phase(0.2, -0.6)),
        identity,
        tuple([1 / math.sqrt(3)] * 3),
    )

    assert control.exact_flat_holonomy_scalarization_verified
    assert control.maximum_component_scalar_residual == pytest.approx(0, abs=1e-12)
    assert control.normalized_component_m4 == pytest.approx(0, abs=1e-12)


def test_holonomy_fixed_subspace_does_not_create_matrix_effects() -> None:
    identity = np.eye(3, dtype=complex)
    basis = identity[:, (0, 2)]
    control = audit_flat_holonomy_component(
        "FIXED-SPACE",
        (identity, _rotation(0.19), _phase(0.7, -0.3)),
        basis,
        (math.sqrt(0.2), math.sqrt(0.3), math.sqrt(0.5)),
    )

    assert control.holonomy_fixed_space_dimension == 2
    assert control.scalar_vertex_weights == pytest.approx((0.2, 0.3, 0.5))
    assert control.component_effects_pairwise_commute
    assert control.exact_flat_holonomy_scalarization_verified


def test_flat_section_rejects_unnormalized_vertex_amplitudes() -> None:
    identity = np.eye(2, dtype=complex)
    with pytest.raises(ValueError):
        flat_holonomy_section((identity, identity), identity, (1.0, 1.0))


def test_flat_full_fiber_support_pattern_obeys_rank_mismatch_bound() -> None:
    supports = []
    for index in range(4):
        projector = np.zeros((8, 8), dtype=complex)
        projector[2 * index, 2 * index] = 1
        projector[2 * index + 1, 2 * index + 1] = 1
        supports.append(projector)
    control = audit_flat_support_pattern(
        "ONE-ACTIVE",
        tuple(supports),
        (0,),
    )

    assert control.normalized_natural_total_support_rank == pytest.approx(1)
    assert control.normalized_flat_support_approximation_error >= (
        control.rank_only_error_lower_bound
    )
    assert control.rank_mismatch_bound_verified


def test_scaling_record_rejects_flat_holonomy_despite_gap_solver() -> None:
    row = flat_holonomy_scaling_record(2.0)

    assert row.natural_support_m4_limit == pytest.approx(2)
    assert row.flat_holonomy_effect_m4 == 0
    assert row.commuting_effect_error_floor == pytest.approx(
        NATURAL_COMMUTING_EFFECT_ERROR_FLOOR
    )
    assert not row.flat_equal_rank_holonomy_sufficient
    assert row.partial_support_or_operator_metric_required


def test_report_preserves_nonflat_gpe_and_algorithmic_boundaries() -> None:
    report = run_flat_holonomy_component_no_go()

    assert report.headline_metrics["flat_holonomy_architecture_no_go_count"] == 1
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["flat_equal_rank_holonomy_component_povm_rejected"]
    assert report.claim_gate["partial_support_or_operator_metric_required"]
    assert not report.claim_gate["all_gpe_holonomy_routes_rejected"]
    assert not report.claim_gate["partial_support_gpe_holonomy_compiled"]
    assert not report.claim_gate["hidden_label_decoder_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
