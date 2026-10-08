from copy import deepcopy
from itertools import product
from types import SimpleNamespace

from flint import fmpq, fmpq_mat
import numpy as np
import pytest

from ternary_pair_collimation import LowProblem
from ternary_pair_cell_coverage import public_charts, _serialized_prepared
from ternary_pair_lattice import coset_target, word_coordinates
from ternary_repair_catalog import frozen_policy
from ternary_adaptive_shell import compile_adaptive
from ternary_prefix_integrality import prefix_geometry
from ternary_prefix_moments import moment_model, word_moments, verify_moments, analyze_moments
from ternary_moment_psd import (certify_psd, verify_ldl, verify_negative, quadratic_value,
    moment_matrix, append_psd_cut, psd_cut_loop)


def prepared(A=(9,23,41,37,65,19),Q=81):
    p=LowProblem((Q,),tuple(((a,),(b,)) for a,b in zip(A[::2],A[1::2])),0)
    policy=frozen_policy(p,_serialized_prepared(public_charts(p,83950)))
    return p,policy,compile_adaptive(policy)


@pytest.mark.parametrize("A",[
    ((0,0),(0,0)),((1,1),(1,1)),((1,0,1),(0,0,0),(1,0,1)),
    (("1/3","2/3"),("2/3","4/3")),
])
def test_exact_singular_psd_factorizations_replay_original_matrix(A):
    result=certify_psd(A)
    assert result["ldl"]["valid"] and result["negative"] is None
    proof=result["ldl"]
    assert verify_ldl(A,proof["lower"],proof["diagonal"])["valid"]
    bad=deepcopy(proof["lower"]);bad[0][0]="2"
    assert not verify_ldl(A,bad,proof["diagonal"])["valid"]


@pytest.mark.parametrize("A",[
    ((0,1),(1,0)),((0,"1/10000000000000000000000000000000000000000"),("1/10000000000000000000000000000000000000000",1)),
    ((1,1),(1,0)),((1,0),(0,"-1/10000000000000000000000000000000000000000")),
    ((1,1,0),(1,1,1),(0,1,0)),
])
def test_indefinite_singular_and_tiny_negative_cases_have_exact_lifted_vectors(A):
    result=certify_psd(A,compact=False)
    assert result["negative"]["valid"] and result["ldl"] is None
    cert=result["negative"]
    assert verify_negative(A,cert["vector"])["valid"]
    assert str(quadratic_value(A,cert["vector"]))==cert["quadratic_value"]
    assert not verify_negative(A,[0]*len(A))["valid"]


def test_floating_eigenvector_is_only_a_proposal_and_cannot_overwrite_exact_proof(monkeypatch):
    monkeypatch.setattr(np.linalg,"eigh",lambda A:(np.array([-100,100]),np.eye(2)))
    result=certify_psd(((1,0),(0,-1)))
    assert result["negative"]["valid"] and result["short_vector_proposal_bits"] is None
    monkeypatch.setattr(np.linalg,"eigh",lambda A:(_ for _ in ()).throw(np.linalg.LinAlgError()))
    assert certify_psd(((0,1),(1,0)))["negative"]["valid"]


def test_invalid_exact_matrix_factor_and_vector_inputs_fail_closed():
    for A in ((),((1,0),),((1,1),(0,1)),((0.1,),),((True,),)):
        with pytest.raises(ValueError): certify_psd(A)
    with pytest.raises(ValueError): verify_negative(((1,),),())
    with pytest.raises(ValueError): verify_ldl(((1,),),(),())
    assert not verify_ldl(((1,),),((1,),),(-1,))["valid"]


def test_native_word_and_exact_mixture_matrices_are_psd_and_all_cuts_are_valid():
    p,policy,c=prepared();g=prefix_geometry(p,(0,),policy,c,6,(0,)*6);model=moment_model(g)
    words=list(product(range(3),repeat=3))
    values=[word_moments(model,w) for w in words]
    mixture=tuple(sum(v[j] for v in values)*fmpq(1,len(values)) for j in range(len(values[0])))
    assert verify_moments(model,mixture)["valid"]
    assert certify_psd(moment_matrix(model,mixture))["ldl"]["valid"]
    vectors=[tuple(i-3 for i in range(10)),tuple(fmpq(i,17) for i in range(10))]
    for vector in vectors:
        strengthened=append_psd_cut(model,vector);cut=strengthened["psd_cuts"][-1]
        for word,v in zip(words,values):
            q=quadratic_value(moment_matrix(model,v),vector)
            scaled=q*int(cut["clearing_denominator"])/int(cut["primitive_divisor"])
            assert scaled>=0
            assert verify_moments(strengthened,(*v,scaled))["valid"]
            assert verify_moments(strengthened,word_moments(strengthened,word))["valid"]


def frustrated_pair_model():
    # Native two-choice blocks with pairwise perfect anticorrelation on a
    # triangle have valid pair marginals but no global distribution.
    p,policy,c=prepared();g=prefix_geometry(p,(0,),policy,c,6,(0,)*6,((0,1),)*3)
    model=moment_model(g)
    values=[]
    for key in model["variables"]:
        values.append(fmpq(1,2) if key[0]=="p" or key[2]!=key[4] else fmpq(0))
    assert verify_moments(model,values)["valid"]
    return model,verify_moments(model,values)


def test_psd_cut_refutes_one_frustrated_point_not_the_feasible_space():
    model,initial=frustrated_pair_model();A=moment_matrix(model,initial["moments"])
    result=certify_psd(A)
    assert result["negative"]["valid"]
    cut_model=append_psd_cut(model,result["negative"]["vector"])
    assert not verify_moments(cut_model,(*initial["moments"],0))["valid"]
    # Honest words still exist in this unconditioned model, so a point
    # refutation cannot be reused as an infeasibility certificate.
    answer=analyze_moments(cut_model)
    assert answer["primal"] and not answer["dual"]


def test_bounded_loop_re_solves_and_cap_is_not_global_infeasibility():
    model,initial=frustrated_pair_model()
    capped=psd_cut_loop(model,initial,0)
    assert capped["status"]=="PSD_CUT_CAP_UNKNOWN" and capped["cuts_added"]==0 and capped["LP_calls"]==0
    result=psd_cut_loop(model,initial,3)
    # Three cuts are not guaranteed to find a PSD point. Honest words certify
    # feasibility, so neither a cap nor another indefinite point proves empty.
    assert result["status"] in ("EXACT_PSD_CONTINUATION_NOT_NATIVE","PSD_CUT_CAP_UNKNOWN")
    assert result["cuts_added"]>=1 and result["LP_calls"]>=1
    assert not result["integer_prefix_completion_proved"]
    honest=verify_moments(model,word_moments(model,(0,0,0)))
    accepted=psd_cut_loop(model,honest,3)
    assert accepted["status"]=="EXACT_PSD_CONTINUATION_NOT_NATIVE" and accepted["LP_calls"]==0


def test_cut_loop_preserves_exact_winding_and_unknown_semantics(monkeypatch):
    import ternary_moment_psd as module
    model,initial=frustrated_pair_model();bad=deepcopy(initial);bad["required_winding"]=1
    with pytest.raises(ValueError): psd_cut_loop(model,bad)
    with pytest.raises(ValueError): psd_cut_loop(model,initial,-1)
    monkeypatch.setattr(module,"analyze_moments",lambda *a,**k:{"primal":None,"dual":None,"cost":{"LP_calls":2}})
    result=psd_cut_loop(model,initial,3)
    assert result["status"]=="PSD_CUT_RECONSTRUCTION_UNKNOWN"
    assert result["cuts_added"]==1 and result["LP_calls"]==2


def test_zero_vector_cannot_add_a_fake_cut_and_slacks_are_not_indicators():
    model,initial=frustrated_pair_model()
    with pytest.raises(ValueError): append_psd_cut(model,[0]*7)
    with pytest.raises(ValueError): append_psd_cut(model,[1])
    vector=(1,1,0,0,0,0,0)
    strengthened=append_psd_cut(model,vector)
    cut=strengthened["psd_cuts"][-1]
    v=word_moments(model,(0,0,0));A=moment_matrix(model,v)
    slack=quadratic_value(A,vector)*int(cut["clearing_denominator"])/int(cut["primitive_divisor"])
    assert moment_matrix(strengthened,(*v,slack))==A


def test_false_dual_generator_flag_cannot_certify_entire_cut_relaxation(monkeypatch):
    import ternary_moment_psd as module
    model,initial=frustrated_pair_model()
    def fake(m,*args):
        return {"primal":None,"dual":{"valid":True,"required_winding":m["required_winding"],
            "signed_equation_multipliers":["0"]*len(m["rows"])},"cost":{"LP_calls":1}}
    monkeypatch.setattr(module,"analyze_moments",fake)
    with pytest.raises(ValueError,match="exact dual recheck"):psd_cut_loop(model,initial,1)
