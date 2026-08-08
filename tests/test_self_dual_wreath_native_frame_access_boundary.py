import math

from self_dual_wreath_native_frame_access_boundary import (
    audit_native_frame_access,
    native_frame_access_scaling_record,
    run_native_frame_access_boundary,
    water_filling_profile,
)


def test_water_filling_exact_cost_is_maximum_amplitude_ratio() -> None:
    source = (math.sqrt(0.8), math.sqrt(0.2))
    target = (math.sqrt(0.5), math.sqrt(0.5))
    profile = water_filling_profile(source, target, 1.0)
    expected = max(t / s for s, t in zip(source, target))
    assert math.isclose(profile.qrs_query_factor, expected, rel_tol=1e-10)
    assert math.isclose(profile.achieved_fidelity, 1.0, abs_tol=1e-10)


def test_water_filling_bounded_fidelity_interpolates() -> None:
    source = (math.sqrt(0.95), math.sqrt(0.05))
    target = (math.sqrt(0.5), math.sqrt(0.5))
    direct = sum(s * t for s, t in zip(source, target)) ** 2
    requested = (1 + direct) / 2
    profile = water_filling_profile(source, target, requested)
    assert profile.direct_source_target_fidelity < requested < 1
    assert math.isclose(profile.achieved_fidelity, requested, abs_tol=1e-10)
    assert 1 < profile.qrs_query_factor < max(
        t / s for s, t in zip(source, target)
    )


def test_flat_frame_survives_truncation_but_costs_sqrt_width() -> None:
    row = audit_native_frame_access(
        "TEST-FLAT",
        (1.0,) * 12,
        256,
        0.5,
    )
    assert row.retained_native_frame_mass == 1
    assert row.flat_retained_spectrum
    assert row.flat_frame_black_box_sqrt_width_boundary_verified
    assert math.isclose(row.initial_good_component_amplification_factor, 16)
    assert math.isclose(row.exact_qrs_query_factor, 16)
    assert math.isclose(row.variable_time_l2_inverse_singular_scale, 16)
    assert math.isclose(row.water_filling.qrs_query_factor, 1)


def test_low_mode_truncation_does_not_remove_width_normalization() -> None:
    row = audit_native_frame_access(
        "TEST-SKEW",
        (1e-10, 0.25, 0.5, 1.0, 2.0),
        1024,
        0.1,
    )
    assert row.retained_rank == 4
    assert row.retained_native_frame_mass > 0.999999999
    assert row.normalized_analysis_minimum_singular_value < 0.02
    assert row.initial_good_component_amplification_factor > 10
    assert row.variable_time_identity_residual < 1e-10


def test_factorial_width_eventually_beats_polynomial_benchmark() -> None:
    row = native_frame_access_scaling_record(48)
    assert row.black_box_access_superpolynomial
    assert row.flat_frame_qrs_lower_bound_log2 > row.polynomial_query_benchmark_log2
    assert not row.trace_weighted_truncation_changes_flat_control
    assert row.representation_specific_direct_transform_required


def test_report_redirects_access_search_without_claiming_hardness() -> None:
    report = run_native_frame_access_boundary()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["explicit_orr_water_filling_vectors_derived"]
    assert report.claim_gate[
        "flat_frame_normalized_access_sqrt_width_lower_bound_proved"
    ]
    assert not report.claim_gate["variable_time_generic_width_bypass_available"]
    assert not report.claim_gate[
        "trace_weighted_truncation_suffices_for_generic_qsvt"
    ]
    assert not report.claim_gate["representation_specific_direct_polar_ruled_out"]
    assert not report.claim_gate["speedup_claim_allowed"]
