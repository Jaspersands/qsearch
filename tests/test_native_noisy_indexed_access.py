import json
import subprocess

from flint import fmpq
import numpy as np
import pytest

from native_noisy_indexed_access import REPORT, canonical_power, indexed_access_bound, indexed_recipe
from ternary_noise_degradation import NoisyLinearRecord


def test_known_noisy_preparation_inverse_has_correct_order_not_exact_ideal_access():
    q = 81
    F = np.array([[np.exp(2j*np.pi*i*j/3) for j in range(3)] for i in range(3)])/np.sqrt(3)
    ideal = np.diag([1, np.exp(2j*np.pi*17/q), np.exp(2j*np.pi*28/q)])
    actual = np.diag([1, np.exp(2j*np.pi*18/q), np.exp(2j*np.pi*27/q)])
    seed = np.array([1, 0, 0])
    U = actual@F
    inverse = F.conj().T@actual.conj().T
    assert np.linalg.norm(inverse@U@seed-seed) < 1e-15
    assert np.linalg.norm(actual.conj().T@F.conj().T@U@seed-seed) > .1
    assert np.linalg.norm(inverse@ideal@F@seed-seed) > .01
    assert np.linalg.norm(inverse@ideal@F@seed-seed) <= np.linalg.norm(actual-ideal, 2)+1e-15


def test_pointwise_query_hybrid_allows_shared_errors_but_charges_every_power():
    q, powers = 81, (1, -1, 3)
    ideal_phases, fixed_errors = np.array([0, 17, 28, 0, 41, 62]), np.array([0, 1, -1, 0, -1, 1])
    ideal = np.diag(np.exp(2j*np.pi*ideal_phases/q))
    actual = np.diag(np.exp(2j*np.pi*(ideal_phases+fixed_errors)/q))
    F = np.array([[np.exp(2j*np.pi*i*j/6) for j in range(6)] for i in range(6)])/np.sqrt(6)
    reference, noisy = np.ones(6)/np.sqrt(6), np.ones(6)/np.sqrt(6)
    for k in powers:
        reference = F@np.linalg.matrix_power(ideal, k)@reference
        noisy = F@np.linalg.matrix_power(actual, k)@noisy
    distance = np.sqrt(max(0, 1-abs(np.vdot(reference, noisy))**2))
    delta = np.linalg.norm(actual-ideal, 2)
    assert distance <= sum(abs(k) for k in powers)*delta+1e-14
    assert delta**2 <= 40*sum(fixed_errors**2)/q**2


def test_phase_powers_are_canonicalized_but_not_charged_only_as_one_gate():
    assert canonical_power(9, 9) == 0 and canonical_power(10, 9) == 1
    assert canonical_power(-10, 9) == -1 and canonical_power(8, 9) == -1
    short = indexed_access_bound(3**64, 512, 3**128*fmpq(1, 1048576)**2/3+fmpq(1, 2), (2**20,))
    assert short["nonidentity_phase_call_count"] == 1 and short["weighted_phase_exposure"] == 2**20
    assert short["complete_pre_rounding_success_loss_upper"] == "1"
    assert not short["fast_forwarded_power_costs_only_one_unit_of_noise_exposure"]


def test_identity_bank_queries_have_no_noise_or_gate_charge():
    b = indexed_access_bound(9, 8, "1/2", (9, -18, 0))
    assert b["weighted_phase_exposure"] == 0 and b["nonidentity_phase_call_count"] == 0
    assert b["complete_pre_rounding_success_loss_upper"] == "0"
    assert not b["chosen_label_oracle_supplied"]


def test_known_indexed_recipe_uses_original_values_not_unknown_secret_and_no_QRAM():
    samples = tuple(NoisyLinearRecord((i % 9,), (3*i+2) % 9, 9, str(i)) for i in range(6))
    forward, backward = indexed_recipe(samples, (2,), 1), indexed_recipe(samples, (2,), -1)
    assert forward["branch_count"] == 3 and forward["index_bits"] == 2
    for i, (a, b) in enumerate(zip(forward["reduction_side_multiplexor_branches"], backward["reduction_side_multiplexor_branches"])):
        assert all((x+y) % 9 == 0 for x, y in zip(a["scaled_known_phase_values"], b["scaled_known_phase_values"]))
        assert a["scaled_known_phase_values"] == tuple((samples[2*i+j].value+2*samples[2*i+j].label[0]) % 9 for j in range(2))
    assert "no QRAM" in forward["access_implementation"]
    assert not forward["source_moment_claimed_by_this_recipe"]
    assert all(x["access"] == "fixed-bank index; phase oracle only" for x in forward["receiver_public_bank"])


def test_exact_norm_upper_bound_interval_precision_scales_with_weighted_exposure():
    b = indexed_access_bound(3**300, 512, "1/2", (2**100,), failure_bits=120)
    lo, hi = fmpq(b["sqrt_of_RMS_upper_bound_lower_enclosure"]), fmpq(b["sqrt_of_RMS_upper_bound_upper_enclosure"])
    squared = fmpq(b["RMS_operator_error_squared_upper"])
    assert lo*lo <= squared <= hi*hi
    assert b["sqrt_interval_bits"] == 120+(4*2**100-1).bit_length()
    assert (hi-lo)*2**100 <= fmpq(1, 2**122)
    assert b["source_errors_are_fixed_across_reused_calls"]
    assert not b["noise_resampled_on_every_call"] and not b["independent_quantum_originals_created_by_reuse"]


def test_exact_checker_replays_fixed_bank_and_all_access_costs():
    r = subprocess.run(["node", str(REPORT.parents[1]/"certificates/native_noisy_indexed_access_crosscheck.js")], capture_output=True, text=True, check=True)
    r = json.loads(r.stdout)
    assert r["status"] == "PASS" and r["bound_controls"] == 7
    assert r["fixed_bank_recipes"] == 4 and r["known_angles"] == 24
    assert not r["ideal_source_inverse_supplied_exactly"]


@pytest.mark.parametrize("mutation", ("exposure", "root", "loss", "inverse", "chosen", "scaled_phase", "refresh"))
def test_access_checker_rejects_false_inverse_or_missing_phase_cost(tmp_path, mutation):
    r = json.loads(REPORT.read_text())
    if mutation == "exposure":
        r["Gaussian_moment_exposure_controls"][-1]["weighted_phase_exposure"] = 1
    elif mutation == "root":
        r["bounds"][1]["sqrt_of_RMS_upper_bound_upper_enclosure"] = "0"
    elif mutation == "loss":
        r["bounds"][0]["complete_pre_rounding_success_loss_upper"] = "0"
    elif mutation == "inverse":
        r["ideal_source_inverse_supplied_exactly"] = True
    elif mutation == "chosen":
        r["chosen_label_oracle_supplied"] = True
    elif mutation == "scaled_phase":
        r["multiplexor_recipes"][0]["reduction_side_multiplexor_branches"][0]["scaled_known_phase_values"][0] = 99
    else:
        r["bounds"][0]["noise_resampled_on_every_call"] = True
    file = tmp_path/"false.json"
    file.write_text(json.dumps(r))
    assert subprocess.run(["node", str(REPORT.parents[1]/"certificates/native_noisy_indexed_access_crosscheck.js"), str(file)], capture_output=True).returncode != 0


@pytest.mark.parametrize("call", (
    lambda: canonical_power(True, 9), lambda: indexed_access_bound(9, 1, .5, (1,)),
    lambda: indexed_access_bound(9, 1, -1, (1,)), lambda: indexed_access_bound(10, 1, 1, (1,)),
    lambda: indexed_recipe((NoisyLinearRecord((1,), 2, 9, "a"),)*2, (0,), 1),
))
def test_false_inputs_and_reused_original_bank_IDs_fail_closed(call):
    with pytest.raises(ValueError):
        call()
