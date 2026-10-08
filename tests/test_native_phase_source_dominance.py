import json
import subprocess

from flint import fmpq
import pytest

from native_phase_source_dominance import REPORT, source_likelihoods, transfer_budget_profile


def test_original_data_likelihood_keeps_all_shared_secrets_and_modular_error_collisions():
    source = source_likelihoods(((1,), (2,)), 3)
    assert source["status"] == "COMPLETE_CALIBRATION_SOURCE_LIKELIHOODS"
    assert source["secret_count"] == 3 and source["classical_transcript_space"] == 9
    for i in range(3):
        assert sum(row[i] for row in source["likelihoods"].values()) == 1
    assert source["likelihoods"][(0, 0)][0] == fmpq(1, 4)
    ceiling = sum(max(p) for p in source["likelihoods"].values())/3
    assert 0 < ceiling <= 1


def test_source_reference_caps_return_unknown_not_a_favorable_subset():
    result = source_likelihoods(((1, 0), (0, 1)), 9, max_secret_count=10)
    assert result["status"] == "UNKNOWN_COMPLETE_SOURCE_ENUMERATION_CAP"
    assert result["likelihoods"] is None and not result["truncated_reference_promoted"]
    result = source_likelihoods(((1,),)*4, 9, max_value_count=100)
    assert result["likelihoods"] is None and result["classical_transcript_space"] == 6561


def test_decoder_sample_count_can_kill_the_same_source_quality_certificate():
    small = transfer_budget_profile(64, 3**64, "1/1048576", 512, "1/2")
    large = transfer_budget_profile(64, 3**64, "1/1048576", 2**40, "1/2")
    assert small["published_source_parameter_guard"] and large["published_source_parameter_guard"]
    assert small["pre_rounding_transfer_is_positive"]
    assert large["pre_rounding_transfer_success_lower"] == "0"
    assert not large["noise_budget_failure_is_a_receiver_impossibility_proof"]
    assert not small["receiver_implemented"] and not small["hardness_transfer_admitted"]


def test_exact_quantum_dual_is_not_a_claim_of_efficient_classical_simulation():
    r = json.loads(REPORT.read_text())
    assert r["any_quantum_receiver_Bayes_success_at_most_original_source_MAP"]
    assert not r["efficient_classical_dequantization_proved"] and not r["quantum_speedup_refuted"]
    assert [c["original_source_Bayes_success_exact"] for c in r["controls"]] == ["1/2", "1/6", "5/8", "9/16", "9/32"]
    for c in r["controls"]:
        ceiling = float(fmpq(c["original_source_Bayes_success_exact"]))
        assert c["numerical_native_PGM_success_diagnostic"] <= ceiling+1e-10
        assert c["numerical_native_F3_MAP_success_diagnostic"] <= ceiling+1e-10
        assert not c["numerical_diagnostics_are_optimality_certificates"]


def test_independent_checker_reconstructs_all_original_laws_and_exact_dual_matrices():
    result = subprocess.run(["node", str(REPORT.parents[1]/"certificates/native_phase_source_dominance_crosscheck.js")], capture_output=True, text=True, check=True)
    result = json.loads(result.stdout)
    assert result["status"] == "PASS" and result["complete_controls"] == 5
    assert result["positive_dual_difference_decompositions"] == 33
    assert result["exact_dual_entries"] == 189 and result["exact_conditional_density_entries"] == 1161
    assert result["exact_readout_likelihood_entries"] == 171


@pytest.mark.parametrize("mutation", ("likelihood", "transcript", "dual", "density", "trace", "readout", "dequantization", "budget"))
def test_independent_checker_rejects_wrong_math_or_overstated_advantage(tmp_path, mutation):
    r = json.loads(REPORT.read_text())
    c = r["controls"][0]
    if mutation == "likelihood":
        c["complete_nonzero_transcripts"][0]["conditional_probabilities"][0] = "-1"
    elif mutation == "transcript":
        c["complete_nonzero_transcripts"].pop()
    elif mutation == "dual":
        c["quantum_discrimination_dual_exact"][0][0] = ["0"]
    elif mutation == "density":
        c["conditional_quantum_densities_exact"][0][0][0] = ["1"]
    elif mutation == "trace":
        c["original_source_Bayes_success_exact"] = "1"
    elif mutation == "readout":
        c["native_F3_readout_likelihoods_exact"][0][0] = ["1"]
    elif mutation == "dequantization":
        r["efficient_classical_dequantization_proved"] = True
    else:
        r["source_budget_controls"][1]["pre_rounding_transfer_is_positive"] = True
    file = tmp_path/"false.json"
    file.write_text(json.dumps(r))
    assert subprocess.run(["node", str(REPORT.parents[1]/"certificates/native_phase_source_dominance_crosscheck.js"), str(file)], capture_output=True).returncode != 0


@pytest.mark.parametrize("call", (
    lambda: source_likelihoods(((1,),), 3), lambda: source_likelihoods(((True,), (1,)), 3),
    lambda: source_likelihoods(((1,), (1, 2)), 3),
    lambda: transfer_budget_profile(2, 9, .25, 1, "1/2"),
    lambda: transfer_budget_profile(2, 9, "1/4", 1, 0),
))
def test_invalid_reference_or_source_assumptions_fail_closed(call):
    with pytest.raises(ValueError):
        call()
