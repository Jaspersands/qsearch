r"""DCP Reed-Muller Boolean polynomial degree to CNOT parity phase-gadget synthesis bridge.

Establishes the exact (2^d - 1)-term Walsh-parity expansion of any degree-d multilinear
monomial 2^{d-1} prod_{j=1}^d u_j in Z and proves that every degree-d carry repair
unitary exp(i * (pi / 2^{d-1}) * prod_{j=1}^d u_j) (such as S at d=1, CZ at d=2, CCZ at
d=3, and C^3Z at d=4) decomposes into exactly 2^d - 1 single-qubit Z-rotations of angle
+/- pi / 2^{d-1} conjugated by CNOT parity trees:

1. Exact Integer Parity-XOR Decomposition of 2^{d-1} * prod_{j=1}^d u_j:
   For any binary variables u_1, ..., u_d in {0, 1} and any non-empty subset
   S subseteq {1, ..., d}, let p_S(u) = (+)_{j in S} u_j in {0, 1} denote the binary
   parity-XOR of S, so 1 - 2 * p_S(u) = (-1)^{sum_{j in S} u_j} = prod_{j in S} (1 - 2*u_j).
   Expanding prod_{j=1}^d u_j = 2^{-d} prod_{j=1}^d (1 - (1 - 2*u_j)) yields the EXACT
   integer identity over Z (holding without any modular reduction for ALL u in {0, 1}^d!):
       2^{d - 1} * prod_{j=1}^d u_j = sum_{emptyset != S subseteq {1, ..., d}} (-1)^{|S| - 1} * p_S(u)!

2. Exact (2^d - 1) Phase-Gadget Synthesis of Hypergraph Carry Repair Gates:
   Multiplying the integer identity by pi / 2^{d - 1} gives:
       pi * prod_{j=1}^d u_j = sum_{emptyset != S subseteq {1, ..., d}} (-1)^{|S| - 1} * (pi / 2^{d - 1}) * p_S(u).
   Therefore, the d-body controlled-Z gate C^{d-1}Z = diag((-1)^{u_1 ... u_d}) is
   synthesized EXACTLY by applying 2^d - 1 diagonal phase gadgets exp(i * (-1)^{|S|-1} * (pi / 2^{d-1}) * p_S(u)),
   each realized by computing the linear parity p_S(u) = (+)_{j in S} u_j via CNOTs and
   applying a single-qubit rotation of angle +/- pi / 2^{d-1}:
   - d = 2 (CZ):  2^2 - 1 = 3 S/S^dagger gadgets (+/- pi/2),
   - d = 3 (CCZ): 2^3 - 1 = 7 T/T^dagger gadgets (+/- pi/4),
   - d = 4 (C^3Z): 2^4 - 1 = 15 sqrt(T) gadgets (+/- pi/8)!
"""

from __future__ import annotations

import cmath
import hashlib
import itertools
import json
from typing import Any, Dict, List


THEOREM_ID = "dcp_reed_muller_boolean_polynomial_degree_cnot_depth_bridge"
SCHEMA_VERSION = "dcp-reed-muller-boolean-polynomial-degree-cnot-depth-bridge-v1"


def evaluate_parity_gadget_monomial_decomposition(d_degree: int) -> Dict[str, Any]:
    """Verify 2^{d-1} prod_{j=1}^d u_j == sum_{S != empty} (-1)^{|S|-1} p_S(u) over Z across all 2^d inputs."""
    if type(d_degree) is not int or d_degree < 1 or d_degree > 6:
        raise ValueError("d_degree must be an integer in [1, 6]")

    all_u = list(itertools.product((0, 1), repeat=d_degree))
    non_empty_subsets: List[tuple[int, ...]] = []
    for k_size in range(1, d_degree + 1):
        for comb in itertools.combinations(range(d_degree), k_size):
            non_empty_subsets.append(comb)

    expected_gadget_count = (1 << d_degree) - 1
    scale_factor = 1 << (d_degree - 1)

    max_int_identity_err = 0
    max_unitary_phase_err = 0.0

    for u_vec in all_u:
        # Left-hand side: 2^{d-1} * prod_{j=1}^d u_j
        prod_u = 1
        for b in u_vec:
            prod_u *= b
        lhs_int = scale_factor * prod_u

        # Right-hand side: sum_{S != empty} (-1)^{|S|-1} * ((+)_{j in S} u_j)
        rhs_int = 0
        for s_sub in non_empty_subsets:
            parity_s = 0
            for idx in s_sub:
                parity_s ^= u_vec[idx]
            sign_s = 1 if (len(s_sub) & 1) else -1
            rhs_int += sign_s * parity_s

        max_int_identity_err = max(max_int_identity_err, abs(lhs_int - rhs_int))

        # Check unitary phase equivalence for C^{d-1}Z: (-1)^{prod u_j} vs prod_S exp(i * (-1)^{|S|-1} * (pi / 2^{d-1}) * p_S(u))
        target_cz_phase = -1.0 + 0j if prod_u == 1 else 1.0 + 0j
        gadget_phase = cmath.exp(1j * cmath.pi * float(rhs_int) / float(scale_factor))
        max_unitary_phase_err = max(max_unitary_phase_err, abs(target_cz_phase - gadget_phase))

    return {
        "d_degree": d_degree,
        "parity_gadget_count_2d_minus_1": len(non_empty_subsets),
        "expected_gadget_count": expected_gadget_count,
        "rotation_denominator_2_pow_d_minus_1": scale_factor,
        "max_integer_identity_error": max_int_identity_err,
        "max_unitary_phase_error": max_unitary_phase_err,
        "exact_decomposition_verified": (
            len(non_empty_subsets) == expected_gadget_count
            and max_int_identity_err == 0
            and max_unitary_phase_err < 1e-12
        ),
    }


def generate_dcp_reed_muller_boolean_polynomial_degree_cnot_depth_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the Reed-Muller parity phase-gadget synthesis bridge."""
    sweep = [evaluate_parity_gadget_monomial_decomposition(d) for d in (1, 2, 3, 4, 5)]
    all_passed = (
        all(r["exact_decomposition_verified"] for r in sweep)
        and sweep[1]["parity_gadget_count_2d_minus_1"] == 3   # CZ = 3 S-gadgets
        and sweep[2]["parity_gadget_count_2d_minus_1"] == 7   # CCZ = 7 T-gadgets
        and sweep[3]["parity_gadget_count_2d_minus_1"] == 15  # C^3Z = 15 pi/8-gadgets
    )

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "proof_status": "LOCAL_DERIVATION_REVIEW_PENDING_NOT_FORMALLY_VERIFIED",
        "scope_constraints": {
            "applies_to": "Exact (2^d - 1)-term CNOT parity-gadget synthesis of degree-d multilinear carry monomials 2^{d-1} prod_{j=1}^d u_j",
            "does_not_claim": "Sub-exponential gadget count for unbounded degree d -> infty without modulo-2^t nilpotency truncation (Subsystem 87)",
            "controls_included": "Verifies exact integer identity error == 0 and unitary error < 1e-12 across d in {1, 2, 3, 4, 5} (1, 3, 7, 15, 31 parity gadgets).",
        },
        "degree_gadget_sweep": sweep,
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
