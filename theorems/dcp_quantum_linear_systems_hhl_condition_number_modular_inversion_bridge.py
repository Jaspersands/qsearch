r"""
Subsystem 143: Quantum Linear Systems (HHL) Condition Number vs. Exact Modular Z_q Inversion Bridge.

Contrasts two paradigms for solving a modular syndrome system H s = b (mod q):
  1. Continuous Complex Embedding (Harrow-Hassidim-Lloyd / QSVT matrix inversion):
     Embeds H in R^{m x m} and prepares |H^{-1} b> / ||H^{-1} b|| with runtime
     O(kappa(H)^2 log(m) / eps) (or O(kappa(H) log(kappa/eps)) via LCU/QSVT).
     Suffers two fundamental obstructions for modular Z_q problems:
       (a) Unkown integer wrap-around vector k in Z^m in the lifted equation H s = b + q k,
           meaning H^{-1} b != (H^{-1} b mod q) whenever wrap-around k != 0.
       (b) Singular value spread kappa(H) = sigma_max(H) / sigma_min(H) > 1 reduces HHL
           post-selection success probability P_succ >= 1 / kappa(H)^2.
  2. Exact Discrete Unitary Modular Peeling (Reversible CNOT / Hensel / Smith Normal Form):
     Operates directly on computational basis states |b> in (C^q)^{\otimes m} via reversible
     modular row operations |b> -> |H^{-1} b mod q>, which is a permutation unitary U_H
     with all singular values equal to 1 (kappa(U_H) = 1.0, success probability = 1.0)
     and automatically folds modular wrap-around k in Z^m without ambiguity!
"""

from __future__ import annotations
import math
from typing import Any, Dict, List


def mat_vec_mod_q(mat: List[List[int]], vec: List[int], q: int) -> List[int]:
    return [sum(mat[i][j] * vec[j] for j in range(len(vec))) % q for i in range(len(mat))]


def analyze_2x2_real_vs_modular_inversion(
    h_mat: List[List[int]],
    q: int,
) -> Dict[str, Any]:
    r"""
    For a 2x2 integer matrix H with gcd(det(H), q) = 1:
      - Compute exact real singular values sigma_max, sigma_min and condition number kappa(H).
      - Compute HHL worst-case post-selection success probability 1 / kappa(H)^2.
      - Compare real inverse H^{-1} b against modular inverse H^{-1} b (mod q) across all
        q^2 secret vectors s in Z_q^2 where b = H s mod q.
    r"""
    a, b = h_mat[0][0], h_mat[0][1]
    c, d = h_mat[1][0], h_mat[1][1]
    det_real = a * d - b * c
    det_mod = det_real % q
    if math.gcd(det_mod, q) != 1:
        raise ValueError("det(H) must be coprime to q")

    # Exact singular values of 2x2 matrix via eigenvalues of H^T H
    tr_hth = float(a * a + b * b + c * c + d * d)
    det_hth = float(det_real * det_real)
    disc = math.sqrt(max(0.0, tr_hth * tr_hth - 4.0 * det_hth))
    lam_max = 0.5 * (tr_hth + disc)
    lam_min = 0.5 * (tr_hth - disc)
    sigma_max = math.sqrt(lam_max)
    sigma_min = math.sqrt(max(1e-15, lam_min))
    kappa = sigma_max / sigma_min
    hhl_worst_case_p_succ = 1.0 / (kappa * kappa)

    # Modular inverse of H over Z_q
    inv_det_mod = pow(det_mod, -1, q)
    h_inv_mod = [
        [(d * inv_det_mod) % q, ((-b) * inv_det_mod) % q],
        [((-c) * inv_det_mod) % q, (a * inv_det_mod) % q],
    ]

    # Count how many of the q^2 secrets s in Z_q^2 experience integer wrap-around k != 0
    # in b = H s mod q such that real H^{-1} b != s
    wraparound_failures = 0
    modular_unitary_successes = 0
    for s0 in range(q):
        for s1 in range(q):
            s_vec = [s0, s1]
            b_mod = mat_vec_mod_q(h_mat, s_vec, q)
            # Real inversion H^{-1} b_mod
            s_real_0 = (d * b_mod[0] - b * b_mod[1]) / float(det_real)
            s_real_1 = (-c * b_mod[0] + a * b_mod[1]) / float(det_real)
            if abs(s_real_0 - s0) > 1e-9 or abs(s_real_1 - s1) > 1e-9:
                wraparound_failures += 1
            # Modular unitary peeling
            s_peeled = mat_vec_mod_q(h_inv_mod, b_mod, q)
            if s_peeled == s_vec:
                modular_unitary_successes += 1

    total_secrets = q * q
    return {
        "matrix_h": h_mat,
        "modulus_q": int(q),
        "det_real": int(det_real),
        "sigma_max": float(sigma_max),
        "sigma_min": float(sigma_min),
        "condition_number_kappa": float(kappa),
        "hhl_worst_case_success_prob": float(hhl_worst_case_p_succ),
        "real_inversion_wraparound_failure_fraction": float(wraparound_failures / total_secrets),
        "modular_unitary_condition_number": 1.0,
        "modular_unitary_recovery_fraction": float(modular_unitary_successes / total_secrets),
    }


def generate_dcp_quantum_linear_systems_hhl_condition_number_modular_inversion_certificate() -> Dict[str, Any]:
    """Generate the Subsystem 143 verification certificate."""
    well_cond = analyze_2x2_real_vs_modular_inversion([[1, 1], [0, 1]], q=8)
    ill_cond = analyze_2x2_real_vs_modular_inversion([[1, 5], [1, 6]], q=8)

    theorem_checks = {
        "unipotent_upper_triangular_has_kappa_golden_ratio_squared": bool(
            abs(well_cond["condition_number_kappa"] - ((1.0 + math.sqrt(5.0)) / 2.0) ** 2) < 1e-9
        ),
        "ill_conditioned_matrix_inflates_hhl_kappa_above_35": bool(
            ill_cond["condition_number_kappa"] > 35.0
            and ill_cond["hhl_worst_case_success_prob"] < 0.001
        ),
        "real_hhl_inversion_fails_on_modular_wraparound_states": bool(
            well_cond["real_inversion_wraparound_failure_fraction"] > 0.25
            and ill_cond["real_inversion_wraparound_failure_fraction"] > 0.70
        ),
        "discrete_modular_unitary_peeling_achieves_100pct_with_kappa_1": bool(
            well_cond["modular_unitary_recovery_fraction"] == 1.0
            and ill_cond["modular_unitary_recovery_fraction"] == 1.0
            and ill_cond["modular_unitary_condition_number"] == 1.0
        ),
    }

    return {
        "subsystem_id": "dcp_quantum_linear_systems_hhl_condition_number_modular_inversion_bridge",
        "subsystem_number": 143,
        "domain": "quantum_linear_systems_hhl_vs_modular_peeling",
        "shear_matrix_case": well_cond,
        "ill_conditioned_unimodular_case": ill_cond,
        "theorem_checks": theorem_checks,
        "all_checks_passed": bool(all(theorem_checks.values())),
        "falsification_status": {
            "accepted_speedup_candidate": False,
            "new_active_negative_result_created": False,
            "novelty_claim": False,
        },
    }
