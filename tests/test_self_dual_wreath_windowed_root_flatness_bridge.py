import pytest

from self_dual_wreath_coherent_component_trim_hybrid import (
    NATURAL_FINAL_FIBER_ASPECT_LOWER,
)
from self_dual_wreath_windowed_root_flatness_bridge import (
    audit_spectral_window_flatness,
    optimized_window_parameters,
    run_windowed_root_flatness_bridge,
    windowed_root_flatness_scaling_record,
    write_windowed_root_flatness_bridge_report,
)


def test_two_sided_window_bounds_native_state_flatness():
    row = audit_spectral_window_flatness(
        "DIRECT",
        100,
        (1e-8, 0.001, 0.002, 0.01, 0.05, 0.5),
        0.1,
        10.0,
    )
    assert row.retained_eigenvalues == (0.001, 0.002, 0.01, 0.05)
    assert row.exact_window_flatness_bound_verified
    assert row.retained_native_state_flatness <= 100
    assert row.flatness_bound_residual == 0


def test_boundary_spectrum_obeys_condition_number_bound():
    alpha = 0.2
    beta = 12.0
    hidden = 64
    row = audit_spectral_window_flatness(
        "BOUNDARY",
        hidden,
        (alpha / hidden,) * 31 + (beta / hidden,),
        alpha,
        beta,
    )
    assert row.exact_window_flatness_bound_verified
    assert row.window_condition_number_upper_bound == pytest.approx(beta / alpha)
    assert row.retained_native_state_flatness < beta / alpha


def test_optimized_window_balances_low_and_high_tail_budgets():
    hidden = 10_000
    copies = (hidden - 1).bit_length() + 2
    loss = 0.1
    alpha, beta, delta, flatness = optimized_window_parameters(
        hidden, copies, loss
    )
    collision = 1 + (hidden - 1) / (1 << copies)
    assert alpha == pytest.approx(delta / 2)
    assert collision / beta == pytest.approx(delta / 2)
    assert alpha + collision / beta == pytest.approx(delta)
    assert flatness == pytest.approx(64 * collision / loss**4)


@pytest.mark.parametrize("n", (8, 12, 16, 24, 48, 96))
def test_extra_two_copy_schedule_has_constant_success_and_flatness(n):
    row = windowed_root_flatness_scaling_record(n)
    assert row.collision_second_moment_factor <= 1.25
    assert row.discarded_native_mass_upper_bound <= (
        row.target_discarded_native_mass * (1 + 1e-12)
    )
    assert row.retained_root_flatness_upper_bound <= 80 / 0.1**4
    assert row.windowed_pgm_success_lower_bound > 0.7
    assert row.constant_success_and_flatness_proved
    expected_threshold = (
        row.target_component_trim_failure
        * float(NATURAL_FINAL_FIBER_ASPECT_LOWER)
        / (2 * row.retained_root_flatness_upper_bound)
    )
    assert row.final_root_component_threshold == pytest.approx(expected_threshold)
    assert not row.structured_window_projector_compiled
    assert not row.all_level_component_rank_budget_proved


def test_report_resolves_information_theoretic_windowed_flatness_only(tmp_path):
    report = run_windowed_root_flatness_bridge()
    assert report.theorem.theorem_verified
    assert report.theorem.exact_window_flatness_bridge_proved
    assert report.theorem.constant_success_windowed_native_root_flatness_proved
    assert not report.theorem.unwindowed_native_root_flatness_proved
    assert not report.theorem.structured_window_projector_compiled
    assert not report.theorem.recursive_component_trim_compiled
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.headline_metrics["scaling_failure_count"] == 0
    assert report.claim_gate[
        "constant_success_windowed_native_root_flatness_proved"
    ]
    assert not report.claim_gate["structured_window_projector_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_windowed_root_flatness_bridge_report(
        tmp_path / "windowed-root-flatness.json"
    )
    assert payload["status"] == (
        "windowed-root-flatness-proved-structured-window-access-open"
    )


def test_invalid_empty_window_is_rejected():
    with pytest.raises(ValueError, match="retains no"):
        audit_spectral_window_flatness(
            "EMPTY",
            100,
            (1e-8, 100.0),
            0.1,
            10.0,
        )
