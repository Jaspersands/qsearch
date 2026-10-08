"""Target-adaptive native shell enumeration with exact simplex/projector cuts.

LOCAL DERIVATIONS / REVIEW PENDING. Standard sphere enumeration is an
exponential baseline, not an invented quantum algorithm or coverage theorem.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
import math
from pathlib import Path
import time

from flint import fmpq

from ternary_pair_collimation import LowProblem, verify_pair
from ternary_pair_lattice import coset_target, decode_shell, scalar_labels, shell_norm
from ternary_repair_catalog import FIXTURE, frozen_policy, _target_coordinates

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/ternary_adaptive_shell.json"


def _positive(x, name):
    if type(x) is not int or x < 1:
        raise ValueError(f"positive integer {name} required")
    return x


def coefficient_interval(center, squared_radius):
    """Exact inclusive integers c with (center-c)^2 <= squared_radius."""
    if not isinstance(center, fmpq) or not isinstance(squared_radius, fmpq):
        raise ValueError("exact FLINT rationals required")
    if squared_radius < 0:
        return (1, 0)
    a, b = int(center.p), int(center.q)
    radius = math.isqrt(int(squared_radius.p)*b*b//int(squared_radius.q))
    return (-((-(a-radius))//b), (a+radius)//b)


def nearest_order(center, lo, hi):
    """Lazy Schnorr-Euchner-style distance order, with no floating square root."""
    if any(type(x) is not int for x in (lo, hi)):
        raise ValueError("integer interval endpoints required")
    if lo > hi:
        return
    a, b = int(center.p), int(center.q)
    middle = min(hi, max(lo, (2*a+b)//(2*b)))
    yield middle
    left, right = middle-1, middle+1
    while left >= lo or right <= hi:
        if right > hi or (left >= lo and abs(a-b*left) <= abs(a-b*right)):
            yield left
            left -= 1
        else:
            yield right
            right += 1


def compile_adaptive(policy, basis_index=0):
    if type(basis_index) is not int or not 0 <= basis_index < len(policy["bases"]):
        raise ValueError("public recorded basis index required")
    basis = policy["bases"][basis_index]
    rows, mu = basis["rows"], basis["mu_q"]
    gs = []
    for i, row in enumerate(rows):
        gs.append(tuple(fmpq(x)-sum((mu[i][j]*gs[j][k] for j in range(i)), fmpq(0))
                        for k, x in enumerate(row)))
    norms = basis["gs_q"]
    if any(sum((x*x for x in row), fmpq(0)) != norms[i] for i, row in enumerate(gs)):
        raise ArithmeticError("exact GS reconstruction failed")
    # Restriction of the prefix projector to the first two coordinates of each
    # A2 block. Rank-zero/one cases must use range constraints, not an inverse.
    block_projectors, prefix = [], [(fmpq(0), fmpq(0), fmpq(0)) for _ in range(policy["width"])]
    for i, row in enumerate(gs):
        block_projectors.append(tuple(prefix))
        prefix = [(a+row[3*j]**2/norms[i], b+row[3*j]*row[3*j+1]/norms[i],
                   c+row[3*j+1]**2/norms[i]) for j, (a, b, c) in enumerate(prefix)]
    rho_ranges = tuple((3*sum((min(row[j:j+3]) for j in range(0, len(row), 3)), fmpq(0))/norms[i],
                        3*sum((max(row[j:j+3]) for j in range(0, len(row), 3)), fmpq(0))/norms[i])
                       for i, row in enumerate(gs))
    return {"basis": basis, "basis_index": basis_index, "gs": tuple(gs), "native_rho_ranges": rho_ranges,
            "prefix_block_projectors": tuple(block_projectors), "fingerprint": policy["frozen_geometry_sha256"],
            "gs_vector_cells": len(rows)*len(rows[0]), "projector_rank_one_updates": len(rows)*policy["width"]}


def block_minimum_energy(gram, r0, r1):
    """Minimum prefix-vector norm subject to two block coordinates; None if impossible."""
    if any(not isinstance(x, fmpq) for x in (*gram, r0, r1)):
        raise ValueError("exact FLINT rational projector entries and residuals required")
    a, b, c = gram
    det = a*c-b*b
    if a < 0 or c < 0 or det < 0:
        raise ValueError("positive semidefinite projector restriction required")
    if det:
        return (c*r0*r0-2*b*r0*r1+a*r1*r1)/det
    if a:
        return r0*r0/a if a*r1 == b*r0 else None
    if c:
        return r1*r1/c if r0 == 0 else None
    return fmpq(0) if r0 == 0 and r1 == 0 else None


def native_domains(projected, remaining, projectors=None):
    """Allowed digits, stopping after the first impossible block if any."""
    checks, domains = 0, []
    for j in range(len(projected)//3):
        block = projected[3*j:3*j+3]
        possible = []
        for digit in range(3):
            if projectors is not None:
                checks += 1
                energy = block_minimum_energy(projectors[j], fmpq(2 if digit == 0 else -1)-block[0],
                                               fmpq(2 if digit == 1 else -1)-block[1])
                if energy is None or energy > remaining:
                    continue
            possible.append(digit)
        domains.append(tuple(possible))
        if not possible:
            return tuple(domains), checks
    return tuple(domains), checks


def native_cut(projected, spent, remaining, projectors=None):
    """Necessary shell feasibility only; never treat passing as a witness."""
    domains, checks = native_domains(projected, remaining, projectors)
    minimum, maximum = fmpq(0), fmpq(0)
    for j, domain in enumerate(domains):
        if not domain:
            return False, checks
        possible = [3*projected[3*j+digit] for digit in domain]
        minimum += min(possible); maximum += max(possible)
    # Any true e has <e, projected> = ||projected||^2. The support interval
    # over feasible block digits must contain that value. Block energy bounds
    # cannot be summed: prefix constraints couple different blocks.
    return minimum <= spent <= maximum, checks


def adaptive_pair(problem, target, policy, compiled, max_nodes=2048, cut="projector", stop_after_pair=True, max_dual_calls=16, max_linear_calls=16):
    _positive(max_nodes, "node budget")
    _positive(max_dual_calls, "dual search budget")
    _positive(max_linear_calls, "linear certificate search budget")
    if cut not in ("sphere", "simplex", "projector", "dual", "linear") or type(stop_after_pair) is not bool:
        raise ValueError("declared cut and Boolean pair stopping policy required")
    if policy["labels"] != scalar_labels(problem) or policy["Q"] != problem.moduli[0] or compiled["fingerprint"] != policy["frozen_geometry_sha256"]:
        raise ValueError("compiled policy belongs to different source labels")
    target = problem.target(target)
    cost = {"coefficient_nodes": 0, "intervals_built": 0, "mu_updates": 0, "projection_cells_updated": 0,
            "projector_digit_checks": 0, "native_cut_prunes": 0, "native_interval_prunes": 0, "leaf_points": 0,
            "dual_search_calls": 0, "dual_support_calls": 0, "dual_projector_applications": 0,
            "dual_iteration_steps": 0, "dual_separator_prunes": 0,
            "linear_LP_calls": 0, "linear_obstruction_prunes": 0, "linear_anchor_roundings": 0,
            "linear_verifier_column_terms": 0,
            "nodes_by_row": [0]*(2*problem.width), "original_lll_preparations_per_fresh_labels": len(policy["bases"]),
            "training_words": 0, "gs_vector_cells_per_fresh_labels": compiled["gs_vector_cells"],
            "projector_updates_per_fresh_labels": compiled["projector_rank_one_updates"],
            "max_exact_rational_bits": 0, "target_adaptive": True, "wall_seconds": 0.0}
    data = coset_target(problem, target, policy["geometry"])
    if data is None:
        return {"status": "DIVISIBILITY_CERTIFIED_EMPTY", "complete_fiber": True, "pair": (), "witnesses": (), "traces": [], "cost": cost, "cap_frontier": None}
    z0, T = data
    basis = compiled["basis"]; d = len(basis["rows"])
    center = _target_coordinates(basis, T)
    radius = fmpq(6*problem.width)
    coeff, repairs, found, traces, separators, linear_certificates = [0]*d, [0]*d, [], [], [], []
    capped = False; stopped_on_pair = False; frontier = None; start = time.perf_counter()

    def visit(i, coordinates, spent, projected):
        nonlocal capped, stopped_on_pair, frontier
        cost["intervals_built"] += 1
        norm, x = basis["gs_q"][i], coordinates[i]
        lo, hi = coefficient_interval(x, (radius-spent)/norm)
        if cut != "sphere":
            lower_rho, upper_rho = compiled["native_rho_ranges"][i]
            left, right = x-upper_rho, x-lower_rho
            lo, hi = max(lo, -int((-left.p)//left.q)), min(hi, int(right.p//right.q))
            if lo > hi:
                cost["native_interval_prunes"] += 1
        for c in nearest_order(x, lo, hi):
            if cost["coefficient_nodes"] >= max_nodes:
                capped = True
                frontier = {"unassigned_rows": i+1, "partial_coefficients": tuple(0 if j <= i else coeff[j] for j in range(d)),
                            "next_row": i, "next_coefficient": c, "assigned_squared_energy": str(spent)}
                return
            cost["coefficient_nodes"] += 1; cost["nodes_by_row"][i] += 1
            coeff[i] = c
            repairs[i] = c-int((2*x.p+x.q)//(2*x.q))
            rho = x-c; new_spent = spent+rho*rho*norm
            if new_spent > radius:
                raise ArithmeticError("inclusive exact sphere interval failed")
            cost["max_exact_rational_bits"] = max(cost["max_exact_rational_bits"], int(new_spent.p).bit_length(), int(new_spent.q).bit_length())
            if cut != "sphere":
                new_projected = tuple(a+rho*b for a, b in zip(projected, compiled["gs"][i]))
                cost["projection_cells_updated"] += len(new_projected)
                permitted, checks = native_cut(new_projected, new_spent, radius-new_spent,
                    compiled["prefix_block_projectors"][i] if cut in ("projector", "dual", "linear") else None)
                cost["projector_digit_checks"] += checks
                if not permitted:
                    cost["native_cut_prunes"] += 1
                    continue
                if cut == "linear" and 0 < i <= 3*d//4 and i % 4 == 0 and cost["linear_LP_calls"] < max_linear_calls:
                    from ternary_prefix_integrality import frontier_geometry, propose_farkas, _saved_geometry
                    checkpoint={"unassigned_rows":i,"partial_coefficients":tuple(0 if j<i else coeff[j] for j in range(d)),
                                "assigned_squared_energy":str(new_spent)}
                    geometry=frontier_geometry(problem,target,policy,compiled,checkpoint)
                    obstruction=propose_farkas(geometry)
                    cost["linear_LP_calls"] += 1; cost["linear_anchor_roundings"] += d
                    if obstruction["certificate"] and obstruction["certificate"]["valid"]:
                        certificate=obstruction["certificate"]
                        cost["linear_obstruction_prunes"] += 1
                        cost["linear_verifier_column_terms"] += i*len(certificate["nonnegative_inequality_multipliers"])
                        linear_certificates.append({"frontier":_saved_geometry(geometry),"certificate":certificate})
                        continue
                if cut == "dual" and i % 8 == 0 and cost["dual_search_calls"] < max_dual_calls:
                    from ternary_native_dual_separation import search_separator, verify_integer_separator
                    search = search_separator(compiled, new_projected, i)
                    cost["dual_search_calls"] += 1
                    cost["dual_support_calls"] += search["cost"]["support_calls"]
                    cost["dual_projector_applications"] += search["cost"]["gs_projector_applications"]
                    cost["dual_iteration_steps"] += search["cost"]["iterations"]
                    if search["direction"]:
                        certificate = verify_integer_separator(basis["rows"], T, tuple(coeff), i, search["direction"])
                        if not certificate["valid"]:
                            raise ArithmeticError("search proposed an invalid exact dual separator")
                        cost["dual_separator_prunes"] += 1
                        separators.append({"unassigned_row_count": i, "partial_coefficients": tuple(coeff),
                            "integer_direction": [str(x) for x in search["direction"]], **certificate})
                        continue
            else:
                new_projected = projected
            if i:
                updated = tuple(coordinates[j]-c*basis["mu_q"][i][j] for j in range(i))
                cost["mu_updates"] += i
                visit(i-1, updated, new_spent, new_projected)
            else:
                cost["leaf_points"] += 1
                z = tuple(a+sum(c*r[j] for c, r in zip(coeff, basis["kernel_rows"])) for j, a in enumerate(z0))
                word = decode_shell(z)
                if word is None or new_spent != radius or problem.value(word) != target:
                    raise ArithmeticError("enumerated native shell disagrees with original fiber")
                if word in found:
                    raise ArithmeticError("full-rank single-basis enumeration repeated a word")
                found.append(word); traces.append({"word": word, "reduced_basis_coefficients": tuple(coeff),
                    "integer_coset_coordinates": z, "exact_original_norm": str(shell_norm(z)),
                    "required_target_adaptive_repairs": tuple(repairs)})
                if len(found) >= 2 and stop_after_pair:
                    stopped_on_pair = True
            if capped or stopped_on_pair:
                return

    visit(d-1, center, fmpq(0), (fmpq(0),)*(3*problem.width))
    cost["wall_seconds"] = time.perf_counter()-start
    if stopped_on_pair:
        status = "VERIFIED_ADAPTIVE_PAIR_NO_COVERAGE_THEOREM"
    elif capped:
        status = "NODE_CAP_PARTIAL_FIBER" if found else "NODE_CAP_NO_WITNESS"
    else:
        status = "COMPLETE_EMPTY_FIBER" if not found else "COMPLETE_SINGLETON_FIBER" if len(found) == 1 else "COMPLETE_FIBER"
    return {"status": status, "complete_fiber": not capped and not stopped_on_pair,
            "pair": verify_pair(problem, target, found[:2]) if len(found) >= 2 else (),
            "witnesses": tuple(found), "traces": traces, "cost": cost, "dual_certificates": separators,
            "linear_certificates":linear_certificates, "cap_frontier": frontier}


def build_report():
    source = json.loads(FIXTURE.read_text()); cases = []
    # Exactly the same independent uniform targets as the catalog controls:
    # paired comparisons only, not a new set of independent population samples.
    catalog = json.loads((ROOT/"research/phase_workbench/ternary_repair_catalog.json").read_text())
    for index in range(len(source["planted_geometry_probes"])):
        old = source["planted_geometry_probes"][index]
        Q = int(old["modulus"]); A = tuple(int(x) for x in old["labels"])
        problem = LowProblem((Q,), tuple(((a,), (c,)) for a, c in zip(A[::2], A[1::2])), 0)
        policy = frozen_policy(problem, old["prepared"]); compiled = compile_adaptive(policy)
        trials = []
        for t in catalog["cases"][index]["uniform_target_trials"]:
            target = (int(t["target"]),)
            for cut in ("sphere", "projector"):
                for budget in (256, 2048):
                    answer = adaptive_pair(problem, target, policy, compiled, budget, cut)
                    trials.append({"target": str(target[0]), "cut": cut, "node_budget": budget, **answer})
        cases.append({"fixture_probe_index": index, "root_digits": old["root_digits"], "width": problem.width,
            "Q": str(Q), "labels": [str(x) for x in A], "fingerprint": policy["frozen_geometry_sha256"],
            "targets_shared_with_catalog_conditional_comparison": True, "targets_per_labels": 8, "basis_index": 0,
            "mitm_reference_half_assignment_counts": [str(3**(problem.width//2)), str(3**(problem.width-problem.width//2))],
            "trials": trials})
    return {"status": "TARGET_ADAPTIVE_EXACT_SHELL_BASELINE_NOT_POLYNOMIAL_SOLVER", "local_derivations_review_pending": True,
        "novelty_claim": False, "polynomial_pair_finder_proved": False, "population_coverage_proved": False,
        "target_independent_catalog_bound_applies": False, "sphere_enumeration_is_known_classical_method": True,
        "source_training_or_unknown_phase_supplied": False, "node_caps_do_not_certify_empty_fibers": True,
        "original_LLL_and_policy_compilation_not_in_decode_wall_seconds": True, "total_physical_wall_runtime_measured": False,
        "all_preparation_and_failure_costs_charged": True, "catalog_target_fixture": "research/phase_workbench/ternary_repair_catalog.json",
        "cases": cases}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--write", action="store_true")
    args = parser.parse_args(); report = build_report()
    if args.write:
        REPORT.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"status": report["status"], "cases": [{"root_digits": c["root_digits"],
        "summaries": [{"cut": cut, "budget": budget,
            "pairs": sum(bool(t["pair"]) for t in c["trials"] if t["cut"] == cut and t["node_budget"] == budget),
            "statuses": dict(Counter(t["status"] for t in c["trials"] if t["cut"] == cut and t["node_budget"] == budget)),
            "nodes": sum(t["cost"]["coefficient_nodes"] for t in c["trials"] if t["cut"] == cut and t["node_budget"] == budget)}
            for cut in ("sphere", "projector") for budget in (256, 2048)]} for c in report["cases"]]}, indent=2))
