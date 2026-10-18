r"""DCP dihedral sign-inversion vs. Heisenberg H_3(Z_{2^t}) / H_3(Z_p) two-copy commutator bridge.

Establishes the exact finite-difference QFT concentration and dyadic boundary-cocycle law
for Heisenberg coset states H_3(Z_q) compared against dihedral sign-inversion states:

1. Odd-Prime Heisenberg H_3(Z_p) Exact Unit Concentration (p >= 3 odd prime):
   Because 2 is invertible modulo any odd prime p (2^{-1} == (p + 1)/2 mod p), the
   binomial phase C(x, 2) = x(x - 1)/2 mod p is strictly p-periodic:
       C(x + p, 2) == C(x, 2) (mod p).
   Consequently, for |psi_H(s_1, s_2; y_0)> = p^{-1/2} sum_{x in Z_p} omega_p^{x(s_2 + y_0) + C(x, 2) s_1} |x>,
   coherent shift-difference x_2 == (x_1 + Delta) mod p at a common anchor y_0 concentrates
   QFT_p^dagger on wire x_1 onto k_1 == (Delta * s_1) mod p with probability 1.0 for ALL
   shifts Delta in Z_p and ALL secrets (s_1, s_2).

2. Dyadic Heisenberg H_3(Z_{2^t}) Boundary-Cocycle Law ((1 - 2*Delta/2^t)^2 for Odd s_1):
   Over Z_{2^t}, (1, s_1, s_2)^{2^t} = (0, 0, 2^{t-1} s_1 mod 2^t), so C(x + 2^t, 2) == C(x, 2) + 2^{t-1} (mod 2^t).
   Under modular wrap-around x_2 = (x_1 + Delta) mod 2^t (0 <= Delta < 2^t), the last Delta
   basis states x_1 in {2^t - Delta, ..., 2^t - 1} acquire a half-period carry phase
   2^{t-1} s_1 mod 2^t (sign (-1)^{s_1}), yielding the exact closed-form QFT_{2^t}^dagger peak probability:
       P_{QFT_{2^t}}(k_1 = Delta * s_1 mod 2^t) = 1.0                      if s_1 == 0 (mod 2),
       P_{QFT_{2^t}}(k_1 = Delta * s_1 mod 2^t) = (1 - 2 * Delta / 2^t)^2  if s_1 == 1 (mod 2).
   In particular, for odd s_1, unit shift Delta = 1 achieves peak probability (1 - 2^{1-t})^2 -> 1,
   whereas the half-period shift Delta = 2^{t-1} suffers complete destructive interference (P = 0).

3. Independent-Anchor Shift Aliasing Countercontrol:
   When two copies have independent unmeasured bilinear anchors y_{0,1} != y_{0,2}, the
   QFT peak shifts to k_1 == Delta * s_1 + (y_{0,2} - y_{0,1}) (mod q), aliasing Delta * s_1
   with the anchor difference unless the second register is measured or shared.
"""

from __future__ import annotations

import cmath
import hashlib
import json
import math
from typing import Any, Dict, List


THEOREM_ID = "dcp_dihedral_vs_heisenberg_two_copy_commutant_bridge"
SCHEMA_VERSION = "dcp-dihedral-vs-heisenberg-two-copy-commutant-bridge-v1"


def heisenberg_qft_distribution_explicit(
    q_mod: int,
    s1: int,
    s2: int,
    y0_1: int,
    y0_2: int,
    delta_shift: int,
    use_mod_p_inv2: bool = False,
) -> List[float]:
    """Compute explicit QFT_q^dagger distribution on x_1 conditioned on x_2 = (x_1 + delta_shift) mod q."""
    inv2 = ((q_mod + 1) // 2) if use_mod_p_inv2 else None
    amps_x1: List[complex] = []
    for x1 in range(q_mod):
        x2 = (x1 + delta_shift) % q_mod
        if use_mod_p_inv2 and inv2 is not None:
            c_x1 = (x1 * (x1 - 1) * inv2) % q_mod
            c_x2 = (x2 * (x2 - 1) * inv2) % q_mod
        else:
            c_x1 = (x1 * (x1 - 1)) // 2
            c_x2 = (x2 * (x2 - 1)) // 2
        phi1 = (x1 * (s2 + y0_1) + c_x1 * s1) % q_mod
        phi2 = (x2 * (s2 + y0_2) + c_x2 * s1) % q_mod
        diff_phi = (phi2 - phi1) % q_mod
        amps_x1.append(cmath.exp(2j * math.pi * diff_phi / float(q_mod)) / math.sqrt(float(q_mod)))

    probs_k1: List[float] = []
    for k1 in range(q_mod):
        amp_k = sum(
            amps_x1[x1] * cmath.exp(-2j * math.pi * (x1 * k1) / float(q_mod)) / math.sqrt(float(q_mod))
            for x1 in range(q_mod)
        )
        probs_k1.append(abs(amp_k) ** 2)
    return probs_k1


def verify_odd_prime_heisenberg_unit_concentration(
    p_mod: int,
    s1: int,
    s2: int,
    y0: int,
) -> Dict[str, Any]:
    """Verify 100% QFT_p concentration at k_1 == Delta * s_1 mod p across all Delta in Z_p."""
    if type(p_mod) is not int or p_mod < 3 or (p_mod % 2) == 0:
        raise ValueError("p_mod must be an odd integer >= 3")
    s1_m, s2_m, y0_m = int(s1) % p_mod, int(s2) % p_mod, int(y0) % p_mod
    max_err = 0.0
    for delta in range(p_mod):
        probs = heisenberg_qft_distribution_explicit(
            q_mod=p_mod, s1=s1_m, s2=s2_m, y0_1=y0_m, y0_2=y0_m, delta_shift=delta, use_mod_p_inv2=True
        )
        target_k1 = (delta * s1_m) % p_mod
        max_err = max(max_err, abs(probs[target_k1] - 1.0))

    # Independent anchor shift alias control
    y0_other = (y0_m + 2) % p_mod
    probs_alias = heisenberg_qft_distribution_explicit(
        q_mod=p_mod, s1=s1_m, s2=s2_m, y0_1=y0_m, y0_2=y0_other, delta_shift=1, use_mod_p_inv2=True
    )
    shifted_k1 = (s1_m + (y0_other - y0_m)) % p_mod

    return {
        "p_mod": p_mod,
        "s1": s1_m,
        "s2": s2_m,
        "y0": y0_m,
        "max_unit_concentration_error": max_err,
        "independent_anchor_alias_verified": abs(probs_alias[shifted_k1] - 1.0) < 1e-12,
        "exact_odd_prime_law_verified": max_err < 1e-12 and abs(probs_alias[shifted_k1] - 1.0) < 1e-12,
    }


def verify_dyadic_heisenberg_boundary_cocycle_law(
    t_bits: int,
    s1: int,
    s2: int,
    y0: int,
) -> Dict[str, Any]:
    """Verify exact peak probability (1 - 2*Delta/2^t)^2 for odd s_1 and 1.0 for even s_1 in H_3(Z_{2^t})."""
    if type(t_bits) is not int or not 2 <= t_bits <= 5:
        raise ValueError("t_bits must be in [2, 5]")
    q = 1 << t_bits
    s1_m, s2_m, y0_m = int(s1) % q, int(s2) % q, int(y0) % q
    is_odd_s1 = (s1_m % 2) == 1

    max_formula_err = 0.0
    delta_records: List[Dict[str, Any]] = []
    for delta in range(q):
        probs = heisenberg_qft_distribution_explicit(
            q_mod=q, s1=s1_m, s2=s2_m, y0_1=y0_m, y0_2=y0_m, delta_shift=delta, use_mod_p_inv2=False
        )
        target_k1 = (delta * s1_m) % q
        emp_prob = probs[target_k1]
        cf_prob = ((1.0 - (2.0 * float(delta)) / float(q)) ** 2) if is_odd_s1 else 1.0
        max_formula_err = max(max_formula_err, abs(emp_prob - cf_prob))
        delta_records.append({
            "delta": delta,
            "target_k1": target_k1,
            "empirical_peak_prob": emp_prob,
            "closed_form_peak_prob": cf_prob,
        })

    return {
        "t_bits": t_bits,
        "q_mod": q,
        "s1": s1_m,
        "s1_is_odd": is_odd_s1,
        "max_cocycle_formula_error": max_formula_err,
        "delta_1_peak_prob": delta_records[1]["empirical_peak_prob"],
        "half_period_delta_peak_prob": delta_records[q // 2]["empirical_peak_prob"],
        "exact_boundary_cocycle_law_verified": max_formula_err < 1e-12,
    }


def generate_dcp_dihedral_vs_heisenberg_two_copy_commutant_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the dihedral vs Heisenberg two-copy commutant bridge."""
    odd_prime_audit = verify_odd_prime_heisenberg_unit_concentration(
        p_mod=7, s1=5, s2=3, y0=4
    )
    dyadic_odd_s1_audit = verify_dyadic_heisenberg_boundary_cocycle_law(
        t_bits=3, s1=5, s2=3, y0=6
    )
    dyadic_even_s1_audit = verify_dyadic_heisenberg_boundary_cocycle_law(
        t_bits=3, s1=6, s2=3, y0=5
    )

    all_passed = (
        odd_prime_audit["exact_odd_prime_law_verified"]
        and dyadic_odd_s1_audit["exact_boundary_cocycle_law_verified"]
        and abs(dyadic_odd_s1_audit["delta_1_peak_prob"] - 0.5625) < 1e-12
        and abs(dyadic_odd_s1_audit["half_period_delta_peak_prob"] - 0.0) < 1e-12
        and dyadic_even_s1_audit["exact_boundary_cocycle_law_verified"]
        and abs(dyadic_even_s1_audit["half_period_delta_peak_prob"] - 1.0) < 1e-12
    )

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "proof_status": "LOCAL_DERIVATION_REVIEW_PENDING_NOT_FORMALLY_VERIFIED",
        "scope_constraints": {
            "applies_to": "Quadratic-chirp finite-difference QFT elimination in H_3(Z_p) and H_3(Z_{2^t})",
            "does_not_claim": "Boundary-free unit QFT concentration in H_3(Z_{2^t}) when s_1 is odd and Delta > 0, or dechirping across independent unmeasured anchors y_{0,1} != y_{0,2}",
            "controls_included": "Includes exact unit concentration in odd-prime H_3(Z_7), exact (1 - 2*Delta/2^t)^2 boundary-cocycle law in dyadic H_3(Z_8) for odd s_1=5 (0.5625 at Delta=1 and 0.0 at Delta=4), unit concentration for even s_1=6, and independent-anchor aliasing.",
        },
        "odd_prime_heisenberg_audit": odd_prime_audit,
        "dyadic_odd_s1_boundary_cocycle_audit": dyadic_odd_s1_audit,
        "dyadic_even_s1_constructive_control": dyadic_even_s1_audit,
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
