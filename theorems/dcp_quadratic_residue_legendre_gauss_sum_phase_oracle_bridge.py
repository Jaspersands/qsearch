r"""DCP quadratic residue Legendre-Gauss sum phase oracle bridge.

Establishes the exact closed-form Gauss sum evaluation and Legendre-symbol secret
residuosity phase law when a prime-modulus DCP / hidden-shift state over Z_p (for an
odd prime p) is probed with a quadratic phase reference |psi_quad> = p^{-1/2} sum_{x=0}^{p-1} |x^2 mod p>:

1. Exact Quadratic Gauss Sum Identity Over Z_p:
   For any odd prime p and any non-zero frequency z = (a * s) mod p in {1, ..., p - 1},
   the quadratic Gauss sum:
       G(z; p) = sum_{x=0}^{p-1} exp(2*pi*i * z * x^2 / p)
   satisfies the exact closed-form law:
       G(z; p) = (z / p)_L * eps_p * sqrt(p),
   where (z / p)_L in {-1, +1} is the Legendre symbol (z^{(p-1)/2} mod p) and:
       eps_p = 1   if p == 1 (mod 4),
       eps_p = i   if p == 3 (mod 4).

2.Multiplicative Secret Legendre Extraction:
   Because the Legendre symbol is completely multiplicative:
       ( (a * s) / p )_L = (a / p)_L * (s / p)_L,
   the normalized inner product between the uniform quadratic-phase state
   |Phi_quad(z)> = p^{-1/2} sum_{x=0}^{p-1} exp(2*pi*i * z * x^2 / p) |x> and the zero-frequency
   reference |+_p> = p^{-1/2} sum_{x=0}^{p-1} |x> is:
       <+_p | Phi_quad(a * s)> = G(a * s; p) / p = (a / p)_L * (s / p)_L * (eps_p / sqrt(p)).
   More powerfully, in the p-dimensional Fourier basis, the quadratic Gauss state
   |Gamma_p> = p^{-1/2} sum_{y=1}^{p-1} (y / p)_L |y> is an EXACT eigenstate of the
   p-point Quantum Fourier Transform (up to eps_p), so a single phase kickback with
   |Gamma_p> multiplies the state by the exact binary sign (a / p)_L * (s / p)_L in {-1, +1}
   with unit modulus |(a*s / p)_L| = 1.0 across all non-zero secrets s in F_p^x!
"""

from __future__ import annotations

import cmath
import hashlib
import json
import math
from typing import Any, Dict, List


THEOREM_ID = "dcp_quadratic_residue_legendre_gauss_sum_phase_oracle_bridge"
SCHEMA_VERSION = "dcp-quadratic-residue-legendre-gauss-sum-phase-oracle-bridge-v1"


def legendre_symbol(a: int, p_prime: int) -> int:
    """Compute exact Legendre symbol (a / p) in {-1, 0, +1} via Euler's criterion."""
    a_mod = a % p_prime
    if a_mod == 0:
        return 0
    val = pow(a_mod, (p_prime - 1) // 2, p_prime)
    return 1 if val == 1 else -1


def evaluate_prime_gauss_sum_and_legendre_kickback(p_prime: int) -> Dict[str, Any]:
    """Verify exact Gauss sum law G(z; p) = (z/p) * eps_p * sqrt(p) and Legendre eigenstate phase kickback across all z in F_p^x."""
    if type(p_prime) is not int or p_prime < 3 or (p_prime % 2) == 0:
        raise ValueError("p_prime must be an odd prime >= 3")

    eps_p = 1.0 + 0j if (p_prime % 4) == 1 else 1j
    sqrt_p = math.sqrt(float(p_prime))

    max_gauss_sum_err = 0.0
    max_eigenstate_kickback_err = 0.0
    residue_records: List[Dict[str, Any]] = []

    for z_val in range(1, p_prime):
        leg_z = legendre_symbol(z_val, p_prime)

        # 1. Explicit quadratic Gauss sum G(z; p) = sum_{x=0}^{p-1} exp(2*pi*i * z * x^2 / p)
        g_exp = sum(
            cmath.exp(2j * math.pi * float((z_val * x * x) % p_prime) / float(p_prime))
            for x in range(p_prime)
        )
        g_cf = float(leg_z) * eps_p * sqrt_p
        max_gauss_sum_err = max(max_gauss_sum_err, abs(g_exp - g_cf))

        # 2. Legendre-weighted state kickback: sum_{y=1}^{p-1} (y/p) * exp(2*pi*i * z * y / p) / (eps_p * sqrt(p)) == (z / p)!
        # Wait: since each quadratic residue r != 0 has 2 square roots in F_p^x,
        # sum_{y=1}^{p-1} (y/p) exp(2*pi*i * z * y / p) == sum_{x=0}^{p-1} exp(2*pi*i * z * x^2 / p) = G(z; p)!
        leg_fourier_sum = sum(
            float(legendre_symbol(y, p_prime)) * cmath.exp(2j * math.pi * float((z_val * y) % p_prime) / float(p_prime))
            for y in range(1, p_prime)
        )
        normalized_kickback = leg_fourier_sum / (eps_p * sqrt_p)
        max_eigenstate_kickback_err = max(
            max_eigenstate_kickback_err,
            abs(normalized_kickback - float(leg_z)),
        )

        residue_records.append({
            "z": z_val,
            "legendre_symbol": leg_z,
            "gauss_sum_real": g_exp.real,
            "gauss_sum_imag": g_exp.imag,
            "normalized_legendre_kickback": normalized_kickback.real,
        })

    return {
        "p_prime": p_prime,
        "p_mod_4": p_prime % 4,
        "eps_p_is_imaginary": (p_prime % 4) == 3,
        "max_gauss_sum_error": max_gauss_sum_err,
        "max_eigenstate_kickback_error": max_eigenstate_kickback_err,
        "residue_records": residue_records,
        "exact_laws_verified": (
            max_gauss_sum_err < 1e-11
            and max_eigenstate_kickback_err < 1e-11
        ),
    }


def generate_dcp_quadratic_residue_legendre_gauss_sum_phase_oracle_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the quadratic residue Legendre-Gauss sum bridge."""
    # 1. p == 1 (mod 4) primes: p = 5 and p = 13 (eps_p = 1, real Gauss sums +/- sqrt(p))
    audit_p5 = evaluate_prime_gauss_sum_and_legendre_kickback(p_prime=5)
    audit_p13 = evaluate_prime_gauss_sum_and_legendre_kickback(p_prime=13)

    # 2. p == 3 (mod 4) primes: p = 7 and p = 11 (eps_p = i, purely imaginary Gauss sums +/- i*sqrt(p))
    audit_p7 = evaluate_prime_gauss_sum_and_legendre_kickback(p_prime=7)
    audit_p11 = evaluate_prime_gauss_sum_and_legendre_kickback(p_prime=11)

    all_passed = (
        audit_p5["exact_laws_verified"]
        and not audit_p5["eps_p_is_imaginary"]
        and audit_p13["exact_laws_verified"]
        and not audit_p13["eps_p_is_imaginary"]
        and audit_p7["exact_laws_verified"]
        and audit_p7["eps_p_is_imaginary"]
        and audit_p11["exact_laws_verified"]
        and audit_p11["eps_p_is_imaginary"]
    )

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "proof_status": "LOCAL_DERIVATION_REVIEW_PENDING_NOT_FORMALLY_VERIFIED",
        "scope_constraints": {
            "applies_to": "Quadratic Gauss sums G(z; p) = (z/p) * eps_p * sqrt(p) and Legendre-eigenstate binary sign kickback over prime moduli Z_p",
            "does_not_claim": "Coherent synthesis of the quadratic residue superposition from uncontrolled random single-qubit headers without coherent modular multiplication",
            "controls_included": "Evaluates p in {5, 13} (p == 1 mod 4, eps_p = 1) and p in {7, 11} (p == 3 mod 4, eps_p = i), verifying < 1e-11 Gauss sum and Legendre kickback error across all non-zero residues.",
        },
        "audit_p5_mod4_eq1": audit_p5,
        "audit_p7_mod4_eq3": audit_p7,
        "audit_p11_mod4_eq3": audit_p11,
        "audit_p13_mod4_eq1": audit_p13,
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
