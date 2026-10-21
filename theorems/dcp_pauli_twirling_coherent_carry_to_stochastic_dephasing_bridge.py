r"""DCP Pauli/sign twirling conversion of coherent carry error to stochastic dephasing bridge.

Establishes the exact quadratic suppression of worst-case diamond / trace distance when
a coherent residual carry phase error R_Z(delta) = diag(1, exp(i * delta)) on a CNOT
survivor wire is randomized via Pauli-X / sign twirling (averaging +delta and -delta
with equal weight 1/2 across symmetric syndrome branches):

1. Linear Worst-Case Trace Distance of Coherent Carry Errors:
   An uncompensated coherent phase error U_delta = diag(1, exp(i * delta)) acting on
   |+> = (|0> + |1>)/sqrt(2) produces |psi(delta)> = (|0> + exp(i * delta)|1>)/sqrt(2),
   whose trace distance from the ideal state |+><+| is:
       D_tr^{coherent}(delta) = sqrt(1 - |<+ | psi(delta)>|^2) = |sin(delta / 2)| = O(|delta|).

2. Exact Quadratic Suppression Under Pauli-X / Sign Twirling:
   Conjugating the coherent error channel E_delta(rho) = U_delta rho U_delta^dagger by
   {I, X} with probability 1/2 each (or averaging across balanced +/- delta syndrome
   branches) yields the twirled channel:
       E_bar_delta(rho) = 0.5 * U_{+delta} rho U_{+delta}^dagger + 0.5 * U_{-delta} rho U_{-delta}^dagger
                        = cos^2(delta / 2) * rho + sin^2(delta / 2) * Z rho Z!
   Because the off-diagonal imaginary skew +/- i * sin(delta/2)*cos(delta/2) * (Z rho - rho Z)
   cancels identically, the worst-case trace distance from the identity channel drops
   from |sin(delta / 2)| to its square:
       D_tr^{twirled}(delta) = sin^2(delta / 2) = (D_tr^{coherent}(delta))^2 = O(delta^2)!
   At delta = 0.10 rad, this reduces trace-distance error from 0.049979 to 0.002498
   (an exact 1 / |sin(delta/2)| > 20.0x error suppression)!
"""

from __future__ import annotations

import cmath
import hashlib
import json
import math
from typing import Any, Dict, List


THEOREM_ID = "dcp_pauli_twirling_coherent_carry_to_stochastic_dephasing_bridge"
SCHEMA_VERSION = "dcp-pauli-twirling-coherent-carry-to-stochastic-dephasing-bridge-v1"


def _trace_distance_2x2_hermitian(a: List[List[complex]], b: List[List[complex]]) -> float:
    """Compute exact trace distance 0.5 * Tr|A - B| for 2x2 Hermitian matrices with Tr(A - B) = 0."""
    # For a traceless 2x2 Hermitian matrix D = [[d_00, d_01], [d_01*, -d_00]],
    # its eigenvalues are +/- sqrt(d_00^2 + |d_01|^2), so 0.5 * Tr|D| = sqrt(d_00^2 + |d_01|^2)!
    d00 = (a[0][0] - b[0][0]).real
    d01 = a[0][1] - b[0][1]
    return math.sqrt((d00 ** 2) + (abs(d01) ** 2))


def evaluate_coherent_vs_pauli_twirled_carry_error(
    delta_values: List[float],
) -> Dict[str, Any]:
    """Compare explicit 2x2 density-matrix trace distances of coherent vs {I, X}-twirled carry errors."""
    rho_ideal = [[0.5 + 0j, 0.5 + 0j], [0.5 + 0j, 0.5 + 0j]]
    records: List[Dict[str, Any]] = []

    for delta in delta_values:
        ph_pos = cmath.exp(-1j * delta)
        ph_neg = cmath.exp(1j * delta)

        rho_coh = [[0.5 + 0j, 0.5 * ph_pos], [0.5 * ph_neg, 0.5 + 0j]]
        # {I, X}-twirled state: 0.5 * rho(+delta) + 0.5 * X rho(+delta) X = 0.5 * rho(+delta) + 0.5 * rho(-delta)
        rho_twirl = [
            [0.5 + 0j, 0.25 * (ph_pos + ph_neg)],
            [0.25 * (ph_neg + ph_pos), 0.5 + 0j],
        ]

        d_coh_exp = _trace_distance_2x2_hermitian(rho_coh, rho_ideal)
        d_twirl_exp = _trace_distance_2x2_hermitian(rho_twirl, rho_ideal)

        d_coh_cf = abs(math.sin(0.5 * delta))
        d_twirl_cf = math.sin(0.5 * delta) ** 2

        suppression_ratio = (d_coh_cf / d_twirl_cf) if d_twirl_cf > 0.0 else float("inf")

        records.append({
            "delta_rad": delta,
            "coherent_trace_distance_explicit": d_coh_exp,
            "coherent_trace_distance_closed_form": d_coh_cf,
            "twirled_trace_distance_explicit": d_twirl_exp,
            "twirled_trace_distance_closed_form": d_twirl_cf,
            "error_suppression_ratio_coh_over_twirl": suppression_ratio,
            "exact_squaring_law_verified": (
                abs(d_coh_exp - d_coh_cf) < 1e-12
                and abs(d_twirl_exp - d_twirl_cf) < 1e-12
                and abs(d_twirl_cf - (d_coh_cf ** 2)) < 1e-12
            ),
        })

    return {
        "records": records,
        "all_verified": all(r["exact_squaring_law_verified"] for r in records),
    }


def generate_dcp_pauli_twirling_coherent_carry_to_stochastic_dephasing_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the Pauli twirling coherent-to-stochastic carry error bridge."""
    sweep = evaluate_coherent_vs_pauli_twirled_carry_error(
        delta_values=[0.02, 0.05, 0.10, 0.25, math.pi / 2.0, math.pi]
    )

    rec_01 = sweep["records"][2]  # delta = 0.10 rad -> >20.0x suppression!
    rec_pi = sweep["records"][5]  # delta = pi rad -> sin(pi/2) = 1.0, both equal 1.0!

    all_passed = (
        sweep["all_verified"]
        and rec_01["error_suppression_ratio_coh_over_twirl"] > 20.0
        and abs(rec_pi["coherent_trace_distance_explicit"] - 1.0) < 1e-12
        and abs(rec_pi["twirled_trace_distance_explicit"] - 1.0) < 1e-12
    )

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "proof_status": "LOCAL_DERIVATION_REVIEW_PENDING_NOT_FORMALLY_VERIFIED",
        "scope_constraints": {
            "applies_to": "Pauli-X / sign twirling conversion of coherent phase carry errors U_delta into stochastic Z-dephasing channels",
            "does_not_claim": "Reduction of the real cosine expectation attenuation 1 - cos(delta) = 2*sin^2(delta/2)",
            "controls_included": "Evaluates delta in {0.02, 0.05, 0.10, 0.25, pi/2, pi}, verifying exact squaring law D_tr^{twirled} = (D_tr^{coherent})^2 = sin^2(delta/2) and >20.0x trace-distance suppression at delta = 0.10 rad.",
        },
        "twirling_carry_sweep": sweep,
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
