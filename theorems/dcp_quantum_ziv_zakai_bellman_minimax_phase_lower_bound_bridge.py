r"""
Subsystem 141: Quantum Ziv-Zakai Bayesian Phase Estimation Lower Bound Bridge.

Proves and numerically certifies the Quantum Ziv-Zakai Bound (QZZB) for circular
/ modular Z_q phase estimation from K copies of a DCP witness state:
  rho(theta) = (1 - v)/2 I + v |psi(theta)><psi(theta)|,
  |psi(theta)> = (|0> + e^{i theta} |1>) / sqrt(2).

While the local Quantum Cramer-Rao Bound (QCRB) scales as:
  MSE_QCRB(K) = 1 / (K * F_Q) = 1 / (K * v^2),
which vanishes at K -> 0 or v -> 0 only locally and ignores prior wrap-around
and large-error ambiguity on S^1 = [0, 2*pi), the Quantum Ziv-Zakai Bound
integrates the Helstrom minimum error probability P_e(h) between rho(theta)^{\otimes K}
and rho(theta + h)^{\otimes K}:
  |<psi(theta)|psi(theta+h)>|^2 = cos^2(h / 2)  (for pure states v = 1),
  P_e(h; K, v) = (1/2) * (1 - sqrt(1 - F(rho(0), rho(h))^K)),
  MSE_QZZB(K, v) = (1/2) \int_0^{\pi} h * (1 - h/\pi) * 2 P_e(h; K, v) dh.

At low copy count K or low visibility v, MSE_QZZB correctly captures the uniform
prior saturation ceiling (\pi^2 / 12 for [-pi/2, pi/2] or \pi^2 / 3 on [-pi, pi])
and strictly bounds any unbiased or Bayesian phase estimator before transitioning
asymptotically to the 1/(K v^2) QCRB regime at large K.
"""

from __future__ import annotations
import math
from typing import Any, Dict, List


def qubit_dephased_fidelity(phase_lag_h: float, visibility_v: float) -> float:
    r"""
    Uhlmann fidelity F(rho(0), rho(h)) = (Tr sqrt(sqrt(rho_0) rho_h sqrt(rho_0)))^2
    for single-qubit states in the equatorial plane with Bloch vector length v:
      r_0 = (v, 0, 0), r_h = (v cos h, v sin h, 0).
    For two qubits with equal Bloch length v and angle h between r_0 and r_h:
      F(rho_0, rho_h) = (1/2) * (1 + r_0 . r_h + sqrt(1 - |r_0|^2) * sqrt(1 - |r_h|^2))
                      = (1/2) * (1 + v^2 cos(h) + (1 - v^2))
                      = 1 - (v^2 / 2) * (1 - cos(h))
                      = 1 - v^2 * sin^2(h / 2).
    r"""
    s2 = math.sin(0.5 * phase_lag_h) ** 2
    return max(0.0, min(1.0, 1.0 - (visibility_v ** 2) * s2))


def helstrom_min_error_bound(phase_lag_h: float, copies_k: int, visibility_v: float) -> float:
    r"""
    Lower bound on two-point hypothesis test error P_e(h) between rho(0)^{\otimes K}
    and rho(h)^{\otimes K} via Fuchs-van de Graaf / Uhlmann fidelity:
      P_e(h) >= (1/2) * (1 - sqrt(1 - F(rho_0, rho_h)^K)).
    (Exact equality holds for pure states v = 1.)
    r"""
    fid_single = qubit_dephased_fidelity(phase_lag_h, visibility_v)
    fid_k = fid_single ** copies_k
    trace_dist_upper = math.sqrt(max(0.0, 1.0 - fid_k))
    return 0.5 * (1.0 - trace_dist_upper)


def evaluate_quantum_ziv_zakai_vs_qcrb(
    copies_list: List[int],
    visibility_v: float = 0.85,
    num_grid: int = 400,
) -> List[Dict[str, float]]:
    r"""
    Compute the Quantum Ziv-Zakai lower bound on [-pi/2, pi/2] (width W = pi,
    prior variance pi^2 / 12 = 0.822467) using composite midpoint quadrature:
      MSE_QZZB = (1/2) \int_0^{\pi} h * (1 - h/\pi) * 2 P_e(h; K, v) dh,
    and compare against the Quantum Cramer-Rao Bound 1 / (K * F_Q) where
    for equatorial dephased qubit rho(theta), F_Q = v^2.
    r"""
    width = math.pi
    dh = width / num_grid
    prior_variance = (width ** 2) / 12.0
    fq_single = visibility_v ** 2

    rows: List[Dict[str, float]] = []
    for k_copies in copies_list:
        integral = 0.0
        for idx in range(num_grid):
            h = (idx + 0.5) * dh
            pe = helstrom_min_error_bound(h, k_copies, visibility_v)
            integral += 0.5 * h * (1.0 - h / width) * (2.0 * pe) * dh
        qcrb = 1.0 / (k_copies * fq_single) if k_copies > 0 and fq_single > 0 else None
        rows.append({
            "copies_k": int(k_copies),
            "visibility_v": float(visibility_v),
            "qzzb_mse": float(integral),
            "qcrb_mse": (float(qcrb) if qcrb is not None else None),
            "prior_variance_ceiling": float(prior_variance),
            "qzzb_respects_prior_ceiling": bool(integral <= prior_variance + 1e-12),
        })
    return rows


def generate_dcp_quantum_ziv_zakai_bellman_minimax_phase_lower_bound_certificate() -> Dict[str, Any]:
    """Generate the Subsystem 141 verification certificate."""
    sweep_v085 = evaluate_quantum_ziv_zakai_vs_qcrb([1, 2, 4, 8, 16, 32, 64], visibility_v=0.85)
    sweep_pure = evaluate_quantum_ziv_zakai_vs_qcrb([1, 2, 4, 8, 16, 32, 64], visibility_v=1.0)
    zero_vis = evaluate_quantum_ziv_zakai_vs_qcrb([10], visibility_v=0.0)[0]

    # At v = 0, P_e = 1/2 everywhere, so QZZB equals the exact prior variance pi^2 / 12:
    # \int_0^W (1/2) h (1 - h/W) dh = W^2 / 12.
    prior_var = (math.pi ** 2) / 12.0
    zero_vis_exact = abs(zero_vis["qzzb_mse"] - prior_var) < 1e-4

    # Monotone decrease with K
    monotone_v085 = all(
        sweep_v085[i]["qzzb_mse"] > sweep_v085[i + 1]["qzzb_mse"]
        for i in range(len(sweep_v085) - 1)
    )
    # At K = 1, QCRB = 1 / 0.85^2 = 1.38408 exceeds the entire prior variance pi^2/12 = 0.822467,
    # whereas QZZB stays strictly bounded by the prior ceiling!
    k1_row = sweep_v085[0]
    qcrb_violates_prior_at_k1 = k1_row["qcrb_mse"] > prior_var and k1_row["qzzb_mse"] < prior_var

    # Pure state v = 1 achieves strictly smaller QZZB bound than noisy v = 0.85 at all K
    pure_beats_noisy = all(
        sweep_pure[i]["qzzb_mse"] < sweep_v085[i]["qzzb_mse"]
        for i in range(len(sweep_pure))
    )

    theorem_checks = {
        "zero_visibility_recovers_exact_prior_variance": bool(zero_vis_exact),
        "qzzb_monotone_decreasing_with_copies_k": bool(monotone_v085),
        "low_copy_qcrb_exceeds_prior_while_qzzb_respects_ceiling": bool(qcrb_violates_prior_at_k1),
        "pure_witness_strictly_outperforms_dephased_witness": bool(pure_beats_noisy),
        "single_qubit_fidelity_formula_exact": bool(
            abs(qubit_dephased_fidelity(math.pi / 3.0, 1.0) - 0.75) < 1e-12
        ),
    }

    return {
        "subsystem_id": "dcp_quantum_ziv_zakai_bellman_minimax_phase_lower_bound_bridge",
        "subsystem_number": 141,
        "domain": "quantum_estimation_theory_ziv_zakai_phase_bounds",
        "prior_variance_pi_sq_over_12": float(prior_var),
        "zero_visibility_check": zero_vis,
        "dephased_v085_sweep": sweep_v085,
        "pure_v100_sweep": sweep_pure,
        "theorem_checks": theorem_checks,
        "all_checks_passed": bool(all(theorem_checks.values())),
        "falsification_status": {
            "accepted_speedup_candidate": False,
            "new_active_negative_result_created": False,
            "novelty_claim": False,
        },
    }
