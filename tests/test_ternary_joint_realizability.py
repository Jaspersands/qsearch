from copy import deepcopy

from flint import fmpq
import pytest

from ternary_pair_collimation import LowProblem
from ternary_pair_cell_coverage import public_charts, _serialized_prepared
from ternary_repair_catalog import frozen_policy
from ternary_adaptive_shell import compile_adaptive
from ternary_prefix_integrality import prefix_geometry
from ternary_prefix_moments import moment_model, verify_moments, word_moments
from ternary_moment_psd import moment_matrix, quadratic_value, append_psd_cut
from ternary_local_marginals import local_model, analyze_local, append_local_cut
from ternary_psd_support_lift import sos_objective, verify_objective, functional_value
from ternary_joint_realizability import base_certificate, positive_hull_point, audit_joint


def fixture():
    p=LowProblem((81,),(((9,),(23,)),((41,),(37,)),((65,),(19,))),0)
    policy=frozen_policy(p,_serialized_prepared(public_charts(p,83950)));compiled=compile_adaptive(policy)
    base=moment_model(prefix_geometry(p,(0,),policy,compiled,6,(0,)*6,((0,1),)*3))
    values=[fmpq(1,2) if key[0]=="p" else fmpq(3,20) if key[2]==key[4] else fmpq(7,20) for key in base["variables"]]
    local=local_model(base,values,(0,1,2));cert=analyze_local(local)["dual"]
    return base,values,append_local_cut(base,local,cert)


def test_honest_joint_point_is_positive_without_claiming_native_relaxation_gap():
    _,_,model=fixture();honest=verify_moments(model,word_moments(model,(0,0,0)))
    result=audit_joint(model,honest,max_psd_cuts=0)
    assert result["status"]=="EXACT_JOINT_PSD_CONTINUATION_NOT_NATIVE_PROOF"
    assert result["joint_gap_point"]["positivity"]["ldl"]["valid"]
    assert not result["full_joint_PSD_infeasibility_proved"] and result["loop"]["cuts_added"]==0
    assert not result["joint_gap_point"]["global_native_distribution_proved"]


def test_old_psd_point_violating_local_cuts_cannot_enter_joint_hull():
    base,values,model=fixture();old=verify_moments(base,values)
    with pytest.raises(ValueError):base_certificate(model,old)
    bad={**old,"moments":[*old["moments"],"0"]}
    with pytest.raises(ValueError,match="ALL original and local"):audit_joint(model,bad)
    with pytest.raises(ValueError):positive_hull_point(model,[bad],{"status":"EXACT_PSD_MOMENT_CONTINUATION_NOT_NATIVE_PROOF","exact_convex_weights":["1"]})


def test_joint_base_point_rechecks_winding_and_every_slack():
    _,_,model=fixture();honest=verify_moments(model,word_moments(model,(0,0,0)))
    bad=deepcopy(honest);bad["required_winding"]=1
    with pytest.raises(ValueError,match="another winding"):base_certificate(model,bad)
    bad=deepcopy(honest);bad["moments"][-1]="-1"
    with pytest.raises(ValueError):base_certificate(model,bad)


def test_psd_cut_has_zero_coefficients_on_existing_local_slack():
    _,_,model=fixture();vector=(1,2,3,4,5,6,7)
    cut=append_psd_cut(model,vector)
    assert cut["psd_cuts"][-1]["integer_coefficients"][-1]=="0"
    values=word_moments(cut,(0,0,0));assert verify_moments(cut,values)["valid"]
    assert len(moment_matrix(cut,values))==7


def test_slack_model_sos_expansion_is_explicit_and_zero_on_both_slack_types():
    _,_,model=fixture();model=append_psd_cut(model,(1,2,3,4,5,6,7))
    with pytest.raises(ValueError):sos_objective(model,[0,1],[[1,2]],[1])
    objective=sos_objective(model,[0,1],[[1,2]],[1],allow_slacks=True)
    c,k=verify_objective(model,objective)
    assert c[-2:]==(0,0) and objective["allow_slacks"]
    values=word_moments(model,(0,0,0));matrix=moment_matrix(model,values)
    trace=quadratic_value(matrix,objective["embedded_vectors"][0])
    assert functional_value(model,objective,values)==trace*int(objective["clearing_denominator"])/int(objective["primitive_divisor"])
    bad=deepcopy(objective);bad["integer_coefficients"][-1]="1"
    with pytest.raises(ValueError):verify_objective(model,bad)
    bad=deepcopy(objective);del bad["allow_slacks"]
    with pytest.raises(ValueError):verify_objective(model,bad)
    with pytest.raises(ValueError):sos_objective(model,[0],[[1]],[1],allow_slacks=1)


def test_joint_convex_point_has_full_original_coordinate_psd_proof():
    _,_,model=fixture();points=[verify_moments(model,word_moments(model,w)) for w in ((0,0,0),(1,1,1))]
    hull={"status":"EXACT_PSD_MOMENT_CONTINUATION_NOT_NATIVE_PROOF","exact_convex_weights":["1/2","1/2"]}
    result=positive_hull_point(model,points,hull)
    assert result["primal"]["valid"] and result["positivity"]["ldl"]["valid"]
    assert not result["global_native_distribution_proved"]
    for weights in (("2","-1"),("1/2",),("1/3","1/3")):
        with pytest.raises(ValueError):positive_hull_point(model,points,{**hull,"exact_convex_weights":weights})


def test_falsely_positive_hull_flag_cannot_bypass_full_psd_verification():
    base,_,_=fixture();values=[]
    correlations={(0,1):-1,(0,2):1,(1,2):1}
    for key in base["variables"]:
        if key[0]=="p":values.append(fmpq(1,2))
        else:
            r=correlations[(key[1],key[3])];values.append(fmpq(1+r if key[2]==key[4] else 1-r,4))
    cert=verify_moments(base,values);assert cert["valid"]
    fake={"status":"EXACT_PSD_MOMENT_CONTINUATION_NOT_NATIVE_PROOF","exact_convex_weights":["1"]}
    with pytest.raises(ValueError,match="original-coordinate"):positive_hull_point(base,[cert],fake)


def test_bounded_joint_loop_cannot_exclude_model_with_honest_native_words():
    base,_,model=fixture();correlations={(0,1):-1,(0,2):1,(1,2):1};values=[]
    for key in base["variables"]:
        if key[0]=="p":values.append(fmpq(1,2))
        else:
            r=correlations[(key[1],key[3])];values.append(fmpq(1+r if key[2]==key[4] else 1-r,4))
    cut=model["local_marginal_cuts"][0]
    slack=sum(int(a)*values[int(j)] for j,a in cut["integer_coefficients"].items())
    initial=verify_moments(model,(*values,slack));assert initial["valid"]
    result=audit_joint(model,initial,max_psd_cuts=3)
    assert result["status"] in ("JOINT_LOCAL_PSD_AUDIT_UNKNOWN","EXACT_JOINT_PSD_CONTINUATION_NOT_NATIVE_PROOF")
    assert not result["full_joint_PSD_infeasibility_proved"] and not result["whole_prefix_infeasibility_proved"]
    assert result["loop"]["cuts_added"]<=3


def test_prior_psd_cuts_cannot_silently_overrun_new_joint_cut_budget():
    _,_,model=fixture();model=append_psd_cut(model,(1,2,3,4,5,6,7))
    honest=verify_moments(model,word_moments(model,(0,0,0)))
    with pytest.raises(ValueError,match="without prior PSD cuts"):audit_joint(model,honest,max_psd_cuts=0)
