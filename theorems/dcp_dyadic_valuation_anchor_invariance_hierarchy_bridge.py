"""DCP dyadic valuation and mod-2^k anchor-invariance hierarchy bridge.

Establishes for any matrix A in Z_{2^t}^{n x K}, any binary witness vector v in {0,1}^K,
and any dyadic modulus level 1 <= k <= t:

1. Exact Anchor-Invariance Criterion at Level k:
   The effective column
       tilde_A(v, x_0) = A v - 2 sum_{r in supp(v)} (x_0)_r A_{., r} mod 2^t
   satisfies tilde_A(v, x_0) == A v (mod 2^k) for ALL anchors x_0 in {0,1}^K
   if and only if every active column r in supp(v) satisfies:
       2 A_{., r} == 0 (mod 2^k)  <==>  A_{., r} == 0 (mod 2^{k-1}).

2. Immediate Consequences for Iterative Mod-2^k Elimination:
   - Level k = 1 (mod 2): Since 2^{k-1} = 1 divides every integer, tilde_A(v, x_0) == A v (mod 2)
     holds universally for every A, every v, and every x_0 in {0,1}^K.
   - Level k >= 2 (mod 2^k): Whenever supp(v) contains at least one column r with
     A_{i, r} not divisible by 2^{k-1}, flipping (x_0)_r in {0, 1} shifts tilde_A_i(v, x_0)
     by 2 * A_{i, r} != 0 (mod 2^k). Specifically, at k = 2 (mod 4), if supp(v) contains
     an odd entry A_{i, r} == 1 (mod 2), then tilde_A_i(v, x_0) mod 4 equals A_i v mod 4
     for exactly half of the anchors x_0 in {0,1}^K and (A_i v + 2) mod 4 for the other half.

3. Scoped Even-Column Constructive Control:
   When every column r in supp(v) IS divisible by 2^{k-1} (e.g. A = [[2, 2]] mod 4 with k = 2
   and v = (1, 1)^T), tilde_A(v, x_0) == A v == 0 (mod 4) holds deterministically across
   all 2^K anchors x_0 in {0,1}^K.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from typing import Any, Dict, List, Sequence, Tuple


THEOREM_ID = "dcp_dyadic_valuation_anchor_invariance_hierarchy_bridge"
SCHEMA_VERSION = "dcp-dyadic-valuation-anchor-invariance-hierarchy-bridge-v1"


def verify_dyadic_level_anchor_invariance(
    a_matrix: Sequence[Sequence[int]],
    v_vec: Sequence[int],
    t_bits: int,
    k_level: int,
) -> Dict[str, Any]:
    """Verify the exact equivalence between anchor invariance mod 2^k and A_{.,r} == 0 mod 2^{k-1} on supp(v)."""
    if not (1 <= k_level <= t_bits):
        raise ValueError("k_level must satisfy 1 <= k_level <= t_bits.")
    n_rows = len(a_matrix)
    k_cols = len(v_vec)
    mod_2k = 1 << k_level
    mod_2k_minus_1 = 1 << (k_level - 1)

    target_av_mod_2k = tuple(
        sum(int(a_matrix[i][r]) * int(v_vec[r]) for r in range(k_cols)) % mod_2k
        for i in range(n_rows)
    )

    support_cols_divisible_by_2k_minus_1 = all(
        (int(a_matrix[i][r]) % mod_2k_minus_1 == 0)
        for r in range(k_cols)
        if v_vec[r]
        for i in range(n_rows)
    )

    matching_anchor_count = 0
    total_anchors = 1 << k_cols
    observed_residues = set()

    for x0 in itertools.product((0, 1), repeat=k_cols):
        tilde_mod_2k = tuple(
            sum(
                int(v_vec[r]) * (1 - 2 * int(x0[r])) * int(a_matrix[i][r])
                for r in range(k_cols)
            )
            % mod_2k
            for i in range(n_rows)
        )
        observed_residues.add(tilde_mod_2k)
        if tilde_mod_2k == target_av_mod_2k:
            matching_anchor_count += 1

    anchor_invariant_mod_2k = matching_anchor_count == total_anchors
    equivalence_verified = (
        anchor_invariant_mod_2k == support_cols_divisible_by_2k_minus_1
    )

    return {
        "n": n_rows,
        "K": k_cols,
        "t": t_bits,
        "k_level": k_level,
        "mod_2k": mod_2k,
        "target_Av_mod_2k": list(target_av_mod_2k),
        "support_cols_divisible_by_2_to_k_minus_1": support_cols_divisible_by_2k_minus_1,
        "anchor_invariant_mod_2k": anchor_invariant_mod_2k,
        "matching_anchor_fraction": matching_anchor_count / float(total_anchors),
        "distinct_residues_mod_2k": len(observed_residues),
        "iff_characterization_verified": equivalence_verified,
    }


def generate_dcp_dyadic_valuation_anchor_invariance_hierarchy_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the dyadic valuation anchor-invariance hierarchy bridge."""
    # 1. Universal k=1 invariance on odd columns A = [[1, 3]] mod 8, v = [1, 1]
    level_1_universal = verify_dyadic_valuation_case_1 = verify_dyadic_level_anchor_invariance(
        a_matrix=[[1, 3]],
        v_vec=[1, 1],
        t_bits=3,
        k_level=1,
    )

    # 2. Level k=2 (mod 4) on odd columns A = [[1, 3]] mod 8, v = [1, 1]:
    # Even though A v = 4 == 0 (mod 4), active columns are odd (not 0 mod 2), so only 1/2 of anchors match 0 mod 4!
    level_2_odd_column_splitting = verify_dyadic_level_anchor_invariance(
        a_matrix=[[1, 3]],
        v_vec=[1, 1],
        t_bits=3,
        k_level=2,
    )

    # 3. Level k=2 (mod 4) constructive control on even active columns A = [[2, 6, 1]] mod 8, v = [1, 1, 0]:
    # Active columns 0 and 1 are even (0 mod 2), so tilde_A(v, x_0) == A v == 0 (mod 4) for 100% of anchors!
    level_2_even_column_constructive_control = verify_dyadic_level_anchor_invariance(
        a_matrix=[[2, 6, 1]],
        v_vec=[1, 1, 0],
        t_bits=3,
        k_level=2,
    )

    # 4. Level k=3 (mod 8) on Doubly-Even active columns A = [[4, 4, 3]] mod 8, v = [1, 1, 0]:
    # Active columns are 0 mod 4 (2^{3-1} = 4), so tilde_A(v, x_0) == 0 (mod 8) for 100% of anchors!
    level_3_doubly_even_constructive_control = verify_dyadic_level_anchor_invariance(
        a_matrix=[[4, 4, 3]],
        v_vec=[1, 1, 0],
        t_bits=3,
        k_level=3,
    )

    all_passed = (
        level_1_universal["iff_characterization_verified"]
        and level_1_universal["anchor_invariant_mod_2k"]
        and level_2_odd_column_splitting["iff_characterization_verified"]
        and not level_2_odd_column_splitting["anchor_invariant_mod_2k"]
        and abs(level_2_odd_column_splitting["matching_anchor_fraction"] - 0.5) < 1e-12
        and level_2_even_column_constructive_control["iff_characterization_verified"]
        and level_2_even_column_constructive_control["anchor_invariant_mod_2k"]
        and level_3_doubly_even_constructive_control["iff_characterization_verified"]
        and level_3_doubly_even_constructive_control["anchor_invariant_mod_2k"]
    )

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "scope_constraints": {
            "applies_to": "Dyadic modulus congruence tilde_A(v, x_0) == A v (mod 2^k) across anchors x_0 in {0,1}^K",
            "does_not_claim": "Failure of mod-2^k invariance when active columns r in supp(v) satisfy A_{.,r} == 0 (mod 2^{k-1})",
            "controls_included": "Includes universal k=1 invariance, odd-column k=2 50/50 residue splitting on A=[[1,3]] mod 8, even-column k=2 constructive invariance on A=[[2,6,1]] mod 8, and doubly-even k=3 constructive invariance on A=[[4,4,3]] mod 8.",
        },
        "level_1_universal_invariance": level_1_universal,
        "level_2_odd_column_splitting": level_2_odd_column_splitting,
        "level_2_even_column_constructive_control": level_2_even_column_constructive_control,
        "level_3_doubly_even_constructive_control": level_3_doubly_even_constructive_control,
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
