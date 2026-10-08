from copy import deepcopy
from fractions import Fraction
import json
import subprocess

from flint import fmpz_poly
import numpy as np
import pytest

from native_noncentral_filter_tradeoff import (
    ROOT, X, amplitude_polynomial, amplification_sos, coefficients,
    label_adaptive_relocation_control, native_control, rank_depth_ledger,
    run_controls, spectral_probability,
)


@pytest.fixture(scope="module")
def report():
    return run_controls()


@pytest.mark.parametrize("k", range(13))
def test_exact_interval_sos_reconstructs_the_global_amplification_bound(k):
    c = amplification_sos(k)
    rhs = fmpz_poly([])
    for t in c["positive_SOS_terms"]:
        p = fmpz_poly([int(x) for x in t["squared_polynomial_ascending_integer_coefficients"]])
        factor = X*X
        if t["nonnegative_interval_factor"] == "x_squared_times_one_minus_x":
            factor *= 1-X
        assert t["positive_weight"] > 0
        rhs += t["positive_weight"]*factor*p*p
    a = amplitude_polynomial(k)
    assert rhs == (2*k+1)**2*X-X*a*a
    assert c["exact_gap_polynomial_ascending_integer_coefficients"] == coefficients(rhs)
    for x in (Fraction(),Fraction(1,243),Fraction(1,3),Fraction(1,2),Fraction(1)):
        p = spectral_probability(x,k)
        assert 0 <= p <= 1
        assert p <= (2*k+1)**2*x


def test_source_weighted_filter_histories_are_actual_not_renormalized_oracle_successes(report):
    assert len(report["complete_actual_native_controls"]) == 8
    for c in report["complete_actual_native_controls"]:
        assert c["same_group_coset_density_error"] < 2e-12
        assert c["maximum_actual_vs_seed_polynomial_good_vector_error"] < 2e-12
        for f in c["noncentral_filters"]:
            assert len(f["source_weighted_iteration_history"]) == 7
            for h in f["source_weighted_iteration_history"]:
                p = Fraction(h["exact_raw_success_probability"])
                assert p <= Fraction(h["exact_rank_depth_upper_bound"])
                assert np.isclose(h["actual_raw_success_probability"],float(p))
                assert h["known_original_controlled_R_calls"] == c["original_source_copies"]*(2*h["iterations"]+1)
        assert not c["unknown_seed_reflection_supplied"]
        assert not c["full_depth_receiver_supplied"]


def test_more_synchronized_copies_do_not_improve_these_group_filters_but_direct_separate_tests_do(report):
    controls = report["complete_actual_native_controls"]
    for a,b in zip(controls[::2],controls[1::2]):
        for fa,fb in zip(a["noncentral_filters"],b["noncentral_filters"]):
            assert [h["exact_raw_success_probability"] for h in fa["source_weighted_iteration_history"]] == [h["exact_raw_success_probability"] for h in fb["source_weighted_iteration_history"]]
        if not a["fixed_guess_matches_hidden_generator"]:
            assert a["direct_order_three_stabilizer_baseline"]["exact_separate_copy_all_acceptance"] == "1/3"
            assert b["direct_order_three_stabilizer_baseline"]["exact_separate_copy_all_acceptance"] == "1/9"
            assert b["direct_order_three_stabilizer_baseline"]["exact_diagonal_tensor_acceptance"] == "1/3"


def test_quantum_verification_baseline_is_not_a_classical_dequantization_or_label_inference_lower_bound(report):
    for c in report["complete_actual_native_controls"]:
        b = c["direct_order_three_stabilizer_baseline"]
        assert not b["classical_dequantization_claimed"]
        assert not b["efficient_full_secret_search_supplied"]
        assert b["no_lower_bound_on_label_aware_inference_claimed"]
        assert b["known_controlled_original_R_calls_for_separate_copy_baseline"] == c["original_source_copies"]


def test_high_rank_is_not_expensive_memory_or_an_exclusion(report):
    for c in report["complete_actual_native_controls"]:
        f = c["noncentral_filters"][2]
        assert f["group_filter_rank"] == c["group_dimension"]//3
        assert f["high_rank_filter_has_a_single_public_rotation_digit_test"]
        assert f["source_weighted_iteration_history"][1]["exact_raw_success_probability"] == "25/27"
    assert not report["rank_lower_bound_is_a_memory_lower_bound"]


def test_growing_root_observed_label_filter_falsifies_the_unqualified_exponential_rank_cut(report):
    for c in report["growing_root_label_adaptive_countercontrols"]:
        assert c["label_adaptive_group_filter_rank"] == 3
        p = Fraction(c["iteration_histories"][0]["exact_raw_success_probability"])
        assert p == Fraction(1,3)
        assert p > Fraction(c["source_label_blind_rank_bound_at_zero_iterations_NOT_APPLICABLE"])
        assert c["selected_abelian_frequency_is_the_observed_native_label"]
        assert c["conditional_original_seed_and_reference_recovered_in_rotation_register"]
        assert not c["new_secret_information_extracted"]
        assert not c["full_depth_secret_decoder_supplied"]
        for h in c["iteration_histories"]:
            assert h["normalized_reference_entangled_seed_relocation_error"] < 2e-12
            assert np.isclose(h["actual_raw_success_probability"]+h["raw_failure_probability"],1)
        assert c["iteration_histories"][1]["exact_raw_success_probability"] == "25/27"
        assert c["iteration_histories"][2]["exact_raw_success_probability"] == "1/243"
    assert not report["label_adaptive_filters_ruled_out"]


@pytest.mark.parametrize("r,n,m", [(8,8,1),(32,32,32),(128,128,128),(512,512,512)])
def test_growing_ledger_explicitly_excludes_label_adaptive_filters_and_charges_each_action(r,n,m):
    ledger = rank_depth_ledger(r,n,7,13,m)
    assert ledger["raw_success_probability_upper_bound"] == {"cap":1,"numerator":7*27**2,"denominator":{"base":3,"exponent":r*n}}
    assert ledger["known_controlled_original_R_calls"] == m*27
    assert ledger["filter_must_be_independent_of_observed_native_frequency_labels"]
    assert not ledger["label_adaptive_filters_covered"]
    assert not ledger["arbitrary_noncentral_or_collective_receivers_covered"]


@pytest.mark.parametrize("args", [(0,1,1,0,1),(1,0,1,0,1),(1,1,0,0,1),(1,1,10,0,1),(1,1,1,-1,1),(1,1,1,0,False)])
def test_invalid_or_invented_resource_models_rejected(args):
    with pytest.raises(ValueError):
        rank_depth_ledger(*args)


def test_invalid_spectrum_or_finite_native_calibration_rejected():
    with pytest.raises(ValueError):
        spectral_probability(Fraction(4,3),2)
    with pytest.raises(ValueError):
        native_control(2,(1,0),True)
    with pytest.raises(ValueError):
        label_adaptive_relocation_control(2)


def replay(report, tmp_path):
    f = tmp_path/"filters.json"
    f.write_text(json.dumps(report,allow_nan=False))
    return subprocess.run(["node",str(ROOT/"research/certificates/native_noncentral_filter_tradeoff_crosscheck.js"),str(f)],capture_output=True,text=True)


def test_independent_integer_sos_and_growing_root_source_replay(report,tmp_path):
    out = replay(report,tmp_path)
    assert out.returncode == 0, out.stderr
    checked = json.loads(out.stdout)
    assert checked["exact_interval_SOS_certificates"] == 9
    assert checked["actual_native_source_histories"] == 168
    assert checked["exact_growing_root_frequency_row_identities"] == 6
    assert checked["label_adaptive_escape_preserved"]


@pytest.mark.parametrize("mutation", ["sos","sos_weight","success","copies","baseline","label_cut","rank_memory","relocation","failure","scaling","broader_cut"])
def test_independent_checker_rejects_forged_signal_or_overgeneralized_no_go(report,mutation,tmp_path):
    bad = deepcopy(report)
    c = bad["complete_actual_native_controls"][0]
    if mutation == "sos":
        bad["exact_amplification_interval_SOS_certificates"][2]["amplitude_polynomial_ascending_integer_coefficients"][0] = "6"
    elif mutation == "sos_weight":
        bad["exact_amplification_interval_SOS_certificates"][2]["positive_SOS_terms"][0]["positive_weight"] = -1
    elif mutation == "success":
        c["noncentral_filters"][0]["source_weighted_iteration_history"][0]["exact_raw_success_probability"] = "1"
    elif mutation == "copies":
        c["noncentral_filters"][0]["source_weighted_iteration_history"][1]["known_original_controlled_R_calls"] = 0
    elif mutation == "baseline":
        c["direct_order_three_stabilizer_baseline"]["classical_dequantization_claimed"] = True
    elif mutation == "label_cut":
        bad["label_adaptive_filters_ruled_out"] = True
    elif mutation == "rank_memory":
        bad["rank_lower_bound_is_a_memory_lower_bound"] = True
    elif mutation == "relocation":
        bad["growing_root_label_adaptive_countercontrols"][0]["new_secret_information_extracted"] = True
    elif mutation == "failure":
        bad["growing_root_label_adaptive_countercontrols"][0]["iteration_histories"][1]["raw_failure_probability"] = 0
    elif mutation == "scaling":
        bad["growing_rank_depth_ledgers"][0]["raw_success_probability_upper_bound"]["numerator"] = 1
    else:
        bad["arbitrary_adaptive_collective_or_high_rank_receivers_ruled_out"] = True
    assert replay(bad,tmp_path).returncode != 0
