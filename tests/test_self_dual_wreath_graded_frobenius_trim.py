import numpy as np
import pytest

from self_dual_wreath_graded_frobenius_trim import (
    audit_grading_compatible_trim,
    graded_frobenius_trim_scaling_record,
    graded_trim_bounds,
    run_graded_frobenius_trim,
)


def test_exact_endpoint_bounds_at_quarter_tolerance() -> None:
    bounds = graded_trim_bounds(0.25)

    assert bounds["metric_lower"] == pytest.approx(12 / 7)
    assert bounds["defect_upper"] < 0.25
    assert bounds["endpoint_gap_lower"] > 0.375


def test_pinched_trim_preserves_grading_and_satisfies_schur_bounds() -> None:
    dimension = 24
    rng = np.random.default_rng(17)
    first = rng.normal(size=(dimension, 3))
    second = rng.normal(size=(dimension, 4))
    metric = 0.16 * (first @ first.T) / dimension
    graded = 0.14 * (second @ second.T) / dimension
    metric -= np.diag(np.diag(metric))
    graded -= np.diag(np.diag(graded))

    record = audit_grading_compatible_trim(
        "PINCHED", metric, graded, 8, 7
    )

    assert record.grading_compatible_trim_verified
    assert record.trim_commutes_with_internal_crossing_grading
    assert record.compressed_metric_perturbation_norm <= 0.25 + 1e-9
    assert record.compressed_graded_perturbation_norm <= 0.25 + 1e-9
    assert record.observed_endpoint_gap >= (
        record.theoretical_endpoint_gap_lower_bound - 1e-9
    )


def test_natural_scaling_gives_vanishing_loss_and_constant_gap() -> None:
    early = graded_frobenius_trim_scaling_record(32)
    late = graded_frobenius_trim_scaling_record(48)

    assert not early.constant_endpoint_gap_after_trim_certified
    assert late.constant_endpoint_gap_after_trim_certified
    assert late.grading_compatible_removed_fraction_upper_bound < 1e-20
    assert late.theoretical_endpoint_gap_lower_bound > 0.375
    assert not late.coherent_pinched_energy_projector_known
    assert late.coefficient_to_pgm_state_mass_transfer_proved
    assert not late.pair_relations_exhaust_full_synthesis_cokernel_proved


def test_report_resolves_state_transfer_but_keeps_circuit_and_h0_blocked() -> None:
    report = run_graded_frobenius_trim()

    assert report.claim_gate["grading_compatible_frobenius_trim_exists"]
    assert report.claim_gate[
        "constant_endpoint_gap_after_vanishing_coefficient_trim_proved"
    ]
    assert not report.claim_gate["coherent_pinched_energy_projector_proved"]
    assert report.claim_gate[
        "coefficient_loss_transfers_to_pgm_state_loss_proved"
    ]
    assert report.claim_gate["relation_trim_zero_pgm_state_loss_proved"]
    assert not report.claim_gate[
        "pair_relations_exhaust_full_synthesis_cokernel_proved"
    ]
    assert report.claim_gate["pair_relations_asymptotically_incomplete_proved"]
    assert report.claim_gate["hierarchical_span_cokernel_completion_proved"]
    assert not report.claim_gate[
        "graded_endpoint_gap_for_hierarchical_span_relations_proved"
    ]
    assert not report.claim_gate["polynomial_hierarchical_polar_sampler_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
