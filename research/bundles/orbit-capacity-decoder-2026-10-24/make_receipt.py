"""Save finite complete-list controls and a conditional asymptotic ledger."""

import argparse
from dataclasses import asdict, replace
from fractions import Fraction
import hashlib
from itertools import product
import json
from pathlib import Path
import random

import capacity as c

ROOT = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def receipt():
    paths = ("capacity.py","test_capacity.py","make_receipt.py","CAPACITY.md","HANDOFF.md",
             "capacity-theorem.html",
             "../orbit-residual-decoder-2026-10-24/orbit_decoder.py",
             "../orbit-residual-decoder-2026-10-24/ORBIT_DECODER.md",
             "../orbit-norm-flat-2026-10-24/FLAT_OPTIMALITY.md")
    before = {p:digest(ROOT/p) for p in paths}
    g = c.o.geometry(31,3,6)
    g = replace(g,representatives=g.representatives[:7])
    rng = random.Random(241026)
    error = [[rng.randrange(31),rng.randrange(31),1] if i<4 else [0]*3 for i in range(7)]
    s = c.o.syndrome(g,error)
    recovered = c.complete_reference(g,5,s)
    if recovered["errors"] != [error]:
        raise ArithmeticError("predeclared beyond-Prony source was not recovered")
    delta = c.weights(g.nodes,31)
    zero = c.unfold(g,[delta,[0]*7,[0]*7])
    guard_source = [row if i<3 else [0]*3 for i,row in enumerate(zero)]
    guard_syndrome = c.o.syndrome(g,guard_source)
    narrow = c.complete_reference(g,3,guard_syndrome)
    guarded = c.complete_reference(g,4,guard_syndrome)
    if narrow["status"]!="VERIFIED_UNIQUE" or guarded["status"]!="REJECT_AMBIGUOUS":
        raise ArithmeticError("whole-cap guard counterexample failed")
    small = c.o.geometry(13,3,3)
    A = c.annihilator_matrix(small,[2,3])
    cols = [0,1,3,4]
    hits = []
    for values in product(range(13),repeat=4):
        if all((sum(int(A[i,j])*v for j,v in zip(cols,values))+int(A[i,2])+2*int(A[i,5]))%13==0
               for i in range(3)):
            source = [list(values[:2])+[1],list(values[2:])+[2],[0]*3,[0]*3]
            listing = c.complete_reference(small,2,c.o.syndrome(small,source))
            if listing["status"]!="REJECT_AMBIGUOUS":
                raise ArithmeticError("exact ambiguity witness failed complete-list replay")
            hits.append({"free_frequencies":values,"complete_list":listing["errors"]})
    if len(hits)!=13 or Fraction(len(hits),13**4)!=c.collision_bound(13,4,3,2,2):
        raise ArithmeticError("fixed-last-frequency collision census disagrees")
    result = {"status":"LOCAL_UNREVIEWED_CAPACITY_APPLICATION_NO_QUANTUM_EXECUTION",
              "beyond_Prony":{"geometry":asdict(g),"seed":241026,"source_error":error,
                  "syndromes":s,"old_receiver":c.o.decode(g,5,s),"complete_receiver":recovered},
              "whole_cap_counterexample":{"geometry":asdict(g),"source":guard_source,
                  "source_radius_list":narrow,"guarded_list":guarded},
              "capacity_endpoint":{"cap":g.row_length,"original_error":error,
                  "competing_error":c.endpoint_competitor(g,s,0),
                  "scope":"nonzero_source_whole_cap_singleton_obstruction_only"},
              "collision_census":{"geometry":asdict(small),"source_support":[0,1],
                  "fixed_last_frequencies":[1,2],"assignments":13**4,"collisions":len(hits),
                  "fraction":str(Fraction(len(hits),13**4)),"collision_witnesses":hits},
              "conditional_large_ledger":c.ledger(),
              "external_dependency":{"url":"https://arxiv.org/html/2609.05870v1",
                  "theorems":["1.1","8.2"],"retrieved":"2026-10-24",
                  "role":"published_preprint_theorem_not_independently_verified_or_implemented"},
              "main_checkout_changed":False,"source_sha256":before}
    if before!={p:digest(ROOT/p) for p in paths}:
        raise RuntimeError("source changed during this run")
    return result


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output",type=Path)
    args = parser.parse_args()
    data = json.dumps(receipt(),indent=2,sort_keys=True)+"\n"
    if args.output:
        args.output.write_text(data)
    else:
        print(data,end="")
