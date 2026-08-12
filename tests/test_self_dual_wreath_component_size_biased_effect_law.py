from __future__ import annotations

import pytest

from self_dual_wreath_component_size_biased_effect_law import (
    UNIFORM_EFFECT_EDGE_THRESHOLD,
    audit_effect_trim_m4_stability,
    audit_size_biased_point_mass_control,
    m4_trim_stability_upper_bound,
    run_component_size_biased_effect_law,
    size_biased_effect_scaling_record,
)


@pytest.mark.parametrize("frame_count", [2, 4])
def test_exact_sparse_fusion_controls_have_point_mass_size_biased_law(
    frame_count: int,
) -> None:
    control = audit_size_biased_point_mass_control(frame_count)
    gamma = 1 / frame_count

    assert control.exact_size_biased_point_mass_control_verified
    assert control.coefficient_aspect == pytest.approx(frame_count)
    assert control.positive_effect_eigenvalue == pytest.approx(gamma)
    assert control.size_biased_moments == pytest.approx(
        tuple(gamma**order for order in range(7))
    )
    assert control.maximum_coefficient_projection_word_residual <= 1e-9
    assert control.normalized_low_effect_trace == pytest.approx(0)
    assert control.component_effects_noncommuting


def test_outcome_free_trim_bound_handles_noncommuting_discarded_sector() -> None:
    control = audit_effect_trim_m4_stability()

    assert control.trim_stability_verified
    assert control.discarded_sector_noncommutative
    assert control.normalized_m4_difference <= control.outcome_free_stability_upper_bound
    assert control.retained_minimum_positive_eigenvalue >= control.trim_threshold
    assert control.normalized_trimmed_m4 > 0


def test_trim_stability_bound_has_square_root_trace_scaling() -> None:
    assert m4_trim_stability_upper_bound(0) == 0
    assert m4_trim_stability_upper_bound(1 / 64) == pytest.approx(1)

    with pytest.raises(ValueError):
        m4_trim_stability_upper_bound(-1e-3)
    with pytest.raises(ValueError):
        m4_trim_stability_upper_bound(1.01)


def test_natural_scaling_keeps_uniform_constant_edge_below_one_quarter() -> None:
    rows = [size_biased_effect_scaling_record(alpha) for alpha in (2.0, 3.0, 4.0)]

    assert UNIFORM_EFFECT_EDGE_THRESHOLD < 1 / 4
    assert all(row.fixed_threshold_discarded_trace_vanishes for row in rows)
    assert all(row.inverse_polynomial_threshold_discarded_trace_vanishes for row in rows)
    assert all(row.trimmed_component_m4_limit >= 3 / 64 for row in rows)
    assert all(not row.uniform_minimum_nonzero_effect_eigenvalue_proved for row in rows)
    assert all(not row.coherent_effect_block_encoding_proved for row in rows)


def test_report_closes_spectral_signal_gate_but_not_access_or_decoder() -> None:
    report = run_component_size_biased_effect_law()

    assert report.headline_metrics[
        "all_fixed_size_biased_effect_moment_theorem_count"
    ] == 1
    assert report.headline_metrics[
        "natural_trace_weighted_effect_edge_theorem_count"
    ] == 1
    assert report.headline_metrics[
        "constant_edge_trimmed_positive_m4_theorem_count"
    ] == 1
    assert report.claim_gate["natural_size_biased_effect_law_proved"]
    assert report.claim_gate["positive_natural_M4_survives_constant_effect_trim"]
    assert not report.claim_gate["tiny_effect_eigenvalues_explain_natural_M4"]
    assert not report.claim_gate["uniform_minimum_nonzero_effect_eigenvalue_proved"]
    assert not report.claim_gate["coherent_component_effect_block_encoding_proved"]
    assert not report.claim_gate["component_povm_dilation_compiled"]
    assert not report.claim_gate["decoder_information_gain_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
