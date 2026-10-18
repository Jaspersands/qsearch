r"""DCP odd-prime modulus Z_p vs. dyadic Z_{2^t} CNOT zero-sum carry-shift obstruction.

Establishes for any odd prime modulus p >= 3 (where gcd(2, p) == 1), any public
matrix A in Z_p^{n x K}, and any binary CNOT combination v in {0,1}^K:

1. Exact Odd-Prime Anchor-Invariance Criterion (Invertibility of 2 in F_p^*):
   For any anchor x_0 in {0,1}^K, the effective column under CNOT collimation is:
       tilde_A(v, x_0) == sum_{r in supp(v)} (1 - 2*(x_0)_r) A_{., r}
                       == A v - 2 * sum_{r in supp(v)} (x_0)_r A_{., r} (mod p).
   Because gcd(2, p) == 1 for every odd prime p >= 3 (so 2 is invertible mod p with
   2^{-1} == (p + 1) / 2 mod p), flipping a single anchor bit (x_0)_r shifts
   tilde_A(v, x_0) by -2 * A_{., r} (mod p). Therefore:
       tilde_A(v, x_0) == A v (mod p)  for all x_0 in {0,1}^K
           <==>  2 * A_{., r} == 0 (mod p)  for all r in supp(v)
           <==>  A_{., r} == 0 (mod p)      for all r in supp(v).
   Unlike Z_{2^t} (where 2 * A_{., r} == 0 mod 2 holds universally for all integers),
   over an odd prime modulus Z_p there is NO non-trivial anchor-invariant binary CNOT
   kernel elimination on non-zero columns.

2. Exact Monochrome-Syndrome Zero-Sum Law & Sub-Sum Escape:
   For a non-trivial zero-sum witness A v == 0 (mod p) of Hamming weight h = wt(v) >= 2:
     - The two monochrome anchor assignments x_0|_{supp(v)} in {0^h, 1^h} (corresponding
       to the single all-zero CNOT syndrome d = 0^{h-1} of probability 2^{-(h-1)}) always
       satisfy tilde_A(v, x_0) == +/- A v == 0 (mod p).
     - An additional non-monochrome anchor x_0|_{supp(v)} not in {0^h, 1^h} satisfies
       tilde_A(v, x_0) == 0 (mod p) if and only if the subset of columns where
       (x_0)_r == 1 is itself a proper zero-sum sub-witness:
           sum_{r in supp(v) : (x_0)_r == 1} A_{., r} == 0 (mod p).
     - Consequently, for any minimal (subset-sum-free) zero-sum witness v of weight h,
       the fraction of anchors achieving tilde_A(v, x_0) == 0 (mod p) is EXACTLY 2^{-(h-1)}.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from typing import Any, Dict, List, Sequence, Tuple


THEOREM_ID = "dcp_odd_prime_modulus_cnot_carry_shift_obstruction"
SCHEMA_VERSION = "dcp-odd-prime-modulus-cnot-carry-shift-obstruction-v1"


def _validate_odd_prime(p_mod: int) -> None:
    if type(p_mod) is not int or p_mod < 3 or (p_mod % 2) == 0:
        raise ValueError("p_mod must be an odd integer >= 3")
    for d in range(3, int(math.isqrt(p_mod)) + 1, 2):
        if (p_mod % d) == 0:
            raise ValueError("p_mod must be prime")


def verify_odd_prime_anchor_invariance_and_minimal_zero_sum_law(
    a_matrix: Sequence[Sequence[int]],
    v_vec: Sequence[int],
    p_mod: int,
) -> Dict[str, Any]:
    """Verify exact iff conditions for anchor invariance mod p and exact 2^{-(h-1)} zero-sum fraction on minimal witnesses."""
    _validate_odd_prime(p_mod)
    n_rows = len(a_matrix)
    k_cols = len(v_vec)
    supp = [r for r in range(k_cols) if int(v_vec[r]) == 1]
    h_wt = len(supp)
    if h_wt == 0:
        raise ValueError("v_vec must be non-zero")

    target_av = tuple(
        sum(int(a_matrix[i][r]) for r in supp) % p_mod for i in range(n_rows)
    )
    all_supp_cols_zero_mod_p = all(
        (int(a_matrix[i][r]) % p_mod) == 0 for r in supp for i in range(n_rows)
    )

    # Check if any non-empty proper subset S subsetneq supp sums to 0 mod p
    has_proper_zero_sum_subset = False
    for s_size in range(1, h_wt):
        for sub in itertools.combinations(supp, s_size):
            if all((sum(int(a_matrix[i][r]) for r in sub) % p_mod) == 0 for i in range(n_rows)):
                has_proper_zero_sum_subset = True
                break

    total_anchors = 1 << k_cols
    matching_target_count = 0
    zero_tilde_count = 0
    sub_witness_iff_verified = True

    for x0 in itertools.product((0, 1), repeat=k_cols):
        tilde_a = tuple(
            sum((1 - 2 * int(x0[r])) * int(a_matrix[i][r]) for r in supp) % p_mod
            for i in range(n_rows)
        )
        if tilde_a == target_av:
            matching_target_count += 1
        is_zero_tilde = all(c == 0 for c in tilde_a)
        if is_zero_tilde:
            zero_tilde_count += 1

        if all(c == 0 for c in target_av):
            # When Av == 0 mod p, tilde_A(v, x0) == -2 * sum_{r in supp: x0_r=1} A_{.,r} == 0 mod p
            # iff sum_{r in supp: x0_r=1} A_{.,r} == 0 mod p!
            ones_sub_sum_zero = all(
                (sum(int(a_matrix[i][r]) for r in supp if x0[r] == 1) % p_mod) == 0
                for i in range(n_rows)
            )
            if is_zero_tilde != ones_raw_iff(ones_sub_sum_zero):
                sub_witness_iff_verified = False

    anchor_invariant = matching_target_count == total_anchors
    zero_fraction = zero_tilde_count / float(total_anchors)
    expected_minimal_fraction = 2.0 ** (-(h_wt - 1))

    return {
        "p_mod": p_mod,
        "n": n_rows,
        "K": k_cols,
        "hamming_weight_h": h_wt,
        "target_Av_mod_p": list(target_av),
        "all_support_cols_zero_mod_p": all_supp_cols_zero_mod_p,
        "anchor_invariant_mod_p": anchor_invariant,
        "invariance_iff_zero_columns_verified": anchor_invariant == all_supp_cols_zero_mod_p,
        "has_proper_zero_sum_subset": has_proper_zero_sum_subset,
        "zero_tilde_anchor_fraction": zero_fraction,
        "monochrome_2_to_minus_h_minus_1_fraction": expected_minimal_fraction,
        "sub_witness_characterization_verified": sub_witness_iff_verified,
        "minimal_witness_exact_monochrome_fraction_verified": (
            (abs(zero_fraction - expected_minimal_fraction) < 1e-12)
            if (all(c == 0 for c in target_av) and not has_proper_zero_sum_subset)
            else True
        ),
    }


def ones_raw_iff(val: bool) -> bool:
    return bool(val)


def generate_dcp_odd_prime_modulus_cnot_carry_shift_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the odd-prime modulus CNOT carry-shift obstruction."""
    # 1. Minimal weight-2 zero-sum witness mod p=5: A = [[1, 4]], v = [1, 1] -> Av = 5 == 0 mod 5
    # Only monochrome x0 in {(0,0), (1,1)} give tilde_A == 0 mod 5 (fraction 2^{-(2-1)} = 1/2)
    p5_minimal_wt2 = verify_odd_prime_anchor_invariance_and_minimal_zero_sum_law(
        a_matrix=[[1, 4]],
        v_vec=[1, 1],
        p_mod=5,
    )

    # 2. Minimal weight-3 zero-sum witness mod p=7: A = [[1, 2, 4]], v = [1, 1, 1] -> Av = 7 == 0 mod 7
    # Proper subsets have sums {1, 2, 4, 3, 5, 6} != 0 mod 7, so zero fraction is exactly 2^{-(3-1)} = 1/4!
    p7_minimal_wt3 = verify_odd_prime_anchor_invariance_and_minimal_zero_sum_law(
        a_matrix=[[1, 2, 4]],
        v_vec=[1, 1, 1],
        p_mod=7,
    )

    # 3. Non-minimal weight-4 zero-sum witness mod p=5: A = [[1, 4, 2, 3]], v = [1, 1, 1, 1]
    # Proper subset {0, 1} sums to 1+4 = 5 == 0 mod 5, doubling zero fraction from 1/8 to 1/4!
    p5_composite_wt4 = verify_odd_prime_anchor_invariance_and_minimal_zero_sum_law(
        a_matrix=[[1, 4, 2, 3]],
        v_vec=[1, 1, 1, 1],
        p_mod=5,
    )

    # 4. Trivial zero-column constructive control mod p=5: A = [[0, 0, 3]], v = [1, 1, 0] -> 100% anchor invariant
    p5_zero_col_control = verify_odd_prime_anchor_invariance_and_minimal_zero_sum_law(
        a_matrix=[[0, 0, 3]],
        v_vec=[1, 1, 0],
        p_mod=5,
    )

    all_passed = (
        p5_minimal_wt2["invariance_iff_zero_columns_verified"]
        and not p5_minimal_wt2["anchor_invariant_mod_p"]
        and p5_minimal_wt2["minimal_witness_exact_monochrome_fraction_verified"]
        and abs(p5_minimal_wt2["zero_tilde_anchor_fraction"] - 0.5) < 1e-12
        and p7_minimal_wt3["invariance_iff_zero_columns_verified"]
        and p7_minimal_wt3["minimal_witness_exact_monochrome_fraction_verified"]
        and abs(p7_minimal_wt3["zero_tilde_anchor_fraction"] - 0.25) < 1e-12
        and p5_composite_wt4["has_proper_zero_sum_subset"]
        and p5_composite_wt4["sub_witness_characterization_verified"]
        and abs(p5_composite_wt4["zero_tilde_anchor_fraction"] - 0.25) < 1e-12
        and p5_zero_col_control["invariance_iff_zero_columns_verified"]
        and p5_zero_col_control["anchor_invariant_mod_p"]
    )

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "proof_status": "LOCAL_DERIVATION_REVIEW_PENDING_NOT_FORMALLY_VERIFIED",
        "scope_constraints": {
            "applies_to": "Binary CNOT witness compression over odd prime moduli Z_p (p >= 3)",
            "does_not_claim": "Inability to use known non-zero syndrome-dependent effective labels tilde_A(v, y_syn) or qutrit/p-dit modular adders",
            "controls_included": "Includes minimal wt=2 (p=5, fraction 1/2) and wt=3 (p=7, fraction 1/4) zero-sum witnesses, composite wt=4 sub-witness escape (fraction 1/4 > 1/8), and zero-column anchor-invariance control.",
        },
        "p5_minimal_wt2_audit": p5_minimal_wt2,
        "p7_minimal_wt3_audit": p7_minimal_wt3,
        "p5_composite_wt4_subwitness_control": p5_composite_wt4,
        "p5_zero_column_invariance_control": p5_zero_col_control,
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
