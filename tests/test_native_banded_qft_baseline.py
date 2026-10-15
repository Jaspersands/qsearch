"""Independent circuit, exact marginals, accuracy, access and cost falsifiers."""
from dataclasses import replace
from fractions import Fraction
from itertools import product
from copy import deepcopy
import json
import random
import subprocess

import numpy as np
import pytest
from flint import ctx

from theorems import native_banded_qft_baseline as B
from theorems.native_full_root_slice import source_data


def dense_kernel(M, b):
    words = tuple(product(range(3), repeat=M))
    out = np.zeros((3 ** M, 3 ** M), complex)
    for vi, v in enumerate(words):
        for wi, w in enumerate(words):
            turn = sum(v[M - 1 - k] * w[ell] / 3 ** (ell - k + 1)
                       for k in range(M) for ell in range(k, min(M, k + b)))
            out[vi, wi] = np.exp(2j * np.pi * turn) / np.sqrt(3 ** M)
    return out


def independent_probabilities(phases, q, b, sign):
    M = len(phases)
    F = dense_kernel(M, b)
    eta = np.array([sum(phases[j][w[j]] for j in range(M)) for w in product(range(3), repeat=M)])
    d = np.exp(2j * np.pi * eta / q)
    state = F.conj().T @ (d ** sign * (F @ (d / np.sqrt(3 ** M))))
    return np.abs(state) ** 2


@pytest.mark.parametrize("M,b", ((1,1),(2,1),(2,2),(3,1),(3,2),(3,3)))
@pytest.mark.parametrize("sign", (-1,1))
def test_independent_unitary_circuit_distribution_matches_complete_integer_marginals(M,b,sign):
    phases = tuple(((j + 1) % 9, (2*j + 4) % 9, (6*j + 2) % 9) for j in range(M))
    F = dense_kernel(M,b)
    assert np.allclose(F.conj().T @ F, np.eye(3**M), atol=1e-13)
    model = B.BandedQFTBaseline(phases,9,b,sign,failure_bits=32)
    measured = np.array([float(model.prefix_probability(x)) for x in product(range(3),repeat=M)])
    reference = independent_probabilities(phases,9,b,sign)
    assert sum(model.prefix_probability(x) for x in product(range(3),repeat=M)) == 1
    assert np.abs(measured-reference).sum()/2 <= float(Fraction(model.ledger["per_complete_sample_TV_upper"])) + 1e-13


@pytest.mark.parametrize("q", (3,9,11,2**80+7))
def test_no_root_array_of_size_q_and_exact_modulus_arguments(q):
    model = B.BandedQFTBaseline(((q-1,1,0),(0,q-1,1)),q,2,failure_bits=12)
    assert len(model.roots) <= 9*model.M*3**model.b
    assert sum(model.prefix_probability(x) for x in product(range(3),repeat=2)) == 1
    assert model.stats["dense_word_rows_allocated"] == 0
    assert model.public_record()["modulus_q"] == str(q)
    assert all(type(x) is str for row in model.public_record()["public_digit_phase_tables"] for x in row)


def test_prefix_marginalization_and_adaptive_ternary_sampling_are_exact():
    model = B.BandedQFTBaseline(((8,1,0),(3,5,1),(4,0,5)),9,2,-1,failure_bits=20)
    for length in range(3):
        for prefix in product(range(3),repeat=length):
            assert sum(model.prefix_weight(prefix+(d,)) for d in range(3)) == model.prefix_weight(prefix)
    rng = random.Random(10011)
    output = model.sample_many(20,rng.getrandbits,record_trace=True)
    for sample in output["samples"]:
        for step in sample["trace"]:
            masses = tuple(map(int,step["child_weights"]))
            u = int(step["uniform_grid_integer"])
            d = step["selected_digit"]
            assert u*sum(masses) >= sum(masses[:d])*2**model.K
            assert u*sum(masses) < sum(masses[:d+1])*2**model.K
    assert model.stats["random_bits_consumed"] == 20*model.M*model.K


def test_low_phase_precision_is_a_measured_error_not_a_conditional_purity_claim():
    model = B.BandedQFTBaseline(((8,1,0),(5,3,1)),9,2,failure_bits=1)
    p = np.array([float(model.prefix_probability(x)) for x in product(range(3),repeat=2)])
    reference = independent_probabilities(model.phases,9,2,1)
    assert np.abs(reference-p).sum()/2 <= float(Fraction(model.ledger["per_complete_sample_TV_upper"]))
    assert model.ledger["rare_prefix_conditional_precision_assumed"] is False


def test_growing_sampler_never_calls_dense_word_rows(monkeypatch):
    from theorems import native_response_path_valuation as P
    def denied(*args,**kwargs):
        raise AssertionError("dense word enumeration forbidden")
    monkeypatch.setattr(P,"word_rows",denied)
    raw,mask,_,_=source_data(1,2,24,True,10012)
    model=B.BandedQFTBaseline.from_records(raw,mask,1,failure_bits=20)
    out=model.sample_many(1,random.Random(4).getrandbits)
    assert len(out["samples"][0]["site_digits_MSB_first"]) == 24
    assert model.stats["peak_boundary_states"] == 1
    assert model.stats["dense_word_rows_allocated"] == 0
    assert model.stats["window_evaluations"] <= (3*model.M+1)*model.M*27**model.b
    assert model.stats["maximum_integer_bits_seen"] <= model.public_record()["intermediate_integer_bits_upper"]


@pytest.mark.parametrize("policy,expected", (
    (replace(B.ContractionPolicy(),max_boundary_states=1),"BOUNDARY"),
    (replace(B.ContractionPolicy(),max_phase_entries=1),"PHASE_ENTRY"),
    (replace(B.ContractionPolicy(),max_enclosure_bits=16),"PRECISION"),
))
def test_source_preflight_caps_fail_closed(policy,expected):
    with pytest.raises(B.BaselineResourceLimit,match="UNKNOWN_.*"+expected):
        B.BandedQFTBaseline(((8,1,0),(0,1,8)),9,2,policy=policy)


def test_whole_batch_work_preflight_precedes_every_random_bit():
    model=B.BandedQFTBaseline(((8,1,0),(0,1,8)),9,2,
        policy=replace(B.ContractionPolicy(),max_total_window_evaluations=1))
    def denied(bits):
        raise AssertionError("not one output random bit may be drawn")
    with pytest.raises(B.BaselineResourceLimit,match="UNKNOWN_COMPLETE_SAMPLE_WORK_CAP"):
        model.sample_many(2,denied)
    assert model.stats["random_bits_consumed"]==0


def test_phase_enclosures_restore_library_context():
    precision=ctx.prec
    model=B.BandedQFTBaseline(((8,1,0),),9,1)
    assert ctx.prec==precision
    for receipt in model.roots.values():
        assert Fraction(receipt["Arb_complex_l1_error_upper"])<=Fraction(4,2**model.P)
        assert receipt["enclosure_bits"]<=model.policy.max_enclosure_bits


@pytest.mark.parametrize("M,f", ((1,1),(2,32),(64,40),(1024,128)))
def test_global_error_budget_has_linear_bits_and_explicit_grid_coupling(M,f):
    L=B.error_ledger(M,f)
    assert Fraction(L["per_complete_sample_TV_upper"])<=Fraction(1,2**f)
    assert L["phase_grid_bits_P"]<=2*M+f+B.ceil_log2(M)+6
    assert L["random_bits_per_digit_K"]==f+B.ceil_log2(4*M)


@pytest.mark.parametrize("ph,q,b,sign", (((),9,1,1),(((9,1,0),),9,1,1),
    (((0,1,2),),1,1,1),(((0,1,2),),9,2,1),(((0,1,2),),9,1,0),
    (((True,1,2),),9,1,1),(((0,1,2),),9,1,True)))
def test_invalid_public_schemas_rejected(ph,q,b,sign):
    with pytest.raises(ValueError): B.BandedQFTBaseline(ph,q,b,sign)


def test_invalid_prefixes_and_random_bit_sources_are_not_guessed():
    model=B.BandedQFTBaseline(((8,1,0),),9,1)
    for prefix in ((3,),(0,1),(True,)):
        with pytest.raises(ValueError): model.prefix_weight(prefix)
    with pytest.raises(ValueError,match="K-bit"):
        model.sample_many(1,lambda K:2**K)


@pytest.mark.parametrize("M,b", ((2,1),(3,1),(3,2),(4,1),(4,2),(4,3)))
def test_qutrit_QFT_omission_telescope_dominates_independent_operator_norm(M,b):
    F=dense_kernel(M,M);G=dense_kernel(M,b)
    omitted=sum((Fraction(M-d,3**(d+1)) for d in range(b,M)),Fraction(0))
    bound=Fraction(176,7)*omitted
    assert np.linalg.norm(F-G,ord=2)<=float(bound)+1e-13


@pytest.mark.parametrize("M,f", ((1,1),(2,8),(32,2),(64,20),(1024,10)))
def test_full_cyclic_cutoff_charges_both_transforms_and_total_accuracy(M,f):
    L=B.cyclic_cutoff_ledger(M,f)
    assert Fraction(L["complete_full_cyclic_sample_TV_upper"])<=Fraction(1,2**f)
    assert L["forward_and_adjoint_QFTs_charged"]==2
    b=L["selected_bandwidth_b"]
    assert b<=M
    if b<M: assert 3**b>=64*M*2**f>3**(b-1)
    assert L["exact_untruncated_sampler_supplied"] is False


def test_full_cyclic_wrapper_executes_small_distribution_and_caps_large_before_bits():
    model=B.FullCyclicQFTBaseline(((8,1,0),(2,3,4)),9,-1,failure_bits=8)
    assert model.banded.b==2
    result=model.sample_many(3,random.Random(1).getrandbits,record_trace=True)
    assert result["target_distribution"]=="IDEAL_FULL_CYCLIC_TWO_CALL_QFT_BORN_DISTRIBUTION"
    assert Fraction(result["joint_batch_TV_upper_under_IID_bits"])<=Fraction(3,256)
    with pytest.raises(B.BaselineResourceLimit,match="UNKNOWN_BOUNDARY_STATE_CAP"):
        B.FullCyclicQFTBaseline(((0,1,8),)*64,9,failure_bits=20)


def node_check(payload):
    return subprocess.run(["node","-e",
        "const X=require('./research/certificates/native_banded_qft_baseline_crosscheck.js');"
        "let s='';process.stdin.on('data',x=>s+=x);"
        "process.stdin.on('end',()=>console.log(JSON.stringify(X.verify(JSON.parse(s)))));"],
        input=json.dumps(payload),text=True,capture_output=True,cwd=B.ROOT)


def test_independent_phase_and_exact_marginal_replay():
    report=json.loads(B.REPORT.read_text())
    result=node_check(report)
    assert result.returncode==0,result.stderr
    assert json.loads(result.stdout)["independent_transcendental_phase_certificates"] is True


@pytest.mark.parametrize("kind", ("phase","mass","grid","width","truth","budget","hash","sampling",
                                  "cyclic-budget","cyclic-call-count"))
def test_independent_checker_rejects_tampering(kind):
    report=json.loads(B.REPORT.read_text())
    C=report["controls"][0];model=C["model"]
    if kind=="phase":
        root=model["phase_grid"][0]
        root["integer_value"][0]=str(int(root["integer_value"][0])+2**model["accuracy_ledger"]["phase_grid_bits_P"])
    elif kind=="mass": C["small_calibration_only_all_outcome_probabilities"][0]="0"
    elif kind=="grid": C["sampling"]["samples"][0]["trace"][0]["uniform_grid_integer"]="-1"
    elif kind=="width": model["max_prefix_boundary_states_upper"]+=1
    elif kind=="truth": model["observed_work"]["hidden_truth_used"]=True
    elif kind=="budget": model["accuracy_ledger"]["per_complete_sample_TV_upper"]="0"
    elif kind=="sampling": C["sampling"]["samples"][0]["trace"][0]["selected_digit"]=3
    elif kind=="cyclic-budget": report["full_cyclic_approximation_profiles"][2]["joint_Born_TV_truncation_upper"]="0"
    elif kind=="cyclic-call-count": report["full_cyclic_approximation_profiles"][2]["forward_and_adjoint_QFTs_charged"]=1
    else: report["producer_sha256"]="0"*64
    assert node_check(report).returncode!=0
