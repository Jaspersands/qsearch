r"""DCP Krawtchouk polynomial binary Hamming association scheme MacWilliams CNOT bridge.

Establishes the exact Krawtchouk polynomial radial Hadamard transformation law on the
K-wire binary Hamming association scheme H(K, 2) and proves the exact quadratic root
blind-spot theorem for weight-2 parity probes at w_pm = (K +/- sqrt(K)) / 2:

1. Exact Krawtchouk Radial Hadamard Matrix Law:
   For any K >= 1, let |S_w> = C(K, w)^{-1/2} sum_{x in {0,1}^K : wt(x) = w} |x> be the
   normalized uniform superposition over the Hamming weight-w shell (w = 0, ..., K).
   Under the K-qubit Hadamard transform H^{\otimes K}, the (K + 1)-dimensional radial
   subspace span{|S_0>, ..., |S_K>} is invariant, with exact matrix elements:
       M_{k, w}^{(K)} = <S_k | H^{\otimes K} | S_w>
                      = 2^{-K/2} * sqrt(C(K, w) / C(K, k)) * K_k(w; K),
   where K_k(w; K) = sum_{j=0}^k (-1)^j C(w, j) C(K - w, k - j) is the degree-k binary
   Krawtchouk polynomial!
   Because H^{\otimes K} is unitary and involutory ((H^{\otimes K})^2 = I_{2^K}), the
   (K + 1) x (K + 1) radial matrix M^{(K)} satisfies:
       (M^{(K)})^2 = I_{K + 1}   <=>   sum_{w=0}^K K_k(w; K) * K_w(r; K) = 2^K * delta_{k, r}!

2. Exact Linear and Quadratic Krawtchouk Root Blind Spots:
   - Degree k = 1 (Weight-1 single-wire probes):
         K_1(w; K) = K - 2 * w = 0   <=>   w = K / 2 (for even K).
   - Degree k = 2 (Weight-2 CNOT pair probes):
         K_2(w; K) = C(K, 2) - 2 * K * w + 2 * w^2 = 0.5 * ( (K - 2*w)^2 - K ) = 0
         <=>   w_pm = (K +/- sqrt(K)) / 2!
   Therefore, whenever K = m^2 is a perfect square (such as K = 4 with w_pm in {1, 3},
   or K = 9 with w_pm in {3, 6}), a weight-2 parity shell |S_2> has ZERO Hadamard
   overlap (<S_2 | H^{\otimes K} | S_{w_pm}> == 0) with the weight-w_pm shell!
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from typing import Any, Dict, List


THEOREM_ID = "dcp_krawtchouk_polynomial_binary_hamming_scheme_macwilliams_cnot_bridge"
SCHEMA_VERSION = "dcp-krawtchouk-polynomial-binary-hamming-scheme-macwilliams-cnot-bridge-v1"


def krawtchouk_poly(k_deg: int, w_val: int, k_total: int) -> int:
    """Compute exact integer value of K_{k_deg}(w_val; k_total) = sum_{j=0}^{k_deg} (-1)^j C(w, j) C(K - w, k - j)."""
    acc = 0
    for j in range(k_deg + 1):
        if j <= w_val and (k_deg - j) <= (k_total - w_val):
            term = math.comb(w_val, j) * math.comb(k_total - w_val, k_deg - j)
            acc += (-term) if (j & 1) else term
    return acc


def evaluate_krawtchouk_radial_hadamard_and_roots(k_total: int) -> Dict[str, Any]:
    """Verify explicit 2^K Hadamard shell overlaps against Krawtchouk polynomials and check involution M^2 = I."""
    if type(k_total) is not int or k_total < 2 or k_total > 10:
        raise ValueError("k_total must be an integer in [2, 10]")

    dim = 1 << k_total
    norm_factor = math.sqrt(float(dim))

    # 1. Construct radial matrix M_{k, w} via Krawtchouk closed form:
    m_rad = [[0.0] * (k_total + 1) for _ in range(k_total + 1)]
    for k_deg in range(k_total + 1):
        for w_val in range(k_total + 1):
            k_val = krawtchouk_poly(k_deg, w_val, k_total)
            m_rad[k_deg][w_val] = (
                math.sqrt(float(math.comb(k_total, w_val)) / float(math.comb(k_total, k_deg)))
                * float(k_val)
                / norm_factor
            )

    # 2. Verify M^2 == I_{K+1} and symmetry M_{k, w} == M_{w, k}:
    max_involution_err = 0.0
    max_symmetry_err = 0.0
    for r in range(k_total + 1):
        for c in range(k_total + 1):
            max_symmetry_err = max(max_symmetry_err, abs(m_rad[r][c] - m_rad[c][r]))
            dot_rc = sum(m_rad[r][j] * m_rad[j][c] for j in range(k_total + 1))
            expected = 1.0 if r == c else 0.0
            max_involution_err = max(max_involution_err, abs(dot_rc - expected))

    # 3. For K <= 6, explicitly compute <S_k | H^{\otimes K} | S_w> by summing (-1)^{<u, x>} over shells:
    max_explicit_shell_err = 0.0
    if k_total <= 6:
        shells: List[List[int]] = [[] for _ in range(k_total + 1)]
        for mask in range(dim):
            shells[bin(mask).count("1")].append(mask)
        for k_deg in range(k_total + 1):
            # By permutation symmetry, <S_k | H^{\otimes K} | S_w> = sqrt(C(K, k) / C(K, w)) * 2^{-K/2} * sum_{x in W_w} (-1)^{<u_rep, x>}
            u_rep = (1 << k_deg) - 1
            for w_val in range(k_total + 1):
                acc = sum(
                    -1.0 if (bin(u_rep & x_mask).count("1") & 1) else 1.0
                    for x_mask in shells[w_val]
                )
                exp_elem = (
                    math.sqrt(float(math.comb(k_total, k_deg)) / float(math.comb(k_total, w_val)))
                    * acc
                    / norm_factor
                )
                max_explicit_shell_err = max(max_explicit_shell_err, abs(exp_elem - m_rad[k_deg][w_val]))

    # 4. Identify exact integer roots of K_2(w; K) = 0:
    k2_values = [krawtchouk_poly(2, w, k_total) for w in range(k_total + 1)]
    k2_zero_weights = [w for w, val in enumerate(k2_values) if val == 0]

    sqrt_k = int(round(math.sqrt(float(k_total))))
    is_perfect_square = (sqrt_k * sqrt_k == k_total)
    expected_k2_roots = sorted([(k_total - sqrt_k) // 2, (k_total + sqrt_k) // 2]) if is_perfect_square else []

    return {
        "K_total": k_total,
        "is_perfect_square_K": is_perfect_square,
        "k2_polynomial_values": k2_values,
        "k2_integer_root_weights": k2_zero_weights,
        "expected_k2_roots": expected_k2_roots,
        "max_involution_error": max_involution_err,
        "max_symmetry_error": max_symmetry_err,
        "max_explicit_shell_error": max_explicit_shell_err,
        "exact_krawtchouk_laws_verified": (
            max_involution_err < 1e-12
            and max_symmetry_err < 1e-12
            and max_explicit_shell_err < 1e-12
            and k2_zero_weights == expected_k2_roots
        ),
    }


def generate_dcp_krawtchouk_polynomial_binary_hamming_scheme_macwilliams_cnot_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the Krawtchouk polynomial binary Hamming scheme bridge."""
    audit_k4 = evaluate_krawtchouk_radial_hadamard_and_roots(k_total=4)  # square K=4 -> roots at w in {1, 3}!
    audit_k6 = evaluate_krawtchouk_radial_hadamard_and_roots(k_total=6)  # non-square K=6 -> no integer roots of K_2!
    audit_k9 = evaluate_krawtchouk_radial_hadamard_and_roots(k_total=9)  # square K=9 -> roots at w in {3, 6}!

    all_passed = (
        audit_k4["exact_krawtchouk_laws_verified"]
        and audit_k4["k2_integer_root_weights"] == [1, 3]
        and audit_k6["exact_krawtchouk_laws_verified"]
        and audit_k6["k2_integer_root_weights"] == []
        and audit_k9["exact_krawtchouk_laws_verified"]
        and audit_k9["k2_integer_root_weights"] == [3, 6]
    )

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "proof_status": "LOCAL_DERIVATION_REVIEW_PENDING_NOT_FORMALLY_VERIFIED",
        "scope_constraints": {
            "applies_to": "Krawtchouk polynomial K_k(w; K) radial Hadamard transformation on H(K, 2) and quadratic root blind spots w_pm = (K +/- sqrt(K))/2",
            "does_not_claim": "Vanishing of non-symmetric targeted weight-2 CNOT pairs when the input state is not symmetrized over the Hamming shell",
            "controls_included": "Evaluates K=4 (roots w in {1, 3}), K=6 (non-square control, no integer roots), and K=9 (roots w in {3, 6}), verifying M^2 == I_{K+1} to < 1e-12.",
        },
        "audit_k4_square": audit_k4,
        "audit_k6_nonsquare": audit_k6,
        "audit_k9_square": audit_k9,
        "all_checks_passed": all_passed,
        "honesty_guardrails": {
            "accepted_speedup_candidate": False,
            "new_active_negative_result_created": False,
            "novelty_claim": False,
        },
    }
    digest = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()[:16]
    payload["certificate_sha256_16"] = digest
    return payload
