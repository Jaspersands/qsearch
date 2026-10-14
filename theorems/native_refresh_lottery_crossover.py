"""Refresh-to-clean-basis crossover inequality and composed canonical DAG pipeline.

Proves that any terminal root g_term where the sign-mix refresh energy
threshold H(g_term) <= 0 automatically satisfies beta(g_term)^2 < (3/2)*delta_energy,
placing the unflooded canonical node inside the clean-basis lottery regime.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path

from native_affine_fibre_relaxation import canonical_vector
from native_basis_lottery import (
    _certificate_int,
    basis_probability_ledger,
    complete as lottery_complete,
    original_bank,
    original_fit,
)
from native_classical_modulus_descent import digest
from native_gaussian_quotient_completion import (
    gaussian_alphabet_boxes,
    gaussian_radius_box,
    nearest_odd_division,
)
from native_prefix_ambiguity_pruning import dag_pruning_source_ledger, modulo_scale_prefix_fit
from native_rounded_gaussian_tolerance import _ceil_log2_fraction, tolerance_budget
from native_small_multiple_completion import _rational, multiple_quotient
from ternary_covariant_noise import root_digits
from ternary_measured_lattice_decoder import exact_json, integer
from ternary_noise_degradation import NoisyLinearRecord, gaussian_rounding_loss

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT / "research/NATIVE_REFRESH_LOTTERY_CROSSOVER.md"
REPORT = ROOT / "research/reductions/native_refresh_lottery_crossover.json"


def _if_zero(prefix, n):
    prefix = tuple(prefix)
    if len(prefix) != n or any(type(x) is not int or x != 0 for x in prefix):
        raise ValueError("scale-1 canonical original prefix must be the zero vector")
    return prefix


def canonical_quotient_node(records, scale, prefix):
    """Extract a quotient node directly from original records, never flooded children."""
    original = original_bank(records)
    q0, n = original[0].modulus, len(original[0].label)
    integer(scale, "positive ternary quotient scale", 1)
    if scale > 1:
        root_digits(scale)
    if q0 % scale != 0:
        raise ValueError("scale must divide original modulus")
    g = q0 // scale
    root_digits(g)
    prefix = canonical_vector(prefix, n, scale) if scale > 1 else tuple(0 for _ in _if_zero(prefix, n))
    children, receipts = [], []
    for origin in original:
        residual = (origin.value - sum(a * p for a, p in zip(origin.label, prefix))) % q0
        value = nearest_odd_division(residual, scale) % g
        child = NoisyLinearRecord(tuple(a % g for a in origin.label), value, g, origin.source_id)
        children.append(child)
        receipts.append({
            "source_id": origin.source_id,
            "original_record_sha256": digest(origin.public()),
            "corrected_original_response": residual,
            "direct_original_derived_response": value,
        })
    node = {
        "original_records_sha256": digest(tuple(r.public() for r in original)),
        "original_modulus": q0,
        "modulus": g,
        "original_scale": scale,
        "known_original_lower_prefix_IF_path_true": prefix,
    }
    return {
        "status": "CANONICAL_ORIGINAL_QUOTIENT_NODE_FOR_REFRESH",
        "canonical_node": node,
        "canonical_node_sha256": digest(node),
        "derived_records": tuple(r.public() for r in children),
        "record_receipts": tuple(receipts),
        "original_records_paid_once": len(original),
        "canonical_rounding_evaluations": len(original),
        "canonical_node_from_originals_not_flooded_children": True,
        "true_prefix_or_Gaussian_law_certified": False,
    }


def _validate_signs(sign_matrix, m):
    signs = tuple(tuple(row) for row in sign_matrix)
    if not signs or any(len(row) != m or any(type(t) is not int or t not in (-1, 1) for t in row) for row in signs):
        raise ValueError("nonempty k-by-m sign matrix in {-1, +1} required")
    return signs


def refresh_batch(records, scale, prefix, sign_matrix, secret_mask, dithers):
    """Apply sign mixing, integer dither flooding and secret masking to a canonical node."""
    node_report = canonical_quotient_node(records, scale, prefix)
    g = node_report["canonical_node"]["modulus"]
    derived = node_report["derived_records"]
    m, n = len(derived), len(derived[0]["label"])
    signs = _validate_signs(sign_matrix, m)
    k = len(signs)
    mask = canonical_vector(secret_mask, n, g)
    dithers = tuple(dithers)
    if len(dithers) != k or any(type(d) is not int for d in dithers):
        raise ValueError("exact integer dither per refreshed row required")
    node_hash = node_report["canonical_node_sha256"]
    refreshed, receipts = [], []
    for r_idx, (t_row, dither) in enumerate(zip(signs, dithers)):
        label = tuple(sum(t * row["label"][j] for t, row in zip(t_row, derived)) % g for j in range(n))
        signed_y = sum(t * row["value"] for t, row in zip(t_row, derived)) % g
        mask_shift = sum(a * z for a, z in zip(label, mask)) % g
        value = (signed_y + dither - mask_shift) % g
        rec = NoisyLinearRecord(label, value, g, f"refresh:{node_hash[:12]}:{r_idx}")
        refreshed.append(rec.public())
        receipts.append({
            "row_index": r_idx,
            "sign_row": t_row,
            "dither": dither,
            "signed_canonical_response_mod_g": signed_y,
            "mask_shift_mod_g": mask_shift,
            "refreshed_record": rec.public(),
        })
    return {
        "status": "CONDITIONAL_SIGN_MIX_MASKED_REFRESH_BATCH",
        "canonical_node_report": node_report,
        "refreshed_rows": k,
        "parent_rows": m,
        "dimension": n,
        "modulus": g,
        "reduction_side_secret_mask": mask,
        "public_producer_input_records": tuple(refreshed),
        "refresh_row_receipts": tuple(receipts),
        "sign_sum_label_operations": k * m * n,
        "sign_sum_response_operations": k * m,
        "mask_shift_operations": k * n,
        "sign_matrix_or_secret_mask_disclosed_to_producer": False,
        "refreshed_records_are_independent_original_samples": False,
        "already_flooded_children_rerandomized": False,
        "dither_gaussian_law_or_parent_entropy_certified_by_algebra": False,
    }


def unmask_multiple(coefficient, masked_multiple, secret_mask, g):
    root_digits(g)
    if type(coefficient) is not int or coefficient % g == 0:
        raise ValueError("nonzero modulo-g exact integer coefficient required")
    n = len(secret_mask)
    w_masked = canonical_vector(masked_multiple, n, g)
    mask = canonical_vector(secret_mask, n, g)
    unmasked = tuple((w + coefficient * z) % g for w, z in zip(w_masked, mask))
    return {
        "modulus": g,
        "signed_coefficient": coefficient,
        "masked_multiple": w_masked,
        "unmasked_multiple": unmasked,
        "unmasking_multiply_add_operations": n,
        "coefficient_dependent_unmasking_is_free": False,
    }


def label_entropy_budget(n, m, k, reachable_root_digits, eta_label):
    integer(n, "positive dimension", 1)
    integer(m, "positive parent row count", 1)
    integer(k, "positive refreshed row count", 1)
    eta = _rational(eta_label)
    if not 0 < eta <= 1:
        raise ValueError("label TV target in (0, 1] required")
    digits_list = tuple(sorted(set(reachable_root_digits)))
    if not digits_list or any(type(d) is not int or d < 1 for d in digits_list):
        raise ValueError("nonempty positive reachable root digits required")
    per_root = []
    total_failure = Fraction(0)
    for d in digits_list:
        g = 3 ** d
        expected_chi2 = Fraction(g ** n - 1, 2 ** m)
        failure = min(Fraction(1), Fraction(k * k) * expected_chi2 / (4 * eta * eta))
        total_failure += failure
        per_root.append({
            "root_digits": d,
            "modulus": g,
            "expected_chi2": str(expected_chi2),
            "markov_label_failure_upper": str(failure),
        })
    union_failure = min(Fraction(1), total_failure)
    return {
        "dimension": n,
        "parent_rows": m,
        "refreshed_rows": k,
        "eta_label": str(eta),
        "reachable_root_digits": digits_list,
        "per_root_budgets": tuple(per_root),
        "all_reachable_roots_label_failure_union_upper": str(union_failure),
        "IID_uniform_original_labels_required": True,
        "single_adaptive_path_replaces_reachable_root_union": False,
        "fixed_instance_label_entropy_certified_by_hashes": False,
    }


def common_energy_budget(m, k, alpha_original, alpha_target, min_root_digits, eta_noise):
    integer(m, "positive parent row count", 1)
    integer(k, "positive refreshed row count", 1)
    integer(min_root_digits, "positive minimum reachable root digits", 1)
    a_orig = _rational(alpha_original)
    a_targ = _rational(alpha_target)
    eta = _rational(eta_noise)
    if not 0 < a_orig < 1 or a_targ <= 0 or not 0 < eta <= 1:
        raise ValueError("valid original width, positive target width and noise TV target required")
    g_min = 3 ** min_root_digits
    target_normalized_energy = eta * eta * a_targ * a_targ / Fraction(4 * k)
    rounding_floor = Fraction(m, 2 * g_min * g_min)
    H = (target_normalized_energy - rounding_floor) / 2
    expected_sum_X2_upper = Fraction(m) * a_orig * a_orig / 6
    if H <= 0:
        failure = Fraction(1)
        status = "NONPOSITIVE_ENERGY_THRESHOLD_VACUOUS"
    else:
        failure = min(Fraction(1), expected_sum_X2_upper / H)
        status = "POSITIVE_COMMON_ORIGINAL_ENERGY_EVENT_BOUND"
    return {
        "status": status,
        "parent_rows": m,
        "refreshed_rows": k,
        "alpha_original": str(a_orig),
        "alpha_target": str(a_targ),
        "alpha_target_in_torus_unit_interval": a_targ < 1,
        "minimum_reachable_root_digits": min_root_digits,
        "minimum_reachable_modulus": g_min,
        "eta_noise": str(eta),
        "required_normalized_quotient_energy_upper": str(target_normalized_energy),
        "worst_case_rounding_floor_m_over_2_g_min_squared": str(rounding_floor),
        "common_original_energy_threshold_H": str(H),
        "expected_original_sum_X_squared_upper": str(expected_sum_X2_upper),
        "common_energy_failure_upper": str(failure),
        "bound_is_nonvacuous": H > 0 and failure < 1 and a_targ < 1,
        "covers_every_true_quotient_at_or_above_g_min_simultaneously": H > 0,
        "assumes_sign_sum_error_and_label_independence": False,
        "original_error_independence_required_for_Markov_step": False,
    }


def dither_precision_budget(max_modulus, k, alpha_target, target_abort_loss):
    root_digits(max_modulus)
    integer(k, "positive refreshed row count", 1)
    a_targ = _rational(alpha_target)
    abort_target = _rational(target_abort_loss)
    if not 0 < a_targ < 1 or not 0 < abort_target <= 1:
        raise ValueError("subunit target width and positive abort target required")
    even_pairs = (k + 1) // 2
    needed = Fraction(4 * even_pairs) * (max_modulus + Fraction(1, a_targ)) / abort_target
    precision_bits = max(8, _ceil_log2_fraction(needed))
    width = Fraction(1, 2 ** precision_bits)
    rounding = gaussian_rounding_loss(max_modulus, str(a_targ), even_pairs, str(width))
    actual_abort = Fraction(rounding["two_M_input_rounding_abort_union_upper"])
    if actual_abort > abort_target:
        raise ArithmeticError("dither precision plan exceeded target abort loss")
    return {
        "maximum_modulus": max_modulus,
        "refreshed_rows_charged": k,
        "paired_rounding_calls_charged": even_pairs,
        "alpha_target": str(a_targ),
        "target_abort_loss_upper": str(abort_target),
        "dither_interval_precision_bits": precision_bits,
        "dither_interval_max_width": str(width),
        "rounding_abort_ledger": rounding,
        "dither_abort_union_upper": str(actual_abort),
        "uncharged_exact_Gaussian_oracle_used": False,
    }


def conditional_refresh_ledger(
    n,
    r,
    m,
    k,
    alpha_original,
    alpha_target,
    min_root_digits,
    max_root_digits,
    eta_label,
    eta_noise,
    dither_abort_loss,
    producer_average_success=None,
    refresh_calls_per_level=1,
    list_size_per_call=1,
    depth=1,
):
    integer(n, "positive dimension", 1)
    integer(r, "positive original root digits", 1)
    integer(min_root_digits, "positive minimum root digits", 1)
    integer(max_root_digits, "positive maximum root digits", min_root_digits)
    if max_root_digits > r:
        raise ValueError("reachable roots cannot exceed original root")
    integer(refresh_calls_per_level, "positive refresh calls per level", 1)
    integer(list_size_per_call, "positive producer list size per call", 1)
    integer(depth, "positive recursion depth", 1)
    reachable = tuple(range(min_root_digits, max_root_digits + 1))
    labels = label_entropy_budget(n, m, k, reachable, eta_label)
    energy = common_energy_budget(m, k, alpha_original, alpha_target, min_root_digits, eta_noise)
    a_targ = _rational(alpha_target)
    dither = (
        dither_precision_budget(3 ** max_root_digits, k, alpha_target, dither_abort_loss)
        if 0 < a_targ < 1
        else None
    )
    tolerance_min = (
        tolerance_budget(3 ** min_root_digits, n, k, alpha_target, "1/10", dither["dither_abort_union_upper"])
        if dither is not None and min_root_digits >= 2
        else None
    )
    eta_total = (
        _rational(eta_label) + _rational(eta_noise) + Fraction(dither["dither_abort_union_upper"])
        if dither is not None
        else None
    )
    parent_bad_union = min(
        Fraction(1),
        Fraction(labels["all_reachable_roots_label_failure_union_upper"]) + Fraction(energy["common_energy_failure_upper"]),
    )
    amplification = None
    if producer_average_success is not None and eta_total is not None:
        p_prod = _rational(producer_average_success)
        if not 0 <= p_prod <= 1:
            raise ValueError("valid producer average-case success probability required")
        p_eff = max(Fraction(0), p_prod - eta_total)
        per_level_miss = (1 - p_eff) ** refresh_calls_per_level
        all_levels_miss_union = min(Fraction(1), depth * per_level_miss)
        effective_branching = refresh_calls_per_level * list_size_per_call
        amplification = {
            "assumed_external_producer_average_success_at_alpha_target": str(p_prod),
            "per_call_refresh_TV_and_abort_loss": str(eta_total),
            "conditional_single_call_success_lower_on_good_parent": str(p_eff),
            "refresh_calls_per_level": refresh_calls_per_level,
            "list_candidates_per_call": list_size_per_call,
            "concatenated_list_candidates_per_level": effective_branching,
            "recursion_depth": depth,
            "complete_concatenated_tree_leaves_upper": effective_branching ** depth,
            "conditional_per_level_miss_upper_on_good_parent": str(per_level_miss),
            "conditional_all_levels_miss_union_upper_on_good_parent": str(all_levels_miss_union),
            "unconditional_good_parent_and_coverage_failure_upper_IF_producer_exists": str(
                min(Fraction(1), parent_bad_union + all_levels_miss_union)
            ),
            "concatenated_lists_resolve_B_to_D_ambiguity": False,
            "false_prefix_branches_obey_this_true_source_bound": False,
        }
    return {
        "dimension": n,
        "original_root_digits": r,
        "parent_rows": m,
        "refreshed_rows": k,
        "alpha_original": str(_rational(alpha_original)),
        "alpha_target": str(a_targ),
        "label_entropy_ledger": labels,
        "common_energy_ledger": energy,
        "dither_precision_ledger": dither,
        "minimum_root_published_tolerance_check": tolerance_min,
        "good_parent_failure_union_upper": str(parent_bad_union),
        "per_call_total_TV_and_abort_loss": None if eta_total is None else str(eta_total),
        "conditional_amplification_and_branching_ledger": amplification,
        "narrow_width_advantage_reused_at_alpha_target": False,
        "actual_quantum_decision_or_multiple_producer_supplied": False,
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
        "candidate_evaluations": tuple(evaluations),
        "surviving_canonical_child_nodes": tuple(surviving_nodes.values()),
        "surviving_canonical_child_count": len(surviving_nodes),
        "surviving_terminal_secrets": tuple(terminal_candidates),
        "require_non_wrapping_4R_lt_L": require_non_wrapping,
        "false_branch_null_assumption_used": False,
        "multiple_producer_supplied": False,
    }


def crossover_width_bound(m, k, alpha_original, alpha_target, min_refresh_digits, terminal_digits, eta_noise):
    """Prove beta(g_term)^2 < (3/2)*delta_energy when H(g_term) <= 0 and H(g_min) > 0."""
    integer(m, "positive original row count", 1)
    integer(k, "positive refreshed row count", 1)
    integer(min_refresh_digits, "positive minimum refresh root digits", 2)
    integer(terminal_digits, "positive terminal root digits", 1)
    if terminal_digits >= min_refresh_digits:
        raise ValueError("terminal root digits must be strictly below min_refresh_digits")
    high_energy = common_energy_budget(m, k, alpha_original, alpha_target, min_refresh_digits, eta_noise)
    term_energy = common_energy_budget(m, k, alpha_original, alpha_target, terminal_digits, eta_noise)
    a_orig = _rational(alpha_original)
    g_min = 3 ** min_refresh_digits
    g_term = 3 ** terminal_digits
    H_min = Fraction(high_energy["common_original_energy_threshold_H"])
    H_term = Fraction(term_energy["common_original_energy_threshold_H"])
    if H_min <= 0:
        raise ValueError("crossover bound requires positive H(g_min) at the refresh floor")
    delta_raw = Fraction(m) * a_orig * a_orig / (6 * H_min)
    delta_used = Fraction(high_energy["common_energy_failure_upper"])
    beta_term = a_orig * g_term
    beta_sq = beta_term * beta_term
    exact_identity_rhs = 6 * delta_raw * H_min * Fraction(g_term * g_term, m)
    if beta_sq != exact_identity_rhs:
        raise ArithmeticError("exact rational crossover identity failed")
    req_energy = Fraction(high_energy["required_normalized_quotient_energy_upper"])
    term_floor = Fraction(term_energy["worst_case_rounding_floor_m_over_2_g_min_squared"])
    in_nonpositive_H_zone = H_term <= 0
    in_half_floor_zone = term_floor >= req_energy / 2
    three_halves_bound = Fraction(3, 2) * delta_raw
    three_bound = 3 * delta_raw
    if in_nonpositive_H_zone and not (beta_sq < three_halves_bound):
        raise ArithmeticError("parameter-free (3/2)*delta_energy crossover inequality failed")
    if in_half_floor_zone and not (beta_sq < three_bound):
        raise ArithmeticError("parameter-free 3*delta_energy half-floor crossover inequality failed")
    return {
        "parent_rows": m,
        "refreshed_rows": k,
        "alpha_original": str(a_orig),
        "alpha_target": high_energy["alpha_target"],
        "eta_noise": high_energy["eta_noise"],
        "min_refresh_root_digits": min_refresh_digits,
        "min_refresh_modulus": g_min,
        "terminal_root_digits": terminal_digits,
        "terminal_modulus": g_term,
        "H_at_min_refresh_root": str(H_min),
        "H_at_terminal_root": str(H_term),
        "unclamped_markov_delta_energy_at_g_min": str(delta_raw),
        "clamped_common_energy_failure_upper_at_g_min": str(delta_used),
        "terminal_unflooded_derived_Gaussian_width_beta": str(beta_term),
        "terminal_beta_squared": str(beta_sq),
        "exact_identity_6_delta_H_min_g_term_sq_over_m": str(exact_identity_rhs),
        "three_halves_delta_energy_upper": str(three_halves_bound),
        "three_delta_energy_upper": str(three_bound),
        "terminal_H_is_nonpositive": in_nonpositive_H_zone,
        "terminal_rounding_floor_at_least_half_target": in_half_floor_zone,
        "beta_squared_strictly_below_three_halves_delta_when_H_nonpositive": (beta_sq < three_halves_bound) if in_nonpositive_H_zone else None,
        "beta_squared_strictly_below_three_delta_when_half_floor": (beta_sq < three_bound) if in_half_floor_zone else None,
        "parameter_cancellation_verified": True,
    }


def complete_canonical_node_via_lottery(records, scale, prefix, radius):
    """Complete a canonical node (g_term, L_term, P_term) via disjoint clean-basis lottery."""
    original = original_bank(records)
    q0, n = original[0].modulus, len(original[0].label)
    node_report = canonical_quotient_node(original, scale, prefix)
    node = node_report["canonical_node"]
    g_term = node["modulus"]
    P_term = node["known_original_lower_prefix_IF_path_true"]
    effective_multiple = tuple((g_term * p) % q0 for p in P_term)
    lottery = lottery_complete(original, g_term, effective_multiple, radius)
    if lottery["quotient_model"]["known_quotient_IF_multiple_is_true"] != P_term or lottery["quotient_model"]["nonunit_factor"] != g_term:
        raise ArithmeticError("canonical node to original-modulus multiple equivalence failed")
    return {
        "status": "CANONICAL_NODE_COMPLETED_BY_CLEAN_BASIS_LOTTERY" if lottery["candidate_secret"] is not None else "CANONICAL_NODE_LOTTERY_INCOMPLETE",
        "canonical_node": node,
        "canonical_node_sha256": node_report["canonical_node_sha256"],
        "equivalent_original_coefficient": g_term,
        "equivalent_original_multiple": effective_multiple,
        "canonical_node_to_multiple_equivalence_verified": True,
        "basis_lottery_completion": lottery,
        "candidate_secret": lottery["candidate_secret"],
        "further_source_refresh_used_at_terminal_node": False,
    }


def composed_pipeline_execution(records, refresh_stage_specs, terminal_Digits_threshold, radius):
    """Execute refresh + unmask + modulo-L DAG pruning down to g_term, then clean-basis lottery."""
    original = original_bank(records)
    q0, n = original[0].modulus, len(original[0].label)
    integer(terminal_Digits_threshold, "positive terminal digits threshold", 1)
    g_threshold = 3 ** terminal_Digits_threshold
    root_node = canonical_quotient_node(original, 1, (0,) * n)
    scale = 1
    prefix = (0,) * n
    stages = []
    for stage_idx, spec in enumerate(refresh_stage_specs):
        g = q0 // scale
        if g <= g_threshold:
            break
        signs = spec["signs"]
        mask = spec["mask"]
        dithers = spec["dithers"]
        masked_candidates = spec["masked_candidates"]
        refreshed = refresh_batch(original, scale, prefix, signs, mask, dithers)
        unmasked_candidates = []
        unmask_receipts = []
        for coeff, w_masked in masked_candidates:
            u = unmask_multiple(coeff, w_masked, mask, g)
            unmask_receipts.append(u)
            unmasked_candidates.append((coeff, u["unmasked_multiple"]))
        pruned = prune_candidate_list_at_node(original, scale, prefix, unmasked_candidates, radius, require_non_wrapping=True)
        stages.append({
            "stage_index": stage_idx,
            "parent_modulus": g,
            "parent_scale": scale,
            "refresh_batch": refreshed,
            "unmask_receipts": tuple(unmask_receipts),
            "modulo_scale_pruning": pruned,
        })
        if pruned["surviving_terminal_secrets"]:
            return {
                "status": "COMPOSED_PIPELINE_TERMINATED_AT_UNIT_STEP",
                "original_records_sha256": root_node["canonical_node"]["original_records_sha256"],
                "terminal_modulus_threshold": g_threshold,
                "refresh_pruning_stages": tuple(stages),
                "terminal_lottery_stage": None,
                "candidate_secret": pruned["surviving_terminal_secrets"][0],
            }
        if not pruned["surviving_canonical_child_nodes"]:
            return {
                "status": "COMPOSED_PIPELINE_NO_SURVIVING_CANONICAL_NODE",
                "original_records_sha256": root_node["canonical_node"]["original_records_sha256"],
                "terminal_modulus_threshold": g_threshold,
                "refresh_pruning_stages": tuple(stages),
                "terminal_lottery_stage": None,
                "candidate_secret": None,
            }
        chosen = min(pruned["surviving_canonical_child_nodes"], key=lambda ch: ch["canonical_node"]["modulus"])
        scale = chosen["canonical_node"]["original_scale"]
        prefix = chosen["canonical_node"]["known_original_lower_prefix_IF_path_true"]
    terminal_lottery = complete_canonical_node_via_lottery(original, scale, prefix, radius)
    return {
        "status": (
            "COMPOSED_REFRESH_DAG_AND_TERMINAL_LOTTERY_RECOVERY"
            if terminal_lottery["candidate_secret"] is not None
            else "COMPOSED_PIPELINE_TERMINAL_LOTTERY_FAILED"
        ),
        "original_records_sha256": root_node["canonical_node"]["original_records_sha256"],
        "terminal_modulus_threshold": g_threshold,
        "refresh_pruning_stages": tuple(stages),
        "terminal_lottery_stage": terminal_lottery,
        "candidate_secret": terminal_lottery["candidate_secret"],
        "multiple_producer_or_source_law_certified": False,
    }


def composed_crossover_source_ledger(
    n,
    r,
    m,
    k,
    alpha_original,
    alpha_target,
    min_refresh_digits,
    max_refresh_digits,
    terminal_lottery_digits,
    coefficient_bound,
    eta_label,
    eta_noise,
    dither_abort_loss,
    producer_average_success,
    refresh_calls_per_level,
    list_size_per_call,
    bits=128,
):
    depth = max_refresh_digits - min_refresh_digits + 1
    refresh_ledger = conditional_refresh_ledger(
        n,
        r,
        m,
        k,
        alpha_original,
        alpha_target,
        min_refresh_digits,
        max_refresh_digits,
        eta_label,
        eta_noise,
        dither_abort_loss,
        producer_average_success,
        refresh_calls_per_level,
        list_size_per_call,
        depth,
    )
    b_level = 2 * coefficient_bound * refresh_calls_per_level * list_size_per_call
    dag_ledger = dag_pruning_source_ledger(n, r, m, alpha_original, coefficient_bound, b_level, bits)
    crossover = crossover_width_bound(
        m, k, alpha_original, alpha_target, min_refresh_digits, terminal_lottery_digits, eta_noise
    )
    g_term = 3 ** terminal_lottery_digits
    a_orig = _rational(alpha_original)
    lottery_ledger = basis_probability_ledger(n, m // n, a_orig * g_term, g_term, bits)
    total_local_source_failure = min(
        Fraction(1),
        Fraction(dag_ledger["total_local_pruning_and_radius_failure_upper"])
        + Fraction(refresh_ledger["good_parent_failure_union_upper"])
        + Fraction(lottery_ledger["all_trials_fail_probability_upper"]),
    )
    amp = refresh_ledger["conditional_amplification_and_branching_ledger"]
    total_with_conditional_coverage = min(
        Fraction(1),
        total_local_source_failure + Fraction(amp["conditional_all_levels_miss_union_upper_on_good_parent"]),
    )
    return {
        "dimension": n,
        "original_root_digits": r,
        "original_rows": m,
        "refreshed_rows": k,
        "alpha_original": str(a_orig),
        "alpha_target": str(_rational(alpha_target)),
        "min_refresh_root_digits": min_refresh_digits,
        "max_refresh_root_digits": max_refresh_digits,
        "terminal_lottery_root_digits": terminal_lottery_digits,
        "high_root_refresh_ledger": refresh_ledger,
        "modulo_scale_dag_pruning_ledger": dag_ledger,
        "refresh_to_lottery_crossover": crossover,
        "terminal_clean_basis_lottery_ledger": lottery_ledger,
        "unconditioned_local_source_failure_union_upper": str(total_local_source_failure),
        "composed_failure_upper_IF_external_producer_meets_average_contract": str(total_with_conditional_coverage),
        "crossover_eliminates_small_root_refresh_vacuity": (
            crossover["terminal_H_is_nonpositive"]
            and refresh_ledger["common_energy_ledger"]["bound_is_nonvacuous"]
            and Fraction(lottery_ledger["all_trials_fail_probability_upper"]) < Fraction(1, 10 ** 15)
        ),
        "actual_quantum_decision_or_multiple_producer_supplied": False,
    }


def verify_probability_boxes(report):
    checked = 0
    for p in report["composed_scaling_profiles"]:
        dag_box = p["modulo_scale_dag_pruning_ledger"]["original_Gaussian_radius_law"]
        r_val = _certificate_int(dag_box["integer_error_radius"])
        if exact_json(gaussian_radius_box(dag_box["continuous_Gaussian_width"], r_val, dag_box["enclosure_bits"])) != dag_box:
            raise ValueError("DAG Gaussian radius box replay failed")
        lot = p["terminal_clean_basis_lottery_ledger"]
        z, wrap = lot["Gaussian_derived_error_law"], lot["nonzero_ring_wrap_tail"]
        if gaussian_alphabet_boxes(z["continuous_Gaussian_width"], z["enclosure_bits"]) != z:
            raise ValueError("terminal lottery Gaussian zero mass replay failed")
        if exact_json(gaussian_radius_box(wrap["continuous_Gaussian_width"], _certificate_int(wrap["integer_error_radius"]), wrap["enclosure_bits"])) != wrap:
            raise ValueError("terminal lottery wrap tail replay failed")
        checked += 3
    high_bad = report["falsifiers"]["premature_high_root_lottery_falsifier"]["high_root_lottery_ledger"]
    z, wrap = high_bad["Gaussian_derived_error_law"], high_bad["nonzero_ring_wrap_tail"]
    if gaussian_alphabet_boxes(z["continuous_Gaussian_width"], z["enclosure_bits"]) != z:
        raise ValueError("falsifier high-root Gaussian zero mass replay failed")
    if exact_json(gaussian_radius_box(wrap["continuous_Gaussian_width"], _certificate_int(wrap["integer_error_radius"]), wrap["enclosure_bits"])) != wrap:
        raise ValueError("falsifier high-root wrap tail replay failed")
    return {
        "verified": True,
        "Gaussian_laws_replayed": checked + 2,
        "same_trusted_Arb_special_functions_reused": True,
        "independent_transcendental_certificate_supplied": False,
    }


def calibration_pipeline_control(q0, n, r_high, r_term, secret, error_at_first_row):
    """Build an original bank with invertible blocks and execute the composed pipeline."""
    m = 3 * n
    raw = []
    for j in range(m):
        block_idx, row_in_block = divmod(j, n)
        if block_idx == 0:
            label = tuple((3 * (j + 1) * (q0 // 11 + i + 1)) % q0 for i in range(n))
        else:
            label = tuple((int(i == row_in_block) + 3 * ((j + 1) ** (i + 2) * (q0 // 11 + 7))) % q0 for i in range(n))
        e = error_at_first_row if j == n else 0
        val = (sum(a * s for a, s in zip(label, secret)) + e) % q0
        raw.append(NoisyLinearRecord(label, val, q0, f"crossover:{q0}:{j}"))
    raw = tuple(raw)
    radius = abs(error_at_first_row)
    g_high = 3 ** r_high
    g_term = 3 ** r_term
    signs0 = tuple(tuple(1 if (r + i) % 2 == 0 else -1 for i in range(m)) for r in range(m))
    mask0 = tuple((5 * (i + 1) + 1) % q0 for i in range(n))
    dithers0 = tuple((r % 3) - 1 for r in range(m))
    h_eff0 = tuple((s - z) % q0 for s, z in zip(secret, mask0))
    w_true0 = tuple((g_high * he) % q0 for he in h_eff0)
    w_false0 = tuple((g_high * he + g_high) % q0 for he in h_eff0)
    stage0 = {
        "signs": signs0,
        "mask": mask0,
        "dithers": dithers0,
        "masked_candidates": (
            (g_high, w_false0),
            (g_high, w_true0),
            (2 * g_high, tuple((2 * w) % q0 for w in w_true0)),
        ),
    }
    L1 = q0 // g_high
    h1 = tuple(s // L1 for s in secret)
    signs1 = tuple(tuple(1 if (r + 2 * i + 1) % 2 == 0 else -1 for i in range(m)) for r in range(m))
    mask1 = tuple((2 * (i + 1) + 1) % g_high for i in range(n))
    dithers1 = tuple(1 - (r % 3) for r in range(m))
    h_eff1 = tuple((h - z) % g_high for h, z in zip(h1, mask1))
    w_true1 = tuple((g_term * he) % g_high for he in h_eff1)
    w_false1 = tuple((g_term * he + g_term) % g_high for he in h_eff1)
    stage1 = {
        "signs": signs1,
        "mask": mask1,
        "dithers": dithers1,
        "masked_candidates": (
            (g_term, w_false1),
            (g_term, w_true1),
        ),
    }
    result = composed_pipeline_execution(raw, (stage0, stage1), r_term, radius)
    if result["candidate_secret"] != secret:
        raise ArithmeticError("composed refresh + DAG + clean-basis lottery calibration failed")
    return {
        "original_records": tuple(r.public() for r in raw),
        "original_secret_FOR_CALIBRATION_ONLY": secret,
        "original_error_at_index_n_FOR_CALIBRATION_ONLY": error_at_first_row,
        "verification_radius": radius,
        "pipeline_result": result,
        "matches_truth_after_solving": result["candidate_secret"] == secret,
        "actual_multiple_producer_supplied": False,
    }


def falsifiers():
    """Falsifiers for premature high-root lottery and below-floor refresh vacuity."""
    high_lottery = basis_probability_ledger(32, 128, Fraction(3 ** 10, 32768), 3 ** 10)
    term_crossover = crossover_width_bound(4096, 32, "1/32768", "1/4", 9, 5, "1/4")
    return {
        "premature_high_root_lottery_falsifier": {
            "dimension": 32,
            "high_root_digits": 10,
            "high_root_modulus": 3 ** 10,
            "derived_Gaussian_width_beta": str(Fraction(3 ** 10, 32768)),
            "high_root_lottery_ledger": high_lottery,
            "no_correct_basis_probability_lower_exceeds_99_percent": Fraction(high_lottery["no_correct_basis_probability_lower"]) > Fraction(99, 100),
            "skipping_refresh_descent_at_wide_root_works": False,
        },
        "below_floor_refresh_vacuous_but_lottery_succeeds_control": term_crossover,
    }


def build_report():
    deps = (
        "native_affine_fibre_relaxation.py",
        "native_basis_lottery.py",
        "native_gaussian_quotient_completion.py",
        "native_prefix_ambiguity_pruning.py",
        "native_small_multiple_completion.py",
        "native_source_refresh.py",
        "ternary_covariant_noise.py",
        "ternary_measured_lattice_decoder.py",
        "ternary_noise_degradation.py",
    )
    controls = (
        calibration_pipeline_control(3 ** 12, 2, 5, 2, (314159, 271828), 437),
        calibration_pipeline_control(
            3 ** 64,
            3,
            8,
            3,
            (3 ** 63 + 121, 3 ** 61 + 73, 3 ** 62 + 9),
            3 ** 20,
        ),
    )
    profiles = (
        composed_crossover_source_ledger(
            32, 32, 4096, 32, "1/32768", "1/4", 9, 10, 5, 512, "1/8", "1/4", "1/64", "3/4", 6, 4
        ),
        composed_crossover_source_ledger(
            128, 128, 8192, 64, "1/2097152", "1/4", 12, 13, 8, 16384, "1/8", "1/4", "1/64", "3/4", 8, 8
        ),
    )
    return {
        "status": "REFRESH_TO_CLEAN_BASIS_CROSSOVER_AND_COMPOSED_DAG_PIPELINE_REVIEW_PENDING",
        "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
        "dependency_sha256": {f: hashlib.sha256((ROOT / "theorems" / f).read_bytes()).hexdigest() for f in deps},
        "actual_composed_pipeline_controls": controls,
        "composed_scaling_profiles": profiles,
        "falsifiers": falsifiers(),
        "accepted_speedup_candidate": False,
        "new_active_negative_result_created": False,
        "actual_quantum_decision_or_multiple_producer": False,
        "complete_recursive_search_to_decision_reduction_established": False,
        "novelty_claim": False,
        "research_decision": "STOP_REFRESH_AT_ROUNDING_FLOOR_AND_FINISH_WITH_CLEAN_BASIS_LOTTERY_UNDER_PARAMETER_FREE_CROSSOVER_BOUND",
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
                "controls_match_truth": [c["matches_truth_after_solving"] for c in report["actual_composed_pipeline_controls"]],
                "crossover_eliminates_vacuity": [p["crossover_eliminates_small_root_refresh_vacuity"] for p in report["composed_scaling_profiles"]],
                "unconditioned_local_failure_uppers": [p["unconditioned_local_source_failure_union_upper"] for p in report["composed_scaling_profiles"]],
                "multiple_producer_supplied": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
