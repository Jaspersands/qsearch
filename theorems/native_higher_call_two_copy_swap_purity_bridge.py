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


SCHEMA_VERSION = "2026-04-12.native-higher-call-two-copy-swap-purity-bridge.v1"
DEFAULT_CONTRACT_PATH = (
    ROOT
    / "research"
    / "hypotheses"
    / "native_higher_call_two_copy_swap_purity_bridge_contract.json"
)
DEFAULT_ARTIFACT_PATH = (
    ROOT
    / "research"
    / "reductions"
    / "native_higher_call_two_copy_swap_purity_bridge.json"
)
DEFAULT_DOC_PATH = (
    ROOT / "research" / "NATIVE_HIGHER_CALL_TWO_COPY_SWAP_PURITY_BRIDGE.md"
)


def canonical_sha256(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _frac_str(val: Fraction) -> str:
    return f"{val.numerator}/{val.denominator}"


def load_contract(path: Path = DEFAULT_CONTRACT_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_swap_operator(D: int) -> np.ndarray:
    """Build exact D^2 x D^2 SWAP unitary S_D(|x1> tensor |x2>) = |x2> tensor |x1>."""
    S = np.zeros((D * D, D * D), dtype=np.complex128)
    for x1 in range(D):
        for x2 in range(D):
            col = x1 * D + x2
            row = x2 * D + x1
            S[row, col] = 1.0
    return S


def evaluate_two_copy_swap_case(
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
    """Verify Theorems 1, 2, and 3 on two-copy SWAP purity and CNOT difference readout."""
    k = len(epsilon)
    secrets = list(itertools.product(range(q), repeat=n))
    num_secrets = len(secrets)

    S_D = build_swap_operator(D)
    I_D2 = np.eye(D * D, dtype=np.complex128)
    Pi_anti = 0.5 * (I_D2 - S_D)

    # 1. Compute single-copy statevectors, Born distributions, and two-copy density operators
    psi_list = []
    born_matrix = np.zeros((num_secrets, D), dtype=np.float64)
    rho_bar = np.zeros((D, D), dtype=np.complex128)
    rho_same_2 = np.zeros((D * D, D * D), dtype=np.complex128)

    # Also compute flipped final Fourier direction sigma_flipped = sigma[:-1] + (-sigma[-1],)
    sigma_flipped = sigma[:-1] + (-sigma[-1],)
    rho_bar_flipped = np.zeros((D, D), dtype=np.complex128)

    for s_idx, s in enumerate(secrets):
        y_s = [
            (sum(freq_table[w][j] * s[j] for j in range(n)) + error_table[w]) % q
            for w in range(D)
        ]
        psi = k_call_statevector(D, q, y_s, epsilon, sigma)
        psi_list.append(psi)
        born_matrix[s_idx, :] = np.abs(psi) ** 2
        rho_s = np.outer(psi, psi.conj())
        rho_bar += rho_s
        psi_2 = np.kron(psi, psi)
        rho_same_2 += np.outer(psi_2, psi_2.conj())

        psi_flip = k_call_statevector(D, q, y_s, epsilon, sigma_flipped)
        rho_bar_flipped += np.outer(psi_flip, psi_flip.conj())

    rho_bar /= float(num_secrets)
    rho_same_2 /= float(num_secrets)
    rho_bar_flipped /= float(num_secrets)
    rho_ind_2 = np.kron(rho_bar, rho_bar)

    # Theorem 1: SWAP expectation on same-secret vs independent-secret pairs
    swap_same = float(np.real(np.trace(S_D @ rho_same_2)))
    anti_same = float(np.real(np.trace(Pi_anti @ rho_same_2)))
    swap_ind = float(np.real(np.trace(S_D @ rho_ind_2)))
    anti_ind = float(np.real(np.trace(Pi_anti @ rho_ind_2)))

    purity_rho_bar = float(np.real(np.trace(rho_bar @ rho_bar)))
    v_hs = 1.0 - purity_rho_bar
    swap_excess = swap_same - swap_ind

    theorem1_verified = (
        abs(swap_same - 1.0) <= tolerance
        and abs(anti_same) <= tolerance
        and abs(swap_ind - purity_rho_bar) <= tolerance
        and abs(swap_excess - v_hs) <= tolerance
        and abs(anti_ind - 0.5 * v_hs) <= tolerance
    )

    # Theorem 2: Final-Fourier direction invariance and k=1 rational collision variety law
    purity_flipped = float(np.real(np.trace(rho_bar_flipped @ rho_bar_flipped)))
    sigma_flip_residual = abs(purity_rho_bar - purity_flipped)

    trajectories = list(itertools.product(range(D), repeat=k))
    num_traj = len(trajectories)
    tau_list = [signed_net_frequency(w, freq_table, epsilon, q) for w in trajectories]
    err_list = [signed_net_error_phase(w, error_table, epsilon, q) for w in trajectories]

    # Collision variety size |V_epsilon(f)|
    variety_size = sum(
        1
        for a in range(num_traj)
        for b in range(num_traj)
        if tau_list[a] == tau_list[b]
    )

    if k == 1:
        k1_purity_exact = Fraction(variety_size, D * D)
        k1_purity_residual = abs(purity_rho_bar - float(k1_purity_exact))
        k1_verified = k1_purity_residual <= tolerance
    else:
        k1_purity_exact = None
        k1_purity_residual = 0.0
        k1_verified = True

    theorem2_verified = sigma_flip_residual <= tolerance and k1_verified

    # Theorem 3: Two-copy modular CNOT difference distribution P_diff(Delta | s)
    # Direct secret average of P_diff(Delta | s)
    emp_p_diff = np.zeros(D, dtype=np.float64)
    for Delta in range(D):
        shifted_born = np.roll(born_matrix, -Delta, axis=1)
        emp_p_diff[Delta] = float(np.mean(np.sum(born_matrix * shifted_born, axis=1)))

    # Harmonic autocorrelation formula using C_{epsilon, sigma}(delta; x)
    diff_fibers: dict[tuple[int, ...], list[tuple[int, int]]] = defaultdict(list)
    for a in range(num_traj):
        for b in range(num_traj):
            delta = tuple((tau_list[a][j] - tau_list[b][j]) % q for j in range(n))
            diff_fibers[delta].append((a, b))

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

    norm_denom = float(D ** (k + 1))
    harmonics: dict[tuple[int, ...], list[complex]] = {}
    for delta, pair_list in diff_fibers.items():
        c_list = []
        for x in range(D):
            pair_sum = sum(
                amps_by_x[x][a] * amps_by_x[x][b].conjugate() for a, b in pair_list
            )
            c_list.append(pair_sum / norm_denom)
        harmonics[delta] = c_list

    zero_delta = tuple([0] * n)
    c0_real = np.array([c.real for c in harmonics[zero_delta]], dtype=np.float64)

    theo_p_diff = np.zeros(D, dtype=np.float64)
    for Delta in range(D):
        val = 0.0
        for x in range(D):
            x_shift = (x + Delta) % D
            val += c0_real[x] * c0_real[x_shift]
            for delta, c_list in harmonics.items():
                if delta == zero_delta:
                    continue
                prod = c_list[x] * c_list[x_shift].conjugate()
                val += prod.real
        theo_p_diff[Delta] = val

    autocorr_residual = float(np.max(np.abs(emp_p_diff - theo_p_diff)))

    # At Delta = 0: coincidence excess E_s[P_diff(0 | s)] - sum_x C(0; x)^2 == E_{epsilon, sigma} <= V_HS
    ind_coincidence = float(np.sum(c0_real ** 2))
    coincidence_excess = float(emp_p_diff[0]) - ind_coincidence
    l2_signal_energy = sum(
        (c_list[x].real ** 2 + c_list[x].imag ** 2)
        for delta, c_list in harmonics.items()
        if delta != zero_delta
        for x in range(D)
    )
    coincidence_excess_residual = abs(coincidence_excess - l2_signal_energy)

    theorem3_verified = (
        autocorr_residual <= tolerance
        and coincidence_excess_residual <= tolerance
        and coincidence_excess <= v_hs + tolerance
    )

    return {
        "case_id": case_id,
        "D": D,
        "q": q,
        "n": n,
        "k_calls": k,
        "epsilon": list(epsilon),
        "sigma": list(sigma),
        "variety_size_V_epsilon": variety_size,
        "swap_same_secret_expectation": swap_same,
        "swap_independent_secret_expectation": swap_ind,
        "swap_expectation_excess": swap_excess,
        "antisymmetric_independent_prob": anti_ind,
        "purity_rho_bar": purity_rho_bar,
        "purity_sigma_k_flipped": purity_flipped,
        "sigma_k_flip_purity_residual": sigma_flip_residual,
        "k1_rational_purity_exact": _frac_str(k1_purity_exact) if k1_purity_exact is not None else None,
        "v_hs_operator_variance": v_hs,
        "cnot_difference_probs_empirical": [float(v) for v in emp_p_diff],
        "cnot_difference_probs_theoretical": [float(v) for v in theo_p_diff],
        "cnot_autocorrelation_residual": autocorr_residual,
        "same_secret_coincidence_prob_Delta0": float(emp_p_diff[0]),
        "independent_secret_coincidence_prob_Delta0": ind_coincidence,
        "coincidence_excess_Delta0": coincidence_excess,
        "single_copy_l2_signal_energy": l2_signal_energy,
        "coincidence_excess_vs_l2_energy_residual": coincidence_excess_residual,
        "coherent_swap_minus_classical_coincidence_gap": v_hs - coincidence_excess,
        "theorem1_verified": theorem1_verified,
        "theorem2_verified": theorem2_verified,
        "theorem3_verified": theorem3_verified,
        "all_theorems_verified": (
            theorem1_verified and theorem2_verified and theorem3_verified
        ),
    }


def build_native_higher_call_two_copy_swap_purity_bridge(
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> dict[str, Any]:
    contract = load_contract(contract_path)

    case_specs = [
        {
            "case_id": "k1_injective_freq_D3_q3_n2",
            "D": 3,
            "q": 3,
            "n": 2,
            "freq_table": [(1, 0), (0, 1), (1, 1)],
            "error_table": [0, 1, 2],
            "epsilon": (1,),
            "sigma": (1,),
        },
        {
            "case_id": "k1_degenerate_collision_D3_q3_n2",
            "D": 3,
            "q": 3,
            "n": 2,
            "freq_table": [(1, 2), (1, 2), (2, 1)],
            "error_table": [0, 1, 2],
            "epsilon": (1,),
            "sigma": (-1,),
        },
        {
            "case_id": "k2_unsigned_D3_q3_n2",
            "D": 3,
            "q": 3,
            "n": 2,
            "freq_table": [(1, 0), (0, 1), (1, 1)],
            "error_table": [0, 1, 2],
            "epsilon": (1, 1),
            "sigma": (1, -1),
        },
        {
            "case_id": "k2_balanced_signed_D3_q3_n2",
            "D": 3,
            "q": 3,
            "n": 2,
            "freq_table": [(1, 0), (0, 1), (1, 1)],
            "error_table": [0, 1, 2],
            "epsilon": (1, -1),
            "sigma": (1, -1),
        },
        {
            "case_id": "k3_alternating_signed_D3_q3_n2",
            "D": 3,
            "q": 3,
            "n": 2,
            "freq_table": [(1, 0), (0, 1), (1, 1)],
            "error_table": [0, 1, 2],
            "epsilon": (1, -1, 1),
            "sigma": (1, -1, 1),
        },
    ]

    cases = [evaluate_two_copy_swap_case(**spec) for spec in case_specs]
    all_verified = all(c["all_theorems_verified"] for c in cases)

    summary = {
        "case_count": len(cases),
        "all_cases_verified": all_verified,
        "max_cnot_autocorrelation_residual": max(
            c["cnot_autocorrelation_residual"] for c in cases
        ),
        "max_coincidence_excess_residual": max(
            c["coincidence_excess_vs_l2_energy_residual"] for c in cases
        ),
        "scientific_verdict": (
            "Across k in {1, 2, 3} oracle calls, the two-copy coherent SWAP expectation excess between "
            "same-secret and independent-secret pairs equals the full operator Hilbert-Schmidt variance "
            "V_HS(epsilon, sigma) = 1 - Tr(rho_bar^2) (which is invariant under flipping sigma_k -> -sigma_k "
            "and equals 1 - |V_{epsilon_1}(f)|/D^2 for k = 1), whereas post-Fourier modular CNOT difference "
            "readout has coincidence excess at Delta = 0 equal to the computational-basis L2 signal energy "
            "E_{epsilon, sigma} <= V_HS(epsilon, sigma)."
        ),
    }

    payload_without_digest = {
        "schema_version": SCHEMA_VERSION,
        "contract_id": contract["contract_id"],
        "title": contract["title"],
        "status": (
            "VERIFIED_EXACT_TWO_COPY_SWAP_PURITY_AND_CNOT_COINCIDENCE_LAWS"
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


def write_native_higher_call_two_copy_swap_purity_bridge(
    output_path: Path = DEFAULT_ARTIFACT_PATH,
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> dict[str, Any]:
    payload = build_native_higher_call_two_copy_swap_purity_bridge(
        contract_path=contract_path
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build or write the native higher-call two-copy SWAP purity bridge."
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
        payload = write_native_higher_call_two_copy_swap_purity_bridge(
            output_path=args.output
        )
    else:
        payload = build_native_higher_call_two_copy_swap_purity_bridge()

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
