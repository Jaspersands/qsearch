from __future__ import annotations

import pytest

from self_dual_wreath_component_trimmed_support_scalarization import (
    _two_frame_weighted_povm,
    audit_trimmed_support_scalarization,
    run_component_trimmed_support_scalarization,
    support_rank_error_bound,
    support_scalarization_bounds,
    support_scalarization_scaling_record,
)


@pytest.mark.parametrize("weight", [0.5, 0.55, 0.6])
def test_trimmed_effect_and_square_root_scalarization_bounds(weight: float) -> None:
    control = audit_trimmed_support_scalarization(
        f"WEIGHT-{weight}",
        _two_frame_weighted_povm(weight),
        0.5,
        0.2,
    )

    assert control.scalarization_bounds_verified
    assert control.normalized_effect_support_scalar_error <= control.effect_error_upper_bound
    assert control.normalized_square_root_support_scalar_error <= control.square_root_error_upper_bound
    assert control.normalized_support_rank_error <= control.support_rank_error_upper_bound
    assert control.maximum_effect_commutator_norm > 0


def test_exact_balanced_fusion_frame_needs_no_matrix_amplitude() -> None:
    control = audit_trimmed_support_scalarization(
        "BALANCED",
        _two_frame_weighted_povm(0.5),
        0.5,
        0.2,
    )

    assert control.normalized_size_biased_variance == pytest.approx(0)
    assert control.normalized_effect_support_scalar_error == pytest.approx(0)
    assert control.normalized_square_root_support_scalar_error == pytest.approx(0)
    assert control.normalized_aggregate_retained_support_rank == pytest.approx(2)


def test_scalarization_bounds_reject_invalid_spectral_parameters() -> None:
    with pytest.raises(ValueError):
        support_scalarization_bounds(-1e-4, 0.5, 0.2)
    with pytest.raises(ValueError):
        support_scalarization_bounds(0.1, 0.2, 0.2)
    with pytest.raises(ValueError):
        support_rank_error_bound(0.1, 1.2, 0.2)


def test_scaling_relocates_compiler_gate_to_support_select() -> None:
    record = support_scalarization_scaling_record(4.0, 1e-4)

    assert record.aggregate_support_rank_to_fiber_target == pytest.approx(4)
    assert not record.matrix_square_root_amplitude_required_asymptotically
    assert not record.coherent_support_projector_select_proved
    assert not record.uniform_partial_isometry_transport_proved


def test_report_preserves_average_only_and_algorithmic_claim_gates() -> None:
    report = run_component_trimmed_support_scalarization()

    assert report.headline_metrics[
        "trimmed_effect_support_scalarization_theorem_count"
    ] == 1
    assert report.headline_metrics[
        "trimmed_square_root_dilation_scalarization_theorem_count"
    ] == 1
    assert report.headline_metrics[
        "aggregate_retained_support_rank_theorem_count"
    ] == 1
    assert report.claim_gate["natural_trimmed_effects_support_scalar_in_aggregate"]
    assert not report.claim_gate["generic_matrix_square_root_amplitudes_are_final_root_bottleneck"]
    assert not report.claim_gate["operator_norm_support_scalarization_proved"]
    assert not report.claim_gate["sourcewise_support_scalarization_proved"]
    assert not report.claim_gate["coherent_support_projector_select_proved"]
    assert not report.claim_gate["uniform_gpe_support_transport_proved"]
    assert not report.claim_gate["component_povm_dilation_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]
