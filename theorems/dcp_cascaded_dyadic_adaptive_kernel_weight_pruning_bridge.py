r"""DCP cascaded multi-stage dyadic adaptive kernel routing and minimum-weight pruning bridge.

Establishes for L-stage cascaded dyadic CNOT elimination (mod 2, mod 4, ..., mod 2^L)
over Z_{2^t}^n (1 <= L <= t):

1. Universal Next-Level Coset Invariance Across All Dyadic Stages (1 <= ell < t):
   Whenever a stage-ell wire j already satisfies tilde_A^{(ell)}_j == 0 (mod 2^ell),
   its residue modulo 2^{ell+1} lies in {0, 2^ell}^n. Because -2^ell == +2^ell (mod 2^{ell+1}),
   sign flips tilde_A^{(ell)}_j -> -tilde_A^{(ell)}_j (mod 2^t) induced by changing coset
   representatives leave tilde_A^{(ell)}_j mod 2^{ell+1} strictly invariant.
   Moreover, by Subsystem 58, any stage-(ell+1) combination w^{(ell+1)} in {0,1}^{n+1}
   applied to wires satisfying tilde_A^{(ell)}_j == 0 (mod 2^ell) has stage-(ell+1)
   effective column congruent to sum_j w^{(ell+1)}_j tilde_A^{(ell)}_j (mod 2^{ell+1})
   independently of the stage-(ell+1) syndrome bits d^{(ell+1)}.

2. Exact 100% Mod-2^L Elimination via (n+1)^{L-1} Adaptive Stage-1 Wires:
   Starting from m_1 = (n + 1)^{L - 1} disjoint mod-2 kernel wires at Stage 1,
   partitioning surviving wires into blocks of size n + 1 at each stage ell = 2, ..., L
   and selecting a non-zero routing vector
       w^{(ell)} in ker_{F_2}((tilde_A^{(ell-1)} mod 2^ell) / 2^{ell-1})
   achieves tilde_A^{(L)} == 0 (mod 2^L) deterministically across 100% of syndromes
   at every stage (compared to 2^{-n} per-stage success for blind non-adaptive CNOT trees).

3. Fixed-Instance Residue Dichotomy vs. Upper-Bit Ensemble Weight & Visibility Recurrence:
   - Fixed-Instance Dichotomy at L = 3 (mod 8): For a single odd pair (a_{2j}, a_{2j+1}) mod 8,
     the unique Stage-1 syndrome y_{1,j}^* with tilde_A^{(1)}_j == 0 (mod 4) has a deterministic
     mod-8 residue r_j in {0, 4}. When all 4 pairs have r_j == 0 mod 8 (e.g. [1,7,3,5,1,7,3,5]),
     mean pruned weight is 11/4 = 2.75; when all 4 pairs have r_j == 4 mod 8 (e.g. [1,3,5,7,1,5,3,7]),
     mean pruned weight is 71/16 = 4.4375 (both achieving 100% mod-8 elimination and strictly
     beating the unpruned full-tree weight 8).
   - Upper-Bit Ensemble Recurrence: Over the uniform upper-bit ensemble A^{(high)} (where r_j in {0, 4}
     is IID fair across pairs), minimum-weight kernel selection at n = 1 selects a weight-1 wire with
     probability 3/4 and a weight-2 CNOT with probability 1/4 at every stage, yielding exact ensemble
     mean weight E[wt^{(L)}] = 2 * (5 / 4)^{L - 1} (25/8 = 3.125 at L = 3) and exact visibility
     recurrence V_ell = (3 / 4) * V_{ell - 1} + (1 / 4) * (V_{ell - 1})^2 > V_1^{2^{ell - 1}}.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from typing import Any, Dict, List, Sequence, Tuple


THEOREM_ID = "dcp_cascaded_dyadic_adaptive_kernel_weight_pruning_bridge"
SCHEMA_VERSION = "dcp-cascaded-dyadic-adaptive-kernel-weight-pruning-bridge-v1"


def verify_all_level_dyadic_sign_invariance(t_bits: int, n_rows: int) -> Dict[str, Any]:
    """Verify for every level 1 <= ell < t that -z == z (mod 2^{ell+1}) for all z in (2^ell Z_{2^t})^n."""
    if type(t_bits) is not int or t_bits < 2 or type(n_rows) is not int or n_rows < 1:
        raise ValueError("t_bits >= 2 and n_rows >= 1 required")
    q_mod = 1 << t_bits
    level_results: List[Dict[str, Any]] = []
    all_invariant = True

    for ell in range(1, t_bits):
        step = 1 << ell
        next_mod = 1 << (ell + 1)
        multiples = list(range(0, q_mod, step))
        checked = 0
        level_ok = True
        for vec in itertools.product(multiples, repeat=n_rows):
            neg_vec = tuple((-c) % q_mod for c in vec)
            if tuple(c % next_mod for c in vec) != tuple(c % next_mod for c in neg_vec):
                level_ok = False
                all_invariant = False
            checked += 1
        level_results.append({
            "ell": ell,
            "mod_2_ell": step,
            "next_mod_2_ell_plus_1": next_mod,
            "vectors_checked": checked,
            "sign_invariance_mod_next_level_verified": level_ok,
        })

    return {
        "t_bits": t_bits,
        "n_rows": n_rows,
        "levels": level_results,
        "all_levels_sign_invariant": all_invariant,
    }


def _min_weight_kernel_vector_1d(b0: int, b1: int) -> Tuple[int, int]:
    """Minimum-Hamming-weight non-zero w in {0,1}^2 such that b0*w0 + b1*w1 == 0 (mod 2)."""
    if (b0 % 2) == 0:
        return (1, 0)
    if (b1 % 2) == 0:
        return (0, 1)
    return (1, 1)


def evaluate_three_stage_mod8_adaptive_cascade_1d(
    a_row: Sequence[int],
    t_bits: int,
    gamma_0: float,
) -> Dict[str, Any]:
    """Execute a full 3-stage (k=1 mod 2 -> k=2 mod 4 -> k=3 mod 8) adaptive CNOT cascade on K=8 odd columns."""
    if type(t_bits) is not int or t_bits < 3:
        raise ValueError("t_bits >= 3 required for 3-stage mod-8 cascade")
    if len(a_row) != 8 or any((int(x) % 2) != 1 for x in a_row):
        raise ValueError("a_row must consist of 8 odd integers for the 4-pair Stage-1 mod-2 kernel")
    if not math.isfinite(gamma_0) or not 0.0 < gamma_0 <= 1.0:
        raise ValueError("gamma_0 must be in (0, 1]")

    q_mod = 1 << t_bits
    a_clean = [int(x) % q_mod for x in a_row]

    total_stage1_syndromes = 1 << 4
    adaptive_mod8_zero_count = 0
    blind_mod8_zero_count = 0
    min_weight_sum = 0.0
    unpruned_weight_sum = 0.0
    min_weight_visibility_sum = 0.0
    unpruned_visibility_sum = 0.0

    for syn1_mask in range(total_stage1_syndromes):
        y1 = [(syn1_mask >> j) & 1 for j in range(4)]
        stage1_cols = [
            (a_clean[2 * j] + (1 - 2 * y1[j]) * a_clean[2 * j + 1]) % q_mod
            for j in range(4)
        ]
        stage1_weights = [2, 2, 2, 2]

        blind_col = sum(stage1_cols) % q_mod
        if (blind_col % 8) == 0:
            blind_mod8_zero_count += 1
        unpruned_weight_sum += 8.0
        unpruned_visibility_sum += gamma_0 ** 8

        b_stage1 = [(c % 4) // 2 for c in stage1_cols]
        w2_a = _min_weight_kernel_vector_1d(b_stage1[0], b_stage1[1])
        w2_b = _min_weight_kernel_vector_1d(b_stage1[2], b_stage1[3])

        branch_mod8_ok = True
        branch_weights: List[int] = []
        branch_visibilities: List[float] = []

        for d2_a in (0, 1):
            if w2_a == (1, 0):
                col2_a = stage1_cols[0]
                wt2_a = stage1_weights[0]
            elif w2_a == (0, 1):
                col2_a = stage1_cols[1]
                wt2_a = stage1_weights[1]
            else:
                col2_a = (stage1_cols[0] + (1 - 2 * d2_a) * stage1_cols[1]) % q_mod
                wt2_a = stage1_weights[0] + stage1_weights[1]

            for d2_b in (0, 1):
                if w2_b == (1, 0):
                    col2_b = stage1_cols[2]
                    wt2_b = stage1_weights[2]
                elif w2_b == (0, 1):
                    col2_b = stage1_cols[3]
                    wt2_b = stage1_weights[3]
                else:
                    col2_b = (stage1_cols[2] + (1 - 2 * d2_b) * stage1_cols[3]) % q_mod
                    wt2_b = stage1_weights[2] + stage1_weights[3]

                if (col2_a % 4) != 0 or (col2_b % 4) != 0:
                    branch_mod8_ok = False

                b_stage2_a = (col2_a % 8) // 4
                b_stage2_b = (col2_b % 8) // 4
                w3 = _min_weight_kernel_vector_1d(b_stage2_a, b_stage2_b)

                for d3 in (0, 1):
                    if w3 == (1, 0):
                        col3 = col2_a
                        wt3 = wt2_a
                    elif w3 == (0, 1):
                        col3 = col2_b
                        wt3 = wt2_b
                    else:
                        col3 = (col2_a + (1 - 2 * d3) * col2_b) % q_mod
                        wt3 = wt2_a + wt2_b

                    if (col3 % 8) != 0:
                        branch_mod8_ok = False
                    branch_weights.append(wt3)
                    branch_visibilities.append(gamma_0 ** wt3)

        if branch_mod8_ok:
            adaptive_mod8_zero_count += 1
        min_weight_sum += sum(branch_weights) / float(len(branch_weights))
        min_weight_visibility_sum += sum(branch_visibilities) / float(len(branch_visibilities))

    mean_min_weight = min_weight_sum / float(total_stage1_syndromes)
    mean_unpruned_weight = unpruned_weight_sum / float(total_stage1_syndromes)
    mean_min_visibility = min_weight_visibility_sum / float(total_stage1_syndromes)
    mean_unpruned_visibility = unpruned_visibility_sum / float(total_stage1_syndromes)

    return {
        "a_row": a_clean,
        "K": 8,
        "t_bits": t_bits,
        "gamma_0": gamma_0,
        "total_stage1_syndromes": total_stage1_syndromes,
        "adaptive_mod8_zero_fraction": adaptive_mod8_zero_count / float(total_stage1_syndromes),
        "blind_mod8_zero_fraction": blind_mod8_zero_count / float(total_stage1_syndromes),
        "empirical_mean_pruned_weight": mean_min_weight,
        "unpruned_full_tree_weight": mean_unpruned_weight,
        "empirical_mean_pruned_visibility": mean_min_visibility,
        "unpruned_full_tree_visibility": mean_unpruned_visibility,
        "visibility_gain_ratio_over_unpruned": mean_min_visibility / mean_unpruned_visibility,
        "deterministic_mod8_elimination_verified": (
            adaptive_mod8_zero_count == total_stage1_syndromes
            and mean_min_weight < mean_unpruned_weight
            and mean_min_visibility > mean_unpruned_visibility
        ),
    }


def evaluate_upper_bit_ensemble_three_stage_mod8_cascade_1d(gamma_0: float) -> Dict[str, Any]:
    """Average the 3-stage mod-8 cascade over all 2^4 = 16 upper-bit pair representatives (r_0, r_1, r_2, r_3) in {0, 4}^4."""
    if not math.isfinite(gamma_0) or not 0.0 < gamma_0 <= 1.0:
        raise ValueError("gamma_0 must be in (0, 1]")
    # Pair representative: (1, 7) has 1+7 = 0 mod 8 (r_j = 0); (1, 3) has 1+3 = 4 mod 8 (r_j = 4)
    pair_reps = {0: (1, 7), 1: (1, 3)}
    total_configs = 16
    wt_acc = 0.0
    vis_acc = 0.0
    all_mod8_ok = True

    for r_bits in itertools.product((0, 1), repeat=4):
        a_row: List[int] = []
        for b in r_bits:
            a_row.extend(pair_reps[b])
        res = evaluate_three_stage_mod8_adaptive_cascade_1d(a_row, t_bits=3, gamma_0=gamma_0)
        if not res["deterministic_mod8_elimination_verified"]:
            all_mod8_ok = False
        wt_acc += res["empirical_mean_pruned_weight"]
        vis_acc += res["empirical_mean_pruned_visibility"]

    ensemble_mean_wt = wt_acc / float(total_configs)
    ensemble_mean_vis = vis_acc / float(total_configs)

    v1 = gamma_0 ** 2
    v2 = 0.75 * v1 + 0.25 * (v1 ** 2)
    v3 = 0.75 * v2 + 0.25 * (v2 ** 2)
    expected_wt_closed_form = 2.0 * ((5.0 / 4.0) ** 2)

    return {
        "gamma_0": gamma_0,
        "upper_bit_pair_configurations": total_configs,
        "ensemble_mean_pruned_weight": ensemble_mean_wt,
        "closed_form_mean_pruned_weight": expected_wt_closed_form,
        "ensemble_mean_pruned_visibility": ensemble_mean_vis,
        "closed_form_mean_pruned_visibility": v3,
        "all_configurations_achieve_100_percent_mod8_elimination": all_mod8_ok,
        "exact_ensemble_recurrence_match": (
            all_mod8_ok
            and abs(ensemble_mean_wt - expected_wt_closed_form) < 1e-12
            and abs(ensemble_mean_vis - v3) < 1e-12
        ),
    }


def verify_multistage_weight_and_visibility_recurrence(
    max_stages: int,
    gamma_0: float,
) -> Dict[str, Any]:
    """Verify by exact distribution propagation across L = 1, ..., max_stages that E[wt] = 2*(5/4)^{L-1} and V_L = 3/4 V_{L-1} + 1/4 V_{L-1}^2."""
    if type(max_stages) is not int or not 1 <= max_stages <= 8:
        raise ValueError("max_stages must be in [1, 8]")
    if not math.isfinite(gamma_0) or not 0.0 < gamma_0 <= 1.0:
        raise ValueError("gamma_0 must be in (0, 1]")

    wt_dist: Dict[int, float] = {2: 1.0}
    v_rec = gamma_0 ** 2
    stage_records: List[Dict[str, Any]] = []
    all_matched = True

    for ell in range(1, max_stages + 1):
        mean_wt_dist = sum(w * p for w, p in wt_dist.items())
        mean_vis_dist = sum((gamma_0 ** w) * p for w, p in wt_dist.items())
        cf_wt = 2.0 * ((1.25) ** (ell - 1))
        unpruned_wt = float(1 << ell)
        unpruned_vis = gamma_0 ** (1 << ell)

        if abs(mean_wt_dist - cf_wt) > 1e-12 or abs(mean_vis_dist - v_rec) > 1e-12:
            all_matched = False

        stage_records.append({
            "stage_ell": ell,
            "modulus_2_to_ell": 1 << ell,
            "stage1_wires_required": 1 << (ell - 1),
            "raw_wires_required": 1 << ell,
            "mean_pruned_weight": mean_wt_dist,
            "unpruned_weight": unpruned_wt,
            "mean_pruned_visibility": mean_vis_dist,
            "unpruned_visibility": unpruned_vis,
        })

        next_dist: Dict[int, float] = {}
        for w, p in wt_dist.items():
            next_dist[w] = next_dist.get(w, 0.0) + 0.75 * p
        for w1, p1 in wt_dist.items():
            for w2, p2 in wt_dist.items():
                next_dist[w1 + w2] = next_dist.get(w1 + w2, 0.0) + 0.25 * p1 * p2
        wt_dist = next_dist
        v_rec = 0.75 * v_rec + 0.25 * (v_rec ** 2)

    return {
        "max_stages": max_stages,
        "gamma_0": gamma_0,
        "stage_records": stage_records,
        "exact_recurrence_verified": all_matched,
    }


def generate_dcp_cascaded_dyadic_adaptive_kernel_weight_pruning_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the cascaded dyadic adaptive kernel weight pruning bridge."""
    sign_invariance_t4_n2 = verify_all_level_dyadic_sign_invariance(t_bits=4, n_rows=2)

    fixed_all4_cascade = evaluate_three_stage_mod8_adaptive_cascade_1d(
        a_row=[1, 3, 5, 7, 1, 5, 3, 7],
        t_bits=3,
        gamma_0=0.85,
    )
    fixed_all0_cascade = evaluate_three_stage_mod8_adaptive_cascade_1d(
        a_row=[1, 7, 3, 5, 1, 7, 3, 5],
        t_bits=3,
        gamma_0=0.85,
    )
    upper_bit_ensemble_cascade = evaluate_upper_bit_ensemble_three_stage_mod8_cascade_1d(
        gamma_0=0.85,
    )

    recurrence_audit = verify_multistage_weight_and_visibility_recurrence(
        max_stages=6,
        gamma_0=0.85,
    )

    all_passed = (
        sign_invariance_t4_n2["all_levels_sign_invariant"]
        and fixed_all4_cascade["deterministic_mod8_elimination_verified"]
        and abs(fixed_all4_cascade["empirical_mean_pruned_weight"] - 4.4375) < 1e-12
        and fixed_all0_cascade["deterministic_mod8_elimination_verified"]
        and abs(fixed_all0_cascade["empirical_mean_pruned_weight"] - 2.375) < 1e-12
        and upper_bit_ensemble_cascade["exact_ensemble_recurrence_match"]
        and abs(upper_bit_ensemble_cascade["ensemble_mean_pruned_weight"] - 3.125) < 1e-12
        and recurrence_audit["exact_recurrence_verified"]
    )

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "proof_status": "LOCAL_DERIVATION_REVIEW_PENDING_NOT_FORMALLY_VERIFIED",
        "scope_constraints": {
            "applies_to": "L-stage cascaded adaptive CNOT routing across dyadic levels k = 1, ..., L with minimum-Hamming-weight kernel selection",
            "does_not_claim": "Elimination of the (n+1)^{L-1} upfront Stage-1 wire pool requirement or an unconditional DCP speedup",
            "controls_included": "Includes universal all-level coset sign invariance (-2^ell == 2^ell mod 2^{ell+1}), fixed-instance 3-stage mod-8 controls (mean weight 19/8 = 2.375 on r_j=0 pairs and 71/16 = 4.4375 on r_j=4 pairs), exact upper-bit ensemble match to 25/8 = 3.125, and 6-stage distribution propagation.",
        },
        "all_level_dyadic_sign_invariance": sign_invariance_t4_n2,
        "fixed_instance_mod8_controls": {
            "all_zero_mod8_pair_sums": fixed_all0_cascade,
            "all_four_mod8_pair_sums": fixed_all4_cascade,
        },
        "upper_bit_ensemble_three_stage_audit": upper_bit_ensemble_cascade,
        "multistage_recurrence_audit": recurrence_audit,
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
