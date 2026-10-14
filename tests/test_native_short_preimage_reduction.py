"""Original-data recovery is conditional on a paid, verified short-preimage helper."""
from copy import deepcopy
from dataclasses import replace
from fractions import Fraction
from itertools import product
import json
import subprocess

from flint import fmpq
import pytest

from theorems import native_short_preimage_reduction as R
from ternary_noise_degradation import NoisyLinearRecord


def chosen_label_fixture(secret, r, mask=None, error=0):
    """Easy deterministic reduction control, not an IID-label LWE instance."""
    q, n = 3**r, len(secret)
    mask = tuple(mask or (0,)*n)
    plan = R.probe_plan(n, q)
    records = []
    for j, p in enumerate(plan):
        label = p["frequency"]
        value = (sum(a*s for a, s in zip(label, secret))+error) % q
        for k in range(2):
            records.append(NoisyLinearRecord(label, value, q, f"chosen-{j}-{k}"))
    family = R.public_family(records, 1, len(plan))
    def helper(public, target):
        assert public == family
        j = next(j for j, p in enumerate(plan) if p["frequency"] == target)
        word = tuple(0 if k == j else 1 for k in range(len(plan)))
        return R.PreimageReceipt(public.fingerprint(), target, 0, word)
    return tuple(records), mask, family, helper


@pytest.mark.parametrize("r,n", ((1, 1), (2, 2), (4, 3), (64, 2)))
def test_complete_nonadaptive_reduction_recovers_zero_and_nonzero_without_secret_search(r, n):
    q = 3**r
    for secret in ((0,)*n, tuple((q-1-i) % q for i in range(n))):
        mask = tuple((i+7) % q for i in range(n))
        records, mask, family, helper = chosen_label_fixture(secret, r, mask)
        result = R.recover_with_helper(records, mask, 1, family.sites, helper)
        assert result["original_secret"] == secret
        assert result["masked_secret"] == tuple((s+m) % q for s, m in zip(secret, mask))
        assert result["helper_calls"] == n*r
        assert result["original_records_paid_once"] == 2*n*r
        assert not result["helper_label_only_independence_proved_by_API"]
        assert not result["helper_classical_polynomial_runtime_proved_by_receipts"]
        assert not result["new_quantum_algorithm_or_speedup"]


def test_public_family_has_labels_only_and_fingerprint_ignores_responses_masks_and_ids():
    records, _, family, _ = chosen_label_fixture((5, 0), 2)
    changed = tuple(replace(x, value=(x.value+1) % 9, source_id="other-"+x.source_id) for x in records)
    assert R.public_family(changed, 1, family.sites).fingerprint() == family.fingerprint()
    assert set(family.record()) == {"modulus", "dimension", "cohorts", "sites", "paired_labels",
                                    "responses_masks_source_IDs_and_errors_supplied"}
    assert not family.record()["responses_masks_source_IDs_and_errors_supplied"]
    changed = (replace(records[0], label=(1, 1)),)+records[1:]
    assert R.public_family(changed, 1, family.sites).fingerprint() != family.fingerprint()


@pytest.mark.parametrize("mutation", ("hash", "target", "word", "cohort", "type"))
def test_receipts_are_recomputed_not_trusted(mutation):
    _, _, family, helper = chosen_label_fixture((5,), 2)
    target = R.probe_plan(1, 9)[0]["frequency"]
    receipt = helper(family, target)
    bad = {"hash": replace(receipt, public_family_sha256="f"*64),
           "target": replace(receipt, target=(0,)),
           "word": replace(receipt, word=(1,)*family.sites),
           "cohort": replace(receipt, cohort=1), "type": receipt.__dict__}[mutation]
    with pytest.raises(ValueError):
        R.verify_receipt(family, target, bad)


def test_public_evaluation_rejects_mismatched_records_and_short_masks():
    records, mask, family, helper = chosen_label_fixture((5, 0), 2)
    target = R.probe_plan(2, 9)[0]["frequency"]
    receipt = helper(family, target)
    changed = (replace(records[0], label=(1, 1)),)+records[1:]
    with pytest.raises(ValueError, match="do not match"):
        R.evaluate_probe(changed, mask, family, target, receipt)
    with pytest.raises(ValueError, match="mask"):
        R.evaluate_probe(records, (), family, target, receipt)


def test_every_selector_has_actual_signed_response_and_bounded_ancestry():
    records = tuple(NoisyLinearRecord(a, v, 9, f"s-{j}") for j, (a, v) in enumerate(
        (((1, 2), 8), ((5, 6), 3), ((7, 4), 1), ((2, 0), 7))))
    mask, family = (3, 8), R.public_family(records, 1, 2)
    for word in product(range(3), repeat=2):
        target = family.frequency(0, word)
        receipt = R.PreimageReceipt(family.fingerprint(), target, 0, word)
        probe = R.evaluate_probe(records, mask, family, target, receipt)
        beta = tuple(w for t in word for w in ((1, 0), (-1, 1), (0, -1))[t])
        assert probe["signed_original_coefficients"] == beta
        assert probe["coefficient_squared_norm"] == sum(w*w for w in beta) <= 4
        assert target == tuple(sum(w*r.label[i] for w, r in zip(beta, records)) % 9 for i in range(2))
        assert probe["derived_masked_response"] == sum(w*(r.value+sum(a*m for a, m in zip(r.label, mask)))
                                                        for w, r in zip(beta, records)) % 9
        assert probe["active_original_source_IDs"] == tuple(r.source_id for w, r in zip(beta, records) if w)
        assert not probe["fresh_original_errors_created"]


def test_helpers_are_called_for_the_whole_fixed_batch_before_responses(monkeypatch):
    records, mask, family, helper = chosen_label_fixture((5, 8), 2)
    events, original = [], R.evaluate_probe
    def spy(public, target):
        events.append(("helper", target))
        return helper(public, target)
    def evaluate(*args):
        events.append(("response", args[3]))
        return original(*args)
    monkeypatch.setattr(R, "evaluate_probe", evaluate)
    result = R.recover_with_helper(records, mask, 1, family.sites, spy)
    assert result["original_secret"] == (5, 8)
    plan = [p["frequency"] for p in R.probe_plan(2, 9)]
    assert events == [("helper", t) for t in plan]+[("response", t) for t in plan]


@pytest.mark.parametrize("r", (1, 2, 3))
def test_every_secret_and_integer_error_strictly_below_q_over_six_decodes(r):
    q = 3**r
    for s, error in product(range(q), range(-q//6+1, q//6+1)):
        plan = R.probe_plan(1, q)
        probes = [{"requested_frequency": p["frequency"],
                   "derived_masked_response": (p["frequency"][0]*s+error) % q} for p in plan]
        result = R.decode_probe_values(probes, 1, q)
        assert result["masked_secret"] == (s,)


def test_large_noise_is_not_repaired_with_a_truth_oracle():
    records, mask, family, helper = chosen_label_fixture((0,), 2, error=2)
    result = R.recover_with_helper(records, mask, 1, family.sites, helper)
    assert result["original_secret"] != (0,)
    assert result["correctness_requires_the_stated_noise_bound"]


@pytest.mark.parametrize("kind", ("missing", "reordered", "random_frequency", "noninteger_response"))
def test_decoder_cannot_promote_partial_or_wrong_schedule(kind):
    probes = [{"requested_frequency": p["frequency"], "derived_masked_response": 0} for p in R.probe_plan(1, 9)]
    if kind == "missing": probes.pop()
    if kind == "reordered": probes.reverse()
    if kind == "random_frequency": probes[0]["requested_frequency"] = (2,)
    if kind == "noninteger_response": probes[0]["derived_masked_response"] = 0.0
    with pytest.raises(ValueError): R.decode_probe_values(probes, 1, 9)


def test_incomplete_helper_is_charged_not_promoted_to_recovery():
    records, mask, family, helper = chosen_label_fixture((5,), 2)
    result = R.recover_with_helper(records, mask, 1, family.sites,
                                   lambda f, t: None if t == (1,) else helper(f, t))
    assert result["status"] == "INCOMPLETE_SHORT_PREIMAGE_HELPER"
    assert result["original_secret"] is None and len(result["missing_probes"]) == 1
    assert result["helper_calls"] == 2 and result["original_records_paid_once"] == 4
    assert not result["partial_batch_promoted_to_recovery"]


def test_exhaustive_control_has_exponential_cost_and_enforces_cap():
    records, mask, family, _ = chosen_label_fixture((5,), 2)
    helper = R.BoundedExhaustiveLabelControl(family, word_cap=9)
    assert R.recover_with_helper(records, mask, 1, 2, helper)["original_secret"] == (5,)
    assert helper.cost()["word_evaluations"] == 9
    assert helper.cost()["word_work_is_exponential_in_sites"]
    assert not helper.cost()["polynomial_scalable_helper_supplied"]
    with pytest.raises(ValueError, match="finite cap"):
        R.BoundedExhaustiveLabelControl(family, word_cap=8)


@pytest.mark.parametrize("model", (R.LABEL_ONLY, R.GLOBAL_MOMENT))
def test_exact_moment_bounds_include_full_batch_helper_failure(model):
    L = R.noise_ledger(2, 81, 2, 5, "3/2", model=model, helper_failure_upper="1/7")
    source = Fraction(72*2*4*5*3, 2*81**2) if model == R.LABEL_ONLY else Fraction(144*2*25*3, 2*81**2)
    assert Fraction(L["source_failure_upper_unclipped"]) == source
    assert Fraction(L["complete_reconstruction_failure_upper"]) == min(1, source+Fraction(1, 7))
    assert L["original_error_independence_and_zero_mean_required"] == (model == R.LABEL_ONLY)
    assert not L["derived_probe_independence_required"]
    assert not L["fresh_source_noise_per_helper_call_required"]
    assert not L["efficient_original_problem_decoder_supplied"]


def test_global_moment_bound_covers_correlated_nonzero_mean_response_dependent_words():
    # Deterministic perfectly correlated errors need not be centred. Cauchy is pathwise.
    records, mask, family, _ = chosen_label_fixture((2,), 2)
    errors = (1, 1, 1, 1)
    for word in product(range(3), repeat=2):
        beta = tuple(w for t in word for w in ((1, 0), (-1, 1), (0, -1))[t])
        actual_squared = sum(b*e for b, e in zip(beta, errors))**2
        assert actual_squared <= 2*family.sites*sum(e*e for e in errors)
    L = R.noise_ledger(1, 9, 1, 2, 1, model=R.GLOBAL_MOMENT)
    assert L["marginal_original_second_moments_suffice_for_global_bound"]
    assert not L["original_errors_independent_of_labels_and_helper_coins_required"]


@pytest.mark.parametrize("bad", ({"moment": "-1"}, {"model": "silent IID"},
                                {"helper_failure_upper": "-1/2"}, {"helper_failure_upper": "2"}))
def test_noise_ledger_rejects_invalid_promises(bad):
    args = {"n": 1, "q": 9, "cohorts": 1, "sites": 2, "moment": 1, "model": R.LABEL_ONLY, **bad}
    with pytest.raises(ValueError): R.noise_ledger(**args)


def test_both_scaling_bounds_decrease_without_constructing_a_helper():
    for model in (R.LABEL_ONLY, R.GLOBAL_MOMENT):
        history = []
        for n in (8, 32, 64, 128):
            q, M = 3**n, n*n+24
            L = R.noise_ledger(n, q, 1, M, fmpq(q*q, 3*n**6)+fmpq(1, 2), model=model)
            history.append(Fraction(L["complete_reconstruction_failure_upper"]))
            assert not L["classical_polynomial_preimage_helper_supplied"]
            assert not L["quantum_preimage_algorithms_excluded"]
        assert all(b < a for a, b in zip(history, history[1:]))
        assert history[-1] < Fraction(1, 100)


def test_live_controls_keep_missing_frequencies_and_observed_noisy_failure():
    report = json.loads(R.REPORT.read_text())
    controls = report["bounded_original_data_controls"]
    assert any(c["matches_truth_fixture"] for c in controls)
    assert any(c["result"]["status"] == "INCOMPLETE_SHORT_PREIMAGE_HELPER" for c in controls)
    assert any(c["result"]["status"] == "COMPLETE_RECEIPT_CHECKED_CLASSICAL_RECONSTRUCTION"
               and not c["matches_truth_fixture"] for c in controls)
    assert not report["accepted_speedup_candidate"] and not report["new_active_negative_result_created"]


def test_independent_checker_accepts_live_report_and_rejects_forged_claims():
    checker = R.ROOT/"research/certificates/native_short_preimage_crosscheck.js"
    script = "const C=require(process.argv[1]);const p=JSON.parse(require('fs').readFileSync(process.argv[2]));C.verify(p);"
    proc = subprocess.run(["node", "-e", script, str(checker), str(R.REPORT)], capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr


@pytest.mark.parametrize("mutation", ("response", "word", "family", "helper_cost", "noise", "candidate", "scope", "missing"))
def test_independent_checker_rejects_tampered_reports(mutation, tmp_path):
    p = json.loads(R.REPORT.read_text())
    c = p["bounded_original_data_controls"][0]
    probe = c["result"]["completed_probe_receipts"][0]
    if mutation == "response": probe["derived_masked_response"] = (probe["derived_masked_response"]+1) % 3
    if mutation == "word": probe["receipt"]["word"][0] = (probe["receipt"]["word"][0]+1) % 3
    if mutation == "family": c["result"]["public_family_sha256"] = "f"*64
    if mutation == "helper_cost": c["helper_cost"]["word_evaluations"] = 1
    if mutation == "noise": p["scalable_source_helper_ledgers"][0]["source_failure_upper_unclipped"] = "0"
    if mutation == "candidate": p["accepted_speedup_candidate"] = True
    if mutation == "scope": p["general_quantum_fibre_processing_ruled_out"] = True
    if mutation == "missing": p["bounded_original_data_controls"][2]["result"]["missing_probes"] = []
    target = tmp_path/"forged.json"
    target.write_text(json.dumps(p))
    checker = R.ROOT/"research/certificates/native_short_preimage_crosscheck.js"
    proc = subprocess.run(["node", str(checker), str(target)], capture_output=True, text=True)
    assert proc.returncode != 0, mutation
