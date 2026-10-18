"""Vector Z4^n short-mask baseline; exponential sorting time and workspace.

Reuses the scalar balanced-join machinery, NOT cyclic integer group addition.
Local derivation, external review pending; no new sieve exponent or decoder.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import islice, product
import json
from pathlib import Path
from random import Random

from dcp_affine_marked_pairing import affine_hash
from dcp_balanced_pairing import balanced_certificate, block_masks, evaluate_record_join
from theorems.dcp_adaptive_direction_rank_gate import dyadic, integer
from theorems.dcp_affine_fiber_rigidity import matrix


ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"research/phase_workbench/dcp_vector_short_mask_join.json"
CONTRACT=ROOT/"research/hypotheses/dcp_vector_short_mask_join_contract.json"
KIND="VECTOR_Z4_BALANCED_SORT_JOIN"
CONTRACT_ID="vector_Z4_short_mask_balanced_sorting_join_frontier_v1"
RESOURCE_FIELDS=("each_list_length","available_block_supports","padded_records",
                 "one_xor_record_evaluations","one_xor_comparators","one_xor_scan_steps",
                 "six_xor_comparators","persistent_workspace_bits")


def resource(n,m,weight=None,list_length=None):
    integer(n,"vector components",1,512)
    integer(m,"original registers",2,4096)
    # Only GROUP CARDINALITY and key width transfer. The scalar routine's
    # fault fields use a different parameter and must not be inherited.
    C=balanced_certificate(2*n,m,weight,list_length)
    return C, {
        "secret_vector_components":n,"group":"Z4^n with componentwise modular addition",
        "group_cardinality_binary_exponent":2*n,"original_registers":m,
        "per_block_weight":C["per_block_weight"],"physical_mask_width":C["radius"],
        "hash_bits":C["hash_bits"],"public_seed_bits":C["public_seed_bits"],
        "mean_degree":dyadic(C["mean_degree"]),"degree_second_moment":dyadic(C["degree_second_moment"]),
        "native_mean_coarse_coverage_lower_bound":dyadic(C["source_mass_lower"]),
        "mark_probability":dyadic(C["mark_probability"]),
        "counts_hex":{key:hex(C[key]) for key in RESOURCE_FIELDS},
        "record_bits":C["record_bits"],"scan_state_bits":C["scan_state_bits"],
        "full_assignment_table_used":False,"coherent_RAM_assumed":False,
        "polynomial_time_claimed":False,"gate_export_implemented":False,
        "time_form":"O(L*log(L)^2*poly(n,m))","space_form":"O(L*poly(n,m)) coherent basis-wire bits",
    }


def make_program(labels,seed,weight=None,list_length=None):
    A=matrix(labels)
    n,m=len(A),len(A[0])
    C,R=resource(n,m,weight,list_length)
    integer(seed,"unconditioned affine seed",0,(1 << C["public_seed_bits"])-1)
    g=C["hash_bits"]
    return {"kind":KIND,"width":m,"components":n,"descent_bits":2,
            "coarse_labels":[[a%4 for a in row] for row in A],
            "per_block_weight":C["per_block_weight"],"list_length_hex":hex(C["each_list_length"]),
            "hash_rows_hex":[hex((seed >> (j*m))&((1 << m)-1)) for j in range(g)],
            "hash_offset_hex":hex(seed >> (g*m)),"resource_ledger":R,
            "selection_access":"coarse-labels-and-independent-unfiltered-affine-seed",
            "seed_has_been_conditioned_on_success":False,
            "uniform_efficient_program_supplied":False,"table_lookup_is_a_free_coherent_oracle":False}


def validate_program(P):
    if P.get("kind")!=KIND or P.get("descent_bits")!=2:
        raise ValueError("vector Z4 descent program required")
    A=matrix(P["coarse_labels"])
    n,m=len(A),len(A[0])
    if (P["components"]!=n or type(P["components"]) is not int or P["width"]!=m
            or type(P["width"]) is not int or any(a>3 for row in A for a in row)):
        raise ValueError("canonical coarse vector matrix required")
    C,R=resource(n,m,P["per_block_weight"],int(P["list_length_hex"],16))
    H=tuple(int(h,16) for h in P["hash_rows_hex"])
    c=int(P["hash_offset_hex"],16)
    if len(H)!=C["hash_bits"] or any(h<0 or h>=1 << m for h in H) or not 0<=c<1 << len(H):
        raise ValueError("complete unfiltered affine hash seed required")
    if (P.get("resource_ledger")!=R or P.get("seed_has_been_conditioned_on_success") is not False
            or P.get("uniform_efficient_program_supplied") is not False
            or P.get("table_lookup_is_a_free_coherent_oracle") is not False
            or P.get("selection_access")!="coarse-labels-and-independent-unfiltered-affine-seed"):
        raise ValueError("exponential join cost and source-selection lineage cannot be waived")
    return A,C,H,c


def packed_group_value(values):
    """An injective KEY encoding only; never use integer addition on this key."""
    return sum((a%4) << (2*l) for l,a in enumerate(values))


def evaluate_xor(P,x,output=0):
    A,C,H,c=validate_program(P)
    n,m=len(A),len(A[0])
    L,k=C["each_list_length"],C["per_block_weight"]
    if L>4096 or 2*n*m*L>1000000:
        raise ValueError("UNKNOWN: explicit exponential sorting replay work cap")
    def records():
        for side in (0,1):
            for mask in islice(block_masks(side*(m//2),m//2,k),L):
                value=tuple(sum(a*(1-2*(x >> i & 1)) for i,a in enumerate(row) if mask >> i & 1)%4 for row in A)
                if side:
                    value=tuple(-a%4 for a in value)
                key=(packed_group_value(value) << len(H)) | affine_hash(mask,H,0)
                yield key,side,mask
    padding=(1 << (2*n+len(H)),2,0)
    return evaluate_record_join(m,x,output,records,lambda:affine_hash(x,H,c)==0,C,padding)


def propose(P,x):
    row=evaluate_xor(P,x)
    if not row["workspace_clean"]:
        raise ArithmeticError("vector join left nonzero work")
    size=1 << P["width"]
    return row["output"]-size if row["output"]&size else None


def exact_source_census(n,m,weight,list_length):
    C,R=resource(n,m,weight,list_length)
    size,g=1 << m,C["hash_bits"]
    seed_count=1 << C["public_seed_bits"]
    total=4**(n*m)*size*seed_count
    if total>5000000:
        raise ValueError("UNKNOWN: complete natural-source census cap")
    masks=[u|v for u in islice(block_masks(0,m//2,weight),list_length)
           for v in islice(block_masks(m//2,m//2,weight),list_length)]
    marks=[]
    for seed in range(seed_count):
        H=tuple((seed >> (j*m))&(size-1) for j in range(g))
        c=seed >> (g*m)
        marks.append(sum(1 << x for x in range(size) if affine_hash(x,H,c)==0))
    first=second=matched=0
    for flat in product(range(4),repeat=n*m):
        A=tuple(flat[l*m:(l+1)*m] for l in range(n))
        sums=[tuple(sum(a for i,a in enumerate(row) if x >> i & 1)%4 for row in A) for x in range(size)]
        graph=[sum(1 << (x^u) for u in masks if sums[x]==sums[x^u]) for x in range(size)]
        first+=sum(adj.bit_count() for adj in graph)
        second+=sum(adj.bit_count()**2 for adj in graph)
        for selected in marks:
            induced=[adj&selected for adj in graph]
            for x,adj in enumerate(induced):
                if selected >> x & 1 and adj and not adj&(adj-1) and induced[adj.bit_length()-1]==1 << x:
                    matched+=1
    denominator=4**(n*m)*size
    p=Fraction(matched,total)
    if (Fraction(first,denominator)!=C["mean_degree"] or Fraction(second,denominator)!=C["degree_second_moment"]
            or p<C["source_mass_lower"]):
        raise ArithmeticError("vector source moment/isolation bound falsified")
    return {"components":n,"width":m,"weight":weight,"list_length":list_length,
            "all_label_seed_assignments_enumerated":total,
            "sum_unmarked_degrees":first,"sum_squared_unmarked_degrees":second,
            "mutual_unique_marked_assignments":matched,
            "observed_coarse_acceptance_probability":dyadic(p),"resource_ledger":R,
            "uniform_hash_seed_space_rank_or_success_postselected":False}


def finite_control(A,seed,phase_bits=4,weight=None,list_length=None):
    from theorems.dcp_nonlinear_fiber_pairing import compiler_certificate,phase_value
    P=make_program(A,seed,weight,list_length)
    coarse,C,H,c=validate_program(P)
    m,n=P["width"],P["components"]
    if m>8:
        raise ValueError("UNKNOWN: finite full original-assignment diagnostic cap")
    family=[u|v for u in islice(block_masks(0,m//2,P["per_block_weight"]),int(P["list_length_hex"],16))
            for v in islice(block_masks(m//2,m//2,P["per_block_weight"]),int(P["list_length_hex"],16))]
    table=[]
    for x in range(1 << m):
        neighbors=[x^u for u in family if affine_hash(x,H,c)==0 and affine_hash(x^u,H,c)==0
                   and phase_value(coarse,x,4)==phase_value(coarse,x^u,4)]
        row=evaluate_xor(P,x)
        expected=((1 << m)|neighbors[0]) if len(neighbors)==1 else 0
        if row["output"]!=expected or not row["workspace_clean"]:
            raise ArithmeticError("sorting join disagrees with original vector relation")
        for field,key in (("record_evaluations","one_xor_record_evaluations"),
                          ("comparators","one_xor_comparators"),("scan_steps","one_xor_scan_steps")):
            if row[field]!=C[key]:
                raise ArithmeticError("forward/inverse join cost omitted")
        table.append(neighbors[0] if len(neighbors)==1 else None)
    return {"program":P,"all_original_assignments_checked":1 << m,
            "diagnostic_proposal_table_NOT_free_oracle":table,
            "compiler":compiler_certificate(A,phase_bits,2,P),
            "source_selection":"unfiltered seeded finite control, NOT a source probability estimate"}


def frontier(n):
    C,R=resource(n,4*n)
    v=1-Fraction(1,n)
    nonzero=1-Fraction(1,1 << (n*n))
    coarse=C["source_mass_lower"]
    return {"resource_ledger":R,"phase_bits":n+2,"original_visibility":dyadic(v),
            "uniform_higher_label_nonzero_probability":dyadic(nonzero),
            "native_mean_useful_probability_lower_bound":dyadic(coarse*nonzero),
            "native_mean_useful_visibility_lower_bound":dyadic(coarse*nonzero*v**C["radius"]),
            "source_coverage_lower_bound_is_for_each_fixed_A_or_seed":False,
            "favorable_A_or_seed_selection_uncharged":False,
            "abstract_noisy_source_wrapper_may_apply_under_its_separate_premises":True,
            "classical_partner_search_is_a_classical_secret_decoder":False,
            "exponential_recursive_supply_removed":False}


def build_report():
    controls=[finite_control(((1,3),(1,3)),0,3,1,1),
              finite_control(((3,1),(0,3)),0,3,1,1)]
    for seed in range(4):
        rng=Random(7201+seed)
        A=tuple(tuple(rng.randrange(16) for _ in range(8)) for _ in range(2))
        controls.append(finite_control(A,rng.getrandbits(18)))
    return {"contract_id":CONTRACT_ID,"status":"LOCAL_DERIVATION_EXTERNAL_REVIEW_PENDING",
            "accepted_speedup_candidate":False,"novelty_claim":False,"external_theorem_review_complete":False,
            "source_quantum_preparations_executed":0,
            "finite_controls":controls,
            "complete_source_censuses":[exact_source_census(1,4,1,2),exact_source_census(2,2,1,1)],
            "native_short_mask_frontiers":[frontier(n) for n in (8,16,32,64,128)],
            "scope":{
                "relation":"A(y-x)=0 in Z4^n, not one cyclic integer congruence",
                "full_higher_labels_are_program_inputs":False,
                "coarse_only_fresh_higher_label_law_applies_with_fresh_batches":True,
                "sorting_network_gate_export_implemented":False,"coherent_RAM_assumed":False,
                "polynomial_time_or_coherent_space_claimed":False,
                "constant_mean_coverage_and_visibility_implies_scalable_decoder":False,
                "natural_source_noise_or_hardness_certified":False,
                "improves_known_DCP_time_query_tradeoff":False},
            "literature":["https://arxiv.org/abs/1207.2307","https://arxiv.org/abs/2206.14408"]}


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-write",action="store_true")
    args=parser.parse_args(argv)
    report=build_report()
    if not args.no_write:
        REPORT.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"status":report["status"],"finite_controls":6,"source_censuses":2,
                      "native_frontiers":5,"polynomial_time_claimed":False,"artifact":str(REPORT)}))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
