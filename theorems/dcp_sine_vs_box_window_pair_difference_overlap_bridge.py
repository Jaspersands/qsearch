r"""DCP discrete sine vs. flat box window shift-autocorrelation and quadratic dephasing bridge.

Establishes the exact closed-form position-shift autocorrelation (single-qubit coherence
visibility) gamma(Delta; P) = sum_{z=0}^{P - 1 - Delta} psi(z) psi(z + Delta) for the
discrete sine window psi_{sin}(z) = sqrt(2 / P) * sin(pi * (z + 1/2) / P) vs. the flat
box window psi_{box}(z) = 1 / sqrt(P) on z in {0, 1, ..., P - 1} (0 <= Delta <= P):

1. Exact Closed-Form Sine-Window Shift Autocorrelation Identity:
   For all integers P >= 2 and shifts 0 <= Delta <= P:
       gamma_{sin}(Delta; P) = (1 - Delta / P) * cos(pi * Delta / P)
                             + (1 / P) * (sin(pi * Delta / P) / sin(pi / P)),
   whereas the flat box window has linear autocorrelation:
       gamma_{box}(Delta; P) = 1 - Delta / P.

2. Exact Unit-Shift Identity & Quadratic Dephasing Loss O(1 / P^2):
   At unit shift Delta = 1, sin(pi * 1 / P) / sin(pi / P) == 1, yielding the exact identity:
       gamma_{sin}(1; P) = (1 - 1 / P) * cos(pi / P) + 1 / P,
   and exact unit-shift dephasing loss:
       1 - gamma_{sin}(1; P) = (1 - 1 / P) * (1 - cos(pi / P))
                             = 2 * (1 - 1 / P) * sin^2(pi / (2 * P)) ~ pi^2 / (2 * P^2).
   Thus the sine window reduces small-shift dephasing loss 1 - gamma(Delta; P) from
   FIRST-ORDER linear loss Delta / P (box window) to SECOND-ORDER quadratic loss
   O(Delta^2 / P^2) (e.g. > 6.69x smaller loss at P = 32, Delta = 1)!

3. Large-Shift Boundary Tapering Crossover (Delta -> P - 1 Countercontrol):
   Because the sine window tapers amplitudes near the boundaries z = 0 and z = P - 1,
   at extreme shifts near the window edge (Delta = P - 1), the box window retains
   larger overlap gamma_{box}(P - 1; P) = 1 / P > gamma_{sin}(P - 1; P) = (2 / P) * sin^2(pi / (2 * P)).
"""

from __future__ import annotations

import hashlib
import json
import math
from typing import Any, Dict, List


THEOREM_ID = "dcp_sine_vs_box_window_pair_difference_overlap_bridge"
SCHEMA_VERSION = "dcp-sine-vs-box-window-pair-difference-overlap-bridge-v1"


def sine_window_autocorrelation_explicit(delta_shift: int, p_window: int) -> float:
    """Compute sum_{z=0}^{P - 1 - Delta} psi_{sin}(z) * psi_{sin}(z + Delta) by explicit summation."""
    if type(p_window) is not int or p_window < 2:
        raise ValueError("p_window must be an integer >= 2")
    if type(delta_shift) is not int or not 0 <= delta_shift <= p_window:
        raise ValueError("delta_shift must satisfy 0 <= delta_shift <= p_window")
    acc = 0.0
    for z in range(p_window - delta_shift):
        s1 = math.sin(math.pi * (float(z) + 0.5) / float(p_window))
        s2 = math.sin(math.pi * (float(z + delta_shift) + 0.5) / float(p_window))
        acc += (2.0 / float(p_window)) * s1 * s2
    return acc


def sine_window_autocorrelation_closed_form(delta_shift: int, p_window: int) -> float:
    """Closed-form identity (1 - Delta/P)*cos(pi*Delta/P) + (1/P)*(sin(pi*Delta/P)/sin(pi/P))."""
    if type(p_window) is not int or p_window < 2:
        raise ValueError("p_window must be an integer >= 2")
    if type(delta_shift) is not int or not 0 <= delta_shift <= p_window:
        raise ValueError("delta_shift must satisfy 0 <= delta_shift <= p_window")
    frac = float(delta_shift) / float(p_window)
    angle = math.pi * frac
    sin_pi_p = math.sin(math.pi / float(p_window))
    return (1.0 - frac) * math.cos(angle) + (1.0 / float(p_window)) * (math.sin(angle) / sin_pi_p)


def verify_sine_vs_box_autocorrelation_and_crossover(p_window: int) -> Dict[str, Any]:
    """Verify closed-form autocorrelation across all Delta = 0..P, exact unit-shift identity, and large-Delta crossover."""
    if type(p_window) is not int or p_window < 4:
        raise ValueError("p_window >= 4 required for crossover audit")
    max_formula_err = 0.0
    for delta in range(p_window + 1):
        exp_val = sine_window_autocorrelation_explicit(delta, p_window)
        cf_val = sine_window_autocorrelation_closed_form(delta, p_window)
        max_formula_err = max(max_formula_err, abs(exp_val - cf_val))

    gamma_sin_1 = sine_window_autocorrelation_explicit(1, p_window)
    expected_sin_1 = (1.0 - 1.0 / float(p_window)) * math.cos(math.pi / float(p_window)) + (1.0 / float(p_window))
    gamma_box_1 = 1.0 - (1.0 / float(p_window))

    loss_sin_1 = 1.0 - gamma_sin_1
    loss_box_1 = 1.0 - gamma_box_1

    gamma_sin_edge = sine_window_autocorrelation_explicit(p_window - 1, p_window)
    gamma_box_edge = 1.0 / float(p_window)
    expected_sin_edge = (2.0 / float(p_window)) * (math.sin(math.pi / (2.0 * float(p_window))) ** 2)

    return {
        "P": p_window,
        "max_closed_form_error_all_deltas": max_formula_err,
        "delta_1_sine_visibility": gamma_sin_1,
        "delta_1_closed_form_visibility": expected_sin_1,
        "delta_1_box_visibility": gamma_box_1,
        "delta_1_sine_dephasing_loss": loss_sin_1,
        "delta_1_box_dephasing_loss": loss_box_1,
        "delta_1_loss_reduction_ratio_box_over_sine": loss_box_1 / loss_sin_1,
        "edge_delta_P_minus_1_sine_visibility": gamma_sin_edge,
        "edge_delta_P_minus_1_box_visibility": gamma_box_edge,
        "exact_identities_and_crossover_verified": (
            max_formula_err < 1e-12
            and abs(gamma_sin_1 - expected_sin_1) < 1e-12
            and gamma_sin_1 > gamma_box_1
            and abs(gamma_sin_edge - expected_sin_edge) < 1e-12
            and gamma_box_edge > gamma_sin_edge
        ),
    }


def generate_dcp_sine_vs_box_window_pair_difference_overlap_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the sine vs box window autocorrelation bridge."""
    audits = [
        verify_sine_vs_box_autocorrelation_and_crossover(p_window=8),
        verify_sine_vs_box_autocorrelation_and_crossover(p_window=16),
        verify_sine_vs_box_autocorrelation_and_crossover(p_window=32),
    ]

    all_passed = (
        all(a["exact_identities_and_crossover_verified"] for a in audits)
        and audits[2]["delta_1_loss_reduction_ratio_box_over_sine"] > 6.5
    )

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "proof_status": "LOCAL_DERIVATION_REVIEW_PENDING_NOT_FORMALLY_VERIFIED",
        "scope_constraints": {
            "applies_to": "Position-shift autocorrelation gamma(Delta; P) of discrete sine vs. flat box windows on {0, ..., P-1}",
            "does_not_claim": "Superiority of the sine window at extreme boundary shifts Delta -> P - 1",
            "controls_included": "Includes exact verification of gamma_{sin}(Delta; P) across all Delta = 0..P for P in {8, 16, 32}, exact unit-shift identity gamma_{sin}(1; P) == (1 - 1/P)*cos(pi/P) + 1/P (>6.69x smaller dephasing loss at P=32), and the Delta = P - 1 boundary crossover countercontrol.",
        },
        "window_overlap_audits": audits,
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
