import numpy as np
import pytest

from dcp_covariant_rank_one_measurement_reduction import (
    audit_covariant_rank_one_measurement,
    bootstrap_scaling_record,
    covariant_rank_one_analysis_matrix,
    covariant_rank_one_reduction_theorem,
    run_covariant_rank_one_measurement_reduction,
)


def _law_and_support() -> tuple[tuple[int, ...], tuple[int, ...]]:
    counts = (2, 0, 1, 3, 0, 2, 1, 1)
    support = tuple(index for index, count in enumerate(counts) if count)
    return counts, support


def test_covariant_completeness_forces_equal_modulus_phase_columns() -> None:
    _, support = _law_and_support()
    phases = np.exp(0.23j * np.arange(len(support)) ** 2)
    analysis = covariant_rank_one_analysis_matrix(8, support, phases)
    assert np.linalg.norm(
        analysis.conj().T @ analysis - np.eye(len(support)),
        ord=2,
    ) <= 1e-10


def test_nonunit_phase_coefficients_are_rejected() -> None:
    _, support = _law_and_support()
    phases = np.ones(len(support), dtype=complex)
    phases[2] = 0.5
    with pytest.raises(ValueError, match="unit modulus"):
        covariant_rank_one_analysis_matrix(8, support, phases)


def test_non_pgm_phase_measurement_reduces_to_phased_fiber_erasure() -> None:
    counts, support = _law_and_support()
    phases = np.exp(0.19j * (np.arange(len(support)) + 1) ** 2)
    control = audit_covariant_rank_one_measurement(
        "NON-PGM",
        counts,
        phases,
        5,
        phase_family="quadratic",
        seed=77,
    )
    assert control.differs_from_aligned_pgm
    assert control.correct_outcome_success_probability > 0
    assert control.matching_branch_amplitude_spread <= 1e-10
    assert control.garbage_cleanup_residual <= 1e-10
    assert control.qft_phased_erasure_residual <= 1e-10
    assert control.inverse_phased_fiber_preparation_residual <= 1e-10
    assert control.exact_covariant_rank_one_reduction_verified


def test_aligned_pgm_is_only_one_phase_control() -> None:
    counts, support = _law_and_support()
    control = audit_covariant_rank_one_measurement(
        "PGM",
        counts,
        np.ones(len(support), dtype=complex),
        3,
        phase_family="aligned-pgm",
        seed=91,
    )
    assert not control.differs_from_aligned_pgm
    assert control.status == "aligned-pgm-rank-one-control-verified"


def test_inverse_polynomial_success_bootstrap_remains_polynomial() -> None:
    for power in (0, 2, 4, 8):
        row = bootstrap_scaling_record(256, power, 8)
        assert row.polynomial_bootstrap
        assert not row.residue_phase_learning_required
        assert row.normalized_fiber_witness_preparation_polynomial_given_measurement


def test_theorem_does_not_overclaim_higher_rank_or_approximate_routes() -> None:
    theorem = covariant_rank_one_reduction_theorem()
    assert theorem.arbitrary_residue_phases
    assert not theorem.pgm_optimality_used
    assert theorem.accessible_rank_one_non_pgm_route_closed
    assert not theorem.arbitrary_higher_rank_povm_closed
    assert not theorem.approximate_unaligned_instrument_closed


def test_report_closes_only_rank_one_non_pgm_escape() -> None:
    report = run_covariant_rank_one_measurement_reduction()
    assert report.headline_metrics[
        "covariant_rank_one_normal_form_theorem_count"
    ] == 1
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.headline_metrics["non_pgm_phase_control_count"] == 4
    assert not report.claim_gate[
        "accessible_exact_rank_one_covariant_non_pgm_route_open"
    ]
    assert not report.claim_gate["higher_rank_collective_measurement_route_closed"]
    assert not report.claim_gate["speedup_claim_allowed"]
