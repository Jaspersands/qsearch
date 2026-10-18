"""Bounded full-outcome block readout, low-degree blindness and twirl baseline.

Likelihood enumeration is exponential and uses a known secret only for
calibration. No efficient inference, classical DCP simulation or speedup.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import combinations, product
import json
from pathlib import Path
from random import Random

import numpy as np
from scipy.linalg import hadamard

from theorems.dcp_adaptive_direction_rank_gate import integer
from theorems.dcp_affine_fiber_rigidity import matrix
from theorems.dcp_correlated_phase_block import native_information_frontier
from theorems.dcp_nonlinear_fiber_pairing import phase_value

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"research/phase_workbench/dcp_correlated_block_observables.json"
CONTRACT=ROOT/"research/hypotheses/dcp_correlated_block_observables_contract.json"


def measurement_channel(labels,phase_bits,visibility,*,coarse_bits=2,axes_mask=0,T_feedback_by_syndrome=None):
    """Full selected readout law; native theorem helpers below remain MOD4."""
    A=matrix(labels)
    n,m=len(A),len(A[0])
    integer(phase_bits,"finite phase bits",3,16)
    integer(coarse_bits,"coarse syndrome bits per component",1,2)
    v=Fraction(visibility)
    if not 0<=v<=1 or any(a>=1 << phase_bits for row in A for a in row):
        raise ValueError("canonical labels and visibility in[0,1] required")
    coarse=1 << coarse_bits
    M,Y,q=1 << m,coarse**n,1 << phase_bits
    residual=q//coarse
    K=residual**n
    if m>8 or K>64 or K*Y*M>150000:
        raise ValueError("UNKNOWN: exponential complete likelihood-table work cap")
    integer(axes_mask,"public Y-axis mask",0,M-1)
    H=hadamard(M).astype(float)
    feedback_phase=np.ones((Y,M),dtype=complex)
    if T_feedback_by_syndrome is not None:
        if len(T_feedback_by_syndrome)!=Y or any(len(row)!=m for row in T_feedback_by_syndrome):
            raise ValueError("one public T-grid phase coefficient per syndrome and input wire required")
        for y,row in enumerate(T_feedback_by_syndrome):
            for value in row:
                integer(value,"public T-grid coefficient",0,7)
            feedback_phase[y]=np.exp(1j*np.pi*np.array([sum(b*(x >> i & 1) for i,b in enumerate(row))%8 for x in range(M)])/4)
    frequencies=np.array([phase_value(A,x,q) for x in range(M)],dtype=np.int64)
    groups=[[] for _ in range(Y)]
    for x,values in enumerate(frequencies):
        groups[sum((int(a)%coarse) << (coarse_bits*l) for l,a in enumerate(values))].append(x)
    noise_eigenvalues=np.array([float(v**u.bit_count()) for u in range(M)])
    secrets=list(product(range(residual),repeat=n))
    axes_phase=np.array([(-1j)**((axes_mask&x).bit_count()%4) for x in range(M)])
    channel=np.zeros((K,Y,M))
    min_probability=1.0
    for i,secret in enumerate(secrets):
        phase=np.exp(2j*np.pi*((frequencies@np.array(secret))%q)/q)*axes_phase
        clean=np.zeros((Y,M))
        for y,indices in enumerate(groups):
            if indices:
                amplitudes=H[:,indices]@(phase[indices]*feedback_phase[y,indices])/M
                clean[y]=np.abs(amplitudes)**2
        # Original Z errors commute with the syndrome projector. H readout
        # turns them into independent bit flips; Walsh eigenvalues are v^|u|.
        noisy=((clean@H)*noise_eigenvalues)@H/M
        min_probability=min(min_probability,float(noisy.min()))
        if noisy.min() < -1e-11:
            raise ArithmeticError("BSC channel lost positivity")
        noisy=np.maximum(noisy,0)
        if abs(noisy.sum()-1)>1e-10:
            raise ArithmeticError("unconditional readout mass was lost")
        channel[i]=noisy
    masses=np.array([len(g)/M for g in groups])
    if np.max(np.abs(channel.sum(axis=2)-masses))>1e-10:
        raise ArithmeticError("syndrome law depends on secret or drops an outcome")
    return {"probabilities":channel,"secrets":secrets,"fibers":groups,"Walsh_matrix":H,
            "syndrome_probabilities":masses,"minimum_probability_before_roundoff_clamp":min_probability,
            "secret_hypotheses_enumerated":K,"basis_addresses_enumerated":M,
            "full_likelihood_entries":K*Y*M,"public_Y_axis_mask":axes_mask,
            "coarse_syndrome_bits_per_component":coarse_bits,
            "residual_secret_modulus":residual}


def information(probabilities):
    probabilities=np.asarray(probabilities,dtype=float)
    if probabilities.ndim<2 or probabilities.shape[0]<1 or not np.all(np.isfinite(probabilities)) or np.any(probabilities<0):
        raise ValueError("finite nonnegative conditional probability table required")
    K=probabilities.shape[0]
    if np.max(np.abs(probabilities.reshape(K,-1).sum(axis=1)-1))>1e-10:
        raise ValueError("unconditional Born mass must be one for each secret")
    average=probabilities.mean(axis=0)
    ratio=np.divide(probabilities,average,out=np.ones_like(probabilities),where=average>0)
    active=probabilities>0
    mutual=float(np.sum(probabilities[active]*np.log2(ratio[active]))/K)
    bayes=float(probabilities.max(axis=0).sum()/K)
    return {"uniform_secret_mutual_information_bits":mutual,"optimal_one_copy_Bayes_guess_probability":bayes,
            "secret_hypotheses_enumerated":K,"likelihood_evaluation_is_free_or_polynomial":False}


def product_twirl_distribution(labels,phase_bits,secret,visibility):
    A=matrix(labels)
    n,m=len(A),len(A[0])
    integer(phase_bits,"finite phase bits",3,16)
    if m>8 or 4**n*(1 << m)>65536:
        raise ValueError("UNKNOWN: product-measurement twirl calibration cap")
    if len(secret)!=n or any(a>=1 << phase_bits for row in A for a in row):
        raise ValueError("secret dimension/full labels mismatch")
    v=Fraction(visibility)
    if not 0<=v<=1:
        raise ValueError("visibility outside[0,1]")
    for s in secret:
        integer(s,"finite canonical calibration secret",0,(1 << phase_bits)-1)
    q=1 << phase_bits
    source_angles=np.array([2*np.pi*(sum(secret[l]*A[l][i] for l in range(n))%q)/q for i in range(m)])
    signs=np.array([[1-2*(z >> i & 1) for i in range(m)] for z in range(1 << m)])
    result=np.zeros(1 << m)
    for dual in product(range(4),repeat=n):
        angles=source_angles+np.array([np.pi*(sum(dual[l]*A[l][i] for l in range(n))%4)/2 for i in range(m)])
        means=float(v)*np.cos(angles)
        result+=np.prod((1+signs*means)/2,axis=1)/4**n
    return result


def minimum_signed_relation(labels):
    A=matrix(labels)
    n,m=len(A),len(A[0])
    if m>8:
        raise ValueError("UNKNOWN: exhaustive signed-relation diagnostic cap")
    tested=0
    for w in range(1,m+1):
        for support in combinations(range(m),w):
            for tail in product((-1,1),repeat=w-1):
                signs=(1,)+tail  # Quotient the redundant overall sign.
                tested+=1
                if all(sum(row[i]*s for i,s in zip(support,signs))%4==0 for row in A):
                    vector=[0]*m
                    for i,s in zip(support,signs):
                        vector[i]=s
                    return {"minimum_nonzero_signed_support":w,"witness":vector,
                            "signed_relations_tested":tested,"diagnostic_search_is_polynomial":False}
    return {"minimum_nonzero_signed_support":None,"witness":None,
            "signed_relations_tested":tested,"diagnostic_search_is_polynomial":False}


def analyze(labels,phase_bits,visibility):
    A=matrix(labels)
    C=measurement_channel(A,phase_bits,visibility)
    P,H=C["probabilities"],C["Walsh_matrix"]
    relation=minimum_signed_relation(A)
    d=relation["minimum_nonzero_signed_support"]
    m=len(A[0])
    blind=m if d is None else d-1
    biases=(P@H)
    masses=C["syndrome_probabilities"]
    conditional=np.divide(biases,masses[:,None],out=np.zeros_like(biases),where=masses[:,None]>0)
    low=[u for u in range(1,1 << m) if u.bit_count()<=blind]
    low_residual=float(np.max(np.abs(conditional[:,:,low]))) if low else 0.0
    if low_residual>1e-10:
        raise ArithmeticError("short-relation-free block has a low-degree X bias")
    residual=0.0
    for i,secret in enumerate(C["secrets"]):
        baseline=product_twirl_distribution(A,phase_bits,secret,visibility)
        residual=max(residual,float(np.max(np.abs(P[i].sum(axis=0)-baseline))))
    if residual>1e-10:
        raise ArithmeticError("discarded-syndrome channel differs from product-measurement twirl")
    return {"full_labels":[list(row) for row in A],"phase_bits":phase_bits,"visibility_exact":str(Fraction(visibility)),
            "residual_secret_modulus":1 << (phase_bits-2),
            "source_secret_known_only_for_likelihood_calibration":True,
            "joint_syndrome_and_X_information":information(P),
            "discarded_syndrome_X_information":information(P.sum(axis=1)),
            "product_measurement_twirl_max_probability_residual":residual,
            "twirl_reproduces_joint_syndrome_and_X":False,
            "twirl_requires_single_qubit_source_measurement_access":True,
            "classical_unknown_secret_DCP_simulation_supplied":False,
            "minimum_signed_relation_diagnostic":relation,
            "all_X_outcomes_k_wise_uniform_conditional_on_syndrome":blind,
            "max_nonconstant_parity_bias_through_blind_degree":low_residual,
            "full_likelihood_entries_enumerated":C["full_likelihood_entries"],
            "basis_addresses_enumerated":C["basis_addresses_enumerated"],
            "syndrome_probabilities":[float(p) for p in masses],
            "minimum_probability_before_roundoff_clamp":C["minimum_probability_before_roundoff_clamp"],
            "full_X_outcome_retained_not_independent_marginal_samples":True,
            "efficient_decoder_or_quantum_advantage_claimed":False}


def native_blindness_frontier(n):
    positive=native_information_frontier(n)
    k=n//4
    # (1+2/32)^(4n)*32^k, and (17/16)^8<2, give this
    # integer Chernoff bound without a floating entropy exponent.
    exception=2*n-(n+1)//2-5*k
    return {"components":n,"original_phase_qubits":4*n,"blind_local_support_or_X_parity_degree":k,
            "any_signed_relation_through_degree_k_probability_power_of_two_upper_exponent":exception,
            "simultaneous_local_blindness_and_Holevo_event_exception_power_of_two_upper_exponent":max(0,min(exception,n*n)-1),
            "all_k_local_reduced_states_secret_independent_IF_no_short_relation":True,
            "full_X_readout_k_wise_uniform_IF_no_short_relation":True,
            "joint_high_degree_X_correlations_excluded":False,
            "local_measurement_circuits_or_full_output_decoders_ruled_out":False,
            "retained_Holevo_lower_bits_IF_full_injective":positive["retained_block_Holevo_bits_lower_IF_injective"],
            "efficient_readout_or_decoder_supplied":False}


def native_collision_moment(n,m,visibility,*,phase_bits=4,secret_has_odd_component=True):
    integer(n,"finite collision components",1,1024)
    integer(m,"finite collision batch width",1,4096)
    integer(phase_bits,"input phase bits",4,4096)
    if secret_has_odd_component is not True:
        raise ValueError("UNKNOWN: primitive residual secret required; even-secret class has different moments")
    v=Fraction(visibility)
    if not 0<=v<=1:
        raise ValueError("visibility outside[0,1]")
    M,G=1 << m,4**n
    B=(1+v*v)**m
    C=(2+v*v)**m
    # G*M times the native mean sum_(y,z) P(y,z|s)^2. The four
    # addresses must have both XOR sum zero and zero integer parallelogram.
    return (Fraction(G,M)+(M+B-2)/M+(C-M-B+1)/(G*M))


def native_collision_census():
    # All4096 original q16 label triples, not selected low-label matrices.
    m,q=3,16
    X=np.array([[x >> i & 1 for i in range(m)] for x in range(8)])
    A=np.array(list(product(range(q),repeat=m)))
    frequencies=(A@X.T)%q
    H=hadamard(8).astype(float)
    rows=[]
    for secret in (1,2):
        phase=np.exp(2j*np.pi*secret*frequencies/q)
        marked=np.stack([np.where(frequencies%4==y,phase,0) for y in range(4)],axis=1)
        clean=np.abs(marked@H/8)**2
        for v in (Fraction(1),Fraction(1,2),Fraction(0)):
            noisy=((clean@H)*np.array([float(v**u.bit_count()) for u in range(8)]))@H/8
            observed=float(np.mean(32*np.sum(noisy*noisy,axis=(1,2))))
            expected=native_collision_moment(1,3,v) if secret%2 else None
            if expected is not None and abs(observed-float(expected))>1e-10:
                raise ArithmeticError("complete native Born census falsified collision formula")
            rows.append({"components":1,"width":3,"phase_bits":4,"fixed_residual_secret":secret,
                         "visibility_exact":str(v),"all_original_label_matrices":4096,
                         "native_mean_uniform_reference_collision_multiplier":observed,
                         "primitive_secret_formula_exact_rational":str(expected) if expected is not None else None,
                         "even_secret_exception_in_formula":secret%2==0})
    return rows


def native_readout_information_frontier(n):
    integer(n,"native information components",16,1 << 20)
    t=n+8
    # Primitive secrets: kappa<=2+2^-n+(27/32)^n, (27/32)^5<1/2.
    # All-even secrets have original prior mass2^-n and KL<=5n.
    h=min(n//5-1,n-(5*n-1).bit_length())-1
    if h<0:
        raise ArithmeticError("information frontier needs a nonnegative correction exponent")
    entropy=n*(t-2)
    # Real syndrome/X circuits alias s and -s. Fano is applied to their
    # negation orbit under the original uniform-secret prior: H(orbit)>=H-1.
    numerator=(3*entropy-8)*(1 << h)
    denominator=4*((1 << h)+1)
    attempts=(numerator+denominator-1)//denominator
    e=(n-1).bit_length()
    return {"components":n,"original_phase_qubits_per_batch":3*n,"original_phase_bits":t,
            "residual_secret_entropy_bits":entropy,
            "mean_information_bits_per_fixed_readout_batch_upper":{"integer_part":1,"dyadic_correction_exponent":h},
            "all_even_secret_prior_probability_exponent":n,
            "all_even_secret_KL_bits_upper":5*n,
            "full_secret_identification_ceiling":{"half_plus_two_to_negative_exponent":entropy-n+1},
            "three_quarter_full_secret_identification_target_attainable":False,
            "Fano_target":"negation orbit under original uniform-secret prior",
            "three_quarter_negation_orbit_identification_attempt_lower_bound":attempts,
            "raw_original_qubits_lower_bound_for_that_orbit_target":3*n*attempts,
            "retained_block_Holevo_lower_bits_IF_full_injective":max(0,n-(3*(e+3)+1)//2),
            "full_frequency_noninjectivity_probability_upper_exponent":n*n+2*n,
            "information_upper_is_native_mean_not_pointwise_in_A":True,
            "only_unrotated_syndrome_then_complete_X_readout_covered":True,
            "adaptively_secret_aligned_bases_or_other_collective_measurements_covered":False,
            "source_preparation_or_decoder_implemented":False,
            "polynomial_sample_lower_bound_is_a_general_algorithmic_no_go":False}


def build_report():
    rng=Random(101518)
    native=[[rng.randrange(16) for _ in range(6)] for _ in range(2)]
    return {"contract_id":"correlated_block_joint_readout_local_blindness_twirl_baseline_v1",
            "status":"BOUNDED_FULL_OUTCOME_CALIBRATION_AND_LOCAL_DERIVATION_REVIEW_PENDING",
            "finite_controls":[analyze(A,t,v) for A,t,v in (
                (((1,0,5,1),(0,1,1,2)),4,Fraction(7,8)),
                (((1,4,0,0),(0,0,1,4)),3,Fraction(7,8)),
                (native,4,Fraction(1,2)))],
            "native_joint_information_blindness_frontiers":[native_blindness_frontier(n) for n in (64,256,1024,4096,16384,65536)],
            "complete_native_collision_censuses":native_collision_census(),
            "native_fixed_readout_information_frontiers":[native_readout_information_frontier(n) for n in (64,256,1024,4096,16384,65536)],
            "selected_controls_are_native_advantage_estimates":False,
            "accepted_speedup_candidate":False,"novelty_claim":False,
            "source_quantum_preparations_executed":0,"exponential_fiber_and_secret_enumeration_charged":True,
            "efficient_unknown_secret_inference_implemented":False,
            "prior_source_and_gate_contract":"research/DCP_PAIRING_COMPOSITION_BARRIER.md#6-physical-retained-block-escape"}


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-write",action="store_true")
    args=parser.parse_args(argv)
    report=build_report()
    if not args.no_write:
        REPORT.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"status":report["status"],"finite_controls":3,"native_frontiers":6,
                      "efficient_decoder":False,"artifact":str(REPORT)}))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
