from dataclasses import asdict
from fractions import Fraction
from itertools import product
import inspect
import json

import numpy as np
import pytest

from theorems.dcp_correlated_phase_block import density
from theorems.dcp_native_parity_bridge import (
    CONTRACT,CONTRACT_ID,REPORT,build_report,dyadic_phase_plan,finite_parity_control,injected_Z_coin,
    lift_scalar_label,minimum_copies_for_advantage,parity_copy_bound,
    prefix_rescale_plan,reduction_resources,source_pushforward_census,
    unmask_predicted_parity,
)


def test_adapter_never_accepts_the_unknown_secret_and_masks_are_exact_bijections():
    assert "secret" not in inspect.signature(lift_scalar_label).parameters
    for s in range(8):
        images={((s+r[0])%8,r[1]) for r in product(range(8),repeat=2)}
        assert images==set(product(range(8),repeat=2))
        assert sum(x[0]%2 for x in images)==32
    c=source_pushforward_census()
    assert c["secret_mask_pairs_checked"]==512
    assert c["exact_phase_identities_checked"]==32768
    assert not c["native_scaling_relation_t_equals_n_plus_8_used_in_this_small_control"]


def test_actual_private_phase_unitary_gives_the_native_density_without_extra_source():
    for s,r in product(range(8),product(range(8),repeat=2)):
        a,aux=3,5
        sample=lift_scalar_label(3,r,a,(aux,))
        theta=2*np.pi*sample.private_rotation_numerator/8
        U=np.diag([1,np.exp(1j*theta)])
        scalar=density(((a,),),3,(s,),Fraction(3,4))
        native=density(((a,),(aux,)),3,((s+r[0])%8,r[1]),Fraction(3,4))
        assert np.allclose(U@scalar@U.conj().T,native,atol=1e-13)
        assert unmask_predicted_parity(((s+r[0])%8)&1,r)==s%2


def test_public_decoder_view_excludes_private_masks_angles_and_prefixes():
    sample=lift_scalar_label(12,(731,955,186),306,(111,27))
    assert sample.native_decoder_view()=={"original_phase_bits":12,"full_label":[306,111,27]}
    assert set(sample.native_decoder_view())=={"original_phase_bits","full_label"}
    assert "private_rotation_numerator" in asdict(sample)
    plan=sample.private_control_plan()
    assert int(plan["numerator_hex"],16)==(306*731+111*955+27*186)%4096
    assert not plan["arbitrary_rotation_unit_cost_assumed"]
    assert not plan["finite_universal_gate_synthesis_executed"]


def test_refreshing_mask_per_packet_can_destroy_the_shared_secret_identity():
    # Identical labels must give identical phase exponents for ONE fixed native secret.
    a=lift_scalar_label(3,(0,0),1,(1,))
    b=lift_scalar_label(3,(1,0),1,(1,))
    assert a.full_label==b.full_label
    assert a.private_rotation_numerator!=b.private_rotation_numerator
    assert not source_pushforward_census()["per_packet_mask_refresh_has_been_authorized"]


def test_prefix_removal_and_label_truncation_match_actual_remaining_secret():
    for s in range(32):
        for k in range(5):
            p=s%(1 << k)
            for a in range(32):
                plan=prefix_rescale_plan(5,k,p,a)
                q=1 << plan["new_phase_bits"]
                rotation=int(plan["private_rotation"]["numerator_hex"],16)
                assert (a*s+rotation)%32==((1 << k)*plan["new_scalar_label"]*(s >> k))%32
                assert plan["new_scalar_label"]==a%q
                assert not plan["postselection_or_source_inverse_required"]
                assert plan["known_prefix_correctness_is_assumed_not_proved"]


def test_dyadic_phase_gate_terms_reconstruct_the_known_angle_exactly():
    for bits in range(1,8):
        for numerator in range(1 << bits):
            p=dyadic_phase_plan(bits,numerator)
            angle_over_pi=sum((Fraction(1,1 << k) for _,k in p["known_single_wire_phase_terms"]),Fraction(0))
            assert angle_over_pi==Fraction(2*numerator,1 << bits)
            for name,k in p["known_single_wire_phase_terms"]:
                assert name==("Z" if k==0 else "S" if k==1 else "T" if k==2 else "P_DYADIC_REQUIRES_SYNTHESIS")


def test_exact_noise_injection_coin_and_geometric_rejection_budget():
    for n in range(2,40):
        words=range(1 << (2*n-1).bit_length())
        results=[injected_Z_coin(n,u) for u in words]
        accepted=[v for v in results if v is not None]
        assert len(accepted)==2*n
        assert Fraction(sum(accepted),len(accepted))==Fraction(1,2*n)
        assert Fraction(results.count(None),len(results))<Fraction(1,2)


def test_clean_verifier_accepts_true_hypothesis_and_false_average_is_exact_half():
    q=16
    for s,candidate in product(range(q),repeat=2):
        probabilities=[(1+np.cos(2*np.pi*a*(s-candidate)/q))/2 for a in range(q)]
        assert np.mean(probabilities)==pytest.approx(1 if s==candidate else .5,abs=1e-13)
    # This is testing candidate phases on FRESH clean samples, not a supplied inverse of the unknown state.
    assert not reduction_resources(16,128,Fraction(1,16))["correct_scalar_recovery_executed"]


def test_all_POVM_bit_blindness_despite_positive_actual_total_information():
    c=finite_parity_control(((1,2),),4,1)
    assert c["target_difference_ordered_pairs"]==0
    assert c["optimal_original_quantum_parity_guess_probability"]==pytest.approx(.5)
    assert c["actual_mod2_joint_X_parity_guess_probability"]==pytest.approx(.5)
    assert c["actual_mod2_joint_X_total_secret_information_bits"]>.4


@pytest.mark.parametrize("v,guess",[(Fraction(1),1),(Fraction(1,2),.75),(Fraction(0),.5)])
def test_target_presence_is_not_mistaken_for_information_after_full_dephasing(v,guess):
    c=finite_parity_control(((8,),),4,v)
    assert c["target_difference_ordered_pairs"]==2
    assert c["optimal_original_quantum_parity_guess_probability"]==pytest.approx(guess)
    assert c["clean_subset_sum_overlap_optimal_parity_guess_probability"]==pytest.approx(1)


def test_subset_sum_occupancy_overlap_also_handles_noninjective_frequency_maps():
    c=finite_parity_control(((4,4),),4,1)
    assert len(c["subset_sum_occupancy_histogram"])==3
    assert c["clean_subset_sum_overlap_optimal_parity_guess_probability"]==pytest.approx(.75)
    assert c["optimal_original_quantum_parity_guess_probability"]==pytest.approx(.75)


def test_leaking_a_known_auxiliary_secret_coordinate_unlocks_an_otherwise_blind_bit():
    A=((1,2,4),(1,2,3))
    c=finite_parity_control(A,3,1)
    assert c["optimal_original_quantum_parity_guess_probability"]==pytest.approx(.5)
    H=np.array([[1,1],[1,-1]])/np.sqrt(2)
    # Private global-mask coordinate r2 IS the second native secret coordinate.
    for s1,s2 in product(range(8),repeat=2):
        rho=density(((4,),(3,)),3,(s1,s2),1)
        U=np.diag([1,np.exp(-2j*np.pi*3*s2/8)])
        p=np.diag(H@U@rho@U.conj().T@H.T).real
        assert p[s1%2]==pytest.approx(1,abs=1e-13)


@pytest.mark.parametrize("copies",[1,2])
@pytest.mark.parametrize("visibility",[Fraction(1),Fraction(1,2),Fraction(0)])
def test_native_average_optimal_advantage_obeys_mass_bound_not_just_target_existence(copies,visibility):
    q=8
    successes=[]
    for labels in product(range(q),repeat=copies):
        c=finite_parity_control((labels,),3,visibility)
        successes.append(c["optimal_original_quantum_parity_guess_probability"])
    average=np.mean(successes)-.5
    assert average<=float(((1+visibility)**copies-1)/(2*q))+1e-12
    if copies==1:
        assert average==pytest.approx(visibility/16)


@pytest.mark.parametrize("n,t,v",[(1,3,Fraction(1,2)),(2,10,Fraction(1,2)),(8,16,Fraction(7,8)),(64,72,Fraction(63,64))])
def test_independent_noise_copy_threshold_is_exact_and_stricter_than_clean(n,t,v):
    eps=Fraction(1,16)
    needed=minimum_copies_for_advantage(n,t,eps,visibility=v)
    assert ((1+v)**needed-1)/(2*(1 << (n*t)))>=eps
    assert ((1+v)**(needed-1)-1)/(2*(1 << (n*t)))<eps
    assert needed>=minimum_copies_for_advantage(n,t,eps)
    r=parity_copy_bound(n,t,needed,visibility=v)
    assert r["stronger_noisy_threshold_requires_independent_original_Z_faults"]
    assert r["arbitrary_noise_data_processing_claim_is_for_clean_upper_bound_only"]
    assert r["requested_budget_not_excluded_by_this_necessary_bound"]
    assert not r["sufficient_copy_count_or_efficient_decoder_proved"]


def test_completely_dephased_source_has_no_finite_necessary_copy_threshold():
    assert minimum_copies_for_advantage(2,10,Fraction(1,16),visibility=0) is None
    r=parity_copy_bound(2,10,100,visibility=0)
    assert not r["requested_budget_not_excluded_by_this_necessary_bound"]


def test_marginal_visibility_does_not_license_the_independent_noise_bound():
    # Correlated all-Z faults erase each marginal, but preserve even-weight coherences.
    labels=((2,2),)
    pure=density(labels,3,(1,),1)
    Zall=np.diag([1,-1,-1,1])
    correlated=(pure+Zall@pure@Zall)/2
    assert abs(correlated[0,3])==pytest.approx(.25)
    assert abs(density(labels,3,(1,),0)[0,3])==0
    means=[]
    for parity in (0,1):
        states=[density(labels,3,(s,),1) for s in range(parity,8,2)]
        means.append(sum((r+Zall@r@Zall)/2 for r in states)/4)
    guess=.5+np.sum(abs(np.linalg.eigvalsh(means[0]-means[1])))/4
    assert guess==pytest.approx(.75)
    assert parity_copy_bound(1,3,2,visibility=0)["stronger_noisy_threshold_requires_independent_original_Z_faults"]


def test_exact_necessary_copy_count_and_power_bounds_are_not_sufficiency_claims():
    for n,t in ((1,3),(2,10),(8,16),(64,72),(128,136)):
        eps=Fraction(1,16)
        needed=minimum_copies_for_advantage(n,t,eps)
        assert Fraction(2**needed-1,2*(1 << (n*t)))>=eps
        assert Fraction(2**(needed-1)-1,2*(1 << (n*t)))<eps
        c=parity_copy_bound(n,t,3*n)
        exact=min(Fraction(1,2),Fraction(2**(3*n)-1,2*(1 << (n*t))))
        e=c["all_algorithms_bit_advantage_power_of_two_upper_exponent"]
        assert exact<=Fraction(1,1 << e)
        assert not c["sufficient_copy_count_or_efficient_decoder_proved"]
    assert minimum_copies_for_advantage(64,72,Fraction(1,16))==4606
    assert not parity_copy_bound(64,72,192)["requested_budget_not_excluded_by_this_necessary_bound"]


def test_conditional_reduction_charges_every_failure_and_rejects_impossible_copy_hypotheses():
    for t in (10,16,32,64):
        p=reduction_resources(t,2*(t-8)*t,Fraction(1,16),failure_bits=12)
        assert p["status"]=="CONDITIONAL_ON_UNIMPLEMENTED_NATIVE_PARITY_PREDICTOR"
        assert p["fresh_independent_masked_invocations_per_stage"]%2==1
        assert Fraction(p["overall_failure_upper_exact_IF_predictor_hypothesis"])<=Fraction(1,1 << 12)
        assert not p["native_predictor_implemented_or_certified"]
        assert p["finite_gate_synthesis_must_be_paid_not_executed"]
        assert not p["coherent_label_oracle_or_purifying_preparation_environment_supplied"]
    rejected=reduction_resources(72,192,Fraction(1,16))
    assert rejected["status"]=="INCONSISTENT_NATIVE_PREDICTOR_COPY_BUDGET"


def test_exact_noise_matching_can_exclude_a_budget_that_clean_bound_does_not():
    clean=reduction_resources(72,64*72,Fraction(1,16),noise_matching="clean_accepted")
    noisy=reduction_resources(72,64*72,Fraction(1,16))
    assert clean["status"]=="CONDITIONAL_ON_UNIMPLEMENTED_NATIVE_PARITY_PREDICTOR"
    assert noisy["status"]=="INCONSISTENT_NATIVE_PREDICTOR_COPY_BUDGET"
    assert clean["noise_coin_cap_abort_probability_upper_exact"]=="0"


def test_predictor_dimension_threshold_is_not_silently_replaced_by_small_constant_tail():
    r=reduction_resources(80,2*72*80,Fraction(1,16),minimum_predictor_components=64)
    assert r["terminal_suffix_bits"]==71
    assert r["terminal_candidate_count"]==2**71
    assert r["adaptive_bit_stages"]==9
    assert r["polynomial_implication_requires_that_threshold_fixed_independently_of_input_size"]
    assert Fraction(r["overall_failure_upper_exact_IF_predictor_hypothesis"])<=Fraction(1,2**16)
    with pytest.raises(ValueError,match="terminal exhaustive cost"):
        reduction_resources(20,1000,Fraction(1,16),minimum_predictor_components=64)


def test_live_report_replays_and_does_not_instantiate_the_missing_predictor():
    r=build_report()
    assert json.loads(REPORT.read_text())==r
    assert len(r["parity_density_controls"])==8
    assert not r["native_predictor_implemented_or_certified"]
    assert not r["positive_mutual_information_instantiates_predictor"]
    assert not r["actual_quantum_source_or_recovery_executed"]
    assert not r["accepted_speedup_candidate"]
    assert r["contract_id"]==CONTRACT_ID
    assert json.loads(CONTRACT.read_text())["contract_id"]==CONTRACT_ID


@pytest.mark.parametrize("call",[
    lambda:lift_scalar_label(3,(1,2),8,(1,)),
    lambda:lift_scalar_label(3,(1,2),1,()),
    lambda:prefix_rescale_plan(4,2,4,1),
    lambda:minimum_copies_for_advantage(2,10,0),
    lambda:reduction_resources(9,100,Fraction(1,16)),
    lambda:parity_copy_bound(2,10,-1),
    lambda:minimum_copies_for_advantage(2,10,Fraction(1,16),visibility=-1),
    lambda:reduction_resources(16,100,Fraction(1,16),noise_matching="marginals_only"),
])
def test_invalid_sources_prefixes_and_hypotheses_fail_closed(call):
    with pytest.raises(ValueError):
        call()
