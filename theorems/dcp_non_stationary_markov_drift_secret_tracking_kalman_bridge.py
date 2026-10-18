r"""DCP non-stationary drifting secret tracking via cross-packet CNOT velocity locking bridge.

Establishes the exact Dirichlet dephasing collapse of naive time-averaged measurements
when a DCP secret drifts linearly across time steps (s^{(t)} = (s_0 + t * delta) mod q),
and proves how cross-packet CNOT difference gates (Subsystem 94) between adjacent
packets (t, t + 1) lock onto the time-invariant velocity delta and restore 100% coherent
alignment with the initial secret s_0:

1. Exact Dirichlet Dephasing Collapse of Static Time-Averaging Under Drift:
   Suppose a sequence of T quantum packets at time steps t = 0, 1, ..., T - 1 carries a
   drifting secret s^{(t)} = (s_0 + t * delta) mod q on a survivor wire with label a.
   Averaging direct Pauli-X measurements across the T steps without drift compensation
   yields the time-averaged expectation:
       mu_static(T) = (1 / T) sum_{t=0}^{T-1} gamma * cos(2*pi * a * (s_0 + t * delta) / q).
   Whenever T is a multiple of the drift period P_drift = q / gcd(a * delta, q) (with
   a * delta != 0 mod q), character orthogonality forces:
       mu_static(T) == 0.0   for ALL initial secrets s_0 in Z_q!

2. Time-Invariant Velocity Extraction via Adjacent-Packet Cross-CNOT:
   Applying a cross-packet CNOT gate between packet t and packet t + 1 (Subsystem 94) on
   the Z-target outcome b = 1 (difference branch) prepares the time-invariant phase state
   with phase angle:
       theta_diff = 2*pi * a * (s^{(t+1)} - s^{(t)}) / q = 2*pi * a * delta / q (mod 2*pi),
   whose Pauli-X expectation is constant across ALL time steps t and ALL initial secrets s_0:
       <X>_{diff}^{(t)} = gamma^2 * cos(2*pi * a * delta / q)!
   Once delta is estimated, applying the adaptive time-indexed counter-rotation
   R_Z(-2*pi * a * t * delta / q) to each packet t aligns every packet to the static
   initial phase 2*pi * a * s_0 / q, restoring constant time-averaged visibility:
       mu_tracked(T) = gamma * cos(2*pi * a * s_0 / q)   for all T >= 1!
"""

from __future__ import annotations

import cmath
import hashlib
import json
import math
from typing import Any, Dict, List


THEOREM_ID = "dcp_non_stationary_markov_drift_secret_tracking_kalman_bridge"
SCHEMA_VERSION = "dcp-non-stationary-markov-drift-secret-tracking-kalman-bridge-v1"


def evaluate_drifting_secret_velocity_locking(
    q_mod: int,
    a_label: int,
    s0_initial: int,
    delta_drift: int,
    gamma: float = 0.9,
) -> Dict[str, Any]:
    """Compare static time-averaging vs adjacent-packet cross-CNOT velocity locking and R_Z counter-rotation."""
    step_gcd = math.gcd(a_label * delta_drift, q_mod)
    t_period = q_mod // step_gcd
    if t_period < 2:
        raise ValueError("a_label * delta_drift must be non-zero mod q_mod")

    static_x_series: List[float] = []
    velocity_diff_x_series: List[float] = []
    tracked_x_series: List[float] = []

    for t_step in range(t_period):
        s_t = (s0_initial + t_step * delta_drift) % q_mod
        s_next = (s0_initial + (t_step + 1) * delta_drift) % q_mod

        theta_t = 2.0 * math.pi * float((a_label * s_t) % q_mod) / float(q_mod)
        theta_next = 2.0 * math.pi * float((a_label * s_next) % q_mod) / float(q_mod)

        # 1. Static uncompensated Pauli-X expectation at step t:
        static_x_series.append(gamma * math.cos(theta_t))

        # 2. Adjacent-packet cross-CNOT b=1 difference branch expectation between t and t+1:
        # Off-diagonal entry of b=1 branch is 0.5 * gamma^2 * exp(-i * (theta_next - theta_t))
        off_diff = 0.5 * (gamma ** 2) * cmath.exp(-1j * (theta_next - theta_t))
        velocity_diff_x_series.append(2.0 * off_diff.real)

        # 3. Velocity-compensated R_Z(-2*pi * a * t * delta / q) expectation at step t:
        phi_drift_t = 2.0 * math.pi * float((a_label * t_step * delta_drift) % q_mod) / float(q_mod)
        off_tracked = 0.5 * gamma * cmath.exp(-1j * theta_t) * cmath.exp(1j * phi_drift_t)
        tracked_x_series.append(2.0 * off_tracked.real)

    mean_static_x = sum(static_x_series) / float(t_period)
    mean_velocity_diff_x = sum(velocity_diff_x_series) / float(t_period)
    mean_tracked_x = sum(tracked_x_series) / float(t_period)

    expected_velocity_x = (gamma ** 2) * math.cos(2.0 * math.pi * float((a_label * delta_drift) % q_mod) / float(q_mod))
    expected_s0_x = gamma * math.cos(2.0 * math.pi * float((a_label * s0_initial) % q_mod) / float(q_mod))

    max_vel_var = max(abs(v - expected_velocity_x) for v in velocity_diff_x_series)
    max_track_var = max(abs(v - expected_s0_x) for v in tracked_x_series)

    return {
        "q_mod": q_mod,
        "a_label": a_label,
        "s0_initial": s0_initial,
        "delta_drift": delta_drift,
        "drift_period_T": t_period,
        "gamma": gamma,
        "static_time_averaged_x": mean_static_x,
        "adjacent_cnot_velocity_x": mean_velocity_diff_x,
        "expected_velocity_x": expected_velocity_x,
        "velocity_tracked_time_averaged_x": mean_tracked_x,
        "expected_initial_s0_x": expected_s0_x,
        "max_velocity_step_deviation": max_vel_var,
        "max_tracked_step_deviation": max_track_var,
        "exact_drift_tracking_verified": (
            abs(mean_static_x) < 1e-12
            and max_vel_var < 1e-12
            and max_track_var < 1e-12
        ),
    }


def generate_dcp_non_stationary_markov_drift_secret_tracking_kalman_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the non-stationary drifting secret tracking bridge."""
    # 1. Unit drift delta = 1 mod 8, s_0 = 0, a = 1 -> static average over T = 8 steps is 0.0, while tracked average is +gamma = +0.9!
    unit_drift_mod8 = evaluate_drifting_secret_velocity_locking(
        q_mod=8, a_label=1, s0_initial=0, delta_drift=1, gamma=0.9
    )

    # 2. Even drift delta = 2 mod 16, s_0 = 8 (pi phase -> cos = -1), a = 1 -> static average over T = 8 steps is 0.0, tracked is -0.9!
    even_drift_mod16 = evaluate_drifting_secret_velocity_locking(
        q_mod=16, a_label=1, s0_initial=8, delta_drift=2, gamma=0.9
    )

    all_passed = (
        unit_drift_mod8["exact_drift_tracking_verified"]
        and abs(unit_drift_mod8["velocity_tracked_time_averaged_x"] - 0.9) < 1e-12
        and even_drift_mod16["exact_drift_tracking_verified"]
        and abs(even_drift_mod16["velocity_tracked_time_averaged_x"] - (-0.9)) < 1e-12
    )

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "proof_status": "LOCAL_DERIVATION_REVIEW_PENDING_NOT_FORMALLY_VERIFIED",
        "scope_constraints": {
            "applies_to": "Time-varying drifting secret s^{(t)} = (s_0 + t * delta) mod q velocity extraction via adjacent-packet CNOTs and R_Z counter-rotation",
            "does_not_claim": "Coherent tracking when each packet has an independent unstructured random shift delta_t with zero autocorrelation",
            "controls_included": "Evaluates delta=1 mod 8 (s_0=0, static avg 0.0 vs tracked +0.9) and delta=2 mod 16 (s_0=8, static avg 0.0 vs tracked -0.9), verifying time-invariant velocity extraction.",
        },
        "unit_drift_mod8_audit": unit_drift_mod8,
        "even_drift_mod16_audit": even_drift_mod16,
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
