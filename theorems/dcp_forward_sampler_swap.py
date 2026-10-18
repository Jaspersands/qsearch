"""Forward-only sampler/SWAP parity instrument, with its actual history kernel.

No native coherent sampler is supplied. A single full-word SWAP has a strong
independent-noise limitation even with unlimited sampler computation/history.
This is not a no-go for other measurements, selected subwords or clean sources.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import product
import json
from pathlib import Path
import sys

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))

from theorems.dcp_adaptive_direction_rank_gate import integer
from theorems.dcp_native_parity_observables import (
    _power_upper_exponent,measurement_operators,target_geometry,
)

REPORT=ROOT/"research/phase_workbench/dcp_forward_sampler_swap.json"
CONTRACT=ROOT/"research/hypotheses/dcp_forward_sampler_swap_contract.json"
CONTRACT_ID="forward_target_sampler_swap_parity_review_pending_v1"


def _finite_program(labels,bits,amplitudes):
    A,freq,target,distances=target_geometry(labels,bits)
    G=1 << (len(A)*bits)
    L=len(freq)
    if G>512:
        raise ValueError("UNKNOWN: finite coherent-sampler target-table cap")
    alpha=np.asarray(amplitudes,dtype=complex)
    if (alpha.ndim!=3 or alpha.shape[:2]!=(G,L) or not 1<=alpha.shape[2]<=64
            or alpha.size>100000 or L*L*alpha.shape[2]>100000
            or not np.isfinite(alpha).all()):
        raise ValueError("bounded normalized coherent target/witness/history array required")
    if np.max(abs(np.sum(abs(alpha)**2,axis=(1,2))-1))>1e-12:
        raise ValueError("every target-controlled preparation must be normalized, including invalid outputs")
    indices=[sum(a << (j*bits) for j,a in enumerate(f)) for f in freq]
    return A,freq,target,distances,indices,alpha


def sampler_observable(labels,bits,amplitudes):
    """Public reference pullback; no secret, inverse program or source reflection."""
    _,_,target,_,indices,alpha=_finite_program(labels,bits,amplitudes)
    vectors=np.array([alpha[f,x,:] for x,f in enumerate(indices)])
    O=(vectors@vectors.conj().T)*target
    if np.max(abs(np.linalg.eigvalsh(O)))>1+1e-11:
        raise ArithmeticError("forward SWAP pullback is not a contraction")
    return O


def swap_instrument(source_vector,labels,bits,amplitudes):
    """Actual forward-preparation, validity flag, controlled-SWAP and H readout."""
    _,_,valid,_,indices,alpha=_finite_program(labels,bits,amplitudes)
    psi=np.asarray(source_vector,dtype=complex)
    L=len(indices)
    if psi.shape!=(L,) or not np.isfinite(psi).all() or abs(np.vdot(psi,psi)-1)>1e-12:
        raise ValueError("normalized finite original input state required")
    # Compute target F(x)+h, apply its read-only-controlled preparation, then
    # uncompute the TARGET from unchanged x. Internal sampler history remains.
    state=np.array([psi[x]*alpha[f^(1 << (bits-1))] for x,f in enumerate(indices)])
    accepted=state*valid[:,:,None]
    rejected=state*(~valid)[:,:,None]
    # The valid relation is symmetric because h=-h. No favorable-branch restart.
    swapped=accepted.transpose(1,0,2)
    plus=float(np.sum(abs((accepted+swapped)/2)**2))
    minus=float(np.sum(abs((accepted-swapped)/2)**2))
    failure=float(np.sum(abs(rejected)**2))
    if abs(plus+minus+failure-1)>1e-11:
        raise ArithmeticError("SWAP instrument omitted probability mass")
    return {"plus":plus,"minus":minus,"failure":failure,
            "guess_even_probability":plus+failure/2,
            "guess_odd_probability":minus+failure/2}


def uniform_fiber_reference(labels,bits,*,history="clean",relative_phase=False):
    """PAID exponential reference, not a native sampler implementation."""
    _,freq,_,_=target_geometry(labels,bits)
    G=1 << (len(freq[0])*bits)
    L=len(freq)
    if G>512:
        raise ValueError("UNKNOWN: full fiber preparation table cap")
    if history not in ("clean","target","witness","seed") or type(relative_phase) is not bool:
        raise ValueError("explicit finite history and phase control required")
    H=1 if history=="clean" else G if history=="target" else L
    if G*L*H>100000:
        raise ValueError("UNKNOWN: exponential history table cap")
    groups={}
    for x,f in enumerate(freq):
        key=sum(a << (j*bits) for j,a in enumerate(f))
        groups.setdefault(key,[]).append(x)
    alpha=np.zeros((G,L,H),complex)
    for t in range(G):
        witnesses=groups.get(t,[0])
        for j,x in enumerate(witnesses):
            g=0 if history=="clean" else t if history=="target" else j if history=="seed" else x
            alpha[t,x,g]=(-1 if relative_phase and j%2 else 1)/np.sqrt(len(witnesses))
    return alpha


def erase_public_target_copy(amplitudes):
    """Known t->history XOR permutation, not a general garbage-erasure oracle."""
    alpha=np.asarray(amplitudes,dtype=complex)
    if alpha.ndim!=3 or alpha.shape[0]!=alpha.shape[2] or alpha.shape[0]&(alpha.shape[0]-1):
        raise ValueError("equal power-of-two target/history registers required")
    result=np.empty_like(alpha)
    for t in range(alpha.shape[0]):
        result[t]=alpha[t][:,np.arange(alpha.shape[2])^t]
    return result


def leading_mode_reference(labels,bits,visibility):
    """Exponential SVD preparation attaining the single-SWAP bound, not a solver."""
    alpha=uniform_fiber_reference(labels,bits)
    R=measurement_operators(labels,bits,visibility)
    groups={}
    for x,f in enumerate(R["frequencies"]):
        key=sum(a << (j*bits) for j,a in enumerate(f))
        groups.setdefault(key,[]).append(x)
    for f,left in sorted(groups.items()):
        partner=f^(1 << (bits-1))
        if partner not in groups or f>=partner:
            continue
        right=groups[partner]
        U,s,Vh=np.linalg.svd(R["kernel"][np.ix_(left,right)],full_matrices=False)
        if s[0]>1e-12:
            alpha[f,:,0]=0
            alpha[partner,:,0]=0
            alpha[f,left,0]=abs(U[:,0])
            alpha[partner,right,0]=abs(Vh[0,:])
    return alpha


def best_single_swap_advantage(labels,bits,visibility):
    R=measurement_operators(labels,bits,visibility)
    return sum(max(b["singular_values"],default=0) for b in R["weighted_frequency_pair_blocks"])/len(R["frequencies"])


def native_swap_frontier(n,bits,copies,*,visibility=None):
    integer(n,"native components",2,256)
    integer(bits,"original phase bits",3,512)
    integer(copies,"original full-word phase samples",1,200000)
    v=Fraction(n-1,n) if visibility is None else Fraction(visibility)
    if not 0<=v<=1:
        raise ValueError("independent original Z visibility outside[0,1]")
    if copies*max((1+v*v).numerator.bit_length(),(1+v*v).denominator.bit_length())>2000000:
        raise ValueError("UNKNOWN: exact single-SWAP arithmetic cap")
    squared=(((1+v*v)/2)**copies-Fraction(1,1 << copies))/4
    e=_power_upper_exponent(squared.numerator,squared.denominator)
    return {"native_components":n,"original_phase_bits":bits,"full_word_original_samples":copies,
            "independent_original_Z_visibility_exact":str(v),
            "source_average_SUP_over_all_sampler_advantage_squared_upper_formula":"(((1+v^2)/2)^K-2^-K)/4",
            "source_average_SUP_advantage_power_of_two_upper_exponent":None if e is None else e//2,
            "advantage_exactly_zero":squared==0,
            "sampler_may_depend_on_all_public_labels_and_visibility":True,
            "arbitrary_computation_history_and_exact_coherent_preparation_allowed_in_this_bound":True,
            "sampler_is_controlled_only_by_full_target_not_original_word":True,
            "single_full_word_SWAP_plus_validity_and_fair_failure_guess_only":True,
            "general_quantum_receiver_or_selected_subword_no_go":False,
            "correlated_marginal_noise_models_covered":False,
            "clean_sampler_or_efficient_native_sampler_implemented":False}


def physical_control(labels,bits,visibility,*,history="clean",relative_phase=False):
    alpha=uniform_fiber_reference(labels,bits,history=history,relative_phase=relative_phase)
    A,freq,target,distances,_,alpha=_finite_program(labels,bits,alpha)
    G,L=alpha.shape[:2]
    if G*L**3*alpha.shape[2]>2000000:
        raise ValueError("UNKNOWN: actual original-error-mixture replay cap")
    v=Fraction(visibility)
    if not 0<=v<=1:
        raise ValueError("independent original Z visibility outside[0,1]")
    O=sampler_observable(A,bits,alpha)
    kernel=target*np.array([[float(v**w) for w in row] for row in distances])
    predicted=.5+float(np.trace(O@kernel).real)/(2*L)
    p=(1-v)/2
    success=[]
    failures=[]
    for s in product(range(1 << bits),repeat=len(A)):
        phases=np.array([np.exp(2j*np.pi*sum(a*b for a,b in zip(f,s))/(1 << bits))/np.sqrt(L) for f in freq])
        correct=failure=0.0
        for error in range(L):
            w=error.bit_count()
            weight=p**w*(1-p)**(len(A[0])-w)
            if not weight:
                continue
            state=phases*np.array([(-1)**((error&x).bit_count()) for x in range(L)])
            receipt=swap_instrument(state,A,bits,alpha)
            correct+=float(weight)*receipt["guess_even_probability" if s[0]%2==0 else "guess_odd_probability"]
            failure+=float(weight)*receipt["failure"]
        success.append(correct)
        failures.append(failure)
    if max(abs(z-predicted) for z in success)>1e-11:
        raise ArithmeticError("actual forward/SWAP Born law disagrees with history kernel")
    bound=best_single_swap_advantage(A,bits,v)
    if predicted-.5>bound+1e-11:
        raise ArithmeticError("one-SWAP sampler exceeds frequency-block spectral norm bound")
    return {"full_labels":[list(row) for row in A],"phase_bits":bits,
            "original_phase_qubits":len(A[0]),"history_mode":history,"alternating_fiber_amplitude_phase":relative_phase,
            "independent_original_Z_visibility_exact":str(v),
            "actual_fixed_secret_success_min":float(min(success)),"actual_fixed_secret_success_max":float(max(success)),
            "history_kernel_predicted_success":predicted,"charged_failure_probability_max":float(max(failures)),
            "best_one_SWAP_over_arbitrary_target_preparations_success_upper":.5+bound,
            "best_arbitrary_quantum_measurement_success":.5+measurement_operators(A,bits,v)["reference_optimal_advantage"],
            "target_witness_history_table_entries_allocated":int(alpha.size),
            "forward_sampler_calls_per_attempt":1,"sampler_inverse_calls":0,
            "controlled_word_SWAP_gates_per_attempt":len(A[0]),"readout_H_gates":2,
            "target_and_validity_arithmetic_must_be_paid":True,
            "native_scalable_sampler_or_speedup_supplied":False}


def build_report():
    redundant=((1,2,4,0),)
    return {"schema_version":1,"contract_id":CONTRACT_ID,
            "status":"FORWARD_SAMPLER_SWAP_CONDITIONAL_CLEAN_ROUTE_NOISY_TEMPLATE_FALSIFIED",
            "native_noise_frontiers":[native_swap_frontier(n,n+8,2*n*(n+8)) for n in (8,32,64,128)],
            "clean_native_countercontrol":native_swap_frontier(64,72,9216,visibility=1),
            "conditional_clean_uniform_sampler_frontiers":[{
                "components":n,"phase_bits":n+8,"original_phase_qubits":n*(n+8)+delta,
                "copy_density_overhead_bits":delta,
                "native_average_parity_success_lower_IF_clean_aligned_uniform_sampler":str(1-Fraction(1,1 << (1+delta//2))),
                "sampler_must_work_coherently_on_every_nonempty_full_target":True,
                "missing_sampler_time_and_workspace_must_be_polynomial":True,
                "inverse_sampler_required":False,"actual_native_sampler_supplied":False}
                for n,delta in ((8,4),(32,4),(64,4),(128,4),(64,16))],
            "physical_controls":[physical_control(A,t,v,history=h,relative_phase=phase) for A,t,v,h,phase in (
                (redundant,3,Fraction(1),"clean",False),
                (redundant,3,Fraction(1),"target",False),
                (redundant,3,Fraction(1),"witness",False),
                (redundant,3,Fraction(1),"seed",False),
                (redundant,3,Fraction(1),"clean",True),
                (redundant,3,Fraction(3,4),"clean",False),
                (((2,2,2,2),),3,Fraction(3,4),"clean",False),
                (((2,2,2,2),),3,Fraction(0),"clean",False))],
            "clean_rank_one_vs_noisy_multiple_singular_modes_is_distinct":True,
            "classical_output_probabilities_determine_this_receiver":False,
            "known_polynomial_coherent_native_sampler_implemented":False,
            "accepted_speedup_candidate":False,"new_active_negative_result_created":False,"novelty_claim":False}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write",action="store_true")
    args=parser.parse_args()
    report=build_report()
    if args.write:
        REPORT.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"status":report["status"],"physical_controls":len(report["physical_controls"]),
                      "native_frontiers":len(report["native_noise_frontiers"]),"native_sampler":False}))


if __name__=="__main__":
    main()
