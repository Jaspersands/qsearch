from dataclasses import replace
from fractions import Fraction
from itertools import product
import json
from pathlib import Path
import random
import subprocess

import numpy as np
import pytest

from cyclotomic_fiber_receiver import inverse_frequency_coordinates,native_source
from ternary_affine_line_extractor import from_quadratic,quadratic_rows
from ternary_cyclic_extractor import random_even_source
from ternary_nonlinear_cycle_compiler import cyclic_coordinates,reconstruct
from ternary_shallow_kernel_cycle import ShallowKernelCycle,control_record,implicit_menu_control,selected_child,unseen_prefix_gate


def source_from_rows(rows,r):
    return native_source([[inverse_frequency_coordinates(a,c,2*r) for a,c in zip(pair[0],pair[1])] for pair in rows],2*r)


def test_complete_actual_native_cube_has_fixed_point_free_first_prefix_cycles():
    source=random_even_source(1,6,8,88114);policy=ShallowKernelCycle.from_source(source);coordinates=[];directions=set()
    for word in product(range(3),repeat=8):
        first=policy(word);second=policy(first)
        assert first!=word and policy(second)==word
        assert policy.control(first)==policy.control(second)==policy.control(word)
        assert len({tuple(a%3 for a in source.value(w)) for w in (word,first,second)})==1
        u,t,flag=cyclic_coordinates(word,policy)
        assert flag and reconstruct(u,t,policy)==word
        assert not any((a-b)%3 for a,b in zip(word,reconstruct(u,t,policy)))
        coordinates.append((u,t));directions.add(policy.control(word)[2])
    assert len(set(coordinates))==6561 and len(directions)>1


@pytest.mark.parametrize("n,r",[(2,2),(2,3),(3,3),(4,4)])
def test_larger_native_words_obey_global_cycle_identities_without_full_cube_enumeration(n,r):
    source=random_even_source(n,2*r,(n+1)**3,88200+n+r);policy=ShallowKernelCycle.from_source(source);rng=random.Random(88300+n)
    for _ in range(48):
        word=tuple(rng.randrange(3) for _ in range(source.inputs));a=policy(word);b=policy(a)
        assert policy(b)==word and len({word,a,b})==3
        assert policy.control(a)==policy.control(b)==policy.control(word)
        assert len({tuple(a%3 for a in source.value(w)) for w in (word,a,b)})==1


def test_policy_has_no_high_row_or_secret_access_and_is_invariant_to_native_high_lifts():
    source=random_even_source(2,6,27,88201);q=source.modulus
    rows=[tuple(tuple((a+3*(i+j+1))%q for j,a in enumerate(row)) for row in pair) for i,pair in enumerate(source.frequencies)]
    changed=source_from_rows(rows,3)
    assert ShallowKernelCycle.from_source(source)==ShallowKernelCycle.from_source(changed)
    assert not ShallowKernelCycle.from_source(source).metadata()["policy_stores_or_reads_high_frequency_rows"]


@pytest.mark.parametrize("n",[1,2,3,4])
def test_polynomial_kernel_policy_can_realize_exponentially_many_implicit_directions(n):
    M=(n+1)**2;A=tuple((0,)*M for _ in range(n));B=tuple(tuple((int(i%(n+1)==j)-int(i%(n+1)==n))%3 for i in range(M)) for j in range(n))
    source=from_quadratic(A,B);supports=tuple(tuple(range(j*(n+1),(j+1)*(n+1))) for j in range(n+1));policy=ShallowKernelCycle(n,M,*quadratic_rows(source),supports);directions=set()
    for c in product(range(3),repeat=n):
        targets=tuple(tuple(int(i==j) for i in range(n)) for j in range(n))+(tuple(-x%3 for x in c),)
        word=tuple(a for column in targets for a in (*tuple(2*x%3 for x in column),0))
        tangents,coefficients,v=policy.control(word)
        assert tangents==targets and coefficients==c+(1,)
        assert policy(policy(policy(word)))==word
        directions.add(v)
    assert len(directions)==3**n
    assert not policy.metadata()["guaranteed_mask_preprocessing_polynomial"]


def test_actual_conditional_high_lifts_give_exact_extra_prefix_gate_not_a_selected_label_histogram():
    source=random_even_source(1,6,8,88114);policy=ShallowKernelCycle.from_source(source);tag,_,_=cyclic_coordinates((0,)*8,policy)
    packet=selected_child(source,policy,tag);a,b=packet["pointed_unit_minor"]["columns"];pairs=[]
    for u,v in product(range(9),repeat=2):
        rows=[[list(row) for row in pair] for pair in source.frequencies]
        rows[a//2][a%2][0]=(rows[a//2][a%2][0]+3*u)%27
        rows[b//2][b%2][0]=(rows[b//2][b%2][0]+3*v)%27
        changed=source_from_rows(rows,3);changed_policy=ShallowKernelCycle.from_source(changed)
        assert changed_policy==policy
        triple=[reconstruct(tag,k,changed_policy) for k in range(3)];f=[changed.value(w)[0] for w in triple]
        pair=tuple((x-f[0])%27//3 for x in f[1:]);pairs.append(pair)
    assert len(set(pairs))==81
    assert sum(a%3==0 and b%3==0 for a,b in pairs)==9
    assert unseen_prefix_gate(1,3,1,2)["mean_extra_prefix_survival_factor"]=="1/9"


def test_locally_valid_native_partners_do_not_certify_a_global_three_cycle():
    source=random_even_source(1,6,8,88114);p=ShallowKernelCycle.from_source(source);word=(0,)*8
    def unsafe(w):
        first,second=p(w),p(p(w))
        return first if w==min(w,first,second) else second
    assert source.value(unsafe(word))[0]%3==source.value(word)[0]%3
    assert source.value(unsafe(unsafe(word)))[0]%3==source.value(word)[0]%3
    assert unsafe(unsafe(unsafe(word)))!=word
    with pytest.raises(ValueError):cyclic_coordinates(word,unsafe)


def test_retaining_original_word_garbage_destroys_the_actual_child_coherence():
    source=random_even_source(1,6,8,88114);p=ShallowKernelCycle.from_source(source);tag,_,_=cyclic_coordinates((0,)*8,p)
    triple=[reconstruct(tag,k,p) for k in range(3)]
    amplitudes=np.exp(2j*np.pi*np.array([source.value(w)[0] for w in triple])/source.modulus)/np.sqrt(3)
    dirty=np.zeros((3**8,3),dtype=complex);clean=np.zeros_like(dirty)
    for t,w in enumerate(triple):
        index=sum(a*3**(7-i) for i,a in enumerate(w));dirty[index,t]=amplitudes[t];clean[0,t]=amplitudes[t]
    target=np.outer(amplitudes,amplitudes.conj());dirty_reduced=dirty.T@dirty.conj();clean_reduced=clean.T@clean.conj()
    assert np.allclose(clean_reduced,target)
    assert np.allclose(dirty_reduced,np.eye(3)/3)
    assert np.isclose(np.sum(abs(np.linalg.eigvalsh(dirty_reduced-target)))/2,2/3)


@pytest.mark.parametrize("n,r,e,d",[(1,3,1,2),(2,3,1,2),(8,5,1,4),(32,6,2,5),(128,7,1,6)])
def test_unseen_prefix_gate_is_exact_for_any_retained_low_only_triples(n,r,e,d):
    value=unseen_prefix_gate(n,r,e,d)
    assert Fraction(value["mean_extra_prefix_survival_factor"])==Fraction(1,3**(2*n*(d-e)))
    assert not value["higher_prefix_informed_actions_or_secret_digit_correction_excluded"]
    assert not value["full_high_label_instance_success_equal_to_population_factor_claimed"]


def test_shallow_report_does_not_claim_higher_depth_or_selected_samples_as_population():
    value=control_record(2,3,88102)
    assert not value["source_cube_enumerated_completely"] and value["original_words_audited"]==48
    assert not value["sample_fraction_is_population_survival_factor_claimed"]
    assert value["raw_first_prefix_acceptance"]=="1"
    assert not value["full_depth_polynomial_supply_supplied"]
    assert not value["novel_shallow_algorithm_claimed"]


@pytest.mark.parametrize("operation",[lambda:unseen_prefix_gate(True,3,1,2),lambda:unseen_prefix_gate(1,3,2,1),lambda:unseen_prefix_gate(1,3,1,3),lambda:ShallowKernelCycle.from_source(random_even_source(2,6,26,1)),lambda:control_record(2,3,1,True)])
def test_invalid_or_excessive_domains_fail_before_partial_certificates(operation):
    with pytest.raises(ValueError):operation()


def test_overlapping_or_nonzero_curvature_masks_are_rejected():
    source=random_even_source(1,6,8,88114);p=ShallowKernelCycle.from_source(source)
    with pytest.raises(ValueError):replace(p,supports=(p.supports[0],p.supports[0]))
    with pytest.raises(ValueError):replace(p,supports=((),p.supports[1]))
    with pytest.raises(ValueError):replace(p,A=((True,)*8,))
    index=next(i for i,a in enumerate(p.B[0]) if a)
    with pytest.raises(ValueError):replace(p,supports=((index,),p.supports[1]))


def test_live_independent_checker_replays_true_sources_and_unseen_lift_censuses():
    root=Path(__file__).resolve().parents[1]
    result=subprocess.run(["node",str(root/"research/certificates/ternary_shallow_kernel_cycle_crosscheck.js")],capture_output=True,text=True)
    assert result.returncode==0,result.stderr
    output=json.loads(result.stdout)
    assert output["wholeOriginalWords"]==6561 and output["sampledOriginalWords"]==96
    assert output["implicitDirectionWitnesses"]==9


@pytest.mark.parametrize("mutation",["mask","tangent","coordinates","cloning","high-access","full-depth","population","implicit-menu","lift","gate","scope","hardware"])
def test_checker_rejects_invalid_policies_false_lift_rates_and_unsupported_claims(tmp_path,mutation):
    root=Path(__file__).resolve().parents[1];record=json.loads((root/"research/phase_workbench/ternary_shallow_kernel_cycle.json").read_text());c=record["native_controls"][0]
    if mutation=="mask":c["policy"]["disjoint_masks"][0]=c["policy"]["disjoint_masks"][1]
    if mutation=="tangent":c["policy"]["A"][0][0]=(c["policy"]["A"][0][0]+1)%3
    if mutation=="coordinates":c["complete_or_sample_coordinate_sha256"]="0"*64
    if mutation=="cloning":c["all_orbit_tags_counted_as_separate_outputs"]=True
    if mutation=="high-access":c["policy"]["policy_stores_or_reads_high_frequency_rows"]=True
    if mutation=="full-depth":record["full_depth_polynomial_time_and_supply_algorithm_supplied"]=True
    if mutation=="population":c["sample_fraction_is_population_survival_factor_claimed"]=True
    if mutation=="implicit-menu":record["implicit_exponential_menu_control"]["distinct_direction_count"]=1
    if mutation=="lift":c["selected_child_controls"][0]["conditional_lift_census"]["per_coordinate_child_pairs_divisible_by_three"][0]=81
    if mutation=="gate":record["unseen_prefix_population_gates"][0]["mean_extra_prefix_survival_factor"]="1"
    if mutation=="scope":record["unseen_prefix_population_gates"][0]["higher_prefix_informed_actions_or_secret_digit_correction_excluded"]=True
    if mutation=="hardware":c["policy"]["native_quantum_gate_synthesis_supplied"]=True
    target=tmp_path/"mutant.json";target.write_text(json.dumps(record))
    result=subprocess.run(["node",str(root/"research/certificates/ternary_shallow_kernel_cycle_crosscheck.js"),str(target)],capture_output=True,text=True)
    assert result.returncode!=0,result.stdout
