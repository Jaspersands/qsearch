from __future__ import annotations

from self_dual_wreath_point_effect_qsvt_no_go import (
    audit_point_beta_purity,
    run_point_effect_qsvt_no_go,
    typical_point_beta_scaling_record,
)


THRESHOLD_LABELS = (
    ((3,), (2, 1)),
    ((3,), (1, 1, 1)),
    ((2, 1), (1, 1, 1)),
)


def test_beta_squared_is_bounded_by_centered_energy_and_purity() -> None:
    for n, labels in (
        (3, (((3,), (2, 1)),)),
        (3, THRESHOLD_LABELS),
        (4, (((4,), (3, 1)), ((2, 2), (2, 1, 1)))),
    ):
        control = audit_point_beta_purity(n, labels, control_id=str(n))
        assert control.beta_purity_chain_verified
        assert control.centered_operator_norm_squared <= (
            control.centered_hilbert_schmidt_norm_squared + 1e-10
        )
        assert control.centered_hilbert_schmidt_norm_squared <= (
            control.native_state_purity + 1e-10
        )
        assert control.twirl_difference_projection_residual < 1e-10


def test_conditional_typical_beta_bound_forces_superpolynomial_qsvt() -> None:
    records = [typical_point_beta_scaling_record(n) for n in (24, 32, 40, 48)]
    assert all(record.typical_beta_upper_bound_log2 < 0 for record in records)
    assert not records[0].generic_qsvt_degree_exceeds_polynomial_benchmark
    assert all(
        record.generic_qsvt_degree_exceeds_polynomial_benchmark
        for record in records[1:]
    )
    assert all(
        record.generic_qsvt_degree_lower_bound_log2
        > record.polynomial_degree_ten_benchmark_log2
        for record in records[1:]
    )
    assert records[-1].generic_qsvt_degree_lower_bound_log2 > 150


def test_scaling_record_requires_possible_collision_free_source_event() -> None:
    import pytest

    with pytest.raises(ValueError, match="impossible"):
        typical_point_beta_scaling_record(8)


def test_report_kills_generic_qsvt_but_not_direct_point_transform() -> None:
    report = run_point_effect_qsvt_no_go()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.headline_metrics["superpolynomial_scaling_row_count"] > 0
    assert not report.claim_gate["typical_collective_beta_inverse_polynomial"]
    assert not report.claim_gate["generic_centered_effect_qsvt_polynomial"]
    assert report.claim_gate[
        "generic_centered_effect_qsvt_superpolynomial_proved"
    ]
    assert report.claim_gate[
        "collision_free_conditioning_preserves_beta_upper_bound"
    ]
    assert not report.claim_gate[
        "linear_point_povm_information_theoretically_invalidated"
    ]
    assert not report.claim_gate[
        "direct_representation_specific_point_transform_ruled_out"
    ]
    assert not report.claim_gate["speedup_claim_allowed"]
