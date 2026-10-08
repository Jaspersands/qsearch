"""Lift finite-hull SOS separators to exact support tests of native moments.

LOCAL DERIVATIONS / REVIEW PENDING. Principal-coordinate embedding imposes
no hull-specific constraints. Numerical optimizers propose, never certify.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import time

from flint import fmpq
import numpy as np
from scipy.optimize import linprog

from ternary_prefix_integrality import rational, exact_affine_proposal, frontier_geometry, REPORT as PREFIX_REPORT
from ternary_prefix_moments import moment_model, verify_moments, _numeric_matrix, REPORT as MOMENT_REPORT
from ternary_moment_psd import moment_matrix, quadratic_value, certify_psd, REPORT as PSD_REPORT
from ternary_moment_psd_mixtures import mixture_search, REPORT as HULL_REPORT
from ternary_pair_collimation import LowProblem
from ternary_repair_catalog import FIXTURE, frozen_policy
from ternary_adaptive_shell import compile_adaptive

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"research/phase_workbench/ternary_psd_support_lift.json"


def _integer(value):
    q=rational(value)
    if q.q!=1:raise ValueError("exact integer objective normalization required")
    return int(q.p)


def sos_objective(model, free_indices, vectors, weights, allow_slacks=False):
    """Embed principal vectors by ZERO, not the hull reconstruction map T."""
    indicators=tuple(key for key in model["variables"] if key[0]=="p")
    if type(allow_slacks) is not bool:raise ValueError("explicit boolean slack-model scope required")
    allowed=("p","J","LOCAL_SLACK","PSD_SLACK") if allow_slacks else ("p","J")
    if any(key[0] not in allowed for key in model["variables"]):
        raise ValueError("original unstrengthened p/J model required")
    n=len(indicators)+1; free=tuple(free_indices)
    if not free or len(set(free))!=len(free) or any(type(i) is not int or not 0<=i<n for i in free):
        raise ValueError("distinct in-range principal indices required")
    w=tuple(rational(a) for a in weights)
    if not vectors or len(w)!=len(vectors) or any(a<0 for a in w) or sum(w)!=1:
        raise ValueError("complete nonnegative normalized exact SOS weights required")
    full=[]
    for vector in vectors:
        if len(vector)!=len(free):raise ValueError("complete exact principal vector required")
        v=[fmpq(0)]*n
        for i,a in zip(free,vector):v[i]=rational(a)
        full.append(tuple(v))
    active=[(a,v) for a,v in zip(w,full) if a]
    constant=sum((a*v[0]**2 for a,v in active),fmpq(0)); coefficients=[]
    lookup={key:i+1 for i,key in enumerate(indicators)}
    for key in model["variables"]:
        if key[0]=="p":
            i=lookup[key];value=sum((a*(2*v[0]*v[i]+v[i]**2) for a,v in active),fmpq(0))
        elif key[0]=="J":
            i=lookup[("p",key[1],key[2])];j=lookup[("p",key[3],key[4])]
            value=sum((2*a*v[i]*v[j] for a,v in active),fmpq(0))
        else:value=fmpq(0)
        coefficients.append(value)
    denominator=math.lcm(*(int(x.q) for x in (*coefficients,constant)))
    integers=tuple(int((a*denominator).p) for a in coefficients); k=int((constant*denominator).p)
    divisor=math.gcd(*integers,k)
    if not divisor:raise ValueError("identically zero SOS moment functional")
    integers=tuple(a//divisor for a in integers);k//=divisor
    result={"principal_indices":list(free),"embedded_vectors":[[str(a) for a in v] for v in full],
        "nonnegative_weights":[str(a) for a in w],"integer_coefficients":[str(fmpq(a)) for a in integers],
        "integer_constant":str(fmpq(k)),"clearing_denominator":str(fmpq(denominator)),"primitive_divisor":str(fmpq(divisor)),
        "required_winding":model["required_winding"],"hull_specific_constraints_added":False,
        "maximum_integer_coefficient_bits":max(abs(a).bit_length() for a in (*integers,k))}
    if allow_slacks:result["allow_slacks"]=True;result["support_model_scope"]="SUPPLIED_MODEL_WITH_EXPLICIT_NONNEGATIVE_SLACKS"
    return result


def verify_objective(model, objective):
    if objective["required_winding"]!=model["required_winding"]:
        raise ValueError("SOS objective belongs to another winding model")
    free=objective["principal_indices"]; full=objective["embedded_vectors"]
    n=1+sum(key[0]=="p" for key in model["variables"])
    if any(len(v)!=n for v in full):raise ValueError("complete original indicator embedding required")
    if any(rational(a)!=0 for v in full for i,a in enumerate(v) if i not in free):
        raise ValueError("embedding must vanish outside its principal coordinates")
    checked=sos_objective(model,free,[[v[i] for i in free] for v in full],objective["nonnegative_weights"],objective.get("allow_slacks",False))
    if checked!=objective:raise ValueError("SOS functional must exactly match its canonical original-coordinate expansion")
    return tuple(_integer(a) for a in checked["integer_coefficients"]),_integer(checked["integer_constant"])


def functional_value(model, objective, values):
    c,k=verify_objective(model,objective)
    if len(values)!=len(c):raise ValueError("complete exact moment array required")
    return fmpq(k)+sum((a*rational(x) for a,x in zip(c,values)),fmpq(0))


def verify_escape(model, objective, values):
    cert=verify_moments(model,values); value=functional_value(model,objective,values)
    return {**cert,"valid":cert["valid"] and value>=0,
        "issues":[*cert["issues"],*(["SOS functional remains strictly negative"] if value<0 else [])],
        "exact_functional_value":str(value),"proves_escape_from_THIS_dual_only":cert["valid"] and value>=0,
        "matrix_PSD_proved":False}


def verify_support_dual(model, objective, weights):
    c,k=verify_objective(model,objective)
    if len(weights)!=len(model["rows"]):raise ValueError("complete exact signed support dual required")
    y=tuple(rational(x) for x in weights); columns=[fmpq(0)]*len(c)
    for a,row in zip(y,model["rows"]):
        if a:
            for j,b in row.items():columns[j]+=a*b
    slacks=tuple(a-b for a,b in zip(columns,c))
    upper=fmpq(k)+sum((a*b for a,b in zip(y,model["rhs"])),fmpq(0));issues=[]
    if any(a<0 for a in slacks):issues.append("exact E^T y does not dominate every objective column")
    if upper>=0:issues.append("exact global SOS upper bound is not strictly negative")
    return {"valid":not issues,"issues":issues,"signed_equation_multipliers":[str(a) for a in y],
        "exact_column_slacks":[str(a) for a in slacks],"exact_functional_upper_bound":str(upper),
        "required_winding":model["required_winding"],"full_degree_two_SDP_infeasibility_proved":not issues,
        "whole_prefix_infeasibility_proved":False}


def support_test(model, objective, max_exact_cells=500_000):
    if type(max_exact_cells) is not int or max_exact_cells<1:raise ValueError("positive exact-reconstruction preflight required")
    c,k=verify_objective(model,objective);start=time.perf_counter()
    E,B,scales=_numeric_matrix(model);N=len(c);R=len(model["rows"])
    scale=max(1,*(abs(a) for a in c));cn=np.array([float(fmpq(a,scale)) for a in c])
    cost={"LP_calls":0,"variables":N,"equations":R,"nonzero_entries":model["nonzero_entries"],
        "exact_reconstruction_cells_budget":max_exact_cells,"reconstruction_attempts":0,"reconstruction_guard_skips":0,
        "objective_numeric_scale":str(fmpq(scale))}
    def finish(status,escape=None,dual=None):
        cost["analysis_wall_seconds_including_exact_reconstruction"]=time.perf_counter()-start
        return {"status":status,"escape":escape,"dual":dual,"cost":cost,
            "numerical_optimality_is_not_proof":True,"whole_prefix_infeasibility_proved":False,
            "full_degree_two_SDP_infeasibility_proved":bool(dual and dual["valid"])}
    cost["LP_calls"]+=1;lp_start=time.perf_counter()
    solution=linprog(-cn,A_eq=E,b_eq=B,bounds=(0,None),method="highs-ds",options={"time_limit":10.0,"maxiter":20_000})
    cost["support_LP_seconds"]=time.perf_counter()-lp_start;cost["support_numeric_status"]=int(solution.status)
    exact_negative=None
    if solution.success:
        if np.asarray(solution.x).shape!=(N,) or not np.isfinite(solution.x).all():raise ValueError("finite complete support-point proposal required")
        seen=set()
        for tolerance in (1e-8,1e-12,0):
            support=tuple(i for i,x in enumerate(solution.x) if x>tolerance)
            if support in seen:continue
            seen.add(support)
            if R*(len(support)+1)>max_exact_cells:cost["reconstruction_guard_skips"]+=1;continue
            cost["reconstruction_attempts"]+=1
            augmented=[[*(row.get(j,0) for j in support),b] for row,b in zip(model["rows"],model["rhs"])]
            for selected,_ in exact_affine_proposal(augmented,solution.x[list(support)]):
                full=[fmpq(0)]*N
                for j,x in zip(support,selected):full[j]=x
                cert=verify_escape(model,objective,full)
                if cert["valid"]:
                    return finish("EXACT_BASE_MOMENT_ESCAPE_FROM_HULL_DUAL",escape=cert)
                if verify_moments(model,full)["valid"]:exact_negative=str(functional_value(model,objective,full))
    cost["exact_negative_point_value_not_global_bound"]=exact_negative
    def reconstruct_dual(proposed_scaled):
        if np.asarray(proposed_scaled).shape!=(R,) or not np.isfinite(proposed_scaled).all():
            raise ValueError("finite complete scaled support-dual proposal required")
        # Reconstruct y/scale against exact c/scale, then multiply EXACTLY.
        # Clearing an SOS denominator can yield integers too large for float.
        proposal=proposed_scaled/np.array(scales,dtype=float)
        slack=np.asarray(E.transpose()@proposed_scaled).reshape(-1)-cn
        active=[j for j,x in enumerate(slack) if abs(x)<=1e-7];seen=set()
        for tolerance in (1e-8,1e-12,0):
            support=tuple(i for i,x in enumerate(proposed_scaled) if abs(x)>tolerance)
            if support in seen:continue
            seen.add(support)
            if (N+1)*(len(support)+1)>max_exact_cells:cost["reconstruction_guard_skips"]+=1;continue
            cost["reconstruction_attempts"]+=1
            augmented=[[*[model["rows"][i].get(j,0) for i in support],fmpq(c[j],scale)] for j in active]
            if not augmented:continue
            for selected,_ in exact_affine_proposal(augmented,proposal[list(support)]):
                full=[fmpq(0)]*R
                for i,x in zip(support,selected):full[i]=x*scale
                cert=verify_support_dual(model,objective,full)
                if cert["valid"]:return cert
        return None
    if solution.success:
        # HiGHS solved min(-c.x); negate its equality marginals for max(c.x).
        cert=reconstruct_dual(-np.asarray(solution.eqlin.marginals))
        if cert:return finish("EXACT_GLOBAL_DEGREE_TWO_PSD_OBSTRUCTION",dual=cert)
    cost["LP_calls"]+=1;lp_start=time.perf_counter()
    dual=linprog(B,A_ub=-E.transpose(),b_ub=-cn,bounds=(None,None),method="highs-ds",options={"time_limit":10.0,"maxiter":20_000})
    cost["dual_LP_seconds"]=time.perf_counter()-lp_start;cost["dual_numeric_status"]=int(dual.status)
    if dual.success:
        cert=reconstruct_dual(np.asarray(dual.x))
        if cert:return finish("EXACT_GLOBAL_DEGREE_TWO_PSD_OBSTRUCTION",dual=cert)
    return finish("GLOBAL_PSD_SUPPORT_RECONSTRUCTION_UNKNOWN")


def refine_with_escape(model, original_points, escape, max_exact_cells=500_000):
    """ONE new source-aware hull; at most one further support LP per winding."""
    if escape["required_winding"]!=model["required_winding"]:
        raise ValueError("hull escape belongs to another winding")
    if not verify_moments(model,escape["moments"])["valid"]:
        raise ValueError("hull refinement needs an independently verified base point")
    refined=mixture_search(model,[*original_points,escape],denominator=8,exact_budget=8)
    result={"expanded_hull":refined,"next_objective":None,"next_support":None,"refinement_rounds":1}
    saved=refined.get("hull_separator",{}).get("certificate")
    if saved:
        objective=sos_objective(model,refined["face"]["free_indices"],saved["vectors"],saved["nonnegative_weights"])
        support=support_test(model,objective,max_exact_cells)
        if support["escape"]:support["escape_positivity"]=certify_psd(moment_matrix(model,support["escape"]["moments"]))
        result["next_objective"]=objective;result["next_support"]=support
    return result


def build_report(max_exact_cells=500_000):
    sources={"hull":HULL_REPORT,"psd":PSD_REPORT,"moment":MOMENT_REPORT,"prefix":PREFIX_REPORT,"fixture":FIXTURE}
    raw={name:p.read_bytes() for name,p in sources.items()};data={name:json.loads(b) for name,b in raw.items()}
    hull=data["hull"];psd=data["psd"];moments=data["moment"];prefixes=data["prefix"];source=data["fixture"]
    if hull["source_psd_report_sha256"]!=hashlib.sha256(raw["psd"]).hexdigest() or hull["source_moment_report_sha256"]!=hashlib.sha256(raw["moment"]).hexdigest():
        raise ValueError("upstream hull source hashes changed; regenerate in dependency order")
    cases=[]
    for hc in hull["cases"]:
        pc=next(c for c in prefixes["cases"] if c["fixture_probe_index"]==hc["fixture_probe_index"])
        mc=next(c for c in moments["cases"] if c["fixture_probe_index"]==hc["fixture_probe_index"])
        sc=next(c for c in psd["cases"] if c["fixture_probe_index"]==hc["fixture_probe_index"])
        original=source["planted_geometry_probes"][hc["fixture_probe_index"]]
        A=tuple(map(int,original["labels"]));Q=int(original["modulus"])
        problem=LowProblem((Q,),tuple(((a,),(c,)) for a,c in zip(A[::2],A[1::2])),0)
        policy=frozen_policy(problem,original["prepared"]);compiled=compile_adaptive(policy);trials=[]
        for ht in hc["trials"]:
            pt=next(t for t in pc["trials"] if t["target"]==ht["target"])
            mt=next(t for t in mc["trials"] if t["target"]==ht["target"])
            st=next(t for t in sc["trials"] if t["target"]==ht["target"])
            f=pt["frontier"];cp={"unassigned_rows":f["unassigned_rows"],"partial_coefficients":tuple(map(int,f["partial_coefficients"])),"assigned_squared_energy":f["assigned_squared_energy"]}
            g=frontier_geometry(problem,(int(ht["target"]),),policy,compiled,cp);runs=[]
            for old in ht["winding_trials"]:
                if old["status"]!="EXACT_SUPPLIED_CONVEX_HULL_PSD_OBSTRUCTION":continue
                k=old["winding_branch"];build_start=time.perf_counter();model=moment_model(g,k)
                build_seconds=time.perf_counter()-build_start
                saved=old["hull_separator"]["certificate"]
                objective=sos_objective(model,old["face"]["free_indices"],saved["vectors"],saved["nonnegative_weights"])
                mr=next(r for r in mt["winding_trials"] if r["winding_branch"]==k)
                sr=next(r for r in st["winding_trials"] if r["winding_branch"]==k)
                points=[mr["primal"],*(s["analysis"]["primal"] for s in sr["steps"][1:] if s["analysis"]["primal"])]
                trace_values=[]
                for cert,trace in zip(points,saved["point_trace_values"]):
                    values=cert["moments"][:len(model["variables"])];matrix=moment_matrix(model,values)
                    exact_trace=sum((rational(a)*quadratic_value(matrix,v) for a,v in zip(objective["nonnegative_weights"],objective["embedded_vectors"])),fmpq(0))
                    value=functional_value(model,objective,values)
                    if exact_trace!=rational(trace) or value!=exact_trace*_integer(objective["clearing_denominator"])/_integer(objective["primitive_divisor"]):
                        raise ArithmeticError("principal embedding/original SOS functional trace identity failed")
                    trace_values.append(str(value))
                if len(points)!=len(saved["point_trace_values"]):raise ValueError("complete original supplied hull trace schedule required")
                result=support_test(model,objective,max_exact_cells);result["cost"]["model_build_seconds"]=build_seconds
                if result["escape"]:
                    result["escape_positivity"]=certify_psd(moment_matrix(model,result["escape"]["moments"]))
                    base_points=[{**p,"moments":p["moments"][:len(model["variables"])]} for p in points]
                    result["refinement"]=refine_with_escape(model,base_points,result["escape"],max_exact_cells)
                    h=result["refinement"]["expanded_hull"]
                    if h["status"]=="EXACT_PSD_MOMENT_CONTINUATION_NOT_NATIVE_PROOF":
                        if pt["status"]!="EXACT_WINDING_PREFIX_INTEGRALITY_GAP" or pt["native_truth"]["native_prefix_words"]!=[]:
                            raise ValueError("a native relaxation gap requires independently verified original prefix emptiness")
                        w=tuple(rational(a) for a in h["exact_convex_weights"])
                        supplied=[*base_points,result["escape"]]
                        values=tuple(sum((a*rational(p["moments"][j]) for a,p in zip(w,supplied)),fmpq(0)) for j in range(len(model["variables"])))
                        cert=verify_moments(model,values)
                        if not cert["valid"]:raise ArithmeticError("PSD convex mixture failed the entire original moment model")
                        result["PSD_native_gap_certificate"]={"moment_certificate":cert,
                            "PSD_proof_is_expanded_hull_exact_face_and_LDL":True,
                            "native_prefix_empty_from_independently_checked_original_report":True,
                            "proves_degree_two_gap_for_THIS_prefix_winding":True,
                            "population_gap_or_general_hierarchy_lower_bound_proved":False}
                runs.append({"winding_branch":k,"objective":objective,"old_hull_functional_values":trace_values,**result})
            trials.append({"target":ht["target"],"all_allowed_windings":list(g["allowed_integral_windings"]),"winding_trials":runs,
                "prefix_eliminated":False,"old_winding_unknowns_not_resolved":True})
        cases.append({"fixture_probe_index":hc["fixture_probe_index"],"root_digits":hc["root_digits"],"fingerprint":hc["fingerprint"],"trials":trials})
    return {"status":"EXACT_GLOBAL_SUPPORT_TEST_OF_SUPPLIED_HULL_PSD_DUALS_NOT_SOLVER",
        "source_sha256":{name:hashlib.sha256(b).hexdigest() for name,b in raw.items()},"cases":cases,
        "local_derivations_review_pending":True,"novelty_claim":False,"polynomial_pair_finder_proved":False,
        "population_obstruction_proved":False,"max_exact_reconstruction_cells":max_exact_cells,
        "hull_refinement_round_budget":1,"refinement_grid_denominator":8,"refinement_exact_candidate_budget":8}


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("--write",action="store_true");parser.add_argument("--exact-cells",type=int,default=500_000)
    args=parser.parse_args();report=build_report(args.exact_cells)
    if args.write:REPORT.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"status":report["status"],"winding_statuses":dict(Counter(r["status"] for c in report["cases"] for t in c["trials"] for r in t["winding_trials"]))},indent=2))
