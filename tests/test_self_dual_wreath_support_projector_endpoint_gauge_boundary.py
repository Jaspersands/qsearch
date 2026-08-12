from __future__ import annotations

import math

import numpy as np
import pytest

from self_dual_wreath_support_projector_endpoint_gauge_boundary import (
    audit_endpoint_gauge_ambiguity,
    audit_endpoint_polar,
    endpoint_gauge_scaling_record,
    run_support_projector_endpoint_gauge_boundary,
    same_range_conditioning_counterexample,
)


def test_same_support_projector_can_induce_distinct_input_povms() -> None:
    identity = np.eye(2, dtype=complex)
    hadamard = np.asarray([[1.0, 1.0], [1.0, -1.0]], dtype=complex) / math.sqrt(2)
    control = audit_endpoint_gauge_ambiguity(
        "Z-X",
        identity,
        hadamard,
        ((0,), (1,)),
        np.asarray([1.0, 0.0], dtype=complex),
    )

    assert control.common_range_projector_residual == pytest.approx(0, abs=1e-12)
    assert control.witness_outcome_total_variation_distance == pytest.approx(0.5)
    assert control.range_projector_transcript_total_variation_distance == 0
    assert control.fixed_compiler_worst_case_isometry_error_lower_bound == pytest.approx(1)
    assert control.exact_same_range_different_povm_verified


def test_boundary_polar_fixes_range_and_coordinate_effects() -> None:
    boundary = np.asarray(
        [[1.0, 0.0], [0.0, 0.6], [0.4, 0.0], [0.0, 0.8]],
        dtype=complex,
    )
    control = audit_endpoint_polar(
        "RECTANGULAR",
        boundary,
        ((0, 1), (2, 3)),
    )

    assert control.exact_endpoint_polar_verified
    assert control.polar_isometry_residual < 1e-12
    assert control.polar_range_projector_residual < 1e-12
    assert control.coordinate_effect_sum_residual < 1e-12


@pytest.mark.parametrize("exponent", [4, 12, 24])
def test_same_range_does_not_control_endpoint_singular_gap(exponent: int) -> None:
    row = same_range_conditioning_counterexample(exponent)

    assert row.common_range_projector_residual == pytest.approx(0)
    assert row.ill_conditioned_minimum_singular_value == pytest.approx(2.0**-exponent)
    assert row.ill_conditioned_inverse_gap == pytest.approx(2.0**exponent)
    assert not row.support_projector_reveals_conditioning


def test_invalid_block_encoding_normalization_is_rejected() -> None:
    with pytest.raises(ValueError):
        audit_endpoint_polar(
            "BAD-BETA",
            np.eye(2, dtype=complex),
            ((0,), (1,)),
            block_encoding_normalization=0.5,
        )


def test_natural_scaling_keeps_endpoint_access_open() -> None:
    row = endpoint_gauge_scaling_record(64)

    assert not row.generic_normalized_endpoint_access_polynomial
    assert not row.sheaf_support_reflection_removes_endpoint_gauge
    assert not row.tightly_normalized_representation_endpoint_map_proved
    assert not row.direct_global_orientation_polar_proved


def test_report_preserves_support_and_algorithmic_claim_gates() -> None:
    report = run_support_projector_endpoint_gauge_boundary()

    assert report.headline_metrics["support_endpoint_gauge_no_go_theorem_count"] == 1
    assert report.headline_metrics["endpoint_polar_normal_form_theorem_count"] == 1
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert not report.claim_gate["support_projector_alone_sufficient_for_physical_povm"]
    assert report.claim_gate["endpoint_polar_is_sufficient_given_boundary_access_and_gap"]
    assert not report.claim_gate["tightly_normalized_natural_boundary_access_proved"]
    assert not report.claim_gate["partial_sheaf_to_physical_endpoint_compiled"]
    assert not report.claim_gate["hidden_label_decoder_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
