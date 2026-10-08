"""Exact elimination of orthogonal code-zero directions; bounded active search.

The reduced objective retains periodic coupling, not a small Euclidean CVP.
Saved label-only LLL bases are reused; new validation follows frozen selection.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import random
import time

from flint import fmpq

from ternary_character_synchronization import _records
from ternary_covariant_noise import CovariantRecord, heldout_gate, heldout_score, simulated_record
from ternary_full_record_cvp import REPORT as PARENT, exact_sparse_profile, rounding_influence
from ternary_measured_lattice_decoder import code_point_to_secret, exact_json, integer, native_loss
from ternary_native_cvp_reduction import squared_residual_cost

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT / "research/TERNARY_QUOTIENT_CVP.md"
REPORT = ROOT / "research/classical_baselines/ternary_quotient_cvp.json"


def nearest(value):
    return (2*int(value.numerator)+int(value.denominator))//(2*int(value.denominator))


def compile_quotient(model, rows):
    rows = tuple(tuple(row) for row in rows)
    if model["status"] != "EXACT_PUBLIC_CODE_LATTICE" or len(rows) != model["lattice_equations"]:
        raise ValueError("complete public code lattice required")
    profile = exact_sparse_profile(rows)
    if profile["gram_determinant"] != int(model["lattice_index"])**2:
        raise ValueError("complete lattice determinant required")
    influence = rounding_influence(model, rows, profile)
    dead = set(influence["dead_rounding_positions"])
    coupling = tuple((i, j) for i in sorted(dead) for j in sorted(profile["mu"][i]) if j in dead)
    certificate = {"live_positions": influence["influential_rounding_positions"],
                   "dead_positions": tuple(sorted(dead)), "dead_dead_GS_edges": coupling,
                   "full_dimension": len(rows), "integer_search_dimension": len(rows)-len(dead),
                   "conditional_minimum_is_global_CVP": False,
                   "reduced_objective_is_ordinary_Euclidean_CVP": False}
    if coupling:
        return {"status": "UNKNOWN_COUPLED_DEAD_DIRECTIONS", "certificate": certificate}
    return {"status": "EXACT_ORTHOGONAL_DEAD_ELIMINATION", "certificate": certificate,
            "model": model, "rows": rows, "profile": profile, "influence": influence}


def target_coordinates(compiled, target):
    rows, p = compiled["rows"], compiled["profile"]
    target = tuple(target)
    if len(target) != len(rows) or any(type(x) is not int for x in target):
        raise ValueError("complete integer target required")
    inner = []
    for i, row in enumerate(rows):
        inner.append(fmpq(sum(x*y for x, y in zip(row, target)))
                     -sum((mu*inner[j] for j, mu in p["mu"][i].items()), fmpq(0)))
    return tuple(x/d for x, d in zip(inner, p["gs_squared"]))


def conditional_point(compiled, target, active_coefficients, initial=None):
    if compiled["status"] != "EXACT_ORTHOGONAL_DEAD_ELIMINATION":
        raise ValueError("orthogonal dead-direction certificate required")
    live = compiled["certificate"]["live_positions"]
    values = tuple(active_coefficients)
    if len(values) != len(live) or any(type(x) is not int for x in values):
        raise ValueError("one integer per live coefficient required")
    initial = target_coordinates(compiled, target) if initial is None else initial
    p, rows = compiled["profile"], compiled["rows"]
    coordinates, coefficients = list(initial), [0]*len(rows)
    fixed = dict(zip(live, values))
    cost = fmpq(0)
    for i in range(len(rows)-1, -1, -1):
        value = coordinates[i]
        coefficients[i] = fixed[i] if i in fixed else nearest(value)
        cost += p["gs_squared"][i]*(value-coefficients[i])**2
        for j, mu in p["mu"][i].items():
            coordinates[j] -= coefficients[i]*mu
    point = tuple(sum(a*row[j] for a, row in zip(coefficients, rows) if a) for j in range(len(rows)))
    distance = sum((x-y)**2 for x, y in zip(point, target))
    if cost.denominator != 1 or int(cost.numerator) != distance:
        raise ArithmeticError("conditional objective disagrees with full Euclidean distance")
    return {"active_coefficients": values, "coefficients": tuple(coefficients), "point": point,
            "supplied_Euclidean_cost": distance,
            "candidate": code_point_to_secret(compiled["model"], point)}


def beam_search(compiled, target, width=32, radius=1):
    integer(width, "positive beam width", 1)
    integer(radius, "coefficient branch radius")
    if compiled["status"] != "EXACT_ORTHOGONAL_DEAD_ELIMINATION":
        return {"status": compiled["status"], "candidates": [], "CVP_optimality_certified": False}
    p = compiled["profile"]
    live = tuple(reversed(compiled["certificate"]["live_positions"]))
    dead = set(compiled["certificate"]["dead_positions"])
    initial = target_coordinates(compiled, target)
    # Dead centers depend only on live coefficients. Finalize their costs as
    # soon as the last (lowest-index) live influencer has been assigned.
    finish = {i: [] for i in live}
    dependencies = {j: [] for j in dead}
    for i in live:
        for j, mu in p["mu"][i].items():
            if j in dead:
                dependencies[j].append(i)
    constant = fmpq(0)
    for j in sorted(dead):
        if dependencies[j]:
            finish[min(dependencies[j])].append(j)
        else:
            constant += p["gs_squared"][j]*(initial[j]-nearest(initial[j]))**2
    beam = [(constant, (), list(initial))]
    stages = []
    for i in live:
        children = []
        for cost, assigned, coordinates in beam:
            center = coordinates[i]
            for a in range(nearest(center)-radius, nearest(center)+radius+1):
                updated = list(coordinates)
                value = cost+p["gs_squared"][i]*(center-a)**2
                for j, mu in p["mu"][i].items():
                    updated[j] -= a*mu
                for j in finish[i]:
                    value += p["gs_squared"][j]*(updated[j]-nearest(updated[j]))**2
                children.append((value, assigned+(a,), updated))
        children.sort(key=lambda state: (state[0], state[1]))
        beam = children[:width]
        stages.append({"live_position": i, "expanded_states": len(children),
                       "retained_states": len(beam), "finalized_dead_positions": tuple(finish[i]),
                       "best_exact_partial_cost": str(beam[0][0])})
    finalists = []
    for cost, assigned, _ in beam:
        point = conditional_point(compiled, target, tuple(reversed(assigned)), initial)
        if cost != point["supplied_Euclidean_cost"]:
            raise ArithmeticError("beam objective did not finalize all original dimensions")
        finalists.append(point)
    return {"status": "BOUNDED_LIVE_COEFFICIENT_BEAM", "beam_width": width,
            "branch_radius": radius, "stages": stages, "candidates": finalists,
            "expanded_states": sum(stage["expanded_states"] for stage in stages),
            "conditional_elimination_exact": True, "CVP_optimality_certified": False,
            "near_exact_approximation_guarantee": False,
            "complete_integer_coefficient_enumeration": False}


def decode_saved(model, rows, records, inherited_candidates=(), width=32, radius=1, inherited_lll_calls=0):
    integer(inherited_lll_calls, "inherited LLL calls")
    records, n, q = _records(records)
    if model["secret_dimension"] != n or model["modulus"] != q:
        raise ValueError("saved lattice and measured records must have identical full-root source parameters")
    compiled = compile_quotient(model, rows)
    if compiled["status"] != "EXACT_ORTHOGONAL_DEAD_ELIMINATION":
        return {"status": compiled["status"], "certificate": compiled["certificate"], "selections": {}}
    target = tuple(x for record in records for x in record.outcome)
    if tuple(row for record in records for row in (record.first, record.second)) != tuple(tuple(row) for row in model["frequency_rows"]):
        raise ValueError("saved lattice must use exactly the current original labels")
    search = beam_search(compiled, target, width, radius)
    inherited = tuple(sorted(set(tuple(s) for s in inherited_candidates)))
    candidates = sorted(set(inherited) | {path["candidate"] for path in search["candidates"]})
    scores = {s: {"candidate": s, "Euclidean_cost": squared_residual_cost(records, s),
                  "native_loss": native_loss(records, s), "native_score": heldout_score(records, s)} for s in candidates}
    selections = {"Euclidean": min(candidates, key=lambda s: scores[s]["Euclidean_cost"]),
                  "native_likelihood": min(candidates, key=lambda s: scores[s]["native_loss"])}
    return {"status": search["status"], "certificate": compiled["certificate"], "search": search,
            "inherited_candidates": inherited,
            "proposal_scores": tuple({**scores[s], "native_loss": str(scores[s]["native_loss"])} for s in candidates),
            "selections": selections, "all_original_records_in_objective": True,
            "cost": {"original_training_qutrits_reused": len(records), "new_training_qutrits": 0,
                     "new_LLL_calls": 0, "inherited_LLL_calls": inherited_lll_calls,
                     "full_lattice_dimension": len(rows), "integer_search_dimension": len(compiled["certificate"]["live_positions"]),
                     "expanded_states": search["expanded_states"], "distinct_candidates_scored": len(candidates)},
            "hidden_secret_or_validation_supplied_to_optimizer": False,
            "accepted_speedup_candidate": False, "classical_dequantization_or_hardness_proved": False}


def saved_rows(decoder):
    width = decoder["model"]["lattice_equations"]
    output = []
    for entries in decoder["reduced_rows_sparse"]:
        row = [0]*width
        for j, x in entries:
            row[j] = int(x)
        output.append(tuple(row))
    return tuple(output)


def systematic_quotient_rows(model):
    """q-axes first always leaves just n live coordinates: not a discovery."""
    n, m, q = model["secret_dimension"], model["lattice_equations"], model["modulus"]
    generators = model.get("code_generator_rows")
    if generators is None:
        generators = model["lattice_rows"][:n]
    generators = tuple(tuple(row) for row in generators)
    pivots = tuple(model["unit_basis_rows"])
    if len(generators) != n or any(len(row) != m for row in generators):
        raise ValueError("complete systematic code generators required")
    for i, row in enumerate(generators):
        if any(row[j] != int(i == k) for k, j in enumerate(pivots)):
            raise ValueError("exact identity pivot coordinates required")
        code_point_to_secret(model, row)
    axes = tuple(tuple(q*int(k == j) for k in range(m)) for j in range(m) if j not in pivots)
    return axes+generators


def systematic_projection_certificate(model):
    rows = systematic_quotient_rows(model)
    n, m, q = model["secret_dimension"], model["lattice_equations"], model["modulus"]
    # Orthogonal q-axes remove every nonpivot component of each generator;
    # the surviving projected rows are the n orthonormal pivot axes.
    return {"systematic_integer_search_dimension": n, "orthogonal_dead_directions": m-n,
            "projected_live_GS_norms_squared": (1,)*n,
            "complete_mod_q_secret_classes": q**n,
            "orthogonal_axis_norm_squared": q*q,
            "LLL_influence_dimension_is_intrinsic_unknown_count": False,
            "systematic_projection_is_new_algorithmic_dimension_reduction": False,
            "periodic_objective_preserves_original_secret_search": True,
            "all_systematic_rows_in_original_lattice": len(rows) == m}


def build_report(parent_path=PARENT):
    parent_bytes = Path(parent_path).read_bytes()
    parent = json.loads(parent_bytes)
    if parent["status"] != "FULL_RECORD_NATIVE_CVP_ATTEMPT_REVIEW_PENDING":
        raise ValueError("completed parent optimizer required")
    controls = []
    for previous in parent["controls"]:
        records = tuple(CovariantRecord(**record) for record in previous["training_records"])
        started = time.monotonic()
        decoder = decode_saved(previous["decoder"]["model"], saved_rows(previous["decoder"]), records,
                               (item["candidate"] for item in previous["decoder"]["proposal_scores"]),
                               inherited_lll_calls=previous["decoder"]["cost"]["LLL_calls"])
        elapsed = time.monotonic()-started
        if not decoder["selections"]:
            raise ValueError("precommitted cohort fails exact elimination; preserve failure before redesign")
        # Fresh seed and IDs: parent validation motivated this attack and is
        # explicitly excluded from both optimization and validation reuse.
        seed, q = 120200+previous["seed"], previous["modulus"]
        rng, secret = random.Random(seed), tuple(previous["calibration_secret"])
        fresh = []
        for _ in range(512):
            a, c = (tuple(rng.randrange(q) for _ in secret) for _ in range(2))
            fresh.append(simulated_record(a, c, secret, q, rng)[0])
        trials = set(decoder["selections"].values())
        gate = heldout_gate(len(fresh), len(trials))
        verification = {name: {"candidate": s, "fresh_score": heldout_score(fresh, s),
                               "threshold_passed": heldout_score(fresh, s) >= .5,
                               "calibration_recovered": s == secret} for name, s in decoder["selections"].items()}
        best = min(item["Euclidean_cost"] for item in decoder["proposal_scores"])
        comparison = previous["CVP_comparison_certificate"]
        margin = 64*best-81*int(comparison["valid_point_squared_distance"])
        controls.append({"parent_seed": previous["seed"], "fresh_seed": seed, "decoder": decoder,
                         "systematic_coordinate_self_critique": systematic_projection_certificate(previous["decoder"]["model"]),
                         "n": previous["n"], "root_digits": previous["root_digits"],
                         "density_per_n_r": previous["density_per_n_r"], "verification": verification,
                         "heldout_records": tuple(record.public() for record in fresh),
                         "heldout_source_IDs": tuple(f"quotient-cvp-{seed}-fresh-{j}" for j in range(512)),
                         "joint_fixed_candidate_gate": gate, "parent_training_and_basis_reused": True,
                         "old_heldout_records_used_by_optimizer_or_validator": False,
                         "new_original_qutrits": 512, "total_inherited_training_plus_new_validation": len(records)+512,
                         "old_validation_not_erased_from_total_research_cost": True,
                         "cumulative_original_qutrits_including_old_validation": len(records)+1024,
                         "best_Euclidean_cost": best, "parent_best_Euclidean_cost": min(int(item["Euclidean_cost"]) for item in previous["decoder"]["proposal_scores"]),
                         "strict_integer_factor_failure_margin": margin,
                         "norm_9_over_8_approximation_falsified": margin > 0,
                         "optimizer_wall_seconds_excluding_inherited_LLL": elapsed})
        print(json.dumps({"n": previous["n"], "r": previous["root_digits"],
                          "full_dimension": decoder["cost"]["full_lattice_dimension"],
                          "active_dimension": decoder["cost"]["integer_search_dimension"],
                          "recoveries": {name: item["calibration_recovered"] for name, item in verification.items()},
                          "seconds": round(elapsed, 3)}), flush=True)
    return {"status": "EXACT_QUOTIENT_COMPILER_BOUNDED_SEARCH_REVIEW_PENDING",
            "parent_report_sha256": hashlib.sha256(parent_bytes).hexdigest(),
            "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "controls": controls, "old_cohorts_influenced_design": True,
            "new_IID_training_or_new_LLL_run": False, "fresh_validation_after_selection": True,
            "population_recovery_or_speedup_claim": False,
            "near_exact_CVP_solver_implemented": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--replay-saved", action="store_true",
                        help="Refresh mathematical certificates on existing data; no new attack or validation")
    args = parser.parse_args()
    if args.replay_saved:
        report = json.loads(REPORT.read_text())
        parent_bytes = PARENT.read_bytes()
        if report["parent_report_sha256"] != hashlib.sha256(parent_bytes).hexdigest():
            raise ValueError("certificate-only refresh cannot replace parent source evidence")
        parent = json.loads(parent_bytes)
        for control, previous in zip(report["controls"], parent["controls"], strict=True):
            if control["parent_seed"] != previous["seed"]:
                raise ValueError("identical saved control identities required")
            control["systematic_coordinate_self_critique"] = systematic_projection_certificate(previous["decoder"]["model"])
        report["derivation_sha256"] = hashlib.sha256(DERIVATION.read_bytes()).hexdigest()
        report["certificate_replay_is_new_source_or_decoder_run"] = False
    else:
        report = build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(report), indent=2)+"\n")
    print(json.dumps({"status": report["status"], "controls": len(report["controls"]),
                      "recoveries": {name: sum(c["verification"][name]["calibration_recovered"] for c in report["controls"])
                                     for name in ("Euclidean", "native_likelihood")},
                      "exact_9_over_8_counterexamples": sum(c["norm_9_over_8_approximation_falsified"] for c in report["controls"]),
                      "near_exact_CVP_solver_implemented": False}, indent=2))


if __name__ == "__main__":
    main()
