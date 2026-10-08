"""Exact dual certificates for coupled native prefix infeasibility.

LOCAL DERIVATIONS / REVIEW PENDING. Bounded Frank-Wolfe is certificate search,
not an exact LP solver, quantum algorithm or polynomial source-coverage proof.
"""
from __future__ import annotations

import math
import argparse
import json
from pathlib import Path

from flint import fmpq


def project_high(compiled, vector, bottom):
    d = len(compiled["gs"])
    if type(bottom) is not int or not 0 <= bottom <= d or len(vector) != len(compiled["gs"][0]):
        raise ValueError("compatible vector and assigned-span boundary required")
    result = [fmpq(0)]*len(vector)
    for row, norm in zip(compiled["gs"][bottom:], compiled["basis"]["gs_q"][bottom:]):
        c = sum((a*b for a, b in zip(vector, row)), fmpq(0))/norm
        if c:
            result = [a+c*b for a, b in zip(result, row)]
    return tuple(result)


def support_vertex(vector):
    if not vector or len(vector) % 3 or any(sum(vector[j:j+3]) for j in range(0, len(vector), 3)):
        raise ValueError("native A2 block-plane dual vector required")
    result, support = [], fmpq(0)
    for j in range(0, len(vector), 3):
        digit = max(range(3), key=lambda i: vector[j+i])
        result.extend(2 if i == digit else -1 for i in range(3))
        support += 3*vector[j+digit]
    return tuple(result), support


def integer_separator(vector):
    denominator = math.lcm(*(int(x.q) for x in vector))
    v = tuple(int(x.p)*(denominator//int(x.q)) for x in vector)
    g = math.gcd(*v)
    return tuple(x//g for x in v) if g else v


def verify_integer_separator(rows, target, coefficients, bottom, direction):
    """Standalone integer certificate; neither saved GS nor numerical LP trusted."""
    d = len(rows); ambient = len(target)
    if type(bottom) is not int or not 0 <= bottom <= d or len(coefficients) != d or len(direction) != ambient or ambient % 3:
        raise ValueError("full integer partial-branch certificate required")
    if any(len(row) != ambient for row in rows) or any(type(x) is not int for row in rows for x in row):
        raise ValueError("canonical integer basis rows required")
    if any(type(x) is not int for x in (*target, *coefficients, *direction)):
        raise ValueError("canonical integer certificate entries required")
    if any(sum(direction[j:j+3]) for j in range(0, ambient, 3)):
        raise ValueError("dual direction outside original native planes")
    if any(sum(a*b for a, b in zip(direction, row)) for row in rows[:bottom]):
        raise ValueError("dual direction not orthogonal to all unassigned rows")
    residual = tuple(target[k]-sum(coefficients[i]*rows[i][k] for i in range(bottom, d)) for k in range(ambient))
    lhs = sum(a*b for a, b in zip(residual, direction))
    rhs = 3*sum(max(direction[j:j+3]) for j in range(0, ambient, 3))
    return {"valid": lhs > rhs, "exact_branch_inner": str(lhs), "exact_native_support": str(rhs),
            "strict_margin": str(lhs-rhs)}


def search_separator(compiled, projected, bottom, iterations=4, step_bits=8):
    if type(iterations) is not int or iterations < 1 or type(step_bits) is not int or not 1 <= step_bits <= 16:
        raise ValueError("positive iterations and bounded dyadic step precision required")
    projected = tuple(fmpq(x) for x in projected)
    if project_high(compiled, projected, bottom) != projected:
        raise ValueError("partial projection is outside declared assigned GS span")
    cost = {"iterations": 0, "support_calls": 0, "gs_projector_applications": 1, "dyadic_step_bits": step_bits}
    vertex, _ = support_vertex(projected); cost["support_calls"] += 1
    current = project_high(compiled, vertex, bottom); cost["gs_projector_applications"] += 1
    scale = 1 << step_bits
    for _ in range(iterations):
        h = tuple(a-b for a, b in zip(projected, current))
        vertex, support = support_vertex(h); cost["support_calls"] += 1
        lhs = sum((a*b for a, b in zip(projected, h)), fmpq(0))
        if lhs > support:
            return {"status": "STRICT_NATIVE_PREFIX_SEPARATOR", "direction": integer_separator(h), "cost": cost}
        if not any(h):
            return {"status": "IN_PROJECTED_CONVEX_HULL_NOT_A_NATIVE_WORD", "direction": (), "cost": cost}
        next_vertex = project_high(compiled, vertex, bottom); cost["gs_projector_applications"] += 1
        delta = tuple(a-b for a, b in zip(next_vertex, current))
        norm = sum((x*x for x in delta), fmpq(0))
        gain = sum((a*b for a, b in zip(h, delta)), fmpq(0))
        if norm == 0 or gain <= 0:
            return {"status": "NO_CERTIFICATE_FROM_THIS_ITERATE", "direction": (), "cost": cost}
        eta = min(fmpq(1), gain/norm)
        numerator = int((eta.p*scale)//eta.q)
        if not numerator:
            return {"status": "NO_CERTIFICATE_AT_STEP_PRECISION", "direction": (), "cost": cost}
        eta = fmpq(numerator, scale)
        current = tuple(a+eta*b for a, b in zip(current, delta))
        cost["iterations"] += 1
    return {"status": "SEPARATION_BUDGET_INCONCLUSIVE", "direction": (), "cost": cost}


def build_report():
    from ternary_pair_collimation import LowProblem
    from ternary_repair_catalog import frozen_policy, FIXTURE
    from ternary_adaptive_shell import adaptive_pair, compile_adaptive
    root = Path(__file__).resolve().parents[1]
    source = json.loads(FIXTURE.read_text())
    baseline = json.loads((root/"research/phase_workbench/ternary_adaptive_shell.json").read_text())
    cases = []
    for index in (6,9,12):
        old = source["planted_geometry_probes"][index]
        Q = int(old["modulus"]); A = tuple(map(int,old["labels"]))
        problem = LowProblem((Q,),tuple(((a,),(b,)) for a,b in zip(A[::2],A[1::2])),0)
        policy = frozen_policy(problem,old["prepared"]); compiled = compile_adaptive(policy)
        matched = next(c for c in baseline["cases"] if c["fixture_probe_index"]==index)
        trials = []
        for old_trial in matched["trials"]:
            if old_trial["cut"] != "projector" or old_trial["node_budget"] != 2048:
                continue
            t = (int(old_trial["target"]),)
            answer = adaptive_pair(problem,t,policy,compiled,2048,"dual",max_dual_calls=8)
            trials.append({"target":str(t[0]),"node_budget":2048,"dual_search_cap":8,**answer,
                "matched_projector_baseline":{"status":old_trial["status"],"pair":old_trial["pair"],"cost":old_trial["cost"]}})
        cases.append({"fixture_probe_index":index,"root_digits":old["root_digits"],"Q":str(Q),
            "labels":[str(x) for x in A],"fingerprint":policy["frozen_geometry_sha256"],"trials":trials})
    return {"status":"EXACT_DUAL_CERTIFICATE_SEARCH_NOT_POLYNOMIAL_PAIR_SOLVER","local_derivations_review_pending":True,
        "novelty_claim":False,"polynomial_pair_finder_proved":False,"population_coverage_proved":False,
        "certificate_check_uses_only_integer_basis_target_and_partial_coefficients":True,
        "failure_to_find_separator_is_not_feasibility_proof":True,
        "convex_membership_is_not_native_word_membership":True,"fresh_population_trials":False,"cases":cases}


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument("--write",action="store_true")
    args=parser.parse_args(); report=build_report()
    if args.write:
        path=Path(__file__).resolve().parents[1]/"research/phase_workbench/ternary_native_dual_separation.json"
        path.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"status":report["status"],"cases":[{"root_digits":c["root_digits"],
        "pairs":sum(bool(t["pair"]) for t in c["trials"]),"nodes":sum(t["cost"]["coefficient_nodes"] for t in c["trials"]),
        "separators":sum(t["cost"]["dual_separator_prunes"] for t in c["trials"]),
        "wall_seconds":sum(t["cost"]["wall_seconds"] for t in c["trials"])} for c in report["cases"]]},indent=2))
