r"""DCP multi-secret block-matrix simultaneous CNOT peeling and cross-packet difference bridge.

Establishes the exact amortization and cross-packet interference laws when a single
public matrix header A in Z_{2^t}^{n x K} is shared across D >= 2 secret vectors
S = [s^{(1)}, ..., s^{(D)}] in Z_{2^t}^{n x D} (as in multi-secret / matrix LWE and
block DCP):

1. Universal Anchor-Independent Mod-2 Elimination Across All D Secrets:
   Because the mod-2 kernel ker(A mod 2) depends solely on the public header A, a single
   classical Gaussian elimination pass compiles ONE disjoint CNOT circuit U_CNOT(V) that,
   when applied independently to each of the D quantum packets |psi_A(s^{(d)})>,
   simultaneously maps every compressed wire j in {1, ..., m} into the even sublattice:
       A_tilde_j(x_0^{(d)}) in (2 * Z_{2^t})^n   for ALL d in {1, ..., D}
   and ALL independent syndrome realizations x_0^{(1)}, ..., x_0^{(D)} in {0, 1}^K!

2. Exact Cross-Packet CNOT Secret-Difference Phase Law:
   Let rho(a, s^{(1)}, gamma) and rho(a, s^{(2)}, gamma) be two single-qubit survivor
   wires sharing the same effective label a in Z_{2^t}^n (for instance, after anchor-free
   mod-2 elimination or Pauli-X sign rectification). Applying a cross-packet CNOT gate
   with packet 1 as control and packet 2 as target, followed by measuring the target
   packet in the computational Z basis (outcome b in {0, 1}, each with probability 1/2),
   prepares on the control wire the exact conditional state:
   - Outcome b = 0 (prob 1/2): rho(a, s^{(1)} + s^{(2)} mod 2^t, gamma^2),
   - Outcome b = 1 (prob 1/2): rho(a, s^{(1)} - s^{(2)} mod 2^t, gamma^2).
   Measuring the control wire in the Pauli-X basis on the b = 1 branch yields expectation:
       <X>_{b=1} = gamma^2 * cos(2*pi * <a, s^{(1)} - s^{(2)}> / 2^t),
   enabling direct quantum equality/difference testing between unknown secrets s^{(1)} and
   s^{(2)} without learning either individual secret!
"""

from __future__ import annotations

import cmath
import hashlib
import json
import math
from typing import Any, Dict, List


THEOREM_ID = "dcp_multi_secret_block_matrix_simultaneous_peeling_bridge"
SCHEMA_VERSION = "dcp-multi-secret-block-matrix-simultaneous-peeling-bridge-v1"


def evaluate_cross_packet_cnot_secret_difference_and_sum(
    q_mod: int,
    a_label: int,
    s1: int,
    s2: int,
    gamma: float,
) -> Dict[str, Any]:
    """Explicitly simulate the 4x4 two-packet density matrix under CNOT_{1->2} and Z-measurement on wire 2."""
    theta1 = 2.0 * math.pi * float((a_label * s1) % q_mod) / float(q_mod)
    theta2 = 2.0 * math.pi * float((a_label * s2) % q_mod) / float(q_mod)

    # Single-qubit density matrices: rho_d = [[0.5, 0.5*gamma*e^{-i*theta_d}], [0.5*gamma*e^{i*theta_d}, 0.5]]
    def _rho1(th: float) -> List[List[complex]]:
        return [
            [0.5 + 0j, 0.5 * gamma * cmath.exp(-1j * th)],
            [0.5 * gamma * cmath.exp(1j * th), 0.5 + 0j],
        ]

    r1 = _rho1(theta1)
    r2 = _rho1(theta2)

    # 4x4 tensor product rho_12 in basis |00>, |01>, |10>, |11>
    rho12 = [[0j] * 4 for _ in range(4)]
    for i1 in range(2):
        for j1 in range(2):
            for i2 in range(2):
                for j2 in range(2):
                    rho12[2 * i1 + i2][2 * j1 + j2] = r1[i1][j1] * r2[i2][j2]

    # Apply CNOT_{1->2}: maps basis index (u1, u2) -> (u1, u1 ^ u2)
    perm = [0, 1, 3, 2]
    rho_post = [[rho12[perm[r]][perm[c]] for c in range(4)] for r in range(4)]

    # Project wire 2 onto |b><b| for b = 0 and b = 1:
    prob_b0 = (rho_post[0][0] + rho_post[2][2]).real
    prob_b1 = (rho_post[1][1] + rho_post[3][3]).real

    cond_b0 = [
        [rho_post[0][0] / prob_b0, rho_post[0][2] / prob_b0],
        [rho_post[2][0] / prob_b0, rho_post[2][2] / prob_b0],
    ]
    cond_b1 = [
        [rho_post[1][1] / prob_b1, rho_post[1][3] / prob_b1],
        [rho_post[3][1] / prob_b1, rho_post[3][3] / prob_b1],
    ]

    theta_sum = 2.0 * math.pi * float((a_label * (s1 + s2)) % q_mod) / float(q_mod)
    theta_diff = 2.0 * math.pi * float((a_label * (s1 - s2)) % q_mod) / float(q_mod)

    expected_off_b0 = 0.5 * (gamma ** 2) * cmath.exp(-1j * theta_sum)
    expected_off_b1 = 0.5 * (gamma ** 2) * cmath.exp(-1j * theta_diff)

    err_b0 = abs(cond_b0[0][1] - expected_off_b0)
    err_b1 = abs(cond_b1[0][1] - expected_off_b1)

    x_exp_b0 = 2.0 * cond_b0[0][1].real
    x_exp_b1 = 2.0 * cond_b1[0][1].real

    return {
        "q_mod": q_mod,
        "a_label": a_label,
        "s1": s1,
        "s2": s2,
        "gamma": gamma,
        "prob_b0_sum_branch": prob_b0,
        "prob_b1_diff_branch": prob_b1,
        "x_expectation_b0_sum": x_exp_b0,
        "x_expectation_b1_diff": x_exp_b1,
        "closed_form_x_sum": (gamma ** 2) * math.cos(theta_sum),
        "closed_form_x_diff": (gamma ** 2) * math.cos(theta_diff),
        "max_density_matrix_error": max(err_b0, err_b1, abs(prob_b0 - 0.5), abs(prob_b1 - 0.5)),
        "exact_sum_and_diff_law_verified": (
            max(err_b0, err_b1, abs(prob_b0 - 0.5), abs(prob_b1 - 0.5)) < 1e-12
        ),
    }


def generate_dcp_multi_secret_block_matrix_simultaneous_peeling_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the multi-secret block-matrix peeling bridge."""
    # 1. Equal secrets control: s1 == s2 = 5 mod 8, a = 2 -> b=1 difference branch has phase 0 and <X> = +gamma^2!
    equal_secrets_control = evaluate_cross_packet_cnot_secret_difference_and_sum(
        q_mod=8, a_label=2, s1=5, s2=5, gamma=0.85
    )

    # 2. Opposite-parity difference control: s1 = 5, s2 = 3 mod 8 (s1 - s2 = 2), a = 2 -> 2*(s1-s2) = 4 == pi shift, <X>_{b=1} = -gamma^2!
    pi_difference_control = evaluate_cross_packet_cnot_secret_difference_and_sum(
        q_mod=8, a_label=2, s1=5, s2=3, gamma=0.85
    )

    # 3. Sum-zero control: s1 = 5, s2 = 3 mod 8 (s1 + s2 = 8 == 0 mod 8), a = 1 -> b=0 sum branch has phase 0 and <X>_{b=0} = +gamma^2!
    sum_zero_control = evaluate_cross_packet_cnot_secret_difference_and_sum(
        q_mod=8, a_label=1, s1=5, s2=3, gamma=0.85
    )

    all_passed = (
        equal_secrets_control["exact_sum_and_diff_law_verified"]
        and abs(equal_secrets_control["x_expectation_b1_diff"] - (0.85 ** 2)) < 1e-12
        and pi_difference_control["exact_sum_and_diff_law_verified"]
        and abs(pi_difference_control["x_expectation_b1_diff"] - (-(0.85 ** 2))) < 1e-12
        and sum_zero_control["exact_sum_and_diff_law_verified"]
        and abs(sum_zero_control["x_expectation_b0_sum"] - (0.85 ** 2)) < 1e-12
    )

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "proof_status": "LOCAL_DERIVATION_REVIEW_PENDING_NOT_FORMALLY_VERIFIED",
        "scope_constraints": {
            "applies_to": "Multi-secret block-matrix DCP CNOT witness amortization and cross-packet CNOT sum/difference phase extraction",
            "does_not_claim": "Cross-packet cancellation when the two packets have unmatched effective labels a^{(1)} != +/- a^{(2)} mod q",
            "controls_included": "Includes equal-secret control (s1=s2=5 mod 8, diff branch <X> = +gamma^2), pi-difference control (s1=5, s2=3, a=2, diff branch <X> = -gamma^2), and sum-zero control (s1+s2=0 mod 8, sum branch <X> = +gamma^2).",
        },
        "equal_secrets_control": equal_secrets_control,
        "pi_difference_control": pi_difference_control,
        "sum_zero_control": sum_zero_control,
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
