from dataclasses import replace
from itertools import product
import json
import random
import subprocess

import numpy as np
import pytest

from native_echo_history_receiver import ROOT, REPORT, EchoSchedule, history_baseline
from native_partial_phase_echo import EchoFamily, F3, bounded_score
from ternary_covariant_noise import phase


def schedule(q=9,n=1,M=3,w=1,d=3,seed=519):
    rng=random.Random(seed)
    first=tuple(tuple(rng.randrange(q) for _ in range(n)) for _ in range(M))
    second=tuple(tuple(rng.randrange(q) for _ in range(n)) for _ in range(M))
    Ks=tuple(tuple(tuple(rng.randrange(q) for _ in range(n)) for _ in range(n)) for _ in range(d))
    eta=tuple(tuple(rng.randrange(q) for _ in range(2)) for _ in range(M))
    return EchoSchedule(EchoFamily(first,second,q,w,Ks[0],eta),Ks)


@pytest.mark.parametrize("q,n,M,w,d", [(3,1,2,1,1),(9,1,3,1,2),(9,1,3,1,3),(3,2,3,1,3),(3,1,3,2,2)])
def test_every_original_probability_matches_independent_history_contraction(q,n,M,w,d):
    s=schedule(q,n,M,w,d)
    for secret in product(range(q),repeat=n):
        dense=s.dense_output(secret)
        streamed=np.array([s.amplitude(secret,out) for out in product(range(3),repeat=M)])
        assert np.allclose(dense,streamed,atol=4e-13)
        assert np.isclose(np.vdot(dense,dense),1,atol=3e-13)


def test_one_round_reduces_to_existing_actual_receiver():
    s=schedule(d=1)
    f=replace(s.source,coupling=s.couplings[0])
    for secret in range(9):
        assert np.allclose(s.dense_output((secret,)),f.dense_output((secret,)),atol=2e-13)
        for out in product(range(3),repeat=3):
            assert np.isclose(s.amplitude((secret,),out),f.amplitude((secret,),out),atol=2e-13)


@pytest.mark.parametrize("d", [1,2,3,4])
def test_zero_lenses_expose_fourier_parity_and_do_not_invent_information(d):
    s=schedule(d=d)
    zero=((0,),)
    s=EchoSchedule(s.source,(zero,)*d)
    result=bounded_score(s)
    if d%2==0:
        assert np.isclose(result["full_uniform_secret_MAP_success_numeric_reference"],1/9)
        assert np.isclose(result["least_trit_MAP_success_numeric_reference"],1/3)
    else:
        f=replace(s.source,coupling=zero)
        assert np.isclose(result["full_uniform_secret_MAP_success_numeric_reference"],bounded_score(f)["full_uniform_secret_MAP_success_numeric_reference"])


def dephased_physical_readout(s,secret):
    f=s.source
    A=tuple(product(range(3),repeat=f.main_width))
    B=tuple(product(range(3),repeat=f.mediator_width))
    words=tuple(a+b for a in A for b in B)
    psi=np.array([phase(sum(x*y for x,y in zip(secret,f.frequency(w)))-f.setting_phase(w),f.modulus) for w in words])/np.sqrt(3**f.copies)
    rho=np.outer(psi,psi.conj())
    U_A=F3
    for _ in range(f.main_width-1):
        U_A=np.kron(U_A,F3)
    U_B=F3
    for _ in range(f.mediator_width-1):
        U_B=np.kron(U_B,F3)
    indices=np.arange(3**f.copies)%len(B)
    for K in s.couplings:
        rho*=indices[:,None]==indices[None,:]
        lens=replace(f,coupling=K)
        D=np.diag([phase(lens.bilinear(f.frequency(a),f.frequency(b,f.main_width)),f.modulus) for a in A for b in B])
        U=np.kron(np.eye(len(A)),U_B)@D.conj()@np.kron(U_A,np.eye(len(B)))@D
        rho=U@rho@U.conj().T
    return np.diag(rho).real


@pytest.mark.parametrize("d", [1,2,3])
def test_full_word_history_dephasing_and_matched_LOCC_are_physical(d):
    s=schedule(q=3,M=3,d=d)
    result,dirty=history_baseline(s)
    for secret in range(3):
        physical=dephased_physical_readout(s,(secret,))
        assert np.allclose(physical,dirty[secret],atol=3e-13)
        assert np.isclose(sum(physical),1)
        assert np.all(abs(s.dense_output((secret,)))**2<=s.histories*physical+3e-13)
    assert result["dephased_full_B_WORD_history_MAP_success"]<=result["A_only_random_history_recorded_MAP_success"]+3e-13
    assert result["A_only_random_history_recorded_MAP_success"]<=result["full_uniform_secret_MAP_success_numeric_reference"]+3e-13
    assert result["same_original_native_copies"]==s.copies
    assert not result["classical_simulation_without_unknown_input_states_claimed"]
    assert not result["efficient_unknown_secret_decoder_supplied"]


def test_clean_ledger_counts_rounds_NOT_new_copies_and_charges_contraction():
    s=schedule(M=4,w=2,d=3)
    r=s.recipe()
    assert r["original_native_source_copies"]==4
    assert r["individual_inverse_F3_operations"]==12
    assert r["mediator_history_count"]==729
    assert r["frequency_scratch_cleared_before_EVERY_mediator_Fourier"]
    assert not r["has_single_echo_architecture"]
    assert r["A_independence_of_coupling_is_NOT_inferred_from_schedule"]
    with pytest.raises(ValueError,match="complete"):
        s.amplitude((0,),(0,0,0,0),history_budget=728)
    with pytest.raises(ValueError,match="complete"):
        history_baseline(s,history_budget=728)


@pytest.mark.parametrize("couplings", [(),(((1,2),),),(((True,),),)])
def test_invalid_public_schedules_are_rejected(couplings):
    with pytest.raises(ValueError):
        EchoSchedule(schedule().source,couplings)


def test_empty_schedule_iterators_and_partial_mediator_histories_are_rejected():
    with pytest.raises(ValueError):
        EchoSchedule(schedule().source,iter(()))
    s=schedule(w=2,M=4,d=2)
    with pytest.raises(ValueError):
        s.local_history_unitaries(((0,),(0,)))
    with pytest.raises(ValueError):
        s.local_history_unitaries(((True,0),(0,0)))


def test_zero_lens_three_rounds_matches_history_LOCC_after_output_relabeling():
    s=schedule()
    s=EchoSchedule(s.source,(((0,),),)*3)
    score=bounded_score(s)
    baseline,_=history_baseline(s)
    for key in ("full_uniform_secret_MAP_success_numeric_reference","least_trit_MAP_success_numeric_reference"):
        assert np.isclose(score[key],baseline[key],atol=3e-13)


def test_live_nonproduct_controls_are_negative_and_keep_resource_and_decoder_debts():
    report=json.loads(REPORT.read_text())
    assert len(report["cohorts"])==12
    records=[r for c in report["cohorts"] for r in c["records"]]
    assert len(records)==120
    for r in records:
        f=r["schedule"]["source"]
        assert r["schedule"]["recipe"]["mediator_history_count"]==3**(3*f["mediator_width"])
        assert r["matched_history_LOCC"]["same_original_native_copies"]==len(f["first_frequencies"])
        assert not r["score"]["efficient_unknown_secret_decoder_supplied"]
        if r["receiver_policy"]!="product_three_rounds":
            assert r["full_MAP_minus_OWN_LOCC"]<0
            assert r["least_trit_MAP_minus_OWN_LOCC"]<0
    assert not report["new_speedup_claimed"]
    assert not report["candidate_accepted"]


def test_independent_exact_clean_channel_and_domination():
    result=subprocess.run(["node",str(ROOT/"research/certificates/native_echo_history_receiver_crosscheck.js")],capture_output=True,text=True,check=True)
    out=json.loads(result.stdout)
    assert out["exactProbabilities"]==2430
    assert out["exactWinnerChecks"]==2430
    assert out["exactDominationChecks"]==2430
    assert out["baseline_MAP_scores"].startswith("numerical")


@pytest.mark.parametrize("tamper", ["promotion","oracle","score"])
def test_independent_checker_rejects_false_research_artifacts(tmp_path,tamper):
    report=json.loads(REPORT.read_text())
    if tamper=="promotion":
        report["candidate_accepted"]=True
    elif tamper=="oracle":
        report["exact_checker_control"]["records"][0]["schedule"]["recipe"]["unknown_source_preparation_inverse_used"]=True
    else:
        report["exact_checker_control"]["records"][0]["score"]["full_uniform_secret_MAP_success_numeric_reference"]+=.02
    path=tmp_path/"tampered.json"
    path.write_text(json.dumps(report))
    result=subprocess.run(["node",str(ROOT/"research/certificates/native_echo_history_receiver_crosscheck.js"),str(path)],capture_output=True,text=True)
    assert result.returncode!=0
