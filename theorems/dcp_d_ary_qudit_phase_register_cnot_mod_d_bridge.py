r"""DCP d-ary qudit phase-register modular SUM carry and step-function linearity bridge.

Generalizes the dyadic mod-2^t CNOT hierarchy (Subsystems 51, 58, 63) to d-ary
qudit phase registers x_r in Z_d = {0, 1, ..., d - 1} over prime-power rings Z_{d^t}^n
(d >= 2, including qutrits d = 3 over Z_{3^t}) under the modular SUM gate
x_r(u; y) = (y_r + v_r * u) mod d (u in Z_d, y in Z_d^K):

1. Exact d-Adic Modular Carry Decomposition Over Z_{d^t}:
   Because (y_r + u) mod d = y_r + u - d * 1[y_r + u >= d] for all y_r, u in {0, ..., d - 1},
   the modular phase polynomial Phi(u; y) = sum_{r=1}^K A_{., r} ((y_r + v_r u) mod d) (mod d^t)
   satisfies the exact identity:
       Phi(u; y) - Phi(0; y) == (A v) * u - d * sum_{r in supp(v)} A_{., r} * 1[y_r + u >= d] (mod d^t).

2. Universal Mod-d Sublattice Descent Across All Syndromes y in Z_d^K:
   Because the carry term is multiplied by d, for ANY v in ker(A mod d) (so A v == 0 mod d):
       Phi(u; y) - Phi(0; y) == 0 (mod d)   for ALL y in Z_d^K and ALL u in Z_d!
   Thus every compressed phase increment lies deterministically in the index-d^n
   sublattice (d Z_{d^t})^n across 100% of syndromes y in Z_d^K.

3. Exact Step-Function Non-Linearity Dichotomy (d = 2 vs. d >= 3):
   - Qubit Case (d = 2, u in {0, 1}): Because u takes only two values {0, 1},
     1[y_r + u >= 2] == y_r * u is strictly LINEAR in u for every y_r in {0, 1}!
   - Higher-Radix Case (d >= 3, u in {0, 1, ..., d - 1}): Whenever y_r in {1, ..., d - 1},
     the threshold indicator c(y_r, u) = 1[y_r + u >= d] jumps from 0 to 1 at u = d - y_r
     and has non-zero discrete second difference Delta^2 c(y_r, u) in {+1, -1} != 0 (mod d).
     Consequently, for d >= 3 and t >= 2, Phi(u; y) - Phi(0; y) is affine-linear in u in Z_d
     modulo d^t across all syndromes y in Z_d^K if and only if every active column satisfies:
         d * A_{., r} == 0 (mod d^t)  <==>  A_{., r} == 0 (mod d^{t - 1}),
     while on the zero-syndrome branch y|_{supp(v)} = 0^h (probability d^{-(h - 1)}),
     1[0 + u >= d] == 0 identically, preserving exact linearity Phi(u; 0) - Phi(0; 0) == (A v) * u (mod d^t).
"""

from __future__ import annotations

import hashlib
import itertools
import json
from typing import Any, Dict, List, Sequence, Tuple


THEOREM_ID = "dcp_d_ary_qudit_phase_register_cnot_mod_d_bridge"
SCHEMA_VERSION = "dcp-d-ary-qudit-phase-register-cnot-mod-d-bridge-v1"


def verify_d_ary_qudit_sum_carry_and_linearity_criterion(
    a_matrix: Sequence[Sequence[int]],
    v_vec: Sequence[int],
    d_radix: int,
    t_exp: int,
) -> Dict[str, Any]:
    """Verify exact d-adic carry identity, universal mod-d descent, and step-function linearity iff condition."""
    if type(d_radix) is not int or d_radix < 2 or type(t_exp) is not int or t_exp < 1:
        raise ValueError("d_radix >= 2 and t_exp >= 1 required")
    q_mod = d_radix ** t_exp
    q_prev = d_radix ** (t_exp - 1)
    n_rows = len(a_matrix)
    k_cols = len(v_vec)
    supp = [r for r in range(k_cols) if int(v_vec[r]) != 0]
    if not supp:
        raise ValueError("v_vec must be non-empty")

    in_mod_d_kernel = all(
        (sum(int(a_matrix[i][r]) * int(v_vec[r]) for r in range(k_cols)) % d_radix) == 0
        for i in range(n_rows)
    )
    support_divisible_by_d_to_t_minus_1 = all(
        (int(a_matrix[i][r]) % q_prev) == 0 for r in supp for i in range(n_rows)
    )

    carry_identity_exact = True
    universal_mod_d_descent = True
    linear_anchor_count = 0
    total_anchors = d_radix ** k_cols

    for y_vec in itertools.product(range(d_radix), repeat=k_cols):
        phi_u: List[Tuple[int, ...]] = []
        for u_val in range(d_radix):
            direct = tuple(
                sum(
                    int(a_matrix[i][r]) * ((y_vec[r] + int(v_vec[r]) * u_val) % d_radix)
                    for r in range(k_cols)
                )
                % q_mod
                for i in range(n_rows)
            )
            phi_0 = tuple(
                sum(int(a_matrix[i][r]) * y_vec[r] for r in range(k_cols)) % q_mod
                for i in range(n_rows)
            )
            av_u_minus_carry = tuple(
                (
                    phi_0[i]
                    + sum(int(a_matrix[i][r]) * int(v_vec[r]) for r in range(k_cols)) * u_val
                    - d_radix
                    * sum(
                        int(a_matrix[i][r]) * (1 if (y_vec[r] + int(v_vec[r]) * u_val) >= d_radix else 0)
                        for r in supp
                    )
                )
                % q_mod
                for i in range(n_rows)
            )
            if direct != av_u_minus_carry:
                carry_identity_exact = False
            if in_mod_d_kernel:
                if any(((direct[i] - phi_0[i]) % d_radix) != 0 for i in range(n_rows)):
                    universal_mod_d_descent = False
            phi_u.append(direct)

        # Check whether Phi(u; y) - Phi(0; y) is linear in u in {0, ..., d-1} mod d^t:
        # i.e. Phi(u; y) - Phi(0; y) == u * (Phi(1; y) - Phi(0; y)) mod d^t for all u
        slope = tuple((phi_u[1][i] - phi_u[0][i]) % q_mod for i in range(n_rows))
        is_linear = all(
            tuple((phi_u[u_val][i] - phi_u[0][i]) % q_mod for i in range(n_rows))
            == tuple((u_val * slope[i]) % q_mod for i in range(n_rows))
            for u_val in range(d_radix)
        )
        if is_linear:
            linear_anchor_count += 1

    all_anchors_linear = linear_anchor_count == total_anchors
    expected_all_linear = True if d_radix == 2 else support_divisible_by_d_to_t_minus_1

    return {
        "d_radix": d_radix,
        "t_exp": t_exp,
        "q_mod": q_mod,
        "n": n_rows,
        "K": k_cols,
        "in_mod_d_kernel": in_mod_d_kernel,
        "support_divisible_by_d_to_t_minus_1": support_divisible_by_d_to_t_minus_1,
        "carry_identity_exact": carry_identity_exact,
        "universal_mod_d_descent_verified": universal_mod_d_descent,
        "linear_anchor_fraction": linear_anchor_count / float(total_anchors),
        "all_anchors_linear_in_u": all_anchors_linear,
        "linearity_characterization_verified": (
            carry_identity_exact
            and universal_mod_d_descent
            and (all_anchors_linear == expected_all_linear)
        ),
    }


def generate_dcp_d_ary_qudit_phase_register_cnot_mod_d_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the d-ary qudit phase-register CNOT mod-d bridge."""
    # 1. Qubit d = 2, t = 3 (q = 8) control: 100% of anchors have linear phase in u in {0, 1}!
    d2_qubit_linear_control = verify_d_ary_qudit_sum_carry_and_linearity_criterion(
        a_matrix=[[1, 3]],
        v_vec=[1, 1],
        d_radix=2,
        t_exp=3,
    )

    # 2. Qutrit d = 3, t = 2 (q = 9) non-multiple-of-3 columns A = [[1, 2]], v = [1, 1] (Av = 3 == 0 mod 3):
    # Universal mod-3 descent holds on 100% of anchors, but step-function carry breaks u-linearity on non-zero anchors (only y=(0,0) is linear: 1/9)!
    d3_qutrit_step_obstruction = verify_d_ary_qudit_sum_carry_and_linearity_criterion(
        a_matrix=[[1, 2]],
        v_vec=[1, 1],
        d_radix=3,
        t_exp=2,
    )

    # 3. Qutrit d = 3, t = 2 (q = 9) constructive multiple-of-3 control A = [[3, 6, 1]], v = [1, 1, 0]:
    # Active columns are 0 mod 3 (d^{t-1} = 3), so 100% of anchors are strictly linear in u in {0, 1, 2} mod 9!
    d3_qutrit_divisible_control = verify_d_ary_qudit_sum_carry_and_linearity_criterion(
        a_matrix=[[3, 6, 1]],
        v_vec=[1, 1, 0],
        d_radix=3,
        t_exp=2,
    )

    all_passed = (
        d2_qubit_linear_control["linearity_characterization_verified"]
        and d2_qubit_linear_control["all_anchors_linear_in_u"]
        and d3_qutrit_step_obstruction["linearity_characterization_verified"]
        and not d3_qutrit_step_obstruction["all_anchors_linear_in_u"]
        and abs(d3_qutrit_step_obstruction["linear_anchor_fraction"] - (1.0 / 3.0)) < 1e-12
        and d3_qutrit_divisible_control["linearity_characterization_verified"]
        and d3_qutrit_divisible_control["all_anchors_linear_in_u"]
    )

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "proof_status": "LOCAL_DERIVATION_REVIEW_PENDING_NOT_FORMALLY_VERIFIED",
        "scope_constraints": {
            "applies_to": "d-ary qudit modular SUM compression x_r(u; y) = (y_r + v_r u) mod d over Z_{d^t}^n",
            "does_not_claim": "Failure of mod-d sublattice descent or failure of linearity on the d monochrome syndromes y|_{supp(v)} = c * 1^h at t=2",
            "controls_included": "Includes d=2 universal 2-point linearity control, d=3 qutrit mod-9 step-function non-linearity audit on A=[[1,2]] (universal mod-3 descent + 1/3 monochrome linear anchor fraction), and d=3 constructive multiple-of-3 linearity control A=[[3,6,1]].",
        },
        "d2_qubit_linear_control": d2_qubit_linear_control,
        "d3_qutrit_step_nonlinearity_audit": d3_qutrit_step_obstruction,
        "d3_qutrit_multiple_of_3_constructive_control": d3_qutrit_divisible_control,
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
