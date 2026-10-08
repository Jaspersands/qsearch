from copy import deepcopy
from itertools import product
from types import SimpleNamespace

from flint import fmpq
import numpy as np
import pytest

from ternary_pair_collimation import LowProblem
from ternary_pair_cell_coverage import public_charts, _serialized_prepared
from ternary_repair_catalog import frozen_policy
from ternary_adaptive_shell import compile_adaptive
from ternary_prefix_integrality import prefix_geometry
from ternary_prefix_moments import moment_model, verify_moments, word_moments, analyze_moments
from ternary_moment_psd import moment_matrix, certify_psd
from ternary_local_marginals import local_model, verify_extension, verify_local_dual, analyze_local, append_local_cut, bounded_cut_resolve


def fixture(correlation=fmpq(-2,5)):
    p=LowProblem((81,),(((9,),(23,)),((41,),(37,)),((65,),(19,))),0)
    policy=frozen_policy(p,_serialized_prepared(public_charts(p,83950)));compiled=compile_adaptive(policy)
    m=moment_model(prefix_geometry(p,(0,),policy,compiled,6,(0,)*6,((0,1),)*3))
    values=[fmpq(1,2) if key[0]=="p" else (1+correlation if key[2]==key[4] else 1-correlation)/4 for key in m["variables"]]
    assert verify_moments(m,values)["valid"]
    return m,values


def test_psd_moment_point_can_fail_three_block_local_realizability():
    m,values=fixture();assert certify_psd(moment_matrix(m,values))["ldl"]["valid"]
    local=local_model(m,values,(0,1,2));result=analyze_local(local)
    assert result["status"]=="EXACT_NONPSD_THREE_BLOCK_OBSTRUCTION" and result["extension"] is None
    cert=result["dual"]
    assert verify_local_dual(local,cert["pair_marginal_multipliers"])["valid"]
    assert fmpq(cert["exact_gap_point_value"])<0
    assert all(fmpq(x)>=0 for x in cert["exact_assignment_coefficients"])
    assert not cert["proves_no_full_moment_PSD_point"]


@pytest.mark.parametrize("correlation",[fmpq(-1,3),fmpq(0),fmpq(1)])
def test_exact_extendable_pair_marginals_are_not_global_recovery(correlation):
    m,values=fixture(correlation);local=local_model(m,values,(0,1,2));result=analyze_local(local)
    assert result["status"]=="EXACT_THREE_BLOCK_EXTENSION_NOT_GLOBAL" and not result["dual"]
    assert verify_extension(local,result["extension"]["assignment_probabilities"])["valid"]
    assert not result["extension"]["global_native_realization_proved"]


def test_every_honest_native_word_extends_and_survives_nonPSD_cut():
    m,values=fixture();local=local_model(m,values,(0,1,2));cert=analyze_local(local)["dual"]
    cut=append_local_cut(m,local,cert)
    for word in product((0,1),repeat=3):
        values=word_moments(m,word);honest=local_model(m,values,(0,1,2))
        distribution=[int(w==word) for w in honest["assignments"]]
        assert verify_extension(honest,distribution)["valid"]
        assert verify_moments(cut,word_moments(cut,word))["valid"]
    assert len(moment_matrix(cut,word_moments(cut,(0,0,0))))==7
    assert analyze_moments(cut)["primal"]


def test_cut_rejects_specific_psd_point_not_entire_feasible_model():
    m,values=fixture();local=local_model(m,values,(0,1,2));cert=analyze_local(local)["dual"]
    cut=append_local_cut(m,local,cert)
    assert not verify_moments(cut,(*values,0))["valid"]
    assert verify_moments(cut,word_moments(cut,(0,0,0)))["valid"]


def test_tiny_negative_native_assignment_column_is_rejected_exactly():
    m,values=fixture();local=local_model(m,values,(0,1,2));cert=analyze_local(local)["dual"]
    weights=[fmpq(a) for a in cert["pair_marginal_multipliers"]]
    j=next(j for j,x in enumerate(cert["exact_assignment_coefficients"]) if fmpq(x)==0)
    row=next(i for i,row in enumerate(local["rows"]) if row[j]);weights[row]-=fmpq(1,10**80)
    assert not verify_local_dual(local,weights)["valid"]


@pytest.mark.parametrize("blocks",[(0,0,2),(2,1,0),(0,1,3),(True,1,2),(0,1)])
def test_invalid_original_block_order_or_domain_indices_fail_closed(blocks):
    m,values=fixture()
    with pytest.raises(ValueError):local_model(m,values,blocks)


def test_bad_points_duals_and_distributions_cannot_be_accepted_by_flags():
    m,values=fixture();bad=list(values);bad[0]=-1
    with pytest.raises(ValueError):local_model(m,bad,(0,1,2))
    local=local_model(m,values,(0,1,2))
    with pytest.raises(ValueError):verify_extension(local,[])
    with pytest.raises(ValueError):verify_local_dual(local,[])
    assert not verify_extension(local,[0]*8)["valid"]
    assert not verify_extension(local,[fmpq(-1,8)]*8)["valid"]
    with pytest.raises(ValueError):append_local_cut(m,local,{"valid":True,"required_winding":None,"pair_marginal_multipliers":[0]*12})
    cert=analyze_local(local)["dual"];bad=deepcopy(cert);bad["required_winding"]=1
    with pytest.raises(ValueError,match="another winding"):append_local_cut(m,local,bad)


def test_false_numerical_feasible_and_dual_statuses_stay_unknown(monkeypatch):
    import ternary_local_marginals as module
    m,values=fixture();local=local_model(m,values,(0,1,2))
    def fake(*args,**kwargs):
        n=8 if kwargs.get("A_ub") is None else 12
        return SimpleNamespace(success=True,x=np.zeros(n))
    monkeypatch.setattr(module,"linprog",fake)
    result=analyze_local(local)
    assert result["status"]=="THREE_BLOCK_EXACT_RECONSTRUCTION_UNKNOWN"
    assert result["extension"] is None and result["dual"] is None


def test_bounded_resolve_preserves_honest_words_and_explicit_caps():
    m,values=fixture();local=local_model(m,values,(0,1,2));result=analyze_local(local)
    trial={"blocks":[0,1,2],**result}
    zero=bounded_cut_resolve(m,values,[trial],cut_budget=0)
    assert not zero["cuts"] and zero["analysis"] is None
    answer=bounded_cut_resolve(m,values,[trial])
    assert len(answer["cuts"])==1 and answer["analysis"]["primal"]
    assert not answer["full_base_plus_selected_local_cuts_infeasible"]
    assert not answer["ordinary_two_witness_recovery_proved"] and not answer["whole_prefix_infeasibility_proved"]
    with pytest.raises(ValueError):bounded_cut_resolve(m,values,[trial],cut_budget=-1)


def test_cut_cannot_transplant_a_farkas_proof_to_different_native_columns_or_assignments():
    m,values=fixture();local=local_model(m,values,(0,1,2));cert=analyze_local(local)["dual"]
    bad=deepcopy(local);bad["pair_variable_indices"]=(0,*bad["pair_variable_indices"][1:])
    with pytest.raises(ValueError,match="EVERY actual native"):append_local_cut(m,bad,cert)
    bad=deepcopy(local);bad["assignments"]=bad["assignments"][:-1]
    with pytest.raises(ValueError,match="EVERY actual native"):append_local_cut(m,bad,cert)
    bad=deepcopy(local);rows=list(bad["rows"]);rows[0]=(0,)*8;bad["rows"]=tuple(rows)
    with pytest.raises(ValueError,match="EVERY actual native"):append_local_cut(m,bad,cert)
