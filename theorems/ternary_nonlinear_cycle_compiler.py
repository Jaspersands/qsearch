"""Canonical three-cycle coordinates erase the original index without ranks.

LOCAL DERIVATION / REVIEW PENDING. Reference atlas evaluation is exponential;
the clean cheap affine control has its actual small coverage charged.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
from itertools import product
import json
from pathlib import Path

import numpy as np

from ternary_affine_line_extractor import coordinate_inverse,coordinate_map,from_quadratic,good,line_ledger
from ternary_batch_fiber_compiler import BatchFiberProgram,batch_ledger,integer,pointed_minor
from ternary_cyclic_extractor import random_even_source,throughput_ledger

ROOT=Path(__file__).resolve().parents[1]
NOTE=ROOT/"research/TERNARY_NONLINEAR_CYCLE_COMPILER.md"
REPORT=ROOT/"research/phase_workbench/ternary_nonlinear_cycle_compiler.json"


def canonical_word(word,M):
    word=tuple(word)
    if len(word)!=M or any(type(a) is not int or a not in range(3) for a in word):raise ValueError("canonical original word required")
    return word


def cyclic_coordinates(word,step):
    word=canonical_word(word,len(word));y=canonical_word(step(word),len(word));z=canonical_word(step(y),len(word))
    if canonical_word(step(z),len(word))!=word:raise ValueError("global order-three identity failed on an original word")
    orbit=(word,y,z)
    if word==y:
        if z!=word:raise ValueError("inconsistent fixed orbit")
        return word,0,False
    if len(set(orbit))!=3:raise ValueError("nontrivial orbit is not a three-cycle")
    index=min(range(3),key=lambda k:orbit[k]);return orbit[index],(-index)%3,True


def reconstruct(u,t,step):
    u=canonical_word(u,len(u));integer(t,"logical digit")
    if t>=3:raise ValueError("logical digit outside qutrit")
    word=u
    for _ in range(t):word=canonical_word(step(word),len(u))
    return word


def reference_step(program,max_words=19683):
    reference=program.reference(max_words);atlas={}
    for tag in range(len(reference.words)//3):
        triple=reference.triple(tag)
        for j,w in enumerate(triple):atlas[w]=triple[(j+1)%3]
    return atlas.__getitem__


def affine_step(source,v):
    ledger=line_ledger(source,v);v=ledger["direction"]
    def step(word):
        u,t=coordinate_map(word,v)
        return coordinate_inverse(u,(t+1)%3,v) if good(u,ledger) else tuple(word)
    return step


def audit(program,evaluator_mode,v=None,max_words=19683):
    integer(max_words,"complete word budget",1);s=program.source;D=3**s.inputs
    if D>max_words:raise ValueError("complete orbit audit exceeds budget; no partial certificate")
    if evaluator_mode not in ("exponential-low-fiber-atlas","supplied-low-affine-direction"):raise ValueError("unreviewed evaluator cost mode")
    if evaluator_mode=="exponential-low-fiber-atlas":
        if v is not None:raise ValueError("reference atlas has no supplied direction")
        step=reference_step(program,max_words)
    else:
        if program.prefix_digits!=1:raise ValueError("affine recipe certifies only the first native prefix")
        step=affine_step(s,v)
    words=tuple(product(range(3),repeat=s.inputs));coordinates=[];orbit_rows={};phase_residual=0.0;erasure_errors=0
    secrets=[(0,)*s.dimension,(1,)*s.dimension,(s.modulus-1,)*s.dimension]
    for word in words:
        u,t,success=cyclic_coordinates(word,step);coordinates.append((u,t,success));original=reconstruct(u,t,step)
        if original!=word:raise ArithmeticError("canonical orbit coordinates not invertible")
        erased=tuple((a-b)%3 for a,b in zip(word,original));erasure_errors+=int(any(erased))
        if program.low_frequency(step(word))!=program.low_frequency(word):raise ValueError("cycle changes actual native prefix")
        if success and u not in orbit_rows:
            triple=tuple(reconstruct(u,k,step) for k in range(3));f=[s.value(w) for w in triple];H=program.prefix_modulus;q=s.modulus;child=q//H
            if any(tuple(a%H for a in row)!=tuple(a%H for a in f[0]) for row in f):raise ArithmeticError("native orbit leaves prefix")
            child_rows=tuple(tuple((a-b)%q//H for a,b in zip(row,f[0])) for row in f[1:])
            for secret in secrets:
                actual=np.exp(2j*np.pi*np.array([sum(a*b for a,b in zip(row,secret))%q for row in f])/q)/np.sqrt(D)
                expected=actual[0]*np.exp(2j*np.pi*np.array([0]+[sum(a*b for a,b in zip(row,secret))%child for row in child_rows])/child)
                phase_residual=max(phase_residual,float(np.max(abs(actual-expected))))
            orbit_rows[u]={"tag_word":u,"original_words":triple,"full_frequencies":f,"child_rows":child_rows,
                           "pointed_unit_minor":pointed_minor(triple),"raw_tag_probability":str(Fraction(3,D))}
    if len(set(coordinates))!=D or erasure_errors or phase_residual>3e-12:raise ArithmeticError("clean basis compilation failed")
    tags=sorted(orbit_rows);moved=3*len(tags);selected=sorted(set((0,len(tags)//2,len(tags)-1))) if tags else []
    return {"dimension":s.dimension,"parent_root_digits":s.level//2,"parent_modulus":s.modulus,"prefix_digits":program.prefix_digits,
            "original_qutrits":s.inputs,"native_labels":s.labels,"full_frequency_rows":s.frequencies,"evaluator_mode":evaluator_mode,
            "supplied_direction":tuple(v) if v is not None else None,
            "low_rows_only_policy":True,"whole_original_words_audited":D,"complete_coordinate_map_sha256":hashlib.sha256(json.dumps(coordinates,separators=(",",":")).encode()).hexdigest(),
            "nonfixed_original_word_count":moved,"accepted_three_cycle_count":len(tags),"raw_success_probability":str(Fraction(moved,D)),
            "nonaffine_three_cycle_count":sum(any(sum(w[j] for w in orbit_rows[u]["original_words"])%3 for j in range(s.inputs)) for u in tags),
            "canonical_tag_register_trits":s.inputs,"logical_register_trits":1,"original_word_scratch_erasure_failures":erasure_errors,
            "global_fiber_rank_or_unrank_called":False,"all_potential_orbits_counted_as_outputs":False,"output_qutrits_per_accepted_batch":1,
            "clean_evaluator_compute_uncompute_call_upper":10,"selected_child_controls":[orbit_rows[tags[k]] for k in selected],
            "all_accepted_child_phases_checked":len(tags),"calibration_secrets":secrets,"physical_phase_residual":phase_residual,
            "efficient_nonlinear_cycle_evaluator_supplied":False,"whole_instrument_approximation_error_bound_supplied":False,
            "quantum_speedup_proved":False}


def report():
    controls=[]
    for n,r,d,M,seed in ((1,3,2,9,88030),(2,2,1,5,88031)):
        p=BatchFiberProgram(random_even_source(n,2*r,M,seed),d)
        controls.append(audit(p,"exponential-low-fiber-atlas"))
    source=from_quadratic([[0,0,1,0],[1,2,0,1]],[[1,2,0,1],[0,0,1,1]])
    controls.append(audit(BatchFiberProgram(source,1),"supplied-low-affine-direction",(1,1,0,0)))
    return {"status":"NATIVE_NONLINEAR_CYCLE_COMPILER_REVIEW_PENDING_FAST_CYCLE_ACTION_MISSING",
            "derivation_sha256":hashlib.sha256(NOTE.read_bytes()).hexdigest(),"candidate_record_accepted":False,"quantum_speedup_proved":False,"novelty_claim":False,
            "native_complete_controls":controls,"source_preparation_inverse_granted":False,
            "full_depth_supply_comparisons":[{"dimension":3**r,"parent_root_digits":r,"prefix_digits":r-1,
                "conditional_direct_batch_original_copies":batch_ledger(3**r,r,r-1)["minimum_original_qutrits_for_all_fibers_divisible_by_three"],
                "existing_sieve":throughput_ledger(3**r,r),"shallow_perfect_acceptance_is_already_known":True,
                "comparison_is_not_an_implemented_direct_algorithm":True} for r in (2,3,4,5)],
            "tag_compression_or_global_ranking_required":False,"efficient_constant_coverage_nonlinear_action_supplied":False,
            "all_quantum_receivers_equivalent_to_cycle_actions_claimed":False}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("--write",action="store_true");args=parser.parse_args();value=report()
    if args.write:REPORT.write_text(json.dumps(value,indent=2,allow_nan=False)+"\n")
    print(json.dumps({"status":value["status"],"whole_original_words_audited":sum(c["whole_original_words_audited"] for c in value["native_complete_controls"]),"fast_cycle_action_supplied":False}))


if __name__=="__main__":main()
