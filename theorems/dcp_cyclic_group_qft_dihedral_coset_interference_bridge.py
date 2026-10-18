"""DCP cyclic-group QFT_{2^m} dihedral coset interference and dyadic progression bridge.

Establishes for any m-wire phase state
    |psi(theta_0, ..., theta_{m-1})> = 2^{-m/2} sum_{U=0}^{2^m - 1} exp(i * sum_{j=0}^{m-1} u_j(U) * theta_j) |U>
where U = sum_{j=0}^{m-1} u_j(U) * 2^j in Z_{2^m}:

1. Exact Cyclic QFT_{2^m}^dagger Product Probability Identity:
   Because exp(-2*pi*i * U * K / 2^m) = prod_{j=0}^{m-1} exp(-i * u_j(U) * (2*pi * K / 2^{m-j})),
   the outcome distribution of the cyclic Fourier transform QFT_{2^m}^dagger over K in Z_{2^m}
   factors identically across the m bit positions:
       P_{QFT_{2^m}}(K | theta) = prod_{j=0}^{m-1} cos^2((theta_j / 2) - (pi * K / 2^{m-j})).

2. Dyadic Geometric Progression Peak Criterion vs. Non-Dyadic Dispersion:
   - Constructive Dyadic Progression Control (Kitaev/Shor Phase Estimation Regime):
     P_{QFT_{2^m}}(K_0 | theta) = 1.0 for an integer K_0 in Z_{2^m} if and only if
     theta_j == 2*pi * 2^j * K_0 / 2^m (mod 2*pi) for all j = 0, ..., m - 1
     (so theta_j == 2^j * theta_0 mod 2*pi).
   - Non-Dyadic DCP Wire Regime:
     Because wire j only couples to K mod 2^{m-j} (in particular, the MSB wire j = m - 1
     couples only to K mod 2 via cos^2(theta_{m-1}/2 - pi*K/2)), whenever the independent
     DCP wire phases fail the dyadic doubling relation theta_j == 2^j * theta_0 (mod 2*pi),
     no single cyclic frequency K in Z_{2^m} can simultaneously align all m factors.
"""

from __future__ import annotations

import cmath
import hashlib
import json
import math
from typing import Any, Dict, List, Sequence


THEOREM_ID = "dcp_cyclic_group_qft_dihedral_coset_interference_bridge"
SCHEMA_VERSION = "dcp-cyclic-group-qft-dihedral-coset-interference-bridge-v1"


def cyclic_qft_probabilities_explicit(thetas: Sequence[float]) -> List[float]:
    """Compute P_{QFT_{2^m}}(K) for K = 0, ..., 2^m - 1 by explicit 2^m-dimensional DFT summation."""
    m = len(thetas)
    dim = 1 << m
    amps_u: List[complex] = []
    for u_int in range(dim):
        phase = sum(((u_int >> j) & 1) * float(thetas[j]) for j in range(m))
        amps_u.append(cmath.exp(1j * phase) / math.sqrt(float(dim)))

    probs_k: List[float] = []
    for k_freq in range(dim):
        amp_k = sum(
            amps_u[u_int]
            * cmath.exp(-2j * math.pi * (u_int * k_freq) / float(dim))
            / math.sqrt(float(dim))
            for u_int in range(dim)
        )
        probs_k.append(abs(amp_k) ** 2)
    return probs_k


def cyclic_qft_probabilities_product_formula(thetas: Sequence[float]) -> List[float]:
    """Closed-form product formula prod_{j=0}^{m-1} cos^2(theta_j / 2 - pi * K / 2^{m-j})."""
    m = len(thetas)
    dim = 1 << m
    probs_k: List[float] = []
    for k_freq in range(dim):
        prod_val = 1.0
        for j in range(m):
            angle = 0.5 * float(thetas[j]) - (math.pi * float(k_freq)) / float(1 << (m - j))
            prod_val *= math.cos(angle) ** 2
        probs_k.append(prod_val)
    return probs_k


def verify_cyclic_qft_product_identity_and_peak_criterion(
    thetas: Sequence[float],
) -> Dict[str, Any]:
    """Verify exact agreement between explicit 2^m-point QFT_{2^m} and the bit-wise cosine product law."""
    p_exp = cyclic_qft_probabilities_explicit(thetas)
    p_prod = cyclic_qft_probabilities_product_formula(thetas)
    max_err = max(abs(a - b) for a, b in zip(p_exp, p_prod))
    max_prob = max(p_prod)
    argmax_k = int( max(range(len(p_prod)), key=lambda k: p_prod[k]) )

    return {
        "m": len(thetas),
        "dim_2m": len(p_prod),
        "max_product_formula_error": max_err,
        "max_outcome_probability": max_prob,
        "argmax_K": argmax_k,
        "total_probability_sum": sum(p_prod),
        "exact_product_formula_verified": (
            max_err < 1e-12 and abs(sum(p_prod) - 1.0) < 1e-12
        ),
    }


def generate_dcp_cyclic_group_qft_dihedral_coset_interference_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the cyclic QFT_{2^m} dihedral coset interference bridge."""
    # 1. Constructive dyadic geometric progression control: m = 3 (dim = 8), K_0 = 5
    # theta_j = 2*pi * 2^j * 5 / 8 -> peaks at K = 5 with probability 1.0!
    k0 = 5
    m_ctrl = 3
    dyadic_thetas = [
        2.0 * math.pi * ((1 << j) * k0) / float(1 << m_ctrl) for j in range(m_ctrl)
    ]
    dyadic_constructive_control = verify_cyclic_qft_product_identity_and_peak_criterion(
        dyadic_thetas
    )

    # 2. Non-dyadic equal-phase conflict audit: theta = [pi, pi, pi]
    # For j = 2 (MSB wire), theta_2 = pi requires K odd (cos^2(pi/2 - pi*K/2) = sin^2(pi*K/2) = 1 for odd K).
    # But for K odd, j = 1 has pi*K/4 in {pi/4, 3*pi/4}, so cos^2(pi/2 - pi*K/4) = 1/2, capping max prob at <= 1/2!
    non_dyadic_pi_conflict = verify_cyclic_qft_product_identity_and_peak_criterion(
        [math.pi, math.pi, math.pi]
    )

    # 3. Generic non-dyadic DCP wire phases: theta = [pi/2, 3*pi/4, pi/4]
    generic_non_dyadic_audit = verify_cyclic_qft_product_identity_and_peak_criterion(
        [math.pi / 2.0, 3.0 * math.pi / 4.0, math.pi / 4.0]
    )

    all_passed = (
        dyadic_constructive_control["exact_product_formula_verified"]
        and dyadic_constructive_control["argmax_K"] == k0
        and abs(dyadic_constructive_control["max_outcome_probability"] - 1.0) < 1e-12
        and non_dyadic_pi_conflict["exact_product_formula_verified"]
        and non_dyadic_pi_conflict["max_outcome_probability"] < 0.5
        and generic_non_dyadic_audit["exact_product_formula_verified"]
    )

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "scope_constraints": {
            "applies_to": "Cyclic QFT_{2^m}^dagger readout on m-wire product phase states",
            "does_not_claim": "Failure of QFT_{2^m} when wire phases follow the dyadic progression theta_j = 2^j * theta_0 (mod 2*pi)",
            "controls_included": "Includes both the dyadic geometric progression constructive control (K_0 = 5, P(5) = 1.0) and non-dyadic phase-conflict audits.",
        },
        "dyadic_progression_constructive_control": dyadic_constructive_control,
        "non_dyadic_pi_conflict_audit": non_dyadic_pi_conflict,
        "generic_non_dyadic_audit": generic_non_dyadic_audit,
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
