"""Retained work-register multiplicity erasure and preimage equivalence audit.

Proves and audits:
1. Conditional secret-readout leakage 1 - 1/(N*C_A) from fibre multiplicity
   variance on the retained integer-slice work register.
2. Exact block-encoding scale price of passive diagonal multiplicity erasure
   w_sigma* = m_min^+ / m_sigma and target-amplitude monotonicity <= 1/N.
3. Noiseless coordinate recovery from chosen-frequency preimages. No noisy
   recovery follows without a public noise bound/decoder; private errors are
   used only to check the forward equations.
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
from native_small_multiple_completion import _rational
from native_word_spectral_filter_audit import finite_control
from native_word_span_decision import root_polynomial
from ternary_measured_lattice_decoder import exact_json, integer

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT / "research/NATIVE_RETAINED_WORK_MULTIPLICITY_ERASURE_AUDIT.md"
CONTRACT = ROOT / "research/hypotheses/native_retained_work_multiplicity_erasure_audit_contract.json"
REPORT = ROOT / "research/reductions/native_retained_work_multiplicity_erasure_audit.json"


def retained_work_multiplicity_control(args):
    """Audit raw vs multiplicity-erased retained work states and preimage equivalence."""
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
    supported_count = len(freq_counts)
    min_pos_mult = min(freq_counts.values())
    max_mult = max(freq_counts.values())

    C_A = sum(Fraction(c * c, D * D) for c in freq_counts.values())
    var_unif = sum((Fraction(freq_counts[f], D) - Fraction(1, N)) ** 2 for f in frequencies)
    if C_A != Fraction(1, N) + var_unif:
        raise ArithmeticError("pushforward collision variance identity C_A == 1/N + Var failed")

    # 1. Noiseless raw retained work readout:
    # P(zero, e=0) = C_A, P(readout -s AND zero, e=0) = 1/N
    raw_cond_true = Fraction(1, N) / C_A
    raw_cond_leakage = 1 - raw_cond_true
    if raw_cond_true != Fraction(1, 1 + N * var_unif):
        raise ArithmeticError("conditional noiseless readout formula mismatch")

    # 2. Passive diagonal multiplicity erasure W* = diag(m_min^+ / m_sigma on supp(p)):
    c_flat = Fraction(min_pos_mult, D)
    erased_joint_zero_prob = supported_count * (c_flat * c_flat)
    erased_joint_true_prob = Fraction(1, N) * ((supported_count * c_flat) ** 2)
    erased_cond_true = erased_joint_true_prob / erased_joint_zero_prob
    if erased_cond_true != Fraction(supported_count, N):
        raise ArithmeticError("multiplicity-erased conditional readout != S_+ / N")
    if erased_joint_true_prob > Fraction(1, N):
        raise ArithmeticError("passive diagonal contraction violated target-amplitude monotonicity")

    # 3. Exact noisy target-readout root polynomial at candidate b = -truth mod q:
    # For raw W = I:
    # < -s | F_q^dag | Psi_work(s, e) > = (1 / (D * sqrt(N))) * sum_w omega_q^(theta_e(w))
    # So P_I(readout -s AND zero, e) = (1 / (N * D^2)) * |sum_w omega_q^(theta_e(w))|^2
    raw_target_coeffs = [Fraction(0)] * q
    for w_idx in range(D):
        for v_idx in range(D):
            diff = (error_phases[v_idx] - error_phases[w_idx]) % q
            raw_target_coeffs[diff] += Fraction(1, N * D * D)
    raw_target_poly = root_polynomial(raw_target_coeffs, q)

    # For multiplicity-erased W* = diag(m_min^+ / m_sigma):
    # w_{f(w)}* = m_min^+ / m_{f(w)}, so each word w has weight m_min^+ / (D * m_{f(w)}).
    erased_target_coeffs = [Fraction(0)] * q
    for w_idx, rw in enumerate(rows):
        mw = freq_counts[tuple(rw["frequency"])]
        for v_idx, rv in enumerate(rows):
            mv = freq_counts[tuple(rv["frequency"])]
            diff = (error_phases[v_idx] - error_phases[w_idx]) % q
            erased_target_coeffs[diff] += Fraction(min_pos_mult * min_pos_mult, N * D * D * mw * mv)
    erased_target_poly = root_polynomial(erased_target_coeffs, q)

    # 4. Classical chosen-frequency preimage equivalence on standard basis vectors e_i:
    basis_preimages = []
    all_basis_covered = True
    recovered_coords = []
    for i in range(n):
        e_vec = tuple(1 if idx == i else 0 for idx in range(n))
        match_idx = next((w_idx for w_idx, r in enumerate(rows) if tuple(r["frequency"]) == e_vec), None)
        if match_idx is None:
            all_basis_covered = False
            basis_preimages.append({
                "coordinate_index": i,
                "target_basis_frequency": e_vec,
                "preimage_found_in_support": False,
                "word_index": None,
                "word_digits": None,
                "known_phase_mod_q": None,
                "word_error_phase_FOR_CALIBRATION_ONLY": None,
                "noiseless_coordinate_matches_truth": None,
            })
        else:
            row_m = rows[match_idx]
            kp = row_m["known_phase"]
            ep = error_phases[match_idx]
            if (kp - ep) % q != truth[i] % q:
                raise ArithmeticError("chosen-frequency preimage equation eta_y == s_i + theta_e mod q failed")
            recovered_coords.append((kp - ep) % q)
            basis_preimages.append({
                "coordinate_index": i,
                "target_basis_frequency": e_vec,
                "preimage_found_in_support": True,
                "word_index": match_idx,
                "word_digits": row_m["word"],
                "known_phase_mod_q": kp,
                "word_error_phase_FOR_CALIBRATION_ONLY": ep,
                "noiseless_coordinate_matches_truth": (kp == truth[i]) if not any(errors) else ((kp - ep) % q == truth[i]),
            })

    return {
        "native_source_reference": base,
        "calibration_truth_FOR_DIAGNOSTIC_ONLY": {"masked_secret": truth, "original_errors": errors},
        "modulus_q": q,
        "dimension_n": n,
        "word_pairs_M": M,
        "word_dimension_D": D,
        "work_dimension_N": N,
        "supported_frequencies_S_plus": supported_count,
        "full_frequency_support_S_plus_equals_N": supported_count == N,
        "min_positive_fibre_multiplicity": min_pos_mult,
        "max_fibre_multiplicity": max_mult,
        "exact_collision_sum_C_A": str(C_A),
        "exact_uniform_departure_variance_sum": str(var_unif),
        "noiseless_raw_work_readout": {
            "joint_zero_acceptance_probability": str(C_A),
            "joint_true_secret_and_zero_probability": str(Fraction(1, N)),
            "conditional_true_secret_probability_given_zero": str(raw_cond_true),
            "conditional_wrong_secret_leakage_given_zero": str(raw_cond_leakage),
        },
        "noiseless_multiplicity_erased_work_readout": {
            "optimal_physical_flat_amplitude_m_min_over_D": str(c_flat),
            "joint_erased_and_zero_probability": str(erased_joint_zero_prob),
            "joint_true_secret_and_erased_and_zero_probability": str(erased_joint_true_prob),
            "conditional_true_secret_probability_given_erased_zero": str(erased_cond_true),
            "erased_joint_true_probability_at_most_one_over_N": erased_joint_true_prob <= Fraction(1, N),
            "strict_joint_scale_penalty_when_unbalanced": (erased_joint_true_prob < Fraction(1, N)) == (min_pos_mult * supported_count < D),
        },
        "noisy_true_secret_readout_root_polynomials": {
            "raw_identity_filter_root_polynomial": raw_target_poly,
            "multiplicity_erased_filter_root_polynomial": erased_target_poly,
        },
        "chosen_frequency_preimage_equivalence": {
            "all_standard_basis_frequencies_supported": all_basis_covered,
            "basis_preimage_queries": tuple(basis_preimages),
            "private_error_subtracted_equations_match_truth": tuple(recovered_coords) == truth if all_basis_covered else None,
            "direct_classical_secret_recovered_when_supported": (
                tuple(recovered_coords) == truth if all_basis_covered and not any(errors) else None),
            "private_errors_used_for_equation_check_only": True,
            "noisy_public_secret_recovery_supplied": False,
            "short_preimage_sampler_gives_classical_coordinate_observations": True,
            "short_preimage_sampler_alone_solves_noisy_problem": False,
        },
    }


def iid_multiplicity_leakage_ledger(n, r, surplus):
    """Compute exact IID population collision expectation and Jensen conditional readout ceiling."""
    for x, name in ((n, "dimension"), (r, "root digits"), (surplus, "word surplus")):
        integer(x, "positive " + name, 1)
    if n * r > 16384 or surplus > 128:
        raise ValueError("scaling exponent cap exceeded")
    M = n * r + surplus
    # E_A[C_A] = 1/N + (1 - 1/N)/D, so N * E_A[C_A] = 1 + (N - 1)/D = 1 + (1 - 1/N) * 3^(-surplus)
    # By convexity of x -> 1/x on x > 0, E_A[1 / (N * C_A)] <= 1 for individual realizations,
    # and the ratio of expected true-and-zero mass (1/N) to expected zero mass E_A[C_A] is:
    # (1/N) / E_A[C_A] = 1 / (1 + (1 - 1/N) * 3^(-surplus)) >= 1 / (1 + 3^(-surplus)) = 3^surplus / (3^surplus + 1).
    ratio_lower = Fraction(3 ** surplus, 3 ** surplus + 1)
    leakage_ratio_upper = 1 - ratio_lower
    return {
        "dimension_n": n,
        "root_digits_r": r,
        "word_sites_M": M,
        "word_surplus": surplus,
        "expected_N_times_C_A_upper": str(1 + Fraction(1, 3 ** surplus)),
        "noiseless_ensemble_true_to_zero_mass_ratio_lower": str(ratio_lower),
        "noiseless_ensemble_leakage_to_zero_mass_ratio_upper": str(leakage_ratio_upper),
        "any_passive_diagonal_work_contraction_joint_true_prob_at_most_3_pow_minus_nr": True,
        "multiplicity_erasure_removes_1_over_N_block_encoding_scale": False,
        "universal_quantum_lower_bound_claimed": False,
    }


def build_report():
    deps = (
        "native_basis_lottery.py",
        "native_full_root_slice.py",
        "native_small_multiple_completion.py",
        "native_word_spectral_filter_audit.py",
        "native_word_span_decision.py",
        "ternary_measured_lattice_decoder.py",
    )
    controls = tuple(
        retained_work_multiplicity_control(p)
        for p in (
            (1, 1, 3, False, 99001),
            (1, 2, 4, False, 99002),
            (1, 3, 5, True, 99003),
            (2, 1, 3, False, 99004),
        )
    )
    ledgers = tuple(iid_multiplicity_leakage_ledger(n, n, 12) for n in (8, 32, 64, 128))
    return {
        "status": "RETAINED_WORK_MULTIPLICITY_ERASURE_AND_PREIMAGE_EQUIVALENCE_AUDIT_REVIEW_PENDING",
        "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
        "contract_sha256": hashlib.sha256(CONTRACT.read_bytes()).hexdigest(),
        "dependency_sha256": {
            f: hashlib.sha256((ROOT / "theorems" / f).read_bytes()).hexdigest() for f in deps
        },
        "retained_work_controls": controls,
        "scaling_multiplicity_leakage_ledgers": ledgers,
        "universal_quantum_lower_bound_claimed": False,
        "preimage_oracle_granted_as_free_quantum_primitive": False,
        "accepted_speedup_candidate": False,
        "new_active_negative_result_created": False,
        "novelty_claim": False,
        "research_decision": "PASSIVE_WORK_MULTIPLICITY_ERASURE_CANNOT_EXCEED_ONE_OVER_N_JOINT_SUCCESS_AND_PREIMAGE_SAMPLING_IS_CLASSICAL_ATTACK",
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
                "controls_checked": len(rep["retained_work_controls"]),
                "monotonicity_verified": [
                    c["noiseless_multiplicity_erased_work_readout"]["erased_joint_true_probability_at_most_one_over_N"]
                    for c in rep["retained_work_controls"]
                ],
                "accepted_speedup_candidate": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
