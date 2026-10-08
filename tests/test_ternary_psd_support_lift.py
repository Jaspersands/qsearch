from copy import deepcopy
from itertools import product
from types import SimpleNamespace

from flint import fmpq
import numpy as np
import pytest

from ternary_prefix_moments import verify_moments, word_moments
from ternary_moment_psd import moment_matrix, quadratic_value, certify_psd, append_psd_cut
from ternary_moment_psd_mixtures import common_native_face, separate_supplied_hull
from ternary_psd_support_lift import (sos_objective, verify_objective, functional_value,
    verify_escape, verify_support_dual, support_test, refine_with_escape)
from ternary_pair_collimation import LowProblem
from ternary_pair_cell_coverage import public_charts, _serialized_prepared
from ternary_repair_catalog import frozen_policy
from ternary_adaptive_shell import compile_adaptive
from ternary_prefix_integrality import prefix_geometry
from ternary_prefix_integrality import rational
from ternary_prefix_moments import moment_model


def fixture():
    p=LowProblem((81,),(((9,),(23,)),((41,),(37,)),((65,),(19,))),0)
    policy=frozen_policy(p,_serialized_prepared(public_charts(p,83950)));compiled=compile_adaptive(policy)
    m=moment_model(prefix_geometry(p,(0,),policy,compiled,6,(0,)*6,((0,1),)*3))
    values=[fmpq(1,2) if key[0]=="p" or key[2]!=key[4] else fmpq(0) for key in m["variables"]]
    point=verify_moments(m,values);assert point["valid"]
    A=moment_matrix(m,point["moments"])
    face,C=common_native_face(m,[A]);separator=separate_supplied_hull(C)["certificate"]
    assert separator
    objective=sos_objective(m,face["free_indices"],separator["vectors"],separator["nonnegative_weights"])
    return m,point,objective


def fixed_point_model(m,point):
    x=tuple(fmpq(a) for a in point["moments"])
    extra=tuple({j:int(a.q)} for j,a in enumerate(x));rhs=tuple(int(a.p) for a in x)
    return {**m,"rows":(*m["rows"],*extra),"rhs":(*m["rhs"],*rhs),
        "nonzero_entries":m["nonzero_entries"]+len(extra)}


def test_sos_expansion_matches_trace_and_is_nonnegative_on_all_honest_words():
    m,point,objective=fixture();D=int(objective["clearing_denominator"]);d=int(objective["primitive_divisor"])
    for values in (point["moments"],*(word_moments(m,w) for w in product((0,1),repeat=3))):
        A=moment_matrix(m,values)
        trace=sum(fmpq(a)*quadratic_value(A,v) for a,v in zip(objective["nonnegative_weights"],objective["embedded_vectors"]))
        assert functional_value(m,objective,values)==trace*D/d
    assert functional_value(m,objective,point["moments"])<0
    assert all(verify_escape(m,objective,word_moments(m,w))["valid"] for w in product((0,1),repeat=3))


def test_principal_embedding_does_not_impose_hull_zero_coordinates():
    m,_,_=fixture();values=word_moments(m,(0,0,0));A=moment_matrix(m,values)
    face,C=common_native_face(m,[A]);assert face["hull_specific_zero_rows"]
    objective=sos_objective(m,face["free_indices"],[[1]*len(C[0])],[1])
    outside=word_moments(m,(1,1,1))
    assert verify_moments(m,outside)["valid"] and verify_escape(m,objective,outside)["valid"]
    assert any(moment_matrix(m,outside)[i][i]>0 for i in face["hull_specific_zero_rows"])
    assert not objective["hull_specific_constraints_added"]


def test_nonnegative_support_point_falsifies_hull_dual_without_claiming_psd():
    m,_,objective=fixture();answer=support_test(m,objective)
    assert answer["status"]=="EXACT_BASE_MOMENT_ESCAPE_FROM_HULL_DUAL"
    assert answer["escape"]["valid"] and answer["cost"]["LP_calls"]==1
    assert not answer["escape"]["matrix_PSD_proved"] and not answer["full_degree_two_SDP_infeasibility_proved"]
    assert verify_escape(m,objective,answer["escape"]["moments"])["valid"]


def test_negative_point_is_not_escape_and_numerical_max_is_not_a_global_bound():
    m,point,objective=fixture()
    assert not verify_escape(m,objective,point["moments"])["valid"]
    assert not verify_support_dual(m,objective,[0]*len(m["rows"]))["valid"]


def test_exact_global_upper_dual_excludes_full_fixed_moment_model():
    m,point,objective=fixture();m=fixed_point_model(m,point)
    answer=support_test(m,objective)
    assert answer["status"]=="EXACT_GLOBAL_DEGREE_TWO_PSD_OBSTRUCTION"
    assert answer["dual"]["valid"] and answer["escape"] is None
    assert answer["full_degree_two_SDP_infeasibility_proved"] and not answer["whole_prefix_infeasibility_proved"]
    cert=verify_support_dual(m,objective,answer["dual"]["signed_equation_multipliers"])
    assert cert["valid"] and all(fmpq(x)>=0 for x in cert["exact_column_slacks"])
    assert fmpq(cert["exact_functional_upper_bound"])<0


def test_exact_column_violation_far_below_float_resolution_is_rejected():
    m,point,objective=fixture();m=fixed_point_model(m,point);c,_=verify_objective(m,objective)
    y=[fmpq(0)]*len(m["rows"])
    for i,a in enumerate(c):y[len(m["rows"])-len(c)+i]=fmpq(a,int(fmpq(point["moments"][i]).q))
    assert verify_support_dual(m,objective,y)["valid"]
    y[-1]-=fmpq(1,10**80)
    bad=verify_support_dual(m,objective,y)
    assert not bad["valid"] and fmpq(bad["exact_column_slacks"][-1])<0


def test_canonical_sos_objective_rejects_tampered_coefficients_embedding_and_winding():
    m,_,objective=fixture()
    for key in ("integer_constant","clearing_denominator","primitive_divisor"):
        bad=deepcopy(objective);bad[key]=str(int(bad[key])+1)
        with pytest.raises(ValueError):verify_objective(m,bad)
    bad=deepcopy(objective);bad["integer_coefficients"][0]="9999"
    with pytest.raises(ValueError):verify_objective(m,bad)
    bad=deepcopy(objective);bad["required_winding"]=1
    with pytest.raises(ValueError,match="another winding"):verify_objective(m,bad)
    bad=deepcopy(objective);bad["embedded_vectors"][0][0]="1"
    with pytest.raises(ValueError):verify_objective(m,bad)


@pytest.mark.parametrize("free,vectors,weights",[
    ([1,1],[[1,1]],[1]),([True],[[1]],[1]),([7],[[1]],[1]),
    ([1],[[1]],[-1]),([1],[[1]],["1/2"]),([1],[[1.0]],[1]),
    ([1],[[0]],[1]),([1],[[1,2]],[1]),
])
def test_bad_sos_inputs_fail_closed(free,vectors,weights):
    m,_,_=fixture()
    with pytest.raises(ValueError):sos_objective(m,free,vectors,weights)


def test_strengthened_models_and_incomplete_arrays_cannot_be_silently_used():
    m,point,objective=fixture();cut=append_psd_cut(m,[1]*7)
    with pytest.raises(ValueError,match="unstrengthened"):sos_objective(cut,[1],[[1]],[1])
    with pytest.raises(ValueError):verify_escape(m,objective,point["moments"][:-1])
    with pytest.raises(ValueError):verify_support_dual(m,objective,[])
    with pytest.raises(ValueError):support_test(m,objective,0)


def test_guarded_reconstruction_preserves_unknown_even_if_numeric_optimum_is_negative():
    m,point,objective=fixture();m=fixed_point_model(m,point)
    answer=support_test(m,objective,max_exact_cells=1)
    assert answer["status"]=="GLOBAL_PSD_SUPPORT_RECONSTRUCTION_UNKNOWN"
    assert answer["cost"]["reconstruction_guard_skips"]>0 and answer["dual"] is None
    assert not answer["full_degree_two_SDP_infeasibility_proved"]


def test_false_optimizer_success_cannot_bypass_exact_source_equations(monkeypatch):
    import ternary_psd_support_lift as module
    m,_,objective=fixture();N=len(m["variables"]);R=len(m["rows"])
    def fake(*args,**kwargs):
        if kwargs.get("A_eq") is not None:
            return SimpleNamespace(success=True,status=0,x=np.zeros(N),eqlin=SimpleNamespace(marginals=np.zeros(R)))
        return SimpleNamespace(success=True,status=0,x=np.zeros(R))
    monkeypatch.setattr(module,"linprog",fake)
    answer=support_test(m,objective)
    assert answer["status"]=="GLOBAL_PSD_SUPPORT_RECONSTRUCTION_UNKNOWN"
    assert answer["escape"] is None and answer["dual"] is None


def test_an_escape_need_not_be_positive_semidefinite():
    m,point,_=fixture()
    objective=sos_objective(m,[0],[[1]],[1])
    cert=verify_escape(m,objective,point["moments"])
    assert cert["valid"] and fmpq(cert["exact_functional_value"])==1
    assert certify_psd(moment_matrix(m,point["moments"]))["negative"]
    assert not cert["matrix_PSD_proved"]


def test_large_exact_sos_normalization_never_uses_decimal_int_or_float_conversion():
    m,_,_=fixture();denominator=10**2500
    objective=sos_objective(m,[0,1],[[1,fmpq(1,denominator)]],[1])
    assert objective["maximum_integer_coefficient_bits"]>16000
    assert len(objective["integer_constant"])>4300
    assert rational(objective["integer_constant"])==fmpq(denominator**2)
    result=support_test(m,objective)
    assert result["escape"]["valid"] and not result["dual"]
    with pytest.raises(ValueError):rational("2/2")
    with pytest.raises(ValueError):rational("1.0")
    with pytest.raises(ValueError):rational("1/0")


def test_one_source_aware_refinement_can_find_psd_mixture_without_global_native_claim():
    m,point,_=fixture();honest=verify_moments(m,word_moments(m,(0,0,0)))
    result=refine_with_escape(m,[point],honest)
    assert result["refinement_rounds"]==1
    assert result["expanded_hull"]["status"]=="EXACT_PSD_MOMENT_CONTINUATION_NOT_NATIVE_PROOF"
    assert not result["expanded_hull"]["global_native_distribution_proved"]
    assert result["next_support"] is None and result["next_objective"] is None


def test_refinement_rechecks_point_values_and_winding_not_generator_flags():
    m,point,_=fixture();bad=deepcopy(point);bad["required_winding"]=1
    with pytest.raises(ValueError,match="another winding"):refine_with_escape(m,[point],bad)
    bad=deepcopy(point);bad["moments"][0]="-1"
    with pytest.raises(ValueError,match="verified base point"):refine_with_escape(m,[point],bad)


def test_refinement_hull_obstruction_is_subjected_to_new_global_support_test(monkeypatch):
    import ternary_psd_support_lift as module
    m,point,objective=fixture();face,C=common_native_face(m,[moment_matrix(m,point["moments"])])
    hull={"face":face,"hull_separator":{"certificate":separate_supplied_hull(C)["certificate"]}}
    monkeypatch.setattr(module,"mixture_search",lambda *a,**k:hull)
    escape=verify_escape(m,objective,word_moments(m,(0,0,0)))
    result=refine_with_escape(m,[point],escape)
    assert result["next_support"]["status"]=="EXACT_BASE_MOMENT_ESCAPE_FROM_HULL_DUAL"
    assert not result["next_support"]["full_degree_two_SDP_infeasibility_proved"]
    assert result["next_support"]["escape_positivity"]
