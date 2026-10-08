"""Clean native affine-line extractor and exact random-label coverage gate.

LOCAL DERIVATION / REVIEW PENDING. Supplied-direction arithmetic is cheap;
its typical success probability, not a demonstration, is the central test.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
from itertools import product
import json
from math import comb
from pathlib import Path

import numpy as np

from cyclotomic_fiber_receiver import inverse_frequency_coordinates,native_source
from ternary_batch_fiber_compiler import BatchFiberProgram,integer,pointed_minor
from ternary_cyclic_extractor import random_even_source

ROOT=Path(__file__).resolve().parents[1]
NOTE=ROOT/"research/TERNARY_AFFINE_LINE_EXTRACTOR.md"
REPORT=ROOT/"research/phase_workbench/ternary_affine_line_extractor.json"


def rank(rows):
    if not rows:return 0
    width=len(rows[0])
    if any(len(row)!=width for row in rows):raise ValueError("rectangular field matrix required")
    a=[[x%3 for x in row] for row in rows];r=0
    for col in range(width):
        pivot=next((i for i in range(r,len(a)) if a[i][col]),None)
        if pivot is None:continue
        a[r],a[pivot]=a[pivot],a[r];scale=a[r][col];a[r]=[x*scale%3 for x in a[r]]
        for i in range(len(a)):
            if i!=r:
                factor=a[i][col];a[i]=[(x-factor*y)%3 for x,y in zip(a[i],a[r])]
        r+=1
        if r==len(a):break
    return r


def quadratic_rows(source):
    BatchFiberProgram(source,1)
    return tuple(tuple(tuple((pair[1][j]-pair[0][j])%3 if k==0 else (2*pair[0][j]-pair[1][j])%3 for pair in source.frequencies) for j in range(source.dimension)) for k in range(2))


def direction(v,M):
    v=tuple(v)
    if len(v)!=M or any(type(x) is not int or x not in range(3) for x in v) or not any(v):raise ValueError("nonzero canonical native word-space direction required")
    p=next(i for i,x in enumerate(v) if x);scale=v[p]
    return tuple(x*scale%3 for x in v),p


def coordinate_map(word,v):
    v,p=direction(v,len(word));word=tuple(word)
    if any(type(x) is not int or x not in range(3) for x in word):raise ValueError("canonical original word required")
    t=word[p];u=tuple((x-t*a)%3 for x,a in zip(word,v))
    return u,t


def coordinate_inverse(u,t,v):
    v,p=direction(v,len(u));u=tuple(u)
    if type(t) is not int or t not in range(3) or any(type(x) is not int or x not in range(3) for x in u) or u[p]!=0:raise ValueError("canonical quotient coordinates required")
    return tuple((x+t*a)%3 for x,a in zip(u,v))


def line_ledger(source,v):
    v,p=direction(v,source.inputs);A,B=quadratic_rows(source)
    curvature=tuple(sum(a*x*x for a,x in zip(row,v))%3 for row in B)
    linear=tuple(sum(a*x for a,x in zip(row,v))%3 for row in A)
    restricted=tuple(tuple(a*x%3 for a,x in zip(row,v)) for row in B);R=rank(restricted)
    augmented=rank([list(row)+[b] for row,b in zip(restricted,linear)])
    consistent=not any(curvature) and augmented==R
    return {"direction":v,"pivot":p,"quadratic_rows":(A,B),"curvature":curvature,"linear_offset":linear,
            "support_rank":R,"augmented_rank":augmented,"predicate_consistent":consistent,
            "exact_raw_success_probability":str(Fraction(1,3**R) if consistent else Fraction(0)),
            "accepted_tag_count":3**(source.inputs-R-1) if consistent else 0,
            "supplied_direction_field_operation_upper":8*source.dimension*source.inputs+8*source.inputs,
            "supplied_direction_finding_cost_included":False,"source_preparation_inverse_granted":False,
            "logical_output_qutrits_per_successful_batch":1}


def good(u,ledger):
    coordinate_inverse(u,0,ledger["direction"])
    if any(ledger["curvature"]):return False
    _,B=ledger["quadratic_rows"];v=ledger["direction"]
    return all((offset+2*sum(a*x*y for a,x,y in zip(row,v,u)))%3==0 for row,offset in zip(B,ledger["linear_offset"]))


def line_control(source,v,max_words=729):
    integer(max_words,"complete replay cap",1);D=3**source.inputs
    if D>max_words:raise ValueError("complete original cube exceeds replay cap; no partial certificate")
    ledger=line_ledger(source,v);v=ledger["direction"];p=ledger["pivot"]
    words=tuple(product(range(3),repeat=source.inputs));tags=tuple(u for u in words if u[p]==0)
    mapping=[];accepted=[];max_phase_error=0.0
    secrets=[(0,)*source.dimension,(1,)*source.dimension,(source.modulus-1,)*source.dimension]
    for u in tags:
        triple=tuple(coordinate_inverse(u,t,v) for t in range(3));mapping.extend(triple)
        for t,w in enumerate(triple):
            if coordinate_map(w,v)!=(u,t):raise ArithmeticError("explicit clean line coordinates not reversible")
        if good(u,ledger):
            f=[source.value(w) for w in triple];H=3;q=source.modulus;child=q//H
            if any(tuple(a%H for a in row)!=tuple(a%H for a in f[0]) for row in f):raise ArithmeticError("accepted line does not have a constant actual prefix")
            rows=tuple(tuple((a-b)%q//H for a,b in zip(row,f[0])) for row in f[1:])
            for s in secrets:
                actual=np.exp(2j*np.pi*np.array([sum(a*b for a,b in zip(row,s))%q for row in f])/q)/np.sqrt(D)
                predicted=actual[0]*np.exp(2j*np.pi*np.array([0]+[sum(a*b for a,b in zip(row,s))%child for row in rows])/child)
                max_phase_error=max(max_phase_error,float(np.max(abs(actual-predicted))))
            accepted.append({"quotient_word":u,"original_words":triple,"full_frequencies":f,"child_rows":rows,"pointed_unit_minor":pointed_minor(triple),"raw_tag_probability":str(Fraction(3,D))})
    if len(set(mapping))!=D or Fraction(3*len(accepted),D)!=Fraction(ledger["exact_raw_success_probability"]) or len(accepted)!=ledger["accepted_tag_count"]:raise ArithmeticError("whole map or exact raw success law failed")
    if max_phase_error>3e-12:raise ArithmeticError("actual source-to-child phase law failed")
    return {**ledger,"dimension":source.dimension,"parent_root_digits":source.level//2,"parent_modulus":source.modulus,
            "original_qutrits":source.inputs,"native_labels":source.labels,"full_frequency_rows":source.frequencies,
            "whole_original_words_replayed":D,"all_quotient_tags_replayed":D//3,
            "coordinate_map_sha256":hashlib.sha256(json.dumps(mapping,separators=(",",":")).encode()).hexdigest(),
            "accepted_tags":accepted,"physical_phase_residual":max_phase_error,"calibration_secrets":secrets,
            "all_potential_tags_counted_as_outputs":False,"efficient_direction_finder_supplied":False,
            "probability_and_direction_finding_cost_may_be_ignored":False,"quantum_speedup_proved":False}


def menu_bound(n,M,T,s):
    integer(n,"dimension",1);integer(M,"batch width",1);integer(T,"direction menu size",1);integer(s,"sparse-kernel cutoff")
    if s>min(n,M):raise ValueError("cutoff outside certified range")
    volume=sum(comb(M,k)*2**k for k in range(1,s+1))
    eta=min(Fraction(1),Fraction(volume,3**n));p=min(Fraction(1),eta+Fraction(T,3**s))
    return {"dimension":n,"original_qutrits":M,"direction_menu_size":T,"sparse_kernel_cutoff":s,
            "nonzero_sparse_coefficient_vectors":str(volume),"exceptional_label_probability_upper":str(eta),
            "mean_raw_menu_success_probability_upper":str(p),"directions_may_depend_on_all_low_labels":True,
            "coherent_direction_interference_or_nonlinear_partitions_excluded":False,
            "quantum_speedup_proved":False}


def best_menu_bound(n,M,T):
    best=menu_bound(n,M,T,0)
    for s in range(1,min(n,M)+1):
        value=menu_bound(n,M,T,s)
        if Fraction(value["mean_raw_menu_success_probability_upper"])<Fraction(best["mean_raw_menu_success_probability_upper"]):best=value
        if value["exceptional_label_probability_upper"]=="1":break
    return best


def from_quadratic(A,B,r=3):
    n=len(A);M=len(A[0]);q=3**r
    rows=[(tuple((A[j][i]+B[j][i])%3 for j in range(n)),tuple((2*A[j][i]+B[j][i])%3 for j in range(n))) for i in range(M)]
    rng=np.random.default_rng(88019)
    rows=[tuple(tuple(a+3*int(rng.integers(q//3)) for a in row) for row in pair) for pair in rows]
    return native_source([[inverse_frequency_coordinates(a,c,2*r) for a,c in zip(pair[0],pair[1])] for pair in rows],2*r)


def report():
    controls=[]
    cases=[("rank-one",[[0,0,1,0],[1,2,0,1]],[[1,2,0,1],[0,0,1,1]],(1,1,0,0)),
           ("rank-two",[[1,2,0,1],[0,1,2,0]],[[1,0,2,1],[0,1,2,0]],(1,1,1,0)),
           ("inconsistent-linear",[[0,0,1,0],[1,0,0,1]],[[1,2,0,1],[0,0,1,1]],(1,1,0,0)),
           ("nonzero-curvature",[[0,0,1,0],[1,2,0,1]],[[1,2,0,1],[0,0,1,1]],(1,0,0,0)),
           ("easy-additive",[[1,2,0,1],[0,0,1,0]],[[0,0,0,0],[0,0,0,0]],(1,1,0,0))]
    for name,A,B,v in cases:controls.append({"name":name,**line_control(from_quadratic(A,B),v)})
    source=random_even_source(2,4,5,88020);menu=[]
    for v in product(range(3),repeat=source.inputs):
        if any(v) and v==direction(v,source.inputs)[0]:menu.append(line_ledger(source,v))
    A,B=quadratic_rows(source);kernel=[]
    for w in product(range(3),repeat=source.inputs):
        if any(w) and all(sum(a*x for a,x in zip(row,w))%3==0 for row in B):kernel.append(w)
    smallest=min((sum(bool(x) for x in w) for w in kernel),default=source.inputs+1)
    if any(c["predicate_consistent"] and c["support_rank"]<smallest-1 for c in menu):raise ArithmeticError("support-rank implication violated")
    selected=max(menu,key=lambda c:Fraction(c["exact_raw_success_probability"]))
    controls.append({"name":"IID-native-best-exhaustive-direction-calibration",**line_control(source,selected["direction"])})
    return {"status":"NATIVE_AFFINE_LINE_INSTRUMENT_REVIEW_PENDING_TYPICAL_COVERAGE_BLOCKED",
            "derivation_sha256":hashlib.sha256(NOTE.read_bytes()).hexdigest(),"candidate_record_accepted":False,
            "quantum_speedup_proved":False,"novelty_claim":False,"native_full_cube_controls":controls,
            "complete_low_label_direction_census":{"native_labels":source.labels,"full_frequency_rows":source.frequencies,
                 "dimension":2,"parent_root_digits":2,"original_qutrits":5,"projective_direction_count":len(menu),
                 "smallest_nonzero_kernel_weight":smallest,"all_direction_support_rank_implications_checked":True,
                 "menu":menu,"full_direction_enumeration_is_scalable":False},
            "polynomial_menu_population_bounds":[best_menu_bound(n,n*n,n*n) for n in (64,128,256,512,1024)],
            "source_preparation_inverse_granted":False,"nonlinear_or_coherent_direction_compilers_ruled_out":False}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("--write",action="store_true");args=parser.parse_args();value=report()
    if args.write:REPORT.write_text(json.dumps(value,indent=2,allow_nan=False)+"\n")
    last=value["polynomial_menu_population_bounds"][-1]
    print(json.dumps({"status":value["status"],"complete_native_controls":len(value["native_full_cube_controls"]),"last_population_dimension":last["dimension"],"last_cutoff":last["sparse_kernel_cutoff"],"last_mean_raw_success_upper_decimal":float(Fraction(last["mean_raw_menu_success_probability_upper"]))}))


if __name__=="__main__":main()
