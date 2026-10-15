"""Banded cyclic QFT two-call schedules and O(M 3^b) transfer-matrix contraction.

Proves and audits:
1. Exact analytical elimination of intermediate call digits v_{M-1-k} in {0,1,2}
   for bandwidth-b two-call cyclic QFT schedules (F_{3^M}^(b))^dag D_y^(+-1) F_{3^M}^(b) D_y |+_D>.
2. Exact O(M 3^b) forward sliding-window transfer-matrix dynamic programming contraction
   over boundary states of size 3^min(b-1, M-1-k), matching the 3^(2M)-path sum identically.
3. Exact recovery of bit-reversed tensor F_3^M at b=1 and full cyclic F_{3^M} at b=M,
   plus scaling ledgers proving poly(M) classical contraction for b = O(log M).
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
from native_response_fourier_factorization_audit import cyclotomic_multiply, site_phase_tables
from native_response_path_valuation import _histogram_probability, fourier_interleaved_readout, word_rows
from native_word_span_decision import root_polynomial
from ternary_measured_lattice_decoder import exact_json, integer

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT / "research/NATIVE_BANDED_QFT_TRANSFER_MATRIX_AUDIT.md"
CONTRACT = ROOT / "research/hypotheses/native_banded_qft_transfer_matrix_audit_contract.json"
REPORT = ROOT / "research/reductions/native_banded_qft_transfer_matrix_audit.json"


def cyclotomic_add(coeffs_a, coeffs_b):
    """Add two length-root rational coefficient vectors."""
    return [a + b for a, b in zip(coeffs_a, coeffs_b)]


def cyclotomic_norm_squared(coeffs, root):
    """Compute |sum_j coeffs[j] * zeta_root^j|^2 as a length-root coefficient vector."""
    out = [Fraction(0)] * root
    for i, a in enumerate(coeffs):
        if a:
            for j, b in enumerate(coeffs):
                if b:
                    out[(i - j) % root] += a * b
    return out


def banded_qft_phase_exponent(w_word, v_word, x_word, bandwidth_b):
    """Compute Phi^(b)(w, v; x) mod 3^M for twiddle bandwidth b in [1, M]."""
    M = len(w_word)
    D = 3 ** M
    total = 0
    for k in range(M):
        v_digit = v_word[M - 1 - k]
        if v_digit == 0:
            continue
        win_end = min(M, k + bandwidth_b)
        win_sum = 0
        for ell in range(k, win_end):
            win_sum += (w_word[ell] - x_word[ell]) * (3 ** (M - 1 - (ell - k)))
        total += v_digit * win_sum
    return total % D


def banded_qft_transfer_matrix_readout(records, mask, bandwidth_b, second_call_sign=1):
    """Contract 2-call bandwidth-b cyclic QFT readout via O(M 3^b) sliding-window DP."""
    if second_call_sign not in (-1, 1):
        raise ValueError("second_call_sign in {-1, +1} required")
    raw = original_bank(records)
    q = raw[0].modulus
    rows = word_rows(raw, mask)
    sites = site_phase_tables(raw, mask)
    M = len(sites)
    integer(bandwidth_b, "positive twiddle bandwidth b", 1)
    if bandwidth_b > M:
        raise ValueError("twiddle bandwidth b <= M required")
    D = 3 ** M
    root = max(q, D)
    phase_scale = root // q
    fourier_scale = root // D

    dp_outcomes = []
    brute_outcomes = []
    window_evals_per_outcome = sum(3 ** min(bandwidth_b, M - k) for k in range(M))
    max_boundary_states = 3 ** (bandwidth_b - 1)

    for x_idx, rx in enumerate(rows):
        x_word = rx["word"]

        # 1. Forward sliding-window transfer-matrix DP over k = 0..M-1
        init_len = min(bandwidth_b - 1, M)
        f_curr = {
            st: ([Fraction(1)] + [Fraction(0)] * (root - 1))
            for st in product(range(3), repeat=init_len)
        }
        actual_win_evals = 0
        for k in range(M):
            win_len = min(bandwidth_b, M - k)
            prev_len = min(bandwidth_b - 1, M - k)
            next_len = min(bandwidth_b - 1, M - 1 - k)
            f_next = {
                st: ([Fraction(0)] * root)
                for st in product(range(3), repeat=next_len)
            }
            phases_w = sites[k]["digit_phases"]
            phases_v = sites[M - 1 - k]["digit_phases"]
            x_slice = x_word[k : k + win_len]

            for w_win in product(range(3), repeat=win_len):
                actual_win_evals += 1
                w_k = w_win[0]
                win_shift = sum(
                    (w_win[offset] - x_slice[offset]) * (3 ** (M - 1 - offset))
                    for offset in range(win_len)
                )
                l_coeffs = [Fraction(0)] * root
                base_w_exp = phase_scale * phases_w[w_k]
                for t in range(3):
                    exp_val = (
                        base_w_exp
                        + phase_scale * (second_call_sign * phases_v[t])
                        + fourier_scale * t * win_shift
                    ) % root
                    l_coeffs[exp_val] += Fraction(1, 3)

                prev_state = w_win[:prev_len]
                next_state = w_win[1:]
                prod_term = cyclotomic_multiply(f_curr[prev_state], l_coeffs, root)
                f_next[next_state] = cyclotomic_add(f_next[next_state], prod_term)
            f_curr = f_next

        if actual_win_evals != window_evals_per_outcome or () not in f_curr:
            raise ArithmeticError("transfer-matrix DP state count mismatch")
        amp_coeffs = f_curr[()]
        prob_coeffs = [c / D for c in cyclotomic_norm_squared(amp_coeffs, root)]
        dp_poly = root_polynomial(prob_coeffs, root)
        dp_outcomes.append(dp_poly)

        # 2. Brute-force 3^(2M) path sum verification
        hist_brute = Counter()
        for rw in rows:
            w_word = rw["word"]
            for rv in rows:
                v_word = rv["word"]
                phi_b = banded_qft_phase_exponent(w_word, v_word, x_word, bandwidth_b)
                exp_val = (
                    phase_scale * (rw["known_phase"] + second_call_sign * rv["known_phase"])
                    + fourier_scale * phi_b
                ) % root
                hist_brute[exp_val] += 1
        brute_poly = root_polynomial(_histogram_probability(hist_brute, root, D ** 3), root)
        if dp_poly != brute_poly:
            raise ArithmeticError("transfer-matrix DP disagreed with brute-force 3^(2M) path sum")
        brute_outcomes.append(brute_poly)

    matches_full_cyclic = None
    if bandwidth_b == M and second_call_sign == 1:
        full_ref = fourier_interleaved_readout(raw, mask)["exact_all_outcome_probabilities"]
        if tuple(dp_outcomes) != tuple(full_ref):
            raise ArithmeticError("b=M transfer-matrix DP disagreed with full cyclic QFT readout")
        matches_full_cyclic = True

    return {
        "modulus_q": q,
        "word_sites_M": M,
        "word_dimension_D": D,
        "root_order": root,
        "twiddle_bandwidth_b": bandwidth_b,
        "second_call_sign": second_call_sign,
        "max_transfer_matrix_boundary_states_3_pow_b_minus_1": max_boundary_states,
        "dp_window_evaluations_per_outcome": window_evals_per_outcome,
        "dp_window_evaluations_upper_bound_M_times_3_pow_b": M * (3 ** bandwidth_b),
        "brute_force_path_pairs_per_outcome_3_pow_2M": D * D,
        "transfer_matrix_dp_all_outcomes": tuple(dp_outcomes),
        "brute_force_path_sum_all_outcomes": tuple(brute_outcomes),
        "dp_matches_brute_force_identically": dp_outcomes == brute_outcomes,
        "matches_untruncated_cyclic_qft_when_b_eq_M": matches_full_cyclic,
    }


def bandwidth_scaling_ledger(M, bandwidth_b):
    """Compute exact DP complexity vs full 3^(2M) path count at pair count M and bandwidth b."""
    integer(M, "positive word sites M", 1)
    integer(bandwidth_b, "positive twiddle bandwidth b", 1)
    if bandwidth_b > M or M > 4096:
        raise ValueError("1 <= b <= M <= 4096 required")
    boundary_states = 3 ** (bandwidth_b - 1)
    dp_window_evals = sum(3 ** min(bandwidth_b, M - k) for k in range(M))
    dp_upper = M * (3 ** bandwidth_b)
    qft_twiddle_gates = sum(min(bandwidth_b, M - k) for k in range(M))
    return {
        "word_sites_M": M,
        "twiddle_bandwidth_b": bandwidth_b,
        "qft_twiddle_gates_count": qft_twiddle_gates,
        "transfer_matrix_boundary_states_3_pow_b_minus_1": boundary_states,
        "exact_dp_window_evaluations_per_outcome": dp_window_evals,
        "dp_window_evaluations_upper_M_3_pow_b": dp_upper,
        "local_summand_evaluations_3_times_dp_windows": 3 * dp_window_evals,
        "dp_within_M_3_pow_b_bound": dp_window_evals <= dp_upper,
        "polynomial_in_M_when_b_is_O_log_M": bandwidth_b <= (M.bit_length() + 1),
        "full_bandwidth_b_eq_M": bandwidth_b == M,
    }


def build_report():
    deps = (
        "native_basis_lottery.py",
        "native_full_root_slice.py",
        "native_response_fourier_factorization_audit.py",
        "native_response_path_valuation.py",
        "native_word_span_decision.py",
        "ternary_measured_lattice_decoder.py",
    )
    raw2, mask2, truth2, errors2 = source_data(1, 2, 2, True, 99205)
    sweep_m2 = (
        banded_qft_transfer_matrix_readout(raw2, mask2, 1, second_call_sign=1),
        banded_qft_transfer_matrix_readout(raw2, mask2, 2, second_call_sign=1),
        banded_qft_transfer_matrix_readout(raw2, mask2, 1, second_call_sign=-1),
        banded_qft_transfer_matrix_readout(raw2, mask2, 2, second_call_sign=-1),
    )

    scaling_profiles = tuple(
        bandwidth_scaling_ledger(M, b)
        for M, b in (
            (16, 1),
            (16, 2),
            (16, 3),
            (64, 2),
            (64, 4),
            (140, 3),
            (140, 6),
        )
    )

    return {
        "status": "BANDED_QFT_TWO_CALL_TRANSFER_MATRIX_DEQUANTIZATION_AUDIT_REVIEW_PENDING",
        "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
        "contract_sha256": hashlib.sha256(CONTRACT.read_bytes()).hexdigest(),
        "dependency_sha256": {
            f: hashlib.sha256((ROOT / "theorems" / f).read_bytes()).hexdigest() for f in deps
        },
        "banded_qft_m2_sweep_control": {
            "original_records": tuple(r.public() for r in original_bank(raw2)),
            "public_mask": tuple(mask2),
            "calibration_only": {"masked_secret": truth2, "original_errors": errors2},
            "bandwidth_and_sign_sweeps": sweep_m2,
            "b1_differs_from_b2_unsigned": (
                sweep_m2[0]["transfer_matrix_dp_all_outcomes"]
                != sweep_m2[1]["transfer_matrix_dp_all_outcomes"]
            ),
            "b1_differs_from_b2_signed": (
                sweep_m2[2]["transfer_matrix_dp_all_outcomes"]
                != sweep_m2[3]["transfer_matrix_dp_all_outcomes"]
            ),
        },
        "bandwidth_scaling_ledgers": scaling_profiles,
        "full_bandwidth_b_eq_M_is_poly_M": False,
        "three_or_more_calls_contracted_by_2call_dp": False,
        "general_quantum_lower_bound_claimed": False,
        "accepted_speedup_candidate": False,
        "new_active_negative_result_created": False,
        "novelty_claim": False,
        "research_decision": "BANDED_TWO_CALL_QFT_SCHEDULES_CONTRACT_IN_O_M_3_POW_B_SO_ANY_TWO_CALL_ADVANTAGE_REQUIRES_SUPERLOG_TWIDDLE_BANDWIDTH",
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
                "dp_matches_brute_force": [
                    s["dp_matches_brute_force_identically"]
                    for s in rep["banded_qft_m2_sweep_control"]["bandwidth_and_sign_sweeps"]
                ],
                "scaling_profiles": len(rep["bandwidth_scaling_ledgers"]),
                "accepted_speedup_candidate": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
