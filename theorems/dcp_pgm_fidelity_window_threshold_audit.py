from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import sys
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.dcp_noisy_tree_merge_error_propagation_audit import cyclic_convolve_power


SCHEMA_VERSION = "2026-04-12.dcp-pgm-fidelity-window-threshold-audit.v1"
DEFAULT_CONTRACT_PATH = (
    ROOT
    / "research"
    / "hypotheses"
    / "dcp_pgm_fidelity_window_threshold_audit_contract.json"
)
DEFAULT_ARTIFACT_PATH = (
    ROOT
    / "research"
    / "phase_workbench"
    / "dcp_pgm_fidelity_window_threshold_audit.json"
)
DEFAULT_DOC_PATH = (
    ROOT / "research" / "DCP_PGM_FIDELITY_WINDOW_THRESHOLD_AUDIT.md"
)


def canonical_sha256(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _frac_str(val: Fraction) -> str:
    return f"{val.numerator}/{val.denominator}"


def load_contract(path: Path = DEFAULT_CONTRACT_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def exact_pgm_operator_success(q: int, p_profile: np.ndarray, K: int) -> float:
    """Compute exact K-copy PGM success probability by constructing the Gram matrix of {|psi_s>^{otimes K}}."""
    # <psi_{s'} | psi_s> = sum_u p_u omega_q^{(s' - s) u}
    # For K copies: <Psi_{s'} | Psi_s> = (<psi_{s'} | psi_s>)^K
    # Since the Gram matrix G_{s', s} = (<psi_{s'} | psi_s>)^K is circulant of size q x q,
    # its eigenvalues are q * W_K(m), and the PGM success probability is (1/q^2) (Tr(sqrt(G)))^2.
    # Here we explicitly build the q x q circulant Gram matrix G and take its Hermitian square root!
    u_grid = np.arange(q, dtype=np.float64)
    G = np.zeros((q, q), dtype=np.complex128)
    for s_prime in range(q):
        for s in range(q):
            diff = (s_prime - s) % q
            inner_1 = np.sum(p_profile * np.exp(2j * np.pi * diff * u_grid / float(q)))
            G[s_prime, s] = inner_1 ** K

    eigvals = np.linalg.eigvalsh(G)
    eigvals_clipped = np.where(eigvals > 1e-14, eigvals, 0.0)
    tr_sqrt_G = float(np.sum(np.sqrt(eigvals_clipped)))
    return (tr_sqrt_G ** 2) / float(q * q)


def bhattacharyya_convolution_pgm_success(q: int, p_profile: np.ndarray, K: int) -> tuple[float, np.ndarray]:
    """Compute P_PGM^succ(K; p) = (1/q) * (sum_m sqrt(W_K(m)))^2 via K-fold cyclic convolution W_K = p^{*K}."""
    W_K = cyclic_convolve_power(p_profile, K)
    sqrt_sum = float(np.sum(np.sqrt(np.maximum(W_K, 0.0))))
    return (sqrt_sum ** 2) / float(q), W_K


def minimum_contiguous_copies_for_tau(q: int, R: int, tau: float) -> int:
    """Return ceil((tau * q - 1) / (R - 1)) for R >= 2."""
    if R < 2:
        raise ValueError("R must be >= 2")
    val = (tau * float(q) - 1.0) / float(R - 1)
    return max(1, int(math.ceil(val - 1e-15)))


def evaluate_pgm_window_case(
    *,
    case_id: str,
    q: int,
    R: int,
    profile_kind: str,
    max_K: int,
    target_tau: float = 0.75,
    tolerance: float = 1e-12,
) -> dict[str, Any]:
    """Verify Theorems 1, 2, and 3 across K = 1, ..., max_K for a contiguous window profile of width R."""
    p_profile = np.zeros(q, dtype=np.float64)
    if profile_kind == "flat":
        for u in range(R):
            p_profile[u] = 1.0 / float(R)
    elif profile_kind == "tapered":
        weights = np.array([float(R - abs(2 * u - (R - 1))) for u in range(R)], dtype=np.float64)
        weights /= np.sum(weights)
        for u in range(R):
            p_profile[u] = weights[u]
    else:
        raise ValueError(f"Unknown profile_kind: {profile_kind}")

    k_rows = []
    max_gram_vs_bhattacharyya_residual = 0.0
    theorem2_bound_holds = True
    theorem3_support_and_bound_holds = True

    k_min_bound = minimum_contiguous_copies_for_tau(q, R, target_tau)

    for K in range(1, max_K + 1):
        p_gram = exact_pgm_operator_success(q, p_profile, K)
        p_bhat, W_K = bhattacharyya_convolution_pgm_success(q, p_profile, K)
        res = abs(p_gram - p_bhat)
        max_gram_vs_bhattacharyya_residual = max(max_gram_vs_bhattacharyya_residual, res)

        support_count = int(np.sum(W_K > 1e-15))
        expected_support_count = min(q, K * (R - 1) + 1)
        support_upper_bound = float(support_count) / float(q)
        contiguous_upper_bound = min(1.0, float(K * (R - 1) + 1) / float(q))

        if p_bhat > support_upper_bound + tolerance:
            theorem2_bound_holds = False
        if K == 1 and profile_kind == "flat":
            if abs(p_bhat - (float(R) / float(q))) > tolerance:
                theorem2_bound_holds = False
        if K == 1 and profile_kind == "tapered" and R >= 3:
            if not (p_bhat < (float(R) / float(q)) - 1e-9):
                theorem2_bound_holds = False

        if support_count != expected_support_count:
            theorem3_support_and_bound_holds = False
        if p_bhat > contiguous_upper_bound + tolerance:
            theorem3_support_and_bound_holds = False
        if p_bhat >= target_tau - tolerance and K < k_min_bound:
            theorem3_support_and_bound_holds = False

        k_rows.append(
            {
                "K_copies": K,
                "pgm_success_gram_operator": p_gram,
                "pgm_success_bhattacharyya_convolution": p_bhat,
                "gram_vs_bhattacharyya_residual": res,
                "observed_support_size": support_count,
                "expected_contiguous_support_size": expected_support_count,
                "support_ratio_upper_bound_exact": _frac_str(Fraction(expected_support_count, q)),
                "support_ratio_upper_bound_float": contiguous_upper_bound,
                "cauchy_schwarz_slack": contiguous_upper_bound - p_bhat,
                "meets_target_tau": (p_bhat >= target_tau),
            }
        )

    theorem1_verified = max_gram_vs_bhattacharyya_residual <= tolerance

    return {
        "case_id": case_id,
        "q": q,
        "R": R,
        "profile_kind": profile_kind,
        "max_K": max_K,
        "target_tau": target_tau,
        "minimum_copy_lower_bound_for_tau": k_min_bound,
        "base_profile": [float(v) for v in p_profile],
        "max_gram_vs_bhattacharyya_residual": max_gram_vs_bhattacharyya_residual,
        "k_rows": k_rows,
        "theorem1_verified": theorem1_verified,
        "theorem2_verified": theorem2_bound_holds,
        "theorem3_verified": theorem3_support_and_bound_holds,
        "all_theorems_verified": (
            theorem1_verified and theorem2_bound_holds and theorem3_support_and_bound_holds
        ),
    }


def build_dcp_pgm_fidelity_window_threshold_audit(
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> dict[str, Any]:
    contract = load_contract(contract_path)

    case_specs = [
        {
            "case_id": "q13_R3_flat_window_K6",
            "q": 13,
            "R": 3,
            "profile_kind": "flat",
            "max_K": 6,
            "target_tau": 0.75,
        },
        {
            "case_id": "q13_R3_tapered_window_K6",
            "q": 13,
            "R": 3,
            "profile_kind": "tapered",
            "max_K": 6,
            "target_tau": 0.75,
        },
        {
            "case_id": "q17_R4_flat_window_K6",
            "q": 17,
            "R": 4,
            "profile_kind": "flat",
            "max_K": 6,
            "target_tau": 0.75,
        },
        {
            "case_id": "q17_R4_tapered_window_K6",
            "q": 17,
            "R": 4,
            "profile_kind": "tapered",
            "max_K": 6,
            "target_tau": 0.75,
        },
        {
            "case_id": "q25_R5_flat_window_K6",
            "q": 25,
            "R": 5,
            "profile_kind": "flat",
            "max_K": 6,
            "target_tau": 0.80,
        },
    ]

    cases = [evaluate_pgm_window_case(**spec) for spec in case_specs]
    all_verified = all(c["all_theorems_verified"] for c in cases)

    summary = {
        "case_count": len(cases),
        "all_cases_verified": all_verified,
        "max_gram_vs_bhattacharyya_residual": max(
            c["max_gram_vs_bhattacharyya_residual"] for c in cases
        ),
        "scientific_verdict": (
            "Exact Gram-operator spectral square-root evaluation and K-fold cyclic convolution confirm "
            "that the K-copy shift-covariant Pretty Good Measurement success probability on Z_q equals "
            "(1/q)(sum_m sqrt(W_K(m)))^2, bounded above by |supp(W_K)| / q with K=1 equality if and only if "
            "the Fourier profile is flat on its support. For any contiguous window of width R, the K-fold "
            "sumset support grows linearly as min(q, K(R-1)+1), enforcing the hard copy lower bound "
            "K >= ceil((tau*q - 1)/(R - 1))."
        ),
    }

    payload_without_digest = {
        "schema_version": SCHEMA_VERSION,
        "contract_id": contract["contract_id"],
        "title": contract["title"],
        "status": (
            "VERIFIED_EXACT_PGM_BHATTACHARYYA_WINDOW_THRESHOLD_LAWS"
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


def write_dcp_pgm_fidelity_window_threshold_audit(
    output_path: Path = DEFAULT_ARTIFACT_PATH,
    contract_path: Path = DEFAULT_CONTRACT_PATH,
) -> dict[str, Any]:
    payload = build_dcp_pgm_fidelity_window_threshold_audit(contract_path=contract_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build or write the DCP PGM fidelity window-threshold audit."
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
        payload = write_dcp_pgm_fidelity_window_threshold_audit(output_path=args.output)
    else:
        payload = build_dcp_pgm_fidelity_window_threshold_audit()

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
