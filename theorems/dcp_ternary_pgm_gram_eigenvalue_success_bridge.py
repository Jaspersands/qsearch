r"""DCP Pretty Good Measurement (PGM) Gram eigenvalue spectrum and square-root occupancy bridge.

Establishes the exact closed-form eigenvalue spectrum of the Q x Q secret Gram matrix
and the exact Pretty Good Measurement (PGM) secret-recovery success probability for
any single-packet K-wire DCP state |psi_A(s)> = 2^{-K/2} sum_{x in {0,1}^K} exp(2*pi*i * <A x, s> / q) |x>
over Z_q^n (Q = q^n):

1. Exact Abelian Group-Convolution Gram Spectrum:
   Across the Q = q^n uniform secret hypotheses s in Z_q^n, the Q x Q Gram matrix
       G_{s, s'}(A) = <psi_A(s) | psi_A(s')> = 2^{-K} sum_{x in {0,1}^K} exp(2*pi*i * <A x, s' - s> / q)
   is diagonalized by the Q x Q Fourier transform over Z_q^n, with exact eigenvalue at
   dual frequency y in Z_q^n given by the subset-sum occupancy count
       N_A(y) = |{x in {0,1}^K : A x == y (mod q)}|:
       lambda_y(G(A)) = (Q / 2^K) * N_A(y).

2. Exact Square-Root Occupancy Law for PGM Success Probability:
   Because P_{PGM}(A) = (Q^{-1} Tr(sqrt(G(A))))^2, the exact PGM success probability is:
       P_{PGM}(A) = (1 / (2^K * Q)) * ( sum_{y in Z_q^n} sqrt(N_A(y)) )^2.

3. Exact Rank / Cauchy-Schwarz Bound and Flat-Fiber Equality Criterion:
   Let R(A) = |{y in Z_q^n : N_A(y) > 0}| <= min(2^K, Q) be the number of occupied
   subset-sum residues. By Cauchy-Schwarz:
       ( sum_{y in Z_q^n} sqrt(N_A(y)) )^2 <= R(A) * sum_{y in Z_q^n} N_A(y) = R(A) * 2^K,
   yielding the universal upper bound:
       P_{PGM}(A) <= R(A) / Q <= min(1, 2^K / Q),
   with exact equality P_{PGM}(A) == R(A) / Q if and only if N_A(y) is constant across
   all occupied residues y (such as collision-free instances N_A(y) in {0, 1} or flat
   surjective instances N_A(y) == 2^K / Q).
"""

from __future__ import annotations

import cmath
import hashlib
import itertools
import json
import math
from typing import Any, Dict, List, Sequence, Tuple


THEOREM_ID = "dcp_ternary_pgm_gram_eigenvalue_success_bridge"
SCHEMA_VERSION = "dcp-ternary-pgm-gram-eigenvalue-success-bridge-v1"

ComplexMatrix = List[List[complex]]


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


def _hermitian_eigenvalues(mat: ComplexMatrix) -> List[float]:
    n = len(mat)
    real_2n = [[0.0] * (2 * n) for _ in range(2 * n)]
    for i in range(n):
        for j in range(n):
            val = 0.5 * (mat[i][j] + mat[j][i].conjugate())
            real_2n[i][j] = real_2n[i + n][j + n] = val.real
            real_2n[i][j + n] = -val.imag
            real_2n[i + n][j] = val.imag
    ev_2n = sorted(_real_symmetric_eigenvalues_jacobi(real_2n))
    return [0.5 * (ev_2n[2 * i] + ev_2n[2 * i + 1]) for i in range(n)]


def evaluate_pgm_gram_spectrum_and_success_probability(
    a_matrix: Sequence[Sequence[int]],
    q_mod: int,
) -> Dict[str, Any]:
    """Verify exact match between explicit Q x Q Gram matrix eigenvalues/PGM success and subset-sum occupancy counts N_A(y)."""
    if type(q_mod) is not int or q_mod < 2:
        raise ValueError("q_mod must be an integer >= 2")
    n_rows = len(a_matrix)
    k_cols = len(a_matrix[0])
    q_total = q_mod ** n_rows
    if q_total > 16:
        raise ValueError("explicit Q x Q Gram eigensolver capped at Q <= 16")

    all_s = list(itertools.product(range(q_mod), repeat=n_rows))
    all_x = list(itertools.product((0, 1), repeat=k_cols))
    dim_x = 1 << k_cols

    # 1. Compute subset-sum occupancy histogram N_A(y)
    occupancy: Dict[Tuple[int, ...], int] = {y: 0 for y in all_s}
    for x_vec in all_x:
        y_vec = tuple(
            sum(int(a_matrix[i][r]) * x_vec[r] for r in range(k_cols)) % q_mod
            for i in range(n_rows)
        )
        occupancy[y_vec] += 1

    # 2. Construct explicit Q x Q Gram matrix G_{s, s'} = <psi_A(s) | psi_A(s')>
    gram: ComplexMatrix = [[0j] * q_total for _ in range(q_total)]
    for idx_s, s_vec in enumerate(all_s):
        for idx_sp, sp_vec in enumerate(all_s):
            acc = 0j
            for x_vec in all_x:
                dot = sum(
                    int(a_matrix[i][r]) * x_vec[r] * (sp_vec[i] - s_vec[i])
                    for i in range(n_rows)
                    for r in range(k_cols)
                ) % q_mod
                acc += cmath.exp(2j * math.pi * dot / float(q_mod))
            gram[idx_s][idx_sp] = acc / float(dim_x)

    eigvals_exp = sorted(_hermitian_eigenvalues(gram))
    eigvals_cf = sorted((float(q_total) / float(dim_x)) * float(occupancy[y]) for y in all_s)
    max_eig_err = max(abs(a - b) for a, b in zip(eigvals_exp, eigvals_cf))

    # 3. PGM success probability: (Q^{-1} sum_y sqrt(lambda_y))^2 vs (1 / (2^K * Q)) * (sum_y sqrt(N_A(y)))^2
    pgm_prob_from_gram = (sum(math.sqrt(ev if ev > 1e-13 else 0.0) for ev in eigvals_exp) / float(q_total)) ** 2
    sqrt_occ_sum = sum(math.sqrt(float(occupancy[y])) for y in all_s)
    pgm_prob_closed_form = (sqrt_occ_sum ** 2) / float(dim_x * q_total)

    occupied_count = sum(1 for y in all_s if occupancy[y] > 0)
    rank_upper_bound = float(occupied_count) / float(q_total)
    non_zero_counts = {occupancy[y] for y in all_s if occupancy[y] > 0}
    is_flat_on_support = len(non_zero_counts) == 1

    return {
        "n": n_rows,
        "K": k_cols,
        "q_mod": q_mod,
        "Q_group_size": q_total,
        "occupied_residue_count_R": occupied_count,
        "is_flat_on_support": is_flat_on_support,
        "max_gram_eigenvalue_error": max_eig_err,
        "pgm_success_from_gram_spectrum": pgm_prob_from_gram,
        "pgm_success_closed_form": pgm_prob_closed_form,
        "cauchy_schwarz_rank_upper_bound": rank_upper_bound,
        "exact_spectrum_and_pgm_law_verified": (
            max_eig_err < 1e-12
            and abs(pgm_prob_from_gram - pgm_prob_closed_form) < 1e-12
            and pgm_prob_closed_form <= rank_upper_bound + 1e-12
            and (abs(pgm_prob_closed_form - rank_upper_bound) < 1e-12 if is_flat_on_support else (pgm_prob_closed_form < rank_upper_bound - 1e-6))
        ),
    }


def generate_dcp_ternary_pgm_gram_eigenvalue_success_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the PGM Gram eigenvalue and square-root occupancy bridge."""
    # 1. Flat surjective dyadic binary basis control: q = 8, n = 1, K = 3, A = [[1, 2, 4]] -> N_A(y) = 1 for all 8 residues, P_PGM = 1.0!
    flat_surjective_control = evaluate_pgm_gram_spectrum_and_success_probability(
        a_matrix=[[1, 2, 4]],
        q_mod=8,
    )

    # 2. Collision-free under-complete control: q = 8, n = 1, K = 2, A = [[1, 2]] -> N_A(y) in {0, 1} on 4 residues, P_PGM = 4/8 = 0.5!
    collision_free_half_control = evaluate_pgm_gram_spectrum_and_success_probability(
        a_matrix=[[1, 2]],
        q_mod=8,
    )

    # 3. Non-flat colliding instance: q = 8, n = 1, K = 3, A = [[1, 1, 2]] -> N_A(y) = [1, 2, 2, 2, 1, 0, 0, 0] on R = 5 residues:
    # sum sqrt(N_A) = 2*1 + 3*sqrt(2) = 2 + 3*sqrt(2), so P_PGM = (2 + 3*sqrt(2))^2 / 64 < 5/8 = 0.625!
    non_flat_collision_audit = evaluate_pgm_gram_spectrum_and_success_probability(
        a_matrix=[[1, 1, 2]],
        q_mod=8,
    )

    # 4. 2D instance over Z_3^2 (Q = 9, K = 3): A = [[1, 0, 1], [0, 1, 1]] mod 3
    q3_2d_audit = evaluate_pgm_gram_spectrum_and_success_probability(
        a_matrix=[[1, 0, 1], [0, 1, 1]],
        q_mod=3,
    )

    all_passed = (
        flat_surjective_control["exact_spectrum_and_pgm_law_verified"]
        and abs(flat_surjective_control["pgm_success_closed_form"] - 1.0) < 1e-12
        and collision_free_half_control["exact_spectrum_and_pgm_law_verified"]
        and abs(collision_free_half_control["pgm_success_closed_form"] - 0.5) < 1e-12
        and non_flat_collision_audit["exact_spectrum_and_pgm_law_verified"]
        and q3_2d_audit["exact_spectrum_and_pgm_law_verified"]
    )

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "proof_status": "LOCAL_DERIVATION_REVIEW_PENDING_NOT_FORMALLY_VERIFIED",
        "scope_constraints": {
            "applies_to": "Pretty Good Measurement (PGM) Gram spectrum and secret-recovery probability on K-wire DCP states over Z_q^n",
            "does_not_claim": "Efficient gate-level synthesis of the PGM square-root inverse S^{-1/2} without coherent fiber normalization",
            "controls_included": "Includes flat surjective control A=[[1,2,4]] mod 8 (P_PGM = 1.0), collision-free under-complete control A=[[1,2]] mod 8 (P_PGM = 0.5), non-flat collision audit A=[[1,1,2]] mod 8 (strict Cauchy-Schwarz gap P_PGM = 0.6090 < 5/8), and 2D Z_3^2 audit.",
        },
        "flat_surjective_control": flat_surjective_control,
        "collision_free_undercomplete_control": collision_free_half_control,
        "non_flat_collision_audit": non_flat_collision_audit,
        "q3_2d_audit": q3_2d_audit,
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
