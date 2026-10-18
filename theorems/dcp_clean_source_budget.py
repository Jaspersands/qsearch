"""Costed clean-predictor transfer and a public sine-source budget fixed point.

This does not supply a predictor, certify a lattice promise, or execute a large
source. Harsh benchmark noise is not a prerequisite for every useful algorithm.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path
import sys

import numpy as np
from flint import fmpq_mat,fmpz_mat
from sympy import nextprime

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))

from theorems.dcp_adaptive_direction_rank_gate import integer
from theorems.lattice_sine_window_source import (
    SineWindowSource,ceil_sqrt_fraction,promise_budget,resource_estimate,
)

REPORT=ROOT/"research/reductions/dcp_clean_source_budget.json"
CONTRACT=ROOT/"research/hypotheses/dcp_clean_source_budget_contract.json"
CONTRACT_ID="clean_predictor_noise_source_budget_review_pending_v1"


def copy_budget_excluded(components,bits,copies,advantage):
    """Compare (2^K-1)/(2*q^n)<eps without allocating n*t bits of integers."""
    integer(components,"predictor secret components",1)
    integer(bits,"original phase bits",3)
    integer(copies,"original sample budget",1)
    eps=Fraction(advantage)
    if not 0<eps<=Fraction(1,2):
        raise ValueError("valid useful-bit advantage required")
    N=components*bits
    if copies>N:
        return False
    a,b=eps.numerator,eps.denominator
    shift=N+1-copies
    if a.bit_length()+shift>b.bit_length():
        return True
    q=a << shift
    if q>=b:
        return True
    gap=b-q
    if gap.bit_length()+copies>b.bit_length():
        return False
    return gap << copies < b


def transfer_budget(copies,advantage,visibility_loss,*,joint_preparation_error_per_call=0,adapter_total_error=0):
    integer(copies,"TOTAL original calls of the hypothetical clean predictor",1)
    if copies.bit_length()>4096:
        raise ValueError("UNKNOWN: exact resource arithmetic cap")
    eps,gamma,prep,adapter=map(Fraction,(advantage,visibility_loss,joint_preparation_error_per_call,adapter_total_error))
    if not 0<eps<=Fraction(1,2) or any(not 0<=e<=1 for e in (gamma,prep,adapter)):
        raise ValueError("valid clean advantage and trace/channel error budgets required")
    noise=copies*gamma/2
    total=noise+copies*prep+adapter
    lower=max(Fraction(-1,2),eps-total)
    return {"original_source_calls":copies,"assumed_clean_average_advantage_exact":str(eps),
            "visibility_loss_per_original_qubit_upper_exact":str(gamma),
            "classical_Z_fault_union_trace_distance_upper_exact":str(min(Fraction(1),noise)),
            "per_call_joint_CQ_preparation_error_upper_exact":str(prep),
            "all_adapter_channel_error_upper_exact":str(adapter),
            "total_charged_trace_channel_error_upper_exact":str(min(Fraction(1),total)),
            "noisy_average_advantage_lower_IF_clean_predictor_exact":str(lower),
            "half_clean_advantage_preserved":lower>=eps/2,
            "arbitrary_correlated_classical_Z_masks_covered_IF_fixed_secret_marginal_union_bounds_hold":True,
            "arbitrary_coherent_noise_with_same_one_qubit_marginals_covered":False,
            "preparation_error_requires_joint_CQ_or_uniform_channel_hybrid_bound":True,
            "original_full_label_law_and_private_adapter_boundary_must_be_preserved":True,
            "clean_predictor_implemented_or_certified":False,
            "fixed_inverse_dimension_benchmark_noise_is_mandatory":False}


def _dyadic_at_least(value):
    threshold=max(2,Fraction(value).__ceil__())
    return 1 << (threshold-1).bit_length()


def plan_sine_source(basis,norm_squared_lower,norm_squared_upper,*,copy_power=2,copy_multiplier=1,
                     advantage_coefficient=Fraction(1,16),advantage_power=0,predictor_family="native_lift"):
    B=tuple(tuple(row) for row in basis)
    n=len(B)
    if not 1<=n<=64 or any(len(row)!=n for row in B):
        raise ValueError("bounded square public integer row basis required")
    for row in B:
        for a in row:
            if type(a) is not int or abs(a).bit_length()>4096:
                raise ValueError("UNKNOWN: exact signed public basis arithmetic cap")
    if not fmpz_mat(B).det():
        raise ValueError("full-rank public lattice basis required")
    for value in (norm_squared_lower,norm_squared_upper):
        integer(value,"public squared-norm interval endpoint",1)
        if value.bit_length()>4096:
            raise ValueError("UNKNOWN: norm interval arithmetic cap")
    if norm_squared_lower>norm_squared_upper:
        raise ValueError("ordered public norm interval required")
    integer(copy_power,"fixed polynomial copy exponent",1,8)
    integer(copy_multiplier,"copy multiplier",1,10**6)
    integer(advantage_power,"fixed inverse-polynomial advantage exponent",0,8)
    coefficient=Fraction(advantage_coefficient)
    if not 0<coefficient<=Fraction(1,2):
        raise ValueError("positive clean advantage coefficient<=1/2 required")
    if predictor_family not in ("native_lift","scalar"):
        raise ValueError("explicit clean scalar or lifted-native predictor family required")
    inverse=fmpq_mat(B).inv()
    bounds=[]
    for j in range(n):
        norm=sum((Fraction(int(inverse[i,j].numerator),int(inverse[i,j].denominator))**2 for i in range(n)),Fraction(0))
        bounds.append(ceil_sqrt_fraction(norm_squared_upper*norm))
    # For every split coordinate and every1<=g<p, |h_j|<=bound_j+1.
    C=sum(bounds)+1
    m=max(1,(10+n-1)//n-1)
    iterations=[]
    for _ in range(256):
        t=n*(m+1)
        if t>1000000 or m>100000:
            raise ValueError("UNKNOWN: public box/modulus fixed-point cap")
        copies=copy_multiplier*t**copy_power
        eps=coefficient/t**advantage_power
        gamma=eps/(2*copies)
        boundary=Fraction(C,1 << m)
        iterations.append({"parent_box_bits":m,"cyclic_phase_bits":t,
                           "hypothetical_predictor_copy_upper":copies,"target_visibility_loss_exact":str(gamma),
                           "public_box_loss_upper_exact":str(boundary)})
        if boundary<=gamma/2:
            break
        required=Fraction(2*C,1)/gamma
        m=max(m+1,(_dyadic_at_least(required)).bit_length()-1)
    else:
        raise ValueError("UNKNOWN: box/modulus fixed point did not close")
    components=t-8 if predictor_family=="native_lift" else 1
    if copy_budget_excluded(components,t,copies,eps):
        raise ValueError("INCONSISTENT: declared clean first-bit predictor violates the native copy upper bound")
    side=_dyadic_at_least(ceil_sqrt_fraction(Fraction(484*norm_squared_upper,49)/gamma))
    radius_squared=Fraction(n*side*side,norm_squared_lower)
    gap=ceil_sqrt_fraction(radius_squared)+1  # Strict, including integer-square boundary.
    pmin=gap+1
    packet_loss=Fraction(242*norm_squared_upper,49*side*side)
    budget=transfer_budget(copies,eps,gamma,joint_preparation_error_per_call=eps/(8*copies),adapter_total_error=eps/8)
    if packet_loss+boundary>gamma or not budget["half_clean_advantage_preserved"]:
        raise ArithmeticError("public source/clean-predictor budget did not close")
    return {"public_basis_rows":[list(row) for row in B],"lattice_dimension":n,
            "assumed_shortest_norm_squared_interval":[norm_squared_lower,norm_squared_upper],
            "norm_interval_squared_ratio_exact":str(Fraction(norm_squared_upper,norm_squared_lower)),
            "constant_factor_norm_interval":norm_squared_upper<=4*norm_squared_lower,
            "public_coefficient_absolute_bounds":bounds,"all_trial_parent_shift_l1_upper":C,
            "parent_box_bits":m,"parent_box_side_hex":hex(1 << m),
            "cyclic_phase_bits":t,"predictor_family":predictor_family,"predictor_secret_components":components,
            "lifted_native_components":t-8 if predictor_family=="native_lift" else None,
            "declared_predictor_copy_budget_not_excluded_by_bit_access_bound":True,
            "sample_model":{"copy_multiplier":copy_multiplier,"copy_power":copy_power,
                            "advantage_coefficient_exact":str(coefficient),"advantage_power":advantage_power},
            "packet_side_hex":hex(side),"packet_side_bits":side.bit_length()-1,
            "packet_loss_upper_exact":str(packet_loss),"boundary_loss_upper_exact":str(boundary),
            "required_unique_gap_strict_sufficient":gap,"splitting_prime_lower_bound":pmin,
            "coordinate_residue_trial_count_upper_formula":"n*(selected_prime-1), times all length guesses",
            "fixed_point_history":iterations,"clean_transfer_budget":budget,
            "per_known_adapter_rotation_error_required_exact":str(eps/(16*copies)),
            "known_adapter_rotations_upper_per_invocation":2*copies,
            "short_vector_gap_correct_trial_and_joint_preparation_precision_certified":False,
            "native_clean_predictor_supplied":False,
            "source_gate_cost_bit_lengths_and_all_outer_guesses_must_be_paid":True,
            "higher_required_gap_is_a_classical_hardness_certificate":False}


def materialize_public_source(plan,*,coordinate=0,residue=1):
    from theorems.planted_qary_usvp_source import prime_certificate
    model=plan["sample_model"]
    lo,hi=plan["assumed_shortest_norm_squared_interval"]
    expected=plan_sine_source(plan["public_basis_rows"],lo,hi,copy_power=model["copy_power"],
                             copy_multiplier=model["copy_multiplier"],
                             advantage_coefficient=Fraction(model["advantage_coefficient_exact"]),
                             advantage_power=model["advantage_power"],predictor_family=plan["predictor_family"])
    if plan!=expected:
        raise ValueError("public source budget receipt disagrees with its declared inputs")
    pmin=plan["splitting_prime_lower_bound"]
    if pmin.bit_length()>40:
        raise ValueError("UNKNOWN: automatic prime-certificate calibration cap")
    p=int(nextprime(pmin-1))
    certificate=prime_certificate(p).record()
    source=SineWindowSource(tuple(tuple(row) for row in plan["public_basis_rows"]),p,residue,coordinate,
                            int(plan["parent_box_side_hex"],16),int(plan["packet_side_hex"],16))
    check=promise_budget(source,lo,hi,plan["required_unique_gap_strict_sufficient"])
    if (source.phase_modulus.bit_length()-1!=plan["cyclic_phase_bits"] or
        not check["nonparallel_aliases_excluded_IF_promises_hold"] or
        not check["parallel_cross_colour_aliases_excluded_IF_promises_hold"] or
        Fraction(check["bad_rate_upper_IF_correct_trial_and_promises_hold"])>
        Fraction(plan["clean_transfer_budget"]["visibility_loss_per_original_qubit_upper_exact"])):
        raise ArithmeticError("existing sine-source ledger disagrees with closed fixed point")
    record={"selected_prime":p,"prime_certificate":certificate,
            "coordinate_residue_trials_upper":source.dimension*(p-1),
            "existing_source_promise_budget":check,"symbolic_source_resources":resource_estimate(source),
            "large_source_executed":False,"actual_lattice_promises_certified_from_basis":False}
    return json.loads(json.dumps(record))


def noise_physics_controls():
    def distance(a,b):
        return float(np.sum(abs(np.linalg.eigvalsh(a-b)))/2)
    rows=[]
    laws=(
        ("shared_all_Z",{0:Fraction(15,16),7:Fraction(1,16)}),
        ("disjoint_single_Z",{0:Fraction(13,16),1:Fraction(1,16),2:Fraction(1,16),4:Fraction(1,16)}),
        ("independent_Z",{e:Fraction(1,16)**e.bit_count()*Fraction(15,16)**(3-e.bit_count()) for e in range(8)}),
    )
    for name,law in laws:
        bound=sum((p*e.bit_count() for e,p in law.items()),Fraction(0))
        maximum=0.0
        for s in range(8):
            psi=np.exp(2j*np.pi*np.arange(8)*s/8)/np.sqrt(8)
            pure=np.outer(psi,psi.conj())
            rho=np.zeros((8,8),complex)
            for e,p in law.items():
                noisy=psi*np.array([(-1)**((e&x).bit_count()) for x in range(8)])
                rho+=float(p)*np.outer(noisy,noisy.conj())
            actual=distance(rho,pure)
            if actual>float(bound)+1e-12 or abs(actual-float(1-law.get(0,0)))>1e-12:
                raise ArithmeticError("actual original Z-mixture violates trace union bound")
            maximum=max(maximum,actual)
        rows.append({"noise_law":name,"actual_fixed_secret_joint_trace_distance_max":maximum,
                     "marginal_union_upper_exact":str(bound),"all_eight_secrets_checked":True})
    plus=np.ones(2)/np.sqrt(2)
    minus=np.array([1,-1])/np.sqrt(2)
    reference=np.kron(plus,plus)
    eta=Fraction(1,8)
    state=np.sqrt(1-float(eta*eta))*reference+float(eta)*np.kron(minus,minus)
    pure=np.outer(reference,reference)
    coherent=np.outer(state,state)
    marginal=np.trace(coherent.reshape(2,2,2,2),axis1=1,axis2=3)
    local=distance(marginal,np.outer(plus,plus))
    joint=distance(coherent,pure)
    if not joint>2*local+1e-12:
        raise ArithmeticError("coherent-noise marginal counterexample failed")
    return {"classical_Z_mixture_controls":rows,
            "coherent_noise_marginal_counterexample":{"amplitude_exact":str(eta),
                "one_qubit_trace_distance":local,"sum_two_marginal_trace_distances":2*local,
                "joint_trace_distance":joint,"classical_Z_mask_assumption_satisfied":False}}


def verified_easy_source_control():
    seed=plan_sine_source(((2,2),(1,2)),1,1)
    D=seed["required_unique_gap_strict_sufficient"]+1
    B=((D,D),(D-1,D))
    plan=plan_sine_source(B,1,1)
    W=((1,-1),(-(D-1),D))
    transformed=fmpz_mat(W)*fmpz_mat(B)
    if fmpz_mat(W).det()!=1 or transformed!=fmpz_mat(((1,0),(0,D))):
        raise ArithmeticError("easy source calibration lost its unimodular certificate")
    side=int(plan["packet_side_hex"],16)
    if D<plan["required_unique_gap_strict_sufficient"] or D*D<=2*side*side:
        raise ArithmeticError("easy source calibration does not satisfy the actual uniqueness premise")
    result=materialize_public_source(plan)
    result.update({"public_plan":plan,"actual_lattice_promises_certified_from_basis":True,
                   "certificate_scope":"THIS_CLASSICALLY_EASY_UNIMODULAR_DIAGONAL_CALIBRATION_ONLY",
                   "unimodular_left_transform":[list(row) for row in W],
                   "diagonalized_basis":[[1,0],[0,D]],"shortest_norm_squared_exact":1,
                   "shortest_nonparallel_norm_squared_exact":D*D,
                   "known_parent_shift_FOR_CALIBRATION_ONLY":[0,-1],
                   "short_vector_was_input_to_planner_or_source_constructor":False})
    return result


def build_report():
    bases=(((1,0),(0,257)),((17,0),(16,1)),((1,0,0),(0,257,0),(0,0,65537)))
    plans=[plan_sine_source(B,1,2,advantage_power=a) for B in bases for a in (0,1)]
    return {"schema_version":1,"contract_id":CONTRACT_ID,
            "status":"CLEAN_FIRST_CONDITIONAL_SOURCE_TRADEOFF_NOT_A_DECODER",
            "public_fixed_point_plans":plans,
            "clean_scalar_comparison":plan_sine_source(bases[0],1,2,copy_power=1,predictor_family="scalar"),
            "existing_source_integration_control":verified_easy_source_control(),
            "actual_noise_physics_controls":noise_physics_controls(),
            "classically_easy_calibration_bases_are_hard_instances":False,
            "inverse_n_noise_robustness_is_a_prerequisite_for_polynomial_clean_DCP_progress":False,
            "new_lattice_reduction_or_novelty_claim":False,"accepted_speedup_candidate":False,
            "regev_primary_context":"https://arxiv.org/abs/cs/0304005",
            "cached_primary_proof":"research/literature_cache/cs_0304005_source/quantum_average.tex"}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write",action="store_true")
    args=parser.parse_args()
    r=build_report()
    if args.write:
        REPORT.write_text(json.dumps(r,indent=2)+"\n")
    print(json.dumps({"status":r["status"],"fixed_point_plans":len(r["public_fixed_point_plans"]),
                      "native_clean_predictor":False,"source_executed":False}))


if __name__=="__main__":
    main()
