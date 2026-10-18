r"""DCP mod-2 bucket-pairing disjoint kernel capacity and exact binomial expectation bridge.

Establishes the exact disjoint mod-2 kernel witness packing capacity of an
arbitrary binary projection A^{(0)} = A mod 2 in F_2^{n x K} and derives the
exact closed-form expected number of disjoint weight-<=2 kernel wires under
uniform random A^{(0)} in F_2^{n x K}:

1. Exact Within-Bucket Disjoint Pairing Law:
   Partition the K column indices {1, ..., K} into 2^n residue buckets
   B_c = {r : A^{(0)}_{., r} == c} for c in F_2^n, with sizes k_c = |B_c|
   (sum_{c in F_2^n} k_c = K).
     - Zero-bucket columns (c = 0^n): Each of the k_{0^n} columns is already a
       disjoint weight-1 mod-2 kernel witness (wt(v) = 1, requiring 0 CNOT gates
       and retaining full single-wire visibility gamma_0^1).
     - Non-zero buckets (c != 0^n): Pairing columns within each bucket B_c yields
       floor(k_c / 2) disjoint weight-2 mod-2 kernel witnesses (wt(v) = 2, requiring
       1 CNOT gate and visibility gamma_0^2), leaving at most one unpaired column
       per non-zero bucket (at most 2^n - 1 leftover columns in total).
   Consequently, for ANY matrix A in Z_{2^t}^{n x K}, within-bucket disjoint pairing
   extracts:
       m_{pair}(A) = k_{0^n} + sum_{c in F_2^n \ {0^n}} floor(k_c / 2)
                  >= (K - (2^n - 1)) / 2
   disjoint mod-2 kernel wires of Hamming weight <= 2, achieving asymptotic packing
   efficiency m_{pair}(A) / (K / 2) -> 1 as K / 2^n -> infinity.

2. Exact Closed-Form Ensemble Expectation Over Uniform A^{(0)} in F_2^{n x K}:
   For each non-zero bucket c != 0^n, k_c ~ Binomial(K, 2^{-n}), whose odd-parity
   probability is P(k_c is odd) = (1 - (1 - 2^{1 - n})^K) / 2. Summing
   E[floor(k_c / 2)] = (E[k_c] - P(k_c is odd)) / 2 over all 2^n - 1 non-zero
   buckets plus E[k_{0^n}] = K / 2^n yields the exact closed-form identity for
   all n >= 1 and K >= 1:
       E_{A^{(0)}}[m_{pair}(A^{(0)})]
           = (K / 2) + (K / 2^{n + 1}) - ((2^n - 1) / 4) * (1 - (1 - 2^{1 - n})^K).
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from typing import Any, Dict, List, Sequence, Tuple


THEOREM_ID = "dcp_multi_target_reusable_syndrome_bank_amortization_bridge"
SCHEMA_VERSION = "dcp-multi-target-reusable-syndrome-bank-amortization-bridge-v1"


def bucket_pair_disjoint_kernel_count(
    a_mod2_cols: Sequence[Sequence[int]],
) -> Dict[str, Any]:
    """Compute exact disjoint weight-<=2 mod-2 kernel count m_{pair}(A) by residue bucket pairing."""
    if not a_mod2_cols or not a_mod2_cols[0]:
        raise ValueError("nonempty column list required")
    k_cols = len(a_mod2_cols)
    n_rows = len(a_mod2_cols[0])
    buckets: Dict[Tuple[int, ...], List[int]] = {}
    for r, col in enumerate(a_mod2_cols):
        if len(col) != n_rows:
            raise ValueError("consistent column dimension n required")
        c_key = tuple(int(x) % 2 for x in col)
        buckets.setdefault(c_key, []).append(r)

    zero_key = tuple([0] * n_rows)
    wt1_count = len(buckets.get(zero_key, []))
    wt2_count = 0
    leftover_nonzero = 0
    for c_key, indices in buckets.items():
        if c_key == zero_key:
            continue
        wt2_count += len(indices) // 2
        leftover_nonzero += len(indices) % 2

    m_pair = wt1_count + wt2_count
    pigeonhole_lower_bound = (k_cols - ((1 << n_rows) - 1)) / 2.0

    return {
        "n": n_rows,
        "K": k_cols,
        "weight_1_zero_columns": wt1_count,
        "weight_2_bucket_pairs": wt2_count,
        "total_disjoint_kernel_wires_m_pair": m_pair,
        "unpaired_nonzero_columns": leftover_nonzero,
        "pigeonhole_lower_bound": pigeonhole_lower_bound,
        "lower_bound_satisfied": m_pair + 1e-12 >= pigeonhole_lower_bound,
    }


def expected_bucket_pair_kernel_count_closed_form(n_rows: int, k_cols: int) -> float:
    """Closed-form expectation K/2 + K/2^{n+1} - ((2^n - 1)/4) * (1 - (1 - 2^{1-n})^K)."""
    if type(n_rows) is not int or n_rows < 1 or type(k_cols) is not int or k_cols < 1:
        raise ValueError("n_rows >= 1 and k_cols >= 1 required")
    two_n = float(1 << n_rows)
    base = 1.0 - (2.0 ** (1 - n_rows))
    odd_prob_sum = ((two_n - 1.0) / 4.0) * (1.0 - (base ** k_cols))
    return (0.5 * float(k_cols)) + (float(k_cols) / (2.0 * two_n)) - odd_prob_sum


def verify_exact_ensemble_bucket_pair_expectation(
    n_rows: int,
    k_cols: int,
) -> Dict[str, Any]:
    """Exhaustively enumerate all 2^{n*K} binary matrices in F_2^{n x K} and verify the closed-form expectation."""
    if type(n_rows) is not int or n_rows < 1 or type(k_cols) is not int or k_cols < 1:
        raise ValueError("positive integer dimensions required")
    if n_rows * k_cols > 12:
        raise ValueError("exhaustive enumeration capped at n*K <= 12")

    all_cols = list(itertools.product((0, 1), repeat=n_rows))
    total_matrices = 0
    sum_m_pair = 0
    all_bounds_ok = True

    for col_tuple in itertools.product(all_cols, repeat=k_cols):
        res = bucket_pair_disjoint_kernel_count(col_tuple)
        if not res["lower_bound_satisfied"]:
            all_bounds_ok = False
        sum_m_pair += res["total_disjoint_kernel_wires_m_pair"]
        total_matrices += 1

    emp_mean = sum_m_pair / float(total_matrices)
    cf_mean = expected_bucket_pair_kernel_count_closed_form(n_rows, k_cols)

    return {
        "n": n_rows,
        "K": k_cols,
        "total_matrices_enumerated": total_matrices,
        "empirical_mean_m_pair": emp_mean,
        "closed_form_mean_m_pair": cf_mean,
        "formula_error": abs(emp_mean - cf_mean),
        "all_pigeonhole_bounds_satisfied": all_bounds_ok,
        "exact_expectation_verified": all_bounds_ok and abs(emp_mean - cf_mean) < 1e-12,
    }


def generate_dcp_multi_target_reusable_syndrome_bank_amortization_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the mod-2 bucket-pairing disjoint kernel capacity bridge."""
    ensemble_audits = [
        verify_exact_ensemble_bucket_pair_expectation(n_rows=1, k_cols=4),
        verify_exact_ensemble_bucket_pair_expectation(n_rows=1, k_cols=5),
        verify_exact_ensemble_bucket_pair_expectation(n_rows=2, k_cols=3),
        verify_exact_ensemble_bucket_pair_expectation(n_rows=2, k_cols=4),
        verify_exact_ensemble_bucket_pair_expectation(n_rows=3, k_cols=3),
    ]

    all_passed = (
        all(a["exact_expectation_verified"] for a in ensemble_audits)
        and abs(ensemble_audits[0]["empirical_mean_m_pair"] - 2.75) < 1e-12
        and abs(ensemble_audits[3]["empirical_mean_m_pair"] - (115.0 / 64.0)) < 1e-12
    )

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "proof_status": "LOCAL_DERIVATION_REVIEW_PENDING_NOT_FORMALLY_VERIFIED",
        "scope_constraints": {
            "applies_to": "Disjoint weight-<=2 mod-2 kernel witness packing via residue bucket pairing in F_2^{n x K}",
            "does_not_claim": "Polynomial packing efficiency when K << 2^n",
            "controls_included": "Includes exact exhaustive verification of E[m_{pair}] = K/2 + K/2^{n+1} - ((2^n-1)/4)*(1 - (1 - 2^{1-n})^K) across (n,K) in {(1,4), (1,5), (2,3), (2,4), (3,3)} and deterministic pigeonhole lower bound (K - (2^n - 1))/2.",
        },
        "ensemble_expectation_audits": ensemble_audits,
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
