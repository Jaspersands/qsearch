from itertools import product

from flint import fmpq
import pytest

from ternary_pair_lattice import embed, word_coordinates
from ternary_native_dual_separation import (
    integer_separator, project_high, search_separator, support_vertex, verify_integer_separator,
)
from ternary_adaptive_shell import adaptive_pair, native_cut
from ternary_pair_collimation import LowProblem
from ternary_pair_cell_coverage import public_charts, _serialized_prepared
from ternary_repair_catalog import frozen_policy
from ternary_adaptive_shell import compile_adaptive


def view(A=(1,7,11,18),Q=27):
    return LowProblem((Q,),tuple(((a,),(b,)) for a,b in zip(A[::2],A[1::2])),0)


def prepared(problem):
    policy = frozen_policy(problem,_serialized_prepared(public_charts(problem,83950)))
    return policy,compile_adaptive(policy)


def test_native_support_is_exact_over_all_original_words():
    h = tuple(map(fmpq,(7,-3,-4,-1,3,-2)))
    vertex, support = support_vertex(h)
    values = []
    for word in product(range(3),repeat=2):
        e = embed(tuple(1-3*x for x in word_coordinates(word)))
        values.append(sum(a*b for a,b in zip(h,e)))
    assert support == max(values) == sum(a*b for a,b in zip(h,vertex))
    assert integer_separator((fmpq(-1,7),fmpq(1,7),fmpq(0))) == (-1,1,0)


def test_strict_dual_finds_coupled_separator_when_radial_simplex_cut_passes():
    problem = view((1,2),9); policy, compiled = prepared(problem)
    p = (fmpq(-11,10),fmpq(11,10),fmpq(0))
    spent = sum(x*x for x in p)
    assert native_cut(p,spent,fmpq(6)-spent)[0]
    answer = search_separator(compiled,p,0,8)
    assert answer["status"] == "STRICT_NATIVE_PREFIX_SEPARATOR"
    h = answer["direction"]
    assert sum(a*b for a,b in zip(p,h)) > 3*max(h)


def test_convex_membership_is_never_promoted_to_native_word_or_pair():
    problem = view((1,2),9); policy, compiled = prepared(problem)
    p = (fmpq(1,2),fmpq(1,2),fmpq(-1))
    answer = search_separator(compiled,p,0,8)
    assert not answer["direction"]
    assert answer["status"] == "IN_PROJECTED_CONVEX_HULL_NOT_A_NATIVE_WORD"
    assert sum(x*x for x in p) == fmpq(3,2) != 6


def test_no_actual_word_projection_at_any_depth_can_be_separated():
    problem = view((9,23,41,37,65,19),81); policy, compiled = prepared(problem)
    for word in product(range(3),repeat=problem.width):
        e = embed(tuple(1-3*x for x in word_coordinates(word)))
        for bottom in range(2*problem.width+1):
            p = project_high(compiled,e,bottom)
            assert not search_separator(compiled,p,bottom,4)["direction"]


def test_integer_branch_certificate_does_not_trust_gs_or_floating_separation():
    rows = ((3,0,-3),(0,3,-3)); T = (-2,1,1); c = (0,0)
    answer = verify_integer_separator(rows,T,c,0,(-2,1,1))
    assert answer["valid"] and answer["strict_margin"] == "3"
    assert not verify_integer_separator(rows,(-1,2,-1),c,0,(-2,1,1))["valid"]
    with pytest.raises(ValueError,match="orthogonal"):
        verify_integer_separator(rows,T,c,1,(-2,1,1))
    with pytest.raises(ValueError,match="planes"):
        verify_integer_separator(rows,T,c,0,(1,1,1))


def test_dual_cut_matches_every_real_two_register_fiber_and_cap_semantics():
    problem = view(); policy, compiled = prepared(problem)
    for target in range(27):
        expected = [w for w in product(range(3),repeat=2) if problem.value(w)==(target,)]
        answer = adaptive_pair(problem,(target,),policy,compiled,100_000,"dual",False)
        assert answer["complete_fiber"] and sorted(answer["witnesses"]) == expected
        assert answer["cost"]["dual_search_calls"] <= 16
        assert len(answer["dual_certificates"]) == answer["cost"]["dual_separator_prunes"]
    with pytest.raises(ValueError): adaptive_pair(problem,(0,),policy,compiled,cut="dual",max_dual_calls=0)


def test_invalid_projection_budget_and_directions_fail_closed():
    problem = view(); policy, compiled = prepared(problem)
    with pytest.raises(ValueError): search_separator(compiled,(0,)*6,0,0)
    with pytest.raises(ValueError): support_vertex((1,1,1))
    e = tuple(map(fmpq,embed((1,1,1,1))))
    with pytest.raises(ValueError,match="outside"):
        search_separator(compiled,e,2)
