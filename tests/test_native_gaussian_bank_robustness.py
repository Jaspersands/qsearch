import json
import math
import subprocess

from flint import fmpq
import numpy as np
import pytest

from native_gaussian_bank_robustness import (
    REPORT, gaussian_bank_bound, gaussian_bank_tail, heavy_tail_countercontrol,
    joint_profile, logarithm_box, compact_capacity, scaling_profile,
)
from ternary_certified_noise_sampler import sqrt_box


@pytest.mark.parametrize("x", (1, 2, 3, 81, 2048, 4096, 2**300+17))
@pytest.mark.parametrize("bits", (16, 64))
def test_logarithm_enclosure_has_exact_width_and_high_precision_reference(x, bits):
    import mpmath as mp
    c = logarithm_box(x, bits)
    lo, hi = fmpq(c["lower"]), fmpq(c["upper"])
    assert hi-lo <= fmpq(1, 2**bits)
    with mp.workdps(180):
        value = mp.log(x)
        endpoint = lambda r: mp.mpf(str(r.numerator))/mp.mpf(str(r.denominator))
        assert endpoint(lo) <= value <= endpoint(hi)


def test_cached_logarithm_cannot_be_mutated_or_admit_boolean_arguments():
    first = logarithm_box(3, 64)
    first["upper"] = "0"
    assert logarithm_box(3, 64)["upper"] != "0"
    logarithm_box(1, 64)
    with pytest.raises(ValueError):
        logarithm_box(True, 64)


def test_original_gaussian_profile_escapes_scoped_global_moment_ledger_exclusion():
    p = joint_profile(64, 3**64, 512, "1/1048576")
    assert p["moment_only_global_exclusion"]["global_incompatibility_certified"]
    assert p["minimum_exposure_certificate"]["minimum_exposure"] == 15306
    b = p["Gaussian_refined_budget"]
    loss = fmpq(b["expected_complete_receiver_noise_success_loss_upper"])
    assert fmpq(14, 100) < loss < fmpq(15, 100)
    assert fmpq(p["conditional_pre_rounding_success_lower_if_that_receiver_exists"]) > fmpq(35, 100)
    assert b["index_comparison_compute_uncompute_pairs_upper"] == 512*15306
    assert not p["ideal_receiver_has_been_constructed"]
    assert not p["passing_support_dimension_and_noise_is_sufficient_for_recovery"]
    assert not p["caller_source_and_hardware_precision_debt_resolved"]


def test_larger_bank_and_smaller_alpha_have_separate_costed_refined_profiles():
    larger = joint_profile(64, 3**64, 1024, "1/1048576")
    lower = joint_profile(64, 3**64, 512, "1/16777216")
    assert larger["minimum_exposure_certificate"]["minimum_exposure"] == 3298
    assert fmpq(larger["Gaussian_refined_budget"]["expected_complete_receiver_noise_success_loss_upper"]) < fmpq(4, 100)
    assert lower["alpha"] != larger["alpha"]
    assert lower["minimum_exposure_certificate"]["minimum_exposure"] == 15306


def test_zero_exposure_and_huge_power_keep_noise_and_gate_debt_separate():
    zero = gaussian_bank_bound(3**64, 512, "1/1048576", 0)
    huge = gaussian_bank_bound(3**64, 512, "1/1048576", 2**20, phase_calls=1)
    assert zero["complete_pre_rounding_success_loss_upper"] == "0"
    assert huge["expected_complete_receiver_noise_success_loss_upper"] == "1"
    assert huge["weighted_phase_exposure"] == 2**20 and huge["nonidentity_phase_calls"] == 1
    assert not huge["fixed_errors_are_refreshed_on_reuse"]
    assert not huge["bound_is_pointwise_for_every_source_realization"]
    assert huge["caller_and_source_rounding_error_still_to_be_added"]


def test_independent_heavy_tail_counterexample_has_same_moment_but_invalidates_gaussian_proxy():
    c = heavy_tail_countercontrol()
    assert c["same_second_moment_promise_satisfied"]
    assert c["errors_are_independent_and_centered"]
    assert not c["Gaussian_marginal_law_satisfied"]
    assert fmpq(c["expected_operator_error_lower"]) > fmpq(c["Gaussian_proxy"]["expected_operator_norm_error_upper"])
    assert c["Gaussian_norm_certificate_falsified"]


def test_gaussian_maximum_control_uses_correct_width_and_charges_rare_banks():
    M, alpha = 16, 1/512
    b = gaussian_bank_bound(3**64, M, "1/512", 1)
    tail = gaussian_bank_tail(3**64, M, "1/512", 8)
    rng = np.random.default_rng(133010)
    X = rng.normal(0, alpha/math.sqrt(2*math.pi), (20000, 2*M))
    maxima = np.max(np.abs(X), axis=1)
    expected = np.mean(2*np.pi*maxima)
    assert expected < float(fmpq(b["expected_operator_norm_error_upper"]))
    assert np.mean(maxima > float(fmpq(tail["Gaussian_lift_absolute_radius_upper"]))) < float(fmpq(tail["failure_probability_upper"]))
    # Numerical controls do not establish the theorem or a source sampler.
    assert not tail["independence_required_for_union_bound"] and tail["no_exceptions_conditioned_away"]


@pytest.mark.parametrize("value,bits", (("0", 16), ("4", 16), ("2/3", 32), ("1234567/13", 64)))
def test_shared_exact_sqrt_enclosure_preserves_endpoints(value, bits):
    x = fmpq(value)
    lo, hi = sqrt_box(x, bits)
    assert lo*lo <= x <= hi*hi and hi-lo <= fmpq(1, 2**bits)


def test_independent_checker_replays_refinement_and_heavy_tail_falsifier():
    result = subprocess.run(["node", str(REPORT.parents[1]/"certificates/native_gaussian_bank_robustness_crosscheck.js")], text=True, capture_output=True, check=True)
    r = json.loads(result.stdout)
    assert r["status"] == "PASS" and r["generic_ledger_exclusions_reopened_by_Gaussian_tails"] == 1
    assert r["heavy_tail_countercontrols"] == 1 and not r["receiver_supplied"]
    assert r["scaling_profiles"] == 9 and r["scaling_support_exclusions"] == 2


@pytest.mark.parametrize("K,W", ((2, 0), (2, 3), (6, 5), (8, 12), (32, 100)))
def test_compact_logarithmic_upper_dominates_exact_small_signature_count(K, W):
    import mpmath as mp
    from native_recovery_capacity import signed_l1_ball
    c = compact_capacity(2, 2, K//2, W)
    upper = fmpq(c["signature_count_log_upper"])
    count = signed_l1_ball(K, W)["count"]
    with mp.workdps(160):
        assert mp.log(count) <= mp.mpf(str(upper.numerator))/mp.mpf(str(upper.denominator))


@pytest.mark.parametrize("n", (64, 256, 1024))
def test_quadratic_bank_has_certified_support_envelope_and_nonvacuous_gaussian_noise(n):
    p = scaling_profile(n, True, True)
    assert p["compact_capacity"]["signature_envelope_reaches_secret_count_by_single_term"]
    assert not p["compact_capacity"]["half_success_excluded_by_support_upper_bound"]
    assert p["Gaussian_refined_budget"]["bound_is_nonvacuous"]
    assert p["source_parameter_guard"]
    assert not p["actual_phase_support_spread_proved"]
    assert not p["efficient_LWE_solver_supplied"]


def test_linear_bank_scaling_fails_capacity_even_when_gaussian_noise_loss_is_small():
    for n in (256, 1024):
        p = scaling_profile(n, False)
        assert p["Gaussian_refined_budget"]["bound_is_nonvacuous"]
        assert p["compact_capacity"]["half_success_excluded_by_support_upper_bound"]
        assert not p["compact_capacity"]["secret_count_or_full_signature_sum_materialized"]


@pytest.mark.parametrize("mutation", ("log", "sqrt", "pi", "rounding", "phase_exposure", "gate_cost", "Gaussian_promise", "margin", "heavy_tail", "scaling_pass", "scaling_receiver", "receiver"))
def test_independent_checker_rejects_changed_proof_ingredients_and_success_claims(tmp_path, mutation):
    r = json.loads(REPORT.read_text())
    b = r["joint_profiles"][0]["Gaussian_refined_budget"]
    if mutation == "log":
        b["logarithm_certificate"]["upper"] = "0"
    elif mutation == "sqrt":
        b["sqrt_upper"] = "0"
    elif mutation == "pi":
        b["pi_upper"] = "3"
    elif mutation == "rounding":
        b["expected_operator_norm_error_upper"] = str(2*fmpq(b["alpha"])*fmpq(b["sqrt_upper"]))
    elif mutation == "phase_exposure":
        b["weighted_phase_exposure"] = 1
    elif mutation == "gate_cost":
        b["index_comparison_compute_uncompute_pairs_upper"] = 0
    elif mutation == "Gaussian_promise":
        b["Gaussian_law_inferred_from_values_or_second_moment"] = True
    elif mutation == "margin":
        r["joint_profiles"][0]["conditional_pre_rounding_success_lower_if_that_receiver_exists"] = "1/2"
    elif mutation == "heavy_tail":
        r["heavy_tail_countercontrol"]["expected_operator_error_lower"] = "0"
    elif mutation == "scaling_pass":
        r["scaling_profiles"][3]["compact_capacity"]["half_success_excluded_by_support_upper_bound"] = False
    elif mutation == "scaling_receiver":
        r["scaling_profiles"][1]["actual_phase_support_spread_proved"] = True
    else:
        r["joint_profiles"][0]["ideal_receiver_has_been_constructed"] = True
    file = tmp_path/"forged.json"
    file.write_text(json.dumps(r))
    assert subprocess.run(["node", str(REPORT.parents[1]/"certificates/native_gaussian_bank_robustness_crosscheck.js"), str(file)], capture_output=True).returncode != 0


@pytest.mark.parametrize("call", (
    lambda: logarithm_box(0), lambda: logarithm_box(3, True),
    lambda: gaussian_bank_bound(10, 512, "1/1024", 1),
    lambda: gaussian_bank_bound(9, 0, "1/1024", 1),
    lambda: gaussian_bank_bound(9, 1, .01, 1),
    lambda: gaussian_bank_bound(9, 1, "0", 1),
    lambda: gaussian_bank_bound(9, 1, "1", 1),
    lambda: gaussian_bank_bound(9, 1, "1/1024", 1, phase_calls=0),
    lambda: gaussian_bank_bound(9, 1, "1/1024", 1, phase_calls=2),
    lambda: gaussian_bank_tail(9, 1, "1/1024", 0),
))
def test_invalid_or_float_source_promises_and_impossible_call_counts_rejected(call):
    with pytest.raises(ValueError):
        call()
