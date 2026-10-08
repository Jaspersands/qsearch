from copy import deepcopy
from fractions import Fraction
from itertools import product
import math

import pytest

from ternary_pair_collimation import LowProblem, verify_pair
from ternary_pair_lattice import coset_target, word_coordinates, embed
from ternary_pair_cell_coverage import _serialized_prepared, public_charts, rounded_errors
from ternary_repair_catalog import (
    _target_coordinates, binomial_upper, catalog_pair, exact_catalog_census,
    force_pattern, frozen_policy, heldout_words, select_catalog, sqrt_upper, train_patterns,
)


def problem(A=(1,7,11,18),Q=27):
    return LowProblem((Q,), tuple(((a,),(c,)) for a,c in zip(A[::2],A[1::2])),0)


def prepare(view):
    return frozen_policy(view,_serialized_prepared(public_charts(view,83475)))


def test_frozen_geometry_replay_checks_complete_kernel_and_real_gs_without_lll():
    view=problem(); raw=_serialized_prepared(public_charts(view,83475)); policy=frozen_policy(view,raw)
    assert policy["lll_calls_rerun"]==0
    assert policy["original_lll_preparations_per_fresh_labels"]==2
    for change in ("rows","direction","offset"):
        broken=deepcopy(raw)
        if change=="rows": broken["bases"][0]["rows"][0][0]=str(int(broken["bases"][0]["rows"][0][0])+3)
        elif change=="direction": broken["bases"][0]["directions"][0]["vector"][0]="999"
        else: broken["offsets"][0][0]="1/100"
        with pytest.raises(ValueError): frozen_policy(view,broken)
    with pytest.raises(ValueError): frozen_policy(problem((1,2,3,4)),raw)
    # Adding a later GS direction preserves earlier orthogonality and the
    # reciprocal dot product, but is NOT the current row's GS projection.
    adversarial=deepcopy(raw); d=adversarial["bases"][0]["directions"]
    v=[int(a)+int(b) for a,b in zip(d[0]["vector"],d[1]["vector"])]
    g=math.gcd(*v); v=[x//g for x in v]
    R=[int(x) for x in adversarial["bases"][0]["rows"][0]]
    d[0]["vector"]=[str(x) for x in v]
    d[0]["multiplier"]=str(Fraction(1,sum(a*b for a,b in zip(R,v))))
    with pytest.raises(ValueError,match="actual GS projection"): frozen_policy(view,adversarial)


def test_forced_pattern_recovers_every_original_word_and_exact_lattice_coefficients():
    view=problem(); policy=prepare(view); o=len(policy["offsets"])
    for word in product(range(3),repeat=view.width):
        target=view.value(word); z0,T=coset_target(view,target,policy["geometry"])
        for i,chart in enumerate(policy["charts"]):
            pattern=tuple(-x for x in rounded_errors(word,chart)); basis=policy["bases"][i//o]
            center=tuple(Fraction(a)+b for a,b in zip(T,policy["offsets"][i%o]))
            coeff=force_pattern(basis,_target_coordinates(basis,center),pattern)
            z=tuple(a+sum(c*r[j] for c,r in zip(coeff,basis["kernel_rows"])) for j,a in enumerate(z0))
            assert z==word_coordinates(word)
            point=tuple(sum(c*r[j] for c,r in zip(coeff,basis["rows"])) for j in range(3*view.width))
            assert point==tuple(3*x for x in embed(tuple(a-b for a,b in zip(z,z0))))


@pytest.mark.parametrize("A,Q",[((0,3),9),((1,7,11,18),27),((9,23,41,37,65,19),81)])
def test_catalog_pair_coverage_matches_complete_original_word_census(A,Q):
    view=problem(A,Q); policy=prepare(view); training=train_patterns(view,policy,128,83875)
    catalog=select_catalog(policy,training,16); census=exact_catalog_census(view,policy,catalog)
    found=0
    for t in range(Q):
        answer=catalog_pair(view,(t,),policy,catalog)
        if answer["pair"]: verify_pair(view,(t,),answer["pair"]); found+=1
        assert answer["cost"]["candidate_decodes"]<=catalog["total_pattern_decodes_budget"]
        assert answer["cost"]["rounding_steps"]==2*view.width*answer["cost"]["candidate_decodes"]
        assert answer["cost"]["training_words_per_fresh_label_attempt"]==128
    assert found==census["pair_covered_targets"]
    assert Fraction(census["gamma_exact"])<=Fraction(census["union_gamma_dyadic_upper"])
    for chart in census["chart_collision_bounds"]:
        mass=Fraction(chart["catalog_captured_word_mass"])
        assert mass*mass<=Fraction(chart["cauchy_squared_mass_upper"])
        assert mass<=Fraction(chart["best_possible_top_K_word_mass"])


def test_training_and_catalog_are_target_independent_and_duplicates_are_not_pairs():
    view=problem(); policy=prepare(view)
    a=train_patterns(view,policy,64,77); b=train_patterns(view,policy,64,77)
    assert a["counts"]==b["counts"] and not a["trained_from_target_or_unknown_phase"]
    catalog=select_catalog(policy,a,1)
    assert catalog["target_independent"]
    assert all(patterns==((0,)*4,) for patterns in catalog["patterns"])
    singleton=catalog_pair(view,(0,),policy,catalog)
    assert not singleton["pair"] and len(singleton["witnesses"])<=1
    assert singleton["cost"]["duplicate_words"]>=1
    cap=catalog_pair(view,(18,),policy,select_catalog(policy,a,16),max_decodes=1)
    assert not cap["pair"] and cap["cost"]["candidate_decodes"]==1
    assert cap["status"]=="DECODE_CAP_NO_PAIR"


def test_train_heldout_and_uniform_target_access_are_separate():
    view=problem(); policy=prepare(view); training=train_patterns(view,policy,64,77)
    catalogs=[select_catalog(policy,training,K) for K in (1,4,16)]
    h=heldout_words(view,policy,catalogs,64,78)
    assert h==heldout_words(view,policy,catalogs,64,78)
    assert not h["target_pair_coverage_estimated"]
    assert h["catalog_word_recall_counts"]==sorted(h["catalog_word_recall_counts"])
    assert training["independent_disjoint_word_pairs"]==32
    assert all(x<=32 for x in training["disjoint_equal_pattern_pairs"])
    cap=exact_catalog_census(view,policy,catalogs[0],max_words=8)
    assert cap["words_classified"]==0 and cap["status"]=="WORD_BUDGET_NO_PARTIAL_CENSUS"


def test_disjoint_pair_binomial_endpoint_is_conservative_and_not_zero_from_no_collisions():
    alpha=Fraction(1,20); n=8
    endpoints=[binomial_upper(n,k,alpha,bits=12) for k in range(n+1)]
    assert endpoints==sorted(endpoints) and endpoints[0]>0 and endpoints[-1]==1
    for p in (Fraction(1,10),Fraction(1,2),Fraction(9,10)):
        failure=sum(Fraction(math.comb(n,k))*p**k*(1-p)**(n-k) for k,U in enumerate(endpoints) if U<p)
        assert failure<=alpha
    U=binomial_upper(256,0)
    assert (1-U)**256<=Fraction(1,1800)
    assert U>Fraction(1,100)


def test_sqrt_upper_is_exact_upward_not_a_floating_heuristic():
    for x in (Fraction(0),Fraction(1,10**20),Fraction(2),Fraction(123456789,987654321)):
        y=sqrt_upper(x)
        assert y*y>=x
        if y: assert (y-Fraction(1,2**24))**2<x


@pytest.mark.parametrize("call",[lambda:binomial_upper(0,0),lambda:binomial_upper(10,11),
    lambda:binomial_upper(10,1,0.1),lambda:sqrt_upper(-1),lambda:train_patterns(problem(),prepare(problem()),0),
    lambda:select_catalog(prepare(problem()),train_patterns(problem(),prepare(problem()),1),0)])
def test_invalid_inputs_fail_closed(call):
    with pytest.raises(ValueError):call()
