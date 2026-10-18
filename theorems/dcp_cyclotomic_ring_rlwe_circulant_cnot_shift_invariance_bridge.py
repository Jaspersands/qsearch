r"""DCP cyclotomic Ring-LWE negacyclic CNOT shift-invariance and wrap-around Pauli-X frame bridge.

Establishes the exact algebraic shift-orbit invariance of mod-2 kernel witnesses over
the cyclotomic polynomial ring R_{2^t} = Z_{2^t}[X] / (X^n + 1) (where n = 2^k) and
proves how Pauli-X sign-flip frame routing (Subsystem 78) restores exact negacyclic
shift equivariance across the X^n == -1 (mod 2^t) wrap-around boundary:

1. Exact Cyclic Shift Invariance of Mod-2 Kernel Witnesses Over R_{2^t}:
   Let a_1(X), ..., a_m(X) in R_{2^t} be public polynomials and let A in Z_{2^t}^{n x (m*n)}
   be the block-negacyclic matrix whose j-th block has columns given by the coefficient
   vectors of X^r * a_j(X) mod (X^n + 1) for r = 0, ..., n - 1.
   Because X^n == -1 == +1 (mod 2), reduction modulo 2 turns every negacyclic block into
   a standard cyclic circulant matrix over GF(2). Consequently, if v in {0, 1}^{m*n} is a
   mod-2 kernel witness (A v == 0 mod 2), then all n block-cyclic shifts S^r(v) (for
   r = 0, ..., n - 1) automatically satisfy:
       A S^r(v) == 0 (mod 2)   for ALL r in {0, ..., n - 1},
   providing an n-fold free amplification of classical witness compilation!

2. Negacyclic Wrap-Around Sign-Flip Law Over Z_{2^t} (t >= 2) and Pauli-X Rectification:
   When shifting a witness support wire across the degree-(n - 1) -> 0 boundary (where
   X * X^{n-1} = X^n = -1 in R_{2^t}), the column vector in Z_{2^t}^n is negated:
       coeff(X^n * a_j(X)) = -coeff(a_j(X)) (mod 2^t).
   Without sign rectification, shifting a weight-2 witness v across the wrap-around
   boundary changes the sum from a + b to a - b (mod 2^t), which can alter the upper
   bits modulo 2^t (for t >= 2) even though a + b == a - b == 0 (mod 2).
   Applying a single Pauli-X frame gate (which negates the wire's effective label
   c -> -c mod 2^t via Subsystem 78) on every wire that crosses the X^n = -1 boundary
   restores exact negacyclic equivariance:
       A_{rectified} S^r(v) == N^r (A v) (mod 2^t)
   across 100% of shifts r in {0, ..., n - 1}!
"""

from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, List, Sequence


THEOREM_ID = "dcp_cyclotomic_ring_rlwe_circulant_cnot_shift_invariance_bridge"
SCHEMA_VERSION = "dcp-cyclotomic-ring-rlwe-circulant-cnot-shift-invariance-bridge-v1"


def _negacyclic_shift_vec(vec: Sequence[int], r_shift: int, q_mod: int) -> List[int]:
    """Compute coefficient vector of X^{r_shift} * v(X) mod (X^n + 1, q_mod)."""
    n = len(vec)
    out = [0] * n
    for i, val in enumerate(vec):
        total_deg = i + r_shift
        wraps = total_deg // n
        rem = total_deg % n
        sign = -1 if (wraps & 1) else 1
        out[rem] = (out[rem] + sign * int(val)) % q_mod
    return out


def evaluate_negacyclic_shift_orbit_witnesses(
    n_deg: int,
    q_mod: int,
    poly_a: Sequence[int],
    poly_b: Sequence[int],
) -> Dict[str, Any]:
    """Verify n-fold mod-2 cyclic witness invariance and exact mod-q negacyclic equivariance under wrap-around Pauli-X rectification."""
    if len(poly_a) != n_deg or len(poly_b) != n_deg:
        raise ValueError("polynomials must have length n_deg")

    # Construct 2n columns: Block 0 is X^r * a(X), Block 1 is X^r * b(X) for r = 0..n-1
    cols_a = [_negacyclic_shift_vec(poly_a, r, q_mod) for r in range(n_deg)]
    cols_b = [_negacyclic_shift_vec(poly_b, r, q_mod) for r in range(n_deg)]

    # Base witness at shift r = 0: suppose poly_a + X^1 * poly_b == 0 (mod 2)
    # shifting by r in {0, ..., n-1} pairs column r of Block A with column (r + 1) mod n of Block B!
    base_sum_mod_q = [(cols_a[0][i] + cols_b[1][i]) % q_mod for i in range(n_deg)]
    base_is_mod2_zero = all((v % 2) == 0 for v in base_sum_mod_q)
    if not base_is_mod2_zero:
        raise ValueError("Base witness must satisfy a(X) + X * b(X) == 0 (mod 2)")

    shift_records: List[Dict[str, Any]] = []
    for r in range(n_deg):
        idx_a = r
        idx_b = (r + 1) % n_deg
        wrapped_b = (r + 1) >= n_deg

        # Unrectified cyclic shift sum: cols_a[idx_a] + cols_b[idx_b] mod q
        unrect_sum = [(cols_a[idx_a][i] + cols_b[idx_b][i]) % q_mod for i in range(n_deg)]
        unrect_mod2_zero = all((v % 2) == 0 for v in unrect_sum)

        # Pauli-X wrap-around rectified sum: if idx_b wrapped across X^n = -1, negate cols_b[idx_b] -> -cols_b[idx_b] mod q!
        sign_b = -1 if wrapped_b else 1
        rect_sum = [(cols_a[idx_a][i] + sign_b * cols_b[idx_b][i]) % q_mod for i in range(n_deg)]
        expected_negacyclic_sum = _negacyclic_shift_vec(base_sum_mod_q, r, q_mod)

        shift_records.append({
            "shift_r": r,
            "wrapped_across_xn_boundary": wrapped_b,
            "unrectified_is_mod2_kernel_witness": unrect_mod2_zero,
            "unrectified_matches_negacyclic_orbit_mod_q": unrect_sum == expected_negacyclic_sum,
            "pauli_x_rectified_matches_negacyclic_orbit_mod_q": rect_sum == expected_negacyclic_sum,
            "rectified_even_sublattice_vector": rect_sum,
        })

    return {
        "n_deg": n_deg,
        "q_mod": q_mod,
        "base_even_sublattice_vector": base_sum_mod_q,
        "shift_records": shift_records,
        "all_shifts_preserve_mod2_kernel": all(sr["unrectified_is_mod2_kernel_witness"] for sr in shift_records),
        "all_shifts_equivariant_under_pauli_x_wrap_frame": all(
            sr["pauli_x_rectified_matches_negacyclic_orbit_mod_q"] for sr in shift_records
        ),
        "wrap_around_requires_sign_flip": not shift_records[-1]["unrectified_matches_negacyclic_orbit_mod_q"],
    }


def generate_dcp_cyclotomic_ring_rlwe_circulant_cnot_shift_invariance_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the cyclotomic Ring-LWE negacyclic CNOT shift-invariance bridge."""
    # R_8 = Z_8[X] / (X^4 + 1):
    # Choose a(X) = 1 + 2X + 3X^2 + 0X^3 -> [1, 2, 3, 0]
    # We want X * b(X) == -a(X) (mod 2) and non-zero even sum mod 8:
    # Let b(X) = [1, 2, 1, 1] so X * b(X) = [-1, 1, 2, 1] == [7, 1, 2, 1] (mod 8).
    # Wait: a(X) + X * b(X) = [1+7, 2+1, 3+2, 0+1] -> let's pick b(X) so a(X) + X*b(X) is all even!
    # Since a(X) mod 2 = [1, 0, 1, 0], we need X * b(X) mod 2 = [1, 0, 1, 0], so b(X) mod 2 = [0, 1, 0, 1].
    # Take b(X) = [2, 1, 4, 3] -> X * b(X) mod 8 = [-3, 2, 1, 4] = [5, 2, 1, 4].
    # Then a(X) + X * b(X) mod 8 = [1+5, 2+2, 3+1, 0+4] = [6, 4, 4, 4] in (2*Z_8)^4!
    audit_n4_q8 = evaluate_negacyclic_shift_orbit_witnesses(
        n_deg=4,
        q_mod=8,
        poly_a=[1, 2, 3, 0],
        poly_b=[2, 1, 4, 3],
    )

    all_passed = (
        audit_n4_q8["all_shifts_preserve_mod2_kernel"]
        and audit_n4_q8["all_shifts_equivariant_under_pauli_x_wrap_frame"]
        and audit_n4_q8["wrap_around_requires_sign_flip"]
    )

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "proof_status": "LOCAL_DERIVATION_REVIEW_PENDING_NOT_FORMALLY_VERIFIED",
        "scope_constraints": {
            "applies_to": "Cyclotomic Ring-LWE / Ideal-DCP block-negacyclic CNOT witness shift orbits over R_{2^t} = Z_{2^t}[X]/(X^n + 1)",
            "does_not_claim": "Disjointness of shifted witnesses when the base witness uses multiple shifts within the same polynomial block",
            "controls_included": "Evaluates R_8 = Z_8[X]/(X^4+1) on a(X)=[1,2,3,0] and b(X)=[2,1,4,3], verifying 100% mod-2 kernel preservation across all 4 cyclic shifts and exact mod-8 negacyclic orbit equivariance under wrap-around Pauli-X sign rectification.",
        },
        "audit_n4_q8": audit_n4_q8,
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
