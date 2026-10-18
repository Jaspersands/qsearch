"""Native useful-bit measurements: weighted kernels and a scoped sparsity bound.

Dense spectral controls are exponential calibration, not quantum algorithms.
Polynomial circuits need not induce sparse observables. No general no-go.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import product
import json
from math import isqrt
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))

from theorems.dcp_adaptive_direction_rank_gate import integer
from theorems.dcp_affine_fiber_rigidity import matrix
from theorems.dcp_correlated_phase_block import density
from theorems.dcp_nonlinear_fiber_pairing import phase_value

REPORT = ROOT/"research/phase_workbench/dcp_native_parity_observables.json"
CONTRACT = ROOT/"research/hypotheses/dcp_native_parity_observables_contract.json"
CONTRACT_ID = "native_noisy_parity_observable_geometry_review_pending_v1"


def short_target_exclusion(n,bits,copies,failure_bits):
    """Exact union count, with sign reversal identified for an order-two target."""
    integer(n,"native secret components",1,256)
    integer(bits,"original phase bits",3,512)
    integer(copies,"TOTAL original IID phase qubits",1,200000)
    integer(failure_bits,"label-exception probability bits",1,200000)
    N=n*bits
    if N>100000:
        raise ValueError("UNKNOWN: signed-witness integer-arithmetic cap")
    budget=(1 << (N-failure_bits)) if N>=failure_bits else 0
    count,choose,r=0,1,0
    for w in range(1,copies+1):
        choose=choose*(copies-w+1)//w
        next_count=count+(choose << (w-1))
        if next_count>budget:
            break
        count,r=next_count,w
    return {"native_components":n,"original_phase_bits":bits,
            "total_original_phase_qubits":copies,
            "specified_target":"(q/2,0,...,0)",
            "excluded_signed_support_weights_through":r,
            "minimum_target_edge_Hamming_distance_on_good_labels":r+1,
            "oriented_short_signed_witness_count_hex":hex(count),
            "union_bound_denominator_binary_exponent":N,
            "label_exception_probability_upper_power_of_two_exponent":failure_bits,
            "exact_union_count_formula":"sum_(w=1..r) binom(K,w)*2^(w-1)",
            "native_scaling_t_equals_n_plus_8":bits==n+8,
            "label_dependent_observable_selection_covered":True,
            "IID_uniform_unfiltered_original_labels_required":True,
            "short_witness_absence_is_computational_hardness":False}


def _power_upper_exponent(numerator,denominator):
    """Largest nonnegative e for numerator/denominator<=2^-e, or None for zero."""
    if not numerator:
        return None
    if numerator>=denominator:
        return 0
    e=denominator.bit_length()-numerator.bit_length()
    return e-1 if numerator << e>denominator else e


def sparse_observable_frontier(n,bits,copies,target_row_degree,*,visibility=None,advantage=Fraction(1,16),failure_bits=None):
    integer(n,"native secret components",2,256)
    integer(target_row_degree,"certified maximum target-coupling entries per row",1)
    if target_row_degree.bit_length()>4096:
        raise ValueError("UNKNOWN: observable-degree certificate cap")
    v=Fraction(n-1,n) if visibility is None else Fraction(visibility)
    eps=Fraction(advantage)
    if not 0<=v<=1 or not 0<eps<=Fraction(1,2):
        raise ValueError("valid independent Z visibility and nonzero target advantage required")
    C=short_target_exclusion(n,bits,copies,n if failure_bits is None else failure_bits)
    w=C["minimum_target_edge_Hamming_distance_on_good_labels"]
    # ||O||<=1 implies row l2 norm<=1; at most D target entries give l1<=sqrt(D).
    root=isqrt(target_row_degree)
    root+=root*root<target_row_degree
    power_num,power_den=v.numerator**w,v.denominator**w
    good=min(Fraction(1,2),Fraction(root*power_num,2*power_den))
    f=C["label_exception_probability_upper_power_of_two_exponent"]
    averaged=min(Fraction(1,2),good+Fraction(1,1 << (f+1)))
    C.update({"independent_original_Z_visibility_exact":str(v),
              "maximum_target_coupling_entries_per_observable_row":target_row_degree,
              "ceil_sqrt_target_row_degree":root,
              "good_label_advantage_upper_formula":"min(1/2,ceil(sqrt(D))*v^(r+1)/2)",
              "good_label_advantage_power_of_two_upper_exponent":_power_upper_exponent(good.numerator,good.denominator),
              "good_label_advantage_exactly_zero":good==0,
              "average_advantage_power_of_two_upper_exponent":_power_upper_exponent(averaged.numerator,averaged.denominator),
              "requested_average_advantage_exact":str(eps),
              "sparse_class_excluded_at_requested_average_advantage":averaged<eps,
              "average_bound_includes_all_label_exceptions":True,
              "requires_original_independent_Z_faults_not_only_marginal_visibilities":True,
              "observable_is_effective_binary_decision_on_original_input":True,
              "observable_operator_norm_at_most_one_required":True,
              "postselected_conditional_advantage_without_acceptance_cost_covered":False,
              "all_polynomial_gate_circuits_induce_sparse_observables":False,
              "general_DCP_or_quantum_decoder_no_go":False})
    return C


def target_geometry(labels,bits):
    A=matrix(labels)
    integer(bits,"finite full-modulus phase bits",3,64)
    n,K=len(A),len(A[0])
    if K>8 or n>8 or any(a >=1 << bits for row in A for a in row):
        raise ValueError("UNKNOWN: canonical bounded finite observable calibration required")
    q,L=1 << bits,1 << K
    frequencies=[phase_value(A,x,q) for x in range(L)]
    h=(q//2,)+(0,)*(n-1)
    matches=np.array([[tuple((a-b)%q for a,b in zip(frequencies[x],frequencies[y]))==h
                       for y in range(L)] for x in range(L)],dtype=bool)
    distances=np.array([[(x^y).bit_count() for y in range(L)] for x in range(L)])
    return A,frequencies,matches,distances


def measurement_operators(labels,bits,visibility):
    """Exponential public-label reference operators, never given a secret."""
    v=Fraction(visibility)
    if not 0<=v<=1:
        raise ValueError("independent original Z visibility outside[0,1]")
    A,frequencies,target,distances=target_geometry(labels,bits)
    L=len(frequencies)
    kernel=target*np.array([[float(v**w) for w in row] for row in distances])
    groups={}
    for x,f in enumerate(frequencies):
        groups.setdefault(f,[]).append(x)
    q=1 << bits
    blocks=[]
    for f,left in sorted(groups.items()):
        partner=((f[0]+q//2)%q,)+f[1:]
        if partner not in groups or f>=partner:
            continue
        right=groups[partner]
        singular=np.linalg.svd(kernel[np.ix_(left,right)],compute_uv=False)
        blocks.append({"frequency":list(f),"paired_frequency":list(partner),
                       "left_fiber_size":len(left),"right_fiber_size":len(right),
                       "singular_values":[float(z) for z in singular],
                       "numerical_rank_not_exact_certificate":int(sum(singular>1e-11))})
    eig,U=np.linalg.eigh(kernel)
    # Null eigenvectors can be assigned fair random guesses. Dense finite control only.
    signs=np.where(eig>1e-11,1,np.where(eig < -1e-11,-1,0))
    optimal=(U*signs)@U.conj().T
    block_advantage=sum(sum(b["singular_values"]) for b in blocks)/L
    if abs(block_advantage-np.sum(abs(eig))/(2*L))>1e-10:
        raise ArithmeticError("weighted frequency-block SVD disagrees with physical trace norm")
    matching=np.zeros((L,L))
    used=set()
    edges=sorted((int(distances[x,y]),x,y) for x in range(L) for y in range(x+1,L) if target[x,y])
    chosen=[]
    for w,x,y in edges:
        if x not in used and y not in used:
            chosen.append((x,y,w))
            used.update((x,y))
            matching[x,y]=matching[y,x]=1
    return {"labels":A,"frequencies":frequencies,"target_mask":target,
            "distances":distances,"kernel":kernel,"optimal_observable":optimal,
            "matching_observable":matching,"matching_edges":chosen,
            "weighted_frequency_pair_blocks":blocks,
            "reference_optimal_advantage":float(np.sum(abs(eig)))/(2*L),
            "reference_matching_advantage":sum(float(v**w) for _,_,w in chosen)/L}


def physical_control(labels,bits,visibility):
    R=measurement_operators(labels,bits,visibility)
    A=R["labels"]
    n,K=len(A),len(A[0])
    q,L=1 << bits,1 << K
    if q**n*L*L>1000000:
        raise ValueError("UNKNOWN: full-secret Born/density calibration cap")
    v=Fraction(visibility)
    means=[np.zeros((L,L),complex),np.zeros((L,L),complex)]
    success={"optimal":[],"matching":[]}
    for s in product(range(q),repeat=n):
        rho=density(A,bits,s,v)
        means[s[0]&1]+=rho/(q**n//2)
        for name in success:
            O=R[name+"_observable"]
            success[name].append(.5+(1-2*(s[0]&1))*float(np.trace(O@rho).real)/2)
    delta=means[0]-means[1]
    residual=float(np.max(abs(delta-2*R["kernel"]/L)))
    achieved={name:float(np.mean(p)) for name,p in success.items()}
    helstrom=.5+np.sum(abs(np.linalg.eigvalsh(delta)))/4
    if (residual>1e-11 or abs(achieved["optimal"]-helstrom)>1e-10 or
        abs(achieved["matching"]-.5-R["reference_matching_advantage"])>1e-11 or
        achieved["matching"]>helstrom+1e-11):
        raise ArithmeticError("actual density violates observable measurement identity")
    nonzero_distances=R["distances"][R["target_mask"]]
    w=int(min(nonzero_distances)) if len(nonzero_distances) else None
    matching_bound=float(v**w)/2 if w is not None else 0
    if achieved["matching"]-.5>matching_bound+1e-11:
        raise ArithmeticError("one-sparse target observable bound violated")
    return {"full_labels":[list(row) for row in A],"phase_bits":bits,"original_qubits":K,
            "independent_original_Z_visibility_exact":str(v),
            "target_ordered_edges":int(R["target_mask"].sum()),
            "minimum_target_Hamming_distance":w,
            "target_geometry_maximum_row_degree":int(max(R["target_mask"].sum(axis=1))),
            "matching_edges":[list(edge) for edge in R["matching_edges"]],
            "weighted_frequency_pair_blocks":R["weighted_frequency_pair_blocks"],
            "physical_parity_density_kernel_residual":residual,
            "original_quantum_optimal_success_probability":float(helstrom),
            "measured_dense_reference_success_probability":achieved["optimal"],
            "measured_pairing_success_probability":achieved["matching"],
            "pairing_success_spread_over_all_fixed_secrets":float(np.ptp(success["matching"])),
            "pairing_advantage_upper_from_minimum_distance":matching_bound,
            "all_original_secrets_checked":q**n,
            "matrix_entries_allocated_for_kernel":L*L,
            "dense_reference_eigendecomposition_dimension":L,
            "numerical_density_and_spectral_calibration_tolerance":1e-10,
            "numerical_spectral_sign_zero_threshold":1e-11,
            "finite_float_replay_is_an_exact_algebraic_certificate":False,
            "finite_universal_gate_receiver_exported":False,
            "exponential_enumeration_and_spectral_costs_paid_as_reference_only":True,
            "fixture_establishes_native_high_probability_performance":False}


def rank_noise_scope_control(bits):
    """Same modulus and per-qubit noise, different rank and ORIGINAL sample load."""
    integer(bits,"scope-comparison phase bits",10,256)
    native_rank=bits-8
    v=Fraction(native_rank-1,native_rank)
    rows=[]
    for rank,name,visibility in ((native_rank,"native_growing_rank_noisy",v),
                                  (1,"scalar_same_modulus_and_visibility",v),
                                  (native_rank,"native_growing_rank_clean",Fraction(1))):
        K=2*rank*bits
        C=short_target_exclusion(rank,bits,K,max(1,bits//4))
        w=C["minimum_target_edge_Hamming_distance_on_good_labels"]
        bottom=visibility**K
        top=visibility**w
        lower_exponent=_power_upper_exponent(bottom.numerator,bottom.denominator)+(0 if bottom==1 else 1)
        rows.append({"regime":name,"components":rank,"phase_bits":bits,
                     "secret_entropy_bits":rank*bits,"original_phase_qubits":K,
                     "independent_original_Z_visibility_exact":str(visibility),
                     "expected_original_Z_faults_exact":str(K*(1-visibility)/2),
                     "minimum_coherence_if_a_target_edge_exists_power_of_two_lower_exponent":lower_exponent,
                     "maximum_target_edge_coherence_on_good_labels_power_of_two_upper_exponent":_power_upper_exponent(top.numerator,top.denominator),
                     "target_edges_or_efficient_receiver_existence_proved":False})
    return {"phase_bits":bits,"regimes":rows,
            "growing_rank_noise_bound_is_a_scalar_DCP_lower_bound":False,
            "clean_scalar_DCP_lift_requires_injecting_noise":False,
            "fault_count_is_a_decoder_failure_probability":False}


def build_report():
    return {"schema_version":1,"contract_id":CONTRACT_ID,
            "status":"SCOPED_NATIVE_SPARSE_OBSERVABLE_BOUND_DENSE_DECODER_OPEN",
            "native_frontiers":[sparse_observable_frontier(n,n+8,2*n*(n+8),D)
                                for n in (8,16,32,64,128) for D in (1,n**4)],
            "rank_and_noise_scope_controls":[rank_noise_scope_control(t) for t in (16,32,72,128)],
            "physical_controls":[physical_control(A,t,v) for A,t,v in (
                (((1,2),),4,Fraction(1)),
                (((8,),),4,Fraction(1,2)),
                (((2,2,2,2),),3,Fraction(1)),
                (((2,2,2,2),),3,Fraction(3,4)),
                (((2,2,2,2),),3,Fraction(0)),
                (((1,2,3,4,6,1),(2,1,4,3,1,6)),3,Fraction(3,4)))],
            "polynomial_circuit_dense_observable_counterexample":{
                "observable":"H^K (I-2|1^K><1^K|) H^K = I-2|minus^K><minus^K|",
                "circuit":"2K Hadamards and one multi-controlled Z; polynomial clean-ancilla decomposition",
                "direct_measurement":"K Hadamards, measure all original wires, return minus iff all outcomes are one; polynomial classical AND",
                "nonzero_off_diagonal_entries_per_row":"2^K-1",
                "for_all_labels_equal_target_h_target_degree_per_row":"2^(K-1)",
                "this_structured_label_fixture_is_native_typical":False,
                "polynomial_gates_imply_sparse_observable":False},
            "accepted_speedup_candidate":False,"new_active_negative_result_created":False,
            "general_quantum_decoder_impossibility_proved":False,"novelty_claim":False}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write",action="store_true")
    args=parser.parse_args()
    report=build_report()
    if args.write:
        REPORT.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"status":report["status"],"native_frontiers":len(report["native_frontiers"]),
                      "physical_controls":len(report["physical_controls"]),"accepted_speedup_candidate":False}))


if __name__=="__main__":
    main()
