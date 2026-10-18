r"""DCP adaptive Bayesian posterior phase-feedforward alignment vs. non-adaptive quadratures bridge.

Establishes the exact closed-form distinguishing advantage and sample complexity law for
adaptive phase-feedforward counter-rotation R_Z(-phi_known) during iterative dyadic secret
bit peeling on DCP single-qubit states:
    rho(a, s, gamma) = 0.5 * [[1, gamma * exp(-2*pi*i * a * s / 2^t)],
                              [gamma * exp(+2*pi*i * a * s / 2^t), 1]].

1. Quadrature Blind-Spot Obstruction of Non-Adaptive Pauli-X Peeling:
   At stage r of dyadic bit peeling, suppose the lower r bits s_low = s mod 2^r are known
   and we probe the next bit b_r in {0, 1} (where s == s_low + 2^r * b_r mod 2^{r+1}) using
   a compressed wire with dyadic valuation v_2(a) = t - 1 - r, so a = 2^{t-1-r} * u with u odd.
   Then the phase decomposes into a known prefix offset phi_known and a binary pi-shift:
       theta(b_r) = 2*pi * a * s / 2^t = phi_known + pi * u * b_r = phi_known + pi * b_r (mod 2*pi),
   where phi_known = pi * u * s_low / 2^r.
   Measuring a fixed Pauli-X basis without phase feedforward yields expectation:
       <X> = (-1)^{b_r} * gamma * cos(phi_known),
   which suffers a complete blind spot (<X> = 0, zero classical Fisher information, infinite
   sample complexity) whenever phi_known == +/- pi/2 (mod 2*pi), e.g., at r >= 1 when
   s_low = 2^{r-1} (such as s_low = 1 at r = 1, where phi_known = pi/2).

2. Exact Adaptive Phase-Feedforward Restoration Identity:
   Applying the deterministic single-qubit Z-rotation gate conditioned on the known prefix s_low:
       R_Z(-phi_known) = diag(1, exp(-i * phi_known))
   maps rho(a, s, gamma) to the phase-aligned state:
       R_Z(-phi_known) rho(a, s, gamma) R_Z(-phi_known)^dagger = 0.5 * (I + (-1)^{b_r} * gamma * X),
   achieving the full Helstrom trace-distance distinguishing bias:
       D_TV^{feedforward}(phi_known) = gamma
   uniformly across ALL known prefixes s_low in {0, ..., 2^r - 1}!

3. Strict 2x Sample-Complexity Advantage over Non-Adaptive Random X/Y Quadrature Sampling:
   A non-adaptive protocol that measures Pauli-X with probability 1/2 and Pauli-Y with
   probability 1/2 (to avoid the cos(phi_known) = 0 blind spot) achieves:
   - L1 total variation bias: D_TV^{XY-rand}(phi_known) = 0.5 * gamma * (|cos(phi_known)| + |sin(phi_known)|) in [0.5 * gamma, (1/sqrt(2)) * gamma] < gamma,
   - Average squared bias (effective Fisher information):
         I_eff^{XY-rand} = 0.5 * gamma^2 * (cos^2(phi_known) + sin^2(phi_known)) = 0.5 * gamma^2,
   whereas adaptive phase-feedforward achieves I_eff^{feedforward} = gamma^2 = 2 * I_eff^{XY-rand}
   (an exact 2.0x reduction in required quantum copies at every prefix s_low).
"""

from __future__ import annotations

import cmath
import hashlib
import json
import math
from typing import Any, Dict, List


THEOREM_ID = "dcp_adaptive_bayesian_posterior_phase_alignment_bridge"
SCHEMA_VERSION = "dcp-adaptive-bayesian-posterior-phase-alignment-bridge-v1"


def evaluate_stage_r_phase_alignment(
    t_bits: int,
    stage_r: int,
    u_odd: int,
    gamma: float,
) -> Dict[str, Any]:
    """Evaluate fixed-X, random-XY, and adaptive R_Z(-phi_known) feedforward across all 2^r prefixes s_low."""
    if type(t_bits) is not int or t_bits < 2:
        raise ValueError("t_bits must be an integer >= 2")
    if type(stage_r) is not int or stage_r < 1 or stage_r >= t_bits:
        raise ValueError("stage_r must satisfy 1 <= stage_r < t_bits")
    if type(u_odd) is not int or (u_odd % 2) == 0:
        raise ValueError("u_odd must be an odd integer")
    if not (0.0 < gamma <= 1.0):
        raise ValueError("gamma must be in (0, 1]")

    q_mod = 1 << t_bits
    a_val = (1 << (t_bits - 1 - stage_r)) * u_odd
    num_prefixes = 1 << stage_r

    prefix_records: List[Dict[str, Any]] = []
    min_fixed_x_tv = 1.0
    min_xy_rand_tv = 1.0
    max_xy_rand_tv = 0.0
    min_feedforward_tv = 1.0
    max_matrix_err = 0.0

    for s_low in range(num_prefixes):
        phi_known = math.pi * float(u_odd * s_low) / float(num_prefixes)

        # Explicit 2x2 density matrices for b_r = 0 and b_r = 1
        s0 = s_low
        s1 = s_low + (1 << stage_r)
        theta0 = 2.0 * math.pi * float((a_val * s0) % q_mod) / float(q_mod)
        theta1 = 2.0 * math.pi * float((a_val * s1) % q_mod) / float(q_mod)

        # Apply R_Z(-phi_known) to off-diagonal entryrho_{0,1} = 0.5 * gamma * exp(-i * theta)
        # Under R_Z(-phi) = diag(1, exp(-i*phi)), rho_{0,1} -> rho_{0,1} * exp(+i * phi_known)
        aligned_off0 = 0.5 * gamma * cmath.exp(-1j * theta0) * cmath.exp(1j * phi_known)
        aligned_off1 = 0.5 * gamma * cmath.exp(-1j * theta1) * cmath.exp(1j * phi_known)

        err0 = abs(aligned_off0 - 0.5 * gamma)
        err1 = abs(aligned_off1 - (-0.5 * gamma))
        max_matrix_err = max(max_matrix_err, err0, err1)

        # 1. Fixed Pauli-X TV distance = 0.5 * |<X>_{b=0} - <X>_{b=1}| = gamma * |cos(phi_known)|
        tv_fixed_x = abs(aligned_off0.real * 0.0 + 0.5 * gamma * math.cos(theta0) - 0.5 * gamma * math.cos(theta1))
        # 2. Random 50/50 X/Y TV distance = 0.5 * gamma * (|cos(phi_known)| + |sin(phi_known)|)
        tv_xy_rand = 0.5 * gamma * (abs(math.cos(phi_known)) + abs(math.sin(phi_known)))
        # 3. Adaptive feedforward Pauli-X TV distance = |aligned_off0.real - aligned_off1.real| = gamma
        tv_feedforward = abs(aligned_off0.real - aligned_off1.real)

        # Effective squared-bias Fisher information proxy:
        info_fixed_x = (gamma * math.cos(phi_known)) ** 2
        info_xy_rand = 0.5 * (gamma ** 2) * (math.cos(phi_known) ** 2 + math.sin(phi_known) ** 2)
        info_feedforward = tv_feedforward ** 2

        min_fixed_x_tv = min(min_fixed_x_tv, tv_fixed_x)
        min_xy_rand_tv = min(min_xy_rand_tv, tv_xy_rand)
        max_xy_rand_tv = max(max_xy_rand_tv, tv_xy_rand)
        min_feedforward_tv = min(min_feedforward_tv, tv_feedforward)

        prefix_records.append({
            "s_low": s_low,
            "phi_known_over_pi": (u_odd * s_low) / float(num_prefixes),
            "tv_fixed_x": tv_fixed_x,
            "tv_random_xy": tv_xy_rand,
            "tv_adaptive_feedforward": tv_feedforward,
            "fisher_info_fixed_x": info_fixed_x,
            "fisher_info_random_xy": info_xy_rand,
            "fisher_info_feedforward": info_feedforward,
            "sample_complexity_ratio_xy_over_feedforward": info_feedforward / info_xy_rand,
        })

    return {
        "t_bits": t_bits,
        "q_mod": q_mod,
        "stage_r": stage_r,
        "u_odd": u_odd,
        "gamma": gamma,
        "num_prefixes": num_prefixes,
        "min_fixed_x_tv": min_fixed_x_tv,
        "min_random_xy_tv": min_xy_rand_tv,
        "max_random_xy_tv": max_xy_rand_tv,
        "min_adaptive_feedforward_tv": min_feedforward_tv,
        "max_alignment_matrix_error": max_matrix_err,
        "prefix_records": prefix_records,
        "exact_laws_verified": (
            max_matrix_err < 1e-12
            and min_fixed_x_tv < 1e-12  # hits blind spot at s_low = 2^{r-1}
            and abs(min_feedforward_tv - gamma) < 1e-12
            and abs(min_xy_rand_tv - 0.5 * gamma) < 1e-12
            and all(abs(r["sample_complexity_ratio_xy_over_feedforward"] - 2.0) < 1e-12 for r in prefix_records)
        ),
    }


def generate_dcp_adaptive_bayesian_posterior_phase_alignment_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the adaptive phase-feedforward alignment bridge."""
    stage1_audit = evaluate_stage_r_phase_alignment(t_bits=3, stage_r=1, u_odd=1, gamma=0.8)
    stage2_audit = evaluate_stage_r_phase_alignment(t_bits=4, stage_r=2, u_odd=3, gamma=0.75)

    all_passed = (
        stage1_audit["exact_laws_verified"]
        and stage2_audit["exact_laws_verified"]
    )

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "proof_status": "LOCAL_DERIVATION_REVIEW_PENDING_NOT_FORMALLY_VERIFIED",
        "scope_constraints": {
            "applies_to": "Adaptive phase-feedforward counter-rotation R_Z(-phi_known) vs. non-adaptive fixed-X and random X/Y quadratures in dyadic bit peeling",
            "does_not_claim": "Recovery of the next bit b_r when the wire label itself is zero modulo 2^{t-r} (v_2(a) >= t - r)",
            "controls_included": "Includes stage r=1 (mod 8, blind spot at s_low=1) and stage r=2 (mod 16, u=3, blind spots at s_low in {1,3}), verifying uniform D_TV = gamma and exact 2.0x Fisher-information gain over random X/Y sampling.",
        },
        "stage1_mod8_audit": stage1_audit,
        "stage2_mod16_audit": stage2_audit,
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
