"""Native higher-call composite-modulus CRT factorization audit and archimedean window coupling control.

Establishes for any coprime composite modulus q = q1 * q2 (gcd(q1, q2) = 1):

1. Exact Additive Character and Twisted Frequency CRT Bijection:
   Let e1 = q2 * (q2^{-1} mod q1) and e2 = q1 * (q1^{-1} mod q2) be the orthogonal
   CRT idempotents mod q. For all y, z in Z_q:
       exp(2*pi*i * y*z / q) = exp(2*pi*i * y1 * z1 / q1) * exp(2*pi*i * y2 * z2 / q2)
   where z1 = z mod q1, z2 = z mod q2, y1 = y * (q2^{-1} mod q1) mod q1, and
   y2 = y * (q1^{-1} mod q2) mod q2.

2. Exact CRT Factorization for Product Error Channels:
   Whenever an error distribution P_q(e) on Z_q factors across its CRT marginals
   P_q(e) = P_{q1}(e mod q1) * P_{q2}(e mod q2), its Fourier survival spectrum and
   valid-check probability for any check matrix B in Z_q^{d x n} factor identically:
       hat_P_q(y) = hat_P_{q1}(y1) * hat_P_{q2}(y2),
       P_valid^{(q)}(B) = P_valid^{(q1)}(B mod q1) * P_valid^{(q2)}(B mod q2).

3. Scoped Archimedean Contiguous-Window Countercontrol:
   When P_q(e) is a contiguous archimedean window on Z_q whose support size |W| is not
   a multiple of q1 or q2 (e.g. q = 6 = 2 * 3 with contiguous window W = {0, 1}),
   the CRT coordinates (e mod q1, e mod q2) are statistically coupled
   (TV distance from product of marginals > 0) and hat_P_q(y) != hat_P_{q1}(y1) * hat_P_{q2}(y2).
"""

from __future__ import annotations

import cmath
import hashlib
import itertools
import json
import math
from typing import Any, Dict, List, Sequence, Tuple


THEOREM_ID = "native_higher_call_composite_modulus_crt_factorization_audit"
SCHEMA_VERSION = "native-higher-call-composite-modulus-crt-factorization-audit-v1"


def mod_inverse(a: int, m: int) -> int:
    """Compute modular inverse of a mod m."""
    return pow(a, -1, m)


def crt_twisted_frequency(y: int, q1: int, q2: int) -> Tuple[int, int]:
    """Return (y1, y2) = (y * (q2^{-1} mod q1) mod q1, y * (q1^{-1} mod q2) mod q2)."""
    inv_q2_mod_q1 = mod_inverse(q2, q1)
    inv_q1_mod_q2 = mod_inverse(q1, q2)
    return (y * inv_q2_mod_q1) % q1, (y * inv_q1_mod_q2) % q2


def verify_crt_character_and_product_channel_factorization(
    q1: int,
    q2: int,
    p1: Sequence[float],
    p2: Sequence[float],
    b_matrix: Sequence[Sequence[int]],
) -> Dict[str, Any]:
    """Verify exact character factorization, Fourier spectrum factorization, and P_valid factorization."""
    if math.gcd(q1, q2) != 1:
        raise ValueError("q1 and q2 must be coprime.")
    q = q1 * q2
    inv_q2_q1 = mod_inverse(q2, q1)
    inv_q1_q2 = mod_inverse(q1, q2)
    e1 = (q2 * inv_q2_q1) % q
    e2 = (q1 * inv_q1_q2) % q

    # Reconstruct composite product distribution P_q(e) = P_{q1}(e mod q1) * P_{q2}(e mod q2)
    p_q = [float(p1[e % q1]) * float(p2[e % q2]) for e in range(q)]

    max_char_err = 0.0
    for y in range(q):
        y1, y2 = crt_twisted_frequency(y, q1, q2)
        for z in range(q):
            z1, z2 = z % q1, z % q2
            lhs = cmath.exp(2j * math.pi * (y * z) / float(q))
            rhs = cmath.exp(2j * math.pi * (y1 * z1) / float(q1)) * cmath.exp(
                2j * math.pi * (y2 * z2) / float(q2)
            )
            err = abs(lhs - rhs)
            if err > max_char_err:
                max_char_err = err

    def fourier_table(probs: Sequence[float], mod_q: int) -> List[complex]:
        return [
            sum(
                probs[e] * cmath.exp(2j * math.pi * (freq * e) / float(mod_q))
                for e in range(mod_q)
            )
            for freq in range(mod_q)
        ]

    hat_q = fourier_table(p_q, q)
    hat_1 = fourier_table(p1, q1)
    hat_2 = fourier_table(p2, q2)

    max_fourier_err = 0.0
    for y in range(q):
        y1, y2 = crt_twisted_frequency(y, q1, q2)
        err = abs(hat_q[y] - hat_1[y1] * hat_2[y2])
        if err > max_fourier_err:
            max_fourier_err = err

    # Verify P_valid(B) factorization
    d_rows = len(b_matrix)
    n_cols = len(b_matrix[0])

    def valid_check_prob(probs: Sequence[float], mod_q: int) -> float:
        total = 0.0
        for z in itertools.product(range(mod_q), repeat=n_cols):
            ok = all(
                sum(int(b_matrix[r][c]) * z[c] for c in range(n_cols)) % mod_q == 0
                for r in range(d_rows)
            )
            if ok:
                prob = 1.0
                for c in range(n_cols):
                    prob *= probs[z[c]]
                total += prob
        return total

    p_valid_q = valid_check_prob(p_q, q)
    p_valid_q1 = valid_check_prob(p1, q1)
    p_valid_q2 = valid_check_prob(p2, q2)
    p_valid_diff = abs(p_valid_q - p_valid_q1 * p_valid_q2)

    return {
        "q1": q1,
        "q2": q2,
        "q": q,
        "idempotents": [e1, e2],
        "idempotent_sum_mod_q": (e1 + e2) % q,
        "max_character_factorization_error": max_char_err,
        "max_fourier_factorization_error": max_fourier_err,
        "p_valid_q": p_valid_q,
        "p_valid_q1": p_valid_q1,
        "p_valid_q2": p_valid_q2,
        "p_valid_product": p_valid_q1 * p_valid_q2,
        "p_valid_factorization_abs_diff": p_valid_diff,
        "exact_crt_factorization": (
            max_char_err < 1e-12 and max_fourier_err < 1e-12 and p_valid_diff < 1e-12
        ),
    }


def verify_non_factoring_window_crt_coupling_control(
    q1: int,
    q2: int,
    window_support: Sequence[int],
) -> Dict[str, Any]:
    """Verify that a contiguous archimedean window with |W| not divisible by q1 or q2 couples CRT marginals."""
    q = q1 * q2
    p_q = [0.0] * q
    for e in window_support:
        p_q[e % q] += 1.0 / float(len(window_support))

    p1 = [0.0] * q1
    p2 = [0.0] * q2
    for e in range(q):
        p1[e % q1] += p_q[e]
        p2[e % q2] += p_q[e]

    tv_distance_from_product = 0.5 * sum(
        abs(p_q[e] - p1[e % q1] * p2[e % q2]) for e in range(q)
    )

    # Check Fourier discrepancy at y = 1
    y1, y2 = crt_twisted_frequency(1, q1, q2)
    hat_q_1 = sum(p_q[e] * cmath.exp(2j * math.pi * e / float(q)) for e in range(q))
    hat_1_y1 = sum(p1[e1] * cmath.exp(2j * math.pi * y1 * e1 / float(q1)) for e1 in range(q1))
    hat_2_y2 = sum(p2[e2] * cmath.exp(2j * math.pi * y2 * e2 / float(q2)) for e2 in range(q2))
    fourier_coupling_gap = abs(hat_q_1 - hat_1_y1 * hat_2_y2)

    return {
        "q1": q1,
        "q2": q2,
        "q": q,
        "window_support": list(window_support),
        "tv_distance_from_crt_product": tv_distance_from_product,
        "fourier_y1_coupling_gap": fourier_coupling_gap,
        "archimedean_window_couples_crt_factors": (
            tv_distance_from_product > 1e-6 and fourier_coupling_gap > 1e-6
        ),
    }


def generate_native_higher_call_composite_modulus_crt_factorization_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for composite-modulus CRT factorization and window coupling."""
    crt_audit = verify_crt_character_and_product_channel_factorization(
        q1=2,
        q2=3,
        p1=[0.75, 0.25],
        p2=[0.6, 0.2, 0.2],
        b_matrix=[[1, 2, 5]],
    )
    window_control = verify_non_factoring_window_crt_coupling_control(
        q1=2,
        q2=3,
        window_support=[0, 1],
    )
    all_passed = (
        crt_audit["exact_crt_factorization"]
        and window_control["archimedean_window_couples_crt_factors"]
    )
    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "scope_constraints": {
            "applies_to": "Composite coprime moduli q = q1 * q2 with gcd(q1, q2) = 1 under CRT-product error channels",
            "does_not_claim": "CRT independence for non-divisible contiguous archimedean windows",
            "controls_included": "Includes both exact CRT-product channel factorization and the contiguous window W={0,1} mod 6 countercontrol where CRT marginals are statistically coupled.",
        },
        "crt_product_channel_audit": crt_audit,
        "contiguous_window_coupling_control": window_control,
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
