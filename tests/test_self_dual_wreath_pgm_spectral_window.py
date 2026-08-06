import math

import pytest

from self_dual_wreath_pgm_spectral_window import (
    audit_physical_spectral_window,
    run_pgm_spectral_window,
    spectral_window_scaling_record,
    window_discarded_mass_upper_bound,
    windowed_pgm_success_lower_bound,
)


THREE_UNEQUAL_TYPES = (
    ((3,), (2, 1)),
    ((3,), (1, 1, 1)),
    ((2, 1), (1, 1, 1)),
)


def test_window_mass_bound_combines_rank_and_second_moment() -> None:
    hidden_count = math.factorial(16)
    copies = math.ceil(math.log2(hidden_count))
    bound = window_discarded_mass_upper_bound(
        hidden_count,
        copies,
        1e-4,
        400,
    )

    assert bound < 0.0051
    assert windowed_pgm_success_lower_bound(
        hidden_count,
        copies,
        1e-4,
        400,
    ) > 0.35


def test_physical_window_effects_are_valid() -> None:
    record = audit_physical_spectral_window(
        "test",
        THREE_UNEQUAL_TYPES,
    )

    assert record.exact_spectral_window_validation
    assert record.observed_discarded_average_mass <= record.total_discarded_mass_upper_bound + 1e-10
    assert record.windowed_pgm_success_probability >= record.gentle_window_success_lower_bound - 1e-10
    assert record.maximum_effect_completeness_violation < 1e-9


def test_tail_window_has_constant_rescaled_condition_number() -> None:
    record = spectral_window_scaling_record(512)

    assert record.retained_condition_number_upper_bound == pytest.approx(4_000_000)
    assert record.windowed_pgm_success_lower_bound > 0.35
    assert record.constant_condition_and_success_certified
    assert record.raw_lower_cutoff_log2 < -3880
    assert not record.structured_window_projector_circuit_proved


def test_report_closes_conditioning_not_measurement() -> None:
    report = run_pgm_spectral_window()

    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["constant_condition_constant_success_subspace_proved"]
    assert not report.claim_gate[
        "minimum_eigenvalue_or_growing_condition_number_is_core_barrier"
    ]
    assert not report.claim_gate["structured_window_projector_circuit_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_invalid_window_is_rejected() -> None:
    with pytest.raises(ValueError, match="0<alpha<beta"):
        window_discarded_mass_upper_bound(8, 3, 2, 1)
