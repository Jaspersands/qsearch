r"""DCP multi-packet collective Helstrom vs. separable tilted and X-basis decision bridge.

Evaluates distinguishability for M single-qubit
DCP phase packets rho(a_1, s, gamma_1), ..., rho(a_M, s, gamma_M) with arbitrary
(distinct) public headers under binary hypothesis testing H_0: s = 0 vs. H_1: s = s^*,
and proves the exact symmetrization collapse under unknown sign s^* <-> -s^*:

1. Three-Tier Known-Target Decision Hierarchy (Distinct Headers, theta_m = 2*pi*<a_m, s^*>/q):
   For a single informative wire with gamma_m > 0 and sin(theta_m) != 0:
     - Tier 1 (Standard X-Basis Readout):
       Measures each wire in {|+>, |->}, achieving single-wire TV bias:
           Delta_m^{(X)} = gamma_m * (1 - cos(theta_m)) / 2 = gamma_m * sin^2(theta_m / 2).
     - Tier 2 (Known-Target Tilted Separable Helstrom Readout):
       Measures each wire in the eigenbasis of rho(0, gamma_m) - rho(theta_m, gamma_m),
       achieving the strictly larger single-wire Helstrom TV bias:
           Delta_m^{(sep-Hel)} = gamma_m * |sin(theta_m / 2)| > Delta_m^{(X)}
       (a quadratic improvement O(|theta_m|) vs O(theta_m^2) for small angles!).
     - Tier 3 (Collective M-Packet Entangling Helstrom Readout):
       The collective optimum is at least either specified product measurement.
       The two product measurements have NO universal ordering. Local binary
       optimality does not imply optimality after combining multiple outcomes.
       A distinct-header mod64 counterexample is retained in the certificate.
       The strict three-tier hierarchy holds only on the specified controls;
       noncommutation alone does not prove a universal strict collective gain.

2. Single-Copy Dihedral Sign-Symmetrization Collapse (s^* <-> -s^*):
   When the sign of s^* is unknown (so H_1 is the equal mixture 0.5*rho(theta_m, gamma_m)
   + 0.5*rho(-theta_m, gamma_m)), the single-copy sin(theta_m) Y-component cancels
   identically, rendering H_0 and symmetrized H_1 simultaneously diagonal in the X basis
   and collapsing the optimal single-copy Helstrom bias back to Delta_m^{(X)} = gamma_m * sin^2(theta_m / 2).
"""

from __future__ import annotations

import cmath
import hashlib
import itertools
import json
import math
from typing import Any, Dict, List, Sequence


THEOREM_ID = "dcp_multi_packet_collective_helstrom_product_likelihood_bridge"
SCHEMA_VERSION = "dcp-multi-packet-collective-helstrom-product-likelihood-bridge-v1"

ComplexMatrix = List[List[complex]]


def _single_qubit_rho(theta: float, gamma: float) -> ComplexMatrix:
    off = 0.5 * float(gamma) * cmath.exp(-1j * float(theta))
    return [[0.5 + 0j, off], [off.conjugate(), 0.5 + 0j]]


def _kron(a: ComplexMatrix, b: ComplexMatrix) -> ComplexMatrix:
    ra, ca = len(a), len(a[0])
    rb, cb = len(b), len(b[0])
    out: ComplexMatrix = [[0j] * (ca * cb) for _ in range(ra * rb)]
    for i1 in range(ra):
        for j1 in range(ca):
            for i2 in range(rb):
                for j2 in range(cb):
                    out[i1 * rb + i2][j1 * cb + j2] = a[i1][j1] * b[i2][j2]
    return out


def _real_symmetric_eigenvalues_jacobi(mat_real: List[List[float]]) -> List[float]:
    n = len(mat_real)
    a = [[float(mat_real[i][j]) for j in range(n)] for i in range(n)]
    for _ in range(60):
        max_off = 0.0
        for p in range(n):
            for q in range(p + 1, n):
                if abs(a[p][q]) > max_off:
                    max_off = abs(a[p][q])
        if max_off < 1e-15:
            break
        for p in range(n):
            for q in range(p + 1, n):
                apq = a[p][q]
                if abs(apq) < 1e-15:
                    continue
                app, aqq = a[p][p], a[q][q]
                tau = (aqq - app) / (2.0 * apq)
                t = math.copysign(1.0 / (abs(tau) + math.sqrt(1.0 + tau * tau)), tau) if tau != 0.0 else 1.0
                c = 1.0 / math.sqrt(1.0 + t * t)
                s = t * c
                a[p][p] = app - t * apq
                a[q][q] = aqq + t * apq
                a[p][q] = a[q][p] = 0.0
                for k in range(n):
                    if k != p and k != q:
                        akp, akq = a[k][p], a[k][q]
                        a[k][p] = a[p][k] = c * akp - s * akq
                        a[k][q] = a[q][k] = s * akp + c * akq
    return [a[i][i] for i in range(n)]


def _hermitian_trace_distance(rho_a: ComplexMatrix, rho_b: ComplexMatrix) -> float:
    n = len(rho_a)
    real_2n = [[0.0] * (2 * n) for _ in range(2 * n)]
    for i in range(n):
        for j in range(n):
            diff = 0.5 * ((rho_a[i][j] - rho_b[i][j]) + (rho_a[j][i] - rho_b[j][i]).conjugate())
            real_2n[i][j] = real_2n[i + n][j + n] = diff.real
            real_2n[i][j + n] = -diff.imag
            real_2n[i + n][j] = diff.imag
    return 0.25 * sum(abs(ev) for ev in _real_symmetric_eigenvalues_jacobi(real_2n))


def _product_coin_tv_distance(probs_0: Sequence[float], probs_1: Sequence[float]) -> float:
    """Exact total variation distance between two M-coin product Bernoulli distributions."""
    m_len = len(probs_0)
    tv = 0.0
    for bits in itertools.product((0, 1), repeat=m_len):
        p0 = 1.0
        p1 = 1.0
        for j, b in enumerate(bits):
            p0 *= probs_0[j] if b == 0 else (1.0 - probs_0[j])
            p1 *= probs_1[j] if b == 0 else (1.0 - probs_1[j])
        tv += 0.5 * abs(p0 - p1)
    return tv


def evaluate_three_tier_distinct_header_decision_hierarchy(
    thetas: Sequence[float],
    gammas: Sequence[float],
) -> Dict[str, Any]:
    """Compare Tier 1 (X^M), Tier 2 (Separable Tilted Helstrom), and Tier 3 (Collective Helstrom) on M distinct headers."""
    m_packets = len(thetas)
    if not 1 <= m_packets <= 4 or len(gammas) != m_packets:
        raise ValueError("matching length M in [1, 4] required")

    # Build M-packet tensor states for H_0 (all 0) and H_1 (thetas)
    rho_h0 = _single_qubit_rho(0.0, gammas[0])
    rho_h1 = _single_qubit_rho(thetas[0], gammas[0])
    for j in range(1, m_packets):
        rho_h0 = _kron(rho_h0, _single_qubit_rho(0.0, gammas[j]))
        rho_h1 = _kron(rho_h1, _single_qubit_rho(thetas[j], gammas[j]))

    tier3_collective_tv = _hermitian_trace_distance(rho_h0, rho_h1)

    # Tier 2: Separable tilted Helstrom measurement on each wire j has symmetric coin probabilities
    # P(0 | H_0) = (1 + delta_j)/2, P(0 | H_1) = (1 - delta_j)/2 with delta_j = gamma_j * |sin(theta_j / 2)|
    p0_tilted = [0.5 * (1.0 + float(gammas[j]) * abs(math.sin(0.5 * float(thetas[j])))) for j in range(m_packets)]
    p1_tilted = [1.0 - p for p in p0_tilted]
    tier2_sep_helstrom_tv = _product_coin_tv_distance(p0_tilted, p1_tilted)

    # Tier 1: Fixed X-basis measurement on each wire j has P(+ | H_0) = (1 + gamma_j)/2, P(+ | H_1) = (1 + gamma_j*cos(theta_j))/2
    p0_x = [0.5 * (1.0 + float(gammas[j])) for j in range(m_packets)]
    p1_x = [0.5 * (1.0 + float(gammas[j]) * math.cos(float(thetas[j]))) for j in range(m_packets)]
    tier1_x_basis_tv = _product_coin_tv_distance(p0_x, p1_x)

    # Single-copy sign-symmetrized state 0.5*rho(theta_0) + 0.5*rho(-theta_0) vs rho(0):
    th0, gm0 = float(thetas[0]), float(gammas[0])
    r_pos = _single_qubit_rho(th0, gm0)
    r_neg = _single_qubit_rho(-th0, gm0)
    r_sym = [[0.5 * (r_pos[r][c] + r_neg[r][c]) for c in range(2)] for r in range(2)]
    r_zero = _single_qubit_rho(0.0, gm0)
    single_copy_sym_tv = _hermitian_trace_distance(r_zero, r_sym)
    single_copy_x_bias = gm0 * (math.sin(0.5 * th0) ** 2)

    return {
        "M_packets": m_packets,
        "thetas": [float(t) for t in thetas],
        "gammas": [float(g) for g in gammas],
        "tier1_x_basis_tv": tier1_x_basis_tv,
        "tier2_separable_tilted_helstrom_tv": tier2_sep_helstrom_tv,
        "tier3_collective_helstrom_tv": tier3_collective_tv,
        "strict_three_tier_hierarchy_holds": (
            tier3_collective_tv > tier2_sep_helstrom_tv + 1e-4
            and tier2_sep_helstrom_tv > tier1_x_basis_tv + 1e-4
        ) if m_packets >= 2 else (abs(tier3_collective_tv - tier2_sep_helstrom_tv) < 1e-12),
        "single_copy_sign_symmetrized_tv": single_copy_sym_tv,
        "single_copy_x_sin_sq_bias": single_copy_x_bias,
        "sign_symmetrization_collapses_to_x_basis": abs(single_copy_sym_tv - single_copy_x_bias) < 1e-12,
    }


def generate_dcp_multi_packet_collective_helstrom_product_likelihood_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the multi-packet collective Helstrom vs product likelihood bridge."""
    single_packet_audit = evaluate_three_tier_distinct_header_decision_hierarchy(
        thetas=[math.pi / 3.0],
        gammas=[0.85],
    )
    two_packet_distinct_audit = evaluate_three_tier_distinct_header_decision_hierarchy(
        thetas=[math.pi / 3.0, math.pi / 2.0],
        gammas=[0.85, 0.8],
    )
    three_packet_distinct_audit = evaluate_three_tier_distinct_header_decision_hierarchy(
        thetas=[math.pi / 4.0, math.pi / 3.0, 2.0 * math.pi / 3.0],
        gammas=[0.85, 0.8, 0.75],
    )
    reversed_product_order = evaluate_three_tier_distinct_header_decision_hierarchy(
        thetas=[2.0 * math.pi * 16 / 64, 2.0 * math.pi * 17 / 64],
        gammas=[1.0, 1.0],
    )

    all_passed = (
        single_packet_audit["sign_symmetrization_collapses_to_x_basis"]
        and single_packet_audit["tier2_separable_tilted_helstrom_tv"] > single_packet_audit["tier1_x_basis_tv"] + 0.15
        and two_packet_distinct_audit["strict_three_tier_hierarchy_holds"]
        and two_packet_distinct_audit["sign_symmetrization_collapses_to_x_basis"]
        and three_packet_distinct_audit["strict_three_tier_hierarchy_holds"]
        and not reversed_product_order["strict_three_tier_hierarchy_holds"]
        and reversed_product_order["tier1_x_basis_tv"] > reversed_product_order["tier2_separable_tilted_helstrom_tv"]
        and reversed_product_order["tier3_collective_helstrom_tv"] >= reversed_product_order["tier1_x_basis_tv"]
    )

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "proof_status": "LOCAL_DERIVATION_REVIEW_PENDING_NOT_FORMALLY_VERIFIED",
        "scope_constraints": {
            "applies_to": "Binary hypothesis testing H_0: s = 0 vs H_1: s = s^* across M distinct-header DCP phase packets",
            "does_not_claim": "Tilted or single-copy linear-angle bias when s^* is unknown and sign-symmetrized (s^* <-> -s^*)",
            "controls_included": "Includes strict 3-tier hierarchy D_tr^{coll} > D_TV^{sep-Hel} > D_TV^{X^M} on M=2 and M=3 distinct headers, plus exact single-copy collapse to gamma*sin^2(theta/2) under s^* <-> -s^* symmetrization.",
        },
        "single_packet_audit": single_packet_audit,
        "two_packet_distinct_header_audit": two_packet_distinct_audit,
        "three_packet_distinct_header_audit": three_packet_distinct_audit,
        "product_order_counterexample": {"q": 64, "headers": [16, 17], "secret": 1,
                                         "evaluation": reversed_product_order},
        "universal_strict_three_tier_hierarchy_claimed": False,
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
