"""Exact three-block realizability probes of a certified native PSD gap.

LOCAL DERIVATION / REVIEW PENDING. Local extensions need not be a global
distribution; local obstructions give native-valid NON-PSD inequalities.
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
import numpy as np
from scipy.optimize import linprog

from ternary_prefix_integrality import rational, exact_affine_proposal, frontier_geometry, REPORT as PREFIX_REPORT
from ternary_prefix_moments import moment_model, verify_moments, analyze_moments
from ternary_moment_psd import moment_matrix, certify_psd
from ternary_psd_support_lift import REPORT as SUPPORT_REPORT
from ternary_pair_collimation import LowProblem
from ternary_repair_catalog import FIXTURE, frozen_policy
from ternary_adaptive_shell import compile_adaptive

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"research/phase_workbench/ternary_local_marginals.json"


def local_model(model, moments, blocks):
    if not verify_moments(model,moments)["valid"]:raise ValueError("exact full original native moments required")
    blocks=tuple(blocks);domains=model["geometry"]["domains"]
    if len(blocks)!=3 or blocks!=tuple(sorted(set(blocks))) or any(type(i) is not int or not 0<=i<len(domains) for i in blocks):
        raise ValueError("three sorted distinct original blocks required")
    index={key:i for i,key in enumerate(model["variables"])}
    assignments=tuple(product(*(domains[i] for i in blocks)));rows=[];rhs=[];indices=[]
    for i,j in combinations(range(3),2):
        for a,b in product(domains[blocks[i]],domains[blocks[j]]):
            key=("J",blocks[i],a,blocks[j],b);k=index[key]
            rows.append(tuple(int(w[i]==a and w[j]==b) for w in assignments));rhs.append(rational(moments[k]));indices.append(k)
    return {"blocks":blocks,"assignments":assignments,"rows":tuple(rows),"rhs":tuple(rhs),
        "pair_variable_indices":tuple(indices),"required_winding":model["required_winding"]}


def verify_extension(local, values):
    if len(values)!=len(local["assignments"]):raise ValueError("complete exact local distribution required")
    t=tuple(rational(x) for x in values);issues=[]
    if any(x<0 for x in t):issues.append("negative local assignment probability")
    if sum(t)!=1:issues.append("local assignment probabilities must sum exactly to one")
    if any(sum((a*x for a,x in zip(row,t)),fmpq(0))!=b for row,b in zip(local["rows"],local["rhs"])):
        issues.append("one or more original pair marginals differ exactly")
    return {"valid":not issues,"issues":issues,"assignment_probabilities":[str(x) for x in t],
        "required_winding":local["required_winding"],"global_native_realization_proved":False}


def verify_local_dual(local, weights):
    if len(weights)!=len(local["rows"]):raise ValueError("complete exact pair-marginal dual required")
    y=tuple(rational(x) for x in weights)
    columns=tuple(sum((a*row[j] for a,row in zip(y,local["rows"])),fmpq(0)) for j in range(len(local["assignments"])))
    rhs=sum((a*b for a,b in zip(y,local["rhs"])),fmpq(0));issues=[]
    if any(x<0 for x in columns):issues.append("local inequality fails on an original native assignment")
    if rhs>=0:issues.append("local inequality does not strictly reject the saved exact marginals")
    return {"valid":not issues,"issues":issues,"pair_marginal_multipliers":[str(a) for a in y],
        "exact_assignment_coefficients":[str(a) for a in columns],"exact_gap_point_value":str(rhs),
        "pair_variable_indices":list(local["pair_variable_indices"]),"required_winding":local["required_winding"],
        "proves_no_three_block_extension":not issues,"proves_no_full_moment_PSD_point":False}


def analyze_local(local):
    start=time.perf_counter();N=len(local["assignments"]);R=len(local["rows"])
    A=np.array(local["rows"],dtype=float);B=np.array([float(x) for x in local["rhs"]])
    cost={"LP_calls":1,"assignments":N,"pair_marginal_rows":R,"exact_reconstruction_attempts":0}
    def finish(status,extension=None,dual=None):
        cost["wall_seconds_including_exact_certificates"]=time.perf_counter()-start
        return {"status":status,"extension":extension,"dual":dual,"cost":cost}
    solution=linprog(np.zeros(N),A_eq=A,b_eq=B,bounds=(0,None),method="highs-ds")
    if solution.success:
        if np.asarray(solution.x).shape!=(N,) or not np.isfinite(solution.x).all():raise ValueError("finite complete local primal proposal required")
        seen=set()
        for tolerance in (1e-8,1e-12,0):
            support=tuple(j for j,x in enumerate(solution.x) if x>tolerance)
            if support in seen:continue
            seen.add(support);cost["exact_reconstruction_attempts"]+=1
            augmented=[[*[row[j] for j in support],b] for row,b in zip(local["rows"],local["rhs"])]
            for selected,_ in exact_affine_proposal(augmented,solution.x[list(support)]):
                full=[fmpq(0)]*N
                for j,x in zip(support,selected):full[j]=x
                cert=verify_extension(local,full)
                if cert["valid"]:return finish("EXACT_THREE_BLOCK_EXTENSION_NOT_GLOBAL",extension=cert)
    cost["LP_calls"]+=1
    # Exact scale fixes b^T*y=-1 only in the PROPOSAL; every column is replayed.
    dual=linprog(np.zeros(R),A_ub=-A.T,b_ub=np.zeros(N),A_eq=B.reshape(1,-1),b_eq=np.array([-1.0]),bounds=(None,None),method="highs-ds")
    if dual.success:
        if np.asarray(dual.x).shape!=(R,) or not np.isfinite(dual.x).all():raise ValueError("finite complete local dual proposal required")
        active=[j for j,x in enumerate(A.T@dual.x) if abs(x)<=1e-7];seen=set()
        for tolerance in (1e-8,1e-12,0):
            support=tuple(i for i,x in enumerate(dual.x) if abs(x)>tolerance)
            if support in seen:continue
            seen.add(support);cost["exact_reconstruction_attempts"]+=1
            augmented=[[*[local["rhs"][i] for i in support],-1]]
            augmented.extend([*[local["rows"][i][j] for i in support],0] for j in active)
            for selected,_ in exact_affine_proposal(augmented,dual.x[list(support)]):
                full=[fmpq(0)]*R
                for i,x in zip(support,selected):full[i]=x
                cert=verify_local_dual(local,full)
                if cert["valid"]:return finish("EXACT_NONPSD_THREE_BLOCK_OBSTRUCTION",dual=cert)
    return finish("THREE_BLOCK_EXACT_RECONSTRUCTION_UNKNOWN")


def append_local_cut(model, local, certificate):
    if certificate["required_winding"]!=model["required_winding"] or local["required_winding"]!=model["required_winding"]:
        raise ValueError("local inequality belongs to another winding")
    blocks=local["blocks"];domains=model["geometry"]["domains"]
    if len(blocks)!=3 or tuple(blocks)!=tuple(sorted(set(blocks))) or any(type(i) is not int or not 0<=i<len(domains) for i in blocks):
        raise ValueError("local cut must use three original native blocks")
    assignments=tuple(product(*(domains[i] for i in blocks)))
    index={key:i for i,key in enumerate(model["variables"])};rows=[];indices=[]
    for i,j in combinations(range(3),2):
        for a,b in product(domains[blocks[i]],domains[blocks[j]]):
            rows.append(tuple(int(w[i]==a and w[j]==b) for w in assignments))
            indices.append(index[("J",blocks[i],a,blocks[j],b)])
    if local["assignments"]!=assignments or local["rows"]!=tuple(rows) or local["pair_variable_indices"]!=tuple(indices):
        raise ValueError("local inequality must match EVERY actual native assignment and original pair column")
    checked=verify_local_dual(local,certificate["pair_marginal_multipliers"])
    if not checked["valid"]:raise ValueError("all local native assignments must independently certify the inequality")
    coefficients={}
    for j,a in zip(local["pair_variable_indices"],checked["pair_marginal_multipliers"]):
        coefficients[j]=coefficients.get(j,fmpq(0))+rational(a)
    D=math.lcm(*(int(a.q) for a in coefficients.values()));ints={j:int((a*D).p) for j,a in coefficients.items()}
    divisor=math.gcd(*ints.values());ints={j:a//divisor for j,a in ints.items() if a}
    N=len(model["variables"]);cuts=model.get("local_marginal_cuts",());row={**ints,N:-1}
    cut={"blocks":list(local["blocks"]),"pair_marginal_multipliers":checked["pair_marginal_multipliers"],
        "integer_coefficients":{str(j):str(a) for j,a in ints.items()},"slack_variable":N,
        "clearing_denominator":str(D),"primitive_divisor":str(divisor)}
    return {**model,"variables":(*model["variables"],("LOCAL_SLACK",len(cuts))),
        "rows":(*model["rows"],row),"rhs":(*model["rhs"],0),
        "row_names":(*model["row_names"],("LOCAL_MARGINAL_CUT",len(cuts))),
        "nonzero_entries":model["nonzero_entries"]+len(row),"local_marginal_cuts":(*cuts,cut)}


def bounded_cut_resolve(model, moments, trials, cut_budget=64):
    if type(cut_budget) is not int or cut_budget<0:raise ValueError("explicit nonnegative local-cut budget required")
    base=model;applied=[];available=sum(bool(t["dual"]) for t in trials)
    for t in trials:
        if not t["dual"] or len(applied)>=cut_budget:continue
        local=local_model(base,moments,t["blocks"]);model=append_local_cut(model,local,t["dual"])
        applied.append(model["local_marginal_cuts"][-1])
    if not applied:
        return {"cuts":[],"available_obstructions":available,"cut_budget":cut_budget,"analysis":None,
            "whole_prefix_infeasibility_proved":False}
    analysis=analyze_moments(model)
    positivity=certify_psd(moment_matrix(model,analysis["primal"]["moments"])) if analysis["primal"] else None
    return {"cuts":applied,"available_obstructions":available,"cut_budget":cut_budget,"analysis":analysis,
        "primal_positivity":positivity,"whole_prefix_infeasibility_proved":False,
        "full_base_plus_selected_local_cuts_infeasible":bool(analysis["dual"]),
        "ordinary_two_witness_recovery_proved":False}


def build_report(cut_budget=64):
    raw=SUPPORT_REPORT.read_bytes();support=json.loads(raw);prefix_raw=PREFIX_REPORT.read_bytes();fixture_raw=FIXTURE.read_bytes()
    if support["source_sha256"]["prefix"]!=hashlib.sha256(prefix_raw).hexdigest() or support["source_sha256"]["fixture"]!=hashlib.sha256(fixture_raw).hexdigest():
        raise ValueError("source hashes changed; regenerate support report before local probes")
    prefixes=json.loads(prefix_raw);source=json.loads(fixture_raw);cases=[]
    for c in support["cases"]:
        eligible=[(t,r) for t in c["trials"] for r in t["winding_trials"] if r.get("PSD_native_gap_certificate")]
        if not eligible:continue
        original=source["planted_geometry_probes"][c["fixture_probe_index"]]
        A=tuple(map(int,original["labels"]));Q=int(original["modulus"])
        problem=LowProblem((Q,),tuple(((a,),(b,)) for a,b in zip(A[::2],A[1::2])),0)
        policy=frozen_policy(problem,original["prepared"]);compiled=compile_adaptive(policy)
        pc=next(x for x in prefixes["cases"] if x["fixture_probe_index"]==c["fixture_probe_index"])
        for t,r in eligible:
            pt=next(x for x in pc["trials"] if x["target"]==t["target"]);f=pt["frontier"]
            cp={"unassigned_rows":f["unassigned_rows"],"partial_coefficients":tuple(map(int,f["partial_coefficients"])),"assigned_squared_energy":f["assigned_squared_energy"]}
            g=frontier_geometry(problem,(int(t["target"]),),policy,compiled,cp);model=moment_model(g,r["winding_branch"])
            cert=r["PSD_native_gap_certificate"]["moment_certificate"]
            if cert["required_winding"]!=r["winding_branch"] or not verify_moments(model,cert["moments"])["valid"]:
                raise ValueError("retained PSD gap must verify against original full source model")
            if pt["status"]!="EXACT_WINDING_PREFIX_INTEGRALITY_GAP" or pt["native_truth"]["native_prefix_words"]!=[]:
                raise ValueError("gap input must reference an independently checked empty original prefix")
            if not certify_psd(moment_matrix(model,cert["moments"]))["ldl"]:
                raise ValueError("gap input must pass exact original-coordinate PSD verification")
            start=time.perf_counter();runs=[]
            for blocks in combinations(range(problem.width),3):
                local=local_model(model,cert["moments"],blocks)
                runs.append({"blocks":list(blocks),**analyze_local(local)})
            cases.append({"fixture_probe_index":c["fixture_probe_index"],"fingerprint":c["fingerprint"],
                "target":t["target"],"winding_branch":r["winding_branch"],"block_count":problem.width,
                "gap_PSD_rechecked_exactly":True,
                "triple_trials":runs,"complete_triple_schedule":True,
                "all_triples_extend_exactly":all(x["extension"] for x in runs),
                "nonPSD_local_obstructions":sum(bool(x["dual"]) for x in runs),
                "wall_seconds_including_source_point_rechecks":time.perf_counter()-start,
                "cut_resolve":bounded_cut_resolve(model,cert["moments"],runs,cut_budget)})
    return {"status":"EXACT_LOCAL_NATIVE_REALIZABILITY_AUDIT_OF_CERTIFIED_PSD_GAPS",
        "source_support_report_sha256":hashlib.sha256(raw).hexdigest(),"cases":cases,
        "local_derivations_review_pending":True,"novelty_claim":False,"polynomial_pair_finder_proved":False,
        "global_distribution_proved":False,"population_gap_proved":False,"local_cut_budget":cut_budget}


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("--write",action="store_true");parser.add_argument("--cut-budget",type=int,default=64);args=parser.parse_args()
    result=build_report(args.cut_budget)
    if args.write:REPORT.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"status":result["status"],"triple_statuses":dict(Counter(t["status"] for c in result["cases"] for t in c["triple_trials"]))},indent=2))
