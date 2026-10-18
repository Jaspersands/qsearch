from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path
import sys
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.planted_qary_noisy_parity_check_likelihood_bridge import hamming_weight


SCHEMA_VERSION = "2026-04-12.planted-qary-noisy-dual-intersection-false-negative-bridge.v1"
DEFAULT_CONTRACT_PATH = (
    ROOT
    / "research"
    / "hypotheses"
    / "planted_qary_noisy_dual_intersection_false_negative_bridge_contract.json"
)
DEFAULT_ARTIFACT_PATH = (
    ROOT
    / "research"
    / "reductions"
    / "planted_qary_noisy_dual_intersection_false_negative_bridge.json"
)
DEFAULT_DOC_PATH = (
    ROOT / "research" / "PLANTED_QARY_NOISY_DUAL_INTERSECTION_FALSE_NEGATIVE_BRIDGE.md"
)


def canonical_sha256(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _frac_str(val: Fraction) -> str:
    return f"{val.numerator}/{val.denominator}"


def load_contract(path: Path = DEFAULT_CONTRACT_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def evaluate_noisy_dual_intersection_case(
    *,
    case_id: str,
    q: int,
    n: int,
    generator_matrix: list[list[int]],
    gamma_num: int,
    gamma_den: int,
    m_samples: int,
) -> dict[str, Any]:
    """Exhaustively compute the exact noisy dual QFT distribution P_QFT(u | B, gamma) and verify Theorems 1, 2, 3."""
    M = np.array(generator_matrix, dtype=int) % q
    d, n_cols = M.shape
    if n_cols != n:
        raise ValueError("generator_matrix column count must equal n")
    gamma_frac = Fraction(gamma_num, gamma_den)
    one_minus_gamma = Fraction(1, 1) - gamma_frac

    all_vectors = [tuple(v) for v in itertools.product(range(q), repeat=n)]
    zero_vec = tuple([0] * n)

    # Construct B and B^perp
    B_set: set[tuple[int, ...]] = set()
    for c in itertools.product(range(q), repeat=d):
        c_arr = np.array(c, dtype=int)
        b_vec = tuple(((c_arr @ M) % q).tolist())
        B_set.add(b_vec)
    if len(B_set) != q ** d:
        raise ValueError("generator_matrix must have full row rank d")

    B_nonzero = sorted(B_set - {zero_vec})
    d_min = min(hamming_weight(b) for b in B_nonzero)

    B_perp_set = {
        u for u in all_vectors if np.all((M @ np.array(u, dtype=int)) % q == 0)
    }
    dual_size_frac = Fraction(len(B_perp_set), 1)

    # Single-coordinate depolarizing probabilities for dual error xi_j:
    p0_frac = Fraction(1, 1) - Fraction(q - 1, q) * gamma_frac
    p1_frac = gamma_frac / Fraction(q, 1)

    # Exact rational probability P_QFT(u | B, gamma) for every u in F_q^n:
    # P_QFT(u | B, gamma) = (1 / |B^perp|) sum_{v in B^perp} p0^{n - wt_H(u - v)} p1^{wt_H(u - v)}
    u_probs_frac: dict[tuple[int, ...], Fraction] = {}
    for u in all_vectors:
        prob_sum = Fraction(0, 1)
        for v in B_perp_set:
            diff_wt = sum(1 for j in range(n) if (u[j] - v[j]) % q != 0)
            prob_sum += (p0_frac ** (n - diff_wt)) * (p1_frac ** diff_wt)
        u_probs_frac[u] = prob_sum / dual_size_frac

    if sum(u_probs_frac.values(), Fraction(0, 1)) != Fraction(1, 1):
        raise ValueError("Noisy QFT distribution does not sum to 1")

    # Evaluate single-sample and m-sample zero-syndrome survival probabilities for every x in F_q^n
    planted_weight_strata: dict[int, dict[str, Any]] = {}
    theorem1_holds = True
    theorem2_holds = True
    max_ssr_observed = Fraction(0, 1)
    expected_spurious_single = Fraction(1, q)
    expected_spurious_m = Fraction(1, q ** m_samples)

    total_expected_planted_survivors = Fraction(0, 1)
    total_expected_spurious_survivors = Fraction(0, 1)

    for x in all_vectors:
        # Exact single-sample survival probability Pr_{u ~ P_QFT}[<x, u> == 0 mod q]
        single_surv = sum(
            (
                pu
                for u, pu in u_probs_frac.items()
                if sum(x[j] * u[j] for j in range(n)) % q == 0
            ),
            Fraction(0, 1),
        )
        m_surv = single_surv ** m_samples

        if x in B_set:
            total_expected_planted_survivors += m_surv
            wt_x = hamming_weight(x)
            theo_single = Fraction(1, q) + Fraction(q - 1, q) * (
                one_minus_gamma ** wt_x
            )
            theo_m = theo_single ** m_samples
            if single_surv != theo_single or m_surv != theo_m:
                theorem1_holds = False
            if x != zero_vec:
                ssr_x = m_surv / expected_spurious_m
                if ssr_x > max_ssr_observed:
                    max_ssr_observed = ssr_x
                planted_weight_strata[wt_x] = {
                    "hamming_weight": wt_x,
                    "single_sample_survival_exact": _frac_str(single_surv),
                    "m_sample_survival_exact": _frac_str(m_surv),
                    "m_sample_survival_float": float(m_surv),
                    "false_negative_prob_exact": _frac_str(Fraction(1, 1) - m_surv),
                    "false_negative_prob_float": float(Fraction(1, 1) - m_surv),
                    "survival_to_spurious_ratio_exact": _frac_str(ssr_x),
                    "survival_to_spurious_ratio_float": float(ssr_x),
                }
        else:
            total_expected_spurious_survivors += m_surv
            if single_surv != expected_spurious_single or m_surv != expected_spurious_m:
                theorem2_holds = False

    theo_total_spurious = Fraction(q ** n - q ** d, q ** m_samples)
    if total_expected_spurious_survivors != theo_total_spurious:
        theorem2_holds = False

    expected_max_ssr = (
        Fraction(1, 1) + Fraction(q - 1, 1) * (one_minus_gamma ** d_min)
    ) ** m_samples
    theorem3_holds = (max_ssr_observed == expected_max_ssr)

    return {
        "case_id": case_id,
        "q": q,
        "n": n,
        "d": d,
        "m_samples": m_samples,
        "gamma_exact": _frac_str(gamma_frac),
        "gamma_float": float(gamma_frac),
        "one_minus_gamma_exact": _frac_str(one_minus_gamma),
        "primal_minimum_distance_d_min": d_min,
        "spurious_single_sample_survival_exact": _frac_str(expected_spurious_single),
        "spurious_m_sample_survival_exact": _frac_str(expected_spurious_m),
        "expected_spurious_survivors_exact": _frac_str(total_expected_spurious_survivors),
        "expected_spurious_survivors_float": float(total_expected_spurious_survivors),
        "expected_planted_survivors_exact": _frac_str(total_expected_planted_survivors),
        "expected_planted_survivors_float": float(total_expected_planted_survivors),
        "max_nonzero_ssr_exact": _frac_str(max_ssr_observed),
        "max_nonzero_ssr_float": float(max_ssr_observed),
        "expected_max_ssr_exact": _frac_str(expected_max_ssr),
        "planted_weight_strata": [
            planted_weight_strata[w] for w in sorted(planted_weight_strata.keys())
        ],
        "theorem1_verified": bool(theorem1_holds),
        "theorem2_verified": bool(theorem2_holds),
        "theorem3_verified": bool(theorem3_holds),
        "all_theorems_verified": bool(
            theorem1_holds and theorem2_holds and theorem3_holds
        ),
    }


def build_planted_qary_noisy_dual_intersection_false_negative_bridge(
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> dict[str, Any]:
    contract = load_contract(contract_path)

    case_specs = [
        {
            "case_id": "q3_n3_d2_gamma_1_over_4_m2",
            "q": 3,
            "n": 3,
            "generator_matrix": [[1, 0, 1], [0, 1, 1]],
            "gamma_num": 1,
            "gamma_den": 4,
            "m_samples": 2,
        },
        {
            "case_id": "q3_n3_d2_gamma_1_over_2_m3",
            "q": 3,
            "n": 3,
            "generator_matrix": [[1, 0, 1], [0, 1, 1]],
            "gamma_num": 1,
            "gamma_den": 2,
            "m_samples": 3,
        },
        {
            "case_id": "q3_n4_d2_dmin2_gamma_1_over_3_m2",
            "q": 3,
            "n": 4,
            "generator_matrix": [[1, 0, 1, 0], [0, 1, 1, 1]],
            "gamma_num": 1,
            "gamma_den": 3,
            "m_samples": 2,
        },
        {
            "case_id": "q3_n4_d2_dmin3_gamma_1_over_3_m2",
            "q": 3,
            "n": 4,
            "generator_matrix": [[1, 0, 2, 1], [0, 1, 1, 2]],
            "gamma_num": 1,
            "gamma_den": 3,
            "m_samples": 2,
        },
        {
            "case_id": "q5_n3_d1_dmin3_gamma_1_over_5_m2",
            "q": 5,
            "n": 3,
            "generator_matrix": [[1, 2, 3]],
            "gamma_num": 1,
            "gamma_den": 5,
            "m_samples": 2,
        },
    ]

    cases = [evaluate_noisy_dual_intersection_case(**spec) for spec in case_specs]
    all_verified = bool(all(c["all_theorems_verified"] for c in cases))

    summary = {
        "case_count": len(cases),
        "all_cases_verified": all_verified,
        "scientific_verdict": (
            "Exhaustive rational evaluation over F_q^n confirms that under m noisy QFT_q^{\\otimes n} "
            "dual samples at coordinate noise rate gamma, every non-planted vector x in F_q^n \\ B "
            "survives the zero-syndrome intersection cascade with noise-invariant probability q^{-m}, "
            "whereas every planted codeword b in B of Hamming weight wt_H(b) survives with probability "
            "(1/q + ((q-1)/q)(1 - gamma)^{wt_H(b)})^m, with maximum non-zero survival-to-spurious ratio "
            "(1 + (q-1)(1 - gamma)^{d_min(B)})^m governed by the primal minimum distance d_min(B)."
        ),
    }

    payload_without_digest = {
        "schema_version": SCHEMA_VERSION,
        "contract_id": contract["contract_id"],
        "title": contract["title"],
        "status": (
            "VERIFIED_EXACT_NOISY_DUAL_INTERSECTION_FALSE_NEGATIVE_LAWS"
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


def write_planted_qary_noisy_dual_intersection_false_negative_bridge(
    output_path: Path = DEFAULT_ARTIFACT_PATH,
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> dict[str, Any]:
    payload = build_planted_qary_noisy_dual_intersection_false_negative_bridge(
        contract_path=contract_path
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build or write the planted q-ary noisy dual-intersection false-negative bridge."
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
        payload = write_planted_qary_noisy_dual_intersection_false_negative_bridge(
            output_path=args.output
        )
    else:
        payload = build_planted_qary_noisy_dual_intersection_false_negative_bridge()

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
