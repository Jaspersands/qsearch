"""Exact primal certificates for native prefix relaxations and integrality gaps.

LOCAL DERIVATIONS / REVIEW PENDING. Numerical LP only proposes active rows.
Primal membership is checked exactly; native truth uses exponential references.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import product
import json
import math
from pathlib import Path
import time

from flint import fmpq, fmpq_mat
import numpy as np
from scipy.optimize import linprog

from ternary_pair_collimation import LowProblem, _value
from ternary_pair_lattice import coset_target, scalar_labels, word_coordinates, embed
from ternary_repair_catalog import frozen_policy, _target_coordinates, FIXTURE
from ternary_adaptive_shell import adaptive_pair, compile_adaptive, native_domains
from ternary_native_dual_separation import project_high

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/ternary_prefix_integrality.json"


def rational(value):
    if type(value) is int:
        return fmpq(value)
    if isinstance(value, fmpq):
        return value
    if type(value) is Fraction:
        return fmpq(value.numerator, value.denominator)
    if type(value) is str:
        # FLINT parses large exact certificates without Python's decimal-int
        # string cap. Canonical equality still rejects decimals and aliases.
        try:
            x = fmpq(value)
        except (ValueError, TypeError, ZeroDivisionError):
            raise ValueError("canonical exact rational required, never float or bool") from None
        if str(x) == value:
            return x
    raise ValueError("canonical exact rational required, never float or bool")


def prefix_geometry(problem, target, policy, compiled, bottom, coefficients, domains=None):
    A = scalar_labels(problem); d = 2*problem.width
    if policy["labels"] != A or policy["Q"] != problem.moduli[0] or compiled["fingerprint"] != policy["frozen_geometry_sha256"]:
        raise ValueError("prefix belongs to different original source")
    if type(bottom) is not int or not 0 <= bottom <= d or len(coefficients) != d or any(type(x) is not int for x in coefficients):
        raise ValueError("canonical complete integer coefficient array and prefix boundary required")
    if any(coefficients[:bottom]):
        raise ValueError("unassigned coefficients must be canonically zero")
    target = problem.target(target)
    data = coset_target(problem, target, policy["geometry"])
    if data is None:
        raise ValueError("empty integer coset has no fractional-prefix experiment")
    z0, T = data; basis = compiled["basis"]; K = basis["kernel_rows"]
    # Recenter the real LP at an exact Babai completion. Without this shift,
    # enormous integer coset offsets can hide O(1) triangle faces in floats.
    coordinates = list(_target_coordinates(basis, T)); anchor = list(coefficients)
    for i in range(d-1,-1,-1):
        if i < bottom:
            x = coordinates[i]; anchor[i] = int((2*x.p+x.q)//(2*x.q))
        for j in range(i): coordinates[j] -= anchor[i]*basis["mu_q"][i][j]
    z_anchor = tuple(a+sum(c*row[j] for c,row in zip(anchor,K)) for j,a in enumerate(z0))
    H = tuple(x-sum(coefficients[i]*basis["rows"][i][j] for i in range(bottom,d)) for j,x in enumerate(T))
    if domains is None:
        domains = ((0,1,2),)*problem.width
    domains = tuple(tuple(D) for D in domains)
    if len(domains) != problem.width or any(not D or D != tuple(sorted(set(D))) or any(type(x) is not int or x not in (0,1,2) for x in D) for D in domains):
        raise ValueError("nonempty canonical allowed native digits required")
    Q = problem.moduli[0]
    wind = tuple(sum(a*x for a,x in zip(A,row))//Q for row in K[:bottom])
    if any(sum(a*x for a,x in zip(A,row)) % Q for row in K):
        raise ArithmeticError("unassigned rows left original integer kernel")
    anchor_sum = sum(a*x for a,x in zip(A,z_anchor))-target[0]
    if anchor_sum % Q:
        raise ArithmeticError("integer Babai anchor left original target coset")
    winding_anchor = anchor_sum//Q
    upper = (sum(max(pair[0][0],pair[1][0]) for pair in problem.frequencies)-target[0])//Q
    g = math.gcd(*wind) if wind else 0
    windings = tuple(k for k in range(max(0,upper+1)) if (k == winding_anchor if g == 0 else (k-winding_anchor)%g == 0))
    return {"problem":problem,"target":target,"Q":Q,"A":A,"bottom":bottom,"basis":basis,"T":T,"H":H,
        "coefficients":tuple(coefficients),"anchor":tuple(anchor),"z_anchor":z_anchor,"kernel_prefix":K[:bottom],
        "domains":domains,"winding_coefficients":wind,"anchor_winding":winding_anchor,"winding_gcd":g,
        "allowed_integral_windings":windings,"global_winding_maximum":upper,
        "nontrivial_assigned_prefix":0 < bottom < d,"fingerprint":policy["frozen_geometry_sha256"]}


def frontier_geometry(problem, target, policy, compiled, checkpoint):
    b = checkpoint["unassigned_rows"]
    if type(b) is not int or not 0 < b < 2*problem.width:
        raise ValueError("genuine nontrivial cap frontier required")
    geom = prefix_geometry(problem,target,policy,compiled,b,tuple(checkpoint["partial_coefficients"]))
    p = project_high(compiled,geom["H"],b); spent = sum((x*x for x in p),fmpq(0))
    if spent != rational(checkpoint["assigned_squared_energy"]):
        raise ValueError("saved frontier energy disagrees with actual assigned span")
    domains,_ = native_domains(p,fmpq(6*problem.width)-spent,compiled["prefix_block_projectors"][b])
    geom["domains"] = domains
    if any(not D for D in domains):
        raise ValueError("reported unresolved parent was already native-pruned")
    geom["assigned_squared_energy"] = str(spent)
    return geom


def verify_primal(geometry, offsets, required_winding=None):
    b = geometry["bottom"]
    if len(offsets) != b or (required_winding is not None and type(required_winding) is not int):
        raise ValueError("complete exact prefix offsets and optional integer winding required")
    y = tuple(rational(x) for x in offsets)
    z = tuple(fmpq(a)+sum((c*row[j] for c,row in zip(y,geometry["kernel_prefix"])),fmpq(0))
              for j,a in enumerate(geometry["z_anchor"]))
    issues = []
    for j,domain in enumerate(geometry["domains"]):
        u,v = z[2*j:2*j+2]; probabilities = (1-u-v,u,v)
        if any(x < 0 for x in probabilities):
            issues.append(f"block{j}: outside exact native triangle")
        if any(probabilities[digit] != 0 for digit in range(3) if digit not in domain):
            issues.append(f"block{j}: uses a digit excluded by prefix energy")
    winding = (sum((a*x for a,x in zip(geometry["A"],z)),fmpq(0))-geometry["target"][0])/geometry["Q"]
    if required_winding is not None and winding != required_winding:
        issues.append("does not satisfy the declared exact integral winding")
    alphabet={(fmpq(0),fmpq(0)):0,(fmpq(1),fmpq(0)):1,(fmpq(0),fmpq(1)):2}
    digits=tuple(alphabet.get(tuple(z[j:j+2])) for j in range(0,len(z),2))
    vertex=all(x is not None for x in digits)
    native_word=digits if vertex and geometry["problem"].value(digits)==geometry["target"] else None
    if native_word is not None and any((geometry["anchor"][i]+y[i]).q != 1 for i in range(b)):
        raise ArithmeticError("true native completion lacks integral full-kernel coefficients")
    return {"valid":not issues,"issues":issues,"rational_offsets":[str(x) for x in y],"original_fractional_coordinates":[str(x) for x in z],
        "winding":str(winding),"integral_winding":winding.q==1,"required_winding":required_winding,
        "native_simplex_vertex":vertex,"actual_native_word":native_word,
        "vertex_has_wrong_original_target":vertex and native_word is None,
        "nontrivial_assigned_prefix":geometry["nontrivial_assigned_prefix"],
        "membership_is_not_pair_or_coverage_proof":True}


def linear_constraints(geometry, required_winding=None):
    K = geometry["kernel_prefix"]; b = geometry["bottom"]; z = geometry["z_anchor"]
    inequalities, bounds, equalities, rhs = [], [], [], []
    for j,D in enumerate(geometry["domains"]):
        u = tuple(row[2*j] for row in K); v = tuple(row[2*j+1] for row in K)
        inequalities.extend((tuple(-x for x in u),tuple(-x for x in v),tuple(a+c for a,c in zip(u,v))))
        bounds.extend((z[2*j],z[2*j+1],1-z[2*j]-z[2*j+1]))
        if 0 not in D:
            equalities.append(tuple(a+c for a,c in zip(u,v))); rhs.append(1-z[2*j]-z[2*j+1])
        if 1 not in D: equalities.append(u); rhs.append(-z[2*j])
        if 2 not in D: equalities.append(v); rhs.append(-z[2*j+1])
    if required_winding is not None:
        if type(required_winding) is not int: raise ValueError("integer winding required")
        equalities.append(geometry["winding_coefficients"]); rhs.append(required_winding-geometry["anchor_winding"])
    assert all(len(row)==b for row in (*inequalities,*equalities))
    return tuple(inequalities),tuple(bounds),tuple(equalities),tuple(rhs)


def exact_affine_proposal(augmented, proposal):
    """Exact face reconstruction; free values are guesses, never proof authority."""
    b=len(proposal)
    if not augmented: return None
    reduced,rank=fmpq_mat(augmented).rref()
    if any(all(reduced[i,j]==0 for j in range(b)) and reduced[i,b]!=0 for i in range(reduced.nrows())):
        return None
    pivots={next(j for j in range(b) if reduced[i,j]) for i in range(rank)}
    free=[j for j in range(b) if j not in pivots]
    for limit in ((1<<20),(1<<32)) if free else (1,):
        extra=[]
        for j in free:
            q=Fraction(float(proposal[j])).limit_denominator(limit)
            row=[0]*b; row[j]=1; extra.append([*row,rational(q)])
        complete,full_rank=fmpq_mat([*augmented,*extra]).rref()
        if full_rank!=b: continue
        answer=tuple(complete[i,b] for i in range(b))
        if all(sum((rational(a)*x for a,x in zip(row[:b],answer)),fmpq(0))==rational(row[b]) for row in augmented):
            yield answer,{"active_rank":rank,"free_coordinate_proposals":free,"free_denominator_limit":limit if free else None}


def recover_active_primal(geometry, proposal, required_winding=None):
    """Recover an exact rational face point; it need not be a vertex."""
    b = geometry["bottom"]
    x = np.asarray(proposal,dtype=float)
    if x.shape != (b,) or not np.isfinite(x).all():
        raise ValueError("finite correctly sized numerical proposal required")
    if b == 0:
        certificate=verify_primal(geometry,(),required_winding)
        return {"status":"EXACT_PRIMAL_CERTIFICATE" if certificate["valid"] else "NO_EXACT_PRIMAL_CERTIFICATE","certificate":certificate}
    inequalities,bounds,equalities,rhs=linear_constraints(geometry,required_winding)
    scales=[max(1,*(abs(a) for a in row)) for row in inequalities]
    slacks=[float(Fraction(B,s))-sum(float(Fraction(a,s))*v for a,v in zip(row,x)) for row,B,s in zip(inequalities,bounds,scales)]
    last="ACTIVE_SET_UNDERRANKED"
    for tolerance in (1e-7,1e-5):
        selected=[i for i,s in enumerate(slacks) if abs(s)<=tolerance]
        augmented=[[*row,B] for row,B in zip(equalities,rhs)]+[[*inequalities[i],bounds[i]] for i in selected]
        if not augmented: continue
        for offsets,metadata in exact_affine_proposal(augmented,x):
            certificate=verify_primal(geometry,offsets,required_winding)
            if certificate["valid"]:
                return {"status":"EXACT_PRIMAL_CERTIFICATE","certificate":certificate,**metadata,
                    "active_triangle_rows":selected,"numerical_tolerance_used_only_for_proposal":tolerance}
            last="RECOVERED_POINT_FAILS_EXACT_CONSTRAINTS"
    return {"status":last,"certificate":None,"failure_is_not_infeasibility_proof":True}


def propose_primal(geometry, required_winding=None):
    b=geometry["bottom"]
    if b==0: return recover_active_primal(geometry,(),required_winding)
    inequalities,bounds,equalities,rhs=linear_constraints(geometry,required_winding)
    def scaled(rows,values):
        scales=[max(1,*(abs(x) for x in row)) for row in rows]
        return np.array([[float(Fraction(x,s)) for x in row] for row,s in zip(rows,scales)]),np.array([float(Fraction(x,s)) for x,s in zip(values,scales)])
    A,B=scaled(inequalities,bounds)
    E,F=scaled(equalities,rhs) if equalities else (None,None)
    start=time.perf_counter()
    result=linprog(np.zeros(b),A_ub=A,b_ub=B,A_eq=E,b_eq=F,bounds=(None,None),method="highs-ds",options={"time_limit":5.0,"maxiter":10000})
    cost={"numerical_LP_calls":1,"LP_seconds":time.perf_counter()-start,"LP_iterations":int(result.nit or 0)}
    if not result.success:
        return {"status":"NUMERICAL_LP_NO_PRIMAL_CERTIFICATE","numerical_status":int(result.status),"certificate":None,
                "failure_is_not_infeasibility_proof":True,"cost":cost}
    recovered=recover_active_primal(geometry,result.x,required_winding)
    recovered["cost"]=cost
    return recovered


def farkas_rows(geometry,required_winding=None):
    A,B,E,F=linear_constraints(geometry,required_winding)
    rows=list(A); rhs=list(B)
    for row,x in zip(E,F):
        rows.extend((row,tuple(-a for a in row))); rhs.extend((x,-x))
    return tuple(rows),tuple(rhs)


def verify_farkas(geometry,weights,required_winding=None):
    A,B=farkas_rows(geometry,required_winding)
    if len(weights)!=len(A): raise ValueError("complete Farkas multiplier array required")
    y=tuple(rational(x) for x in weights); b=geometry["bottom"]
    issues=[]
    if any(x<0 for x in y): issues.append("negative multiplier is not a valid inequality combination")
    if any(sum((x*row[j] for x,row in zip(y,A)),fmpq(0)) for j in range(b)):
        issues.append("multipliers do not annihilate every unassigned LP column")
    rhs=sum((x*B_i for x,B_i in zip(y,B)),fmpq(0))
    if rhs>=0: issues.append("combined right hand side is not strictly negative")
    return {"valid":not issues,"issues":issues,"nonnegative_inequality_multipliers":[str(x) for x in y],
            "exact_combined_rhs":str(rhs),"required_winding":required_winding,
            "proves_no_fractional_prefix_in_declared_relaxation":not issues}


def propose_farkas(geometry,required_winding=None):
    """Numerically propose y>=0, y*A=0, y*B=-1; re-solve/check exactly."""
    A,B=farkas_rows(geometry,required_winding); b=geometry["bottom"]; m=len(A)
    constraints=[tuple(row[j] for row in A) for j in range(b)]+[B]
    rhs=(0,)*b+(-1,)
    scales=[max(1,*(abs(a) for a in row)) for row in constraints]
    matrix=np.array([[float(Fraction(a,s)) for a in row] for row,s in zip(constraints,scales)])
    values=np.array([float(Fraction(a,s)) for a,s in zip(rhs,scales)])
    start=time.perf_counter()
    result=linprog(np.zeros(m),A_eq=matrix,b_eq=values,bounds=(0,None),method="highs-ds",options={"time_limit":5.0,"maxiter":10000})
    cost={"numerical_dual_LP_calls":1,"dual_LP_seconds":time.perf_counter()-start,"dual_LP_iterations":int(result.nit or 0)}
    if not result.success:
        return {"status":"NO_EXACT_FARKAS_CERTIFICATE","certificate":None,"numerical_status":int(result.status),"cost":cost,
                "failure_is_not_feasibility_proof":True}
    if np.asarray(result.x).shape!=(m,) or not np.isfinite(result.x).all(): raise ValueError("invalid numerical dual proposal")
    # A basic nonnegative solution has small support. Discarding tiny proposed
    # multipliers is safe only because the recovered full combination is checked.
    for tolerance in (1e-8,1e-12,0):
        support=[i for i,x in enumerate(result.x) if x>tolerance]
        if not support: continue
        augmented=[[*(row[i] for i in support),x] for row,x in zip(constraints,rhs)]
        for selected,metadata in exact_affine_proposal(augmented,result.x[support]):
            weights=[fmpq(0)]*m
            for i,x in zip(support,selected): weights[i]=x
            certificate=verify_farkas(geometry,weights,required_winding)
            if certificate["valid"]:
                return {"status":"EXACT_FARKAS_PREFIX_OBSTRUCTION","certificate":certificate,"cost":cost,**metadata}
    return {"status":"NO_EXACT_FARKAS_CERTIFICATE","certificate":None,"cost":cost,"failure_is_not_feasibility_proof":True}


def prepare_reference(problem,max_half_words=200_000):
    if type(max_half_words) is not int or max_half_words<1: raise ValueError("positive reference preflight budget required")
    split=problem.width//2; bounds=(3**split,3**(problem.width-split))
    if max(bounds)>max_half_words:
        return {"status":"REFERENCE_BUDGET_NO_PARTIAL_TRUTH","raw_half_assignments":[str(x) for x in bounds],"half_assignments_enumerated":0}
    left=defaultdict(list); right=[]
    for word in product(range(3),repeat=split): left[_value(problem.frequencies[:split],problem.moduli,word)].append(word)
    for word in product(range(3),repeat=problem.width-split): right.append((_value(problem.frequencies[split:],problem.moduli,word),word))
    return {"status":"COMPLETE_EXPONENTIAL_REFERENCE_TABLES","left":left,"right":right,
            "raw_half_assignments":[str(x) for x in bounds],"half_assignments_enumerated":sum(bounds)}


def reference_prefix(geometry,reference,max_matches=100_000):
    if type(max_matches) is not int or max_matches<1: raise ValueError("positive complete-match budget required")
    if reference["status"]!="COMPLETE_EXPONENTIAL_REFERENCE_TABLES":
        return {"status":"REFERENCE_BUDGET_NO_NATIVE_TRUTH","native_prefix_words":None}
    problem=geometry["problem"]; Q=geometry["Q"]; t=geometry["target"]; b=geometry["bottom"]
    fibers=[]
    for value,word in reference["right"]:
        key=tuple((a-c)%q for a,c,q in zip(t,value,problem.moduli))
        for prefix in reference["left"].get(key,()):
            if len(fibers)>=max_matches:
                return {"status":"REFERENCE_MATCH_CAP_NO_COMPLETE_TRUTH","native_prefix_words":None}
            fibers.append(prefix+word)
    # Solve prefix span membership exactly. The complete integer kernel means
    # a true original-target native word must also have INTEGER prefix offsets.
    answers=[]
    for word in fibers:
        desired=word_coordinates(word); delta=tuple(a-c for a,c in zip(desired,geometry["z_anchor"]))
        if b:
            augmented=fmpq_mat([[*(row[j] for row in geometry["kernel_prefix"]),delta[j]] for j in range(2*problem.width)])
            reduced,rank=augmented.rref()
            if rank != b: continue
            offsets=tuple(reduced[i,b] for i in range(b))
            if any(x.q!=1 for x in offsets): raise ArithmeticError("complete native kernel coefficient integrality failed")
        else:
            if any(delta): continue
            offsets=()
        if verify_primal(geometry,offsets)["valid"]: answers.append(word)
    return {"status":"COMPLETE_NATIVE_PREFIX_TRUTH","whole_target_fiber_size":len(fibers),
            "whole_target_fiber":fibers,"native_prefix_words":answers,"right_hash_lookups":len(reference["right"]),
            "reference_is_exponential_not_given_to_LP":True}


def _saved_geometry(g):
    return {"unassigned_rows":g["bottom"],"partial_coefficients":[str(x) for x in g["coefficients"]],
        "anchor_coefficients":[str(x) for x in g["anchor"]],"anchor_native_coordinates":[str(x) for x in g["z_anchor"]],
        "allowed_digits":g["domains"],"assigned_squared_energy":g.get("assigned_squared_energy"),
        "winding_coefficients":[str(x) for x in g["winding_coefficients"]],"anchor_winding":str(g["anchor_winding"]),
        "winding_gcd":str(g["winding_gcd"]),"allowed_integral_windings":list(g["allowed_integral_windings"])}


def build_report():
    source=json.loads(FIXTURE.read_text()); catalog=json.loads((ROOT/"research/phase_workbench/ternary_repair_catalog.json").read_text()); cases=[]
    for index in range(6,15):
        old=source["planted_geometry_probes"][index]; Q=int(old["modulus"]); A=tuple(map(int,old["labels"]))
        problem=LowProblem((Q,),tuple(((a,),(c,)) for a,c in zip(A[::2],A[1::2])),0)
        policy=frozen_policy(problem,old["prepared"]); compiled=compile_adaptive(policy); reference=prepare_reference(problem)
        trials=[]
        for t in catalog["cases"][index]["uniform_target_trials"]:
            target=(int(t["target"]),); search=adaptive_pair(problem,target,policy,compiled,256,"projector")
            checkpoint=search["cap_frontier"]
            if checkpoint is None or checkpoint["unassigned_rows"]==2*problem.width:
                trials.append({"target":str(target[0]),"status":"NO_NONTRIVIAL_CAP_FRONTIER","decoder_status":search["status"],"decoder_cost":search["cost"]}); continue
            g=frontier_geometry(problem,target,policy,compiled,checkpoint)
            primal=propose_primal(g); dual=None; winding_runs=[]
            if not (primal["certificate"] and primal["certificate"]["valid"]): dual=propose_farkas(g)
            # Complete allowed winding schedule, never just a favorable lift.
            for k in g["allowed_integral_windings"]:
                result=propose_primal(g,k)
                if not (result["certificate"] and result["certificate"]["valid"]): result["farkas"]=propose_farkas(g,k)
                winding_runs.append({"winding_branch":k,**result})
            truth=reference_prefix(g,reference)
            no_native=truth["native_prefix_words"]==[]
            has_primal=bool(primal["certificate"] and primal["certificate"]["valid"])
            survives_winding=any(r["certificate"] and r["certificate"]["valid"] for r in winding_runs)
            linear_empty=bool(dual and dual["certificate"] and dual["certificate"]["valid"])
            all_windings_empty=all(r.get("farkas",{}).get("certificate") and r["farkas"]["certificate"]["valid"] for r in winding_runs)
            if (linear_empty or all_windings_empty) and truth["native_prefix_words"]:
                raise ArithmeticError("exact linear obstruction contradicts a genuine native completion")
            trials.append({"target":str(target[0]),"status":"EXACT_WINDING_PREFIX_INTEGRALITY_GAP" if no_native and survives_winding
                else "EXACT_PREFIX_INTEGRALITY_GAP" if no_native and has_primal else "EXACT_LINEAR_PREFIX_OBSTRUCTION" if linear_empty
                else "EXACT_ALL_WINDINGS_PREFIX_OBSTRUCTION" if all_windings_empty else "CERTIFIED_RELAXATION_NATIVE_TRUTH_UNKNOWN" if has_primal and truth["native_prefix_words"] is None else "PREFIX_ANALYSIS_NOT_A_POPULATION_THEOREM",
                "decoder_status":search["status"],"decoder_cost":search["cost"],"frontier":_saved_geometry(g),
                "prefix_primal":primal,"prefix_farkas":dual,"all_allowed_windings_exactly_obstructed":bool(all_windings_empty),
                "prefix_relaxation_exactly_obstructed":linear_empty,"integral_winding_trials":winding_runs,"native_truth":truth})
        cases.append({"fixture_probe_index":index,"root_digits":old["root_digits"],"Q":str(Q),"labels":[str(x) for x in A],
            "fingerprint":policy["frozen_geometry_sha256"],"node_budget":256,"shared_uniform_targets_conditional_not_new_population_trials":True,
            "reference_cost":{k:v for k,v in reference.items() if k not in ("left","right")},"trials":trials})
    return {"status":"EXACT_PREFIX_RELAXATION_CERTIFICATES_NOT_SOLVER_OR_POPULATION_NO_GO","local_derivations_review_pending":True,
        "novelty_claim":False,"polynomial_pair_finder_proved":False,"population_obstruction_proved":False,
        "numerical_LP_status_never_accepted_as_proof":True,"forbidden_native_digits_retained":True,
        "original_modular_winding_and_prefix_winding_gcd_checked":True,"reference_not_available_to_proposer":True,
        "winding_branch_schedule_complete":True,"cases":cases}


def build_decoder_report():
    source=json.loads(FIXTURE.read_text())
    baseline=json.loads((ROOT/"research/phase_workbench/ternary_adaptive_shell.json").read_text()); cases=[]
    for old_case in baseline["cases"]:
        index=old_case["fixture_probe_index"]
        if old_case["root_digits"]<16: continue
        old=source["planted_geometry_probes"][index]; Q=int(old["modulus"]); A=tuple(map(int,old["labels"]))
        problem=LowProblem((Q,),tuple(((a,),(c,)) for a,c in zip(A[::2],A[1::2])),0)
        policy=frozen_policy(problem,old["prepared"]); compiled=compile_adaptive(policy); trials=[]
        for old_trial in old_case["trials"]:
            if old_trial["cut"]!="projector" or old_trial["node_budget"]!=2048: continue
            t=(int(old_trial["target"]),); answer=adaptive_pair(problem,t,policy,compiled,2048,"linear",max_linear_calls=16)
            trials.append({"target":str(t[0]),"node_budget":2048,"linear_LP_cap":16,**answer,
                "matched_projector_baseline":{"status":old_trial["status"],"pair":old_trial["pair"],"cost":old_trial["cost"]}})
        cases.append({"fixture_probe_index":index,"root_digits":old["root_digits"],"Q":str(Q),"labels":[str(x) for x in A],
            "fingerprint":policy["frozen_geometry_sha256"],"shared_conditional_targets_not_fresh_population":True,"trials":trials})
    return {"status":"EXACT_LINEAR_PREFIX_PRUNING_BASELINE_NOT_POLYNOMIAL_SOLVER","local_derivations_review_pending":True,
        "novelty_claim":False,"polynomial_pair_finder_proved":False,"population_coverage_proved":False,
        "LP_flags_never_prune_without_exact_Farkas_certificate":True,"search_window":"0<unassigned<=3*d/4; boundary divisible by4",
        "original_LLL_not_in_decode_wall_seconds":True,"cases":cases}


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument("--write",action="store_true"); parser.add_argument("--decoder",action="store_true")
    args=parser.parse_args(); report=build_decoder_report() if args.decoder else build_report()
    if args.write:
        destination=ROOT/"research/phase_workbench/ternary_prefix_lp_decoder.json" if args.decoder else REPORT
        destination.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"status":report["status"],"roots":[{"root_digits":r,"statuses":dict(Counter(t["status"] for c in report["cases"] if c["root_digits"]==r for t in c["trials"])),
        "pairs":sum(bool(t.get("pair")) for c in report["cases"] if c["root_digits"]==r for t in c["trials"])} for r in (16,24,32)]},indent=2))
