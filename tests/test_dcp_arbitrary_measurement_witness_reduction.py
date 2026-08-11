import numpy as np
import pytest

from dcp_arbitrary_measurement_witness_reduction import (
    arbitrary_measurement_scaling_record,
    arbitrary_measurement_witness_theorem,
    audit_arbitrary_measurement_reduction,
    covariant_correlation_seed,
    random_exact_povm,
    run_arbitrary_measurement_witness_reduction,
)


COUNTS = (2, 0, 1, 3, 0, 2, 1, 1)
SUPPORT = tuple(index for index, count in enumerate(COUNTS) if count)


def test_higher_rank_covariant_measurement_yields_average_fiber_filter() -> None:
    phases = np.exp(0.17j * (np.arange(len(SUPPORT)) + 1) ** 2)
    seed = covariant_correlation_seed(
        len(COUNTS),
        len(SUPPORT),
        mixing=0.65,
        phases=phases,
    )
    control = audit_arbitrary_measurement_reduction(
        "HIGHER-RANK",
        COUNTS,
        source_measurement_kind="higher-rank-covariant",
        covariant_seed=seed,
    )
    assert control.higher_rank_effect_verified
    assert not control.initially_noncovariant_measurement
    assert control.qft_diagonal_filter_residual <= 1e-10
    assert control.inverse_filter_residual <= 1e-10
    assert (
        control.uniform_legal_average_target_preparation_probability
        + 1e-10
        >= control.source_measurement_average_success
    )
    assert (
        control.planted_average_target_preparation_probability
        + 1e-10
        >= control.legal_support_to_assignment_ratio
        * control.uniform_legal_average_target_preparation_probability
    )
    assert control.exact_arbitrary_measurement_reduction_verified


def test_random_noncovariant_povm_symmetrizes_without_average_loss() -> None:
    original = random_exact_povm(
        len(COUNTS),
        len(SUPPORT),
        seed=313,
    )
    control = audit_arbitrary_measurement_reduction(
        "NONCOVARIANT",
        COUNTS,
        source_measurement_kind="random-noncovariant",
        original_effects=original,
    )
    assert control.initially_noncovariant_measurement
    assert control.higher_rank_effect_verified
    assert control.source_to_symmetrized_success_residual <= 1e-10
    assert control.symmetrized_success_spread <= 1e-10
    assert control.symmetrized_covariance_residual <= 1e-10
    assert control.exact_arbitrary_measurement_reduction_verified


def test_target_filter_is_a_valid_contraction_even_when_nonuniform() -> None:
    phases = np.exp(0.31j * np.arange(len(SUPPORT)))
    seed = covariant_correlation_seed(
        len(COUNTS),
        len(SUPPORT),
        mixing=0.41,
        phases=phases,
    )
    control = audit_arbitrary_measurement_reduction(
        "NONUNIFORM-FILTER",
        COUNTS,
        source_measurement_kind="nonuniform-higher-rank",
        covariant_seed=seed,
    )
    assert 0 <= control.minimum_target_preparation_probability <= 1
    assert 0 <= control.maximum_target_preparation_probability <= 1 + 1e-10
    assert control.cleaned_subanalysis_contraction_residual <= 1e-10
    assert control.decoding_success_to_filter_mass_residual <= 1e-10
    assert control.planted_average_dominates_scaled_legal_residual <= 1e-10


def test_invalid_covariant_seed_diagonal_fails_completeness() -> None:
    invalid = np.eye(len(SUPPORT)) / (len(COUNTS) + 1)
    control = audit_arbitrary_measurement_reduction(
        "INVALID",
        COUNTS,
        source_measurement_kind="invalid-seed",
        covariant_seed=invalid,
    )
    assert not control.exact_arbitrary_measurement_reduction_verified
    assert control.symmetrized_effect_completeness_residual > 1e-3


def test_inverse_polynomial_measurement_bootstrap_is_polynomial() -> None:
    for power in (0, 2, 4, 8):
        row = arbitrary_measurement_scaling_record(256, power, 8)
        assert row.polynomial_bootstrap
        assert row.one_shot_uniform_legal_witness_success_lower_bound == pytest.approx(
            256.0 ** (-power)
        )
        assert row.actual_circuit_povm_semantics_exact
        assert row.inverse_polynomial_wrapper_precision_sufficient
        assert row.robust_average_witness_success_lower_bound == pytest.approx(
            0.75 * row.decoding_success_lower_bound
        )
        assert not row.per_target_bounded_error_proved


def test_theorem_scope_keeps_approximation_and_per_target_guarantees_open() -> None:
    theorem = arbitrary_measurement_witness_theorem()
    assert theorem.arbitrary_effect_rank
    assert theorem.initially_noncovariant_measurements
    assert not theorem.pgm_structure_used
    assert theorem.accessible_exact_measurement_route_reduced
    assert theorem.average_planted_inversion_route_reduced
    assert not theorem.approximation_to_ideal_povm_is_loophole
    assert theorem.standard_wrapper_gate_synthesis_robust
    assert not theorem.per_target_bounded_error_proved
    assert not theorem.inaccessible_noisy_channel_reduced


def test_report_closes_exact_measurement_architecture_shortcuts() -> None:
    report = run_arbitrary_measurement_witness_reduction()
    assert report.headline_metrics[
        "arbitrary_exact_measurement_to_witness_theorem_count"
    ] == 1
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.headline_metrics["higher_rank_control_count"] == 4
    assert report.headline_metrics["initially_noncovariant_control_count"] == 2
    assert not report.claim_gate[
        "accessible_exact_higher_rank_measurement_shortcut_open"
    ]
    assert not report.claim_gate[
        "accessible_exact_noncovariant_measurement_shortcut_open"
    ]
    assert not report.claim_gate[
        "approximation_to_ideal_standard_circuit_measurement_is_loophole"
    ]
    assert report.claim_gate["standard_wrapper_gate_synthesis_robust"]
    assert not report.claim_gate["inaccessible_noisy_channel_route_closed"]
    assert not report.claim_gate["speedup_claim_allowed"]
