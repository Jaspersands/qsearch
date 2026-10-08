from collections import Counter
from fractions import Fraction
from itertools import product
import json
import math
import subprocess

import numpy as np
import pytest

from ternary_cubic_program_factory import (
    DERIVATION, REPORT, CubicProgram, cost_ledger, cubic_powers, evaluate,
    factory, injection_tensor, linear_source_census, relation, seeded_cohort,
    source_chart_census, vary_linear_lift,
)
from ternary_quadratic_program_receiver import isotropic_direction
from cyclotomic_fiber_receiver import frequency_coordinates


@pytest.fixture(scope="module")
def cohorts():
    return {(n,d): seeded_cohort(n,d,seed) for n,d,seed in ((1,2,88705),(1,3,88707),(2,3,88708))}


def outcomes(programs):
    _, certificate = relation(programs); d=programs[0].width
    return tuple(tuple((j+i+1) % 3 for i in range(d)) for j in certificate["selected_program_indices"])


@pytest.mark.parametrize("d",[1,2,3,7,12])
def test_canonical_cubic_feature_count(d):
    powers=cubic_powers(d)
    assert len(powers)==math.comb(d+2,3)-d
    assert all(sum(p)==3 and max(p)<=2 for p in powers)
    assert len(set(powers))==len(powers)


@pytest.mark.parametrize("key",[(1,2),(1,3),(2,3)])
def test_actual_original_polynomials_and_nontrivial_cubic_relation(cohorts,key):
    programs=cohorts[key]; c,r=relation(programs); d=key[1]
    assert len(r["selected_program_indices"])>=2 and 2 in c
    assert not r["selection_reads_high_linear_or_quadratic_coefficients"]
    assert not r["physical_IID_independence_proved_by_ancestry_ids"]
    for p in programs:
        polynomial=p.polynomial()
        assert all(p.value(z)==p.original_value(z)==evaluate(polynomial,z) for z in product(range(3),repeat=d))
    for l in range(key[0]):
        for exponent in cubic_powers(d):
            assert sum(a*p.top()[l].get(exponent,0) for a,p in zip(c,programs)) % 3==0
    if key==(2,3):
        assert len({str(programs[j].top()) for j in r["selected_program_indices"]})>1


def test_every_small_injection_transcript_cancels_cubics(cohorts):
    programs=cohorts[1,2]; ws=tuple(product(range(3),repeat=2))
    c,r=relation(programs);selected=r["selected_program_indices"]
    assert len(selected)==2
    for measured in product(ws,repeat=2):
        family,record,value=factory(programs,measured)
        assert all(value(z)==family.value(z) for z in ws)
        assert record["all_injection_outcomes_accepted"]
        assert Fraction(record["conditional_one_injection_transcript_probability"])==Fraction(1,81)
        for z in ws:
            direct=sum(programs[j].original_value(tuple((a+c[j]*b) % 3 for a,b in zip(m,z)))[0]-programs[j].original_value(m)[0] for j,m in zip(selected,measured)) % 3
            assert value(z)==(direct,)


@pytest.mark.parametrize("coefficient",[1,2])
def test_one_unknown_program_actual_sum_is_uniform_on_reference_entangled_data(cohorts,coefficient):
    p=cohorts[1,2][0];D=9;data=np.eye(D,dtype=complex)/math.sqrt(D)
    tensor=injection_tensor(p,coefficient,(1,),data)
    ws=tuple(product(range(3),repeat=2))
    for i,m in enumerate(ws):
        phase=np.array([np.exp(2j*np.pi*p.original_value(tuple((a+coefficient*b) % 3 for a,b in zip(m,z)))[0]/3) for z in ws])
        assert np.allclose(tensor[:,i],data*phase/math.sqrt(D))
        assert np.sum(abs(tensor[:,i])**2)==pytest.approx(1/D)


def test_complete_two_program_choi_composition_with_every_outcome(cohorts):
    programs=cohorts[1,2];c,r=relation(programs);ws=tuple(product(range(3),repeat=2));D=9
    branches=[((),np.eye(D,dtype=complex)/math.sqrt(D))]
    for j in r["selected_program_indices"]:
        expanded=[]
        for transcript,state in branches:
            replay=injection_tensor(programs[j],c[j],(1,),state)
            for i,m in enumerate(ws):
                assert np.sum(abs(replay[:,i])**2)==pytest.approx(1/D)
                expanded.append((transcript+(m,),replay[:,i]*math.sqrt(D)))
        branches=expanded
    assert len(branches)==81
    for transcript,state in branches:
        phase=np.array([np.exp(2j*np.pi*(sum(programs[j].original_value(tuple((a+c[j]*b) % 3 for a,b in zip(m,z)))[0] for j,m in zip(r["selected_program_indices"],transcript)) % 3)/3) for z in ws])
        assert np.allclose(state,np.diag(phase)/math.sqrt(D))
        # Inverse SUM from data to reference makes the reference exactly zero.
        flat=np.zeros((D,D),complex)
        for zi,z in enumerate(ws):
            for ri,reference in enumerate(ws):
                new=tuple((a-b) % 3 for a,b in zip(reference,z))
                flat[ws.index(new),zi]=state[ri,zi]
        assert np.allclose(flat[0],phase/math.sqrt(D)) and np.allclose(flat[1:],0)


def test_true_original_high_lifts_keep_matrices_fixed_and_supply_every_beta(cohorts):
    programs=cohorts[1,2];record=linear_source_census(programs,outcomes(programs))
    assert record["complete_original_pivot_lifts"]==27
    histogram=Counter(tuple(row["component_zero_linear"]) for row in record["source_lifts"])
    assert len(histogram)==9 and set(histogram.values())=={3}
    assert record["quadratic_matrices_unchanged"]
    assert not record["virtual_lifts_are_additional_physical_samples"]
    assert not record["physical_IID_source_premise_certified"]


def test_conditioned_original_pivot_chart_is_a_full_bijection_at_all_pointer_shifts():
    record=source_chart_census()
    assert record["complete_conditioned_original_frequency_pairs_checked"]==243
    for c in record["conditioned_pivot_controls"]:
        assert set(map(tuple,c["odd_chart_words"]))==set(product(range(3),repeat=3))
    assert not record["IID_input_premise_certified_by_finite_census"]


@pytest.mark.parametrize("key",[(1,2),(1,3),(2,3)])
def test_true_source_alpha_delta_decomposition_not_merely_a_histogram(cohorts,key):
    for p in cohorts[key]:
        packet=p.branch.packet;base=packet.assignment(p.logical((0,)*p.width))
        pairs=[tuple(frequency_coordinates(label,3) for label in row) for row in packet.labels]
        for z in product(range(3),repeat=p.width):
            t=packet.assignment(p.logical(z));expected=[]
            for l in range(p.components):
                low_carry=sum((pair[l][0] % 3)*(a-b) for pair,a,b in zip(pairs,t,base))
                assert low_carry % 3==0
                high=sum(((pair[l][0]-pair[l][0] % 3)//3)*(a-b)+(((pair[l][1]-2*pair[l][0]) % 9)//3)*(int(a==2)-int(b==2)) for pair,a,b in zip(pairs,t,base))
                expected.append((low_carry//3+high) % 3)
            assert p.original_value(z)==tuple(expected)


def test_high_label_filtering_can_destroy_the_uniform_equation_law(cohorts):
    programs=cohorts[1,2];measured=outcomes(programs);j=relation(programs)[1]["selected_program_indices"][0]
    labels=[]
    for increments in product(range(3),repeat=3):
        cohort=list(programs);cohort[j]=vary_linear_lift(programs[j],increments)
        family,_,_=factory(cohort,measured);v,_=isotropic_direction(family)
        labels.append(family.receiver(v)["label_offset"][0])
    assert Counter(labels)=={0:9,1:9,2:9}
    filtered=[x for x in labels if x==0]
    assert len(filtered)==9 and set(filtered)=={0}


def test_guaranteed_width_native_factory_and_receiver_do_not_use_dense_tables():
    programs=seeded_cohort(1,7,88770)
    family,record,value=factory(programs,outcomes(programs))
    v,search=isotropic_direction(family)
    assert search["scalable_search_claimed"] and family.quadratic(v)==(0,)
    assert not search["direction_selection_reads_linear_coefficients"]
    assert record["original_native_inputs_charged"]==2496
    for j in range(25):
        z=tuple((j+i*i) % 3 for i in range(7))
        assert family.value(z)==value(z)
    assert not record["growing_depth_speedup_proved"]


def test_all_cohort_inputs_and_unselected_programs_are_charged(cohorts):
    programs=cohorts[2,3];_,r,_=factory(programs,outcomes(programs))
    assert r["cohort_programs_charged"]==15
    assert len(r["selected_program_indices"])==4
    assert r["original_native_inputs_charged"]==675
    assert not r["unselected_programs_claimed_fresh_IID"]
    source_exponent=sum(len(p.branch.acquisition.active)-p.width for p in programs)
    assert Fraction(r["original_source_measurement_branch_probability"])==Fraction(1,3**source_exponent)
    assert Fraction(r["raw_source_and_injection_transcript_probability"])==Fraction(1,3**(source_exponent+12))
    assert not r["cloning_conjugate_program_or_unknown_inverse_used"]


@pytest.mark.parametrize("bad",[0,3,True,-1])
def test_invalid_injection_coefficients_rejected(cohorts,bad):
    with pytest.raises(ValueError,match="coefficient"):
        injection_tensor(cohorts[1,2][0],bad,(1,),np.eye(9)/3)


def test_source_reuse_and_malformed_transcripts_rejected(cohorts):
    p=cohorts[1,2][0]
    with pytest.raises(ValueError,match="ancestry"): relation((p,p))
    with pytest.raises(ValueError,match="measured word"): factory(cohorts[1,2],())
    with pytest.raises(ValueError,match="ternary"): factory(cohorts[1,2],((3,0),(0,0)))
    with pytest.raises(ValueError,match="same width"): relation((p,cohorts[1,3][0]))
    with pytest.raises(ValueError,match="retained width"): CubicProgram(p.branch,99,())


def test_cost_ledger_uses_closed_form_instead_of_enormous_feature_enumeration():
    r=cost_ledger(32);d=33**3-32
    assert r["cubic_features"]==32*(math.comb(d+2,3)-d)
    assert r["asymptotic_input_cap_degree_in_n"]==15
    R=r["cubic_features"]
    assert r["dense_relation_matrix_field_entries"]==str(R*(R+1))
    assert r["dense_relation_elimination_field_operation_scale"]==str(R*R*(R+1))
    assert not r["field_operation_scale_is_tight_gate_count"]
    assert r["known_fixed_root_sieves_already_polynomial"]
    assert not r["growing_depth_tensor_or_copy_cost_polynomial"]
    assert not r["full_modulus_recovery_or_cryptographic_reduction_supplied"]


def test_live_independent_certificate():
    result=subprocess.run(["node","research/certificates/ternary_cubic_program_factory_crosscheck.js",str(REPORT)],capture_output=True,text=True)
    assert result.returncode==0,result.stderr


@pytest.mark.parametrize("mutation",["cost","phase","relation","probability","ancestry","speedup","source-law"])
def test_independent_checker_rejects_false_claims_and_corrupted_artifacts(tmp_path,mutation):
    report=json.loads(REPORT.read_text()); c=report["native_controls"][0]
    if mutation=="cost":c["original_native_inputs_charged"]-=1
    elif mutation=="phase":c["component_linear"][0][0]=(c["component_linear"][0][0]+1)%3
    elif mutation=="relation":c["coefficients"][0]=(c["coefficients"][0]+1)%3
    elif mutation=="probability":c["conditional_one_injection_transcript_probability"]="1"
    elif mutation=="ancestry":c["programs"][1]["source"]["original_source_ids"][0]=c["programs"][0]["source"]["original_source_ids"][0]
    elif mutation=="speedup":report["growing_depth_speedup_proved"]=True
    else:c["original_linear_source_census"]["source_lifts"][0]["component_zero_linear"][0]=(c["original_linear_source_census"]["source_lifts"][0]["component_zero_linear"][0]+1)%3
    path=tmp_path/"mutation.json";path.write_text(json.dumps(report))
    result=subprocess.run(["node","research/certificates/ternary_cubic_program_factory_crosscheck.js",str(path)],capture_output=True,text=True)
    assert result.returncode!=0
