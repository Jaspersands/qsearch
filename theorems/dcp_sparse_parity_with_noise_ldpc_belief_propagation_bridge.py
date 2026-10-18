r"""DCP sparse parity-with-noise LDPC hyperbolic-tangent belief propagation bridge.

Establishes the exact hyperbolic-tangent log-likelihood ratio (LLR) algebra and MAP bit
error reduction when CNOT kernel elimination produces an overcomplete system of noisy
parity checks <v_j, s mod 2> == b_j (mod 2) on the secret LSB vector z = s mod 2 in {0, 1}^n:

1. Exact Hyperbolic-Tangent Reliability Product Law for Noisy Parity Checks:
   Suppose a binary parity check c = z_{i_1} (+) ... (+) z_{i_d} is measured via a
   weight-h CNOT tree with measurement bias gamma_c = 1 - 2 * eps_c in (0, 1), and each
   participating variable z_{i_r} has independent prior bias gamma_{i_r} = tanh(LLR_{i_r} / 2).
   Then the extrinsic message sent from check c to target bit z_{i_1} has exact effective
   bias equal to the product of the check reliability and the partner variable biases:
       gamma_{c -> i_1} = gamma_c * prod_{r=2}^d gamma_{i_r},
   corresponding to the exact belief-propagation check-to-variable LLR update:
       LLR_{c -> i_1} = 2 * atanh( gamma_c * prod_{r=2}^d tanh(LLR_{i_r} / 2) ).

2. Exact Additive LLR Pooling Across L Disjoint Auxiliaries (Tree-Graph Exactness):
   When target bit z_0 in {0, 1} is observed both directly with bias gamma_0 (error rate
   eps_0 = (1 - gamma_0)/2) and via L disjoint weight-2 parity checks c_l = z_0 (+) z_l
   where each partner bit z_l has direct observation bias gamma_partner and each check
   has measurement bias gamma_check, the exact Bayesian posterior LLR on the star tree is:
       LLR_post(z_0) = 2 * atanh(gamma_0) + L * 2 * atanh(gamma_check * gamma_partner).
   This strictly matches the exact brute-force Bayes posterior across all 2^{2L+1} syndrome
   measurement configurations {y_0, (y_{l,partner}, y_{l,check})_{l=1}^L} in {-1, +1}^{2L+1},
   and strictly drives the MAP bit-error probability P_err^{MAP}(L) -> 0 exponentially in L!
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from typing import Any, Dict, List


THEOREM_ID = "dcp_sparse_parity_with_noise_ldpc_belief_propagation_bridge"
SCHEMA_VERSION = "dcp-sparse-parity-with-noise-ldpc-belief-propagation-bridge-v1"


def _bias_to_llr(gamma: float) -> float:
    return 2.0 * math.atanh(gamma)


def evaluate_ldpc_star_check_belief_propagation(
    gamma_direct: float,
    gamma_partner: float,
    gamma_check: float,
    l_checks: int,
) -> Dict[str, Any]:
    """Compare closed-form tanh/atanh BP LLR pooling against exact brute-force Bayes over 2^{2L+1} outcomes."""
    if not (0.0 < gamma_direct < 1.0 and 0.0 < gamma_partner < 1.0 and 0.0 < gamma_check < 1.0):
        raise ValueError("biases must be in (0, 1)")
    if type(l_checks) is not int or l_checks < 0 or l_checks > 6:
        raise ValueError("l_checks must be an integer in [0, 6]")

    llr_direct = _bias_to_llr(gamma_direct)
    gamma_extrinsic_single = gamma_check * gamma_partner
    llr_extrinsic_single = _bias_to_llr(gamma_extrinsic_single)

    # Enumerate all 2^{2L + 1} observation tuples (y_0, y_{p,1}, y_{c,1}, ..., y_{p,L}, y_{c,L}) in {-1, +1}^{2L+1}
    # under true secret z_0 = +1 (bit 0) and marginalize over uniform partner bits z_1, ..., z_L in {-1, +1}^L:
    p_0_pos = 0.5 * (1.0 + gamma_direct)
    p_0_neg = 0.5 * (1.0 - gamma_direct)
    # Under uniform partner z_l in {-1, +1}, the composite auxiliary observation u_l = y_{p,l} * y_{c,l} in {-1, +1}
    # equals +1 (agreeing with z_0 = +1) with probability:
    # P(u_l = +1 | z_0 = +1) = (1 + gamma_partner * gamma_check) / 2!
    # Let's verify this both by explicit marginalization over z_l in {-1, +1} AND by full 2^{2L+1} enumeration!
    num_obs_vars = 2 * l_checks + 1
    max_llr_diff = 0.0
    map_error_prob = 0.0
    total_prob_check = 0.0

    for obs in itertools.product((-1, 1), repeat=num_obs_vars):
        y0 = obs[0]
        # Closed-form BP posterior LLR:
        llr_bp = y0 * llr_direct
        for l_idx in range(l_checks):
            yp = obs[1 + 2 * l_idx]
            yc = obs[1 + 2 * l_idx + 1]
            llr_bp += (yp * yc) * llr_extrinsic_single

        # Exact brute-force Bayes likelihood P(obs | z_0 = +1) and P(obs | z_0 = -1)
        # marginalizing over all 2^L partner assignments z_1..z_L in {-1, +1}^L:
        prob_given_plus = (p_0_pos if y0 == 1 else p_0_neg)
        prob_given_minus = (p_0_neg if y0 == 1 else p_0_pos)

        for l_idx in range(l_checks):
            yp = obs[1 + 2 * l_idx]
            yc = obs[1 + 2 * l_idx + 1]
            # Marginalize over z_l in {-1, +1} with prior 1/2 each:
            acc_plus = 0.0
            acc_minus = 0.0
            for zl in (-1, 1):
                p_yp = 0.5 * (1.0 + gamma_partner * zl * yp)
                p_yc_plus = 0.5 * (1.0 + gamma_check * (+1 * zl) * yc)
                p_yc_minus = 0.5 * (1.0 + gamma_check * (-1 * zl) * yc)
                acc_plus += 0.5 * p_yp * p_yc_plus
                acc_minus += 0.5 * p_yp * p_yc_minus
            prob_given_plus *= acc_plus
            prob_given_minus *= acc_minus

        llr_bayes = math.log(prob_given_plus / prob_given_minus)
        max_llr_diff = max(max_llr_diff, abs(llr_bp - llr_bayes))
        total_prob_check += prob_given_plus

        # MAP decoder under z_0 = +1 errs when llr_bp < 0 (or 0.5 when llr_bp == 0)
        if abs(llr_bp) < 1e-12:
            map_error_prob += 0.5 * prob_given_plus
        elif llr_bp < 0.0:
            map_error_prob += prob_given_plus

    direct_error_prob = 0.5 * (1.0 - gamma_direct)

    return {
        "L_auxiliary_checks": l_checks,
        "gamma_direct": gamma_direct,
        "gamma_partner": gamma_partner,
        "gamma_check": gamma_check,
        "single_check_extrinsic_bias": gamma_extrinsic_single,
        "single_check_extrinsic_llr": llr_extrinsic_single,
        "direct_only_error_prob": direct_error_prob,
        "bp_map_error_prob": map_error_prob,
        "max_bp_vs_exact_bayes_llr_error": max_llr_diff,
        "total_probability_sum": total_prob_check,
        "exact_bp_bayes_equivalence_verified": (
            max_llr_diff < 1e-12
            and abs(total_prob_check - 1.0) < 1e-12
            and (map_error_prob <= direct_error_prob + 1e-12)
        ),
    }


def generate_dcp_sparse_parity_with_noise_ldpc_belief_propagation_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the sparse parity-with-noise LDPC belief propagation bridge."""
    sweep = [
        evaluate_ldpc_star_check_belief_propagation(
            gamma_direct=0.5,
            gamma_partner=0.7,
            gamma_check=0.7,
            l_checks=l_val,
        )
        for l_val in (0, 1, 2, 3, 4)
    ]

    monotone_error_drop = (
        abs(sweep[0]["bp_map_error_prob"] - 0.25) < 1e-12
        and sweep[2]["bp_map_error_prob"] < sweep[0]["bp_map_error_prob"]
        and sweep[4]["bp_map_error_prob"] < sweep[2]["bp_map_error_prob"]
    )
    all_passed = all(r["exact_bp_bayes_equivalence_verified"] for r in sweep) and monotone_error_drop

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "proof_status": "LOCAL_DERIVATION_REVIEW_PENDING_NOT_FORMALLY_VERIFIED",
        "scope_constraints": {
            "applies_to": "Exact hyperbolic-tangent LLR belief propagation and MAP bit-error suppression on tree-structured noisy CNOT parity checks",
            "does_not_claim": "Exact Bayes optimality of loopy belief propagation on short-cycle check graphs without girth control",
            "controls_included": "Evaluates L = 0, 1, 2, 3, 4 auxiliary checks at gamma_0 = 0.5 (direct error 0.25) and gamma_partner = gamma_check = 0.7 (extrinsic bias 0.49), verifying < 1e-12 LLR error vs brute-force 2^L marginalization.",
        },
        "ldpc_star_check_sweep": sweep,
        "monotone_map_error_reduction_verified": monotone_error_drop,
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
