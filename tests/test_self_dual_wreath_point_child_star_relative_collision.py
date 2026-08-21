import math

import numpy as np

from self_dual_wreath_point_child_star_relative_collision import (
    audit_point_child_star_relative_collision,
    build_point_child_star_relative_collision_report,
    point_child_star_relative_collision_scaling_record,
    relative_collision,
)


THRESHOLD_LABELS = (
    ((3,), (2, 1)),
    ((3,), (1, 1, 1)),
    ((2, 1), (1, 1, 1)),
)


def test_relative_collision_is_positive_and_predicts_point_pgm_success():
    control = audit_point_child_star_relative_collision(
        3,
        THRESHOLD_LABELS,
        control_id="TEST-W3",
    )
    assert control.exact_child_star_relative_collision_verified
    assert control.direct_relative_collision > 0
    assert math.isclose(
        control.direct_pgm_success,
        1 / 3 + control.direct_relative_collision / 3,
        abs_tol=1e-9,
    )


def test_child_and_parent_pair_channels_sum_to_direct_relative_collision():
    control = audit_point_child_star_relative_collision(
        3,
        THRESHOLD_LABELS,
        control_id="TEST-W3-DECOMPOSE",
    )
    assert control.relative_collision_decomposition_residual < 1e-8
    assert math.isclose(
        control.decomposed_relative_collision,
        control.parent_diagonal_relative_collision
        + control.parent_offdiagonal_relative_collision,
        abs_tol=1e-8,
    )
    assert any(
        row.active_offdiagonal_parent_pair_count > 0
        for row in control.child_records
    )


def test_common_density_rescaling_cancels_from_every_child_effect():
    control = audit_point_child_star_relative_collision(
        3,
        THRESHOLD_LABELS,
        control_id="TEST-W3-SCALE",
    )
    assert control.maximum_rescaled_effect_cancellation_residual < 1e-8


def test_relative_collision_handles_rank_deficient_average_support():
    average = np.diag([0.6, 0.4, 0.0])
    centered = np.diag([0.1, -0.1, 0.0])
    observed = relative_collision(average, centered)
    expected = 0.1**2 / 0.6 + 0.1**2 / 0.4
    assert math.isclose(observed, expected)


def test_scaling_and_report_keep_natural_asymptotic_gates_false():
    scaling = point_child_star_relative_collision_scaling_record(128)
    report = build_point_child_star_relative_collision_report()
    assert scaling.exact_positive_relative_channel_formula_available
    assert scaling.common_density_normalization_cancels_from_pgm_effect
    assert not scaling.natural_critical_relative_collision_lower_bound_proved
    assert report.theorem.theorem_verified
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["common_density_scalar_cancels_from_pgm_effect"]
    assert not report.claim_gate[
        "natural_critical_relative_collision_lower_bound_proved"
    ]
    assert not report.claim_gate["critical_harmonic_point_measurement_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]
