"""Native signed-list tree moments and overflow contract; NO receiver supplied.

Two-wise leaf uniformity suffices; arbitrary IID list-oracle assumptions are
not granted. A clean bounded-list quantum program remains a separate task.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import islice, product
import json
from math import comb
from pathlib import Path
from random import Random

from dcp_balanced_pairing import block_masks
from theorems.dcp_adaptive_direction_rank_gate import dyadic, integer


ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"research/phase_workbench/dcp_native_tree_moment_audit.json"
CONTRACT=ROOT/"research/hypotheses/dcp_native_tree_moment_audit_contract.json"
CONTRACT_ID="native_signed_tree_second_moment_and_overflow_contract_v1"


def dimensions(depth,chunk):
    integer(depth,"tree depth",1,8)
    integer(chunk,"component chunk",1,64)
    return 1 << depth,4**chunk,chunk*(depth+1)


def moments(depth,chunk):
    k,L,n=dimensions(depth,chunk)
    value=Fraction(1)
    rows=[dyadic(value)]
    for _ in range(depth):
        value=value*value+Fraction(L-1,L*L)
        rows.append(dyadic(value))
    second=value+1-Fraction(1,L)
    return {"depth":depth,"chunk_components":chunk,"secret_vector_components":n,
            "leaf_count":k,"leaf_list_length_hex":hex(L),"mean_degree":dyadic(Fraction(1)),
            "internal_weight_moment_recurrence":rows,"second_degree_moment":dyadic(second),
            "M_at_most_3_sufficient_size_condition":L>=2*(k-1),
            "M_actually_at_most_3":second<=3,
            "leaf_entries_assumed_mutually_IID":False}


def unit_rank_mod4(rows):
    """Only a zero residual certifies all constraints have unit pivots."""
    A=[list(row) for row in rows]
    if not A or not A[0] or any(len(row)!=len(A[0]) for row in A):
        raise ValueError("nonempty rectangular modular constraint matrix required")
    for row in A:
        for a in row:
            integer(a,"Z4 coefficient",0,3)
    rank=0
    for j in range(len(A[0])):
        pivot=next((i for i in range(rank,len(A)) if A[i][j]&1),None)
        if pivot is None:
            continue
        A[rank],A[pivot]=A[pivot],A[rank]
        inverse=A[rank][j]  # 1 and3 are self-inverse modulo4.
        A[rank]=[a*inverse%4 for a in A[rank]]
        for i in range(len(A)):
            if i!=rank and A[i][j]:
                c=A[i][j]
                A[i]=[(a-c*b)%4 for a,b in zip(A[i],A[rank])]
        rank+=1
    if any(any(row) for row in A[rank:]):
        raise ValueError("UNKNOWN: nonzero even residual; field-rank probability is not justified")
    return rank


def pattern_constraints(depth,shared):
    k,_,_=dimensions(depth,1)
    integer(shared,"shared leaf pattern",0,(1 << k)-1)
    matrices=[]
    for level in list(range(1,depth+1))+[depth]:
        size=1 << level
        rows=[]
        for start in range(0,k,size):
            first=[0]*(2*k)
            second=[0]*(2*k)
            for leaf in range(start,start+size):
                first[leaf]=1
                second[leaf if shared >> leaf & 1 else k+leaf]=1
            rows.extend((first,second))
        matrices.append(rows)
    return matrices


def pattern_census(depth,chunk):
    k,L,n=dimensions(depth,chunk)
    if k>8:
        raise ValueError("UNKNOWN: complete equality-pattern rank replay cap")
    rows=[]
    total=Fraction(0)
    for shared in range(1 << k):
        matrices=pattern_constraints(depth,shared)
        ranks=[unit_rank_mod4(A) for A in matrices]
        redundant=0
        for level in list(range(1,depth+1))+[depth]:
            size=1 << level
            redundant+=sum((shared >> start)&((1 << size)-1)==(1 << size)-1
                           for start in range(0,k,size))
        if sum(ranks)!=2*k-redundant:
            raise ArithmeticError("tree redundancy count disagrees with exact Z4 elimination")
        count=L**k*(L-1)**(k-shared.bit_count())
        probability=Fraction(1,L**sum(ranks))
        term=count*probability
        total+=term
        rows.append({"shared_leaf_mask_hex":hex(shared),"unit_constraint_ranks_by_chunk":ranks,
                     "shared_subtree_and_last_root_redundancies":redundant,
                     "ordered_tuple_pair_count_hex":hex(count),
                     "joint_survival_probability":dyadic(probability),"second_moment_term":dyadic(term)})
    expected=moments(depth,chunk)["second_degree_moment"]
    if dyadic(total)!=expected:
        raise ArithmeticError("native equality-pattern census contradicts compact recurrence")
    return {"depth":depth,"chunk_components":chunk,"patterns":rows,"observed_second_moment":dyadic(total),
            "ranks_are_over_Z4_with_no_even_residual_not_only_F2":True}


def overflow_contract(depth,chunk):
    k,L,n=dimensions(depth,chunk)
    if 2*chunk*k>8192:
        raise ValueError("UNKNOWN: exact rational overflow-ledger work cap")
    Mrecord=moments(depth,chunk)
    value=Mrecord["second_degree_moment"]
    M=Fraction(int(value["numerator_hex"],16),1 << value["denominator_binary_exponent"])
    g=0
    while (1 << g)<4*(M-1):
        g+=1
    theta=Fraction(1,1 << g)
    ceilM=(M.numerator+M.denominator-1)//M.denominator
    cap=256*ceilM*k*L
    delta=Fraction((k-2)*L,cap+1)
    product_bound=M*delta
    if product_bound>=Fraction(1,256):
        raise ArithmeticError("overflow capacity does not justify the Cauchy loss bound")
    original=theta**2-2*theta**3*(M-1)
    loss=theta**2/8 if k>2 else Fraction(0)
    lower=original-loss
    if lower<3*theta**2/8:
        raise ArithmeticError("marking parameter invalidates source lower contract")
    w=next(w for w in range(1,2*chunk+1) if comb(4*chunk,w)>=L)
    visibility=1-Fraction(1,1 << (n.bit_length()-1))
    return {"moment":Mrecord,"hash_bits":g,"affine_mark_probability":dyadic(theta),
            "public_affine_seed_bits":g*(4*chunk*k+1),
            "intermediate_list_capacity_hex":hex(cap),"nonroot_internal_nodes":k-2,
            "overflow_probability_upper_bound_exact_rational":str(delta),
            "M_times_overflow_bound_exact_rational":str(product_bound),
            "original_mutual_isolation_lower":dyadic(original),
            "overflow_marked_mass_loss_upper_surrogate":dyadic(loss),
            "coarse_mass_lower_IF_clean_exact_receiver_contract":dyadic(lower),
            "universal_loose_coarse_lower_IF_receiver_contract":dyadic(3*theta**2/8),
            "default_leaf_block_width":4*chunk,"default_original_registers":4*chunk*k,
            "default_leaf_support_weight":w,"default_full_physical_mask_width":k*w,
            "dyadic_original_visibility_lower_promise":dyadic(visibility),
            "ideal_inverse_dimension_visibility_exact_rational":str(1-Fraction(1,n)),
            "conditional_mean_unfiltered_visibility_lower_IF_receiver_contract":dyadic(lower*visibility**(k*w)),
            "input_phase_bits_for_higher_label_factor":n+2,
            "conditional_mean_useful_visibility_lower_factors_IF_receiver_contract":[
                dyadic(lower),dyadic(visibility**(k*w)),{"one_minus_two_to_negative":n*n}],
            "naive_nonroot_candidate_cell_upper_bound_hex":hex((k-2)*cap*cap),
            "classical_Wagner_expected_kL_bound_used_as_quantum_gate_count":False,
            "clean_bounded_list_receiver_implemented":False,
            "overflow_detection_inspects_affine_mark_seed":False,
            "overflow_independent_of_degree_assumed":False,
            "native_mean_is_before_label_or_syndrome_postselection":True,
            "source_bound_is_pointwise_in_A_or_hash_seed":False}


def filtered_relation(labels,x,leaf_supports,depth,chunk):
    k,L,n=dimensions(depth,chunk)
    A=tuple(tuple(row) for row in labels)
    if len(A)!=n or not A[0] or any(len(row)!=len(A[0]) for row in A):
        raise ValueError("native matrix dimensions must match chunked tree")
    m=len(A[0])
    if n*m>100000 or m>1024:
        raise ValueError("UNKNOWN: finite edge diagnostic work cap")
    for row in A:
        for a in row:
            integer(a,"coarse public label",0,3)
    integer(x,"original assignment",0,(1 << m)-1)
    if len(leaf_supports)!=k:
        raise ValueError("one nonempty support per physical leaf required")
    used=0
    sums=[]
    for u in leaf_supports:
        integer(u,"nonempty physical support",1,(1 << m)-1)
        if used&u:
            raise ValueError("physical leaf blocks must be disjoint")
        used|=u
        sums.append(tuple(sum(a*(1-2*(x >> i & 1)) for i,a in enumerate(row) if u >> i & 1)%4 for row in A))
    current=sums
    for level in range(depth):
        current=[tuple((a+b)%4 for a,b in zip(current[i],current[i+1])) for i in range(0,len(current),2)]
        if any(any(value[level*chunk:(level+1)*chunk]) for value in current):
            return False
    return not any(current[0][depth*chunk:])


def build_report():
    depth,chunk=2,1
    k,L,n=dimensions(depth,chunk)
    rng=Random(7703)
    A=tuple(tuple(rng.randrange(4) for _ in range(16)) for _ in range(n))
    leaves=[list(block_masks(4*j,4,1)) for j in range(k)]
    controls=[]
    for labels,name in ((A,"unfiltered-seeded-native-edge-control"),(((0,)*16,)*n,"all-zero-high-degree-countercontrol")):
        edges=0
        checks=0
        for x in (0,3,17,121,1024,65535):
            for supports in product(*leaves):
                passed=filtered_relation(labels,x,supports,depth,chunk)
                u=sum(supports)
                if passed:
                    if not filtered_relation(labels,x^u,supports,depth,chunk):
                        raise ArithmeticError("zero tree filters are not partner invariant")
                    if any(sum(a*(((x^u) >> i & 1)-(x >> i & 1)) for i,a in enumerate(row))%4 for row in labels):
                        raise ArithmeticError("tree edge does not preserve full coarse vector")
                    edges+=1
                checks+=1
        controls.append({"control_id":name,"depth":depth,"chunk_components":chunk,
                         "coarse_labels":labels,"original_assignments":[0,3,17,121,1024,65535],
                         "leaf_supports_hex":[[hex(u) for u in masks] for masks in leaves],
                         "tuple_tests":checks,"accepted_filtered_edges":edges,
                         "counts_are_native_probability_estimates":False})
    # JSON-native arrays keep provenance comparisons exact.
    for C in controls:
        C["coarse_labels"]=[list(row) for row in C["coarse_labels"]]
    return {"contract_id":CONTRACT_ID,"status":"LOCAL_DERIVATION_RECEIVER_NOT_IMPLEMENTED",
            "accepted_speedup_candidate":False,"novelty_claim":False,"external_theorem_review_complete":False,
            "source_quantum_preparations_executed":0,
            "complete_pattern_rank_censuses":[pattern_census(a,1) for a in (1,2,3)],
            "native_edge_invariance_controls":controls,
            "conditional_overflow_frontiers":[overflow_contract(a,b) for a,b in ((1,1),(2,1),(3,1),(3,4),(4,8),(4,16),(4,32),(4,64))],
            "scope":{"leaf_entries_assumed_mutually_IID":False,"free_list_oracle_or_QRAM":False,
                     "higher_label_useful_factor_requires_fresh_uniform_lifts":True,
                     "silent_truncation_inherits_this_contract":False,"overflow_independent_of_degree_assumed":False,
                     "mathematical_graph_bound_is_an_implemented_receiver":False,
                     "polynomial_time_or_growing_depth_decoder_supplied":False,
                     "actual_natural_source_noise_certified":False},
            "literature":["https://people.eecs.berkeley.edu/~daw/papers/genbday.html","https://arxiv.org/abs/2410.06856"]}


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-write",action="store_true")
    args=parser.parse_args(argv)
    report=build_report()
    if not args.no_write:
        REPORT.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"status":report["status"],"pattern_censuses":3,"conditional_frontiers":8,
                      "coherent_receiver_implemented":False,"artifact":str(REPORT)}))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
