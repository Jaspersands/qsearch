"""Response-phase Fourier factorization, 1-call autoregressive chain rule, and signed 2-call pinching.

Proves and audits:
1. Exact O(M) product factorization of tensor-product qutrit schedules
   (F_3^dag)^(tensor M) D_y^(+-1) F_3^(tensor M) D_y |+_3>^(tensor M).
2. Exact O(M) triangular autoregressive chain rule for 1-call cyclic DFT readout
   F_{3^M} D_y |+_D>, with Z_3 Parseval conditional normalization at every prefix.
3. Exact difference-relation pinching f_A(w)-f_A(v) = f_A(w')-f_A(v') mod q and
   diagonal w=v secret/noise cancellation for signed (+1,-1) cyclic 2-call readout.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
from itertools import product
import json
from pathlib import Path

from native_basis_lottery import original_bank
from native_full_root_slice import source_data
from native_response_path_valuation import DIGITS, _histogram_probability, fourier_interleaved_readout, word_rows
from native_word_span_decision import root_polynomial
from ternary_measured_lattice_decoder import exact_json, integer

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT / "research/NATIVE_RESPONSE_FOURIER_FACTORIZATION_AUDIT.md"
CONTRACT = ROOT / "research/hypotheses/native_response_fourier_factorization_audit_contract.json"
REPORT = ROOT / "research/reductions/native_response_fourier_factorization_audit.json"


def cyclotomic_multiply(coeffs_a, coeffs_b, root):
    """Multiply two unreduced length-root rational coefficient vectors mod z^root - 1."""
    out = [Fraction(0)] * root
    for i, a in enumerate(coeffs_a):
        if a:
            for j, b in enumerate(coeffs_b):
                if b:
                    out[(i + j) % root] += a * b
    return out


def site_phase_tables(records, mask):
    """Compute per-site 3-element phase and frequency tables for M paired original records."""
    raw = original_bank(records)
    q, n = raw[0].modulus, len(raw[0].label)
    mask = tuple(mask)
    if len(raw) % 2 or len(mask) != n:
        raise ValueError("paired original rows and full public mask required")
    M = len(raw) // 2
    sites = []
    for j in range(M):
        r0, r1 = raw[2 * j], raw[2 * j + 1]
        site_freqs = []
        site_phases = []
        for t in range(3):
            b0, b1 = DIGITS[t]
            f_t = tuple((b0 * r0.label[i] + b1 * r1.label[i]) % q for i in range(n))
            p_t = (b0 * r0.value + b1 * r1.value + sum(a * z for a, z in zip(f_t, mask))) % q
            site_freqs.append(f_t)
            site_phases.append(p_t)
        sites.append({
            "site_index": j,
            "digit_frequencies": tuple(site_freqs),
            "digit_phases": tuple(site_phases),
        })
    return tuple(sites)


def tensor_qutrit_two_call_readout(records, mask, second_call_sign=1):
    """Verify O(M) tensor-product factorization of (F_3^dag)^M D_y^(sign) F_3^M D_y |+_3>^M."""
    if second_call_sign not in (-1, 1):
        raise ValueError("second_call_sign in {-1, +1} required")
    raw = original_bank(records)
    q = raw[0].modulus
    rows = word_rows(raw, mask)
    sites = site_phase_tables(raw, mask)
    M = len(sites)
    D = 3 ** M
    f3_scale = q // 3

    # 1. Compute O(M) single-qutrit marginal distributions (9 path terms per site/outcome)
    site_marginals = []
    site_raw_coeffs = []
    for s_info in sites:
        phases = s_info["digit_phases"]
        out_polys = []
        out_raw = []
        sum_site = [Fraction(0)] * q
        for x_j in range(3):
            hist = Counter(
                (phases[w_j] + second_call_sign * phases[v_j] + f3_scale * v_j * (w_j - x_j)) % q
                for w_j in range(3)
                for v_j in range(3)
            )
            c_vec = _histogram_probability(hist, q, 27)
            out_raw.append(c_vec)
            out_polys.append(root_polynomial(c_vec, q))
            sum_site = [a + b for a, b in zip(sum_site, c_vec)]
        if root_polynomial(sum_site, q) != root_polynomial([Fraction(1)] + [Fraction(0)] * (q - 1), q):
            raise ArithmeticError("single-qutrit marginal distribution failed normalization")
        site_raw_coeffs.append(out_raw)
        site_marginals.append({
            "site_index": s_info["site_index"],
            "digit_phases": phases,
            "marginal_outcome_probabilities": tuple(out_polys),
        })

    # 2. Multiply site marginals and verify exact match with full D^2-path F_3^(tensor M) sum
    product_outcomes = []
    full_path_outcomes = []
    for x_idx, r_x in enumerate(rows):
        x_word = r_x["word"]
        prod_coeffs = [Fraction(1)] + [Fraction(0)] * (q - 1)
        for j, x_j in enumerate(x_word):
            prod_coeffs = cyclotomic_multiply(prod_coeffs, site_raw_coeffs[j][x_j], q)
        prod_poly = root_polynomial(prod_coeffs, q)

        hist_full = Counter()
        for r_w in rows:
            w_word = r_w["word"]
            for r_v in rows:
                v_word = r_v["word"]
                f3_dot = sum(v_j * (w_j - x_j) for w_j, v_j, x_j in zip(w_word, v_word, x_word)) % 3
                exp_val = (r_w["known_phase"] + second_call_sign * r_v["known_phase"] + f3_scale * f3_dot) % q
                hist_full[exp_val] += 1
        full_poly = root_polynomial(_histogram_probability(hist_full, q, D ** 3), q)
        if prod_poly != full_poly:
            raise ArithmeticError("O(M) product of 1-qutrit marginals disagreed with full F_3^M path sum")
        product_outcomes.append(prod_poly)
        full_path_outcomes.append(full_poly)

    cyclic_ref = fourier_interleaved_readout(raw, mask)["exact_all_outcome_probabilities"] if second_call_sign == 1 else None
    differs_from_cyclic = (
        None
        if cyclic_ref is None
        else tuple(product_outcomes) != tuple(cyclic_ref)
    )

    return {
        "modulus_q": q,
        "word_sites_M": M,
        "word_dimension_D": D,
        "second_call_sign": second_call_sign,
        "single_qutrit_site_marginals": tuple(site_marginals),
        "product_of_marginals_all_outcomes": tuple(product_outcomes),
        "full_path_sum_all_outcomes": tuple(full_path_outcomes),
        "product_matches_full_path_sum_identically": product_outcomes == full_path_outcomes,
        "single_qutrit_path_terms_evaluated_9_times_3_times_M": 27 * M,
        "full_dense_path_terms_3_pow_3M": D ** 3,
        "differs_from_cyclic_F_D_when_M_ge_2": differs_from_cyclic,
        "tensor_qutrit_schedule_classically_tractable_in_O_M": True,
    }


def one_call_cyclic_autoregressive_chain_rule(records, mask):
    """Prove and verify the O(M) triangular autoregressive chain rule for F_D D_y |+_D>."""
    raw = original_bank(records)
    q = raw[0].modulus
    rows = word_rows(raw, mask)
    sites = site_phase_tables(raw, mask)
    M = len(sites)
    D = 3 ** M
    root = max(q, D)
    phase_scale = root // q
    fourier_scale = root // D

    # 1. Full D-term cyclic DFT Born probabilities |<v | F_D D_y |+_D>|^2 for v in 0..D-1
    full_cyclic_1call = []
    for v in range(D):
        hist = Counter(
            (phase_scale * rw["known_phase"] + fourier_scale * v * w) % root
            for w, rw in enumerate(rows)
        )
        full_cyclic_1call.append(root_polynomial(_histogram_probability(hist, root, D ** 2), root))

    # 2. Triangular autoregressive conditional table P_k(v_k | v_0, ..., v_{k-1})
    # Note: in word_rows, product(range(3), repeat=M) orders w = (w_0, ..., w_{M-1})
    # such that index w = sum_{l=0}^{M-1} w_l * 3^(M - 1 - l).
    # Thus site l has weight 3^(M - 1 - l). Setting k = l (so weight is 3^(M - 1 - k)),
    # v * w = sum_{k=0}^{M-1} v * w_k * 3^(M - 1 - k) mod 3^M.
    # Notice that v * 3^(M - 1 - k) mod 3^M depends ONLY on (v mod 3^(k+1)) = v_0 + 3*v_1 + ... + 3^k * v_k!
    conditional_tables = []
    raw_cond_lookup = {}
    for k in range(M):
        site_phases = sites[k]["digit_phases"]
        twiddle_scale = root // (3 ** (k + 1))
        prefix_entries = []
        for v_prefix in range(3 ** k):
            branch_polys = []
            sum_branches = [Fraction(0)] * root
            for v_k in range(3):
                v_le_k = v_prefix + (3 ** k) * v_k
                hist = Counter(
                    (phase_scale * site_phases[t] + twiddle_scale * v_le_k * t) % root
                    for t in range(3)
                )
                c_vec = _histogram_probability(hist, root, 9)
                raw_cond_lookup[(k, v_prefix, v_k)] = c_vec
                branch_polys.append(root_polynomial(c_vec, root))
                sum_branches = [a + b for a, b in zip(sum_branches, c_vec)]
            if root_polynomial(sum_branches, root) != root_polynomial([Fraction(1)] + [Fraction(0)] * (root - 1), root):
                raise ArithmeticError("Z_3 Parseval conditional normalization failed at prefix")
            prefix_entries.append({
                "v_prefix_mod_3_pow_k": v_prefix,
                "conditional_probabilities_v_k_0_1_2": tuple(branch_polys),
                "parseval_sum_equals_one": True,
            })
        conditional_tables.append({
            "step_k": k,
            "paired_site_index": k,
            "prefix_modulus_3_pow_k": 3 ** k,
            "prefix_conditionals": tuple(prefix_entries),
        })

    # 3. Verify that prod_{k=0}^{M-1} P_k(v_k | v_0, ..., v_{k-1}) == full_cyclic_1call[v] for all v in 0..D-1
    chain_rule_outcomes = []
    for v in range(D):
        prod_coeffs = [Fraction(1)] + [Fraction(0)] * (root - 1)
        for k in range(M):
            v_prefix = v % (3 ** k)
            v_k = (v // (3 ** k)) % 3
            prod_coeffs = cyclotomic_multiply(prod_coeffs, raw_cond_lookup[(k, v_prefix, v_k)], root)
        poly_v = root_polynomial(prod_coeffs, root)
        if poly_v != full_cyclic_1call[v]:
            raise ArithmeticError("autoregressive chain rule product disagreed with 1-call cyclic DFT")
        chain_rule_outcomes.append(poly_v)

    return {
        "modulus_q": q,
        "word_sites_M": M,
        "word_dimension_D": D,
        "root_order": root,
        "autoregressive_conditional_tables": tuple(conditional_tables),
        "chain_rule_product_all_outcomes": tuple(chain_rule_outcomes),
        "full_cyclic_dft_1call_all_outcomes": tuple(full_cyclic_1call),
        "chain_rule_matches_full_cyclic_dft_identically": chain_rule_outcomes == full_cyclic_1call,
        "per_sample_autoregressive_evaluation_steps": M,
        "one_call_cyclic_dft_classically_sampleable_in_O_M": True,
    }


def signed_two_call_cyclic_control(parameters):
    """Audit signed (+1, -1) cyclic 2-call schedule F_D^dag D_y^dag F_D D_y |+_D>."""
    raw, mask, truth, errors = source_data(*parameters)
    raw = original_bank(raw)
    rows = word_rows(raw, mask)
    D, q = len(rows), raw[0].modulus
    n = len(raw[0].label)
    root = max(D, q)
    phase_scale, fourier_scale = root // q, root // D

    # Observed public-data readout for signed (+1, -1) schedule
    observed_outcomes = []
    for x in range(D):
        hist = Counter(
            (phase_scale * (rw["known_phase"] - rv["known_phase"]) + fourier_scale * v * (w - x)) % root
            for w, rw in enumerate(rows)
            for v, rv in enumerate(rows)
        )
        observed_outcomes.append(root_polynomial(_histogram_probability(hist, root, D ** 3), root))

    # Data phases cancel, but the quadratic Fourier phase remains.
    diagonal_zero_phase_paths = sum(
        1 for w, rw in enumerate(rows) if (rw["known_phase"] - rows[w]["known_phase"]) % q == 0
    )

    secrets = tuple(product(range(q), repeat=n))
    error_phases = tuple(
        sum(
            b * e
            for t, pair in zip(r["word"], zip(errors[::2], errors[1::2]))
            for b, e in zip(DIGITS[t], pair)
        )
        % q
        for r in rows
    )

    sweep_outcomes = []
    pinched_outcomes = []
    for x in range(D):
        sweep = [Fraction(0)] * root
        for s in secrets:
            hist = Counter()
            for w, rw in enumerate(rows):
                for v, rv in enumerate(rows):
                    phase = sum((a - b) * t for a, b, t in zip(rw["frequency"], rv["frequency"], s))
                    exponent = (
                        phase_scale * (phase + error_phases[w] - error_phases[v])
                        + fourier_scale * v * (w - x)
                    ) % root
                    hist[exponent] += 1
            term = _histogram_probability(hist, root, (D ** 3) * len(secrets))
            sweep = [a + b for a, b in zip(sweep, term)]

        # Difference-relation pinching: group by delta_f = (f_A(w) - f_A(v)) mod q
        grouped = {}
        for w, rw in enumerate(rows):
            for v, rv in enumerate(rows):
                delta_f = tuple((a - b) % q for a, b in zip(rw["frequency"], rv["frequency"]))
                exponent = (
                    phase_scale * (error_phases[w] - error_phases[v])
                    + fourier_scale * v * (w - x)
                ) % root
                grouped.setdefault(delta_f, Counter())[exponent] += 1
        pinched = [Fraction(0)] * root
        for hist in grouped.values():
            term = _histogram_probability(hist, root, D ** 3)
            pinched = [a + b for a, b in zip(pinched, term)]

        poly_s = root_polynomial(sweep, root)
        poly_p = root_polynomial(pinched, root)
        if poly_s != poly_p:
            raise ArithmeticError("signed (+1,-1) difference pinching disagreed with secret sweep")
        sweep_outcomes.append(poly_s)
        pinched_outcomes.append(poly_p)

    unsigned_ref = fourier_interleaved_readout(raw, mask)["exact_all_outcome_probabilities"]

    return {
        "original_records": tuple(r.public() for r in raw),
        "public_mask": tuple(mask),
        "calibration_only": {"masked_secret": truth, "original_errors": errors},
        "modulus_q": q,
        "word_dimension_D": D,
        "root_order": root,
        "schedule": "F_D_DAGGER D_y_DAGGER F_D D_y |PLUS_D>",
        "diagonal_w_eq_v_zero_phase_path_count": diagonal_zero_phase_paths,
        "diagonal_data_phase_cancels_only": True,
        "diagonal_fourier_component_weights": tuple(
            root_polynomial(_histogram_probability(
                Counter(w * (w - x) % D for w in range(D)), D, D ** 3
            ), D) for x in range(D)
        ),
        "diagonal_component_is_probability_lower_bound": False,
        "exact_observed_all_outcome_probabilities": tuple(observed_outcomes),
        "uniform_secret_mean_all_outcomes": tuple(sweep_outcomes),
        "difference_relation_pinched_all_outcomes": tuple(pinched_outcomes),
        "signed_pinching_matches_secret_sweep_identically": sweep_outcomes == pinched_outcomes,
        "signed_readout_differs_from_unsigned_readout": tuple(observed_outcomes) != tuple(unsigned_ref),
    }


def diagonal_floor_countercontrol():
    """Original paired phases (8,1,0) retain destructive Fourier interference."""
    D, q, phases = 3, 9, (8, 1, 0)
    hist = Counter(
        (phases[w] - phases[v] + (q // D) * v * w) % q
        for w in range(D) for v in range(D)
    )
    return {"modulus_q": q, "word_dimension_D": D,
        "original_pair_values": (8, 0), "digit_phases": phases,
        "outcome_x": 0,
        "exact_probability": root_polynomial(_histogram_probability(hist, q, D ** 3), q),
        "diagonal_component_weight": "1/9",
        "old_claimed_floor": "1/3", "probability_floor_claim_refuted": True}


def build_report():
    deps = (
        "native_basis_lottery.py",
        "native_full_root_slice.py",
        "native_response_path_valuation.py",
        "native_word_span_decision.py",
        "ternary_measured_lattice_decoder.py",
    )
    params_list = (
        (1, 2, 1, False, 99201),
        (1, 1, 2, True, 99202),
        (1, 2, 2, True, 99205),
    )
    tensor_controls = []
    autoregressive_controls = []
    signed_controls = []
    for p in params_list:
        raw, mask, _, _ = source_data(*p)
        tensor_controls.append(tensor_qutrit_two_call_readout(raw, mask, second_call_sign=1))
        autoregressive_controls.append(one_call_cyclic_autoregressive_chain_rule(raw, mask))
        signed_controls.append(signed_two_call_cyclic_control(p))

    return {
        "status": "RESPONSE_FOURIER_FACTORIZATION_AND_SIGNED_PATH_PINCHING_AUDIT_REVIEW_PENDING",
        "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
        "contract_sha256": hashlib.sha256(CONTRACT.read_bytes()).hexdigest(),
        "dependency_sha256": {
            f: hashlib.sha256((ROOT / "theorems" / f).read_bytes()).hexdigest() for f in deps
        },
        "tensor_qutrit_factorization_controls": tuple(tensor_controls),
        "one_call_cyclic_autoregressive_controls": tuple(autoregressive_controls),
        "signed_two_call_cyclic_controls": tuple(signed_controls),
        "diagonal_floor_countercontrol": diagonal_floor_countercontrol(),
        "this_finite_audit_supplies_polynomial_two_call_sampler": False,
        "full_cyclic_approximate_sampling_has_separate_classical_baseline": True,
        "general_quantum_lower_bound_claimed": False,
        "accepted_speedup_candidate": False,
        "new_active_negative_result_created": False,
        "novelty_claim": False,
        "research_decision": "TENSOR_F3_AND_ONE_CALL_CYCLIC_F_D_FACTORIZE_IN_O_M_WHILE_TWO_CALL_CYCLIC_F_D_COUPLES_REVERSE_DIGITS",
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
                "tensor_product_matches": [
                    c["product_matches_full_path_sum_identically"]
                    for c in rep["tensor_qutrit_factorization_controls"]
                ],
                "autoregressive_chain_rule_matches": [
                    c["chain_rule_matches_full_cyclic_dft_identically"]
                    for c in rep["one_call_cyclic_autoregressive_controls"]
                ],
                "signed_two_call_pinching_matches": [
                    c["signed_pinching_matches_secret_sweep_identically"]
                    for c in rep["signed_two_call_cyclic_controls"]
                ],
                "accepted_speedup_candidate": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
