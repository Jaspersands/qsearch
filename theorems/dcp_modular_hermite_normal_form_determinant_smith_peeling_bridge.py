r"""DCP modular Smith Normal Form (SNF) invariant-factor channel decoupling bridge.

Establishes that for any n x n compressed DCP column matrix B in Z_q^{n x n} (even when
det(B) is NOT coprime to q, so 2-adic Newton-Hensel unit inversion in Subsystem 91 is
inapplicable), the Smith Normal Form decomposition:
    U * B * V == diag(d_1, d_2, ..., d_n) (mod q),
where U, V in GL_n(Z_q) have gcd(det(U), q) = gcd(det(V), q) = 1 and d_1 | d_2 | ... | d_n,
decouples the n-dimensional phase register into n completely independent cyclic subgroup
channels of orders q_i = q / gcd(d_i, q):

1. Exact Unimodular Equivalence & Channel Decoupling:
   For any wire excitation vector u in {0, 1}^n (or Z_q^n) with wire input v = V u mod q
   and transformed secret s_tilde = U^{-T} s mod q, the DCP phase inner product satisfies:
       <B v, s> == <B V u, U^T s_tilde> == <U B V u, s_tilde>
                == sum_{i=1}^n d_i * u_i * s_tilde_i (mod q)!
   Dividing by q in the phase exponent exp(2*pi*i <B v, s> / q) yields the EXACT product
   factorization across the n invariant coordinates:
       exp(2*pi*i * <B V u, s> / q) = prod_{i=1}^n exp( 2*pi*i * (d_i / gcd(d_i, q)) * u_i * s_tilde_i / q_i ),
   where q_i = q / gcd(d_i, q) is the effective cyclic modulus of channel i!

2. Exact Identifiable Coset Cardinality Law:
   As s ranges over all Q = q^n secrets in Z_q^n, the map s -> B^T s (mod q) has image
   isomorphic to Z_{q_1} x Z_{q_2} x ... x Z_{q_n}, of exact cardinality:
       |Im(B^T mod q)| = prod_{i=1}^n ( q / gcd(d_i, q) ),
   and kernel (indistinguishable secret coset fiber) of exact size:
       |ker(B^T mod q)| = prod_{i=1}^n gcd(d_i, q) = Q / |Im(B^T mod q)|!
"""

from __future__ import annotations

import cmath
import hashlib
import itertools
import json
import math
from typing import Any, Dict, List, Sequence, Tuple


THEOREM_ID = "dcp_modular_hermite_normal_form_determinant_smith_peeling_bridge"
SCHEMA_VERSION = "dcp-modular-hermite-normal-form-determinant-smith-peeling-bridge-v1"

IntMatrix = List[List[int]]


def _mat_mul_mod(a: Sequence[Sequence[int]], b: Sequence[Sequence[int]], q_mod: int) -> IntMatrix:
    n = len(a)
    return [
        [sum(int(a[i][k]) * int(b[k][j]) for k in range(n)) % q_mod for j in range(n)]
        for i in range(n)
    ]


def evaluate_smith_normal_form_channel_decoupling(
    q_mod: int,
    u_unimod: Sequence[Sequence[int]],
    v_unimod: Sequence[Sequence[int]],
    inv_factors_d: Sequence[int],
) -> Dict[str, Any]:
    """Construct B = U^{-1} diag(d) V^{-1} mod q (or test U B V == diag(d) mod q) and verify exact coset image cardinality and phase decoupling."""
    n = len(inv_factors_d)
    diag_d = [[int(inv_factors_d[i]) % q_mod if i == j else 0 for j in range(n)] for i in range(n)]

    # Check divisibility chain d_1 | d_2 | ... | d_n:
    divisibility_chain_ok = all(
        (inv_factors_d[i + 1] % inv_factors_d[i] == 0) if inv_factors_d[i] != 0 else (inv_factors_d[i + 1] == 0)
        for i in range(n - 1)
    )

    # Construct coupled matrix B such that U * B * V == diag(d) mod q by defining B_coupled = U_inv * diag(d) * V_inv:
    # Here we pass U_inv and V_inv directly via u_unimod, v_unimod as unimodular integer matrices (det == +/- 1),
    # and compute their exact unimodular inverses!
    def _invert_unimodular_2x2_or_3x3(m: Sequence[Sequence[int]]) -> IntMatrix:
        dim = len(m)
        if dim == 2:
            a, b = int(m[0][0]), int(m[0][1])
            c, d = int(m[1][0]), int(m[1][1])
            det = (a * d - b * c) % q_mod
            det_inv = pow(det, -1, q_mod)
            return [
                [(d * det_inv) % q_mod, (-b * det_inv) % q_mod],
                [(-c * det_inv) % q_mod, (a * det_inv) % q_mod],
            ]
        raise ValueError("Use 2x2 for explicit closed-form modular adjugate")

    u_inv = _invert_unimodular_2x2_or_3x3(u_unimod)
    v_inv = _invert_unimodular_2x2_or_3x3(v_unimod)

    b_coupled = _mat_mul_mod(_mat_mul_mod(u_inv, diag_d, q_mod), v_inv, q_mod)
    ubv_check = _mat_mul_mod(_mat_mul_mod(u_unimod, b_coupled, q_mod), v_unimod, q_mod)

    # 1. Enumerate all Q = q^n secrets s in Z_q^n and compute exact image size |{B^T s mod q}| and kernel size:
    all_s = list(itertools.product(range(q_mod), repeat=n))
    image_set = set()
    kernel_count = 0
    for s_vec in all_s:
        bt_s = tuple(
            sum(b_coupled[i][j] * s_vec[i] for i in range(n)) % q_mod
            for j in range(n)
        )
        image_set.add(bt_s)
        if all(x == 0 for x in bt_s):
            kernel_count += 1

    q_i_channels = [q_mod // math.gcd(int(d_val), q_mod) for d_val in inv_factors_d]
    gcd_factors = [math.gcd(int(d_val), q_mod) for d_val in inv_factors_d]

    expected_image_size = 1
    expected_kernel_size = 1
    for qi, gi in zip(q_i_channels, gcd_factors):
        expected_image_size *= qi
        expected_kernel_size *= gi

    # 2. Verify exact phase decoupling identity across all s in Z_q^n and u in {0,1}^n:
    # <B V u, s> == sum_i d_i u_i (U^{-T} s)_i (mod q)
    max_phase_decoupling_err = 0.0
    for s_vec in all_s:
        s_tilde = [
            sum(u_inv[r][i] * s_vec[r] for r in range(n)) % q_mod
            for i in range(n)
        ]
        for u_vec in itertools.product((0, 1), repeat=n):
            v_wire = [
                sum(int(v_unimod[j][k]) * u_vec[k] for k in range(n)) % q_mod
                for j in range(n)
            ]
            bv = [
                sum(b_coupled[i][j] * v_wire[j] for j in range(n)) % q_mod
                for i in range(n)
            ]
            dot_coupled = sum(bv[i] * s_vec[i] for i in range(n)) % q_mod
            dot_snf = sum(int(inv_factors_d[i]) * u_vec[i] * s_tilde[i] for i in range(n)) % q_mod

            ph_coupled = cmath.exp(2j * math.pi * float(dot_coupled) / float(q_mod))
            ph_snf = cmath.exp(2j * math.pi * float(dot_snf) / float(q_mod))
            max_phase_decoupling_err = max(max_phase_decoupling_err, abs(ph_coupled - ph_snf))

    return {
        "n_dim": n,
        "q_mod": q_mod,
        "invariant_factors_d": [int(d) for d in inv_factors_d],
        "channel_orders_q_i": q_i_channels,
        "coupled_matrix_B": b_coupled,
        "snf_diagonal_verified": ubv_check == diag_d,
        "divisibility_chain_verified": divisibility_chain_ok,
        "explicit_image_cardinality": len(image_set),
        "expected_image_cardinality": expected_image_size,
        "explicit_kernel_cardinality": kernel_count,
        "expected_kernel_cardinality": expected_kernel_size,
        "max_phase_decoupling_error": max_phase_decoupling_err,
        "exact_snf_laws_verified": (
            (ubv_check == diag_d)
            and divisibility_chain_ok
            and len(image_set) == expected_image_size
            and kernel_count == expected_kernel_size
            and max_phase_decoupling_err < 1e-12
        ),
    }


def generate_dcp_modular_hermite_normal_form_determinant_smith_peeling_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the Smith Normal Form invariant-factor decoupling bridge."""
    # 1. Rank-deficient / non-unit invariant factors over Z_8^2: d = [1, 2] -> q_1 = 8, q_2 = 4 -> 32 distinguishable cosets, kernel size 2!
    audit_d_1_2_mod8 = evaluate_smith_normal_form_channel_decoupling(
        q_mod=8,
        u_unimod=[[1, 3], [2, 7]],
        v_unimod=[[3, 2], [4, 3]],
        inv_factors_d=[1, 2],
    )

    # 2. Higher divisibility invariant factors over Z_{12}^2: d = [2, 6] -> gcd(2, 12)=2 (q_1=6), gcd(6, 12)=6 (q_2=2) -> 12 cosets, kernel size 12!
    audit_d_2_6_mod12 = evaluate_smith_normal_form_channel_decoupling(
        q_mod=12,
        u_unimod=[[1, 2], [2, 5]],
        v_unimod=[[1, 1], [0, 1]],
        inv_factors_d=[2, 6],
    )

    all_passed = (
        audit_d_1_2_mod8["exact_snf_laws_verified"]
        and audit_d_1_2_mod8["explicit_image_cardinality"] == 32
        and audit_d_2_6_mod12["exact_snf_laws_verified"]
        and audit_d_2_6_mod12["explicit_image_cardinality"] == 12
    )

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "proof_status": "LOCAL_DERIVATION_REVIEW_PENDING_NOT_FORMALLY_VERIFIED",
        "scope_constraints": {
            "applies_to": "Smith Normal Form U B V == diag(d_1, ..., d_n) mod q invariant-factor channel decoupling and coset capacity",
            "does_not_claim": "Recovery of secret components lying inside the non-trivial kernel ker(B^T mod q) of size prod_i gcd(d_i, q)",
            "controls_included": "Evaluates d=[1, 2] over Z_8^2 (|Im|=32, |ker|=2) and d=[2, 6] over Z_{12}^2 (|Im|=12, |ker|=12), verifying < 1e-12 phase decoupling error across all (s, u).",
        },
        "audit_d_1_2_mod8": audit_d_1_2_mod8,
        "audit_d_2_6_mod12": audit_d_2_6_mod12,
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
