"""Exact facial reduction and convex-mixture probes of native moment gaps.

LOCAL DERIVATIONS / REVIEW PENDING. A finite grid is only a proposal search.
Its failure never proves infeasibility of the convex hull or the full SDP.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import time

from flint import fmpq, fmpq_mat
import numpy as np
from scipy.optimize import linprog

from ternary_moment_psd import moment_matrix, certify_psd, quadratic_value, REPORT as PSD_REPORT
from ternary_prefix_moments import moment_model, verify_moments, REPORT as MOMENT_REPORT
from ternary_prefix_integrality import rational, frontier_geometry, REPORT as PREFIX_REPORT
from ternary_pair_collimation import LowProblem
from ternary_repair_catalog import FIXTURE, frozen_policy
from ternary_adaptive_shell import compile_adaptive

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"research/phase_workbench/ternary_moment_psd_mixtures.json"


def common_native_face(model, matrices):
    """Exact M=T*C*T^T for every supplied point, BEFORE optimizing its mixture.

    Source normalization and conditioned arithmetic equations force common
    moment kernels. Zero rows shared by this particular hull may reduce it
    further, but are NOT asserted for every feasible native moment point.
    """
    indicators=tuple(key for key in model["variables"] if key[0]=="p");n=len(indicators)+1
    if not matrices or any(len(A)!=n or any(len(row)!=n for row in A) for A in matrices):
        raise ValueError("correctly sized nonempty native matrix family required")
    if any(any(rational(A[i][j])!=rational(A[j][i]) for i in range(n) for j in range(i)) for A in matrices):
        raise ValueError("exact symmetric moment matrices required")
    relations=[]
    for j in range(len(model["geometry"]["domains"])):
        relations.append((-1,*(int(key[1]==j) for key in indicators)))
    for coefficients,B,_ in model["source_equations"]:
        relations.append((-B,*(coefficients[key[1]][key[2]] for key in indicators)))
    source_rows=len(relations)
    hull_zero_rows=[]
    for i in range(n):
        if all(all(rational(x)==0 for x in A[i]) for A in matrices):
            relations.append(tuple(int(i==j) for j in range(n)));hull_zero_rows.append(i)
    relation_matrix=fmpq_mat(relations);reduced,rank=relation_matrix.rref()
    pivots=[next(j for j in range(n) if reduced[i,j]) for i in range(rank)]
    transposed,_=relation_matrix.transpose().rref()
    independent_rows=[next(j for j in range(len(relations)) if transposed[i,j]) for i in range(rank)]
    minor=fmpq_mat([[relations[i][j] for j in pivots] for i in independent_rows]).det()
    if not minor:raise ArithmeticError("exact independent relation minor vanished")
    free=[j for j in range(n) if j not in pivots]
    if not free: raise ArithmeticError("constant moment cannot vanish in the entire face")
    T=[[fmpq(0)]*len(free) for _ in range(n)]
    for k,j in enumerate(free):T[j][k]=1
    for i,pivot in enumerate(pivots):
        for k,j in enumerate(free):T[pivot][k]=-reduced[i,j]
    tm=fmpq_mat(T);compressed=[]
    for A in matrices:
        am=fmpq_mat([[rational(x) for x in row] for row in A])
        C=tuple(tuple(rational(A[i][j]) for j in free) for i in free)
        if tm*fmpq_mat(C)*tm.transpose()!=am:
            raise ValueError("every original point must reconstruct exactly from the claimed common face")
        compressed.append(C)
    return {"matrix_dimension":n,"face_dimension":len(free),"relation_rank":rank,"free_indices":free,
        "source_relation_rows":source_rows,"hull_specific_zero_rows":hull_zero_rows,
        "independent_relation_rows":independent_rows,"independent_relation_columns":pivots,
        "nonzero_relation_minor_determinant":str(minor),
        "transformation":[[str(x) for x in row] for row in T],
        "source_relations":[[str(x) for x in row] for row in relations[:source_rows]],
        "all_original_matrices_reconstruct_exactly":True,
        "hull_zero_rows_not_a_global_native_constraint":True},tuple(compressed)


def _compositions(total,parts):
    if parts==1:
        yield (total,);return
    for i in range(total+1):
        for tail in _compositions(total-i,parts-1):yield (i,*tail)


def separate_supplied_hull(matrices, extra_vectors=()):
    """Exact PSD dual as a NONNEGATIVE sum of rational outer products.

    Strictly negative trace at every supplied point excludes its entire convex
    hull. It says nothing about other feasible moment points or the full SDP.
    """
    if not matrices:raise ValueError("nonempty supplied hull required")
    vectors=[tuple(rational(x) for x in v) for v in extra_vectors]
    for A in matrices:
        proof=certify_psd(A)
        if proof["negative"]:vectors.append(tuple(rational(x) for x in proof["negative"]["vector"]))
    vectors=list(dict.fromkeys(vectors))
    cost={"vector_count":len(vectors),"point_count":len(matrices),"LP_calls":0}
    if not vectors:return {"status":"HULL_SEPARATOR_UNKNOWN","certificate":None,"cost":cost}
    features=tuple(tuple(quadratic_value(A,v) for A in matrices) for v in vectors)
    def certificate(weights):
        w=tuple(rational(x) for x in weights)
        if len(w)!=len(vectors) or any(x<0 for x in w) or sum(w)!=1:
            raise ValueError("complete nonnegative normalized exact cone weights required")
        traces=tuple(sum((a*features[j][i] for j,a in enumerate(w)),fmpq(0)) for i in range(len(matrices)))
        if not all(x<0 for x in traces):return None
        return {"valid":True,"vectors":[[str(x) for x in v] for v in vectors],"nonnegative_weights":[str(x) for x in w],
            "point_trace_values":[str(x) for x in traces],"positive_semidefinite_dual_is_sum_of_squares":True,
            "proves_ONLY_supplied_convex_hull_has_no_psd_matrix":True,"full_SDP_infeasibility_proved":False}
    for j,row in enumerate(features):
        if all(x<0 for x in row):
            cert=certificate(tuple(int(i==j) for i in range(len(vectors))))
            return {"status":"EXACT_SUPPLIED_HULL_PSD_OBSTRUCTION","certificate":cert,"cost":cost}
    inequalities=np.array([[*(float(row[i]) for row in features),-1.0] for i in range(len(matrices))])
    cost["LP_calls"]=1
    result=linprog(np.array([*(0.0 for _ in vectors),1.0]),A_ub=inequalities,b_ub=np.zeros(len(matrices)),
        A_eq=np.array([[*(1.0 for _ in vectors),0.0]]),b_eq=np.array([1.0]),
        bounds=(*((0,None) for _ in vectors),(None,None)),method="highs-ds")
    if result.success:
        for limit in (1<<16,1<<24,1<<32):
            guessed=tuple(rational(Fraction(max(0,float(x))).limit_denominator(limit)) for x in result.x[:-1])
            total=sum(guessed)
            if not total:continue
            cert=certificate(tuple(x/total for x in guessed))
            if cert:return {"status":"EXACT_SUPPLIED_HULL_PSD_OBSTRUCTION","certificate":cert,"cost":cost}
    return {"status":"HULL_SEPARATOR_UNKNOWN","certificate":None,"cost":cost,
        "numerical_failure_not_convex_hull_or_full_SDP_feasibility":True}


def mixture_search(model, point_certificates, denominator=8, exact_budget=8, grid_budget=50_000):
    if any(type(x) is not int or x<1 for x in (denominator,exact_budget,grid_budget)):
        raise ValueError("positive explicit grid/exact/preflight budgets required")
    if not point_certificates:raise ValueError("nonempty certified convex-hull family required")
    start=time.perf_counter();N=len(model["variables"]);points=[];matrices=[]
    for cert in point_certificates:
        # Cut slack variables are not part of the base model or its moment matrix.
        values=tuple(rational(x) for x in cert["moments"][:N])
        if cert["required_winding"]!=model["required_winding"] or not verify_moments(model,values)["valid"]:
            raise ValueError("every supplied point must independently satisfy the SAME original winding model")
        points.append(values);matrices.append(moment_matrix(model,values))
    face,compressed=common_native_face(model,matrices);count=len(points);size=math.comb(denominator+count-1,count-1)
    cost={"grid_points_preflight":str(size),"grid_budget":grid_budget,"numeric_eigen_proposals":0,
        "exact_psd_checks":0,"exact_budget":exact_budget,"point_count":count}
    if size>grid_budget:
        return {"status":"CONVEX_PSD_GRID_PREFLIGHT_UNKNOWN","face":face,"attempts":[],"cost":cost,
            "global_native_distribution_proved":False,"full_SDP_infeasibility_proved":False}
    numeric=np.array([[[float(x) for x in row] for row in C] for C in compressed])
    candidates=[]
    for weights in _compositions(denominator,count):
        A=np.tensordot(np.array(weights,dtype=float)/denominator,numeric,axes=1)
        score=float(np.linalg.eigvalsh(A)[0]);cost["numeric_eigen_proposals"]+=1
        candidates.append((score,weights))
    candidates.sort(reverse=True);attempts=[]
    for _,weights in candidates[:exact_budget]:
        w=tuple(fmpq(x,denominator) for x in weights)
        C=tuple(tuple(sum((weight*matrix[i][j] for weight,matrix in zip(w,compressed)),fmpq(0))
                for j in range(face["face_dimension"])) for i in range(face["face_dimension"]))
        proof=certify_psd(C,compact=False);cost["exact_psd_checks"]+=1
        attempts.append({"weights":[str(x) for x in w],"compressed_positivity":proof})
        if proof["ldl"]:
            values=tuple(sum((weight*point[j] for weight,point in zip(w,points)),fmpq(0)) for j in range(N))
            if not verify_moments(model,values)["valid"]:raise ArithmeticError("exact convex mixture failed original native equations")
            cost["analysis_wall_seconds"]=time.perf_counter()-start
            return {"status":"EXACT_PSD_MOMENT_CONTINUATION_NOT_NATIVE_PROOF","face":face,"attempts":attempts,"cost":cost,
                "exact_convex_weights":attempts[-1]["weights"],"global_native_distribution_proved":False,
                "integer_prefix_completion_proved":False,"full_SDP_infeasibility_proved":False,
                "matrix_psd_from_exact_face_and_compressed_LDL":True}
    separator=separate_supplied_hull(compressed,[a["compressed_positivity"]["negative"]["vector"] for a in attempts if a["compressed_positivity"]["negative"]])
    cost["analysis_wall_seconds"]=time.perf_counter()-start
    return {"status":"EXACT_SUPPLIED_CONVEX_HULL_PSD_OBSTRUCTION" if separator["certificate"] else "CONVEX_HULL_PSD_SEARCH_UNKNOWN",
        "face":face,"attempts":attempts,"cost":cost,"hull_separator":separator,
        "global_native_distribution_proved":False,"full_SDP_infeasibility_proved":False,
        "grid_failure_not_convex_hull_or_native_infeasibility":True}


def build_report(denominator=8,exact_budget=8):
    psd_bytes=PSD_REPORT.read_bytes();moment_bytes=MOMENT_REPORT.read_bytes()
    psd=json.loads(psd_bytes);moments=json.loads(moment_bytes);prefixes=json.loads(PREFIX_REPORT.read_text());source=json.loads(FIXTURE.read_text());cases=[]
    for case in psd["cases"]:
        original=source["planted_geometry_probes"][case["fixture_probe_index"]]
        mc=next(c for c in moments["cases"] if c["fixture_probe_index"]==case["fixture_probe_index"])
        pc=next(c for c in prefixes["cases"] if c["fixture_probe_index"]==case["fixture_probe_index"])
        A=tuple(map(int,original["labels"]));Q=int(original["modulus"])
        problem=LowProblem((Q,),tuple(((a,),(c,)) for a,c in zip(A[::2],A[1::2])),0)
        policy=frozen_policy(problem,original["prepared"]);compiled=compile_adaptive(policy);trials=[]
        for old in case["trials"]:
            pt=next(t for t in pc["trials"] if t["target"]==old["target"]);mt=next(t for t in mc["trials"] if t["target"]==old["target"])
            f=pt["frontier"];cp={"unassigned_rows":f["unassigned_rows"],"partial_coefficients":tuple(map(int,f["partial_coefficients"])),"assigned_squared_energy":f["assigned_squared_energy"]}
            g=frontier_geometry(problem,(int(old["target"]),),policy,compiled,cp);runs=[]
            for run in old["winding_trials"]:
                if run["status"]!="PSD_CUT_CAP_UNKNOWN":continue
                mr=next(r for r in mt["winding_trials"] if r["winding_branch"]==run["winding_branch"])
                points=[mr["primal"],*(s["analysis"]["primal"] for s in run["steps"][1:] if s["analysis"]["primal"])]
                result=mixture_search(moment_model(g,run["winding_branch"]),points,denominator,exact_budget)
                if result["status"]=="EXACT_PSD_MOMENT_CONTINUATION_NOT_NATIVE_PROOF":
                    if pt["native_truth"]["native_prefix_words"]!=[]:raise ArithmeticError("a relaxation gap requires independently known native emptiness")
                    result["status"]="EXACT_PSD_NATIVE_RELAXATION_GAP";result["base_native_truth_verified_empty"]=True
                runs.append({"winding_branch":run["winding_branch"],**result})
            trials.append({"target":old["target"],"winding_trials":runs,
                "psd_gap_survives":any(r["status"]=="EXACT_PSD_NATIVE_RELAXATION_GAP" for r in runs),
                "only_cap_unknown_windings_probed":True,"prefix_eliminated":False})
        cases.append({"fixture_probe_index":case["fixture_probe_index"],"root_digits":case["root_digits"],"fingerprint":case["fingerprint"],"trials":trials})
    return {"status":"EXACT_NATIVE_MOMENT_FACE_AND_MIXTURE_PROBES_NOT_SOLVER",
        "source_psd_report_sha256":hashlib.sha256(psd_bytes).hexdigest(),"source_moment_report_sha256":hashlib.sha256(moment_bytes).hexdigest(),
        "local_derivations_review_pending":True,"novelty_claim":False,"polynomial_pair_finder_proved":False,
        "population_obstruction_proved":False,"grid_denominator":denominator,"exact_candidate_budget":exact_budget,"cases":cases}


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("--write",action="store_true");parser.add_argument("--denominator",type=int,default=8);parser.add_argument("--exact-candidates",type=int,default=8)
    args=parser.parse_args();report=build_report(args.denominator,args.exact_candidates)
    if args.write:REPORT.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"status":report["status"],"winding_statuses":dict(Counter(r["status"] for c in report["cases"] for t in c["trials"] for r in t["winding_trials"]))},indent=2))
