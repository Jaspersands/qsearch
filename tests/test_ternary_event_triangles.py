from itertools import product

from flint import fmpq
import pytest

from ternary_pair_collimation import LowProblem
from ternary_pair_cell_coverage import public_charts, _serialized_prepared
from ternary_repair_catalog import frozen_policy
from ternary_adaptive_shell import compile_adaptive
from ternary_prefix_integrality import prefix_geometry
from ternary_prefix_moments import moment_model, word_moments, verify_moments
from ternary_event_triangles import event_subsets, triangle_coefficients, verify_triangle, scan_triangles


def fixture(domains=((0,1),)*3):
    p=LowProblem((81,),(((9,),(23,)),((41,),(37,)),((65,),(19,))),0)
    policy=frozen_policy(p,_serialized_prepared(public_charts(p,83950)));compiled=compile_adaptive(policy)
    return moment_model(prefix_geometry(p,(0,),policy,compiled,6,(0,)*6,domains))


def correlation_point(m,r=fmpq(-2,5)):
    values=[fmpq(1,2) if k[0]=="p" else (1+r if k[2]==k[4] else 1-r)/4 for k in m["variables"]]
    assert verify_moments(m,values)["valid"];return values


def test_nonPSD_event_inequality_detects_false_psd_triangle_without_any_LP(monkeypatch):
    m=fixture();values=correlation_point(m)
    import scipy.optimize
    monkeypatch.setattr(scipy.optimize,"linprog",lambda *a,**k:(_ for _ in ()).throw(AssertionError("no LP allowed")))
    result=scan_triangles(m,values);trial=result["triple_trials"][0]
    assert trial["certificate"]["rejects_THIS_point"]
    assert trial["status"]=="EXACT_EVENT_TRIANGLE_NATIVE_OBSTRUCTION"
    assert result["cost"]["LP_calls"]==0 and result["cost"]["event_combinations_evaluated"]==12
    assert fmpq(trial["certificate"]["exact_point_value"])<0
    assert not trial["certificate"]["proves_entire_relaxation_infeasible"]


def test_all_original_three_digit_words_satisfy_every_selected_event_triangle():
    m=fixture(((0,1,2),)*3)
    for word in product(range(3),repeat=3):
        result=scan_triangles(m,word_moments(m,word))
        assert result["cost"]["event_combinations_evaluated"]==324
        assert all(not t["certificate"] for t in result["triple_trials"])
        assert result["no_violations_is_not_local_extendability_proof"]
    proof=verify_triangle(m,word_moments(m,(0,1,2)),(0,1,2),((0,2),(0,1),(1,2)),0)
    assert all(a in (0,1) for a in proof["local_assignment_values"])


def test_uniform_native_mixture_passes_but_is_not_promoted_to_global_proof():
    m=fixture(((0,1,2),)*3);words=list(product(range(3),repeat=3));points=[word_moments(m,w) for w in words]
    values=[sum(p[j] for p in points)*fmpq(1,27) for j in range(len(points[0]))]
    result=scan_triangles(m,values)
    assert all(not t["certificate"] for t in result["triple_trials"])
    assert not result["global_native_distribution_proved"]


def test_complementing_all_three_events_preserves_the_exact_inequality_value():
    m=fixture();values=correlation_point(m);events=((0,),(1,),(0,));opposite=((1,),(0,),(1,))
    for center in range(3):
        a=verify_triangle(m,values,(0,1,2),events,center);b=verify_triangle(m,values,(0,1,2),opposite,center)
        assert a["exact_point_value"]==b["exact_point_value"]
        assert a["local_assignment_values"]==b["local_assignment_values"]


@pytest.mark.parametrize("blocks,events,center",[
    ((0,0,2),((0,),(0,),(0,)),0),((2,1,0),((0,),(0,),(0,)),0),
    ((0,1,3),((0,),(0,),(0,)),0),((True,1,2),((0,),(0,),(0,)),0),
    ((0,1,2),((),(0,),(0,)),0),((0,1,2),((0,1),(0,),(0,)),0),
    ((0,1,2),((2,),(0,),(0,)),0),((0,1,2),((0,),(0,),(0,)),True),
])
def test_bad_events_original_indices_and_centers_fail_closed(blocks,events,center):
    with pytest.raises(ValueError):triangle_coefficients(fixture(),blocks,events,center)


def test_whole_family_preflight_is_unknown_not_a_pass():
    m=fixture();result=scan_triangles(m,correlation_point(m),event_budget=1)
    assert result["status"]=="EVENT_TRIANGLE_PREFLIGHT_UNKNOWN" and not result["triple_trials"]
    assert result["cost"]["event_combinations_evaluated"]==0 and result["cost"]["LP_calls"]==0
    with pytest.raises(ValueError):scan_triangles(m,correlation_point(m),event_budget=0)


def test_bad_moments_are_not_accepted_because_a_cached_sum_looks_positive():
    m=fixture();values=correlation_point(m);values[0]=-1
    with pytest.raises(ValueError):scan_triangles(m,values)
    with pytest.raises(ValueError):verify_triangle(m,values,(0,1,2),((0,),(0,),(0,)),0)


def test_native_domains_of_size_one_do_not_create_improper_events():
    assert event_subsets((2,))==()
    m=fixture(((0,),(0,1),(0,1)));values=word_moments(m,(0,0,0));result=scan_triangles(m,values)
    assert result["cost"]["event_combinations_preflight"]==0
    assert result["triple_trials"][0]["certificate"] is None
