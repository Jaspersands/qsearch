"""Modulo-scale original-prefix pruning and canonical DAG width collapse.

Proves and audits that reducing (y_orig - a_orig . P) modulo the cumulative
scale L = q_0 / g eliminates the unknown upper secret L * h identically,
pruning all wrong prefixes in the non-wrapping regime 4 * R_orig < L and
collapsing surviving true candidates per valuation into one canonical node.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path

from native_affine_fibre_relaxation import canonical_vector
from native_basis_lottery import _certificate_int, original_bank, original_fit
from native_classical_modulus_descent import digest
from native_gaussian_quotient_completion import gaussian_radius_box
from native_small_multiple_completion import _rational, multiple_quotient, separation_ledger, PublicBasisCache, complete_multiple
from native_source_refresh import canonical_quotient_node
from ternary_covariant_noise import root_digits
from ternary_measured_lattice_decoder import exact_json, integer
from ternary_noise_degradation import NoisyLinearRecord

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT / "research/NATIVE_PREFIX_AMBIGUITY_PRUNING.md"
REPORT = ROOT / "research/reductions/native_prefix_ambiguity_pruning.json"


def modulo_scale_prefix_fit(records, scale, prefix, radius):
    """Evaluate modulo-L circular residual distances on the original bank."""
    original = original_bank(records)
    q0, n = original[0].modulus, len(original[0].label)
    integer(scale, "positive ternary scale L", 3)
    root_digits(scale)
    if q0 % scale != 0:
        raise ValueError("scale L must divide original modulus q_0")
    integer(radius, "nonnegative original error radius")
    if 4 * radius >= q0:
        raise ValueError("original radius requires4R<q_0")
    prefix = canonical_vector(prefix, n, scale)
    distances = tuple(
        min(r_mod, scale - r_mod)
        for rec in original
        for r_mod in ((rec.value - sum(a * p for a, p in zip(rec.label, prefix))) % scale,)
    )
    non_wrapping = 4 * radius < scale
    wraps_completely = scale <= 2 * radius
    return {
        "original_modulus": q0,
        "scale": scale,
        "remaining_child_modulus": q0 // scale,
        "candidate_prefix": prefix,
        "radius": radius,
        "non_wrapping_unique_decoding_regime_4R_lt_L": non_wrapping,
        "complete_wrap_zero_pruning_regime_L_le_2R": wraps_completely,
        "modulo_scale_circular_distances": distances,
        "original_records_checked": len(original),
        "fits_modulo_scale_radius": max(distances) <= radius,
        "upper_quotient_annihilated_modulo_scale": True,
        "pruning_soundness_requires_4R_lt_L_and_code_separation": True,
    }


def prune_candidate_list_at_node(records, scale, prefix, candidates, radius, require_non_wrapping=True):
    """Filter candidate (coefficient, multiple) pairs at a canonical node and merge survivors."""
    original = original_bank(records)
    q0, n = original[0].modulus, len(original[0].label)
    integer(radius, "public original radius")
    if 4 * radius >= q0:
        raise ValueError("original radius requires4R<q_0")
    parent_node = canonical_quotient_node(original, scale, prefix)
    g = parent_node["canonical_node"]["modulus"]
    candidates = tuple(candidates)
    if not candidates:
        raise ValueError("nonempty candidate (coefficient, multiple) list required")
    evaluations = []
    surviving_nodes = {}
    terminal_candidates = []
    distance_checks = 0
    node_rounding_checks = parent_node["original_response_rounding_evaluations"]
    for idx, (coeff, mult) in enumerate(candidates):
        mult = canonical_vector(mult, n, g)
        model = multiple_quotient(g, coeff, mult)
        entry = {"candidate_index": idx, "coefficient": coeff, "multiple": mult}
        if model is None:
            evaluations.append({**entry, "status": "REJECTED_INCOMPATIBLE_RING_IMAGE"})
            continue
        x, Q, g_child = model.quotient_secret, model.remaining_modulus, model.factor
        next_prefix = tuple(p + scale * xi for p, xi in zip(parent_node["canonical_node"]["known_original_lower_prefix_IF_path_true"], x))
        next_scale = scale * Q
        entry["quotient_model"] = model.record()
        entry["candidate_next_scale"] = next_scale
        entry["candidate_next_prefix"] = next_prefix
        if g_child == 1:
            fit = original_fit(original, next_prefix, radius)
            distance_checks += len(original)
            if fit["fits_public_radius"]:
                if next_prefix not in terminal_candidates:
                    terminal_candidates.append(next_prefix)
                evaluations.append({**entry, "status": "SURVIVING_TERMINAL_ORIGINAL_FIT", "original_fit": fit})
            else:
                evaluations.append({**entry, "status": "PRUNED_BY_FULL_ORIGINAL_RADIUS", "original_fit": fit})
            continue
        pfit = modulo_scale_prefix_fit(original, next_scale, next_prefix, radius)
        distance_checks += len(original)
        entry["modulo_scale_fit"] = pfit
        if require_non_wrapping and not pfit["non_wrapping_unique_decoding_regime_4R_lt_L"]:
            evaluations.append({**entry, "status": "UNPRUNED_WRAPPING_SCALE_4R_GE_L"})
            continue
        if not pfit["fits_modulo_scale_radius"]:
            evaluations.append({**entry, "status": "PRUNED_BY_MODULO_SCALE_ORIGINAL_RESIDUAL"})
            continue
        child_report = canonical_quotient_node(original, next_scale, next_prefix)
        node_rounding_checks += child_report["original_response_rounding_evaluations"]
        node_hash = child_report["canonical_node_sha256"]
        merged = node_hash in surviving_nodes
        if not merged:
            surviving_nodes[node_hash] = child_report
        evaluations.append({
            **entry,
            "status": "MERGED_INTO_EXISTING_CANONICAL_NODE" if merged else "SURVIVING_NEW_CANONICAL_NODE",
            "canonical_node_sha256": node_hash,
        })
    return {
        "parent_canonical_node": parent_node["canonical_node"],
        "parent_canonical_node_sha256": parent_node["canonical_node_sha256"],
        "candidates_evaluated": len(candidates),
        "original_modulo_distance_evaluations": distance_checks,
        "canonical_node_original_rounding_evaluations": node_rounding_checks,
        "candidate_evaluations": tuple(evaluations),
        "surviving_canonical_child_nodes": tuple(surviving_nodes.values()),
        "surviving_canonical_child_count": len(surviving_nodes),
        "surviving_terminal_secrets": tuple(terminal_candidates),
        "require_non_wrapping_4R_lt_L": require_non_wrapping,
        "false_branch_null_assumption_used": False,
        "multiple_producer_supplied": False,
    }


def pruned_dag_traversal(records, level_candidate_lists, radius):
    """Traverse a multi-level candidate DAG using modulo-L pruning and canonical node merging."""
    original = original_bank(records)
    q0, n = original[0].modulus, len(original[0].label)
    root_node = canonical_quotient_node(original, 1, (0,) * n)
    active = {root_node["canonical_node_sha256"]: root_node}
    levels = []
    expanded_hashes = set()
    expansion_calls = 0
    total_candidates = 0
    total_distance_checks = 0
    total_node_roundings = root_node["original_response_rounding_evaluations"]
    terminal_fits = []
    for depth_idx, candidate_map in enumerate(level_candidate_lists):
        next_active = {}
        level_reports = []
        for node_hash, node_report in active.items():
            g = node_report["canonical_node"]["modulus"]
            scale = node_report["canonical_node"]["original_scale"]
            prefix = node_report["canonical_node"]["known_original_lower_prefix_IF_path_true"]
            cands = candidate_map.get(g, ())
            if not cands:
                continue
            expanded_hashes.add(node_hash)
            expansion_calls += 1
            pruned = prune_candidate_list_at_node(original, scale, prefix, cands, radius, require_non_wrapping=True)
            total_candidates += pruned["candidates_evaluated"]
            total_distance_checks += pruned["original_modulo_distance_evaluations"]
            total_node_roundings += pruned["canonical_node_original_rounding_evaluations"]
            level_reports.append(pruned)
            for s in pruned["surviving_terminal_secrets"]:
                if s not in terminal_fits:
                    terminal_fits.append(s)
            for child in pruned["surviving_canonical_child_nodes"]:
                next_active[child["canonical_node_sha256"]] = child
        levels.append({
            "depth_index": depth_idx,
            "expanded_canonical_nodes": len(level_reports),
            "node_pruning_reports": tuple(level_reports),
            "distinct_surviving_child_nodes": len(next_active),
        })
        active = next_active
        if terminal_fits or not active:
            break
    return {
        "status": "CANONICAL_PRUNED_DAG_TERMINAL_FIT" if len(terminal_fits) == 1 else "CANONICAL_PRUNED_DAG_INCOMPLETE_OR_AMBIGUOUS",
        "original_records_sha256": root_node["canonical_node"]["original_records_sha256"],
        "original_records_paid_once": len(original),
        "verification_radius": radius,
        "levels_traversed": len(levels),
        "level_reports": tuple(levels),
        "total_candidates_evaluated": total_candidates,
        "total_original_distance_evaluations": total_distance_checks,
        "total_canonical_node_original_rounding_evaluations": total_node_roundings,
        "max_active_canonical_nodes_per_level": max((lv["distinct_surviving_child_nodes"] for lv in levels), default=0),
        "surviving_terminal_secrets": tuple(terminal_fits),
        "candidate_secret": terminal_fits[0] if len(terminal_fits) == 1 else None,
        "actual_canonical_node_expansion_calls": expansion_calls,
        "actual_distinct_canonical_nodes_expanded": len(expanded_hashes),
        "actual_repeated_canonical_node_expansions": expansion_calls - len(expanded_hashes),
        "global_candidate_list_per_node_cache_used": False,
        "unpruned_exponential_tree_elimination_certified_on_observed_bank": False,
        "polynomial_work_bound_requires_radius_code_separation_and_scope_events": True,
        "multiple_producer_or_source_law_certified": False,
    }


def direct_classical_root_comparison(records,candidates,radius):
    """Existing one-pass baseline on the same original controls and ALL root pairs."""
    raw=original_bank(records)
    if len(raw) % 2: raise ValueError("existing reference API requires even controls; do not pad originals")
    cache=PublicBasisCache(raw);trials=[];fits=[];roundings=distances=0
    for c,w in candidates:
        w=canonical_vector(w,len(raw[0].label),raw[0].modulus)
        result=complete_multiple(raw,c,w,cache=cache)
        roundings+=result["original_response_residual_evaluations"]
        fit=None
        if result["candidate_secret"] is not None:
            fit=original_fit(raw,result["candidate_secret"],radius);distances+=len(raw)
            if fit["fits_public_radius"] and result["candidate_secret"] not in fits: fits.append(result["candidate_secret"])
        trials.append({"coefficient":c,"multiple":w,"completion":result,"original_fit":fit})
    return {"original_records_paid_once":len(raw),"public_label_rref_calls":1,
        "cached_ring_inversions":len(cache.models),"original_response_rounding_evaluations":roundings,
        "original_candidate_distance_evaluations":distances,"root_trials":tuple(trials),"fitting_secrets":tuple(fits),
        "additional_multiple_or_decision_producer_calls":0,"Gaussian_flooded_samples_requested":0,
        "reference_API_parity_is_not_a_mathematical_condition":True,
        "planted_truth_or_source_law_certified":False}


def dag_pruning_source_ledger(n, r, m, alpha_original, coefficient_bound, list_candidates_per_node, bits=128):
    """Compare tight Gaussian radius vs crude Markov radius for modulo-L DAG pruning."""
    integer(n, "positive dimension", 1)
    integer(r, "positive root digits", 2)
    integer(m, "positive original rows", 1)
    integer(coefficient_bound, "positive centered coefficient bound", 3)
    integer(list_candidates_per_node, "positive list candidates per node", 1)
    q0 = 3 ** r
    alpha = _rational(alpha_original)
    if not 0 < alpha < 1:
        raise ValueError("positive subunit Gaussian width required")
    # First nonunit child modulus upper bound from c != 0 mod q_0 and |c| <= C:
    g_max, d_max = 1, 0
    while 3 * g_max <= coefficient_bound and d_max + 1 < r:
        g_max *= 3
        d_max += 1
    # Tight continuous-Gaussian radius R_gauss = ceil(8 * alpha * q0):
    scaled = 8 * alpha * q0
    R_gauss = (scaled.numerator + scaled.denominator - 1) // scaled.denominator
    gauss_box = gaussian_radius_box(alpha * q0, R_gauss, bits)
    whole_bank_gauss_tail = min(Fraction(1), m * Fraction(gauss_box["upper"]))
    # Maximum child modulus prunable under 4 * g * R_gauss < q0:
    g_prunable = 1
    d_prunable = 0
    while 4 * (3 * g_prunable) * R_gauss < q0 and d_prunable + 1 < r:
        g_prunable *= 3
        d_prunable += 1
    covers_all_first_step_children = d_max <= d_prunable
    # Union of modulo-L code separation failures over all reachable non-wrapping child valuations 1 <= d <= min(d_max, d_prunable):
    scale_ledgers = []
    sep_union = Fraction(0)
    for d in range(1, min(d_max, d_prunable) + 1):
        L = 3 ** (r - d)
        sep = separation_ledger(L, n, m, R_gauss)
        sep_union += Fraction(sep["global_code_separation_failure_upper_used"])
        scale_ledgers.append({
            "child_root_digits": d,
            "child_modulus": 3 ** d,
            "cumulative_scale_L": L,
            "non_wrapping_4R_lt_L": 4 * R_gauss < L,
            "modulo_scale_code_separation_ledger": sep,
        })
    full_sep = separation_ledger(q0, n, m, R_gauss)
    sep_union = min(Fraction(1), sep_union + Fraction(full_sep["global_code_separation_failure_upper_used"]))
    total_pruning_failure = min(Fraction(1), whole_bank_gauss_tail + sep_union)
    crude_R = q0 // n
    crude_d_prunable = 0
    while 4 * (3 ** (crude_d_prunable + 1)) * crude_R < q0 and crude_d_prunable + 1 < r:
        crude_d_prunable += 1
    return {
        "dimension": n,
        "original_root_digits": r,
        "original_modulus": q0,
        "original_rows": m,
        "alpha_original": str(alpha),
        "declared_centered_coefficient_bound": coefficient_bound,
        "first_step_max_child_root_digits": d_max,
        "first_step_max_child_modulus": g_max,
        "tight_Gaussian_verification_radius": R_gauss,
        "original_Gaussian_radius_law": gauss_box,
        "whole_bank_Gaussian_radius_failure_upper": str(whole_bank_gauss_tail),
        "max_prunable_child_root_digits_under_tight_radius": d_prunable,
        "max_prunable_child_modulus_under_tight_radius": g_prunable,
        "crude_q_over_n_radius_max_prunable_child_root_digits": crude_d_prunable,
        "tight_radius_covers_all_declared_nonunit_children": covers_all_first_step_children,
        "reachable_scale_separation_ledgers": tuple(scale_ledgers),
        "terminal_full_modulus_separation_ledger": full_sep,
        "all_scales_code_separation_failure_union_upper": str(sep_union),
        "total_local_pruning_and_radius_failure_upper": str(total_pruning_failure),
        "candidates_per_expanded_node": list_candidates_per_node,
        "unpruned_complete_tree_leaves_at_depth_d_max": list_candidates_per_node ** max(1, d_max),
        "pruned_canonical_DAG_internal_nodes_upper_IF_covered": d_max if covers_all_first_step_children else None,
        "internal_node_bound_counts_unique_nonroot_nodes_not_expansion_calls": True,
        "pruned_canonical_DAG_expansion_calls_upper_IF_covered": (
            1 + d_max * (d_max + 1) // 2 if covers_all_first_step_children else None
        ),
        "pruned_canonical_DAG_candidate_checks_upper_IF_covered": (
            (1 + d_max * (d_max + 1) // 2) * list_candidates_per_node if covers_all_first_step_children else None
        ),
        "coefficient_bound_derived_from_actual_or_published_producer": False,
        "all_actual_producer_coefficients_covered": False,
        "same_successful_pruning_events_imply_exact_one_pass_classical_completion": True,
        "pruning_opens_a_new_completion_regime_beyond_the_one_pass_baseline": False,
        "pruning_eliminates_exponential_tree_IF_4_g_max_R_lt_q0": covers_all_first_step_children,
        "pruning_supplies_missing_multiple_producer": False,
    }


def verify_probability_boxes(report):
    for p in report["Gaussian_DAG_pruning_profiles"]:
        box = p["original_Gaussian_radius_law"]
        r_val = _certificate_int(box["integer_error_radius"])
        expected = exact_json(gaussian_radius_box(box["continuous_Gaussian_width"], r_val, box["enclosure_bits"]))
        if expected != box:
            raise ValueError("Gaussian radius probability box replay failed")
    return {
        "verified": True,
        "Gaussian_profiles_replayed": len(report["Gaussian_DAG_pruning_profiles"]),
        "same_trusted_Arb_special_functions_reused": True,
        "independent_transcendental_certificate_supplied": False,
    }


def falsifiers():
    """Falsifiers for L <= 2*R complete wrap-around and 2*R < L <= 4*R collision zone."""
    q0 = 81
    secret = (47, 29)
    raw = tuple(
        NoisyLinearRecord(
            ((j + 1) % q0, (3 * j + 2) % q0),
            ((j + 1) * secret[0] + (3 * j + 2) * secret[1] + (1 if j % 2 == 0 else -1)) % q0,
            q0,
            f"wrap:{j}",
        )
        for j in range(6)
    )
    # 1. Complete wrap-around: scale L = 3, radius R = 2 (L <= 2*R). Every prefix in Z_3^2 fits!
    all_mod3_fits = [
        modulo_scale_prefix_fit(raw, 3, p, 2)["fits_modulo_scale_radius"]
        for p in ((0, 0), (1, 0), (2, 1), (secret[0] % 3, secret[1] % 3))
    ]
    blocked_pruning = prune_candidate_list_at_node(
        raw,
        1,
        (0, 0),
        ((27, (27 * (secret[0] % 3), 27 * (secret[1] % 3))), (27, (0, 0))),
        2,
        require_non_wrapping=True,
    )
    # 2. Half-modulus collision zone: scale L = 9, radius R = 3 (2*R < L <= 4*R).
    # Construct a 1D control where e = 3 and a wrong prefix differs by h=1 at label a=6 (6*1 = 6 == -3 mod 9, so e + 6 = 0 mod 9).
    collision_raw = (NoisyLinearRecord((6,), (6 * 5 + 3) % 81, 81, "half-wrap:0"),)
    true_fit_9 = modulo_scale_prefix_fit(collision_raw, 9, (5,), 3)
    wrong_fit_9 = modulo_scale_prefix_fit(collision_raw, 9, (6,), 3)
    return {
        "complete_wrap_L_le_2R_falsifier": {
            "scale": 3,
            "radius": 2,
            "all_tested_prefixes_fit_trivially": all(all_mod3_fits),
            "pruner_refuses_wrapping_scale": all(
                e["status"] == "UNPRUNED_WRAPPING_SCALE_4R_GE_L" for e in blocked_pruning["candidate_evaluations"]
            ),
            "surviving_canonical_child_count": blocked_pruning["surviving_canonical_child_count"],
        },
        "half_modulus_collision_2R_lt_L_le_4R_falsifier": {
            "scale": 9,
            "radius": 3,
            "non_wrapping_4R_lt_L": true_fit_9["non_wrapping_unique_decoding_regime_4R_lt_L"],
            "true_prefix_fits": true_fit_9["fits_modulo_scale_radius"],
            "colliding_wrong_prefix_also_fits": wrong_fit_9["fits_modulo_scale_radius"],
            "four_R_lt_L_is_sufficient_scope_not_instance_necessity": True,
        },
    }


def scope_and_revisit_countercontrols():
    raw = (NoisyLinearRecord((1,), 5, 81, "repeated-node"),)
    lists = (
        {81: ((9, (45,)), (3, (15,)))},
        {9: ((3, (0,)), (6, (0,))), 3: ((1, (1,)), (2, (2,)))},
        {3: ((1, (0,)), (2, (0,)))},
    )
    result = pruned_dag_traversal(raw, lists, 0)
    population = tuple(NoisyLinearRecord((a,), a * 5 % 81, 81, f"nonnecessary:{a}") for a in range(27))
    fits = tuple(x for x in range(27) if modulo_scale_prefix_fit(population, 27, (x,), 7)["fits_modulo_scale_radius"])
    return {
        "canonical_node_revisited_at_different_depths": {
            "original_records": tuple(r.public() for r in raw),
            "supplied_level_candidate_lists": lists,
            "dag_traversal": result,
            "claimed_old_linear_candidate_bound": 6,
            "actual_candidate_checks_exceed_old_bound": result["total_candidates_evaluated"] > 6,
            "different_depth_lists_must_not_be_silently_cached_as_one_list": True,
        },
        "unique_instance_outside_nonwrapping_proof_scope": {
            "original_records": tuple(r.public() for r in population),
            "scale": 27, "radius": 7, "complete_prefixes_checked": 27,
            "compatible_prefixes": fits,
            "four_R_lt_L": False,
            "proof_gate_is_not_a_general_instance_impossibility_claim": True,
        },
    }


def calibration_dag_control(q0, secret, errors):
    """Build a multi-path noisy candidate list with false branches and verify DAG collapse."""
    n = len(secret)
    raw = tuple(
        NoisyLinearRecord(
            tuple(((j + 1) ** (i + 1) + j + i) % q0 for i in range(n)),
            (sum(((j + 1) ** (i + 1) + j + i) * s for i, s in enumerate(secret)) + e) % q0,
            q0,
            f"dag:{q0}:{j}",
        )
        for j, e in enumerate(errors)
    )
    radius = max(abs(e) for e in errors)
    # Level 0 (at q0): supply TWO distinct true coefficients with gcd=9 (e.g. 9 and 18),
    # ONE true coefficient with gcd=3 (e.g. 3), and FOUR false candidate multiples!
    w_true_9 = tuple(9 * s % q0 for s in secret)
    w_true_18 = tuple(18 * s % q0 for s in secret)
    w_true_3 = tuple(3 * s % q0 for s in secret)
    w_false_9a = tuple((9 * s + 9) % q0 for s in secret)
    w_false_9b = tuple((9 * s + 27) % q0 for s in secret)
    w_false_incompat = tuple((9 * s + 1) % q0 for s in secret)
    level0 = {
        q0: (
            (9, w_false_9a),
            (9, w_false_9b),
            (9, w_false_incompat),
            (9, w_true_9),
            (18, w_true_18),
            (3, w_true_3),
        )
    }
    # Level 1 (at g=9 and g=3):
    h_9 = tuple(s // (q0 // 9) for s in secret)
    h_3 = tuple(s // (q0 // 3) for s in secret)
    level1 = {
        9: (
            (3, tuple((3 * h + 3) % 9 for h in h_9)),
            (3, tuple(3 * h % 9 for h in h_9)),
            (6, tuple(6 * h % 9 for h in h_9)),
        ),
        3: (
            (1, tuple((h + 1) % 3 for h in h_3)),
            (1, h_3),
        ),
    }
    # Level 2 (at g=3):
    level2 = {
        3: (
            (1, tuple((h + 2) % 3 for h in h_3)),
            (1, h_3),
            (2, tuple(2 * h % 3 for h in h_3)),
        )
    }
    dag = pruned_dag_traversal(raw, (level0, level1, level2), radius)
    return {
        "original_records": tuple(r.public() for r in raw),
        "original_secret_FOR_CALIBRATION_ONLY": secret,
        "original_errors_FOR_CALIBRATION_ONLY": errors,
        "supplied_level_candidate_lists": (level0, level1, level2),
        "one_pass_classical_root_comparison": direct_classical_root_comparison(raw,level0[q0],radius),
        "dag_traversal": dag,
        "matches_truth_after_solving": dag["candidate_secret"] == secret,
        "actual_multiple_producer_supplied": False,
    }


def build_report():
    deps = (
        "native_affine_fibre_relaxation.py",
        "native_basis_lottery.py",
        "native_classical_modulus_descent.py",
        "native_gaussian_quotient_completion.py",
        "native_small_multiple_completion.py",
        "native_source_refresh.py",
        "ternary_covariant_noise.py",
        "ternary_measured_lattice_decoder.py",
        "ternary_noise_degradation.py",
    )
    controls = (
        calibration_dag_control(3 ** 8, (4242, 3011), (13, -7, 0, 4, -3, 9, -11, 2)),
        calibration_dag_control(
            3 ** 64,
            (3 ** 63 + 121, 3 ** 61 + 73, 3 ** 62 + 9),
            (3 ** 20, -3 ** 21, 0, 1, -1, 11, -9, 5, -7, 3),
        ),
    )
    profiles = (
        dag_pruning_source_ledger(8, 8, 1024, "1/512", 64, 16),
        dag_pruning_source_ledger(32, 32, 4096, "1/32768", 512, 64),
        dag_pruning_source_ledger(128, 128, 32768, "1/2097152", 16384, 256),
    )
    return {
        "status": "MODULO_SCALE_PREFIX_PRUNING_AND_CANONICAL_DAG_COLLAPSE_AUDIT_REVIEW_PENDING",
        "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
        "dependency_sha256": {f: hashlib.sha256((ROOT / "theorems" / f).read_bytes()).hexdigest() for f in deps},
        "actual_dag_pruning_controls": controls,
        "Gaussian_DAG_pruning_profiles": profiles,
        "wrap_around_falsifiers": falsifiers(),
        "scope_and_revisit_countercontrols": scope_and_revisit_countercontrols(),
        "accepted_speedup_candidate": False,
        "new_active_negative_result_created": False,
        "actual_quantum_decision_or_multiple_producer": False,
        "complete_recursive_search_to_decision_reduction_established": False,
        "novelty_claim": False,
        "research_decision": "KEEP_PREFIX_PRUNING_AS_AUDIT_WHERE_ONE_PASS_CLASSICAL_COMPLETION_ALREADY_SUFFICES",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check-probabilities", action="store_true")
    args = parser.parse_args()
    if args.check_probabilities:
        print(json.dumps(verify_probability_boxes(json.loads(REPORT.read_text())), indent=2))
        return
    report = build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(report), indent=2) + "\n")
    print(
        json.dumps(
            {
                "status": report["status"],
                "dag_controls_match_truth": [c["matches_truth_after_solving"] for c in report["actual_dag_pruning_controls"]],
                "tight_radius_covers_all_children": [p["tight_radius_covers_all_declared_nonunit_children"] for p in report["Gaussian_DAG_pruning_profiles"]],
                "pruned_dag_nodes_upper": [p["pruned_canonical_DAG_internal_nodes_upper_IF_covered"] for p in report["Gaussian_DAG_pruning_profiles"]],
                "multiple_producer_supplied": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
