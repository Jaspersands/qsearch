from copy import deepcopy
from fractions import Fraction
from itertools import product
import json
from pathlib import Path
import subprocess
import sys

import numpy as np
import pytest
from scipy.linalg import hadamard

from theorems.dcp_complex_axis_readout import (
    REPORT, alias_metrics, axis_ensemble, build_report, exact_coarse_norm,
    feedback_coefficients, native_Gram_census, native_query_frontier,
    public_feedback, readout_gate_plan, xy_parity_estimator,
)
from theorems.dcp_correlated_block_observables import measurement_channel
from theorems.dcp_correlated_phase_block import density
from theorems.dcp_nonlinear_fiber_pairing import phase_value

ROOT=Path(__file__).resolve().parents[1]
CHECKER=ROOT/"research/certificates/dcp_complex_axis_readout_crosscheck.js"


@pytest.fixture(scope="module")
def report():
    return build_report()


def test_real_readout_has_exact_conjugation_alias_but_public_masks_can_break_it():
    A=((4,8),)
    baseline=measurement_channel(A,4,Fraction(7,8))
    s,t=baseline["secrets"].index((1,)),baseline["secrets"].index((3,))
    assert np.allclose(baseline["probabilities"][s],baseline["probabilities"][t])
    E=axis_ensemble(A,4,Fraction(7,8))
    assert np.max(np.abs(E["probabilities"][s]-E["probabilities"][t]))>0.05
    assert alias_metrics(E["probabilities"],E["secrets"],4)["all_secret_laws_distinct_on_this_selected_matrix"] is True


def test_conjugation_relates_complex_outcomes_by_recorded_mask_flip_not_equality():
    A=((1,0,5,1),(0,1,1,2))
    E=axis_ensemble(A,4,Fraction(7,8))
    P=E["probabilities"]
    for i,s in enumerate(E["secrets"]):
        j=E["secrets"].index(tuple(-v%4 for v in s))
        for r in range(16):
            assert np.allclose(P[j,r],P[i,r][:,np.arange(16)^r],atol=1e-13)
    assert np.allclose(P.sum(axis=(1,2,3)),1)


def test_actual_T_Sdg_H_plan_matches_full_density_readout_on_each_syndrome():
    A=((1,2,5),)
    feedback=public_feedback(A)
    H=hadamard(8)/np.sqrt(8)
    for r in (0,1,5,7):
        C=measurement_channel(A,4,Fraction(3,4),axes_mask=r,T_feedback_by_syndrome=feedback)
        for s,secret in enumerate(C["secrets"]):
            rho=density(A,4,secret,Fraction(3,4))
            for y,indices in enumerate(C["fibers"]):
                plan=readout_gate_plan(A,r,measured_syndrome_index=y,use_feedback=True)
                phases=np.array([np.exp(1j*np.pi*sum(feedback[y][i]*(x >> i & 1) for i in range(3))/4)*(-1j)**((r&x).bit_count()) for x in range(8)])
                U=H@np.diag(phases)
                branch=np.zeros((8,8),complex)
                branch[np.ix_(indices,indices)]=rho[np.ix_(indices,indices)]
                expected=np.diag(U@branch@U.conj().T).real
                assert np.allclose(expected,C["probabilities"][s,y],atol=1e-13)
                assert sum(g[0]=="T" for g in plan["terminal_gates_after_syndrome_measurement"])==sum(feedback[y])
                assert sum(g[0]=="SDG" for g in plan["terminal_gates_after_syndrome_measurement"])==r.bit_count()


def test_physical_feedback_does_not_enumerate_all_syndromes(monkeypatch):
    import theorems.dcp_complex_axis_readout as module
    def forbidden(*args):
        pytest.fail("physical plan enumerated a feedback table")
    monkeypatch.setattr(module,"public_feedback",forbidden)
    A=[[1]*8 for _ in range(5)]
    y=4**5-1
    plan=readout_gate_plan(A,7,measured_syndrome_index=y,use_feedback=True)
    assert plan["T_grid_feedback_coefficients"]==feedback_coefficients(A,y)
    assert plan["feedback_computed_only_for_realized_syndrome"] is True


def test_mask_dependent_feedback_can_undo_the_dither_and_is_outside_the_theorem():
    A=((4,8),)
    tables=[]
    for r in range(4):
        undo=[[2*(r >> i & 1) for i in range(2)] for _ in range(4)]
        tables.append(measurement_channel(A,4,1,axes_mask=r,T_feedback_by_syndrome=undo)["probabilities"]/4)
    P=np.stack(tables,axis=1)
    assert np.allclose(P[1],P[3])
    assert native_query_frontier(8)["random_axes_may_depend_on_secret_history_instead_of_fresh_uniform_coins"] is False


def test_exact_native_norm_counts_and_all_secret_order_classes(report):
    expected={"1":Fraction(87,64),"1/2":Fraction(1095,1024),"0":Fraction(1)}
    for C in report["complete_native_Gram_censuses"]:
        target=expected[C["visibility_exact"]]
        assert Fraction(C["exact_common_diagonal_from_coarse_parallelogram_census"])==target
        K=np.array(C["full_Gram_observed"])
        assert np.allclose(K,np.ones_like(K)+np.eye(len(K))*(float(target)-1),atol=1e-12)
        assert C["includes_zero_and_order_two_secrets"] is True
        assert C["source_family_identifiable_in_L2"]==(target>1)
    assert report["complete_native_Gram_censuses"][-1]["phase_bits"]==3
    assert report["complete_native_Gram_censuses"][-1]["all_original_label_matrices"]==64


def test_exact_coarse_counts_do_not_need_full_label_entries():
    assert exact_coarse_norm(1,2,1)==Fraction(87,64)
    assert exact_coarse_norm(1,2,Fraction(1,2))==Fraction(1095,1024)
    assert exact_coarse_norm(1,2,0)==1


def test_unbiased_XY_importance_estimator_and_exponential_second_moment():
    A=((4,8),)
    v=Fraction(7,8)
    E=axis_ensemble(A,4,v)
    P=E["probabilities"][1]
    for support,desired,expected in ((1,1,float(v)),(3,1,-float(v*v))):
        first=second=0.0
        for r,y,z in product(range(4),repeat=3):
            value=xy_parity_estimator(2,z,r,support,desired)
            first+=P[r,y,z]*value
            second+=P[r,y,z]*value*value
        assert first==pytest.approx(expected)
        assert second==pytest.approx(1 << support.bit_count())


def test_inference_receipts_do_not_turn_identifiability_or_SQ_into_a_decoder():
    for n in (8,16,32,64,128):
        F=native_query_frontier(n)
        H=n*(n+6)
        maxdist=int(F["max_secrets_distinguished_per_query_hex"],16)
        assert maxdist==6*n**4
        numerator=n*n*maxdist+1
        E=F["SQ_uniform_identification_probability_power_of_two_upper_exponent"]
        assert Fraction(numerator,1 << H)<=Fraction(1,1 << E)
        assert not F["raw_sample_learning_or_joint_multi_record_queries_ruled_out"]
        assert F["any_public_source_syndrome_local_phase_feedback_before_random_mask_covered"]
        assert F["adaptive_phase_feedback_transcript_information_bits_upper_per_fresh_batch"]=="3"
        assert not F["efficient_decoder_or_classical_simulator_supplied"]


def test_invalid_masks_targets_and_enumeration_caps_are_rejected():
    with pytest.raises(ValueError):
        readout_gate_plan(((1,2),),4)
    with pytest.raises(ValueError):
        xy_parity_estimator(2,0,0,1,2)
    with pytest.raises(ValueError):
        measurement_channel(((1,2),),4,1,T_feedback_by_syndrome=[[8,0]]*4)
    with pytest.raises(ValueError,match="UNKNOWN"):
        axis_ensemble(((1,)*5,),4,1)


def test_live_artifact_and_independent_phase_and_kernel_replay(report):
    assert json.loads(REPORT.read_text())==report
    result=subprocess.run(["node",str(CHECKER)],text=True,capture_output=True,check=True)
    assert json.loads(result.stdout)["complete_native_Gram_censuses"]==5


@pytest.mark.parametrize("field",["Gram","phase_plan","SQ_scope","decoder"])
def test_independent_checker_rejects_forged_statistics_gates_or_scope(report,tmp_path,field):
    payload=deepcopy(report)
    if field=="Gram":
        payload["complete_native_Gram_censuses"][0]["full_Gram_observed"][0][1]+=0.1
    elif field=="phase_plan":
        payload["selected_controls"][0]["exported_readout_plan"]["terminal_gates_after_syndrome_measurement"].pop()
    elif field=="SQ_scope":
        payload["native_inference_frontiers"][0]["raw_sample_learning_or_joint_multi_record_queries_ruled_out"]=True
    else:
        payload["selected_controls"][0]["decoder_or_speedup_candidate_supplied"]=True
    path=tmp_path/"forged.json"
    path.write_text(json.dumps(payload))
    result=subprocess.run(["node",str(CHECKER),str(path)],text=True,capture_output=True)
    assert result.returncode!=0


def test_readonly_cli_keeps_artifact_unchanged():
    before=REPORT.read_bytes()
    result=subprocess.run([sys.executable,"qsearch.py","dcp-complex-axis-readout","--no-write"],cwd=ROOT,text=True,capture_output=True)
    assert result.returncode==0,result.stderr
    assert REPORT.read_bytes()==before
