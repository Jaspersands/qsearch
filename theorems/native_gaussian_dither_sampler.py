"""Certified public rounded-Gaussian dither and sign/mask batch sampler.

Samples E = nearest(W) for W ~ sigma^-1 exp(-pi w^2 / sigma^2) using lazy
dyadic prefixes of a single uniform U in [0, 1) per draw and directed FLINT/Arb
CDF enclosures derived from gaussian_radius_box. Enforces the all-threshold
adaptive binary-search union bound 4*(2B+2)*2^-K and complete-batch aborts.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import json
from pathlib import Path

from native_basis_lottery import _certificate_int, original_bank
from native_classical_modulus_descent import digest
from native_gaussian_quotient_completion import gaussian_radius_box
from native_small_multiple_completion import _rational
from native_source_refresh import refresh_node, source_ledger
from ternary_covariant_noise import root_digits
from ternary_measured_lattice_decoder import exact_json, integer
from ternary_noise_degradation import NoisyLinearRecord

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT / "research/NATIVE_GAUSSIAN_DITHER_SAMPLER.md"
CONTRACT = ROOT / "research/hypotheses/native_gaussian_dither_sampler_contract.json"
REPORT = ROOT / "research/reductions/native_gaussian_dither_sampler.json"


def ceil_log2_int(m):
    """Exact integer ceiling of log2(m) for positive integer m."""
    integer(m, "positive integer for ceil_log2", 1)
    return (m - 1).bit_length()


def ceil_fraction_int(val):
    """Exact integer ceiling of a Fraction or rational value."""
    q = _rational(val)
    return (q.numerator + q.denominator - 1) // q.denominator


def dither_draw_parameters(sigma, failure_bits, k_override=None):
    """Compute truncation bound B, dyadic precision K, and adaptive union budgets."""
    sig = _rational(sigma)
    if sig <= 0:
        raise ValueError("positive exact rational sigma required")
    integer(failure_bits, "positive per-draw failure-bit target", 1)
    B = max(1, ceil_fraction_int(failure_bits * sig))
    min_K = failure_bits + ceil_log2_int(16 * (B + 1))
    if k_override is not None:
        integer(k_override, "positive dyadic prefix bits override", 1)
        K = k_override
    else:
        K = min_K
    num_thresholds = 2 * B + 2
    max_path_queries = ceil_log2_int(2 * B + 1) + 2
    max_cdf_width = Fraction(2, 2 ** K)
    adaptive_union = min(Fraction(1), Fraction(4 * num_thresholds, 2 ** K))
    naive_query_bound = min(Fraction(1), Fraction(4 * max_path_queries, 2 ** K))
    ratio = Fraction(num_thresholds, max_path_queries)
    tail_3f2 = Fraction(1, 2 ** min(512, 3 * failure_bits * failure_bits))
    tail_f1 = Fraction(1, 2 ** (failure_bits + 1))
    per_draw_loss = min(Fraction(1), adaptive_union + tail_f1)
    if k_override is None:
        if adaptive_union > tail_f1:
            raise ArithmeticError("adaptive precision abort bound exceeded 2^(-f-1)")
        if per_draw_loss > Fraction(1, 2 ** failure_bits):
            raise ArithmeticError("total per-draw coupling loss exceeded 2^(-f)")
    return {
        "sigma": str(sig),
        "failure_bits_target": failure_bits,
        "truncation_bound_B": B,
        "minimum_certified_dyadic_bits_K": min_K,
        "active_dyadic_bits_K": K,
        "using_uncertified_K_override": k_override is not None and K < min_K,
        "total_binary_search_thresholds_2B_plus_2": num_thresholds,
        "max_single_path_queries_ceil_log2_2B_plus_1_plus_2": max_path_queries,
        "required_cdf_enclosure_max_width": str(max_cdf_width),
        "adaptive_all_threshold_precision_abort_upper": str(adaptive_union),
        "naive_query_count_precision_bound_DO_NOT_USE": str(naive_query_bound),
        "adaptive_over_naive_threshold_multiplier": str(ratio),
        "adaptive_union_strictly_exceeds_naive_for_positive_B": num_thresholds > max_path_queries,
        "analytical_tail_abort_upper_2_pow_minus_3_f_sq": str(tail_3f2),
        "analytical_tail_abort_upper_2_pow_minus_f_minus_1": str(tail_f1),
        "per_draw_coupling_loss_upper": str(per_draw_loss),
        "per_draw_target_2_pow_minus_f": str(Fraction(1, 2 ** failure_bits)),
        "meets_per_draw_target": per_draw_loss <= Fraction(1, 2 ** failure_bits),
    }


def gaussian_cdf_box(sigma, t, K, min_enclosure_bits=None, max_enclosure_bits=512):
    """Compute directed rational enclosure of F(t) = P[E <= t] with width <= 2*2^-K."""
    sig = _rational(sigma)
    if sig <= 0:
        raise ValueError("positive exact rational sigma required")
    if type(t) is not int:
        raise ValueError("exact integer CDF threshold t required")
    integer(K, "positive dyadic precision bits K", 1)
    integer(max_enclosure_bits, "positive maximum Arb enclosure bits", 4)
    max_width = Fraction(2, 2 ** K)
    start_bits = K + 4 if min_enclosure_bits is None else max(4, min_enclosure_bits)
    if start_bits > max_enclosure_bits:
        start_bits = max_enclosure_bits

    radius = t if t >= 0 else (-t - 1)
    nonnegative = t >= 0
    bits = start_bits
    escalations = 0
    while True:
        rad_box = gaussian_radius_box(sig, radius, bits)
        tail_lo = Fraction(rad_box["lower"])
        tail_hi = Fraction(rad_box["upper"])
        if nonnegative:
            cdf_lo = Fraction(1) - tail_hi / 2
            cdf_hi = Fraction(1) - tail_lo / 2
        else:
            cdf_lo = tail_lo / 2
            cdf_hi = tail_hi / 2
        width = cdf_hi - cdf_lo
        escalations += 1
        if width <= max_width:
            return {
                "status": "CERTIFIED_DIRECTED_CDF_BOX",
                "continuous_Gaussian_width": str(sig),
                "threshold_t": t,
                "radius_index": radius,
                "nonnegative_branch": nonnegative,
                "enclosure_bits": bits,
                "escalation_evaluations": escalations,
                "underlying_tail_box": exact_json(rad_box),
                "lower": str(cdf_lo),
                "upper": str(cdf_hi),
                "width": str(width),
                "max_allowed_width": str(max_width),
                "width_satisfies_bound": True,
                "independent_transcendental_certificate_supplied": False,
            }
        if bits >= max_enclosure_bits:
            return {
                "status": "NUMERICAL_PRECISION_CAP_ABORT",
                "continuous_Gaussian_width": str(sig),
                "threshold_t": t,
                "radius_index": radius,
                "nonnegative_branch": nonnegative,
                "enclosure_bits": bits,
                "escalation_evaluations": escalations,
                "underlying_tail_box": exact_json(rad_box),
                "lower": str(cdf_lo),
                "upper": str(cdf_hi),
                "width": str(width),
                "max_allowed_width": str(max_width),
                "width_satisfies_bound": False,
                "independent_transcendental_certificate_supplied": False,
            }
        bits = min(max_enclosure_bits, max(bits + 16, bits * 2))


class BitTape:
    """Deterministic or external bit stream cursor with full consumption accounting."""

    def __init__(self, bits):
        cleaned = []
        for b in bits:
            if type(b) is not int or b not in (0, 1):
                raise ValueError("bit stream must contain only exact integers 0 or 1")
            cleaned.append(b)
        self._bits = tuple(cleaned)
        self._pos = 0

    @property
    def position(self):
        return self._pos

    @property
    def remaining(self):
        return len(self._bits) - self._pos

    def read_one(self):
        if self._pos >= len(self._bits):
            raise ValueError("bit stream exhausted before decision or precision cap")
        b = self._bits[self._pos]
        self._pos += 1
        return b

    def read_many(self, count):
        integer(count, "nonnegative bit count", 0)
        if self._pos + count > len(self._bits):
            raise ValueError("bit stream exhausted during multi-bit draw")
        out = self._bits[self._pos : self._pos + count]
        self._pos += count
        return out


def sample_rounded_gaussian_dither(
    sigma,
    failure_bits,
    bit_source,
    max_enclosure_bits=512,
    k_override=None,
    cdf_cache=None,
):
    """Sample one rounded-Gaussian dither E in [-B, B] with lazy dyadic prefix reading."""
    params = dither_draw_parameters(sigma, failure_bits, k_override=k_override)
    sig = _rational(sigma)
    B = params["truncation_bound_B"]
    K = params["active_dyadic_bits_K"]
    tape = bit_source if isinstance(bit_source, BitTape) else BitTape(bit_source)
    cache = {} if cdf_cache is None else cdf_cache

    prefix_bits = []
    prefix_int = 0
    comparisons = []
    arb_evaluations = 0

    def current_dyadic_box():
        r = len(prefix_bits)
        denom = 2 ** r
        return Fraction(prefix_int, denom), Fraction(prefix_int + 1, denom)

    def compare_threshold(t, role):
        nonlocal prefix_int, arb_evaluations
        key = (str(sig), t, K, max_enclosure_bits)
        if key in cache:
            cdf = cache[key]
            newly_evaluated = 0
        else:
            cdf = gaussian_cdf_box(sig, t, K, max_enclosure_bits=max_enclosure_bits)
            cache[key] = cdf
            newly_evaluated = cdf["escalation_evaluations"]
        arb_evaluations += newly_evaluated
        if cdf["status"] != "CERTIFIED_DIRECTED_CDF_BOX":
            u_lo, u_hi = current_dyadic_box()
            rec = {
                "step_index": len(comparisons),
                "role": role,
                "threshold_t": t,
                "cdf_box": cdf,
                "bits_read_after_step": len(prefix_bits),
                "dyadic_prefix_bits": tuple(prefix_bits),
                "dyadic_interval_lower": str(u_lo),
                "dyadic_interval_upper": str(u_hi),
                "outcome": "NUMERICAL_PRECISION_CAP_ABORT",
            }
            comparisons.append(rec)
            return "NUMERICAL_PRECISION_CAP_ABORT"

        cdf_lo = Fraction(cdf["lower"])
        cdf_hi = Fraction(cdf["upper"])
        while True:
            u_lo, u_hi = current_dyadic_box()
            if u_hi <= cdf_lo:
                rec = {
                    "step_index": len(comparisons),
                    "role": role,
                    "threshold_t": t,
                    "cdf_box": cdf,
                    "bits_read_after_step": len(prefix_bits),
                    "dyadic_prefix_bits": tuple(prefix_bits),
                    "dyadic_interval_lower": str(u_lo),
                    "dyadic_interval_upper": str(u_hi),
                    "outcome": "U_LT_F",
                }
                comparisons.append(rec)
                return "U_LT_F"
            if u_lo >= cdf_hi:
                rec = {
                    "step_index": len(comparisons),
                    "role": role,
                    "threshold_t": t,
                    "cdf_box": cdf,
                    "bits_read_after_step": len(prefix_bits),
                    "dyadic_prefix_bits": tuple(prefix_bits),
                    "dyadic_interval_lower": str(u_lo),
                    "dyadic_interval_upper": str(u_hi),
                    "outcome": "U_GE_F",
                }
                comparisons.append(rec)
                return "U_GE_F"
            if len(prefix_bits) >= K:
                rec = {
                    "step_index": len(comparisons),
                    "role": role,
                    "threshold_t": t,
                    "cdf_box": cdf,
                    "bits_read_after_step": len(prefix_bits),
                    "dyadic_prefix_bits": tuple(prefix_bits),
                    "dyadic_interval_lower": str(u_lo),
                    "dyadic_interval_upper": str(u_hi),
                    "outcome": "UNIFORM_PREFIX_PRECISION_ABORT",
                }
                comparisons.append(rec)
                return "UNIFORM_PREFIX_PRECISION_ABORT"
            bit = tape.read_one()
            prefix_bits.append(bit)
            prefix_int = (prefix_int << 1) | bit

    def finish(status, sampled_integer, abort_reason, tail_side=None):
        u_lo, u_hi = current_dyadic_box()
        return {
            "status": status,
            "draw_parameters": params,
            "sampled_integer": sampled_integer,
            "abort_reason": abort_reason,
            "tail_side": tail_side,
            "bits_consumed": len(prefix_bits),
            "dyadic_prefix_bits": tuple(prefix_bits),
            "dyadic_prefix_integer": prefix_int,
            "final_dyadic_lower": str(u_lo),
            "final_dyadic_upper": str(u_hi),
            "thresholds_queried_count": len(comparisons),
            "threshold_comparisons": tuple(comparisons),
            "arb_tail_evaluations": arb_evaluations,
            "max_enclosure_bits": max_enclosure_bits,
            "midpoint_or_floating_fallback_used": False,
            "silent_resampling_used": False,
            "independent_transcendental_certificate_supplied": False,
        }

    # 1. Left tail check at t = -B - 1
    left_out = compare_threshold(-B - 1, "LEFT_TAIL_CHECK")
    if left_out in ("UNIFORM_PREFIX_PRECISION_ABORT", "NUMERICAL_PRECISION_CAP_ABORT"):
        return finish(left_out, None, left_out)
    if left_out == "U_LT_F":
        return finish("TAIL_TRUNCATION_ABORT", None, "TAIL_TRUNCATION_ABORT", tail_side="LEFT_TAIL")

    # 2. Right tail check at t = B
    right_out = compare_threshold(B, "RIGHT_TAIL_CHECK")
    if right_out in ("UNIFORM_PREFIX_PRECISION_ABORT", "NUMERICAL_PRECISION_CAP_ABORT"):
        return finish(right_out, None, right_out)
    if right_out == "U_GE_F":
        return finish("TAIL_TRUNCATION_ABORT", None, "TAIL_TRUNCATION_ABORT", tail_side="RIGHT_TAIL")

    # 3. Binary search on [-B, B] for smallest t with U < F(t).
    # Invariant: U >= F(low - 1) and U < F(high).
    low = -B
    high = B
    while low < high:
        mid = (low + high) // 2
        out = compare_threshold(mid, "BINARY_SEARCH_STEP")
        if out in ("UNIFORM_PREFIX_PRECISION_ABORT", "NUMERICAL_PRECISION_CAP_ABORT"):
            return finish(out, None, out)
        if out == "U_LT_F":
            high = mid
        else:
            low = mid + 1

    # Verify bracketing certificate: U >= F(low - 1) and U < F(low)
    u_lo, u_hi = current_dyadic_box()
    lower_bracket_t = low - 1
    upper_bracket_t = low
    lower_box = cache[(str(sig), lower_bracket_t, K, max_enclosure_bits)]
    upper_box = cache[(str(sig), upper_bracket_t, K, max_enclosure_bits)]
    if not (u_lo >= Fraction(lower_box["upper"]) and u_hi <= Fraction(upper_box["lower"])):
        raise ArithmeticError("accepted sample failed certified quantile bracket")

    return finish("CERTIFIED_ROUNDED_GAUSSIAN_SAMPLE", low, None)


def complete_dyadic_prefix_census(sigma, failure_bits, census_bits, max_work=100000):
    """Exhaustively census all 2^census_bits dyadic prefixes of length census_bits."""
    integer(census_bits, "positive census dyadic bits", 1)
    integer(max_work, "positive census work cap", 1)
    params = dither_draw_parameters(sigma, failure_bits, k_override=census_bits)
    B = params["truncation_bound_B"]
    total_cells = 2 ** census_bits
    work = total_cells * params["max_single_path_queries_ceil_log2_2B_plus_1_plus_2"]
    if work > max_work:
        raise ValueError("complete dyadic prefix census work cap exceeded")

    sig = _rational(sigma)
    cdf_cache = {}
    all_thresholds = {}
    for t in range(-B - 1, B + 1):
        box = gaussian_cdf_box(sig, t, census_bits)
        if box["status"] != "CERTIFIED_DIRECTED_CDF_BOX":
            raise ArithmeticError("census CDF box failed width bound")
        cdf_cache[(str(sig), t, census_bits, 512)] = box
        all_thresholds[str(t)] = box

    status_counts = Counter()
    integer_counts = Counter()
    tail_sides = Counter()
    total_bits_consumed = 0

    for cell in range(total_cells):
        bits = tuple((cell >> (census_bits - 1 - j)) & 1 for j in range(census_bits))
        res = sample_rounded_gaussian_dither(
            sig,
            failure_bits,
            bits,
            k_override=census_bits,
            cdf_cache=cdf_cache,
        )
        st = res["status"]
        status_counts[st] += 1
        total_bits_consumed += res["bits_consumed"]
        u_lo = Fraction(cell, total_cells)
        u_hi = Fraction(cell + 1, total_cells)
        if st == "CERTIFIED_ROUNDED_GAUSSIAN_SAMPLE":
            val = res["sampled_integer"]
            integer_counts[str(val)] += 1
            lo_box = all_thresholds[str(val - 1)]
            hi_box = all_thresholds[str(val)]
            if not (u_lo >= Fraction(lo_box["upper"]) and u_hi <= Fraction(hi_box["lower"])):
                raise ArithmeticError("census accepted cell violated quantile enclosure")
        elif st == "TAIL_TRUNCATION_ABORT":
            side = res["tail_side"]
            tail_sides[side] += 1
            if side == "LEFT_TAIL":
                if not (u_hi <= Fraction(all_thresholds[str(-B - 1)]["lower"])):
                    raise ArithmeticError("census left-tail cell violated F(-B-1) lower bound")
            else:
                if not (u_lo >= Fraction(all_thresholds[str(B)]["upper"])):
                    raise ArithmeticError("census right-tail cell violated F(B) upper bound")
        elif st == "UNIFORM_PREFIX_PRECISION_ABORT":
            last_t = res["threshold_comparisons"][-1]["threshold_t"]
            t_box = all_thresholds[str(last_t)]
            if u_hi <= Fraction(t_box["lower"]) or u_lo >= Fraction(t_box["upper"]):
                raise ArithmeticError("census precision abort did not straddle threshold enclosure")
        else:
            raise ArithmeticError(f"unexpected census status {st}")

    precision_abort_rate = Fraction(status_counts["UNIFORM_PREFIX_PRECISION_ABORT"], total_cells)
    tail_abort_rate = Fraction(status_counts["TAIL_TRUNCATION_ABORT"], total_cells)
    accepted_rate = Fraction(status_counts["CERTIFIED_ROUNDED_GAUSSIAN_SAMPLE"], total_cells)
    if precision_abort_rate > Fraction(params["adaptive_all_threshold_precision_abort_upper"]):
        raise ArithmeticError("observed precision abort rate exceeded adaptive union bound")
    if accepted_rate + precision_abort_rate + tail_abort_rate != 1:
        raise ArithmeticError("census partition of unity failed")

    return {
        "sigma": str(sig),
        "failure_bits_target": failure_bits,
        "census_dyadic_bits": census_bits,
        "truncation_bound_B": B,
        "total_dyadic_cells_censused": total_cells,
        "total_lazy_bits_consumed": total_bits_consumed,
        "draw_parameters": params,
        "threshold_cdf_boxes": all_thresholds,
        "status_counts": dict(sorted(status_counts.items())),
        "sampled_integer_histogram": dict(sorted(integer_counts.items(), key=lambda kv: int(kv[0]))),
        "tail_abort_side_counts": dict(sorted(tail_sides.items())),
        "exact_accepted_mass": str(accepted_rate),
        "exact_precision_abort_mass": str(precision_abort_rate),
        "exact_tail_abort_mass": str(tail_abort_rate),
        "precision_abort_within_adaptive_union_bound": precision_abort_rate <= Fraction(params["adaptive_all_threshold_precision_abort_upper"]),
        "every_accepted_cell_verified_against_directed_cdf_brackets": True,
        "finite_census_is_an_oracle_or_speedup_candidate": False,
    }


def sample_uniform_signs_and_mask(n, m, k, g, mask_failure_bits, bit_source):
    """Sample paid uniform sign matrix in {-1,+1}^{k x m} and uniform mask in Z_g^n."""
    for x, name in (
        (n, "dimension"),
        (m, "parent rows"),
        (k, "output rows"),
        (mask_failure_bits, "mask failure bits"),
    ):
        integer(x, "positive " + name, 1)
    root_digits(g)
    tape = bit_source if isinstance(bit_source, BitTape) else BitTape(bit_source)
    start_pos = tape.position

    sign_rows = []
    for _ in range(k):
        bits = tape.read_many(m)
        sign_rows.append(tuple(2 * b - 1 for b in bits))
    sign_bits_used = k * m

    bits_per_trial = ceil_log2_int(g)
    trials_per_coord = mask_failure_bits + ceil_log2_int(max(2, n))
    single_trial_reject_prob = Fraction(2 ** bits_per_trial - g, 2 ** bits_per_trial)
    coord_abort_prob = single_trial_reject_prob ** trials_per_coord
    mask_abort_upper = min(Fraction(1), n * coord_abort_prob)
    if mask_abort_upper > Fraction(1, 2 ** mask_failure_bits):
        raise ArithmeticError("mask rejection abort upper bound exceeded 2^(-mask_failure_bits)")

    mask_coords = []
    coord_receipts = []
    mask_bits_used = 0
    aborted = False
    for coord_idx in range(n):
        trials = []
        accepted_val = None
        for t_idx in range(trials_per_coord):
            t_bits = tape.read_many(bits_per_trial)
            mask_bits_used += bits_per_trial
            val = 0
            for b in t_bits:
                val = (val << 1) | b
            accepted = val < g
            trials.append({
                "trial_index": t_idx,
                "bits": t_bits,
                "candidate_integer": val,
                "accepted": accepted,
            })
            if accepted:
                accepted_val = val
                break
        coord_receipts.append({
            "coordinate_index": coord_idx,
            "trials_attempted": len(trials),
            "accepted_value": accepted_val,
            "trial_receipts": tuple(trials),
        })
        if accepted_val is None:
            aborted = True
            break
        mask_coords.append(accepted_val)

    return {
        "status": "MASK_REJECTION_SAMPLING_ABORT" if aborted else "CERTIFIED_UNIFORM_SIGNS_AND_MASK",
        "dimension": n,
        "parent_rows": m,
        "output_rows": k,
        "modulus": g,
        "mask_failure_bits_target": mask_failure_bits,
        "bits_per_mask_trial": bits_per_trial,
        "max_trials_per_coordinate": trials_per_coord,
        "single_trial_rejection_probability": str(single_trial_reject_prob),
        "mask_rejection_abort_probability_upper": str(mask_abort_upper),
        "sign_bits_consumed": sign_bits_used,
        "mask_bits_consumed": mask_bits_used,
        "total_sign_and_mask_bits_consumed": tape.position - start_pos,
        "sign_rows": tuple(sign_rows),
        "secret_mask": None if aborted else tuple(mask_coords),
        "mask_coordinate_receipts": tuple(coord_receipts),
        "signs_and_mask_from_paid_ideal_bits": True,
    }


def batch_sampler_budget(n, m, k, g, sigma, batch_failure_bits, mask_failure_bits):
    """Compute complete-batch coupled sampler TV/abort loss budget."""
    for x, name in (
        (n, "dimension"),
        (m, "parent rows"),
        (k, "output rows"),
        (batch_failure_bits, "batch dither failure bits"),
        (mask_failure_bits, "mask failure bits"),
    ):
        integer(x, "positive " + name, 1)
    root_digits(g)
    per_draw_f = batch_failure_bits + ceil_log2_int(max(2, k))
    draw_params = dither_draw_parameters(sigma, per_draw_f)
    per_draw_loss = Fraction(draw_params["per_draw_coupling_loss_upper"])
    all_dithers_loss = min(Fraction(1), k * per_draw_loss)

    bits_per_trial = ceil_log2_int(g)
    trials_per_coord = mask_failure_bits + ceil_log2_int(max(2, n))
    single_reject = Fraction(2 ** bits_per_trial - g, 2 ** bits_per_trial)
    mask_loss = min(Fraction(1), n * (single_reject ** trials_per_coord))
    total_sampler_loss = min(Fraction(1), all_dithers_loss + mask_loss)

    max_bits_upper = k * m + n * trials_per_coord * bits_per_trial + k * draw_params["active_dyadic_bits_K"]
    return {
        "dimension": n,
        "parent_rows": m,
        "output_rows": k,
        "modulus": g,
        "sigma": draw_params["sigma"],
        "batch_dither_failure_bits_target": batch_failure_bits,
        "per_draw_failure_bits_f": per_draw_f,
        "mask_failure_bits_target": mask_failure_bits,
        "single_dither_draw_parameters": draw_params,
        "k_dither_draws_abort_union_upper": str(all_dithers_loss),
        "mask_rejection_abort_union_upper": str(mask_loss),
        "certified_complete_dither_sampler_TV_loss": str(total_sampler_loss),
        "worst_case_batch_random_bits_upper": max_bits_upper,
        "shortened_partial_batch_allowed": False,
        "fresh_randomness_counts_as_new_original_samples": False,
    }


def certified_refresh_batch(
    records,
    g,
    prefix,
    sigma,
    batch_rows_k,
    batch_failure_bits,
    mask_failure_bits,
    bit_source,
    max_enclosure_bits=512,
    max_entries=2000000,
):
    """Execute complete sign/mask + k-dither sampling and feed refresh_node on success."""
    raw = original_bank(records)
    m = len(raw)
    n = len(raw[0].label)
    budget = batch_sampler_budget(n, m, batch_rows_k, g, sigma, batch_failure_bits, mask_failure_bits)
    per_draw_f = budget["per_draw_failure_bits_f"]
    tape = bit_source if isinstance(bit_source, BitTape) else BitTape(bit_source)
    start_pos = tape.position

    sm_report = sample_uniform_signs_and_mask(n, m, batch_rows_k, g, mask_failure_bits, tape)
    dither_receipts = []
    cdf_cache = {}
    aborted = sm_report["status"] != "CERTIFIED_UNIFORM_SIGNS_AND_MASK"
    abort_reason = sm_report["status"] if aborted else None

    if not aborted:
        for draw_idx in range(batch_rows_k):
            draw = sample_rounded_gaussian_dither(
                sigma,
                per_draw_f,
                tape,
                max_enclosure_bits=max_enclosure_bits,
                cdf_cache=cdf_cache,
            )
            dither_receipts.append({
                "draw_index": draw_idx,
                **draw,
            })
            if draw["status"] != "CERTIFIED_ROUNDED_GAUSSIAN_SAMPLE":
                aborted = True
                abort_reason = f"DITHER_DRAW_{draw_idx}_{draw['status']}"
                break

    if aborted:
        return {
            "status": "ABORTED_COMPLETE_REFRESH_BATCH_DIAGNOSTIC_ONLY",
            "abort_reason": abort_reason,
            "batch_sampler_budget": budget,
            "signs_and_mask_sampling": sm_report,
            "dither_draw_receipts": tuple(dither_receipts),
            "completed_dither_draws": sum(
                1 for d in dither_receipts if d["status"] == "CERTIFIED_ROUNDED_GAUSSIAN_SAMPLE"
            ),
            "total_random_bits_consumed": tape.position - start_pos,
            "refresh_transform": None,
            "producer_input": None,
            "shortened_batch_emitted_as_valid_source": False,
            "fresh_public_randomness_is_a_fresh_original_sample": False,
            "actual_quantum_decision_or_multiple_producer_supplied": False,
        }

    dithers = tuple(d["sampled_integer"] for d in dither_receipts)
    transform = refresh_node(
        raw,
        g,
        prefix,
        sm_report["sign_rows"],
        sm_report["secret_mask"],
        dithers,
        max_entries=max_entries,
    )
    return {
        "status": "CERTIFIED_COMPLETE_REFRESH_BATCH_READY_FOR_EXTERNAL_PRODUCER",
        "abort_reason": None,
        "batch_sampler_budget": budget,
        "signs_and_mask_sampling": sm_report,
        "dither_draw_receipts": tuple(dither_receipts),
        "completed_dither_draws": len(dither_receipts),
        "total_random_bits_consumed": tape.position - start_pos,
        "refresh_transform": transform,
        "producer_input": transform["producer_input"],
        "shortened_batch_emitted_as_valid_source": False,
        "fresh_public_randomness_is_a_fresh_original_sample": False,
        "actual_quantum_decision_or_multiple_producer_supplied": False,
    }


def deterministic_bit_stream(seed_tag, count):
    """Generate a reproducible bit list from SHA-256 counter blocks for test/control fixtures."""
    bits = []
    block_idx = 0
    while len(bits) < count:
        digest_bytes = hashlib.sha256(f"{seed_tag}:{block_idx}".encode("utf-8")).digest()
        for byte in digest_bytes:
            for shift in range(7, -1, -1):
                bits.append((byte >> shift) & 1)
                if len(bits) == count:
                    break
            if len(bits) == count:
                break
        block_idx += 1
    return tuple(bits)


def build_single_draw_controls():
    """Build negative, zero, positive, and giant-width single-draw controls."""
    # Control 1: sigma = 5/2, f = 4 -> B = 10, K = 12
    # Prefix [0, 0, 1, 0, ...] ~ 0.125 -> negative integer outcome
    bits_neg = (0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1)
    draw_neg = sample_rounded_gaussian_dither("5/2", 4, bits_neg)

    # Prefix [1, 0, 0, 0, ...] ~ 0.5 -> zero integer outcome
    bits_zero = (1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0)
    draw_zero = sample_rounded_gaussian_dither("5/2", 4, bits_zero)

    # Prefix [1, 1, 1, 0, ...] ~ 0.875 -> positive integer outcome
    bits_pos = (1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1)
    draw_pos = sample_rounded_gaussian_dither("5/2", 4, bits_pos)

    # Giant rational width beyond 2^53: sigma = 3^40 / 7, f = 6
    giant_sigma = Fraction(3 ** 40, 7)
    giant_params = dither_draw_parameters(giant_sigma, 6)
    bits_giant = deterministic_bit_stream("giant-sigma-control", giant_params["active_dyadic_bits_K"])
    draw_giant = sample_rounded_gaussian_dither(giant_sigma, 6, bits_giant)

    return (
        {"control_id": "negative_integer_draw", "draw": draw_neg},
        {"control_id": "zero_integer_draw", "draw": draw_zero},
        {"control_id": "positive_integer_draw", "draw": draw_pos},
        {"control_id": "giant_sigma_beyond_2_pow_53_draw", "draw": draw_giant},
    )


def build_abort_and_trap_falsifiers():
    """Build forced left-tail, right-tail, uniform-precision, numerical-cap, and batch aborts."""
    tail_params = dither_draw_parameters("16", 1)
    K_tail = tail_params["active_dyadic_bits_K"]
    # Left tail abort: all-zero prefix puts U in [0, 2^-K_tail] <= F(-B-1) for sigma=16, f=1 (B=16, K=10)
    left_tail = sample_rounded_gaussian_dither("16", 1, (0,) * K_tail)
    # Right tail abort: all-one prefix puts U in [1 - 2^-K_tail, 1] >= F(B)
    right_tail = sample_rounded_gaussian_dither("16", 1, (1,) * K_tail)

    params = dither_draw_parameters("3/2", 1)
    K = params["active_dyadic_bits_K"]
    # Uniform-prefix precision abort: pick the K-bit cell containing F(0)_lower
    cdf0 = gaussian_cdf_box("3/2", 0, K)
    cell_idx = int(Fraction(cdf0["lower"]) * (2 ** K))
    straddle_bits = tuple((cell_idx >> (K - 1 - j)) & 1 for j in range(K))
    precision_abort = sample_rounded_gaussian_dither("3/2", 1, straddle_bits)

    # Numerical precision cap abort: set max_enclosure_bits = 4 < K
    numerical_abort = sample_rounded_gaussian_dither("3/2", 1, (1, 0) * (K // 2), max_enclosure_bits=4)

    # Adaptive-threshold precision trap regression across increasing widths
    trap_profiles = []
    for sig_str in ("3/2", "81", str(3 ** 20), str(3 ** 40)):
        p = dither_draw_parameters(sig_str, 8)
        trap_profiles.append({
            "sigma": p["sigma"],
            "truncation_bound_B": p["truncation_bound_B"],
            "dyadic_bits_K": p["active_dyadic_bits_K"],
            "total_thresholds_2B_plus_2": p["total_binary_search_thresholds_2B_plus_2"],
            "single_path_queries": p["max_single_path_queries_ceil_log2_2B_plus_1_plus_2"],
            "adaptive_all_threshold_union_upper": p["adaptive_all_threshold_precision_abort_upper"],
            "naive_query_count_bound_DO_NOT_USE": p["naive_query_count_precision_bound_DO_NOT_USE"],
            "adaptive_over_naive_multiplier": p["adaptive_over_naive_threshold_multiplier"],
        })

    # Complete-batch abort diagnostic: 2nd dither draw hits uniform precision abort
    q = 3 ** 16
    g = 81
    L = q // g
    s = (3 ** 15 + 17123, 3 ** 14 + 28114)
    errors = (L + 2, -L - 1, 0, 4, -3)
    raw = tuple(
        NoisyLinearRecord((j + 2, 3 * j + 1), ((j + 2) * s[0] + (3 * j + 1) * s[1] + e) % q, q, f"batch-src:{j}")
        for j, e in enumerate(errors)
    )
    prefix = tuple(x % L for x in s)
    # For batch_rows_k=2, batch_failure_bits=2 -> per_draw_f = 3.
    # Let's construct a bit tape where signs + mask + dither 0 succeed, and dither 1 hits straddle cell at F(0).
    b_budget = batch_sampler_budget(2, 5, 2, g, "3/2", 2, 4)
    K_batch = b_budget["single_dither_draw_parameters"]["active_dyadic_bits_K"]
    cdf0_batch = gaussian_cdf_box("3/2", 0, K_batch)
    straddle_idx_b = int(Fraction(cdf0_batch["lower"]) * (2 ** K_batch))
    straddle_bits_b = tuple((straddle_idx_b >> (K_batch - 1 - j)) & 1 for j in range(K_batch))
    # 10 sign bits + 2 * 7 mask bits (0000001 = 1 < 81) + 1 bit for dither 0 (1 -> [1/2, 1), then 0s -> t=0)
    dither0_bits = (1,) + (0,) * (K_batch - 1)
    # Wait: let's check how many bits dither 0 actually consumes!
    d0_test = sample_rounded_gaussian_dither("3/2", 3, dither0_bits)
    d0_consumed = dither0_bits[: d0_test["bits_consumed"]]
    sign_and_mask_bits = (1, 0, 1, 1, 0, 0, 1, 0, 1, 1) + (0, 0, 0, 0, 0, 0, 1) * 2
    aborted_batch = certified_refresh_batch(
        raw,
        g,
        prefix,
        "3/2",
        2,
        2,
        4,
        sign_and_mask_bits + d0_consumed + straddle_bits_b,
    )

    return {
        "forced_left_tail_abort": left_tail,
        "forced_right_tail_abort": right_tail,
        "forced_uniform_prefix_precision_abort": precision_abort,
        "forced_numerical_precision_cap_abort": numerical_abort,
        "adaptive_threshold_trap_regression": tuple(trap_profiles),
        "forced_complete_batch_abort_diagnostic": aborted_batch,
    }


def build_integrated_refresh_controls():
    """Build complete-batch source-refresh controls and coupled source_ledger profiles."""
    q = 3 ** 16
    g = 81
    L = q // g
    s = (3 ** 15 + 17123, 3 ** 14 + 28114)
    errors = (L + 2, -L - 1, 0, 4, -3)
    raw = tuple(
        NoisyLinearRecord((j + 2, 3 * j + 1), ((j + 2) * s[0] + (3 * j + 1) * s[1] + e) % q, q, f"refresh-original:{j}")
        for j, e in enumerate(errors)
    )
    prefix = tuple(x % L for x in s)
    bits = deterministic_bit_stream("certified-refresh-batch-control", 512)
    batch = certified_refresh_batch(
        raw,
        g,
        prefix,
        "9/2",
        3,
        6,
        8,
        bits,
    )
    if batch["status"] != "CERTIFIED_COMPLETE_REFRESH_BATCH_READY_FOR_EXTERNAL_PRODUCER":
        raise ArithmeticError("integrated refresh batch control unexpectedly aborted")

    # Coupled scaling profiles feeding native_source_refresh.source_ledger
    coupled_profiles = []
    for n, dmin, dmax, power in ((32, 8, 9, 9), (32, 8, 9, 16), (128, 12, 14, 16)):
        k = n * 9 * n.bit_length()
        m = n ** 3
        g_max = 3 ** dmax
        alpha_targ = Fraction(1, n)
        sigma_max = alpha_targ * g_max
        sampler = batch_sampler_budget(n, m, k, g_max, sigma_max, 24, 24)
        ledger = source_ledger(
            n,
            n,
            m,
            k,
            dmin,
            dmax,
            Fraction(1, n ** power),
            alpha_targ,
            Fraction(1, n ** 3),
            Fraction(1, n ** 3),
            ideal_producer_success="1/8",
            sampler_TV_loss=sampler["certified_complete_dither_sampler_TV_loss"],
        )
        coupled_profiles.append({
            "dimension": n,
            "dmin": dmin,
            "dmax": dmax,
            "batch_sampler_budget": sampler,
            "coupled_source_refresh_ledger": ledger,
        })

    return {
        "complete_batch_control": {
            "original_records": tuple(r.public() for r in raw),
            "calibration_secret_FOR_DIAGNOSTIC_ONLY": s,
            "calibration_errors_FOR_DIAGNOSTIC_ONLY": errors,
            "batch_result": batch,
        },
        "coupled_source_refresh_profiles": tuple(coupled_profiles),
    }


def verify_probability_boxes(report):
    """Replay every Arb tail box in the report using FLINT/Arb."""
    replayed = 0

    def check_cdf_box(cdf):
        nonlocal replayed
        sig = _rational(cdf["continuous_Gaussian_width"])
        rad = _certificate_int(cdf["radius_index"])
        bits = cdf["enclosure_bits"]
        tail = cdf["underlying_tail_box"]
        if exact_json(gaussian_radius_box(sig, rad, bits)) != tail:
            raise ValueError("Arb tail box replay mismatch in gaussian_cdf_box")
        replayed += 1

    for ctrl in report["single_draw_controls"]:
        for comp in ctrl["draw"]["threshold_comparisons"]:
            check_cdf_box(comp["cdf_box"])

    for census in report["bounded_dyadic_prefix_censuses"]:
        for box in census["threshold_cdf_boxes"].values():
            check_cdf_box(box)

    fals = report["abort_and_trap_falsifiers"]
    for key in (
        "forced_left_tail_abort",
        "forced_right_tail_abort",
        "forced_uniform_prefix_precision_abort",
        "forced_numerical_precision_cap_abort",
    ):
        for comp in fals[key]["threshold_comparisons"]:
            check_cdf_box(comp["cdf_box"])
    for draw in fals["forced_complete_batch_abort_diagnostic"]["dither_draw_receipts"]:
        for comp in draw["threshold_comparisons"]:
            check_cdf_box(comp["cdf_box"])

    for draw in report["integrated_source_refresh"]["complete_batch_control"]["batch_result"]["dither_draw_receipts"]:
        for comp in draw["threshold_comparisons"]:
            check_cdf_box(comp["cdf_box"])

    return {
        "verified": True,
        "Arb_tail_boxes_replayed": replayed,
        "same_trusted_Arb_special_functions_reused": True,
        "independent_transcendental_certificate_supplied": False,
    }


def build_report():
    deps = (
        "native_basis_lottery.py",
        "native_classical_modulus_descent.py",
        "native_gaussian_quotient_completion.py",
        "native_small_multiple_completion.py",
        "native_source_refresh.py",
        "ternary_covariant_noise.py",
        "ternary_measured_lattice_decoder.py",
        "ternary_noise_degradation.py",
    )
    censuses = (
        complete_dyadic_prefix_census("3/2", 1, 7),
        complete_dyadic_prefix_census("5/3", 2, 8),
    )
    return {
        "status": "CERTIFIED_ROUNDED_GAUSSIAN_DITHER_SAMPLER_AND_BATCH_COUPLING_REVIEW_PENDING",
        "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
        "contract_sha256": hashlib.sha256(CONTRACT.read_bytes()).hexdigest(),
        "dependency_sha256": {
            f: hashlib.sha256((ROOT / "theorems" / f).read_bytes()).hexdigest() for f in deps
        },
        "single_draw_controls": build_single_draw_controls(),
        "bounded_dyadic_prefix_censuses": censuses,
        "abort_and_trap_falsifiers": build_abort_and_trap_falsifiers(),
        "integrated_source_refresh": build_integrated_refresh_controls(),
        "source_refresh_dither_sampler_implemented": True,
        "source_conditioned_producer_amplification_established": False,
        "actual_quantum_decision_or_multiple_producer_supplied": False,
        "independent_transcendental_certificate_supplied": False,
        "accepted_speedup_candidate": False,
        "new_active_negative_result_created": False,
        "novelty_claim": False,
        "research_decision": "USE_CERTIFIED_ADAPTIVE_THRESHOLD_DITHER_AND_MASK_SAMPLER_FOR_REFRESH_BATCHES_EXTERNAL_PRODUCER_STILL_REQUIRED",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check-probabilities", action="store_true")
    args = parser.parse_args()
    if args.check_probabilities:
        print(json.dumps(verify_probability_boxes(json.loads(REPORT.read_text())), indent=2))
        return
    rep = build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(rep), indent=2) + "\n")
    print(
        json.dumps(
            {
                "status": rep["status"],
                "single_draw_outcomes": [
                    c["draw"]["sampled_integer"] for c in rep["single_draw_controls"]
                ],
                "censused_dyadic_cells": sum(
                    c["total_dyadic_cells_censused"] for c in rep["bounded_dyadic_prefix_censuses"]
                ),
                "complete_batch_dithers": [
                    d["sampled_integer"]
                    for d in rep["integrated_source_refresh"]["complete_batch_control"]["batch_result"]["dither_draw_receipts"]
                ],
                "actual_quantum_producer_supplied": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
