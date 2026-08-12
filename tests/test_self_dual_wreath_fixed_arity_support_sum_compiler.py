from __future__ import annotations

import math

import numpy as np
import pytest

from self_dual_wreath_fixed_arity_support_sum_compiler import (
    UNIFORM_FREE_BINOMIAL_LOWER_EDGE,
    UNIFORM_FREE_BINOMIAL_UPPER_EDGE,
    audit_stacked_support_access,
    free_binomial_support_record,
    post_router_compiler_scaling_record,
    run_fixed_arity_support_sum_compiler,
)


@pytest.mark.parametrize("arity", (8, 16, 256, 65536))
@pytest.mark.parametrize("beta", (2.0, 2.5, 3.0, 3.999))
def test_free_binomial_jump_has_uniform_atom_free_bulk(
    arity: int,
    beta: float,
) -> None:
    row = free_binomial_support_record(arity, beta)

    assert row.no_endpoint_atoms
    assert row.uniform_edge_bounds_verified
    assert row.continuous_support_lower >= UNIFORM_FREE_BINOMIAL_LOWER_EDGE - 1e-12
    assert row.continuous_support_upper <= UNIFORM_FREE_BINOMIAL_UPPER_EDGE + 1e-12


def test_free_binomial_edges_converge_to_mp_edges() -> None:
    row = free_binomial_support_record(1 << 24, 2.5)

    assert row.continuous_support_lower == pytest.approx(
        (math.sqrt(2.5) - 1) ** 2,
        rel=1e-6,
    )
    assert row.continuous_support_upper == pytest.approx(
        (math.sqrt(2.5) + 1) ** 2,
        rel=1e-6,
    )


def test_stacked_support_prepare_select_identity_is_exact() -> None:
    dimension = 8
    supports = []
    for index in range(4):
        projector = np.zeros((dimension, dimension), complex)
        projector[index, index] = 1
        supports.append(projector)
    control = audit_stacked_support_access(
        "STACK",
        tuple(supports),
        qsvt_window_lower=UNIFORM_FREE_BINOMIAL_LOWER_EDGE,
    )

    assert control.exact_stacked_prepare_select_identity_verified
    assert control.stacked_gram_residual == pytest.approx(0.0)
    assert control.normalized_stacked_operator_norm == pytest.approx(0.5)
    assert control.predicted_normalized_operator_norm == pytest.approx(0.5)


def test_fixed_arity_qsvt_cost_is_constant_in_n_but_grows_with_R() -> None:
    rows = [post_router_compiler_scaling_record(bits) for bits in (8, 16, 24)]

    assert all(row.jump_qsvt_overhead_constant_in_n for row in rows)
    assert all(row.final_root_overhead_constant_in_n for row in rows)
    assert all(row.flattened_early_router_assumed for row in rows)
    assert all(not row.flattened_early_router_proved for row in rows)
    assert all(
        right.qsvt_select_call_upper_proxy > left.qsvt_select_call_upper_proxy
        for left, right in zip(rows, rows[1:])
    )


def test_invalid_fixed_arity_support_parameters_are_rejected() -> None:
    with pytest.raises(ValueError):
        free_binomial_support_record(4, 2.0)
    with pytest.raises(ValueError):
        free_binomial_support_record(8, 4.0)
    with pytest.raises(ValueError):
        post_router_compiler_scaling_record(2)
    with pytest.raises(ValueError):
        post_router_compiler_scaling_record(8, spectral_window_lower=0.2)


def test_report_isolates_router_without_promoting_conditional_compiler() -> None:
    report = run_fixed_arity_support_sum_compiler()

    assert report.theorem.theorem_verified
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["fixed_arity_support_sum_free_binomial_law_proved"]
    assert report.claim_gate["fixed_R_jump_overhead_constant_in_n_given_router"]
    assert report.claim_gate["final_root_overhead_constant_in_n_given_router"]
    assert not report.claim_gate["uniform_finite_n_operator_edge_proved"]
    assert not report.claim_gate["flattened_early_orientation_router_proved"]
    assert not report.claim_gate["orientation_polar_compiled_unconditionally"]
    assert not report.claim_gate["speedup_claim_allowed"]
