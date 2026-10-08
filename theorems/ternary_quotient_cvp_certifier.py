"""Complete exact sphere search on the compiled periodic objective, or UNKNOWN.

Finite certificates are not efficient population decoders. A node cap cannot
certify nearestness, hardness, or the9/8 factor from lack of better points.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import time

from flint import fmpq

from ternary_full_record_cvp import REPORT as ORIGINAL
from ternary_measured_lattice_decoder import exact_json, integer
from ternary_quotient_cvp import (
    REPORT as QUOTIENT, beam_search, compile_quotient, conditional_point, nearest,
    saved_rows, target_coordinates,
)

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT / "research/TERNARY_QUOTIENT_CVP_CERTIFIER.md"
REPORT = ROOT / "research/classical_baselines/ternary_quotient_cvp_certifier.json"


def sphere_search(compiled, target, node_cap=4096, incumbent_active=None):
    integer(node_cap, "exact search node cap")
    if compiled["status"] != "EXACT_ORTHOGONAL_DEAD_ELIMINATION":
        return {"status": compiled["status"], "CVP_optimality_certified": False}
    initial = target_coordinates(compiled, target)
    p = compiled["profile"]
    live = tuple(reversed(compiled["certificate"]["live_positions"]))
    dead = set(compiled["certificate"]["dead_positions"])
    if incumbent_active is None:
        incumbent = beam_search(compiled, target, width=1, radius=0)["candidates"][0]
    else:
        incumbent = conditional_point(compiled, target, tuple(incumbent_active), initial)
    original_incumbent = incumbent
    upper = fmpq(incumbent["supplied_Euclidean_cost"])
    finish = {i: [] for i in live}
    dependencies = {j: [] for j in dead}
    for i in live:
        for j in p["mu"][i]:
            if j in dead:
                dependencies[j].append(i)
    constant = fmpq(0)
    for j in sorted(dead):
        if dependencies[j]:
            finish[min(dependencies[j])].append(j)
        else:
            constant += p["gs_squared"][j]*(initial[j]-nearest(initial[j]))**2
    counters = {"tested_coefficient_extensions": 0, "partial_cost_prunes": 0,
                "completed_live_assignments": 0, "strict_incumbent_improvements": 0}
    trace = []
    exhausted = False

    def visit(depth, cost, assigned, coordinates):
        nonlocal incumbent, upper, exhausted
        if cost > upper:
            counters["partial_cost_prunes"] += 1
            return
        if depth == len(live):
            point = conditional_point(compiled, target, tuple(reversed(assigned)), initial)
            if cost != point["supplied_Euclidean_cost"]:
                raise ArithmeticError("complete exact search objective disagrees with full distance")
            counters["completed_live_assignments"] += 1
            if cost < upper:
                incumbent, upper = point, cost
                counters["strict_incumbent_improvements"] += 1
                trace.append({"at_extension": counters["tested_coefficient_extensions"],
                              "active_coefficients": point["active_coefficients"],
                              "supplied_Euclidean_cost": point["supplied_Euclidean_cost"]})
            return
        i = live[depth]
        center, offset = coordinates[i], 0
        base = nearest(center)
        # Every coefficient is eventually visited unless its GS cost exceeds
        # the shrinking valid radius. Once BOTH outward fronts exceed it,
        # all further integers are excluded by monotonic distance from center.
        while True:
            options = (base,) if offset == 0 else (base-offset, base+offset)
            relevant = False
            for a in options:
                increment = p["gs_squared"][i]*(center-a)**2
                if cost+increment > upper:
                    continue
                relevant = True
                if counters["tested_coefficient_extensions"] >= node_cap:
                    exhausted = True
                    return
                counters["tested_coefficient_extensions"] += 1
                updated = list(coordinates)
                for j, mu in p["mu"][i].items():
                    updated[j] -= a*mu
                value = cost+increment
                for j in finish[i]:
                    value += p["gs_squared"][j]*(updated[j]-nearest(updated[j]))**2
                visit(depth+1, value, assigned+(a,), updated)
                if exhausted:
                    return
            if not relevant:
                break
            offset += 1

    visit(0, constant, (), list(initial))
    return {"status": "UNKNOWN_NODE_CAP_EXHAUSTED" if exhausted else "EXACT_FINITE_CVP_OPTIMUM_CERTIFIED",
            "CVP_optimality_certified": not exhausted, "node_cap": node_cap,
            "search_counters": counters, "strict_improvement_trace": trace,
            "initial_incumbent": original_incumbent, "best_point": incumbent,
            "initial_squared_radius": original_incumbent["supplied_Euclidean_cost"],
            "final_squared_radius": incumbent["supplied_Euclidean_cost"],
            "unbounded_integer_coefficients_handled_by_exact_radius": True,
            "all_live_branches_within_radius_exhausted": not exhausted,
            "cost_pruning_uses_exact_nonnegative_partial_bound": True,
            "cap_exhaustion_certifies_approximation_or_hardness": False,
            "efficient_population_decoder_or_speedup": False}


def point_active_coefficients(compiled, point):
    """Exact public inverse basis coordinates; no reduced-transform inverse."""
    coordinates = list(target_coordinates(compiled, tuple(point)))
    coefficients = [0]*len(coordinates)
    for i in range(len(coordinates)-1, -1, -1):
        if coordinates[i].denominator != 1:
            raise ValueError("point is not in the represented complete integer lattice")
        a = int(coordinates[i].numerator)
        coefficients[i] = a
        for j, mu in compiled["profile"]["mu"][i].items():
            coordinates[j] -= a*mu
    return tuple(coefficients[i] for i in compiled["certificate"]["live_positions"])


def build_report():
    original_bytes, quotient_bytes = ORIGINAL.read_bytes(), QUOTIENT.read_bytes()
    original, quotient = json.loads(original_bytes), json.loads(quotient_bytes)
    if quotient["parent_report_sha256"] != hashlib.sha256(original_bytes).hexdigest():
        raise ValueError("quotient evidence must pin the actual original report")
    controls = []
    for previous, improved in zip(original["controls"], quotient["controls"], strict=True):
        if previous["seed"] != improved["parent_seed"]:
            raise ValueError("exact matching cohorts required")
        decoder = previous["decoder"]
        compiled = compile_quotient(decoder["model"], saved_rows(decoder))
        target = tuple(y for record in previous["training_records"] for y in record["outcome"])
        proposal = min(improved["decoder"]["proposal_scores"], key=lambda item: int(item["Euclidean_cost"]))
        candidate, q = tuple(proposal["candidate"]), previous["modulus"]
        point = tuple(y-((y-sum(a*s for a, s in zip(row, candidate))+q//2) % q-q//2)
                      for record in previous["training_records"]
                      for row, y in zip((record["first"], record["second"]), record["outcome"]))
        active = point_active_coefficients(compiled, point)
        canonical = conditional_point(compiled, target, active)
        if canonical["point"] != point or canonical["supplied_Euclidean_cost"] != int(proposal["Euclidean_cost"]):
            raise ArithmeticError("canonical best public proposal is not its exact conditional minimum")
        started = time.monotonic()
        result = sphere_search(compiled, target, incumbent_active=active)
        elapsed = time.monotonic()-started
        # Calibration truth and the old validation batches are not optimizer
        # inputs. Comparison is posthoc only; a changed point is NOT assigned
        # the predecessor's fresh-validation success or confidence bound.
        best = result["best_point"]
        W = int(previous["CVP_comparison_certificate"]["valid_point_squared_distance"])
        margin = 64*best["supplied_Euclidean_cost"]-81*W
        controls.append({"parent_seed": previous["seed"], "n": previous["n"],
                         "root_digits": previous["root_digits"], "density_per_n_r": previous["density_per_n_r"],
                         "full_dimension": compiled["certificate"]["full_dimension"],
                         "active_dimension": compiled["certificate"]["integer_search_dimension"],
                         "initial_incumbent_source": "BEST_PUBLIC_TRAINING_PROPOSAL_CANONICAL_POINT",
                         "initial_candidate": candidate,
                         "result": result, "strict_integer_factor_failure_margin": margin,
                         "norm_9_over_8_approximation_falsified": margin > 0,
                         "calibration_secret_match_diagnostic_only": tuple(best["candidate"]) == tuple(previous["calibration_secret"]),
                         "fresh_validation_performed": False, "new_original_qutrits": 0,
                         "inherited_original_qutrits_including_both_validation_batches": improved["cumulative_original_qutrits_including_old_validation"],
                         "new_LLL_calls": 0, "search_wall_seconds": elapsed})
        print(json.dumps({"n": previous["n"], "r": previous["root_digits"],
                          "status": result["status"], "extensions": result["search_counters"]["tested_coefficient_extensions"],
                          "seconds": round(elapsed, 3)}), flush=True)
    return {"status": "EXACT_QUOTIENT_SPHERE_SEARCH_CERTIFICATION_REVIEW_PENDING",
            "original_report_sha256": hashlib.sha256(original_bytes).hexdigest(),
            "quotient_report_sha256": hashlib.sha256(quotient_bytes).hexdigest(),
            "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "controls": controls, "new_training_validation_or_LLL_run": False,
            "near_exact_population_solver_or_classical_hardness_proved": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write:
        REPORT.write_text(json.dumps(exact_json(report), indent=2)+"\n")
    print(json.dumps({"status": report["status"], "controls": len(report["controls"]),
                      "certified_optima": sum(c["result"]["CVP_optimality_certified"] for c in report["controls"]),
                      "unknown_capped_controls": sum(not c["result"]["CVP_optimality_certified"] for c in report["controls"]),
                      "population_solver": False}, indent=2))


if __name__ == "__main__":
    main()
