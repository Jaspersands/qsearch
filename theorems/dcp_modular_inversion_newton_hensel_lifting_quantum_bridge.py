r"""DCP 2-adic Newton-Hensel quadratic matrix inversion and zero-ancilla phase decoupling bridge.

Establishes the exact quadratic convergence of 2-adic Newton-Hensel matrix lifting over
Z_{2^m}^{n x n} and proves that preconditioning n linearly independent compressed DCP
wires by the lifted modular inverse V_L = U^{-1} mod 2^m decouples an arbitrary
invertible coupling matrix U in GL_n(Z_{2^m}) into n orthogonal 1D scalar phase registers:

1. Exact Quadratic Convergence of 2-Adic Matrix Hensel Lifting:
   Let U in Z_{2^m}^{n x n} have odd determinant det(U) == 1 (mod 2), and let V_0 in {0, 1}^{n x n}
   be its unique inverse over GF(2) satisfying U V_0 == I (mod 2).
   Defining the Newton-Hensel sequence for j = 0, 1, ..., L - 1 (where 2^L >= m):
       V_{j+1} = V_j * (2 * I - U * V_j) mod 2^{min(m, 2^{j+1})},
   the residual matrix R_j = I - U * V_j satisfies the exact squaring identity:
       R_{j+1} == I - U * V_j * (I + R_j) == I - (I - R_j)*(I + R_j) == R_j^2 (mod 2^m).
   Since R_0 == 0 (mod 2), by induction R_j == 0 (mod 2^{2^j}), so V_L = U^{-1} mod 2^m is
   reached in strictly L = ceil(log_2(m)) quadratic Newton steps!

2. Zero-Ancilla Phase Decoupling of Coupled n-Dimensional DCP Wires:
   Suppose n compressed survivor wires after k-stage mod-2 elimination carry effective
   columns A_tilde = 2^k * U mod 2^t (so each wire j in {0, ..., n-1} has phase
   theta_j(s) = (2*pi / 2^m) * <(U^T s)_j, 1>, where m = t - k).
   Applying the invertible mod-2^m linear transformation V_L^T (either classically to the
   reconstructed phases or via reversible modular CNOT/adder basis change on the binary
   index register) transforms the coupled phase vector U^T s mod 2^m into:
       V_L^T (U^T s) == (U V_L)^T s == I_n s == s (mod 2^m),
   producing n completely independent 1D phase registers exp(2*pi*i * s_r / 2^m) with
   100% tensor-product fidelity (F = 1.0) against the ideal uncoupled secret state!
"""

from __future__ import annotations

import cmath
import hashlib
import itertools
import json
import math
from typing import Any, Dict, List, Sequence


THEOREM_ID = "dcp_modular_inversion_newton_hensel_lifting_quantum_bridge"
SCHEMA_VERSION = "dcp-modular-inversion-newton-hensel-lifting-quantum-bridge-v1"

IntMatrix = List[List[int]]


def _mat_mul_mod(a: IntMatrix, b: IntMatrix, mod: int) -> IntMatrix:
    n = len(a)
    return [
        [sum(a[i][k] * b[k][j] for k in range(n)) % mod for j in range(n)]
        for i in range(n)
    ]


def _mat_sub_mod(a: IntMatrix, b: IntMatrix, mod: int) -> IntMatrix:
    n = len(a)
    return [[(a[i][j] - b[i][j]) % mod for j in range(n)] for i in range(n)]


def _identity_mat(n: int) -> IntMatrix:
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


def _invert_gf2(u_mat: Sequence[Sequence[int]]) -> IntMatrix:
    n = len(u_mat)
    aug = [
        [int(u_mat[i][j]) % 2 for j in range(n)] + [1 if i == j else 0 for j in range(n)]
        for i in range(n)
    ]
    for col in range(n):
        pivot = None
        for r in range(col, n):
            if aug[r][col] == 1:
                pivot = r
                break
        if pivot is None:
            raise ValueError("Matrix is singular over GF(2)")
        aug[col], aug[pivot] = aug[pivot], aug[col]
        for r in range(n):
            if r != col and aug[r][col] == 1:
                for c in range(2 * n):
                    aug[r][c] ^= aug[col][c]
    return [row[n:] for row in aug]


def evaluate_newton_hensel_matrix_lifting_and_decoupling(
    u_mat: Sequence[Sequence[int]],
    m_bits: int,
    test_secret_s: Sequence[int],
) -> Dict[str, Any]:
    """Run quadratic 2-adic Newton-Hensel lifting to invert U mod 2^m and verify phase decoupling."""
    if type(m_bits) is not int or m_bits < 1:
        raise ValueError("m_bits must be an integer >= 1")
    n = len(u_mat)
    q_mod = 1 << m_bits
    u_mod = [[int(u_mat[i][j]) % q_mod for j in range(n)] for i in range(n)]

    v_curr = _invert_gf2(u_mod)
    ident = _identity_mat(n)
    two_ident = [[2 if i == j else 0 for j in range(n)] for i in range(n)]

    steps_history: List[Dict[str, Any]] = []
    # Check initial j = 0 (mod 2^1)
    prod0 = _mat_mul_mod(u_mod, v_curr, 2)
    steps_history.append({
        "step_j": 0,
        "guaranteed_precision_bits": 1,
        "verified_identity_mod_2_pow_2j": prod0 == ident,
    })

    num_steps = math.ceil(math.log2(m_bits)) if m_bits > 1 else 0
    for j in range(num_steps):
        prec_bits = min(m_bits, 1 << (j + 1))
        mod_step = 1 << prec_bits
        uv = _mat_mul_mod(u_mod, v_curr, mod_step)
        factor = _mat_sub_mod(two_ident, uv, mod_step)
        v_curr = _mat_mul_mod(v_curr, factor, mod_step)
        check_prod = _mat_mul_mod(u_mod, v_curr, mod_step)
        steps_history.append({
            "step_j": j + 1,
            "guaranteed_precision_bits": prec_bits,
            "verified_identity_mod_2_pow_2j": check_prod == ident,
        })

    # Verify final inverse modulo 2^m:
    uv_final = _mat_mul_mod(u_mod, v_curr, q_mod)
    vu_final = _mat_mul_mod(v_curr, u_mod, q_mod)
    exact_inverse_verified = (uv_final == ident) and (vu_final == ident)

    # Verify quantum phase decoupling on n qubits:
    # Coupled wire j has effective phase angle (2*pi / 2^m) * (U^T s)_j.
    # Preconditioning by V_L^T maps the effective column matrix U -> U * V_L == I_n (mod 2^m).
    coupled_phases = [
        sum(u_mod[i][j] * int(test_secret_s[i]) for i in range(n)) % q_mod
        for j in range(n)
    ]
    decoupled_phases = [
        sum(v_curr[j][k] * coupled_phases[j] for j in range(n)) % q_mod
        for k in range(n)
    ]
    expected_secret_mod = [int(test_secret_s[k]) % q_mod for k in range(n)]

    # Explicit n-qubit state fidelity between preconditioned state and ideal product state:
    all_b = list(itertools.product((0, 1), repeat=n))
    dim_b = 1 << n
    overlap = 0j
    for b_vec in all_b:
        ph_pre = sum(b_vec[k] * decoupled_phases[k] for k in range(n)) % q_mod
        ph_ideal = sum(b_vec[k] * expected_secret_mod[k] for k in range(n)) % q_mod
        amp_pre = cmath.exp(2j * math.pi * float(ph_pre) / float(q_mod)) / math.sqrt(float(dim_b))
        amp_ideal = cmath.exp(2j * math.pi * float(ph_ideal) / float(q_mod)) / math.sqrt(float(dim_b))
        overlap += amp_pre.conjugate() * amp_ideal
    decoupled_fidelity = abs(overlap) ** 2

    return {
        "n_dim": n,
        "m_bits": m_bits,
        "q_mod": q_mod,
        "num_newton_steps": num_steps,
        "steps_history": steps_history,
        "exact_inverse_verified": exact_inverse_verified,
        "coupled_phases": coupled_phases,
        "decoupled_phases": decoupled_phases,
        "expected_secret_mod": expected_secret_mod,
        "decoupled_state_fidelity": decoupled_fidelity,
        "all_verified": (
            exact_inverse_verified
            and all(s["verified_identity_mod_2_pow_2j"] for s in steps_history)
            and decoupled_phases == expected_secret_mod
            and abs(decoupled_fidelity - 1.0) < 1e-12
        ),
    }


def generate_dcp_modular_inversion_newton_hensel_lifting_quantum_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the 2-adic Newton-Hensel matrix inversion bridge."""
    # 1. 3x3 invertible matrix over Z_{256} (m = 8 bits -> strictly 3 quadratic Newton steps: 1 -> 2 -> 4 -> 8 bits!)
    u_3x3 = [
        [1, 2, 3],
        [0, 1, 5],
        [2, 4, 1],
    ]
    audit_3x3_m8 = evaluate_newton_hensel_matrix_lifting_and_decoupling(
        u_mat=u_3x3,
        m_bits=8,
        test_secret_s=[137, 42, 219],
    )

    # 2. 4x4 invertible matrix over Z_{65536} (m = 16 bits -> strictly 4 quadratic Newton steps: 1 -> 2 -> 4 -> 8 -> 16 bits!)
    u_4x4 = [
        [1, 1, 2, 3],
        [2, 1, 1, 4],
        [4, 2, 1, 1],
        [2, 4, 2, 1],
    ]
    audit_4x4_m16 = evaluate_newton_hensel_matrix_lifting_and_decoupling(
        u_mat=u_4x4,
        m_bits=16,
        test_secret_s=[12345, 54321, 9999, 42424],
    )

    all_passed = (
        audit_3x3_m8["all_verified"]
        and audit_3x3_m8["num_newton_steps"] == 3
        and audit_4x4_m16["all_verified"]
        and audit_4x4_m16["num_newton_steps"] == 4
    )

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "proof_status": "LOCAL_DERIVATION_REVIEW_PENDING_NOT_FORMALLY_VERIFIED",
        "scope_constraints": {
            "applies_to": "2-adic Newton-Hensel quadratic matrix inversion over GL_n(Z_{2^m}) and phase-preconditioning decoupling of n compressed DCP wires",
            "does_not_claim": "Invertibility when det(U) == 0 (mod 2) prior to factoring out the maximal power of 2",
            "controls_included": "Includes 3x3 inversion mod 2^8 = 256 (3 Newton steps) and 4x4 inversion mod 2^16 = 65536 (4 Newton steps), verifying exact phase decoupling and 100% product state fidelity.",
        },
        "audit_3x3_mod256": audit_3x3_m8,
        "audit_4x4_mod65536": audit_4x4_m16,
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
