"""Exact Boolean-event triangle separation of native pair moments.

LOCAL DERIVATION / REVIEW PENDING. This is a classical necessary-condition
separator, not a complete local polytope test or a quantum algorithm.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
from itertools import combinations, product
import json
import math
from pathlib import Path
import time

from flint import fmpq

from ternary_prefix_integrality import rational, frontier_geometry, REPORT as PREFIX_REPORT
from ternary_prefix_moments import moment_model, verify_moments
from ternary_joint_realizability import REPORT as JOINT_REPORT
from ternary_psd_support_lift import REPORT as SUPPORT_REPORT
from ternary_local_marginals import REPORT as LOCAL_REPORT
from ternary_pair_collimation import LowProblem
from ternary_repair_catalog import FIXTURE, frozen_policy
from ternary_adaptive_shell import compile_adaptive

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"research/phase_workbench/ternary_event_triangles.json"


def event_subsets(domain):
    return tuple(tuple(domain[j] for j in range(len(domain)) if mask&(1<<j)) for mask in range(1,(1<<len(domain))-1))


def triangle_coefficients(model, blocks, events, center):
    blocks=tuple(blocks);events=tuple(tuple(S) for S in events);domains=model["geometry"]["domains"]
    if len(blocks)!=3 or blocks!=tuple(sorted(set(blocks))) or any(type(i) is not int or not 0<=i<len(domains) for i in blocks):
        raise ValueError("three sorted distinct original blocks required")
    if len(events)!=3 or any(S not in event_subsets(domains[i]) for i,S in zip(blocks,events)):
        raise ValueError("nonempty proper native digit events required")
    if type(center) is not int or not 0<=center<3:raise ValueError("original event center in 0..2 required")
    index={key:i for i,key in enumerate(model["variables"])};coefficients={}
    def add(key,a):
        j=index[key];coefficients[j]=coefficients.get(j,0)+a
    for a in events[center]:add(("p",blocks[center],a),1)
    for i,j in combinations(range(3),2):
        sign=-1 if center in (i,j) else 1
        for a,b in product(events[i],events[j]):add(("J",blocks[i],a,blocks[j],b),sign)
    return {j:a for j,a in coefficients.items() if a}


def verify_triangle(model, moments, blocks, events, center):
    if not verify_moments(model,moments)["valid"]:raise ValueError("exact original full moment point required")
    coefficients=triangle_coefficients(model,blocks,events,center)
    local_values=[]
    for word in product(*(model["geometry"]["domains"][i] for i in blocks)):
        bits=[int(a in S) for a,S in zip(word,events)];others=[i for i in range(3) if i!=center]
        value=bits[center]-bits[center]*bits[others[0]]-bits[center]*bits[others[1]]+bits[others[0]]*bits[others[1]]
        if value not in (0,1):raise ArithmeticError("Boolean event triangle must be pointwise nonnegative")
        lifted=0
        for j,a in coefficients.items():
            key=model["variables"][j]
            indicator=int(word[blocks.index(key[1])]==key[2])
            if key[0]=="J":indicator*=int(word[blocks.index(key[3])]==key[4])
            lifted+=a*indicator
        if lifted!=value:raise ArithmeticError("original native coefficient expansion disagrees with Boolean truth table")
        local_values.append(value)
    value=sum((a*rational(moments[j]) for j,a in coefficients.items()),fmpq(0))
    return {"valid_native_inequality":True,"rejects_THIS_point":value<0,"blocks":list(blocks),
        "events":[list(S) for S in events],"center_position":center,
        "integer_coefficients":{str(j):str(a) for j,a in coefficients.items()},
        "exact_point_value":str(value),"local_assignment_values":local_values,
        "required_winding":model["required_winding"],"proves_no_native_realization_of_THIS_point":value<0,
        "proves_entire_relaxation_infeasible":False}


def scan_triangles(model, moments, event_budget=2_000_000):
    if type(event_budget) is not int or event_budget<1:raise ValueError("positive whole-event-family preflight required")
    start=time.perf_counter();cert=verify_moments(model,moments)
    if not cert["valid"]:raise ValueError("exact original full moment point required")
    domains=model["geometry"]["domains"];M=len(domains);families=[event_subsets(D) for D in domains]
    triples=list(combinations(range(M),3));size=0
    for blocks in triples:
        for center in range(3):
            # Complementing ALL three Boolean events leaves T unchanged.
            # Keep only center events containing the first native digit.
            counts=[sum(domains[b][0] in S for S in families[b]) if j==center else len(families[b]) for j,b in enumerate(blocks)]
            size+=math.prod(counts)
    cost={"event_combinations_preflight":size,"event_budget":event_budget,"event_combinations_evaluated":0,
        "LP_calls":0,"pair_event_sums_computed":0,"selected_native_inequality_checks":0,"full_original_point_verification_calls":1}
    if size>event_budget:
        cost["wall_seconds_including_original_point_and_native_checks"]=time.perf_counter()-start
        return {"status":"EVENT_TRIANGLE_PREFLIGHT_UNKNOWN","triple_trials":[],"cost":cost,
            "no_violations_is_not_local_extendability_proof":True}
    x=tuple(rational(a) for a in moments);denominator=math.lcm(*(int(a.q) for a in x));numerators=tuple(int((a*denominator).p) for a in x)
    cost["exact_common_denominator_bits"]=denominator.bit_length()
    cost["maximum_scaled_moment_bits"]=max((0,*(abs(a).bit_length() for a in numerators)))
    index={key:i for i,key in enumerate(model["variables"])}
    marginals={(b,S):sum(numerators[index[("p",b,a)]] for a in S) for b in range(M) for S in families[b]}
    pairs={}
    for i,j in combinations(range(M),2):
        for S,T in product(families[i],families[j]):
            pairs[(i,S,j,T)]=sum(numerators[index[("J",i,a,j,b)]] for a,b in product(S,T));cost["pair_event_sums_computed"]+=1
    trials=[]
    for blocks in triples:
        best=None;tested=0
        for center in range(3):
            choices=[tuple(S for S in families[b] if domains[b][0] in S) if j==center else families[b] for j,b in enumerate(blocks)]
            for events in product(*choices):
                value=marginals[(blocks[center],events[center])]
                for i,j in combinations(range(3),2):
                    pair=pairs[(blocks[i],events[i],blocks[j],events[j])]
                    value+=-pair if center in (i,j) else pair
                tested+=1
                if value<0 and (best is None or value<best[0]):best=(value,events,center)
        cost["event_combinations_evaluated"]+=tested
        if best:
            proof=verify_triangle(model,moments,blocks,best[1],best[2]);cost["selected_native_inequality_checks"]+=1;cost["full_original_point_verification_calls"]+=1
            if not proof["rejects_THIS_point"] or rational(proof["exact_point_value"])!=fmpq(best[0],denominator):
                raise ArithmeticError("cached exact event sum disagrees with original-variable proof")
            trials.append({"blocks":list(blocks),"status":"EXACT_EVENT_TRIANGLE_NATIVE_OBSTRUCTION","event_combinations_evaluated":tested,"certificate":proof})
        else:trials.append({"blocks":list(blocks),"status":"NO_EVENT_TRIANGLE_VIOLATION_NOT_LOCAL_PROOF","event_combinations_evaluated":tested,"certificate":None})
    cost["wall_seconds_including_original_point_and_native_checks"]=time.perf_counter()-start
    return {"status":"EXACT_COMPLETE_EVENT_TRIANGLE_SCAN_NOT_LOCAL_POLYTOPE_TEST","triple_trials":trials,"cost":cost,
        "global_native_distribution_proved":False,"no_violations_is_not_local_extendability_proof":True}


def build_report():
    paths={"joint":JOINT_REPORT,"support":SUPPORT_REPORT,"local":LOCAL_REPORT,"prefix":PREFIX_REPORT,"fixture":FIXTURE}
    raw={k:p.read_bytes() for k,p in paths.items()};data={k:json.loads(b) for k,b in raw.items()}
    joint=data["joint"];support=data["support"];local=data["local"]
    if any(joint["source_sha256"][k]!=hashlib.sha256(raw[k]).hexdigest() for k in ("support","local","prefix","fixture")):
        raise ValueError("event scan sources changed; regenerate joint report first")
    cases=[]
    for lc in local["cases"]:
        pc=next(c for c in data["prefix"]["cases"] if c["fixture_probe_index"]==lc["fixture_probe_index"])
        pt=next(t for t in pc["trials"] if t["target"]==lc["target"]);original=data["fixture"]["planted_geometry_probes"][lc["fixture_probe_index"]]
        A=tuple(map(int,original["labels"]));Q=int(original["modulus"])
        problem=LowProblem((Q,),tuple(((a,),(b,)) for a,b in zip(A[::2],A[1::2])),0)
        policy=frozen_policy(problem,original["prepared"]);compiled=compile_adaptive(policy);f=pt["frontier"]
        cp={"unassigned_rows":f["unassigned_rows"],"partial_coefficients":tuple(map(int,f["partial_coefficients"])),"assigned_squared_energy":f["assigned_squared_energy"]}
        g=frontier_geometry(problem,(int(lc["target"]),),policy,compiled,cp);model=moment_model(g,lc["winding_branch"]);N=len(model["variables"])
        sc=next(c for c in support["cases"] if c["fixture_probe_index"]==lc["fixture_probe_index"])
        st=next(t for t in sc["trials"] if t["target"]==lc["target"])
        sr=next(r for r in st["winding_trials"] if r["winding_branch"]==lc["winding_branch"])
        records=[("INITIAL_PSD_GAP",sr["PSD_native_gap_certificate"]["moment_certificate"],lc)]
        records.extend(("JOINT_SELECTED_LOCAL_CUTS_PSD_GAP",c["joint_gap_point"]["primal"],None) for c in joint["cases"] if c["fixture_probe_index"]==lc["fixture_probe_index"] and c["target"]==lc["target"] and c["winding_branch"]==lc["winding_branch"] and c["joint_gap_point"])
        for name,point,reference in records:
            result=scan_triangles(model,point["moments"][:N])
            comparison=None
            if reference:
                comparison={"reference_local_obstructions":reference["nonPSD_local_obstructions"],"detected_reference_obstructions":0,"reference_obstructions_not_detected":0,"contradictions_with_exact_extensions":0}
                for t,r in zip(result["triple_trials"],reference["triple_trials"]):
                    if t["blocks"]!=r["blocks"]:raise ValueError("exact same complete original triple schedule required")
                    if r["extension"] and t["certificate"]:raise ArithmeticError("native event inequality contradicts an exact local distribution")
                    if r["dual"]:
                        comparison["detected_reference_obstructions" if t["certificate"] else "reference_obstructions_not_detected"]+=1
            cases.append({"fixture_probe_index":lc["fixture_probe_index"],"fingerprint":lc["fingerprint"],"target":lc["target"],
                "winding_branch":lc["winding_branch"],"source_point":name,"local_reference_comparison":comparison,**result})
    return {"status":"EXACT_BOOLEAN_EVENT_NATIVE_SEPARATION_PILOT_NOT_SOLVER","cases":cases,
        "source_sha256":{k:hashlib.sha256(b).hexdigest() for k,b in raw.items()},"local_derivations_review_pending":True,
        "novelty_claim":False,"polynomial_pair_finder_proved":False,"complete_local_polytope_separator_proved":False}


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("--write",action="store_true");args=parser.parse_args();report=build_report()
    if args.write:REPORT.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"status":report["status"],"points":[{"source":c["source_point"],"triple_statuses":dict(Counter(t["status"] for t in c["triple_trials"])),"cost":c["cost"],"reference":c["local_reference_comparison"]} for c in report["cases"]]},indent=2))
