from collections import Counter,defaultdict
from fractions import Fraction
from itertools import product
import json

import numpy as np
import pytest

from theorems.dcp_nonlinear_fiber_pairing import phase_value
from theorems.dcp_weighted_fiber_moment_search import (
    REPORT, exact_witness, local_search, native_cube_count, paid_fiber,
    pair_buckets, support_structure,
)


def direct_moment(A,t,F,weights):
    buckets=defaultdict(int)
    for i,a in enumerate(F):
        if not weights[i]:
            continue
        fa=phase_value(A,a,1 << t)
        for j,b in enumerate(F):
            if not weights[j]:
                continue
            fb=phase_value(A,b,1 << t)
            buckets[tuple((x+y)%(1 << t) for x,y in zip(fa,fb))]+=weights[i]*weights[j]
    return Fraction(sum(v*v for v in buckets.values()),sum(w*w for w in weights)**2)


def test_paid_MITM_matches_every_one_row_coarse_source_and_syndrome():
    for row in product(range(4),repeat=4):
        A=(row,)
        for y in range(4):
            expected=[x for x in range(16) if phase_value(A,x,4)==(y,)]
            if not expected:
                with pytest.raises(ValueError,match="zero-probability"):
                    paid_fiber(A,3,(y,))
                continue
            F,c=paid_fiber(A,3,(y,))
            assert F==expected
            assert c["half_table_entries"]==[4,4]
            assert Fraction(c["Born_syndrome_probability_exact"])==Fraction(len(F),16)
            assert not c["polynomial_time_in_n_claimed"]


def test_packed_full_frequency_groups_do_not_carry_between_components():
    A=((15,14,5),(13,11,7))
    F=list(range(8))
    ids,counts=pair_buckets(A,4,F)
    groups=defaultdict(list)
    for i,j in product(range(8),repeat=2):
        a,b=phase_value(A,i,16),phase_value(A,j,16)
        groups[tuple((x+y)%16 for x,y in zip(a,b))].append((i,j))
    assert sorted(counts.tolist())==sorted(map(len,groups.values()))
    assert len({ids[i,j] for pairs in groups.values() for i,j in pairs})==len(groups)
    for pairs in groups.values():
        assert len({int(ids[i,j]) for i,j in pairs})==1
    w=list(range(1,9))
    assert Fraction(exact_witness(ids,w)["fourth_moment_exact"])==direct_moment(A,4,F,w)


def test_local_search_is_only_a_monotone_lower_bound_and_exact_replay():
    A=((4,8,16),)
    ids,counts=pair_buckets(A,5,list(range(8)))
    w,traces=local_search(ids,seed=7,restarts=3,steps=12)
    assert Fraction(w["fourth_moment_exact"])==8
    assert direct_moment(A,5,list(range(8)),w["integer_weights"])==8
    assert all(t["objective_last"]>=t["objective_first"]-1e-10 for t in traces)
    assert not w["global_optimality_proved"]
    assert not w["large_moment_is_a_mutual_information_lower_bound"]
    assert max(counts)==8


def cubes(m,d):
    result=set()
    for assignment in product(range(d+1),repeat=m):
        if any(j not in assignment for j in range(1,d+1)):
            continue
        directions=[sum((a==j) << i for i,a in enumerate(assignment)) for j in range(1,d+1)]
        for origin in range(1 << m):
            words=[]
            for u in range(1 << d):
                x=origin
                for i,v in enumerate(directions):
                    if u >> i & 1:
                        x^=v
                words.append(x)
            result.add(tuple(sorted(words)))
    return sorted(result)


@pytest.mark.parametrize("n,m,d",[(1,3,1),(1,4,2),(1,4,3),(2,3,2)])
def test_exact_Born_cube_first_moment_against_complete_native_source_census(n,m,d):
    geometry=cubes(m,d)
    c=native_cube_count(n,m,d)
    assert len(geometry)==int(c["distinct_unordered_physical_cubes"])
    born_total=all_total=0
    for flat in product(range(4),repeat=n*m):
        A=[flat[l*m:(l+1)*m] for l in range(n)]
        y=[phase_value(A,x,4) for x in range(1 << m)]
        occupancies=Counter(y)
        for cube in geometry:
            if all(y[x]==y[cube[0]] for x in cube):
                all_total+=1
                born_total+=occupancies[y[cube[0]]]
    assert Fraction(all_total,4**(n*m))==Fraction(c["expected_cubes_over_all_fibers_exact"])
    assert Fraction(born_total,4**(n*m)*2**m)==Fraction(c["expected_cubes_in_Born_sampled_fiber_exact"])
    uniform_syndrome=Fraction(all_total,4**(n*m+n))
    assert Fraction(c["expected_cubes_in_Born_sampled_fiber_exact"])>uniform_syndrome
    assert not c["covers_arbitrary_weights_or_all_high_moment_motifs"]


def test_sparse_covariant_completion_is_physically_complete_but_has_paid_mass():
    # A proper support in a Sidon fiber: complete its covariant orbit by diagonal padding.
    A,t,F=((1,5,13,29),),6,[1,2,4,8]
    ids,_=pair_buckets(A,t,F)
    integers=[1,1,0,0]
    c=exact_witness(ids,integers)
    w=np.array(integers)/np.linalg.norm(integers)
    states=np.array([[np.exp(2j*np.pi*phase_value(A,x,64)[0]*s/64)/2 for x in F] for s in range(16)])
    beta=1/max(abs(w)**2)
    vectors=np.array([[w[j]*np.exp(2j*np.pi*phase_value(A,x,64)[0]*s/64) for j,x in enumerate(F)] for s in range(16)])
    effects=[beta/16*np.outer(v,v.conj()) for v in vectors]
    padding=np.eye(4)-sum(effects)
    assert np.linalg.eigvalsh(padding).min()>-1e-12
    assert sum(effects)+padding==pytest.approx(np.eye(4))
    P=np.array([[np.vdot(psi,E@psi).real for E in effects+[padding]] for psi in states])
    assert P.sum(axis=1)==pytest.approx(np.ones(16))
    assert P[:,:-1].sum(axis=1).mean()==pytest.approx(float(Fraction(c["covariant_single_seed_completion_mass_exact"])))
    marginal=P.mean(axis=0)
    valid=P>1e-30
    info=np.sum(P[valid]*np.log2((P/marginal)[valid]))/16
    assert info<=c["completed_single_seed_information_upper_bits"]+1e-12
    assert not c["this_upper_bound_covers_all_measurements"]


def test_live_native_witnesses_have_exact_replay_and_no_asymptotic_promotion():
    r=json.loads(REPORT.read_text())
    assert not r["accepted_speedup_candidate"]
    for c in r["cases"]:
        F=[int(x,16) for x in c["fiber_assignments_hex"]]
        actual,receipt=paid_fiber(c["full_labels"],c["original_phase_bits"],c["measured_syndrome"])
        assert actual==F and receipt==c["paid_fiber_receipt"]
        assert phase_value(c["full_labels"],c["original_uniform_assignment_used_for_Born_syndrome_calibration"],4)==tuple(c["measured_syndrome"])
        w=c["exact_witness"]["integer_weights"]
        moment=direct_moment(c["full_labels"],c["original_phase_bits"],F,w)
        assert moment==Fraction(c["fourth_moment_supremum_lower_exact"])
        assert c["exact_weight_support_structure"]==support_structure(F,c["exact_witness"])
        for t in c["quantitative_cap_tests"]:
            assert t["falsified_by_exact_selected_witness"]==(moment>t["cap"])
        assert not c["native_high_probability_or_asymptotic_statement_proved"]
        assert not c["efficient_secret_decoder_or_POVM_compiler"]
    large=r["cases"][-1]
    assert large["exact_weight_support_structure"]["nonzero_weight_support"]==12
    assert large["exact_witness"]["completed_single_seed_information_upper_bits"]<0.023


def test_enumeration_limits_and_bad_witnesses_fail_closed():
    with pytest.raises(ValueError,match="half-table cap"):
        paid_fiber(((1,)*20,),4,(0,),half_table_cap=100)
    with pytest.raises(ValueError,match="output cap"):
        paid_fiber(((0,)*8,),4,(0,),fiber_cap=10)
    with pytest.raises(ValueError,match="noninjective"):
        pair_buckets(((0,0),),4,[0,1])
    with pytest.raises(ValueError,match="nonzero bounded"):
        exact_witness(np.zeros((1,1),dtype=int),[0])
