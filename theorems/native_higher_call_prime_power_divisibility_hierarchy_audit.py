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

from theorems.native_higher_call_weighted_fourier_pinching_audit import (
    bilinear_fourier_phase,
    k_call_statevector,
    signed_net_error_phase,
    signed_net_frequency,
)


SCHEMA_VERSION = "2026-04-12.native-higher-call-prime-power-divisibility-hierarchy-audit.v1"
DEFAULT_CONTRACT_PATH = (
    ROOT
    / "research"
    / "hypotheses"
    / "native_higher_call_prime_power_divisibility_hierarchy_audit_contract.json"
)
DEFAULT_ARTIFACT_PATH = (
    ROOT
    / "research"
    / "reductions"
    / "native_higher_call_prime_power_divisibility_hierarchy_audit.json"
)
DEFAULT_DOC_PATH = (
    ROOT / "research" / "NATIVE_HIGHER_CALL_PRIME_POWER_DIVISIBILITY_HIERARCHY_AUDIT.md"
)


def canonical_sha256(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _frac_str(val: Fraction) -> str:
    return f"{val.numerator}/{val.denominator}"


def load_contract(path: Path = DEFAULT_CONTRACT_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def padic_valuation_int(val: int, p: int, r: int) -> int:
    """Return min(v_p(val mod p^r), r)."""
    q = p ** r
    v = val % q
    if v == 0:
        return r
    count = 0
    while v % p == 0 and count < r:
        v //= p
        count += 1
    return count


def padic_valuation_vec(vec: tuple[int, ...], p: int, r: int) -> int:
    """Return min_{i} v_p(vec[i] mod p^r) in {0, 1, ..., r}."""
    return min(padic_valuation_int(c, p, r) for c in vec)


def evaluate_divisibility_hierarchy_case(
    *,
    case_id: str,
    p: int,
    r: int,
    D: int,
    n: int,
    freq_table: list[tuple[int, ...]],
    error_table: list[int],
    epsilon: tuple[int, ...],
    sigma: tuple[int, ...],
    tolerance: float = 1e-12,
) -> dict[str, Any]:
    """Verify Theorems 1, 2, and 3 across all p-adic filtration levels j in {0, ..., r}."""
    q = p ** r
    k = len(epsilon)
    trajectories = list(itertools.product(range(D), repeat=k))
    num_traj = len(trajectories)  # D^k

    # Precompute tau_epsilon(w), E_epsilon(w), and Phi_sigma(w; x) for all w in {0, ..., D-1}^k
    tau_list = [signed_net_frequency(w, freq_table, epsilon, q) for w in trajectories]
    err_list = [signed_net_error_phase(w, error_table, epsilon, q) for w in trajectories]
    phi_by_x = [
        [bilinear_fourier_phase(w, sigma, x, D) for w in trajectories]
        for x in range(D)
    ]

    # Precompute complex trajectory amplitudes A(w; x) = exp(2 pi i E(w)/q + 2 pi i Phi(w; x)/D)
    amps_by_x = []
    for x in range(D):
        row = []
        for idx in range(num_traj):
            angle = (2.0 * math.pi * err_list[idx] / float(q)) + (
                2.0 * math.pi * phi_by_x[x][idx] / float(D)
            )
            row.append(complex(math.cos(angle), math.sin(angle)))
        amps_by_x.append(row)

    # 1. Evaluate level j in {0, ..., r}:
    #    - Direct subgroup average over H_j = p^{r-j} Z_{p^r}^n
    #    - Pinched congruence variety sum over V_epsilon^{(j)}(f)
    level_rows = []
    pinched_probs_by_level: list[np.ndarray] = []
    variety_sizes: list[int] = []
    max_theorem1_residual = 0.0

    for j in range(r + 1):
        mod_j = p ** j
        scale_j = p ** (r - j)
        # Subgroup H_j elements: s = scale_j * s' mod q for s' in {0, ..., p^j - 1}^n
        s_prime_tuples = list(itertools.product(range(mod_j), repeat=n))
        born_sum = np.zeros(D, dtype=np.float64)
        for s_prime in s_prime_tuples:
            s_vec = tuple((scale_j * c) % q for c in s_prime)
            y_s = [
                (sum(freq_table[w][coord] * s_vec[coord] for coord in range(n)) + error_table[w]) % q
                for w in range(D)
            ]
            psi = k_call_statevector(D, q, y_s, epsilon, sigma)
            born_sum += np.abs(psi) ** 2
        subgroup_avg_born = born_sum / float(len(s_prime_tuples))

        # Partition trajectories by tau_epsilon(w) mod p^j
        fibers_j: dict[tuple[int, ...], list[int]] = defaultdict(list)
        for idx, tau in enumerate(tau_list):
            key = tuple(c % mod_j for c in tau)
            fibers_j[key].append(idx)

        var_size_j = sum(len(idxs) ** 2 for idxs in fibers_j.values())
        variety_sizes.append(var_size_j)

        norm_denom = float(D ** (k + 1))
        pinched_j = np.zeros(D, dtype=np.float64)
        for x in range(D):
            sq_sum = 0.0
            for idxs in fibers_j.values():
                f_amp = sum(amps_by_x[x][idx] for idx in idxs)
                sq_sum += f_amp.real ** 2 + f_amp.imag ** 2
            pinched_j[x] = sq_sum / norm_denom

        pinched_probs_by_level.append(pinched_j)
        res_j = float(np.max(np.abs(subgroup_avg_born - pinched_j)))
        max_theorem1_residual = max(max_theorem1_residual, res_j)

        level_rows.append(
            {
                "level_j": j,
                "congruence_modulus_p_pow_j": mod_j,
                "subgroup_order_H_j": len(s_prime_tuples),
                "distinct_congruence_fibers": len(fibers_j),
                "variety_size_V_j": var_size_j,
                "variety_density_exact": _frac_str(Fraction(var_size_j, num_traj ** 2)),
                "subgroup_averaged_born_probs": [float(v) for v in subgroup_avg_born],
                "pinched_variety_probs": [float(v) for v in pinched_j],
                "theorem1_level_residual": res_j,
            }
        )

    # 2. Verify Theorem 2 & Theorem 3 across valuation shells D_epsilon^{(j)}(f) = V^{(j)} \ V^{(j+1)}
    shell_rows = []
    shell_counts_sum = 0
    max_shell_formula_residual = 0.0
    max_shell_zero_sum_residual = 0.0
    norm_denom = float(D ** (k + 1))

    for j in range(r):
        # Explicitly enumerate pairs (idx_a, idx_b) with v_p(tau(w_a) - tau(w_b)) == j
        shell_pairs = []
        diagonal_in_shell = 0
        for idx_a in range(num_traj):
            for idx_b in range(num_traj):
                diff_vec = tuple((tau_list[idx_a][c] - tau_list[idx_b][c]) % q for c in range(n))
                val = padic_valuation_vec(diff_vec, p, r)
                if val == j:
                    shell_pairs.append((idx_a, idx_b))
                    if idx_a == idx_b:
                        diagonal_in_shell += 1

        shell_count = len(shell_pairs)
        expected_shell_count = variety_sizes[j] - variety_sizes[j + 1]
        shell_counts_sum += shell_count

        # Compute direct shell sum for each outcome x in {0, ..., D-1}
        shell_probs_direct = np.zeros(D, dtype=np.float64)
        for x in range(D):
            pair_sum = 0.0 + 0.0j
            for idx_a, idx_b in shell_pairs:
                pair_sum += amps_by_x[x][idx_a] * amps_by_x[x][idx_b].conjugate()
            shell_probs_direct[x] = pair_sum.real / norm_denom

        increment_from_levels = pinched_probs_by_level[j] - pinched_probs_by_level[j + 1]
        shell_formula_res = float(np.max(np.abs(shell_probs_direct - increment_from_levels)))
        shell_zero_sum_res = abs(float(np.sum(shell_probs_direct)))
        max_shell_formula_residual = max(max_shell_formula_residual, shell_formula_res)
        max_shell_zero_sum_residual = max(max_shell_zero_sum_residual, shell_zero_sum_res)

        shell_rows.append(
            {
                "shell_valuation_j": j,
                "shell_pair_count": shell_count,
                "variety_difference_V_j_minus_V_j_plus_1": expected_shell_count,
                "diagonal_pairs_in_shell": diagonal_in_shell,
                "shell_increment_probs": [float(v) for v in shell_probs_direct],
                "shell_increment_sum_over_x": float(np.sum(shell_probs_direct)),
                "shell_formula_vs_level_diff_residual": shell_formula_res,
            }
        )

    # Check monotone filtration and telescoping identities
    monotone_filtration_holds = (
        variety_sizes[0] == num_traj ** 2
        and all(variety_sizes[j] >= variety_sizes[j + 1] for j in range(r))
        and variety_sizes[r] >= num_traj
    )
    telescoping_count_holds = (
        variety_sizes[r] + shell_counts_sum == num_traj ** 2
        and all(
            s["shell_pair_count"] == s["variety_difference_V_j_minus_V_j_plus_1"]
            and s["diagonal_pairs_in_shell"] == 0
            for s in shell_rows
        )
    )
    total_prob_telescoping_residual = float(
        np.max(
            np.abs(
                pinched_probs_by_level[0]
                - (
                    pinched_probs_by_level[r]
                    + sum(np.array(s["shell_increment_probs"]) for s in shell_rows)
                )
            )
        )
    )

    theorem1_verified = max_theorem1_residual <= tolerance
    theorem2_verified = monotone_filtration_holds and telescoping_count_holds
    theorem3_verified = (
        max_shell_formula_residual <= tolerance
        and max_shell_zero_sum_residual <= tolerance
        and total_prob_telescoping_residual <= tolerance
    )

    return {
        "case_id": case_id,
        "p": p,
        "r": r,
        "q": q,
        "D": D,
        "n": n,
        "k_calls": k,
        "epsilon": list(epsilon),
        "sigma": list(sigma),
        "variety_sizes_by_level": variety_sizes,
        "level_rows": level_rows,
        "shell_rows": shell_rows,
        "max_theorem1_residual": max_theorem1_residual,
        "max_shell_formula_residual": max_shell_formula_residual,
        "max_shell_zero_sum_residual": max_shell_zero_sum_residual,
        "total_prob_telescoping_residual": total_prob_telescoping_residual,
        "theorem1_verified": theorem1_verified,
        "theorem2_verified": theorem2_verified,
        "theorem3_verified": theorem3_verified,
        "all_theorems_verified": (
            theorem1_verified and theorem2_verified and theorem3_verified
        ),
    }


def build_native_higher_call_prime_power_divisibility_hierarchy_audit(
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> dict[str, Any]:
    contract = load_contract(contract_path)

    case_specs = [
        {
            "case_id": "k2_unsigned_p3_r2_q9_D3_n1",
            "p": 3,
            "r": 2,
            "D": 3,
            "n": 1,
            "freq_table": [(1,), (4,), (2,)],
            "error_table": [0, 2, 5],
            "epsilon": (1, 1),
            "sigma": (1, -1),
        },
        {
            "case_id": "k2_balanced_signed_p3_r2_q9_D3_n1",
            "p": 3,
            "r": 2,
            "D": 3,
            "n": 1,
            "freq_table": [(1,), (4,), (2,)],
            "error_table": [0, 2, 5],
            "epsilon": (1, -1),
            "sigma": (1, -1),
        },
        {
            "case_id": "k2_balanced_signed_p3_r2_q9_D3_n2",
            "p": 3,
            "r": 2,
            "D": 3,
            "n": 2,
            "freq_table": [(1, 3), (4, 0), (2, 6)],
            "error_table": [1, 4, 7],
            "epsilon": (1, -1),
            "sigma": (1, -1),
        },
        {
            "case_id": "k2_balanced_signed_p3_r3_q27_D3_n1",
            "p": 3,
            "r": 3,
            "D": 3,
            "n": 1,
            "freq_table": [(1,), (4,), (10,)],
            "error_table": [0, 3, 9],
            "epsilon": (1, -1),
            "sigma": (1, -1),
        },
        {
            "case_id": "k3_alternating_signed_p3_r2_q9_D3_n1",
            "p": 3,
            "r": 2,
            "D": 3,
            "n": 1,
            "freq_table": [(1,), (4,), (2,)],
            "error_table": [0, 3, 6],
            "epsilon": (1, -1, 1),
            "sigma": (1, -1, 1),
        },
    ]

    cases = [evaluate_divisibility_hierarchy_case(**spec) for spec in case_specs]
    all_verified = all(c["all_theorems_verified"] for c in cases)

    summary = {
        "case_count": len(cases),
        "all_cases_verified": all_verified,
        "max_theorem1_residual": max(c["max_theorem1_residual"] for c in cases),
        "max_shell_formula_residual": max(c["max_shell_formula_residual"] for c in cases),
        "max_shell_zero_sum_residual": max(c["max_shell_zero_sum_residual"] for c in cases),
        "scientific_verdict": (
            "Across prime-power moduli q = p^r (q = 9, 27) and k in {2, 3} oracle calls, averaging the "
            "k-call Born distribution over the p-adic secret subgroup H_j = p^{r-j} Z_{p^r}^n pinches "
            "the trajectory sum onto the congruence collision variety V_epsilon^{(j)}(f) = {(w, w') : "
            "tau_epsilon(w) == tau_epsilon(w') mod p^j}. The varieties form a monotone filtration whose "
            "successive valuation shells D_epsilon^{(j)}(f) = V_epsilon^{(j)}(f) \\ V_epsilon^{(j+1)}(f) "
            "contain zero diagonal pairs, have zero-sum oscillatory probability increments across x in {0, ..., D-1}, "
            "and telescope exactly to the full gap between single-instance and uniform-secret averages."
        ),
    }

    payload_without_digest = {
        "schema_version": SCHEMA_VERSION,
        "contract_id": contract["contract_id"],
        "title": contract["title"],
        "status": (
            "VERIFIED_EXACT_PRIME_POWER_DIVISIBILITY_PINCHING_HIERARCHY"
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


def write_native_higher_call_prime_power_divisibility_hierarchy_audit(
    output_path: Path = DEFAULT_ARTIFACT_PATH,
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> dict[str, Any]:
    payload = build_native_higher_call_prime_power_divisibility_hierarchy_audit(
        contract_path=contract_path
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build or write the native higher-call prime-power divisibility hierarchy audit."
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
        payload = write_native_higher_call_prime_power_divisibility_hierarchy_audit(
            output_path=args.output
        )
    else:
        payload = build_native_higher_call_prime_power_divisibility_hierarchy_audit()

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
