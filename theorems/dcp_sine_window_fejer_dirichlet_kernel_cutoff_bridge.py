"""DCP sine-window three-point Dirichlet kernel decomposition and first-lobe survival bridge.

Establishes for the discrete sine-window state on z in {0, ..., P - 1} (P >= 2)
with squared amplitudes w_sin(z) = (2 / P) * sin^2(pi * (z + 1/2) / P)
and centered Dirichlet kernel D_P(phi) = (1 / P) * sum_{z=0}^{P-1} exp(i * phi * (z - (P - 1)/2)):

1. Exact Unit Normalization and Three-Dirichlet-Kernel Decomposition:
   Using sin^2(pi*(z + 1/2)/P) = (1 + cos(2*pi*(z - (P - 1)/2)/P)) / 2, the centered
   characteristic function tilde_gamma_sin(phi; P) = sum_{z=0}^{P-1} w_sin(z) exp(i * phi * (z - (P - 1)/2))
   satisfies the exact closed-form identity for all phi in R:
       tilde_gamma_sin(phi; P) = D_P(phi) + (1 / 2) * D_P(phi + 2*pi / P) + (1 / 2) * D_P(phi - 2*pi / P).

2. Constructive First-Dirichlet-Zero Survival Control (phi = +/- 2*pi / P):
   At the first zero phi_1 = 2*pi / P of the flat box window where D_P(2*pi / P) = 0,
   the sine window retains exact survival:
       tilde_gamma_sin(2*pi / P; P) = (1 / 2) * D_P(0) + (1 / 2) * D_P(4*pi / P)
                                    = 1 / 2  (for all P >= 3, since D_P(4*pi / P) = 0).

3. Sidelobe Suppression Beyond the Main Lobe (phi = 2*pi * m / P):
   At every harmonic multiple phi_m = 2*pi * m / P with 2 <= m <= P - 2, all three
   Dirichlet kernels D_P(2*pi*m/P), D_P(2*pi*(m+1)/P), and D_P(2*pi*(m-1)/P) vanish
   simultaneously, yielding exact zero leakage tilde_gamma_sin(2*pi * m / P; P) = 0,
   Cubic decay is a PRINCIPAL-PERIOD bound, not an unrestricted real-frequency
   bound: write delta=dist(phi, 2*pi*Z) in [0,pi]. For P>=4 and
   4*pi/P <= delta <= pi, |tilde_gamma| <= 2*sin^2(pi/P)/(P*sin^3(delta/2))
   <= 2*pi^5/(P*delta)^3. Magnitudes are 2*pi-periodic; aliased main lobes
   survive at arbitrarily large |phi|. In particular P8,phi=2*pi*7.5/8
   ENHANCES the box magnitude, contradicting the former unqualified claim.
"""

from __future__ import annotations

import cmath
import hashlib
import json
import math
from typing import Any, Dict, List, Sequence


THEOREM_ID = "dcp_sine_window_fejer_dirichlet_kernel_cutoff_bridge"
SCHEMA_VERSION = "dcp-sine-window-fejer-dirichlet-kernel-cutoff-bridge-v2"


def _validate_window(phi: float, p_window: int) -> None:
    if type(p_window) is not int or p_window < 2 or not math.isfinite(phi):
        raise ValueError("finite phi and integer P>=2 required")


def principal_sidelobe_bound(phi: float, p_window: int) -> Dict[str, Any]:
    """Analytic bound evaluated in floats; not an interval-arithmetic certificate.

    With x=delta/2,d=pi/P, the three-kernel identity gives magnitude ratio
    (1-cos d)*(1+cos d-sin^2 x)/(sin^2 x-sin^2 d). In this range,
    sin^2 x >= sin^2(2d) >= 2 sin^2 d, so the denominator >= sin^2 x/2.
    Multiply by |D|<=1/(P sin x), then sin x>=delta/pi.
    """
    _validate_window(phi, p_window)
    delta = abs(math.remainder(phi, 2 * math.pi))
    if p_window < 4 or delta < 4 * math.pi / p_window:
        return {"principal_distance": delta, "sidelobe_bound_applies": False, "upper_bound": 1.0}
    upper = 2 * math.sin(math.pi / p_window) ** 2 / (p_window * math.sin(delta / 2) ** 3)
    return {"principal_distance": delta, "sidelobe_bound_applies": True, "upper_bound": min(1.0, upper)}


def centered_dirichlet_kernel(phi: float, p_window: int) -> float:
    """Compute D_P(phi) = (1/P) sum_{z=0}^{P-1} exp(i * phi * (z - (P-1)/2))."""
    _validate_window(phi, p_window)
    half = 0.5 * float(p_window - 1)
    val = sum(
        cmath.exp(1j * float(phi) * (float(z) - half)) for z in range(p_window)
    ) / float(p_window)
    return val.real


def centered_sine_characteristic_explicit(phi: float, p_window: int) -> float:
    """Compute tilde_gamma_sin(phi; P) by explicit summation over z = 0, ..., P - 1."""
    _validate_window(phi, p_window)
    half = 0.5 * float(p_window - 1)
    total = 0j
    for z in range(p_window):
        w_z = (2.0 / float(p_window)) * (
            math.sin(math.pi * (float(z) + 0.5) / float(p_window)) ** 2
        )
        total += w_z * cmath.exp(1j * float(phi) * (float(z) - half))
    return total.real


def centered_sine_characteristic_three_dirichlet(phi: float, p_window: int) -> float:
    """Closed-form three-Dirichlet-kernel combination D_P(phi) + 0.5*D_P(phi + 2*pi/P) + 0.5*D_P(phi - 2*pi/P)."""
    _validate_window(phi, p_window)
    step = 2.0 * math.pi / float(p_window)
    return (
        centered_dirichlet_kernel(phi, p_window)
        + 0.5 * centered_dirichlet_kernel(phi + step, p_window)
        + 0.5 * centered_dirichlet_kernel(phi - step, p_window)
    )


def verify_sine_window_three_dirichlet_identity_and_controls(
    p_window: int,
    test_phis: Sequence[float],
) -> Dict[str, Any]:
    """Verify unit normalization, three-Dirichlet identity, first-zero survival 1/2, and sidelobe suppression."""
    _validate_window(0.0, p_window)
    if p_window < 6:
        raise ValueError("the chosen 2.5-harmonic sidelobe control requires P>=6")
    norm_sum = centered_sine_characteristic_explicit(0.0, p_window)
    max_three_dirichlet_err = 0.0
    for phi in test_phis:
        exp_val = centered_sine_characteristic_explicit(phi, p_window)
        cf_val = centered_sine_characteristic_three_dirichlet(phi, p_window)
        err = abs(exp_val - cf_val)
        if err > max_three_dirichlet_err:
            max_three_dirichlet_err = err

    # Constructive control at phi_1 = 2*pi / P: box kernel is 0.0, sine kernel is 0.5 (for P >= 3)
    phi_1 = 2.0 * math.pi / float(p_window)
    box_at_phi_1 = centered_dirichlet_kernel(phi_1, p_window)
    sine_at_phi_1 = centered_sine_characteristic_explicit(phi_1, p_window)

    # Sidelobe comparison at phi_{2.5} = 2*pi * 2.5 / P
    phi_sidelobe = 2.0 * math.pi * 2.5 / float(p_window)
    box_sidelobe_abs = abs(centered_dirichlet_kernel(phi_sidelobe, p_window))
    sine_sidelobe_abs = abs(centered_sine_characteristic_explicit(phi_sidelobe, p_window))

    return {
        "P": p_window,
        "normalization_sum": norm_sum,
        "max_three_dirichlet_formula_error": max_three_dirichlet_err,
        "box_at_first_harmonic_2pi_over_P": box_at_phi_1,
        "sine_at_first_harmonic_2pi_over_P": sine_at_phi_1,
        "box_sidelobe_2_5_abs": box_sidelobe_abs,
        "sine_sidelobe_2_5_abs": sine_sidelobe_abs,
        "sidelobe_suppratio_sine_over_box": sine_sidelobe_abs / box_sidelobe_abs,
        "exact_identity_and_controls_verified": (
            abs(norm_sum - 1.0) < 1e-12
            and max_three_dirichlet_err < 1e-12
            and abs(box_at_phi_1) < 1e-12
            and abs(sine_at_phi_1 - 0.5) < 1e-12
            and sine_sidelobe_abs < 0.25 * box_sidelobe_abs
        ),
    }


def generate_dcp_sine_window_fejer_dirichlet_kernel_cutoff_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the sine-window three-Dirichlet kernel bridge."""
    test_grid = [0.0, 0.15, 0.37, 0.82, 1.41, 2.19]
    audits = [
        verify_sine_window_three_dirichlet_identity_and_controls(p_window=8, test_phis=test_grid),
        verify_sine_window_three_dirichlet_identity_and_controls(p_window=16, test_phis=test_grid),
    ]

    all_passed = all(a["exact_identity_and_controls_verified"] for a in audits)
    alias_phi = 2 * math.pi * 7.5 / 8
    alias_control = {
        "P": 8, "phi": alias_phi,
        "principal_distance": principal_sidelobe_bound(alias_phi, 8)["principal_distance"],
        "box_magnitude": abs(centered_dirichlet_kernel(alias_phi, 8)),
        "sine_magnitude": abs(centered_sine_characteristic_explicit(alias_phi, 8)),
        "is_a_principal_sidelobe": False,
    }
    principal_controls = []
    for p in (8, 16):
        for j in range(17):
            phi = 4 * math.pi / p + (math.pi - 4 * math.pi / p) * j / 16
            record = principal_sidelobe_bound(phi, p)
            principal_controls.append({"P": p, "phi": phi, **record,
                                       "native_magnitude": abs(centered_sine_characteristic_explicit(phi, p))})
    all_passed = (all_passed and alias_control["sine_magnitude"] > alias_control["box_magnitude"]
                  and all(c["native_magnitude"] <= c["upper_bound"] + 1e-12 for c in principal_controls))
    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "proof_status": "LOCAL_DERIVATION_REVIEW_PENDING_NOT_FORMALLY_VERIFIED",
        "v1_unrestricted_sidelobe_suppression_retracted": True,
        "aliased_main_lobe_counterexample": alias_control,
        "principal_period_bound_controls": principal_controls,
        "scope_constraints": {
            "applies_to": "Centered Fourier / characteristic function of the discrete sine window w_sin(z) = (2/P)*sin^2(pi*(z+1/2)/P)",
            "does_not_claim": "Zero survival inside the main lobe |phi| <= 2*pi / P",
            "controls_included": "Includes both the constructive first-harmonic survival control (tilde_gamma_sin(2*pi/P) = 0.5 where D_P(2*pi/P) = 0) and high-harmonic sidelobe suppression.",
        },
        "window_audits": audits,
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
