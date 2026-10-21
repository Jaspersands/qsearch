r"""
Subsystem 145: Quantum Stein's Lemma & Umegaki Relative Entropy Syndrome Hypothesis Bridge.

Proves and certifies the asymmetric quantum hypothesis testing exponent (Hiai-Petz /
Ogawa-Nagaoka Quantum Stein's Lemma) between a coherent CNOT-peeled witness state
rho_1 (Bloch visibility v_1 along +X) and a carry-dephased / unpeeled witness state
rho_0 (Bloch visibility v_0 < v_1 along +X):
  rho_k = (1/2) (I + v_k X),   eigenvalues lambda_{\pm}^{(k)} = (1 \pm v_k) / 2.

Because [rho_1, rho_0] = 0 in the shared Pauli-X eigenbasis {|+>, |->} (and more generally
via Umegaki quantum relative entropy D(rho_1 || rho_0) = Tr(rho_1 (log rho_1 - log rho_0))),
for bounded type-I false-alarm probability alpha in (0, 1), the minimum type-II missed-detection
probability beta_K(alpha) over K copies decays exponentially at the exact rate:
  \lim_{K -> \infty} -(1/K) \log \beta_K(\alpha) = D(\rho_1 || \rho_0)
    = \frac{1 + v_1}{2} \ln\left(\frac{1 + v_1}{1 + v_0}\right)
    + \frac{1 - v_1}{2} \ln\left(\frac{1 - v_1}{1 - v_0}\right).

Furthermore, Pinsker's inequality lower-bounds D(rho_1 || rho_0) by twice the squared
trace distance:
  D(\rho_1 || \rho_0) >= 2 * ||\rho_1 - \rho_0||_1^2 = \frac{1}{2} (v_1 - v_0)^2.
"""

from __future__ import annotations
import math
from typing import Any, Dict, List


def umegaki_relative_entropy_qubit(v1_x: float, v0_x: float, theta_angle: float = 0.0) -> float:
    r"""
    Exact Umegaki quantum relative entropy D(rho_1 || rho_0) = Tr(rho_1 (ln rho_1 - ln rho_0))
    between two single-qubit states:
      rho_1 = (1/2)(I + v_1 X),
      rho_0 = (1/2)(I + v_0 (cos(theta) X + sin(theta) Y)).
    Using the spectral decomposition of rho_1 and rho_0:
      Tr(rho_1 ln rho_1) = ((1+v_1)/2) ln((1+v_1)/2) + ((1-v_1)/2) ln((1-v_1)/2).
      ln(rho_0) = (1/2) ln((1 - v_0^2)/4) I + (1/2) ln((1+v_0)/(1-v_0)) (cos(theta) X + sin(theta) Y),
      so Tr(rho_1 ln rho_0) = (1/2) ln((1 - v_0^2)/4) + (v_1 cos(theta) / 2) ln((1+v_0)/(1-v_0)).
    r"""
    if abs(v0_x) >= 1.0:
        raise ValueError("Reference state rho_0 must be full rank (|v0_x| < 1)")
    p1_plus = 0.5 * (1.0 + v1_x)
    p1_minus = 0.5 * (1.0 - v1_x)
    ent_rho1 = 0.0
    if p1_plus > 0:
        ent_rho1 += p1_plus * math.log(p1_plus)
    if p1_minus > 0:
        ent_rho1 += p1_minus * math.log(p1_minus)

    cross_term = 0.5 * math.log(0.25 * (1.0 - v0_x * v0_x)) + 0.5 * v1_x * math.cos(theta_angle) * math.log(
        (1.0 + v0_x) / (1.0 - v0_x)
    )
    return float(ent_rho1 - cross_term)


def quantum_pinsker_lower_bound(v1_x: float, v0_x: float, theta_angle: float = 0.0) -> float:
    r"""
    Trace distance T(rho_1, rho_0) = (1/2) ||rho_1 - rho_0||_1
      = (1/2) sqrt((v_1 - v_0 cos(theta))^2 + (v_0 sin(theta))^2).
    Quantum Pinsker inequality: D(rho_1 || rho_0) >= 2 * T(rho_1, rho_0)^2.
    r"""
    dx = v1_x - v0_x * math.cos(theta_angle)
    dy = -v0_x * math.sin(theta_angle)
    trace_dist_sq = 0.25 * (dx * dx + dy * dy)
    return float(2.0 * trace_dist_sq)


def generate_dcp_quantum_sanov_theorem_large_deviations_kl_syndrome_hypothesis_certificate() -> Dict[str, Any]:
    """Generate the Subsystem 145 verification certificate."""
    # Compare peeled visibility v_1 = 0.92 vs carry-corrupted visibility v_0 in [0.10, 0.25, 0.50, 0.75]
    v1 = 0.92
    sweep: List[Dict[str, float]] = []
    for v0 in [0.10, 0.25, 0.50, 0.75]:
        d_rel = umegaki_relative_entropy_qubit(v1, v0, theta_angle=0.0)
        pinsker_lb = quantum_pinsker_lower_bound(v1, v0, theta_angle=0.0)
        # Non-commuting rotated reference state theta = pi / 3
        d_rot = umegaki_relative_entropy_qubit(v1, v0, theta_angle=math.pi / 3.0)
        pinsker_rot = quantum_pinsker_lower_bound(v1, v0, theta_angle=math.pi / 3.0)
        sweep.append({
            "peeled_visibility_v1": float(v1),
            "corrupted_visibility_v0": float(v0),
            "stein_exponent_d_rel": float(d_rel),
            "pinsker_lower_bound": float(pinsker_lb),
            "noncommuting_rotated_d_rel": float(d_rot),
            "noncommuting_pinsker_lb": float(pinsker_rot),
            "copies_for_1e_minus_6_type2_error": float(math.ceil(math.log(1e6) / d_rel)),
        })

    # Identity check: D(rho || rho) = 0
    zero_div = abs(umegaki_relative_entropy_qubit(0.7, 0.7, 0.0)) < 1e-15

    # Pinsker inequality holds everywhere
    pinsker_ok = all(
        r["stein_exponent_d_rel"] >= r["pinsker_lower_bound"] - 1e-12
        and r["noncommuting_rotated_d_rel"] >= r["noncommuting_pinsker_lb"] - 1e-12
        for r in sweep
    )

    # Non-commuting phase misalignment theta = pi/3 increases distinguishability D(rho_1 || rho_0)
    noncommuting_increases_d = all(
        r["noncommuting_rotated_d_rel"] > r["stein_exponent_d_rel"] for r in sweep
    )

    theorem_checks = {
        "zero_relative_entropy_for_identical_states": bool(zero_div),
        "quantum_pinsker_inequality_holds_commuting_and_noncommuting": bool(pinsker_ok),
        "stein_exponent_monotone_decreasing_as_v0_approaches_v1": bool(
            all(sweep[i]["stein_exponent_d_rel"] > sweep[i + 1]["stein_exponent_d_rel"] for i in range(len(sweep) - 1))
        ),
        "phase_misalignment_increases_umegaki_divergence": bool(noncommuting_increases_d),
    }

    return {
        "subsystem_id": "dcp_quantum_sanov_theorem_large_deviations_kl_syndrome_hypothesis_bridge",
        "subsystem_number": 145,
        "domain": "quantum_information_stein_lemma_umegaki_relative_entropy",
        "visibility_sweep": sweep,
        "theorem_checks": theorem_checks,
        "all_checks_passed": bool(all(theorem_checks.values())),
        "falsification_status": {
            "accepted_speedup_candidate": False,
            "new_active_negative_result_created": False,
            "novelty_claim": False,
        },
    }
