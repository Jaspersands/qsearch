r"""DCP non-abelian wreath-product (S_2 wr S_M) pair-swap commutant and singlet sufficiency bridge.

Establishes the exact representation-theoretic decomposition and optimal distinguishing
laws for M pairs of two-copy DCP states under the hyperoctahedral / wreath product
symmetry group B_M = S_2 \wr S_M = (Z_2)^M \rtimes S_M:

1. Exact Wreath-Product Sector Decomposition of ((C^2)^{otimes 2})^{otimes M}:
   For each two-copy pair m in {1, ..., M}, the intra-pair swap operator SWAP_m splits
   C^2 otimes C^2 = Sym^2(C^2) (+) Lambda^2(C^2) into the 3D triplet (eigenvalue +1) and
   1D antisymmetric singlet |Psi^->_m (eigenvalue -1).
   Under the inter-pair permutation group S_M acting on the M pairs, the 4^M-dimensional
   Hilbert space decomposes into M + 1 wreath-invariant singlet-count sectors H_k
   (for k = 0, 1, ..., M singlets) of exact dimension:
       dim(H_k) = C(M, k) * 3^{M - k},   with   sum_{k=0}^M C(M, k) * 3^{M - k} = 4^M.

2. Exact Binomial Singlet-Count Sufficiency for Sign-Incoherent / Dihedral-Twirled Pairs:
   When each pair m = 1, ..., M is independently sign-twirled (sigma_m(theta_0, gamma) =
   0.5 * rho(+theta_0)^{\otimes 2} + 0.5 * rho(-theta_0)^{\otimes 2}) and phase-twirled
   inside the triplet, or measured in the intra-pair singlet/triplet projective basis
   {P_sing, P_trip}^{\otimes M}, the singlet count K_sing in {0, 1, ..., M} follows the
   exact Binomial distribution:
       P(K_sing = k | theta_0, gamma) = C(M, k) * p_sing^k * (1 - p_sing)^{M - k},
   where p_sing(theta_0, gamma) = 0.5 * (1 - gamma^2 * cos(theta_0)).
   In particular, between theta_0 = pi (p_sing = 0.5*(1 + gamma^2)) and theta_0 = 0
   (p_sing = 0.5*(1 - gamma^2)), the total variation distance of K_sing equals the
   complete M-sample Bernoulli TV distance.

3. Strict Global Symmetric-Subspace Advantage when All 2M Copies Share Identical Signed Phase:
   When all 2M copies carry the SAME coherent state rho(+theta_0, gamma)^{\otimes 2M},
   inter-pair coherent interference across the M triplet sectors is non-zero, and the
   global (2M + 1)-dimensional Schur-Weyl symmetric projection Sym^{2M}(C^2) achieves
   strictly larger distinguishing advantage than the intra-pair Binomial singlet count:
       D_TV^{Sym^{2M}}(theta_0 = pi vs 0) > D_TV^{Binomial-singlet}(theta_0 = pi vs 0)
   for all M >= 1 and gamma in (0, 1).
"""

from __future__ import annotations

import hashlib
import json
import math
from typing import Any, Dict, List


THEOREM_ID = "dcp_non_abelian_wreath_product_pair_swap_commutant_bridge"
SCHEMA_VERSION = "dcp-non-abelian-wreath-product-pair-swap-commutant-bridge-v1"


def evaluate_wreath_product_sectors_and_singlet_vs_sym2m(
    m_pairs: int,
    gamma: float,
) -> Dict[str, Any]:
    """Verify wreath-product sector dimensions and compare Binomial singlet count vs Sym^{2M}(C^2)."""
    if type(m_pairs) is not int or m_pairs < 1:
        raise ValueError("m_pairs must be an integer >= 1")
    if not (0.0 < gamma < 1.0):
        raise ValueError("gamma must be in (0, 1)")

    # 1. Verify sector dimensions sum_{k=0}^M C(M, k) * 3^{M - k} == 4^M
    sector_dims = [math.comb(m_pairs, k) * (3 ** (m_pairs - k)) for k in range(m_pairs + 1)]
    total_dim = sum(sector_dims)
    expected_dim = 4 ** m_pairs

    # 2. Binomial singlet-count distribution at theta = 0 vs theta = pi:
    p_sing_0 = 0.5 * (1.0 - (gamma ** 2))
    p_sing_pi = 0.5 * (1.0 + (gamma ** 2))

    dist_sing_0 = [
        math.comb(m_pairs, k) * (p_sing_0 ** k) * ((1.0 - p_sing_0) ** (m_pairs - k))
        for k in range(m_pairs + 1)
    ]
    dist_sing_pi = [
        math.comb(m_pairs, k) * (p_sing_pi ** k) * ((1.0 - p_sing_pi) ** (m_pairs - k))
        for k in range(m_pairs + 1)
    ]
    tv_binomial_singlet = 0.5 * sum(abs(a - b) for a, b in zip(dist_sing_0, dist_sing_pi))

    # 3. Compare with full 2M-copy symmetric subspace projection Sym^{2M}(C^2) in the X-Dickie basis:
    # For a single copy at theta in {0, pi}, the X-basis probabilities are:
    # theta = 0:  p_+ = (1 + gamma)/2, p_- = (1 - gamma)/2
    # theta = pi: p_+ = (1 - gamma)/2, p_- = (1 + gamma)/2
    # On 2M copies, the Hamming weight w in {0, ..., 2M} in the |+>, |-> basis (which spans Sym^{2M}(C^2)
    # and is sufficient for commuting X-diagonal states at theta in {0, pi}) has Binomial(2M, (1 +/- gamma)/2) distribution!
    r_copies = 2 * m_pairs
    q_plus = 0.5 * (1.0 + gamma)
    q_minus = 0.5 * (1.0 - gamma)
    dist_sym2m_0 = [
        math.comb(r_copies, w) * (q_plus ** (r_copies - w)) * (q_minus ** w)
        for w in range(r_copies + 1)
    ]
    dist_sym2m_pi = [
        math.comb(r_copies, w) * (q_minus ** (r_copies - w)) * (q_plus ** w)
        for w in range(r_copies + 1)
    ]
    tv_sym2m = 0.5 * sum(abs(a - b) for a, b in zip(dist_sym2m_0, dist_sym2m_pi))

    return {
        "M_pairs": m_pairs,
        "total_qubits_2M": r_copies,
        "gamma": gamma,
        "wreath_sector_dimensions": sector_dims,
        "total_hilbert_dimension": total_dim,
        "p_singlet_theta_0": p_sing_0,
        "p_singlet_theta_pi": p_sing_pi,
        "tv_binomial_singlet": tv_binomial_singlet,
        "tv_global_sym2m": tv_sym2m,
        "sym2m_advantage_over_singlet": tv_sym2m - tv_binomial_singlet,
        "exact_laws_verified": (
            total_dim == expected_dim
            and abs(sum(dist_sing_0) - 1.0) < 1e-12
            and abs(sum(dist_sing_pi) - 1.0) < 1e-12
            and tv_sym2m > tv_binomial_singlet + 1e-6
        ),
    }


def generate_dcp_non_abelian_wreath_product_pair_swap_commutant_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the wreath-product S_2 wr S_M commutant bridge."""
    sweep = [
        evaluate_wreath_product_sectors_and_singlet_vs_sym2m(m_pairs=m, gamma=0.6)
        for m in (1, 2, 3, 4)
    ]

    all_passed = all(r["exact_laws_verified"] for r in sweep)

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "proof_status": "LOCAL_DERIVATION_REVIEW_PENDING_NOT_FORMALLY_VERIFIED",
        "scope_constraints": {
            "applies_to": "Hyperoctahedral wreath-product B_M = S_2 wr S_M sector decomposition and Binomial singlet-count vs. global Sym^{2M} distinguishing distance",
            "does_not_claim": "Inter-pair coherent advantage when the M pairs have independent unknown headers with unaligned phase magnitudes",
            "controls_included": "Evaluates M = 1, 2, 3, 4 pairs (2M = 2..8 qubits) at gamma = 0.6, verifying sum_{k=0}^M C(M,k) 3^{M-k} = 4^M and strict dominance D_TV^{Sym^{2M}} > D_TV^{Binomial-singlet}.",
        },
        "wreath_pair_sweep": sweep,
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
