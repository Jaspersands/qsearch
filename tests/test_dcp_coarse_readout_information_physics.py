from fractions import Fraction
from itertools import product
import json
import math

import numpy as np
import pytest
from scipy.linalg import hadamard

from theorems.dcp_correlated_phase_block import density
from theorems.dcp_nonlinear_fiber_pairing import phase_value
from theorems.dcp_correlated_block_observables import information
from theorems.dcp_coarse_readout_information import (
    REPORT,build_report,finite_control,native_frontier,product_twirl_plan,
    raw_information_rate_lower,
)
from theorems.dcp_correlated_block_observables import measurement_channel
from theorems.dcp_quadratic_fiber_coordinates import coordinate_plan,lift_free_word


def h2(p):
    return -sum(x*math.log2(x) for x in (p,1-p) if x>1e-30)


@pytest.mark.parametrize("v",[Fraction(0),Fraction(1,4),Fraction(3,4),Fraction(1)])
def test_every_dyadic_phase_grid_entropy_is_bounded_by_the_exact_series(v):
    lower=float(raw_information_rate_lower(v))
    for order in (1,2,4,8,16,64,256):
        entropy=sum(h2((1+float(v)*math.cos(2*math.pi*j/order))/2) for j in range(order))/order
        assert 1-entropy>=lower-1e-12


def test_log_constant_and_uniform_linear_asymptotic_constant_are_rationally_certified():
    x=Fraction(7,10)
    expansion=sum((x**k/Fraction(math.factorial(k)) for k in range(4)),Fraction(0))
    assert expansion==Fraction(12013,6000)>2
    assert 5*raw_information_rate_lower(Fraction(63,64))-2>Fraction(1,16)
    assert 3*raw_information_rate_lower(Fraction(63,64))-1>Fraction(1,4)
    for n in (64,65,128,256,1024):
        c=native_frontier(n)
        assert Fraction(c["discard_syndrome_fixed_X_information_lower_bits_exact"])>=Fraction(n,4)
        wide=native_frontier(n,coarse_bits=2,width_multiple=5)
        assert Fraction(wide["discard_syndrome_fixed_X_information_lower_bits_exact"])>=Fraction(n,16)
        m,t=5*n,n+8
        assert Fraction(3**m-1,1 << (t*n))<Fraction(1,1 << (n*n))
        assert not c["full_secret_identification_or_efficient_inference_proved"]
        assert not c["information_lower_bound_is_a_sample_complexity_upper_bound"]


@pytest.mark.parametrize("v",[Fraction(0),Fraction(3,4),Fraction(1)])
def test_original_density_X_readout_matches_bernoulli_marginals_and_chain_rule(v):
    A,t,m=((1,2,4,8,16),),6,5
    H=hadamard(1 << m)/np.sqrt(1 << m)
    raw=[]
    for s in range(64):
        rho=density(A,t,(s,),v)
        measured=np.diag(H@rho@H.T).real
        formula=np.array([np.prod([(1+(-1)**(z >> i & 1)*float(v)*np.cos(2*np.pi*A[0][i]*s/64))/2 for i in range(m)]) for z in range(1 << m)])
        assert np.allclose(measured,formula,atol=1e-13)
        raw.append(np.maximum(measured,0))
    raw=np.array(raw)
    assert raw.mean(axis=0)==pytest.approx(np.full(32,1/32))
    lumped=raw.reshape(4,16,32).mean(axis=0)
    Iraw=information(raw)["uniform_secret_mutual_information_bits"]
    Ipinch=information(lumped)["uniform_secret_mutual_information_bits"]
    c=finite_control(A,t,v)
    assert Iraw==pytest.approx(c["raw_full_original_secret_information_bits"])
    assert Ipinch==pytest.approx(c["pinched_residual_secret_X_information_bits"])
    assert -1e-12<=Iraw-Ipinch<=2+1e-12
    assert Ipinch>=float(Fraction(c["certified_information_lower_bits_exact"]))-1e-12


@pytest.mark.parametrize("common_mode",[False,True])
@pytest.mark.parametrize("coarse_bits",[1,2])
def test_actual_phase_H_twirl_gates_match_discarded_coarse_measurement(common_mode,coarse_bits):
    A,t,m=((1,5,9),),4,3
    v=Fraction(3,4)
    rho=density(A,t,(1,),1 if common_mode else v)
    if common_mode:
        Z=np.diag([(-1)**x.bit_count() for x in range(8)])
        rho=(1+float(v))/2*rho+(1-float(v))/2*Z@rho@Z
    H=hadamard(8)/np.sqrt(8)
    pinched=np.array([[rho[x,z] if phase_value(A,x,1 << coarse_bits)==phase_value(A,z,1 << coarse_bits) else 0 for z in range(8)] for x in range(8)])
    expected=np.diag(H@pinched@H.T).real
    twirled=np.zeros(8)
    for u in range(1 << coarse_bits):
        plan=product_twirl_plan(A,t,(u,),coarse_bits=coarse_bits)
        U=np.eye(8,dtype=complex)
        for gate in plan["gates"]:
            if gate[0] in ("S","Z"):
                phase=1j if gate[0]=="S" else -1
                G=np.diag([phase if x >> gate[1] & 1 else 1 for x in range(8)])
            else:
                G=np.zeros((8,8))
                mask=1 << gate[1]
                for x in range(8):
                    G[x,x]=(-1 if x&mask else 1)/np.sqrt(2)
                    G[x^mask,x]=1/np.sqrt(2)
            U=G@U
        twirled+=np.diag(U@rho@U.conj().T).real/(1 << coarse_bits)
        assert plan["extra_zero_qubits"]==0
        assert plan["pointwise_z_channel_equality_is_after_ignoring_twirl_values"]
        assert plan["twirl_values_may_be_retained_without_weakening_information_lower_bound"]
        assert plan["baseline_requires_actual_unknown_secret_phase_qubits"]
        assert not plan["classical_simulation_of_unknown_secret_data_supplied"]
    assert twirled==pytest.approx(expected)


def test_arbitrary_correlated_secret_independent_Z_faults_need_not_factor():
    A,t,m=((1,2,4),),4,3
    H=hadamard(8)/np.sqrt(8)
    faults={0:Fraction(4,5),3:Fraction(1,10),5:Fraction(1,10)}
    visibilities=[sum(p*(-1)**(e >> i & 1) for e,p in faults.items()) for i in range(m)]
    assert visibilities==[Fraction(3,5),Fraction(4,5),Fraction(4,5)]
    raw=[]
    for s in range(16):
        rho=density(A,t,(s,),1)
        noisy=np.zeros_like(rho)
        for e,p in faults.items():
            Z=np.diag([(-1)**((x&e).bit_count()) for x in range(8)])
            noisy+=float(p)*Z@rho@Z
        raw.append(np.maximum(np.diag(H@noisy@H.T).real,0))
    raw=np.array(raw)
    assert raw.mean(axis=0)==pytest.approx(np.full(8,1/8))
    assert information(raw)["uniform_secret_mutual_information_bits"]>=3*float(raw_information_rate_lower(Fraction(3,5)))
    assert not np.allclose(raw,[[np.prod([(1+(-1)**(z >> i & 1)*float(visibilities[i])*np.cos(2*np.pi*A[0][i]*s/16))/2 for i in range(3)]) for z in range(8)] for s in range(16)])


def test_noninjective_zero_source_cannot_receive_the_positive_certificate():
    c=finite_control(((0,0,0,0,0),),4,1)
    assert not c["full_frequency_map_injective"]
    assert c["certified_information_lower_bits_exact"] is None
    assert c["raw_full_original_secret_information_bits"]==0
    assert c["pinched_residual_secret_X_information_bits"]==0


def test_uniform_prior_is_essential_and_real_readout_alias_remains():
    A,t,v=((1,2,4,8,16),),6,Fraction(1)
    # A prior concentrated on ONE secret carries zero information regardless of entropy bounds for a uniform prior.
    assert information(np.ones((1,1)))["uniform_secret_mutual_information_bits"]==0
    assert float(Fraction(finite_control(A,t,v)["certified_information_lower_bits_exact"]))>0
    c=native_frontier(64)
    assert c["uniform_original_and_residual_secret_priors_required"]
    assert not c["uniform_prior_bound_valid_for_arbitrary_adaptive_posteriors"]


def test_parity_only_clifford_compression_preserves_the_complete_X_information():
    A,t,m=((1,5,9,2),),5,4
    v=Fraction(7,8)
    C=measurement_channel(A,t,v,coarse_bits=1)
    for y in range(2):
        plan=coordinate_plan(A,t,(y,),coarse_bits=1)
        assert plan["higher_syndrome_constraints_not_measured_or_imposed"]
        assert plan["quadratic_high_syndrome_equations"]==[]
        k=plan["retained_quantum_wires"]
        xs=[lift_free_word(plan,u) for u in range(1 << k)]
        H=hadamard(1 << k)/np.sqrt(1 << k)
        V=[int(x,16) for x in plan["kernel_direction_hex"]]
        for s in range(16):
            rho=density(A,t,(s,),v)[np.ix_(xs,xs)]
            joint=np.diag(H@rho@H.T).real
            for z in range(1 << m):
                w=sum(((z&d).bit_count()%2) << j for j,d in enumerate(V))
                assert C["probabilities"][s,y,z]==pytest.approx(joint[w]/(1 << (m-k)),abs=1e-13)
    # No full-fiber enumeration is needed even with >2 million possible Hessian coefficients.
    A=[[int(i==j) for i in range(120)] for j in range(40)]
    plan=coordinate_plan(A,8,[0]*40,coarse_bits=1)
    assert plan["retained_quantum_wires"]==80
    assert plan["quadratic_high_syndrome_equations"]==[]


def test_mod2_and_mod4_bounds_are_distinct_physical_channels_not_interchangeable():
    A,t,v=((1,2,4,8,16),),6,Fraction(1)
    parity=finite_control(A,t,v,coarse_bits=1)
    two_bits=finite_control(A,t,v,coarse_bits=2)
    assert parity["all_residual_secrets_enumerated"]==2*two_bits["all_residual_secrets_enumerated"]
    assert Fraction(parity["certified_information_lower_bits_exact"])>Fraction(two_bits["certified_information_lower_bits_exact"])
    assert parity["charged_secret_coset_information_loss_bits"]<=1+1e-12
    assert two_bits["charged_secret_coset_information_loss_bits"]<=2+1e-12


def test_live_report_and_all_finite_controls_replay_without_claiming_a_decoder():
    r=build_report()
    assert json.loads(REPORT.read_text())==r
    assert len(r["finite_controls"])==9
    assert r["actual_positive_information_lower_bound_not_Holevo_only"]
    assert not r["full_secret_negation_alias_of_real_readout_removed"]
    assert not r["accepted_speedup_candidate"]
    assert not r["efficient_decoder_supplied"]
    assert not r["actual_natural_source_noise_certified"]
    assert r["any_secret_independent_correlated_Z_fault_distribution_with_marginal_visibility_lower_bound_covered"]
    for c in r["finite_controls"]:
        assert c["actual_pinching_vs_classical_secret_coset_average_residual"]<1e-12
        assert not c["likelihood_tables_are_polynomial_decoders"]


@pytest.mark.parametrize("call",[
    lambda:raw_information_rate_lower(Fraction(-1,2)),
    lambda:raw_information_rate_lower(1,terms=0),
    lambda:native_frontier(True),
    lambda:product_twirl_plan(((1,2),),4,(4,)),
    lambda:finite_control(((1,)*9,),4,1),
])
def test_invalid_sources_and_unpaid_tables_fail_closed(call):
    with pytest.raises(ValueError):
        call()
