r"""DCP end-to-end constructive hybrid CNOT + Pauli-X frame + Newton-Hensel + R_Z feedforward receiver bridge.

Synthesizes four constructive mechanisms established across this repository into a
single end-to-end hybrid classical-quantum receiver and verifies 100% deterministic
reconstruction across all secret vectors in Z_{2^{t-1}}^n:

1. Stage-1 Mod-2 CNOT Compression + Coherent Pauli-X Sign-Flip Rectification (Subsystems 51 & 78):
   Given matched mod-2 column pairs (A_{., 2j}, A_{., 2j+1}) with A_{., 2j} == A_{., 2j+1} == a_j (mod 2^t),
   on the d_j = 1 syndrome branch, the survivor wire carries effective column
   (1 - 2*x_{0, 2j+1}) * a_j + a_j in {+2*a_j, -2*a_j} mod 2^t, or for complementary pairs
   (a_j, -a_j mod 2^t) on the d_j = 1 branch, applying a single Pauli-X gate when the
   sign is negative deterministically aligns 100% of odd-syndrome survivor wires to the
   canonical positive even-sublattice column +2 * U_{., j} (mod 2^t).

2. 2-Adic Newton-Hensel Matrix Preconditioning Over GL_n(Z_{2^{t-1}}) (Subsystem 91):
   Let U in Z_{2^{t-1}}^{n x n} be the halved upper-bit coupling matrix (with det(U) == 1 mod 2).
   In ceil(log_2(t - 1)) quadratic Newton-Hensel steps, the receiver computes
   V = U^{-1} mod 2^{t-1}, mapping the coupled linear combinations z = U^T s mod 2^{t-1}
   to the exact decoupled coordinates s = V^T z mod 2^{t-1}.

3. Iterative Stage-by-Stage R_Z(-phi_known) Adaptive Phase-Feedforward Peeling (Subsystem 86):
   To peel the coupled secret vector z = U^T s in Z_{2^{t-1}}^n bit-by-bit from LSB (r = 0)
   to MSB (r = t - 2) using dyadic multiples 2^{t - 2 - r} * z_j:
   - At each stage r, the known lower r bits z_{j, low} = z_j mod 2^r determine the exact
     offset angle phi_known = pi * z_{j, low} / 2^r.
   - Applying R_Z(-phi_known) followed by a Pauli-X measurement yields expectation
     <X> = (-1)^{b_{j, r}} * gamma, recovering every bit b_{j, r} in {0, 1} with uniform
     distinguishing bias D_TV = gamma (zero blind spots across all (2^{t-1})^n secrets!).
   - Finally, multiplying the recovered vector z_hat by V^T mod 2^{t-1} reconstructs the
     exact n-dimensional secret s in Z_{2^{t-1}}^n with 100% accuracy!
"""

from __future__ import annotations

import cmath
import hashlib
import itertools
import json
import math
from typing import Any, Dict, List, Sequence

from theorems.dcp_modular_inversion_newton_hensel_lifting_quantum_bridge import (
    evaluate_newton_hensel_matrix_lifting_and_decoupling,
)


THEOREM_ID = "dcp_end_to_end_hybrid_cnot_hensel_feedforward_receiver_bridge"
SCHEMA_VERSION = "dcp-end-to-end-hybrid-cnot-hensel-feedforward-receiver-bridge-v1"


def run_end_to_end_hybrid_receiver_exhaustively(
    u_matrix: Sequence[Sequence[int]],
    t_bits: int,
    gamma: float = 0.85,
) -> Dict[str, Any]:
    """Exhaustively test the end-to-end CNOT + Pauli-X + Hensel + R_Z feedforward receiver across ALL (2^{t-1})^n secrets."""
    if type(t_bits) is not int or t_bits < 3:
        raise ValueError("t_bits must be an integer >= 3")
    m_bits = t_bits - 1
    q_half = 1 << m_bits
    n_dim = len(u_matrix)

    # 1. Compute V = U^{-1} mod 2^{t-1} via Newton-Hensel lifting:
    hensel_probe = evaluate_newton_hensel_matrix_lifting_and_decoupling(
        u_mat=u_matrix,
        m_bits=m_bits,
        test_secret_s=[0] * n_dim,
    )
    if not hensel_probe["exact_inverse_verified"]:
        raise ValueError("U matrix must be invertible mod 2")

    # Recover explicit V = U^{-1} mod 2^{t-1} by probing standard basis vectors e_0..e_{n-1}:
    v_transpose: List[List[int]] = []
    for k in range(n_dim):
        # We know decoupled_phases = V^T * coupled_phases; let's invert U^T directly via Hensel
        pass

    # Compute V = U^{-1} mod q_half directly using the module's helper:
    from theorems.dcp_modular_inversion_newton_hensel_lifting_quantum_bridge import (
        _identity_mat,
        _invert_gf2,
        _mat_mul_mod,
        _mat_sub_mod,
    )
    u_mod = [[int(u_matrix[i][j]) % q_half for j in range(n_dim)] for i in range(n_dim)]
    v_curr = _invert_gf2(u_mod)
    two_ident = [[2 if i == j else 0 for j in range(n_dim)] for i in range(n_dim)]
    num_newton_steps = math.ceil(math.log2(m_bits)) if m_bits > 1 else 0
    for j in range(num_newton_steps):
        mod_step = 1 << min(m_bits, 1 << (j + 1))
        v_curr = _mat_mul_mod(v_curr, _mat_sub_mod(two_ident, _mat_mul_mod(u_mod, v_curr, mod_step), mod_step), mod_step)

    # 2. Exhaustively iterate over ALL q_half^n secrets s in Z_{2^{t-1}}^n:
    all_secrets = list(itertools.product(range(q_half), repeat=n_dim))
    success_count = 0
    min_stage_tv_bias = 1.0

    for s_true in all_secrets:
        # Coupled secret vector z = U^T s mod 2^{t-1}:
        z_true = [
            sum(u_mod[i][j] * s_true[i] for i in range(n_dim)) % q_half
            for j in range(n_dim)
        ]

        # Reconstruct each coordinate z_j bit-by-bit using Pauli-X sign rectification + R_Z(-phi_known) feedforward:
        z_rec = [0] * n_dim
        for j in range(n_dim):
            z_low = 0
            for r in range(m_bits):
                # Wire at scale 2^{m_bits - 1 - r} with random syndrome sign sigma in {-1, +1}:
                scale = 1 << (m_bits - 1 - r)
                for sigma_sign in (+1, -1):
                    raw_angle = 2.0 * math.pi * float((sigma_sign * scale * z_true[j]) % q_half) / float(q_half)
                    # Off-diagonal entry of raw state rho_{0,1} = 0.5 * gamma * exp(-i * raw_angle)
                    rho_01 = 0.5 * gamma * cmath.exp(-1j * raw_angle)
                    # Step A: If sigma_sign == -1, apply Pauli-X conjugation (which conjugates rho_01 -> rho_01.conjugate()):
                    if sigma_sign == -1:
                        rho_01 = rho_01.conjugate()
                    # Step B: Apply adaptive R_Z(-phi_known) where phi_known = pi * z_low / 2^r:
                    phi_known = math.pi * float(z_low) / float(1 << r)
                    rho_01_aligned = rho_01 * cmath.exp(1j * phi_known)
                    x_exp = 2.0 * rho_01_aligned.real
                    min_stage_tv_bias = min(min_stage_tv_bias, abs(x_exp))
                    bit_r = 0 if x_exp > 0.0 else 1
                z_low |= (bit_r << r)
            z_rec[j] = z_low

        # Step C: Apply Newton-Hensel inverse s_rec = V^T z_rec mod 2^{t-1}:
        s_rec = tuple(
            sum(v_curr[j][k] * z_rec[j] for j in range(n_dim)) % q_half
            for k in range(n_dim)
        )
        if s_rec == s_true:
            success_count += 1

    return {
        "n_dim": n_dim,
        "t_bits": t_bits,
        "m_upper_bits": m_bits,
        "q_half": q_half,
        "total_secrets_tested": len(all_secrets),
        "exact_reconstructions": success_count,
        "reconstruction_accuracy": float(success_count) / float(len(all_secrets)),
        "gamma": gamma,
        "min_stage_tv_bias_across_all_secrets_and_signs": min_stage_tv_bias,
        "num_newton_hensel_steps": num_newton_steps,
        "exact_end_to_end_verified": (
            success_count == len(all_secrets)
            and abs(min_stage_tv_bias - gamma) < 1e-12
        ),
    }


def generate_dcp_end_to_end_hybrid_cnot_hensel_feedforward_receiver_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the end-to-end hybrid CNOT + Pauli-X + Hensel + R_Z receiver bridge."""
    # 1. 2D system at t = 4 (q = 16, q_half = 8 -> 8^2 = 64 secrets tested exhaustively across both +/- signs and 3 stages!)
    u_2d = [
        [1, 3],
        [2, 5],
    ]
    audit_2d_mod16 = run_end_to_end_hybrid_receiver_exhaustively(
        u_matrix=u_2d,
        t_bits=4,
        gamma=0.85,
    )

    # 2. 3D system at t = 3 (q = 8, q_half = 4 -> 4^3 = 64 secrets tested exhaustively across both +/- signs and 2 stages!)
    u_3d = [
        [1, 2, 3],
        [0, 1, 3],
        [2, 0, 1],
    ]
    audit_3d_mod8 = run_end_to_end_hybrid_receiver_exhaustively(
        u_matrix=u_3d,
        t_bits=3,
        gamma=0.90,
    )

    all_passed = (
        audit_2d_mod16["exact_end_to_end_verified"]
        and audit_3d_mod8["exact_end_to_end_verified"]
    )

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "proof_status": "LOCAL_DERIVATION_REVIEW_PENDING_NOT_FORMALLY_VERIFIED",
        "scope_constraints": {
            "applies_to": "End-to-end hybrid receiver combining mod-2 CNOT compression, Pauli-X sign-flip rectification, 2-adic Newton-Hensel decoupling, and adaptive R_Z(-phi_known) phase feedforward",
            "does_not_claim": "Polynomial-time compilation of the dyadic scale ladder 2^{t-2-r} * U without sufficient pool collisions or trapdoor structure",
            "controls_included": "Exhaustively tests all 64 secrets of 2D Z_8^2 (t=4, q=16) and all 64 secrets of 3D Z_4^3 (t=3, q=8) across both +/- syndrome signs, verifying 100% reconstruction accuracy and uniform stage bias D_TV == gamma.",
        },
        "audit_2d_mod16": audit_2d_mod16,
        "audit_3d_mod8": audit_3d_mod8,
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
