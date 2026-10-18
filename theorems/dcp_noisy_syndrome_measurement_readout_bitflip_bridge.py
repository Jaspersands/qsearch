r"""DCP noisy syndrome measurement readout bit-flip and parity-check post-selection bridge.

Quantifies the exact impact of classical syndrome measurement readout bit-flip errors
(with independent bit-flip probability eta in [0, 1/2]) on CNOT witness compression
and sign-flip Pauli-frame routing (Subsystems 51, 65, 77, 78), and establishes the
exact O(eta^2) error suppression of redundant parity-check syndrome verification:

1. Exact Readout Bit-Flip Mixing on Weight-2 CNOT Pairs:
   In a weight-2 CNOT pair (u_0 = x_0, d_1 = x_0 (+) x_1) on equal columns A_{.,0} = A_{.,1} = a:
   - True syndrome d_1 = 0 (prob 1/2) prepares the clean zero-sum state rho(0) = |+><+|.
   - True syndrome d_1 = 1 (prob 1/2) prepares the odd-branch state with phase +/- 2a.
   When classical readout of d_1 suffers bit-flip error eta in [0, 1/2], conditioned on
   observing d_obs = 0 (or d_obs = 1), the post-measurement state is a convex mixture of
   weight (1 - eta) of the true branch and weight eta of the opposite branch.

2. Exact Readout Damping Law for Stage-2 Sign-Flip Pauli-Frame Routing:
   In two-stage sign-flip routing (Subsystem 78), where two pairs both report observed
   syndrome d_{1,obs} = d_{2,obs} = 1 (or where each pair applies X^{d_{m,obs}} to rectify
   random signs z_m in {+a, -a} mod q so that z_m = (-1)^{d_{m,true}} a), a readout error
   flips d_{m,obs} != d_{m,true} with probability eta, inverting the Pauli-X frame!
   Consequently:
   - For a single sign-rectified pair, the effective phase-coherence factor is damped by:
         gamma_eff(eta) = (1 - 2*eta) * gamma.
   - Across two sign-rectified pairs combined in a Stage-2 CNOT, the probability that both
     frames match (so Stage-2 d_2 = 0 eliminates the residue) is:
         P_aligned(eta) = (1 - eta)^2 + eta^2 = 0.5 * (1 + (1 - 2*eta)^2),
     and the net parity coherence visibility scales as (1 - 2*eta)^2.

3. Exact O(eta^2) Suppression via 1-Ancilla Parity-Check Readout Verification:
   If a syndrome bit d_1 is copied to one verification ancilla d_1' = d_1 prior to readout
   (a 2-readout repetition check with independent readout error eta on both measurements),
   post-selecting on agreement (d_{1,obs} == d_{1,obs}') succeeds with probability
   P_accept = (1 - eta)^2 + eta^2 and reduces the effective syndrome error rate to:
       eta_post(eta) = eta^2 / ((1 - eta)^2 + eta^2),
   boosting single-pair coherence from (1 - 2*eta) to:
       1 - 2 * eta_post(eta) = (1 - 2*eta) / ((1 - eta)^2 + eta^2).
"""

from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, List


THEOREM_ID = "dcp_noisy_syndrome_measurement_readout_bitflip_bridge"
SCHEMA_VERSION = "dcp-noisy-syndrome-measurement-readout-bitflip-bridge-v1"


def evaluate_syndrome_readout_bitflip_and_parity_verification(
    eta_values: List[float],
    gamma: float = 0.9,
) -> Dict[str, Any]:
    """Evaluate exact unverified vs parity-verified readout damping across error rates eta."""
    records: List[Dict[str, Any]] = []
    for eta in eta_values:
        if not (0.0 <= eta <= 0.5):
            raise ValueError("eta must be in [0, 0.5]")

        # Explicit 4-outcome probabilities over (e_1, e_2) in {0,1}^2 for two pairs:
        p00 = (1.0 - eta) ** 2
        p01 = (1.0 - eta) * eta
        p10 = eta * (1.0 - eta)
        p11 = eta ** 2

        # Single-pair effective visibility after X^{d_obs} sign rectification:
        # True state has sign (-1)^{d_true}; applying X^{d_obs} leaves sign (-1)^{d_true (+) d_obs} = (-1)^e
        single_pair_vis_explicit = ((1.0 - eta) * (+1.0) + eta * (-1.0)) * gamma
        single_pair_vis_closed = (1.0 - 2.0 * eta) * gamma

        # Two-pair Stage-2 alignment probability (both errors e_1 == e_2 so relative sign is +1):
        two_pair_align_prob_explicit = p00 + p11
        two_pair_align_prob_closed = 0.5 * (1.0 + (1.0 - 2.0 * eta) ** 2)
        two_pair_net_vis_explicit = ((p00 + p11) * (+1.0) + (p01 + p10) * (-1.0)) * (gamma ** 2)
        two_pair_net_vis_closed = ((1.0 - 2.0 * eta) ** 2) * (gamma ** 2)

        # 2-readout parity-check post-selection on each syndrome:
        p_accept_single = (1.0 - eta) ** 2 + (eta ** 2)
        eta_post = (eta ** 2) / p_accept_single
        single_pair_vis_verified = (1.0 - 2.0 * eta_post) * gamma
        two_pair_net_vis_verified = ((1.0 - 2.0 * eta_post) ** 2) * (gamma ** 2)

        err_reduction_factor = (eta / eta_post) if eta_post > 0.0 else float("inf")

        records.append({
            "eta": eta,
            "single_pair_visibility_unverified": single_pair_vis_closed,
            "two_pair_alignment_prob_unverified": two_pair_align_prob_closed,
            "two_pair_net_visibility_unverified": two_pair_net_vis_closed,
            "parity_check_accept_prob_per_syndrome": p_accept_single,
            "eta_post_selected": eta_post,
            "error_rate_reduction_factor": err_reduction_factor if eta > 0 else 1.0,
            "single_pair_visibility_verified": single_pair_vis_verified,
            "two_pair_net_visibility_verified": two_pair_net_vis_verified,
            "exact_identities_verified": (
                abs(single_pair_vis_explicit - single_pair_vis_closed) < 1e-12
                and abs(two_pair_align_prob_explicit - two_pair_align_prob_closed) < 1e-12
                and abs(two_pair_net_vis_explicit - two_pair_net_vis_closed) < 1e-12
                and (eta_post < eta if 0.0 < eta < 0.5 else abs(eta_post - eta) < 1e-12)
            ),
        })

    return {
        "gamma": gamma,
        "records": records,
        "all_verified": all(r["exact_identities_verified"] for r in records),
    }


def generate_dcp_noisy_syndrome_measurement_readout_bitflip_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the noisy syndrome readout bit-flip bridge."""
    sweep = evaluate_syndrome_readout_bitflip_and_parity_verification(
        eta_values=[0.0, 0.01, 0.05, 0.10, 0.25, 0.50],
        gamma=0.9,
    )

    rec_05 = next(r for r in sweep["records"] if abs(r["eta"] - 0.05) < 1e-12)
    rec_50 = next(r for r in sweep["records"] if abs(r["eta"] - 0.50) < 1e-12)

    all_passed = (
        sweep["all_verified"]
        and abs(rec_05["eta_post_selected"] - (0.0025 / 0.905)) < 1e-12
        and rec_05["error_rate_reduction_factor"] > 18.0
        and abs(rec_50["single_pair_visibility_unverified"]) < 1e-12
    )

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "proof_status": "LOCAL_DERIVATION_REVIEW_PENDING_NOT_FORMALLY_VERIFIED",
        "scope_constraints": {
            "applies_to": "Classical syndrome measurement readout bit-flip damping (1-2*eta)^2 and 2-readout parity-check O(eta^2) suppression",
            "does_not_claim": "Protection against coherent phase errors on the unmeasured survivor wire prior to the CNOT gate",
            "controls_included": "Includes noiseless eta=0.0 control, realistic eta=0.05 readout error (18.1x suppression to eta_post = 0.002762), and maximal-noise eta=0.50 erasure control (visibility = 0.0).",
        },
        "readout_error_sweep": sweep,
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
