"""Planted q-ary MacWilliams dual weight enumerator and noisy QFT check survival bridge.

Establishes three exact identities for any rank-d check matrix B in F_q^{d x n}
over a prime field F_q:

1. Exact q-ary MacWilliams Krawtchouk Identity:
   Let A_w(B) = |{u in F_q^d : wt_H(u^T B) = w}| be the weight enumerator of the row
   space C_B = rowspace(B), and A_k^perp(B) = |{z in ker(B) : wt_H(z) = k}| be the
   weight enumerator of the dual code C_B^perp = ker(B). Then for all 0 <= k <= n:
       A_k^perp(B) = q^{-d} sum_{w=0}^n A_w(B) K_k(w; n, q),
   where K_k(w; n, q) = sum_{j=0}^k (-1)^j (q-1)^{k-j} C(w, j) C(n-w, k-j).

2. Noisy QFT_q^{tensor n} Valid-Check Probability Bridge:
   Under a q-ary depolarizing error channel with parameter gamma in [0, 1] (where each
   coordinate is uncorrupted with probability p_0 = 1 - gamma*(q-1)/q and takes each of
   the q-1 nonzero shifts with probability p_{!=0} = gamma/q), the probability that a
   noisy sample z in F_q^n lies in ker(B) satisfies:
       P_valid(B, gamma) = sum_{k=0}^n A_k^perp(B) p_0^{n-k} p_{!=0}^k
                         = q^{-d} sum_{w=0}^n A_w(B) (1 - gamma)^w.

3. Off-Dual vs. On-Dual Secret Dichotomy (Scoped Controls):
   - Off-Dual Surjectivity Control (B s != 0 mod q): As s ranges uniformly over F_q^n,
     for every nonzero row-space vector c = u^T B != 0, <c, s> mod q is uniform over F_q,
     and the polynomial generating identity sum_{w=0}^n A_w(B) (1 - gamma)^w = q^d P_valid(B, gamma)
     locks the check-space survival polynomial directly to the dual weight enumerator.
   - On-Dual Constructive Control (s in ker(B), B s = 0 mod q): Every row-space check
     c = u^T B satisfies <c, s> = u^T (B s) = 0 mod q deterministically, demonstrating
     that dual-code alignment is undefeated by row-space averaging.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from typing import Any, Dict, List, Sequence, Tuple


THEOREM_ID = "planted_qary_macwilliams_dual_weight_enumerator_bridge"
SCHEMA_VERSION = "planted-qary-macwilliams-dual-weight-enumerator-bridge-v1"


def krawtchouk_qary(k: int, w: int, n: int, q: int) -> int:
    """Compute the exact q-ary Krawtchouk polynomial K_k(w; n, q)."""
    total = 0
    for j in range(k + 1):
        if j <= w and (k - j) <= (n - w):
            term = (
                ((-1) ** j)
                * ((q - 1) ** (k - j))
                * math.comb(w, j)
                * math.comb(n - w, k - j)
            )
            total += term
    return total


def rowspace_and_dual_weight_enumerators(
    b_matrix: Sequence[Sequence[int]],
    q: int,
) -> Dict[str, Any]:
    """Compute exact rowspace weight enumerator A_w(B) and dual weight enumerator A_k^perp(B)."""
    d_rows = len(b_matrix)
    n_cols = len(b_matrix[0])
    a_w = [0] * (n_cols + 1)
    for u in itertools.product(range(q), repeat=d_rows):
        codeword = [
            sum(u[r] * int(b_matrix[r][c]) for r in range(d_rows)) % q
            for c in range(n_cols)
        ]
        wt = sum(1 for x in codeword if x != 0)
        a_w[wt] += 1

    a_perp = [0] * (n_cols + 1)
    for z in itertools.product(range(q), repeat=n_cols):
        syndrome_zero = all(
            sum(int(b_matrix[r][c]) * z[c] for c in range(n_cols)) % q == 0
            for r in range(d_rows)
        )
        if syndrome_zero:
            wt = sum(1 for x in z if x != 0)
            a_perp[wt] += 1

    macwilliams_perp = []
    for k in range(n_cols + 1):
        val = sum(a_w[w] * krawtchouk_qary(k, w, n_cols, q) for w in range(n_cols + 1))
        macwilliams_perp.append(val / float(q ** d_rows))

    exact_match = all(
        abs(a_perp[k] - macwilliams_perp[k]) < 1e-12 for k in range(n_cols + 1)
    )
    return {
        "q": q,
        "d": d_rows,
        "n": n_cols,
        "rowspace_weights_A_w": a_w,
        "dual_weights_A_k_perp": a_perp,
        "macwilliams_reconstructed_dual": macwilliams_perp,
        "macwilliams_identity_exact": exact_match,
    }


def verify_noisy_qft_valid_check_macwilliams_bridge(
    b_matrix: Sequence[Sequence[int]],
    q: int,
    gamma: float,
) -> Dict[str, Any]:
    """Verify P_valid(B, gamma) == q^{-d} sum_w A_w(B) (1 - gamma)^w."""
    enum = rowspace_and_dual_weight_enumerators(b_matrix, q)
    n_cols = enum["n"]
    d_rows = enum["d"]
    a_w = enum["rowspace_weights_A_w"]
    a_perp = enum["dual_weights_A_k_perp"]

    p0 = 1.0 - gamma * (q - 1.0) / float(q)
    p_err = gamma / float(q)

    p_valid_dual_sum = sum(
        a_perp[k] * (p0 ** (n_cols - k)) * (p_err ** k)
        for k in range(n_cols + 1)
    )
    p_valid_primal_poly = sum(
        a_w[w] * ((1.0 - gamma) ** w) for w in range(n_cols + 1)
    ) / float(q ** d_rows)

    return {
        "q": q,
        "d": d_rows,
        "n": n_cols,
        "gamma": gamma,
        "p_valid_dual_sum": p_valid_dual_sum,
        "p_valid_primal_poly": p_valid_primal_poly,
        "abs_diff": abs(p_valid_dual_sum - p_valid_primal_poly),
        "bridge_identity_exact": abs(p_valid_dual_sum - p_valid_primal_poly) < 1e-12,
        "macwilliams_identity_exact": enum["macwilliams_identity_exact"],
    }


def verify_secret_syndrome_controls(
    b_matrix: Sequence[Sequence[int]],
    q: int,
    s_off_dual: Sequence[int],
    s_on_dual: Sequence[int],
) -> Dict[str, Any]:
    """Verify off-dual character orthogonality vs. on-dual constructive alignment."""
    d_rows = len(b_matrix)
    n_cols = len(b_matrix[0])

    def syndrome(s_vec: Sequence[int]) -> Tuple[int, ...]:
        return tuple(
            sum(int(b_matrix[r][c]) * int(s_vec[c]) for c in range(n_cols)) % q
            for r in range(d_rows)
        )

    syn_off = syndrome(s_off_dual)
    syn_on = syndrome(s_on_dual)

    off_dual_zero_dot_count = 0
    on_dual_zero_dot_count = 0
    total_u = q ** d_rows
    for u in itertools.product(range(q), repeat=d_rows):
        dot_off = sum(u[r] * syn_off[r] for r in range(d_rows)) % q
        dot_on = sum(u[r] * syn_on[r] for r in range(d_rows)) % q
        if dot_off == 0:
            off_dual_zero_dot_count += 1
        if dot_on == 0:
            on_dual_zero_dot_count += 1

    return {
        "q": q,
        "d": d_rows,
        "n": n_cols,
        "s_off_dual_syndrome": list(syn_off),
        "s_on_dual_syndrome": list(syn_on),
        "off_dual_orthogonal_fraction": off_dual_zero_dot_count / float(total_u),
        "expected_off_dual_fraction": 1.0 / float(q),
        "on_dual_orthogonal_fraction": on_dual_zero_dot_count / float(total_u),
        "off_dual_exact_one_over_q": abs(off_dual_zero_dot_count / float(total_u) - 1.0 / float(q)) < 1e-12,
        "on_dual_constructive_alignment_unit": on_dual_zero_dot_count == total_u,
    }


def generate_planted_qary_macwilliams_dual_weight_enumerator_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the q-ary MacWilliams dual weight enumerator bridge."""
    b_f3 = [
        [1, 0, 1, 2],
        [0, 1, 1, 1],
    ]
    b_f2 = [
        [1, 1, 0, 1, 0],
        [0, 1, 1, 0, 1],
    ]

    checks = [
        verify_noisy_qft_valid_check_macwilliams_bridge(b_f3, q=3, gamma=0.25),
        verify_noisy_qft_valid_check_macwilliams_bridge(b_f3, q=3, gamma=0.6),
        verify_noisy_qft_valid_check_macwilliams_bridge(b_f2, q=2, gamma=0.3),
    ]

    # For b_f3 over F_3:
    # z = (2, 2, 1, 0) has B z = (2+1, 2+1) = (0, 0) mod 3 -> on-dual constructive control!
    # s = (1, 0, 0, 0) has B s = (1, 0) != (0, 0) mod 3 -> off-dual control!
    syndrome_controls = verify_secret_syndrome_controls(
        b_matrix=b_f3,
        q=3,
        s_off_dual=[1, 0, 0, 0],
        s_on_dual=[2, 2, 1, 0],
    )

    all_passed = (
        all(c["macwilliams_identity_exact"] and c["bridge_identity_exact"] for c in checks)
        and syndrome_controls["off_dual_exact_one_over_q"]
        and syndrome_controls["on_dual_constructive_alignment_unit"]
    )

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "scope_constraints": {
            "applies_to": "Rank-d check matrices B in F_q^{d x n} under symmetric q-ary local depolarizing noise",
            "does_not_claim": "Impossibility when the secret s lies in the dual code ker(B)",
            "controls_included": "Includes both off-dual secret control (B s != 0 -> orthogonal fraction 1/q) and on-dual constructive control (s in ker(B) -> orthogonal fraction 1.0).",
        },
        "macwilliams_and_valid_check_audits": checks,
        "secret_syndrome_controls": syndrome_controls,
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
