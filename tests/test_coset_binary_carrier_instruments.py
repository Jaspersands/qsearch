from fractions import Fraction

import numpy as np
import pytest

from coset_binary_carrier_instruments import (
    DEFAULT_EXPERIMENT_ID, SCHEDULES, _rank_one_carrier_hmm, _total_projectors,
    binary_outcome_statistics, build_binary_carrier_instrument_report,
    evaluate_binary_carrier_instruments, invariant_block_transcript_distance_squared_bound,
    evaluate_pair_gpe_cleanup,
    audit_regular_cell_compression, fixed_palette_scaling_controls,
    audit_source_conditioned_cell_lifts, source_conditioned_palette_scaling_controls,
    source_conditioned_unbalanced_palette_controls,
    audit_adaptive_palette_abort_cover, adaptive_palette_catalogue_scaling_controls,
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


@pytest.mark.parametrize("n,t", ((3, 1), (4, 2)))
def test_clean_gpe_matches_luders_but_discarding_workspace_erases_correlations(n, t):
    cleanup = evaluate_pair_gpe_cleanup(n, t)
    controls = evaluate_binary_carrier_instruments(n, t)
    left = next(row for row in controls["schedules"] if row["schedule"] == "L")
    assert cleanup["finite_complete_source_cleanup_verified"]
    assert cleanup["source_blocks_evaluated"] == controls["source_blocks_evaluated"]
    assert max(cleanup["residuals"].values()) < 1e-10
    assert cleanup["clean_first_pair_retained_trace_distance"] == pytest.approx(left["retained_quantum_trace_distance"])
    assert cleanup["discarded_reference_retained_trace_distance"] == pytest.approx(left["transcript"]["total_variation"])
    assert cleanup["discard_then_clean_right_transcript"]["total_variation"] == pytest.approx(left["transcript"]["total_variation"])
    assert cleanup["extra_loss_from_discarded_reference"] > 0
    assert cleanup["hypothesis_independent_state_after_first_label"]
    assert not cleanup["global_twirl_is_the_same_channel_as_pair_twirl"]
    if n == 4:
        assert cleanup["extra_loss_from_discarded_reference"] == pytest.approx(37 / 192)


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
    assert report["headline_metrics"]["polynomial_label_arithmetic_controls"] == 4
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
    assert "DISCARDED-GPE-REFERENCE-NOT-LUDERS-INSTRUMENT" in negatives
    assert "FIXED-SUBSET-PALETTE-COPY-COMPRESSION" in negatives
    assert "SOURCE-LABELS-DO-NOT-RESCUE-FIXED-LARGE-CELLS" in negatives
    assert "ADAPTIVE-PALETTE-CATALOGUE-NOT-FREE-ESCAPE" in negatives
    from dequantization_checks import findings_from_negative_results
    from proof_tracker import _binary_carrier_instrument_lemmas
    findings = findings_from_negative_results([{"id": "CODE-COSET-COLLECTIVE"}], load_negative_results())
    finding = next(row for row in findings if row.id.endswith("FINITE-CARRIER-LATENT-IRREP-MODEL"))
    assert "rank-one condition already fails in S6" in finding.required_action
    assert "does not replace the quantum front end" in finding.required_action
    assert "spectral" not in finding.id.lower()
    cleanup = next(row for row in findings if row.id.endswith("CLEAN-GPE-INSTRUMENT-CONTRACT"))
    assert "global diagonal twirl preserves" in cleanup.required_action
    assert "not classical dequantization" in cleanup.required_action
    lemmas = _binary_carrier_instrument_lemmas("CODE-COSET-COLLECTIVE")
    assert lemmas[0].status.startswith("numerically-verified-finite-")
    assert lemmas[1].status.startswith("blocked-")
    assert lemmas[2].status == "derived-clean-gpe-primitive-reduction-review-pending"
    assert "neither a multiplicity basis nor a growing-copy classifier" in lemmas[2].falsification_test
    assert lemmas[3].status == "implemented-known-polynomial-two-copy-label-score"
    assert lemmas[4].status == "derived-fixed-palette-compression-review-pending"
    assert "Individual source labels split cells" in lemmas[4].falsification_test
    assert lemmas[5].status == "derived-source-conditioned-palette-bound-review-pending"
    assert "source-selected palettes invalidate" in lemmas[5].falsification_test
    conditioned = next(row for row in findings if row.id.endswith("SOURCE-CONDITIONED-PALETTE-BOUND"))
    assert "not classical dequantization" in conditioned.required_action
    assert "not been independently reviewed" in conditioned.required_action
    assert lemmas[6].status == "derived-adaptive-catalogue-cover-review-pending"
    assert "Catalogue cardinality is not a runtime lower bound" in lemmas[6].falsification_test
    cover = next(row for row in findings if row.id.endswith("ADAPTIVE-PALETTE-CATALOGUE-COVER"))
    assert "stepwise coverage is insufficient" in cover.required_action
    assert "not classical dequantization" in cover.required_action
    assert validate_registry()["valid"]


def test_missing_cleanup_artifact_does_not_resolve_the_instrument_obligation(tmp_path, monkeypatch):
    from proof_tracker import _binary_carrier_instrument_lemmas
    monkeypatch.chdir(tmp_path)
    assert _binary_carrier_instrument_lemmas("CODE-COSET-COLLECTIVE")[2].status.startswith("blocked-")
    assert _binary_carrier_instrument_lemmas("CODE-COSET-COLLECTIVE")[5].status.startswith("blocked-")
    assert _binary_carrier_instrument_lemmas("CODE-COSET-COLLECTIVE")[6].status.startswith("blocked-")


@pytest.mark.parametrize("spec", ((3, 1, 2), (3, 1, 3), (4, 2, 2)))
def test_cell_compression_preserves_each_hidden_input_and_diagonal_group_action(spec):
    control = audit_regular_cell_compression(*spec)
    assert control["regular_cell_compression_verified"]
    assert control["null_and_every_hidden_member_checked"]
    assert control["marginal_residual"] < 1e-12
    assert control["diagonal_action_intertwining_residual"] == 0


def test_growing_raw_copy_budget_does_not_rescue_a_fixed_palette():
    rows = {row["listed_subset_count"]: row for row in fixed_palette_scaling_controls()}
    assert rows[3]["raw_copy_count"] == 842
    assert rows[3]["effective_cell_count"] == 7
    assert Fraction(rows[3]["trace_distance_squared_upper_bound"]) < Fraction(1, 2**800)
    assert rows[10]["effective_cell_count"] == rows[10]["raw_copy_count"]
    assert Fraction(rows[10]["trace_distance_squared_upper_bound"]) == 1


def test_one_pair_label_arithmetic_does_not_enumerate_all_partitions(monkeypatch):
    import coset_binary_carrier_instruments as module
    def forbidden(*args):
        raise AssertionError("label validation must not enumerate every partition")
    monkeypatch.setattr(module, "integer_partitions", forbidden)
    ratio = module.one_pair_likelihood_ratio(((2048, 2048),) * 3, (4096,), 2048, "L")
    assert ratio > 0


@pytest.mark.parametrize("n,t,count,zero", ((3, 1, 81, 75), (4, 2, 620, 0)))
def test_conditioned_lifts_and_missing_irrep_povm_extensions_preserve_all_source_mass(n, t, count, zero):
    report = audit_source_conditioned_cell_lifts(n, t)
    assert report["finite_source_conditioned_lifts_verified"]
    assert report["all_source_mass_retained"] and report["all_hidden_members_checked"]
    assert report["positive_weight_lifts_checked"] == count
    assert report["zero_weight_tuples_omitted"] == zero
    assert report["incomplete_support_povm_extensions_checked"] > 0
    assert max(report["residuals"].values()) < 1e-12
    assert report["residuals"]["action_product_convention"] == 0
    assert not report["efficient_physical_conversion_claimed"]
    for row in report["controls"]:
        assert row["average_conditional_trace_distance"] <= row["exact_second_moment_jensen_upper_bound"] + 1e-12
        assert row["distance_of_averaged_state"] < 1e-12
        assert row["average_conditional_trace_distance"] > .1


def test_s4_normal_klein_four_persistent_modes_falsify_universal_cell_mixing():
    report = audit_source_conditioned_cell_lifts(4, 2)
    rows = [row for row in report["controls"] if row["hypothesis"] == "alternative"]
    for row in rows:
        assert row["maximum_outside_second_moment"] == pytest.approx(1)
        assert row["outside_modes_with_unit_second_moment"] == 2
        assert row["uniform_second_moment_upper_bound"] == 1
    third = next(row for row in rows if row["cell_width"] == 3)
    assert third["average_conditional_parseval_square"] == pytest.approx(241 / 72)
    assert third["average_conditional_trace_distance"] > .57
    # Exact characters, independent of the floating matrix construction:
    # for another nonidentity g in V4, h, g and hg share cycle type 2^2.
    dimensions = (1, 3, 2, 3, 1)
    characters = (1, -1, 2, -1, 1)
    second = sum(Fraction(d * (d + ch), 24) * Fraction(2 * ch, d + ch)**2
                 for d, ch in zip(dimensions, characters))
    assert second == 1


def test_source_selected_cells_cannot_reuse_the_iid_moment_estimate():
    report = audit_source_conditioned_cell_lifts(3, 1)
    alt = next(row for row in report["controls"] if row["hypothesis"] == "alternative")
    assert alt["maximum_outside_second_moment"] == pytest.approx(.5)
    # Under the alternative, S3's trivial irrep has probability 1/3. A cell
    # selected to contain only that label has f(g)=1, not iid p moments.
    selected_second_moment = Fraction(1)
    assert selected_second_moment > alt["maximum_outside_second_moment"]
    assert 1 - Fraction(2, 3)**20 > Fraction(999, 1000)


def test_source_conditioned_scaling_separates_obstruction_from_a_vacuous_bound():
    rows = {(row["degree"], row["listed_subset_count"]): row for row in source_conditioned_palette_scaling_controls()}
    assert rows[1024, 2]["trace_distance_upper_bound_power_of_two"] == -602
    assert rows[4096, 1]["trace_distance_upper_bound_power_of_two"] < -10000
    assert rows[4096, 3]["bound_is_vacuous"]
    for row in rows.values():
        assert not row["untouched_copies"]
        assert row["effective_cell_count"] == 2**row["listed_subset_count"] - 1
        assert sum(row["cell_widths"]) == row["source_labels_retained"]


def test_shared_hidden_cells_are_not_replaced_by_independent_hidden_samples():
    from coset_three_copy_recoupling_obstruction import involutions
    from coset_hidden_involution_binary_decision_reduction import right_regular_matrix
    single = [(np.eye(6) + right_regular_matrix(3, h)) / 6 for h in involutions(3, 1)]
    shared = sum(np.kron(state, state) for state in single) / 3
    independent = np.kron(sum(single) / 3, sum(single) / 3)
    assert np.linalg.norm(shared - independent) > .01
    difference = shared - np.eye(36) / 36
    assert 36 * np.trace(difference @ difference) == pytest.approx(Fraction(2**2 - 1, 3))


def test_unbalanced_palettes_do_not_gain_a_free_escape_from_a_few_small_cells():
    for row in source_conditioned_unbalanced_palette_controls():
        assert row["effective_cell_count"] == 3
        assert row["effective_coset_copy_count"] == 1 + sum(row["retained_cell_widths"])
        assert len(row["compressed_cell_widths"]) == 1
        assert row["trace_distance_upper_bound_power_of_two"] < -150


@pytest.mark.parametrize("n,t,blocks", ((3, 1, 27), (4, 2, 125)))
def test_aborting_catalogue_simulators_reconstruct_every_actual_adaptive_branch(n, t, blocks):
    row = audit_adaptive_palette_abort_cover(n, t)
    assert row["finite_adaptive_cover_verified"]
    assert row["source_blocks_evaluated"] == blocks
    assert row["selector_uses_an_actual_quantum_measurement_outcome"]
    assert row["all_source_mass_retained"]
    assert row["aborts_before_outside_operation"]
    assert not row["postselection_normalization_used"]
    assert max(row["residuals"].values()) < 1e-12
    assert row["actual_output"]["total_variation"] <= row["sum_of_comparison_distance_upper_bound"] + 1e-12
    for comparison in row["aborting_comparisons"]:
        assert 0 < comparison["abort_mass_null"] < 1
        assert 0 < comparison["abort_mass_alternative"] < 1
        assert comparison["success_mass_null"] + comparison["abort_mass_null"] == pytest.approx(1)
        assert comparison["success_mass_alternative"] + comparison["abort_mass_alternative"] == pytest.approx(1)


def test_finite_catalogue_is_not_assumed_to_rescue_the_asymptotic_signal():
    rows = {row["degree"]: row for row in adaptive_palette_catalogue_scaling_controls()}
    assert rows[128]["bound_is_vacuous"]
    assert rows[1024]["trace_distance_upper_bound_power_of_two"] == -601
    assert rows[4096]["trace_distance_upper_bound_power_of_two"] < -10000
    assert all(row["catalogue_size"] == 2 for row in rows.values())
