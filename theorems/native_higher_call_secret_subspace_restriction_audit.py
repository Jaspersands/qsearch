from __future__ import annotations

import argparse
from collections import defaultdict
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

from theorems.native_higher_call_weighted_fourier_pinching_audit import (
    bilinear_fourier_phase,
    k_call_statevector,
    signed_net_error_phase,
    signed_net_frequency,
)


SCHEMA_VERSION = "2026-04-12.native-higher-call-secret-subspace-restriction-audit.v1"
DEFAULT_CONTRACT_PATH = (
    ROOT
    / "research"
    / "hypotheses"
    / "native_higher_call_secret_subspace_restriction_audit_contract.json"
)
DEFAULT_ARTIFACT_PATH = (
    ROOT
    / "research"
    / "reductions"
    / "native_higher_call_secret_subspace_restriction_audit.json"
)
DEFAULT_DOC_PATH = (
    ROOT / "research" / "NATIVE_HIGHER_CALL_SECRET_SUBSPACE_RESTRICTION_AUDIT.md"
)


def canonical_sha256(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def load_contract(path: Path = DEFAULT_CONTRACT_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def evaluate_secret_subspace_case(
    *,
    case_id: str,
    D: int,
    q: int,
    n: int,
    subspace_basis_cols: list[list[int]],
    freq_table: list[tuple[int, ...]],
    error_table: list[int],
    epsilon: tuple[int, ...],
    sigma: tuple[int, ...],
    tolerance: float = 1e-12,
) -> dict[str, Any]:
    """Verify Theorems 1, 2, and 3 on secret subspace W_S = colspan(G_S) in F_q^n."""
    G_S = np.array(subspace_basis_cols, dtype=int).T % q  # shape (n, r)
    n_rows, r = G_S.shape
    if n_rows != n:
        raise ValueError("G_S row count must equal n")
    k = len(epsilon)

    # 1. Construct W_S, W_S^perp, and the q^{n-r} cosets W_S + a in F_q^n / W_S
    all_secrets = [tuple(s) for s in itertools.product(range(q), repeat=n)]
    W_S_set = {
        tuple(((G_S @ np.array(z, dtype=int)) % q).tolist())
        for z in itertools.product(range(q), repeat=r)
    }
    if len(W_S_set) != q ** r:
        raise ValueError("subspace_basis_cols must be linearly independent over F_q")

    W_S_perp_set = {
        delta
        for delta in all_secrets
        if np.all((G_S.T @ np.array(delta, dtype=int)) % q == 0)
    }
    if len(W_S_perp_set) != q ** (n - r):
        raise ValueError("W_S^perp size mismatch")

    # Partition F_q^n into q^{n-r} cosets of W_S
    cosets: list[list[tuple[int, ...]]] = []
    visited: set[tuple[int, ...]] = set()
    for s in all_secrets:
        if s in visited:
            continue
        coset = [
            tuple((s[j] + w_s[j]) % q for j in range(n)) for w_s in sorted(W_S_set)
        ]
        visited.update(coset)
        cosets.append(coset)

    # 2. Evaluate P_{epsilon, sigma}(x | s) for all s in F_q^n
    born_by_s: dict[tuple[int, ...], np.ndarray] = {}
    for s in all_secrets:
        y_s = [
            (sum(freq_table[w][j] * s[j] for j in range(n)) + error_table[w]) % q
            for w in range(D)
        ]
        psi = k_call_statevector(D, q, y_s, epsilon, sigma)
        born_by_s[s] = np.abs(psi) ** 2

    # 3. Compute full-space harmonics C_{epsilon, sigma}(delta; x) for all delta in F_q^n
    trajectories = list(itertools.product(range(D), repeat=k))
    num_traj = len(trajectories)
    tau_list = [signed_net_frequency(w, freq_table, epsilon, q) for w in trajectories]
    err_list = [signed_net_error_phase(w, error_table, epsilon, q) for w in trajectories]

    amps_by_x = []
    for x in range(D):
        row = []
        for idx, w in enumerate(trajectories):
            phi_val = bilinear_fourier_phase(w, sigma, x, D)
            angle = (2.0 * math.pi * err_list[idx] / float(q)) + (
                2.0 * math.pi * phi_val / float(D)
            )
            row.append(complex(math.cos(angle), math.sin(angle)))
        amps_by_x.append(row)

    diff_fibers: dict[tuple[int, ...], list[tuple[int, int]]] = defaultdict(list)
    for a in range(num_traj):
        for b in range(num_traj):
            delta = tuple((tau_list[a][j] - tau_list[b][j]) % q for j in range(n))
            diff_fibers[delta].append((a, b))

    norm_denom = float(D ** (k + 1))
    harmonics: dict[tuple[int, ...], list[complex]] = {
        delta: [0.0 + 0.0j] * D for delta in all_secrets
    }
    for delta, pair_list in diff_fibers.items():
        c_list = []
        for x in range(D):
            pair_sum = sum(
                amps_by_x[x][a] * amps_by_x[x][b].conjugate() for a, b in pair_list
            )
            c_list.append(pair_sum / norm_denom)
        harmonics[delta] = c_list

    # 4. Verify Theorem 1: Projected variety pinching on W_S
    emp_ws_mean = np.mean([born_by_s[s] for s in sorted(W_S_set)], axis=0)
    proj_fibers: dict[tuple[int, ...], list[int]] = defaultdict(list)
    for idx, tau in enumerate(tau_list):
        tau_bar = tuple(((G_S.T @ np.array(tau, dtype=int)) % q).tolist())
        proj_fibers[tau_bar].append(idx)

    proj_variety_size = sum(len(idxs) ** 2 for idxs in proj_fibers.values())
    pinched_ws_probs = np.zeros(D, dtype=np.float64)
    for x in range(D):
        sq_sum = 0.0
        for idxs in proj_fibers.values():
            f_amp = sum(amps_by_x[x][idx] for idx in idxs)
            sq_sum += f_amp.real ** 2 + f_amp.imag ** 2
        pinched_ws_probs[x] = sq_sum / norm_denom

    sum_ws_perp_harmonics = np.array(
        [
            sum(harmonics[delta][x] for delta in W_S_perp_set).real
            for x in range(D)
        ],
        dtype=np.float64,
    )
    theorem1_residual = max(
        float(np.max(np.abs(emp_ws_mean - pinched_ws_probs))),
        float(np.max(np.abs(emp_ws_mean - sum_ws_perp_harmonics))),
    )
    theorem1_verified = bool(theorem1_residual <= tolerance)

    # 5. Verify Theorem 2: Folded Parseval identity for Var_{s ~ W_S}[P(x | s)]
    ws_born_mat = np.array([born_by_s[s] for s in sorted(W_S_set)], dtype=np.float64)
    emp_ws_var = np.mean((ws_born_mat - emp_ws_mean[None, :]) ** 2, axis=0)

    folded_harmonics: dict[tuple[int, ...], list[complex]] = defaultdict(
        lambda: [0.0 + 0.0j] * D
    )
    for delta, c_list in harmonics.items():
        delta_bar = tuple(((G_S.T @ np.array(delta, dtype=int)) % q).tolist())
        for x in range(D):
            folded_harmonics[delta_bar][x] += c_list[x]

    zero_r = tuple([0] * r)
    folded_parseval_var = np.zeros(D, dtype=np.float64)
    for delta_bar, c_list in folded_harmonics.items():
        if delta_bar == zero_r:
            continue
        for x in range(D):
            folded_parseval_var[x] += (c_list[x].real ** 2 + c_list[x].imag ** 2)

    theorem2_residual = float(np.max(np.abs(emp_ws_var - folded_parseval_var)))
    theorem2_verified = bool(theorem2_residual <= tolerance)

    # 6. Verify Theorem 3: Fourier-space Law of Total Variance across F_q^n / W_S
    full_born_mat = np.array([born_by_s[s] for s in all_secrets], dtype=np.float64)
    full_mean = np.mean(full_born_mat, axis=0)
    emp_total_var = np.mean((full_born_mat - full_mean[None, :]) ** 2, axis=0)

    coset_means = []
    coset_vars = []
    for coset in cosets:
        c_mat = np.array([born_by_s[s] for s in coset], dtype=np.float64)
        c_mean = np.mean(c_mat, axis=0)
        c_var = np.mean((c_mat - c_mean[None, :]) ** 2, axis=0)
        coset_means.append(c_mean)
        coset_vars.append(c_var)

    coset_means_arr = np.array(coset_means, dtype=np.float64)
    emp_between_var = np.mean(
        (coset_means_arr - full_mean[None, :]) ** 2, axis=0
    )
    emp_within_var = np.mean(coset_vars, axis=0)

    zero_n = tuple([0] * n)
    fourier_between_var = np.zeros(D, dtype=np.float64)
    fourier_within_var = np.zeros(D, dtype=np.float64)
    for delta, c_list in harmonics.items():
        if delta == zero_n:
            continue
        in_perp = delta in W_S_perp_set
        for x in range(D):
            mod_sq = c_list[x].real ** 2 + c_list[x].imag ** 2
            if in_perp:
                fourier_between_var[x] += mod_sq
            else:
                fourier_within_var[x] += mod_sq

    between_var_residual = float(
        np.max(np.abs(emp_between_var - fourier_between_var))
    )
    within_var_residual = float(np.max(np.abs(emp_within_var - fourier_within_var)))
    total_var_decomp_residual = float(
        np.max(
            np.abs(emp_total_var - (fourier_between_var + fourier_within_var))
        )
    )
    theorem3_verified = bool(
        between_var_residual <= tolerance
        and within_var_residual <= tolerance
        and total_var_decomp_residual <= tolerance
    )

    return {
        "case_id": case_id,
        "D": D,
        "q": q,
        "n": n,
        "r_subspace_dim": r,
        "k_calls": k,
        "epsilon": list(epsilon),
        "sigma": list(sigma),
        "projected_variety_size": proj_variety_size,
        "full_variety_size": len(diff_fibers[zero_n]),
        "total_l2_variance": float(np.sum(emp_total_var)),
        "between_coset_l2_variance": float(np.sum(emp_between_var)),
        "expected_within_coset_l2_variance": float(np.sum(emp_within_var)),
        "homogeneous_subspace_ws_l2_variance": float(np.sum(emp_ws_var)),
        "theorem1_residual": theorem1_residual,
        "theorem2_residual": theorem2_residual,
        "between_var_residual": between_var_residual,
        "within_var_residual": within_var_residual,
        "total_var_decomp_residual": total_var_decomp_residual,
        "theorem1_verified": theorem1_verified,
        "theorem2_verified": theorem2_verified,
        "theorem3_verified": theorem3_verified,
        "all_theorems_verified": bool(
            theorem1_verified and theorem2_verified and theorem3_verified
        ),
    }


def build_native_higher_call_secret_subspace_restriction_audit(
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> dict[str, Any]:
    contract = load_contract(contract_path)

    case_specs = [
        {
            "case_id": "k2_unsigned_D3_q3_n2_r1_first_coord",
            "D": 3,
            "q": 3,
            "n": 2,
            "subspace_basis_cols": [[1, 0]],
            "freq_table": [(1, 0), (0, 1), (1, 1)],
            "error_table": [0, 1, 2],
            "epsilon": (1, 1),
            "sigma": (1, -1),
        },
        {
            "case_id": "k2_balanced_signed_D3_q3_n2_r1_diagonal",
            "D": 3,
            "q": 3,
            "n": 2,
            "subspace_basis_cols": [[1, 1]],
            "freq_table": [(1, 0), (0, 1), (1, 1)],
            "error_table": [0, 1, 2],
            "epsilon": (1, -1),
            "sigma": (1, -1),
        },
        {
            "case_id": "k2_balanced_signed_D3_q3_n3_r2_plane",
            "D": 3,
            "q": 3,
            "n": 3,
            "subspace_basis_cols": [[1, 0, 1], [0, 1, 2]],
            "freq_table": [(1, 0, 2), (0, 1, 1), (1, 2, 0)],
            "error_table": [0, 1, 2],
            "epsilon": (1, -1),
            "sigma": (1, -1),
        },
        {
            "case_id": "k3_alternating_signed_D3_q3_n2_r1_skew",
            "D": 3,
            "q": 3,
            "n": 2,
            "subspace_basis_cols": [[1, 2]],
            "freq_table": [(1, 0), (0, 1), (1, 1)],
            "error_table": [0, 1, 2],
            "epsilon": (1, -1, 1),
            "sigma": (1, -1, 1),
        },
        {
            "case_id": "k3_unsigned_D3_q3_n3_r1_line",
            "D": 3,
            "q": 3,
            "n": 3,
            "subspace_basis_cols": [[1, 1, 2]],
            "freq_table": [(1, 0, 1), (0, 1, 1), (1, 1, 0)],
            "error_table": [1, 0, 2],
            "epsilon": (1, 1, 1),
            "sigma": (1, -1, 1),
        },
    ]

    cases = [evaluate_secret_subspace_case(**spec) for spec in case_specs]
    all_verified = bool(all(c["all_theorems_verified"] for c in cases))

    summary = {
        "case_count": len(cases),
        "all_cases_verified": all_verified,
        "max_theorem1_residual": max(c["theorem1_residual"] for c in cases),
        "max_theorem2_residual": max(c["theorem2_residual"] for c in cases),
        "max_total_var_decomp_residual": max(
            c["total_var_decomp_residual"] for c in cases
        ),
        "scientific_verdict": (
            "Across k in {2, 3} oracle calls and secret subspaces W_S subseteq F_q^n, averaging over "
            "s ~ Unif(W_S) pinches the trajectory sum onto V_epsilon(f; W_S) = {(w, w') : tau(w) - tau(w') "
            "in W_S^perp}, while within-subspace variance equals the sum of squared moduli of the folded "
            "harmonics C^{(W_S)}(delta_bar; x). Across the quotient cosets F_q^n / W_S, the Law of Total "
            "Variance partitions the non-zero Fourier difference spectrum into W_S^perp \\ {0} (between-coset "
            "variance) and F_q^n \\ W_S^perp (expected within-coset variance)."
        ),
    }

    payload_without_digest = {
        "schema_version": SCHEMA_VERSION,
        "contract_id": contract["contract_id"],
        "title": contract["title"],
        "status": (
            "VERIFIED_EXACT_SECRET_SUBSPACE_PINCHING_AND_TOTAL_VARIANCE_PARTITION"
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


def write_native_higher_call_secret_subspace_restriction_audit(
    output_path: Path = DEFAULT_ARTIFACT_PATH,
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> dict[str, Any]:
    payload = build_native_higher_call_secret_subspace_restriction_audit(
        contract_path=contract_path
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build or write the native higher-call secret-subspace restriction audit."
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
        payload = write_native_higher_call_secret_subspace_restriction_audit(
            output_path=args.output
        )
    else:
        payload = build_native_higher_call_secret_subspace_restriction_audit()

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
