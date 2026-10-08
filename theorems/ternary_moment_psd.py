"""Exact native moment positivity and bounded, proof-carrying quadratic cuts.

LOCAL DERIVATIONS / REVIEW PENDING. PSD moments need not be a global native
distribution. A negative direction refutes a point, not an entire relaxation.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import time

from flint import fmpq, fmpq_mat
import numpy as np

from ternary_prefix_integrality import rational, frontier_geometry, REPORT as PREFIX_REPORT
from ternary_prefix_moments import moment_model, verify_moments, verify_moment_dual, analyze_moments, REPORT as MOMENT_REPORT
from ternary_pair_collimation import LowProblem
from ternary_repair_catalog import FIXTURE, frozen_policy
from ternary_adaptive_shell import compile_adaptive

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"research/phase_workbench/ternary_moment_psd.json"


def _square(matrix):
    n=len(matrix)
    if not n or any(len(row)!=n for row in matrix): raise ValueError("nonempty exact square matrix required")
    A=tuple(tuple(rational(x) for x in row) for row in matrix)
    if any(A[i][j]!=A[j][i] for i in range(n) for j in range(i)):
        raise ValueError("exact symmetric matrix required")
    return A


def quadratic_value(matrix, vector):
    A=_square(matrix); v=tuple(rational(x) for x in vector)
    if len(v)!=len(A): raise ValueError("complete exact vector required")
    return sum((v[i]*x*v[j] for i,row in enumerate(A) for j,x in enumerate(row)),fmpq(0))


def verify_negative(matrix, vector):
    value=quadratic_value(matrix,vector)
    return {"valid":value<0,"vector":[str(rational(x)) for x in vector],"quadratic_value":str(value)}


def verify_ldl(matrix, lower, diagonal):
    A=_square(matrix); n=len(A)
    if len(lower)!=n or any(len(row)!=n for row in lower) or len(diagonal)!=n:
        raise ValueError("full exact LDL dimensions required")
    L=tuple(tuple(rational(x) for x in row) for row in lower); D=tuple(rational(x) for x in diagonal)
    valid=all(L[i][i]==1 and all(L[i][j]==0 for j in range(i+1,n)) for i in range(n)) and all(x>=0 for x in D)
    if valid:
        lm=fmpq_mat(L); dm=fmpq_mat([[D[i] if i==j else 0 for j in range(n)] for i in range(n)])
        valid=lm*dm*lm.transpose()==fmpq_mat(A)
    return {"valid":valid,"lower":[[str(x) for x in row] for row in L],"diagonal":[str(x) for x in D],
        "proves_psd":valid,"matrix_dimension":n}


def certify_psd(matrix, compact=True):
    """Exact symmetric elimination, including singular pivot range tests."""
    A=_square(matrix); n=len(A); S=[list(row) for row in A]
    L=[[fmpq(int(i==j)) for j in range(n)] for i in range(n)]; D=[fmpq(0)]*n
    start=time.perf_counter(); updates=0
    def negative(y,pivot,reason):
        # Eliminate earlier completed positive squares in ORIGINAL coordinates.
        for k in range(pivot-1,-1,-1): y[k]=-sum((L[j][k]*y[j] for j in range(k+1,n)),fmpq(0))
        cert=verify_negative(A,y)
        if not cert["valid"]: raise ArithmeticError("exact Schur direction failed original-coordinate negativity")
        proposal_bits=None
        if compact:
            # Floating eigenvectors propose short cuts ONLY. Their exact rational
            # quadratic forms, not the eigenvalue, determine acceptance.
            try:
                _,vectors=np.linalg.eigh(np.array([[float(x) for x in row] for row in A]))
                for bits in (4,8,12,16):
                    v=tuple(int(round(float(x)*(1<<bits))) for x in vectors[:,0])
                    proposed=verify_negative(A,v)
                    if proposed["valid"]:
                        cert=proposed; proposal_bits=bits; break
            except (ValueError,OverflowError,np.linalg.LinAlgError):
                pass
        return {"status":"EXACT_INDEFINITE_MOMENT_MATRIX","negative":cert,"ldl":None,
            "matrix_dimension":n,"pivot":pivot,"pivot_reason":reason,"short_vector_proposal_bits":proposal_bits,
            "exact_schur_updates":updates,"analysis_wall_seconds":time.perf_counter()-start}
    for i in range(n):
        pivot=S[i][i]
        if pivot<0:
            y=[fmpq(0)]*n;y[i]=1
            return negative(y,i,"negative_diagonal")
        if pivot==0:
            j=next((j for j in range(i+1,n) if S[i][j]),None)
            if j is not None:
                y=[fmpq(0)]*n;y[j]=1;y[i]=-(S[j][j]+1)/(2*S[i][j])
                return negative(y,i,"zero_diagonal_nonzero_offdiagonal")
            continue
        D[i]=pivot
        for j in range(i+1,n): L[j][i]=S[j][i]/pivot
        for j in range(i+1,n):
            for k in range(j,n):
                S[j][k]-=S[j][i]*S[i][k]/pivot; S[k][j]=S[j][k]; updates+=1
    cert=verify_ldl(A,L,D)
    if not cert["valid"]: raise ArithmeticError("exact LDL reconstruction failed")
    return {"status":"EXACT_PSD_MOMENT_MATRIX","negative":None,"ldl":cert,"matrix_dimension":n,
        "exact_schur_updates":updates,"analysis_wall_seconds":time.perf_counter()-start}


def moment_matrix(model, values):
    cert=verify_moments(model,values)
    if not cert["valid"]: raise ValueError("all original and added moment rows must verify first")
    x=tuple(rational(a) for a in values); index={key:i for i,key in enumerate(model["variables"])}
    indicators=tuple(key for key in model["variables"] if key[0]=="p"); n=len(indicators)+1
    A=[[fmpq(0)]*n for _ in range(n)]; A[0][0]=1
    for i,key in enumerate(indicators,1):
        A[0][i]=A[i][0]=A[i][i]=x[index[key]]
        for j,other in enumerate(indicators[:i-1],1):
            if key[1]!=other[1]:
                a,b=sorted((key,other),key=lambda k:k[1])
                A[i][j]=A[j][i]=x[index[("J",a[1],a[2],b[1],b[2])]]
    return tuple(tuple(row) for row in A)


def append_psd_cut(model, vector):
    """Retain the exact nonnegative-square inequality using one nonnegative slack."""
    indicators=tuple(key for key in model["variables"] if key[0]=="p")
    if len(vector)!=len(indicators)+1: raise ValueError("vector must index constant and every original indicator")
    v=tuple(rational(x) for x in vector); by_key={key:v[i+1] for i,key in enumerate(indicators)}
    coefficients=[]
    for key in model["variables"]:
        if key[0]=="p": coefficients.append(2*v[0]*by_key[key]+by_key[key]**2)
        elif key[0]=="J": coefficients.append(2*by_key[("p",key[1],key[2])]*by_key[("p",key[3],key[4])])
        else: coefficients.append(fmpq(0))
    constant=v[0]**2; denominator=math.lcm(*(int(x.q) for x in (*coefficients,constant)))
    integral=tuple(int((a*denominator).p) for a in coefficients); c=int((constant*denominator).p)
    divisor=math.gcd(*integral,c)
    if divisor==0: raise ValueError("zero vector gives no nontrivial moment cut")
    integral=tuple(x//divisor for x in integral); c//=divisor
    N=len(model["variables"]); previous=model.get("psd_cuts",()); row={i:x for i,x in enumerate(integral) if x};row[N]=-1
    cut={"vector":[str(x) for x in v],"integer_coefficients":[str(x) for x in integral],"integer_constant":str(c),
        "clearing_denominator":str(denominator),"primitive_divisor":str(divisor),"slack_variable":N,
        "maximum_integer_coefficient_bits":max(abs(x).bit_length() for x in (*integral,c))}
    return {**model,"variables":(*model["variables"],("PSD_SLACK",len(previous))),"rows":(*model["rows"],row),
        "rhs":(*model["rhs"],-c),"row_names":(*model["row_names"],("PSD_CUT",len(previous))),
        "nonzero_entries":model["nonzero_entries"]+len(row),"psd_cuts":(*previous,cut)}


def psd_cut_loop(base, initial, max_cuts=3, max_exact_cells=500_000):
    if type(max_cuts) is not int or max_cuts<0: raise ValueError("nonnegative explicit PSD-cut budget required")
    if initial["required_winding"]!=base["required_winding"] or not verify_moments(base,initial["moments"])["valid"]:
        raise ValueError("initial certificate must belong to the exact base winding model")
    model=base; analysis={"status":"REUSED_EXACT_COUPLED_MOMENT_CONTINUATION","primal":initial,"dual":None,"cost":{"LP_calls":0}}
    steps=[]; start=time.perf_counter()
    def finish(status):
        return {"status":status,"required_winding":base["required_winding"],"cut_budget":max_cuts,
            "cuts_added":len(model.get("psd_cuts",())),"steps":steps,
            "LP_calls":sum(s["analysis"]["cost"]["LP_calls"] for s in steps),
            "loop_wall_seconds":time.perf_counter()-start,"integer_prefix_completion_proved":False}
    while True:
        step={"analysis":analysis};steps.append(step)
        if analysis["dual"]:
            c=analysis["dual"]
            if c["required_winding"]!=model["required_winding"]:raise ValueError("dual belongs to another winding model")
            checked=verify_moment_dual(model,c["signed_equation_multipliers"])
            if not checked["valid"]:raise ValueError("no cut obstruction without an exact dual recheck")
            analysis["dual"]=checked
            return finish("EXACT_VALID_PSD_CUT_OBSTRUCTION")
        if not analysis["primal"]: return finish("PSD_CUT_RECONSTRUCTION_UNKNOWN")
        if analysis["primal"]["required_winding"]!=model["required_winding"]:
            raise ValueError("primal belongs to another winding model")
        A=moment_matrix(model,analysis["primal"]["moments"]); psd=certify_psd(A);step["positivity"]=psd
        if psd["ldl"]: return finish("EXACT_PSD_CONTINUATION_NOT_NATIVE")
        if len(model.get("psd_cuts",()))==max_cuts: return finish("PSD_CUT_CAP_UNKNOWN")
        strengthened=append_psd_cut(model,psd["negative"]["vector"])
        cut=strengthened["psd_cuts"][-1]
        x=tuple(rational(a) for a in analysis["primal"]["moments"])
        lhs=fmpq(int(cut["integer_constant"]))+sum((int(a)*value for a,value in zip(cut["integer_coefficients"],x)),fmpq(0))
        if lhs>=0: raise ArithmeticError("new exact PSD cut does not reject the certified point")
        step["added_cut"]=cut; model=strengthened
        analysis=analyze_moments(model,max_exact_cells)


def build_report(max_cuts=3):
    moments=json.loads(MOMENT_REPORT.read_text()); prefixes=json.loads(PREFIX_REPORT.read_text()); source=json.loads(FIXTURE.read_text()); cases=[]
    for old_case in moments["cases"]:
        eligible=[t for t in old_case["trials"] if t["coupled_moment_survives"]]
        if not eligible: continue
        original=source["planted_geometry_probes"][old_case["fixture_probe_index"]]
        pc=next(c for c in prefixes["cases"] if c["fixture_probe_index"]==old_case["fixture_probe_index"])
        A=tuple(map(int,original["labels"]));Q=int(original["modulus"])
        problem=LowProblem((Q,),tuple(((a,),(c,)) for a,c in zip(A[::2],A[1::2])),0)
        policy=frozen_policy(problem,original["prepared"]);compiled=compile_adaptive(policy);trials=[]
        for old in eligible:
            saved=next(t for t in pc["trials"] if t["target"]==old["target"])["frontier"]
            cp={"unassigned_rows":saved["unassigned_rows"],"partial_coefficients":tuple(map(int,saved["partial_coefficients"])),"assigned_squared_energy":saved["assigned_squared_energy"]}
            g=frontier_geometry(problem,(int(old["target"]),),policy,compiled,cp);runs=[]
            for run in old["winding_trials"]:
                if run["primal"]:
                    model=moment_model(g,run["winding_branch"]); result=psd_cut_loop(model,run["primal"],max_cuts)
                    # This exact certificate is already retained in the linked,
                    # hash-pinned source report; avoid duplicating its large array.
                    result["steps"][0]["analysis"]["primal"]=None
                    result["steps"][0]["analysis"]["primal_from_source_report"]=True
                else:
                    result={"status":"REUSED_EXACT_MOMENT_OBSTRUCTION" if run["dual"] else "CARRIED_BASE_WINDING_UNKNOWN",
                        "required_winding":run["winding_branch"],"steps":[],"cuts_added":0,"LP_calls":0}
                runs.append({"winding_branch":run["winding_branch"],**result})
            eliminated=all(r["status"] in ("REUSED_EXACT_MOMENT_OBSTRUCTION","EXACT_VALID_PSD_CUT_OBSTRUCTION") for r in runs)
            trials.append({"target":old["target"],"all_allowed_windings":old["all_allowed_windings"],"winding_trials":runs,
                "prefix_eliminated":eliminated,"psd_continuation_survives":any(r["status"]=="EXACT_PSD_CONTINUATION_NOT_NATIVE" for r in runs)})
        cases.append({"fixture_probe_index":old_case["fixture_probe_index"],"root_digits":old_case["root_digits"],"fingerprint":old_case["fingerprint"],"trials":trials})
    return {"status":"EXACT_NATIVE_MOMENT_PSD_CUT_PILOT_NOT_SOLVER","source_moment_report":str(MOMENT_REPORT.relative_to(ROOT)),
        "source_moment_report_sha256":hashlib.sha256(MOMENT_REPORT.read_bytes()).hexdigest(),
        "local_derivations_review_pending":True,"novelty_claim":False,"polynomial_pair_finder_proved":False,
        "population_obstruction_proved":False,"cut_budget":max_cuts,"cases":cases}


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("--write",action="store_true");parser.add_argument("--cuts",type=int,default=3)
    args=parser.parse_args();report=build_report(args.cuts)
    if args.write: REPORT.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"status":report["status"],"winding_statuses":dict(Counter(r["status"] for c in report["cases"] for t in c["trials"] for r in t["winding_trials"]))},indent=2))
