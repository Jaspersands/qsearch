r"""DCP Quantum Singular Value Transformation (QSVT) PGM Chebyshev equalization bridge.

Establishes the exact singular-value spectrum of the subset-sum fiber block encoding and
proves how low-degree odd QSVT polynomials P_d(sigma) boost post-selected and
unconditional QFT secret-recovery probability toward the Pretty Good Measurement (PGM)
optimum on colliding DCP instances:

1. Exact Singular-Value Spectrum of the Subset-Sum Fiber Isometry:
   For a public matrix A in Z_q^{n x K}, let N_A(y) = |{x in {0,1}^K : A x == y (mod q)}|
   be the fiber occupancy of residue y in Z_q^n (Q = q^n), and let N_max = max_y N_A(y).
   The normalized fiber-overlap block encoding has singular values on occupied residues
   y in supp(N_A):
       sigma_y = sqrt(N_A(y) / N_max) in (0, 1],
   with spectral condition number kappa(A) = sqrt(N_max / N_min).

2. Exact QSVT Polynomial Equalization Law:
   Applying a bounded odd QSVT polynomial P_d: [-1, 1] -> [-1, 1] (with P_d(0) = 0 and
   |P_d(sigma)| <= 1 for all sigma in [0, 1]) transforms the normalized fiber amplitude
   from sigma_y to P_d(sigma_y):
   - Conditional (post-selected on QSVT ancilla |0>_anc) QFT secret-recovery probability:
         P_{QFT, cond}(A; P_d) = ( sum_{y: N_A(y) > 0} P_d(sigma_y) )^2 / ( Q * sum_{y: N_A(y) > 0} P_d(sigma_y)^2 ).
   - Specifically:
     * Degree-1 linear identity P_1(sigma) = sigma reproduces the exact Pretty Good
       Measurement probability:
           P_{QFT, cond}(A; P_1) = ( sum_y sqrt(N_A(y)) )^2 / ( Q * 2^K ) = P_{PGM}(A)!
     * Degree-3 concave equalization polynomial P_3(sigma) = 0.5 * sigma * (3 - sigma^2)
       (and degree-5 P_5(sigma) = (1/8) * sigma * (15 - 10*sigma^2 + 3*sigma^4)) flattens
       the singular value disparities sigma_y < 1 toward 1, strictly lifting the
       conditional post-selected QFT success probability ABOVE P_{PGM}(A) toward the
       flat-fiber ceiling R(A) / Q:
           P_{PGM}(A) = P_{QFT, cond}(A; P_1) < P_{QFT, cond}(A; P_3) < P_{QFT, cond}(A; P_5) <= R(A) / Q
       for every non-flat colliding instance!
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from typing import Any, Callable, Dict, List, Sequence, Tuple


THEOREM_ID = "dcp_quantum_singular_value_transformation_pgm_chebyshev_bridge"
SCHEMA_VERSION = "dcp-quantum-singular-value-transformation-pgm-chebyshev-bridge-v1"


def _p1_linear(sigma: float) -> float:
    return sigma


def _p3_equalizer(sigma: float) -> float:
    # Monotone odd degree-3 polynomial on [0, 1] with P_3(0)=0, P_3(1)=1, |P_3(sigma)| <= 1
    return 0.5 * sigma * (3.0 - (sigma ** 2))


def _p5_equalizer(sigma: float) -> float:
    # Monotone odd degree-5 polynomial on [0, 1] with P_5(0)=0, P_5(1)=1, |P_5(sigma)| <= 1
    s2 = sigma ** 2
    return 0.125 * sigma * (15.0 - 10.0 * s2 + 3.0 * (s2 ** 2))


def evaluate_qsvt_fiber_equalization(
    a_matrix: Sequence[Sequence[int]],
    q_mod: int,
) -> Dict[str, Any]:
    """Evaluate exact singular values and QSVT degree-1, 3, 5 post-selected QFT success probabilities."""
    n_rows = len(a_matrix)
    k_cols = len(a_matrix[0])
    q_total = q_mod ** n_rows
    dim_x = 1 << k_cols

    all_s = list(itertools.product(range(q_mod), repeat=n_rows))
    all_x = list(itertools.product((0, 1), repeat=k_cols))

    occupancy: Dict[Tuple[int, ...], int] = {y: 0 for y in all_s}
    for x_vec in all_x:
        y_vec = tuple(
            sum(int(a_matrix[i][r]) * x_vec[r] for r in range(k_cols)) % q_mod
            for i in range(n_rows)
        )
        occupancy[y_vec] += 1

    non_zero_counts = [occupancy[y] for y in all_s if occupancy[y] > 0]
    occupied_r = len(non_zero_counts)
    n_max = max(non_zero_counts)
    n_min = min(non_zero_counts)
    kappa = math.sqrt(float(n_max) / float(n_min))
    is_flat = (n_max == n_min)

    sigmas = [math.sqrt(float(c) / float(n_max)) for c in non_zero_counts]

    def _eval_poly(poly_fn: Callable[[float], float]) -> Dict[str, float]:
        vals = [poly_fn(s) for s in sigmas]
        sum_v = sum(vals)
        sum_v2 = sum(v * v for v in vals)
        # Acceptance probability relative to maximally occupied normalization N_max / 2^K:
        p_acc = (float(n_max) / float(dim_x)) * (sum_v2 / float(occupied_r))
        p_cond_qft = (sum_v ** 2) / (float(q_total) * sum_v2)
        return {
            "conditional_qft_success": p_cond_qft,
            "normalized_acceptance_weight": p_acc,
            "max_boundedness_val": max(abs(v) for v in vals),
        }

    res_p1 = _eval_poly(_p1_linear)
    res_p3 = _eval_poly(_p3_equalizer)
    res_p5 = _eval_poly(_p5_equalizer)

    pgm_closed = ((sum(math.sqrt(float(c)) for c in non_zero_counts)) ** 2) / float(dim_x * q_total)
    rank_ceiling = float(occupied_r) / float(q_total)

    return {
        "n": n_rows,
        "K": k_cols,
        "q_mod": q_mod,
        "Q_group_size": q_total,
        "occupied_residue_count_R": occupied_r,
        "n_min": n_min,
        "n_max": n_max,
        "condition_number_kappa": kappa,
        "is_flat_support": is_flat,
        "pgm_baseline_prob": pgm_closed,
        "rank_ceiling_R_over_Q": rank_ceiling,
        "deg1_linear": res_p1,
        "deg3_qsvt": res_p3,
        "deg5_qsvt": res_p5,
        "exact_hierarchy_verified": (
            abs(res_p1["conditional_qft_success"] - pgm_closed) < 1e-12
            and res_p3["max_boundedness_val"] <= 1.0 + 1e-12
            and res_p5["max_boundedness_val"] <= 1.0 + 1e-12
            and (
                abs(res_p1["conditional_qft_success"] - rank_ceiling) < 1e-12
                if is_flat
                else (
                    res_p1["conditional_qft_success"]
                    < res_p3["conditional_qft_success"]
                    < res_p5["conditional_qft_success"]
                    <= rank_ceiling + 1e-12
                )
            )
        ),
    }


def generate_dcp_quantum_singular_value_transformation_pgm_chebyshev_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the QSVT PGM Chebyshev equalization bridge."""
    # 1. Non-flat colliding instance: A = [[1, 1, 2]] mod 8 (N_A in {1, 2}, R = 5, Q = 8 -> ceiling 5/8 = 0.625)
    colliding_mod8 = evaluate_qsvt_fiber_equalization([[1, 1, 2]], q_mod=8)

    # 2. High-disparity colliding instance: A = [[1, 1, 1, 2]] mod 8 (N_A in {1, 3, 4}, R = 6, Q = 8 -> ceiling 6/8 = 0.75)
    high_disparity_mod8 = evaluate_qsvt_fiber_equalization([[1, 1, 1, 2]], q_mod=8)

    # 3. Flat surjective control: A = [[1, 2, 4]] mod 8 (N_A = 1 for all 8 residues -> all degrees give 1.0!)
    flat_control_mod8 = evaluate_qsvt_fiber_equalization([[1, 2, 4]], q_mod=8)

    all_passed = (
        colliding_mod8["exact_hierarchy_verified"]
        and high_disparity_mod8["exact_hierarchy_verified"]
        and flat_control_mod8["exact_hierarchy_verified"]
    )

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "proof_status": "LOCAL_DERIVATION_REVIEW_PENDING_NOT_FORMALLY_VERIFIED",
        "scope_constraints": {
            "applies_to": "Odd-polynomial QSVT singular-value equalization P_d(sigma) on subset-sum fiber block encodings over Z_q^n",
            "does_not_claim": "Efficient implementation of the reflection around the subset-sum fiber support without coherent collision-finding",
            "controls_included": "Includes A=[[1,1,2]] mod 8 (P_1=0.6089 < P_3=0.6227 < P_5=0.6246 < 5/8=0.625), high-disparity A=[[1,1,1,2]] mod 8, and flat control A=[[1,2,4]] mod 8 (P_1=P_3=P_5=1.0).",
        },
        "colliding_mod8_audit": colliding_mod8,
        "high_disparity_mod8_audit": high_disparity_mod8,
        "flat_control_mod8": flat_control_mod8,
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
