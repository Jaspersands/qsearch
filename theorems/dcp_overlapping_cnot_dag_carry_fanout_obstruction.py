"""DCP overlapping CNOT DAG carry fanout and multilinear cross-term obstruction.

Establishes for any m-wire CNOT DAG compression x(u; x_0) = x_0 xor (V u) in {0,1}^K
where V in {0,1}^{K x m} may have overlapping column supports (row fanout d_r = sum_{j=1}^m V_{r,j}):

1. Exact Arithmetic-XOR Multilinear Expansion over Z_{2^t}:
   For each row r in {1, ..., K} with active wire set S_r = {j : V_{r,j} == 1},
       x_r(u; x_0) = (x_0)_r + (1 - 2*(x_0)_r) * sum_{emptyset != J subseteq S_r} (-2)^{|J| - 1} prod_{j in J} u_j.
   Consequently, the modular phase polynomial P(u; x_0) = A x(u; x_0) mod 2^t decomposes into:
     - Constant anchor offset: A x_0 mod 2^t,
     - Linear wire terms (|J| = 1): sum_{j=1}^m tilde_A_j(x_0) u_j mod 2^t,
     - Higher-degree cross-terms (|J| >= 2):
       Delta_cross(u; x_0) = sum_{r : |S_r| >= 2} (1 - 2*(x_0)_r) A_{., r} sum_{J subseteq S_r, |J| >= 2} (-2)^{|J| - 1} prod_{j in J} u_j mod 2^t.

2. Exact All-Anchor Linearity Criterion (including aggregate cancellations):
   Delta_cross(u; x_0) == 0 (mod 2^t) for all u in {0,1}^m and all anchors x_0 in {0,1}^K
   if and only if BOTH conditions hold:
       4 * A_{., r} == 0 (mod 2^t) for every shared row r,
       2 * sum_{r : j,k in S_r} A_{., r} == 0 (mod 2^t) for every wire pair j < k.
   Necessity: isolate the quadratic coefficient and toggle one anchor bit.
   Sufficiency: pair coefficients vanish at anchor zero and every toggle changes
   them by 4*A; all degree >= 3 coefficients vanish termwise by the same condition.
   The old termwise 2*A == 0 condition is sufficient, NOT necessary.

3. Scoped Controls:
   - Disjoint-Support Control (|S_r| <= 1 for all r): Delta_cross == 0 identically for all A and t.
   - Mod-2 Control (t = 1, q = 2): 2^{t-1} = 1 divides every integer, so Delta_cross == 0 mod 2 for any overlapping V.
   - Half-Period Shared-Row Control (A_{., r} == 2^{t-1} mod 2^t on shared rows): Delta_cross == 0 mod 2^t.
   - Odd shared rows obstruct ALL-anchor linearity for t >= 3; at t = 2
     aggregate cancellation can restore it even with odd shared rows.
   This is modular label linearity, not an all-secret or all-receiver no-go.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from typing import Any, Dict, List, Sequence, Tuple


THEOREM_ID = "dcp_overlapping_cnot_dag_carry_fanout_obstruction"
SCHEMA_VERSION = "dcp-overlapping-cnot-dag-carry-fanout-obstruction-v2"


def all_anchor_linearity_conditions(a_matrix, v_matrix, t_bits):
    """Polynomial-size exact criterion; no anchor or wire assignment enumeration."""
    if type(t_bits) is not int or t_bits < 1:
        raise ValueError("positive integer modulus exponent required")
    if not a_matrix or not v_matrix or not v_matrix[0]:
        raise ValueError("nonempty matrix dimensions required")
    k, m = len(v_matrix), len(v_matrix[0])
    if (any(len(row) != k for row in a_matrix)
            or any(len(row) != m for row in v_matrix)
            or any(type(x) is not int for row in a_matrix for x in row)
            or any(type(x) is not int or x not in (0, 1) for row in v_matrix for x in row)):
        raise ValueError("integer A and matching rectangular binary V required")
    q = 1 << t_bits
    shared = [r for r, row in enumerate(v_matrix) if sum(row) >= 2]
    toggles = all(4*row[r] % q == 0 for row in a_matrix for r in shared)
    pairs = all(2*sum(row[r] for r in range(k) if v_matrix[r][j] and v_matrix[r][l]) % q == 0
                for row in a_matrix for j in range(m) for l in range(j+1, m))
    termwise = all(2*row[r] % q == 0 for row in a_matrix for r in shared)
    return {"anchor_toggle_condition": toggles, "aggregate_pair_condition": pairs,
            "all_anchor_linearity_predicted": toggles and pairs,
            "old_termwise_sufficient_condition": termwise}


def evaluate_overlapping_dag_cross_terms(
    a_matrix: Sequence[Sequence[int]],
    v_matrix: Sequence[Sequence[int]],
    t_bits: int,
) -> Dict[str, Any]:
    """Verify exact multilinear expansion of A(x_0 xor V u) mod 2^t and check the cross-term vanishing criterion."""
    conditions = all_anchor_linearity_conditions(a_matrix, v_matrix, t_bits)
    q_mod = 1 << t_bits
    half_mod = 1 << (t_bits - 1)
    n_rows = len(a_matrix)
    k_rows = len(v_matrix)
    m_wires = len(v_matrix[0])

    row_fanouts = [sum(1 for j in range(m_wires) if v_matrix[r][j]) for r in range(k_rows)]
    shared_rows = [r for r, d_r in enumerate(row_fanouts) if d_r >= 2]

    shared_rows_divisible_by_half_mod = all(
        (int(a_matrix[i][r]) % half_mod == 0)
        for r in shared_rows
        for i in range(n_rows)
    )

    max_multilinear_expansion_err = 0
    non_zero_cross_term_count = 0
    total_evaluations = (1 << k_rows) * (1 << m_wires)

    for x0 in itertools.product((0, 1), repeat=k_rows):
        # Precompute linear effective columns tilde_A_j(x_0)
        tilde_cols = []
        for j in range(m_wires):
            col = [
                sum(
                    int(v_matrix[r][j]) * (1 - 2 * int(x0[r])) * int(a_matrix[i][r])
                    for r in range(k_rows)
                )
                % q_mod
                for i in range(n_rows)
            ]
            tilde_cols.append(col)

        for u in itertools.product((0, 1), repeat=m_wires):
            # 1. Direct XOR evaluation: x_r = (x_0)_r xor (oplus_j V_{r,j} u_j)
            x_xor = [
                (int(x0[r]) ^ (sum(int(v_matrix[r][j]) * int(u[j]) for j in range(m_wires)) & 1))
                for r in range(k_rows)
            ]
            direct_phase = [
                sum(int(a_matrix[i][r]) * x_xor[r] for r in range(k_rows)) % q_mod
                for i in range(n_rows)
            ]

            # 2. Constant + linear approximation: A x_0 + sum_j tilde_A_j(x_0) u_j mod 2^t
            linear_approx = [
                (
                    sum(int(a_matrix[i][r]) * int(x0[r]) for r in range(k_rows))
                    + sum(tilde_cols[j][i] * int(u[j]) for j in range(m_wires))
                )
                % q_mod
                for i in range(n_rows)
            ]

            # 3. Exact higher-order multilinear cross-terms (|J| >= 2)
            cross_term = [0] * n_rows
            for r in shared_rows:
                active_js = [j for j in range(m_wires) if v_matrix[r][j] and u[j]]
                # Since prod_{j in J} u_j == 1 iff J subseteq active_js:
                if len(active_js) >= 2:
                    k_act = len(active_js)
                    # sum_{s=2}^{k_act} C(k_act, s) (-2)^{s-1}
                    # Note: 1 - 2*k_act + sum_{s=2}^{k_act} C(k_act, s) (-2)^{s} = (1 - 2)^{k_act} = (-1)^{k_act}
                    # Wait: sum_{s=1}^{k_act} C(k_act, s) (-2)^{s-1} = (1 - (-1)^{k_act}) / 2 = k_act mod 2!
                    # So sum_{s=2}^{k_act} C(k_act, s) (-2)^{s-1} = (k_act mod 2) - k_act!
                    coeff = (k_act % 2) - k_act
                    sign_x0 = 1 - 2 * int(x0[r])
                    for i in range(n_rows):
                        cross_term[i] = (
                            cross_term[i] + sign_x0 * int(a_matrix[i][r]) * coeff
                        ) % q_mod

            reconstructed = [
                (linear_approx[i] + cross_term[i]) % q_mod for i in range(n_rows)
            ]
            for i in range(n_rows):
                err = abs(direct_phase[i] - reconstructed[i])
                if err > max_multilinear_expansion_err:
                    max_multilinear_expansion_err = err

            if any(c != 0 for c in cross_term):
                non_zero_cross_term_count += 1

    cross_terms_identically_zero = non_zero_cross_term_count == 0
    iff_criterion_verified = cross_terms_identically_zero == conditions["all_anchor_linearity_predicted"]

    return {
        "n": n_rows,
        "K": k_rows,
        "m": m_wires,
        "t": t_bits,
        "shared_row_indices": shared_rows,
        "shared_rows_divisible_by_2_to_t_minus_1": shared_rows_divisible_by_half_mod,
        "max_multilinear_expansion_error": max_multilinear_expansion_err,
        "non_zero_cross_term_evaluations": non_zero_cross_term_count,
        "total_evaluations": total_evaluations,
        "cross_terms_identically_zero": cross_terms_identically_zero,
        "analytic_conditions": conditions,
        "iff_criterion_verified": (
            max_multilinear_expansion_err == 0 and iff_criterion_verified
        ),
    }


def generate_dcp_overlapping_cnot_dag_carry_fanout_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the overlapping CNOT DAG carry fanout obstruction."""
    # 1. Overlapping DAG with odd shared row r=1 (t=3, q=8): V = [[1,0],[1,1],[0,1]]
    odd_shared_row_obstruction = evaluate_overlapping_dag_cross_terms(
        a_matrix=[[3, 1, 5]],
        v_matrix=[[1, 0], [1, 1], [0, 1]],
        t_bits=3,
    )

    # 2. Disjoint-support control: V = [[1,0],[1,0],[0,1],[0,1]] -> no shared rows, zero cross-terms
    disjoint_support_control = evaluate_overlapping_dag_cross_terms(
        a_matrix=[[3, 5, 1, 7]],
        v_matrix=[[1, 0], [1, 0], [0, 1], [0, 1]],
        t_bits=3,
    )

    # 3. Half-period shared-row constructive control (t=3, q=8, shared row r=1 has A_{0,1} = 4 == 0 mod 4):
    half_period_shared_row_control = evaluate_overlapping_dag_cross_terms(
        a_matrix=[[3, 4, 5]],
        v_matrix=[[1, 0], [1, 1], [0, 1]],
        t_bits=3,
    )

    # 4. Mod-2 (t=1, q=2) constructive control: overlapping DAG has zero cross-terms mod 2
    mod2_overlapping_control = evaluate_overlapping_dag_cross_terms(
        a_matrix=[[1, 1, 1]],
        v_matrix=[[1, 0], [1, 1], [0, 1]],
        t_bits=1,
    )

    # Full-column-rank V: duplicate shared rows cancel at q=4 for EVERY anchor.
    cancellation_control = evaluate_overlapping_dag_cross_terms(
        [[1, 1, 3, 5]], [[1, 1], [1, 1], [1, 0], [0, 1]], 2,
    )

    all_passed = (
        odd_shared_row_obstruction["iff_criterion_verified"]
        and not odd_shared_row_obstruction["cross_terms_identically_zero"]
        and disjoint_support_control["iff_criterion_verified"]
        and disjoint_support_control["cross_terms_identically_zero"]
        and half_period_shared_row_control["iff_criterion_verified"]
        and half_period_shared_row_control["cross_terms_identically_zero"]
        and mod2_overlapping_control["iff_criterion_verified"]
        and mod2_overlapping_control["cross_terms_identically_zero"]
        and cancellation_control["iff_criterion_verified"]
        and cancellation_control["cross_terms_identically_zero"]
        and not cancellation_control["analytic_conditions"]["old_termwise_sufficient_condition"]
    )

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "scope_constraints": {
            "applies_to": "Overlapping CNOT DAG wire compression x(u; x_0) = x_0 xor (V u) over Z_{2^t}",
            "does_not_claim": "Termwise necessity, impossibility for a fixed anchor or secret, or a general receiver no-go. Aggregate cancellations are retained.",
            "controls_included": "Includes odd shared-row quadratic carry cross-term audit alongside disjoint-support, half-period shared-row, and t=1 mod-2 constructive zero-cross-term controls.",
        },
        "odd_shared_row_obstruction": odd_shared_row_obstruction,
        "disjoint_support_control": disjoint_support_control,
        "half_period_shared_row_control": half_period_shared_row_control,
        "mod2_overlapping_control": mod2_overlapping_control,
        "aggregate_cancellation_counterexample_to_v1": cancellation_control,
        "v1_termwise_necessity_retracted": True,
        "general_derivation_review_pending": True,
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
