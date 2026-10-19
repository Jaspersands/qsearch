r"""DCP non-binary Reed-Solomon Vandermonde qudit barycentric witness bridge.

Establishes the exact Lagrange-Vandermonde barycentric nullspace theorem over finite
prime fields F_p (for odd primes p >= 5) that deterministically constructs a
(d + 2)-qudit zero-sum witness w = (w_0, ..., w_{d+1}) in (F_p^x)^{d+2} annihilating
EVERY degree <= d polynomial progression while isolating the pure degree-(d + 1) leading
coefficient:

1. Exact Lagrange Barycentric Vandermonde Orthogonality Law Over F_p:
   Let x_0, x_1, ..., x_{d+1} in F_p be d + 2 distinct evaluation points (with d + 2 <= p).
   Define the non-zero barycentric weights in F_p^x:
       w_j = prod_{0 <= l <= d + 1, l != j} (x_j - x_l)^{-1} (mod p)   for j = 0, ..., d + 1.
   By partial-fraction decomposition of 1 / prod_{j=0}^{d+1} (X - x_j), the barycentric
   weights satisfy the EXACT Vandermonde moment identities over F_p:
       sum_{j=0}^{d+1} w_j * x_j^r == 0 (mod p)   for ALL r in {0, 1, ..., d},
       sum_{j=0}^{d+1} w_j * x_j^{d+1} == 1 (mod p)!

2. Universal Annihilation of Degree <= d Nuisance Polynomials & Pure Leading Extraction:
   For ANY polynomial label family P(X) = c_{d+1} X^{d+1} + sum_{r=0}^d c_r X^r in F_p[X],
   applying the Z_p-weighted modular qudit sum with weights (w_0, ..., w_{d+1}) across the
   d + 2 wires evaluated at (x_0, ..., x_{d+1}) yields:
       sum_{j=0}^{d+1} w_j * P(x_j) == c_{d+1} (mod p),
   simultaneously eliminating all d + 1 lower-degree coefficients (c_0, ..., c_d) across
   100% of p^{d+1} nuisance polynomials!
"""

from __future__ import annotations

import hashlib
import itertools
import json
from typing import Any, Dict, List, Sequence


THEOREM_ID = "dcp_non_binary_reed_solomon_vandermonde_qudit_witness_bridge"
SCHEMA_VERSION = "dcp-non-binary-reed-solomon-vandermonde-qudit-witness-bridge-v1"


def compute_barycentric_vandermonde_weights(
    eval_points: Sequence[int],
    p_prime: int,
) -> List[int]:
    """Compute exact barycentric weights w_j = prod_{l != j} (x_j - x_l)^{-1} mod p."""
    m_pts = len(eval_points)
    weights: List[int] = []
    for j in range(m_pts):
        xj = int(eval_points[j]) % p_prime
        denom = 1
        for l_idx in range(m_pts):
            if l_idx != j:
                xl = int(eval_points[l_idx]) % p_prime
                diff = (xj - xl) % p_prime
                if diff == 0:
                    raise ValueError("eval_points must be distinct mod p_prime")
                denom = (denom * diff) % p_prime
        weights.append(pow(denom, -1, p_prime))
    return weights


def evaluate_reed_solomon_barycentric_witness(
    p_prime: int,
    d_degree: int,
    eval_points: Sequence[int],
) -> Dict[str, Any]:
    """Verify Vandermonde moment identities for r = 0..d+1 and exhaustive annihilation of all p^{d+1} polynomials of degree <= d."""
    if len(eval_points) != d_degree + 2:
        raise ValueError("eval_points must have length d_degree + 2")

    weights = compute_barycentric_vandermonde_weights(eval_points, p_prime)

    # 1. Check Vandermonde power sums sum_{j=0}^{d+1} w_j * x_j^r mod p for r = 0 .. d + 1:
    moment_sums: List[int] = []
    for r in range(d_degree + 2):
        s_r = sum(weights[j] * pow(int(eval_points[j]), r, p_prime) for j in range(d_degree + 2)) % p_prime
        moment_sums.append(s_r)

    expected_moments = [0] * (d_degree + 1) + [1]
    moments_verified = (moment_sums == expected_moments)

    # 2. Exhaustively test ALL p^{d+1} polynomials P(X) = c_{d+1} X^{d+1} + sum_{r=0}^d c_r X^r for c_{d+1} in {0, 3}:
    all_lower_coeffs = list(itertools.product(range(p_prime), repeat=d_degree + 1))
    zero_sum_hits = 0
    leading_3_hits = 0
    c_lead_test = 3 % p_prime

    for coeffs in all_lower_coeffs:
        # Case A: c_{d+1} = 0 (pure degree <= d polynomial):
        val0 = 0
        val_lead = 0
        for j, xj in enumerate(eval_points):
            px0 = sum(coeffs[r] * pow(int(xj), r, p_prime) for r in range(d_degree + 1)) % p_prime
            px_lead = (px0 + c_lead_test * pow(int(xj), d_degree + 1, p_prime)) % p_prime
            val0 = (val0 + weights[j] * px0) % p_prime
            val_lead = (val_lead + weights[j] * px_lead) % p_prime
        if val0 == 0:
            zero_sum_hits += 1
        if val_lead == c_lead_test:
            leading_3_hits += 1

    total_polys = len(all_lower_coeffs)

    return {
        "p_prime": p_prime,
        "d_degree": d_degree,
        "num_wires_d_plus_2": d_degree + 2,
        "eval_points": [int(x) for x in eval_points],
        "barycentric_weights_mod_p": weights,
        "vandermonde_moment_sums_r_0_to_d_plus_1": moment_sums,
        "total_degree_le_d_polynomials_tested": total_polys,
        "degree_le_d_annihilated_count": zero_sum_hits,
        "leading_coeff_extracted_count": leading_3_hits,
        "exact_barycentric_laws_verified": (
            moments_verified
            and all(w != 0 for w in weights)
            and zero_sum_hits == total_polys
            and leading_3_hits == total_polys
        ),
    }


def generate_dcp_non_binary_reed_solomon_vandermonde_qudit_witness_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the Reed-Solomon Vandermonde qudit witness bridge."""
    # 1. p = 5, d = 2 (4 evaluation points [0, 1, 2, 3], 5^3 = 125 polynomials tested exhaustively):
    # Note: on consecutive points [0, 1, 2, 3], finite differences have alternating binomial weights
    # (-1)^{3-j} C(3, j) = [-1, 3, -3, 1] / 3! == [-1, 3, 2, 1] * (-1) mod 5!
    audit_p5_d2 = evaluate_reed_solomon_barycentric_witness(
        p_prime=5, d_degree=2, eval_points=[0, 1, 2, 3]
    )

    # 2. p = 7, d = 2 on non-consecutive points [1, 2, 4, 6] (7^3 = 343 polynomials tested exhaustively):
    audit_p7_d2_nonconsec = evaluate_reed_solomon_barycentric_witness(
        p_prime=7, d_degree=2, eval_points=[1, 2, 4, 6]
    )

    all_passed = (
        audit_p5_d2["exact_barycentric_laws_verified"]
        and audit_p7_d2_nonconsec["exact_barycentric_laws_verified"]
    )

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "proof_status": "LOCAL_DERIVATION_REVIEW_PENDING_NOT_FORMALLY_VERIFIED",
        "scope_constraints": {
            "applies_to": "Lagrange barycentric Vandermonde weights w_j = prod_{l!=j} (x_j - x_l)^{-1} mod p for qudit polynomial witness annihilation over F_p",
            "does_not_claim": "Carry-free lifting from F_p to Z_{p^2} without monochrome syndrome selection (Subsystem 83)",
            "controls_included": "Exhaustively tests all 125 degree<=2 polynomials over F_5 on [0,1,2,3] and all 343 degree<=2 polynomials over F_7 on non-consecutive [1,2,4,6], verifying 100% annihilation and leading-term extraction.",
        },
        "audit_p5_d2_consecutive": audit_p5_d2,
        "audit_p7_d2_nonconsecutive": audit_p7_d2_nonconsec,
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
