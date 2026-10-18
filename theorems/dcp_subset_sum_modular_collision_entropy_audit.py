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

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


SCHEMA_VERSION = "2026-04-12.dcp-subset-sum-modular-collision-entropy-audit.v1"
DEFAULT_CONTRACT_PATH = (
    ROOT
    / "research"
    / "hypotheses"
    / "dcp_subset_sum_modular_collision_entropy_audit_contract.json"
)
DEFAULT_ARTIFACT_PATH = (
    ROOT
    / "research"
    / "phase_workbench"
    / "dcp_subset_sum_modular_collision_entropy_audit.json"
)
DEFAULT_DOC_PATH = (
    ROOT / "research" / "DCP_SUBSET_SUM_MODULAR_COLLISION_ENTROPY_AUDIT.md"
)


def canonical_sha256(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _frac_str(val: Fraction) -> str:
    return f"{val.numerator}/{val.denominator}"


def load_contract(path: Path = DEFAULT_CONTRACT_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def cosine_product_collision_prob(a_vec: tuple[int, ...], q: int) -> float:
    """Compute (1/q) * sum_{u=0}^{q-1} prod_{j=1}^m cos^2(pi * u * a_j / q)."""
    total = 0.0
    for u in range(q):
        prod = 1.0
        for a_j in a_vec:
            c = math.cos(math.pi * float(u * a_j) / float(q))
            prod *= (c * c)
        total += prod
    return total / float(q)


def evaluate_subset_sum_collision_case(
    *,
    case_id: str,
    q: int,
    m: int,
    is_composite_q: bool,
    tolerance: float = 1e-12,
) -> dict[str, Any]:
    """Exhaustively enumerate all q^m weight vectors a in Z_q^m and all 2^m Boolean inputs x in {0,1}^m."""
    bool_inputs = list(itertools.product((0, 1), repeat=m))
    bool_arr = np.array(bool_inputs, dtype=int)  # shape (2^m, m)
    num_bool = 2 ** m
    num_bool_sq = num_bool * num_bool

    all_a_vectors = list(itertools.product(range(q), repeat=m))
    total_a_vectors = len(all_a_vectors)  # q^m

    max_cosine_formula_residual = 0.0
    total_collision_prob_sum = Fraction(0, 1)
    total_off_diag_collision_sum = Fraction(0, 1)

    for a_vec in all_a_vectors:
        a_arr = np.array(a_vec, dtype=int)
        sums_mod_q = (bool_arr @ a_arr) % q
        counts = np.bincount(sums_mod_q, minlength=q)
        coll_pairs = int(np.sum(counts * counts))

        c_exact = Fraction(coll_pairs, num_bool_sq)
        c_off_exact = c_exact - Fraction(1, num_bool)
        total_collision_prob_sum += c_exact
        total_off_diag_collision_sum += c_off_exact

        c_cos_float = cosine_product_collision_prob(a_vec, q)
        res = abs(float(c_exact) - c_cos_float)
        max_cosine_formula_residual = max(max_cosine_formula_residual, res)

    # Verify Theorem 1
    theorem1_verified = bool(max_cosine_formula_residual <= tolerance)

    # Verify Theorem 2:
    # (a) Check pairwise collision probability Pr_{a ~ Z_q^m}[<a, x - x'> == 0 mod q] == 1/q for all x != x'
    a_mat = np.array(all_a_vectors, dtype=int)  # shape (q^m, m)
    all_sums = (a_mat @ bool_arr.T) % q  # shape (q^m, 2^m)
    pairwise_surjective_holds = True
    expected_pair_hits = total_a_vectors // q
    for i in range(num_bool):
        for j in range(i + 1, num_bool):
            hits = int(np.sum(all_sums[:, i] == all_sums[:, j]))
            if hits != expected_pair_hits:
                pairwise_surjective_holds = False

    # (b) Exact ensemble mean collision probability: 1/q + (1 - 1/q)*2^{-m}
    emp_mean_coll = total_collision_prob_sum / Fraction(total_a_vectors, 1)
    emp_mean_off_coll = total_off_diag_collision_sum / Fraction(total_a_vectors, 1)
    theo_mean_coll = Fraction(1, q) + Fraction(q - 1, q) * Fraction(1, num_bool)
    theo_mean_off_coll = Fraction(num_bool - 1, num_bool * q)

    theorem2_verified = bool(
        pairwise_surjective_holds
        and emp_mean_coll == theo_mean_coll
        and emp_mean_off_coll == theo_mean_off_coll
    )

    # Verify Theorem 3: single-coordinate average (1/q) sum_{a=0}^{q-1} cos^2(pi u a / q)
    max_single_coord_cos_residual = 0.0
    for u in range(q):
        avg_u = sum(
            math.cos(math.pi * float(u * a) / float(q)) ** 2 for a in range(q)
        ) / float(q)
        target_u = 1.0 if u == 0 else 0.5
        max_single_coord_cos_residual = max(
            max_single_coord_cos_residual, abs(avg_u - target_u)
        )

    theorem3_verified = bool(max_single_coord_cos_residual <= tolerance)

    return {
        "case_id": case_id,
        "q": q,
        "m": m,
        "is_composite_q": is_composite_q,
        "total_weight_vectors_q_pow_m": total_a_vectors,
        "boolean_cube_size_2_pow_m": num_bool,
        "mean_collision_probability_exact": _frac_str(emp_mean_coll),
        "mean_collision_probability_float": float(emp_mean_coll),
        "theoretical_mean_collision_exact": _frac_str(theo_mean_coll),
        "mean_off_diagonal_collision_exact": _frac_str(emp_mean_off_coll),
        "mean_off_diagonal_collision_float": float(emp_mean_off_coll),
        "pairwise_boolean_difference_surjective": pairwise_surjective_holds,
        "max_cosine_formula_residual": max_cosine_formula_residual,
        "max_single_coord_cos_residual": max_single_coord_cos_residual,
        "theorem1_verified": theorem1_verified,
        "theorem2_verified": theorem2_verified,
        "theorem3_verified": theorem3_verified,
        "all_theorems_verified": bool(
            theorem1_verified and theorem2_verified and theorem3_verified
        ),
    }


def build_dcp_subset_sum_modular_collision_entropy_audit(
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> dict[str, Any]:
    contract = load_contract(contract_path)

    case_specs = [
        {
            "case_id": "q5_prime_m3",
            "q": 5,
            "m": 3,
            "is_composite_q": False,
        },
        {
            "case_id": "q6_composite_m3",
            "q": 6,
            "m": 3,
            "is_composite_q": True,
        },
        {
            "case_id": "q8_power_of_two_m3",
            "q": 8,
            "m": 3,
            "is_composite_q": True,
        },
        {
            "case_id": "q9_odd_prime_power_m3",
            "q": 9,
            "m": 3,
            "is_composite_q": True,
        },
        {
            "case_id": "q4_composite_m4",
            "q": 4,
            "m": 4,
            "is_composite_q": True,
        },
    ]

    cases = [evaluate_subset_sum_collision_case(**spec) for spec in case_specs]
    all_verified = bool(all(c["all_theorems_verified"] for c in cases))

    summary = {
        "case_count": len(cases),
        "all_cases_verified": all_verified,
        "max_cosine_formula_residual": max(
            c["max_cosine_formula_residual"] for c in cases
        ),
        "max_single_coord_cos_residual": max(
            c["max_single_coord_cos_residual"] for c in cases
        ),
        "scientific_verdict": (
            "Across prime, power-of-two, odd prime-power, and composite moduli q in {4, 5, 6, 8, 9}, "
            "the modular subset-sum collision probability C(a) equals (1/q) sum_{u=0}^{q-1} prod_{j=1}^m "
            "cos^2(pi u a_j / q). Because every non-zero Boolean difference x - x' in {-1, 0, +1}^m \\ {0} "
            "contains at least one unit coordinate +-1 mod q, Pr_a[f_a(x) == f_a(x') mod q] = 1/q "
            "holds universally even for composite q, yielding E_a[C(a)] = 1/q + (1 - 1/q) 2^{-m}."
        ),
    }

    payload_without_digest = {
        "schema_version": SCHEMA_VERSION,
        "contract_id": contract["contract_id"],
        "title": contract["title"],
        "status": (
            "VERIFIED_EXACT_SUBSET_SUM_COLLISION_AND_BOOLEAN_SURJECTIVITY_LAWS"
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


def write_dcp_subset_sum_modular_collision_entropy_audit(
    output_path: Path = DEFAULT_ARTIFACT_PATH,
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> dict[str, Any]:
    payload = build_dcp_subset_sum_modular_collision_entropy_audit(
        contract_path=contract_path
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build or write the DCP subset-sum modular collision-entropy audit."
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
        payload = write_dcp_subset_sum_modular_collision_entropy_audit(
            output_path=args.output
        )
    else:
        payload = build_dcp_subset_sum_modular_collision_entropy_audit()

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
