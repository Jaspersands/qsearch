from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import subprocess

import numpy as np
import pytest
from sympy import Matrix, eye

from ternary_character_synchronization import (
    DERIVATION, REPORT, character_validator, lifted_inverse, native_control,
    rank_one_character_lift, source_ledger, synchronization_witness, vocabulary,
)
from ternary_covariant_noise import CovariantRecord


@pytest.fixture(scope="module")
def controls():
    return [native_control(n,r,M,seed) for n,r,M,seed in ((8,2,8,89513),(12,2,12,89523),(8,3,8,89533))]


def records(c):
    return tuple(CovariantRecord(tuple(x["first"]),tuple(x["second"]),tuple(x["outcome"]),x["modulus"]) for x in c["native_records"])


@pytest.mark.parametrize("index",[0,1,2])
def test_real_native_rank_one_PSD_perfect_fit_is_rejected_as_noncharacter(controls,index):
    c=controls[index];w=c["witness"];v=c["validator"]
    assert w["rank_one_witness_is_valid_for_the_relaxation"]
    assert w["no_accidental_formal_difference_resonances"]
    assert w["perfect_local_paired_phase_score"]==3*c["ledger"]["original_native_qutrits"]
    assert v["status"]=="RANK_ONE_PHASE_FIT_NOT_A_CHARACTER"
    assert not v["full_group_character_fit_certified"]
    assert v["first_nonzero_character_relation"]["outcome_phase_residual"]
    q=int(c["ledger"]["modulus"]);phases=np.exp(2j*math.pi*np.array([x["phase_exponent"] for x in w["nodes"]])/q)
    gram=np.outer(phases,phases.conjugate())
    assert np.linalg.eigvalsh(gram).min()>-1e-10
    assert np.diag(gram)==pytest.approx(np.ones(len(phases)))
    assert np.linalg.matrix_rank(gram,tol=1e-8)==1


@pytest.mark.parametrize("q",[3,9,27,81,243])
def test_composite_ring_inverse_uses_safe_prime_field_Newton_lift(q):
    B=[[3,1],[1,0]];X=lifted_inverse(B,q)
    assert (Matrix(B)*X).applyfunc(lambda x:int(x) % q)==eye(2)
    assert (X*Matrix(B)).applyfunc(lambda x:int(x) % q)==eye(2)
    with pytest.raises(ValueError,match="unit determinant"):
        lifted_inverse([[3,0],[0,1]],q)


@pytest.mark.parametrize("index",[0,1,2])
def test_honest_group_characters_pass_and_public_syzygies_are_exact(controls,index):
    c=controls[index];honest=c["honest_character_countercontrol"]
    assert honest["status"]=="EXACT_CHARACTER_FIT"
    assert honest["basis_interpolated_secret_trial"]==c["calibration_secret"]
    A=[row for r in records(c) for row in (r.first,r.second)];y=[x for r in records(c) for x in r.outcome];q=int(c["ledger"]["modulus"])
    for relation in c["validator"]["all_native_group_relations"]:
        weights=relation["native_frequency_relation_weights"]
        assert all(sum(w*row[j] for w,row in zip(weights,A)) % q==0 for j in range(len(A[0])))
        assert sum(w*b for w,b in zip(weights,y)) % q==relation["outcome_phase_residual"]
    assert not c["validator"]["truth_or_hidden_secret_used"]
    assert not c["validator"]["character_validator_is_a_noisy_secret_decoder"]


def test_rank_deficiency_is_unknown_not_proof_of_noncharacter():
    r=(CovariantRecord((1,0,0),(0,1,0),(1,2),9),)
    v=character_validator(r)
    assert v["status"]=="UNKNOWN_NO_FULL_UNIT_ROW_BASIS"
    assert not v["full_group_character_fit_certified"]


def test_actual_label_resonance_can_break_the_fixed_vocabulary_fit():
    r=(CovariantRecord((1,0),(0,1),(0,0),9),CovariantRecord((1,1),(1,8),(1,0),9))
    w=synchronization_witness(r)
    assert w["accidental_difference_resonance_count"]>0
    assert w["violated_difference_constraint_count"]>0
    assert not w["rank_one_witness_is_valid_for_the_relaxation"]
    assert w["constraint_violation_witnesses"][0]["nonzero_phase_residual"]


def test_changing_outcomes_does_not_change_the_fixed_formal_templates(controls):
    r=records(controls[0]);changed=tuple(CovariantRecord(x.first,x.second,tuple((a+1) % x.modulus for a in x.outcome),x.modulus) for x in r)
    first=vocabulary(r);second=vocabulary(changed)
    assert [x["formal_coefficients"] for x in first]==[x["formal_coefficients"] for x in second]
    assert [x["frequency"] for x in first]==[x["frequency"] for x in second]
    assert [x["phase_exponent"] for x in first]!=[x["phase_exponent"] for x in second]
    assert synchronization_witness(changed)["rank_one_witness_is_valid_for_the_relaxation"]


@pytest.mark.parametrize("n,r,M",[(32,3,64),(64,4,128),(128,5,256)])
def test_fixed_vocabulary_source_bound_does_not_claim_label_adaptive_impossibility(n,r,M):
    x=source_ledger(n,r,M);q=3**r;K=6*M+1
    assert Fraction(x["fixed_A2_template_any_accidental_resonance_probability_upper"])==min(Fraction(1),math.comb(K*K,2)*Fraction(3,q)**n)
    assert Fraction(x["any_shared_character_perfectly_fits_noise_probability_upper"])==min(Fraction(1),q**n*Fraction(3,q*q)**M)
    rank=min(Fraction(1),Fraction(3**n-1,2*3**(2*M)))
    assert Fraction(x["unit_basis_rank_failure_probability_upper"])==rank
    assert Fraction(x["local_fake_and_global_rejection_and_unit_basis_probability_lower"])==max(Fraction(0),1-Fraction(x["fixed_A2_template_any_accidental_resonance_probability_upper"])-Fraction(x["any_shared_character_perfectly_fits_noise_probability_upper"])-rank)
    assert not x["same_result_for_label_adaptive_syzygy_templates"]
    assert not x["source_distribution_bound_is_pointwise_certificate"]
    assert not x["quantum_or_all_classical_decoder_lower_bound"]


def test_complete_table_cap_never_silently_certifies_a_partial_audit(controls):
    with pytest.raises(ValueError,match="complete difference-constraint audit"):
        synchronization_witness(records(controls[0]),max_moment_entries=10)
    with pytest.raises(ValueError,match="validated original"):
        synchronization_witness(())
    with pytest.raises(ValueError,match="same secret dimension"):
        character_validator((CovariantRecord((1,),(2,),(0,0),9),CovariantRecord((1,0),(0,1),(0,0),9)))


def test_live_artifact_pins_source_representation_and_scope():
    r=json.loads(REPORT.read_text())
    assert r["derivation_sha256"]==hashlib.sha256(DERIVATION.read_bytes()).hexdigest()
    assert r["existing_identifiability_and_noise_modules_reused_not_reimplemented"]
    assert not r["label_adaptive_lifts_or_all_spectral_methods_ruled_out"]
    assert not r["efficient_noisy_secret_decoder_supplied"] and not r["quantum_speedup_proved"]
    for c in r["native_controls"]:
        assert len(set(c["original_ancestry_ids"]))==c["ledger"]["original_native_qutrits"]
        assert not c["source_law_physically_certified"]


@pytest.mark.parametrize("index",[0,1,2])
def test_polynomial_adaptive_lift_kills_fake_and_preserves_all_honest_characters(controls,index):
    c=controls[index];lift=c["adaptive_character_lift"];q=int(c["ledger"]["modulus"])
    assert lift["every_rank_one_feasible_point_is_a_shared_group_character"]
    assert lift["fake_perfect_local_fit_violated_stencils"]
    assert all(x["kind"]=="native_target" for x in lift["fake_perfect_local_fit_violated_stencils"])
    assert not lift["convex_relaxation_tightness_proved"]
    assert not lift["rank_one_optimum_or_efficient_decoder_supplied"]
    nodes=lift["nodes"];n=len(nodes[0]["frequency"])
    for secret in ((0,)*n,tuple((2*j+1) % q for j in range(n)),(q-1,)*n):
        exponents=[sum(a*b for a,b in zip(x["frequency"],secret)) % q for x in nodes]
        for stencil in lift["linear_moment_stencils"]:
            i,j=stencil["left_entry"];k,l=stencil["right_entry"]
            assert (exponents[i]-exponents[j]-exponents[k]+exponents[l]) % q==0
            assert tuple((a-b) % q for a,b in zip(nodes[i]["frequency"],nodes[j]["frequency"]))==tuple((a-b) % q for a,b in zip(nodes[k]["frequency"],nodes[l]["frequency"]))
    assert lift["dense_PSD_complex_entries"]==len(nodes)**2
    bounds=[]
    for cert in lift["all_rank_PSD_near_perfect_gap_certificates"]:
        assert cert["nonzero_modular_phase_residual"]
        expected=Fraction(8,q*q*cert["one_plus_basis_coefficient_squared_norm"])
        assert Fraction(cert["any_feasible_PSD_objective_gap_lower"])==expected
        bounds.append(expected)
    assert Fraction(lift["any_feasible_PSD_objective_gap_lower"])==max(bounds)>0
    assert lift["gap_is_to_impossible_perfect_score_not_true_secret_score"]


def test_q_loops_reject_nonroot_phase_assignments_not_only_observed_fake(controls):
    c=controls[0];lift=c["adaptive_character_lift"];q=int(c["ledger"]["modulus"])
    basis=lift["unit_basis_frequency_rows"];n=len(basis);theta=[math.sqrt(2)/7]+[0]*(n-1)
    # Assign non-qth-root basis phases and otherwise use their canonical products.
    exponents=[]
    for node in lift["nodes"]:
        exponents.append(sum(node["formal_coefficients"][i]*t for i,t in zip(basis,theta)))
    residuals=[]
    for stencil in lift["linear_moment_stencils"]:
        i,j=stencil["left_entry"];k,l=stencil["right_entry"]
        residuals.append(abs(np.exp(2j*math.pi*(exponents[i]-exponents[j]-exponents[k]+exponents[l]))-1))
    assert max(residuals)>0.1
    assert len(lift["basis_q_loops"])==n


def test_honest_lift_has_zero_fake_fit_gap_instead_of_rejecting_every_source():
    source=(CovariantRecord((1,0),(0,1),(2,3),9),CovariantRecord((1,1),(2,1),(5,7),9))
    lift=rank_one_character_lift(source)
    assert not lift["fake_perfect_local_fit_violated_stencils"]
    assert lift["any_feasible_PSD_objective_gap_lower"]=="0"


def test_adaptive_circuit_preflight_and_rank_failure_never_accept_partial_soundness(controls):
    with pytest.raises(ValueError,match="whole character-circuit node cap"):
        rank_one_character_lift(records(controls[0]),max_nodes=10)
    unknown=rank_one_character_lift((CovariantRecord((1,0,0),(0,1,0),(1,2),9),))
    assert unknown["status"]=="UNKNOWN_NO_FULL_UNIT_ROW_BASIS"
    assert not unknown["rank_one_character_soundness_certified"]


def test_all_rank_gap_and_addition_error_propagation_on_honest_character_mixture(controls):
    c=controls[0];lift=c["adaptive_character_lift"];q=int(c["ledger"]["modulus"]);n=c["ledger"]["components"]
    s1=c["calibration_secret"];s2=(0,)*n
    vectors=np.array([[math.sqrt(.3)*np.exp(2j*math.pi*sum(a*b for a,b in zip(x["frequency"],s1))/q),
                       math.sqrt(.7)*np.exp(2j*math.pi*sum(a*b for a,b in zip(x["frequency"],s2))/q)] for x in lift["nodes"]])
    h=np.exp(2j*math.pi*np.array([x["fake_observed_phase_exponent"] for x in lift["nodes"]])/q)
    epsilon=np.linalg.norm(vectors-h[:,None]*vectors[0],axis=1)
    for stencil in lift["linear_moment_stencils"]:
        i,j=stencil["left_entry"];k,l=stencil["right_entry"]
        left=np.vdot(vectors[j],vectors[i]);right=np.vdot(vectors[l],vectors[k])
        assert left==pytest.approx(right)
        if stencil["kind"]=="addition":assert epsilon[i]<=epsilon[k]+epsilon[l]+1e-12
    score=0.
    native=[x["native_node"] for x in lift["native_target_maps"]]
    for j,r in enumerate(records(c)):
        a,b=native[2*j:2*j+2]
        score+=(np.conjugate(h[a])*np.vdot(vectors[0],vectors[a])).real
        score+=(np.conjugate(h[b])*np.vdot(vectors[0],vectors[b])).real
        score+=(np.conjugate(h[a])*h[b]*np.vdot(vectors[b],vectors[a])).real
    assert 3*len(records(c))-score>=float(Fraction(lift["any_feasible_PSD_objective_gap_lower"]))


CHECKER=Path(__file__).resolve().parents[1]/"research/certificates/ternary_character_synchronization_crosscheck.js"


def test_independent_native_and_adaptive_lift_checker_passes_live_artifact():
    result=subprocess.run(["node",str(CHECKER)],capture_output=True,text=True,check=True)
    x=json.loads(result.stdout)
    assert x["status"]=="PASS" and x["public_native_syzygies"]==56
    assert x["recompiled_adaptive_moment_stencils"]==1164
    assert not x["external_IID_supply_certified"] and not x["noisy_decoder_supplied"]


@pytest.mark.parametrize("mutation",["inverse","relation","moment","tightness","gap","stencil","q_loop","source"])
def test_independent_checker_rejects_false_character_and_lift_evidence(tmp_path,mutation):
    r=json.loads(REPORT.read_text());c=r["native_controls"][0]
    if mutation=="inverse":c["validator"]["modular_unit_basis_inverse"][0][0]+=1
    elif mutation=="relation":c["validator"]["all_native_group_relations"][-1]["outcome_phase_residual"]+=1
    elif mutation=="moment":c["witness"]["nodes"][1]["phase_exponent"]+=1
    elif mutation=="tightness":c["adaptive_character_lift"]["convex_relaxation_tightness_proved"]=True
    elif mutation=="gap":c["adaptive_character_lift"]["any_feasible_PSD_objective_gap_lower"]="1"
    elif mutation=="stencil":c["adaptive_character_lift"]["linear_moment_stencils"].pop()
    elif mutation=="q_loop":c["adaptive_character_lift"]["basis_q_loops"][0]["integer_multiplier"]=3
    elif mutation=="source":c["original_ring_labels"][0][0][0]+=1
    path=tmp_path/"mutated.json";path.write_text(json.dumps(r))
    result=subprocess.run(["node",str(CHECKER),str(path)],capture_output=True,text=True)
    assert result.returncode!=0 and result.stderr
