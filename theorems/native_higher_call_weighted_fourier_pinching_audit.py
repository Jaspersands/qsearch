from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction
import itertools
import json
import math
from pathlib import Path
import sys
from typing import Any

import numpy as np

import hashlib

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def canonical_sha256(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


SCHEMA_VERSION = "2026-04-12.native-higher-call-weighted-fourier-pinching-audit.v1"
DEFAULT_CONTRACT_PATH = (
    ROOT / "research" / "hypotheses" / "native_higher_call_weighted_fourier_pinching_audit_contract.json"
)
DEFAULT_ARTIFACT_PATH = (
    ROOT / "research" / "reductions" / "native_higher_call_weighted_fourier_pinching_audit.json"
)
DEFAULT_DOC_PATH = (
    ROOT / "research" / "NATIVE_HIGHER_CALL_WEIGHTED_FOURIER_PINCHING_AUDIT.md"
)


def _frac_str(val: Fraction) -> str:
    return f"{val.numerator}/{val.denominator}"


def load_contract(path: Path = DEFAULT_CONTRACT_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def fourier_matrix_power(D: int, sigma: int) -> np.ndarray:
    """Return F_D^{sigma} where <b | F_D^{sigma} | a> = D^{-1/2} exp(sigma * 2 pi i a b / D)."""
    if sigma not in (-1, 1):
        raise ValueError("sigma must be -1 or +1")
    grid = np.outer(np.arange(D, dtype=np.float64), np.arange(D, dtype=np.float64))
    return np.exp(sigma * 2j * np.pi * grid / float(D)) / math.sqrt(float(D))


def k_call_statevector(
    D: int,
    q: int,
    y_phases: list[int] | np.ndarray,
    epsilon: tuple[int, ...],
    sigma: tuple[int, ...],
) -> np.ndarray:
    """Compute |Psi_{epsilon, sigma}(y)> = F_D^{sigma_k} D_y^{epsilon_k} ... F_D^{sigma_1} D_y^{epsilon_1} |+_D>."""
    k = len(epsilon)
    if len(sigma) != k:
        raise ValueError("epsilon and sigma must have the same length")
    y_arr = np.asarray(y_phases, dtype=np.float64)
    state = np.ones(D, dtype=np.complex128) / math.sqrt(float(D))
    for ell in range(k):
        diag_phase = np.exp(epsilon[ell] * 2j * np.pi * y_arr / float(q))
        state = diag_phase * state
        F_step = fourier_matrix_power(D, sigma[ell])
        state = F_step @ state
    return state


def signed_net_frequency(
    w_tuple: tuple[int, ...],
    freq_table: list[tuple[int, ...]],
    epsilon: tuple[int, ...],
    q: int,
) -> tuple[int, ...]:
    """Compute tau_epsilon(w) = sum_{ell=1}^k epsilon_ell f(w_ell) mod q."""
    n = len(freq_table[0])
    out = [0] * n
    for w_ell, eps_ell in zip(w_tuple, epsilon):
        fw = freq_table[w_ell]
        for j in range(n):
            out[j] = (out[j] + eps_ell * fw[j]) % q
    return tuple(out)


def signed_net_error_phase(
    w_tuple: tuple[int, ...],
    error_table: list[int],
    epsilon: tuple[int, ...],
    q: int,
) -> int:
    """Compute E_epsilon(w) = sum_{ell=1}^k epsilon_ell e(w_ell) mod q."""
    total = 0
    for w_ell, eps_ell in zip(w_tuple, epsilon):
        total = (total + eps_ell * error_table[w_ell]) % q
    return total


def bilinear_fourier_phase(
    w_tuple: tuple[int, ...],
    sigma: tuple[int, ...],
    x: int,
    D: int,
) -> int:
    """Compute Phi_sigma(w; x) = (sum_{ell=1}^{k-1} sigma_ell w_{ell+1} w_ell + sigma_k x w_k) mod D."""
    k = len(w_tuple)
    total = 0
    for ell in range(k - 1):
        total += sigma[ell] * w_tuple[ell + 1] * w_tuple[ell]
    total += sigma[k - 1] * x * w_tuple[k - 1]
    return total % D


def evaluate_schedule_case(
    *,
    case_id: str,
    D: int,
    q: int,
    n: int,
    freq_table: list[tuple[int, ...]],
    error_table: list[int],
    epsilon: tuple[int, ...],
    sigma: tuple[int, ...],
    tolerance: float = 1e-12,
) -> dict[str, Any]:
    """Verify Theorems 1, 2, and 3 on a concrete k-call schedule and word frequency table."""
    k = len(epsilon)
    if len(freq_table) != D or len(error_table) != D:
        raise ValueError("freq_table and error_table must have length D")

    # 1. Exhaustive secret average over s in Z_q^n of exact statevector Born probabilities
    secrets = list(itertools.product(range(q), repeat=n))
    num_secrets = len(secrets)
    born_sum = np.zeros(D, dtype=np.float64)
    for s in secrets:
        y_s = [
            (sum(freq_table[w][j] * s[j] for j in range(n)) + error_table[w]) % q
            for w in range(D)
        ]
        psi = k_call_statevector(D, q, y_s, epsilon, sigma)
        born_sum += np.abs(psi) ** 2
    secret_averaged_born = born_sum / float(num_secrets)

    # 2. Partition all D^k trajectories into signed frequency fibers tau_epsilon(w)
    trajectories = list(itertools.product(range(D), repeat=k))
    fibers: dict[tuple[int, ...], list[tuple[int, ...]]] = defaultdict(list)
    for w_tuple in trajectories:
        tau = signed_net_frequency(w_tuple, freq_table, epsilon, q)
        fibers[tau].append(w_tuple)

    # Collision variety count |V_epsilon(f)| = sum_tau |fiber(tau)|^2
    variety_size = sum(len(f_list) ** 2 for f_list in fibers.values())
    total_trajectory_pairs = D ** (2 * k)
    diagonal_trajectory_count = D ** k
    off_diagonal_collision_count = variety_size - diagonal_trajectory_count
    unweighted_collision_ratio = Fraction(variety_size, total_trajectory_pairs)
    zero_fiber_multiplicity = len(fibers.get(tuple([0] * n), []))

    # 3. Theorem 1 & Theorem 2: Pinched fiber squared-modulus sum and diagonal/off-diagonal split
    pinched_probs = np.zeros(D, dtype=np.float64)
    off_diagonal_surplus = np.zeros(D, dtype=np.float64)
    diagonal_floor = 1.0 / float(D)
    norm_denom = float(D ** (k + 1))

    for x in range(D):
        fiber_sq_sum = 0.0
        off_diag_sum = 0.0 + 0.0j
        for tau, f_list in fibers.items():
            amps = []
            for w_tuple in f_list:
                e_val = signed_net_error_phase(w_tuple, error_table, epsilon, q)
                phi_val = bilinear_fourier_phase(w_tuple, sigma, x, D)
                phase = (2.0 * math.pi * e_val / float(q)) + (2.0 * math.pi * phi_val / float(D))
                amps.append( complex(math.cos(phase), math.sin(phase)) )
            fiber_amp = sum(amps)
            fiber_sq_sum += (fiber_amp.real ** 2 + fiber_amp.imag ** 2)
            # Off-diagonal pairs in this fiber
            m = len(amps)
            for idx_a in range(m):
                for idx_b in range(m):
                    if idx_a != idx_b:
                        off_diag_sum += amps[idx_a] * amps[idx_b].conjugate()
        pinched_probs[x] = fiber_sq_sum / norm_denom
        off_diagonal_surplus[x] = off_diag_sum.real / norm_denom

    # Residuals
    theorem1_max_residual = float(np.max(np.abs(secret_averaged_born - pinched_probs)))
    theorem2_decomp_residual = float(
        np.max(np.abs(pinched_probs - (diagonal_floor + off_diagonal_surplus)))
    )
    off_diagonal_sum = float(np.sum(off_diagonal_surplus))
    prob_normalization_residual = abs(float(np.sum(pinched_probs)) - 1.0)

    # Check Theorem 3 properties for k=2
    transpose_off_diag_collisions = 0
    self_diff_in_zero_fiber = 0
    if k == 2:
        for w1 in range(D):
            for w2 in range(D):
                if w1 != w2:
                    t1 = signed_net_frequency((w1, w2), freq_table, epsilon, q)
                    t2 = signed_net_frequency((w2, w1), freq_table, epsilon, q)
                    if t1 == t2:
                        transpose_off_diag_collisions += 1
            t_diag = signed_net_frequency((w1, w1), freq_table, epsilon, q)
            if all(c == 0 for c in t_diag):
                self_diff_in_zero_fiber += 1

    verified = (
        theorem1_max_residual <= tolerance
        and theorem2_decomp_residual <= tolerance
        and abs(off_diagonal_sum) <= tolerance
        and prob_normalization_residual <= tolerance
    )

    return {
        "case_id": case_id,
        "D": D,
        "q": q,
        "n": n,
        "k_calls": k,
        "epsilon": list(epsilon),
        "sigma": list(sigma),
        "freq_table": [list(row) for row in freq_table],
        "error_table": list(error_table),
        "distinct_active_fibers": len(fibers),
        "zero_fiber_multiplicity": zero_fiber_multiplicity,
        "variety_size_V_epsilon": variety_size,
        "diagonal_trajectory_count": diagonal_trajectory_count,
        "off_diagonal_collision_count": off_diagonal_collision_count,
        "unweighted_collision_ratio_exact": _frac_str(unweighted_collision_ratio),
        "unweighted_collision_ratio_float": float(unweighted_collision_ratio),
        "diagonal_floor_exact": _frac_str(Fraction(1, D)),
        "diagonal_floor_float": diagonal_floor,
        "secret_averaged_born_probs": [float(v) for v in secret_averaged_born],
        "pinched_variety_probs": [float(v) for v in pinched_probs],
        "off_diagonal_surplus": [float(v) for v in off_diagonal_surplus],
        "off_diagonal_surplus_sum": off_diagonal_sum,
        "max_abs_off_diagonal_surplus": float(np.max(np.abs(off_diagonal_surplus))),
        "l1_tv_distance_from_uniform": 0.5 * float(np.sum(np.abs(off_diagonal_surplus))),
        "theorem1_secret_avg_vs_pinched_residual": theorem1_max_residual,
        "theorem2_floor_plus_offdiag_residual": theorem2_decomp_residual,
        "probability_normalization_residual": prob_normalization_residual,
        "k2_transpose_off_diagonal_collisions": transpose_off_diag_collisions,
        "k2_self_difference_zero_fiber_count": self_diff_in_zero_fiber,
        "exact_verification_passed": verified,
    }


def build_native_higher_call_weighted_fourier_pinching_audit(
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> dict[str, Any]:
    contract = load_contract(contract_path)

    # Canonical ternary/prime-power word tables (D=3, q=3, n=2 and D=3, q=9, n=1)
    # plus 3-call schedules (k=3, D=3, q=3, n=2)
    case_specs = [
        {
            "case_id": "k2_unsigned_sum_pinching_D3_q3_n2",
            "D": 3,
            "q": 3,
            "n": 2,
            "freq_table": [(1, 0), (0, 1), (1, 1)],
            "error_table": [0, 1, 2],
            "epsilon": (1, 1),
            "sigma": (1, -1),
        },
        {
            "case_id": "k2_balanced_signed_diff_pinching_D3_q3_n2",
            "D": 3,
            "q": 3,
            "n": 2,
            "freq_table": [(1, 0), (0, 1), (1, 1)],
            "error_table": [0, 1, 2],
            "epsilon": (1, -1),
            "sigma": (1, -1),
        },
        {
            "case_id": "k2_unsigned_degenerate_collision_D3_q3_n2",
            "D": 3,
            "q": 3,
            "n": 2,
            "freq_table": [(1, 2), (1, 2), (2, 1)],
            "error_table": [0, 1, 0],
            "epsilon": (1, 1),
            "sigma": (1, -1),
        },
        {
            "case_id": "k2_balanced_signed_degenerate_collision_D3_q3_n2",
            "D": 3,
            "q": 3,
            "n": 2,
            "freq_table": [(1, 2), (1, 2), (2, 1)],
            "error_table": [0, 1, 0],
            "epsilon": (1, -1),
            "sigma": (1, -1),
        },
        {
            "case_id": "k3_alternating_signed_pinching_D3_q3_n2",
            "D": 3,
            "q": 3,
            "n": 2,
            "freq_table": [(1, 0), (0, 1), (1, 1)],
            "error_table": [0, 1, 2],
            "epsilon": (1, -1, 1),
            "sigma": (1, -1, 1),
        },
        {
            "case_id": "k3_unsigned_all_plus_pinching_D3_q3_n2",
            "D": 3,
            "q": 3,
            "n": 2,
            "freq_table": [(1, 0), (0, 1), (1, 1)],
            "error_table": [0, 1, 2],
            "epsilon": (1, 1, 1),
            "sigma": (1, -1, 1),
        },
        {
            "case_id": "k3_prime_power_q9_pinching_D3_q9_n1",
            "D": 3,
            "q": 9,
            "n": 1,
            "freq_table": [(1,), (2,), (4,)],
            "error_table": [0, 3, 6],
            "epsilon": (1, -1, 1),
            "sigma": (1, 1, -1),
        },
    ]

    cases = [evaluate_schedule_case(**spec) for spec in case_specs]
    all_verified = all(c["exact_verification_passed"] for c in cases)

    # Check Theorem 3 contrast specifically on the first two cases (unsigned vs balanced signed on same f)
    unsigned_case = cases[0]
    balanced_case = cases[1]
    theorem3_verified = (
        unsigned_case["k2_transpose_off_diagonal_collisions"] == unsigned_case["D"] * (unsigned_case["D"] - 1)
        and balanced_case["k2_self_difference_zero_fiber_count"] == balanced_case["D"]
        and balanced_case["zero_fiber_multiplicity"] >= balanced_case["D"]
    )

    summary = {
        "case_count": len(cases),
        "all_cases_verified": all_verified and theorem3_verified,
        "theorem3_unsigned_vs_balanced_contrast_verified": theorem3_verified,
        "max_theorem1_pinching_residual": max(
            c["theorem1_secret_avg_vs_pinched_residual"] for c in cases
        ),
        "max_theorem2_decomposition_residual": max(
            c["theorem2_floor_plus_offdiag_residual"] for c in cases
        ),
        "max_off_diagonal_zero_sum_residual": max(
            abs(c["off_diagonal_surplus_sum"]) for c in cases
        ),
        "scientific_verdict": (
            "Averaging the k-call Born distribution of F_D^{sigma_k} D_y^{epsilon_k} ... F_D^{sigma_1} D_y^{epsilon_1} |+_D> "
            "over a uniform secret s in Z_q^n pinches the 2k-fold unitary path sum onto the signed frequency-collision "
            "variety V_epsilon(f) = {(w, w') : tau_epsilon(w) == tau_epsilon(w')}. The D^k diagonal trajectories w = w' "
            "contribute the universal 1/D uniform floor to every outcome x, while the off-diagonal collision pairs carry "
            "bilinear Fourier phases Phi_sigma(w; x) - Phi_sigma(w'; x) whose sum over x in {0, ..., D-1} vanishes identically. "
            "For k = 2, the balanced signed schedule epsilon = (+1, -1) concentrates all D self-difference trajectories "
            "w_1 = w_2 into the tau = 0 fiber, whereas the unsigned schedule epsilon = (+1, +1) pairs all D(D-1) "
            "off-diagonal transpose trajectories (w_1, w_2) <-> (w_2, w_1)."
        ),
    }

    payload_without_digest = {
        "schema_version": SCHEMA_VERSION,
        "contract_id": contract["contract_id"],
        "title": contract["title"],
        "status": (
            "VERIFIED_EXACT_K_CALL_WEIGHTED_FOURIER_PINCHING_IDENTITIES"
            if summary["all_cases_verified"]
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


def write_native_higher_call_weighted_fourier_pinching_audit(
    output_path: Path = DEFAULT_ARTIFACT_PATH,
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> dict[str, Any]:
    payload = build_native_higher_call_weighted_fourier_pinching_audit(contract_path=contract_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build or write the native higher-call weighted Fourier pinching audit."
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
        payload = write_native_higher_call_weighted_fourier_pinching_audit(output_path=args.output)
    else:
        payload = build_native_higher_call_weighted_fourier_pinching_audit()

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
