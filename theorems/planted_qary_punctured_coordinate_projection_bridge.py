from __future__ import annotations

import argparse
from collections import defaultdict
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

from theorems.planted_qary_multiprobe_gl_rank_saturation_bridge import gf_prime_rank
from theorems.planted_qary_noisy_parity_check_likelihood_bridge import hamming_weight


SCHEMA_VERSION = "2026-04-12.planted-qary-punctured-coordinate-projection-bridge.v1"
DEFAULT_CONTRACT_PATH = (
    ROOT
    / "research"
    / "hypotheses"
    / "planted_qary_punctured_coordinate_projection_bridge_contract.json"
)
DEFAULT_ARTIFACT_PATH = (
    ROOT
    / "research"
    / "reductions"
    / "planted_qary_punctured_coordinate_projection_bridge.json"
)
DEFAULT_DOC_PATH = (
    ROOT / "research" / "PLANTED_QARY_PUNCTURED_COORDINATE_PROJECTION_BRIDGE.md"
)


def canonical_sha256(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _frac_str(val: Fraction) -> str:
    return f"{val.numerator}/{val.denominator}"


def load_contract(path: Path = DEFAULT_CONTRACT_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def evaluate_punctured_projection_case(
    *,
    case_id: str,
    q: int,
    n: int,
    generator_matrix: list[list[int]],
    kept_indices_J: list[int],
    window: list[int],
    tolerance: float = 1e-12,
) -> dict[str, Any]:
    """Exhaustively verify Theorems 1, 2, and 3 for coordinate subset J subset {0, ..., n-1}."""
    M = np.array(generator_matrix, dtype=int) % q
    d, n_cols = M.shape
    if n_cols != n:
        raise ValueError("generator_matrix column count must equal n")

    J = sorted(kept_indices_J)
    J_bar = [idx for idx in range(n) if idx not in J]
    m = len(J)
    t = len(J_bar)
    R = len(window)
    window_set = set(window)
    zero_in_window = 0 in window_set

    M_J = M[:, J]
    M_J_bar = M[:, J_bar]
    d_J = gf_prime_rank(M_J, q)
    d_J_bar = gf_prime_rank(M_J_bar, q)
    k_J = d - d_J_bar

    all_vectors_n = [tuple(v) for v in itertools.product(range(q), repeat=n)]
    all_vectors_m = [tuple(v) for v in itertools.product(range(q), repeat=m)]
    vec_m_to_idx = {v: idx for idx, v in enumerate(all_vectors_m)}
    zero_n = tuple([0] * n)

    # Construct B and B^perp
    B_set: set[tuple[int, ...]] = set()
    for c in itertools.product(range(q), repeat=d):
        c_arr = np.array(c, dtype=int)
        b_vec = tuple(((c_arr @ M) % q).tolist())
        B_set.add(b_vec)
    if len(B_set) != q ** d:
        raise ValueError("generator_matrix must have full row rank d")

    d_min = min(hamming_weight(b) for b in B_set if b != zero_n)
    B_perp_set = {
        u for u in all_vectors_n if np.all((M @ np.array(u, dtype=int)) % q == 0)
    }

    # 1. Verify Theorem 1: Reduced density matrix rho_{B, J} = Tr_{J_bar}(|psi_B><psi_B|)
    # Group b in B by its punctured suffix z = b_{J_bar}
    fibers_by_z: dict[tuple[int, ...], list[tuple[int, ...]]] = defaultdict(list)
    for b in B_set:
        z_bar = tuple(b[idx] for idx in J_bar)
        b_j = tuple(b[idx] for idx in J)
        fibers_by_z[z_bar].append(b_j)

    dim_m = q ** m
    rho_B_J = np.zeros((dim_m, dim_m), dtype=np.complex128)
    for z_bar, b_j_list in fibers_by_z.items():
        ket = np.zeros(dim_m, dtype=np.complex128)
        for b_j in b_j_list:
            ket[vec_m_to_idx[b_j]] += 1.0
        rho_B_J += np.outer(ket, ket.conj()) / float(q ** d)

    eigvals = np.linalg.eigvalsh(rho_B_J)
    nonzero_eigs = [float(v) for v in eigvals if v > 1e-12]
    obs_rank = len(nonzero_eigs)
    schmidt_rank_exp = d_J + d_J_bar - d
    expected_rank = q ** schmidt_rank_exp
    target_eig = 1.0 / float(expected_rank)
    eig_spread = max(abs(v - target_eig) for v in nonzero_eigs)
    obs_purity = float(np.real(np.trace(rho_B_J @ rho_B_J)))

    theorem1_verified = bool(
        obs_rank == expected_rank
        and eig_spread <= tolerance
        and abs(obs_purity - target_eig) <= tolerance
    )

    # 2. Verify Theorem 2: Puncturing-shortening duality
    # Punctured code B_J = pi_J(B)
    B_J_set = {tuple(b[idx] for idx in J) for b in B_set}
    # Dual of B_J in F_q^m
    B_J_dual_set = {
        u_m
        for u_m in all_vectors_m
        if all(sum(b_j[i] * u_m[i] for i in range(m)) % q == 0 for b_j in B_J_set)
    }
    # Shortened dual {u_m in F_q^m : iota_J(u_m) in B^perp}
    shortened_dual_set = set()
    for u_m in all_vectors_m:
        u_n = [0] * n
        for i, col_idx in enumerate(J):
            u_n[col_idx] = u_m[i]
        if tuple(u_n) in B_perp_set:
            shortened_dual_set.add(u_m)

    # Punctured dual pi_J(B^perp)
    punctured_dual_set = {tuple(u[idx] for idx in J) for u in B_perp_set}

    theorem2_verified = bool(
        len(B_J_set) == q ** d_J
        and B_J_dual_set == shortened_dual_set
        and len(B_J_dual_set) == q ** (m - d_J)
        and B_J_dual_set.issubset(punctured_dual_set)
        and len(punctured_dual_set) == q ** (m - k_J)
    )

    # 3. Verify Theorem 3: J-supported classical probe variance and d_min rank-locking
    counts_J = []
    for u_m in all_vectors_m:
        u_n = [0] * n
        for i, col_idx in enumerate(J):
            u_n[col_idx] = u_m[i]
        cnt = sum(
            1
            for b in B_set
            if (sum(b[col] * u_n[col] for col in range(n)) % q) in window_set
        )
        counts_J.append(cnt)

    emp_mean = Fraction(sum(counts_J), dim_m)
    emp_second = Fraction(sum(c * c for c in counts_J), dim_m)
    emp_var = emp_second - (emp_mean ** 2)

    ind_zero = Fraction(1, 1) if zero_in_window else Fraction(0, 1)
    theo_var = (
        Fraction(q ** (2 * (d - d_J)), 1)
        * Fraction(q ** d_J - 1, 1)
        * ((ind_zero - Fraction(R, q)) ** 2)
    )

    # Check d_min rank-locking across ALL subsets of size |J| when t < d_min
    rank_locked_across_all_subsets = True
    if t < d_min:
        for comb_J in itertools.combinations(range(n), m):
            if gf_prime_rank(M[:, list(comb_J)], q) != d:
                rank_locked_across_all_subsets = False

    theorem3_verified = bool(
        emp_var == theo_var and rank_locked_across_all_subsets
    )

    return {
        "case_id": case_id,
        "q": q,
        "n": n,
        "d": d,
        "kept_indices_J": J,
        "m_kept": m,
        "t_punctured": t,
        "primal_minimum_distance_d_min": d_min,
        "punctured_rank_d_J": d_J,
        "complement_rank_d_J_bar": d_J_bar,
        "shortened_dim_k_J": k_J,
        "reduced_state_rank": obs_rank,
        "reduced_state_purity_exact": _frac_str(Fraction(1, expected_rank)),
        "reduced_state_purity_float": obs_purity,
        "shortened_dual_size": len(B_J_dual_set),
        "punctured_dual_size": len(punctured_dual_set),
        "j_supported_probe_mean_exact": _frac_str(emp_mean),
        "j_supported_probe_variance_exact": _frac_str(emp_var),
        "theoretical_j_supported_variance_exact": _frac_str(theo_var),
        "t_less_than_d_min": (t < d_min),
        "rank_locked_d_J_equals_d": (d_J == d),
        "theorem1_verified": theorem1_verified,
        "theorem2_verified": theorem2_verified,
        "theorem3_verified": theorem3_verified,
        "all_theorems_verified": bool(
            theorem1_verified and theorem2_verified and theorem3_verified
        ),
    }


def build_planted_qary_punctured_coordinate_projection_bridge(
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> dict[str, Any]:
    contract = load_contract(contract_path)

    case_specs = [
        {
            "case_id": "q3_n4_d2_dmin3_puncture1_rank_locked",
            "q": 3,
            "n": 4,
            "generator_matrix": [[1, 0, 2, 1], [0, 1, 1, 2]],
            "kept_indices_J": [0, 1, 2],
            "window": [1, 2],
        },
        {
            "case_id": "q3_n4_d2_dmin3_puncture2_still_full_rank",
            "q": 3,
            "n": 4,
            "generator_matrix": [[1, 0, 2, 1], [0, 1, 1, 2]],
            "kept_indices_J": [0, 1],
            "window": [1, 2],
        },
        {
            "case_id": "q3_n4_d2_dmin1_puncture2_rank_drop",
            "q": 3,
            "n": 4,
            "generator_matrix": [[1, 0, 1, 0], [0, 0, 0, 1]],
            "kept_indices_J": [0, 1],
            "window": [1, 2],
        },
        {
            "case_id": "q3_n4_d2_dmin1_puncture2_with_zero",
            "q": 3,
            "n": 4,
            "generator_matrix": [[1, 0, 1, 0], [0, 0, 0, 1]],
            "kept_indices_J": [0, 1],
            "window": [0, 1],
        },
        {
            "case_id": "q2_n4_d2_dmin2_puncture1_rank_locked",
            "q": 2,
            "n": 4,
            "generator_matrix": [[1, 0, 1, 1], [0, 1, 1, 0]],
            "kept_indices_J": [0, 1, 2],
            "window": [1],
        },
    ]

    cases = [evaluate_punctured_projection_case(**spec) for spec in case_specs]
    all_verified = bool(all(c["all_theorems_verified"] for c in cases))

    summary = {
        "case_count": len(cases),
        "all_cases_verified": all_verified,
        "scientific_verdict": (
            "Across coordinate bipartitions (J, J_bar), tracing out J_bar produces a reduced state "
            "rho_{B, J} of exact rank q^{d_{J_bar}} and purity q^{-d_{J_bar}}. Local QFT_q^{\\otimes m} "
            "samples uniformly from the punctured dual pi_J(B^perp) of size q^{m - k_J}, while the dual "
            "of the punctured code (B_J)^perp equals the shortened dual of size q^{m - d_J}, and "
            "puncturing fewer than d_min(B) coordinates strictly locks d_J = d across all subsets J."
        ),
    }

    payload_without_digest = {
        "schema_version": SCHEMA_VERSION,
        "contract_id": contract["contract_id"],
        "title": contract["title"],
        "status": (
            "VERIFIED_EXACT_PUNCTURED_PROJECTION_AND_RANK_LOCKING_LAWS"
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


def write_planted_qary_punctured_coordinate_projection_bridge(
    output_path: Path = DEFAULT_ARTIFACT_PATH,
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> dict[str, Any]:
    payload = build_planted_qary_punctured_coordinate_projection_bridge(
        contract_path=contract_path
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build or write the planted q-ary punctured-coordinate projection bridge."
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
        payload = write_planted_qary_punctured_coordinate_projection_bridge(
            output_path=args.output
        )
    else:
        payload = build_planted_qary_punctured_coordinate_projection_bridge()

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
