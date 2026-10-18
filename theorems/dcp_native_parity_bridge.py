"""Conditional cyclic-DCP reduction through native single-bit prediction.

No predictor is implemented. Exact source/control plans, bit-access obstructions
and polynomial resource implications must not be relabeled as a solver.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))

from theorems.dcp_adaptive_direction_rank_gate import integer
from theorems.dcp_affine_fiber_rigidity import matrix
from theorems.dcp_correlated_block_observables import information,measurement_channel
from theorems.dcp_correlated_phase_block import density
from theorems.dcp_nonlinear_fiber_pairing import phase_value

REPORT = ROOT/"research/reductions/dcp_native_parity_bridge.json"
CONTRACT = ROOT/"research/hypotheses/dcp_native_parity_bridge_contract.json"
CONTRACT_ID = "native_parity_to_cyclic_dcp_review_pending_v1"


def dyadic_phase_plan(bits,numerator):
    integer(bits,"known phase denominator bits",1,4096)
    integer(numerator,"canonical known phase numerator",0,(1 << bits)-1)
    terms = []
    for j in range(bits):
        if numerator >> j & 1:
            k = bits-j-1
            terms.append(["Z" if k==0 else "S" if k==1 else "T" if k==2 else "P_DYADIC_REQUIRES_SYNTHESIS",k])
    return {"angle":"2*pi*numerator/2^denominator_bits","numerator_hex":hex(numerator),
            "denominator_bits":bits,"known_single_wire_phase_terms":terms,
            "finite_universal_gate_synthesis_executed":False,
            "arbitrary_rotation_unit_cost_assumed":False,
            "synthesis_existence_reference":"https://arxiv.org/abs/quant-ph/0505030"}


@dataclass(frozen=True)
class AdaptedSample:
    phase_bits: int
    full_label: tuple[int,...]
    private_rotation_numerator: int

    def native_decoder_view(self):
        # Do NOT send asdict(self): the preparation angle is private reduction data.
        return {"original_phase_bits":self.phase_bits,"full_label":list(self.full_label)}

    def private_control_plan(self):
        return dyadic_phase_plan(self.phase_bits,self.private_rotation_numerator)


def lift_scalar_label(bits,global_mask,scalar_label,auxiliary_labels):
    """Compile a known phase adapter without accepting the unknown scalar secret."""
    integer(bits,"original cyclic phase bits",3,4096)
    q = 1 << bits
    r = tuple(global_mask)
    if not 2 <= len(r) <= 1024 or len(auxiliary_labels)!=len(r)-1:
        raise ValueError("one fixed global mask and n-1 fresh auxiliary labels required")
    for value in r:
        integer(value,"private global mask coordinate",0,q-1)
    labels = (scalar_label,*auxiliary_labels)
    for value in labels:
        integer(value,"canonical original or auxiliary label",0,q-1)
    offset = sum(a*b for a,b in zip(labels,r))%q
    return AdaptedSample(bits,tuple(labels),offset)


def unmask_predicted_parity(native_prediction,global_mask):
    integer(native_prediction,"native first-coordinate parity prediction",0,1)
    r = tuple(global_mask)
    if not r or any(type(v) is not int or v<0 for v in r):
        raise ValueError("private global mask required")
    return native_prediction^(r[0]&1)


def injected_Z_coin(n,random_word):
    """Rejection rule: accepted words give fault probability exactly1/(2n)."""
    integer(n,"native components",2,1024)
    width = (2*n-1).bit_length()
    integer(random_word,"fresh noise random word",0,(1 << width)-1)
    return None if random_word>=2*n else int(random_word==0)


def prefix_rescale_plan(original_bits,known_prefix_bits,known_prefix,original_label):
    integer(original_bits,"original phase bits",3,4096)
    integer(known_prefix_bits,"correctly recovered prefix length",0,original_bits-1)
    integer(known_prefix,"canonical recovered prefix",0,(1 << known_prefix_bits)-1)
    integer(original_label,"canonical original source label",0,(1 << original_bits)-1)
    bits = original_bits-known_prefix_bits
    return {"new_phase_bits":bits,"new_scalar_label":original_label% (1 << bits),
            "private_rotation":dyadic_phase_plan(original_bits,(-original_label*known_prefix)%(1 << original_bits)),
            "known_prefix_correctness_is_assumed_not_proved":True,
            "requires_fresh_original_phase_sample":True,
            "postselection_or_source_inverse_required":False,
            "fresh_uniform_label_law_preserved_by_truncation":True}


def minimum_copies_for_advantage(n,bits,advantage,*,visibility=Fraction(1)):
    integer(n,"native secret components",1,512)
    integer(bits,"original phase bits",3,1024)
    if n*bits>200000:
        raise ValueError("UNKNOWN: exact copy-bound arithmetic cap")
    eps = Fraction(advantage)
    if not 0<eps<=Fraction(1,2):
        raise ValueError("nonzero prediction advantage <=1/2 required")
    v = Fraction(visibility)
    if not 0<=v<=1:
        raise ValueError("independent original Z visibility outside[0,1]")
    if v==0:
        return None
    # Clean optimal advantage is half the Bhattacharyya overlap between the
    # Boolean subset-sum occupancy law and its order-two translate. Integer
    # occupancies give E_A advantage <=(2^M-1)/(2*q^n), stronger than existence.
    target = eps.denominator+2*eps.numerator*(1 << (n*bits))
    if v<1:
        # Entrywise nuclear-norm bound gives the stronger noisy expression
        # ((1+v)^M-1)/(2*q^n). Original INDEPENDENT Z faults are essential here.
        base = 1+v
        def enough(copies):
            if copies*max(base.numerator.bit_length(),base.denominator.bit_length())>20000000:
                raise ValueError("UNKNOWN: exact noisy threshold arithmetic cap")
            return base.numerator**copies*eps.denominator>=target*base.denominator**copies
        lo,hi = 0,max(1,n*bits)
        while not enough(hi):
            hi*=2
        while lo<hi:
            mid=(lo+hi)//2
            if enough(mid):
                hi=mid
            else:
                lo=mid+1
        return lo
    rounded_up = (target+eps.denominator-1)//eps.denominator
    return (rounded_up-1).bit_length()


def parity_copy_bound(n,bits,copies,advantage=Fraction(1,16),*,visibility=Fraction(1)):
    integer(copies,"total ORIGINAL native phase-qubit budget",0,200000)
    necessary = minimum_copies_for_advantage(n,bits,advantage,visibility=visibility)
    # 3^5<2^8 gives a conservative exact power-of-two union bound.
    e = n*bits-(8*copies+4)//5
    return {"native_components":n,"original_phase_bits":bits,"original_phase_qubits":copies,
            "specified_target":"first-coordinate parity of the uniform original secret",
            "all_algorithms_bit_advantage_power_of_two_upper_exponent":max(1,n*bits-copies+1) if copies else None,
            "fixed_target_exact_blindness_failure_probability_upper_power_exponent":max(0,e+1),
            "no_copy_advantage_exact":"0" if copies==0 else None,
            "probability_any_low_secret_parity_is_accessible_upper_power_exponent":max(0,e-n+1),
            "required_prediction_advantage_exact":str(Fraction(advantage)),
            "minimum_original_copies_necessary_for_that_advantage":necessary,
            "requested_budget_not_excluded_by_this_necessary_bound":necessary is not None and copies>=necessary,
            "independent_original_Z_visibility_for_stronger_threshold":str(Fraction(visibility)),
            "clean_average_advantage_upper_formula":"min(1/2,(2^K-1)/(2*q^n))",
            "independent_Z_average_advantage_upper_formula":"min(1/2,((1+v)^K-1)/(2*q^n))",
            "stronger_noisy_threshold_requires_independent_original_Z_faults":Fraction(visibility)<1,
            "arbitrary_secret_blind_joint_or_adaptive_measurements_covered":True,
            "any_secret_blind_noise_channel_also_covered_by_data_processing":True,
            "arbitrary_noise_data_processing_claim_is_for_clean_upper_bound_only":True,
            "average_advantage_bound_uses_subset_sum_mass_not_only_target_existence":True,
            "requires_source_labels_IID_uniform_and_secret_independent":True,
            "positive_mutual_information_guarantees_this_bit_access":False,
            "sufficient_copy_count_or_efficient_decoder_proved":False}


def reduction_resources(original_bits,native_samples_per_invocation,advantage,failure_bits=16,*,minimum_predictor_components=2,noise_matching="inject_independent"):
    integer(original_bits,"asymptotic cyclic phase bits",10,512)
    integer(native_samples_per_invocation,"assumed native original-sample budget",1,10**12)
    integer(failure_bits,"overall failure-budget bits",1,256)
    integer(minimum_predictor_components,"fixed minimum predictor component threshold",2,128)
    if original_bits<minimum_predictor_components+8:
        raise ValueError("native predictor unavailable at this phase size; terminal exhaustive cost must be modeled separately")
    if noise_matching not in ("inject_independent","clean_accepted"):
        raise ValueError("explicit native noise-matching contract required")
    eps = Fraction(advantage)
    n = original_bits-8
    native_visibility = Fraction(n-1,n) if noise_matching=="inject_independent" else Fraction(1)
    needed = minimum_copies_for_advantage(n,original_bits,eps,visibility=native_visibility)
    stage_failure_bits = failure_bits+(original_bits-1).bit_length()+2
    repeats = (Fraction(stage_failure_bits,2)/(eps*eps)).__ceil__()
    if repeats%2==0:
        repeats+=1
    terminal_bits = minimum_predictor_components+7
    stages = original_bits-terminal_bits
    invocations = stages*repeats
    tail_candidates = 1 << terminal_bits
    tail_tests = failure_bits+terminal_bits+2
    source_calls = invocations*native_samples_per_invocation+tail_candidates*tail_tests
    rotations = 2*source_calls  # Prefix removal plus native mask; tail uses at most this.
    precision_bits = failure_bits+(rotations-1).bit_length()+2
    coin_attempts = failure_bits+(source_calls-1).bit_length()+2
    total_error = (stages*Fraction(1,1 << stage_failure_bits)
                   +(tail_candidates-1)*Fraction(1,1 << tail_tests)
                   +Fraction(rotations,1 << precision_bits)
                   +(Fraction(source_calls,1 << coin_attempts) if noise_matching=="inject_independent" else 0))
    if total_error>Fraction(1,1 << failure_bits):
        raise ArithmeticError("charged amplification/verification/precision budget exceeded")
    return {"original_phase_bits":original_bits,"maximum_native_components":n,
            "status":"CONDITIONAL_ON_UNIMPLEMENTED_NATIVE_PARITY_PREDICTOR" if native_samples_per_invocation>=needed else "INCONSISTENT_NATIVE_PREDICTOR_COPY_BUDGET",
            "required_native_average_prediction_advantage_exact":str(eps),
            "assumed_native_sample_budget_per_invocation":native_samples_per_invocation,
            "necessary_sample_budget_at_largest_dimension":needed,
            "minimum_predictor_components":minimum_predictor_components,
            "polynomial_implication_requires_that_threshold_fixed_independently_of_input_size":True,
            "native_noise_matching":noise_matching,
            "adaptive_bit_stages":stages,"fresh_independent_masked_invocations_per_stage":repeats,
            "native_predictor_invocations_upper":invocations,
            "fresh_clean_scalar_phase_samples_upper":source_calls,
            "global_private_mask_random_bits_upper":invocations*n*original_bits,
            "auxiliary_label_random_bits_upper":invocations*native_samples_per_invocation*(n-1)*original_bits,
            "optional_noise_coin_random_bits_expected_upper_per_sample":2*((2*n-1).bit_length()),
            "noise_coin_rejection_attempt_cap_per_sample":coin_attempts,
            "noise_coin_random_bits_worst_case_upper_per_sample":coin_attempts*((2*n-1).bit_length()),
            "noise_coin_cap_abort_probability_upper_exact":str(Fraction(source_calls,1 << coin_attempts) if noise_matching=="inject_independent" else Fraction(0)),
            "native_predictor_own_runtime_and_randomness_remain_a_hypothesis":True,
            "known_control_classical_arithmetic_per_sample_schoolbook_bit_cost":"O(n*t^2), plus precision-dependent finite-gate synthesis",
            "advantage_lower_bound_required_at_every_stage_and_native_dimension":True,
            "mask_samples_internal_randomness_and_workspace_reset_per_invocation_required":True,
            "known_single_wire_rotations_upper":rotations,
            "per_rotation_diamond_error_power_of_two_upper_exponent":precision_bits,
            "finite_gate_synthesis_must_be_paid_not_executed":True,
            "terminal_suffix_bits":terminal_bits,"terminal_candidate_count":tail_candidates,
            "fresh_clean_verifier_samples_per_candidate":tail_tests,
            "overall_failure_upper_exact_IF_predictor_hypothesis":str(total_error),
            "overall_failure_target_exact":str(Fraction(1,1 << failure_bits)),
            "correct_scalar_recovery_executed":False,
            "native_predictor_implemented_or_certified":False,
            "coherent_label_oracle_or_purifying_preparation_environment_supplied":False,
            "new_algorithm_or_speedup_established":False}


def finite_parity_control(labels,bits,visibility):
    A = matrix(labels)
    n,m = len(A),len(A[0])
    integer(bits,"finite phase bits",3,6)
    q,M = 1 << bits,1 << m
    if m>6 or q**n*M*M>200000:
        raise ValueError("UNKNOWN: full-secret parity density calibration cap")
    v = Fraction(visibility)
    if not 0<=v<=1:
        raise ValueError("visibility outside[0,1]")
    mixtures = [np.zeros((M,M),complex),np.zeros((M,M),complex)]
    for s in product(range(q),repeat=n):
        mixtures[s[0]&1]+=density(A,bits,s,v)/(q**n//2)
    delta = mixtures[0]-mixtures[1]
    frequencies = [phase_value(A,x,q) for x in range(M)]
    target = (q//2,)+(0,)*(n-1)
    matches = np.array([[tuple((a-b)%q for a,b in zip(frequencies[x],frequencies[z]))==target
                         for z in range(M)] for x in range(M)])
    expected = np.array([[2*float(v**((x^z).bit_count()))/M for z in range(M)] for x in range(M)])*matches
    residual = float(np.max(np.abs(delta-expected)))
    quantum_guess = .5+float(np.sum(np.abs(np.linalg.eigvalsh(delta))))/4
    counts = {}
    for f in frequencies:
        counts[f] = counts.get(f,0)+1
    overlap = sum(np.sqrt(count*counts.get(tuple((a+b)%q for a,b in zip(f,target)),0))/M
                  for f,count in counts.items())
    clean_optimal_guess = .5+overlap/2
    channel = measurement_channel(A,bits,v,coarse_bits=1)
    P = channel["probabilities"]
    even = np.mean([p for s,p in zip(channel["secrets"],P) if s[0]%2==0],axis=0)
    odd = np.mean([p for s,p in zip(channel["secrets"],P) if s[0]%2],axis=0)
    classical_guess = .5+float(np.sum(np.abs(even-odd)))/4
    if (residual>1e-11 or classical_guess>quantum_guess+1e-11 or
        quantum_guess>clean_optimal_guess+1e-11 or
        (v==1 and abs(quantum_guess-clean_optimal_guess)>1e-11)):
        raise ArithmeticError("physical parity frequency/measurement bound falsified")
    return {"full_labels":[list(row) for row in A],"original_phase_bits":bits,
            "visibility_exact":str(v),"target_frequency":list(target),
            "target_difference_ordered_pairs":int(np.count_nonzero(matches)),
            "max_exact_parity_density_identity_residual":residual,
            "optimal_original_quantum_parity_guess_probability":quantum_guess,
            "clean_subset_sum_overlap_optimal_parity_guess_probability":clean_optimal_guess,
            "subset_sum_occupancy_histogram":[{"frequency":list(f),"count":count} for f,count in sorted(counts.items())],
            "actual_mod2_joint_X_parity_guess_probability":classical_guess,
            "actual_mod2_joint_X_total_secret_information_bits":information(P)["uniform_secret_mutual_information_bits"],
            "full_density_and_secret_enumeration_is_polynomial":False,
            "fixture_is_a_native_high_probability_statement":False}


def source_pushforward_census():
    q,n = 8,2
    secret_masks_checked = identities = 0
    for s in range(q):
        images = set()
        for r in product(range(q),repeat=n):
            S = ((s+r[0])%q,r[1])
            images.add(S)
            for a in range(q):
                for auxiliary in range(q):
                    lifted = lift_scalar_label(3,r,a,(auxiliary,))
                    if (a*s+lifted.private_rotation_numerator)%q != sum(x*y for x,y in zip(lifted.full_label,S))%q:
                        raise ArithmeticError("native lift phase identity failed")
                    identities+=1
            secret_masks_checked+=1
        if len(images)!=q**n:
            raise ArithmeticError("global-mask pushforward is not uniform")
    return {"calibration_phase_bits":3,"components":n,"fixed_scalar_secrets":q,
            "secret_mask_pairs_checked":secret_masks_checked,"exact_phase_identities_checked":identities,
            "native_scaling_relation_t_equals_n_plus_8_used_in_this_small_control":False,
            "unknown_scalar_secret_is_an_input_to_adapter":False,
            "per_packet_mask_refresh_has_been_authorized":False}


def build_report():
    return {"schema_version":1,"contract_id":CONTRACT_ID,
            "status":"CONDITIONAL_NATIVE_PARITY_TO_CYCLIC_DCP_REDUCTION_PREDICTOR_MISSING",
            "literature_links":["https://arxiv.org/abs/quant-ph/0501044","https://arxiv.org/abs/quant-ph/0505030"],
            "complete_source_pushforward_control":source_pushforward_census(),
            "parity_density_controls":[finite_parity_control(A,t,v) for A,t,v in (
                (((1,2),),4,Fraction(1)),(((8,),),4,Fraction(1)),
                (((8,),),4,Fraction(1,2)),(((8,),),4,Fraction(0)),
                (((1,0),(0,1)),3,Fraction(1)),(((4,0),(0,4)),3,Fraction(1)),
                (((1,2,4),(1,2,3)),3,Fraction(1)),(((4,4),),4,Fraction(1)))],
            "native_copy_frontiers":[parity_copy_bound(n,n+8,3*n*T,visibility=Fraction(n-1,n)) for n in (8,32,64,128) for T in sorted({1,max(1,n//8)})],
            "conditional_resource_frontiers":[reduction_resources(t,2*(t-8)*t,Fraction(1,16)) for t in (16,32,64,128)],
            "large_only_predictor_tail_cost_countercontrol":reduction_resources(80,2*80*72,Fraction(1,16),minimum_predictor_components=64),
            "impossible_single_packet_predictor_countercontrol":reduction_resources(72,3*64,Fraction(1,16)),
            "first_bit_prediction_not_full_vector_recovery_is_sufficient":True,
            "positive_mutual_information_instantiates_predictor":False,
            "accepted_speedup_candidate":False,"novelty_claim":False,
            "native_predictor_implemented_or_certified":False,
            "actual_quantum_source_or_recovery_executed":False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write",action="store_true")
    args = parser.parse_args()
    r = build_report()
    if args.write:
        REPORT.write_text(json.dumps(r,indent=2)+"\n")
    print(json.dumps({"status":r["status"],"parity_density_controls":len(r["parity_density_controls"]),
                      "native_predictor":False,"resource_frontiers":len(r["conditional_resource_frontiers"])}))


if __name__ == "__main__":
    main()
