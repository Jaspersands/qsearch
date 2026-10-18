"""DCP multi-packet product-twirl statistical query (SQ) dimension and sign-ambiguity audit.

Establishes for T independent product-twirled DCP packets with survival gamma in [0, 1]
and single-packet conditional bit law
    P_gamma(y | a, s) = 1/2 + (1/2)*(1 - 2*y)*gamma*cos(2*pi*<a, s>/q):

1. Exact Global Sign Indistinguishability:
   Because cos(2*pi*<a, s>/q) == cos(2*pi*<a, -s>/q) for all a in Z_q^n, the T-packet
   joint distribution P_{s}^{tensor T} is identical for s and -s mod q
   (TV distance == 0 and KL divergence == 0 for all T >= 1).

2. Cosine Character Orthogonality & Unordered-Pair SQ Dimension over Random Headers:
   Over uniform headers a ~ Unif(Z_q^n), the normalized density profiles
   phi_s(a) = cos(2*pi*<a, s>/q) satisfy:
     - E_a[phi_s(a) * phi_{s'}(a)] = 0 whenever s != +/- s' mod q,
     - E_a[phi_s(a)^2] = 1 if 2*s == 0 mod q, and 1/2 if 2*s != 0 mod q,
     - Single-packet chi-square divergence chi^2(P_s || P_0) = gamma^2 * E_a[phi_s(a)^2].
   Thus the family of non-zero unordered shift pairs {[s] = {s, -s} : s != 0} is
   mutually orthogonal in L^2(Unif(Z_q^n)) with exact orthogonal family size:
     - (q^n - 1) / 2 for odd q,
     - 2^n - 1 + (q^n - 2^n) / 2 for even q.

3. Scoped Known-Basis Constructive Control:
   If headers are chosen deterministically along standard basis vectors a^{(i)} = e_i
   rather than drawn uniformly from Z_q^n, then E[1 - 2*y | a = e_i] = gamma*cos(2*pi*s_i/q),
   recovering cos(2*pi*s_i/q) coordinate-by-coordinate in O(n / gamma^2) samples.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from typing import Any, Dict, List, Sequence, Tuple


THEOREM_ID = "dcp_multi_packet_product_twirl_sq_dimension_audit"
SCHEMA_VERSION = "dcp-multi-packet-product-twirl-sq-dimension-audit-v1"


def cosine_profile(a_vec: Sequence[int], s_vec: Sequence[int], q: int) -> float:
    """Compute phi_s(a) = cos(2*pi * <a, s> / q)."""
    dot = sum(int(a_vec[i]) * int(s_vec[i]) for i in range(len(a_vec))) % q
    return math.cos(2.0 * math.pi * dot / float(q))


def verify_cosine_character_orthogonality_and_sq_dimension(
    q: int,
    n: int,
    gamma: float,
) -> Dict[str, Any]:
    """Verify exact orthogonality across distinct unordered pairs {s, -s} and exact chi-square divergence."""
    all_vectors = list(itertools.product(range(q), repeat=n))
    total_a = float(len(all_vectors))

    # Partition non-zero shifts into unordered pairs {s, -s mod q}
    visited = set()
    unordered_representatives: List[Tuple[int, ...]] = []
    two_torsion_count = 0
    non_two_torsion_pair_count = 0

    for s in all_vectors:
        if all(x == 0 for x in s):
            continue
        if s in visited:
            continue
        neg_s = tuple((-x) % q for x in s)
        visited.add(s)
        visited.add(neg_s)
        unordered_representatives.append(s)
        if s == neg_s:
            two_torsion_count += 1
        else:
            non_two_torsion_pair_count += 1

    # Verify global sign invariance between s and -s
    max_sign_asymmetry = 0.0
    for s in unordered_representatives:
        neg_s = tuple((-x) % q for x in s)
        for a in all_vectors:
            diff = abs(cosine_profile(a, s, q) - cosine_profile(a, neg_s, q))
            if diff > max_sign_asymmetry:
                max_sign_asymmetry = diff

    # Verify pairwise orthogonality across distinct unordered representatives
    max_off_diagonal_inner_product = 0.0
    max_norm_formula_err = 0.0
    max_chi_square_err = 0.0

    for idx_i, s_i in enumerate(unordered_representatives):
        neg_s_i = tuple((-x) % q for x in s_i)
        expected_norm_sq = 1.0 if s_i == neg_s_i else 0.5
        actual_norm_sq = (
            sum(cosine_profile(a, s_i, q) ** 2 for a in all_vectors) / total_a
        )
        err_norm = abs(actual_norm_sq - expected_norm_sq)
        if err_norm > max_norm_formula_err:
            max_norm_formula_err = err_norm

        # Exact single-packet chi-square divergence chi^2(P_{s_i} || P_0) over uniform a and y in {0,1}
        chi_sq = 0.0
        for a in all_vectors:
            c_val = cosine_profile(a, s_i, q)
            for y in (0, 1):
                p_sy = (1.0 / total_a) * (0.5 + 0.5 * (1 - 2 * y) * gamma * c_val)
                p_0y = (1.0 / total_a) * 0.5
                chi_sq += ((p_sy - p_0y) ** 2) / p_0y
        err_chi = abs(chi_sq - (gamma ** 2) * expected_norm_sq)
        if err_chi > max_chi_square_err:
            max_chi_square_err = err_chi

        for idx_j in range(idx_i + 1, len(unordered_representatives)):
            s_j = unordered_representatives[idx_j]
            ip = (
                sum(
                    cosine_profile(a, s_i, q) * cosine_profile(a, s_j, q)
                    for a in all_vectors
                )
                / total_a
            )
            if abs(ip) > max_off_diagonal_inner_product:
                max_off_diagonal_inner_product = abs(ip)

    if q % 2 == 1:
        expected_sq_dim = ((q ** n) - 1) // 2
    else:
        expected_sq_dim = (2 ** n) - 1 + ((q ** n) - (2 ** n)) // 2

    return {
        "q": q,
        "n": n,
        "gamma": gamma,
        "unordered_nonzero_pair_count": len(unordered_representatives),
        "expected_orthogonal_sq_dimension": expected_sq_dim,
        "two_torsion_nonzero_count": two_torsion_count,
        "non_two_torsion_pair_count": non_two_torsion_pair_count,
        "max_sign_asymmetry": max_sign_asymmetry,
        "max_off_diagonal_inner_product": max_off_diagonal_inner_product,
        "max_norm_formula_error": max_norm_formula_err,
        "max_chi_square_formula_error": max_chi_square_err,
        "exact_orthogonality_and_chi_square_verified": (
            len(unordered_representatives) == expected_sq_dim
            and max_sign_asymmetry < 1e-12
            and max_off_diagonal_inner_product < 1e-12
            and max_norm_formula_err < 1e-12
            and max_chi_square_err < 1e-12
        ),
    }


def verify_known_basis_header_constructive_control(
    q: int,
    s_vec: Sequence[int],
    gamma: float,
) -> Dict[str, Any]:
    """Verify that deterministic standard-basis headers a^{(i)} = e_i directly read out gamma*cos(2*pi*s_i/q)."""
    n = len(s_vec)
    biases = []
    exact_match = True
    for i in range(n):
        e_i = [1 if j == i else 0 for j in range(n)]
        p_y0 = 0.5 + 0.5 * gamma * cosine_profile(e_i, s_vec, q)
        p_y1 = 0.5 - 0.5 * gamma * cosine_profile(e_i, s_vec, q)
        expected_z = p_y0 - p_y1
        target_z = gamma * math.cos(2.0 * math.pi * int(s_vec[i]) / float(q))
        if abs(expected_z - target_z) > 1e-12:
            exact_match = False
        biases.append(expected_z)

    return {
        "q": q,
        "n": n,
        "gamma": gamma,
        "basis_header_biases": biases,
        "constructive_basis_readout_exact": exact_match,
    }


def generate_dcp_multi_packet_product_twirl_sq_dimension_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the multi-packet product-twirl SQ dimension audit."""
    audits = [
        verify_cosine_character_orthogonality_and_sq_dimension(q=4, n=2, gamma=0.5),
        verify_cosine_character_orthogonality_and_sq_dimension(q=5, n=2, gamma=0.4),
    ]
    basis_control = verify_known_basis_header_constructive_control(
        q=8, s_vec=[1, 3, 4], gamma=0.5
    )

    all_passed = (
        all(a["exact_orthogonality_and_chi_square_verified"] for a in audits)
        and basis_control["constructive_basis_readout_exact"]
    )

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "scope_constraints": {
            "applies_to": "Product-twirled single-coordinate DCP observations over uniform random headers a ~ Unif(Z_q^n)",
            "does_not_claim": "Hardness under chosen/deterministic basis headers a = e_i or joint un-twirled multi-copy quantum measurements",
            "controls_included": "Includes both uniform-header orthogonal cosine-pair SQ dimension and chosen-header standard-basis constructive readout.",
        },
        "uniform_header_sq_audits": audits,
        "chosen_basis_header_control": basis_control,
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
