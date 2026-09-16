import copy
import json
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

from coherent_overlap_programs import OverlapEchoProgram
from coset_overlap_echo import (
    DEFAULT_EXPERIMENT_ID, build_overlap_echo_report, exact_three_copy_echo,
    reflection_coefficients, regular_control, source_block_control, write_overlap_echo_report,
)


@pytest.mark.parametrize("spec", ((3, 1, 3, 1), (4, 2, 4, 2), (6, 3, 36, 6)))
def test_charged_growing_path_program(spec):
    program = OverlapEchoProgram(*spec)
    result = program.resource_contract(forward_gpe_operator_error=1e-8)
    q = 2 * (spec[2] - 1) * spec[3]
    assert len(program.chronological_bonds()) == q
    assert result["controlled_phase_queries"] == q
    assert result["group_qft_or_inverse_calls"] == 2 * q
    assert result["controlled_single_copy_group_action_or_inverse_calls"] == 4 * q
    assert result["composed_channel_diamond_distance_upper_bound"] == pytest.approx(4*q*1e-8)
    assert result["nonempty_subset_incidence_cells"] == spec[2]
    assert not result["data_reprepared_between_queries"]
    assert not result["intermediate_isotypic_labels_measured_or_discarded"]
    assert not result["speedup_claim_allowed"]
    assert not result["inverse_polynomial_bias_proved"]
    assert result["coset_preparations_per_trial"] == spec[2]


def test_chronological_echo_is_not_reverse_order_undo():
    assert OverlapEchoProgram(6, 3, 3).chronological_bonds() == ((0, 1), (1, 2), (0, 1), (1, 2))
    row = regular_control()
    assert row["verified"]
    assert row["reverse_order_undo_identity_residual"] < 1e-9
    assert row["state_weighted_commutator_effect_residual"] < 1e-9
    assert row["shared_hidden_minus_probability"] == 0
    assert row["independently_averaged_hidden_minus_probability"] > 0.01


@pytest.mark.parametrize("spec", ((True, 1, 3, 1), (4, True, 3, 1), (4, 2, True, 1),
                                  (4, 2, 3, False), (1, 1, 3, 1), (4, 3, 3, 1),
                                  (4, 2, 2, 1), (4, 2, 3, 0), (4, 0, 3, 1)))
def test_invalid_program_rejected(spec):
    with pytest.raises(ValueError):
        OverlapEchoProgram(*spec)


@pytest.mark.parametrize("error", (True, -0.1, float("nan"), float("inf"), "0"))
def test_invalid_precision_rejected(error):
    with pytest.raises(ValueError):
        OverlapEchoProgram(6, 3, 3).resource_contract(forward_gpe_operator_error=error)


def test_symbolic_large_program_does_not_expand():
    program = OverlapEchoProgram(1026, 513, 1026**2, 1026)
    record = program.resource_contract()
    assert record["controlled_phase_queries"] > 2_000_000_000
    json.dumps(record)
    with pytest.raises(ValueError, match="expansion budget"):
        program.chronological_bonds()


def test_raw_copy_bound_cannot_be_evaded_by_more_rounds():
    once = OverlapEchoProgram(1026, 513, 3).resource_contract()
    many = OverlapEchoProgram(1026, 513, 3, 1026**3).resource_contract()
    assert once["known_raw_class_mixture_trace_distance_squared_cap"] == many["known_raw_class_mixture_trace_distance_squared_cap"]
    assert once["known_raw_class_mixture_trace_distance_log2_outward_cap"] < -2000
    growing = OverlapEchoProgram(1026, 513, 1026**2, 1026).resource_contract()
    assert growing["known_raw_class_mixture_trace_distance_log2_outward_cap"] == 0
    assert growing["speedup_claim_allowed"] is False
    json.dumps(many)


@pytest.mark.parametrize("spec", ((3, 1), (4, 1), (4, 2)))
def test_exact_words_match_full_source_weighted_physical_readout(spec):
    exact = exact_three_copy_echo(*spec)
    physical = source_block_control(OverlapEchoProgram(*spec, 3))
    assert exact["verified"] and physical["verified"]
    assert exact["exact_reflection_convolution_verified"]
    for key in ("null_minus_probability", "alternative_minus_probability"):
        assert float(Fraction(exact[key])) == pytest.approx(physical[key], abs=1e-10)
    assert max(physical["residuals"].values()) < 1e-9


def test_nonmissing_is_not_sufficient_for_noncommutativity():
    record = exact_three_copy_echo(4, 2)
    assert record["nonmissing_negative_targets"]
    assert record["coefficient_support_is_commuting"]
    assert Fraction(record["normalized_squared_commutator_norm"]) == 0
    assert Fraction(record["exact_output_total_variation"]) == 0


def test_exact_s6_nonmissing_noncommuting_readout_still_loses_to_baseline():
    record = exact_three_copy_echo(6, 3)
    assert record["hidden_members_checked"] == 15
    assert len(record["nonmissing_negative_targets"]) == 4
    assert not record["coefficient_support_is_commuting"]
    assert Fraction(record["exact_output_total_variation"]) == Fraction(16843, 303750)
    assert Fraction(record["exact_output_total_variation"]) < Fraction(38684413, 186624000)
    assert len(set(record["per_hidden_moments"])) == 1
    assert not record["classical_solver_for_unknown_input_constructed"]


def test_repeating_the_echo_is_not_monotonic_amplification():
    once = source_block_control(OverlapEchoProgram(3, 1, 4, 1))
    twice = source_block_control(OverlapEchoProgram(3, 1, 4, 2))
    assert once["verified"] and twice["verified"]
    assert twice["output_total_variation"] < once["output_total_variation"]


def test_finite_evaluators_refuse_factorial_allocations():
    with pytest.raises(ValueError, match="budget"):
        reflection_coefficients(100, 50)
    with pytest.raises(ValueError, match="budget"):
        source_block_control(OverlapEchoProgram(6, 3, 36))


@pytest.fixture(scope="module")
def report():
    return build_overlap_echo_report()


def test_report_claims_and_falsifiers(report):
    assert report["claim_gate"]["finite_controls_verified"]
    assert report["claim_gate"]["nonmissing_noncommuting_control_verified"]
    assert not report["claim_gate"]["growing_degree_signal_proved"]
    assert not report["claim_gate"]["speedup_claim_allowed"]
    assert report["headline_metrics"]["finite_baseline_wins"] == 0
    assert len(report["falsifiers_triggered"]) == 2
    assert len(report["scaling_contracts"]) == 9
    json.dumps(report)


def test_writer_respects_registry_switch_and_custom_ids(tmp_path, monkeypatch, report):
    import coset_overlap_echo as module
    monkeypatch.setattr(module, "build_overlap_echo_report", lambda: copy.deepcopy(report))
    results, negatives = [], []
    monkeypatch.setattr(module, "upsert_experiment_result", results.append)
    monkeypatch.setattr(module, "upsert_negative_result", negatives.append)
    target = tmp_path / "report.json"
    write_overlap_echo_report(target, write_registry=False)
    assert results == [] and negatives == []
    write_overlap_echo_report(target, registry_experiment_id="EXP-CUSTOM", registry_candidate_id="CAND-CUSTOM", registry_result_id="RESULT-CUSTOM")
    assert results[0].id == "RESULT-CUSTOM"
    assert results[0].experiment_id == "EXP-CUSTOM"
    assert negatives[0].applies_to == ["CAND-CUSTOM"]
    assert json.loads(target.read_text())["claim_gate"]["speedup_claim_allowed"] is False


def test_proof_tracker_requires_literal_evidence_and_keeps_scaling_blocked(tmp_path, monkeypatch, report):
    from proof_tracker import _overlap_echo_lemmas
    monkeypatch.chdir(tmp_path)
    target = Path("research/representation/coset_overlap_echo.json")
    target.parent.mkdir(parents=True)
    target.write_text(json.dumps(report))
    records = _overlap_echo_lemmas("CAND")
    assert records[0].status.startswith("verified-finite")
    assert records[1].status.startswith("blocked")
    modified = copy.deepcopy(report)
    modified["claim_gate"]["finite_controls_verified"] = "true"
    target.write_text(json.dumps(modified))
    assert _overlap_echo_lemmas("CAND")[0].status.startswith("blocked")


def test_cli_no_registry_does_not_initialize_seed(monkeypatch, report):
    import qsearch
    from argparse import Namespace
    monkeypatch.setattr(qsearch, "initialize_seed_registry", lambda **kw: pytest.fail("seed touched"))
    monkeypatch.setattr(qsearch, "write_overlap_echo_report", lambda **kw: report if kw["write_registry"] is False else pytest.fail("registry touched"))
    assert qsearch.command_coset_overlap_echo(Namespace(no_registry=True)) == 0


def test_runner_and_seed_are_wired():
    from experiment_runner import COSET_EXPERIMENTS
    from research_registry import seed_candidate_records
    assert DEFAULT_EXPERIMENT_ID in COSET_EXPERIMENTS
    assert any(row.id == DEFAULT_EXPERIMENT_ID for row in seed_candidate_records()[1])


def test_runner_registry_dequantization_and_idempotency(tmp_path, monkeypatch, report):
    import coset_overlap_echo as module
    import experiment_runner
    from dequantization_checks import build_dequantization_report
    from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry
    monkeypatch.chdir(tmp_path)
    initialize_seed_registry(overwrite=False)
    monkeypatch.setattr(module, "build_overlap_echo_report", lambda: copy.deepcopy(report))
    write_overlap_echo_report()
    for _ in range(2):
        assert experiment_runner.run_experiment(DEFAULT_EXPERIMENT_ID).status == "completed"
    results = [r for r in load_experiment_results() if r["experiment_id"] == DEFAULT_EXPERIMENT_ID]
    assert len(results) == 1
    assert any(r["id"] == "COHERENT-OVERLAP-ECHO-FINITE-CALIBRATION-LIMITS" for r in load_negative_results())
    findings = build_dequantization_report()["findings"]
    assert any(r["id"].endswith("COHERENT-OVERLAP-ECHO-READOUT-BASELINE") and r["blocks_speedup_claim"] for r in findings)
    assert validate_registry()["valid"]


def test_negative_character_phase_matches_existing_clean_gpe_primitive():
    from coset_binary_carrier_instruments import _pair_gpe_instrument
    from coset_overlap_echo import _group_data
    from self_dual_wreath_physical_frame_blocks import permutation_representation_matrices
    from weak_fourier_signal import character_on_involution
    left, right = (3, 1), (2, 2)
    primitive = _pair_gpe_instrument(left, right)
    phases = {lam: -1 if character_on_involution(lam, 1) < 0 else 1 for lam in primitive.labels}
    clean = primitive.phase_unitary(phases)
    group = _group_data(4)[0]
    lr, rr = dict(permutation_representation_matrices(left)), dict(permutation_representation_matrices(right))
    numerators = reflection_coefficients(4, 1)[0]
    direct = sum(int(c)/24 * np.kron(lr[g], rr[g]) for c, g in zip(numerators, group))
    assert np.linalg.norm(clean - direct) < 1e-9
