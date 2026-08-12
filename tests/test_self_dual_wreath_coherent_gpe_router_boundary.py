from __future__ import annotations

import math

import numpy as np
import pytest

from self_dual_wreath_coherent_gpe_router_boundary import (
    audit_coherent_gpe_analysis,
    fixed_arity_gpe_scaling_record,
    natural_gpe_moment_benchmark,
    run_coherent_gpe_router_boundary,
)


def _orthogonal_projectors(count: int) -> tuple[np.ndarray, ...]:
    output = []
    for index in range(count):
        projector = np.zeros((count, count), complex)
        projector[index, index] = 1
        output.append(projector)
    return tuple(output)


@pytest.mark.parametrize("count", (2, 4, 8, 16))
def test_controlled_gpe_on_uniform_mask_is_exactly_normalized_analysis(
    count: int,
) -> None:
    control = audit_coherent_gpe_analysis("FLAT", _orthogonal_projectors(count))

    assert control.exact_controlled_gpe_analysis_identity_verified
    assert control.flat_orthogonal_family
    assert control.controlled_gpe_to_normalized_analysis_residual == pytest.approx(0.0)
    assert control.analysis_gram_residual == pytest.approx(0.0)
    assert control.native_success_probability == pytest.approx(1 / count)
    assert control.flat_expected_success_probability == pytest.approx(1 / count)


def test_overlapping_projectors_obey_native_trace_formula() -> None:
    vectors = (
        np.asarray((1.0, 0.0, 0.0), complex),
        np.asarray((1.0, 1.0, 0.0), complex) / math.sqrt(2),
        np.asarray((0.0, 1.0, 1.0), complex) / math.sqrt(2),
    )
    projectors = tuple(np.outer(vector, vector.conj()) for vector in vectors)
    control = audit_coherent_gpe_analysis("OVERLAP", projectors)

    assert control.exact_controlled_gpe_analysis_identity_verified
    assert not control.flat_orthogonal_family
    assert control.native_success_probability == pytest.approx(
        control.native_success_trace_formula
    )


def test_sparse_mp_native_success_remains_inverse_orientation_width() -> None:
    row = natural_gpe_moment_benchmark(2**-12, 32)

    assert row.native_gpe_success_moment_ratio == pytest.approx(
        (1 + row.child_aspect) / 2**32
    )
    assert row.amplitude_amplification_query_scale == pytest.approx(
        math.sqrt(2**32 / (1 + row.child_aspect))
    )
    assert row.support_scalarization_native_error_can_be_small
    assert row.coherent_gpe_membership_success_inverse_orientation_width


def test_fixed_arity_gpe_membership_route_remains_superpolynomial() -> None:
    row = fixed_arity_gpe_scaling_record(80)

    assert row.coherent_gpe_membership_router_superpolynomial
    assert not row.direct_physical_branch_router_ruled_out
    assert row.early_child_orientation_count_log2 > 300


def test_invalid_gpe_router_inputs_are_rejected() -> None:
    with pytest.raises(ValueError):
        audit_coherent_gpe_analysis("EMPTY", ())
    with pytest.raises(ValueError):
        natural_gpe_moment_benchmark(0.75, 8)
    with pytest.raises(ValueError):
        fixed_arity_gpe_scaling_record(2)


def test_report_rejects_membership_router_but_not_physical_interference() -> None:
    report = run_coherent_gpe_router_boundary()

    assert report.theorem.theorem_verified
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["orientation_invariant_membership_projectors_gpe_measurable"]
    assert report.claim_gate["coherent_uniform_gpe_equals_normalized_analysis"]
    assert not report.claim_gate["sparse_support_scalarization_removes_gpe_width"]
    assert not report.claim_gate["coherent_gpe_membership_router_polynomial"]
    assert not report.claim_gate["direct_physical_branch_router_ruled_out"]
    assert not report.claim_gate["speedup_claim_allowed"]
