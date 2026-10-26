"""Full-target feedback, multilevel beam search, J16 scaling, and 924-bit cosine attacks.

This is a bounded classical heuristic and scaling audit, not exact CVP or an
asymptotic dequantization theorem. Every proposal is checked on the complete target.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
import hashlib
import json
import math
from pathlib import Path
import random
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from flint import fmpz_mat

from theorems import integer_character_babai as babai
from theorems import integer_character_interpolation as integer
from theorems import integer_character_near_vector as near
from theorems import integer_character_readset as readset
from theorems import integer_character_uniform as uniform

REPORT = ROOT / "research/classical_baselines/integer_character_feedback.json"


def complete_tail(rows, order, target, exact, incumbent, plane, offset):
    """Freeze higher core coefficients, branch once, complete every lower row."""
    prefix = exact["rounding_profile"]["prefix"]
    upper = exact["rounding_profile"]["upper_rows"]
    pivots = exact["normalized_gram_pivots"]
    rank, m = len(prefix), len(rows)
    d = m-rank
    if (type(plane) is not int or not 0 <= plane < d or type(offset) is not int
            or len(incumbent) != m or any(type(c) is not int for c in incumbent)):
        raise ValueError("valid core plane, integer offset and complete integer incumbent required")
    coefficients = [0]*m
    for k in range(d-1, -1, -1):
        if k > plane:
            coefficients[rank+k] = incumbent[rank+k]
            continue
        numerator = upper[k][d]-order*sum(
            coefficients[rank+i]*upper[k][i] for i in range(k+1, d))
        denominator = order*pivots[rank+k]
        coefficients[rank+k] = (2*numerator+denominator)//(2*denominator)
        if k == plane:
            coefficients[rank+k] += offset
    for i, (j, sign) in enumerate(prefix):
        residual = target[j]-sum(coefficients[k]*rows[k][j] for k in range(rank, m))
        coefficients[i] = (2*sign*residual+order)//(2*order)
    return coefficients


def evaluate(rows, labels, order, target, coefficients):
    if len(coefficients) != len(rows) or any(type(c) is not int for c in coefficients):
        raise ValueError("one exact integer coefficient per basis row required")
    point = [sum(c*row[j] for c, row in zip(coefficients, rows)) for j in range(len(labels))]
    assignment = near.recover_assignment(labels, order, point)
    witness = near.witness(labels, target, order, assignment)
    raw_square = Q(sum((a-b)**2 for a, b in zip(target, point)), len(labels)*order*order)
    if witness["mean_square"] > raw_square:
        raise ArithmeticError("coordinate centering increased distance")
    return {
        "coefficients": coefficients, "point": point,
        "canonical_point": witness["numerator"], "assignment": assignment,
        "mean_square": witness["mean_square"], "raw_mean_square": raw_square,
        "threshold_met": witness["accepted"],
    }


def feedback_search(rows, labels, order, target, exact, incumbent, planes, *, radius=4, progress=None):
    if (type(radius) is not int or radius < 0
            or any(type(i) is not int or not 0 <= i < exact["exact_core_dimension"] for i in planes)):
        raise ValueError("nonnegative radius and valid core-plane schedule required")
    best = evaluate(rows, labels, order, target, list(incumbent))
    initial_mean, initial_assignment = best["mean_square"], best["assignment"]
    offsets = [0]+[sign*k for k in range(1, radius+1) for sign in (1, -1)]
    trials, history = [], []
    for step, plane in enumerate(planes):
        parent = best
        selected_offset = None
        for offset in offsets:
            coefficients = complete_tail(rows, order, target, exact, parent["coefficients"], plane, offset)
            proposal = evaluate(rows, labels, order, target, coefficients)
            trials.append({
                "step": step, "core_plane": plane, "offset": offset,
                "parent_assignment_decimal": str(parent["assignment"]),
                "assignment_decimal": str(proposal["assignment"]),
                "mean_square": str(proposal["mean_square"]),
                "threshold_met": proposal["threshold_met"],
            })
            if proposal["mean_square"] < best["mean_square"]:
                best, selected_offset = proposal, offset
        if best["mean_square"] > parent["mean_square"]:
            raise ArithmeticError("feedback search lost its incumbent")
        history.append({
            "step": step, "core_plane": plane, "selected_offset": selected_offset,
            "before_mean_square": str(parent["mean_square"]),
            "after_mean_square": str(best["mean_square"]),
            "selected_assignment_decimal": str(best["assignment"]),
        })
        if progress:
            progress({"phase": "full_target_feedback", "step": step+1, "of": len(planes),
                      "mean_square": float(best["mean_square"])})
    return {
        "method": "greedy_full_target_feedback_with_exact_nearest_plane_completion",
        "radius": radius, "core_plane_schedule": list(planes),
        "initial_assignment_decimal": str(initial_assignment),
        "initial_mean_square": str(initial_mean),
        "proposal_count": len(trials), "score_evaluations_including_initial": len(trials)+1,
        "unique_proposed_assignments": len({t["assignment_decimal"] for t in trials}),
        "trials": trials, "history": history,
        "best": {
            "assignment_decimal": str(best["assignment"]),
            "mean_square": str(best["mean_square"]),
            "raw_mean_square": str(best["raw_mean_square"]),
            "basis_coefficients_decimal": list(map(str, best["coefficients"])),
            "basis_point_decimal": list(map(str, best["point"])),
            "canonical_point_decimal": list(map(str, best["canonical_point"])),
            "threshold_met": best["threshold_met"],
        },
        "candidate_generation_uses_full_target_feedback": True,
        "visited_candidates_are_not_a_target_blind_pool": True,
        "global_optimum_or_convergence_claimed": False,
        "asymptotic_dequantization_claimed": False,
    }


def multilevel_beam_search(rows, labels, order, target, exact, seed_coefficients_list,
                           planes, *, beam_width=4, radius=2, progress=None):
    """Non-greedy width-B beam search across multiple core planes."""
    if (type(beam_width) is not int or beam_width < 1
            or type(radius) is not int or radius < 0
            or not seed_coefficients_list
            or any(type(i) is not int or not 0 <= i < exact["exact_core_dimension"] for i in planes)):
        raise ValueError("positive beam_width, nonnegative radius, nonempty seeds, and valid planes required")
    evaluated_seeds = [evaluate(rows, labels, order, target, list(coeffs))
                       for coeffs in seed_coefficients_list]
    by_assignment = {}
    for item in evaluated_seeds:
        existing = by_assignment.get(item["assignment"])
        if existing is None or item["mean_square"] < existing["mean_square"]:
            by_assignment[item["assignment"]] = item
    beam = sorted(by_assignment.values(), key=lambda item: (item["mean_square"], item["assignment"]))[:beam_width]
    initial_best = beam[0]
    offsets = [0] + [sign*k for k in range(1, radius+1) for sign in (1, -1)]
    trials, level_history = [], []
    for step, plane in enumerate(planes):
        before_best = beam[0]["mean_square"]
        candidates = {item["assignment"]: item for item in beam}
        for rank_idx, parent in enumerate(beam):
            for offset in offsets:
                coeffs = complete_tail(rows, order, target, exact, parent["coefficients"], plane, offset)
                prop = evaluate(rows, labels, order, target, coeffs)
                trials.append({
                    "step": step,
                    "core_plane": plane,
                    "parent_beam_rank": rank_idx,
                    "offset": offset,
                    "parent_assignment_decimal": str(parent["assignment"]),
                    "assignment_decimal": str(prop["assignment"]),
                    "mean_square": str(prop["mean_square"]),
                    "threshold_met": prop["threshold_met"],
                })
                prev = candidates.get(prop["assignment"])
                if prev is None or prop["mean_square"] < prev["mean_square"]:
                    candidates[prop["assignment"]] = prop
        beam = sorted(candidates.values(), key=lambda item: (item["mean_square"], item["assignment"]))[:beam_width]
        if beam[0]["mean_square"] > before_best:
            raise ArithmeticError("multilevel beam search lost its incumbent")
        level_history.append({
            "step": step,
            "core_plane": plane,
            "before_best_mean_square": str(before_best),
            "after_best_mean_square": str(beam[0]["mean_square"]),
            "beam_assignments_decimal": [str(item["assignment"]) for item in beam],
            "beam_mean_squares": [str(item["mean_square"]) for item in beam],
        })
        if progress:
            progress({"phase": "multilevel_beam_search", "step": step+1, "of": len(planes),
                      "best_mean_square": float(beam[0]["mean_square"])})
    best = beam[0]
    return {
        "method": "non_greedy_multilevel_beam_search_with_exact_nearest_plane_completion",
        "beam_width": beam_width,
        "radius": radius,
        "core_plane_schedule": list(planes),
        "seed_count": len(seed_coefficients_list),
        "initial_best_assignment_decimal": str(initial_best["assignment"]),
        "initial_best_mean_square": str(initial_best["mean_square"]),
        "proposal_count": len(trials),
        "score_evaluations_including_seeds": len(trials) + len(seed_coefficients_list),
        "unique_proposed_assignments": len({t["assignment_decimal"] for t in trials}),
        "distinct_threshold_witnesses_found": len(
            {t["assignment_decimal"] for t in trials if t["threshold_met"]}
            | {str(s["assignment"]) for s in evaluated_seeds if s["threshold_met"]}
        ),
        "improved_over_initial_seed": best["mean_square"] < initial_best["mean_square"],
        "level_history": level_history,
        "trials": trials,
        "best": {
            "assignment_decimal": str(best["assignment"]),
            "mean_square": str(best["mean_square"]),
            "raw_mean_square": str(best["raw_mean_square"]),
            "basis_coefficients_decimal": list(map(str, best["coefficients"])),
            "threshold_met": best["threshold_met"],
        },
        "candidate_generation_uses_full_target_feedback": True,
        "visited_candidates_are_not_a_target_blind_pool": True,
        "global_optimum_or_convergence_claimed": False,
        "asymptotic_dequantization_claimed": False,
    }


def extract_prefix_and_readset(rows, labels, order):
    """Identify the leading +/-N coordinate prefix (blind set) and Schur core (read set)."""
    blind, prefix_open = [], True
    for row in rows:
        near.recover_assignment(labels, order, row)
        support = [j for j, v in enumerate(row) if v]
        if prefix_open and len(support) == 1 and abs(row[support[0]]) == order:
            if support[0] in blind:
                raise ValueError("coordinate prefix is singular")
            blind.append(support[0])
        else:
            prefix_open = False
    read_indices = [i for i in range(len(labels)) if i not in blind]
    return blind, read_indices


def multi_length_j16_campaign(lengths=(32, 64, 96, 128), seeds_per_length=2):
    """Predeclared multi-length / multi-center J16 classical campaign with finite quantum certificates."""
    if any(type(m) is not int or m < 16 for m in lengths) or type(seeds_per_length) is not int or seeds_per_length < 1:
        raise ValueError("lengths >= 16 and positive seeds_per_length required")
    moment = 16
    length_records = []
    for m in lengths:
        cap = max(1, (7 * m) // 200)
        t0 = time.perf_counter()
        public = near.construct(integer.prime_support(m), cap, moment=moment)
        integer.validate_public_labels(public["primes"], public["labels"], public["exponent"])
        label_seconds = time.perf_counter() - t0
        labels, order = public["labels"], public["order"]
        first, second = near.source_moments(m, cap)
        finite_q_cert = near.distance_bound(first, second, moment)

        t_lll = time.perf_counter()
        _, basis = near.lattice_bases(labels, order)
        reduced = fmpz_mat(basis).lll(delta=0.99, eta=0.51)
        rows = [[int(v) for v in row] for row in reduced.tolist()]
        lll_seconds = time.perf_counter() - t_lll
        blind_indices, read_indices = extract_prefix_and_readset(rows, labels, order)

        center_runs = []
        for s_idx in range(1, seeds_per_length + 1):
            center_seed = 2026102000 + 100 * m + s_idx
            rng = random.Random(center_seed)
            centers = [rng.randrange(order) for _ in range(m)]
            t_run = time.perf_counter()
            zero_w = near.witness(labels, centers, order, 0)
            exact = babai.exact_normalized_babai(rows, labels, order, centers)
            babai_w = near.witness(labels, centers, order, exact["assignment"])
            branch = babai.bounded_last_plane_search(rows, labels, order, centers, exact, radius=16)

            d = exact["exact_core_dimension"]
            greedy_planes = list(range(d-2, max(-1, d-6), -1))
            best_branch_offset = int(branch["best"]["offset"])
            seed_coeffs, _ = babai._round_profile(
                rows, order, centers, exact["normalized_gram_pivots"],
                exact["rounding_profile"]["upper_rows"], exact["rounding_profile"]["prefix"],
                best_branch_offset,
            )
            greedy = feedback_search(rows, labels, order, centers, exact, seed_coeffs,
                                     greedy_planes, radius=2)

            sorted_trials = sorted(branch["trials"], key=lambda item: Q(item["mean_square"]))
            beam_seeds, seen_assign = [], set()
            for tr in sorted_trials:
                if tr["assignment_decimal"] not in seen_assign:
                    seen_assign.add(tr["assignment_decimal"])
                    c_vec, _ = babai._round_profile(
                        rows, order, centers, exact["normalized_gram_pivots"],
                        exact["rounding_profile"]["upper_rows"], exact["rounding_profile"]["prefix"],
                        int(tr["offset"]),
                    )
                    beam_seeds.append(c_vec)
                    if len(beam_seeds) == 3:
                        break
            beam_planes = list(range(d-2, max(-1, d-5), -1))
            beam = multilevel_beam_search(rows, labels, order, centers, exact,
                                          beam_seeds, beam_planes, beam_width=3, radius=2)
            run_seconds = time.perf_counter() - t_run
            rs_bound = readset.readset_bound(m, len(blind_indices), order, branch["trials_evaluated"])
            center_runs.append({
                "center_seed": center_seed,
                "centers_sha256": hashlib.sha256(json.dumps(centers).encode()).hexdigest(),
                "zero_control_mean_square": str(zero_w["mean_square"]),
                "plain_babai_assignment_decimal": str(exact["assignment"]),
                "plain_babai_mean_square": str(babai_w["mean_square"]),
                "plain_babai_threshold_met": babai_w["accepted"],
                "last_plane_33branch_best_assignment_decimal": branch["best"]["assignment_decimal"],
                "last_plane_33branch_best_mean_square": branch["best"]["mean_square"],
                "last_plane_33branch_threshold_met": branch["best"]["threshold_met"],
                "last_plane_target_blind_readset_bound": rs_bound["success_probability_upper"],
                "greedy_feedback_best_assignment_decimal": greedy["best"]["assignment_decimal"],
                "greedy_feedback_best_mean_square": greedy["best"]["mean_square"],
                "greedy_feedback_threshold_met": greedy["best"]["threshold_met"],
                "multilevel_beam_best_assignment_decimal": beam["best"]["assignment_decimal"],
                "multilevel_beam_best_mean_square": beam["best"]["mean_square"],
                "multilevel_beam_threshold_met": beam["best"]["threshold_met"],
                "multilevel_beam_improved_over_last_plane": (
                    Q(beam["best"]["mean_square"]) < Q(branch["best"]["mean_square"])
                ),
                "wall_seconds": run_seconds,
            })
        length_records.append({
            "length": m,
            "cap_each_sign": cap,
            "moment_budget": moment,
            "modulus_exponent": public["exponent"],
            "cyclic_order_bits": order.bit_length(),
            "finite_quantum_certificate": finite_q_cert,
            "uniform_m20000_theorem_applied": False,
            "label_construction_seconds": label_seconds,
            "lll_reduction_seconds": lll_seconds,
            "orthogonal_integer_prefix_rank": len(blind_indices),
            "exact_core_dimension": len(read_indices),
            "blind_fraction": str(Q(len(blind_indices), m)),
            "read_fraction": str(Q(len(read_indices), m)),
            "center_runs": center_runs,
        })
    return {
        "lengths_tested": list(lengths),
        "seeds_per_length": seeds_per_length,
        "threshold": str(near.GRID_THRESHOLD),
        "records": length_records,
        "all_public_generation_and_lll_costs_charged": True,
        "asymptotic_dequantization_claimed": False,
    }


def cosine_family_924bit_attack_campaign(center_seeds=(2026102001, 2026102002)):
    """Matched p-adic digit/block, CRT subgroup, and row-subset LLL attacks on the 924-bit J=1 cosine instance."""
    started = time.perf_counter()
    interp_bytes = integer.REPORT.read_bytes()
    interp_report = json.loads(interp_bytes)
    if interp_report["producer_sha256"] != hashlib.sha256(Path(integer.__file__).read_bytes()).hexdigest():
        raise ValueError("reproduce stale integer_character_interpolation artifact before cosine attack")
    native = interp_report["native"]
    primes = native["public_primes"]
    labels = list(map(int, native["public_labels_decimal"]))
    exponent = native["modulus_exponent"]
    order = int(native["cyclic_order_decimal"])
    integer.validate_public_labels(primes, labels, exponent)
    q3 = 3**(exponent - 1)
    m = len(labels)

    # Precompute target-independent d=64 row-subset LLL basis once and charge it
    t_lll = time.perf_counter()
    subset_dim = 64
    sub_labels = labels[:subset_dim]
    _, sub_basis = near.lattice_bases(sub_labels, order)
    sub_red = fmpz_mat(sub_basis).lll(delta=0.99, eta=0.51)
    sub_rows = [[int(v) for v in r] for r in sub_red.tolist()]
    lll_d64_seconds = time.perf_counter() - t_lll
    sub_blind, sub_read = extract_prefix_and_readset(sub_rows, sub_labels, order)

    def exact_big_int_float_cosine(x_val, centers):
        if type(x_val) is not int or not 0 <= x_val < order:
            raise ValueError("canonical integer assignment required")
        twopi = 2.0 * math.pi
        total = 0.0
        for a, c in zip(labels, centers):
            r = (a * x_val - c) % order
            total += math.cos(twopi * (r / order))
        return total / m

    def topdown_padic_block_polish(start_x, start_cos, centers, top_places=40):
        cur_x, cur_cos = start_x, start_cos
        accepted_moves = 0
        evals = 0
        for j in range(5, 5 + top_places):
            place = exponent - 1 - j
            step_3 = (2 * (3**place)) % order
            best_x, best_cos = cur_x, cur_cos
            for d in range(1, 9):
                cand_x = (cur_x + d * step_3) % order
                evals += 1
                sc = exact_big_int_float_cosine(cand_x, centers)
                if sc > best_cos + 1e-15:
                    best_cos, best_x = sc, cand_x
            if best_x != cur_x:
                accepted_moves += 1
                cur_x, cur_cos = best_x, best_cos
        return cur_x, cur_cos, accepted_moves, evals

    seed_runs = []
    for c_seed in center_seeds:
        rng = random.Random(c_seed)
        centers = [rng.randrange(order) for _ in range(m)]
        centers_sha256 = hashlib.sha256(json.dumps(list(map(str, centers))).encode()).hexdigest()

        # 1. Zero control
        zero_ver = uniform.verify_score(labels, centers, order, 0)

        # 2. Exact CRT subgroup of order 2 * 3^4 = 162
        sub_step = 3**(exponent - 5)
        best_sub_x, best_sub_cos = 0, exact_big_int_float_cosine(0, centers)
        for e in (0, 1):
            for u in range(81):
                cand_x = uniform.crt_character_label(e, (sub_step * u) % q3, exponent)
                sc = exact_big_int_float_cosine(cand_x, centers)
                if sc > best_sub_cos:
                    best_sub_cos, best_sub_x = sc, cand_x
        sub_ver = uniform.verify_score(labels, centers, order, best_sub_x)

        # 3. Top-down 3-adic 2-trit block search from CRT subgroup winner
        padic_x, padic_cos, padic_moves, padic_evals = topdown_padic_block_polish(
            best_sub_x, best_sub_cos, centers, top_places=40
        )
        padic_ver = uniform.verify_score(labels, centers, order, padic_x)

        # 4. Tempered multi-start 3-adic digit search (4 starts x 30 steps)
        sa_rng = random.Random(c_seed + 500)
        best_sa_x, best_sa_cos = best_sub_x, best_sub_cos
        sa_evals = 0
        for _ in range(4):
            e0 = sa_rng.randrange(2)
            v0 = sa_rng.randrange(q3)
            cur_x = uniform.crt_character_label(e0, v0, exponent)
            cur_cos = exact_big_int_float_cosine(cur_x, centers)
            sa_evals += 1
            if cur_cos > best_sa_cos:
                best_sa_cos, best_sa_x = cur_cos, cur_x
            for step_i in range(30):
                beta = 25.0 + 5.0 * step_i
                j = sa_rng.randrange(1, 45)
                place = exponent - 1 - j
                d = sa_rng.randrange(1, 3)
                cand_x = (cur_x + d * 2 * (3**place)) % order
                cand_cos = exact_big_int_float_cosine(cand_x, centers)
                sa_evals += 1
                if cand_cos > best_sa_cos:
                    best_sa_cos, best_sa_x = cand_cos, cand_x
                delta = cand_cos - cur_cos
                if delta >= 0 or sa_rng.random() < math.exp(max(-700.0, beta * delta)):
                    cur_x, cur_cos = cand_x, cand_cos
        sa_ver = uniform.verify_score(labels, centers, order, best_sa_x)

        # 5. Row-subset d=64 LLL + nearest-plane + 33-branch + top-down 3-adic polish
        exact_sub = babai.exact_normalized_babai(sub_rows, sub_labels, order, centers[:subset_dim])
        branch_sub = babai.bounded_last_plane_search(
            sub_rows, sub_labels, order, centers[:subset_dim], exact_sub, radius=16
        )
        best_lll_x, best_lll_cos = 0, -1.0
        for tr in branch_sub["trials"]:
            x_cand = int(tr["assignment_decimal"])
            sc = exact_big_int_float_cosine(x_cand, centers)
            if sc > best_lll_cos:
                best_lll_cos, best_lll_x = sc, x_cand
        lll_ver = uniform.verify_score(labels, centers, order, best_lll_x)
        lll_pol_x, lll_pol_cos, lll_pol_moves, lll_pol_evals = topdown_padic_block_polish(
            best_lll_x, best_lll_cos, centers, top_places=25
        )
        lll_pol_ver = uniform.verify_score(labels, centers, order, lll_pol_x)

        methods = [
            {
                "name": "zero_assignment_control",
                "evaluations": 1,
                "assignment_decimal": "0",
                "arb_score_verification": zero_ver,
            },
            {
                "name": "exact_crt_subgroup_order_162",
                "evaluations": 162,
                "assignment_decimal": str(best_sub_x),
                "arb_score_verification": sub_ver,
            },
            {
                "name": "padic_topdown_2trit_block_from_subgroup",
                "evaluations": 162 + padic_evals,
                "accepted_block_moves": padic_moves,
                "assignment_decimal": str(padic_x),
                "arb_score_verification": padic_ver,
            },
            {
                "name": "tempered_padic_multistart_4x30",
                "evaluations": sa_evals,
                "assignment_decimal": str(best_sa_x),
                "arb_score_verification": sa_ver,
            },
            {
                "name": "row_subset_d64_lll_33branch",
                "evaluations": len(branch_sub["trials"]),
                "subset_dimension": subset_dim,
                "subset_best_mean_square": branch_sub["best"]["mean_square"],
                "assignment_decimal": str(best_lll_x),
                "arb_score_verification": lll_ver,
            },
            {
                "name": "row_subset_d64_lll_plus_padic_topdown_polish",
                "evaluations": len(branch_sub["trials"]) + lll_pol_evals,
                "accepted_polish_moves": lll_pol_moves,
                "assignment_decimal": str(lll_pol_x),
                "arb_score_verification": lll_pol_ver,
            },
        ]
        best_method = max(methods, key=lambda item: Q(item["arb_score_verification"]["score_lower"]))
        seed_runs.append({
            "center_seed": c_seed,
            "centers_sha256": centers_sha256,
            "methods": methods,
            "best_method": best_method["name"],
            "best_score_lower": best_method["arb_score_verification"]["score_lower"],
            "best_score_upper": best_method["arb_score_verification"]["score_upper"],
            "threshold_3_10_accepted": best_method["arb_score_verification"]["accepted"],
        })
    return {
        "interpolation_artifact_sha256": hashlib.sha256(interp_bytes).hexdigest(),
        "dimension": m,
        "cap_each_sign": native["cap_each_sign"],
        "modulus_exponent": exponent,
        "cyclic_order_bits": order.bit_length(),
        "source_pilot_mean_cosine_lower": native["source_mean"]["mean_cosine_lower"],
        "score_threshold": "3/10",
        "row_subset_d64_lll_preprocessing": {
            "subset_dimension": subset_dim,
            "lll_seconds": lll_d64_seconds,
            "orthogonal_integer_prefix_rank": len(sub_blind),
            "exact_core_dimension": len(sub_read),
        },
        "int64_cast_used_on_labels_or_centers": False,
        "arb_interval_verifier_used": True,
        "seed_runs": seed_runs,
        "any_run_accepted_at_0_3": any(r["threshold_3_10_accepted"] for r in seed_runs),
        "elapsed_seconds_diagnostic": time.perf_counter() - started,
    }


def native_report(*, reuse_native_search=False, progress=None):
    attack_bytes, input_bytes = babai.REPORT.read_bytes(), near.REPORT.read_bytes()
    attack, source = json.loads(attack_bytes), json.loads(input_bytes)
    if (attack["producer_sha256"] != hashlib.sha256(Path(babai.__file__).read_bytes()).hexdigest()
            or source["producer_sha256"] != hashlib.sha256(Path(near.__file__).read_bytes()).hexdigest()
            or attack["input_artifact_sha256"] != hashlib.sha256(input_bytes).hexdigest()):
        raise ValueError("reproduce stale native input/Babai provenance before feedback search")
    native = source["native"]
    if native["length"] != 1024 or native["moment_budget"] != 16:
        raise ValueError("feedback experiment is fixed to the complete native J16 input")
    labels, centers = list(map(int, native["public_labels_decimal"])), list(map(int, native["centers_decimal"]))
    order = int(native["cyclic_order_decimal"])
    basis_path = ROOT/attack["basis_artifact"]
    if hashlib.sha256(basis_path.read_bytes()).hexdigest() != attack["basis_artifact_sha256"]:
        raise ValueError("native reduced basis hash mismatch")
    started = time.perf_counter()
    rows = babai.read_basis(basis_path)
    exact = babai.exact_normalized_babai(rows, labels, order, centers, progress=progress)
    profile_seconds = time.perf_counter()-started
    seed = attack["bounded_last_plane_search"]["best"]
    coefficients = list(map(int, seed["basis_coefficients_decimal"]))
    initial = evaluate(rows, labels, order, centers, coefficients)
    if str(initial["assignment"]) != seed["assignment_decimal"] or str(initial["mean_square"]) != seed["mean_square"]:
        raise ValueError("seed witness failed exact replay")

    d = exact["exact_core_dimension"]
    planes = list(range(d-2, max(-1, d-26), -1))
    reused_cached = False
    if reuse_native_search and REPORT.exists():
        cached = json.loads(REPORT.read_text())
        if (cached.get("babai_artifact_sha256") == hashlib.sha256(attack_bytes).hexdigest()
                and cached.get("input_artifact_sha256") == hashlib.sha256(input_bytes).hexdigest()
                and cached.get("basis_artifact_sha256") == attack["basis_artifact_sha256"]
                and "search" in cached and "multilevel_beam_search" in cached):
            search = cached["search"]
            beam_search = cached["multilevel_beam_search"]
            s_best = evaluate(rows, labels, order, centers, list(map(int, search["best"]["basis_coefficients_decimal"])))
            b_best = evaluate(rows, labels, order, centers, list(map(int, beam_search["best"]["basis_coefficients_decimal"])))
            if (str(s_best["mean_square"]) == search["best"]["mean_square"]
                    and str(b_best["mean_square"]) == beam_search["best"]["mean_square"]):
                search_seconds = cached["current_costs"]["feedback_search_seconds"]
                beam_seconds = cached["current_costs"].get("multilevel_beam_search_seconds", 0.0)
                reused_cached = True

    if not reused_cached:
        started = time.perf_counter()
        search = feedback_search(rows, labels, order, centers, exact, coefficients,
                                 planes, radius=4, progress=progress)
        search_seconds = time.perf_counter()-started

        started_beam = time.perf_counter()
        sorted_last_plane = sorted(
            attack["bounded_last_plane_search"]["trials"],
            key=lambda item: Q(item["mean_square"]),
        )
        beam_seed_coeffs, seen_assign = [], set()
        for tr in sorted_last_plane:
            if tr["assignment_decimal"] not in seen_assign:
                seen_assign.add(tr["assignment_decimal"])
                c_vec, _ = babai._round_profile(
                    rows, order, centers, exact["normalized_gram_pivots"],
                    exact["rounding_profile"]["upper_rows"], exact["rounding_profile"]["prefix"],
                    int(tr["offset"]),
                )
                beam_seed_coeffs.append(c_vec)
                if len(beam_seed_coeffs) == 4:
                    break
        beam_planes = list(range(d-2, max(-1, d-5), -1))
        beam_search = multilevel_beam_search(
            rows, labels, order, centers, exact, beam_seed_coeffs,
            beam_planes, beam_width=4, radius=2, progress=progress,
        )
        beam_seconds = time.perf_counter() - started_beam

    started_scaling = time.perf_counter()
    scaling_campaign = multi_length_j16_campaign(lengths=(32, 64, 96, 128), seeds_per_length=2)
    scaling_seconds = time.perf_counter() - started_scaling

    started_cosine = time.perf_counter()
    cosine_campaign = cosine_family_924bit_attack_campaign()
    cosine_seconds = time.perf_counter() - started_cosine

    return {
        "schema": "integer_character_feedback_v2",
        "status": "one_fixed_native_full_target_classical_attack_plus_beam_scaling_and_cosine_campaigns",
        "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "babai_artifact_sha256": hashlib.sha256(attack_bytes).hexdigest(),
        "input_artifact_sha256": hashlib.sha256(input_bytes).hexdigest(),
        "basis_artifact": attack["basis_artifact"],
        "basis_artifact_sha256": attack["basis_artifact_sha256"],
        "dimension": len(labels), "center_seed": native["center_seed"],
        "cyclic_order_bits": order.bit_length(), "original_threshold": str(near.GRID_THRESHOLD),
        "inherited_basis_and_seed_costs": {
            "basis_generation": attack["basis_generation"],
            "seed_profile_seconds": attack["exact_arithmetic"]["wall_seconds"],
            "seed_search_seconds": attack["bounded_last_plane_search"]["wall_seconds"],
            "scope": "inherited work is not free; incomplete-run elapsed already includes LLL, so do not add LLL twice",
        },
        "current_costs": {
            "basis_load_and_exact_profile_seconds": profile_seconds,
            "feedback_search_seconds": search_seconds,
            "multilevel_beam_search_seconds": beam_seconds,
            "multi_length_j16_campaign_seconds": scaling_seconds,
            "cosine_family_924bit_campaign_seconds": cosine_seconds,
        },
        "search": search,
        "multilevel_beam_search": beam_search,
        "multi_length_j16_campaign": scaling_campaign,
        "cosine_family_924bit_attack_campaign": cosine_campaign,
        "quantum_expected_distance_upper_reference": native["distance_bound"]["mean_normalized_squared_distance_upper"],
        "comparison_scope": "a single classical witness does not match a quantum output distribution or establish asymptotic performance",
        "classical_asymptotic_dequantization_proved": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPORT)
    parser.add_argument("--reuse-native-search", action="store_true",
                        help="reuse verified native greedy/beam search traces when provenance hashes match")
    args = parser.parse_args()
    report = native_report(
        reuse_native_search=args.reuse_native_search,
        progress=lambda event: print(json.dumps(event), flush=True),
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({
        "output": str(args.output),
        "initial_mean_square": float(Q(report["search"]["initial_mean_square"])),
        "final_mean_square": float(Q(report["search"]["best"]["mean_square"])),
        "beam_best_mean_square": float(Q(report["multilevel_beam_search"]["best"]["mean_square"])),
        "scaling_read_fractions": {
            str(r["length"]): r["read_fraction"] for r in report["multi_length_j16_campaign"]["records"]
        },
        "cosine_924bit_best_scores": [
            {"seed": r["center_seed"], "best_method": r["best_method"], "score_lower": float(Q(r["best_score_lower"]))}
            for r in report["cosine_family_924bit_attack_campaign"]["seed_runs"]
        ],
        "threshold_met": report["search"]["best"]["threshold_met"],
        "asymptotic_dequantization_claimed": False,
    }))


if __name__ == "__main__":
    main()
