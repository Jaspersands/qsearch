from copy import deepcopy
from fractions import Fraction
from itertools import product
from types import SimpleNamespace

from flint import fmpq, fmpq_mat
import numpy as np
import pytest

from ternary_pair_collimation import LowProblem
from ternary_pair_cell_coverage import public_charts, _serialized_prepared
from ternary_pair_lattice import coset_target, word_coordinates, embed
from ternary_repair_catalog import frozen_policy
from ternary_adaptive_shell import adaptive_pair, compile_adaptive
from ternary_prefix_integrality import (
    frontier_geometry, linear_constraints, prefix_geometry, prepare_reference,
    propose_primal, rational, recover_active_primal, reference_prefix, verify_primal,
    exact_affine_proposal, propose_farkas, verify_farkas,
)


def view(A=(1,7,11,18),Q=27):
    return LowProblem((Q,),tuple(((a,),(c,)) for a,c in zip(A[::2],A[1::2])),0)


def prepared(problem):
    policy=frozen_policy(problem,_serialized_prepared(public_charts(problem,83950)))
    return policy,compile_adaptive(policy)


def coefficients(problem,target,compiled,policy,word):
    z0,_=coset_target(problem,target,policy["geometry"])
    delta=[a-b for a,b in zip(word_coordinates(word),z0)]
    K=fmpq_mat(compiled["basis"]["kernel_rows"]).transpose()
    solution=K.solve(fmpq_mat([[x] for x in delta]))
    assert all(solution[i,0].q==1 for i in range(solution.nrows()))
    return tuple(int(solution[i,0].p) for i in range(solution.nrows()))


@pytest.mark.parametrize("A,Q",[((1,7,11,18),27),((0,3),9),((0,0,0,0),27)])
def test_every_true_native_word_at_every_prefix_has_exact_integral_primal(A,Q):
    problem=view(A,Q); policy,compiled=prepared(problem); d=2*problem.width
    for word in product(range(3),repeat=problem.width):
        target=problem.value(word); full=coefficients(problem,target,compiled,policy,word)
        for b in range(d+1):
            partial=tuple(0 if i<b else x for i,x in enumerate(full))
            g=prefix_geometry(problem,target,policy,compiled,b,partial)
            offsets=tuple(full[i]-g["anchor"][i] for i in range(b))
            cert=verify_primal(g,offsets)
            assert cert["valid"] and cert["actual_native_word"]==word and cert["integral_winding"]
            winding=int(rational(cert["winding"]).p)
            assert winding in g["allowed_integral_windings"]
            assert verify_primal(g,offsets,winding)["valid"]
            e=embed(tuple(1-3*x for x in word_coordinates(word)))
            for gs in compiled["gs"][b:]:
                assert sum(a*v for a,v in zip(e,gs))==sum(a*v for a,v in zip(g["H"],gs))


def test_exact_verifier_rejects_tiny_negativity_wrong_domains_and_wrong_winding():
    problem=view((1,2),9); policy,compiled=prepared(problem)
    g=prefix_geometry(problem,(0,),policy,compiled,2,(0,0))
    K=fmpq_mat(g["kernel_prefix"]).transpose()
    desired=(fmpq(-1,10**50),fmpq(0))
    offsets=K.solve(fmpq_mat([[x-y] for x,y in zip(desired,g["z_anchor"])]))
    assert not verify_primal(g,tuple(offsets[i,0] for i in range(2)))["valid"]
    desired=(fmpq(1),fmpq(0))
    offsets=K.solve(fmpq_mat([[x-y] for x,y in zip(desired,g["z_anchor"])]))
    y=tuple(offsets[i,0] for i in range(2))
    cert=verify_primal(g,y)
    assert cert["valid"] and cert["vertex_has_wrong_original_target"] and not cert["integral_winding"]
    assert not verify_primal(g,y,0)["valid"]
    restricted=prefix_geometry(problem,(0,),policy,compiled,2,(0,0),((0,2),))
    assert not verify_primal(restricted,y)["valid"]
    assert not cert["nontrivial_assigned_prefix"]


def test_exact_reconstruction_does_not_rationalize_the_numerical_point_itself():
    problem=view((1,2),9); policy,compiled=prepared(problem)
    g=prefix_geometry(problem,(0,),policy,compiled,2,(0,0))
    result=propose_primal(g)
    assert result["certificate"]["valid"]
    certificate=result["certificate"]
    noisy=np.array([float(rational(x))+1e-9 for x in certificate["rational_offsets"]])
    recovered=recover_active_primal(g,noisy)
    assert recovered["certificate"]["valid"]
    assert recovered["certificate"]["rational_offsets"]==certificate["rational_offsets"]
    unranked=recover_active_primal(g,np.array([999.1,997.2]))
    assert unranked["certificate"] is None
    with pytest.raises(ValueError): recover_active_primal(g,[float("nan"),0])


def test_numerical_success_or_failure_is_never_an_exact_feasibility_claim(monkeypatch):
    import ternary_prefix_integrality as module
    problem=view(); policy,compiled=prepared(problem)
    g=prefix_geometry(problem,(0,),policy,compiled,4,(0,0,0,0))
    monkeypatch.setattr(module,"linprog",lambda *a,**k:SimpleNamespace(success=False,status=2,nit=0))
    answer=propose_primal(g)
    assert answer["certificate"] is None and answer["failure_is_not_infeasibility_proof"]
    monkeypatch.setattr(module,"linprog",lambda *a,**k:SimpleNamespace(success=True,x=np.array([999.1]*4),nit=0))
    answer=propose_primal(g)
    assert answer["certificate"] is None


def test_terminal_and_degenerate_active_constraints_are_checked_exactly():
    problem=view((0,0),9); policy,compiled=prepared(problem)
    g=prefix_geometry(problem,(0,),policy,compiled,2,(0,0),((0,),))
    answer=propose_primal(g,0)
    assert answer["certificate"]["valid"] and answer["certificate"]["actual_native_word"]==(0,)
    full=coefficients(problem,(0,),compiled,policy,(2,))
    terminal=prefix_geometry(problem,(0,),policy,compiled,0,full)
    assert propose_primal(terminal)["certificate"]["actual_native_word"]==(2,)
    assert not verify_primal(terminal,(),1)["valid"]


def test_reference_matches_every_original_word_and_prefix_including_nonunits():
    for A in ((1,7,11,18),(0,3,6,0),(0,0,0,0)):
        problem=view(A); policy,compiled=prepared(problem); reference=prepare_reference(problem)
        K=compiled["basis"]["kernel_rows"]
        for t in range(27):
            if coset_target(problem,(t,),policy["geometry"]) is None: continue
            g=prefix_geometry(problem,(t,),policy,compiled,2,(0,0,0,0))
            truth=reference_prefix(g,reference)
            actual=[w for w in product(range(3),repeat=2) if problem.value(w)==(t,)]
            assert sorted(truth["whole_target_fiber"])==actual
            expected=[]
            for word in actual:
                full=coefficients(problem,(t,),compiled,policy,word)
                if full[2:]==(0,0): expected.append(word)
            assert sorted(truth["native_prefix_words"])==expected
            assert truth["right_hash_lookups"]==3


def test_reference_caps_and_incomplete_truth_are_not_empty_prefixes():
    problem=view((0,0,0,0),27); policy,compiled=prepared(problem)
    g=prefix_geometry(problem,(0,),policy,compiled,2,(0,0,0,0))
    guarded=prepare_reference(problem,2)
    assert guarded["half_assignments_enumerated"]==0
    assert reference_prefix(g,guarded)["native_prefix_words"] is None
    capped=reference_prefix(g,prepare_reference(problem),1)
    assert capped["native_prefix_words"] is None and "CAP" in capped["status"]


def test_frontiers_are_real_passed_parent_branches_and_replay_their_energy():
    problem=view((9,23,41,37,65,19),81); policy,compiled=prepared(problem)
    seen=0
    for t in range(81):
        answer=adaptive_pair(problem,(t,),policy,compiled,4,"projector")
        cp=answer["cap_frontier"]
        if cp is None or cp["unassigned_rows"]==6: continue
        g=frontier_geometry(problem,(t,),policy,compiled,cp)
        assert g["nontrivial_assigned_prefix"] and all(g["domains"])
        assert not any(cp["partial_coefficients"][:cp["unassigned_rows"]])
        broken=deepcopy(cp); broken["assigned_squared_energy"]="999"
        with pytest.raises(ValueError,match="energy"): frontier_geometry(problem,(t,),policy,compiled,broken)
        seen+=1
    assert seen>0


def test_floating_and_noncanonical_inputs_fail_closed():
    for x in (True,0.1,"0.1","2/2","nan"):
        with pytest.raises((ValueError,ZeroDivisionError)): rational(x)
    assert rational(Fraction(1,3))==fmpq(1,3)
    problem=view(); policy,compiled=prepared(problem)
    with pytest.raises(ValueError): prefix_geometry(problem,(0,),policy,compiled,2,(1,0,0,0))
    with pytest.raises(ValueError): prefix_geometry(problem,(0,),policy,compiled,2,(0,0,0,0),((0,),(0,0)))
    with pytest.raises(ValueError): prefix_geometry(view((1,2,3,4)),(0,),policy,compiled,2,(0,0,0,0))
    with pytest.raises(ValueError): verify_primal(prefix_geometry(problem,(0,),policy,compiled,2,(0,0,0,0)),(0.1,0))


def test_underranked_face_can_use_guessed_free_coordinates_only_after_exact_checks():
    candidates=list(exact_affine_proposal([[1,1,1]],np.array([0.500000001,0.499999999])))
    assert candidates
    point,metadata=candidates[0]
    assert sum(point)==1 and metadata["active_rank"]==1
    assert metadata["free_coordinate_proposals"]==[1]
    assert not list(exact_affine_proposal([[1,0,0],[1,0,1]],np.array([0,0])))


def test_farkas_certificates_are_exact_strict_and_cannot_obstruct_true_native_words():
    problem=view(); policy,compiled=prepared(problem)
    impossible=prefix_geometry(problem,(0,),policy,compiled,0,(10,0,0,0))
    result=propose_farkas(impossible)
    cert=result["certificate"]
    assert cert["valid"] and cert["exact_combined_rhs"]=="-1"
    assert verify_farkas(impossible,cert["nonnegative_inequality_multipliers"])["valid"]
    broken=list(cert["nonnegative_inequality_multipliers"])
    i=next(i for i,x in enumerate(broken) if rational(x)>0)
    broken[i]=str(-rational(broken[i]))
    assert not verify_farkas(impossible,broken)["valid"]
    zero=["0"]*len(broken)
    assert not verify_farkas(impossible,zero)["valid"]
    for word in ((0,0),(1,2),(2,1)):
        t=problem.value(word); full=coefficients(problem,t,compiled,policy,word)
        g=prefix_geometry(problem,t,policy,compiled,2,(0,0,*full[2:]))
        assert propose_farkas(g)["certificate"] is None
        winding=(sum(a*x for a,x in zip(g["A"],word_coordinates(word)))-t[0])//g["Q"]
        assert propose_farkas(g,winding)["certificate"] is None


def test_exact_integral_winding_gap_on_a_nontrivial_original_native_prefix():
    problem=view((9,23,41,37,65,19),81); policy,compiled=prepared(problem); reference=prepare_reference(problem)
    found=False
    for t in range(81):
        g=prefix_geometry(problem,(t,),policy,compiled,3,(0,0,0,0,0,0))
        truth=reference_prefix(g,reference)
        if truth["native_prefix_words"]: continue
        for k in g["allowed_integral_windings"]:
            result=propose_primal(g,k); cert=result["certificate"]
            if cert and cert["valid"]:
                assert cert["integral_winding"] and cert["actual_native_word"] is None
                assert not cert["native_simplex_vertex"] and g["nontrivial_assigned_prefix"]
                assert not propose_farkas(g,k)["certificate"]
                found=True; break
        if found: break
    assert found


def test_numerical_dual_success_with_zero_multipliers_is_not_a_certificate(monkeypatch):
    import ternary_prefix_integrality as module
    problem=view(); policy,compiled=prepared(problem)
    g=prefix_geometry(problem,(0,),policy,compiled,4,(0,0,0,0))
    monkeypatch.setattr(module,"linprog",lambda c,**k:SimpleNamespace(success=True,x=np.zeros(len(c)),nit=0))
    assert propose_farkas(g)["certificate"] is None


def test_fixed_winding_obstruction_cannot_be_reused_as_a_global_obstruction():
    problem=view((1,2),9); policy,compiled=prepared(problem)
    g=prefix_geometry(problem,(0,),policy,compiled,2,(0,0))
    assert propose_primal(g)["certificate"]["valid"]
    fixed=propose_farkas(g,1)["certificate"]
    assert fixed["valid"] and fixed["required_winding"]==1
    weights=fixed["nonnegative_inequality_multipliers"]
    assert verify_farkas(g,weights,1)["valid"]
    with pytest.raises(ValueError,match="complete Farkas"):
        verify_farkas(g,weights)
    assert not verify_farkas(g,weights[:-2])["valid"]


def test_linear_decoder_matches_all81_original_three_register_target_fibers():
    problem=view((9,23,41,37,65,19),81); policy,compiled=prepared(problem)
    fibers={t:[] for t in range(81)}
    for word in product(range(3),repeat=3): fibers[problem.value(word)[0]].append(word)
    searches=0
    for t,expected in fibers.items():
        result=adaptive_pair(problem,(t,),policy,compiled,100_000,"linear",False,max_linear_calls=2)
        assert result["complete_fiber"] and sorted(result["witnesses"])==sorted(expected)
        assert result["cost"]["linear_LP_calls"]<=2
        assert len(result["linear_certificates"])==result["cost"]["linear_obstruction_prunes"]
        searches+=result["cost"]["linear_LP_calls"]
    assert searches>0
    with pytest.raises(ValueError): adaptive_pair(problem,(0,),policy,compiled,cut="linear",max_linear_calls=0)
