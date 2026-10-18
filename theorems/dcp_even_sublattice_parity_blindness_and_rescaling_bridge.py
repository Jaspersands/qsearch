"""DCP even-sublattice parity blindness and mod-2^{t-1} rescaling bridge.

Establishes the exact algebraic and distributional structure of effective columns
under disjoint mod-2 kernel witness extraction V_1, ..., V_m in ker(A mod 2):

1. Universal Evenness Identity:
   For any A in Z_{2^t}^{n x K}, any v in ker(A mod 2), and any anchor x_0 in {0,1}^K,
   the effective column
       tilde_A(v, x_0) = sum_{r=1}^K v_r (1 - 2*(x_0)_r) A_{., r} mod 2^t
   satisfies tilde_A(v, x_0) == A v == 0 (mod 2) in every coordinate. Thus tilde_A(v, x_0)
   lies deterministically in the index-2^n even sublattice (2 Z_{2^t})^n for all x_0.

2. Odd-Shift Blindness and Mod-2^{t-1} Halving Isomorphism:
   - Every compressed difference tilde_A (u - u') mod 2^t lies in (2 Z_{2^t})^n, so any
     shift vector h in Z_{2^t}^n with at least one odd coordinate (including the t=1
     half-period target h = (1, 0, ..., 0)) has strictly zero compressed collisions
     and zero conditional Helstrom advantage across all A, V, and x_0.
   - For t >= 2, dividing by 2 defines an exact group isomorphism from (2 Z_{2^t})^n
     onto Z_{2^{t-1}}^n:
         B_j(x_0) = (tilde_A_j(x_0) mod 2^t) / 2 in Z_{2^{t-1}}^n,
     mapping the half-period target h = (2^{t-1}, 0, ..., 0) in Z_{2^t}^n to
         h' = (2^{t-2}, 0, ..., 0) in Z_{2^{t-1}}^n.

3. Fixed-Instance vs. Upper-Bit Ensemble Dichotomy:
   - For a fixed matrix A, B_j(x_0) is not IID uniform as x_0 varies:
     * For A = [[2, 0]] mod 4 and V_1 = (1, 1)^T, B_1(x_0) = 1 (mod 2) for all 4 anchors
       x_0 in {0,1}^2, giving Adv_cond = 1.0 universally across x_0 (and unconditional
       branch contribution 2^{-(K-m)} = 1/2).
     * For A = [[1, 1]] mod 4 and V_1 = (1, 1)^T, B_1(x_0) = 1 (mod 2) for half of the
       anchors x_0 in {0,1}^2, giving E_{x_0}[Adv_cond] = 1/2 (and unconditional branch
       contribution 1/4).
   - Writing A = A^{(0)} + 2 A^{(high)} with A^{(0)} = A mod 2 in {0,1}^{n x K} and
     A^{(high)} = floor(A / 2) in Z_{2^{t-1}}^{n x K}, for ANY fixed (A^{(0)}, disjoint
     non-empty V_1, ..., V_m in ker(A^{(0)}), x_0 in {0,1}^K), as A^{(high)} ranges
     uniformly over (Z_{2^{t-1}})^{n x K}, the rescaled columns (B_1(x_0), ..., B_m(x_0))
     are exact IID uniform over (Z_{2^{t-1}}^n)^m with reduced group size
     Q_even = 2^{n(t-1)} (not 2^{nt}).
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from typing import Any, Dict, List, Sequence, Tuple


THEOREM_ID = "dcp_even_sublattice_parity_blindness_and_rescaling_bridge"
SCHEMA_VERSION = "dcp-even-sublattice-parity-blindness-and-rescaling-bridge-v1"


def compute_effective_column_mod_2t(
    a_matrix: Sequence[Sequence[int]],
    v_vec: Sequence[int],
    x0_vec: Sequence[int],
    t_bits: int,
) -> Tuple[int, ...]:
    """Compute tilde_A(v, x_0) = sum_r v_r (1 - 2*(x_0)_r) A_{., r} mod 2^t."""
    q_mod = 1 << t_bits
    n_rows = len(a_matrix)
    k_cols = len(v_vec)
    out: List[int] = []
    for i in range(n_rows):
        acc = 0
        for r in range(k_cols):
            if v_vec[r]:
                sign = 1 - 2 * int(x0_vec[r])
                acc += sign * int(a_matrix[i][r])
        out.append(acc % q_mod)
    return tuple(out)


def verify_even_effective_column_identity(
    a_matrix: Sequence[Sequence[int]],
    v_vec: Sequence[int],
    t_bits: int,
) -> Dict[str, Any]:
    """Verify that for v in ker(A mod 2), tilde_A(v, x_0) is even for all x_0 in {0,1}^K."""
    n_rows = len(a_matrix)
    k_cols = len(v_vec)
    mod2_syndrome = tuple(
        sum(int(a_matrix[i][r]) * int(v_vec[r]) for r in range(k_cols)) % 2
        for i in range(n_rows)
    )
    in_mod2_kernel = all(s == 0 for s in mod2_syndrome)

    all_even = True
    halving_bijection_holds = True
    distinct_rescaled_columns = set()
    for x0 in itertools.product((0, 1), repeat=k_cols):
        col = compute_effective_column_mod_2t(a_matrix, v_vec, x0, t_bits)
        if any((c % 2) != 0 for c in col):
            all_even = False
        rescaled = tuple(c // 2 for c in col)
        distinct_rescaled_columns.add(rescaled)
        if tuple(2 * b for b in rescaled) != col:
            halving_bijection_holds = False

    return {
        "n": n_rows,
        "t": t_bits,
        "K": k_cols,
        "in_mod2_kernel": in_mod2_kernel,
        "all_anchors_checked": 1 << k_cols,
        "all_effective_columns_even": all_even,
        "halving_bijection_holds": halving_bijection_holds,
        "distinct_rescaled_column_count": len(distinct_rescaled_columns),
    }


def conditional_helstrom_advantage_from_effective_columns(
    tilde_a_cols: Sequence[Sequence[int]],
    target_h: Sequence[int],
    t_bits: int,
) -> float:
    """Exact conditional single-copy Helstrom advantage for distinguishing s=0 vs s=h on m compressed wires."""
    q_mod = 1 << t_bits
    n_rows = len(target_h)
    m_wires = len(tilde_a_cols)
    occupied_labels = set()
    for u_bits in itertools.product((0, 1), repeat=m_wires):
        label = tuple(
            sum(int(tilde_a_cols[j][i]) * u_bits[j] for j in range(m_wires)) % q_mod
            for i in range(n_rows)
        )
        occupied_labels.add(label)

    matched_count = 0
    for u_bits in itertools.product((0, 1), repeat=m_wires):
        shifted = tuple(
            (sum(int(tilde_a_cols[j][i]) * u_bits[j] for j in range(m_wires)) + int(target_h[i])) % q_mod
            for i in range(n_rows)
        )
        if shifted in occupied_labels:
            matched_count += 1
    return matched_count / float(1 << m_wires)


def conditional_helstrom_advantage_from_rescaled_columns(
    b_cols: Sequence[Sequence[int]],
    rescaled_h: Sequence[int],
    t_minus_1_bits: int,
) -> float:
    """Exact conditional single-copy Helstrom advantage computed in the halved group Z_{2^{t-1}}^n."""
    return conditional_helstrom_advantage_from_effective_columns(
        tilde_a_cols=b_cols,
        target_h=rescaled_h,
        t_bits=t_minus_1_bits,
    )


def verify_odd_target_impossibility_and_halving_isomorphism(
    a_matrix: Sequence[Sequence[int]],
    v_basis: Sequence[Sequence[int]],
    t_bits: int,
) -> Dict[str, Any]:
    """Verify odd-target blindness (including t=1) and exact halving isomorphism to Z_{2^{t-1}}^n for t >= 2."""
    n_rows = len(a_matrix)
    k_cols = len(a_matrix[0])
    m_wires = len(v_basis)
    odd_target = tuple([1] + [0] * (n_rows - 1))
    half_period_target = tuple([1 << (t_bits - 1)] + [0] * (n_rows - 1))

    max_odd_target_advantage = 0.0
    halving_isomorphism_exact = True
    anchor_advantages: List[float] = []

    for x0 in itertools.product((0, 1), repeat=k_cols):
        tilde_cols = [
            compute_effective_column_mod_2t(a_matrix, v_vec, x0, t_bits)
            for v_vec in v_basis
        ]
        adv_odd = conditional_helstrom_advantage_from_effective_columns(
            tilde_cols, odd_target, t_bits
        )
        if adv_odd > max_odd_target_advantage:
            max_odd_target_advantage = adv_odd

        adv_half_period = conditional_helstrom_advantage_from_effective_columns(
            tilde_cols, half_period_target, t_bits
        )
        anchor_advantages.append(adv_half_period)

        if t_bits >= 2:
            b_cols = [tuple(c // 2 for c in col) for col in tilde_cols]
            rescaled_h = tuple(c // 2 for c in half_period_target)
            adv_rescaled = conditional_helstrom_advantage_from_rescaled_columns(
                b_cols, rescaled_h, t_bits - 1
            )
            if abs(adv_half_period - adv_rescaled) > 1e-12:
                halving_isomorphism_exact = False

    mean_conditional_advantage = sum(anchor_advantages) / float(len(anchor_advantages))
    subspace_selection_probability = 2.0 ** (-(k_cols - m_wires))
    unconditional_branch_contribution = subspace_selection_probability * mean_conditional_advantage

    return {
        "n": n_rows,
        "t": t_bits,
        "K": k_cols,
        "m": m_wires,
        "max_odd_target_advantage": max_odd_target_advantage,
        "odd_target_strictly_blind": max_odd_target_advantage == 0.0,
        "halving_isomorphism_exact": halving_isomorphism_exact,
        "mean_conditional_advantage": mean_conditional_advantage,
        "subspace_selection_probability": subspace_selection_probability,
        "unconditional_branch_contribution": unconditional_branch_contribution,
    }


def verify_upper_bit_ensemble_rescaled_uniformity(
    a_mod2: Sequence[Sequence[int]],
    v_basis: Sequence[Sequence[int]],
    x0_vec: Sequence[int],
    t_bits: int,
) -> Dict[str, Any]:
    """Verify that over uniform upper bits A^{(high)} in Z_{2^{t-1}}^{n x K}, B_1(x_0), ..., B_m(x_0) are exact IID uniform over Z_{2^{t-1}}^n."""
    if t_bits < 2:
        raise ValueError("t_bits must be >= 2 for non-trivial upper-bit ensemble.")
    n_rows = len(a_mod2)
    k_cols = len(a_mod2[0])
    m_wires = len(v_basis)
    q_half = 1 << (t_bits - 1)
    q_even = q_half ** n_rows
    rescaled_h = tuple([1 << (t_bits - 2)] + [0] * (n_rows - 1))

    tuple_counts: Dict[Tuple[Tuple[int, ...], ...], int] = {}
    total_instances = 0
    total_adv = 0.0

    for high_entries in itertools.product(range(q_half), repeat=n_rows * k_cols):
        a_matrix = []
        for i in range(n_rows):
            row = []
            for r in range(k_cols):
                a_high = high_entries[i * k_cols + r]
                row.append((int(a_mod2[i][r]) + 2 * a_high) % (1 << t_bits))
            a_matrix.append(row)

        tilde_cols = [
            compute_effective_column_mod_2t(a_matrix, v_vec, x0_vec, t_bits)
            for v_vec in v_basis
        ]
        b_cols = tuple(tuple(c // 2 for c in col) for col in tilde_cols)
        tuple_counts[b_cols] = tuple_counts.get(b_cols, 0) + 1
        total_instances += 1
        total_adv += conditional_helstrom_advantage_from_rescaled_columns(
            b_cols, rescaled_h, t_bits - 1
        )

    expected_distinct_tuples = q_even ** m_wires
    counts_set = set(tuple_counts.values())
    exact_iid_uniform = (
        len(tuple_counts) == expected_distinct_tuples
        and len(counts_set) == 1
        and next(iter(counts_set)) * expected_distinct_tuples == total_instances
    )

    ensemble_mean_conditional_adv = total_adv / float(total_instances)
    rescaled_bcdv_bound = min(1.0, math.sqrt(((1 << m_wires) - 1.0) / float(q_even)))

    return {
        "n": n_rows,
        "t": t_bits,
        "K": k_cols,
        "m": m_wires,
        "q_even_sublattice_size": q_even,
        "total_upper_bit_instances": total_instances,
        "distinct_rescaled_column_tuples": len(tuple_counts),
        "expected_distinct_tuples": expected_distinct_tuples,
        "exact_iid_uniform_over_even_sublattice": exact_iid_uniform,
        "ensemble_mean_conditional_advantage": ensemble_mean_conditional_adv,
        "rescaled_bcdv_bound_q_even": rescaled_bcdv_bound,
        "bound_respected": ensemble_mean_conditional_adv <= rescaled_bcdv_bound + 1e-12,
    }


def generate_dcp_even_sublattice_parity_blindness_and_rescaling_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the even-sublattice parity blindness and rescaling bridge."""
    evenness_checks = [
        verify_even_effective_column_identity(
            a_matrix=[[3, 5, 2]],
            v_vec=[1, 1, 0],
            t_bits=3,
        ),
        verify_even_effective_column_identity(
            a_matrix=[[1, 3, 2], [2, 4, 5]],
            v_vec=[1, 1, 0],
            t_bits=3,
        ),
    ]

    t1_blindness_audit = verify_odd_target_impossibility_and_halving_isomorphism(
        a_matrix=[[1, 1]],
        v_basis=[[1, 1]],
        t_bits=1,
    )

    all_anchor_resonant_control = verify_odd_target_impossibility_and_halving_isomorphism(
        a_matrix=[[2, 0]],
        v_basis=[[1, 1]],
        t_bits=2,
    )

    half_anchor_resonant_control = verify_odd_target_impossibility_and_halving_isomorphism(
        a_matrix=[[1, 1]],
        v_basis=[[1, 1]],
        t_bits=2,
    )

    upper_bit_ensemble_checks = [
        verify_upper_bit_ensemble_rescaled_uniformity(
            a_mod2=[[1, 1, 0]],
            v_basis=[[1, 1, 0]],
            x0_vec=[0, 1, 0],
            t_bits=2,
        ),
        verify_upper_bit_ensemble_rescaled_uniformity(
            a_mod2=[[1, 1, 0]],
            v_basis=[[1, 1, 0]],
            x0_vec=[1, 0, 1],
            t_bits=3,
        ),
        verify_upper_bit_ensemble_rescaled_uniformity(
            a_mod2=[[1, 1, 1, 1]],
            v_basis=[[1, 1, 0, 0], [0, 0, 1, 1]],
            x0_vec=[0, 1, 1, 0],
            t_bits=2,
        ),
    ]

    all_passed = (
        all(c["in_mod2_kernel"] and c["all_effective_columns_even"] and c["halving_bijection_holds"] for c in evenness_checks)
        and t1_blindness_audit["odd_target_strictly_blind"]
        and t1_blindness_audit["mean_conditional_advantage"] == 0.0
        and all_anchor_resonant_control["odd_target_strictly_blind"]
        and all_anchor_resonant_control["halving_isomorphism_exact"]
        and abs(all_anchor_resonant_control["mean_conditional_advantage"] - 1.0) <= 1e-12
        and abs(all_anchor_resonant_control["unconditional_branch_contribution"] - 0.5) <= 1e-12
        and half_anchor_resonant_control["odd_target_strictly_blind"]
        and half_anchor_resonant_control["halving_isomorphism_exact"]
        and abs(half_anchor_resonant_control["mean_conditional_advantage"] - 0.5) <= 1e-12
        and abs(half_anchor_resonant_control["unconditional_branch_contribution"] - 0.25) <= 1e-12
        and all(
            u["exact_iid_uniform_over_even_sublattice"] and u["bound_respected"]
            for u in upper_bit_ensemble_checks
        )
    )

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "scope_constraints": {
            "applies_to": "Disjoint mod-2 kernel witness compression V_1, ..., V_m in ker(A mod 2) conditioned on the anchor subspace event y = (I_K, V) u",
            "does_not_claim": "General DCP impossibility or fixed-instance uniformity across anchors x_0",
            "reconciles": "Explains why effective columns lie in the index-2^n even sublattice (2 Z_{2^t})^n (isomorphic to Z_{2^{t-1}}^n of size Q_even = 2^{n(t-1)}), exhibits fixed-instance resonant controls (Adv_cond = 1.0 for A=[[2,0]] mod 4 and E_{x_0}[Adv_cond] = 0.5 for A=[[1,1]] mod 4), and proves exact IID uniformity of the halved columns B_j(x_0) over Z_{2^{t-1}}^n under uniform upper bits A^{(high)} = floor(A/2).",
        },
        "evenness_checks": evenness_checks,
        "t1_blindness_audit": t1_blindness_audit,
        "fixed_instance_controls": {
            "all_anchor_resonant_A_2_0_mod_4": all_anchor_resonant_control,
            "half_anchor_resonant_A_1_1_mod_4": half_anchor_resonant_control,
        },
        "upper_bit_ensemble_checks": upper_bit_ensemble_checks,
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
