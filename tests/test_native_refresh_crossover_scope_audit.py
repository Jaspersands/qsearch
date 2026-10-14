from copy import deepcopy
from fractions import Fraction
import json
import subprocess

import pytest

from theorems import native_refresh_crossover_scope_audit as A


def stored():
    return json.loads(A.REPORT.read_text())


def node_check(payload):
    return subprocess.run([
        "node", "-e",
        "const A=require('./research/certificates/native_refresh_crossover_scope_audit_crosscheck.js');"
        "let s='';process.stdin.on('data',x=>s+=x);process.stdin.on('end',()=>console.log(JSON.stringify(A.verify(JSON.parse(s)))));",
    ], input=json.dumps(payload), text=True, capture_output=True, cwd=A.ROOT)


def test_profiles_have_disjoint_refresh_and_first_child_scopes():
    profiles = stored()["scaling_scope_audits"]
    assert [p["maximum_first_child_digits"] for p in profiles] == [5, 8]
    assert [p["declared_refresh_min_digits"] for p in profiles] == [9, 12]
    for p in profiles:
        assert p["reachable_refresh_digits"] == []
        assert p["jointly_covered_refresh_digits"] == []
        assert len(p["scope_issues"]) == 2
        assert p["composed_recovery_failure_upper_certified"] is None
        assert all(not r["covered_by_original_radius_nonwrapping_gate"] for r in p["refresh_root_checks"])


def test_scope_detector_does_not_automatically_reject_compatible_intervals():
    p = deepcopy(json.loads(A.INPUT.read_text())["composed_scaling_profiles"][0])
    p.update(min_refresh_root_digits=2, max_refresh_root_digits=4)
    audit = A.scope(p)
    assert audit["scope_issues"] == ()
    assert audit["jointly_covered_refresh_digits"] == (2, 3, 4)
    assert audit["composed_recovery_failure_upper_certified"] is None


@pytest.mark.parametrize("index", (0, 1))
def test_controls_are_matched_classically_without_later_candidates(index):
    control = stored()["original_baseline_controls"][index]
    out = A.compare_control(json.loads(A.INPUT.read_text())["actual_composed_pipeline_controls"][index])
    assert A.exact_json(out) == control
    baseline = control["original_baseline"]
    assert baseline["additional_producer_calls"] == baseline["additional_refresh_batches"] == 0
    assert control["same_calibration_secret_recovered_without_later_stages"]
    trials = baseline["root_candidate_completions"]
    assert trials[0]["candidate_secret"] is None
    assert all(t["candidate_secret"] == control["original_secret_FOR_POST_SOLVE_COMPARISON_ONLY"] for t in trials[1:])
    assert baseline["public_label_rank_calls"] > 0
    assert baseline["public_ring_inverse_calls"] > 0
    assert baseline["original_candidate_verification_evaluations"] > 0
    assert not control["calibration_dominance_proves_global_no_go"]


def test_false_unmask_receipt_is_not_trusted():
    control = deepcopy(json.loads(A.INPUT.read_text())["actual_composed_pipeline_controls"][0])
    control["pipeline_result"]["refresh_pruning_stages"][0]["unmask_receipts"][0]["unmasked_multiple"][0] += 1
    with pytest.raises(ValueError, match="unmask"):
        A.compare_control(control)


def test_dimension_free_implication_is_falsified_without_astronomical_execution():
    counter = stored()["dimension_counterprofile"]
    energy = counter["energy_crossover"]
    assert energy["beta_squared_lt_three_halves_delta_IF_H_terminal_nonpositive"]
    assert Fraction(energy["unclamped_energy_failure_bound"]) < Fraction(1, 100)
    assert Fraction(energy["terminal_beta"]) == Fraction(1, 10)
    assert Fraction(counter["no_correct_basis_probability_lower"]) > Fraction(99, 100)
    assert counter["dimension_free_high_probability_inference_falsified"]
    assert not counter["bank_was_executed"]
    assert not counter["current_n32_n128_lottery_profiles_falsified"]
    assert not counter["arbitrary_classical_or_quantum_decoder_lower_bound_proved"]
    assert A.verify_probability_boxes(stored())["verified"]


@pytest.mark.parametrize("args", (
    (128, 32, "1/1000", "1/4", "1/4", 5, 5),
    (128, 32, "1/1000", "1/4", "1/4", 2, 1),
    (128, 32, "0", "1/4", "1/4", 8, 2),
))
def test_invalid_crossover_parameters_rejected(args):
    with pytest.raises(ValueError):
        A.crossover_energy(*args)


def test_independent_js_replays_all_current_audit_records():
    r = node_check(stored())
    assert r.returncode == 0, r.stderr
    assert json.loads(r.stdout)["verified"]


@pytest.mark.parametrize("kind", (
    "scope-null", "scope-root", "scope-radius", "scope-reachable", "root-multiple",
    "baseline-result", "baseline-paid-rank", "counter-energy", "counter-exponent",
    "counter-bound", "counter-executed", "global-no-go", "producer-hash", "input-hash",
))
def test_independent_js_rejects_scope_execution_and_claim_tampering(kind):
    p = deepcopy(stored())
    scope, control, counter = p["scaling_scope_audits"][0], p["original_baseline_controls"][0], p["dimension_counterprofile"]
    if kind == "scope-null":
        scope["composed_recovery_failure_upper_certified"] = "1/100"
    elif kind == "scope-root":
        scope["maximum_first_child_digits"] += 1
    elif kind == "scope-radius":
        scope["recomputed_Gaussian_radius"] = "1"
    elif kind == "scope-reachable":
        scope["reachable_refresh_digits"] = [9]
    elif kind == "root-multiple":
        control["supplied_original_root_candidates"][0][1][0] += 1
    elif kind == "baseline-result":
        control["original_baseline"]["fitting_secrets"] = []
    elif kind == "baseline-paid-rank":
        control["original_baseline"]["public_label_rank_calls"] = 0
    elif kind == "counter-energy":
        counter["energy_crossover"]["H_min"] = "1"
    elif kind == "counter-exponent":
        counter["complete_probability_blocks"] = "0"
    elif kind == "counter-bound":
        counter["any_correct_basis_probability_upper"] = "1"
    elif kind == "counter-executed":
        counter["bank_was_executed"] = True
    elif kind == "global-no-go":
        p["general_source_refresh_or_quantum_no_go_claimed"] = True
    elif kind == "producer-hash":
        p["producer_sha256"] = "0" * 64
    else:
        p["reviewed_artifact_sha256"] = "0" * 64
    assert node_check(p).returncode != 0
