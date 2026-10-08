from itertools import product
from types import SimpleNamespace

from flint import fmpq, fmpq_mat
import numpy as np
import pytest

from ternary_pair_collimation import LowProblem
from ternary_pair_cell_coverage import public_charts, _serialized_prepared
from ternary_pair_lattice import word_coordinates, coset_target
from ternary_repair_catalog import frozen_policy
from ternary_adaptive_shell import compile_adaptive
from ternary_prefix_integrality import prefix_geometry
from ternary_prefix_moments import moment_model, verify_moments, word_moments, analyze_moments, verify_moment_dual


def prepared(A=(9,23,41,37,65,19),Q=81):
    p=LowProblem((Q,),tuple(((a,),(b,)) for a,b in zip(A[::2],A[1::2])),0)
    policy=frozen_policy(p,_serialized_prepared(public_charts(p,83950)))
    return p,policy,compile_adaptive(policy)


@pytest.mark.parametrize("A,Q",[((9,23,41,37,65,19),81),((0,3,6,0),27),((0,0),9)])
def test_every_actual_native_word_provides_true_coupled_moments_at_every_prefix(A,Q):
    p,policy,c=prepared(A,Q); K=fmpq_mat(c["basis"]["kernel_rows"]).transpose();d=2*p.width
    for word in product(range(3),repeat=p.width):
        t=p.value(word);z0,_=coset_target(p,t,policy["geometry"])
        full=K.solve(fmpq_mat([[a-b] for a,b in zip(word_coordinates(word),z0)]))
        coeff=tuple(int(full[i,0].p) for i in range(d))
        for b in range(d+1):
            partial=tuple(0 if i<b else x for i,x in enumerate(coeff))
            g=prefix_geometry(p,t,policy,c,b,partial)
            winding=(sum(a*z for a,z in zip(g["A"],word_coordinates(word)))-t[0])//Q
            model=moment_model(g,winding);values=word_moments(model,word)
            assert verify_moments(model,values)["valid"]
            # Domain restriction is exact, not an untested independent-bit model.
            g["domains"]=tuple((x,) if j==0 else (0,1,2) for j,x in enumerate(word))
            model=moment_model(g,winding)
            assert verify_moments(model,word_moments(model,word))["valid"]


def test_floating_negative_inconsistent_and_wrong_winding_moments_fail_closed():
    p,policy,c=prepared((1,2),9);g=prefix_geometry(p,(0,),policy,c,2,(0,0))
    model=moment_model(g,0); values=list(word_moments(model,(0,)))
    assert verify_moments(model,values)["valid"]
    values[0]-=fmpq(1,10**50)
    assert not verify_moments(model,values)["valid"]
    with pytest.raises(ValueError): verify_moments(model,[0.1]*len(values))
    with pytest.raises(ValueError): moment_model(g,True)
    with pytest.raises(ValueError): word_moments(model,(3,))
    assert not verify_moments(moment_model(g,1),word_moments(model,(0,)))["valid"]


def test_exact_dual_obstruction_and_true_word_positive_control():
    p,policy,c=prepared((1,2),9);g=prefix_geometry(p,(0,),policy,c,2,(0,0))
    impossible=moment_model(g,1); result=analyze_moments(impossible)
    assert result["dual"] and result["dual"]["valid"]
    y=result["dual"]["signed_equation_multipliers"]
    assert verify_moment_dual(impossible,y)["valid"]
    assert not verify_moment_dual(impossible,["0"]*len(y))["valid"]
    assert not verify_moment_dual(impossible,[str(-fmpq(x)) for x in y])["valid"]
    honest=analyze_moments(moment_model(g,0))
    assert honest["primal"]["valid"] and honest["dual"] is None


def test_numeric_flags_and_reconstruction_guards_are_never_proofs(monkeypatch):
    import ternary_prefix_moments as module
    p,policy,c=prepared();g=prefix_geometry(p,(0,),policy,c,6,(0,)*6);m=moment_model(g)
    monkeypatch.setattr(module,"linprog",lambda *a,**k:SimpleNamespace(success=False,status=2))
    answer=analyze_moments(m)
    assert answer["primal"] is None and answer["dual"] is None
    assert answer["numerical_infeasibility_not_proof"]
    monkeypatch.setattr(module,"linprog",lambda *a,**k:SimpleNamespace(success=True,x=np.ones(len(m["variables"]))))
    answer=analyze_moments(m,1)
    assert answer["primal"] is None and answer["unknown_not_infeasible"]
    assert answer["cost"]["reconstruction_attempts"]==0
    with pytest.raises(ValueError): analyze_moments(m,0)


def test_conditional_joint_rows_are_not_only_independent_marginal_constraints():
    p,policy,c=prepared();g=prefix_geometry(p,(0,),policy,c,3,(0,)*6);m=moment_model(g,0)
    assert any(name[0]=="condition" for name in m["row_names"])
    assert any(name[0]=="left_marginal" for name in m["row_names"])
    assert len(m["variables"])==9+3*9
    assert all(type(a) is int for row in m["rows"] for a in row.values())
    assert all(type(B) is int for B in m["rhs"])
