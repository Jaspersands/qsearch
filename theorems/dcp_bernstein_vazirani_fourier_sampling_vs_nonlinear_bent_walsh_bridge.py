r"""
Subsystem 156: Bernstein-Vazirani 1-Query Fourier Sampling vs. Nonlinear Carry Dilution Bridge.

Proves and quantifies the exact single-query Bernstein-Vazirani success probability
P_{\text{BV}}(s) = |\hat{F}(s)|^2 when a linear secret parity s \cdot x (over \mathbb{F}_2^n)
is corrupted by a nonlinear Boolean carry function c(x) \in \{0, 1\}:
  f(x) = (s \cdot x) \oplus c(x),   F(x) = (-1)^{f(x)} = (-1)^{s \cdot x} (-1)^{c(x)}.

Key theorems proven and certified:
  1. Exact Walsh-Fourier Shift Identity:
       \hat{F}(u) = 2^{-n} \sum_{x \in \mathbb{F}_2^n} (-1)^{(s \oplus u) \cdot x} (-1)^{c(x)} = \hat{C}(u \oplus s),
     where \hat{C}(w) = 2^{-n} \sum_x (-1)^{c(x) \oplus w \cdot x}.
  2. Single-Query Bernstein-Vazirani Target Peak Formula:
       P_{\text{BV}}(s) = |\hat{F}(s)|^2 = |\hat{C}(0)|^2 = \left(1 - \frac{2\,\text{wt}(c)}{2^n}\right)^2,
     where \text{wt}(c) = |\{x \in \mathbb{F}_2^n : c(x) = 1\}| is the Hamming weight of the carry truth table!
  3. Three Canonical Regimes on n = 4 bits (2^n = 16):
       - Coherent CNOT-peeled affine function (c(x) = 0, \text{wt}(c) = 0):
           P_{\text{BV}}(s) = 1.0 (100% single-query deterministic recovery).
       - Single quadratic AND carry c(x) = x_1 x_2 (\text{wt}(c) = 2^{n-2} = 4):
           P_{\text{BV}}(s) = (1 - 2/4)^2 = 1/4 = 0.25 (6 dB carry dilution loss).
       - Balanced carry defect (\text{wt}(c) = 2^{n-1} = 8):
           P_{\text{BV}}(s) = 0.0 (complete destructive interference of target secret s!).
"""

from __future__ import annotations
from typing import Any, Dict, List


def evaluate_bernstein_vazirani_under_carry_defect(
    n_bits: int,
    secret_s: int,
    carry_truth_table: List[int],
) -> Dict[str, Any]:
    """
    Compute the full Walsh-Hadamard spectrum of f(x) = (s . x) xor c(x) over F_2^n
    and verify Parseval's identity and the exact formula P_BV(s) = (1 - 2*wt(c)/2^n)^2.
    """
    dim = 1 << n_bits
    assert len(carry_truth_table) == dim
    wt_c = sum(1 for v in carry_truth_table if (v & 1) == 1)

    probs: List[float] = []
    for u in range(dim):
        walsh_sum = 0
        for x in range(dim):
            dot_sx = ((secret_s & x).bit_count()) & 1
            dot_ux = ((u & x).bit_count()) & 1
            bit = dot_sx ^ (carry_truth_table[x] & 1) ^ dot_ux
            walsh_sum += -1 if bit else 1
        hat_f_u = walsh_sum / float(dim)
        probs.append(hat_f_u * hat_f_u)

    parseval_sum = sum(probs)
    target_prob = probs[secret_s]
    formula_prob = (1.0 - (2.0 * wt_c) / float(dim)) ** 2

    return {
        "n_bits": int(n_bits),
        "secret_s": int(secret_s),
        "carry_hamming_weight": int(wt_c),
        "target_bv_probability": float(target_prob),
        "analytic_formula_probability": float(formula_prob),
        "parseval_total_probability": float(parseval_sum),
        "max_spectrum_probability": float(max(probs)),
    }


def generate_dcp_bernstein_vazirani_fourier_sampling_vs_nonlinear_bent_walsh_certificate() -> Dict[str, Any]:
    """Generate the Subsystem 156 verification certificate."""
    n_bits = 4
    dim = 1 << n_bits
    secret_s = 0b1011

    # 1. CNOT-peeled zero carry c(x) = 0
    peeled = evaluate_bernstein_vazirani_under_carry_defect(n_bits, secret_s, [0] * dim)

    # 2. Single radix-2 AND carry c(x) = x_0 & x_1 (weight 4 out of 16)
    and_carry = [1 if ((x & 1) and ((x >> 1) & 1)) else 0 for x in range(dim)]
    quadratic_and = evaluate_bernstein_vazirani_under_carry_defect(n_bits, secret_s, and_carry)

    # 3. Two-stage carry cascade c(x) = (x_0 & x_1) ^ (x_2 & x_3) (bent function, weight 6 out of 16)
    bent_carry = [
        ((1 if ((x & 1) and ((x >> 1) & 1)) else 0) ^ (1 if (((x >> 2) & 1) and ((x >> 3) & 1)) else 0))
        for x in range(dim)
    ]
    bent_case = evaluate_bernstein_vazirani_under_carry_defect(n_bits, secret_s, bent_carry)

    # 4. Balanced carry defect (weight 8 out of 16 -> P_BV(s) = 0)
    balanced_carry = [1 if (x & 1) else 0 for x in range(dim)]
    balanced_case = evaluate_bernstein_vazirani_under_carry_defect(n_bits, secret_s, balanced_carry)

    cases = [peeled, quadratic_and, bent_case, balanced_case]
    theorem_checks = {
        "parseval_identity_sums_to_1_across_all_regimes": bool(
            all(abs(c["parseval_total_probability"] - 1.0) < 1e-14 for c in cases)
        ),
        "analytic_weight_formula_matches_exact_walsh_peak": bool(
            all(abs(c["target_bv_probability"] - c["analytic_formula_probability"]) < 1e-14 for c in cases)
        ),
        "cnot_peeled_zero_carry_achieves_100pct_single_query_bv": bool(
            abs(peeled["target_bv_probability"] - 1.0) < 1e-14
        ),
        "single_and_carry_dilutes_bv_peak_to_exact_one_quarter": bool(
            abs(quadratic_and["target_bv_probability"] - 0.25) < 1e-14
        ),
        "bent_carry_creates_flat_1_over_16_walsh_floor_everywhere": bool(
            abs(bent_case["target_bv_probability"] - 0.0625) < 1e-14
            and abs(bent_case["max_spectrum_probability"] - 0.0625) < 1e-14
        ),
        "balanced_carry_completely_extinguishes_target_secret_peak": bool(
            abs(balanced_case["target_bv_probability"]) < 1e-14
        ),
    }

    return {
        "subsystem_id": "dcp_bernstein_vazirani_fourier_sampling_vs_nonlinear_bent_walsh_bridge",
        "subsystem_number": 156,
        "domain": "boolean_fourier_analysis_bernstein_vazirani_carry_dilution",
        "peeled_zero_carry_case": peeled,
        "quadratic_and_carry_case": quadratic_and,
        "bent_cascade_carry_case": bent_case,
        "balanced_carry_case": balanced_case,
        "theorem_checks": theorem_checks,
        "all_checks_passed": bool(all(theorem_checks.values())),
        "falsification_status": {
            "accepted_speedup_candidate": False,
            "new_active_negative_result_created": False,
            "novelty_claim": False,
        },
    }
