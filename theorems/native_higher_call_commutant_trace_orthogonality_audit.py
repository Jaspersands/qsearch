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
    fourier_matrix_power,
    k_call_statevector,
    signed_net_error_phase,
    signed_net_frequency,
)


SCHEMA_VERSION = "2026-04-12.native-higher-call-commutant-trace-orthogonality-audit.v1"
DEFAULT_CONTRACT_PATH = (
    ROOT
    / "research"
    / "hypotheses"
    / "native_higher_call_commutant_trace_orthogonality_audit_contract.json"
)
DEFAULT_ARTIFACT_PATH = (
    ROOT
    / "research"
    / "reductions"
    / "native_higher_call_commutant_trace_orthogonality_audit.json"
)
DEFAULT_DOC_PATH = (
    ROOT / "research" / "NATIVE_HIGHER_CALL_COMMUTANT_TRACE_ORTHOGONALITY_AUDIT.md"
)


def canonical_sha256(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def load_contract(path: Path = DEFAULT_CONTRACT_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def pre_fourier_phase(w_tuple: tuple[int, ...], sigma: tuple[int, ...], D: int) -> int:
    """Compute Phi_sigma^{pre}(w) = sum_{ell=1}^{k-1} sigma_ell w_{ell+1} w_ell mod D."""
    total = 0
    for ell in range(len(w_tuple) - 1):
        total += sigma[ell] * w_tuple[ell + 1] * w_tuple[ell]
    return total % D


def evaluate_commutant_trace_case(
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
    """Verify Theorems 1, 2, and 3 on the full D x D density-matrix ensemble rho_{epsilon, sigma}(s)."""
    k = len(epsilon)
    secrets = list(itertools.product(range(q), repeat=n))
    num_secrets = len(secrets)

    # 1. Compute rho(s) = |Psi(s)><Psi(s)| for all s in Z_q^n
    rho_by_s = np.zeros((num_secrets, D, D), dtype=np.complex128)
    for s_idx, s in enumerate(secrets):
        y_s = [
            (sum(freq_table[w][j] * s[j] for j in range(n)) + error_table[w]) % q
            for w in range(D)
        ]
        psi = k_call_statevector(D, q, y_s, epsilon, sigma)
        rho_by_s[s_idx] = np.outer(psi, psi.conj())

    rho_bar = np.mean(rho_by_s, axis=0)
    purity_rho_bar = float(np.real(np.trace(rho_bar @ rho_bar)))
    purity_deficit = 1.0 - purity_rho_bar

    # Direct Hilbert-Schmidt variance E_s[||rho(s) - rho_bar||_F^2]
    diffs = rho_by_s - rho_bar[None, :, :]
    hs_variance_direct = float(np.mean(np.sum(np.abs(diffs) ** 2, axis=(1, 2))))

    # 2. Construct pre-Fourier harmonics M_hat(delta) via trajectory pairs pinned at endpoints (u, v)
    trajectories = list(itertools.product(range(D), repeat=k))
    num_traj = len(trajectories)
    tau_list = [signed_net_frequency(w, freq_table, epsilon, q) for w in trajectories]
    err_list = [signed_net_error_phase(w, error_table, epsilon, q) for w in trajectories]
    phi_pre_list = [pre_fourier_phase(w, sigma, D) for w in trajectories]

    pre_amps = []
    for idx in range(num_traj):
        angle = (2.0 * math.pi * err_list[idx] / float(q)) + (
            2.0 * math.pi * phi_pre_list[idx] / float(D)
        )
        pre_amps.append(complex(math.cos(angle), math.sin(angle)))

    m_hat_by_delta: dict[tuple[int, ...], np.ndarray] = defaultdict(
        lambda: np.zeros((D, D), dtype=np.complex128)
    )
    norm_pre = float(D ** k)
    for idx_a, w_a in enumerate(trajectories):
        u = w_a[-1]
        for idx_b, w_b in enumerate(trajectories):
            v = w_b[-1]
            delta = tuple((tau_list[idx_a][j] - tau_list[idx_b][j]) % q for j in range(n))
            m_hat_by_delta[delta][u, v] += (
                pre_amps[idx_a] * pre_amps[idx_b].conjugate() / norm_pre
            )

    F_last = fourier_matrix_power(D, sigma[-1])
    F_last_dag = F_last.conj().T

    rho_hat_by_delta: dict[tuple[int, ...], np.ndarray] = {}
    for delta, M_mat in m_hat_by_delta.items():
        rho_hat_by_delta[delta] = F_last @ M_mat @ F_last_dag

    # Compare rho_hat_by_delta against direct secret-Fourier transform of rho(s)
    max_fourier_inversion_residual = 0.0
    for delta, rho_hat in rho_hat_by_delta.items():
        direct_hat = np.zeros((D, D), dtype=np.complex128)
        for s_idx, s in enumerate(secrets):
            dot_ds = sum(delta[j] * s[j] for j in range(n)) % q
            phase = np.exp(-2j * np.pi * dot_ds / float(q))
            direct_hat += rho_by_s[s_idx] * phase
        direct_hat /= float(num_secrets)
        res = float(np.max(np.abs(rho_hat - direct_hat)))
        max_fourier_inversion_residual = max(max_fourier_inversion_residual, res)

    zero_delta = tuple([0] * n)

    # Verify Theorem 1:
    # (a) Adjoint symmetry: rho_hat(-delta) == rho_hat(delta)^dagger
    # (b) Trace orthogonality: Tr(rho_hat(0)) == 1, Tr(rho_hat(delta)) == 0 for delta != 0
    max_adjoint_residual = 0.0
    max_nonzero_trace_residual = 0.0
    for delta, rho_hat in rho_hat_by_delta.items():
        neg_delta = tuple((-c) % q for c in delta)
        neg_mat = rho_hat_by_delta[neg_delta]
        adj_res = float(np.max(np.abs(neg_mat - rho_hat.conj().T)))
        max_adjoint_residual = max(max_adjoint_residual, adj_res)
        if delta != zero_delta:
            tr_res = abs(complex(np.trace(rho_hat)))
            max_nonzero_trace_residual = max(max_nonzero_trace_residual, tr_res)

    tr_zero_residual = abs(complex(np.trace(rho_hat_by_delta[zero_delta])) - 1.0)
    theorem1_verified = (
        max_fourier_inversion_residual <= tolerance
        and max_adjoint_residual <= tolerance
        and max_nonzero_trace_residual <= tolerance
        and tr_zero_residual <= tolerance
    )

    # Verify Theorem 2:
    # V_HS == 1 - Tr(rho_bar^2) == sum_{delta != 0} ||rho_hat(delta)||_F^2 == sum_{delta != 0} ||M_hat(delta)||_F^2 <= 1 - 1/D
    sum_frob_rho_hat = sum(
        float(np.sum(np.abs(mat) ** 2))
        for delta, mat in rho_hat_by_delta.items()
        if delta != zero_delta
    )
    sum_frob_m_hat = sum(
        float(np.sum(np.abs(mat) ** 2))
        for delta, mat in m_hat_by_delta.items()
        if delta != zero_delta
    )
    hs_vs_purity_deficit_residual = abs(hs_variance_direct - purity_deficit)
    hs_vs_parseval_rho_residual = abs(hs_variance_direct - sum_frob_rho_hat)
    hs_vs_parseval_m_residual = abs(hs_variance_direct - sum_frob_m_hat)

    theorem2_verified = (
        hs_vs_purity_deficit_residual <= tolerance
        and hs_vs_parseval_rho_residual <= tolerance
        and hs_vs_parseval_m_residual <= tolerance
        and purity_deficit <= (1.0 - 1.0 / float(D)) + tolerance
    )

    # Verify Theorem 3 across 3 canonical readout unitaries V in U(D):
    # (1) V = I_D (standard Fourier readout)
    # (2) V = F_last_dag (computational pre-Fourier readout)
    # (3) V = eigenbasis of rho_bar (which diagonalizes rho_bar)
    _, eigvecs_rho_bar = np.linalg.eigh(rho_bar)
    unitary_tests = [
        ("identity_fourier_basis", np.eye(D, dtype=np.complex128)),
        ("inverse_fourier_computational_basis", F_last_dag),
        ("rho_bar_eigenbasis", eigvecs_rho_bar.conj().T),
    ]

    basis_evaluations = []
    max_conservation_residual = 0.0
    theorem3_bounds_hold = True

    for b_name, V in unitary_tests:
        diag_energy = 0.0
        off_diag_energy = 0.0
        for delta, rho_hat in rho_hat_by_delta.items():
            if delta == zero_delta:
                continue
            rot_mat = V @ rho_hat @ V.conj().T
            diag_entries = np.diag(rot_mat)
            diag_sq = float(np.sum(np.abs(diag_entries) ** 2))
            total_sq = float(np.sum(np.abs(rot_mat) ** 2))
            diag_energy += diag_sq
            off_diag_energy += (total_sq - diag_sq)

        cons_res = abs((diag_energy + off_diag_energy) - purity_deficit)
        max_conservation_residual = max(max_conservation_residual, cons_res)
        if diag_energy > purity_deficit + tolerance or diag_energy > (1.0 - 1.0 / float(D)) + tolerance:
            theorem3_bounds_hold = False

        basis_evaluations.append(
            {
                "basis_name": b_name,
                "diagonal_l2_signal_energy": diag_energy,
                "off_diagonal_coherence_energy": off_diag_energy,
                "sum_energy": diag_energy + off_diag_energy,
                "conservation_residual": cons_res,
                "captured_fraction_of_hs_variance": (
                    diag_energy / purity_deficit if purity_deficit > 0.0 else 0.0
                ),
            }
        )

    theorem3_verified = (
        theorem3_bounds_hold and max_conservation_residual <= tolerance
    )

    return {
        "case_id": case_id,
        "D": D,
        "q": q,
        "n": n,
        "k_calls": k,
        "epsilon": list(epsilon),
        "sigma": list(sigma),
        "distinct_active_harmonics": len(rho_hat_by_delta),
        "purity_rho_bar": purity_rho_bar,
        "purity_deficit_1_minus_tr_rho_bar_sq": purity_deficit,
        "universal_max_purity_deficit_1_minus_1_over_D": 1.0 - 1.0 / float(D),
        "hs_variance_direct": hs_variance_direct,
        "sum_frob_nonzero_rho_hat": sum_frob_rho_hat,
        "sum_frob_nonzero_m_hat": sum_frob_m_hat,
        "max_fourier_inversion_residual": max_fourier_inversion_residual,
        "max_adjoint_residual": max_adjoint_residual,
        "max_nonzero_trace_residual": max_nonzero_trace_residual,
        "hs_vs_purity_deficit_residual": hs_vs_purity_deficit_residual,
        "hs_vs_parseval_rho_residual": hs_vs_parseval_rho_residual,
        "max_conservation_residual": max_conservation_residual,
        "basis_evaluations": basis_evaluations,
        "theorem1_verified": theorem1_verified,
        "theorem2_verified": theorem2_verified,
        "theorem3_verified": theorem3_verified,
        "all_theorems_verified": (
            theorem1_verified and theorem2_verified and theorem3_verified
        ),
    }


def build_native_higher_call_commutant_trace_orthogonality_audit(
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> dict[str, Any]:
    contract = load_contract(contract_path)

    case_specs = [
        {
            "case_id": "k1_single_call_D3_q3_n2",
            "D": 3,
            "q": 3,
            "n": 2,
            "freq_table": [(1, 0), (0, 1), (1, 1)],
            "error_table": [0, 1, 2],
            "epsilon": (1,),
            "sigma": (1,),
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
        {
            "case_id": "k3_prime_power_D3_q9_n1",
            "D": 3,
            "q": 9,
            "n": 1,
            "freq_table": [(1,), (2,), (4,)],
            "error_table": [0, 3, 6],
            "epsilon": (1, -1, 1),
            "sigma": (1, 1, -1),
        },
    ]

    cases = [evaluate_commutant_trace_case(**spec) for spec in case_specs]
    all_verified = all(c["all_theorems_verified"] for c in cases)

    summary = {
        "case_count": len(cases),
        "all_cases_verified": all_verified,
        "max_nonzero_trace_residual": max(
            c["max_nonzero_trace_residual"] for c in cases
        ),
        "max_hs_vs_purity_deficit_residual": max(
            c["hs_vs_purity_deficit_residual"] for c in cases
        ),
        "max_conservation_residual": max(
            c["max_conservation_residual"] for c in cases
        ),
        "scientific_verdict": (
            "Across k in {1, 2, 3} oracle calls and prime/prime-power moduli, the matrix secret-Fourier "
            "harmonics rho_hat(delta) satisfy exact Hermitian conjugation rho_hat(-delta) = rho_hat(delta)^dagger "
            "and trace orthogonality Tr(rho_hat(delta)) = 0 for all delta != 0. The full operator Hilbert-Schmidt "
            "variance E_s[||rho(s) - rho_bar||_F^2] equals the exact purity deficit 1 - Tr(rho_bar^2) = "
            "sum_{delta != 0} ||rho_hat(delta)||_F^2 <= 1 - 1/D, which universally upper-bounds the L2 readout "
            "signal energy of any post-circuit unitary basis rotation V in U(D)."
        ),
    }

    payload_without_digest = {
        "schema_version": SCHEMA_VERSION,
        "contract_id": contract["contract_id"],
        "title": contract["title"],
        "status": (
            "VERIFIED_EXACT_OPERATOR_COMMUTANT_TRACE_AND_PURITY_DEFICIT_LAWS"
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


def write_native_higher_call_commutant_trace_orthogonality_audit(
    output_path: Path = DEFAULT_ARTIFACT_PATH,
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> dict[str, Any]:
    payload = build_native_higher_call_commutant_trace_orthogonality_audit(
        contract_path=contract_path
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build or write the native higher-call commutant trace-orthogonality audit."
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
        payload = write_native_higher_call_commutant_trace_orthogonality_audit(
            output_path=args.output
        )
    else:
        payload = build_native_higher_call_commutant_trace_orthogonality_audit()

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
