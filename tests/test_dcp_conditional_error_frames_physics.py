from fractions import Fraction
from itertools import product
from math import comb,factorial
import inspect
import json

import numpy as np
import pytest

from theorems.dcp_conditional_error_frames import (
    CONTRACT,CONTRACT_ID,REPORT,born_gram_bound,build_report,dense_frame_transforms,
    finite_frames,native_frontier,parity_harmless_alias_control,physical_control,
)


@pytest.mark.parametrize("K",[2,3,4])
def test_exact_signed_occupancy_moment_for_all_fixed_nonzero_differences(K):
    q,L=4,1 << K
    totals=[Fraction(0) for _ in range(L)]
    for labels in product(range(q),repeat=K):
        _,_,_,rows=finite_frames((labels,),2,(0,))
        for d in range(1,L):
            totals[d]+=sum(sum((-1)**((d&x).bit_count()) for x in row["words"])**2 for row in rows)
    assert {z/q**K for z in totals[1:]}=={Fraction(L*(q-1),q)}


def test_complete_source_census_checks_Born_normalization_not_only_raw_signed_counts():
    q,K,L=4,5,32
    total=Fraction(0)
    for labels in product(range(q),repeat=K):
        _,_,_,rows=finite_frames((labels,),2,(0,1))
        total+=sum((Fraction(row["Gram_denominator"],L)*row["Gram_error_Frobenius_squared"] for row in rows),Fraction(0))
    mean=total/q**K
    assert mean<=born_gram_bound(q,L,2)<1
    assert mean>0


def test_label_adaptive_error_alias_does_not_inherit_the_fixed_difference_average():
    q,K,L=4,5,32
    aliases=0
    total=Fraction(0)
    for labels in product(range(q),repeat=K):
        d=sum((a&1) << i for i,a in enumerate(labels))
        if not d:
            continue
        _,_,_,rows=finite_frames((labels,),2,(0,d))
        weighted=sum((Fraction(row["Gram_denominator"],L)*row["Gram_error_Frobenius_squared"]/2 for row in rows),Fraction(0))
        assert weighted==1
        total+=weighted
        aliases+=1
    assert aliases==q**K-(q//2)**K
    assert total/q**K>Fraction(4*(q-1),L)


@pytest.mark.parametrize("A,E",[
    (((1,2,0,0),),(0,4,8)),
    (((1,1,1,1,1,1),),(0,1)),
    (((1,2,3,1,0,2),),(0,1,2)),
])
def test_actual_error_frames_and_public_controlled_unitaries_match_exact_Gram_algebra(A,E):
    _,errors,_,rows,transforms,diagnostic=dense_frame_transforms(A,2,E)
    L=1 << len(A[0])
    assert "secret" not in inspect.signature(dense_frame_transforms).parameters
    for row,diag in zip(rows,diagnostic):
        d=row["Gram_denominator"]
        Phi=np.zeros((L,len(errors)))
        for x in row["words"]:
            Phi[x]=[(-1)**((e&x).bit_count())/np.sqrt(d) for e in errors]
        expected=np.array(row["signed_Gram_numerators"])/d
        assert np.allclose(Phi.T@Phi,expected,atol=1e-13)
        eta=Fraction(row["Gram_error_Frobenius_squared"])
        assert np.linalg.norm(expected-np.eye(len(errors)))**2==pytest.approx(float(eta))
        U=transforms[row["frequency"]]
        assert np.allclose(U@U.T,np.eye(L),atol=1e-12)
        if eta<1:
            assert np.linalg.norm(U@Phi-np.eye(L)[:,list(errors)])**2<=float(eta)+1e-12
        else:
            assert diag["unitary_identity_on_bad_frames"]


def test_nonzero_Gram_overlap_has_a_real_approximate_multimode_transform():
    c=physical_control(((1,1,1,1,1,1),),2,(0,1))
    assert 0<Fraction(c["Born_weighted_Gram_error_squared_exact"])<1
    assert c["max_original_error_state_transport_squared_error"]>1e-5
    assert c["actual_success_min"]>=c["state_distance_success_lower"]-1e-12
    assert not c["uniform_polynomial_transform_implemented"]


def test_known_orthogonal_error_modes_can_be_corrected_without_actual_error_input():
    c=physical_control(((1,2,0,0),),2,(0,4,8))
    assert c["Born_weighted_Gram_error_squared_exact"]=="0"
    assert c["actual_success_min"]==pytest.approx(1)
    assert c["max_original_error_state_transport_squared_error"]<1e-20
    assert c["conditioned_on_error_set_not_full_noise_law"]


def test_full_independent_noise_replay_pays_the_omitted_error_probability():
    A=((1,2,0,0),)
    _,errors,_,rows,transforms,_=dense_frame_transforms(A,2,(0,4,8))
    p=Fraction(1,8)
    mass={e:p**e.bit_count()*(1-p)**(4-e.bit_count()) for e in range(16)}
    tail=1-sum(mass[e] for e in errors)
    for s in range(4):
        success=0.0
        for e in range(16):
            state=np.zeros((16,4),complex)
            for row in rows:
                f=row["frequency"][0]
                for x in row["words"]:
                    state[x,f]=np.exp(2j*np.pi*f*s/4)*(-1)**((e&x).bit_count())/4
                state[:,f]=transforms[(f,)]@state[:,f]
            correct=.5+(-1)**(s%2)*np.vdot(state,state[:,np.arange(4)^2]).real/2
            success+=float(mass[e])*correct
        assert success>=float(1-tail)-1e-12
        assert success<1


def test_bad_frame_gate_is_not_a_general_noise_or_parity_no_go():
    c=physical_control(((1,1,1,1),),2,(0,15))
    assert all(not row["good_frame_exact_gate"] for row in c["fiber_frames"])
    alias=parity_harmless_alias_control()
    assert alias["known_dense_clean_readout_success"]>.9
    assert not alias["Gram_near_identity_is_necessary_for_parity_recovery"]
    assert not alias["first_secret_parity_changed"]


def test_locally_invisible_frame_phase_gauges_must_not_erase_relative_bit_phase():
    A=((1,2,0,0),)
    _,errors,freq,rows,transforms,_=dense_frame_transforms(A,2,(0,4,8))
    for s in range(4):
        aligned=np.zeros((16,4),complex)
        gauged=np.zeros_like(aligned)
        for row in rows:
            f=row["frequency"][0]
            source=np.zeros(16,complex)
            for x in row["words"]:
                source[x]=np.exp(2j*np.pi*f*s/4)/4
            output=transforms[(f,)]@source
            aligned[:,f]=output
            gauged[:,f]=(-1)**(f >> 1)*output
            assert np.allclose(np.outer(output,output.conj()),np.outer(gauged[:,f],gauged[:,f].conj()))
        correct=.5+(-1)**(s%2)*np.vdot(aligned,aligned[:,np.arange(4)^2]).real/2
        wrong=.5+(-1)**(s%2)*np.vdot(gauged,gauged[:,np.arange(4)^2]).real/2
        assert correct==pytest.approx(1)
        assert wrong==pytest.approx(0)


def test_generic_mode_label_projection_is_not_free_even_for_orthogonal_frames():
    _,errors,_,rows=finite_frames(((1,2,0,0),),2,(0,4,8,12))
    M=len(errors)
    for row in rows:
        signs=np.zeros((16,M),dtype=int)
        for x in row["words"]:
            signs[x]=[(-1)**((e&x).bit_count()) for e in errors]
        # Exact dyadic Gram/projection sums avoid unnecessary floating BLAS.
        gram=[[int(np.sum(signs[:,i]*signs[:,j])) for j in range(M)] for i in range(M)]
        assert gram==[[4*int(i==j) for j in range(M)] for i in range(M)]
        for j in range(M):
            projected=[Fraction(gram[i][j],8) for i in range(M)]
            assert sum(z*z for z in projected)==Fraction(1,M)


@pytest.mark.parametrize("n",[8,16,32,64,128])
def test_native_information_bound_counts_typical_errors_tail_and_missing_compiler(n):
    r=native_frontier(n)
    t,K=n+8,2*n*(n+8)
    M=sum(comb(K,j) for j in range(2*t+1))
    assert int(r["typical_error_pattern_count_hex"],16)==M
    assert r["generic_uniform_mode_erasure_projection_probability_power_of_two_exponent"]==(M-1).bit_length()
    assert not r["generic_projection_is_a_lower_bound_on_all_structured_transforms"]
    assert Fraction(r["expected_original_Z_errors_exact"])==t
    assert r["original_word_and_frequency_register_qubits"]==3*n*t
    assert not r["exponential_classical_reference_memory_implies_exponential_quantum_width"]
    ratio=Fraction(2**(n*t)-1,2**K)
    norm=20*M*(M-1)*ratio
    e=r["source_average_parity_failure_upper_power_of_two_exponent_IF_arbitrary_frame_unitary"]
    if norm>=1:
        assert e==0
    else:
        assert e>=1
        norm_e=r["source_average_transport_state_distance_upper_power_of_two_exponent"]
        assert norm<=Fraction(1,2**(2*norm_e))
        # Independently round square roots via an exact squared comparison.
        upper=Fraction(1,2**(norm_e))+Fraction(1,2**((n*t)//2+1))+Fraction(11,16)**t
        assert upper<=Fraction(1,2**e)
    assert not r["uniform_poly_time_or_space_frame_unitary_implemented"]
    assert not r["approximate_orthogonality_is_an_efficient_syndrome_decoder"]
    assert not r["frame_source_bound_allows_label_adaptive_error_sets"]


def test_rational_Chernoff_constant_is_outward_and_actual_small_binomial_tail_is_smaller():
    exp_upper=sum((Fraction(1,factorial(j)) for j in range(5)),Fraction(0))+Fraction(1,100)
    assert exp_upper<Fraction(11,4)
    n=2
    t=n+8
    K=2*n*t
    p=Fraction(1,2*n)
    tail=sum((comb(K,j)*p**j*(1-p)**(K-j) for j in range(2*t+1,K+1)),Fraction(0))
    assert tail<=Fraction(11,16)**t


def test_live_report_contract_and_no_efficiency_or_speedup_promotion():
    r=build_report()
    assert json.loads(REPORT.read_text())==r
    assert json.loads(CONTRACT.read_text())["contract_id"]==r["contract_id"]==CONTRACT_ID
    assert len(r["physical_controls"])==4
    assert not r["accepted_speedup_candidate"]
    assert not r["new_active_negative_result_created"]
    assert not r["novelty_claim"]


@pytest.mark.parametrize("call",[
    lambda:finite_frames(((1,2),),2,()),
    lambda:finite_frames(((1,2),),2,(0,0)),
    lambda:finite_frames(((1,2),),2,(0,4)),
    lambda:finite_frames(((4,2),),2,(0,1)),
    lambda:finite_frames(((1,)*10,),2,(0,1)),
    lambda:native_frontier(1),
    lambda:born_gram_bound(8,16,17),
])
def test_invalid_or_exponentially_large_controls_fail_closed(call):
    with pytest.raises(ValueError):
        call()
