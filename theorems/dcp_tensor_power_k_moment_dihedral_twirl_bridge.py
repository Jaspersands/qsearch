r"""DCP r-copy secret-twirled tensor-power density matrix and ternary kernel moment bridge.

Establishes the exact structure of the secret-twirled r-copy DCP density operator
    bar_rho^{(r)}(A) = E_{s ~ Unif(Z_q^n)}[rho(a_1, s, gamma_1) tensor ... tensor rho(a_r, s, gamma_r)]
for any modulus q >= 2 (both dyadic 2^t and odd prime p), any headers A = [a_1, ..., a_r]
in Z_q^{n x r}, and any visibilities gamma_1, ..., gamma_r in [0, 1]:

1. Exact Ternary Zero-Sum Matrix Element Law:
   In the r-qubit computational basis {|x> : x in {0, 1}^r}, for any pair (x, y) with
   ternary difference vector delta(x, y) = y - x in {-1, 0, +1}^r:
       <x | bar_rho^{(r)}(A) | y>
           = 2^{-r} * (prod_{j : x_j != y_j} gamma_j) * 1[A * (y - x) == 0 (mod q)].
   Consequently, the exact Frobenius-norm distance squared from the maximally mixed
   state I_{2^r} / 2^r is governed by the ternary zero-sum relation enumerator:
       ||bar_rho^{(r)}(A) - I_{2^r} / 2^r||_F^2
           = 2^{-r} * sum_{0 != delta in {-1, 0, +1}^r : A delta == 0 (mod q)} prod_{j : delta_j != 0} (gamma_j^2 / 2).
   In particular, bar_rho^{(r)}(A) == I_{2^r} / 2^r (complete multi-copy secret-twirl
   erasure) holds if and only if A admits NO non-trivial ternary zero-sum relation
   A delta == 0 (mod q) with delta in {-1, 0, +1}^r \ {0^r} (for gamma_j > 0).

2. Universal Unit-Entry Exact Ensemble Moment Identity Across All Moduli q >= 2:
   Because every non-zero entry of delta in {-1, 0, +1}^r \ {0^r} is +/- 1, which is a
   multiplicative unit modulo EVERY integer q >= 2 (with zero zero-divisor exceptions
   even when q = 2^t), P_{A ~ Unif(Z_q^{n x r})}[A delta == 0 (mod q)] == q^{-n} holds
   identically for all 3^r - 1 non-zero ternary vectors delta!
   Summing prod_{j : delta_j != 0} (gamma_j^2 / 2) over {-1, 0, +1}^r yields the exact
   closed-form ensemble Frobenius identity for all q >= 2, n >= 1, r >= 1:
       E_{A ~ Unif(Z_q^{n x r})}[||bar_rho^{(r)}(A) - I_{2^r} / 2^r||_F^2]
           = (prod_{j=1}^r (1 + gamma_j^2) - 1) / (2^r * q^n).
"""

from __future__ import annotations

import cmath
import hashlib
import itertools
import json
import math
from typing import Any, Dict, List, Sequence, Tuple


THEOREM_ID = "dcp_tensor_power_k_moment_dihedral_twirl_bridge"
SCHEMA_VERSION = "dcp-tensor-power-k-moment-dihedral-twirl-bridge-v1"


def secret_twirled_density_matrix_explicit(
    a_cols: Sequence[Sequence[int]],
    q_mod: int,
    gammas: Sequence[float],
) -> List[List[complex]]:
    """Compute E_{s in Z_q^n}[rho(a_1, s, gamma_1) tensor ... tensor rho(a_r, s, gamma_r)] by explicit sum over s."""
    r = len(a_cols)
    n = len(a_cols[0])
    if len(gammas) != r or q_mod < 2:
        raise ValueError("matching r and q_mod >= 2 required")
    dim = 1 << r
    accum = [[0j] * dim for _ in range(dim)]
    all_s = list(itertools.product(range(q_mod), repeat=n))
    inv_q_n = 1.0 / float(len(all_s))
    inv_2_r = 1.0 / float(dim)

    all_x = list(itertools.product((0, 1), repeat=r))
    for s_vec in all_s:
        thetas = [
            2.0 * math.pi * (sum(int(a_cols[j][i]) * s_vec[i] for i in range(n)) % q_mod) / float(q_mod)
            for j in range(r)
        ]
        for idx_x, x_vec in enumerate(all_x):
            for idx_y, y_vec in enumerate(all_x):
                val = inv_2_r + 0j
                for j in range(r):
                    if x_vec[j] != y_vec[j]:
                        diff = y_vec[j] - x_vec[j]
                        val *= float(gammas[j]) * cmath.exp(-1j * diff * thetas[j])
                accum[idx_x][idx_y] += inv_q_n * val
    return accum


def ternary_zero_sum_frobenius_distance_sq_closed_form(
    a_cols: Sequence[Sequence[int]],
    q_mod: int,
    gammas: Sequence[float],
) -> float:
    r"""Compute ||bar_rho^{(r)}(A) - I_{2^r}/2^r||_F^2 via the ternary zero-sum enumerator over delta in {-1, 0, +1}^r \ {0^r}."""
    r = len(a_cols)
    n = len(a_cols[0])
    acc = 0.0
    for delta in itertools.product((-1, 0, 1), repeat=r):
        if all(d == 0 for d in delta):
            continue
        is_zero_sum = all(
            (sum(delta[j] * int(a_cols[j][i]) for j in range(r)) % q_mod) == 0
            for i in range(n)
        )
        if is_zero_sum:
            term = 1.0
            for j in range(r):
                if delta[j] != 0:
                    term *= 0.5 * (float(gammas[j]) ** 2)
            acc += term
    return acc / float(1 << r)


def verify_single_instance_twirl_and_ternary_enumerator(
    a_cols: Sequence[Sequence[int]],
    q_mod: int,
    gammas: Sequence[float],
) -> Dict[str, Any]:
    """Verify exact equality between explicit secret-twirled density matrix Frobenius norm and ternary zero-sum enumerator."""
    rho_bar = secret_twirled_density_matrix_explicit(a_cols, q_mod, gammas)
    dim = len(rho_bar)
    inv_dim = 1.0 / float(dim)

    frob_sq_exp = 0.0
    max_imag_entry = 0.0
    for i in range(dim):
        for j in range(dim):
            target = inv_dim if i == j else 0.0
            diff = rho_bar[i][j] - target
            frob_sq_exp += (diff.real ** 2) + (diff.imag ** 2)
            max_imag_entry = max(max_imag_entry, abs(rho_bar[i][j].imag))

    frob_sq_cf = ternary_zero_sum_frobenius_distance_sq_closed_form(a_cols, q_mod, gammas)

    return {
        "q_mod": q_mod,
        "n": len(a_cols[0]),
        "r_copies": len(a_cols),
        "frob_sq_explicit_twirl": frob_sq_exp,
        "frob_sq_ternary_closed_form": frob_sq_cf,
        "max_imaginary_entry_abs": max_imag_entry,
        "formula_error": abs(frob_sq_exp - frob_sq_cf),
        "exact_ternary_twirl_law_verified": (
            abs(frob_sq_exp - frob_sq_cf) < 1e-12 and max_imag_entry < 1e-12
        ),
    }


def verify_ensemble_mean_frobenius_identity(
    q_mod: int,
    n_rows: int,
    gammas: Sequence[float],
) -> Dict[str, Any]:
    """Exhaustively average ||bar_rho^{(r)}(A) - I/2^r||_F^2 over all A in Z_q^{n x r} and compare to (prod(1 + gamma_j^2) - 1)/(2^r q^n)."""
    r = len(gammas)
    if (q_mod ** (n_rows * r)) > 512:
        raise ValueError("exhaustive ensemble check capped at q^{n*r} <= 512")

    all_cols = list(itertools.product(range(q_mod), repeat=n_rows))
    total_instances = 0
    frob_acc = 0.0
    for a_cols in itertools.product(all_cols, repeat=r):
        frob_acc += ternary_zero_sum_frobenius_distance_sq_closed_form(a_cols, q_mod, gammas)
        total_instances += 1

    emp_mean = frob_acc / float(total_instances)
    prod_term = math.prod(1.0 + (float(g) ** 2) for g in gammas)
    cf_mean = (prod_term - 1.0) / float((1 << r) * (q_mod ** n_rows))

    return {
        "q_mod": q_mod,
        "n": n_rows,
        "r_copies": r,
        "total_instances": total_instances,
        "empirical_mean_frob_sq": emp_mean,
        "closed_form_mean_frob_sq": cf_mean,
        "formula_error": abs(emp_mean - cf_mean),
        "exact_ensemble_identity_verified": abs(emp_mean - cf_mean) < 1e-12,
    }


def generate_dcp_tensor_power_k_moment_dihedral_twirl_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the r-copy secret-twirled tensor-power bridge."""
    # 1. Collision-free ternary instance: q=8, a_cols = [[1], [3]] -> no delta in {-1,0,1}^2 \ {0} has delta_1 + 3*delta_2 == 0 mod 8!
    collision_free_control = verify_single_instance_twirl_and_ternary_enumerator(
        a_cols=[[1], [3]],
        q_mod=8,
        gammas=[0.85, 0.75],
    )

    # 2. Active ternary collision instance: q=8, a_cols = [[1], [2], [3]] -> 1 + 2 - 3 == 0 mod 8!
    ternary_collision_audit = verify_single_instance_twirl_and_ternary_enumerator(
        a_cols=[[1], [2], [3]],
        q_mod=8,
        gammas=[0.9, 0.8, 0.7],
    )

    # 3. Exhaustive ensemble averages over both dyadic q=4 and odd prime q=3,5:
    ensemble_audits = [
        verify_ensemble_mean_frobenius_identity(q_mod=4, n_rows=1, gammas=[0.8, 0.7, 0.6]),
        verify_ensemble_mean_frobenius_identity(q_mod=3, n_rows=1, gammas=[0.9, 0.8, 0.7]),
        verify_ensemble_mean_frobenius_identity(q_mod=2, n_rows=2, gammas=[0.85, 0.75]),
    ]

    all_passed = (
        collision_free_control["exact_ternary_twirl_law_verified"]
        and abs(collision_free_control["frob_sq_explicit_twirl"] - 0.0) < 1e-12
        and ternary_collision_audit["exact_ternary_twirl_law_verified"]
        and ternary_collision_audit["frob_sq_explicit_twirl"] > 0.005
        and all(e["exact_ensemble_identity_verified"] for e in ensemble_audits)
    )

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "proof_status": "LOCAL_DERIVATION_REVIEW_PENDING_NOT_FORMALLY_VERIFIED",
        "scope_constraints": {
            "applies_to": "Secret-twirled r-copy DCP density operators bar_rho^{(r)}(A) = E_s[otimes_{j=1}^r rho(a_j, s, gamma_j)]",
            "does_not_claim": "Single-secret distinguishability bounds when s is fixed rather than twirled",
            "controls_included": "Includes collision-free ternary control (a=[1,3] mod 8 with bar_rho^{(2)} == I_4/4), active 3-copy ternary collision audit (a=[1,2,3] mod 8), and exact ensemble identity (prod(1+gamma_j^2)-1)/(2^r q^n) across dyadic q=4,2^2 and prime q=3.",
        },
        "collision_free_ternary_control": collision_free_control,
        "active_ternary_collision_audit": ternary_collision_audit,
        "ensemble_frobenius_audits": ensemble_audits,
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
