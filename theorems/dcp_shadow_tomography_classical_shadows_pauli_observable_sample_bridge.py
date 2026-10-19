r"""DCP Classical Shadows randomized Pauli tomography vs. commuting X^K witness derandomization bridge.

Establishes the exact 3^w single-snapshot variance law of Huang-Kueng-Preskill randomized
Pauli Classical Shadows for estimating M candidate weight-w DCP witness parity observables
O_m = \bigotimes_{r in S_m} X_r (|S_m| = w), and proves that derandomizing into the
single commuting basis X^{\otimes K} achieves an exact 3^w-fold reduction in sample
variance (and Simultaneous estimation of all 2^K - 1 X-parities from every shot!):

1. Exact 3^w Shadow Norm Variance Law of Randomized Pauli Tomography:
   In standard single-qubit Pauli shadow tomography on K qubits, each qubit r in {0, ..., K-1}
   is measured independently in a uniformly random basis B_r in {X, Y, Z} (probability 1/3 each)
   with outcome b_r in {-1, +1}.
   For any weight-w Pauli observable O_m = \bigotimes_{r in S_m} X_r (|S_m| = w), the
   unbiased single-snapshot classical shadow estimator is:
       o_hat_m = 3^w * prod_{r in S_m} b_r   if B_r == X for all r in S_m (prob 3^{-w}),
       o_hat_m = 0                           otherwise (prob 1 - 3^{-w}).
   Because E[o_hat_m] = 3^w * 3^{-w} * <O_m> = <O_m> and E[o_hat_m^2] = (3^w)^2 * 3^{-w} * 1 = 3^w,
   the exact single-snapshot estimator variance is:
       Var_{shadow}[o_hat_m] = 3^w - <O_m>^2!

2. Exact 3^w Sample Savings via Commuting X^{\otimes K} Derandomization:
   Because all M candidate witness parity observables {O_m = \bigotimes_{r in S_m} X_r}
   belong to the commuting abelian group {I, X}^{\otimes K} ([O_m, O_{m'}] == 0 for all m, m'),
   measuring EVERY qubit deterministically in the Pauli-X basis (hit probability 1.0 for
   ALL 2^K - 1 X-parities simultaneously!) yields the direct parity estimator
   o_tilde_m = prod_{r in S_m} b_r in {-1, +1} with exact variance:
       Var_{derand}[o_tilde_m] = 1 - <O_m>^2,
   achieving an exact variance / sample-complexity reduction factor of:
       Var_{shadow}[o_hat_m] / Var_{derand}[o_tilde_m] = (3^w - <O_m>^2) / (1 - <O_m>^2) >= 3^w!
"""

from __future__ import annotations

import hashlib
import itertools
import json
from typing import Any, Dict, List


THEOREM_ID = "dcp_shadow_tomography_classical_shadows_pauli_observable_sample_bridge"
SCHEMA_VERSION = "dcp-shadow-tomography-classical-shadows-pauli-observable-sample-bridge-v1"


def evaluate_classical_shadows_vs_commuting_x_derandomization(
    w_weights: List[int],
    true_expectation_mu: float = 0.25,
) -> Dict[str, Any]:
    """Verify exact 3^w shadow estimator expectation and variance over all 3^w basis choices vs derandomized X^w readout."""
    records: List[Dict[str, Any]] = []

    for w in w_weights:
        if type(w) is not int or w < 1 or w > 6:
            raise ValueError("w must be an integer in [1, 6]")

        num_bases = 3 ** w
        hit_prob = 1.0 / float(num_bases)

        # Conditional on hitting the all-X basis (1 of the 3^w basis strings), the parity product P in {-1, +1}
        # has P(+1) = (1 + mu)/2 and P(-1) = (1 - mu)/2:
        p_plus = 0.5 * (1.0 + true_expectation_mu)
        p_minus = 0.5 * (1.0 - true_expectation_mu)

        # Explicit enumeration over all 3^w Pauli basis strings B in {0(X), 1(Y), 2(Z)}^w:
        mean_shadow = 0.0
        second_moment_shadow = 0.0
        for basis_tuple in itertools.product((0, 1, 2), repeat=w):
            is_all_x = all(b == 0 for b in basis_tuple)
            if is_all_x:
                val_pos = float(num_bases) * (+1.0)
                val_neg = float(num_bases) * (-1.0)
                mean_shadow += hit_prob * (p_plus * val_pos + p_minus * val_neg)
                second_moment_shadow += hit_prob * (p_plus * (val_pos ** 2) + p_minus * (val_neg ** 2))

        var_shadow_explicit = second_moment_shadow - (mean_shadow ** 2)
        var_shadow_closed = float(3 ** w) - (true_expectation_mu ** 2)

        # Derandomized X^{\otimes w} estimator: hits with probability 1.0!
        var_derand = 1.0 - (true_expectation_mu ** 2)
        variance_ratio = var_shadow_explicit / var_derand

        records.append({
            "weight_w": w,
            "true_expectation_mu": true_expectation_mu,
            "shadow_hit_probability_3_pow_minus_w": hit_prob,
            "shadow_mean_explicit": mean_shadow,
            "shadow_variance_explicit": var_shadow_explicit,
            "shadow_variance_closed_form": var_shadow_closed,
            "derandomized_x_variance": var_derand,
            "sample_reduction_ratio_shadow_over_derand": variance_ratio,
            "zero_signal_baseline_3_pow_w": float(3 ** w),
            "exact_shadow_laws_verified": (
                abs(mean_shadow - true_expectation_mu) < 1e-12
                and abs(var_shadow_explicit - var_shadow_closed) < 1e-11
                and variance_ratio >= float(3 ** w) - 1e-12
            ),
        })

    return {
        "true_expectation_mu": true_expectation_mu,
        "records": records,
        "all_verified": all(r["exact_shadow_laws_verified"] for r in records),
    }


def generate_dcp_shadow_tomography_classical_shadows_pauli_observable_sample_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the Classical Shadows vs. commuting X^K derandomization bridge."""
    sweep = evaluate_classical_shadows_vs_commuting_x_derandomization(
        w_weights=[1, 2, 3, 4, 5],
        true_expectation_mu=0.25,
    )

    rec_w3 = sweep["records"][2]  # w = 3 -> >28.7x variance reduction (3^3 = 27 at mu=0)
    rec_w4 = sweep["records"][3]  # w = 4 -> >86.3x variance reduction (3^4 = 81 at mu=0)

    all_passed = (
        sweep["all_verified"]
        and rec_w3["sample_reduction_ratio_shadow_over_derand"] > 28.0
        and rec_w4["sample_reduction_ratio_shadow_over_derand"] > 86.0
    )

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "proof_status": "LOCAL_DERIVATION_REVIEW_PENDING_NOT_FORMALLY_VERIFIED",
        "scope_constraints": {
            "applies_to": "Randomized Pauli Classical Shadows 3^w variance vs. derandomized X^{otimes K} simultaneous readout for weight-w CNOT witness parities",
            "does_not_claim": "Simultaneous single-basis measurement of non-commuting X-type and Z-type observables",
            "controls_included": "Evaluates weights w in {1, 2, 3, 4, 5} over all 3^w basis strings, verifying exact unbiasedness E[o_hat] == mu, Var = 3^w - mu^2, and >86x sample savings at w = 4.",
        },
        "shadow_vs_derandomized_sweep": sweep,
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
