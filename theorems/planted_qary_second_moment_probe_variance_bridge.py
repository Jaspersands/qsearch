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


SCHEMA_VERSION = "2026-04-12.planted-qary-second-moment-probe-variance-bridge.v1"
DEFAULT_CONTRACT_PATH = (
    ROOT
    / "research"
    / "hypotheses"
    / "planted_qary_second_moment_probe_variance_bridge_contract.json"
)
DEFAULT_ARTIFACT_PATH = (
    ROOT
    / "research"
    / "reductions"
    / "planted_qary_second_moment_probe_variance_bridge.json"
)
DEFAULT_DOC_PATH = (
    ROOT / "research" / "PLANTED_QARY_SECOND_MOMENT_PROBE_VARIANCE_BRIDGE.md"
)


def canonical_sha256(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _frac_str(val: Fraction) -> str:
    return f"{val.numerator}/{val.denominator}"


def load_contract(path: Path = DEFAULT_CONTRACT_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_projective_rep(vec: tuple[int, ...], q: int) -> tuple[int, ...]:
    """Return canonical representative of the projective ray F_q^x * vec (first non-zero entry normalized to 1)."""
    for c in vec:
        if c % q != 0:
            inv_c = pow(c % q, -1, q)
            return tuple((x * inv_c) % q for x in vec)
    raise ValueError("Zero vector has no projective representative")


def evaluate_probe_variance_case(
    *,
    case_id: str,
    q: int,
    n: int,
    generator_matrix: list[list[int]],
    window: list[int],
) -> dict[str, Any]:
    """Exhaustively verify Theorems 1, 2, and 3 across all u in F_q^n."""
    M = np.array(generator_matrix, dtype=int) % q
    d, n_cols = M.shape
    if n_cols != n:
        raise ValueError("generator_matrix column count must equal n")
    R = len(window)
    window_set = set(window)
    zero_in_window = 0 in window_set

    all_vectors = [tuple(v) for v in itertools.product(range(q), repeat=n)]
    N_total = q ** n
    zero_vec = tuple([0] * n)

    # 1. Construct planted subspace B = rowspan(M)
    B_set: set[tuple[int, ...]] = set()
    for c in itertools.product(range(q), repeat=d):
        c_arr = np.array(c, dtype=int)
        b_vec = tuple(((c_arr @ M) % q).tolist())
        B_set.add(b_vec)
    if len(B_set) != q ** d:
        raise ValueError("generator_matrix must have full row rank d")

    B_nonzero = sorted(B_set - {zero_vec})
    B_perp_set = {
        u for u in all_vectors if np.all((M @ np.array(u, dtype=int)) % q == 0)
    }

    # Partition B \ {0} into L_d = (q^d - 1)/(q - 1) projective rays
    rays_dict: dict[tuple[int, ...], list[tuple[int, ...]]] = {}
    for b in B_nonzero:
        rep = canonical_projective_rep(b, q)
        rays_dict.setdefault(rep, []).append(b)
    num_rays = len(rays_dict)
    expected_num_rays = (q ** d - 1) // (q - 1)
    if num_rays != expected_num_rays:
        raise ValueError("Projective ray count mismatch")

    # Construct a ray-free subset S in F_q^n \ {0} of size M_nonzero = q^d - 1
    # (Possible whenever q^d - 1 <= (q^n - 1)/(q - 1))
    all_projective_reps: list[tuple[int, ...]] = []
    seen_reps: set[tuple[int, ...]] = set()
    for v in all_vectors:
        if v == zero_vec:
            continue
        rep = canonical_projective_rep(v, q)
        if rep not in seen_reps:
            seen_reps.add(rep)
            all_projective_reps.append(v)

    ray_free_subset = all_projective_reps[: (q ** d - 1)]
    if len(ray_free_subset) != q ** d - 1:
        raise ValueError("Not enough projective rays in F_q^n to form ray-free subset of size q^d - 1")

    # 2. Evaluate N_W(u; B), ray counts Y_i(u), and N_W(u; S_ray_free) across all u in F_q^n
    u_arr = np.array(all_vectors, dtype=int)  # shape (q^n, n)
    B_arr = np.array(sorted(B_set), dtype=int)  # shape (q^d, n)
    evals_B = (u_arr @ B_arr.T) % q  # shape (q^n, q^d)
    in_win_B = np.isin(evals_B, list(window_set)).astype(int)
    counts_B = np.sum(in_win_B, axis=1)  # shape (q^n,)

    # Separate on-dual vs off-dual counts
    off_dual_counts = [
        int(counts_B[idx])
        for idx, u in enumerate(all_vectors)
        if u not in B_perp_set
    ]
    on_dual_counts = [
        int(counts_B[idx])
        for idx, u in enumerate(all_vectors)
        if u in B_perp_set
    ]

    emp_mean_B = Fraction(int(np.sum(counts_B)), N_total)
    emp_second_B = Fraction(int(np.sum(counts_B ** 2)), N_total)
    emp_var_B = emp_second_B - (emp_mean_B ** 2)

    theo_mean_B = (
        (Fraction(1, 1) if zero_in_window else Fraction(0, 1))
        + Fraction(q ** d - 1, 1) * Fraction(R, q)
    )
    ind_zero = Fraction(1, 1) if zero_in_window else Fraction(0, 1)
    theo_var_B = Fraction(q ** d - 1, 1) * ((ind_zero - Fraction(R, q)) ** 2)

    off_dual_var_zero = (len(set(off_dual_counts)) == 1 and off_dual_counts[0] == (q ** (d - 1)) * R)
    theorem1_verified = (
        emp_mean_B == theo_mean_B
        and emp_var_B == theo_var_B
        and off_dual_var_zero
    )

    # 3. Verify Theorem 2: Ray variance decomposition and zero off-ray covariance
    ray_lists = list(rays_dict.values())
    ray_counts_matrix = np.zeros((N_total, num_rays), dtype=int)
    for r_idx, r_vecs in enumerate(ray_lists):
        r_arr = np.array(r_vecs, dtype=int)
        r_evals = (u_arr @ r_arr.T) % q
        ray_counts_matrix[:, r_idx] = np.sum(np.isin(r_evals, list(window_set)), axis=1)

    ray_vars: list[Fraction] = []
    for r_idx in range(num_rays):
        col = ray_counts_matrix[:, r_idx]
        m1 = Fraction(int(np.sum(col)), N_total)
        m2 = Fraction(int(np.sum(col ** 2)), N_total)
        ray_vars.append(m2 - m1 ** 2)

    sum_ray_vars = sum(ray_vars, Fraction(0, 1))
    # Check all off-diagonal ray covariances Cov(Y_i, Y_j) for i != j
    max_off_ray_cov = Fraction(0, 1)
    for i in range(num_rays):
        for j in range(i + 1, num_rays):
            ci = ray_counts_matrix[:, i]
            cj = ray_counts_matrix[:, j]
            mi = Fraction(int(np.sum(ci)), N_total)
            mj = Fraction(int(np.sum(cj)), N_total)
            mij = Fraction(int(np.sum(ci * cj)), N_total)
            cov_ij = abs(mij - mi * mj)
            if cov_ij > max_off_ray_cov:
                max_off_ray_cov = cov_ij

    theorem2_verified = (
        sum_ray_vars == emp_var_B and max_off_ray_cov == Fraction(0, 1)
    )

    # 4. Verify Theorem 3: Ray-free subset variance and exact ratio R / (q - R) on zero-free windows
    S_arr = np.array(ray_free_subset, dtype=int)
    evals_S = (u_arr @ S_arr.T) % q
    counts_S = np.sum(np.isin(evals_S, list(window_set)), axis=1)
    emp_mean_S = Fraction(int(np.sum(counts_S)), N_total)
    emp_second_S = Fraction(int(np.sum(counts_S ** 2)), N_total)
    emp_var_S = emp_second_S - (emp_mean_S ** 2)

    theo_var_S = (
        Fraction(q ** d - 1, 1)
        * Fraction(R, q)
        * (Fraction(1, 1) - Fraction(R, q))
    )
    var_ratio_B_over_S = emp_var_B / emp_var_S
    expected_zero_free_ratio = Fraction(R, q - R)

    if not zero_in_window:
        theorem3_verified = (
            emp_var_S == theo_var_S
            and var_ratio_B_over_S == expected_zero_free_ratio
            and off_dual_var_zero
        )
    else:
        theorem3_verified = (emp_var_S == theo_var_S and off_dual_var_zero)

    return {
        "case_id": case_id,
        "q": q,
        "n": n,
        "d": d,
        "R": R,
        "window": list(window),
        "zero_in_window": zero_in_window,
        "projective_ray_count_L_d": num_rays,
        "subspace_mean_exact": _frac_str(emp_mean_B),
        "subspace_variance_exact": _frac_str(emp_var_B),
        "subspace_variance_float": float(emp_var_B),
        "theoretical_subspace_variance_exact": _frac_str(theo_var_B),
        "single_ray_variance_exact": _frac_str(ray_vars[0]),
        "sum_of_ray_variances_exact": _frac_str(sum_ray_vars),
        "max_off_ray_covariance_exact": _frac_str(max_off_ray_cov),
        "ray_free_subset_mean_exact": _frac_str(emp_mean_S),
        "ray_free_subset_variance_exact": _frac_str(emp_var_S),
        "ray_free_subset_variance_float": float(emp_var_S),
        "variance_ratio_subspace_over_ray_free_exact": _frac_str(var_ratio_B_over_S),
        "variance_ratio_subspace_over_ray_free_float": float(var_ratio_B_over_S),
        "off_dual_constant_count": off_dual_counts[0],
        "on_dual_constant_count": on_dual_counts[0],
        "off_dual_variance_is_zero": off_dual_var_zero,
        "theorem1_verified": theorem1_verified,
        "theorem2_verified": theorem2_verified,
        "theorem3_verified": theorem3_verified,
        "all_theorems_verified": (
            theorem1_verified and theorem2_verified and theorem3_verified
        ),
    }


def build_planted_qary_second_moment_probe_variance_bridge(
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> dict[str, Any]:
    contract = load_contract(contract_path)

    case_specs = [
        {
            "case_id": "q3_n3_d2_zerofree_R1",
            "q": 3,
            "n": 3,
            "generator_matrix": [[1, 0, 1], [0, 1, 1]],
            "window": [1],
        },
        {
            "case_id": "q3_n3_d2_zerofree_R2",
            "q": 3,
            "n": 3,
            "generator_matrix": [[1, 0, 1], [0, 1, 1]],
            "window": [1, 2],
        },
        {
            "case_id": "q3_n3_d2_with_zero_R2",
            "q": 3,
            "n": 3,
            "generator_matrix": [[1, 0, 1], [0, 1, 1]],
            "window": [0, 1],
        },
        {
            "case_id": "q3_n4_d2_zerofree_R2",
            "q": 3,
            "n": 4,
            "generator_matrix": [[1, 0, 2, 1], [0, 1, 1, 2]],
            "window": [1, 2],
        },
        {
            "case_id": "q5_n3_d2_zerofree_R2",
            "q": 5,
            "n": 3,
            "generator_matrix": [[1, 0, 2], [0, 1, 3]],
            "window": [1, 4],
        },
    ]

    cases = [evaluate_probe_variance_case(**spec) for spec in case_specs]
    all_verified = all(c["all_theorems_verified"] for c in cases)

    summary = {
        "case_count": len(cases),
        "all_cases_verified": all_verified,
        "scientific_verdict": (
            "Exhaustive evaluation over F_q^n confirms that for any dimension-d planted subspace B, "
            "N_W(u; B) has exact variance (q^d - 1)(1_{0 in W} - R/q)^2, which decomposes into the sum "
            "of L_d = (q^d - 1)/(q - 1) uncorrelated projective-ray variances with zero off-ray covariance. "
            "For any zero-free window W of size R, the variance ratio between B and a ray-free subset S "
            "of size q^d - 1 is exactly R / (q - R), while 100% of the variance of B is localized on the "
            "q^{-d}-rare dual subspace u in B^perp."
        ),
    }

    payload_without_digest = {
        "schema_version": SCHEMA_VERSION,
        "contract_id": contract["contract_id"],
        "title": contract["title"],
        "status": (
            "VERIFIED_EXACT_SECOND_MOMENT_PROBE_VARIANCE_LAWS"
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


def write_planted_qary_second_moment_probe_variance_bridge(
    output_path: Path = DEFAULT_ARTIFACT_PATH,
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> dict[str, Any]:
    payload = build_planted_qary_second_moment_probe_variance_bridge(
        contract_path=contract_path
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build or write the planted q-ary second-moment probe-variance bridge."
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
        payload = write_planted_qary_second_moment_probe_variance_bridge(
            output_path=args.output
        )
    else:
        payload = build_planted_qary_second_moment_probe_variance_bridge()

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
