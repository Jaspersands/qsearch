"""Source-refresh algebra, exact entropy censuses and common-energy budgets.

Supplied integer dithers are not a certified Gaussian sampler. No actual
decision mechanism, coverage contract, source law or quantum speedup is supplied.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
from itertools import product
import json
from pathlib import Path

from native_basis_lottery import original_bank
from native_affine_fibre_relaxation import canonical_vector
from native_classical_modulus_descent import digest
from native_gaussian_quotient_completion import nearest_odd_division
from native_small_multiple_completion import _rational
from ternary_covariant_noise import root_digits
from ternary_noise_degradation import NoisyLinearRecord
from ternary_measured_lattice_decoder import integer, exact_json

ROOT=Path(__file__).resolve().parents[1]
DERIVATION=ROOT/"research/NATIVE_SOURCE_REFRESH.md"
REPORT=ROOT/"research/reductions/native_source_refresh.json"


def label_quality_ledger(n,d,m,k,eta_label):
    for x,name in ((n,"dimension"),(d,"root digits"),(m,"original rows"),(k,"output rows")):
        integer(x,"positive "+name,1)
    eta=_rational(eta_label)
    if not 0<eta<1: raise ValueError("positive subunit label tolerance required")
    if n*d>65536: raise ValueError("complete label population bit scope exceeded")
    N=3**(n*d);factor=Fraction(k*k,4)/eta**2
    # Upward population/factor bits certify a bound without expanding2^m.
    population_bits=(N-1).bit_length()
    factor_exponent=factor.numerator.bit_length()-(factor.denominator.bit_length()-1)
    exponent=population_bits+factor_exponent-m
    upper=Fraction(1,2**min(64,max(0,-exponent)))
    exact=Fraction(N-1,2**m) if m<=2048 and n*d<=2048 else None
    return {"dimension":n,"root_digits":d,"original_rows":m,"output_rows":k,
        "batch_label_TV_tolerance":str(eta),"label_population_base3_exponent":n*d,
        "nonzero_population_ceil_log2_upper":population_bits,
        "Markov_chi_square_factor":str(factor),"factor_power2_exponent_upper":factor_exponent,
        "label_quality_failure_power2_exponent_upper":exponent,
        "label_quality_failure_upper":str(upper),
        "exact_expected_chi_square_IF_small":None if exact is None else str(exact),
        "expected_chi_square_formula":"(g^n-1)/2^m",
        "IID_uniform_original_label_rows_required":True,"sign_difference2_is_a_ring_unit":True,
        "one_observed_full_rank_bank_quality_certified":False,
        "rows_from_reused_parent_are_new_original_samples":False}


def source_ledger(n,r,m,k,dmin,dmax,alpha_original,alpha_target,eta_label,eta_noise,
                  ideal_producer_success=None,sampler_TV_loss=None):
    integer(r,"positive original root digits",1)
    integer(dmin,"positive minimum supported root",1);integer(dmax,"positive maximum supported root",1)
    if not dmin<=dmax<=r: raise ValueError("complete reachable root interval required")
    a,b,el,en=map(_rational,(alpha_original,alpha_target,eta_label,eta_noise))
    if not all(0<x<1 for x in (a,b,el,en)) or el+en>=1:
        raise ValueError("positive subunit widths and useful total TV tolerances required")
    label=label_quality_ledger(n,dmax,m,k,el);D=dmax-dmin+1
    label_failure=min(Fraction(1),D*Fraction(label["label_quality_failure_upper"]))
    rounding=Fraction(m,2*3**(2*dmin));threshold=(en**2*b**2/(4*k)-rounding)/2
    expected_energy=m*a*a/6
    noise_failure=min(Fraction(1),expected_energy/threshold) if threshold>0 else Fraction(1)
    source_failure=min(Fraction(1),label_failure+noise_failure)
    primitive=Fraction(1,3**n);p=None if ideal_producer_success is None else _rational(ideal_producer_success)
    delta=None if sampler_TV_loss is None else _rational(sampler_TV_loss)
    if any(x is not None and not 0<=x<=1 for x in (p,delta)): raise ValueError("valid external producer/sampler bounds required")
    success=None if p is None or delta is None else max(Fraction(0),p-el-en-primitive-delta)
    return {"dimension":n,"original_root_digits":r,"original_rows":m,"output_rows":k,
        "minimum_supported_root_digits":dmin,"maximum_supported_root_digits":dmax,
        "normalized_original_Gaussian_width":str(a),"normalized_target_Gaussian_width":str(b),
        "batch_label_TV_tolerance":str(el),"batch_noise_TV_tolerance":str(en),
        "target_width_multiplier":str(b/a),"maximum_root_label_quality_ledger":label,
        "reachable_fixed_roots_covered":D,"all_reachable_label_quality_failure_upper":str(label_failure),
        "normalized_rounding_energy_floor_upper":str(rounding),
        "common_continuous_original_energy_threshold":str(threshold),
        "true_original_continuous_energy_expectation_upper_using_pi_gt3":str(expected_energy),
        "common_original_energy_failure_upper":str(noise_failure),
        "all_reachable_source_quality_failure_upper":str(source_failure),
        "common_energy_event_is_nonvacuous":threshold>0 and noise_failure<1,
        "uniform_to_primitive_masked_secret_TV":str(primitive),
        "ideal_target_source_producer_success_lower_EXTERNAL":None if p is None else str(p),
        "certified_complete_dither_sampler_TV_loss_EXTERNAL":None if delta is None else str(delta),
        "one_refresh_coverage_lower_IF_quality_and_external_contracts_hold":None if success is None else str(success),
        "one_refresh_unconditional_coverage_lower_IF_source_and_external_contracts_hold":None if success is None else str((1-source_failure)*success),
        "original_noise_independence_required_for_energy_Markov_bound":False,
        "sign_sum_error_and_label_independence_assumed":False,
        "only_true_original_prefixes_covered":True,
        "same_narrow_width_producer_advantage_inherited":False,
        "actual_source_law_quality_sampler_or_producer_certified":False,
        "coefficient_ambiguity_or_false_prefix_pruning_resolved":False}


def canonical_quotient_node(records,scale,prefix):
    """Actual same-original child records; node equality does not certify truth."""
    raw=original_bank(records);q=raw[0].modulus;n=len(raw[0].label)
    integer(scale,"positive original cumulative scale",1)
    if scale!=1: root_digits(scale)
    if q % scale or scale>=q: raise ValueError("nonterminal scale dividing the original root required")
    prefix=canonical_vector(prefix,n,scale);g=q//scale
    node={"original_records_sha256":digest(tuple(r.public() for r in raw)),"modulus":g,
        "original_scale":scale,"known_original_lower_prefix_IF_path_true":prefix}
    children=[];receipts=[]
    for row in raw:
        residual=(row.value-sum(a*x for a,x in zip(row.label,prefix))) % q
        child=NoisyLinearRecord(tuple(a % g for a in row.label),nearest_odd_division(residual,scale) % g,g,row.source_id)
        children.append(child.public());receipts.append({"source_id":row.source_id,
            "original_record_sha256":digest(row.public()),"corrected_original_response":residual,"derived_record":child.public()})
    return {"canonical_node":node,"canonical_node_sha256":digest(node),"derived_records":tuple(children),
        "record_receipts":tuple(receipts),"original_records_paid_once":len(raw),
        "original_response_rounding_evaluations":len(raw),"source_IDs_preserved":True,
        "true_prefix_or_noise_law_certified":False,"new_original_samples_created":False}


def refresh_node(records,g,prefix,signs,mask,dithers,max_entries=2000000):
    raw=original_bank(records);q=raw[0].modulus;n=len(raw[0].label);m=len(raw)
    root_digits(g);integer(max_entries,"positive whole transform entry cap",1)
    if q % g: raise ValueError("actual original quotient root required")
    L=q//g;prefix=canonical_vector(prefix,n,L)
    mask=canonical_vector(mask,n,g);signs=tuple(tuple(row) for row in signs);dithers=tuple(dithers)
    if not signs or len(dithers)!=len(signs) or any(len(row)!=m or any(type(t) is not int or t not in (-1,1) for t in row) for row in signs):
        raise ValueError("complete actual sign rows and supplied integer dithers required")
    if any(type(e) is not int for e in dithers): raise ValueError("exact supplied integer dithers required")
    k=len(signs);entries=m*n+k*m+k*n
    base={"original_records_sha256":digest(tuple(r.public() for r in raw)),"original_records_paid_once":m,
        "modulus":g,"original_scale":L,"known_original_lower_prefix_IF_true":prefix,
        "supplied_sign_rows":signs,"supplied_secret_mask":mask,"supplied_integer_dithers":dithers,
        "planned_transform_entries":entries,"max_entries":max_entries,
        "derived_original_record_count":0,"original_response_rounding_evaluations":0,
        "sign_label_accumulation_terms":0,"sign_response_accumulation_terms":0,"mask_dot_product_terms":0,
        "producer_input":None,"original_quotient_receipts":(),"output_receipts":(),
        "source_quality_or_true_prefix_established":False,
        "supplied_dithers_certified_Gaussian":False,"signs_and_mask_certified_IID_uniform":False,
        "fresh_public_randomness_is_a_fresh_original_sample":False,
        "actual_producer_or_quantum_algorithm_supplied":False}
    if entries>max_entries: return {**base,"status":"WHOLE_REFRESH_TRANSFORM_CAP_EXCEEDED_NOT_SOURCE_FAILURE"}
    canonical=canonical_quotient_node(raw,L,prefix)
    derived=tuple(NoisyLinearRecord(**r) for r in canonical["derived_records"]);receipts=canonical["record_receipts"]
    labels=[];values=[];outputs=[]
    for index,(sign,e) in enumerate(zip(signs,dithers)):
        label=tuple(sum(t*r.label[j] for t,r in zip(sign,derived)) % g for j in range(n))
        response=sum(t*r.value for t,r in zip(sign,derived)) % g
        shift=sum(a*z for a,z in zip(label,mask)) % g;value=(response+e-shift) % g
        labels.append(label);values.append(value)
        outputs.append({"output_index":index,"ALL_original_source_IDs":tuple(r.source_id for r in raw),
            "signed_parent_response_modulus":response,"mask_response_shift":shift,
            "supplied_integer_dither":e,"output_label":label,"output_response":value})
    return {**base,"status":"ACTUAL_SIGN_MASK_TRANSFORM_WITH_UNCERTIFIED_EXTERNAL_DITHERS",
        "derived_original_record_count":m,"original_response_rounding_evaluations":m,
        "sign_label_accumulation_terms":k*m*n,"sign_response_accumulation_terms":k*m,"mask_dot_product_terms":k*n,
        "producer_input":{"modulus":g,"labels":tuple(labels),"responses":tuple(values)},
        "original_quotient_receipts":tuple(receipts),"output_receipts":tuple(outputs),
        "producer_input_contains_signs_mask_prefix_or_source_metadata":False}


def sign_census(n,d,m,max_work=100000):
    for x,name in ((n,"dimension"),(d,"root digits"),(m,"original rows"),(max_work,"complete census cap")):
        integer(x,"positive "+name,1)
    q=3**d;N=q**n;work=N**m*2**m*m*n
    if work>max_work: raise ValueError("complete original-matrix/sign census cap exceeded")
    labels=tuple(product(range(q),repeat=n));signs=tuple(product((-1,1),repeat=m));chi=Fraction(0);tv=Fraction(0);zero_tv=None
    distributions=Counter()
    for rows in product(labels,repeat=m):
        counts=Counter(tuple(sum(t*a[j] for t,a in zip(sign,rows)) % q for j in range(n)) for sign in signs)
        c=Fraction(N*sum(v*v for v in counts.values()),4**m)-1
        t=(sum(abs(Fraction(counts[a],2**m)-Fraction(1,N)) for a in labels))/2
        chi+=c;tv+=t;distributions[str(t)]+=1
        if all(not any(a) for a in rows): zero_tv=t
    banks=N**m;mean_chi=chi/banks;mean_tv=tv/banks;expected=Fraction(N-1,2**m)
    if mean_chi!=expected or mean_tv**2>mean_chi/4: raise ArithmeticError("complete sign collision identity or TV bound failed")
    return {"dimension":n,"root_digits":d,"original_rows":m,"original_matrices_checked":banks,
        "sign_rows_per_matrix":2**m,"complete_label_accumulation_terms":work,
        "exact_mean_chi_square":str(mean_chi),"theoretical_exact_mean_chi_square":str(expected),
        "exact_mean_conditional_label_TV":str(mean_tv),"zero_matrix_conditional_TV":str(zero_tv),
        "conditional_TV_histogram":dict(sorted(distributions.items())),
        "all_source_matrices_individually_uniform_claimed":False,
        "finite_census_is_a_new_oracle_problem_or_candidate":False}


def control():
    q=3**16;g=81;L=q//g;s=(3**15+17123,3**14+28114);errors=(L+2,-L-1,0,4,-3)
    raw=tuple(NoisyLinearRecord((j+2,3*j+1),((j+2)*s[0]+(3*j+1)*s[1]+e) % q,q,f"refresh-original:{j}") for j,e in enumerate(errors))
    prefix=tuple(x % L for x in s);mask=(17,25);signs=((-1,1,-1,1,-1),(1,1,-1,-1,1),(-1,-1,1,1,1));dithers=(3,-2,1)
    return {"original_records":tuple(r.public() for r in raw),"secret_AND_original_errors_FOR_CALIBRATION_ONLY":{"secret":s,"errors":errors},
        "transform":refresh_node(raw,g,prefix,signs,mask,dithers),
        "Gaussian_dithers_or_uniform_signs_mask_claimed":False}


def build_report():
    profiles=[]
    for n in (8,32,128):
        dmin=dmax=1
        while 3**dmin<n**7: dmin+=1
        while 3**(dmax+1)<=n**9 and dmax+1<=n: dmax+=1
        if dmin>dmax:
            profiles.append({"dimension":n,"status":"NO_DECLARED_ROOT_INTERVAL_ABOVE_ROUNDING_FLOOR",
                "required_minimum_root_digits":dmin,"available_maximum_root_digits":dmax});continue
        k=n*9*n.bit_length();m=n**3
        for power in (3,9,16):
            profiles.append(source_ledger(n,n,m,k,dmin,dmax,Fraction(1,n**power),Fraction(1,n),Fraction(1,n**3),Fraction(1,n**3)))
    deps=("native_basis_lottery.py","native_affine_fibre_relaxation.py","native_classical_modulus_descent.py",
        "native_gaussian_quotient_completion.py","native_small_multiple_completion.py","ternary_covariant_noise.py",
        "ternary_noise_degradation.py","ternary_measured_lattice_decoder.py")
    calibration=control();raw=tuple(NoisyLinearRecord(**r) for r in calibration["original_records"]);f=calibration["transform"]
    wrong=tuple((x+1) % f["original_scale"] for x in f["known_original_lower_prefix_IF_true"])
    alias=refresh_node(raw,f["modulus"],wrong,f["supplied_sign_rows"],f["supplied_secret_mask"],f["supplied_integer_dithers"])
    return {"status":"SOURCE_REFRESH_ALGEBRA_ENTROPY_AND_COMMON_ENERGY_AUDIT_SAMPLER_AND_PRODUCER_MISSING",
        "producer_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),"derivation_sha256":hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
        "dependency_sha256":{f:hashlib.sha256((ROOT/"theorems"/f).read_bytes()).hexdigest() for f in deps},
        "actual_supplied_dither_control":calibration,
        "false_prefix_calibration_alias":{"transform":alias,"same_producer_input":alias["producer_input"]==f["producer_input"],
            "same_input_certifies_true_prefix":False,"finite_alias_is_general_source_or_no_go":False},
        "complete_sign_collision_censuses":(sign_census(1,2,3),sign_census(2,1,3)),
        "width_and_root_scope_profiles":profiles,"source_refresh_sampler_implemented":False,
        "source_conditioned_producer_amplification_established":False,
        "accepted_speedup_candidate":False,"new_active_negative_result_created":False,"novelty_claim":False}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("--write",action="store_true");args=parser.parse_args();p=build_report()
    if args.write: REPORT.write_text(json.dumps(exact_json(p),indent=2)+"\n")
    print(json.dumps({"status":p["status"],"censused_original_matrices":sum(c["original_matrices_checked"] for c in p["complete_sign_collision_censuses"]),
        "nonvacuous_common_energy_profiles":sum(s.get("common_energy_event_is_nonvacuous",False) for s in p["width_and_root_scope_profiles"]),
        "actual_Gaussian_sampler_or_producer_supplied":False},indent=2))


if __name__=="__main__": main()
