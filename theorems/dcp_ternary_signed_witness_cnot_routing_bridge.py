r"""DCP ternary signed-support witness extraction and CNOT-syndrome routing bridge.

Connects the ternary zero-sum relation law of Subsystem 76 (A * delta == 0 mod q
with delta in {-1, 0, +1}^K \ {0^K}) to physical CNOT-star syndrome routing and
Pigeonhole collision guarantees:

1. Exact Bijection Between Signed Ternary Supports and CNOT Syndrome Branches:
   Let delta in {-1, 0, +1}^K be a ternary vector with support S = {r_0 < r_1 < ... < r_{w-1}}
   of size w = ||delta||_1 >= 2, normalized by global sign so that delta_{r_0} = +1.
   Applying the w-wire CNOT star with control r_0 and targets r_1, ..., r_{w-1} produces
   on syndrome branch d = (d_1, ..., d_{w-1}) in {0, 1}^{w-1} the effective column:
       tilde_A(S, d) = A_{., r_0} + sum_{j=1}^{w-1} (1 - 2 * d_j) A_{., r_j} (mod q).
   Therefore, 1 - 2 * d_j == delta_{r_j} for all j = 1, ..., w - 1 holds on the UNIQUE
   canonical syndrome branch:
       d_j^*(delta) = (1 - delta_{r_j}) / 2 in {0, 1},   j = 1, ..., w - 1,
   which occurs with exact Born probability 2^{-(w - 1)}.
   More generally, if the support S admits M_{tern}(S) distinct signed zero-sum vectors
   delta in {+1} x {-1, +1}^{w-1} with A * delta == 0 (mod q), a single CNOT star on S
   succeeds on M_{tern}(S) syndrome branches with total zero-sum probability M_{tern}(S) / 2^{w-1}.

2. Pigeonhole Threshold Separation (K > n log_2(q) for Ternary vs. Binary Empty Regimes):
   By Pigeonhole Principle on the 2^K binary vectors x in {0, 1}^K, whenever 2^K > q^n
   (i.e. K >= floor(n * log_2(q)) + 1), there ALWAYS exist two distinct binary vectors
   x != y in {0, 1}^K with A x == A y (mod q), whose difference delta = x - y in {-1, 0, +1}^K \ {0^K}
   is a guaranteed non-trivial ternary zero-sum witness A * delta == 0 (mod q), EVEN when
   A admits ZERO non-empty binary zero-sum witnesses v in {0, 1}^K \ {0^K}!
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from typing import Any, Dict, List, Sequence, Tuple


THEOREM_ID = "dcp_ternary_signed_witness_cnot_routing_bridge"
SCHEMA_VERSION = "dcp-ternary-signed-witness-cnot-routing-bridge-v1"


def canonical_syndrome_for_ternary_witness(
    delta_vec: Sequence[int],
) -> Dict[str, Any]:
    """Map a ternary witness delta in {-1, 0, +1}^K (with first non-zero entry +1) to its support and CNOT syndrome d^*(delta)."""
    supp = [r for r, val in enumerate(delta_vec) if int(val) != 0]
    if not supp:
        raise ValueError("delta_vec must be non-zero")
    if any(int(val) not in (-1, 0, 1) for val in delta_vec):
        raise ValueError("delta_vec entries must lie in {-1, 0, +1}")
    sign_0 = int(delta_vec[supp[0]])
    oriented = [sign_0 * int(val) for val in delta_vec]
    syndrome_bits = tuple((1 - oriented[r]) // 2 for r in supp[1:])
    return {
        "support_indices": supp,
        "hamming_weight_w": len(supp),
        "oriented_delta": oriented,
        "target_syndrome_bits": list(syndrome_bits),
        "branch_probability": 2.0 ** (-(len(supp) - 1)),
    }


def evaluate_binary_vs_ternary_zero_sum_witnesses(
    a_matrix: Sequence[Sequence[int]],
    q_mod: int,
) -> Dict[str, Any]:
    """Enumerate all non-empty binary and oriented ternary zero-sum witnesses mod q and verify CNOT branch bijection."""
    if type(q_mod) is not int or q_mod < 2:
        raise ValueError("q_mod must be an integer >= 2")
    n_rows = len(a_matrix)
    k_cols = len(a_matrix[0])

    binary_witnesses: List[Tuple[int, ...]] = []
    for v in itertools.product((0, 1), repeat=k_cols):
        if not any(v):
            continue
        if all((sum(int(a_matrix[i][r]) * v[r] for r in range(k_cols)) % q_mod) == 0 for i in range(n_rows)):
            binary_witnesses.append(v)

    oriented_ternary_witnesses: List[Tuple[int, ...]] = []
    bijection_verified = True

    for delta in itertools.product((-1, 0, 1), repeat=k_cols):
        supp = [r for r, val in enumerate(delta) if val != 0]
        if not supp or delta[supp[0]] != 1:
            continue
        is_zero = all(
            (sum(int(a_matrix[i][r]) * delta[r] for r in range(k_cols)) % q_mod) == 0
            for i in range(n_rows)
        )
        if is_zero:
            oriented_ternary_witnesses.append(delta)
            info = canonical_syndrome_for_ternary_witness(delta)
            d_bits = info["target_syndrome_bits"]
            r0 = supp[0]
            realized = tuple(
                (
                    int(a_matrix[i][r0])
                    + sum((1 - 2 * d_bits[idx]) * int(a_matrix[i][r]) for idx, r in enumerate(supp[1:]))
                )
                % q_mod
                for i in range(n_rows)
            )
            if any(c != 0 for c in realized):
                bijection_verified = False

    pigeonhole_guaranteed = (1 << k_cols) > (q_mod ** n_rows)

    return {
        "n": n_rows,
        "K": k_cols,
        "q_mod": q_mod,
        "two_to_K": 1 << k_cols,
        "q_to_n": q_mod ** n_rows,
        "pigeonhole_ternary_collision_guaranteed": pigeonhole_guaranteed,
        "binary_zero_sum_witness_count": len(binary_witnesses),
        "oriented_ternary_zero_sum_witness_count": len(oriented_ternary_witnesses),
        "cnot_syndrome_bijection_verified": bijection_verified,
        "pigeonhole_guarantee_respected": (len(oriented_ternary_witnesses) >= 1) if pigeonhole_guaranteed else True,
    }


def generate_dcp_ternary_signed_witness_cnot_routing_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the ternary signed-witness CNOT routing bridge."""
    # 1. Binary-empty but ternary-rich separation control: q = 5, n = 1, K = 3, A = [[1, 1, 1]] mod 5
    # 2^3 = 8 > 5^1: 0 binary witnesses, but 3 oriented weight-2 ternary witnesses (1,-1,0), (1,0,-1), (0,1,-1)!
    q5_binary_empty_control = evaluate_binary_vs_ternary_zero_sum_witnesses(
        a_matrix=[[1, 1, 1]],
        q_mod=5,
    )

    # 2. Dyadic q = 8, n = 1, K = 4, A = [[1, 1, 1, 1]] mod 8:
    # 2^4 = 16 > 8: 0 binary witnesses (max sum is 4 != 0 mod 8), but 9 oriented ternary zero-sum witnesses!
    q8_dyadic_binary_empty_control = evaluate_binary_vs_ternary_zero_sum_witnesses(
        a_matrix=[[1, 1, 1, 1]],
        q_mod=8,
    )

    # 3. 2D instance: q = 3, n = 2, K = 4 (2^4 = 16 > 3^2 = 9), A = [[1, 1, 0, 2], [0, 1, 1, 1]] mod 3
    q3_2d_audit = evaluate_binary_vs_ternary_zero_sum_witnesses(
        a_matrix=[[1, 1, 0, 2], [0, 1, 1, 1]],
        q_mod=3,
    )

    all_passed = (
        q5_binary_empty_control["cnot_syndrome_bijection_verified"]
        and q5_binary_empty_control["binary_zero_sum_witness_count"] == 0
        and q5_binary_empty_control["oriented_ternary_zero_sum_witness_count"] == 3
        and q8_dyadic_binary_empty_control["cnot_syndrome_bijection_verified"]
        and q8_dyadic_binary_empty_control["binary_zero_sum_witness_count"] == 0
        and q8_dyadic_binary_empty_control["oriented_ternary_zero_sum_witness_count"] == 9
        and q3_2d_audit["cnot_syndrome_bijection_verified"]
        and q3_2d_audit["pigeonhole_guarantee_respected"]
    )

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "proof_status": "LOCAL_DERIVATION_REVIEW_PENDING_NOT_FORMALLY_VERIFIED",
        "scope_constraints": {
            "applies_to": "Signed ternary zero-sum witnesses delta in {-1, 0, +1}^K and their realization via w-wire CNOT star syndrome branches",
            "does_not_claim": "Deterministic single-shot projection onto d^*(delta) without paying the 2^{-(w-1)} syndrome branch probability",
            "controls_included": "Includes q=5 (A=[[1,1,1]]) and dyadic q=8 (A=[[1,1,1,1]]) controls with 0 binary witnesses vs. 3 and 9 ternary witnesses, plus 2D q=3 pigeonhole verification.",
        },
        "q5_binary_empty_ternary_rich_control": q5_binary_empty_control,
        "q8_dyadic_binary_empty_control": q8_dyadic_binary_empty_control,
        "q3_2d_pigeonhole_audit": q3_2d_audit,
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
