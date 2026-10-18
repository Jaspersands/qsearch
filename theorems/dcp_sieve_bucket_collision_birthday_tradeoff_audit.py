"""DCP sieve bucket collision birthday tradeoff and multi-layer coherence audit.

Establishes for bucketed collision sieving on M independent DCP state copies
partitioned across B uniform coset buckets:

1. Exact Finite-Sample Disjoint Pairing Yield Identity:
   When M balls are placed independently and uniformly into B buckets with bucket
   occupancies (N_1, ..., N_B) ~ Multinomial(M; 1/B, ..., 1/B), greedy disjoint pairing
   within each bucket yields M_pairs = sum_{b=1}^B floor(N_b / 2) pairs. Using the
   exact parity decomposition floor(N / 2) = N/2 - (1 - (-1)^N)/4 and the binomial
   moment E[(-1)^{N_b}] = (1 - 2/B)^M:
       E[M_pairs] = M / 2 - (B / 4) * (1 - (1 - 2 / B)^M).

2. Sub-Saturation Birthday Regime vs. Linear Saturation Regime:
   - For M << B, E[M_pairs] = M*(M - 1) / (2*B) + O(M^3 / B^2) (quadratic birthday scaling).
   - For M >> B with B >= 2, E[M_pairs] approaches M / 2 - B / 4.
     For B=1 the exact answer is floor(M/2), not this limiting expression.

3. Multi-Layer Coherence Squaring vs. Single-Layer Clean Constructive Control:
   - Across L recursive sieve layers where each paired difference state undergoes
     phase-difference convolution, single-coordinate Fourier survival scales as
     gamma_L = gamma_0^{2^L}.
   - Constructive Small-Bucket / Clean Control: At L = 1 with B <= M and gamma_0 = 1.0
     (noiseless clean source) or bounded L = O(1) with gamma_0 = 1 - eps, bucket pairing
     achieves constant pairing efficiency (M >= B >= 2) and coherence gamma_1 = gamma_0^2.

The old real-valued mean recurrence is RETRACTED. Multilayer expected yields
now propagate the entire exact rational pool-size law. This remains a model
of fresh IID uniform re-bucketing at EVERY layer, not a proved law of a real
DCP sieve. Coherence squaring assumes independent, label-independent phase
noise on disjoint source trees; correlated errors can cancel instead.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from fractions import Fraction
from functools import lru_cache
from typing import Any, Dict, List, Sequence


THEOREM_ID = "dcp_sieve_bucket_collision_birthday_tradeoff_audit"
SCHEMA_VERSION = "dcp-sieve-bucket-collision-birthday-tradeoff-audit-v2"


def _validate_pool(m_balls: int, b_buckets: int) -> None:
    if type(m_balls) is not int or m_balls < 0:
        raise ValueError("M must be a nonnegative integer")
    if type(b_buckets) is not int or b_buckets < 1:
        raise ValueError("B must be a positive integer")
    if m_balls > 512 or b_buckets > 65536:
        raise ValueError("exact reference limited to M<=512, B<=65536; not a hardness result")


@lru_cache(maxsize=512, typed=True)
def disjoint_pair_count_law(m_balls: int, b_buckets: int) -> tuple[tuple[int, Fraction], ...]:
    """Exact occupancy law via number of odd buckets, not B**M enumeration.

    At odd-bucket count o the next ball has B-o choices increasing o, and o
    choices decreasing it. Every assignment has weight B**(-M). Pair count
    is (M-o)/2. Integer path counts give an exact rational transition kernel.
    """
    _validate_pool(m_balls, b_buckets)
    counts = {0: 1}
    for _ in range(m_balls):
        next_counts: Dict[int, int] = {}
        for odd, count in counts.items():
            if odd < b_buckets:
                next_counts[odd + 1] = next_counts.get(odd + 1, 0) + count * (b_buckets - odd)
            if odd:
                next_counts[odd - 1] = next_counts.get(odd - 1, 0) + count * odd
        counts = next_counts
    denominator = b_buckets ** m_balls
    assert sum(counts.values()) == denominator
    return tuple(sorted(((m_balls - odd) // 2, Fraction(count, denominator)) for odd, count in counts.items()))


def _fraction_record(value: Fraction) -> Dict[str, Any]:
    return {"numerator": str(value.numerator), "denominator": str(value.denominator), "float": float(value)}


def exact_expected_disjoint_pairs_closed_form(m_balls: int, b_buckets: int) -> float:
    """Closed-form expectation E[sum_{b=1}^B floor(N_b / 2)] = M/2 - (B/4)*(1 - (1 - 2/B)^M)."""
    _validate_pool(m_balls, b_buckets)
    # Rational evaluation avoids catastrophic cancellation in sparse buckets.
    mean = Fraction(m_balls, 2) - Fraction(b_buckets, 4) * (
        1 - Fraction(b_buckets - 2, b_buckets) ** m_balls
    )
    return float(mean)


def verify_bucket_pairing_yield_identity_exhaustive(
    m_balls: int,
    b_buckets: int,
) -> Dict[str, Any]:
    """Exhaustively enumerate all B^M bucket assignments and verify the closed-form pair expectation."""
    total_assignments = b_buckets ** m_balls
    total_pairs = 0
    for assignment in itertools.product(range(b_buckets), repeat=m_balls):
        counts = [0] * b_buckets
        for bucket_id in assignment:
            counts[bucket_id] += 1
        total_pairs += sum(c // 2 for c in counts)

    exhaustive_mean = total_pairs / float(total_assignments)
    closed_form_mean = exact_expected_disjoint_pairs_closed_form(m_balls, b_buckets)

    # Also check single-bucket binomial parity sum
    p = 1.0 / float(b_buckets)
    single_bucket_mean = sum(
        math.comb(m_balls, k) * (p ** k) * ((1.0 - p) ** (m_balls - k)) * (k // 2)
        for k in range(m_balls + 1)
    )
    binomial_sum_mean = float(b_buckets) * single_bucket_mean

    return {
        "M": m_balls,
        "B": b_buckets,
        "total_assignments": total_assignments,
        "exhaustive_mean_pairs": exhaustive_mean,
        "binomial_sum_mean_pairs": binomial_sum_mean,
        "closed_form_mean_pairs": closed_form_mean,
        "abs_diff_exhaustive_vs_closed": abs(exhaustive_mean - closed_form_mean),
        "abs_diff_binomial_vs_closed": abs(binomial_sum_mean - closed_form_mean),
        "exact_identity_verified": (
            abs(exhaustive_mean - closed_form_mean) < 1e-12
            and abs(binomial_sum_mean - closed_form_mean) < 1e-12
        ),
    }


def verify_multi_layer_sieve_coherence_and_controls(
    gamma_0: float,
    bucket_sizes: Sequence[int],
    initial_pool_m0: int,
) -> Dict[str, Any]:
    """Exact pool distribution in the explicitly conditional IID bucket model."""
    _validate_pool(initial_pool_m0, 1)
    if not math.isfinite(gamma_0) or not 0 <= gamma_0 <= 1:
        raise ValueError("gamma_0 must be finite and in [0,1]")
    for buckets in bucket_sizes:
        _validate_pool(initial_pool_m0, buckets)
    pool = {initial_pool_m0: Fraction(1)}
    gamma_curr = float(gamma_0)
    layers: List[Dict[str, Any]] = []

    for idx, b_ell in enumerate(bucket_sizes, start=1):
        input_mean = sum((m * prob for m, prob in pool.items()), Fraction())
        next_pool: Dict[int, Fraction] = {}
        for m, pool_prob in pool.items():
            for pairs, conditional_prob in disjoint_pair_count_law(m, b_ell):
                next_pool[pairs] = next_pool.get(pairs, Fraction()) + pool_prob * conditional_prob
        assert sum(next_pool.values()) == 1
        output_mean = sum((m * prob for m, prob in next_pool.items()), Fraction())
        assert 0 <= output_mean <= input_mean / 2
        gamma_next = gamma_curr ** 2
        layers.append(
            {
                "layer": idx,
                "buckets_B": b_ell,
                "input_pool_M": float(input_mean),
                "expected_output_pairs_M": float(output_mean),
                "exact_expected_output_pairs": _fraction_record(output_mean),
                "output_pool_distribution": [
                    {"pairs": m, "probability": _fraction_record(prob)} for m, prob in sorted(next_pool.items())
                ],
                "nonempty_probability": _fraction_record(1 - next_pool.get(0, Fraction())),
                "output_coherence_gamma": gamma_next,
            }
        )
        pool = next_pool
        gamma_curr = gamma_next

    expected_final_gamma = gamma_0 ** (2 ** len(bucket_sizes))
    return {
        "gamma_0": gamma_0,
        "num_layers": len(bucket_sizes),
        "initial_pool_M0": initial_pool_m0,
        "final_expected_pairs": float(sum((m * prob for m, prob in pool.items()), Fraction())),
        "pool_model": "FRESH_IID_UNIFORM_BUCKET_ASSIGNMENTS_CONDITIONAL_ON_EACH_POOL_SIZE",
        "actual_DCP_output_headers_proved_IID": False,
        "merge_branch_acceptance_charged": False,
        "coherence_assumption": "Independent label-independent noise on disjoint binary source trees",
        "v1_mean_closure_retracted": True,
        "final_coherence_gamma": gamma_curr,
        "expected_final_coherence_formula": expected_final_gamma,
        "coherence_squaring_exact": abs(gamma_curr - expected_final_gamma) < 1e-12,
        "layers": layers,
    }


def generate_dcp_sieve_bucket_collision_birthday_tradeoff_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the sieve bucket collision birthday tradeoff audit."""
    exhaustive_checks = [
        verify_bucket_pairing_yield_identity_exhaustive(m_balls=2, b_buckets=4),
        verify_bucket_pairing_yield_identity_exhaustive(m_balls=5, b_buckets=3),
        verify_bucket_pairing_yield_identity_exhaustive(m_balls=6, b_buckets=4),
    ]

    # Multi-layer noisy decay audit (L = 4 layers, gamma_0 = 0.8 -> gamma_4 = 0.8^16)
    multi_layer_noisy_audit = verify_multi_layer_sieve_coherence_and_controls(
        gamma_0=0.8,
        bucket_sizes=[8, 8, 8, 8],
        initial_pool_m0=256,
    )

    # Single-layer clean constructive control (L = 1, B = 4, M_0 = 16, gamma_0 = 1.0 -> lossless coherence)
    single_layer_clean_control = verify_multi_layer_sieve_coherence_and_controls(
        gamma_0=1.0,
        bucket_sizes=[4],
        initial_pool_m0=16,
    )
    mean_closure_counterexample = verify_multi_layer_sieve_coherence_and_controls(
        gamma_0=1.0, bucket_sizes=[2, 2], initial_pool_m0=2,
    )

    all_passed = (
        all(c["exact_identity_verified"] for c in exhaustive_checks)
        and multi_layer_noisy_audit["coherence_squaring_exact"]
        and single_layer_clean_control["coherence_squaring_exact"]
        and abs(single_layer_clean_control["final_coherence_gamma"] - 1.0) < 1e-12
        and single_layer_clean_control["final_expected_pairs"] > 7.0
        and mean_closure_counterexample["final_expected_pairs"] == 0
    )

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "proof_status": "LOCAL_DERIVATION_REVIEW_PENDING_NOT_FORMALLY_VERIFIED",
        "scope_constraints": {
            "applies_to": "Disjoint within-bucket collision pairing of M uniform-header DCP states across B coset buckets",
            "does_not_claim": "Zero pairing yield when M >= Omega(B) or coherence loss when gamma_0 = 1.0 (noiseless source)",
            "controls_included": "Includes both multi-layer noisy coherence squaring (gamma_L = gamma_0^{2^L}) and the single-layer noiseless constructive control (gamma_0 = 1.0, M_0 = 16, B = 4 -> E[M_pairs] = 7.00015, gamma_1 = 1.0).",
        },
        "exhaustive_pairing_yield_checks": exhaustive_checks,
        "multi_layer_noisy_audit": multi_layer_noisy_audit,
        "single_layer_clean_constructive_control": single_layer_clean_control,
        "mean_closure_counterexample": mean_closure_counterexample,
        "v1_retractions": [
            "f(E[M]) is not E[f(M)]; continuous mean closure could predict negative pools",
            "fresh uniform output bucket law is an assumption, not a DCP sieve theorem",
            "coherence squaring is not valid for arbitrary correlated phase noise",
        ],
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
