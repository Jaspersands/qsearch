r"""DCP multi-copy distinct-header cyclic-swap and Schur-Weyl bipartite even-flip interference bridge.

Establishes for r copies of single-qubit DCP phase states with arbitrary (distinct or matched)
public headers a_1, ..., a_r in Z_q^n, phase angles theta_j = 2*pi * <a_j, s> / q, and
visibilities gamma_1, ..., gamma_r in [0, 1]:

1. Exact Bipartite Even-Flip Cycle Expansion for the r-Cycle Permutation C_r = (1 2 ... r):
   Because every closed walk x_1 -> x_2 -> ... -> x_r -> x_1 on the two-element basis {0, 1}
   must alternate 0 -> 1 and 1 -> 0 an EVEN number of times 2m (0 <= 2m <= r), the r-cycle
   expectation Tr(C_r (rho_1 tensor ... tensor rho_r)) = Tr(rho_1 rho_2 ... rho_r) is strictly
   real and expands exclusively over even-sized alternating index subsets
   1 <= j_1 < k_1 < ... < j_m < k_m <= r:
       Tr(C_r (rho_1 tensor ... tensor rho_r))
           = 2^{-(r - 1)} * [ 1 + sum_{m=1}^{floor(r / 2)} sum_{j_1 < k_1 < ... < j_m < k_m}
                              (prod_{l=1}^m gamma_{j_l} gamma_{k_l}) cos(sum_{l=1}^m (theta_{j_l} - theta_{k_l})) ].

2. Universal Balanced-Difference Degree Ceiling (deg <= floor(r / 2)) & Sign Invariance:
   Since every permutation pi in S_r decomposes into disjoint cycles whose lengths sum to r,
   and every Schur-Weyl projector Pi_lambda (and permutation-invariant observable in C[S_r])
   is a linear combination of permutations pi in S_r:
     - Every Fourier harmonic appearing in Tr(Pi_lambda (rho_1 tensor ... tensor rho_r)) is a
       zero-sum balanced difference of at most floor(r / 2) header pairs:
           sum_{l=1}^m (a_{j_l} - a_{k_l}) mod q,   m <= floor(r / 2).
     - All Schur-Weyl sector probabilities Tr(Pi_lambda (rho_1 tensor ... tensor rho_r)) are
       strictly invariant under global secret negation s -> -s mod q for all r >= 1.
     - Odd-Copy Degree Collapse (r = 3): Because floor(3 / 2) = 1, both the 3-cycle trace
       Tr(C_3 (rho_1 tensor rho_2 tensor rho_3)) and the 3-copy symmetric subspace projection
       probability
           Tr(Pi_{Sym^3} (rho_1 tensor rho_2 tensor rho_3))
               = (1 / 2) + (1 / 6) * sum_{1 <= j < k <= 3} gamma_j gamma_k cos(theta_j - theta_k)
       contain ZERO 3-body phase correlations and depend exclusively on pairwise differences
       theta_j - theta_k (matching the uniform average of 2-copy swap tests over the 3 pairs).

3. Constructive Escape via Weight-Changing CNOT / GHZ Readout:
   Unlike permutation operators pi in S_r (which preserve computational Hamming weight wt(x)),
   conjugating by CNOT / Hadamard gates mixes Hamming weights 0 and r, enabling the r-qubit
   GHZ parity observable X^{tensor r} to access the full degree-r sum cos(theta_1 + ... + theta_r)
   (via signed even-Y Pauli combinations or CNOT-star readout).
"""

from __future__ import annotations

import cmath
import hashlib
import itertools
import json
import math
from typing import Any, Dict, List, Sequence, Tuple


THEOREM_ID = "dcp_multicopy_distinct_header_cyclic_swap_interference_bridge"
SCHEMA_VERSION = "dcp-multicopy-distinct-header-cyclic_swap-interference-bridge-v1"

ComplexMatrix = List[List[complex]]


def _single_qubit_rho(theta: float, gamma: float) -> ComplexMatrix:
    if not math.isfinite(theta) or not math.isfinite(gamma) or not 0.0 <= gamma <= 1.0:
        raise ValueError("finite theta and gamma in [0, 1] required")
    off = 0.5 * gamma * cmath.exp(-1j * theta)
    return [[0.5 + 0j, off], [off.conjugate(), 0.5 + 0j]]


def _matmul_2x2(a: ComplexMatrix, b: ComplexMatrix) -> ComplexMatrix:
    return [
        [a[0][0] * b[0][0] + a[0][1] * b[1][0], a[0][0] * b[0][1] + a[0][1] * b[1][1]],
        [a[1][0] * b[0][0] + a[1][1] * b[1][0], a[1][0] * b[0][1] + a[1][1] * b[1][1]],
    ]


def cyclic_shift_trace_explicit_tensor(
    thetas: Sequence[float],
    gammas: Sequence[float],
) -> complex:
    """Compute Tr(C_r (rho_1 tensor ... tensor rho_r)) by explicit 2^r basis summation <x_2,...,x_r,x_1 | rho_{1..r} | x_1,...,x_r>."""
    r = len(thetas)
    if r < 2 or len(gammas) != r or r > 7:
        raise ValueError("matching length r in [2, 7] required")
    rhos = [_single_qubit_rho(float(th), float(gm)) for th, gm in zip(thetas, gammas)]
    total = 0j
    for x in itertools.product((0, 1), repeat=r):
        prod_val = 1.0 + 0j
        for j in range(r):
            x_in = x[j]
            x_out = x[(j + 1) % r]
            prod_val *= rhos[j][x_out][x_in]
        total += prod_val
    return total


def cyclic_shift_trace_matrix_product(
    thetas: Sequence[float],
    gammas: Sequence[float],
) -> complex:
    """Compute Tr(rho_1 * rho_2 * ... * rho_r) via 2x2 matrix multiplication."""
    r = len(thetas)
    if r < 2 or len(gammas) != r:
        raise ValueError("matching length r >= 2 required")
    acc = _single_qubit_rho(float(thetas[0]), float(gammas[0]))
    for j in range(1, r):
        acc = _matmul_2x2(acc, _single_qubit_rho(float(thetas[j]), float(gammas[j])))
    return acc[0][0] + acc[1][1]


def cyclic_shift_trace_bipartite_even_flip_closed_form(
    thetas: Sequence[float],
    gammas: Sequence[float],
) -> float:
    """Closed-form bipartite even-flip expansion over 2m-element subsets S subseteq {0, ..., r-1}."""
    r = len(thetas)
    if r < 2 or len(gammas) != r:
        raise ValueError("matching length r >= 2 required")
    acc = 1.0
    for m in range(1, (r // 2) + 1):
        for indices in itertools.combinations(range(r), 2 * m):
            gamma_prod = 1.0
            angle_diff = 0.0
            for l_idx in range(m):
                j_idx = indices[2 * l_idx]
                k_idx = indices[2 * l_idx + 1]
                gamma_prod *= float(gammas[j_idx]) * float(gammas[k_idx])
                angle_diff += float(thetas[j_idx]) - float(thetas[k_idx])
            acc += gamma_prod * math.cos(angle_diff)
    return acc / float(1 << (r - 1))


def verify_cyclic_shift_bipartite_even_flip_identity(
    thetas: Sequence[float],
    gammas: Sequence[float],
) -> Dict[str, Any]:
    """Verify exact equality between 2^r tensor trace, 2x2 product trace, and bipartite even-flip closed form, plus s -> -s invariance."""
    exp_tensor = cyclic_shift_trace_explicit_tensor(thetas, gammas)
    exp_matprod = cyclic_shift_trace_matrix_product(thetas, gammas)
    cf_val = cyclic_shift_trace_bipartite_even_flip_closed_form(thetas, gammas)
    neg_tensor = cyclic_shift_trace_explicit_tensor([-float(th) for th in thetas], gammas)

    max_err = max(
        abs(exp_tensor - cf_val),
        abs(exp_matprod - cf_val),
        abs(exp_tensor.imag),
        abs(exp_tensor - neg_tensor),
    )

    return {
        "r_copies": len(thetas),
        "max_pair_degree_floor_r_over_2": len(thetas) // 2,
        "explicit_tensor_trace_real": exp_tensor.real,
        "explicit_tensor_trace_imag": exp_tensor.imag,
        "matrix_product_trace_real": exp_matprod.real,
        "bipartite_even_flip_closed_form": cf_val,
        "negated_secret_trace_real": neg_tensor.real,
        "max_identity_and_sign_error": max_err,
        "exact_even_flip_law_verified": max_err < 1e-12,
    }


def verify_three_copy_distinct_header_symmetric_projection_pairwise_law(
    thetas: Sequence[float],
    gammas: Sequence[float],
) -> Dict[str, Any]:
    """Verify that for r=3 distinct headers, Tr(Pi_{Sym^3}(rho_1 tensor rho_2 tensor rho_3)) reduces strictly to 2-body pairwise differences."""
    if len(thetas) != 3 or len(gammas) != 3:
        raise ValueError("r=3 thetas and gammas required")
    rhos = [_single_qubit_rho(float(th), float(gm)) for th, gm in zip(thetas, gammas)]

    # Explicit 8x8 density matrix rho_123 in computational basis {0..7}
    rho_123: ComplexMatrix = [[0j] * 8 for _ in range(8)]
    for x in range(8):
        x0, x1, x2 = (x >> 2) & 1, (x >> 1) & 1, x & 1
        for y in range(8):
            y0, y1, y2 = (y >> 2) & 1, (y >> 1) & 1, y & 1
            rho_123[x][y] = rhos[0][x0][y0] * rhos[1][x1][y1] * rhos[2][x2][y2]

    # Explicit 8x8 projector Pi_{Sym^3} from the 4 Dicke states |D_0>, |D_1>, |D_2>, |D_3>
    pi_sym3: ComplexMatrix = [[0j] * 8 for _ in range(8)]
    for w in range(4):
        norm = float(math.comb(3, w))
        for x in range(8):
            if bin(x).count("1") != w:
                continue
            for y in range(8):
                if bin(y).count("1") == w:
                    pi_sym3[x][y] += 1.0 / norm

    prob_explicit = sum(pi_sym3[i][k] * rho_123[k][i] for i in range(8) for k in range(8)).real

    # Pairwise 2-body closed form: 1/2 + (1/6) * sum_{j<k} gamma_j * gamma_k * cos(theta_j - theta_k)
    pairwise_sum = (
        float(gammas[0]) * float(gammas[1]) * math.cos(float(thetas[0]) - float(thetas[1]))
        + float(gammas[1]) * float(gammas[2]) * math.cos(float(thetas[1]) - float(thetas[2]))
        + float(gammas[0]) * float(gammas[2]) * math.cos(float(thetas[0]) - float(thetas[2]))
    )
    prob_pairwise_cf = 0.5 + pairwise_sum / 6.0

    # Check invariance under common shift theta_j -> theta_j + delta (proving zero sensitivity to theta_1 + theta_2 + theta_3)
    delta_shift = 0.91
    shifted_thetas = [float(th) + delta_shift for th in thetas]
    rhos_shifted = [_single_qubit_rho(th, float(gm)) for th, gm in zip(shifted_thetas, gammas)]
    prob_shifted = 0.0
    for w in range(4):
        norm = float(math.comb(3, w))
        for x in range(8):
            if bin(x).count("1") != w:
                continue
            x0, x1, x2 = (x >> 2) & 1, (x >> 1) & 1, x & 1
            for y in range(8):
                if bin(y).count("1") == w:
                    y0, y1, y2 = (y >> 2) & 1, (y >> 1) & 1, y & 1
                    prob_shifted += (
                        rhos_shifted[0][x0][y0] * rhos_shifted[1][x1][y1] * rhos_shifted[2][x2][y2]
                    ).real / norm

    # Contrast with weight-changing CNOT/GHZ observable O_{GHZ}^{(3)} = |000><111| + |111><000|, which accesses cos(theta_1 + theta_2 + theta_3)
    ghz_sum_exp = (rho_123[0][7] + rho_123[7][0]).real
    ghz_sum_cf = 0.25 * float(gammas[0]) * float(gammas[1]) * float(gammas[2]) * math.cos(
        float(thetas[0]) + float(thetas[1]) + float(thetas[2])
    )

    return {
        "thetas": [float(th) for th in thetas],
        "gammas": [float(gm) for gm in gammas],
        "sym3_prob_explicit_8x8": prob_explicit,
        "sym3_prob_pairwise_closed_form": prob_pairwise_cf,
        "sym3_prob_under_common_phase_shift": prob_shifted,
        "pairwise_formula_error": abs(prob_explicit - prob_pairwise_cf),
        "common_shift_invariance_error": abs(prob_explicit - prob_shifted),
        "weight_changing_ghz_sum_harmonic_explicit": ghz_sum_exp,
        "weight_changing_ghz_sum_harmonic_closed_form": ghz_sum_cf,
        "three_body_sum_absent_in_sym3_projector_verified": (
            abs(prob_explicit - prob_pairwise_cf) < 1e-12
            and abs(prob_explicit - prob_shifted) < 1e-12
            and abs(ghz_sum_exp - ghz_sum_cf) < 1e-12
        ),
    }


def generate_dcp_multicopy_distinct_header_cyclic_swap_interference_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the multi-copy distinct-header cyclic-swap interference bridge."""
    cycle_audits = [
        verify_cyclic_shift_bipartite_even_flip_identity(
            thetas=[0.3, 1.1],
            gammas=[0.85, 0.75],
        ),
        verify_cyclic_shift_bipartite_even_flip_identity(
            thetas=[0.2, 0.9, 2.1],
            gammas=[0.9, 0.8, 0.7],
        ),
        verify_cyclic_shift_bipartite_even_flip_identity(
            thetas=[0.15, 0.85, 1.75, 2.65],
            gammas=[0.9, 0.85, 0.8, 0.75],
        ),
        verify_cyclic_shift_bipartite_even_flip_identity(
            thetas=[0.1, 0.7, 1.4, 2.2, 2.9],
            gammas=[0.9, 0.85, 0.8, 0.75, 0.7],
        ),
    ]

    r3_sym_audit = verify_three_copy_distinct_header_symmetric_projection_pairwise_law(
        thetas=[0.25, 1.15, 2.35],
        gammas=[0.9, 0.8, 0.7],
    )

    all_passed = (
        all(a["exact_even_flip_law_verified"] for a in cycle_audits)
        and r3_sym_audit["three_body_sum_absent_in_sym3_projector_verified"]
    )

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "proof_status": "LOCAL_DERIVATION_REVIEW_PENDING_NOT_FORMALLY_VERIFIED",
        "scope_constraints": {
            "applies_to": "r-cycle permutation traces Tr(C_r (rho_1 tensor ... tensor rho_r)) and Schur-Weyl sector projectors Pi_lambda on distinct headers",
            "does_not_claim": "Absence of r-fold sum harmonics in weight-changing CNOT/GHZ circuits outside the permutation algebra C[S_r]",
            "controls_included": "Includes exact bipartite even-flip cycle expansion across r = 2, 3, 4, 5, exact r=3 symmetric projection reduction to 2-body pairwise differences (common-phase-shift invariance), and constructive contrast with the weight-changing GHZ sum observable.",
        },
        "cyclic_shift_even_flip_audits": cycle_audits,
        "three_copy_symmetric_pairwise_audit": r3_sym_audit,
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
