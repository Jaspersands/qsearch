"""Exact pairwise native moments conditioned on all assigned prefix equations.

LOCAL DERIVATION / REVIEW PENDING. Polynomial-size classical relaxation only.
No floating LP status, locally consistent moments or fixed lift proves recovery.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import json
from pathlib import Path
import time

from flint import fmpq
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

from ternary_prefix_integrality import rational, exact_affine_proposal, frontier_geometry, REPORT as PREFIX_REPORT
from ternary_pair_collimation import LowProblem
from ternary_repair_catalog import FIXTURE, frozen_policy
from ternary_adaptive_shell import compile_adaptive
from ternary_pair_cell_coverage import integer_gs_directions

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"research/phase_workbench/ternary_prefix_moments.json"


def moment_model(g, winding=None):
    if winding is not None and type(winding) is not int:
        raise ValueError("exact integer winding required")
    domains=g["domains"]; M=len(domains); variables=[]; index={}
    for j,D in enumerate(domains):
        for digit in D:
            key=("p",j,digit); index[key]=len(variables); variables.append(key)
    for i in range(M):
        for j in range(i+1,M):
            for a in domains[i]:
                for b in domains[j]:
                    key=("J",i,a,j,b); index[key]=len(variables); variables.append(key)
    rows=[]; rhs=[]; names=[]
    def add(terms,B,name):
        row={}
        for key,a in terms:
            if a: row[index[key]]=row.get(index[key],0)+a
        rows.append({i:a for i,a in row.items() if a}); rhs.append(B); names.append(name)
    def joint(i,a,j,b):
        return ("J",i,a,j,b) if i<j else ("J",j,b,i,a)
    for j,D in enumerate(domains):
        add([(("p",j,a),1) for a in D],1,("normalize",j))
    for i in range(M):
        for j in range(i+1,M):
            for a in domains[i]:
                add([(joint(i,a,j,b),1) for b in domains[j]]+[(("p",i,a),-1)],0,("left_marginal",i,a,j))
            for b in domains[j]:
                add([(joint(i,a,j,b),1) for a in domains[i]]+[(("p",j,b),-1)],0,("right_marginal",i,j,b))
    equations=[]
    # The assigned GS integer direction h tests E(z): coefficients are
    # h_0-h_1 for u and h_0-h_2 for v. Anchor membership preserves its RHS.
    directions=integer_gs_directions(g["basis"]["rows"],g["basis"]["profile"])
    for i in range(g["bottom"],2*M):
        h=directions[i]["direction"]
        coefficients=tuple((0,h[3*j]-h[3*j+1],h[3*j]-h[3*j+2]) for j in range(M))
        B=sum(a*g["z_anchor"][2*j]+c*g["z_anchor"][2*j+1] for j,(_,a,c) in enumerate(coefficients))
        equations.append((coefficients,B,("assigned",i)))
    if winding is not None:
        equations.append((tuple((0,g["A"][2*j],g["A"][2*j+1]) for j in range(M)),g["target"][0]+g["Q"]*winding,("winding",winding)))
    for coefficients,B,name in equations:
        add([(("p",j,a),coefficients[j][a]) for j,D in enumerate(domains) for a in D],B,("mean",*name))
        for i,D in enumerate(domains):
            for a in D:
                terms=[(("p",i,a),coefficients[i][a]-B)]
                terms.extend((joint(i,a,j,b),coefficients[j][b]) for j,Dj in enumerate(domains) if j!=i for b in Dj)
                add(terms,0,("condition",*name,i,a))
    return {"geometry":g,"required_winding":winding,"variables":tuple(variables),"rows":tuple(rows),"rhs":tuple(rhs),
        "row_names":tuple(names),"source_equations":tuple(equations),
        "nonzero_entries":sum(len(row) for row in rows)}


def verify_moments(model, values):
    if len(values)!=len(model["variables"]): raise ValueError("complete exact native moment array required")
    x=tuple(rational(a) for a in values); issues=[]
    if any(a<0 for a in x): issues.append("negative native moment")
    for i,(row,B) in enumerate(zip(model["rows"],model["rhs"])):
        if sum((a*x[j] for j,a in row.items()),fmpq(0))!=B:
            issues.append(f"violated exact equation {i}")
    return {"valid":not issues,"issues":issues,"moments":[str(a) for a in x],
        "required_winding":model["required_winding"],"global_native_distribution_proved":False,
        "integer_prefix_completion_proved":False}


def word_moments(model, word):
    g=model["geometry"]
    if len(word)!=len(g["domains"]) or any(type(x) is not int or x not in D for x,D in zip(word,g["domains"])):
        raise ValueError("domain-valid original native word required")
    values=[]
    for key in model["variables"]:
        if key[0]=="p": values.append(int(word[key[1]]==key[2]))
        elif key[0]=="J": values.append(int(word[key[1]]==key[2] and word[key[3]]==key[4]))
        elif key[0]=="PSD_SLACK":
            cut=model["psd_cuts"][key[1]]
            values.append(int(cut["integer_constant"])+sum(int(a)*x for a,x in zip(cut["integer_coefficients"],values)))
        elif key[0]=="LOCAL_SLACK":
            cut=model["local_marginal_cuts"][key[1]]
            values.append(sum(int(a)*values[int(j)] for j,a in cut["integer_coefficients"].items()))
        else: raise ValueError("unknown native moment variable")
    return tuple(values)


def verify_moment_dual(model, weights):
    if len(weights)!=len(model["rows"]): raise ValueError("complete exact signed equation multipliers required")
    y=tuple(rational(x) for x in weights); columns=[fmpq(0)]*len(model["variables"])
    for weight,row in zip(y,model["rows"]):
        if weight:
            for j,a in row.items(): columns[j]+=weight*a
    rhs=sum((weight*B for weight,B in zip(y,model["rhs"])),fmpq(0)); issues=[]
    if any(a<0 for a in columns): issues.append("negative column is incompatible with nonnegative native moments")
    if rhs>=0: issues.append("combined exact right hand side not strictly negative")
    return {"valid":not issues,"issues":issues,"signed_equation_multipliers":[str(x) for x in y],
        "exact_column_coefficients":[str(x) for x in columns],"exact_combined_rhs":str(rhs),
        "required_winding":model["required_winding"],"proves_no_coupled_moments":not issues}


def _numeric_matrix(model):
    scales=[max((1,*(abs(a) for a in row.values()))) for row in model["rows"]]
    data=[]; rows=[]; cols=[]
    for i,(row,scale) in enumerate(zip(model["rows"],scales)):
        for j,a in row.items(): rows.append(i); cols.append(j); data.append(float(Fraction(a,scale)))
    matrix=coo_matrix((data,(rows,cols)),shape=(len(model["rows"]),len(model["variables"]))).tocsr()
    rhs=np.array([float(Fraction(B,s)) for B,s in zip(model["rhs"],scales)])
    return matrix,rhs,scales


def analyze_moments(model,max_exact_cells=500_000):
    if type(max_exact_cells) is not int or max_exact_cells<1: raise ValueError("positive exact-reconstruction preflight required")
    analysis_start=time.perf_counter()
    E,B,scales=_numeric_matrix(model); N=len(model["variables"]); R=len(model["rows"])
    start=time.perf_counter(); cost={"LP_calls":1,"variables":N,"equations":R,"nonzero_entries":model["nonzero_entries"],
        "exact_reconstruction_cells_budget":max_exact_cells,"reconstruction_attempts":0,"reconstruction_guard_skips":0}
    def finish(answer):
        cost["analysis_wall_seconds_including_exact_reconstruction"]=time.perf_counter()-analysis_start
        return answer
    solution=linprog(np.zeros(N),A_eq=E,b_eq=B,bounds=(0,None),method="highs-ds",options={"time_limit":10.0,"maxiter":20_000})
    cost["LP_seconds"]=time.perf_counter()-start
    cost["primal_numeric_status"]=int(getattr(solution,"status",0))
    if solution.success:
        if np.asarray(solution.x).shape!=(N,) or not np.isfinite(solution.x).all():
            raise ValueError("finite correctly sized native moment proposal required")
        seen=set()
        for tolerance in (1e-8,1e-12,0):
            support=[i for i,x in enumerate(solution.x) if x>tolerance]
            if tuple(support) in seen: continue
            seen.add(tuple(support))
            if R*(len(support)+1)>max_exact_cells:
                cost["reconstruction_guard_skips"]+=1; continue
            cost["reconstruction_attempts"]+=1
            augmented=[[*(row.get(j,0) for j in support),b] for row,b in zip(model["rows"],model["rhs"])]
            for selected,meta in exact_affine_proposal(augmented,solution.x[support]):
                full=[fmpq(0)]*N
                for i,x in zip(support,selected): full[i]=x
                cert=verify_moments(model,full)
                if cert["valid"]: return finish({"status":"EXACT_COUPLED_MOMENT_CONTINUATION","primal":cert,"dual":None,"cost":cost,**meta})
        return finish({"status":"PRIMAL_PROPOSAL_NO_EXACT_CERTIFICATE","primal":None,"dual":None,"cost":cost,"unknown_not_infeasible":True})
    # Equality Farkas alternative: E^T*y>=0, B^T*y<0. Numerical signs are not
    # proof authority. Recover original unscaled equation multipliers exactly.
    cost["LP_calls"]+=1; start=time.perf_counter()
    dual=linprog(np.zeros(R),A_ub=-E.transpose(),b_ub=np.zeros(N),A_eq=B.reshape(1,-1),b_eq=np.array([-1.0]),
        bounds=(None,None),method="highs-ds",options={"time_limit":10.0,"maxiter":20_000})
    cost["dual_LP_seconds"]=time.perf_counter()-start
    cost["dual_numeric_status"]=int(getattr(dual,"status",0))
    if dual.success:
        if np.asarray(dual.x).shape!=(R,) or not np.isfinite(dual.x).all():
            raise ValueError("finite correctly sized native dual proposal required")
        proposal=dual.x/np.array(scales,dtype=float)
        seen=set()
        for tolerance in (1e-8,1e-12,0):
            support=[i for i,x in enumerate(dual.x) if abs(x)>tolerance]
            if tuple(support) in seen: continue
            seen.add(tuple(support))
            if (N+1)*(len(support)+1)>max_exact_cells:
                cost["reconstruction_guard_skips"]+=1; continue
            # Only proposed zero columns need equality reconstruction; every
            # unselected column is still checked for exact nonnegativity.
            numer=np.asarray(E.transpose()@dual.x).reshape(-1)
            active=[j for j,x in enumerate(numer) if abs(x)<=1e-7]
            augmented=[[*[model["rhs"][i] for i in support],-1]]
            augmented.extend([*[model["rows"][i].get(j,0) for i in support],0] for j in active)
            cost["reconstruction_attempts"]+=1
            for selected,meta in exact_affine_proposal(augmented,proposal[support]):
                full=[fmpq(0)]*R
                for i,x in zip(support,selected): full[i]=x
                cert=verify_moment_dual(model,full)
                if cert["valid"]: return finish({"status":"EXACT_COUPLED_MOMENT_OBSTRUCTION","primal":None,"dual":cert,"cost":cost,**meta})
    return finish({"status":"COUPLED_MOMENT_ANALYSIS_UNKNOWN","primal":None,"dual":None,"cost":cost,
        "numerical_infeasibility_not_proof":True})


def build_report(max_prefixes=1):
    if type(max_prefixes) is not int or max_prefixes<1: raise ValueError("positive explicit prefix count required")
    old=json.loads(PREFIX_REPORT.read_text()); source=json.loads(FIXTURE.read_text()); cases=[]; done=0
    for case in old["cases"]:
        eligible=[t for t in case["trials"] if t["status"]=="EXACT_WINDING_PREFIX_INTEGRALITY_GAP"]
        if not eligible or done>=max_prefixes: continue
        original=source["planted_geometry_probes"][case["fixture_probe_index"]]
        A=tuple(map(int,original["labels"]));Q=int(original["modulus"])
        problem=LowProblem((Q,),tuple(((a,),(c,)) for a,c in zip(A[::2],A[1::2])),0)
        policy=frozen_policy(problem,original["prepared"]); compiled=compile_adaptive(policy); trials=[]
        for t in eligible:
            if done>=max_prefixes: break
            f=t["frontier"]; checkpoint={"unassigned_rows":f["unassigned_rows"],"partial_coefficients":tuple(map(int,f["partial_coefficients"])),"assigned_squared_energy":f["assigned_squared_energy"]}
            g=frontier_geometry(problem,(int(t["target"]),),policy,compiled,checkpoint); runs=[]
            for k in g["allowed_integral_windings"]:
                start=time.perf_counter(); model=moment_model(g,k); build_seconds=time.perf_counter()-start
                result=analyze_moments(model); result["cost"]["model_build_seconds"]=build_seconds
                runs.append({"winding_branch":k,**result})
            trials.append({"target":t["target"],"all_allowed_windings":list(g["allowed_integral_windings"]),"winding_trials":runs,
                "prefix_eliminated":all(r["dual"] and r["dual"]["valid"] for r in runs),
                "coupled_moment_survives":any(r["primal"] and r["primal"]["valid"] for r in runs)})
            done+=1
        cases.append({"fixture_probe_index":case["fixture_probe_index"],"root_digits":case["root_digits"],"fingerprint":case["fingerprint"],"trials":trials})
    return {"status":"EXACT_COUPLED_NATIVE_MOMENT_PILOT_NOT_SOLVER","local_derivations_review_pending":True,"novelty_claim":False,
        "polynomial_pair_finder_proved":False,"population_obstruction_proved":False,"prefix_budget":max_prefixes,"prefixes_analyzed":done,"cases":cases}


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("--write",action="store_true");parser.add_argument("--prefixes",type=int,default=1)
    args=parser.parse_args(); report=build_report(args.prefixes)
    if args.write: REPORT.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"status":report["status"],"prefixes":report["prefixes_analyzed"],"winding_statuses":dict(Counter(r["status"] for c in report["cases"] for t in c["trials"] for r in t["winding_trials"]))},indent=2))
