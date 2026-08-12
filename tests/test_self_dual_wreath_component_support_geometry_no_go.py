from __future__ import annotations

import pytest

from self_dual_wreath_component_size_biased_effect_law import (
    _fusion_frame_system,
)
from self_dual_wreath_component_support_geometry_no_go import (
    _coordinate_pvm_approximants,
    audit_commuting_classifier_bound,
    audit_support_curl_transfer,
    run_component_support_geometry_no_go,
    scalarization_commutator_constant,
    support_geometry_scaling_record,
    trimmed_effects_and_supports,
)
from self_dual_wreath_component_trimmed_support_scalarization import (
    _two_frame_weighted_povm,
)


@pytest.mark.parametrize("frame_count,gamma", [(2, 0.5), (4, 0.25)])
def test_exact_fusion_frames_transfer_m4_to_supports(
    frame_count: int,
    gamma: float,
) -> None:
    effects, _ = _fusion_frame_system(frame_count)
    control = audit_support_curl_transfer(
        f"FRAME-{frame_count}",
        effects,
        gamma,
        0.2,
    )

    assert control.transfer_bound_verified
    assert control.normalized_scalarization_error == pytest.approx(0)
    assert control.normalized_trimmed_effect_m4 == pytest.approx(
        control.normalized_rescaled_support_m4
    )


def test_perturbed_effect_amplitudes_obey_commutator_transfer_bound() -> None:
    control = audit_support_curl_transfer(
        "PERTURBED",
        _two_frame_weighted_povm(0.55),
        0.5,
        0.2,
    )

    assert control.normalized_scalarization_error > 0
    assert control.square_root_m4_transfer_residual <= (
        control.square_root_m4_transfer_upper_bound
    )
    assert control.transfer_bound_verified


def test_retained_supports_have_exact_threshold_bessel_bound() -> None:
    effects, _ = _fusion_frame_system(4)
    control = audit_support_curl_transfer("BESSEL", effects, 0.25, 0.2)

    assert control.support_frame_bessel_norm == pytest.approx(4)
    assert control.support_frame_bessel_norm <= control.support_frame_bessel_upper_bound
    assert control.normalized_support_projector_m4 <= control.support_m4_upper_bound


def test_commuting_coordinate_classifier_has_nonzero_error_floor() -> None:
    effects, _ = _fusion_frame_system(2)
    _, supports = trimmed_effects_and_supports(effects, 0.2)
    control = audit_commuting_classifier_bound(
        "COORDINATE-PVM",
        supports,
        _coordinate_pvm_approximants(len(supports), 4),
        0.2,
    )

    assert control.approximants_pairwise_commute
    assert control.support_projector_m4_per_dimension > 0
    assert control.commuting_error_lower_bound > 0
    assert control.normalized_support_approximation_error >= (
        control.commuting_error_lower_bound
    )
    assert control.commuting_classifier_inequality_verified


def test_natural_support_limit_and_uniform_classifier_floor() -> None:
    row = support_geometry_scaling_record(2.0)

    assert row.natural_effect_m4_limit == pytest.approx(1 / 8)
    assert row.natural_support_projector_m4_limit == pytest.approx(2)
    assert row.bounded_commuting_classifier_error_lower_bound == pytest.approx(1 / 20)
    assert row.pvm_transcript_classifier_error_lower_bound == pytest.approx(1 / 12)
    assert not row.commuting_label_predicate_sufficient


def test_invalid_scalarization_parameters_are_rejected() -> None:
    with pytest.raises(ValueError):
        scalarization_commutator_constant(0.2, 0.2)
    with pytest.raises(ValueError):
        support_geometry_scaling_record(1.9)


def test_report_preserves_coherent_gpe_and_decoder_boundaries() -> None:
    report = run_component_support_geometry_no_go()

    assert report.headline_metrics["natural_support_m4_limit_theorem_count"] == 1
    assert report.headline_metrics["commuting_classifier_no_go_theorem_count"] == 1
    assert report.headline_metrics["uniform_support_m4_lower_bound"] == pytest.approx(2)
    assert report.headline_metrics[
        "uniform_bounded_commuting_classifier_error_floor"
    ] == pytest.approx(1 / 20)
    assert report.claim_gate["commuting_bounded_support_classifier_rejected"]
    assert not report.claim_gate["all_gpe_based_support_classifiers_rejected"]
    assert not report.claim_gate["coherent_recoupling_support_classifier_proved"]
    assert not report.claim_gate["hidden_label_information_gain_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
