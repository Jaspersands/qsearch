from itertools import product
import json
import subprocess

from flint import fmpq
import numpy as np
import pytest

from native_noisy_indexed_access import indexed_access_profile
from native_noisy_phase_input import rounded_gaussian_quantum_profile
from ternary_measured_lattice_decoder import exact_json
from native_recovery_capacity import (
    REPORT, copy_recovery_capacity, generic_noise_incompatibility, indexed_recovery_capacity,
    minimum_exposure, signed_l1_ball,
)


@pytest.mark.parametrize("K", range(5))
@pytest.mark.parametrize("W", range(5))
def test_exact_integer_signature_count_matches_complete_bounded_enumeration(K, W):
    count = sum(sum(abs(x) for x in c) <= W for c in product(range(-W, W+1), repeat=K))
    result = signed_l1_ball(K, W)
    assert result["status"] == "EXACT_SIGNED_INTEGER_L1_BALL"
    assert result["count"] == count and not result["partial_count_promoted"]


def test_copy_only_nonvacuous_noise_profiles_cannot_promise_full_recovery():
    profile = rounded_gaussian_quantum_profile(64, 3**64, "1/1048576", 512)
    assert fmpq(profile["composed_success_loss_upper"]) < fmpq(1, 10**8)
    capacity = profile["full_recovery_capacity"]
    assert capacity["full_secret_recovery_success_upper"] == str(fmpq(1, 3**3584))
    assert not capacity["target_not_excluded_by_capacity"]
    assert capacity["minimum_qutrits_required_by_dimension"] == 4096
    assert not profile["nonvacuous_noise_bound_is_full_recovery_feasibility"]


def test_noisy_copy_capacity_is_unconditional_and_not_a_small_prior_gate():
    zero = copy_recovery_capacity(2, 9, 0)
    sufficient = copy_recovery_capacity(2, 9, 4)
    assert zero["full_secret_recovery_success_upper"] == "1/81"
    assert sufficient["target_not_excluded_by_capacity"]
    assert not sufficient["capacity_pass_is_receiver_existence_or_efficiency"]
    assert not sufficient["nonuniform_small_secret_prior_covered"]
    assert sufficient["applies_to_noisy_qutrits_and_arbitrary_collective_receiver"]


def test_large_weighted_queries_require_phase_signature_capacity_not_just_small_noise_loss():
    q = 3**64
    V = q*q*fmpq(1, 1048576)**2/3+fmpq(1, 2)
    for W in (128, 1024):
        p = indexed_access_profile(64, q, 512, V, (1,)*W)
        assert p["bound_is_nonvacuous"]
        assert not p["full_recovery_capacity"]["target_not_excluded_by_capacity"]
        assert p["full_recovery_capacity"]["also_applies_to_exact_noisy_bank_with_no_classical_value_leak"]
        assert not p["nonvacuous_noise_bound_is_full_recovery_feasibility"]
    assert signed_l1_ball(1024, 128)["count"].bit_length() == 693
    assert signed_l1_ball(1024, 1024)["count"].bit_length() == 2599


def test_finite_query_orbit_stays_in_public_monomial_span_despite_ancilla_mixing():
    q, n = 9, 2
    labels = ((1, 2), (4, 5), (2, 7), (8, 1))
    # One bank query on an index/qutrit register with a clean four-state ancilla.
    dimension, rng = 24, np.random.default_rng(133000)
    raw = rng.normal(size=(dimension, dimension))+1j*rng.normal(size=(dimension, dimension))
    mixing, _ = np.linalg.qr(raw)
    initial = np.ones(dimension)/np.sqrt(dimension)
    columns = []
    for secret in product(range(q), repeat=n):
        phases = (0, sum(a*b for a, b in zip(labels[0], secret)), sum(a*b for a, b in zip(labels[1], secret)),
                  0, sum(a*b for a, b in zip(labels[2], secret)), sum(a*b for a, b in zip(labels[3], secret)))
        diagonal = np.repeat(np.exp(2j*np.pi*np.array(phases)/q), 4)
        columns.append(mixing@(diagonal*initial))
    # Numerical conformance only; the general bound follows from the symbolic argument.
    assert np.linalg.matrix_rank(np.column_stack(columns), tol=1e-10) == 5
    # The signed-query envelope also allows inverse branches, unlike this forward-only control.
    capacity = indexed_recovery_capacity(n, q, 2, 1)
    assert capacity["ball"]["count"] == 9
    assert capacity["full_secret_recovery_success_upper"] == "1/9"


@pytest.mark.parametrize("n,q,M,target", ((1, 9, 1, "1/2"), (2, 9, 2, "1/2"), (64, 3**64, 512, "1/2")))
def test_minimum_exposure_has_exact_consecutive_boundary_certificates(n, q, M, target):
    result = minimum_exposure(n, q, M, target)
    threshold = fmpq(target)*q**n
    assert result["coefficient_ball_at_threshold"] >= threshold
    if result["minimum_exposure"]:
        assert result["coefficient_ball_before_threshold"] < threshold
    assert not result["necessary_condition_is_sufficient_for_receiver"]


def test_chance_guessing_does_not_need_any_query_even_with_zero_term_budget():
    result = minimum_exposure(2, 9, 1, "1/81", max_terms=0)
    assert result["minimum_exposure"] == 0 and result["coefficient_ball_at_threshold"] == 1
    result = indexed_recovery_capacity(2, 9, 1, 0, "1/81", max_terms=0)
    assert result["target_not_excluded_by_capacity"]


def test_global_noise_certificate_incompatibility_covers_all_weighted_exposures():
    q, alpha = 3**64, fmpq(1, 1048576)
    result = generic_noise_incompatibility(64, q, 512, q*q*alpha*alpha/3+fmpq(1, 2))
    assert result["global_incompatibility_certified"]
    assert result["last_exposure_before_proxy_reaches_one"] == 8973
    assert result["ball_at_boundary"]["count"].bit_length() == 5704
    B, lower = result["last_exposure_before_proxy_reaches_one"], fmpq(result["sqrt_upper_bound_lower_enclosure"])
    assert fmpq(result["ball_at_boundary"]["count"], q**64) <= B*lower
    assert not result["actual_noise_error_lower_bound_claimed"]
    assert not result["noisy_receiver_impossibility_claimed"]


def test_signed_ball_per_exposure_monotonicity_needed_by_global_witness():
    for K in range(2, 8):
        ratios = [fmpq(signed_l1_ball(K, W)["count"], W) for W in range(1, 16)]
        assert all(x <= y for x, y in zip(ratios, ratios[1:]))
    # It is FALSE for K1; the theorem must keep its K>=2 premise.
    assert fmpq(signed_l1_ball(1, 2)["count"], 2) < signed_l1_ball(1, 1)["count"]


def test_larger_bank_and_lower_noise_are_not_incorrectly_rejected_by_global_gate():
    q = 3**64
    for M, alpha in ((1024, fmpq(1, 1048576)), (512, fmpq(1, 16777216))):
        result = generic_noise_incompatibility(64, q, M, q*q*alpha*alpha/3+fmpq(1, 2))
        assert not result["global_incompatibility_certified"]
    zero_noise = generic_noise_incompatibility(2, 9, 2, 0)
    assert zero_noise["status"] == "NO_POSITIVE_PROXY_LOWER_ENCLOSURE"
    assert not zero_noise["global_incompatibility_certified"]


def test_caps_do_not_turn_partial_signature_counts_into_upper_bounds():
    ball = signed_l1_ball(100, 20, max_terms=10)
    assert ball["count"] is None and not ball["partial_count_promoted"]
    capacity = indexed_recovery_capacity(64, 3**64, 512, 1024, max_terms=10)
    assert capacity["full_secret_recovery_success_upper"] is None
    assert capacity["target_not_excluded_by_capacity"] is None and not capacity["unknown_is_capacity_pass"]
    minimum = minimum_exposure(64, 3**64, 512, max_terms=10)
    assert minimum["minimum_exposure"] is None and not minimum["unknown_is_receiver_feasible"]
    q = 3**64
    V = q*q*fmpq(1, 1048576)**2/3+fmpq(1, 2)
    noise = generic_noise_incompatibility(64, q, 512, V, max_terms=10)
    assert noise["status"] == "UNKNOWN_GLOBAL_INCOMPATIBILITY_TERM_CAP" and not noise["global_incompatibility_certified"]


@pytest.mark.parametrize("V,cap,status", (("1/2", 10, "NO_POSITIVE_PROXY_LOWER_ENCLOSURE"),
    (str((3**64)**2*fmpq(1, 1048576)**2/3+fmpq(1, 2)), 10, "UNKNOWN_GLOBAL_INCOMPATIBILITY_TERM_CAP")))
def test_independent_verifier_keeps_incomplete_global_witnesses_unknown(V, cap, status):
    result = exact_json(generic_noise_incompatibility(64, 3**64, 512, V, max_terms=cap))
    assert result["status"] == status
    helper = REPORT.parents[1]/"certificates/native_recovery_capacity_exact.js"
    script = "const H=require(process.argv[1]),C=require(require('path').join(require('path').dirname(process.argv[1]),'cyclotomic_exact.js'));const r=JSON.parse(process.argv[2]);H.incompatibility(r,64,3n**64n,512n,C.parse(r.source_integer_second_moment_upper));"
    subprocess.run(["node", "-e", script, str(helper), json.dumps(result)], capture_output=True, check=True)
    result["global_incompatibility_certified"] = True
    assert subprocess.run(["node", "-e", script, str(helper), json.dumps(result)], capture_output=True).returncode != 0


def test_independent_checker_replays_joint_capacity_and_live_source_profiles():
    result = subprocess.run(["node", str(REPORT.parents[1]/"certificates/native_recovery_capacity_crosscheck.js")], capture_output=True, text=True, check=True)
    result = json.loads(result.stdout)
    assert result["status"] == "PASS" and result["global_generic_ledger_incompatibilities"] == 1
    assert result["exact_ball_reference_controls"] == 25
    assert result["live_copy_profiles"] == 4 and result["live_query_profiles"] == 3


@pytest.mark.parametrize("mutation", ("copy_pass", "ball", "query_pass", "minimum", "proxy", "boundary", "no_go"))
def test_checker_rejects_falsely_feasible_parameters_or_overclaimed_no_go(tmp_path, mutation):
    r = json.loads(REPORT.read_text())
    if mutation == "copy_pass":
        r["copy_controls"][0]["target_not_excluded_by_capacity"] = True
    elif mutation == "ball":
        r["query_controls"][1]["ball"]["count"] = "1"
    elif mutation == "query_pass":
        r["query_controls"][2]["target_not_excluded_by_capacity"] = True
    elif mutation == "minimum":
        r["Gaussian_joint_profiles"][0]["indexed_minimum_exposure"]["minimum_exposure"] = 1
    elif mutation == "proxy":
        r["Gaussian_joint_profiles"][0]["generic_noise_incompatibility"]["sqrt_upper_bound_lower_enclosure"] = "1"
    elif mutation == "boundary":
        r["Gaussian_joint_profiles"][0]["generic_noise_incompatibility"]["ball_at_boundary"]["count"] = "0"
    else:
        r["general_noisy_quantum_lower_bound"] = True
    file = tmp_path/"forged.json"
    file.write_text(json.dumps(r))
    assert subprocess.run(["node", str(REPORT.parents[1]/"certificates/native_recovery_capacity_crosscheck.js"), str(file)], capture_output=True).returncode != 0


@pytest.mark.parametrize("call", (
    lambda: copy_recovery_capacity(0, 9, 1), lambda: copy_recovery_capacity(1, 9, True),
    lambda: copy_recovery_capacity(1, 9, 1, .5), lambda: indexed_recovery_capacity(1, 9, 0, 1),
    lambda: signed_l1_ball(2, -1), lambda: minimum_exposure(1, 10, 1),
    lambda: generic_noise_incompatibility(1, 9, 1, -1),
))
def test_invalid_or_floating_capacity_promises_fail_closed(call):
    with pytest.raises(ValueError):
        call()
