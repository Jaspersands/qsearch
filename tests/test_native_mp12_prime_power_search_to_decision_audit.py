"""Tests for Micciancio-Peikert prime-power Hensel probes and sample expansion audit."""
from copy import deepcopy
from fractions import Fraction
import json
import subprocess

import pytest

from theorems import native_mp12_prime_power_search_to_decision_audit as M


def stored():
    return json.loads(M.REPORT.read_text())


def node_check(payload):
    return subprocess.run(
        [
            "node",
            "-e",
            "const X=require('./research/certificates/native_mp12_prime_power_search_to_decision_audit_crosscheck.js');"
            "let s='';process.stdin.on('data',x=>s+=x);"
            "process.stdin.on('end',()=>console.log(JSON.stringify(X.verify(JSON.parse(s)))));",
        ],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        cwd=M.ROOT,
    )


def test_hensel_probe_batch_control_preserves_true_digit_and_shifts_false_digit():
    ctrl = stored()["hensel_probe_batch_control"]
    s = ctrl["calibration_secret_FOR_DIAGNOSTIC_ONLY"]
    q = 27
    s_low = (s[0] % 3, s[1] % 3)
    rem_s = ((s[0] - s_low[0]) % q, (s[1] - s_low[1]) % q)

    true_b = ctrl["true_digit_probe_batch"]
    false_b = ctrl["false_digit_probe_batch"]
    assert not true_b["fresh_probe_randomness_is_a_fresh_original_sample"]

    # Original errors are (1, -1, 0), widen dithers are (1, -1, 0) -> sum is (2, -2, 0) mod 27
    expected_true_res = (2, 25, 0)
    for idx, rec in enumerate(true_b["probed_records"]):
        res = (rec["value"] - rec["label"][0] * rem_s[0] - rec["label"][1] * rem_s[1]) % q
        assert res == expected_true_res[idx]

    # False digit d=2 has d - true_d = 1, so shift is u * 9 mod 27 for u in (0, 1, 2)
    for idx, rec in enumerate(false_b["probed_records"]):
        res = (rec["value"] - rec["label"][0] * rem_s[0] - rec["label"][1] * rem_s[1]) % q
        assert (res - expected_true_res[idx]) % q == (idx * 9) % q


@pytest.mark.parametrize("r,l", ((2, 0), (2, 1), (3, 1)))
def test_complete_hensel_subgroup_censuses(r, l):
    c = M.complete_hensel_subgroup_census(r, l)
    q = 3 ** r
    assert c["true_digit_zero_shift_invariance_checks"] == q * q
    assert c["false_digit_subgroup_bijection_checks"] == 2 * q * q
    assert c["all_true_digits_preserve_error_law"]
    assert c["all_false_digits_biject_onto_order3_subgroup"]
    assert c["false_lower_prefix_invalidates_all_candidate_digits"] is (l >= 1)


def test_coupled_mp12_reduction_ledgers_and_sample_expansion():
    rep = stored()
    ledgers = rep["coupled_mp12_reduction_ledgers"]
    assert [l["dimension_n"] for l in ledgers] == [8, 32, 64, 128]
    # n=8 has excessive rounded-widening TV loss, so effective advantage is 0
    assert ledgers[0]["effective_decision_advantage_lower_after_widening_and_sampler"] == "0"
    assert ledgers[0]["sample_expansion_multiplier_over_single_query_bank"] is None
    for l in ledgers[1:]:
        assert not l["fixed_single_query_bank_suffices"]
        assert not l["actual_decision_algorithm_supplied"]
        assert Fraction(l["effective_decision_advantage_lower_after_widening_and_sampler"]) > 0
        assert l["sample_expansion_multiplier_over_single_query_bank"] > 100000
        assert (
            l["total_disjoint_original_search_samples_required"]
            == l["total_decision_oracle_queries"] * l["decision_rows_per_query_m_dec"]
        )


def test_independent_js_checker_verifies_stored_report():
    r = node_check(stored())
    assert r.returncode == 0, r.stderr
    out = json.loads(r.stdout)
    assert out["verified"] is True
    assert out["subgroup_censuses"] == 3
    assert out["coupled_ledgers"] == 4
    assert out["actual_decision_algorithm_supplied"] is False


@pytest.mark.parametrize(
    "kind",
    (
        "probe-label",
        "probe-value",
        "census-true-count",
        "census-false-count",
        "census-subgroup",
        "ledger-tv-round",
        "ledger-sampler-loss",
        "ledger-gamma-eff",
        "ledger-queries",
        "ledger-samples",
        "fixed-bank-flag",
        "decision-alg-flag",
        "dependency",
        "hash",
    ),
)
def test_independent_js_checker_rejects_mp12_probe_and_ledger_tampering(kind):
    p = deepcopy(stored())
    tb = p["hensel_probe_batch_control"]["true_digit_probe_batch"]
    c0 = p["complete_hensel_subgroup_censuses"][0]
    l1 = p["coupled_mp12_reduction_ledgers"][1]

    if kind == "probe-label":
        tb["probed_records"][0]["label"][0] = (tb["probed_records"][0]["label"][0] + 1) % 27
    elif kind == "probe-value":
        tb["probed_records"][0]["value"] = (tb["probed_records"][0]["value"] + 1) % 27
    elif kind == "census-true-count":
        c0["true_digit_zero_shift_invariance_checks"] += 1
    elif kind == "census-false-count":
        c0["false_digit_subgroup_bijection_checks"] += 1
    elif kind == "census-subgroup":
        c0["order_3_top_subgroup"][1] = 1
    elif kind == "ledger-tv-round":
        l1["rounded_input_widening_TV_upper"] = "0"
    elif kind == "ledger-sampler-loss":
        l1["per_query_dither_sampler_TV_loss_upper"] = "0"
    elif kind == "ledger-gamma-eff":
        l1["effective_decision_advantage_lower_after_widening_and_sampler"] = "1/2"
    elif kind == "ledger-queries":
        l1["total_decision_oracle_queries"] = 1
    elif kind == "ledger-samples":
        l1["total_disjoint_original_search_samples_required"] = 1
    elif kind == "fixed-bank-flag":
        p["fixed_single_query_bank_suffices"] = True
    elif kind == "decision-alg-flag":
        p["actual_decision_algorithm_supplied"] = True
    elif kind == "dependency":
        p["dependency_sha256"]["native_gaussian_dither_sampler.py"] = "0" * 64
    else:
        p["producer_sha256"] = "0" * 64
    assert node_check(p).returncode != 0
