from __future__ import annotations

import pytest

from self_dual_wreath_final_root_scalar_mixer_no_go import (
    UNIFORM_CANONICAL_NATIVE_ERROR_FLOOR,
    UNIFORM_EFFECT_MSE_FLOOR,
    UNIFORM_WINDOW_ONLY_NATIVE_ERROR_FLOOR,
    audit_polar_only_indistinguishability,
    audit_scalar_endpoint_control,
    noncommuting_metric_control,
    run_final_root_scalar_mixer_no_go,
    scalar_mixer_moment_record,
    symmetric_free_moment_control,
    write_final_root_scalar_mixer_no_go_report,
)


@pytest.mark.parametrize("alpha", [2.0, 2.5, 3.0, 4.0])
def test_free_jacobi_variance_and_uniform_floors(alpha: float) -> None:
    row = scalar_mixer_moment_record(alpha)

    assert row.free_jacobi_mean == 0.5
    assert row.free_jacobi_variance == pytest.approx(1 / (8 * alpha))
    assert row.free_jacobi_second_moment == pytest.approx(
        0.25 + 1 / (8 * alpha)
    )
    assert row.scalar_effect_mean_square_error >= UNIFORM_EFFECT_MSE_FLOOR
    assert row.canonical_native_error_lower_bound >= (
        UNIFORM_CANONICAL_NATIVE_ERROR_FLOOR
    )
    assert row.window_only_native_error_lower_bound >= (
        UNIFORM_WINDOW_ONLY_NATIVE_ERROR_FLOOR
    )


def test_hadamard_uniquely_minimizes_scalar_effect_error() -> None:
    optimum = scalar_mixer_moment_record(3.0, 0.5)
    left = scalar_mixer_moment_record(3.0, 0.2)
    right = scalar_mixer_moment_record(3.0, 0.8)

    assert left.scalar_effect_mean_square_error == pytest.approx(
        right.scalar_effect_mean_square_error
    )
    assert left.scalar_effect_mean_square_error > (
        optimum.scalar_effect_mean_square_error
    )
    improvement = (
        left.scalar_effect_mean_square_error
        - optimum.scalar_effect_mean_square_error
    )
    assert improvement == pytest.approx(0.3**2)


@pytest.mark.parametrize("alpha,t", [(2.0, 0.5), (3.0, 0.25), (4.0, 0.8)])
def test_symmetric_controls_match_theoretical_effect_moments(
    alpha: float,
    t: float,
) -> None:
    control = symmetric_free_moment_control(alpha, t)
    moment = scalar_mixer_moment_record(alpha, t)

    assert control.exact_endpoint_identities_verified
    assert control.scalar_effect_lower_bound_verified
    assert control.positive_phase_alignment_verified
    assert control.gpe_transport_invariance_verified
    assert control.relative_effect_mean == pytest.approx(moment.free_jacobi_mean)
    assert control.relative_effect_variance == pytest.approx(
        moment.free_jacobi_variance
    )
    assert control.scalar_effect_mean_square_error == pytest.approx(
        moment.scalar_effect_mean_square_error
    )


def test_noncommuting_metrics_obey_endpoint_and_transport_identities() -> None:
    left, right = noncommuting_metric_control()
    control = audit_scalar_endpoint_control("noncommuting", left, right, 0.5)

    assert control.exact_endpoint_identities_verified
    assert control.scalar_effect_lower_bound_verified
    assert control.native_canonical_mean_square_error >= (
        control.native_window_effect_lower_bound
    )
    assert control.phase_perturbed_native_error >= (
        control.native_canonical_mean_square_error
    )
    assert control.transported_native_error == pytest.approx(
        control.native_canonical_mean_square_error
    )


def test_invalid_parameters_are_rejected() -> None:
    with pytest.raises(ValueError):
        scalar_mixer_moment_record(1.9)
    with pytest.raises(ValueError):
        scalar_mixer_moment_record(4.1)
    with pytest.raises(ValueError):
        scalar_mixer_moment_record(2.0, -0.1)
    left, right = noncommuting_metric_control()
    with pytest.raises(ValueError):
        audit_scalar_endpoint_control("bad-weight", left, right, 1.1)
    with pytest.raises(ValueError):
        audit_polar_only_indistinguishability(1.0)


def test_child_polars_and_supports_do_not_determine_endpoint_metric() -> None:
    control = audit_polar_only_indistinguishability(3.0)

    assert control.identical_polar_oracles_verified
    assert control.distinct_endpoint_effects_verified
    assert control.constant_oracle_indistinguishability_gap_verified
    assert control.endpoint_effect_distance == pytest.approx(0.25)
    assert control.endpoint_isometry_mean_square_distance > 0.06
    assert control.common_output_worst_case_mean_square_lower_bound > 0.015
    assert control.transported_distance_residual < 1e-12


def test_report_closes_scalar_shortcut_but_keeps_matrix_access_open() -> None:
    report = run_final_root_scalar_mixer_no_go()

    assert report.theorem.theorem_verified
    assert report.headline_metrics["exact_control_failure_count"] == 0
    assert report.claim_gate[
        "natural_final_root_relative_effect_second_moment_proved"
    ]
    assert report.claim_gate["hadamard_is_optimal_deterministic_scalar_endpoint"]
    assert report.claim_gate[
        "every_deterministic_scalar_endpoint_has_constant_native_error"
    ]
    assert not report.claim_gate[
        "pair_gpe_transport_removes_matrix_endpoint_mixer"
    ]
    assert not report.claim_gate[
        "child_polar_and_support_oracles_determine_endpoint_metric"
    ]
    assert report.claim_gate["coherent_metric_magnitude_access_is_necessary"]
    assert report.claim_gate[
        "final_root_matrix_endpoint_is_well_conditioned_after_native_trim"
    ]
    assert not report.claim_gate["structured_matrix_endpoint_effect_access_proved"]
    assert not report.claim_gate["source_adaptive_scalar_endpoint_no_go_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_writer_emits_artifact_without_registry_mutation(tmp_path) -> None:
    path = tmp_path / "scalar-mixer.json"
    payload = write_final_root_scalar_mixer_no_go_report(
        path,
        write_registry=False,
    )

    assert path.exists()
    assert payload["theorem"]["theorem_verified"]
    assert payload["headline_metrics"]["exact_control_failure_count"] == 0
