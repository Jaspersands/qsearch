from copy import deepcopy

from flint import fmpq, fmpq_mat
import pytest

from ternary_pair_collimation import LowProblem
from ternary_pair_cell_coverage import public_charts, _serialized_prepared
from ternary_repair_catalog import frozen_policy
from ternary_adaptive_shell import compile_adaptive
from ternary_prefix_integrality import prefix_geometry
from ternary_prefix_moments import moment_model, verify_moments
from ternary_moment_psd import certify_psd, moment_matrix
from ternary_moment_psd_mixtures import common_native_face, mixture_search, separate_supplied_hull


def model():
    p=LowProblem((81,),(((9,),(23,)),((41,),(37,)),((65,),(19,))),0)
    policy=frozen_policy(p,_serialized_prepared(public_charts(p,83950)));c=compile_adaptive(policy)
    return moment_model(prefix_geometry(p,(0,),policy,c,6,(0,)*6,((0,1),)*3))


def correlation_point(m,correlations):
    edges={(0,1):correlations[0],(0,2):correlations[1],(1,2):correlations[2]};values=[]
    for key in m["variables"]:
        if key[0]=="p":values.append(fmpq(1,2))
        else:
            r=edges[(key[1],key[3])];values.append(fmpq(1+r if key[2]==key[4] else 1-r,4))
    certificate=verify_moments(m,values)
    assert certificate["valid"]
    return certificate


def test_known_source_kernel_reduces_singular_matrices_without_losing_positivity():
    m=model();points=[correlation_point(m,r) for r in ((-1,1,1),(1,-1,1),(1,1,-1))]
    matrices=[moment_matrix(m,p["moments"]) for p in points]
    assert all(certify_psd(A)["negative"] for A in matrices)
    face,C=common_native_face(m,matrices)
    assert face["matrix_dimension"]==7 and face["face_dimension"]==4
    assert face["source_relation_rows"]==3 and not face["hull_specific_zero_rows"]
    assert fmpq(face["nonzero_relation_minor_determinant"])!=0
    assert len(face["independent_relation_rows"])==face["relation_rank"]
    T=fmpq_mat(face["transformation"])
    assert all(T*fmpq_mat(c)*T.transpose()==fmpq_mat(A) for c,A in zip(C,matrices))


def test_indefinite_points_can_have_exact_psd_convex_mixture():
    m=model();points=[correlation_point(m,r) for r in ((-1,1,1),(1,-1,1),(1,1,-1))]
    result=mixture_search(m,points,denominator=3)
    assert result["status"]=="EXACT_PSD_MOMENT_CONTINUATION_NOT_NATIVE_PROOF"
    weights=tuple(fmpq(x) for x in result["exact_convex_weights"])
    assert sum(weights)==1 and all(w>=0 for w in weights)
    values=tuple(sum(w*fmpq(p["moments"][j]) for w,p in zip(weights,points)) for j in range(len(m["variables"])))
    assert verify_moments(m,values)["valid"]
    assert certify_psd(moment_matrix(m,values))["ldl"]["valid"]
    assert not result["global_native_distribution_proved"]
    assert result["attempts"][-1]["compressed_positivity"]["ldl"]["valid"]


def test_grid_failure_does_not_prove_infeasibility_even_if_every_tested_point_negative():
    m=model();point=correlation_point(m,(-1,-1,-1))
    result=mixture_search(m,[point],denominator=8)
    assert result["status"]=="EXACT_SUPPLIED_CONVEX_HULL_PSD_OBSTRUCTION"
    assert result["attempts"][0]["compressed_positivity"]["negative"]["valid"]
    assert result["grid_failure_not_convex_hull_or_native_infeasibility"]
    assert not result["full_SDP_infeasibility_proved"]
    assert result["hull_separator"]["certificate"]["proves_ONLY_supplied_convex_hull_has_no_psd_matrix"]


def test_positive_dual_combination_can_separate_hull_when_no_single_direction_does():
    matrices=((("-1","0"),("0","1/2")),(("1/2","0"),("0","-1")))
    result=separate_supplied_hull(matrices)
    assert result["certificate"]["valid"] and result["cost"]["LP_calls"]==1
    cert=result["certificate"]
    assert sum(fmpq(x) for x in cert["nonnegative_weights"])==1
    assert all(fmpq(x)<0 for x in cert["point_trace_values"])


def test_feasible_hull_cannot_be_excluded_by_an_exact_positive_dual():
    matrices=((("-1","0"),("0","2")),(("2","0"),("0","-1")))
    result=separate_supplied_hull(matrices)
    assert result["certificate"] is None
    assert result["status"]=="HULL_SEPARATOR_UNKNOWN"


def test_whole_grid_preflight_is_unknown_and_performs_no_numerical_search():
    m=model();points=[correlation_point(m,r) for r in ((-1,1,1),(1,-1,1),(1,1,-1))]
    result=mixture_search(m,points,denominator=100,grid_budget=10)
    assert result["status"]=="CONVEX_PSD_GRID_PREFLIGHT_UNKNOWN"
    assert result["cost"]["numeric_eigen_proposals"]==0 and not result["attempts"]


def test_bad_point_winding_face_and_budget_inputs_fail_closed():
    m=model();point=correlation_point(m,(-1,1,1));bad=deepcopy(point);bad["required_winding"]=1
    with pytest.raises(ValueError):mixture_search(m,[bad])
    bad=deepcopy(point);bad["moments"][0]="-1"
    with pytest.raises(ValueError):mixture_search(m,[bad])
    with pytest.raises(ValueError):mixture_search(m,[point],denominator=0)
    with pytest.raises(ValueError):mixture_search(m,[])
    A=[list(row) for row in moment_matrix(m,point["moments"])]
    A[0][0]+=1
    with pytest.raises(ValueError,match="reconstruct"):common_native_face(m,[A])
    A[0][1]+=1
    with pytest.raises(ValueError,match="symmetric"):common_native_face(m,[A])
