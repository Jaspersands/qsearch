from dataclasses import replace
from fractions import Fraction
from itertools import product

from flint import nmod_mat
import pytest

import norm_flat as n


def projective_vectors(p, r):
    for pivot in range(r):
        for tail in product(range(p), repeat=r-pivot-1):
            yield [0]*pivot+[1]+list(tail)


def test_exact_threshold_does_not_dequantize_the_point_eight_example():
    row = n.parameters(n.geometry(12289,3,3276))
    assert row["dimension"] == 9828
    assert row["parity_rank"] == 2460
    assert row["flat_dimension"] == 1636
    assert not row["applicable"]
    assert row["one_attempt_failure_bound"] is None
    edge = n.parameters(n.geometry(2053,3,570))
    assert edge["flat_dimension"] == edge["parity_rank"] == 342
    assert edge["one_attempt_failure_bound"] == Fraction(1,2052)


def test_original_vandermonde_parity_not_random_mq():
    g,b,nu,_ = n.fixture(19,5,917)
    s = n.build(g,b,nu)
    for power in range(g.dimension):
        xyz = [[pow(o[j],power,g.p) for o in g.points] for j in range(3)]
        syndrome = s.hx*n.vector(xyz[0],g.p)+s.hy*n.vector(xyz[1],g.p)+s.hz*n.vector(xyz[2],g.p)
        assert syndrome == n.vector([0]*s.ledger["parity_rank"],g.p)


@pytest.mark.parametrize("p,K", [(19,5),(31,9),(43,12)])
def test_whole_norm_flat_has_zero_quadratic_and_polar_terms(p,K):
    g,b,nu,_ = n.fixture(p,K,917)
    s = n.build(g,b,nu)
    D, r = s.ledger["flat_dimension"], s.ledger["parity_rank"]
    assert nmod_mat([[int(s.wx[i,j]) for j in range(D)] for i in range(len(g.points))]
                    +[[int(s.wy[i,j]) for j in range(D)] for i in range(len(g.points))],p).rank()==D
    columns = [(n.values(s.wx*n.vector([int(j==a) for j in range(D)],p)),
                n.values(s.wy*n.vector([int(j==a) for j in range(D)],p))) for a in range(D)]
    for x,y in columns:
        assert n.quadratic_syndrome(s,x,y)==n.vector([0]*r,p)
    for x,y in columns:
        for xx,yy in columns:
            assert n.quadratic_syndrome(s,[(a+c)%p for a,c in zip(x,xx)],
                                       [(a+c)%p for a,c in zip(y,yy)])==n.vector([0]*r,p)


def test_all_381_projective_dual_maps_have_full_proved_rank():
    g,b,nu,_ = n.fixture(19,5,917)
    s = n.build(g,b,nu)
    count = 0
    for dual in projective_vectors(19,3):
        assert n.dual_derivative(s,dual).rank()==4
        count += 1
    assert count==381
    assert Fraction(count,19**4)<s.ledger["one_attempt_failure_bound"]


def test_extension_linearity_and_sharp_krylov_dimensions():
    g,b,nu,_ = n.fixture(19,5,917)
    s = n.build(g,b,nu)
    W = [[int(matrix[i,j]) for j in range(4)] for matrix in (s.wx,s.wy) for i in range(6)]
    thetaW = [[nu*int(s.wy[i,j])%19 for j in range(4)] for i in range(6)] + [
        [int(s.wx[i,j]) for j in range(4)] for i in range(6)]
    assert nmod_mat([a+b for a,b in zip(W,thetaW)],19).rank()==4
    dimensions = []
    for t in range(3):
        rows = [[pow(g.points[i][2],j,19)*int(matrix[i,a])%19
                 for j in range(t+1) for a in range(4)]
                for matrix in (s.wx,s.wy) for i in range(6)]
        dimensions.append(nmod_mat(rows,19).rank())
    assert dimensions==[4,6,8]
    assert dimensions[-1]+4==12


def test_fp_subspace_need_not_be_extension_linear():
    g,b,nu,_ = n.fixture(19,5,917)
    s = n.build(g,b,nu)
    # One real basis vector remains a quadratic-zero subspace but is not
    # theta-closed, so the extension-linear upper bound needs its premise.
    rows = [[int(s.wx[i,0]),nu*int(s.wy[i,0])%19] for i in range(6)]+[
        [int(s.wy[i,0]),int(s.wx[i,0])] for i in range(6)]
    assert nmod_mat(rows,19).rank()==2


def singular_center(s):
    dual = [1]+[0]*(s.ledger["parity_rank"]-1)
    derivative = n.dual_derivative(s,dual)
    rhs = n.vector([-int(s.linear[0,j]) for j in range(s.ledger["flat_dimension"])],s.g.p)
    center,rank = n.full_row_solve(derivative,rhs)
    assert rank==s.ledger["flat_dimension"]
    return center


def test_a_constructed_bad_center_is_a_paid_retry_not_a_native_negative():
    g,b,nu,allowed = n.fixture(19,5,917)
    s = n.build(g,b,nu)
    center = singular_center(s)
    matrix,_ = n.linear_system(s,center,[min(a) for a in allowed])
    assert all(matrix[0,j]==0 for j in range(s.ledger["flat_dimension"]))
    result = n.attempt(s,allowed,center)
    assert result["status"]=="RETRY_RANK"
    assert "coefficients" not in result
    assert n.solve(g,b,nu,allowed,seed=918)["status"]=="VERIFIED_NATIVE_PERFECT"


def test_failed_centers_are_counted_and_saved(monkeypatch):
    g,b,nu,allowed = n.fixture(19,5,917)
    center = singular_center(n.build(g,b,nu))
    draws = iter(center*2)

    class FixedCoins:
        def randrange(self,p):
            return next(draws)

    monkeypatch.setattr(n.random,"Random",lambda seed: FixedCoins())
    result = n.solve(g,b,nu,allowed,seed=10,attempts=2)
    assert result["status"]=="RETRY_RANK"
    assert result["attempts_executed"]==2
    assert result["work"]["random_field_draws"]==24
    assert len(result["attempt_history"])==2


@pytest.mark.parametrize("p,K", [(19,5),(31,9),(43,12),(97,27),(193,54)])
def test_native_perfect_outputs_keep_original_degree_and_every_predicate(p,K):
    g,b,nu,allowed = n.fixture(p,K,917)
    result = n.solve(g,b,nu,allowed,seed=918)
    assert result["status"]=="VERIFIED_NATIVE_PERFECT"
    checked = n.verify(g,b,nu,allowed,result["coefficients"])
    assert checked["all_predicates_pass"]
    assert checked["degree"]<g.dimension
    assert checked["residuals"]==[min(row) for row in allowed]


def test_adversarial_nonrandom_halfsets_and_nonconsecutive_orbits():
    original,b,nu,_ = n.fixture(43,12,917)
    g = replace(original, representatives=original.representatives[1::2], row_length=6)
    b = tuple(b[1::2])
    allowed = [tuple(range(1,(g.p+1)//2)) for _ in g.points]
    result = n.solve(g,b,nu,allowed,seed=918)
    assert result["status"]=="VERIFIED_NATIVE_PERFECT"
    assert result["verification"]["residuals"]==[1]*len(g.points)


def test_below_threshold_is_unresolved_not_unsatisfiable():
    g,b,nu,allowed = n.fixture(31,8,917)
    result = n.solve(g,b,nu,allowed,seed=918)
    assert result["status"]=="OUTSIDE_CERTIFIED_RANK_GATE"
    assert not result["hardness_or_infeasibility_claim"]


def test_broken_norm_scale_destroys_the_flat():
    g,b,nu,_ = n.fixture(19,5,917)
    s = n.build(g,b,nu)
    s.wx[0,0] = (int(s.wx[0,0])+1)%g.p
    column = n.vector([1,0,0,0],g.p)
    assert n.quadratic_syndrome(s,n.values(s.wx*column),n.values(s.wy*column)) != n.vector([0]*3,g.p)


@pytest.mark.parametrize("mutation", ["square", "zero_multiplier", "missing_table", "duplicate_value", "oversized_polynomial"])
def test_reject_changed_or_invalid_native_contracts(mutation):
    g,b,nu,allowed = n.fixture(19,5,917)
    with pytest.raises(ValueError):
        if mutation=="square":
            n.build(g,b,1)
        elif mutation=="zero_multiplier":
            n.build(g,(0,)+b[1:],nu)
        elif mutation=="missing_table":
            n.solve(g,b,nu,allowed[:-1])
        elif mutation=="duplicate_value":
            n.solve(g,b,nu,((1,)*9,)+allowed[1:])
        else:
            n.verify(g,b,nu,allowed,[0]*(g.dimension+1))
