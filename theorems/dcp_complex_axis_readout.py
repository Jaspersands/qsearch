"""Public random X/Y block readout, exact source Gram and costed inference gates.

This breaks real-circuit conjugation aliases without duplicate packets or
inverses. Identifiability is not efficient learning or quantum advantage.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import product
import json
from pathlib import Path
from random import Random

import numpy as np

from theorems.dcp_adaptive_direction_rank_gate import integer
from theorems.dcp_affine_fiber_rigidity import matrix
from theorems.dcp_correlated_block_observables import information, measurement_channel
from theorems.dcp_correlated_phase_block import syndrome_circuit
from theorems.dcp_nonlinear_fiber_pairing import phase_value

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"research/phase_workbench/dcp_complex_axis_readout.json"
CONTRACT=ROOT/"research/hypotheses/dcp_complex_axis_readout_contract.json"


def feedback_coefficients(labels,syndrome_index):
    A=matrix(labels)
    n,m=len(A),len(A[0])
    integer(syndrome_index,"measured syndrome index",0,4**n-1)
    return [(sum((((syndrome_index >> (2*l))&3)+1)*(A[l][i]%8) for l in range(n))+i)%8 for i in range(m)]


def public_feedback(labels):
    A=matrix(labels)
    n,m=len(A),len(A[0])
    if m>256 or 4**n*m>100000:
        raise ValueError("UNKNOWN: full feedback-table export cap; no compact policy cost waived")
    return [feedback_coefficients(A,y) for y in range(4**n)]


def readout_gate_plan(labels,axes_mask,*,measured_syndrome_index=0,use_feedback=False):
    circuit=syndrome_circuit(labels)
    m=circuit["input_phase_qubits"]
    integer(axes_mask,"public Y-axis mask",0,(1 << m)-1)
    n=circuit["measured_syndrome_qubits"]//2
    integer(measured_syndrome_index,"measured syndrome index",0,4**n-1)
    coefficients=feedback_coefficients(labels,measured_syndrome_index) if use_feedback else [0]*m
    terminal=[]
    for i in range(m):
        terminal.extend([["T",i]]*coefficients[i])
        if axes_mask >> i & 1:
            terminal.append(["SDG",i])
        terminal.append(["H",i])
    return {"syndrome_circuit":circuit,"public_Y_axis_mask_hex":hex(axes_mask),
            "terminal_gates_after_syndrome_measurement":terminal,
            "terminal_Z_measurement_wires":list(range(m)),
            "actual_axes":"X/Y after optional public T-grid phase feedback",
            "T_grid_feedback_coefficients":coefficients,
            "feedback_uses_public_source_and_measured_syndrome_only":True,
            "feedback_computed_only_for_realized_syndrome":True,
            "full_feedback_table_is_calibration_only":True,
            "measured_syndrome_index":measured_syndrome_index,
            "public_uniform_mask_bits_per_attempt":m,
            "mask_is_retained_in_classical_record":True,
            "source_quantum_preparations_per_attempt":m,
            "quantum_samples_multiplied_by_number_of_calibrated_masks":False,
            "unknown_source_inverse_or_duplicate_packet_used":False,
            "hardware_transpilation_or_execution_performed":False}


def axis_ensemble(labels,phase_bits,visibility,*,use_feedback=False):
    A=matrix(labels)
    n,m=len(A),len(A[0])
    integer(phase_bits,"finite phase bits",3,8)
    K=(1 << (phase_bits-2))**n
    M=1 << m
    if m>4 or K*4**n*M*M>100000:
        raise ValueError("UNKNOWN: complete mask/secret likelihood calibration cap")
    feedback=public_feedback(A) if use_feedback else None
    channels=[measurement_channel(A,phase_bits,visibility,axes_mask=r,T_feedback_by_syndrome=feedback) for r in range(M)]
    P=np.stack([C["probabilities"]/M for C in channels],axis=1)
    return {"probabilities":P,"secrets":channels[0]["secrets"],
            "syndrome_probabilities":channels[0]["syndrome_probabilities"],
            "all_masks_calibrated":M,"full_likelihood_entries":int(P.size)}


def alias_metrics(probabilities,secrets,modulus):
    P=np.asarray(probabilities)
    K=len(secrets)
    if P.shape[0]!=K:
        raise ValueError("secret/table dimension mismatch")
    aliases=[]
    for s in range(K):
        aliases.append([t for t in range(K) if np.max(np.abs(P[s]-P[t]))<1e-11])
    negation_residual=0.0
    for i,s in enumerate(secrets):
        j=secrets.index(tuple(-a%modulus for a in s))
        negation_residual=max(negation_residual,float(np.max(np.abs(P[i]-P[j]))))
    classes={min(group) for group in aliases}
    return {"all_secret_laws_distinct_on_this_selected_matrix":all(len(g)==1 for g in aliases),
            "number_of_distinct_likelihood_classes":len(classes),
            "maximum_negation_pair_probability_difference":negation_residual,
            "complete_likelihood_comparisons_are_exponential":True,
            "aliases_by_secret_index":aliases}


def selected_control(labels,phase_bits,visibility,*,use_feedback=False):
    A=matrix(labels)
    E=axis_ensemble(A,phase_bits,visibility,use_feedback=use_feedback)
    baseline=measurement_channel(A,phase_bits,visibility)
    Q=1 << (phase_bits-2)
    return {"full_labels":[list(row) for row in A],"phase_bits":phase_bits,
            "visibility_exact":str(Fraction(visibility)),"residual_secret_modulus":Q,
            "public_source_syndrome_T_feedback_used":use_feedback,
            "fixed_X_information":information(baseline["probabilities"]),
            "public_random_XY_information":information(E["probabilities"]),
            "fixed_X_aliases":alias_metrics(baseline["probabilities"],E["secrets"],Q),
            "random_XY_aliases":alias_metrics(E["probabilities"],E["secrets"],Q),
            "exported_readout_plan":readout_gate_plan(A,1,use_feedback=use_feedback),
            "all_public_masks_calibrated":E["all_masks_calibrated"],
            "likelihood_entries_enumerated":E["full_likelihood_entries"],
            "selected_matrix_is_native_average_evidence":False,
            "higher_mutual_information_than_fixed_X_guaranteed":False,
            "decoder_or_speedup_candidate_supplied":False}


def exact_coarse_norm(n,m,visibility):
    integer(n,"exact coarse components",1,2)
    integer(m,"exact physical width",1,4)
    if 4**(n*m)*8**m>1000000:
        raise ValueError("UNKNOWN: exact weighted parallelogram census cap")
    v=Fraction(visibility)
    if not 0<=v<=1:
        raise ValueError("visibility outside[0,1]")
    total=Fraction(0)
    M=1 << m
    for flat in product(range(4),repeat=n*m):
        A=tuple(flat[l*m:(l+1)*m] for l in range(n))
        f=[phase_value(A,x,4) for x in range(M)]
        counts={y:f.count(y) for y in set(f)}
        value=Fraction(0)
        for x,z in product(range(M),repeat=2):
            if f[x]!=f[z]:
                continue
            u=x^z
            w=u
            while True:
                if f[x^w]==f[x] and f[z^w]==f[x]:
                    value+=v**(2*w.bit_count())/counts[f[x]]/M
                if w==0:
                    break
                w=(w-1)&u
        total+=value/4**(n*m)
    return total


def native_Gram_census(visibility,*,use_feedback=False,phase_bits=4):
    v=Fraction(visibility)
    integer(phase_bits,"complete native census phase bits",3,4)
    q,Q=1 << phase_bits,1 << (phase_bits-2)
    gram=np.zeros((Q,Q))
    for row in product(range(q),repeat=2):
        E=axis_ensemble((row,),phase_bits,v,use_feedback=use_feedback)
        P=E["probabilities"].reshape(Q,-1)
        # Exact source-matched Q(R,y,z)=1/4 * (D_y/4) *1/4.
        reference=np.tile(np.repeat(E["syndrome_probabilities"]/16,4),4)
        active=reference>0
        gram+=(P[:,active]/reference[active])@P[:,active].T/(q*q)
    norm=exact_coarse_norm(1,2,v)
    expected=np.ones((Q,Q))+np.eye(Q)*(float(norm)-1)
    if np.max(np.abs(gram-expected))>1e-10:
        raise ArithmeticError("complete native all-secret Gram theorem falsified")
    return {"components":1,"physical_width":2,"phase_bits":phase_bits,"visibility_exact":str(v),
            "public_source_syndrome_T_feedback_used":use_feedback,
            "all_original_label_matrices":q*q,"all_public_axis_masks":4,
            "all_residual_secrets":Q,"full_Gram_observed":gram.tolist(),
            "exact_common_diagonal_from_coarse_parallelogram_census":str(norm),
            "exact_off_diagonal":"1","includes_zero_and_order_two_secrets":True,
            "source_family_identifiable_in_L2":norm>1,
            "efficient_inference_or_TV_lower_bound_proved":False,
            "fiber_sizes_enumerated_only_for_bounded_control":True}


def native_query_frontier(n):
    integer(n,"native components",2,4096)
    H=n*(n+6)  # residual modulus2^(n+6), original t=n+8.
    T=n*n
    tolerance=Fraction(1,n*n)
    distinguished=6*n**4
    numerator=T*distinguished+1
    success_bits=max(0,H-(numerator-1).bit_length())
    return {"components":n,"original_phase_bits":n+8,"physical_width":3*n,
            "all_residual_secret_count_binary_exponent":H,
            "source_matched_reference_sampling":"draw A,R; draw uniform original x; set y=A*x mod4; draw uniform z",
            "reference_sampler_needs_fiber_sizes_or_secret":False,
            "centered_density_squared_norm_upper":"6",
            "any_public_source_syndrome_local_phase_feedback_before_random_mask_covered":True,
            "random_axes_may_depend_on_secret_history_instead_of_fresh_uniform_coins":False,
            "adaptive_phase_feedback_transcript_information_bits_upper_per_fresh_batch":"3",
            "positive_norm_lower_factors_at_inverse_n_noise":[{"base_numerator":n-1,"base_denominator":n,"exponent":6*n},
                                                                    {"one_minus_two_to_negative":n}],
            "every_distinct_secret_pair_source_kernel_exact":"1",
            "unavoidable_negation_alias_after_public_XY_mask":False,
            "statistical_queries":T,"absolute_SQ_tolerance":str(tolerance),
            "max_secrets_distinguished_per_query_hex":hex(distinguished),
            "SQ_uniform_identification_probability_power_of_two_upper_exponent":success_bits,
            "SQ_query_evaluation_time_restricted":False,
            "raw_sample_learning_or_joint_multi_record_queries_ruled_out":False,
            "efficient_decoder_or_classical_simulator_supplied":False,
            "Pauli_importance_estimator_second_moment_at_weight_floor_n_over_four":{"power_of_two":n//4},
            "all_source_theorems_external_review_complete":False}


def xy_parity_estimator(width,outcome,axes_mask,support,desired_Y_mask):
    integer(width,"original phase width",1,4096)
    for value,name in ((outcome,"X/Y readout bits"),(axes_mask,"public axes"),(support,"Pauli support"),(desired_Y_mask,"Pauli Y axes")):
        integer(value,name,0,(1 << width)-1)
    if desired_Y_mask & ~support:
        raise ValueError("desired Y axes must lie on the observable support")
    if axes_mask&support != desired_Y_mask:
        return 0
    return (-1 if (outcome&support).bit_count()%2 else 1)*(1 << support.bit_count())


def build_report():
    rng=Random(101519)
    native=((rng.randrange(16),rng.randrange(16),rng.randrange(16)),)
    return {"contract_id":"public_complex_axes_native_Gram_and_inference_contract_v1",
            "status":"COMPLEX_GATE_READOUT_EXACT_KERNEL_REVIEW_PENDING",
            "selected_controls":[selected_control(A,t,v) for A,t,v in (
                (((4,8),),4,Fraction(7,8)),
                (((1,0,5,1),(0,1,1,2)),4,Fraction(7,8)),
                (native,4,Fraction(1,2)))]+
                [selected_control(native,4,Fraction(1,2),use_feedback=True)],
            "complete_native_Gram_censuses":[native_Gram_census(v) for v in (Fraction(1),Fraction(1,2),Fraction(0))]+
                [native_Gram_census(Fraction(1,2),use_feedback=True),native_Gram_census(Fraction(1,2),phase_bits=3)],
            "native_inference_frontiers":[native_query_frontier(n) for n in (8,16,32,64,128,256)],
            "accepted_speedup_candidate":False,"novelty_claim":False,
            "source_quantum_preparations_executed":0,"actual_natural_source_noise_certified":False,
            "same_state_copy_source_or_unknown_inverse_required":False,
            "identifiability_does_not_prove_efficient_learning":True,
            "random_axes_guarantee_per_attempt_information_improvement":False,
            "reference_is_an_exact_classical_sampler_for_real_data":False}


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-write",action="store_true")
    args=parser.parse_args(argv)
    report=build_report()
    if not args.no_write:
        REPORT.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"status":report["status"],"selected_controls":len(report["selected_controls"]),"native_Gram_censuses":len(report["complete_native_Gram_censuses"]),
                      "efficient_decoder":False,"artifact":str(REPORT)}))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
