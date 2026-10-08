"""Finite cyclic Fourier-positivity repair of the native character SDP.

Constructive numerical decoder experiment plus exact old-witness rejection.
No population recovery theorem, scalable success, novelty or speedup claim.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import random

import numpy as np
from scipy.sparse import csr_matrix

from ternary_character_sdp_decoder import (
    REPORT as SOURCE_REPORT, _public_decoding, audit_matrix, compile_model, coordinate_refine,
    rounded_proposals, solve_relaxation, verify_fresh,
)
from ternary_character_sdp_gap_certificate import REPORT as GAP_REPORT, root_intervals
from ternary_covariant_noise import CovariantRecord, root_digits, simulated_record
from ternary_cyclic_extractor import random_even_source

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/classical_baselines/ternary_character_cyclic_decoder.json"
DERIVATION = ROOT / "research/TERNARY_CHARACTER_CYCLIC_DECODER.md"


def represented_differences(nodes, q):
    root_digits(q)
    if not nodes or not nodes[0] or len(set(map(tuple, nodes))) != len(nodes) or any(
            len(row) != len(nodes[0]) or any(type(x) is not int or not 0 <= x < q for x in row) for row in nodes):
        raise ValueError("distinct rectangular canonical full-root frequency nodes required")
    return {tuple((a-b) % q for a, b in zip(u, v)): i*len(nodes)+j
            for i, u in reversed(tuple(enumerate(nodes))) for j, v in reversed(tuple(enumerate(nodes)))}


def complete_cyclic_groups(nodes, q, max_order=81, max_constraints=200000):
    if any(type(x) is not int or x < 1 for x in (max_order, max_constraints)):
        raise ValueError("positive whole cyclic-order and constraint caps required")
    if q > max_order:
        return {"status": "CYCLIC_ORDER_CAP_EXHAUSTED", "partial_cyclic_scan_used": False}
    differences = represented_differences(nodes, q)
    visited, groups, count = set(), [], 0
    for d in differences:
        order = q//math.gcd(q, *d)
        if order == 1:
            continue
        canonical = min(tuple(k*x % q for x in d) for k in range(1, order) if math.gcd(k, order) == 1)
        if canonical in visited:
            continue
        visited.add(canonical)
        powers = tuple(tuple(k*x % q for x in canonical) for k in range(order))
        if all(x in differences for x in powers):
            count += order
            if count > max_constraints:
                return {"status": "CYCLIC_CONSTRAINT_CAP_EXHAUSTED", "partial_cyclic_scan_used": False}
            groups.append({"order": order, "generator": canonical,
                           "power_entries": tuple(differences[x] for x in powers)})
    groups.sort(key=lambda g: (g["order"], g["generator"]))
    return {"status": "ALL_REPRESENTED_COMPLETE_CYCLIC_GROUPS", "groups": groups,
            "constraints": count, "distinct_represented_differences": len(differences),
            "all_full_group_cyclic_subgroups_enumerated": False,
            "incomplete_subgroups_silently_completed": False}


def augment_model(model, max_order=81, max_constraints=200000):
    if model["status"] != "COMPILED":
        return model
    description = complete_cyclic_groups(model["nodes"], model["modulus"], max_order, max_constraints)
    if description["status"] != "ALL_REPRESENTED_COMPLETE_CYCLIC_GROUPS":
        return {**description, "dimension": model["dimension"], "modulus": model["modulus"]}
    rows, cols, values, row = [], [], [], 0
    for group in description["groups"]:
        m = group["order"]
        for t in range(m):
            for k, entry in enumerate(group["power_entries"]):
                rows.append(row)
                cols.append(entry)
                values.append(np.exp(-2j*np.pi*k*t/m)/m)
            row += 1
    operator = csr_matrix((values, (rows, cols)), shape=(row, model["matrix_nodes"]**2), dtype=complex)
    return {**model, "cyclic_fourier_operator": operator, "cyclic_description": description,
            "cyclic_compilation_reads_truth_or_outcomes": False,
            "cyclic_cost_polynomial_in_q_not_logq": True}


def _bounded_product(coefficient, interval, component, lower):
    endpoint = "lower" if (coefficient >= 0) == lower else "upper"
    return coefficient*interval[component+"_"+endpoint]


def exact_old_witness_audit(certificate):
    q, nodes, witness = certificate["modulus"], certificate["nodes"], certificate["witness"]
    K, S = len(nodes), witness["moment_scale"]
    description = complete_cyclic_groups(nodes, q)
    re, im = witness["matrix_real_integer"], witness["matrix_imag_integer"]
    violations, least_upper = [], None
    for gi, group in enumerate(description["groups"]):
        m = group["order"]
        roots = root_intervals(m)
        for t in range(m):
            upper = 0
            for k, entry in enumerate(group["power_entries"]):
                i, j = divmod(entry, K)
                interval = roots[k*t % m]
                upper += _bounded_product(re[i][j], interval, "cos", False)
                upper += _bounded_product(im[i][j], interval, "sin", False)
            value = Fraction(upper, S*2**48*m)
            if least_upper is None or value < least_upper:
                least_upper = value
            if upper < 0:
                violations.append({"group_index": gi, "sector": t, "order": m,
                                   "generator": group["generator"], "probability_upper_numerator": str(upper),
                                   "probability_upper_denominator": str(S*2**48*m)})
    # First-moment root polygons are a strictly weaker proposed repair.
    differences = represented_differences(nodes, q)
    polygon_minimum, polygon_checks = None, 0
    for d, entry in differences.items():
        m = q//math.gcd(q, *d)
        if m == 1:
            continue
        i, j = divmod(entry, K)
        roots = root_intervals(m)
        for t in range(m):
            h = ((m-1)//2-t) % m
            margin = -S*roots[(m-1)//2]["cos_upper"]
            margin += _bounded_product(re[i][j], roots[h], "cos", True)
            margin += _bounded_product(-im[i][j], roots[h], "sin", True)
            polygon_minimum = margin if polygon_minimum is None else min(margin, polygon_minimum)
            polygon_checks += 1
    return {"seed": certificate["seed"], "description": description,
            "exact_negative_cyclic_probabilities": violations,
            "negative_laws_certified": len(violations),
            "negative_cyclic_groups_certified": len({x["group_index"] for x in violations}),
            "least_probability_upper_exact": str(least_upper),
            "first_moment_polygons_pass_exactly": polygon_minimum is not None and polygon_minimum >= 0,
            "first_moment_polygon_checks": polygon_checks,
            "minimum_polygon_margin_integer": str(polygon_minimum), "polygon_margin_denominator": str(S*2**48),
            "full_secret_enumeration_used_to_find_cuts": False,
            "cyclic_positivity_proves_global_realizability": False}


def run_control(original, fresh_count=256, saved=None):
    records = tuple(CovariantRecord(tuple(r["first"]), tuple(r["second"]), tuple(r["outcome"]), r["modulus"])
                    for r in original["training_records"])
    seed, n, q = original["seed"], original["dimension"], records[0].modulus
    model = augment_model(compile_model(records, max_matrix_nodes=384))
    if saved is None:
        solution = solve_relaxation(model)
        solution["numerical_solver_reexecuted_this_run"] = True
    else:
        if json.dumps(saved["model"]["nodes"]) != json.dumps(model["nodes"]) or json.dumps(saved["model"]["cyclic_description"]) != json.dumps(model["cyclic_description"]):
            raise ValueError("saved matrix belongs to a different public model")
        solution = dict(saved["solver"])
        matrix = np.array(solution.pop("matrix_real"))+1j*np.array(solution.pop("matrix_imag"))
        solution["matrix"] = matrix
        solution["audit"] = audit_matrix(model, matrix)
        solution["status"] = "SOLVED_NUMERICALLY" if solution["audit"]["numerically_feasible"] else "UNCERTIFIED_SOLVER_OUTPUT"
        solution["numerical_solver_reexecuted_this_run"] = False
    candidate, proposals, refinement = None, None, None
    if solution["status"] == "SOLVED_NUMERICALLY":
        proposals = rounded_proposals(model, solution["matrix"], seed=seed, gaussian_draws=12)
        refinement = coordinate_refine(records, proposals["proposals"], sweeps=2)
        candidate = refinement["candidate"]
    public_model = {k: v for k, v in model.items() if k != "cyclic_fourier_operator"}
    public = _public_decoding({"model": public_model, "solver": solution})
    result = {"seed": seed, "dimension": n, "modulus": q, "candidate": candidate,
              "model": public["model"], "solver": public["solver"], "rounding": proposals,
              "refinement": refinement, "old_training_ids": original["decoder"]["original_ids"],
              "reused_classical_training_records_are_not_reused_quantum_inputs": True,
              "old_holdout_used_for_validation": False, "population_recovery_proved": False}
    # Freeze all candidates before accessing this physically new validation cohort.
    selected = {"cyclic": candidate, "old_SDP": original["decoder"]["candidate"],
                "classical14": original["decoder"]["matched_nonSDP_baseline"]["candidate"],
                "classical256": original["decoder"]["stronger_nonSDP_baseline"]["candidate"]}
    selected = {name: tuple(s) if s is not None else None for name, s in selected.items()}
    truth = tuple(original["calibration_secret_NOT_decoder_input"])
    source = random_even_source(n, 2*original["root_digits"], fresh_count, seed+100)
    rng = random.Random(seed+101)
    fresh = tuple(simulated_record(a, c, truth, q, rng)[0] for a, c in source.frequencies)
    ids = tuple(f"cyclic-{seed}-NEW-fresh-{i}" for i in range(fresh_count))
    result["fresh_source"] = {"seed": seed+100, "original_level": source.level,
                              "original_ring_labels": source.labels, "records": [r.public() for r in fresh]}
    result["new_fresh_native_qutrits"] = fresh_count
    result["historical_training_native_qutrits"] = len(records)
    result["fresh_verification"] = {name: verify_fresh(fresh, s, ids, result["old_training_ids"])
                                     for name, s in selected.items() if s is not None}
    result["calibration_recovery_NOT_decoder_input"] = {name: s == truth for name, s in selected.items() if s is not None}
    result["simultaneous_four_method_false_acceptance_upper"] = min(1., 4*math.exp(-2*fresh_count/81))
    result["independent_physical_source_supply_certified_by_seeds"] = False
    result["saved_matrix_replay_is_not_a_new_independent_experiment"] = saved is not None
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--replay-saved-matrices", action="store_true",
                        help="revalidate saved matrices and replay the SAME fixed experiment; do not rerun expensive SCS")
    args = parser.parse_args()
    source, gaps = json.loads(SOURCE_REPORT.read_text()), json.loads(GAP_REPORT.read_text())
    saved = {}
    if args.replay_saved_matrices:
        old = json.loads(REPORT.read_text())
        if old["source_report_sha256"] != hashlib.sha256(SOURCE_REPORT.read_bytes()).hexdigest() or old["gap_report_sha256"] != hashlib.sha256(GAP_REPORT.read_bytes()).hexdigest():
            raise ValueError("saved matrices have changed parent records or certificates")
        saved = {c["seed"]: c for c in old["controls"]}
    report = {"status": "NATIVE_COMPLETE_CYCLIC_POSITIVITY_REPAIR_NUMERICAL_ONLY",
              "source_report_sha256": hashlib.sha256(SOURCE_REPORT.read_bytes()).hexdigest(),
              "gap_report_sha256": hashlib.sha256(GAP_REPORT.read_bytes()).hexdigest(),
              "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
              "exact_old_witness_audits": [exact_old_witness_audit(c) for c in gaps["certificates"]],
              "controls": [run_control(c, saved=saved.get(c["seed"])) for c in source["native_controls"] if c["seed"] in (93013, 93017, 93018)],
              "global_realizability_or_population_recovery_proved": False, "accepted_candidate_or_speedup": False}
    if args.write:
        REPORT.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"status": report["status"], "old_witness_negative_laws": [
        c["negative_laws_certified"] for c in report["exact_old_witness_audits"]],
        "controls": [{"seed": c["seed"], "status": c["solver"]["status"],
                       "recovery": c["calibration_recovery_NOT_decoder_input"],
                       "scores": {k: v["score"] for k, v in c["fresh_verification"].items()}}
                      for c in report["controls"]]}, indent=2))


if __name__ == "__main__":
    main()
