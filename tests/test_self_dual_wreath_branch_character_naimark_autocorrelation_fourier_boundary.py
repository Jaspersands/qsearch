import json
import math

from self_dual_wreath_branch_character_naimark_autocorrelation_fourier_boundary import (
    audit_branch_fourier_boundary,
    audit_legendre_autocorrelation_counterexample,
    legendre_phase_field,
    run_naimark_autocorrelation_fourier_boundary,
    write_naimark_autocorrelation_fourier_boundary_report,
)


THRESHOLD_LABELS = (
    ((3,), (2, 1)),
    ((3,), (1, 1, 1)),
    ((2, 1), (1, 1, 1)),
)


def test_nonabelian_fourier_blocks_reproduce_direct_convolution_spectrum() -> None:
    control = audit_branch_fourier_boundary(
        "TEST-S3-THRESHOLD",
        THRESHOLD_LABELS,
    )
    assert control.exact_nonabelian_fourier_boundary_verified
    assert control.direct_to_fourier_singular_spectrum_residual < 1e-10
    assert math.isclose(
        control.convolution_condition_number,
        1.4950900031928052,
        rel_tol=1e-10,
    )


def test_matrix_autocorrelation_and_fourier_parseval_identities_hold() -> None:
    control = audit_branch_fourier_boundary(
        "TEST-S3-SINGLE",
        (((3,), (2, 1)),),
    )
    assert control.autocorrelation_to_global_parseval_residual < 1e-10
    assert control.fourier_to_global_parseval_residual < 1e-10
    assert math.isclose(
        control.normalized_gram_frobenius_residual,
        0.848870563244934,
        rel_tol=1e-10,
    )


def test_threshold_fourier_sector_extremes_are_recorded() -> None:
    control = audit_branch_fourier_boundary(
        "TEST-S3-SECTORS",
        THRESHOLD_LABELS,
    )
    by_partition = {row.partition: row for row in control.sector_controls}
    assert math.isclose(
        by_partition[(3,)].maximum_gram_eigenvalue,
        19.0 / 12.0,
        rel_tol=1e-10,
    )
    assert math.isclose(
        by_partition[(1, 1, 1)].minimum_gram_eigenvalue,
        17.0 / 24.0,
        rel_tol=1e-10,
    )


def test_completed_legendre_field_is_pointwise_unit_modulus() -> None:
    field = legendre_phase_field(43)
    assert len(field) == 43
    assert all(abs(abs(value) - 1.0) < 1e-12 for value in field)


def test_order_inverse_autocorrelation_does_not_give_uniform_gap() -> None:
    control = audit_legendre_autocorrelation_counterexample(43)
    assert control.exact_legendre_counterexample_verified
    assert math.isclose(
        control.maximum_nonidentity_autocorrelation_magnitude,
        1.0 / 43.0,
        rel_tol=1e-10,
    )
    assert math.isclose(
        control.convolution_condition_number,
        math.sqrt(44.0),
        rel_tol=1e-10,
    )
    assert not control.pointwise_order_inverse_autocorrelation_sufficient_for_uniform_gap


def test_legendre_bad_uniform_sector_has_vanishing_regular_mass() -> None:
    control = audit_legendre_autocorrelation_counterexample(103)
    assert math.isclose(
        control.normalized_gram_frobenius_residual,
        102.0 / 103.0**2,
        rel_tol=1e-10,
    )
    assert math.isclose(
        control.half_window_bad_spectral_mass_fraction,
        1.0 / 103.0,
        rel_tol=1e-10,
    )
    assert control.vanishing_frobenius_error_allows_state_weighted_trimming


def test_report_preserves_all_physical_and_speedup_gates() -> None:
    report = run_naimark_autocorrelation_fourier_boundary()
    assert report.theorem.theorem_verified
    assert report.claim_gate["nonabelian_fourier_block_criterion_proved"]
    assert not report.claim_gate["natural_branch_state_weighted_fourier_tail_proved"]
    assert not report.claim_gate["physical_input_maximally_mixed_or_dominated_proved"]
    assert not report.claim_gate["normalization_one_dense_fourier_multiplier_compiled"]
    assert not report.claim_gate["physical_pgm_decoder_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_writer_emits_live_artifact(tmp_path) -> None:
    path = tmp_path / "autocorrelation-fourier.json"
    payload = write_naimark_autocorrelation_fourier_boundary_report(path)
    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert loaded["status"] == payload["status"]
    assert loaded["headline_metrics"]["legendre_uniform_gap_counterexample_count"] == 8
