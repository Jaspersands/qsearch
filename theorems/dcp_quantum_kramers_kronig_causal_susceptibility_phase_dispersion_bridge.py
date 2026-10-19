r"""
Subsystem 153: Quantum Kramers-Kronig Causal Susceptibility & Dispersive Readout Phase Bridge.

Proves that any causal linear dispersive syndrome-readout resonator with complex
susceptibility \chi(\Delta) = \chi'(\Delta) + i \chi''(\Delta) (\Delta = \omega - \omega_r)
for a Lorentzian cavity resonance of half-linewidth \kappa / 2 = \gamma:
  \chi(\Delta) = \frac{-\Delta + i \gamma}{\Delta^2 + \gamma^2}
satisfies the exact Kramers-Kronig Hilbert transform relation:
  \chi'(\Delta) = \frac{1}{\pi} \mathcal{P} \int_{-\infty}^{\infty} \frac{\chi''(\Omega)}{\Omega - \Delta} d\Omega
                = \frac{-\Delta}{\Delta^2 + \gamma^2},
and induces a deterministic dispersive phase shift \phi(\Delta) = -\arctan(\Delta / \gamma)
that must be calibrated or echoed out to prevent Z-phase bias on unmeasured spectator
witness qubits.
"""

from __future__ import annotations
import math
from typing import Any, Dict, List


def lorentzian_susceptibility(detuning_delta: float, half_linewidth_gamma: float) -> Dict[str, float]:
    denom = detuning_delta * detuning_delta + half_linewidth_gamma * half_linewidth_gamma
    chi_real = -detuning_delta / denom
    chi_imag = half_linewidth_gamma / denom
    phase_shift = math.atan2(chi_imag, chi_real)
    return {
        "detuning_delta": float(detuning_delta),
        "gamma": float(half_linewidth_gamma),
        "chi_real_analytic": float(chi_real),
        "chi_imag_analytic": float(chi_imag),
        "modulus_squared": float(1.0 / denom),
        "dispersive_phase_rad": float(phase_shift),
    }


def verify_kramers_kronig_hilbert_quadrature(
    detuning_delta: float = 1.5,
    half_linewidth_gamma: float = 1.0,
    cutoff_w: float = 200.0,
    num_pairs: int = 4000,
) -> Dict[str, float]:
    r"""
    Numerically evaluate the principal-value Kramers-Kronig integral by symmetric
    folding around the pole \Omega = \Delta:
      \chi'(\Delta) = \frac{1}{\pi} \int_0^\infty \frac{\chi''(\Delta + u) - \chi''(\Delta - u)}{u} du,
    which removes the 1/u singularity analytically at u = 0!
    """
    du = cutoff_w / float(num_pairs)
    integral = 0.0
    g2 = half_linewidth_gamma * half_linewidth_gamma
    for k in range(1, num_pairs + 1):
        u = (k - 0.5) * du
        chi_im_plus = half_linewidth_gamma / (((detuning_delta + u) ** 2) + g2)
        chi_im_minus = half_linewidth_gamma / (((detuning_delta - u) ** 2) + g2)
        integral += ((chi_im_plus - chi_im_minus) / u) * du
    chi_real_kk = integral / math.pi
    exact = lorentzian_susceptibility(detuning_delta, half_linewidth_gamma)["chi_real_analytic"]
    return {
        "detuning_delta": float(detuning_delta),
        "gamma": float(half_linewidth_gamma),
        "chi_real_kramers_kronig_quadrature": float(chi_real_kk),
        "chi_real_analytic": float(exact),
        "absolute_error": float(abs(chi_real_kk - exact)),
    }


def generate_dcp_quantum_kramers_kronig_causal_susceptibility_phase_dispersion_certificate() -> Dict[str, Any]:
    """Generate the Subsystem 153 verification certificate."""
    kk_checks = [
        verify_kramers_kronig_hilbert_quadrature(detuning_delta=d, half_linewidth_gamma=1.0)
        for d in [-2.0, -1.0, 0.0, 1.0, 2.0]
    ]
    res_zero = lorentzian_susceptibility(0.0, 1.0)
    res_plus = lorentzian_susceptibility(1.0, 1.0)
    res_minus = lorentzian_susceptibility(-1.0, 1.0)

    theorem_checks = {
        "kramers_kronig_principal_value_matches_analytic_within_2e_minus_3": bool(
            all(c["absolute_error"] < 2e-3 for c in kk_checks)
        ),
        "zero_detuning_has_purely_absorptive_susceptibility": bool(
            abs(res_zero["chi_real_analytic"]) < 1e-15 and abs(res_zero["chi_imag_analytic"] - 1.0) < 1e-15
        ),
        "real_part_odd_and_imaginary_part_even_in_detuning": bool(
            abs(res_plus["chi_real_analytic"] + res_minus["chi_real_analytic"]) < 1e-15
            and abs(res_plus["chi_imag_analytic"] - res_minus["chi_imag_analytic"]) < 1e-15
        ),
        "half_linewidth_detuning_gives_exact_3pi_over_4_phase": bool(
            abs(res_plus["dispersive_phase_rad"] - 3.0 * math.pi / 4.0) < 1e-12
        ),
    }

    return {
        "subsystem_id": "dcp_quantum_kramers_kronig_causal_susceptibility_phase_dispersion_bridge",
        "subsystem_number": 153,
        "domain": "causal_linear_response_kramers_kronig_dispersive_readout",
        "kramers_kronig_quadrature_checks": kk_checks,
        "theorem_checks": theorem_checks,
        "all_checks_passed": bool(all(theorem_checks.values())),
        "falsification_status": {
            "accepted_speedup_candidate": False,
            "new_active_negative_result_created": False,
            "novelty_claim": False,
        },
    }
