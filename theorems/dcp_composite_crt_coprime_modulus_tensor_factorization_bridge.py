r"""DCP composite CRT coprime modulus (q = 2^t * p) tensor factorization and factor annihilation bridge.

Establishes the exact Chinese Remainder Theorem (CRT) Bezout phase decomposition for
composite moduli q = q_1 * q_2 with gcd(q_1, q_2) = 1 (specifically q = 2^t * p where
p is an odd prime) and proves that CNOT witness combinations divisible by p or 2^t
completely annihilate one CRT factor while preserving the other:

1. Exact CRT Bezout Idempotent Phase Splitting:
   Let q = q_1 * q_2 with q_1 = 2^t and q_2 = p (odd prime). Let e_1 = p * (p^{-1} mod 2^t)
   and e_2 = 2^t * ((2^t)^{-1} mod p) be the orthogonal CRT idempotents satisfying:
       e_1 + e_2 == 1 (mod q),   e_1 == 1 (mod 2^t), e_1 == 0 (mod p),
                                 e_2 == 0 (mod 2^t), e_2 == 1 (mod p).
   For any label a in Z_q and secret s in Z_q with CRT coordinates s_1 = s mod 2^t and
   s_2 = s mod p, the DCP quantum phase splits additively as:
       exp(2*pi*i * a * s / q) = exp(2*pi*i * a_1_eff * s_1 / 2^t) * exp(2*pi*i * a_2_eff * s_2 / p),
   where a_1_eff = (a * (p^{-1} mod 2^t)) mod 2^t and a_2_eff = (a * ((2^t)^{-1} mod p)) mod p!

2. Exact CRT Factor Annihilation via p-Multiple and 2^t-Multiple CNOT Witnesses:
   - Odd-Prime Factor Annihilation (Isolating Z_{2^t}):
     Whenever a CNOT witness v in {0, 1}^K satisfies A v == 0 (mod p) (while A v == 2*u mod 2^t),
     the effective odd-prime label a_2_eff = 0 (mod p) vanishes identically, so the
     compressed wire phase is 100% independent of s_2 in Z_p (zero trace distance across
     all p values of s_2) and reduces to a pure dyadic even-sublattice state over Z_{2^{t-1}}!
   - Dyadic Factor Annihilation (Isolating Z_p):
     Whenever a witness w satisfies A w == 0 (mod 2^t) and A w != 0 (mod p), the compressed
     wire phase is 100% independent of s_1 in Z_{2^t} (zero trace distance across all 2^t
     values of s_1) and reduces to a pure odd-prime Z_p phase state!
"""

from __future__ import annotations

import cmath
import hashlib
import json
import math
from typing import Any, Dict, List


THEOREM_ID = "dcp_composite_crt_coprime_modulus_tensor_factorization_bridge"
SCHEMA_VERSION = "dcp-composite-crt-coprime-modulus-tensor-factorization-bridge-v1"


def evaluate_crt_composite_modulus_factor_annihilation(
    t_bits: int,
    p_prime: int,
) -> Dict[str, Any]:
    """Verify exact CRT Bezout phase factorization and orthogonal factor annihilation over Z_{2^t * p}."""
    q1 = 1 << t_bits
    q2 = p_prime
    if math.gcd(q1, q2) != 1:
        raise ValueError("q1 = 2^t and q2 = p must be coprime")
    q_total = q1 * q2

    inv_q2_mod_q1 = pow(q2, -1, q1)
    inv_q1_mod_q2 = pow(q1, -1, q2)
    e1 = (q2 * inv_q2_mod_q1) % q_total
    e2 = (q1 * inv_q1_mod_q2) % q_total

    bezout_identity_verified = ((e1 + e2) % q_total == 1) and (e1 % q1 == 1) and (e1 % q2 == 0) and (e2 % q1 == 0) and (e2 % q2 == 1)

    # 1. Verify exact phase splitting across all a in Z_q and s in Z_q:
    max_phase_split_err = 0.0
    for a in range(q_total):
        a1_eff = (a * inv_q2_mod_q1) % q1
        a2_eff = (a * inv_q1_mod_q2) % q2
        for s in range(q_total):
            s1 = s % q1
            s2 = s % q2
            ph_joint = cmath.exp(2j * math.pi * float((a * s) % q_total) / float(q_total))
            ph_split = (
                cmath.exp(2j * math.pi * float((a1_eff * s1) % q1) / float(q1))
                * cmath.exp(2j * math.pi * float((a2_eff * s2) % q2) / float(q2))
            )
            max_phase_split_err = max(max_phase_split_err, abs(ph_joint - ph_split))

    # 2. Witness Type I: A v = 2 * p (mod q) -> divisible by p AND even!
    # Check that its phase is 100% invariant across all s2 in Z_p while varying across s1 in Z_{2^{t-1}}:
    a_type1 = (2 * p_prime) % q_total
    max_s2_leakage_type1 = 0.0
    for s1 in range(q1):
        ref_val = None
        for s2 in range(q2):
            s = (s1 * e1 + s2 * e2) % q_total
            val = cmath.exp(2j * math.pi * float((a_type1 * s) % q_total) / float(q_total))
            if ref_val is None:
                ref_val = val
            else:
                max_s2_leakage_type1 = max(max_s2_leakage_type1, abs(val - ref_val))

    # 3. Witness Type II: A w = 2^t (mod q) -> divisible by 2^t and coprime to p!
    # Check that its phase is 100% invariant across all s1 in Z_{2^t} while varying across s2 in Z_p:
    a_type2 = q1 % q_total
    max_s1_leakage_type2 = 0.0
    for s2 in range(q2):
        ref_val = None
        for s1 in range(q1):
            s = (s1 * e1 + s2 * e2) % q_total
            val = cmath.exp(2j * math.pi * float((a_type2 * s) % q_total) / float(q_total))
            if ref_val is None:
                ref_val = val
            else:
                max_s1_leakage_type2 = max(max_s1_leakage_type2, abs(val - ref_val))

    return {
        "t_bits": t_bits,
        "q1_dyadic": q1,
        "q2_prime": q2,
        "q_composite": q_total,
        "idempotent_e1": e1,
        "idempotent_e2": e2,
        "bezout_identity_verified": bezout_identity_verified,
        "max_crt_phase_splitting_error": max_phase_split_err,
        "max_s2_leakage_under_p_multiple_witness": max_s2_leakage_type1,
        "max_s1_leakage_under_2t_multiple_witness": max_s1_leakage_type2,
        "exact_crt_laws_verified": (
            bezout_identity_verified
            and max_phase_split_err < 1e-12
            and max_s2_leakage_type1 < 1e-12
            and max_s1_leakage_type2 < 1e-12
        ),
    }


def generate_dcp_composite_crt_coprime_modulus_tensor_factorization_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the composite CRT coprime modulus factorization bridge."""
    audit_q12 = evaluate_crt_composite_modulus_factor_annihilation(t_bits=2, p_prime=3)  # q = 4 * 3 = 12
    audit_q24 = evaluate_crt_composite_modulus_factor_annihilation(t_bits=3, p_prime=3)  # q = 8 * 3 = 24
    audit_q40 = evaluate_crt_composite_modulus_factor_annihilation(t_bits=3, p_prime=5)  # q = 8 * 5 = 40

    all_passed = (
        audit_q12["exact_crt_laws_verified"]
        and audit_q24["exact_crt_laws_verified"]
        and audit_q40["exact_crt_laws_verified"]
    )

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "proof_status": "LOCAL_DERIVATION_REVIEW_PENDING_NOT_FORMALLY_VERIFIED",
        "scope_constraints": {
            "applies_to": "Chinese Remainder Theorem Bezout phase splitting and orthogonal factor annihilation over composite moduli q = 2^t * p",
            "does_not_claim": "CRT splitting across prime powers p^k without p-adic carry compensation (see Subsystem 83)",
            "controls_included": "Evaluates q = 12 (4x3), q = 24 (8x3), and q = 40 (8x5) exhaustively across all (a, s) in Z_q^2, verifying < 1e-12 phase splitting error and exact 0.0 cross-factor leakage.",
        },
        "audit_q12_4x3": audit_q12,
        "audit_q24_8x3": audit_q24,
        "audit_q40_8x5": audit_q40,
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
