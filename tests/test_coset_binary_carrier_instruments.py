from fractions import Fraction

import numpy as np
import pytest

from coset_binary_carrier_instruments import (
    DEFAULT_EXPERIMENT_ID, SCHEDULES, _rank_one_carrier_hmm, _total_projectors,
    binary_outcome_statistics, build_binary_carrier_instrument_report,
    evaluate_binary_carrier_instruments, invariant_block_transcript_distance_squared_bound,
    one_pair_likelihood_ratio, write_binary_carrier_instrument_report,
)


@pytest.mark.parametrize("bad", ([0.2, 0.3], [1.1, -0.1], [float("nan"), 1], [float("inf"), 0], [0.5 + 0.1j, 0.5]))
def test_invalid_laws_are_not_clipped_or_renormalized(bad):
    with pytest.raises(ValueError):
        binary_outcome_statistics(np.array([0.5, 0.5]), bad)


def test_binary_statistics_use_half_l1_and_do_not_compile_a_likelihood_table():
    row = binary_outcome_statistics(np.array([0.5, 0.5]), np.array([0.25, 0.75]))
    assert row["total_variation"] == 0.25
    assert row["equal_prior_bayes_success"] == 0.625
    assert row["optimal_likelihood_table_is_a_compiled_classifier"] is False


@pytest.mark.parametrize("n,t", ((3, 1), (4, 2)))
def test_complete_source_instruments_charge_measurement_disturbance(n, t):
    report = evaluate_binary_carrier_instruments(n, t)
    assert report["finite_full_source_instrument_checks_verified"]
    assert report["source_blocks_evaluated"] == report["source_blocks_expected"]
    assert not report["postselected_source_mass"]
    rows = {row["schedule"]: row for row in report["schedules"]}
    assert rows["L"]["transcript"]["total_variation"] > rows["NONE"]["transcript"]["total_variation"]
    assert rows["L"]["retained_quantum_trace_distance"] < report["physical_raw_trace_distance"]
    assert rows["LT"]["transcript"]["total_variation"] == pytest.approx(rows["L"]["retained_quantum_trace_distance"])
    assert rows["LL"]["transcript"]["total_variation"] == pytest.approx(rows["L"]["transcript"]["total_variation"])
    assert rows["TL"]["transcript"]["total_variation"] == pytest.approx(rows["LT"]["transcript"]["total_variation"])
    for side in ("L", "R"):
        assert rows[side]["one_pair_character_likelihood_residual"] < 1e-10
        assert rows[side]["one_pair_character_classifier_distance"] == pytest.approx(rows[side]["transcript"]["total_variation"])
    for row in rows.values():
        assert row["transcript"]["normalization_residual"] < 1e-8
        assert row["young_row_readout"]["normalization_residual"] < 1e-8
        assert not row["retained_helstrom_distance_is_implemented_readout"]


def test_full_outcome_laws_not_only_aggregate_scores_have_a_classical_latent_model():
    report = evaluate_binary_carrier_instruments()
    assert report["physical_raw_trace_distance"] == pytest.approx(21 / 32)
    assert report["latent_total_irrep_hmm_source_blocks"] == 125
    assert report["maximum_joint_multiplicity"] == 1
    assert report["full_outcome_law_hmm_replay_residual"] < 1e-10
    rows = {row["schedule"]: row for row in report["schedules"]}
    assert rows["L"]["irrecoverable_trace_distance_loss"] == pytest.approx(1 / 24)
    assert rows["LT"]["transcript"]["total_variation"] == pytest.approx(59 / 96)
    assert rows["LRL"]["latent_total_irrep_hmm_replay_verified"]
    assert rows["LRL"]["transcript"]["total_variation"] < rows["LT"]["transcript"]["total_variation"]
    assert rows["LRL"]["young_row_readout"]["total_variation"] > rows["LRL"]["product_dephased_markov_ablation"]["total_variation"]
    assert not rows["LRL"]["dephased_ablation_is_a_general_classical_lower_bound"]


def test_latent_scalar_model_refuses_higher_multiplicity_branches():
    from representation_obstruction import integer_partitions
    from self_dual_wreath_physical_frame_blocks import permutation_representation_matrices
    sources = ((3, 1),) * 3
    representations = {lam: dict(permutation_representation_matrices(lam)) for lam in integer_partitions(4)}
    total = _total_projectors(sources, representations)
    coarse = (np.eye(27),) + tuple(np.zeros((27, 27)) for _ in range(4))
    row = _rank_one_carrier_hmm(sources, {"L": coarse, "R": coarse, "T": total}, np.eye(27) / 27, np.eye(27) / 27, ("L",))
    assert not row["applicable"]
    assert row["maximum_multiplicity"] > 1
    assert row["channels"] == {}


def test_fixed_copy_repetition_does_not_become_an_algorithm():
    assert invariant_block_transcript_distance_squared_bound(8, 3, 64) < Fraction(1, 1000)
    assert invariant_block_transcript_distance_squared_bound(128, 3, 128**2) < Fraction(1, 2**700)
    assert invariant_block_transcript_distance_squared_bound(8, 3, 0) == 0
    report = build_binary_carrier_instrument_report()
    assert report["headline_metrics"]["source_blocks_with_exact_latent_irrep_model"] == 152
    witness = report["classical_model_nonextension_witness"]
    assert witness["joint_multiplicity"] == 4
    assert witness["pair_kronecker_coefficient"] == 2
    assert Fraction(witness["exact_natural_source_triple_mass"]) == Fraction(27, 8000)
    assert not witness["quantum_advantage_implied"]
    assert not report["claim_gate"]["speedup_claim_allowed"]
    assert not report["claim_gate"]["fixed_copy_calibrations_are_candidate_algorithms"]
    assert not report["claim_gate"]["legal_classical_sampler_for_initial_latent_distribution_supplied"]
    assert not report["claim_gate"]["latent_model_replaces_quantum_frontend"]


def test_bad_protocols_are_rejected():
    for schedules in (("LRLR",), ("bad",), ("L", "L"), ()):
        with pytest.raises(ValueError):
            evaluate_binary_carrier_instruments(schedules=schedules)
    with pytest.raises(ValueError):
        evaluate_binary_carrier_instruments(6, 3)
    with pytest.raises(ValueError):
        one_pair_likelihood_ratio(((3, 1),) * 3, (4,), 2, "LR")
    with pytest.raises(ValueError):
        invariant_block_transcript_distance_squared_bound(4, True, 2)


def test_clean_registry_runner_and_negative_baseline_artifacts(tmp_path, monkeypatch):
    from research_registry import initialize_seed_registry, load_negative_results, load_experiment_results, validate_registry
    from experiment_runner import run_experiment, supported_experiment_ids
    monkeypatch.chdir(tmp_path)
    write_binary_carrier_instrument_report(write_registry=False)
    assert not (tmp_path / "research/registry").exists()
    initialize_seed_registry(overwrite=True)
    assert DEFAULT_EXPERIMENT_ID in supported_experiment_ids()
    assert run_experiment(DEFAULT_EXPERIMENT_ID).status == "completed"
    assert any(row["experiment_id"] == DEFAULT_EXPERIMENT_ID for row in load_experiment_results())
    negatives = {row["id"] for row in load_negative_results()}
    assert "CARRIER-INVARIANCE-NOT-A-BINARY-NO-GO" in negatives
    assert "FINITE-BINARY-CARRIER-ALTERNATION-LATENT-IRREP" in negatives
    from dequantization_checks import findings_from_negative_results
    from proof_tracker import _binary_carrier_instrument_lemmas
    findings = findings_from_negative_results([{"id": "CODE-COSET-COLLECTIVE"}], load_negative_results())
    finding = next(row for row in findings if row.id.endswith("FINITE-CARRIER-LATENT-IRREP-MODEL"))
    assert "rank-one condition already fails in S6" in finding.required_action
    assert "does not replace the quantum front end" in finding.required_action
    assert "spectral" not in finding.id.lower()
    lemmas = _binary_carrier_instrument_lemmas("CODE-COSET-COLLECTIVE")
    assert lemmas[0].status.startswith("numerically-verified-finite-")
    assert lemmas[1].status.startswith("blocked-")
    assert validate_registry()["valid"]
