from copy import deepcopy
from itertools import product

import pytest
from flint import fmpq_mat

from ternary_pair_collimation import LowProblem
from ternary_pair_cell_coverage import public_charts, _serialized_prepared
from ternary_pair_lattice import word_coordinates, coset_target
from ternary_repair_catalog import frozen_policy
from ternary_adaptive_shell import compile_adaptive
from ternary_prefix_integrality import prefix_geometry
from ternary_prefix_modular import (binary_shadow, support_dp, fourier_support_bound,
    analyze_geometry, propose_modular_word, verify_modular_word)


def prepared(A=(9,23,41,37,65,19),Q=81):
    problem=LowProblem((Q,),tuple(((a,),(c,)) for a,c in zip(A[::2],A[1::2])),0)
    policy=frozen_policy(problem,_serialized_prepared(public_charts(problem,83950)))
    return problem,policy,compile_adaptive(policy)


def syndrome(H,z):
    return sum((sum(a*x for a,x in zip(h,z))%2)<<i for i,h in enumerate(H))


@pytest.mark.parametrize("A,Q",[((9,23,41,37,65,19),81),((0,3,6,0),27),((0,0),9)])
def test_binary_domain_elimination_matches_every_original_modular_word(A,Q):
    problem,policy,compiled=prepared(A,Q); d=2*problem.width
    all_domains=((0,1,2),(0,1),(0,2),(1,2),(0,),(1,),(2,))
    for b in range(d+1):
        for D in all_domains:
            domains=tuple(D if j%2==0 else (0,1,2) for j in range(problem.width))
            g=prefix_geometry(problem,(0,),policy,compiled,b,(0,)*d,domains)
            shadow=binary_shadow(g); H=shadow["quotient_annihilator"]
            result=support_dp(shadow)
            K=g["kernel_prefix"]
            span={tuple(sum(c*row[j] for c,row in zip(coeff,K))%2 for j in range(d))
                  for coeff in product((0,1),repeat=b)}
            modular_words=[]
            for w in product(*domains):
                delta=tuple((a-z)%2 for a,z in zip(word_coordinates(w),g["z_anchor"]))
                if delta in span: modular_words.append(w)
            assert result["target_reachable"]==bool(modular_words)
            assert all(sum(a*x for a,x in zip(h,row))%2==0 for h in H for row in K)
            assert len(H)==shadow["quotient_dimension"]
            assert len(H)<=shadow["original_shadow_dimension"]
            if result["support_saturated"]:
                assert result["target_reachable"]


def test_two_choice_domains_are_eliminated_only_as_binary_lines():
    problem,policy,compiled=prepared((1,2),9)
    for D in ((0,1),(0,2),(1,2)):
        g=prefix_geometry(problem,(0,),policy,compiled,0,(0,0),(D,))
        shadow=binary_shadow(g)
        assert shadow["eliminated_binary_span_rank"]==1
        assert shadow["quotient_dimension"]==1 and not shadow["full_blocks"]
        assert shadow["exact_binary_elimination_not_valid_over_F3"]
    g=prefix_geometry(problem,(0,),policy,compiled,0,(0,0),((2,),))
    assert binary_shadow(g)["quotient_dimension"]==2
    assert support_dp(binary_shadow(g))["target_reachable"] is False


def test_integer_false_prefix_can_survive_the_complete_modular_shadow():
    problem,policy,compiled=prepared((1,2),9)
    # Anchor (2,0) is not native; its residue equals the zero native digit.
    # Therefore a modular word is not an actual integer continuation.
    K=compiled["basis"]["kernel_rows"]
    chosen=next((2*int(row[0]),2*int(row[1])) for row in K if any(row))
    g=prefix_geometry(problem,(0,),policy,compiled,0,(0,0))
    g["z_anchor"]=chosen
    result=analyze_geometry(g)
    assert result["support"]["target_reachable"]
    assert not result["support"]["integer_completion_proved"]
    assert chosen not in ((0,0),(1,0),(0,1))


def test_support_saturation_is_a_complete_not_target_only_certificate():
    shadow={"quotient_dimension":2,"target_syndrome":3,
            "full_blocks":[{"choices":(0,1,2)},{"choices":(0,1,2)},{"choices":(0,3,3)}]}
    result=support_dp(shadow)
    assert result["support_saturated"] and result["target_reachable"]
    assert result["cost"]["blocks_processed"]==2
    assert result["support_history"]==[1,3,4]
    assert result["cost"]["xor_transitions"]==12
    assert result["status"]=="ALL_MOD2_PREFIX_PREDICATES_POWERLESS"


def test_nonfull_support_distinguishes_reachable_and_certified_obstruction():
    shadow={"quotient_dimension":2,"target_syndrome":3,"full_blocks":[{"choices":(0,1,2)}]}
    result=support_dp(shadow)
    assert result["status"]=="MOD2_NATIVE_PREFIX_OBSTRUCTION"
    shadow["target_syndrome"]=1
    assert support_dp(shadow)["status"]=="MOD2_TARGET_REACHABLE_NOT_NATIVE"
    assert not fourier_support_bound(shadow)["proves_full_support"]


def test_fourier_support_bound_agrees_with_exact_every_syndrome_probability():
    choices=((0,1,2),(0,1,2),(0,1,3))
    shadow={"quotient_dimension":2,"target_syndrome":0,"full_blocks":[{"choices":x} for x in choices]}
    bound=fourier_support_bound(shadow)
    assert bound["proves_full_support"]
    counts=[0]*4
    for word in product(*choices):
        x=0
        for c in word: x^=c
        counts[x]+=1
    num,den=map(int,bound["every_syndrome_probability_lower_bound"])
    assert all(c*den>=num*3**len(choices) for c in counts)
    assert sum(bound["nonzero_character_weight_histogram"])==3
    assert support_dp(shadow)["support_saturated"]


def test_fourier_failure_is_not_a_missing_support_claim():
    # Three biased binary images fill F2^3 but (4/3)^3-1 exceeds one.
    shadow={"quotient_dimension":3,"target_syndrome":7,
            "full_blocks":[{"choices":(0,1,1)},{"choices":(0,2,2)},{"choices":(0,4,4)}]}
    assert support_dp(shadow)["support_saturated"]
    bound=fourier_support_bound(shadow)
    assert not bound["proves_full_support"] and bound["bound_failure_is_not_missing_support"]


def test_preflight_does_not_truncate_support_and_call_it_empty():
    shadow={"quotient_dimension":30,"target_syndrome":1,"full_blocks":[{"choices":(0,1,2)}]}
    result=support_dp(shadow,16)
    assert result["target_reachable"] is None
    assert result["cost"]["xor_transitions"]==0 and result["support_history"]==[]
    assert fourier_support_bound(shadow,16)["characters_checked"]==0
    zero={"quotient_dimension":0,"target_syndrome":0,"full_blocks":[]}
    assert support_dp(zero,1)["support_saturated"]
    assert fourier_support_bound(zero,1)["proves_full_support"]
    with pytest.raises(ValueError): support_dp(shadow,0)
    with pytest.raises(ValueError): fourier_support_bound(shadow,0)


def test_huge_original_integer_entries_are_reduced_before_int64_conversion():
    problem,policy,compiled=prepared((1,2),9)
    g=prefix_geometry(problem,(0,),policy,compiled,1,(0,0))
    old=binary_shadow(g)
    altered=deepcopy(g)
    altered["kernel_prefix"]=tuple(tuple(x+2*(10**100) for x in row) for row in g["kernel_prefix"])
    new=binary_shadow(altered)
    assert old==new


def test_modular_screen_never_rejects_an_actual_native_completion():
    problem,policy,compiled=prepared()
    K=fmpq_mat(compiled["basis"]["kernel_rows"]).transpose()
    for word in product(range(3),repeat=3):
        target=problem.value(word); z0,_=coset_target(problem,target,policy["geometry"])
        full=K.solve(fmpq_mat([[a-b] for a,b in zip(word_coordinates(word),z0)]))
        c=tuple(int(full[i,0].p) for i in range(6))
        for b in range(7):
            partial=tuple(0 if i<b else x for i,x in enumerate(c))
            domains=tuple(tuple(sorted({x,(x+1)%3})) if j%2==0 else (0,1,2) for j,x in enumerate(word))
            g=prefix_geometry(problem,target,policy,compiled,b,partial,domains)
            result=analyze_geometry(g,max_attempts=256)
            assert result["support"]["target_reachable"]
            exact=tuple((c[i]-g["anchor"][i])%2 for i in range(b))
            assert verify_modular_word(g,word,exact)["valid"]


def test_invalid_domains_rows_and_syndromes_fail_closed():
    problem,policy,compiled=prepared((1,2),9)
    g=prefix_geometry(problem,(0,),policy,compiled,1,(0,0))
    for domains in (((0,0),),((3,),),((),)):
        altered=deepcopy(g); altered["domains"]=domains
        with pytest.raises(ValueError): binary_shadow(altered)
    altered=deepcopy(g); altered["kernel_prefix"]=((0.1,0),)
    with pytest.raises(ValueError): binary_shadow(altered)
    for target in (True,-1,2):
        with pytest.raises(ValueError): support_dp({"quotient_dimension":1,"target_syndrome":target,"full_blocks":[]})
    for choices in ((1,1,2),(0,1),(0,1,4),(0,1,0.1)):
        with pytest.raises(ValueError): fourier_support_bound({"quotient_dimension":2,"full_blocks":[{"choices":choices}]})


def test_every_retained_modular_word_verifies_without_the_quotient_or_rng():
    problem,policy,compiled=prepared()
    for b in range(7):
        g=prefix_geometry(problem,(0,),policy,compiled,b,(0,)*6)
        result=propose_modular_word(g,binary_shadow(g),4096,191+b)
        if not result["certificate"]: continue
        cert=result["certificate"]
        assert verify_modular_word(g,cert["native_word"],cert["prefix_coefficients_mod2"])["valid"]
        assert result["cost"]["affine_proposals"]<=4096
        assert result["cost"]["recovery_affine_solves"]==1
        assert not cert["integer_prefix_membership_proved"]
        if b:
            bad=list(cert["prefix_coefficients_mod2"]); bad[0]^=1
            if any(x%2 for x in g["kernel_prefix"][0]):
                assert not verify_modular_word(g,cert["native_word"],bad)["valid"]
    g=prefix_geometry(problem,(0,),policy,compiled,6,(0,)*6)
    with pytest.raises(ValueError): verify_modular_word(g,(3,0,0),(0,)*6)
    with pytest.raises(ValueError): verify_modular_word(g,(0,0,0),(True,0,0,0,0,0))


def test_random_affine_proposal_cap_and_linear_impossibility_remain_distinct():
    problem,policy,compiled=prepared((1,2),9)
    # Full triangle has modular hull F2^2, but its forbidden fourth corner can
    # be the unique affine solution. A rejected proposal is not a proof.
    g=prefix_geometry(problem,(0,),policy,compiled,0,(0,0))
    g["z_anchor"]=(1,1)
    result=propose_modular_word(g,binary_shadow(g),3,17)
    assert result["certificate"] is None and result["status"]=="MODULAR_PROPOSAL_CAP_UNKNOWN"
    assert result["cost"]["affine_proposals"]==3
    assert not support_dp(binary_shadow(g))["target_reachable"]
    g["domains"]=((0,),)
    result=propose_modular_word(g,binary_shadow(g),3,17)
    assert result["status"]=="EXACT_AFFINE_MOD2_OBSTRUCTION" and result["cost"]["affine_proposals"]==0
    with pytest.raises(ValueError): propose_modular_word(g,binary_shadow(g),0)
