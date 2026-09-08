from pathlib import Path

import proof_tracker

from self_dual_wreath_dimensionless_pgm_truncation_bridge import (
    write_dimensionless_pgm_truncation_bridge_report,
)
from self_dual_wreath_disjoint_pair_covariance_polar_reduction import (
    audit_pair_carrier_flatness,
    audit_two_pair_covariance_polar,
    natural_pair_lcu_normalization_record,
    run_disjoint_pair_covariance_polar_reduction,
    write_disjoint_pair_covariance_polar_reduction_report,
)


def test_pair_carrier_average_is_flat_with_kronecker_multiplicity_two() -> None:
    controls = audit_pair_carrier_flatness(5, 2, (2, 3))
    repeated = next(
        control
        for control in controls
        if control.carrier_partition == (3, 1, 1)
    )
    assert repeated.kronecker_multiplicity == 2
    assert repeated.carrier_support_rank == 12
    assert repeated.maximum_flat_average_residual <= 1e-10
    assert repeated.maximum_rank_scaled_lcu_identity_residual <= 1e-10
    assert repeated.maximum_centered_mean_residual <= 1e-10
    assert repeated.exact_pair_branch_flatness_verified is True
    assert repeated.exact_rank_scaled_lcu_verified is True


def test_natural_lcu_likelihood_denominator_cancels_in_expectation() -> None:
    records = [
        natural_pair_lcu_normalization_record(n, n // 2)
        for n in (3, 5, 6, 8, 10)
    ]
    assert all(record.exact_natural_branch_probability_mass == "1" for record in records)
    assert all(
        record.expected_rank_scaled_lcu_normalization <= 4.0 + 1e-12
        for record in records
    )
    assert all(record.exact_expectation_bound_verified for record in records)
    assert records[2].maximum_finite_rank_scaled_lcu_normalization >= 60.0
    assert all(
        record.retained_natural_two_pair_mass_lower_bound >= 0.75
        for record in records
    )


def test_dimensionless_covariance_frame_reproduces_global_pgm() -> None:
    controls = [
        audit_two_pair_covariance_polar(5, 2, (0, 1), (0, 1)),
        audit_two_pair_covariance_polar(5, 2, (1, 1), (1, 1)),
    ]
    for control in controls:
        assert abs(control.total_joint_branch_probability - 1.0) <= 1e-10
        assert control.maximum_dimensionless_frame_identity_residual <= 1e-10
        assert control.maximum_reduced_pgm_effect_residual <= 1e-10
        assert control.maximum_reduced_pgm_completeness_residual <= 1e-10
        assert control.minimum_positive_dimensionless_metric_eigenvalue > 0
        assert control.maximum_operator_schmidt_rank_upper_bound_residual == 0
        assert control.exact_covariance_polar_reduction_verified is True
    assert controls[1].maximum_covariance_operator_schmidt_rank == 14
    assert controls[1].maximum_dimensionless_metric_support_condition_number > 7.7


def test_report_keeps_access_compiler_spectral_gap_and_speedup_blocked() -> None:
    report = run_disjoint_pair_covariance_polar_reduction()
    assert report.theorem.all_n_pair_branch_flatness_proved is True
    assert report.theorem.dimensionless_covariance_frame_reduction_proved is True
    assert report.theorem.pgm_rank_normalization_cancellation_proved is True
    assert report.theorem.all_n_natural_lcu_expectation_bound_proved is True
    assert (
        report.theorem.conditional_public_covariance_block_encoding_schema_proved
        is True
    )
    assert report.theorem.uniform_public_covariance_block_encoding_compiled is False
    assert report.theorem.inverse_square_root_spectral_gap_proved is False
    assert report.theorem.threshold_copy_extension_proved is False
    assert report.theorem.pgm_output_isometry_compiled is False
    assert report.theorem.hidden_involution_decoder_compiled is False
    assert report.claim_gate["speedup_claim_allowed"] is False


def test_writer_emits_artifact_without_registry(tmp_path: Path) -> None:
    output = tmp_path / "covariance-polar-reduction.json"
    payload = write_disjoint_pair_covariance_polar_reduction_report(
        output,
        write_registry=False,
    )
    assert output.exists()
    assert payload["status"] == (
        "dimensionless-covariance-polar-access-normalized-spectral-gap-open"
    )
    assert (
        payload["headline_metrics"][
            "uniform_public_covariance_block_encoding_compiler_count"
        ]
        == 0
    )


def test_proof_tracker_separates_proved_reduction_from_open_compiler(
    tmp_path: Path,
    monkeypatch,
) -> None:
    output = tmp_path / "covariance-polar-reduction.json"
    write_disjoint_pair_covariance_polar_reduction_report(
        output,
        write_registry=False,
    )
    truncation_output = tmp_path / "dimensionless-truncation.json"
    write_dimensionless_pgm_truncation_bridge_report(
        truncation_output,
        write_registry=False,
    )
    monkeypatch.setattr(
        proof_tracker,
        "DISJOINT_PAIR_COVARIANCE_POLAR_REDUCTION_PATH",
        output,
    )
    monkeypatch.setattr(
        proof_tracker,
        "DIMENSIONLESS_PGM_TRUNCATION_BRIDGE_PATH",
        truncation_output,
    )
    lemmas = {
        lemma.id: lemma
        for lemma in proof_tracker._disjoint_pair_covariance_polar_lemmas(
            "CODE-COSET-COLLECTIVE"
        )
    }
    assert "proved" in lemmas[
        "LEMMA-CODE-COSET-COLLECTIVE-PAIR-CARRIER-ALL-N-FLATNESS"
    ].status
    assert "proved" in lemmas[
        "LEMMA-CODE-COSET-COLLECTIVE-PAIR-COVARIANCE-RANK-NORMALIZATION-CANCELLATION"
    ].status
    for lemma_id in (
        "LEMMA-CODE-COSET-COLLECTIVE-PAIR-COVARIANCE-PUBLIC-BLOCK-ENCODING",
        "LEMMA-CODE-COSET-COLLECTIVE-THRESHOLD-COVARIANCE-PGM-OUTPUT-DECODER",
    ):
        assert lemmas[lemma_id].status.startswith("blocked-")
    assert lemmas[
        "LEMMA-CODE-COSET-COLLECTIVE-PAIR-COVARIANCE-POSITIVE-SPECTRAL-EDGE"
    ].status.startswith("superseded-")
