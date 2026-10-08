"""Compressed exact proper-marginal/pair-PSD representation falsifiers.

LOCAL DERIVATION / REVIEW PENDING. These are mathematical proof controls,
not native-source instances, hardness benchmarks or quantum candidates.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import time

from flint import fmpq

from ternary_prefix_integrality import rational
from ternary_moment_psd import certify_psd, verify_ldl

ROOT=Path(__file__).resolve().parents[1]
DERIVATION=ROOT/"research/NATIVE_PROPER_MARGINAL_GAP_DERIVATION.md"
REPORT=ROOT/"research/phase_workbench/ternary_proper_marginal_gap.json"
ODD_SIZES=(5,7,15,31,63)
EVEN_SIZES=(4,6,16,32,64)


def choose(n,h):
    return math.comb(n,h) if 0<=h<=n else 0


def balanced_word_probability(N,k,h):
    if type(N) is not int or N<2 or N%2 or type(k) is not int or not 0<=k<=N or type(h) is not int or not 0<=h<=k:
        raise ValueError("even population and complete valid native k/h coordinates required")
    return fmpq(choose(N-k,N//2-h),math.comb(N,N//2))


def components(M):
    if type(M) is not int or M<4:raise ValueError("native-event size must be an exact integer >=4")
    if M%2:return ((M-1,fmpq(M-2,2*(M-1))),(M+1,fmpq(M,2*(M-1))))
    return ((M,fmpq(1)),)


def word_probability(M,k,h):
    parts=components(M);maximum=M-1 if M%2 else M
    if type(k) is not int or not 0<=k<=maximum or type(h) is not int or not 0<=h<=k:
        raise ValueError("proper odd or full honest-even marginal coordinates required")
    return sum((w*balanced_word_probability(N,k,h) for N,w in parts),fmpq(0))


def sign_matrix(M):
    components(M)
    return tuple(tuple(fmpq(1) if i==j else fmpq(-1,M-1) for j in range(M)) for i in range(M))


def psd_template(M):
    r=fmpq(-1,M-1)
    return {"sign_diagonal":"1","sign_off_diagonal":str(r),"edge_square_weight":str(fmpq(1,M-1)),
        "edge_square_count":math.comb(M,2),"constant_moment":"1","constant_sign_means":"0",
        "indicator_constant_coefficient":"1/2","indicator_sign_coefficients":["-1/2","1/2"],
        "cross_block_same_indicator_probability":str((1+r)/4),
        "cross_block_opposite_indicator_probability":str((1-r)/4),
        "same_block_indicator_diagonal":"1/2","same_block_distinct_indicator_product":"0"}


def verify_psd_template(M, template):
    if template!=psd_template(M):raise ValueError("canonical complete sign/indicator PSD template required")
    # Reconstruct EVERY sign-matrix entry from the positive edge squares,
    # then check the full affine binary-indicator congruence entry by entry.
    weight=rational(template["edge_square_weight"]);gram=[[fmpq(0)]*M for _ in range(M)]
    for i in range(M):
        for j in range(i+1,M):
            gram[i][i]+=weight;gram[j][j]+=weight;gram[i][j]-=weight;gram[j][i]-=weight
    if tuple(tuple(row) for row in gram)!=sign_matrix(M):raise ValueError("edge-square identity must reconstruct the whole matrix")
    a=rational(template["indicator_constant_coefficient"]);signs=tuple(rational(x) for x in template["indicator_sign_coefficients"])
    checks=0
    for i in range(M):
        for j in range(M):
            for s in range(2):
                for t in range(2):
                    value=a*a+signs[s]*signs[t]*gram[i][j]
                    expected=fmpq(1,2) if i==j and s==t else fmpq(0) if i==j else rational(template["cross_block_same_indicator_probability" if s==t else "cross_block_opposite_indicator_probability"])
                    if value!=expected:raise ValueError("native indicator congruence does not match original one-hot pair moments")
                    checks+=1
    return {"edge_squares_checked":math.comb(M,2),"indicator_pair_entries_checked":checks,
        "constant_indicator_entries_checked":2*M+1,"full_indicator_matrix_PSD_proved_by_congruence":True}


def parity_certificate(M):
    if type(M) is not int or M<5 or M%2==0:raise ValueError("odd native parity certificate applies ONLY to odd M>=5")
    constant=(M*M-1)//8;single=-(M-1)//2
    values=[constant+single*h+math.comb(h,2) for h in range(M+1)]
    if any(a<0 or 8*a!=(2*h-M)**2-1 for h,a in enumerate(values)):
        raise ArithmeticError("parity inequality must hold on every odd native Hamming weight")
    value=fmpq(constant)+single*M*fmpq(1,2)+math.comb(M,2)*word_probability(M,2,2)
    if value!=fmpq(-1,8):raise ArithmeticError("expected strict global-native parity obstruction")
    return {"integer_constant":str(constant),"single_indicator_coefficient":str(single),"pair_indicator_coefficient":"1",
        "all_native_hamming_weight_values":[str(x) for x in values],"exact_pair_moment_value":str(value),
        "minimum_native_total_spin_squared":"1","exact_moment_total_spin_squared":"0",
        "proves_no_global_native_distribution":True,"source_hardness_or_quantum_lower_bound_proved":False}


def build_case(M,max_class_records=20_000,max_matrix_cells=20_000):
    parts=components(M);maximum=M-1 if M%2 else M
    if any(type(x) is not int or x<1 for x in (max_class_records,max_matrix_cells)):
        raise ValueError("positive complete class/matrix preflights required")
    count=(maximum+1)*(maximum+2)//2;cells=M*M;start=time.perf_counter()
    cost={"class_records_preflight":count,"class_record_budget":max_class_records,"sign_matrix_cells_preflight":cells,
        "sign_matrix_cell_budget":max_matrix_cells,"native_words_enumerated":0,"LP_calls":0}
    if count>max_class_records or cells>max_matrix_cells:
        return {"M":M,"status":"PROPER_MARGINAL_CONTROL_PREFLIGHT_UNKNOWN","cost":cost,
            "is_source_instance":False,"is_algorithm_candidate":False,"global_nonrealizability_proved":False}
    rows=[];projections=0
    for k in range(maximum+1):
        classes=[];total=fmpq(0)
        for h in range(k+1):
            p=word_probability(M,k,h);multiplicity=math.comb(k,h);mass=multiplicity*p;total+=mass
            if k<maximum:
                if p!=word_probability(M,k+1,h)+word_probability(M,k+1,h+1):raise ArithmeticError("exact marginal projectivity failed")
                projections+=1
            classes.append({"h":h,"word_multiplicity":str(multiplicity),"particular_word_probability":str(p),"Hamming_class_mass":str(mass)})
        if total!=1:raise ArithmeticError("exact class-mass normalization failed")
        rows.append({"k":k,"classes":classes,"exact_normalization":str(total)})
    template=psd_template(M);proof=certify_psd(sign_matrix(M));checks=verify_psd_template(M,template)
    if not proof["ldl"]:raise ArithmeticError("exact pair matrix must be PSD")
    if M%2:
        global_record={"status":"EXACT_GLOBAL_NATIVE_NONREALIZABILITY","parity_certificate":parity_certificate(M),
            "is_global_probability_distribution":False,"all_proper_marginals_projectively_consistent":True}
    else:
        global_record={"status":"EXACT_HONEST_GLOBAL_BALANCED_DISTRIBUTION","balanced_positive_count":M//2,
            "number_of_global_support_words":str(math.comb(M,M//2)),"particular_support_word_probability":str(fmpq(1,math.comb(M,M//2))),
            "is_global_probability_distribution":True,"odd_parity_inequality_applicable":False,
            "balanced_word_countervalue_for_invalid_odd_inequality":"-1/8"}
    cost.update({"class_records_checked":count,"normalizations_checked":maximum+1,"projective_identities_checked":projections,
        "maximum_probability_numerator_bits":max(abs(int(rational(c["particular_word_probability"]).p)).bit_length() for row in rows for c in row["classes"]),
        "maximum_probability_denominator_bits":max(int(rational(c["particular_word_probability"]).q).bit_length() for row in rows for c in row["classes"]),
        **checks,"construction_wall_seconds":time.perf_counter()-start})
    return {"M":M,"status":"EXACT_ODD_PROPER_MARGINAL_PSD_GLOBAL_GAP" if M%2 else "EXACT_EVEN_HONEST_GLOBAL_CONTROL",
        "maximum_marginal_size":maximum,"compressed_probability_semantics":"PER_WORD_AND_MULTIPLICITY_WEIGHTED_CLASS_MASS_DISTINCT",
        "components":[{"population_size":N,"mixture_weight":str(w),"balanced_word_count":str(math.comb(N,N//2))} for N,w in parts],
        "marginal_rows":rows,"sign_mean":"0","off_diagonal_sign_correlation":str(fmpq(-1,M-1)),
        "PSD_sum_of_squares_template":template,"exact_sign_LDL_control":proof,"global_record":global_record,"cost":cost,
        "is_source_instance":False,"is_algorithm_candidate":False,"quantum_speedup_proved":False,
        "population_obstruction_proved":False,"global_nonrealizability_proved":bool(M%2)}


def verify_case(record):
    M=record["M"];parts=components(M);maximum=M-1 if M%2 else M
    if record.get("is_source_instance") is not False or record.get("is_algorithm_candidate") is not False:
        raise ValueError("proper-marginal schemas are NEVER source instances or algorithm candidates")
    if record["status"]=="PROPER_MARGINAL_CONTROL_PREFLIGHT_UNKNOWN":
        cost=record["cost"]
        if record["global_nonrealizability_proved"] or "marginal_rows" in record or not ((maximum+1)*(maximum+2)//2>cost["class_record_budget"] or M*M>cost["sign_matrix_cell_budget"]):
            raise ValueError("whole preflight unknown cannot carry fake probability or nonrealizability proofs")
        return {"valid":True,"unknown_not_proof":True}
    if record["status"]!=("EXACT_ODD_PROPER_MARGINAL_PSD_GLOBAL_GAP" if M%2 else "EXACT_EVEN_HONEST_GLOBAL_CONTROL") or record["maximum_marginal_size"]!=maximum:
        raise ValueError("odd proper versus even global scope must match exact native size")
    if (maximum+1)*(maximum+2)//2>record["cost"]["class_record_budget"] or M*M>record["cost"]["sign_matrix_cell_budget"]:
        raise ValueError("complete proof cannot exceed its declared whole class/matrix budgets")
    if record["compressed_probability_semantics"]!="PER_WORD_AND_MULTIPLICITY_WEIGHTED_CLASS_MASS_DISTINCT":raise ValueError("unambiguous native word/class semantics required")
    expected_parts=[{"population_size":N,"mixture_weight":str(w),"balanced_word_count":str(math.comb(N,N//2))} for N,w in parts]
    if record["components"]!=expected_parts:raise ValueError("complete canonical balanced-population mixture required")
    if len(record["marginal_rows"])!=maximum+1:raise ValueError("every proper/full marginal size must be present")
    if any(type(row["k"]) is not int or row["k"]!=k or len(row["classes"])!=k+1 for k,row in enumerate(record["marginal_rows"])):
        raise ValueError("complete ordered k/h schedule required before projection checks")
    projections=0
    for k,row in enumerate(record["marginal_rows"]):
        if type(row["k"]) is not int or row["k"]!=k or len(row["classes"])!=k+1:raise ValueError("complete ordered k/h schedule required")
        total=fmpq(0)
        for h,c in enumerate(row["classes"]):
            p=rational(c["particular_word_probability"]);mass=rational(c["Hamming_class_mass"])
            if type(c["h"]) is not int or c["h"]!=h or c["word_multiplicity"]!=str(math.comb(k,h)) or p<0 or p!=word_probability(M,k,h) or mass!=math.comb(k,h)*p:
                raise ValueError("per-word probabilities must match exact binomial counts and class masses")
            total+=mass
            if k<maximum:
                following=record["marginal_rows"][k+1]["classes"]
                if p!=rational(following[h]["particular_word_probability"])+rational(following[h+1]["particular_word_probability"]):raise ValueError("exact projective identity violated")
                projections+=1
        if total!=1 or rational(row["exact_normalization"])!=1:raise ValueError("entire native marginal law must normalize exactly")
    p1=record["marginal_rows"][1]["classes"];p2=record["marginal_rows"][2]["classes"]
    mean=rational(p1[1]["particular_word_probability"])-rational(p1[0]["particular_word_probability"])
    corr=rational(p2[0]["particular_word_probability"])+rational(p2[2]["particular_word_probability"])-2*rational(p2[1]["particular_word_probability"])
    if mean!=rational(record["sign_mean"]) or mean!=0 or corr!=rational(record["off_diagonal_sign_correlation"]) or corr!=fmpq(-1,M-1):raise ValueError("all first/pair moments must match proper marginal laws")
    checks=verify_psd_template(M,record["PSD_sum_of_squares_template"]);ldl=record["exact_sign_LDL_control"].get("ldl")
    if not ldl or not verify_ldl(sign_matrix(M),ldl["lower"],ldl["diagonal"])["valid"]:raise ValueError("PSD generator flags cannot replace an exact full factor recheck")
    global_record=record["global_record"]
    if M%2:
        if global_record["status"]!="EXACT_GLOBAL_NATIVE_NONREALIZABILITY" or global_record["is_global_probability_distribution"] or not global_record["all_proper_marginals_projectively_consistent"] or global_record["parity_certificate"]!=parity_certificate(M):
            raise ValueError("odd global gap needs whole native parity evidence, not local infeasibility")
    else:
        if global_record!={"status":"EXACT_HONEST_GLOBAL_BALANCED_DISTRIBUTION","balanced_positive_count":M//2,"number_of_global_support_words":str(math.comb(M,M//2)),"particular_support_word_probability":str(fmpq(1,math.comb(M,M//2))),"is_global_probability_distribution":True,"odd_parity_inequality_applicable":False,"balanced_word_countervalue_for_invalid_odd_inequality":"-1/8"}:
            raise ValueError("even balanced controls must not inherit an invalid odd-global obstruction")
    if record["global_nonrealizability_proved"]!=bool(M%2) or record["quantum_speedup_proved"] or record["population_obstruction_proved"]:raise ValueError("global native/proof-control scope cannot be promoted to quantum/source claims")
    cost=record["cost"];count=(maximum+1)*(maximum+2)//2
    probabilities=[rational(c["particular_word_probability"]) for row in record["marginal_rows"] for c in row["classes"]]
    expected_cost={"class_records_preflight":count,"class_records_checked":count,"sign_matrix_cells_preflight":M*M,"normalizations_checked":maximum+1,"projective_identities_checked":projections,"native_words_enumerated":0,"LP_calls":0,
        "maximum_probability_numerator_bits":max(abs(int(p.p)).bit_length() for p in probabilities),
        "maximum_probability_denominator_bits":max(int(p.q).bit_length() for p in probabilities),**checks}
    if any(cost[k]!=v or (type(v) is int and type(cost[k]) is not int) for k,v in expected_cost.items()):raise ValueError("complete compressed proof-cost ledger required")
    return {"valid":True,"M":M,"class_records_checked":count,"projective_identities_checked":projections,
        "global_native_nonrealizability_proved":bool(M%2),"quantum_or_source_hardness_proved":False}


def build_report():
    cases=[build_case(M) for M in (*ODD_SIZES,*EVEN_SIZES)]
    checks=[verify_case(c) for c in cases]
    return {"status":"EXACT_COMPRESSED_NATIVE_PROPER_MARGINAL_PROOF_CONTROLS_NOT_ALGORITHMS",
        "derivation_sha256":hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),"odd_sizes":list(ODD_SIZES),"even_sizes":list(EVEN_SIZES),
        "cases":cases,"exact_Python_verifier_results":checks,"local_derivation_review_pending":True,"novelty_claim":False,
        "candidate_record_accepted":False,"source_population_gap_proved":False,"quantum_speedup_proved":False}


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("--write",action="store_true");args=parser.parse_args();report=build_report()
    if args.write:REPORT.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"status":report["status"],"odd_gap_controls":len(ODD_SIZES),"honest_even_controls":len(EVEN_SIZES),
        "compressed_class_records":sum(c["cost"]["class_records_checked"] for c in report["cases"]),
        "projective_identities":sum(c["cost"]["projective_identities_checked"] for c in report["cases"]),"native_words_enumerated":0},indent=2))
