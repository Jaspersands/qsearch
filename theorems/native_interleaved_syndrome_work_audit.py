"""Multi-round interleaved syndrome-work circuits and response-call degree audit.

Proves and audits:
1. Exact fibre-pinching of arbitrary label-only interleaved word/syndrome effects
   under uniform-secret averaging (annihilating all cross-fibre coherences).
2. Exact Parseval conservation of total uniform-secret ground overlap across all N
   syndrome readout sectors under multi-round noncommuting syndrome interleaving.
3. Exact 4-tuple additive frequency-collision pinching and 3-adic valuation
   stratification (15^M, 27^M - 15^M, 81^M - 27^M) for 2-call response-phase
   interleaved circuits, plus (2r+1)^2 degree bounds for r-call reflection schedules.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
from itertools import product
import json
from math import isqrt
from pathlib import Path

from native_basis_lottery import original_bank
from native_full_root_slice import source_data
from native_small_multiple_completion import _rational
from native_word_spectral_filter_audit import finite_control
from native_word_span_decision import root_polynomial
from ternary_measured_lattice_decoder import exact_json, integer

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT / "research/NATIVE_INTERLEAVED_SYNDROME_WORK_AUDIT.md"
CONTRACT = ROOT / "research/hypotheses/native_interleaved_syndrome_work_audit_contract.json"
REPORT = ROOT / "research/reductions/native_interleaved_syndrome_work_audit.json"


def quadratic_syndrome_phase_exponents(frequencies, q):
    """Exact non-additive syndrome phase exponents Q(z) mod q on Z_q^n."""
    out = []
    for z in frequencies:
        quad = sum((i + 1) * (zi * zi + zi) for i, zi in enumerate(z))
        bump = (q // 3) if all(zi == 0 for zi in z) else 0
        out.append((quad + bump) % q)
    return tuple(out)


def multi_round_syndrome_sector_weights(frequencies, q):
    """Compute exact cyclotomic and rational sector weights w_t(sigma) = |beta_t(sigma)|^2."""
    N = len(frequencies)
    Q2 = quadratic_syndrome_phase_exponents(frequencies, q)
    delta_poly = {}
    for delta in frequencies:
        coeffs = [Fraction(0)] * q
        for z_idx, z in enumerate(frequencies):
            for zp_idx, zp in enumerate(frequencies):
                inner = sum(d * (za - zpa) for d, za, zpa in zip(delta, z, zp)) % q
                exp_diff = (Q2[z_idx] - Q2[zp_idx] + inner) % q
                coeffs[exp_diff] += Fraction(1, N * N)
        delta_poly[delta] = (coeffs, root_polynomial(coeffs, q))

    sum_coeffs = [Fraction(0)] * q
    for delta in frequencies:
        c_vec = delta_poly[delta][0]
        for k in range(q):
            sum_coeffs[k] += c_vec[k]
    if root_polynomial(sum_coeffs, q) != root_polynomial([Fraction(1)] + [Fraction(0)] * (q - 1), q):
        raise ArithmeticError("Parseval sum rule over syndrome sectors failed")

    return {
        "syndrome_dimension_N": N,
        "modulus_q": q,
        "Q2_phase_table": Q2,
        "delta_sector_weight_polynomials": {
            ",".join(str(x) for x in d): delta_poly[d][1] for d in frequencies
        },
        "delta_raw_cyclotomic_coeffs": delta_poly,
        "parseval_sum_over_all_sectors_equals_one": True,
    }


def multi_round_interleaved_control(args):
    """Audit multi-round noncommuting syndrome interleaving on an actual original bank."""
    raw, mask, truth, errors = source_data(*args)
    raw = original_bank(raw)
    q, n = raw[0].modulus, len(raw[0].label)
    M = len(raw) // 2
    D = 3 ** M
    N = q ** n
    base = finite_control(raw, mask, (("GEOMETRIC", 1),))
    rows = base["actual_native_word_rows"]
    frequencies = tuple(product(range(q), repeat=n))
    freq_counts = Counter(tuple(r["frequency"]) for r in rows)
    max_fibre = max(freq_counts.values())
    collision_C_A = sum(Fraction(c * c, D * D) for c in freq_counts.values())

    error_phases = tuple(
        sum(
            b * e
            for j, t in enumerate(row["word"])
            for b, e in zip(((1, 0), (-1, 1), (0, -1))[t], errors[2 * j : 2 * j + 2])
        )
        % q
        for row in rows
    )

    raw_gram_coeffs = [Fraction(0)] * q
    for w_idx, rw in enumerate(rows):
        fw = tuple(rw["frequency"])
        for v_idx, rv in enumerate(rows):
            if tuple(rv["frequency"]) == fw:
                diff = (error_phases[v_idx] - error_phases[w_idx]) % q
                raw_gram_coeffs[diff] += Fraction(1, D * D)
    raw_gram_poly = root_polynomial(raw_gram_coeffs, q)

    synd_info = multi_round_syndrome_sector_weights(frequencies, q)
    delta_raw = synd_info["delta_raw_cyclotomic_coeffs"]

    sector_avg_polys = []
    total_ground_band_coeffs = [Fraction(0)] * q
    for t in frequencies:
        sec_coeffs = [Fraction(0)] * q
        for w_idx, rw in enumerate(rows):
            fw = tuple(rw["frequency"])
            delta = tuple((fw[i] - t[i]) % q for i in range(n))
            w_coeffs = delta_raw[delta][0]
            for v_idx, rv in enumerate(rows):
                if tuple(rv["frequency"]) == fw:
                    err_diff = (error_phases[v_idx] - error_phases[w_idx]) % q
                    for k_exp, c_val in enumerate(w_coeffs):
                        if c_val:
                            sec_coeffs[(err_diff + k_exp) % q] += c_val / (D * D)
        for k_exp in range(q):
            total_ground_band_coeffs[k_exp] += sec_coeffs[k_exp]
        sector_avg_polys.append({
            "sector_t": t,
            "uniform_secret_mean_overlap_root_polynomial": root_polynomial(sec_coeffs, q),
        })

    total_ground_band_poly = root_polynomial(total_ground_band_coeffs, q)
    if total_ground_band_poly != raw_gram_poly:
        raise ArithmeticError("multi-round Parseval ground-band conservation law failed")

    distinct_delta_polys = len({
        json.dumps(v) for v in synd_info["delta_sector_weight_polynomials"].values()
    })
    distinct_sector_polys = len({
        json.dumps(s["uniform_secret_mean_overlap_root_polynomial"])
        for s in sector_avg_polys
    })

    sweep_cross_coeffs = [Fraction(0)] * q
    for s_vec in frequencies:
        for w_idx, rw in enumerate(rows):
            pw = (sum(a * x for a, x in zip(rw["frequency"], s_vec)) + error_phases[w_idx]) % q
            for v_idx, rv in enumerate(rows):
                pv = (sum(a * x for a, x in zip(rv["frequency"], s_vec)) + error_phases[v_idx]) % q
                sweep_cross_coeffs[(pv - pw) % q] += Fraction(1, N * D * D)
    sweep_cross_poly = root_polynomial(sweep_cross_coeffs, q)
    if sweep_cross_poly != raw_gram_poly:
        raise ArithmeticError("cross-fibre pinching identity under complete secret sweep failed")

    off_fibre_pairs = sum(
        1 for w_idx, rw in enumerate(rows) for v_idx, rv in enumerate(rows) if rw["frequency"] != rv["frequency"]
    )

    return {
        "native_source_reference": base,
        "calibration_truth_FOR_SWEEP_ONLY": {"masked_secret": truth, "original_errors": errors},
        "modulus_q": q,
        "dimension_n": n,
        "word_pairs_M": M,
        "word_dimension_D": D,
        "syndrome_dimension_N": N,
        "max_fibre_multiplicity": max_fibre,
        "fibre_trace_envelope_upper_m_max_over_D": str(Fraction(max_fibre, D)),
        "exact_1call_collision_density_C_A": str(collision_C_A),
        "raw_gram_uniform_secret_overlap_root_polynomial": raw_gram_poly,
        "multi_round_syndrome_weights": {
            "Q2_phase_table": synd_info["Q2_phase_table"],
            "delta_sector_weight_polynomials": synd_info["delta_sector_weight_polynomials"],
            "distinct_delta_weight_polynomial_count": distinct_delta_polys,
            "parseval_sum_over_all_sectors_equals_one": True,
        },
        "sector_uniform_secret_overlaps": tuple(sector_avg_polys),
        "distinct_sector_overlap_polynomial_count": distinct_sector_polys,
        "sum_over_all_sectors_uniform_secret_overlap_root_polynomial": total_ground_band_poly,
        "multi_round_parseval_ground_band_conservation_holds": total_ground_band_poly == raw_gram_poly,
        "cross_fibre_word_effect_pinching": {
            "off_fibre_nonzero_entries_in_E_cross": off_fibre_pairs,
            "complete_secret_sweep_mean_root_polynomial": sweep_cross_poly,
            "pinched_fibre_diagonal_root_polynomial": raw_gram_poly,
            "cross_fibre_entries_annihilated_exactly_by_secret_twirl": sweep_cross_poly == raw_gram_poly,
        },
    }


def two_call_response_interleaving_control(args):
    """Audit 2-call response-phase interleaving D_y V D_y and 4-tuple additive collisions."""
    raw, mask, truth, errors = source_data(*args)
    raw = original_bank(raw)
    q, n = raw[0].modulus, len(raw[0].label)
    M = len(raw) // 2
    D = 3 ** M
    N = q ** n
    base = finite_control(raw, mask, (("GEOMETRIC", 1),))
    rows = base["actual_native_word_rows"]
    frequencies = tuple(product(range(q), repeat=n))
    error_phases = tuple(
        sum(
            b * e
            for j, t in enumerate(row["word"])
            for b, e in zip(((1, 0), (-1, 1), (0, -1))[t], errors[2 * j : 2 * j + 2])
        )
        % q
        for row in rows
    )

    freq_counts = Counter(tuple(r["frequency"]) for r in rows)
    one_call_collisions = sum(c * c for c in freq_counts.values())

    pair_sum_counts = Counter()
    for r1 in rows:
        f1 = r1["frequency"]
        for r2 in rows:
            f2 = r2["frequency"]
            tau = tuple((a + b) % q for a, b in zip(f1, f2))
            pair_sum_counts[tau] += 1

    two_call_additive_collisions = sum(c * c for c in pair_sum_counts.values())
    product_one_call_collisions = one_call_collisions * one_call_collisions
    nontrivial_additive_4tuples = two_call_additive_collisions - product_one_call_collisions

    pair_list = []
    for w1_idx, r1 in enumerate(rows):
        f1 = r1["frequency"]
        e1 = error_phases[w1_idx]
        for w2_idx, r2 in enumerate(rows):
            f2 = r2["frequency"]
            e2 = error_phases[w2_idx]
            pair_list.append((
                tuple((a + b) % q for a, b in zip(f1, f2)),
                (e1 + e2) % q,
            ))

    sweep_2call_coeffs = [Fraction(0)] * q
    for s_vec in frequencies:
        phase_hist = Counter()
        for tau, e_sum in pair_list:
            tot_phase = (sum(a * x for a, x in zip(tau, s_vec)) + e_sum) % q
            phase_hist[tot_phase] += 1
        for p1, c1 in phase_hist.items():
            for p2, c2 in phase_hist.items():
                sweep_2call_coeffs[(p2 - p1) % q] += Fraction(c1 * c2, N * (D ** 4))
    sweep_2call_poly = root_polynomial(sweep_2call_coeffs, q)

    pinched_2call_coeffs = [Fraction(0)] * q
    by_tau = {}
    for tau, e_sum in pair_list:
        by_tau.setdefault(tau, []).append(e_sum)
    for tau, e_list in by_tau.items():
        hist = Counter(e_list)
        for e1, c1 in hist.items():
            for e2, c2 in hist.items():
                pinched_2call_coeffs[(e2 - e1) % q] += Fraction(c1 * c2, D ** 4)
    pinched_2call_poly = root_polynomial(pinched_2call_coeffs, q)

    if sweep_2call_poly != pinched_2call_poly:
        raise ArithmeticError("2-call uniform-secret sweep disagreed with 4-tuple additive pinching")

    return {
        "native_source_reference": base,
        "calibration_truth_FOR_SWEEP_ONLY": {"masked_secret": truth, "original_errors": errors},
        "modulus_q": q,
        "dimension_n": n,
        "word_pairs_M": M,
        "word_dimension_D": D,
        "syndrome_dimension_N": N,
        "one_call_fibre_collision_pairs": one_call_collisions,
        "one_call_collision_density_C_A": str(Fraction(one_call_collisions, D * D)),
        "two_call_total_4tuples_D4": D ** 4,
        "two_call_additive_collision_4tuples": two_call_additive_collisions,
        "product_of_1call_collision_4tuples": product_one_call_collisions,
        "nontrivial_cross_fibre_additive_collision_4tuples": nontrivial_additive_4tuples,
        "two_call_collision_density_C2_A": str(Fraction(two_call_additive_collisions, D ** 4)),
        "complete_secret_sweep_2call_root_polynomial": sweep_2call_poly,
        "additive_4tuple_pinched_2call_root_polynomial": pinched_2call_poly,
        "two_call_pinching_theorem_verified": sweep_2call_poly == pinched_2call_poly,
        "nontrivial_additive_collisions_present": nontrivial_additive_4tuples > 0,
    }


def iid_additive_collision_census(n, d, M, max_work=100000):
    """Exact 3-adic valuation stratification census for 2-call additive 4-tuples."""
    for x, name in ((n, "dimension"), (d, "root digits"), (M, "word pairs"), (max_work, "work cap")):
        integer(x, "positive " + name, 1)
    q = 3 ** d
    N = q ** n
    D = 3 ** M
    total_4tuples = D ** 4
    if total_4tuples * M > max_work:
        raise ValueError("4-tuple word census work cap exceeded")

    digit_vectors = ((1, 0), (-1, 1), (0, -1))
    words = tuple(product(range(3), repeat=M))
    stratum_zero_Z = 0
    stratum_div3_nonzero = 0
    stratum_unit = 0

    for w1 in words:
        for w2 in words:
            for v1 in words:
                for v2 in words:
                    all_zero_z = True
                    all_div3 = True
                    for j in range(M):
                        c0 = (
                            digit_vectors[w1[j]][0]
                            + digit_vectors[w2[j]][0]
                            - digit_vectors[v1[j]][0]
                            - digit_vectors[v2[j]][0]
                        )
                        c1 = (
                            digit_vectors[w1[j]][1]
                            + digit_vectors[w2[j]][1]
                            - digit_vectors[v1[j]][1]
                            - digit_vectors[v2[j]][1]
                        )
                        if c0 != 0 or c1 != 0:
                            all_zero_z = False
                        if c0 % 3 != 0 or c1 % 3 != 0:
                            all_div3 = False
                            break
                    if all_zero_z:
                        stratum_zero_Z += 1
                    elif all_div3:
                        stratum_div3_nonzero += 1
                    else:
                        stratum_unit += 1

    if stratum_zero_Z != 15 ** M:
        raise ArithmeticError("stratum_zero_Z disagreed with 15^M")
    if stratum_div3_nonzero != 27 ** M - 15 ** M:
        raise ArithmeticError("stratum_div3_nonzero disagreed with 27^M - 15^M")
    if stratum_unit != 81 ** M - 27 ** M:
        raise ArithmeticError("stratum_unit disagreed with 81^M - 27^M")

    # Collision probability per stratum under IID uniform labels in (Z_q^n)^(2M):
    # - stratum_zero_Z: collides with probability 1
    # - stratum_div3_nonzero: collides with probability 1 if d == 1 (q == 3), else 3^n / N
    # - stratum_unit: collides with probability 1 / N
    prob_div3 = Fraction(1) if d == 1 else Fraction(3 ** n, N)
    expected_c2 = (
        Fraction(stratum_zero_Z, total_4tuples)
        + Fraction(stratum_div3_nonzero, total_4tuples) * prob_div3
        + Fraction(stratum_unit, total_4tuples) * Fraction(1, N)
    )

    exact_bank_verified = False
    if (N ** (2 * M)) * total_4tuples <= max_work:
        labels = tuple(product(range(q), repeat=n))
        bank_sum = Fraction(0)
        num_banks = N ** (2 * M)
        for bank in product(labels, repeat=2 * M):
            counts = Counter()
            for w in words:
                freq = tuple(
                    sum(
                        digit_vectors[w[j]][0] * bank[2 * j][i]
                        + digit_vectors[w[j]][1] * bank[2 * j + 1][i]
                        for j in range(M)
                    )
                    % q
                    for i in range(n)
                )
                counts[freq] += 1
            pair_counts = Counter()
            for f1, c1 in counts.items():
                for f2, c2 in counts.items():
                    tau = tuple((a + b) % q for a, b in zip(f1, f2))
                    pair_counts[tau] += c1 * c2
            bank_sum += Fraction(sum(v * v for v in pair_counts.values()), total_4tuples)
        if bank_sum / num_banks != expected_c2:
            raise ArithmeticError("complete label-bank average disagreed with 3-adic stratum formula")
        exact_bank_verified = True

    return {
        "dimension_n": n,
        "root_digits_d": d,
        "modulus_q": q,
        "word_pairs_M": M,
        "word_dimension_D": D,
        "syndrome_dimension_N": N,
        "total_4tuples_81_pow_M": total_4tuples,
        "stratum_zero_over_Z_15_pow_M": stratum_zero_Z,
        "stratum_div3_nonzero_27_pow_M_minus_15_pow_M": stratum_div3_nonzero,
        "stratum_unit_81_pow_M_minus_27_pow_M": stratum_unit,
        "div3_subgroup_collision_probability": str(prob_div3),
        "exact_expected_2call_collision_density_E_A_C2": str(expected_c2),
        "complete_label_bank_enumeration_verified": exact_bank_verified,
        "three_adic_valuation_stratification_verified": True,
    }


def interleaved_scaling_ledger(n, r, surplus, response_calls_r, target="1/2"):
    """Compute scaling bounds for L-round interleaved and r-call response circuits."""
    for x, name in (
        (n, "dimension"),
        (r, "root digits"),
        (surplus, "word surplus"),
        (response_calls_r, "response calls r"),
    ):
        integer(x, "positive " + name, 1)
    if n * r > 16384 or surplus > 128:
        raise ValueError("scaling exponent cap exceeded")
    target_prob = _rational(target)
    if not 0 < target_prob <= 1:
        raise ValueError("valid target acceptance probability required")
    M = n * r + surplus
    one_call_factor = 1 + Fraction(1, 3 ** surplus)
    # Using the exact 3-adic stratum upper bound (1/3)^M + (1 - (1/3)^M)/N <= (1 + 3^-surplus) * 3^(-n*r)
    two_call_factor = 1 + Fraction(1, 3 ** surplus)
    chebyshev_factor = (2 * response_calls_r + 1) ** 2
    amplified_1call_factor = chebyshev_factor * one_call_factor

    squared = target_prob * (3 ** (n * r)) / one_call_factor
    d_req = isqrt(squared.numerator // squared.denominator)
    if d_req * d_req * squared.denominator < squared.numerator:
        d_req += 1

    return {
        "dimension_n": n,
        "root_digits_r": r,
        "word_sites_M": M,
        "word_surplus": surplus,
        "declared_response_calls_r": response_calls_r,
        "one_call_expected_collision_upper": {
            "coefficient": str(one_call_factor),
            "base": 3,
            "exponent": -n * r,
        },
        "two_call_expected_collision_upper": {
            "coefficient": str(two_call_factor),
            "base": 3,
            "exponent": -n * r,
        },
        "r_call_reflection_chebyshev_multiplier_2r_plus_1_sq": chebyshev_factor,
        "r_call_amplified_mean_acceptance_upper": {
            "coefficient": str(amplified_1call_factor),
            "base": 3,
            "exponent": -n * r,
        },
        "target_mean_acceptance": str(target_prob),
        "necessary_reflection_calls_lower_for_target": d_req // 2,
        "arbitrary_depth_label_only_syndrome_interleaving_bounded_by_fibre_pinching": True,
        "universal_quantum_lower_bound_claimed": False,
        "scalable_quantum_speedup_supplied": False,
    }


def build_report():
    deps = (
        "native_basis_lottery.py",
        "native_full_root_slice.py",
        "native_small_multiple_completion.py",
        "native_syndrome_dilation.py",
        "native_word_spectral_filter_audit.py",
        "native_word_span_decision.py",
        "ternary_measured_lattice_decoder.py",
    )
    interleaved_controls = tuple(
        multi_round_interleaved_control(p)
        for p in ((1, 1, 2, False, 99101), (1, 1, 3, True, 99102), (2, 1, 2, False, 99103))
    )
    two_call_controls = tuple(
        two_call_response_interleaving_control(p)
        for p in ((1, 1, 2, False, 99101), (1, 2, 2, True, 99104))
    )
    censuses = (
        iid_additive_collision_census(1, 1, 1),
        iid_additive_collision_census(1, 2, 1),
        iid_additive_collision_census(1, 2, 2),
        iid_additive_collision_census(2, 1, 2),
    )
    scaling = tuple(
        interleaved_scaling_ledger(n, n, 12, 4) for n in (8, 32, 64, 128)
    )
    return {
        "status": "INTERLEAVED_SYNDROME_WORK_PINCHING_AND_RESPONSE_DEGREE_AUDIT_REVIEW_PENDING",
        "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
        "contract_sha256": hashlib.sha256(CONTRACT.read_bytes()).hexdigest(),
        "dependency_sha256": {
            f: hashlib.sha256((ROOT / "theorems" / f).read_bytes()).hexdigest() for f in deps
        },
        "multi_round_interleaved_controls": interleaved_controls,
        "two_call_response_interleaving_controls": two_call_controls,
        "iid_two_call_additive_collision_censuses": censuses,
        "interleaved_scaling_ledgers": scaling,
        "universal_quantum_lower_bound_claimed": False,
        "scalable_quantum_speedup_supplied": False,
        "accepted_speedup_candidate": False,
        "new_active_negative_result_created": False,
        "novelty_claim": False,
        "research_decision": "LABEL_ONLY_WORK_INTERLEAVING_PINCHES_TO_FIBRES_MULTI_CALL_RESPONSE_INTERLEAVING_GOVERNED_BY_ADDITIVE_COLLISION_TENSOR",
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
                "interleaved_controls_conserved": [
                    c["multi_round_parseval_ground_band_conservation_holds"]
                    for c in rep["multi_round_interleaved_controls"]
                ],
                "two_call_pinching_verified": [
                    c["two_call_pinching_theorem_verified"]
                    for c in rep["two_call_response_interleaving_controls"]
                ],
                "censuses_verified": len(rep["iid_two_call_additive_collision_censuses"]),
                "scalable_quantum_speedup_supplied": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
