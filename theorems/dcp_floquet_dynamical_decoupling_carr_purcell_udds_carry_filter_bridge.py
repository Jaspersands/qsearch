r"""
Subsystem 144: Floquet Dynamical Decoupling (CPMG vs. Uhrig UDD) Filter Function Bridge.

Analyzes time-domain pi-pulse dynamical decoupling sequences applied during idle or
multi-qubit routing intervals of coherent CNOT syndrome extraction:
  1. Free Induction Decay (FID, N = 0 pulses):
       y_FID(omega * tau) = |1 - e^{i omega tau}|^2 = 4 sin^2(omega tau / 2) = O((omega tau)^2).
  2. Carr-Purcell-Meiboom-Gill (CPMG, N pulses at t_j = tau * (j - 1/2) / N):
       Cancels linear and quadratic low-frequency drift up to O((omega tau)^6) for even N >= 2.
  3. Uhrig Dynamical Decoupling (UDD_N, N pulses at t_j = tau * sin^2(pi j / (2N + 2))):
       Cancels the first N derivatives of the modulation filter function at omega = 0:
         F_UDD^{(N)}(omega tau) = |1 + (-1)^{N+1} e^{i omega tau} + 2 \sum_{j=1}^N (-1)^j e^{i omega t_j}|^2
                                = O((omega tau)^{2N + 2}),
     achieving high-order suppression of quasistatic 1/f spectator phase drift while commuting
     with instantaneous logical CNOT parity gates synchronized at decoupling nodes.
"""

from __future__ import annotations
import cmath
import math
from typing import Any, Dict, List


def pulse_times_cpmg(num_pulses: int) -> List[float]:
    if num_pulses <= 0:
        return []
    return [(j - 0.5) / float(num_pulses) for j in range(1, num_pulses + 1)]


def pulse_times_udd(num_pulses: int) -> List[float]:
    if num_pulses <= 0:
        return []
    return [math.sin(math.pi * j / float(2 * num_pulses + 2)) ** 2 for j in range(1, num_pulses + 1)]


def evaluate_dd_filter_function(norm_pulse_times: List[float], omega_tau: float) -> float:
    r"""
    Compute the dimensionless filter function F(omega * tau) = |y(omega * tau)|^2 where:
      y(x) = 1 + (-1)^{N+1} e^{i x} + 2 \sum_{j=1}^N (-1)^j e^{i x (t_j / tau)}.
    r"""
    n_pulses = len(norm_pulse_times)
    y_val = 1.0 + ((-1) ** (n_pulses + 1)) * cmath.exp(1j * omega_tau)
    for idx, frac_t in enumerate(norm_pulse_times, start=1):
        y_val += 2.0 * ((-1) ** idx) * cmath.exp(1j * omega_tau * frac_t)
    return float((y_val.real ** 2) + (y_val.imag ** 2))


def compare_fid_cpmg_udd_low_frequency_suppression(
    omega_tau: float = 0.2,
    orders_n: List[int] = [1, 2, 3, 4, 5],
) -> List[Dict[str, float]]:
    fid_val = evaluate_dd_filter_function([], omega_tau)
    rows: List[Dict[str, float]] = []
    for n_ord in orders_n:
        f_cpmg = evaluate_dd_filter_function(pulse_times_cpmg(n_ord), omega_tau)
        f_udd = evaluate_dd_filter_function(pulse_times_udd(n_ord), omega_tau)
        rows.append({
            "num_pulses_n": int(n_ord),
            "omega_tau": float(omega_tau),
            "fid_filter_value": float(fid_val),
            "cpmg_filter_value": float(f_cpmg),
            "udd_filter_value": float(f_udd),
            "udd_over_fid_suppression_ratio": float(f_udd / fid_val) if fid_val > 0 else 0.0,
        })
    return rows


def generate_dcp_floquet_dynamical_decoupling_carr_purcell_udds_carry_filter_certificate() -> Dict[str, Any]:
    """Generate the Subsystem 144 verification certificate."""
    sweep = compare_fid_cpmg_udd_low_frequency_suppression(omega_tau=0.2, orders_n=[1, 2, 3, 4, 5])

    # For N = 1 (Hahn spin echo, t_1 = 0.5), CPMG_1 and UDD_1 coincide exactly at t_1 = sin^2(pi/4) = 0.5
    n1_coincide = abs(sweep[0]["cpmg_filter_value"] - sweep[0]["udd_filter_value"]) < 1e-15

    # For N = 2, CPMG_2 and UDD_2 both have pulse times sin^2(pi/6) = 1/4 and sin^2(2pi/6) = 3/4!
    n2_coincide = abs(sweep[1]["cpmg_filter_value"] - sweep[1]["udd_filter_value"]) < 1e-15

    # For N >= 3 at low frequency omega*tau = 0.2, UDD_N strictly outperforms CPMG_N by cancelling
    # higher Taylor orders O((omega*tau)^{2N+2})
    udd_beats_cpmg_high_order = all(
        row["udd_filter_value"] < row["cpmg_filter_value"] for row in sweep if row["num_pulses_n"] >= 3
    )

    # UDD filter value decreases monotonically with pulse order N at omega*tau = 0.2
    udd_monotone = all(
        sweep[i]["udd_filter_value"] > sweep[i + 1]["udd_filter_value"] for i in range(len(sweep) - 1)
    )

    theorem_checks = {
        "n1_hahn_echo_cpmg_equals_udd_exact": bool(n1_coincide),
        "n2_two_pulse_cpmg_equals_udd_at_quarter_three_quarter": bool(n2_coincide),
        "udd_strictly_outperforms_cpmg_for_n_ge_3_at_low_freq": bool(udd_beats_cpmg_high_order),
        "udd_filter_monotone_decreasing_with_order_n": bool(udd_monotone),
        "udd5_suppresses_low_freq_noise_by_over_12_orders_of_magnitude": bool(
            sweep[-1]["udd_over_fid_suppression_ratio"] < 1e-12
        ),
    }

    return {
        "subsystem_id": "dcp_floquet_dynamical_decoupling_carr_purcell_udds_carry_filter_bridge",
        "subsystem_number": 144,
        "domain": "dynamical_decoupling_filter_functions_cpmg_udd",
        "low_frequency_sweep": sweep,
        "theorem_checks": theorem_checks,
        "all_checks_passed": bool(all(theorem_checks.values())),
        "falsification_status": {
            "accepted_speedup_candidate": False,
            "new_active_negative_result_created": False,
            "novelty_claim": False,
        },
    }
