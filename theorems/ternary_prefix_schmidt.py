"""Native prefix-measurement Schmidt spectrum and source-weighted MPS audit.

LOCAL DERIVATION / REVIEW PENDING. A fixed-cut explicit low-bond simulation
obstruction is NOT quantum hardness or a bound on other tensor geometries,
adaptive word partitions, or observable-only approximations.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
from itertools import product
import json
import math
from pathlib import Path

import numpy as np

from ternary_coherent_edge_receiver import NativeEdgeProgram, _jsonable, digits
from ternary_covariant_noise import phase
from ternary_cyclic_extractor import _integer, random_even_source

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"research/phase_workbench/ternary_prefix_schmidt.json"
DERIVATION=ROOT/"research/TERNARY_PREFIX_SCHMIDT.md"


def purity_certificate(n,r,prefix_digits,split,chi=1):
    for x,name,minimum in ((n,"dimension",1),(r,"root digits",1),(prefix_digits,"prefix digits",0),(split,"fixed split",1),(chi,"bond cap",1)):
        _integer(x,name,minimum)
    M=n*r-2
    if not 1<=split<M or not 0<=prefix_digits<=r:
        raise ValueError("nontrivial fixed word split and legal prefix depth required")
    L,R=3**split,3**(M-split);D=L*R;H=3**(n*prefix_digits);mu=Fraction(D,H)
    collision_factor=(1+Fraction(L-1,H))*(1+Fraction(R-1,H))
    bad=min(Fraction(1),2*(1-Fraction(1,H))/mu)
    good=2*collision_factor/mu
    purity=min(Fraction(1),bad+good)
    minimum_bond=math.ceil(Fraction(81,100)/purity)
    return {"dimension":n,"root_digits":r,"source_qutrits":M,"prefix_digits":prefix_digits,"fixed_left_width":split,
        "left_words":str(L),"right_words":str(R),"prefix_group_size":str(H),"native_words":str(D),
        "mean_uniform_target_fiber_size":mu,"uniform_target_fiber_variance":mu*(1-Fraction(1,H)),
        "independent_half_collision_factor":collision_factor,
        "mean_Born_mass_of_fibers_below_half_mean_upper":bad,
        "mean_purity_good_sector_upper":good,"mean_Born_weighted_Schmidt_purity_upper":purity,
        "mean_bond_budget":chi,"mean_squared_overlap_upper_squared":min(Fraction(1),chi*purity),
        "necessary_bond_for_mean_squared_overlap_ge_nine_tenths":str(minimum_bond),
        "mean_Renyi2_entropy_bits_lower_diagnostic":math.log2(purity.denominator)-math.log2(purity.numerator),
        "source_law":"ALL_IID_ORIGINAL_NATIVE_LABELS_AND_ACTUAL_PREFIX_BORN_MEASUREMENTS",
        "secret_scope":"EVERY_FIXED_SECRET; SCHMIDT_WEIGHTS_INDEPENDENT_OF_SECRET",
        "partition_scope":"FIXED_PUBLIC_WORD_SPLIT_INDEPENDENT_OF_RANDOM_LABELS",
        "low_bond_full_state_fidelity_scope_only":True,"adaptive_label_partition_covered":False,
        "label_outcome_dependent_bond_allocation_covered_by_mean_cost_bound":True,
        "general_tensor_network_or_quantum_no_go":False,"quantum_speedup_proved":False,
        "large_word_space_executed":False}


def _half_values(source,start,width):
    return [tuple(sum(source.frequencies[start+i][d-1][j] if d else 0 for i,d in enumerate(digits(x,width)))%source.modulus
                  for j in range(source.dimension)) for x in range(3**width)]


def branch_record(left_counts,right_counts,target,modulus,D,chi):
    weights=[]
    for z,a in sorted(left_counts.items()):
        partner=tuple((y-x)%modulus for y,x in zip(target,z));b=right_counts.get(partner,0)
        if b:weights.append({"left_syndrome":z,"right_syndrome":partner,"integer_weight":str(a*b)})
    C=sum(int(w["integer_weight"]) for w in weights)
    if not C:return {"target":target,"status":"EMPTY_PHYSICAL_BRANCH","fiber_size":"0","Born_probability":"0",
                     "Schmidt_integer_weights":[],"conditional_purity":None,"conditional_best_rank_chi_squared_overlap":None}
    numbers=[int(w["integer_weight"]) for w in weights]
    return {"target":target,"status":"EXACT_NATIVE_PREFIX_SCHMIDT_BRANCH","fiber_size":str(C),"Born_probability":Fraction(C,D),
        "Schmidt_integer_weights":weights,"Schmidt_rank":len(weights),"conditional_purity":Fraction(sum(w*w for w in numbers),C*C),
        "conditional_best_rank_chi_squared_overlap":Fraction(sum(sorted(numbers,reverse=True)[:chi]),C)}


def classical_prefix_sample(program,prefix_digits,rng):
    _integer(prefix_digits,"prefix digits",0)
    if prefix_digits>program.source.level//2:
        raise ValueError("prefix cannot exceed native root")
    word=tuple(rng.randrange(3) for _ in range(program.width))
    target=tuple(x%3**prefix_digits for x in program.source.value(word))
    return {"prefix_outcome":target,"known_native_rows_evaluated":program.width,
            "query_model":"EXPLICIT_PUBLIC_NATIVE_LABEL_ARITHMETIC",
            "unknown_secret_used":False,"coherent_conditioned_phase_state_produced":False,
            "reproduces_prefix_outcome_law_only":True}


def prefix_control(program,prefix_digits,split,chi=1):
    s=program.source;certificate=purity_certificate(s.dimension,s.level//2,prefix_digits,split,chi)
    L,R,D,H=map(int,(certificate["left_words"],certificate["right_words"],certificate["native_words"],certificate["prefix_group_size"]))
    if L+R>2000 or H>300 or D>10000:
        raise ValueError("complete prefix-count diagnostic preflight exceeded; no partial classification")
    Q=3**prefix_digits
    left=_half_values(s,0,split);right=_half_values(s,split,s.inputs-split)
    cL=Counter(tuple(x%Q for x in row) for row in left);cR=Counter(tuple(x%Q for x in row) for row in right)
    targets=list(product(range(Q),repeat=s.dimension))
    records=[branch_record(cL,cR,target,Q,D,chi) for target in targets]
    norm=sum((Fraction(row["Born_probability"]) for row in records),Fraction(0))
    if norm!=1:raise ArithmeticError("all actual prefix Born probabilities must sum to one")
    purity=sum((Fraction(row["Born_probability"])*row["conditional_purity"] for row in records if row["conditional_purity"] is not None),Fraction(0))
    fidelity=sum((Fraction(row["Born_probability"])*row["conditional_best_rank_chi_squared_overlap"] for row in records if row["conditional_purity"] is not None),Fraction(0))
    if fidelity*fidelity>chi*purity:raise ArithmeticError("source-weighted rank/fidelity Cauchy-Schwarz bound failed")
    return {"prefix_digits":prefix_digits,"fixed_left_width":split,"bond_cap":chi,"complete_branches":records,
        "left_syndrome_counts":[{"syndrome":z,"count":str(c)} for z,c in sorted(cL.items())],
        "right_syndrome_counts":[{"syndrome":z,"count":str(c)} for z,c in sorted(cR.items())],
        "Born_probability_sum":norm,"Born_weighted_purity":purity,"Born_weighted_best_rank_chi_squared_overlap":fidelity,
        "half_words_enumerated":L+R,"full_native_words_enumerated_for_counts":0,
        "all_branch_classification_not_population_estimate":True}


def physical_control(program,prefix_digits,split,target,secret):
    s=program.source;cert=purity_certificate(s.dimension,s.level//2,prefix_digits,split)
    L,R,D=map(int,(cert["left_words"],cert["right_words"],cert["native_words"]));Q=3**prefix_digits
    target=tuple(target);secret=tuple(secret)
    if D>10000 or len(target)!=s.dimension or any(type(x) is not int or not 0<=x<Q for x in target):
        raise ValueError("bounded dense replay and canonical prefix target required")
    if len(secret)!=s.dimension or any(type(x) is not int or not 0<=x<s.modulus for x in secret):
        raise ValueError("canonical full secret only for calibration required")
    left=_half_values(s,0,split);right=_half_values(s,split,s.inputs-split)
    pL=np.array([phase(sum(a*v for a,v in zip(row,secret)),s.modulus) for row in left])
    pR=np.array([phase(sum(a*v for a,v in zip(row,secret)),s.modulus) for row in right])
    mask=np.array([[all((a+b)%Q==y for a,b,y in zip(u,v,target)) for v in right] for u in left])
    C=int(mask.sum())
    if not C:return {"target":target,"calibration_secret_only":secret,"status":"EMPTY_PHYSICAL_BRANCH","Born_probability":"0"}
    matrix=np.outer(pL,pR)*mask/math.sqrt(C)
    observed=sorted((float(v*v) for v in np.linalg.svd(matrix,compute_uv=False)),reverse=True)
    cL=Counter(tuple(x%Q for x in row) for row in left);cR=Counter(tuple(x%Q for x in row) for row in right)
    record=branch_record(cL,cR,target,Q,D,1)
    predicted=sorted([float(Fraction(w["integer_weight"])/C) for w in record["Schmidt_integer_weights"]],reverse=True)
    predicted+=[0.]*(min(L,R)-len(predicted))
    return {"target":target,"calibration_secret_only":secret,"status":"NATIVE_PREFIX_PROJECTOR_DENSE_SCHMIDT_REPLAY",
        "Born_probability":Fraction(C,D),"observed_squared_singular_values":observed,
        "predicted_squared_singular_values":predicted,"spectrum_residual":max(abs(a-b) for a,b in zip(observed,predicted)),
        "matrix_norm_residual":abs(float(np.sum(abs(matrix)**2))-1),
        "unknown_secret_used_in_receiver_recipe":False,"dense_calibration_cells":D}


def low_label_census():
    # n1/r4/M2, d1: exhaust the entire IID low-row law, not selected full labels.
    total_variance=Fraction(0);collisions=0;purity=Fraction(0)
    for a,c,b,e in product(range(3),repeat=4):
        L=Counter((x,) for x in (0,a,c));R=Counter((x,) for x in (0,b,e))
        rows=[branch_record(L,R,(y,),3,9,1) for y in range(3)]
        total_variance+=sum((Fraction((int(row["fiber_size"])-3)**2,3) for row in rows),Fraction(0))
        collisions+=sum(x*x for x in L.values())*sum(x*x for x in R.values())
        purity+=sum((Fraction(row["Born_probability"])*row["conditional_purity"] for row in rows if row["conditional_purity"] is not None),Fraction(0))
    if total_variance/81!=2 or Fraction(collisions,81)!=25:raise ArithmeticError("entire IID prefix law must match analytical moments")
    return {"complete_IID_low_label_cases":81,"prefix_targets_per_case":3,"uniform_target_variance":total_variance/81,
        "independent_half_collision_product_mean":Fraction(collisions,81),"Born_weighted_purity_mean":purity/81,
        "IID_full_root_lifts_preserve_this_low_law":True,"not_a_quantum_candidate":True}


def build_report():
    certs=[purity_certificate(n,r,d,split,(n*r)**2) for n,r,d,split in ((1,16,7,7),(1,32,15,15),(1,64,31,31),(2,16,7,15))]
    cases=[]
    for n,r,d,split,seed in ((1,8,3,3,99501),(1,10,4,4,99502),(2,4,1,3,99503)):
        source=random_even_source(n,2*r,n*r-2,seed);p=NativeEdgeProgram(source)
        controls=[]
        for k in ((0,d,r-1) if n==1 else (0,d,2)):
            if 3**(n*k)>300:
                controls.append({"status":"WHOLE_PREFIX_DIAGNOSTIC_PREFLIGHT_UNKNOWN","prefix_digits":k,
                                 "prefix_group_size":str(3**(n*k)),"complete_target_budget":300,
                                 "classification_complete":False,"Born_weighted_purity":None})
            else:controls.append(prefix_control(p,k,split,2))
        cases.append({"dimension":n,"root_digits":r,"seed":seed,"native_labels":source.labels,"full_frequencies":source.frequencies,
            "count_controls":controls,"physical_controls":[physical_control(p,d,split,target,secret)
                for target in ((0,)*n,(1,)*n,(3**d-1,)*n) for secret in ((0,)*n,(3,)*n,(source.modulus-1,)*n)]})
    return _jsonable({"status":"SOURCE_WEIGHTED_NATIVE_PREFIX_SCHMIDT_AUDIT_NOT_QUANTUM_HARDNESS",
        "derivation_sha256":hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),"population_certificates":certs,
        "complete_low_label_census":low_label_census(),"prespecified_native_cases":cases,
        "local_derivation_review_pending":True,"novelty_claim":False,"candidate_record_accepted":False,
        "quantum_speedup_proved":False,"generic_quantum_or_tensor_network_lower_bound":False,
        "classical_prefix_outcome_law_exactly_reproduced":True,
        "prefix_outcomes_depend_on_unknown_secret":False,
        "classical_sampler_prepares_coherent_conditioned_state":False})


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("--write",action="store_true");args=parser.parse_args();report=build_report()
    if args.write:REPORT.write_text(json.dumps(report,indent=2,allow_nan=False)+"\n")
    print(json.dumps({"status":report["status"],"population_certificates":len(report["population_certificates"]),
        "native_cases":len(report["prespecified_native_cases"]),"quantum_speedup_proved":False},indent=2))
