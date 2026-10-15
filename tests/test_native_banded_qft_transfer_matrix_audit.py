"""Tests for banded cyclic QFT two-call transfer-matrix contraction and scaling ledgers."""
from copy import deepcopy
import json
import subprocess

import pytest

from theorems import native_banded_qft_transfer_matrix_audit as B


def stored():
    return json.loads(B.REPORT.read_text())


def node_check(payload):
    return subprocess.run(
        [
            "node",
            "-e",
            "const X=require('./research/certificates/native_banded_qft_transfer_matrix_audit_crosscheck.js');"
            "let s='';process.stdin.on('data',x=>s+=x);"
            "process.stdin.on('end',()=>console.log(JSON.stringify(X.verify(JSON.parse(s)))));",
        ],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        cwd=B.ROOT,
    )


def test_banded_qft_transfer_matrix_matches_brute_force_and_full_cyclic_at_b_eq_M():
    ctrl = stored()["banded_qft_m2_sweep_control"]
    sweeps = ctrl["bandwidth_and_sign_sweeps"]
    assert len(sweeps) == 4
    for s in sweeps:
        assert s["dp_matches_brute_force_identically"]
        assert s["transfer_matrix_dp_all_outcomes"] == s["brute_force_path_sum_all_outcomes"]
        assert s["dp_window_evaluations_per_outcome"] <= s["dp_window_evaluations_upper_bound_M_times_3_pow_b"]
    assert ctrl["b1_differs_from_b2_unsigned"] is True
    assert ctrl["b1_differs_from_b2_signed"] is True
    assert sweeps[1]["matches_untruncated_cyclic_qft_when_b_eq_M"] is True


def test_bandwidth_scaling_ledgers_verify_O_M_3_pow_b_bound():
    ledgers = stored()["bandwidth_scaling_ledgers"]
    assert len(ledgers) == 7
    for l in ledgers:
        M = l["word_sites_M"]
        b = l["twiddle_bandwidth_b"]
        assert l["dp_within_M_3_pow_b_bound"]
        assert l["transfer_matrix_boundary_states_3_pow_b_minus_1"] == 3 ** (b - 1)
        assert l["exact_dp_window_evaluations_per_outcome"] <= M * (3 ** b)
    with pytest.raises(ValueError):
        B.bandwidth_scaling_ledger(4, 5)


def test_independent_js_checker_verifies_stored_report():
    r = node_check(stored())
    assert r.returncode == 0, r.stderr
    out = json.loads(r.stdout)
    assert out["verified"] is True
    assert out["sweeps_checked"] == 4
    assert out["scaling_profiles"] == 7
    assert out["accepted_speedup_candidate"] is False


@pytest.mark.parametrize(
    "kind",
    (
        "dp-outcome",
        "brute-outcome",
        "win-evals",
        "boundary-states",
        "b1-diff-flag",
        "scaling-dp-wins",
        "scaling-gates",
        "poly-m-claim",
        "three-call-claim",
        "speedup-claim",
        "dependency",
        "hash",
    ),
)
def test_independent_js_checker_rejects_banded_qft_and_scaling_tampering(kind):
    p = deepcopy(stored())
    s0 = p["banded_qft_m2_sweep_control"]["bandwidth_and_sign_sweeps"][0]
    sc0 = p["bandwidth_scaling_ledgers"][0]

    if kind == "dp-outcome":
        s0["transfer_matrix_dp_all_outcomes"][0] = ["0"]
    elif kind == "brute-outcome":
        s0["brute_force_path_sum_all_outcomes"][0] = ["0"]
    elif kind == "win-evals":
        s0["dp_window_evaluations_per_outcome"] += 1
    elif kind == "boundary-states":
        s0["max_transfer_matrix_boundary_states_3_pow_b_minus_1"] += 1
    elif kind == "b1-diff-flag":
        p["banded_qft_m2_sweep_control"]["b1_differs_from_b2_unsigned"] = False
    elif kind == "scaling-dp-wins":
        sc0["exact_dp_window_evaluations_per_outcome"] += 1
    elif kind == "scaling-gates":
        sc0["qft_twiddle_gates_count"] += 1
    elif kind == "poly-m-claim":
        p["full_bandwidth_b_eq_M_is_poly_M"] = True
    elif kind == "three-call-claim":
        p["three_or_more_calls_contracted_by_2call_dp"] = True
    elif kind == "speedup-claim":
        p["accepted_speedup_candidate"] = True
    elif kind == "dependency":
        p["dependency_sha256"]["native_response_path_valuation.py"] = "0" * 64
    else:
        p["producer_sha256"] = "0" * 64
    assert node_check(p).returncode != 0
