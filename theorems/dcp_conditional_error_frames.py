"""Conditional full-frequency error frames and a costed information-only escape.

Existence of a correcting frame transform is not an efficient decoder. Native
frontiers are analytical; only bounded known matrices are physically replayed.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from itertools import product
import json
from math import comb
from pathlib import Path
import sys

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))

from theorems.dcp_adaptive_direction_rank_gate import integer
from theorems.dcp_affine_fiber_rigidity import matrix
from theorems.dcp_native_parity_observables import _power_upper_exponent
from theorems.dcp_nonlinear_fiber_pairing import phase_value

REPORT=ROOT/"research/phase_workbench/dcp_conditional_error_frames.json"
CONTRACT=ROOT/"research/hypotheses/dcp_conditional_error_frames_contract.json"
CONTRACT_ID="native_conditional_multimode_error_frames_review_pending_v1"


def finite_frames(labels,bits,error_masks):
    A=matrix(labels)
    integer(bits,"finite full phase bits",2,16)
    n,K=len(A),len(A[0])
    errors=tuple(error_masks)
    if (K>9 or n>3 or not errors or len(set(errors))!=len(errors)
            or len(errors)>32 or (1 << K)*len(errors)**2>1000000
            or any(a>=1 << bits for row in A for a in row)):
        raise ValueError("UNKNOWN: canonical bounded full-frequency error frame required")
    for e in errors:
        integer(e,"distinct original Z-error mask",0,(1 << K)-1)
    groups={}
    frequencies=[phase_value(A,x,1 << bits) for x in range(1 << K)]
    for x,f in enumerate(frequencies):
        groups.setdefault(f,[]).append(x)
    rows=[]
    for f,words in sorted(groups.items()):
        d=len(words)
        signed=[[sum((-1)**(((e^other)&x).bit_count()) for x in words) for other in errors] for e in errors]
        eta=sum((Fraction(signed[i][j],d)**2 for i in range(len(errors)) for j in range(len(errors)) if i!=j),Fraction(0))
        rows.append({"frequency":f,"words":words,"signed_Gram_numerators":signed,
                     "Gram_denominator":d,"Gram_error_Frobenius_squared":eta})
    return A,errors,frequencies,rows


def born_gram_bound(group_size,original_words,error_count):
    integer(group_size,"full frequency group size",2)
    integer(original_words,"Boolean source word count",2)
    integer(error_count,"fixed label-independent error-frame size",1,original_words)
    return Fraction(4*error_count*(error_count-1)*(group_size-1),original_words)


def dense_frame_transforms(labels,bits,error_masks):
    """PAID controlled unitary reference, generated only from public A and E."""
    A,errors,frequencies,rows=finite_frames(labels,bits,error_masks)
    L=1 << len(A[0])
    if L>128 or L*L*len(rows)>1000000:
        raise ValueError("UNKNOWN: exponential controlled-unitary reference cap")
    transforms={}
    diagnostic=[]
    for row in rows:
        f=row["frequency"]
        eta=row["Gram_error_Frobenius_squared"]
        good=eta<1
        U=np.eye(L)
        error=0.0
        if good:
            Phi=np.zeros((L,len(errors)))
            for x in row["words"]:
                Phi[x]=[(-1)**((e&x).bit_count())/np.sqrt(len(row["words"])) for e in errors]
            left,s,right=np.linalg.svd(Phi,full_matrices=False)
            if min(s)<1e-10:
                raise ArithmeticError("exact Gram gate promises full column rank; numerical control failed")
            W=left@right
            Q,_=np.linalg.qr(W,mode="complete")
            domain=np.column_stack((W,Q[:,len(errors):]))
            output_order=list(errors)+[x for x in range(L) if x not in errors]
            U=np.eye(L)[:,output_order]@domain.T
            error=float(np.linalg.norm(U@Phi-np.eye(L)[:,list(errors)])**2)
            if error>float(eta)+1e-10:
                raise ArithmeticError("polar error-frame transport violates its exact Gram bound")
        if np.max(abs(U@U.T-np.eye(L)))>1e-10:
            raise ArithmeticError("conditional error-frame transform is not unitary")
        transforms[f]=U
        diagnostic.append({"frequency":list(f),"fiber_size":len(row["words"]),
                           "exact_Gram_error_squared":str(eta),"good_frame_exact_gate":good,
                           "numerical_total_frame_transport_squared_error":error,
                           "unitary_identity_on_bad_frames":not good})
    return A,errors,frequencies,rows,transforms,diagnostic


def physical_control(labels,bits,error_masks):
    A,errors,frequencies,rows,transforms,diag=dense_frame_transforms(labels,bits,error_masks)
    n,K=len(A),len(A[0])
    L,G=1 << K,1 << (n*bits)
    if G>128 or G*L*len(errors)>100000:
        raise ValueError("UNKNOWN: full source/error readout calibration cap")
    count=Counter(frequencies)
    ideal=.5+sum(np.sqrt(c*count.get(((f[0]+(1 << (bits-1)))%(1 << bits),)+f[1:],0))/L for f,c in count.items())/2
    eta=sum((Fraction(row["Gram_denominator"],L)*row["Gram_error_Frobenius_squared"] for row in rows),Fraction(0))
    successes=[]
    max_state_error=0.0
    for s in product(range(1 << bits),repeat=n):
        for e in errors:
            state=np.zeros((L,G),complex)
            reference=np.zeros_like(state)
            for row in rows:
                f=row["frequency"]
                key=sum(a << (j*bits) for j,a in enumerate(f))
                phase=np.exp(2j*np.pi*sum(a*b for a,b in zip(f,s))/(1 << bits))
                for x in row["words"]:
                    state[x,key]=phase*(-1)**((e&x).bit_count())/np.sqrt(L)
                state[:,key]=transforms[f]@state[:,key]
                reference[e,key]=phase*np.sqrt(len(row["words"])/L)
            if abs(np.vdot(state,state)-1)>1e-10:
                raise ArithmeticError("controlled frame circuit lost source probability")
            distance=float(np.linalg.norm(state-reference)**2)
            max_state_error=max(max_state_error,distance)
            if distance>5*float(eta)+1e-10:
                raise ArithmeticError("source-weighted frame transport exceeds good/bad-frame bound")
            expectation=np.vdot(state,state[:,np.arange(G)^(1 << (bits-1))]).real
            successes.append(.5+(1-2*(s[0]&1))*expectation/2)
    lower=max(0,ideal-np.sqrt(5*float(eta)))
    if min(successes)<lower-1e-10:
        raise ArithmeticError("actual multimode parity measurement violates state-distance bound")
    return {"full_labels":[list(row) for row in A],"phase_bits":bits,"original_phase_qubits":K,
            "fixed_original_error_masks":list(errors),"conditioned_on_error_set_not_full_noise_law":True,
            "Born_weighted_Gram_error_squared_exact":str(eta),"fiber_frames":diag,
            "ideal_clean_parity_success":float(ideal),"actual_success_min":float(min(successes)),
            "actual_success_max":float(max(successes)),"state_distance_success_lower":float(lower),
            "max_original_error_state_transport_squared_error":max_state_error,
            "dense_controlled_matrix_entries_allocated":len(transforms)*L*L,
            "numerical_circuit_replay_tolerance":1e-10,
            "finite_float_replay_is_an_exact_algebraic_certificate":False,
            "uniform_polynomial_transform_implemented":False,
            "source_or_error_set_selected_after_inspecting_secret":False}


def parity_harmless_alias_control():
    A=((1,1,1,1),)
    _,_,freq,rows=finite_frames(A,2,(0,15))
    L=16
    counts=Counter(freq)
    O=np.array([[float(f[0]-g[0])%4==2 for g in freq] for f in freq],dtype=float)
    for x,f in enumerate(freq):
        for y,g in enumerate(freq):
            if O[x,y]:
                O[x,y]/=np.sqrt(counts[f]*counts[g])
    success=[]
    alias_residual=0.0
    for s in range(4):
        psi=np.exp(2j*np.pi*np.array([f[0] for f in freq])*s/4)/4
        zpsi=psi*np.array([(-1)**x.bit_count() for x in range(L)])
        shifted=np.exp(2j*np.pi*np.array([f[0] for f in freq])*((s+2)%4)/4)/4
        alias_residual=max(alias_residual,float(np.max(abs(zpsi-shifted))))
        success.extend([float(.5+(1-2*(s%2))*np.vdot(state,O@state).real/2) for state in (psi,zpsi)])
    if alias_residual>1e-11 or np.ptp(success)>1e-11:
        raise ArithmeticError("binary-rowspace error does not preserve the target parity law")
    return {"full_labels":[list(row) for row in A],"phase_bits":2,
            "binary_rowspace_alias_error":15,"induced_secret_shift":2,
            "first_secret_parity_changed":False,"known_dense_clean_readout_success":float(min(success)),
            "max_exact_phase_identity_numerical_residual":alias_residual,
            "Gram_near_identity_is_necessary_for_parity_recovery":False,
            "label_adaptive_error_masks_may_use_fixed_difference_average_bound":False}


def native_frontier(n):
    integer(n,"native components",2,256)
    t=n+8
    N=n*t
    K=2*N
    w=2*t
    M=sum(comb(K,j) for j in range(w+1))
    padded_mode_bits=(M-1).bit_length()
    ratio=Fraction((1 << N)-1,1 << K)
    frame=20*M*(M-1)*ratio
    tail=Fraction(11,16)**t  # e<11/4 in the standard threshold-2mu Chernoff bound.
    if frame>=1:
        failure=Fraction(1)
        norm_exponent=None
    else:
        clean_e=_power_upper_exponent(ratio.numerator,ratio.denominator)//2
        norm_exponent=_power_upper_exponent(frame.numerator,frame.denominator)//2
        failure=min(Fraction(1),Fraction(1,1 << (clean_e+1))+Fraction(1,1 << norm_exponent)+tail)
    exponent=_power_upper_exponent(failure.numerator,failure.denominator)
    return {"components":n,"phase_bits":t,"original_samples":K,
            "original_word_and_frequency_register_qubits":K+N,
            "original_independent_Z_probability_exact":str(Fraction(1,2*n)),
            "expected_original_Z_errors_exact":str(Fraction(K,2*n)),
            "fixed_typical_error_weight_cutoff":w,"typical_error_pattern_count_hex":hex(M),
            "typical_error_pattern_count_binary_bits":M.bit_length(),
            "generic_uniform_mode_erasure_projection_probability_power_of_two_exponent":padded_mode_bits,
            "generic_mode_erasure_amplification_characteristic_exponent_half":padded_mode_bits,
            "generic_projection_is_a_lower_bound_on_all_structured_transforms":False,
            "source_average_transport_state_distance_upper_power_of_two_exponent":norm_exponent,
            "noise_tail_upper_formula":"(11/16)^t; threshold2t with mean t",
            "source_average_parity_failure_upper_power_of_two_exponent_IF_arbitrary_frame_unitary":exponent,
            "information_only_uniform_per_fixed_secret_source_average":True,
            "uniform_poly_time_or_space_frame_unitary_implemented":False,
            "dense_frame_enumeration_and_synthesis_is_polynomial":False,
            "exponential_classical_reference_memory_implies_exponential_quantum_width":False,
            "approximate_orthogonality_is_an_efficient_syndrome_decoder":False,
            "frame_source_bound_allows_label_adaptive_error_sets":False,
            "natural_source_or_correlated_noise_transfer_certified":False}


def build_report():
    return {"schema_version":1,"contract_id":CONTRACT_ID,
            "status":"INFORMATION_ONLY_MULTIMODE_ESCAPE_EFFICIENT_FRAME_TRANSPORT_OPEN",
            "native_frontiers":[native_frontier(n) for n in (8,16,32,64,128)],
            "physical_controls":[physical_control(A,t,E) for A,t,E in (
                (((1,2,0,0),),2,(0,4,8)),
                (((1,2,3,1,0,2),),2,(0,1,2)),
                (((1,1,1,1,1,1),),2,(0,1)),
                (((1,1,1,1),),2,(0,15)))],
            "parity_harmless_rowspace_alias_control":parity_harmless_alias_control(),
            "signed_occupancy_fixed_difference_moment":"E_A sum_f B_f(d)^2 = 2^K*(1-1/q^n), for fixed d!=0 independent of A",
            "Born_normalized_frame_bound":"E_A sum_f (d_f/2^K)*||Gram_f-I||_F^2 <=4*M*(M-1)*(q^n-1)/2^K",
            "binary_rowspace_alias_is_a_parity_harmless_control_not_general_noise_failure":True,
            "accepted_speedup_candidate":False,"new_active_negative_result_created":False,"novelty_claim":False}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write",action="store_true")
    args=parser.parse_args()
    report=build_report()
    if args.write:
        REPORT.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"status":report["status"],"native_frontiers":len(report["native_frontiers"]),
                      "physical_controls":len(report["physical_controls"]),"efficient_transform":False}))


if __name__=="__main__":
    main()
