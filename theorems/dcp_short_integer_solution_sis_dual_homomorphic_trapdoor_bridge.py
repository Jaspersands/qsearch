r"""DCP Short Integer Solution (SIS) dual gadget trapdoor binary witness compilation bridge.

Establishes the exact constructive duality between Micciancio-Peikert / GPV gadget
trapdoors for the Short Integer Solution (SIS) lattice Lambda_q^perp(A) and zero-carry
binary CNOT witness compilation for DCP secret recovery over Z_{2^t}^n:

1. Exact Binary Gadget Trapdoor Identity (A * T == 0 mod 2^t):
   Let G = I_n \otimes [1, 2, 4, ..., 2^{t-1}] in Z_{2^t}^{n x (n*t)} be the canonical
   dyadic power-of-2 gadget matrix, and let A = [G | B] in Z_{2^t}^{n x (n*t + m)} where
   B = (-G * R) mod 2^t for a short binary trapdoor matrix R in {0, 1}^{(n*t) x m}.
   Then the (n*t + m) x m binary matrix:
       T = [[R], [I_m]] in {0, 1}^{(n*t + m) x m}
   satisfies the EXACT modular zero-sum identity:
       A * T = G * R + B * I_m = G * R - G * R == 0 (mod 2^t)!
   Because every entry of T belongs to {0, 1} (not merely {-1, 0, +1}), every column
   t_j of T is a pure binary zero-sum witness (A t_j == 0 mod 2^t) realized on the
   all-zero CNOT syndrome branch d = 0^{wt(t_j)-1}!

2. Exact Dyadic Scale Extraction via Punctured Trapdoor Columns:
   For any target row i in {0, ..., n - 1} and bit scale r in {0, ..., t - 1}
   (corresponding to gadget column g_{i, r} = 2^r * e_i at index idx = i*t + r),
   Suppose column j of R has R_{idx, j} = 1. Flipping ONLY the single bit at row idx of
   t_j defines the punctured binary vector:
       v_{j, idx} = t_j - e_{idx} in {0, 1}^{n*t + m},
   which satisfies the exact dyadic scale isolation identity:
       A * v_{j, idx} = A * t_j - A_{., idx} == -2^r * e_i (mod 2^t)!
   Applying a single Pauli-X sign-flip gate (Subsystem 78) on the survivor wire then
   prepares the exact canonical dyadic scale +2^r * e_i (mod 2^t) with zero cross-coordinate
   contamination!
"""

from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, List, Sequence


THEOREM_ID = "dcp_short_integer_solution_sis_dual_homomorphic_trapdoor_bridge"
SCHEMA_VERSION = "dcp-short-integer-solution-sis-dual-homomorphic-trapdoor-bridge-v1"


def build_gadget_matrix(n_dim: int, t_bits: int) -> List[List[int]]:
    """Construct G = I_n otimes [1, 2, ..., 2^{t-1}] in Z_{2^t}^{n x (n*t)}."""
    cols = n_dim * t_bits
    g_mat = [[0] * cols for _ in range(n_dim)]
    for i in range(n_dim):
        for r in range(t_bits):
            g_mat[i][i * t_bits + r] = 1 << r
    return g_mat


def evaluate_sis_gadget_trapdoor_witness_compilation(
    n_dim: int,
    t_bits: int,
    r_trapdoor: Sequence[Sequence[int]],
) -> Dict[str, Any]:
    """Verify A * T == 0 mod 2^t and punctured dyadic scale isolation A * (t_j - e_{idx}) == -2^r e_i mod 2^t."""
    q_mod = 1 << t_bits
    nt = n_dim * t_bits
    m_cols = len(r_trapdoor[0])
    if len(r_trapdoor) != nt:
        raise ValueError("r_trapdoor must have n_dim * t_bits rows")

    g_mat = build_gadget_matrix(n_dim, t_bits)
    # B = -G * R mod 2^t
    b_mat = [
        [
            (-sum(g_mat[i][k] * int(r_trapdoor[k][j]) for k in range(nt))) % q_mod
            for j in range(m_cols)
        ]
        for i in range(n_dim)
    ]

    # Full public header A = [G | B] in Z_{2^t}^{n x (nt + m)}
    k_total = nt + m_cols
    a_mat = [g_mat[i] + b_mat[i] for i in range(n_dim)]

    # Trapdoor witness matrix T = [[R], [I_m]] in {0, 1}^{(nt + m) x m}
    t_mat: List[List[int]] = []
    for k in range(nt):
        t_mat.append([int(r_trapdoor[k][j]) & 1 for j in range(m_cols)])
    for j in range(m_cols):
        t_mat.append([1 if j == c else 0 for c in range(m_cols)])

    # 1. Verify A * T == 0 (mod 2^t) across all n rows and m columns:
    at_prod = [
        [
            sum(a_mat[i][row] * t_mat[row][j] for row in range(k_total)) % q_mod
            for j in range(m_cols)
        ]
        for i in range(n_dim)
    ]
    zero_sum_verified = all(at_prod[i][j] == 0 for i in range(n_dim) for j in range(m_cols))

    # 2. Verify punctured dyadic scale extraction: for every column j and every active row idx in R (R[idx][j] == 1),
    # v = t_j - e_{idx} in {0, 1}^K satisfies A * v == -2^r e_i (mod 2^t)!
    punctured_records: List[Dict[str, Any]] = []
    all_punctured_exact = True

    for j in range(m_cols):
        for idx in range(nt):
            if t_mat[idx][j] == 1:
                coord_i = idx // t_bits
                scale_r = idx % t_bits
                v_punc = [t_mat[row][j] - (1 if row == idx else 0) for row in range(k_total)]
                av_punc = [
                    sum(a_mat[i][row] * v_punc[row] for row in range(k_total)) % q_mod
                    for i in range(n_dim)
                ]
                expected_neg_scale = [
                    ((- (1 << scale_r)) % q_mod) if i == coord_i else 0
                    for i in range(n_dim)
                ]
                pauli_x_rectified_scale = [(-val) % q_mod for val in av_punc]
                expected_pos_scale = [
                    (1 << scale_r) if i == coord_i else 0
                    for i in range(n_dim)
                ]
                if av_punc != expected_neg_scale or pauli_x_rectified_scale != expected_pos_scale:
                    all_punctured_exact = False
                punctured_records.append({
                    "trapdoor_col_j": j,
                    "gadget_row_idx": idx,
                    "target_coord_i": coord_i,
                    "dyadic_scale_r": scale_r,
                    "punctured_weight": sum(v_punc),
                    "raw_column_sum_mod_q": av_punc,
                    "pauli_x_rectified_column_sum_mod_q": pauli_x_rectified_scale,
                })

    return {
        "n_dim": n_dim,
        "t_bits": t_bits,
        "q_mod": q_mod,
        "K_total_wires": k_total,
        "m_trapdoor_cols": m_cols,
        "zero_sum_at_eq_0_mod_2t_verified": zero_sum_verified,
        "all_punctured_dyadic_scales_verified": all_punctured_exact,
        "num_punctured_scales_extracted": len(punctured_records),
        "punctured_records": punctured_records,
        "all_verified": zero_sum_verified and all_punctured_exact and len(punctured_records) == nt,
    }


def generate_dcp_short_integer_solution_sis_dual_homomorphic_trapdoor_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the SIS dual gadget trapdoor witness compilation bridge."""
    # n = 2, t = 3 (q = 8, nt = 6), m = 2 trapdoor columns covering all 6 gadget coordinates:
    r_trap_2x3 = [
        [1, 0],  # coord 0, scale 1
        [1, 0],  # coord 0, scale 2
        [1, 0],  # coord 0, scale 4
        [0, 1],  # coord 1, scale 1
        [0, 1],  # coord 1, scale 2
        [0, 1],  # coord 1, scale 4
    ]
    audit_n2_t3 = evaluate_sis_gadget_trapdoor_witness_compilation(
        n_dim=2, t_bits=3, r_trapdoor=r_trap_2x3
    )

    all_passed = audit_n2_t3["all_verified"]

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "proof_status": "LOCAL_DERIVATION_REVIEW_PENDING_NOT_FORMALLY_VERIFIED",
        "scope_constraints": {
            "applies_to": "Micciancio-Peikert / GPV gadget trapdoor A = [G | -G R mod 2^t] binary zero-sum witness compilation and punctured dyadic scale extraction",
            "does_not_claim": "Efficient recovery of the secret trapdoor R from a random public matrix A without trapdoor knowledge",
            "controls_included": "Evaluates 2D Z_8^2 (n=2, t=3, K=8) gadget trapdoor, verifying A * T == 0 mod 8 and exact extraction of all 6 dyadic scale vectors +/- 2^r e_i via 1-bit puncturing + Pauli-X rectification.",
        },
        "gadget_trapdoor_n2_t3_audit": audit_n2_t3,
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
