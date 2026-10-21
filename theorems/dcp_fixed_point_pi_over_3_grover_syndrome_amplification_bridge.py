r"""DCP fixed-point pi/3 Grover syndrome amplification bridge.

Resolves the weight-2 (p_0 = 1/2) over-rotation barrier of standard pi-phase Grover
amplification (Subsystem 117) by applying Grover / Yoder-Low-Chuang pi/3 fixed-point
phase reflections:
    R_0(pi/3) = I - (1 - exp(i*pi/3)) |Psi_0><Psi_0|,
    R_chi(pi/3) = I - (1 - exp(i*pi/3)) Pi_marked:

1. Exact Cubic Failure-Rate Contraction Law (1 - P_1^{(pi/3)}(p_0) = (1 - p_0)^3):
   In the 2D invariant subspace spanned by the unmarked component |B> (weight 1 - p_0)
   and marked syndrome component |G> (weight p_0), let omega = exp(i * pi / 3), so
   1 - omega = exp(-i * pi / 3) and |1 - omega| = 1.
   Applying the single-step pi/3-reflection operator:
       A_{pi/3} = R_0(pi/3) * R_chi(pi/3)
   maps the unmarked state amplitude to:
       <B | A_{pi/3} | Psi_0> = sqrt(1 - p_0) * (1 - p_0 * (1 - omega)*(1 + omega))
                              = sqrt(1 - p_0) * (1 - p_0) = (1 - p_0)^{3/2},
   because (1 - omega) + (1 - omega) - (1 - omega)^2 = 1 for omega = exp(i*pi/3)
   (since omega^2 - omega + 1 = 0 is the 6th cyclotomic polynomial Phi_6(omega) = 0)!
   Squaring the unmarked amplitude yields the EXACT universal identity for ALL p_0 in [0, 1]:
       1 - P_1^{(pi/3)}(p_0) = (1 - p_0)^3,
       P_1^{(pi/3)}(p_0) = 1 - (1 - p_0)^3 = p_0 * (3 - 3*p_0 + p_0^2)!

2. Resolution of the Weight-2 CNOT Syndrome Branch (p_0 = 1/2 -> 7/8 -> 511/512):
   For a weight-2 CNOT witness pair where p_0 = 1/2 (and standard pi-Grover gives P_1 = 1/2):
   - 1-step pi/3 recursion (3 queries) boosts the target syndrome probability from
     1/2 = 50% to 1 - (1/2)^3 = 7/8 = 87.5%!
   - 2-level recursive pi/3 amplification (9 queries) cubes the failure rate again to
     (1/2)^9 = 1/512, achieving P_2^{(pi/3)}(1/2) = 511/512 = 99.8046875%!
"""

from __future__ import annotations

import cmath
import hashlib
import itertools
import json
import math
from typing import Any, Dict, List


THEOREM_ID = "dcp_fixed_point_pi_over_3_grover_syndrome_amplification_bridge"
SCHEMA_VERSION = "dcp-fixed-point-pi-over-3-grover-syndrome-amplification-bridge-v1"


def evaluate_pi_over_3_fixed_point_amplification(
    p0_values: List[float],
) -> Dict[str, Any]:
    """Verify the exact 2x2 unitary matrix action of R_0(pi/3)*R_chi(pi/3) and the cubic contraction law 1 - P_1 = (1 - p_0)^3."""
    omega = cmath.exp(1j * math.pi / 3.0)
    one_minus_omega = 1.0 - omega

    # Verify 6th cyclotomic polynomial identity omega^2 - omega + 1 == 0:
    cyclotomic_phi6_err = abs((omega ** 2) - omega + 1.0)

    records: List[Dict[str, Any]] = []
    for p0 in p0_values:
        if not (0.0 <= p0 <= 1.0):
            raise ValueError("p0 must be in [0, 1]")

        # In basis {|B> (unmarked), |G> (marked)}, |Psi_0> = [sqrt(1 - p0), sqrt(p0)]^T:
        b0 = math.sqrt(1.0 - p0)
        g0 = math.sqrt(p0)

        # Step 1: R_chi(pi/3) multiplies |G> by omega:
        v1_b = b0
        v1_g = omega * g0

        # Step 2: R_0(pi/3) = I - (1 - omega) |Psi_0><Psi_0|:
        ov = b0 * v1_b + g0 * v1_g
        v2_b = v1_b - one_minus_omega * ov * b0
        v2_g = v1_g - one_minus_omega * ov * g0

        p1_pi3_explicit = abs(v2_g) ** 2
        fail1_pi3_explicit = abs(v2_b) ** 2
        fail1_closed_form = (1.0 - p0) ** 3
        p1_pi3_closed_form = 1.0 - fail1_closed_form

        # Compare with 1-step standard pi-Grover: P_1^{(pi)}(p0) = p0 * (3 - 4*p0)^2
        p1_standard_pi = p0 * ((3.0 - 4.0 * p0) ** 2)

        # Level-2 recursive pi/3 amplification: failure is (1 - p1_pi3)^3 = (1 - p0)^9!
        p2_pi3_recursive = 1.0 - ((1.0 - p0) ** 9)

        records.append({
            "p0": p0,
            "p1_standard_pi_grover": p1_standard_pi,
            "p1_pi_over_3_explicit": p1_pi3_explicit,
            "p1_pi_over_3_closed_form": p1_pi3_closed_form,
            "failure_rate_1_minus_p1_explicit": fail1_pi3_explicit,
            "failure_rate_cubed_law": fail1_closed_form,
            "p2_recursive_pi_over_3": p2_pi3_recursive,
            "unitary_norm_check": p1_pi3_explicit + fail1_pi3_explicit,
            "exact_cubic_law_verified": (
                abs(p1_pi3_explicit - p1_pi3_closed_form) < 1e-12
                and abs(fail1_pi3_explicit - fail1_closed_form) < 1e-12
                and abs((p1_pi3_explicit + fail1_pi3_explicit) - 1.0) < 1e-12
            ),
        })

    return {
        "cyclotomic_phi6_error": cyclotomic_phi6_err,
        "records": records,
        "all_verified": (
            cyclotomic_phi6_err < 1e-12
            and all(r["exact_cubic_law_verified"] for r in records)
        ),
    }


def generate_dcp_fixed_point_pi_over_3_grover_syndrome_amplification_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the fixed-point pi/3 Grover syndrome amplification bridge."""
    sweep = evaluate_pi_over_3_fixed_point_amplification(
        p0_values=[0.125, 0.25, 0.50, 0.75, 1.0]
    )

    rec_half = next(r for r in sweep["records"] if abs(r["p0"] - 0.50) < 1e-12)
    rec_three_quarters = next(r for r in sweep["records"] if abs(r["p0"] - 0.75) < 1e-12)

    all_passed = (
        sweep["all_verified"]
        and abs(rec_half["p1_standard_pi_grover"] - 0.50) < 1e-12
        and abs(rec_half["p1_pi_over_3_explicit"] - 0.875) < 1e-12
        and abs(rec_half["p2_recursive_pi_over_3"] - 511.0 / 512.0) < 1e-12
        # At p0 = 0.75, standard pi-Grover over-rotates all the way down to 0.0, whereas pi/3 boosts to 63/64 = 0.984375!
        and abs(rec_three_quarters["p1_standard_pi_grover"] - 0.0) < 1e-12
        and abs(rec_three_quarters["p1_pi_over_3_explicit"] - 63.0 / 64.0) < 1e-12
    )

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "proof_status": "LOCAL_DERIVATION_REVIEW_PENDING_NOT_FORMALLY_VERIFIED",
        "scope_constraints": {
            "applies_to": "Fixed-point pi/3 Grover-Yoder-Low-Chuang syndrome amplification 1 - P_1 = (1 - p_0)^3 on CNOT witness trees",
            "does_not_claim": "Zero-error 1.0 exactness at p_0 = 1/2 in a finite number of pi/3 steps (converges doubly-exponentially as 1 - 2^{-3^L})",
            "controls_included": "Evaluates p_0 in {1/8, 1/4, 1/2, 3/4, 1}, verifying P_1^{(pi/3)}(1/2) = 7/8 = 0.875 vs P_1^{(pi)}(1/2) = 0.50, and P_1^{(pi/3)}(3/4) = 63/64 vs P_1^{(pi)}(3/4) = 0.0.",
        },
        "pi_over_3_amplification_sweep": sweep,
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
