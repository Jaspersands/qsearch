"""Full-record Euclidean native decoder with exact public lattice proposals.

No BDD/Gaussian promise, near-exact CVP guarantee or quantum speedup supplied.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import random
import time

from flint import fmpq, fmpz_mat

from ternary_character_synchronization import _records
from ternary_covariant_noise import CovariantRecord, heldout_gate, heldout_score, simulated_record
from ternary_measured_lattice_decoder import (
    code_point_to_secret, compile_code_lattice, exact_json, integer, native_loss,
)
from ternary_native_cvp_reduction import squared_residual_cost

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT / "research/TERNARY_FULL_RECORD_CVP.md"
REPORT = ROOT / "research/classical_baselines/ternary_full_record_cvp.json"


def sparse_rows(rows):
    return tuple(tuple((j, x) for j, x in enumerate(row) if x) for row in rows)


def exact_sparse_profile(rows):
    """Exact LDL of the Gram matrix, exploiting zero support without dropping it."""
    rows = tuple(tuple(row) for row in rows)
    if not rows:
        raise ValueError("nonempty exact basis required")
    m, width = len(rows), len(rows[0])
    if not m or width < m or any(len(row) != width for row in rows):
        raise ValueError("whole full-row-rank rectangular basis required")
    columns = [[] for _ in range(width)]
    for i, row in enumerate(rows):
        for j, x in enumerate(row):
            if x:
                columns[j].append((i, x))
    gram = [dict() for _ in rows]
    for column in columns:
        for i, x in column:
            for j, y in column:
                if j <= i:
                    gram[i][j] = gram[i].get(j, 0)+x*y
    mu, gs = [], []
    determinant = fmpq(1)
    for i in range(m):
        current = {}
        for j in range(i):
            value = fmpq(gram[i].get(j, 0))
            for k in current.keys() & mu[j].keys():
                value -= current[k]*mu[j][k]*gs[k]
            if value:
                current[j] = value/gs[j]
        norm = fmpq(gram[i].get(i, 0))-sum((x*x*gs[j] for j, x in current.items()), fmpq(0))
        if norm <= 0:
            raise ValueError("singular exact public basis")
        mu.append(current)
        gs.append(norm)
        determinant *= norm
    if determinant.denominator != 1:
        raise ArithmeticError("integer Gram determinant lost")
    return {"mu": mu, "gs_squared": gs, "gram_determinant": int(determinant.numerator)}


def public_repairs(rank, count, seed, positions=None):
    integer(rank, "basis rank", 1)
    integer(count, "public repair paths")
    integer(seed, "public repair seed")
    positions = tuple(range(rank)) if positions is None else tuple(positions)
    if not positions or len(set(positions)) != len(positions) or any(type(j) is not int or not 0 <= j < rank for j in positions):
        raise ValueError("nonempty distinct public repair positions required")
    rng, paths = random.Random(seed), [(0,)*rank]
    for i in range(count):
        row = [0]*rank
        for j in rng.sample(positions, min(len(positions), 1+i % 4)):
            row[j] = rng.choice((-1, 1))
        paths.append(tuple(row))
    return tuple(paths)


def rounding_influence(model, rows, profile=None):
    """Exact secret-class influence DAG, not just per-row q-axis removal."""
    profile = exact_sparse_profile(rows) if profile is None else profile
    secrets = tuple(code_point_to_secret(model, row) for row in rows)
    live, parents = [], []
    for i, secret in enumerate(secrets):
        parent = next((j for j in sorted(profile["mu"][i]) if live[j]), None)
        live.append(any(secret) or parent is not None)
        parents.append(parent)
    return {"row_code_secrets": secrets,
            "influential_rounding_positions": tuple(i for i, x in enumerate(live) if x),
            "dead_rounding_positions": tuple(i for i, x in enumerate(live) if not x),
            "earlier_influential_parent": tuple(parents),
            "any_dead_only_repair_preserves_secret_for_every_target": True,
            "zero_mod_q_rows_can_be_discarded_without_GS_dependencies": False,
            "influence_claims_recovery_or_approximation_guarantee": False}


def exact_repair_paths(rows, target, offsets, profile=None):
    rows, target = tuple(rows), tuple(target)
    profile = exact_sparse_profile(rows) if profile is None else profile
    m, mu, gs = len(rows), profile["mu"], profile["gs_squared"]
    if len(target) != len(rows[0]):
        raise ValueError("complete target required")
    inner = []
    for i, row in enumerate(rows):
        value = fmpq(sum(a*b for a, b in zip(row, target)))
        value -= sum((x*inner[j] for j, x in mu[i].items()), fmpq(0))
        inner.append(value)
    initial = tuple(x/y for x, y in zip(inner, gs))
    for repair in offsets:
        if len(repair) != m or any(type(x) is not int or x not in (-1, 0, 1) for x in repair):
            raise ValueError("complete public signed repair vector required")
        coordinates, coefficients = list(initial), [0]*m
        for i in range(m-1, -1, -1):
            value = coordinates[i]
            coefficients[i] = (2*int(value.numerator)+int(value.denominator))//(2*int(value.denominator))+repair[i]
            if coefficients[i]:
                for j, x in mu[i].items():
                    coordinates[j] -= coefficients[i]*x
        point = tuple(sum(a*row[j] for a, row in zip(coefficients, rows) if a) for j in range(len(target)))
        yield {"public_repair": repair, "coefficients": tuple(coefficients), "point": point}


def compact_model(model):
    if model["status"] != "EXACT_PUBLIC_CODE_LATTICE":
        return model
    n, m = model["secret_dimension"], model["lattice_equations"]
    return {k: v for k, v in model.items() if k != "lattice_rows"} | {
        "code_generator_rows": model["lattice_rows"][:n],
        "nonpivot_axis_indices": tuple(j for j in range(m) if j not in model["unit_basis_rows"])}


def embedding_proposals(model, target, scale):
    integer(scale, "positive embedding scale", 1)
    original = tuple(tuple(row)+(0,) for row in model["lattice_rows"])+(tuple(target)+(scale,),)
    reduced, transform = fmpz_mat(original).lll(transform=True, gram="exact")
    if transform*fmpz_mat(original) != reduced or abs(int(transform.det())) != 1:
        raise ArithmeticError("embedding reduction changed the integer lattice")
    rows = tuple(tuple(map(int, row)) for row in reduced.tolist())
    q, rejected, candidates = model["modulus"], [], []
    for i, row in enumerate(rows):
        if row[-1] % scale:
            raise ArithmeticError("embedding coefficient is not integral")
        coefficient = row[-1]//scale
        if math.gcd(coefficient, q) != 1:
            rejected.append({"row": i, "coefficient": coefficient,
                             "reason": "NONUNIT_TARGET_COEFFICIENT"})
            continue
        lattice_point = tuple(x-coefficient*y for x, y in zip(row[:-1], target))
        base_secret = code_point_to_secret(model, lattice_point)
        candidate = tuple(-pow(coefficient, -1, q)*s % q for s in base_secret)
        candidates.append({"row": i, "target_coefficient": coefficient,
                           "code_lattice_point": lattice_point, "candidate": candidate,
                           "literal_CVP_error_vector": abs(coefficient) == 1})
    return {"scale": scale, "rows_sparse": sparse_rows(rows),
            "transform_sparse": sparse_rows(tuple(tuple(map(int, row)) for row in transform.tolist())),
            "candidates": candidates, "rejected_rows": rejected,
            "unit_coefficients_beyond_plus_minus_one_are_modular_trials_only": True,
            "bounded_distance_promise_or_near_exact_factor_proved": False}


def bdd_gate(records):
    records, _, q = _records(records)
    M = len(records)
    delta = max(Fraction(0), Fraction(4, 81)-Fraction(1, 4*M))
    exponent = 8*M*delta**2
    return {"shortest_lattice_vector_length_upper": q,
            "true_secret_BDD_squared_distance_necessary_upper": str(Fraction(q*q, 4)),
            "true_normalized_pair_cost_mean_lower": "4/81",
            "Hoeffding_lower_tail_exponent": str(exponent),
            "BDD_promise_probability_upper_diagnostic": math.exp(-float(exponent)),
            "Gaussian_or_BDD_source_promise_granted": False,
            "general_CVP_or_quantum_receiver_impossibility": False}


def decode(records, original_ids, repair_count=32, seed=0, max_equations=1024, embeddings=True):
    records, n, q = _records(records)
    integer(repair_count, "public repair count")
    integer(seed, "public decoder seed")
    if type(embeddings) is not bool:
        raise ValueError("explicit embedding mode required")
    ids = tuple(original_ids)
    if len(ids) != len(records) or len(set(ids)) != len(ids) or any(type(x) is not str or not x for x in ids):
        raise ValueError("one distinct original source ID per measured record required")
    model = compile_code_lattice(records, max_equations)
    if model["status"] != "EXACT_PUBLIC_CODE_LATTICE":
        return {"status": model["status"], "model": model, "partial_cohort_or_decoder_used": False,
                "selections": {}, "near_exact_CVP_guarantee": False}
    original = fmpz_mat(model["lattice_rows"])
    reduced, transform = original.lll(transform=True, gram="exact")
    if transform*original != reduced or abs(int(transform.det())) != 1:
        raise ArithmeticError("full cohort LLL changed lattice")
    rows = tuple(tuple(map(int, row)) for row in reduced.tolist())
    profile = exact_sparse_profile(rows)
    if profile["gram_determinant"] != model["lattice_index"]**2:
        raise ArithmeticError("full Euclidean Gram determinant failed")
    influence = rounding_influence(model, rows, profile)
    target = tuple(x for r in records for x in r.outcome)
    proposals, paths = {}, []
    def add(candidate):
        if candidate not in proposals:
            proposals[candidate] = {"candidate": candidate,
                                   "Euclidean_cost": squared_residual_cost(records, candidate),
                                   "native_loss": native_loss(records, candidate),
                                   "native_score": heldout_score(records, candidate)}
    offsets = public_repairs(len(rows), repair_count, seed)
    for path in exact_repair_paths(rows, target, offsets, profile):
        candidate = code_point_to_secret(model, path["point"])
        distance = sum((a-b)**2 for a, b in zip(target, path["point"]))
        paths.append({**path, "candidate": candidate, "supplied_Euclidean_cost": distance})
        add(candidate)
    embedding_runs = []
    if embeddings:
        for scale in sorted({max(1, q//4), max(1, q//2)}):
            run = embedding_proposals(model, target, scale)
            embedding_runs.append(run)
            for item in run["candidates"]:
                add(item["candidate"])
    candidates = sorted(proposals)
    selections = {"Euclidean": min(candidates, key=lambda s: proposals[s]["Euclidean_cost"]),
                  "native_likelihood": min(candidates, key=lambda s: proposals[s]["native_loss"])}
    public_scores = tuple({**proposals[s], "native_loss": str(proposals[s]["native_loss"])} for s in candidates)
    return {"status": "FULL_COHORT_LATTICE_PROPOSALS_ONLY", "model": compact_model(model),
            "source_IDs": ids, "reduced_rows_sparse": sparse_rows(rows),
            "transform_sparse": sparse_rows(tuple(tuple(map(int, row)) for row in transform.tolist())),
            "repair_paths": paths, "embedding_runs": embedding_runs,
            "proposal_scores": public_scores, "selections": selections,
            "cost": {"original_measured_qutrits": len(records), "LLL_calls": 1+len(embedding_runs),
                     "lattice_dimension": len(rows), "exact_repair_paths": len(paths),
                     "exact_rounding_steps": len(paths)*len(rows), "distinct_candidates_scored": len(candidates),
                     "secret_or_root_value_enumeration": False},
            "BDD_gate": bdd_gate(records), "all_original_records_in_optimization": True,
            "rounding_influence_certificate": influence,
            "matrix_selected_using_hidden_secret": False, "Gaussian_error_promise": False,
            "near_exact_CVP_guarantee": False, "failure_proves_hardness": False,
            "accepted_speedup_candidate": False}


def calibration(n, digits, density, seed):
    integer(n, "secret dimension", 1)
    integer(digits, "root digits", 1)
    integer(density, "original-copy density", 1)
    integer(seed, "calibration seed")
    q, M, rng = 3**digits, density*n*digits, random.Random(seed)
    secret = tuple(rng.randrange(q) for _ in range(n))
    def sample(count):
        output = []
        for _ in range(count):
            a, c = (tuple(rng.randrange(q) for _ in range(n)) for _ in range(2))
            output.append(simulated_record(a, c, secret, q, rng)[0])
        return tuple(output)
    training = sample(M)
    ids = tuple(f"full-cvp-{seed}-train-{j}" for j in range(M))
    started = time.monotonic()
    result = decode(training, ids, seed=seed+1000)
    elapsed = time.monotonic()-started
    # Both selections are frozen before the independent simulated batch.
    fresh = sample(512)
    trials = set(result["selections"].values())
    gate = heldout_gate(len(fresh), len(trials)) if trials else None
    verification = {name: {"candidate": candidate, "fresh_score": heldout_score(fresh, candidate),
                           "threshold_passed": heldout_score(fresh, candidate) >= .5,
                           "calibration_recovered": candidate == secret}
                    for name, candidate in result["selections"].items()}
    true_cost = squared_residual_cost(training, secret)
    control = {"n": n, "root_digits": digits, "density_per_n_r": density, "seed": seed,
            "modulus": q, "calibration_secret": secret,
            "training_records": tuple(r.public() for r in training),
            "heldout_records": tuple(r.public() for r in fresh),
            "heldout_source_IDs": tuple(f"full-cvp-{seed}-fresh-{j}" for j in range(512)),
            "decoder": result, "verification": verification, "joint_fixed_candidate_gate": gate,
            "true_Euclidean_cost_diagnostic": true_cost,
            "true_cost_within_q_over_two_BDD_radius": 4*true_cost <= q*q,
            "meets_conservative_CVP_population_copy_budget": M >= 2048*(2*n*digits+17),
            "true_fresh_score_diagnostic": heldout_score(fresh, secret),
            "original_training_plus_fresh_qutrits": M+512,
            "decoder_wall_seconds_including_LLL": elapsed,
            "native_law_simulation_supplies_unknown_quantum_states": False,
            "bounded_trials_are_population_theorem": False}
    return attach_comparison_certificate(control)


def attach_comparison_certificate(control):
    """Public valid-point witness; calibration truth never reaches the optimizer."""
    records = tuple(CovariantRecord(**r) for r in control["training_records"])
    secret, q = tuple(control["calibration_secret"]), control["modulus"]
    point = tuple(y-((e+q//2) % q-q//2)
                  for r in records for y, e in zip(r.outcome, r.residual(secret)))
    if any((sum(a*s for a, s in zip(row, secret))-x) % q
           for row, x in zip((row for r in records for row in (r.first, r.second)), point)):
        raise ArithmeticError("comparison witness is not in the actual code lattice")
    cost = sum((y-x)**2 for y, x in zip((y for r in records for y in r.outcome), point))
    best = min(int(p["Euclidean_cost"]) for p in control["decoder"]["proposal_scores"])
    margin = 64*best-81*cost
    control["CVP_comparison_certificate"] = {
        "public_valid_lattice_point": point, "public_point_secret": secret,
        "valid_point_squared_distance": cost, "best_all_generated_candidates_squared_distance": best,
        "strict_integer_factor_failure_margin": margin,
        "norm_9_over_8_approximation_falsified_on_this_instance": margin > 0,
        "globally_nearest_point_or_true_secret_optimality_assumed": False,
        "comparison_truth_supplied_to_decoder": False,
        "comparison_witness_is_posthoc_not_population_hardness": True}
    decoder = control["decoder"]
    if "rounding_influence_certificate" not in decoder:
        width = decoder["model"]["lattice_equations"]
        rows = []
        for entries in decoder["reduced_rows_sparse"]:
            row = [0]*width
            for j, x in entries:
                row[j] = int(x)
            rows.append(tuple(row))
        decoder["rounding_influence_certificate"] = rounding_influence(decoder["model"], tuple(rows))
    return control


def build_report():
    controls = []
    for n, r in ((2, 2), (2, 8), (4, 8), (8, 8)):
        for density in (4, 8):
            seed = 97200+100*n+10*r+density
            control = calibration(n, r, density, seed)
            controls.append(control)
            print(json.dumps({"n": n, "r": r, "density": density,
                              "recoveries": {k: v["calibration_recovered"] for k, v in control["verification"].items()},
                              "seconds": round(control["decoder_wall_seconds_including_LLL"], 3)}), flush=True)
    return {"status": "FULL_RECORD_NATIVE_CVP_ATTEMPT_REVIEW_PENDING",
            "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "controls": controls, "near_exact_CVP_solver_implemented": False,
            "classical_source_dequantization_or_hardness_proved": False,
            "accepted_speedup_candidate": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--replay-saved", action="store_true",
                        help="Add exact comparison witnesses to saved optimizer outputs; no new optimizer or source run")
    args = parser.parse_args()
    if args.replay_saved:
        report = json.loads(REPORT.read_text())
        if report["status"] != "FULL_RECORD_NATIVE_CVP_ATTEMPT_REVIEW_PENDING":
            raise ValueError("actual saved full-record optimizer report required")
        for control in report["controls"]:
            attach_comparison_certificate(control)
        report["derivation_sha256"] = hashlib.sha256(DERIVATION.read_bytes()).hexdigest()
        report["comparison_replay_is_new_source_or_LLL_run"] = False
    else:
        report = build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(report), indent=2)+"\n")
    print(json.dumps({"status": report["status"], "controls": len(report["controls"]),
                      "exact_9_over_8_counterexamples": sum(c["CVP_comparison_certificate"]["norm_9_over_8_approximation_falsified_on_this_instance"] for c in report["controls"]),
                      "near_exact_CVP_solver_implemented": False}, indent=2))


if __name__ == "__main__":
    main()
