from fractions import Fraction
from itertools import product
import inspect
import json

import numpy as np
import pytest

from theorems.dcp_forward_sampler_swap import (
    CONTRACT,CONTRACT_ID,REPORT,best_single_swap_advantage,build_report,
    erase_public_target_copy,leading_mode_reference,native_swap_frontier,
    physical_control,sampler_observable,swap_instrument,uniform_fiber_reference,
)
from theorems.dcp_native_parity_observables import measurement_operators,target_geometry


REDUNDANT=((1,2,4,0),)


@pytest.mark.parametrize("mode,success",[("clean",1),("target",.5),("witness",.5),("seed",.75)])
def test_identical_classical_outputs_can_have_different_physical_SWAP_signals(mode,success):
    alpha=uniform_fiber_reference(REDUNDANT,3,history=mode)
    clean=uniform_fiber_reference(REDUNDANT,3)
    assert np.allclose(np.sum(abs(alpha)**2,axis=2),np.sum(abs(clean)**2,axis=2))
    c=physical_control(REDUNDANT,3,1,history=mode)
    assert c["actual_fixed_secret_success_min"]==pytest.approx(success)
    assert c["actual_fixed_secret_success_max"]==pytest.approx(success)
    assert c["sampler_inverse_calls"]==0
    assert c["forward_sampler_calls_per_attempt"]==1
    assert not c["native_scalable_sampler_or_speedup_supplied"]


def test_output_probabilities_and_clean_history_still_do_not_fix_amplitude_phases():
    plus=uniform_fiber_reference(REDUNDANT,3)
    minus=uniform_fiber_reference(REDUNDANT,3,relative_phase=True)
    assert np.allclose(abs(plus)**2,abs(minus)**2)
    assert np.linalg.norm(sampler_observable(REDUNDANT,3,minus))>0
    c=physical_control(REDUNDANT,3,1,relative_phase=True)
    assert c["actual_fixed_secret_success_min"]==pytest.approx(.5)
    # For this explicit dyadic+one-zero-column calibration, a known Z on the
    # free sampler wire repairs the amplitude phase. No native generalization.
    repaired=minus*np.array([(-1)**(y >> 3 & 1) for y in range(16)])[None,:,None]
    assert np.allclose(repaired,plus,atol=1e-14)


def test_public_copy_can_be_cleaned_without_finder_inverse_but_tracing_is_not_cleanup():
    dirty=uniform_fiber_reference(REDUNDANT,3,history="target")
    clean=uniform_fiber_reference(REDUNDANT,3)
    repaired=erase_public_target_copy(dirty)
    assert np.allclose(repaired[:,:,0],clean[:,:,0])
    assert np.count_nonzero(abs(repaired[:,:,1:])>1e-12)==0
    assert np.allclose(erase_public_target_copy(repaired),dirty)
    assert np.linalg.norm(sampler_observable(REDUNDANT,3,dirty))==0
    assert np.linalg.norm(sampler_observable(REDUNDANT,3,repaired))>0


def test_preparing_uniform_redundant_fibers_is_real_CNOT_and_H_algebra_not_a_hidden_oracle():
    alpha=uniform_fiber_reference(REDUNDANT,3)
    # Explicit preparation: copy the three target bits into blank witness bits,
    # then H on its fourth bit. These labels are calibration, not native IID.
    for t in range(8):
        state=np.zeros(16,complex)
        state[t]=1
        after=np.zeros_like(state)
        for y in range(16):
            after[y]=(state[y&7]+(-1)**(y >> 3)*state[(y&7)|8])/np.sqrt(2)
        assert np.allclose(after,alpha[t,:,0],atol=1e-14)


def test_complex_program_pullback_matches_actual_forward_instrument_for_arbitrary_inputs():
    A=((1,2,4),)
    rng=np.random.default_rng(5127)
    alpha=rng.normal(size=(8,8,3))+1j*rng.normal(size=(8,8,3))
    alpha/=np.sqrt(np.sum(abs(alpha)**2,axis=(1,2)))[:,None,None]
    O=sampler_observable(A,3,alpha)
    assert np.allclose(O,O.conj().T,atol=1e-13)
    assert max(abs(np.linalg.eigvalsh(O)))<=1+1e-12
    for _ in range(10):
        psi=rng.normal(size=8)+1j*rng.normal(size=8)
        psi/=np.linalg.norm(psi)
        receipt=swap_instrument(psi,A,3,alpha)
        assert receipt["plus"]+receipt["minus"]+receipt["failure"]==pytest.approx(1)
        assert receipt["guess_even_probability"]==pytest.approx(.5+np.vdot(psi,O@psi).real/2)
        assert receipt["failure"]>0  # Invalid outputs are charged, not resampled.


@pytest.mark.parametrize("v",[Fraction(0),Fraction(1,2),Fraction(3,4),Fraction(1)])
def test_noisy_sampler_signal_uses_original_Hamming_noise_and_all_secrets(v):
    c=physical_control(((2,2,2,2),),3,v)
    assert c["actual_fixed_secret_success_min"]==pytest.approx(c["history_kernel_predicted_success"])
    assert c["actual_fixed_secret_success_max"]==pytest.approx(c["history_kernel_predicted_success"])
    assert c["history_kernel_predicted_success"]<=c["best_one_SWAP_over_arbitrary_target_preparations_success_upper"]+1e-12


@pytest.mark.parametrize("v",[Fraction(1,2),Fraction(3,4),Fraction(1)])
def test_leading_singular_mode_is_achievable_but_does_not_collect_all_noisy_modes(v):
    A=((1,2,3,4),)
    alpha=leading_mode_reference(A,3,v)
    O=sampler_observable(A,3,alpha)
    R=measurement_operators(A,3,v)
    measured=np.trace(O@R["kernel"]).real/32
    assert measured==pytest.approx(best_single_swap_advantage(A,3,v))
    assert measured<=R["reference_optimal_advantage"]+1e-12
    if v<1:
        assert measured<R["reference_optimal_advantage"]-1e-4


@pytest.mark.parametrize("K",[1,2,3])
@pytest.mark.parametrize("v",[Fraction(0),Fraction(1,2),Fraction(1)])
def test_complete_IID_label_census_obeys_SUP_sampler_noise_second_moment_bound(K,v):
    best=[]
    for labels in product(range(8),repeat=K):
        best.append(best_single_swap_advantage((labels,),3,v))
    mean=np.mean(best)
    squared_upper=(((1+v*v)/2)**K-Fraction(1,2**K))/4
    assert mean**2<=float(squared_upper)+1e-12
    if v==0:
        assert mean==pytest.approx(0,abs=1e-12)


@pytest.mark.parametrize("n",[8,32,64,128])
def test_native_oracle_sampler_upper_bound_is_exponential_but_does_not_cover_clean_sources(n):
    K=2*n*(n+8)
    c=native_swap_frontier(n,n+8,K)
    v=Fraction(n-1,n)
    rhs=(((1+v*v)/2)**K-Fraction(1,2**K))/4
    e=c["source_average_SUP_advantage_power_of_two_upper_exponent"]
    assert rhs<=Fraction(1,2**(2*e))
    assert e>=n
    assert not c["general_quantum_receiver_or_selected_subword_no_go"]
    assert not c["correlated_marginal_noise_models_covered"]
    assert native_swap_frontier(n,n+8,K,visibility=1)["source_average_SUP_advantage_power_of_two_upper_exponent"]==1


def test_measuring_the_computed_target_is_not_authorized_by_this_forward_only_route():
    assert "secret" not in inspect.signature(sampler_observable).parameters
    assert "secret" not in inspect.signature(swap_instrument).parameters
    # A target history surviving the forward program kills the bit, so retaining
    # the explicit target in place of uncomputing it is not a harmless shortcut.
    dirty=uniform_fiber_reference(REDUNDANT,3,history="target")
    assert np.count_nonzero(sampler_observable(REDUNDANT,3,dirty))==0


def test_actual_compute_and_uncompute_target_is_a_known_permutation_before_SWAP():
    _,freq,_,_=target_geometry(REDUNDANT,3)
    alpha=uniform_fiber_reference(REDUNDANT,3)
    for secret in (0,1,3):
        psi=np.array([np.exp(2j*np.pi*f[0]*secret/8)/4 for f in freq])
        state=np.zeros((16,16,8),complex)
        for x,f in enumerate(freq):
            state[x,:,f[0]^4]=psi[x]*alpha[f[0]^4,:,0]
        assert np.vdot(state,state)==pytest.approx(1)
        assert np.vdot(state,state.transpose(1,0,2))==pytest.approx(0)
        uncomputed=np.zeros_like(state)
        for x,f in enumerate(freq):
            uncomputed[x]=state[x][:,np.arange(8)^(f[0]^4)]
        assert np.count_nonzero(abs(uncomputed[:,:,1:])>1e-12)==0
        assert np.vdot(uncomputed,uncomputed.transpose(1,0,2)).real==pytest.approx((-1)**(secret%2))


def test_empty_target_fibers_charge_failures_instead_of_granting_a_sampler_success():
    alpha=uniform_fiber_reference(((0,0),),3)
    result=swap_instrument(np.ones(4)/2,((0,0),),3,alpha)
    assert result["failure"]==pytest.approx(1)
    assert result["guess_even_probability"]==pytest.approx(.5)


@pytest.mark.parametrize("n,K",[(1,2),(1,3),(2,2)])
def test_exact_native_average_block_Frobenius_moment_on_complete_original_label_source(n,K):
    q,L=8,2**K
    v=Fraction(1,2)
    total=Fraction(0)
    cases=0
    columns=list(product(range(q),repeat=n))
    for labels in product(columns,repeat=K):
        A=tuple(tuple(column[j] for column in labels) for j in range(n))
        _,_,target,distances=target_geometry(A,3)
        total+=sum((v**(2*int(distances[x,y])) for x in range(L) for y in range(x+1,L) if target[x,y]),Fraction(0))
        cases+=1
    assert total/cases==Fraction(L,2*q**n)*((1+v*v)**K-1)


def test_clean_uniform_sampler_conditional_success_bound_uses_actual_occupancy_not_per_label_promises():
    q,K,L=8,3,8
    success=[]
    l2=[]
    for labels in product(range(q),repeat=K):
        _,frequencies,_,_=target_geometry((labels,),3)
        counts=[sum(f==(t,) for f in frequencies) for t in range(q)]
        tv=sum(abs(Fraction(c,L)-Fraction(1,q)) for c in counts)/2
        achieved=.5+best_single_swap_advantage((labels,),3,1)
        assert achieved>=float(1-tv)-1e-12
        success.append(achieved)
        l2.append(sum((Fraction(c,L)-Fraction(1,q))**2 for c in counts))
    assert sum(l2)/len(l2)==Fraction(q-1,q*L)
    assert np.mean(success)>=1-.5*np.sqrt((q-1)/L)-1e-12


def test_live_artifact_contract_and_no_promotion():
    r=build_report()
    assert json.loads(REPORT.read_text())==r
    assert json.loads(CONTRACT.read_text())["contract_id"]==r["contract_id"]==CONTRACT_ID
    assert len(r["physical_controls"])==8
    assert not r["accepted_speedup_candidate"]
    assert not r["new_active_negative_result_created"]
    assert not r["known_polynomial_coherent_native_sampler_implemented"]


@pytest.mark.parametrize("call",[
    lambda:uniform_fiber_reference(((1,2),),3,history="unavailable_environment_oracle"),
    lambda:uniform_fiber_reference(((1,2),),64),
    lambda:erase_public_target_copy(np.zeros((8,8,3))),
    lambda:native_swap_frontier(2,10,0),
    lambda:native_swap_frontier(2,10,40,visibility=-1),
    lambda:swap_instrument(np.zeros(16),REDUNDANT,3,uniform_fiber_reference(REDUNDANT,3)),
    lambda:sampler_observable(REDUNDANT,3,np.zeros((8,16,1))),
])
def test_invalid_access_models_and_unnormalized_channels_fail_closed(call):
    with pytest.raises(ValueError):
        call()
