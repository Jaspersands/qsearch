r"""DCP Quantum Chernoff Information geodesic exponent vs. separable Helstrom Chernoff bridge.

Establishes the exact closed-form Quantum Chernoff Bound (QCB) exponent
    xi_QCB(rho_0, rho_1) = -ln( min_{0 <= s <= 1} Tr(rho_0^s rho_1^{1-s}) )
for distinguishing two single-qubit DCP phase states rho_0 = rho(theta_0, gamma) and
rho_1 = rho(theta_1, gamma) (with phase difference Delta_theta = theta_1 - theta_0),
and proves a strict multi-copy collective Chernoff exponent advantage over optimal
separable single-copy Helstrom measurements whenever rho_0 and rho_1 do not commute:

1. Exact Midpoint Optimality (s* = 1/2) and Closed-Form Quantum Bhattacharyya Coefficient:
   Because rho_0 and rho_1 are unitarily equivalent with identical spectrum
   lambda_+ = (1 + gamma)/2 and lambda_- = (1 - gamma)/2, the Holder trace function
   f(s) = Tr(rho_0^s rho_1^{1-s}) is symmetric (f(s) = f(1 - s)) and strictly convex on
   [0, 1], attaining its unique global minimum at s* = 1/2:
       min_{0 <= s <= 1} Tr(rho_0^s rho_1^{1-s}) = Tr(rho_0^{1/2} rho_1^{1/2})
           = cos^2(Delta_theta / 2) + sin^2(Delta_theta / 2) * sqrt(1 - gamma^2)
           = 1 - (1 - sqrt(1 - gamma^2)) * sin^2(Delta_theta / 2)!
   Therefore, the exact Quantum Chernoff Exponent is:
       xi_QCB(Delta_theta, gamma) = -ln( 1 - (1 - sqrt(1 - gamma^2)) * sin^2(Delta_theta / 2) ).

2. Strict Collective Multi-Copy Exponent Advantage at Non-Commuting Phases (Delta_theta != 0, pi):
   Any repeated single-copy projective measurement has minimum single-shot Helstrom error
   eps_Hel = 0.5 * (1 - gamma * |sin(Delta_theta / 2)|), whose classical Bhattacharyya
   coefficient is:
       B_sep_Hel(Delta_theta, gamma) = 2 * sqrt(eps_Hel * (1 - eps_Hel))
                                     = sqrt(1 - gamma^2 * sin^2(Delta_theta / 2)),
   with separable Chernoff exponent xi_sep_Hel = -ln( B_sep_Hel ).
   - Commuting Antipodal Case (Delta_theta = pi, sin^2(Delta_theta / 2) = 1):
     rho_0 and rho_1 commute, and B_QCB == B_sep_Hel == sqrt(1 - gamma^2) (zero gap).
   - Non-Commuting Case (0 < sin^2(Delta_theta / 2) < 1, e.g. Delta_theta = pi / 2):
     By the strict concavity of u -> sqrt(1 - gamma^2 * u) on (0, 1):
         Tr(rho_0^{1/2} rho_1^{1/2}) < sqrt(1 - gamma^2 * sin^2(Delta_theta / 2)),
     proving that collective entangling measurements across r copies achieve a STRICTLY
     LARGER asymptotic error exponent:
         xi_QCB(Delta_theta, gamma) > xi_sep_Hel(Delta_theta, gamma)
     for every gamma in (0, 1) and every non-commuting phase shift Delta_theta not in {0, pi} mod 2*pi!
"""

from __future__ import annotations

import hashlib
import json
import math
from typing import Any, Dict, List


THEOREM_ID = "dcp_quantum_chernoff_information_geodesic_exponent_bridge"
SCHEMA_VERSION = "dcp-quantum-chernoff-information-geodesic-exponent-bridge-v1"


def _trace_rho0_s_rho1_1_minus_s(delta_theta: float, gamma: float, s_exp: float) -> float:
    """Compute exact Tr(rho_0^s rho_1^{1-s}) from the spectral decomposition of rho_0 and rho_1."""
    lam_p = 0.5 * (1.0 + gamma)
    lam_m = 0.5 * (1.0 - gamma)
    c2 = math.cos(0.5 * delta_theta) ** 2
    s2 = math.sin(0.5 * delta_theta) ** 2
    # Overlaps between eigenstates |psi_pm(theta_0)> and |psi_pm(theta_1)>:
    # |<+|+>|^2 = |-|->|^2 = cos^2(Delta_theta / 2)
    # |<+|->|^2 = |<-|+>|^2 = sin^2(Delta_theta / 2)
    term_same = c2 * ((lam_p ** s_exp) * (lam_p ** (1.0 - s_exp)) + (lam_m ** s_exp) * (lam_m ** (1.0 - s_exp)))
    term_cross = s2 * ((lam_p ** s_exp) * (lam_m ** (1.0 - s_exp)) + (lam_m ** s_exp) * (lam_p ** (1.0 - s_exp)))
    return term_same + term_cross


def evaluate_quantum_vs_separable_chernoff_exponents(
    delta_theta_values: List[float],
    gamma: float = 0.85,
) -> Dict[str, Any]:
    """Compare exact Quantum Chernoff Exponent against separable Helstrom Chernoff exponent across Delta_theta."""
    records: List[Dict[str, Any]] = []
    s_grid = [0.1 * k for k in range(1, 10)]

    for d_theta in delta_theta_values:
        # 1. Verify midpoint s* = 0.5 minimizes Tr(rho_0^s rho_1^{1-s}) across s in (0, 1):
        grid_vals = [_trace_rho0_s_rho1_1_minus_s(d_theta, gamma, s_val) for s_val in s_grid]
        b_qcb_explicit = _trace_rho0_s_rho1_1_minus_s(d_theta, gamma, 0.5)
        min_grid_val = min(grid_vals)

        s2 = math.sin(0.5 * d_theta) ** 2
        b_qcb_closed = 1.0 - (1.0 - math.sqrt(1.0 - (gamma ** 2))) * s2
        xi_qcb = -math.log(b_qcb_closed)

        # 2. Separable single-copy Helstrom Bhattacharyya coefficient and Chernoff exponent:
        b_sep_hel = math.sqrt(1.0 - (gamma ** 2) * s2)
        xi_sep_hel = -math.log(b_sep_hel)

        is_commuting = (s2 < 1e-12) or (abs(s2 - 1.0) < 1e-12)

        records.append({
            "delta_theta_over_pi": d_theta / math.pi,
            "sin_sq_half_delta_theta": s2,
            "is_commuting_pair": is_commuting,
            "quantum_bhattacharyya_explicit": b_qcb_explicit,
            "quantum_bhattacharyya_closed_form": b_qcb_closed,
            "separable_helstrom_bhattacharyya": b_sep_hel,
            "quantum_chernoff_exponent_xi_QCB": xi_qcb,
            "separable_helstrom_exponent_xi_sep": xi_sep_hel,
            "collective_exponent_ratio_qcb_over_sep": (xi_qcb / xi_sep_hel) if xi_sep_hel > 0 else 1.0,
            "exact_laws_verified": (
                abs(b_qcb_explicit - b_qcb_closed) < 1e-12
                and abs(min_grid_val - b_qcb_explicit) < 1e-12
                and (
                    abs(xi_qcb - xi_sep_hel) < 1e-12
                    if is_commuting
                    else (xi_qcb > xi_sep_hel + 1e-4)
                )
            ),
        })

    return {
        "gamma": gamma,
        "records": records,
        "all_verified": all(r["exact_laws_verified"] for r in records),
    }


def generate_dcp_quantum_chernoff_information_geodesic_exponent_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the Quantum Chernoff Information geodesic exponent bridge."""
    sweep = evaluate_quantum_vs_separable_chernoff_exponents(
        delta_theta_values=[math.pi / 4.0, math.pi / 2.0, 3.0 * math.pi / 4.0, math.pi],
        gamma=0.85,
    )

    rec_pi2 = sweep["records"][1]  # Delta_theta = pi/2 (non-commuting -> strict collective advantage!)
    rec_pi = sweep["records"][3]   # Delta_theta = pi   (commuting -> exact equality!)

    all_passed = (
        sweep["all_verified"]
        and rec_pi2["collective_exponent_ratio_qcb_over_sep"] > 1.15
        and abs(rec_pi["collective_exponent_ratio_qcb_over_sep"] - 1.0) < 1e-12
    )

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "proof_status": "LOCAL_DERIVATION_REVIEW_PENDING_NOT_FORMALLY_VERIFIED",
        "scope_constraints": {
            "applies_to": "Quantum Chernoff Bound (QCB) exponent xi_QCB vs. separable single-copy Helstrom Chernoff exponent on DCP states",
            "does_not_claim": "Collective Chernoff advantage at Delta_theta == pi where rho_0 and rho_1 commute",
            "controls_included": "Evaluates Delta_theta in {pi/4, pi/2, 3*pi/4, pi} at gamma = 0.85, verifying strict collective advantage xi_QCB > xi_sep_Hel for non-commuting phases (>1.15x at pi/2) and exact equality at commuting Delta_theta = pi.",
        },
        "chernoff_exponent_sweep": sweep,
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
