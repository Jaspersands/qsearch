"""Micciancio-Peikert prime-power search-to-decision adapter and sample expansion audit.

Proves and audits:
1. Exact p-adic Hensel subgroup-shift probe algebra for q = 3^r:
   a' = a + u * 3^(r-1-l) * e_j mod q, y' = y - <a, s_low> + u * 3^(r-1) * d + e_widen mod q.
2. Complete finite census of true-digit invariance, false-digit order-3 subgroup
   bijection {0, 3^(r-1), 2*3^(r-1)}, and false-lower-prefix failure across all d in {0,1,2}.
3. Coupled rounded-input Gaussian widening TV bound, certified adaptive-threshold
   dither sampler budget, and 2*n*r*R_rep*m_dec disjoint sample expansion ledger.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from math import isqrt
from pathlib import Path

from native_affine_fibre_relaxation import canonical_vector
from native_basis_lottery import _certificate_int, original_bank
from native_gaussian_dither_sampler import ceil_log2_int, dither_draw_parameters
from native_small_multiple_completion import _rational
from native_word_span_decision import prime_power_route
from ternary_covariant_noise import root_digits
from ternary_measured_lattice_decoder import exact_json, integer
from ternary_noise_degradation import NoisyLinearRecord

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT / "research/NATIVE_MP12_PRIME_POWER_SEARCH_TO_DECISION_AUDIT.md"
CONTRACT = ROOT / "research/hypotheses/native_mp12_prime_power_search_to_decision_audit_contract.json"
REPORT = ROOT / "research/reductions/native_mp12_prime_power_search_to_decision_audit.json"


def hensel_digit_probe_record(record, level_l, coord_j, s_low, candidate_digit_d, probe_u, widen_dither=0):
    """Apply the MP12 prime-power coordinate-digit probe to a single original record."""
    if not isinstance(record, NoisyLinearRecord):
        record = NoisyLinearRecord(**record)
    q = record.modulus
    r = root_digits(q)
    n = len(record.label)
    integer(level_l, "nonnegative Hensel level l", 0)
    integer(coord_j, "nonnegative coordinate index j", 0)
    integer(candidate_digit_d, "candidate ternary digit d", 0)
    integer(probe_u, "ternary probe multiplier u", 0)
    if level_l >= r or coord_j >= n or candidate_digit_d >= 3 or probe_u >= 3:
        raise ValueError("valid level l < r, coord j < n, and ternary d, u in {0,1,2} required")
    if type(widen_dither) is not int:
        raise ValueError("exact integer widening dither required")
    scale_low = 3 ** level_l
    s_low_vec = canonical_vector(s_low, n, scale_low) if level_l > 0 else (0,) * n
    if level_l == 0 and tuple(s_low) != (0,) * n:
        raise ValueError("level-0 lower prefix must be the zero vector")

    shift_a = (probe_u * (3 ** (r - 1 - level_l))) % q
    new_label = tuple(
        (a_val + (shift_a if idx == coord_j else 0)) % q
        for idx, a_val in enumerate(record.label)
    )
    prefix_dot = sum(a_val * p_val for a_val, p_val in zip(record.label, s_low_vec)) % q
    shift_y = (probe_u * (3 ** (r - 1)) * candidate_digit_d) % q
    new_value = (record.value - prefix_dot + shift_y + widen_dither) % q

    return {
        "modulus_q": q,
        "root_digits_r": r,
        "dimension_n": n,
        "level_l": level_l,
        "coordinate_j": coord_j,
        "known_lower_prefix_s_low": s_low_vec,
        "candidate_digit_d": candidate_digit_d,
        "probe_multiplier_u": probe_u,
        "widen_dither": widen_dither,
        "probed_record": NoisyLinearRecord(
            new_label, new_value, q, f"{record.source_id}:mp12:l{level_l}:j{coord_j}:d{candidate_digit_d}:u{probe_u}"
        ).public(),
    }


def hensel_digit_probe_batch(records, level_l, coord_j, s_low, candidate_digit_d, probe_u_list, widen_dithers):
    """Apply the MP12 coordinate-digit probe across a batch of original records."""
    raw = original_bank(records)
    m = len(raw)
    u_tuple = tuple(probe_u_list)
    dither_tuple = tuple(widen_dithers)
    if len(u_tuple) != m or len(dither_tuple) != m:
        raise ValueError("probe_u_list and widen_dithers must match record count m")
    probed = []
    receipts = []
    for idx, (rec, u_val, e_w) in enumerate(zip(raw, u_tuple, dither_tuple)):
        pr = hensel_digit_probe_record(rec, level_l, coord_j, s_low, candidate_digit_d, u_val, e_w)
        probed.append(pr["probed_record"])
        receipts.append({
            "row_index": idx,
            "original_source_id": rec.source_id,
            "probe_u": u_val,
            "widen_dither": e_w,
            "probed_record": pr["probed_record"],
        })
    return {
        "modulus_q": raw[0].modulus,
        "dimension_n": len(raw[0].label),
        "batch_rows_m": m,
        "level_l": level_l,
        "coordinate_j": coord_j,
        "known_lower_prefix_s_low": tuple(s_low),
        "candidate_digit_d": candidate_digit_d,
        "probed_records": tuple(probed),
        "probe_receipts": tuple(receipts),
        "original_records_paid_once": m,
        "fresh_probe_randomness_is_a_fresh_original_sample": False,
    }


def complete_hensel_subgroup_census(r, level_l):
    """Exhaustively census all secret digits, candidate digits d, and probe multipliers u."""
    integer(r, "positive root digits r", 2)
    integer(level_l, "nonnegative Hensel level l", 0)
    if level_l >= r or r > 6:
        raise ValueError("0 <= level_l < r <= 6 required for complete subgroup census")
    q = 3 ** r
    top_subgroup = (0, 3 ** (r - 1), 2 * (3 ** (r - 1)))

    # Single-coordinate (n=1) complete census over all s in Z_q, a in Z_q, d in {0,1,2}
    true_hypothesis_checks = 0
    false_hypothesis_bijections = 0
    false_prefix_failures = 0

    for s in range(q):
        true_s_low = s % (3 ** level_l)
        s_upper = s // (3 ** level_l)
        true_digit = s_upper % 3
        for a in range(q):
            y = (a * s + 1) % q  # fixed error e = 1
            rec = NoisyLinearRecord((a,), y, q, f"census:{s}:{a}")
            for d in range(3):
                shifts = []
                for u in range(3):
                    pr = hensel_digit_probe_record(rec, level_l, 0, (true_s_low,), d, u, widen_dither=0)["probed_record"]
                    # Residual relative to remaining secret s - true_s_low = 3^l * s_upper
                    rem_secret = (s - true_s_low) % q
                    residual = (pr["value"] - pr["label"][0] * rem_secret) % q
                    shift = (residual - 1) % q
                    shifts.append(shift)
                if d == true_digit:
                    if tuple(shifts) != (0, 0, 0):
                        raise ArithmeticError("true digit hypothesis failed zero-shift invariance")
                    true_hypothesis_checks += 1
                else:
                    if tuple(sorted(shifts)) != top_subgroup:
                        raise ArithmeticError("false digit hypothesis failed order-3 subgroup bijection")
                    false_hypothesis_bijections += 1

            # False lower-prefix countercontrol when level_l >= 1
            if level_l >= 1:
                wrong_s_low = (true_s_low + 1) % (3 ** level_l)
                rem_wrong = (s - wrong_s_low) % q
                any_d_invariant = False
                for d in range(3):
                    shifts_w = []
                    for u in range(3):
                        pr_w = hensel_digit_probe_record(rec, level_l, 0, (wrong_s_low,), d, u, widen_dither=0)["probed_record"]
                        res_w = (pr_w["value"] - pr_w["label"][0] * rem_wrong) % q
                        shifts_w.append((res_w - 1) % q)
                    if len(set(shifts_w)) == 1:
                        any_d_invariant = True
                if any_d_invariant:
                    raise ArithmeticError("false lower prefix unexpectedly had u-invariant residual")
                false_prefix_failures += 1

    return {
        "root_digits_r": r,
        "modulus_q": q,
        "hensel_level_l": level_l,
        "order_3_top_subgroup": top_subgroup,
        "secrets_and_labels_pairs_checked": q * q,
        "true_digit_zero_shift_invariance_checks": true_hypothesis_checks,
        "false_digit_subgroup_bijection_checks": false_hypothesis_bijections,
        "false_lower_prefix_all_d_noninvariant_checks": false_prefix_failures,
        "all_true_digits_preserve_error_law": True,
        "all_false_digits_biject_onto_order3_subgroup": True,
        "false_lower_prefix_invalidates_all_candidate_digits": level_l >= 1,
    }


def ceil_sqrt_fraction(frac):
    """Exact rational upper bound >= sqrt(frac) using integer square-root ceiling."""
    q = _rational(frac)
    if q < 0:
        raise ValueError("nonnegative fraction required for ceil_sqrt_fraction")
    if q == 0:
        return Fraction(0)
    # Write q = (num * den) / den^2; ceil(sqrt(num * den)) / den >= sqrt(q)
    prod_val = q.numerator * q.denominator
    s = isqrt(prod_val)
    if s * s < prod_val:
        s += 1
    return Fraction(s, q.denominator)


def mp12_coupled_reduction_ledger(
    n,
    r,
    decision_alpha,
    decision_rows_m,
    dither_failure_bits,
    total_recovery_failure_target="1/64",
    assumed_ideal_decision_advantage="1/2",
):
    """Compute coupled MP12 widening, dither-sampler, and disjoint sample expansion ledger."""
    for x, name in (
        (n, "dimension n"),
        (r, "root digits r"),
        (decision_rows_m, "decision rows m_dec"),
        (dither_failure_bits, "batch dither failure bits"),
    ):
        integer(x, "positive " + name, 1)
    base_route = prime_power_route(n, r, decision_alpha, decision_rows_m)
    q = 3 ** r
    h = base_route["smoothing_function_value"]
    a_dec = _rational(decision_alpha)
    a_search = _rational(base_route["search_continuous_D_alpha_width"])
    added2 = _rational(base_route["fresh_auxiliary_Gaussian_width_squared"])
    tv_sq = _rational(base_route["rounded_search_input_then_fresh_Gaussian_widening_TV_squared_upper"])
    tv_round_widen = min(Fraction(1), ceil_sqrt_fraction(tv_sq))

    # Conservative rational lower bound on continuous widening width sigma_widen = q * sqrt(a_dec^2 - a_search^2):
    # Since sqrt(1 - 1/h^4) >= 1 - 1/h^4 for h >= 2, sigma_widen_floor = q * a_dec * (1 - 1/h^4).
    sigma_widen_floor = q * a_dec * (1 - Fraction(1, h ** 4))
    per_draw_f = dither_failure_bits + ceil_log2_int(max(2, decision_rows_m))
    dither_params = dither_draw_parameters(sigma_widen_floor, per_draw_f)
    per_draw_loss = Fraction(dither_params["per_draw_coupling_loss_upper"])
    batch_sampler_loss = min(Fraction(1), decision_rows_m * per_draw_loss)

    gamma_ideal = _rational(assumed_ideal_decision_advantage)
    delta_tot = _rational(total_recovery_failure_target)
    if not 0 < gamma_ideal <= 1 or not 0 < delta_tot < 1:
        raise ValueError("valid ideal decision advantage and total failure target required")

    gamma_eff = max(Fraction(0), gamma_ideal - 2 * tv_round_widen - 2 * batch_sampler_loss)
    total_hypothesis_tests = 2 * n * r
    # Per-test failure target delta_step = delta_tot / (2*n*r)
    # Using ceil_log2(4*n*r / delta_tot) >= ln(2 / delta_step):
    inv_target = ceil_log2_int(int((Fraction(4 * n * r) / delta_tot).numerator // (Fraction(4 * n * r) / delta_tot).denominator) + 1)
    if gamma_eff > 0:
        rep_needed_frac = Fraction(2 * inv_target) / (gamma_eff * gamma_eff)
        reps_per_test = (rep_needed_frac.numerator + rep_needed_frac.denominator - 1) // rep_needed_frac.denominator
        if reps_per_test % 2 == 0:
            reps_per_test += 1
        total_decision_queries = total_hypothesis_tests * reps_per_test
        total_disjoint_samples = total_decision_queries * decision_rows_m
    else:
        reps_per_test = None
        total_decision_queries = None
        total_disjoint_samples = None

    return {
        "dimension_n": n,
        "root_digits_r": r,
        "modulus_q": q,
        "decision_rows_per_query_m_dec": decision_rows_m,
        "smoothing_parameter_h": h,
        "decision_continuous_width_alpha_dec": str(a_dec),
        "search_continuous_width_alpha_search": str(a_search),
        "widening_width_squared_alpha_dec_sq_minus_alpha_search_sq": str(added2),
        "rounded_input_widening_TV_squared_upper": str(tv_sq),
        "rounded_input_widening_TV_upper": str(tv_round_widen),
        "sigma_widen_rational_floor": str(sigma_widen_floor),
        "certified_dither_sampler_draw_parameters": dither_params,
        "per_query_dither_sampler_TV_loss_upper": str(batch_sampler_loss),
        "assumed_ideal_decision_advantage_EXTERNAL": str(gamma_ideal),
        "effective_decision_advantage_lower_after_widening_and_sampler": str(gamma_eff),
        "total_coordinate_level_hypothesis_tests_2nr": total_hypothesis_tests,
        "total_recovery_failure_target": str(delta_tot),
        "majority_repetitions_per_hypothesis_test": reps_per_test,
        "total_decision_oracle_queries": total_decision_queries,
        "total_disjoint_original_search_samples_required": total_disjoint_samples,
        "sample_expansion_multiplier_over_single_query_bank": (
            None if total_disjoint_samples is None else total_disjoint_samples // decision_rows_m
        ),
        "fixed_single_query_bank_suffices": False,
        "base_prime_power_route": base_route,
        "actual_decision_algorithm_supplied": False,
    }


def build_report():
    deps = (
        "native_affine_fibre_relaxation.py",
        "native_basis_lottery.py",
        "native_gaussian_dither_sampler.py",
        "native_small_multiple_completion.py",
        "native_word_span_decision.py",
        "ternary_covariant_noise.py",
        "ternary_measured_lattice_decoder.py",
        "ternary_noise_degradation.py",
    )
    # Multi-coordinate probe batch control
    q = 27
    s = (19, 14)  # base 3: 19 = 1 + 0*3 + 2*9; 14 = 2 + 1*3 + 1*9
    s_low_l1 = (19 % 3, 14 % 3)  # (1, 2)
    raw = (
        NoisyLinearRecord((4, 7), (4 * s[0] + 7 * s[1] + 1) % q, q, "mp12:0"),
        NoisyLinearRecord((11, 5), (11 * s[0] + 5 * s[1] - 1) % q, q, "mp12:1"),
        NoisyLinearRecord((2, 16), (2 * s[0] + 16 * s[1] + 0) % q, q, "mp12:2"),
    )
    # Level l=1, coordinate j=1: true digit of s[1]=14 at l=1 is (14 // 3) % 3 = 1
    true_batch = hensel_digit_probe_batch(raw, 1, 1, s_low_l1, 1, (0, 1, 2), (1, -1, 0))
    false_batch = hensel_digit_probe_batch(raw, 1, 1, s_low_l1, 2, (0, 1, 2), (1, -1, 0))

    censuses = (
        complete_hensel_subgroup_census(2, 0),
        complete_hensel_subgroup_census(2, 1),
        complete_hensel_subgroup_census(3, 1),
    )

    ledgers = tuple(
        mp12_coupled_reduction_ledger(n, n, Fraction(1, n ** 3), 2 * (n * n + 12), 16)
        for n in (8, 32, 64, 128)
    )

    return {
        "status": "MP12_PRIME_POWER_HENSEL_PROBE_AND_SAMPLE_EXPANSION_AUDIT_REVIEW_PENDING",
        "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
        "contract_sha256": hashlib.sha256(CONTRACT.read_bytes()).hexdigest(),
        "dependency_sha256": {
            f: hashlib.sha256((ROOT / "theorems" / f).read_bytes()).hexdigest() for f in deps
        },
        "hensel_probe_batch_control": {
            "original_records": tuple(r.public() for r in raw),
            "calibration_secret_FOR_DIAGNOSTIC_ONLY": s,
            "true_digit_probe_batch": true_batch,
            "false_digit_probe_batch": false_batch,
        },
        "complete_hensel_subgroup_censuses": censuses,
        "coupled_mp12_reduction_ledgers": ledgers,
        "actual_decision_algorithm_supplied": False,
        "fixed_single_query_bank_suffices": False,
        "worst_case_lattice_reduction_compatibility_established": False,
        "accepted_speedup_candidate": False,
        "new_active_negative_result_created": False,
        "novelty_claim": False,
        "research_decision": "PAY_DISJOINT_SAMPLE_EXPANSION_AND_CERTIFIED_DITHER_WIDENING_WHEN_USING_MP12_PRIME_POWER_SEARCH_TO_DECISION",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    rep = build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(rep), indent=2) + "\n")
    print(
        json.dumps(
            {
                "status": rep["status"],
                "subgroup_censuses": len(rep["complete_hensel_subgroup_censuses"]),
                "sample_expansion_multipliers": [
                    l["sample_expansion_multiplier_over_single_query_bank"]
                    for l in rep["coupled_mp12_reduction_ledgers"]
                ],
                "actual_decision_algorithm_supplied": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
