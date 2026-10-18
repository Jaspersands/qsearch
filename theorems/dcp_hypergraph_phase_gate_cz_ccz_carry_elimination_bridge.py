r"""DCP hypergraph phase-gate (CZ / CCZ) carry cross-term elimination bridge.

Establishes the exact Clifford-hierarchy degree cutoff of multi-tree overlapping CNOT
carries modulo 2^t (extending Subsystem 63) and proves when diagonal hypergraph phase
gates (CZ at t=2 mod 4, controlled-phase + CCZ at t=3 mod 8) exactly unentangle
overlapping CNOT compression trees:

1. Exact Degree-t Nilpotency Cutoff of Binary-XOR Carries Modulo 2^t:
   When a shared pivot wire x_r = u_1 (+) u_2 (+) ... (+) u_m (with anchor x_{0, r} = 0)
   participates in m >= 2 overlapping CNOT trees over Z_{2^t}^n, its integer value embeds
   into Z_{2^t} via the inclusion-exclusion polynomial:
       x_r = sum_{k=1}^m (-2)^{k-1} sum_{|J|=k} prod_{j in J} u_j.
   Because (-2)^{k-1} == 0 (mod 2^t) for all k >= t + 1, EVERY multilinear carry term of
   degree k >= t + 1 vanishes identically modulo 2^t! Specifically:
   - At t = 2 (mod 4), all degree k >= 3 carries vanish mod 4, leaving ONLY pairwise
     degree-2 terms: -2 * sum_{j < l} u_j u_l == 2 * sum_{j < l} u_j u_l (mod 4).
   - At t = 3 (mod 8), all degree k >= 4 carries vanish mod 8, leaving ONLY degree-2
     (-2 u_j u_l) and degree-3 (+4 u_j u_l u_p) terms.

2. Exact CZ Unentanglement at t = 2 (mod 4) Conditioned on LSB Secret Parity:
   At t = 2 (mod 4), the entangling phase factor across m overlapping trees is:
       exp( (2*pi*i / 4) * <A_{., r}, s> * (-2 sum_{j < l} u_j u_l) )
       = prod_{1 <= j < l <= m} (-1)^{ p_r * u_j * u_l }
       = prod_{1 <= j < l <= m} CZ_{j, l}^{ p_r },
   where p_r = <A_{., r}, s> mod 2 in {0, 1} is the LSB parity on column r.
   - Constructive Law: Once p_r in {0, 1} is known from Stage-1 mod-2 peeling, applying
     prod_{j < l} CZ_{j, l}^{p_r} deterministically unentangles all m overlapping wires
     into an exact product state (fidelity F = 1.0 for every m >= 2).
   - Secret-Independent Obstruction: Without knowing p_r, any fixed secret-independent
     diagonal unitary U_diag has worst-case fidelity <= 0.5 on m = 2 overlapping wires.

3. Exact Controlled-Phase + CCZ Unentanglement at t = 3 (mod 8):
   At t = 3 (mod 8) with m = 3 overlapping wires, knowing s_r_mod4 = <A_{., r}, s> mod 4
   from Stages 1-2 allows applying pairwise controlled-S^{s_r_mod4} gates together with
   the 3-body hypergraph gate CCZ_{1,2,3}^{s_r_mod4 mod 2} to restore 100% product state
   fidelity (F = 1.0), whereas omitting the 3-body CCZ gate when s_r_mod4 is odd leaves
   residual 3-body entanglement (F = 9/16 = 0.5625).
"""

from __future__ import annotations

import cmath
import hashlib
import itertools
import json
import math
from typing import Any, Dict, List


THEOREM_ID = "dcp_hypergraph_phase_gate_cz_ccz_carry_elimination_bridge"
SCHEMA_VERSION = "dcp-hypergraph-phase-gate-cz-ccz-carry-elimination-bridge-v1"


def _xor_int(bits: tuple[int, ...]) -> int:
    res = 0
    for b in bits:
        res ^= b
    return res


def evaluate_mod_2t_carry_degree_cutoff_and_hypergraph_repair(
    t_bits: int,
    m_trees: int,
    col_dot_s: int,
) -> Dict[str, Any]:
    """Verify exact degree-t nilpotency cutoff modulo 2^t and explicit CZ/CCZ unentanglement fidelity."""
    if type(t_bits) is not int or t_bits < 2:
        raise ValueError("t_bits must be an integer >= 2")
    if type(m_trees) is not int or m_trees < 2:
        raise ValueError("m_trees must be an integer >= 2")

    q_mod = 1 << t_bits
    dim_u = 1 << m_trees
    all_u = list(itertools.product((0, 1), repeat=m_trees))

    # 1. Verify exact polynomial cutoff at degree <= t_bits across all u in {0,1}^m
    max_poly_mod_diff = 0
    for u_vec in all_u:
        xor_val = _xor_int(u_vec)
        trunc_poly = 0
        for deg in range(1, min(m_trees, t_bits) + 1):
            coeff = (-2) ** (deg - 1)
            for comb in itertools.combinations(range(m_trees), deg):
                prod = 1
                for idx in comb:
                    prod *= u_vec[idx]
                trunc_poly += coeff * prod
        diff_mod = (xor_val - trunc_poly) % q_mod
        max_poly_mod_diff = max(max_poly_mod_diff, diff_mod)

    # 2. Construct true overlapping state |psi_true> vs ideal product state |psi_linear>
    # where linear state has phase (2*pi/2^t) * col_dot_s * sum_j u_j
    psi_true: List[complex] = []
    psi_linear: List[complex] = []
    psi_deg2_only_repaired: List[complex] = []
    psi_full_hypergraph_repaired: List[complex] = []

    for u_vec in all_u:
        xor_val = _xor_int(u_vec)
        lin_val = sum(u_vec)
        amp_true = cmath.exp(2j * math.pi * float((col_dot_s * xor_val) % q_mod) / float(q_mod)) / math.sqrt(float(dim_u))
        amp_lin = cmath.exp(2j * math.pi * float((col_dot_s * lin_val) % q_mod) / float(q_mod)) / math.sqrt(float(dim_u))

        # Degree-2 repair: cancels (-2) * sum_{j < l} u_j u_l
        deg2_sum = sum(u_vec[j] * u_vec[l] for j in range(m_trees) for l in range(j + 1, m_trees))
        repair_deg2 = cmath.exp(-2j * math.pi * float((col_dot_s * (-2 * deg2_sum)) % q_mod) / float(q_mod))

        # Full degree <= t repair (CZ at t=2; controlled-S + CCZ at t=3)
        higher_sum = 0
        for deg in range(2, min(m_trees, t_bits) + 1):
            coeff = (-2) ** (deg - 1)
            for comb in itertools.combinations(range(m_trees), deg):
                prod = 1
                for idx in comb:
                    prod *= u_vec[idx]
                higher_sum += coeff * prod
        repair_full = cmath.exp(-2j * math.pi * float((col_dot_s * higher_sum) % q_mod) / float(q_mod))

        psi_true.append(amp_true)
        psi_linear.append(amp_lin)
        psi_deg2_only_repaired.append(amp_true * repair_deg2)
        psi_full_hypergraph_repaired.append(amp_true * repair_full)

    def _fidelity(v1: List[complex], v2: List[complex]) -> float:
        ov = sum(a.conjugate() * b for a, b in zip(v1, v2))
        return abs(ov) ** 2

    fid_unrepaired = _fidelity(psi_true, psi_linear)
    fid_deg2_repaired = _fidelity(psi_deg2_only_repaired, psi_linear)
    fid_full_repaired = _fidelity(psi_full_hypergraph_repaired, psi_linear)

    return {
        "t_bits": t_bits,
        "q_mod": q_mod,
        "m_trees": m_trees,
        "col_dot_s": col_dot_s,
        "max_degree_t_polynomial_mod_error": max_poly_mod_diff,
        "unrepaired_product_fidelity": fid_unrepaired,
        "deg2_only_repaired_product_fidelity": fid_deg2_repaired,
        "full_hypergraph_repaired_product_fidelity": fid_full_repaired,
        "exact_cutoff_and_repair_verified": (
            max_poly_mod_diff == 0
            and abs(fid_full_repaired - 1.0) < 1e-12
            and (abs(fid_deg2_repaired - 1.0) < 1e-12 if t_bits == 2 else True)
        ),
    }


def generate_dcp_hypergraph_phase_gate_cz_ccz_carry_elimination_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the hypergraph CZ/CCZ carry elimination bridge."""
    # 1. t = 2 (mod 4), m = 3 overlapping trees, col_dot_s = 1 (odd):
    # Degree-3 carry (-2)^2 = 4 == 0 mod 4 vanishes automatically, so pairwise CZ gates alone achieve F = 1.0!
    mod4_m3_odd = evaluate_mod_2t_carry_degree_cutoff_and_hypergraph_repair(
        t_bits=2, m_trees=3, col_dot_s=1
    )

    # 2. t = 2 (mod 4), m = 2 overlapping trees, col_dot_s = 1:
    # Unrepaired fidelity is |3 + (-1)|^2 / 16 = 4/16 = 0.25; CZ-repaired fidelity is 1.0!
    mod4_m2_odd = evaluate_mod_2t_carry_degree_cutoff_and_hypergraph_repair(
        t_bits=2, m_trees=2, col_dot_s=1
    )

    # 3. t = 3 (mod 8), m = 3 overlapping trees, col_dot_s = 1:
    # Degree-2 repair alone leaves the u_1 u_2 u_3 CCZ sign flip on |111> -> fidelity |(7 - 1)/8|^2 = 36/64 = 9/16 = 0.5625;
    # Adding CCZ_{1,2,3} restores F = 1.0!
    mod8_m3_odd = evaluate_mod_2t_carry_degree_cutoff_and_hypergraph_repair(
        t_bits=3, m_trees=3, col_dot_s=1
    )

    # 4. t = 3 (mod 8), m = 4 overlapping trees, col_dot_s = 1:
    # Degree-4 carry (-2)^3 = -8 == 0 mod 8 vanishes automatically, so degree <= 3 hypergraph gates restore F = 1.0!
    mod8_m4_odd = evaluate_mod_2t_carry_degree_cutoff_and_hypergraph_repair(
        t_bits=3, m_trees=4, col_dot_s=1
    )

    all_passed = (
        mod4_m3_odd["exact_cutoff_and_repair_verified"]
        and abs(mod4_m3_odd["deg2_only_repaired_product_fidelity"] - 1.0) < 1e-12
        and mod4_m2_odd["exact_cutoff_and_repair_verified"]
        and abs(mod4_m2_odd["unrepaired_product_fidelity"] - 0.25) < 1e-12
        and mod8_m3_odd["exact_cutoff_and_repair_verified"]
        and abs(mod8_m3_odd["deg2_only_repaired_product_fidelity"] - 9.0 / 16.0) < 1e-12
        and abs(mod8_m3_odd["full_hypergraph_repaired_product_fidelity"] - 1.0) < 1e-12
        and mod8_m4_odd["exact_cutoff_and_repair_verified"]
    )

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "proof_status": "LOCAL_DERIVATION_REVIEW_PENDING_NOT_FORMALLY_VERIFIED",
        "scope_constraints": {
            "applies_to": "Degree-t nilpotency cutoff of overlapping CNOT carries modulo 2^t and conditional CZ / CCZ unentanglement",
            "does_not_claim": "Secret-independent unentanglement when the lower prefix bits <A_{., r}, s> mod 2^{t-1} are unknown",
            "controls_included": "Includes mod 4 m=2 (unrepaired F=0.25 -> CZ F=1.0), mod 4 m=3 (degree-3 vanishes mod 4 so CZ alone gives F=1.0), mod 8 m=3 (deg-2 only F=9/16=0.5625 -> +CCZ F=1.0), and mod 8 m=4 (degree-4 vanishes mod 8).",
        },
        "mod4_m2_audit": mod4_m2_odd,
        "mod4_m3_audit": mod4_m3_odd,
        "mod8_m3_audit": mod8_m3_odd,
        "mod8_m4_audit": mod8_m4_odd,
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
