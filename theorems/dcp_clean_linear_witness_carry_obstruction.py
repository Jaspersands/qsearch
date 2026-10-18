"""Scoped clean-DCP linear witness identities and conditioned-label audit.

Tests two concrete uniform polynomial-time witness-synthesis constructions on
the clean DCP / sine-window bridge (dcp_direct_witness_filter.py and
dcp_forward_sampler_swap.py):
1. Theorem 1 (2-Adic Hensel Disjoint Boolean Translate Theorem):
   For any A in Z_{2^t}^{n x K} (t >= 2) with an odd-determinant n x n pivot block
   A_P in GL_n(Z_{2^t}), the deterministic 2-adic witness map
     w_P(t) = A_P^{-1}(t - A_{bar{P}} u_0) mod 2^t,   w_{bar{P}}(t) = u_0 in {0,1}^{K-n}
   produces a valid Boolean witness w(t) in {0,1}^K for exactly 2^n of the 2^{nt}
   targets (verified coverage beta_A = 2^{-n(t-1)}, direct-filter success
   2^{-(K-nt)} * 2^{-2n(t-1)}). For the parity target h = (2^{t-1}, 0, ..., 0),
   the pivot shift A_P^{-1} h = 2^{t-1}(A_P^{-1} e_1 mod 2) mod 2^t has entries in
   {0, 2^{t-1}} with at least one non-zero entry, so T_valid intersect (T_valid + h) = empty
   and the forward-SWAP observable O = V^dagger P W P V is identically zero (Adv_SWAP = 0)
   for every secret S in Z_{2^t}^n.
2. Theorem 2 (Exact Carry-Parity Vanishing Criterion for Bitwise F_2-RREF Circuits):
   For any F_2-right inverse R_{F_2} in F_2^{K x (nt)} of the stacked bit-matrix
   M_{F_2} in F_2^{(nt) x K}, the CNOT witness synthesis w(t) = R_{F_2} bits(t) mod 2
   satisfies (A w(t))_ell^{(b)} = t_ell^{(b)} XOR (c_ell^{(b)}(w(t)) mod 2), so
   A w(t) = t mod 2^t holds if and only if all n(t-1) intermediate carry parities
   c_ell^{(b)}(w(t)) mod 2 (ell=0..n-1, b=1..t-1) vanish simultaneously.
3. Theorem 3 (Disjoint-Support Kernel Linearization):
   Eliminating carry cross-terms on the layer-0 F_2-kernel x(u) = x_0 XOR (XOR_{j=1}^m u_j V_j)
   by selecting m pairwise-disjoint kernel supports supp(V_j) with wt_H(V_j) >= 2
   restricts m <= floor(K/2) and linearizes A x(u) mod 2^t to an affine 0-1 subset sum
   of width m. Its effective labels are EVEN, not IID uniform over Z_{2^t}^n.
   No source-average decay follows without the actual conditioned label law.
   Exact finite occupancy calculations below retain all collisions and pay the
   probability of projecting the original state onto ONE chosen affine subspace.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, List, Sequence, Tuple

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTRACT_PATH = (
    ROOT
    / "research"
    / "hypotheses"
    / "dcp_clean_linear_witness_carry_obstruction_contract.json"
)
DEFAULT_ARTIFACT_PATH = (
    ROOT
    / "research"
    / "reductions"
    / "dcp_clean_linear_witness_carry_obstruction.json"
)


def invert_matrix_mod_2adic(mat: Sequence[Sequence[int]], t: int) -> List[List[int]]:
    """Invert an n x n integer matrix modulo 2^t via GF(2) Gauss-Jordan + Hensel lifting."""
    arr = np.array(mat, dtype=object)
    n = arr.shape[0]
    mod2 = (arr % 2).astype(int)
    aug = np.hstack([mod2, np.eye(n, dtype=int)])
    for col in range(n):
        piv = None
        for row in range(col, n):
            if int(aug[row, col]) % 2 == 1:
                piv = row
                break
        if piv is None:
            raise ValueError("Pivot block is not invertible modulo 2")
        if piv != col:
            aug[[col, piv]] = aug[[piv, col]]
        for row in range(n):
            if row != col and int(aug[row, col]) % 2 == 1:
                aug[row] = aug[row] ^ aug[col]
    inv = aug[:, n:].astype(object)
    q = 1 << t
    for _ in range(t):
        inv = (inv @ (2 * np.eye(n, dtype=object) - (arr.astype(object) @ inv))) % q
    res = [[int(x) for x in row] for row in inv.tolist()]
    check = (arr.astype(object) @ np.array(res, dtype=object)) % q
    if not np.array_equal(check, np.eye(n, dtype=object)):
        raise ArithmeticError("2-adic Hensel inverse failed verification")
    return res


def stack_bit_layers_f2(A: Sequence[Sequence[int]], t: int) -> List[List[int]]:
    """Stack the n*t binary bit-layers of A in Z_{2^t}^{n x K} into M_{F_2} in F_2^{(nt) x K}."""
    n = len(A)
    K = len(A[0])
    M = [[0] * K for _ in range(n * t)]
    for ell in range(n):
        for b in range(t):
            row_idx = ell * t + b
            for r in range(K):
                M[row_idx][r] = int((int(A[ell][r]) >> b) & 1)
    return M


def solve_f2_right_inverse(M_f2: Sequence[Sequence[int]]) -> List[List[int]]:
    """Compute a canonical right-inverse R in F_2^{K x rows} such that M_f2 @ R = I mod 2."""
    arr = np.array(M_f2, dtype=int) % 2
    rows, K = arr.shape
    if K < rows:
        raise ValueError("K >= rows required for F_2 right inverse")
    piv_cols: List[int] = []
    aug = arr.copy()
    r = 0
    for c in range(K):
        if r >= rows:
            break
        piv = None
        for rr in range(r, rows):
            if int(aug[rr, c]) == 1:
                piv = rr
                break
        if piv is None:
            continue
        if piv != r:
            aug[[r, piv]] = aug[[piv, r]]
        for rr in range(rows):
            if rr != r and int(aug[rr, c]) == 1:
                aug[rr] ^= aug[r]
        piv_cols.append(c)
        r += 1
    if len(piv_cols) < rows:
        raise ValueError("Stacked bit-layer matrix M_f2 does not have full row rank over F_2")
    sub = arr[:, piv_cols] % 2
    sub_inv = invert_matrix_mod_2adic(sub.tolist(), 1)
    R = [[0] * rows for _ in range(K)]
    for idx, c in enumerate(piv_cols):
        R[c] = [int(x % 2) for x in sub_inv[idx]]
    check = (arr @ np.array(R, dtype=int)) % 2
    if not np.array_equal(check, np.eye(rows, dtype=int)):
        raise ArithmeticError("F_2 right inverse failed verification")
    return R


def target_to_bits(t_vec: Sequence[int], t: int) -> List[int]:
    """Expand t_vec in Z_{2^t}^n into its n*t binary digits (LSB first per coordinate)."""
    bits: List[int] = []
    for val in t_vec:
        for b in range(t):
            bits.append(int((int(val) >> b) & 1))
    return bits


def compute_carry_parities(
    A: Sequence[Sequence[int]], w: Sequence[int], t: int
) -> Tuple[List[List[int]], List[List[int]]]:
    """Return (carry_parities_b1_to_t_minus_1, full_carries_b0_to_t_minus_1) for A w mod 2^t."""
    n = len(A)
    K = len(A[0])
    carry_parities: List[List[int]] = []
    full_carries: List[List[int]] = []
    for ell in range(n):
        c = 0
        ell_parities: List[int] = []
        ell_full: List[int] = []
        for b in range(t):
            ell_full.append(int(c))
            if b >= 1:
                ell_parities.append(int(c % 2))
            s_b = sum(((int(A[ell][r]) >> b) & 1) * int(w[r]) for r in range(K)) + c
            c = s_b // 2
        carry_parities.append(ell_parities)
        full_carries.append(ell_full)
    return carry_parities, full_carries


def compressed_parity_audit(
    columns: Sequence[Sequence[int]], t: int, *, precision_bits: int = 80
) -> Dict[str, Any]:
    """Finite clean-state Helstrom parity overlap, with integer sqrt enclosures.

    The secret is uniform on Z_(2^t)^n. No random-label assumption is used.
    This exponential reference computes information, not an efficient receiver.
    """
    if type(t) is not int or t < 2 or t > 4096:
        raise ValueError("phase bits must be an integer in [2,4096]")
    if type(precision_bits) is not int or not 1 <= precision_bits <= 512:
        raise ValueError("precision_bits must be in [1,512]")
    n = len(columns)
    m = len(columns[0]) if n else 0
    if not n or m > 16 or any(len(row) != m for row in columns):
        raise ValueError("rectangular nonempty matrix and at most 16 reference wires required")
    q = 1 << t
    if any(type(v) is not int or not 0 <= v < q for row in columns for v in row):
        raise ValueError("canonical exact integer labels required")
    counts = Counter(
        tuple(sum(row[j] * word[j] for j in range(m)) % q for row in columns)
        for word in itertools.product((0, 1), repeat=m)
    )
    denominator = 2 * (1 << m)
    scale = 1 << precision_bits
    lower_sum = upper_sum = 0
    exact_sum = 0
    all_square = True
    for frequency, count in counts.items():
        partner = ((frequency[0] + q // 2) % q, *frequency[1:])
        product = count * counts.get(partner, 0)
        root = math.isqrt(product)
        all_square &= root * root == product
        exact_sum += root
        scaled_product = product * scale * scale
        floor_root = math.isqrt(scaled_product)
        lower_sum += floor_root
        upper_sum += floor_root + int(floor_root * floor_root != scaled_product)
    lower = Fraction(lower_sum, scale * denominator)
    upper = min(Fraction(1, 2), Fraction(upper_sum, scale * denominator))
    return {
        "target": "first_coordinate_parity_of_uniform_secret",
        "enumerated_boolean_words": 1 << m,
        "occupied_frequencies": len(counts),
        "effective_columns_all_even": all(v % 2 == 0 for row in columns for v in row),
        "optimal_conditional_advantage_exact": str(Fraction(exact_sum, denominator)) if all_square else None,
        "optimal_conditional_advantage_lower_exact": str(lower),
        "optimal_conditional_advantage_upper_exact": str(upper),
        "source_average_bound_inferred": False,
        "efficient_measurement_implemented": False,
    }


def evaluate_instance(instance: Dict[str, Any]) -> Dict[str, Any]:
    """Verify Theorems 1, 2, and 3 on a concrete clean DCP instance."""
    instance_id = str(instance["instance_id"])
    n = int(instance["n"])
    t = int(instance["t"])
    K = int(instance["K"])
    q = 1 << t
    delta = K - n * t
    A_hensel = [[int(x) for x in row] for row in instance["A_hensel"]]
    A_f2_rref = [[int(x) for x in row] for row in instance["A_f2_rref"]]

    h = [0] * n
    h[0] = q // 2
    all_targets = list(itertools.product(range(q), repeat=n))

    # --- Theorem 1: 2-Adic Hensel Right-Inverse Obstruction ---
    A_piv = [row[:n] for row in A_hensel]
    R_piv = invert_matrix_mod_2adic(A_piv, t)
    hensel_valid_targets: List[Tuple[int, ...]] = []
    for t_tuple in all_targets:
        w_piv = [
            int(sum(R_piv[i][j] * t_tuple[j] for j in range(n)) % q)
            for i in range(n)
        ]
        if all(x in (0, 1) for x in w_piv):
            w_full = w_piv + [0] * (K - n)
            lhs = [
                int(sum(A_hensel[ell][r] * w_full[r] for r in range(K)) % q)
                for ell in range(n)
            ]
            assert lhs == list(t_tuple)
            hensel_valid_targets.append(t_tuple)

    hensel_valid_set = set(hensel_valid_targets)
    hensel_paired_targets = [
        t_tuple
        for t_tuple in hensel_valid_targets
        if tuple((t_tuple[ell] + h[ell]) % q for ell in range(n)) in hensel_valid_set
    ]
    pivot_shift_h = [
        int(sum(R_piv[i][j] * h[j] for j in range(n)) % q) for i in range(n)
    ]

    expected_hensel_valid_count = 1 << n
    beta_hensel = Fraction(len(hensel_valid_targets), q ** n)
    expected_beta_hensel = Fraction(1 << n, q ** n)
    direct_filter_hensel = beta_hensel * beta_hensel * Fraction(1, 1 << delta)

    # Also verify exact forward-SWAP observable O = 0 on the 2^K state space for A_hensel
    L = 1 << K
    f_hensel = [
        tuple(
            int(sum(A_hensel[ell][r] * ((x >> r) & 1) for r in range(K)) % q)
            for ell in range(n)
        )
        for x in range(L)
    ]
    hensel_swap_nonzero_entries = 0
    for x in range(L):
        t_x = tuple((f_hensel[x][ell] + h[ell]) % q for ell in range(n))
        w_piv = [
            int(sum(R_piv[i][j] * t_x[j] for j in range(n)) % q) for i in range(n)
        ]
        if all(v in (0, 1) for v in w_piv):
            y = sum(int(w_piv[i]) << i for i in range(n))
            if f_hensel[y] == t_x:
                t_y = tuple((f_hensel[y][ell] + h[ell]) % q for ell in range(n))
                w_piv_back = [
                    int(sum(R_piv[i][j] * t_y[j] for j in range(n)) % q)
                    for i in range(n)
                ]
                if all(v in (0, 1) for v in w_piv_back):
                    x_back = sum(int(w_piv_back[i]) << i for i in range(n))
                    if x_back == x:
                        hensel_swap_nonzero_entries += 1

    theorem1_passed = bool(
        len(hensel_valid_targets) == expected_hensel_valid_count
        and beta_hensel == expected_beta_hensel
        and len(hensel_paired_targets) == 0
        and hensel_swap_nonzero_entries == 0
        and any(v == (q // 2) for v in pivot_shift_h)
        and all(v in (0, q // 2) for v in pivot_shift_h)
    )

    # --- Theorem 2: Bitwise F_2-RREF Carry-Parity Vanishing Criterion ---
    M_f2 = stack_bit_layers_f2(A_f2_rref, t)
    R_f2 = solve_f2_right_inverse(M_f2)

    f2_valid_targets: List[Tuple[int, ...]] = []
    bitwise_identity_verified_count = 0
    carry_equivalence_verified_count = 0

    for t_tuple in all_targets:
        t_bits = target_to_bits(t_tuple, t)
        w = [
            int(sum(R_f2[r][idx] * t_bits[idx] for idx in range(n * t)) % 2)
            for r in range(K)
        ]
        carry_parities, full_carries = compute_carry_parities(A_f2_rref, w, t)
        actual_sum = [
            int(sum(A_f2_rref[ell][r] * w[r] for r in range(K)) % q)
            for ell in range(n)
        ]

        # Check bitwise identity: (A w)_ell^{(b)} == t_ell^{(b)} XOR (c_ell^{(b)}(w) mod 2)
        bitwise_ok = True
        for ell in range(n):
            for b in range(t):
                actual_bit = (actual_sum[ell] >> b) & 1
                target_bit = (t_tuple[ell] >> b) & 1
                c_mod2 = full_carries[ell][b] % 2
                if actual_bit != (target_bit ^ c_mod2):
                    bitwise_ok = False
        if bitwise_ok:
            bitwise_identity_verified_count += 1

        is_valid_witness = actual_sum == list(t_tuple)
        all_carries_even = all(
            c_par == 0 for ell_row in carry_parities for c_par in ell_row
        )
        if is_valid_witness == all_carries_even:
            carry_equivalence_verified_count += 1
        if is_valid_witness:
            f2_valid_targets.append(t_tuple)

    f2_valid_set = set(f2_valid_targets)
    f2_paired_targets = [
        t_tuple
        for t_tuple in f2_valid_targets
        if tuple((t_tuple[ell] + h[ell]) % q for ell in range(n)) in f2_valid_set
    ]

    f_f2_map = [
        tuple(
            int(sum(A_f2_rref[ell][r] * ((x >> r) & 1) for r in range(K)) % q)
            for ell in range(n)
        )
        for x in range(L)
    ]
    f2_swap_mutual_pairs = 0
    for x in range(L):
        t_x = tuple((f_f2_map[x][ell] + h[ell]) % q for ell in range(n))
        t_x_bits = target_to_bits(t_x, t)
        w_tx = [
            int(sum(R_f2[r][idx] * t_x_bits[idx] for idx in range(n * t)) % 2)
            for r in range(K)
        ]
        y = sum(int(w_tx[r]) << r for r in range(K))
        if f_f2_map[y] == t_x:
            t_y = tuple((f_f2_map[y][ell] + h[ell]) % q for ell in range(n))
            t_y_bits = target_to_bits(t_y, t)
            w_ty = [
                int(sum(R_f2[r][idx] * t_y_bits[idx] for idx in range(n * t)) % 2)
                for r in range(K)
            ]
            x_back = sum(int(w_ty[r]) << r for r in range(K))
            if x_back == x:
                f2_swap_mutual_pairs += 1

    beta_f2 = Fraction(len(f2_valid_targets), q ** n)
    swap_adv_f2 = Fraction(f2_swap_mutual_pairs, 2 * L)

    theorem2_passed = bool(
        bitwise_identity_verified_count == (q ** n)
        and carry_equivalence_verified_count == (q ** n)
    )

    # --- Theorem 3: Disjoint-Support Kernel Linearization, NOT IID labels ---
    A_dk = [[int(x) for x in row] for row in instance["disjoint_kernel_A"]]
    x0 = [int(x) for x in instance["disjoint_kernel_x0"]]
    V_rows = [[int(x) for x in row] for row in instance["disjoint_kernel_V"]]
    K_dk = len(A_dk[0])
    m_dk = len(V_rows)

    # Verify supports are pairwise disjoint and in ker(A_dk mod 2) with weight >= 2
    supports = [{r for r in range(K_dk) if V_rows[j][r] == 1} for j in range(m_dk)]
    disjoint_ok = all(
        len(supports[i] & supports[j]) == 0
        for i in range(m_dk)
        for j in range(i + 1, m_dk)
    )
    weights_ok = all(len(s) >= 2 for s in supports)
    in_mod2_kernel_ok = all(
        sum(A_dk[ell][r] * V_rows[j][r] for r in range(K_dk)) % 2 == 0
        for j in range(m_dk)
        for ell in range(n)
    )

    # Effective columns tilde_A_j = sum_{r in supp(V_j)} (1 - 2 x0_r) A_{., r} mod q
    base_offset = [
        int(sum(A_dk[ell][r] * x0[r] for r in range(K_dk)) % q)
        for ell in range(n)
    ]
    tilde_A = [
        [
            int(
                sum((1 - 2 * x0[r]) * A_dk[ell][r] for r in supports[j]) % q
            )
            for j in range(m_dk)
        ]
        for ell in range(n)
    ]

    linearization_matches = 0
    for u in itertools.product((0, 1), repeat=m_dk):
        x_u = [
            int(x0[r] ^ (sum(u[j] * V_rows[j][r] for j in range(m_dk)) % 2))
            for r in range(K_dk)
        ]
        actual_mod_q = [
            int(sum(A_dk[ell][r] * x_u[r] for r in range(K_dk)) % q)
            for ell in range(n)
        ]
        affine_mod_q = [
            int(
                (base_offset[ell] + sum(u[j] * tilde_A[ell][j] for j in range(m_dk)))
                % q
            )
            for ell in range(n)
        ]
        if actual_mod_q == affine_mod_q:
            linearization_matches += 1

    parity_audit = compressed_parity_audit(tilde_A, t)
    # Selecting one affine Boolean subspace from the original flat phase state.
    branch_probability = Fraction(1, 1 << (K_dk - m_dk))
    parity_audit["selected_affine_subspace_probability_exact"] = str(branch_probability)
    for endpoint in ("lower", "upper"):
        parity_audit[f"selected_branch_unconditional_advantage_{endpoint}_exact"] = str(
            branch_probability * Fraction(parity_audit[f"optimal_conditional_advantage_{endpoint}_exact"])
        )
    theorem3_passed = bool(
        disjoint_ok
        and weights_ok
        and in_mod2_kernel_ok
        and m_dk <= (K_dk // 2)
        and linearization_matches == (1 << m_dk)
        and parity_audit["effective_columns_all_even"]
    )

    return {
        "instance_id": instance_id,
        "n": int(n),
        "t": int(t),
        "q": int(q),
        "K": int(K),
        "total_targets": int(q ** n),
        "hensel_audit": {
            "A_hensel": A_hensel,
            "R_piv": R_piv,
            "valid_boolean_witness_count": int(len(hensel_valid_targets)),
            "expected_valid_boolean_witness_count": int(expected_hensel_valid_count),
            "verified_coverage_beta_exact": str(beta_hensel),
            "direct_filter_success_exact": str(direct_filter_hensel),
            "pivot_shift_h_mod_q": pivot_shift_h,
            "paired_valid_targets_for_h": int(len(hensel_paired_targets)),
            "forward_swap_nonzero_entries": int(hensel_swap_nonzero_entries),
            "forward_swap_advantage_exact": "0",
            "theorem1_passed": bool(theorem1_passed),
        },
        "f2_rref_audit": {
            "A_f2_rref": A_f2_rref,
            "R_f2": R_f2,
            "num_carry_constraints": int(n * (t - 1)),
            "bitwise_identity_verified_targets": int(bitwise_identity_verified_count),
            "carry_equivalence_verified_targets": int(carry_equivalence_verified_count),
            "carry_free_valid_target_count": int(len(f2_valid_targets)),
            "verified_coverage_beta_exact": str(beta_f2),
            "paired_valid_targets_for_h": int(len(f2_paired_targets)),
            "swap_reciprocal_valid_pairs": int(f2_swap_mutual_pairs),
            "forward_swap_advantage_exact": str(swap_adv_f2),
            "forward_swap_advantage_float": float(swap_adv_f2),
            "theorem2_passed": bool(theorem2_passed),
        },
        "disjoint_kernel_audit": {
            "K_dk": int(K_dk),
            "m_disjoint_directions": int(m_dk),
            "max_possible_disjoint_directions": int(K_dk // 2),
            "base_offset_mod_q": base_offset,
            "effective_columns_tilde_A": tilde_A,
            "linearization_verified_assignments": int(linearization_matches),
            "compressed_source_average_advantage_upper_exact": None,
            "source_average_bound_status": "UNKNOWN_CONDITIONED_ADAPTIVE_LABEL_LAW",
            "iid_uniform_full_group_assumption_valid": False,
            "parity_audit": parity_audit,
            "theorem3_passed": bool(theorem3_passed),
        },
        "instance_passed": bool(
            theorem1_passed and theorem2_passed and theorem3_passed
        ),
    }


def evaluate_asymptotic_scaling(grid: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Compute exact asymptotic scaling exponents on the clean DCP frontier."""
    rows: List[Dict[str, Any]] = []
    for item in grid:
        n = int(item["n"])
        t = int(item["t"])
        K = int(item["K"])
        nt = n * t
        hensel_coverage_neg_log2 = int(n * (t - 1))
        hensel_direct_filter_neg_log2 = int((K - nt) + 2 * n * (t - 1))
        carry_constraints = int(n * (t - 1))
        m_disjoint_max = int(K // 2)
        rows.append(
            {
                "n": int(n),
                "t": int(t),
                "K": int(K),
                "group_bits_nt": int(nt),
                "hensel_coverage_beta_power_of_two_neg_exponent": hensel_coverage_neg_log2,
                "hensel_direct_filter_success_power_of_two_neg_exponent": hensel_direct_filter_neg_log2,
                "hensel_forward_swap_advantage_exact": "0",
                "f2_rref_simultaneous_carry_parity_constraints": carry_constraints,
                "disjoint_kernel_max_free_wires_m": m_disjoint_max,
                "disjoint_kernel_average_advantage_upper_power_of_two_neg_exponent": None,
                "disjoint_kernel_source_average_status": "NOT_PROVED_LABEL_LAW_REQUIRED",
            }
        )
    return rows


def build_dcp_clean_linear_witness_carry_obstruction_report(
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> Dict[str, Any]:
    """Build the full reduction artifact from the locked contract."""
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    instances = [evaluate_instance(inst) for inst in contract["test_instances"]]
    asymptotic_rows = evaluate_asymptotic_scaling(contract["asymptotic_scaling_grid"])

    all_t1 = bool(all(inst["hensel_audit"]["theorem1_passed"] for inst in instances))
    all_t2 = bool(all(inst["f2_rref_audit"]["theorem2_passed"] for inst in instances))
    all_t3 = bool(
        all(inst["disjoint_kernel_audit"]["theorem3_passed"] for inst in instances)
    )
    all_passed = bool(all_t1 and all_t2 and all_t3)

    payload_for_hash = {
        "contract_id": contract["contract_id"],
        "instances": instances,
        "asymptotic_scaling": asymptotic_rows,
        "all_passed": all_passed,
    }
    digest = hashlib.sha256(
        json.dumps(payload_for_hash, sort_keys=True).encode("utf-8")
    ).hexdigest()

    return {
        "schema_version": "2.0",
        "subsystem": "dcp_clean_linear_witness_carry_obstruction",
        "contract_id": str(contract["contract_id"]),
        "title": str(contract["title"]),
        "family": str(contract["family"]),
        "note_path": "research/DCP_CLEAN_LINEAR_WITNESS_CARRY_OBSTRUCTION.md",
        "contract_path": "research/hypotheses/dcp_clean_linear_witness_carry_obstruction_contract.json",
        "summary": {
            "num_instances": int(len(instances)),
            "theorem1_hensel_disjoint_translate_passed": bool(all_t1),
            "theorem2_f2_rref_carry_parity_vanishing_passed": bool(all_t2),
            "theorem3_disjoint_kernel_linearization_passed": bool(all_t3),
            "all_theorems_passed": bool(all_passed),
            "max_hensel_swap_advantage": 0.0,
            "disjoint_kernel_source_average_decay_proved": False,
            "old_full_group_iid_bound": "RETRACTED_EFFECTIVE_LABELS_ARE_EVEN",
            "verification_scope": "finite_identity_controls_and_local_derivations_review_pending",
        },
        "instances": instances,
        "asymptotic_scaling": asymptotic_rows,
        "honesty_guardrails": {
            "accepted_speedup_candidate": False,
            "new_active_negative_result_created": False,
            "novelty_claim": False,
        },
        "sha256": str(digest),
    }


def write_dcp_clean_linear_witness_carry_obstruction_report(
    artifact_path: Path = DEFAULT_ARTIFACT_PATH,
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> Dict[str, Any]:
    """Generate and write the JSON reduction artifact to disk."""
    report = build_dcp_clean_linear_witness_carry_obstruction_report(
        contract_path=contract_path
    )
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    artifact_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the clean DCP linear and bitwise-RREF witness carry obstruction audit."
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write the reduction JSON artifact to research/reductions/.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print the full report as JSON to stdout.",
    )
    args = parser.parse_args()

    if args.write:
        report = write_dcp_clean_linear_witness_carry_obstruction_report()
    else:
        report = build_dcp_clean_linear_witness_carry_obstruction_report()

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        s = report["summary"]
        print(
            f"[dcp_clean_linear_witness_carry_obstruction] "
            f"instances={s['num_instances']} "
            f"all_passed={s['all_theorems_passed']} "
            f"max_hensel_swap_adv={s['max_hensel_swap_advantage']:.3e} "
            f"sha256={report['sha256'][:16]}"
        )
    return 0 if report["summary"]["all_theorems_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
