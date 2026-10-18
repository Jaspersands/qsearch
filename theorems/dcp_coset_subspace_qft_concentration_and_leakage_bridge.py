"""DCP coset-subspace H^{tensor m} concentration and non-half-period leakage bridge.

Establishes for any m-wire compressed DCP phase state
    |psi(s; tilde_A)> = 2^{-m/2} sum_{u in {0,1}^m} exp(2*pi*i * <tilde_A u, s> / 2^t) |u>
with wire phase angles theta_j(s) = 2*pi * <tilde_A_j, s> / 2^t (j = 1, ..., m):

1. Exact Tensor-Product Hadamard Output Distribution:
   Applying H^{tensor m} to |psi(s; tilde_A)> yields the exact product distribution over z in {0,1}^m:
       P_{H^{tensor m}}(z | tilde_A, s) = prod_{j=1}^m cos^2((theta_j(s) - pi * z_j) / 2)
                                        = prod_{j=1}^m ((1 + (1 - 2*z_j)*cos(theta_j(s))) / 2).

2. Exact Total-Variation Distance from the Zero-Shift Reference delta_{0^m}:
   Since P_{H^{tensor m}}(z | tilde_A, 0) = 1[z == 0^m], the exact total-variation distance
   between the Hadamard readout at shift s and at s = 0 is:
       D_TV(P_{H^{tensor m}}(. | tilde_A, s), delta_{0^m}) = 1 - P_{H^{tensor m}}(0^m | tilde_A, s)
                                                           = 1 - prod_{j=1}^m cos^2(theta_j(s) / 2).

3. Scoped Half-Period Deterministic Concentration vs. Carry-Phase Leakage:
   - Half-Period Constructive Concentration Control: Whenever <tilde_A_j, s> == 2^{t-1} * b_j (mod 2^t)
     with b_j in {0, 1} for all j = 1, ..., m (so theta_j(s) = pi * b_j), P_{H^{tensor m}}(z = b) = 1.0
     with zero leakage across the other 2^m - 1 bitstrings.
   - Non-Half-Period Leakage Regime: Whenever any wire j has <tilde_A_j, s> not in {0, 2^{t-1}} mod 2^t,
     wire j has Shannon entropy H_2(cos^2(theta_j(s)/2)) > 0 and spreads probability across both z_j = 0 and z_j = 1.
"""

from __future__ import annotations

import cmath
import hashlib
import itertools
import json
import math
from typing import Any, Dict, List, Sequence, Tuple


THEOREM_ID = "dcp_coset_subspace_qft_concentration_and_leakage_bridge"
SCHEMA_VERSION = "dcp-coset-subspace-qft-concentration-and-leakage-bridge-v1"


def hadamard_distribution_explicit_transform(
    tilde_a_cols: Sequence[Sequence[int]],
    s_vec: Sequence[int],
    t_bits: int,
) -> Dict[Tuple[int, ...], float]:
    """Compute P_{H^{tensor m}}(z) by explicit 2^m x 2^m Walsh-Hadamard summation."""
    q_mod = 1 << t_bits
    m_wires = len(tilde_a_cols)
    n_rows = len(s_vec)
    all_u = list(itertools.product((0, 1), repeat=m_wires))

    # State amplitudes in computational basis |u>
    amps_u = {}
    for u in all_u:
        dot = sum(
            int(tilde_a_cols[j][i]) * u[j] * int(s_vec[i])
            for j in range(m_wires)
            for i in range(n_rows)
        ) % q_mod
        amps_u[u] = cmath.exp(2j * math.pi * dot / float(q_mod)) / math.sqrt(float(1 << m_wires))

    probs_z: Dict[Tuple[int, ...], float] = {}
    for z in all_u:
        amp_z = sum(
            amps_u[u]
            * ((-1.0) ** sum(u[j] * z[j] for j in range(m_wires)))
            / math.sqrt(float(1 << m_wires))
            for u in all_u
        )
        probs_z[z] = abs(amp_z) ** 2
    return probs_z


def verify_hadamard_product_law_and_tv_identity(
    tilde_a_cols: Sequence[Sequence[int]],
    s_vec: Sequence[int],
    t_bits: int,
) -> Dict[str, Any]:
    """Verify exact match between explicit Walsh-Hadamard probabilities, cosine-squared product law, and TV formula."""
    q_mod = 1 << t_bits
    m_wires = len(tilde_a_cols)
    n_rows = len(s_vec)

    thetas = [
        2.0 * math.pi * (sum(int(tilde_a_cols[j][i]) * int(s_vec[i]) for i in range(n_rows)) % q_mod) / float(q_mod)
        for j in range(m_wires)
    ]

    explicit_probs = hadamard_distribution_explicit_transform(tilde_a_cols, s_vec, t_bits)
    max_product_law_err = 0.0
    for z, p_exp in explicit_probs.items():
        p_prod = 1.0
        for j in range(m_wires):
            p_prod *= math.cos(0.5 * (thetas[j] - math.pi * z[j])) ** 2
        err = abs(p_exp - p_prod)
        if err > max_product_law_err:
            max_product_law_err = err

    zero_tuple = tuple([0] * m_wires)
    tv_empirical = 0.5 * sum(
        abs(p_exp - (1.0 if z == zero_tuple else 0.0))
        for z, p_exp in explicit_probs.items()
    )
    tv_closed_form = 1.0 - math.prod(math.cos(0.5 * th) ** 2 for th in thetas)
    max_prob = max(explicit_probs.values())

    return {
        "m": m_wires,
        "t": t_bits,
        "max_product_law_error": max_product_law_err,
        "tv_distance_from_zero_shift_empirical": tv_empirical,
        "tv_distance_from_zero_shift_closed_form": tv_closed_form,
        "tv_formula_error": abs(tv_empirical - tv_closed_form),
        "max_single_outcome_probability": max_prob,
        "exact_product_and_tv_verified": (
            max_product_law_err < 1e-12 and abs(tv_empirical - tv_closed_form) < 1e-12
        ),
    }


def generate_dcp_coset_subspace_qft_concentration_and_leakage_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the coset-subspace H^{tensor m} concentration and leakage bridge."""
    # 1. Constructive half-period concentration control: t=3 (q=8), tilde_A cols = [[4], [0], [4]], s=[1]
    # theta = [pi, 0, pi] -> concentrates with probability 1.0 on z = (1, 0, 1)
    half_period_constructive_control = verify_hadamard_product_law_and_tv_identity(
        tilde_a_cols=[[4], [0], [4]],
        s_vec=[1],
        t_bits=3,
    )

    # 2. Non-half-period carry-leakage regime: t=3 (q=8), tilde_A cols = [[2], [1], [3]], s=[1]
    # theta = [pi/2, pi/4, 3*pi/4] -> spreads across all 2^3 = 8 outcomes
    carry_leakage_audit = verify_hadamard_product_law_and_tv_identity(
        tilde_a_cols=[[2], [1], [3]],
        s_vec=[1],
        t_bits=3,
    )

    all_passed = (
        half_period_constructive_control["exact_product_and_tv_verified"]
        and abs(half_period_constructive_control["max_single_outcome_probability"] - 1.0) < 1e-12
        and abs(half_period_constructive_control["tv_distance_from_zero_shift_closed_form"] - 1.0) < 1e-12
        and carry_leakage_audit["exact_product_and_tv_verified"]
        and carry_leakage_audit["max_single_outcome_probability"] < 0.45
    )

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "scope_constraints": {
            "applies_to": "H^{tensor m} computational-basis readout on m-wire compressed DCP phase states",
            "does_not_claim": "Anti-concentration when all wire phases lie in the half-period subgroup {0, pi}",
            "controls_included": "Includes both the half-period constructive concentration control (max outcome prob = 1.0 on z=(1,0,1)) and the non-half-period carry-leakage audit.",
        },
        "half_period_constructive_control": half_period_constructive_control,
        "carry_leakage_audit": carry_leakage_audit,
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
