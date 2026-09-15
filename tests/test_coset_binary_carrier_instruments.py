from fractions import Fraction
import math

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
    COHERENT_PHASE_RULES, _coherent_phase_values, evaluate_coherent_subset_phase_query,
    unlabeled_selector_scaling_controls,
    _coherent_walsh_histogram_law, coherent_walsh_copy_scaling_controls, independent_pair_copy_baseline,
    fixed_selector_marginal_scaling_controls,
    symmetric_boolean_fourier_profile, coherent_terminal_rule_controls, coherent_parity_scaling_controls,
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
    from research_registry import initialize_seed_registry, load_negative_results, load_experiment_results, load_experiments, validate_registry
    from experiment_runner import run_experiment, supported_experiment_ids
    monkeypatch.chdir(tmp_path)
    write_binary_carrier_instrument_report(write_registry=False)
    assert not (tmp_path / "research/registry").exists()
    initialize_seed_registry(overwrite=True)
    assert DEFAULT_EXPERIMENT_ID in supported_experiment_ids()
    assert run_experiment(DEFAULT_EXPERIMENT_ID).status == "completed"
    recorded = next(row for row in load_experiments() if row["id"] == DEFAULT_EXPERIMENT_ID)
    assert "declared_terminal_rules_evaluated" in recorded["metrics"]
    initialize_seed_registry(overwrite=False)
    assert next(row for row in load_experiments() if row["id"] == DEFAULT_EXPERIMENT_ID) == recorded
    assert any(row["experiment_id"] == DEFAULT_EXPERIMENT_ID for row in load_experiment_results())
    negatives = {row["id"] for row in load_negative_results()}
    assert "CARRIER-INVARIANCE-NOT-A-BINARY-NO-GO" in negatives
    assert "FINITE-BINARY-CARRIER-ALTERNATION-LATENT-IRREP" in negatives
    assert "DISCARDED-GPE-REFERENCE-NOT-LUDERS-INSTRUMENT" in negatives
    assert "FIXED-SUBSET-PALETTE-COPY-COMPRESSION" in negatives
    assert "SOURCE-LABELS-DO-NOT-RESCUE-FIXED-LARGE-CELLS" in negatives
    assert "ADAPTIVE-PALETTE-CATALOGUE-NOT-FREE-ESCAPE" in negatives
    assert "UNLABELED-COHERENT-MASK-COUNT-NOT-INFORMATION-AMPLIFICATION" in negatives
    assert "SOURCE-SELECTOR-MARGINALS-NOT-JOINT-INFORMATION" in negatives
    assert "FIXED-SELECTOR-MARGINAL-NOT-SCALABLE-READOUT" in negatives
    assert "S4-COHERENT-SIGN-PHASE-HAS-ABELIAN-SUPPORT" in negatives
    assert "COHERENT-PARITY-AND-BOUNDED-FOURIER-NORM-READOUTS" in negatives
    assert "POLYNOMIAL-READOUT-TIME-NOT-SMALL-FOURIER-NORM" in negatives
    assert "S6-SOURCE-SELECTED-PARITY-ALL-COPY-FAILURE" in negatives
    assert "CORRECTED-WALSH-OUTPUT-LARGE-COPY-MIXTURE-BOUND" in negatives
    assert "FULL-SOURCE-WALSH-LARGE-COPY-MIXTURE-BOUND" in negatives
    assert "S8-SIGN-CATEGORY-WALSH-INTERMEDIATE-PAIR-FAILURE" in negatives
    assert "FULL-SOURCE-QUANTUM-SELECTOR-LARGE-COPY-BOUND" in negatives
    assert "UNMEASURED-IRREP-LABEL-NOT-A-COHERENT-ESCAPE" in negatives
    assert "HIGH-OCCUPATION-MASK-FIDELITY-OBSTRUCTION" in negatives
    assert "FIXED-MASK-PHASE-ASYMMETRY-NOT-EXTRA-INFORMATION" in negatives
    assert "VACUUM-COHERENCE-NOT-ASYMPTOTIC-RESCUE" in negatives
    assert "LOW-OCCUPATION-SUPPORT-DIMENSION-OBSTRUCTION" in negatives
    assert "SEPARATED-LOW-HIGH-COHERENCE-NOT-ASYMPTOTIC-ESCAPE" in negatives
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
    assert lemmas[7].status == "derived-coherent-phase-primitive-reduction-review-pending"
    assert lemmas[8].status == "derived-unlabeled-selector-bound-review-pending"
    assert lemmas[9].status == "derived-fixed-selector-marginal-bound-review-pending"
    assert lemmas[1].status == "blocked-terminal-rules-supplied-scalable-advantage-missing"
    assert lemmas[10].status == "derived-coherent-parity-fourier-norm-bound-review-pending"
    assert lemmas[11].status == "exact-finite-degree-all-copy-certificate-review-pending"
    assert lemmas[12].status == "derived-corrected-output-mixture-bound-review-pending"
    assert lemmas[13].status == "derived-full-source-walsh-bound-review-pending"
    assert lemmas[14].status == "exact-s8-finite-window-failure-review-pending"
    assert lemmas[15].status == "derived-source-selector-quantum-bound-review-pending"
    assert lemmas[16].status == "derived-mask-tail-fidelity-bound-review-pending"
    tail = next(row for row in findings if row.id.endswith("MASK-TAIL-FIDELITY-BOUND"))
    assert "Source-selected masks falsify" in tail.required_action
    assert "not a novel result by certification" in tail.required_action
    assert "WITHOUT a uniform-overlap penalty" in lemmas[16].statement
    assert lemmas[17].status == "derived-selector-mask-symmetry-review-pending"
    symmetry = next(row for row in findings if row.id.endswith("SELECTOR-MASK-SYMMETRY-REDUCTION"))
    assert "not an all-mask no-go" in symmetry.required_action
    assert "cross-weight coherence" in lemmas[17].statement
    assert lemmas[18].status == "derived-vacuum-coherence-bound-review-pending"
    vacuum = next(row for row in findings if row.id.endswith("VACUUM-COHERENCE-GAIN-BOUND"))
    assert "NOT a bound on total trace distance" in vacuum.required_action
    assert "nonempty low-weight" in lemmas[18].statement
    assert lemmas[19].status == "derived-low-occupation-support-bound-review-pending"
    low_support = next(row for row in findings if row.id.endswith("LOW-OCCUPATION-SUPPORT-BOUND"))
    assert "do NOT bound their mutual coherence" in low_support.required_action
    assert lemmas[20].status == "derived-occupation-band-bound-review-pending"
    band = next(row for row in findings if row.id.endswith("OCCUPATION-BAND-LOCALIZATION"))
    assert "Do not project to the middle band alone" in band.required_action
    assert lemmas[21].status == "derived-source-resolved-selector-schur-boundary-review-pending"
    schur = next(row for row in findings if row.id.endswith("SOURCE-RESOLVED-SELECTOR-SCHUR-BOUNDARY"))
    assert "Matrix dimension is not a circuit lower bound" in schur.required_action
    assert lemmas[22].status == "derived-selector-coefficient-mass-bound-review-pending"
    mass = next(row for row in findings if row.id.endswith("SELECTOR-COEFFICIENT-MASS-BOUND"))
    assert "not an all-query no-go" in mass.required_action
    assert "average individual distance" in mass.required_action
    quantum = next(row for row in findings if row.id.endswith("SOURCE-SELECTOR-QUANTUM-MIXTURE-BOUND"))
    assert "Source records are CLASSICAL" in quantum.required_action
    assert "intermediate window is closed ASYMPTOTICALLY" in quantum.required_action
    assert "not for every finite degree or arbitrary mask state" in quantum.required_action
    assert "Never substitute one representative" in quantum.required_action
    assert "raw-copy bound" in quantum.required_action
    assert "common group-algebra unitary" in lemmas[15].statement
    assert "decision distance" in lemmas[15].statement
    assert "every polynomial copy budget" in lemmas[15].statement
    assert "BOTH endpoint orientations" in lemmas[15].falsification_test
    intermediate = next(row for row in findings if row.id.endswith("S8-SIGN-CATEGORY-INTERMEDIATE-FAILURE"))
    assert "does NOT test every retained irrep label" in intermediate.required_action
    retained = next(row for row in findings if row.id.endswith("FULL-SOURCE-WALSH-MIXTURE-BOUND"))
    assert "intermediate copy window is NOT closed" in retained.required_action
    assert "Complex phases are allowed" in retained.required_action
    selected = next(row for row in findings if row.id.endswith("SOURCE-SELECTED-PARITY-FINITE-BASELINE"))
    assert "fixed-degree all-copy certificate" in selected.required_action
    assert "not classical dequantization" in selected.required_action
    corrected = next(row for row in findings if row.id.endswith("CORRECTED-WALSH-OUTPUT-MIXTURE-BOUND"))
    assert "do NOT close the intermediate window" in corrected.required_action
    assert "requires discarding source labels" in corrected.required_action
    unlabeled = next(row for row in findings if row.id.endswith("UNLABELED-COHERENT-SELECTOR-BOUND"))
    assert "excludes retained source labels" in unlabeled.required_action
    assert validate_registry()["valid"]


def test_missing_cleanup_artifact_does_not_resolve_the_instrument_obligation(tmp_path, monkeypatch):
    from proof_tracker import _binary_carrier_instrument_lemmas
    monkeypatch.chdir(tmp_path)
    assert _binary_carrier_instrument_lemmas("CODE-COSET-COLLECTIVE")[2].status.startswith("blocked-")
    assert _binary_carrier_instrument_lemmas("CODE-COSET-COLLECTIVE")[5].status.startswith("blocked-")
    assert _binary_carrier_instrument_lemmas("CODE-COSET-COLLECTIVE")[6].status.startswith("blocked-")
    assert _binary_carrier_instrument_lemmas("CODE-COSET-COLLECTIVE")[7].status.startswith("blocked-")
    assert _binary_carrier_instrument_lemmas("CODE-COSET-COLLECTIVE")[11].status.startswith("blocked-")
    assert _binary_carrier_instrument_lemmas("CODE-COSET-COLLECTIVE")[12].status.startswith("blocked-")
    assert _binary_carrier_instrument_lemmas("CODE-COSET-COLLECTIVE")[8].status.startswith("blocked-")
    assert _binary_carrier_instrument_lemmas("CODE-COSET-COLLECTIVE")[9].status.startswith("blocked-")
    assert _binary_carrier_instrument_lemmas("CODE-COSET-COLLECTIVE")[10].status.startswith("blocked-")


@pytest.mark.parametrize("n,t", ((3, 1), (4, 2)))
@pytest.mark.parametrize("rule", COHERENT_PHASE_RULES)
def test_coherent_phase_query_matches_independent_conditional_kernels(n, t, rule):
    row = evaluate_coherent_subset_phase_query(n, t, 3, rule, True)
    assert row["finite_coherent_query_verified"]
    assert max(row["residuals"].values()) < 1e-12
    assert row["source_blocks_evaluated"] == (27 if n == 3 else 125)
    assert row["conditional_kernels_checked"] == (51 if n == 3 else 500)
    assert row["zero_weight_alternative_blocks_omitted"] == (57 if n == 3 else 0)
    assert row["selector_without_source_labels_trace_distance"] == pytest.approx(
        row["unlabeled_selector_closed_form_distance"], abs=1e-12)
    assert not row["postselection_used"]
    assert not row["finite_helstrom_table_is_compiled_classifier"]
    assert not row["growing_copy_advantage_established"]
    assert not row["speedup_claim_allowed"]
    assert row["residuals"]["fixed_marginal_background_mixture"] < 1e-12
    assert row["residuals"]["random_two_subset_parity_law"] < 1e-12
    assert row["conditional_parity_laws_checked"] == 3 * row["conditional_kernels_checked"]
    assert row["random_hadamard_branches_checked"] == 8 * row["conditional_parity_laws_checked"]
    assert set(row["fixed_mask_marginal_with_all_source_labels_distances"]) == {"1", "2"}


def test_source_selector_correlations_cannot_be_replaced_by_product_marginals():
    row = evaluate_coherent_subset_phase_query(4, 2, 3, "negative_character_reflection", False)
    marginal_sum = row["source_only_readout"]["total_variation"] + row["selector_without_source_labels_trace_distance"]
    assert row["selector_and_source_label_trace_distance"] > marginal_sum + 0.04
    assert row["source_conditioning_counterexample"]["physical_source_weight"] > 0
    assert row["source_selector_decorrelation_distances"]["alternative"] > 0.8
    assert row["selector_without_source_labels_trace_distance"] == pytest.approx(3 / 14)


def test_coherent_signal_must_face_existing_pair_total_readout():
    row = evaluate_coherent_subset_phase_query(4, 2, 3, "negative_character_reflection", True)
    assert row["walsh_readout_with_source_labels"]["total_variation"] == pytest.approx(33 / 64)
    baseline = row["existing_carrier_baselines"]
    assert baseline["coherent_walsh_gain_over_one_pair_in_this_control"] == pytest.approx(3 / 32)
    assert baseline["coherent_retained_gain_over_pair_total_in_this_control"] < -0.02
    assert baseline["pair_total_uses_two_label_queries"]
    assert not baseline["pair_total_is_scalable_classifier"]
    support = row["exact_reflection_support_audit"]
    assert support["exact_support_audit_available"]
    assert support["support_is_subgroup"] and support["support_is_commuting"]
    assert support["all_overlapping_subset_phase_actions_commute"]
    assert sorted(item["coefficient"] for item in support["exact_coefficients"]) == ["-1/2", "1/2", "1/2", "1/2"]
    nonabelian = evaluate_coherent_subset_phase_query(3, 1, 3, "negative_character_reflection", True)
    assert not nonabelian["exact_reflection_support_audit"]["support_is_commuting"]


def test_zero_character_is_a_unit_phase_and_identity_control_is_identified():
    phases = _coherent_phase_values(((3,), (2, 1), (1, 1, 1)), 1, "negative_character_reflection")
    assert phases[(2, 1)] == 1
    assert phases[(1, 1, 1)] == -1
    row = evaluate_coherent_subset_phase_query(4, 2, 3, "zero_character_reflection", True)
    assert row["source_conditioning_counterexample"] is None
    assert row["selector_and_source_label_trace_distance"] == pytest.approx(row["source_only_readout"]["total_variation"])
    assert row["selector_without_source_labels_trace_distance"] < 1e-12
    for args in ((6, 3), (4, 2, True), (4, 2, 4), (3, 1, 3, "unknown"),
                 (3, 1, 3, "negative_character_reflection", "false")):
        with pytest.raises(ValueError):
            evaluate_coherent_subset_phase_query(*args)


def test_unlabeled_selector_mask_count_does_not_amplify_information():
    rows = unlabeled_selector_scaling_controls()
    assert len(rows) == 10
    assert all(row["applicable"] and not row["covers_retained_source_labels"] for row in rows)
    assert all(row["trace_distance_upper_bound_power_of_two"] < -50 for row in rows)


def test_walsh_copy_scaling_is_not_growing_degree_evidence_or_a_classical_solver():
    rows = coherent_walsh_copy_scaling_controls()
    assert len(rows) == 12
    assert all(row["finite_outcome_contraction_verified"] for row in rows)
    assert all(not row["is_growing_degree_scaling"] and not row["is_polynomial_sn_classifier"] for row in rows)
    s4 = next(row for row in rows if row["degree"] == 4 and row["copy_count"] == 8)
    assert s4["ordered_outcome_count"] == 100000000
    assert s4["histogram_count"] == 24310
    assert s4["walsh_readout"]["total_variation"] == pytest.approx(0.9190750122070312)
    assert s4["independent_pair_baseline"]["exact_total_variation"] == "3471/4096"
    assert not s4["independent_pair_baseline"]["quantum_frontend_classically_replaced"]
    s3 = next(row for row in rows if row["degree"] == 3 and row["copy_count"] == 12)
    assert s3["gain_over_independent_pair_baseline"] < -0.01


def test_pair_product_baseline_matches_existing_complete_three_copy_readout():
    for n, t in ((3, 1), (4, 2)):
        direct = evaluate_binary_carrier_instruments(n, t)
        pair = next(row for row in direct["schedules"] if row["schedule"] == "L")
        assert independent_pair_copy_baseline(n, t, 3)["total_variation"] == pytest.approx(pair["transcript"]["total_variation"])
        assert independent_pair_copy_baseline(n, t, 3)["fixed_point_free_terminal_scoring_polynomial"] == (n == 4)
    for n, t, copies in ((6, 3, 2), (4, 2, 9), (4, 2, True), (3, True, 3)):
        with pytest.raises(ValueError):
            _coherent_walsh_histogram_law(n, t, copies, "negative_character_reflection")


def test_low_order_fixed_selector_readouts_have_growing_degree_bounds():
    rows = fixed_selector_marginal_scaling_controls()
    assert len(rows) == 6
    assert all(row["all_source_labels_retained"] and row["applicable"] for row in rows)
    assert all(not row["covers_arbitrary_full_selector_classifier"] for row in rows)
    large = next(row for row in rows if row["degree"] == 1024 and row["observed_mask_bits"] == 11)
    assert large["trace_distance_upper_bound_power_of_two"] == -2174


@pytest.mark.parametrize("k", (1, 2, 3, 7, 16))
def test_krawtchouk_spectrum_reconstructs_every_hamming_weight(k):
    for rule, threshold in (("parity", None), ("threshold", 1), ("threshold", k // 2 + 1)):
        profile = symmetric_boolean_fourier_profile(k, rule, threshold)
        for w in range(k + 1):
            value = sum(Fraction(numerator, 2**k) * sum((-1)**j * math.comb(w, j) * math.comb(k - w, d - j)
                for j in range(max(0, d - (k - w)), min(d, w) + 1))
                for d, numerator in enumerate(profile["coefficient_numerators_by_degree"]))
            assert value == (1 if (w % 2 if rule == "parity" else w >= threshold) else -1)
        if rule == "parity":
            assert profile["exact_fourier_l1_norm"] == "1"
        if threshold == 1:
            assert Fraction(profile["exact_fourier_l1_norm"]) == 3 - Fraction(4, 2**k)


def test_majority_fourier_norm_is_not_bounded_by_its_linear_evaluation_cost():
    for k in (3, 7, 15, 31, 63, 127):
        m = (k - 1) // 2
        row = symmetric_boolean_fourier_profile(k, "threshold")
        for j in range(m + 1):
            expected = Fraction(math.comb(2 * m, m) * math.comb(m, j), 4**m * math.comb(2 * m, 2 * j))
            assert Fraction(abs(row["coefficient_numerators_by_degree"][2 * j + 1]), 2**k) == expected
        assert Fraction(row["exact_fourier_l1_norm"]) >= Fraction(2)**row["majority_fourier_l1_lower_bound_power_of_two"]
    assert Fraction(row["exact_fourier_l1_norm"]) > 2**60


def test_declared_terminal_rules_do_not_silently_fit_accepting_orientation():
    row = coherent_terminal_rule_controls(4, 2, 8)
    all_zero = next(item for item in row["rules"] if item["rule"] == "all_zero" and item["phase_corrected"])
    assert all_zero["signed_acceptance_gap"] == pytest.approx(0.9190750122070312)
    assert all_zero["signed_acceptance_gap"] == pytest.approx(all_zero["joint_source_and_rule_output"]["total_variation"])
    majority = next(item for item in row["rules"] if item["rule"] == "strict_majority" and item["phase_corrected"])
    assert majority["equal_prior_success"] < 0.5
    assert not majority["fitted_orientation_used"]
    assert Fraction(all_zero["exact_fourier_l1_norm"]) < 3
    assert not row["growing_degree_signal_established"]
    bound = next(item for item in coherent_parity_scaling_controls() if item["degree"] == 1024 and item["parity_size"] == 1)
    assert bound["source_corrected_all_zero_absolute_gap_upper_bound_power_of_two"] == -139


def test_histogram_rule_laws_match_the_executable_terminal_decisions():
    from involution_character_arithmetic import coherent_walsh_terminal_decision
    from representation_obstruction import integer_partitions
    partitions = integer_partitions(4)
    histograms, null, alternative, _ = _coherent_walsh_histogram_law(4, 2, 2, "negative_character_reflection")
    report = coherent_terminal_rule_controls(4, 2, 2)
    for rule in report["rules"]:
        accepts = []
        for histogram in histograms:
            sources, bits = [], []
            for i, count in enumerate(histogram):
                sources.extend([partitions[i // 2]] * count)
                bits.extend([i % 2] * count)
            result = coherent_walsh_terminal_decision(tuple(sources), tuple(bits),
                "parity" if rule["rule"] == "odd_parity" else "threshold",
                phase_corrected=rule["phase_corrected"], threshold=rule["threshold"], complement=rule["complement"])
            accepts.append(result["accept_hidden_class"])
        assert np.dot(null, accepts) == pytest.approx(rule["null_acceptance_probability"])
        assert np.dot(alternative, accepts) == pytest.approx(rule["alternative_acceptance_probability"])


@pytest.mark.parametrize("selection", ("all", "negative", "positive", "zero"))
@pytest.mark.parametrize("corrected", (False, True))
def test_exact_source_selected_moments_match_executable_rule_on_every_histogram(selection, corrected):
    from coset_binary_carrier_instruments import source_selected_parity_controls
    from involution_character_arithmetic import coherent_walsh_terminal_decision
    from representation_obstruction import integer_partitions
    partitions = integer_partitions(4)
    histograms, null, alternative, _ = _coherent_walsh_histogram_law(4, 2, 3, "negative_character_reflection")
    decisions = []
    for histogram in histograms:
        sources = tuple(label for i, label in enumerate(partitions) for bit in (0, 1) for _ in range(histogram[2 * i + bit]))
        bits = tuple(bit for i in range(len(partitions)) for bit in (0, 1) for _ in range(histogram[2 * i + bit]))
        decisions.append(coherent_walsh_terminal_decision(sources, bits, "parity",
            parity_selection=selection, phase_corrected=corrected)["accept_hidden_class"])
    row = source_selected_parity_controls(4, 2, (3,), selection, corrected)["copy_sweep"][0]
    assert row["null_acceptance_probability"] == pytest.approx(np.dot(null, decisions))
    assert row["alternative_acceptance_probability"] == pytest.approx(np.dot(alternative, decisions))


def test_source_selected_contraction_keeps_exact_class_covariance_beyond_s4():
    from coset_binary_carrier_instruments import audit_source_selected_parity_contraction
    audit = audit_source_selected_parity_contraction()
    assert audit["verified"] and audit["maximum_histogram_law_residual"] < 1e-12
    assert audit["independent_histogram_probability_laws_checked"] == 96
    assert audit["exact_all_hidden_member_spectra_checked"] == 21
    assert not audit["formal_proof_verification"]


def test_s6_source_selected_parity_failure_covers_every_copy_count_not_just_a_sweep():
    from coset_binary_carrier_instruments import source_selected_parity_all_copy_obstruction, source_selected_parity_controls
    certificate = source_selected_parity_all_copy_obstruction()
    assert certificate["all_copy_counts_from_two_covered"]
    assert certificate["tail_starts_at_copy_count"] == 38
    assert certificate["finite_prefix_copy_counts_checked"] == 36
    baseline = Fraction(certificate["exact_one_pair_baseline_gap"])
    assert baseline == Fraction(1271, 7200)
    assert Fraction(certificate["exact_finite_prefix_maximum_absolute_gap"]) < baseline
    assert Fraction(certificate["exact_tail_start_gap_upper_bound"]) < baseline
    norms = [Fraction(row["exact_weight_l1_norm"]) for row in certificate["null_and_alternative_envelopes"]]
    radii = [Fraction(row["exact_radius"]) for row in certificate["null_and_alternative_envelopes"]]
    assert radii == [Fraction(139, 180), Fraction(13, 15)]
    for k in (38, 39, 128, 2048):
        assert sum(norm * radius**k for norm, radius in zip(norms, radii)) / 2 < baseline
    assert not certificate["is_growing_degree_obstruction"]
    assert not certificate["covers_arbitrary_source_based_postprocessing"]
    result = source_selected_parity_controls(6, 3, (1, 2, 8, 128))
    assert result["copy_sweep"][1]["signed_acceptance_gap"] == -1 / 64
    assert result["copy_sweep"][-1]["signed_acceptance_gap"] == pytest.approx(-1.2207252482083908e-9)
    assert result["copy_sweep"][-1]["loses_to_pair_count_even_after_orientation_flip"]
    assert result["moment_certificate"]["negative_weights_present"]
    assert not result["moment_certificate"]["is_positive_classical_sampler"]


def test_averaging_the_hidden_member_before_the_product_changes_the_experiment():
    from coset_binary_carrier_instruments import _source_parity_group_data, _source_parity_local_moment, source_selected_parity_moment_certificate, _parity_spectrum_mean
    data = _source_parity_group_data(4, 2)
    order, hidden_count = len(data[0]), len(data[8])
    weighted = np.outer(data[5], data[5]).reshape(-1)
    averaged_numerators = sum(_source_parity_local_moment(data, "negative", True, h) for h in range(hidden_count)).reshape(-1)
    independent_h_mean = Fraction(sum(int(w) * int(value)**3 for w, value in zip(weighted, averaged_numerators)),
                                  order**2 * (2 * order * hidden_count)**3)
    actual = _parity_spectrum_mean(source_selected_parity_moment_certificate(4, 2), "alternative", 3)
    assert independent_h_mean != actual


def test_corrected_weight_formula_matches_matrix_histograms_and_exact_coset_mixtures():
    import json
    from coset_binary_carrier_instruments import audit_corrected_weight_contraction
    audit = audit_corrected_weight_contraction()
    assert audit["verified"]
    assert audit["independent_matrix_histogram_laws_checked"] == 24
    assert audit["maximum_histogram_residual"] < 1e-12
    assert audit["exact_diagonal_mixture_laws_checked"] == 48
    assert audit["exact_all_hidden_member_kernel_covariances_checked"] == 42
    assert not audit["arbitrary_complex_phases_covered"]
    assert json.loads(json.dumps(audit))["verified"] is True


def test_s6_corrected_weight_optimal_table_and_declared_thresholds_lose_to_pairs():
    from coset_binary_carrier_instruments import corrected_weight_controls
    control = corrected_weight_controls(6, 3, (2, 4, 8, 16, 32, 64, 128))
    for row in control["copy_sweep"]:
        assert not row["full_weight_bayes_beats_pair_event_count"]
        assert not row["bayes_table_is_compiled_classifier"]
        assert not row["exploratory_threshold_is_declared_algorithm"]
        assert all(not rule["absolute_gap_beats_pair_event_count"] for rule in row["declared_rules"])
    last = control["copy_sweep"][-1]
    assert last["full_corrected_weight_total_variation"] == pytest.approx(0.26548916173826664)
    assert last["declared_rules"][1]["signed_acceptance_gap"] == pytest.approx(0.007046078171967876)
    assert last["mixture_distances_from_full_laws"][0] < 6e-38
    assert control["does_not_retain_joint_source_and_corrected_bits"]


@pytest.mark.parametrize("rule", ("negative_character_reflection", "zero_character_reflection"))
def test_positive_binomial_mixture_is_an_approximation_not_a_free_exact_sampler(rule):
    from coset_binary_carrier_instruments import corrected_weight_laws, corrected_weight_character_certificate
    certificate = corrected_weight_character_certificate(6, 3, rule)
    full, mixtures, errors = corrected_weight_laws(6, 3, 1, rule)
    assert full[0] == full[1] == (Fraction(1), Fraction())
    assert full != mixtures
    for p, q, error in zip(full, mixtures, errors):
        assert sum(p) == sum(q) == 1 and min(p) >= 0 and min(q) >= 0
        assert 0 < sum(abs(x - y) for x, y in zip(p, q)) / 2 <= error
    assert certificate["class_overlap_bound_verified"]
    assert Fraction(certificate["exact_amplitude_overlap"]) <= Fraction(1, 15)
    assert not certificate["positive_mixture_is_full_law"]
    assert not certificate["classical_quantum_frontend_replacement"]


def test_every_real_central_s3_s4_reflection_satisfies_the_mixture_identities():
    import itertools
    from coset_binary_carrier_instruments import _source_parity_group_data, _corrected_weight_kernel, _integer_pair_spectrum, _exact_binomial_spectrum_law
    checked = 0
    for n, t in ((3, 1), (4, 2)):
        data = _source_parity_group_data(n, t)
        order = len(data[0])
        for phases in itertools.product((-1, 1), repeat=len(data[1])):
            coefficients = (data[3] * np.array(phases, dtype=np.int64)) @ data[2]
            assert int(coefficients @ coefficients) == order**2
            shifted = coefficients[data[8][0]]
            overlap = Fraction(sum(int(a)**2 * int(b)**2 for a, b in zip(coefficients, shifted)), order**4)
            assert overlap <= Fraction(1, len(data[8]))
            assert int(coefficients @ shifted) == 0
            for h in (None, 0):
                alpha, beta, diagonal, amplitudes = _corrected_weight_kernel(data, coefficients, h)
                radius = (np.abs(alpha) + np.abs(beta))[~diagonal]
                assert np.all(2 * radius**2 <= (4 * order)**2)
                spectrum = _integer_pair_spectrum(alpha, beta, np.outer(coefficients, coefficients))
                law = _exact_binomial_spectrum_law(spectrum, 3, 4 * order, order**2)
                assert min(law) >= 0 and sum(law) == 1
                assert int(amplitudes @ amplitudes) == (1 if h is None else 2) * order**2
            checked += 1
    assert checked == 40


def test_s6_noncentral_unitary_refutes_a_pointwise_class_overlap_bound_without_centrality():
    from coset_binary_carrier_instruments import _source_parity_group_data
    from coset_hidden_involution_binary_decision_reduction import compose_permutations
    data = _source_parity_group_data(6, 3)
    group, h = data[0], data[0][data[8][0][0]]
    # A real unitary supported on a Klein four subgroup, not a central S6 phase.
    e = tuple(range(6))
    g = (1, 0, 2, 3, 4, 5)
    assert compose_permutations(g, h) == compose_permutations(h, g)
    coefficients = {e: Fraction(1, 2), g: Fraction(1, 2), h: Fraction(1, 2), compose_permutations(g, h): Fraction(-1, 2)}
    convolution = {}
    for u, a in coefficients.items():
        for v, b in coefficients.items():
            product = compose_permutations(u, v)
            convolution[product] = convolution.get(product, Fraction()) + a * b
    assert convolution[e] == 1 and all(value == 0 for key, value in convolution.items() if key != e)
    overlap = sum(a*a * coefficients.get(compose_permutations(h, u), Fraction())**2 for u, a in coefficients.items())
    assert overlap == Fraction(1, 4) > Fraction(1, len(data[8]))
    # The averaged overlap can still obey a class-mass bound; this refutes only its pointwise form.


@pytest.mark.parametrize("n,t,k,rule", [(10, 5, 2, "negative_character_reflection"),
    (8, 4, 2, "zero_character_reflection"),
    (6, 3, True, "negative_character_reflection"), (6, 3, 0, "negative_character_reflection"),
    (6, 3, 257, "negative_character_reflection"), (6, 3, 2, "character_ratio_rotation")])
def test_corrected_weight_law_rejects_undeclared_controls(n, t, k, rule):
    from coset_binary_carrier_instruments import corrected_weight_laws
    with pytest.raises(ValueError):
        corrected_weight_laws(n, t, k, rule)


def test_pair_event_count_is_only_a_coarsening_of_the_full_pair_likelihood_baseline():
    from coset_binary_carrier_instruments import _pair_event_count_baseline
    for n, t in ((3, 1), (4, 2)):
        for k in (2, 3, 4, 8):
            distance, report = _pair_event_count_baseline(n, t, k)
            full = independent_pair_copy_baseline(n, t, k)
            assert distance <= Fraction(full["exact_total_variation"])
            assert not report["is_full_pair_likelihood_optimum"]
            assert not report["quantum_frontend_classically_replaced"]


@pytest.mark.parametrize("n,t,copies,selection,corrected", [
    (True, 1, (2,), "negative", True), (6, True, (2,), "negative", True),
    (8, 4, (2,), "negative", True), (6, 3, (), "negative", True),
    (6, 3, (True,), "negative", True), (6, 3, (0,), "negative", True),
    (6, 3, (1025,), "negative", True), (6, 3, (2,), "fitted", True), (6, 3, (2,), "negative", 1),
])
def test_source_selected_certificate_rejects_undeclared_or_unbounded_controls(n, t, copies, selection, corrected):
    from coset_binary_carrier_instruments import source_selected_parity_controls
    with pytest.raises(ValueError):
        source_selected_parity_controls(n, t, copies, selection, corrected)


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
