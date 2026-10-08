"""Bounded joint local-marginal/PSD audit of an original native prefix.

LOCAL DERIVATION / REVIEW PENDING. Every conclusion retains the exact
fixed-winding scope; a joint continuation is not native realizability.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import time

from flint import fmpq

from ternary_prefix_integrality import rational, frontier_geometry, REPORT as PREFIX_REPORT
from ternary_prefix_moments import moment_model, verify_moments
from ternary_moment_psd import moment_matrix, certify_psd, psd_cut_loop
from ternary_moment_psd_mixtures import mixture_search
from ternary_psd_support_lift import sos_objective, support_test, REPORT as SUPPORT_REPORT
from ternary_local_marginals import local_model, append_local_cut, REPORT as LOCAL_REPORT
from ternary_pair_collimation import LowProblem
from ternary_repair_catalog import FIXTURE, frozen_policy
from ternary_adaptive_shell import compile_adaptive

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"research/phase_workbench/ternary_joint_realizability.json"


def base_certificate(model, certificate):
    if certificate["required_winding"]!=model["required_winding"]:
        raise ValueError("joint point belongs to another winding")
    values=certificate["moments"][:len(model["variables"])]
    checked=verify_moments(model,values)
    if not checked["valid"]:raise ValueError("every point must satisfy ALL original and local-cut rows")
    return checked


def positive_hull_point(model, points, hull):
    if hull["status"]!="EXACT_PSD_MOMENT_CONTINUATION_NOT_NATIVE_PROOF":return None
    weights=tuple(rational(x) for x in hull["exact_convex_weights"])
    if len(weights)!=len(points) or any(w<0 for w in weights) or sum(weights)!=1:
        raise ValueError("complete nonnegative exact convex weights required")
    checked=[base_certificate(model,p) for p in points]
    values=tuple(sum((w*rational(p["moments"][j]) for w,p in zip(weights,checked)),fmpq(0)) for j in range(len(model["variables"])))
    cert=verify_moments(model,values);positivity=certify_psd(moment_matrix(model,values))
    if not cert["valid"] or not positivity["ldl"]:raise ValueError("claimed positive hull needs full original-coordinate exact joint proof")
    return {"primal":cert,"positivity":positivity,"global_native_distribution_proved":False}


def audit_joint(model, initial, max_psd_cuts=3):
    if model.get("psd_cuts") or any(key[0] not in ("p","J","LOCAL_SLACK") for key in model["variables"]):
        raise ValueError("joint audit starts from native rows and explicit local slacks, without prior PSD cuts")
    initial=base_certificate(model,initial);start=time.perf_counter()
    loop=psd_cut_loop(model,initial,max_cuts=max_psd_cuts)
    answer={"loop":loop,"joint_gap_point":None,"hull":None,"support_objective":None,
        "support":None,"refined_hull":None,"whole_prefix_infeasibility_proved":False,
        "full_joint_PSD_infeasibility_proved":loop["status"]=="EXACT_VALID_PSD_CUT_OBSTRUCTION"}
    points=[initial,*[base_certificate(model,s["analysis"]["primal"]) for s in loop["steps"][1:] if s["analysis"]["primal"]]]
    def finish(status):
        answer["status"]=status;answer["audit_wall_seconds"]=time.perf_counter()-start
        return answer
    if answer["full_joint_PSD_infeasibility_proved"]:return finish("EXACT_FIXED_WINDING_JOINT_PSD_OBSTRUCTION")
    if loop["status"]=="EXACT_PSD_CONTINUATION_NOT_NATIVE":
        cert=points[-1];answer["joint_gap_point"]={"primal":cert,"positivity":certify_psd(moment_matrix(model,cert["moments"])),"global_native_distribution_proved":False}
        return finish("EXACT_JOINT_PSD_CONTINUATION_NOT_NATIVE_PROOF")
    hull=mixture_search(model,points,denominator=8,exact_budget=8);answer["hull"]=hull
    positive=positive_hull_point(model,points,hull)
    if positive:
        answer["joint_gap_point"]=positive
        return finish("EXACT_JOINT_PSD_CONTINUATION_NOT_NATIVE_PROOF")
    separator=hull.get("hull_separator",{}).get("certificate")
    if not separator:return finish("JOINT_LOCAL_PSD_AUDIT_UNKNOWN")
    objective=sos_objective(model,hull["face"]["free_indices"],separator["vectors"],separator["nonnegative_weights"],allow_slacks=True)
    result=support_test(model,objective);answer["support_objective"]=objective;answer["support"]=result
    if result["dual"]:
        answer["full_joint_PSD_infeasibility_proved"]=True
        return finish("EXACT_FIXED_WINDING_JOINT_PSD_OBSTRUCTION")
    if not result["escape"]:return finish("JOINT_LOCAL_PSD_AUDIT_UNKNOWN")
    escape=base_certificate(model,result["escape"])
    result["escape_positivity"]=certify_psd(moment_matrix(model,escape["moments"]))
    if result["escape_positivity"]["ldl"]:
        answer["joint_gap_point"]={"primal":escape,"positivity":result["escape_positivity"],"global_native_distribution_proved":False}
        return finish("EXACT_JOINT_PSD_CONTINUATION_NOT_NATIVE_PROOF")
    refined=mixture_search(model,[*points,escape],denominator=8,exact_budget=8);answer["refined_hull"]=refined
    positive=positive_hull_point(model,[*points,escape],refined)
    if positive:
        answer["joint_gap_point"]=positive
        return finish("EXACT_JOINT_PSD_CONTINUATION_NOT_NATIVE_PROOF")
    return finish("JOINT_LOCAL_PSD_AUDIT_UNKNOWN")


def build_report(max_psd_cuts=3):
    paths={"local":LOCAL_REPORT,"support":SUPPORT_REPORT,"prefix":PREFIX_REPORT,"fixture":FIXTURE}
    raw={k:p.read_bytes() for k,p in paths.items()};data={k:json.loads(b) for k,b in raw.items()}
    local=data["local"];support=data["support"];prefixes=data["prefix"];fixture=data["fixture"]
    if local["source_support_report_sha256"]!=hashlib.sha256(raw["support"]).hexdigest() or any(support["source_sha256"][k]!=hashlib.sha256(raw[k]).hexdigest() for k in ("prefix","fixture")):
        raise ValueError("joint source hashes changed; regenerate in dependency order")
    cases=[]
    for c in local["cases"]:
        resolved=c["cut_resolve"]
        if not resolved["analysis"] or not resolved["analysis"]["primal"]:continue
        original=fixture["planted_geometry_probes"][c["fixture_probe_index"]]
        A=tuple(map(int,original["labels"]));Q=int(original["modulus"])
        problem=LowProblem((Q,),tuple(((a,),(b,)) for a,b in zip(A[::2],A[1::2])),0)
        policy=frozen_policy(problem,original["prepared"]);compiled=compile_adaptive(policy)
        pc=next(x for x in prefixes["cases"] if x["fixture_probe_index"]==c["fixture_probe_index"])
        pt=next(t for t in pc["trials"] if t["target"]==c["target"]);f=pt["frontier"]
        cp={"unassigned_rows":f["unassigned_rows"],"partial_coefficients":tuple(map(int,f["partial_coefficients"])),"assigned_squared_energy":f["assigned_squared_energy"]}
        g=frontier_geometry(problem,(int(c["target"]),),policy,compiled,cp);base=moment_model(g,c["winding_branch"])
        sc=next(x for x in support["cases"] if x["fixture_probe_index"]==c["fixture_probe_index"])
        st=next(t for t in sc["trials"] if t["target"]==c["target"])
        sr=next(r for r in st["winding_trials"] if r["winding_branch"]==c["winding_branch"])
        moments=sr["PSD_native_gap_certificate"]["moment_certificate"]["moments"]
        selected=[t for t in c["triple_trials"] if t["dual"]][:len(resolved["cuts"])];model=base
        for t,saved in zip(selected,resolved["cuts"]):
            model=append_local_cut(model,local_model(base,moments,t["blocks"]),t["dual"])
            if model["local_marginal_cuts"][-1]!=saved:raise ValueError("every saved local cut must reconstruct exactly")
        if len(selected)!=len(resolved["cuts"]):raise ValueError("complete source local-cut schedule required")
        result=audit_joint(model,resolved["analysis"]["primal"],max_psd_cuts)
        if result["joint_gap_point"]:
            if pt["status"]!="EXACT_WINDING_PREFIX_INTEGRALITY_GAP" or pt["native_truth"]["native_prefix_words"]!=[]:
                raise ValueError("joint relaxation GAP needs independently checked native emptiness")
            result["status"]="EXACT_NATIVE_JOINT_LOCAL_PSD_RELAXATION_GAP";result["native_empty_from_original_prefix_report"]=True
        # Initial proof is already retained in the hash-pinned local report.
        result["loop"]["steps"][0]["analysis"]["primal"]=None
        result["loop"]["steps"][0]["analysis"]["primal_from_local_report"]=True
        cases.append({"fixture_probe_index":c["fixture_probe_index"],"fingerprint":c["fingerprint"],
            "target":c["target"],"winding_branch":c["winding_branch"],"local_cut_count":len(selected),**result})
    return {"status":"BOUNDED_EXACT_JOINT_NATIVE_LOCAL_PSD_AUDIT_NOT_SOLVER","cases":cases,
        "source_sha256":{k:hashlib.sha256(b).hexdigest() for k,b in raw.items()},"PSD_cut_budget":max_psd_cuts,
        "hull_denominator":8,"hull_exact_candidate_budget":8,"support_tests_per_case_budget":1,
        "support_hull_refinement_budget":1,"local_derivations_review_pending":True,"novelty_claim":False,
        "polynomial_pair_finder_proved":False,"population_gap_proved":False}


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("--write",action="store_true");parser.add_argument("--PSD-cuts",type=int,default=3)
    args=parser.parse_args();report=build_report(args.PSD_cuts)
    if args.write:REPORT.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"status":report["status"],"case_statuses":dict(Counter(c["status"] for c in report["cases"]))},indent=2))
