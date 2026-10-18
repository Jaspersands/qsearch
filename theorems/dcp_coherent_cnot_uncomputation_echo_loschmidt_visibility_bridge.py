r"""DCP coherent CNOT uncomputation echo (Loschmidt) visibility vs. syndrome readout bridge.

Resolves what happens when a CNOT compression gate CNOT_{0->1} is applied to two DCP
wires rho(theta_0, gamma) \otimes rho(theta_1, gamma), the survivor wire 0 is probed
in the Pauli-X_0 basis (or rotated by exp(-i * alpha * X_0)), and the syndrome wire 1
is UNCOMPUTED via CNOT_{0->1}^dagger without classical syndrome measurement:

1. Exact Heisenberg Operator Conjugation Law:
   Because CNOT_{0->1}^dagger (X_0 \otimes I_1) CNOT_{0->1} = X_0 \otimes X_1, measuring
   the survivor wire observable X_0 after CNOT_{0->1} WITHOUT conditioning on the
   syndrome wire Z_1 outcome (or after uncomputing CNOT_{0->1}^dagger and tracing out wire 1)
   is unitarily identical to measuring the 2-qubit parity observable X_0 \otimes X_1 on
   the input product state:
       <X_0>_{uncomputed} = Tr( (X_0 \otimes I_1) CNOT_{0->1} (rho_0 \otimes rho_1) CNOT_{0->1}^dagger )
                          = Tr( (X_0 \otimes X_1) (rho_0 \otimes rho_1) )
                          = gamma^2 * cos(theta_0) * cos(theta_1)
                          = 0.5 * gamma^2 * ( cos(theta_0 + theta_1) + cos(theta_0 - theta_1) )!

2. 50/50 Sum-Difference Interferometric Mixing Penalty vs. Syndrome-Conditioned Readout:
   Suppose wire 0 and wire 1 form a mod-q zero-sum witness pair (theta_0 + theta_1 == 0 mod 2*pi,
   so cos(theta_0 + theta_1) = 1.0):
   - Syndrome-Conditioned Readout (measuring Z_1 = d_1 in {0, 1}):
     On the d_1 = 0 branch (probability 1/2), the conditional state has exact phase
     theta_0 + theta_1 == 0 and full coherence:
         <X_0 | d_1 = 0> = gamma^2 * cos(theta_0 + theta_1) = gamma^2,
     independent of the difference angle theta_0 - theta_1 = 2 * theta_0!
   - Uncomputed / Unmeasured Syndrome Echo:
     Because uncomputing or ignoring wire 1 averages the d_1 = 0 (sum) and d_1 = 1
     (difference) branches 50/50, the uncomputed expectation:
         <X_0>_{uncomputed} = 0.5 * gamma^2 * (1 + cos(2 * theta_0)) = gamma^2 * cos^2(theta_0)
     suffers a complete destructive interference blind spot (<X_0>_{uncomputed} = 0!)
     whenever theta_0 == +/- pi/2 (mod 2*pi), and averages only 0.5 * gamma^2 over uniform
     theta_0!
"""

from __future__ import annotations

import cmath
import hashlib
import json
import math
from typing import Any, Dict, List


THEOREM_ID = "dcp_coherent_cnot_uncomputation_echo_loschmidt_visibility_bridge"
SCHEMA_VERSION = "dcp-coherent-cnot-uncomputation-echo-loschmidt-visibility-bridge-v1"


def evaluate_cnot_uncomputation_echo_vs_syndrome_readout(
    theta_0_values: List[float],
    gamma: float = 0.9,
) -> Dict[str, Any]:
    """Compare explicit 4x4 density matrix expectations for syndrome-conditioned d_1=0 vs uncomputed CNOT echo."""
    records: List[Dict[str, Any]] = []

    for theta0 in theta_0_values:
        # Zero-sum witness pair: theta_1 = -theta_0 (mod 2*pi) so theta_0 + theta_1 = 0!
        theta1 = -theta0

        def _rho1(th: float) -> List[List[complex]]:
            return [
                [0.5 + 0j, 0.5 * gamma * cmath.exp(-1j * th)],
                [0.5 * gamma * cmath.exp(1j * th), 0.5 + 0j],
            ]

        r0 = _rho1(theta0)
        r1 = _rho1(theta1)

        rho_in = [[0j] * 4 for _ in range(4)]
        for i0 in range(2):
            for j0 in range(2):
                for i1 in range(2):
                    for j1 in range(2):
                        rho_in[2 * i0 + i1][2 * j0 + j1] = r0[i0][j0] * r1[i1][j1]

        # Apply CNOT_{0->1}: permutes |10> (2) <-> |11> (3)
        perm = [0, 1, 3, 2]
        rho_cnot = [[rho_in[perm[r]][perm[c]] for c in range(4)] for r in range(4)]

        # 1. Syndrome-conditioned d_1 = 0 branch (indices 0 and 2):
        prob_d0 = (rho_cnot[0][0] + rho_cnot[2][2]).real
        x0_given_d0 = 2.0 * (rho_cnot[0][2] / prob_d0).real

        # 2. Syndrome-conditioned d_1 = 1 branch (indices 1 and 3):
        prob_d1 = (rho_cnot[1][1] + rho_cnot[3][3]).real
        x0_given_d1 = 2.0 * (rho_cnot[1][3] / prob_d1).real

        # 3. Uncomputed / unmeasured marginal Tr_1(rho_cnot) on wire 0:
        rho_surv_01 = rho_cnot[0][2] + rho_cnot[1][3]
        x0_uncomputed_exp = 2.0 * rho_surv_01.real
        x0_uncomputed_closed = (gamma ** 2) * (math.cos(theta0) ** 2)

        records.append({
            "theta_0": theta0,
            "prob_d0": prob_d0,
            "x0_expectation_given_d0_zero_sum": x0_given_d0,
            "x0_expectation_given_d1_diff": x0_given_d1,
            "x0_expectation_uncomputed_explicit": x0_uncomputed_exp,
            "x0_expectation_uncomputed_closed_form": x0_uncomputed_closed,
            "exact_laws_verified": (
                abs(prob_d0 - 0.5) < 1e-12
                and abs(x0_given_d0 - (gamma ** 2)) < 1e-12
                and abs(x0_given_d1 - (gamma ** 2) * math.cos(2.0 * theta0)) < 1e-12
                and abs(x0_uncomputed_exp - x0_uncomputed_closed) < 1e-12
            ),
        })

    return {
        "gamma": gamma,
        "records": records,
        "all_verified": all(r["exact_laws_verified"] for r in records),
    }


def generate_dcp_coherent_cnot_uncomputation_echo_loschmidt_visibility_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the coherent CNOT uncomputation echo bridge."""
    sweep = evaluate_cnot_uncomputation_echo_vs_syndrome_readout(
        theta_0_values=[0.0, math.pi / 4.0, math.pi / 2.0, 3.0 * math.pi / 4.0],
        gamma=0.9,
    )

    rec_pi_over_2 = sweep["records"][2]  # theta_0 = pi/2 -> uncomputed echo vanishes to 0.0, while d_1=0 keeps +gamma^2 = 0.81!
    all_passed = (
        sweep["all_verified"]
        and abs(rec_pi_over_2["x0_expectation_uncomputed_explicit"]) < 1e-12
        and abs(rec_pi_over_2["x0_expectation_given_d0_zero_sum"] - 0.81) < 1e-12
    )

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "proof_status": "LOCAL_DERIVATION_REVIEW_PENDING_NOT_FORMALLY_VERIFIED",
        "scope_constraints": {
            "applies_to": "Coherent CNOT uncomputation echo CNOT^dagger (X_0 otimes I_1) CNOT = X_0 otimes X_1 vs. classical syndrome readout on DCP pairs",
            "does_not_claim": "Loss of coherence when the syndrome wire is measured in the Z basis or used for conditional Pauli-frame routing",
            "controls_included": "Evaluates theta_0 in {0, pi/4, pi/2, 3*pi/4} on a zero-sum pair theta_0 + theta_1 = 0, verifying constant d_1=0 expectation +gamma^2=0.81 vs complete destructive cancellation (<X_0>=0) of uncomputed echo at theta_0=pi/2.",
        },
        "echo_vs_readout_sweep": sweep,
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
