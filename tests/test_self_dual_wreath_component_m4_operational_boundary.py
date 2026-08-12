from __future__ import annotations

import math

import pytest

from self_dual_wreath_component_m4_operational_boundary import (
    NATURAL_M4_LIMINF,
    audit_m4_operational_boundary,
    commuting_approximation_error_lower_bound,
    m4_operational_scaling_record,
    run_component_m4_operational_boundary,
    witness_probability_lower_bound,
)


def test_random_walsh_pair_mean_equals_component_m4() -> None:
    control = audit_m4_operational_boundary()

    assert control.exact_operational_boundary_verified
    assert control.normalized_component_m4 == pytest.approx(1 / 16)
    assert control.normalized_walsh_pair_gap_mean == pytest.approx(
        control.normalized_component_m4
    )
    assert control.maximum_normalized_pair_gap <= 2


def test_bounded_mean_forces_constant_random_witness_mass() -> None:
    threshold = NATURAL_M4_LIMINF / 2
    probability = witness_probability_lower_bound(
        NATURAL_M4_LIMINF,
        threshold,
    )

    assert probability == pytest.approx(3 / 253)
    record = m4_operational_scaling_record(4.0)
    assert record.asymptotic_random_pair_witness_probability_lower_bound == pytest.approx(
        3 / 253
    )
    assert record.joint_natural_source_and_mask_witness_guaranteed
    assert not record.sourcewise_witness_guaranteed


def test_positive_m4_excludes_vanishing_commuting_approximation() -> None:
    control = audit_m4_operational_boundary()
    lower = commuting_approximation_error_lower_bound(
        control.normalized_component_m4
    )

    assert lower == pytest.approx(control.normalized_component_m4 / 8)
    assert control.commuting_approximation_normalized_squared_error >= lower
    assert control.commuting_effect_commutator_residual <= 1e-10
    assert commuting_approximation_error_lower_bound(NATURAL_M4_LIMINF) == pytest.approx(
        3 / 512
    )


def test_m4_and_uniform_affine_mask_law_are_covariance_blind() -> None:
    control = audit_m4_operational_boundary()

    assert control.conjugated_relabelled_m4_residual <= 1e-10
    assert control.affine_relabelled_pair_distribution_residual <= 1e-10
    assert control.zero_information_counterensemble_holevo_bits == pytest.approx(0)
    assert control.perfect_information_counterensemble_holevo_bits == pytest.approx(2)
    assert control.same_internal_m4_in_both_counterensembles


def test_report_preserves_algorithmic_claim_gates() -> None:
    report = run_component_m4_operational_boundary()

    assert report.headline_metrics["m4_random_pair_witness_theorem_count"] == 1
    assert report.headline_metrics["commuting_approximation_no_go_theorem_count"] == 1
    assert report.headline_metrics["m4_covariance_blindness_theorem_count"] == 1
    assert report.claim_gate[
        "positive_M4_implies_constant_joint_source_mask_witness_rate"
    ]
    assert report.claim_gate["positive_M4_rules_out_commuting_POVM_approximation"]
    assert not report.claim_gate["M4_scalar_is_hidden_label_sensitive"]
    assert not report.claim_gate["M4_only_transcript_has_hidden_information"]
    assert not report.claim_gate["dependency_support_state_and_reflection_compiled"]
    assert not report.claim_gate["label_sensitive_covariant_decoder_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_witness_bound_rejects_invalid_parameters() -> None:
    with pytest.raises(ValueError):
        witness_probability_lower_bound(0.1, 0.1)
    with pytest.raises(ValueError):
        witness_probability_lower_bound(2.1, 0.1)
    with pytest.raises(ValueError):
        commuting_approximation_error_lower_bound(-1e-3)


def test_natural_scaling_floor_and_trial_count_are_constant() -> None:
    records = [m4_operational_scaling_record(alpha) for alpha in (2.0, 3.0, 4.0)]

    assert min(row.natural_normalized_m4_limit for row in records) == pytest.approx(
        NATURAL_M4_LIMINF
    )
    assert max(row.independent_trials_for_95_percent_witness_probability for row in records) < 300
    assert min(row.commuting_approximation_rms_error_lower_bound for row in records) == pytest.approx(
        math.sqrt(3 / 512)
    )
