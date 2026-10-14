"""Exact ternary multiples, actual original-data completion and adaptive verification."""
from dataclasses import replace
from fractions import Fraction
from itertools import product
import json
import subprocess

import pytest

from theorems import native_small_multiple_completion as S
from native_full_root_slice import source_data
from ternary_noise_degradation import NoisyLinearRecord


def raw(q=27, labels=((1,), (2,), (3,), (4,)), secret=(17,), errors=(0, 0, 0, 0)):
    return tuple(NoisyLinearRecord(a, (sum(x*y for x, y in zip(a, secret))+e) % q, q, f"source-{j}")
                 for j, (a, e) in enumerate(zip(labels, errors)))


@pytest.mark.parametrize("q", (3, 9, 27, 3**16, 3**64))
@pytest.mark.parametrize("c", (1, -1, 2, -2, 3, -3, 9, -27))
def test_true_multiple_exposes_exact_quotient_without_a_nonunit_inverse(q, c):
    if c % q == 0:
        with pytest.raises(ValueError): S.multiple_quotient(q, c, (0, 0))
        return
    secret = (q-1, q//2)
    w = tuple(c*x % q for x in secret)
    result = S.multiple_quotient(q, c, w)
    assert result.quotient_secret == tuple(x % result.remaining_modulus for x in secret)
    assert result.factor*result.remaining_modulus == q
    assert result.unit_coefficient % 3 != 0
    assert not result.record()["multiple_membership_in_original_secret_orbit_established"]


def test_nonunit_image_membership_and_zero_or_invalid_coefficients_are_distinct():
    assert S.multiple_quotient(27, 3, (1, 0)) is None
    for c in (0, 27, -54, True, 1.0):
        with pytest.raises(ValueError): S.multiple_quotient(27, c, (0, 0))
    for w in ((), (27,), (-1,), (True,)):
        with pytest.raises(ValueError): S.multiple_quotient(27, 1, w)


@pytest.mark.parametrize("q,c", ((27, 3), (27, -9), (81, 27), (3**64, -27)))
def test_all_original_rounding_noise_within_true_spacing_completes_missing_quotient(q, c):
    g = S.multiple_quotient(q, c, (0,)).factor
    Q = q//g
    limit = min(2, Q//2)
    for e in product(range(-limit, limit+1), repeat=2):
        data = raw(q, ((1,), (2,)), (q-2,), e)
        w = (c*(q-2) % q,)
        result = S.complete_multiple(data, c, w)
        assert result["candidate_secret"] == (q-2,)
        assert result["public_basis_model"]["composite_field_inverse_used"] is False
        assert result["original_response_residual_evaluations"] == 2
        assert not result["multiple_truth_premise_verified"]


def test_actual_wide_original_source_noisy_completions_do_not_read_secret_or_errors():
    c = S.control(3, 64, 16, True, 96003, (3, 9, -27))
    assert all(a["matches_truth_fixture"] for a in c["known_coefficient_completions"])
    assert not c["secret_or_errors_entered_completion"]
    assert c["multiple_inputs_prepared_from_truth_FOR_CALIBRATION_ONLY"]


@pytest.mark.parametrize("secret", (0, 3, 18))
def test_local_completion_does_not_require_a_primitive_planted_secret(secret):
    result = S.complete_multiple(raw(secret=(secret,), errors=(-1, 1, 0, 1)), 3, (3*secret % 27,))
    assert result["candidate_secret"] == (secret,)


def test_low_rank_bad_equations_and_wrong_cache_fail_without_guessing():
    constant = raw(labels=((0,), (0,)))
    result = S.complete_multiple(constant, 3, (0,))
    assert result["status"] == "ORIGINAL_LOW_LABEL_RANK_UNSUPPORTED_NOT_NO_SOLUTION"
    data = raw()
    w = (3*17 % 27,)
    good = S.complete_multiple(data, 3, w)
    changed = list(data);changed[-1] = replace(data[-1], value=(data[-1].value+9) % 27)
    bad = S.complete_multiple(changed, 3, w)
    assert bad["status"] == "INCONSISTENT_ROUNDED_MISSING_QUOTIENT" and bad["candidate_secret"] is None
    cache = S.PublicBasisCache(raw(labels=((2,), (1,), (3,), (4,))))
    with pytest.raises(ValueError, match="same actual"):
        S.complete_multiple(data, 3, w, cache)
    assert good["public_basis_model"]["label_only_basis_rows"] == (0,)


def test_label_aligned_noise_can_make_wrong_consistent_preimage_and_fit():
    data = raw()
    altered = tuple(replace(s, value=(s.value+9*s.label[0]) % 27) for s in data)
    result = S.complete_multiple(altered, 3, (3*17 % 27,))
    assert result["candidate_secret"] != (17,)
    assert result["status"] == "CONDITIONAL_ORIGINAL_BANK_MULTIPLE_COMPLETION"
    assert S.bounded_fit(altered, result["candidate_secret"], 0)["fits_public_radius"]
    assert not result["rounded_consistency_is_an_original_secret_certificate"]


def test_complete_unknown_coefficient_scan_cost_cache_and_preflight_exhaustion():
    data = raw(errors=(-1, 1, 0, -1))
    scan = S.scan_list(data, ((3*17 % 27,), (0,)), 3, 1)
    assert scan["planned_coefficient_trials"] == scan["trials_evaluated"] == 12
    assert [r["candidate_secret"] for r in scan["bounded_fit_candidates"]] == [(17,)]
    assert scan["original_records_paid_once"] == 4
    assert len(scan["public_basis_inversions"]) == 1
    assert scan["original_response_residual_evaluations"] == 16
    assert scan["original_candidate_verification_evaluations"] > 0
    cap = S.scan_list(data, ((0,),), 10**100, 1, max_trials=1)
    assert cap["effective_centered_coefficient_bound"] == 13
    assert cap["status"] == "COMPLETE_SCAN_CAP_EXCEEDED_NOT_NO_CANDIDATES"
    assert cap["trials_evaluated"] == 0
    assert not scan["list_coverage_or_decision_solver_supplied"]
    assert scan["public_verification_radius"] == 1 and scan["supplied_multiples"] == ((24,), (0,))
    assert scan["public_basis_rref_calls"] == scan["public_basis_inversion_calls"] == 1
    assert not scan["public_matrix_preprocessing_is_free"]


def test_wrong_or_uninformative_lists_keep_no_candidate_and_ambiguity_explicit():
    missing = S.scan_list(raw(), ((0,),), 1, 0)
    assert missing["status"] == "NO_BOUNDED_FIT_CANDIDATE_NOT_NO_SECRET"
    constant = raw(q=9, labels=((0,), (0,)), secret=(0,), errors=(0, 0))
    ambiguous = S.scan_list(constant, ((1,),), 1, 0)
    assert ambiguous["status"] == "AMBIGUOUS_BOUNDED_FIT_CANDIDATES"


@pytest.mark.parametrize("q,n", ((3, 2), (9, 2), (27, 1)))
def test_actual_difference_valuation_population_and_uniform_subgroup_small_ball(q, n):
    r = S.root_digits(q);R = 0 if q == 3 else 1
    ledger = S.separation_ledger(q, n, 20, R)
    for cert in ledger["valuation_small_ball_certificates"]:
        d, count = cert["difference_valuation"], 0
        for h in product(range(q), repeat=n):
            if not any(h): continue
            factor = 1
            while all(x % (factor*3) == 0 for x in h): factor *= 3
            if factor == 3**d: count += 1
        assert count == 3**((r-d)*n)-3**((r-d-1)*n)
        g, L = 3**d, 3**(r-d)
        outputs = [a*g % q for a in range(q)]
        p = Fraction(sum(min(x, q-x) <= 2*R for x in outputs), q)
        assert p == Fraction(cert["small_ball_numerator"], L)
        k, b = cert["power_negative_log2_floor"], cert["exact_probability_power_block"]
        assert 2**k*p.numerator**b <= p.denominator**b < 2**(k+1)*p.numerator**b


@pytest.mark.parametrize("R", (0, 1))
def test_full_original_label_census_obeys_global_union_not_fixed_candidate_sampling(R):
    c = S.code_census(9, 4, R)
    assert c["original_label_banks_checked"] == 6561
    assert Fraction(c["exact_separation_failure_probability"]) <= Fraction(c["ledger"]["global_code_separation_failure_upper_used"])
    assert c["ledger"]["separation_event_covers_all_secrets_and_adaptive_candidates"]
    assert not c["ledger"]["candidate_count_union_multiplier_required"]


def test_globally_separated_original_code_verifies_every_adaptive_candidate():
    q, labels, R = 9, ((1,), (2,), (3,), (4,)), 1
    assert all(any(min(a[0]*h % q, (-a[0]*h) % q) > 2*R for a in labels) for h in range(1, q))
    for truth, e in product(range(q), product(range(-R, R+1), repeat=4)):
        data = raw(q, labels, (truth,), e)
        survivors = [s for s in range(q) if S.bounded_fit(data, (s,), R)["fits_public_radius"]]
        assert survivors == [truth]


def test_uniform_source_event_does_not_condition_on_adaptively_selected_true_multiple():
    L = S.source_event_ledger(27, 2, 20, 2, 1, "1/2")
    assert L["uniform_good_original_error_threshold"] == 2
    assert Fraction(L["original_error_event_failure_upper"]) == 1
    assert not L["conditioning_on_data_selected_multiple_truth_used"]
    assert not L["original_errors_assumed_independent"]
    assert L["composed_recovery_failure_upper_IF_external_coverage_is_proved"] is None
    covered = S.source_event_ledger(3**32, 32, 2*33**3, 3**32//32, 3, Fraction(3**64, 3*32**6), "1/100")
    assert Fraction(covered["composed_recovery_failure_upper_IF_external_coverage_is_proved"]) < 1
    assert not covered["source_promises_or_published_reduction_applicability_established"]


def test_small_coefficient_size_does_not_guarantee_usable_valuation_or_nonvacuous_noise():
    n, q, m = 64, 3**64, 2*65**3
    V = Fraction(q*q, 3*n**6)+Fraction(1, 2)
    safe = S.source_event_ledger(q, n, m, q//n, 3, V)
    gap = S.coefficient_size_gap(q, n, m, q//n, V, n**9)
    assert Fraction(safe["uniform_local_event_failure_upper"]) < 1
    assert gap["worst_factor_local_source_event"]["original_error_event_failure_upper"] == "1"
    assert not gap["small_integer_coefficient_bound_guarantees_a_safe_valuation"]
    assert not gap["bound_is_derived_from_an_implemented_decision_reduction"]


@pytest.mark.parametrize("bad", ("radius", "valuation", "moment", "floating", "coverage", "cap", "reuse"))
def test_invalid_source_promises_and_unpaid_access_are_rejected(bad):
    with pytest.raises(ValueError):
        if bad == "radius": S.separation_ledger(9, 1, 2, 3)
        elif bad == "valuation": S.source_event_ledger(9, 1, 2, 1, 2, 1)
        elif bad == "moment": S.source_event_ledger(9, 1, 2, 1, 1, -1)
        elif bad == "floating": S.source_event_ledger(9, 1, 2, 1, 1, 0.1)
        elif bad == "coverage": S.source_event_ledger(9, 1, 2, 1, 1, 1, "2")
        elif bad == "cap": S.scan_list(raw(), ((0,),), 1, 0, 0)
        elif bad == "reuse": S.scan_list((raw()[0], raw()[0]), ((0,),), 1, 0)


def test_live_artifact_and_independent_checker():
    p = json.loads(S.REPORT.read_text())
    assert not p["accepted_speedup_candidate"] and not p["new_active_negative_result_created"]
    result = subprocess.run(["node", "research/certificates/native_small_multiple_completion_crosscheck.js"], cwd=S.ROOT, capture_output=True, text=True, check=True)
    assert json.loads(result.stdout)["verified"]


@pytest.mark.parametrize("tamper", ("multiple", "inverse", "noise_threshold", "small_ball", "preprocessing", "oracle"))
def test_independent_checker_rejects_false_multiple_or_source_event_evidence(tamper):
    p = json.loads(S.REPORT.read_text());c = p["original_data_controls"][0]
    if tamper == "multiple": c["known_coefficient_completions"][0]["completion"]["quotient_model"]["multiple_membership_in_original_secret_orbit_established"] = True
    elif tamper == "inverse": c["known_coefficient_completions"][2]["completion"]["public_basis_model"]["inverse"][0][0] += 1
    elif tamper == "noise_threshold": p["scaling_source_events_and_size_gaps"][0]["safe_valuation_source_ledger"]["uniform_good_original_error_threshold"] += 1
    elif tamper == "small_ball": p["complete_original_code_censuses"][0]["ledger"]["valuation_small_ball_certificates"][1]["small_ball_numerator"] += 1
    elif tamper == "preprocessing": c["unknown_coefficient_list_scan"]["public_matrix_preprocessing_is_free"] = True
    elif tamper == "oracle": c["unknown_coefficient_list_scan"]["list_coverage_or_decision_solver_supplied"] = True
    result = subprocess.run(["node", "-e", "require('./research/certificates/native_small_multiple_completion_crosscheck.js').verify(JSON.parse(require('fs').readFileSync(0,'utf8')))"],
        input=json.dumps(p), cwd=S.ROOT, capture_output=True, text=True)
    assert result.returncode != 0
