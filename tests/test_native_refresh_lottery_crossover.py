"""Tests for refresh-to-clean-basis crossover inequality and composed DAG pipeline."""
from copy import deepcopy
from fractions import Fraction
import json
import subprocess

import pytest

from theorems import native_refresh_lottery_crossover as C
from native_basis_lottery import _certificate_int


def stored():
    return json.loads(C.REPORT.read_text())


def records(rows):
    return tuple(
        C.NoisyLinearRecord(
            tuple(_certificate_int(a) for a in r["label"]),
            _certificate_int(r["value"]),
            _certificate_int(r["modulus"]),
            r["source_id"],
        )
        for r in rows
    )


def node_check(payload):
    return subprocess.run(
        [
            "node",
            "-e",
            "const X=require('./research/certificates/native_refresh_lottery_crossover_crosscheck.js');"
            "let s='';process.stdin.on('data',x=>s+=x);"
            "process.stdin.on('end',()=>console.log(JSON.stringify(X.verify(JSON.parse(s)))));",
        ],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        cwd=C.ROOT,
    )


@pytest.mark.parametrize(
    "m,k,a_orig,a_targ,d_min,d_term,eta_n",
    (
        (512, 32, "1/32768", "1/4", 8, 4, "1/4"),
        (4096, 32, "1/32768", "1/4", 9, 5, "1/4"),
        (8192, 64, "1/2097152", "1/4", 12, 8, "1/4"),
        (1024, 16, "1/65536", "1/8", 9, 6, "1/8"),
    ),
)
def test_parameter_free_crossover_inequality_holds_whenever_terminal_H_is_nonpositive(
    m, k, a_orig, a_targ, d_min, d_term, eta_n
):
    res = C.crossover_width_bound(m, k, a_orig, a_targ, d_min, d_term, eta_n)
    assert res["parameter_cancellation_verified"]
    assert res["terminal_H_is_nonpositive"]
    assert res["beta_squared_strictly_below_three_halves_delta_when_H_nonpositive"]
    beta_sq = Fraction(res["terminal_beta_squared"])
    delta = Fraction(res["unclamped_markov_delta_energy_at_g_min"])
    assert beta_sq == Fraction(res["exact_identity_6_delta_H_min_g_term_sq_over_m"])
    assert beta_sq < Fraction(3, 2) * delta


@pytest.mark.parametrize("index", (0, 1))
def test_actual_composed_pipeline_controls_recover_full_root_secret(index):
    ctrl = stored()["actual_composed_pipeline_controls"][index]
    raw = records(ctrl["original_records"])
    secret = tuple(_certificate_int(x) for x in ctrl["original_secret_FOR_CALIBRATION_ONLY"])
    pipe = ctrl["pipeline_result"]
    assert pipe["status"] == "COMPOSED_REFRESH_DAG_AND_TERMINAL_LOTTERY_RECOVERY"
    assert tuple(_certificate_int(x) for x in pipe["candidate_secret"]) == secret
    assert len(pipe["refresh_pruning_stages"]) == 2
    lot = pipe["terminal_lottery_stage"]
    assert lot["canonical_node_to_multiple_equivalence_verified"]
    assert not lot["further_source_refresh_used_at_terminal_node"]
    assert lot["basis_lottery_completion"]["trial_records"][0]["status"] == "SINGULAR_UNIT_MINOR_NOT_NO_SECRET"
    assert lot["basis_lottery_completion"]["trial_records"][1]["status"] == "ORIGINAL_RADIUS_FIT"


def test_composed_scaling_profiles_and_arb_probability_replay():
    rep = stored()
    profiles = rep["composed_scaling_profiles"]
    assert [p["dimension"] for p in profiles] == [32, 128]
    assert all(p["crossover_eliminates_small_root_refresh_vacuity"] for p in profiles)
    assert C.verify_probability_boxes(rep)["verified"] is True
    for p in profiles:
        assert Fraction(p["unconditioned_local_source_failure_union_upper"]) < Fraction(1, 15)
        assert not p["actual_quantum_decision_or_multiple_producer_supplied"]


def test_premature_high_root_lottery_and_below_floor_refresh_falsifiers():
    f = stored()["falsifiers"]
    prem = f["premature_high_root_lottery_falsifier"]
    assert prem["no_correct_basis_probability_lower_exceeds_99_percent"]
    assert not prem["skipping_refresh_descent_at_wide_root_works"]
    ctrl = f["below_floor_refresh_vacuous_but_lottery_succeeds_control"]
    assert ctrl["terminal_H_is_nonpositive"]
    assert Fraction(ctrl["terminal_beta_squared"]) < Fraction(ctrl["three_halves_delta_energy_upper"])


def test_validation_rejects_invalid_crossover_roots():
    with pytest.raises(ValueError):
        C.crossover_width_bound(512, 32, "1/32768", "1/4", 5, 5, "1/4")
    with pytest.raises(ValueError):
        C.crossover_width_bound(512, 32, "1/32768", "1/4", 2, 1, "1/4")


def test_independent_js_checker_verifies_stored_report():
    r = node_check(stored())
    assert r.returncode == 0, r.stderr
    out = json.loads(r.stdout)
    assert out["verified"] is True
    assert out["composed_controls"] == 2
    assert out["stages_replayed"] == 4
    assert out["multiple_producer_supplied"] is False


@pytest.mark.parametrize(
    "kind",
    (
        "stage-refresh",
        "stage-unmask",
        "stage-prune",
        "terminal-lottery-mult",
        "terminal-candidate",
        "crossover-H-min",
        "crossover-beta-sq",
        "crossover-three-halves",
        "profile-local-union",
        "profile-composed-union",
        "profile-elim-flag",
        "premature-lottery-flag",
        "producer-claim",
        "dependency",
        "hash",
    ),
)
def test_independent_js_checker_rejects_crossover_pipeline_and_claim_tampering(kind):
    p = deepcopy(stored())
    c0 = p["actual_composed_pipeline_controls"][0]["pipeline_result"]
    prof = p["composed_scaling_profiles"][0]
    cross = prof["refresh_to_lottery_crossover"]
    if kind == "stage-refresh":
        c0["refresh_pruning_stages"][0]["refresh_batch"]["public_producer_input_records"][0]["value"] ^= 1
    elif kind == "stage-unmask":
        c0["refresh_pruning_stages"][0]["unmask_receipts"][0]["unmasked_multiple"][0] ^= 1
    elif kind == "stage-prune":
        c0["refresh_pruning_stages"][0]["modulo_scale_pruning"]["surviving_canonical_child_count"] += 1
    elif kind == "terminal-lottery-mult":
        c0["terminal_lottery_stage"]["equivalent_original_multiple"][0] ^= 1
    elif kind == "terminal-candidate":
        c0["candidate_secret"][0] += 1
    elif kind == "crossover-H-min":
        cross["H_at_min_refresh_root"] = "1"
    elif kind == "crossover-beta-sq":
        cross["terminal_beta_squared"] = "0"
    elif kind == "crossover-three-halves":
        cross["three_halves_delta_energy_upper"] = "1"
    elif kind == "profile-local-union":
        prof["unconditioned_local_source_failure_union_upper"] = "0"
    elif kind == "profile-composed-union":
        prof["composed_failure_upper_IF_external_producer_meets_average_contract"] = "0"
    elif kind == "profile-elim-flag":
        prof["crossover_eliminates_small_root_refresh_vacuity"] = False
    elif kind == "premature-lottery-flag":
        p["falsifiers"]["premature_high_root_lottery_falsifier"]["skipping_refresh_descent_at_wide_root_works"] = True
    elif kind == "producer-claim":
        p["actual_quantum_decision_or_multiple_producer"] = True
    elif kind == "dependency":
        p["dependency_sha256"]["native_prefix_ambiguity_pruning.py"] = "0" * 64
    else:
        p["producer_sha256"] = "0" * 64
    assert node_check(p).returncode != 0
