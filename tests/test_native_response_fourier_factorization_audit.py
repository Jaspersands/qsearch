"""Tests for response-phase Fourier factorization, 1-call autoregressive chain rule, and signed 2-call pinching."""
from copy import deepcopy
import json
import subprocess

import pytest

from theorems import native_response_fourier_factorization_audit as F


def stored():
    return json.loads(F.REPORT.read_text())


def node_check(payload):
    return subprocess.run(
        [
            "node",
            "-e",
            "const X=require('./research/certificates/native_response_fourier_factorization_audit_crosscheck.js');"
            "let s='';process.stdin.on('data',x=>s+=x);"
            "process.stdin.on('end',()=>console.log(JSON.stringify(X.verify(JSON.parse(s)))));",
        ],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        cwd=F.ROOT,
    )


def test_tensor_qutrit_two_call_readout_factorizes_into_O_M_site_marginals():
    rep = stored()
    ctrls = rep["tensor_qutrit_factorization_controls"]
    assert len(ctrls) == 3
    for c in ctrls:
        assert c["product_matches_full_path_sum_identically"]
        assert c["tensor_qutrit_schedule_classically_tractable_in_O_M"]
        assert c["product_of_marginals_all_outcomes"] == c["full_path_sum_all_outcomes"]
    assert ctrls[2]["differs_from_cyclic_F_D_when_M_ge_2"] is True


def test_one_call_cyclic_dft_satisfies_exact_autoregressive_chain_rule():
    rep = stored()
    ctrls = rep["one_call_cyclic_autoregressive_controls"]
    assert len(ctrls) == 3
    for c in ctrls:
        assert c["chain_rule_matches_full_cyclic_dft_identically"]
        assert c["one_call_cyclic_dft_classically_sampleable_in_O_M"]
        assert c["chain_rule_product_all_outcomes"] == c["full_cyclic_dft_1call_all_outcomes"]
        for tbl in c["autoregressive_conditional_tables"]:
            for pe in tbl["prefix_conditionals"]:
                assert pe["parseval_sum_equals_one"]


def test_signed_two_call_cyclic_schedule_matches_difference_pinching_and_cancels_diagonal():
    rep = stored()
    ctrls = rep["signed_two_call_cyclic_controls"]
    assert len(ctrls) == 3
    for c in ctrls:
        assert c["signed_pinching_matches_secret_sweep_identically"]
        assert c["diagonal_w_eq_v_zero_phase_path_count"] == c["word_dimension_D"]
        D = c["word_dimension_D"]
        from fractions import Fraction
        assert c["diagonal_fourier_component_weights"] == [[str(Fraction(1,D*D))]]*D
        assert c["diagonal_component_is_probability_lower_bound"] is False
        assert c["uniform_secret_mean_all_outcomes"] == c["difference_relation_pinched_all_outcomes"]
    assert ctrls[0]["signed_readout_differs_from_unsigned_readout"] is True
    assert ctrls[2]["signed_readout_differs_from_unsigned_readout"] is True


def test_actual_circuit_refutes_the_diagonal_probability_floor():
    import numpy as np
    D=3
    W=np.exp(2j*np.pi*np.outer(np.arange(D),np.arange(D))/D)/np.sqrt(D)
    phases=np.array((8,1,0))
    data=np.exp(2j*np.pi*phases/9)
    state=W.conj().T@(data.conj()*(W@(data/np.sqrt(D))))
    diagonal=sum(np.exp(2j*np.pi*w*w/D) for w in range(D))/D**1.5
    assert abs(diagonal)**2 == pytest.approx(1/9)
    assert abs(state[0])**2 < 1/9
    assert stored()["diagonal_floor_countercontrol"]["probability_floor_claim_refuted"] is True


def test_independent_js_checker_verifies_stored_report():
    r = node_check(stored())
    assert r.returncode == 0, r.stderr
    out = json.loads(r.stdout)
    assert out["verified"] is True
    assert out["tensor_controls"] == 3
    assert out["autoregressive_controls"] == 3
    assert out["signed_two_call_controls"] == 3
    assert out["accepted_speedup_candidate"] is False


@pytest.mark.parametrize(
    "kind",
    (
        "tensor-marginal",
        "tensor-product",
        "auto-cond",
        "auto-chain",
        "signed-obs",
        "signed-sweep",
        "signed-diag",
        "signed-fourier-diag",
        "signed-floor-countercontrol",
        "dequant-claim",
        "speedup-claim",
        "dependency",
        "hash",
    ),
)
def test_independent_js_checker_rejects_factorization_and_signed_pinching_tampering(kind):
    p = deepcopy(stored())
    t0 = p["tensor_qutrit_factorization_controls"][0]
    a0 = p["one_call_cyclic_autoregressive_controls"][0]
    s0 = p["signed_two_call_cyclic_controls"][0]

    if kind == "tensor-marginal":
        t0["single_qutrit_site_marginals"][0]["marginal_outcome_probabilities"][0] = ["0"]
    elif kind == "tensor-product":
        t0["product_of_marginals_all_outcomes"][0] = ["0"]
    elif kind == "auto-cond":
        a0["autoregressive_conditional_tables"][0]["prefix_conditionals"][0]["conditional_probabilities_v_k_0_1_2"][0] = ["0"]
    elif kind == "auto-chain":
        a0["chain_rule_product_all_outcomes"][0] = ["0"]
    elif kind == "signed-obs":
        s0["exact_observed_all_outcome_probabilities"][0] = ["0"]
    elif kind == "signed-sweep":
        s0["uniform_secret_mean_all_outcomes"][0] = ["0"]
    elif kind == "signed-diag":
        s0["diagonal_w_eq_v_zero_phase_path_count"] += 1
    elif kind == "signed-fourier-diag":
        s0["diagonal_fourier_component_weights"][0] = ["1/3"]
    elif kind == "signed-floor-countercontrol":
        p["diagonal_floor_countercontrol"]["exact_probability"] = ["1/3"]
    elif kind == "dequant-claim":
        p["this_finite_audit_supplies_polynomial_two_call_sampler"] = True
    elif kind == "speedup-claim":
        p["accepted_speedup_candidate"] = True
    elif kind == "dependency":
        p["dependency_sha256"]["native_response_path_valuation.py"] = "0" * 64
    else:
        p["producer_sha256"] = "0" * 64
    assert node_check(p).returncode != 0
