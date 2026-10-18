from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import itertools
import json
import math
from pathlib import Path
import sys
from typing import Any

import numpy as np
from flint import nmod_mat

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.planted_qary_multiprobe_gl_rank_saturation_bridge import (
    exact_projected_rank_probability,
    gf_prime_rank,
)


SCHEMA_VERSION = "2026-04-12.planted-qary-dual-intersection-cascade-bridge.v1"
DEFAULT_CONTRACT_PATH = (
    ROOT
    / "research"
    / "hypotheses"
    / "planted_qary_dual_intersection_cascade_bridge_contract.json"
)
DEFAULT_ARTIFACT_PATH = (
    ROOT
    / "research"
    / "reductions"
    / "planted_qary_dual_intersection_cascade_bridge.json"
)
DEFAULT_DOC_PATH = (
    ROOT / "research" / "PLANTED_QARY_DUAL_INTERSECTION_CASCADE_BRIDGE.md"
)


def canonical_sha256(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _frac_str(val: Fraction) -> str:
    return f"{val.numerator}/{val.denominator}"


def load_contract(path: Path = DEFAULT_CONTRACT_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _prime_field(q: int) -> None:
    if (type(q) is not int or not 2 <= q <= 127
            or any(q % p == 0 for p in range(2, math.isqrt(q) + 1))):
        raise ValueError("prime q<=127 required; composite rings/extension fields unsupported")


def recover_measured_span(samples, *, q: int, n: int, shared_affine_offset=False):
    """Sample-only baseline: no generator, secret offset, dual or density access.

    With a fixed unknown affine offset, subtract ONE observed anchor. Fresh
    independently randomized offsets do not satisfy this source contract.
    Returning a span does not certify that the samples span the unknown code.
    """
    _prime_field(q)
    if type(n) is not int or n < 1 or type(shared_affine_offset) is not bool:
        raise ValueError("positive integer n and explicit boolean offset mode required")
    rows = [list(row) for row in samples]
    if any(len(row) != n or any(type(x) is not int or not 0 <= x < q for x in row)
           for row in rows):
        raise ValueError("canonical measured prime-field vectors required")
    count = len(rows)
    if shared_affine_offset and rows:
        anchor = rows[0]
        rows = [[(x-y) % q for x,y in zip(row,anchor)] for row in rows[1:]]
    if rows:
        reduced, rank = nmod_mat(rows, q).rref()
        basis = [[int(reduced[i,j]) for j in range(n)] for i in range(rank)]
    else:
        basis, rank = [], 0
    return {"observed_span_basis": basis, "observed_rank": rank,
            "measured_input_copies": count, "elimination_rows": len(rows),
            "full_unknown_subspace_recovery_certified": False,
            "requires_shared_offset_if_affine": shared_affine_offset,
            "coherent_operations_after_measurement": 0,
            "known_generator_or_offset_supplied_to_recovery": False}


def measured_span_recovery_probability(q: int, dimension: int, copies: int,
                                       *, shared_affine_offset=False) -> Fraction:
    """Exact source-average probability, not a data-dependent certificate."""
    _prime_field(q)
    if (type(dimension) is not int or dimension < 0 or type(copies) is not int
            or copies < 0 or type(shared_affine_offset) is not bool):
        raise ValueError("nonnegative integer dimensions/copies and boolean mode required")
    effective = max(0, copies-int(shared_affine_offset))
    if effective < dimension:
        return Fraction(0)
    result = Fraction(1)
    for j in range(dimension):
        result *= 1-Fraction(1, q**(effective-j))
    return result


def measurement_baseline_comparison(q: int, n: int, d: int, copies: int):
    """Compare legal readouts of the same noiseless subspace/coset copies."""
    if type(n) is not int or type(d) is not int or not 0 <= d <= n or n < 1:
        raise ValueError("0<=d<=n with positive n required")
    return {
        "task": "recover_hidden_linear_subspace_not_lattice_short_vector_or_code_equivalence",
        "copies": copies,
        "homogeneous_Z_sample_recovery_exact": str(measured_span_recovery_probability(q,d,copies)),
        "shared_unknown_affine_offset_Z_recovery_exact": str(measured_span_recovery_probability(
            q,d,copies,shared_affine_offset=True)),
        "coherent_coset_Fourier_recovery_exact": str(measured_span_recovery_probability(q,n-d,copies)),
        "homogeneous_phase_only_noise_changes_Z_distribution": False,
        "fresh_uniform_offsets_hide_B_from_all_Z_transcripts": True,
        "fresh_uniform_offsets_hide_B_from_coherent_Fourier_readout": False,
        "homogeneous_baseline_applies_to_depolarizing_or_translation_noise_without_proof": False,
        "classical_postprocessing_field_operations_upper_order": "O(copies*n*min(copies,n))",
        "classical_postprocessing_field_elements_upper_order": "O(copies*n)",
        "Z_samples_free_from_an_arbitrary_classical_problem_instance": False,
        "quantum_state_source_cost_included_by_this_comparison": False,
        "recovery_probability_is_an_algorithmic_speedup": False,
        "novelty_claim": False,
    }


def evaluate_dual_intersection_case(
    *,
    case_id: str,
    q: int,
    n: int,
    generator_matrix: list[list[int]],
    m_samples: int,
) -> dict[str, Any]:
    """Exhaustively enumerate all (q^{n-d})^m dual sample tuples U_perp in (B^perp)^m and verify Theorems 1, 2, 3."""
    M = np.array(generator_matrix, dtype=int) % q
    d, n_cols = M.shape
    if n_cols != n:
        raise ValueError("generator_matrix column count must equal n")
    dual_dim = n - d

    all_vectors = [tuple(v) for v in itertools.product(range(q), repeat=n)]
    u_all_arr = np.array(all_vectors, dtype=int)  # shape (q^n, n)

    # Construct B and B^perp
    B_set: set[tuple[int, ...]] = set()
    for c in itertools.product(range(q), repeat=d):
        c_arr = np.array(c, dtype=int)
        b_vec = tuple(((c_arr @ M) % q).tolist())
        B_set.add(b_vec)
    if len(B_set) != q ** d:
        raise ValueError("generator_matrix must have full row rank d")

    B_perp_list = [
        u for u in all_vectors if np.all((M @ np.array(u, dtype=int)) % q == 0)
    ]
    if len(B_perp_list) != q ** dual_dim:
        raise ValueError("Dual subspace size mismatch")

    total_tuples = len(B_perp_list) ** m_samples
    rank_counts: dict[int, int] = {r: 0 for r in range(min(dual_dim, m_samples) + 1)}
    total_candidate_size_sum = 0
    total_spurious_size_sum = 0
    exact_recovery_count = 0
    non_planted_survival_counts: dict[tuple[int, ...], int] = {
        x: 0 for x in all_vectors if x not in B_set
    }

    theorem1_holds = True

    for u_tuple in itertools.product(B_perp_list, repeat=m_samples):
        U_mat = np.array(u_tuple, dtype=int)  # shape (m, n)
        r_perp = gf_prime_rank(U_mat, q)
        rank_counts[r_perp] += 1

        # Candidate subspace B_hat_m = {x in F_q^n : U_mat @ x == 0 mod q}
        syndrome = (u_all_arr @ U_mat.T) % q  # shape (q^n, m)
        in_b_hat = np.all(syndrome == 0, axis=1)
        cand_vecs = {all_vectors[idx] for idx in np.where(in_b_hat)[0]}

        cand_size = len(cand_vecs)
        expected_cand_size = q ** (n - r_perp)
        if not B_set.issubset(cand_vecs) or cand_size != expected_cand_size:
            theorem1_holds = False
        if (cand_vecs == B_set) != (r_perp == dual_dim):
            theorem1_holds = False

        if cand_vecs == B_set:
            exact_recovery_count += 1

        total_candidate_size_sum += cand_size
        total_spurious_size_sum += (cand_size - len(B_set))
        for x in cand_vecs - B_set:
            non_planted_survival_counts[x] += 1

    # Verify Theorem 2:
    # (a) Every x in F_q^n \ B survives with exact probability q^{-m}
    expected_single_survival_prob = Fraction(1, q ** m_samples)
    pointwise_survival_holds = all(
        Fraction(cnt, total_tuples) == expected_single_survival_prob
        for cnt in non_planted_survival_counts.values()
    )

    # (b) Expected candidate size == q^d + (q^n - q^d) * q^{-m} == sum_r q^{n-r} P_rank(r | q, n-d, m)
    emp_expected_cand_size = Fraction(total_candidate_size_sum, total_tuples)
    emp_expected_spurious = Fraction(total_spurious_size_sum, total_tuples)
    theo_expected_spurious = Fraction(q ** n - q ** d, q ** m_samples)
    theo_expected_cand_size = Fraction(q ** d, 1) + theo_expected_spurious

    rank_sum_expected_cand_size = sum(
        (
            Fraction(q ** (n - r), 1)
            * exact_projected_rank_probability(q, dual_dim, m_samples, r)
            for r in range(min(dual_dim, m_samples) + 1)
        ),
        Fraction(0, 1),
    )

    theorem2_verified = (
        pointwise_survival_holds
        and emp_expected_cand_size == theo_expected_cand_size
        and emp_expected_spurious == theo_expected_spurious
        and rank_sum_expected_cand_size == theo_expected_cand_size
    )

    # Verify Theorem 3: Exact full-recovery probability and two-sided oversampling bounds
    emp_recover_prob = Fraction(exact_recovery_count, total_tuples)
    if m_samples < dual_dim:
        theo_recover_prob = Fraction(0, 1)
        delta_m = m_samples - dual_dim
        lower_bound = Fraction(0, 1)
        upper_bound = Fraction(0, 1)
        bounds_hold = (emp_recover_prob == Fraction(0, 1))
    else:
        delta_m = m_samples - dual_dim
        theo_recover_prob = Fraction(1, 1)
        for i in range(1, dual_dim + 1):
            theo_recover_prob *= (Fraction(1, 1) - Fraction(1, q ** (delta_m + i)))
        union_sum = sum(
            (Fraction(1, q ** (delta_m + i)) for i in range(1, dual_dim + 1)),
            Fraction(0, 1),
        )
        lower_bound = Fraction(1, 1) - union_sum
        upper_bound = Fraction(1, 1) - Fraction(1, q ** (delta_m + 1))
        bounds_hold = (
            emp_recover_prob == theo_recover_prob
            and lower_bound <= emp_recover_prob <= upper_bound
        )

    theorem3_verified = bounds_hold

    return {
        "case_id": case_id,
        "q": q,
        "n": n,
        "d": d,
        "dual_dim_n_minus_d": dual_dim,
        "m_samples": m_samples,
        "oversampling_margin_delta_m": delta_m,
        "total_dual_tuples_enumerated": total_tuples,
        "single_non_planted_survival_prob_exact": _frac_str(expected_single_survival_prob),
        "expected_candidate_size_exact": _frac_str(emp_expected_cand_size),
        "expected_candidate_size_float": float(emp_expected_cand_size),
        "expected_spurious_survivors_exact": _frac_str(emp_expected_spurious),
        "expected_spurious_survivors_float": float(emp_expected_spurious),
        "recovery_probability_exact": _frac_str(emp_recover_prob),
        "recovery_probability_float": float(emp_recover_prob),
        "recovery_lower_bound_exact": _frac_str(lower_bound),
        "recovery_upper_bound_exact": _frac_str(upper_bound),
        "sample_only_classical_baseline": measurement_baseline_comparison(q,n,d,m_samples),
        "theorem1_verified": theorem1_holds,
        "theorem2_verified": theorem2_verified,
        "theorem3_verified": theorem3_verified,
        "all_theorems_verified": (
            theorem1_holds and theorem2_verified and theorem3_verified
        ),
    }


def build_planted_qary_dual_intersection_cascade_bridge(
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> dict[str, Any]:
    contract = load_contract(contract_path)

    case_specs = [
        {
            "case_id": "q3_n3_d1_dual2_m1_undersampled",
            "q": 3,
            "n": 3,
            "generator_matrix": [[1, 1, 2]],
            "m_samples": 1,
        },
        {
            "case_id": "q3_n3_d1_dual2_m2_exact_threshold",
            "q": 3,
            "n": 3,
            "generator_matrix": [[1, 1, 2]],
            "m_samples": 2,
        },
        {
            "case_id": "q3_n3_d1_dual2_m3_oversampled_plus1",
            "q": 3,
            "n": 3,
            "generator_matrix": [[1, 1, 2]],
            "m_samples": 3,
        },
        {
            "case_id": "q3_n4_d2_dual2_m2_exact_threshold",
            "q": 3,
            "n": 4,
            "generator_matrix": [[1, 0, 2, 1], [0, 1, 1, 2]],
            "m_samples": 2,
        },
        {
            "case_id": "q2_n4_d1_dual3_m4_oversampled_plus1",
            "q": 2,
            "n": 4,
            "generator_matrix": [[1, 1, 0, 1]],
            "m_samples": 4,
        },
    ]

    cases = [evaluate_dual_intersection_case(**spec) for spec in case_specs]
    all_verified = all(c["all_theorems_verified"] for c in cases)

    summary = {
        "case_count": len(cases),
        "all_cases_verified": all_verified,
        "scientific_verdict": (
            "Exhaustive enumeration over (B^perp)^m confirms three exact laws for the dual-intersection "
            "cascade B_hat_m(U_perp): (1) |B_hat_m(U_perp)| = q^{n - r_perp(U_perp)} with exact recovery "
            "B_hat_m = B iff r_perp = n - d; (2) every non-planted vector x in F_q^n \\ B survives with "
            "probability q^{-m}, yielding expected spurious count (q^n - q^d) q^{-m}; and (3) for m >= n - d "
            "(Delta_m = m - (n - d)), full recovery succeeds with probability prod_{i=1}^{n-d} (1 - q^{-(Delta_m + i)})."
        ),
    }

    payload_without_digest = {
        "schema_version": SCHEMA_VERSION,
        "contract_id": contract["contract_id"],
        "title": contract["title"],
        "status": (
            "VERIFIED_EXACT_DUAL_INTERSECTION_CASCADE_LAWS"
            if all_verified
            else "FAILED"
        ),
        "contract_path": str(contract_path.relative_to(ROOT)),
        "doc_path": str(DEFAULT_DOC_PATH.relative_to(ROOT)),
        "guardrails": contract["guardrails"],
        "theorems": contract["theorems"],
        "summary": summary,
        "cases": cases,
    }
    digest = canonical_sha256(payload_without_digest)
    return {
        **payload_without_digest,
        "certificate_sha256": digest,
    }


def write_planted_qary_dual_intersection_cascade_bridge(
    output_path: Path = DEFAULT_ARTIFACT_PATH,
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> dict[str, Any]:
    payload = build_planted_qary_dual_intersection_cascade_bridge(
        contract_path=contract_path
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build or write the planted q-ary dual-intersection cascade bridge."
    )
    parser.add_argument("--write", action="store_true", help="Write artifact JSON to disk.")
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_ARTIFACT_PATH,
        help="Output artifact path.",
    )
    args = parser.parse_args()

    if args.write:
        payload = write_planted_qary_dual_intersection_cascade_bridge(
            output_path=args.output
        )
    else:
        payload = build_planted_qary_dual_intersection_cascade_bridge()

    print(
        json.dumps(
            {
                "status": payload["status"],
                "case_count": payload["summary"]["case_count"],
                "all_cases_verified": payload["summary"]["all_cases_verified"],
                "certificate_sha256": payload["certificate_sha256"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if payload["summary"]["all_cases_verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
