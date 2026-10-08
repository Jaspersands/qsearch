from fractions import Fraction
from itertools import product
import json
import math
import subprocess

import numpy as np
import pytest

from cyclotomic_fiber_receiver import frequency_coordinates, inverse_frequency_coordinates, native_source
from ternary_correlated_packet_acquisition import PacketAcquisition
from ternary_native_phase_identity import NativeProgram, injection_control
from ternary_ridge_cancellation import (
    REPORT, cancel, cohort_ledger, linear_lift_census, low_relation, native_cohort,
    lowest_digit_readout, program_only_population_bound,
)


@pytest.fixture(scope="module")
def cohorts():
    return {(n,d,r):native_cohort(n,d,r,seed) for n,d,r,seed in ((1,1,1,89001),(1,2,1,89128),(1,2,2,89128),(2,3,3,89031))}


def outcomes(programs):
    c,_=low_relation(programs);d=programs[0].width
    return tuple(tuple((j+i+1) % 3 for i in range(d)) for j,x in enumerate(c) if x)


@pytest.mark.parametrize("n,d",[(1,1),(1,2),(2,3),(8,4),(32,8),(32,16),(32,32)])
def test_depth_independent_cohort_bound_and_exponential_width_are_explicit(n,d):
    ledger=cohort_ledger(n,d);P=(3**d-1)//2;B=n*(P-d)+1
    assert ledger["guaranteed_cohort_programs"]==str(B)
    assert ledger["full_original_input_cap"]==str(B*(n+d)*(n+1)**2)
    assert not ledger["source_cap_depends_on_phase_depth"]
    assert ledger["ambient_width_dependence_exponential"]
    assert not ledger["decoder_or_full_depth_speedup_supplied"]


@pytest.mark.parametrize("key",[(1,1,1),(1,2,1),(1,2,2),(2,3,3)])
def test_actual_source_cohort_low_signatures_obey_both_kernel_dimension_bounds(cohorts,key):
    programs=cohorts[key];c,r=low_relation(programs);n,d,_=key
    assert r["signature_matrix_rank"]<=r["observed_signature_space_dimension_upper"]<=int(r["ambient_signature_space_dimension_upper"])
    assert len(programs)==int(cohort_ledger(n,d)["guaranteed_cohort_programs"])
    assert r["reads_only_native_low_signature_residues"]
    assert not r["high_frequency_digits_or_measured_injection_words_read_for_selection"]
    assert not r["sparse_occupied_bound_guarantees_future_cohorts"]
    assert not r["all_ambient_projective_forms_materialized"]
    for row in r["signature_rows"]:
        assert sum(a*b for a,b in zip(c,row["program_coefficients"])) % 3==0
    if d>1:
        assert sum(bool(x) for x in c)>1 and 2 in c
        assert r["selected_inputs_include_nonzero_low_signature"]


def test_every_two_program_measurement_transcript_cancels_without_postselection(cohorts):
    programs=cohorts[1,2,2];c,_=low_relation(programs);selected=[j for j,x in enumerate(c) if x];ws=tuple(product(range(3),repeat=2))
    assert len(selected)==2
    for measured in product(ws,repeat=2):
        phase,r=cancel(programs,measured)
        assert phase.modulus==9
        assert all(x % 3==0 for _,tables in phase.groups for row in tables for x in row)
        assert r["degree_certificate"]["certified_global_degree_upper"]<=4
        assert r["all_injection_outcomes_accepted"] and r["each_selected_program_consumed_once"]
        assert Fraction(r["conditional_injection_transcript_probability"])==Fraction(1,81)
        for z in ws:
            direct=sum(programs[j].original_value(tuple((a+c[j]*b) % 3 for a,b in zip(m,z)))[0]-programs[j].original_value(m)[0] for j,m in zip(selected,measured)) % 9
            assert phase.value(z)==(direct,)


@pytest.mark.parametrize("key",[(1,2,1),(1,2,2),(2,3,3)])
def test_original_full_phase_root_and_all_acquisition_costs_are_preserved(cohorts,key):
    programs=cohorts[key];phase,r=cancel(programs,outcomes(programs));n,d,rdepth=key
    assert phase.modulus==3**rdepth
    assert r["full_original_input_cap_charged"]==int(cohort_ledger(n,d)["full_original_input_cap"])
    source_exponent=sum(len(p.branch.acquisition.active)-d for p in programs)
    assert Fraction(r["raw_source_program_transcript_probability"])==Fraction(1,3**source_exponent)
    assert not r["physical_source_IID_premise_verified"]
    assert not r["full_phase_order_of_every_branch_guaranteed"]
    assert not r["full_root_secret_identifiability_proved"]
    assert not r["ordinary_field3_readout_or_phase_power_oracle_supplied"]
    assert Fraction(r["conditional_full_phase_order_loss_upper"])==Fraction(1,3**(n*d))


def test_trivial_single_coordinate_control_loses_root_and_is_not_promoted(cohorts):
    programs=cohorts[1,1,1];phase,r=cancel(programs,((0,),))
    assert cohort_ledger(1,1)["one_coordinate_stage_is_trivial"]
    assert low_relation(programs)[1]["signature_matrix_rank"]==0
    assert all(phase.value((z,))==(0,) for z in range(3))
    assert not r["full_phase_order_of_every_branch_guaranteed"]
    assert not r["quantum_speedup_proved"]


def test_true_high_root_alpha_census_supplies_uniform_mod3_linear_offsets(cohorts):
    programs=cohorts[1,2,2];c,r=low_relation(programs);selected=[j for j,x in enumerate(c) if x]
    result=linear_lift_census(programs,outcomes(programs))
    assert result["retained_phase_digits"]==2 and result["complete_original_high_lifts"]==27
    changes=[tuple(row["component_zero_linear_change_mod3"]) for row in result["records"]]
    assert set(changes)==set(product(range(3),repeat=2))
    assert all(changes.count(beta)==3 for beta in set(changes))
    assert not result["finite_census_certifies_physical_IID_premise"]
    assert not result["virtual_lifts_are_additional_quantum_samples"]


@pytest.mark.parametrize("key",[(1,2,2),(2,3,3)])
def test_native_alpha_delta_decomposition_at_growing_modulus(cohorts,key):
    for p in cohorts[key]:
        packet=p.branch.packet;q=packet.phase_modulus;retained=q//3
        b=packet.assignment((0,)*p.width+p.complement)
        pairs=[tuple(frequency_coordinates(label,packet.level) for label in row) for row in packet.labels]
        for z in product(range(3),repeat=p.width):
            t=packet.assignment(z+p.complement);actual=[]
            for l in range(packet.secret_dimension):
                low=sum((row[l][0] % 3)*(a-b0) for row,a,b0 in zip(pairs,t,b))
                assert low % 3==0
                high=sum(((row[l][0]-row[l][0] % 3)//3)*(a-b0)+(((row[l][1]-2*row[l][0]) % q)//3)*(int(a==2)-int(b0==2)) for row,a,b0 in zip(pairs,t,b))
                actual.append((low//3+high) % retained)
            assert p.original_value(z)==tuple(actual)


@pytest.mark.parametrize("key",[(1,2,2),(2,3,3)])
def test_physical_signed_injection_at_real_full_root(cohorts,key):
    programs=cohorts[key];c,_=low_relation(programs);j=next(i for i,x in enumerate(c) if x==2);n,d,r=key
    control=injection_control(programs[j],2,tuple((3**r-1-l) % (3**r) for l in range(n)))
    assert control["all_injection_outcomes"]==3**d
    assert control["arbitrary_reference_entangled_max_error"]<1e-12


def test_insufficient_cohort_source_reuse_and_width_budget_rejected(cohorts):
    # Find a nonzero signature source; one column cannot cancel itself.
    program=next(p for p in cohorts[1,2,2] if any(row[1] % 3 for _,tables in p.compact().groups for row in tables))
    with pytest.raises(ValueError,match="no relation"):low_relation((program,))
    with pytest.raises(ValueError,match="ancestry"):low_relation((program,program))
    with pytest.raises(ValueError,match="preflight"):native_cohort(32,16,2,1,max_programs=1000)
    with pytest.raises(ValueError,match="same width"):low_relation((program,cohorts[2,3,3][0]))
    with pytest.raises(ValueError,match="measured word"):cancel(cohorts[1,2,2],())


def test_full_modulus_two_point_law_from_true_original_unit_pivot(cohorts):
    programs=cohorts[1,2,2];c,_=low_relation(programs);selected=[j for j,x in enumerate(c) if x];measured=outcomes(programs)
    j=selected[0];p=programs[j];m=measured[0];source=p.branch.acquisition.source;packet=p.branch.packet
    z0,z1=(0,0),(1,0)
    t0=packet.assignment(m+p.complement)
    t1=packet.assignment(tuple((a+c[j]*b) % 3 for a,b in zip(m,z1))+p.complement)
    odd=next(i for i,(a,b) in enumerate(zip(t0,t1)) if (a-b) % 3)
    pivot=p.branch.acquisition.supports[odd][0];values=[]
    for h in range(9):
        labels=[list(row) for row in source.labels];a,b=(row[0] for row in source.frequencies[pivot])
        labels[pivot][0]=inverse_frequency_coordinates((a+3*h)%27,(b+6*h)%27,6)
        acquisition=PacketAcquisition.from_source(native_source(labels,6),3,p.source_ids,12)
        pointers=tuple(p.branch.anchor[i] for i in p.branch.acquisition.pointers)
        branch=acquisition.branch(pointers,packet.syndrome);cohort=list(programs)
        cohort[j]=NativeProgram(branch,2,p.complement);phase,_=cancel(cohort,measured)
        values.append((phase.value(z1)[0]-phase.value(z0)[0]) % 9)
    assert sorted(values)==list(range(9))


def test_exact_lowest_digit_optimum_matches_full_density_twirl_and_pgm(cohorts):
    programs=cohorts[1,2,2];phase,_=cancel(programs,outcomes(programs));reference=lowest_digit_readout(phase)
    ws=tuple(product(range(3),repeat=2));D=9;states=[]
    for low in range(3):
        rho=np.zeros((D,D),complex)
        for high in range(3):
            psi=np.array([np.exp(2j*np.pi*((low+3*high)*phase.value(z)[0] % 9)/9)/3 for z in ws])
            rho+=np.outer(psi,psi.conj())/3
        states.append(rho)
    average=sum(states)/3;eigenvalues,vectors=np.linalg.eigh(average)
    inverse=vectors @ np.diag([1/math.sqrt(x) if x>1e-10 else 0 for x in eigenvalues]) @ vectors.conj().T
    success=sum(np.trace((inverse @ rho @ inverse/3) @ rho).real/3 for rho in states)
    assert reference["ideal_optimal_lowest_digit_success"]==pytest.approx(success)
    assert not reference["high_secret_twirl_not_tensor_of_independent_per_program_twirls"] is False
    assert reference["reference_only_not_efficient_measurement_implementation"]


def test_collective_bound_uses_shared_high_secret_not_independent_copy_twirl():
    for B in (0,1,4,8):
        bound=program_only_population_bound(8,3,4,B)
        expected=min(Fraction(3**8-1,3**8),Fraction(3**(3*B)-1,3**32))
        assert Fraction(bound["mean_optimal_lowest_digit_advantage_upper"])==expected
        assert bound["same_shared_higher_secret_across_outputs"]
        assert not bound["unused_original_registers_or_additional_outputs_covered"]
        assert not bound["population_bound_applies_to_each_fixed_instance"]


def test_live_independent_checker():
    result=subprocess.run(["node","research/certificates/ternary_ridge_cancellation_crosscheck.js",str(REPORT)],capture_output=True,text=True)
    assert result.returncode==0,result.stderr


@pytest.mark.parametrize("mutation",["relation","signature","degree","root-order","cost","source-census","supply","decoder"])
def test_independent_checker_rejects_mutated_proofs_and_claims(tmp_path,mutation):
    report=json.loads(REPORT.read_text());c=report["native_controls"][2]
    if mutation=="relation":c["coefficients"][0]=(c["coefficients"][0]+1)%3
    elif mutation=="signature":c["low_relation"]["signature_rows"][0]["program_coefficients"][0]=(c["low_relation"]["signature_rows"][0]["program_coefficients"][0]+1)%3
    elif mutation=="degree":c["degree_certificate"]["certified_global_degree_upper"]-=1
    elif mutation=="root-order":c["component_frequency_family_order"]="3"
    elif mutation=="cost":c["full_original_input_cap_charged"]-=1
    elif mutation=="source-census":c["original_linear_source_census"]["records"][0]["component_zero_linear_change_mod3"][0]=(c["original_linear_source_census"]["records"][0]["component_zero_linear_change_mod3"][0]+1)%3
    elif mutation=="supply":c["physical_source_IID_premise_verified"]=True
    else:report["full_root_decoder_supplied"]=True
    p=tmp_path/"mutation.json";p.write_text(json.dumps(report))
    result=subprocess.run(["node","research/certificates/ternary_ridge_cancellation_crosscheck.js",str(p)],capture_output=True,text=True)
    assert result.returncode!=0
