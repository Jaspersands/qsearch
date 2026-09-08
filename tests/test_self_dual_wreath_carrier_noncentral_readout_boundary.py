import numpy as np

from self_dual_wreath_carrier_noncentral_readout_boundary import (
    _channel_statistics,
    audit_carrier_noncentral_control,
    exhaustive_group_orbit_product_baseline,
    natural_carrier_row_channels,
    run_carrier_noncentral_readout_boundary,
    write_carrier_noncentral_readout_boundary_report,
)


def test_exact_natural_channels_normalize_and_carrier_transcripts_are_blind() -> None:
    channels = natural_carrier_row_channels(3, 1)
    for schedule, row_channel, transcript_channel in channels:
        row_information, _, row_residual = _channel_statistics(row_channel)
        transcript_information, transcript_bayes, transcript_residual = (
            _channel_statistics(transcript_channel)
        )
        assert row_residual <= 1e-12
        assert transcript_residual <= 1e-12
        assert abs(transcript_information) <= 1e-12
        assert abs(transcript_bayes - 1 / 3) <= 1e-12
        if schedule:
            assert row_information > 0


def test_relative_group_orbit_product_basis_search_is_exhaustive_for_s4() -> None:
    baseline = exhaustive_group_orbit_product_baseline(4, 2)
    assert baseline.relative_basis_setting_count == 24**2
    assert baseline.exhaustive_over_group_orbit_bases is True
    assert baseline.exhaustive_over_all_local_povms is False
    assert baseline.best_mutual_information_bits > 0.43
    assert baseline.best_bayes_success_probability > 0.55


def test_perfect_matching_control_has_small_depth_one_signal_but_pgm_dominates() -> None:
    control = audit_carrier_noncentral_control(
        "S4-PERFECT-MATCHINGS",
        4,
        2,
    )
    records = {record.schedule: record for record in control.schedules}
    assert records["L"].mutual_information_bits > records["NONE"].mutual_information_bits
    assert control.best_carrier_schedule_by_information in {"L", "R"}
    assert control.deeper_alternation_improves_over_depth_one is False
    assert control.best_carrier_beats_global_pgm_information is False
    assert control.best_carrier_beats_global_pgm_bayes is False
    assert control.global_pgm_mutual_information_bits > 1.3
    assert control.global_pgm_bayes_success_probability > 0.9
    assert control.maximum_carrier_transcript_mutual_information_residual <= 1e-12
    assert control.exact_natural_channel_control_verified is True


def test_carrier_refinement_is_not_a_uniform_default_basis_improvement() -> None:
    control = audit_carrier_noncentral_control("S3-TRANSPOSITIONS", 3, 1)
    baseline = next(record for record in control.schedules if record.schedule == "NONE")
    nonempty = [record for record in control.schedules if record.schedule != "NONE"]
    assert max(record.mutual_information_bits for record in nonempty) < baseline.mutual_information_bits
    assert max(record.bayes_success_probability for record in nonempty) < baseline.bayes_success_probability


def test_report_compiles_noncentral_readout_without_promoting_decoder() -> None:
    report = run_carrier_noncentral_readout_boundary()
    assert report.theorem.carrier_transcript_zero_information_proved is True
    assert report.theorem.minimum_covariant_noncentral_readout_compiled is True
    assert report.theorem.physical_hidden_conditioned_signal_exhibited is True
    assert report.theorem.carrier_contextuality_implies_decoder_information is False
    assert report.headline_metrics[
        "finite_carrier_gain_over_default_young_control_count"
    ] == 1
    assert report.headline_metrics[
        "finite_global_pgm_dominates_carrier_control_count"
    ] == 3
    assert report.headline_metrics["deeper_alternation_gain_control_count"] == 0
    assert report.claim_gate["all_n_collective_information_advantage_proved"] is False
    assert report.claim_gate["speedup_claim_allowed"] is False


def test_writer_emits_artifact_without_registry(tmp_path) -> None:
    output = tmp_path / "carrier-noncentral-readout.json"
    payload = write_carrier_noncentral_readout_boundary_report(
        output,
        write_registry=False,
    )
    assert output.exists()
    assert payload["status"] == (
        "noncentral-readout-accessible-carrier-contextuality-not-decoder"
    )
    assert np.isfinite(
        payload["headline_metrics"]["maximum_best_carrier_information_bits"]
    )
