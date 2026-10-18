from fractions import Fraction
from itertools import product
from math import comb
import inspect
import json

import numpy as np
import pytest

from theorems.dcp_correlated_phase_block import density
from theorems.dcp_native_parity_bridge import finite_parity_control
from theorems.dcp_native_parity_observables import (
    CONTRACT,CONTRACT_ID,REPORT,_power_upper_exponent,build_report,
    measurement_operators,physical_control,rank_noise_scope_control,short_target_exclusion,
    sparse_observable_frontier,target_geometry,
)


@pytest.mark.parametrize("n,t,K,f",[(1,3,2,1),(1,3,3,1),(2,10,40,2),(64,72,9216,64)])
def test_oriented_union_count_and_maximal_exclusion_are_exact(n,t,K,f):
    c=short_target_exclusion(n,t,K,f)
    r=c["excluded_signed_support_weights_through"]
    count=sum(comb(K,w)*2**(w-1) for w in range(1,r+1))
    assert int(c["oriented_short_signed_witness_count_hex"],16)==count
    assert Fraction(count,2**(n*t))<=Fraction(1,2**f)
    if r<K:
        assert Fraction(count+comb(K,r+1)*2**r,2**(n*t))>Fraction(1,2**f)
    assert c["minimum_target_edge_Hamming_distance_on_good_labels"]==r+1


@pytest.mark.parametrize("K",[1,2,3])
def test_complete_IID_label_census_obeys_the_signed_unit_coefficient_union_bound(K):
    c=short_target_exclusion(1,3,K,1)
    r=c["excluded_signed_support_weights_through"]
    exceptions=0
    for labels in product(range(8),repeat=K):
        _,_,matches,distances=target_geometry((labels,),3)
        exceptions+=bool(np.any(matches & (distances<=r)))
    union=Fraction(int(c["oriented_short_signed_witness_count_hex"],16),8)
    assert Fraction(exceptions,8**K)<=union


@pytest.mark.parametrize("n",[8,16,32,64,128])
def test_exact_native_frontier_includes_rare_labels_and_polynomial_degree_scope(n):
    N=n*(n+8)
    for D in (1,n**4):
        c=sparse_observable_frontier(n,n+8,2*N,D)
        r=c["excluded_signed_support_weights_through"]
        assert r>=N//16  # Independent generating-function proof in the note.
        v=Fraction(n-1,n)
        root=c["ceil_sqrt_target_row_degree"]
        good=min(Fraction(1,2),Fraction(root,2)*v**(r+1))
        averaged=min(Fraction(1,2),good+Fraction(1,2**(n+1)))
        e=c["average_advantage_power_of_two_upper_exponent"]
        assert averaged<=Fraction(1,2**e)
        assert c["sparse_class_excluded_at_requested_average_advantage"]==(averaged<Fraction(1,16))
        assert not c["all_polynomial_gate_circuits_induce_sparse_observables"]
        assert not c["general_DCP_or_quantum_decoder_no_go"]
        if n>=64:
            assert c["sparse_class_excluded_at_requested_average_advantage"]


def test_clean_source_does_not_inherit_the_noise_sparsity_penalty():
    c=sparse_observable_frontier(64,72,9216,1,visibility=1)
    assert not c["sparse_class_excluded_at_requested_average_advantage"]
    assert c["average_advantage_power_of_two_upper_exponent"]==1
    c=sparse_observable_frontier(2,10,40,1,visibility=0)
    assert c["good_label_advantage_exactly_zero"]
    assert c["good_label_advantage_power_of_two_upper_exponent"] is None


@pytest.mark.parametrize("v",[Fraction(0),Fraction(1,2),Fraction(3,4),Fraction(1)])
def test_public_only_reference_operators_are_valid_POVMs_and_actual_Born_probabilities(v):
    assert "secret" not in inspect.signature(measurement_operators).parameters
    A=((2,2,2,2),)
    R=measurement_operators(A,3,v)
    L=16
    for name in ("matching","optimal"):
        O=R[name+"_observable"]
        assert np.allclose(O,O.conj().T,atol=1e-12)
        for sign in (-1,1):
            E=(np.eye(L)+sign*O)/2
            assert np.linalg.eigvalsh(E).min()>=-1e-12
        assert np.max(abs(O[~R["target_mask"]]))<1e-10
    c=physical_control(A,3,v)
    old=finite_parity_control(A,3,v)
    assert c["original_quantum_optimal_success_probability"]==pytest.approx(old["optimal_original_quantum_parity_guess_probability"])
    assert c["pairing_success_spread_over_all_fixed_secrets"]<1e-12
    assert c["measured_pairing_success_probability"]<=c["original_quantum_optimal_success_probability"]+1e-12


def test_partial_involution_readout_is_an_actual_complete_measurement_not_conditioned_coverage():
    A=((2,2,2,2),)
    v=Fraction(3,4)
    R=measurement_operators(A,3,v)
    L=16
    H=np.eye(L)
    plus,minus,unused=[],[],set(range(L))
    for x,y,_ in R["matching_edges"]:
        H[x,x]=H[x,y]=H[y,x]=1/np.sqrt(2)
        H[y,y]=-1/np.sqrt(2)
        plus.append(x)
        minus.append(y)
        unused-={x,y}
    assert np.allclose(H@H.T,np.eye(L),atol=1e-12)
    for s in range(8):
        final=H@density(A,3,(s,),v)@H.T
        p=final.diagonal().real
        correct=(p[plus] if s%2==0 else p[minus]).sum()+sum(p[x] for x in unused)/2
        assert correct==pytest.approx(.5+R["reference_matching_advantage"])


def test_dense_collective_measurement_can_beat_disjoint_pairing_without_becoming_an_algorithm():
    c=physical_control(((2,2,2,2),),3,Fraction(3,4))
    assert c["original_quantum_optimal_success_probability"]>c["measured_pairing_success_probability"]+.08
    assert c["exponential_enumeration_and_spectral_costs_paid_as_reference_only"]
    assert not c["finite_universal_gate_receiver_exported"]


def test_Cauchy_bound_also_covers_complex_norm_one_observables_not_only_matchings():
    R=measurement_operators(((2,2,2,2),),3,Fraction(1,4))
    target=R["target_mask"]
    D=int(max(target.sum(axis=1)))
    O=np.zeros((16,16),complex)
    for x in range(16):
        for y in range(x+1,16):
            if target[x,y]:
                O[x,y]=(1j if (x+y)%2 else -1)/D
                O[y,x]=O[x,y].conjugate()
    assert np.max(abs(np.linalg.eigvalsh(O)))<=1+1e-12
    w=int(min(R["distances"][target]))
    advantage=abs(np.trace(O@R["kernel"]).real)/(2*16)
    assert advantage<=np.sqrt(D)*float(Fraction(1,4)**w)/2+1e-12


def test_weighted_frequency_pair_singular_values_not_unweighted_occupancies_give_noisy_optimum():
    R=measurement_operators(((2,2,2,2),),3,Fraction(3,4))
    blocks=R["weighted_frequency_pair_blocks"]
    assert len(blocks)==2
    assert any(b["numerical_rank_not_exact_certificate"]>1 for b in blocks)
    block_adv=sum(sum(b["singular_values"]) for b in blocks)/16
    assert block_adv==pytest.approx(R["reference_optimal_advantage"])
    clean=measurement_operators(((2,2,2,2),),3,1)
    assert all(b["numerical_rank_not_exact_certificate"]==1 for b in clean["weighted_frequency_pair_blocks"])


def test_just_computing_the_frequency_cannot_supply_the_parity_readout():
    A=((2,2,2,2),)
    _,freq,_,_=target_geometry(A,3)
    for secret in range(8):
        state=np.zeros((16,8),complex)
        for x,f in enumerate(freq):
            state[x,f[0]]=np.exp(2j*np.pi*f[0]*secret/8)/4
        # X on the top frequency bit, ignoring original x, is exactly blind.
        expectation=np.vdot(state,state[:,np.arange(8)^4]).real
        assert expectation==0
    assert physical_control(A,3,1)["original_quantum_optimal_success_probability"]>.9


@pytest.mark.parametrize("K",[2,4,6])
def test_polynomial_gate_implementation_can_have_exponentially_dense_effective_observable(K):
    H=np.array([[1,1],[1,-1]])/np.sqrt(2)
    U=np.ones((1,1))
    for _ in range(K):
        U=np.kron(U,H)
    L=1 << K
    multiZ=np.eye(L)
    multiZ[-1,-1]=-1
    actual=U@multiZ@U
    signs=np.array([(-1)**x.bit_count() for x in range(L)])
    closed=np.eye(L)-2*np.outer(signs,signs)/L
    assert np.allclose(actual,closed,atol=1e-12)
    # The SAME dense observable needs only product-X readout plus a classical AND.
    Eminus=np.outer(U[-1],U[-1])
    assert np.allclose(np.eye(L)-2*Eminus,closed,atol=1e-12)
    assert np.allclose(actual@actual,np.eye(L),atol=1e-12)
    assert all(sum(abs(actual[x,y])>1e-12 for y in range(L) if y!=x)==L-1 for x in range(L))
    _,_,target,_=target_geometry(((4,)*K,),3)
    assert np.all(target.sum(axis=1)==L//2)


def test_correlated_zero_marginal_visibility_cannot_be_inserted_into_the_independent_noise_bound():
    A=((2,2),)
    R=measurement_operators(A,3,0)
    O=R["matching_observable"]
    Z=np.diag([1,-1,-1,1])
    correct=[]
    for s in range(8):
        r=density(A,3,(s,),1)
        r=(r+Z@r@Z)/2
        correct.append(.5+(1-2*(s%2))*np.trace(O@r).real/2)
    assert np.mean(correct)==pytest.approx(.75)
    assert R["reference_matching_advantage"]==0
    assert sparse_observable_frontier(2,10,40,1)["requires_original_independent_Z_faults_not_only_marginal_visibilities"]


def test_integer_power_bounds_do_not_round_rare_events_to_zero():
    for a,b in ((1,2),(3,8),(1,2**1000),(2**101,2**103),(7,8)):
        e=_power_upper_exponent(a,b)
        assert Fraction(a,b)<=Fraction(1,2**e)
        assert Fraction(a,b)>Fraction(1,2**(e+1))
    assert _power_upper_exponent(0,8) is None


@pytest.mark.parametrize("t",[16,32,72,128])
def test_growing_rank_noise_obstruction_is_not_transferred_to_scalar_or_clean_source(t):
    c=rank_noise_scope_control(t)
    native,scalar,clean=c["regimes"]
    assert native["secret_entropy_bits"]==(t-8)*t
    assert scalar["secret_entropy_bits"]==t
    assert native["independent_original_Z_visibility_exact"]==scalar["independent_original_Z_visibility_exact"]
    assert Fraction(native["expected_original_Z_faults_exact"])==t
    assert Fraction(scalar["expected_original_Z_faults_exact"])==Fraction(t,t-8)
    assert clean["expected_original_Z_faults_exact"]=="0"
    for row in c["regimes"]:
        v=Fraction(row["independent_original_Z_visibility_exact"])
        e=row["minimum_coherence_if_a_target_edge_exists_power_of_two_lower_exponent"]
        assert v**row["original_phase_qubits"]>=Fraction(1,2**e)
        assert not row["target_edges_or_efficient_receiver_existence_proved"]
    assert not c["growing_rank_noise_bound_is_a_scalar_DCP_lower_bound"]
    assert not c["clean_scalar_DCP_lift_requires_injecting_noise"]


def test_live_report_replays_with_all_non_algorithm_scope_flags():
    r=build_report()
    assert json.loads(REPORT.read_text())==r
    assert json.loads(CONTRACT.read_text())["contract_id"]==r["contract_id"]==CONTRACT_ID
    assert len(r["native_frontiers"])==10
    assert len(r["physical_controls"])==6
    assert not r["accepted_speedup_candidate"]
    assert not r["new_active_negative_result_created"]
    assert not r["general_quantum_decoder_impossibility_proved"]
    assert not r["novelty_claim"]


@pytest.mark.parametrize("call",[
    lambda:short_target_exclusion(2,10,0,2),
    lambda:short_target_exclusion(2,10,40,0),
    lambda:sparse_observable_frontier(2,10,40,True),
    lambda:sparse_observable_frontier(2,10,40,1,visibility=-1),
    lambda:sparse_observable_frontier(2,10,40,1,advantage=0),
    lambda:target_geometry(((8,1),),3),
    lambda:target_geometry(((1,)*9,),3),
    lambda:physical_control(((1,2),(2,3)),64,1),
])
def test_invalid_models_and_exponential_controls_fail_closed(call):
    with pytest.raises(ValueError):
        call()
