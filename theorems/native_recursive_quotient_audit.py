"""Exact same-original quotient composition and honest recursive producer debt.

This consumes supplied hypotheses, never constructs a decision/multiple oracle.
Canonical node equality is not a Gaussian-law or true-prefix certificate.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path

from native_basis_lottery import original_bank, original_fit
from native_affine_fibre_relaxation import canonical_vector
from native_small_multiple_completion import multiple_quotient, _rational
from native_classical_modulus_descent import digest
from native_gaussian_quotient_completion import nearest_odd_division
from ternary_covariant_noise import root_digits
from ternary_noise_degradation import NoisyLinearRecord
from ternary_measured_lattice_decoder import integer, exact_json

ROOT=Path(__file__).resolve().parents[1]
DERIVATION=ROOT/"research/NATIVE_RECURSIVE_QUOTIENT_AUDIT.md"
REPORT=ROOT/"research/reductions/native_recursive_quotient_audit.json"


def adapt_chain(records, hypotheses, radius, max_steps=128):
    original=original_bank(records);q0=original[0].modulus;n=len(original[0].label)
    integer(max_steps,"positive complete chain cap",1);integer(radius,"public original radius")
    if 4*radius>=q0: raise ValueError("original verifier requires4R<q")
    hypotheses=tuple(hypotheses)
    if not hypotheses: raise ValueError("nonempty supplied hypothesis path required")
    base={"original_records_sha256":digest(tuple(r.public() for r in original)),
        "original_records_paid_once":len(original),"max_steps":max_steps,"verification_radius":radius,
        "declared_path_length":len(hypotheses),"steps":(),"candidate_secret":None,
        "sequential_response_rounding_evaluations":0,"canonical_composition_rounding_evaluations":0,
        "new_independent_original_samples_created":False,"multiple_producer_supplied":False,
        "true_prefix_or_Gaussian_law_certified":False,"planted_truth_or_uniqueness_certified":False}
    if len(hypotheses)>max_steps:
        return {**base,"status":"COMPLETE_PATH_CAP_EXCEEDED_NOT_NO_SECRET","complete_declared_path_or_terminal_preimage":False}
    current=original;prefix=(0,)*n;scale=1;steps=[]
    for index,(coefficient,multiple) in enumerate(hypotheses):
        q=current[0].modulus;multiple=canonical_vector(multiple,n,q)
        model=multiple_quotient(q,coefficient,multiple)
        step={"index":index,"parent_modulus":q,"parent_scale":scale,"parent_original_prefix":prefix,
            "coefficient":coefficient,"multiple":multiple,"parent_records_sha256":digest(tuple(r.public() for r in current))}
        if model is None:
            steps.append({**step,"status":"EXACT_CURRENT_RING_IMAGE_INCOMPATIBILITY"})
            return {**base,"status":"INCOMPATIBLE_SUPPLIED_PATH_NOT_NO_ORIGINAL_SECRET","steps":tuple(steps),
                "complete_declared_path_or_terminal_preimage":False}
        step["quotient_model"]=model.record()
        x=model.quotient_secret;Q=model.remaining_modulus;g=model.factor
        if g==1:
            candidate=tuple(a+scale*b for a,b in zip(prefix,x));fit=original_fit(original,candidate,radius)
            steps.append({**step,"status":"TERMINAL_UNIT_PREIMAGE_NOT_SOURCE_CERTIFICATE","current_algebraic_preimage":x})
            equations=tuple(tuple(t["coefficient"]*(s//t["parent_scale"]) % t["parent_modulus"] for s in candidate)==t["multiple"] for t in steps)
            if not all(equations): raise ArithmeticError("lifted preimage escaped supplied path")
            return {**base,"status":"ONE_ORIGINAL_RADIUS_FIT_SOURCE_CERTIFICATION_REQUIRED" if fit["fits_public_radius"] else "TERMINAL_PREIMAGE_ORIGINAL_RADIUS_FIT_FAILED",
                "steps":tuple(steps),"candidate_secret":candidate if fit["fits_public_radius"] else None,
                "terminal_original_algebraic_preimage":candidate,"original_fit":fit,
                "supplied_multiple_chain_equations_verified":equations,
                "unconsumed_supplied_hypotheses":len(hypotheses)-index-1,"complete_declared_path_or_terminal_preimage":True}
        nextprefix=tuple(a+scale*b for a,b in zip(prefix,x));nextscale=scale*Q
        if q0//nextscale!=g or not g<q: raise ArithmeticError("strict original-root quotient descent failed")
        children=[];receipts=[]
        for parent,origin in zip(current,original):
            residual=(parent.value-sum(a*b for a,b in zip(parent.label,x))) % q
            value=nearest_odd_division(residual,Q) % g
            direct_residual=(origin.value-sum(a*b for a,b in zip(origin.label,nextprefix))) % q0
            direct=nearest_odd_division(direct_residual,nextscale) % g
            child=NoisyLinearRecord(tuple(a % g for a in parent.label),value,g,parent.source_id)
            if direct!=value or child.label!=tuple(a % g for a in origin.label):
                raise ArithmeticError("nested and direct same-original quotient disagree")
            children.append(child);receipts.append({"source_id":origin.source_id,
                "parent_record_sha256":digest(parent.public()),"original_record_sha256":digest(origin.public()),
                "corrected_parent_response":residual,"corrected_original_response":direct_residual,
                "sequential_derived_response":value,"direct_original_derived_response":direct})
        node={"original_records_sha256":base["original_records_sha256"],"modulus":g,
            "original_scale":nextscale,"known_original_lower_prefix_IF_path_true":nextprefix}
        steps.append({**step,"status":"CANONICAL_ORIGINAL_QUOTIENT_NODE_NOT_TRUE_PREFIX_CERTIFICATE",
            "canonical_node":node,"canonical_node_sha256":digest(node),
            "derived_records":tuple(r.public() for r in children),"record_receipts":tuple(receipts),
            "source_IDs_preserved":True,"composition_verified_on_every_original":True})
        base["sequential_response_rounding_evaluations"]+=len(original)
        base["canonical_composition_rounding_evaluations"]+=len(original)
        current=tuple(children);prefix=nextprefix;scale=nextscale
    return {**base,"status":"SUPPLIED_PATH_EXHAUSTED_MISSING_TERMINAL_DECODER_NOT_NO_SECRET",
        "steps":tuple(steps),"complete_declared_path_or_terminal_preimage":True,
        "final_canonical_node":steps[-1]["canonical_node"]}


def recursion_cost(branches, depth, marginal_coverage, conditional_coverage=None):
    integer(branches,"positive list/coefficient branch budget",1);integer(depth,"positive recursive depth",1)
    p=_rational(marginal_coverage);c=None if conditional_coverage is None else _rational(conditional_coverage)
    if not 0<=p<=1 or c is not None and not 0<=c<=1: raise ValueError("valid coverage probabilities required")
    if depth*branches.bit_length()>65536: raise ValueError("complete exact recursion cost exceeds declared bit scope")
    leaves=branches**depth;nodes=depth+1 if branches==1 else (branches**(depth+1)-1)//(branches-1)
    return {"declared_branches_per_level":branches,"declared_depth":depth,
        "complete_tree_leaves_upper":leaves,"complete_tree_nodes_upper":nodes,
        "random_one_branch_success_IF_every_visited_true_list_covers":str(Fraction(1,leaves)),
        "each_fixed_true_root_marginal_coverage_lower_EXTERNAL":str(p),
        "all_required_fixed_root_events_Frechet_lower":str(max(Fraction(0),depth*p-(depth-1))),
        "conditional_on_every_previous_true_choice_coverage_lower_EXTERNAL":None if c is None else str(c),
        "all_levels_coverage_lower_IF_conditional_contract_proved":None if c is None else str(c**depth),
        "marginal_success_product_is_justified":False,"same_bank_repetition_amplifies_source_good_fraction":False,
        "fixed_root_Frechet_bound_covers_unknown_adaptive_root_selection":False,
        "polynomial_branch_budget_implies_polynomial_total_work":False,
        "actual_coverage_or_producer_contract_established":False,
        "tree_bound_is_a_general_reduction_lower_bound":False}


def fixed_root_source_contract(n,r,alpha,coefficient_bound):
    integer(n,"positive source dimension",1);integer(r,"positive source root",1)
    integer(coefficient_bound,"positive centered coefficient bound",1);alpha=_rational(alpha)
    if not 0<alpha<1: raise ValueError("positive subunit Gaussian width required")
    q=3**r;g=1;d=0
    while 3*g<=coefficient_bound and d+1<r: g*=3;d+=1
    return {"dimension":n,"original_modulus":q,"root_digits":r,"normalized_Gaussian_width":str(alpha),
        "declared_centered_coefficient_bound":coefficient_bound,
        "nonunit_child_possible_within_declared_bound":coefficient_bound>=3 and r>1,
        "first_nonunit_child_root_digits_upper":d,"first_nonunit_child_modulus_upper":g,
        "additional_strict_nonunit_steps_upper_after_first":max(0,d-1),
        "all_proper_fixed_true_root_primitive_failure_union_upper_IF_original_secret_uniform":str(min(Fraction(1),Fraction(max(0,r-1),3**n))),
        "fixed_true_quotient_normalized_width_preserved":True,
        "fixed_true_quotient_laws_share_original_noise_and_are_not_independent":True,
        "adaptively_selected_root_has_unconditioned_Gaussian_law_certified":False,
        "original_primitive_secret_implies_every_high_quotient_primitive":False,
        "same_normalized_width_guarantees_a_distinguisher_at_every_root":False,
        "published_rounded_Gaussian_reduction_applicable_at_all_roots":False,
        "actual_decision_algorithm_or_uniform_conditional_coverage_supplied":False}


def wrong_prefix_census():
    # Complete label population: wrong lower prefix gives a subgroup null, not full uniform.
    q,g,s,x=81,9,5,2;rows=tuple(NoisyLinearRecord((a,),a*s % q,q,f"wrong-prefix:{a}") for a in range(q))
    result=adapt_chain(rows,((9,(9*x,)),),0)
    child=result["steps"][0]["derived_records"];counts=tuple(tuple(sum(c["label"]==(b,) and c["value"]==v for c in child) for v in range(g)) for b in range(g))
    tv=tuple(sum(abs(Fraction(c,9)-Fraction(1,9)) for c in row)/2 for row in counts)
    return {"original_records":tuple(r.public() for r in rows),"supplied_wrong_prefix":x,
        "true_secret_FOR_COUNTERCONTROL_ONLY":s,"chain":result,"conditional_child_value_counts_by_child_label":counts,
        "conditional_TV_from_full_uniform":tuple(str(t) for t in tv),
        "wrong_prefix_implies_full_uniform_child":False,"candidate_or_decision_oracle_created":False}


def control(q,secret,coefficients,errors):
    n=len(secret);labels=tuple(tuple((j+1)*(i+1)+int(j%n==i) for i in range(n)) for j in range(len(errors)))
    original=tuple(NoisyLinearRecord(tuple(a % q for a in row),(sum(a*s for a,s in zip(row,secret))+e) % q,q,f"chain:{q}:{j}") for j,(row,e) in enumerate(zip(labels,errors)))
    currentq=q;currents=secret;hypotheses=[]
    for c in coefficients:
        w=tuple(c*s % currentq for s in currents);hypotheses.append((c,w))
        model=multiple_quotient(currentq,c,w)
        if model.factor==1: break
        currents=tuple(s//model.remaining_modulus for s in currents);currentq=model.factor
    result=adapt_chain(original,hypotheses,max(abs(e) for e in errors))
    return {"original_records":tuple(r.public() for r in original),"supplied_hypotheses_FOR_CALIBRATION_ONLY":tuple(hypotheses),
        "original_secret_FOR_CALIBRATION_ONLY":secret,"original_errors_FOR_CALIBRATION_ONLY":errors,"chain":result,
        "matches_truth_after_solving":result["candidate_secret"]==secret,"actual_multiple_producer_supplied":False}


def build_report():
    deps=("native_basis_lottery.py","native_affine_fibre_relaxation.py","native_small_multiple_completion.py",
        "native_classical_modulus_descent.py","native_gaussian_quotient_completion.py","ternary_covariant_noise.py",
        "ternary_noise_degradation.py","ternary_measured_lattice_decoder.py")
    controls=(control(3**8,(4242,3011),(81,9,1),(13,-7,0,4,-3)),
        control(3**64,(3**63+121,3**61+73,3**62+9),(3**8,3**4,3,1),(3**20,-3**21,0,1,-1,11,-9)))
    return {"status":"EXACT_QUOTIENT_COMPOSITION_AND_RECURSION_COST_AUDIT_REVIEW_PENDING",
        "producer_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "derivation_sha256":hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
        "dependency_sha256":{f:hashlib.sha256((ROOT/"theorems"/f).read_bytes()).hexdigest() for f in deps},
        "actual_chain_calibrations":controls,"wrong_prefix_subgroup_countercontrol":wrong_prefix_census(),
        "source_contract_profiles":tuple(fixed_root_source_contract(n,n,Fraction(1,n**3),n**9) for n in (8,32,128)),
        "ambiguity_profiles":tuple(recursion_cost(n**2,max(1,n.bit_length()-1),"1/8") for n in (8,32,128)),
        "conditional_contract_reference":recursion_cost(2,4,"1/8","7/8"),
        "shared_source_coverage_countercontrol":{"two_disjoint_source_good_events_each_probability":"1/2",
            "their_joint_probability":"0","naive_marginal_product":"1/4","decision_oracle_or_toy_problem_generated":False},
        "published_interface_scope":{"literature_id":"LIT-BTV-2026-SAMPLE-PRESERVING",
            "nonzero_coefficient_is_nonzero_modulo_current_q":True,
            "list_outputs_are_certified_true_pairs":False,"source_average_success_is_uniform_per_instance":False,
            "general_noise_theorem_not_discrete_Gaussian_corollary_required":True},
        "accepted_speedup_candidate":False,"new_active_negative_result_created":False,"actual_quantum_decision_or_multiple_producer":False,
        "complete_recursive_search_to_decision_reduction_established":False,"novelty_claim":False}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("--write",action="store_true");args=parser.parse_args()
    p=build_report()
    if args.write: REPORT.write_text(json.dumps(exact_json(p),indent=2)+"\n")
    print(json.dumps({"status":p["status"],"actual_chain_truth_matches":[c["matches_truth_after_solving"] for c in p["actual_chain_calibrations"]],
        "wrong_prefix_child_TV":p["wrong_prefix_subgroup_countercontrol"]["conditional_TV_from_full_uniform"],
        "recursive_reduction_established":False},indent=2))


if __name__=="__main__": main()
