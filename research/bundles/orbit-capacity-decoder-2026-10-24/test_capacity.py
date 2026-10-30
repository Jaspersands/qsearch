from dataclasses import replace
from fractions import Fraction
from itertools import combinations, product
import random

from flint import nmod_mat
import pytest

import capacity as c


def small_case():
    g = c.o.geometry(31,3,6)
    return replace(g,representatives=g.representatives[:7])


def test_recover_source_beyond_old_cap_rank():
    g = small_case()
    rng = random.Random(241026)
    error = [[rng.randrange(31),rng.randrange(31),1] if i<4 else [0,0,0] for i in range(7)]
    syndrome = c.o.syndrome(g,error)
    assert c.o.cap_rank(g,5,syndrome)<=3<4
    assert c.o.decode(g,5,syndrome)["status"] != "VERIFIED_UNIQUE"
    result = c.complete_reference(g,5,syndrome)
    assert result["complete"] and result["errors"]==[error]
    assert result["status"]=="VERIFIED_UNIQUE"


def guard_case():
    g = small_case()
    delta = c.weights(g.nodes,g.p)
    word = c.unfold(g,[delta,[0]*7,[0]*7])
    assert not any(v for row in c.o.syndrome(g,word) for v in row)
    source = [row if i<3 else [0]*3 for i,row in enumerate(word)]
    other = [[0]*3 if i<3 else [(-v)%g.p for v in row] for i,row in enumerate(word)]
    return g,source,other


def test_full_guard_rejects_real_alias_outside_source_radius():
    g,source,other = guard_case()
    assert all(source[i][2] for i in range(3))
    s = c.o.syndrome(g,source)
    assert c.o.syndrome(g,other)==s
    assert c.complete_reference(g,3,s)["errors"]==[source]
    guarded = c.complete_reference(g,4,s)
    assert guarded["status"]=="REJECT_AMBIGUOUS"
    assert source in guarded["errors"] and other in guarded["errors"]


def test_scalar_dual_conversion_has_correct_weights():
    g = c.o.geometry(13,3,3)
    delta = c.weights(g.nodes,13)
    for constant in range(13):
        word = [(constant*v)%13 for v in delta]
        assert all(sum(word[i]*pow(z,j,13) for i,z in enumerate(g.nodes))%13==0
                   for j in range(3))


def support_enumeration(g,cap,syndromes):
    """Independent check: enumerate supports, not scalar code messages."""
    found = set()
    M,p,K = len(g.nodes),g.p,g.row_length
    if not any(v for row in syndromes for v in row):
        found.add((0,)*(3*M))
    for size in range(1,cap+1):
        for support in combinations(range(M),size):
            V = nmod_mat([[pow(g.nodes[i],j,p) for i in support] for j in range(size)],p)
            amplitudes = V.solve(nmod_mat([[syndromes[h][j] for h in range(3)]
                                          for j in range(size)],p))
            rows = [[0]*M for _ in range(3)]
            for j,i in enumerate(support):
                for h in range(3):
                    rows[h][i]=int(amplitudes[j,h])
            if any(sum(rows[h][i]*pow(g.nodes[i],j,p) for i in range(M))%p!=syndromes[h][j]
                   for h in range(3) for j in range(K)):
                continue
            error = c.unfold(g,rows)
            found.add(tuple(v for row in error for v in row))
    return found


def test_complete_lists_match_independent_support_enumeration():
    g = c.o.geometry(13,3,3)
    rng = random.Random(820261024)
    for trial in range(100):
        # Include received syndromes with no promised bounded source error.
        error = [[rng.randrange(13) for _ in range(3)] if i<trial%5 else [0]*3
                 for i in range(4)]
        syndromes = c.o.syndrome(g,error)
        reference = c.complete_reference(g,2,syndromes)
        assert reference["complete"]
        assert {tuple(v for row in e for v in row) for e in reference["errors"]} == \
            support_enumeration(g,2,syndromes)


def test_zero_cap_and_zero_source_remain_valid():
    g = small_case()
    zero = [[0]*6 for _ in range(3)]
    result = c.complete_reference(g,0,zero)
    assert result["complete"] and result["errors"]==[[[0]*3 for _ in range(7)]]
    assert result["status"]=="VERIFIED_UNIQUE"


def test_every_nonzero_source_has_an_endpoint_competitor():
    g = small_case()
    for block in range(7):
        for value in (1,2,30):
            source = [[0]*3 for _ in range(7)]
            source[block]=[0,0,value]
            s = c.o.syndrome(g,source)
            other = c.endpoint_competitor(g,s,block)
            assert other!=source and not any(other[block])
            assert sum(any(row) for row in other)<=g.row_length
            assert c.o.syndrome(g,other)==s
    with pytest.raises(ValueError):
        c.endpoint_competitor(replace(g,row_length=7),[[0]*7 for _ in range(3)],0)


def test_all_free_assignments_match_exact_collision_probability():
    g = c.o.geometry(13,3,3)
    matrix = c.annihilator_matrix(g,[2,3])
    assert matrix.rank()==3
    free = [0,1,3,4]
    sub = nmod_mat([[int(matrix[i,j]) for j in free] for i in range(3)],13)
    assert sub.rank()==3
    hits = []
    for values in product(range(13),repeat=4):
        if all((sum(int(matrix[i,j])*v for j,v in zip(free,values))+
                int(matrix[i,2])+2*int(matrix[i,5]))%13==0 for i in range(3)):
            hits.append(values)
    assert len(hits)==13
    assert Fraction(len(hits),13**4)==c.collision_bound(13,4,3,2,2)==Fraction(1,13**3)
    for values in hits:
        source = [list(values[:2])+[1],list(values[2:])+[2],[0]*3,[0]*3]
        result = c.complete_reference(g,2,c.o.syndrome(g,source))
        assert result["status"]=="REJECT_AMBIGUOUS"
        assert source in result["errors"]


def test_annihilator_ranks_hold_for_nonconsecutive_native_supports():
    g = small_case()
    for T in combinations(range(7),4):
        A = c.annihilator_matrix(g,T)
        assert A.rank()==6
        assert all(A[j,3*i+ell]==0 for i in T for ell in range(3) for j in range(6))
        remaining = [i for i in range(7) if i not in T]
        for count in range(1,4):
            cols = [3*i+ell for i in remaining[:count] for ell in (0,1)]
            assert nmod_mat([[int(A[j,col]) for col in cols] for j in range(6)],31).rank()==min(6,2*count)


def test_coarse_bound_dominates_all_finite_support_bounds():
    for M in range(3,15):
        for K in range(2,M+1):
            for C in range(K):
                coarse = c.collision_bound(43,M,K,C)
                for w in range(C+1):
                    assert c.collision_bound(43,M,K,C,w)<=coarse
    assert c.collision_bound(13,4,3,2,0)==0


def test_budgets_never_turn_partial_lists_into_singletons():
    g,source,_ = guard_case()
    s = c.o.syndrome(g,source)
    small = c.complete_reference(g,4,s,scalar_budget=30)
    assert small["status"]=="UNAVAILABLE_REFERENCE_BUDGET" and not small["complete"]
    capped = c.complete_reference(g,4,s,product_budget=1)
    assert capped["status"]=="UNAVAILABLE_PRODUCT_BUDGET" and not capped["complete"]
    assert "errors" not in small and "errors" not in capped


def test_union_support_not_sum_of_independent_row_acceptance():
    g = small_case()
    delta = c.weights(g.nodes,g.p)
    rows = [[v if i in support else 0 for i,v in enumerate(delta)]
            for support in ({0,1,2},{0,3,4},set())]
    result = c.complete_reference(g,4,c.o.syndrome(g,c.unfold(g,rows)))
    assert result["Cartesian_product_size"]>result["list_size"]
    assert result["status"]=="REJECT_EMPTY"
    assert all(sum(any(row) for row in error)<=4 for error in result["errors"])


def test_new_ledger_is_conditional_not_executed_quantum_evidence():
    row = c.ledger()
    assert Fraction(row["rate"])<Fraction(2,3)
    assert row["dimension"]==7863
    assert not row["old_full_rank_gate_holds"]
    assert Fraction(row["ideal_one_attempt_failure_upper_dyadic"])<Fraction(1,10**8)
    for key in ("external_capacity_theorem_finite_threshold_instantiated","capacity_backend_implemented",
                "quantum_circuit_executed","native_polynomial_produced","speedup_or_novelty_established"):
        assert row[key] is False


@pytest.mark.parametrize("bad_cap",[-1,6,True])
def test_invalid_cap_rejected(bad_cap):
    g = small_case()
    with pytest.raises(ValueError):
        c.complete_reference(g,bad_cap,[[0]*6 for _ in range(3)])
