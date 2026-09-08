from pathlib import Path

import proof_tracker

from self_dual_wreath_dimensionless_pgm_truncation_bridge import (
    audit_dimensionless_branch_truncation,
    logarithmic_pair_cutoff_polynomial_lower_bound,
    logarithmic_pair_success_polynomial_lower_bound,
    run_dimensionless_pgm_truncation_bridge,
    sufficient_dimensionless_cutoff,
    threshold_truncation_scaling_record,
    write_dimensionless_pgm_truncation_bridge_report,
)


def test_dimensionless_metric_bounds_discarded_mass_without_support_dimension() -> None:
    control = audit_dimensionless_branch_truncation(
        5,
        2,
        (1, 1),
        (1, 1),
        (4, 1),
        (4, 1),
        spectral_cutoff=0.5,
    )
    assert control.product_support_dimension == 16
    assert control.dimensionless_metric_trace_residual <= 1e-10
    assert control.discarded_positive_eigenvalue_count == 11
    assert control.nontrivial_positive_spectrum_truncation is True
    assert 0 < control.discarded_average_state_mass < 0.5
    assert (
        control.discarded_average_state_mass
        <= control.discarded_mass_dimension_bound + 1e-10
    )
    assert control.discarded_mass_dimension_bound <= control.spectral_cutoff


def test_truncated_effects_are_legal_and_match_dimensionless_inverse() -> None:
    control = audit_dimensionless_branch_truncation(
        5,
        2,
        (1, 1),
        (1, 1),
        (3, 2),
        (3, 2),
        spectral_cutoff=0.9,
    )
    assert control.discarded_positive_eigenvalue_count == 5
    assert control.truncated_pgm_success < control.ideal_pgm_success
    assert control.truncated_pgm_success + 1e-10 >= control.gentle_success_lower_bound
    assert control.maximum_truncated_inverse_effect_residual <= 1e-10
    assert control.truncated_effect_completeness_residual <= 1e-10
    assert control.truncated_effect_subpovm_eigenvalue_violation <= 1e-10
    assert control.exact_dimensionless_truncation_verified is True


def test_success_adaptive_cutoff_retains_half_the_certificate() -> None:
    for success in (1.0, 0.5, 1.0 / 272.0, 1e-6):
        cutoff = sufficient_dimensionless_cutoff(success)
        assert 2.0 * cutoff**0.5 == success / 2.0


def test_fixed_and_logarithmic_pair_depth_have_polynomial_cutoffs() -> None:
    fixed = threshold_truncation_scaling_record(
        64,
        2,
        schedule="fixed-two-pair",
    )
    logarithmic = threshold_truncation_scaling_record(
        64,
        6,
        schedule="logarithmic-pair-depth",
    )
    assert fixed.pair_budget_legal is True
    assert fixed.cutoff_inverse_polynomial_proved is True
    assert fixed.sufficient_dimensionless_cutoff > 8e-7
    assert logarithmic.pair_budget_legal is True
    assert logarithmic.cutoff_inverse_polynomial_proved is True
    assert (
        logarithmic.pgm_success_lower_bound
        >= logarithmic_pair_success_polynomial_lower_bound(64)
    )
    assert (
        logarithmic.sufficient_dimensionless_cutoff
        >= logarithmic_pair_cutoff_polynomial_lower_bound(64)
    )
    assert fixed.minimum_positive_eigenvalue_required is False
    assert logarithmic.minimum_positive_eigenvalue_required is False


def test_report_removes_only_spectral_edge_gate() -> None:
    report = run_dimensionless_pgm_truncation_bridge()
    assert report.theorem.dimensionless_low_mass_bound_proved is True
    assert report.theorem.mixed_state_truncated_pgm_robustness_proved is True
    assert report.theorem.minimum_positive_spectral_edge_required is False
    assert report.theorem.full_threshold_metric_block_encoding_compiled is False
    assert report.theorem.pgm_output_isometry_compiled is False
    assert report.theorem.hidden_involution_decoder_compiled is False
    assert report.claim_gate["speedup_claim_allowed"] is False
    assert (
        report.headline_metrics[
            "nontrivial_positive_spectrum_truncation_control_count"
        ]
        == 2
    )


def test_writer_emits_artifact_without_registry(tmp_path: Path) -> None:
    output = tmp_path / "dimensionless-truncation.json"
    payload = write_dimensionless_pgm_truncation_bridge_report(
        output,
        write_registry=False,
    )
    assert output.exists()
    assert payload["status"] == (
        "minimum-spectral-edge-removed-full-threshold-frame-access-open"
    )
    assert payload["headline_metrics"]["full_threshold_metric_block_encoding_compiler_count"] == 0


def test_proof_tracker_marks_truncation_proved_but_full_access_blocked(
    tmp_path: Path,
    monkeypatch,
) -> None:
    output = tmp_path / "dimensionless-truncation.json"
    write_dimensionless_pgm_truncation_bridge_report(
        output,
        write_registry=False,
    )
    monkeypatch.setattr(
        proof_tracker,
        "DIMENSIONLESS_PGM_TRUNCATION_BRIDGE_PATH",
        output,
    )
    lemmas = {
        lemma.id: lemma
        for lemma in proof_tracker._dimensionless_pgm_truncation_lemmas(
            "CODE-COSET-COLLECTIVE"
        )
    }
    assert lemmas[
        "LEMMA-CODE-COSET-COLLECTIVE-DIMENSIONLESS-PGM-SPECTRAL-TRUNCATION"
    ].status.startswith("proved-")
    assert lemmas[
        "LEMMA-CODE-COSET-COLLECTIVE-FULL-THRESHOLD-RANK-SCALED-METRIC-ACCESS"
    ].status.startswith("blocked-")
    assert lemmas[
        "LEMMA-CODE-COSET-COLLECTIVE-TRUNCATED-PGM-HYPOTHESIS-OUTPUT-DECODER"
    ].status.startswith("blocked-")
