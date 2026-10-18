r"""DCP post-selected weak-value phase amplification vs. total Fisher information conservation obstruction.

Resolves whether post-selecting a weakly coupled ancilla / pointer onto a nearly
orthogonal state |phi_post(eps)> (weak-value amplification) can reduce total quantum
query complexity for detecting or estimating a small DCP phase shift theta = 2*pi*a*s/q:

1. Exact Physical 3-Outcome Post-Selected Interferometer POVM:
   On the single-qubit DCP state rho(theta, gamma) = 0.5 * (I + gamma * (cos(theta) X + sin(theta) Y)),
   consider the trace-preserving 3-outcome weak-value POVM {E_+(eps), E_-(eps), E_R(eps)}
   parameterized by post-selection angle eps in (0, pi/2]:
       E_+(eps) = sin^2(eps) |+i><+i| + 0.5 * cos^2(eps) |-><-|,
       E_-(eps) = sin^2(eps) |-i><-i| + 0.5 * cos^2(eps) |-><-|,
       E_R(eps) = cos^2(eps) |+><+|,
   with E_+(eps) + E_-(eps) + E_R(eps) = I_2 and exact outcome probabilities:
       p_+(theta, eps) = 0.5 * sin^2(eps) * (1 + gamma * sin(theta)) + 0.25 * cos^2(eps) * (1 - gamma * cos(theta)),
       p_-(theta, eps) = 0.5 * sin^2(eps) * (1 - gamma * sin(theta)) + 0.25 * cos^2(eps) * (1 - gamma * cos(theta)),
       p_R(theta, eps) = 0.5 * cos^2(eps) * (1 + gamma * cos(theta)).
   Conditioned on acceptance (outcomes A_+ or A_-, total probability p_acc = 1 - p_R),
   for a pure state (gamma = 1) or near-pure state at small eps, the conditional contrast
   is amplified while the acceptance probability drops as O(eps^2 + theta^2).

2. Exact Total Classical Fisher Information Conservation Identity:
   By the chain rule of classical Fisher information:
       I_total(theta; eps) = p_acc(theta; eps) * I_cond(theta | Accept) + I_binary(Accept vs Reject)
                          <= I_Q(rho(theta, gamma)) = gamma^2.
   Consequently, the net per-prepared-copy Fisher information from the post-selected
   sub-ensemble p_acc * I_cond(theta | Accept) NEVER exceeds the non-post-selected
   optimal readout (eps = pi/2, where p_R = 0 and I_net(theta=0) == gamma^2).
"""

from __future__ import annotations

import hashlib
import json
import math
from typing import Any, Dict, List


THEOREM_ID = "dcp_post_selected_weak_value_phase_amplification_obstruction"
SCHEMA_VERSION = "dcp-post-selected-weak-value-phase-amplification-obstruction-v1"


def evaluate_weak_value_post_selection_fisher_budget(
    theta: float,
    gamma: float,
    eps_values: List[float],
) -> Dict[str, Any]:
    """Compare conditional Fisher info, acceptance probability, and net per-copy Fisher info across post-selection angles eps."""
    qfi_bound = gamma ** 2
    records: List[Dict[str, Any]] = []

    for eps in eps_values:
        s_sq = math.sin(eps) ** 2
        c_sq = math.cos(eps) ** 2
        ct = math.cos(theta)
        st = math.sin(theta)

        p_plus = 0.5 * s_sq * (1.0 + gamma * st) + 0.25 * c_sq * (1.0 - gamma * ct)
        p_minus = 0.5 * s_sq * (1.0 - gamma * st) + 0.25 * c_sq * (1.0 - gamma * ct)
        p_acc = p_plus + p_minus
        p_rej = 0.5 * c_sq * (1.0 + gamma * ct)

        dp_plus = 0.5 * s_sq * gamma * ct + 0.25 * c_sq * gamma * st
        dp_minus = -0.5 * s_sq * gamma * ct + 0.25 * c_sq * gamma * st
        dp_acc = dp_plus + dp_minus
        dp_rej = -0.5 * c_sq * gamma * st

        q_plus = p_plus / p_acc
        q_minus = p_minus / p_acc
        dq_plus = (dp_plus * p_acc - p_plus * dp_acc) / (p_acc ** 2)
        dq_minus = -dq_plus

        i_cond_given_acc = (dq_plus ** 2) / q_plus + (dq_minus ** 2) / q_minus
        i_net_post_only = p_acc * i_cond_given_acc
        i_binary_acc_rej = ((dp_acc ** 2) / p_acc + (dp_rej ** 2) / p_rej) if p_rej > 1e-15 else 0.0
        i_total_3outcome = (dp_plus ** 2) / p_plus + (dp_minus ** 2) / p_minus + ((dp_rej ** 2) / p_rej if p_rej > 1e-15 else 0.0)

        cond_contrast = abs(q_plus - q_minus)
        chain_rule_err = abs((i_net_post_only + i_binary_acc_rej) - i_total_3outcome)

        records.append({
            "eps": eps,
            "p_accept": p_acc,
            "p_reject": p_rej,
            "conditional_contrast_on_accepted": cond_contrast,
            "conditional_fisher_info_given_accept": i_cond_given_acc,
            "net_per_copy_post_selected_fisher_info": i_net_post_only,
            "discarded_accept_reject_fisher_info": i_binary_acc_rej,
            "total_3outcome_fisher_info": i_total_3outcome,
            "quantum_fisher_info_bound": qfi_bound,
            "chain_rule_error": chain_rule_err,
            "exact_conservation_verified": (
                abs((p_acc + p_rej) - 1.0) < 1e-12
                and chain_rule_err < 1e-12
                and i_net_post_only <= i_total_3outcome + 1e-12
                and i_total_3outcome <= qfi_bound + 1e-12
            ),
        })

    return {
        "theta": theta,
        "gamma": gamma,
        "quantum_fisher_info_bound": qfi_bound,
        "records": records,
        "all_verified": all(r["exact_conservation_verified"] for r in records),
    }


def generate_dcp_post_selected_weak_value_phase_amplification_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the weak-value post-selection Fisher conservation obstruction."""
    audit = evaluate_weak_value_post_selection_fisher_budget(
        theta=0.05,
        gamma=0.95,
        eps_values=[0.05, 0.15, 0.30, 0.60, math.pi / 2.0],
    )

    rec_weak = audit["records"][0]
    rec_full = audit["records"][-1]

    all_passed = (
        audit["all_verified"]
        and rec_weak["net_per_copy_post_selected_fisher_info"] < rec_full["net_per_copy_post_selected_fisher_info"]
        and abs(rec_full["p_accept"] - 1.0) < 1e-12
    )

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "proof_status": "LOCAL_DERIVATION_REVIEW_PENDING_NOT_FORMALLY_VERIFIED",
        "scope_constraints": {
            "applies_to": "Post-selected weak-value phase amplification vs. total per-copy classical and quantum Fisher information on DCP states",
            "does_not_claim": "Absence of technical-noise / detector-saturation advantages when pointer readout is limited by classical detector dynamic range",
            "controls_included": "Compares weak post-selection angles eps in {0.05, 0.15, 0.30, 0.60} against full non-post-selected readout eps=pi/2 (p_accept = 1.0), verifying exact Fisher chain-rule conservation and I_net <= I_total <= QFI = gamma^2.",
        },
        "weak_value_fisher_audit": audit,
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
