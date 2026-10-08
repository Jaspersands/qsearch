"""Full-root primal lattice shortlist for native covariant measurement records.

Exact public lattice arithmetic; heuristic decoding, not a Gaussian-noise
promise, a source simulator, a hardness certificate or an accepted algorithm.
"""
from __future__ import annotations

import argparse
import hashlib
from itertools import product
import json
import math
from pathlib import Path
import random
import time

from flint import fmpz_mat, nmod_mat

from native_rlwe_primal_babai import exact_row_profile
from ternary_character_synchronization import _records, lifted_inverse
from ternary_covariant_noise import heldout_gate, heldout_score, root_digits, simulated_record
from ternary_pair_lattice import nearest_plane_list

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT / "research/TERNARY_MEASURED_LATTICE_DECODER.md"
REPORT = ROOT / "research/classical_baselines/ternary_measured_lattice_decoder.json"


def integer(value, name, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return value


def paired_embed(values):
    values = tuple(values)
    if not values or len(values) % 2 or any(type(x) is not int for x in values):
        raise ValueError("nonempty exact integer pairs required")
    return tuple(x for a, c in zip(values[::2], values[1::2]) for x in (a, c, a-c))


def paired_unembed(values):
    values = tuple(values)
    if not values or len(values) % 3 or any(type(x) is not int for x in values):
        raise ValueError("nonempty exact embedded integer triples required")
    if any(a-c != d for a, c, d in zip(values[::3], values[1::3], values[2::3])):
        raise ValueError("point escaped the paired metric subspace")
    return tuple(x for a, c in zip(values[::3], values[1::3]) for x in (a, c))


def compile_code_lattice(records, max_equations=32):
    """Systematic basis of A Z^n + q Z^m, without outcome-dependent selection."""
    records, n, q = _records(records)
    integer(max_equations, "whole lattice equation cap", 1)
    m = 2*len(records)
    if m > max_equations:
        return {"status": "WHOLE_LATTICE_CAP_EXHAUSTED", "lattice_equations": m,
                "partial_lattice_compiled": False}
    A = tuple(row for r in records for row in (r.first, r.second))
    reduced, rank = nmod_mat([[row[j] % 3 for row in A] for j in range(n)], 3).rref()
    if rank != n:
        return {"status": "UNKNOWN_NO_UNIT_ROW_BASIS", "rank_mod3": int(rank),
                "partial_secret_or_hardness_claimed": False}
    pivots = tuple(next(j for j in range(m) if reduced[i, j]) for i in range(n))
    inverse = lifted_inverse(tuple(A[j] for j in pivots), q)
    inverse = tuple(tuple(int(inverse[i, j]) for j in range(n)) for i in range(n))
    other = tuple(j for j in range(m) if j not in pivots)
    coefficients = tuple(tuple(sum(A[j][l]*inverse[l][i] for l in range(n)) % q
                               for i in range(n)) for j in range(m))
    rows = []
    for i in range(n):
        rows.append(tuple((coefficients[j][i]+q//2) % q-q//2 for j in range(m)))
    for j in other:
        rows.append(tuple(q*int(k == j) for k in range(m)))
    rows = tuple(rows)
    determinant = abs(int(fmpz_mat(rows).det()))
    if determinant != q**(m-n):
        raise ArithmeticError("systematic native code lattice index failed")
    return {"status": "EXACT_PUBLIC_CODE_LATTICE", "secret_dimension": n,
            "modulus": q, "frequency_rows": A, "unit_basis_rows": pivots,
            "unit_basis_inverse": inverse, "lattice_rows": rows, "lattice_equations": m,
            "lattice_index": determinant, "basis_reads_outcomes": False,
            "Gaussian_error_promise": False}


def compile_lattice(records, max_equations=32):
    model = compile_code_lattice(records, max_equations)
    if model["status"] != "EXACT_PUBLIC_CODE_LATTICE":
        return model
    rows, m = model["lattice_rows"], model["lattice_equations"]
    embedded = tuple(paired_embed(row) for row in rows)
    profile = exact_row_profile(embedded)
    gram = 3**(m//2)*model["lattice_index"]**2
    if profile["leading_gram_determinants"][-1] != gram:
        raise ArithmeticError("correlation metric Gram determinant failed")
    return {**model, "status": "EXACT_PUBLIC_PAIRED_CODE_LATTICE", "embedded_rows": embedded,
            "ambient_metric_dimension": 3*(m//2), "embedded_gram_determinant": gram}


def point_to_secret(model, point):
    if model.get("status") != "EXACT_PUBLIC_PAIRED_CODE_LATTICE":
        raise ValueError("complete full-rank public code lattice required")
    return code_point_to_secret(model, paired_unembed(point))


def code_point_to_secret(model, point):
    if model.get("status") not in ("EXACT_PUBLIC_CODE_LATTICE", "EXACT_PUBLIC_PAIRED_CODE_LATTICE"):
        raise ValueError("complete full-rank public code lattice required")
    point = tuple(point)
    if any(type(x) is not int for x in point):
        raise ValueError("exact integer code point required")
    A, q, n = model["frequency_rows"], model["modulus"], model["secret_dimension"]
    if len(point) != len(A):
        raise ValueError("complete lattice point required")
    values = tuple(point[j] for j in model["unit_basis_rows"])
    secret = tuple(sum(a*b for a, b in zip(row, values)) % q for row in model["unit_basis_inverse"])
    if any((sum(a*s for a, s in zip(row, secret))-value) % q for row, value in zip(A, point)):
        raise ValueError("point is not in the native modular code lattice")
    if len(secret) != n:
        raise ArithmeticError("secret dimension changed")
    return secret


def reduce_basis(model, seed=0, basis_index=0):
    integer(seed, "public basis seed")
    integer(basis_index, "public basis index")
    if model.get("status") != "EXACT_PUBLIC_PAIRED_CODE_LATTICE":
        raise ValueError("complete public lattice required")
    original = fmpz_mat(model["embedded_rows"])
    m = original.nrows()
    rng, order = random.Random(seed+basis_index), list(range(m))
    if basis_index:
        rng.shuffle(order)
    P = [[0]*m for _ in range(m)]
    for i, j in enumerate(order):
        P[i][j] = rng.choice((-1, 1)) if basis_index else 1
    P = fmpz_mat(P)
    reduced, transform = (P*original).lll(transform=True, gram="exact")
    transform = transform*P
    if transform*original != reduced or abs(int(transform.det())) != 1:
        raise ArithmeticError("LLL changed the public code lattice")
    rows = tuple(tuple(int(x) for x in row) for row in reduced.tolist())
    profile = exact_row_profile(rows)
    if profile["leading_gram_determinants"][-1] != model["embedded_gram_determinant"]:
        raise ArithmeticError("LLL changed the paired metric determinant")
    return {"rows": rows, "transform": tuple(tuple(int(x) for x in row) for row in transform.tolist()), "profile": profile,
            "exact_unimodular_transform_checked": True, "basis_reads_outcomes": False}


def public_subset_schedule(count, n, seed, rounds=2, max_equations=32):
    integer(count, "available original records", 1)
    integer(n, "secret dimension", 1)
    integer(seed, "public subset seed")
    integer(rounds, "subset rounds", 1)
    integer(max_equations, "lattice equation cap", 1)
    minimum = (n+1)//2
    sizes = tuple(sorted({minimum+1, n+1, 2*n+1}))
    sizes = tuple(k for k in sizes if k <= count and 2*k <= max_equations)
    rng, schedule = random.Random(seed), []
    for round_index in range(rounds):
        order = list(range(count))
        if round_index:
            rng.shuffle(order)
        for k in sizes:
            subset = tuple(sorted(order[:k]))
            if subset not in schedule:
                schedule.append(subset)
    return tuple(schedule)


def native_loss(records, trial):
    """Stable form of (3-score)/2, avoiding cancellation near perfect fit."""
    records, _, q = _records(records)
    residuals = tuple(r.residual(trial) for r in records)
    centered = tuple((x+q//2) % q-q//2 for a, c in residuals for x in (a, c, a-c))
    if q.bit_length() <= 256:
        return math.fsum(math.sin(math.pi*x/q)**2 for x in centered)/len(records)
    import mpmath as mp
    with mp.workdps(32+(3*q.bit_length()+4)//5):
        return mp.fsum(mp.sin(mp.pi*mp.mpf(x)/q)**2 for x in centered)/len(records)


def decode(records, original_ids, seed=0, subset_rounds=2, basis_count=2,
           max_equations=32, single_repairs=True):
    """Fixed public subset menu, exact Babai repairs, native-score selection."""
    records, n, q = _records(records)
    ids = tuple(original_ids)
    if len(ids) != len(records) or len(set(ids)) != len(ids) or any(type(x) is not str or not x for x in ids):
        raise ValueError("one distinct nonempty original record ID per input required")
    integer(seed, "public attack seed")
    integer(basis_count, "basis count", 1)
    if type(single_repairs) is not bool:
        raise ValueError("explicit single-repair mode required")
    schedule = public_subset_schedule(len(records), n, seed, subset_rounds, max_equations)
    costs = {"original_measured_qutrits": len(records), "LLL_calls": 0,
             "nearest_plane_paths": 0, "exact_rounding_steps": 0,
             "training_score_evaluations": 0, "distinct_source_IDs_prove_IID": False,
             "classical_record_reuse_is_charged_once": True,
             "root_value_or_secret_grid_enumeration": False, "LLL_time_deadline": False}
    cases, proposals, losses = [], {}, {}
    for subset in schedule:
        selected = tuple(records[j] for j in subset)
        model = compile_lattice(selected, max_equations)
        case = {"subset": subset, "source_IDs": tuple(ids[j] for j in subset),
                "model": model, "reductions": [], "attempts": []}
        cases.append(case)
        if model["status"] != "EXACT_PUBLIC_PAIRED_CODE_LATTICE":
            continue
        target = paired_embed(tuple(x for r in selected for x in r.outcome))
        for basis_index in range(basis_count):
            reduced = reduce_basis(model, seed+37*len(cases), basis_index)
            costs["LLL_calls"] += 1
            case["reductions"].append({"rows": reduced["rows"], "transform": reduced["transform"]})
            for witness in nearest_plane_list(reduced["rows"], target, reduced["profile"]):
                costs["nearest_plane_paths"] += 1
                costs["exact_rounding_steps"] += model["lattice_equations"]
                secret = point_to_secret(model, witness["point"])
                distance = sum((a-b)**2 for a, b in zip(target, witness["point"]))
                case["attempts"].append({**witness, "basis_index": basis_index,
                                         "candidate": secret, "paired_distance_squared": distance})
                if secret not in proposals:
                    proposals[secret] = heldout_score(records, secret)
                    losses[secret] = native_loss(records, secret)
                    costs["training_score_evaluations"] += 1
                if not single_repairs:
                    break
    candidate = min(sorted(proposals), key=lambda s: losses[s]) if proposals else None
    return {"status": "NATIVE_SCORE_SELECTED_LATTICE_PROPOSAL" if candidate is not None
            else "NO_PROPOSAL_FROM_PUBLIC_LATTICE_MENU", "candidate": candidate,
            "training_score": proposals.get(candidate), "proposals": tuple(sorted(proposals)),
            "proposal_scores": tuple({"candidate": s, "score": proposals[s],
                                      "selection_loss": str(losses[s])} for s in sorted(proposals)),
            "subset_schedule": schedule, "cost": costs, "cases": cases,
            "training_secret_or_heldout_used": False, "asymptotic_recovery_proved": False,
            "native_score_selected_via_stable_equivalent_sine_loss": True,
            "score_ordering_has_certified_interval_precision": False,
            "failure_proves_classical_hardness": False, "native_quantum_source_simulated": False,
            "accepted_speedup_candidate": False}


def verify_fresh(records, candidate, original_ids, training_ids):
    records, n, q = _records(records)
    ids, old = tuple(original_ids), tuple(training_ids)
    if len(ids) != len(records) or len(set(ids)) != len(ids) or any(type(x) is not str or not x for x in ids):
        raise ValueError("distinct fresh original record IDs required")
    if set(ids) & set(old):
        raise ValueError("held-out originals must be disjoint from training")
    if candidate is None:
        return {"status": "NO_CANDIDATE_TO_VERIFY", "threshold_passed": False}
    if len(candidate) != n or any(type(x) is not int or not 0 <= x < q for x in candidate):
        raise ValueError("canonical full-root candidate required")
    score = heldout_score(records, candidate)
    return {"status": "FRESH_NATIVE_VERIFICATION", "score": score,
            "threshold_passed": score >= .5, "gate": heldout_gate(len(records), 1),
            "candidate_fixed_before_fresh_records": True, "physical_IID_from_IDs_proved": False}


def metric_countercontrol(q=9):
    """The true torus metric is not the exact periodic native score."""
    root_digits(q)
    if q > 27:
        raise ValueError("complete metric countercontrol capped at modulus27")
    entries = []
    for a, c in product(range(q), repeat=2):
        distance = min(sum(x*x for x in paired_embed((a+q*i, c+q*j)))
                       for i, j in product((-1, 0), repeat=2))
        score = math.cos(2*math.pi*a/q)+math.cos(2*math.pi*c/q)+math.cos(2*math.pi*(a-c)/q)
        entries.append({"residual": (a, c), "torus_paired_distance_squared": distance,
                        "native_score": score})
    witness = next(((a, b) for a in entries for b in entries
                    if a["torus_paired_distance_squared"] < b["torus_paired_distance_squared"]
                    and a["native_score"] < b["native_score"]-1e-9), None)
    if witness is None:
        raise ArithmeticError("countercontrol did not separate surrogate and native metric")
    return {"modulus": q, "closer_but_worse": witness[0], "farther_but_better": witness[1],
            "Euclidean_CVP_equals_native_likelihood_maximization": False,
            "complete_one_pair_residuals_checked": q*q}


def calibration(n, digits, seed, training_count=96, heldout_count=512):
    integer(n, "calibration dimension", 1)
    integer(digits, "root digits", 1)
    integer(seed, "calibration seed")
    q, rng = 3**digits, random.Random(seed)
    secret = tuple(rng.randrange(q) for _ in range(n))
    def sample(count):
        output, proposals = [], 0
        for _ in range(count):
            first, second = (tuple(rng.randrange(q) for _ in range(n)) for _ in range(2))
            record, attempts = simulated_record(first, second, secret, q, rng)
            output.append(record)
            proposals += attempts
        return tuple(output), proposals
    training, training_proposals = sample(training_count)
    ids = tuple(f"measured-lattice-{seed}-train-{j}" for j in range(training_count))
    started = time.monotonic()
    result = decode(training, ids, seed+1000)
    wall = time.monotonic()-started
    # Selection is complete before the held-out batch exists.
    fresh, fresh_proposals = sample(heldout_count)
    fresh_ids = tuple(f"measured-lattice-{seed}-fresh-{j}" for j in range(heldout_count))
    verification = verify_fresh(fresh, result["candidate"], fresh_ids, ids)
    return {"n": n, "root_digits": digits, "modulus": q, "seed": seed,
            "calibration_secret": secret, "training_records": tuple(r.public() for r in training),
            "training_IDs": ids, "heldout_records": tuple(r.public() for r in fresh),
            "heldout_IDs": fresh_ids, "decoder": result, "verification": verification,
            "calibration_recovered": result["candidate"] == secret,
            "true_training_score_diagnostic": heldout_score(training, secret),
            "true_heldout_score_diagnostic": heldout_score(fresh, secret),
            "training_plus_fresh_original_qutrits": training_count+heldout_count,
            "offline_noise_sampler_proposals": training_proposals+fresh_proposals,
            "decode_wall_seconds_includes_LLL": wall,
            "records_are_native_law_simulation_not_unknown_source_supply": True,
            "bounded_success_is_asymptotic_recovery": False}


def build_report():
    controls = [calibration(n, r, 95200+100*n+10*r+k)
                for n, r in ((2, 2), (2, 8), (4, 2), (4, 8), (8, 2), (8, 8))
                for k in range(2)]
    return {"status": "FULL_ROOT_PAIRED_LATTICE_BASELINE_REVIEW_PENDING",
            "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "controls": controls, "metric_countercontrol": metric_countercontrol(),
            "control_count": len(controls),
            "recoveries": sum(c["calibration_recovered"] for c in controls),
            "fresh_threshold_passes": sum(c["verification"]["threshold_passed"] for c in controls),
            "population_or_asymptotic_recovery_theorem": False,
            "classical_simulation_of_original_quantum_inputs": False,
            "failure_implies_classical_hardness": False, "accepted_speedup_candidate": False}


def exact_json(value):
    """Keep large certificate integers exact for independent JSON consumers."""
    if type(value) is int and abs(value) > 2**53-1:
        return str(value)
    if isinstance(value, dict):
        return {k: exact_json(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [exact_json(v) for v in value]
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(report), indent=2)+"\n")
    print(json.dumps({key: report[key] for key in ("status", "control_count", "recoveries",
                                                  "fresh_threshold_passes")}, indent=2))


if __name__ == "__main__":
    main()
